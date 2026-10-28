"""Assemblage du staging PA01 depuis programmes liés et assets épinglés.

Assemble uniquement des fichiers issus des traces locales du build et de la liaison.
Ne qualifie ni confiance, ni fermeture de dépendances, ni import/runtime,
ni comportement, ni reproductibilité, ni SBOM. Ne compile ni n'exécute rien.
Le rapport du linker est une trace locale protégée par l'appelant, pas une
signature ni une autorité.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
import re
import stat
from pathlib import Path

from . import builder
from .build_profile import ProfileError, parse_profile
from .generator import ObjectRecord, _check_hash, _checked_records
from .linker import PinnedFile, ProgramRecord, _elf, _NATIVE_SONAMES

__all__ = ["RuntimeAsset", "stage_bundle"]

_HASH = re.compile(r"[0-9a-f]{64}")
_LINK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
_PY_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\.py")
_PACKAGE_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_DYNLOAD_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\.cpython-314-x86_64-linux-gnu\.so")
_LIB_SONAMES = _NATIVE_SONAMES
_PROVIDER_DESTINATION = "lib/ossl-modules/tpm2.so"
_SENSITIVE_SEGMENTS = frozenset({
    ".git", ".cache", ".opencode", ".venv", "venv", "env",
    "__pycache__", "site-packages", "dist-packages",
    "secret", "secrets", "certificate", "certificates", "cert",
    "key", "keys", "token", "password", "credentials",
    "sitecustomize", "usercustomize",
})
_SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".crt", ".cer", ".der")


@dataclass(frozen=True, slots=True)
class RuntimeAsset:
    source: PinnedFile
    destination: str
    dependency_name: str


def _fail(code: str) -> ProfileError:
    return ProfileError(code)


def _destination(value: object) -> str:
    if type(value) is not str or not value:
        raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
    if (value.startswith("/") or "\\" in value or "\x00" in value
            or "//" in value or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
    parts = value.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
    lowered = [p.lower() for p in parts]
    if (any(p in _SENSITIVE_SEGMENTS for p in lowered)
            or lowered[-1] in ("sitecustomize.py", "usercustomize.py")):
        raise _fail("PA01_BUNDLE_DESTINATION_SENSITIVE")
    if any(p.endswith(_SENSITIVE_SUFFIXES) for p in lowered):
        raise _fail("PA01_BUNDLE_DESTINATION_SENSITIVE")
    if value == _PROVIDER_DESTINATION:
        return value
    if value.startswith("runtime/lib/python3.14/lib-dynload/"):
        rest = value[len("runtime/lib/python3.14/lib-dynload/"):]
        if "/" in rest or _DYNLOAD_NAME.fullmatch(rest) is None:
            raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
        return value
    if value.startswith("runtime/lib/python3.14/"):
        rest = value[len("runtime/lib/python3.14/"):]
        items = rest.split("/")
        if (_PY_NAME.fullmatch(items[-1]) is None
                or any(_PACKAGE_NAME.fullmatch(p) is None for p in items[:-1])):
            raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
        return value
    if value.startswith("lib/"):
        rest = value[len("lib/"):]
        if "/" in rest or rest not in _LIB_SONAMES:
            raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
        return value
    raise _fail("PA01_BUNDLE_DESTINATION_INVALID")


def _lstat_tree(absolute: Path, expect_file: bool) -> None:
    parts = absolute.parts
    current = Path(parts[0])
    entries = [(current, True)]
    for part in parts[1:]:
        current = current / part
        entries.append((current, False))
    for index, (path, _is_root) in enumerate(entries):
        try:
            info = os.lstat(path)
        except OSError as error:
            raise _fail("PA01_BUNDLE_FILE_UNAVAILABLE") from error
        if stat.S_ISLNK(info.st_mode):
            raise _fail("PA01_BUNDLE_SYMLINK")
        last = index == len(entries) - 1
        if not last and not stat.S_ISDIR(info.st_mode):
            raise _fail("PA01_BUNDLE_PATH_INVALID")
        if last and ((expect_file and not stat.S_ISREG(info.st_mode))
                     or (not expect_file and not stat.S_ISDIR(info.st_mode))):
            raise _fail("PA01_BUNDLE_PATH_INVALID")


def _open_bounded(absolute: Path, max_bytes: int) -> bytes:
    if type(max_bytes) is not int or isinstance(max_bytes, bool) or max_bytes < 0:
        raise _fail("PA01_BUNDLE_BUDGET_INVALID")
    _lstat_tree(absolute, True)
    fd = os.open(absolute, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
    try:
        first = os.fstat(fd)
        if not stat.S_ISREG(first.st_mode) or first.st_nlink != 1:
            raise _fail("PA01_BUNDLE_FILE_INVALID")
        size = first.st_size
        if type(size) is not int or size < 0 or size > max_bytes:
            raise _fail("PA01_BUNDLE_FILE_TOO_LARGE")
        chunks: list[bytes] = []
        remaining = size
        while remaining > 0:
            chunk = os.read(fd, min(65536, remaining))
            if not chunk:
                raise _fail("PA01_BUNDLE_FILE_CHANGED")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(fd, 1) != b"":
            raise _fail("PA01_BUNDLE_FILE_CHANGED")
        second = os.fstat(fd)
        if ((second.st_dev, second.st_ino, second.st_size,
             second.st_mtime_ns, second.st_ctime_ns)
                != (first.st_dev, first.st_ino, first.st_size,
                    first.st_mtime_ns, first.st_ctime_ns)):
            raise _fail("PA01_BUNDLE_FILE_CHANGED")
        return b"".join(chunks)
    finally:
        os.close(fd)


def _read_absolute_pin(pin: object, max_bytes: int) -> tuple[bytes, Path]:
    if type(pin) is not PinnedFile:
        raise _fail("PA01_BUNDLE_FILE_PIN_INVALID")
    if type(pin.sha256) is not str or _HASH.fullmatch(pin.sha256) is None:
        raise _fail("PA01_BUNDLE_FILE_PIN_INVALID")
    absolute = builder._public_path(pin.path)
    if not isinstance(absolute, Path) or not absolute.is_absolute():
        raise _fail("PA01_BUNDLE_FILE_PIN_INVALID")
    data = _open_bounded(absolute, max_bytes)
    _check_hash(data, pin.sha256)
    return data, absolute


def _read_relative_pinned(root: Path, relative: str, expected_sha: object, max_bytes: int) -> bytes:
    if type(relative) is not str or not relative:
        raise _fail("PA01_BUNDLE_LOCAL_PATH_INVALID")
    if relative.startswith("/") or "\\" in relative or "//" in relative:
        raise _fail("PA01_BUNDLE_LOCAL_PATH_INVALID")
    if any(p in ("", ".", "..") for p in relative.split("/")):
        raise _fail("PA01_BUNDLE_LOCAL_PATH_INVALID")
    if type(expected_sha) is not str or _HASH.fullmatch(expected_sha) is None:
        raise _fail("PA01_BUNDLE_FILE_PIN_INVALID")
    absolute = root / relative
    builder._public_path(str(absolute))
    data = _open_bounded(absolute, max_bytes)
    _check_hash(data, expected_sha)
    return data


def _check_link_report(report: object, profile_text: str, profile_version: str,
                       programs: tuple[ProgramRecord, ...], link_relative: str) -> dict:
    if type(report) is not dict:
        raise _fail("PA01_BUNDLE_TRACE_INVALID")
    if (report.get("schema_version") != "1.0.0"
            or report.get("state") != "PROGRAMS_LINKED_UNQUALIFIED"
            or report.get("complete") is not True):
        raise _fail("PA01_BUNDLE_TRACE_STATE_INVALID")
    if report.get("profile_sha256") != hashlib.sha256(profile_text.encode("utf-8")).hexdigest():
        raise _fail("PA01_BUNDLE_TRACE_PROFILE_MISMATCH")
    if report.get("profile_version") != profile_version:
        raise _fail("PA01_BUNDLE_TRACE_PROFILE_MISMATCH")
    commands = report.get("commands")
    if type(commands) is not list or not commands:
        raise _fail("PA01_BUNDLE_TRACE_COMMANDS_INVALID")
    for item in commands:
        if (type(item) is not dict or item.get("state") != "COMPLETED"
                or type(item.get("exit")) is not int or item["exit"] != 0
                or type(item.get("argv")) is not list or not item["argv"]):
            raise _fail("PA01_BUNDLE_TRACE_COMMANDS_INVALID")
    items = report.get("programs")
    if type(items) is not list or len(items) != 4:
        raise _fail("PA01_BUNDLE_TRACE_PROGRAMS_INVALID")
    link_parent = Path(link_relative).parent
    by_role = {p.role: p for p in programs}
    seen = set()
    for item in items:
        if type(item) is not dict:
            raise _fail("PA01_BUNDLE_TRACE_PROGRAMS_INVALID")
        role = item.get("role")
        if type(role) is not str or role in seen or role not in by_role:
            raise _fail("PA01_BUNDLE_TRACE_PROGRAMS_INVALID")
        seen.add(role)
        record = by_role[role]
        if item.get("program") != record.program_path or item.get("sha256") != record.program_sha256:
            raise _fail("PA01_BUNDLE_TRACE_PROGRAM_MISMATCH")
        if Path(record.program_path).parent != link_parent / "bin" or Path(record.program_path).name != role:
            raise _fail("PA01_BUNDLE_PROGRAM_DIVERTED")
        expected = [{"path": o.object_path, "sha256": o.object_sha256} for o in record.objects]
        if item.get("objects") != expected:
            raise _fail("PA01_BUNDLE_TRACE_OBJECT_MISMATCH")
    if seen != set(by_role):
        raise _fail("PA01_BUNDLE_TRACE_PROGRAMS_INVALID")
    return report


def stage_bundle(profile_text: str, programs: tuple[ProgramRecord, ...],
                 assets: tuple[RuntimeAsset, ...], *, link_report_relative: str,
                 link_report_sha256: str, source_root: Path, output_relative: str,
                 source_date_epoch: int, max_asset_bytes: int,
                 max_total_bytes: int, max_files: int) -> str:
    """Assemble un staging neuf, sans qualifier le runtime ni l'exécuter."""
    if type(profile_text) is not str or not profile_text:
        raise _fail("PA01_BUNDLE_PROFILE_INVALID")
    if type(programs) is not tuple or len(programs) != 4:
        raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
    if type(assets) is not tuple:
        raise _fail("PA01_BUNDLE_ASSETS_INVALID")
    if type(link_report_relative) is not str or type(link_report_sha256) is not str:
        raise _fail("PA01_BUNDLE_TRACE_PATH_INVALID")
    if not isinstance(source_root, Path) or not source_root.is_absolute():
        raise _fail("PA01_BUNDLE_ROOT_INVALID")
    if type(output_relative) is not str or not output_relative:
        raise _fail("PA01_BUNDLE_OUTPUT_INVALID")
    if type(source_date_epoch) is not int or isinstance(source_date_epoch, bool) or source_date_epoch < 0:
        raise _fail("PA01_BUNDLE_EPOCH_INVALID")
    asset_limit = builder._positive(max_asset_bytes)
    total_limit = builder._positive(max_total_bytes)
    files_limit = builder._positive(max_files)
    profile = parse_profile(profile_text)
    builder._public_path(str(source_root))
    _lstat_tree(source_root, False)
    root = source_root.resolve(strict=True)
    if not root.is_dir():
        raise _fail("PA01_BUNDLE_ROOT_INVALID")
    roles = {e.name: e for e in profile.executables}
    if len(roles) != 4:
        raise _fail("PA01_BUNDLE_PROFILE_INVALID")
    seen_roles: set[str] = set()
    for record in programs:
        if type(record) is not ProgramRecord:
            raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
        if (type(record.role) is not str or record.role in seen_roles
                or record.role not in roles):
            raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
        seen_roles.add(record.role)
        if type(record.program_path) is not str or type(record.program_sha256) is not str:
            raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
        if _HASH.fullmatch(record.program_sha256) is None:
            raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
        if type(record.objects) is not tuple or not record.objects:
            raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
    if seen_roles != set(roles):
        raise _fail("PA01_BUNDLE_PROGRAMS_INVALID")
    by_path: dict[str, ObjectRecord] = {}
    for record in programs:
        for item in record.objects:
            if type(item) is not ObjectRecord:
                raise _fail("PA01_BUNDLE_OBJECTS_INVALID")
            if (type(item.object_path) is not str or not item.object_path.endswith(".o")
                    or type(item.source) is not str
                    or not (item.source.startswith("src/pixs/pa_native/")
                            or item.source == "src/pixs/kernel/manifest/semver.py")
                    or Path(item.source).suffix not in (".py", ".pyx")
                    or any(p.startswith(".") or p == "__pycache__" for p in item.source.split("/"))):
                raise _fail("PA01_BUNDLE_OBJECTS_INVALID")
            known = by_path.get(item.object_path)
            if known is None:
                by_path[item.object_path] = item
            elif known != item:
                raise _fail("PA01_BUNDLE_OBJECT_INCOHERENT")
    unified = tuple(by_path[path] for path in sorted(by_path))
    for item in unified:
        _read_relative_pinned(root, item.source, item.source_sha256, asset_limit)
        _read_relative_pinned(root, item.object_path, item.object_sha256, asset_limit)
    _checked_records(profile, unified, root, root)
    for record in programs:
        entry = roles[record.role]
        candidates = [o for o in unified if o.source == entry.source and record.role in o.executables]
        if len(candidates) != 1:
            raise _fail("PA01_BUNDLE_ENTRY_INVALID")
        selected = tuple(sorted((o for o in unified if record.role in o.executables),
                                key=lambda o: o.module_name))
        if selected != record.objects:
            raise _fail("PA01_BUNDLE_OBJECTS_MISMATCH")
    parts = link_report_relative.split("/")
    if (len(parts) != 5 or parts[:3] != ["output", "native", "pa01"]
            or _LINK_ID.fullmatch(parts[3]) is None or parts[3] in (".", "..")
            or parts[4] != "link-report.json"):
        raise _fail("PA01_BUNDLE_TRACE_PATH_INVALID")
    trace_bytes = _read_relative_pinned(root, link_report_relative, link_report_sha256, total_limit)
    def _pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise _fail("PA01_BUNDLE_TRACE_DUPLICATE")
            result[key] = value
        return result

    def _constant(_value):
        raise _fail("PA01_BUNDLE_TRACE_CONSTANT")

    try:
        trace = json.loads(trace_bytes.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
    except (UnicodeDecodeError, ValueError) as error:
        raise _fail("PA01_BUNDLE_TRACE_INVALID") from error
    _check_link_report(trace, profile_text, profile.profile_version, programs, link_report_relative)
    dependencies = {name: (version, provenance, license_id, fingerprint)
                    for name, version, provenance, license_id, fingerprint in profile.dependencies}
    if 4 + len(assets) + 1 > files_limit:
        raise _fail("PA01_BUNDLE_BUDGET_EXCEEDED")
    destinations: dict[str, RuntimeAsset] = {}
    for asset in assets:
        if type(asset) is not RuntimeAsset:
            raise _fail("PA01_BUNDLE_ASSETS_INVALID")
        if type(asset.source) is not PinnedFile:
            raise _fail("PA01_BUNDLE_FILE_PIN_INVALID")
        if type(asset.dependency_name) is not str:
            raise _fail("PA01_BUNDLE_DEPENDENCY_INVALID")
        destination = _destination(asset.destination)
        if destination in destinations:
            raise _fail("PA01_BUNDLE_DESTINATION_COLLISION")
        destinations[destination] = asset
        if asset.dependency_name not in dependencies:
            raise _fail("PA01_BUNDLE_DEPENDENCY_UNKNOWN")
        version, provenance, license_id, fingerprint = dependencies[asset.dependency_name]
        if not version or not provenance or not license_id:
            raise _fail("PA01_BUNDLE_DEPENDENCY_METADATA_INVALID")
        if asset.source.sha256 != fingerprint:
            raise _fail("PA01_BUNDLE_DEPENDENCY_DIGEST_MISMATCH")
    required = {"runtime/lib/python3.14/encodings/__init__.py",
                "runtime/lib/python3.14/encodings/aliases.py",
                "runtime/lib/python3.14/encodings/utf_8.py"}
    if not required.issubset(set(destinations)):
        raise _fail("PA01_BUNDLE_RUNTIME_MINIMUM_MISSING")
    manifest_relative = output_relative + "/staging-manifest.json"
    file_paths = ["staging-manifest.json"] + ["bin/" + r for r in roles] + sorted(destinations)
    for index, first in enumerate(file_paths):
        for second in file_paths[index + 1:]:
            if first == second or second.startswith(first + "/") or first.startswith(second + "/"):
                raise _fail("PA01_BUNDLE_DESTINATION_COLLISION")
    used_bytes = 0
    program_data: dict[str, bytes] = {}
    for record in programs:
        data = _read_relative_pinned(root, record.program_path, record.program_sha256,
                                     min(asset_limit, total_limit - used_bytes))
        _elf(data, (2, 3))
        program_data[record.role] = data
        used_bytes += len(data)
    asset_data: dict[str, bytes] = {}
    for destination in sorted(destinations):
        asset = destinations[destination]
        data, _absolute = _read_absolute_pin(asset.source, min(asset_limit, total_limit - used_bytes))
        if destination.startswith("runtime/lib/python3.14/lib-dynload/") or destination.startswith("lib/"):
            _elf(data, (3,))
        elif not destination.endswith(".py"):
            raise _fail("PA01_BUNDLE_DESTINATION_INVALID")
        asset_data[destination] = data
        used_bytes += len(data)
    total_bytes = sum(len(v) for v in program_data.values()) + sum(len(v) for v in asset_data.values())
    if total_bytes > total_limit:
        raise _fail("PA01_BUNDLE_BUDGET_EXCEEDED")
    if 4 + len(asset_data) + 1 > files_limit:
        raise _fail("PA01_BUNDLE_BUDGET_EXCEEDED")
    output = builder._output(root, output_relative)
    created_dirs: list[Path] = []
    created_output = False
    report: dict = {
        "schema_version": "1.0.0",
        "state": "PREPARING",
        "complete": False,
        "profile_sha256": hashlib.sha256(profile_text.encode("utf-8")).hexdigest(),
        "profile_version": profile.profile_version,
        "source_date_epoch": source_date_epoch,
        "link_report": {"path": link_report_relative, "sha256": link_report_sha256},
        "budgets": {"max_asset_bytes": asset_limit, "max_total_bytes": total_limit,
                    "max_files": files_limit},
        "programs": [], "assets": [],
        "qualification": {"runtime": False, "dependency_closure": False,
                          "catalogue_behavior": False, "reproducibility": False,
                          "dynamic_load": False, "closure": False,
                          "trust": False, "sbom_signed": False},
    }

    def _encode_state(payload: dict) -> bytes:
        return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")

    def _sync_dir(path: Path) -> None:
        descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _persist_state(payload: dict) -> None:
        import tempfile
        descriptor, temporary = tempfile.mkstemp(prefix="staging-manifest-", suffix=".json", dir=output)
        try:
            os.fchmod(descriptor, 0o644)
            view = _encode_state(payload)
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    raise OSError("PA01_BUNDLE_SHORT_WRITE")
                view = view[written:]
            os.utime(descriptor, (source_date_epoch, source_date_epoch))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.replace(temporary, root / manifest_relative)
        _sync_dir(output)

    def _ensure_dir(relative: str) -> Path:
        path = output / relative
        path.mkdir(exist_ok=False)
        os.chmod(path, 0o755)
        created_dirs.append(path)
        return path

    def _write_tracked(relative: str, data: bytes, mode: int) -> None:
        target = root / relative
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode)
        try:
            os.fchmod(descriptor, mode)
            view = data
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    raise OSError("PA01_BUNDLE_SHORT_WRITE")
                view = view[written:]
            os.utime(descriptor, (source_date_epoch, source_date_epoch))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        _sync_dir(target.parent)

    for role in sorted(program_data):
        record = next(p for p in programs if p.role == role)
        report["programs"].append({
            "role": role, "path": output_relative + "/bin/" + role,
            "sha256": record.program_sha256, "size": len(program_data[role]),
            "mode": "0755",
            "objects": [{"path": o.object_path, "sha256": o.object_sha256}
                        for o in record.objects],
        })
    for destination in sorted(asset_data):
        asset = destinations[destination]
        version, provenance, license_id, fingerprint = dependencies[asset.dependency_name]
        report["assets"].append({
            "destination": destination, "sha256": asset.source.sha256,
            "size": len(asset_data[destination]), "mode": "0644",
            "dependency": {"name": asset.dependency_name, "version": version,
                           "provenance": provenance, "license": license_id,
                           "sha256": fingerprint},
        })
    final_report = dict(report, state="STAGED_UNQUALIFIED", complete=True)
    if used_bytes + len(_encode_state(final_report)) > total_limit:
        raise _fail("PA01_BUNDLE_BUDGET_EXCEEDED")
    directories = {"bin", "runtime", "runtime/lib", "runtime/lib/python3.14",
                   "runtime/lib/python3.14/lib-dynload", "lib"}
    for destination in destinations:
        parent = Path(destination).parent
        while str(parent) != ".":
            directories.add(parent.as_posix())
            parent = parent.parent
    try:
        output.mkdir(exist_ok=False)
        created_output = True
        os.chmod(output, 0o755)
        created_dirs.append(output)
        _persist_state(report)
        for relative in sorted(directories, key=lambda p: (p.count("/"), p)):
            _ensure_dir(relative)
        for role in sorted(program_data):
            _write_tracked(output_relative + "/bin/" + role, program_data[role], 0o755)
        for destination in sorted(asset_data):
            _write_tracked(output_relative + "/" + destination, asset_data[destination], 0o644)
        for record in programs:
            fresh = _read_relative_pinned(root, record.program_path,
                                         record.program_sha256, asset_limit)
            if fresh != program_data[record.role]:
                raise _fail("PA01_BUNDLE_FILE_CHANGED")
        for destination in sorted(destinations):
            fresh, _abs = _read_absolute_pin(destinations[destination].source, asset_limit)
            if fresh != asset_data[destination]:
                raise _fail("PA01_BUNDLE_FILE_CHANGED")
        _read_relative_pinned(root, link_report_relative, link_report_sha256, total_limit)
        for item in unified:
            _read_relative_pinned(root, item.source, item.source_sha256, asset_limit)
            _read_relative_pinned(root, item.object_path, item.object_sha256, asset_limit)
        _checked_records(profile, unified, root, root)
        for role in sorted(program_data):
            _read_relative_pinned(output, "bin/" + role,
                                  hashlib.sha256(program_data[role]).hexdigest(), asset_limit)
        for destination in sorted(asset_data):
            _read_relative_pinned(output, destination,
                                  hashlib.sha256(asset_data[destination]).hexdigest(), asset_limit)
        report.update(state="STAGED_UNQUALIFIED", complete=True)
        _persist_state(report)
        for path in sorted(created_dirs, key=lambda p: len(p.parts), reverse=True):
            os.utime(path, (source_date_epoch, source_date_epoch))
            _sync_dir(path)
        _sync_dir(output.parent)
        return manifest_relative
    except BaseException as initial:
        report.update(state="FAILED", complete=False)
        try:
            if created_output:
                _persist_state(report)
                for path in reversed(created_dirs):
                    _sync_dir(path)
                _sync_dir(output.parent)
        except BaseException as report_error:
            raise BaseExceptionGroup("PA01_BUNDLE_AND_REPORT_FAILED", [initial, report_error])
        raise
