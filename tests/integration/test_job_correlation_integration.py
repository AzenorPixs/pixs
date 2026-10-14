"""Import et validation declarative de correlation des travaux dans un processus Python frais, sous gardes d'effets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "JOB_CORRELATION_SAFE_INTEGRATION_OK"
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

    import pixs.kernel.job_correlation as job_correlation_module
    from pixs.kernel.job_correlation import JobCorrelation, validate_job_correlation
    from pixs.kernel.diagnostics import VALIDATE, Diagnostic
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"

    class BanningStr(str):
        def __bool__(self):
            raise AssertionError("bool forbidden on unvalidated str subclass")

    valid = JobCorrelation(
        "JOB-MARKER",
        "CORR-MARKER",
        "CAUSE-MARKER",
        "SCOPE-MARKER",
    )
    assert validate_job_correlation(valid) == []

    assert job_correlation_module.__all__ == [
        "JobCorrelation",
        "validate_job_correlation",
    ]

    foreign = validate_job_correlation(None)
    assert len(foreign) == 1
    assert isinstance(foreign[0], Diagnostic)
    assert foreign[0].step == VALIDATE
    assert foreign[0].element == "job_correlation.correlation"
    assert foreign[0].constraint == "corrélation de travail exacte attendue"
    assert foreign[0].message == "corrélation de travail exacte attendue"

    broken = JobCorrelation(None, 0, "", BanningStr("MARKER-REF"))
    refused = validate_job_correlation(broken)
    elements = [diagnostic.element for diagnostic in refused]
    assert elements == [
        "job_correlation.causation_id",
        "job_correlation.correlation_id",
        "job_correlation.job_id",
        "job_correlation.perimeter_reference",
    ], elements
    keys = [
        (diagnostic.element, diagnostic.constraint, diagnostic.message)
        for diagnostic in refused
    ]
    assert keys == sorted(keys)
    assert len(keys) == len(set(keys)) == 4
    for diagnostic in refused:
        assert diagnostic.step == VALIDATE
        assert diagnostic.constraint == "référence opaque exacte non vide attendue"
        assert diagnostic.message == "référence opaque exacte non vide attendue"
    rendered = " | ".join(str(diagnostic) for diagnostic in refused)
    for marker_value in (
        "JOB-MARKER",
        "CORR-MARKER",
        "CAUSE-MARKER",
        "SCOPE-MARKER",
        "MARKER-REF",
    ):
        assert marker_value not in rendered

    again = validate_job_correlation(broken)
    assert again == refused
    assert again is not refused

    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root
    assert counters == {
        "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0,
    }, "import or controlled refusals produced observable effects on guarded surfaces"

print("JOB_CORRELATION_SAFE_INTEGRATION_OK")
'''


class TestJobCorrelationFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "job_correlation_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout, MARKER + "\n")


if __name__ == "__main__":
    unittest.main()
