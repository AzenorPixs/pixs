"""DTO pur disjoint R01 : BootstrapOperatorFacts, structure seule, sans preuve ni droit."""

from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass
from urllib.parse import quote

from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError, validate_structure

__all__ = [
    "BootstrapOperatorError",
    "BootstrapOperatorFacts",
    "BOOTSTRAP_ACTION",
    "BOOTSTRAP_EFFECTS",
    "BOOTSTRAP_WINDOW_SECONDS",
    "validate_bootstrap_window_current",
]

BOOTSTRAP_ACTION = "pixs.core.bootstrap.apply"
BOOTSTRAP_WINDOW_SECONDS = 600
BOOTSTRAP_EFFECTS = (
    "CREATE_IDENTITY",
    "BIND_SUPER_ADMIN",
    "STAMP_CREDENTIAL",
    "CREATE_TENANT",
    "GRANT_SUPER_ADMIN_TENANT",
    "REUSE_EXISTING",
)


class BootstrapOperatorError(ValueError):
    def __init__(self):
        super().__init__("Faits opérateur R01 invalides.")
        self.code = "BOOTSTRAP_OPERATOR_INVALID"
        self.element = "bootstrap_operator_facts"
        self.step = "validate_bootstrap_operator"


def _check_str(value: object) -> None:
    if type(value) is bool or type(value) is not str or value == "":
        raise BootstrapOperatorError()


def _check_sha256(value: object) -> None:
    if type(value) is bool or type(value) is not str:
        raise BootstrapOperatorError()
    if len(value) != 64:
        raise BootstrapOperatorError()
    if value != value.lower():
        raise BootstrapOperatorError()
    for ch in value:
        if ch not in "0123456789abcdef":
            raise BootstrapOperatorError()


def _check_identity_ref(value: object) -> None:
    if type(value) is bool or type(value) is not str or value == "":
        raise BootstrapOperatorError()
    prefix = "pixs.core.identity:"
    if not value.startswith(prefix):
        raise BootstrapOperatorError()
    raw = value[len(prefix):]
    try:
        parsed = uuid.UUID(raw)
    except ValueError:
        raise BootstrapOperatorError() from None
    if parsed.version != 7:
        raise BootstrapOperatorError()
    if str(parsed) != raw:
        raise BootstrapOperatorError()


def _check_utc(value: object) -> None:
    if type(value) is not datetime.datetime:
        raise BootstrapOperatorError()
    if value.tzinfo is not datetime.timezone.utc:
        raise BootstrapOperatorError()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapOperatorFacts:
    operator_subject_ref: str
    resource_id: str
    action_id: str
    context: ScopeContext
    installation_ref: str
    plan_version: str
    authorized_actions: tuple[str, ...]
    closed_effects: tuple[str, ...]
    operator_proof_ref: str
    authorization_ref: str
    operation_id: str
    target_identity_ref: str
    target_tenant_ref: str | None
    plan_sha256: str
    valid_from: datetime.datetime
    expires_at: datetime.datetime
    key_id: str
    trust_policy_version: str
    consumed_operation_id: str | None

    def __post_init__(self) -> None:
        for name in (
            "operator_subject_ref",
            "resource_id",
            "action_id",
            "installation_ref",
            "plan_version",
            "operator_proof_ref",
            "authorization_ref",
            "operation_id",
            "target_identity_ref",
            "plan_sha256",
            "key_id",
            "trust_policy_version",
        ):
            _check_str(object.__getattribute__(self, name))
        consumed = object.__getattribute__(self, "consumed_operation_id")
        if consumed is not None:
            _check_str(consumed)
        tenant_ref = object.__getattribute__(self, "target_tenant_ref")
        if tenant_ref is not None:
            _check_str(tenant_ref)
            prefix = "pixs.core.tenant:"
            if not tenant_ref.startswith(prefix):
                raise BootstrapOperatorError()
            if tenant_ref == prefix:
                raise BootstrapOperatorError()
        ctx = object.__getattribute__(self, "context")
        if type(ctx) is not ScopeContext:
            raise BootstrapOperatorError()
        try:
            validate_structure(ctx)
        except ScopeStructureError:
            raise BootstrapOperatorError() from None
        if object.__getattribute__(ctx, "scope_type") is not ScopeType.PLATFORM:
            raise BootstrapOperatorError()
        if object.__getattribute__(ctx, "tenant_id") is not None:
            raise BootstrapOperatorError()
        if object.__getattribute__(ctx, "scope_id") is not None:
            raise BootstrapOperatorError()
        if object.__getattribute__(self, "action_id") != BOOTSTRAP_ACTION:
            raise BootstrapOperatorError()
        actions = object.__getattribute__(self, "authorized_actions")
        if (type(actions) is not tuple
                or any(type(action) is not str for action in actions)
                or actions != (BOOTSTRAP_ACTION,)):
            raise BootstrapOperatorError()
        installation = object.__getattribute__(self, "installation_ref")
        try:
            expected_resource = "pixs.core.bootstrap:" + quote(installation, safe="")
        except UnicodeError as error:
            raise BootstrapOperatorError() from error
        if object.__getattribute__(self, "resource_id") != expected_resource:
            raise BootstrapOperatorError()
        effects = object.__getattribute__(self, "closed_effects")
        if type(effects) is not tuple or len(effects) == 0:
            raise BootstrapOperatorError()
        seen: set[str] = set()
        for effect in effects:
            _check_str(effect)
            if effect not in BOOTSTRAP_EFFECTS:
                raise BootstrapOperatorError()
            if effect in seen:
                raise BootstrapOperatorError()
            seen.add(effect)
        if "REUSE_EXISTING" in seen:
            if effects != ("REUSE_EXISTING",):
                raise BootstrapOperatorError()
        else:
            for required in ("CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"):
                if required not in seen:
                    raise BootstrapOperatorError()
        if "CREATE_TENANT" in seen or "GRANT_SUPER_ADMIN_TENANT" in seen:
            if tenant_ref is None:
                raise BootstrapOperatorError()
        _check_identity_ref(object.__getattribute__(self, "target_identity_ref"))
        _check_sha256(object.__getattribute__(self, "plan_sha256"))
        valid_from = object.__getattribute__(self, "valid_from")
        expires_at = object.__getattribute__(self, "expires_at")
        _check_utc(valid_from)
        _check_utc(expires_at)
        if not valid_from < expires_at:
            raise BootstrapOperatorError()
        if (expires_at - valid_from) != datetime.timedelta(seconds=BOOTSTRAP_WINDOW_SECONDS):
            raise BootstrapOperatorError()


def validate_bootstrap_window_current(facts: BootstrapOperatorFacts, now: datetime.datetime) -> None:
    if type(facts) is not BootstrapOperatorFacts:
        raise BootstrapOperatorError()
    facts.__post_init__()
    _check_utc(now)
    valid_from = object.__getattribute__(facts, "valid_from")
    expires_at = object.__getattribute__(facts, "expires_at")
    if not valid_from <= now < expires_at:
        raise BootstrapOperatorError()
