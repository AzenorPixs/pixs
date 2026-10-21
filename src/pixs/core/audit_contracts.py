"""Contrats C05 : politique explicite, sources de confiance, sérialisation bornée.

Importable sans Django. Aucune horloge, IO, transaction ou secret.
Les validateurs Kernel restent purs et inchangés ; seule l'opération C05
applique une règle fournie. Aucun placeholder ni paramètre implicite.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.authz.ports import Effect, Request
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent
from pixs.kernel.audit_event import validate_audit_event
from pixs.kernel.audit_field_redaction import (
    AuditFieldRedaction,
    RedactionMode,
    validate_audit_field_redaction,
)
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

__all__ = [
    "AuditError",
    "AuditPolicy",
    "AuditPolicySource",
    "ExplicitAuditPolicySource",
    "AuditLifecyclePort",
    "encode_policy_version",
    "decode_policy_version",
    "canonical_generic_bytes",
    "canonical_pdp_bytes",
    "apply_redactions_generic",
    "apply_redactions_pdp",
    "check_policy_preserves_c01",
    "serialize_generic", "serialize_pdp",
    "validate_generic_payload", "validate_pdp_payload",
]

_FIXED = "Audit contract invalide."

_MAX_POLICY_DEPTH = 8
_MAX_POLICY_ITEMS = 512
_MAX_POLICY_STR = 4096
_MAX_PAYLOAD_BYTES = 65536

_GENERIC_KEYS = (
    "event_id", "occurred_at", "actor_reference", "tenant_reference",
    "action", "resource_type", "resource_id", "result", "reason_or_error",
    "correlation_ids", "causation_ids", "component_id", "component_version",
)
_PDP_KEYS = (
    "decision_id", "subject_id", "resource_id", "action_id", "context",
    "correlation_id", "effect", "reason_code", "policy_version", "evaluated_at",
)
class AuditError(ValueError):
    def __init__(self, code: str = "AUDIT_CONTRACT_INVALID") -> None:
        super().__init__(_FIXED)
        self.code = code
        self.element = "audit_contract"
        self.step = "validate"


def _is_exact_str(value: object) -> bool:
    return type(value) is str and value != ""


@dataclass(frozen=True, slots=True)
class AuditPolicy:
    policy_id: str
    policy_version: str
    origin: str
    retention_days: int
    max_event_bytes: int
    max_query_records: int
    redactions: tuple[AuditFieldRedaction, ...]
    governance_ref: str
    confidentiality: ConfidentialityLevel
    personal: PersonalDataLevel

    def __post_init__(self) -> None:
        if not _is_exact_str(self.policy_id):
            raise AuditError()
        if not _is_exact_str(self.policy_version):
            raise AuditError()
        if not _is_exact_str(self.origin):
            raise AuditError()
        if type(self.retention_days) is not int or isinstance(self.retention_days, bool):
            raise AuditError()
        if self.retention_days <= 0:
            raise AuditError()
        if type(self.max_event_bytes) is not int or isinstance(self.max_event_bytes, bool):
            raise AuditError()
        if self.max_event_bytes <= 0:
            raise AuditError()
        if type(self.max_query_records) is not int or isinstance(self.max_query_records, bool):
            raise AuditError()
        if self.max_query_records <= 0:
            raise AuditError()
        if type(self.redactions) is not tuple:
            raise AuditError()
        seen = set()
        for item in self.redactions:
            if type(item) is not AuditFieldRedaction:
                raise AuditError()
            if validate_audit_field_redaction(item):
                raise AuditError()
            _check_rule_target("generic", item)
            if item.field_reference in seen:
                raise AuditError()
            seen.add(item.field_reference)
        if not _is_exact_str(self.governance_ref):
            raise AuditError()
        if type(self.confidentiality) is not ConfidentialityLevel:
            raise AuditError()
        if type(self.personal) is not PersonalDataLevel:
            raise AuditError()


class AuditPolicySource(Protocol):
    def resolve(self, *, context: ScopeContext, alias: str) -> AuditPolicy:
        ...


@dataclass(frozen=True, slots=True)
class ExplicitAuditPolicySource:
    """Politique sélectionnée explicitement à la composition, sans droit implicite."""
    approved_context: ScopeContext
    policy: AuditPolicy

    def __post_init__(self) -> None:
        if type(self.approved_context) is not ScopeContext or type(self.policy) is not AuditPolicy:
            raise AuditError()
        try:
            validate_structure(self.approved_context)
        except ScopeStructureError as error:
            raise AuditError() from error
        self.policy.__post_init__()

    def resolve(self, *, context: ScopeContext, alias: str) -> AuditPolicy:
        if not _is_exact_str(alias) or type(context) is not ScopeContext:
            raise AuditError()
        try:
            validate_structure(context)
        except ScopeStructureError as error:
            raise AuditError() from error
        if context != self.approved_context:
            raise AuditError()
        self.policy.__post_init__()
        return self.policy


class AuditLifecyclePort(Protocol):
    """Fourni par Jobs/C10/C16 : vérifie mandat Job, rétention/holds/références/projections COURANTS."""

    def authorize_maintenance(self, *, request: Request, record_reference: str, policy: AuditPolicy, alias: str, operation_id: str, job_id: str, mode: str) -> None:
        ...


def encode_policy_version(value: object) -> object:
    def _enc(item: object, depth: int) -> object:
        if depth > _MAX_POLICY_DEPTH:
            raise AuditError()
        if item is None:
            return None
        if type(item) is str:
            if len(item) > _MAX_POLICY_STR:
                raise AuditError()
            return item
        if type(item) is tuple:
            if len(item) > _MAX_POLICY_ITEMS:
                raise AuditError()
            return {"__tuple__": [_enc(sub, depth + 1) for sub in item]}
        raise AuditError()
    if value is None:
        return None
    if type(value) is not tuple:
        raise AuditError()
    return {"encoded_policy_version": _enc(value, 0)}


def decode_policy_version(raw: object) -> object:
    def _dec(item: object, depth: int) -> object:
        if depth > _MAX_POLICY_DEPTH:
            raise AuditError()
        if item is None:
            return None
        if type(item) is str:
            if len(item) > _MAX_POLICY_STR:
                raise AuditError()
            return item
        if type(item) is dict and set(item.keys()) == {"__tuple__"}:
            inner = item["__tuple__"]
            if type(inner) is not list or len(inner) > _MAX_POLICY_ITEMS:
                raise AuditError()
            return tuple(_dec(sub, depth + 1) for sub in inner)
        raise AuditError()
    if raw is None:
        return None
    if type(raw) is not dict or set(raw.keys()) != {"encoded_policy_version"}:
        raise AuditError()
    result = _dec(raw["encoded_policy_version"], 0)
    if type(result) is not tuple:
        raise AuditError()
    return result


def _dumps_canonical(payload: dict) -> bytes:
    try:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        data = raw.encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as error:
        raise AuditError() from error
    if len(data) == 0 or len(data) > _MAX_PAYLOAD_BYTES:
        raise AuditError()
    return data


def canonical_generic_bytes(payload: dict) -> bytes:
    if type(payload) is not dict or set(payload.keys()) != set(_GENERIC_KEYS):
        raise AuditError()
    validate_generic_payload(payload)
    return _dumps_canonical(payload)


def canonical_pdp_bytes(payload: dict) -> bytes:
    if type(payload) is not dict or set(payload.keys()) != set(_PDP_KEYS):
        raise AuditError()
    validate_pdp_payload(payload)
    return _dumps_canonical(payload)


_MUTABLE_FIELDS = {
    "generic": {"actor_reference": False, "resource_id": False, "reason_or_error": True},
    "pdp": {"subject_id": True, "resource_id": True},
}


def _check_rule_target(kind: str, rule: AuditFieldRedaction) -> str | None:
    qualified = rule.field_reference
    if type(qualified) is not str or "." not in qualified:
        raise AuditError()
    namespace, field = qualified.split(".", 1)
    if namespace not in _MUTABLE_FIELDS or field not in _MUTABLE_FIELDS[namespace]:
        raise AuditError()
    if rule.mode is RedactionMode.REDACTED:
        if rule.replacement_reference is not None or not _MUTABLE_FIELDS[namespace][field]:
            raise AuditError()
    elif rule.mode is RedactionMode.PSEUDONYMIZED_REFERENCE:
        if not _is_exact_str(rule.replacement_reference):
            raise AuditError()
    else:
        raise AuditError()
    return field if namespace == kind else None


def _redact(kind: str, payload: dict, redactions: tuple) -> dict:
    expected = _GENERIC_KEYS if kind == "generic" else _PDP_KEYS
    if type(payload) is not dict or set(payload) != set(expected) or type(redactions) is not tuple:
        raise AuditError()
    result = dict(payload)
    seen = set()
    for rule in redactions:
        if type(rule) is not AuditFieldRedaction or validate_audit_field_redaction(rule):
            raise AuditError()
        if rule.field_reference in seen:
            raise AuditError()
        seen.add(rule.field_reference)
        field = _check_rule_target(kind, rule)
        if field is not None:
            result[field] = None if rule.mode is RedactionMode.REDACTED else rule.replacement_reference
    return result


def apply_redactions_generic(payload: dict, redactions: tuple) -> dict:
    return _redact("generic", payload, redactions)


def apply_redactions_pdp(payload: dict, redactions: tuple) -> dict:
    return _redact("pdp", payload, redactions)


def check_policy_preserves_c01(policy: AuditPolicy) -> None:
    if type(policy) is not AuditPolicy:
        raise AuditError()
    policy.__post_init__()
    if any(_check_rule_target("generic", rule) is not None for rule in policy.redactions):
        raise AuditError()


def serialize_generic(event: GenericAuditEvent) -> dict:
    if type(event) is not GenericAuditEvent or validate_audit_event(event):
        raise AuditError()
    result = {key: getattr(event, key) for key in _GENERIC_KEYS}
    result["correlation_ids"] = list(event.correlation_ids)
    result["causation_ids"] = list(event.causation_ids)
    return result


def serialize_pdp(event: PdpAuditEvent) -> dict:
    if type(event) is not PdpAuditEvent:
        raise AuditError()
    try:
        event.__post_init__()
        context = event.context
        if context is not None:
            validate_structure(context)
    except (ValueError, TypeError) as error:
        raise AuditError() from error
    return {
        "decision_id": event.decision_id, "subject_id": event.subject_id,
        "resource_id": event.resource_id, "action_id": event.action_id,
        "context": None if context is None else {
            "scope_type": context.scope_type.value, "tenant_id": context.tenant_id,
            "scope_id": context.scope_id},
        "correlation_id": event.correlation_id, "effect": event.effect.value,
        "reason_code": event.reason_code,
        "policy_version": encode_policy_version(event.policy_version),
        "evaluated_at": None if event.evaluated_at is None else event.evaluated_at.isoformat(),
    }


def validate_generic_payload(payload: dict) -> None:
    if type(payload) is not dict or set(payload) != set(_GENERIC_KEYS):
        raise AuditError()
    if type(payload["correlation_ids"]) is not list or type(payload["causation_ids"]) is not list:
        raise AuditError()
    data = dict(payload)
    data["correlation_ids"] = tuple(data["correlation_ids"])
    data["causation_ids"] = tuple(data["causation_ids"])
    try:
        event = GenericAuditEvent(**data)
    except TypeError as error:
        raise AuditError() from error
    if validate_audit_event(event):
        raise AuditError()


def validate_pdp_payload(payload: dict) -> None:
    import datetime
    if type(payload) is not dict or set(payload) != set(_PDP_KEYS):
        raise AuditError()
    data = dict(payload)
    ctx = data["context"]
    if ctx is not None:
        if type(ctx) is not dict or set(ctx) != {"scope_type", "tenant_id", "scope_id"}:
            raise AuditError()
        if type(ctx["scope_type"]) is not str:
            raise AuditError()
        try:
            data["context"] = ScopeContext(ScopeType(ctx["scope_type"]), ctx["tenant_id"], ctx["scope_id"])
            validate_structure(data["context"])
        except (ValueError, TypeError) as error:
            raise AuditError() from error
    if type(data["effect"]) is not str:
        raise AuditError()
    try:
        data["effect"] = Effect(data["effect"])
        data["policy_version"] = decode_policy_version(data["policy_version"])
        if data["policy_version"] is not None and type(data["policy_version"]) is not tuple:
            raise AuditError()
        if data["evaluated_at"] is not None:
            if type(data["evaluated_at"]) is not str:
                raise AuditError()
            data["evaluated_at"] = datetime.datetime.fromisoformat(data["evaluated_at"])
        PdpAuditEvent(**data)
    except (ValueError, TypeError) as error:
        raise AuditError() from error
