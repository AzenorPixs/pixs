"""Profil public BootstrapPolicy/v1 (14 champs).

FORME pure adoptee dans le lot, code NON QUALIFIE : sans admission,
acte, preuve materielle, TPM, PG, PZT ni qualification native ou
d origine. 14 valeurs strictes, canon trie compact, liaisons de
donnees. PayloadLimits externe explicite borne le chargement du
document et de ses references ; Resource24 reel explicite borne la
duree de validite propre (0 < span_ns <= max_validity_span_ns,
INCLUSIVE) et recoupe la liaison de donnees, sans authentifier son
origine. Sans clock/timeprovider, sans deadline JSON, sans
cle/signature.
"""

from __future__ import annotations

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
    from .bootstrap_resource_profile import bootstrap_resource_profile_binding as res_binding_public
elif __package__ in (None, ""):
    if (
        "postgresql_contracts" in sys.builtin_module_names
        and "bootstrap_nv_profile" in sys.builtin_module_names
        and "bootstrap_resource_profile" in sys.builtin_module_names
    ):
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from bootstrap_nv_profile import BootstrapNvProfile
        from bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
        from bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_public
        from bootstrap_resource_profile import BootstrapResourceProfile
        from bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
        from bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
        from bootstrap_resource_profile import bootstrap_resource_profile_binding as res_binding_public
    else:
        raise ImportError("bootstrap_policy_profile: unsupported package context")
else:
    raise ImportError("bootstrap_policy_profile: unsupported package context")

__all__ = [
    "BootstrapPolicyProfileContractError",
    "BootstrapPolicyProfile",
    "encode_bootstrap_policy_profile",
    "decode_bootstrap_policy_profile",
    "bootstrap_policy_profile_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_policy/v1"
SCHEMA_VERSION = "1.0.0"
DOMAIN = "PA_ADMIN_INITIAL"
ADMISSION_SCOPE = "CONFIGURATION_ONLY"
WITHDRAWAL_RIGHT = "WITHDRAW_PA_INITIAL"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "policy_ref",
    "policy_version",
    "domain",
    "admission_scope",
    "withdrawal_right",
    "nv_profile",
    "installation_ref",
    "target_ref",
    "tpm_context_binding",
    "resource_profile_binding",
    "valid_not_before_utc6",
    "valid_not_after_utc6",
)

_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "policy_ref",
    "policy_version",
    "domain",
    "admission_scope",
    "withdrawal_right",
    "installation_ref",
    "target_ref",
    "valid_not_before_utc6",
    "valid_not_after_utc6",
))

_BINDING_FIELDS = (
    "tpm_context_binding",
    "resource_profile_binding",
)

NV_FIELD_NAMES = (
    "nv_index",
    "nv_attributes",
    "nv_name_alg",
    "nv_data_size",
    "nv_authpolicy_hex",
    "nv_name_hex",
    "maintenance_p256_ref",
)

NV_INT_FIELDS = frozenset(("nv_index", "nv_attributes", "nv_data_size"))

BINDING_NAMES = ("ref", "version", "sha256")


class BootstrapPolicyProfileContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None


def _is_forbidden_codepoint(code: int) -> bool:
    if code < 0x20:
        return True
    if code == 0x7F:
        return True
    if 0xD800 <= code <= 0xDFFF:
        return True
    return False


def _check_strict_nonempty_text(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if value == "":
        _fail()
    for char in value:
        if _is_forbidden_codepoint(ord(char)):
            _fail()


def _check_no_wildcard(value: str) -> None:
    if "*" in value:
        _fail()


def _check_limits(limits: Any) -> None:
    if type(limits) is not PayloadLimits:
        _fail()
    if type(limits.max_json_bytes) is not int:
        _fail()
    if type(limits.max_ref_bytes) is not int:
        _fail()
    if type(limits.max_observation_refs) is not int:
        _fail()
    if limits.max_json_bytes <= 0:
        _fail()
    if limits.max_ref_bytes <= 0:
        _fail()
    if limits.max_observation_refs <= 0:
        _fail()


def _check_bounded_ref(value: str, ceiling: int) -> None:
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


def _check_utc6_shape(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 27:
        _fail()
    if value[4] != "-" or value[7] != "-" or value[10] != "T":
        _fail()
    if value[13] != ":" or value[16] != ":" or value[19] != "." or value[26] != "Z":
        _fail()
    for idx in (0, 1, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 22, 23, 24, 25):
        ch = value[idx]
        if ch < "0" or ch > "9":
            _fail()


def _parse_utc6(value: str) -> datetime:
    _check_utc6_shape(value)
    try:
        year = int(value[0:4], 10)
        month = int(value[5:7], 10)
        day = int(value[8:10], 10)
        hour = int(value[11:13], 10)
        minute = int(value[14:16], 10)
        second = int(value[17:19], 10)
        micro = int(value[20:26], 10)
    except ValueError:
        _fail()
    if year <= 0 or year > 9999:
        _fail()
    try:
        return datetime(year, month, day, hour, minute, second, micro)
    except ValueError:
        _fail()
    raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None


def _utc6_span_ns(before: str, after: str) -> int:
    dt_before = _parse_utc6(before)
    dt_after = _parse_utc6(after)
    if dt_after <= dt_before:
        _fail()
    delta = dt_after - dt_before
    return (delta.days * 86400 + delta.seconds) * 1000000000 + delta.microseconds * 1000


def _check_binding_intrinsic(binding: Any) -> None:
    if type(binding) is not ContentBinding:
        _fail()
    try:
        ContentBinding(ref=binding.ref, version=binding.version, sha256=binding.sha256)
    except PgContractError:
        _fail()
    except (TypeError, ValueError):
        _fail()


def _check_binding_shape(binding: Any, limits: PayloadLimits) -> None:
    _check_binding_intrinsic(binding)
    _check_bounded_ref(binding.ref, limits.max_ref_bytes)
    _check_bounded_ref(binding.version, limits.max_ref_bytes)


def _check_resource_valid(resource_profile: Any, limits: PayloadLimits) -> None:
    if type(resource_profile) is not BootstrapResourceProfile:
        _fail()
    try:
        res_encode_public(resource_profile, limits)
    except ResContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


def _check_nv_valid(nv_profile: Any, limits: PayloadLimits) -> None:
    if type(nv_profile) is not BootstrapNvProfile:
        _fail()
    try:
        nv_encode_public(nv_profile, limits)
    except NvContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPolicyProfile:
    object_type: str
    schema_version: str
    policy_ref: str
    policy_version: str
    domain: str
    admission_scope: str
    withdrawal_right: str
    nv_profile: BootstrapNvProfile
    installation_ref: str
    target_ref: str
    tpm_context_binding: ContentBinding
    resource_profile_binding: ContentBinding
    valid_not_before_utc6: str
    valid_not_after_utc6: str

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_nonempty_text(self.policy_ref)
        _check_strict_nonempty_text(self.policy_version)
        if type(self.domain) is not str or self.domain != DOMAIN:
            _fail()
        if type(self.admission_scope) is not str or self.admission_scope != ADMISSION_SCOPE:
            _fail()
        if type(self.withdrawal_right) is not str or self.withdrawal_right != WITHDRAWAL_RIGHT:
            _fail()
        if type(self.nv_profile) is not BootstrapNvProfile:
            _fail()
        _check_strict_nonempty_text(self.installation_ref)
        _check_strict_nonempty_text(self.target_ref)
        _check_no_wildcard(self.installation_ref)
        _check_no_wildcard(self.target_ref)
        _check_binding_intrinsic(self.tpm_context_binding)
        _check_binding_intrinsic(self.resource_profile_binding)
        _check_utc6_shape(self.valid_not_before_utc6)
        _check_utc6_shape(self.valid_not_after_utc6)
        dt_before = _parse_utc6(self.valid_not_before_utc6)
        dt_after = _parse_utc6(self.valid_not_after_utc6)
        if dt_after <= dt_before:
            _fail()


def _check_bounded_form(
    value: BootstrapPolicyProfile,
    limits: PayloadLimits,
    resource_profile: BootstrapResourceProfile,
) -> None:
    _check_limits(limits)
    _check_resource_valid(resource_profile, limits)
    if type(value) is not BootstrapPolicyProfile:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    _check_strict_nonempty_text(value.policy_ref)
    _check_strict_nonempty_text(value.policy_version)
    _check_bounded_ref(value.policy_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.policy_version, limits.max_ref_bytes)
    if type(value.domain) is not str or value.domain != DOMAIN:
        _fail()
    if type(value.admission_scope) is not str or value.admission_scope != ADMISSION_SCOPE:
        _fail()
    if type(value.withdrawal_right) is not str or value.withdrawal_right != WITHDRAWAL_RIGHT:
        _fail()
    _check_nv_valid(value.nv_profile, limits)
    _check_strict_nonempty_text(value.installation_ref)
    _check_strict_nonempty_text(value.target_ref)
    _check_bounded_ref(value.installation_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.target_ref, limits.max_ref_bytes)
    _check_no_wildcard(value.installation_ref)
    _check_no_wildcard(value.target_ref)
    _check_binding_shape(value.tpm_context_binding, limits)
    _check_binding_shape(value.resource_profile_binding, limits)
    span_ns = _utc6_span_ns(value.valid_not_before_utc6, value.valid_not_after_utc6)
    if type(resource_profile.max_validity_span_ns) is not int:
        _fail()
    if span_ns <= 0:
        _fail()
    if span_ns > resource_profile.max_validity_span_ns:
        _fail()
    if value.installation_ref != resource_profile.installation_ref:
        _fail()
    if value.target_ref != resource_profile.target_ref:
        _fail()
    try:
        expected = res_binding_public(resource_profile, limits)
    except ResContractError:
        _fail()
    except (TypeError, ValueError):
        _fail()
    if type(expected) is not ContentBinding:
        _fail()
    if value.resource_profile_binding != expected:
        _fail()


def _nv_to_payload(nv: BootstrapNvProfile) -> dict[str, Any]:
    return {
        "nv_index": nv.nv_index,
        "nv_attributes": nv.nv_attributes,
        "nv_name_alg": nv.nv_name_alg,
        "nv_data_size": nv.nv_data_size,
        "nv_authpolicy_hex": nv.nv_authpolicy_hex,
        "nv_name_hex": nv.nv_name_hex,
        "maintenance_p256_ref": nv.maintenance_p256_ref,
    }


def _binding_to_payload(binding: ContentBinding) -> dict[str, Any]:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def encode_bootstrap_policy_profile(
    value: BootstrapPolicyProfile,
    limits: PayloadLimits,
    resource_profile: BootstrapResourceProfile,
) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits, resource_profile)
    payload = {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "policy_ref": value.policy_ref,
        "policy_version": value.policy_version,
        "domain": value.domain,
        "admission_scope": value.admission_scope,
        "withdrawal_right": value.withdrawal_right,
        "nv_profile": _nv_to_payload(value.nv_profile),
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "tpm_context_binding": _binding_to_payload(value.tpm_context_binding),
        "resource_profile_binding": _binding_to_payload(value.resource_profile_binding),
        "valid_not_before_utc6": value.valid_not_before_utc6,
        "valid_not_after_utc6": value.valid_not_after_utc6,
    }
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except BootstrapPolicyProfileContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


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
    raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None


def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        _fail()
    keyset = set(keys)
    if keyset == set(FIELD_NAMES):
        if len(pairs) != 14:
            _fail()
        result: dict[str, Any] = {}
        for key, item in pairs:
            if type(key) is not str:
                _fail()
            if key in _STR_FIELDS:
                if type(item) is not str:
                    _fail()
            elif key == "nv_profile":
                if type(item) is not dict:
                    _fail()
            elif key in _BINDING_FIELDS:
                if type(item) is not dict:
                    _fail()
            else:
                _fail()
            result[key] = item
        return result
    if keyset == set(NV_FIELD_NAMES):
        if len(pairs) != 7:
            _fail()
        result = {}
        for key, item in pairs:
            if type(key) is not str:
                _fail()
            if key in NV_INT_FIELDS:
                if type(item) is not int:
                    _fail()
            else:
                if type(item) is not str:
                    _fail()
            result[key] = item
        return result
    if keyset == set(BINDING_NAMES):
        if len(pairs) != 3:
            _fail()
        result = {}
        for key, item in pairs:
            if type(key) is not str:
                _fail()
            if type(item) is not str:
                _fail()
            result[key] = item
        return result
    _fail()


def decode_bootstrap_policy_profile(
    text: Any,
    limits: PayloadLimits,
    resource_profile: BootstrapResourceProfile,
) -> BootstrapPolicyProfile:
    _check_limits(limits)
    _check_resource_valid(resource_profile, limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPolicyProfileContractError("bootstrap_policy_profile: invalid value") from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    try:
        data = json.loads(
            text,
            object_pairs_hook=_pairs_hook,
            parse_int=_parse_int,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except BootstrapPolicyProfileContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    try:
        nv_dict = data["nv_profile"]
        tpm_dict = data["tpm_context_binding"]
        res_dict = data["resource_profile_binding"]
    except KeyError:
        _fail()
    try:
        nv = BootstrapNvProfile(
            nv_index=nv_dict["nv_index"],
            nv_attributes=nv_dict["nv_attributes"],
            nv_name_alg=nv_dict["nv_name_alg"],
            nv_data_size=nv_dict["nv_data_size"],
            nv_authpolicy_hex=nv_dict["nv_authpolicy_hex"],
            nv_name_hex=nv_dict["nv_name_hex"],
            maintenance_p256_ref=nv_dict["maintenance_p256_ref"],
        )
    except NvContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        tpm_binding = ContentBinding(ref=tpm_dict["ref"], version=tpm_dict["version"], sha256=tpm_dict["sha256"])
    except PgContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        res_binding = ContentBinding(ref=res_dict["ref"], version=res_dict["version"], sha256=res_dict["sha256"])
    except PgContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        value = BootstrapPolicyProfile(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            policy_ref=data["policy_ref"],
            policy_version=data["policy_version"],
            domain=data["domain"],
            admission_scope=data["admission_scope"],
            withdrawal_right=data["withdrawal_right"],
            nv_profile=nv,
            installation_ref=data["installation_ref"],
            target_ref=data["target_ref"],
            tpm_context_binding=tpm_binding,
            resource_profile_binding=res_binding,
            valid_not_before_utc6=data["valid_not_before_utc6"],
            valid_not_after_utc6=data["valid_not_after_utc6"],
        )
    except BootstrapPolicyProfileContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits, resource_profile)
    return value


def bootstrap_policy_profile_binding(
    value: BootstrapPolicyProfile,
    limits: PayloadLimits,
    resource_profile: BootstrapResourceProfile,
) -> ContentBinding:
    _check_limits(limits)
    _check_bounded_form(value, limits, resource_profile)
    canon = encode_bootstrap_policy_profile(value, limits, resource_profile)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    try:
        return ContentBinding(ref=value.policy_ref, version=value.policy_version, sha256=digest)
    except PgContractError:
        _fail()
