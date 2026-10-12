"""Valeurs préparatoires de BulkOperationRecord v1, validation pure sans ORM.

Le dict explicite est contrôlé sans conversion, normalisation, résolution,
effet de stockage, application de mode ou preuve d'autorisation.
"""

from .bulk_operations import (
    BulkCommitMode,
    BulkConflictStrategy,
    BulkOperationState,
    BulkOperationVariant,
    BulkReferenceFormat,
)
from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_version

__all__ = ["validate_bulk_operation_record_values"]

_FIELDS = (
    "operation_id",
    "bulk_type",
    "bulk_version",
    "status",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
)
_NULLABLE = frozenset(
    {"scope_context_reference", "conflict_strategy", "commit_mode"}
)
_REFERENCES = frozenset(
    {"operation_id", "tenant_context_reference", "scope_context_reference"}
)
_ENUM_VALUES = {
    "bulk_type": frozenset(item.value for item in BulkOperationVariant),
    "status": frozenset(item.value for item in BulkOperationState),
    "format": frozenset(item.value for item in BulkReferenceFormat),
    "conflict_strategy": frozenset(item.value for item in BulkConflictStrategy),
    "commit_mode": frozenset(item.value for item in BulkCommitMode),
}


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_operation_record_values.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_operation_record_values(candidate: object) -> list[Diagnostic]:
    """Refuse d'abord les types étrangers, puis contrôle les valeurs exactes."""
    if type(candidate) is not dict:
        return [_refusal("mapping", "dict exact attendu")]

    items = tuple(candidate.items())
    if any(type(key) is not str for key, _value in items):
        return [_refusal("keys", "clés str exactes attendues")]

    values = dict(items)
    refusals: list[Diagnostic] = []
    invalid_types: set[str] = set()
    if any(key not in _FIELDS for key in values):
        refusals.append(_refusal("mapping", "neuf clés exactes attendues"))
    for field in _FIELDS:
        if field not in values:
            refusals.append(_refusal(field, "champ explicite requis"))
            continue
        value = values[field]
        if type(value) is not str and not (
            field in _NULLABLE and value is None
        ):
            invalid_types.add(field)
            refusals.append(
                _refusal(field, "str exacte ou nullabilité déclarée attendue")
            )

    for field in _FIELDS:
        if field not in values or field in invalid_types:
            continue
        value = values[field]
        if value is None:
            continue
        if field in _REFERENCES and not value:
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )
        if field in _ENUM_VALUES and value not in _ENUM_VALUES[field]:
            refusals.append(
                _refusal(field, "valeur texte canonique exacte attendue")
            )
        if field == "bulk_version":
            try:
                parse_version(value)
            except ValueError:
                refusals.append(
                    _refusal(field, "version SemVer complète exacte attendue")
                )
    return _pack(refusals)
