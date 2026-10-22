"""Politique sessions Auth v1 : déclarative pure, sans I/O ni privilège."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum

from pixs.core.scope.context import (
    ScopeContext,
    ScopeStructureError,
    ScopeType,
    validate_structure,
)
from pixs.kernel.manifest.semver import parse_version


class AuthPolicyError(ValueError):
    def __init__(self) -> None:
        super().__init__("Politique Auth invalide.")
        self.code = "AUTH_POLICY_INVALID"
        self.element = "auth_policy"
        self.step = "validate_policy"


class SessionCategory(Enum):
    ORDINARY = "ORDINARY"
    ADMIN = "ADMIN"


class PolicyOrigin(Enum):
    PLATFORM = "PLATFORM"
    TENANT = "TENANT"
    SCOPE = "SCOPE"


def _is_id(v: object) -> bool:
    return type(v) is str and v != ""


def _is_utc(v: object) -> bool:
    return type(v) is datetime.datetime and v.tzinfo is datetime.timezone.utc


def _is_member(v: object, enum_cls: type[Enum]) -> bool:
    if type(v) is not enum_cls:
        return False
    return any(v is m for m in tuple(enum_cls))


def _check_ctx(v: object) -> None:
    if type(v) is not ScopeContext:
        raise AuthPolicyError()
    try:
        if not _is_member(object.__getattribute__(v, "scope_type"), ScopeType):
            raise AuthPolicyError()
        validate_structure(v)
    except (ScopeStructureError, AttributeError):
        raise AuthPolicyError() from None


def _check_version(v: object) -> None:
    if type(v) is not str:
        raise AuthPolicyError()
    try:
        parse_version(v)
    except (ValueError, AttributeError):
        raise AuthPolicyError() from None


@dataclass(frozen=True, slots=True, repr=False)
class SessionLimits:
    idle_seconds: int
    absolute_seconds: int
    access_seconds: int
    freshness_seconds: int
    max_sessions: int

    def __post_init__(self) -> None:
        try:
            vals = tuple(object.__getattribute__(self, n) for n in (
                "idle_seconds", "absolute_seconds", "access_seconds",
                "freshness_seconds", "max_sessions"))
        except AttributeError:
            raise AuthPolicyError() from None
        for v in vals:
            if type(v) is bool or type(v) is not int or v <= 0:
                raise AuthPolicyError()
        idle, absolute, access, fresh, _ = vals
        if not idle <= absolute or not access <= absolute or not fresh <= absolute:
            raise AuthPolicyError()


@dataclass(frozen=True, slots=True, repr=False)
class PolicyRule:
    policy_id: str
    version: str
    context: ScopeContext
    category: SessionCategory
    limits: SessionLimits

    def __post_init__(self) -> None:
        try:
            pid = object.__getattribute__(self, "policy_id")
            ver = object.__getattribute__(self, "version")
            ctx = object.__getattribute__(self, "context")
            cat = object.__getattribute__(self, "category")
            lim = object.__getattribute__(self, "limits")
        except AttributeError:
            raise AuthPolicyError() from None
        if not _is_id(pid):
            raise AuthPolicyError()
        _check_version(ver)
        _check_ctx(ctx)
        if not _is_member(cat, SessionCategory):
            raise AuthPolicyError()
        if type(lim) is not SessionLimits:
            raise AuthPolicyError()
        lim.__post_init__()


@dataclass(frozen=True, slots=True, repr=False)
class ResolvedPolicy:
    rule: PolicyRule
    requested_context: ScopeContext
    origin: PolicyOrigin

    def __post_init__(self) -> None:
        try:
            rule = object.__getattribute__(self, "rule")
            req = object.__getattribute__(self, "requested_context")
            origin = object.__getattribute__(self, "origin")
        except AttributeError:
            raise AuthPolicyError() from None
        _rule(rule)
        _check_ctx(req)
        if not _is_member(origin, PolicyOrigin):
            raise AuthPolicyError()
        rc = object.__getattribute__(rule, "context")
        if origin is PolicyOrigin.PLATFORM:
            if not rc.scope_type is ScopeType.PLATFORM:
                raise AuthPolicyError()
        elif origin is PolicyOrigin.TENANT:
            if not rc.scope_type is ScopeType.TENANT or rc.scope_id is not None:
                raise AuthPolicyError()
            if not req.scope_type is ScopeType.TENANT or req.tenant_id != rc.tenant_id:
                raise AuthPolicyError()
        else:
            if not rc.scope_type is ScopeType.TENANT or rc.scope_id is None:
                raise AuthPolicyError()
            if not req.scope_type is ScopeType.TENANT:
                raise AuthPolicyError()
            if req.tenant_id != rc.tenant_id or req.scope_id != rc.scope_id:
                raise AuthPolicyError()


    def effective_values(self) -> tuple[tuple[str, int, str, str, str], ...]:
        return effective_values(self)


def _limits(v: object) -> SessionLimits:
    if type(v) is not SessionLimits:
        raise AuthPolicyError()
    v.__post_init__()
    return v


def _rule(v: object) -> PolicyRule:
    if type(v) is not PolicyRule:
        raise AuthPolicyError()
    v.__post_init__()
    return v


def _resolved(v: object) -> ResolvedPolicy:
    if type(v) is not ResolvedPolicy:
        raise AuthPolicyError()
    v.__post_init__()
    return v


def default_rule(category: SessionCategory) -> PolicyRule:
    if category is SessionCategory.ORDINARY:
        limits = SessionLimits(3600, 43200, 900, 300, 5)
    elif category is SessionCategory.ADMIN:
        limits = SessionLimits(900, 7200, 900, 300, 2)
    else:
        raise AuthPolicyError()
    return PolicyRule("pixs.auth.defaults", "1.0.0",
                      ScopeContext(ScopeType.PLATFORM, None, None), category, limits)


def _selector(rule: PolicyRule) -> tuple[str, str | None, str | None]:
    ctx = object.__getattribute__(rule, "context")
    st = object.__getattribute__(ctx, "scope_type")
    return (st.value, object.__getattribute__(ctx, "tenant_id"),
            object.__getattribute__(ctx, "scope_id"))


def resolve_policy(context: ScopeContext, category: SessionCategory,
                   rules: tuple[PolicyRule, ...]) -> ResolvedPolicy:
    _check_ctx(context)
    if not _is_member(category, SessionCategory):
        raise AuthPolicyError()
    if type(rules) is not tuple:
        raise AuthPolicyError()
    for r in rules:
        _rule(r)
    applicable: list[tuple[int, PolicyRule]] = []
    for r in rules:
        if not object.__getattribute__(r, "category") is category:
            continue
        rc = object.__getattribute__(r, "context")
        if rc.scope_type is ScopeType.PLATFORM:
            applicable.append((0, r))
        elif (rc.scope_type is ScopeType.TENANT and rc.scope_id is None
              and context.scope_type is ScopeType.TENANT
              and rc.tenant_id == context.tenant_id):
            applicable.append((1, r))
        elif (rc.scope_type is ScopeType.TENANT and rc.scope_id is not None
              and context.scope_type is ScopeType.TENANT
              and rc.tenant_id == context.tenant_id
              and rc.scope_id == context.scope_id):
            applicable.append((2, r))
    if not applicable:
        raise AuthPolicyError()
    keys = [_selector(r) for _, r in applicable]
    if len(set(keys)) != len(keys):
        raise AuthPolicyError()
    best = max(lvl for lvl, _ in applicable)
    chosen = [r for lvl, r in applicable if lvl == best]
    if len(chosen) != 1:
        raise AuthPolicyError()
    origin = (PolicyOrigin.PLATFORM if best == 0
              else PolicyOrigin.TENANT if best == 1 else PolicyOrigin.SCOPE)
    return ResolvedPolicy(chosen[0], context, origin)


def _policy_limits(policy: ResolvedPolicy) -> SessionLimits:
    _resolved(policy)
    rule = object.__getattribute__(policy, "rule")
    return _limits(object.__getattribute__(rule, "limits"))


def effective_values(policy: ResolvedPolicy
                     ) -> tuple[tuple[str, int, str, str, str], ...]:
    _resolved(policy)
    rule = object.__getattribute__(policy, "rule")
    origin = object.__getattribute__(policy, "origin").value
    limits = object.__getattribute__(rule, "limits")
    pid = object.__getattribute__(rule, "policy_id")
    ver = object.__getattribute__(rule, "version")
    return tuple((n, object.__getattribute__(limits, n), origin, pid, ver)
                 for n in ("idle_seconds", "absolute_seconds", "access_seconds",
                           "freshness_seconds", "max_sessions"))


def session_deadlines(policy: ResolvedPolicy, created_at: datetime.datetime,
                       last_activity_at: datetime.datetime, now: datetime.datetime,
                       valid_until: tuple[datetime.datetime, ...]
                       ) -> tuple[datetime.datetime, datetime.datetime, datetime.datetime]:
    limits = _policy_limits(policy)
    if type(valid_until) is not tuple:
        raise AuthPolicyError()
    for v in (created_at, last_activity_at, now, *valid_until):
        if not _is_utc(v):
            raise AuthPolicyError()
    if not created_at <= last_activity_at <= now:
        raise AuthPolicyError()
    try:
        absolute_exp = min((created_at + datetime.timedelta(
            seconds=object.__getattribute__(limits, "absolute_seconds")), *valid_until))
        idle_exp = min(last_activity_at + datetime.timedelta(
            seconds=object.__getattribute__(limits, "idle_seconds")), absolute_exp)
        access_exp = min(now + datetime.timedelta(
            seconds=object.__getattribute__(limits, "access_seconds")), idle_exp)
    except (AttributeError, ValueError, OverflowError):
        raise AuthPolicyError() from None
    if not now < idle_exp or not now < absolute_exp or not now < access_exp:
        raise AuthPolicyError()
    return (idle_exp, absolute_exp, access_exp)


def check_fresh(policy: ResolvedPolicy, authentication_time: datetime.datetime,
                now: datetime.datetime) -> bool:
    limits = _policy_limits(policy)
    if not _is_utc(authentication_time) or not _is_utc(now):
        raise AuthPolicyError()
    if not authentication_time <= now:
        raise AuthPolicyError()
    try:
        return ((now - authentication_time).total_seconds()
                < object.__getattribute__(limits, "freshness_seconds"))
    except (AttributeError, ValueError, OverflowError):
        raise AuthPolicyError() from None


__all__ = ["AuthPolicyError", "SessionCategory", "PolicyOrigin", "SessionLimits",
           "PolicyRule", "ResolvedPolicy", "default_rule", "resolve_policy",
           "session_deadlines", "check_fresh", "effective_values"]
