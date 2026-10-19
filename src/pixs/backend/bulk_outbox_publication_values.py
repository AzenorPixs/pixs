"""Garde et capture pures des valeurs OutboxPublicationV1, sans effet.

Entree fermee aux 12 cles normatives du schema logique OutboxPublicationV1,
types exacts avant tout comportement, puis controles fermes memoire. Aucune
persistance, publication, catalogue, autorisation, horloge, comparaison de
dates, politique serveur, FK, unicite, allocation de sequence, retry, CAS,
SQL ni preuve serveur. PENDING explicite et compteur 0 restent des valeurs
de l appelant, sans defaut ni restriction historique.
"""

from __future__ import annotations

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
    "validate_bulk_outbox_publication_values",
    "capture_bulk_outbox_publication_values",
]

_SCOPE = "bulk_outbox_publication_values"

_FIELDS = (
    "event_id",
    "state",
    "attempt_count",
    "lease_owner",
    "lease_expires_at",
    "next_attempt_at",
    "published_at",
    "failure_code",
    "sequence_index",
    "policy_reference",
    "policy_version",
    "revision",
)

_STR_REQUIRED = (
    "event_id",
    "state",
    "policy_reference",
    "policy_version",
)

_STR_OR_NONE = (
    "lease_owner",
    "failure_code",
)

_INT_FIELDS = (
    "attempt_count",
    "sequence_index",
    "revision",
)

_DATETIME_OR_NONE = (
    "lease_expires_at",
    "next_attempt_at",
    "published_at",
)

_STATES = frozenset({"PENDING", "PUBLISHED", "RETRYING", "FAILED", "DEAD_LETTER"})


@dataclass(frozen=True, slots=True)
class _OutboxPublicationBound:
    event_id: str
    state: str
    attempt_count: int
    lease_owner: str | None
    lease_expires_at: datetime | None
    next_attempt_at: datetime | None
    published_at: datetime | None
    failure_code: str | None
    sequence_index: int
    policy_reference: str
    policy_version: str
    revision: int


def _type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_SCOPE, field, "str exacte attendue")
        for field in _STR_REQUIRED
        if type(values[field]) is not str
    ]
    refusals.extend(
        _refusal(_SCOPE, field, "str exacte ou None declare attendu")
        for field in _STR_OR_NONE
        if type(values[field]) is not str and values[field] is not None
    )
    refusals.extend(
        _refusal(_SCOPE, field, "int exact attendu")
        for field in _INT_FIELDS
        if type(values[field]) is not int
    )
    for field in _DATETIME_OR_NONE:
        value = values[field]
        if value is not None and type(value) is not datetime:
            refusals.append(
                _refusal(_SCOPE, field, "datetime exact ou None declare attendu")
            )
        elif type(value) is datetime and value.tzinfo is not timezone.utc:
            refusals.append(
                _refusal(_SCOPE, field, "datetime exact aware UTC attendu")
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
    if not _is_complete_semver(values["policy_version"]):
        refusals.append(
            _refusal(
                _SCOPE,
                "policy_version",
                "version SemVer complete exacte attendue",
            )
        )
    if values["state"] not in _STATES:
        refusals.append(
            _refusal(_SCOPE, "state", "valeur texte canonique exacte attendue")
        )
    if values["attempt_count"] < 0:
        refusals.append(
            _refusal(
                _SCOPE,
                "attempt_count",
                "entier exact superieur ou egal a zero attendu",
            )
        )
    if values["sequence_index"] < 1:
        refusals.append(
            _refusal(
                _SCOPE,
                "sequence_index",
                "entier exact superieur ou egal a un attendu",
            )
        )
    if values["revision"] < 1:
        refusals.append(
            _refusal(
                _SCOPE,
                "revision",
                "entier exact superieur ou egal a un attendu",
            )
        )
    if (values["lease_owner"] is None) != (values["lease_expires_at"] is None):
        refusals.append(
            _refusal(
                _SCOPE,
                "lease_owner",
                "lease_owner et lease_expires_at tous deux None ou presents attendus",
            )
        )
    if values["state"] == "RETRYING" and values["next_attempt_at"] is None:
        refusals.append(
            _refusal(
                _SCOPE,
                "next_attempt_at",
                "next_attempt_at non None attendu pour RETRYING",
            )
        )
    if values["state"] == "PUBLISHED" and values["published_at"] is None:
        refusals.append(
            _refusal(
                _SCOPE,
                "published_at",
                "published_at non None attendu pour PUBLISHED",
            )
        )
    return refusals


def _prepare(
    candidate: object,
) -> tuple[dict | None, list[Diagnostic]]:
    """Mapping exact puis types complets avant toute valeur ou comportement."""
    values, refusals = _exact_mapping(
        candidate, _SCOPE, _FIELDS, "douze cles exactes attendues"
    )
    if values is None:
        return None, _pack(refusals)
    type_refusals = _type_refusals(values)
    if type_refusals:
        return None, _pack(type_refusals)
    return values, []


def validate_bulk_outbox_publication_values(
    candidate: object,
) -> list[Diagnostic]:
    """Refuse les types etrangers avant tout comportement, puis controle strict."""
    values, prepared = _prepare(candidate)
    if values is None:
        return prepared
    return _pack(_value_refusals(values))


def capture_bulk_outbox_publication_values(
    candidate: object,
) -> tuple[_OutboxPublicationBound | None, list[Diagnostic]]:
    """Capture owned immuable ou refuse sans capture partielle."""
    values, prepared = _prepare(candidate)
    if values is None:
        return None, prepared
    packed = _pack(_value_refusals(values))
    if packed:
        return None, packed
    return (
        _OutboxPublicationBound(
            event_id=values["event_id"],
            state=values["state"],
            attempt_count=values["attempt_count"],
            lease_owner=values["lease_owner"],
            lease_expires_at=values["lease_expires_at"],
            next_attempt_at=values["next_attempt_at"],
            published_at=values["published_at"],
            failure_code=values["failure_code"],
            sequence_index=values["sequence_index"],
            policy_reference=values["policy_reference"],
            policy_version=values["policy_version"],
            revision=values["revision"],
        ),
        [],
    )
