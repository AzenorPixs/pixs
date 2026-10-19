"""Validation et capture pures des valeurs ExportManifestV1, sans effet.

Entrée fermée aux dix-sept clés normatives du schéma logique ExportManifestV1,
types exacts et UTC avant tout comportement, puis contrôles fermés mémoire.
Aucun manifeste servi, finalisation prouvée, horloge, gouvernance, autorité,
consistance résolue, hash calculé, stockage, export, URL, transaction,
défaut, cohérence entre champs ni preuve.
"""

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
    "validate_bulk_export_manifest_values",
    "capture_bulk_export_manifest_values",
]

_SCOPE = "bulk_export_manifest_values"

_FIELDS = (
    "manifest_version",
    "operation_id",
    "format",
    "mapping_reference",
    "mapping_version",
    "tenant_context_reference",
    "scope_context_reference",
    "consistency_kind",
    "consistency_reference",
    "row_count",
    "size_bytes",
    "sha256",
    "classification_reference",
    "expires_at",
    "object_reference",
    "object_version",
    "complete",
)

_STR_REQUIRED = (
    "manifest_version",
    "operation_id",
    "format",
    "mapping_reference",
    "mapping_version",
    "tenant_context_reference",
    "consistency_kind",
    "consistency_reference",
    "sha256",
    "classification_reference",
    "object_reference",
    "object_version",
)

_FORMATS = frozenset({"CSV", "NDJSON"})
_KINDS = frozenset({"SNAPSHOT", "WATERMARK"})

_SHA256_PATTERN = re.compile("[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class _ExportManifestBound:
    manifest_version: str
    operation_id: str
    format: str
    mapping_reference: str
    mapping_version: str
    tenant_context_reference: str
    scope_context_reference: str | None
    consistency_kind: str
    consistency_reference: str
    row_count: int
    size_bytes: int
    sha256: str
    classification_reference: str
    expires_at: datetime
    object_reference: str
    object_version: str
    complete: bool


def _type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_SCOPE, field, "str exacte attendue")
        for field in _STR_REQUIRED
        if type(values[field]) is not str
    ]
    if (
        type(values["scope_context_reference"]) is not str
        and values["scope_context_reference"] is not None
    ):
        refusals.append(
            _refusal(_SCOPE, "scope_context_reference", "str exacte ou None déclaré attendu")
        )
    if type(values["row_count"]) is not int:
        refusals.append(
            _refusal(_SCOPE, "row_count", "int exact attendu")
        )
    if type(values["size_bytes"]) is not int:
        refusals.append(
            _refusal(_SCOPE, "size_bytes", "int exact attendu")
        )
    if type(values["expires_at"]) is not datetime:
        refusals.append(
            _refusal(_SCOPE, "expires_at", "datetime exact attendu")
        )
    elif values["expires_at"].tzinfo is not timezone.utc:
        refusals.append(
            _refusal(_SCOPE, "expires_at", "datetime exact aware UTC attendu")
        )
    if type(values["complete"]) is not bool:
        refusals.append(
            _refusal(_SCOPE, "complete", "bool exact attendu")
        )
    return refusals


def _value_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in _STR_REQUIRED:
        if not _is_runtime_text(values[field]):
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "texte runtime UTF-8 strict non vide sans NUL attendu",
                )
            )
    if values["scope_context_reference"] is not None and not _is_runtime_text(
        values["scope_context_reference"]
    ):
        refusals.append(
            _refusal(
                _SCOPE,
                "scope_context_reference",
                "texte runtime UTF-8 strict non vide sans NUL attendu",
            )
        )
    if values["manifest_version"] != "1.0.0":
        refusals.append(
            _refusal(_SCOPE, "manifest_version", "1.0.0 exact attendu")
        )
    if not _is_complete_semver(values["mapping_version"]):
        refusals.append(
            _refusal(
                _SCOPE,
                "mapping_version",
                "version SemVer complète exacte attendue",
            )
        )
    if values["format"] not in _FORMATS:
        refusals.append(
            _refusal(
                _SCOPE, "format", "valeur texte canonique exacte attendue"
            )
        )
    if values["consistency_kind"] not in _KINDS:
        refusals.append(
            _refusal(
                _SCOPE, "consistency_kind", "valeur texte canonique exacte attendue"
            )
        )
    if _SHA256_PATTERN.fullmatch(values["sha256"]) is None:
        refusals.append(
            _refusal(
                _SCOPE,
                "sha256",
                "empreinte SHA-256 hex minuscule de 64 caractères attendue",
            )
        )
    for field in ("row_count", "size_bytes"):
        if values[field] < 0:
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "entier exact supérieur ou égal à zéro attendu",
                )
            )
    return refusals


def _prepare(
    candidate: object,
) -> tuple[dict | None, list[Diagnostic]]:
    """Mapping exact puis types et UTC avant toute valeur ou comportement."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "dix-sept clés exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return None, _pack(type_refusals)
    return values, []


def validate_bulk_export_manifest_values(
    candidate: object,
) -> list[Diagnostic]:
    """Refuse les types étrangers avant tout comportement, puis contrôle strict."""
    values, prepared = _prepare(candidate)
    if values is None:
        return prepared
    return _pack(_value_refusals(values))


def capture_bulk_export_manifest_values(
    candidate: object,
) -> tuple[_ExportManifestBound | None, list[Diagnostic]]:
    """Capture owned immuable ou refuse sans capture partielle."""
    values, prepared = _prepare(candidate)
    if values is None:
        return None, prepared
    packed = _pack(_value_refusals(values))
    if packed:
        return None, packed
    return (
        _ExportManifestBound(
            manifest_version=values["manifest_version"],
            operation_id=values["operation_id"],
            format=values["format"],
            mapping_reference=values["mapping_reference"],
            mapping_version=values["mapping_version"],
            tenant_context_reference=values["tenant_context_reference"],
            scope_context_reference=values["scope_context_reference"],
            consistency_kind=values["consistency_kind"],
            consistency_reference=values["consistency_reference"],
            row_count=values["row_count"],
            size_bytes=values["size_bytes"],
            sha256=values["sha256"],
            classification_reference=values["classification_reference"],
            expires_at=values["expires_at"],
            object_reference=values["object_reference"],
            object_version=values["object_version"],
            complete=values["complete"],
        ),
        [],
    )
