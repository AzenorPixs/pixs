"""Référence préparatoire de déduplication des travaux.

Le profil `JobDeduplicationReferenceV1` porte seulement les
références opaques `deduplication_key` et `perimeter_reference`.
Il ne compare aucune unicité, ne résout rien, ne stocke rien,
ne fixe aucune rétention et n'envoie rien. Le validateur contrôle
seulement la structure exacte, sans normalisation ni effet.
"""
from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic


__all__ = [
    "JobDeduplicationReferenceV1",
    "validate_job_deduplication_reference",
]


@dataclass(frozen=True)
class JobDeduplicationReferenceV1:
    deduplication_key: str
    perimeter_reference: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"job_deduplication_reference.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (
            diagnostic.element,
            diagnostic.constraint,
            diagnostic.message,
        )
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque(value: object) -> bool:
    return type(value) is str and bool(value)


def validate_job_deduplication_reference(
    candidate: object,
) -> list[Diagnostic]:
    """Valide la structure exacte d'une référence, sans écho ni effet."""
    if type(candidate) is not JobDeduplicationReferenceV1:
        return [
            _refusal("reference", "profil de déduplication exact attendu")
        ]
    refusals: list[Diagnostic] = []
    if not _is_opaque(candidate.deduplication_key):
        refusals.append(
            _refusal(
                "deduplication_key",
                "référence opaque exacte non vide attendue",
            )
        )
    if not _is_opaque(candidate.perimeter_reference):
        refusals.append(
            _refusal(
                "perimeter_reference",
                "référence opaque exacte non vide attendue",
            )
        )
    return _pack(refusals)
