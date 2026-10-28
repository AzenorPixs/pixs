"""Lecteur privé C08 : résultat durable et garde PostgreSQL du marqueur.

Ce dépôt ne donne ni autorisation R01 ni mode. La composition de confiance
effectue les contrôles d'entrée ; aucune route publique n'est ouverte ici.
Le lecteur post-commit utilise un alias serveur distinct, jamais fourni
par un client, et reste séparé des participants de la transaction mutatrice.
"""
from __future__ import annotations

import datetime as dt
from contextlib import contextmanager

from django.db import connections, transaction, DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.installation.marker import (
    InstallationMarkerContent, MarkerInvalid, MarkerResultUnavailable, MarkerIssueUnknown)
from pixs.backend.installation.result_writer import (
    C08TransactionalResultWriter, _model, _native_context)
from pixs.backend.installation.act_idempotence import (
    C08ActIdempotenceParticipant, _model as _act_model, _values as _act_values)
from pixs.core.dto import BootstrapActInput
from pixs.core.ports import CorePortError
from pixs.core.services_common import CoreServiceError, lock_scopes


class _ResultAbsent(MarkerResultUnavailable):
    code = "C08_RESULT_ABSENT"


class C08ResultReader:
    def __init__(self, *, writer: C08TransactionalResultWriter,
                 inspection_using: str, marker_format_version: str,
                 idempotence: C08ActIdempotenceParticipant | None = None) -> None:
        if type(writer) is not C08TransactionalResultWriter:
            raise CorePortError()
        self._writer = writer
        writer._text(inspection_using)
        writer._text(marker_format_version)
        if inspection_using == writer._using:
            raise CorePortError()
        self._inspection = inspection_using
        self._format = marker_format_version
        self._active = False
        if idempotence is not None and (
                type(idempotence) is not C08ActIdempotenceParticipant
                or idempotence._writer is not writer
                or idempotence._inspection != inspection_using):
            raise CorePortError()
        if writer._act.closed_effects == ("REUSE_EXISTING",) and idempotence is None:
            raise CorePortError()
        self._idempotence = idempotence
        writer._stable()
        self._aliases()

    def _aliases(self):
        try:
            main = connections[self._writer._using]
            reader = connections[self._inspection]
        except ConnectionDoesNotExist:
            raise CorePortError() from None
        if (main is reader or main.vendor != "postgresql" or reader.vendor != "postgresql"
                or (main.connection is not None and reader.connection is main.connection)):
            raise CorePortError()
        # Comparaison en processus seulement : aucune valeur privée n'est copiée
        # dans un résultat, une empreinte publique ou un diagnostic.
        for name in ("ENGINE", "NAME", "USER", "PASSWORD", "HOST", "PORT", "OPTIONS", "TIME_ZONE"):
            if main.settings_dict.get(name) != reader.settings_dict.get(name):
                raise CorePortError()
        return main, reader

    def _load_committed(self, alias, native):
        self._writer._stable()
        act = self._writer._act
        row = _model().objects.using(alias).filter(installation_ref=act.installation_ref).first()
        if row is None:
            return None
        if (type(row.pid) is not int or row.pid < 1
                or type(row.xid) is not str or not row.xid.isdigit() or row.xid == "0"
                or row.xid == native[2]
                or (row.database_oid, row.schema_oid) != (native[3], native[4])
                or type(row.prepared_at) is not dt.datetime or row.prepared_at.tzinfo is None
                or row.prepared_at.astimezone(dt.timezone.utc) > self._writer._now()):
            raise CorePortError()
        if act.closed_effects == ("REUSE_EXISTING",):
            return self._load_reuse_committed(alias, native, row)
        # Ce tuple décrit l'écrivain historique du reçu, pas une preuve native
        # du lecteur courant. La visibilité et native ci-dessus sont vérifiées.
        stored = (None, row.pid, row.xid, row.database_oid, row.schema_oid, ())
        expected = self._writer._expected(
            row.transaction_token, "pixs.core.binding:" + act.installation_ref, stored)
        prepared = row.prepared_at.astimezone(dt.timezone.utc)
        self._writer._check_row(row, expected, prepared)
        self._writer._stable()
        content = InstallationMarkerContent(
            self._format, act.installation_ref, row.result_ref, row.result_version)
        return content, expected, prepared

    def _load_reuse_committed(self, alias, native, header):
        # Le nouvel acte et le résultat initial ont des identités distinctes.
        # Le reçu propre à cet acte doit être réellement visible après commit.
        if self._idempotence is None or header.result_version != 1:
            raise CorePortError()
        row = _act_model().objects.using(alias).filter(
            operation_id=self._writer._act.operation_id).first()
        if row is None:
            raise _ResultAbsent()
        value = _act_values(row)
        if value["xid"] == native[2] or value["status"] != "SUCCEEDED":
            raise CorePortError()
        self._idempotence._shape(value, (*native, alias), succeeded=True)
        if value["result_kind"] != "REUSE" or value["result_ref"] != header.result_ref:
            raise CorePortError()
        prepared = header.prepared_at.astimezone(dt.timezone.utc)
        content = InstallationMarkerContent(
            self._format, header.installation_ref, header.result_ref, header.result_version)
        # Les deux lignes sont rapprochées à nouveau à la fin du guard.
        return content, (_act_values(header), value), prepared

    def inspect_confirmed(self, act: BootstrapActInput) -> str | None:
        if type(act) is not BootstrapActInput or act != self._writer._act:
            raise CorePortError()
        self._writer._stable()
        try:
            main = connections[self._writer._using]
            if main.in_atomic_block:
                lock_scopes(self._writer._using, ("installation:" + act.installation_ref,),
                            shared=True)
                native = _native_context(self._writer._using)
                value = self._load_committed(self._writer._using, native)
                if not self._writer._same_native(native, _native_context(self._writer._using)):
                    raise CorePortError()
                return None if value is None else value[0].result_ref
            with self.guard_confirmed(installation_ref=act.installation_ref) as content:
                return content.result_ref
        except _ResultAbsent:
            return None
        except (ConnectionDoesNotExist, DatabaseError, InterfaceError, CoreServiceError,
                MarkerInvalid):
            raise CorePortError() from None

    @staticmethod
    def _main_identity(connection):
        if (connection.in_atomic_block or not connection.get_autocommit()
                or connection.needs_rollback or connection.closed_in_transaction
                or connection.connection.autocommit is not True):
            raise CorePortError()
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
            raise CorePortError()
        return row[:3]

    @contextmanager
    def guard_confirmed(self, *, installation_ref: str):
        if installation_ref != self._writer._act.installation_ref or self._active:
            raise MarkerResultUnavailable()
        self._writer._stable()
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
                raise CorePortError()
            with transaction.atomic(using=self._inspection, durable=True):
                with reader.cursor() as cursor:
                    cursor.execute("SET TRANSACTION READ ONLY")
                lock_scopes(self._inspection,
                            ("installation:" + installation_ref,), shared=True)
                native = _native_context(self._inspection)
                if native[1] == identity[0] or (native[3], native[4]) != identity[1:]:
                    raise CorePortError()
                value = self._load_committed(self._inspection, native)
                if value is None:
                    raise _ResultAbsent()
                yielded = True
                yield value[0]
                if (self._aliases() != (main, reader)
                        or self._main_identity(main) != identity
                        or not self._writer._same_native(native, _native_context(self._inspection))
                        or self._load_committed(self._inspection, native) != value):
                    raise CorePortError()
        except (CorePortError, CoreServiceError, DatabaseError, InterfaceError,
                ConnectionDoesNotExist):
            if yielded:
                raise MarkerIssueUnknown() from None
            raise MarkerResultUnavailable() from None
        finally:
            for connection in ((reader, main) if main_opened_here else (reader,)):
                if (connection is reader and not main_opened_here
                        and reader.connection is not None and reader.connection is main.connection):
                    cleanup_failed = True
                    continue
                try:
                    connection.close()
                    if connection.connection is not None:
                        cleanup_failed = True
                except (DatabaseError, InterfaceError):
                    cleanup_failed = True
            if cleanup_failed:
                raise MarkerIssueUnknown() from None
            self._active = False
