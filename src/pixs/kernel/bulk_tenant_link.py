"""Profil interne préparatoire BulkTenantLink v1 et validation structurelle pure.

Deux références opaques explicites, y compris égales, sont conservées sans
résolution, rattachement réel, autorisation, propagation ou persistance.
Aucun contexte concret pixs.core n’est importé ou interprété.
"""

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic

__all__ = ["BulkTenantLink", "validate_bulk_tenant_link"]

_FIELDS = ("operation_id", "tenant_context_reference")
_MISSING = object()


@dataclass(frozen=True)
class BulkTenantLink:
    operation_id: str
    tenant_context_reference: str


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_tenant_link.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_tenant_link(candidate: object) -> list[Diagnostic]:
    """Valide le type exact puis les références, sans effet ni écho."""
    if type(candidate) is not BulkTenantLink:
        return [_refusal("link", "lien BulkTenantLink exact attendu")]

    values = tuple(getattr(candidate, field, _MISSING) for field in _FIELDS)
    refusals: list[Diagnostic] = []
    for field, value in zip(_FIELDS, values):
        if type(value) is not str or not value:
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )

    return _pack(refusals)
