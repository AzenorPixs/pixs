"""Import puis fonction composite FrontendContributionDeclaration v1 en processus frais sous gardes."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "FRONTEND_CONTRIBUTION_DECLARATION_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 10
FIXED_ENV = {"LANG": "C.UTF-8", "PATH": "/usr/bin:/bin"}

WORKER = r'''
import builtins
import contextlib
import io
import _io
import os
import socket
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

src_path = sys.argv[1]
probe = sys.argv[2]
tmpdir = sys.argv[3]
canary_name = sys.argv[4]
counters = {"reads": 0, "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "fs": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")
MESSAGE = "FrontendContributionDeclaration v1 invalide"

sys.path.insert(0, src_path)
sys.path.insert(0, tmpdir)
environ_type = type(os.environ)
original_builtins_open = builtins.open
original_io_open = io.open
original_io_open_code = io.open_code if hasattr(io, "open_code") else None
original__io_open_code = _io.open_code if hasattr(_io, "open_code") else None
original_os_open = os.open
original_os_stat = os.stat
original_os_lstat = os.lstat
original_os_access = os.access
original_os_listdir = os.listdir
original_os_scandir = os.scandir
original_path_open = Path.open
original_path_resolve = Path.resolve
original_path_stat = Path.stat


class GuardBlocked(Exception):
    pass


class _BlockedImportFinder:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".", 1)[0] in BLOCKED_DB_ROOTS:
            counters["db"] += 1
            raise GuardBlocked("blocked by integration guard")
        return None


def _is_loader_allowed():
    frame = sys._getframe(2)
    loader_modules = {
        "_frozen_importlib", "_frozen_importlib_external",
        "importlib._bootstrap", "importlib._bootstrap_external", "zipimport",
    }
    while frame is not None:
        filename = frame.f_code.co_filename
        name = frame.f_globals.get("__name__", "")
        function = frame.f_code.co_name
        if filename == "<string>" and function.startswith("_guarded_"):
            frame = frame.f_back
            continue
        if (
            name == "pixs" or name.startswith("pixs.")
            or filename.startswith(src_path + os.sep)
            or filename.startswith(tmpdir + os.sep)
            or filename == "<string>"
        ):
            return False
        if name in loader_modules:
            return True
        frame = frame.f_back
    return False


def _mode_is_write(mode):
    return any(flag in mode for flag in "wax+")


def _guarded_builtins_open(file, mode="r", *args, **kwargs):
    if _mode_is_write(mode):
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    if _is_loader_allowed():
        return original_builtins_open(file, mode, *args, **kwargs)
    counters["reads"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_io_open(file, mode="r", *args, **kwargs):
    if _mode_is_write(mode):
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    if _is_loader_allowed():
        return original_io_open(file, mode, *args, **kwargs)
    counters["reads"] += 1
    raise GuardBlocked("blocked by integration guard")


def _blocked_read_open(file, *args, **kwargs):
    counters["reads"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_io_open_code(path, *args, **kwargs):
    if _is_loader_allowed():
        return original_io_open_code(path, *args, **kwargs)
    counters["reads"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded__io_open_code(path, *args, **kwargs):
    if _is_loader_allowed():
        return original__io_open_code(path, *args, **kwargs)
    counters["reads"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_path_open(self, mode="r", *args, **kwargs):
    if _mode_is_write(mode):
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    if _is_loader_allowed():
        return original_path_open(self, mode, *args, **kwargs)
    counters["reads"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_os_open(path, flags, *args, **kwargs):
    write_flags = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
    if flags & write_flags:
        counters["writes"] += 1
        raise GuardBlocked("blocked by integration guard")
    if _is_loader_allowed():
        return original_os_open(path, flags, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_stat(path, *args, **kwargs):
    if _is_loader_allowed():
        return original_os_stat(path, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_lstat(path, *args, **kwargs):
    if _is_loader_allowed():
        return original_os_lstat(path, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_access(path, *args, **kwargs):
    if _is_loader_allowed():
        return original_os_access(path, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_listdir(path, *args, **kwargs):
    if _is_loader_allowed():
        return original_os_listdir(path, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_scandir(path, *args, **kwargs):
    if _is_loader_allowed():
        return original_os_scandir(path, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_resolve(self, *args, **kwargs):
    if _is_loader_allowed():
        return original_path_resolve(self, *args, **kwargs)
    counters["fs"] += 1
    raise GuardBlocked("blocked by integration guard")


def _guarded_path_stat(self, *args, **kwargs):
    if _is_loader_allowed():
        return original_path_stat(self, *args, **kwargs)
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


def _positive_control(label, callable_target, counter):
    before = dict(counters)
    try:
        callable_target()
    except GuardBlocked:
        expected = dict(before)
        expected[counter] += 1
        assert counters == expected, "unexpected guard counters: " + label
        return
    raise AssertionError("guard did not block: " + label)


def _make_valid(**overrides):
    base = {
        "type": "ROUTE",
        "id": "acme.crm.contacts",
        "entry": "frontend/routes/contacts",
        "version": "1.0.0",
        "requires": [],
        "scope": "PUBLIC",
    }
    base.update(overrides)
    return base


for root in BLOCKED_DB_ROOTS:
    assert root not in sys.modules, "db module preloaded: " + root

with contextlib.ExitStack() as stack:
    stack.enter_context(patch.object(builtins, "open", new=_guarded_builtins_open))
    stack.enter_context(patch.object(io, "open", new=_guarded_io_open))
    if original_io_open_code is not None:
        stack.enter_context(patch.object(io, "open_code", new=_guarded_io_open_code))
    if original__io_open_code is not None:
        stack.enter_context(patch.object(_io, "open_code", new=_guarded__io_open_code))
    stack.enter_context(patch.object(Path, "open", new=_guarded_path_open))
    stack.enter_context(patch.object(os, "open", new=_guarded_os_open))
    stack.enter_context(patch.object(os, "stat", new=_guarded_stat))
    stack.enter_context(patch.object(os, "lstat", new=_guarded_lstat))
    stack.enter_context(patch.object(os, "access", new=_guarded_access))
    stack.enter_context(patch.object(os, "listdir", new=_guarded_listdir))
    stack.enter_context(patch.object(os, "scandir", new=_guarded_scandir))
    stack.enter_context(patch.object(Path, "resolve", new=_guarded_resolve))
    stack.enter_context(patch.object(Path, "stat", new=_guarded_path_stat))
    stack.enter_context(patch.object(socket, "socket", new=_guarded_socket))
    stack.enter_context(patch.object(subprocess, "Popen", new=_guarded_popen))
    stack.enter_context(patch.object(os, "system", new=_guarded_system))
    stack.enter_context(patch.object(environ_type, "__getitem__", new=_guarded_environ_getitem))
    stack.enter_context(patch.object(sys, "meta_path", new=[_BlockedImportFinder()] + list(sys.meta_path)))

    controls = [
        ("builtins-write", lambda: builtins.open(probe, "w"), "writes"),
        ("builtins-read", lambda: builtins.open(probe, "r"), "reads"),
        ("io-read", lambda: io.open(probe, "r"), "reads"),
        ("io-write", lambda: io.open(probe, "w"), "writes"),
        ("path-read", lambda: Path(probe).open("r"), "reads"),
        ("path-write", lambda: Path(probe).open("w"), "writes"),
        ("os-open-read", lambda: os.open(probe, os.O_RDONLY), "fs"),
        ("os-open-write", lambda: os.open(probe, os.O_WRONLY | os.O_CREAT), "writes"),
        ("stat", lambda: os.stat(probe), "fs"),
        ("lstat", lambda: os.lstat(probe), "fs"),
        ("access", lambda: os.access(probe, os.R_OK), "fs"),
        ("listdir", lambda: os.listdir("."), "fs"),
        ("scandir", lambda: os.scandir("."), "fs"),
        ("resolve", lambda: Path("a/b").resolve(), "fs"),
        ("path-stat", lambda: Path("a/b").stat(), "fs"),
        ("socket", lambda: socket.socket(), "network"),
        ("popen", lambda: subprocess.Popen(["/usr/bin/true"]), "process"),
        ("system", lambda: os.system("true"), "process"),
        ("environ", lambda: os.environ["PATH"], "environ"),
        ("getenv", lambda: os.getenv("PATH"), "environ"),
    ]
    if original_io_open_code is not None:
        controls.append(("io-open-code", lambda: io.open_code(probe), "reads"))
    if original__io_open_code is not None:
        controls.append(("_io-open-code", lambda: _io.open_code(probe), "reads"))
    for label, target, counter in controls:
        _positive_control(label, target, counter)
    for root in BLOCKED_DB_ROOTS:
        _positive_control("db-" + root, lambda root=root: __import__(root), "db")
        assert root not in sys.modules, "db module loaded: " + root
    assert not hasattr(sys, "_fcd_guard_canary_entered")
    before = dict(counters)
    try:
        __import__(canary_name)
    except GuardBlocked:
        assert getattr(sys, "_fcd_guard_canary_entered", False) is True
    else:
        raise AssertionError("canary import not blocked")
    expected = dict(before)
    expected["reads"] += 1
    assert counters == expected, "canary must reach its application read only"
    del sys._fcd_guard_canary_entered
    assert canary_name not in sys.modules
    counters.update((key, 0) for key in counters)

    import pixs.kernel.frontend_contribution_declarations as module
    from pixs.kernel.frontend_contribution_declarations import validate_frontend_contribution_declaration_v1
    assert counters == {key: 0 for key in counters}, "module import produced observable effects"
    assert module.__all__ == ["validate_frontend_contribution_declaration_v1"]
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    snapshot = validate_frontend_contribution_declaration_v1(_make_valid(
        type="PAGE",
        id="pixs.contacts",
        entry="frontend/routes/contacts",
        version="1.2.3-alpha.1+build.11",
        requires=["audit >=1.0.0 <2.0.0", "pkg-b ==2.0.0", "audit >=1.0.0 <2.0.0"],
        scope="TENANT_SCOPED",
    ))
    assert snapshot.type == "PAGE"
    assert snapshot.id == "pixs.contacts"
    assert snapshot.entry == "frontend/routes/contacts"
    assert snapshot.version == "1.2.3-alpha.1+build.11"
    assert snapshot.requires == ("audit >=1.0.0 <2.0.0", "pkg-b ==2.0.0", "audit >=1.0.0 <2.0.0")
    assert type(snapshot.requires) is tuple
    assert snapshot.scope == "TENANT_SCOPED"
    for invalid in (
        _make_valid(type="UNKNOWN_TYPE"),
        _make_valid(id="a"),
        _make_valid(entry="/a"),
        _make_valid(version=""),
        _make_valid(version="^1.0.0"),
        _make_valid(version=">=1.0.0"),
        _make_valid(version="1.0"),
        _make_valid(requires=[""]),
        _make_valid(requires=["pkg-a ^1.0.0"]),
        _make_valid(requires=["pkg-b ~1.2.0"]),
        _make_valid(requires=["pkg-c *"]),
        _make_valid(requires=["pkg-a >=1.0.0 || pkg-a ==2.0.0"]),
        _make_valid(scope="UNKNOWN"),
        _make_valid(scope="public"),
    ):
        try:
            validate_frontend_contribution_declaration_v1(invalid)
        except ValueError as exc:
            assert str(exc) == MESSAGE
        else:
            raise AssertionError("invalid accepted")
    sentinel = "SENTINELLE_XYZ_789.SENTINELLE/XYZ_789"
    try:
        validate_frontend_contribution_declaration_v1(_make_valid(id=sentinel))
    except ValueError as exc:
        assert str(exc) == MESSAGE
        assert sentinel not in str(exc)
    else:
        raise AssertionError("sentinel accepted")
    for bad in (None, 123, "x", b"x", ["type"], {"type": "x"}):
        try:
            validate_frontend_contribution_declaration_v1(bad)
        except (TypeError, ValueError) as exc:
            assert str(exc) == MESSAGE
        else:
            raise AssertionError("non-dict accepted")
    assert counters == {key: 0 for key in counters}, "validator produced observable I/O"
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

print("FRONTEND_CONTRIBUTION_DECLARATION_SAFE_INTEGRATION_OK")
'''


class TestFrontendContributionDeclarationFreshProcess(unittest.TestCase):
    def test_pure_function_in_fresh_process_with_minimal_env(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            canary_name = "canary_import_probe"
            canary_path = Path(tmp) / (canary_name + ".py")
            canary_path.write_text('import builtins\nimport sys\nsys._fcd_guard_canary_entered = True\nbuiltins.open(__file__, "rb")\n', encoding="utf-8")
            probe = str(Path(tmp) / "frontend_contribution_declaration_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe, tmp, canary_name],
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
