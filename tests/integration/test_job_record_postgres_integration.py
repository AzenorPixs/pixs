"""Intégration PostgreSQL bornée de JobRecord : gardes sûres plus callable réel mandaté."""

import re
import subprocess
import sys
import textwrap
import unittest
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_INTEGRATION = str(_ROOT / "tests" / "integration")
_TARGET = str(Path(__file__))
_MARKER = "JOB_RECORD_PG_HARNESS_SAFE_OK\n"
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

_PG_HOST = "127.0.0.1"
_PG_PORT = 5432
_CONNECT_TIMEOUT_SECONDS = 2
_STATEMENT_TIMEOUT_MS = 1500
_LOCK_TIMEOUT_MS = 1500
_ENV_READ_LIMIT = 65537
_MIGRATION_0001 = "0001_feature_flag_source_snapshot"
_MIGRATION_0002 = "0002_job_record"
_MIGRATION_FORWARD = ("backend", _MIGRATION_0002)
_MIGRATION_REVERSE = ("backend", _MIGRATION_0001)
_FF_TABLE = "backend_featureflagsourcesnapshotrecord"
_FIXED_VERSION_MSG = "version de travail SemVer complète attendue"
_SCHEMA_RE = re.compile(r"job_record_[0-9a-f]{16}")
_FIXED_CODE_RE = re.compile(r"[A-Z][A-Z_]*")

_JOB_FIELDS = (
    "job_id",
    "job_type",
    "job_version",
    "payload",
    "subject",
    "tenant_context",
    "correlation_id",
    "causation_id",
    "perimeter_reference",
    "state",
    "attempt_count",
    "lease_owner",
    "lease_expires_at",
)
_REQUIRED_FLAGS = (
    "forward_applied",
    "roundtrip",
    "attempt_default",
    "checks_refused",
    "null_refused",
    "duplicate_refused",
    "semver_db_accepted",
    "semver_python_refused",
    "row_removed",
    "reverse_only_0002",
    "ff_identity_stable",
)

_CHILD = textwrap.dedent(
    r"""
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
            "job_record_pg_harness_under_test", target_path
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

        assert callable(harness.run_real_job_record_postgres)
        assert callable(harness._read_project_env)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_job_record_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_job_record_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("JOB_RECORD_PG_HARNESS_SAFE_OK")
    """
).strip()


def _closed_result():
    result = {"real_pg": False, "phase": "INIT", "reason": "NONE"}
    for key in _REQUIRED_FLAGS:
        result[key] = False
    result["cleanup_ok"] = False
    result["conns_closed"] = False
    return result


def _combine(result, code):
    if result["reason"] != "NONE":
        return
    if type(code) is str and _FIXED_CODE_RE.fullmatch(code) and code != "NONE":
        result["reason"] = code


def _env_loader():
    if _INTEGRATION not in sys.path:
        sys.path.insert(0, _INTEGRATION)
    import test_pg_connectivity_integration as harness

    return harness._parse_env_text


def _read_project_env(root_str):
    parse = _env_loader()
    env_path = Path(root_str) / "project.env"
    try:
        with env_path.open("rb") as handle:
            raw = handle.read(_ENV_READ_LIMIT)
    except Exception:
        return None
    if len(raw) >= _ENV_READ_LIMIT:
        return None
    try:
        text = raw.decode("utf-8")
    except Exception:
        return None
    if "\x00" in text:
        return None
    try:
        return parse(text)
    except Exception:
        return None


@contextmanager
def _mask_output():
    import io
    import logging

    previous_disable = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    original_out = sys.stdout
    original_err = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = original_out
        sys.stderr = original_err
        logging.disable(previous_disable)


def _pg_options(search_path=None):
    options = (
        f"-c statement_timeout={_STATEMENT_TIMEOUT_MS} "
        f"-c lock_timeout={_LOCK_TIMEOUT_MS}"
    )
    if search_path is not None:
        options = f"{options} -c search_path={search_path},pg_catalog"
    return options


def _safe_schema_name():
    name = "job_record_" + uuid.uuid4().hex[:16]
    if _SCHEMA_RE.fullmatch(name) is None:
        raise RuntimeError("invalid synthetic schema name")
    return name


@contextmanager
def _managed_pg_connection(database, user, password, refs, close_failures, options=None):
    import psycopg

    connection = None
    try:
        connection = psycopg.connect(
            host=_PG_HOST,
            port=_PG_PORT,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=_CONNECT_TIMEOUT_SECONDS,
            autocommit=True,
            options=_pg_options() if options is None else options,
        )
        refs.append(connection)
        yield connection
    finally:
        if connection is not None:
            try:
                if not connection.closed:
                    connection.close()
            except Exception:
                close_failures.append("CONN_CLOSE_FAILED")


def _scalar(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    finally:
        cursor.close()


def _schema_exists(connection, schema_name):
    return bool(
        _scalar(
            connection,
            "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (schema_name,),
        )
    )


def _table_exists(connection, schema_name, table_name):
    return bool(
        _scalar(
            connection,
            """
            SELECT EXISTS (
                SELECT 1
                FROM pg_class AS class
                JOIN pg_namespace AS namespace
                  ON namespace.oid = class.relnamespace
                WHERE namespace.nspname = %s AND class.relname = %s
            )
            """,
            (schema_name, table_name),
        )
    )


def _table_identity(connection, schema_name, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT class.oid, class.relfilenode, namespace.nspname
            FROM pg_class AS class
            JOIN pg_namespace AS namespace
              ON namespace.oid = class.relnamespace
            WHERE namespace.nspname = %s AND class.relname = %s
            """,
            (schema_name, table_name),
        )
        return cursor.fetchone()
    finally:
        cursor.close()


def _applied_count(wrapper, schema_name, migration_name):
    from psycopg import sql

    wrapper.ensure_connection()
    query = (
        sql.SQL(
            "SELECT count(*) FROM {}.django_migrations WHERE app = %s AND name = %s"
        )
        .format(sql.Identifier(schema_name))
        .as_string(wrapper.connection)
    )
    cursor = wrapper.cursor()
    try:
        cursor.execute(query, ("backend", migration_name))
        return int(cursor.fetchone()[0])
    finally:
        cursor.close()


def _create_schema(connection, schema_name):
    from psycopg import errors, sql

    if _SCHEMA_RE.fullmatch(schema_name) is None:
        return False, "SCHEMA_NAME_INVALID"
    try:
        if _schema_exists(connection, schema_name):
            return False, "SCHEMA_COLLISION"
    except Exception:
        return False, "SCHEMA_PROBE_FAILED"

    owned = False
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name))
            )
            owned = True
        finally:
            cursor.close()
    except errors.DuplicateSchema:
        return False, "SCHEMA_COLLISION"
    except errors.InsufficientPrivilege:
        return owned, "SCHEMA_PERMISSION_DENIED"
    except Exception:
        return owned, "SCHEMA_CREATE_FAILED"

    try:
        if _schema_exists(connection, schema_name):
            return owned, "NONE"
        return owned, "SCHEMA_CREATE_UNPROVED"
    except Exception:
        return owned, "SCHEMA_CREATE_UNPROVED"


def _drop_schema_if_owned(connection, schema_name, owned):
    from psycopg import sql

    if not owned:
        return False
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema_name))
            )
        finally:
            cursor.close()
    except Exception:
        return False
    return not _schema_exists(connection, schema_name)


def _quote_search_path(connection, schema_name):
    from psycopg import sql

    return sql.Identifier(schema_name).as_string(connection)


def _valid_kwargs(**over):
    suffix = uuid.uuid4().hex[:12]
    values = {
        "job_id": "jr-" + suffix,
        "job_type": "notify.real",
        "job_version": "2.0.0-rc.1",
        "payload": {"k": [1, 2, {"x": None}]},
        "subject": {"tenant": "t-" + suffix},
        "tenant_context": {},
        "correlation_id": "corr-" + suffix,
        "causation_id": "cause-" + suffix,
        "perimeter_reference": "perim-" + suffix,
        "state": "PENDING",
        "attempt_count": 0,
        "lease_owner": "worker-" + suffix,
        "lease_expires_at": datetime(2099, 1, 1, tzinfo=timezone.utc),
    }
    values.update(over)
    return values


def _refuses_integrity(operation):
    from django.db import IntegrityError, transaction

    try:
        with transaction.atomic():
            operation()
    except IntegrityError:
        return True
    return False


def _refuses_raw_null(wrapper, schema_name, table_name, column, job_id):
    from django.db import IntegrityError, transaction
    from psycopg import sql

    wrapper.ensure_connection()
    query = (
        sql.SQL("UPDATE {}.{} SET {} = NULL WHERE job_id = %s")
        .format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.Identifier(column),
        )
        .as_string(wrapper.connection)
    )
    try:
        with transaction.atomic():
            cursor = wrapper.cursor()
            try:
                cursor.execute(query, (job_id,))
            finally:
                cursor.close()
    except IntegrityError:
        return True
    return False


def _job_real_body(result, refs, close_failures, state):
    import django
    from django.apps import apps
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    state["schema"] = _safe_schema_name()
    with _managed_pg_connection(
        state["database"], state["user"], state["password"], refs, close_failures
    ) as admin_connection:
        state["ident_before"] = _table_identity(admin_connection, "public", _FF_TABLE)
        owned, reason = _create_schema(admin_connection, state["schema"])
        state["owned"] = bool(owned)
        _combine(result, reason)
        if not owned or reason != "NONE":
            return
        if owned:
            state["search_path"] = _quote_search_path(admin_connection, state["schema"])

    if state["search_path"] is None:
        return
    if settings.configured:
        _combine(result, "SETTINGS_ALREADY_CONFIGURED")
        return

    settings.configure(
        DEFAULT_CHARSET="utf-8",
        INSTALLED_APPS=["pixs.backend"],
        SECRET_KEY="real-pg-synthetic-only",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": state["database"],
                "USER": state["user"],
                "PASSWORD": state["password"],
                "HOST": _PG_HOST,
                "PORT": str(_PG_PORT),
                "OPTIONS": {
                    "options": _pg_options(state["search_path"]),
                    "connect_timeout": _CONNECT_TIMEOUT_SECONDS,
                },
                "TIME_ZONE": "UTC",
                "CONN_MAX_AGE": 0,
                "ATOMIC_REQUESTS": False,
                "AUTOCOMMIT": True,
            }
        },
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    state["configured"] = True
    django.setup()

    Model = apps.get_model("backend", "JobRecord")
    table_name = Model._meta.db_table
    if _scalar(connection, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        _combine(result, "SEARCH_PATH_MISMATCH")
        return

    MigrationExecutor(connection).migrate([_MIGRATION_FORWARD])
    if not (
        _table_exists(connection, state["schema"], table_name)
        and _table_exists(connection, state["schema"], _FF_TABLE)
        and _applied_count(connection, state["schema"], _MIGRATION_0002) == 1
        and _applied_count(connection, state["schema"], _MIGRATION_0001) == 1
    ):
        _combine(result, "FORWARD_NOT_PROVED")
        return
    result["forward_applied"] = True

    data = _valid_kwargs()
    instance = Model(**data)
    instance.clean_fields()
    instance.save()
    fetched = Model.objects.get(pk=data["job_id"])
    if any(getattr(fetched, name) != data[name] for name in _JOB_FIELDS):
        _combine(result, "ROUNDTRIP_FAILED")
        return
    result["roundtrip"] = True

    minimal = _valid_kwargs()
    for name in ("attempt_count", "lease_owner", "lease_expires_at"):
        minimal.pop(name)
    default_row = Model.objects.create(**minimal)
    if not (
        default_row.attempt_count == 0
        and default_row.lease_owner is None
        and default_row.lease_expires_at is None
    ):
        _combine(result, "DEFAULT_NULLABLE_FAILED")
        return
    result["attempt_default"] = True

    result["checks_refused"] = bool(
        all(
            _refuses_integrity(
                lambda field=name: Model.objects.create(
                    **_valid_kwargs(**{field: ""})
                )
            )
            for name in (
                "job_id",
                "job_type",
                "job_version",
                "correlation_id",
                "causation_id",
                "perimeter_reference",
            )
        )
        and _refuses_integrity(
            lambda: Model.objects.create(**_valid_kwargs(state="BOGUS"))
        )
        and _refuses_integrity(
            lambda: Model.objects.create(**_valid_kwargs(attempt_count=-1))
        )
    )
    result["null_refused"] = all(
        _refuses_raw_null(connection, state["schema"], table_name, column, data["job_id"])
        for column in ("payload", "subject", "tenant_context")
    )
    result["duplicate_refused"] = _refuses_integrity(
        lambda: Model.objects.create(**_valid_kwargs(job_id=data["job_id"]))
    )
    if not (
        result["checks_refused"]
        and result["null_refused"]
        and result["duplicate_refused"]
    ):
        _combine(result, "REFUSALS_INCOMPLETE")
        return

    bad_id = "jr-semver-" + uuid.uuid4().hex[:12]
    bad = Model.objects.create(**_valid_kwargs(job_id=bad_id, job_version="01.2.3"))
    result["semver_db_accepted"] = Model.objects.filter(pk=bad_id).exists()
    try:
        Model.objects.get(pk=bad_id).full_clean(
            validate_unique=False, validate_constraints=False
        )
    except ValidationError as caught:
        result["semver_python_refused"] = bool(
            caught.messages == [_FIXED_VERSION_MSG] and caught.__cause__ is None
        )
    bad.delete()
    result["row_removed"] = not Model.objects.filter(pk=bad_id).exists()
    if not (
        result["semver_db_accepted"]
        and result["semver_python_refused"]
        and result["row_removed"]
    ):
        _combine(result, "SEMVER_GATE_FAILED")
        return

    MigrationExecutor(connection).migrate([_MIGRATION_REVERSE])
    if not (
        not _table_exists(connection, state["schema"], table_name)
        and _table_exists(connection, state["schema"], _FF_TABLE)
        and _applied_count(connection, state["schema"], _MIGRATION_0002) == 0
        and _applied_count(connection, state["schema"], _MIGRATION_0001) == 1
    ):
        _combine(result, "REVERSE_NOT_PROVED")
        return
    result["reverse_only_0002"] = True

    with _managed_pg_connection(
        state["database"],
        state["user"],
        state["password"],
        refs,
        close_failures,
    ) as identity_connection:
        state["ident_after"] = _table_identity(
            identity_connection, "public", _FF_TABLE
        )
    result["ff_identity_stable"] = bool(state["ident_after"] == state["ident_before"])
    if not result["ff_identity_stable"]:
        _combine(result, "FF_IDENTITY_DIVERGED")


def _finalize_job(result, refs, close_failures, state):
    if state["configured"]:
        try:
            from django.db import connections
            for alias in connections:
                wrapper = connections[alias]
                if wrapper.connection is not None:
                    refs.append(wrapper.connection)
                wrapper.close()
        except Exception:
            close_failures.append("ORM_CLOSE_FAILED")

    if state["owned"]:
        if not state["dropped"]:
            try:
                with _managed_pg_connection(
                    state["database"],
                    state["user"],
                    state["password"],
                    refs,
                    close_failures,
                ) as cleanup_connection:
                    state["dropped"] = _drop_schema_if_owned(
                        cleanup_connection, state["schema"], True
                    )
            except Exception:
                state["dropped"] = False
        result["cleanup_ok"] = bool(state["dropped"])
        if not state["dropped"]:
            _combine(result, "CLEANUP_FAILED")
    else:
        result["cleanup_ok"] = True

    all_closed = not close_failures
    for connection in refs:
        try:
            all_closed = all_closed and bool(connection.closed)
        except Exception:
            all_closed = False
    result["conns_closed"] = bool(all_closed)
    if not all_closed:
        _combine(result, "CONNECTION_CLOSE_FAILED")

    result["real_pg"] = bool(
        result["reason"] == "NONE"
        and result["cleanup_ok"]
        and result["conns_closed"]
        and all(result[key] for key in _REQUIRED_FLAGS)
    )
    result["phase"] = "COMPLETE"
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"


def run_real_job_record_postgres(root_str):
    """Callable PG réel invoqué uniquement par une commande CAB dédiée."""
    result = _closed_result()
    refs = []
    close_failures = []
    state = {
        "schema": None,
        "owned": False,
        "dropped": False,
        "configured": False,
        "search_path": None,
        "database": None,
        "user": None,
        "password": None,
        "ident_before": "UNSET",
        "ident_after": "UNSET",
    }

    with _mask_output():
        try:
            if type(root_str) is not str or root_str == "":
                _combine(result, "ROOT_INVALID")
            else:
                try:
                    resolved = str(Path(root_str).resolve())
                except Exception:
                    resolved = ""
                if resolved != _EXPECTED_ROOT:
                    _combine(result, "ROOT_MISMATCH")
                else:
                    found = _read_project_env(root_str)
                    if not isinstance(found, dict):
                        _combine(result, "ENV_REFUSED")
                    else:
                        values = tuple(
                            found.get(name)
                            for name in ("PG_DATABASE", "PG_USERNAME", "PG_PASSWORD")
                        )
                        if any(
                            type(value) is not str or value == "" for value in values
                        ):
                            _combine(result, "ENV_INCOMPLETE")
                        else:
                            (
                                state["database"],
                                state["user"],
                                state["password"],
                            ) = values
                            del values, found
                            result["phase"] = "ENV_READY"
                            _job_real_body(result, refs, close_failures, state)
        except BaseException:
            _combine(result, "UNEXPECTED")
        finally:
            try:
                _finalize_job(result, refs, close_failures, state)
            except BaseException:
                result["real_pg"] = False
                result["cleanup_ok"] = False
                result["conns_closed"] = False
                result["phase"] = "COMPLETE"
                _combine(result, "FINALIZATION_FAILED")
    return result


class JobRecordPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)

if __name__ == "__main__":
    unittest.main()
