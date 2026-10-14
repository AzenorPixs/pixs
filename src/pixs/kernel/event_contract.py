"""Représentation déclarative partielle des contrats d'événement du Kernel.

Les valeurs des champs sont fournies par un caller trusted ou par des fixtures
synthétiques. La validation vérifie seulement la structure déclarative exigée
par la norme canonique ``events`` ; elle ne prouve ni la légitimité, ni
l'existence, ni la résolution, ni la classification de sensibilité d'une
référence, et ne constitue pas une minimisation.

Cette représentation ne remplace pas l'enregistrement, ``ContractDescriptor``
ni les garanties documentées d'un contrat public. Elle ne définit aucune
instance, aucun payload, aucune enveloppe complète, aucun wire format, aucune
persistance, aucune publication, aucune audience effective, aucun schéma
effectif, aucun ordre effectif, aucune exposition réelle vers l'extérieur,
aucune outbox, aucune transaction, aucune idempotence, aucun publisher et
aucun runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_version

__all__ = [
    "DomainEventContract",
    "IntegrationEventContract",
    "validate_domain_event_contract",
    "validate_integration_event_contract",
]

_OPAQUE_FIELDS = (
    "event_type",
    "producer_reference",
    "schema_reference",
    "order_scope_reference",
)


@dataclass(frozen=True)
class DomainEventContract:
    event_type: str
    contract_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str


@dataclass(frozen=True)
class IntegrationEventContract:
    event_type: str
    contract_version: str
    producer_reference: str
    schema_reference: str
    order_scope_reference: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"event_contract.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque_reference(value: object) -> bool:
    return type(value) is str and bool(value)


def _is_contract_version(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _validate(event: object, expected: type, rule: str) -> list[Diagnostic]:
    if type(event) is not expected:
        return [_refusal("event", rule)]

    refusals: list[Diagnostic] = []

    for field in _OPAQUE_FIELDS:
        if not _is_opaque_reference(getattr(event, field)):
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )

    if not _is_contract_version(event.contract_version):
        refusals.append(
            _refusal("contract_version", "version SemVer 2.0.0 complète attendue")
        )

    return _pack(refusals)


def validate_domain_event_contract(event: object) -> list[Diagnostic]:
    """Valide la structure déclarative d'un contrat de domaine, sans écho."""
    return _validate(
        event,
        DomainEventContract,
        "contrat de domaine exact attendu",
    )


def validate_integration_event_contract(event: object) -> list[Diagnostic]:
    """Valide la structure déclarative d'un contrat d'intégration, sans écho."""
    return _validate(
        event,
        IntegrationEventContract,
        "contrat d'intégration exact attendu",
    )
