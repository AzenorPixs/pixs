"""Profil interne préparatoire BulkOperationCommitMode v1 et validation pure.

Le mode canonique est conservé sans choix, application, transaction, mutation,
découpage, staging, autorisation, persistance ni import/export.
"""

from dataclasses import dataclass

from .bulk_operations import BulkCommitMode
from .diagnostics import VALIDATE, Diagnostic

__all__ = ["BulkOperationCommitMode", "validate_bulk_operation_commit_mode"]

_MISSING = object()


@dataclass(frozen=True)
class BulkOperationCommitMode:
    operation_id: str
    commit_mode: BulkCommitMode


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_operation_commit_mode.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_operation_commit_mode(candidate: object) -> list[Diagnostic]:
    """Valide les types et membres exacts, sans effet ni écho des valeurs."""
    if type(candidate) is not BulkOperationCommitMode:
        return [_refusal("profile", "profil BulkOperationCommitMode exact attendu")]

    operation_id = getattr(candidate, "operation_id", _MISSING)
    mode_value = getattr(candidate, "commit_mode", _MISSING)
    refusals: list[Diagnostic] = []

    if type(operation_id) is not str or not operation_id:
        refusals.append(
            _refusal("operation_id", "référence opaque exacte non vide attendue")
        )

    if type(mode_value) is not BulkCommitMode or not any(
        mode_value is member for member in BulkCommitMode
    ):
        refusals.append(
            _refusal("commit_mode", "membre canonique BulkCommitMode exact attendu")
        )

    return _pack(refusals)
