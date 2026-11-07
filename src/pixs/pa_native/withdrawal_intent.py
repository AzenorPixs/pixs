# FILE: src/pixs/pa_native/withdrawal_intent.py
"""Intention de retrait PA, forme seule 7 champs.

Forme pure, sans admission, acte, effet, journal, Extend, NV,
politique, operateur, idempotence propre, mandat futur, A07,
claims, booleen verifie, signature, autorite ou provenance
authentique. Document ferme 7 champs, CANON deterministe hors
document. PayloadLimits PG externe explicite reutilise tel quel,
sans nouveau profil. Liaisons request_binding et
signed_mandate_binding fournies seulement structurees, jamais
preuves de requete, de mandat, de signature ou d'autorite.
Sans clock, date, TTL, grace, port, NV, SQL, runtime, lecteur
de mandat, contexte admin courant. Resolutions proprietaires,
comparaisons et signatures actuelles restant des DEPENDANCES,
jamais vraies depuis ce candidat.
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
    import sys as _intent_sys
    if "postgresql_contracts" not in _intent_sys.builtin_module_names:
        raise ImportError("WITHDRAWAL_INTENT_PG_BUILTIN_MISSING")
    import postgresql_contracts as _intent_pg
    ContentBinding = _intent_pg.ContentBinding
    PayloadLimits = _intent_pg.PayloadLimits
else:
    raise ImportError("WITHDRAWAL_INTENT_CONTEXT_REFUSED")

__all__ = [
    "WithdrawalIntentError",
    "WithdrawalIntent",
    "encode_withdrawal_intent",
    "decode_withdrawal_intent",
    "withdrawal_intent_binding",
]

_FIXED_MESSAGE = "Intention de retrait invalide."
_OBJECT_TYPE = "pixs.agent.withdrawal_intent/v1"
_SCHEMA_VERSION = "1.0.0"
_BINDING_VERSION = "1.0.0"
_FIELDS = frozenset({
    "object_type", "schema_version", "installation_ref",
    "target_ref", "operation_id", "request_binding",
    "signed_mandate_binding",
})
_REF_FIELDS = (
    "installation_ref", "target_ref", "operation_id",
)
_BINDING_FIELDS = (
    "request_binding", "signed_mandate_binding",
)
_WILDCARDS = ("*", "?", "[", "]")
_DIGEST = re.compile(r"[0-9a-f]{64}")


class WithdrawalIntentError(ValueError):
    def __init__(self, code="WITHDRAWAL_INTENT_INVALID"):
        super().__init__(_FIXED_MESSAGE)
        self.code = code
        self.element = "withdrawal_intent"
        self.step = "validate_withdrawal_intent"


def _fail(code="WITHDRAWAL_INTENT_INVALID"):
    raise WithdrawalIntentError(code) from None


def _intent_ref(value, maximum):
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
            raise WithdrawalIntentError("WITHDRAWAL_INTENT_REFERENCE_LIMIT_EXCEEDED") from None


def _intent_ref_no_wildcard(value, maximum):
    _intent_ref(value, maximum)
    for w in _WILDCARDS:
        if w in value:
            raise WithdrawalIntentError("WITHDRAWAL_INTENT_WILDCARD_REFUSED") from None


def _intent_digest(value):
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        _fail()


def _intent_number(_value):
    raise WithdrawalIntentError("WITHDRAWAL_INTENT_NUMBER_NOT_ALLOWED") from None


def _intent_constant(_value):
    raise WithdrawalIntentError("WITHDRAWAL_INTENT_CONSTANT_INVALID") from None


def _intent_pairs(pairs):
    data = {}
    for name, item in pairs:
        if name in data:
            raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELD_DUPLICATED") from None
        data[name] = item
    return data


def _limits_max(limits):
    if type(limits) is not PayloadLimits:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    try:
        jb = object.__getattribute__(limits, "max_json_bytes")
        rb = object.__getattribute__(limits, "max_ref_bytes")
        ob = object.__getattribute__(limits, "max_observation_refs")
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    if type(jb) is not int or type(rb) is not int or type(ob) is not int:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    if jb <= 0 or rb <= 0 or ob <= 0:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    return jb, rb


def _check_binding_value(value, maximum):
    if type(value) is not ContentBinding:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    _intent_ref(ref, maximum)
    if type(ver) is not str or ver != _BINDING_VERSION:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    _intent_ref(ver, maximum)
    _intent_digest(sha)


def _binding_from_dict(value, maximum):
    if type(value) is not dict:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    if set(value) != {"ref", "version", "sha256"}:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    ref = value["ref"]
    ver = value["version"]
    sha = value["sha256"]
    if type(ref) is not str or type(ver) is not str:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    _intent_ref(ref, maximum)
    if ver != _BINDING_VERSION:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    _intent_ref(ver, maximum)
    _intent_digest(sha)
    try:
        return ContentBinding(ref=ref, version=ver, sha256=sha)
    except ValueError as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from exc


def _binding_to_dict(value):
    try:
        ref = object.__getattribute__(value, "ref")
        ver = object.__getattribute__(value, "version")
        sha = object.__getattribute__(value, "sha256")
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from None
    return {"ref": ref, "version": ver, "sha256": sha}


@dataclass(frozen=True, slots=True, repr=False)
class WithdrawalIntent:
    object_type: str
    schema_version: str
    installation_ref: str
    target_ref: str
    operation_id: str
    request_binding: ContentBinding
    signed_mandate_binding: ContentBinding

    def __post_init__(self):
        _check_withdrawal_intent(self, None)


def _check_withdrawal_intent(value, limits):
    if type(value) is not WithdrawalIntent:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_INPUT_INVALID") from None
    maximum = None
    if limits is not None:
        _, maximum = _limits_max(limits)
    try:
        getters = {n: object.__getattribute__(value, n) for n in _FIELDS}
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELDS_INVALID") from None
    if type(getters["object_type"]) is not str or getters["object_type"] != _OBJECT_TYPE:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_TYPE_INVALID") from None
    if type(getters["schema_version"]) is not str or getters["schema_version"] != _SCHEMA_VERSION:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_VERSION_INVALID") from None
    for name in _REF_FIELDS:
        item = getters[name]
        if name in ("installation_ref", "target_ref"):
            _intent_ref_no_wildcard(item, maximum)
        else:
            _intent_ref(item, maximum)
    for name in _BINDING_FIELDS:
        _check_binding_value(getters[name], maximum)
    try:
        req_ref = object.__getattribute__(getters["request_binding"], "ref")
        op_id = getters["operation_id"]
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELDS_INVALID") from None
    if type(req_ref) is not str or req_ref != op_id:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_REQUEST_REF_INVALID") from None


def _intent_to_dict(value):
    try:
        out = {
            "object_type": object.__getattribute__(value, "object_type"),
            "schema_version": object.__getattribute__(value, "schema_version"),
            "installation_ref": object.__getattribute__(value, "installation_ref"),
            "target_ref": object.__getattribute__(value, "target_ref"),
            "operation_id": object.__getattribute__(value, "operation_id"),
            "request_binding": _binding_to_dict(object.__getattribute__(value, "request_binding")),
            "signed_mandate_binding": _binding_to_dict(object.__getattribute__(value, "signed_mandate_binding")),
        }
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELDS_INVALID") from None
    return out


def _intent_encode(obj, max_bytes):
    try:
        text = json.dumps(obj, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_ENCODE_INVALID") from exc
    try:
        size = len(text.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_UTF8_INVALID") from exc
    if size > max_bytes:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_PAYLOAD_LIMIT_EXCEEDED") from None
    return text


def encode_withdrawal_intent(value: WithdrawalIntent, *, limits: PayloadLimits) -> str:
    if type(limits) is not PayloadLimits:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    max_bytes, _ = _limits_max(limits)
    _check_withdrawal_intent(value, limits)
    return _intent_encode(_intent_to_dict(value), max_bytes)


def decode_withdrawal_intent(text: str, *, limits: PayloadLimits) -> WithdrawalIntent:
    if type(limits) is not PayloadLimits:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    max_bytes, max_ref = _limits_max(limits)
    if type(text) is not str:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_INPUT_INVALID") from None
    try:
        if len(text.encode("utf-8")) > max_bytes:
            raise WithdrawalIntentError("WITHDRAWAL_INTENT_PAYLOAD_LIMIT_EXCEEDED") from None
        value = json.loads(text, object_pairs_hook=_intent_pairs, parse_int=_intent_number, parse_float=_intent_number, parse_constant=_intent_constant)
    except UnicodeEncodeError as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_UTF8_INVALID") from exc
    except (json.JSONDecodeError, RecursionError) as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_JSON_INVALID") from exc
    if type(value) is not dict:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_OBJECT_REQUIRED") from None
    if set(value) != _FIELDS:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELDS_INVALID") from None
    for name in _BINDING_FIELDS:
        value[name] = _binding_from_dict(value[name], max_ref)
    try:
        result = WithdrawalIntent(**value)
    except TypeError as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELDS_INVALID") from exc
    _check_withdrawal_intent(result, limits)
    return result


def withdrawal_intent_binding(value: WithdrawalIntent, *, limits: PayloadLimits) -> ContentBinding:
    if type(limits) is not PayloadLimits:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_LIMITS_INVALID") from None
    _check_withdrawal_intent(value, limits)
    text = encode_withdrawal_intent(value, limits=limits)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    try:
        ref = object.__getattribute__(value, "operation_id")
        ver = object.__getattribute__(value, "schema_version")
    except AttributeError:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_FIELDS_INVALID") from None
    try:
        return ContentBinding(ref=ref, version=ver, sha256=digest)
    except ValueError as exc:
        raise WithdrawalIntentError("WITHDRAWAL_INTENT_BINDING_INVALID") from exc
