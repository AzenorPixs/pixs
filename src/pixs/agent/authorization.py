"""Autorisation privée Agent sur C04 public, liée à une invocation et à sa TX."""
from __future__ import annotations
import datetime
from dataclasses import dataclass
from dataclasses import replace
from django.db import connections
from django.db import DatabaseError
from django.db import InterfaceError
from django.utils.connection import ConnectionDoesNotExist
from pixs.agent.contracts import AgentManagementInstruction
from pixs.agent.contracts import AgentParamSpec
from pixs.agent.contracts import AgentValidationContext
from pixs.agent.contracts import AllowedCatalogEntry
from pixs.agent.contracts import validate_agent_instruction
from pixs.agent.ports import AgentClock
from pixs.agent.ports import AgentCoreDeciderFactory
from pixs.agent.ports import AgentOperationalProfile
from pixs.agent.ports import PURPOSES, AgentPortsError
from pixs.core.audit_contracts import AuditError
from pixs.core.audit_contracts import encode_policy_version
from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.policy import Obligation
from pixs.core.authz.policy import PolicyError
from pixs.core.authz.ports import PortError
from pixs.core.authz.ports import Request
from pixs.core.ports import AuthorizationDecider
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext
from pixs.core.scope.context import ScopeStructureError
from pixs.core.scope.context import validate_structure
from pixs.core.services_authorization_guard import transaction_identity
from pixs.core.services_common import CoreServiceError
from pixs.kernel.manifest.semver import parse_version
__all__ = ['AgentAuthorizationError', 'AgentAuthorization']
# Helper prive Agent : consomme le C04 public sans recompiler ses regles.
# Le service appelant a deja ouvert la vraie TX PostgreSQL ; ce helper ne
# commit pas, n audite pas et n effectue aucune mutation metier. La fabrique
# C04 est appelee DANS la TX et epingle Core avant tout verrou Agent.
_CATALOG_KINDS = ('str', 'int', 'bool')
class AgentAuthorizationError(ValueError):
    def __init__(self, code='AGENT_AUTORISATION_IMPOSSIBLE'):
        super().__init__('Autorisation Agent impossible.')
        self.code = code
        self.element = 'agent_authorization'
        self.step = 'authorize_agent_c04'
    def __repr__(self):
        return 'AgentAuthorizationError(<confidentiel>)'
    def __str__(self):
        return 'AgentAuthorizationError(<confidentiel>)'
def _fail(code):
    raise AgentAuthorizationError(code) from None
def _opaque(value, limit):
    if type(value) is not str or value == '' or chr(0) in value or len(value) > limit:
        return False
    try:
        value.encode('utf-8')
    except UnicodeEncodeError:
        return False
    return True
def _is_canonical_20(value):
    if type(value) is not str or len(value) != 20:
        return False
    if value[4] != '-' or value[7] != '-' or value[10] != 'T' or value[13] != ':' or value[16] != ':' or value[19] != 'Z':
        return False
    for i in (0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18):
        if not '0' <= value[i] <= '9':
            return False
    try:
        datetime.datetime(int(value[0:4]), int(value[5:7]), int(value[8:10]), int(value[11:13]), int(value[14:16]), int(value[17:19]))
    except ValueError:
        return False
    return True
def _check_version(value):
    if type(value) is not str or value == '':
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True
def _check_profile(profile):
    if type(profile) is not AgentOperationalProfile:
        _fail("PROFIL_INVALIDE")
    try:
        profile.__post_init__()
    except AgentPortsError:
        _fail("PROFIL_INVALIDE")
def _check_agent_context(agent_context):
    if type(agent_context) is not AgentValidationContext:
        _fail('CONTEXTE_INVALIDE')
    if type(agent_context.expected_scope) is not ScopeContext:
        _fail('CONTEXTE_INVALIDE')
    try:
        validate_structure(agent_context.expected_scope)
    except ScopeStructureError:
        _fail('CONTEXTE_INVALIDE')
    for bound in (agent_context.max_id_len, agent_context.max_doc_len, agent_context.max_ids, agent_context.max_params, agent_context.max_observation_age_seconds):
        if type(bound) is not int or bound < 1:
            _fail('CONTEXTE_INVALIDE')
    max_id = agent_context.max_id_len
    for field in ('expected_actor', 'expected_target', 'expected_operation', 'expected_operation_id', 'expected_idempotency_key', 'mandate_proof'):
        if not _opaque(getattr(agent_context, field), max_id):
            _fail('CONTEXTE_INVALIDE')
    for field in ('expected_origin_proof', 'expected_confirmation_proof'):
        value = getattr(agent_context, field)
        if value is not None and not _opaque(value, max_id):
            _fail('CONTEXTE_INVALIDE')
    if not _check_version(agent_context.expected_version):
        _fail('CONTEXTE_INVALIDE')
    if type(agent_context.expected_generation) is not int or agent_context.expected_generation < 0:
        _fail('CONTEXTE_INVALIDE')
    correlations = agent_context.expected_correlation_ids
    if type(correlations) is not tuple or not correlations or len(correlations) > agent_context.max_ids:
        _fail('CONTEXTE_INVALIDE')
    for item in correlations:
        if not _opaque(item, max_id):
            _fail('CONTEXTE_INVALIDE')
    if not _is_canonical_20(agent_context.now_iso):
        _fail('CONTEXTE_INVALIDE')
def _check_request_binding(profile, request, agent_context, alias, operation_id, purpose):
    if type(request) is not Request:
        _fail('REQUETE_INVALIDE')
    try:
        request.__post_init__()
    except PortError:
        _fail('REQUETE_INVALIDE')
    try:
        validate_structure(request.context)
    except ScopeStructureError:
        _fail('REQUETE_INVALIDE')
    max_id = agent_context.max_id_len
    for value in (request.decision_id, request.subject_id, request.resource_id, request.action_id, request.correlation_id):
        if not _opaque(value, max_id):
            _fail('REQUETE_INVALIDE')
    if operation_id != agent_context.expected_operation_id:
        _fail('LIAISON_OPERATION_INVALIDE')
    if not _opaque(alias, max_id) or not _opaque(operation_id, max_id):
        _fail('LIAISON_INVALIDE')
    if type(purpose) is not str or purpose not in PURPOSES:
        _fail('INTENTION_INVALIDE')
    if request.subject_id != agent_context.expected_actor:
        _fail('LIAISON_ACTEUR_INVALIDE')
    if request.context != agent_context.expected_scope:
        _fail('LIAISON_CONTEXTE_INVALIDE')
    if request.resource_id != agent_context.expected_target:
        _fail('LIAISON_CIBLE_INVALIDE')
    if request.correlation_id not in agent_context.expected_correlation_ids:
        _fail('LIAISON_CORRELATION_INVALIDE')
    allowed = False
    for pair in profile.allowed_core_actions:
        if pair[0] == purpose and request.action_id in pair[1]:
            allowed = True
    if not allowed:
        _fail('ACTION_NON_AUTORISEE')
def _require_open_tx(alias):
    try:
        holder = connections[alias]
    except (ConnectionDoesNotExist, DatabaseError, InterfaceError):
        _fail('TX_ABSENTE')
    if holder.vendor != 'postgresql':
        _fail('MOTEUR_REFUSE')
    if holder.in_atomic_block is not True:
        _fail('TX_ABSENTE')
def _capture_pin(alias):
    try:
        pin = transaction_identity(alias)
    except (CoreServiceError, DatabaseError, InterfaceError):
        _fail('TX_INDETERMINEE')
    try:
        physical = connections[alias].connection
    except (ConnectionDoesNotExist, DatabaseError, InterfaceError):
        _fail('TX_ABSENTE')
    if type(pin) is not tuple or len(pin) != 4:
        _fail('TX_INDETERMINEE')
    for part in pin:
        if type(part) is not int:
            _fail('TX_INDETERMINEE')
    return (pin, physical)
def _read_clock(clock):
    try:
        now = clock.now()
    except (PortError, CorePortError, CoreServiceError, AuditError, DatabaseError, InterfaceError):
        _fail('HORLOGE_ILLISIBLE')
    if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
        _fail('HORLOGE_ILLISIBLE')
    return now
def _check_decision(decision, request, now):
    if type(decision) is not Decision:
        _fail('DECISION_INVALIDE')
    if type(decision.decision_id) is not str or decision.decision_id != request.decision_id:
        _fail('DECISION_INVALIDE')
    if decision.effect is not Effect.ALLOW:
        _fail('AUTORISATION_REFUSEE')
    if type(decision.reason_code) is not str or decision.reason_code != 'ALLOWED':
        _fail('DECISION_INVALIDE')
    if type(decision.policy_version) is not tuple:
        _fail('VERSION_INVALIDE')
    try:
        encode_policy_version(decision.policy_version)
    except AuditError:
        _fail('VERSION_INVALIDE')
    for bound in (decision.evaluated_at, decision.expires_at):
        if type(bound) is not datetime.datetime or bound.tzinfo is not datetime.timezone.utc:
            _fail('ECHEANCE_INVALIDE')
    if not decision.evaluated_at <= now < decision.expires_at:
        _fail('ECHEANCE_INVALIDE')
    if type(decision.obligations) is not tuple:
        _fail('OBLIGATIONS_INVALIDES')
    for item in decision.obligations:
        if type(item) is not Obligation or item.kind != 'AUDIT':
            _fail('OBLIGATIONS_INVALIDES')
@dataclass(frozen=True, slots=True, repr=False)
class _SealedAuthorization:
    decision: Decision
    alias: str
    operation_id: str
    tx_pin: tuple
    audit_waived: bool
    governance_waived: bool
    decider: AuthorizationDecider
    def __repr__(self):
        return '_SealedAuthorization(<confidentiel>)'
    def __str__(self):
        return '_SealedAuthorization(<confidentiel>)'
    def __post_init__(self):
        if type(self.decision) is not Decision:
            _fail('PREUVE_INVALIDE')
        if type(self.alias) is not str or self.alias == '':
            _fail('PREUVE_INVALIDE')
        if type(self.operation_id) is not str or self.operation_id == '':
            _fail('PREUVE_INVALIDE')
        if type(self.tx_pin) is not tuple or len(self.tx_pin) != 4:
            _fail('PREUVE_INVALIDE')
        for part in self.tx_pin:
            if type(part) is not int:
                _fail('PREUVE_INVALIDE')
        if type(self.audit_waived) is not bool or type(self.governance_waived) is not bool:
            _fail('PREUVE_INVALIDE')
        for method in ('revalidate_under_locks', 'audit_waived', 'governance_waived'):
            if not callable(getattr(self.decider, method, None)):
                _fail('PREUVE_INVALIDE')
class AgentAuthorization:
    def __init__(self, *, profile: AgentOperationalProfile, request: Request, agent_context: AgentValidationContext, alias: str, operation_id: str, purpose: str, decider_factory: AgentCoreDeciderFactory, clock: AgentClock):
        _check_profile(profile)
        _check_agent_context(agent_context)
        for field in ("max_id_len", "max_doc_len", "max_ids", "max_params", "max_observation_age_seconds"):
            if getattr(agent_context, field) != getattr(profile, field):
                _fail("BORNES_DIVERGENTES")
        for identifier in (agent_context.expected_scope.tenant_id, agent_context.expected_scope.scope_id):
            if identifier is not None and not _opaque(identifier, profile.max_id_len):
                _fail("CONTEXTE_INVALIDE")
        _check_request_binding(profile, request, agent_context, alias, operation_id, purpose)
        if not callable(getattr(decider_factory, 'decider_for', None)):
            _fail('FABRIQUE_INVALIDE')
        if not callable(getattr(clock, 'now', None)):
            _fail('HORLOGE_ILLISIBLE')
        _require_open_tx(alias)
        self._profile = profile
        self._request = request
        self._agent_context = agent_context
        self._alias = alias
        self._operation_id = operation_id
        self._purpose = purpose
        self._decider_factory = decider_factory
        self._clock = clock
        self._tx_pin = _capture_pin(alias)
        self._last_proof = None
        self._active_decider = None
    @property
    def profile(self):
        return self._profile
    @property
    def request(self):
        return self._request
    @property
    def agent_context(self):
        return self._agent_context
    @property
    def alias(self):
        return self._alias
    @property
    def operation_id(self):
        return self._operation_id
    @property
    def purpose(self):
        return self._purpose
    @staticmethod
    def with_fresh_now(agent_context: AgentValidationContext, now: datetime.datetime):
        if type(agent_context) is not AgentValidationContext:
            _fail('CONTEXTE_INVALIDE')
        if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
            _fail('HORLOGE_ILLISIBLE')
        iso = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        if len(iso) != 20 or not _is_canonical_20(iso):
            _fail('CONTEXTE_INVALIDE')
        return replace(agent_context, now_iso=iso)
    def bind_instruction(self, instruction: AgentManagementInstruction):
        if type(instruction) is not AgentManagementInstruction:
            _fail('INSTRUCTION_INVALIDE')
        self._assert_usable()
        current_context = self.with_fresh_now(self._agent_context, _read_clock(self._clock))
        diagnostics = validate_agent_instruction(instruction, self._profile.allowed_catalog, current_context)
        if type(diagnostics) is not list or diagnostics != []:
            _fail('INSTRUCTION_INVALIDE')
        if instruction.catalog_operation != self._request.action_id:
            _fail('LIAISON_OPERATION_INVALIDE')
        if instruction.initial_actor != self._agent_context.expected_actor:
            _fail('ACTEUR_INVALIDE')
        if instruction.operation_id != self._operation_id:
            _fail('LIAISON_OPERATION_INVALIDE')
        return None
    def _assert_usable(self):
        _require_open_tx(self._alias)
        pin, physical = _capture_pin(self._alias)
        if pin != self._tx_pin[0] or physical is not self._tx_pin[1]:
            _fail('TX_MODIFIEE')
    def _waivers(self, decider, decision):
        try:
            audit_ok = decider.audit_waived(self._request, decision, alias=self._alias, operation_id=self._operation_id)
            governance_ok = decider.governance_waived(self._request, decision, alias=self._alias, operation_id=self._operation_id)
        except (PortError, CorePortError, CoreServiceError, AuditError, DatabaseError, InterfaceError):
            _fail('DEROGATION_INVALIDE')
        if type(audit_ok) is not bool or type(governance_ok) is not bool:
            _fail('DEROGATION_INVALIDE')
        return (audit_ok, governance_ok)
    def authorize(self):
        self._assert_usable()
        try:
            decider = self._decider_factory.decider_for(request=self._request, alias=self._alias, operation_id=self._operation_id, purpose=self._purpose)
        except (PortError, CorePortError, CoreServiceError, AuditError, DatabaseError, InterfaceError):
            _fail('FABRIQUE_INVALIDE')
        for method in ("revalidate_under_locks", "audit_waived", "governance_waived"):
            if not callable(getattr(decider, method, None)):
                _fail("FABRIQUE_INVALIDE")
        try:
            decision = decider.revalidate_under_locks(self._request, alias=self._alias, operation_id=self._operation_id)
        except (PortError, CorePortError, CoreServiceError, AuditError, DatabaseError, InterfaceError):
            _fail('DECISION_INVALIDE')
        now = _read_clock(self._clock)
        _check_decision(decision, self._request, now)
        audit_ok, governance_ok = self._waivers(decider, decision)
        self._assert_usable()
        proof = _SealedAuthorization(decision=decision, alias=self._alias, operation_id=self._operation_id, tx_pin=self._tx_pin[0], audit_waived=audit_ok, governance_waived=governance_ok, decider=decider)
        self._active_decider = decider
        self._last_proof = proof
        return proof
    def verify_final(self, proof):
        if type(proof) is not _SealedAuthorization or proof is not self._last_proof or proof.decider is not self._active_decider:
            _fail('PREUVE_INVALIDE')
        if proof.alias != self._alias or proof.operation_id != self._operation_id:
            _fail('LIAISON_MODIFIEE')
        self._assert_usable()
        if proof.tx_pin != self._tx_pin[0]:
            _fail('TX_MODIFIEE')
        decider = proof.decider
        try:
            fresh = decider.revalidate_under_locks(self._request, alias=self._alias, operation_id=self._operation_id)
        except (PortError, CorePortError, CoreServiceError, AuditError, DatabaseError, InterfaceError):
            _fail('DECISION_INVALIDE')
        now = _read_clock(self._clock)
        _check_decision(fresh, self._request, now)
        if fresh.policy_version != proof.decision.policy_version:
            _fail('VERSION_MODIFIEE')
        if fresh.decision_id != self._request.decision_id:
            _fail('LIAISON_MODIFIEE')
        audit_ok, governance_ok = self._waivers(decider, fresh)
        if audit_ok != proof.audit_waived or governance_ok != proof.governance_waived:
            _fail('DEROGATIONS_MODIFIEES')
        self._assert_usable()
        return None
