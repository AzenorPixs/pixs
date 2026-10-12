"""Import et validation structurelle BulkJobLink dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_JOB_LINK_SAFE_INTEGRATION_OK"
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
counters = {"writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")
state = {"read_block": False}

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
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    counters.update((key, 0) for key in counters)

    import pixs.kernel.bulk_job_link as bulk_job_link_module
    from pixs.kernel.bulk_job_link import BulkJobLink, validate_bulk_job_link
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
            raise AssertionError("bool forbidden on unvalidated str subclass")
        def __eq__(self, other):
            raise AssertionError("eq forbidden on unvalidated str subclass")

    assert bulk_job_link_module.__all__ == ["BulkJobLink", "validate_bulk_job_link"]

    valid = BulkJobLink(" OP-MARKER ", "JOB-MARKER\\u00a0")
    assert validate_bulk_job_link(valid) == []
    assert valid.operation_id == " OP-MARKER "
    assert valid.job_id == "JOB-MARKER\\u00a0"

    foreign = validate_bulk_job_link(None)
    assert len(foreign) == 1
    assert isinstance(foreign[0], Diagnostic)
    assert foreign[0].step == VALIDATE
    assert foreign[0].element == "bulk_job_link.link"
    assert foreign[0].constraint == "lien BulkJobLink exact attendu"

    hostile = BulkJobLink(BanningStr("OP-MARKER"), "JOB-MARKER\\u00a0")
    refused = validate_bulk_job_link(hostile)
    assert len(refused) == 1
    assert refused[0].step == VALIDATE
    assert refused[0].element == "bulk_job_link.operation_id"
    assert refused[0].constraint == "référence opaque exacte non vide attendue"

    equal = BulkJobLink("EQUAL-MARKER", "EQUAL-MARKER")
    distinction = validate_bulk_job_link(equal)
    assert len(distinction) == 1
    assert distinction[0].step == VALIDATE
    assert distinction[0].element == "bulk_job_link.distinction"
    assert distinction[0].constraint == "références distinctes attendues"

    rendered = " | ".join(
        str(diagnostic) for diagnostic in foreign + refused + distinction
    )
    for marker_value in ("OP-MARKER", "JOB-MARKER", "EQUAL-MARKER"):
        assert marker_value not in rendered

    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert counters == {
        "writes": 0, "reads": 0, "network": 0, "process": 0, "environ": 0, "db": 0,
    }, "import or controlled refusals produced observable effects on guarded surfaces"

print("BULK_JOB_LINK_SAFE_INTEGRATION_OK")
'''


class TestBulkJobLinkFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_job_link_guard_probe.txt")
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
