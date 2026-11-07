# FILE: src/pixs/pa_native/withdrawal_confirmation.py
"""Confirmation C08 de retrait PA, forme seule 17 champs.

Forme pure, sans admission, acte, preuve materielle, fraicheur,
politique courante, autorite, mandat, droit, effet, consommation,
signature ou provenance authentique. Document ferme 17 champs,
CANON deterministe hors document. PayloadLimits PG externe explicite
reutilise tel quel, sans nouveau profil. Liaison plan_binding fournie
seulement structuree, jamais preuve d'autorite. Sans clock, duree,
TTL, grace, port, NV, SQL, signature.
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
    import sys as _conf_sys
    if "postgresql_contracts" not in _conf_sys.builtin_module_names:
        raise ImportError("WITHDRAWAL_CONFIRMATION_PG_BUILTIN_MISSING")
    import postgresql_contracts as _conf_pg
    ContentBinding = _conf_pg.ContentBinding
    PayloadLimits = _conf_pg.PayloadLimits
else:
    raise ImportError("WITHDRAWAL_CONFIRMATION_CONTEXT_REFUSED")

__all__ = [
    "WithdrawalConfirmationError",
    "WithdrawalConfirmation",
    "encode_withdrawal_confirmation",
    "decode_withdrawal_confirmation",
    "withdrawal_confirmation_binding",
]

_FIXED_MESSAGE = "Confirmation de retrait invalide."
_OBJECT_TYPE = "pixs.c08.pa_initial_withdrawal_confirmation/v1"
_SCHEMA_VERSION = "1.0.0"
_FIELDS = frozenset({
    "object_type", "schema_version", "confirmation_ref", "confirmation_version",
    "installation_ref", "target_ref", "operation_id", "idempotency_key",
    "plan_binding", "policy_ref", "policy_version", "operator_ref",
    "operator_key_ref", "confirmer_subject_ref", "authorization_decision_ref",
    "confirmed_at", "correlation_id",
})
_REF_FIELDS = (
    "confirmation_ref", "confirmation_version", "installation_ref",
    "target_ref", "operation_id", "idempotency_key", "policy_ref",
    "policy_version", "operator_ref", "operator_key_ref",
    "confirmer_subject_ref", "authorization_decision_ref", "correlation_id",
)
_WILDCARDS = ("*", "?", "[", "]")
_DIGEST = re.compile(r"[0-9a-f]{64}")


class WithdrawalConfirmationError(ValueError):
    def __init__(self, code="WITHDRAWAL_CONFIRMATION_INVALID"):
        super().__init__(_FIXED_MESSAGE)
        self.code = code
        self.element = "withdrawal_confirmation"
        self.step = "validate_withdrawal_confirmation"


def _fail(code="WITHDRAWAL_CONFIRMATION_INVALID"):
    raise WithdrawalConfirmationError(code) from None


def _conf_ref(value, maximum):
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
            raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_REFERENCE_LIMIT_EXCEEDED") from None


def _conf_ref_no_wildcard(value, maximum):
    _conf_ref(value, maximum)
    for w in _WILDCARDS:
        if w in value:
            raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_WILDCARD_REFUSED") from None


def _conf_digest(value):
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        _fail()


def _conf_number(_value):
    raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_NUMBER_NOT_ALLOWED") from None


def _conf_constant(_value):
    raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_CONSTANT_INVALID") from None


def _conf_pairs(pairs):
    data = {}
    for name, item in pairs:
        if name in data:
            raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_FIELD_DUPLICATED") from None
        data[name] = item
    return data


def _limits_max(limits):
    if type(limits) is not PayloadLimits:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    try:
        jb = object.__getattribute__(limits, "max_json_bytes")
        rb = object.__getattribute__(limits, "max_ref_bytes")
        ob = object.__getattribute__(limits, "max_observation_refs")
    except AttributeError:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    if type(jb) is not int or type(rb) is not int or type(ob) is not int:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    if jb <= 0 or rb <= 0 or ob <= 0:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    return jb, rb


def _check_binding_value(value, maximum):
    if type(value) is not ContentBinding:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from None
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from None
    _conf_ref(ref, maximum)
    _conf_ref(ver, maximum)
    _conf_digest(sha)


def _binding_from_dict(value, maximum):
    if type(value) is not dict:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from None
    if set(value) != {"ref", "version", "sha256"}:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from None
    ref = value["ref"]
    ver = value["version"]
    sha = value["sha256"]
    if type(ref) is not str or type(ver) is not str:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from None
    _conf_ref(ref, maximum)
    _conf_ref(ver, maximum)
    _conf_digest(sha)
    try:
        return ContentBinding(ref=ref, version=ver, sha256=sha)
    except ValueError as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from exc


def _binding_to_dict(value):
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from None
    return {"ref": ref, "version": ver, "sha256": sha}


def _check_utc6_shape(value):
    if type(value) is not str or len(value) != 27:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_TIME_INVALID") from None
    if (value[4] != "-" or value[7] != "-" or value[10] != "T"
            or value[13] != ":" or value[16] != ":" or value[19] != "."
            or value[26] != "Z"):
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_TIME_INVALID") from None
    digits = value[0:4] + value[5:7] + value[8:10] + value[11:13] + value[14:16] + value[17:19] + value[20:26]
    for ch in digits:
        if ch < "0" or ch > "9":
            raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_TIME_INVALID") from None


def _check_confirmed_at(value):
    _check_utc6_shape(value)
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except (TypeError, ValueError):
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_TIME_INVALID") from None


@dataclass(frozen=True, slots=True, repr=False)
class WithdrawalConfirmation:
    object_type: str
    schema_version: str
    confirmation_ref: str
    confirmation_version: str
    installation_ref: str
    target_ref: str
    operation_id: str
    idempotency_key: str
    plan_binding: ContentBinding
    policy_ref: str
    policy_version: str
    operator_ref: str
    operator_key_ref: str
    confirmer_subject_ref: str
    authorization_decision_ref: str
    confirmed_at: str
    correlation_id: str

    def __post_init__(self):
        _check_withdrawal_confirmation(self, None)


def _check_withdrawal_confirmation(value, limits):
    if type(value) is not WithdrawalConfirmation:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_INPUT_INVALID") from None
    maximum = None
    if limits is not None:
        _, maximum = _limits_max(limits)
    try:
        getters = {n: object.__getattribute__(value, n) for n in _FIELDS}
    except AttributeError:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_FIELDS_INVALID") from None
    if type(getters["object_type"]) is not str or getters["object_type"] != _OBJECT_TYPE:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_TYPE_INVALID") from None
    if type(getters["schema_version"]) is not str or getters["schema_version"] != _SCHEMA_VERSION:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_VERSION_INVALID") from None
    for name in _REF_FIELDS:
        item = getters[name]
        if name in ("installation_ref", "target_ref"):
            _conf_ref_no_wildcard(item, maximum)
        else:
            _conf_ref(item, maximum)
    _check_binding_value(getters["plan_binding"], maximum)
    _check_confirmed_at(getters["confirmed_at"])


def _conf_to_dict(value):
    try:
        out = {
            "object_type": object.__getattribute__(value, "object_type"),
            "schema_version": object.__getattribute__(value, "schema_version"),
            "confirmation_ref": object.__getattribute__(value, "confirmation_ref"),
            "confirmation_version": object.__getattribute__(value, "confirmation_version"),
            "installation_ref": object.__getattribute__(value, "installation_ref"),
            "target_ref": object.__getattribute__(value, "target_ref"),
            "operation_id": object.__getattribute__(value, "operation_id"),
            "idempotency_key": object.__getattribute__(value, "idempotency_key"),
            "plan_binding": _binding_to_dict(object.__getattribute__(value, "plan_binding")),
            "policy_ref": object.__getattribute__(value, "policy_ref"),
            "policy_version": object.__getattribute__(value, "policy_version"),
            "operator_ref": object.__getattribute__(value, "operator_ref"),
            "operator_key_ref": object.__getattribute__(value, "operator_key_ref"),
            "confirmer_subject_ref": object.__getattribute__(value, "confirmer_subject_ref"),
            "authorization_decision_ref": object.__getattribute__(value, "authorization_decision_ref"),
            "confirmed_at": object.__getattribute__(value, "confirmed_at"),
            "correlation_id": object.__getattribute__(value, "correlation_id"),
        }
    except AttributeError:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_FIELDS_INVALID") from None
    return out


def _conf_encode(obj, max_bytes):
    try:
        text = json.dumps(obj, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_ENCODE_INVALID") from exc
    try:
        size = len(text.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_UTF8_INVALID") from exc
    if size > max_bytes:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_PAYLOAD_LIMIT_EXCEEDED") from None
    return text


def encode_withdrawal_confirmation(value: WithdrawalConfirmation, *, limits: PayloadLimits) -> str:
    if type(limits) is not PayloadLimits:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    max_bytes, _ = _limits_max(limits)
    _check_withdrawal_confirmation(value, limits)
    return _conf_encode(_conf_to_dict(value), max_bytes)


def decode_withdrawal_confirmation(text: str, *, limits: PayloadLimits) -> WithdrawalConfirmation:
    if type(limits) is not PayloadLimits:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    max_bytes, max_ref = _limits_max(limits)
    if type(text) is not str:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_INPUT_INVALID") from None
    try:
        if len(text.encode("utf-8")) > max_bytes:
            raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_PAYLOAD_LIMIT_EXCEEDED") from None
        value = json.loads(text, object_pairs_hook=_conf_pairs, parse_int=_conf_number, parse_float=_conf_number, parse_constant=_conf_constant)
    except UnicodeEncodeError as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_UTF8_INVALID") from exc
    except (json.JSONDecodeError, RecursionError) as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_JSON_INVALID") from exc
    if type(value) is not dict:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_OBJECT_REQUIRED") from None
    if set(value) != _FIELDS:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_FIELDS_INVALID") from None
    value["plan_binding"] = _binding_from_dict(value["plan_binding"], max_ref)
    try:
        result = WithdrawalConfirmation(**value)
    except TypeError as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_FIELDS_INVALID") from exc
    _check_withdrawal_confirmation(result, limits)
    return result


def withdrawal_confirmation_binding(value: WithdrawalConfirmation, *, limits: PayloadLimits) -> ContentBinding:
    if type(limits) is not PayloadLimits:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_LIMITS_INVALID") from None
    _check_withdrawal_confirmation(value, limits)
    text = encode_withdrawal_confirmation(value, limits=limits)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    try:
        ref = object.__getattribute__(value, "confirmation_ref")
        ver = object.__getattribute__(value, "confirmation_version")
    except AttributeError:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_FIELDS_INVALID") from None
    try:
        return ContentBinding(ref=ref, version=ver, sha256=digest)
    except ValueError as exc:
        raise WithdrawalConfirmationError("WITHDRAWAL_CONFIRMATION_BINDING_INVALID") from exc
