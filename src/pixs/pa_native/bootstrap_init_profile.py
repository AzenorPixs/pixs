"""Profil public INIT BootstrapInitProfile/v1 (douze champs).

Forme publique de configuration : douze valeurs strictes et canon trie
compact. Type et forme seulement : les bindings sont des donnees
simples, jamais des resolutions ni des permissions ; la base attendue
est une attente calculee pure, jamais une observation ni une creation.
Aucun lien vers base, recette, plan futur, tete, publication ou
provenance, sans selecteur de repli. Les actes materiels et la cible
(compatibilite 1.38 a qualifier, sans minimum releve) restent hors
document.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from typing import Any

if __package__ == "pixs.pa_native":
    from .bootstrap_nv_profile import (
        FIELD_NAMES as NV_FIELD_NAMES,
        BootstrapNvProfile,
        BootstrapNvProfileContractError,
        decode_bootstrap_nv_profile,
        encode_bootstrap_nv_profile,
    )
    from .postgresql_contracts import (
        ContentBinding,
        ContractError as PgContractError,
        PayloadLimits,
    )
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_nv_profile" in sys.builtin_module_names):
        from bootstrap_nv_profile import (
            FIELD_NAMES as NV_FIELD_NAMES,
            BootstrapNvProfile,
            BootstrapNvProfileContractError,
            decode_bootstrap_nv_profile,
            encode_bootstrap_nv_profile,
        )
        from postgresql_contracts import (
            ContentBinding,
            ContractError as PgContractError,
            PayloadLimits,
        )
    else:
        raise ImportError("bootstrap_init_profile: unsupported package context")
else:
    raise ImportError("bootstrap_init_profile: unsupported package context")

__all__ = [
    "BootstrapInitProfileContractError",
    "BootstrapInitProfile",
    "encode_bootstrap_init_profile",
    "decode_bootstrap_init_profile",
    "bootstrap_init_profile_binding",
    "bootstrap_expected_base_hex64",
]

OBJECT_TYPE = "pixs.agent.bootstrap_init_profile/v1"
SCHEMA_VERSION = "1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "init_profile_ref",
    "init_profile_version",
    "installation_ref",
    "target_ref",
    "tpm_context_binding",
    "nv_profile",
    "initialization_input_hex64",
    "authority_binding",
    "procedure_binding",
    "executor_binding",
)

_ROOT_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "init_profile_ref",
    "init_profile_version",
    "installation_ref",
    "target_ref",
    "initialization_input_hex64",
))

_ROOT_DICT_FIELDS = frozenset((
    "tpm_context_binding",
    "nv_profile",
    "authority_binding",
    "procedure_binding",
    "executor_binding",
))

_NV_INT_FIELDS = frozenset(("nv_index", "nv_attributes", "nv_data_size"))

_BINDING_KEYS = frozenset(("ref", "version", "sha256"))

_HEX_LOWER = frozenset("0123456789abcdef")


class BootstrapInitProfileContractError(ValueError):
    pass


def _fail() -> None:
    raise BootstrapInitProfileContractError("bootstrap_init_profile: invalid value") from None


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


def _check_input_hex64(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 64:
        _fail()
    for char in value:
        if char not in _HEX_LOWER:
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
    size = len(value.encode("utf-8"))
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


def _check_binding_shape(value: Any) -> None:
    if type(value) is not ContentBinding:
        _fail()
    try:
        ContentBinding(ref=value.ref, version=value.version, sha256=value.sha256)
    except PgContractError:
        _fail()


def _check_binding(value: Any, limits: PayloadLimits) -> None:
    _check_binding_shape(value)
    _check_strict_nonempty_text(value.ref)
    _check_strict_nonempty_text(value.version)
    _check_bounded_ref(value.ref, limits.max_ref_bytes)
    _check_bounded_ref(value.version, limits.max_ref_bytes)


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapInitProfile:
    object_type: str
    schema_version: str
    init_profile_ref: str
    init_profile_version: str
    installation_ref: str
    target_ref: str
    tpm_context_binding: ContentBinding
    nv_profile: BootstrapNvProfile
    initialization_input_hex64: str
    authority_binding: ContentBinding
    procedure_binding: ContentBinding
    executor_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_nonempty_text(self.init_profile_ref)
        _check_strict_nonempty_text(self.init_profile_version)
        _check_strict_nonempty_text(self.installation_ref)
        _check_strict_nonempty_text(self.target_ref)
        _check_no_wildcard(self.installation_ref)
        _check_no_wildcard(self.target_ref)
        _check_binding_shape(self.tpm_context_binding)
        _check_binding_shape(self.authority_binding)
        _check_binding_shape(self.procedure_binding)
        _check_binding_shape(self.executor_binding)
        if type(self.nv_profile) is not BootstrapNvProfile:
            _fail()
        _check_input_hex64(self.initialization_input_hex64)


def _check_bounded_form(value: BootstrapInitProfile, limits: PayloadLimits) -> None:
    if type(value) is not BootstrapInitProfile:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    _check_strict_nonempty_text(value.init_profile_ref)
    _check_bounded_ref(value.init_profile_ref, limits.max_ref_bytes)
    _check_strict_nonempty_text(value.init_profile_version)
    _check_bounded_ref(value.init_profile_version, limits.max_ref_bytes)
    _check_strict_nonempty_text(value.installation_ref)
    _check_no_wildcard(value.installation_ref)
    _check_bounded_ref(value.installation_ref, limits.max_ref_bytes)
    _check_strict_nonempty_text(value.target_ref)
    _check_no_wildcard(value.target_ref)
    _check_bounded_ref(value.target_ref, limits.max_ref_bytes)
    _check_binding(value.tpm_context_binding, limits)
    _check_binding(value.authority_binding, limits)
    _check_binding(value.procedure_binding, limits)
    _check_binding(value.executor_binding, limits)
    if type(value.nv_profile) is not BootstrapNvProfile:
        _fail()
    try:
        encode_bootstrap_nv_profile(value.nv_profile, limits)
    except BootstrapNvProfileContractError:
        _fail()
    _check_input_hex64(value.initialization_input_hex64)


def _binding_payload(binding: ContentBinding) -> dict[str, str]:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def encode_bootstrap_init_profile(value: BootstrapInitProfile, limits: PayloadLimits) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits)
    payload = {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "init_profile_ref": value.init_profile_ref,
        "init_profile_version": value.init_profile_version,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "tpm_context_binding": _binding_payload(value.tpm_context_binding),
        "nv_profile": {
            "nv_index": value.nv_profile.nv_index,
            "nv_attributes": value.nv_profile.nv_attributes,
            "nv_name_alg": value.nv_profile.nv_name_alg,
            "nv_data_size": value.nv_profile.nv_data_size,
            "nv_authpolicy_hex": value.nv_profile.nv_authpolicy_hex,
            "nv_name_hex": value.nv_profile.nv_name_hex,
            "maintenance_p256_ref": value.nv_profile.maintenance_p256_ref,
        },
        "initialization_input_hex64": value.initialization_input_hex64,
        "authority_binding": _binding_payload(value.authority_binding),
        "procedure_binding": _binding_payload(value.procedure_binding),
        "executor_binding": _binding_payload(value.executor_binding),
    }
    try:
        text = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except BootstrapInitProfileContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapInitProfileContractError("bootstrap_init_profile: invalid value") from None
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


def _reject_float(token: str) -> None:
    raise BootstrapInitProfileContractError("bootstrap_init_profile: invalid value")


def _reject_constant(token: str) -> None:
    raise BootstrapInitProfileContractError("bootstrap_init_profile: invalid value")


def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        _fail()
    keyset = set(keys)
    if keyset == _BINDING_KEYS:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if type(item) is not str:
                _fail()
            result[key] = item
        return result
    if keyset == set(NV_FIELD_NAMES):
        result = {}
        for key, item in pairs:
            if type(key) is not str:
                _fail()
            if key in _NV_INT_FIELDS:
                if type(item) is not int:
                    _fail()
            elif type(item) is not str:
                _fail()
            result[key] = item
        return result
    if keyset == set(FIELD_NAMES):
        result = {}
        for key, item in pairs:
            if type(key) is not str:
                _fail()
            if key in _ROOT_STR_FIELDS:
                if type(item) is not str:
                    _fail()
            elif key in _ROOT_DICT_FIELDS:
                if type(item) is not dict:
                    _fail()
            else:
                _fail()
            result[key] = item
        return result
    _fail()


def _nested_binding(data: Any) -> ContentBinding:
    if type(data) is not dict:
        _fail()
    try:
        return ContentBinding(ref=data["ref"], version=data["version"], sha256=data["sha256"])
    except PgContractError:
        _fail()


def _nested_nv_profile(data: Any, limits: PayloadLimits) -> BootstrapNvProfile:
    if type(data) is not dict:
        _fail()
    try:
        sub = json.dumps(
            data,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        return decode_bootstrap_nv_profile(sub, limits)
    except BootstrapNvProfileContractError:
        _fail()


def decode_bootstrap_init_profile(text: Any, limits: PayloadLimits) -> BootstrapInitProfile:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapInitProfileContractError("bootstrap_init_profile: invalid value") from None
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
    except BootstrapInitProfileContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    try:
        value = BootstrapInitProfile(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            init_profile_ref=data["init_profile_ref"],
            init_profile_version=data["init_profile_version"],
            installation_ref=data["installation_ref"],
            target_ref=data["target_ref"],
            tpm_context_binding=_nested_binding(data["tpm_context_binding"]),
            nv_profile=_nested_nv_profile(data["nv_profile"], limits),
            initialization_input_hex64=data["initialization_input_hex64"],
            authority_binding=_nested_binding(data["authority_binding"]),
            procedure_binding=_nested_binding(data["procedure_binding"]),
            executor_binding=_nested_binding(data["executor_binding"]),
        )
    except BootstrapInitProfileContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits)
    return value


def bootstrap_init_profile_binding(value: BootstrapInitProfile, limits: PayloadLimits) -> ContentBinding:
    _check_limits(limits)
    canon = encode_bootstrap_init_profile(value, limits)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    return ContentBinding(
        ref=value.init_profile_ref,
        version=value.init_profile_version,
        sha256=digest,
    )


def bootstrap_expected_base_hex64(value: BootstrapInitProfile, limits: PayloadLimits) -> str:
    _check_limits(limits)
    encode_bootstrap_init_profile(value, limits)
    raw_input = bytes.fromhex(value.initialization_input_hex64)
    return hashlib.sha256(b"\x00" * 32 + raw_input).hexdigest()
