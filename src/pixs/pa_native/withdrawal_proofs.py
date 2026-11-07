# FILE: src/pixs/pa_native/withdrawal_proofs.py
"""Bundle de preuves PA, forme seule 18 champs.

Forme pure, sans admission, acte, effet, fraicheur, politique
courante, autorite, mandat, droit, consommation, signature ou
provenance authentique. Document ferme 18 champs, CANON
deterministe hors document. PayloadLimits PG externe explicite
reutilise tel quel, sans nouveau profil. Liaisons plan_binding,
confirmation_binding, anchor_binding fournies seulement
structurees, jamais preuves d'autorite ni de resultat. Sans
clock, duree, TTL, grace, port, NV, SQL, signature, producteur,
C08ResultReader, audit, runtime, mandat futur, A07, claims,
booleen verifie.
"""
from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding
    from .postgresql_contracts import PayloadLimits
elif __package__ in (None, ""):
    import sys as _proofs_sys
    if "postgresql_contracts" not in _proofs_sys.builtin_module_names:
        raise ImportError("WITHDRAWAL_PROOFS_PG_BUILTIN_MISSING")
    import postgresql_contracts as _proofs_pg
    ContentBinding = _proofs_pg.ContentBinding
    PayloadLimits = _proofs_pg.PayloadLimits
else:
    raise ImportError("WITHDRAWAL_PROOFS_CONTEXT_REFUSED")

__all__ = [
    "WithdrawalProofsError",
    "WithdrawalProofs",
    "encode_withdrawal_proofs",
    "decode_withdrawal_proofs",
    "withdrawal_proofs_binding",
]

_FIXED_MESSAGE = "Bundle de preuves invalide."
_OBJECT_TYPE = "pixs.agent.withdrawal_proofs/v1"
_SCHEMA_VERSION = "1.0.0"
_FIELDS = frozenset({
    "object_type", "schema_version", "proofs_ref", "proofs_version",
    "installation_ref", "target_ref", "operation_id", "idempotency_key",
    "plan_binding", "confirmation_binding", "installation_result_ref",
    "authorization_decision_ref", "operator_ref", "operator_key_ref",
    "policy_ref", "policy_version", "anchor_binding", "prepared_at",
})
_REF_FIELDS = (
    "proofs_ref", "proofs_version", "installation_ref",
    "target_ref", "operation_id", "idempotency_key",
    "installation_result_ref", "authorization_decision_ref",
    "operator_ref", "operator_key_ref", "policy_ref",
    "policy_version",
)
_BINDING_FIELDS = (
    "plan_binding", "confirmation_binding", "anchor_binding",
)
_WILDCARDS = ("*", "?", "[", "]")
_DIGEST = re.compile(r"[0-9a-f]{64}")


class WithdrawalProofsError(ValueError):
    def __init__(self, code="WITHDRAWAL_PROOFS_INVALID"):
        super().__init__(_FIXED_MESSAGE)
        self.code = code
        self.element = "withdrawal_proofs"
        self.step = "validate_withdrawal_proofs"


def _fail(code="WITHDRAWAL_PROOFS_INVALID"):
    raise WithdrawalProofsError(code) from None


def _proofs_ref(value, maximum):
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
            raise WithdrawalProofsError("WITHDRAWAL_PROOFS_REFERENCE_LIMIT_EXCEEDED") from None


def _proofs_ref_no_wildcard(value, maximum):
    _proofs_ref(value, maximum)
    for w in _WILDCARDS:
        if w in value:
            raise WithdrawalProofsError("WITHDRAWAL_PROOFS_WILDCARD_REFUSED") from None


def _proofs_digest(value):
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        _fail()


def _proofs_number(_value):
    raise WithdrawalProofsError("WITHDRAWAL_PROOFS_NUMBER_NOT_ALLOWED") from None


def _proofs_constant(_value):
    raise WithdrawalProofsError("WITHDRAWAL_PROOFS_CONSTANT_INVALID") from None


def _proofs_pairs(pairs):
    data = {}
    for name, item in pairs:
        if name in data:
            raise WithdrawalProofsError("WITHDRAWAL_PROOFS_FIELD_DUPLICATED") from None
        data[name] = item
    return data


def _limits_max(limits):
    if type(limits) is not PayloadLimits:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    try:
        jb = object.__getattribute__(limits, "max_json_bytes")
        rb = object.__getattribute__(limits, "max_ref_bytes")
        ob = object.__getattribute__(limits, "max_observation_refs")
    except AttributeError:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    if type(jb) is not int or type(rb) is not int or type(ob) is not int:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    if jb <= 0 or rb <= 0 or ob <= 0:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    return jb, rb


def _check_binding_value(value, maximum):
    if type(value) is not ContentBinding:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from None
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from None
    _proofs_ref(ref, maximum)
    _proofs_ref(ver, maximum)
    _proofs_digest(sha)


def _binding_from_dict(value, maximum):
    if type(value) is not dict:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from None
    if set(value) != {"ref", "version", "sha256"}:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from None
    ref = value["ref"]
    ver = value["version"]
    sha = value["sha256"]
    if type(ref) is not str or type(ver) is not str:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from None
    _proofs_ref(ref, maximum)
    _proofs_ref(ver, maximum)
    _proofs_digest(sha)
    try:
        return ContentBinding(ref=ref, version=ver, sha256=sha)
    except ValueError as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from exc


def _binding_to_dict(value):
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from None
    return {"ref": ref, "version": ver, "sha256": sha}


def _check_utc6_shape(value):
    if type(value) is not str or len(value) != 27:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_TIME_INVALID") from None
    if (value[4] != "-" or value[7] != "-" or value[10] != "T"
            or value[13] != ":" or value[16] != ":" or value[19] != "."
            or value[26] != "Z"):
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_TIME_INVALID") from None
    digits = value[0:4] + value[5:7] + value[8:10] + value[11:13] + value[14:16] + value[17:19] + value[20:26]
    for ch in digits:
        if ch < "0" or ch > "9":
            raise WithdrawalProofsError("WITHDRAWAL_PROOFS_TIME_INVALID") from None


def _check_prepared_at(value):
    _check_utc6_shape(value)
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except (TypeError, ValueError):
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_TIME_INVALID") from None


@dataclass(frozen=True, slots=True, repr=False)
class WithdrawalProofs:
    object_type: str
    schema_version: str
    proofs_ref: str
    proofs_version: str
    installation_ref: str
    target_ref: str
    operation_id: str
    idempotency_key: str
    plan_binding: ContentBinding
    confirmation_binding: ContentBinding
    installation_result_ref: str
    authorization_decision_ref: str
    operator_ref: str
    operator_key_ref: str
    policy_ref: str
    policy_version: str
    anchor_binding: ContentBinding
    prepared_at: str

    def __post_init__(self):
        _check_withdrawal_proofs(self, None)


def _check_withdrawal_proofs(value, limits):
    if type(value) is not WithdrawalProofs:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_INPUT_INVALID") from None
    maximum = None
    if limits is not None:
        _, maximum = _limits_max(limits)
    try:
        getters = {n: object.__getattribute__(value, n) for n in _FIELDS}
    except AttributeError:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_FIELDS_INVALID") from None
    if type(getters["object_type"]) is not str or getters["object_type"] != _OBJECT_TYPE:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_TYPE_INVALID") from None
    if type(getters["schema_version"]) is not str or getters["schema_version"] != _SCHEMA_VERSION:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_VERSION_INVALID") from None
    for name in _REF_FIELDS:
        item = getters[name]
        if name in ("installation_ref", "target_ref"):
            _proofs_ref_no_wildcard(item, maximum)
        else:
            _proofs_ref(item, maximum)
    for name in _BINDING_FIELDS:
        _check_binding_value(getters[name], maximum)
    _check_prepared_at(getters["prepared_at"])


def _proofs_to_dict(value):
    try:
        out = {
            "object_type": object.__getattribute__(value, "object_type"),
            "schema_version": object.__getattribute__(value, "schema_version"),
            "proofs_ref": object.__getattribute__(value, "proofs_ref"),
            "proofs_version": object.__getattribute__(value, "proofs_version"),
            "installation_ref": object.__getattribute__(value, "installation_ref"),
            "target_ref": object.__getattribute__(value, "target_ref"),
            "operation_id": object.__getattribute__(value, "operation_id"),
            "idempotency_key": object.__getattribute__(value, "idempotency_key"),
            "plan_binding": _binding_to_dict(object.__getattribute__(value, "plan_binding")),
            "confirmation_binding": _binding_to_dict(object.__getattribute__(value, "confirmation_binding")),
            "installation_result_ref": object.__getattribute__(value, "installation_result_ref"),
            "authorization_decision_ref": object.__getattribute__(value, "authorization_decision_ref"),
            "operator_ref": object.__getattribute__(value, "operator_ref"),
            "operator_key_ref": object.__getattribute__(value, "operator_key_ref"),
            "policy_ref": object.__getattribute__(value, "policy_ref"),
            "policy_version": object.__getattribute__(value, "policy_version"),
            "anchor_binding": _binding_to_dict(object.__getattribute__(value, "anchor_binding")),
            "prepared_at": object.__getattribute__(value, "prepared_at"),
        }
    except AttributeError:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_FIELDS_INVALID") from None
    return out


def _proofs_encode(obj, max_bytes):
    try:
        text = json.dumps(obj, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_ENCODE_INVALID") from exc
    try:
        size = len(text.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_UTF8_INVALID") from exc
    if size > max_bytes:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_PAYLOAD_LIMIT_EXCEEDED") from None
    return text


def encode_withdrawal_proofs(value: WithdrawalProofs, *, limits: PayloadLimits) -> str:
    if type(limits) is not PayloadLimits:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    max_bytes, _ = _limits_max(limits)
    _check_withdrawal_proofs(value, limits)
    return _proofs_encode(_proofs_to_dict(value), max_bytes)


def decode_withdrawal_proofs(text: str, *, limits: PayloadLimits) -> WithdrawalProofs:
    if type(limits) is not PayloadLimits:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    max_bytes, max_ref = _limits_max(limits)
    if type(text) is not str:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_INPUT_INVALID") from None
    try:
        if len(text.encode("utf-8")) > max_bytes:
            raise WithdrawalProofsError("WITHDRAWAL_PROOFS_PAYLOAD_LIMIT_EXCEEDED") from None
        value = json.loads(text, object_pairs_hook=_proofs_pairs, parse_int=_proofs_number, parse_float=_proofs_number, parse_constant=_proofs_constant)
    except UnicodeEncodeError as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_UTF8_INVALID") from exc
    except (json.JSONDecodeError, RecursionError) as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_JSON_INVALID") from exc
    if type(value) is not dict:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_OBJECT_REQUIRED") from None
    if set(value) != _FIELDS:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_FIELDS_INVALID") from None
    for name in _BINDING_FIELDS:
        value[name] = _binding_from_dict(value[name], max_ref)
    try:
        result = WithdrawalProofs(**value)
    except TypeError as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_FIELDS_INVALID") from exc
    _check_withdrawal_proofs(result, limits)
    return result


def withdrawal_proofs_binding(value: WithdrawalProofs, *, limits: PayloadLimits) -> ContentBinding:
    if type(limits) is not PayloadLimits:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_LIMITS_INVALID") from None
    _check_withdrawal_proofs(value, limits)
    text = encode_withdrawal_proofs(value, limits=limits)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    try:
        ref = object.__getattribute__(value, "proofs_ref")
        ver = object.__getattribute__(value, "proofs_version")
    except AttributeError:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_FIELDS_INVALID") from None
    try:
        return ContentBinding(ref=ref, version=ver, sha256=digest)
    except ValueError as exc:
        raise WithdrawalProofsError("WITHDRAWAL_PROOFS_BINDING_INVALID") from exc
