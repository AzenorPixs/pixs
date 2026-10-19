"""Import du vocabulaire BulkAuthorizationDecision dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_AUTHORIZATION_DECISION_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"}

# DB/PostgreSQL: N/A — vocabulaire pur ; frontend: N/A.

WORKER = '''
import builtins
import contextlib
import io
import os
import socket
import subprocess
import sys
from enum import Enum
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
    stack.enter_context(patch.object(environ_type, "__getitem__", new=_guarded_environ_getitem))
    stack.enter_context(patch.object(sys, "meta_path", new=[_BlockedImportFinder()] + list(sys.meta_path)))
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
    import pixs.backend as backend_facade
    assert tuple(backend_facade.__all__) == ("SettingsTemplate", "build_settings_template", "check_template", "inspect_roles")
    import pixs.backend.bulk_authorization_decision as vocabulary_module
    assert tuple(backend_facade.__all__) == ("SettingsTemplate", "build_settings_template", "check_template", "inspect_roles"), "facade exports changed"
    assert issubclass(vocabulary_module.BulkAuthorizationDecision, Enum)
    assert not issubclass(vocabulary_module.BulkAuthorizationDecision, str)
    assert vocabulary_module.__all__ == ["BulkAuthorizationDecision"]
    assert tuple(vocabulary_module.BulkAuthorizationDecision.__members__) == ("ALLOW", "DENY", "UNAVAILABLE")
    assert vocabulary_module.BulkAuthorizationDecision.ALLOW.value == "ALLOW"
    assert vocabulary_module.BulkAuthorizationDecision.UNAVAILABLE.value == "UNAVAILABLE"
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert counters == {"writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "core": 0}, "module import produced observable effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe, "r"))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)
    assert type(vocabulary_module.BulkAuthorizationDecision.ALLOW.value) is str
    assert type(vocabulary_module.BulkAuthorizationDecision.ALLOW) is not str
    assert counters == {"writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "core": 0}, "checks produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)
print("BULK_AUTHORIZATION_DECISION_SAFE_INTEGRATION_OK")
'''


class TestBulkAuthorizationDecisionFreshProcess(unittest.TestCase):
    def test_import_in_fresh_process_with_minimal_env(self):
        probe = str(REPO_ROOT / "bulk_authorization_decision_guard_probe.txt")
        self.assertFalse(Path(probe).exists())
        completed = subprocess.run(
            [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
            env=FIXED_ENV,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=REPO_ROOT,
        )
        self.assertFalse(Path(probe).exists())
        self.assertEqual(completed.stderr, "")
        self.assertEqual(completed.stdout, MARKER + "\n")
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
