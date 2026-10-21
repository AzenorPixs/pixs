"""Revalidation Auth sous transaction ; aucune admission ni mutation métier.

Les fabriques ne livrent pas de session. La composition serveur fournit seule
les ports de confiance, assurance et faits Core ; aucun DTO client ne les remplace.
C04 acquiert ses gardes avant revalidate. REFRESH ne permet jamais un accès.
"""
from __future__ import annotations

import datetime
import hashlib
import hmac
import threading
from dataclasses import dataclass
from typing import Protocol

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import connections
from pixs.auth.identifiers import parse_identity_reference, identity_reference
from pixs.auth.passwords import verify_password, AuthPasswordError
from pixs.auth.tokens import OpaqueToken, TokenKind, token_fingerprint
from pixs.auth.policy import PolicyRule, SessionLimits, SessionCategory, resolve_policy
from pixs.core.authz.ports import AuthenticationContext, RevocationStatus, Request
from pixs.core.authz.policy import IdentityAssurance, AuthenticationAssurance, FederationTrust
from pixs.core.dto import CorePageItem
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext, ScopeType


class AuthVerificationError(CorePortError):
    def __init__(self):
        ValueError.__init__(self, "Authentification courante non vérifiable.")
        self.code = "AUTH_VERIFICATION_FAILED"
        self.element = "auth_verification"
        self.step = "revalidate_auth"


def _text(value):
    if type(value) is not str or not value or len(value) > 1024:
        raise AuthVerificationError()


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise AuthVerificationError()
    return value


@dataclass(frozen=True, slots=True, repr=False)
class LocalTrustProfile:
    profile_id: str
    version: str
    provider_id: str
    issuer: str
    federation_trust: FederationTrust

    def __post_init__(self):
        from pixs.kernel.manifest.semver import parse_version
        for name in ("profile_id", "version", "provider_id", "issuer"):
            _text(getattr(self, name))
        parse_version(self.version)
        if type(self.federation_trust) is not FederationTrust:
            raise AuthVerificationError()


class LocalTrustSource(Protocol):
    def resolve(self, profile_id: str, request: Request, *, alias: str, operation_id: str) -> LocalTrustProfile: ...


class IdentityAssuranceSource(Protocol):
    def resolve(self, identity_ref: str, request: Request, *, alias: str, operation_id: str) -> IdentityAssurance: ...


def _native(alias):
    conn = connections[alias]
    if conn.vendor != "postgresql" or not conn.in_atomic_block:
        raise AuthVerificationError()
    with conn.cursor() as cursor:
        cursor.execute("SELECT pg_backend_pid(),txid_current(),(SELECT oid FROM pg_database WHERE datname=current_database()),(SELECT oid FROM pg_namespace WHERE nspname=current_schema()),current_schema(),current_schemas(false)")
        pid, xid, db_oid, schema_oid, schema, paths = cursor.fetchone()
    if list(paths) != [schema] or any(type(v) is not int or v < 1 for v in (pid, xid, db_oid, schema_oid)):
        raise AuthVerificationError()
    return conn.connection, (pid, xid, db_oid, schema_oid)


def acquire_auth_policy_guard(alias: str, *, exclusive: bool) -> None:
    """Les producteurs de politiques doivent prendre la même garde en exclusif."""
    if type(exclusive) is not bool:
        raise AuthVerificationError()
    _, native = _native(alias)
    material = b"pixs.auth.policy.v1:" + str(native[2]).encode("ascii") + b":" + str(native[3]).encode("ascii")
    key = int.from_bytes(hashlib.sha256(material).digest()[:8], "big", signed=True)
    function = "pg_advisory_xact_lock" if exclusive else "pg_advisory_xact_lock_shared"
    with connections[alias].cursor() as cursor:
        cursor.execute("SELECT " + function + "(%s)", (key,))


def _policy(alias, request, category):
    from pixs.auth.models import AuthPolicyRow
    rows = list(AuthPolicyRow.objects.using(alias).filter(is_current=True, category=category.value).order_by("id")[:1025])
    if len(rows) > 1024:
        raise AuthVerificationError()
    rules = []
    for row in rows:
        try:
            row.full_clean(validate_unique=False, validate_constraints=False)
        except ValidationError:
            raise AuthVerificationError() from None
        ctx = ScopeContext(ScopeType(row.scope_type), row.tenant_id, row.scope_id)
        rules.append(PolicyRule(row.policy_id, row.policy_version, ctx, category,
                                SessionLimits(row.idle_seconds, row.absolute_seconds, row.access_seconds, row.freshness_seconds, row.max_sessions)))
    return resolve_policy(request.context, category, tuple(rules))


_KEY = object()
_RENEWAL = object()


class AuthAuthenticationVerifier:
    """Objet serveur d'une seule invocation, lié à la première TX réelle utilisée."""
    __slots__ = ("_request", "_alias", "_operation", "_profile", "_trust", "_assurance", "_facts", "_clock", "_binding", "_credential", "_hash", "_binding_version", "_credential_version", "_gate_generations", "_time", "_category", "_digest", "_kind", "_session", "_transaction", "_mutex", "_purpose")

    def __init__(self, key, *, request, alias, operation_id, profile, trust_source, assurance_source, facts_reader, clock, binding, credential, gate, verified_at, category, digest=None, kind=None, session=None, purpose=None):
        if key is not _KEY or type(request) is not Request or type(profile) is not LocalTrustProfile:
            raise AuthVerificationError()
        request.__post_init__()
        parse_identity_reference(request.subject_id)
        profile.__post_init__()
        for value in (alias, operation_id):
            _text(value)
        if type(category) is not SessionCategory:
            raise AuthVerificationError()
        for port, method in ((trust_source, "resolve"), (assurance_source, "resolve"), (facts_reader, "read_facts"), (clock, "now")):
            if not callable(getattr(port, method, None)):
                raise AuthVerificationError()
        if identity_reference(gate.pk) != request.subject_id or binding.identity_id != gate.pk or credential.binding_id != binding.pk:
            raise AuthVerificationError()
        if (binding.provider_id, binding.issuer) != (profile.provider_id, profile.issuer) or not binding.enabled or not credential.enabled:
            raise AuthVerificationError()
        if purpose is not None and (purpose is not _RENEWAL or kind is not TokenKind.REFRESH or request.action_id != "pixs.auth.session.renew" or request.resource_id != "pixs.auth.session:"+str(session)):
            raise AuthVerificationError()
        self._purpose = purpose
        self._request, self._alias, self._operation = request, alias, operation_id
        self._profile, self._trust, self._assurance, self._facts, self._clock = profile, trust_source, assurance_source, facts_reader, clock
        self._binding, self._credential = binding.pk, credential.pk
        self._hash = hashlib.sha256(credential.password_hash.encode("utf-8")).digest()
        self._binding_version, self._credential_version = binding.version, credential.version
        self._gate_generations = (gate.session_generation, gate.credential_generation, gate.core_identity_version)
        self._time, self._category = _utc(verified_at), category
        self._digest, self._kind, self._session = digest, kind, session
        self._transaction = None
        self._mutex = threading.RLock()

    def revalidate(self, request: Request, *, alias: str, operation_id: str) -> tuple[AuthenticationContext, RevocationStatus]:
        with self._mutex:
            try:
                return self._revalidate_locked(request, alias=alias, operation_id=operation_id)
            except ObjectDoesNotExist:
                raise AuthVerificationError() from None

    def _revalidate_locked(self, request, *, alias, operation_id):
        from pixs.auth import models as m
        if type(request) is not Request or request != self._request or alias != self._alias or operation_id != self._operation:
            raise AuthVerificationError()
        physical, native = _native(alias)
        if self._transaction is None:
            self._transaction = (physical, native)
        elif self._transaction[0] is not physical or self._transaction[1] != native:
            raise AuthVerificationError()
        current_profile = self._trust.resolve(self._profile.profile_id, request, alias=alias, operation_id=operation_id)
        if type(current_profile) is not LocalTrustProfile or current_profile != self._profile:
            raise AuthVerificationError()
        current_profile.__post_init__()
        facts = self._facts.read_facts("IDENTITY", (request.subject_id,), request.context, alias, 1)
        if type(facts) is not tuple or len(facts) != 1 or type(facts[0]) is not CorePageItem:
            raise AuthVerificationError()
        fact = facts[0]
        fact.__post_init__()
        if (fact.kind, fact.ref, fact.context, fact.persistence_state) != ("IDENTITY", request.subject_id, request.context, "ACTIVE"):
            raise AuthVerificationError()
        if dict(fact.data).get("state") != "ACTIVE":
            raise AuthVerificationError()
        acquire_auth_policy_guard(alias, exclusive=False)
        gate = m.AuthAccountGate.objects.using(alias).select_for_update().get(pk=parse_identity_reference(request.subject_id))
        binding = m.AuthBinding.objects.using(alias).select_for_update().get(pk=self._binding)
        credential = m.AuthPasswordCredential.objects.using(alias).select_for_update().get(pk=self._credential)
        if (gate.persistence_state != "ACTIVE" or binding.persistence_state != "ACTIVE" or credential.persistence_state != "ACTIVE"
                or not binding.enabled or not credential.enabled or binding.identity_id != gate.pk or credential.binding_id != binding.pk
                or binding.version != self._binding_version or credential.version != self._credential_version
                or (binding.provider_id, binding.issuer) != (current_profile.provider_id, current_profile.issuer)
                or (gate.session_generation, gate.credential_generation, gate.core_identity_version) != self._gate_generations
                or gate.core_identity_version != fact.version
                or not hmac.compare_digest(hashlib.sha256(credential.password_hash.encode("utf-8")).digest(), self._hash)):
            raise AuthVerificationError()
        now = _utc(self._clock.now())
        policy = _policy(alias, request, self._category).rule.limits
        if not self._time <= now:
            raise AuthVerificationError()
        authenticated_at = self._time
        expires_at = self._time + datetime.timedelta(seconds=policy.absolute_seconds)
        preparation_expires_at = self._time + datetime.timedelta(seconds=policy.freshness_seconds)
        session_id = None
        if self._digest is None:
            if not now < preparation_expires_at:
                raise AuthVerificationError()
        else:
            if self._kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION) and not (self._purpose is _RENEWAL and self._kind is TokenKind.REFRESH):
                raise AuthVerificationError()
            session = m.AuthSession.objects.using(alias).select_for_update().get(pk=self._session)
            token = m.AuthToken.objects.using(alias).select_for_update().get(digest=self._digest)
            if (session.identity_id != gate.pk or session.binding_id != binding.pk or session.credential_id != credential.pk
                    or session.state != "ACTIVE" or session.persistence_state != "ACTIVE" or session.category != self._category.value
                    or (session.scope_type, session.tenant_id, session.scope_id) != (request.context.scope_type.value, request.context.tenant_id, request.context.scope_id)
                    or session.generation != gate.session_generation or session.credential_revision != credential.version
                    or session.binding_revision != binding.version or session.core_identity_version != fact.version
                    or token.session_id != session.pk or token.state != "ACTIVE" or token.persistence_state != "ACTIVE"
                    or token.kind != self._kind.value or token.session_generation != session.token_generation
                    or token.consumed_at is not None or token.consumed_operation_ref is not None
                    or (session.facade == "WEB") != (self._kind is TokenKind.WEB_SESSION)):
                raise AuthVerificationError()
            authenticated_at = session.authenticated_at
            if not session.created_at <= authenticated_at <= session.last_activity_at <= now:
                raise AuthVerificationError()
            access_cap = token.issued_at + datetime.timedelta(seconds=policy.access_seconds) if self._kind is TokenKind.ACCESS else session.absolute_expires_at
            expires_at = min(access_cap, token.expires_at, session.idle_expires_at, session.absolute_expires_at, session.context_expires_at,
                             session.last_activity_at+datetime.timedelta(seconds=policy.idle_seconds),
                             authenticated_at+datetime.timedelta(seconds=policy.absolute_seconds))
            if not authenticated_at <= token.issued_at <= now < expires_at:
                raise AuthVerificationError()
            session_id = str(session.pk)
        level = self._assurance.resolve(request.subject_id, request, alias=alias, operation_id=operation_id)
        if type(level) is not IdentityAssurance:
            raise AuthVerificationError()
        for source in (self._trust, self._assurance):
            validity = getattr(source, "context_valid_until", None)
            if callable(validity):
                bound = _utc(validity(request, alias=alias, operation_id=operation_id))
                if not now < bound:
                    raise AuthVerificationError()
                expires_at = min(expires_at, bound)
        context = AuthenticationContext(request.subject_id, binding.provider_id, binding.issuer, binding.external_subject,
                                        authenticated_at, expires_at, ("PASSWORD",), level,
                                        AuthenticationAssurance.SINGLE_FACTOR, current_profile.federation_trust,
                                        request.context, session_id, str(credential.pk))
        return context, RevocationStatus.ACTIVE


def prepare_password_verifier(*, request: Request, alias: str, operation_id: str, profile: LocalTrustProfile, trust_source: LocalTrustSource, assurance_source: IdentityAssuranceSource, facts_reader, clock, external_subject: str, password: str, category: SessionCategory) -> AuthAuthenticationVerifier:
    from pixs.auth import models as m
    if type(profile) is not LocalTrustProfile:
        raise AuthVerificationError()
    profile.__post_init__()
    _text(external_subject)
    try:
        binding = m.AuthBinding.objects.using(alias).get(provider_id=profile.provider_id, issuer=profile.issuer, external_subject=external_subject)
        credential = m.AuthPasswordCredential.objects.using(alias).get(binding=binding)
        gate = m.AuthAccountGate.objects.using(alias).get(pk=binding.identity_id)
        valid = verify_password(password, credential.password_hash)
    except (m.AuthBinding.DoesNotExist, m.AuthPasswordCredential.DoesNotExist, m.AuthAccountGate.DoesNotExist, AuthPasswordError):
        raise AuthVerificationError() from None
    if not valid:
        raise AuthVerificationError()
    return AuthAuthenticationVerifier(_KEY, request=request, alias=alias, operation_id=operation_id, profile=profile, trust_source=trust_source, assurance_source=assurance_source, facts_reader=facts_reader, clock=clock, binding=binding, credential=credential, gate=gate, verified_at=clock.now(), category=category)


def prepare_token_verifier(*, request: Request, alias: str, operation_id: str, profile: LocalTrustProfile, trust_source: LocalTrustSource, assurance_source: IdentityAssuranceSource, facts_reader, clock, token: OpaqueToken, kind: TokenKind) -> AuthAuthenticationVerifier:
    from pixs.auth import models as m
    if kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION) or type(kind) is not TokenKind:
        raise AuthVerificationError()
    digest = token_fingerprint(token, kind)
    try:
        row = m.AuthToken.objects.using(alias).get(digest=digest, kind=kind.value)
        session = m.AuthSession.objects.using(alias).get(pk=row.session_id)
        binding = m.AuthBinding.objects.using(alias).get(pk=session.binding_id)
        credential = m.AuthPasswordCredential.objects.using(alias).get(pk=session.credential_id)
        gate = m.AuthAccountGate.objects.using(alias).get(pk=session.identity_id)
    except (m.AuthToken.DoesNotExist, m.AuthSession.DoesNotExist, m.AuthBinding.DoesNotExist, m.AuthPasswordCredential.DoesNotExist, m.AuthAccountGate.DoesNotExist):
        raise AuthVerificationError() from None
    return AuthAuthenticationVerifier(_KEY, request=request, alias=alias, operation_id=operation_id, profile=profile, trust_source=trust_source, assurance_source=assurance_source, facts_reader=facts_reader, clock=clock, binding=binding, credential=credential, gate=gate, verified_at=clock.now(), category=SessionCategory(session.category), digest=digest, kind=kind, session=session.pk)


def prepare_renewal_verifier(*, request: Request, alias: str, operation_id: str, profile: LocalTrustProfile, trust_source: LocalTrustSource, assurance_source: IdentityAssuranceSource, facts_reader, clock, token: OpaqueToken) -> AuthAuthenticationVerifier:
    """Preuve réservée à renew sur sa session exacte ; jamais un accès API ordinaire."""
    from pixs.auth import models as m
    if type(request) is not Request or request.action_id != "pixs.auth.session.renew":
        raise AuthVerificationError()
    digest = token_fingerprint(token, TokenKind.REFRESH)
    try:
        row = m.AuthToken.objects.using(alias).get(digest=digest, kind="REFRESH")
        session = m.AuthSession.objects.using(alias).get(pk=row.session_id)
        binding = m.AuthBinding.objects.using(alias).get(pk=session.binding_id)
        credential = m.AuthPasswordCredential.objects.using(alias).get(pk=session.credential_id)
        gate = m.AuthAccountGate.objects.using(alias).get(pk=session.identity_id)
    except (m.AuthToken.DoesNotExist, m.AuthSession.DoesNotExist, m.AuthBinding.DoesNotExist, m.AuthPasswordCredential.DoesNotExist, m.AuthAccountGate.DoesNotExist):
        raise AuthVerificationError() from None
    return AuthAuthenticationVerifier(_KEY, request=request, alias=alias, operation_id=operation_id, profile=profile, trust_source=trust_source, assurance_source=assurance_source, facts_reader=facts_reader, clock=clock, binding=binding, credential=credential, gate=gate, verified_at=clock.now(), category=SessionCategory(session.category), digest=digest, kind=TokenKind.REFRESH, session=session.pk, purpose=_RENEWAL)


__all__ = ["prepare_renewal_verifier", "acquire_auth_policy_guard", "AuthVerificationError", "LocalTrustProfile", "LocalTrustSource", "IdentityAssuranceSource", "AuthAuthenticationVerifier", "prepare_password_verifier", "prepare_token_verifier"]
