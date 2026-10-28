"""Fournisseur initial C10 : faits publiés et reçus SQL dans la transaction Core.

La composition tient les deux gardes filesystem jusqu'au retour de l'acte
Core. Cette classe ne crée ni publisher, ni autorité, ni fonctionnalité de
purge. Le reçu SQL ne prouve pas à lui seul un commit Core/Auth/C08.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import threading
from urllib.parse import quote

from django.db import connections, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist
from pixs.backend.c10_catalog import C10Catalog, CatalogInvalid, _Lease
from pixs.core.authz.ports import Clock, Request, PortError
from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION
from pixs.core.dto import CoreInputInvalid, GovernanceAttestation
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType, validate_structure, ScopeStructureError

__all__ = ["C10GovernanceAdapter"]


def _text(value: object, limit: int) -> None:
    if type(value) is not str or not 0 < len(value) <= limit or not value.isprintable():
        raise CorePortError()


def _bytes(value: object) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError):
        raise CorePortError() from None


def _model():
    from pixs.backend.c10_receipt_record import C10ReceiptRecord
    return C10ReceiptRecord


def _scope(context: object) -> None:
    if type(context) is not ScopeContext:
        raise CorePortError()
    try:
        validate_structure(context)
    except ScopeStructureError:
        raise CorePortError() from None
    if (context.scope_type is not ScopeType.PLATFORM
            or context.tenant_id is not None or context.scope_id is not None):
        raise CorePortError()


class C10GovernanceAdapter:
    def __init__(self, *, using: str, installation_ref: str,
                 core_lease: _Lease, metadata_lease: _Lease, clock: Clock) -> None:
        for lease in (core_lease, metadata_lease):
            if type(lease) is not _Lease or type(lease.owner) is not C10Catalog:
                raise CorePortError()
        if core_lease is metadata_lease or core_lease.owner is metadata_lease.owner:
            raise CorePortError()
        self._core, self._metadata, self._clock = core_lease, metadata_lease, clock
        if not callable(getattr(clock, "now", None)):
            raise CorePortError()
        self._limit = min(core_lease.owner.config.max_ref_len,
                          metadata_lease.owner.config.max_ref_len)
        for value in (using, installation_ref):
            _text(value, self._limit)
        self._using, self._installation = using, installation_ref
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._operation = None
        self._frame = None
        self._profiles()

    def _now(self):
        now = self._clock.now()
        if type(now) is not dt.datetime or now.tzinfo is not dt.timezone.utc:
            raise CorePortError()
        return now

    def _profiles(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()
        try:
            core, metadata = self._core.profile(), self._metadata.profile()
        except CatalogInvalid:
            raise CorePortError() from None
        if ((core.publication_ref, core.catalog_version, core.raw_sha256) !=
                (metadata.publication_ref, metadata.catalog_version, metadata.raw_sha256)
                or core.profile.owner_component != "pixs.core"
                or core.profile.data_asset_id == metadata.profile.data_asset_id
                or self._core.owner.config.binding.profile_ref ==
                   self._metadata.owner.config.binding.profile_ref):
            raise CorePortError()
        return core, metadata

    def _native(self, alias):
        if type(alias) is not str or alias != self._using:
            raise CorePortError()
        self._profiles()
        try:
            connection = connections[alias]
            if (connection.vendor != "postgresql" or not connection.in_atomic_block
                    or connection.needs_rollback or connection.closed_in_transaction
                    or connection.connection is None):
                raise CorePortError()
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_backend_pid(), pg_current_xact_id()::text")
                result = cursor.fetchone()
        except (ConnectionDoesNotExist, DatabaseError, InterfaceError):
            raise CorePortError() from None
        if (result is None or type(result[0]) is not int or result[0] < 1
                or type(result[1]) is not str or not result[1].isdigit()):
            raise CorePortError()
        return connection.connection, result[0], result[1], tuple(connection.savepoint_ids)

    def _request(self, request, alias, operation, token):
        if type(request) is not Request:
            raise CorePortError()
        try:
            request.__post_init__()
        except PortError:
            raise CorePortError() from None
        _scope(request.context)
        for value in (operation, token, request.decision_id, request.subject_id,
                      request.resource_id, request.action_id, request.correlation_id):
            _text(value, self._limit)
        if (request.action_id != BOOTSTRAP_ACTION
                or request.resource_id != "pixs.core.bootstrap:" + quote(self._installation, safe="")):
            raise CorePortError()
        if self._operation is not None and self._operation != operation:
            raise CorePortError()
        native = self._native(alias)
        core, metadata = self._profiles()
        if request.resource_id not in core.resource_refs:
            raise CorePortError()
        digest = hashlib.sha256(_bytes([
            request.decision_id, request.subject_id, request.resource_id,
            request.action_id, "PLATFORM", request.correlation_id])).hexdigest()
        return native, core, metadata, digest

    def _values(self, request, operation, token, kind, resources, native, core, metadata, digest):
        meta = metadata.profile
        key = hashlib.sha256(_bytes(["C10_RECEIPT_V1", self._using, operation,
                                      token, native[2], kind, list(resources), digest])).hexdigest()
        return dict(
            receipt_id="c10:" + key, operation_id=operation, transaction_token=token,
            receipt_kind=kind, scope_type="PLATFORM", tenant_id=None, scope_id=None,
            request_sha256=digest, resource_refs=list(resources), correlation_id=request.correlation_id,
            publication_ref=core.publication_ref, catalog_version=core.catalog_version,
            raw_sha256=core.raw_sha256, core_profile_ref=self._core.owner.config.binding.profile_ref,
            core_published_version=core.published_version, core_data_asset_id=core.profile.data_asset_id,
            metadata_profile_ref=self._metadata.owner.config.binding.profile_ref,
            metadata_published_version=metadata.published_version,
            metadata_owner_component=meta.owner_component, metadata_source_of_truth=meta.source_of_truth,
            governance_ref=meta.data_asset_id, confidentiality=meta.confidentiality.value,
            personal=meta.personal_data.value, retention_policy=meta.retention_policy,
            deletion_policy=meta.deletion_policy, pid=native[1], xid=native[2])

    def _stage(self, request, alias, operation, token, kind, resources):
        native, core, metadata, digest = self._request(request, alias, operation, token)
        if (type(resources) is not tuple or not resources
                or any(type(r) is not str or r not in core.resource_refs for r in resources)
                or len(set(resources)) != len(resources)):
            raise CorePortError()
        if kind == "ATTEST":
            if self._frame is None or self._frame["native"][2] != native[2]:
                self._frame = dict(native=native, request=request, operation=operation,
                                   token=token, receipts={})
            elif (self._frame["request"] is not request
                    or self._frame["token"] != token
                    or self._frame["native"][0] is not native[0]
                    or self._frame["native"][1:] != native[1:]):
                raise CorePortError()
            self._operation = operation
        elif (self._frame is None or self._frame["request"] is not request
              or self._frame["operation"] != operation or self._frame["token"] != token
              or self._frame["native"][0] is not native[0]
              or self._frame["native"][1:3] != native[1:3]):
            raise CorePortError()
        expected = self._values(request, operation, token, kind, resources,
                                native, core, metadata, digest)
        now = self._now()
        try:
            row = _model().objects.using(alias).filter(pk=expected["receipt_id"]).first()
            if row is None:
                row = _model().objects.using(alias).create(**expected, prepared_at=now)
            self._check_row(row, expected, now)
        except (DatabaseError, InterfaceError):
            raise CorePortError() from None
        self._frame["receipts"][expected["receipt_id"]] = (kind, resources)
        return expected["receipt_id"], core, now

    @staticmethod
    def _check_row(row, expected, now):
        if any(getattr(row, name) != value for name, value in expected.items()):
            raise CorePortError()
        if (type(row.prepared_at) is not dt.datetime or row.prepared_at.tzinfo is None
                or row.prepared_at.astimezone(dt.timezone.utc) > now):
            raise CorePortError()

    def attest(self, request: Request, *, alias: str, operation_id: str,
               transaction_token: str) -> GovernanceAttestation:
        core, _ = self._profiles()
        _, core, now = self._stage(request, alias, operation_id, transaction_token,
                                   "ATTEST", core.resource_refs)
        try:
            return GovernanceAttestation(core.profile, core.published_version,
                                         request.context, core.resource_refs, now)
        except CoreInputInvalid:
            raise CorePortError() from None

    def stage_read(self, request: Request, *, resource_refs: tuple[str, ...],
                   alias: str, operation_id: str, transaction_token: str) -> StagedRef:
        key, _, _ = self._stage(request, alias, operation_id, transaction_token,
                                "READ", resource_refs)
        return StagedRef(operation_id, alias, transaction_token, request.context, "c10-read:" + key)

    def authorize_state_change(self, request: Request, *, current_state: str, target_state: str,
                               alias: str, operation_id: str, transaction_token: str) -> StagedRef:
        # Le fournisseur initial ne réalise ni archivage ni suppression C10.
        raise CorePortError()

    def verify_staged(self, proof: TransactionProof) -> None:
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        for stage in proof.staged:
            stage.__post_init__()
        _scope(proof.context)
        frame = self._frame
        if (frame is None or proof.operation_id != frame["operation"]
                or proof.transaction_token != frame["token"]
                or proof.context != frame["request"].context):
            raise CorePortError()
        native, core, metadata, digest = self._request(
            frame["request"], proof.alias, proof.operation_id, proof.transaction_token)
        if (native[0] is not frame["native"][0] or native[1:] != frame["native"][1:]):
            raise CorePortError()
        now = self._now()
        if proof.prepared_at > now:
            raise CorePortError()
        expected_reads = {"c10-read:" + key for key, value in frame["receipts"].items()
                          if value[0] == "READ"}
        actual_reads = [s.staged_kind for s in proof.staged if s.staged_kind.startswith("c10-read:")]
        if set(actual_reads) != expected_reads or len(actual_reads) != len(expected_reads):
            raise CorePortError()
        for stage in proof.staged:
            if stage.staged_kind in expected_reads and stage.context != proof.context:
                raise CorePortError()
        attest_count = 0
        for key, (kind, resources) in frame["receipts"].items():
            expected = self._values(frame["request"], proof.operation_id,
                proof.transaction_token, kind, resources, native, core, metadata, digest)
            if expected["receipt_id"] != key:
                raise CorePortError()
            try:
                row = _model().objects.using(proof.alias).filter(pk=key).first()
            except (DatabaseError, InterfaceError):
                raise CorePortError() from None
            if row is None:
                raise CorePortError()
            self._check_row(row, expected, now)
            attest_count += kind == "ATTEST"
        if attest_count != 1:
            raise CorePortError()
