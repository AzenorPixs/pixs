# path: src/pixs/agent/fact_inventory.py
"""Codec prive d'inventaire AgentFact D-S1 3.6 : tableau 17 valeurs, verification pure.

Frontiere seule, sans effet. Ne prouve ni provenance, ni classification,
ni version payload, ni signature, ni autorite, ni transport, ni confiance.
Stdlib et pixs.agent.identifiers pour UUIDv7 seulement. Aucun import Django,
DB, provider, reseau, horloge, generation UUID ou I/O.
"""
from __future__ import annotations
import hashlib
import json
import uuid as _uuid
from pixs.agent.identifiers import require_agent_uuid7, AgentIdentifierError

INT64_MAX = 9223372036854775807
INVENTORY_CODEC = "agent-fact-inventory.v1"
FIXED_MESSAGE = "Inventaire AgentFact invalide."
ORDERED_KEYS = ("id", "operation_id", "observed_fact_id", "scope_type", "tenant_id", "scope_id", "target_id", "generation", "kind", "outcome", "occurred_at", "observed_at", "origin_proof", "observed_document", "source_ref", "proof_ref", "postcondition_ref")
FACT_KIND = ("OBSERVED", "CONFIRMED")
FACT_OUTCOME = ("ack", "confirmed", "failed", "unknown")

class AgentFactInventoryError(ValueError):
    def __init__(self) -> None:
        super().__init__(FIXED_MESSAGE)
        self.code = "AGENT_FACT_INVENTORY_INVALID"
        self.element = "agent_fact_inventory"
        self.step = "validate_inventory"
    def __repr__(self) -> str:
        return "AgentFactInventoryError(<redacted>)"
    def __str__(self) -> str:
        return "AgentFactInventoryError(<redacted>)"

def _fail() -> None:
    raise AgentFactInventoryError() from None

def _require_opaque(value: object) -> str:
    if type(value) is not str or value == "" or "\x00" in value:
        _fail()
    assert isinstance(value, str)
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    return value

def _require_nullable_opaque(value: object) -> str | None:
    if value is None:
        return None
    return _require_opaque(value)

def _require_uuid_text(value: object) -> str:
    if type(value) is not _uuid.UUID:
        _fail()
    assert isinstance(value, _uuid.UUID)
    try:
        require_agent_uuid7(value)
    except AgentIdentifierError:
        _fail()
    return str(value)

def _require_nullable_uuid_text(value: object) -> str | None:
    if value is None:
        return None
    return _require_uuid_text(value)

def _require_generation(value: object) -> int:
    if type(value) is bool or type(value) is not int:
        _fail()
    assert isinstance(value, int)
    if not 0 <= value <= INT64_MAX:
        _fail()
    return value

def _reject_constant(value: str) -> None:
    _fail()

def _reject_float(value: str) -> None:
    _fail()

def _check_int(value: str) -> int:
    try:
        number = int(value, 10)
    except ValueError:
        _fail()
    assert isinstance(number, int)
    return number

def canonical_fact_inventory(*, id: object, operation_id: object, observed_fact_id: object, scope_type: object, tenant_id: object, scope_id: object, target_id: object, generation: object, kind: object, outcome: object, occurred_at: object, observed_at: object, origin_proof: object, observed_document: object, source_ref: object, proof_ref: object, postcondition_ref: object) -> str:
    v_id = _require_uuid_text(id)
    v_op = _require_uuid_text(operation_id)
    v_obs_fact = _require_nullable_uuid_text(observed_fact_id)
    if type(scope_type) is not str or scope_type not in ("PLATFORM", "TENANT"):
        _fail()
    assert isinstance(scope_type, str)
    v_tenant = _require_nullable_opaque(tenant_id)
    v_scope = _require_nullable_opaque(scope_id)
    if scope_type == "PLATFORM":
        if v_tenant is not None or v_scope is not None:
            _fail()
    else:
        if v_tenant is None:
            _fail()
    v_target = _require_opaque(target_id)
    v_gen = _require_generation(generation)
    if type(kind) is not str or kind not in FACT_KIND:
        _fail()
    if type(outcome) is not str or outcome not in FACT_OUTCOME:
        _fail()
    assert isinstance(kind, str) and isinstance(outcome, str)
    v_occurred = _require_opaque(occurred_at)
    v_observed_at = _require_nullable_opaque(observed_at)
    v_origin = _require_nullable_opaque(origin_proof)
    v_doc = _require_nullable_opaque(observed_document)
    v_source = _require_opaque(source_ref)
    v_proof = _require_nullable_opaque(proof_ref)
    v_post = _require_nullable_opaque(postcondition_ref)
    ordered = [v_id, v_op, v_obs_fact, scope_type, v_tenant, v_scope, v_target, v_gen, kind, outcome, v_occurred, v_observed_at, v_origin, v_doc, v_source, v_proof, v_post]
    try:
        text = json.dumps(ordered, sort_keys=False, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    assert isinstance(text, str)
    if "\x00" in text or text.endswith("\n"):
        _fail()
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    return text

def require_fact_inventory_canonical(text: object) -> str:
    if type(text) is not str or text == "":
        _fail()
    assert isinstance(text, str)
    if "\x00" in text or text.endswith("\n"):
        _fail()
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    try:
        parsed = json.loads(text, parse_constant=_reject_constant, parse_float=_reject_float, parse_int=_check_int)
    except (ValueError, RecursionError):
        _fail()
    if type(parsed) is not list or len(parsed) != 17:
        _fail()
    assert isinstance(parsed, list)
    (p_id, p_op, p_obs_fact, p_scope, p_tenant, p_scope_id, p_target, p_gen, p_kind, p_outcome, p_occurred, p_observed_at, p_origin, p_doc, p_source, p_proof, p_post) = parsed
    try:
        id_u = _uuid.UUID(p_id) if type(p_id) is str else _fail()
        op_u = _uuid.UUID(p_op) if type(p_op) is str else _fail()
        obs_u = None
        if p_obs_fact is not None:
            if type(p_obs_fact) is not str:
                _fail()
            obs_u = _uuid.UUID(p_obs_fact)
        rebuilt = canonical_fact_inventory(id=id_u, operation_id=op_u, observed_fact_id=obs_u, scope_type=p_scope, tenant_id=p_tenant, scope_id=p_scope_id, target_id=p_target, generation=p_gen, kind=p_kind, outcome=p_outcome, occurred_at=p_occurred, observed_at=p_observed_at, origin_proof=p_origin, observed_document=p_doc, source_ref=p_source, proof_ref=p_proof, postcondition_ref=p_post)
    except AgentFactInventoryError:
        _fail()
    except (ValueError, AttributeError, TypeError):
        _fail()
    assert isinstance(rebuilt, str)
    if rebuilt != text:
        _fail()
    return text

def fact_inventory_sha256(canonical_text: object) -> str:
    if type(canonical_text) is not str:
        _fail()
    assert isinstance(canonical_text, str)
    require_fact_inventory_canonical(canonical_text)
    return hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()
