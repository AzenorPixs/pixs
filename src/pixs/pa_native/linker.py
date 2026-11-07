"""Liaison native PA01 depuis des objets tracés, sans qualification du runtime.

Le rapport builder est une trace locale protégée par l'appelant, pas une
signature ou une autorité. Les programmes ne sont jamais exécutés ici.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import tempfile
import time

from . import builder
from .build_profile import ProfileError, parse_profile
from .generator import ObjectRecord, _bytes, _check_hash, _checked_records, render_program

__all__ = ["PinnedFile", "NativeLibrary", "LinkToolchain", "ProgramRecord", "link_programs"]
_HASH = re.compile(r"[0-9a-f]{64}")
_SYSTEM_FLAGS = {"-ldl", "-lm", "-lpthread", "-lutil", "-lrt", "-lc", "-pthread"}
_SYSTEM_SONAMES = {"libc.so.6", "libm.so.6", "libdl.so.2", "libpthread.so.0",
                   "libutil.so.1", "librt.so.1", "ld-linux-x86-64.so.2"}
_NATIVE_SONAMES = frozenset({
    "libssl.so.3", "libcrypto.so.3", "libpq.so.5",
    "libtss2-esys.so.0", "libtss2-mu.so.0", "libtss2-sys.so.1",
    "libtss2-tctildr.so.0", "libtss2-rc.so.0",
    "libtss2-tcti-device.so.0", "libtss2-tcti-tabrmd.so.0",
    "libdbus-1.so.3", "libsystemd.so.0",
})
_PYTHON_EXPECTED = {
    "version": [3, 14, 9, "final", 0], "gil": 0, "shared": 0,
    "soabi": "cpython-314-x86_64-linux-gnu", "platform": "linux",
    "machine": "x86_64", "os": "debian", "release": "13",
}
_LINK_PROBE = """import json,platform,sys,sysconfig
r=platform.freedesktop_os_release()
print(json.dumps(dict(version=list(sys.version_info),
gil=sysconfig.get_config_var('Py_GIL_DISABLED'),
shared=sysconfig.get_config_var('Py_ENABLE_SHARED'),
soabi=sysconfig.get_config_var('SOABI'),platform=sys.platform,
machine=platform.machine(),os=r.get('ID'),release=r.get('VERSION_ID'),
include=sysconfig.get_path('include'),libdir=sysconfig.get_config_var('LIBDIR'),
library=sysconfig.get_config_var('LIBRARY'),libs=sysconfig.get_config_var('LIBS'),
syslibs=sysconfig.get_config_var('SYSLIBS'))))
"""
_PRIVATE_NO_API_SOURCES = frozenset({
    "src/pixs/pa_native/nv_secret.pyx",
    "src/pixs/pa_native/nv_anchor.pyx",
    "src/pixs/pa_native/nv_journal.pyx",
    "src/pixs/pa_native/nv_intent.pyx",
    "src/pixs/pa_native/systemd_observation.pyx",
})


@dataclass(frozen=True, slots=True)
class PinnedFile:
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class NativeLibrary:
    file: PinnedFile
    soname: str


@dataclass(frozen=True, slots=True)
class LinkToolchain:
    python: builder.PinnedTool
    compiler: builder.PinnedTool
    reader: builder.PinnedTool
    static_python: PinnedFile
    include_dirs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProgramRecord:
    role: str
    program_path: str
    program_sha256: str
    objects: tuple[ObjectRecord, ...]


def _fail(code: str) -> ProfileError:
    return ProfileError(code)


def _asset(pin: object) -> Path:
    if type(pin) is not PinnedFile or type(pin.sha256) is not str or not _HASH.fullmatch(pin.sha256):
        raise _fail("PA01_LINK_FILE_PIN_INVALID")
    try:
        requested = builder._public_path(pin.path)
        actual = requested.resolve(strict=True)
        builder._public_path(str(actual))
        if not actual.is_file():
            raise _fail("PA01_LINK_FILE_UNAVAILABLE")
        _check_hash(actual.read_bytes(), pin.sha256)
        return actual
    except OSError as error:
        raise _fail("PA01_LINK_FILE_UNAVAILABLE") from error


def _local(root: Path, relative: str) -> bytes:
    builder._text(relative)
    parts = relative.split("/")
    if relative.startswith("/") or "\\" in relative or any(p in ("", ".", "..") for p in parts):
        raise _fail("PA01_LINK_LOCAL_PATH_INVALID")
    current = root
    try:
        for part in parts:
            current /= part
            if current.is_symlink():
                raise _fail("PA01_LINK_LOCAL_SYMLINK")
        if not current.resolve(strict=True).is_relative_to(root) or not current.is_file():
            raise _fail("PA01_LINK_LOCAL_PATH_INVALID")
        return current.read_bytes()
    except OSError as error:
        raise _fail("PA01_LINK_LOCAL_UNAVAILABLE") from error


def _flags(value: object) -> tuple[str, ...]:
    if type(value) is not str or any(ord(c) < 32 and c not in "\t\n\r" for c in value):
        raise _fail("PA01_LINK_FLAGS_INVALID")
    tokens = tuple(value.split())
    if any(token not in _SYSTEM_FLAGS for token in tokens):
        raise _fail("PA01_LINK_FLAGS_INVALID")
    return tokens


def _check_builder_headers(root: Path, base: str, modules: object) -> dict[str, tuple[str, int]]:
    if type(modules) is not list:
        raise _fail("PA01_LINK_TRACE_MODULES_INVALID")
    if type(base) is not str:
        raise _fail("PA01_LINK_HEADERS_DIR_INVALID")
    parts = base.split("/")
    if (len(parts) != 4 or parts[:3] != ["output", "native", "pa01"]
            or not builder._ID.fullmatch(parts[3]) or parts[3] in (".", "..")):
        raise _fail("PA01_LINK_HEADERS_DIR_INVALID")
    try:
        build_dir = root
        for part in parts:
            build_dir /= part
            if build_dir.is_symlink():
                raise _fail("PA01_LINK_HEADERS_DIR_INVALID")
        if not build_dir.is_dir():
            raise _fail("PA01_LINK_HEADERS_DIR_INVALID")
        children = list(build_dir.iterdir())
    except OSError as error:
        raise _fail("PA01_LINK_HEADERS_UNAVAILABLE") from error
    found: dict[str, Path] = {}
    for child in children:
        if child.suffix != ".h":
            continue
        if child.name in found:
            raise _fail("PA01_LINK_HEADER_COLLISION")
        found[child.name] = child
    declared: dict[str, tuple[str, int]] = {}
    for item in modules:
        if type(item) is not dict or type(item.get("module")) is not str:
            raise _fail("PA01_LINK_TRACE_MODULES_INVALID")
        module = item["module"]
        source = item.get("source")
        raw = item.get("generated_headers", [])
        if type(raw) is not list:
            raise _fail("PA01_LINK_HEADERS_INVALID")
        for entry in raw:
            if type(entry) is not dict or set(entry) != {"path", "sha256", "size"}:
                raise _fail("PA01_LINK_HEADERS_INVALID")
            path, digest, size = entry.get("path"), entry.get("sha256"), entry.get("size")
            if type(path) is not str or path != module + ".h" and path != module + "_api.h":
                raise _fail("PA01_LINK_HEADERS_INVALID")
            if "/" in path or "\\" in path or path in (".", ".."):
                raise _fail("PA01_LINK_HEADERS_INVALID")
            if type(digest) is not str or not _HASH.fullmatch(digest):
                raise _fail("PA01_LINK_HEADERS_INVALID")
            if type(size) is not int or size <= 0:
                raise _fail("PA01_LINK_HEADERS_INVALID")
            if path in declared:
                raise _fail("PA01_LINK_HEADER_COLLISION")
            if type(source) is str and source in _PRIVATE_NO_API_SOURCES and path.endswith("_api.h"):
                raise _fail("PA01_LINK_PRIVATE_API_HEADER_FORBIDDEN")
            declared[path] = (digest, size)
    for name, path in found.items():
        if name not in declared:
            raise _fail("PA01_LINK_HEADER_FOREIGN")
        try:
            if path.is_symlink() or not path.is_file() or path.stat().st_nlink != 1:
                raise _fail("PA01_LINK_HEADER_SYMLINK")
            data = _local(root, base + "/" + name)
        except OSError as error:
            raise _fail("PA01_LINK_HEADERS_UNAVAILABLE") from error
        if not data or len(data) != declared[name][1]:
            raise _fail("PA01_LINK_HEADER_SIZE_MISMATCH")
        if hashlib.sha256(data).hexdigest() != declared[name][0]:
            raise _fail("PA01_LINK_HEADER_MISMATCH")
    if set(found) != set(declared):
        raise _fail("PA01_LINK_HEADER_MISSING")
    return declared


def _trace(profile_text, objects, report_bytes, python_pin, compiler_pin, root, report_relative):
    try:
        report = json.loads(report_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise _fail("PA01_LINK_TRACE_INVALID") from error
    if (type(report) is not dict or report.get("schema_version") != "1.0.0"
            or report.get("state") != "OBJECTS_BUILT_UNQUALIFIED" or report.get("complete") is not True
            or report.get("profile_sha256") != hashlib.sha256(profile_text.encode("utf-8")).hexdigest()):
        raise _fail("PA01_LINK_TRACE_INVALID")
    commands, modules, tools = (report.get(k) for k in ("commands", "modules", "tools"))
    if (type(commands) is not list or not commands
            or any(type(c) is not dict or c.get("state") != "COMPLETED"
                   or type(c.get("exit")) is not int or c["exit"] != 0
                   or type(c.get("argv")) is not list for c in commands)):
        raise _fail("PA01_LINK_TRACE_COMMANDS_INVALID")
    if type(tools) is not dict:
        raise _fail("PA01_LINK_TRACE_TOOLS_INVALID")
    for name, pin in (("python", python_pin), ("compiler", compiler_pin)):
        if type(tools.get(name)) is not dict or tools[name].get("sha256") != pin.sha256:
            raise _fail("PA01_LINK_TRACE_TOOL_MISMATCH")
    for name in ("python", "cython_python"):
        item = tools.get(name)
        metadata = item.get("metadata") if type(item) is dict else None
        if (type(metadata) is not dict or any(metadata.get(k) != v for k, v in _PYTHON_EXPECTED.items())
                or type(item.get("sha256")) is not str or not _HASH.fullmatch(item["sha256"])):
            raise _fail("PA01_LINK_TRACE_PYTHON_INVALID")
    if type(modules) is not list or len(modules) != len(objects):
        raise _fail("PA01_LINK_TRACE_MODULES_INVALID")
    base = str(Path(report_relative).parent)
    by_name = {}
    for item in modules:
        if type(item) is not dict or type(item.get("module")) is not str or item["module"] in by_name:
            raise _fail("PA01_LINK_TRACE_MODULES_INVALID")
        by_name[item["module"]] = item
    for record in objects:
        item = by_name.get(record.module_name)
        if (item is None or item.get("source") != record.source
                or item.get("source_sha256") != record.source_sha256
                or item.get("object") != record.object_path
                or item.get("object_sha256") != record.object_sha256
                or record.object_path != base + "/" + record.module_name + ".o"):
            raise _fail("PA01_LINK_TRACE_OBJECT_MISMATCH")
        c_path, d_path = (base + "/" + record.module_name + suffix for suffix in (".c", ".d"))
        _check_hash(_local(root, c_path), item.get("c_sha256"))
        _check_hash(_local(root, d_path), item.get("depfile_sha256"))
        if not any(c["argv"] and c["argv"][0] == tools["compiler"]["requested"]
                   and "-c" in c["argv"] and c_path in c["argv"]
                   and "-o" in c["argv"] and record.object_path in c["argv"] for c in commands):
            raise _fail("PA01_LINK_TRACE_COMPILE_MISSING")
        if not any(c["argv"] and c["argv"][0] == tools["cython_python"]["requested"]
                   and "--module-name" in c["argv"] and record.module_name in c["argv"]
                   and c_path in c["argv"] and record.source in c["argv"] for c in commands):
            raise _fail("PA01_LINK_TRACE_CYTHON_MISSING")
    _check_builder_headers(root, base, modules)
    return report


def _persist(directory: Path, report: dict) -> None:
    fd, temporary = tempfile.mkstemp(prefix="link-report-", suffix=".json", dir=directory)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, directory / "link-report.json")
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _elf(data: bytes, permitted: tuple[int, ...]) -> None:
    if (len(data) < 64 or data[:6] != b"\x7fELF\x02\x01"
            or struct.unpack_from("<HH", data, 16)[0] not in permitted
            or struct.unpack_from("<HH", data, 16)[1] != 62):
        raise _fail("PA01_LINK_ELF_INVALID")


def link_programs(profile_text: str, objects: tuple[ObjectRecord, ...],
                  toolchain: LinkToolchain, native_libraries: dict[str, tuple[NativeLibrary, ...]], *,
                  builder_report_relative: str, builder_report_sha256: str,
                  launcher_c_sha256: str, launcher_h_sha256: str,
                  source_root: Path, output_relative: str, source_date_epoch: int,
                  timeout_seconds: int, cleanup_timeout_seconds: int,
                  max_log_bytes: int) -> tuple[ProgramRecord, ...]:
    """Lie quatre programmes, sans les exécuter ni distribuer leur runtime.

    L'appelant protège sources, rapports et outils contre les modifications
    pendant le build. Aucun argument n'est un paramètre d'une requête PA.
    """
    started = time.monotonic()
    profile = parse_profile(profile_text)
    if not isinstance(source_root, Path) or not source_root.is_absolute():
        raise _fail("PA01_LINK_ROOT_INVALID")
    if type(toolchain) is not LinkToolchain:
        raise _fail("PA01_LINK_TOOLCHAIN_INVALID")
    timeout = builder._positive(timeout_seconds)
    cleanup = builder._positive(cleanup_timeout_seconds)
    log_limit = builder._positive(max_log_bytes)
    if type(source_date_epoch) is not int or source_date_epoch < 0:
        raise _fail("PA01_LINK_EPOCH_INVALID")
    root = source_root.resolve(strict=True)
    if not root.is_dir():
        raise _fail("PA01_LINK_ROOT_INVALID")
    output = builder._output(root, output_relative)
    _checked_records(profile, objects, root, root)
    roles = {e.name: e for e in profile.executables}
    generated, selected = {}, {}
    for role, entry in roles.items():
        candidates = [o for o in objects if o.source == entry.source and role in o.executables]
        if len(candidates) != 1:
            raise _fail("PA01_LINK_ENTRY_INVALID")
        generated[role] = render_program(profile, role, candidates[0].module_name, objects,
                                         source_root=root, object_root=root)
        selected[role] = tuple(sorted((o for o in objects if role in o.executables),
                                      key=lambda o: o.module_name))
    builder._text(builder_report_relative)
    parts = builder_report_relative.split("/")
    if (len(parts) != 5 or parts[:3] != ["output", "native", "pa01"]
            or not builder._ID.fullmatch(parts[3]) or parts[3] in (".", "..")
            or parts[4] != "build-report.json"):
        raise _fail("PA01_LINK_TRACE_PATH_INVALID")
    trace_bytes = _local(root, builder_report_relative)
    _check_hash(trace_bytes, builder_report_sha256)
    tools = {name: builder._tool(getattr(toolchain, name)) for name in ("python", "compiler", "reader")}
    trace = _trace(profile_text, objects, trace_bytes, toolchain.python, toolchain.compiler,
                   root, builder_report_relative)
    builder_base = str(Path(builder_report_relative).parent)
    header_pins = _check_builder_headers(root, builder_base, trace.get("modules"))
    if type(toolchain.include_dirs) is not tuple or not toolchain.include_dirs:
        raise _fail("PA01_LINK_INCLUDE_INVALID")
    includes = []
    for value in toolchain.include_dirs:
        path = builder._public_path(value).resolve(strict=True)
        builder._public_path(str(path))
        if not path.is_dir() or str(path) in includes:
            raise _fail("PA01_LINK_INCLUDE_INVALID")
        includes.append(str(path))
    archive = _asset(toolchain.static_python)
    if archive.name != "libpython3.14.a" or archive.read_bytes()[:8] != b"!<arch>\n":
        raise _fail("PA01_LINK_STATIC_PYTHON_INVALID")
    for name, pin in (("launcher.c", launcher_c_sha256), ("launcher.h", launcher_h_sha256)):
        _check_hash(_local(root, "native/pa01/" + name), pin)
    if type(native_libraries) is not dict or set(native_libraries) != set(roles):
        raise _fail("PA01_LINK_LIBRARIES_INVALID")
    libraries = {}
    for role, items in native_libraries.items():
        if type(items) is not tuple:
            raise _fail("PA01_LINK_LIBRARIES_INVALID")
        resolved, names, paths = [], set(), set()
        for item in items:
            if (type(item) is not NativeLibrary or type(item.soname) is not str
                    or item.soname not in _NATIVE_SONAMES or item.soname in names):
                raise _fail("PA01_LINK_LIBRARY_INVALID")
            path = _asset(item.file)
            _elf(path.read_bytes(), (3,))
            if path in paths or not any(dep[4] == item.file.sha256 for dep in profile.dependencies):
                raise _fail("PA01_LINK_LIBRARY_INVENTORY_MISMATCH")
            names.add(item.soname)
            paths.add(path)
            resolved.append((item, path))
        libraries[role] = resolved
    deadline = started + timeout
    environment = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
                   "SOURCE_DATE_EPOCH": str(source_date_epoch)}
    report = {"schema_version": "1.0.0", "profile_sha256": hashlib.sha256(profile_text.encode()).hexdigest(),
              "profile_version": profile.profile_version, "state": "PREPARING", "complete": False,
              "source_date_epoch": source_date_epoch, "builder_report": {
                  "path": builder_report_relative, "sha256": builder_report_sha256},
              "budgets": {"timeout_seconds": timeout, "cleanup_timeout_seconds": cleanup,
                          "max_log_bytes": log_limit},
              "tools": {name: {"requested": getattr(toolchain, name).path,
                               "resolved": str(path.resolve(strict=True)),
                               "sha256": getattr(toolchain, name).sha256} for name, path in tools.items()},
              "static_python": {"path": str(archive), "sha256": toolchain.static_python.sha256},
              "launcher": {"c_sha256": launcher_c_sha256, "h_sha256": launcher_h_sha256},
              "commands": [], "programs": [], "native_libraries": [],
              "qualification": {"runtime": False, "dependency_closure": False,
                                "catalogue_behavior": False, "reproducibility": False}}
    builder._output(root, output_relative)
    if time.monotonic() >= deadline:
        raise _fail("PA01_LINK_TIMEOUT")
    output.mkdir(parents=True, exist_ok=False)
    try:
        _persist(output, report)
        temporary = output / "temporary"
        temporary.mkdir()
        environment["TMPDIR"] = str(temporary)

        def run(argv):
            remaining = log_limit - sum(c.get("log_bytes", 0) for c in report["commands"])
            if remaining <= 0:
                raise _fail("PA01_LINK_LOG_LIMIT")
            receipt = builder._run(argv, root, environment, deadline, remaining, cleanup,
                                   report["commands"], lambda: _persist(output, report))
            _persist(output, report)
            return builder._stdout(receipt)

        metadata = json.loads(run([str(tools["python"]), "-I", "-B", "-c", _LINK_PROBE]))
        if (type(metadata) is not dict or set(metadata) != set(_PYTHON_EXPECTED) | {
                "include", "libdir", "library", "libs", "syslibs"}
                or any(metadata.get(k) != v for k, v in _PYTHON_EXPECTED.items())):
            raise _fail("PA01_LINK_PYTHON_MISMATCH")
        include = builder._public_path(metadata["include"]).resolve(strict=True)
        libdir = builder._public_path(metadata["libdir"]).resolve(strict=True)
        if str(include) not in includes or metadata["library"] != "libpython3.14.a" or libdir / metadata["library"] != archive:
            raise _fail("PA01_LINK_PYTHON_LAYOUT_MISMATCH")
        header = include / "Python.h"
        expected_header = trace["tools"]["python"].get("python_header_sha256")
        _check_hash(header.read_bytes(), expected_header)
        flags = _flags(metadata["libs"]) + _flags(metadata["syslibs"])
        report["python_metadata"] = metadata
        report["tools"]["compiler"]["version_text"] = run([str(tools["compiler"]), "--version"])
        report["tools"]["reader"]["version_text"] = run([str(tools["reader"]), "--version"])
        for role, items in libraries.items():
            for item, path in items:
                dynamic = run([str(tools["reader"]), "-d", str(path)])
                if re.findall(r"\(SONAME\).*\[([^\]]+)\]", dynamic) != [item.soname]:
                    raise _fail("PA01_LINK_LIBRARY_SONAME_MISMATCH")
                report["native_libraries"].append({"role": role, "path": str(path),
                    "soname": item.soname, "sha256": item.file.sha256, "dynamic": dynamic})
        report["state"] = "LINKING"
        bin_directory = output / "bin"
        bin_directory.mkdir()
        prefix = ["-ffile-prefix-map=" + str(root) + "=.",
                  "-ffile-prefix-map=" + output_relative + "=build"]
        compiler = str(tools["compiler"])
        launcher_object = output / "launcher.o"
        run([compiler, "-std=c11", "-fPIC", "-Wall", "-Wextra", "-c",
             *("-I" + value for value in includes), "-MD", "-MF",
             str((output / "launcher.d").relative_to(root)), *prefix,
             "native/pa01/launcher.c", "-o", str(launcher_object.relative_to(root))])
        records = []
        for role in sorted(roles):
            c_file, o_file, d_file = (output / (role + suffix) for suffix in (".c", ".o", ".d"))
            c_file.write_text(generated[role], encoding="utf-8", newline="\n")
            run([compiler, "-std=c11", "-fPIC", "-Wall", "-Wextra", "-c",
                 "-Inative/pa01", *("-I" + value for value in includes), "-MD", "-MF",
                 str(d_file.relative_to(root)), *prefix,
                 str(c_file.relative_to(root)), "-o", str(o_file.relative_to(root))])
            program = bin_directory / role
            run([compiler, "-Wl,--export-dynamic", "-Wl,-rpath,$ORIGIN/../lib",
                 "-o", str(program.relative_to(root)), str(o_file.relative_to(root)),
                 str(launcher_object.relative_to(root)),
                 *(o.object_path for o in selected[role]), str(archive),
                 *(str(path) for _, path in libraries[role]), *flags])
            data = program.read_bytes()
            _elf(data, (2, 3))
            dynamic = run([str(tools["reader"]), "-d", str(program.relative_to(root))])
            needed = re.findall(r"\(NEEDED\).*\[([^\]]+)\]", dynamic)
            allowed = _SYSTEM_SONAMES | {item.soname for item, _ in libraries[role]}
            paths = re.findall(r"\((?:RPATH|RUNPATH)\).*\[([^\]]+)\]", dynamic)
            if (any(name.startswith("libpython") or name not in allowed for name in needed)
                    or paths != ["$ORIGIN/../lib"]):
                raise _fail("PA01_LINK_DYNAMIC_DEPENDENCY_INVALID")
            headers = run([str(tools["reader"]), "-l", str(program.relative_to(root))])
            record = ProgramRecord(role, str(program.relative_to(root)),
                                   hashlib.sha256(data).hexdigest(), selected[role])
            records.append(record)
            report["programs"].append({"role": role, "program": record.program_path,
                "sha256": record.program_sha256,
                "objects": [{"path": o.object_path, "sha256": o.object_sha256} for o in selected[role]],
                "generated_c_sha256": hashlib.sha256(c_file.read_bytes()).hexdigest(),
                "generated_object_sha256": hashlib.sha256(o_file.read_bytes()).hexdigest(),
                "generated_depfile_sha256": hashlib.sha256(d_file.read_bytes()).hexdigest(),
                "needed": needed, "dynamic": dynamic, "program_headers": headers})
            _persist(output, report)
        _checked_records(profile, objects, root, root)
        _check_hash(_local(root, builder_report_relative), builder_report_sha256)
        for name, pin in (("launcher.c", launcher_c_sha256), ("launcher.h", launcher_h_sha256)):
            _check_hash(_local(root, "native/pa01/" + name), pin)
        _check_hash(header.read_bytes(), expected_header)
        for name in tools:
            builder._tool(getattr(toolchain, name))
        _asset(toolchain.static_python)
        for items in libraries.values():
            for item, _ in items:
                _asset(item.file)
        for record in records:
            _check_hash((root / record.program_path).read_bytes(), record.program_sha256)
        if _check_builder_headers(root, builder_base, trace.get("modules")) != header_pins:
            raise _fail("PA01_LINK_HEADER_MISMATCH")
        if time.monotonic() > deadline:
            raise _fail("PA01_LINK_TIMEOUT")
        report["launcher"].update(object_sha256=hashlib.sha256(launcher_object.read_bytes()).hexdigest(),
            depfile_sha256=hashlib.sha256((output / "launcher.d").read_bytes()).hexdigest())
        report.update(state="PROGRAMS_LINKED_UNQUALIFIED", complete=True)
        _persist(output, report)
        return tuple(records)
    except BaseException as initial:
        report.update(state="IN_DOUBT" if any(c.get("state") == "IN_DOUBT"
                      for c in report["commands"]) else "FAILED", complete=False)
        try:
            _persist(output, report)
        except BaseException as report_error:
            raise BaseExceptionGroup("PA01_LINK_AND_REPORT_FAILED", [initial, report_error])
        raise
