"""Intégration PG réelle des migrations Core : gardes sûres plus callable mandaté.

Conventions reprises de test_pg_connectivity_integration.py (processus isolé,
parseur borné, callable réel) et test_job_record_postgres_integration.py
(schémas jetables, Identifier, search_path strict sans public, cleanup suivi,
fermeture y compris threads). project.env chargé uniquement par le processus
test (cinq clés PG_HOST/PG_PORT/PG_DATABASE/PG_USERNAME/PG_PASSWORD) ; valeurs
jamais dans le code, CLI, journaux ou rapports ; sortie rédigée après
suppression des valeurs. Aucune réussite par skip : PG indisponible => échec
explicite. Versions numériques observées seulement, aucune chaîne brute, aucune
prétention C03-C10. Aucune migration de production ni configuration persistante
modifiées ; commandes par mandats séparés.
"""
from __future__ import annotations

import re
import subprocess
import sys
import textwrap
import threading
import unittest
from contextlib import contextmanager
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_INTEGRATION = str(_ROOT / "tests" / "integration")
_TARGET = str(Path(__file__))
_SUPPORT_TARGET = str(Path(_INTEGRATION) / "core_pg_test_support.py")
_MARKER = "CORE_PG_MIGRATIONS_HARNESS_SAFE_OK\n"
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}
_SCHEMA_RE = re.compile(r"c02_[0-9a-f]{16}")
_FIXED_CODE_RE = re.compile(r"[A-Z][A-Z0-9_]*")
_NUMERIC_VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
_NUMERIC_BUILD_RE = re.compile(r"[0-9]+")

_EXPECTED_TABLES = frozenset(
    {
        "pixs_core_user", "pixs_core_identity", "pixs_core_idlink",
        "pixs_core_tenant", "pixs_core_scope", "pixs_core_group",
        "pixs_core_ugroup", "pixs_core_idtenant", "pixs_core_perm",
        "pixs_core_role", "pixs_core_roleperm", "pixs_core_roleassign",
        "pixs_core_policy", "pixs_core_tombstone", "pixs_core_su_binding",
        "pixs_core_su_grant",
    }
)
_MIGRATION_NAME = "0001_core_initial"

_REQUIRED_FLAGS = (
    "applied_initial", "replay_idempotent", "invalid_plan_refused",
    "contract_refused", "interrupted_resumed", "concurrent_single_winner",
    "distinct_schemas_independent", "partial_refused_intact",
    "unknown_migration_refused", "recorder_gap_refused",
    "mixed_search_path_refused", "versions_observed",
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

    support_path = sys.argv[1]
    src_path = sys.argv[2]
    sys.path.insert(0, src_path)

    import django
    import psycopg
    from django.apps import apps
    from django.conf import LazySettings, settings
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
    guards = [mock.Mock(side_effect=AssertionError("forbidden")) for _ in guard_targets]

    with ExitStack() as stack:
        for (target, name, _args), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))

        spec = importlib.util.spec_from_file_location("core_pg_support_under_test", support_path)
        support = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(support)

        for (target, name, args), guard in zip(guard_targets, guards):
            try:
                getattr(target, name)(*args)
            except AssertionError:
                pass
            else:
                raise AssertionError("garde inactive")
            assert guard.call_count == 1
            guard.reset_mock()

        assert callable(support.parse_project_env_text)
        assert callable(support.read_project_env)
        good = (
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=db\n"
            "PG_USERNAME=user\nPG_PASSWORD=secret\n"
        )
        found = support.parse_project_env_text(good)
        assert found["PG_HOST"] == "127.0.0.1" and found["PG_PORT"] == "5432"
        for bad in (
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=db\nPG_USERNAME=user\n",
            "PG_HOST=example.com\nPG_PORT=5432\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=p\n",
            "PG_HOST=127.0.0.1\nPG_PORT=0\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=p\n",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=db\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=p\n",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=pa$ss\n",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=pa`ss\n",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=pa\\ss\n",
            "",
            None,
        ):
            try:
                support.parse_project_env_text(bad)
            except ValueError as caught:
                assert str(caught) == "env invalid" and caught.__cause__ is None
            else:
                raise AssertionError("parseur perméable")
        assert support.read_project_env(None) is None
        assert support.read_project_env("") is None
        assert support.read_project_env("/synthetic/root") is None
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("CORE_PG_MIGRATIONS_HARNESS_SAFE_OK")
    """
).strip()


def _support():
    if _INTEGRATION not in sys.path:
        sys.path.insert(0, _INTEGRATION)
    import core_pg_test_support as support

    return support


def _closed_result():
    result = {"real_pg": False, "phase": "INIT", "reason": "NONE"}
    for key in _REQUIRED_FLAGS:
        result[key] = False
    result["cleanup_ok"] = False
    result["conns_closed"] = False
    result["django_version_num"] = ""
    result["pg_server_version_num"] = ""
    return result


def _combine(result, code):
    if result["reason"] != "NONE":
        return
    if type(code) is str and _FIXED_CODE_RE.fullmatch(code) is not None and code != "NONE":
        result["reason"] = code


def _applied_count(wrapper, schema_name, migration_name):
    from psycopg import sql as psql

    wrapper.ensure_connection()
    query = psql.SQL(
        "SELECT count(*) FROM {}.django_migrations WHERE app = %s AND name = %s"
    ).format(psql.Identifier(schema_name))
    cursor = wrapper.cursor()
    try:
        cursor.execute(query, ("pixs_core", migration_name))
        return int(cursor.fetchone()[0])
    finally:
        cursor.close()


def _worker_apply(alias, slot, results, refs, close_failures, gate, lock_mod, support):
    outcome = None
    try:
        try:
            gate.wait(timeout=30)
        except threading.BrokenBarrierError:
            results[slot] = ("BARRIER_TIMEOUT",)
            return
        try:
            outcome = lock_mod.run_core_initial(alias, origin=None, target="0.1.0")
        except BaseException as exc:
            results[slot] = ("ERROR", type(exc).__name__, getattr(exc, "code", ""))
        else:
            results[slot] = ("OK", outcome)
    finally:
        try:
            support.close_django_connections(refs, close_failures)
        except BaseException:
            close_failures.append("THREAD_CLOSE_FAILED")


def _run_barrier_pair(result, close_failures, refs, support, lock_mod, alias_a, alias_b, state):
    gate = threading.Barrier(3, timeout=30)
    outcomes = {}
    workers = [
        threading.Thread(target=_worker_apply, args=(alias_a, "w1", outcomes, refs, close_failures, gate, lock_mod, support)),
        threading.Thread(target=_worker_apply, args=(alias_b, "w2", outcomes, refs, close_failures, gate, lock_mod, support)),
    ]
    state["workers"] = workers
    for worker in workers:
        worker.start()
    try:
        gate.wait(timeout=30)
    except threading.BrokenBarrierError:
        _combine(result, "BARRIER_TIMEOUT")
    for worker in workers:
        worker.join(timeout=300)
    if any(worker.is_alive() for worker in workers):
        state["skip_drops"] = True
        _combine(result, "WORKER_STILL_ALIVE")
        return None
    return outcomes


def _run_scenarios(result, refs, close_failures, state):
    support = _support()
    import django
    from django.apps import apps
    from django.conf import settings

    names = {}
    for key in ("main", "resume", "partial", "unknown", "gap", "mix_a", "mix_b", "conc", "sole_a", "sole_b"):
        names[key] = support.safe_schema_name()
    state["schemas"] = names
    admin = state["admin"]
    owned = {}
    for key, name in names.items():
        is_owned, reason = support.create_schema(admin, name)
        owned[key] = bool(is_owned)
        if not is_owned or reason != "NONE":
            _combine(result, reason)
            state["owned"] = owned
            return
    state["owned"] = owned
    quoted = {}
    for key, name in names.items():
        quoted[key] = support.quote_search_path(admin, name)
    from pixs.core import migration_lock as lock_mod

    specs = {
        "default": quoted["main"],
        "main": quoted["main"],
        "resume": quoted["resume"],
        "partial": quoted["partial"],
        "unknown": quoted["unknown"],
        "gap": quoted["gap"],
        "conc": quoted["conc"],
        "sole_a": quoted["sole_a"],
        "sole_b": quoted["sole_b"],
        "mixed": quoted["mix_a"] + "," + quoted["mix_b"],
    }
    aliases = {}
    for alias, path in specs.items():
        aliases[alias] = {
            "dbname": state["database"], "user": state["user"],
            "password": state["password"], "host": state["host"],
            "port": state["port"], "options": support.pg_options(path),
        }
    if settings.configured:
        _combine(result, "SETTINGS_ALREADY_CONFIGURED")
        return
    support.configure_django_core_pg(aliases)
    state["configured"] = True
    django.setup()
    django_version = django.get_version()
    if type(django_version) is not str or _NUMERIC_VERSION_RE.fullmatch(django_version) is None:
        _combine(result, "VERSION_UNPROVED")
        return
    result["django_version_num"] = django_version
    from django.db import connections as dj_conns

    main_conn = dj_conns["main"]
    main_conn.ensure_connection()
    with main_conn.cursor() as cursor:
        cursor.execute("SELECT current_setting('server_version_num');")
        row = cursor.fetchone()
    if row is None or type(row[0]) is not str or _NUMERIC_BUILD_RE.fullmatch(row[0]) is None:
        _combine(result, "VERSION_UNPROVED")
        return
    result["pg_server_version_num"] = row[0]
    result["versions_observed"] = True

    if lock_mod.run_core_initial("main", origin=None, target="0.1.0") != "applied":
        _combine(result, "APPLY_NOT_PROVED")
        return
    if support.table_names_of_current_schema(main_conn) & _EXPECTED_TABLES != _EXPECTED_TABLES:
        _combine(result, "TABLES_NOT_PROVED")
        return
    from django.db.migrations.recorder import MigrationRecorder

    if ("pixs_core", _MIGRATION_NAME) not in MigrationRecorder(main_conn).applied_migrations():
        _combine(result, "RECORDER_NOT_PROVED")
        return
    if _applied_count(main_conn, names["main"], _MIGRATION_NAME) != 1:
        _combine(result, "RECORDER_NOT_PROVED")
        return
    result["applied_initial"] = True

    if lock_mod.run_core_initial("main", origin=None, target="0.1.0") != "already_applied":
        _combine(result, "REPLAY_NOT_IDEMPOTENT")
        return
    if _applied_count(main_conn, names["main"], _MIGRATION_NAME) != 1:
        _combine(result, "REPLAY_NOT_IDEMPOTENT")
        return
    result["replay_idempotent"] = True

    count_before = _applied_count(main_conn, names["main"], _MIGRATION_NAME)
    for bad_origin, bad_target in (("x", "0.1.0"), (None, "9.9.9")):
        try:
            lock_mod.run_core_initial("main", origin=bad_origin, target=bad_target)
        except lock_mod.MigrationLockError:
            pass
        else:
            _combine(result, "INVALID_PLAN_ACCEPTED")
            return
    if _applied_count(main_conn, names["main"], _MIGRATION_NAME) != count_before:
        _combine(result, "INVALID_PLAN_ALTERED_STATE")
        return
    result["invalid_plan_refused"] = True

    import importlib as importlib_mod
    from unittest import mock as mock_mod

    module = importlib_mod.import_module("pixs.core.migrations.0001_core_initial")
    with mock_mod.patch.object(module.Migration, "pixs_target", "9.9.9"):
        try:
            lock_mod.verify_migration_contract(None, "0.1.0")
        except lock_mod.MigrationLockError:
            pass
        else:
            _combine(result, "ALTERED_CONTRACT_ACCEPTED")
            return
    result["contract_refused"] = True

    from django.db.migrations.executor import MigrationExecutor as ExecutorCls

    class _ControlledInterrupt(Exception):
        pass

    real_migrate = ExecutorCls.migrate

    def _explode(self, targets, plan=None, state=None, fake=False, fake_initial=False):
        real_migrate(self, targets, plan=plan, state=state, fake=fake, fake_initial=fake_initial)
        raise _ControlledInterrupt()

    resume_conn = dj_conns["resume"]
    with mock_mod.patch.object(ExecutorCls, "migrate", _explode):
        try:
            lock_mod.run_core_initial("resume", origin=None, target="0.1.0")
        except _ControlledInterrupt:
            pass
        else:
            _combine(result, "INTERRUPT_NOT_SURFACED")
            return
    if support.table_names_of_current_schema(resume_conn) & _EXPECTED_TABLES:
        _combine(result, "INTERRUPT_NOT_ROLLED_BACK")
        return
    if support.table_exists(admin, names["resume"], "django_migrations"):
        _combine(result, "INTERRUPT_NOT_ROLLED_BACK")
        return
    if lock_mod.run_core_initial("resume", origin=None, target="0.1.0") != "applied":
        _combine(result, "RESUME_NOT_PROVED")
        return
    result["interrupted_resumed"] = True

    outcomes = _run_barrier_pair(result, close_failures, refs, support, lock_mod, "conc", "conc", state)
    if outcomes is None:
        return
    winners = [slot for slot, item in outcomes.items() if item == ("OK", "applied")]
    losers_ok = all(
        outcomes.get(slot) == ("OK", "already_applied")
        or outcomes.get(slot) == ("ERROR", "MigrationLockError", "EXECUTEUR_CONCURRENT")
        for slot in ("w1", "w2")
        if slot not in winners
    )
    if len(winners) != 1 or not losers_ok:
        _combine(result, "SINGLE_WINNER_NOT_PROVED")
        return
    result["concurrent_single_winner"] = True

    sole = _run_barrier_pair(result, close_failures, refs, support, lock_mod, "sole_a", "sole_b", state)
    if sole is None:
        return
    if sole.get("w1") != ("OK", "applied") or sole.get("w2") != ("OK", "applied"):
        _combine(result, "SCHEMAS_NOT_INDEPENDENT")
        return
    result["distinct_schemas_independent"] = True

    from psycopg import sql as psql

    partial_conn = dj_conns["partial"]
    partial_conn.ensure_connection()
    with partial_conn.cursor() as cursor:
        cursor.execute(
            psql.SQL("CREATE TABLE {}.{} (user_id text PRIMARY KEY)").format(
                psql.Identifier(names["partial"]), psql.Identifier("pixs_core_user")
            )
        )
    try:
        lock_mod.run_core_initial("partial", origin=None, target="0.1.0")
    except lock_mod.MigrationLockError as caught:
        if caught.code != "ETAT_PARTIEL_REFUSE":
            _combine(result, "PARTIAL_WRONG_REFUSAL")
            return
    else:
        _combine(result, "PARTIAL_ACCEPTED")
        return
    if not support.table_exists(admin, names["partial"], "pixs_core_user"):
        _combine(result, "PARTIAL_ERASED")
        return
    if support.table_exists(admin, names["partial"], "django_migrations"):
        _combine(result, "PARTIAL_ALTERED")
        return
    result["partial_refused_intact"] = True

    for alias, key, inserted, expected_code in (
        ("unknown", "unknown", "9999_unknown", "MIGRATION_INCONNUE"),
        ("gap", "gap", _MIGRATION_NAME, "ETAT_PARTIEL_REFUSE"),
    ):
        schema = names[key]
        wrapper = dj_conns[alias]
        wrapper.ensure_connection()
        with wrapper.cursor() as cursor:
            cursor.execute(
                psql.SQL(
                    "CREATE TABLE {}.django_migrations (id BIGSERIAL PRIMARY KEY, "
                    "app VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, "
                    "applied TIMESTAMPTZ NOT NULL DEFAULT now())"
                ).format(psql.Identifier(schema))
            )
            cursor.execute(
                psql.SQL("INSERT INTO {}.django_migrations (app, name) VALUES (%s, %s)").format(
                    psql.Identifier(schema)
                ),
                ("pixs_core", inserted),
            )
        try:
            lock_mod.run_core_initial(alias, origin=None, target="0.1.0")
        except lock_mod.MigrationLockError as caught:
            if caught.code != expected_code:
                _combine(result, "RECORDER_WRONG_REFUSAL")
                return
        else:
            _combine(result, "RECORDER_GAP_ACCEPTED")
            return
        if support.table_names_of_current_schema(wrapper) & _EXPECTED_TABLES:
            _combine(result, "RECORDER_STATE_ALTERED")
            return
    result["unknown_migration_refused"] = True
    result["recorder_gap_refused"] = True

    try:
        lock_mod.run_core_initial("mixed", origin=None, target="0.1.0")
    except lock_mod.MigrationLockError as caught:
        if caught.code != "NAMESPACE_AMBIGU":
            _combine(result, "MIXED_WRONG_REFUSAL")
            return
    else:
        _combine(result, "MIXED_SEARCH_PATH_ACCEPTED")
        return
    if support.table_exists(admin, names["mix_a"], "django_migrations"):
        _combine(result, "MIXED_STATE_ALTERED")
        return
    if support.table_exists(admin, names["mix_b"], "django_migrations"):
        _combine(result, "MIXED_STATE_ALTERED")
        return
    result["mixed_search_path_refused"] = True


def _cleanup_inside(result, refs, close_failures, state):
    support = _support()
    if state.get("configured"):
        support.close_django_connections(refs, close_failures)
    if state.get("skip_drops"):
        state["cleaned"] = False
        _combine(result, "CLEANUP_SKIPPED_LIVE_THREAD")
        return
    admin = state.get("admin")
    owned = state.get("owned") or {}
    schemas = state.get("schemas") or {}
    dropped = True
    if admin is None:
        dropped = False
    else:
        for key, is_owned in owned.items():
            if is_owned:
                if not support.drop_schema_if_owned(admin, schemas[key], True):
                    dropped = False
    state["cleaned"] = bool(dropped)
    if not dropped:
        _combine(result, "CLEANUP_FAILED")


def _compute_result(result, refs, close_failures, state):
    try:
        import psycopg as _pgmod
        from django.db import DatabaseError as _DBError
        from django.db import InterfaceError as _IFError

        _close_errors = (_pgmod.Error, OSError, _DBError, _IFError)
    except ImportError:
        _close_errors = (OSError,)
    if not state.get("cleaned", False):
        _combine(result, "CLEANUP_FAILED")
    all_closed = not close_failures
    for connection in refs:
        try:
            all_closed = all_closed and bool(connection.closed)
        except _close_errors:
            all_closed = False
    result["conns_closed"] = bool(all_closed)
    if not all_closed:
        _combine(result, "CONNECTION_CLOSE_FAILED")
    result["real_pg"] = bool(
        result["reason"] == "NONE"
        and state.get("cleaned", False)
        and result["conns_closed"]
        and all(result[key] for key in _REQUIRED_FLAGS)
    )
    result["cleanup_ok"] = bool(state.get("cleaned", False))
    result["phase"] = "COMPLETE"
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"


def run_real_core_pg_migrations(root_str):
    """Callable PG réel invoqué uniquement par une commande CAB dédiée."""
    support = _support()
    result = _closed_result()
    refs = []
    close_failures = []
    state = {
        "schemas": {}, "owned": {}, "configured": False, "admin": None,
        "database": None, "user": None, "password": None,
        "host": None, "port": None, "cleaned": False, "skip_drops": False,
    }
    with support.mask_output():
        try:
            if type(root_str) is not str or root_str == "":
                _combine(result, "ROOT_INVALID")
            else:
                try:
                    resolved = str(Path(root_str).resolve())
                except (OSError, RuntimeError, ValueError):
                    resolved = ""
                if resolved != _EXPECTED_ROOT:
                    _combine(result, "ROOT_MISMATCH")
                else:
                    found = support.read_project_env(root_str)
                    if not isinstance(found, dict):
                        _combine(result, "ENV_REFUSED")
                    else:
                        values = tuple(found.get(name) for name in support.WANTED_KEYS)
                        if any(type(value) is not str or value == "" for value in values):
                            _combine(result, "ENV_INCOMPLETE")
                        else:
                            state["host"], state["port"], state["database"], state["user"], state["password"] = values
                            del values, found
                            try:
                                with support.managed_pg_connection(
                                    state["host"], int(state["port"], 10), state["database"],
                                    state["user"], state["password"], refs, close_failures,
                                ) as admin:
                                    state["admin"] = admin
                                    result["phase"] = "ENV_READY"
                                    try:
                                        _run_scenarios(result, refs, close_failures, state)
                                    finally:
                                        _cleanup_inside(result, refs, close_failures, state)
                            except BaseException:
                                raise
                            if state.get("admin") is None or not state["admin"].closed:
                                _combine(result, "ADMIN_CLOSE_FAILED")
        except BaseException as exc:
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            try:
                from pixs.core import migration_lock as _lock

                _is_lock_error = isinstance(exc, _lock.MigrationLockError)
                _code = getattr(exc, "code", "")
            except ImportError:
                _is_lock_error = False
                _code = ""
            if _is_lock_error and type(_code) is str and _FIXED_CODE_RE.fullmatch(_code) is not None:
                _combine(result, _code)
            elif isinstance(exc, AssertionError):
                _combine(result, "ASSERTION_FAILED")
            else:
                _combine(result, "PG_FAILED")
        finally:
            try:
                _compute_result(result, refs, close_failures, state)
            except BaseException:
                result["real_pg"] = False
                result["cleanup_ok"] = False
                result["conns_closed"] = False
                result["phase"] = "COMPLETE"
                _combine(result, "FINALIZATION_FAILED")
    return result


class CorePgMigrationsHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SUPPORT_TARGET, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


class CorePgEnvParserTests(unittest.TestCase):
    def test_parser_accepts_five_keys(self):
        support = _support()
        found = support.parse_project_env_text(
            "PG_HOST=localhost\nPG_PORT=5433\nPG_DATABASE=db\nPG_USERNAME=u\nPG_PASSWORD=p\n"
        )
        self.assertEqual(found["PG_HOST"], "localhost")
        self.assertEqual(found["PG_PORT"], "5433")

    def test_parser_refuses(self):
        support = _support()
        cases = [
            "",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=d\nPG_USERNAME=u\n",
            "PG_HOST=example.com\nPG_PORT=5432\nPG_DATABASE=d\nPG_USERNAME=u\nPG_PASSWORD=p\n",
            "PG_HOST=127.0.0.1\nPG_PORT=0\nPG_DATABASE=d\nPG_USERNAME=u\nPG_PASSWORD=p\n",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=d\nPG_DATABASE=d\nPG_USERNAME=u\nPG_PASSWORD=p\n",
            "PG_HOST=127.0.0.1\nPG_PORT=5432\nPG_DATABASE=d\nPG_USERNAME=u\nPG_PASSWORD=pa$ss\n",
            None,
            "x" * 65537,
        ]
        for text in cases:
            with self.assertRaises(ValueError) as caught:
                support.parse_project_env_text(text)
            self.assertIsNone(caught.exception.__cause__)
            self.assertEqual(str(caught.exception), "env invalid")


if __name__ == "__main__":
    unittest.main()
