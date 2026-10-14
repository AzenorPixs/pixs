"""Integration ValidationReportV1 en processus frais sous gardes (unittest seul)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_VALIDATION_REPORT_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 30
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = r'''

import builtins
import contextlib
import io
import os
import socket
import subprocess
import sys
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
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

    assert "pixs.backend.bulk_validation_report_values" not in sys.modules
    import pixs.backend.bulk_validation_report_values as runtime
    expected_file = os.path.join(src_path, "pixs", "backend", "bulk_validation_report_values.py")
    assert runtime.__file__ == expected_file, (runtime.__file__, expected_file)
    assert runtime.__all__ == ["validate_bulk_validation_report_values", "capture_bulk_validation_report_values"]
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    policy = {'max_input_bytes': 1048576, 'max_rows': 1000000, 'max_row_bytes': 8192, 'max_columns': 64, 'max_json_depth': 8, 'max_json_members': 32, 'max_diagnostics': 100, 'read_chunk_bytes': 4096, 'chunk_rows': 500, 'max_attempts': 3, 'lease_seconds': 60, 'renewal_seconds': 20, 'publish_max_attempts': 1, 'publish_lease_seconds': 50, 'publish_renewal_seconds': 20, 'max_parallel_operations': 2, 'max_runtime_seconds': 3600, 'replay_window_seconds': 300, 'idempotency_retention_seconds': 600, 'staging_retention_seconds': 900, 'result_retention_seconds': 1200, 'max_download_url_seconds': 60, 'retry_delays_seconds': [1, 2], 'publish_retry_delays_seconds': []}
    policy["max_diagnostics"] = 1
    args = dict(policy=policy, declared_codes=("INVALID_FIELD",), declared_fields=("name",))

    def valid():
        return dict(report_version="1.0.0", operation_id="op-test",
                    mode="VALIDATE_ONLY", progress=dict(total_rows=None, validated_rows=2,
                    invalid_rows=1, applied_rows=0, execution_rejected_rows=0, exported_rows=0),
                    diagnostics=(dict(code="INVALID_FIELD", field_reference="name", line_index=1),),
                    complete=True, source_version=None, mapping_version="1.2.3-rc.1+build")

    candidate = valid()
    assert runtime.validate_bulk_validation_report_values(candidate, **args) == []
    bound, diags = runtime.capture_bulk_validation_report_values(candidate, **args)
    assert bound is not None and diags == []
    candidate["progress"]["validated_rows"] = 99
    candidate["diagnostics"][0]["code"] = "muté"
    assert bound.progress.validated_rows == 2 and bound.diagnostics[0].code == "INVALID_FIELD"
    for obj, field, value in ((bound, "complete", False),
                              (bound.progress, "validated_rows", 3),
                              (bound.diagnostics[0], "code", "muté")):
        try:
            setattr(obj, field, value)
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError("snapshot not frozen")
        assert not hasattr(obj, "__dict__")

    class Hostile:
        def __bool__(self):
            raise AssertionError("foreign bool")
        def __eq__(self, other):
            raise AssertionError("foreign equality")
        def __hash__(self):
            raise AssertionError("foreign hash")
        def __repr__(self):
            raise AssertionError("foreign repr")

    too_long = valid()
    too_long["diagnostics"] = (Hostile(), Hostile())
    assert runtime.validate_bulk_validation_report_values(too_long, **args)
    assert runtime.capture_bulk_validation_report_values(too_long, **args)[0] is None
    for mode in (None, "VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT"):
        candidate = valid()
        candidate["mode"] = mode
        assert runtime.validate_bulk_validation_report_values(candidate, **args) == []
    for field, value in (("report_version", "2.0.0"), ("mode", "IMPORT"),
                         ("complete", 1), ("mapping_version", "1.2"),
                         ("operation_id", "a\x00b"), ("diagnostics", [])):
        candidate = valid()
        candidate[field] = value
        first = runtime.validate_bulk_validation_report_values(candidate, **args)
        second = runtime.validate_bulk_validation_report_values(candidate, **args)
        assert first and first == second and first is not second
        assert all(type(d) is runtime.Diagnostic and d.step == "validate" for d in first)
        assert runtime.capture_bulk_validation_report_values(candidate, **args)[0] is None
    assert runtime.validate_bulk_validation_report_values(valid(), **dict(args, policy=None))
    assert runtime.validate_bulk_validation_report_values(valid(), **dict(args, declared_codes=()))
    for complete in (True, False):
        candidate = valid()
        candidate["complete"] = complete
        assert runtime.validate_bulk_validation_report_values(candidate, **args) == []

    assert counters == {key: 0 for key in counters}, "primitives produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_VALIDATION_REPORT_SAFE_INTEGRATION_OK")
'''


class TestBulkValidationReportFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_validation_report_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe],
                cwd=str(REPO_ROOT),
                env=FIXED_ENV,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stdout, MARKER + "\n")
            self.assertEqual(completed.stderr, "")
            self.assertFalse(Path(probe).exists())
        self.assertFalse(Path(tmp).exists())


if __name__ == "__main__":
    unittest.main()
