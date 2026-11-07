# path: tests/integration/agent_pg_test_support.py
"""Support PG reel Agent : namespace ag10 jetable, migration verrouillee, nettoyage prouve.

Profil de stockage seul par defaut ; Core/C05 reels en option explicite.
Les faits Auth et ports de confiance restent des fixtures de l appelant ;
aucune qualification C03, reseau ou transport n est revendiquee.
"""
from __future__ import annotations
import re
import secrets
from pathlib import Path
EXPECTED_ROOT = "/home/devops/datas/pixs"
NS_PATTERN = re.compile(r"ag10_[0-9a-f]{16}")
HISTORICAL_AGENT_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact"})
EXTENDED_AGENT_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document"})
PROVENANCE_AGENT_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document", "pixs_agent_payload_provenance"})
BINDING_AGENT_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document", "pixs_agent_payload_provenance", "pixs_agent_pa_binding", "pixs_agent_pa_binding_revision", "pixs_agent_pa_binding_state"})
RELAY_AGENT_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document", "pixs_agent_payload_provenance", "pixs_agent_pa_binding", "pixs_agent_pa_binding_revision", "pixs_agent_pa_binding_state", "pixs_agent_pa_outbox", "pixs_agent_pa_attempt", "pixs_agent_pa_delivery_event"})
__all__ = ["EXPECTED_ROOT", "NS_PATTERN", "HISTORICAL_AGENT_TABLES", "EXTENDED_AGENT_TABLES", "PROVENANCE_AGENT_TABLES", "BINDING_AGENT_TABLES", "RELAY_AGENT_TABLES", "run_in_agent_schema"]
def run_in_agent_schema(root_str, callback, expected_cases, *, with_core=False, with_payload_document=False, with_provenance=False, with_binding=False, with_relay=False):
    import core_pg_test_support as core
    out = {"real_pg": False, "code": "AGENT_PG_FAILED", "failure_type": "NONE", "failure_frames": [], "pg_version_num": "", "django_version": "", "cases": {}, "migration": False, "namespace": False, "cleanup": False, "conns_closed": False, "threads_closed": False}
    out["core_migration"] = False if with_core is True else None
    refs, failures, private_values = [], [], []
    tracked_threads = []
    env, namespace, proof = None, None, None
    attempted, configured, callback_ok = False, False, False
    with core.mask_output():
        try:
            if type(root_str) is not str or str(Path(root_str).resolve()) != EXPECTED_ROOT:
                raise ValueError("ROOT_INVALID")
            if not callable(callback) or type(expected_cases) is not tuple or not expected_cases:
                raise ValueError("CASES_INVALID")
            if any(type(k) is not str or not k for k in expected_cases):
                raise ValueError("CASES_INVALID")
            if len(set(expected_cases)) != len(expected_cases):
                raise ValueError("CASES_INVALID")
            if type(with_core) is not bool:
                raise ValueError("PROFILE_INVALID")
            if type(with_payload_document) is not bool:
                raise ValueError("PROFILE_INVALID")
            if type(with_provenance) is not bool:
                raise ValueError("PROFILE_INVALID")
            if type(with_binding) is not bool:
                raise ValueError("PROFILE_INVALID")
            if type(with_relay) is not bool:
                raise ValueError("PROFILE_INVALID")
            if with_provenance is True and with_payload_document is not True:
                raise ValueError("PROFILE_INVALID")
            if with_binding is True and (with_payload_document is not True or with_provenance is not True):
                raise ValueError("PROFILE_INVALID")
            if with_relay is True and (with_payload_document is not True or with_provenance is not True or with_binding is not True):
                raise ValueError("PROFILE_INVALID")
            from django.conf import settings
            if settings.configured:
                raise RuntimeError("SETTINGS_PREEXISTING")
            env = core.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_INVALID")
            private_values = list(env.values())
            namespace = "ag10_" + secrets.token_hex(8)
            if NS_PATTERN.fullmatch(namespace) is None:
                raise RuntimeError("NAMESPACE_INVALID")
            if namespace == "public":
                raise RuntimeError("NAMESPACE_INVALID")
            from psycopg import sql
            args = (env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"], env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures)
            with core.managed_pg_connection(*args) as admin:
                with admin.transaction():
                    with admin.cursor() as cursor:
                        cursor.execute("SELECT oid FROM pg_roles WHERE rolname=current_user")
                        role_oid = int(cursor.fetchone()[0])
                        cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(namespace)))
                        attempted = True
                        cursor.execute("SELECT oid,nspowner FROM pg_namespace WHERE nspname=%s", (namespace,))
                        row = cursor.fetchone()
                        if row is None or int(row[1]) != role_oid:
                            raise RuntimeError("OWNERSHIP_UNPROVED")
                        proof = (int(row[0]), int(row[1]), role_oid)
                quoted = sql.Identifier(namespace).as_string(admin)
            options = core.pg_options(search_path_quoted=quoted)
            databases = {alias: {"ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"], "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"], "HOST": env["PG_HOST"], "PORT": env["PG_PORT"], "OPTIONS": {"options": options, "connect_timeout": 2}, "CONN_MAX_AGE": 0, "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True} for alias in ("default", "peer", "contender")}
            from pixs.agent.apps import DJANGO_REQUIRED_APPS
            if tuple(DJANGO_REQUIRED_APPS) != ("django.contrib.postgres", "pixs.agent.apps.PixsAgentConfig"):
                raise RuntimeError("REQUIRED_APPS_INVALID")
            selected_apps = tuple(DJANGO_REQUIRED_APPS) + (("pixs.backend.apps.PixsCoreConfig",) if with_core else ())
            settings.configure(INSTALLED_APPS=list(selected_apps), DATABASES=databases, USE_TZ=True, TIME_ZONE="UTC", LOGGING_CONFIG=None)
            configured = True
            import django
            django.setup()
            from django.apps import apps
            from django.db import connections
            from django.db.migrations.executor import MigrationExecutor
            from django.db.migrations.recorder import MigrationRecorder
            connection = connections["default"]
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_schema(),current_schemas(false),current_setting('server_version_num')")
                schema, path, version = cursor.fetchone()
                cursor.execute("SELECT oid,nspowner FROM pg_namespace WHERE nspname=%s", (namespace,))
                observed = cursor.fetchone()
            if schema != namespace or list(path) != [namespace] or observed is None:
                raise RuntimeError("NAMESPACE_UNPROVED")
            if (int(observed[0]), int(observed[1])) != proof[:2]:
                raise RuntimeError("NAMESPACE_CHANGED")
            if type(version) is not str or re.fullmatch(r"[0-9]+", version) is None:
                raise RuntimeError("VERSION_UNPROVED")
            out["namespace"] = True
            out["pg_version_num"] = version
            out["django_version"] = django.get_version()
            from pixs.agent import models as _agent_models
            _registered = list(apps.get_app_config("pixs_agent").get_models())
            if len({m.__name__ for m in _registered}) != len(_registered) or len({m._meta.db_table for m in _registered}) != len(_registered):
                raise RuntimeError("MODEL_SET_INVALID")
            _by_name = {m.__name__: m for m in _registered}
            for _name, _table in (("AgentHead", "pixs_agent_head"), ("AgentOperation", "pixs_agent_operation"), ("AgentFact", "pixs_agent_fact")):
                if _by_name.get(_name) is not getattr(_agent_models, _name, None) or _by_name[_name]._meta.db_table != _table:
                    raise RuntimeError("MODEL_SET_INVALID")
            from pixs.agent import _registry_support as _agent_registry
            _loader = MigrationExecutor(connection).loader
            if _agent_registry.check_registry_current(apps, _by_name, _agent_models, _loader) is not True:
                raise RuntimeError("MODEL_SET_INVALID")
            if with_core:
                from pixs.core.migration_lock import run_core_initial
                from django.db import transaction
                target = ("pixs_core", "0002_core_audit")
                loader = MigrationExecutor(connection).loader
                expected_core_migrations = {name for app, name in loader.graph.forwards_plan(target) if app == "pixs_core"}
                historical = loader.project_state([target]).apps.get_app_config("pixs_core")
                expected_core_tables = {model._meta.db_table for model in historical.get_models(include_auto_created=True) if model._meta.managed and not model._meta.proxy}
                if not expected_core_tables:
                    raise RuntimeError("CORE_STATE_UNPROVED")
                if run_core_initial("default", origin=None, target="0.1.0") != "applied":
                    raise RuntimeError("CORE_INITIAL_UNPROVED")
                with transaction.atomic(using="default", durable=True):
                    MigrationExecutor(connection).migrate([target])
                with connection.cursor() as cursor:
                    observed_core_tables = {name for name in connection.introspection.table_names(cursor) if name.startswith("pixs_core_")}
                observed_core_migrations = {name for app, name in MigrationRecorder(connection).applied_migrations() if app == "pixs_core"}
                if observed_core_tables != expected_core_tables or observed_core_migrations != expected_core_migrations:
                    raise RuntimeError("CORE_AUDIT_UNPROVED")
                out["core_migration"] = True
            from pixs.agent.migration_lock import APP_LABEL, EXPECTED_TABLES, MIGRATION_NAME, run_agent_initial
            if APP_LABEL != "pixs_agent" or MIGRATION_NAME != "0001_agent_initial":
                raise RuntimeError("MIGRATION_CONTRACT_INVALID")
            if set(EXPECTED_TABLES) != set(HISTORICAL_AGENT_TABLES):
                raise RuntimeError("MIGRATION_CONTRACT_INVALID")
            if run_agent_initial("default", origin=None, target="0.1.0") != "applied":
                raise RuntimeError("MIGRATION_CONTRACT_INVALID")
            with connection.cursor() as cursor:
                _pre_tables = set(connection.introspection.table_names(cursor))
            if {n for n in _pre_tables if n.startswith("pixs_agent_")} != set(HISTORICAL_AGENT_TABLES):
                raise RuntimeError("TABLE_SET_INVALID")
            if "django_migrations" not in _pre_tables:
                raise RuntimeError("RECORDER_MISSING")
            if {name for (app, name) in MigrationRecorder(connection).applied_migrations() if app == "pixs_agent"} != {"0001_agent_initial"}:
                raise RuntimeError("MIGRATION_UNPROVED")
            if with_relay is True:
                _target_state = _loader.project_state([("pixs_agent", "0005_agent_pa_relay")]).apps.get_app_config("pixs_agent")
                if {_m._meta.db_table for _m in _target_state.get_models()} != set(RELAY_AGENT_TABLES):
                    raise RuntimeError("MODEL_SET_INVALID")
                MigrationExecutor(connection).migrate([("pixs_agent", "0005_agent_pa_relay")])
                with connection.cursor() as cursor:
                    tables = set(connection.introspection.table_names(cursor))
                if {n for n in tables if n.startswith("pixs_agent_")} != set(RELAY_AGENT_TABLES):
                    raise RuntimeError("TABLE_SET_INVALID")
                if "django_migrations" not in tables:
                    raise RuntimeError("RECORDER_MISSING")
                if {name for (app, name) in MigrationRecorder(connection).applied_migrations() if app == "pixs_agent"} != {"0001_agent_initial", "0002_agent_payload_document", "0003_agent_payload_provenance", "0004_agent_pa_binding", "0005_agent_pa_relay"}:
                    raise RuntimeError("MIGRATION_UNPROVED")
            elif with_binding is True:
                _target_state = _loader.project_state([("pixs_agent", "0004_agent_pa_binding")]).apps.get_app_config("pixs_agent")
                if {_m._meta.db_table for _m in _target_state.get_models()} != set(BINDING_AGENT_TABLES):
                    raise RuntimeError("MODEL_SET_INVALID")
                MigrationExecutor(connection).migrate([("pixs_agent", "0004_agent_pa_binding")])
                with connection.cursor() as cursor:
                    tables = set(connection.introspection.table_names(cursor))
                if {n for n in tables if n.startswith("pixs_agent_")} != set(BINDING_AGENT_TABLES):
                    raise RuntimeError("TABLE_SET_INVALID")
                if "django_migrations" not in tables:
                    raise RuntimeError("RECORDER_MISSING")
                if {name for (app, name) in MigrationRecorder(connection).applied_migrations() if app == "pixs_agent"} != {"0001_agent_initial", "0002_agent_payload_document", "0003_agent_payload_provenance", "0004_agent_pa_binding"}:
                    raise RuntimeError("MIGRATION_UNPROVED")
            elif with_provenance is True:
                _target_state = _loader.project_state([("pixs_agent", "0003_agent_payload_provenance")]).apps.get_app_config("pixs_agent")
                if {_m._meta.db_table for _m in _target_state.get_models()} != set(PROVENANCE_AGENT_TABLES):
                    raise RuntimeError("MODEL_SET_INVALID")
                MigrationExecutor(connection).migrate([("pixs_agent", "0003_agent_payload_provenance")])
                with connection.cursor() as cursor:
                    tables = set(connection.introspection.table_names(cursor))
                if {n for n in tables if n.startswith("pixs_agent_")} != set(PROVENANCE_AGENT_TABLES):
                    raise RuntimeError("TABLE_SET_INVALID")
                if "django_migrations" not in tables:
                    raise RuntimeError("RECORDER_MISSING")
                if {name for (app, name) in MigrationRecorder(connection).applied_migrations() if app == "pixs_agent"} != {"0001_agent_initial", "0002_agent_payload_document", "0003_agent_payload_provenance"}:
                    raise RuntimeError("MIGRATION_UNPROVED")
            elif with_payload_document is False:
                with connection.cursor() as cursor:
                    tables = set(connection.introspection.table_names(cursor))
                if {n for n in tables if n.startswith("pixs_agent_")} != set(HISTORICAL_AGENT_TABLES):
                    raise RuntimeError("TABLE_SET_INVALID")
                if "django_migrations" not in tables:
                    raise RuntimeError("RECORDER_MISSING")
                if {name for (app, name) in MigrationRecorder(connection).applied_migrations() if app == "pixs_agent"} != {"0001_agent_initial"}:
                    raise RuntimeError("MIGRATION_UNPROVED")
            else:
                _target_state = _loader.project_state([("pixs_agent", "0002_agent_payload_document")]).apps.get_app_config("pixs_agent")
                if {_m._meta.db_table for _m in _target_state.get_models()} != set(EXTENDED_AGENT_TABLES):
                    raise RuntimeError("MODEL_SET_INVALID")
                if {_target_state.get_model(_name)._meta.db_table for _name in ("AgentHead", "AgentOperation", "AgentFact", "PayloadDocument")} != set(EXTENDED_AGENT_TABLES):
                    raise RuntimeError("MODEL_SET_INVALID")
                MigrationExecutor(connection).migrate([("pixs_agent", "0002_agent_payload_document")])
                with connection.cursor() as cursor:
                    tables = set(connection.introspection.table_names(cursor))
                if {n for n in tables if n.startswith("pixs_agent_")} != set(EXTENDED_AGENT_TABLES):
                    raise RuntimeError("TABLE_SET_INVALID")
                if "django_migrations" not in tables:
                    raise RuntimeError("RECORDER_MISSING")
                if {name for (app, name) in MigrationRecorder(connection).applied_migrations() if app == "pixs_agent"} != {"0001_agent_initial", "0002_agent_payload_document"}:
                    raise RuntimeError("MIGRATION_UNPROVED")
            out["migration"] = True
            cases = callback(refs, failures, tracked_threads, out["cases"])
            if type(cases) is not dict or set(cases) != set(expected_cases):
                raise RuntimeError("CASE_SET_INVALID")
            if any(type(vv) is not bool for vv in cases.values()):
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
                safe_name = name if re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", name) else "native"
                safe_function = function if re.fullmatch(r"[A-Za-z_<>][A-Za-z0-9_<>]{0,127}", function) else "callback"
                out["failure_frames"].append((safe_name, line, safe_function))
        finally:
            threads_ok = True
            try:
                for t in list(tracked_threads):
                    t.join(timeout=10)
                    if t.is_alive():
                        threads_ok = False
            except Exception:
                threads_ok = False
                failures.append("THREAD_JOIN_FAILED")
            out["threads_closed"] = bool(threads_ok and all(not t.is_alive() for t in tracked_threads))
            if configured:
                try:
                    core.close_django_connections(refs, failures)
                except Exception:
                    failures.append("ORM_CLOSE_FAILED")
            if not attempted:
                out["cleanup"] = True
            elif threads_ok is False:
                out["cleanup"] = False
                if out["failure_type"] == "NONE":
                    out["failure_type"] = "ThreadActive"
            elif env is not None and namespace is not None:
                try:
                    from psycopg import sql
                    args = (env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"], env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures)
                    with core.managed_pg_connection(*args) as cleaner:
                        with cleaner.transaction():
                            with cleaner.cursor() as cursor:
                                cursor.execute("SELECT oid,nspowner FROM pg_namespace WHERE nspname=%s", (namespace,))
                                current = cursor.fetchone()
                                if current is None:
                                    out["cleanup"] = True
                                else:
                                    cursor.execute("SELECT oid FROM pg_roles WHERE rolname=current_user")
                                    current_role = int(cursor.fetchone()[0])
                                    valid = (proof is not None and NS_PATTERN.fullmatch(namespace) is not None and (int(current[0]), int(current[1]), current_role) == proof and int(current[1]) == current_role)
                                    if not valid:
                                        raise RuntimeError("CLEANUP_OWNERSHIP_UNPROVED")
                                    cursor.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(namespace)))
                        with cleaner.cursor() as cursor:
                            cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname=%s)", (namespace,))
                            out["cleanup"] = not bool(cursor.fetchone()[0])
                except Exception:
                    out["cleanup"] = False
                    if out["failure_type"] == "NONE":
                        out["failure_type"] = "CleanupError"
            if attempted and not out["cleanup"] and proof is not None:
                out["remaining_namespace"] = {"name": namespace, "oid": proof[0], "owner_oid": proof[1]}
            out["conns_closed"] = not failures and all(bool(cc.closed) for cc in refs)
            out["real_pg"] = bool(callback_ok and out["migration"] and (not with_core or out["core_migration"] is True) and out["namespace"] and out["cleanup"] and out["conns_closed"] and out["threads_closed"] and out["failure_type"] == "NONE")
            if out["real_pg"]:
                out["code"] = "NONE"
            elif out["failure_type"] == "NONE":
                out["failure_type"] = "IncompleteProof"
    for key in ("code", "failure_type", "pg_version_num", "django_version"):
        out[key] = core.scrub_text(out[key], private_values)
    return out
