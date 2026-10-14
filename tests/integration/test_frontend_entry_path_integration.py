"""Import puis fonction pure FrontendEntryPath v1 en processus frais sous gardes."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "FRONTEND_ENTRY_PATH_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = r'''
import builtins
import contextlib
import io
import os
import socket
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

src_path = sys.argv[1]
probe = sys.argv[2]
counters = {"reads": 0, "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "fs": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")

sys.path.insert(0, src_path)
environ_type = type(os.environ)
original_open = builtins.open


class GuardBlocked(Exception):
    pass


class _BlockedImportFinder:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("blocked by integration guard")
        return None


def _guarded_import_open(file, mode="r", *args, **kwargs):
    if any(flag in mode for flag in "wax+"):
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    return original_open(file, mode, *args, **kwargs)


def _guarded_open(file, mode="r", *args, **kwargs):
    key = "writes" if any(flag in mode for flag in "wax+") else "reads"
    counters[key] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_io_open(file, *args, **kwargs):
    return _guarded_open(file, *args, **kwargs)


def _guarded_path_open(self, *args, **kwargs):
    return _guarded_open(self, *args, **kwargs)


def _guarded_os_open(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_stat(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_lstat(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_access(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_listdir(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_scandir(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_resolve(self, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_path_stat(self, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_socket(*args, **kwargs):
    counters["network"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_popen(*args, **kwargs):
    counters["process"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_system(*args, **kwargs):
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
    stack.enter_context(patch.object(builtins, "open", new=_guarded_import_open))
    stack.enter_context(patch.object(socket, "socket", new=_guarded_socket))
    stack.enter_context(patch.object(subprocess, "Popen", new=_guarded_popen))
    stack.enter_context(patch.object(os, "system", new=_guarded_system))
    stack.enter_context(patch.object(environ_type, "__getitem__", new=_guarded_environ_getitem))
    stack.enter_context(patch.object(sys, "meta_path", new=[_BlockedImportFinder()] + list(sys.meta_path)))

    _positive_control("import-write", lambda: builtins.open(probe, "w"))
    assert counters["writes"] == 1
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

    import pixs.kernel.frontend_entry_paths as module
    from pixs.kernel.frontend_entry_paths import validate_frontend_entry_path_v1
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"
    assert module.__all__ == ["validate_frontend_entry_path_v1"]
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    stack.enter_context(patch.object(builtins, "open", new=_guarded_open))
    stack.enter_context(patch.object(io, "open", new=_guarded_io_open))
    stack.enter_context(patch.object(Path, "open", new=_guarded_path_open))
    stack.enter_context(patch.object(os, "open", new=_guarded_os_open))
    stack.enter_context(patch.object(os, "stat", new=_guarded_stat))
    stack.enter_context(patch.object(os, "lstat", new=_guarded_lstat))
    stack.enter_context(patch.object(os, "access", new=_guarded_access))
    stack.enter_context(patch.object(os, "listdir", new=_guarded_listdir))
    stack.enter_context(patch.object(os, "scandir", new=_guarded_scandir))
    stack.enter_context(patch.object(Path, "resolve", new=_guarded_resolve))
    stack.enter_context(patch.object(Path, "stat", new=_guarded_path_stat))

    _positive_control("open-write", lambda: builtins.open(probe, "w"))
    assert counters["writes"] == 1
    _positive_control("open-read", lambda: builtins.open(probe, "r"))
    assert counters["reads"] == 1
    _positive_control("io-open", lambda: io.open(probe, "r"))
    assert counters["reads"] == 2
    _positive_control("path-open", lambda: Path(probe).open("r"))
    assert counters["reads"] == 3
    _positive_control("os-open", lambda: os.open(probe, os.O_RDONLY))
    assert counters["fs"] == 1
    _positive_control("stat", lambda: os.stat(probe))
    assert counters["fs"] == 2
    _positive_control("lstat", lambda: os.lstat(probe))
    assert counters["fs"] == 3
    _positive_control("access", lambda: os.access(probe, os.R_OK))
    assert counters["fs"] == 4
    _positive_control("listdir", lambda: os.listdir("."))
    assert counters["fs"] == 5
    _positive_control("scandir", lambda: os.scandir("."))
    assert counters["fs"] == 6
    _positive_control("resolve", lambda: Path("a/b").resolve())
    assert counters["fs"] == 7
    _positive_control("path-stat", lambda: Path("a/b").stat())
    assert counters["fs"] == 8
    counters.update((key, 0) for key in counters)

    for valid in ("frontend/routes/contacts", "donn\u00e9es/\u00e9t\u00e9", " a/b", "a/b ", ".hidden/route"):
        assert validate_frontend_entry_path_v1(valid) == valid
    for invalid in ("", "/a", "a//b", "a/./b", "a/../b", "a\\b", "a:b", "a?b", "a#b", "a%b", "a\x00b", "a\x7fb", "\ud800", "\udc00"):
        try:
            validate_frontend_entry_path_v1(invalid)
        except ValueError as exc:
            assert str(exc) == "FrontendEntryPath v1 invalide"
            if invalid != "":
                assert invalid not in str(exc)
        else:
            raise AssertionError("invalid accepted: " + repr(invalid))
    for bad in (None, 123, b"a"):
        try:
            validate_frontend_entry_path_v1(bad)
        except TypeError as exc:
            assert str(exc) == "FrontendEntryPath v1 invalide"
        else:
            raise AssertionError("non-str accepted: " + repr(bad))
    assert counters == {key: 0 for key in counters}, "validator produced observable I/O"
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

print("FRONTEND_ENTRY_PATH_SAFE_INTEGRATION_OK")
'''


class TestFrontendEntryPathFreshProcess(unittest.TestCase):
    def test_pure_function_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "frontend_entry_path_guard_probe.txt")
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
