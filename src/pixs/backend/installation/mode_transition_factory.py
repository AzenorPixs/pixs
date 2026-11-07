"""Fabrique publique fermee C08 : construit participant/ports/scopes chez le proprietaire."""
from __future__ import annotations
from dataclasses import dataclass
from django.db import DatabaseError, InterfaceError
from django.utils.connection import ConnectionDoesNotExist
from pixs.backend.installation.marker import MarkerInvalid
from pixs.backend.installation.result_writer import _native_context
from pixs.backend.installation.mode_commands import MODE_SERIALIZER_VERSION, ModeCommandInput, check_mode_command, mode_action_ref, mode_command_type, mode_content_sha256, mode_resource_ref
from pixs.backend.installation.mode_governance import C10ModeGovernanceAdapter
from pixs.backend.installation.mode_participant import C08ModeIdempotenceParticipant
from pixs.backend.installation.mode_reader import C08InstalledModeReader
from pixs.backend.installation.mode_values import ModeOperationKind
from pixs.core.audit_contracts import AuditError
from pixs.core.authz.ports import PortError
from pixs.core.dto import CommandEnvelope, CoreInputInvalid
from pixs.core.ports import CorePortError, CoreServicePorts, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.services_common import CoreServiceError
from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider, RuntimeWaiverRequest
from pixs.core.services_runtime_facts import RuntimeResourceOwner, RuntimeTrustedFactsProvider
from pixs.core.services_runtime_filter import RuntimeSourceFilterProvider
from pixs.core.services_runtime_store import CoreAuthorizationStore
from pixs.core.services_transaction_types import AppliedMutation, MutationContext
from pixs.core.audit_sink import PostgresAuditParticipant, PostgresAuditSink
from pixs.core.authz.filter_plan import FilterConfig, FilterPlanError
from pixs.auth.invocation import AuthInvocationSource
__all__ = ["ModesTransition", "build_modes_transition"]
@dataclass(frozen=True, slots=True, repr=False)
class ModesTransition:
    ports: CoreServicePorts
    apply: object
    resource_id: str
    action_id: str
    command_type: str
    content_sha256: str
    lock_scopes: tuple
    max_ref_len: int
def _text(v: str, lim: int) -> None:
    if type(v) is not str or not 0 < len(v) <= lim or not v.isprintable():
        raise CorePortError()
    try:
        v.encode("utf-8")
    except UnicodeError:
        raise CorePortError() from None
def build_modes_transition(*, using: str, inspection_using: str, clock: object, envelope: CommandEnvelope, command: ModeCommandInput, reader: C08InstalledModeReader, store: CoreAuthorizationStore, authentication_source: AuthInvocationSource, audit: object, filter_config: FilterConfig, governance: object, waiver_request: object) -> ModesTransition:
    if type(reader) is not C08InstalledModeReader:
        raise CorePortError()
    if type(store) is not CoreAuthorizationStore:
        raise CorePortError()
    if type(authentication_source) is not AuthInvocationSource:
        raise CorePortError()
    if type(envelope) is not CommandEnvelope:
        raise CorePortError()
    if type(command) is not ModeCommandInput:
        raise CorePortError()
    if type(filter_config) is not FilterConfig:
        raise CorePortError()
    try:
        m = object.__getattribute__(reader, "_marker")
        ru = object.__getattribute__(reader, "_using")
        ri = object.__getattribute__(reader, "_inspection")
        rinst = object.__getattribute__(reader, "_installation")
        rclock = object.__getattribute__(reader, "_clock")
        rtarget = object.__getattribute__(reader, "_target")
        m.__post_init__()
    except (AttributeError, MarkerInvalid):
        raise CorePortError() from None
    lim = m.max_ref_len
    for v in (using, inspection_using):
        _text(v, lim)
    if using == inspection_using or ru != using or ri != inspection_using or rclock is not clock:
        raise CorePortError()
    if not callable(getattr(clock, "now", None)):
        raise CorePortError()
    try:
        envelope.__post_init__()
        check_mode_command(command, max_ref_len=lim)
        filter_config.__post_init__()
    except (CoreInputInvalid, ValueError):
        raise CorePortError() from None
    try:
        sinst = object.__getattribute__(store, "_installation")
    except AttributeError:
        raise CorePortError() from None
    if store.alias != using or sinst != command.installation_ref or rinst != command.installation_ref:
        raise CorePortError()
    try:
        tpl = object.__getattribute__(authentication_source, "_template")
        if tpl is None or tpl._request != envelope.request or tpl._alias != using or tpl._operation != envelope.operation_id or tpl._clock is not clock:
            raise CorePortError()
    except AttributeError:
        raise CorePortError() from None
    if audit is not None:
        if type(audit) is not PostgresAuditParticipant or audit.clock is not clock or audit.peer_alias != inspection_using:
            raise CorePortError()
        try:
            audit.__post_init__()
        except AuditError:
            raise CorePortError() from None
    if governance is not None and type(governance) is not C10ModeGovernanceAdapter:
        raise CorePortError()
    if governance is not None and (governance._clock is not clock or governance._using != using or governance._installation != command.installation_ref):
        raise CorePortError()
    if waiver_request is not None and type(waiver_request) is not RuntimeWaiverRequest:
        raise CorePortError()
    if envelope.serializer_version != MODE_SERIALIZER_VERSION or command.installation_ref != rinst:
        raise CorePortError()
    try:
        exp_res = mode_resource_ref(command, max_ref_len=lim)
        exp_act = mode_action_ref(command.kind)
        exp_hash = mode_content_sha256(command, max_ref_len=lim)
        exp_type = mode_command_type(command.kind)
    except ValueError:
        raise CorePortError() from None
    req = envelope.request
    if req.resource_id != exp_res or req.action_id != exp_act or envelope.content_sha256 != exp_hash or req.context.scope_type is not ScopeType.PLATFORM:
        raise CorePortError()
    if req.subject_id != command.actor_ref or envelope.idempotency_key != command.idempotency_key:
        raise CorePortError()
    cat = store.catalog
    if command.actor_ref not in cat.subject_ids or exp_res not in cat.resource_ids or req.context not in cat.scope_contexts:
        raise CorePortError()
    for k in (mode_action_ref(ModeOperationKind.FINALIZE_CONFIGURATION), mode_action_ref(ModeOperationKind.ENTER_MAINTENANCE), mode_action_ref(ModeOperationKind.EXIT_MAINTENANCE)):
        if k not in cat.action_ids:
            raise CorePortError()
    def _mode_ownership(resource_id: str, *, context: ScopeContext, alias: str, operation_id: str) -> ResourceOwnership | None:
        if resource_id != exp_res or context != req.context or context.scope_type is not ScopeType.PLATFORM or alias != using or operation_id != envelope.operation_id:
            raise CorePortError()
        native = _native_context(alias)
        try:
            from pixs.backend.c08_installation_result_record import C08InstallationResultRecord
            prow = C08InstallationResultRecord.objects.using(alias).filter(installation_ref=command.installation_ref).first()
        except (DatabaseError, InterfaceError, ConnectionDoesNotExist):
            raise CorePortError() from None
        if prow is None or prow.database_target_ref != rtarget or prow.result_ref != "pixs.core.binding:" + command.installation_ref:
            return None
        reader._check_native_historic(prow.pid, prow.xid, prow.database_oid, prow.schema_oid, native[3], native[4])
        reader._check_date(prow.prepared_at, reader._now())
        reader._check_governed(prow, status="GOVERNED")
        return ResourceOwnership(resource_id, context)
    mode_owner = RuntimeResourceOwner("pixs.backend.modes:", _mode_ownership)
    try:
        facts = RuntimeTrustedFactsProvider(store=store, authentication_source=authentication_source, request=req, operation_id=envelope.operation_id, additional_owners=(mode_owner,))
        decider = RuntimeAuthorizationDecider(store=store, facts_provider=facts, clock=clock, request=req, operation_id=envelope.operation_id, waiver_request=waiver_request)
        sink = None if audit is None else PostgresAuditSink(participant=audit, alias=using, context=req.context, operation_id=envelope.operation_id)
        filt = RuntimeSourceFilterProvider(store, facts, clock, sink, filter_config, req, envelope.operation_id, waiver_request=waiver_request)
    except (PortError, AuditError, FilterPlanError):
        raise CorePortError() from None
    participant = C08ModeIdempotenceParticipant(using=using, inspection_using=inspection_using, clock=clock, envelope=envelope, command=command, reader=reader, decider=decider, governance=governance)
    class _NoModeOutboundEffects:
        def stage_envelope(self, *, alias: str, operation_id: str, transaction_token: str, context: ScopeContext, correlation_id: str, request: object, decision: object, causation_id: object, governance_waived: bool, governance_ref: object, payload_refs: tuple, outbound_declarations: tuple = ()) -> object:
            raise CorePortError()
        def verify_staged(self, proof: TransactionProof) -> None:
            raise CorePortError()
        def reconcile_unknown(self, proof: TransactionProof) -> str:
            raise CorePortError()
    outbox = _NoModeOutboundEffects()
    ports = CoreServicePorts(facts_provider=facts, clock=clock, decider=decider, filter_provider=filt, audit=audit, idempotence=participant, outbox=outbox, declarations=None, governance=governance)
    def _apply(ctx: MutationContext) -> AppliedMutation:
        return participant.apply_transition(ctx)
    try:
        base = ("installation:" + command.installation_ref,)
        extra = store.required_scopes(context=req.context, actor_ref=req.subject_id)
    except CoreServiceError:
        raise CorePortError() from None
    scopes = tuple(sorted(set(base + tuple(extra))))
    if type(lim) is bool or type(lim) is not int or lim <= 0:
        raise CorePortError()
    return ModesTransition(ports=ports, apply=_apply, resource_id=exp_res, action_id=exp_act, command_type=exp_type, content_sha256=exp_hash, lock_scopes=scopes, max_ref_len=lim)
