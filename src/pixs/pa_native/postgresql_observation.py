"""Manifeste public d'observation PostgreSQL 1.0.0 : forme seulement.

Douze champs fermés exacts : schema, schema_version, observation_ref,
inspection_operation_id, installation_ref, target_ref, policy_ref,
policy_version, profile_bindings, resources, observed_at,
time_evidence_binding. Aucune identité, fraîcheur, réalité technique,
politique, autorisation ou producteur n'est prouvé par ce codec.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import datetime as _datetime
import hashlib as _hashlib
import json as _json
import re as _re

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import (
        ContentBinding,
        ContractError as _PGContractError,
        PayloadLimits,
    )
elif __package__ in (None, ""):
    import sys as _pg_obs_sys
    if "postgresql_contracts" not in _pg_obs_sys.builtin_module_names:
        raise ImportError("PA01_OBSERVATION_PG_BUILTIN_MISSING")
    import postgresql_contracts as _pg_obs_flat
    ContentBinding = _pg_obs_flat.ContentBinding
    _PGContractError = _pg_obs_flat.ContractError
    PayloadLimits = _pg_obs_flat.PayloadLimits
else:
    raise ImportError("PA01_OBSERVATION_CONTEXT_REFUSED")

__all__ = [
    "ObservationContractError",
    "ObservationProfileBindings",
    "ObservationResource",
    "ObservationManifest",
    "encode_observation",
    "decode_observation",
    "observation_binding",
]

_OBS_SCHEMA = "pixs.agent.postgresql.observation_manifest"
_OBS_VERSION = "1.0.0"
_OBS_PROFILE_KEYS = ("runtime", "service", "role", "database")
_OBS_KINDS = ("SOFTWARE", "CLUSTER", "SERVICE", "ROLE", "DATABASE")
_OBS_SERVICE_STATES = frozenset(("ABSENT", "STOPPED", "RUNNING", "UNOBSERVABLE"))
_OBS_OTHER_STATES = frozenset(("ABSENT", "PRESENT", "UNOBSERVABLE"))
_OBS_MATCH = frozenset(("MATCH", "MISMATCH", "UNDETERMINED"))
_OBS_TIME = _re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z"
)
_OBS_DIGEST = _re.compile(r"[0-9a-f]{64}")
_OBS_REF_FIELDS = (
    "observation_ref",
    "inspection_operation_id",
    "installation_ref",
    "target_ref",
    "policy_ref",
    "policy_version",
)


class ObservationContractError(ValueError):
    """Diagnostic stable sans contenu reçu."""


@dataclass(frozen=True, slots=True, repr=False)
class ObservationProfileBindings:
    runtime: ContentBinding
    service: ContentBinding
    role: ContentBinding
    database: ContentBinding

    def __post_init__(self):
        _check_profile_bindings(self, None)


@dataclass(frozen=True, slots=True, repr=False)
class ObservationResource:
    kind: str
    resource_ref: str
    state: str
    match: str
    evidence_binding: ContentBinding

    def __post_init__(self):
        _check_resource(self, None)


@dataclass(frozen=True, slots=True, repr=False)
class ObservationManifest:
    schema: str
    schema_version: str
    observation_ref: str
    inspection_operation_id: str
    installation_ref: str
    target_ref: str
    policy_ref: str
    policy_version: str
    profile_bindings: ObservationProfileBindings
    resources: tuple[ObservationResource, ...]
    observed_at: str
    time_evidence_binding: ContentBinding

    def __post_init__(self):
        _check_observation(self, None)


def _obs_ref(value: object, maximum: int | None) -> None:
    if type(value) is not str or not value:
        raise ObservationContractError("PA01_OBSERVATION_REFERENCE_INVALID")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127:
            raise ObservationContractError("PA01_OBSERVATION_REFERENCE_INVALID")
        if 0xD800 <= code <= 0xDFFF:
            raise ObservationContractError("PA01_OBSERVATION_REFERENCE_INVALID")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise ObservationContractError(
            "PA01_OBSERVATION_REFERENCE_UTF8_INVALID"
        ) from error
    if maximum is not None and size > maximum:
        raise ObservationContractError(
            "PA01_OBSERVATION_REFERENCE_LIMIT_EXCEEDED"
        )


def _obs_digest(value: object) -> None:
    if type(value) is not str or _OBS_DIGEST.fullmatch(value) is None:
        raise ObservationContractError("PA01_OBSERVATION_DIGEST_INVALID")


def _obs_fields(value: dict, names: tuple, code: str) -> None:
    if type(value) is not dict or set(value) != set(names):
        raise ObservationContractError(code)


def _obs_pairs(pairs):
    data = {}
    for name, _ in pairs:
        if name in data:
            raise ObservationContractError("PA01_OBSERVATION_JSON_DUPLICATED")
        data[name] = None
    return {name: val for name, val in pairs}


def _obs_constant(_token):
    raise ObservationContractError("PA01_OBSERVATION_CONSTANT_INVALID")


def _obs_number(_token):
    raise ObservationContractError("PA01_OBSERVATION_NUMBER_NOT_ALLOWED")


def _obs_timestamp(value: object) -> None:
    if type(value) is not str or _OBS_TIME.fullmatch(value) is None:
        raise ObservationContractError("PA01_OBSERVATION_TIMESTAMP_INVALID")
    try:
        _datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ObservationContractError(
            "PA01_OBSERVATION_TIMESTAMP_INVALID"
        ) from error


def _obs_check_binding_instance(value: object, maximum: int | None) -> None:
    if type(value) is not ContentBinding:
        raise ObservationContractError("PA01_OBSERVATION_BINDING_INVALID")
    _obs_ref(value.ref, maximum)
    _obs_ref(value.version, maximum)
    _obs_digest(value.sha256)


def _obs_binding_from_dict(value: object, maximum: int | None) -> ContentBinding:
    if type(value) is not dict:
        raise ObservationContractError("PA01_OBSERVATION_BINDING_INVALID")
    _obs_fields(value, ("ref", "version", "sha256"),
                 "PA01_OBSERVATION_BINDING_FIELDS_INVALID")
    if type(value["ref"]) is not str or type(value["version"]) is not str:
        raise ObservationContractError("PA01_OBSERVATION_BINDING_INVALID")
    _obs_ref(value["ref"], maximum)
    _obs_ref(value["version"], maximum)
    _obs_digest(value["sha256"])
    try:
        return ContentBinding(ref=value["ref"], version=value["version"],
                              sha256=value["sha256"])
    except _PGContractError as error:
        raise ObservationContractError(
            "PA01_OBSERVATION_BINDING_INVALID"
        ) from error


def _check_profile_bindings(value: object,
                             limits: PayloadLimits | None) -> None:
    if type(value) is not ObservationProfileBindings:
        raise ObservationContractError("PA01_OBSERVATION_PROFILE_INVALID")
    if limits is not None and type(limits) is not PayloadLimits:
        raise ObservationContractError("PA01_OBSERVATION_LIMITS_INVALID")
    maximum = None if limits is None else limits.max_ref_bytes
    for name in _OBS_PROFILE_KEYS:
        _obs_check_binding_instance(getattr(value, name), maximum)


def _check_resource(value: object, limits: PayloadLimits | None) -> None:
    if type(value) is not ObservationResource:
        raise ObservationContractError("PA01_OBSERVATION_RESOURCE_INVALID")
    if limits is not None and type(limits) is not PayloadLimits:
        raise ObservationContractError("PA01_OBSERVATION_LIMITS_INVALID")
    maximum = None if limits is None else limits.max_ref_bytes
    if type(value.kind) is not str or value.kind not in _OBS_KINDS:
        raise ObservationContractError("PA01_OBSERVATION_KIND_INVALID")
    _obs_ref(value.resource_ref, maximum)
    if type(value.state) is not str or type(value.match) is not str:
        raise ObservationContractError("PA01_OBSERVATION_STATE_INVALID")
    if value.kind == "SERVICE":
        if value.state not in _OBS_SERVICE_STATES:
            raise ObservationContractError("PA01_OBSERVATION_STATE_INVALID")
    else:
        if value.state not in _OBS_OTHER_STATES:
            raise ObservationContractError("PA01_OBSERVATION_STATE_INVALID")
    if value.match not in _OBS_MATCH:
        raise ObservationContractError("PA01_OBSERVATION_MATCH_INVALID")
    if value.state == "UNOBSERVABLE" and value.match != "UNDETERMINED":
        raise ObservationContractError("PA01_OBSERVATION_STATE_MATCH_MISMATCH")
    _obs_check_binding_instance(value.evidence_binding, maximum)


def _check_observation(value: object, limits: PayloadLimits | None) -> None:
    if type(value) is not ObservationManifest:
        raise ObservationContractError("PA01_OBSERVATION_DOCUMENT_INVALID")
    if limits is not None and type(limits) is not PayloadLimits:
        raise ObservationContractError("PA01_OBSERVATION_LIMITS_INVALID")
    maximum = None if limits is None else limits.max_ref_bytes
    if type(value.schema) is not str or value.schema != _OBS_SCHEMA:
        raise ObservationContractError("PA01_OBSERVATION_SCHEMA_INVALID")
    if type(value.schema_version) is not str or value.schema_version != _OBS_VERSION:
        raise ObservationContractError("PA01_OBSERVATION_SCHEMA_INVALID")
    for name in _OBS_REF_FIELDS:
        _obs_ref(getattr(value, name), maximum)
    _check_profile_bindings(value.profile_bindings, limits)
    if type(value.resources) is not tuple or len(value.resources) != 5:
        raise ObservationContractError("PA01_OBSERVATION_RESOURCES_INVALID")
    for item in value.resources:
        _check_resource(item, limits)
    if tuple(item.kind for item in value.resources) != _OBS_KINDS:
        raise ObservationContractError("PA01_OBSERVATION_ORDER_INVALID")
    _obs_timestamp(value.observed_at)
    _obs_check_binding_instance(value.time_evidence_binding, maximum)


def _obs_to_dict(value: ObservationManifest) -> dict:
    result = asdict(value)
    result["profile_bindings"] = {
        name: asdict(getattr(value.profile_bindings, name))
        for name in _OBS_PROFILE_KEYS
    }
    result["resources"] = [
        {"kind": r.kind, "resource_ref": r.resource_ref, "state": r.state,
         "match": r.match, "evidence_binding": asdict(r.evidence_binding)}
        for r in value.resources
    ]
    result["time_evidence_binding"] = asdict(value.time_evidence_binding)
    return result


def _obs_encode_dict(data: dict, limits: PayloadLimits) -> str:
    text = _json.dumps(data, ensure_ascii=False, allow_nan=False,
                       sort_keys=True, separators=(",", ":"))
    try:
        size = len(text.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise ObservationContractError(
            "PA01_OBSERVATION_UTF8_INVALID") from error
    if size > limits.max_json_bytes:
        raise ObservationContractError("PA01_OBSERVATION_LIMIT_EXCEEDED")
    return text


def encode_observation(value: ObservationManifest,
                       limits: PayloadLimits) -> str:
    """Octets canoniques UTF-8 fermés ; ne prouvent ni réalité ni fraîcheur."""
    if type(limits) is not PayloadLimits:
        raise ObservationContractError("PA01_OBSERVATION_LIMITS_INVALID")
    _check_observation(value, limits)
    return _obs_encode_dict(_obs_to_dict(value), limits)


def decode_observation(text: str, limits: PayloadLimits) -> ObservationManifest:
    if type(limits) is not PayloadLimits or type(text) is not str:
        raise ObservationContractError("PA01_OBSERVATION_PAYLOAD_INVALID")
    try:
        if len(text.encode("utf-8")) > limits.max_json_bytes:
            raise ObservationContractError("PA01_OBSERVATION_LIMIT_EXCEEDED")
        data = _json.loads(text, object_pairs_hook=_obs_pairs,
                           parse_int=_obs_number, parse_float=_obs_number,
                           parse_constant=_obs_constant)
    except (UnicodeEncodeError, _json.JSONDecodeError,
            RecursionError) as error:
        raise ObservationContractError(
            "PA01_OBSERVATION_JSON_INVALID") from error
    if type(data) is not dict:
        raise ObservationContractError("PA01_OBSERVATION_OBJECT_REQUIRED")
    _obs_fields(data, tuple(ObservationManifest.__dataclass_fields__),
                 "PA01_OBSERVATION_FIELDS_INVALID")
    maximum = limits.max_ref_bytes
    for name in _OBS_REF_FIELDS:
        _obs_ref(data[name], maximum)
    if type(data["schema"]) is not str or data["schema"] != _OBS_SCHEMA:
        raise ObservationContractError("PA01_OBSERVATION_SCHEMA_INVALID")
    if type(data["schema_version"]) is not str or data["schema_version"] != _OBS_VERSION:
        raise ObservationContractError("PA01_OBSERVATION_SCHEMA_INVALID")
    profiles = data["profile_bindings"]
    if type(profiles) is not dict:
        raise ObservationContractError("PA01_OBSERVATION_PROFILE_INVALID")
    _obs_fields(profiles, _OBS_PROFILE_KEYS,
                 "PA01_OBSERVATION_PROFILE_FIELDS_INVALID")
    bindings = tuple(_obs_binding_from_dict(profiles[name], maximum)
                     for name in _OBS_PROFILE_KEYS)
    profile_obj = ObservationProfileBindings(*bindings)
    _check_profile_bindings(profile_obj, limits)
    raw_resources = data["resources"]
    if type(raw_resources) is not list or len(raw_resources) != 5:
        raise ObservationContractError("PA01_OBSERVATION_RESOURCES_INVALID")
    items = []
    for entry in raw_resources:
        if type(entry) is not dict:
            raise ObservationContractError("PA01_OBSERVATION_RESOURCE_INVALID")
        _obs_fields(entry, ("kind", "resource_ref", "state", "match",
                            "evidence_binding"),
                     "PA01_OBSERVATION_RESOURCE_FIELDS_INVALID")
        ev = _obs_binding_from_dict(entry["evidence_binding"], maximum)
        obj = ObservationResource(kind=entry["kind"],
                                  resource_ref=entry["resource_ref"],
                                  state=entry["state"],
                                  match=entry["match"],
                                  evidence_binding=ev)
        items.append(obj)
    resources = tuple(items)
    time_binding = _obs_binding_from_dict(data["time_evidence_binding"],
                                          maximum)
    _obs_timestamp(data["observed_at"])
    result = ObservationManifest(
        schema=data["schema"], schema_version=data["schema_version"],
        observation_ref=data["observation_ref"],
        inspection_operation_id=data["inspection_operation_id"],
        installation_ref=data["installation_ref"],
        target_ref=data["target_ref"], policy_ref=data["policy_ref"],
        policy_version=data["policy_version"],
        profile_bindings=profile_obj, resources=resources,
        observed_at=data["observed_at"],
        time_evidence_binding=time_binding)
    _check_observation(result, limits)
    return result


def observation_binding(value: ObservationManifest,
                        limits: PayloadLimits) -> ContentBinding:
    """Binding du manifeste : ref opaque, version 1.0.0 fixée, sha des octets."""
    if type(limits) is not PayloadLimits:
        raise ObservationContractError("PA01_OBSERVATION_LIMITS_INVALID")
    _check_observation(value, limits)
    digest = _hashlib.sha256(
        encode_observation(value, limits).encode("utf-8")).hexdigest()
    try:
        binding = ContentBinding(ref=value.observation_ref, version="1.0.0",
                                 sha256=digest)
    except _PGContractError as error:
        raise ObservationContractError(
            "PA01_OBSERVATION_BINDING_INVALID") from error
    _obs_check_binding_instance(binding, limits.max_ref_bytes)
    return binding
