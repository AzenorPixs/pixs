"""Garde catalogue C04 : partagee/exclusive reelle PostgreSQL, sans droit delivre."""

from __future__ import annotations

from django.db import DatabaseError, InterfaceError

from pixs.core.services_common import CoreServiceError, _connection, lock_scopes

__all__ = [
    "CATALOG_SCOPE",
    "acquire_catalog_guard",
    "transaction_identity",
]

CATALOG_SCOPE = "authorization:catalog-v1"


def acquire_catalog_guard(alias: object, exclusive: object) -> None:
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    if type(exclusive) is not bool:
        raise CoreServiceError("SCOPES_INVALIDES") from None
    _connection(alias)
    if exclusive is True:
        lock_scopes(alias, (CATALOG_SCOPE,), shared=False)
    else:
        lock_scopes(alias, (CATALOG_SCOPE,), shared=True)


def transaction_identity(alias: object) -> tuple[int, int, int, int]:
    if type(alias) is not str or alias == "":
        raise CoreServiceError("ALIAS_INVALIDE") from None
    conn = _connection(alias)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid();")
            pid_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT txid_current();")
            tx_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_schema();")
            schema_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_schemas(false);")
            paths_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT oid FROM pg_database WHERE datname = current_database();")
            db_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT oid FROM pg_namespace WHERE nspname = current_schema();")
            nsp_row = cursor.fetchone()
    except (DatabaseError, InterfaceError) as error:
        raise CoreServiceError("VERROU_INACQUIS") from error
    if pid_row is None or type(pid_row[0]) is not int:
        raise CoreServiceError("BASE_INDETERMINEE") from None
    if tx_row is None or type(tx_row[0]) is not int:
        raise CoreServiceError("BASE_INDETERMINEE") from None
    if schema_row is None or type(schema_row[0]) is not str or schema_row[0] == "":
        raise CoreServiceError("NAMESPACE_INDETERMINE") from None
    if paths_row is None or type(paths_row[0]) is not list or len(paths_row[0]) != 1 or paths_row[0][0] != schema_row[0]:
        raise CoreServiceError("NAMESPACE_AMBIGU") from None
    if db_row is None or type(db_row[0]) is not int:
        raise CoreServiceError("BASE_INDETERMINEE") from None
    if nsp_row is None or type(nsp_row[0]) is not int:
        raise CoreServiceError("NAMESPACE_INDETERMINE") from None
    return (pid_row[0], tx_row[0], db_row[0], nsp_row[0])
