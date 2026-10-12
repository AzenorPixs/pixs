"""Import et validation structurelle BulkOperationCommitMode dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_OPERATION_COMMIT_MODE_SAFE_INTEGRATION_OK"
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

    import pixs.kernel.bulk_operation_commit_mode as commit_mode_module
    from pixs.kernel.bulk_operation_commit_mode import BulkOperationCommitMode, validate_bulk_operation_commit_mode
    from pixs.kernel.bulk_operations import BulkCommitMode
    from pixs.kernel.diagnostics import VALIDATE, Diagnostic
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"

    state["read_block"] = True
    assert os.path.exists(read_probe)
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    assert counters["reads"] == 1
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    class BanningStr(str):
        def __bool__(self):
            raise AssertionError("bool forbidden on foreign str subclass")
        def __eq__(self, other):
            raise AssertionError("eq forbidden on foreign str subclass")

    assert commit_mode_module.__all__ == ["BulkOperationCommitMode", "validate_bulk_operation_commit_mode"]

    for mode_member in BulkCommitMode:
        valid = BulkOperationCommitMode(" OP-MARKER ", mode_member)
        assert validate_bulk_operation_commit_mode(valid) == []
        assert valid.operation_id == " OP-MARKER "
        assert valid.commit_mode is mode_member

    foreign = validate_bulk_operation_commit_mode(None)
    assert len(foreign) == 1
    assert isinstance(foreign[0], Diagnostic)
    assert foreign[0].step == VALIDATE
    assert foreign[0].element == "bulk_operation_commit_mode.profile"

    hostile = BulkOperationCommitMode(BanningStr("OP-MARKER"), "MODE-MARKER")
    refused = validate_bulk_operation_commit_mode(hostile)
    assert [item.element for item in refused] == [
        "bulk_operation_commit_mode.commit_mode", "bulk_operation_commit_mode.operation_id",
    ]

    forged = object.__new__(BulkCommitMode)
    forged_result = validate_bulk_operation_commit_mode(
        BulkOperationCommitMode("OP-MARKER", forged)
    )
    assert len(forged_result) == 1
    assert forged_result[0].element == "bulk_operation_commit_mode.commit_mode"

    diagnostics = foreign + refused + forged_result
    assert all(item.step == VALIDATE for item in diagnostics)
    rendered = " | ".join(str(item) for item in diagnostics)
    for marker_value in ("OP-MARKER", "MODE-MARKER"):
        assert marker_value not in rendered

    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert "pixs.core" not in sys.modules
    assert counters == {
        "writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "core": 0,
    }, "import or controlled refusals produced observable effects on guarded surfaces"

print("BULK_OPERATION_COMMIT_MODE_SAFE_INTEGRATION_OK")
'''


class TestBulkOperationCommitModeFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_operation_commit_mode_guard_probe.txt")
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
