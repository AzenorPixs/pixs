"""Import et validation structurelle BulkOperationRecordValues dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_RECORD_VALUES_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = '''
import builtins
import contextlib
import io
import os
import socket
import subprocess
import sys
from unittest.mock import patch

src_path = sys.argv[1]
probe = sys.argv[2]
read_probe = sys.executable
counters = {"writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "core": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")
state = {"read_block": False}

sys.path.insert(0, src_path)
builtins_open = builtins.open
environ_type = type(os.environ)


class GuardBlocked(Exception):
    pass


class _BlockedImportFinder:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "pixs.core" or fullname.startswith("pixs.core."):
            counters["core"] += 1
            raise GuardBlocked("blocked concrete core import")
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("blocked by integration guard")
        return None


def _guarded_open(file, mode="r", *args, **kwargs):
    if any(flag in mode for flag in "wax+"):
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    if state["read_block"]:
        counters["reads"] += 1
        raise GuardBlocked("blocked by integration guard")
    return builtins_open(file, mode, *args, **kwargs)


def _guarded_socket(*args, **kwargs):
    counters["network"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_popen(*args, **kwargs):
    counters["process"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_system(command):
    counters["process"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_environ_getitem(mapping, key):
    counters["environ"] += 1
    raise GuardBlocked("blocked by integration guard")


def _positive_control(label, callable_target):
    try:
        callable_target()
    except GuardBlocked:
        return
    raise AssertionError("guard did not block: " + label)


for root in BLOCKED_DB_ROOTS:
    assert root not in sys.modules, "db module preloaded: " + root

with contextlib.ExitStack() as stack:
    stack.enter_context(patch.object(builtins, "open", new=_guarded_open))
    stack.enter_context(patch.object(io, "open", new=_guarded_open))
    stack.enter_context(patch.object(socket, "socket", new=_guarded_socket))
    stack.enter_context(patch.object(subprocess, "Popen", new=_guarded_popen))
    stack.enter_context(patch.object(os, "system", new=_guarded_system))
    stack.enter_context(
        patch.object(environ_type, "__getitem__", new=_guarded_environ_getitem)
    )
    stack.enter_context(
        patch.object(
            sys, "meta_path",
            new=[_BlockedImportFinder()] + list(sys.meta_path),
        )
    )

    assert not os.path.exists(probe)
    _positive_control("open", lambda: builtins.open(probe, "w"))
    assert counters["writes"] == 1
    assert not os.path.exists(probe)
    _positive_control("socket", lambda: socket.socket())
    assert counters["network"] == 1
    _positive_control("popen", lambda: subprocess.Popen(["/usr/bin/true"]))
    assert counters["process"] == 1
    _positive_control("system", lambda: os.system("true"))
    assert counters["process"] == 2
    _positive_control("environ", lambda: os.environ["PATH"])
    assert counters["environ"] == 1
    _positive_control("getenv", lambda: os.getenv("PATH"))
    assert counters["environ"] == 2
    _positive_control("db", lambda: __import__("sqlite3"))
    assert counters["db"] == 1
    assert "pixs.core" not in sys.modules
    _positive_control("core", lambda: __import__("pixs.core"))
    assert counters["core"] == 1
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    counters.update((key, 0) for key in counters)

    import pixs.kernel.bulk_operation_record_values as record_values_module
    from pixs.kernel.bulk_operation_record_values import validate_bulk_operation_record_values
    from pixs.kernel.bulk_operations import BulkReferenceFormat
    from pixs.kernel.diagnostics import VALIDATE, Diagnostic

    assert counters == {key: 0 for key in counters}, "import produced effects"
    assert record_values_module.__all__ == ["validate_bulk_operation_record_values"]
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    values = {
        "operation_id": " OP-MARKER ",
        "bulk_type": "EXPORT",
        "bulk_version": "1.2.3-rc.1+build",
        "status": "REQUESTED",
        "tenant_context_reference": "TENANT-MARKER",
        "scope_context_reference": None,
        "format": "NDJSON",
        "conflict_strategy": None,
        "commit_mode": None,
    }
    original = tuple(values.items())
    assert validate_bulk_operation_record_values(values) == []
    assert tuple(values.items()) == original

    equal = dict(values)
    for field in ("operation_id", "tenant_context_reference", "scope_context_reference"):
        equal[field] = "EQUAL-MARKER"
    assert validate_bulk_operation_record_values(equal) == []

    class BanningStr(str):
        def __bool__(self):
            raise AssertionError("bool forbidden")
        def __eq__(self, other):
            raise AssertionError("eq forbidden")
        def __hash__(self):
            raise AssertionError("hash forbidden")

    class BanningDict(dict):
        def items(self):
            raise AssertionError("items forbidden")

    bad = dict(values)
    bad["operation_id"] = BanningStr("OP-MARKER")
    refused = validate_bulk_operation_record_values(bad)
    foreign = validate_bulk_operation_record_values(BanningDict(values))
    enums = dict(values)
    enums["format"] = BulkReferenceFormat.CSV
    enum_refusals = validate_bulk_operation_record_values(enums)
    missing = dict(values)
    del missing["commit_mode"]
    missing_refusals = validate_bulk_operation_record_values(missing)
    for group in (refused, foreign, enum_refusals, missing_refusals):
        assert group
        for diagnostic in group:
            assert isinstance(diagnostic, Diagnostic)
            assert diagnostic.step == VALIDATE
            assert diagnostic.constraint == diagnostic.message
            for marker_value in ("OP-MARKER", "TENANT-MARKER", "EQUAL-MARKER"):
                assert marker_value not in str(diagnostic)
    assert counters == {key: 0 for key in counters}, "validation produced effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules

print("BULK_RECORD_VALUES_SAFE_INTEGRATION_OK")
'''


class TestBulkOperationRecordValuesFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_operation_record_values_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout, MARKER + "\n")
            self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
