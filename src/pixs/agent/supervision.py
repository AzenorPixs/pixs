'''Supervision Agent honnete, lecture seule et reconciliation sans executant.'''
from __future__ import annotations
import datetime
import uuid
from dataclasses import dataclass, replace
from pixs.agent.adapter import AgentFacadeHandle
from pixs.agent.contracts import AgentManagementResult, AgentManagementState, validate_agent_state
from pixs.agent.ports import AgentOperationalProfile, AgentPortsError
from pixs.agent.service import PostgresAgentManagementService, AgentServiceError, _Snapshot, _now_utc
from pixs.agent.identifiers import AgentIdentifierError, require_agent_uuid7
from pixs.core.scope.context import ScopeContext
__all__ = ['AgentSupervisionError', 'AgentSupervisionView', 'AgentSupervisor']
FIXED = 'Supervision Agent impossible.'
TRANSPORT_STATUS = 'PZT_NOT_BOUND'
EXECUTOR_STATUS = 'UNKNOWN'
OUTCOMES = ('ack', 'confirmed', 'failed', 'unknown')
class AgentSupervisionError(ValueError):
    def __init__(self, code='AGENT_SUPERVISION_IMPOSSIBLE'):
        super().__init__(FIXED)
        self.code = code
        self.element = 'agent_supervision'
        self.step = 'reconcile'
    def __repr__(self):
        return 'AgentSupervisionError(<confidentiel>)'
    def __str__(self):
        return 'AgentSupervisionError(<confidentiel>)'
def _fail(code):
    raise AgentSupervisionError(code) from None
def _opaque(value, limit):
    if type(value) is not str or value == '' or chr(0) in value or len(value) > limit:
        return False
    try:
        value.encode('utf-8')
    except UnicodeEncodeError:
        return False
    return True
def _storage_ref(value):
    if type(value) is not str:
        return False
    try:
        parsed = uuid.UUID(value)
        require_agent_uuid7(parsed)
    except (ValueError, AgentIdentifierError):
        return False
    return str(parsed) == value
def _parse_instant(value):
    if type(value) is not str or len(value) != 20:
        return None
    if value[4] != '-' or value[7] != '-' or value[10] != 'T' or value[13] != ':' or value[16] != ':' or value[19] != 'Z':
        return None
    for i in (0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18):
        if value[i] < '0' or value[i] > '9':
            return None
    try:
        return datetime.datetime(int(value[0:4]), int(value[5:7]), int(value[8:10]), int(value[11:13]), int(value[14:16]), int(value[17:19]), tzinfo=datetime.timezone.utc)
    except ValueError:
        return None
@dataclass(frozen=True, slots=True, repr=False)
class AgentSupervisionView:
    """Fenetre bornee ; last_result concerne la generation souhaitee courante.

    Aucun historique complet ni disponibilite PA/PZT ne sont deduits.
    """
    target: str
    scope: ScopeContext
    desired_doc: str | None
    desired_operation_id: str | None
    desired_generation: int | None
    state: AgentManagementState | None
    observation_status: str
    last_known_generation: int | None
    last_known_stale: bool | None
    last_result: AgentManagementResult | None
    confirmation_status: str
    last_confirmation_generation: int | None
    last_confirmation_at: str | None
    last_confirmation_ref: str | None
    checked_at: str
    history_limit: int
    transport_status: str
    executor_status: str
    def __repr__(self):
        return 'AgentSupervisionView(<confidentiel>)'
    def __str__(self):
        return 'AgentSupervisionView(<confidentiel>)'
class AgentSupervisor:
    def __init__(self, *, management):
        if type(management) is PostgresAgentManagementService:
            service = management
        elif type(management) is AgentFacadeHandle:
            service = management._service
            if type(service) is not PostgresAgentManagementService:
                _fail('GESTION_INVALIDE')
        else:
            _fail('GESTION_INVALIDE')
        profile = service._profile
        clock = service._clock
        if type(profile) is not AgentOperationalProfile:
            _fail('PROFIL_INVALIDE')
        try:
            profile.__post_init__()
        except AgentPortsError:
            _fail('PROFIL_INVALIDE')
        if not callable(getattr(clock, 'now', None)):
            _fail('HORLOGE_INVALIDE')
        self._management = management
        self._service = service
    def __repr__(self):
        return 'AgentSupervisor(<confidentiel>)'
    def _check_fact_shape(self, f, profile, now):
        max_id = profile.max_id_len
        if type(f) is not tuple or len(f) != 14:
            _fail('PROJECTION_INCOHERENTE')
        if not _storage_ref(f[0]) or not _storage_ref(f[1]):
            _fail('PROJECTION_INCOHERENTE')
        if not _opaque(f[2], max_id):
            _fail('PROJECTION_INCOHERENTE')
        if f[3] is not None and not _storage_ref(f[3]):
            _fail('PROJECTION_INCOHERENTE')
        if type(f[4]) is not int or f[4] < 1:
            _fail('PROJECTION_INCOHERENTE')
        if type(f[5]) is not str or f[5] not in ('OBSERVED', 'CONFIRMED'):
            _fail('PROJECTION_INCOHERENTE')
        if type(f[6]) is not str or f[6] not in OUTCOMES:
            _fail('PROJECTION_INCOHERENTE')
        if f[5] == 'CONFIRMED':
            if f[6] != 'confirmed' or f[3] is None or f[9] is None:
                _fail('PROJECTION_INCOHERENTE')
            if not _opaque(f[12], max_id) or not _opaque(f[13], max_id):
                _fail('PROJECTION_INCOHERENTE')
        elif f[3] is not None or f[12] is not None or f[13] is not None:
            _fail('PROJECTION_INCOHERENTE')
        occurred = _parse_instant(f[7])
        if occurred is None or occurred > now:
            _fail('PROJECTION_INCOHERENTE')
        if f[9] is None:
            if f[8] is not None:
                _fail('PROJECTION_INCOHERENTE')
        else:
            if not _opaque(f[9], profile.max_doc_len):
                _fail('PROJECTION_INCOHERENTE')
            seen = _parse_instant(f[8])
            if seen is None or seen > now:
                _fail('PROJECTION_INCOHERENTE')
        if not _opaque(f[10], max_id):
            _fail('PROJECTION_INCOHERENTE')
        if f[6] == 'unknown':
            if f[11] is not None:
                _fail('PROJECTION_INCOHERENTE')
        elif not _opaque(f[11], max_id):
            _fail('PROJECTION_INCOHERENTE')
    def reconcile(self, *, request, context, limit):
        snap = self._management.query_state(request=request, context=context, limit=limit)
        if type(snap) is not _Snapshot:
            _fail('PROJECTION_IMPOSSIBLE')
        target = snap.target_id
        scope = snap.scope_context
        if target != request.resource_id:
            _fail('PROJECTION_INCOHERENTE')
        if scope != request.context:
            _fail('PROJECTION_INCOHERENTE')
        if type(snap.head_generation) is not int or snap.head_generation < 0:
            _fail('PROJECTION_INCOHERENTE')
        if type(snap.operations) is not tuple or type(snap.facts) is not tuple:
            _fail('PROJECTION_INCOHERENTE')
        profile = self._service._profile
        if type(profile) is not AgentOperationalProfile:
            _fail('PROFIL_INVALIDE')
        try:
            profile.__post_init__()
        except AgentPortsError:
            _fail('PROFIL_INVALIDE')
        max_id = profile.max_id_len
        max_age = profile.max_observation_age_seconds
        try:
            now = _now_utc(self._service._clock)
        except AgentServiceError:
            _fail('HORLOGE_ILLISIBLE')
        if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
            _fail('HORLOGE_ILLISIBLE')
        checked = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        if _parse_instant(checked) is None:
            _fail('HORLOGE_ILLISIBLE')
        if snap.desired_doc is None:
            if snap.desired_request_op is not None or snap.head_generation != 0 or snap.operations or snap.facts:
                _fail('PROJECTION_INCOHERENTE')
            return AgentSupervisionView(target, scope, None, None, None, None, 'ABSENT', None, None, None, 'NONE', None, None, None, checked, limit, TRANSPORT_STATUS, EXECUTOR_STATUS)
        if not _opaque(snap.desired_doc, profile.max_doc_len):
            _fail('PROJECTION_INCOHERENTE')
        if not _opaque(snap.desired_request_op, max_id):
            _fail('PROJECTION_INCOHERENTE')
        linked = None
        by_op = {}
        generations = set()
        for op in snap.operations:
            if type(op) is not tuple or len(op) != 7:
                _fail('PROJECTION_INCOHERENTE')
            if not _storage_ref(op[0]) or not _opaque(op[1], max_id) or not _opaque(op[2], max_id):
                _fail('PROJECTION_INCOHERENTE')
            if type(op[3]) is not int or not 1 <= op[3] <= snap.head_generation:
                _fail('PROJECTION_INCOHERENTE')
            if not _opaque(op[4], profile.max_doc_len):
                _fail('PROJECTION_INCOHERENTE')
            for trace in (op[5], op[6]):
                if type(trace) is not tuple or len(trace) > profile.max_ids:
                    _fail('PROJECTION_INCOHERENTE')
                if any(not _opaque(item, max_id) for item in trace):
                    _fail('PROJECTION_INCOHERENTE')
            if not op[5] or op[0] in by_op or op[3] in generations:
                _fail('PROJECTION_INCOHERENTE')
            by_op[op[0]] = op
            generations.add(op[3])
            if op[3] == snap.head_generation:
                if op[1] != snap.desired_request_op or op[4] != snap.desired_doc or linked is not None:
                    _fail('PROJECTION_INCOHERENTE')
                linked = op
        if linked is None:
            _fail('PROJECTION_INCOHERENTE')
        desired_id = linked[0]
        desired_gen = linked[3]
        desired_corr = linked[5]
        current = []
        best_known = None
        best_confirmed = None
        fact_ids = set()
        for f in snap.facts:
            self._check_fact_shape(f, profile, now)
            owner_op = by_op.get(f[1])
            if owner_op is None or f[2] != owner_op[1] or f[4] != owner_op[3] or f[0] in fact_ids:
                _fail('PROJECTION_INCOHERENTE')
            fact_ids.add(f[0])
            if f[1] == desired_id and f[4] == desired_gen:
                current.append(f)
            if f[9] is not None:
                key = (f[8], f[7], f[0])
                if best_known is None or key > (best_known[8], best_known[7], best_known[0]):
                    best_known = f
            if f[5] == 'CONFIRMED':
                key = (f[7], f[0])
                if best_confirmed is None or key > (best_confirmed[7], best_confirmed[0]):
                    best_confirmed = f
        latest = None
        for f in current:
            if latest is None or (f[7], f[0]) > (latest[7], latest[0]):
                latest = f
        last_result = None
        if latest is not None:
            last_result = AgentManagementResult(operation_id=latest[2], pa_target=target, generation=latest[4], scope_context=scope, outcome=latest[6], correlation_ids=desired_corr, occurred_at=latest[7], origin_proof=latest[11])
        observed_doc = None
        observed_at = None
        if latest is not None and latest[9] is not None:
            seen = _parse_instant(latest[8])
            if seen is not None and (now - seen).total_seconds() <= max_age:
                observed_doc = latest[9]
                observed_at = latest[8]
        known_doc = None
        known_at = None
        known_gen = None
        if best_known is not None:
            known_doc = best_known[9]
            known_at = best_known[8]
            known_gen = best_known[4]
        stale = None if best_known is None else (now - _parse_instant(known_at)).total_seconds() > max_age
        confirmation_status = 'NONE'
        conf_gen = None
        conf_at = None
        conf_ref = None
        conf_proof = None
        if latest is not None and latest[5] == 'CONFIRMED':
            if observed_doc is not None and type(latest[12]) is str and latest[12] != '' and type(latest[13]) is str and latest[13] != '':
                confirmation_status = 'CURRENT'
                conf_gen = latest[4]
                conf_at = latest[7]
                conf_ref = latest[12]
                conf_proof = latest[12]
            else:
                confirmation_status = 'STALE'
                conf_gen = latest[4]
                conf_at = latest[7]
                conf_ref = latest[12]
        elif best_confirmed is not None:
            confirmation_status = 'HISTORICAL'
            conf_gen = best_confirmed[4]
            conf_at = best_confirmed[7]
            conf_ref = best_confirmed[12]
        state = AgentManagementState(operation_id=snap.desired_request_op, pa_target=target, generation=desired_gen, scope_context=scope, desired_doc=snap.desired_doc, observed_doc=observed_doc, observed_at=observed_at, last_known_doc=known_doc, last_known_at=known_at, confirmation_proof=conf_proof)
        derived = replace(context, expected_operation_id=snap.desired_request_op, expected_generation=desired_gen, expected_confirmation_proof=conf_proof, now_iso=checked)
        if validate_agent_state(state, derived) != []:
            _fail('PROJECTION_INCOHERENTE')
        status = 'ABSENT'
        if observed_doc is not None:
            status = 'CURRENT'
        elif latest is not None and latest[9] is not None:
            status = 'STALE'
        elif known_doc is not None:
            status = 'HISTORICAL'
        return AgentSupervisionView(target, scope, snap.desired_doc, snap.desired_request_op, desired_gen, state, status, known_gen, stale, last_result, confirmation_status, conf_gen, conf_at, conf_ref, checked, limit, TRANSPORT_STATUS, EXECUTOR_STATUS)
