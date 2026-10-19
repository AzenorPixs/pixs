"""Demande interne cancellation_requested : gardes hostiles avant I/O, processus frais sous gardes."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src")
_TESTS = str(_ROOT / "tests")
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
_MARKER = "BULK_CANCELLATION_REQUEST_OFFLINE_SAFE_OK\n"
_CHILD = textwrap.dedent(
    r'''
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from unittest import mock

    sys.path.insert(0, sys.argv[1])
    sys.path.insert(0, sys.argv[2])

    import django
    from django.apps import apps
    from django.conf import settings

    assert not settings.configured
    assert not apps.ready

    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

    class GuardBlocked(Exception):
        pass

    counters = {"db": 0, "network": 0, "process": 0}

    def _make_guard(bucket):
        def _blocked(*args, **kwargs):
            counters[bucket] += 1
            raise GuardBlocked(bucket)
        return _blocked

    guard_targets = [
        (PGWrapper, "get_new_connection", "db"),
        (psycopg, "connect", "db"),
        (psycopg.Connection, "connect", "db"),
        (socket.socket, "connect", "network"),
        (socket, "create_connection", "network"),
        (subprocess, "Popen", "process"),
        (subprocess, "run", "process"),
    ]
    with ExitStack() as stack:
        for target, name, bucket in guard_targets:
            stack.enter_context(mock.patch.object(target, name, side_effect=_make_guard(bucket)))
        def _probe(call, bucket):
            try:
                call()
            except GuardBlocked as error:
                assert str(error) == bucket, error
                return
            raise AssertionError("garde non declenchee")
        _probe(lambda: PGWrapper.get_new_connection(object(), {}), "db")
        _probe(lambda: psycopg.connect(), "db")
        _probe(lambda: psycopg.Connection.connect(), "db")
        _probe(lambda: socket.socket.connect(object(), ("127.0.0.1", 0)), "network")
        _probe(lambda: socket.create_connection(("127.0.0.1", 0)), "network")
        _probe(lambda: subprocess.Popen(["true"]), "process")
        _probe(lambda: subprocess.run(["true"]), "process")
        assert counters == {"db": 3, "network": 2, "process": 2}, counters
        for key in counters:
            counters[key] = 0
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            INSTALLED_APPS=["pixs.backend"],
            SECRET_KEY="unit-offline-synthetic-only",
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "bulk_cancel_offline_synthetic"}},
            LOGGING_CONFIG=None,
            MIDDLEWARE=(),
            USE_TZ=True,
        )
        django.setup()
        from django.core.exceptions import ValidationError
        from pixs.backend.bulk_runtime_records import _INT64_MAX
        from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
        repo = BulkRuntimeRepository(using="default", failure_codes=frozenset({"TECHNICAL"}))
        class Hostile:
            def __bool__(self):
                raise AssertionError("comportement etranger")
            def __eq__(self, other):
                raise AssertionError("comparaison etrangere")
            def __lt__(self, other):
                raise AssertionError("comparaison etrangere")
            def __str__(self):
                raise AssertionError("echo etranger")
        class ForeignStr(str):
            def encode(self, *args, **kwargs):
                raise AssertionError("comportement etranger")
        class ForeignInt(int):
            def __eq__(self, other):
                raise AssertionError("comparaison etrangere")
            def __lt__(self, other):
                raise AssertionError("comparaison etrangere")
            def __bool__(self):
                raise AssertionError("comportement etranger")
        class HostileInt:
            def __eq__(self, other):
                raise AssertionError("comparaison etrangere")
            def __lt__(self, other):
                raise AssertionError("comparaison etrangere")
            def __gt__(self, other):
                raise AssertionError("comparaison etrangere")
            def __bool__(self):
                raise AssertionError("comportement etranger")
            def __index__(self):
                raise AssertionError("comportement etranger")
        def _refused(call):
            try:
                call()
            except ValidationError:
                return
            raise AssertionError("refus attendu absent")
        for bad_op in (None, "", "a\x00b", "op-\ud800", "op-\udc00", b"op", 0, Hostile(), ForeignStr("op")):
            _refused(lambda: repo.request_cancellation(operation_id=bad_op, expected_revision=1))
        for bad_rev in (None, True, False, 0, -1, "1", 1.0, Hostile(), HostileInt(), ForeignInt(1), _INT64_MAX, _INT64_MAX + 1):
            _refused(lambda: repo.request_cancellation(operation_id="op-test", expected_revision=bad_rev))
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
    print("BULK_CANCELLATION_REQUEST_OFFLINE_SAFE_OK")
    '''
).strip()


class BulkCancellationRequestOfflineSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TESTS],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
