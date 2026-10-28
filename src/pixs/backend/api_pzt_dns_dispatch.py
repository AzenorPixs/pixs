"""Assemblage serveur et dispatch C14, distincts de la frontière de transport HTTP."""
from __future__ import annotations

import copy
import hashlib
from dataclasses import dataclass

from pixs.auth.activity import UserActivityEvidence
from pixs.auth.api_request_source import ApiRequestSource, ResolvedActor
from pixs.auth.contracts import AuthServiceError, Facade
from pixs.auth.services import PostgresLocalAuthService
from pixs.auth.tokens import OpaqueToken, TokenKind
from pixs.backend.api_core_errors_catalog import classify_error
from pixs.backend.api_pzt_dns_catalog import C14_HTTP_BINDINGS, c14_http_binding
from pixs.backend.api_pzt_dns_inputs import C14HttpInputError, parse_c14_http_input
from pixs.core.audit_sink import PostgresAuditParticipant
from pixs.core.authz.ports import Request
from pixs.core.command_metadata import CommandMetadata
from pixs.core.services_runtime_store import CoreAuthorizationStore
from pixs.core.services_runtime_decider import RuntimeWaiverRequest
from pixs.dns.services import DnsCommandResult, PostgresDnsService
from pixs.pzt.identifiers import new_uuid7
from pixs.pzt.services import PztCommandResult, PostgresPztService

__all__ = ["C14ApiComposition", "C14DispatchResult", "C14WaiverIntent", "dispatch_c14_operation"]


def _text(value):
    if type(value) is not str or not value or "\x00" in value:
        raise C14HttpInputError()
    try:
        value.encode("utf-8")
    except UnicodeError:
        raise C14HttpInputError() from None
    return value


@dataclass(frozen=True, slots=True, repr=False)
class C14ApiComposition:
    alias: str
    peer_alias: str
    request_source: ApiRequestSource
    auth_service: PostgresLocalAuthService
    store: CoreAuthorizationStore
    audit: PostgresAuditParticipant
    clock: object
    pzt_policy_source: object
    dns_policy_source: object
    interactive_commands: frozenset[str]

    def __post_init__(self):
        for value in (self.alias, self.peer_alias):
            _text(value)
        if (self.alias == self.peer_alias or type(self.request_source) is not ApiRequestSource
                or type(self.auth_service) is not PostgresLocalAuthService
                or type(self.store) is not CoreAuthorizationStore or self.store.alias != self.alias
                or type(self.audit) is not PostgresAuditParticipant or self.audit.peer_alias != self.peer_alias
                or not callable(getattr(self.clock, "now", None))):
            raise C14HttpInputError()
        for source in (self.pzt_policy_source, self.dns_policy_source):
            if not callable(getattr(source, "resolve", None)):
                raise C14HttpInputError()
        names = {b.name for b in C14_HTTP_BINDINGS if b.kind == "COMMAND"}
        if (type(self.interactive_commands) is not frozenset
                or any(type(n) is not str or n not in names for n in self.interactive_commands)):
            raise C14HttpInputError()

    def service(self, owner, *, token, kind):
        if (type(token) is not OpaqueToken or type(kind) is not TokenKind
                or kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION)):
            raise C14HttpInputError()

        def authentication(*, request, alias, operation_id):
            return self.request_source.token_verifier(
                request=request, alias=alias, operation_id=operation_id, token=token, kind=kind)

        arguments = dict(alias=self.alias, peer_alias=self.peer_alias, store=self.store,
                         clock=self.clock, audit=self.audit, auth_factory=authentication)
        if type(owner) is str and owner == "pixs.pzt":
            return PostgresPztService(**arguments, policy_source=self.pzt_policy_source)
        if type(owner) is str and owner == "pixs.dns":
            return PostgresDnsService(**arguments, policy_source=self.dns_policy_source)
        raise C14HttpInputError()


@dataclass(frozen=True, slots=True)
class C14WaiverIntent:
    """Demande explicite ; seul C04 décide selon les autorités fraîches du sujet."""
    audit: bool
    governance: bool

    def __post_init__(self):
        if type(self.audit) is not bool or type(self.governance) is not bool:
            raise C14HttpInputError()


@dataclass(frozen=True, slots=True, repr=False)
class C14DispatchResult:
    status: int
    body: dict

    def json_payload(self):
        return copy.deepcopy(self.body)


@dataclass(frozen=True, slots=True, repr=False)
class _CompletedSource:
    evidence: UserActivityEvidence
    owner: str
    alias: str
    operation_id: str

    def verify_completed_interactive(self, reference, *, request, session_id, alias, operation_id):
        evidence = self.evidence
        if (type(evidence) is not UserActivityEvidence or type(request) is not Request
                or self.owner not in ("pixs.pzt", "pixs.dns")
                or reference != evidence.event_ref or session_id != evidence.session_id
                or alias != self.alias or operation_id != self.operation_id
                or evidence.owner_component != self.owner
                or request.subject_id != evidence.actor_ref or request.context != evidence.context
                or request.action_id != "pixs.auth.session.activity"
                or request.resource_id != "pixs.auth.session:" + str(session_id)):
            raise AuthServiceError("AUTH_DENIED")
        evidence.__post_init__()
        request.__post_init__()
        return evidence


def _activity(composition, *, owner, actor, result, correlation_id, token, kind):
    event_ref = owner + ".activity:" + result.operation_id
    command = composition.request_source.auth_command(
        actor=actor, resource_id="pixs.auth.session:" + str(actor.session_id),
        action_id="pixs.auth.session.activity", correlation_id=correlation_id,
        decision_id="c14-activity-" + result.operation_id,
        idempotency_key=hashlib.sha256(event_ref.encode("utf-8")).hexdigest())
    evidence = UserActivityEvidence(event_ref, actor.identity_ref, actor.session_id, actor.context,
                                   composition.clock.now(), owner, result.operation_id)
    source = _CompletedSource(evidence, owner, composition.alias, command.operation_id)
    composition.auth_service.record_activity(
        command, token, activity_reference=event_ref, activity_source=source, kind=kind)


def dispatch_c14_operation(composition, *, owner, kind, name, payload, actor, token, token_kind,
                           correlation_id, idempotency_key=None, waiver_intent=None):
    """Port serveur : HTTPS/Host/Origin/CSRF restent à prouver par sa frontière HTTP.

    L'acteur et le justificatif viennent de la source Auth serveur. Le service
    revalide C03/C04/C05 dans sa transaction ; ce port ne reçoit aucun fait client.
    """
    if type(composition) is not C14ApiComposition or type(actor) is not ResolvedActor:
        raise C14HttpInputError()
    composition.__post_init__()
    actor.__post_init__()
    binding = c14_http_binding(owner, kind, name)
    if (type(token) is not OpaqueToken or type(token_kind) is not TokenKind
            or token_kind not in (TokenKind.ACCESS, TokenKind.WEB_SESSION)):
        raise C14HttpInputError()
    expected_facade = Facade.WEB if token_kind is TokenKind.WEB_SESSION else Facade.API
    if actor.facade is not expected_facade or actor.session_id is None:
        raise C14HttpInputError()
    if type(payload) is not dict:
        raise C14HttpInputError()
    resource = _text(payload.get("resource_id"))
    correlation = _text(correlation_id)
    operation = str(new_uuid7())
    request = composition.request_source.request(
        actor=actor, resource_id=resource, action_id=binding.name,
        correlation_id=correlation, decision_id=str(new_uuid7()))
    metadata = None
    if binding.kind == "COMMAND":
        metadata = CommandMetadata(operation, (correlation,), (), request.context, binding.name,
                                   request.subject_id, _text(idempotency_key))
    elif idempotency_key is not None:
        raise C14HttpInputError()
    dto = parse_c14_http_input(binding.owner, binding.kind, binding.name, payload,
                               request=request, metadata=metadata)
    waiver_request = None
    if waiver_intent is not None:
        if type(waiver_intent) is not C14WaiverIntent:
            raise C14HttpInputError()
        waiver_intent.__post_init__()
        waiver_request = RuntimeWaiverRequest(request, composition.alias, operation,
                                             waiver_intent.audit, waiver_intent.governance)
    service = composition.service(binding.owner, token=token, kind=token_kind)
    if binding.owner == "pixs.pzt":
        methods = {"declare_desired_pzt": service.declare_desired, "retire_desired_pzt": service.retire_desired,
                   "get_desired_pzt": service.get_desired, "get_applied_pzt": service.get_applied}
        result_type = PztCommandResult
    else:
        methods = {"declare_desired_dns": service.declare_desired, "retire_desired_dns": service.retire_desired,
                   "declare_name": service.declare_name, "retire_name": service.retire_name,
                   "get_desired_dns": service.get_desired, "get_applied_dns": service.get_applied,
                   "resolve_view_policy": service.resolve_view_policy}
        result_type = DnsCommandResult
    meta = {"correlation_id": correlation,
            "context": {"scope_type": request.context.scope_type.value,
                        "tenant_id": request.context.tenant_id, "scope_id": request.context.scope_id}}
    if binding.kind == "QUERY":
        data = methods[binding.name](dto, operation_id=operation, waiver_request=waiver_request)
        if type(data) is not dict:
            raise C14HttpInputError()
        return C14DispatchResult(200, {"data": data, "meta": meta, "links": {}})
    result = methods[binding.name](dto, waiver_request=waiver_request)
    if (type(result) is not result_type or result.resource_id != resource
            or type(result.replayed) is not bool
            or result.outcome not in ("SUCCEEDED", "UNKNOWN")
            or result.audit_disposition not in ("AUDITED", "WAIVED", "UNKNOWN")
            or (result.outcome == "SUCCEEDED"
                and (type(result.config_revision) is not int or result.config_revision < 1
                     or result.audit_disposition not in ("AUDITED", "WAIVED")))
            or (result.outcome == "UNKNOWN" and result.config_revision is not None)
            or (not result.replayed and result.operation_id != operation)):
        raise C14HttpInputError()
    status = 200 if result.outcome == "SUCCEEDED" else 202
    if (status == 200 and expected_facade is Facade.WEB
            and binding.name in composition.interactive_commands):
        if result.replayed or result.operation_id != operation:
            meta["activity"] = {"status": "REPLAY_IGNORED"}
        else:
            try:
                _activity(composition, owner=binding.owner, actor=actor, result=result,
                          correlation_id=correlation, token=token, kind=token_kind)
            except Exception as activity_error:
                # Le résultat métier est déjà confirmé ; la défaillance Auth reste distincte.
                meta["activity"] = {"status": "NOT_RECORDED", "error_code": classify_error(activity_error).code}
            else:
                meta["activity"] = {"status": "RECORDED"}
    return C14DispatchResult(status, {"data": result.record(), "meta": meta, "links": {}})
