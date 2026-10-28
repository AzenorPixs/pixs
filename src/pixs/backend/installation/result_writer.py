"""Écrivain transactionnel privé du résultat C08, sans pouvoir d'autorisation.

La composition de confiance appelle ce participant après les contrôles Core,
Auth et audit. Ni une preuve structurée ni cette ligne ne prouvent le commit.
Le résultat initial et le premier état sont créés dans la même transaction.
Le chemin de réutilisation et la lecture indépendante de l'ancien acte
restent à réaliser. Cette source n'est pas encore testée, aucun état committé ni disponibilité P0 démontré.
"""
from __future__ import annotations

import datetime as dt
import os
import threading

from django.db import connections, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.c10_catalog import C10Catalog, CatalogInvalid, _Lease
from pixs.backend.installation.act_content import verify_act_plan_binding
from pixs.backend.installation.plan import PlanInvalid, PlanConfirmationLink, plan_sha256
from pixs.backend.installation.storage import PlanStoreConfig, read_plan
from pixs.backend.startup_mode import StartupMode
from pixs.core.authz.ports import Clock
from pixs.core.dto import BootstrapActInput, CommandEnvelope
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7, generate_uuid7
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.services_common import CoreServiceError, lock_scopes

__all__ = ["C08TransactionalResultWriter"]

_KIND = "c08-installation-result"


def _model():
    from pixs.backend.c08_installation_result_record import C08InstallationResultRecord
    return C08InstallationResultRecord


def _snapshot_model():
    from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord
    return C08ModeSnapshotRecord


def _native_context(alias):
    if type(alias) is not str or not alias:
        raise CorePortError()
    try:
        connection = connections[alias]
        if (connection.vendor != "postgresql" or not connection.in_atomic_block
                or connection.connection is None or connection.needs_rollback
                or connection.closed_in_transaction
                or connection.connection.autocommit is not False):
            raise CorePortError()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pg_backend_pid(), pg_current_xact_id()::text, "
                "(SELECT oid::bigint FROM pg_database WHERE datname=current_database()), "
                "(SELECT oid::bigint FROM pg_namespace WHERE nspname=current_schema()), "
                "current_schema(), current_schemas(false)")
            row = cursor.fetchone()
    except (ConnectionDoesNotExist, DatabaseError, InterfaceError):
        raise CorePortError() from None
    if (row is None or len(row) != 6
            or any(type(row[i]) is not int or row[i] < 1 for i in (0, 2, 3))
            or type(row[1]) is not str or not row[1].isdigit() or row[1] == "0"
            or type(row[4]) is not str or not row[4] or row[5] != [row[4]]):
        raise CorePortError()
    return (connection.connection, row[0], row[1], row[2], row[3],
            tuple(connection.savepoint_ids))


class C08TransactionalResultWriter:
    def __init__(self, *, using: str, store: PlanStoreConfig,
                 act: BootstrapActInput, envelope: CommandEnvelope,
                 confirmations: tuple[PlanConfirmationLink, ...],
                 metadata_lease: _Lease, clock: Clock, result_version: int) -> None:
        if (type(store) is not PlanStoreConfig or type(act) is not BootstrapActInput
                or type(envelope) is not CommandEnvelope or type(metadata_lease) is not _Lease
                or type(metadata_lease.owner) is not C10Catalog
                or type(result_version) is not int or result_version < 1
                or not callable(getattr(clock, "now", None))):
            raise CorePortError()
        self._using, self._store = using, store
        self._act, self._envelope, self._confirmations = act, envelope, confirmations
        self._metadata, self._clock, self._version = metadata_lease, clock, result_version
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._frame = None
        try:
            self._plan_digest = plan_sha256(read_plan(store), store.limits)
        except PlanInvalid:
            raise CorePortError() from None
        self._text(using)
        self._metadata_pin = None
        self._stable()

    def _text(self, value):
        if (type(value) is not str or not 0 < len(value) <= self._store.limits.max_ref_len
                or not value.isprintable()):
            raise CorePortError()

    def _now(self):
        value = self._clock.now()
        if type(value) is not dt.datetime or value.tzinfo is not dt.timezone.utc:
            raise CorePortError()
        return value

    def _stable(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise CorePortError()
        try:
            plan = read_plan(self._store)
            if plan_sha256(plan, self._store.limits) != self._plan_digest:
                raise CorePortError()
            verify_act_plan_binding(self._act, self._envelope, plan,
                                    self._confirmations, self._store.limits)
            entry = self._metadata.profile()
        except (PlanInvalid, CatalogInvalid):
            raise CorePortError() from None
        # La composition sélectionne le profil propre aux données C08.
        # Le propriétaire est le module backend qui porte la table C08.
        if (entry.profile.owner_component != "pixs.backend"
                or self._envelope.request.resource_id not in entry.resource_refs):
            raise CorePortError()
        pin = (entry.publication_ref, entry.catalog_version, entry.raw_sha256,
               self._metadata.owner.config.binding.profile_ref,
               entry.published_version, entry.profile)
        if self._metadata_pin is None:
            self._metadata_pin = pin
        elif self._metadata_pin != pin:
            raise CorePortError()
        return plan, entry

    def _require_initial_effects(self):
        try:
            effects = list(self._act.closed_effects)
        except TypeError:
            raise CorePortError() from None
        if self._version != 1 or "REUSE_EXISTING" in effects:
            raise CorePortError()
        if ("CREATE_IDENTITY" not in effects or "BIND_SUPER_ADMIN" not in effects
                or "STAMP_CREDENTIAL" not in effects):
            raise CorePortError()

    def _native(self, alias):
        if type(alias) is not str or alias != self._using:
            raise CorePortError()
        return _native_context(alias)

    def _proof(self, proof):
        if type(proof) is not TransactionProof:
            raise CorePortError()
        proof.__post_init__()
        if (proof.alias != self._using or proof.operation_id != self._act.operation_id
                or proof.context != self._act.context or proof.prepared_at > self._now()):
            raise CorePortError()
        self._text(proof.transaction_token)
        self._stable()

    def _expected(self, transaction_token, result_ref, native):
        self._text(transaction_token)
        plan, entry = self._stable()
        profile = entry.profile
        act = self._act
        return dict(
            installation_ref=act.installation_ref, operation_id=act.operation_id,
            plan_version=act.plan_version, plan_sha256=self._plan_digest,
            content_sha256=act.content_sha256, serializer_version=act.serializer_version,
            database_target_ref=plan.database_target_ref,
            operator_subject_ref=act.operator_subject_ref, operator_proof_ref=act.operator_proof_ref,
            authorization_ref=act.authorization_ref, target_identity_ref=act.target_identity_ref,
            target_tenant_ref=act.target_tenant_ref, closed_effects=list(act.closed_effects),
            confirmations=list(act.confirmations), correlation_id=act.correlation_id,
            causation_id=act.causation_id, idempotency_key=act.idempotency_key,
            result_ref=result_ref, result_version=self._version,
            transaction_token=transaction_token,
            scope_type="PLATFORM", tenant_id=None, scope_id=None,
            publication_ref=entry.publication_ref, catalog_version=entry.catalog_version,
            catalog_sha256=entry.raw_sha256,
            metadata_profile_ref=self._metadata.owner.config.binding.profile_ref,
            metadata_published_version=entry.published_version,
            metadata_owner_component=profile.owner_component,
            metadata_source_of_truth=profile.source_of_truth,
            governance_ref=profile.data_asset_id, confidentiality=profile.confidentiality.value,
            personal=profile.personal_data.value, retention_policy=profile.retention_policy,
            deletion_policy=profile.deletion_policy,
            database_oid=native[3], schema_oid=native[4], pid=native[1], xid=native[2])

    def _snapshot_expected(self, native, snapshot_id):
        try:
            check_uuid7(snapshot_id)
        except Uuid7Error:
            raise CorePortError() from None
        _, entry = self._stable()
        profile = entry.profile
        act = self._act
        return dict(
            record_id=snapshot_id, installation_id=act.installation_ref, version=1,
            configuration_state="PENDING",
            operating_mode=StartupMode.FIRST_CONFIGURATION.value,
            origin="R01_INITIAL", predecessor_id=None, operation_receipt_id=None,
            creator_operation_id=act.operation_id,
            pid=native[1], xid=native[2], database_oid=native[3], schema_oid=native[4],
            metadata_profile_ref=self._metadata.owner.config.binding.profile_ref,
            metadata_published_version=entry.published_version,
            metadata_owner_component=profile.owner_component,
            metadata_source_of_truth=profile.source_of_truth,
            governance_ref=profile.data_asset_id, governance_status="GOVERNED",
            confidentiality=profile.confidentiality.value, personal=profile.personal_data.value,
            retention_policy=profile.retention_policy, deletion_policy=profile.deletion_policy,
            publication_ref=entry.publication_ref, catalog_version=entry.catalog_version,
            catalog_sha256=entry.raw_sha256)

    @staticmethod
    def _same_native(first, current):
        return first[0] is current[0] and first[1:] == current[1:]

    @staticmethod
    def _check_row(row, expected, prepared_at):
        if (row is None or any(getattr(row, name) != value for name, value in expected.items())
                or type(row.prepared_at) is not dt.datetime or row.prepared_at.tzinfo is None
                or row.prepared_at.astimezone(dt.timezone.utc) != prepared_at):
            raise CorePortError()

    @staticmethod
    def _check_snapshot_row(row, expected, prepared_at):
        if row is None or any(getattr(row, name) != value for name, value in expected.items()):
            raise CorePortError()
        if (type(row.created_at) is not dt.datetime or row.created_at.tzinfo is None
                or row.created_at.astimezone(dt.timezone.utc) != prepared_at):
            raise CorePortError()

    def stage_result(self, proof: TransactionProof, *, result_ref: str,
                     transaction_token: str) -> StagedRef:
        self._proof(proof)
        self._text(result_ref)
        if (transaction_token != proof.transaction_token
                or result_ref != "pixs.core.binding:" + self._act.installation_ref):
            raise CorePortError()
        self._require_initial_effects()
        # Même domaine d'exclusion que l'acte Core, pas de namespace C08 parallèle.
        try:
            lock_scopes(self._using, ("installation:" + self._act.installation_ref,))
        except CoreServiceError:
            raise CorePortError() from None
        native = self._native(proof.alias)
        expected = self._expected(proof.transaction_token, result_ref, native)
        if self._frame is not None:
            if (not self._same_native(self._frame["native"], native)
                    or self._frame["expected"] != expected):
                raise CorePortError()
            prepared_at = self._frame["prepared_at"]
            snapshot_id = self._frame["snapshot_id"]
        else:
            prepared_at = self._now()
            try:
                snapshot_id = generate_uuid7()
                check_uuid7(snapshot_id)
            except Uuid7Error:
                raise CorePortError() from None
        snapshot_expected = self._snapshot_expected(native, snapshot_id)
        if (self._frame is not None
                and self._frame["snapshot_expected"] != snapshot_expected):
            raise CorePortError()
        try:
            row = _model().objects.using(proof.alias).filter(
                installation_ref=self._act.installation_ref).first()
            snap_row = _snapshot_model().objects.using(proof.alias).filter(
                record_id=snapshot_id).first()
            if self._frame is None:
                if row is not None or snap_row is not None:
                    raise CorePortError()
                if _snapshot_model().objects.using(proof.alias).filter(
                        installation_id=self._act.installation_ref).exists():
                    raise CorePortError()
                row = _model().objects.using(proof.alias).create(**expected, prepared_at=prepared_at)
                snap_row = _snapshot_model().objects.using(proof.alias).create(
                    **snapshot_expected, created_at=prepared_at)
            self._check_row(row, expected, prepared_at)
            self._check_snapshot_row(snap_row, snapshot_expected, prepared_at)
            if _snapshot_model().objects.using(proof.alias).filter(
                    installation_id=self._act.installation_ref).count() != 1:
                raise CorePortError()
            if (snap_row.version != 1 or snap_row.configuration_state != "PENDING"
                    or snap_row.operating_mode != StartupMode.FIRST_CONFIGURATION.value
                    or snap_row.origin != "R01_INITIAL" or snap_row.predecessor_id is not None
                    or snap_row.operation_receipt_id is not None
                    or snap_row.creator_operation_id != self._act.operation_id):
                raise CorePortError()
        except (DatabaseError, InterfaceError):
            raise CorePortError() from None
        self._frame = dict(native=native, expected=expected, prepared_at=prepared_at,
                           snapshot_id=snapshot_id, snapshot_expected=snapshot_expected)
        return StagedRef(proof.operation_id, proof.alias, transaction_token, proof.context, _KIND)

    def verify_staged(self, proof: TransactionProof) -> None:
        self._proof(proof)
        self._require_initial_effects()
        if self._frame is None or sum(s.staged_kind == _KIND for s in proof.staged) != 1:
            raise CorePortError()
        native = self._native(proof.alias)
        expected = self._expected(proof.transaction_token, self._frame["expected"]["result_ref"], native)
        snapshot_expected = self._snapshot_expected(native, self._frame["snapshot_id"])
        if (not self._same_native(self._frame["native"], native)
                or self._frame["expected"] != expected
                or self._frame["snapshot_expected"] != snapshot_expected):
            raise CorePortError()
        try:
            row = _model().objects.using(proof.alias).filter(
                installation_ref=self._act.installation_ref).first()
            self._check_row(row, expected, self._frame["prepared_at"])
            snap_row = _snapshot_model().objects.using(proof.alias).filter(
                record_id=self._frame["snapshot_id"]).first()
            self._check_snapshot_row(snap_row, snapshot_expected, self._frame["prepared_at"])
            others = _snapshot_model().objects.using(proof.alias).filter(
                installation_id=self._act.installation_ref).exclude(
                record_id=self._frame["snapshot_id"])
            if others.exists():
                raise CorePortError()
        except (DatabaseError, InterfaceError):
            raise CorePortError() from None
        return None
