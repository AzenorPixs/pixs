"""Attachement de processus de recette au seul schéma jetable possédé par son parent."""
from __future__ import annotations

import types


def attach_existing(root_str, schema, callback):
    """Ne crée ni ne supprime de schéma ; masque les sorties et ferme ses connexions."""
    import core_pg_test_support as support
    out = {"code": "NONE", "failure_type": "", "trace": [], "closed": False, "result": None}
    refs, failures = [], []
    configured = False
    with support.mask_output():
        try:
            if type(root_str) is not str or root_str != support.EXPECTED_ROOT:
                raise ValueError("ROOT_INVALIDE")
            if type(schema) is not str or support.SCHEMA_PATTERN.fullmatch(schema) is None:
                raise ValueError("SCHEMA_INVALIDE")
            if type(callback) is not types.FunctionType:
                raise ValueError("CALLBACK_INVALIDE")
            env = support.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_REFUSE")
            with support.managed_pg_connection(
                env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures,
            ) as admin:
                if not support.schema_exists(admin, schema):
                    raise RuntimeError("SCHEMA_ABSENT")
                options = support.pg_options(support.quote_search_path(admin, schema))
                database = {
                    "ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"],
                    "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"],
                    "HOST": env["PG_HOST"], "PORT": env["PG_PORT"],
                    "OPTIONS": {"options": options, "connect_timeout": 2},
                    "TIME_ZONE": "UTC", "CONN_MAX_AGE": 0,
                    "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True,
                }
                import copy
                import django
                from django.conf import settings
                if settings.configured:
                    raise RuntimeError("SETTINGS_DEJA_CONFIGURES")
                settings.configure(
                    INSTALLED_APPS=["pixs.backend", "pixs.backend.apps.PixsCoreConfig"],
                    SECRET_KEY="synthetic-c09-process-test-only",
                    DATABASES={"default": copy.deepcopy(database), "peer": copy.deepcopy(database)},
                    LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True, TIME_ZONE="UTC",
                    DEFAULT_CHARSET="utf-8",
                )
                configured = True
                django.setup()
                from django.db import connections
                pids = []
                for alias in ("default", "peer"):
                    with connections[alias].cursor() as cur:
                        cur.execute("SELECT current_schemas(false), pg_backend_pid()")
                        schemas, pid = cur.fetchone()
                    if schemas != [schema] or type(pid) is not int or pid <= 0:
                        raise RuntimeError("CONTEXTE_PG_INVALIDE")
                    pids.append(pid)
                if pids[0] == pids[1]:
                    raise RuntimeError("CONNEXIONS_NON_DISTINCTES")
                out["result"] = callback({"schema": schema, "pids": tuple(pids)})
        except Exception as error:
            out["code"] = "ENFANT_NON_PROUVE"
            out["failure_type"] = type(error).__name__
            import traceback
            out["trace"] = [(frame.filename.split("/")[-1], frame.lineno)
                            for frame in traceback.extract_tb(error.__traceback__)[-4:]]
        finally:
            if configured:
                try:
                    support.close_django_connections(refs, failures)
                except Exception:
                    failures.append("FERMETURE_NON_PROUVEE")
            out["closed"] = bool(refs and not failures and all(bool(c.closed) for c in refs))
    if out["code"] != "NONE" or not out["closed"]:
        out["result"] = None
    return out
