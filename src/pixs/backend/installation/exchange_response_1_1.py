from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError,
    PayloadLimits,
    NativeResult,
    decode_result,
    encode_result,
)
from pixs.pa_native.postgresql_observation import (
    ObservationManifest,
    ObservationContractError,
    decode_observation,
    encode_observation,
    observation_binding,
)
from .planning_bundle import (
    PlanningBundle,
    PlanningBundleLimits,
    PlanningBundleError,
    parse_planning_bundle,
    dump_planning_bundle,
    planning_bundle_binding,
)
from .exchange_envelope_1_1 import (
    ExchangeEnvelopeError,
    ExchangeRequest,
    ExchangeRequestLimits,
    dump_exchange_request,
)


__all__ = [
    "ExchangeResponseError",
    "ExchangeResponseLimits",
    "ObservationPayload",
    "PlanningPayload",
    "ExchangeResponse",
    "parse_exchange_response",
    "dump_exchange_response",
    "exchange_response_sha256",
    "match_request_response",
]


_RESP_SCHEMA = "pixs.agent.postgresql.exchange.response"
_RESP_VERSION = "1.1.0"
_PURPOSES = ("OBSERVE", "PREPARE_PLAN", "PREPARE", "READ_RESULT")
_PURPOSE_OPERATION = {
    "OBSERVE": "inspect_postgresql",
    "PREPARE_PLAN": "inspect_postgresql",
    "PREPARE": "prepare_postgresql",
    "READ_RESULT": "get_postgresql_result",
}


class ExchangeResponseError(ValueError):
    def __init__(self) -> None:
        super().__init__("Reponse echange 1.1 C08 non verifiable.")
        self.code = "C08_EXCHANGE_RESPONSE_INVALID"
        self.element = "exchange_response"
        self.step = "validate_exchange_response"


@dataclass(frozen=True, slots=True)
class ExchangeResponseLimits:
    payload: PayloadLimits
    bundle_limits: PlanningBundleLimits
    max_response_bytes: int

    def __post_init__(self) -> None:
        if type(self.payload) is not PayloadLimits:
            raise ExchangeResponseError()
        if type(self.bundle_limits) is not PlanningBundleLimits:
            raise ExchangeResponseError()
        if type(self.max_response_bytes) is not int:
            raise ExchangeResponseError()
        if self.max_response_bytes < 1:
            raise ExchangeResponseError()


@dataclass(frozen=True, slots=True, repr=False)
class ObservationPayload:
    observation_document: ObservationManifest
    observation_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.observation_document) is not ObservationManifest:
            raise ExchangeResponseError()
        if type(self.observation_binding) is not ContentBinding:
            raise ExchangeResponseError()


@dataclass(frozen=True, slots=True, repr=False)
class PlanningPayload:
    planning_bundle: PlanningBundle
    planning_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.planning_bundle) is not PlanningBundle:
            raise ExchangeResponseError()
        if type(self.planning_binding) is not ContentBinding:
            raise ExchangeResponseError()


@dataclass(frozen=True, slots=True, repr=False)
class ExchangeResponse:
    schema: str
    schema_version: str
    purpose: str
    result: NativeResult
    payload: ObservationPayload | PlanningPayload | None

    def __post_init__(self) -> None:
        _check_structure(self)


def _pairs(pairs) -> dict:
    d = {}
    for k, v in pairs:
        if k in d:
            raise ExchangeResponseError()
        d[k] = v
    return d


def _number(v) -> None:
    raise ExchangeResponseError()


def _check_structure(value: ExchangeResponse) -> None:
    if type(value) is not ExchangeResponse:
        raise ExchangeResponseError()
    if type(value.schema) is not str or value.schema != _RESP_SCHEMA:
        raise ExchangeResponseError()
    if type(value.schema_version) is not str:
        raise ExchangeResponseError()
    if value.schema_version != _RESP_VERSION:
        raise ExchangeResponseError()
    if type(value.purpose) is not str:
        raise ExchangeResponseError()
    if value.purpose not in _PURPOSES:
        raise ExchangeResponseError()
    if type(value.result) is not NativeResult:
        raise ExchangeResponseError()
    if value.result.catalog_operation != _PURPOSE_OPERATION[value.purpose]:
        raise ExchangeResponseError()
    phase = value.result.phase
    if type(phase) is not str:
        raise ExchangeResponseError()
    if phase != "SUCCEEDED" or value.purpose in ("PREPARE", "READ_RESULT"):
        if value.payload is not None:
            raise ExchangeResponseError()
        return
    if value.purpose == "OBSERVE":
        if type(value.payload) is not ObservationPayload:
            raise ExchangeResponseError()
        obs = value.payload.observation_document
        bind = value.payload.observation_binding
        if bind.version != "1.0.0":
            raise ExchangeResponseError()
        if bind.ref != obs.observation_ref:
            raise ExchangeResponseError()
        if obs.inspection_operation_id != value.result.operation_id:
            raise ExchangeResponseError()
        if obs.installation_ref != value.result.installation_ref:
            raise ExchangeResponseError()
        if obs.target_ref != value.result.target_ref:
            raise ExchangeResponseError()
        if type(value.result.observation_refs) is not tuple:
            raise ExchangeResponseError()
        if obs.observation_ref not in value.result.observation_refs:
            raise ExchangeResponseError()
        return
    if value.purpose == "PREPARE_PLAN":
        if type(value.payload) is not PlanningPayload:
            raise ExchangeResponseError()
        bundle = value.payload.planning_bundle
        bind = value.payload.planning_binding
        if bind.version != "1.0.0":
            raise ExchangeResponseError()
        if bind.ref != bundle.bundle_ref:
            raise ExchangeResponseError()
        if value.result.operation_id != bundle.planning_operation_id:
            raise ExchangeResponseError()
        if value.result.installation_ref != bundle.installation_ref:
            raise ExchangeResponseError()
        if value.result.target_ref != bundle.target_ref:
            raise ExchangeResponseError()
        if value.result.correlation_id != bundle.correlation_id:
            raise ExchangeResponseError()
        if value.result.plan_ref != bundle.plan_document.plan_ref:
            raise ExchangeResponseError()
        if value.result.plan_version != bundle.plan_document.plan_version:
            raise ExchangeResponseError()
        if value.result.plan_digest != bundle.plan_binding.sha256:
            raise ExchangeResponseError()
        if type(value.result.observation_refs) is not tuple:
            raise ExchangeResponseError()
        if bundle.observation_binding.ref not in value.result.observation_refs:
            raise ExchangeResponseError()
        return
    raise ExchangeResponseError()


def _check_bounded(
    value: ExchangeResponse, limits: ExchangeResponseLimits
) -> None:
    if type(limits) is not ExchangeResponseLimits:
        raise ExchangeResponseError()
    _check_structure(value)
    phase = value.result.phase
    if phase != "SUCCEEDED":
        return
    if value.purpose == "OBSERVE":
        if type(value.payload) is not ObservationPayload:
            raise ExchangeResponseError()
        obs = value.payload.observation_document
        bind = value.payload.observation_binding
        try:
            expect = observation_binding(obs, limits.payload)
        except ObservationContractError as e:
            raise ExchangeResponseError() from e
        if (
            expect.ref != bind.ref
            or expect.version != bind.version
            or expect.sha256 != bind.sha256
        ):
            raise ExchangeResponseError()
        return
    if value.purpose == "PREPARE_PLAN":
        if type(value.payload) is not PlanningPayload:
            raise ExchangeResponseError()
        bundle = value.payload.planning_bundle
        bind = value.payload.planning_binding
        try:
            expect = planning_bundle_binding(bundle, limits.bundle_limits)
        except PlanningBundleError as e:
            raise ExchangeResponseError() from e
        if (
            expect.ref != bind.ref
            or expect.version != bind.version
            or expect.sha256 != bind.sha256
        ):
            raise ExchangeResponseError()
        return
    return


def _decode_outer(raw: bytes, limits: ExchangeResponseLimits) -> dict:
    if type(raw) is not bytes or not raw:
        raise ExchangeResponseError()
    if len(raw) > limits.max_response_bytes:
        raise ExchangeResponseError()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ExchangeResponseError() from e
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise ExchangeResponseError() from e
    if type(doc) is not dict:
        raise ExchangeResponseError()
    return doc


def _encode_outer(doc: dict, limits: ExchangeResponseLimits) -> bytes:
    try:
        text = json.dumps(
            doc,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise ExchangeResponseError() from e
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError as e:
        raise ExchangeResponseError() from e
    if len(raw) > limits.max_response_bytes:
        raise ExchangeResponseError()
    return raw


def parse_exchange_response(
    raw: bytes, limits: ExchangeResponseLimits
) -> ExchangeResponse:
    if type(limits) is not ExchangeResponseLimits:
        raise ExchangeResponseError()
    doc = _decode_outer(raw, limits)
    if set(doc) != {"schema", "schema_version", "purpose", "result", "payload"}:
        raise ExchangeResponseError()
    if type(doc["schema"]) is not str:
        raise ExchangeResponseError()
    if doc["schema"] != _RESP_SCHEMA:
        raise ExchangeResponseError()
    if type(doc["schema_version"]) is not str:
        raise ExchangeResponseError()
    if doc["schema_version"] != _RESP_VERSION:
        raise ExchangeResponseError()
    purpose = doc["purpose"]
    if type(purpose) is not str or purpose not in _PURPOSES:
        raise ExchangeResponseError()
    if type(doc["result"]) is not dict:
        raise ExchangeResponseError()
    if type(doc["payload"]) is not dict:
        raise ExchangeResponseError()
    try:
        res_text = json.dumps(
            doc["result"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise ExchangeResponseError() from e
    try:
        result = decode_result(res_text, limits.payload)
    except ContractError as e:
        raise ExchangeResponseError() from e
    if result.catalog_operation != _PURPOSE_OPERATION[purpose]:
        raise ExchangeResponseError()
    payload: ObservationPayload | PlanningPayload | None = None
    if result.phase == "SUCCEEDED" and purpose == "OBSERVE":
        if set(doc["payload"]) != {"observation_document", "observation_binding"}:
            raise ExchangeResponseError()
        if type(doc["payload"]["observation_document"]) is not dict:
            raise ExchangeResponseError()
        try:
            obs_text = json.dumps(
                doc["payload"]["observation_document"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        except (TypeError, ValueError, RecursionError) as e:
            raise ExchangeResponseError() from e
        try:
            obs = decode_observation(obs_text, limits.payload)
        except ObservationContractError as e:
            raise ExchangeResponseError() from e
        bdoc = doc["payload"]["observation_binding"]
        if type(bdoc) is not dict or set(bdoc) != {"ref", "version", "sha256"}:
            raise ExchangeResponseError()
        try:
            bind = ContentBinding(
                ref=bdoc["ref"], version=bdoc["version"], sha256=bdoc["sha256"]
            )
        except ContractError as e:
            raise ExchangeResponseError() from e
        payload = ObservationPayload(
            observation_document=obs, observation_binding=bind
        )
    elif result.phase == "SUCCEEDED" and purpose == "PREPARE_PLAN":
        if set(doc["payload"]) != {"planning_bundle", "planning_binding"}:
            raise ExchangeResponseError()
        if type(doc["payload"]["planning_bundle"]) is not dict:
            raise ExchangeResponseError()
        try:
            bundle_text = json.dumps(
                doc["payload"]["planning_bundle"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        except (TypeError, ValueError, RecursionError) as e:
            raise ExchangeResponseError() from e
        try:
            bundle = parse_planning_bundle(
                bundle_text.encode("utf-8"), limits.bundle_limits
            )
        except (PlanningBundleError, UnicodeEncodeError) as e:
            raise ExchangeResponseError() from e
        bdoc = doc["payload"]["planning_binding"]
        if type(bdoc) is not dict or set(bdoc) != {"ref", "version", "sha256"}:
            raise ExchangeResponseError()
        try:
            bind = ContentBinding(
                ref=bdoc["ref"], version=bdoc["version"], sha256=bdoc["sha256"]
            )
        except ContractError as e:
            raise ExchangeResponseError() from e
        payload = PlanningPayload(planning_bundle=bundle, planning_binding=bind)
    else:
        if doc["payload"] != {}:
            raise ExchangeResponseError()
        payload = None
    value = ExchangeResponse(
        schema=doc["schema"],
        schema_version=doc["schema_version"],
        purpose=purpose,
        result=result,
        payload=payload,
    )
    _check_bounded(value, limits)
    if dump_exchange_response(value, limits) != raw:
        raise ExchangeResponseError()
    return value


def dump_exchange_response(
    value: ExchangeResponse, limits: ExchangeResponseLimits
) -> bytes:
    if type(limits) is not ExchangeResponseLimits:
        raise ExchangeResponseError()
    _check_bounded(value, limits)
    try:
        res_text = encode_result(value.result, limits.payload)
    except ContractError as e:
        raise ExchangeResponseError() from e
    try:
        res_doc = json.loads(
            res_text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise ExchangeResponseError() from e
    if value.purpose == "OBSERVE" and value.result.phase == "SUCCEEDED":
        if type(value.payload) is not ObservationPayload:
            raise ExchangeResponseError()
        try:
            obs_text = encode_observation(
                value.payload.observation_document, limits.payload
            )
        except ObservationContractError as e:
            raise ExchangeResponseError() from e
        try:
            obs_doc = json.loads(
                obs_text,
                object_pairs_hook=_pairs,
                parse_int=_number,
                parse_float=_number,
                parse_constant=_number,
            )
        except (json.JSONDecodeError, RecursionError) as e:
            raise ExchangeResponseError() from e
        pay = {
            "observation_document": obs_doc,
            "observation_binding": {
                "ref": value.payload.observation_binding.ref,
                "version": value.payload.observation_binding.version,
                "sha256": value.payload.observation_binding.sha256,
            },
        }
    elif value.purpose == "PREPARE_PLAN":
        if value.result.phase != "SUCCEEDED":
            if value.payload is not None:
                raise ExchangeResponseError()
            pay = {}
        else:
            if type(value.payload) is not PlanningPayload:
                raise ExchangeResponseError()
            try:
                bundle_raw = dump_planning_bundle(
                    value.payload.planning_bundle, limits.bundle_limits
                )
            except PlanningBundleError as e:
                raise ExchangeResponseError() from e
            try:
                bundle_doc = json.loads(
                    bundle_raw.decode("utf-8"),
                    object_pairs_hook=_pairs,
                    parse_int=_number,
                    parse_float=_number,
                    parse_constant=_number,
                )
            except (
                UnicodeDecodeError,
                json.JSONDecodeError,
                RecursionError,
            ) as e:
                raise ExchangeResponseError() from e
            pay = {
                "planning_bundle": bundle_doc,
                "planning_binding": {
                    "ref": value.payload.planning_binding.ref,
                    "version": value.payload.planning_binding.version,
                    "sha256": value.payload.planning_binding.sha256,
                },
            }
    else:
        if value.payload is not None:
            raise ExchangeResponseError()
        pay = {}
    doc = {
        "schema": value.schema,
        "schema_version": value.schema_version,
        "purpose": value.purpose,
        "result": res_doc,
        "payload": pay,
    }
    return _encode_outer(doc, limits)


def exchange_response_sha256(
    value: ExchangeResponse, limits: ExchangeResponseLimits
) -> str:
    return hashlib.sha256(dump_exchange_response(value, limits)).hexdigest()


def match_request_response(
    request: ExchangeRequest,
    request_limits: ExchangeRequestLimits,
    response: ExchangeResponse,
    response_limits: ExchangeResponseLimits,
) -> None:
    try:
        dump_exchange_request(request, request_limits)
    except ExchangeEnvelopeError as e:
        raise ExchangeResponseError() from e
    dump_exchange_response(response, response_limits)
    if request.purpose != response.purpose:
        raise ExchangeResponseError()
    if request.request.catalog_operation != response.result.catalog_operation:
        raise ExchangeResponseError()
    if request.request.operation_id != response.result.operation_id:
        raise ExchangeResponseError()
    if request.request.correlation_id != response.result.correlation_id:
        raise ExchangeResponseError()
    if request.request.installation_ref != response.result.installation_ref:
        raise ExchangeResponseError()
    if request.request.target_ref != response.result.target_ref:
        raise ExchangeResponseError()
    if request.purpose == "READ_RESULT":
        params = request.request.params
        if type(params) is not tuple:
            raise ExchangeResponseError()
        found = None
        for k, v in params:
            if type(k) is not str or type(v) is not str:
                raise ExchangeResponseError()
            if k == "operation_ref":
                found = v
        if found is None:
            raise ExchangeResponseError()
        if response.result.subject_operation_ref != found:
            raise ExchangeResponseError()
    if request.purpose == "PREPARE":
        params = request.request.params
        if type(params) is not tuple:
            raise ExchangeResponseError()
        wanted: dict[str, str] = {}
        for k, v in params:
            if type(k) is not str or type(v) is not str:
                raise ExchangeResponseError()
            wanted[k] = v
        if response.result.phase == "SUCCEEDED":
            if response.result.plan_ref != wanted.get("plan_ref"):
                raise ExchangeResponseError()
            if response.result.plan_version != wanted.get("plan_version"):
                raise ExchangeResponseError()
            if response.result.plan_digest != wanted.get("plan_digest"):
                raise ExchangeResponseError()
        else:
            if response.result.plan_ref is not None:
                if response.result.plan_ref != wanted.get("plan_ref"):
                    raise ExchangeResponseError()
            if response.result.plan_version is not None:
                if response.result.plan_version != wanted.get("plan_version"):
                    raise ExchangeResponseError()
            if response.result.plan_digest is not None:
                if response.result.plan_digest != wanted.get("plan_digest"):
                    raise ExchangeResponseError()
    if request.purpose == "PREPARE_PLAN":
        if response.result.phase != "SUCCEEDED":
            return None
        if type(response.payload) is not PlanningPayload:
            raise ExchangeResponseError()
        bundle = response.payload.planning_bundle
        if request.projection_binding != bundle.projection_binding:
            raise ExchangeResponseError()
        if request.projection_document != bundle.projection_document:
            raise ExchangeResponseError()
        if request.confirmation_ref != bundle.plan_document.confirmation_ref:
            raise ExchangeResponseError()
    return None
