"""Moteur authorize PDP minimal : recalcul borné, audit unique."""

import datetime
from dataclasses import dataclass

from ..scope.context import ScopeContext, ScopeType, validate_structure
from ..scope.topology import (
    ScopeNode,
    TopologyError,
    TopologySnapshot,
    validate_context,
)
from ..scope.ownership import ResourceOwnership
from .policy import (
    AuthenticationAssurance,
    Effect,
    FederationTrust,
    IdentityAssurance,
)
from .ports import (
    AuditEvent,
    AuthenticationContext,
    Request,
    RevocationStatus,
    TrustedFacts,
)
from .snapshot import Snapshot, SnapshotError, validate_snapshot


class DecisionError(ValueError):
    def __init__(self):
        super().__init__("Décision PDP invalide.")
        self.code = "PDP_DECISION_INVALID"
        self.element = "pdp_decision"
        self.step = "authorize"


class _InternalDeny(Exception):
    pass


class _PolicyDeny(Exception):
    pass


@dataclass(frozen=True, slots=True, repr=False)
class Decision:
    decision_id: object
    effect: Effect
    reason_code: str
    policy_version: object
    obligations: tuple
    evaluated_at: object
    expires_at: object


_ORDERS = {
    IdentityAssurance: ("CLAIMED", "VERIFIED", "PROOFED"),
    AuthenticationAssurance: (
        "SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"),
    FederationTrust: ("UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"),
}


def _rank(enum_type, value):
    for index, name in enumerate(_ORDERS[enum_type]):
        for cand in enum_type:
            if (object.__getattribute__(cand, "name") == name
                    and value is cand):
                return index
    return -1


def _is_id(value):
    return type(value) is str and value != ""


def _prepare_detailed(request, snapshot, provider, clock, topology):
    """Prépare le calcul interne ; aucun audit, commit ou accès n’est confirmé."""
    version = None
    now = None
    view = (None, None, None, None, None, None)
    effect = Effect.DENY
    obligations = ()
    expires = None
    status = "ERROR"
    try:
        candidate_time = clock.now()
        if (type(candidate_time) is datetime.datetime
                and candidate_time.tzinfo is datetime.timezone.utc):
            now = candidate_time
    except Exception:
        pass
    try:
        canon = validate_snapshot(snapshot)
        version = canon.version
        budget = _Budget(canon.limits)
        view, request_key = _request_view(request, budget)
        if now is None:
            raise _InternalDeny()
        obligations, expires = _evaluate(
            request, canon, provider, now, topology, budget, request_key)
        effect = Effect.ALLOW
        status = "ALLOW"
    except _PolicyDeny:
        effect = Effect.DENY
        obligations = ()
        expires = now
        status = "DENY_POLICY"
    except Exception:
        effect = Effect.DENY
        obligations = ()
        expires = now
        status = "ERROR"
    code = "ALLOWED" if effect is Effect.ALLOW else "DENIED"
    return (
        Decision(view[0], effect, code, version, obligations, now, expires),
        status,
        view,
    )


def _authorize_detailed(request, snapshot, provider, clock, audit, topology):
    decision, status, view = _prepare_detailed(
        request, snapshot, provider, clock, topology)
    effect = decision.effect
    code = decision.reason_code
    version = decision.policy_version
    obligations = decision.obligations
    now = decision.evaluated_at
    expires = decision.expires_at
    platform = (view[4] is not None
                and view[4].scope_type is ScopeType.PLATFORM)
    if effect is Effect.DENY or platform:
        event = AuditEvent(
            view[0], view[1], view[2], view[3], view[4], view[5],
            effect, code, version, now)
        try:
            acknowledged = audit.record(event) is True
        except Exception:
            acknowledged = False
        if not acknowledged:
            effect = Effect.DENY
            code = "DENIED"
            obligations = ()
            expires = now
            status = "ERROR"
    return (
        Decision(view[0], effect, code, version, obligations, now, expires),
        status,
    )


def authorize(request, snapshot, provider, clock, audit, topology):
    decision, _status = _authorize_detailed(
        request, snapshot, provider, clock, audit, topology)
    return decision


class _Budget:
    def __init__(self, limits):
        self.max_cost = object.__getattribute__(limits, "max_cost")
        self.max_id = object.__getattribute__(limits, "max_id_length")
        self.max_val = object.__getattribute__(limits, "max_value_length")
        self.max_items = limits.max_selector_values
        self.max_memberships = limits.max_memberships
        self.max_attributes = limits.max_attributes
        self.used = 0

    def spend(self, units):
        self.used += units
        if self.used > self.max_cost:
            raise _InternalDeny()

    def check_id(self, value):
        if type(value) is not str or value == "":
            raise _InternalDeny()
        if len(value) > self.max_id:
            raise _InternalDeny()
        self.spend(1 + len(value))
        return True

    def check_value(self, value, tag):
        if tag == "STR":
            if type(value) is not str or value == "":
                raise _InternalDeny()
            if len(value) > self.max_val:
                raise _InternalDeny()
            self.spend(1 + len(value))
        else:
            if type(value) is not int or type(value) is bool:
                raise _InternalDeny()
            if value.bit_length() > self.max_val:
                raise _InternalDeny()
            self.spend(2)
        return True


def _scope_key(ctx, budget):
    if type(ctx) is not ScopeContext:
        raise _InternalDeny()
    stype = object.__getattribute__(ctx, "scope_type")
    tenant = object.__getattribute__(ctx, "tenant_id")
    scp = object.__getattribute__(ctx, "scope_id")
    if stype is not ScopeType.TENANT and stype is not ScopeType.PLATFORM:
        raise _InternalDeny()
    if tenant is not None:
        budget.check_id(tenant)
    elif stype is ScopeType.TENANT:
        raise _InternalDeny()
    if scp is not None:
        budget.check_id(scp)
    try:
        validate_structure(ctx)
    except Exception:
        raise _InternalDeny() from None
    budget.spend(2)
    return (
        object.__getattribute__(stype, "value"),
        tenant if tenant is not None else "",
        scp if scp is not None else "",
    )


def _request_view(request, budget):
    if type(request) is not Request:
        raise _InternalDeny()
    vals = []
    for name in (
        "decision_id", "subject_id", "resource_id",
        "action_id", "correlation_id",
    ):
        value = object.__getattribute__(request, name)
        budget.check_id(value)
        vals.append(value)
    ctx = object.__getattribute__(request, "context")
    key = _scope_key(ctx, budget)
    budget.spend(1)
    return ((vals[0], vals[1], vals[2], vals[3], ctx, vals[4]), key)


def _validated_topology(topology, budget):
    if type(topology) is not TopologySnapshot:
        raise _InternalDeny()
    tenants = object.__getattribute__(topology, "tenants")
    scopes = object.__getattribute__(topology, "scopes")
    if type(tenants) is not tuple or type(scopes) is not tuple:
        raise _InternalDeny()
    if len(tenants) > budget.max_items or len(scopes) > budget.max_items:
        raise _InternalDeny()
    budget.spend(len(tenants) + len(scopes) + 1)
    for tenant in tenants:
        budget.check_id(tenant)
    for node in scopes:
        if type(node) is not ScopeNode:
            raise _InternalDeny()
        sid = object.__getattribute__(node, "scope_id")
        tid = object.__getattribute__(node, "tenant_id")
        parent = object.__getattribute__(node, "parent_scope_id")
        budget.check_id(sid)
        budget.check_id(tid)
        if parent is not None:
            budget.check_id(parent)
        budget.spend(2)
    budget.spend(32 * (len(tenants) + len(scopes) + 1) * (1 + budget.max_id))
    try:
        canon = TopologySnapshot(tenants, scopes)
    except Exception:
        raise _InternalDeny() from None
    budget.spend(len(tenants) + len(scopes))
    return canon


def _validated_facts(facts, request, request_key, canon, budget):
    if type(facts) is not TrustedFacts:
        raise _InternalDeny()
    f_sid = object.__getattribute__(facts, "subject_id")
    f_rid = object.__getattribute__(facts, "resource_id")
    f_aid = object.__getattribute__(facts, "action_id")
    for value in (f_sid, f_rid, f_aid):
        budget.check_id(value)
    auth = object.__getattribute__(facts, "auth")
    own = object.__getattribute__(facts, "ownership")
    f_ctx = object.__getattribute__(facts, "context")
    rev = object.__getattribute__(facts, "revocation_status")
    if type(auth) is not AuthenticationContext:
        raise _InternalDeny()
    if type(own) is not ResourceOwnership:
        raise _InternalDeny()
    a_did = object.__getattribute__(auth, "digital_identity_id")
    a_prov = object.__getattribute__(auth, "provider_id")
    a_iss = object.__getattribute__(auth, "issuer")
    a_ext = object.__getattribute__(auth, "external_subject")
    for value in (a_did, a_prov, a_iss, a_ext):
        budget.check_id(value)
    methods = object.__getattribute__(auth, "methods")
    if type(methods) is not tuple or len(methods) > budget.max_items or not methods:
        raise _InternalDeny()
    budget.spend(len(methods) + 1)
    for method in methods:
        budget.check_id(method)
    for name in ("session_id", "credential_id"):
        value = object.__getattribute__(auth, name)
        if value is not None:
            budget.check_id(value)
    a_time = object.__getattribute__(auth, "authentication_time")
    a_exp = object.__getattribute__(auth, "expires_at")
    if not (type(a_time) is datetime.datetime
            and a_time.tzinfo is datetime.timezone.utc):
        raise _InternalDeny()
    if not (type(a_exp) is datetime.datetime
            and a_exp.tzinfo is datetime.timezone.utc):
        raise _InternalDeny()
    if not a_time < a_exp:
        raise _InternalDeny()
    budget.spend(3)
    for enum_type, name in (
        (IdentityAssurance, "identity_assurance"),
        (AuthenticationAssurance, "authentication_assurance"),
        (FederationTrust, "federation_trust"),
    ):
        value = object.__getattribute__(auth, name)
        found = False
        for member in enum_type:
            if value is member:
                found = True
                break
        if not found:
            raise _InternalDeny()
        budget.spend(1)
    a_ctx = object.__getattribute__(auth, "context")
    a_key = _scope_key(a_ctx, budget)
    f_key = _scope_key(f_ctx, budget)
    if not (a_key == f_key == request_key):
        raise _InternalDeny()
    o_rid = object.__getattribute__(own, "resource_id")
    o_ctx = object.__getattribute__(own, "context")
    budget.check_id(o_rid)
    if not (f_sid == request.subject_id == a_did
            and f_rid == request.resource_id == o_rid
            and f_aid == request.action_id):
        raise _InternalDeny()
    o_key = _scope_key(o_ctx, budget)
    if o_key != request_key:
        raise _InternalDeny()
    if type(rev) is not RevocationStatus:
        raise _InternalDeny()
    budget.spend(2)
    memberships = object.__getattribute__(facts, "memberships")
    attributes = object.__getattribute__(facts, "attributes")
    if type(memberships) is not tuple or type(attributes) is not tuple:
        raise _InternalDeny()
    if (len(memberships) > budget.max_memberships
            or len(attributes) > budget.max_attributes):
        raise _InternalDeny()
    budget.spend(len(memberships) + len(attributes) + 1)
    try:
        catalog = object.__getattribute__(canon, "catalog")
        attr_types = object.__getattribute__(catalog, "attribute_types")
    except Exception:
        raise _InternalDeny() from None
    budget.spend((len(attr_types) + 1) * (budget.max_id + 2))
    tag_map = {}
    for entry in attr_types:
        if type(entry) is not tuple or len(entry) != 2:
            raise _InternalDeny()
        tag_map[entry[0]] = entry[1]
        budget.spend(1)
    for member in memberships:
        budget.check_id(member)
    attr_map = {}
    for entry in attributes:
        if type(entry) is not tuple or len(entry) != 2:
            raise _InternalDeny()
        name, value = entry
        if type(name) is not str or name == "":
            raise _InternalDeny()
        budget.check_id(name)
        if name not in tag_map:
            raise _InternalDeny()
        tag = tag_map[name]
        if name in attr_map:
            raise _InternalDeny()
        if tag == "STR":
            if type(value) is not str or value == "":
                raise _InternalDeny()
            if len(value) > budget.max_val:
                raise _InternalDeny()
            budget.spend(1 + len(value))
        else:
            if type(value) is not int or type(value) is bool:
                raise _InternalDeny()
            if value.bit_length() > budget.max_val:
                raise _InternalDeny()
            budget.spend(2)
        attr_map[name] = value
    if rev is RevocationStatus.UNKNOWN:
        raise _InternalDeny()
    if rev is not RevocationStatus.ACTIVE:
        raise _PolicyDeny()
    return (auth, attr_map)


def _evaluate(request, canon, provider, now, topology, budget, request_key):
    topology = _validated_topology(topology, budget)
    budget.spend(8 * (len(topology.tenants) + len(topology.scopes) + 1)
                 * (budget.max_id + 1))
    validate_context(request.context, topology)
    try:
        facts = provider.resolve(request)
    except Exception:
        raise _InternalDeny() from None
    auth, attributes = _validated_facts(
        facts, request, request_key, canon, budget)
    auth_time = auth.authentication_time
    if not auth_time <= now < auth.expires_at:
        raise _PolicyDeny()
    expiry = min(
        now + datetime.timedelta(seconds=canon.limits.ttl_seconds),
        auth.expires_at,
        auth_time + datetime.timedelta(
            seconds=canon.limits.max_freshness_seconds))
    if expiry <= now:
        raise _PolicyDeny()
    allow = False
    deny = False
    audit_required = False
    for policy in canon.policies:
        budget.spend(
            (len(policy.subject.values) + len(policy.resource.values)
             + len(policy.action.values) + 1) * (budget.max_id + 1))
        target = (request.subject_id in policy.subject.values
                  and request.resource_id in policy.resource.values
                  and request.action_id in policy.action.values)
        if not target:
            continue
        scope_match = False
        budget.spend((len(policy.scope.contexts) + 1)
                     * (3 * budget.max_id + 4))
        for context in policy.scope.contexts:
            if _scope_key(context, budget) == request_key:
                scope_match = True
        if not scope_match:
            continue
        for boundary in (policy.valid_from, policy.valid_until):
            if boundary is not None and now < boundary < expiry:
                expiry = boundary
        if policy.max_auth_age_seconds is not None:
            freshness = auth_time + datetime.timedelta(
                seconds=policy.max_auth_age_seconds)
            if now < freshness < expiry:
                expiry = freshness
        if (policy.valid_from is not None and now < policy.valid_from):
            continue
        if (policy.valid_until is not None and now >= policy.valid_until):
            continue
        budget.spend((len(policy.conditions) + 1) * (budget.max_id + 2))
        for condition in policy.conditions:
            if condition.attr not in attributes:
                raise _InternalDeny()
        conditions_match = True
        for condition in policy.conditions:
            actual = attributes[condition.attr]
            expected = condition.value
            values = (expected,) if condition.op == "eq" else expected
            budget.spend((len(values) + 1) * (budget.max_val + 2))
            hit = False
            for value in values:
                if type(actual) is type(value) and actual == value:
                    hit = True
            if not hit:
                conditions_match = False
        if not conditions_match:
            continue
        budget.spend(32)
        if (policy.min_identity_assurance is not None
                and _rank(IdentityAssurance, auth.identity_assurance)
                < _rank(IdentityAssurance, policy.min_identity_assurance)):
            continue
        if (policy.min_authentication_assurance is not None
                and _rank(AuthenticationAssurance, auth.authentication_assurance)
                < _rank(AuthenticationAssurance,
                        policy.min_authentication_assurance)):
            continue
        if (policy.min_federation_trust is not None
                and _rank(FederationTrust, auth.federation_trust)
                < _rank(FederationTrust, policy.min_federation_trust)):
            continue
        if (policy.max_auth_age_seconds is not None
                and now >= auth_time + datetime.timedelta(
                    seconds=policy.max_auth_age_seconds)):
            continue
        if policy.effect is Effect.DENY:
            deny = True
        elif policy.effect is Effect.ALLOW:
            allow = True
            budget.spend(2 * (len(policy.obligations) + 1))
            for obligation in policy.obligations:
                if obligation.kind == "AUDIT":
                    audit_required = True
    if deny or not allow or expiry <= now:
        raise _PolicyDeny()
    if (request.context.scope_type is ScopeType.PLATFORM
            and not audit_required):
        raise _PolicyDeny()
    return (("AUDIT",) if audit_required else ()), expiry


__all__ = ["DecisionError", "Decision", "authorize"]
