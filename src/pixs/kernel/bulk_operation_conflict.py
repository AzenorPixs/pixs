"""Profil interne préparatoire BulkOperationConflict v1 et validation pure.

La stratégie canonique est conservée sans choix, application, résolution de
conflit, mutation, idempotence, autorisation ou persistance.
"""

from dataclasses import dataclass

from .bulk_operations import BulkConflictStrategy
from .diagnostics import VALIDATE, Diagnostic

__all__ = ["BulkOperationConflict", "validate_bulk_operation_conflict"]

_MISSING = object()


@dataclass(frozen=True)
class BulkOperationConflict:
    operation_id: str
    conflict_strategy: BulkConflictStrategy


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_operation_conflict.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_operation_conflict(candidate: object) -> list[Diagnostic]:
    """Valide les types et membres exacts, sans effet ni écho des valeurs."""
    if type(candidate) is not BulkOperationConflict:
        return [_refusal("profile", "profil BulkOperationConflict exact attendu")]

    operation_id = getattr(candidate, "operation_id", _MISSING)
    strategy_value = getattr(candidate, "conflict_strategy", _MISSING)
    refusals: list[Diagnostic] = []

    if type(operation_id) is not str or not operation_id:
        refusals.append(
            _refusal("operation_id", "référence opaque exacte non vide attendue")
        )

    if type(strategy_value) is not BulkConflictStrategy or not any(
        strategy_value is member for member in BulkConflictStrategy
    ):
        refusals.append(
            _refusal("conflict_strategy", "membre canonique BulkConflictStrategy exact attendu")
        )

    return _pack(refusals)
