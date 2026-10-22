"""Reprise C01 scellée : lot complet, commit C05 et vérification indépendante."""
from __future__ import annotations

import dataclasses
import datetime
import hashlib
import json
import os
import uuid
from dataclasses import dataclass

from pixs.core.audit_contracts import AuditError
from pixs.core.scope.context import ScopeType, validate_structure

__all__ = ["SealedBootstrapSource", "CommittedBootstrapImport", "import_sealed_bootstrap", "verify_committed_import"]


@dataclass(frozen=True, slots=True)
class SealedBootstrapSource:
    journal_dir: str
    journal_uid: int
    journal_id: str
    max_event_bytes: int
    max_journal_bytes: int

    def __post_init__(self):
        from pixs.core.persistence.uuid7 import check_uuid7
        if type(self.journal_dir) is not str or not os.path.isabs(self.journal_dir):
            raise AuditError()
        if type(self.journal_uid) is not int or self.journal_uid < 0:
            raise AuditError()
        if type(self.journal_id) is not str:
            raise AuditError()
        try:
            value = uuid.UUID(self.journal_id)
            check_uuid7(value)
        except ValueError as error:
            raise AuditError() from error
        if str(value) != self.journal_id:
            raise AuditError()
        for limit in (self.max_event_bytes, self.max_journal_bytes):
            if type(limit) is not int or limit < 1:
                raise AuditError()

    def read(self):
        from pixs.backend.bootstrap_audit import list_sealed_records
        self.__post_init__()
        return list_sealed_records(journal_dir=self.journal_dir, journal_uid=self.journal_uid,
                                   journal_id=self.journal_id, max_event_bytes=self.max_event_bytes,
                                   max_journal_bytes=self.max_journal_bytes)


@dataclass(frozen=True, slots=True)
class CommittedBootstrapImport:
    journal_id: str
    batch_sha256: str
    receipts: tuple
    verified_at: datetime.datetime | None


def _batch_hash(receipts):
    return hashlib.sha256(json.dumps(
        [[r.event_id, r.sequence, r.event_sha256] for r in receipts],
        ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def _marker_id(journal_id, digest):
    return "audit-bootstrap-transfer:" + journal_id + ":" + digest


def verify_committed_import(*, participant, alias, context, result):
    from django.db import DatabaseError, InterfaceError, connections
    from django.core.exceptions import ValidationError
    from pixs.backend.bootstrap_audit import BootstrapAuditReceiptV1
    from pixs.core.audit_sink import PostgresAuditParticipant, _connection, source_reference
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.models_authz import CoreTombstoneRef
    if type(participant) is not PostgresAuditParticipant or type(result) is not CommittedBootstrapImport:
        raise AuditError()
    validate_structure(context)
    if context.scope_type is not ScopeType.PLATFORM or type(result.receipts) is not tuple:
        raise AuditError()
    if participant.peer_alias == alias:
        raise AuditError("AUDIT_INDEPENDENT_CONNECTION_REQUIRED")
    from pixs.core.persistence.uuid7 import check_uuid7
    if type(result.journal_id) is not str or type(result.batch_sha256) is not str or len(result.batch_sha256) != 64:
        raise AuditError()
    try:
        journal_uuid = uuid.UUID(result.journal_id)
        check_uuid7(journal_uuid)
    except ValueError as error:
        raise AuditError() from error
    if str(journal_uuid) != result.journal_id or any(char not in "0123456789abcdef" for char in result.batch_sha256):
        raise AuditError()
    expected_sequence = 1
    for receipt in result.receipts:
        if (type(receipt) is not BootstrapAuditReceiptV1 or receipt.journal_id != result.journal_id
                or type(receipt.sequence) is not int or receipt.sequence != expected_sequence
                or type(receipt.event_id) is not str or type(receipt.event_sha256) is not str
                or len(receipt.event_sha256) != 64 or any(char not in "0123456789abcdef" for char in receipt.event_sha256)):
            raise AuditError()
        expected_sequence += 1
    if _batch_hash(result.receipts) != result.batch_sha256:
        raise AuditError("AUDIT_IMPORT_DIGEST_INVALID")
    peer = None
    try:
        owner = connections[alias]
        peer = _connection(participant.peer_alias, outer=False)
        if owner.in_atomic_block or not peer.get_autocommit():
            raise AuditError("AUDIT_IMPORT_BOUNDARY_INVALID")
        if any(owner.settings_dict.get(k) != peer.settings_dict.get(k) for k in ("ENGINE", "HOST", "PORT", "NAME", "OPTIONS")):
            raise AuditError("AUDIT_IMPORT_DATABASE_MISMATCH")
        marker = CoreAuditEvent.objects.using(participant.peer_alias).filter(
            generic_event_id=_marker_id(result.journal_id, result.batch_sha256),
            scope_type="PLATFORM", tenant_id=None, scope_id=None).first()
        if marker is None:
            raise AuditError("AUDIT_IMPORT_UNCONFIRMED")
        marker.clean()
        for receipt in result.receipts:
            row = CoreAuditEvent.objects.using(participant.peer_alias).filter(
                generic_event_id=receipt.event_id, c01_journal_id=uuid.UUID(result.journal_id),
                c01_sequence=receipt.sequence, c01_event_sha256=receipt.event_sha256,
                scope_type="PLATFORM", tenant_id=None, scope_id=None).first()
            if row is not None:
                row.clean()
                continue
            expected = source_reference(receipt.event_id, receipt.event_sha256) + ":" + result.journal_id + ":" + str(receipt.sequence)
            tomb = CoreTombstoneRef.objects.using(participant.peer_alias).filter(
                synchronization_reference=expected, tenant_ref=None, scope_ref=None).exists()
            if not tomb:
                raise AuditError("AUDIT_IMPORT_UNCONFIRMED")
    except (DatabaseError, InterfaceError, ValidationError) as error:
        raise AuditError("AUDIT_IMPORT_UNCONFIRMED") from error
    finally:
        if peer is not None and not peer.in_atomic_block:
            peer.close()
    return dataclasses.replace(result, verified_at=participant.now())


def import_sealed_bootstrap(*, ports, request, source, alias, operation_id, component_version):
    from django.db import DatabaseError, InterfaceError, transaction
    from pixs.backend.bootstrap_audit import BootstrapAuditReceiptV1, canonical_event_bytes, event_sha256
    from pixs.core.audit_sink import PostgresAuditParticipant, _connection
    from pixs.core.audit_access import _audit, _refusal
    from pixs.core.ports import CoreServicePorts, BootstrapServicePorts, CorePortError
    from pixs.core.authz.ports import Request, PortError
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.services_common import allow, published_profile, lock_scopes, CoreServiceError
    from pixs.kernel.audit_event import AuditEvent

    if type(source) is not SealedBootstrapSource or type(request) is not Request:
        raise AuditError()
    if type(ports) not in (CoreServicePorts, BootstrapServicePorts) or type(ports.audit) is not PostgresAuditParticipant:
        raise AuditError("AUDIT_PARTICIPANT_UNAVAILABLE")
    ports.__post_init__()
    request.__post_init__()
    validate_structure(request.context)
    source.__post_init__()
    _connection(alias, outer=False)
    if (request.context.scope_type is not ScopeType.PLATFORM
            or request.action_id != "pixs.core.audit.bootstrap_import"
            or request.resource_id != "bootstrap-journal:" + source.journal_id
            or type(operation_id) is not str or not operation_id
            or type(component_version) is not str):
        raise AuditError()
    participant = ports.audit
    token = generate_uuid7().hex
    result = None
    commit_attempted = False
    try:
        allow(ports, request, under_locks=False, alias=alias, operation_id=operation_id)
        records = source.read()
        if type(records) is not tuple:
            raise AuditError()
        receipts = []
        ids = set()
        for sequence, item in enumerate(records, 1):
            if type(item) is not dict or set(item) != {"journal_id", "sequence", "event", "event_sha256"}:
                raise AuditError()
            if item["journal_id"] != source.journal_id or type(item["sequence"]) is not int or item["sequence"] != sequence:
                raise AuditError("AUDIT_IMPORT_ORDER_INVALID")
            event = item["event"]
            raw = canonical_event_bytes(event)
            if (event.event_id in ids or len(raw) > source.max_event_bytes
                    or event_sha256(event) != item["event_sha256"]):
                raise AuditError("AUDIT_IMPORT_DIGEST_INVALID")
            ids.add(event.event_id)
            receipts.append(BootstrapAuditReceiptV1(source.journal_id, event.event_id, sequence, item["event_sha256"]))
        result = CommittedBootstrapImport(source.journal_id, _batch_hash(receipts), tuple(receipts), None)
        with transaction.atomic(using=alias, durable=True):
            lock_scopes(alias, ("audit-bootstrap:" + source.journal_id,))
            _, decision = allow(ports, request, under_locks=True, alias=alias, operation_id=operation_id)
            _, waived, governance_waived = published_profile(
                ports, request, decision, alias=alias, operation_id=operation_id, token=token)
            for item in records:
                participant.stage_generic(
                    item["event"], alias=alias, operation_id=operation_id,
                    transaction_token=token, context=request.context,
                    source=(uuid.UUID(source.journal_id), item["sequence"], item["event_sha256"]))
            marker_id = _marker_id(source.journal_id, result.batch_sha256)
            marker = CoreAuditEvent.objects.using(alias).filter(generic_event_id=marker_id).first()
            if marker is None:
                event = AuditEvent(marker_id, participant.now().isoformat(), request.subject_id, None,
                                   "pixs.core.audit.bootstrap_import", "bootstrap-journal",
                                   source.journal_id, "IMPORTED", "batch-sha256:" + result.batch_sha256,
                                   (request.correlation_id,), (), "pixs.core", component_version)
                participant.stage_generic(event, alias=alias, operation_id=operation_id,
                                          transaction_token=token, context=request.context)
            _audit(ports, request, decision, alias, operation_id, token, waived)
            _, fresh = allow(ports, request, under_locks=True, alias=alias, operation_id=operation_id)
            _, final_waived, final_governance_waived = published_profile(
                ports, request, fresh, alias=alias, operation_id=operation_id, token=token)
            if fresh.policy_version != decision.policy_version or (waived, governance_waived) != (final_waived, final_governance_waived):
                raise AuditError("AUDIT_IMPORT_AUTHORITY_CHANGED")
            commit_attempted = True
        return verify_committed_import(participant=participant, alias=alias, context=request.context, result=result)
    except (DatabaseError, InterfaceError) as error:
        if commit_attempted and result is not None:
            try:
                return verify_committed_import(participant=participant, alias=alias, context=request.context, result=result)
            except AuditError as unconfirmed:
                raise AuditError("AUDIT_IMPORT_COMMIT_UNKNOWN") from ExceptionGroup(
                    "Issue du transfert indéterminée", [error, unconfirmed])
        _refusal(ports, request, alias, operation_id, error)
    except (AuditError, CorePortError, PortError, CoreServiceError, ValueError) as error:
        _refusal(ports, request, alias, operation_id, error)
