"""Intégration FingerprintV1 en processus frais sous gardes (unittest seul)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "BULK_ADMISSION_FINGERPRINT_SAFE_INTEGRATION_OK"
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

    import pixs.backend.bulk_admission_fingerprint as runtime
    assert counters == {key: 0 for key in counters}, "import produced effects"
    state["read_block"] = True
    _positive_control("read", lambda: builtins.open(read_probe, "r"))
    _positive_control("read io", lambda: io.open(read_probe))
    assert counters["reads"] == 2
    counters.update((key, 0) for key in counters)

    FIXTURE_EXPIRES = datetime(1, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    EXPECTED_TEXT = '{"bulk_type":"IMPORT","bulk_version":"1.0.0","commit_mode":"VALIDATE_ONLY","conflict_strategy":"REJECT","consistency_kind":null,"consistency_reference":null,"execution_version":"1.0.0","expires_at":"0001-01-02T03:04:05.000006Z","format":"CSV","idempotency_key":"clé-é","input_reference":"objet-é","input_sha256":"0000000000000000000000000000000000000000000000000000000000000000","input_size_bytes":0,"input_version":"v1","mapping_reference":"mapping","mapping_version":"1.0.0","policy_reference":"policy","policy_version":"1.0.0","projection_reference":null,"requested_by_reference":"sujet-é","scope_context_reference":null,"tenant_context_reference":"tenant-é"}'
    EXPECTED_SHA = "e20cf2666bebd31f919db9220e926a456ee53f93926c21c04ef6c58691a1dc41"

    def _valid_import():
        return {
            "execution_version": "1.0.0",
            "bulk_type": "IMPORT",
            "bulk_version": "1.0.0",
            "tenant_context_reference": "tenant-é",
            "scope_context_reference": None,
            "format": "CSV",
            "conflict_strategy": "REJECT",
            "commit_mode": "VALIDATE_ONLY",
            "requested_by_reference": "sujet-é",
            "mapping_reference": "mapping",
            "mapping_version": "1.0.0",
            "input_reference": "objet-é",
            "input_version": "v1",
            "input_sha256": "0" * 64,
            "input_size_bytes": 0,
            "projection_reference": None,
            "consistency_kind": None,
            "consistency_reference": None,
            "idempotency_key": "clé-é",
            "policy_reference": "policy",
            "policy_version": "1.0.0",
            "expires_at": FIXTURE_EXPIRES,
        }

    def _valid_export():
        base = _valid_import()
        base["bulk_type"] = "EXPORT"
        base["input_reference"] = None
        base["input_version"] = None
        base["input_sha256"] = None
        base["input_size_bytes"] = None
        base["projection_reference"] = "proj"
        base["consistency_kind"] = "SNAPSHOT"
        base["consistency_reference"] = None
        return base

    assert runtime.validate_bulk_admission_fingerprint_values(_valid_import()) == []
    snap, diags = runtime.capture_bulk_admission_fingerprint(_valid_import())
    assert snap is not None and diags == []
    assert snap.canonical_bytes == EXPECTED_TEXT.encode("utf-8")
    assert snap.content_sha256 == EXPECTED_SHA

    caller = _valid_export()
    assert caller["consistency_reference"] is None
    snap0, diags0 = runtime.capture_bulk_admission_fingerprint(caller)
    assert snap0 is not None and diags0 == []
    before = bytes(snap0.canonical_bytes)
    caller["consistency_reference"] = "mutee"
    assert snap0.canonical_bytes == before

    other = _valid_import()
    other["idempotency_key"] = "autre"
    snap1, _ = runtime.capture_bulk_admission_fingerprint(other)
    assert snap1 is not None and snap1.content_sha256 != snap.content_sha256

    hors = _valid_import()
    hors["operation_id"] = "x"
    assert runtime.validate_bulk_admission_fingerprint_values(hors)
    s_hors, d_hors = runtime.capture_bulk_admission_fingerprint(hors)
    assert s_hors is None and d_hors

    assert counters == {key: 0 for key in counters}, "primitives produced forbidden effects"
    assert "pixs.core" not in sys.modules
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules
    assert not os.path.exists(probe)

print("BULK_ADMISSION_FINGERPRINT_SAFE_INTEGRATION_OK")
'''


class TestBulkAdmissionFingerprintFreshProcess(unittest.TestCase):
    def test_import_and_controls_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "bulk_admission_fingerprint_guard_probe.txt")
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
