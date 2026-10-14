"""Représentation déclarative interne et partielle d'une demande relative aux données.

Les onze champs suivent TECHNICAL §14.6. Le validateur contrôle uniquement
la structure, sans interpréter les références ni les None explicites des
champs éventuels. Cette unité ne fournit aucun traitement de demande.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data_subject_operations import DataSubjectOperation
from .diagnostics import VALIDATE, Diagnostic

__all__ = [
    "DataSubjectRequest",
    "validate_data_subject_request",
]

_REQUIRED_OPAQUE_FIELDS = (
    "request_id",
    "subject_reference",
    "requested_by",
    "status",
    "policy_version",
)

_OPTIONAL_FIELDS = (
    "tenant_id",
    "scope_id",
    "operation_id",
    "legal_hold_decision",
    "result_reference",
)


@dataclass(frozen=True)
class DataSubjectRequest:
    request_id: str
    operation: DataSubjectOperation
    subject_reference: str
    tenant_id: str | None
    scope_id: str | None
    requested_by: str
    status: str
    policy_version: str
    operation_id: str | None
    legal_hold_decision: str | None
    result_reference: str | None


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"data_subject_request.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_opaque(value: object) -> bool:
    return type(value) is str and bool(value)


def _is_none_or_opaque(value: object) -> bool:
    return value is None or (type(value) is str and bool(value))


def _is_canonical_operation(value: object) -> bool:
    return any(member is value for member in DataSubjectOperation)


def validate_data_subject_request(candidate: object) -> list[Diagnostic]:
    """Valide la structure déclarative interne d'une demande relative aux
    données, sans écho ni effet."""
    if type(candidate) is not DataSubjectRequest:
        return [_refusal("request", "demande exacte attendue")]

    refusals: list[Diagnostic] = []

    if not _is_canonical_operation(candidate.operation):
        refusals.append(
            _refusal("operation", "membre DataSubjectOperation canonique attendu")
        )
    for field in _REQUIRED_OPAQUE_FIELDS:
        if not _is_opaque(getattr(candidate, field)):
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )
    for field in _OPTIONAL_FIELDS:
        if not _is_none_or_opaque(getattr(candidate, field)):
            refusals.append(
                _refusal(
                    field,
                    "None exact ou référence opaque str exacte non vide attendue",
                )
            )

    return _pack(refusals)
