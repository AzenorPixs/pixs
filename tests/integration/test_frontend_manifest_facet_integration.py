"""Import puis facette FrontendManifestFacet v1 en processus frais sous gardes."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
MARKER = "FRONTEND_MANIFEST_FACET_SAFE_INTEGRATION_OK"
TIMEOUT_SECONDS = 20
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
from dataclasses import FrozenInstanceError

src_path = sys.argv[1]
probe = sys.argv[2]
tmpdir = sys.argv[3]
canary_name = sys.argv[4]
order = sys.argv[5]
counters = {"reads": 0, "writes": 0, "network": 0, "process": 0, "environ": 0, "db": 0, "fs": 0}
BLOCKED_DB_ROOTS = ("sqlite3", "psycopg", "psycopg2", "django")

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


def _valid_contribution(**overrides):
    base = {
        "type": "ROUTE",
        "id": "acme.crm.contacts",
        "entry": "frontend/routes/contacts",
        "version": "1.0.0",
        "requires": [],
        "scope": "TENANT_SCOPED",
    }
    base.update(overrides)
    return base


def _base_manifest(comp_type="MODULE", with_frontend=True, contributions=None):
    data = {"schema_version": "1", "id": "demo", "type": comp_type, "version": "1.0.0"}
    if with_frontend:
        data["frontend"] = {
            "schema_version": "1",
            "contributions": [] if contributions is None else list(contributions),
        }
    return data


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
    assert not hasattr(sys, "_fmf_guard_canary_entered")
    before = dict(counters)
    try:
        __import__(canary_name)
    except GuardBlocked:
        assert getattr(sys, "_fmf_guard_canary_entered", False) is True
    else:
        raise AssertionError("canary import not blocked")
    expected = dict(before)
    expected["reads"] += 1
    assert counters == expected, "canary must reach its application read only"
    del sys._fmf_guard_canary_entered
    assert canary_name not in sys.modules
    counters.update((key, 0) for key in counters)

    assert order in ("manifest-first", "fcd-first"), "unknown order"
    if order == "manifest-first":
        import pixs.kernel.manifest as manifest_module
        import pixs.kernel.frontend_contribution_declarations as fcd_module
    else:
        import pixs.kernel.frontend_contribution_declarations as fcd_module
        import pixs.kernel.manifest as manifest_module
    from pixs.kernel.frontend_contribution_declarations import validate_frontend_contribution_declaration_v1
    from pixs.kernel.manifest import ManifestValidationError, parse_manifest
    from pixs.kernel.manifest import parse_manifest_text
    assert counters == {key: 0 for key in counters}, "imports produced observable effects"
    assert "parse_manifest" in manifest_module.__all__
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

    # Factory directe prouve la fixture valide (pas de résolution/activation/chargement).
    canonical = _valid_contribution()
    proven = validate_frontend_contribution_declaration_v1(dict(canonical))
    assert proven.id == "acme.crm.contacts"
    try:
        with patch(
            "pixs.kernel.frontend_contribution_declarations.validate_frontend_contribution_declaration_v1",
            side_effect=RuntimeError("boom"),
        ):
            parse_manifest(_base_manifest(contributions=[canonical]))
    except RuntimeError:
        pass
    else:
        raise AssertionError("unexpected factory error swallowed")
    assert counters == {key: 0 for key in counters}, "factory patch produced I/O"

    # Absence frontend legacy inchangée (six types).
    for owner in ("KERNEL", "MODULE", "SUBMODULE", "PROVIDER", "EXTENSION", "THEME"):
        parsed = parse_manifest(_base_manifest(comp_type=owner, with_frontend=False))
        assert parsed.frontend is None
        assert parsed.type == owner
    # MODULE/SUBMODULE facette vide reconnue sans activation.
    for owner in ("MODULE", "SUBMODULE"):
        empty = parse_manifest(_base_manifest(comp_type=owner, contributions=[]))
        assert empty.frontend is not None
        assert empty.frontend.schema_version == "1"
        assert empty.frontend.contributions == ()
        empty_text = parse_manifest_text(
            'schema_version = "1"\nid = "demo"\ntype = "' + owner + '"\nversion = "1.0.0"\n'
            '[frontend]\nschema_version = "1"\ncontributions = []\n'
        )
        assert empty_text.frontend is not None
        assert empty_text.frontend.contributions == ()
    assert counters == {key: 0 for key in counters}, "legacy/empty produced I/O"

    # Contributions 3 : doublons/ordre/requires/version texte/casse immuables.
    first = _valid_contribution()
    second = _valid_contribution(
        type="PAGE",
        id="ACME.crm.second",
        entry="frontend/pages/second",
        version="1.2.3-beta+build.1",
        requires=["audit >=1.0.0", "audit >=1.0.0"],
        scope="AUTHENTICATED",
    )
    third = dict(first)
    for item in (first, second, third):
        validate_frontend_contribution_declaration_v1(dict(item))
    manifest_data = _base_manifest(contributions=[first, second, third])
    parsed = parse_manifest(manifest_data)
    assert parsed.frontend is not None
    assert len(parsed.frontend.contributions) == 3
    assert [c.id for c in parsed.frontend.contributions] == ["acme.crm.contacts", "ACME.crm.second", "acme.crm.contacts"]
    assert parsed.frontend.contributions[1].version == "1.2.3-beta+build.1"
    assert parsed.frontend.contributions[1].requires == ("audit >=1.0.0", "audit >=1.0.0")
    assert type(parsed.frontend.contributions[1].requires) is tuple
    assert parsed.frontend.contributions[0] == parsed.frontend.contributions[2]
    # Text API ordonnée avec doublon.
    toml_text = 'schema_version="1"\nid="demo"\ntype="SUBMODULE"\nversion="1.0.0"\n[frontend]\nschema_version="1"\n'
    unit = '\n[[frontend.contributions]]\ntype="ROUTE"\nid="ACME.contacts"\nentry="frontend/contacts"\nversion="1.2.3-beta+build.1"\nrequires=["audit >=1.0.0", "audit >=1.0.0"]\nscope="TENANT_SCOPED"\n'
    parsed_text = parse_manifest_text(toml_text + unit + unit)
    assert parsed_text.frontend is not None
    assert len(parsed_text.frontend.contributions) == 2
    assert parsed_text.frontend.contributions[0].id == "ACME.contacts"
    # Mutation raw après parse sans altération du snapshot.
    first["id"] = "acme.crm.mutated"
    manifest_data["frontend"]["contributions"].append(_valid_contribution())
    manifest_data["frontend"]["contributions"][0]["requires"].append("acme.x >=9.0.0")
    assert parsed.frontend.contributions[0].id == "acme.crm.contacts"
    assert parsed.frontend.contributions[0].requires == ()
    assert len(parsed.frontend.contributions) == 3
    for target, field, value in ((parsed, "frontend", None), (parsed.frontend, "schema_version", "2"), (parsed.frontend.contributions[0], "id", "mutated")):
        try:
            setattr(target, field, value)
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError("snapshot is mutable")
    assert counters == {key: 0 for key in counters}, "positive parse produced I/O"

    # Invalides : frontend null/schema2/keys/owner + six champs FCD, sans sentinel.
    sentinel = "SENTINELLE_XYZ_789.SENTINELLE/XYZ_789"
    from pixs.kernel.manifest import ManifestValidationError as _MVE
    for bad_frontend in (None, [], "frontend", 42, True):
        bad = _base_manifest(with_frontend=False)
        bad["frontend"] = bad_frontend
        try:
            parse_manifest(bad)
        except _MVE as exc:
            assert any("frontend" in d for d in exc.diagnostics)
            assert sentinel not in str(exc)
        else:
            raise AssertionError("bad frontend accepted")
    for bad_version in ("2", "", 1, None):
        bad = _base_manifest(contributions=[])
        bad["frontend"]["schema_version"] = bad_version
        try:
            parse_manifest(bad)
        except _MVE:
            pass
        else:
            raise AssertionError("bad facet version accepted")
    bad_keys = _base_manifest(contributions=[])
    bad_keys["frontend"]["extra"] = "1"
    try:
        parse_manifest(bad_keys)
    except _MVE:
        pass
    else:
        raise AssertionError("extra facet key accepted")
    for owner in ("KERNEL", "PROVIDER", "EXTENSION", "THEME"):
        try:
            parse_manifest(_base_manifest(comp_type=owner, contributions=[]))
        except _MVE:
            pass
        else:
            raise AssertionError("owner accepted")
    for field in ("type", "id", "entry", "version", "requires", "scope"):
        contrib = _valid_contribution()
        del contrib[field]
        try:
            parse_manifest(_base_manifest(contributions=[contrib]))
        except _MVE as exc:
            assert sentinel not in ";".join(exc.diagnostics)
        else:
            raise AssertionError("missing FCD field accepted")
    try:
        parse_manifest(_base_manifest(contributions=[_valid_contribution(id=sentinel)]))
    except _MVE as exc:
        assert sentinel not in ";".join(exc.diagnostics)
        assert sentinel not in str(exc)
    else:
        raise AssertionError("sentinel accepted")
    # Garde commune : entry frontend/eval(1) lexicale FCD-valide mais manifest refusé.
    entry = "frontend/eval(1)"
    validate_frontend_contribution_declaration_v1(_valid_contribution(entry=entry))
    try:
        parse_manifest(_base_manifest(contributions=[_valid_contribution(entry=entry)]))
    except _MVE as exc:
        joined = ";".join(exc.diagnostics)
        assert "frontend" in joined
        assert "eval(1)" not in joined
        assert entry not in joined
    else:
        raise AssertionError("eval entry accepted")
    assert counters == {key: 0 for key in counters}, "invalid produced I/O"
    for root in BLOCKED_DB_ROOTS:
        assert root not in sys.modules, "db module loaded: " + root

print("FRONTEND_MANIFEST_FACET_SAFE_INTEGRATION_OK")
'''


class TestFrontendManifestFacetFreshProcess(unittest.TestCase):
    def _run_order(self, order):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp:
            canary_name = "canary_manifest_facet_probe"
            canary_path = Path(tmp) / (canary_name + ".py")
            canary_path.write_text(
                'import builtins\nimport sys\nsys._fmf_guard_canary_entered = True\nbuiltins.open(__file__, "rb")\n',
                encoding="utf-8",
            )
            probe = str(Path(tmp) / "frontend_manifest_facet_guard_probe.txt")
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", WORKER, str(SRC_PATH), probe, tmp, canary_name, order],
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

    def test_manifest_first_then_fcd(self):
        self._run_order("manifest-first")

    def test_fcd_first_then_manifest(self):
        self._run_order("fcd-first")


if __name__ == "__main__":
    unittest.main()
