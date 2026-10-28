"""Projection du contexte WEB après contrôles Auth, C04 et C05 dans leur transaction.

Ce GET ne prolonge aucune activité et ne remet aucun jeton au navigateur.
"""
from __future__ import annotations

import datetime

from django.db import DatabaseError, InterfaceError, transaction

from pixs.auth.api_request_source import ApiRequestSource, ResolvedActor
from pixs.auth.contracts import AuthCommand, AuthServiceError, Facade
from pixs.auth.identifiers import new_uuid7, require_uuid7
from pixs.auth.invocation import AuthInvocationSource
from pixs.auth.services import PostgresLocalAuthService
from pixs.auth.tokens import OpaqueToken, TokenKind
from pixs.core.authz.ports import AuthenticationContext, PortError, RevocationStatus
from pixs.core.ports import CorePortError
from pixs.core.services_common import CoreServiceError

SHELL_CONTEXT_VERSION = '1.0.0'

_CONTEXT_READ_ACTION = 'pixs.auth.session.context.read'

__all__ = ['SHELL_CONTEXT_VERSION', 'PostgresShellContextService']


def _fail(code='AUTH_DENIED'):
    raise AuthServiceError(code)


def _check_correlation(value):
    if type(value) is not str or not value or len(value) > 128 or chr(0) in value:
        _fail('AUTH_INPUT_INVALID')
    try:
        value.encode('utf-8')
    except UnicodeError:
        _fail('AUTH_INPUT_INVALID')
    if any(c in value for c in (chr(10), chr(13))):
        _fail('AUTH_INPUT_INVALID')
    return value


class PostgresShellContextService:
    __slots__ = ('_auth_service', '_request_source', '_alias')

    def __init__(self, *, auth_service: PostgresLocalAuthService, request_source: ApiRequestSource):
        if type(auth_service) is not PostgresLocalAuthService:
            _fail('AUTH_INPUT_INVALID')
        if type(request_source) is not ApiRequestSource:
            _fail('AUTH_INPUT_INVALID')
        alias = auth_service._alias
        if type(alias) is not str or not alias:
            _fail('AUTH_INPUT_INVALID')
        if request_source._alias != alias:
            _fail('AUTH_INPUT_INVALID')
        self._auth_service = auth_service
        self._request_source = request_source
        self._alias = alias

    def __repr__(self):
        return 'PostgresShellContextService()'

    @property
    def request_source(self) -> ApiRequestSource:
        return self._request_source

    def read_context(self, *, actor: ResolvedActor, token: OpaqueToken, kind: TokenKind, correlation_id: str) -> dict:
        if type(actor) is not ResolvedActor:
            _fail('AUTH_INPUT_INVALID')
        if type(token) is not OpaqueToken or type(kind) is not TokenKind:
            _fail('AUTH_INPUT_INVALID')
        try:
            actor.__post_init__()
        except AttributeError:
            _fail('AUTH_INPUT_INVALID')
        _check_correlation(correlation_id)
        if actor.facade is not Facade.WEB:
            _fail('AUTH_DENIED')
        if kind is not TokenKind.WEB_SESSION:
            _fail('AUTH_DENIED')
        if actor.session_id is None:
            _fail('AUTH_DENIED')
        try:
            require_uuid7(actor.session_id)
        except (ValueError, TypeError, AttributeError):
            _fail('AUTH_DENIED')
        service = self._auth_service
        source_factory = self._request_source
        alias = self._alias
        resource_id = 'pixs.auth.session:' + str(actor.session_id)
        decision_id = str(new_uuid7())
        idempotency_key = 'pixs.auth.shell.context.read:' + str(new_uuid7())
        command = source_factory.auth_command(
            actor=actor, resource_id=resource_id, action_id=_CONTEXT_READ_ACTION,
            correlation_id=correlation_id, decision_id=decision_id,
            idempotency_key=idempotency_key,
        )
        if (type(command) is not AuthCommand
                or command.request.action_id != _CONTEXT_READ_ACTION
                or command.request.resource_id != resource_id):
            _fail('AUTH_INPUT_INVALID')
        service._owner()
        invocation = source_factory.open_core_source(
            request=command.request, operation_id=command.operation_id, token=token, kind=kind,
        )
        if type(invocation) is not AuthInvocationSource:
            _fail('AUTH_INPUT_INVALID')
        decider = None
        commit_attempted = False
        try:
            with transaction.atomic(using=alias, durable=True):
                decider = service._decider(command, invocation)
                decider.prepare_core_under_locks(command.request, alias, command.operation_id)
                decision = service._allow(decider.revalidate_under_locks(
                    command.request, alias=alias, operation_id=command.operation_id), command)
                metadata, audit_waived = service._metadata(command, decider, decision)
                if type(audit_waived) is not bool:
                    _fail('AUTH_DENIED')
                auth_ctx, revocation = invocation.revalidate(
                    command.request, alias=alias, operation_id=command.operation_id)
                self._check_proof(command, actor, auth_ctx, revocation)
                if not audit_waived:
                    service._audit_stage(command, decision, new_uuid7().hex)
                # La dispense ne retire jamais les contrôles finaux.
                fresh = service._allow(decider.revalidate_under_locks(
                    command.request, alias=alias, operation_id=command.operation_id), command)
                fresh_metadata, fresh_waived = service._metadata(command, decider, fresh)
                if (fresh.policy_version != decision.policy_version
                        or fresh_metadata != metadata or fresh_waived is not audit_waived):
                    _fail('AUTH_DENIED')
                auth_ctx, revocation = invocation.revalidate(
                    command.request, alias=alias, operation_id=command.operation_id)
                self._check_proof(command, actor, auth_ctx, revocation)
                current = source_factory.resolve_token(context=actor.context, token=token, kind=kind)
                if type(current) is not ResolvedActor:
                    _fail('AUTH_DENIED')
                current.__post_init__()
                if current != actor:
                    _fail('AUTH_DENIED')
                projected = self._project(current, auth_ctx)
                commit_attempted = True
            return projected
        except (DatabaseError, InterfaceError) as cause:
            if commit_attempted:
                # Aucun contexte n'est livré si le commit de l'audit reste inconnu.
                raise AuthServiceError('AUTH_COMMIT_UNKNOWN') from cause
            service._refusal(command, invocation, decider)
            raise AuthServiceError('AUTH_STATE_UNAVAILABLE') from cause
        except (CorePortError, PortError, CoreServiceError) as cause:
            service._refusal(command, invocation, decider)
            if type(cause) is AuthServiceError:
                raise
            raise AuthServiceError('AUTH_DENIED') from cause
        finally:
            invocation.close()

    def _check_proof(self, command, actor, auth_ctx, revocation):
        if type(auth_ctx) is not AuthenticationContext:
            _fail('AUTH_DENIED')
        if revocation is not RevocationStatus.ACTIVE:
            _fail('AUTH_DENIED')
        try:
            auth_ctx.__post_init__()
        except AttributeError:
            _fail('AUTH_DENIED')
        if auth_ctx.digital_identity_id != actor.identity_ref or auth_ctx.digital_identity_id != command.request.subject_id:
            _fail('AUTH_DENIED')
        if auth_ctx.context != command.request.context or auth_ctx.context != actor.context:
            _fail('AUTH_DENIED')
        if auth_ctx.session_id != str(actor.session_id):
            _fail('AUTH_DENIED')
        for value in (auth_ctx.authentication_time, auth_ctx.expires_at):
            if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
                _fail('AUTH_DENIED')
        if not auth_ctx.authentication_time <= self._auth_service._now() < auth_ctx.expires_at:
            _fail('AUTH_DENIED')
        return True

    def _project(self, actor, auth_ctx):
        now = self._auth_service._now()
        if not auth_ctx.authentication_time <= now < auth_ctx.expires_at:
            _fail('AUTH_DENIED')
        context = actor.context
        scope = {'scope_type': context.scope_type.value, 'tenant_id': context.tenant_id, 'scope_id': context.scope_id}
        return {'identity_ref': actor.identity_ref, 'scope': scope, 'session_id': str(actor.session_id), 'category': actor.category.value, 'facade': actor.facade.value, 'authentication_time': auth_ctx.authentication_time.isoformat(), 'expires_at': auth_ctx.expires_at.isoformat(), 'identity_assurance': auth_ctx.identity_assurance.value, 'authentication_assurance': auth_ctx.authentication_assurance.value, 'ui_permissions': {'status': 'UNAVAILABLE', 'items': []}}
