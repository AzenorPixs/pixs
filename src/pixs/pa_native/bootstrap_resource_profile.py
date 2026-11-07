"""Profil public BootstrapResourceProfile/v1 (24 champs).

Lot Resource24 ADOPTE par le developpeur ; code de forme encore a
qualifier, sans admission, acte, preuve materielle, TPM, PG, PZT ni
qualification native. Forme publique de configuration : 24 valeurs
strictes, canon trie compact, liaison de forme. PayloadLimits externe
explicite borne le chargement du document et de ses references ; les
plafonds contenus dans le candidat ne donnent AUCUNE autorite pour sa
propre allocation ou son propre chargement. Sans deadline_ns JSON,
sans CLOCK_MONOTONIC, sans effet actuel. sizeof(size_t) observe via
struct.calcsize("N") pour SIZE_MAX et max_record <= SIZE_MAX - 65 ;
max_bytes n est PAS borne par SIZE_MAX.
"""

from __future__ import annotations

import hashlib
import json
import struct
import sys
from dataclasses import dataclass
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
elif __package__ in (None, ""):
    if "postgresql_contracts" in sys.builtin_module_names:
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
    else:
        raise ImportError("bootstrap_resource_profile: unsupported package context")
else:
    raise ImportError("bootstrap_resource_profile: unsupported package context")

__all__ = [
    "BootstrapResourceProfileContractError",
    "BootstrapResourceProfile",
    "encode_bootstrap_resource_profile",
    "decode_bootstrap_resource_profile",
    "bootstrap_resource_profile_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_resource_profile/v1"
SCHEMA_VERSION = "1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "profile_ref",
    "profile_version",
    "installation_ref",
    "target_ref",
    "registry_ref",
    "registry_generation_ref",
    "epoch",
    "first_sequence",
    "payload_max_json_bytes",
    "payload_max_ref_bytes",
    "payload_max_observation_refs",
    "max_epoch",
    "max_sequence",
    "max_correlation_refs",
    "max_causation_refs",
    "max_bytes",
    "max_record",
    "max_records",
    "max_validity_span_ns",
    "max_command_bytes",
    "max_response_bytes",
    "operation_budget_ns",
)

_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "profile_ref",
    "profile_version",
    "installation_ref",
    "target_ref",
    "registry_ref",
    "registry_generation_ref",
))

_REF_FIELDS = (
    "profile_ref",
    "profile_version",
    "installation_ref",
    "target_ref",
    "registry_ref",
    "registry_generation_ref",
)

_INT_FIELDS = frozenset((
    "epoch",
    "first_sequence",
    "payload_max_json_bytes",
    "payload_max_ref_bytes",
    "payload_max_observation_refs",
    "max_epoch",
    "max_sequence",
    "max_correlation_refs",
    "max_causation_refs",
    "max_bytes",
    "max_record",
    "max_records",
    "max_validity_span_ns",
    "max_command_bytes",
    "max_response_bytes",
    "operation_budget_ns",
))

_UINT32_MAX = 4294967295
_UINT64_MAX = 18446744073709551615
_INT63_MAX = 9223372036854775807


class BootstrapResourceProfileContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapResourceProfileContractError("bootstrap_resource_profile: invalid value") from None


def _size_max() -> int:
    return (1 << (struct.calcsize("N") * 8)) - 1


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
        _fail()
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


def _check_range(value: Any, lo: int, hi: int) -> None:
    if type(value) is not int:
        _fail()
    if value < lo or value > hi:
        _fail()


def _check_positive(value: Any) -> None:
    if type(value) is not int:
        _fail()
    if value <= 0:
        _fail()


def _check_form(value: Any, maximum: int | None) -> None:
    if type(value) is not BootstrapResourceProfile:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    for name in _REF_FIELDS:
        item = getattr(value, name)
        _check_strict_nonempty_text(item)
        if maximum is not None:
            _check_bounded_ref(item, maximum)
    _check_no_wildcard(value.installation_ref)
    _check_no_wildcard(value.target_ref)
    _check_range(value.epoch, 0, _UINT64_MAX)
    _check_range(value.first_sequence, 0, _UINT64_MAX)
    _check_range(value.payload_max_json_bytes, 1, _UINT32_MAX)
    _check_range(value.payload_max_ref_bytes, 1, _UINT32_MAX)
    _check_positive(value.payload_max_observation_refs)
    _check_range(value.max_epoch, 0, _UINT64_MAX)
    _check_range(value.max_sequence, 0, _UINT64_MAX)
    _check_range(value.max_correlation_refs, 1, _UINT32_MAX)
    _check_range(value.max_causation_refs, 1, _UINT32_MAX)
    _check_range(value.max_bytes, 59, _INT63_MAX)
    _check_range(value.max_record, 1, _UINT32_MAX)
    _check_range(value.max_records, 1, _UINT32_MAX)
    _check_range(value.max_validity_span_ns, 1, _UINT64_MAX)
    _check_range(value.max_command_bytes, 10, _UINT32_MAX)
    _check_range(value.max_response_bytes, 10, _UINT32_MAX)
    _check_range(value.operation_budget_ns, 1, _UINT64_MAX)
    if value.epoch > value.max_epoch:
        _fail()
    if value.first_sequence > value.max_sequence:
        _fail()
    if value.max_record + 58 > value.max_bytes:
        _fail()
    if value.max_record > _size_max() - 65:
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapResourceProfile:
    object_type: str
    schema_version: str
    profile_ref: str
    profile_version: str
    installation_ref: str
    target_ref: str
    registry_ref: str
    registry_generation_ref: str
    epoch: int
    first_sequence: int
    payload_max_json_bytes: int
    payload_max_ref_bytes: int
    payload_max_observation_refs: int
    max_epoch: int
    max_sequence: int
    max_correlation_refs: int
    max_causation_refs: int
    max_bytes: int
    max_record: int
    max_records: int
    max_validity_span_ns: int
    max_command_bytes: int
    max_response_bytes: int
    operation_budget_ns: int

    def __post_init__(self) -> None:
        _check_form(self, None)


def _check_bounded_form(value: BootstrapResourceProfile, limits: PayloadLimits) -> None:
    _check_limits(limits)
    _check_form(value, limits.max_ref_bytes)


def encode_bootstrap_resource_profile(value: BootstrapResourceProfile, limits: PayloadLimits) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits)
    payload = {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "profile_ref": value.profile_ref,
        "profile_version": value.profile_version,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "registry_ref": value.registry_ref,
        "registry_generation_ref": value.registry_generation_ref,
        "epoch": value.epoch,
        "first_sequence": value.first_sequence,
        "payload_max_json_bytes": value.payload_max_json_bytes,
        "payload_max_ref_bytes": value.payload_max_ref_bytes,
        "payload_max_observation_refs": value.payload_max_observation_refs,
        "max_epoch": value.max_epoch,
        "max_sequence": value.max_sequence,
        "max_correlation_refs": value.max_correlation_refs,
        "max_causation_refs": value.max_causation_refs,
        "max_bytes": value.max_bytes,
        "max_record": value.max_record,
        "max_records": value.max_records,
        "max_validity_span_ns": value.max_validity_span_ns,
        "max_command_bytes": value.max_command_bytes,
        "max_response_bytes": value.max_response_bytes,
        "operation_budget_ns": value.operation_budget_ns,
    }
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except BootstrapResourceProfileContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapResourceProfileContractError("bootstrap_resource_profile: invalid value") from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def _parse_int(token: str) -> int:
    if token[:1] == "-":
        _fail()
    try:
        return int(token, 10)
    except ValueError:
        _fail()


def _reject_float(token: str) -> NoReturn:
    raise BootstrapResourceProfileContractError("bootstrap_resource_profile: invalid value") from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapResourceProfileContractError("bootstrap_resource_profile: invalid value") from None


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
        if key in _STR_FIELDS:
            if type(item) is not str:
                _fail()
        elif key in _INT_FIELDS:
            if type(item) is not int:
                _fail()
        else:
            _fail()
        result[key] = item
    return result


def decode_bootstrap_resource_profile(text: Any, limits: PayloadLimits) -> BootstrapResourceProfile:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapResourceProfileContractError("bootstrap_resource_profile: invalid value") from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    try:
        data = json.loads(text, object_pairs_hook=_pairs_hook, parse_int=_parse_int, parse_float=_reject_float, parse_constant=_reject_constant)
    except BootstrapResourceProfileContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    try:
        value = BootstrapResourceProfile(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            profile_ref=data["profile_ref"],
            profile_version=data["profile_version"],
            installation_ref=data["installation_ref"],
            target_ref=data["target_ref"],
            registry_ref=data["registry_ref"],
            registry_generation_ref=data["registry_generation_ref"],
            epoch=data["epoch"],
            first_sequence=data["first_sequence"],
            payload_max_json_bytes=data["payload_max_json_bytes"],
            payload_max_ref_bytes=data["payload_max_ref_bytes"],
            payload_max_observation_refs=data["payload_max_observation_refs"],
            max_epoch=data["max_epoch"],
            max_sequence=data["max_sequence"],
            max_correlation_refs=data["max_correlation_refs"],
            max_causation_refs=data["max_causation_refs"],
            max_bytes=data["max_bytes"],
            max_record=data["max_record"],
            max_records=data["max_records"],
            max_validity_span_ns=data["max_validity_span_ns"],
            max_command_bytes=data["max_command_bytes"],
            max_response_bytes=data["max_response_bytes"],
            operation_budget_ns=data["operation_budget_ns"],
        )
    except BootstrapResourceProfileContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits)
    return value


def bootstrap_resource_profile_binding(value: BootstrapResourceProfile, limits: PayloadLimits) -> ContentBinding:
    _check_limits(limits)
    canon = encode_bootstrap_resource_profile(value, limits)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    try:
        return ContentBinding(ref=value.profile_ref, version=value.profile_version, sha256=digest)
    except PgContractError:
        _fail()
