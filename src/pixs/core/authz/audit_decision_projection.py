"""Projection préparatoire décision et audit v1 : contrôle mémoire pur.

AuditDecisionProjectionV1 relie un événement PDP exact et un événement
générique exact déjà fournis, sans persistance, acquittement, exhaustivité
ni conformité P0. La validation réutilise seulement les validateurs publics
``validate_structure`` et ``validate_audit_event`` sur les mêmes objets.
Le constructeur ``AuditEvent`` du PDP n'est jamais rejoué ni utilisé pour
recopier ; ses champs sont vérifiés explicitement selon la projection.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.scope.context import (
    ScopeContext,
    ScopeStructureError,
    ScopeType,
    validate_structure,
)
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent
from pixs.kernel.audit_event import validate_audit_event
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

__all__ = [
    "AuditDecisionProjectionV1",
    "validate_audit_decision_projection",
]


@dataclass(frozen=True, slots=True)
class AuditDecisionProjectionV1:
    decision_event: object
    audit_event: object


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"audit_decision_projection.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        key = (diagnostic.element, diagnostic.constraint, diagnostic.message)
        unique[key] = diagnostic
    return [unique[key] for key in sorted(unique)]


def _is_exact_nonempty_str(value: object) -> bool:
    return type(value) is str and value != ""


def validate_audit_decision_projection(candidate: object) -> list[Diagnostic]:
    """Valide la projection sans écho, sans IO, sans horloge ni mutation."""
    if type(candidate) is not AuditDecisionProjectionV1:
        return [_refusal("candidate", "profil exact attendu")]
    decision = object.__getattribute__(candidate, "decision_event")
    generic = object.__getattribute__(candidate, "audit_event")
    if type(decision) is not PdpAuditEvent or type(generic) is not GenericAuditEvent:
        refusals: list[Diagnostic] = []
        if type(decision) is not PdpAuditEvent:
            refusals.append(_refusal("decision_event", "événement PDP exact attendu"))
        if type(generic) is not GenericAuditEvent:
            refusals.append(_refusal("audit_event", "événement générique exact attendu"))
        return _pack(refusals)
    refusals = []
    decision_id = object.__getattribute__(decision, "decision_id")
    subject_id = object.__getattribute__(decision, "subject_id")
    resource_id = object.__getattribute__(decision, "resource_id")
    action_id = object.__getattribute__(decision, "action_id")
    correlation_id = object.__getattribute__(decision, "correlation_id")
    context = object.__getattribute__(decision, "context")
    effect = object.__getattribute__(decision, "effect")
    reason_code = object.__getattribute__(decision, "reason_code")
    policy_version = object.__getattribute__(decision, "policy_version")
    evaluated_at = object.__getattribute__(decision, "evaluated_at")
    if not _is_exact_nonempty_str(decision_id):
        refusals.append(_refusal("decision_id", "référence opaque exacte non vide attendue"))
    if not _is_exact_nonempty_str(subject_id):
        refusals.append(_refusal("subject_id", "référence opaque exacte non vide attendue"))
    if not _is_exact_nonempty_str(resource_id):
        refusals.append(_refusal("resource_id", "référence opaque exacte non vide attendue"))
    if not _is_exact_nonempty_str(action_id):
        refusals.append(_refusal("action_id", "référence opaque exacte non vide attendue"))
    if not _is_exact_nonempty_str(correlation_id):
        refusals.append(_refusal("correlation_id", "référence opaque exacte non vide attendue"))
    context_ok = True
    if type(context) is not ScopeContext:
        refusals.append(_refusal("context", "contexte exact valide attendu"))
        context_ok = False
    else:
        try:
            validate_structure(context)
        except ScopeStructureError:
            refusals.append(_refusal("context", "contexte exact valide attendu"))
            context_ok = False
    effect_ok = type(effect) is Effect and (effect is Effect.ALLOW or effect is Effect.DENY)
    if not effect_ok:
        refusals.append(_refusal("effect", "effet exact attendu"))
    if type(reason_code) is not str:
        refusals.append(_refusal("reason_code", "motif exact cohérent attendu"))
    elif effect_ok:
        if effect is Effect.ALLOW and reason_code != "ALLOWED":
            refusals.append(_refusal("reason_code", "motif exact cohérent attendu"))
        elif effect is Effect.DENY and reason_code != "DENIED":
            refusals.append(_refusal("reason_code", "motif exact cohérent attendu"))
    elif reason_code != "ALLOWED" and reason_code != "DENIED":
        refusals.append(_refusal("reason_code", "motif exact cohérent attendu"))
    if type(policy_version) is not tuple:
        refusals.append(_refusal("policy_version", "tuple exact non None attendu"))
    if type(evaluated_at) is not datetime.datetime:
        refusals.append(_refusal("evaluated_at", "instant UTC exact attendu"))
    else:
        tzinfo = object.__getattribute__(evaluated_at, "tzinfo")
        if tzinfo is not datetime.timezone.utc:
            refusals.append(_refusal("evaluated_at", "instant UTC exact attendu"))
    generic_diagnostics = validate_audit_event(generic)
    if generic_diagnostics:
        refusals.extend(generic_diagnostics)
        return _pack(refusals)
    if refusals:
        return _pack(refusals)
    occurred_at = object.__getattribute__(generic, "occurred_at")
    parsed = datetime.datetime.fromisoformat(occurred_at)
    if parsed != evaluated_at:
        refusals.append(_refusal("occurred_at", "même instant UTC attendu"))
        return _pack(refusals)
    actor_reference = object.__getattribute__(generic, "actor_reference")
    audit_resource_id = object.__getattribute__(generic, "resource_id")
    audit_action = object.__getattribute__(generic, "action")
    result = object.__getattribute__(generic, "result")
    reason_or_error = object.__getattribute__(generic, "reason_or_error")
    tenant_reference = object.__getattribute__(generic, "tenant_reference")
    correlation_ids = object.__getattribute__(generic, "correlation_ids")
    causation_ids = object.__getattribute__(generic, "causation_ids")
    if actor_reference != subject_id:
        refusals.append(_refusal("actor_reference", "correspondance exacte attendue"))
    if audit_resource_id != resource_id:
        refusals.append(_refusal("audit_resource_id", "correspondance exacte attendue"))
    if audit_action != action_id:
        refusals.append(_refusal("audit_action", "correspondance exacte attendue"))
    if result != effect.value:
        refusals.append(_refusal("result", "correspondance exacte attendue"))
    if reason_or_error != reason_code:
        refusals.append(_refusal("reason_or_error", "correspondance exacte attendue"))
    if context_ok:
        scope_type = object.__getattribute__(context, "scope_type")
        tenant_id = object.__getattribute__(context, "tenant_id")
        if scope_type is ScopeType.TENANT:
            if tenant_reference != tenant_id:
                refusals.append(_refusal("tenant_reference", "référence tenant exacte attendue"))
        else:
            if tenant_reference is not None:
                refusals.append(_refusal("tenant_reference", "référence tenant exacte attendue"))
    if correlation_id not in correlation_ids:
        refusals.append(_refusal("correlation_ids", "référence requise attendue"))
    if decision_id not in causation_ids:
        refusals.append(_refusal("causation_ids", "référence requise attendue"))
    return _pack(refusals)
