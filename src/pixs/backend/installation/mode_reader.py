"""Lecteur prive du mode C08 installe, sans autorisation ni selection."""

from __future__ import annotations

import datetime as dt
import os
import threading
import uuid
from contextlib import contextmanager
from dataclasses import dataclass

from django.db import connections, transaction, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.installation.marker import (
    MarkerConfig, MarkerInvalid,
    read_installation_marker)
from pixs.backend.installation.mode_values import (
    ConfigurationState, ModeOperationKind, validate_state_pair,
    transition_state, ModeValuesError)
from pixs.backend.installation.result_writer import _native_context
from pixs.backend.startup_mode import StartupMode
from pixs.core.authz.ports import Clock
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.ports import CorePortError
from pixs.core.services_common import CoreServiceError, lock_scopes

__all__ = ["C08ModeReadUnavailable", "C08ModeReadIssueUnknown",
           "C08InstalledMode", "C08InstalledModeReader"]


class C08ModeReadUnavailable(CorePortError):
    code = "C08_MODE_READ_UNAVAILABLE"

    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_MODE_READ_UNAVAILABLE"
        self.element = "installation_mode"
        self.step = "read_current"
        self.args = ("Mode installé indisponible.",)


class C08ModeReadIssueUnknown(CorePortError):
    code = "C08_MODE_READ_ISSUE_UNKNOWN"

    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_MODE_READ_ISSUE_UNKNOWN"
        self.element = "installation_mode"
        self.step = "read_current"
        self.args = ("Lecture du mode incertaine.",)


@dataclass(frozen=True, slots=True, repr=False)
class C08InstalledMode:
    installation_ref: str
    snapshot_id: uuid.UUID
    version: int
    configuration_state: ConfigurationState
    operating_mode: StartupMode


def _parent_model():
    from pixs.backend.c08_installation_result_record import C08InstallationResultRecord
    return C08InstallationResultRecord


def _snapshot_model():
    from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord
    return C08ModeSnapshotRecord


def _receipt_model():
    from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord
    return C08ModeOperationReceiptRecord


_GOVERNED_FIELDS = ("metadata_profile_ref", "metadata_published_version",
                    "metadata_owner_component", "metadata_source_of_truth",
                    "governance_ref", "confidentiality", "personal",
                    "retention_policy", "deletion_policy", "publication_ref",
                    "catalog_version", "catalog_sha256")


class C08InstalledModeReader:
    def __init__(self, *, using: str, inspection_using: str,
                 marker_config: MarkerConfig, installation_ref: str,
                 database_target_ref: str, clock: Clock) -> None:
        for value in (using, inspection_using, installation_ref, database_target_ref):
            if type(value) is not str or not value or not value.isprintable():
                raise C08ModeReadUnavailable()
        if type(marker_config) is not MarkerConfig:
            raise C08ModeReadUnavailable()
        if using == inspection_using:
            raise C08ModeReadUnavailable()
        if not callable(getattr(clock, "now", None)):
            raise C08ModeReadUnavailable()
        try:
            marker_config.__post_init__()
        except MarkerInvalid:
            raise C08ModeReadUnavailable() from None
        for value in (using, inspection_using, installation_ref, database_target_ref):
            if len(value) > marker_config.max_ref_len:
                raise C08ModeReadUnavailable()
        self._using = using
        self._inspection = inspection_using
        self._marker = marker_config
        self._installation = installation_ref
        self._target = database_target_ref
        self._clock = clock
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._active = False

    def _now(self):
        value = self._clock.now()
        if type(value) is not dt.datetime or value.tzinfo is not dt.timezone.utc:
            raise C08ModeReadUnavailable()
        return value

    def _stable(self):
        if os.getpid() != self._pid or threading.get_ident() != self._thread:
            raise C08ModeReadIssueUnknown()

    def _aliases(self):
        try:
            main = connections[self._using]
            reader = connections[self._inspection]
        except ConnectionDoesNotExist:
            raise C08ModeReadUnavailable() from None
        if (main is reader or main.vendor != "postgresql" or reader.vendor != "postgresql"
                or (main.connection is not None and reader.connection is main.connection)):
            raise C08ModeReadUnavailable()
        for name in ("ENGINE", "NAME", "USER", "PASSWORD", "HOST", "PORT", "OPTIONS", "TIME_ZONE"):
            if main.settings_dict.get(name) != reader.settings_dict.get(name):
                raise C08ModeReadUnavailable()
        return main, reader

    @staticmethod
    def _main_identity(connection):
        if (connection.in_atomic_block or not connection.get_autocommit()
                or connection.needs_rollback or connection.closed_in_transaction
                or connection.connection.autocommit is not True):
            raise C08ModeReadUnavailable()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pg_backend_pid(), "
                "(SELECT oid::bigint FROM pg_database WHERE datname=current_database()), "
                "(SELECT oid::bigint FROM pg_namespace WHERE nspname=current_schema()), "
                "current_schema(), current_schemas(false)")
            row = cursor.fetchone()
        if (row is None or len(row) != 5
                or any(type(row[i]) is not int or row[i] < 1 for i in (0, 1, 2))
                or type(row[3]) is not str or not row[3] or row[4] != [row[3]]):
            raise C08ModeReadUnavailable()
        return row[:3]

    @staticmethod
    def _check_uuid(value):
        try:
            check_uuid7(value)
        except Uuid7Error:
            raise C08ModeReadUnavailable() from None

    @staticmethod
    def _check_native_historic(pid, xid, db_oid, sch_oid, current_db, current_sch):
        if (type(pid) is not int or pid < 1 or type(xid) is not str
                or not xid.isdigit() or xid == "0"
                or type(db_oid) is not int or db_oid < 1
                or type(sch_oid) is not int or sch_oid < 1):
            raise C08ModeReadUnavailable()
        if (db_oid, sch_oid) != (current_db, current_sch):
            raise C08ModeReadUnavailable()

    @staticmethod
    def _check_date(value, now):
        if (type(value) is not dt.datetime or value.tzinfo is None
                or value == dt.datetime.max.replace(tzinfo=dt.timezone.utc)
                or value == dt.datetime.min.replace(tzinfo=dt.timezone.utc)):
            raise C08ModeReadUnavailable()
        if value.astimezone(dt.timezone.utc) > now:
            raise C08ModeReadUnavailable()

    @staticmethod
    def _check_governed(row, status=None):
        actual = status if status is not None else row.governance_status
        if actual == "WAIVED":
            for name in _GOVERNED_FIELDS:
                if getattr(row, name) is not None:
                    raise C08ModeReadUnavailable()
            return
        if actual != "GOVERNED":
            raise C08ModeReadUnavailable()
        for name in _GOVERNED_FIELDS:
            value = getattr(row, name)
            if type(value) is not str or value == "":
                raise C08ModeReadUnavailable()
        if (row.metadata_owner_component != "pixs.backend"
                or row.confidentiality not in ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED")
                or row.personal not in ("NONE", "PERSONAL", "SENSITIVE_PERSONAL")):
            raise C08ModeReadUnavailable()
        if type(row.catalog_sha256) is not str or len(row.catalog_sha256) != 64:
            raise C08ModeReadUnavailable()
        for ch in row.catalog_sha256:
            if ch not in "0123456789abcdef":
                raise C08ModeReadUnavailable()

    def _load_all(self, alias, current_db, current_sch, now):
        parent = _parent_model().objects.using(alias).filter(
            installation_ref=self._installation).first()
        if parent is None:
            raise C08ModeReadUnavailable()
        if (parent.database_target_ref != self._target
                or parent.result_ref != "pixs.core.binding:" + self._installation):
            raise C08ModeReadUnavailable()
        if type(parent.result_version) is not int or parent.result_version < 1:
            raise C08ModeReadUnavailable()
        self._check_native_historic(parent.pid, parent.xid, parent.database_oid,
                                    parent.schema_oid, current_db, current_sch)
        self._check_date(parent.prepared_at, now)
        self._check_governed(parent, status="GOVERNED")
        effects = parent.closed_effects
        if type(effects) is not list or not effects:
            raise C08ModeReadUnavailable()
        if any(type(v) is not str or not v for v in effects):
            raise C08ModeReadUnavailable()
        if len(set(effects)) != len(effects):
            raise C08ModeReadUnavailable()
        allowed = {"CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL", "CREATE_TENANT", "GRANT_SUPER_ADMIN_TENANT", "REUSE_EXISTING"}
        if any(v not in allowed for v in effects):
            raise C08ModeReadUnavailable()
        if ("REUSE_EXISTING" in effects or "CREATE_IDENTITY" not in effects
                or "BIND_SUPER_ADMIN" not in effects or "STAMP_CREDENTIAL" not in effects):
            raise C08ModeReadUnavailable()
        root = _snapshot_model().objects.using(alias).filter(
            installation_id=self._installation, version=1).first()
        if root is None:
            raise C08ModeReadUnavailable()
        self._check_uuid(root.record_id)
        if (root.version != 1 or root.origin != "R01_INITIAL"
                or root.configuration_state != "PENDING"
                or root.operating_mode != StartupMode.FIRST_CONFIGURATION.value
                or root.governance_status != "GOVERNED"
                or root.predecessor_id is not None
                or root.operation_receipt_id is not None
                or root.creator_operation_id != parent.operation_id):
            raise C08ModeReadUnavailable()
        if ((root.pid, root.xid, root.database_oid, root.schema_oid)
                != (parent.pid, parent.xid, parent.database_oid, parent.schema_oid)):
            raise C08ModeReadUnavailable()
        self._check_date(root.created_at, now)
        if root.created_at.astimezone(dt.timezone.utc) != parent.prepared_at.astimezone(dt.timezone.utc):
            raise C08ModeReadUnavailable()
        self._check_governed(root)
        last = _snapshot_model().objects.using(alias).filter(
            installation_id=self._installation).order_by("-version").first()
        if last is None:
            raise C08ModeReadUnavailable()
        self._check_uuid(last.record_id)
        self._check_native_historic(last.pid, last.xid, last.database_oid,
                                    last.schema_oid, current_db, current_sch)
        self._check_date(last.created_at, now)
        self._check_governed(last)
        if type(last.version) is not int or last.version < 1:
            raise C08ModeReadUnavailable()
        try:
            config = ConfigurationState(last.configuration_state)
            mode = StartupMode(last.operating_mode)
        except ValueError:
            raise C08ModeReadUnavailable() from None
        if mode is StartupMode.INSTALLER:
            raise C08ModeReadUnavailable()
        try:
            validate_state_pair(config, mode)
        except ModeValuesError:
            raise C08ModeReadUnavailable() from None
        receipt = None
        predecessor = None
        if last.version == 1:
            if last.record_id != root.record_id:
                raise C08ModeReadUnavailable()
        else:
            if last.origin != "MODE_TRANSITION":
                raise C08ModeReadUnavailable()
            predecessor = _snapshot_model().objects.using(alias).filter(
                record_id=last.predecessor_id).first()
            if (predecessor is None or str(predecessor.installation_id) != self._installation
                    or predecessor.version != last.version - 1):
                raise C08ModeReadUnavailable()
            self._check_uuid(predecessor.record_id)
            self._check_native_historic(
                predecessor.pid, predecessor.xid, predecessor.database_oid,
                predecessor.schema_oid, current_db, current_sch)
            self._check_date(predecessor.created_at, now)
            self._check_governed(predecessor)
            if predecessor.version == 1 and predecessor.record_id != root.record_id:
                raise C08ModeReadUnavailable()
            receipt = _receipt_model().objects.using(alias).filter(
                record_id=last.operation_receipt_id).first()
            if (receipt is None or receipt.status != "SUCCEEDED"
                    or str(receipt.installation_id) != self._installation
                    or receipt.operation_id != last.creator_operation_id
                    or receipt.expected_version != predecessor.version
                    or receipt.result_kind != "NEW_SNAPSHOT"
                    or receipt.result_snapshot_id != last.record_id
                    or receipt.result_version != last.version
                    or receipt.result_persistence_state != "ACTIVE"
                    or receipt.result_correlation_id != receipt.correlation_id
                    or (receipt.pid, receipt.xid, receipt.database_oid, receipt.schema_oid)
                    != (last.pid, last.xid, last.database_oid, last.schema_oid)):
                raise C08ModeReadUnavailable()
            self._check_uuid(receipt.record_id)
            if (receipt.scope_type != "PLATFORM" or receipt.tenant_id is not None
                    or receipt.scope_id is not None
                    or type(receipt.result_ref) is not str or not receipt.result_ref
                    or type(receipt.correlation_id) is not str or not receipt.correlation_id):
                raise C08ModeReadUnavailable()
            self._check_date(receipt.started_at, now)
            self._check_date(receipt.finished_at, now)
            if receipt.finished_at < receipt.started_at:
                raise C08ModeReadUnavailable()
            self._check_governed(receipt)
            try:
                kind = ModeOperationKind(receipt.kind)
                before = (ConfigurationState(predecessor.configuration_state),
                          StartupMode(predecessor.operating_mode))
                after = transition_state(before[0], before[1], kind)
            except (ValueError, ModeValuesError):
                raise C08ModeReadUnavailable() from None
            if after != (config, mode) or after == before:
                raise C08ModeReadUnavailable()
        def values(row):
            if row is None:
                return None
            return {field.attname: getattr(row, field.attname)
                    for field in row._meta.concrete_fields}

        view = {"parent": values(parent), "root": values(root),
                "last": values(last), "predecessor": values(predecessor),
                "receipt": values(receipt)}
        mode_value = C08InstalledMode(self._installation, last.record_id, last.version, config, mode)
        return mode_value, view

    @contextmanager
    def guard_current(self):
        if self._active:
            raise C08ModeReadUnavailable()
        self._stable()
        try:
            before_marker = read_installation_marker(self._marker)
        except MarkerInvalid:
            raise C08ModeReadUnavailable() from None
        if (before_marker.installation_ref != self._installation
                or before_marker.result_ref != "pixs.core.binding:" + self._installation
                or type(before_marker.result_version) is not int or before_marker.result_version < 1):
            raise C08ModeReadUnavailable()
        main, reader = self._aliases()
        main_opened_here = main.connection is None
        self._active = True
        yielded = False
        cleanup_failed = False
        try:
            identity = self._main_identity(main)
            if (reader.in_atomic_block or not reader.get_autocommit()
                    or reader.needs_rollback or reader.closed_in_transaction
                    or reader.connection.autocommit is not True
                    or reader.connection is main.connection):
                raise C08ModeReadUnavailable()
            with transaction.atomic(using=self._inspection, durable=True):
                with reader.cursor() as cursor:
                    cursor.execute("SET TRANSACTION READ ONLY")
                lock_scopes(self._inspection, ("installation:" + self._installation,), shared=True)
                native = _native_context(self._inspection)
                if native[1] == identity[0] or (native[3], native[4]) != identity[1:]:
                    raise C08ModeReadUnavailable()
                current_db, current_sch = native[3], native[4]
                locked_marker = read_installation_marker(self._marker)
                if locked_marker != before_marker:
                    raise C08ModeReadUnavailable()
                now = self._now()
                mode_value, view = self._load_all(self._inspection, current_db, current_sch, now)
                if (before_marker.result_ref != "pixs.core.binding:" + self._installation
                        or before_marker.result_version != view["parent"]["result_version"]):
                    raise C08ModeReadUnavailable()
                yielded = True
                yield mode_value
                self._stable()
                if (self._aliases() != (main, reader)
                        or self._main_identity(main) != identity
                        or not self._same_native(native)):
                    raise C08ModeReadIssueUnknown()
                try:
                    after_marker = read_installation_marker(self._marker)
                except MarkerInvalid:
                    raise C08ModeReadIssueUnknown() from None
                if after_marker != before_marker:
                    raise C08ModeReadIssueUnknown()
                now = self._now()
                again, view_again = self._load_all(self._inspection, current_db, current_sch, now)
                if again != mode_value or view_again != view:
                    raise C08ModeReadIssueUnknown()
        except C08ModeReadIssueUnknown:
            raise
        except (CorePortError, CoreServiceError, DatabaseError, InterfaceError,
                ConnectionDoesNotExist, MarkerInvalid):
            if yielded:
                raise C08ModeReadIssueUnknown() from None
            raise C08ModeReadUnavailable() from None
        finally:
            self._active = False
            if os.getpid() != self._pid or threading.get_ident() != self._thread:
                raise C08ModeReadIssueUnknown() from None
            if (not main_opened_here and reader.connection is not None
                    and main.connection is not None and reader.connection is main.connection):
                raise C08ModeReadIssueUnknown() from None
            for connection in ((reader, main) if main_opened_here else (reader,)):
                try:
                    connection.close()
                    if connection.connection is not None:
                        cleanup_failed = True
                except (DatabaseError, InterfaceError):
                    cleanup_failed = True
            if cleanup_failed:
                raise C08ModeReadIssueUnknown() from None

    def _same_native(self, native):
        try:
            current = _native_context(self._inspection)
        except CorePortError:
            return False
        return (native[0] is current[0] and native[1:] == current[1:]
                and tuple(native[5]) == tuple(current[5]))

    def read_current(self) -> C08InstalledMode:
        with self.guard_current() as mode:
            result = mode
        return result
