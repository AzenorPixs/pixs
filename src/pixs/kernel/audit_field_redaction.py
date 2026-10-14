"""Représentation interne, immuable et purement mémoire du profil
d'occultation de champ d'audit v1.

Le requirement « Profil structurel préparatoire d'occultation de champ
d'audit v1 » de openspec/specs/audit/spec.md fixe les trois champs et leur
validation strictement structurelle. Les références restent opaques, sans
normalisation ni résolution ; les None explicites ne valent aucune
autorisation, exemption de rétention ni décision d'applicabilité. Ce module
ne réalise aucune occultation, pseudonymisation ou minimisation effective,
n'inspecte aucun payload avant/après, ne consulte aucune classification et
ne persiste aucun événement d'audit.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .diagnostics import VALIDATE, Diagnostic

__all__ = [
    "RedactionMode",
    "AuditFieldRedaction",
    "validate_audit_field_redaction",
]


class RedactionMode(Enum):
    """Deux modes structurels fermés d'un champ d'audit."""

    REDACTED = "REDACTED"
    PSEUDONYMIZED_REFERENCE = "PSEUDONYMIZED_REFERENCE"


@dataclass(frozen=True)
class AuditFieldRedaction:
    field_reference: str
    mode: RedactionMode
    replacement_reference: str | None


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"audit_field_redaction.{field}",
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


def _is_exact_mode(value: object) -> bool:
    return (
        value is RedactionMode.REDACTED
        or value is RedactionMode.PSEUDONYMIZED_REFERENCE
    )


def validate_audit_field_redaction(candidate: object) -> list[Diagnostic]:
    """Valide la structure du profil d'occultation v1, sans écho ni effet."""
    if type(candidate) is not AuditFieldRedaction:
        return [_refusal("candidate", "profil d'occultation de champ exact attendu")]

    refusals: list[Diagnostic] = []

    if not _is_opaque(candidate.field_reference):
        refusals.append(
            _refusal(
                "field_reference",
                "référence de champ opaque str exacte non vide attendue",
            )
        )

    if not _is_exact_mode(candidate.mode):
        refusals.append(
            _refusal(
                "mode",
                "membre exact de l'Enum fermé RedactionMode attendu",
            )
        )

    if candidate.mode is RedactionMode.REDACTED:
        if candidate.replacement_reference is not None:
            refusals.append(
                _refusal(
                    "replacement_reference",
                    "None explicite attendue en mode REDACTED",
                )
            )
    elif candidate.mode is RedactionMode.PSEUDONYMIZED_REFERENCE:
        if not _is_opaque(candidate.replacement_reference):
            refusals.append(
                _refusal(
                    "replacement_reference",
                    "référence pseudonyme opaque str exacte non vide attendue"
                    " en mode PSEUDONYMIZED_REFERENCE",
                )
            )

    return _pack(refusals)
