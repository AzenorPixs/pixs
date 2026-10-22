"""Cycle PG de qualification Auth : namespace privé, masquage et preuve de nettoyage."""
from __future__ import annotations

import re
import secrets
from pathlib import Path

EXPECTED_ROOT = "/home/devops/datas/pixs"
NS_PATTERN = re.compile(r"c03_[0-9a-f]{16}")


def run_in_auth_schema(root_str, callback, expected_cases, *, with_core=False, core_target="0002_core_audit"):
    import core_pg_test_support as core
    out = {"real_pg": False, "code": "AUTH_PG_FAILED", "failure_type": "NONE", "failure_frames": [],
           "pg_version_num": "", "django_version": "", "cases": {},
           "migration": False, "core_migration": None, "namespace": False, "cleanup": False,
           "conns_closed": False}
    refs, failures, private_values = [], [], []
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
            if type(core_target) is not str or core_target not in ("0002_core_audit", "0003_core_idempotence"):
                raise ValueError("CORE_TARGET_INVALID")
            if not with_core and core_target != "0002_core_audit":
                raise ValueError("CORE_TARGET_INVALID")
            out["core_migration"] = False if with_core else None
            from django.conf import settings
            if settings.configured:
                raise RuntimeError("SETTINGS_PREEXISTING")
            env = core.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_INVALID")
            private_values = list(env.values())
            namespace = "c03_" + secrets.token_hex(8)
            if NS_PATTERN.fullmatch(namespace) is None:
                raise RuntimeError("NAMESPACE_INVALID")
            from psycopg import sql
            args = (env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                    env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures)
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
            databases = {
                alias: {"ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"],
                        "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"],
                        "HOST": env["PG_HOST"], "PORT": env["PG_PORT"],
                        "OPTIONS": {"options": options, "connect_timeout": 2},
                        "CONN_MAX_AGE": 0, "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True}
                for alias in ("default", "peer", "contender")
            }
            from pixs.auth.apps import DJANGO_REQUIRED_APPS
            selected_apps = DJANGO_REQUIRED_APPS + (("pixs.backend.apps.PixsCoreConfig",) if with_core else ())
            settings.configure(INSTALLED_APPS=selected_apps, DATABASES=databases,
                               USE_TZ=True, TIME_ZONE="UTC", LOGGING_CONFIG=None)
            configured = True
            import django
            django.setup()
            from django.apps import apps
            from django.db import connections, transaction
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
            model_tables = {m._meta.db_table for m in apps.get_app_config("pixs_auth").get_models()}
            if len(model_tables) != 11:
                raise RuntimeError("MODEL_SET_INVALID")
            from pixs.auth.migration_lock import run_auth_initial
            if run_auth_initial("default", origin=None, target="0.1.0") != "applied":
                raise RuntimeError("MIGRATION_CONTRACT_INVALID")
            with connection.cursor() as cursor:
                tables = set(connection.introspection.table_names(cursor))
            if {name for name in tables if name.startswith("pixs_auth_")} != model_tables:
                raise RuntimeError("TABLE_SET_INVALID")
            if "django_migrations" not in tables:
                raise RuntimeError("RECORDER_MISSING")
            if ("pixs_auth", "0001_auth_initial") not in MigrationRecorder(connection).applied_migrations():
                raise RuntimeError("MIGRATION_UNPROVED")
            out["migration"] = True
            if with_core:
                from pixs.core.migration_lock import run_core_initial
                from django.db.migrations.executor import MigrationExecutor
                target = ("pixs_core", core_target)
                loader = MigrationExecutor(connection).loader
                if target not in loader.graph.nodes:
                    raise RuntimeError("CORE_TARGET_UNPROVED")
                expected_applied = {name for app, name in loader.graph.forwards_plan(target) if app == "pixs_core"}
                historical = loader.project_state([target]).apps.get_app_config("pixs_core")
                expected_core_tables = {model._meta.db_table for model in historical.get_models(include_auto_created=True)
                                        if model._meta.managed and not model._meta.proxy}
                if not expected_core_tables:
                    raise RuntimeError("CORE_STATE_UNPROVED")
                if run_core_initial("default", origin=None, target="0.1.0") != "applied":
                    raise RuntimeError("CORE_INITIAL_UNPROVED")
                with transaction.atomic(using="default", durable=True):
                    MigrationExecutor(connection).migrate([target])
                with connection.cursor() as cursor:
                    core_tables = {name for name in connection.introspection.table_names(cursor) if name.startswith("pixs_core_")}
                core_applied = {name for app, name in MigrationRecorder(connection).applied_migrations() if app == "pixs_core"}
                if core_tables != expected_core_tables or core_applied != expected_applied:
                    raise RuntimeError("CORE_AUDIT_UNPROVED")
                out["core_migration"] = True
            cases = callback()
            if type(cases) is not dict or set(cases) != set(expected_cases):
                raise RuntimeError("CASE_SET_INVALID")
            if any(type(v) is not bool for v in cases.values()):
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
            if configured:
                try:
                    core.close_django_connections(refs, failures)
                except Exception:
                    failures.append("ORM_CLOSE_FAILED")
            if not attempted:
                out["cleanup"] = True
            elif env is not None and namespace is not None:
                try:
                    from psycopg import sql
                    args = (env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                            env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures)
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
                                    valid = (proof is not None and NS_PATTERN.fullmatch(namespace) is not None
                                             and (int(current[0]), int(current[1]), current_role) == proof
                                             and int(current[1]) == current_role)
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
            out["conns_closed"] = not failures and all(bool(c.closed) for c in refs)
            out["real_pg"] = bool(callback_ok and out["migration"] and out["namespace"]
                                  and (not with_core or out["core_migration"] is True)
                                  and out["cleanup"] and out["conns_closed"]
                                  and out["failure_type"] == "NONE")
            if out["real_pg"]:
                out["code"] = "NONE"
            elif out["failure_type"] == "NONE":
                out["failure_type"] = "IncompleteProof"
    for key in ("code", "failure_type", "pg_version_num", "django_version"):
        out[key] = core.scrub_text(out[key], private_values)
    return out


__all__ = ["EXPECTED_ROOT", "NS_PATTERN", "run_in_auth_schema"]
