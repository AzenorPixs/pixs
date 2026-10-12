"""Capture pure initial-snapshot FingerprintV1, sans ORM ni effet.

Valide une entrée fermée aux 22 clés normatives FingerprintV1, la
canonicalise une seule fois (tri lexicographique, JSON compact,
ensure_ascii=False, UTF-8 strict, datetime UTC six décimales Z,
None->null, sans float) puis rend son SHA-256 dans un snapshot
immuable. Types exacts d'abord, sans conversion ni hooks foreign.
Aucune persistance, autorité, déduplication SQL, horloge, réseau,
environnement, fichier ou processus.
"""

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from pixs.backend.bulk_execution_values import (
    _exact_mapping,
    _is_complete_semver,
    _is_runtime_text,
    _pack,
    _refusal,
)
from pixs.kernel.diagnostics import Diagnostic

__all__ = [
    "validate_bulk_admission_fingerprint_values",
    "capture_bulk_admission_fingerprint",
]

_SCOPE = "bulk_admission_fingerprint_values"

_FIELDS = (
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
)

_STR_REQUIRED = (
    "execution_version",
    "bulk_type",
    "bulk_version",
    "tenant_context_reference",
    "format",
    "requested_by_reference",
    "mapping_reference",
    "mapping_version",
    "idempotency_key",
    "policy_reference",
    "policy_version",
)

_STR_NULLABLE = (
    "scope_context_reference",
    "conflict_strategy",
    "commit_mode",
    "input_reference",
    "input_version",
    "input_sha256",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
)

_SIZE_NULLABLE = ("input_size_bytes",)

_SEMVER_FIELDS = ("bulk_version", "mapping_version", "policy_version")
_SHA_FIELDS = ("input_sha256",)

_SHA256_PATTERN = re.compile("[0-9a-f]{64}")

_IMPORT = "IMPORT"
_EXPORT = "EXPORT"
_VARIANTS = frozenset({_IMPORT, _EXPORT})
_FORMATS = frozenset({"CSV", "NDJSON"})
_CONFLICTS = frozenset({"REJECT", "CREATE_ONLY", "UPDATE_ONLY", "UPSERT"})
_COMMIT_MODES = frozenset({"VALIDATE_ONLY", "ATOMIC", "ATOMIC_PER_CHUNK", "BEST_EFFORT"})
_CONSISTENCY_KINDS = frozenset({"SNAPSHOT", "WATERMARK"})
_INPUT_FIELDS = (
    "input_reference",
    "input_version",
    "input_sha256",
    "input_size_bytes",
)


@dataclass(frozen=True, slots=True)
class _AdmissionFingerprint:
    canonical_bytes: bytes
    content_sha256: str


def _type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_SCOPE, field, "str exacte attendue")
        for field in _STR_REQUIRED
        if type(values[field]) is not str
    ]
    refusals.extend(
        _refusal(_SCOPE, field, "str exacte ou None déclaré attendu")
        for field in _STR_NULLABLE
        if type(values[field]) is not str and values[field] is not None
    )
    refusals.extend(
        _refusal(_SCOPE, field, "int exact ou None déclaré attendu")
        for field in _SIZE_NULLABLE
        if type(values[field]) is not int and values[field] is not None
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
    for field in (*_STR_REQUIRED, *_STR_NULLABLE):
        value = values[field]
        if value is not None and not _is_runtime_text(value):
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "texte runtime UTF-8 strict non vide sans NUL attendu",
                )
            )
    if values["execution_version"] != "1.0.0":
        refusals.append(
            _refusal(_SCOPE, "execution_version", "1.0.0 exact attendu")
        )
    if values["bulk_type"] not in _VARIANTS:
        refusals.append(
            _refusal(
                _SCOPE, "bulk_type", "valeur texte canonique exacte attendue"
            )
        )
    if values["format"] not in _FORMATS:
        refusals.append(
            _refusal(_SCOPE, "format", "valeur texte canonique exacte attendue")
        )
    if (
        values["conflict_strategy"] is not None
        and values["conflict_strategy"] not in _CONFLICTS
    ):
        refusals.append(
            _refusal(
                _SCOPE,
                "conflict_strategy",
                "valeur texte canonique exacte attendue",
            )
        )
    if values["commit_mode"] is not None and values["commit_mode"] not in _COMMIT_MODES:
        refusals.append(
            _refusal(
                _SCOPE, "commit_mode", "valeur texte canonique exacte attendue"
            )
        )
    for field in _SEMVER_FIELDS:
        if not _is_complete_semver(values[field]):
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "version SemVer complète exacte attendue",
                )
            )
    for field in _SHA_FIELDS:
        value = values[field]
        if value is not None and _SHA256_PATTERN.fullmatch(value) is None:
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "empreinte SHA-256 hex minuscule de 64 caractères attendue",
                )
            )
    size = values["input_size_bytes"]
    if size is not None and size < 0:
        refusals.append(
            _refusal(
                _SCOPE,
                "input_size_bytes",
                "entier exact supérieur ou égal à zéro attendu",
            )
        )
    if values["expires_at"].tzinfo is not timezone.utc:
        refusals.append(
            _refusal(_SCOPE, "expires_at", "datetime exact aware UTC attendu")
        )
    if (
        values["consistency_kind"] is not None
        and values["consistency_kind"] not in _CONSISTENCY_KINDS
    ):
        refusals.append(
            _refusal(
                _SCOPE,
                "consistency_kind",
                "consistency_kind SNAPSHOT ou WATERMARK attendu pour EXPORT",
            )
        )
    # scope None ne désigne ni PLATFORM ni tenant global : aucune
    # interprétation élargie, seule la nullabilité déclarée est admise.
    return refusals


def _import_export_refusals(values: dict) -> list[Diagnostic]:
    bulk_type = values["bulk_type"]
    if bulk_type not in _VARIANTS:
        return []
    refusals: list[Diagnostic] = []
    if bulk_type == _IMPORT:
        for field in _INPUT_FIELDS:
            if values[field] is None:
                refusals.append(
                    _refusal(
                        _SCOPE, field, "valeur non NULL attendue pour IMPORT"
                    )
                )
        for field in (
            "projection_reference",
            "consistency_kind",
            "consistency_reference",
        ):
            if values[field] is not None:
                refusals.append(
                    _refusal(
                        _SCOPE, field, "valeur NULL attendue pour IMPORT"
                    )
                )
        return refusals
    for field in _INPUT_FIELDS:
        if values[field] is not None:
            refusals.append(
                _refusal(_SCOPE, field, "valeur NULL attendue pour EXPORT")
            )
    if values["projection_reference"] is None:
        refusals.append(
            _refusal(
                _SCOPE,
                "projection_reference",
                "projection_reference non NULL attendue pour EXPORT",
            )
        )
    if values["consistency_kind"] not in _CONSISTENCY_KINDS:
        refusals.append(
            _refusal(
                _SCOPE,
                "consistency_kind",
                "consistency_kind SNAPSHOT ou WATERMARK attendu pour EXPORT",
            )
        )
    return refusals


def _canonicalize(values: dict) -> bytes:
    canonical: dict = {}
    for key in values:
        value = values[key]
        if type(value) is datetime:
            text = value.isoformat(timespec="microseconds")
            if text.endswith("+00:00"):
                text = text[:-6] + "Z"
            canonical[key] = text
        else:
            canonical[key] = value
    rendered = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return rendered.encode("utf-8")


def validate_bulk_admission_fingerprint_values(
    candidate: object,
) -> list[Diagnostic]:
    """Refuse les types étrangers avant tout comportement, puis contrôle B10/B02."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "vingt-deux clés exactes attendues"
    )
    if values is None:
        return _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return _pack(type_refusals)
    refusals = _value_refusals(values)
    refusals.extend(_import_export_refusals(values))
    return _pack(refusals)


def capture_bulk_admission_fingerprint(
    candidate: object,
) -> tuple[_AdmissionFingerprint | None, list[Diagnostic]]:
    """Capture owned immuable ou refuse sans capture partielle."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "vingt-deux clés exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return None, _pack(type_refusals)
    refusals = _value_refusals(values)
    refusals.extend(_import_export_refusals(values))
    packed = _pack(refusals)
    if packed:
        return None, packed
    try:
        canonical = _canonicalize(values)
    except ValueError:
        # La limite native de conversion des grands entiers peut refuser JSON.
        return None, _pack([
            _refusal(_SCOPE, "canonical_bytes", "sérialisation canonique indisponible")
        ])
    digest = hashlib.sha256(canonical).hexdigest()
    return (
        _AdmissionFingerprint(canonical_bytes=canonical, content_sha256=digest),
        [],
    )
