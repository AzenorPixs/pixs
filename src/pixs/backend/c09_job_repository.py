"""Moteur PostgreSQL C09 : unité propriétaire, bail et reprise durables.

Les handlers de ce profil rejoignent la transaction C09 et ne réalisent
aucun effet externe. Les propriétaires qui imposent leur propre transaction
durable nécessitent leur adaptateur distinct, sans transaction englobante.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import uuid
from dataclasses import dataclass
from types import FunctionType

from django.db import DatabaseError, IntegrityError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.c09_authorization_adapter import (
    C09AuthorizationAdapter, C09AuthorizationRefused, C09Identity, C09Refused,
    c09_pg_now, c09_text, c09_utc, validate_c09_identity,
)
from pixs.backend.c09_contracts import (
    C09PolicyV1, C09RoleDeclarationV1, validate_c09_policy,
    validate_c09_role_declaration,
)
from pixs.backend.c09_registry import C09RegistryV1, validate_c09_registry
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent
from pixs.core.ports import StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure

__all__ = [
    "C09Refused", "C09BusinessRefused", "C09TechnicalRetryable",
    "C09LeaseHandle", "C09JobView", "C09HandlerBinding",
    "C09ExecutionContext", "C09HandlerResult", "C09RunResult",
    "C09Reconciliation", "C09JobRepository",
]
_I32 = 2**31 - 1
_I64 = 2**63 - 1
_TERMINAL = frozenset(("SUCCEEDED", "FAILED", "CANCELLED", "DEAD_LETTER"))
_STATES = _TERMINAL | frozenset(("PENDING", "SCHEDULED", "RUNNING", "RETRYING", "PAUSED"))
_FAILURES = frozenset(("BUSINESS_REFUSED", "RETRYABLE_ERROR", "RETRY_EXHAUSTED",
                      "DEADLINE_EXPIRED", "CONTEXT_REFUSED", "LEASE_EXPIRED", "STOP_REQUESTED"))


class C09BusinessRefused(ValueError):
    def __init__(self):
        super().__init__("C09 : rejet métier.")


class C09TechnicalRetryable(ValueError):
    def __init__(self):
        super().__init__("C09 : erreur technique rejouable déclarée.")


@dataclass(frozen=True, slots=True, repr=False)
class C09LeaseHandle:
    job_id: str
    owner: str
    lease_generation: int
    revision: int


@dataclass(frozen=True, slots=True, repr=False)
class C09JobView:
    job_id: str
    state: str
    lease_generation: int
    revision: int
    attempt_count: int
    checkpoint: str | None
    result: str | None
    failure_code: str | None
    next_run_at: dt.datetime | None
    job_deadline: dt.datetime


@dataclass(frozen=True, slots=True, repr=False)
class C09ExecutionContext:
    job_id: str
    using: str
    operation_id: str
    request: object
    decision: object
    checkpoint: str | None


@dataclass(frozen=True, slots=True, repr=False)
class C09HandlerResult:
    checkpoint_reference: str
    result_reference: str | None
    complete: bool


@dataclass(frozen=True, slots=True, repr=False)
class C09HandlerBinding:
    declaration: C09RoleDeclarationV1
    execute: object
    external_effects: bool


@dataclass(frozen=True, slots=True, repr=False)
class C09RunResult:
    view: C09JobView
    lease: C09LeaseHandle | None


@dataclass(frozen=True, slots=True, repr=False)
class C09Reconciliation:
    outcome: str
    view: C09JobView | None


def _models():
    from pixs.backend.models import JobRecord
    from pixs.backend.c09_job_records import C09JobExtensionRecord
    return JobRecord, C09JobExtensionRecord


def _integer(value, lower=1, upper=_I64):
    if type(value) is not int or not lower <= value <= upper:
        raise C09Refused()
    return value


def _version(value):
    from pixs.kernel.manifest.semver import parse_version
    c09_text(value)
    try:
        parse_version(value)
    except ValueError:
        raise C09Refused() from None
    return value


def _digest(value):
    c09_text(value)
    if re.fullmatch("[0-9a-f]{64}", value) is None:
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


def _context_document(context):
    if type(context) is not ScopeContext:
        raise C09Refused()
    validate_structure(context)
    return {"scope_type": context.scope_type.value,
            "tenant_id": context.tenant_id, "scope_id": context.scope_id}


def _context(value):
    doc = _mapping(value, ("scope_type", "tenant_id", "scope_id"))
    kind = c09_text(doc["scope_type"])
    for key in ("tenant_id", "scope_id"):
        if doc[key] is not None:
            c09_text(doc[key])
    kinds = {item.value: item for item in ScopeType}
    if kind not in kinds:
        raise C09Refused()
    result = ScopeContext(kinds[kind], doc["tenant_id"], doc["scope_id"])
    validate_structure(result)
    return result


def _plus(now, seconds):
    _integer(seconds, upper=_I32)
    try:
        return now + dt.timedelta(seconds=seconds)
    except OverflowError:
        raise C09Refused() from None


def _policy(policy):
    if validate_c09_policy(policy):
        raise C09Refused()
    c09_text(policy.policy_reference)
    _version(policy.policy_version)
    return policy


def _policy_digest(policy):
    from dataclasses import fields
    _policy(policy)
    values = {field.name: getattr(policy, field.name) for field in fields(C09PolicyV1)}
    values["effective_from"] = policy.effective_from.isoformat()
    return hashlib.sha256(json.dumps(values, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def _fingerprint(identity, payload):
    # Document construit exclusivement depuis les références validées.
    body = {"actor": identity.actor_reference, "perimeter": identity.perimeter_reference,
            "context": _context_document(identity.context),
            "correlation_id": identity.correlation_id, "payload": payload}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()


class C09JobRepository:
    def __init__(self, *, using, peer_using, authorization, audit, registry, handlers, policies):
        from pixs.core.audit_sink import PostgresAuditParticipant
        c09_text(using)
        c09_text(peer_using)
        if using == peer_using or type(authorization) is not C09AuthorizationAdapter:
            raise C09Refused()
        if type(audit) is not PostgresAuditParticipant:
            raise C09Refused()
        if validate_c09_registry(registry) or type(handlers) is not tuple:
            raise C09Refused()
        if type(policies) is not tuple or not policies:
            raise C09Refused()
        self._policies = {}
        for policy in policies:
            _policy(policy)
            key = (policy.policy_reference, policy.policy_version)
            if key in self._policies:
                raise C09Refused()
            self._policies[key] = policy
        declared = {(r.handler_reference, r.handler_version): r
                    for r in registry.roles if r.role == "worker"}
        bindings = {}
        for binding in handlers:
            if type(binding) is not C09HandlerBinding:
                raise C09Refused()
            declaration = binding.declaration
            if validate_c09_role_declaration(declaration):
                raise C09Refused()
            key = (c09_text(declaration.handler_reference), _version(declaration.handler_version))
            if (key not in declared or declaration != declared[key]
                    or type(binding.execute) is not FunctionType
                    or type(binding.external_effects) is not bool
                    or binding.external_effects is not False or key in bindings):
                raise C09Refused()
            bindings[key] = binding
        if not bindings:
            raise C09Refused()
        self.using, self.peer_using = using, peer_using
        self.authorization, self.audit = authorization, audit
        self._handlers = bindings

    def _owned_policy(self, policy):
        _policy(policy)
        expected = self._policies.get((policy.policy_reference, policy.policy_version))
        if expected is None or policy != expected:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        return policy

    def _policy_row(self, ext, policy):
        self._owned_policy(policy)
        self._load(ext)
        if (ext.policy_reference != policy.policy_reference
                or ext.policy_version != policy.policy_version
                or ext.job.payload["policy_sha256"] != _policy_digest(policy)):
            raise C09Refused("C09_POLICY_DIVERGENT")

    def _load(self, ext):
        row = ext.job
        for name in ("policy_reference", "actor_reference", "command_id", "operation_id",
                     "perimeter_reference", "handler_reference", "dedup_key", "request_reference"):
            c09_text(getattr(ext, name))
        for name in ("policy_version", "handler_version", "request_version"):
            _version(getattr(ext, name))
        _integer(ext.revision)
        _integer(ext.lease_generation)
        _integer(row.attempt_count, lower=0, upper=_I32)
        c09_text(row.job_id)
        c09_text(row.correlation_id)
        c09_text(row.causation_id)
        if row.causation_id != ext.command_id:
            raise C09Refused()
        if len({row.job_id, ext.command_id, ext.operation_id}) != 3:
            raise C09Refused()
        if type(row.state) is not str or row.state not in _STATES:
            raise C09Refused()
        if (row.job_type != ext.handler_reference or row.job_version != ext.handler_version
                or row.perimeter_reference != ext.perimeter_reference):
            raise C09Refused()
        subject = _mapping(row.subject, ("actor_reference",))
        if c09_text(subject["actor_reference"]) != ext.actor_reference:
            raise C09Refused()
        payload = _mapping(row.payload, ("request_reference", "request_version",
                                         "resource_id", "action_id", "content_sha256", "policy_sha256"))
        for value in payload.values():
            c09_text(value)
        _digest(payload["content_sha256"])
        _digest(payload["policy_sha256"])
        if (payload["request_reference"] != ext.request_reference
                or payload["request_version"] != ext.request_version):
            raise C09Refused()
        context = _context(row.tenant_context)
        identity = C09Identity(ext.actor_reference, ext.perimeter_reference,
                              ext.request_reference, ext.request_version,
                              payload["resource_id"], payload["action_id"], context, row.correlation_id)
        validate_c09_identity(identity)
        if _digest(ext.content_sha256) != _fingerprint(identity, payload):
            raise C09Refused("C09_CONTENT_DIVERGENT")
        c09_utc(ext.job_deadline)
        for name in ("attempt_deadline", "next_run_at"):
            value = getattr(ext, name)
            if value is not None and c09_utc(value) > ext.job_deadline:
                raise C09Refused()
        for name in ("checkpoint_reference", "result_reference", "failure_code"):
            value = getattr(ext, name)
            if value is not None:
                c09_text(value)
        if ext.failure_code is not None and ext.failure_code not in _FAILURES:
            raise C09Refused()
        if row.lease_owner is None:
            if row.lease_expires_at is not None:
                raise C09Refused()
        else:
            c09_text(row.lease_owner)
            row.lease_expires_at = c09_utc(row.lease_expires_at, database=True)
        if row.state == "RUNNING" and (row.lease_owner is None or ext.attempt_deadline is None):
            raise C09Refused()
        if row.state != "RUNNING" and row.lease_owner is not None:
            raise C09Refused()
        if row.state == "SUCCEEDED" and (ext.result_reference is None or ext.checkpoint_reference is None):
            raise C09Refused()
        if row.state in ("RETRYING", "SCHEDULED") and ext.next_run_at is None:
            raise C09Refused()
        return row, identity, payload

    def _view(self, ext):
        row, _, _ = self._load(ext)
        return C09JobView(row.job_id, row.state, ext.lease_generation, ext.revision,
                          row.attempt_count, ext.checkpoint_reference, ext.result_reference,
                          ext.failure_code, ext.next_run_at, ext.job_deadline)

    def _audit(self, request, decision, *, using, operation_id, grant=None):
        if grant is not None:
            waived = grant.decider.audit_waived(request, decision, alias=using,
                                                operation_id=operation_id)
            if type(waived) is not bool:
                raise C09Refused()
            if waived:
                return None
        effect = Effect.DENY if decision is None else decision.effect
        event = AuditEvent(request.decision_id, request.subject_id, request.resource_id,
                           request.action_id, request.context, request.correlation_id,
                           effect, "DENIED" if decision is None else decision.reason_code,
                           None if decision is None else decision.policy_version,
                           None if decision is None else decision.evaluated_at)
        token = uuid.uuid4().hex
        staged = self.audit.stage(event, alias=using, operation_id=operation_id,
                                  transaction_token=token, context=request.context, decision=decision)
        if type(staged) is not StagedRef:
            raise C09Refused()
        proof = TransactionProof(operation_id, using, token, request.context,
                                 (staged,), c09_pg_now(using))
        self.audit.verify_staged(proof)
        return proof

    def _authorize(self, ext, *, using=None, with_proof=False):
        using = self.using if using is None else using
        _, identity, payload = self._load(ext)
        grant = self.authorization.authorize(identity, using=using,
                    operation_id=ext.operation_id, expected_sha=payload["content_sha256"])
        proof = self._audit(grant.request, grant.decision, using=using,
                            operation_id=ext.operation_id, grant=grant)
        return (grant, proof) if with_proof else grant

    def _save(self, ext):
        if ext.revision >= _I64:
            raise C09Refused()
        ext.revision += 1
        self._load(ext)
        ext.job.save(using=self.using)
        ext.save(using=self.using)

    def _clear(self, ext, state, code=None):
        ext.job.state = state
        ext.job.lease_owner = None
        ext.job.lease_expires_at = None
        ext.attempt_deadline = None
        ext.next_run_at = None
        ext.failure_code = code

    def _deny(self, ext, error):
        self._audit(error.request, error.decision, using=self.using,
                    operation_id=ext.operation_id)
        self._clear(ext, "FAILED", "CONTEXT_REFUSED")
        self._save(ext)

    def admit(self, *, identity, policy, job_id, command_id, operation_id,
              handler_reference, handler_version, dedup_key):
        validate_c09_identity(identity)
        self._owned_policy(policy)
        for value in (job_id, command_id, operation_id, handler_reference, dedup_key):
            c09_text(value)
        _version(handler_version)
        if len({job_id, command_id, operation_id}) != 3:
            raise C09Refused()
        if (handler_reference, handler_version) not in self._handlers:
            raise C09Refused()
        _, Extension = _models()
        denied = None
        result = None
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            try:
                grant = self.authorization.authorize(identity, using=self.using,
                                                      operation_id=operation_id)
            except C09AuthorizationRefused as error:
                self._audit(error.request, error.decision, using=self.using,
                            operation_id=operation_id)
                denied = error
            else:
                self._audit(grant.request, grant.decision, using=self.using,
                            operation_id=operation_id, grant=grant)
                payload = {"request_reference": identity.request_reference,
                           "request_version": identity.request_version,
                           "resource_id": identity.resource_id, "action_id": identity.action_id,
                           "content_sha256": grant.content_sha256,
                           "policy_sha256": _policy_digest(policy)}
                digest = _fingerprint(identity, payload)
                key = dict(perimeter_reference=identity.perimeter_reference,
                           actor_reference=identity.actor_reference,
                           handler_reference=handler_reference, handler_version=handler_version,
                           dedup_key=dedup_key)
                existing = Extension.objects.using(self.using).select_related("job").filter(**key).first()
                if existing is None:
                    now = c09_pg_now(self.using)
                    if now < policy.effective_from:
                        raise C09Refused()
                    Job, _ = _models()
                    try:
                        with transaction.atomic(using=self.using):
                            job = Job(job_id=job_id, job_type=handler_reference,
                                      job_version=handler_version, payload=payload,
                                      subject={"actor_reference": identity.actor_reference},
                                      tenant_context=_context_document(identity.context),
                                      correlation_id=grant.request.correlation_id,
                                      causation_id=command_id, perimeter_reference=identity.perimeter_reference,
                                      state="PENDING", attempt_count=0,
                                      lease_owner=None, lease_expires_at=None)
                            job.save(using=self.using, force_insert=True)
                            existing = Extension(job=job, policy_reference=policy.policy_reference,
                                policy_version=policy.policy_version, revision=1, lease_generation=1,
                                actor_reference=identity.actor_reference, command_id=command_id,
                                operation_id=operation_id, perimeter_reference=identity.perimeter_reference,
                                handler_reference=handler_reference, handler_version=handler_version,
                                dedup_key=dedup_key, request_reference=identity.request_reference,
                                request_version=identity.request_version, content_sha256=digest,
                                job_deadline=_plus(now, policy.job_timeout_seconds),
                                attempt_deadline=None, next_run_at=None,
                                checkpoint_reference=None, result_reference=None, failure_code=None)
                            existing.save(using=self.using, force_insert=True)
                    except IntegrityError:
                        existing = Extension.objects.using(self.using).select_related("job").filter(**key).first()
                        if existing is None:
                            raise C09Refused() from None
                self._load(existing)
                if (existing.content_sha256 != digest or existing.policy_reference != policy.policy_reference
                        or existing.policy_version != policy.policy_version):
                    raise C09Refused()
                result = self._view(existing)
        if denied is not None:
            raise denied
        return result

    def _query(self, *, using=None, skip_locked=False):
        _, Extension = _models()
        using = self.using if using is None else using
        return (Extension.objects.using(using).select_related("job")
                .select_for_update(skip_locked=skip_locked, of=("self", "job")))

    def _handle(self, ext):
        return C09LeaseHandle(ext.job_id, ext.job.lease_owner,
                              ext.lease_generation, ext.revision)

    def _expired(self, ext, now):
        if now >= ext.job_deadline:
            return True
        if ext.job.state == "RUNNING":
            return (now >= ext.attempt_deadline
                    or now >= c09_utc(ext.job.lease_expires_at, database=True))
        return False

    def _retry(self, ext, policy, now, code):
        count = _integer(ext.job.attempt_count, lower=1, upper=_I32)
        if now >= ext.job_deadline:
            self._clear(ext, "FAILED", "DEADLINE_EXPIRED")
        elif count >= policy.max_attempts:
            self._clear(ext, "DEAD_LETTER", "RETRY_EXHAUSTED")
        else:
            delay = policy.retry_delays_seconds[count - 1]
            due = _plus(now, delay)
            if due >= ext.job_deadline:
                self._clear(ext, "FAILED", "DEADLINE_EXPIRED")
            else:
                self._clear(ext, "RETRYING", code)
                ext.next_run_at = due
        self._save(ext)

    def acquire_next(self, *, owner, policy):
        from django.db.models import Q
        c09_text(owner)
        self._owned_policy(policy)
        with transaction.atomic(using=self.using):
            now = c09_pg_now(self.using)
            allowed = Q()
            for reference, version in self._handlers:
                allowed |= Q(handler_reference=reference, handler_version=version)
            due = (Q(job__state="PENDING")
                   | Q(job__state__in=("SCHEDULED", "RETRYING"), next_run_at__lte=now)
                   | Q(job__state="RUNNING", job__lease_owner=owner)
                   | Q(job__state="RUNNING", job__lease_expires_at__lte=now)
                   | Q(job__state="RUNNING", attempt_deadline__lte=now))
            ext = (self._query(skip_locked=True).filter(allowed, due,
                       policy_reference=policy.policy_reference,
                       policy_version=policy.policy_version)
                   .order_by("job_id").first())
            if ext is None:
                return None
            row, _, _ = self._load(ext)
            self._policy_row(ext, policy)
            try:
                self._authorize(ext)
            except C09AuthorizationRefused as error:
                self._deny(ext, error)
                return None
            now = c09_pg_now(self.using)
            if now < policy.effective_from:
                raise C09Refused()
            if row.state == "RUNNING":
                if self._expired(ext, now):
                    self._retry(ext, policy, now, "LEASE_EXPIRED")
                    return None
                if row.lease_owner != owner:
                    return None
                return self._handle(ext)
            if now >= ext.job_deadline:
                self._clear(ext, "FAILED", "DEADLINE_EXPIRED")
                self._save(ext)
                return None
            if row.attempt_count >= policy.max_attempts:
                self._clear(ext, "DEAD_LETTER", "RETRY_EXHAUSTED")
                self._save(ext)
                return None
            if ext.lease_generation >= _I64 or row.attempt_count >= _I32:
                raise C09Refused()
            deadline = min(_plus(now, policy.attempt_timeout_seconds), ext.job_deadline)
            expires = min(_plus(now, policy.lease_seconds), deadline)
            row.lease_owner = owner
            row.lease_expires_at = expires
            row.state = "RUNNING"
            row.attempt_count += 1
            ext.lease_generation += 1
            ext.attempt_deadline = deadline
            ext.next_run_at = None
            ext.failure_code = None
            self._save(ext)
            return self._handle(ext)

    def _checked_handle(self, handle):
        if type(handle) is not C09LeaseHandle:
            raise C09Refused()
        c09_text(handle.job_id)
        c09_text(handle.owner)
        _integer(handle.lease_generation)
        _integer(handle.revision)

    def _lease(self, handle, policy):
        self._checked_handle(handle)
        self._owned_policy(policy)
        ext = self._query().filter(pk=handle.job_id).first()
        if ext is None:
            raise C09Refused()
        row, _, _ = self._load(ext)
        self._policy_row(ext, policy)
        now = c09_pg_now(self.using)
        if (row.state != "RUNNING" or row.lease_owner != handle.owner
                or ext.lease_generation != handle.lease_generation
                or ext.revision != handle.revision or self._expired(ext, now)):
            raise C09Refused("C09_LEASE_STALE")
        return ext

    def renew(self, *, handle, policy):
        self._checked_handle(handle)
        self._owned_policy(policy)
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            ext = self._lease(handle, policy)
            self._authorize(ext)
            now = c09_pg_now(self.using)
            if self._expired(ext, now):
                raise C09Refused()
            ext.job.lease_expires_at = min(_plus(now, policy.lease_seconds),
                                           ext.attempt_deadline, ext.job_deadline)
            self._save(ext)
            return self._handle(ext)

    def run_unit(self, *, handle, policy):
        from pixs.core.services_authorization_guard import transaction_identity
        self._checked_handle(handle)
        self._owned_policy(policy)
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            ext = self._lease(handle, policy)
            try:
                grant, audit_proof = self._authorize(ext, with_proof=True)
            except C09AuthorizationRefused as error:
                self._deny(ext, error)
                return C09RunResult(self._view(ext), None)
            if self._expired(ext, c09_pg_now(self.using)):
                self._retry(ext, policy, c09_pg_now(self.using), "LEASE_EXPIRED")
                return C09RunResult(self._view(ext), None)
            binding = self._handlers.get((ext.handler_reference, ext.handler_version))
            if binding is None:
                raise C09Refused()
            context = C09ExecutionContext(ext.job_id, self.using, ext.operation_id,
                                         grant.request, grant.decision,
                                         ext.checkpoint_reference)
            before = transaction_identity(self.using)
            outcome = None
            failure = None
            try:
                with transaction.atomic(using=self.using):
                    if self._expired(ext, c09_pg_now(self.using)):
                        raise C09TechnicalRetryable()
                    outcome = binding.execute(context)
                    _, identity, payload = self._load(ext)
                    final_grant = self.authorization.authorize(
                        identity, using=self.using, operation_id=ext.operation_id,
                        expected_sha=payload["content_sha256"])
                    if final_grant.decision.policy_version != grant.decision.policy_version:
                        raise C09TechnicalRetryable()
                    if audit_proof is not None:
                        self.audit.verify_staged(audit_proof)
                    else:
                        self._audit(final_grant.request, final_grant.decision,
                                    using=self.using, operation_id=ext.operation_id,
                                    grant=final_grant)
                    if transaction_identity(self.using) != before:
                        raise C09Refused()
                    if type(outcome) is not C09HandlerResult or type(outcome.complete) is not bool:
                        raise C09Refused()
                    c09_text(outcome.checkpoint_reference)
                    if outcome.complete:
                        c09_text(outcome.result_reference)
                    elif outcome.result_reference is not None:
                        raise C09Refused()
                    if self._expired(ext, c09_pg_now(self.using)):
                        raise C09TechnicalRetryable()
            except C09AuthorizationRefused as error:
                self._deny(ext, error)
                return C09RunResult(self._view(ext), None)
            except C09BusinessRefused:
                failure = "BUSINESS_REFUSED"
            except C09TechnicalRetryable:
                failure = "RETRYABLE_ERROR"
            # Une erreur inattendue quitte la transaction et conserve sa cause.
            if failure == "BUSINESS_REFUSED":
                self._clear(ext, "FAILED", failure)
                self._save(ext)
            elif failure is not None:
                self._retry(ext, policy, c09_pg_now(self.using), failure)
            else:
                ext.checkpoint_reference = outcome.checkpoint_reference
                if outcome.complete:
                    ext.result_reference = outcome.result_reference
                    self._clear(ext, "SUCCEEDED")
                self._save(ext)
            view = self._view(ext)
            return C09RunResult(view, self._handle(ext) if view.state == "RUNNING" else None)

    def restitute(self, *, handle, policy):
        """Restitution sans nouvelle unité ; une révision consommée est refusée."""
        self._checked_handle(handle)
        self._owned_policy(policy)
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            ext = self._lease(handle, policy)
            self._authorize(ext)
            self._retry(ext, policy, c09_pg_now(self.using), "STOP_REQUESTED")
            return C09RunResult(self._view(ext), None)

    def transition(self, *, job_id, policy, target, due_at=None):
        """Contrôle serveur explicite ; ne constitue aucune API publique libre."""
        c09_text(job_id)
        self._owned_policy(policy)
        if type(target) is not str or target not in ("PAUSED", "CANCELLED", "PENDING", "SCHEDULED"):
            raise C09Refused()
        if due_at is not None:
            c09_utc(due_at)
        permitted = {
            "PENDING": ("PAUSED", "CANCELLED", "SCHEDULED"),
            "SCHEDULED": ("PAUSED", "CANCELLED"),
            "RUNNING": ("PAUSED", "CANCELLED"),
            "RETRYING": ("PAUSED", "CANCELLED"),
            "PAUSED": ("PENDING", "CANCELLED"),
        }
        with transaction.atomic(using=self.using):
            now = c09_pg_now(self.using)
            ext = self._query().filter(pk=job_id).first()
            if ext is None:
                raise C09Refused()
            row, _, _ = self._load(ext)
            self._policy_row(ext, policy)
            try:
                self._authorize(ext)
            except C09AuthorizationRefused as error:
                self._deny(ext, error)
                return self._view(ext)
            if target not in permitted.get(row.state, ()):
                raise C09Refused()
            now = c09_pg_now(self.using)
            if now >= ext.job_deadline:
                self._clear(ext, "FAILED", "DEADLINE_EXPIRED")
            else:
                self._clear(ext, target)
                if target == "SCHEDULED":
                    if due_at is None or not now <= due_at < ext.job_deadline:
                        raise C09Refused()
                    ext.next_run_at = due_at
                elif due_at is not None:
                    raise C09Refused()
            self._save(ext)
            return self._view(ext)

    def inspect(self, *, job_id, policy):
        c09_text(job_id)
        self._owned_policy(policy)
        denied = None
        result = None
        with transaction.atomic(using=self.using):
            c09_pg_now(self.using)
            ext = self._query().filter(pk=job_id).first()
            if ext is None:
                raise C09Refused()
            self._policy_row(ext, policy)
            try:
                self._authorize(ext)
            except C09AuthorizationRefused as error:
                self._audit(error.request, error.decision, using=self.using,
                            operation_id=ext.operation_id)
                denied = error
            else:
                result = self._view(ext)
        if denied is not None:
            raise denied
        return result

    def reconcile_unknown(self, *, job_id, policy):
        c09_text(job_id)
        self._owned_policy(policy)
        try:
            owner = connections[self.using]
            peer = connections[self.peer_using]
        except ConnectionDoesNotExist:
            raise C09Refused() from None
        if (owner.in_atomic_block or peer.in_atomic_block
                or owner.vendor != "postgresql" or peer.vendor != "postgresql"
                or not owner.get_autocommit() or not peer.get_autocommit()):
            raise C09Refused()
        keys = ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")
        if any(owner.settings_dict.get(k) != peer.settings_dict.get(k) for k in keys):
            raise C09Refused()
        denied = None
        confirmed = C09Reconciliation("UNKNOWN", None)
        try:
            metadata = []
            for connection in (owner, peer):
                with connection.cursor() as cursor:
                    cursor.execute("SELECT current_database(), current_schema(), current_schemas(false)")
                    row = cursor.fetchone()
                if (type(row) is not tuple or len(row) != 3
                        or type(row[0]) is not str or type(row[1]) is not str
                        or type(row[2]) is not list or row[2] != [row[1]]):
                    raise C09Refused()
                metadata.append((row[0], row[1]))
            if metadata[0] != metadata[1] or owner.connection is peer.connection:
                raise C09Refused()
            with transaction.atomic(using=self.peer_using):
                c09_pg_now(self.peer_using)
                _, Extension = _models()
                ext = (Extension.objects.using(self.peer_using).select_related("job")
                       .filter(pk=job_id).first())
                if ext is None:
                    return C09Reconciliation("UNKNOWN", None)
                self._load(ext)
                self._policy_row(ext, policy)
                try:
                    self._authorize(ext, using=self.peer_using)
                except C09AuthorizationRefused as error:
                    self._audit(error.request, error.decision, using=self.peer_using,
                                operation_id=ext.operation_id)
                    denied = error
                else:
                    view = self._view(ext)
                    outcome = "TERMINAL_CONFIRMED" if view.state in _TERMINAL else "UNKNOWN"
                    confirmed = C09Reconciliation(outcome, view)
            if denied is not None:
                raise denied
            return confirmed
        except (DatabaseError, InterfaceError):
            return C09Reconciliation("UNKNOWN", None)
        finally:
            if not peer.in_atomic_block:
                peer.close()
