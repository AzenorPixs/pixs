"""Plan privé C08 : sérialisation et liaisons, sans stockage ni autorité.

Les liens de confirmation et faits structurés ne prouvent pas une signature,
une confirmation opérateur, une décision courante ou un commit.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, fields

from pixs.core.bootstrap_operator import BOOTSTRAP_EFFECTS, BootstrapOperatorFacts, BootstrapOperatorError
from pixs.core.dto import BootstrapTargetSpec, CoreInputInvalid
from pixs.core.identity.models import IdentityState, IdentityType

__all__ = ["PlanInvalid", "PlanBindingInvalid", "PlanLimits", "InstallationPlan",
           "PlanConfirmationLink", "canonical_plan_bytes", "plan_sha256",
           "parse_plan_bytes", "bind_confirmation", "check_confirmation_link",
           "check_plan_facts_bind"]


class PlanInvalid(ValueError):
    code = "C08_PLAN_INVALID"

    def __init__(self) -> None:
        super().__init__("Plan d'installation refusé.")


class PlanBindingInvalid(PlanInvalid):
    code = "C08_PLAN_BINDING_INVALID"


def _reference(value: object, limit: int) -> None:
    if type(value) is not str or not 0 < len(value) <= limit or not value.isprintable():
        raise PlanInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class PlanLimits:
    max_bytes: int
    max_ref_len: int
    max_effects: int
    allowed_schema_versions: tuple[str, ...]
    allowed_plan_versions: tuple[str, ...]

    def __post_init__(self) -> None:
        for value in (self.max_bytes, self.max_ref_len, self.max_effects):
            if type(value) is not int or value < 1:
                raise PlanInvalid()
        for versions in (self.allowed_schema_versions, self.allowed_plan_versions):
            if type(versions) is not tuple or not versions:
                raise PlanInvalid()
            for version in versions:
                _reference(version, self.max_ref_len)
            if len(set(versions)) != len(versions):
                raise PlanInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class InstallationPlan:
    schema_version: str
    plan_version: str
    operation_id: str
    installation_ref: str
    database_target_ref: str
    observed_database_state: str
    database_action: str
    operator_subject_ref: str
    target_identity_ref: str
    target_tenant_ref: str | None
    target_spec: BootstrapTargetSpec
    closed_effects: tuple[str, ...]
    credential_intent_ref: str | None
    correlation_id: str
    causation_id: str | None
    idempotency_key: str


@dataclass(frozen=True, slots=True, repr=False)
class PlanConfirmationLink:
    plan_sha256: str
    confirmation_ref: str


_ACTIONS = {"ABSENT": ("PREPARATION",), "CONFORME": ("REUTILISATION",),
            "MIGRABLE": ("MIGRATION",), "INCOMPATIBLE": ("RECREATION",)}


def _limits(limits: object) -> None:
    if type(limits) is not PlanLimits:
        raise PlanInvalid()
    limits.__post_init__()


def _validate(plan: object, limits: PlanLimits) -> None:
    _limits(limits)
    if type(plan) is not InstallationPlan:
        raise PlanInvalid()
    for name in ("schema_version", "plan_version", "operation_id", "installation_ref",
                 "database_target_ref", "operator_subject_ref", "target_identity_ref",
                 "correlation_id", "idempotency_key"):
        _reference(getattr(plan, name), limits.max_ref_len)
    for value in (plan.target_tenant_ref, plan.causation_id, plan.credential_intent_ref):
        if value is not None:
            _reference(value, limits.max_ref_len)
    if (plan.schema_version not in limits.allowed_schema_versions
            or plan.plan_version not in limits.allowed_plan_versions
            or type(plan.observed_database_state) is not str
            or type(plan.database_action) is not str
            or plan.database_action not in _ACTIONS.get(plan.observed_database_state, ())):
        raise PlanInvalid()
    if type(plan.target_spec) is not BootstrapTargetSpec:
        raise PlanInvalid()
    try:
        plan.target_spec.__post_init__()
    except CoreInputInvalid:
        raise PlanInvalid() from None
    spec = plan.target_spec
    if plan.target_identity_ref != "pixs.core.identity:" + str(spec.identity_id):
        raise PlanInvalid()
    tenant_ref = None if spec.tenant_id is None else "pixs.core.tenant:" + spec.tenant_id
    if plan.target_tenant_ref != tenant_ref:
        raise PlanInvalid()
    if spec.tenant_id is not None:
        _reference(spec.tenant_id, limits.max_ref_len)
    effects = plan.closed_effects
    if (type(effects) is not tuple or not 0 < len(effects) <= limits.max_effects
            or any(type(e) is not str or e not in BOOTSTRAP_EFFECTS for e in effects)
            or len(set(effects)) != len(effects)):
        raise PlanInvalid()
    if effects == ("REUSE_EXISTING",):
        if (plan.credential_intent_ref is not None
                or spec.expected_binding_version is None
                or spec.expected_identity_version is None):
            raise PlanInvalid()
    else:
        if ("REUSE_EXISTING" in effects or any(e not in effects for e in BOOTSTRAP_EFFECTS[:3])
                or plan.credential_intent_ref is None
                or spec.expected_binding_version is not None
                or spec.expected_identity_version is not None):
            raise PlanInvalid()
    if any(e in effects for e in ("CREATE_TENANT", "GRANT_SUPER_ADMIN_TENANT")):
        if spec.tenant_id is None:
            raise PlanInvalid()


def _spec_document(spec: BootstrapTargetSpec) -> dict[str, object]:
    return {"identity_id": str(spec.identity_id), "identity_type": spec.identity_type.value,
            "identity_state": spec.identity_state.value,
            "expected_binding_version": spec.expected_binding_version,
            "expected_identity_version": spec.expected_identity_version,
            "tenant_id": spec.tenant_id, "expected_tenant_version": spec.expected_tenant_version}


def canonical_plan_bytes(plan: InstallationPlan, limits: PlanLimits) -> bytes:
    _validate(plan, limits)
    document = {field.name: getattr(plan, field.name) for field in fields(InstallationPlan)}
    document["target_spec"] = _spec_document(plan.target_spec)
    document["closed_effects"] = list(plan.closed_effects)
    try:
        raw = json.dumps(document, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError):
        raise PlanInvalid() from None
    if len(raw) > limits.max_bytes:
        raise PlanInvalid()
    return raw


def plan_sha256(plan: InstallationPlan, limits: PlanLimits) -> str:
    """Recalcule le digest des seuls octets canoniques du plan validé."""
    return hashlib.sha256(canonical_plan_bytes(plan, limits)).hexdigest()


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    document: dict[str, object] = {}
    for key, value in pairs:
        if key in document:
            raise PlanInvalid()
        document[key] = value
    return document


def _constant(value: str) -> object:
    raise PlanInvalid()


def parse_plan_bytes(raw: bytes, limits: PlanLimits) -> InstallationPlan:
    _limits(limits)
    if type(raw) is not bytes or not 0 < len(raw) <= limits.max_bytes:
        raise PlanInvalid()
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                              parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError):
        raise PlanInvalid() from None
    if type(document) is not dict or set(document) != {f.name for f in fields(InstallationPlan)}:
        raise PlanInvalid()
    spec = document["target_spec"]
    if type(spec) is not dict or set(spec) != {f.name for f in fields(BootstrapTargetSpec)}:
        raise PlanInvalid()
    if (type(spec["identity_id"]) is not str or type(spec["identity_type"]) is not str
            or type(spec["identity_state"]) is not str
            or type(document["closed_effects"]) is not list):
        raise PlanInvalid()
    try:
        identity = uuid.UUID(spec["identity_id"])
        if str(identity) != spec["identity_id"]:
            raise PlanInvalid()
        target = BootstrapTargetSpec(
            identity_id=identity, identity_type=IdentityType(spec["identity_type"]),
            identity_state=IdentityState(spec["identity_state"]),
            expected_binding_version=spec["expected_binding_version"],
            expected_identity_version=spec["expected_identity_version"],
            tenant_id=spec["tenant_id"], expected_tenant_version=spec["expected_tenant_version"])
    except (ValueError, CoreInputInvalid):
        raise PlanInvalid() from None
    document["target_spec"] = target
    document["closed_effects"] = tuple(document["closed_effects"])
    plan = InstallationPlan(**document)
    canonical_plan_bytes(plan, limits)
    return plan


def bind_confirmation(plan: InstallationPlan, confirmation_ref: str,
                      limits: PlanLimits) -> PlanConfirmationLink:
    _limits(limits)
    _reference(confirmation_ref, limits.max_ref_len)
    return PlanConfirmationLink(plan_sha256(plan, limits), confirmation_ref)


def check_confirmation_link(plan: InstallationPlan, link: PlanConfirmationLink,
                            limits: PlanLimits) -> None:
    _validate(plan, limits)
    if type(link) is not PlanConfirmationLink:
        raise PlanBindingInvalid()
    _reference(link.confirmation_ref, limits.max_ref_len)
    if link.plan_sha256 != plan_sha256(plan, limits):
        raise PlanBindingInvalid()


def check_plan_facts_bind(plan: InstallationPlan, facts: BootstrapOperatorFacts,
                         limits: PlanLimits) -> None:
    """Liaison structurelle seulement ; ne vérifie pas la signature ni l'autorité."""
    _validate(plan, limits)
    if type(facts) is not BootstrapOperatorFacts:
        raise PlanBindingInvalid()
    try:
        facts.__post_init__()
    except BootstrapOperatorError:
        raise PlanBindingInvalid() from None
    if facts.plan_sha256 != plan_sha256(plan, limits):
        raise PlanBindingInvalid()
    for name in ("operation_id", "plan_version", "installation_ref", "operator_subject_ref",
                 "target_identity_ref", "target_tenant_ref", "closed_effects"):
        if getattr(facts, name) != getattr(plan, name):
            raise PlanBindingInvalid()
