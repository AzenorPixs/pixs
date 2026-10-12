"""Profil interne préparatoire BulkOperationStatus v1 et validation structurelle pure.

Ce profil conserve deux valeurs explicites sans état réel, transition,
terminalité, autorisation, rattachement de Jobs ni persistance.
"""

from dataclasses import dataclass

from .bulk_operations import BulkOperationState
from .diagnostics import VALIDATE, Diagnostic

__all__ = ["BulkOperationStatus", "validate_bulk_operation_status"]


@dataclass(frozen=True)
class BulkOperationStatus:
    operation_id: str
    status: BulkOperationState


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_operation_status.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_operation_status(candidate: object) -> list[Diagnostic]:
    """Valide les types exacts sans effet, interprétation d'état ni écho."""
    if type(candidate) is not BulkOperationStatus:
        return [_refusal("profile", "profil BulkOperationStatus exact attendu")]

    operation_id = getattr(candidate, "operation_id", None)
    status = getattr(candidate, "status", None)
    refusals: list[Diagnostic] = []

    if type(operation_id) is not str or not operation_id:
        refusals.append(
            _refusal("operation_id", "référence opaque exacte non vide attendue")
        )

    if type(status) is not BulkOperationState or not any(
        status is member for member in BulkOperationState
    ):
        refusals.append(
            _refusal("status", "membre BulkOperationState exact attendu")
        )

    return _pack(refusals)
