"""Ports PDP : frontière backend de confiance, sans backend réel."""

import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from ..scope.context import ScopeContext
from ..scope.ownership import ResourceOwnership
from .policy import (
    AuthenticationAssurance,
    Effect,
    FederationTrust,
    IdentityAssurance,
    _is_utc_aware,
)


class PortError(ValueError):
    def __init__(self):
        super().__init__("Port PDP invalide.")
        self.code = "PDP_PORT_INVALID"
        self.element = "pdp_port"
        self.step = "validate_port"


class RevocationStatus(Enum):
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    UNKNOWN = "UNKNOWN"


def _is_id(value):
    return type(value) is str and value != ""


def _is_opt_id(value):
    return value is None or _is_id(value)


@dataclass(frozen=True, slots=True, repr=False)
class Request:
    decision_id: str
    subject_id: str
    resource_id: str
    action_id: str
    context: ScopeContext
    correlation_id: str

    def __post_init__(self):
        for name in (
            "decision_id",
            "subject_id",
            "resource_id",
            "action_id",
            "correlation_id",
        ):
            if not _is_id(object.__getattribute__(self, name)):
                raise PortError()
        if type(object.__getattribute__(self, "context")) is not ScopeContext:
            raise PortError()


@dataclass(frozen=True, slots=True, repr=False)
class AuthenticationContext:
    digital_identity_id: str
    provider_id: str
    issuer: str
    external_subject: str
    authentication_time: datetime.datetime
    expires_at: datetime.datetime
    methods: tuple
    identity_assurance: IdentityAssurance
    authentication_assurance: AuthenticationAssurance
    federation_trust: FederationTrust
    context: ScopeContext
    session_id: object = None
    credential_id: object = None

    def __post_init__(self):
        for name in (
            "digital_identity_id",
            "provider_id",
            "issuer",
            "external_subject",
        ):
            if not _is_id(object.__getattribute__(self, name)):
                raise PortError()
        auth_time = object.__getattribute__(self, "authentication_time")
        expiry = object.__getattribute__(self, "expires_at")
        if not _is_utc_aware(auth_time) or not _is_utc_aware(expiry):
            raise PortError()
        if not auth_time < expiry:
            raise PortError()
        if type(object.__getattribute__(self, "methods")) is not tuple:
            raise PortError()
        if type(
            object.__getattribute__(self, "identity_assurance")
        ) is not IdentityAssurance:
            raise PortError()
        if type(
            object.__getattribute__(self, "authentication_assurance")
        ) is not AuthenticationAssurance:
            raise PortError()
        if type(
            object.__getattribute__(self, "federation_trust")
        ) is not FederationTrust:
            raise PortError()
        if type(object.__getattribute__(self, "context")) is not ScopeContext:
            raise PortError()
        for name in ("session_id", "credential_id"):
            value = object.__getattribute__(self, name)
            if value is not None and not _is_id(value):
                raise PortError()


@dataclass(frozen=True, slots=True, repr=False)
class TrustedFacts:
    subject_id: str
    resource_id: str
    action_id: str
    auth: AuthenticationContext
    ownership: ResourceOwnership
    context: ScopeContext
    revocation_status: RevocationStatus
    memberships: tuple = ()
    attributes: tuple = ()

    def __post_init__(self):
        for name in ("subject_id", "resource_id", "action_id"):
            if not _is_id(object.__getattribute__(self, name)):
                raise PortError()
        if (
            type(object.__getattribute__(self, "auth"))
            is not AuthenticationContext
        ):
            raise PortError()
        if (
            type(object.__getattribute__(self, "ownership"))
            is not ResourceOwnership
        ):
            raise PortError()
        if type(object.__getattribute__(self, "context")) is not ScopeContext:
            raise PortError()
        if (
            type(object.__getattribute__(self, "revocation_status"))
            is not RevocationStatus
        ):
            raise PortError()
        if type(object.__getattribute__(self, "memberships")) is not tuple:
            raise PortError()
        if type(object.__getattribute__(self, "attributes")) is not tuple:
            raise PortError()


@dataclass(frozen=True, slots=True, repr=False)
class AuditEvent:
    decision_id: object
    subject_id: object
    resource_id: object
    action_id: object
    context: object
    correlation_id: object
    effect: Effect
    reason_code: str
    policy_version: object
    evaluated_at: object

    def __post_init__(self):
        for name in (
            "decision_id",
            "subject_id",
            "resource_id",
            "action_id",
            "correlation_id",
        ):
            if not _is_opt_id(object.__getattribute__(self, name)):
                raise PortError()
        context = object.__getattribute__(self, "context")
        if context is not None and type(context) is not ScopeContext:
            raise PortError()
        effect = object.__getattribute__(self, "effect")
        reason = object.__getattribute__(self, "reason_code")
        if type(effect) is not Effect:
            raise PortError()
        if type(reason) is not str:
            raise PortError()
        if effect is Effect.ALLOW and reason != "ALLOWED":
            raise PortError()
        if effect is Effect.DENY and reason != "DENIED":
            raise PortError()
        version = object.__getattribute__(self, "policy_version")
        if version is not None and type(version) is not tuple:
            raise PortError()
        evaluated = object.__getattribute__(self, "evaluated_at")
        if evaluated is not None and not _is_utc_aware(evaluated):
            raise PortError()


class TrustedFactsProvider(Protocol):
    def resolve(self, request: Request) -> TrustedFacts:
        ...


class Clock(Protocol):
    def now(self) -> datetime.datetime:
        ...


class AuditSink(Protocol):
    def record(self, event: AuditEvent) -> bool:
        ...


__all__ = [
    "PortError",
    "RevocationStatus",
    "Request",
    "AuthenticationContext",
    "TrustedFacts",
    "AuditEvent",
    "TrustedFactsProvider",
    "Clock",
    "AuditSink",
]
