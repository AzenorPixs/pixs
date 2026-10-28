"""Profil public NV BootstrapNvProfile (sous-objet B-NV, sept champs).

Forme publique de configuration : sept valeurs strictes et canon trie
compact. Type et forme seulement : le champ Name n'est jamais une
identite ni une preuve TPM ; aucune relation materielle, aucune
autorite, aucune creation ni observation n'est fabriquee ici. Les
resolutions natives et la cible materielle (compatibilite 1.38 a
qualifier, sans minimum releve) restent hors document.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import PayloadLimits
elif __package__ in (None, ""):
    if "postgresql_contracts" in sys.builtin_module_names:
        from postgresql_contracts import PayloadLimits
    else:
        raise ImportError("bootstrap_nv_profile: unsupported package context")
else:
    raise ImportError("bootstrap_nv_profile: unsupported package context")

__all__ = [
    "BootstrapNvProfileContractError",
    "BootstrapNvProfile",
    "encode_bootstrap_nv_profile",
    "decode_bootstrap_nv_profile",
]

FIELD_NAMES = (
    "nv_index",
    "nv_attributes",
    "nv_name_alg",
    "nv_data_size",
    "nv_authpolicy_hex",
    "nv_name_hex",
    "maintenance_p256_ref",
)

_INT_FIELDS = frozenset(("nv_index", "nv_attributes", "nv_data_size"))

NV_INDEX_MIN = 0x01000000
NV_INDEX_MAX = 0x01FFFFFF
NV_ATTRIBUTES_MAX = 0xFFFFFFFF
NV_ATTRS_REQUIRED = 0x60040404
NV_ATTRS_FORBIDDEN = 0x1C000800
NV_NT_MASK = 0xF0
NV_NT_EXTEND = 0x40
NV_NAME_ALG = "SHA256"
NV_DATA_SIZE = 32

_HEX_LOWER = frozenset("0123456789abcdef")


class BootstrapNvProfileContractError(ValueError):
    pass


def _fail() -> None:
    raise BootstrapNvProfileContractError("bootstrap_nv_profile: invalid value") from None


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


def _check_uint32_strict(value: Any) -> None:
    if type(value) is not int:
        _fail()
    if value < 0 or value > NV_ATTRIBUTES_MAX:
        _fail()


def _check_nv_index(value: Any) -> None:
    _check_uint32_strict(value)
    if value < NV_INDEX_MIN or value > NV_INDEX_MAX:
        _fail()


def _check_nv_attributes(value: Any) -> None:
    _check_uint32_strict(value)
    if (value & NV_ATTRS_REQUIRED) != NV_ATTRS_REQUIRED:
        _fail()
    if (value & NV_ATTRS_FORBIDDEN) != 0:
        _fail()
    if (value & NV_NT_MASK) != NV_NT_EXTEND:
        _fail()


def _check_authpolicy_hex(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 64:
        _fail()
    for char in value:
        if char not in _HEX_LOWER:
            _fail()


def _check_name_hex(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 68:
        _fail()
    if value[:4] != "000b":
        _fail()
    for char in value[4:]:
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


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapNvProfile:
    nv_index: int
    nv_attributes: int
    nv_name_alg: str
    nv_data_size: int
    nv_authpolicy_hex: str
    nv_name_hex: str
    maintenance_p256_ref: str

    def __post_init__(self) -> None:
        _check_nv_index(self.nv_index)
        _check_nv_attributes(self.nv_attributes)
        if type(self.nv_name_alg) is not str or self.nv_name_alg != NV_NAME_ALG:
            _fail()
        if type(self.nv_data_size) is not int or self.nv_data_size != NV_DATA_SIZE:
            _fail()
        _check_authpolicy_hex(self.nv_authpolicy_hex)
        _check_name_hex(self.nv_name_hex)
        _check_strict_nonempty_text(self.maintenance_p256_ref)


def _check_bounded_form(value: BootstrapNvProfile, limits: PayloadLimits) -> None:
    if type(value) is not BootstrapNvProfile:
        _fail()
    _check_nv_index(value.nv_index)
    _check_nv_attributes(value.nv_attributes)
    if type(value.nv_name_alg) is not str or value.nv_name_alg != NV_NAME_ALG:
        _fail()
    if type(value.nv_data_size) is not int or value.nv_data_size != NV_DATA_SIZE:
        _fail()
    _check_authpolicy_hex(value.nv_authpolicy_hex)
    _check_name_hex(value.nv_name_hex)
    _check_strict_nonempty_text(value.maintenance_p256_ref)
    _check_bounded_ref(value.maintenance_p256_ref, limits.max_ref_bytes)


def encode_bootstrap_nv_profile(value: BootstrapNvProfile, limits: PayloadLimits) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits)
    payload = {
        "nv_index": value.nv_index,
        "nv_attributes": value.nv_attributes,
        "nv_name_alg": value.nv_name_alg,
        "nv_data_size": value.nv_data_size,
        "nv_authpolicy_hex": value.nv_authpolicy_hex,
        "nv_name_hex": value.nv_name_hex,
        "maintenance_p256_ref": value.maintenance_p256_ref,
    }
    try:
        text = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except BootstrapNvProfileContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapNvProfileContractError("bootstrap_nv_profile: invalid value") from None
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
    raise BootstrapNvProfileContractError("bootstrap_nv_profile: invalid value")


def _reject_constant(token: str) -> None:
    raise BootstrapNvProfileContractError("bootstrap_nv_profile: invalid value")


def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        _fail()
    if set(keys) != set(FIELD_NAMES):
        _fail()
    if len(pairs) != len(FIELD_NAMES):
        _fail()
    result: dict[str, Any] = {}
    for key, item in pairs:
        if type(key) is not str:
            _fail()
        if key in _INT_FIELDS:
            if type(item) is not int:
                _fail()
        elif type(item) is not str:
            _fail()
        result[key] = item
    return result


def decode_bootstrap_nv_profile(text: Any, limits: PayloadLimits) -> BootstrapNvProfile:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapNvProfileContractError("bootstrap_nv_profile: invalid value") from None
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
    except BootstrapNvProfileContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    try:
        value = BootstrapNvProfile(
            nv_index=data["nv_index"],
            nv_attributes=data["nv_attributes"],
            nv_name_alg=data["nv_name_alg"],
            nv_data_size=data["nv_data_size"],
            nv_authpolicy_hex=data["nv_authpolicy_hex"],
            nv_name_hex=data["nv_name_hex"],
            maintenance_p256_ref=data["maintenance_p256_ref"],
        )
    except BootstrapNvProfileContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits)
    return value
