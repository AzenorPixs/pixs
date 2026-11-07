"""Magasin relais prive, lecture seule inactive : snapshot reconciliation coherent."""
from __future__ import annotations
import json
import uuid as _uuidmod
from dataclasses import dataclass
from django.db import DatabaseError, InterfaceError, connections
from django.utils.connection import ConnectionDoesNotExist
from pixs.agent.identifiers import AgentIdentifierError, require_agent_uuid7, require_canonical_instant_v2
from pixs.agent.models import BINDING_STATE, EVENT_KIND, OUTBOX_STATE
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure

__all__ = ["AgentRelayStoreError", "AttemptView", "EventView", "ReconciliationSnapshot", "read_reconciliation"]

_FIXED = "Magasin relais impossible."

_ATT_KEYS = frozenset({"id", "attempt_no", "claim_epoch", "binding_revision", "composition_ref"})
_EV_KEYS = frozenset({"attempt_id", "event_no", "event_kind", "occurred_at", "detail_ref", "transport_receipt_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref", "postcondition_refs"})


class AgentRelayStoreError(ValueError):
    def __init__(self, code="AGENT_RELAY_STORE_IMPOSSIBLE"):
        super().__init__(_FIXED)
        self.code = code
        self.element = "agent_relay_store"
        self.step = "agent_reconcile_read"


def _fail(code):
    raise AgentRelayStoreError(code) from None


def _alias(using):
    if type(using) is not str or using == "":
        _fail("ALIAS_INVALIDE")
    try:
        connection = connections[using]
    except ConnectionDoesNotExist:
        _fail("ALIAS_INCONNU")
    if connection.vendor != "postgresql":
        _fail("MOTEUR_REFUSE")
    return connection


def _check_scope(scope, target_id):
    if type(scope) is not ScopeContext:
        _fail("SCOPE_INVALIDE")
    try:
        validate_structure(scope)
    except ScopeStructureError:
        _fail("SCOPE_INVALIDE")
    if type(target_id) is not str or target_id == "" or "\x00" in target_id:
        _fail("CIBLE_INVALIDE")
    try:
        target_id.encode("utf-8")
    except UnicodeEncodeError:
        _fail("CIBLE_INVALIDE")


def _check_uuid(value):
    try:
        require_agent_uuid7(value)
    except AgentIdentifierError:
        _fail("IDENTIFIANT_INVALIDE")


def _check_text(value, nullable):
    if value is None:
        if nullable:
            return
        _fail("DONNEE_CORROMPUE")
    if type(value) is not str or value == "" or "\x00" in value:
        _fail("DONNEE_CORROMPUE")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail("DONNEE_CORROMPUE")


def _check_int(value, lo, hi):
    if type(value) is not int:
        _fail("DONNEE_CORROMPUE")
    if not lo <= value <= hi:
        _fail("DONNEE_CORROMPUE")


@dataclass(frozen=True, slots=True)
class AttemptView:
    attempt_id: str
    attempt_no: int
    claim_epoch: int
    binding_revision: int
    composition_ref: str


@dataclass(frozen=True, slots=True)
class EventView:
    attempt_id: str
    event_no: int
    event_kind: str
    occurred_at: str
    detail_ref: str | None
    transport_receipt_ref: str | None
    native_operation_ref: str | None
    native_result_ref: str | None
    native_snapshot_ref: str | None
    native_revision_ref: str | None
    response_digest: str | None
    origin_proof_ref: str | None
    time_evidence_ref: str | None
    postcondition_refs: tuple | None


@dataclass(frozen=True, slots=True)
class ReconciliationSnapshot:
    outbox_id: str
    binding_id: str
    outbox_state: str
    outbox_revision: int
    expected_binding_revision: int
    binding_state_revision: int
    binding_state: str
    binding_state_reason: str | None
    native_request_ref: str
    staged_owner_operation_id: str | None
    attempts: tuple
    events: tuple
    pg_backend_pid: int
    schema: str
    # Donnees observees immuables a un instant statement, sans preuve de
    # commit attendu, rollback, absence d emission, causalite ou autorisation.
    # Tri de presentation par attempt_no/event_no seulement ; references et
    # postcondition_refs jamais normalisees, ordre et doublons preserves.


_SQL = (
    "SELECT ob.id, ob.state, ob.revision, ob.expected_binding_revision, ob.native_request_ref, ob.staged_owner_operation_id, "
    "b.id, bs.revision, bs.state, bs.state_reason_ref, br.state, br.state_reason_ref, b.native_request_ref, "
    "pg_backend_pid(), current_schema(), "
    "(SELECT COALESCE(json_agg(row_to_json(a) ORDER BY a.attempt_no), '[]'::json) FROM "
    "(SELECT id, attempt_no, claim_epoch, binding_revision, composition_ref FROM pixs_agent_pa_attempt WHERE outbox_id = ob.id) a), "
    "(SELECT COALESCE(json_agg(row_to_json(e) ORDER BY e.event_no), '[]'::json) FROM "
    "(SELECT d.attempt_id, d.event_no, d.event_kind, d.occurred_at, d.detail_ref, d.transport_receipt_ref, d.native_operation_ref, "
    "d.native_result_ref, d.native_snapshot_ref, d.native_revision_ref, d.response_digest, d.origin_proof_ref, d.time_evidence_ref, d.postcondition_refs "
    "FROM pixs_agent_pa_delivery_event d JOIN pixs_agent_pa_attempt x ON x.id = d.attempt_id WHERE x.outbox_id = ob.id) e) "
    "FROM pixs_agent_pa_outbox ob "
    "JOIN pixs_agent_pa_binding b ON b.id = ob.binding_id "
    "JOIN pixs_agent_pa_binding_state bs ON bs.binding_id = b.id "
    "JOIN pixs_agent_pa_binding_revision br ON br.binding_id = b.id AND br.revision = bs.revision "
    "WHERE ob.id = %s AND b.scope_type = %s AND b.agent_target_id = %s "
    "AND b.tenant_id IS NOT DISTINCT FROM %s AND b.scope_id IS NOT DISTINCT FROM %s"
)


def _uuid_text(value):
    if isinstance(value, _uuidmod.UUID):
        try:
            require_agent_uuid7(value)
        except AgentIdentifierError:
            _fail("DONNEE_CORROMPUE")
        return str(value)
    if type(value) is str:
        try:
            parsed = _uuidmod.UUID(value)
        except ValueError:
            _fail("DONNEE_CORROMPUE")
        try:
            require_agent_uuid7(parsed)
        except AgentIdentifierError:
            _fail("DONNEE_CORROMPUE")
        if value != str(parsed):
            _fail("DONNEE_CORROMPUE")
        return value
    _fail("DONNEE_CORROMPUE")


def _parse_json_list(value):
    if type(value) is str:
        try:
            parsed = json.loads(value)
        except ValueError:
            _fail("DONNEE_CORROMPUE")
    elif type(value) is list:
        parsed = value
    else:
        _fail("DONNEE_CORROMPUE")
    if type(parsed) is not list:
        _fail("DONNEE_CORROMPUE")
    return parsed


def _postconditions_immutable(value):
    if value is None:
        return None
    if type(value) is not list:
        _fail("DONNEE_CORROMPUE")
    for item in value:
        _check_text(item, False)
    return tuple(value)


def read_reconciliation(*, using, scope, target_id, outbox_id):
    _check_scope(scope, target_id)
    _check_uuid(outbox_id)
    connection = _alias(using)
    scope_value = scope.scope_type.value
    if type(scope_value) is not str:
        _fail("SCOPE_INVALIDE")
    params = [_uuid_text(outbox_id), scope_value, target_id, scope.tenant_id, scope.scope_id]
    try:
        with connection.cursor() as cursor:
            cursor.execute(_SQL, params)
            row = cursor.fetchone()
    except (DatabaseError, InterfaceError):
        raise AgentRelayStoreError("LECTURE_IMPOSSIBLE") from None
    if row is None:
        _fail("ABSENT")
    (ob_id, ob_state, ob_rev, ob_exp, ob_nat, ob_staged, b_id, bs_rev, bs_state, bs_reason, br_state, br_reason, b_nat, pid, schema, att_json, ev_json) = row
    if type(ob_state) is not str or type(ob_nat) is not str or type(bs_state) is not str or type(br_state) is not str or type(b_nat) is not str:
        _fail("DONNEE_CORROMPUE")
    if ob_state not in OUTBOX_STATE or bs_state not in BINDING_STATE or br_state not in BINDING_STATE:
        _fail("DONNEE_CORROMPUE")
    if bs_reason is not None:
        _check_text(bs_reason, False)
    if br_reason is not None:
        _check_text(br_reason, False)
    _check_text(ob_nat, False)
    _check_text(b_nat, False)
    _check_int(ob_rev, 1, 9223372036854775807)
    _check_int(ob_exp, 1, 9223372036854775807)
    _check_int(bs_rev, 1, 9223372036854775807)
    if bs_state != br_state or bs_reason != br_reason:
        _fail("DIVERGENCE_ETAT_REVISION")
    if ob_nat != b_nat:
        _fail("DIVERGENCE_REF_NATIVE")
    if ob_exp != bs_rev:
        _fail("DIVERGENCE_REVISION_ATTENDUE")
    attempts = []
    for item in _parse_json_list(att_json):
        if type(item) is not dict or set(item.keys()) != _ATT_KEYS:
            _fail("DONNEE_CORROMPUE")
        _check_text(item["composition_ref"], False)
        _check_int(item["attempt_no"], 1, 9223372036854775807)
        _check_int(item["claim_epoch"], 0, 9223372036854775807)
        _check_int(item["binding_revision"], 1, 9223372036854775807)
        attempts.append(AttemptView(attempt_id=_uuid_text(item["id"]), attempt_no=item["attempt_no"], claim_epoch=item["claim_epoch"], binding_revision=item["binding_revision"], composition_ref=item["composition_ref"]))
    attempts.sort(key=lambda v: v.attempt_no)
    events = []
    for item in _parse_json_list(ev_json):
        if type(item) is not dict or set(item.keys()) != _EV_KEYS:
            _fail("DONNEE_CORROMPUE")
        if type(item["event_kind"]) is not str or item["event_kind"] not in EVENT_KIND:
            _fail("DONNEE_CORROMPUE")
        _check_text(item["occurred_at"], False)
        try:
            require_canonical_instant_v2(item["occurred_at"])
        except AgentIdentifierError:
            _fail("DONNEE_CORROMPUE")
        _check_int(item["event_no"], 1, 9223372036854775807)
        for key in ("detail_ref", "transport_receipt_ref", "native_operation_ref", "native_result_ref", "native_snapshot_ref", "native_revision_ref", "response_digest", "origin_proof_ref", "time_evidence_ref"):
            _check_text(item.get(key), True)
        events.append(EventView(attempt_id=_uuid_text(item["attempt_id"]), event_no=item["event_no"], event_kind=item["event_kind"], occurred_at=item["occurred_at"], detail_ref=item.get("detail_ref"), transport_receipt_ref=item.get("transport_receipt_ref"), native_operation_ref=item.get("native_operation_ref"), native_result_ref=item.get("native_result_ref"), native_snapshot_ref=item.get("native_snapshot_ref"), native_revision_ref=item.get("native_revision_ref"), response_digest=item.get("response_digest"), origin_proof_ref=item.get("origin_proof_ref"), time_evidence_ref=item.get("time_evidence_ref"), postcondition_refs=_postconditions_immutable(item.get("postcondition_refs"))))
    events.sort(key=lambda v: (v.attempt_id, v.event_no))
    if type(pid) is not int or type(schema) is not str:
        _fail("DONNEE_CORROMPUE")
    return ReconciliationSnapshot(outbox_id=_uuid_text(ob_id), binding_id=_uuid_text(b_id), outbox_state=ob_state, outbox_revision=ob_rev, expected_binding_revision=ob_exp, binding_state_revision=bs_rev, binding_state=bs_state, binding_state_reason=bs_reason, native_request_ref=ob_nat, staged_owner_operation_id=None if ob_staged is None else _uuid_text(ob_staged), attempts=tuple(attempts), events=tuple(events), pg_backend_pid=pid, schema=schema)
