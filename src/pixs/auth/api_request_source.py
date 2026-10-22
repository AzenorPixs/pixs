"""Raccordement HTTP propriétaire Auth : métadonnées de requête, jamais preuve d'accès.

Le backend consommateur ne lit aucune table privée Auth. Les hints ne sont
pas des faits d'authentification : les services/verifiers C03 et C04 doivent
toujours revalider l'identité, le justificatif, le contexte et les autorités.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass

from pixs.auth.contracts import AuthCommand
from pixs.auth.identifiers import AuthIdentifierError, identity_reference, parse_identity_reference, require_uuid7
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.policy import SessionCategory
from pixs.auth.runtime_verifier import AuthVerificationError, LocalTrustProfile, prepare_token_verifier
from pixs.auth.tokens import AuthTokenError, OpaqueToken, TokenKind, token_fingerprint
from pixs.core.authz.ports import PortError, Request
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure

__all__ = ["ApiRequestSourceError", "ResolvedActor", "ApiRequestSource"]


class ApiRequestSourceError(CorePortError):
    def __init__(self):
        ValueError.__init__(self, "Justificatif Auth non résolu.")
        self.code = "API_AUTH_SOURCE_INVALID"
        self.element = "api_request_source"
        self.step = "resolve_actor"


def _fail():
    raise ApiRequestSourceError()


def _text(value, maximum):
    if type(value) is not str or not value or len(value) > maximum or chr(0) in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeError:
        _fail()
    return value


def _context(value):
    if type(value) is not ScopeContext:
        _fail()
    try:
        validate_structure(value)
    except (ScopeStructureError, AttributeError):
        _fail()
    return value


@dataclass(frozen=True, slots=True, repr=False)
class ResolvedActor:
    identity_ref: str
    context: ScopeContext
    session_id: uuid.UUID | None
    category: SessionCategory
    facade: object
    credential_id: uuid.UUID | None = None
    def __post_init__(self):
        from pixs.auth.contracts import Facade
        try:
            parse_identity_reference(self.identity_ref)
            if self.session_id is not None:
                require_uuid7(self.session_id)
            if self.credential_id is not None:
                require_uuid7(self.credential_id)
        except (AuthIdentifierError, AttributeError):
            _fail()
        _context(self.context)
        if type(self.category) is not SessionCategory or type(self.facade) is not Facade:
            _fail()


class ApiRequestSource:
    def __init__(self, *, alias, profile_id, trust_source, assurance_source,
                 facts_reader, clock, max_identifier_chars):
        if type(max_identifier_chars) is not int or max_identifier_chars < 1:
            _fail()
        _text(alias, max_identifier_chars)
        _text(profile_id, max_identifier_chars)
        for port, method in ((trust_source, "current_profile"), (trust_source, "resolve"),
                             (assurance_source, "resolve"), (facts_reader, "read_facts"), (clock, "now")):
            if not callable(getattr(port, method, None)):
                _fail()
        self._alias, self._profile_id = alias, profile_id
        self._trust, self._assurance, self._facts, self._clock = trust_source, assurance_source, facts_reader, clock
        self._maximum = max_identifier_chars

    def _profile(self, context):
        from django.db import connections
        from django.utils.connection import ConnectionDoesNotExist
        try:
            connection = connections[self._alias]
        except ConnectionDoesNotExist:
            _fail()
        if connection.vendor != "postgresql":
            _fail()
        _context(context)
        profile = self._trust.current_profile(context)
        if type(profile) is not LocalTrustProfile:
            _fail()
        try:
            profile.__post_init__()
        except (AuthVerificationError, AttributeError):
            _fail()
        if profile.profile_id != self._profile_id:
            _fail()
        return profile

    def resolve_login(self, *, context, external_subject, facade):
        from pixs.auth import models as m
        from pixs.auth.contracts import Facade
        profile = self._profile(context)
        _text(external_subject, self._maximum)
        if type(facade) is not Facade:
            _fail()
        try:
            binding = m.AuthBinding.objects.using(self._alias).get(
                provider_id=profile.provider_id, issuer=profile.issuer, external_subject=external_subject)
        except m.AuthBinding.DoesNotExist:
            _fail()
        # Orientation seulement : login vérifiera mot de passe, gate, profil,
        # activation et autorisation ; aucune assurance n'est fabriquée ici.
        return ResolvedActor(identity_reference(binding.identity_id), context, None,
                             SessionCategory.ADMIN, facade)

    def login_resource(self, actor):
        """Référence de création dérivée côté serveur, sans droit issu du hint."""
        if type(actor) is not ResolvedActor or actor.session_id is not None:
            _fail()
        actor.__post_init__()
        from pixs.core.scope.context import ScopeType
        from pixs.auth.identifiers import session_creation_reference
        resource = actor.identity_ref if actor.context.scope_type is ScopeType.PLATFORM else session_creation_reference(actor.identity_ref, actor.context)
        return _text(resource, self._maximum)

    def resolve_token(self, *, context, token, kind):
        from pixs.auth import models as m
        from pixs.auth.contracts import Facade
        if type(token) is not OpaqueToken or type(kind) is not TokenKind:
            _fail()
        if kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION, TokenKind.REFRESH):
            _fail()
        profile = self._profile(context)
        try:
            digest = token_fingerprint(token, kind)
        except AuthTokenError:
            _fail()
        try:
            row = m.AuthToken.objects.using(self._alias).get(digest=digest, kind=kind.value)
            session = m.AuthSession.objects.using(self._alias).get(pk=row.session_id)
            binding = m.AuthBinding.objects.using(self._alias).get(pk=session.binding_id)
        except (m.AuthToken.DoesNotExist, m.AuthSession.DoesNotExist, m.AuthBinding.DoesNotExist):
            _fail()
        if ((binding.provider_id, binding.issuer) != (profile.provider_id, profile.issuer)
                or binding.identity_id != session.identity_id
                or (session.scope_type, session.tenant_id, session.scope_id)
                   != (context.scope_type.value, context.tenant_id, context.scope_id)):
            _fail()
        try:
            return ResolvedActor(identity_reference(session.identity_id), context,
                                 session.pk, SessionCategory(session.category), Facade(session.facade), session.credential_id)
        except (ValueError, AuthIdentifierError):
            _fail()

    def request(self, *, actor, resource_id, action_id, correlation_id, decision_id):
        if type(actor) is not ResolvedActor:
            _fail()
        try:
            actor.__post_init__()
        except AttributeError:
            _fail()
        for value in (resource_id, action_id, correlation_id, decision_id):
            _text(value, self._maximum)
        try:
            return Request(decision_id, actor.identity_ref, resource_id, action_id, actor.context, correlation_id)
        except PortError:
            _fail()

    def auth_command(self, *, actor, resource_id, action_id, correlation_id, decision_id, idempotency_key):
        request = self.request(actor=actor, resource_id=resource_id, action_id=action_id,
                               correlation_id=correlation_id, decision_id=decision_id)
        _text(idempotency_key, self._maximum)
        # Identifiant déterministe serveur, sans secret et sans autorité.
        document = [request.subject_id, request.action_id,
                    [request.context.scope_type.value, request.context.tenant_id, request.context.scope_id],
                    idempotency_key]
        raw = json.dumps(document, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode("ascii")
        operation_id = "pixs.auth.http.v1:" + hashlib.sha256(b"pixs.auth.http.operation.v1:" + raw).hexdigest()
        return AuthCommand(request, operation_id, idempotency_key)

    def open_core_source(self, *, request, operation_id, token, kind):
        if type(request) is not Request or type(token) is not OpaqueToken or type(kind) is not TokenKind:
            _fail()
        if kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION):
            _fail()
        try:
            request.__post_init__()
        except (PortError, AttributeError):
            _fail()
        _text(operation_id, self._maximum)
        profile = self._profile(request.context)
        try:
            verifier = prepare_token_verifier(
                request=request, alias=self._alias, operation_id=operation_id,
                profile=profile, trust_source=self._trust, assurance_source=self._assurance,
                facts_reader=self._facts, clock=self._clock, token=token, kind=kind)
        except AuthVerificationError:
            _fail()
        return AuthInvocationSource(verifier)
