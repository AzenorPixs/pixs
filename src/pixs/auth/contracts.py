"""Contrats Auth v1 spécialisés ; les DTO ne prouvent ni autorité ni commit."""
from __future__ import annotations

import datetime
import uuid
from typing import Protocol, runtime_checkable
from dataclasses import dataclass
from enum import Enum
from pixs.auth.identifiers import require_uuid7, parse_identity_reference
from pixs.auth.policy import SessionCategory
from pixs.auth.tokens import OpaqueToken, TokenKind
from pixs.core.authz.ports import Request
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext, validate_structure
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

AUTH_CONTRACT_VERSION = "1.0.0"


class AuthServiceError(CorePortError):
    def __init__(self, code="AUTH_DENIED"):
        allowed = {"AUTH_DENIED", "AUTH_INPUT_INVALID", "AUTH_SESSION_LIMIT", "AUTH_OPERATION_CONFLICT", "AUTH_COMMIT_UNKNOWN", "AUTH_AUDIT_UNAVAILABLE", "AUTH_STATE_UNAVAILABLE", "AUTH_REAUTH_REQUIRED", "AUTH_TARGET_INVALID"}
        ValueError.__init__(self, "Opération Auth non confirmée.")
        self.code = code if type(code) is str and code in allowed else "AUTH_DENIED"
        self.element = "auth_service"
        self.step = "execute_auth"


def _text(value):
    if type(value) is not str or not value or len(value) > 1024:
        raise AuthServiceError("AUTH_INPUT_INVALID")


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise AuthServiceError("AUTH_INPUT_INVALID")


class Facade(Enum):
    WEB = "WEB"
    API = "API"


class AuthOutcome(Enum):
    ISSUED = "ISSUED"
    REAUTH_REQUIRED = "REAUTH_REQUIRED"
    WITHDRAWN = "WITHDRAWN"
    WITHDRAWN_AUDIT_PENDING = "WITHDRAWN_AUDIT_PENDING"
    UNKNOWN = "UNKNOWN"


class CredentialDisposition(Enum):
    CHANGED = "CHANGED"
    UNCHANGED = "UNCHANGED"
    UNKNOWN = "UNKNOWN"


class AuditDisposition(Enum):
    CONFIRMED = "CONFIRMED"
    WAIVED = "WAIVED"
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True, repr=False)
class AuthDataClassification:
    governance_ref: str
    confidentiality: ConfidentialityLevel
    personal: PersonalDataLevel
    def __post_init__(self):
        _text(self.governance_ref)
        if type(self.confidentiality) is not ConfidentialityLevel or type(self.personal) is not PersonalDataLevel:
            raise AuthServiceError("AUTH_INPUT_INVALID")
    def values(self):
        self.__post_init__()
        return dict(governance_ref=self.governance_ref, confidentiality=self.confidentiality.value, personal=self.personal.value)


@dataclass(frozen=True, slots=True, repr=False)
class AuthCommand:
    request: Request
    operation_id: str
    idempotency_key: str
    def __post_init__(self):
        if type(self.request) is not Request:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        self.request.__post_init__()
        validate_structure(self.request.context)
        parse_identity_reference(self.request.subject_id)
        for value in (self.operation_id, self.idempotency_key, self.request.decision_id, self.request.resource_id, self.request.action_id, self.request.correlation_id):
            _text(value)


@dataclass(frozen=True, slots=True, repr=False)
class LoginInput:
    external_subject: str
    password: str
    category: SessionCategory
    facade: Facade
    replace_session_id: uuid.UUID | None
    def __post_init__(self):
        _text(self.external_subject)
        if type(self.password) is not str or not self.password or type(self.category) is not SessionCategory or type(self.facade) is not Facade:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if self.replace_session_id is not None:
            require_uuid7(self.replace_session_id)


@dataclass(frozen=True, slots=True, repr=False)
class SessionInfo:
    session_id: uuid.UUID
    identity_id: uuid.UUID
    category: SessionCategory
    facade: Facade
    context: ScopeContext
    authenticated_at: datetime.datetime
    idle_expires_at: datetime.datetime
    absolute_expires_at: datetime.datetime
    def __post_init__(self):
        require_uuid7(self.session_id)
        require_uuid7(self.identity_id)
        if type(self.category) is not SessionCategory or type(self.facade) is not Facade or type(self.context) is not ScopeContext:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        validate_structure(self.context)
        for value in (self.authenticated_at, self.idle_expires_at, self.absolute_expires_at):
            _utc(value)
        if not self.authenticated_at < self.idle_expires_at <= self.absolute_expires_at:
            raise AuthServiceError("AUTH_INPUT_INVALID")


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class AuthEmission:
    access: OpaqueToken | None
    refresh: OpaqueToken | None
    cookie: OpaqueToken | None
    def __post_init__(self):
        for value in (self.access, self.refresh, self.cookie):
            if value is not None:
                if type(value) is not OpaqueToken:
                    raise AuthServiceError("AUTH_INPUT_INVALID")
                value.__post_init__()
        if not ((self.access is not None and self.refresh is not None and self.cookie is None) or (self.access is None and self.refresh is None and self.cookie is not None)):
            raise AuthServiceError("AUTH_INPUT_INVALID")


@dataclass(frozen=True, slots=True, repr=False)
class AuthResult:
    outcome: AuthOutcome
    operation_id: str
    audit: AuditDisposition
    session: SessionInfo | None
    emission: AuthEmission | None
    pending_audit_ref: str | None
    credential: CredentialDisposition | None = None
    def __post_init__(self):
        _text(self.operation_id)
        if self.credential is not None and (type(self.credential) is not CredentialDisposition or self.emission is not None or self.outcome is AuthOutcome.ISSUED):
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if type(self.outcome) is not AuthOutcome or type(self.audit) is not AuditDisposition:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if self.session is not None:
            if type(self.session) is not SessionInfo:
                raise AuthServiceError("AUTH_INPUT_INVALID")
            self.session.__post_init__()
        if self.emission is not None:
            if type(self.emission) is not AuthEmission:
                raise AuthServiceError("AUTH_INPUT_INVALID")
            self.emission.__post_init__()
        if self.outcome is AuthOutcome.ISSUED:
            if self.session is None or self.emission is None or self.audit not in (AuditDisposition.CONFIRMED, AuditDisposition.WAIVED):
                raise AuthServiceError("AUTH_INPUT_INVALID")
            if (self.session.facade is Facade.WEB) != (self.emission.cookie is not None):
                raise AuthServiceError("AUTH_INPUT_INVALID")
        elif self.emission is not None:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        pending = self.outcome is AuthOutcome.WITHDRAWN_AUDIT_PENDING
        if pending != (self.pending_audit_ref is not None) or pending != (self.audit is AuditDisposition.PENDING):
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if self.pending_audit_ref is not None:
            _text(self.pending_audit_ref)


@runtime_checkable
class AuthenticationService(Protocol):
    def login(self, command: AuthCommand, supplied: LoginInput) -> AuthResult: ...


@runtime_checkable
class SessionService(Protocol):
    def renew(self, command: AuthCommand, token: OpaqueToken) -> AuthResult: ...
    def logout(self, command: AuthCommand, token: OpaqueToken, kind: TokenKind = TokenKind.ACCESS) -> AuthResult: ...
    def revoke_session(self, command: AuthCommand, token: OpaqueToken, kind: TokenKind = TokenKind.ACCESS) -> AuthResult: ...
    def revoke_all(self, command: AuthCommand, token: OpaqueToken, kind: TokenKind = TokenKind.ACCESS) -> AuthResult: ...
    def reconcile_audit(self, command: AuthCommand, token: OpaqueToken, kind: TokenKind = TokenKind.ACCESS) -> AuthResult: ...
    def record_activity(self, command: AuthCommand, token: OpaqueToken, *, activity_reference: str, activity_source: object, kind: TokenKind = TokenKind.ACCESS) -> SessionInfo: ...


@runtime_checkable
class CredentialService(Protocol):
    def change_password(self, command: AuthCommand, token: OpaqueToken, new_password: str, kind: TokenKind = TokenKind.ACCESS) -> AuthResult: ...
    def recover_password(self, command: AuthCommand, token: OpaqueToken, new_password: str, kind: TokenKind = TokenKind.ACCESS) -> AuthResult: ...


__all__ = ["AuthenticationService", "SessionService", "CredentialService", "AUTH_CONTRACT_VERSION", "AuthServiceError", "Facade", "AuthOutcome", "AuditDisposition", "CredentialDisposition", "AuthDataClassification", "AuthCommand", "LoginInput", "SessionInfo", "AuthEmission", "AuthResult"]
