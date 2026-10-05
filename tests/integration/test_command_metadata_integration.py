"""Intégration sûre des métadonnées déclaratives de commande : import et validation gardés."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "COMMAND_METADATA_SAFE_INTEGRATION_OK\n"
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
    import uuid

    sys.path.insert(0, sys.argv[1])

    from unittest import mock

    FORBIDDEN_IMPORT_PREFIXES = ("django", "psycopg", "psycopg2", "psycopg_pool", "psycopg_binary")


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
        clock_calls = []

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

    from pixs.core.command_metadata import CommandMetadata, validate_command_metadata
    from pixs.core.scope import ScopeContext, ScopeType
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

    tenant_context = ScopeContext(ScopeType.TENANT, "tenant-synthetic", "scope-synthetic")
    platform_context = ScopeContext(ScopeType.PLATFORM)

    def values(**overrides):
        result = {
            "command_id": "command-synthetic",
            "correlation_ids": ("corr-synthetic", "corr-synthetic", "corr-other"),
            "causation_ids": (),
            "scope_context": tenant_context,
            "command_type": "command-type-synthetic",
            "subject_id": "subject-synthetic",
            "idempotency_key": "key-synthetic",
        }
        result.update(overrides)
        return result

    def make_command(**overrides):
        return CommandMetadata(**values(**overrides))

    for scope_context in (tenant_context, platform_context):
        command = make_command(scope_context=scope_context)
        before = dataclasses.asdict(command)
        first = validate_command_metadata(command)
        second = validate_command_metadata(command)
        assert first == [] and second == [] and first is not second
        first.append("synthetic local mutation")
        assert second == [] and validate_command_metadata(command) == []
        assert dataclasses.asdict(command) == before
        assert command.correlation_ids == ("corr-synthetic", "corr-synthetic", "corr-other")
        assert command.causation_ids == ()

    for field in ("command_id", "command_type", "subject_id", "idempotency_key"):
        command = make_command(**{field: " "})
        assert validate_command_metadata(command) == []
    empty_tuples = make_command(correlation_ids=(), causation_ids=())
    spaced_tuple = make_command(correlation_ids=(" ", " ", "x"))
    spaced_context = make_command(scope_context=ScopeContext(ScopeType.TENANT, " ", " "))
    assert validate_command_metadata(empty_tuples) == []
    assert validate_command_metadata(spaced_tuple) == []
    assert validate_command_metadata(spaced_context) == []

    foreign = validate_command_metadata(object())
    assert len(foreign) == 1 and foreign[0].element == "command_metadata.command"
    assert foreign[0].step == VALIDATE and foreign[0].constraint == foreign[0].message

    malformed_context = object.__new__(ScopeContext)
    object.__setattr__(malformed_context, "scope_type", ScopeType.PLATFORM)
    object.__setattr__(malformed_context, "tenant_id", "synthetic-forbidden-tenant")
    object.__setattr__(malformed_context, "scope_id", None)
    context_refusal = validate_command_metadata(make_command(scope_context=malformed_context))
    assert len(context_refusal) == 1
    assert context_refusal[0].element == "command_metadata.scope_context"
    assert context_refusal[0].step == VALIDATE
    assert context_refusal[0].constraint == context_refusal[0].message
    assert "synthetic-forbidden-tenant" not in context_refusal[0].message

    sentinel = "SENTINEL_SYNTHETIC_COMMAND"
    invalid_command = make_command(
        command_id=object(), correlation_ids=(sentinel, object()),
        causation_ids=(sentinel, ""), scope_context=object(), command_type=object(),
        subject_id=object(), idempotency_key=object(),
    )
    refusal = validate_command_metadata(invalid_command)
    independent = validate_command_metadata(invalid_command)
    keys = [(item.element, item.constraint, item.message) for item in refusal]
    assert len(keys) == 7 and len(set(keys)) == 7 and keys == sorted(keys)
    names = tuple(field.name for field in dataclasses.fields(CommandMetadata))
    assert {item.element for item in refusal} == {f"command_metadata.{name}" for name in names}
    assert all(item.step == VALIDATE and item.constraint == item.message for item in refusal)
    assert all(item.constraint.startswith(item.element + ": ") for item in refusal)
    assert all(sentinel not in item.message and sentinel not in item.constraint for item in refusal)
    assert refusal == independent and refusal is not independent
    independent.clear()
    assert len(refusal) == 7 and len(validate_command_metadata(invalid_command)) == 7

    for _, _, _, guard in function_guards:
        assert guard.call_count == 0
    assert environment_guard.calls == []
    assert import_guard.calls == []
    assert GuardedDatetime.clock_calls == []
    assert GuardedDate.clock_calls == []
    assert file_guard_calls == []

    print("COMMAND_METADATA_SAFE_INTEGRATION_OK")
    '''
).strip()


class CommandMetadataIntegrationTests(unittest.TestCase):
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
