"""Integration InboxReceiptV1 en processus frais sous gardes (unittest seul)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_INBOX_RECEIPT_SAFE_INTEGRATION_OK"
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

    assert "pixs.backend.bulk_inbox_receipt_values" not in sys.modules
    import pixs.backend.bulk_inbox_receipt_values as runtime
    expected_file = os.path.join(src_path, "pixs", "backend", "bulk_inbox_receipt_values.py")
    assert runtime.__file__ == expected_file, (runtime.__file__, expected_file)
    assert runtime.__all__ == ["validate_bulk_inbox_receipt_values", "capture_bulk_inbox_receipt_values"]
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    CONSUMED_AT = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)

    def _valid_entry():
        return {
            "consumer_reference": "consumer-test",
            "event_id": "event-test",
            "event_version": "1.2.3",
            "content_sha256": "0f" * 32,
            "state": "CONSUMED",
            "consumed_at": CONSUMED_AT,
            "correlation_id": "correlation-test",
            "causation_id": None,
        }

    class Hostile:
        def __bool__(self):
            raise AssertionError("hook bool étranger")
        def __eq__(self, other):
            raise AssertionError("hook eq étranger")
        def __hash__(self):
            raise AssertionError("hook hash étranger")
        def __str__(self):
            raise AssertionError("hook str étranger")
        def __repr__(self):
            raise AssertionError("hook repr étranger")

    candidate = _valid_entry()
    assert runtime.validate_bulk_inbox_receipt_values(candidate) == []
    bound, diags = runtime.capture_bulk_inbox_receipt_values(candidate)
    assert bound is not None and diags == []
    assert bound.consumer_reference == "consumer-test"
    assert bound.event_id == "event-test"
    assert bound.consumed_at is CONSUMED_AT
    candidate["event_id"] = "muté"
    assert bound.event_id == "event-test"
    other, other_diags = runtime.capture_bulk_inbox_receipt_values(_valid_entry())
    assert other == bound and other is not bound
    assert other_diags == [] and other_diags is not diags
    assert not hasattr(bound, "__dict__")
    try:
        bound.state = "X"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("bound not frozen")

    causal = _valid_entry()
    causal["causation_id"] = "cause-é"
    causal["event_version"] = "2.3.4-rc.1+build.7"
    assert runtime.validate_bulk_inbox_receipt_values(causal) == []

    for field in _valid_entry():
        missing = _valid_entry()
        del missing[field]
        assert runtime.validate_bulk_inbox_receipt_values(missing)
        capture, refused = runtime.capture_bulk_inbox_receipt_values(missing)
        assert capture is None and refused
        hostile = _valid_entry()
        hostile[field] = Hostile()
        assert runtime.validate_bulk_inbox_receipt_values(hostile)
        capture, refused = runtime.capture_bulk_inbox_receipt_values(hostile)
        assert capture is None and refused

    bad = _valid_entry()
    bad["intrus"] = Hostile()
    assert runtime.validate_bulk_inbox_receipt_values(bad)
    for foreign in (None, 0, "x", [], Hostile()):
        assert runtime.validate_bulk_inbox_receipt_values(foreign)
        capture, refused = runtime.capture_bulk_inbox_receipt_values(foreign)
        assert capture is None and refused

    for field, value in (
        ("state", "PENDING"),
        ("state", "consumed"),
        ("content_sha256", "0F" * 32),
        ("content_sha256", "0f" * 31),
        ("event_version", "1.2"),
        ("consumer_reference", ""),
        ("causation_id", "a\x00b"),
        ("correlation_id", "surrogate\ud800"),
        ("consumed_at", datetime(2026, 1, 1)),
    ):
        candidate = _valid_entry()
        candidate[field] = value
        first = runtime.validate_bulk_inbox_receipt_values(candidate)
        second = runtime.validate_bulk_inbox_receipt_values(candidate)
        assert first and first == second and first is not second
        assert all(type(d) is runtime.Diagnostic and d.step == "validate" for d in first)
        keys = [(d.element, d.constraint, d.message) for d in first]
        assert keys == sorted(set(keys))
        capture, refused = runtime.capture_bulk_inbox_receipt_values(candidate)
        assert capture is None and refused

    assert counters == {key: 0 for key in counters}, "primitives produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_INBOX_RECEIPT_SAFE_INTEGRATION_OK")
'''


class TestBulkInboxReceiptFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_inbox_receipt_guard_probe.txt")
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
