"""C11 selection operateur epinglee + capture physique avant parse/import.

Frontiere LOCAL_OPERATOR_SELECTION. Pin hors flux. Attestations fournies
par l'appelant, jamais fabriquees. Capture n'active rien, n'execute rien.
Donnees internes build, pas export bundle. Ne publie ni plan, ni bundle,
ni etat backend. Stdlib + API publique Kernel + interne C11 autorise.
"""

from __future__ import annotations

import argparse
import base64
import codecs
import hashlib
import hmac
import json
import os
import stat
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from pixs.kernel.manifest import ManifestValidationError, parse_manifest_text
from pixs.kernel.manifest.semver import parse_version

from build_frontend_composition import (
    BuildError as _BridgeBuildError, _directory, _project_root,
)

SELECTION_SCHEMA = "pixs.frontend.selection/1.0.0"
SELECTION_KIND = "LOCAL_OPERATOR_SELECTION"
ENVIRONMENTS = ("DEVELOPMENT", "PRODUCTION")
TRUST_LEVELS = ("PLATFORM", "TRUSTED", "SANDBOXED", "DEVELOPMENT")
MANIFEST_FILENAME = "component.toml"
SOURCE_SUFFIXES = (".js", ".mjs")

_FORBIDDEN_DIRS = frozenset({
    ".git", ".opencode", ".cache", "__pycache__", ".venv", "venv",
    "env", "logs", "node_modules", "tmp", ".idea", ".mypy_cache", ".npm",
    ".pytest_cache", ".ruff_cache", ".stfolder", ".stignore", ".vscode",
    ".python-version",
})
_DENY_BASENAMES = frozenset({
    "id_rsa", "id_ed25519",
    "credentials.json", "credentials.yaml",
    "secrets.json", "secrets.yaml",
})
_DENY_SUFFIXES = (".key", ".pem", ".p12", ".pfx", ".crt", ".cer", ".der")
_ATTESTATION_FIELDS = (
    "component_id", "component_version", "scope", "target_id",
    "target_version", "suite_id", "suite_version", "verdict", "proof_ref",
)


class SelectionError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _is_hex64(value: object) -> bool:
    if type(value) is not str or len(value) != 64:
        return False
    for ch in value:
        if ch not in "0123456789abcdef":
            return False
    return True


def _no_dupes(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise SelectionError("SELECTION_JSON_INVALID")
        result[key] = value
    return result


def _reject_const(value: str) -> object:
    raise SelectionError("SELECTION_JSON_INVALID")



def _text(value: object) -> str:
    if type(value) is not str or not value or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise SelectionError("SELECTION_SCHEMA_INVALID") from error
    return value

def _parts(value: object) -> tuple[str, ...]:
    if type(value) is not str or not value:
        raise SelectionError("SELECTION_PATH_INVALID")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise SelectionError("SELECTION_PATH_INVALID") from error
    if "\\" in value or PurePosixPath(value).is_absolute() or PurePosixPath(value).as_posix() != value:
        raise SelectionError("SELECTION_PATH_INVALID")
    if any(c in value for c in ":?#%"):
        raise SelectionError("SELECTION_PATH_INVALID")
    segments = value.split("/")
    for seg in segments:
        if not seg or seg in (".", "..") or seg in _FORBIDDEN_DIRS:
            raise SelectionError("SELECTION_PATH_INVALID")
        if any(ord(c) < 32 or ord(c) == 127 for c in seg):
            raise SelectionError("SELECTION_PATH_INVALID")
    for base in segments:
        if (base in _DENY_BASENAMES or base == ".env" or base.endswith(".env")
                or ".env." in base or any(base.endswith(suffix) for suffix in _DENY_SUFFIXES)):
            raise SelectionError("SELECTION_SECRET_REFUSED")
    if segments[0] == "openspec" and len(segments) > 1 and segments[1] in {
        ".generated", ".history", ".output", ".tmp", "build", "dist",
    }:
        raise SelectionError("SELECTION_PATH_INVALID")
    return tuple(segments)


@dataclass(frozen=True, slots=True)
class SelectionLimits:
    max_selection_bytes: int
    max_owners: int
    max_files_per_owner: int
    max_total_files: int
    max_bytes_per_file: int
    max_total_bytes: int

    def __post_init__(self) -> None:
        for name in (
            "max_selection_bytes", "max_owners", "max_files_per_owner",
            "max_total_files", "max_bytes_per_file", "max_total_bytes",
        ):
            v = getattr(self, name)
            if type(v) is not int or isinstance(v, bool):
                raise SelectionError("SELECTION_LIMITS_INVALID")
            if v < 1 or v > sys.maxsize - 1:
                raise SelectionError("SELECTION_LIMITS_INVALID")


@dataclass(frozen=True, slots=True)
class AttestationRecord:
    component_id: str
    component_version: str
    scope: str
    target_id: str
    target_version: str
    suite_id: str
    suite_version: str
    verdict: str
    proof_ref: str

    def __post_init__(self) -> None:
        for name in _ATTESTATION_FIELDS:
            v = getattr(self, name)
            if type(v) is not str or not v or "\x00" in v or "\r" in v or "\n" in v:
                raise SelectionError("SELECTION_SCHEMA_INVALID")
            try:
                v.encode("utf-8")
            except UnicodeEncodeError as error:
                raise SelectionError("SELECTION_SCHEMA_INVALID") from error

    def to_dict(self) -> dict:
        return {name: getattr(self, name) for name in _ATTESTATION_FIELDS}


@dataclass(frozen=True, slots=True)
class CapturedFile:
    owner_index: int
    path: str
    sha256: str
    size: int
    data: bytes

    def __post_init__(self) -> None:
        if type(self.owner_index) is not int or isinstance(self.owner_index, bool) or self.owner_index < 0:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.path) is not str or not self.path:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if not _is_hex64(self.sha256):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.data) is not bytes:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.size) is not int or self.size < 0 or self.size != len(self.data):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if hashlib.sha256(self.data).hexdigest() != self.sha256:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        _parts(self.path)

    def to_dict(self) -> dict:
        return {
            "owner_index": self.owner_index,
            "path": self.path,
            "sha256": self.sha256,
            "size": self.size,
            "data_b64": base64.b64encode(self.data).decode("ascii"),
        }


@dataclass(frozen=True, slots=True)
class OwnerCapture:
    index: int
    owner: str
    owner_version: str
    root: str
    trust: str
    manifest: CapturedFile
    sources: tuple[CapturedFile, ...]

    def __post_init__(self) -> None:
        if type(self.index) is not int or self.index < 0:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        for v in (self.owner, self.owner_version, self.root, self.trust):
            _text(v)
        _parts(self.root)
        if self.trust not in TRUST_LEVELS:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.manifest) is not CapturedFile:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.sources) is not tuple or any(type(s) is not CapturedFile for s in self.sources):
            raise SelectionError("SELECTION_SCHEMA_INVALID")

        if (self.manifest.owner_index != self.index
                or self.manifest.path != self.root + "/" + MANIFEST_FILENAME
                or any(s.owner_index != self.index or not s.path.startswith(self.root + "/") for s in self.sources)):
            raise SelectionError("SELECTION_SCHEMA_INVALID")

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "owner": self.owner,
            "owner_version": self.owner_version,
            "root": self.root,
            "trust": self.trust,
            "manifest": self.manifest.to_dict(),
            "sources": [s.to_dict() for s in self.sources],
        }


@dataclass(frozen=True, slots=True)
class CaptureError:
    owner_index: int
    owner: str
    path: str
    code: str
    observed_sha256: str

    def __post_init__(self) -> None:
        if type(self.owner_index) is not int or isinstance(self.owner_index, bool) or self.owner_index < -1:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.owner) is not str or type(self.path) is not str or type(self.code) is not str or not self.code:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.observed_sha256) is not str:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if self.observed_sha256 and not _is_hex64(self.observed_sha256):
            raise SelectionError("SELECTION_SCHEMA_INVALID")

    def to_dict(self) -> dict:
        return {
            "owner_index": self.owner_index,
            "owner": self.owner,
            "path": self.path,
            "code": self.code,
            "observed_sha256": self.observed_sha256,
        }


@dataclass(frozen=True, slots=True)
class CompositionSnapshot:
    official_ids: tuple[str, ...]
    required_ids: tuple[str, ...]
    configured_providers: tuple[tuple[str, str], ...] | None
    attestations: tuple[AttestationRecord, ...]

    def __post_init__(self) -> None:
        if type(self.official_ids) is not tuple or type(self.required_ids) is not tuple:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        for v in self.official_ids + self.required_ids:
            _text(v)
        if (len(set(self.official_ids)) != len(self.official_ids)
                or len(set(self.required_ids)) != len(self.required_ids)):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if self.configured_providers is not None:
            if type(self.configured_providers) is not tuple:
                raise SelectionError("SELECTION_SCHEMA_INVALID")
            for pair in self.configured_providers:
                if type(pair) is not tuple or len(pair) != 2:
                    raise SelectionError("SELECTION_SCHEMA_INVALID")
                k, val = pair
                if type(k) is not str or not k or type(val) is not str or not val:
                    raise SelectionError("SELECTION_SCHEMA_INVALID")
            if len({k for k, _ in self.configured_providers}) != len(self.configured_providers):
                raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.attestations) is not tuple or any(type(a) is not AttestationRecord for a in self.attestations):
            raise SelectionError("SELECTION_SCHEMA_INVALID")

    def to_dict(self) -> dict:
        if self.configured_providers is None:
            providers: dict[str, str] | None = None
        else:
            providers = {k: v for k, v in self.configured_providers}
        return {
            "official_ids": list(self.official_ids),
            "required_ids": list(self.required_ids),
            "configured_providers": providers,
            "attestations": [a.to_dict() for a in self.attestations],
        }


@dataclass(frozen=True, slots=True)
class BatchCapture:
    selection_sha256: str
    environment: str
    provenance_reference: str
    context_fingerprint: str
    composition: CompositionSnapshot
    owners: tuple[OwnerCapture, ...]
    errors: tuple[CaptureError, ...]

    def __post_init__(self) -> None:
        if not _is_hex64(self.selection_sha256) or not _is_hex64(self.context_fingerprint):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if self.environment not in ENVIRONMENTS:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.provenance_reference) is not str or not self.provenance_reference:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.composition) is not CompositionSnapshot:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.owners) is not tuple or any(type(o) is not OwnerCapture for o in self.owners):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if type(self.errors) is not tuple or any(type(e) is not CaptureError for e in self.errors):
            raise SelectionError("SELECTION_SCHEMA_INVALID")

    def to_dict(self) -> dict:
        return {
            "schema": SELECTION_SCHEMA,
            "selection_sha256": self.selection_sha256,
            "environment": self.environment,
            "provenance_reference": self.provenance_reference,
            "context_fingerprint": self.context_fingerprint,
            "composition": self.composition.to_dict(),
            "owners": [o.to_dict() for o in self.owners],
            "errors": [e.to_dict() for e in self.errors],
        }


def _limits_fingerprint(limits: SelectionLimits) -> str:
    raw = "|".join(str(getattr(limits, n)) for n in (
        "max_selection_bytes", "max_owners", "max_files_per_owner",
        "max_total_files", "max_bytes_per_file", "max_total_bytes"))
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def _context_fingerprint(selection_sha256: str, environment: str, limits: SelectionLimits) -> str:
    raw = f"{SELECTION_SCHEMA}:{selection_sha256}:{environment}:{_limits_fingerprint(limits)}"
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def _read_confined(root: Path, full_posix: str, limits: SelectionLimits, remaining: list[int]) -> bytes:
    if remaining[0] < 0:
        raise SelectionError("QUOTA_EXCEEDED")
    names = _parts(full_posix)
    out = bytearray()
    file_left = limits.max_bytes_per_file
    with _directory(root, names[:-1]) as folder:
        fd = os.open(names[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder)
        try:
            mode = os.fstat(fd).st_mode
            if stat.S_ISFIFO(mode):
                raise SelectionError("FIFO_REFUSED")
            if not stat.S_ISREG(mode):
                raise SelectionError("NOT_REGULAR")
            while True:
                global_left = remaining[0]
                if global_left < 0:
                    raise SelectionError("QUOTA_EXCEEDED")
                allow = file_left if file_left < global_left else global_left
                want = allow + 1
                if want > 65536:
                    want = 65536
                if want < 1:
                    want = 1
                chunk = os.read(fd, want)
                if not chunk:
                    break
                out.extend(chunk)
                take = len(chunk)
                file_left -= take
                remaining[0] -= take
                if len(out) > limits.max_bytes_per_file or remaining[0] < 0:
                    raise SelectionError("QUOTA_EXCEEDED")
        finally:
            os.close(fd)
    return bytes(out)


def _validate_attestation(obj: object) -> AttestationRecord:
    if not isinstance(obj, dict) or set(obj.keys()) != set(_ATTESTATION_FIELDS):
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    values: dict[str, str] = {}
    for name in _ATTESTATION_FIELDS:
        v = obj[name]
        if type(v) is not str or not v or "\x00" in v or "\r" in v or "\n" in v:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        try:
            v.encode("utf-8")
        except UnicodeEncodeError as error:
            raise SelectionError("SELECTION_SCHEMA_INVALID") from error
        values[name] = v
    return AttestationRecord(**values)


def capture_selection(selection_bytes: bytes, *, expected_sha256: str,
                      project_root: Path, limits: SelectionLimits) -> BatchCapture:
    if type(selection_bytes) is not bytes:
        raise SelectionError("SELECTION_BYTES_INVALID")
    if type(expected_sha256) is not str or not _is_hex64(expected_sha256):
        raise SelectionError("SELECTION_PIN_INVALID")
    if not isinstance(project_root, Path):
        raise SelectionError("SELECTION_ROOT_INVALID")
    if type(limits) is not SelectionLimits:
        raise SelectionError("SELECTION_LIMITS_INVALID")
    limits.__post_init__()
    if len(selection_bytes) == 0 or len(selection_bytes) > limits.max_selection_bytes:
        raise SelectionError("SELECTION_TOO_LARGE")
    digest = hashlib.sha256(selection_bytes).hexdigest()
    if not hmac.compare_digest(digest, expected_sha256):
        raise SelectionError("SELECTION_PIN_MISMATCH")
    if selection_bytes.startswith(codecs.BOM_UTF8):
        raise SelectionError("SELECTION_BOM")
    if b"\r" in selection_bytes:
        raise SelectionError("SELECTION_BAD_NEWLINE")
    try:
        text = selection_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SelectionError("SELECTION_NOT_UTF8") from error
    if "\x00" in text:
        raise SelectionError("SELECTION_JSON_INVALID")
    try:
        obj = json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_const)
    except SelectionError:
        raise
    except (json.JSONDecodeError, ValueError, RecursionError) as error:
        raise SelectionError("SELECTION_JSON_INVALID") from error
    if not isinstance(obj, dict) or set(obj.keys()) != {"schema", "environment", "provenance", "components", "composition"}:
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    if obj["schema"] != SELECTION_SCHEMA or obj["environment"] not in ENVIRONMENTS:
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    prov = obj["provenance"]
    if (not isinstance(prov, dict) or set(prov.keys()) != {"kind", "reference"}
            or prov["kind"] != SELECTION_KIND
            or type(prov.get("reference")) is not str or not prov["reference"]
            or "\x00" in prov["reference"] or "\r" in prov["reference"]):
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    try:
        prov["reference"].encode("utf-8")
    except UnicodeEncodeError as error:
        raise SelectionError("SELECTION_SCHEMA_INVALID") from error
    _text(prov["reference"])
    comps = obj["components"]
    if type(comps) is not list or not comps or len(comps) > limits.max_owners:
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    comp = obj["composition"]
    if not isinstance(comp, dict) or set(comp.keys()) != {"official_ids", "required_ids", "configured_providers", "attestations"}:
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    for key in ("official_ids", "required_ids"):
        ids = comp[key]
        if type(ids) is not list or any(type(x) is not str or not x for x in ids) or len(set(ids)) != len(ids):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
    for key in ("official_ids", "required_ids"):
        for value in comp[key]:
            _text(value)
    raw_providers = comp["configured_providers"]
    if raw_providers is None:
        providers: tuple[tuple[str, str], ...] | None = None
    elif isinstance(raw_providers, Mapping):
        items: list[tuple[str, str]] = []
        for k, v in raw_providers.items():
            if type(k) is not str or not k or type(v) is not str or not v:
                raise SelectionError("SELECTION_SCHEMA_INVALID")
            _text(k)
            _text(v)
            items.append((k, v))
        if len({k for k, _ in items}) != len(items):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        providers = tuple(sorted(items))
    else:
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    raw_atts = comp["attestations"]
    if type(raw_atts) is not list:
        raise SelectionError("SELECTION_SCHEMA_INVALID")
    attestations = tuple(_validate_attestation(a) for a in raw_atts)
    composition = CompositionSnapshot(
        official_ids=tuple(comp["official_ids"]),
        required_ids=tuple(comp["required_ids"]),
        configured_providers=providers,
        attestations=attestations,
    )
    fingerprint = _context_fingerprint(digest, obj["environment"], limits)
    # Tout le document de contrôle est validé avant accès au système de fichiers.
    struct: list[tuple[int, dict]] = []
    seen_owners: set[str] = set()
    seen_roots: set[str] = set()
    seen_full: set[str] = set()
    total_files = 0
    for index, component in enumerate(comps):
        if type(component) is not dict or set(component) != {
            "owner", "owner_version", "root", "trust", "manifest", "sources",
        }:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        _text(component["owner"])
        _text(component["owner_version"])
        try:
            parse_version(component["owner_version"])
        except ValueError as error:
            raise SelectionError("SELECTION_SCHEMA_INVALID") from error
        parts = _parts(component["root"])
        if type(component["trust"]) is not str or component["trust"] not in TRUST_LEVELS:
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        if component["owner"] in seen_owners or component["root"] in seen_roots:
            raise SelectionError("SELECTION_DUPLICATE")
        seen_owners.add(component["owner"])
        seen_roots.add(component["root"])
        manifest = component["manifest"]
        if (type(manifest) is not dict or set(manifest) != {"path", "sha256"}
                or manifest["path"] != MANIFEST_FILENAME or not _is_hex64(manifest["sha256"])):
            raise SelectionError("SELECTION_SCHEMA_INVALID")
        sources = component["sources"]
        if type(sources) is not list or len(sources) + 1 > limits.max_files_per_owner:
            raise SelectionError("SELECTION_LIMITS_INVALID")
        total_files += len(sources) + 1
        if total_files > limits.max_total_files:
            raise SelectionError("SELECTION_LIMITS_INVALID")
        full_paths = [component["root"] + "/" + MANIFEST_FILENAME]
        for source in sources:
            if type(source) is not dict or set(source) != {"path", "sha256"}:
                raise SelectionError("SELECTION_SCHEMA_INVALID")
            _parts(source["path"])
            if not source["path"].endswith(SOURCE_SUFFIXES) or not _is_hex64(source["sha256"]):
                raise SelectionError("SELECTION_SCHEMA_INVALID")
            full_paths.append(component["root"] + "/" + source["path"])
        for path in full_paths:
            _parts(path)
            if path in seen_full:
                raise SelectionError("SELECTION_DUPLICATE")
            seen_full.add(path)
        struct.append((index, component))
    for index, component in struct:
        for path in [component["root"] + "/" + MANIFEST_FILENAME] + [
            component["root"] + "/" + source["path"] for source in component["sources"]
        ]:
            for _, other in struct:
                if (other["root"] != component["root"]
                        and other["root"].startswith(component["root"] + "/")
                        and path.startswith(other["root"] + "/")):
                    raise SelectionError("SELECTION_OWNER_CONFLICT")
    try:
        root = _project_root(project_root)
    except _BridgeBuildError as error:
        raise SelectionError("SELECTION_ROOT_INVALID") from error

    remaining = [limits.max_total_bytes]
    owners: list[OwnerCapture] = []
    errors: list[CaptureError] = []
    for index, component in struct:
        if remaining[0] < 0:
            errors.append(CaptureError(index, "", "", "QUOTA_EXCEEDED", ""))
            continue
        owner, owner_errors = _capture_owner(index, component, root, limits, remaining)
        if owner is not None:
            owners.append(owner)
        errors.extend(owner_errors)
    return BatchCapture(
        selection_sha256=digest,
        environment=obj["environment"],
        provenance_reference=prov["reference"],
        context_fingerprint=fingerprint,
        composition=composition,
        owners=tuple(owners),
        errors=tuple(errors),
    )


def _capture_owner(index: int, c: dict, root: Path, limits: SelectionLimits,
                   remaining: list[int]) -> tuple[OwnerCapture | None, list[CaptureError]]:
    owner: str = c["owner"]
    root_rel: str = c["root"]
    mf_full = f"{root_rel}/{MANIFEST_FILENAME}"
    try:
        mf_bytes = _read_confined(root, mf_full, limits, remaining)
    except SelectionError as error:
        return None, [CaptureError(index, "", "", error.code, "")]
    except OSError as error:
        return None, [CaptureError(index, "", "", "SOURCE_UNAVAILABLE", "")]
    observed_mf = hashlib.sha256(mf_bytes).hexdigest()
    if observed_mf != c["manifest"]["sha256"]:
        return None, [CaptureError(index, "", "", "MANIFEST_MISMATCH", observed_mf)]
    if mf_bytes.startswith(codecs.BOM_UTF8):
        return None, [CaptureError(index, "", "", "BOM_REFUSED", observed_mf)]
    if b"\r" in mf_bytes:
        return None, [CaptureError(index, "", "", "CRLF_REFUSED", observed_mf)]
    try:
        mf_text = mf_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None, [CaptureError(index, "", "", "UTF8_INVALID", observed_mf)]
    try:
        parsed = parse_manifest_text(mf_text)
    except ManifestValidationError:
        return None, [CaptureError(index, "", "", "MANIFEST_KERNEL_REFUSED", observed_mf)]
    if parsed.id != owner or parsed.version != c["owner_version"]:
        return None, [CaptureError(index, "", "", "MANIFEST_MISMATCH", observed_mf)]
    listed = {s["path"] for s in c["sources"]}
    if parsed.frontend is not None:
        contributions = parsed.frontend.contributions
        if type(contributions) is not tuple:
            return None, [CaptureError(index, "", "", "MANIFEST_KERNEL_REFUSED", observed_mf)]
        for item in contributions:
            entry = item.entry
            if type(entry) is not str or entry not in listed:
                return None, [CaptureError(index, "", "", "FRONTEND_ENTRY_UNLISTED", observed_mf)]
    manifest_cf = CapturedFile(index, mf_full, observed_mf, len(mf_bytes), mf_bytes)
    srcs: list[CapturedFile] = []
    for s in c["sources"]:
        full = f"{root_rel}/{s['path']}"
        try:
            data = _read_confined(root, full, limits, remaining)
        except SelectionError as error:
            return None, [CaptureError(index, "", "", error.code, "")]
        except OSError as error:
            return None, [CaptureError(index, "", "", "SOURCE_UNAVAILABLE", "")]
        observed = hashlib.sha256(data).hexdigest()
        if observed != s["sha256"]:
            return None, [CaptureError(index, "", "", "HASH_DRIFT", observed)]
        if data.startswith(codecs.BOM_UTF8):
            return None, [CaptureError(index, "", "", "BOM_REFUSED", observed)]
        if b"\r" in data:
            return None, [CaptureError(index, "", "", "CRLF_REFUSED", observed)]
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            return None, [CaptureError(index, "", "", "UTF8_INVALID", observed)]
        srcs.append(CapturedFile(index, full, observed, len(data), data))
    return OwnerCapture(index, owner, c["owner_version"], root_rel, c["trust"], manifest_cf, tuple(srcs)), []


def verify_before_publish(capture: BatchCapture, *, selection_bytes: bytes,
                          expected_sha256: str, project_root: Path,
                          limits: SelectionLimits) -> BatchCapture:
    if type(capture) is not BatchCapture or type(selection_bytes) is not bytes:
        raise SelectionError("SELECTION_BYTES_INVALID")
    if type(expected_sha256) is not str or not _is_hex64(expected_sha256):
        raise SelectionError("SELECTION_PIN_INVALID")
    if not isinstance(project_root, Path) or type(limits) is not SelectionLimits:
        raise SelectionError("SELECTION_LIMITS_INVALID")
    limits.__post_init__()
    fresh = capture_selection(selection_bytes, expected_sha256=expected_sha256,
                              project_root=project_root, limits=limits)
    if fresh.selection_sha256 != capture.selection_sha256:
        raise SelectionError("SELECTION_DRIFT")
    if fresh.selection_sha256 != expected_sha256:
        raise SelectionError("SELECTION_DRIFT")
    if fresh.context_fingerprint != capture.context_fingerprint:
        raise SelectionError("SELECTION_DRIFT")
    if fresh != capture:
        raise SelectionError("SELECTION_DRIFT")
    return capture


def _build_limits(ns: argparse.Namespace) -> SelectionLimits:
    return SelectionLimits(
        max_selection_bytes=int(ns.max_selection_bytes),
        max_owners=int(ns.max_owners),
        max_files_per_owner=int(ns.max_files_per_owner),
        max_total_files=int(ns.max_total_files),
        max_bytes_per_file=int(ns.max_bytes_per_file),
        max_total_bytes=int(ns.max_total_bytes),
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="build_frontend_selection")
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--max-selection-bytes", required=True)
    ap.add_argument("--max-owners", required=True)
    ap.add_argument("--max-files-per-owner", required=True)
    ap.add_argument("--max-total-files", required=True)
    ap.add_argument("--max-bytes-per-file", required=True)
    ap.add_argument("--max-total-bytes", required=True)
    ns = ap.parse_args(argv)
    try:
        limits = _build_limits(ns)
    except SelectionError:
        sys.stderr.write("SELECTION_LIMITS_INVALID\n")
        return 2
    except (TypeError, ValueError):
        sys.stderr.write("SELECTION_LIMITS_INVALID\n")
        return 2
    data = sys.stdin.buffer.read(limits.max_selection_bytes + 1)
    if not data or len(data) > limits.max_selection_bytes:
        sys.stderr.write("SELECTION_TOO_LARGE\n")
        return 2
    try:
        cap = capture_selection(
            data,
            expected_sha256=ns.expected_sha256,
            project_root=Path(ns.project_root),
            limits=limits,
        )
    except SelectionError as error:
        sys.stderr.write(error.code + "\n")
        return 2
    except _BridgeBuildError as error:
        sys.stderr.write(error.code + "\n")
        return 2
    sys.stdout.write(json.dumps(cap.to_dict(), sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
