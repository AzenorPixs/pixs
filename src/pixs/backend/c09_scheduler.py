"""Scheduler ponctuel C09, sous bail persistant et autorisation courante.

Chaque déclenchement possède sa transaction. Un lot interrompu ne retire pas
les unités déjà engagées ; leurs marqueurs restent consultables. Ce module
ne lance aucun handler, aucun Core durable ou processus externe.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import uuid
from dataclasses import dataclass, fields

from django.db import DatabaseError, IntegrityError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.c09_authorization_adapter import (
    C09AuthorizationAdapter, C09AuthorizationRefused, C09Identity, C09Refused,
    c09_pg_now, c09_text, c09_utc, validate_c09_identity,
)
from pixs.backend.c09_contracts import C09PolicyV1, validate_c09_policy
from pixs.backend.c09_job_repository import C09JobRepository
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent
from pixs.core.ports import StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure

__all__ = ["C09SchedulerHandle", "C09ScheduleView", "C09ScheduleReconciliation", "C09Scheduler"]
_I64 = 2**63 - 1
_STATES = frozenset(("PENDING", "TRIGGERED", "FAILED", "PAUSED", "CANCELLED"))
_FAILURES = frozenset(("CONTEXT_REFUSED", "DEADLINE_EXPIRED", "POLICY_DIVERGENT",
                       "INPUT_INVALID", "TARGET_REFUSED", "RESTORE_UNPROVED"))


@dataclass(frozen=True, slots=True, repr=False)
class C09SchedulerHandle:
    coordinator_ref: str
    owner: str
    generation: int
    revision: int


@dataclass(frozen=True, slots=True, repr=False)
class C09ScheduleView:
    schedule_ref: str
    state: str
    revision: int
    due_at: dt.datetime
    expires_at: dt.datetime
    job_id: str
    confirmed_job_id: str | None
    failure_code: str | None


@dataclass(frozen=True, slots=True, repr=False)
class C09ScheduleReconciliation:
    outcome: str
    view: C09ScheduleView | None


class _WindowExpired(ValueError):
    pass


def _models():
    from pixs.backend.c09_event_records import C09SchedulerLeaseRecord, C09ScheduleRecord
    return C09SchedulerLeaseRecord, C09ScheduleRecord


def _integer(value):
    if type(value) is not int or not 1 <= value <= _I64:
        raise C09Refused()
    return value


def _scope(value):
    if type(value) is not ScopeContext:
        raise C09Refused()
    validate_structure(value)
    for part in (value.tenant_id, value.scope_id):
        if part is not None:
            c09_text(part)
    return value


def _context_doc(value):
    _scope(value)
    return {"scope_type": value.scope_type.value, "tenant_id": value.tenant_id, "scope_id": value.scope_id}


def _version(value):
    from pixs.kernel.manifest.semver import parse_version
    c09_text(value)
    try:
        parse_version(value)
    except ValueError:
        raise C09Refused() from None
    return value


def _policy(value):
    if validate_c09_policy(value):
        raise C09Refused()
    c09_text(value.policy_reference)
    _version(value.policy_version)
    return value


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def _hash(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _policy_hash(value):
    _policy(value)
    document = {field.name: getattr(value, field.name) for field in fields(C09PolicyV1)}
    document["effective_from"] = value.effective_from.isoformat()
    return _hash(document)


def _digest(value):
    c09_text(value)
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise C09Refused()
    return value


def _mapping(value, names):
    if type(value) is not dict:
        raise C09Refused()
    for key in value:
        c09_text(key)
    if set(value) != set(names):
        raise C09Refused()
    return value


def _identity_doc(identity):
    validate_c09_identity(identity)
    return {
        "actor_reference": identity.actor_reference, "perimeter_reference": identity.perimeter_reference,
        "request_reference": identity.request_reference, "request_version": identity.request_version,
        "resource_id": identity.resource_id, "action_id": identity.action_id,
        "correlation_id": identity.correlation_id, "context": _context_doc(identity.context),
    }


def _decode(document):
    document = _mapping(document, ("identity", "request_content_sha256"))
    data = _mapping(document["identity"], (
        "actor_reference", "perimeter_reference", "request_reference", "request_version",
        "resource_id", "action_id", "correlation_id", "context",
    ))
    context = _mapping(data["context"], ("scope_type", "tenant_id", "scope_id"))
    kind = c09_text(context["scope_type"])
    for part in (context["tenant_id"], context["scope_id"]):
        if part is not None:
            c09_text(part)
    kinds = {item.value: item for item in ScopeType}
    if kind not in kinds:
        raise C09Refused()
    scope = ScopeContext(kinds[kind], context["tenant_id"], context["scope_id"])
    identity = C09Identity(
        data["actor_reference"], data["perimeter_reference"], data["request_reference"],
        data["request_version"], data["resource_id"], data["action_id"], scope, data["correlation_id"],
    )
    validate_c09_identity(identity)
    return identity, _digest(document["request_content_sha256"])


def _plus(now, seconds):
    try:
        return now + dt.timedelta(seconds=seconds)
    except OverflowError:
        raise C09Refused() from None


class C09Scheduler:
    def __init__(self, *, using, peer_using, perimeter_reference, scope, coordination_policy,
                 authorization, audit, registry, handlers, policies, max_pending_schedules):
        from pixs.core.audit_sink import PostgresAuditParticipant
        c09_text(using)
        c09_text(peer_using)
        c09_text(perimeter_reference)
        _scope(scope)
        _policy(coordination_policy)
        if type(max_pending_schedules) is not int or not 1 <= max_pending_schedules <= 2**31 - 1:
            raise C09Refused("C09_CAPACITY_INVALID")
        if using == peer_using or type(authorization) is not C09AuthorizationAdapter:
            raise C09Refused()
        if type(audit) is not PostgresAuditParticipant or type(policies) is not tuple:
            raise C09Refused()
        self.jobs = C09JobRepository(
            using=using, peer_using=peer_using, authorization=authorization, audit=audit,
            registry=registry, handlers=handlers, policies=policies,
        )
        self._policies = {}
        for policy in policies:
            _policy(policy)
            key = (policy.policy_reference, policy.policy_version)
            if key in self._policies:
                raise C09Refused()
            self._policies[key] = policy
        self._handlers = {(h.declaration.handler_reference, h.declaration.handler_version) for h in handlers}
        self.using, self.peer_using = using, peer_using
        self._authorization, self._audit_sink = authorization, audit
        self._perimeter, self._scope, self._coordination_policy = perimeter_reference, scope, coordination_policy
        self._max_pending_schedules = max_pending_schedules
        self._coordinator = "c09-coordinator:" + _hash({
            "perimeter_reference": perimeter_reference, "context": _context_doc(scope),
        })

    def _coordination_hash(self, policy=None, limit=None):
        policy = self._coordination_policy if policy is None else policy
        limit = self._max_pending_schedules if limit is None else limit
        _policy(policy)
        if type(limit) is not int or not 1 <= limit <= 2**31 - 1:
            raise C09Refused("C09_CAPACITY_INVALID")
        return _hash({"base_policy_sha256": _policy_hash(policy), "max_pending_schedules": limit})

    def _bound_identity(self, identity):
        validate_c09_identity(identity)
        _scope(identity.context)
        if identity.perimeter_reference != self._perimeter or identity.context != self._scope:
            raise C09Refused()
        return identity

    def _execution_policy(self, policy):
        _policy(policy)
        expected = self._policies.get((policy.policy_reference, policy.policy_version))
        if expected is None or expected != policy:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        return policy

    def _audit(self, request, decision, *, using, operation_id, grant=None, denied=False):
        if grant is not None:
            waived = grant.decider.audit_waived(request, decision, alias=using, operation_id=operation_id)
            if type(waived) is not bool:
                raise C09Refused()
            if waived:
                return
        effect = Effect.DENY if denied or decision is None else decision.effect
        event = AuditEvent(
            request.decision_id, request.subject_id, request.resource_id, request.action_id,
            request.context, request.correlation_id, effect,
            "DENIED" if effect is Effect.DENY else decision.reason_code,
            None if decision is None else decision.policy_version,
            None if decision is None else decision.evaluated_at,
        )
        token = uuid.uuid4().hex
        staged = self._audit_sink.stage(
            event, alias=using, operation_id=operation_id, transaction_token=token,
            context=request.context, decision=decision,
        )
        if type(staged) is not StagedRef:
            raise C09Refused()
        proof = TransactionProof(operation_id, using, token, request.context, (staged,), c09_pg_now(using))
        self._audit_sink.verify_staged(proof)

    def _deny_audit(self, identity, operation_id, error=None):
        try:
            grant = self._authorization.authorize(identity, using=self.using, operation_id=operation_id)
        except C09AuthorizationRefused as current:
            self._audit(current.request, current.decision, using=self.using, operation_id=operation_id, denied=True)
        else:
            self._audit(grant.request, grant.decision, using=self.using,
                        operation_id=operation_id, grant=grant, denied=True)

    def _load_lease(self, row, *, expected_policy=True):
        if row is None:
            raise C09Refused()
        if row.coordinator_ref != self._coordinator or row.perimeter_reference != self._perimeter:
            raise C09Refused()
        if (row.scope_type, row.tenant_id, row.scope_id) != (
            self._scope.scope_type.value, self._scope.tenant_id, self._scope.scope_id
        ):
            raise C09Refused()
        _integer(row.generation)
        _integer(row.revision)
        if type(row.admission_closed) is not bool:
            raise C09Refused()
        if row.owner_reference is None:
            if row.lease_expires_at is not None:
                raise C09Refused()
        else:
            c09_text(row.owner_reference)
            c09_utc(row.lease_expires_at)
        c09_text(row.policy_reference)
        _version(row.policy_version)
        _digest(row.policy_sha256)
        if expected_policy and (
            row.policy_reference != self._coordination_policy.policy_reference
            or row.policy_version != self._coordination_policy.policy_version
            or row.policy_sha256 != self._coordination_hash()
        ):
            raise C09Refused("C09_POLICY_DIVERGENT")
        return row

    def _ensure_lease(self):
        Lease, _ = _models()
        row = Lease.objects.using(self.using).select_for_update().filter(pk=self._coordinator).first()
        if row is None:
            try:
                with transaction.atomic(using=self.using):
                    Lease.objects.using(self.using).create(
                        coordinator_ref=self._coordinator, perimeter_reference=self._perimeter,
                        scope_type=self._scope.scope_type.value, tenant_id=self._scope.tenant_id,
                        scope_id=self._scope.scope_id,
                        policy_reference=self._coordination_policy.policy_reference,
                        policy_version=self._coordination_policy.policy_version,
                        policy_sha256=self._coordination_hash(),
                        owner_reference=None, lease_expires_at=None, generation=1, revision=1,
                        admission_closed=False,
                    )
            except IntegrityError:
                pass  # La ligne gagnante est relue ; aucune erreur n'est assimilée à un succès.
            row = Lease.objects.using(self.using).select_for_update().filter(pk=self._coordinator).first()
        return self._load_lease(row)

    def _handle(self, row):
        return C09SchedulerHandle(row.coordinator_ref, row.owner_reference, row.generation, row.revision)

    def _check_handle(self, handle):
        if type(handle) is not C09SchedulerHandle:
            raise C09Refused()
        c09_text(handle.coordinator_ref)
        c09_text(handle.owner)
        _integer(handle.generation)
        _integer(handle.revision)
        if handle.coordinator_ref != self._coordinator:
            raise C09Refused("C09_LEASE_STALE")

    def _locked_lease(self, handle, *, active=True, admission=True):
        self._check_handle(handle)
        Lease, _ = _models()
        row = self._load_lease(Lease.objects.using(self.using).select_for_update().filter(pk=self._coordinator).first())
        self._check_lease(row, handle, active=active, admission=admission)
        return row

    def _check_lease(self, row, handle, *, active=True, admission=True):
        if (row.owner_reference != handle.owner or row.generation != handle.generation
                or row.revision != handle.revision):
            raise C09Refused("C09_LEASE_STALE")
        if admission and row.admission_closed:
            raise C09Refused("C09_LEASE_STALE")
        now = c09_pg_now(self.using)
        if active and (row.lease_expires_at is None or now >= row.lease_expires_at):
            raise C09Refused("C09_LEASE_STALE")
        if now < self._coordination_policy.effective_from:
            raise C09Refused()
        return now

    def _save_lease(self, row):
        if row.revision >= _I64:
            raise C09Refused("C09_CAPACITY_INVALID")
        row.revision += 1
        self._load_lease(row)
        row.save(using=self.using)

    def acquire_lease(self, *, owner):
        c09_text(owner)
        with transaction.atomic(using=self.using):
            now = c09_pg_now(self.using)
            row = self._ensure_lease()
            now = c09_pg_now(self.using)
            if row.admission_closed:
                return None
            if now < self._coordination_policy.effective_from:
                raise C09Refused()
            if row.owner_reference is not None and now < row.lease_expires_at:
                return self._handle(row) if row.owner_reference == owner else None
            if row.generation >= _I64:
                raise C09Refused("C09_CAPACITY_INVALID")
            row.generation += 1
            row.owner_reference = owner
            row.lease_expires_at = _plus(now, self._coordination_policy.lease_seconds)
            self._save_lease(row)
            return self._handle(row)

    def renew(self, *, handle):
        self._check_handle(handle)
        with transaction.atomic(using=self.using):
            row = self._locked_lease(handle)
            now = c09_pg_now(self.using)
            row.lease_expires_at = _plus(now, self._coordination_policy.lease_seconds)
            self._save_lease(row)
            return self._handle(row)

    def close_admission(self, *, handle):
        with transaction.atomic(using=self.using):
            row = self._locked_lease(handle, active=False, admission=False)
            row.admission_closed = True
            self._save_lease(row)
            return self._handle(row)

    def restitute(self, *, handle):
        with transaction.atomic(using=self.using):
            row = self._locked_lease(handle, active=False, admission=False)
            row.owner_reference, row.lease_expires_at = None, None
            self._save_lease(row)

    def reopen(self):
        with transaction.atomic(using=self.using):
            row = self._ensure_lease()
            if row.owner_reference is not None:
                raise C09Refused("C09_LEASE_STALE")
            row.admission_closed = False
            self._save_lease(row)

    def reconfigure(self, *, coordination_policy, max_pending_schedules):
        _policy(coordination_policy)
        new_hash = self._coordination_hash(coordination_policy, max_pending_schedules)
        with transaction.atomic(using=self.using):
            row = self._ensure_lease()
            if row.owner_reference is not None or not row.admission_closed:
                raise C09Refused("C09_LEASE_STALE")
            same = (row.policy_reference, row.policy_version) == (
                coordination_policy.policy_reference, coordination_policy.policy_version
            )
            if same:
                if row.policy_sha256 != new_hash:
                    raise C09Refused("C09_POLICY_DIVERGENT")
                return
            row.policy_reference = coordination_policy.policy_reference
            row.policy_version = coordination_policy.policy_version
            row.policy_sha256 = new_hash
            if row.revision >= _I64:
                raise C09Refused("C09_CAPACITY_INVALID")
            row.revision += 1
            row.save(using=self.using)
        self._coordination_policy = coordination_policy
        self._max_pending_schedules = max_pending_schedules

    def _fingerprint(self, row):
        return _hash({
            "identity_document": row.identity_document, "policy_sha256": row.policy_sha256,
            "handler_reference": row.handler_reference, "handler_version": row.handler_version,
            "dedup_key": row.dedup_key, "due_at": row.due_at.isoformat(), "expires_at": row.expires_at.isoformat(),
        })

    def _load_schedule(self, row):
        if row is None:
            raise C09Refused()
        for name in ("schedule_ref", "actor_reference", "perimeter_reference", "handler_reference",
                     "dedup_key", "job_id", "command_id", "operation_id"):
            c09_text(getattr(row, name))
        for name in ("handler_version", "policy_version"):
            _version(getattr(row, name))
        _integer(row.revision)
        identity, source_sha = _decode(row.identity_document)
        self._bound_identity(identity)
        if (row.coordinator_id != self._coordinator or row.actor_reference != identity.actor_reference
                or row.perimeter_reference != identity.perimeter_reference):
            raise C09Refused()
        c09_text(row.policy_reference)
        policy = self._policies.get((row.policy_reference, row.policy_version))
        if policy is None or row.policy_sha256 != _policy_hash(policy):
            raise C09Refused("C09_POLICY_DIVERGENT")
        if (row.handler_reference, row.handler_version) not in self._handlers:
            raise C09Refused()
        c09_utc(row.due_at)
        c09_utc(row.expires_at)
        if row.due_at > row.expires_at or len({row.job_id, row.command_id, row.operation_id}) != 3:
            raise C09Refused()
        if type(row.state) is not str or row.state not in _STATES:
            raise C09Refused()
        if row.failure_code is not None:
            c09_text(row.failure_code)
            if row.failure_code not in _FAILURES:
                raise C09Refused()
        if ((row.state == "TRIGGERED" and row.confirmed_job_id != row.job_id)
                or (row.state != "TRIGGERED" and row.confirmed_job_id is not None)):
            raise C09Refused()
        if _digest(row.content_sha256) != self._fingerprint(row):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        return identity, policy, source_sha

    def _view(self, row):
        self._load_schedule(row)
        return C09ScheduleView(row.schedule_ref, row.state, row.revision, row.due_at,
                               row.expires_at, row.job_id, row.confirmed_job_id, row.failure_code)

    def _save_schedule(self, row):
        if row.revision >= _I64:
            raise C09Refused("C09_CAPACITY_INVALID")
        row.revision += 1
        self._load_schedule(row)
        row.save(using=self.using)

    def _failed(self, row, reason):
        row.state, row.failure_code = "FAILED", reason
        self._save_schedule(row)

    def plan_once(self, *, identity, schedule_ref, due_at, expires_at, execution_policy,
                  handler_reference, handler_version, dedup_key):
        self._bound_identity(identity)
        self._execution_policy(execution_policy)
        for value in (schedule_ref, handler_reference, dedup_key):
            c09_text(value)
        _version(handler_version)
        if (handler_reference, handler_version) not in self._handlers:
            raise C09Refused()
        c09_utc(due_at)
        c09_utc(expires_at)
        if due_at > expires_at:
            raise C09Refused()
        _, Schedule = _models()
        denied = None
        result = None
        operation_id = "operation:" + uuid.uuid4().hex
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            try:
                with transaction.atomic(using=self.using):
                    grant = self._authorization.authorize(identity, using=self.using, operation_id=operation_id)
                    coordinator = self._ensure_lease()
                    candidate = Schedule(
                        schedule_ref=schedule_ref, coordinator_id=self._coordinator,
                        identity_document={"identity": _identity_doc(identity), "request_content_sha256": grant.content_sha256},
                        policy_sha256=_policy_hash(execution_policy),
                        actor_reference=identity.actor_reference, perimeter_reference=identity.perimeter_reference,
                        handler_reference=handler_reference, handler_version=handler_version, dedup_key=dedup_key,
                        policy_reference=execution_policy.policy_reference, policy_version=execution_policy.policy_version,
                        job_id="job:" + uuid.uuid4().hex, command_id="command:" + uuid.uuid4().hex,
                        operation_id=operation_id, due_at=due_at, expires_at=expires_at,
                        state="PENDING", revision=1, failure_code=None, confirmed_job_id=None,
                    )
                    candidate.content_sha256 = self._fingerprint(candidate)
                    key = dict(perimeter_reference=identity.perimeter_reference, actor_reference=identity.actor_reference,
                               handler_reference=handler_reference, handler_version=handler_version, dedup_key=dedup_key)
                    row = Schedule.objects.using(self.using).select_for_update().filter(**key).first()
                    if row is None:
                        if coordinator.admission_closed:
                            raise C09Refused("C09_CAPACITY_INVALID")
                        pending = Schedule.objects.using(self.using).filter(
                            coordinator_id=self._coordinator, state__in=("PENDING", "PAUSED"),
                        ).count()
                        if pending >= self._max_pending_schedules:
                            raise C09Refused("C09_CAPACITY_INVALID")
                        now = c09_pg_now(self.using)
                        if now > due_at or now >= expires_at or now < execution_policy.effective_from:
                            raise C09Refused("C09_TIME_INVALID")
                        try:
                            with transaction.atomic(using=self.using):
                                candidate.save(using=self.using, force_insert=True)
                            row = candidate
                        except IntegrityError:
                            row = Schedule.objects.using(self.using).select_for_update().filter(**key).first()
                            if row is None:
                                raise C09Refused() from None
                    self._load_schedule(row)
                    if row.content_sha256 != candidate.content_sha256:
                        raise C09Refused("C09_CONTENT_DIVERGENT")
                    fresh = self._authorization.authorize(
                        identity, using=self.using, operation_id=operation_id, expected_sha=grant.content_sha256,
                    )
                    self._audit(fresh.request, fresh.decision, using=self.using, operation_id=operation_id, grant=fresh)
                    result = self._view(row)
            except C09Refused as error:
                self._deny_audit(identity, operation_id, error)
                denied = error
        if denied is not None:
            raise denied
        return result

    def _trigger_one(self, handle):
        _, Schedule = _models()
        with transaction.atomic(using=self.using):
            lease = self._locked_lease(handle)
            now = c09_pg_now(self.using)
            row = (Schedule.objects.using(self.using).select_for_update(skip_locked=True)
                   .filter(coordinator_id=self._coordinator, state="PENDING", due_at__lte=now)
                   .order_by("due_at", "schedule_ref").first())
            if row is None:
                return None
            identity, policy, source_sha = self._load_schedule(row)
            try:
                with transaction.atomic(using=self.using):
                    if c09_pg_now(self.using) >= row.expires_at:
                        raise _WindowExpired()
                    grant = self._authorization.authorize(
                        identity, using=self.using, operation_id=row.operation_id, expected_sha=source_sha,
                    )
                    self._audit(grant.request, grant.decision, using=self.using,
                                operation_id=row.operation_id, grant=grant)
                    view = self.jobs.admit(
                        identity=identity, policy=policy, job_id=row.job_id,
                        command_id=row.command_id, operation_id=row.operation_id,
                        handler_reference=row.handler_reference, handler_version=row.handler_version,
                        dedup_key="c09-schedule-job:" + row.schedule_ref,
                    )
                    if view.job_id != row.job_id:
                        raise C09Refused()
                    self._check_lease(lease, handle)
                    if c09_pg_now(self.using) >= row.expires_at:
                        raise _WindowExpired()
                    row.confirmed_job_id, row.state = row.job_id, "TRIGGERED"
                    self._save_schedule(row)
                    self._check_lease(lease, handle)
            except _WindowExpired:
                self._check_lease(lease, handle)
                self._deny_audit(identity, row.operation_id)
                self._failed(row, "DEADLINE_EXPIRED")
            except C09AuthorizationRefused as error:
                self._check_lease(lease, handle)
                self._deny_audit(identity, row.operation_id, error)
                self._failed(row, "CONTEXT_REFUSED")
            except C09Refused as error:
                if error.code == "C09_LEASE_STALE":
                    raise
                self._check_lease(lease, handle)
                self._deny_audit(identity, row.operation_id, error)
                self._failed(row, "TARGET_REFUSED")
            self._check_lease(lease, handle)
            return self._view(row)

    def trigger_due(self, *, handle, max_triggers=None):
        self._check_handle(handle)
        maximum = min(self._coordination_policy.polling_max_batch, self._coordination_policy.max_units_per_poll)
        if max_triggers is not None:
            if type(max_triggers) is not int or not 1 <= max_triggers <= 2**31 - 1:
                raise C09Refused("C09_INPUT_INVALID")
            maximum = min(maximum, max_triggers)
        result = []
        for _ in range(maximum):
            view = self._trigger_one(handle)
            if view is None:
                break
            result.append(view)
        return tuple(result)

    def transition(self, *, schedule_ref, target):
        c09_text(schedule_ref)
        if type(target) is not str or target not in ("PENDING", "PAUSED", "CANCELLED"):
            raise C09Refused()
        _, Schedule = _models()
        denied, result = None, None
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            row = Schedule.objects.using(self.using).select_for_update().filter(pk=schedule_ref).first()
            identity, _, source_sha = self._load_schedule(row)
            try:
                grant = self._authorization.authorize(
                    identity, using=self.using, operation_id=row.operation_id, expected_sha=source_sha,
                )
            except C09AuthorizationRefused as error:
                self._deny_audit(identity, row.operation_id, error)
                if row.state in ("PENDING", "PAUSED"):
                    self._failed(row, "CONTEXT_REFUSED")
                denied = error
            else:
                allowed = {"PENDING": ("PAUSED", "CANCELLED"), "PAUSED": ("PENDING", "CANCELLED")}
                if target not in allowed.get(row.state, ()):
                    self._audit(grant.request, grant.decision, using=self.using,
                                operation_id=row.operation_id, grant=grant, denied=True)
                    denied = C09Refused()
                else:
                    self._audit(grant.request, grant.decision, using=self.using,
                                operation_id=row.operation_id, grant=grant)
                    row.state = target
                    self._save_schedule(row)
                    result = self._view(row)
        if denied is not None:
            raise denied
        return result

    def inspect(self, *, schedule_ref):
        c09_text(schedule_ref)
        denied = None
        result = None
        _, Schedule = _models()
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            row = Schedule.objects.using(self.using).select_for_update().filter(pk=schedule_ref).first()
            identity, _, source_sha = self._load_schedule(row)
            try:
                grant = self._authorization.authorize(
                    identity, using=self.using, operation_id=row.operation_id, expected_sha=source_sha,
                )
            except C09AuthorizationRefused as error:
                self._audit(error.request, error.decision, using=self.using, operation_id=row.operation_id, denied=True)
                denied = error
            else:
                self._audit(grant.request, grant.decision, using=self.using, operation_id=row.operation_id, grant=grant)
                result = self._view(row)
        if denied is not None:
            raise denied
        return result

    def reconcile_unknown(self, *, schedule_ref):
        c09_text(schedule_ref)
        try:
            owner, peer = connections[self.using], connections[self.peer_using]
        except ConnectionDoesNotExist:
            raise C09Refused("C09_DATABASE_INVALID") from None
        if owner.in_atomic_block or peer.in_atomic_block or not owner.get_autocommit() or not peer.get_autocommit():
            raise C09Refused()
        if any(owner.settings_dict.get(k) != peer.settings_dict.get(k)
               for k in ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")):
            raise C09Refused()
        if owner.vendor != "postgresql" or peer.vendor != "postgresql":
            raise C09Refused()
        result = C09ScheduleReconciliation("UNKNOWN", None)
        job_check = None
        denied = None
        try:
            metadata = []
            for connection in (owner, peer):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT current_database(),current_schema(),current_schemas(false)")
                    row = cursor.fetchone()
                if row[2] != [row[1]]:
                    raise C09Refused()
                metadata.append((row[0], row[1]))
            if metadata[0] != metadata[1] or owner.connection is peer.connection:
                raise C09Refused()
            _, Schedule = _models()
            with transaction.atomic(using=self.peer_using):
                c09_pg_now(self.peer_using)
                row = Schedule.objects.using(self.peer_using).filter(pk=schedule_ref).first()
                if row is None:
                    return result
                identity, policy, source_sha = self._load_schedule(row)
                try:
                    grant = self._authorization.authorize(
                        identity, using=self.peer_using, operation_id=row.operation_id, expected_sha=source_sha,
                    )
                except C09AuthorizationRefused as error:
                    self._audit(error.request, error.decision, using=self.peer_using, operation_id=row.operation_id, denied=True)
                    denied = error
                else:
                    self._audit(grant.request, grant.decision, using=self.peer_using, operation_id=row.operation_id, grant=grant)
                    view = self._view(row)
                    if row.state == "TRIGGERED":
                        job_check = (row.job_id, policy, view)
                    elif row.state in ("FAILED", "CANCELLED"):
                        result = C09ScheduleReconciliation("TERMINAL_CONFIRMED", view)
                    else:
                        result = C09ScheduleReconciliation("UNKNOWN", view)
            if denied is not None:
                raise denied
            if job_check is not None:
                job_id, policy, view = job_check
                confirmed = self.jobs.reconcile_unknown(job_id=job_id, policy=policy)
                if confirmed.view is not None and confirmed.view.job_id == job_id:
                    result = C09ScheduleReconciliation("TRIGGER_CONFIRMED", view)
            return result
        except (DatabaseError, InterfaceError):
            return C09ScheduleReconciliation("UNKNOWN", None)
        finally:
            if not peer.in_atomic_block:
                peer.close()
