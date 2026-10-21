"""Persistance C05 propriétaire : staging transactionnel et constat indépendant."""
from __future__ import annotations

import datetime
import hashlib
from dataclasses import dataclass

from pixs.core.audit_contracts import (
    AuditError, AuditPolicy, apply_redactions_generic, apply_redactions_pdp,
    canonical_generic_bytes, canonical_pdp_bytes, serialize_generic, serialize_pdp,
)
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, validate_structure

__all__ = ["PostgresAuditParticipant", "PostgresAuditSink", "stage_reference", "source_reference"]


def _text(value):
    if type(value) is not str or not value:
        raise AuditError()


def _context(value):
    if type(value) is not ScopeContext:
        raise AuditError()
    validate_structure(value)


def stage_reference(operation_id, token, context):
    _text(operation_id)
    _text(token)
    _context(context)
    import json
    raw = json.dumps([operation_id, token, context.scope_type.value,
                      context.tenant_id, context.scope_id],
                     ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "audit-stage:" + hashlib.sha256(raw).hexdigest()


def source_reference(event_id, digest=None):
    _text(event_id)
    prefix = "audit-source:" + hashlib.sha256(event_id.encode("utf-8")).hexdigest()
    return prefix if digest is None else prefix + ":" + digest


def _connection(alias, *, outer):
    from django.db import connections
    _text(alias)
    from django.utils.connection import ConnectionDoesNotExist
    try:
        connection = connections[alias]
    except ConnectionDoesNotExist as error:
        raise AuditError("AUDIT_ALIAS_INVALID") from error
    if connection.vendor != "postgresql" or connection.in_atomic_block is not outer:
        raise AuditError("AUDIT_TRANSACTION_INVALID")
    return connection


def _xid(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_current_xact_id()::text")
        return cursor.fetchone()[0]


def _scope_filter(context):
    return {"scope_type": context.scope_type.value,
            "tenant_id": context.tenant_id, "scope_id": context.scope_id}


@dataclass(frozen=True, slots=True)
class PostgresAuditParticipant:
    policy_source: object
    clock: object
    peer_alias: str

    def __post_init__(self):
        if not callable(getattr(self.policy_source, "resolve", None)):
            raise AuditError()
        if not callable(getattr(self.clock, "now", None)):
            raise AuditError()
        _text(self.peer_alias)

    def now(self):
        now = self.clock.now()
        if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
            raise AuditError("AUDIT_CLOCK_INVALID")
        return now

    def policy(self, context, alias):
        _context(context)
        policy = self.policy_source.resolve(context=context, alias=alias)
        if type(policy) is not AuditPolicy:
            raise AuditError("AUDIT_POLICY_UNAVAILABLE")
        policy.__post_init__()
        return policy

    def _append(self, kind, payload, *, alias, operation_id, transaction_token,
                context, policy, source=None):
        from django.core.exceptions import ValidationError
        from django.db import IntegrityError, transaction
        from pixs.core.persistence.models_audit import CoreAuditEvent
        from pixs.core.persistence.models_authz import CoreTombstoneRef
        from pixs.core.persistence.uuid7 import generate_uuid7
        from pixs.core.services_common import lock_scopes

        connection = _connection(alias, outer=True)
        _text(operation_id)
        _text(transaction_token)
        _context(context)
        current_xid = _xid(connection)
        stage_key = stage_reference(operation_id, transaction_token, context)
        keys = [stage_key]
        if kind == "GENERIC_AUDIT":
            event_id = payload["event_id"]
            digest = hashlib.sha256(canonical_generic_bytes(payload)).hexdigest()
            source_key = source_reference(event_id)
            keys.append(source_key)
            lookup = {"generic_event_id": event_id}
        else:
            event_id, digest, source_key = None, None, None
            lookup = {"kind": kind, "operation_id": operation_id,
                      "transaction_token": transaction_token,
                      "pdp_decision_id": payload["decision_id"]}
        lock_scopes(alias, tuple(sorted(keys)))
        tombstones = CoreTombstoneRef.objects.using(alias)
        if tombstones.filter(deduplication_reference=stage_key).exists():
            raise AuditError("AUDIT_ALREADY_PURGED")
        if source_key and tombstones.filter(synchronization_reference__startswith=source_key + ":").exists():
            raise AuditError("AUDIT_ALREADY_PURGED")
        row = CoreAuditEvent.objects.using(alias).filter(**lookup).first()
        source_fields = {"c01_journal_id": None, "c01_sequence": None, "c01_event_sha256": None}
        if source is not None:
            source_fields = {"c01_journal_id": source[0], "c01_sequence": source[1],
                             "c01_event_sha256": source[2]}
        if row is not None:
            same_context = all(getattr(row, key) == value for key, value in _scope_filter(context).items())
            if kind == "GENERIC_AUDIT":
                same = row.generic_event_sha256 == digest and all(
                    getattr(row, key) == value for key, value in source_fields.items())
            else:
                same = (row.pdp_payload == payload and row.staged_xid == current_xid)
            if not same_context or not same:
                raise AuditError("AUDIT_COLLISION")
            return row
        raw = canonical_generic_bytes(payload) if kind == "GENERIC_AUDIT" else canonical_pdp_bytes(payload)
        if len(raw) > policy.max_event_bytes:
            raise AuditError("AUDIT_CAPACITY")
        now = self.now()
        row = CoreAuditEvent(
            record_id=generate_uuid7(), kind=kind, operation_id=operation_id,
            alias=alias, transaction_token=transaction_token, staged_xid=current_xid,
            **_scope_filter(context),
            generic_payload=payload if kind == "GENERIC_AUDIT" else None,
            pdp_payload=payload if kind == "PDP_AUDIT" else None,
            generic_event_id=event_id, generic_event_sha256=digest,
            pdp_decision_id=payload["decision_id"] if kind == "PDP_AUDIT" else None,
            **source_fields,
            retention_policy_id=policy.policy_id, retention_policy_version=policy.policy_version,
            retention_policy_origin=policy.origin, retention_days=policy.retention_days,
            governance_ref=policy.governance_ref, confidentiality=policy.confidentiality.value,
            personal=policy.personal.value, created_at=now, updated_at=now,
        )
        row._state.db = alias
        try:
            row.full_clean(validate_unique=False, validate_constraints=False)
            with transaction.atomic(using=alias):
                row.save(force_insert=True, using=alias)
        except (IntegrityError, ValidationError) as error:
            raise AuditError("AUDIT_RECORD_INVALID") from error
        return row

    def append_pdp(self, event, *, alias, operation_id, transaction_token, context):
        """Entrée d'adapter interne : un événement observé ne confère aucun droit."""
        _connection(alias, outer=True)
        if type(event) is not PdpAuditEvent:
            raise AuditError()
        event.__post_init__()
        _context(context)
        if event.context is not None and event.context != context:
            raise AuditError("AUDIT_CONTEXT_MISMATCH")
        policy = self.policy(context, alias)
        payload = apply_redactions_pdp(serialize_pdp(event), policy.redactions)
        canonical_pdp_bytes(payload)
        return self._append("PDP_AUDIT", payload, alias=alias, operation_id=operation_id,
                            transaction_token=transaction_token, context=context, policy=policy)

    def stage(self, event, *, alias, operation_id, transaction_token, context, decision):
        try:
            if type(event) is not PdpAuditEvent:
                raise AuditError()
            event.__post_init__()
            if decision is None:
                if event.effect is not Effect.DENY:
                    raise AuditError("AUDIT_DECISION_MISSING")
            else:
                if type(decision) is not Decision:
                    raise AuditError()
                if (decision.decision_id != event.decision_id or decision.policy_version != event.policy_version
                        or (event.effect is Effect.ALLOW and decision.effect is not Effect.ALLOW)):
                    raise AuditError("AUDIT_DECISION_MISMATCH")
                now = self.now()
                if (type(decision.evaluated_at) is not datetime.datetime
                        or decision.evaluated_at.tzinfo is not datetime.timezone.utc
                        or decision.evaluated_at > now):
                    raise AuditError("AUDIT_DECISION_STALE")
                if event.evaluated_at is not None and not decision.evaluated_at <= event.evaluated_at <= now:
                    raise AuditError("AUDIT_EVENT_TIME_INVALID")
                if event.effect is Effect.ALLOW and (
                    type(decision.expires_at) is not datetime.datetime
                    or decision.expires_at.tzinfo is not datetime.timezone.utc
                    or not now < decision.expires_at
                ):
                    raise AuditError("AUDIT_DECISION_STALE")
            self.append_pdp(event, alias=alias, operation_id=operation_id,
                            transaction_token=transaction_token, context=context)
            return StagedRef(operation_id, alias, transaction_token, context, "audit")
        except AuditError as error:
            raise CorePortError() from error

    def stage_generic(self, event, *, alias, operation_id, transaction_token, context, source=None):
        _connection(alias, outer=True)
        policy = self.policy(context, alias)
        original = serialize_generic(event)
        if original["tenant_reference"] != context.tenant_id:
            raise AuditError("AUDIT_CONTEXT_MISMATCH")
        payload = apply_redactions_generic(original, policy.redactions)
        canonical_generic_bytes(payload)
        if source is not None and payload != original:
            raise AuditError("AUDIT_SOURCE_TRANSFORMED")
        return self._append("GENERIC_AUDIT", payload, alias=alias, operation_id=operation_id,
                            transaction_token=transaction_token, context=context,
                            policy=policy, source=source)

    def stage_observation(self, event, *, source, alias, operation_id, transaction_token, context):
        """Stage d'un fait committé propriétaire, sans réutiliser son ancien ALLOW.

        source vérifie la provenance et l'autorité courante de réconciliation
        sous verrous dans la transaction propriétaire. Aucun effet métier
        nouveau n'est autorisé par cette observation.
        """
        connection = _connection(alias, outer=True)
        _context(context)
        verify = getattr(source, "verify_committed_observation", None)
        if not callable(verify):
            raise AuditError("AUDIT_OBSERVATION_SOURCE_UNAVAILABLE")
        payload = serialize_generic(event)
        digest = hashlib.sha256(canonical_generic_bytes(payload)).hexdigest()
        args = dict(event=event, alias=alias, operation_id=operation_id,
                    transaction_token=transaction_token, context=context)
        if verify(**args) is not None:
            raise AuditError("AUDIT_OBSERVATION_SOURCE_INVALID")
        policy = self.policy(context, alias)
        if apply_redactions_generic(payload, policy.redactions) != payload:
            raise AuditError("AUDIT_OBSERVATION_TRANSFORMED")
        row = self.stage_generic(event, alias=alias, operation_id=operation_id,
                                 transaction_token=transaction_token, context=context)
        if row.generic_event_sha256 != digest:
            raise AuditError("AUDIT_OBSERVATION_TRANSFORMED")
        if (row.operation_id != operation_id or row.transaction_token != transaction_token
                or row.staged_xid != _xid(connection)):
            raise AuditError("AUDIT_OBSERVATION_ALREADY_RECORDED")
        if verify(**args) is not None:
            raise AuditError("AUDIT_OBSERVATION_SOURCE_INVALID")
        return StagedRef(operation_id, alias, transaction_token, context, "audit")

    def confirm_observation(self, event, *, alias, context):
        """Constat committé indépendant identité+contenu+contexte, sans insertion.

        Le caller reste responsable de son autorité courante et de la preuve
        propriétaire avant de solder une référence Auth. Aucun ABSENT inféré.
        """
        from django.db import DatabaseError, InterfaceError, connections
        from django.core.exceptions import ValidationError
        from django.utils.connection import ConnectionDoesNotExist
        from pixs.core.persistence.models_audit import CoreAuditEvent
        from pixs.core.persistence.models_authz import CoreTombstoneRef
        _text(alias)
        _context(context)
        payload = serialize_generic(event)
        digest = hashlib.sha256(canonical_generic_bytes(payload)).hexdigest()
        if self.peer_alias == alias:
            return "UNKNOWN"
        peer = None
        try:
            owner = connections[alias]
            peer = _connection(self.peer_alias, outer=False)
            if owner.vendor != "postgresql" or not peer.get_autocommit():
                return "UNKNOWN"
            keys = ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")
            if any(owner.settings_dict.get(key) != peer.settings_dict.get(key) for key in keys):
                return "UNKNOWN"
            row = CoreAuditEvent.objects.using(self.peer_alias).filter(
                generic_event_id=event.event_id, generic_event_sha256=digest,
                **_scope_filter(context)).first()
            if row is not None:
                row.clean()
                return "CONFIRMED"
            exact_source = source_reference(event.event_id, digest)
            tombstone = CoreTombstoneRef.objects.using(self.peer_alias).filter(
                synchronization_reference=exact_source,
                tenant_ref=context.tenant_id, scope_ref=context.scope_id).exists()
            return "CONFIRMED" if tombstone else "UNKNOWN"
        except (DatabaseError, InterfaceError, ConnectionDoesNotExist, AuditError, ValueError, ValidationError):
            return "UNKNOWN"
        finally:
            if peer is not None and not peer.in_atomic_block:
                peer.close()

    def verify_staged(self, proof):
        from pixs.core.persistence.models_audit import CoreAuditEvent
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        connection = _connection(proof.alias, outer=True)
        if not any(ref.staged_kind == "audit" for ref in proof.staged):
            raise CorePortError()
        rows = list(CoreAuditEvent.objects.using(proof.alias).filter(
            operation_id=proof.operation_id, transaction_token=proof.transaction_token,
            staged_xid=_xid(connection), **_scope_filter(proof.context)))
        if not rows:
            raise CorePortError()
        for row in rows:
            row.clean()
        return None

    def reconcile_unknown(self, proof):
        from django.db import DatabaseError, InterfaceError, connections
        from django.core.exceptions import ValidationError
        from django.utils.connection import ConnectionDoesNotExist
        from pixs.core.persistence.models_audit import CoreAuditEvent
        from pixs.core.persistence.models_authz import CoreTombstoneRef
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        if self.peer_alias == proof.alias:
            return "UNKNOWN"
        peer = None
        try:
            owner = connections[proof.alias]
            peer = _connection(self.peer_alias, outer=False)
            if owner.in_atomic_block or not peer.get_autocommit():
                return "UNKNOWN"
            keys = ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")
            if any(owner.settings_dict.get(key) != peer.settings_dict.get(key) for key in keys):
                return "UNKNOWN"
            rows = list(CoreAuditEvent.objects.using(self.peer_alias).filter(
                operation_id=proof.operation_id, transaction_token=proof.transaction_token,
                **_scope_filter(proof.context)))
            if rows:
                for row in rows:
                    row.clean()
                return "CONFIRMED"
            tomb = CoreTombstoneRef.objects.using(self.peer_alias).filter(
                deduplication_reference=stage_reference(proof.operation_id, proof.transaction_token, proof.context),
                tenant_ref=proof.context.tenant_id, scope_ref=proof.context.scope_id).exists()
            return "CONFIRMED" if tomb else "UNKNOWN"
        except (DatabaseError, InterfaceError, ConnectionDoesNotExist, AuditError, ValueError, ValidationError):
            return "UNKNOWN"
        finally:
            if peer is not None and not peer.in_atomic_block:
                peer.close()


@dataclass(frozen=True, slots=True)
class PostgresAuditSink:
    """Adapter AuditSink : bool d'acquittement, jamais un reçu de conformité P0."""
    participant: PostgresAuditParticipant
    alias: str
    context: ScopeContext
    operation_id: str

    def __post_init__(self):
        if type(self.participant) is not PostgresAuditParticipant:
            raise AuditError()
        _text(self.alias)
        _text(self.operation_id)
        _context(self.context)

    def record(self, event):
        from django.db import connections, transaction
        from pixs.core.persistence.uuid7 import generate_uuid7
        connection = connections[self.alias]
        if connection.vendor != "postgresql":
            raise AuditError()
        token = generate_uuid7().hex
        if connection.in_atomic_block:
            self.participant.append_pdp(event, alias=self.alias, operation_id=self.operation_id,
                                        transaction_token=token, context=self.context)
        else:
            with transaction.atomic(using=self.alias, durable=True):
                self.participant.append_pdp(event, alias=self.alias, operation_id=self.operation_id,
                                            transaction_token=token, context=self.context)
        return True
