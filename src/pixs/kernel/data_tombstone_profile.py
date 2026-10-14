"""Représentation interne, immuable et purement mémoire du profil tombstone-v1.

Le requirement « Profil structurel préparatoire de tombstone v1 » de
openspec/specs/data-lifecycle/spec.md fixe les huit champs et leur validation
strictement structurelle. Les références restent opaques, sans normalisation
ni résolution ; les None explicites ne valent aucune autorisation, exemption
de rétention ni décision d'applicabilité. Cette unité ne supprime, ne purge,
ne persiste, ne propage, ne reconstruit et ne restaure rien, et ne lit aucune
horloge.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, time

from .diagnostics import VALIDATE, Diagnostic

__all__ = [
    "TombstoneProfile",
    "validate_data_tombstone_profile",
]

_OPTIONAL_REFERENCE_FIELDS = (
    "tenant_id",
    "scope_id",
    "retention_reference",
    "synchronization_reference",
    "deduplication_reference",
)

_INSTANT_PATTERN = re.compile(
    r"\A(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    r"T(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.[0-9]{1,6})?(?:Z|[+]00:00)\Z"
)


@dataclass(frozen=True)
class TombstoneProfile:
    resource_reference: str
    deletion_version: int
    deleted_at: str
    tenant_id: str | None
    scope_id: str | None
    retention_reference: str | None
    synchronization_reference: str | None
    deduplication_reference: str | None


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"data_tombstone_profile.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque(value: object) -> bool:
    return type(value) is str and bool(value)


def _is_none_or_opaque(value: object) -> bool:
    return value is None or (type(value) is str and bool(value))


def _is_valid_instant(value: object) -> bool:
    if type(value) is not str:
        return False
    matched = _INSTANT_PATTERN.fullmatch(value)
    if matched is None:
        return False
    second = int(matched["second"])
    try:
        date(int(matched["year"]), int(matched["month"]), int(matched["day"]))
        time(int(matched["hour"]), int(matched["minute"]), second)
    except ValueError:
        return False
    return True


def validate_data_tombstone_profile(candidate: object) -> list[Diagnostic]:
    """Valide la structure du profil tombstone-v1, sans écho ni effet."""
    if type(candidate) is not TombstoneProfile:
        return [_refusal("profile", "profil tombstone-v1 exact attendu")]

    refusals: list[Diagnostic] = []

    if not _is_opaque(candidate.resource_reference):
        refusals.append(
            _refusal(
                "resource_reference",
                "référence opaque exacte non vide attendue",
            )
        )

    if type(candidate.deletion_version) is not int or candidate.deletion_version < 0:
        refusals.append(
            _refusal(
                "deletion_version",
                "entier exact supérieur ou égal à zéro attendu",
            )
        )

    if not _is_valid_instant(candidate.deleted_at):
        refusals.append(
            _refusal(
                "deleted_at",
                "instant calendaire UTC exact au format YYYY-MM-DDTHH:MM:SS"
                " avec fraction optionnelle et suffixe Z ou +00:00 attendu",
            )
        )

    for field in _OPTIONAL_REFERENCE_FIELDS:
        if not _is_none_or_opaque(getattr(candidate, field)):
            refusals.append(
                _refusal(
                    field,
                    "None exact ou référence opaque str exacte non vide attendue",
                )
            )

    if candidate.scope_id is not None and candidate.tenant_id is None:
        refusals.append(
            _refusal(
                "scope_context",
                "scope sans tenant explicite refusé",
            )
        )

    return _pack(refusals)
