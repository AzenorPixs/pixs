"""Import et validation de DataSubjectRequest dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "DATA_SUBJECT_REQUEST_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = '''
import builtins
import contextlib
import os
import socket
import subprocess
import sys
from unittest.mock import patch

src_path = sys.argv[1]
counters = {"writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")

sys.path.insert(0, src_path)
builtins_open = builtins.open
environ_type = type(os.environ)


class GuardBlocked(Exception):
    pass


class _BlockedImportFinder:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("blocked by integration guard")
        return None


def _guarded_open(file, mode="r", *args, **kwargs):
    if any(flag in mode for flag in "wax+"):
        counters["writes"] += 1
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

    probe = sys.argv[2]
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
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    counters.update((key, 0) for key in counters)

    from pixs.kernel.data_subject_operations import DataSubjectOperation
    import pixs.kernel.data_subject_request as request_module
    from pixs.kernel.diagnostics import VALIDATE
    from pixs.kernel.data_subject_request import (
        DataSubjectRequest,
        validate_data_subject_request,
    )
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"

    valid = DataSubjectRequest(
        request_id="req-1",
        operation=DataSubjectOperation.ACCESS,
        subject_reference="subject-1",
        tenant_id=None,
        scope_id=None,
        requested_by="requester-1",
        status="OPEN",
        policy_version="1.0.0",
        operation_id=None,
        legal_hold_decision=None,
        result_reference=None,
    )
    assert validate_data_subject_request(valid) == []
    assert request_module.__all__ == [
        "DataSubjectRequest", "validate_data_subject_request",
    ]

    broken = DataSubjectRequest(
        request_id=None,
        operation="ACCESS",
        subject_reference=None,
        tenant_id=None,
        scope_id=None,
        requested_by=None,
        status=None,
        policy_version=None,
        operation_id=None,
        legal_hold_decision=None,
        result_reference=None,
    )
    diagnostics = validate_data_subject_request(broken)
    assert len(diagnostics) == 6, len(diagnostics)
    assert all(d.step == VALIDATE and d.message == d.constraint for d in diagnostics)
    elements = [d.element for d in diagnostics]
    assert elements == sorted(elements)
    assert len(set(elements)) == 6
    assert set(elements) == {
        "data_subject_request.request_id",
        "data_subject_request.operation",
        "data_subject_request.subject_reference",
        "data_subject_request.requested_by",
        "data_subject_request.status",
        "data_subject_request.policy_version",
    }
    assert "None" not in str(diagnostics)
    assert "ACCESS" not in str(diagnostics)

    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert counters == {
        "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0,
    }, "import or controlled refusals produced observable effects on guarded surfaces"

print("DATA_SUBJECT_REQUEST_SAFE_INTEGRATION_OK")
'''


class TestDataSubjectRequestFreshProcess(unittest.TestCase):
    def test_import_and_validation_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "data_subject_request_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=REPO_ROOT,
            )
            self.assertFalse(Path(probe).exists())
        self.assertFalse(Path(tmp).exists())
        self.assertEqual(completed.stderr, "")
        self.assertEqual(completed.stdout, MARKER + "\n")
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
