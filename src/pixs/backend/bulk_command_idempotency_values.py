"""Validation et capture pures des valeurs CommandIdempotencyV1, sans effet.

Entrée fermée aux 12 clés normatives du schéma logique CommandIdempotencyV1,
types exacts avant tout comportement, puis contrôles fermés mémoire. Aucune
persistance, transaction, horloge, port, catalogue, autorisation, purge, retry,
fenêtre, hold, commit, CAS ou cohérence inventée. IN_PROGRESS accepté comme les
autres états, sans engagement.
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
    "validate_bulk_command_idempotency_values",
    "capture_bulk_command_idempotency_values",
]

_SCOPE = "bulk_command_idempotency_values"

_FIELDS = (
    "tenant_id",
    "subject_id",
    "command_type",
    "idempotency_key",
    "content_sha256",
    "serializer_version",
    "state",
    "result_reference",
    "failure_code",
    "created_at",
    "expires_at",
    "revision",
)

_STR_REQUIRED = (
    "tenant_id",
    "subject_id",
    "command_type",
    "idempotency_key",
    "content_sha256",
    "serializer_version",
    "state",
)

_STR_OR_NONE = (
    "result_reference",
    "failure_code",
)

_STATES = frozenset({"IN_PROGRESS", "SUCCEEDED", "REJECTED"})

_SHA256_PATTERN = re.compile("[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class _CommandIdempotencyBound:
    tenant_id: str
    subject_id: str
    command_type: str
    idempotency_key: str
    content_sha256: str
    serializer_version: str
    state: str
    result_reference: str | None
    failure_code: str | None
    created_at: datetime
    expires_at: datetime
    revision: int


def _type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_SCOPE, field, "str exacte attendue")
        for field in _STR_REQUIRED
        if type(values[field]) is not str
    ]
    refusals.extend(
        _refusal(_SCOPE, field, "str exacte ou None déclaré attendu")
        for field in _STR_OR_NONE
        if type(values[field]) is not str and values[field] is not None
    )
    for field in ("created_at", "expires_at"):
        if type(values[field]) is not datetime:
            refusals.append(
                _refusal(_SCOPE, field, "datetime exact attendu")
            )
        elif values[field].tzinfo is not timezone.utc:
            refusals.append(
                _refusal(_SCOPE, field, "datetime exact aware UTC attendu")
            )
    if type(values["revision"]) is not int:
        refusals.append(
            _refusal(_SCOPE, "revision", "int exact attendu")
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
    for field in _STR_OR_NONE:
        value = values[field]
        if value is not None and not _is_runtime_text(value):
            refusals.append(
                _refusal(
                    _SCOPE,
                    field,
                    "texte runtime UTF-8 strict non vide sans NUL attendu",
                )
            )
    if _SHA256_PATTERN.fullmatch(values["content_sha256"]) is None:
        refusals.append(
            _refusal(
                _SCOPE,
                "content_sha256",
                "empreinte SHA-256 hex minuscule de 64 caractères attendue",
            )
        )
    if not _is_complete_semver(values["serializer_version"]):
        refusals.append(
            _refusal(
                _SCOPE,
                "serializer_version",
                "version SemVer complète exacte attendue",
            )
        )
    if values["state"] not in _STATES:
        refusals.append(
            _refusal(
                _SCOPE, "state", "valeur texte canonique exacte attendue"
            )
        )
    if values["revision"] < 1:
        refusals.append(
            _refusal(
                _SCOPE,
                "revision",
                "entier exact supérieur ou égal à un attendu",
            )
        )
    for field in ("created_at", "expires_at"):
        if values[field].tzinfo is not timezone.utc:
            refusals.append(
                _refusal(_SCOPE, field, "datetime exact aware UTC attendu")
            )
    return refusals


def _prepare(
    candidate: object,
) -> tuple[dict | None, list[Diagnostic]]:
    """Mapping exact puis types des 12 avant toute valeur ou comportement."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "douze clés exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return None, _pack(type_refusals)
    return values, []


def validate_bulk_command_idempotency_values(
    candidate: object,
) -> list[Diagnostic]:
    """Refuse les types étrangers avant tout comportement, puis contrôle strict."""
    values, prepared = _prepare(candidate)
    if values is None:
        return prepared
    return _pack(_value_refusals(values))


def capture_bulk_command_idempotency_values(
    candidate: object,
) -> tuple[_CommandIdempotencyBound | None, list[Diagnostic]]:
    """Capture owned immuable ou refuse sans capture partielle."""
    values, prepared = _prepare(candidate)
    if values is None:
        return None, prepared
    packed = _pack(_value_refusals(values))
    if packed:
        return None, packed
    return (
        _CommandIdempotencyBound(
            tenant_id=values["tenant_id"],
            subject_id=values["subject_id"],
            command_type=values["command_type"],
            idempotency_key=values["idempotency_key"],
            content_sha256=values["content_sha256"],
            serializer_version=values["serializer_version"],
            state=values["state"],
            result_reference=values["result_reference"],
            failure_code=values["failure_code"],
            created_at=values["created_at"],
            expires_at=values["expires_at"],
            revision=values["revision"],
        ),
        [],
    )
