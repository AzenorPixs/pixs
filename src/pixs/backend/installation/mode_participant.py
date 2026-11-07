"""Participant C08 concret au protocole C06, sans autorite inventee."""
from __future__ import annotations

import datetime as dt
import copy
import os
import threading
from dataclasses import dataclass
from typing import NoReturn

from django.db import connections, transaction, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.installation.marker import MarkerInvalid, read_installation_marker
from pixs.backend.installation.mode_commands import (
    MODE_SERIALIZER_VERSION,
    ModeCommandInput,
    check_mode_command,
    mode_action_ref,
    mode_command_type,
    mode_content_sha256,
    mode_resource_ref,
)
from pixs.backend.installation.mode_governance import C10ModeGovernanceAdapter
from pixs.backend.installation.mode_reader import C08InstalledModeReader, _parent_model
from pixs.backend.installation.mode_values import (
    ConfigurationState, ModeOperationKind, ModeValuesError, transition_state, validate_state_pair,
)
from pixs.backend.startup_mode import StartupMode
from pixs.backend.installation.result_writer import _native_context
from pixs.core.audit_contracts import AuditError, decode_policy_version, encode_policy_version
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import PortError
from pixs.core.dto import CommandEnvelope, CoreInputInvalid, CoreMutationResult
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7, generate_uuid7
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.services_transaction_types import AppliedMutation, MutationContext
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import CoreServiceError
from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
from pixs.core.services_runtime_store import ROOT_PERMITTED

__all__ = ["C08ModeIdempotenceParticipant"]

_CHECK = "c08-modes:check-v1"
_RESULT = "c08-modes:result-v1"


def _fail(code: str = "IDEMPOTENCE_PREUVE_INVALIDE") -> NoReturn:
    raise CoreServiceError(code)


def _text(value: object, limit: int) -> None:
    if type(value) is not str or not 0 < len(value) <= limit or not value.isprintable():
        raise CorePortError()
    try:
        value.encode("utf-8")
    except UnicodeError:
        raise CorePortError() from None


def _receipt_model():
    from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord
    return C08ModeOperationReceiptRecord


def _snapshot_model():
    from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord
    return C08ModeSnapshotRecord


def _row_values(row) -> dict:
    return {field.attname: copy.deepcopy(getattr(row, field.attname))
            for field in row._meta.concrete_fields}


@dataclass(slots=True, repr=False)
class _Frame:
    alias: str
    operation_id: str
    token: str
    context: ScopeContext
    command: ModeCommandInput
    key: tuple
    native: tuple
    receipt_snapshot: dict
    check: StagedRef
    started_at: dt.datetime
    fresh: bool
    result_stage: StagedRef | None
    policy_encoded: object
    governance_status: str
    root_state: str
    pin: tuple
    mode_publication: tuple
    mode_metadata: dict
    decision: Decision
    phase: str
    base_view: dict
    marker_snapshot: object
    applied_result: AppliedMutation | None
    result_snapshot: dict | None


class C08ModeIdempotenceParticipant:
    def __init__(self, *, using: str, inspection_using: str, clock, envelope: CommandEnvelope, command: ModeCommandInput, reader: C08InstalledModeReader, decider: RuntimeAuthorizationDecider, governance: C10ModeGovernanceAdapter | None) -> None:
        if type(reader) is not C08InstalledModeReader:
            raise CorePortError()
        try:
            reader_marker = object.__getattribute__(reader, "_marker")
            reader_using = object.__getattribute__(reader, "_using")
            reader_inspection = object.__getattribute__(reader, "_inspection")
            reader_installation = object.__getattribute__(reader, "_installation")
            reader_clock = object.__getattribute__(reader, "_clock")
            reader_marker.__post_init__()
        except (AttributeError, MarkerInvalid):
            raise CorePortError() from None
        limit = reader_marker.max_ref_len
        for value in (using, inspection_using):
            _text(value, limit)
        if using == inspection_using:
            raise CorePortError()
        if reader_using != using or reader_inspection != inspection_using:
            raise CorePortError()
        if not callable(getattr(clock, "now", None)):
            raise CorePortError()
        if reader_clock is not clock:
            raise CorePortError()
        if type(envelope) is not CommandEnvelope or type(command) is not ModeCommandInput:
            raise CorePortError()
        try:
            envelope.__post_init__()
            check_mode_command(command, max_ref_len=limit)
        except (CoreInputInvalid, ValueError):
            raise CorePortError() from None
        if type(decider) is not RuntimeAuthorizationDecider:
            raise CorePortError()
        try:
            decider_request = object.__getattribute__(decider, "_request")
            decider_operation = object.__getattribute__(decider, "_operation_id")
            decider_clock = object.__getattribute__(decider, "_clock")
        except AttributeError:
            raise CorePortError() from None
        if decider_clock is not clock:
            raise CorePortError()
        if decider_request != envelope.request or decider_operation != envelope.operation_id:
            raise CorePortError()
        if governance is not None and type(governance) is not C10ModeGovernanceAdapter:
            raise CorePortError()
        if governance is not None and governance._clock is not clock:
            raise CorePortError()
        if command.installation_ref != reader_installation:
            raise CorePortError()
        if envelope.request.subject_id != command.actor_ref:
            raise CorePortError()
        if envelope.idempotency_key != command.idempotency_key:
            raise CorePortError()
        if envelope.serializer_version != MODE_SERIALIZER_VERSION:
            raise CorePortError()
        try:
            expected_resource = mode_resource_ref(command, max_ref_len=limit)
            expected_action = mode_action_ref(command.kind)
            expected_hash = mode_content_sha256(command, max_ref_len=limit)
        except ValueError:
            raise CorePortError() from None
        if envelope.request.resource_id != expected_resource:
            raise CorePortError()
        if envelope.request.action_id != expected_action:
            raise CorePortError()
        if envelope.content_sha256 != expected_hash:
            raise CorePortError()
        self._alias = using
        self._peer = inspection_using
        self._clock = clock
        self._envelope = envelope
        self._command = command
        self._reader = reader
        self._decider = decider
        self._governance = governance
        self._limit = limit
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._frames: list[_Frame] = []
        self._attempts = 0
        self._reconciled = False

    def _stable(self) -> None:
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()

    def _now(self) -> dt.datetime:
        self._stable()
        try:
            now = self._clock.now()
        except (PortError, CorePortError, CoreInputInvalid, DatabaseError, InterfaceError):
            raise CorePortError() from None
        if type(now) is not dt.datetime or now.tzinfo is not dt.timezone.utc:
            raise CorePortError()
        return now

    def check_or_stage(self, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, subject_id: str, command_type: str, idempotency_key: str, content_sha256: str, serializer_version: str) -> StagedRef:
        self._stable()
        for value in (alias, operation_id, transaction_token, subject_id, idempotency_key):
            _text(value, self._limit)
        if type(context) is not ScopeContext:
            raise CorePortError()
        if context != self._envelope.request.context or context.scope_type is not ScopeType.PLATFORM:
            raise CorePortError()
        if alias != self._alias or operation_id != self._envelope.operation_id:
            raise CorePortError()
        if subject_id != self._command.actor_ref or idempotency_key != self._command.idempotency_key:
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        try:
            expected_type = mode_command_type(self._command.kind)
            expected_hash = mode_content_sha256(self._command, max_ref_len=self._limit)
        except ValueError:
            raise CorePortError() from None
        if command_type != expected_type:
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        if content_sha256 != self._envelope.content_sha256 or content_sha256 != expected_hash:
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        if serializer_version != MODE_SERIALIZER_VERSION or serializer_version != self._envelope.serializer_version:
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        if self._attempts != 0 and not (self._attempts == 1 and self._reconciled and len(self._frames) == 1):
            raise CoreServiceError("IDEMPOTENCE_CADRE_EPUISE")
        self._attempts += 1
        try:
            marker = read_installation_marker(object.__getattribute__(self._reader, "_marker"))
        except MarkerInvalid:
            raise CorePortError() from None
        if marker.installation_ref != self._command.installation_ref:
            raise CorePortError()
        try:
            native = _native_context(alias)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        started = self._now()
        request = self._envelope.request
        try:
            snapshot, _topology, pin, epoch, state = self._decider.prepare_core_under_locks(request, alias, operation_id)
        except PortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        try:
            decision = self._decider.revalidate_under_locks(request, alias=alias, operation_id=operation_id)
        except PortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if type(decision) is not Decision or decision.effect is not Effect.ALLOW:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if decision.decision_id != request.decision_id:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        checked_at = self._now()
        if decision.reason_code != "ALLOWED":
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if not (type(decision.evaluated_at) is dt.datetime and decision.evaluated_at.tzinfo is dt.timezone.utc and type(decision.expires_at) is dt.datetime and decision.expires_at.tzinfo is dt.timezone.utc and decision.evaluated_at <= checked_at < decision.expires_at):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            policy_encoded = encode_policy_version(decision.policy_version)
            if decode_policy_version(policy_encoded) != decision.policy_version:
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        except AuditError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if self._command.kind is ModeOperationKind.FINALIZE_CONFIGURATION and state != ROOT_PERMITTED:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if transaction_identity(alias) != pin:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            after_native = _native_context(alias)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if after_native[0] is not native[0] or after_native[1:] != native[1:]:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            waived = self._decider.governance_waived(request, decision, alias=alias, operation_id=operation_id)
        except PortError:
            raise CoreServiceError("GOUVERNANCE_ABSENTE") from None
        if type(waived) is not bool:
            raise CoreServiceError("GOUVERNANCE_ABSENTE")
        if waived is True:
            governance_status = "WAIVED"
            mode_publication = (None, None, None)
            mode_metadata: dict = {"metadata_profile_ref": None, "metadata_published_version": None, "metadata_owner_component": None, "metadata_source_of_truth": None, "governance_ref": None, "confidentiality": None, "personal": None, "retention_policy": None, "deletion_policy": None, "publication_ref": None, "catalog_version": None, "catalog_sha256": None}
        else:
            if self._governance is None:
                raise CoreServiceError("GOUVERNANCE_ABSENTE")
            try:
                mode_wrap, _meta_wrap = self._governance._profiles()
            except CorePortError:
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
            if mode_wrap.profile.owner_component != "pixs.backend":
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
            prof = mode_wrap.profile
            governance_status = "GOVERNED"
            mode_publication = (mode_wrap.publication_ref, mode_wrap.catalog_version, mode_wrap.raw_sha256)
            mode_metadata = {"metadata_profile_ref": self._governance._core.owner.config.binding.profile_ref, "metadata_published_version": mode_wrap.published_version, "metadata_owner_component": prof.owner_component, "metadata_source_of_truth": prof.source_of_truth, "governance_ref": prof.data_asset_id, "confidentiality": prof.confidentiality.value, "personal": prof.personal_data.value, "retention_policy": prof.retention_policy, "deletion_policy": prof.deletion_policy, "publication_ref": mode_wrap.publication_ref, "catalog_version": mode_wrap.catalog_version, "catalog_sha256": mode_wrap.raw_sha256}
        try:
            _mode_value, view = self._reader._load_all(alias, native[3], native[4], started)
        except (CorePortError, DatabaseError, InterfaceError, ConnectionDoesNotExist):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        model = _receipt_model()
        try:
            by_op = model.objects.using(alias).filter(operation_id=operation_id).first()
        except (DatabaseError, InterfaceError):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if by_op is not None and (by_op.installation_id != self._command.installation_ref or by_op.actor_ref != self._command.actor_ref or by_op.kind != self._command.kind.value or by_op.idempotency_key != self._command.idempotency_key):
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        try:
            row = model.objects.using(alias).filter(installation_id=self._command.installation_ref, actor_ref=self._command.actor_ref, kind=self._command.kind.value, idempotency_key=self._command.idempotency_key).first()
        except (DatabaseError, InterfaceError):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        fresh = row is None
        if fresh:
            if self._frames:
                raise CoreServiceError("ISSUE_INCONNUE")
            if self._command.expected_version != _mode_value.version:
                raise CoreServiceError("IDEMPOTENCE_CONFLIT")
            try:
                record_id = generate_uuid7()
                self._reader._check_uuid(record_id)
            except (Uuid7Error, CorePortError):
                raise CorePortError() from None
            row_kwargs = {"record_id": record_id, "operation_id": operation_id, "installation_id": self._command.installation_ref, "actor_ref": self._command.actor_ref, "scope_type": "PLATFORM", "tenant_id": None, "scope_id": None, "kind": self._command.kind.value, "expected_version": self._command.expected_version, "content_sha256": content_sha256, "serializer_version": serializer_version, "idempotency_key": idempotency_key, "correlation_id": self._envelope.correlation_id, "causation_id": self._envelope.causation_id, "transaction_token": transaction_token, "authorization_ref": request.decision_id, "policy_version": policy_encoded, "pid": native[1], "xid": native[2], "database_oid": native[3], "schema_oid": native[4], "started_at": started, "status": "IN_PROGRESS", "governance_status": governance_status}
            row_kwargs.update(mode_metadata)
            try:
                created = model.objects.using(alias).create(**row_kwargs)
                row = model.objects.using(alias).get(record_id=created.record_id)
            except (DatabaseError, InterfaceError):
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        snapshot_dict = _row_values(row)
        if snapshot_dict["content_sha256"] != content_sha256 or snapshot_dict["serializer_version"] != serializer_version or snapshot_dict["scope_type"] != "PLATFORM" or snapshot_dict["tenant_id"] is not None or snapshot_dict["scope_id"] is not None:
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        if snapshot_dict["installation_id"] != self._command.installation_ref or snapshot_dict["actor_ref"] != self._command.actor_ref or snapshot_dict["kind"] != self._command.kind.value or snapshot_dict["idempotency_key"] != idempotency_key or snapshot_dict["expected_version"] != self._command.expected_version:
            raise CoreServiceError("IDEMPOTENCE_CONFLIT")
        if not fresh and snapshot_dict["status"] != "SUCCEEDED":
            raise CoreServiceError("ISSUE_INCONNUE")
        ref = StagedRef(operation_id, alias, transaction_token, context, _CHECK)
        frame = _Frame(alias, operation_id, transaction_token, context, self._command, (self._command.installation_ref, self._command.actor_ref, self._command.kind.value, self._command.idempotency_key), native, snapshot_dict, ref, started, fresh, None, policy_encoded, governance_status, state, pin, mode_publication, mode_metadata, decision, "CHECK", copy.deepcopy(view), marker, None, None)
        self._frames.append(frame)
        return ref

    def _receipt_shape(self, row, frame: _Frame) -> None:
        self._stable()
        if type(row) is not _receipt_model():
            raise CorePortError()
        try:
            self._reader._check_uuid(row.record_id)
        except CorePortError:
            raise
        except (Uuid7Error, AttributeError):
            raise CorePortError() from None
        try:
            object.__getattribute__(self._reader, "_check_native_historic")(object.__getattribute__(row, "pid"), object.__getattribute__(row, "xid"), object.__getattribute__(row, "database_oid"), object.__getattribute__(row, "schema_oid"), frame.native[3], frame.native[4])
        except CorePortError:
            raise
        if object.__getattribute__(row, "scope_type") != "PLATFORM" or object.__getattribute__(row, "tenant_id") is not None or object.__getattribute__(row, "scope_id") is not None:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if object.__getattribute__(row, "kind") not in ("FINALIZE_CONFIGURATION", "ENTER_MAINTENANCE", "EXIT_MAINTENANCE"):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if object.__getattribute__(row, "status") not in ("IN_PROGRESS", "SUCCEEDED"):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if object.__getattribute__(row, "result_kind") is not None and object.__getattribute__(row, "result_kind") not in ("NEW_SNAPSHOT", "NO_CHANGE"):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        for name in ("operation_id", "actor_ref", "serializer_version", "idempotency_key", "correlation_id", "transaction_token", "authorization_ref", "xid"):
            value = object.__getattribute__(row, name)
            if type(value) is not str or not value or len(value) > self._limit or not value.isprintable():
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        for name in ("expected_version", "result_version"):
            value = object.__getattribute__(row, name)
            if value is not None and (type(value) is bool or type(value) is not int or value < 1):
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if object.__getattribute__(row, "status") != "SUCCEEDED":
            raise CoreServiceError("ISSUE_INCONNUE")
        now = self._now()
        try:
            object.__getattribute__(self._reader, "_check_date")(object.__getattribute__(row, "started_at"), now)
            object.__getattribute__(self._reader, "_check_date")(object.__getattribute__(row, "finished_at"), now)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if object.__getattribute__(row, "finished_at") < object.__getattribute__(row, "started_at"):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if object.__getattribute__(row, "result_persistence_state") != DataPersistenceState.ACTIVE.value:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if object.__getattribute__(row, "result_correlation_id") != object.__getattribute__(row, "correlation_id"):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            stable_ref = mode_resource_ref(frame.command, max_ref_len=self._limit)
        except ValueError:
            raise CorePortError() from None
        if object.__getattribute__(row, "result_ref") != stable_ref:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            object.__getattribute__(self._reader, "_check_governed")(row)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        try:
            decoded = decode_policy_version(object.__getattribute__(row, "policy_version"))
        except AuditError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if (type(decoded) is not tuple or len(decoded) != 2
                or type(decoded[0]) is not str or not decoded[0]
                or type(decoded[1]) is not tuple
                or any(type(p) is not tuple or len(p) != 2
                       or any(type(v) is not str or not v for v in p)
                       for p in decoded[1])):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if row.serializer_version != MODE_SERIALIZER_VERSION:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            original = ModeCommandInput(
                installation_ref=row.installation_id, actor_ref=row.actor_ref,
                kind=ModeOperationKind(row.kind), expected_version=row.expected_version,
                idempotency_key=row.idempotency_key,
            )
            expected_digest = mode_content_sha256(original, max_ref_len=self._limit)
        except ValueError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if expected_digest != row.content_sha256:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if row.installation_id != frame.command.installation_ref:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if row.causation_id is not None:
            _text(row.causation_id, self._limit)
        if type(row.expected_version) is not int or row.expected_version < 1:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        if type(row.result_version) is not int or row.result_version < 1:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            if encode_policy_version(decoded) != object.__getattribute__(row, "policy_version"):
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        except AuditError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        return None

    def _snapshot_shape(self, row, frame: _Frame) -> None:
        if type(row) is not _snapshot_model():
            raise CorePortError()
        self._reader._check_uuid(row.record_id)
        self._reader._check_native_historic(
            row.pid, row.xid, row.database_oid, row.schema_oid,
            frame.native[3], frame.native[4],
        )
        self._reader._check_date(row.created_at, self._now())
        self._reader._check_governed(row)
        _text(row.creator_operation_id, self._limit)
        if (row.installation_id != frame.command.installation_ref
                or type(row.version) is not int or row.version < 1):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE")
        try:
            pair = (ConfigurationState(row.configuration_state),
                    StartupMode(row.operating_mode))
            validate_state_pair(*pair)
        except (ValueError, ModeValuesError):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if row.version == 1:
            if (_row_values(row) != frame.base_view["root"]
                    or row.origin != "R01_INITIAL"):
                raise CoreServiceError("ISSUE_INCONNUE")
        elif (row.origin != "MODE_TRANSITION" or row.predecessor_id is None
              or row.operation_receipt_id is None):
            raise CoreServiceError("ISSUE_INCONNUE")

    def _validate_history(self, frame: _Frame, *, read_alias: str) -> tuple[dict, dict]:
        self._stable()
        _text(read_alias, self._limit)
        if read_alias != frame.alias and read_alias != self._peer:
            raise CorePortError()
        model = _receipt_model()
        smodel = _snapshot_model()
        try:
            row = model.objects.using(read_alias).filter(record_id=frame.receipt_snapshot["record_id"]).first()
        except (DatabaseError, InterfaceError):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if row is None:
            raise CoreServiceError("ISSUE_INCONNUE")
        current = _row_values(row)
        if current != frame.receipt_snapshot:
            raise CoreServiceError("ISSUE_INCONNUE")
        self._receipt_shape(row, frame)
        try:
            snap_id = object.__getattribute__(row, "result_snapshot_id")
        except AttributeError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        try:
            snap = smodel.objects.using(read_alias).filter(record_id=snap_id).first()
        except (DatabaseError, InterfaceError):
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        if snap is None:
            raise CoreServiceError("ISSUE_INCONNUE")
        self._snapshot_shape(snap, frame)
        snap_vals = _row_values(snap)
        if (snap.version != row.result_version
                or snap.installation_id != row.installation_id):
            raise CoreServiceError("ISSUE_INCONNUE")
        if frame.result_snapshot is not None and snap_vals != frame.result_snapshot:
            raise CoreServiceError("ISSUE_INCONNUE")
        try:
            self._reader._check_uuid(snap.record_id)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        try:
            object.__getattribute__(self._reader, "_check_governed")(snap)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        now = self._now()
        try:
            object.__getattribute__(self._reader, "_check_date")(object.__getattribute__(snap, "created_at"), now)
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        try:
            object.__getattribute__(self._reader, "_check_native_historic")(object.__getattribute__(snap, "pid"), object.__getattribute__(snap, "xid"), object.__getattribute__(snap, "database_oid"), object.__getattribute__(snap, "schema_oid"), frame.native[3], frame.native[4])
        except CorePortError:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
        result_kind = object.__getattribute__(row, "result_kind")
        if result_kind == "NEW_SNAPSHOT":
            if snap_vals["version"] != object.__getattribute__(row, "expected_version") + 1:
                raise CoreServiceError("ISSUE_INCONNUE")
            if object.__getattribute__(snap, "operation_receipt_id") != object.__getattribute__(row, "record_id"):
                raise CoreServiceError("ISSUE_INCONNUE")
            if (snap_vals["pid"], snap_vals["xid"], snap_vals["database_oid"], snap_vals["schema_oid"]) != (current["pid"], current["xid"], current["database_oid"], current["schema_oid"]):
                raise CoreServiceError("ISSUE_INCONNUE")
            for name in ("metadata_profile_ref", "metadata_published_version", "metadata_owner_component", "metadata_source_of_truth", "governance_ref", "confidentiality", "personal", "retention_policy", "deletion_policy", "publication_ref", "catalog_version", "catalog_sha256"):
                if snap_vals[name] != current[name]:
                    raise CoreServiceError("ISSUE_INCONNUE")
            if not (object.__getattribute__(row, "started_at") <= object.__getattribute__(snap, "created_at") <= object.__getattribute__(row, "finished_at")):
                raise CoreServiceError("ISSUE_INCONNUE")
            if object.__getattribute__(snap, "creator_operation_id") != object.__getattribute__(row, "operation_id"):
                raise CoreServiceError("ISSUE_INCONNUE")
        elif result_kind == "NO_CHANGE":
            if smodel.objects.using(read_alias).filter(operation_receipt_id=row.record_id).exists():
                raise CoreServiceError("ISSUE_INCONNUE")
            if snap_vals["version"] != object.__getattribute__(row, "expected_version") or snap_vals["version"] != object.__getattribute__(row, "result_version"):
                raise CoreServiceError("ISSUE_INCONNUE")
            if not (object.__getattribute__(snap, "created_at") <= object.__getattribute__(row, "started_at")):
                raise CoreServiceError("ISSUE_INCONNUE")
            try:
                snap_pair = (ConfigurationState(snap_vals["configuration_state"]), StartupMode(snap_vals["operating_mode"]))
                if transition_state(snap_pair[0], snap_pair[1], frame.command.kind) != snap_pair:
                    raise CoreServiceError("ISSUE_INCONNUE")
            except (ValueError, ModeValuesError):
                raise CoreServiceError("ISSUE_INCONNUE") from None
        else:
            raise CoreServiceError("ISSUE_INCONNUE")
        if snap_vals["version"] == 1:
            if object.__getattribute__(snap, "origin") != "R01_INITIAL":
                raise CoreServiceError("ISSUE_INCONNUE")
            if frame.base_view["root"] != {k: snap_vals[k] for k in frame.base_view["root"].keys()}:
                raise CoreServiceError("ISSUE_INCONNUE")
        else:
            try:
                pred = smodel.objects.using(read_alias).filter(record_id=object.__getattribute__(snap, "predecessor_id")).first()
                creator = model.objects.using(read_alias).filter(record_id=object.__getattribute__(snap, "operation_receipt_id")).first()
            except (DatabaseError, InterfaceError):
                raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from None
            if pred is None or creator is None:
                raise CoreServiceError("ISSUE_INCONNUE")
            self._snapshot_shape(pred, frame)
            pred_vals = _row_values(pred)
            creator_vals = _row_values(creator)
            if pred_vals["version"] != snap_vals["version"] - 1 or str(pred_vals["installation_id"]) != str(snap_vals["installation_id"]):
                raise CoreServiceError("ISSUE_INCONNUE")
            if creator_vals["status"] != "SUCCEEDED" or creator_vals["result_kind"] != "NEW_SNAPSHOT":
                raise CoreServiceError("ISSUE_INCONNUE")
            if creator_vals["result_snapshot_id"] != snap_vals["record_id"] or creator_vals["result_version"] != snap_vals["version"]:
                raise CoreServiceError("ISSUE_INCONNUE")
            if creator_vals["operation_id"] != snap_vals["creator_operation_id"]:
                raise CoreServiceError("ISSUE_INCONNUE")
            if (creator_vals["pid"], creator_vals["xid"], creator_vals["database_oid"], creator_vals["schema_oid"]) != (snap_vals["pid"], snap_vals["xid"], snap_vals["database_oid"], snap_vals["schema_oid"]):
                raise CoreServiceError("ISSUE_INCONNUE")
            for name in ("metadata_profile_ref", "metadata_published_version", "metadata_owner_component", "metadata_source_of_truth", "governance_ref", "confidentiality", "personal", "retention_policy", "deletion_policy", "publication_ref", "catalog_version", "catalog_sha256"):
                if creator_vals[name] != snap_vals[name]:
                    raise CoreServiceError("ISSUE_INCONNUE")
            if creator_vals["expected_version"] != pred_vals["version"]:
                raise CoreServiceError("ISSUE_INCONNUE")
            try:
                creator_kind = ModeOperationKind(creator_vals["kind"])
                pred_pair = (ConfigurationState(pred_vals["configuration_state"]), StartupMode(pred_vals["operating_mode"]))
                snap_pair = (ConfigurationState(snap_vals["configuration_state"]), StartupMode(snap_vals["operating_mode"]))
                if transition_state(pred_pair[0], pred_pair[1], creator_kind) != snap_pair or snap_pair == pred_pair:
                    raise CoreServiceError("ISSUE_INCONNUE")
            except (ValueError, ModeValuesError):
                raise CoreServiceError("ISSUE_INCONNUE") from None
            self._receipt_shape(creator, frame)
            if (creator.installation_id != snap.installation_id
                    or creator.governance_status != snap.governance_status
                    or not creator.started_at <= snap.created_at <= creator.finished_at):
                raise CoreServiceError("ISSUE_INCONNUE")
        return (current, snap_vals)

    def _frame(self, proof: TransactionProof, *, live: bool = True,
               allow_phases: tuple[str, ...] = ("CHECK", "APPLIED", "RESULT", "RESTORED")) -> _Frame:
        self._stable()
        if type(live) is not bool or type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        for stage in proof.staged:
            stage.__post_init__()
            if (stage.operation_id != proof.operation_id or stage.alias != proof.alias
                    or stage.transaction_token != proof.transaction_token
                    or stage.context != proof.context):
                _fail()
        matches = [f for f in self._frames if
                   (f.alias, f.operation_id, f.token, f.context) ==
                   (proof.alias, proof.operation_id, proof.transaction_token, proof.context)]
        if len(matches) != 1:
            _fail()
        frame = matches[0]
        if frame.phase not in allow_phases:
            _fail()
        now = self._now()
        if (type(proof.prepared_at) is not dt.datetime
                or proof.prepared_at.tzinfo is not dt.timezone.utc
                or not frame.started_at <= proof.prepared_at <= now):
            _fail()
        owned = tuple(s for s in proof.staged if s.staged_kind.startswith("c08-modes:"))
        expected = ((frame.check,) if frame.result_stage is None
                    else (frame.check, frame.result_stage))
        if owned != expected:
            _fail()
        if live:
            native = _native_context(frame.alias)
            if native[0] is not frame.native[0] or native[1:] != frame.native[1:]:
                _fail()
            if transaction_identity(frame.alias) != frame.pin:
                _fail()
        return frame

    def _same_row(self, alias, model, expected):
        if expected is None:
            return None
        row = model.objects.using(alias).filter(
            pk=expected[model._meta.pk.attname]).first()
        if row is None or _row_values(row) != expected:
            _fail("ISSUE_INCONNUE")
        return row

    def _base_unchanged(self, frame):
        for role, model in (
            ("parent", _parent_model()), ("root", _snapshot_model()),
            ("last", _snapshot_model()), ("predecessor", _snapshot_model()),
            ("receipt", _receipt_model()),
        ):
            self._same_row(frame.alias, model, frame.base_view[role])

    def _eligibility(self, frame):
        self._stable()
        try:
            marker = read_installation_marker(self._reader._marker)
        except MarkerInvalid:
            raise CorePortError() from None
        parent = frame.base_view["parent"]
        if (marker != frame.marker_snapshot
                or marker.installation_ref != frame.command.installation_ref
                or marker.result_ref != parent["result_ref"]
                or marker.result_version != parent["result_version"]):
            _fail("ISSUE_INCONNUE")
        if frame.phase == "RESTORED":
            self._base_unchanged(frame)
            return
        changed_pending = (
            frame.phase == "APPLIED" and frame.applied_result is not None
            and frame.applied_result.version == frame.command.expected_version + 1
        )
        if changed_pending:
            self._base_unchanged(frame)
            if frame.result_snapshot is None:
                _fail()
            self._same_row(frame.alias, _snapshot_model(), frame.result_snapshot)
            last = _snapshot_model().objects.using(frame.alias).filter(
                installation_id=frame.command.installation_ref).order_by("-version").first()
            if last is None or _row_values(last) != frame.result_snapshot:
                _fail("ISSUE_INCONNUE")
            return
        _, view = self._reader._load_all(
            frame.alias, frame.native[3], frame.native[4], self._now())
        expected = frame.base_view
        if (frame.phase == "RESULT" and frame.fresh
                and frame.receipt_snapshot["result_kind"] == "NEW_SNAPSHOT"):
            expected = {
                "parent": frame.base_view["parent"], "root": frame.base_view["root"],
                "last": frame.result_snapshot, "predecessor": frame.base_view["last"],
                "receipt": frame.receipt_snapshot,
            }
        if view != expected:
            _fail("ISSUE_INCONNUE")

    def verify_staged(self, proof: TransactionProof) -> None:
        frame = self._frame(proof)
        self._eligibility(frame)
        self._same_row(frame.alias, _receipt_model(), frame.receipt_snapshot)
        if frame.phase in ("RESULT", "RESTORED") or not frame.fresh:
            self._validate_history(frame, read_alias=frame.alias)
        elif frame.receipt_snapshot["status"] != "IN_PROGRESS":
            _fail()
        if (frame.decision.decision_id != self._envelope.request.decision_id
                or frame.decision.effect is not Effect.ALLOW):
            _fail()

    def restore_confirmed(self, proof: TransactionProof) -> CoreMutationResult | None:
        frame = self._frame(proof, allow_phases=("CHECK",))
        self.verify_staged(proof)
        if frame.fresh:
            return None
        receipt, snapshot = self._validate_history(frame, read_alias=frame.alias)
        result = CoreMutationResult(
            receipt["operation_id"], receipt["result_ref"], receipt["result_version"],
            DataPersistenceState(receipt["result_persistence_state"]),
            receipt["result_correlation_id"],
        )
        frame.result_snapshot = snapshot
        frame.phase = "RESTORED"
        return result

    def report_conflict(self, proof: TransactionProof) -> str:
        self.verify_staged(proof)
        _fail("IDEMPOTENCE_AUCUN_CONFLIT")

    def apply_transition(self, ctx: MutationContext) -> AppliedMutation:
        self._stable()
        if type(ctx) is not MutationContext:
            _fail()
        ctx.__post_init__()
        if (ctx.envelope != self._envelope or ctx.alias != self._alias
                or ctx.ports.idempotence is not self
                or ctx.ports.decider is not self._decider
                or ctx.ports.clock is not self._clock
                or ctx.ports.governance is not self._governance):
            _fail()
        frame = self._frame(ctx.proof(), allow_phases=("CHECK",))
        if not frame.fresh or len(self._frames) != 1:
            _fail()
        self.verify_staged(ctx.proof())
        decision = ctx.decision
        now = self._now()
        if (type(decision) is not Decision or decision.effect is not Effect.ALLOW
                or decision.reason_code != "ALLOWED"
                or decision.decision_id != frame.decision.decision_id
                or decision.policy_version != frame.decision.policy_version
                or not decision.evaluated_at <= now < decision.expires_at):
            _fail()
        waived = frame.governance_status == "WAIVED"
        if ctx.governance_waived is not waived:
            _fail()
        if waived:
            if ctx.attestation is not None or any(
                    value is not None for value in frame.mode_metadata.values()):
                _fail()
        else:
            if self._governance is None or ctx.attestation is None:
                _fail()
            mode, _ = self._governance._profiles()
            if ((mode.publication_ref, mode.catalog_version, mode.raw_sha256)
                    != frame.mode_publication
                    or ctx.attestation.profile != mode.profile
                    or ctx.attestation.published_version != mode.published_version
                    or mode.profile.owner_component != "pixs.backend"
                    or ctx.attestation.context != frame.context):
                _fail()
        classification = ctx.classification()
        expected_classification = {
            name: frame.mode_metadata[name]
            for name in ("governance_ref", "confidentiality", "personal")
        }
        if classification != expected_classification:
            _fail()
        last = frame.base_view["last"]
        if last["version"] != frame.command.expected_version:
            _fail("IDEMPOTENCE_CONFLIT")
        try:
            before = (ConfigurationState(last["configuration_state"]),
                      StartupMode(last["operating_mode"]))
            after = transition_state(*before, frame.command.kind)
        except (ValueError, ModeValuesError):
            _fail()
        snapshot = copy.deepcopy(last)
        if after != before:
            if last["version"] >= 2 ** 63 - 1:
                _fail("C08_MODE_VERSION_EPUISEE")
            identifier = generate_uuid7()
            self._reader._check_uuid(identifier)
            created_at = self._now()
            if created_at < frame.started_at:
                _fail()
            values = dict(
                record_id=identifier, installation_id=frame.command.installation_ref,
                version=last["version"] + 1, configuration_state=after[0].value,
                operating_mode=after[1].value, origin="MODE_TRANSITION",
                predecessor_id=last["record_id"],
                operation_receipt_id=frame.receipt_snapshot["record_id"],
                creator_operation_id=frame.operation_id, pid=frame.native[1],
                xid=frame.native[2], database_oid=frame.native[3],
                schema_oid=frame.native[4], created_at=created_at,
                governance_status=frame.governance_status, **frame.mode_metadata,
            )
            created = _snapshot_model().objects.using(frame.alias).create(**values)
            row = _snapshot_model().objects.using(frame.alias).filter(
                record_id=created.record_id).first()
            if row is None:
                _fail("ISSUE_INCONNUE")
            self._snapshot_shape(row, frame)
            snapshot = _row_values(row)
            for name, value in values.items():
                if snapshot[name] != value:
                    _fail("ISSUE_INCONNUE")
        else:
            if _snapshot_model().objects.using(frame.alias).filter(
                    operation_receipt_id=frame.receipt_snapshot["record_id"]).exists():
                _fail("ISSUE_INCONNUE")
        applied = AppliedMutation(
            result_ref=mode_resource_ref(frame.command, max_ref_len=self._limit),
            version=snapshot["version"], persistence_state=DataPersistenceState.ACTIVE,
            **classification,
        )
        frame.result_snapshot = snapshot
        frame.applied_result = applied
        frame.phase = "APPLIED"
        return applied

    def stage_result(self, proof: TransactionProof, *, result: CoreMutationResult) -> StagedRef:
        frame = self._frame(proof, allow_phases=("APPLIED",))
        if (not frame.fresh or type(frame.applied_result) is not AppliedMutation
                or frame.result_snapshot is None or type(result) is not CoreMutationResult):
            _fail()
        result.__post_init__()
        if (result.operation_id != frame.operation_id
                or result.result_ref != frame.applied_result.result_ref
                or result.version != frame.applied_result.version
                or result.persistence_state is not DataPersistenceState.ACTIVE
                or result.correlation_id != self._envelope.correlation_id):
            _fail()
        if result.version == frame.command.expected_version:
            result_kind = "NO_CHANGE"
        elif result.version == frame.command.expected_version + 1:
            result_kind = "NEW_SNAPSHOT"
        else:
            _fail()
        self._eligibility(frame)
        self._same_row(frame.alias, _receipt_model(), frame.receipt_snapshot)
        self._same_row(frame.alias, _snapshot_model(), frame.result_snapshot)
        finished = self._now()
        if finished < frame.started_at:
            _fail()
        updates = dict(
            status="SUCCEEDED", result_snapshot_id=frame.result_snapshot["record_id"],
            result_version=result.version, result_ref=result.result_ref,
            result_kind=result_kind, result_persistence_state=result.persistence_state.value,
            result_correlation_id=result.correlation_id, finished_at=finished,
        )
        expected = copy.deepcopy(frame.receipt_snapshot)
        expected.update(updates)
        changed = _receipt_model().objects.using(frame.alias).filter(
            record_id=expected["record_id"], status="IN_PROGRESS",
            operation_id=frame.operation_id, transaction_token=frame.token,
        ).update(**updates)
        if changed != 1:
            _fail("VERSION_DIVERGENTE")
        self._same_row(frame.alias, _receipt_model(), expected)
        frame.receipt_snapshot = expected
        self._validate_history(frame, read_alias=frame.alias)
        frame.result_stage = StagedRef(
            frame.operation_id, frame.alias, frame.token, frame.context, _RESULT)
        frame.phase = "RESULT"
        return frame.result_stage

    def reconcile_unknown(self, proof: TransactionProof) -> str:
        frame = self._frame(proof, live=False, allow_phases=("RESULT",))
        if (len(self._frames) != 1 or self._attempts != 1 or self._reconciled
                or not frame.fresh or frame.result_stage is None):
            _fail("ISSUE_INCONNUE")
        main, peer = self._reader._aliases()
        if main.in_atomic_block or peer.in_atomic_block:
            _fail("ISSUE_INCONNUE")
        had_peer = peer.connection is not None
        try:
            peer.ensure_connection()
            if (not peer.get_autocommit() or peer.needs_rollback
                    or peer.closed_in_transaction or peer.connection.autocommit is not True
                    or peer.connection is frame.native[0]
                    or (main.connection is not None and peer.connection is main.connection)):
                _fail("ISSUE_INCONNUE")
            with transaction.atomic(using=self._peer, durable=True):
                with peer.cursor() as cursor:
                    cursor.execute("SET TRANSACTION READ ONLY")
                observed = _native_context(self._peer)
                if (observed[0] is frame.native[0] or observed[1] == frame.native[1]
                        or observed[3:5] != frame.native[3:5]):
                    _fail("ISSUE_INCONNUE")
                self._validate_history(frame, read_alias=self._peer)
        except (CoreServiceError, CorePortError, CoreInputInvalid, PortError,
                DatabaseError, InterfaceError) as error:
            raise CoreServiceError("ISSUE_INCONNUE") from error
        finally:
            if not had_peer and peer.connection is not None:
                try:
                    peer.close()
                except (DatabaseError, InterfaceError) as error:
                    raise CoreServiceError("ISSUE_INCONNUE") from error
        self._reconciled = True
        return "SUCCEEDED"
