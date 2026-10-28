"""Idempotence privée R01 C08, sans autorité d'installation.

Le participant conserve des faits transactionnels. Core/Auth/C04/C05/C10
restent responsables de leurs effets et autorisations. Cette source seule
ne compose pas le parcours INITIAL/REUSE et ne le qualifie pas.
"""
from __future__ import annotations

import copy
import datetime as dt
import os
import threading
from contextlib import contextmanager
from dataclasses import dataclass

from django.db import connections, transaction, DatabaseError, InterfaceError, IntegrityError
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.installation.result_writer import C08TransactionalResultWriter, _native_context
from pixs.core.dto import BootstrapActInput, CoreMutationResult
from pixs.core.persistence.uuid7 import generate_uuid7, check_uuid7, Uuid7Error
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.services_common import CoreServiceError, lock_scopes
from pixs.kernel.data_persistence_states import DataPersistenceState

__all__ = ["C08ActIdempotenceParticipant"]
_COMMAND = "pixs.core.bootstrap.apply:v1"
_CHECK = "c08-act-check"
_RESULT = "c08-act-result"
_RESULT_FIELDS = ("result_ref", "result_version", "result_kind", "result_persistence_state",
                  "result_correlation_id", "finished_at")
_METADATA = ("publication_ref", "catalog_version", "catalog_sha256", "metadata_profile_ref",
             "metadata_published_version", "metadata_owner_component", "metadata_source_of_truth",
             "governance_ref", "confidentiality", "personal", "retention_policy", "deletion_policy")


def _fail(code="IDEMPOTENCE_PREUVE_INVALIDE"):
    raise CoreServiceError(code)


def _model():
    from pixs.backend.c08_act_receipt_record import C08ActReceiptRecord
    return C08ActReceiptRecord


def _header_model():
    from pixs.backend.c08_installation_result_record import C08InstallationResultRecord
    return C08InstallationResultRecord


def _values(row):
    return {field.attname: copy.deepcopy(getattr(row, field.attname))
            for field in row._meta.concrete_fields}


@dataclass(repr=False)
class _Frame:
    alias: str
    token: str
    native: tuple
    check: StagedRef
    snapshot: dict
    fresh: bool
    phase: str = "CHECK"
    result_stage: StagedRef | None = None


class C08ActIdempotenceParticipant:
    def __init__(self, *, writer: C08TransactionalResultWriter, inspection_using: str):
        if type(writer) is not C08TransactionalResultWriter:
            raise CorePortError()
        writer._text(inspection_using)
        if inspection_using == writer._using:
            raise CorePortError()
        self._writer = writer
        self._inspection = inspection_using
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._frames = []
        self._attempts = 0
        self._reconciled = False
        self._aliases()
        self._bound()

    def _aliases(self):
        try:
            main = connections[self._writer._using]
            peer = connections[self._inspection]
        except ConnectionDoesNotExist:
            raise CorePortError() from None
        if (main is peer or main.vendor != "postgresql" or peer.vendor != "postgresql"
                or (main.connection is not None and peer.connection is main.connection)):
            raise CorePortError()
        for key in ("ENGINE", "NAME", "USER", "PASSWORD", "HOST", "PORT", "OPTIONS", "TIME_ZONE"):
            if main.settings_dict.get(key) != peer.settings_dict.get(key):
                raise CorePortError()
        return main, peer

    def _bound(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()
        plan, entry = self._writer._stable()
        act = self._writer._act
        spec = plan.target_spec
        reuse = act.closed_effects == ("REUSE_EXISTING",)
        version = spec.expected_binding_version if reuse else 1
        if type(version) is not int or version < 1 or self._writer._version != version:
            raise CorePortError()
        bound = dict(
            operation_id=act.operation_id, installation_id=act.installation_ref,
            operator_subject_ref=act.operator_subject_ref, operator_proof_ref=act.operator_proof_ref,
            command_type=_COMMAND, mode=act.mode, idempotency_key=act.idempotency_key,
            content_sha256=act.content_sha256, serializer_version=act.serializer_version,
            plan_version=act.plan_version, plan_sha256=self._writer._plan_digest,
            database_target_ref=plan.database_target_ref, authorization_ref=act.authorization_ref,
            target_identity_ref=act.target_identity_ref, target_tenant_ref=act.target_tenant_ref,
            closed_effects=list(act.closed_effects), confirmations=list(act.confirmations),
            correlation_id=act.correlation_id, causation_id=act.causation_id,
            expected_binding_version=spec.expected_binding_version,
            expected_identity_version=spec.expected_identity_version,
            expected_tenant_version=spec.expected_tenant_version,
            scope_type="PLATFORM", tenant_id=None, scope_id=None,
        )
        profile = entry.profile
        metadata = dict(
            governance_status="GOVERNED", publication_ref=entry.publication_ref,
            catalog_version=entry.catalog_version, catalog_sha256=entry.raw_sha256,
            metadata_profile_ref=self._writer._metadata.owner.config.binding.profile_ref,
            metadata_published_version=entry.published_version,
            metadata_owner_component=profile.owner_component,
            metadata_source_of_truth=profile.source_of_truth, governance_ref=profile.data_asset_id,
            confidentiality=profile.confidentiality.value, personal=profile.personal_data.value,
            retention_policy=profile.retention_policy, deletion_policy=profile.deletion_policy,
        )
        return bound, metadata, version, reuse

    def _shape(self, row, native, *, succeeded):
        bound, _metadata, version, reuse = self._bound()
        for key, value in bound.items():
            if row[key] != value:
                _fail("IDEMPOTENCE_CONFLIT")
        try:
            check_uuid7(row["record_id"])
        except (Uuid7Error, ValueError):
            _fail()
        if (type(row["pid"]) is not int or row["pid"] < 1
                or type(row["xid"]) is not str or not row["xid"].isdigit()
                or row["xid"] == "0"
                or type(row["database_oid"]) is not int or type(row["schema_oid"]) is not int
                or (row["database_oid"], row["schema_oid"]) != native[3:5]
                or type(row["started_at"]) is not dt.datetime
                or row["started_at"].tzinfo is not dt.timezone.utc
                or row["started_at"] > self._writer._now()
                or row["governance_status"] != "GOVERNED"
                or row["metadata_owner_component"] != "pixs.backend"):
            _fail()
        for key in ("transaction_token", *_METADATA):
            self._writer._text(row[key])
        if (len(row["catalog_sha256"]) != 64
                or any(char not in "0123456789abcdef" for char in row["catalog_sha256"])
                or row["confidentiality"] not in ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED")
                or row["personal"] not in ("NONE", "PERSONAL", "SENSITIVE_PERSONAL")):
            _fail()
        if not succeeded:
            if row["status"] != "IN_PROGRESS" or any(row[key] is not None for key in _RESULT_FIELDS):
                _fail()
            return
        if (row["status"] != "SUCCEEDED"
                or row["result_ref"] != "pixs.core.binding:" + bound["installation_id"]
                or type(row["result_version"]) is not int or row["result_version"] != version
                or row["result_kind"] != ("REUSE" if reuse else "INITIAL")
                or row["result_persistence_state"] != "ACTIVE"
                or row["result_correlation_id"] != row["correlation_id"]
                or type(row["finished_at"]) is not dt.datetime
                or row["finished_at"].tzinfo is not dt.timezone.utc
                or not row["started_at"] <= row["finished_at"] <= self._writer._now()):
            _fail()
        self._header(row, native)

    def _header(self, row, native):
        header = _header_model().objects.using(native[6]).filter(
            installation_ref=row["installation_id"]).first()
        if header is None:
            _fail("ISSUE_INCONNUE")
        value = _values(header)
        if (value["database_target_ref"] != row["database_target_ref"]
                or (value["database_oid"], value["schema_oid"]) != native[3:5]
                or value["result_ref"] != row["result_ref"]
                or type(value["prepared_at"]) is not dt.datetime
                or value["prepared_at"].tzinfo is not dt.timezone.utc):
            _fail("ISSUE_INCONNUE")
        if row["result_kind"] == "INITIAL":
            for key in ("operation_id", "plan_version", "plan_sha256", "content_sha256",
                        "serializer_version", "operator_subject_ref", "operator_proof_ref",
                        "authorization_ref", "target_identity_ref", "target_tenant_ref",
                        "closed_effects", "confirmations", "correlation_id", "causation_id",
                        "idempotency_key", "transaction_token", "pid", "xid", *_METADATA):
                if value[key] != row[key]:
                    _fail("ISSUE_INCONNUE")
            if not row["started_at"] <= value["prepared_at"] <= row["finished_at"]:
                _fail("ISSUE_INCONNUE")
        elif value["xid"] == row["xid"] or value["prepared_at"] > row["started_at"]:
            _fail("ISSUE_INCONNUE")

    def _native(self, alias):
        native = _native_context(alias)
        return (*native, alias)

    def _same_native(self, first, current):
        return first[6] == current[6] and self._writer._same_native(first[:6], current[:6])

    def _frame(self, proof, *, live=True):
        self._bound()
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        selected = [frame for frame in self._frames if frame.token == proof.transaction_token]
        if len(selected) != 1:
            _fail()
        frame = selected[0]
        act = self._writer._act
        if (proof.alias != frame.alias or proof.operation_id != act.operation_id
                or proof.context != act.context or proof.prepared_at > self._writer._now()
                or tuple(stage for stage in proof.staged if stage.staged_kind == _CHECK) != (frame.check,)):
            _fail()
        if live and not self._same_native(frame.native, self._native(frame.alias)):
            _fail()
        return frame

    def _read_frame(self, frame, alias):
        row = _model().objects.using(alias).filter(record_id=frame.snapshot["record_id"]).first()
        if row is None or _values(row) != frame.snapshot:
            _fail("ISSUE_INCONNUE")
        return row

    def check_or_stage(self, *, alias, operation_id, transaction_token, context,
                       subject_id, command_type, idempotency_key, content_sha256,
                       serializer_version):
        bound, metadata, _version, reuse = self._bound()
        for value in (alias, operation_id, transaction_token, subject_id, command_type,
                      idempotency_key, content_sha256, serializer_version):
            self._writer._text(value)
        act = self._writer._act
        if (alias != self._writer._using or context != act.context
                or operation_id != act.operation_id or subject_id != act.operator_subject_ref
                or command_type != _COMMAND or idempotency_key != act.idempotency_key
                or content_sha256 != act.content_sha256 or serializer_version != act.serializer_version):
            _fail("IDEMPOTENCE_CONFLIT")
        if self._attempts != 0 and not (self._attempts == 1 and self._reconciled):
            _fail("IDEMPOTENCE_CADRE_EPUISE")
        lock_scopes(alias, ("installation:" + act.installation_ref,))
        native = self._native(alias)
        if self._frames and (transaction_token == self._frames[0].token
                             or native[2] == self._frames[0].native[2]):
            _fail("IDEMPOTENCE_PREUVE_INVALIDE")
        query = _model().objects.using(alias).select_for_update()
        try:
            by_operation = query.filter(operation_id=operation_id).first()
            by_key = query.filter(installation_id=act.installation_ref,
                                  operator_subject_ref=subject_id, command_type=command_type,
                                  idempotency_key=idempotency_key).first()
            if by_operation is not None and by_key is not None and by_operation.pk == by_key.pk:
                row, fresh = by_operation, False
                value = _values(row)
                if value["xid"] == native[2]:
                    _fail("ISSUE_INCONNUE")
                self._shape(value, native, succeeded=True)
            elif by_operation is not None or by_key is not None:
                _fail("IDEMPOTENCE_CONFLIT")
            else:
                parent = _header_model().objects.using(alias).filter(
                    installation_ref=act.installation_ref).first()
                if reuse:
                    if parent is None:
                        _fail("LIAISON_ABSENTE")
                    if (parent.database_target_ref != bound["database_target_ref"]
                            or (parent.database_oid, parent.schema_oid) != native[3:5]
                            or parent.xid == native[2]):
                        _fail("ISSUE_INCONNUE")
                elif parent is not None:
                    _fail("INSTALLATION_EXISTANTE")
                identifier = generate_uuid7()
                check_uuid7(identifier)
                row = _model().objects.using(alias).create(
                    **bound, **metadata, record_id=identifier, transaction_token=transaction_token,
                    status="IN_PROGRESS", started_at=self._writer._now(), finished_at=None,
                    result_ref=None, result_version=None, result_kind=None,
                    result_persistence_state=None, result_correlation_id=None,
                    pid=native[1], xid=native[2], database_oid=native[3], schema_oid=native[4])
                fresh = True
        except IntegrityError:
            _fail("IDEMPOTENCE_CONFLIT")
        except (DatabaseError, InterfaceError, Uuid7Error):
            _fail()
        value = _values(row)
        self._shape(value, native, succeeded=not fresh)
        stage = StagedRef(operation_id, alias, transaction_token, context, _CHECK)
        self._frames.append(_Frame(alias, transaction_token, native, stage, value, fresh))
        self._attempts += 1
        return stage

    def verify_staged(self, proof):
        frame = self._frame(proof)
        self._read_frame(frame, frame.alias)
        self._shape(frame.snapshot, frame.native, succeeded=not frame.fresh or frame.phase != "CHECK")
        if frame.phase == "RESULT":
            if (frame.result_stage is None or
                    tuple(stage for stage in proof.staged if stage.staged_kind == _RESULT) != (frame.result_stage,)):
                _fail()
        elif any(stage.staged_kind == _RESULT for stage in proof.staged):
            _fail()

    def restore_confirmed(self, proof):
        frame = self._frame(proof)
        if frame.phase != "CHECK":
            _fail()
        self.verify_staged(proof)
        if frame.fresh:
            return None
        frame.phase = "RESTORED"
        row = frame.snapshot
        return CoreMutationResult(row["operation_id"], row["result_ref"], row["result_version"],
                                  DataPersistenceState.ACTIVE, row["result_correlation_id"])

    def stage_result(self, proof, *, result):
        frame = self._frame(proof)
        if not frame.fresh or frame.phase != "CHECK" or type(result) is not CoreMutationResult:
            _fail()
        result.__post_init__()
        self.verify_staged(proof)
        bound, _metadata, version, reuse = self._bound()
        if (result.operation_id != bound["operation_id"]
                or result.result_ref != "pixs.core.binding:" + bound["installation_id"]
                or result.version != version or result.persistence_state is not DataPersistenceState.ACTIVE
                or result.correlation_id != bound["correlation_id"]):
            _fail()
        finished = self._writer._now()
        if finished < frame.snapshot["started_at"]:
            _fail()
        changes = dict(status="SUCCEEDED", result_ref=result.result_ref, result_version=result.version,
                       result_kind="REUSE" if reuse else "INITIAL", result_persistence_state="ACTIVE",
                       result_correlation_id=result.correlation_id, finished_at=finished)
        try:
            count = _model().objects.using(frame.alias).filter(
                record_id=frame.snapshot["record_id"], status="IN_PROGRESS",
                transaction_token=frame.token).update(**changes)
        except (DatabaseError, InterfaceError):
            _fail()
        if count != 1:
            _fail("ISSUE_INCONNUE")
        expected = copy.deepcopy(frame.snapshot)
        expected.update(changes)
        frame.snapshot = expected
        frame.phase = "RESULT"
        frame.result_stage = StagedRef(proof.operation_id, proof.alias, proof.transaction_token,
                                       proof.context, _RESULT)
        self._read_frame(frame, frame.alias)
        self._shape(expected, frame.native, succeeded=True)
        return frame.result_stage

    def report_conflict(self, proof):
        self.verify_staged(proof)
        _fail("IDEMPOTENCE_CONFLIT")

    @contextmanager
    def _inspect(self):
        main, peer = self._aliases()
        if main.in_atomic_block or peer.in_atomic_block:
            _fail("ISSUE_INCONNUE")
        had_peer = peer.connection is not None
        try:
            peer.ensure_connection()
            if (not peer.get_autocommit() or peer.needs_rollback or peer.closed_in_transaction
                    or peer.connection is main.connection):
                _fail("ISSUE_INCONNUE")
            with transaction.atomic(using=self._inspection, durable=True):
                with peer.cursor() as cursor:
                    cursor.execute("SET TRANSACTION READ ONLY")
                lock_scopes(self._inspection, ("installation:" + self._writer._act.installation_ref,),
                            shared=True)
                yield self._native(self._inspection)
        finally:
            if not had_peer and peer.connection is not None:
                peer.close()

    def inspect_confirmed(self, act):
        if type(act) is not BootstrapActInput or act != self._writer._act:
            raise CorePortError()
        self._bound()
        main, _peer = self._aliases()
        if main.in_atomic_block:
            native = self._native(self._writer._using)
            row = _model().objects.using(self._writer._using).filter(operation_id=act.operation_id).first()
            if row is None:
                return None
            value = _values(row)
            if value["status"] == "IN_PROGRESS":
                matching = [frame for frame in self._frames
                            if frame.fresh and frame.phase == "CHECK" and frame.snapshot == value
                            and frame.token == value["transaction_token"]
                            and self._same_native(frame.native, native)]
                if len(matching) == 1:
                    self._shape(value, native, succeeded=False)
                    return None
                _fail("ISSUE_INCONNUE")
            self._shape(value, native, succeeded=True)
            if value["xid"] == native[2]:
                _fail("ISSUE_INCONNUE")
            return value["result_ref"]
        try:
            with self._inspect() as native:
                row = _model().objects.using(self._inspection).filter(operation_id=act.operation_id).first()
                if row is None:
                    return None
                value = _values(row)
                self._shape(value, native, succeeded=True)
                return value["result_ref"]
        except (CoreServiceError, CorePortError, DatabaseError, InterfaceError, ConnectionDoesNotExist):
            _fail("ISSUE_INCONNUE")

    def reconcile_unknown(self, proof):
        frame = self._frame(proof, live=False)
        main, _peer = self._aliases()
        if (main.in_atomic_block or len(self._frames) != 1 or self._attempts != 1
                or self._reconciled or not frame.fresh or frame.phase != "RESULT"
                or frame.result_stage is None
                or tuple(stage for stage in proof.staged if stage.staged_kind == _RESULT)
                   != (frame.result_stage,)):
            _fail("ISSUE_INCONNUE")
        try:
            with self._inspect() as native:
                if native[0] is frame.native[0] or native[1] == frame.native[1]:
                    _fail("ISSUE_INCONNUE")
                self._read_frame(frame, self._inspection)
                self._shape(frame.snapshot, native, succeeded=True)
        except (CoreServiceError, CorePortError, DatabaseError, InterfaceError, ConnectionDoesNotExist):
            _fail("ISSUE_INCONNUE")
        self._reconciled = True
        return "SUCCEEDED"
