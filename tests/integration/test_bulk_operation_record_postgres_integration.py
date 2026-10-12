"""Preuves PostgreSQL isolées de BulkOperationRecord v1 ; import et tests ordinaires inertes."""

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_TARGET = str(Path(__file__))
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
_FIELDS = (
    "operation_id", "bulk_type", "bulk_version", "status",
    "tenant_context_reference", "scope_context_reference", "format",
    "conflict_strategy", "commit_mode",
)
_FLAGS = (
    "search_path_isolated", "forward_applied", "roundtrip", "nullable_roundtrip",
    "canonical_members_roundtrip", "null_refused", "empty_refused",
    "unknown_members_refused", "duplicate_refused", "semver_db_accepted",
    "semver_python_refused", "save_without_implicit_validation",
    "reverse_only_0003", "existing_tables_stable", "public_tables_stable",
)

def _helpers():
    integration = str(_ROOT / "tests" / "integration")
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration


def _outcome():
    return {
        "real_pg": False, "phase": "COMPLETE", "reason": "NONE",
        "cleanup_ok": False, "conns_closed": False, "server_version_num": None,
        **{key: False for key in _FLAGS},
    }


def _body(result, h, state, refs, failures):
    import django
    from django.apps import apps
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from psycopg import sql
    from unittest import mock

    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
        result["server_version_num"] = int(h._scalar(admin, "SHOW server_version_num", ()))
        state["public_before"] = [h._table_identity(admin, "public", table) for table in state["tables"]]
        state["schema"] = h._safe_schema_name()
        state["owned"], reason = h._create_schema(admin, state["schema"])
        if reason != "NONE" or not state["owned"]:
            result["reason"] = reason
            return
        search_path = h._quote_search_path(admin, state["schema"])
    if settings.configured:
        result["reason"] = "SETTINGS_ALREADY_CONFIGURED"
        return
    database, user, password = state["credentials"]
    settings.configure(
        INSTALLED_APPS=["pixs.backend"], SECRET_KEY="bulk-record-synthetic-test",
        DATABASES={"default": {
            "ENGINE": "django.db.backends.postgresql", "NAME": database,
            "USER": user, "PASSWORD": password, "HOST": "127.0.0.1", "PORT": "5432",
            "OPTIONS": {"options": h._pg_options(search_path), "connect_timeout": 2},
            "CONN_MAX_AGE": 0,
        }},
        LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True,
    )
    state["configured"] = True
    django.setup()
    Model = apps.get_model("backend", "BulkOperationRecord")
    from pixs.kernel.bulk_operations import (
        BulkCommitMode, BulkConflictStrategy, BulkOperationState,
        BulkOperationVariant, BulkReferenceFormat,
    )
    enums = {
        "bulk_type": BulkOperationVariant, "status": BulkOperationState,
        "format": BulkReferenceFormat, "conflict_strategy": BulkConflictStrategy,
        "commit_mode": BulkCommitMode,
    }
    if h._scalar(connection, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        result["reason"] = "SEARCH_PATH_MISMATCH"
        return
    result["search_path_isolated"] = True
    MigrationExecutor(connection).migrate([("backend", "0002_job_record")])
    before = [h._table_identity(connection, state["schema"], table) for table in state["tables"][:2]]
    assert all(before)
    MigrationExecutor(connection).migrate([("backend", "0003_bulk_operation_record")])
    assert h._table_exists(connection, state["schema"], Model._meta.db_table)
    assert h._applied_count(connection, state["schema"], "0003_bulk_operation_record") == 1
    result["forward_applied"] = True
    data = {
        "operation_id": "bulk-opaque-é", "bulk_type": next(iter(BulkOperationVariant)).value,
        "bulk_version": "1.2.3-rc.1+build", "status": next(iter(BulkOperationState)).value,
        "tenant_context_reference": "opaque equal ", "scope_context_reference": "opaque equal ",
        "format": next(iter(BulkReferenceFormat)).value, "conflict_strategy": None,
        "commit_mode": None,
    }
    row = Model.from_values(data)
    assert row._state.adding
    row.full_clean()
    row.save(force_insert=True)
    fetched = Model.objects.get(pk=data["operation_id"])
    assert all(getattr(fetched, name) == data[name] for name in _FIELDS)
    result["roundtrip"] = True
    null_data = {**data, "operation_id": "bulk-nulls", "scope_context_reference": None}
    Model.from_values(null_data).save(force_insert=True)
    null_row = Model.objects.get(pk=null_data["operation_id"])
    assert all(getattr(null_row, name) is None for name in ("scope_context_reference", "conflict_strategy", "commit_mode"))
    result["nullable_roundtrip"] = True
    for name, enum in enums.items():
        for index, item in enumerate(enum):
            values = {**data, "operation_id": name + str(index), name: item.value}
            candidate = Model.from_values(values)
            candidate.full_clean()
            candidate.save(force_insert=True)
            assert getattr(Model.objects.get(pk=values["operation_id"]), name) == item.value
    result["canonical_members_roundtrip"] = True

    def raw_refused(name, value):
        query = sql.SQL("UPDATE {}.{} SET {} = %s WHERE operation_id = %s").format(
            sql.Identifier(state["schema"]), sql.Identifier(Model._meta.db_table),
            sql.Identifier(name),
        ).as_string(connection.connection)
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(query, (value, data["operation_id"]))
        except IntegrityError:
            return True
        return False

    nullable = {"scope_context_reference", "conflict_strategy", "commit_mode"}
    result["null_refused"] = all(raw_refused(name, None) for name in _FIELDS if name not in nullable)
    result["empty_refused"] = all(raw_refused(name, "") for name in _FIELDS)
    result["unknown_members_refused"] = all(raw_refused(name, "UNKNOWN") for name in enums)
    query = sql.SQL("INSERT INTO {}.{} SELECT * FROM {}.{} WHERE operation_id = %s").format(
        sql.Identifier(state["schema"]), sql.Identifier(Model._meta.db_table),
        sql.Identifier(state["schema"]), sql.Identifier(Model._meta.db_table),
    ).as_string(connection.connection)
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(query, (data["operation_id"],))
    except IntegrityError:
        result["duplicate_refused"] = True
    invalid = Model(**{**data, "operation_id": "bulk-invalid-semver", "bulk_version": "not-semver"})
    with mock.patch.object(Model, "full_clean", side_effect=AssertionError("validation implicite")):
        invalid.save(force_insert=True)
    result["save_without_implicit_validation"] = True
    loaded = Model.objects.get(pk=invalid.pk)
    result["semver_db_accepted"] = loaded.bulk_version == "not-semver"
    try:
        loaded.full_clean(exclude=["bulk_version"])
    except ValidationError as error:
        result["semver_python_refused"] = error.messages == ["valeurs de persistance bulk invalides"]
    invalid.delete()
    MigrationExecutor(connection).migrate([("backend", "0002_job_record")])
    result["reverse_only_0003"] = bool(
        not h._table_exists(connection, state["schema"], Model._meta.db_table)
        and h._applied_count(connection, state["schema"], "0003_bulk_operation_record") == 0
        and h._applied_count(connection, state["schema"], "0002_job_record") == 1
        and h._applied_count(connection, state["schema"], "0001_feature_flag_source_snapshot") == 1
    )
    result["existing_tables_stable"] = before == [
        h._table_identity(connection, state["schema"], table) for table in state["tables"][:2]
    ]


def run_real_bulk_operation_record_postgres(root_str):
    """Charge les secrets uniquement dans le processus de test, sortie fermée et nettoyage prouvé."""
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result["reason"] = "ROOT_INVALID"
        return result
    if str(Path(root_str).resolve()) != _EXPECTED_ROOT:
        result["reason"] = "ROOT_MISMATCH"
        return result
    h = _helpers()
    refs, failures = [], []
    state = {
        "credentials": None, "schema": None, "owned": False, "configured": False,
        "public_before": None,
        "tables": ("backend_featureflagsourcesnapshotrecord", "backend_jobrecord", "backend_bulkoperationrecord"),
    }
    with h._mask_output():
        try:
            found = h._read_project_env(root_str)
            if type(found) is not dict:
                result["reason"] = "ENV_REFUSED"
            else:
                credentials = tuple(found.get(name) for name in ("PG_DATABASE", "PG_USERNAME", "PG_PASSWORD"))
                del found
                if any(type(value) is not str or not value for value in credentials):
                    result["reason"] = "ENV_INCOMPLETE"
                else:
                    state["credentials"] = credentials
                    del credentials
                    _body(result, h, state, refs, failures)
        except BaseException:
            # Frontière du test sensible : aucune exception ni valeur secrète ne sort.
            result["reason"] = "TEST_FAILED"
        finally:
            try:
                if state["configured"]:
                    from django.db import connections
                    connections.close_all()
                if state["credentials"] is not None:
                    with h._managed_pg_connection(*state["credentials"], refs, failures) as admin:
                        if state["public_before"] is not None:
                            result["public_tables_stable"] = state["public_before"] == [
                                h._table_identity(admin, "public", table) for table in state["tables"]
                            ]
                        if state["owned"]:
                            result["cleanup_ok"] = h._drop_schema_if_owned(admin, state["schema"], True)
                        else:
                            result["cleanup_ok"] = True
                else:
                    result["cleanup_ok"] = True
                result["conns_closed"] = not failures and all(bool(conn.closed) for conn in refs)
                if state["configured"]:
                    result["conns_closed"] = result["conns_closed"] and all(
                        wrapper.connection is None for wrapper in connections.all()
                    )
            except BaseException:
                result["reason"] = "FINALIZATION_FAILED"
                result["cleanup_ok"] = result["conns_closed"] = False
    result["real_pg"] = bool(
        result["reason"] == "NONE" and result["cleanup_ok"] and result["conns_closed"]
        and all(result[key] for key in _FLAGS)
    )
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"
    return result

_CHILD = textwrap.dedent(
    r'''
    import builtins
    import importlib.util
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock

    src_path = sys.argv[1]
    target_path = sys.argv[2]
    sys.path.insert(0, src_path)

    import django
    import psycopg
    from django.apps import apps
    from django.conf import settings
    from django.db import connection
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from psycopg import Connection

    assert settings.configured is False
    assert apps.ready is False

    guard_targets = (
        (psycopg, "connect", ()),
        (Connection, "connect", ()),
        (PGWrapper, "get_new_connection", (object(), {})),
        (socket.socket, "connect", (object(), ("127.0.0.1", 0))),
        (socket, "create_connection", (("127.0.0.1", 0),)),
        (subprocess, "Popen", (["true"],)),
        (subprocess, "run", (["true"],)),
        (builtins, "open", ("project.env", "rb")),
        (Path, "open", (Path("project.env"), "rb")),
        (os, "open", ("project.env", os.O_RDONLY)),
    )
    guards = [
        mock.Mock(side_effect=AssertionError("forbidden"))
        for _ in guard_targets
    ]

    with ExitStack() as stack:
        for (target, name, _args), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))

        spec = importlib.util.spec_from_file_location(
            "bulk_record_pg_harness_under_test", target_path
        )
        harness = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(harness)

        for (target, name, args), guard in zip(guard_targets, guards):
            try:
                getattr(target, name)(*args)
            except AssertionError:
                pass
            else:
                raise AssertionError("garde inactive")
            assert guard.call_count == 1
            guard.reset_mock()

        assert callable(harness.run_real_bulk_operation_record_postgres)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_bulk_operation_record_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_bulk_operation_record_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("BULK_RECORD_PG_HARNESS_SAFE_OK")
    '''
).strip()

class BulkOperationRecordPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "BULK_RECORD_PG_HARNESS_SAFE_OK\n")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ("--real-pg", "--real-pg-job-regression"):
        if sys.argv[1] == "--real-pg":
            outcome = run_real_bulk_operation_record_postgres(str(_ROOT))
        else:
            outcome = _helpers().run_real_job_record_postgres(str(_ROOT))
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
