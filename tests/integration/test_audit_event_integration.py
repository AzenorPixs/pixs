"""Intégration sûre de la représentation d’événement d’audit : import et validation gardés."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "AUDIT_EVENT_SAFE_INTEGRATION_OK\n"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONPATH": _SRC,
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(
    r'''
    import builtins
    import dataclasses
    import datetime
    import importlib.util
    import io
    import os
    import socket
    import subprocess
    import sys
    import time

    sys.path.insert(0, sys.argv[1])

    from unittest import mock

    FORBIDDEN_IMPORT_PREFIXES = ("django", "psycopg", "psycopg2", "psycopg_pool", "psycopg_binary")
    CALENDAR_VALID = "2024-02-29T00:00:00Z"
    CALENDAR_INVALID = "2026-02-29T00:00:00Z"


    class ForbiddenImportFinder:
        def __init__(self):
            self.calls = []

        def find_spec(self, fullname, path=None, target=None):
            for prefix in FORBIDDEN_IMPORT_PREFIXES:
                if fullname == prefix or fullname.startswith(prefix + "."):
                    self.calls.append(fullname)
                    raise AssertionError("forbidden base import")
            return None


    import_guard = ForbiddenImportFinder()
    sys.meta_path.insert(0, import_guard)

    original_datetime = datetime.datetime
    original_date = datetime.date


    class GuardedDatetime(original_datetime):
        calendar_calls = []
        clock_calls = []

        @classmethod
        def fromisoformat(cls, value):
            cls.calendar_calls.append(value)
            return original_datetime.fromisoformat(value)

        @classmethod
        def now(cls, tz=None):
            cls.clock_calls.append("now")
            raise AssertionError("forbidden clock")

        @classmethod
        def today(cls):
            cls.clock_calls.append("today")
            raise AssertionError("forbidden clock")

        @classmethod
        def utcnow(cls):
            cls.clock_calls.append("utcnow")
            raise AssertionError("forbidden clock")


    datetime.datetime = GuardedDatetime
    class GuardedDate(original_date):
        clock_calls = []

        @classmethod
        def today(cls):
            cls.clock_calls.append("today")
            raise AssertionError("forbidden date clock")

    datetime.date = GuardedDate
    try:
        datetime.date.today()
    except AssertionError:
        pass
    else:
        raise AssertionError("date clock guard inactive")
    assert GuardedDate.clock_calls == ["today"]
    GuardedDate.clock_calls.clear()


    class GuardedEnvironment:
        def __init__(self):
            self.calls = []

        def _forbid(self, name):
            self.calls.append(name)
            raise AssertionError("forbidden environment")

        def __getitem__(self, key):
            self._forbid("getitem")

        def get(self, key, default=None):
            self._forbid("get")


        def __iter__(self):
            self._forbid("__iter__")

        def __len__(self):
            self._forbid("__len__")

        def __contains__(self, key):
            self._forbid("__contains__")

        def __setitem__(self, key, value):
            self._forbid("__setitem__")

        def __delitem__(self, key):
            self._forbid("__delitem__")

        def keys(self):
            self._forbid("keys")

        def values(self):
            self._forbid("values")

        def items(self):
            self._forbid("items")

        def copy(self):
            self._forbid("copy")

        def setdefault(self, key, default=None):
            self._forbid("setdefault")

        def pop(self, key, default=None):
            self._forbid("pop")

        def update(self, *args, **kwargs):
            self._forbid("update")


    environment_guard = GuardedEnvironment()
    os.environ = environment_guard

    function_guards = []


    def install_function_guard(target, name, args):
        guard = mock.Mock(side_effect=AssertionError("forbidden"))
        setattr(target, name, guard)
        function_guards.append((target, name, args, guard))


    install_function_guard(socket.socket, "connect", (object(), ("127.0.0.1", 0)))
    install_function_guard(socket, "create_connection", (("127.0.0.1", 0),))
    install_function_guard(subprocess, "Popen", (["true"],))
    install_function_guard(subprocess, "run", (["true"],))
    install_function_guard(time, "time", ())
    install_function_guard(time, "monotonic", ())
    install_function_guard(time, "perf_counter", ())
    install_function_guard(os, "getenv", ("PATH",))
    install_function_guard(time, "localtime", ())
    install_function_guard(time, "gmtime", ())
    install_function_guard(time, "sleep", (0,))
    install_function_guard(os, "system", ("true",))
    install_function_guard(os, "popen", ("true",))
    install_function_guard(os, "execv", ("/usr/bin/true", ["true"]))
    install_function_guard(os, "spawnl", (os.P_WAIT, "/usr/bin/true", "true"))

    for target, name, args, guard in function_guards:
        try:
            getattr(target, name)(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError("function guard inactive")
        assert guard.call_count == 1
        guard.reset_mock()

    for forbidden in FORBIDDEN_IMPORT_PREFIXES:
        try:
            importlib.util.find_spec(forbidden)
        except AssertionError:
            pass
        else:
            raise AssertionError("import guard inactive")
        assert import_guard.calls == [forbidden]
        import_guard.calls.clear()

    for method_name in ("now", "today", "utcnow"):
        try:
            getattr(datetime.datetime, method_name)()
        except AssertionError:
            pass
        else:
            raise AssertionError("clock guard inactive")

    assert GuardedDatetime.clock_calls == ["now", "today", "utcnow"]
    GuardedDatetime.clock_calls.clear()

    for operation, expected_call in (
        (lambda: os.environ["PATH"], "getitem"),
        (lambda: os.environ.get("PATH"), "get"),
    ):
        try:
            operation()
        except AssertionError:
            pass
        else:
            raise AssertionError("environment guard inactive")
        assert environment_guard.calls[-1] == expected_call

    assert environment_guard.calls == ["getitem", "get"]
    environment_guard.calls.clear()
    extra_environment_probes = (
        (lambda: iter(os.environ), "__iter__"),
        (lambda: len(os.environ), "__len__"),
        (lambda: "PATH" in os.environ, "__contains__"),
        (lambda: os.environ.__setitem__("PATH", "synthetic"), "__setitem__"),
        (lambda: os.environ.__delitem__("PATH"), "__delitem__"),
        (lambda: os.environ.keys(), "keys"),
        (lambda: os.environ.values(), "values"),
        (lambda: os.environ.items(), "items"),
        (lambda: os.environ.copy(), "copy"),
        (lambda: os.environ.setdefault("PATH"), "setdefault"),
        (lambda: os.environ.pop("PATH"), "pop"),
        (lambda: os.environ.update({}), "update"),
    )
    for operation, expected_route in extra_environment_probes:
        try:
            operation()
        except AssertionError:
            pass
        else:
            raise AssertionError("environment guard inactive")
        assert environment_guard.calls == [expected_route]
        environment_guard.calls.clear()

    from pixs.kernel.audit_event import AuditEvent, validate_audit_event
    from pixs.kernel.diagnostics import VALIDATE

    # Contrôle après bootstrap : aucun accès applicatif interdit masqué.
    for _, _, _, guard in function_guards:
        assert guard.call_count == 0
    assert environment_guard.calls == []
    assert import_guard.calls == []
    assert GuardedDatetime.clock_calls == []
    assert GuardedDate.clock_calls == []

    # Imports normaux achevés ; sondes fichiers armées pour la validation.
    file_guard_calls = []


    def make_file_guard(route):
        def forbidden(*args, **kwargs):
            file_guard_calls.append(route)
            raise AssertionError("forbidden file access")

        return forbidden


    file_guard_targets = (
        (builtins, "open"),
        (io, "open"),
        (os, "fdopen"),
        (os, "stat"),
        (os, "scandir"),
        (os, "unlink"),
        (os, "rename"),
        (os, "open"),
        (os, "read"),
        (os, "write"),
        (os, "listdir"),
        (os, "remove"),
    )
    for target, name in file_guard_targets:
        setattr(target, name, make_file_guard(f"{'builtins' if target is builtins else 'io' if target is io else 'os'}.{name}"))

    file_probe_operations = (
        (lambda: builtins.open(os.devnull), "builtins.open"),
        (lambda: io.open(os.devnull), "io.open"),
        (lambda: os.fdopen(3), "os.fdopen"),
        (lambda: os.stat("."), "os.stat"),
        (lambda: os.scandir("."), "os.scandir"),
        (lambda: os.unlink(os.devnull), "os.unlink"),
        (lambda: os.rename(os.devnull, os.devnull), "os.rename"),
        (lambda: os.open(os.devnull, os.O_RDONLY), "os.open"),
        (lambda: os.read(3, 1), "os.read"),
        (lambda: os.write(3, b""), "os.write"),
        (lambda: os.listdir("."), "os.listdir"),
        (lambda: os.remove(os.devnull), "os.remove"),
    )
    for operation, expected_route in file_probe_operations:
        try:
            operation()
        except AssertionError:
            pass
        else:
            raise AssertionError("file guard inactive")
        assert file_guard_calls[-1] == expected_route

    assert file_guard_calls == [expected for _, expected in file_probe_operations]
    file_guard_calls.clear()

    def values(**overrides):
        result = {
            "event_id": "evt-integration",
            "occurred_at": "2026-01-01T00:00:00Z",
            "actor_reference": "actor-integration",
            "tenant_reference": "tenant-integration",
            "action": "synthetic.read",
            "resource_type": "synthetic-resource",
            "resource_id": "resource-integration",
            "result": "SYNTHETIC",
            "reason_or_error": None,
            "correlation_ids": ("corr-integration",),
            "causation_ids": ("cause-integration",),
            "component_id": "pixs.backend",
            "component_version": "0.1.0",
        }
        result.update(overrides)
        return result

    def build_event(**overrides):
        return AuditEvent(**values(**overrides))

    assert validate_audit_event(build_event()) == []
    assert validate_audit_event(build_event(tenant_reference=None, reason_or_error=None)) == []

    first_success = validate_audit_event(build_event())
    second_success = validate_audit_event(build_event())
    assert first_success == []
    assert second_success == []
    assert first_success is not second_success

    for opaque_field in (
        "event_id",
        "actor_reference",
        "action",
        "resource_type",
        "resource_id",
        "result",
        "tenant_reference",
        "reason_or_error",
    ):
        assert validate_audit_event(build_event(**{opaque_field: " "})) == []

    empty_correlations = ()
    ordered_duplicates = ("b", "a", "b")
    tuple_event = build_event(
        correlation_ids=empty_correlations,
        causation_ids=ordered_duplicates,
    )
    assert validate_audit_event(tuple_event) == []
    assert tuple_event.correlation_ids is empty_correlations
    assert tuple_event.causation_ids is ordered_duplicates
    assert tuple_event.causation_ids == ("b", "a", "b")

    GuardedDatetime.calendar_calls.clear()
    assert validate_audit_event(build_event(occurred_at=CALENDAR_VALID)) == []
    calendar_refusal = validate_audit_event(build_event(occurred_at=CALENDAR_INVALID))
    assert len(calendar_refusal) == 1
    assert calendar_refusal[0].element == "audit_event.occurred_at"
    assert calendar_refusal[0].step == VALIDATE
    assert CALENDAR_VALID in GuardedDatetime.calendar_calls
    assert CALENDAR_INVALID in GuardedDatetime.calendar_calls

    assert validate_audit_event(
        build_event(
            component_id="pixs.backend",
            component_version="1.2.3-rc.1+build.7",
        )
    ) == []
    component_refusal = validate_audit_event(
        build_event(component_id="pixs >=1.0.0")
    )
    assert len(component_refusal) == 1
    assert component_refusal[0].element == "audit_event.component_id"

    sentinel = "SENTINEL_SYNTHETIC_INVALID"
    sentinel_refusal = validate_audit_event(
        build_event(occurred_at=sentinel, component_id=sentinel + " >=bad", component_version=sentinel)
    )
    assert len(sentinel_refusal) == 3
    assert all(sentinel not in item.message and sentinel not in item.constraint for item in sentinel_refusal)

    marker = object()
    field_names = tuple(field.name for field in dataclasses.fields(AuditEvent))
    invalid_event = AuditEvent(**{name: marker for name in field_names})
    invalid_refusal = validate_audit_event(invalid_event)
    independent_refusal = validate_audit_event(invalid_event)
    keys = [
        (diagnostic.element, diagnostic.constraint, diagnostic.message)
        for diagnostic in invalid_refusal
    ]
    elements = [diagnostic.element for diagnostic in invalid_refusal]
    rendered = "".join(
        f"{diagnostic.element}{diagnostic.constraint}{diagnostic.message}"
        for diagnostic in invalid_refusal
    )
    assert len(keys) == len(field_names)
    assert len(set(keys)) == len(keys)
    assert keys == sorted(keys)
    assert set(elements) == {f"audit_event.{name}" for name in field_names}
    assert all(diagnostic.step == VALIDATE for diagnostic in invalid_refusal)
    assert all(diagnostic.message == diagnostic.constraint for diagnostic in invalid_refusal)
    assert "SENTINEL" not in rendered
    assert invalid_refusal == independent_refusal
    assert invalid_refusal is not independent_refusal
    independent_refusal.clear()
    assert len(invalid_refusal) == len(field_names)

    for _, _, _, guard in function_guards:
        assert guard.call_count == 0
    assert environment_guard.calls == []
    assert import_guard.calls == []
    assert GuardedDatetime.clock_calls == []
    assert GuardedDate.clock_calls == []
    assert file_guard_calls == []

    print("AUDIT_EVENT_SAFE_INTEGRATION_OK")
    '''
).strip()


class AuditEventIntegrationTests(unittest.TestCase):
    def test_fresh_guarded_import_and_validation(self):
        result = subprocess.run(
            [sys.executable, "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)


if __name__ == "__main__":
    unittest.main()
