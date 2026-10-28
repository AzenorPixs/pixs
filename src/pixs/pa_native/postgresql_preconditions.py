"""Manifeste public de preconditions PostgreSQL 1.0.0 : forme seulement."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib as _hashlib
import json as _json

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, ContractError as _PGContractError, PayloadLimits
elif __package__ in (None, ""):
    import sys as _pg_pre_sys
    if "postgresql_contracts" not in _pg_pre_sys.builtin_module_names:
        raise ImportError("PA01_PRECONDITIONS_PG_BUILTIN_MISSING")
    import postgresql_contracts as _pg_pre_flat
    ContentBinding = _pg_pre_flat.ContentBinding
    _PGContractError = _pg_pre_flat.ContractError
    PayloadLimits = _pg_pre_flat.PayloadLimits
else:
    raise ImportError("PA01_PRECONDITIONS_CONTEXT_REFUSED")

__all__ = ["PreconditionsContractError", "PreconditionsLimits", "ResourceGuard",
           "PreconditionCondition", "PreconditionsManifest",
           "encode_preconditions", "decode_preconditions", "preconditions_binding"]

_PRE_SCHEMA = "pixs.agent.postgresql.preconditions_manifest"
_PRE_VERSION = "1.0.0"
_PRE_BINDING_VERSION = "1.0.0"
_PRE_FIELDS10 = ("schema", "schema_version", "preconditions_ref", "installation_ref",
                 "target_ref", "operation_id", "projection_binding",
                 "observation_binding", "resource_guards", "conditions")
_PRE_KINDS5 = ("SOFTWARE", "CLUSTER", "SERVICE", "ROLE", "DATABASE")
_PRE_STAGES = ("BEFORE_EFFECT", "AFTER_SERVICE_START_BEFORE_EFFECT")
_PRE_MATCH = frozenset(("MATCH", "MISMATCH", "UNDETERMINED"))
_PRE_SVC_STATES = frozenset(("ABSENT", "STOPPED", "RUNNING", "UNOBSERVABLE"))
_PRE_OTHER_STATES = frozenset(("ABSENT", "PRESENT", "UNOBSERVABLE"))
_PRE_EFFECTS = ("SERVICE_INSTALL", "SERVICE_CONFIGURE", "CLUSTER_INITIALIZE",
                "SERVICE_START", "ROLE_CREATE", "DATABASE_CREATE")
_PRE_EFFECTS_SET = frozenset(_PRE_EFFECTS)
_PRE_REF_FIELDS = ("preconditions_ref", "installation_ref", "target_ref", "operation_id")

class PreconditionsContractError(ValueError):
    """Diagnostic stable sans contenu recu."""

@dataclass(frozen=True, slots=True, repr=False)
class PreconditionsLimits:
    payload: PayloadLimits
    max_conditions: int
    def __post_init__(self):
        if type(self.payload) is not PayloadLimits:
            raise PreconditionsContractError("PA01_PRECONDITIONS_LIMITS_INVALID")
        if type(self.max_conditions) is not int or type(self.max_conditions) is bool:
            raise PreconditionsContractError("PA01_PRECONDITIONS_MAX_CONDITIONS_INVALID")
        if self.max_conditions < 1:
            raise PreconditionsContractError("PA01_PRECONDITIONS_MAX_CONDITIONS_INVALID")

@dataclass(frozen=True, slots=True, repr=False)
class ResourceGuard:
    kind: str
    resource_ref: str
    profile_binding: ContentBinding
    def __post_init__(self):
        _check_guard(self, None)

@dataclass(frozen=True, slots=True, repr=False)
class PreconditionCondition:
    condition_ref: str
    resource_kind: str
    resource_ref: str
    profile_binding: ContentBinding
    effect: str
    check_stage: str
    expected_state: str
    expected_match: str
    evidence_binding: ContentBinding | None
    def __post_init__(self):
        _check_condition(self, None)

@dataclass(frozen=True, slots=True, repr=False)
class PreconditionsManifest:
    schema: str
    schema_version: str
    preconditions_ref: str
    installation_ref: str
    target_ref: str
    operation_id: str
    projection_binding: ContentBinding
    observation_binding: ContentBinding
    resource_guards: tuple[ResourceGuard, ...]
    conditions: tuple[PreconditionCondition, ...]
    def __post_init__(self):
        _check_preconditions(self, None)

def _pre_ref(v: object, mx: int | None) -> None:
    if type(v) is not str or not v:
        raise PreconditionsContractError("PA01_PRECONDITIONS_REFERENCE_INVALID")
    for ch in v:
        c = ord(ch)
        if c < 32 or c == 127 or 0xD800 <= c <= 0xDFFF:
            raise PreconditionsContractError("PA01_PRECONDITIONS_REFERENCE_INVALID")
    try:
        n = len(v.encode("utf-8"))
    except UnicodeEncodeError as e:
        raise PreconditionsContractError("PA01_PRECONDITIONS_REFERENCE_UTF8_INVALID") from e
    if mx is not None and n > mx:
        raise PreconditionsContractError("PA01_PRECONDITIONS_REFERENCE_LIMIT_EXCEEDED")

def _pre_digest(v: object) -> None:
    import re as _re
    if type(v) is not str or _re.fullmatch(r"[0-9a-f]{64}", v) is None:
        raise PreconditionsContractError("PA01_PRECONDITIONS_DIGEST_INVALID")

def _pre_fields(v: dict, names: tuple, code: str) -> None:
    if type(v) is not dict or set(v) != set(names):
        raise PreconditionsContractError(code)

def _pre_pairs(pairs):
    d = {}
    for k, _ in pairs:
        if k in d:
            raise PreconditionsContractError("PA01_PRECONDITIONS_JSON_DUPLICATED")
        d[k] = None
    return {k: v for k, v in pairs}

def _pre_const(_t):
    raise PreconditionsContractError("PA01_PRECONDITIONS_CONSTANT_INVALID")

def _pre_num(_t):
    raise PreconditionsContractError("PA01_PRECONDITIONS_NUMBER_NOT_ALLOWED")

def _pre_binding_instance(v: object, mx: int | None) -> None:
    if type(v) is not ContentBinding:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_INVALID")
    _pre_ref(v.ref, mx)
    _pre_ref(v.version, mx)
    _pre_digest(v.sha256)

def _pre_binding_from_dict(v: object, mx: int | None) -> ContentBinding:
    if type(v) is not dict:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_INVALID")
    _pre_fields(v, ("ref", "version", "sha256"), "PA01_PRECONDITIONS_BINDING_FIELDS_INVALID")
    if type(v["ref"]) is not str or type(v["version"]) is not str:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_INVALID")
    _pre_ref(v["ref"], mx)
    _pre_ref(v["version"], mx)
    _pre_digest(v["sha256"])
    try:
        return ContentBinding(ref=v["ref"], version=v["version"], sha256=v["sha256"])
    except _PGContractError as e:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_INVALID") from e

def _pre_state_ok(kind: str, state: object) -> None:
    if type(state) is not str:
        raise PreconditionsContractError("PA01_PRECONDITIONS_STATE_INVALID")
    ok = _PRE_SVC_STATES if kind == "SERVICE" else _PRE_OTHER_STATES
    if state not in ok or type(kind) is not str or kind not in _PRE_KINDS5:
        raise PreconditionsContractError("PA01_PRECONDITIONS_STATE_INVALID")

def _check_guard(v: object, lim: PreconditionsLimits | None) -> None:
    if type(v) is not ResourceGuard:
        raise PreconditionsContractError("PA01_PRECONDITIONS_GUARD_INVALID")
    if lim is not None and type(lim) is not PreconditionsLimits:
        raise PreconditionsContractError("PA01_PRECONDITIONS_LIMITS_INVALID")
    mx = None if lim is None else lim.payload.max_ref_bytes
    if type(v.kind) is not str or v.kind not in _PRE_KINDS5:
        raise PreconditionsContractError("PA01_PRECONDITIONS_KIND_INVALID")
    _pre_ref(v.resource_ref, mx)
    _pre_binding_instance(v.profile_binding, mx)

def _check_condition(v: object, lim: PreconditionsLimits | None) -> None:
    if type(v) is not PreconditionCondition:
        raise PreconditionsContractError("PA01_PRECONDITIONS_CONDITION_INVALID")
    if lim is not None and type(lim) is not PreconditionsLimits:
        raise PreconditionsContractError("PA01_PRECONDITIONS_LIMITS_INVALID")
    mx = None if lim is None else lim.payload.max_ref_bytes
    _pre_ref(v.condition_ref, mx)
    if type(v.resource_kind) is not str or v.resource_kind not in _PRE_KINDS5:
        raise PreconditionsContractError("PA01_PRECONDITIONS_KIND_INVALID")
    _pre_ref(v.resource_ref, mx)
    _pre_binding_instance(v.profile_binding, mx)
    if type(v.effect) is not str or v.effect not in _PRE_EFFECTS_SET:
        raise PreconditionsContractError("PA01_PRECONDITIONS_EFFECT_INVALID")
    if type(v.check_stage) is not str or v.check_stage not in _PRE_STAGES:
        raise PreconditionsContractError("PA01_PRECONDITIONS_STAGE_INVALID")
    _pre_state_ok(v.resource_kind, v.expected_state)
    if type(v.expected_match) is not str or v.expected_match not in _PRE_MATCH:
        raise PreconditionsContractError("PA01_PRECONDITIONS_MATCH_INVALID")
    ev = v.evidence_binding
    if ev is None:
        ok_null = ((v.resource_kind == "ROLE" and v.effect == "ROLE_CREATE") or
                   (v.resource_kind == "DATABASE" and v.effect == "DATABASE_CREATE"))
        if not (ok_null and v.check_stage == "AFTER_SERVICE_START_BEFORE_EFFECT"):
            raise PreconditionsContractError("PA01_PRECONDITIONS_EVIDENCE_NULL_FORBIDDEN")
    else:
        _pre_binding_instance(ev, mx)

def _check_preconditions(v: object, lim: PreconditionsLimits | None) -> None:
    if type(v) is not PreconditionsManifest:
        raise PreconditionsContractError("PA01_PRECONDITIONS_DOCUMENT_INVALID")
    if lim is not None and type(lim) is not PreconditionsLimits:
        raise PreconditionsContractError("PA01_PRECONDITIONS_LIMITS_INVALID")
    mx = None if lim is None else lim.payload.max_ref_bytes
    if type(v.schema) is not str or v.schema != _PRE_SCHEMA:
        raise PreconditionsContractError("PA01_PRECONDITIONS_SCHEMA_INVALID")
    if type(v.schema_version) is not str or v.schema_version != _PRE_VERSION:
        raise PreconditionsContractError("PA01_PRECONDITIONS_SCHEMA_INVALID")
    for n in _PRE_REF_FIELDS:
        _pre_ref(getattr(v, n), mx)
    _pre_binding_instance(v.projection_binding, mx)
    _pre_binding_instance(v.observation_binding, mx)
    if v.projection_binding.version != _PRE_BINDING_VERSION:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_VERSION_MISMATCH")
    if v.observation_binding.version != _PRE_BINDING_VERSION:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_VERSION_MISMATCH")
    if type(v.resource_guards) is not tuple or len(v.resource_guards) != 5:
        raise PreconditionsContractError("PA01_PRECONDITIONS_GUARDS_INVALID")
    for g in v.resource_guards:
        _check_guard(g, lim)
    if tuple(g.kind for g in v.resource_guards) != _PRE_KINDS5:
        raise PreconditionsContractError("PA01_PRECONDITIONS_ORDER_INVALID")
    if type(v.conditions) is not tuple:
        raise PreconditionsContractError("PA01_PRECONDITIONS_CONDITIONS_INVALID")
    if lim is not None and len(v.conditions) > lim.max_conditions:
        raise PreconditionsContractError("PA01_PRECONDITIONS_CONDITIONS_LIMIT_EXCEEDED")
    seen: set[str] = set()
    for c in v.conditions:
        _check_condition(c, lim)
        if c.condition_ref in seen:
            raise PreconditionsContractError("PA01_PRECONDITIONS_CONDITION_DUPLICATE")
        seen.add(c.condition_ref)

def _pre_to_dict(v: PreconditionsManifest) -> dict:
    from dataclasses import asdict as _as
    return {
        "schema": v.schema, "schema_version": v.schema_version,
        "preconditions_ref": v.preconditions_ref, "installation_ref": v.installation_ref,
        "target_ref": v.target_ref, "operation_id": v.operation_id,
        "projection_binding": _as(v.projection_binding),
        "observation_binding": _as(v.observation_binding),
        "resource_guards": [{"kind": g.kind, "resource_ref": g.resource_ref,
                             "profile_binding": _as(g.profile_binding)} for g in v.resource_guards],
        "conditions": [{"condition_ref": c.condition_ref, "resource_kind": c.resource_kind,
                        "resource_ref": c.resource_ref, "profile_binding": _as(c.profile_binding),
                        "effect": c.effect, "check_stage": c.check_stage,
                        "expected_state": c.expected_state, "expected_match": c.expected_match,
                        "evidence_binding": None if c.evidence_binding is None else _as(c.evidence_binding)}
                       for c in v.conditions],
    }

def _pre_encode_dict(d: dict, lim: PreconditionsLimits) -> str:
    t = _json.dumps(d, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    try:
        n = len(t.encode("utf-8"))
    except UnicodeEncodeError as e:
        raise PreconditionsContractError("PA01_PRECONDITIONS_UTF8_INVALID") from e
    if n > lim.payload.max_json_bytes:
        raise PreconditionsContractError("PA01_PRECONDITIONS_LIMIT_EXCEEDED")
    return t

def encode_preconditions(v: PreconditionsManifest, lim: PreconditionsLimits) -> str:
    if type(lim) is not PreconditionsLimits:
        raise PreconditionsContractError("PA01_PRECONDITIONS_LIMITS_INVALID")
    _check_preconditions(v, lim)
    return _pre_encode_dict(_pre_to_dict(v), lim)

def decode_preconditions(t: str, lim: PreconditionsLimits) -> PreconditionsManifest:
    if type(lim) is not PreconditionsLimits or type(t) is not str:
        raise PreconditionsContractError("PA01_PRECONDITIONS_PAYLOAD_INVALID")
    try:
        if len(t.encode("utf-8")) > lim.payload.max_json_bytes:
            raise PreconditionsContractError("PA01_PRECONDITIONS_LIMIT_EXCEEDED")
        d = _json.loads(t, object_pairs_hook=_pre_pairs, parse_int=_pre_num,
                        parse_float=_pre_num, parse_constant=_pre_const)
    except (UnicodeEncodeError, _json.JSONDecodeError, RecursionError) as e:
        raise PreconditionsContractError("PA01_PRECONDITIONS_JSON_INVALID") from e
    if type(d) is not dict:
        raise PreconditionsContractError("PA01_PRECONDITIONS_OBJECT_REQUIRED")
    _pre_fields(d, _PRE_FIELDS10, "PA01_PRECONDITIONS_FIELDS_INVALID")
    mx = lim.payload.max_ref_bytes
    for n in _PRE_REF_FIELDS:
        _pre_ref(d[n], mx)
    pb = _pre_binding_from_dict(d["projection_binding"], mx)
    ob = _pre_binding_from_dict(d["observation_binding"], mx)
    if pb.version != _PRE_BINDING_VERSION or ob.version != _PRE_BINDING_VERSION:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_VERSION_MISMATCH")
    rg_raw = d["resource_guards"]
    if type(rg_raw) is not list or len(rg_raw) != 5:
        raise PreconditionsContractError("PA01_PRECONDITIONS_GUARDS_INVALID")
    guards = []
    for e in rg_raw:
        if type(e) is not dict:
            raise PreconditionsContractError("PA01_PRECONDITIONS_GUARD_INVALID")
        _pre_fields(e, ("kind", "resource_ref", "profile_binding"), "PA01_PRECONDITIONS_GUARD_FIELDS_INVALID")
        guards.append(ResourceGuard(kind=e["kind"], resource_ref=e["resource_ref"],
                                    profile_binding=_pre_binding_from_dict(e["profile_binding"], mx)))
    cond_raw = d["conditions"]
    if type(cond_raw) is not list or len(cond_raw) > lim.max_conditions:
        raise PreconditionsContractError("PA01_PRECONDITIONS_CONDITIONS_INVALID")
    conds = []
    for e in cond_raw:
        if type(e) is not dict:
            raise PreconditionsContractError("PA01_PRECONDITIONS_CONDITION_INVALID")
        _pre_fields(e, ("condition_ref", "resource_kind", "resource_ref", "profile_binding",
                        "effect", "check_stage", "expected_state", "expected_match",
                        "evidence_binding"), "PA01_PRECONDITIONS_CONDITION_FIELDS_INVALID")
        ev = None if e["evidence_binding"] is None else _pre_binding_from_dict(e["evidence_binding"], mx)
        conds.append(PreconditionCondition(condition_ref=e["condition_ref"], resource_kind=e["resource_kind"],
                                          resource_ref=e["resource_ref"],
                                          profile_binding=_pre_binding_from_dict(e["profile_binding"], mx),
                                          effect=e["effect"], check_stage=e["check_stage"],
                                          expected_state=e["expected_state"], expected_match=e["expected_match"],
                                          evidence_binding=ev))
    res = PreconditionsManifest(schema=d["schema"], schema_version=d["schema_version"],
                                preconditions_ref=d["preconditions_ref"],
                                installation_ref=d["installation_ref"], target_ref=d["target_ref"],
                                operation_id=d["operation_id"], projection_binding=pb,
                                observation_binding=ob, resource_guards=tuple(guards),
                                conditions=tuple(conds))
    _check_preconditions(res, lim)
    return res

def preconditions_binding(v: PreconditionsManifest, lim: PreconditionsLimits) -> ContentBinding:
    if type(lim) is not PreconditionsLimits:
        raise PreconditionsContractError("PA01_PRECONDITIONS_LIMITS_INVALID")
    _check_preconditions(v, lim)
    digest = _hashlib.sha256(encode_preconditions(v, lim).encode("utf-8")).hexdigest()
    try:
        b = ContentBinding(ref=v.preconditions_ref, version="1.0.0", sha256=digest)
    except _PGContractError as e:
        raise PreconditionsContractError("PA01_PRECONDITIONS_BINDING_INVALID") from e
    _pre_binding_instance(b, lim.payload.max_ref_bytes)
    return b
