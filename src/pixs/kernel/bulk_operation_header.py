"""Profil interne préparatoire BulkOperationHeader v1 et validation structurelle pure.

Ce profil conserve trois valeurs explicites sans import/export, persistance,
autorisation, rattachement de Jobs ni décision de compatibilité.
"""

from dataclasses import dataclass

from .bulk_operations import BulkOperationVariant
from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_version

__all__ = ["BulkOperationHeader", "validate_bulk_operation_header"]


@dataclass(frozen=True)
class BulkOperationHeader:
    operation_id: str
    bulk_type: BulkOperationVariant
    bulk_version: str


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"bulk_operation_header.{field}",
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def validate_bulk_operation_header(candidate: object) -> list[Diagnostic]:
    """Valide les types exacts puis la version, sans effet ni écho."""
    if type(candidate) is not BulkOperationHeader:
        return [_refusal("header", "entête BulkOperationHeader exact attendu")]

    operation_id = getattr(candidate, "operation_id", None)
    bulk_type = getattr(candidate, "bulk_type", None)
    bulk_version = getattr(candidate, "bulk_version", None)
    refusals: list[Diagnostic] = []

    if type(operation_id) is not str or not operation_id:
        refusals.append(
            _refusal("operation_id", "référence opaque exacte non vide attendue")
        )

    if type(bulk_type) is not BulkOperationVariant or not any(
        bulk_type is member for member in BulkOperationVariant
    ):
        refusals.append(
            _refusal("bulk_type", "membre BulkOperationVariant exact attendu")
        )

    if type(bulk_version) is not str:
        refusals.append(
            _refusal("bulk_version", "version SemVer 2.0.0 complète exacte attendue")
        )
    else:
        try:
            parse_version(bulk_version)
        except ValueError:
            refusals.append(
                _refusal("bulk_version", "version SemVer 2.0.0 complète exacte attendue")
            )

    return _pack(refusals)
