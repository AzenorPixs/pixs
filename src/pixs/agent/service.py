"""Service prive Agent : transaction durable PG, C04 avant mutex, sans transport."""
from __future__ import annotations
import datetime
import hashlib
import json
from dataclasses import dataclass
from django.core.exceptions import ValidationError
from django.db import DatabaseError, InterfaceError, connections, transaction
from django.utils.connection import ConnectionDoesNotExist
from pixs.agent import models as m
from pixs.agent.audit_adapter import AgentAuditAdapter, AgentAuditError
from pixs.agent.authorization import AgentAuthorization, AgentAuthorizationError
from pixs.agent.contracts import AgentManagementInstruction, AgentManagementResult, AgentValidationContext
from pixs.agent.identifiers import AgentIdentifierError, canonical_head_identity, new_agent_uuid7, require_agent_uuid7
from pixs.agent.ports import AgentOperationalProfile, AgentPortsError
from pixs.agent.repository import append_observation as repo_append
from pixs.agent.repository import confirm_observation as repo_confirm
from pixs.agent.repository import persist_desired_instruction as repo_persist
from pixs.agent.repository import read_head as repo_head
from pixs.agent.repository import read_history as repo_history
from pixs.agent.repository import AgentRepositoryError, AgentTrustError
from pixs.core.audit_contracts import AuditError, encode_policy_version
from pixs.core.authz.ports import AuthenticationContext, PortError, Request, RevocationStatus
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import AuditEvent as PdpAuditEvent
from pixs.core.dto import CoreInputInvalid, GovernanceAttestation
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType, ScopeStructureError, validate_structure
from pixs.core.services_common import CoreServiceError
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState
from pixs.kernel.diagnostics import Diagnostic
__all__ = ["AgentServiceError", "PostgresAgentManagementService"]
FIXED = "Service Agent impossible."
class AgentServiceError(ValueError):
    def __init__(self, code="AGENT_SERVICE_IMPOSSIBLE"):
        super().__init__(FIXED)
        self.code = code
        self.element = "agent_service"
        self.step = "agent_act"
    def __repr__(self):
        return "AgentServiceError(<confidentiel>)"
    def __str__(self):
        return "AgentServiceError(<confidentiel>)"
def _fail(code):
    raise AgentServiceError(code) from None
def _opaque(value, limit):
    if type(value) is not str or value == "" or chr(0) in value or len(value) > limit:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True
def _check_alias_free(alias):
    if type(alias) is not str or alias == "" or chr(0) in alias:
        _fail("ALIAS_INVALIDE")
    try:
        holder = connections[alias]
    except ConnectionDoesNotExist:
        _fail("ALIAS_INCONNU")
    if holder.vendor != "postgresql":
        _fail("MOTEUR_REFUSE")
    if holder.in_atomic_block is True:
        _fail("TX_EXTERNE_REFUSEE")
    try:
        auto = holder.get_autocommit()
    except (DatabaseError, InterfaceError):
        _fail("TX_INDETERMINEE")
    if auto is not True:
        _fail("TX_EXTERNE_REFUSEE")
    return alias
def _advisory_key(scope, target):
    ident = canonical_head_identity(scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target)
    raw = b"pixs.agent.management:" + ident.encode("utf-8")
    digest = hashlib.sha256(raw).digest()
    return int.from_bytes(digest[0:8], "big", signed=True)
def _lock_agent(alias, scope, target):
    key = _advisory_key(scope, target)
    try:
        with connections[alias].cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(%s);", [key])
    except (DatabaseError, InterfaceError):
        _fail("VERROU_AGENT_IMPOSSIBLE")
def _now_utc(clock):
    try:
        now = clock.now()
    except (PortError, CorePortError, CoreServiceError, AuditError, DatabaseError, InterfaceError):
        _fail("HORLOGE_ILLISIBLE")
    if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
        _fail("HORLOGE_ILLISIBLE")
    return now
def _iso(now):
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")
def _require_attestation(att, scope, target, now):
    if type(att) is not GovernanceAttestation:
        _fail("GOUVERNANCE_REFUSEE")
    try:
        att.__post_init__()
    except CoreInputInvalid:
        _fail("GOUVERNANCE_REFUSEE")
    if att.context != scope:
        _fail("GOUVERNANCE_REFUSEE")
    if att.profile.owner_component != "pixs.agent":
        _fail("GOUVERNANCE_REFUSEE")
    if att.published_version != att.profile.profile_version:
        _fail("GOUVERNANCE_REFUSEE")
    if type(att.attested_at) is not datetime.datetime or att.attested_at.tzinfo is not datetime.timezone.utc:
        _fail("GOUVERNANCE_REFUSEE")
    if att.attested_at > now:
        _fail("GOUVERNANCE_REFUSEE")
    if type(att.resource_refs) is not tuple or target not in att.resource_refs:
        _fail("GOUVERNANCE_REFUSEE")
    if type(att.outbound_declarations) is not tuple or len(att.outbound_declarations) != 0:
        _fail("GOUVERNANCE_REFUSEE")
    return att
def _meta_for(att, waived):
    if waived is True:
        return (None, None, None)
    return (att.profile.data_asset_id, att.profile.confidentiality.value, att.profile.personal_data.value)
def _scope_ok_row(row, scope, target):
    if row.scope_type != scope.scope_type.value:
        _fail("SCOPE_DIVERGENT")
    if row.tenant_id != scope.tenant_id:
        _fail("SCOPE_DIVERGENT")
    if row.scope_id != scope.scope_id:
        _fail("SCOPE_DIVERGENT")
    if row.target_id != target:
        _fail("SCOPE_DIVERGENT")
def _assert_accessible(row, scope, target, meta, waived):
    _scope_ok_row(row, scope, target)
    try:
        row.clean()
    except ValidationError:
        _fail("DONNEE_CORROMPUE")
    except CoreInputInvalid:
        _fail("DONNEE_CORROMPUE")
    if waived is True:
        return None
    if row.persistence_state != DataPersistenceState.ACTIVE.value:
        _fail("ETAT_INACCESSIBLE")
    if row.retention_state != DataRetentionState.RETAINED.value:
        _fail("ETAT_INACCESSIBLE")
    gov, conf, pers = meta
    if type(gov) is not str or gov == "" or chr(0) in gov:
        _fail("METADONNEES_DIVERGENTES")
    if type(conf) is not str or type(pers) is not str:
        _fail("METADONNEES_DIVERGENTES")
    if row.governance_ref != gov or row.confidentiality != conf or row.personal != pers:
        _fail("METADONNEES_DIVERGENTES")
    return None
def _apply_meta(row, meta):
    gov, conf, pers = meta
    row.governance_ref = gov
    row.confidentiality = conf
    row.personal = pers
    if row.persistence_state != DataPersistenceState.ACTIVE.value or row.retention_state != DataRetentionState.RETAINED.value:
        _fail("ETAT_INACCESSIBLE")
    try:
        row.clean()
    except ValidationError:
        _fail("DONNEE_CORROMPUE")
    except CoreInputInvalid:
        _fail("DONNEE_CORROMPUE")
    try:
        row.save(using=row._state.db)
    except (DatabaseError, InterfaceError):
        _fail("STOCKAGE_INDISPONIBLE")
@dataclass(frozen=True, slots=True, repr=False)
class _Receipt:
    operation_id: str
    target_id: str
    generation: int
    local_ref: str
    replay: bool
    audit_disposition: str
    local_issue: str
    def __repr__(self):
        return "_Receipt(<confidentiel>)"
    def __str__(self):
        return "_Receipt(<confidentiel>)"
@dataclass(frozen=True, slots=True, repr=False)
class _Snapshot:
    target_id: str
    scope_context: ScopeContext
    head_generation: int
    desired_doc: str | None
    desired_request_op: str | None
    operations: tuple
    facts: tuple
    def __repr__(self):
        return "_Snapshot(<confidentiel>)"
    def __str__(self):
        return "_Snapshot(<confidentiel>)"
class PostgresAgentManagementService:
    def __init__(self, *, profile, decider_factory, clock, audit_adapter, governance_port, mandate_port, origin_port, confirmation_port, alias):
        if type(profile) is not AgentOperationalProfile:
            _fail("PROFIL_INVALIDE")
        try:
            profile.__post_init__()
        except AgentPortsError:
            _fail("PROFIL_INVALIDE")
        if not callable(getattr(decider_factory, "decider_for", None)):
            _fail("PORT_MANQUANT")
        if not callable(getattr(decider_factory, "authentication_for", None)):
            _fail("PORT_MANQUANT")
        if not callable(getattr(clock, "now", None)):
            _fail("PORT_MANQUANT")
        if audit_adapter is not None and type(audit_adapter) is not AgentAuditAdapter:
            _fail("PORT_MANQUANT")
        if governance_port is not None:
            for name in ("attest", "stage_read", "verify_staged"):
                if not callable(getattr(governance_port, name, None)):
                    _fail("PORT_MANQUANT")
        if mandate_port is not None and not callable(getattr(mandate_port, "verify_mandate", None)):
            _fail("PORT_MANQUANT")
        if origin_port is not None and not callable(getattr(origin_port, "verify_origin", None)):
            _fail("PORT_MANQUANT")
        if confirmation_port is not None and not callable(getattr(confirmation_port, "verify_confirmation", None)):
            _fail("PORT_MANQUANT")
        _check_alias_free(alias)
        self._profile = profile
        self._factory = decider_factory
        self._clock = clock
        self._audit = audit_adapter
        self._gov = governance_port
        self._mandate = mandate_port
        self._origin = origin_port
        self._confirm = confirmation_port
        self._alias = alias
    def _refuse_pzt(self, *, request, context, instruction):
        _fail("PZT_TRANSPORT_UNAVAILABLE")
    def persist_desired(self, *, request, context, instruction):
        return self._call_with_refusal(self._persist_desired, "desired.persist", request, context, instruction=instruction)
    def append_observation(self, *, request, context, result, observed_document, observed_at, source_ref):
        return self._call_with_refusal(self._append_observation, "observation.append", request, context, result=result, observed_document=observed_document, observed_at=observed_at, source_ref=source_ref)
    def confirm_observation(self, *, request, context, result, observed_fact_id, proof_ref, postcondition_ref):
        return self._call_with_refusal(self._confirm_observation, "confirmation.confirm", request, context, result=result, observed_fact_id=observed_fact_id, proof_ref=proof_ref, postcondition_ref=postcondition_ref)
    def query_state(self, *, request, context, limit):
        return self._call_with_refusal(self._query_state, "state.query", request, context, limit=limit)
    def dispatch(self, *, request, context, instruction):
        return self._call_with_refusal(self._refuse_pzt, "desired.persist", request, context, instruction=instruction)
    def _call_with_refusal(self, callback, purpose, request, context, **kwargs):
        try:
            return callback(request=request, context=context, **kwargs)
        except AgentServiceError as e:
            if e.code == "ISSUE_INCONNUE":
                raise
            self._record_refusal(purpose, request, context, e.code)
            raise
    def _record_refusal(self, purpose, request, context, code):
        # Nouvelle TX apres rollback ; aucun nouvel effet Agent ni rejeu.
        try:
            holder = connections[self._alias]
            external = holder.in_atomic_block or not holder.get_autocommit()
            alias = self._alias
            if external:
                if self._audit is None:
                    _fail("AUDIT_REFUS_IMPOSSIBLE")
                alias = self._audit.peer_alias
                if alias == self._alias:
                    _fail("AUDIT_REFUS_IMPOSSIBLE")
                peer = connections[alias]
                if peer.vendor != "postgresql" or peer.in_atomic_block or not peer.get_autocommit():
                    _fail("AUDIT_REFUS_IMPOSSIBLE")
                if peer.connection is holder.connection:
                    _fail("AUDIT_REFUS_IMPOSSIBLE")
            operation = new_agent_uuid7().hex
            token = new_agent_uuid7().hex
            with transaction.atomic(using=alias, durable=True):
                actor = "UNVERIFIED"
                scope = ScopeContext(ScopeType.PLATFORM)
                action, target, correlations = "agent.management.refused", "pixs.agent", (operation,)
                try:
                    # Une erreur SQL quitte le savepoint AVANT le staging C05.
                    with transaction.atomic(using=alias):
                        if type(request) is not Request or type(context) is not AgentValidationContext:
                            raise PortError()
                        request.__post_init__()
                        validate_structure(request.context)
                        for value in (request.decision_id, request.subject_id, request.resource_id, request.action_id, request.correlation_id):
                            if not _opaque(value, self._profile.max_id_len):
                                raise PortError()
                        bound_operation = context.expected_operation_id
                        if not _opaque(bound_operation, self._profile.max_id_len):
                            raise PortError()
                        decider = self._factory.decider_for(request=request, alias=alias, operation_id=bound_operation, purpose=purpose)
                        evaluation_started = _now_utc(self._clock)
                        decision = decider.revalidate_under_locks(request, alias=alias, operation_id=bound_operation)
                        if type(decision) is not Decision or decision.decision_id != request.decision_id:
                            raise PortError()
                        if decision.effect is Effect.ALLOW:
                            if decision.reason_code != "ALLOWED":
                                raise PortError()
                        elif decision.effect is Effect.DENY:
                            if decision.reason_code != "DENIED":
                                raise PortError()
                        else:
                            raise PortError()
                        now = _now_utc(self._clock)
                        for instant in (decision.evaluated_at, decision.expires_at):
                            if type(instant) is not datetime.datetime or instant.tzinfo is not datetime.timezone.utc:
                                raise PortError()
                        if decision.effect is Effect.ALLOW:
                            if not decision.evaluated_at <= now < decision.expires_at:
                                raise PortError()
                        else:
                            # C04 DENY a une fenetre nulle : aucune permission
                            # n est prolongee pour tracer ce refus courant.
                            if not evaluation_started <= decision.evaluated_at <= now or decision.expires_at != decision.evaluated_at:
                                raise PortError()
                        if type(decision.policy_version) is not tuple:
                            raise PortError()
                        encode_policy_version(decision.policy_version)
                        waived = decider.audit_waived(request, decision, alias=alias, operation_id=bound_operation)
                        if type(waived) is not bool:
                            raise PortError()
                        if waived is True and decision.effect is Effect.ALLOW:
                            return None
                        source = self._factory.authentication_for(request=request, alias=alias, operation_id=bound_operation, purpose=purpose)
                        if not callable(getattr(source, "revalidate", None)):
                            raise PortError()
                        pair = source.revalidate(request, alias=alias, operation_id=bound_operation)
                        if type(pair) is not tuple or len(pair) != 2:
                            raise PortError()
                        authentication, revocation = pair
                        if type(authentication) is not AuthenticationContext or revocation is not RevocationStatus.ACTIVE:
                            raise PortError()
                        authentication.__post_init__()
                        now = _now_utc(self._clock)
                        if authentication.digital_identity_id != request.subject_id or authentication.context != request.context:
                            raise PortError()
                        if not authentication.authentication_time <= now < authentication.expires_at:
                            raise PortError()
                        actor, scope = authentication.digital_identity_id, authentication.context
                        action, target, correlations = request.action_id, request.resource_id, (request.correlation_id,)
                except (CorePortError, PortError, CoreServiceError, AuditError, DatabaseError, InterfaceError, CoreInputInvalid, ValidationError, ScopeStructureError):
                    actor, scope = "UNVERIFIED", ScopeContext(ScopeType.PLATFORM)
                    action, target, correlations = "agent.management.refused", "pixs.agent", (operation,)
                if self._audit is None:
                    _fail("AUDIT_REFUS_IMPOSSIBLE")
                event = AuditEvent(new_agent_uuid7().hex, _iso(_now_utc(self._clock)), actor, scope.tenant_id, action, "agent", target, "DENIED", code, correlations, (), "pixs.agent", "0.1.0")
                ref = self._audit.stage_generic(event, alias=alias, operation_id=operation, transaction_token=token, context=scope)
                proof = TransactionProof(operation, alias, token, scope, (ref,), _now_utc(self._clock))
                if self._audit.verify_staged(proof) is not None:
                    _fail("AUDIT_REFUS_IMPOSSIBLE")
        except AgentServiceError:
            raise
        except (CorePortError, PortError, CoreInputInvalid, CoreServiceError, DatabaseError, InterfaceError, AuditError, AgentAuditError, ConnectionDoesNotExist, ValidationError):
            _fail("AUDIT_REFUS_IMPOSSIBLE")
    def _attest_once(self, request, op, token):
        if self._gov is None:
            _fail("GOUVERNANCE_REFUSEE")
        try:
            return self._gov.attest(request, alias=self._alias, operation_id=op, transaction_token=token)
        except (CorePortError, PortError, DatabaseError, InterfaceError, ValidationError, CoreServiceError, AuditError, CoreInputInvalid, AgentRepositoryError, AgentAuditError, AgentAuthorizationError, AgentTrustError):
            _fail("GOUVERNANCE_REFUSEE")
    def _generic_event(self, request, scope, op, outcome, causation):
        eid = new_agent_uuid7().hex
        now = _now_utc(self._clock)
        if type(causation) is not tuple:
            _fail("TRACE_INVALIDE")
        return AuditEvent(event_id=eid, occurred_at=_iso(now), actor_reference=request.subject_id, tenant_reference=scope.tenant_id, action=request.action_id, resource_type="agent", resource_id=request.resource_id, result=outcome, reason_or_error=None, correlation_ids=(request.correlation_id,), causation_ids=causation, component_id="pixs.agent", component_version="0.1.0")
    def _pdp_event(self, request, scope, decision):
        return PdpAuditEvent(decision_id=decision.decision_id, subject_id=request.subject_id, resource_id=request.resource_id, action_id=request.action_id, context=scope, correlation_id=request.correlation_id, effect=decision.effect, reason_code=decision.reason_code, policy_version=decision.policy_version, evaluated_at=decision.evaluated_at)
    def _persist_desired(self, *, request, context, instruction):
        if type(request) is not Request:
            _fail("REQUETE_INVALIDE")
        if type(context) is not AgentValidationContext:
            _fail("CONTEXTE_INVALIDE")
        if type(instruction) is not AgentManagementInstruction:
            _fail("INSTRUCTION_INVALIDE")
        if self._mandate is None:
            _fail("PORT_MANQUANT")
        alias = self._alias
        _check_alias_free(alias)
        scope = request.context
        try:
            validate_structure(scope)
        except ScopeStructureError:
            _fail("SCOPE_INVALIDE")
        target = request.resource_id
        op = context.expected_operation_id
        if not _opaque(op, self._profile.max_id_len):
            _fail("LIAISON_INVALIDE")
        token = new_agent_uuid7().hex
        commit_attempted = False
        local_ref = ""
        generation = 0
        replay_flag = False
        audit_disp = "WAIVED"
        try:
            with transaction.atomic(using=alias, durable=True):
                helper = AgentAuthorization(profile=self._profile, request=request, agent_context=context, alias=alias, operation_id=op, purpose="desired.persist", decider_factory=self._factory, clock=self._clock)
                proof = helper.authorize()
                _lock_agent(alias, scope, target)
                now2 = _now_utc(self._clock)
                fresh = AgentAuthorization.with_fresh_now(context, now2)
                helper.bind_instruction(instruction)
                helper.verify_final(proof)
                waived_audit = proof.audit_waived
                waived_gov = proof.governance_waived
                if waived_audit is not True and waived_audit is not False:
                    _fail("DEROGATION_INVALIDE")
                if waived_gov is not True and waived_gov is not False:
                    _fail("DEROGATION_INVALIDE")
                att = None
                if waived_gov is not True:
                    att = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                meta = _meta_for(att, waived_gov)
                try:
                    head_pre = repo_head(using=alias, scope=scope, target_id=target)
                except AgentRepositoryError:
                    _fail("DEPOT_IMPOSSIBLE")
                if head_pre is not None:
                    _assert_accessible(head_pre, scope, target, meta, waived_gov)
                def _mandate_cb(inst, ctx):
                    diags = self._mandate.verify_mandate(instruction=inst, context=ctx)
                    if type(diags) not in (list, tuple):
                        raise AgentTrustError("AUTORITE_BOOLEENNE_REFUSEE")
                    for item in diags:
                        if type(item) is not Diagnostic:
                            raise AgentTrustError("DIAGNOSTIC_INVALIDE")
                    return list(diags)
                try:
                    out = repo_persist(using=alias, scope=scope, target_id=target, instruction=instruction, context=fresh, allowed_catalog=self._profile.allowed_catalog, mandate_trust_port=_mandate_cb)
                except AgentRepositoryError:
                    _fail("DEPOT_IMPOSSIBLE")
                except AgentTrustError:
                    _fail("MANDAT_REFUSE")
                is_replay = out["replay"]
                if is_replay is True:
                    replay_flag = True
                elif is_replay is False:
                    replay_flag = False
                else:
                    _fail("REJEU_INVALIDE")
                operation = out["operation"]
                head = out["head"]
                if replay_flag is True:
                    _scope_ok_row(operation, scope, target)
                    _assert_accessible(operation, scope, target, meta, waived_gov)
                    local_ref = str(operation.id)
                    generation = int(operation.generation)
                else:
                    _apply_meta(operation, meta)
                    if head is None:
                        _fail("RELECTURE_DIVERGENTE")
                    if head_pre is None:
                        _apply_meta(head, meta)
                    else:
                        _assert_accessible(head, scope, target, meta, waived_gov)
                    local_ref = str(operation.id)
                    generation = int(operation.generation)
                if waived_audit is not True:
                    if self._audit is None:
                        _fail("AUDIT_IMPOSSIBLE")
                    outcome = "REPLAY" if replay_flag is True else "PERSISTED"
                    generic = self._generic_event(request, scope, op, outcome, instruction.causation_ids)
                    pdp = self._pdp_event(request, scope, proof.decision)
                    try:
                        gref = self._audit.stage_generic(generic, alias=alias, operation_id=op, transaction_token=token, context=scope)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        pref = self._audit.stage_decision(pdp, alias=alias, operation_id=op, transaction_token=token, context=scope, decision=proof.decision)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    if type(gref) is not StagedRef or type(pref) is not StagedRef:
                        _fail("AUDIT_IMPOSSIBLE")
                    if gref.operation_id != op or pref.operation_id != op:
                        _fail("AUDIT_IMPOSSIBLE")
                    if gref.alias != alias or pref.alias != alias:
                        _fail("AUDIT_IMPOSSIBLE")
                    if gref.transaction_token != token or pref.transaction_token != token:
                        _fail("AUDIT_IMPOSSIBLE")
                    if gref.context != scope or pref.context != scope:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        combined = TransactionProof(op, alias, token, scope, (gref, pref), _now_utc(self._clock))
                    except CorePortError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        outcome_v = self._audit.verify_staged(combined)
                    except (AgentAuditError, CorePortError, PortError, AuditError, DatabaseError, InterfaceError, ValidationError, CoreInputInvalid, CoreServiceError):
                        _fail("AUDIT_IMPOSSIBLE")
                    if outcome_v is not None:
                        _fail("AUDIT_IMPOSSIBLE")
                    audit_disp = "STAGED"
                else:
                    audit_disp = "WAIVED"
                if waived_gov is not True:
                    again = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                    if again.profile != att.profile or again.published_version != att.published_version or again.context != scope:
                        _fail("GOUVERNANCE_REFUSEE")
                helper.verify_final(proof)
                commit_attempted = True
        except AgentServiceError:
            raise
        except (TypeError, AttributeError):
            raise
        except (DatabaseError, InterfaceError) as err:
            if commit_attempted is True:
                _fail("ISSUE_INCONNUE")
            _fail("STOCKAGE_INDISPONIBLE")
        except (AgentAuthorizationError, AgentRepositoryError, AgentAuditError, AgentTrustError, AgentIdentifierError, CorePortError, PortError, AuditError, CoreServiceError, ValidationError, CoreInputInvalid):
            _fail("ACTE_IMPOSSIBLE")
        if commit_attempted is not True:
            _fail("STOCKAGE_INDISPONIBLE")
        issue = "REPLAY" if replay_flag is True else "PERSISTED"
        return _Receipt(operation_id=operation.request_operation_id, target_id=target, generation=generation, local_ref=local_ref, replay=replay_flag, audit_disposition=audit_disp, local_issue=issue)
    def _append_observation(self, *, request, context, result, observed_document, observed_at, source_ref):
        if type(request) is not Request:
            _fail("REQUETE_INVALIDE")
        if type(context) is not AgentValidationContext:
            _fail("CONTEXTE_INVALIDE")
        if type(result) is not AgentManagementResult:
            _fail("RESULTAT_INVALIDE")
        if self._origin is None:
            _fail("PORT_MANQUANT")
        alias = self._alias
        _check_alias_free(alias)
        scope = request.context
        try:
            validate_structure(scope)
        except ScopeStructureError:
            _fail("SCOPE_INVALIDE")
        target = request.resource_id
        op = context.expected_operation_id
        token = new_agent_uuid7().hex
        commit_attempted = False
        local_ref = ""
        generation = 0
        audit_disp = "WAIVED"
        try:
            with transaction.atomic(using=alias, durable=True):
                helper = AgentAuthorization(profile=self._profile, request=request, agent_context=context, alias=alias, operation_id=op, purpose="observation.append", decider_factory=self._factory, clock=self._clock)
                proof = helper.authorize()
                _lock_agent(alias, scope, target)
                now2 = _now_utc(self._clock)
                fresh = AgentAuthorization.with_fresh_now(context, now2)
                helper.verify_final(proof)
                waived_audit = proof.audit_waived
                waived_gov = proof.governance_waived
                if waived_audit is not True and waived_audit is not False:
                    _fail("DEROGATION_INVALIDE")
                if waived_gov is not True and waived_gov is not False:
                    _fail("DEROGATION_INVALIDE")
                att = None
                if waived_gov is not True:
                    att = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                meta = _meta_for(att, waived_gov)
                head_pre = repo_head(using=alias, scope=scope, target_id=target)
                if head_pre is None:
                    _fail("OPERATION_INTROUVABLE")
                _assert_accessible(head_pre, scope, target, meta, waived_gov)
                linked_pre = m.AgentOperation.objects.using(alias).filter(generation=result.generation, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                if linked_pre is None:
                    _fail("OPERATION_INTROUVABLE")
                _assert_accessible(linked_pre, scope, target, meta, waived_gov)
                diags0 = self._origin.verify_origin(result=result, context=fresh, observed_document=observed_document, observed_at=observed_at, source_ref=source_ref, target_id=target, scope=scope)
                if type(diags0) not in (list, tuple):
                    raise AgentTrustError("AUTORITE_BOOLEENNE_REFUSEE")
                for item in diags0:
                    if type(item) is not Diagnostic:
                        raise AgentTrustError("DIAGNOSTIC_INVALIDE")
                if list(diags0) != []:
                    _fail("ORIGINE_REFUSEE")
                def _origin_cb(res, ctx):
                    inner = self._origin.verify_origin(result=res, context=ctx, observed_document=observed_document, observed_at=observed_at, source_ref=source_ref, target_id=target, scope=scope)
                    if type(inner) not in (list, tuple):
                        raise AgentTrustError("AUTORITE_BOOLEENNE_REFUSEE")
                    for item in inner:
                        if type(item) is not Diagnostic:
                            raise AgentTrustError("DIAGNOSTIC_INVALIDE")
                    return list(inner)
                try:
                    fact = repo_append(using=alias, scope=scope, target_id=target, result=result, context=fresh, observed_document=observed_document, observed_at=observed_at, source_ref=source_ref, origin_trust_port=_origin_cb)
                except AgentRepositoryError:
                    _fail("DEPOT_IMPOSSIBLE")
                except AgentTrustError:
                    _fail("ORIGINE_REFUSEE")
                _scope_ok_row(fact, scope, target)
                try:
                    linked = m.AgentOperation.objects.using(alias).filter(pk=fact.operation_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                except (DatabaseError, InterfaceError):
                    _fail("STOCKAGE_INDISPONIBLE")
                if linked is None:
                    _fail("OPERATION_INTROUVABLE")
                _assert_accessible(linked, scope, target, meta, waived_gov)
                _apply_meta(fact, meta)
                if waived_audit is not True:
                    if self._audit is None:
                        _fail("AUDIT_IMPOSSIBLE")
                    generic = self._generic_event(request, scope, op, "OBSERVED", ())
                    pdp = self._pdp_event(request, scope, proof.decision)
                    try:
                        gref = self._audit.stage_generic(generic, alias=alias, operation_id=op, transaction_token=token, context=scope)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        pref = self._audit.stage_decision(pdp, alias=alias, operation_id=op, transaction_token=token, context=scope, decision=proof.decision)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        combined = TransactionProof(op, alias, token, scope, (gref, pref), _now_utc(self._clock))
                    except CorePortError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        outcome_v = self._audit.verify_staged(combined)
                    except (AgentAuditError, CorePortError, PortError, AuditError, DatabaseError, InterfaceError, ValidationError, CoreInputInvalid, CoreServiceError):
                        _fail("AUDIT_IMPOSSIBLE")
                    if outcome_v is not None:
                        _fail("AUDIT_IMPOSSIBLE")
                    audit_disp = "STAGED"
                else:
                    audit_disp = "WAIVED"
                if waived_gov is not True:
                    again = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                    if again.profile != att.profile or again.published_version != att.published_version or again.context != scope:
                        _fail("GOUVERNANCE_REFUSEE")
                helper.verify_final(proof)
                local_ref = str(fact.id)
                generation = int(fact.generation)
                commit_attempted = True
        except AgentServiceError:
            raise
        except (TypeError, AttributeError):
            raise
        except (DatabaseError, InterfaceError):
            if commit_attempted is True:
                _fail("ISSUE_INCONNUE")
            _fail("STOCKAGE_INDISPONIBLE")
        except (AgentAuthorizationError, AgentRepositoryError, AgentAuditError, AgentTrustError, AgentIdentifierError, CorePortError, PortError, AuditError, CoreServiceError, ValidationError, CoreInputInvalid):
            _fail("ACTE_IMPOSSIBLE")
        if commit_attempted is not True:
            _fail("STOCKAGE_INDISPONIBLE")
        return _Receipt(operation_id=op, target_id=target, generation=generation, local_ref=local_ref, replay=False, audit_disposition=audit_disp, local_issue="OBSERVED")
    def _confirm_observation(self, *, request, context, result, observed_fact_id, proof_ref, postcondition_ref):
        if type(request) is not Request:
            _fail("REQUETE_INVALIDE")
        if type(context) is not AgentValidationContext:
            _fail("CONTEXTE_INVALIDE")
        if type(result) is not AgentManagementResult:
            _fail("RESULTAT_INVALIDE")
        if self._confirm is None:
            _fail("PORT_MANQUANT")
        alias = self._alias
        _check_alias_free(alias)
        scope = request.context
        try:
            validate_structure(scope)
        except ScopeStructureError:
            _fail("SCOPE_INVALIDE")
        target = request.resource_id
        op = context.expected_operation_id
        token = new_agent_uuid7().hex
        commit_attempted = False
        local_ref = ""
        generation = 0
        audit_disp = "WAIVED"
        try:
            with transaction.atomic(using=alias, durable=True):
                helper = AgentAuthorization(profile=self._profile, request=request, agent_context=context, alias=alias, operation_id=op, purpose="confirmation.confirm", decider_factory=self._factory, clock=self._clock)
                proof = helper.authorize()
                _lock_agent(alias, scope, target)
                now2 = _now_utc(self._clock)
                fresh = AgentAuthorization.with_fresh_now(context, now2)
                helper.verify_final(proof)
                waived_audit = proof.audit_waived
                waived_gov = proof.governance_waived
                if waived_audit is not True and waived_audit is not False:
                    _fail("DEROGATION_INVALIDE")
                if waived_gov is not True and waived_gov is not False:
                    _fail("DEROGATION_INVALIDE")
                att = None
                if waived_gov is not True:
                    att = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                meta = _meta_for(att, waived_gov)
                head_pre = repo_head(using=alias, scope=scope, target_id=target)
                if head_pre is None:
                    _fail("OPERATION_INTROUVABLE")
                _assert_accessible(head_pre, scope, target, meta, waived_gov)
                require_agent_uuid7(observed_fact_id)
                observed_pre = m.AgentFact.objects.using(alias).filter(pk=observed_fact_id, kind="OBSERVED", scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                if observed_pre is None:
                    _fail("FAIT_INTROUVABLE")
                _assert_accessible(observed_pre, scope, target, meta, waived_gov)
                linked_pre = m.AgentOperation.objects.using(alias).filter(pk=observed_pre.operation_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                if linked_pre is None:
                    _fail("OPERATION_INTROUVABLE")
                _assert_accessible(linked_pre, scope, target, meta, waived_gov)
                def _confirm_cb(state, res, fact_id, src_ref, origin_proof, post_ref, ctx):
                    inner = self._confirm.verify_confirmation(state=state, result=res, observed_fact_id=fact_id, observed_source_ref=src_ref, observed_origin_proof=origin_proof, postcondition_ref=post_ref, context=ctx, target_id=target, scope=scope)
                    if type(inner) not in (list, tuple):
                        raise AgentTrustError("AUTORITE_BOOLEENNE_REFUSEE")
                    for item in inner:
                        if type(item) is not Diagnostic:
                            raise AgentTrustError("DIAGNOSTIC_INVALIDE")
                    return list(inner)
                try:
                    fact = repo_confirm(using=alias, scope=scope, target_id=target, observed_fact_id=observed_fact_id, proof_ref=proof_ref, postcondition_ref=postcondition_ref, result=result, context=fresh, confirmation_trust_port=_confirm_cb)
                except AgentRepositoryError:
                    _fail("DEPOT_IMPOSSIBLE")
                except AgentTrustError:
                    _fail("CONFIRMATION_REFUSEE")
                _scope_ok_row(fact, scope, target)
                try:
                    observed = m.AgentFact.objects.using(alias).filter(pk=fact.observed_fact_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                except (DatabaseError, InterfaceError):
                    _fail("STOCKAGE_INDISPONIBLE")
                if observed is None:
                    _fail("FAIT_INTROUVABLE")
                _assert_accessible(observed, scope, target, meta, waived_gov)
                try:
                    linked = m.AgentOperation.objects.using(alias).filter(pk=fact.operation_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                except (DatabaseError, InterfaceError):
                    _fail("STOCKAGE_INDISPONIBLE")
                if linked is None:
                    _fail("OPERATION_INTROUVABLE")
                _assert_accessible(linked, scope, target, meta, waived_gov)
                _apply_meta(fact, meta)
                if waived_audit is not True:
                    if self._audit is None:
                        _fail("AUDIT_IMPOSSIBLE")
                    generic = self._generic_event(request, scope, op, "CONFIRMED_LOCAL", ())
                    pdp = self._pdp_event(request, scope, proof.decision)
                    try:
                        gref = self._audit.stage_generic(generic, alias=alias, operation_id=op, transaction_token=token, context=scope)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        pref = self._audit.stage_decision(pdp, alias=alias, operation_id=op, transaction_token=token, context=scope, decision=proof.decision)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        combined = TransactionProof(op, alias, token, scope, (gref, pref), _now_utc(self._clock))
                    except CorePortError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        outcome_v = self._audit.verify_staged(combined)
                    except (AgentAuditError, CorePortError, PortError, AuditError, DatabaseError, InterfaceError, ValidationError, CoreInputInvalid, CoreServiceError):
                        _fail("AUDIT_IMPOSSIBLE")
                    if outcome_v is not None:
                        _fail("AUDIT_IMPOSSIBLE")
                    audit_disp = "STAGED"
                else:
                    audit_disp = "WAIVED"
                if waived_gov is not True:
                    again = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                    if again.profile != att.profile or again.published_version != att.published_version or again.context != scope:
                        _fail("GOUVERNANCE_REFUSEE")
                helper.verify_final(proof)
                local_ref = str(fact.id)
                generation = int(fact.generation)
                commit_attempted = True
        except AgentServiceError:
            raise
        except (TypeError, AttributeError):
            raise
        except (DatabaseError, InterfaceError):
            if commit_attempted is True:
                _fail("ISSUE_INCONNUE")
            _fail("STOCKAGE_INDISPONIBLE")
        except (AgentAuthorizationError, AgentRepositoryError, AgentAuditError, AgentTrustError, AgentIdentifierError, CorePortError, PortError, AuditError, CoreServiceError, ValidationError, CoreInputInvalid):
            _fail("ACTE_IMPOSSIBLE")
        if commit_attempted is not True:
            _fail("STOCKAGE_INDISPONIBLE")
        return _Receipt(operation_id=op, target_id=target, generation=generation, local_ref=local_ref, replay=False, audit_disposition=audit_disp, local_issue="CONFIRMED_LOCAL")
    def _query_state(self, *, request, context, limit):
        if type(request) is not Request:
            _fail("REQUETE_INVALIDE")
        if type(context) is not AgentValidationContext:
            _fail("CONTEXTE_INVALIDE")
        if type(limit) is not int or limit < 1 or limit > self._profile.max_ids:
            _fail("LIMITE_INVALIDE")
        alias = self._alias
        _check_alias_free(alias)
        scope = request.context
        try:
            validate_structure(scope)
        except ScopeStructureError:
            _fail("SCOPE_INVALIDE")
        target = request.resource_id
        op = context.expected_operation_id
        token = new_agent_uuid7().hex
        commit_attempted = False
        snap = None
        try:
            with transaction.atomic(using=alias, durable=True):
                helper = AgentAuthorization(profile=self._profile, request=request, agent_context=context, alias=alias, operation_id=op, purpose="state.query", decider_factory=self._factory, clock=self._clock)
                proof = helper.authorize()
                _lock_agent(alias, scope, target)
                now2 = _now_utc(self._clock)
                fresh = AgentAuthorization.with_fresh_now(context, now2)
                helper.verify_final(proof)
                waived_audit = proof.audit_waived
                waived_gov = proof.governance_waived
                if waived_audit is not True and waived_audit is not False:
                    _fail("DEROGATION_INVALIDE")
                if waived_gov is not True and waived_gov is not False:
                    _fail("DEROGATION_INVALIDE")
                att = None
                if waived_gov is not True:
                    att = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                meta = _meta_for(att, waived_gov)
                try:
                    head = repo_head(using=alias, scope=scope, target_id=target)
                except AgentRepositoryError:
                    _fail("DEPOT_IMPOSSIBLE")
                try:
                    bundle = repo_history(using=alias, scope=scope, target_id=target, limit=limit)
                except AgentRepositoryError:
                    _fail("DEPOT_IMPOSSIBLE")
                ops = list(bundle["operations"])
                facts = list(bundle["facts"])
                rows = []
                if head is not None:
                    rows.append(head)
                rows.extend(ops)
                rows.extend(facts)
                for row in rows:
                    _assert_accessible(row, scope, target, meta, waived_gov)
                by_op = {}
                for o in ops:
                    by_op[str(o.id)] = o
                for f in facts:
                    key = str(f.operation_id)
                    if key not in by_op:
                        try:
                            extra = m.AgentOperation.objects.using(alias).filter(pk=f.operation_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                        except (DatabaseError, InterfaceError):
                            _fail("STOCKAGE_INDISPONIBLE")
                        if extra is None:
                            _fail("OPERATION_INTROUVABLE")
                        _assert_accessible(extra, scope, target, meta, waived_gov)
                        by_op[key] = extra
                        ops.append(extra)
                        rows.append(extra)
                    if f.kind == "CONFIRMED":
                        try:
                            obs = m.AgentFact.objects.using(alias).filter(pk=f.observed_fact_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                        except (DatabaseError, InterfaceError):
                            _fail("STOCKAGE_INDISPONIBLE")
                        if obs is None:
                            _fail("FAIT_INTROUVABLE")
                        _assert_accessible(obs, scope, target, meta, waived_gov)
                        rows.append(obs)
                desired_doc = None
                desired_req = None
                if head is not None and head.desired_entry_id is not None:
                    try:
                        de = m.AgentOperation.objects.using(alias).filter(pk=head.desired_entry_id, scope_type=scope.scope_type.value, tenant_id=scope.tenant_id, scope_id=scope.scope_id, target_id=target).first()
                    except (DatabaseError, InterfaceError):
                        _fail("STOCKAGE_INDISPONIBLE")
                    if de is None:
                        _fail("OPERATION_INTROUVABLE")
                    _assert_accessible(de, scope, target, meta, waived_gov)
                    if str(de.id) not in by_op:
                        by_op[str(de.id)] = de
                        ops.append(de)
                        rows.append(de)
                    desired_doc = de.content_canonical
                    desired_req = str(de.request_operation_id)
                # Une lecture sans ligne reste liee a la cible autorisee.
                refs = tuple(dict.fromkeys((target, *(str(r.id) for r in rows))))
                if waived_gov is not True:
                    for r in refs:
                        if r not in att.resource_refs:
                            _fail("GOUVERNANCE_REFUSEE")
                    if self._gov is None:
                        _fail("GOUVERNANCE_REFUSEE")
                    try:
                        sref = self._gov.stage_read(request, resource_refs=refs, alias=alias, operation_id=op, transaction_token=token)
                    except (CorePortError, PortError, DatabaseError, InterfaceError, ValidationError, CoreInputInvalid, CoreServiceError, AuditError):
                        _fail("GOUVERNANCE_REFUSEE")
                    if type(sref) is not StagedRef:
                        _fail("GOUVERNANCE_REFUSEE")
                    if sref.operation_id != op or sref.alias != alias or sref.transaction_token != token or sref.context != scope:
                        _fail("GOUVERNANCE_REFUSEE")
                    try:
                        gproof = TransactionProof(op, alias, token, scope, (sref,), _now_utc(self._clock))
                    except CorePortError:
                        _fail("GOUVERNANCE_REFUSEE")
                    try:
                        gout = self._gov.verify_staged(gproof)
                    except (CorePortError, PortError, DatabaseError, InterfaceError, ValidationError, CoreInputInvalid, CoreServiceError, AuditError):
                        _fail("GOUVERNANCE_REFUSEE")
                    if gout is not None:
                        _fail("GOUVERNANCE_REFUSEE")
                ops_t = []
                for o in ops:
                    corr = tuple(json.loads(o.correlation_ids_canonical))
                    caus = tuple(json.loads(o.causation_ids_canonical))
                    ops_t.append((str(o.id), str(o.request_operation_id), str(o.subject_id), int(o.generation), str(o.content_canonical), corr, caus))
                facts_t = []
                for f in facts:
                    facts_t.append((str(f.id), str(f.operation_id), str(by_op[str(f.operation_id)].request_operation_id), str(f.observed_fact_id) if f.observed_fact_id is not None else None, int(f.generation), str(f.kind), str(f.outcome), str(f.occurred_at), f.observed_at, f.observed_document, str(f.source_ref), f.origin_proof, f.proof_ref, f.postcondition_ref))
                snap = _Snapshot(target_id=target, scope_context=scope, head_generation=int(head.current_generation) if head is not None else 0, desired_doc=desired_doc, desired_request_op=desired_req, operations=tuple(ops_t), facts=tuple(facts_t))
                if waived_audit is not True:
                    if self._audit is None:
                        _fail("AUDIT_IMPOSSIBLE")
                    generic = self._generic_event(request, scope, op, "READ", ())
                    pdp = self._pdp_event(request, scope, proof.decision)
                    try:
                        gref = self._audit.stage_generic(generic, alias=alias, operation_id=op, transaction_token=token, context=scope)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        pref = self._audit.stage_decision(pdp, alias=alias, operation_id=op, transaction_token=token, context=scope, decision=proof.decision)
                    except AgentAuditError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        combined = TransactionProof(op, alias, token, scope, (gref, pref), _now_utc(self._clock))
                    except CorePortError:
                        _fail("AUDIT_IMPOSSIBLE")
                    try:
                        outcome_v = self._audit.verify_staged(combined)
                    except (AgentAuditError, CorePortError, PortError, AuditError, DatabaseError, InterfaceError, ValidationError, CoreInputInvalid, CoreServiceError):
                        _fail("AUDIT_IMPOSSIBLE")
                    if outcome_v is not None:
                        _fail("AUDIT_IMPOSSIBLE")
                if waived_gov is not True:
                    again = _require_attestation(self._attest_once(request, op, token), scope, target, _now_utc(self._clock))
                    if again.profile != att.profile or again.published_version != att.published_version or again.context != scope or any(ref not in again.resource_refs for ref in refs):
                        _fail("GOUVERNANCE_REFUSEE")
                helper.verify_final(proof)
                commit_attempted = True
        except AgentServiceError:
            raise
        except (TypeError, AttributeError):
            raise
        except (DatabaseError, InterfaceError):
            if commit_attempted is True:
                _fail("ISSUE_INCONNUE")
            _fail("STOCKAGE_INDISPONIBLE")
        except (AgentAuthorizationError, AgentRepositoryError, AgentAuditError, AgentTrustError, AgentIdentifierError, CorePortError, PortError, AuditError, CoreServiceError, ValidationError, CoreInputInvalid):
            _fail("ACTE_IMPOSSIBLE")
        if commit_attempted is not True:
            _fail("STOCKAGE_INDISPONIBLE")
        return snap
