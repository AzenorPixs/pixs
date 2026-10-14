"""Intégration sûre de l’adaptateur PostgreSQL des fanions : app, modèle, migration et lecture simulée."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "FEATURE_FLAG_POSTGRES_SOURCE_SAFE_INTEGRATION_OK\n"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(
    r"""
    import builtins
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from unittest import mock

    sys.path.insert(0, sys.argv[1])

    import django
    import psycopg
    from django.apps import apps
    from django.conf import settings
    from django.db import connection, migrations
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.loader import MigrationLoader
    from django.db.migrations.operations import CreateModel
    from django.db.migrations.questioner import NonInteractiveMigrationQuestioner
    from django.db.migrations.state import ProjectState
    from psycopg import Connection

    assert not settings.configured
    assert not apps.ready

    base_guard_targets = (
        (psycopg, "connect", ()),
        (Connection, "connect", ()),
        (PGWrapper, "get_new_connection", (object(), {})),
        (socket.socket, "connect", (object(), ("127.0.0.1", 0))),
        (socket, "create_connection", (("127.0.0.1", 0),)),
        (subprocess, "Popen", (["true"],)),
        (subprocess, "run", (["true"],)),
    )
    base_guards = [
        mock.Mock(side_effect=AssertionError("forbidden"))
        for _ in base_guard_targets
    ]

    with ExitStack() as stack:
        for (target, name, _args), guard in zip(base_guard_targets, base_guards):
            stack.enter_context(mock.patch.object(target, name, guard))

        import pixs.backend.feature_flag_postgres_source as loader

        assert "pixs.backend.models" not in sys.modules

        settings.configure(
            DEFAULT_CHARSET="utf-8",
            INSTALLED_APPS=["pixs.backend"],
            SECRET_KEY="integration-synthetic-test-only",
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                }
            },
            LOGGING_CONFIG=None,
            MIDDLEWARE=(),
            USE_TZ=True,
        )
        django.setup()

        from pixs.backend.feature_flag_snapshot_codec import (
            encode_feature_flag_source_snapshot,
        )
        from pixs.backend.models import FeatureFlagSourceSnapshotRecord as Record
        from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule
        import pixs.kernel.feature_flag_sources as source_module
        from pixs.kernel.feature_flag_sources import (
            FeatureFlagSourceSnapshot,
            evaluate_feature_flag_source_snapshot,
        )
        from pixs.kernel.feature_flags import (
            FeatureFlagAssignment,
            FeatureFlagDefinition,
            FeatureFlagEvaluationContext,
        )

        assert "pixs.backend.models" in sys.modules

        write_guard_targets = (
            (connection, "cursor", ()),
            (Record, "save", ()),
            (Record, "delete", ()),
            (Record.objects, "create", ()),
            (Record.objects, "update", ()),
            (Record.objects, "bulk_create", ()),
            (Record.objects, "get_or_create", ()),
        )
        write_guards = [
            mock.Mock(side_effect=AssertionError("forbidden write"))
            for _ in write_guard_targets
        ]
        guard_targets = base_guard_targets + write_guard_targets
        guards = base_guards + write_guards

        for (target, name, args), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))

        for (target, name, args), guard in zip(guard_targets, guards):
            try:
                getattr(target, name)(*args)
            except AssertionError:
                pass
            else:
                raise AssertionError("garde inactive")
            assert guard.call_count == 1
            guard.reset_mock()

        config = apps.get_app_config("backend")
        assert config.name == "pixs.backend"
        assert config.label == "backend"
        assert Record._meta.app_label == "backend"
        assert [model.__name__ for model in apps.get_models()] == [
            "FeatureFlagSourceSnapshotRecord",
            "JobRecord",
        ]
        assert [field.name for field in Record._meta.fields] == [
            "configuration_version",
            "snapshot",
        ]
        primary_key = Record._meta.pk
        assert primary_key.name == "configuration_version"
        assert primary_key.primary_key is True
        assert primary_key.get_internal_type() == "TextField"
        assert Record._meta.get_field("snapshot").get_internal_type() == "JSONField"

        migration_key = ("backend", "0001_feature_flag_source_snapshot")
        migration_loader = MigrationLoader(None, ignore_no_migrations=True)
        assert migration_key in migration_loader.disk_migrations
        assert migration_key in migration_loader.graph.nodes

        initial_migration = migration_loader.disk_migrations[migration_key]
        assert initial_migration.initial is True
        assert initial_migration.dependencies == []
        assert len(initial_migration.operations) == 1

        create_model = initial_migration.operations[0]
        assert isinstance(create_model, CreateModel)
        assert create_model.name == Record.__name__
        assert hasattr(create_model, "database_backwards")
        assert create_model.reversible is True
        assert all(
            isinstance(operation, CreateModel)
            for operation in initial_migration.operations
        )

        loaded_state = migration_loader.project_state()
        current_state = ProjectState.from_apps(apps)
        autodetector = MigrationAutodetector(
            loaded_state,
            current_state,
            questioner=NonInteractiveMigrationQuestioner(
                specified_apps={"backend"},
                dry_run=True,
            ),
        )
        assert autodetector.changes(graph=migration_loader.graph) == {}

        _CFG = "cfg-integration"
        _FALLBACK_CFG = "cfg-fallback"
        _FLAG = "web.integration"
        _PAST = "2025-01-01T00:00:00Z"
        _FAR = "2099-01-01T00:00:00Z"
        _USE_KINDS = (
            "NON_SENSITIVE",
            "PERMISSION",
            "MUTATION",
            "PROTECTED_DATA",
            "CONTRACT",
        )

        def definition(**overrides):
            values = {
                "flag_id": _FLAG,
                "flag_version": "v1",
                "owner_component": "web-main",
                "purpose": "Intégration PostgreSQL",
                "value_schema": "BOOLEAN",
                "default_value": False,
                "targeting_dimensions": ("INSTALLATION", "TENANT"),
                "cohort_key": None,
                "prerequisites": (),
                "fallback_policy": "DENY",
                "expires_at": _FAR,
                "audit_policy": "standard",
            }
            values.update(overrides)
            return FeatureFlagDefinition(**values)

        def assignment(selector, selector_value, value, version):
            return FeatureFlagAssignment(
                flag_id=_FLAG,
                selector=selector,
                selector_value=selector_value,
                value=value,
                valid_from=_PAST,
                valid_until=_FAR,
                configuration_version=version,
                updated_by="administrator.1",
            )

        c2_snapshot = FeatureFlagSourceSnapshot(
            _CFG,
            (definition(),),
            (
                assignment("INSTALLATION", "install-a", True, _CFG),
                assignment("TENANT", "tenant-a", False, _CFG),
            ),
            (),
        )
        fallback_snapshot = FeatureFlagSourceSnapshot(
            _FALLBACK_CFG,
            (definition(fallback_policy="DEFAULT"),),
            (),
            (),
        )

        def loaded_record(version, document):
            record = Record()
            record.configuration_version = version
            record.snapshot = document
            return record

        c2_document = encode_feature_flag_source_snapshot(c2_snapshot)
        c2_calls = []

        def c2_get(**kwargs):
            c2_calls.append(dict(kwargs))
            return loaded_record(_CFG, c2_document)

        with mock.patch.object(Record.objects, "get", side_effect=c2_get):
            loaded_c2 = loader.load_feature_flag_source_snapshot(_CFG)

        assert c2_calls == [{"pk": _CFG}]
        assert loaded_c2 == c2_snapshot

        composition_calls = []
        real_composition = source_module.evaluate_feature_flag_assignments_with_cohort
        def composition_spy(*args, **kwargs):
            composition_calls.append((args, kwargs))
            return real_composition(*args, **kwargs)
        stack.enter_context(mock.patch.object(
            source_module, "evaluate_feature_flag_assignments_with_cohort",
            side_effect=composition_spy,
        ))

        c2_context = FeatureFlagEvaluationContext(
            "install-a",
            None,
            "tenant-a",
            None,
            _PAST,
        )
        for use_kind in _USE_KINDS:
            evaluation = evaluate_feature_flag_source_snapshot(
                loaded_c2,
                _CFG,
                _FLAG,
                c2_context,
                use_kind,
            )
            assert (evaluation.status, evaluation.value) == ("SELECTED", False)
            assert not hasattr(evaluation, "permission")

        fallback_document = encode_feature_flag_source_snapshot(fallback_snapshot)
        fallback_calls = []

        def fallback_get(**kwargs):
            fallback_calls.append(dict(kwargs))
            return loaded_record(_FALLBACK_CFG, fallback_document)

        with mock.patch.object(Record.objects, "get", side_effect=fallback_get):
            loaded_fallback = loader.load_feature_flag_source_snapshot(
                _FALLBACK_CFG
            )

        assert fallback_calls == [{"pk": _FALLBACK_CFG}]
        assert loaded_fallback == fallback_snapshot

        fallback_context = FeatureFlagEvaluationContext(
            "absent",
            None,
            "absent",
            None,
            _PAST,
        )
        non_sensitive = evaluate_feature_flag_source_snapshot(
            loaded_fallback,
            _FALLBACK_CFG,
            _FLAG,
            fallback_context,
            "NON_SENSITIVE",
        )
        assert (non_sensitive.status, non_sensitive.value) == ("DEFAULT", False)

        for use_kind in _USE_KINDS[1:]:
            refused = evaluate_feature_flag_source_snapshot(
                loaded_fallback,
                _FALLBACK_CFG,
                _FLAG,
                fallback_context,
                use_kind,
            )
            assert (refused.status, refused.value) == ("REFUSED", None)
            assert not hasattr(refused, "permission")

        def load_synthetic(snapshot):
            document = encode_feature_flag_source_snapshot(snapshot)
            calls = []
            def get_record(**kwargs):
                calls.append(kwargs)
                return loaded_record(snapshot.configuration_version, document)
            with mock.patch.object(Record.objects, "get", side_effect=get_record):
                result = loader.load_feature_flag_source_snapshot(snapshot.configuration_version)
            assert calls == [{"pk": snapshot.configuration_version}]
            assert result == snapshot
            return result

        for threshold in (10000, 0):
            version = "cfg-cohort-" + str(threshold)
            cohort_snapshot = FeatureFlagSourceSnapshot(
                version, (definition(cohort_key="rollout", fallback_policy="DEFAULT"),),
                (assignment("TENANT", "tenant-a", False, version),),
                (FeatureFlagCohortRule("rollout", "TENANT", threshold, version),),
            )
            loaded = load_synthetic(cohort_snapshot)
            for use_kind in _USE_KINDS:
                evaluation = evaluate_feature_flag_source_snapshot(
                    loaded, version, _FLAG, c2_context, use_kind,
                )
                expected = ("SELECTED", False) if threshold == 10000 else (
                    ("DEFAULT", False) if use_kind == "NON_SENSITIVE" else ("REFUSED", None)
                )
                assert (evaluation.status, evaluation.value) == expected

        expired_version = "cfg-expired"
        expired_snapshot = FeatureFlagSourceSnapshot(
            expired_version,
            (definition(fallback_policy="DEFAULT", expires_at="2026-01-01T00:00:00Z"),),
            (assignment("TENANT", "tenant-a", True, expired_version),), (),
        )
        loaded_expired = load_synthetic(expired_snapshot)
        expired_context = FeatureFlagEvaluationContext(
            "install-a", None, "tenant-a", None, "2026-06-01T00:00:00Z",
        )
        for use_kind in _USE_KINDS:
            evaluation = evaluate_feature_flag_source_snapshot(
                loaded_expired, expired_version, _FLAG, expired_context, use_kind,
            )
            expected = ("DEFAULT", False) if use_kind == "NON_SENSITIVE" else ("REFUSED", None)
            assert (evaluation.status, evaluation.value) == expected

        deny_version = "cfg-deny"
        loaded_deny = load_synthetic(FeatureFlagSourceSnapshot(
            deny_version, (definition(fallback_policy="DENY"),), (), (),
        ))
        for use_kind in _USE_KINDS:
            evaluation = evaluate_feature_flag_source_snapshot(
                loaded_deny, deny_version, _FLAG, fallback_context, use_kind,
            )
            assert (evaluation.status, evaluation.value) == ("REFUSED", None)
        assert len(composition_calls) == 30
        refused_version = evaluate_feature_flag_source_snapshot(
            loaded_c2, "incompatible", _FLAG, c2_context, "NON_SENSITIVE",
        )
        assert (refused_version.status, refused_version.value) == ("REFUSED", None)
        assert len(composition_calls) == 30

        assert connection.connection is None
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("FEATURE_FLAG_POSTGRES_SOURCE_SAFE_INTEGRATION_OK")
    """
).strip()


class FeatureFlagPostgresSourceSafeIntegrationTests(unittest.TestCase):
    def test_backend_app_model_initial_migration_and_simulated_source(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


import uuid
from contextlib import contextmanager
from pathlib import Path


class _ControlledCleanupCaseFailure(Exception):
    """Échec privé distinguant le cas volontaire d’un incident imprévu."""


_PG_HOST = "127.0.0.1"
_PG_PORT = 5432
_CONNECT_TIMEOUT_SECONDS = 2
_STATEMENT_TIMEOUT_MS = 1500
_LOCK_TIMEOUT_MS = 1500
_ENV_READ_LIMIT = 65537
_MIGRATION_NAME = "0001_feature_flag_source_snapshot"


def _closed_result():
    return {
        "ok": False,
        "migration_applied": False,
        "roundtrip": False,
        "single_select": False,
        "refusals": False,
        "migration_reversed": False,
        "cleanup_success": False,
        "cleanup_failure_case": False,
        "connections_closed": False,
        "phase": "INIT",
        "reason": "NONE",
    }


def _set_phase(result, phase, reason="NONE"):
    result["phase"] = phase
    result["reason"] = reason


def _safe_schema_name():
    name = f"feature_flag_{uuid.uuid4().hex[:16]}"
    if not name.isidentifier():
        raise RuntimeError("invalid synthetic schema identifier")
    return name


def _pg_options(search_path=None):
    options = (
        f"-c statement_timeout={_STATEMENT_TIMEOUT_MS} "
        f"-c lock_timeout={_LOCK_TIMEOUT_MS}"
    )
    if search_path is not None:
        options = f"{options} -c search_path={search_path}"
    return options


def _read_project_env(root_str):
    from tests.integration.test_pg_connectivity_integration import _parse_env_text

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
        return _parse_env_text(text)
    except Exception:
        return None


@contextmanager
def _managed_pg_connection(database, user, password, connection_refs):
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
            options=_pg_options(),
        )
        if connection_refs is not None:
            connection_refs.append(connection)
        yield connection
    finally:
        if connection is not None:
            try:
                if not connection.closed:
                    connection.close()
            except Exception:
                if connection_refs is not None:
                    connection_refs.append("_CONNECTION_CLOSE_FAILED")


def _schema_exists(connection, schema_name):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (schema_name,),
        )
        return bool(cursor.fetchone()[0])
    finally:
        cursor.close()


def _table_exists(connection, schema_name, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM pg_class AS class
                JOIN pg_namespace AS namespace
                  ON namespace.oid = class.relnamespace
                WHERE namespace.nspname = %s
                  AND class.relname = %s
            )
            """,
            (schema_name, table_name),
        )
        return bool(cursor.fetchone()[0])
    finally:
        cursor.close()


def _create_schema(connection, schema_name):
    from psycopg import errors, sql

    try:
        if _schema_exists(connection, schema_name):
            return False, "SCHEMA_COLLISION"
    except Exception:
        return False, "SCHEMA_PROBE_FAILED"

    created = False
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name))
            )
            created = True
    except errors.DuplicateSchema:
        return False, "SCHEMA_COLLISION"
    except errors.InsufficientPrivilege:
        return created, "SCHEMA_PERMISSION_DENIED"
    except Exception:
        return created, "SCHEMA_CREATE_FAILED"

    try:
        if _schema_exists(connection, schema_name):
            return True, "NONE"
        return True, "SCHEMA_CREATE_UNPROVED"
    except Exception:
        return True, "SCHEMA_CREATE_UNPROVED"


def _drop_schema_if_owned(connection, schema_name, owned):
    from psycopg import sql

    if not owned:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema_name))
            )
    except Exception:
        return False
    return not _schema_exists(connection, schema_name)


def _quote_search_path(connection, schema_name):
    from psycopg import sql

    return sql.Identifier(schema_name).as_string(connection)


def _synthetic_snapshot_document():
    import json

    from pixs.backend.feature_flag_snapshot_codec import (
        encode_feature_flag_source_snapshot,
    )
    from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule
    from pixs.kernel.feature_flag_sources import FeatureFlagSourceSnapshot
    from pixs.kernel.feature_flags import (
        FeatureFlagAssignment,
        FeatureFlagDefinition,
    )

    configuration_version = "cfg-real-" + uuid.uuid4().hex[:12]
    flag_id = "web.dark_mode"
    past = "2025-01-01T00:00:00Z"
    far = "2099-01-01T00:00:00Z"

    definition = FeatureFlagDefinition(
        flag_id=flag_id,
        flag_version="v1",
        owner_component="web-main",
        purpose="Validation PostgreSQL",
        value_schema="BOOLEAN",
        default_value=False,
        targeting_dimensions=("INSTALLATION", "TENANT"),
        cohort_key="beta",
        prerequisites=(),
        fallback_policy="DENY",
        expires_at=far,
        audit_policy="standard",
    )
    assignment = FeatureFlagAssignment(
        flag_id=flag_id,
        selector="TENANT",
        selector_value="tenant-" + uuid.uuid4().hex[:8],
        value=False,
        valid_from=past,
        valid_until=far,
        configuration_version=configuration_version,
        updated_by="administrator-" + uuid.uuid4().hex[:8],
    )
    rule = FeatureFlagCohortRule(
        cohort_key="beta",
        subject_dimension="TENANT",
        threshold_basis_points=10000,
        configuration_version=configuration_version,
    )
    snapshot = FeatureFlagSourceSnapshot(
        configuration_version,
        (definition,),
        (assignment,),
        (rule,),
    )
    document = json.loads(
        json.dumps(encode_feature_flag_source_snapshot(snapshot))
    )
    return snapshot, document, flag_id, past, far


def _make_sql_category_counter(counter):
    def wrapper(execute, sql, params, many, context):
        normalized = " ".join(sql.strip().upper().split())
        first_word = normalized.split(" ", 1)[0]
        if first_word == "SELECT":
            counter["select"] += 1
        elif first_word == "INSERT":
            counter["insert"] += 1
        elif first_word == "UPDATE":
            counter["update"] += 1
        elif first_word == "DELETE":
            counter["delete"] += 1
        elif first_word in {"CREATE", "DROP", "ALTER"}:
            counter["ddl"] += 1
        return execute(sql, params, many, context)

    return wrapper


def _run_real_success_case(database, user, password, result, connection_refs):
    import django
    from django.conf import settings
    from django.db import connection, connections, transaction
    from django.db.migrations.executor import MigrationExecutor

    schema_name = _safe_schema_name()
    schema_owned = False
    schema_cleanup_done = False
    search_path = None
    configured = False
    completed = False

    def _mark_failure(code):
        current = result["reason"]
        if code == "NONE" or not isinstance(code, str) or not code:
            return
        if current == "NONE":
            result["reason"] = code
        else:
            result["reason"] = f"{current}_{code}"

    try:
        with _managed_pg_connection(database, user, password, connection_refs) as admin_connection:
            schema_owned, schema_reason = _create_schema(admin_connection, schema_name)
            if not schema_owned:
                _mark_failure(schema_reason)
            elif schema_reason != "NONE":
                _mark_failure(schema_reason)
            else:
                search_path = _quote_search_path(admin_connection, schema_name)

        if search_path is None:
            _mark_failure("SETTINGS_SKIPPED")
        elif settings.configured:
            _mark_failure("DJANGO_SETTINGS_ALREADY_CONFIGURED")
        else:
            settings.configure(
                DEFAULT_CHARSET="utf-8",
                INSTALLED_APPS=["pixs.backend"],
                SECRET_KEY="real-test-synthetic-only",
                DATABASES={
                    "default": {
                        "ENGINE": "django.db.backends.postgresql",
                        "NAME": database,
                        "USER": user,
                        "PASSWORD": password,
                        "HOST": _PG_HOST,
                        "PORT": str(_PG_PORT),
                        "OPTIONS": {"options": _pg_options(search_path), "connect_timeout": _CONNECT_TIMEOUT_SECONDS},
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
            configured = True
            django.setup()

            from pixs.backend.feature_flag_postgres_source import (
                FeatureFlagSourceLoadError,
                load_feature_flag_source_snapshot,
            )
            from pixs.backend.models import FeatureFlagSourceSnapshotRecord as Record
            from pixs.kernel.feature_flag_sources import (
                evaluate_feature_flag_source_snapshot,
            )
            from pixs.kernel.feature_flags import FeatureFlagEvaluationContext

            executor = MigrationExecutor(connection)
            executor.migrate([("backend", _MIGRATION_NAME)])
            result["migration_applied"] = True

            snapshot, document, flag_id, past, far = _synthetic_snapshot_document()
            table_name = Record._meta.db_table

            if not _table_exists(connection, schema_name, table_name):
                _mark_failure("TABLE_MISSING")
            else:
                Record.objects.create(
                    configuration_version=snapshot.configuration_version,
                    snapshot=document,
                )

                counter = {
                    "select": 0,
                    "insert": 0,
                    "update": 0,
                    "delete": 0,
                    "ddl": 0,
                }
                with connection.execute_wrapper(_make_sql_category_counter(counter)):
                    loaded = load_feature_flag_source_snapshot(
                        snapshot.configuration_version
                    )

                if (
                    loaded != snapshot
                    or loaded.configuration_version != snapshot.configuration_version
                ):
                    _mark_failure("ROUNDTRIP_FAILED")
                elif not (
                    counter["select"] == 1
                    and counter["insert"] == 0
                    and counter["update"] == 0
                    and counter["delete"] == 0
                    and counter["ddl"] == 0
                ):
                    _mark_failure("READ_CATEGORY_COUNTS_INVALID")
                elif len(loaded.assignments) != 1:
                    _mark_failure("LOADER_ASSIGNMENTS_INVALID")
                else:
                    result["roundtrip"] = True
                    result["single_select"] = True

                    evaluation_context = FeatureFlagEvaluationContext(
                        None,
                        None,
                        loaded.assignments[0].selector_value,
                        None,
                        past,
                    )
                    evaluation = evaluate_feature_flag_source_snapshot(
                        loaded,
                        loaded.configuration_version,
                        flag_id,
                        evaluation_context,
                        "PERMISSION",
                    )
                    if (evaluation.status, evaluation.value) != ("SELECTED", False):
                        _mark_failure("LOADED_SNAPSHOT_COMPOSITION_FAILED")
                    else:
                        divergence_key = "divergent-" + uuid.uuid4().hex[:12]
                        invalid_document = dict(document)
                        invalid_document["configuration_version"] = (
                            "invalid-" + uuid.uuid4().hex[:12]
                        )
                        invalid_document.pop("definitions", None)
                        absent_key = "absent-" + uuid.uuid4().hex[:12]
                        fixed_error = "Source de fanions indisponible"
                        refusal_failure = None

                        def expect_refusal(operation):
                            try:
                                operation()
                            except FeatureFlagSourceLoadError as caught:
                                return (
                                    str(caught) == fixed_error
                                    and caught.__cause__ is None
                                    and caught.__suppress_context__ is True
                                )
                            return False

                        with transaction.atomic():
                            try:
                                Record.objects.create(
                                    configuration_version=divergence_key,
                                    snapshot=document,
                                )
                                if not expect_refusal(
                                    lambda: load_feature_flag_source_snapshot(
                                        divergence_key
                                    )
                                ):
                                    refusal_failure = "DIVERGENCE_NOT_REFUSED"
                                else:
                                    stored = Record.objects.get(
                                        pk=snapshot.configuration_version
                                    )
                                    stored.snapshot = invalid_document
                                    stored.save()
                                    if not expect_refusal(
                                        lambda: load_feature_flag_source_snapshot(
                                            snapshot.configuration_version
                                        )
                                    ):
                                        refusal_failure = "INVALID_DOCUMENT_NOT_REFUSED"
                                    elif not expect_refusal(
                                        lambda: load_feature_flag_source_snapshot(
                                            absent_key
                                        )
                                    ):
                                        refusal_failure = "ABSENT_VERSION_NOT_REFUSED"
                            except Exception:
                                refusal_failure = "REFUSAL_SETUP_FAILED"

                            transaction.set_rollback(True)

                        if refusal_failure is not None:
                            _mark_failure(refusal_failure)
                        else:
                            result["refusals"] = True

                            reverse_executor = MigrationExecutor(connection)
                            reverse_executor.migrate([("backend", None)])

                            if _table_exists(connection, schema_name, table_name):
                                _mark_failure("TABLE_STILL_PRESENT")
                            else:
                                result["migration_reversed"] = True
                                completed = True

    except Exception:
        _mark_failure("UNEXPECTED")

    finally:
        if configured:
            try:
                for alias in connections:
                    wrapper = connections[alias]
                    if wrapper.connection is not None:
                        connection_refs.append(wrapper.connection)
                    wrapper.close()
            except Exception:
                _mark_failure("ORM_CLOSE_FAILED")

        if schema_owned and not schema_cleanup_done:
            try:
                with _managed_pg_connection(
                    database,
                    user,
                    password,
                    connection_refs,
                ) as cleanup_connection:
                    schema_cleanup_done = _drop_schema_if_owned(
                        cleanup_connection,
                        schema_name,
                        schema_owned,
                    )
            except Exception:
                schema_cleanup_done = False
                _mark_failure("CLEANUP_FAILED")

            if not schema_cleanup_done:
                _mark_failure("CLEANUP_FAILED")

        result["cleanup_success"] = bool(schema_owned and schema_cleanup_done)

        if result["reason"] == "NONE":
            _set_phase(result, "COMPLETE", "NONE")
        else:
            result["phase"] = "COMPLETE"

    return bool(
        completed
        and result["reason"] == "NONE"
        and result["cleanup_success"]
    )


def _run_controlled_failure_case(database, user, password, result, connection_refs):
    schema_name = _safe_schema_name()
    schema_owned = False
    schema_cleanup_done = False
    controlled_raised = False

    def _mark_failure(code):
        current = result["reason"]
        if code == "NONE" or not isinstance(code, str) or not code:
            return
        if current == "NONE":
            result["reason"] = code
        else:
            result["reason"] = f"{current}_{code}"

    try:
        with _managed_pg_connection(database, user, password, connection_refs) as admin_connection:
            schema_owned, schema_reason = _create_schema(admin_connection, schema_name)
            if not schema_owned:
                _mark_failure(schema_reason)
            elif schema_reason != "NONE":
                _mark_failure(schema_reason)
            else:
                controlled_raised = True
                raise _ControlledCleanupCaseFailure()
    except _ControlledCleanupCaseFailure:
        controlled_raised = True
    except Exception:
        _mark_failure("UNEXPECTED")

    finally:
        if schema_owned and not schema_cleanup_done:
            try:
                with _managed_pg_connection(
                    database,
                    user,
                    password,
                    connection_refs,
                ) as cleanup_connection:
                    schema_cleanup_done = _drop_schema_if_owned(
                        cleanup_connection,
                        schema_name,
                        schema_owned,
                    )
            except Exception:
                schema_cleanup_done = False
                _mark_failure("CLEANUP_FAILED")

            if not schema_cleanup_done:
                _mark_failure("CLEANUP_FAILED")

        case_success = bool(
            controlled_raised
            and schema_owned
            and schema_cleanup_done
            and result["reason"] == "NONE"
        )
        result["cleanup_failure_case"] = case_success

        if case_success:
            _set_phase(result, "CLEANUP_CASE_COMPLETE", "NONE")
        else:
            result["phase"] = "CLEANUP_CASE_COMPLETE"

    return result["cleanup_failure_case"]


def run_real_postgres_source(root_str):
    import io
    import logging
    from contextlib import redirect_stderr, redirect_stdout

    result = _closed_result()
    connection_refs = []
    private_stdout = io.StringIO()
    private_stderr = io.StringIO()
    previous_logging_disable = logging.root.manager.disable
    logging.disable(logging.CRITICAL)

    def _combine_failure(code):
        current = result["reason"]
        if code == "NONE" or not isinstance(code, str) or not code:
            return
        if current == "NONE":
            result["reason"] = code
        else:
            result["reason"] = f"{current}_{code}"

    def _finalize():
        all_closed = True
        for connection in connection_refs:
            if not hasattr(connection, "closed"):
                all_closed = False
                continue
            try:
                if not connection.closed:
                    all_closed = False
            except Exception:
                all_closed = False

        result["connections_closed"] = all_closed
        if not all_closed:
            _combine_failure("CONNECTION_CLOSE_FAILED")

        result["ok"] = bool(
            result["migration_applied"]
            and result["roundtrip"]
            and result["single_select"]
            and result["refusals"]
            and result["migration_reversed"]
            and result["cleanup_success"]
            and result["cleanup_failure_case"]
            and all_closed
            and result["reason"] == "NONE"
        )

        if result["ok"]:
            _set_phase(result, "COMPLETE", "NONE")
        else:
            result["phase"] = "COMPLETE"
            if result["reason"] == "NONE":
                result["reason"] = "CASE_INCOMPLETE"

    try:
        with (
            redirect_stdout(private_stdout),
            redirect_stderr(private_stderr),
        ):
            if type(root_str) is not str or not root_str:
                _combine_failure("ROOT_INVALID")
            else:
                try:
                    resolved_root = Path(root_str).resolve()
                except Exception:
                    resolved_root = None

                if str(resolved_root) != "/home/devops/datas/pixs":
                    _combine_failure("ROOT_MISMATCH")
                else:
                    found_env = _read_project_env(root_str)
                    if not isinstance(found_env, dict):
                        _combine_failure("ENV_REFUSED")
                    else:
                        required = ("PG_DATABASE", "PG_USERNAME", "PG_PASSWORD")
                        values = tuple(found_env.get(name) for name in required)
                        if any(
                            not isinstance(value, str) or not value
                            for value in values
                        ):
                            _combine_failure("ENV_INCOMPLETE")
                        else:
                            database, user, password = values
                            del required, values, found_env

                            _set_phase(result, "ENV_READY")
                            first_case_ok = _run_real_success_case(
                                database,
                                user,
                                password,
                                result,
                                connection_refs,
                            )
                            if first_case_ok and result["reason"] == "NONE":
                                _run_controlled_failure_case(
                                    database, user, password, result, connection_refs,
                                )

                            del database, user, password

    except BaseException:
        _combine_failure("UNEXPECTED")
    finally:
        logging.disable(previous_logging_disable)

    _finalize()
    return result


if __name__ == "__main__":
    unittest.main()
