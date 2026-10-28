"""Harnais PG reel modes C08 : namespace jetable, migrations reelles, preuve de nettoyage.

Perimetre : Auth DJANGO_REQUIRED_APPS + PixsCoreConfig + PixsBackendConfig
explicites, trois aliases default/peer/contender, processus frais, schema
possede et OID/proprietaire verifies avant destruction, public intact.
Aucun scenario importe ni appele ici : le harnais recoit callback et
l'execute en phase2 seulement. Aucune fabrication AuthContext/attestation.
Artefacts eventuels sous output/tests/c08-modes uniquement, jamais /tmp.
Le graphe backend 0001-0016 est prepare dans ce seul schema jetable ;
son application ne qualifie pas les fonctionnalites Bulk/C09 correspondantes.
Secrets PG locaux au processus, masques via core_pg_test_support.
"""
from __future__ import annotations

import re
import secrets
from pathlib import Path

EXPECTED_ROOT = "/home/devops/datas/pixs"
NS_PATTERN = re.compile(r"c08_[0-9a-f]{16}")
ARTIFACT_REL = Path("output") / "tests" / "c08-modes"

AUTH_ORIGIN = None
AUTH_TARGET = "0.1.0"
CORE_ORIGIN = None
CORE_TARGET = "0.1.0"
CORE_AUDIT_TARGET = ("pixs_core", "0002_core_audit")
CORE_IDEMPOTENCE_TARGET = ("pixs_core", "0003_core_idempotence")
BACKEND_TARGET = ("backend", "0016_c08_mode_storage")
BACKEND_EXPECTED_GRAPH = ('0001_feature_flag_source_snapshot', '0002_job_record', '0003_bulk_operation_record', '0004_bulk_runtime_persistence', '0005_bulk_admission_identity', '0006_bulk_command_idempotency', '0007_bulk_event_envelope', '0008_bulk_inbox_receipt', '0009_bulk_validation_report', '0010_bulk_export_manifest', '0011_bulk_outbox_publication', '0012_c09_jobs', '0013_c09_events_scheduler', '0014_c10_initial_governance_receipts', '0015_c08_installation_result', '0016_c08_mode_storage')
BACKEND_REQUIRED = (
    "0014_c10_initial_governance_receipts",
    "0015_c08_installation_result",
    "0016_c08_mode_storage",
)
BACKEND_REQUIRED_TABLES = frozenset({
    "backend_c10receiptrecord",
    "backend_c08installationresultrecord",
    "backend_c08modesnapshotrecord",
    "backend_c08modeoperationreceiptrecord",
})

__all__ = ["EXPECTED_ROOT", "NS_PATTERN", "ARTIFACT_REL", "run_in_modes_schema"]


def _public_tables(admin_connection):
    with admin_connection.cursor() as cursor:
        cursor.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY 1;"
        )
        rows = cursor.fetchall()
    names: list[str] = []
    for row in rows:
        if type(row[0]) is not str or row[0] == "":
            raise RuntimeError("PUBLIC_INVENTORY_UNPROVED")
        names.append(row[0])
    return names


def run_in_modes_schema(root_str, callback, expected_cases):
    import core_pg_test_support as core

    out = {
        "real_pg": False,
        "code": "MODES_PG_FAILED",
        "failure_type": "NONE",
        "failure_frames": [],
        "pg_version_num": "",
        "django_version": "",
        "cases": {},
        "migration": False,
        "core_migration": False,
        "core_applied": [],
        "backend_migration": False,
        "backend_applied": [],
        "backend_plan": [],
        "namespace": False,
        "cleanup": False,
        "conns_closed": False,
        "artifact_dir": str(ARTIFACT_REL),
    }
    refs: list = []
    failures: list[str] = []
    private_values: list[str] = []
    env = None
    namespace = None
    proof = None
    attempted = False
    configured = False
    callback_ok = False
    before_public: list[str] | None = None
    with core.mask_output():
        try:
            if type(root_str) is not str or str(Path(root_str).resolve()) != EXPECTED_ROOT:
                raise ValueError("ROOT_INVALID")
            if not callable(callback):
                raise ValueError("CALLBACK_INVALID")
            if type(expected_cases) is not tuple or len(expected_cases) == 0:
                raise ValueError("CASES_INVALID")
            for key in expected_cases:
                if type(key) is not str or key == "":
                    raise ValueError("CASES_INVALID")
            if len(set(expected_cases)) != len(expected_cases):
                raise ValueError("CASES_INVALID")
            from django.conf import settings as dj_settings

            if dj_settings.configured:
                raise RuntimeError("SETTINGS_PREEXISTING")
            env = core.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_INVALID")
            private_values = list(env.values())
            namespace = "c08_" + secrets.token_hex(8)
            if NS_PATTERN.fullmatch(namespace) is None:
                raise RuntimeError("NAMESPACE_INVALID")
            artifact_path = Path(root_str) / ARTIFACT_REL
            artifact_path.mkdir(parents=True, exist_ok=True)
            out["artifact_dir"] = str(ARTIFACT_REL)
            from psycopg import sql as pg_sql

            args = (
                env["PG_HOST"],
                env["PG_PORT"],
                env["PG_DATABASE"],
                env["PG_USERNAME"],
                env["PG_PASSWORD"],
                refs,
                failures,
            )
            with core.managed_pg_connection(*args) as admin:
                before_public = _public_tables(admin)
                with admin.transaction():
                    with admin.cursor() as cursor:
                        cursor.execute(
                            "SELECT oid FROM pg_roles WHERE rolname=current_user;"
                        )
                        role_row = cursor.fetchone()
                        if role_row is None:
                            raise RuntimeError("OWNERSHIP_UNPROVED")
                        role_oid = int(role_row[0])
                        cursor.execute(
                            pg_sql.SQL("CREATE SCHEMA {}").format(
                                pg_sql.Identifier(namespace)
                            )
                        )
                        attempted = True
                        cursor.execute(
                            "SELECT oid,nspowner FROM pg_namespace WHERE nspname=%s;",
                            (namespace,),
                        )
                        row = cursor.fetchone()
                        if row is None or int(row[1]) != role_oid:
                            raise RuntimeError("OWNERSHIP_UNPROVED")
                        proof = (int(row[0]), int(row[1]), role_oid)
                quoted = pg_sql.Identifier(namespace).as_string(admin)
            options = core.pg_options(search_path_quoted=quoted)
            databases = {
                alias: {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": env["PG_DATABASE"],
                    "USER": env["PG_USERNAME"],
                    "PASSWORD": env["PG_PASSWORD"],
                    "HOST": env["PG_HOST"],
                    "PORT": env["PG_PORT"],
                    "OPTIONS": {"options": options, "connect_timeout": 2},
                    "CONN_MAX_AGE": 0,
                    "ATOMIC_REQUESTS": False,
                    "AUTOCOMMIT": True,
                }
                for alias in ("default", "peer", "contender")
            }
            from pixs.auth.apps import DJANGO_REQUIRED_APPS

            selected_apps = DJANGO_REQUIRED_APPS + (
                "pixs.backend.apps.PixsCoreConfig",
                "pixs.backend.apps.PixsBackendConfig",
            )
            dj_settings.configure(
                INSTALLED_APPS=selected_apps,
                DATABASES=databases,
                USE_TZ=True,
                TIME_ZONE="UTC",
                LOGGING_CONFIG=None,
            )
            configured = True
            import django

            django.setup()
            from django.apps import apps as dj_apps
            from django.db import connections, transaction
            from django.db.migrations.executor import MigrationExecutor
            from django.db.migrations.recorder import MigrationRecorder

            connection = connections["default"]
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT current_schema(),current_schemas(false),"
                    "current_setting('server_version_num');"
                )
                schema, path, version = cursor.fetchone()
                cursor.execute(
                    "SELECT oid,nspowner FROM pg_namespace WHERE nspname=%s;",
                    (namespace,),
                )
                observed = cursor.fetchone()
            if schema != namespace or list(path) != [namespace]:
                raise RuntimeError("NAMESPACE_UNPROVED")
            if observed is None:
                raise RuntimeError("NAMESPACE_UNPROVED")
            if proof is not None and (int(observed[0]), int(observed[1])) != proof[:2]:
                raise RuntimeError("NAMESPACE_CHANGED")
            if type(version) is not str or re.fullmatch(r"[0-9]+", version) is None:
                raise RuntimeError("VERSION_UNPROVED")
            out["namespace"] = True
            out["pg_version_num"] = version
            out["django_version"] = django.get_version()
            auth_tables = {
                model._meta.db_table
                for model in dj_apps.get_app_config("pixs_auth").get_models()
            }
            if len(auth_tables) != 11:
                raise RuntimeError("MODEL_SET_INVALID")
            from pixs.auth.migration_lock import run_auth_initial

            if run_auth_initial("default", origin=AUTH_ORIGIN, target=AUTH_TARGET) != "applied":
                raise RuntimeError("MIGRATION_CONTRACT_INVALID")
            with connection.cursor() as cursor:
                current_tables = set(connection.introspection.table_names(cursor))
            if {name for name in current_tables if name.startswith("pixs_auth_")} != auth_tables:
                raise RuntimeError("TABLE_SET_INVALID")
            if "django_migrations" not in current_tables:
                raise RuntimeError("RECORDER_MISSING")
            if ("pixs_auth", "0001_auth_initial") not in MigrationRecorder(
                connection
            ).applied_migrations():
                raise RuntimeError("MIGRATION_UNPROVED")
            out["migration"] = True
            from pixs.core.migration_lock import run_core_initial

            if run_core_initial("default", origin=CORE_ORIGIN, target=CORE_TARGET) != "applied":
                raise RuntimeError("CORE_INITIAL_UNPROVED")
            loader = MigrationExecutor(connection).loader
            if CORE_AUDIT_TARGET not in loader.graph.nodes:
                raise RuntimeError(
                    "BACKEND_CONTRACT_MISSING:src/pixs/core/migrations/0002_core_audit.py"
                )
            if CORE_IDEMPOTENCE_TARGET not in loader.graph.nodes:
                raise RuntimeError(
                    "BACKEND_CONTRACT_MISSING:src/pixs/core/migrations/0003_core_idempotence.py"
                )
            core_plan = loader.graph.forwards_plan(CORE_IDEMPOTENCE_TARGET)
            expected_core_applied = sorted(
                name for app, name in core_plan if app == "pixs_core"
            )
            if "0001_core_initial" not in expected_core_applied:
                raise RuntimeError("CORE_PLAN_UNPROVED")
            historical = loader.project_state([CORE_IDEMPOTENCE_TARGET]).apps.get_app_config(
                "pixs_core"
            )
            expected_core_tables = {
                model._meta.db_table
                for model in historical.get_models(
                    include_auto_created=True
                )
                if model._meta.managed and not model._meta.proxy
            }
            if not expected_core_tables:
                raise RuntimeError("CORE_STATE_UNPROVED")
            with transaction.atomic(using="default", durable=True):
                MigrationExecutor(connection).migrate([CORE_IDEMPOTENCE_TARGET])
            with connection.cursor() as cursor:
                core_tables = {
                    name
                    for name in connection.introspection.table_names(cursor)
                    if name.startswith("pixs_core_")
                }
            core_applied = sorted(
                name
                for app, name in MigrationRecorder(connection).applied_migrations()
                if app == "pixs_core"
            )
            if core_tables != expected_core_tables:
                raise RuntimeError("CORE_AUDIT_UNPROVED")
            if core_applied != expected_core_applied:
                raise RuntimeError("CORE_AUDIT_UNPROVED")
            out["core_migration"] = True
            out["core_applied"] = list(core_applied)
            backend_loader = MigrationExecutor(connection).loader
            if BACKEND_TARGET not in backend_loader.graph.nodes:
                raise RuntimeError(
                    "BACKEND_CONTRACT_MISSING:"
                    "src/pixs/backend/migrations/0016_c08_mode_storage.py"
                )
            backend_plan = backend_loader.graph.forwards_plan(BACKEND_TARGET)
            backend_plan_names = sorted(
                name for app, name in backend_plan if app == "backend"
            )
            if tuple(name for app, name in backend_plan if app == "backend") != BACKEND_EXPECTED_GRAPH:
                raise RuntimeError("BACKEND_GRAPH_CHANGED")
            out["backend_plan"] = list(backend_plan_names)
            for required in BACKEND_REQUIRED:
                if required not in backend_plan_names:
                    raise RuntimeError("BACKEND_PLAN_UNPROVED")
            backend_executor = MigrationExecutor(connection)
            planned = backend_executor.migration_plan([BACKEND_TARGET])
            if any(backwards for _migration, backwards in planned):
                raise RuntimeError("BACKEND_REVERSE_UNEXPECTED")
            backend_state = backend_loader.project_state([BACKEND_TARGET])
            expected_backend_tables = {
                model._meta.db_table
                for model in backend_state.apps.get_app_config("backend").get_models(
                    include_auto_created=True)
                if model._meta.managed and not model._meta.proxy
            }
            if not expected_backend_tables:
                raise RuntimeError("BACKEND_STATE_UNPROVED")
            with transaction.atomic(using="default", durable=True):
                backend_executor.migrate([BACKEND_TARGET])
            with connection.cursor() as cursor:
                backend_tables = set(connection.introspection.table_names(cursor))
            backend_applied = sorted(
                name
                for app, name in MigrationRecorder(connection).applied_migrations()
                if app == "backend"
            )
            if backend_applied != backend_plan_names:
                raise RuntimeError("BACKEND_MIGRATION_UNPROVED")
            if not expected_backend_tables.issubset(backend_tables):
                raise RuntimeError("BACKEND_STATE_UNPROVED")
            if not BACKEND_REQUIRED_TABLES.issubset(backend_tables):
                raise RuntimeError("BACKEND_TABLES_UNPROVED")
            out["backend_migration"] = True
            out["backend_applied"] = list(backend_applied)
            cases = callback()
            if type(cases) is not dict or set(cases) != set(expected_cases):
                raise RuntimeError("CASE_SET_INVALID")
            for value in cases.values():
                if type(value) is not bool:
                    raise RuntimeError("CASE_TYPE_INVALID")
            out["cases"] = dict(cases)
            callback_ok = all(cases.values())
            if not callback_ok:
                raise RuntimeError("CASE_UNPROVED")
        except Exception as error:
            out["failure_type"] = type(error).__name__
            from traceback import walk_tb

            for frame, line in list(walk_tb(error.__traceback__))[-8:]:
                name = Path(frame.f_code.co_filename).name
                function = frame.f_code.co_name
                if re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", name) is None:
                    name = "native"
                if re.fullmatch(r"[A-Za-z_<>][A-Za-z0-9_<>]{0,127}", function) is None:
                    function = "callback"
                out["failure_frames"].append((name, line, function))
        finally:
            if configured:
                try:
                    core.close_django_connections(refs, failures)
                except Exception:
                    failures.append("ORM_CLOSE_FAILED")
            if not attempted:
                out["cleanup"] = True
            elif env is not None and namespace is not None:
                try:
                    from psycopg import sql as pg_sql

                    args = (
                        env["PG_HOST"],
                        env["PG_PORT"],
                        env["PG_DATABASE"],
                        env["PG_USERNAME"],
                        env["PG_PASSWORD"],
                        refs,
                        failures,
                    )
                    with core.managed_pg_connection(*args) as cleaner:
                        with cleaner.cursor() as cursor:
                            cursor.execute(
                                "SELECT oid,nspowner FROM pg_namespace WHERE nspname=%s;",
                                (namespace,),
                            )
                            current = cursor.fetchone()
                            if current is None:
                                out["cleanup"] = True
                            else:
                                with cleaner.cursor() as role_cursor:
                                    role_cursor.execute(
                                        "SELECT oid FROM pg_roles WHERE rolname=current_user;"
                                    )
                                    current_role_row = role_cursor.fetchone()
                                if current_role_row is None:
                                    raise RuntimeError("CLEANUP_OWNERSHIP_UNPROVED")
                                current_role = int(current_role_row[0])
                                valid = (
                                    proof is not None
                                    and NS_PATTERN.fullmatch(namespace) is not None
                                    and namespace != "public"
                                    and (int(current[0]), int(current[1]), current_role)
                                    == proof
                                    and int(current[1]) == current_role
                                )
                                if not valid:
                                    raise RuntimeError("CLEANUP_OWNERSHIP_UNPROVED")
                                with cleaner.transaction():
                                    with cleaner.cursor() as drop_cursor:
                                        drop_cursor.execute(
                                            pg_sql.SQL("DROP SCHEMA {} CASCADE").format(
                                                pg_sql.Identifier(namespace)
                                            )
                                        )
                        if before_public is not None:
                            with cleaner.cursor() as cursor:
                                cursor.execute(
                                    "SELECT tablename FROM pg_tables "
                                    "WHERE schemaname='public' ORDER BY 1;"
                                )
                                after_public = [row[0] for row in cursor.fetchall()]
                            if after_public != before_public:
                                raise RuntimeError("PUBLIC_SCOPE_DIVERGENT")
                        with cleaner.cursor() as cursor:
                            cursor.execute(
                                "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname=%s);",
                                (namespace,),
                            )
                            out["cleanup"] = not bool(cursor.fetchone()[0])
                except Exception:
                    out["cleanup"] = False
                    if out["failure_type"] == "NONE":
                        out["failure_type"] = "CleanupError"
            out["conns_closed"] = not failures and all(
                bool(getattr(item, "closed", True)) for item in refs
            )
            out["real_pg"] = bool(
                callback_ok
                and out["migration"]
                and out["core_migration"]
                and out["backend_migration"]
                and out["namespace"]
                and out["cleanup"]
                and out["conns_closed"]
                and out["failure_type"] == "NONE"
            )
            if out["real_pg"]:
                out["code"] = "NONE"
            elif out["failure_type"] == "NONE":
                out["failure_type"] = "IncompleteProof"
    for key in ("code", "failure_type", "pg_version_num", "django_version"):
        out[key] = core.scrub_text(out[key], private_values)
    return out
