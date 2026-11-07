"""Construction d'objets Cython de confiance, séparée du runtime PA.

Les déclarations de catalogue ne prouvent pas leur comportement. La fermeture
des dépendances, la reproductibilité et les recettes restent à qualifier.
L'exécuteur possède ses groupes de processus ; ce n'est pas un bac à sable.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import signal
import struct
import subprocess
import tempfile
import time

from .build_profile import Operation, ProfileError, parse_profile
from .generator import (ObjectRecord, _bytes, _check_hash, _checked_records,
                        _check_private_roles, _check_intent_composition, _check_admin_composition,
                        _check_observation_composition, _check_preconditions_composition,
                        _check_bootstrap_context_composition, _check_bootstrap_nv_profile_composition,
                        _check_bootstrap_init_profile_composition, _check_bootstrap_base_composition,
                        _check_bootstrap_resource_profile_composition,
                        _check_bootstrap_policy_profile_composition,
                        _check_bootstrap_prepublication_composition,
                        _check_bootstrap_recipe_composition,
                        _check_bootstrap_plan_composition,
                        _check_bootstrap_initial_record_composition,
                        _check_bootstrap_history_composition,
                        _check_bootstrap_provenance_composition,
                        _check_bootstrap_publication_composition,
                        _check_withdrawal_plan_composition,
                        _check_withdrawal_confirmation_composition,
                        _check_withdrawal_proofs_composition,
                        _check_withdrawal_intent_composition)

__all__ = ["ModuleSource", "PinnedTool", "Toolchain", "compile_objects"]
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
_HASH = re.compile(r"[0-9a-f]{64}")
_PYTHON_PROBE = """import json,platform,sys,sysconfig
r=platform.freedesktop_os_release()
print(json.dumps(dict(version=list(sys.version_info),
gil=sysconfig.get_config_var('Py_GIL_DISABLED'),
shared=sysconfig.get_config_var('Py_ENABLE_SHARED'),
soabi=sysconfig.get_config_var('SOABI'),platform=sys.platform,
machine=platform.machine(),os=r.get('ID'),release=r.get('VERSION_ID'),
include=sysconfig.get_path('include'))))
"""
_CYTHON_PROBE = "import json,Cython;print(json.dumps(dict(version=Cython.__version__)))"

_PRIVATE_NO_API_SOURCES = frozenset({
    "src/pixs/pa_native/nv_secret.pyx",
    "src/pixs/pa_native/nv_anchor.pyx",
    "src/pixs/pa_native/nv_journal.pyx",
    "src/pixs/pa_native/nv_intent.pyx",
    "src/pixs/pa_native/systemd_observation.pyx",
})


@dataclass(frozen=True, slots=True)
class ModuleSource:
    module_name: str
    source: str
    source_sha256: str
    executables: tuple[str, ...]
    operations: tuple[Operation, ...]
    generated_headers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PinnedTool:
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class Toolchain:
    python: PinnedTool
    cython_python: PinnedTool
    compiler: PinnedTool
    include_dirs: tuple[str, ...]


def _fail(code: str) -> ProfileError:
    return ProfileError(code)


def _positive(value: object) -> int:
    if type(value) is not int or not 1 <= value <= 2147483647:
        raise _fail("PA01_BUILD_BUDGET_INVALID")
    return value


def _text(value: object) -> str:
    if type(value) is not str or not value or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise _fail("PA01_BUILD_PATH_INVALID")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise _fail("PA01_BUILD_PATH_INVALID") from error
    return value


def _public_path(value: object) -> Path:
    value = _text(value)
    path = PurePosixPath(value)
    if not path.is_absolute() or str(path) != value or "\\" in value or value.startswith("//"):
        raise _fail("PA01_BUILD_TOOL_PATH_INVALID")
    forbidden = {".git", ".cache", ".opencode", ".venv", "venv", "env",
                 "credentials.json", "credentials.yaml", "secrets.json", "secrets.yaml",
                 "id_rsa", "id_ed25519", ".python-version"}
    suffixes = (".crt", ".cer", ".der", ".key", ".pem", ".p12", ".pfx", ".env")
    if any(part in forbidden or part in (".", "..") or ".env." in part
           or part.endswith(suffixes) for part in path.parts):
        raise _fail("PA01_BUILD_EXCLUDED_TOOL_PATH")
    return Path(value)


def _tool(item: object) -> Path:
    if type(item) is not PinnedTool or type(item.sha256) is not str or not _HASH.fullmatch(item.sha256):
        raise _fail("PA01_BUILD_TOOL_PIN_INVALID")
    original = _public_path(item.path)
    try:
        actual = original.resolve(strict=True)
        _public_path(str(actual))
        if not actual.is_file() or not os.access(original, os.X_OK):
            raise _fail("PA01_BUILD_TOOL_UNAVAILABLE")
        _check_hash(actual.read_bytes(), item.sha256)
    except OSError as error:
        raise _fail("PA01_BUILD_TOOL_UNAVAILABLE") from error
    return original


def _check_generated_headers(module_name: str, source: str, generated: object) -> tuple[str, ...]:
    if type(generated) is not tuple:
        raise _fail("PA01_BUILD_HEADERS_INVALID")
    seen = set()
    for name in generated:
        if type(name) is not str:
            raise _fail("PA01_BUILD_HEADERS_INVALID")
        if name in seen:
            raise _fail("PA01_BUILD_HEADERS_INVALID")
        seen.add(name)
        if name != module_name + ".h" and name != module_name + "_api.h":
            raise _fail("PA01_BUILD_HEADERS_INVALID")
        if "/" in name or "\\" in name or name in (".", ".."):
            raise _fail("PA01_BUILD_HEADERS_INVALID")
        if source in _PRIVATE_NO_API_SOURCES and name.endswith("_api.h"):
            raise _fail("PA01_BUILD_PRIVATE_API_HEADER_FORBIDDEN")
    if tuple(sorted(generated)) != generated:
        raise _fail("PA01_BUILD_HEADERS_INVALID")
    return generated


def _sources(profile, sources: object, root: Path) -> None:
    if type(sources) is not tuple or not sources:
        raise _fail("PA01_BUILD_SOURCES_REQUIRED")
    roles = {role.name: role for role in profile.executables}
    expected = {operation.name: operation for operation in profile.operations}
    modules, paths, delivered, entries = set(), set(), {}, set()
    header_owner: dict[str, str] = {}
    for item in sources:
        if type(item) is not ModuleSource:
            raise _fail("PA01_BUILD_SOURCE_TYPE_INVALID")
        if type(item.module_name) is not str or not _NAME.fullmatch(item.module_name) or item.module_name in modules:
            raise _fail("PA01_BUILD_MODULE_INVALID")
        _text(item.source)
        if item.source in paths:
            raise _fail("PA01_BUILD_SOURCE_DUPLICATE")
        if (type(item.executables) is not tuple or not item.executables
                or any(type(role) is not str or role not in roles for role in item.executables)
                or len(set(item.executables)) != len(item.executables)
                or type(item.operations) is not tuple):
            raise _fail("PA01_BUILD_ROLES_INVALID")
        _check_private_roles(item.source, item.executables)
        generated = _check_generated_headers(item.module_name, item.source,
                                             getattr(item, "generated_headers", ()))
        for header in generated:
            if header in header_owner:
                raise _fail("PA01_BUILD_HEADER_COLLISION")
            header_owner[header] = item.module_name
        local = {}
        for operation in item.operations:
            if (type(operation) is not Operation or type(operation.name) is not str
                    or operation.name in delivered or expected.get(operation.name) != operation
                    or operation.source != item.source
                    or any(operation.mode not in roles[role].modes for role in item.executables)):
                raise _fail("PA01_BUILD_OPERATION_INVALID")
            local[operation.name] = operation
            delivered[operation.name] = operation
        if local != {name: op for name, op in expected.items() if op.source == item.source}:
            raise _fail("PA01_BUILD_SOURCE_CATALOGUE_INVALID")
        for role in item.executables:
            if roles[role].source == item.source:
                entries.add(role)
        _check_hash(_bytes(root, item.source, source=True), item.source_sha256)
        modules.add(item.module_name)
        paths.add(item.source)
    if delivered != expected or entries != set(roles):
        raise _fail("PA01_BUILD_COMPOSITION_INCOMPLETE")
    _check_intent_composition(sources)
    _check_admin_composition(sources)
    _check_observation_composition(sources)
    _check_preconditions_composition(sources)
    _check_bootstrap_context_composition(sources)
    _check_bootstrap_nv_profile_composition(sources)
    _check_bootstrap_init_profile_composition(sources)
    _check_bootstrap_base_composition(sources)
    _check_bootstrap_resource_profile_composition(sources)
    _check_bootstrap_policy_profile_composition(sources)
    _check_bootstrap_prepublication_composition(sources)
    _check_bootstrap_recipe_composition(sources)
    _check_bootstrap_plan_composition(sources)
    _check_bootstrap_initial_record_composition(sources)
    _check_bootstrap_history_composition(sources)
    _check_bootstrap_provenance_composition(sources)
    _check_bootstrap_publication_composition(sources)
    _check_withdrawal_plan_composition(sources)
    _check_withdrawal_confirmation_composition(sources)
    _check_withdrawal_proofs_composition(sources)
    _check_withdrawal_intent_composition(sources)


def _output(root: Path, relative: object) -> Path:
    relative = _text(relative)
    parts = relative.split("/")
    if (len(parts) != 4 or parts[:3] != ["output", "native", "pa01"]
            or not _ID.fullmatch(parts[3]) or parts[3] in (".", "..")):
        raise _fail("PA01_BUILD_OUTPUT_INVALID")
    current = root
    for part in parts:
        current /= part
        if current.is_symlink():
            raise _fail("PA01_BUILD_OUTPUT_SYMLINK")
    if current.exists():
        raise _fail("PA01_BUILD_OUTPUT_EXISTS")
    return current


def _inventory_headers(directory: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    try:
        children = list(directory.iterdir())
    except OSError as error:
        raise _fail("PA01_BUILD_HEADER_INVENTORY_FAILED") from error
    for child in children:
        if child.suffix != ".h" or child.name in (".", ".."):
            continue
        if "/" in child.name or "\\" in child.name:
            raise _fail("PA01_BUILD_HEADERS_INVALID")
        if child.name in found:
            raise _fail("PA01_BUILD_HEADER_COLLISION")
        found[child.name] = child
    return found


def _pin_header_file(path: Path) -> tuple[str, int]:
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_nlink != 1:
            raise _fail("PA01_BUILD_HEADER_SYMLINK")
        data = path.read_bytes()
    except OSError as error:
        raise _fail("PA01_BUILD_HEADER_UNAVAILABLE") from error
    if not data:
        raise _fail("PA01_BUILD_HEADER_EMPTY")
    return (hashlib.sha256(data).hexdigest(), len(data))


def _group_exists(pid: int) -> bool:
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return False
    return True


def _cleanup(process, budget: int) -> None:
    # Le leader n'a pas été réabsorbé : son PID identifie encore notre groupe.
    deadline = time.monotonic() + budget
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        if process.returncode is None:
            process.wait(timeout=max(0.0, deadline - time.monotonic()))
    else:
        process.wait(timeout=max(0.0, deadline - time.monotonic()))
    while _group_exists(process.pid):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _fail("PA01_BUILD_QUIESCENCE_UNPROVEN")
        time.sleep(min(0.01, remaining))


def _run(argv, root, environment, deadline, log_limit, cleanup_budget, journal, persist):
    receipt = {"argv": list(argv), "state": "STARTING", "exit": None,
               "stdout_b64": "", "stderr_b64": ""}
    journal.append(receipt)
    persist()
    if time.monotonic() >= deadline:
        receipt["state"] = "FAILED"
        raise _fail("PA01_BUILD_TIMEOUT")
    try:
        process = subprocess.Popen(
            argv, cwd=root, env=environment, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False, start_new_session=True)
    except OSError as error:
        receipt["state"] = "FAILED"
        raise _fail("PA01_BUILD_SPAWN_FAILED") from error
    receipt.update(state="RUNNING", pid=process.pid)
    buffers = {"stdout_b64": bytearray(), "stderr_b64": bytearray()}
    failure = None
    cleanup_error = None
    try:
        persist()
        with selectors.DefaultSelector() as selector:
            for stream, name in ((process.stdout, "stdout_b64"), (process.stderr, "stderr_b64")):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, name)
            exited = None
            while selector.get_map() or exited is None:
                # WNOWAIT observe la fin sans libérer le PID avant le nettoyage.
                exited = os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise _fail("PA01_BUILD_TIMEOUT")
                for key, _ in selector.select(min(remaining, 0.05)):
                    try:
                        chunk = os.read(key.fd, min(65536, log_limit + 1))
                    except BlockingIOError:
                        continue
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    if sum(map(len, buffers.values())) + len(chunk) > log_limit:
                        raise _fail("PA01_BUILD_LOG_LIMIT")
                    buffers[key.data].extend(chunk)
            if time.monotonic() > deadline:
                raise _fail("PA01_BUILD_TIMEOUT")
    except BaseException as error:
        failure = error
    finally:
        try:
            _cleanup(process, cleanup_budget)
        except BaseException as error:
            cleanup_error = error
        finally:
            process.stdout.close()
            process.stderr.close()
            receipt["exit"] = process.returncode
            receipt["log_bytes"] = sum(map(len, buffers.values()))
            for name, data in buffers.items():
                receipt[name] = base64.b64encode(data).decode("ascii")
            receipt["state"] = "IN_DOUBT" if cleanup_error else (
                "FAILED" if failure or process.returncode else "COMPLETED")
    if cleanup_error:
        causes = [cleanup_error] if failure is None else [failure, cleanup_error]
        raise BaseExceptionGroup("PA01_BUILD_QUIESCENCE_UNPROVEN", causes)
    if failure:
        raise failure
    if process.returncode:
        raise _fail("PA01_BUILD_COMMAND_FAILED")
    return receipt


def _stdout(receipt):
    try:
        return base64.b64decode(receipt["stdout_b64"], validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as error:
        raise _fail("PA01_BUILD_TOOL_OUTPUT_INVALID") from error


def _write_report(directory, report):
    fd, temporary = tempfile.mkstemp(prefix="build-report-", suffix=".json", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, directory / "build-report.json")
        descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except BaseException:
        # Le fichier temporaire conservé permet une inspection après échec.
        raise


def compile_objects(profile_text: str, sources: tuple[ModuleSource, ...],
                    toolchain: Toolchain, *, source_root: Path, output_relative: str,
                    source_date_epoch: int, timeout_seconds: int,
                    cleanup_timeout_seconds: int, max_log_bytes: int) -> tuple[ObjectRecord, ...]:
    """Construit des objets, sans lier, charger ni exécuter un runtime PA.

    L'appelant protège les sources et outils pendant la construction.
    Le rapport et les commandes restent des preuves à examiner, pas une
    autorisation ni une qualification automatique.
    """
    begun = time.monotonic()
    profile = parse_profile(profile_text)
    if not isinstance(source_root, Path) or not source_root.is_absolute():
        raise _fail("PA01_BUILD_ROOT_INVALID")
    if type(toolchain) is not Toolchain:
        raise _fail("PA01_BUILD_TOOLCHAIN_INVALID")
    timeout = _positive(timeout_seconds)
    cleanup = _positive(cleanup_timeout_seconds)
    log_limit = _positive(max_log_bytes)
    if type(source_date_epoch) is not int or source_date_epoch < 0:
        raise _fail("PA01_BUILD_EPOCH_INVALID")
    try:
        epoch = str(source_date_epoch)
        root = source_root.resolve(strict=True)
    except (ValueError, OSError) as error:
        raise _fail("PA01_BUILD_INPUT_INVALID") from error
    if not root.is_dir():
        raise _fail("PA01_BUILD_ROOT_INVALID")
    output = _output(root, output_relative)
    _sources(profile, sources, root)
    pins = {"python": toolchain.python, "cython_python": toolchain.cython_python,
            "compiler": toolchain.compiler}
    tools = {name: _tool(pin) for name, pin in pins.items()}
    if type(toolchain.include_dirs) is not tuple or not toolchain.include_dirs:
        raise _fail("PA01_BUILD_INCLUDE_REQUIRED")
    includes = []
    for name in toolchain.include_dirs:
        try:
            directory = _public_path(name).resolve(strict=True)
        except OSError as error:
            raise _fail("PA01_BUILD_INCLUDE_INVALID") from error
        if not directory.is_dir():
            raise _fail("PA01_BUILD_INCLUDE_INVALID")
        includes.append(str(directory))
    if len(set(includes)) != len(includes):
        raise _fail("PA01_BUILD_INCLUDE_DUPLICATE")
    expected_headers: dict[str, str] = {}
    for item in sources:
        for header in getattr(item, "generated_headers", ()):
            expected_headers[header] = item.module_name
    environment = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "SOURCE_DATE_EPOCH": epoch}
    deadline = begun + timeout
    report = {"schema_version": "1.0.0", "profile_sha256": hashlib.sha256(profile_text.encode()).hexdigest(),
              "profile_version": profile.profile_version, "state": "PREPARING", "complete": False,
              "cython_version": {"locked": profile.cython_version, "observed": None},
              "budgets": {"timeout_seconds": timeout, "cleanup_timeout_seconds": cleanup,
                          "max_log_bytes": log_limit},
              "tools": {name: {"requested": pin.path, "resolved": str(tools[name].resolve(strict=True)), "sha256": pin.sha256}
                        for name, pin in pins.items()},
              "commands": [], "modules": [],
              "qualification": {"runtime": False, "catalogue_behavior": False,
                                "dependency_closure": False, "reproducibility": False}}
    # Toutes les entrées structurelles sont contrôlées avant ce premier effet.
    _output(root, output_relative)
    if time.monotonic() >= deadline:
        raise _fail("PA01_BUILD_TIMEOUT")
    output.mkdir(parents=True, exist_ok=False)
    records = []
    try:
        _write_report(output, report)
        temporary = output / "temporary"
        temporary.mkdir()
        environment["TMPDIR"] = str(temporary)

        def run(argv):
            remaining_log = log_limit - sum(command.get("log_bytes", 0) for command in report["commands"])
            if remaining_log <= 0:
                raise _fail("PA01_BUILD_LOG_LIMIT")
            receipt = _run(argv, root, environment, deadline, remaining_log, cleanup, report["commands"],
                           lambda: _write_report(output, report))
            _write_report(output, report)
            return receipt

        for name in ("python", "cython_python"):
            receipt = run([str(tools[name]), "-I", "-B", "-c", _PYTHON_PROBE])
            try:
                metadata = json.loads(_stdout(receipt))
            except ValueError as error:
                raise _fail("PA01_BUILD_PYTHON_METADATA_INVALID") from error
            expected = {"version": [3, 14, 9, "final", 0], "gil": 0, "shared": 0,
                        "soabi": "cpython-314-x86_64-linux-gnu", "platform": "linux",
                        "machine": "x86_64", "os": "debian", "release": "13"}
            if (type(metadata) is not dict or set(metadata) != set(expected) | {"include"}
                    or any(metadata.get(key) != value for key, value in expected.items())):
                raise _fail("PA01_BUILD_TOOLCHAIN_MISMATCH")
            if str(_public_path(metadata["include"]).resolve(strict=True)) not in includes:
                raise _fail("PA01_BUILD_PYTHON_INCLUDE_MISMATCH")
            python_header = Path(metadata["include"]) / "Python.h"
            if not python_header.is_file():
                raise _fail("PA01_BUILD_PYTHON_HEADER_UNAVAILABLE")
            report["tools"][name]["metadata"] = metadata
            report["tools"][name]["python_header_sha256"] = hashlib.sha256(python_header.read_bytes()).hexdigest()
        cython = run([str(tools["cython_python"]), "-I", "-B", "-c", _CYTHON_PROBE])
        try:
            cython_metadata = json.loads(_stdout(cython))
        except json.JSONDecodeError as error:
            raise _fail("PA01_BUILD_CYTHON_METADATA_INVALID") from error
        if (type(cython_metadata) is not dict or set(cython_metadata) != {"version"}
                or type(cython_metadata["version"]) is not str):
            raise _fail("PA01_BUILD_CYTHON_METADATA_INVALID")
        report["cython_version"]["observed"] = cython_metadata["version"]
        if cython_metadata["version"] != profile.cython_version:
            raise _fail("PA01_BUILD_CYTHON_MISMATCH")
        compiler = run([str(tools["compiler"]), "--version"])
        report["tools"]["compiler"]["version_text"] = _stdout(compiler)
        report["state"] = "COMPILING"
        _write_report(output, report)
        pinned: dict[str, tuple[str, int]] = {}
        for item in sources:
            c_file = output / (item.module_name + ".c")
            run([str(tools["cython_python"]), "-I", "-B", "-m", "cython", "-3",
                 "--module-name", item.module_name, "-o", str(c_file.relative_to(root)), item.source])
            inventory = _inventory_headers(output)
            expected_now = set(pinned) | set(item.generated_headers)
            if set(inventory) - expected_now:
                raise _fail("PA01_BUILD_HEADER_UNEXPECTED")
            if expected_now - set(inventory):
                raise _fail("PA01_BUILD_HEADER_MISSING")
            for name, path in inventory.items():
                digest, size = _pin_header_file(path)
                if name in pinned and pinned[name] != (digest, size):
                    raise _fail("PA01_BUILD_HEADER_ALTERED")
                pinned[name] = (digest, size)
        found = set(_inventory_headers(output))
        if found != set(expected_headers):
            raise _fail("PA01_BUILD_HEADER_MISSING")
        header_pins: dict[str, tuple[str, int]] = {}
        for name in found:
            header_pins[name] = _pin_header_file(output / name)
            if header_pins[name] != pinned[name]:
                raise _fail("PA01_BUILD_HEADER_ALTERED")
        build_include = str(output)
        for item in sources:
            current = _inventory_headers(output)
            if set(current) != set(expected_headers):
                raise _fail("PA01_BUILD_HEADER_MISSING")
            for name in current:
                if _pin_header_file(output / name) != header_pins[name]:
                    raise _fail("PA01_BUILD_HEADER_ALTERED")
            c_file, o_file, d_file = (output / (item.module_name + suffix) for suffix in (".c", ".o", ".d"))
            feature_flags = (("-D_GNU_SOURCE=1",)
                             if item.source == "src/pixs/pa_native/systemd_observation.pyx" else ())
            run([str(tools["compiler"]), "-std=c11", "-fPIC", "-Wall", "-Wextra", "-c", *feature_flags,
                 "-I" + build_include, *("-I" + value for value in includes),
                 "-MD", "-MF", str(d_file.relative_to(root)),
                 "-ffile-prefix-map=" + str(root) + "=.",
                 "-ffile-prefix-map=" + output_relative + "=build",
                 str(c_file.relative_to(root)), "-o", str(o_file.relative_to(root))])
            _check_hash(_bytes(root, item.source, source=True), item.source_sha256)
            data = _bytes(root, str(o_file.relative_to(root)), source=False)
            if (len(data) < 64 or data[:6] != b"\x7fELF\x02\x01"
                    or struct.unpack_from("<HH", data, 16) != (1, 62)):
                raise _fail("PA01_BUILD_OBJECT_FORMAT_INVALID")
            current = _inventory_headers(output)
            if set(current) != set(expected_headers):
                raise _fail("PA01_BUILD_HEADER_MISSING")
            for name in current:
                if _pin_header_file(output / name) != header_pins[name]:
                    raise _fail("PA01_BUILD_HEADER_ALTERED")
            record = ObjectRecord(item.module_name, item.source, str(o_file.relative_to(root)),
                                  item.source_sha256, hashlib.sha256(data).hexdigest(),
                                  item.executables, item.operations)
            records.append(record)
            headers = []
            for header in getattr(item, "generated_headers", ()):
                digest, size = header_pins[header]
                headers.append({"path": header, "sha256": digest, "size": size})
            report["modules"].append({
                "module": item.module_name, "source": item.source, "source_sha256": item.source_sha256,
                "object": record.object_path, "object_sha256": record.object_sha256,
                "c_sha256": hashlib.sha256(c_file.read_bytes()).hexdigest(),
                "depfile_sha256": hashlib.sha256(d_file.read_bytes()).hexdigest(),
                "generated_headers": headers})
            _write_report(output, report)
        _checked_records(profile, tuple(records), root, root)
        for pin in pins.values():
            _tool(pin)
        final = _inventory_headers(output)
        if set(final) != set(expected_headers):
            raise _fail("PA01_BUILD_HEADER_MISSING")
        for name in final:
            if _pin_header_file(output / name) != header_pins[name]:
                raise _fail("PA01_BUILD_HEADER_ALTERED")
        if time.monotonic() > deadline:
            raise _fail("PA01_BUILD_TIMEOUT")
        report.update(state="OBJECTS_BUILT_UNQUALIFIED", complete=True)
        _write_report(output, report)
        return tuple(records)
    except BaseException as initial:
        report.update(state="IN_DOUBT" if any(command["state"] == "IN_DOUBT"
                      for command in report["commands"]) else "FAILED", complete=False)
        try:
            _write_report(output, report)
        except BaseException as report_error:
            raise BaseExceptionGroup("PA01_BUILD_AND_REPORT_FAILED", [initial, report_error])
        raise
