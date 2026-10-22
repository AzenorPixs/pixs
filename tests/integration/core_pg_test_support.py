"""Support partagé des tests PG réels Core : parsing borné, schémas jetables, Django éphémère, rédaction.

Rôle borné réutilisable pour les prochains tests services : aucune logique
métier, aucune lecture d'environnement à l'import, aucune configuration Django
à l'import, aucune valeur réelle. Le seul processus de test charge project.env
via read_project_env ; les cinq valeurs PG restent locales à ce processus et
ne figurent ni dans les journaux, ni dans les rapports, ni dans le code.
"""
from __future__ import annotations

import re
import uuid
from contextlib import contextmanager
from pathlib import Path

__all__ = [
    "EXPECTED_ROOT",
    "WANTED_KEYS",
    "SCHEMA_PATTERN",
    "FIXED_CODE_PATTERN",
    "parse_project_env_text",
    "read_project_env",
    "mask_output",
    "scrub_text",
    "safe_schema_name",
    "pg_options",
    "managed_pg_connection",
    "scalar_one",
    "schema_exists",
    "table_names_of_current_schema",
    "table_exists",
    "create_schema",
    "drop_schema_if_owned",
    "quote_identifier",
    "quote_search_path",
    "configure_django_core_pg",
    "close_django_connections",
]

EXPECTED_ROOT = "/home/devops/datas/pixs"
WANTED_KEYS = ("PG_HOST", "PG_PORT", "PG_DATABASE", "PG_USERNAME", "PG_PASSWORD")
SCHEMA_PATTERN = re.compile(r"c02_[0-9a-f]{16}")
FIXED_CODE_PATTERN = re.compile(r"[A-Z][A-Z0-9_]*")

_ENV_READ_LIMIT = 65537
_ENV_LINE_LIMIT = 2000
_VALUE_LIMIT = 1024
_STATEMENT_TIMEOUT_MS = 1500
_LOCK_TIMEOUT_MS = 1500
_CONNECT_TIMEOUT_SECONDS = 2


def parse_project_env_text(text):
    """Parse borné des cinq clés PG ; refuse expansion, littéraux filtrés."""
    if type(text) is not str:
        raise ValueError("env invalid") from None
    if len(text) > 65536 or "\x00" in text:
        raise ValueError("env invalid") from None
    lines = text.splitlines()
    if len(lines) > _ENV_LINE_LIMIT:
        raise ValueError("env invalid") from None
    found = {}
    for raw in lines:
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if name not in WANTED_KEYS:
            continue
        if name in found:
            raise ValueError("env invalid") from None
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            inner = value[1:-1]
            if value[0] in inner:
                raise ValueError("env invalid") from None
            value = inner
        elif len(value) >= 1 and (value[0] in ("'", '"') or value[-1] in ("'", '"')):
            raise ValueError("env invalid") from None
        if value == "" or len(value) > _VALUE_LIMIT or "\x00" in value:
            raise ValueError("env invalid") from None
        if "$" in value or "`" in value or "\\" in value:
            raise ValueError("env invalid") from None
        found[name] = value
    for name in WANTED_KEYS:
        if name not in found:
            raise ValueError("env invalid") from None
    if found["PG_HOST"] != "127.0.0.1" and found["PG_HOST"] != "localhost":
        raise ValueError("env invalid") from None
    if re.fullmatch(r"[0-9]+", found["PG_PORT"]) is None:
        raise ValueError("env invalid") from None
    try:
        port_number = int(found["PG_PORT"], 10)
    except ValueError:
        raise ValueError("env invalid") from None
    if port_number < 1 or port_number > 65535:
        raise ValueError("env invalid") from None
    return found


def read_project_env(root_str):
    """Charge locale project.env du seul processus test ; None si refusé."""
    if type(root_str) is not str or root_str == "":
        return None
    try:
        resolved = str(Path(root_str).resolve())
    except (OSError, RuntimeError, ValueError):
        return None
    if resolved != EXPECTED_ROOT:
        return None
    try:
        with Path(root_str, "project.env").open("rb") as handle:
            raw = handle.read(_ENV_READ_LIMIT)
    except OSError:
        return None
    if len(raw) >= _ENV_READ_LIMIT:
        return None
    try:
        text = raw.decode("utf-8")
    except (UnicodeDecodeError, ValueError):
        return None
    if "\x00" in text:
        return None
    try:
        return parse_project_env_text(text)
    except ValueError:
        return None


@contextmanager
def mask_output():
    """Capture stdout/stderr/traces du processus test ; rédaction après."""
    import io
    import logging
    import sys

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


def scrub_text(text, secrets):
    """Rédige toute valeur PG d'un texte ; sortie sûre uniquement après."""
    if type(text) is not str:
        return ""
    try:
        ordered = sorted(secrets, key=len, reverse=True)
    except TypeError:
        return "***"
    redacted = text
    for secret in ordered:
        if type(secret) is str and secret != "":
            redacted = redacted.replace(secret, "***")
    return redacted


def safe_schema_name():
    """Schéma jetable c02_<hex> ; jamais public ni existant ciblé."""
    name = "c02_" + uuid.uuid4().hex[:16]
    if SCHEMA_PATTERN.fullmatch(name) is None:
        raise RuntimeError("invalid synthetic schema name")
    if name == "public":
        raise RuntimeError("invalid synthetic schema name")
    return name


def pg_options(search_path_quoted=None):
    """Options PG fixes ; search_path déjà quoté par Identifier en amont."""
    options = (
        "-c statement_timeout=%d -c lock_timeout=%d"
        % (_STATEMENT_TIMEOUT_MS, _LOCK_TIMEOUT_MS)
    )
    if search_path_quoted is not None:
        if type(search_path_quoted) is not str or search_path_quoted == "":
            raise ValueError("search path invalid")
        options = "%s -c search_path=%s" % (options, search_path_quoted)
    return options


@contextmanager
def managed_pg_connection(host, port, database, user, password, refs, close_failures, options=None):
    """Connexion psycopg autocommit fermée même en échec."""
    import psycopg

    connection = None
    try:
        connection = psycopg.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=_CONNECT_TIMEOUT_SECONDS,
            autocommit=True,
            options=pg_options() if options is None else options,
        )
        refs.append(connection)
        yield connection
    finally:
        if connection is not None:
            try:
                if not connection.closed:
                    connection.close()
            except (psycopg.Error, OSError):
                close_failures.append("CONN_CLOSE_FAILED")


def scalar_one(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    finally:
        cursor.close()


def schema_exists(connection, schema_name):
    if type(schema_name) is not str or SCHEMA_PATTERN.fullmatch(schema_name) is None:
        return False
    return bool(
        scalar_one(
            connection,
            "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (schema_name,),
        )
    )


def table_names_of_current_schema(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = current_schema();"
        )
        rows = cursor.fetchall()
    finally:
        cursor.close()
    names = set()
    for row in rows:
        if type(row[0]) is not str or row[0] == "":
            raise RuntimeError("inventory unexpected")
        names.add(row[0])
    return names


def table_exists(connection, schema_name, table_name):
    if type(table_name) is not str or table_name == "":
        return False
    return bool(
        scalar_one(
            connection,
            "SELECT EXISTS (SELECT 1 FROM pg_class AS class "
            "JOIN pg_namespace AS namespace ON namespace.oid = class.relnamespace "
            "WHERE namespace.nspname = %s AND class.relname = %s)",
            (schema_name, table_name),
        )
    )


def create_schema(connection, schema_name):
    """Crée un schéma jetable ; refuse public, collisions et permissions."""
    from psycopg import Error, errors, sql

    if type(schema_name) is not str or SCHEMA_PATTERN.fullmatch(schema_name) is None:
        return False, "SCHEMA_NAME_INVALID"
    if schema_name == "public":
        return False, "SCHEMA_NAME_INVALID"
    try:
        if schema_exists(connection, schema_name):
            return False, "SCHEMA_COLLISION"
    except (Error, OSError):
        return False, "SCHEMA_PROBE_FAILED"
    owned = False
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name)))
            owned = True
        finally:
            cursor.close()
    except errors.DuplicateSchema:
        return False, "SCHEMA_COLLISION"
    except errors.InsufficientPrivilege:
        return owned, "SCHEMA_PERMISSION_DENIED"
    except Error:
        return owned, "SCHEMA_CREATE_FAILED"
    try:
        if schema_exists(connection, schema_name):
            return owned, "NONE"
        return owned, "SCHEMA_CREATE_UNPROVED"
    except (Error, OSError):
        return owned, "SCHEMA_CREATE_UNPROVED"


def drop_schema_if_owned(connection, schema_name, owned):
    """Supprime seulement un schéma réellement créé et suivi ; jamais public."""
    from psycopg import Error, sql

    if not owned:
        return False
    if type(schema_name) is not str or SCHEMA_PATTERN.fullmatch(schema_name) is None:
        return False
    if schema_name == "public":
        return False
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema_name)))
        finally:
            cursor.close()
    except (Error, OSError):
        return False
    return not schema_exists(connection, schema_name)


def quote_identifier(connection, name):
    from psycopg import sql

    if type(name) is not str or name == "":
        raise ValueError("identifier invalid")
    return sql.Identifier(name).as_string(connection)


def quote_search_path(connection, schema_name):
    if type(schema_name) is not str or SCHEMA_PATTERN.fullmatch(schema_name) is None:
        raise ValueError("search path invalid")
    return quote_identifier(connection, schema_name)


def configure_django_core_pg(aliases):
    """Configure éphémère de test : PixsCoreConfig seul, alias explicites."""
    from django.conf import settings

    if settings.configured:
        raise RuntimeError("settings already configured")
    if type(aliases) is not dict or len(aliases) == 0:
        raise ValueError("aliases invalid")
    databases = {}
    for alias, spec in aliases.items():
        if type(alias) is not str or alias == "":
            raise ValueError("alias invalid")
        if type(spec) is not dict or set(spec.keys()) != {"dbname", "user", "password", "host", "port", "options"}:
            raise ValueError("alias spec invalid")
        for key, value in spec.items():
            if type(value) is not str or value == "":
                raise ValueError("alias spec invalid")
        databases[alias] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": spec["dbname"],
            "USER": spec["user"],
            "PASSWORD": spec["password"],
            "HOST": spec["host"],
            "PORT": spec["port"],
            "OPTIONS": {
                "options": spec["options"],
                "connect_timeout": _CONNECT_TIMEOUT_SECONDS,
            },
            "TIME_ZONE": "UTC",
            "CONN_MAX_AGE": 0,
            "ATOMIC_REQUESTS": False,
            "AUTOCOMMIT": True,
        }
    settings.configure(
        INSTALLED_APPS=["pixs.backend.apps.PixsCoreConfig"],
        SECRET_KEY="core-pg-synthetic-only",
        DATABASES=databases,
        USE_TZ=True,
        TIME_ZONE="UTC",
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
    )


def close_django_connections(refs, close_failures):
    """Ferme les alias du thread courant ; chaque thread ferme les siens."""
    from django.db import DatabaseError, InterfaceError
    from django.db import connections as dj_conns

    for alias in dj_conns:
        try:
            wrapper = dj_conns[alias]
            if wrapper.connection is not None:
                refs.append(wrapper.connection)
            wrapper.close()
        except (DatabaseError, InterfaceError):
            close_failures.append("ORM_CLOSE_FAILED")
