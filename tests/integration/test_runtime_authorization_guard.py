"""Recette C04 PostgreSQL réelle : verrous, transaction et namespace jetables.

Le processus local seul charge les cinq valeurs PG avec le support existant.
Aucun schéma métier, migration, credential ou acteur synthétique n'est requis.
"""
from __future__ import annotations

import re

_CASES = (
    "hors_transaction", "mode_bool_strict", "lecteurs_compatibles",
    "lecteur_bloque_ecrivain", "ecrivain_bloque_lecteur",
    "ecrivains_exclusifs", "rollback_libere", "identite_stable",
    "transaction_nouvelle", "namespaces_independants",
)


def run_real_runtime_guard(root_str: str) -> dict:
    import core_pg_test_support as support

    out = {"real_pg": False, "cases": {}, "cleanup": False,
           "conns_closed": False, "code": "NONE", "pg_version_num": ""}
    refs, failures, schemas = [], [], []
    configured = False
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                raise RuntimeError("ENV_REFUSE")
            with support.managed_pg_connection(
                env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
                env["PG_USERNAME"], env["PG_PASSWORD"], refs, failures,
            ) as admin:
                try:
                    for _ in range(2):
                        name = support.safe_schema_name()
                        owned, reason = support.create_schema(admin, name)
                        if owned:
                            schemas.append(name)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                    aliases = {}
                    for alias, name in (("default", schemas[0]), ("peer", schemas[0]),
                                        ("other", schemas[1])):
                        aliases[alias] = {
                            "dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"],
                            "password": env["PG_PASSWORD"], "host": env["PG_HOST"],
                            "port": env["PG_PORT"],
                            "options": support.pg_options(support.quote_search_path(admin, name)),
                        }
                    support.configure_django_core_pg(aliases)
                    configured = True
                    import django
                    django.setup()
                    from django.db import connections
                    with connections["default"].cursor() as cursor:
                        cursor.execute("SELECT current_setting('server_version_num')")
                        version = cursor.fetchone()[0]
                    if type(version) is not str or re.fullmatch(r"[0-9]+", version) is None:
                        raise RuntimeError("VERSION_NON_PROUVEE")
                    out["pg_version_num"] = version
                    out["cases"] = _scenarios()
                finally:
                    if configured:
                        support.close_django_connections(refs, failures)
                    cleanup = [support.drop_schema_if_owned(admin, name, True)
                               for name in reversed(schemas)]
                    out["cleanup"] = len(cleanup) == 2 and all(cleanup)
        except Exception as error:
            # Frontière de sortie : aucun message ou détail de connexion.
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
        finally:
            out["conns_closed"] = not failures and all(bool(c.closed) for c in refs)
    out["real_pg"] = (
        out["code"] == "NONE" and out["cleanup"] and out["conns_closed"]
        and set(out["cases"]) == set(_CASES) and all(out["cases"].values())
    )
    if not out["real_pg"] and out["code"] == "NONE":
        out["code"] = "CAS_NON_PROUVE"
    return out


def _scenarios() -> dict:
    from django.db import transaction
    from pixs.core.services_authorization_guard import (
        acquire_catalog_guard, transaction_identity,
    )
    from pixs.core.services_common import CoreServiceError

    def refused(fn, code):
        try:
            fn()
        except CoreServiceError as error:
            return error.code == code
        return False

    out = {}
    out["hors_transaction"] = refused(
        lambda: acquire_catalog_guard("default", False), "HORS_TRANSACTION")
    with transaction.atomic(using="default"):
        out["mode_bool_strict"] = refused(
            lambda: acquire_catalog_guard("default", 1), "SCOPES_INVALIDES")
        acquire_catalog_guard("default", False)
        first = transaction_identity("default")
        out["identite_stable"] = first == transaction_identity("default")
        with transaction.atomic(using="peer"):
            acquire_catalog_guard("peer", False)
            out["lecteurs_compatibles"] = (
                transaction_identity("peer")[0] != first[0])
        with transaction.atomic(using="peer"):
            out["lecteur_bloque_ecrivain"] = refused(
                lambda: acquire_catalog_guard("peer", True), "VERROU_CONCURRENT")
        transaction.set_rollback(True, using="default")
    with transaction.atomic(using="peer"):
        acquire_catalog_guard("peer", True)
        out["rollback_libere"] = True
        with transaction.atomic(using="default"):
            out["ecrivain_bloque_lecteur"] = refused(
                lambda: acquire_catalog_guard("default", False), "VERROU_CONCURRENT")
        with transaction.atomic(using="default"):
            out["ecrivains_exclusifs"] = refused(
                lambda: acquire_catalog_guard("default", True), "VERROU_CONCURRENT")
        with transaction.atomic(using="other"):
            acquire_catalog_guard("other", True)
            out["namespaces_independants"] = (
                transaction_identity("other")[3] != first[3])
    with transaction.atomic(using="default"):
        acquire_catalog_guard("default", True)
        out["transaction_nouvelle"] = transaction_identity("default")[1] != first[1]
    return out
