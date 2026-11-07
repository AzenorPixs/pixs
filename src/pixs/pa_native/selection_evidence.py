"""Preuves de selection PA01, decodeurs purs S2a.

Valide la forme JSON fermee du manifeste (8 racines), de l'acquisition
(7 champs), des fichiers (role/path/sha256), de l'admission (8 champs)
et du retrait (7 champs), sans entree-sortie, sans reseau, sans
environnement, sans processus et sans compilation. Donnees non
certifiees : aucune origine, unicite historique, autorisation reelle,
identite physique, lien symbolique, auto-condensat, utilisabilite ou
etat courant n'est verifie ici. Liaisons entre preuves, S2b et S3
ulterieurs.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, time
from pathlib import PurePosixPath
from typing import Any

from pixs.pa_native.build_profile import ProfileError, _CYTHON_LOCK as _PROFILE_CYTHON_LOCK

__all__ = [
    "AdmissionRecord",
    "EvidenceManifest",
    "ManifestAcquisition",
    "ManifestFile",
    "SelectionEvidenceError",
    "WithdrawalEvent",
    "parse_admission",
    "parse_manifest",
    "parse_withdrawal",
]

_CODE = "PA01_CAMPAIGN_METADATA_INVALID"
_SCHEMA = "1.0.0"
_COMPONENT = "pa01"
_SOURCE_URL = "https://pypi.org/pypi/Cython/json"
_MANIFEST_KEYS = frozenset({"schema_version", "campaign_id", "component", "cython_version", "verified_at", "source_url", "acquisition", "files"})
_ACQUISITION_KEYS = frozenset({"requested_url", "final_url", "started_at", "finished_at", "http_status", "client_ref", "tls_policy_ref"})
_FILE_KEYS = frozenset({"role", "path", "sha256"})
_ADMISSION_KEYS = frozenset({"schema_version", "admission_id", "campaign_id", "manifest_sha256", "reviewer_ref", "authorization_ref", "reviewed_at", "decision"})
_WITHDRAWAL_KEYS = frozenset({"schema_version", "withdrawal_id", "admission_id", "withdrawn_at", "reviewer_ref", "authorization_ref", "reason"})
_ROLES = frozenset({"build_profile", "campaign_metadata", "pyproject", "pypi_snapshot", "distribution"})
_SINGLETON_ORDER = ("build_profile", "campaign_metadata", "pyproject", "pypi_snapshot")
_SINGLETON_ROLES = frozenset(_SINGLETON_ORDER)
_SHA256 = re.compile(r"[0-9a-f]{64}")
_UTC = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]+))?Z")


class SelectionEvidenceError(ProfileError):
    """Preuve invalide en forme ; diagnostic structurel sans restitution des valeurs."""


@dataclass(frozen=True, slots=True)
class ManifestAcquisition:
    requested_url: str
    final_url: str
    started_at: str
    finished_at: str
    http_status: int
    client_ref: str
    tls_policy_ref: str


@dataclass(frozen=True, slots=True)
class ManifestFile:
    role: str
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class EvidenceManifest:
    schema_version: str
    campaign_id: str
    component: str
    cython_version: str
    verified_at: str
    source_url: str
    acquisition: ManifestAcquisition
    files: tuple[ManifestFile, ...]


@dataclass(frozen=True, slots=True)
class AdmissionRecord:
    schema_version: str
    admission_id: str
    campaign_id: str
    manifest_sha256: str
    reviewer_ref: str
    authorization_ref: str
    reviewed_at: str
    decision: str


@dataclass(frozen=True, slots=True)
class WithdrawalEvent:
    schema_version: str
    withdrawal_id: str
    admission_id: str
    withdrawn_at: str
    reviewer_ref: str
    authorization_ref: str
    reason: str


def _fail(detail: str) -> SelectionEvidenceError:
    return SelectionEvidenceError(_CODE + " : " + detail)


def _is_forbidden_control(value: str) -> bool:
    for c in value:
        o = ord(c)
        if o < 32 or 127 <= o <= 159 or 0xD800 <= o <= 0xDFFF:
            return True
    return False


def _text(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise _fail(field + " : texte non vide attendu") from None
    if _is_forbidden_control(value):
        raise _fail(field + " : texte non vide attendu") from None
    return value


def _closed(value: Any, keys: frozenset, field: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != set(keys):
        raise _fail(field + " : champs obligatoires manquants ou inconnus") from None
    return value


def _utc(value: Any, field: str) -> str:
    text = _text(value, field)
    match = _UTC.fullmatch(text)
    if match is None:
        raise _fail(field + " : instant UTC textuel attendu") from None
    try:
        date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError as error:
        raise _fail(field + " : instant UTC textuel attendu") from error
    try:
        time(int(match.group(4)), int(match.group(5)), int(match.group(6)))
    except ValueError as error:
        raise _fail(field + " : instant UTC textuel attendu") from error
    return text


def _split_utc(text: str) -> tuple[int, int, int, int, int, int, str]:
    match = _UTC.fullmatch(text)
    assert match is not None
    frac = match.group(7) if match.group(7) is not None else ""
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)), int(match.group(6)), frac)


def _le_utc(first: str, second: str) -> bool:
    a = _split_utc(first)
    b = _split_utc(second)
    if a[:6] != b[:6]:
        return a[:6] <= b[:6]
    fa = a[6]
    fb = b[6]
    width = len(fa) if len(fa) >= len(fb) else len(fb)
    pa = fa.ljust(width, "0")
    pb = fb.ljust(width, "0")
    return pa <= pb


def _sha256(value: Any, field: str) -> str:
    text = _text(value, field)
    if _SHA256.fullmatch(text) is None:
        raise _fail(field + " : SHA-256 hexadecimal attendu") from None
    return text


def _cython_version(value: Any) -> str:
    text = _text(value, "cython_version")
    if _PROFILE_CYTHON_LOCK.fullmatch(text) is None:
        raise _fail("cython_version : version stable exacte normalisee requise") from None
    return text


def _relative_path(value: Any, field: str) -> str:
    text = _text(value, field)
    if "\\" in text:
        raise _fail(field + " : chemin relatif canonique requis") from None
    if PurePosixPath(text).is_absolute():
        raise _fail(field + " : chemin relatif canonique requis") from None
    parts = text.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise _fail(field + " : chemin relatif canonique requis") from None
    return text


def _no_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError("cle dupliquee")
    return dict(pairs)


def _reject_constant(value: str) -> Any:
    raise ValueError("constante JSON interdite")


def _load(data: bytes, doc: str) -> dict[str, Any]:
    if type(data) is not bytes:
        raise _fail(doc + " : octets JSON attendus") from None
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise _fail(doc + " : texte UTF-8 strict attendu") from error
    if "\r" in text:
        raise _fail(doc + " : fins de ligne LF attendues") from None
    try:
        parsed = json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_constant)
    except RecursionError as error:
        raise _fail(doc + " : profondeur JSON excessive") from error
    except ValueError as error:
        raise _fail(doc + " : syntaxe JSON stricte invalide") from error
    if type(parsed) is not dict:
        raise _fail(doc + " : objet JSON attendu") from None
    return parsed


def _acquisition(value: Any) -> ManifestAcquisition:
    table = _closed(value, _ACQUISITION_KEYS, "acquisition")
    requested = _text(table["requested_url"], "acquisition.requested_url")
    if requested != _SOURCE_URL:
        raise _fail("acquisition.requested_url : source exacte attendue") from None
    final = _text(table["final_url"], "acquisition.final_url")
    if final != _SOURCE_URL:
        raise _fail("acquisition.final_url : source exacte attendue") from None
    started = _utc(table["started_at"], "acquisition.started_at")
    finished = _utc(table["finished_at"], "acquisition.finished_at")
    if not _le_utc(started, finished):
        raise _fail("acquisition : ordre chronologique attendu") from None
    status = table["http_status"]
    if type(status) is not int or status != 200:
        raise _fail("acquisition.http_status : entier exact 200 attendu") from None
    client = _text(table["client_ref"], "acquisition.client_ref")
    policy = _text(table["tls_policy_ref"], "acquisition.tls_policy_ref")
    return ManifestAcquisition(requested_url=requested, final_url=final, started_at=started, finished_at=finished, http_status=200, client_ref=client, tls_policy_ref=policy)


def parse_manifest(data: bytes) -> EvidenceManifest:
    """Valide un manifeste de preuve a partir de ses octets JSON figes.

    Pur : aucune entree-sortie, aucun acces reseau, aucune lecture
d'environnement, aucun sous-processus. Ordre des cles, indentation et
Unicode echappe acceptes si JSON valide ; sans reecriture.
    """
    root = _load(data, "manifeste")
    _closed(root, _MANIFEST_KEYS, "manifeste")
    if type(root["schema_version"]) is not str or root["schema_version"] != _SCHEMA:
        raise _fail("schema_version : version exacte 1.0.0 attendue") from None
    campaign_id = _text(root["campaign_id"], "campaign_id")
    if type(root["component"]) is not str or root["component"] != _COMPONENT:
        raise _fail("component : valeur exacte pa01 attendue") from None
    cython = _cython_version(root["cython_version"])
    verified = _utc(root["verified_at"], "verified_at")
    if type(root["source_url"]) is not str or root["source_url"] != _SOURCE_URL:
        raise _fail("source_url : source exacte attendue") from None
    acquisition = _acquisition(root["acquisition"])
    if verified != acquisition.finished_at:
        raise _fail("verified_at : identite textuelle avec finished_at attendue") from None
    raw_files = root["files"]
    if type(raw_files) is not list or not raw_files:
        raise _fail("files : liste non vide attendue") from None
    seen_paths: set[str] = set()
    seen_roles: dict[str, int] = {}
    files: list[ManifestFile] = []
    for item in raw_files:
        _closed(item, _FILE_KEYS, "files[]")
        role = _text(item["role"], "files[].role")
        if role not in _ROLES:
            raise _fail("files[].role : role ferme attendu") from None
        seen_roles[role] = seen_roles.get(role, 0) + 1
        path = _relative_path(item["path"], "files[].path")
        if path in seen_paths:
            raise _fail("files[].path : chemin unique attendu") from None
        seen_paths.add(path)
        digest = _sha256(item["sha256"], "files[].sha256")
        files.append(ManifestFile(role=role, path=path, sha256=digest))
    for singleton in _SINGLETON_ORDER:
        if seen_roles.get(singleton, 0) != 1:
            raise _fail("files : un seul " + singleton + " attendu") from None
    if seen_roles.get("distribution", 0) < 1:
        raise _fail("files : au moins une distribution attendue") from None
    return EvidenceManifest(schema_version=_SCHEMA, campaign_id=campaign_id, component=_COMPONENT, cython_version=cython, verified_at=verified, source_url=_SOURCE_URL, acquisition=acquisition, files=tuple(files))


def parse_admission(data: bytes) -> AdmissionRecord:
    """Valide un enregistrement d'admission (donnee non certifiee)."""
    root = _load(data, "admission")
    _closed(root, _ADMISSION_KEYS, "admission")
    if type(root["schema_version"]) is not str or root["schema_version"] != _SCHEMA:
        raise _fail("schema_version : version exacte 1.0.0 attendue") from None
    admission_id = _text(root["admission_id"], "admission_id")
    campaign_id = _text(root["campaign_id"], "campaign_id")
    manifest = _sha256(root["manifest_sha256"], "manifest_sha256")
    reviewer = _text(root["reviewer_ref"], "reviewer_ref")
    authorization = _text(root["authorization_ref"], "authorization_ref")
    reviewed = _utc(root["reviewed_at"], "reviewed_at")
    decision = root["decision"]
    if type(decision) is not str or decision != "ADMITTED":
        raise _fail("decision : valeur exacte ADMITTED attendue") from None
    return AdmissionRecord(schema_version=_SCHEMA, admission_id=admission_id, campaign_id=campaign_id, manifest_sha256=manifest, reviewer_ref=reviewer, authorization_ref=authorization, reviewed_at=reviewed, decision="ADMITTED")


def parse_withdrawal(data: bytes) -> WithdrawalEvent:
    """Valide un evenement de retrait (donnee non certifiee)."""
    root = _load(data, "retrait")
    _closed(root, _WITHDRAWAL_KEYS, "retrait")
    if type(root["schema_version"]) is not str or root["schema_version"] != _SCHEMA:
        raise _fail("schema_version : version exacte 1.0.0 attendue") from None
    withdrawal_id = _text(root["withdrawal_id"], "withdrawal_id")
    admission_id = _text(root["admission_id"], "admission_id")
    withdrawn = _utc(root["withdrawn_at"], "withdrawn_at")
    reviewer = _text(root["reviewer_ref"], "reviewer_ref")
    authorization = _text(root["authorization_ref"], "authorization_ref")
    reason = _text(root["reason"], "reason")
    return WithdrawalEvent(schema_version=_SCHEMA, withdrawal_id=withdrawal_id, admission_id=admission_id, withdrawn_at=withdrawn, reviewer_ref=reviewer, authorization_ref=authorization, reason=reason)
