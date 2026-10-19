"""Validation et capture pures des valeurs InboxReceiptV1, sans effet.

Entrée fermée aux huit clés normatives du schéma logique InboxReceiptV1,
types exacts et UTC avant tout comportement, puis contrôles fermés mémoire.
Aucune persistance, déduplication, transaction, horloge, calcul de hash,
comparaison de version, catalogue, provenance, autorisation, FK, unicité,
cohérence entre champs ni preuve de consommation avant commit.
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
    "validate_bulk_inbox_receipt_values",
    "capture_bulk_inbox_receipt_values",
]

_SCOPE = "bulk_inbox_receipt_values"

_FIELDS = (
    "consumer_reference",
    "event_id",
    "event_version",
    "content_sha256",
    "state",
    "consumed_at",
    "correlation_id",
    "causation_id",
)

_STR_REQUIRED = (
    "consumer_reference",
    "event_id",
    "event_version",
    "content_sha256",
    "state",
    "correlation_id",
)

_STATES = frozenset({"CONSUMED"})

_SHA256_PATTERN = re.compile("[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class _InboxReceiptBound:
    consumer_reference: str
    event_id: str
    event_version: str
    content_sha256: str
    state: str
    consumed_at: datetime
    correlation_id: str
    causation_id: str | None


def _type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_SCOPE, field, "str exacte attendue")
        for field in _STR_REQUIRED
        if type(values[field]) is not str
    ]
    if type(values["causation_id"]) is not str and values["causation_id"] is not None:
        refusals.append(
            _refusal(_SCOPE, "causation_id", "str exacte ou None déclaré attendu")
        )
    if type(values["consumed_at"]) is not datetime:
        refusals.append(
            _refusal(_SCOPE, "consumed_at", "datetime exact attendu")
        )
    elif values["consumed_at"].tzinfo is not timezone.utc:
        refusals.append(
            _refusal(_SCOPE, "consumed_at", "datetime exact aware UTC attendu")
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
    if values["causation_id"] is not None and not _is_runtime_text(
        values["causation_id"]
    ):
        refusals.append(
            _refusal(
                _SCOPE,
                "causation_id",
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
    if not _is_complete_semver(values["event_version"]):
        refusals.append(
            _refusal(
                _SCOPE,
                "event_version",
                "version SemVer complète exacte attendue",
            )
        )
    if values["state"] not in _STATES:
        refusals.append(
            _refusal(
                _SCOPE, "state", "valeur texte canonique exacte attendue"
            )
        )
    return refusals


def _prepare(
    candidate: object,
) -> tuple[dict | None, list[Diagnostic]]:
    """Mapping exact puis types et UTC avant toute valeur ou comportement."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "huit clés exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return None, _pack(type_refusals)
    return values, []


def validate_bulk_inbox_receipt_values(
    candidate: object,
) -> list[Diagnostic]:
    """Refuse les types étrangers avant tout comportement, puis contrôle strict."""
    values, prepared = _prepare(candidate)
    if values is None:
        return prepared
    return _pack(_value_refusals(values))


def capture_bulk_inbox_receipt_values(
    candidate: object,
) -> tuple[_InboxReceiptBound | None, list[Diagnostic]]:
    """Capture owned immuable ou refuse sans capture partielle."""
    values, prepared = _prepare(candidate)
    if values is None:
        return None, prepared
    packed = _pack(_value_refusals(values))
    if packed:
        return None, packed
    return (
        _InboxReceiptBound(
            consumer_reference=values["consumer_reference"],
            event_id=values["event_id"],
            event_version=values["event_version"],
            content_sha256=values["content_sha256"],
            state=values["state"],
            consumed_at=values["consumed_at"],
            correlation_id=values["correlation_id"],
            causation_id=values["causation_id"],
        ),
        [],
    )
