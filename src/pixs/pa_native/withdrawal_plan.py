"""Plan administratif de retrait PA, forme seule 16 champs.

Forme pure proposee, sans admission, acte, preuve materielle, fraicheur,
politique courante, autorite, mandat, droit ou effet. Document ferme 16
champs, CANON deterministe hors document. PayloadLimits PG externe explicite
reutilise tel quel, sans nouveau profil. Liaisons ContentBinding fournies
seulement structurees, jamais preuve d'autorite ou de provenance authentique.
Sans clock, deadline, port, NV, SQL, signature.
"""
from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding
    from .postgresql_contracts import PayloadLimits
elif __package__ in (None, ""):
    import sys as _plan_sys
    if "postgresql_contracts" not in _plan_sys.builtin_module_names:
        raise ImportError("WITHDRAWAL_PLAN_PG_BUILTIN_MISSING")
    import postgresql_contracts as _plan_pg
    ContentBinding = _plan_pg.ContentBinding
    PayloadLimits = _plan_pg.PayloadLimits
else:
    raise ImportError("WITHDRAWAL_PLAN_CONTEXT_REFUSED")

__all__ = [
    "WithdrawalPlanError",
    "WithdrawalPlan",
    "encode_withdrawal_plan",
    "decode_withdrawal_plan",
    "withdrawal_plan_binding",
]

_FIXED_MESSAGE = "Plan de retrait invalide."
_OBJECT_TYPE = "pixs.agent.withdrawal_plan/v1"
_SCHEMA_VERSION = "1.0.0"
_CATALOG_OPERATION = "withdraw_initial_authority"
_CATALOG_VERSION = "1.0.0"
_QUIESCENCE = "stop_new_initial_preparations_and_quiesce_concerned_preparations"
_DIGEST = re.compile(r"[0-9a-f]{64}")
_FIELDS = frozenset({
    "object_type", "schema_version", "plan_ref", "plan_version",
    "installation_ref", "target_ref", "catalog_operation", "catalog_version",
    "operation_id", "idempotency_key", "policy_ref", "policy_version",
    "initial_publication_binding", "anchor_binding",
    "installation_result_ref", "quiescence_scope",
})
_REF_FIELDS = (
    "plan_ref", "plan_version", "installation_ref", "target_ref",
    "operation_id", "idempotency_key", "policy_ref", "policy_version",
    "installation_result_ref",
)
_WILDCARDS = ("*", "?", "[", "]")


class WithdrawalPlanError(ValueError):
    def __init__(self, code="WITHDRAWAL_PLAN_INVALID"):
        super().__init__(_FIXED_MESSAGE)
        self.code = code
        self.element = "withdrawal_plan"
        self.step = "validate_withdrawal_plan"


def _fail(code="WITHDRAWAL_PLAN_INVALID"):
    raise WithdrawalPlanError(code) from None


def _plan_ref(value, maximum):
    if type(value) is not str or value == "":
        _fail()
    for ch in value:
        o = ord(ch)
        if o < 32 or o == 127 or 0xD800 <= o <= 0xDFFF:
            _fail()
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        _fail()
    if maximum is not None:
        if type(maximum) is not int or maximum <= 0:
            _fail()
        if size > maximum:
            raise WithdrawalPlanError("WITHDRAWAL_PLAN_REFERENCE_LIMIT_EXCEEDED") from None


def _plan_ref_no_wildcard(value, maximum):
    _plan_ref(value, maximum)
    for w in _WILDCARDS:
        if w in value:
            raise WithdrawalPlanError("WITHDRAWAL_PLAN_WILDCARD_REFUSED") from None


def _plan_digest(value):
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        _fail()


def _plan_number(_value):
    raise WithdrawalPlanError("WITHDRAWAL_PLAN_NUMBER_NOT_ALLOWED") from None


def _plan_constant(_value):
    raise WithdrawalPlanError("WITHDRAWAL_PLAN_CONSTANT_INVALID") from None


def _plan_pairs(pairs):
    data = {}
    for name, item in pairs:
        if name in data:
            raise WithdrawalPlanError("WITHDRAWAL_PLAN_FIELD_DUPLICATED") from None
        data[name] = item
    return data


def _limits_max(limits):
    if type(limits) is not PayloadLimits:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    try:
        jb = object.__getattribute__(limits, "max_json_bytes")
        rb = object.__getattribute__(limits, "max_ref_bytes")
        ob = object.__getattribute__(limits, "max_observation_refs")
    except AttributeError:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    if type(jb) is not int or type(rb) is not int or type(ob) is not int:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    if jb <= 0 or rb <= 0 or ob <= 0:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    return jb, rb


def _check_binding_value(value, maximum):
    if type(value) is not ContentBinding:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from None
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from None
    _plan_ref(ref, maximum)
    _plan_ref(ver, maximum)
    _plan_digest(sha)


def _binding_from_dict(value, maximum):
    if type(value) is not dict:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from None
    if set(value) != {"ref", "version", "sha256"}:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from None
    ref = value["ref"]
    ver = value["version"]
    sha = value["sha256"]
    if type(ref) is not str or type(ver) is not str:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from None
    _plan_ref(ref, maximum)
    _plan_ref(ver, maximum)
    _plan_digest(sha)
    try:
        return ContentBinding(ref=ref, version=ver, sha256=sha)
    except ValueError as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from exc


def _binding_to_dict(value):
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from None
    return {"ref": ref, "version": ver, "sha256": sha}


@dataclass(frozen=True, slots=True, repr=False)
class WithdrawalPlan:
    object_type: str
    schema_version: str
    plan_ref: str
    plan_version: str
    installation_ref: str
    target_ref: str
    catalog_operation: str
    catalog_version: str
    operation_id: str
    idempotency_key: str
    policy_ref: str
    policy_version: str
    initial_publication_binding: ContentBinding
    anchor_binding: ContentBinding
    installation_result_ref: str
    quiescence_scope: str

    def __post_init__(self):
        _check_withdrawal_plan(self, None)


def _check_withdrawal_plan(value, limits):
    if type(value) is not WithdrawalPlan:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_INPUT_INVALID") from None
    maximum = None
    if limits is not None:
        _, maximum = _limits_max(limits)
    try:
        getters = {n: object.__getattribute__(value, n) for n in _FIELDS}
    except AttributeError:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_FIELDS_INVALID") from None
    if type(getters["object_type"]) is not str or getters["object_type"] != _OBJECT_TYPE:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_TYPE_INVALID") from None
    if type(getters["schema_version"]) is not str or getters["schema_version"] != _SCHEMA_VERSION:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_VERSION_INVALID") from None
    if type(getters["catalog_operation"]) is not str or getters["catalog_operation"] != _CATALOG_OPERATION:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_OPERATION_INVALID") from None
    if type(getters["catalog_version"]) is not str or getters["catalog_version"] != _CATALOG_VERSION:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_VERSION_INVALID") from None
    if type(getters["quiescence_scope"]) is not str or getters["quiescence_scope"] != _QUIESCENCE:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_QUIESCENCE_INVALID") from None
    for name in _REF_FIELDS:
        item = getters[name]
        if name in ("installation_ref", "target_ref"):
            _plan_ref_no_wildcard(item, maximum)
        else:
            _plan_ref(item, maximum)
    _check_binding_value(getters["initial_publication_binding"], maximum)
    _check_binding_value(getters["anchor_binding"], maximum)


def _plan_to_dict(value):
    try:
        out = {
            "object_type": object.__getattribute__(value, "object_type"),
            "schema_version": object.__getattribute__(value, "schema_version"),
            "plan_ref": object.__getattribute__(value, "plan_ref"),
            "plan_version": object.__getattribute__(value, "plan_version"),
            "installation_ref": object.__getattribute__(value, "installation_ref"),
            "target_ref": object.__getattribute__(value, "target_ref"),
            "catalog_operation": object.__getattribute__(value, "catalog_operation"),
            "catalog_version": object.__getattribute__(value, "catalog_version"),
            "operation_id": object.__getattribute__(value, "operation_id"),
            "idempotency_key": object.__getattribute__(value, "idempotency_key"),
            "policy_ref": object.__getattribute__(value, "policy_ref"),
            "policy_version": object.__getattribute__(value, "policy_version"),
            "initial_publication_binding": _binding_to_dict(object.__getattribute__(value, "initial_publication_binding")),
            "anchor_binding": _binding_to_dict(object.__getattribute__(value, "anchor_binding")),
            "installation_result_ref": object.__getattribute__(value, "installation_result_ref"),
            "quiescence_scope": object.__getattribute__(value, "quiescence_scope"),
        }
    except AttributeError:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_FIELDS_INVALID") from None
    return out


def _plan_encode(obj, max_bytes):
    try:
        text = json.dumps(obj, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_ENCODE_INVALID") from exc
    try:
        size = len(text.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_UTF8_INVALID") from exc
    if size > max_bytes:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_PAYLOAD_LIMIT_EXCEEDED") from None
    return text


def encode_withdrawal_plan(value: WithdrawalPlan, *, limits: PayloadLimits) -> str:
    if type(limits) is not PayloadLimits:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    max_bytes, _ = _limits_max(limits)
    _check_withdrawal_plan(value, limits)
    return _plan_encode(_plan_to_dict(value), max_bytes)


def decode_withdrawal_plan(text: str, *, limits: PayloadLimits) -> WithdrawalPlan:
    if type(limits) is not PayloadLimits:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    max_bytes, max_ref = _limits_max(limits)
    if type(text) is not str:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_INPUT_INVALID") from None
    try:
        if len(text.encode("utf-8")) > max_bytes:
            raise WithdrawalPlanError("WITHDRAWAL_PLAN_PAYLOAD_LIMIT_EXCEEDED") from None
        value = json.loads(text, object_pairs_hook=_plan_pairs, parse_int=_plan_number, parse_float=_plan_number, parse_constant=_plan_constant)
    except UnicodeEncodeError as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_UTF8_INVALID") from exc
    except (json.JSONDecodeError, RecursionError) as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_JSON_INVALID") from exc
    if type(value) is not dict:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_OBJECT_REQUIRED") from None
    if set(value) != _FIELDS:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_FIELDS_INVALID") from None
    value["initial_publication_binding"] = _binding_from_dict(value["initial_publication_binding"], max_ref)
    value["anchor_binding"] = _binding_from_dict(value["anchor_binding"], max_ref)
    try:
        result = WithdrawalPlan(**value)
    except TypeError as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_FIELDS_INVALID") from exc
    _check_withdrawal_plan(result, limits)
    return result


def withdrawal_plan_binding(value: WithdrawalPlan, *, limits: PayloadLimits) -> ContentBinding:
    if type(limits) is not PayloadLimits:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_LIMITS_INVALID") from None
    _check_withdrawal_plan(value, limits)
    text = encode_withdrawal_plan(value, limits=limits)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    try:
        plan_ref = object.__getattribute__(value, "plan_ref")
        plan_version = object.__getattribute__(value, "plan_version")
    except AttributeError:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_FIELDS_INVALID") from None
    try:
        return ContentBinding(ref=plan_ref, version=plan_version, sha256=digest)
    except ValueError as exc:
        raise WithdrawalPlanError("WITHDRAWAL_PLAN_BINDING_INVALID") from exc
