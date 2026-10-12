"""Import et validation mémoire Bulk runtime dans un processus frais sous gardes."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_RUNTIME_VALUES_SAFE_INTEGRATION_OK"
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


    import pixs.backend.bulk_execution_values as runtime
    from datetime import datetime, timezone, tzinfo
    from pixs.kernel.diagnostics import VALIDATE, Diagnostic

    assert runtime.__all__ == [
        "validate_bulk_execution_values",
        "validate_bulk_progress_values",
        "validate_bulk_policy_values",
    ]
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    def progress():
        return {
            "total_rows": None, "validated_rows": 2, "invalid_rows": 1,
            "applied_rows": 0, "execution_rejected_rows": 0, "exported_rows": 0,
        }

    def execution():
        return {
            "operation_id": " OP-MARKER ", "bulk_type": "IMPORT",
            "bulk_version": "1.2.3-rc.1+build", "status": "REQUESTED",
            "tenant_context_reference": "TENANT-MARKER",
            "scope_context_reference": None, "format": "CSV",
            "conflict_strategy": None, "commit_mode": None,
            "execution_version": "1.0.0", "requested_by_reference": "ACTOR-MARKER",
            "resolved_context_reference": "CONTEXT-MARKER",
            "mapping_reference": "MAPPING-MARKER", "mapping_version": "1.0.0",
            "input_reference": "INPUT-MARKER", "input_version": "VERSION-MARKER",
            "input_sha256": "a" * 64, "input_size_bytes": 0,
            "output_reference": None, "output_version": None,
            "output_sha256": None, "output_size_bytes": None,
            "projection_reference": None, "consistency_kind": None,
            "consistency_reference": None, "idempotency_key": "KEY-MARKER",
            "correlation_id": "CORRELATION-MARKER", "causation_id": None,
            "progress": progress(), "checkpoint_reference": None,
            "result_reference": None,
            "expires_at": datetime(2020, 1, 1, tzinfo=timezone.utc),
            "policy_reference": "POLICY-MARKER", "policy_version": "1.0.0",
            "revision": 1, "cancellation_requested": False,
        }

    policy_fields = (
        "max_input_bytes", "max_rows", "max_row_bytes", "max_columns",
        "max_json_depth", "max_json_members", "max_diagnostics",
        "read_chunk_bytes", "chunk_rows", "max_attempts", "lease_seconds",
        "renewal_seconds", "publish_max_attempts", "publish_lease_seconds",
        "publish_renewal_seconds", "max_parallel_operations",
        "max_runtime_seconds", "replay_window_seconds",
        "idempotency_retention_seconds", "staging_retention_seconds",
        "result_retention_seconds", "max_download_url_seconds",
    )

    def policy():
        values = {field: 1 for field in policy_fields}
        values.update(
            lease_seconds=3, publish_lease_seconds=3,
            retry_delays_seconds=[], publish_retry_delays_seconds=[],
        )
        return values

    def check(fn, value, accepted):
        before = tuple((key, id(item)) for key, item in value.items()) if type(value) is dict else None
        first = fn(value)
        second = fn(value)
        assert type(first) is list and first is not second
        assert bool(first) is not accepted
        keys = [(item.element, item.constraint, item.message) for item in first]
        assert keys == sorted(set(keys))
        for item in first:
            assert type(item) is Diagnostic and item.step == VALIDATE
            for marker in ("OP-MARKER", "TENANT-MARKER", "UNKNOWN-MARKER"):
                assert marker not in str(item)
        if before is not None:
            assert tuple((key, id(item)) for key, item in value.items()) == before
        assert counters == {key: 0 for key in counters}, "validation produced effects"

    full = execution()
    nested_before = tuple(full["progress"].items())
    check(runtime.validate_bulk_execution_values, full, True)
    assert tuple(full["progress"].items()) == nested_before
    check(runtime.validate_bulk_progress_values, progress(), True)
    check(runtime.validate_bulk_policy_values, policy(), True)

    export = execution()
    export.update(
        bulk_type="EXPORT", input_reference=None, input_version=None,
        input_sha256=None, input_size_bytes=None,
        projection_reference="PROJECTION-MARKER", consistency_kind="SNAPSHOT",
    )
    check(runtime.validate_bulk_execution_values, export, True)
    export["status"] = "READY"
    check(runtime.validate_bulk_execution_values, export, False)
    export["consistency_reference"] = "SNAPSHOT-MARKER"
    check(runtime.validate_bulk_execution_values, export, True)

    class Hostile:
        def __bool__(self):
            raise AssertionError("foreign bool")
        def __eq__(self, other):
            raise AssertionError("foreign equality")
        def __hash__(self):
            raise AssertionError("foreign hash")
        def __str__(self):
            raise AssertionError("foreign str")
        def __repr__(self):
            raise AssertionError("foreign repr")

    class ForeignDict(dict):
        def items(self):
            raise AssertionError("foreign items")

    class ForeignList(list):
        def __iter__(self):
            raise AssertionError("foreign iteration")

    class ForeignTimezone(tzinfo):
        def utcoffset(self, value):
            raise AssertionError("foreign utcoffset")
        def dst(self, value):
            raise AssertionError("foreign dst")
        def tzname(self, value):
            raise AssertionError("foreign tzname")

    class HashOnce:
        def __init__(self):
            self.calls = 0
        def __hash__(self):
            self.calls += 1
            if self.calls > 1:
                raise AssertionError("foreign rehash")
            return 17
        def __eq__(self, other):
            raise AssertionError("foreign key equality")

    for fn, factory in (
        (runtime.validate_bulk_execution_values, execution),
        (runtime.validate_bulk_progress_values, progress),
        (runtime.validate_bulk_policy_values, policy),
    ):
        check(fn, Hostile(), False)
        check(fn, ForeignDict(factory()), False)
        omitted = factory()
        del omitted[next(iter(omitted))]
        check(fn, omitted, False)
        unknown = factory()
        unknown["UNKNOWN-MARKER"] = Hostile()
        check(fn, unknown, False)

    foreign_key = HashOnce()
    foreign_keys = execution()
    foreign_keys[foreign_key] = Hostile()
    # Inspecter seulement le résultat statique et le compteur pour une clé étrangère.
    assert runtime.validate_bulk_execution_values(foreign_keys)
    assert foreign_key.calls == 1

    bad = execution()
    bad["progress"] = ForeignDict(progress())
    check(runtime.validate_bulk_execution_values, bad, False)
    bad = execution()
    bad["progress"]["validated_rows"] = Hostile()
    check(runtime.validate_bulk_execution_values, bad, False)
    bad = execution()
    bad["revision"] = True
    check(runtime.validate_bulk_execution_values, bad, False)
    bad = execution()
    bad["expires_at"] = datetime(2020, 1, 1, tzinfo=ForeignTimezone())
    check(runtime.validate_bulk_execution_values, bad, False)
    bad = progress()
    bad["total_rows"] = -1
    check(runtime.validate_bulk_progress_values, bad, False)
    bad = policy()
    bad["retry_delays_seconds"] = ForeignList()
    check(runtime.validate_bulk_policy_values, bad, False)
    bad = policy()
    bad["max_rows"] = True
    check(runtime.validate_bulk_policy_values, bad, False)
    bad = policy()
    bad["lease_seconds"] = 2
    check(runtime.validate_bulk_policy_values, bad, False)

    assert counters == {key: 0 for key in counters}
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_RUNTIME_VALUES_SAFE_INTEGRATION_OK")
'''


class TestBulkExecutionValuesFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_runtime_values_guard_probe.txt")
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
