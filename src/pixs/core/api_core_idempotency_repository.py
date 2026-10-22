"""Idempotence durable Core : transaction propriétaire et réconciliation sans rejeu.

Une instance appartient à une invocation. Un second cadre n'est admis qu'après
confirmation sur une connexion dédiée, pour le chemin Core restore_only.
Les profils injectés sont structurels ; ils ne qualifient pas le runtime C10.
"""
from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import DatabaseError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.core.api_core_idempotency_record import CoreApiIdempotencyRecord
from pixs.core.api_core_idempotency_values import (
    ApiCoreIdempotencyConfig, ApiCoreIdempotencyEntry,
    ApiCoreIdempotencyProofInvalid, resolve_idempotency_key,
    validate_idempotency_entry,
)
from pixs.core.api_core_serializer_v1 import API_CORE_SERIALIZER_VERSION
from pixs.core.authz.ports import PortError, Request
from pixs.core.dto import CoreInputInvalid, CoreMutationResult
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7, generate_uuid7
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import CoreServiceError, utc_now
from pixs.kernel.data_governance_profile import (
    DataGovernanceProfile, validate_data_governance_profile,
)
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = ["CoreApiIdempotencyRepository"]

_CHECK = "idempotence:check-v1"
_RESULT = "idempotence:result-v1"


def _fail(code="IDEMPOTENCE_PREUVE_INVALIDE"):
    raise CoreServiceError(code)


def _text(value):
    if type(value) is not str or not value or chr(0) in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeError as error:
        raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error


def _connection(alias):
    _text(alias)
    try:
        conn = connections[alias]
    except ConnectionDoesNotExist as error:
        raise CoreServiceError("ALIAS_INCONNU") from error
    if conn.vendor != "postgresql":
        _fail("MOTEUR_NON_PG_REFUSE")
    return conn


def _native(alias):
    conn = _connection(alias)
    pin = transaction_identity(alias)
    if (not conn.in_atomic_block or conn.needs_rollback
            or conn.connection is None or conn.closed_in_transaction):
        _fail("HORS_TRANSACTION")
    return pin, conn.connection, tuple(conn.savepoint_ids)


def _same_native(actual, expected):
    return (actual[0] == expected[0] and actual[1] is expected[1]
            and actual[2] == expected[2])


def _normalize(value):
    if type(value) is not datetime.datetime or value.tzinfo is None:
        _fail()
    return value.astimezone(datetime.timezone.utc)


def _result(row):
    if row["state"] != "SUCCEEDED":
        return None
    try:
        return CoreMutationResult(
            row["result_operation_id"], row["result_ref"], row["result_version"],
            DataPersistenceState(row["result_persistence_state"]),
            row["result_correlation_id"],
        )
    except (CoreInputInvalid, ValueError) as error:
        raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error


@dataclass(slots=True)
class _Frame:
    alias: str
    operation_id: str
    token: str
    context: ScopeContext
    key: object
    native: tuple
    snapshot: dict
    check: StagedRef
    started_at: datetime.datetime
    fresh: bool
    result_ref: StagedRef | None = None


class CoreApiIdempotencyRepository:
    """Participant par invocation, sans transaction durable imbriquée."""

    def __init__(self, *, alias: str, peer_alias: str,
                 config: ApiCoreIdempotencyConfig, clock,
                 request: Request, operation_id: str,
                 profile: DataGovernanceProfile | None, decider=None):
        from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider

        _text(alias)
        _text(peer_alias)
        _text(operation_id)
        if alias == peer_alias:
            _fail("ALIAS_DIVERGENT")
        if type(config) is not ApiCoreIdempotencyConfig or type(request) is not Request:
            _fail()
        try:
            config.__post_init__()
            request.__post_init__()
            validate_structure(request.context)
        except (ApiCoreIdempotencyProofInvalid, PortError, ScopeStructureError, AttributeError) as error:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error
        if not callable(getattr(clock, "now", None)):
            _fail("HORLOGE_ILLISIBLE")
        if profile is None:
            if type(decider) is not RuntimeAuthorizationDecider:
                _fail("GOUVERNANCE_ABSENTE")
            try:
                bound_request = object.__getattribute__(decider, "_request")
                bound_operation = object.__getattribute__(decider, "_operation_id")
            except AttributeError as error:
                raise CoreServiceError("GOUVERNANCE_ABSENTE") from error
            if bound_request != request or bound_operation != operation_id:
                _fail("GOUVERNANCE_ABSENTE")
            classification = None
        else:
            if (type(profile) is not DataGovernanceProfile
                    or validate_data_governance_profile(profile)
                    or profile.owner_component != "pixs.core"):
                _fail("GOUVERNANCE_INVALIDE")
            classification = {
                "governance_ref": profile.data_asset_id,
                "confidentiality": profile.confidentiality.value,
                "personal": profile.personal_data.value,
            }
        self._alias = alias
        self._peer_alias = peer_alias
        self._config = config
        self._clock = clock
        self._request = request
        self._operation_id = operation_id
        self._classification = classification
        self._decider = decider
        self._frames: list[_Frame] = []
        self._attempts = 0
        self._reconciled = False

    def _snapshot(self, row):
        if type(row) is not CoreApiIdempotencyRecord:
            _fail()
        data = {f.attname: getattr(row, f.attname) for f in row._meta.concrete_fields}
        try:
            check_uuid7(data["record_id"])
            for name in ("created_at", "updated_at", "completed_at", "expires_at"):
                if data[name] is not None:
                    data[name] = _normalize(data[name])
            # clean() est local ; aucune validation ORM des contraintes/uniques.
            CoreApiIdempotencyRecord(**data).clean()
            context = ScopeContext(ScopeType(data["scope_type"]),
                                   data["context_tenant_id"], data["context_scope_id"])
            key = resolve_idempotency_key(
                context=context, subject_id=data["subject_id"],
                command_type=data["command_type"], idempotency_key=data["idempotency_key"],
                config=self._config,
            )
            entry = ApiCoreIdempotencyEntry(
                key, data["content_sha256"], data["serializer_version"], context,
                data["state"], _result(data), data["created_at"], data["completed_at"],
                data["expires_at"], data["revision"],
            )
            validate_idempotency_entry(entry, config=self._config)
        except (ValidationError, Uuid7Error, ApiCoreIdempotencyProofInvalid,
                CoreInputInvalid, AttributeError) as error:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error
        if (data["persistence_state"] != "ACTIVE"
                or data["retention_state"] != "RETAINED"):
            _fail()
        return data

    def _classification_now(self, alias, operation_id):
        if self._classification is not None:
            return dict(self._classification)
        try:
            decision = self._decider.revalidate_under_locks(
                self._request, alias=alias, operation_id=operation_id)
            waived = self._decider.governance_waived(
                self._request, decision, alias=alias, operation_id=operation_id)
        except (PortError, CorePortError, CoreInputInvalid) as error:
            raise CoreServiceError("GOUVERNANCE_ABSENTE") from error
        if waived is not True:
            _fail("GOUVERNANCE_ABSENTE")
        return {"governance_ref": None, "confidentiality": None, "personal": None}

    def _lock(self, key, native):
        parts = [native[0][2], native[0][3], key.namespace, key.tenant_id,
                 key.subject_id, key.command_type, key.idempotency_key]
        canonical = json.dumps(parts, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        lock_id = int.from_bytes(hashlib.sha256(canonical).digest()[:8], "big", signed=True)
        with connections[self._alias].cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", [lock_id])

    def check_or_stage(self, *, alias: str, operation_id: str,
                       transaction_token: str, context: ScopeContext,
                       subject_id: str, command_type: str, idempotency_key: str,
                       content_sha256: str, serializer_version: str) -> StagedRef:
        for value in (alias, operation_id, transaction_token, subject_id):
            _text(value)
        if type(context) is not ScopeContext:
            _fail()
        try:
            validate_structure(context)
        except (ScopeStructureError, AttributeError) as error:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error
        if (alias != self._alias or operation_id != self._operation_id
                or context != self._request.context or subject_id != self._request.subject_id):
            _fail()
        if self._attempts != 0 and not (
                self._attempts == 1 and self._reconciled and len(self._frames) == 1):
            _fail("IDEMPOTENCE_CADRE_EPUISE")
        if (type(content_sha256) is not str or len(content_sha256) != 64
                or any(c not in "0123456789abcdef" for c in content_sha256)
                or type(serializer_version) is not str
                or serializer_version != API_CORE_SERIALIZER_VERSION):
            _fail()
        try:
            key = resolve_idempotency_key(
                context=context, subject_id=subject_id, command_type=command_type,
                idempotency_key=idempotency_key, config=self._config)
        except ApiCoreIdempotencyProofInvalid as error:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error
        self._attempts += 1
        native = _native(alias)
        started = utc_now(self._clock)
        classification = self._classification_now(alias, operation_id)
        self._lock(key, native)
        if not _same_native(_native(alias), native):
            _fail()
        if self._frames and (
                transaction_token == self._frames[0].token
                or native[0] == self._frames[0].native[0]):
            _fail()
        query = CoreApiIdempotencyRecord.objects.using(alias)
        row = query.filter(
            namespace=key.namespace, tenant_id=key.tenant_id,
            subject_id=key.subject_id, command_type=key.command_type,
            idempotency_key=key.idempotency_key,
        ).first()
        fresh = row is None
        if fresh:
            if self._frames:
                _fail("ISSUE_INCONNUE")
            try:
                expires = started + datetime.timedelta(seconds=self._config.replay_window_seconds)
            except OverflowError as error:
                raise CoreServiceError("EXPIRATION_INVALIDE") from error
            with connections[alias].cursor() as cursor:
                cursor.execute("SELECT pg_current_xact_id()::text")
                staged_xid = cursor.fetchone()[0]
            row = CoreApiIdempotencyRecord(
                record_id=generate_uuid7(), namespace=key.namespace, tenant_id=key.tenant_id,
                subject_id=key.subject_id, command_type=key.command_type,
                idempotency_key=key.idempotency_key, scope_type=context.scope_type.value,
                context_tenant_id=context.tenant_id, context_scope_id=context.scope_id,
                content_sha256=content_sha256, serializer_version=serializer_version,
                state="IN_PROGRESS", created_at=started, updated_at=started,
                expires_at=expires, replay_window_seconds=self._config.replay_window_seconds,
                revision=1, version=1, operation_id=operation_id, db_alias=alias,
                transaction_token=transaction_token, staged_xid=staged_xid, **classification,
            )
            self._snapshot(row)
            row.save(using=alias, force_insert=True)
            row = query.get(record_id=row.record_id)
        snapshot = self._snapshot(row)
        if (snapshot["content_sha256"] != content_sha256
                or snapshot["serializer_version"] != serializer_version
                or (snapshot["scope_type"], snapshot["context_tenant_id"],
                    snapshot["context_scope_id"]) !=
                   (context.scope_type.value, context.tenant_id, context.scope_id)):
            _fail("IDEMPOTENCE_CONFLIT")
        if not fresh and snapshot["state"] != "SUCCEEDED":
            _fail("ISSUE_INCONNUE")
        if self._frames and snapshot != self._frames[0].snapshot:
            _fail("ISSUE_INCONNUE")
        if not _same_native(_native(alias), native):
            _fail()
        ref = StagedRef(operation_id, alias, transaction_token, context, _CHECK)
        frame = _Frame(alias, operation_id, transaction_token, context, key,
                       native, snapshot, ref, started, fresh)
        self._frames.append(frame)
        return ref

    def _frame(self, proof, *, live=True):
        if type(proof) is not TransactionProof:
            _fail()
        try:
            proof.__post_init__()
            for ref in proof.staged:
                StagedRef.__post_init__(ref)
        except (CorePortError, AttributeError) as error:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error
        found = [f for f in self._frames if (
            proof.alias, proof.operation_id, proof.transaction_token, proof.context
        ) == (f.alias, f.operation_id, f.token, f.context)]
        if len(found) != 1:
            _fail()
        frame = found[0]
        own = tuple(s for s in proof.staged if s.staged_kind.startswith("idempotence:"))
        wanted = (frame.check,) if frame.result_ref is None else (frame.check, frame.result_ref)
        if len(own) != len(wanted) or any(
                sum(s is ref for s in own) != 1 for ref in wanted):
            _fail()
        if not frame.started_at <= proof.prepared_at <= utc_now(self._clock):
            _fail()
        if live:
            actual = _native(frame.alias)
            if (actual[0] != frame.native[0] or actual[1] is not frame.native[1]
                    or actual[2] != frame.native[2]):
                _fail()
        return frame

    def _read(self, frame, alias):
        row = CoreApiIdempotencyRecord.objects.using(alias).filter(
            record_id=frame.snapshot["record_id"],
            namespace=frame.key.namespace, tenant_id=frame.key.tenant_id,
            subject_id=frame.key.subject_id, command_type=frame.key.command_type,
            idempotency_key=frame.key.idempotency_key,
        ).first()
        if row is None or self._snapshot(row) != frame.snapshot:
            _fail("ISSUE_INCONNUE")
        return row

    def verify_staged(self, proof: TransactionProof) -> None:
        frame = self._frame(proof)
        self._read(frame, frame.alias)

    def restore_confirmed(self, proof: TransactionProof) -> CoreMutationResult | None:
        frame = self._frame(proof)
        self._read(frame, frame.alias)
        if frame.fresh:
            if frame.result_ref is not None:
                _fail()
            return None
        return _result(frame.snapshot)

    def stage_result(self, proof: TransactionProof, *, result: CoreMutationResult) -> StagedRef:
        frame = self._frame(proof)
        if not frame.fresh or frame.result_ref is not None or type(result) is not CoreMutationResult:
            _fail()
        try:
            result.__post_init__()
        except (CoreInputInvalid, AttributeError) as error:
            raise CoreServiceError("IDEMPOTENCE_PREUVE_INVALIDE") from error
        if result.operation_id != frame.operation_id:
            _fail()
        self._read(frame, frame.alias)
        now = utc_now(self._clock)
        if now < frame.snapshot["created_at"]:
            _fail("HORLOGE_NON_MONOTONE")
        try:
            expires = now + datetime.timedelta(seconds=self._config.replay_window_seconds)
        except OverflowError as error:
            raise CoreServiceError("EXPIRATION_INVALIDE") from error
        changes = {
            "state": "SUCCEEDED", "result_operation_id": result.operation_id,
            "result_ref": result.result_ref, "result_version": result.version,
            "result_persistence_state": result.persistence_state.value,
            "result_correlation_id": result.correlation_id,
            "completed_at": now, "updated_at": now,
            "expires_at": max(expires, frame.snapshot["expires_at"]),
            "version": frame.snapshot["version"] + 1, "revision": frame.snapshot["revision"] + 1,
        }
        if not _same_native(_native(frame.alias), frame.native):
            _fail()
        changed = CoreApiIdempotencyRecord.objects.using(frame.alias).filter(
            record_id=frame.snapshot["record_id"], state="IN_PROGRESS",
            version=frame.snapshot["version"], revision=frame.snapshot["revision"],
            operation_id=frame.operation_id, transaction_token=frame.token,
            staged_xid=frame.snapshot["staged_xid"],
        ).update(**changes)
        if changed != 1:
            _fail("VERSION_DIVERGENTE")
        frame.snapshot = dict(frame.snapshot, **changes)
        self._read(frame, frame.alias)
        frame.result_ref = StagedRef(frame.operation_id, frame.alias, frame.token,
                                    frame.context, _RESULT)
        return frame.result_ref

    def report_conflict(self, proof: TransactionProof) -> str:
        # Le conflit est levé à l'admission ; une preuve valide n'en fabrique pas.
        self.verify_staged(proof)
        _fail("IDEMPOTENCE_AUCUN_CONFLIT")

    def reconcile_unknown(self, proof: TransactionProof) -> str:
        frame = self._frame(proof, live=False)
        if (len(self._frames) != 1 or self._reconciled
                or frame.snapshot["state"] != "SUCCEEDED"):
            _fail("ISSUE_INCONNUE")
        owner = _connection(frame.alias)
        peer = _connection(self._peer_alias)
        if (owner.in_atomic_block or peer.in_atomic_block
                or (peer.connection is not None and peer.connection is frame.native[1])):
            _fail("ISSUE_INCONNUE")
        try:
            with transaction.atomic(using=self._peer_alias):
                current = _native(self._peer_alias)
                if (current[0][2:] != frame.native[0][2:]
                        or current[1] is frame.native[1]
                        or current[0][0] == frame.native[0][0]):
                    _fail("ISSUE_INCONNUE")
                self._read(frame, self._peer_alias)
        except (CoreServiceError, DatabaseError, InterfaceError) as error:
            raise CoreServiceError("ISSUE_INCONNUE") from error
        finally:
            try:
                peer.close()
            except (DatabaseError, InterfaceError) as error:
                raise CoreServiceError("ISSUE_INCONNUE") from error
        self._reconciled = True
        return "SUCCEEDED"
