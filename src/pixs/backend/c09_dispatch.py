"""Boucles locales C09 : une unité propriétaire à la fois, aucun exécutant JSON."""
from __future__ import annotations

import dataclasses
import inspect
import threading
import time
from dataclasses import dataclass
from types import FunctionType

from django.db import transaction
from django.db.models import Q, Exists, OuterRef

from pixs.backend.c09_authorization_adapter import C09AuthorizationRefused, C09Refused, c09_pg_now, c09_text
from pixs.backend.c09_job_repository import (
    C09JobRepository, C09LeaseHandle, C09TechnicalRetryable, C09BusinessRefused)
from pixs.backend.c09_outbox_repository import C09OutboxRepository, C09OutboxHandle
from pixs.backend.c09_inbox_repository import C09InboxRepository
from pixs.backend.c09_scheduler import C09Scheduler
from pixs.backend.c09_runtime_repository import C09BoundedJobAdmission
from pixs.core.c09_owner_participant import C09CoreOwnerParticipant, C09CoreJobUnit, C09CoreInboxUnit
from pixs.core.c09_outbox_participant import C09CoreOutboxParticipant
from pixs.core.dto import CommandEnvelope
from pixs.core.ports import CoreServicePorts
from pixs.core.services_common import CoreServiceError

__all__=["C09CoreInvocation","C09DispatchResult","invoke_c09_core",
         "C09JobDriver","C09PublisherDriver","C09SchedulerDriver"]


@dataclass(frozen=True,slots=True,repr=False)
class C09CoreInvocation:
    service: object
    command: object
    envelope: CommandEnvelope
    ports: CoreServicePorts
    alias: str


@dataclass(frozen=True,slots=True,repr=False)
class C09DispatchResult:
    outcome: str
    work_reference: str | None
    detail: str


def _core_owner(invocation):
    if type(invocation) is not C09CoreInvocation or type(invocation.ports) is not CoreServicePorts:
        raise C09Refused()
    if type(invocation.envelope) is not CommandEnvelope:
        raise C09Refused()
    invocation.envelope.__post_init__()
    owner=invocation.ports.idempotence
    if (type(owner) is not C09CoreOwnerParticipant
            or type(invocation.ports.outbox) is not C09CoreOutboxParticipant
            or invocation.ports.outbox.owner is not owner or owner._outbox is not invocation.ports.outbox
            or owner.envelope is not invocation.envelope or invocation.alias!=owner.using):
        raise C09Refused()
    return owner


def invoke_c09_core(invocation):
    _core_owner(invocation)
    # Registre fermé de fonctions publiques installées, jamais d'import issu du payload.
    from pixs.core import services_identity,services_scope,services_groups,services_authz
    allowed=[]
    for module in (services_identity,services_scope,services_groups,services_authz):
        for name in module.__all__:
            candidate=getattr(module,name)
            if type(candidate) is FunctionType and {"command","envelope","ports","alias"}.issubset(
                    inspect.signature(candidate).parameters):
                allowed.append(candidate)
    if not any(invocation.service is candidate for candidate in allowed):
        raise C09Refused("C09_POLICY_UNRESOLVED")
    return invocation.service(command=invocation.command,envelope=invocation.envelope,
                               ports=invocation.ports,alias=invocation.alias)


class C09JobDriver:
    def __init__(self,*,repository,policy,transaction_mode,core_factory):
        if type(repository) is not C09JobRepository or type(transaction_mode) is not str:
            raise C09Refused()
        repository._owned_policy(policy)
        if transaction_mode=="JOINED":
            if core_factory is not None:
                raise C09Refused()
        elif transaction_mode=="CORE_DURABLE":
            if type(core_factory) is not FunctionType:
                raise C09Refused("C09_POLICY_UNRESOLVED")
        else:
            raise C09Refused()
        self.repository,self.policy,self.mode=repository,policy,transaction_mode
        self.core_factory=core_factory
        self._stop=threading.Event()
        self.last_job=None
        self.last_lease=None

    def request_stop(self):
        self._stop.set()

    def _current_lease(self,owner):
        if self.last_job is not None:
            with transaction.atomic(using=self.repository.using):
                ext=self.repository._query().filter(pk=self.last_job).first()
                if ext is None:
                    raise C09Refused()
                row,_,_=self.repository._load(ext)
                if row.state=="RUNNING" and row.lease_owner==owner:
                    try:
                        self.repository._authorize(ext)
                    except C09AuthorizationRefused as error:
                        self.repository._deny(ext,error)
                        self.last_lease=None
                        return None
                    if self.repository._expired(ext,c09_pg_now(self.repository.using)):
                        self.repository._retry(ext,self.policy,c09_pg_now(self.repository.using),"LEASE_EXPIRED")
                        self.last_lease=None
                        return None
                    self.last_lease=self.repository._handle(ext)
                    return self.last_lease
                self.last_lease=None
        handle=self.repository.acquire_next(owner=owner,policy=self.policy)
        if handle is not None:
            self.last_job,self.last_lease=handle.job_id,handle
        return handle

    def _fail_owned(self,handle):
        with transaction.atomic(using=self.repository.using):
            ext=self.repository._lease(handle,self.policy)
            try:
                self.repository._authorize(ext)
            except C09AuthorizationRefused as error:
                self.repository._deny(ext,error)
            else:
                self.repository._clear(ext,"FAILED","BUSINESS_REFUSED")
                self.repository._save(ext)
            self.last_lease=None
            return C09DispatchResult("KNOWN",handle.job_id,"OWNER_REFUSED")

    def step(self,*,owner):
        c09_text(owner)
        if self._stop.is_set():
            return C09DispatchResult("IDLE",None,"ADMISSION_CLOSED")
        handle=self._current_lease(owner)
        if handle is None:
            return C09DispatchResult("IDLE",self.last_job,"NO_ELIGIBLE_JOB")
        if self._stop.is_set():
            self.repository.restitute(handle=handle,policy=self.policy)
            self.last_lease=None
            return C09DispatchResult("KNOWN",handle.job_id,"RESTITUTED")
        try:
            if self.mode=="JOINED":
                result=self.repository.run_unit(handle=handle,policy=self.policy)
                self.last_lease=result.lease
                return C09DispatchResult("KNOWN",handle.job_id,result.view.state)
            view=self.repository.inspect(job_id=handle.job_id,policy=self.policy)
            invocation=self.core_factory(handle=handle,view=view,owner_reference=owner)
            participant=_core_owner(invocation)
            unit=participant.unit
            if (type(unit) is not C09CoreJobUnit or unit.repository is not self.repository
                    or unit.handle!=handle or unit.job_id!=handle.job_id or unit.policy!=self.policy):
                raise C09Refused()
            if self._stop.is_set():
                self.repository.restitute(handle=handle,policy=self.policy)
                self.last_lease=None
                return C09DispatchResult("KNOWN",handle.job_id,"RESTITUTED")
            invoke_c09_core(invocation)
            observed=self.repository.inspect(job_id=handle.job_id,policy=self.policy)
            self.last_lease=(C09LeaseHandle(handle.job_id,owner,observed.lease_generation,observed.revision)
                             if observed.state=="RUNNING" else None)
            return C09DispatchResult("KNOWN",handle.job_id,observed.state)
        except CoreServiceError as error:
            if error.code in ("ISSUE_INCONNUE","AUDIT_REFUS_INDISPONIBLE"):
                return C09DispatchResult("UNKNOWN",handle.job_id,"CORE_OUTCOME_UNRESOLVED")
            try:
                return self._fail_owned(handle)
            except C09Refused:
                return C09DispatchResult("UNKNOWN",handle.job_id,"OWNER_STATE_UNRESOLVED")

    def shutdown(self,*,owner):
        self.request_stop()
        if self.last_lease is None:
            return C09DispatchResult("KNOWN",self.last_job,"QUIESCENT")
        observed=self.repository.inspect(job_id=self.last_job,policy=self.policy)
        if observed.state=="RUNNING":
            candidate=C09LeaseHandle(self.last_job,owner,observed.lease_generation,observed.revision)
            self.repository.restitute(handle=candidate,policy=self.policy)
        self.last_lease=None
        return C09DispatchResult("KNOWN",self.last_job,"RESTITUTED")


class C09PublisherDriver:
    def __init__(self,*,outbox,inbox,core_factory):
        if type(outbox) is not C09OutboxRepository or type(inbox) is not C09InboxRepository or inbox.outbox is not outbox:
            raise C09Refused()
        if core_factory is not None and type(core_factory) is not FunctionType:
            raise C09Refused()
        for binding in inbox._bindings.values():
            if binding.transaction_mode=="CORE_DURABLE" and core_factory is None:
                raise C09Refused("C09_POLICY_UNRESOLVED")
        if set(inbox._bindings)!={consumer.consumer_reference for consumer in outbox._registry.consumers}:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        self.outbox,self.inbox,self.core_factory=outbox,inbox,core_factory
        self._stop=threading.Event()
        self.handle=None

    def request_stop(self):
        self._stop.set()

    def _next(self,owner):
        from pixs.backend.c09_event_records import C09OutboxPublicationRecord as Publication
        with transaction.atomic(using=self.outbox.using):
            now=c09_pg_now(self.outbox.using)
            policies=tuple(self.outbox._policies.values())
            maximum=min(p.base_policy.polling_max_batch for p in policies)
            due=Q(state="PENDING")|Q(state="RETRYING",next_attempt_at__lte=now)|Q(state="RUNNING",lease_expires_at__lte=now)
            earlier=Publication.objects.using(self.outbox.using).filter(
                event__cursor_id=OuterRef("event__cursor_id"),
                event__sequence_index__lt=OuterRef("event__sequence_index")).exclude(state="PUBLISHED")
            refs=tuple(Publication.objects.using(self.outbox.using).annotate(
                c09_order_blocked=Exists(earlier)).filter(c09_order_blocked=False).filter(
                due,event__perimeter_reference=self.outbox._perimeter,
                event__cursor__scope_type=self.outbox._scope.scope_type.value,
                event__cursor__tenant_id=self.outbox._scope.tenant_id,
                event__cursor__scope_id=self.outbox._scope.scope_id).order_by(
                    "event__occurred_at","event_id").values_list("event_id",flat=True)[:maximum])
        for reference in refs:
            if self._stop.is_set():
                return None
            handle=self.outbox.acquire(event_id=reference,owner=owner)
            if handle is not None:
                return handle
        return None

    def step(self,*,owner):
        c09_text(owner)
        if self._stop.is_set():
            return C09DispatchResult("IDLE",None,"ADMISSION_CLOSED")
        if self.handle is None:
            self.handle=self._next(owner)
        if self.handle is None:
            return C09DispatchResult("IDLE",None,"NO_ELIGIBLE_EVENT")
        reference=self.handle.event_id
        envelope,destinations=self.outbox.pending_deliveries(handle=self.handle)
        if not destinations:
            return C09DispatchResult("UNKNOWN",reference,"RECEIPTS_REQUIRE_RECONCILIATION")
        destination=destinations[0]
        try:
            binding=self.inbox._binding(destination.consumer_reference)
            if binding.transaction_mode=="JOINED":
                receipt=self.inbox.consume(envelope=envelope,consumer_reference=destination.consumer_reference,
                                            publisher_handle=self.handle)
            else:
                invocation=self.core_factory(envelope=envelope,consumer_reference=destination.consumer_reference,
                                               publisher_handle=self.handle,owner_reference=owner)
                participant=_core_owner(invocation)
                unit=participant.unit
                if (type(unit) is not C09CoreInboxUnit or unit.repository is not self.inbox
                        or unit.envelope!=envelope or unit.consumer_reference!=destination.consumer_reference
                        or unit.publisher_handle!=self.handle):
                    raise C09Refused()
                invoke_c09_core(invocation)
                receipt=self.inbox.reconcile(envelope=envelope,consumer_reference=destination.consumer_reference)
            if receipt.outcome not in ("CONSUMED","REPLAY","CONFIRMED") or receipt.receipt_reference is None:
                return C09DispatchResult("UNKNOWN",reference,"CONSUMER_OUTCOME_UNRESOLVED")
            if self._stop.is_set():
                return C09DispatchResult("KNOWN",reference,"RECEIPT_COMMITTED_ACK_DEFERRED")
            result=self.outbox.acknowledge(handle=self.handle,consumer_reference=destination.consumer_reference,
                                            receipt_reference=receipt.receipt_reference)
            self.handle=result if type(result) is C09OutboxHandle else None
            return C09DispatchResult("KNOWN",reference,"DELIVERY_CONFIRMED")
        except C09TechnicalRetryable:
            self.outbox.fail(handle=self.handle,kind="RETRYABLE_ERROR")
            self.handle=None
            return C09DispatchResult("KNOWN",reference,"RETRYING")
        except C09BusinessRefused:
            self.outbox.fail(handle=self.handle,kind="BUSINESS_REFUSED")
            self.handle=None
            return C09DispatchResult("KNOWN",reference,"BUSINESS_REFUSED")
        except CoreServiceError as error:
            if error.code in ("ISSUE_INCONNUE","AUDIT_REFUS_INDISPONIBLE"):
                return C09DispatchResult("UNKNOWN",reference,"CORE_OUTCOME_UNRESOLVED")
            self.outbox.fail(handle=self.handle,kind="BUSINESS_REFUSED")
            self.handle=None
            return C09DispatchResult("KNOWN",reference,"CORE_REFUSED")

    def shutdown(self,*,owner):
        self.request_stop()
        reference=None if self.handle is None else self.handle.event_id
        if self.handle is not None:
            if self.handle.owner!=owner:
                raise C09Refused()
            self.outbox.restitute(handle=self.handle)
            self.handle=None
        return C09DispatchResult("KNOWN",reference,"RESTITUTED")


class C09SchedulerDriver:
    def __init__(self,*,scheduler,admission):
        if type(scheduler) is not C09Scheduler or type(admission) is not C09BoundedJobAdmission:
            raise C09Refused()
        if admission.repository is not scheduler.jobs or admission.perimeter!=scheduler._perimeter or admission.scope!=scheduler._scope:
            raise C09Refused()
        self.scheduler,self.admission=scheduler,admission
        self.handle=None
        self._stop=threading.Event()
        self._renew_at=None

    def request_stop(self):
        self._stop.set()

    def step(self,*,owner):
        c09_text(owner)
        if self._stop.is_set():
            return C09DispatchResult("IDLE",None,"ADMISSION_CLOSED")
        if self.handle is None:
            self.handle=self.scheduler.acquire_lease(owner=owner)
            self._renew_at=time.monotonic()+self.scheduler._coordination_policy.renewal_seconds
        if self.handle is None:
            return C09DispatchResult("IDLE",None,"COORDINATOR_HELD")
        if time.monotonic()>=self._renew_at:
            self.handle=self.scheduler.renew(handle=self.handle)
            self._renew_at=time.monotonic()+self.scheduler._coordination_policy.renewal_seconds
        with self.admission.coordination() as available:
            if available<1 or self._stop.is_set():
                return C09DispatchResult("IDLE",None,"QUEUE_FULL_OR_CLOSED")
            results=self.scheduler.trigger_due(handle=self.handle,max_triggers=1)
        return C09DispatchResult("KNOWN" if results else "IDLE",
                                  None if not results else results[0].schedule_ref,"SCHEDULE_TRIGGERED" if results else "NO_DUE_SCHEDULE")

    def shutdown(self,*,owner):
        self.request_stop()
        if self.handle is not None:
            if self.handle.owner!=owner:
                raise C09Refused()
            # Arrêt ciblé du détenteur, sans fermer l'admission du périmètre partagé.
            self.scheduler.restitute(handle=self.handle)
            self.handle=None
        return C09DispatchResult("KNOWN",None,"COORDINATOR_RESTITUTED")
