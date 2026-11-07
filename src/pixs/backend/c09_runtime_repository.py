"""Coordination technique C09 : slots PG et admission Job bornée.

Ces slots n'accordent aucun droit métier et ne prouvent aucun effet achevé.
Les fonctions d'observation sont issues de la composition serveur sélectionnée.
"""
from __future__ import annotations

import hashlib
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from types import FunctionType

from django.db import connections, transaction

from pixs.backend.c09_authorization_adapter import (
    C09AuthorizationRefused, C09Refused, c09_pg_now, c09_text, c09_utc, validate_c09_identity)
from pixs.backend.c09_job_repository import C09JobRepository
from pixs.backend.c09_outbox_repository import _integer, _json, _native, _plus, _scope
from pixs.backend.c09_runtime_plan import (
    c09_role_plan, c09_runtime_plan_sha256, validate_c09_applied_observation, _fresh, _version)
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent
from pixs.core.ports import StagedRef, TransactionProof

__all__ = ["C09RuntimeHandle", "C09RuntimeView", "C09RuntimeRepository", "C09BoundedJobAdmission", "C09RuntimeRecoveryObservationV1"]
_I64 = 2**63-1


@dataclass(frozen=True, slots=True, repr=False)
class C09RuntimeHandle:
    instance_ref: str
    process_reference: str
    generation: int
    revision: int


@dataclass(frozen=True, slots=True, repr=False)
class C09RuntimeView:
    instance_ref: str
    role: str
    stop_state: str
    admission_closed: bool
    inflight_count: int
    generation: int
    revision: int



@dataclass(frozen=True, slots=True, repr=False)
class C09RuntimeRecoveryObservationV1:
    source_reference: str
    source_version: str
    environment_reference: str
    revision: int
    observed_at: object
    valid_until: object
    instance_ref: str
    process_reference: str
    generation: int
    slot_revision: int
    state: str
    active_units: int
    unknown_units: int
    readmission_reference: str
    readmission_version: str


def _model():
    from pixs.backend.c09_event_records import C09RuntimeInstanceRecord
    return C09RuntimeInstanceRecord


def _lock(using, namespace, document):
    native = _native(using)
    key = int.from_bytes(hashlib.sha256(_json(
        [namespace, native[0][2:], document])).digest()[:8], "big", signed=True)
    with connections[using].cursor() as cursor:
        cursor.execute("SELECT pg_advisory_xact_lock(%s)", (key,))


class C09RuntimeRepository:
    def __init__(self, *, using, plan, role, process_index, budget_source, applied_source):
        c09_text(using)
        selected = c09_role_plan(plan, role)
        if type(process_index) is not int or not 0 <= process_index < selected.policy.process_count:
            raise C09Refused("C09_CAPACITY_INVALID")
        if type(budget_source) is not FunctionType or type(applied_source) is not FunctionType:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        self.using, self.plan, self.role, self.index = using, plan, role, process_index
        self.policy, self.plan_sha = selected.policy, c09_runtime_plan_sha256(plan)
        self._budget_source, self._applied_source = budget_source, applied_source
        self.environment_key = "c09-env:"+hashlib.sha256(_json(
            ["C09_RUNTIME_ENV_V1", plan.environment_reference])).hexdigest()
        self.instance_ref = "c09-slot:"+hashlib.sha256(_json(
            [self.environment_key, self.plan_sha, role, process_index])).hexdigest()
        self.last_budget = self.last_applied = None

    def _observe(self, process_reference):
        budget = self._budget_source()
        applied = self._applied_source(plan=self.plan, role=self.role,
                                       process_index=self.index, process_reference=process_reference)
        now = c09_pg_now(self.using)
        validate_c09_applied_observation(self.plan, budget, applied,
            role=self.role, process_index=self.index, process_reference=process_reference, now=now)
        if now < self.policy.effective_from:
            raise C09Refused("C09_TIME_INVALID")
        self.last_budget, self.last_applied = budget, applied
        return budget, applied

    def _load(self, row):
        if row is None:
            raise C09Refused()
        if (row.instance_ref, row.owner_reference, row.role, row.plan_reference,
                row.plan_version, row.plan_sha256) != (
                self.instance_ref, self.environment_key, self.role, self.plan.plan_reference,
                self.plan.plan_version, self.plan_sha):
            raise C09Refused("C09_POLICY_DIVERGENT")
        for value in (row.budget_reference, row.budget_version):
            c09_text(value)
        _integer(row.generation)
        _integer(row.revision)
        _integer(row.inflight_count, 0)
        if (row.inflight_count > self.policy.max_concurrency or type(row.admission_closed) is not bool
                or type(row.stop_state) is not str
                or row.stop_state not in ("STARTING","RUNNING","DRAINING","STOPPED","UNKNOWN")):
            raise C09Refused()
        if (row.lease_owner is None) != (row.lease_expires_at is None):
            raise C09Refused()
        if row.lease_owner is not None:
            c09_text(row.lease_owner)
            c09_utc(row.lease_expires_at)
        if row.stop_state in ("STARTING","DRAINING","STOPPED","UNKNOWN") and not row.admission_closed:
            raise C09Refused()
        if row.stop_state=="RUNNING" and (row.lease_owner is None or row.admission_closed):
            raise C09Refused()
        if row.stop_state=="STOPPED" and (row.inflight_count or row.lease_owner is not None):
            raise C09Refused()
        return row

    def _handle(self, row):
        return C09RuntimeHandle(row.instance_ref,row.lease_owner,row.generation,row.revision)

    def _view(self, row):
        self._load(row)
        return C09RuntimeView(row.instance_ref,row.role,row.stop_state,row.admission_closed,
                               row.inflight_count,row.generation,row.revision)

    def _save(self, row):
        if row.revision>=_I64:
            raise C09Refused("C09_CAPACITY_INVALID")
        row.revision+=1
        self._load(row)
        row.save(using=self.using)

    def _checked(self, handle, *, active=True):
        if type(handle) is not C09RuntimeHandle:
            raise C09Refused()
        c09_text(handle.instance_ref)
        c09_text(handle.process_reference)
        _integer(handle.generation)
        _integer(handle.revision)
        if handle.instance_ref!=self.instance_ref:
            raise C09Refused("C09_LEASE_STALE")
        row=self._load(_model().objects.using(self.using).select_for_update().filter(pk=self.instance_ref).first())
        if (row.lease_owner,row.generation,row.revision)!=(handle.process_reference,handle.generation,handle.revision):
            raise C09Refused("C09_LEASE_STALE")
        if active and c09_pg_now(self.using)>=row.lease_expires_at:
            raise C09Refused("C09_LEASE_STALE")
        return row

    def claim(self, *, process_reference):
        c09_text(process_reference)
        with transaction.atomic(using=self.using):
            budget,_=self._observe(process_reference)
            _lock(self.using,"C09_RUNTIME_ENV_V1",self.plan.environment_reference)
            incompatible=_model().objects.using(self.using).filter(
                owner_reference=self.environment_key).exclude(plan_sha256=self.plan_sha).exclude(
                    stop_state="STOPPED",inflight_count=0,lease_owner__isnull=True)
            if incompatible.exists():
                raise C09Refused("C09_POLICY_DIVERGENT")
            row=_model().objects.using(self.using).select_for_update().filter(pk=self.instance_ref).first()
            if row is None:
                row=_model().objects.using(self.using).create(
                    instance_ref=self.instance_ref,owner_reference=self.environment_key,role=self.role,
                    plan_reference=self.plan.plan_reference,plan_version=self.plan.plan_version,
                    plan_sha256=self.plan_sha,budget_reference=budget.source_reference,
                    budget_version=budget.source_version,lease_owner=None,lease_expires_at=None,
                    generation=1,revision=1,admission_closed=True,inflight_count=0,stop_state="STARTING")
            self._load(row)
            if (row.budget_reference,row.budget_version)!=(budget.source_reference,budget.source_version):
                raise C09Refused("C09_POLICY_DIVERGENT")
            now=c09_pg_now(self.using)
            if row.stop_state=="UNKNOWN":
                raise C09Refused("C09_POLICY_UNRESOLVED")
            if row.inflight_count:
                if row.lease_expires_at is not None and now>=row.lease_expires_at:
                    row.admission_closed,row.stop_state=True,"UNKNOWN"
                    self._save(row)
                    return None
                raise C09Refused("C09_POLICY_UNRESOLVED")
            if row.stop_state=="DRAINING":
                return None
            if row.lease_owner is not None and now<row.lease_expires_at:
                return self._handle(row) if row.lease_owner==process_reference else None
            if row.generation>=_I64:
                raise C09Refused("C09_CAPACITY_INVALID")
            row.generation+=1
            row.lease_owner=process_reference
            row.lease_expires_at=_plus(now,self.policy.lease_seconds)
            row.admission_closed,row.stop_state=False,"RUNNING"
            self._save(row)
            self._checked(self._handle(row))
            return self._handle(row)

    def renew(self, *, handle):
        with transaction.atomic(using=self.using):
            row=self._checked(handle)
            budget,_=self._observe(handle.process_reference)
            if (row.budget_reference,row.budget_version)!=(budget.source_reference,budget.source_version):
                raise C09Refused("C09_POLICY_DIVERGENT")
            row.lease_expires_at=_plus(c09_pg_now(self.using),self.policy.lease_seconds)
            self._save(row)
            return self._handle(row)

    def begin_unit(self, *, handle):
        with transaction.atomic(using=self.using):
            row=self._checked(handle)
            if row.admission_closed or row.stop_state!="RUNNING":
                raise C09Refused()
            budget,_=self._observe(handle.process_reference)
            if (row.budget_reference,row.budget_version)!=(budget.source_reference,budget.source_version):
                raise C09Refused("C09_POLICY_DIVERGENT")
            self._checked(handle)
            if row.inflight_count>=self.policy.max_concurrency:
                raise C09Refused("C09_CAPACITY_INVALID")
            row.inflight_count+=1
            self._save(row)
            self._checked(self._handle(row))
            return self._handle(row)

    def end_unit(self, *, handle):
        """Fin technique connue ; ne transforme jamais un résultat métier inconnu."""
        with transaction.atomic(using=self.using):
            row=self._checked(handle,active=False)
            if row.inflight_count<1:
                raise C09Refused()
            row.inflight_count-=1
            self._save(row)
            return self._handle(row)

    def close_admissions(self, *, handle):
        with transaction.atomic(using=self.using):
            row=self._checked(handle,active=False)
            row.admission_closed=True
            if row.stop_state!="UNKNOWN":
                row.stop_state="DRAINING"
            self._save(row)
            return self._handle(row)

    def mark_unknown(self, *, handle):
        with transaction.atomic(using=self.using):
            row=self._checked(handle,active=False)
            row.admission_closed,row.stop_state=True,"UNKNOWN"
            self._save(row)
            return self._handle(row)

    def stop(self, *, handle):
        with transaction.atomic(using=self.using):
            row=self._checked(handle,active=False)
            if row.inflight_count or not row.admission_closed or row.stop_state=="UNKNOWN":
                raise C09Refused("C09_POLICY_UNRESOLVED")
            row.lease_owner=row.lease_expires_at=None
            row.stop_state="STOPPED"
            self._save(row)
            return self._view(row)


    def reconcile_quiescence(self, *, recovery_source):
        """Le propriétaire vérifie processus disparu, effets réconciliés et réadmission courante.

        Sans ce port serveur authentifié, UNKNOWN reste fermé. Le DTO seul
        n'est jamais une autorisation et aucun handler n'est réexécuté.
        """
        if type(recovery_source) is not FunctionType:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        with transaction.atomic(using=self.using):
            row=self._load(_model().objects.using(self.using).select_for_update().filter(pk=self.instance_ref).first())
            if row.stop_state!="UNKNOWN" or row.lease_owner is None:
                raise C09Refused()
            observation=recovery_source(
                environment_reference=self.plan.environment_reference,instance_ref=self.instance_ref,
                process_reference=row.lease_owner,generation=row.generation,slot_revision=row.revision)
            if type(observation) is not C09RuntimeRecoveryObservationV1:
                raise C09Refused()
            _fresh(observation,c09_pg_now(self.using))
            for value in (observation.instance_ref,observation.process_reference,observation.readmission_reference):
                c09_text(value)
            _version(observation.readmission_version)
            for value in (observation.generation,observation.slot_revision):
                _integer(value)
            if (observation.environment_reference!=self.plan.environment_reference
                    or observation.instance_ref!=self.instance_ref or observation.process_reference!=row.lease_owner
                    or observation.generation!=row.generation or observation.slot_revision!=row.revision
                    or type(observation.state) is not str or observation.state!="QUIESCENT"
                    or type(observation.active_units) is not int or observation.active_units!=0
                    or type(observation.unknown_units) is not int or observation.unknown_units!=0):
                raise C09Refused("C09_POLICY_UNRESOLVED")
            # Deux transitions prouvées, jamais UNKNOWN directement assimilé à STOPPED.
            row.inflight_count=0
            row.admission_closed,row.stop_state=True,"DRAINING"
            row.lease_owner=row.lease_expires_at=None
            self._save(row)
            row.stop_state="STOPPED"
            self._save(row)
            return self._view(row)


    def inspect(self):
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            return self._view(_model().objects.using(self.using).filter(pk=self.instance_ref).first())


class C09BoundedJobAdmission:
    def __init__(self, *, repository, perimeter_reference, scope, maximum_pending):
        if type(repository) is not C09JobRepository:
            raise C09Refused()
        c09_text(perimeter_reference)
        _scope(scope)
        if type(maximum_pending) is not int or not 1<=maximum_pending<=2**31-1:
            raise C09Refused("C09_CAPACITY_INVALID")
        self.repository,self.using=repository,repository.using
        self.perimeter,self.scope,self.maximum=perimeter_reference,scope,maximum_pending

    def _active(self):
        from pixs.backend.c09_job_records import C09JobExtensionRecord
        context={"scope_type":self.scope.scope_type.value,"tenant_id":self.scope.tenant_id,"scope_id":self.scope.scope_id}
        return C09JobExtensionRecord.objects.using(self.using).filter(
            perimeter_reference=self.perimeter,job__tenant_context=context,
            job__state__in=("PENDING","SCHEDULED","RUNNING","RETRYING","PAUSED"))

    @contextmanager
    def coordination(self):
        with transaction.atomic(using=self.using):
            _lock(self.using,"C09_JOB_QUEUE_V1",[self.perimeter,self.scope.scope_type.value,
                                                self.scope.tenant_id,self.scope.scope_id])
            yield max(0,self.maximum-self._active().count())

    def _deny(self, identity, operation_id):
        repo=self.repository
        try:
            grant=repo.authorization.authorize(identity,using=self.using,operation_id=operation_id)
        except C09AuthorizationRefused as error:
            request,decision=error.request,error.decision
        else:
            waived=grant.decider.audit_waived(grant.request,grant.decision,alias=self.using,operation_id=operation_id)
            if type(waived) is not bool:
                raise C09Refused()
            if waived:
                return
            request,decision=grant.request,grant.decision
        event=AuditEvent(request.decision_id,request.subject_id,request.resource_id,request.action_id,
            request.context,request.correlation_id,Effect.DENY,"DENIED",
            None if decision is None else decision.policy_version,
            None if decision is None else decision.evaluated_at)
        token=uuid.uuid4().hex
        ref=repo.audit.stage(event,alias=self.using,operation_id=operation_id,transaction_token=token,
                            context=request.context,decision=decision)
        if type(ref) is not StagedRef:
            raise C09Refused()
        repo.audit.verify_staged(TransactionProof(operation_id,self.using,token,request.context,(ref,),c09_pg_now(self.using)))

    def admit(self, **arguments):
        identity=arguments.get("identity")
        validate_c09_identity(identity)
        if identity.perimeter_reference!=self.perimeter or identity.context!=self.scope:
            raise C09Refused()
        for name in ("operation_id","handler_reference","handler_version","dedup_key"):
            c09_text(arguments.get(name))
        denied,result=None,None
        with self.coordination() as available:
            from pixs.backend.c09_job_records import C09JobExtensionRecord
            replay=C09JobExtensionRecord.objects.using(self.using).filter(
                actor_reference=identity.actor_reference,perimeter_reference=self.perimeter,
                handler_reference=arguments["handler_reference"],handler_version=arguments["handler_version"],
                dedup_key=arguments["dedup_key"]).exists()
            if available<1 and not replay:
                self._deny(identity,arguments["operation_id"])
                denied=C09Refused("C09_CAPACITY_INVALID")
            else:
                try:
                    result=self.repository.admit(**arguments)
                except C09Refused as error:
                    denied=error
        if denied is not None:
            raise denied
        return result
