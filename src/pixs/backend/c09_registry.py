"""Registre déclaratif C09 : fermé, déterministe, sans exécution."""

from __future__ import annotations

from dataclasses import dataclass

from pixs.backend.c09_contracts import (
    C09ConsumerDeclarationV1,
    C09EventBindingV1,
    C09RoleDeclarationV1,
    validate_c09_consumer_declaration,
    validate_c09_event_binding,
    validate_c09_role_declaration,
)
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

__all__ = [
    "C09RegistryV1",
    "validate_c09_registry",
]


@dataclass(frozen=True, slots=True)
class C09RegistryV1:
    """Registre de rôles, liaisons et consommateurs déclarés."""

    roles: tuple[C09RoleDeclarationV1, ...]
    bindings: tuple[C09EventBindingV1, ...]
    consumers: tuple[C09ConsumerDeclarationV1, ...]


def _refusal(element: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=element,
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_sorted_tuple(values: tuple[str, ...]) -> bool:
    current: str | None = None
    for value in values:
        if current is not None and not current <= value:
            return False
        current = value
    return True


def validate_c09_registry(candidate: object) -> list[Diagnostic]:
    """Valide un registre déclaratif, refus d'abord, sans callback."""
    if type(candidate) is not C09RegistryV1:
        return [_refusal("c09_registry", "registre exact attendu")]
    roles = candidate.roles
    bindings = candidate.bindings
    consumers = candidate.consumers
    if type(roles) is not tuple or type(bindings) is not tuple or type(consumers) is not tuple:
        return [_refusal("c09_registry", "tuples exacts attendus")]
    refusals: list[Diagnostic] = []
    for role in roles:
        for diagnostic in validate_c09_role_declaration(role):
            refusals.append(diagnostic)
    for binding in bindings:
        for diagnostic in validate_c09_event_binding(binding):
            refusals.append(diagnostic)
    for consumer in consumers:
        for diagnostic in validate_c09_consumer_declaration(consumer):
            refusals.append(diagnostic)
    if refusals:
        return _pack(refusals)
    role_refs: list[str] = []
    for role in roles:
        role_refs.append(role.handler_reference)
    if len(set(role_refs)) != len(role_refs):
        refusals.append(_refusal("c09_registry.roles", "collision de référence refusée"))
    if role_refs and not _is_sorted_tuple(tuple(role_refs)):
        refusals.append(_refusal("c09_registry.roles", "ordre déterministe trié attendu"))
    entry_refs: list[str] = []
    for binding in bindings:
        entry_refs.append(binding.entry_reference)
    if len(set(entry_refs)) != len(entry_refs):
        refusals.append(_refusal("c09_registry.bindings", "collision de référence refusée"))
    if entry_refs and not _is_sorted_tuple(tuple(entry_refs)):
        refusals.append(_refusal("c09_registry.bindings", "ordre déterministe trié attendu"))
    consumer_refs: list[str] = []
    for consumer in consumers:
        consumer_refs.append(consumer.consumer_reference)
    if len(set(consumer_refs)) != len(consumer_refs):
        refusals.append(_refusal("c09_registry.consumers", "collision de référence refusée"))
    if consumer_refs and not _is_sorted_tuple(tuple(consumer_refs)):
        refusals.append(_refusal("c09_registry.consumers", "ordre déterministe trié attendu"))
    if refusals:
        return _pack(refusals)
    by_entry: dict[str, C09EventBindingV1] = {}
    for binding in bindings:
        by_entry[binding.entry_reference] = binding
    for consumer in consumers:
        linked = by_entry.get(consumer.entry_reference)
        if linked is None:
            refusals.append(
                _refusal("c09_registry.consumers", "liaison manquante refusée")
            )
        elif consumer.event_contract_version != linked.contract.contract_version:
            refusals.append(
                _refusal("c09_registry.consumers", "version incompatible refusée")
            )
    return _pack(refusals)
