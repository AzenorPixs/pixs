"""Validation et capture pures de l'identité d'admission Bulk, sans ORM ni effet.

Entrée fermée aux 9 clés exactes, types exacts avant tout comportement, snapshot
bytes strict vérifié par recapture exacte via `capture_bulk_admission_fingerprint`
existant. Aucune persistance, autorité, purge, hold, transaction ou I/O.
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from pixs.backend.bulk_admission_fingerprint import (
    capture_bulk_admission_fingerprint,
)
from pixs.backend.bulk_execution_values import (
    _exact_mapping,
    _is_complete_semver,
    _is_runtime_text,
    _pack,
    _refusal,
)
from pixs.kernel.diagnostics import Diagnostic

__all__ = [
    "validate_bulk_admission_identity_values",
    "capture_bulk_admission_identity",
]

_SCOPE = "bulk_admission_identity_values"

_FIELDS = (
    "resolved_tenant_id",
    "resolved_subject_id",
    "bulk_type",
    "idempotency_key",
    "operation_id",
    "admission_content_sha256",
    "admission_contract_version",
    "admission_content_snapshot",
    "expires_at",
)

_STR_REQUIRED = (
    "resolved_tenant_id",
    "resolved_subject_id",
    "bulk_type",
    "idempotency_key",
    "operation_id",
    "admission_content_sha256",
    "admission_contract_version",
)

_FINGERPRINT_FIELDS = frozenset((
    "execution_version",
    "bulk_type",
    "bulk_version",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
    "requested_by_reference",
    "mapping_reference",
    "mapping_version",
    "input_reference",
    "input_version",
    "input_sha256",
    "input_size_bytes",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
    "idempotency_key",
    "policy_reference",
    "policy_version",
    "expires_at",
))

_VARIANTS = frozenset({"IMPORT", "EXPORT"})
_SHA256_PATTERN = re.compile("[0-9a-f]{64}")
_INSTANT_PATTERN = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z"
)


@dataclass(frozen=True, slots=True)
class _AdmissionIdentityBound:
    resolved_tenant_id: str
    resolved_subject_id: str
    bulk_type: str
    idempotency_key: str
    operation_id: str
    admission_content_sha256: str
    admission_contract_version: str
    admission_content_snapshot: bytes
    expires_at: datetime


def _type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_SCOPE, field, "str exacte attendue")
        for field in _STR_REQUIRED
        if type(values[field]) is not str
    ]
    if type(values["admission_content_snapshot"]) is not bytes:
        refusals.append(
            _refusal(_SCOPE, "admission_content_snapshot", "bytes exacts attendus")
        )
    if type(values["expires_at"]) is not datetime:
        refusals.append(
            _refusal(_SCOPE, "expires_at", "datetime exact attendu")
        )
    elif values["expires_at"].tzinfo is not timezone.utc:
        refusals.append(
            _refusal(_SCOPE, "expires_at", "datetime exact aware UTC attendu")
        )
    return refusals


def _value_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in _STR_REQUIRED:
        value = values[field]
        if value is not None and not _is_runtime_text(value):
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "texte runtime UTF-8 strict non vide sans NUL attendu",
                )
            )
    if values["bulk_type"] not in _VARIANTS:
        refusals.append(
            _refusal(
                _SCOPE, "bulk_type", "valeur texte canonique exacte attendue"
            )
        )
    if _SHA256_PATTERN.fullmatch(values["admission_content_sha256"]) is None:
        refusals.append(
            _refusal(
                _SCOPE,
                "admission_content_sha256",
                "empreinte SHA-256 hex minuscule de 64 caractères attendue",
            )
        )
    if values["admission_contract_version"] != "1.0.0":
        refusals.append(
            _refusal(
                _SCOPE, "admission_contract_version", "1.0.0 exact attendu"
            )
        )
    elif not _is_complete_semver(values["admission_contract_version"]):
        refusals.append(
            _refusal(
                _SCOPE,
                "admission_contract_version",
                "version SemVer complète exacte attendue",
            )
        )
    snapshot = values["admission_content_snapshot"]
    if len(snapshot) == 0:
        refusals.append(
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot bytes exacts non vides attendu",
            )
        )
    if values["expires_at"].tzinfo is not timezone.utc:
        refusals.append(
            _refusal(_SCOPE, "expires_at", "datetime exact aware UTC attendu")
        )
    return refusals


def _reject_float(value: str) -> object:
    raise ValueError("float interdit")


def _reject_constant(value: str) -> object:
    raise ValueError("constante non finie interdite")


def _pairs_no_duplicates(pairs: list) -> dict:
    seen: set = set()
    result: dict = {}
    for key, value in pairs:
        if type(key) is not str or key in seen:
            raise ValueError("clé dupliquée ou étrangère")
        seen.add(key)
        result[key] = value
    return result


def _parse_canonical_instant(text: object) -> datetime | None:
    if type(text) is not str:
        return None
    if _INSTANT_PATTERN.fullmatch(text) is None:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed


def _resolve_snapshot(values: dict) -> tuple[object | None, list[Diagnostic]]:
    snapshot = values["admission_content_snapshot"]
    try:
        text = snapshot.decode("utf-8")
    except UnicodeDecodeError:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot UTF-8 strict invalide",
            )
        ]
    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_reject_float,
            parse_int=int,
            parse_constant=_reject_constant,
        )
    except (ValueError, RecursionError):
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot JSON fermé 22 champs invalide",
            )
        ]
    if type(parsed) is not dict:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot JSON fermé 22 champs invalide",
            )
        ]
    if set(parsed.keys()) != set(_FINGERPRINT_FIELDS) or len(parsed) != 22:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot JSON fermé 22 champs invalide",
            )
        ]
    instant = _parse_canonical_instant(parsed.get("expires_at"))
    if instant is None:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot JSON fermé 22 champs invalide",
            )
        ]
    candidate = dict(parsed)
    candidate["expires_at"] = instant
    recapture, diags = capture_bulk_admission_fingerprint(candidate)
    if recapture is None or diags:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot JSON fermé 22 champs invalide",
            )
        ]
    if recapture.canonical_bytes != snapshot:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_snapshot",
                "snapshot non canonique refusé",
            )
        ]
    if values["admission_content_sha256"] != recapture.content_sha256:
        return None, [
            _refusal(
                _SCOPE,
                "admission_content_sha256",
                "digest incohérent avec le snapshot",
            )
        ]
    if values["bulk_type"] != parsed.get("bulk_type"):
        return None, [
            _refusal(
                _SCOPE, "bulk_type", "incohérent avec le snapshot"
            )
        ]
    if values["idempotency_key"] != parsed.get("idempotency_key"):
        return None, [
            _refusal(
                _SCOPE, "idempotency_key", "incohérent avec le snapshot"
            )
        ]
    if values["admission_contract_version"] != parsed.get("execution_version"):
        return None, [
            _refusal(
                _SCOPE,
                "admission_contract_version",
                "incohérente avec le snapshot",
            )
        ]
    return recapture, []


def validate_bulk_admission_identity_values(
    candidate: object,
) -> list[Diagnostic]:
    """Refuse les types étrangers avant tout comportement, puis contrôle strict."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "neuf clés exactes attendues"
    )
    if values is None:
        return _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return _pack(type_refusals)
    refusals = _value_refusals(values)
    if refusals:
        return _pack(refusals)
    _, snapshot_refusals = _resolve_snapshot(values)
    refusals.extend(snapshot_refusals)
    return _pack(refusals)


def capture_bulk_admission_identity(
    candidate: object,
) -> tuple[_AdmissionIdentityBound | None, list[Diagnostic]]:
    """Capture owned immuable ou refuse sans capture partielle."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "neuf clés exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return None, _pack(type_refusals)
    refusals = _value_refusals(values)
    if refusals:
        return None, _pack(refusals)
    _, snapshot_refusals = _resolve_snapshot(values)
    packed = _pack([*refusals, *snapshot_refusals])
    if packed:
        return None, packed
    return (
        _AdmissionIdentityBound(
            resolved_tenant_id=values["resolved_tenant_id"],
            resolved_subject_id=values["resolved_subject_id"],
            bulk_type=values["bulk_type"],
            idempotency_key=values["idempotency_key"],
            operation_id=values["operation_id"],
            admission_content_sha256=values["admission_content_sha256"],
            admission_contract_version=values["admission_contract_version"],
            admission_content_snapshot=bytes(values["admission_content_snapshot"]),
            expires_at=values["expires_at"],
        ),
        [],
    )
