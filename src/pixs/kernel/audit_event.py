"""Représentation structurelle minimale d'un événement d'audit.

Le modèle est purement mémoire, sans persistance, sans wire format, sans
classification de secret et sans obligation runtime de corrélation ou de
causalité. Les références sont fournies par un caller trusted ou par des
fixtures synthétiques. La validation vérifie seulement la forme déclarée par
la norme canonique ``audit`` ; elle ne prouve ni une légitimité métier, ni une
minimisation, ni une administration, ni une auditabilité durable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_requirement, parse_version

__all__ = [
    "AuditEvent",
    "validate_audit_event",
]

_REQUIRED_OPAQUE_FIELDS = (
    "event_id",
    "actor_reference",
    "action",
    "resource_type",
    "resource_id",
    "result",
)

_OPTIONAL_OPAQUE_FIELDS = (
    "tenant_reference",
    "reason_or_error",
)

_CORRELATION_FIELDS = (
    "correlation_ids",
    "causation_ids",
)

_TIMESTAMP_PATTERN = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})"
    r"T([0-9]{2}):([0-9]{2}):([0-9]{2})"
    r"(?:\.([0-9]{1,6}))?"
    r"(?:Z|\+00:00)"
)


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    occurred_at: str
    actor_reference: str
    tenant_reference: str | None
    action: str
    resource_type: str
    resource_id: str
    result: str
    reason_or_error: str | None
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]
    component_id: str
    component_version: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"audit_event.{field}",
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


def _is_optional_opaque(value: object) -> bool:
    return value is None or (type(value) is str and bool(value))


def _is_opaque_tuple(value: object) -> bool:
    if type(value) is not tuple:
        return False
    return all(type(item) is str and bool(item) for item in value)


def _is_utc_instant(value: object) -> bool:
    if type(value) is not str:
        return False

    match = _TIMESTAMP_PATTERN.fullmatch(value)
    if match is None:
        return False

    hour = int(match.group(4))
    minute = int(match.group(5))
    second = int(match.group(6))
    if hour > 23 or minute > 59 or second > 59:
        return False

    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return False

    return parsed.utcoffset() == timezone.utc.utcoffset(None)


def _is_component_id(value: object) -> bool:
    if not _is_opaque(value):
        return False
    try:
        requirement = parse_requirement(value)
    except ValueError:
        return False
    return requirement.constraints == () and requirement.target_id == value


def _is_component_version(value: object) -> bool:
    if not _is_opaque(value):
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def validate_audit_event(event: object) -> list[Diagnostic]:
    """Valide la structure d'un événement d'audit, sans écho ni effet."""
    if type(event) is not AuditEvent:
        return [_refusal("event", "événement d'audit exact attendu")]

    refusals: list[Diagnostic] = []

    for field in _REQUIRED_OPAQUE_FIELDS:
        if not _is_opaque(getattr(event, field)):
            refusals.append(
                _refusal(field, "référence opaque exacte non vide attendue")
            )

    if not _is_utc_instant(event.occurred_at):
        refusals.append(_refusal("occurred_at", "horodatage UTC borné attendu"))

    for field in _OPTIONAL_OPAQUE_FIELDS:
        if not _is_optional_opaque(getattr(event, field)):
            refusals.append(
                _refusal(
                    field,
                    "valeur ``None`` ou référence opaque exacte non vide attendue",
                )
            )

    for field in _CORRELATION_FIELDS:
        if not _is_opaque_tuple(getattr(event, field)):
            refusals.append(
                _refusal(
                    field,
                    "tuple de références opaques exactes non vides attendu",
                )
            )

    if not _is_component_id(event.component_id):
        refusals.append(
            _refusal("component_id", "identifiant de composant nu attendu")
        )

    if not _is_component_version(event.component_version):
        refusals.append(
            _refusal(
                "component_version",
                "version SemVer 2.0.0 complète attendue",
            )
        )

    return _pack(refusals)
