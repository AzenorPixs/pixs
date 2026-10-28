"""Base publique BootstrapBase/v1 (huit champs).

Forme publique de configuration : huit valeurs strictes et canon trie
compact. Type et forme seulement : les liaisons sont coherentes de
forme, jamais des preuves d'origine protegee, de TPM ou de HMAC ;
aucun acteur, permission ou effet materiel n'est porte ici. La base
attendue est derivee de l'entree INIT, jamais observee. Les actes
materiels et la cible (compatibilite 1.38 a qualifier, sans minimum
releve) restent hors document.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from typing import Any

if __package__ == "pixs.pa_native":
    from .bootstrap_context import (
        BootstrapContextContractError,
        BootstrapTpmContext,
        bootstrap_context_binding,
        encode_bootstrap_context,
    )
    from .bootstrap_init_profile import (
        BootstrapInitProfile,
        BootstrapInitProfileContractError,
        bootstrap_expected_base_hex64,
        bootstrap_init_profile_binding,
        encode_bootstrap_init_profile,
    )
    from .postgresql_contracts import (
        ContentBinding,
        ContractError as PgContractError,
        PayloadLimits,
    )
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_init_profile" in sys.builtin_module_names
            and "bootstrap_context" in sys.builtin_module_names):
        from bootstrap_context import (
            BootstrapContextContractError,
            BootstrapTpmContext,
            bootstrap_context_binding,
            encode_bootstrap_context,
        )
        from bootstrap_init_profile import (
            BootstrapInitProfile,
            BootstrapInitProfileContractError,
            bootstrap_expected_base_hex64,
            bootstrap_init_profile_binding,
            encode_bootstrap_init_profile,
        )
        from postgresql_contracts import (
            ContentBinding,
            ContractError as PgContractError,
            PayloadLimits,
        )
    else:
        raise ImportError("bootstrap_base: unsupported package context")
else:
    raise ImportError("bootstrap_base: unsupported package context")

__all__ = [
    "BootstrapBaseContractError",
    "BootstrapNvCoordinates",
    "BootstrapBase",
    "encode_bootstrap_base",
    "decode_bootstrap_base",
    "bootstrap_base_binding",
    "derive_bootstrap_base",
]

OBJECT_TYPE = "pixs.agent.bootstrap_base/v1"
SCHEMA_VERSION = "1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "base_ref",
    "base_version",
    "tpm_context_binding",
    "nv_coordinates",
    "expected_base_hex64",
    "init_profile_binding",
)

_ROOT_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "base_ref",
    "base_version",
    "expected_base_hex64",
))

_ROOT_DICT_FIELDS = frozenset((
    "tpm_context_binding",
    "nv_coordinates",
    "init_profile_binding",
))

_BINDING_KEYS = frozenset(("ref", "version", "sha256"))

_COORDS_KEYS = frozenset(("nv_index", "nv_name_hex"))

NV_INDEX_MIN = 0x01000000
NV_INDEX_MAX = 0x01FFFFFF

_HEX_LOWER = frozenset("0123456789abcdef")


class BootstrapBaseContractError(ValueError):
    pass


def _fail() -> None:
    raise BootstrapBaseContractError("bootstrap_base: invalid value") from None


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


def _check_hex64(value: Any) -> None:
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


def _check_nv_index(value: Any) -> None:
    if type(value) is not int:
        _fail()
    if value < NV_INDEX_MIN or value > NV_INDEX_MAX:
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
class BootstrapNvCoordinates:
    nv_index: int
    nv_name_hex: str

    def __post_init__(self) -> None:
        _check_nv_index(self.nv_index)
        _check_name_hex(self.nv_name_hex)


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapBase:
    object_type: str
    schema_version: str
    base_ref: str
    base_version: str
    tpm_context_binding: ContentBinding
    nv_coordinates: BootstrapNvCoordinates
    expected_base_hex64: str
    init_profile_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_nonempty_text(self.base_ref)
        _check_strict_nonempty_text(self.base_version)
        _check_binding_shape(self.tpm_context_binding)
        if type(self.nv_coordinates) is not BootstrapNvCoordinates:
            _fail()
        _check_hex64(self.expected_base_hex64)
        _check_binding_shape(self.init_profile_binding)


def _check_bounded_form(value: BootstrapBase, limits: PayloadLimits) -> None:
    if type(value) is not BootstrapBase:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    _check_strict_nonempty_text(value.base_ref)
    _check_bounded_ref(value.base_ref, limits.max_ref_bytes)
    _check_strict_nonempty_text(value.base_version)
    _check_bounded_ref(value.base_version, limits.max_ref_bytes)
    _check_binding(value.tpm_context_binding, limits)
    if type(value.nv_coordinates) is not BootstrapNvCoordinates:
        _fail()
    _check_nv_index(value.nv_coordinates.nv_index)
    _check_name_hex(value.nv_coordinates.nv_name_hex)
    _check_hex64(value.expected_base_hex64)
    _check_binding(value.init_profile_binding, limits)


def _binding_payload(binding: ContentBinding) -> dict[str, str]:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def encode_bootstrap_base(value: BootstrapBase, limits: PayloadLimits) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits)
    payload = {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "base_ref": value.base_ref,
        "base_version": value.base_version,
        "tpm_context_binding": _binding_payload(value.tpm_context_binding),
        "nv_coordinates": {
            "nv_index": value.nv_coordinates.nv_index,
            "nv_name_hex": value.nv_coordinates.nv_name_hex,
        },
        "expected_base_hex64": value.expected_base_hex64,
        "init_profile_binding": _binding_payload(value.init_profile_binding),
    }
    try:
        text = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except BootstrapBaseContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapBaseContractError("bootstrap_base: invalid value") from None
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
    raise BootstrapBaseContractError("bootstrap_base: invalid value")


def _reject_constant(token: str) -> None:
    raise BootstrapBaseContractError("bootstrap_base: invalid value")


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
    if keyset == _COORDS_KEYS:
        result = {}
        for key, item in pairs:
            if type(key) is not str:
                _fail()
            if key == "nv_index":
                if type(item) is not int:
                    _fail()
            elif key == "nv_name_hex":
                if type(item) is not str:
                    _fail()
            else:
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


def _nested_coordinates(data: Any) -> BootstrapNvCoordinates:
    if type(data) is not dict:
        _fail()
    try:
        return BootstrapNvCoordinates(nv_index=data["nv_index"], nv_name_hex=data["nv_name_hex"])
    except BootstrapBaseContractError:
        raise
    except (TypeError, KeyError):
        _fail()


def decode_bootstrap_base(text: Any, limits: PayloadLimits) -> BootstrapBase:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapBaseContractError("bootstrap_base: invalid value") from None
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
    except BootstrapBaseContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    try:
        value = BootstrapBase(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            base_ref=data["base_ref"],
            base_version=data["base_version"],
            tpm_context_binding=_nested_binding(data["tpm_context_binding"]),
            nv_coordinates=_nested_coordinates(data["nv_coordinates"]),
            expected_base_hex64=data["expected_base_hex64"],
            init_profile_binding=_nested_binding(data["init_profile_binding"]),
        )
    except BootstrapBaseContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits)
    return value


def bootstrap_base_binding(value: BootstrapBase, limits: PayloadLimits) -> ContentBinding:
    _check_limits(limits)
    canon = encode_bootstrap_base(value, limits)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    return ContentBinding(
        ref=value.base_ref,
        version=value.base_version,
        sha256=digest,
    )


def derive_bootstrap_base(init_profile: Any, context: Any, *, base_ref: Any, base_version: Any, limits: Any) -> BootstrapBase:
    _check_limits(limits)
    if type(init_profile) is not BootstrapInitProfile:
        _fail()
    if type(context) is not BootstrapTpmContext:
        _fail()
    try:
        encode_bootstrap_init_profile(init_profile, limits)
    except BootstrapInitProfileContractError:
        _fail()
    try:
        encode_bootstrap_context(context, limits)
    except BootstrapContextContractError:
        _fail()
    if (init_profile.installation_ref != context.installation_ref
            or init_profile.target_ref != context.target_ref):
        _fail()
    try:
        context_binding = bootstrap_context_binding(context, limits)
    except BootstrapContextContractError:
        _fail()
    if init_profile.tpm_context_binding != context_binding:
        _fail()
    _check_strict_nonempty_text(base_ref)
    _check_bounded_ref(base_ref, limits.max_ref_bytes)
    _check_strict_nonempty_text(base_version)
    _check_bounded_ref(base_version, limits.max_ref_bytes)
    nv = init_profile.nv_profile
    coordinates = BootstrapNvCoordinates(nv_index=nv.nv_index, nv_name_hex=nv.nv_name_hex)
    try:
        expected = bootstrap_expected_base_hex64(init_profile, limits)
    except BootstrapInitProfileContractError:
        _fail()
    try:
        init_binding = bootstrap_init_profile_binding(init_profile, limits)
    except BootstrapInitProfileContractError:
        _fail()
    value = BootstrapBase(
        object_type=OBJECT_TYPE,
        schema_version=SCHEMA_VERSION,
        base_ref=base_ref,
        base_version=base_version,
        tpm_context_binding=context_binding,
        nv_coordinates=coordinates,
        expected_base_hex64=expected,
        init_profile_binding=init_binding,
    )
    encode_bootstrap_base(value, limits)
    return value
