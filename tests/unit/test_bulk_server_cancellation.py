"""Façade demande CANCEL : gardes hostiles avant I/O, processus frais isolés."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src")
_TESTS = str(_ROOT / "tests")
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
_MARKER_INERT = "BULK_SERVER_CANCELLATION_INERT_SAFE_OK\n"
_MARKER_UNIT = "BULK_SERVER_CANCELLATION_UNIT_SAFE_OK\n"
_CHILD_INERT = textwrap.dedent(
    r'''
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from unittest import mock

    sys.path.insert(0, sys.argv[1])
    sys.path.insert(0, sys.argv[2])

    counters = {"network": 0, "process": 0, "environment": 0}

    def _make_guard(bucket):
        def _blocked(*args, **kwargs):
            counters[bucket] += 1
            raise AssertionError("forbidden-" + bucket)
        return _blocked

    class _NoEnvironment:
        def _blocked(self, *args, **kwargs):
            counters["environment"] += 1
            raise AssertionError("forbidden-environment")
        __getitem__ = get = __iter__ = __len__ = __contains__ = _blocked

    class _FrameworkBlocker:
        def find_module(self, name, path=None):
            if name == "django" or name.startswith("django.") or name == "psycopg" or name.startswith("psycopg"):
                return self
            return None
        def load_module(self, name):
            raise AssertionError("framework-import-blocked")
        def find_spec(self, name, path=None, target=None):
            if name == "django" or name.startswith("django.") or name == "psycopg" or name.startswith("psycopg"):
                raise AssertionError("framework-import-blocked")
            return None

    sys.meta_path.insert(0, _FrameworkBlocker())
    with ExitStack() as stack:
        stack.enter_context(mock.patch.object(os, "environ", _NoEnvironment()))
        stack.enter_context(mock.patch.object(os, "getenv", side_effect=_make_guard("environment")))
        stack.enter_context(mock.patch.object(socket.socket, "connect", side_effect=_make_guard("network")))
        stack.enter_context(mock.patch.object(socket, "create_connection", side_effect=_make_guard("network")))
        stack.enter_context(mock.patch.object(subprocess, "Popen", side_effect=_make_guard("process")))
        stack.enter_context(mock.patch.object(subprocess, "run", side_effect=_make_guard("process")))
        try:
            socket.socket.connect(object(), ("127.0.0.1", 0))
        except AssertionError:
            pass
        else:
            raise AssertionError("garde inactive")
        try:
            subprocess.run(["true"])
        except AssertionError:
            pass
        else:
            raise AssertionError("garde inactive")
        for probe in (lambda: os.getenv("CISMP_ENV_PROBE"), lambda: os.environ.get("CISMP_ENV_PROBE")):
            try:
                probe()
            except AssertionError:
                pass
            else:
                raise AssertionError("garde environnement inactive")
        assert counters == {"network": 1, "process": 1, "environment": 2}, counters
        for key in counters:
            counters[key] = 0
        import pixs.backend.bulk_server_cancellation as module
        assert callable(module.request_bulk_cancellation), module
        assert "django" not in sys.modules, "django charge a l import"
        assert "psycopg" not in sys.modules, "psycopg charge a l import"
        assert counters == {"network": 0, "process": 0, "environment": 0}, counters
    print("BULK_SERVER_CANCELLATION_INERT_SAFE_OK")
    '''
).strip()
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
            SECRET_KEY="unit-synthetic-only",
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "bulk_server_cancel_synthetic"}},
            LOGGING_CONFIG=None,
            MIDDLEWARE=(),
            USE_TZ=True,
        )
        django.setup()
        from django.core.exceptions import ValidationError
        from django.db import DatabaseError, connections
        from pixs.backend.bulk_runtime_records import _INT64_MAX
        from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
        from pixs.backend.bulk_server_cancellation import request_bulk_cancellation
        from pixs.backend.bulk_trusted_ports import _BulkTrustedPorts, compose_bulk_trusted_ports
        from pixs.kernel.diagnostics import VALIDATE
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
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
            def __bool__(self):
                raise AssertionError("comportement etranger")
        class HostileInt:
            def __eq__(self, other):
                raise AssertionError("comparaison etrangere")
            def __bool__(self):
                raise AssertionError("comportement etranger")
            def __index__(self):
                raise AssertionError("comportement etranger")
        class SubPorts(_BulkTrustedPorts):
            pass
        class SubRepo(BulkRuntimeRepository):
            pass
        class FakeRepo:
            pass
        class HostileVendor:
            def __eq__(self, other):
                raise AssertionError("comparaison etrangere")
            def __str__(self):
                raise AssertionError("echo etranger")
        def _context():
            return {"subject_id": "actor-test", "tenant_id": "tenant-test", "perimeter_reference": "perimeter-test", "context_reference": "context-test"}
        def _allow():
            return {"decision": "ALLOW", "resolved_context": dict(_context())}
        class _Authority:
            def __init__(self, response=None, fail=False):
                self.calls = []
                self.response = _allow() if response is None else response
                self.fail = fail
            def check(self, context, action, operation, resource):
                self.calls.append((context, action, operation, resource))
                if self.fail:
                    raise RuntimeError("provider-synthetic")
                return self.response
        class _Resolver:
            def __init__(self):
                self.calls = []
            def resolve(self, reference, version, owner):
                self.calls.append((reference, version, owner))
                raise AssertionError("resolve non appele pour CANCEL")
        def _compose(authority):
            return compose_bulk_trusted_ports(
                authority_adapter=authority,
                mapping_resolver=_Resolver(),
                mapping_descriptors=(),
                owner_declarations=(),
                governance_adapter=None,
                owner_command_adapter=None,
                owner_projection_adapter=None,
                audit_adapter=None,
            )
        def _repo():
            return BulkRuntimeRepository(using="default", failure_codes=frozenset({"TECHNICAL"}))
        def _refused(call):
            result, diagnostics = call()
            assert result is None, result
            assert type(diagnostics) is list and diagnostics, diagnostics
            for item in diagnostics:
                assert item.step is VALIDATE, item
                assert "LEAK-MARKER" not in str(item), item
            return diagnostics
        for bad_op in (None, "", "a\x00b", "LEAK-MARKER\x00", "op-\ud800", b"op", 0, Hostile(), ForeignStr("op")):
            _refused(lambda: request_bulk_cancellation(trusted_ports=_compose(_Authority()), runtime_repository=_repo(), server_context=object(), operation_id=bad_op, expected_revision=1))
        for bad_rev in (None, True, False, 0, -1, "1", 1.0, Hostile(), HostileInt(), ForeignInt(1), _INT64_MAX, _INT64_MAX + 1):
            _refused(lambda: request_bulk_cancellation(trusted_ports=_compose(_Authority()), runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=bad_rev))
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
        for bad_ports in (None, object(), Hostile(), SubPorts.__new__(SubPorts)):
            authority_probe = _Authority()
            _refused(lambda: request_bulk_cancellation(trusted_ports=bad_ports, runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=1))
        for bad_repo in (None, object(), Hostile(), FakeRepo(), SubRepo.__new__(SubRepo)):
            authority = _Authority()
            ports = _compose(authority)
            _refused(lambda: request_bulk_cancellation(trusted_ports=ports, runtime_repository=bad_repo, server_context=object(), operation_id="op-test", expected_revision=1))
            assert authority.calls == [], authority.calls
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
        repo = _repo()
        object.__delattr__(repo, "_using")
        authority = _Authority()
        _refused(lambda: request_bulk_cancellation(trusted_ports=_compose(authority), runtime_repository=repo, server_context=object(), operation_id="op-test", expected_revision=1))
        assert authority.calls == [], authority.calls
        repo = _repo()
        object.__setattr__(repo, "_using", ForeignStr("default"))
        authority = _Authority()
        _refused(lambda: request_bulk_cancellation(trusted_ports=_compose(authority), runtime_repository=repo, server_context=object(), operation_id="op-test", expected_revision=1))
        assert authority.calls == [], authority.calls
        repo = _repo()
        object.__setattr__(repo, "_using", "undeclared-alias-synthetic")
        authority = _Authority()
        _refused(lambda: request_bulk_cancellation(trusted_ports=_compose(authority), runtime_repository=repo, server_context=object(), operation_id="op-test", expected_revision=1))
        assert authority.calls == [], authority.calls
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
        wrapper = connections["default"]
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
        for vendor in ("mysql", "", HostileVendor(), ForeignStr("postgresql"), 0):
            with mock.patch.object(wrapper, "vendor", vendor):
                authority = _Authority()
                ports = _compose(authority)
                _refused(lambda: request_bulk_cancellation(trusted_ports=ports, runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=1))
                assert authority.calls == [], authority.calls
            assert counters == {"db": 0, "network": 0, "process": 0}, counters
        assert wrapper.vendor == "postgresql", wrapper.vendor
        for response in ({"decision": "DENY", "resolved_context": None}, {"decision": "UNAVAILABLE", "resolved_context": None}, {"decision": "ALLOW", "resolved_context": None}, {"decision": "ALLOW", "resolved_context": dict(_context(), tenant_id=None)}):
            authority = _Authority(response)
            ports = _compose(authority)
            before = dict(counters)
            _refused(lambda: request_bulk_cancellation(trusted_ports=ports, runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=1))
            assert counters == before, counters
            assert len(authority.calls) == 1, authority.calls
        authority = _Authority(fail=True)
        ports = _compose(authority)
        before = dict(counters)
        _refused(lambda: request_bulk_cancellation(trusted_ports=ports, runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=1))
        assert counters == before, counters
        for key in counters:
            counters[key] = 0
        server_context = object()
        authority = _Authority()
        ports = _compose(authority)
        try:
            request_bulk_cancellation(trusted_ports=ports, runtime_repository=_repo(), server_context=server_context, operation_id="op-target", expected_revision=1)
        except GuardBlocked as blocked:
            assert str(blocked) == "db", blocked
        else:
            raise AssertionError("flux ALLOW non prouve jusqu au SQL garde")
        assert authority.calls == [(server_context, "CANCEL", "op-target", None)], authority.calls
        assert authority.calls[0][0] is server_context, authority.calls
        assert counters == {"db": 1, "network": 0, "process": 0}, counters
        for key in counters:
            counters[key] = 0
        with mock.patch.object(PGWrapper, "get_new_connection", side_effect=DatabaseError("synthetic")):
            result, diagnostics = request_bulk_cancellation(trusted_ports=_compose(_Authority()), runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=1)
            assert result is None and diagnostics, diagnostics
            assert "LEAK-MARKER" not in str(diagnostics), diagnostics
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
        with mock.patch.object(PGWrapper, "get_new_connection", side_effect=RuntimeError("unexpected-synthetic")):
            try:
                request_bulk_cancellation(trusted_ports=_compose(_Authority()), runtime_repository=_repo(), server_context=object(), operation_id="op-test", expected_revision=1)
            except RuntimeError:
                pass
            else:
                raise AssertionError("erreur inattendue masquee")
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
    print("BULK_SERVER_CANCELLATION_UNIT_SAFE_OK")
    '''
).strip()


class BulkServerCancellationInertTests(unittest.TestCase):
    def test_inert_import_without_framework(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD_INERT, _SRC, _TESTS],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER_INERT)


class BulkServerCancellationUnitSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TESTS],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER_UNIT)


if __name__ == "__main__":
    unittest.main()
