"""Profil interne préparatoire BulkOperationFormat v1 et validation pure.

Le format canonique est conservé sans parsing, conversion, résolution
d'adaptateur, validité de contenu, compatibilité, autorisation ou persistance.
"""

from dataclasses import dataclass

from .bulk_operations import BulkReferenceFormat
from .diagnostics import VALIDATE, Diagnostic

__all__ = ["BulkOperationFormat", "validate_bulk_operation_format"]

_MISSING = object()


@dataclass(frozen=True)
class BulkOperationFormat:
    operation_id: str
    format: BulkReferenceFormat


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_operation_format.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_operation_format(candidate: object) -> list[Diagnostic]:
    """Valide les types et membres exacts, sans effet ni écho des valeurs."""
    if type(candidate) is not BulkOperationFormat:
        return [_refusal("profile", "profil BulkOperationFormat exact attendu")]

    operation_id = getattr(candidate, "operation_id", _MISSING)
    format_value = getattr(candidate, "format", _MISSING)
    refusals: list[Diagnostic] = []

    if type(operation_id) is not str or not operation_id:
        refusals.append(
            _refusal("operation_id", "référence opaque exacte non vide attendue")
        )

    if type(format_value) is not BulkReferenceFormat or not any(
        format_value is member for member in BulkReferenceFormat
    ):
        refusals.append(
            _refusal("format", "membre canonique BulkReferenceFormat exact attendu")
        )

    return _pack(refusals)
