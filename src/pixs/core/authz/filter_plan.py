"""Plan préparatoire source-filter-plan-v1 : lot homogène vers plan déclaratif."""

import datetime
from dataclasses import dataclass

from ..scope.context import ScopeContext, validate_structure
from ..scope.topology import TopologySnapshot, validate_context
from .decision import _Budget, _authorize_detailed, _validated_topology
from .ports import Request
from .snapshot import validate_snapshot


PROFILE_VERSION = "source-filter-plan-v1"


class FilterPlanError(ValueError):
    def __init__(self):
        super().__init__("Plan de filtrage invalide.")
        self.code = "FILTER_PLAN_INVALID"
        self.element = "filter_plan"
        self.step = "plan_filter"


def _is_id(value):
    return type(value) is str and value != ""


def _is_utc_aware(value):
    return (
        type(value) is datetime.datetime
        and value.tzinfo is datetime.timezone.utc
    )


@dataclass(frozen=True, slots=True, repr=False)
class FilterConfig:
    max_filter_requests: int

    def __post_init__(self):
        value = object.__getattribute__(self, "max_filter_requests")
        if type(value) is bool or type(value) is not int or value <= 0:
            raise FilterPlanError()


@dataclass(frozen=True, slots=True, repr=False)
class FilterLot:
    subject_id: str
    action_id: str
    context: ScopeContext
    correlation_id: str
    requests: tuple

    def __post_init__(self):
        for name in ("subject_id", "action_id", "correlation_id"):
            if not _is_id(object.__getattribute__(self, name)):
                raise FilterPlanError()
        if type(object.__getattribute__(self, "context")) is not ScopeContext:
            raise FilterPlanError()
        if type(object.__getattribute__(self, "requests")) is not tuple:
            raise FilterPlanError()


@dataclass(frozen=True, slots=True, repr=False)
class FilterPlan:
    subject_id: str
    action_id: str
    context: ScopeContext
    correlation_id: str
    profile_version: str
    snapshot_version: object
    evaluated_at: object
    resource_ids: tuple
    obligations: tuple
    expires_at: object

    def __post_init__(self):
        for name in (
            "subject_id", "action_id", "correlation_id", "profile_version",
        ):
            if not _is_id(object.__getattribute__(self, name)):
                raise FilterPlanError()
        if type(object.__getattribute__(self, "context")) is not ScopeContext:
            raise FilterPlanError()
        for name in ("resource_ids", "obligations"):
            if type(object.__getattribute__(self, name)) is not tuple:
                raise FilterPlanError()


class _FixedClock:
    def __init__(self, now):
        self._now = now

    def now(self):
        return self._now


def _scope_equal(a, b):
    return (
        type(a) is ScopeContext
        and type(b) is ScopeContext
        and object.__getattribute__(a, "scope_type")
        is object.__getattribute__(b, "scope_type")
        and object.__getattribute__(a, "tenant_id")
        == object.__getattribute__(b, "tenant_id")
        and object.__getattribute__(a, "scope_id")
        == object.__getattribute__(b, "scope_id")
    )


def plan_filter(lot, snapshot, provider, clock, audit, topology, config):
    if type(config) is not FilterConfig:
        raise FilterPlanError()
    max_n = object.__getattribute__(config, "max_filter_requests")
    if type(max_n) is bool or type(max_n) is not int or max_n <= 0:
        raise FilterPlanError()
    if type(lot) is not FilterLot:
        raise FilterPlanError()
    subject = object.__getattribute__(lot, "subject_id")
    action = object.__getattribute__(lot, "action_id")
    context = object.__getattribute__(lot, "context")
    correlation = object.__getattribute__(lot, "correlation_id")
    requests = object.__getattribute__(lot, "requests")
    if not (_is_id(subject) and _is_id(action) and _is_id(correlation)):
        raise FilterPlanError()
    if type(context) is not ScopeContext:
        raise FilterPlanError()
    if type(requests) is not tuple:
        raise FilterPlanError()
    if len(requests) > max_n:
        raise FilterPlanError()
    try:
        canon = validate_snapshot(snapshot)
    except Exception:
        raise FilterPlanError() from None
    version = canon.version
    catalog = object.__getattribute__(canon, "catalog")
    limits = object.__getattribute__(canon, "limits")
    max_id = object.__getattribute__(limits, "max_id_length")
    for header_id in (subject, action, correlation):
        if len(header_id) > max_id:
            raise FilterPlanError()
    if subject not in object.__getattribute__(catalog, "subject_ids"):
        raise FilterPlanError()
    if action not in object.__getattribute__(catalog, "action_ids"):
        raise FilterPlanError()
    header_scope_found = False
    for candidate in object.__getattribute__(catalog, "scope_contexts"):
        if _scope_equal(candidate, context):
            header_scope_found = True
            break
    if not header_scope_found:
        raise FilterPlanError()
    try:
        lot_budget = _Budget(limits)
        canon_topology = _validated_topology(topology, lot_budget)
        validate_context(context, canon_topology)
    except Exception:
        raise FilterPlanError() from None
    seen_resource = set()
    seen_decision = set()
    for request in requests:
        if type(request) is not Request:
            raise FilterPlanError()
        rid = object.__getattribute__(request, "resource_id")
        did = object.__getattribute__(request, "decision_id")
        sid = object.__getattribute__(request, "subject_id")
        aid = object.__getattribute__(request, "action_id")
        ctx = object.__getattribute__(request, "context")
        corr = object.__getattribute__(request, "correlation_id")
        if not (_is_id(rid) and _is_id(did)):
            raise FilterPlanError()
        if not (_is_id(sid) and _is_id(aid) and _is_id(corr)):
            raise FilterPlanError()
        if not (sid == subject and aid == action):
            raise FilterPlanError()
        if not (corr == correlation and _scope_equal(ctx, context)):
            raise FilterPlanError()
        if rid in seen_resource or did in seen_decision:
            raise FilterPlanError()
        seen_resource.add(rid)
        seen_decision.add(did)
        if rid not in object.__getattribute__(catalog, "resource_ids"):
            raise FilterPlanError()
        if sid not in object.__getattribute__(catalog, "subject_ids"):
            raise FilterPlanError()
        if aid not in object.__getattribute__(catalog, "action_ids"):
            raise FilterPlanError()
        found_scope = False
        for candidate in object.__getattribute__(catalog, "scope_contexts"):
            if _scope_equal(candidate, ctx):
                found_scope = True
                break
        if not found_scope:
            raise FilterPlanError()
    try:
        now = clock.now()
    except Exception:
        raise FilterPlanError() from None
    if not _is_utc_aware(now):
        raise FilterPlanError()
    fixed = _FixedClock(now)
    allowed = []
    expiries = []
    audits = set()
    for request in requests:
        try:
            decision, status = _authorize_detailed(
                request, canon, provider, fixed, audit, canon_topology)
        except Exception:
            raise FilterPlanError() from None
        if status == "ERROR":
            raise FilterPlanError()
        if status == "DENY_POLICY":
            continue
        if status != "ALLOW":
            raise FilterPlanError()
        if object.__getattribute__(decision, "policy_version") != version:
            raise FilterPlanError()
        if object.__getattribute__(decision, "evaluated_at") != now:
            raise FilterPlanError()
        if object.__getattribute__(decision, "decision_id") != object.__getattribute__(
            request, "decision_id"
        ):
            raise FilterPlanError()
        allowed.append(object.__getattribute__(request, "resource_id"))
        expiries.append(object.__getattribute__(decision, "expires_at"))
        for obligation in object.__getattribute__(decision, "obligations"):
            audits.add(obligation)
    resource_ids = tuple(sorted(set(allowed)))
    obligations = tuple(sorted(audits))
    expires = min(expiries) if expiries else None
    if not expiries:
        obligations = ()
    return FilterPlan(
        subject, action, context, correlation, PROFILE_VERSION,
        version, now, resource_ids, obligations, expires,
    )


__all__ = [
    "FilterConfig",
    "FilterLot",
    "FilterPlan",
    "FilterPlanError",
    "PROFILE_VERSION",
    "plan_filter",
]
