"""Déclaration passive d'enregistrement d'événement v1.

Représentation uniquement structurelle du profil préparatoire
`EventRegistrationDeclarationV1` défini par la norme canonique `events`.
Les valeurs sont fournies par un appelant de confiance ou des fixtures
synthétiques. La validation est explicite, fermée et sans effet : elle ne
prouve ni admission, existence, résolution, légitimité ou sensibilité, et ne
réalise aucun enregistrement, abonnement, publication, livraison, persistance,
outbox, transaction ou bus runtime. Le registre P0 reste fermé.
"""

from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic
from .event_contract import (
    DomainEventContract,
    IntegrationEventContract,
    validate_domain_event_contract,
    validate_integration_event_contract,
)

__all__ = [
    "EventRegistrationDeclarationV1",
    "validate_event_registration_declaration",
]


@dataclass(frozen=True, slots=True)
class EventRegistrationDeclarationV1:
    owner_id: str
    entry_id: str
    event_contract: DomainEventContract | IntegrationEventContract


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"event_registration.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_exact_non_empty_str(value: object) -> bool:
    return type(value) is str and bool(value)


def validate_event_registration_declaration(declaration: object) -> list[Diagnostic]:
    """Valide la structure fermée d'une déclaration, sans écho ni effet."""
    if type(declaration) is not EventRegistrationDeclarationV1:
        return [_refusal("declaration", "déclaration exacte attendue")]

    refusals: list[Diagnostic] = []

    if not _is_exact_non_empty_str(declaration.owner_id):
        refusals.append(
            _refusal("owner_id", "identifiant exact non vide attendu")
        )

    if not _is_exact_non_empty_str(declaration.entry_id):
        refusals.append(
            _refusal("entry_id", "identifiant exact non vide attendu")
        )

    contract = declaration.event_contract
    if type(contract) is DomainEventContract:
        refusals.extend(validate_domain_event_contract(contract))
    elif type(contract) is IntegrationEventContract:
        refusals.extend(validate_integration_event_contract(contract))
    else:
        refusals.append(
            _refusal("event_contract", "contrat exact attendu")
        )

    return _pack(refusals)
