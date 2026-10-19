"""Import puis fonction pure FrontendContributionId v1 en processus frais."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "FRONTEND_CONTRIBUTION_ID_SAFE_INTEGRATION_OK"
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


class _BlockingImportLoader:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("bloqué par la garde d'intégration")
        return None


def _guarded_import_open(file, mode="r", *args, **kwargs):
    if any(flag in mode for flag in "wax+"):
        counters["writes"] += 1
        raise GuardBlocked("bloqué par la garde d'intégration")
    return original_open(file, mode, *args, **kwargs)


def _guarded_open(file, mode="r", *args, **kwargs):
    key = "writes" if any(flag in mode for flag in "wax+") else "reads"
    counters[key] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_io_open(file, *args, **kwargs):
    return _guarded_open(file, *args, **kwargs)


def _guarded_path_open(self, *args, **kwargs):
    return _guarded_open(self, *args, **kwargs)


def _guarded_os_open(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_stat(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_lstat(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_access(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_listdir(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_scandir(path, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_resolve(self, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_path_stat(self, *args, **kwargs):
    counters["fs"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_socket(*args, **kwargs):
    counters["network"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_popen(*args, **kwargs):
    counters["process"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_system(*args, **kwargs):
    counters["process"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _guarded_environ_getitem(mapping, key):
    counters["environ"] += 1
    raise GuardBlocked("bloqué par la garde d'intégration")


def _assert_guard(label, target):
    try:
        target()
    except GuardBlocked:
        return
    raise AssertionError("garde inactive : " + label)


for root in BLOCKED_DB_ROOTS:
    assert root not in sys.modules, "module DB préchargé : " + root

with contextlib.ExitStack() as stack:
    stack.enter_context(patch.object(builtins, "open", new=_guarded_import_open))
    stack.enter_context(patch.object(socket, "socket", new=_guarded_socket))
    stack.enter_context(patch.object(subprocess, "Popen", new=_guarded_popen))
    stack.enter_context(patch.object(os, "system", new=_guarded_system))
    stack.enter_context(patch.object(environ_type, "__getitem__", new=_guarded_environ_getitem))
    stack.enter_context(patch.object(sys, "meta_path", new=[_BlockingImportLoader()] + list(sys.meta_path)))

    _assert_guard("écriture-import", lambda: builtins.open(probe, "w"))
    assert counters["writes"] == 1
    _assert_guard("socket", lambda: socket.socket())
    assert counters["network"] == 1
    _assert_guard("popen", lambda: subprocess.Popen(["/usr/bin/true"]))
    assert counters["process"] == 1
    _assert_guard("system", lambda: os.system("true"))
    assert counters["process"] == 2
    _assert_guard("environ", lambda: os.environ["PATH"])
    assert counters["environ"] == 1
    _assert_guard("getenv", lambda: os.getenv("PATH"))
    assert counters["environ"] == 2
    _assert_guard("db", lambda: __import__("sqlite3"))
    assert counters["db"] == 1
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "module DB chargé : " + root
    counters.update((key, 0) for key in counters)

    import pixs.kernel.frontend_contribution_ids as module
    from pixs.kernel.frontend_contribution_ids import validate_frontend_contribution_id_v1
    assert counters == {key: 0 for key in counters}, "import du module avec effets observables"
    assert module.__all__ == ["validate_frontend_contribution_id_v1"]
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "module DB chargé : " + root

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

    _assert_guard("écriture-open", lambda: builtins.open(probe, "w"))
    assert counters["writes"] == 1
    _assert_guard("lecture-open", lambda: builtins.open(probe, "r"))
    assert counters["reads"] == 1
    _assert_guard("io-open", lambda: io.open(probe, "r"))
    assert counters["reads"] == 2
    _assert_guard("chemin-open", lambda: Path(probe).open("r"))
    assert counters["reads"] == 3
    _assert_guard("os-open", lambda: os.open(probe, os.O_RDONLY))
    assert counters["fs"] == 1
    _assert_guard("stat", lambda: os.stat(probe))
    assert counters["fs"] == 2
    _assert_guard("lstat", lambda: os.lstat(probe))
    assert counters["fs"] == 3
    _assert_guard("access", lambda: os.access(probe, os.R_OK))
    assert counters["fs"] == 4
    _assert_guard("listdir", lambda: os.listdir("."))
    assert counters["fs"] == 5
    _assert_guard("scandir", lambda: os.scandir("."))
    assert counters["fs"] == 6
    _assert_guard("resolve", lambda: Path("a/b").resolve())
    assert counters["fs"] == 7
    _assert_guard("chemin-stat", lambda: Path("a/b").stat())
    assert counters["fs"] == 8
    counters.update((key, 0) for key in counters)

    for valid in ("acme.crm.contacts", "ACME.crm-2.contacts_1", "pixs.contacts", "-._"):
        assert validate_frontend_contribution_id_v1(valid) == valid
    for invalid in ("", "a", ".a", "a.", "a..b", "a b.c", "a\tb.c", "a\x00b.c", "a\x7fb.c", "donn\u00e9es.\u00e9t\u00e9", "a/b.c", "a:b.c", "\ud800.c"):
        try:
            validate_frontend_contribution_id_v1(invalid)
        except ValueError as exc:
            assert str(exc) == "FrontendContributionId v1 invalide"
        else:
            raise AssertionError("invalide accepté : " + repr(invalid))
    sentinel = "SENTINELLE_XYZ_789.SENTINELLE/XYZ_789"
    try:
        validate_frontend_contribution_id_v1(sentinel)
    except ValueError as exc:
        assert str(exc) == "FrontendContributionId v1 invalide"
        assert sentinel not in str(exc)
    else:
        raise AssertionError("sentinelle acceptée")
    for bad in (None, 123, b"a.c"):
        try:
            validate_frontend_contribution_id_v1(bad)
        except TypeError as exc:
            assert str(exc) == "FrontendContributionId v1 invalide"
        else:
            raise AssertionError("non-str accepté : " + repr(bad))
    assert counters == {key: 0 for key in counters}, "validateur avec entrées-sorties observables"
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "module DB chargé : " + root

print("FRONTEND_CONTRIBUTION_ID_SAFE_INTEGRATION_OK")
'''


class TestFrontendContributionIdFreshProcess(unittest.TestCase):
    def test_pure_function_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            probe = str(Path(tmp) / "frontend_contribution_id_guard_probe.txt")
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
