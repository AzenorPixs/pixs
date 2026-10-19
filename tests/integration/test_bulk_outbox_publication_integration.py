"""Integration OutboxPublicationV1 en processus frais sous gardes (unittest seul)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_OUTBOX_PUBLICATION_SAFE_INTEGRATION_OK"
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

    assert "pixs.backend.bulk_outbox_publication_values" not in sys.modules
    import pixs.backend.bulk_outbox_publication_values as runtime
    expected_file = os.path.join(src_path, "pixs", "backend", "bulk_outbox_publication_values.py")
    assert runtime.__file__ == expected_file, (runtime.__file__, expected_file)
    assert runtime.__all__ == ["validate_bulk_outbox_publication_values", "capture_bulk_outbox_publication_values"]
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    LEASE_AT = datetime(2026, 1, 3, 4, 5, 6, 7, tzinfo=timezone.utc)
    NEXT_AT = datetime(2026, 2, 4, 5, 6, 7, 8, tzinfo=timezone.utc)
    PUBLISHED_AT = datetime(2026, 3, 5, 6, 7, 8, 9, tzinfo=timezone.utc)

    def _valid_entry():
        return {
            "event_id": "event-test",
            "state": "PENDING",
            "attempt_count": 0,
            "lease_owner": None,
            "lease_expires_at": None,
            "next_attempt_at": None,
            "published_at": None,
            "failure_code": None,
            "sequence_index": 1,
            "policy_reference": "policy-test",
            "policy_version": "1.2.3",
            "revision": 1,
        }

    class Hostile:
        def __bool__(self):
            raise AssertionError("hook bool etranger")
        def __eq__(self, other):
            raise AssertionError("hook eq etranger")
        def __hash__(self):
            raise AssertionError("hook hash etranger")
        def __str__(self):
            raise AssertionError("hook str etranger")
        def __repr__(self):
            raise AssertionError("hook repr etranger")

    assert runtime.validate_bulk_outbox_publication_values(_valid_entry()) == []
    bound, diags = runtime.capture_bulk_outbox_publication_values(_valid_entry())
    assert bound is not None and diags == []
    assert bound.event_id == "event-test"
    assert bound.revision == 1

    assert runtime.validate_bulk_outbox_publication_values(_valid_entry()) == []
    bound2, diags2 = runtime.capture_bulk_outbox_publication_values(_valid_entry())
    assert bound2 is not None and diags2 == []
    assert bound2 == bound

    try:
        bound.revision = 2
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("bound not frozen")

    caller = _valid_entry()
    bound0, diags0 = runtime.capture_bulk_outbox_publication_values(caller)
    assert bound0 is not None and diags0 == []
    caller["event_id"] = "mute"
    caller["revision"] = 999
    assert bound0.event_id == "event-test"
    assert bound0.revision == 1

    retrying = _valid_entry()
    retrying["state"] = "RETRYING"
    retrying["next_attempt_at"] = NEXT_AT
    assert runtime.validate_bulk_outbox_publication_values(retrying) == []
    published = _valid_entry()
    published["state"] = "PUBLISHED"
    published["published_at"] = PUBLISHED_AT
    assert runtime.validate_bulk_outbox_publication_values(published) == []

    hors = _valid_entry()
    hors["intrus"] = "x"
    assert runtime.validate_bulk_outbox_publication_values(hors)
    s_hors, d_hors = runtime.capture_bulk_outbox_publication_values(hors)
    assert s_hors is None and d_hors

    for foreign in (None, 0, "x", []):
        assert runtime.validate_bulk_outbox_publication_values(foreign)
        s_f, d_f = runtime.capture_bulk_outbox_publication_values(foreign)
        assert s_f is None and d_f

    hostile = _valid_entry()
    hostile["event_id"] = Hostile()
    assert runtime.validate_bulk_outbox_publication_values(hostile)
    s_h, d_h = runtime.capture_bulk_outbox_publication_values(hostile)
    assert s_h is None and d_h

    leased = _valid_entry()
    leased["lease_owner"] = "bail-test"
    assert runtime.validate_bulk_outbox_publication_values(leased)
    leased["lease_expires_at"] = LEASE_AT
    assert runtime.validate_bulk_outbox_publication_values(leased) == []

    assert counters == {key: 0 for key in counters}, "primitives produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_OUTBOX_PUBLICATION_SAFE_INTEGRATION_OK")
'''


class TestBulkOutboxPublicationFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_outbox_publication_guard_probe.txt")
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
