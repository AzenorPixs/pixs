"""Manifeste public d effets PostgreSQL 1.0.0 : forme seulement.

Huit champs fermes exacts : schema, schema_version, effects_ref,
installation_ref, target_ref, operation_id, projection_binding,
allowed_effects. Aucune couverture, fraicheur, realite technique,
autorisation ou producteur n est prouve par ce codec.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib as _hashlib
import json as _json

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import (
        ContentBinding,
        ContractError as _PGContractError,
        PayloadLimits,
    )
elif __package__ in (None, ""):
    import sys as _pg_eff_sys
    if "postgresql_contracts" not in _pg_eff_sys.builtin_module_names:
        raise ImportError("PA01_EFFECTS_PG_BUILTIN_MISSING")
    import postgresql_contracts as _pg_eff_flat
    ContentBinding = _pg_eff_flat.ContentBinding
    _PGContractError = _pg_eff_flat.ContractError
    PayloadLimits = _pg_eff_flat.PayloadLimits
else:
    raise ImportError("PA01_EFFECTS_CONTEXT_REFUSED")

__all__ = [
    "EffectsContractError",
    "EffectsManifest",
    "encode_effects",
    "decode_effects",
    "effects_binding",
    "effects_digest",
]

_EFF_SCHEMA = "pixs.agent.postgresql.effects_manifest"
_EFF_VERSION = "1.0.0"
_EFF_BINDING_VERSION = "1.0.0"
_EFF_FIELDS8 = (
    "schema", "schema_version", "effects_ref", "installation_ref",
    "target_ref", "operation_id", "projection_binding", "allowed_effects",
)
EFFECTS_CANONICAL = (
    "SERVICE_INSTALL",
    "SERVICE_CONFIGURE",
    "CLUSTER_INITIALIZE",
    "SERVICE_START",
    "ROLE_CREATE",
    "DATABASE_CREATE",
)
EFFECTS_CLOSED = frozenset(EFFECTS_CANONICAL)
_EFF_INDEX = {n: i for i, n in enumerate(EFFECTS_CANONICAL)}
_EFF_REF_FIELDS = (
    "effects_ref", "installation_ref", "target_ref", "operation_id",
)


class EffectsContractError(ValueError):
    """Diagnostic stable sans contenu recu."""


@dataclass(frozen=True, slots=True, repr=False)
class EffectsManifest:
    schema: str
    schema_version: str
    effects_ref: str
    installation_ref: str
    target_ref: str
    operation_id: str
    projection_binding: ContentBinding
    allowed_effects: tuple[str, ...]

    def __post_init__(self):
        _check_effects(self, None)


def _eff_ref(value: object, maximum: int | None) -> None:
    if type(value) is not str or not value:
        raise EffectsContractError("PA01_EFFECTS_REFERENCE_INVALID")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127:
            raise EffectsContractError("PA01_EFFECTS_REFERENCE_INVALID")
        if 0xD800 <= code <= 0xDFFF:
            raise EffectsContractError("PA01_EFFECTS_REFERENCE_INVALID")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise EffectsContractError(
            "PA01_EFFECTS_REFERENCE_UTF8_INVALID"
        ) from error
    if maximum is not None and size > maximum:
        raise EffectsContractError(
            "PA01_EFFECTS_REFERENCE_LIMIT_EXCEEDED"
        )


def _eff_digest(value: object) -> None:
    import re as _re
    if type(value) is not str or _re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise EffectsContractError("PA01_EFFECTS_DIGEST_INVALID")


def _eff_fields(value: dict, names: tuple, code: str) -> None:
    if type(value) is not dict or set(value) != set(names):
        raise EffectsContractError(code)


def _eff_pairs(pairs):
    data = {}
    for name, _ in pairs:
        if name in data:
            raise EffectsContractError("PA01_EFFECTS_JSON_DUPLICATED")
        data[name] = None
    return {name: val for name, val in pairs}


def _eff_constant(_token):
    raise EffectsContractError("PA01_EFFECTS_CONSTANT_INVALID")


def _eff_number(_token):
    raise EffectsContractError("PA01_EFFECTS_NUMBER_NOT_ALLOWED")


def _eff_check_binding_instance(value: object, maximum: int | None) -> None:
    if type(value) is not ContentBinding:
        raise EffectsContractError("PA01_EFFECTS_BINDING_INVALID")
    _eff_ref(value.ref, maximum)
    _eff_ref(value.version, maximum)
    _eff_digest(value.sha256)


def _eff_binding_from_dict(value: object, maximum: int | None) -> ContentBinding:
    if type(value) is not dict:
        raise EffectsContractError("PA01_EFFECTS_BINDING_INVALID")
    _eff_fields(value, ("ref", "version", "sha256"),
                "PA01_EFFECTS_BINDING_FIELDS_INVALID")
    if type(value["ref"]) is not str or type(value["version"]) is not str:
        raise EffectsContractError("PA01_EFFECTS_BINDING_INVALID")
    _eff_ref(value["ref"], maximum)
    _eff_ref(value["version"], maximum)
    _eff_digest(value["sha256"])
    try:
        return ContentBinding(ref=value["ref"], version=value["version"],
                              sha256=value["sha256"])
    except _PGContractError as error:
        raise EffectsContractError(
            "PA01_EFFECTS_BINDING_INVALID"
        ) from error


def _check_effects(value: object, limits: PayloadLimits | None) -> None:
    if type(value) is not EffectsManifest:
        raise EffectsContractError("PA01_EFFECTS_DOCUMENT_INVALID")
    if limits is not None and type(limits) is not PayloadLimits:
        raise EffectsContractError("PA01_EFFECTS_LIMITS_INVALID")
    maximum = None if limits is None else limits.max_ref_bytes
    if type(value.schema) is not str or value.schema != _EFF_SCHEMA:
        raise EffectsContractError("PA01_EFFECTS_SCHEMA_INVALID")
    if type(value.schema_version) is not str or value.schema_version != _EFF_VERSION:
        raise EffectsContractError("PA01_EFFECTS_SCHEMA_INVALID")
    for name in _EFF_REF_FIELDS:
        _eff_ref(getattr(value, name), maximum)
    _eff_check_binding_instance(value.projection_binding, maximum)
    if value.projection_binding.version != _EFF_BINDING_VERSION:
        raise EffectsContractError("PA01_EFFECTS_BINDING_VERSION_MISMATCH")
    if type(value.allowed_effects) is not tuple:
        raise EffectsContractError("PA01_EFFECTS_LIST_INVALID")
    seen: set[str] = set()
    last = -1
    for e in value.allowed_effects:
        if type(e) is not str or e not in EFFECTS_CLOSED or e in seen:
            raise EffectsContractError("PA01_EFFECTS_ENTRY_INVALID")
        if _EFF_INDEX[e] <= last:
            raise EffectsContractError("PA01_EFFECTS_ORDER_INVALID")
        seen.add(e)
        last = _EFF_INDEX[e]


def _eff_to_dict(value: EffectsManifest) -> dict:
    b = value.projection_binding
    return {
        "schema": value.schema, "schema_version": value.schema_version,
        "effects_ref": value.effects_ref,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref, "operation_id": value.operation_id,
        "projection_binding": {"ref": b.ref, "version": b.version,
                               "sha256": b.sha256},
        "allowed_effects": list(value.allowed_effects),
    }


def _eff_encode_dict(data: dict, limits: PayloadLimits) -> str:
    text = _json.dumps(data, ensure_ascii=False, allow_nan=False,
                       sort_keys=True, separators=(",", ":"))
    try:
        size = len(text.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise EffectsContractError(
            "PA01_EFFECTS_UTF8_INVALID") from error
    if size > limits.max_json_bytes:
        raise EffectsContractError("PA01_EFFECTS_LIMIT_EXCEEDED")
    return text


def encode_effects(value: EffectsManifest,
                   limits: PayloadLimits) -> str:
    """Octets canoniques UTF-8 fermes ; vide admis comme FORME sans admission."""
    if type(limits) is not PayloadLimits:
        raise EffectsContractError("PA01_EFFECTS_LIMITS_INVALID")
    _check_effects(value, limits)
    return _eff_encode_dict(_eff_to_dict(value), limits)


def decode_effects(text: str, limits: PayloadLimits) -> EffectsManifest:
    if type(limits) is not PayloadLimits or type(text) is not str:
        raise EffectsContractError("PA01_EFFECTS_PAYLOAD_INVALID")
    try:
        if len(text.encode("utf-8")) > limits.max_json_bytes:
            raise EffectsContractError("PA01_EFFECTS_LIMIT_EXCEEDED")
        data = _json.loads(text, object_pairs_hook=_eff_pairs,
                           parse_int=_eff_number, parse_float=_eff_number,
                           parse_constant=_eff_constant)
    except (UnicodeEncodeError, _json.JSONDecodeError,
            RecursionError) as error:
        raise EffectsContractError(
            "PA01_EFFECTS_JSON_INVALID") from error
    if type(data) is not dict:
        raise EffectsContractError("PA01_EFFECTS_OBJECT_REQUIRED")
    _eff_fields(data, _EFF_FIELDS8, "PA01_EFFECTS_FIELDS_INVALID")
    maximum = limits.max_ref_bytes
    for name in _EFF_REF_FIELDS:
        _eff_ref(data[name], maximum)
    if type(data["schema"]) is not str or data["schema"] != _EFF_SCHEMA:
        raise EffectsContractError("PA01_EFFECTS_SCHEMA_INVALID")
    if type(data["schema_version"]) is not str or data["schema_version"] != _EFF_VERSION:
        raise EffectsContractError("PA01_EFFECTS_SCHEMA_INVALID")
    pb = _eff_binding_from_dict(data["projection_binding"], maximum)
    if pb.version != _EFF_BINDING_VERSION:
        raise EffectsContractError("PA01_EFFECTS_BINDING_VERSION_MISMATCH")
    ae = data["allowed_effects"]
    if type(ae) is not list:
        raise EffectsContractError("PA01_EFFECTS_LIST_INVALID")
    for e in ae:
        if type(e) is not str:
            raise EffectsContractError("PA01_EFFECTS_ENTRY_INVALID")
    result = EffectsManifest(
        schema=data["schema"], schema_version=data["schema_version"],
        effects_ref=data["effects_ref"],
        installation_ref=data["installation_ref"],
        target_ref=data["target_ref"], operation_id=data["operation_id"],
        projection_binding=pb, allowed_effects=tuple(ae))
    _check_effects(result, limits)
    return result


def effects_binding(value: EffectsManifest,
                    limits: PayloadLimits) -> ContentBinding:
    """Binding du document entier : ref opaque, version 1.0.0, sha des octets."""
    if type(limits) is not PayloadLimits:
        raise EffectsContractError("PA01_EFFECTS_LIMITS_INVALID")
    _check_effects(value, limits)
    digest = _hashlib.sha256(
        encode_effects(value, limits).encode("utf-8")).hexdigest()
    try:
        binding = ContentBinding(ref=value.effects_ref, version="1.0.0",
                                 sha256=digest)
    except _PGContractError as error:
        raise EffectsContractError(
            "PA01_EFFECTS_BINDING_INVALID") from error
    _eff_check_binding_instance(binding, limits.max_ref_bytes)
    return binding


def effects_digest(value: EffectsManifest,
                   limits: PayloadLimits) -> str:
    """SHA du seul tableau canonique, apres validation document+budget."""
    if type(limits) is not PayloadLimits:
        raise EffectsContractError("PA01_EFFECTS_LIMITS_INVALID")
    text = encode_effects(value, limits)
    _ = text
    arr = _json.dumps(list(value.allowed_effects), ensure_ascii=False,
                      allow_nan=False, sort_keys=True,
                      separators=(",", ":"))
    return _hashlib.sha256(arr.encode("utf-8")).hexdigest()
