"""Outbox PostgreSQL C09, transaction propriétaire et publication locale bornée.

Les fonctions serveur injectées portent les vérifications de leurs propriétaires.
Un DTO ou une déclaration structurelle ne confère aucun droit. Les réceptions
inbox doivent être engagées avant accusé ; aucune garantie exactly-once.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import json
import uuid
from dataclasses import dataclass
from types import FunctionType

from django.db import DatabaseError, IntegrityError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.c09_authorization_adapter import (
    C09AuthorizationAdapter, C09AuthorizationRefused, C09Identity, C09Refused,
    c09_pg_now, c09_text, c09_utc, validate_c09_identity,
)
from pixs.backend.c09_event_values import (
    C09DeliveryPolicyV1, C09EventEnvelopeV1, c09_delivery_fingerprint,
    c09_envelope_content_sha256, c09_envelope_from_document,
    c09_envelope_wire_bytes, validate_c09_delivery_catalog, validate_c09_delivery_policy,
    validate_c09_event_envelope,
)
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent, PortError
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import CoreServiceError
from pixs.kernel.data_outbound_declaration import validate_data_outbound_declaration

__all__ = ["C09OutboxHandle", "C09PublicationView", "C09DeliveryView", "C09OutboxRepository"]
_I64 = 2**63 - 1
_PREFIX = "outbox:c09-v1:"
_TERMINAL = ("PUBLISHED", "FAILED", "DEAD_LETTER")
_STATES = _TERMINAL + ("PENDING", "RUNNING", "RETRYING", "PAUSED")
_FAILURES = ("CONTEXT_REFUSED", "DEADLINE_EXPIRED", "BUSINESS_REFUSED", "RETRYABLE_ERROR",
             "RETRY_EXHAUSTED", "LEASE_EXPIRED", "STOP_REQUESTED", "POLICY_DIVERGENT", "RESTORE_UNPROVED")


@dataclass(frozen=True, slots=True, repr=False)
class C09OutboxHandle:
    event_id: str
    owner: str
    generation: int
    revision: int


@dataclass(frozen=True, slots=True, repr=False)
class C09PublicationView:
    event_id: str
    state: str
    generation: int
    revision: int
    attempt_count: int
    publication_deadline: dt.datetime
    failure_code: str | None


@dataclass(frozen=True, slots=True, repr=False)
class C09DeliveryView:
    event_id: str
    consumer_reference: str
    consumer_version: str
    event_version: str
    component_reference: str
    entry_reference: str
    governance_reference: str | None
    state: str
    receipt_reference: str | None


def _integer(value, lower=1):
    if type(value) is not int or not lower <= value <= _I64:
        raise C09Refused()
    return value


def _scope(value):
    if type(value) is not ScopeContext:
        raise C09Refused()
    try:
        validate_structure(value)
    except ScopeStructureError:
        raise C09Refused() from None
    for part in (value.tenant_id, value.scope_id):
        if part is not None:
            c09_text(part)
    return value


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _mapping(value, keys):
    if type(value) is not dict or not all(type(k) is str for k in value):
        raise C09Refused()
    if set(value) != set(keys):
        raise C09Refused()
    return value


def _plus(instant, seconds):
    try:
        return instant + dt.timedelta(seconds=seconds)
    except OverflowError:
        raise C09Refused("C09_TIME_INVALID") from None


def _connection(alias):
    c09_text(alias)
    try:
        connection = connections[alias]
    except ConnectionDoesNotExist:
        raise C09Refused() from None
    if connection.vendor != "postgresql":
        raise C09Refused()
    return connection


def _native(alias):
    connection = _connection(alias)
    c09_pg_now(alias)
    if (not connection.in_atomic_block or connection.needs_rollback
            or connection.closed_in_transaction or connection.connection is None):
        raise C09Refused()
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_current_xact_id()::text")
        xid = cursor.fetchone()[0]
    c09_text(xid)
    return transaction_identity(alias), connection.connection, tuple(connection.savepoint_ids), xid


def _same_native(actual, expected):
    return (actual[0] == expected[0] and actual[1] is expected[1]
            and actual[2:] == expected[2:])


def _models():
    from pixs.backend.c09_event_records import (
        C09DeliveryRecord, C09EventEnvelopeRecord, C09InboxReceiptRecord,
        C09OrderCursorRecord, C09OutboxPublicationRecord, C09OutboxStageRecord,
    )
    return (C09DeliveryRecord, C09EventEnvelopeRecord, C09InboxReceiptRecord,
            C09OrderCursorRecord, C09OutboxPublicationRecord, C09OutboxStageRecord)


def _receipt_reference(receipt):
    return "c09-inbox:" + str(_integer(receipt.pk))



def _consume_operation(event_id, consumer_reference):
    c09_text(event_id)
    c09_text(consumer_reference)
    return uuid.uuid5(uuid.NAMESPACE_OID, _json(
        ["C09_INBOX_OPERATION_V1", event_id, consumer_reference]).decode("utf-8")).hex


def _identity_document(identity):
    validate_c09_identity(identity)
    _scope(identity.context)
    return {
        "actor_reference": identity.actor_reference, "perimeter_reference": identity.perimeter_reference,
        "request_reference": identity.request_reference, "request_version": identity.request_version,
        "resource_id": identity.resource_id, "action_id": identity.action_id,
        "correlation_id": identity.correlation_id,
        "context": {"scope_type": identity.context.scope_type.value,
                    "tenant_id": identity.context.tenant_id, "scope_id": identity.context.scope_id},
    }


def _identity_from_document(document):
    doc = _mapping(document, ("actor_reference", "perimeter_reference", "request_reference",
                              "request_version", "resource_id", "action_id", "correlation_id", "context"))
    ctx = _mapping(doc["context"], ("scope_type", "tenant_id", "scope_id"))
    kind = c09_text(ctx["scope_type"])
    if kind not in ("PLATFORM", "TENANT"):
        raise C09Refused()
    for part in (ctx["tenant_id"], ctx["scope_id"]):
        if part is not None:
            c09_text(part)
    context = _scope(ScopeContext(ScopeType(kind), ctx["tenant_id"], ctx["scope_id"]))
    identity = C09Identity(doc["actor_reference"], doc["perimeter_reference"], doc["request_reference"],
                           doc["request_version"], doc["resource_id"], doc["action_id"],
                           context, doc["correlation_id"])
    validate_c09_identity(identity)
    return identity


class C09OutboxRepository:
    def __init__(self, *, using, peer_using, perimeter_reference, scope,
                 authorization, audit, registry, bindings, delivery_policies,
                 governance_verifier):
        from pixs.core.audit_sink import PostgresAuditParticipant
        c09_text(using)
        c09_text(peer_using)
        c09_text(perimeter_reference)
        _scope(scope)
        if using == peer_using or type(authorization) is not C09AuthorizationAdapter:
            raise C09Refused()
        if type(audit) is not PostgresAuditParticipant:
            raise C09Refused()
        if type(delivery_policies) is not tuple or not delivery_policies:
            raise C09Refused()
        if governance_verifier is not None and type(governance_verifier) is not FunctionType:
            raise C09Refused()
        policies = {}
        for policy in delivery_policies:
            if validate_c09_delivery_catalog(registry, bindings, policy):
                raise C09Refused()
            key = (policy.delivery_policy_reference, policy.delivery_policy_version)
            if key in policies:
                raise C09Refused()
            policies[key] = policy
        if any(binding.perimeter_reference != perimeter_reference for binding in bindings):
            raise C09Refused()
        self.using, self.peer_using = using, peer_using
        self._perimeter, self._scope = perimeter_reference, scope
        self._authorization, self._audit_sink = authorization, audit
        self._registry, self._bindings, self._policies = registry, bindings, policies
        self._governance_verifier = governance_verifier
        self._frames = []

    def _outside(self):
        if _connection(self.using).in_atomic_block:
            raise C09Refused("C09_DATABASE_INVALID")

    def _binding(self, entry):
        c09_text(entry)
        found = [binding for binding in self._bindings if binding.entry_reference == entry]
        if len(found) != 1:
            raise C09Refused()
        return found[0]

    def _policy(self, policy):
        if validate_c09_delivery_policy(policy):
            raise C09Refused("C09_POLICY_UNRESOLVED")
        expected = self._policies.get((policy.delivery_policy_reference, policy.delivery_policy_version))
        if expected is None or expected != policy:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        return expected

    def _bound(self, identity):
        validate_c09_identity(identity)
        _scope(identity.context)
        if identity.perimeter_reference != self._perimeter or identity.context != self._scope:
            raise C09Refused()
        return identity

    def _budget_lock(self, alias):
        document = {"namespace": "C09_OUTBOX_BUDGET_V1", "perimeter": self._perimeter,
                    "scope_type": self._scope.scope_type.value,
                    "tenant_id": self._scope.tenant_id, "scope_id": self._scope.scope_id}
        document["database_schema_oids"] = transaction_identity(alias)[2:]
        key = int.from_bytes(hashlib.sha256(_json(document)).digest()[:8], "big", signed=True)
        with connections[alias].cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", (key,))

    def _audit(self, request, decision, *, alias, operation_id, grant=None, denied=False):
        if grant is not None:
            waived = grant.decider.audit_waived(request, decision, alias=alias, operation_id=operation_id)
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
        ref = self._audit_sink.stage(event, alias=alias, operation_id=operation_id,
                                     transaction_token=token, context=request.context, decision=decision)
        if type(ref) is not StagedRef:
            raise C09Refused()
        proof = TransactionProof(operation_id, alias, token, request.context, (ref,), c09_pg_now(alias))
        if self._audit_sink.verify_staged(proof) is not None:
            raise C09Refused()

    def _governance(self, grant, *, operation_id, token, payload_refs, consumers,
                    declarations, governance_ref):
        if type(declarations) is not tuple:
            raise C09Refused()
        for declaration in declarations:
            if validate_data_outbound_declaration(declaration):
                raise C09Refused()
            for part in (declaration.destination_reference, declaration.consumer_reference,
                         declaration.guarantee_reference):
                if part is not None:
                    c09_text(part)
        waived = grant.decider.governance_waived(
            grant.request, grant.decision, alias=self.using, operation_id=operation_id)
        if type(waived) is not bool:
            raise C09Refused()
        if waived:
            return
        if self._governance_verifier is None or governance_ref is None or not declarations:
            raise C09Refused("C09_POLICY_UNRESOLVED")
        for consumer in consumers:
            if not any(d.consumer_reference == consumer.consumer_reference for d in declarations):
                raise C09Refused("C09_POLICY_UNRESOLVED")
        outcome = self._governance_verifier(
            request=grant.request, decision=grant.decision, alias=self.using,
            operation_id=operation_id, transaction_token=token, context=self._scope,
            payload_refs=payload_refs, consumers=consumers,
            outbound_declarations=declarations, governance_ref=governance_ref)
        if outcome is not None:
            raise C09Refused("C09_POLICY_UNRESOLVED")

    def _load(self, event_id, *, alias, lock=False):
        """Lecture interne C09 ; l'appelant propriétaire applique l'autorisation de son opération."""
        c09_text(event_id)
        c09_pg_now(alias)
        Delivery, Envelope, _, Cursor, Publication, Stage = _models()
        query = Publication.objects.using(alias)
        if lock:
            query = query.select_for_update()
        publication = query.filter(pk=event_id).first()
        event = Envelope.objects.using(alias).filter(pk=event_id).first()
        stage = Stage.objects.using(alias).filter(pk=event_id).first()
        if publication is None or event is None or stage is None:
            raise C09Refused()
        key = (c09_text(publication.delivery_policy_reference),
               c09_text(publication.delivery_policy_version))
        policy = self._policies.get(key)
        if policy is None or c09_delivery_fingerprint(policy) != publication.delivery_policy_sha256:
            raise C09Refused("C09_POLICY_DIVERGENT")
        binding = self._binding(event.entry_reference)
        try:
            envelope = c09_envelope_from_document(event.wire_document, binding, policy, self._registry)
        except ValueError:
            raise C09Refused("C09_CONTENT_DIVERGENT") from None
        self._bound(envelope.identity)
        for name in ("event_id", "sequence_index", "kind", "entry_reference", "event_type",
                     "event_version", "producer_reference", "schema_reference", "order_scope_reference",
                     "occurred_at", "request_content_sha256", "content_sha256"):
            if getattr(event, name) != getattr(envelope, name):
                raise C09Refused("C09_CONTENT_DIVERGENT")
        if event.perimeter_reference != self._perimeter:
            raise C09Refused()
        cursor = Cursor.objects.using(alias).filter(pk=event.cursor_id).first()
        if cursor is None or (cursor.perimeter_reference, cursor.scope_type, cursor.tenant_id,
                              cursor.scope_id, cursor.order_scope_reference) != (
                self._perimeter, self._scope.scope_type.value, self._scope.tenant_id,
                self._scope.scope_id, envelope.order_scope_reference):
            raise C09Refused()
        if _integer(cursor.last_sequence, 0) < envelope.sequence_index:
            raise C09Refused()
        _integer(cursor.revision)
        for name in ("operation_id", "transaction_token", "staged_xid"):
            c09_text(getattr(stage, name))
        c09_utc(stage.prepared_at)
        if (stage.context_scope_type, stage.context_tenant_id, stage.context_scope_id) != (
                self._scope.scope_type.value, self._scope.tenant_id, self._scope.scope_id):
            raise C09Refused()
        if stage.owner_unit_ref is not None:
            c09_text(stage.owner_unit_ref)
        if type(publication.state) is not str or publication.state not in _STATES:
            raise C09Refused()
        for name in ("generation", "revision"):
            _integer(getattr(publication, name))
        _integer(publication.attempt_count, 0)
        if publication.attempt_count > policy.base_policy.max_attempts:
            raise C09Refused()
        c09_utc(publication.publication_deadline)
        for name in ("lease_expires_at", "next_attempt_at", "attempt_deadline", "published_at"):
            if getattr(publication, name) is not None:
                c09_utc(getattr(publication, name))
        if publication.failure_code is not None:
            c09_text(publication.failure_code)
            if publication.failure_code not in _FAILURES:
                raise C09Refused()
        if (publication.owner_reference is None) != (publication.lease_expires_at is None):
            raise C09Refused()
        if publication.owner_reference is not None:
            c09_text(publication.owner_reference)
        if (publication.state == "RUNNING") != (publication.owner_reference is not None):
            raise C09Refused()
        if (publication.state == "RUNNING") != (publication.attempt_deadline is not None):
            raise C09Refused()
        if (publication.state == "RETRYING") != (publication.next_attempt_at is not None):
            raise C09Refused()
        if (publication.state == "PUBLISHED") != (publication.published_at is not None):
            raise C09Refused()
        if publication.attempt_deadline is not None and publication.attempt_deadline > publication.publication_deadline:
            raise C09Refused()
        if publication.lease_expires_at is not None and publication.lease_expires_at > publication.attempt_deadline:
            raise C09Refused()
        declarations = tuple(c for c in self._registry.consumers if c.entry_reference == binding.entry_reference)
        deliveries = tuple(Delivery.objects.using(alias).filter(event_id=event_id).order_by("consumer_reference"))
        if len(deliveries) != len(declarations) or not deliveries:
            raise C09Refused()
        for delivery, declaration in zip(deliveries, declarations, strict=True):
            snapshot = dataclasses.asdict(declaration)
            _mapping(delivery.declaration_snapshot, snapshot)
            if not all(type(v) is str for v in delivery.declaration_snapshot.values()):
                raise C09Refused()
            if delivery.declaration_snapshot != snapshot:
                raise C09Refused("C09_CONTENT_DIVERGENT")
            for name in ("consumer_reference", "consumer_version", "entry_reference", "component_reference"):
                if getattr(delivery, name) != getattr(declaration, name):
                    raise C09Refused()
            if delivery.event_version != envelope.event_version:
                raise C09Refused()
            _integer(delivery.revision)
            if type(delivery.state) is not str or delivery.state not in ("PENDING", "CONFIRMED", "REFUSED"):
                raise C09Refused()
            for name in ("receipt_reference", "outcome_reference", "governance_reference"):
                if getattr(delivery, name) is not None:
                    c09_text(getattr(delivery, name))
        return envelope, policy, event, stage, publication, deliveries

    def stage(self, *, identity, entry_reference, delivery_policy, event_id, operation_id,
              transaction_token, payload_refs, causation_id, owner_unit_ref,
              governance_ref, outbound_declarations):
        self._bound(identity)
        binding, policy = self._binding(entry_reference), self._policy(delivery_policy)
        for value in (event_id, operation_id, transaction_token):
            c09_text(value)
        for value in (causation_id, owner_unit_ref, governance_ref):
            if value is not None:
                c09_text(value)
        if type(payload_refs) is not tuple or not payload_refs or len(payload_refs) > policy.max_payload_refs:
            raise C09Refused()
        for value in payload_refs:
            c09_text(value)
        if len(set(payload_refs)) != len(payload_refs):
            raise C09Refused()
        native = _native(self.using)
        started = c09_pg_now(self.using)
        if self._frames and any((f["operation_id"], f["token"]) != (operation_id, transaction_token) for f in self._frames):
            raise C09Refused("C09_REFUSED")
        self._budget_lock(self.using)
        grant = self._authorization.authorize(identity, using=self.using, operation_id=operation_id)
        consumers = tuple(c for c in self._registry.consumers if c.entry_reference == entry_reference)
        self._governance(grant, operation_id=operation_id, token=transaction_token,
                         payload_refs=payload_refs, consumers=consumers,
                         declarations=outbound_declarations, governance_ref=governance_ref)
        Delivery, Envelope, _, Cursor, Publication, Stage = _models()
        existing = Envelope.objects.using(self.using).filter(pk=event_id).exists()
        if existing:
            loaded = self._load(event_id, alias=self.using)
            original, old_policy, _, old_stage, _, deliveries = loaded
            candidate = dataclasses.replace(original, identity=identity, entry_reference=entry_reference,
                                            payload_refs=payload_refs, causation_id=causation_id,
                                            request_content_sha256=grant.content_sha256, content_sha256="")
            candidate = dataclasses.replace(candidate, content_sha256=c09_envelope_content_sha256(candidate))
            if (c09_envelope_wire_bytes(candidate) != c09_envelope_wire_bytes(original)
                    or old_policy != policy or old_stage.operation_id != operation_id
                    or old_stage.owner_unit_ref != owner_unit_ref
                    or any(d.governance_reference != governance_ref for d in deliveries)):
                raise C09Refused("C09_CONTENT_DIVERGENT")
            row = loaded[2]
        else:
            pending = Publication.objects.using(self.using).filter(
                event__perimeter_reference=self._perimeter,
                event__cursor__scope_type=self._scope.scope_type.value,
                event__cursor__tenant_id=self._scope.tenant_id,
                event__cursor__scope_id=self._scope.scope_id).exclude(state__in=_TERMINAL)
            pending_count = pending.count()
            delivery_count = Delivery.objects.using(self.using).filter(
                event_id__in=pending.values("event_id"), state="PENDING").count()
            if pending_count >= policy.max_pending_events or delivery_count + len(consumers) > policy.max_pending_deliveries:
                raise C09Refused("C09_CAPACITY_INVALID")
            key = dict(perimeter_reference=self._perimeter, scope_type=self._scope.scope_type.value,
                       tenant_id=self._scope.tenant_id, scope_id=self._scope.scope_id,
                       order_scope_reference=binding.order_scope_reference)
            cursor = Cursor.objects.using(self.using).select_for_update().filter(**key).first()
            if cursor is None:
                cursor = Cursor.objects.using(self.using).create(**key, last_sequence=0, revision=1)
            if _integer(cursor.last_sequence, 0) >= _I64 or _integer(cursor.revision) >= _I64:
                raise C09Refused("C09_CAPACITY_INVALID")
            now = c09_pg_now(self.using)
            if now < policy.base_policy.effective_from:
                raise C09Refused("C09_TIME_INVALID")
            envelope = C09EventEnvelopeV1(
                event_id, binding.kind, identity, entry_reference, binding.event_type,
                binding.event_version, binding.producer_reference, binding.schema_reference,
                binding.order_scope_reference, causation_id, now, cursor.last_sequence+1,
                payload_refs, grant.content_sha256, "",
            )
            envelope = dataclasses.replace(envelope, content_sha256=c09_envelope_content_sha256(envelope))
            if validate_c09_event_envelope(envelope, binding, policy):
                raise C09Refused()
            wire = c09_envelope_wire_bytes(envelope)
            document = json.loads(wire)
            c09_envelope_from_document(document, binding, policy, self._registry)
            row = Envelope(
                event_id=event_id, cursor_id=cursor.pk, sequence_index=envelope.sequence_index,
                kind=envelope.kind, entry_reference=entry_reference, event_type=envelope.event_type,
                event_version=envelope.event_version, producer_reference=envelope.producer_reference,
                schema_reference=envelope.schema_reference, order_scope_reference=envelope.order_scope_reference,
                perimeter_reference=self._perimeter, occurred_at=now,
                request_content_sha256=grant.content_sha256,
                content_sha256=envelope.content_sha256, wire_document=document,
            )
            row.save(using=self.using, force_insert=True)
            Stage(
                event_id=event_id, operation_id=operation_id, transaction_token=transaction_token,
                staged_xid=native[3], context_scope_type=self._scope.scope_type.value,
                context_tenant_id=self._scope.tenant_id, context_scope_id=self._scope.scope_id,
                owner_unit_ref=owner_unit_ref, prepared_at=now,
            ).save(using=self.using, force_insert=True)
            Publication.objects.using(self.using).create(
                event_id=event_id, delivery_policy_reference=policy.delivery_policy_reference,
                delivery_policy_version=policy.delivery_policy_version,
                delivery_policy_sha256=c09_delivery_fingerprint(policy), state="PENDING",
                revision=1, generation=1, owner_reference=None, lease_expires_at=None,
                attempt_count=0, next_attempt_at=None, attempt_deadline=None,
                publication_deadline=_plus(now, policy.base_policy.job_timeout_seconds),
                published_at=None, failure_code=None,
            )
            for consumer in consumers:
                Delivery.objects.using(self.using).create(
                    event_id=event_id, consumer_reference=consumer.consumer_reference,
                    consumer_version=consumer.consumer_version, event_version=envelope.event_version,
                    component_reference=consumer.component_reference, entry_reference=entry_reference,
                    declaration_snapshot=dataclasses.asdict(consumer), governance_reference=governance_ref,
                    state="PENDING", revision=1, receipt_reference=None, outcome_reference=None,
                )
            cursor.last_sequence += 1
            cursor.revision += 1
            cursor.save(using=self.using)
        fresh = self._authorization.authorize(identity, using=self.using,
                                               operation_id=operation_id, expected_sha=grant.content_sha256)
        self._audit(fresh.request, fresh.decision, alias=self.using, operation_id=operation_id, grant=fresh)
        if not _same_native(_native(self.using), native):
            raise C09Refused()
        ref = StagedRef(operation_id, self.using, transaction_token, identity.context, _PREFIX+event_id)
        self._frames.append({"ref": ref, "event_id": event_id, "native": native,
                             "operation_id": operation_id, "token": transaction_token,
                             "wire": _json(row.wire_document), "fresh": not existing, "started": started})
        return ref

    def _frame(self, proof, *, live):
        if type(proof) is not TransactionProof:
            raise C09Refused()
        try:
            proof.__post_init__()
        except CorePortError:
            raise C09Refused() from None
        own = [ref for ref in proof.staged if ref.staged_kind.startswith(_PREFIX)]
        frames = [frame for frame in self._frames if any(ref is frame["ref"] for ref in own)]
        if not frames or len(frames) != len(own):
            raise C09Refused()
        for frame in frames:
            if (proof.alias, proof.operation_id, proof.transaction_token, proof.context) != (
                    self.using, frame["operation_id"], frame["token"], self._scope):
                raise C09Refused()
            if live:
                if not _same_native(_native(self.using), frame["native"]):
                    raise C09Refused()
                if not frame["started"] <= proof.prepared_at <= c09_pg_now(self.using):
                    raise C09Refused()
        return frames

    def verify_staged(self, proof):
        for frame in self._frame(proof, live=True):
            envelope, _, event, stage, _, _ = self._load(frame["event_id"], alias=self.using)
            if _json(event.wire_document) != frame["wire"] or stage.operation_id != frame["operation_id"]:
                raise C09Refused()
            if frame["fresh"] and (stage.transaction_token != frame["token"] or stage.staged_xid != frame["native"][3]):
                raise C09Refused()
            self._authorization.authorize(envelope.identity, using=self.using,
                                          operation_id=proof.operation_id,
                                          expected_sha=envelope.request_content_sha256)

    def _peer_check(self):
        owner, peer = _connection(self.using), _connection(self.peer_using)
        if owner.in_atomic_block or peer.in_atomic_block:
            raise C09Refused()
        for key in ("ENGINE", "NAME", "HOST", "PORT", "USER", "OPTIONS"):
            if owner.settings_dict.get(key) != peer.settings_dict.get(key):
                raise C09Refused()
        owner.ensure_connection()
        peer.ensure_connection()
        if owner.connection is peer.connection:
            raise C09Refused()
        mappings = []
        for connection in (owner, peer):
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database(), current_schemas(false), pg_backend_pid()")
                mappings.append(cursor.fetchone())
        if (mappings[0][:2] != mappings[1][:2] or mappings[0][2] == mappings[1][2]
                or type(mappings[0][1]) is not list or len(mappings[0][1]) != 1):
            raise C09Refused()

    def reconcile_unknown(self, proof):
        try:
            frames = self._frame(proof, live=False)
            self._peer_check()
            with transaction.atomic(using=self.peer_using):
                for frame in frames:
                    envelope, _, event, stage, _, _ = self._load(frame["event_id"], alias=self.peer_using)
                    if (_json(event.wire_document) != frame["wire"]
                            or stage.operation_id != frame["operation_id"]
                            or (frame["fresh"] and (stage.transaction_token != frame["token"]
                                                   or stage.staged_xid != frame["native"][3]))):
                        return "UNKNOWN"
                    self._authorization.authorize(envelope.identity, using=self.peer_using,
                                                  operation_id=proof.operation_id,
                                                  expected_sha=envelope.request_content_sha256)
            return "CONFIRMED"
        except (C09Refused, CoreServiceError, PortError, DatabaseError, InterfaceError):
            return "UNKNOWN"

    def _view(self, loaded):
        row = loaded[4]
        return C09PublicationView(row.event_id, row.state, row.generation, row.revision,
                                  row.attempt_count, row.publication_deadline, row.failure_code)

    def _operate(self, event_id, action, *, handle=None):
        """La décision refusée est auditée après rollback du seul savepoint d'opération."""
        self._outside()
        denied, result = None, None
        with transaction.atomic(using=self.using):
            loaded = self._load(event_id, alias=self.using, lock=True)
            envelope = loaded[0]
            operation = uuid.uuid4().hex
            try:
                with transaction.atomic(using=self.using):
                    cutoff = None
                    if handle is not None:
                        self._lease(loaded, handle)
                        cutoff = min(loaded[4].lease_expires_at, loaded[4].attempt_deadline, loaded[4].publication_deadline)
                    grant = self._authorization.authorize(
                        envelope.identity, using=self.using, operation_id=operation,
                        expected_sha=envelope.request_content_sha256)
                    result = action(loaded)
                    fresh = self._authorization.authorize(
                        envelope.identity, using=self.using, operation_id=operation,
                        expected_sha=envelope.request_content_sha256)
                    self._audit(fresh.request, fresh.decision, alias=self.using,
                                operation_id=operation, grant=fresh)
                    if cutoff is not None and c09_pg_now(self.using) >= cutoff:
                        raise C09Refused("C09_LEASE_STALE")
                    if type(result) is C09OutboxHandle:
                        self._lease(loaded, result)
            except C09Refused as error:
                try:
                    current = self._authorization.authorize(
                        envelope.identity, using=self.using, operation_id=operation,
                        expected_sha=envelope.request_content_sha256)
                except C09AuthorizationRefused as refusal:
                    self._audit(refusal.request, refusal.decision, alias=self.using,
                                operation_id=operation, denied=True)
                else:
                    self._audit(current.request, current.decision, alias=self.using,
                                operation_id=operation, grant=current, denied=True)
                denied = error
        if denied is not None:
            raise denied
        return result

    def _save(self, row):
        if _integer(row.revision) >= _I64:
            raise C09Refused("C09_CAPACITY_INVALID")
        row.revision += 1
        row.save(using=self.using)

    def _handle(self, row):
        return C09OutboxHandle(row.event_id, row.owner_reference, row.generation, row.revision)

    def _check_handle(self, handle):
        if type(handle) is not C09OutboxHandle:
            raise C09Refused("C09_LEASE_STALE")
        c09_text(handle.event_id)
        c09_text(handle.owner)
        _integer(handle.generation)
        _integer(handle.revision)

    def _lease(self, loaded, handle, *, active=True):
        self._check_handle(handle)
        row = loaded[4]
        if (row.event_id, row.owner_reference, row.generation, row.revision, row.state) != (
                handle.event_id, handle.owner, handle.generation, handle.revision, "RUNNING"):
            raise C09Refused("C09_LEASE_STALE")
        now = c09_pg_now(self.using)
        if active and (now >= row.lease_expires_at or now >= row.attempt_deadline
                       or now >= row.publication_deadline):
            raise C09Refused("C09_LEASE_STALE")
        return now

    def _earlier(self, loaded, alias):
        _, Envelope, _, _, Publication, _ = _models()
        event = loaded[2]
        earlier = Envelope.objects.using(alias).filter(cursor_id=event.cursor_id,
                                                       sequence_index__lt=event.sequence_index)
        return Publication.objects.using(alias).filter(event_id__in=earlier.values("event_id")).exclude(state="PUBLISHED").exists()

    def _clear(self, row, *, state, code):
        row.state, row.failure_code = state, code
        row.owner_reference = row.lease_expires_at = row.attempt_deadline = row.next_attempt_at = None

    def acquire(self, *, event_id, owner):
        c09_text(event_id)
        c09_text(owner)
        def action(loaded):
            policy, row = loaded[1].base_policy, loaded[4]
            now = c09_pg_now(self.using)
            if row.state in _TERMINAL or row.state == "PAUSED" or self._earlier(loaded, self.using):
                return None
            if row.state == "RUNNING" and now < row.lease_expires_at and now < row.attempt_deadline:
                return self._handle(row) if row.owner_reference == owner else None
            if row.state == "RETRYING" and now < row.next_attempt_at:
                return None
            if now < policy.effective_from:
                raise C09Refused("C09_TIME_INVALID")
            if now >= row.publication_deadline:
                self._clear(row, state="FAILED", code="DEADLINE_EXPIRED")
                self._save(row)
                return None
            if row.attempt_count >= policy.max_attempts:
                self._clear(row, state="DEAD_LETTER", code="RETRY_EXHAUSTED")
                self._save(row)
                return None
            if row.generation >= _I64 or row.attempt_count >= _I64:
                raise C09Refused("C09_CAPACITY_INVALID")
            row.state, row.owner_reference = "RUNNING", owner
            row.generation += 1
            row.attempt_count += 1
            row.next_attempt_at = row.failure_code = None
            row.attempt_deadline = min(row.publication_deadline, _plus(now, policy.attempt_timeout_seconds))
            row.lease_expires_at = min(row.attempt_deadline, _plus(now, policy.lease_seconds))
            self._save(row)
            handle = self._handle(row)
            self._lease(loaded, handle)
            return handle
        return self._operate(event_id, action)

    def renew(self, *, handle):
        self._check_handle(handle)
        def action(loaded):
            now = self._lease(loaded, handle)
            row, policy = loaded[4], loaded[1].base_policy
            row.lease_expires_at = min(row.attempt_deadline, _plus(now, policy.lease_seconds))
            self._save(row)
            result = self._handle(row)
            self._lease(loaded, result)
            return result
        return self._operate(handle.event_id, action, handle=handle)

    def pending_deliveries(self, *, handle):
        self._check_handle(handle)
        def action(loaded):
            self._lease(loaded, handle)
            if self._earlier(loaded, self.using):
                raise C09Refused()
            values = tuple(C09DeliveryView(
                d.event_id, d.consumer_reference, d.consumer_version, d.event_version,
                d.component_reference, d.entry_reference, d.governance_reference,
                d.state, d.receipt_reference) for d in loaded[5] if d.state == "PENDING")
            self._lease(loaded, handle)
            return loaded[0], values
        return self._operate(handle.event_id, action, handle=handle)

    def acknowledge(self, *, handle, consumer_reference, receipt_reference):
        self._check_handle(handle)
        c09_text(consumer_reference)
        c09_text(receipt_reference)
        def action(loaded):
            self._lease(loaded, handle)
            envelope, _, _, _, row, deliveries = loaded
            Delivery, _, Inbox, _, _, _ = _models()
            found = [d for d in deliveries if d.consumer_reference == consumer_reference]
            if len(found) != 1:
                raise C09Refused()
            delivery = Delivery.objects.using(self.using).select_for_update().get(pk=found[0].pk)
            receipt = Inbox.objects.using(self.using).filter(delivery_id=delivery.pk).first()
            if (receipt is None or receipt_reference != _receipt_reference(receipt)
                    or receipt.event_id != envelope.event_id or receipt.consumer_reference != consumer_reference
                    or receipt.consumer_version != delivery.consumer_version
                    or receipt.event_version != envelope.event_version
                    or receipt.content_sha256 != envelope.content_sha256
                    or receipt.actor_reference != envelope.identity.actor_reference
                    or receipt.perimeter_reference != self._perimeter
                    or (receipt.scope_type, receipt.tenant_id, receipt.scope_id) != (
                        self._scope.scope_type.value, self._scope.tenant_id, self._scope.scope_id)):
                raise C09Refused("C09_CONTENT_DIVERGENT")
            receipt_identity = _identity_from_document(receipt.identity_document)
            if (receipt_identity.actor_reference != envelope.identity.actor_reference
                    or receipt_identity.perimeter_reference != self._perimeter
                    or receipt_identity.context != self._scope
                    or receipt_identity.request_reference != receipt.request_reference
                    or receipt_identity.request_version != receipt.request_version
                    or receipt_identity.correlation_id != receipt.correlation_id
                    or receipt.operation_id != _consume_operation(envelope.event_id, consumer_reference)):
                raise C09Refused("C09_CONTENT_DIVERGENT")
            for value in (receipt.result_reference, receipt.checkpoint_reference, receipt.transaction_token,
                          receipt.request_content_sha256, receipt.consumed_xid):
                c09_text(value)
            if (len(receipt.request_content_sha256) != 64
                    or any(c not in "0123456789abcdef" for c in receipt.request_content_sha256)
                    or not receipt.consumed_xid.isascii() or not receipt.consumed_xid.isdigit()
                    or c09_utc(receipt.consumed_at) > c09_pg_now(self.using)):
                raise C09Refused("C09_CONTENT_DIVERGENT")
            if delivery.state == "CONFIRMED":
                if delivery.receipt_reference != receipt_reference:
                    raise C09Refused()
            elif delivery.state == "PENDING":
                if _integer(delivery.revision) >= _I64:
                    raise C09Refused()
                delivery.state, delivery.receipt_reference = "CONFIRMED", receipt_reference
                delivery.outcome_reference = receipt.result_reference
                delivery.revision += 1
                delivery.save(using=self.using)
            else:
                raise C09Refused()
            self._lease(loaded, handle)
            remaining = Delivery.objects.using(self.using).filter(event_id=row.event_id).exclude(state="CONFIRMED").exists()
            if not remaining:
                if self._earlier(loaded, self.using):
                    raise C09Refused()
                self._clear(row, state="PUBLISHED", code=None)
                row.published_at = c09_pg_now(self.using)
                self._save(row)
                return self._view(loaded)
            self._save(row)
            return self._handle(row)
        return self._operate(handle.event_id, action, handle=handle)

    def fail(self, *, handle, kind):
        self._check_handle(handle)
        if type(kind) is not str or kind not in ("RETRYABLE_ERROR", "BUSINESS_REFUSED", "RESTORE_UNPROVED"):
            raise C09Refused()
        def action(loaded):
            now = self._lease(loaded, handle)
            row, policy = loaded[4], loaded[1].base_policy
            if kind != "RETRYABLE_ERROR":
                self._clear(row, state="FAILED", code=kind)
            elif row.attempt_count >= policy.max_attempts:
                self._clear(row, state="DEAD_LETTER", code="RETRY_EXHAUSTED")
            else:
                due = _plus(now, policy.retry_delays_seconds[row.attempt_count-1])
                if due >= row.publication_deadline:
                    self._clear(row, state="FAILED", code="DEADLINE_EXPIRED")
                else:
                    self._clear(row, state="RETRYING", code=kind)
                    row.next_attempt_at = due
            self._save(row)
            return self._view(loaded)
        return self._operate(handle.event_id, action, handle=handle)

    def restitute(self, *, handle):
        """Arrêt local connu : attente bornée et historique des tentatives conservé."""
        self._check_handle(handle)
        def action(loaded):
            now = self._lease(loaded, handle)
            row, policy = loaded[4], loaded[1].base_policy
            if row.attempt_count >= policy.max_attempts:
                self._clear(row, state="DEAD_LETTER", code="RETRY_EXHAUSTED")
            else:
                due = _plus(now, policy.retry_delays_seconds[row.attempt_count-1])
                if due >= row.publication_deadline:
                    self._clear(row, state="FAILED", code="DEADLINE_EXPIRED")
                else:
                    self._clear(row, state="RETRYING", code="STOP_REQUESTED")
                    row.next_attempt_at = due
            self._save(row)
            return self._view(loaded)
        return self._operate(handle.event_id, action, handle=handle)

    def pause(self, *, handle):
        self._check_handle(handle)
        def action(loaded):
            self._lease(loaded, handle)
            self._clear(loaded[4], state="PAUSED", code="STOP_REQUESTED")
            self._save(loaded[4])
            return self._view(loaded)
        return self._operate(handle.event_id, action, handle=handle)

    def resume(self, *, event_id):
        c09_text(event_id)
        def action(loaded):
            row = loaded[4]
            if row.state != "PAUSED":
                raise C09Refused()
            if row.attempt_count >= loaded[1].base_policy.max_attempts or c09_pg_now(self.using) >= row.publication_deadline:
                raise C09Refused("C09_CAPACITY_INVALID")
            self._clear(row, state="PENDING", code=None)
            self._save(row)
            return self._view(loaded)
        return self._operate(event_id, action)

    def inspect(self, *, event_id):
        c09_text(event_id)
        return self._operate(event_id, self._view)

    def reconcile_publication(self, *, event_id):
        c09_text(event_id)
        try:
            self._peer_check()
            with transaction.atomic(using=self.peer_using):
                loaded = self._load(event_id, alias=self.peer_using)
                operation = uuid.uuid4().hex
                grant = self._authorization.authorize(
                    loaded[0].identity, using=self.peer_using, operation_id=operation,
                    expected_sha=loaded[0].request_content_sha256)
                self._audit(grant.request, grant.decision, alias=self.peer_using,
                            operation_id=operation, grant=grant)
                if loaded[4].state in _TERMINAL:
                    return "TERMINAL_CONFIRMED", self._view(loaded)
                return "UNKNOWN", self._view(loaded)
        except (C09Refused, CoreServiceError, PortError, DatabaseError, InterfaceError):
            return "UNKNOWN", None
