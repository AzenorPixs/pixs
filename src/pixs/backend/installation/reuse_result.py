"""Participant privé C08 de réutilisation, sans écriture de compte ni de mode.

Core vérifie la liaison existante ; Auth consomme sa propre autorisation.
C08 conserve son résultat initial et son dernier état, sans les réinitialiser.
"""
from __future__ import annotations

import copy
import datetime as dt
from dataclasses import dataclass, replace

from django.db import DatabaseError, InterfaceError

from pixs.auth.bootstrap_backend import AuthBootstrapBackend
from pixs.backend.installation.result_writer import (
    C08TransactionalResultWriter, _KIND, _model, _snapshot_model)
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.services_common import CoreServiceError, lock_scopes

__all__ = ["C08ReuseResultParticipant"]
_AUTH_KIND = "bootstrap-authorization-consumption"


def _values(row):
    return {field.attname: copy.deepcopy(getattr(row, field.attname))
            for field in row._meta.concrete_fields}


@dataclass(frozen=True, slots=True, repr=False)
class _ReuseResultFrame:
    native: tuple
    header: dict
    snapshot: dict
    authorization: StagedRef
    result: StagedRef
    observed_at: dt.datetime


class C08ReuseResultParticipant:
    def __init__(self, *, writer: C08TransactionalResultWriter,
                 auth: AuthBootstrapBackend) -> None:
        if (type(writer) is not C08TransactionalResultWriter
                or type(auth) is not AuthBootstrapBackend
                or auth._alias != writer._using
                or writer._act.closed_effects != ("REUSE_EXISTING",)):
            raise CorePortError()
        self._writer, self._auth = writer, auth
        self._frame = None
        self._bound()

    def _bound(self):
        plan, _entry = self._writer._stable()
        spec = plan.target_spec
        if (self._writer._act.closed_effects != ("REUSE_EXISTING",)
                or type(spec.expected_binding_version) is not int
                or spec.expected_binding_version < 1
                or type(spec.expected_identity_version) is not int
                or spec.expected_identity_version < 1
                or self._writer._version != spec.expected_binding_version
                or self._auth._alias != self._writer._using):
            raise CorePortError()
        return plan

    def _capture(self, native):
        plan = self._bound()
        alias = self._writer._using
        act = self._writer._act
        try:
            header = _model().objects.using(alias).select_for_update().filter(
                installation_ref=act.installation_ref).first()
            snapshot = _snapshot_model().objects.using(alias).select_for_update().filter(
                installation_id=act.installation_ref).order_by("-version").first()
        except (DatabaseError, InterfaceError):
            raise CorePortError() from None
        if header is None or snapshot is None:
            raise CorePortError()
        now = self._writer._now()
        if (header.database_target_ref != plan.database_target_ref
                or header.result_ref != "pixs.core.binding:" + act.installation_ref
                or header.result_version != 1
                or (header.database_oid, header.schema_oid) != native[3:5]
                or snapshot.installation_id != act.installation_ref
                or (snapshot.database_oid, snapshot.schema_oid) != native[3:5]
                or type(snapshot.version) is not int or snapshot.version < 1):
            raise CorePortError()
        for row, timestamp in ((header, header.prepared_at), (snapshot, snapshot.created_at)):
            if (type(row.pid) is not int or row.pid < 1
                    or type(row.xid) is not str or not row.xid.isdigit()
                    or row.xid == "0" or row.xid == native[2]
                    or type(timestamp) is not dt.datetime or timestamp.tzinfo is None
                    or timestamp.astimezone(dt.timezone.utc) > now):
                raise CorePortError()
        return _values(header), _values(snapshot)

    def stage_result(self, proof: TransactionProof, *, result_ref: str,
                     transaction_token: str) -> StagedRef:
        self._writer._proof(proof)
        if (transaction_token != proof.transaction_token
                or result_ref != "pixs.core.binding:" + self._writer._act.installation_ref
                or any(ref.staged_kind in (_KIND, _AUTH_KIND) for ref in proof.staged)):
            raise CorePortError()
        try:
            lock_scopes(self._writer._using,
                        ("installation:" + self._writer._act.installation_ref,))
        except CoreServiceError:
            raise CorePortError() from None
        native = self._writer._native(proof.alias)
        header, snapshot = self._capture(native)
        if self._frame is not None:
            frame = self._frame
            if (not self._writer._same_native(frame.native, native)
                    or frame.header != header or frame.snapshot != snapshot
                    or frame.result.transaction_token != transaction_token):
                raise CorePortError()
        authorization = self._auth.consume_reuse_authorization(
            alias=proof.alias, operation_id=proof.operation_id,
            transaction_token=transaction_token,
            target_identity_ref=self._writer._act.target_identity_ref,
            context=proof.context)
        expected = StagedRef(proof.operation_id, proof.alias, transaction_token,
                             proof.context, _AUTH_KIND)
        if type(authorization) is not StagedRef or authorization != expected:
            raise CorePortError()
        result = StagedRef(proof.operation_id, proof.alias, transaction_token,
                           proof.context, _KIND)
        if self._frame is None:
            self._frame = _ReuseResultFrame(native, header, snapshot, authorization,
                                           result, self._writer._now())
        elif (self._frame.authorization != authorization or self._frame.result != result):
            raise CorePortError()
        return result

    def verify_staged(self, proof: TransactionProof) -> None:
        self._writer._proof(proof)
        self._bound()
        frame = self._frame
        if (frame is None
                or tuple(ref for ref in proof.staged if ref.staged_kind == _KIND) != (frame.result,)
                or any(ref.staged_kind == _AUTH_KIND for ref in proof.staged)
                or proof.prepared_at < frame.observed_at):
            raise CorePortError()
        native = self._writer._native(proof.alias)
        if not self._writer._same_native(frame.native, native):
            raise CorePortError()
        header, snapshot = self._capture(native)
        if frame.header != header or frame.snapshot != snapshot:
            raise CorePortError()
        # Cette référence vient de l'effet Auth réellement préparé dans cette
        # transaction. Le participant Auth vérifie son propre cadre natif.
        auth_proof = replace(proof, staged=proof.staged + (frame.authorization,))
        auth_proof.__post_init__()
        if self._auth.verify_reuse_staged(auth_proof) is not None:
            raise CorePortError()
        return None
