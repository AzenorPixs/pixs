"""Prepublication B-PUB independante signee (DTO 15 champs, wire 21, enveloppe 2).

FORME pure proposee phase1, code NON QUALIFIE : sans admission, acte,
preuve materielle, TPM, PG, PZT, cle privee, verification crypto ni
qualification. Le document porte 12 scalaires jusqu'a version, un
nv_profile:BootstrapNvProfile reel et 2 UTC6 ; le canon aplati les 7
champs NV. Enveloppe {document,signature_b64} fermee. PayloadLimits
externe borne le chargement ; Resource24 reel explicite borne la
fenetre 0<span_ns<=max_validity_span_ns INCLUSIVE et recoupe
installation/target. Comparaisons pin/binding/profil = coherence de
forme, jamais preuve d'autorite ou de provenance. Sans clock, deadline
JSON, port.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
    from .bootstrap_nv_profile import BootstrapNvProfile
    from .bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
    from .bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_public
    from .bootstrap_resource_profile import BootstrapResourceProfile
    from .bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
    from .bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_nv_profile" in sys.builtin_module_names
            and "bootstrap_resource_profile" in sys.builtin_module_names):
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from bootstrap_nv_profile import BootstrapNvProfile
        from bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
        from bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_public
        from bootstrap_resource_profile import BootstrapResourceProfile
        from bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
        from bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
    else:
        raise ImportError("bootstrap_prepublication: unsupported package context")
else:
    raise ImportError("bootstrap_prepublication: unsupported package context")

__all__ = [
    "BootstrapPrepublicationContractError",
    "BootstrapPrepublication",
    "BootstrapPrepublicationEnvelope",
    "encode_bootstrap_prepublication",
    "decode_bootstrap_prepublication",
    "encode_bootstrap_prepublication_envelope",
    "decode_bootstrap_prepublication_envelope",
    "prepublication_signed_bytes",
    "prepublication_envelope_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_prepublication/v1"
SCHEMA_VERSION = "1.0.0"
DOMAIN = "PA_ADMIN_INITIAL"
PREFIX = "PIXS:PA:BOOTSTRAP:PREPUBLICATION:1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "prepublication_ref",
    "installation_ref",
    "target_ref",
    "policy_ref",
    "policy_version",
    "admin_key_ref",
    "admin_public_key_hex",
    "admin_key_pin",
    "domain",
    "version",
    "nv_index",
    "nv_attributes",
    "nv_name_alg",
    "nv_data_size",
    "nv_authpolicy_hex",
    "nv_name_hex",
    "maintenance_p256_ref",
    "valid_not_before_utc6",
    "valid_not_after_utc6",
)

_WIRE_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "prepublication_ref",
    "installation_ref",
    "target_ref",
    "policy_ref",
    "policy_version",
    "admin_key_ref",
    "admin_public_key_hex",
    "admin_key_pin",
    "domain",
    "version",
    "nv_name_alg",
    "nv_authpolicy_hex",
    "nv_name_hex",
    "maintenance_p256_ref",
    "valid_not_before_utc6",
    "valid_not_after_utc6",
))

_WIRE_INT_FIELDS = frozenset((
    "nv_index",
    "nv_attributes",
    "nv_data_size",
))

_ENVELOPE_NAMES = frozenset((
    "document",
    "signature_b64",
))

_HEX = frozenset("0123456789abcdef")

_MSG = "prepublication : valeur invalide"


class BootstrapPrepublicationContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapPrepublicationContractError(_MSG) from None


def _check_limits(limits: Any) -> None:
    if type(limits) is not PayloadLimits:
        _fail()
    if (type(limits.max_json_bytes) is not int
            or type(limits.max_ref_bytes) is not int
            or type(limits.max_observation_refs) is not int):
        _fail()
    if (isinstance(limits.max_json_bytes, bool)
            or isinstance(limits.max_ref_bytes, bool)
            or isinstance(limits.max_observation_refs, bool)):
        _fail()
    if limits.max_json_bytes <= 0 or limits.max_ref_bytes <= 0 or limits.max_observation_refs <= 0:
        _fail()


def _check_strict_text(value: Any) -> None:
    if type(value) is not str or len(value) == 0:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPrepublicationContractError(_MSG) from None
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127:
            _fail()
        if 0xD800 <= code <= 0xDFFF:
            _fail()


def _check_bounded_ref(value: Any, bound: int) -> None:
    _check_strict_text(value)
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapPrepublicationContractError(_MSG) from None
    if size > bound:
        _fail()


def _check_no_wildcard(value: str) -> None:
    if "*" in value or "?" in value:
        _fail()


def _check_hex64(value: Any) -> None:
    if type(value) is not str or len(value) != 64:
        _fail()
    for ch in value:
        if ch not in _HEX:
            _fail()


def _check_utc6_shape(value: Any) -> None:
    if type(value) is not str or len(value) != 27:
        _fail()
    if (value[4] != "-" or value[7] != "-" or value[10] != "T"
            or value[13] != ":" or value[16] != ":" or value[19] != "."
            or value[26] != "Z"):
        _fail()
    digits = value[0:4] + value[5:7] + value[8:10] + value[11:13] + value[14:16] + value[17:19] + value[20:26]
    for ch in digits:
        if ch < "0" or ch > "9":
            _fail()


def _parse_utc6(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except (TypeError, ValueError):
        _fail()


def _utc6_span_ns(before: str, after: str) -> int:
    delta = _parse_utc6(after) - _parse_utc6(before)
    return int(delta.days * 86400 * 1000000000 + delta.seconds * 1000000000 + delta.microseconds * 1000)


def _check_resource_valid(resource: Any, limits: PayloadLimits) -> None:
    if type(resource) is not BootstrapResourceProfile:
        _fail()
    try:
        res_encode_public(resource, limits)
    except ResContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


def _check_nv_public(nv: Any, limits: PayloadLimits) -> None:
    if type(nv) is not BootstrapNvProfile:
        _fail()
    try:
        nv_encode_public(nv, limits)
    except NvContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


def _check_admin_pin(pub_hex: str, pin: str) -> None:
    try:
        raw = bytes.fromhex(pub_hex)
    except ValueError:
        _fail()
    if len(raw) != 32:
        _fail()
    if hashlib.sha256(raw).hexdigest() != pin:
        _fail()


def _check_sig_b64(sig: Any) -> bytes:
    if type(sig) is not str or len(sig) != 88:
        _fail()
    for ch in sig:
        if ch in "-_":
            _fail()
    try:
        raw = base64.b64decode(sig.encode("ascii"), validate=True)
    except (ValueError, binascii.Error, UnicodeEncodeError) as error:
        raise BootstrapPrepublicationContractError(_MSG) from error
    if len(raw) != 64:
        _fail()
    if base64.b64encode(raw).decode("ascii") != sig:
        _fail()
    return raw


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPrepublication:
    object_type: str
    schema_version: str
    prepublication_ref: str
    installation_ref: str
    target_ref: str
    policy_ref: str
    policy_version: str
    admin_key_ref: str
    admin_public_key_hex: str
    admin_key_pin: str
    domain: str
    version: str
    nv_profile: BootstrapNvProfile
    valid_not_before_utc6: str
    valid_not_after_utc6: str

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        for field in ("prepublication_ref", "installation_ref", "target_ref",
                      "policy_ref", "policy_version", "admin_key_ref", "version"):
            _check_strict_text(getattr(self, field))
        _check_no_wildcard(self.installation_ref)
        _check_no_wildcard(self.target_ref)
        _check_hex64(self.admin_public_key_hex)
        _check_hex64(self.admin_key_pin)
        if type(self.domain) is not str or self.domain != DOMAIN:
            _fail()
        if type(self.nv_profile) is not BootstrapNvProfile:
            _fail()
        _check_admin_pin(self.admin_public_key_hex, self.admin_key_pin)
        _check_utc6_shape(self.valid_not_before_utc6)
        _check_utc6_shape(self.valid_not_after_utc6)
        if _parse_utc6(self.valid_not_after_utc6) <= _parse_utc6(self.valid_not_before_utc6):
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPrepublicationEnvelope:
    document: BootstrapPrepublication
    signature_b64: str

    def __post_init__(self) -> None:
        if type(self.document) is not BootstrapPrepublication:
            _fail()
        _check_sig_b64(self.signature_b64)


def _check_bounded_form(
    value: BootstrapPrepublication,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> None:
    _check_limits(limits)
    _check_resource_valid(resource, limits)
    if type(value) is not BootstrapPrepublication:
        _fail()
    value.__post_init__()
    for field in ("prepublication_ref", "installation_ref", "target_ref",
                  "policy_ref", "policy_version", "admin_key_ref", "version"):
        _check_bounded_ref(getattr(value, field), limits.max_ref_bytes)
    _check_bounded_ref(value.nv_profile.maintenance_p256_ref, limits.max_ref_bytes)
    _check_nv_public(value.nv_profile, limits)
    span_ns = _utc6_span_ns(value.valid_not_before_utc6, value.valid_not_after_utc6)
    if type(resource.max_validity_span_ns) is not int or isinstance(resource.max_validity_span_ns, bool):
        _fail()
    if span_ns <= 0 or span_ns > resource.max_validity_span_ns:
        _fail()
    if value.installation_ref != resource.installation_ref:
        _fail()
    if value.target_ref != resource.target_ref:
        _fail()


def _doc_payload(value: BootstrapPrepublication) -> dict[str, Any]:
    return {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "prepublication_ref": value.prepublication_ref,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "policy_ref": value.policy_ref,
        "policy_version": value.policy_version,
        "admin_key_ref": value.admin_key_ref,
        "admin_public_key_hex": value.admin_public_key_hex,
        "admin_key_pin": value.admin_key_pin,
        "domain": value.domain,
        "version": value.version,
        "nv_index": value.nv_profile.nv_index,
        "nv_attributes": value.nv_profile.nv_attributes,
        "nv_name_alg": value.nv_profile.nv_name_alg,
        "nv_data_size": value.nv_profile.nv_data_size,
        "nv_authpolicy_hex": value.nv_profile.nv_authpolicy_hex,
        "nv_name_hex": value.nv_profile.nv_name_hex,
        "maintenance_p256_ref": value.nv_profile.maintenance_p256_ref,
        "valid_not_before_utc6": value.valid_not_before_utc6,
        "valid_not_after_utc6": value.valid_not_after_utc6,
    }


def _canon(payload: dict[str, Any], limits: PayloadLimits) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPrepublicationContractError(_MSG) from None
    if len(raw) > limits.max_json_bytes:
        _fail()
    return text


def encode_bootstrap_prepublication(
    value: BootstrapPrepublication,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> str:
    _check_bounded_form(value, limits, resource)
    return _canon(_doc_payload(value), limits)


def _parse_int(token: str) -> int:
    if token[:1] == "-":
        _fail()
    if len(token) > 10:
        _fail()
    try:
        return int(token, 10)
    except ValueError:
        _fail()


def _reject_float(token: str) -> NoReturn:
    raise BootstrapPrepublicationContractError(_MSG) from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapPrepublicationContractError(_MSG) from None


def _pairs_generic(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    for key in keys:
        if type(key) is not str:
            _fail()
    if len(set(keys)) != len(keys):
        _fail()
    return {key: item for key, item in pairs}


def _decode_json(text: Any, limits: PayloadLimits) -> dict[str, Any]:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError as error:
        raise BootstrapPrepublicationContractError(_MSG) from error
    if len(raw) > limits.max_json_bytes:
        _fail()
    try:
        data = json.loads(
            text,
            object_pairs_hook=_pairs_generic,
            parse_int=_parse_int,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except BootstrapPrepublicationContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    return data


def _build_document(data: dict[str, Any], limits: PayloadLimits, resource: BootstrapResourceProfile) -> BootstrapPrepublication:
    if type(data) is not dict or set(data) != set(FIELD_NAMES):
        _fail()
    for key in _WIRE_STR_FIELDS:
        if type(data[key]) is not str:
            _fail()
    for key in _WIRE_INT_FIELDS:
        if type(data[key]) is not int or isinstance(data[key], bool):
            _fail()
    try:
        nv = BootstrapNvProfile(
            nv_index=data["nv_index"],
            nv_attributes=data["nv_attributes"],
            nv_name_alg=data["nv_name_alg"],
            nv_data_size=data["nv_data_size"],
            nv_authpolicy_hex=data["nv_authpolicy_hex"],
            nv_name_hex=data["nv_name_hex"],
            maintenance_p256_ref=data["maintenance_p256_ref"],
        )
    except NvContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        value = BootstrapPrepublication(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            prepublication_ref=data["prepublication_ref"],
            installation_ref=data["installation_ref"],
            target_ref=data["target_ref"],
            policy_ref=data["policy_ref"],
            policy_version=data["policy_version"],
            admin_key_ref=data["admin_key_ref"],
            admin_public_key_hex=data["admin_public_key_hex"],
            admin_key_pin=data["admin_key_pin"],
            domain=data["domain"],
            version=data["version"],
            nv_profile=nv,
            valid_not_before_utc6=data["valid_not_before_utc6"],
            valid_not_after_utc6=data["valid_not_after_utc6"],
        )
    except BootstrapPrepublicationContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits, resource)
    return value


def decode_bootstrap_prepublication(
    text: Any,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> BootstrapPrepublication:
    _check_limits(limits)
    _check_resource_valid(resource, limits)
    return _build_document(_decode_json(text, limits), limits, resource)


def prepublication_signed_bytes(
    value: BootstrapPrepublication,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> bytes:
    canon = encode_bootstrap_prepublication(value, limits, resource)
    return PREFIX.encode("ascii") + b"\n" + canon.encode("utf-8")


def encode_bootstrap_prepublication_envelope(
    env: BootstrapPrepublicationEnvelope,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> str:
    _check_limits(limits)
    _check_resource_valid(resource, limits)
    if type(env) is not BootstrapPrepublicationEnvelope:
        _fail()
    env.__post_init__()
    encode_bootstrap_prepublication(env.document, limits, resource)
    payload = {"document": _doc_payload(env.document), "signature_b64": env.signature_b64}
    return _canon(payload, limits)


def decode_bootstrap_prepublication_envelope(
    text: Any,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> BootstrapPrepublicationEnvelope:
    _check_limits(limits)
    _check_resource_valid(resource, limits)
    data = _decode_json(text, limits)
    if set(data) != set(_ENVELOPE_NAMES):
        _fail()
    doc_data = data["document"]
    sig = data["signature_b64"]
    if type(doc_data) is not dict:
        _fail()
    if type(sig) is not str:
        _fail()
    doc = _build_document(doc_data, limits, resource)
    _check_sig_b64(sig)
    try:
        return BootstrapPrepublicationEnvelope(document=doc, signature_b64=sig)
    except BootstrapPrepublicationContractError:
        raise
    except TypeError:
        _fail()


def prepublication_envelope_binding(
    env: BootstrapPrepublicationEnvelope,
    limits: PayloadLimits,
    resource: BootstrapResourceProfile,
) -> ContentBinding:
    _check_limits(limits)
    text = encode_bootstrap_prepublication_envelope(env, limits, resource)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    _check_bounded_ref(env.document.prepublication_ref, limits.max_ref_bytes)
    _check_bounded_ref(env.document.schema_version, limits.max_ref_bytes)
    try:
        return ContentBinding(ref=env.document.prepublication_ref, version=env.document.schema_version, sha256=digest)
    except PgContractError:
        _fail()
