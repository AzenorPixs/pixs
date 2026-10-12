"""Représentation déclarative interne et partielle d'une déclaration de flux
sortant.

Les trois champs suivent le scénario canonique data-governance « Flux sortant
sans consommateur refusé ». Le validateur contrôle uniquement la structure,
sans interpréter les références ni les None explicites des champs éventuels.
Cette unité ne fournit aucune activation, aucun runtime, aucun audit, aucune
résolution de consommateur ou de garantie.
"""

from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic

__all__ = [
    "DataOutboundDeclaration",
    "validate_data_outbound_declaration",
]

_OPTIONAL_FIELDS = (
    "consumer_reference",
    "guarantee_reference",
)


@dataclass(frozen=True)
class DataOutboundDeclaration:
    destination_reference: str
    consumer_reference: str | None
    guarantee_reference: str | None


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"data_outbound_declaration.{field}",
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


def validate_data_outbound_declaration(candidate: object) -> list[Diagnostic]:
    """Valide la structure déclarative interne d'un flux sortant, sans écho
    ni effet."""
    if type(candidate) is not DataOutboundDeclaration:
        return [
            _refusal("declaration", "déclaration de transfert exacte attendue")
        ]

    refusals: list[Diagnostic] = []

    if not _is_opaque(candidate.destination_reference):
        refusals.append(
            _refusal(
                "destination_reference",
                "référence opaque exacte non vide attendue",
            )
        )
    for field in _OPTIONAL_FIELDS:
        if not _is_none_or_opaque(getattr(candidate, field)):
            refusals.append(
                _refusal(
                    field,
                    "None exact ou référence opaque str exacte non vide attendue",
                )
            )
    if (
        candidate.consumer_reference is None
        and candidate.guarantee_reference is None
    ):
        refusals.append(
            _refusal(
                "outbound_flow",
                "transfert sans consommateur ni garantie documentée refusé",
            )
        )

    return _pack(refusals)
