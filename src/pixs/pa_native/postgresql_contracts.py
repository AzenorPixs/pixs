"""Contrats techniques PostgreSQL PA01 v1 : structure seulement.

Aucune identité, autorisation, confirmation, durabilité ou fraîcheur n'est
prouvée par ces DTO. Transport A07/PZT et propriétaires serveur restent requis.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import binascii
import datetime as _datetime
import hashlib
import json
import re

__all__ = ["ContractError", "PayloadLimits", "NativeRequest", "NativeResult",
           "TechnicalPlan", "decode_request", "decode_result", "decode_plan",
           "encode_request", "encode_result", "encode_plan", "plan_sha256"]

_OPERATIONS = {
    "inspect_postgresql": (),
    "prepare_postgresql": ("plan_digest", "plan_ref", "plan_version"),
    "get_postgresql_result": ("operation_ref",),
}
_PHASES = frozenset(("RECEIVED", "RUNNING", "SUCCEEDED", "FAILED", "IN_DOUBT", "BLOCKED"))
_DIGEST = re.compile(r"[0-9a-f]{64}")
_CODE = re.compile(r"[A-Z][A-Z0-9_]*")


class ContractError(ValueError):
    """Diagnostic stable sans contenu reçu."""


@dataclass(frozen=True, slots=True)
class PayloadLimits:
    max_json_bytes: int
    max_ref_bytes: int
    max_observation_refs: int

    def __post_init__(self):
        if any(type(value) is not int or value <= 0
               for value in (self.max_json_bytes, self.max_ref_bytes, self.max_observation_refs)):
            raise ContractError("PA01_LIMITS_INVALID")


def _ref(value: object, limit: int | None = None) -> None:
    if type(value) is not str or not value or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ContractError("PA01_REFERENCE_INVALID")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise ContractError("PA01_REFERENCE_UTF8_INVALID") from error
    if limit is not None and size > limit:
        raise ContractError("PA01_REFERENCE_LIMIT_EXCEEDED")


def _common(value, limits: PayloadLimits | None) -> None:
    if (type(value.schema_version) is not str or value.schema_version != "1.0.0"
            or type(value.catalog_version) is not str or value.catalog_version != "1.0.0"):
        raise ContractError("PA01_CONTRACT_VERSION_INVALID")
    if type(value.catalog_operation) is not str or value.catalog_operation not in _OPERATIONS:
        raise ContractError("PA01_OPERATION_NOT_DELIVERED")
    maximum = None if limits is None else limits.max_ref_bytes
    for name in ("operation_id", "correlation_id", "installation_ref", "target_ref"):
        _ref(getattr(value, name), maximum)


@dataclass(frozen=True, slots=True, repr=False)
class NativeRequest:
    schema_version: str
    catalog_operation: str
    catalog_version: str
    operation_id: str
    idempotency_key: str
    correlation_id: str
    installation_ref: str
    target_ref: str
    mandate_ref: str
    params: tuple[tuple[str, str], ...]

    def __post_init__(self):
        _check_request(self, None)


@dataclass(frozen=True, slots=True, repr=False)
class NativeResult:
    schema_version: str
    catalog_operation: str
    catalog_version: str
    operation_id: str
    correlation_id: str
    installation_ref: str
    target_ref: str
    subject_operation_ref: str | None
    phase: str
    result_ref: str | None
    observation_refs: tuple[str, ...]
    plan_ref: str | None
    plan_version: str | None
    plan_digest: str | None
    diagnostic_code: str | None

    def __post_init__(self):
        _check_result(self, None)



@dataclass(frozen=True, slots=True, repr=False)
class TechnicalPlan:
    schema_version: str
    catalog_operation: str
    catalog_version: str
    operation_id: str
    idempotency_key: str
    correlation_id: str
    plan_ref: str
    plan_version: str
    installation_ref: str
    target_ref: str
    projection_ref: str
    confirmation_ref: str
    policy_ref: str
    preconditions_ref: str
    service_ref: str
    role_ref: str
    database_ref: str

    def __post_init__(self):
        _check_plan(self, None)


def _check_plan(plan: TechnicalPlan, limits: PayloadLimits | None) -> None:
    _common(plan, limits)
    if plan.catalog_operation != "prepare_postgresql":
        raise ContractError("PA01_PLAN_OPERATION_INVALID")
    maximum = None if limits is None else limits.max_ref_bytes
    for name in ("idempotency_key", "plan_ref", "plan_version", "projection_ref",
                 "confirmation_ref", "policy_ref", "preconditions_ref",
                 "service_ref", "role_ref", "database_ref"):
        _ref(getattr(plan, name), maximum)


def _check_request(request: NativeRequest, limits: PayloadLimits | None) -> None:
    _common(request, limits)
    maximum = None if limits is None else limits.max_ref_bytes
    _ref(request.idempotency_key, maximum)
    _ref(request.mandate_ref, maximum)
    if type(request.params) is not tuple:
        raise ContractError("PA01_PARAMS_INVALID")
    for pair in request.params:
        if type(pair) is not tuple or len(pair) != 2 or type(pair[0]) is not str:
            raise ContractError("PA01_PARAMS_INVALID")
        _ref(pair[1], maximum)
    names = tuple(name for name, _ in request.params)
    if len(set(names)) != len(names) or tuple(sorted(names)) != _OPERATIONS[request.catalog_operation]:
        raise ContractError("PA01_PARAMS_FIELDS_INVALID")
    if request.catalog_operation == "prepare_postgresql":
        if _DIGEST.fullmatch(dict(request.params)["plan_digest"]) is None:
            raise ContractError("PA01_PLAN_DIGEST_INVALID")


def _check_result(result: NativeResult, limits: PayloadLimits | None) -> None:
    _common(result, limits)
    maximum = None if limits is None else limits.max_ref_bytes
    if type(result.phase) is not str or result.phase not in _PHASES:
        raise ContractError("PA01_RESULT_PHASE_INVALID")
    for value in (result.subject_operation_ref, result.result_ref, result.plan_ref,
                  result.plan_version, result.plan_digest, result.diagnostic_code):
        if value is not None:
            _ref(value, maximum)
    if type(result.observation_refs) is not tuple:
        raise ContractError("PA01_OBSERVATIONS_INVALID")
    for value in result.observation_refs:
        _ref(value, maximum)
    if len(set(result.observation_refs)) != len(result.observation_refs):
        raise ContractError("PA01_OBSERVATIONS_DUPLICATED")
    if limits is not None and len(result.observation_refs) > limits.max_observation_refs:
        raise ContractError("PA01_OBSERVATIONS_LIMIT_EXCEEDED")
    plan = (result.plan_ref, result.plan_version, result.plan_digest)
    if any(value is not None for value in plan):
        if any(value is None for value in plan) or _DIGEST.fullmatch(result.plan_digest) is None:
            raise ContractError("PA01_RESULT_PLAN_INVALID")
    if result.diagnostic_code is not None and _CODE.fullmatch(result.diagnostic_code) is None:
        raise ContractError("PA01_DIAGNOSTIC_INVALID")
    if result.phase not in ("RECEIVED", "BLOCKED") and result.result_ref is None:
        raise ContractError("PA01_DURABLE_RESULT_REFERENCE_REQUIRED")
    if result.phase == "SUCCEEDED":
        if not result.observation_refs:
            raise ContractError("PA01_POSTCONDITION_REFERENCE_REQUIRED")
        if result.catalog_operation in ("prepare_postgresql", "get_postgresql_result") and result.plan_ref is None:
            raise ContractError("PA01_RESULT_PLAN_REQUIRED")
    if result.phase in ("FAILED", "IN_DOUBT", "BLOCKED") and result.diagnostic_code is None:
        raise ContractError("PA01_DIAGNOSTIC_REQUIRED")
    if result.catalog_operation == "get_postgresql_result" and result.subject_operation_ref is None:
        raise ContractError("PA01_SUBJECT_OPERATION_REQUIRED")


def _pairs(pairs):
    data = {}
    for name, value in pairs:
        if name in data:
            raise ContractError("PA01_JSON_FIELD_DUPLICATED")
        data[name] = value
    return data


def _constant(_):
    raise ContractError("PA01_JSON_CONSTANT_INVALID")


def _decode(text: str, limits: PayloadLimits) -> dict:
    if type(limits) is not PayloadLimits or type(text) is not str:
        raise ContractError("PA01_PAYLOAD_INPUT_INVALID")
    try:
        if len(text.encode("utf-8")) > limits.max_json_bytes:
            raise ContractError("PA01_PAYLOAD_LIMIT_EXCEEDED")
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (UnicodeEncodeError, json.JSONDecodeError, RecursionError) as error:
        raise ContractError("PA01_JSON_INVALID") from error
    if type(value) is not dict:
        raise ContractError("PA01_PAYLOAD_OBJECT_REQUIRED")
    return value


def _fields(value: dict, cls) -> None:
    if set(value) != set(cls.__dataclass_fields__):
        raise ContractError("PA01_PAYLOAD_FIELDS_INVALID")


def decode_request(text: str, limits: PayloadLimits) -> NativeRequest:
    value = _decode(text, limits)
    _fields(value, NativeRequest)
    params = value["params"]
    if type(params) is not dict:
        raise ContractError("PA01_PARAMS_INVALID")
    value["params"] = tuple(sorted(params.items()))
    result = NativeRequest(**value)
    _check_request(result, limits)
    return result


def decode_result(text: str, limits: PayloadLimits) -> NativeResult:
    value = _decode(text, limits)
    _fields(value, NativeResult)
    if type(value["observation_refs"]) is not list:
        raise ContractError("PA01_OBSERVATIONS_INVALID")
    value["observation_refs"] = tuple(value["observation_refs"])
    result = NativeResult(**value)
    _check_result(result, limits)
    return result


def _encode(value: dict, limits: PayloadLimits) -> str:
    text = json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    if len(text.encode("utf-8")) > limits.max_json_bytes:
        raise ContractError("PA01_PAYLOAD_LIMIT_EXCEEDED")
    return text


def encode_request(value: NativeRequest, limits: PayloadLimits) -> str:
    if type(value) is not NativeRequest or type(limits) is not PayloadLimits:
        raise ContractError("PA01_PAYLOAD_INPUT_INVALID")
    _check_request(value, limits)
    result = asdict(value)
    result["params"] = dict(value.params)
    return _encode(result, limits)


def encode_result(value: NativeResult, limits: PayloadLimits) -> str:
    if type(value) is not NativeResult or type(limits) is not PayloadLimits:
        raise ContractError("PA01_PAYLOAD_INPUT_INVALID")
    _check_result(value, limits)
    result = asdict(value)
    result["observation_refs"] = list(value.observation_refs)
    return _encode(result, limits)


def decode_plan(text: str, limits: PayloadLimits) -> TechnicalPlan:
    value = _decode(text, limits)
    _fields(value, TechnicalPlan)
    result = TechnicalPlan(**value)
    _check_plan(result, limits)
    return result


def encode_plan(value: TechnicalPlan, limits: PayloadLimits) -> str:
    """JSON UTF-8 fermé et déterministe ; ne prétend pas qualifier un JCS général."""
    if type(value) is not TechnicalPlan or type(limits) is not PayloadLimits:
        raise ContractError("PA01_PAYLOAD_INPUT_INVALID")
    _check_plan(value, limits)
    return _encode(asdict(value), limits)


def plan_sha256(value: TechnicalPlan, limits: PayloadLimits) -> str:
    """Empreinte de corrélation du plan technique, jamais preuve d'autorisation."""
    return hashlib.sha256(encode_plan(value, limits).encode("utf-8")).hexdigest()


# E4 : ces représentations ne confèrent aucune autorité.
_MANDATE_PREFIX = b"PIXS:PA:POSTGRESQL:INITIAL:1.0.0\n"
_MANDATE_DOMAIN = "PA_POSTGRESQL_INITIAL"
_MANDATE_CLASS = {
    "inspect_postgresql": "Protégé",
    "prepare_postgresql": "Critique",
    "get_postgresql_result": "Protégé",
}
_MANDATE_REFS = ("mandate_ref", "invocation_ref", "operator_ref", "operator_key_ref",
                 "policy_ref", "policy_version", "caller_terminal_ref",
                 "executor_terminal_ref", "pzt_relation_ref", "idempotency_key")
_MANDATE_TIME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z")


@dataclass(frozen=True, slots=True)
class MandateLimits:
    payload: PayloadLimits
    max_correlation_refs: int
    max_causation_refs: int

    def __post_init__(self):
        if type(self.payload) is not PayloadLimits or any(
                type(v) is not int or v <= 0 for v in
                (self.max_correlation_refs, self.max_causation_refs)):
            raise ContractError("PA01_MANDATE_LIMITS_INVALID")


def _check_digest(value):
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        raise ContractError("PA01_MANDATE_DIGEST_INVALID")


@dataclass(frozen=True, slots=True, repr=False)
class ContentBinding:
    ref: str
    version: str
    sha256: str

    def __post_init__(self):
        _check_binding(self, None)


def _check_binding(value, maximum):
    if type(value) is not ContentBinding:
        raise ContractError("PA01_MANDATE_BINDING_INVALID")
    _ref(value.ref, maximum)
    _ref(value.version, maximum)
    _check_digest(value.sha256)


@dataclass(frozen=True, slots=True, repr=False)
class PreparationMandateClaims:
    projection_binding: ContentBinding
    plan_binding: ContentBinding
    preconditions_binding: ContentBinding
    confirmation_binding: ContentBinding
    effects_digest: str

    def __post_init__(self):
        for name in ("projection_binding", "plan_binding", "preconditions_binding",
                     "confirmation_binding"):
            _check_binding(getattr(self, name), None)
        if self.projection_binding.version != "1.0.0":
            raise ContractError("PA01_MANDATE_PROJECTION_VERSION_INVALID")
        _check_digest(self.effects_digest)


@dataclass(frozen=True, slots=True, repr=False)
class ResultMandateClaims:
    operation_ref: str

    def __post_init__(self):
        _ref(self.operation_ref)


@dataclass(frozen=True, slots=True, repr=False)
class InitialMandate:
    schema_version: str
    domain: str
    mandate_ref: str
    invocation_ref: str
    operator_ref: str
    operator_key_ref: str
    policy_ref: str
    policy_version: str
    installation_ref: str
    target_ref: str
    caller_terminal_ref: str
    executor_terminal_ref: str
    pzt_relation_ref: str
    catalog_operation: str
    catalog_version: str
    criticality: str
    operation_id: str
    idempotency_key: str
    correlation_id: str
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]
    issued_at: str
    not_before: str
    expires_at: str
    request_digest: str
    anchor_binding: ContentBinding
    claims: PreparationMandateClaims | ResultMandateClaims | None

    def __post_init__(self):
        _check_mandate(self, None)


@dataclass(frozen=True, slots=True, repr=False)
class SignedMandate:
    document: InitialMandate
    signature: bytes

    def __post_init__(self):
        if type(self.document) is not InitialMandate:
            raise ContractError("PA01_MANDATE_DOCUMENT_INVALID")
        _check_mandate(self.document, None)
        if type(self.signature) is not bytes or len(self.signature) != 64:
            raise ContractError("PA01_MANDATE_SIGNATURE_SHAPE_INVALID")


def _mandate_timestamp(value):
    if type(value) is not str or _MANDATE_TIME.fullmatch(value) is None:
        raise ContractError("PA01_MANDATE_TIMESTAMP_INVALID")
    try:
        return _datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ContractError("PA01_MANDATE_TIMESTAMP_INVALID") from error


def _check_mandate(value, limits):
    if type(value) is not InitialMandate:
        raise ContractError("PA01_MANDATE_DOCUMENT_INVALID")
    if limits is not None and type(limits) is not MandateLimits:
        raise ContractError("PA01_MANDATE_LIMITS_INVALID")
    payload = None if limits is None else limits.payload
    maximum = None if payload is None else payload.max_ref_bytes
    _common(value, payload)
    if type(value.domain) is not str or value.domain != _MANDATE_DOMAIN:
        raise ContractError("PA01_MANDATE_DOMAIN_INVALID")
    if type(value.criticality) is not str or value.criticality != _MANDATE_CLASS[value.catalog_operation]:
        raise ContractError("PA01_MANDATE_CLASS_INVALID")
    for name in _MANDATE_REFS:
        _ref(getattr(value, name), maximum)
    for name, bound in (("correlation_ids", None if limits is None else limits.max_correlation_refs),
                        ("causation_ids", None if limits is None else limits.max_causation_refs)):
        refs = getattr(value, name)
        if type(refs) is not tuple:
            raise ContractError("PA01_MANDATE_TRACE_INVALID")
        if bound is not None and len(refs) > bound:
            raise ContractError("PA01_MANDATE_TRACE_LIMIT_EXCEEDED")
        for item in refs:
            _ref(item, maximum)
    if value.correlation_id not in value.correlation_ids:
        raise ContractError("PA01_MANDATE_CORRELATION_MISMATCH")
    issued, start, expiry = (_mandate_timestamp(getattr(value, name))
                             for name in ("issued_at", "not_before", "expires_at"))
    if not issued <= start < expiry:
        raise ContractError("PA01_MANDATE_TIME_ORDER_INVALID")
    # Aucune comparaison à l'heure système : cette structure ne prouve pas la fraîcheur.
    _check_digest(value.request_digest)
    _check_binding(value.anchor_binding, maximum)
    if value.catalog_operation == "inspect_postgresql":
        if value.claims is not None:
            raise ContractError("PA01_MANDATE_CLAIMS_INVALID")
    elif value.catalog_operation == "get_postgresql_result":
        if type(value.claims) is not ResultMandateClaims:
            raise ContractError("PA01_MANDATE_CLAIMS_INVALID")
        _ref(value.claims.operation_ref, maximum)
    else:
        if type(value.claims) is not PreparationMandateClaims:
            raise ContractError("PA01_MANDATE_CLAIMS_INVALID")
        for name in ("projection_binding", "plan_binding", "preconditions_binding",
                     "confirmation_binding"):
            _check_binding(getattr(value.claims, name), maximum)
        if value.claims.projection_binding.version != "1.0.0":
            raise ContractError("PA01_MANDATE_PROJECTION_VERSION_INVALID")
        _check_digest(value.claims.effects_digest)


def _mandate_dict(value):
    result = asdict(value)
    result["correlation_ids"] = list(value.correlation_ids)
    result["causation_ids"] = list(value.causation_ids)
    if value.claims is None:
        result["claims"] = {}
    return result


def mandate_signed_bytes(value: InitialMandate, limits: MandateLimits) -> bytes:
    """Octets E4 exacts à signer/vérifier, sans clé et sans autorité."""
    if type(limits) is not MandateLimits:
        raise ContractError("PA01_MANDATE_LIMITS_INVALID")
    _check_mandate(value, limits)
    encoded = _MANDATE_PREFIX + _encode(_mandate_dict(value), limits.payload).encode("utf-8")
    if len(encoded) > limits.payload.max_json_bytes:
        raise ContractError("PA01_PAYLOAD_LIMIT_EXCEEDED")
    return encoded


def encode_signed_mandate(value: SignedMandate, limits: MandateLimits) -> str:
    if type(value) is not SignedMandate or type(limits) is not MandateLimits:
        raise ContractError("PA01_MANDATE_ENVELOPE_INVALID")
    _check_mandate(value.document, limits)
    if type(value.signature) is not bytes or len(value.signature) != 64:
        raise ContractError("PA01_MANDATE_SIGNATURE_SHAPE_INVALID")
    return _encode({"document": _mandate_dict(value.document),
                    "signature_b64": base64.b64encode(value.signature).decode("ascii")},
                   limits.payload)


def _mandate_number(_):
    raise ContractError("PA01_MANDATE_NUMBER_NOT_ALLOWED")


def _decode_mandate_payload(text, limits):
    if type(text) is not str or type(limits) is not MandateLimits:
        raise ContractError("PA01_MANDATE_PAYLOAD_INVALID")
    try:
        if len(text.encode("utf-8")) > limits.payload.max_json_bytes:
            raise ContractError("PA01_PAYLOAD_LIMIT_EXCEEDED")
        result = json.loads(text, object_pairs_hook=_pairs, parse_int=_mandate_number,
                            parse_float=_mandate_number, parse_constant=_constant)
    except (UnicodeEncodeError, json.JSONDecodeError, RecursionError) as error:
        raise ContractError("PA01_MANDATE_JSON_INVALID") from error
    if type(result) is not dict:
        raise ContractError("PA01_MANDATE_ENVELOPE_INVALID")
    return result


def _binding_from_dict(value):
    if type(value) is not dict:
        raise ContractError("PA01_MANDATE_BINDING_INVALID")
    _fields(value, ContentBinding)
    return ContentBinding(**value)


def decode_signed_mandate(text: str, limits: MandateLimits) -> SignedMandate:
    value = _decode_mandate_payload(text, limits)
    if set(value) != {"document", "signature_b64"}:
        raise ContractError("PA01_MANDATE_ENVELOPE_FIELDS_INVALID")
    document = value["document"]
    if type(document) is not dict:
        raise ContractError("PA01_MANDATE_DOCUMENT_INVALID")
    _fields(document, InitialMandate)
    for name in ("correlation_ids", "causation_ids"):
        if type(document[name]) is not list:
            raise ContractError("PA01_MANDATE_TRACE_INVALID")
        document[name] = tuple(document[name])
    document["anchor_binding"] = _binding_from_dict(document["anchor_binding"])
    claims = document["claims"]
    if type(claims) is not dict:
        raise ContractError("PA01_MANDATE_CLAIMS_INVALID")
    operation = document["catalog_operation"]
    if type(operation) is not str or operation not in _OPERATIONS:
        raise ContractError("PA01_OPERATION_NOT_DELIVERED")
    if operation == "inspect_postgresql":
        if claims:
            raise ContractError("PA01_MANDATE_CLAIMS_INVALID")
        document["claims"] = None
    elif operation == "get_postgresql_result":
        _fields(claims, ResultMandateClaims)
        document["claims"] = ResultMandateClaims(**claims)
    else:
        _fields(claims, PreparationMandateClaims)
        for name in ("projection_binding", "plan_binding", "preconditions_binding",
                     "confirmation_binding"):
            claims[name] = _binding_from_dict(claims[name])
        document["claims"] = PreparationMandateClaims(**claims)
    mandate = InitialMandate(**document)
    _check_mandate(mandate, limits)
    encoded = value["signature_b64"]
    if type(encoded) is not str or len(encoded) != 88:
        raise ContractError("PA01_MANDATE_SIGNATURE_ENCODING_INVALID")
    try:
        signature = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (ValueError, binascii.Error) as error:
        raise ContractError("PA01_MANDATE_SIGNATURE_ENCODING_INVALID") from error
    if (len(signature) != 64 or base64.b64encode(signature).decode("ascii") != encoded):
        raise ContractError("PA01_MANDATE_SIGNATURE_ENCODING_INVALID")
    return SignedMandate(mandate, signature)


def request_sha256(value: NativeRequest, limits: PayloadLimits) -> str:
    return hashlib.sha256(encode_request(value, limits).encode("utf-8")).hexdigest()


def check_mandate_request_binding(mandate: InitialMandate, request: NativeRequest,
                                 limits: MandateLimits) -> None:
    """Rapprochement structurel uniquement ; ne résout ni identité ni politique."""
    if type(limits) is not MandateLimits or type(request) is not NativeRequest:
        raise ContractError("PA01_MANDATE_BINDING_INPUT_INVALID")
    _check_mandate(mandate, limits)
    _check_request(request, limits.payload)
    for name in ("mandate_ref", "catalog_operation", "catalog_version", "operation_id",
                 "idempotency_key", "correlation_id", "installation_ref", "target_ref"):
        if getattr(mandate, name) != getattr(request, name):
            raise ContractError("PA01_MANDATE_REQUEST_MISMATCH")
    if mandate.request_digest != request_sha256(request, limits.payload):
        raise ContractError("PA01_MANDATE_REQUEST_DIGEST_MISMATCH")
    params = dict(request.params)
    if request.catalog_operation == "prepare_postgresql":
        binding = mandate.claims.plan_binding
        if (binding.ref, binding.version, binding.sha256) != (
                params["plan_ref"], params["plan_version"], params["plan_digest"]):
            raise ContractError("PA01_MANDATE_PLAN_REQUEST_MISMATCH")
    if request.catalog_operation == "get_postgresql_result":
        if mandate.claims.operation_ref != params["operation_ref"]:
            raise ContractError("PA01_MANDATE_RESULT_REQUEST_MISMATCH")


def check_mandate_plan_binding(mandate: InitialMandate, plan: TechnicalPlan,
                              limits: MandateLimits) -> None:
    """Compare un plan fourni ; aucune résolution ni postcondition n'est prouvée."""
    if type(limits) is not MandateLimits or type(plan) is not TechnicalPlan:
        raise ContractError("PA01_MANDATE_BINDING_INPUT_INVALID")
    _check_mandate(mandate, limits)
    _check_plan(plan, limits.payload)
    if mandate.catalog_operation != "prepare_postgresql":
        raise ContractError("PA01_MANDATE_PLAN_OPERATION_INVALID")
    for name in ("catalog_operation", "catalog_version", "operation_id", "idempotency_key",
                 "correlation_id", "installation_ref", "target_ref", "policy_ref"):
        if getattr(mandate, name) != getattr(plan, name):
            raise ContractError("PA01_MANDATE_PLAN_MISMATCH")
    claims = mandate.claims
    if (claims.plan_binding.ref, claims.plan_binding.version, claims.plan_binding.sha256) != (
            plan.plan_ref, plan.plan_version, plan_sha256(plan, limits.payload)):
        raise ContractError("PA01_MANDATE_PLAN_DIGEST_MISMATCH")
    if (claims.projection_binding.ref != plan.projection_ref
            or claims.confirmation_binding.ref != plan.confirmation_ref
            or claims.preconditions_binding.ref != plan.preconditions_ref):
        raise ContractError("PA01_MANDATE_PLAN_REFERENCES_MISMATCH")


__all__ += ["MandateLimits", "ContentBinding", "PreparationMandateClaims",
            "ResultMandateClaims", "InitialMandate", "SignedMandate",
            "encode_signed_mandate", "decode_signed_mandate", "mandate_signed_bytes",
            "request_sha256", "check_mandate_request_binding", "check_mandate_plan_binding"]


# Schéma public D10–D12 : forme seulement, jamais lecture TPM ou autorité.
_ANCHOR_TYPE = "pixs.agent.postgresql.anchor_snapshot/v1"
_ANCHOR_NAME = re.compile(r"000b[0-9a-f]{64}")
_ANCHOR_REFS = ("snapshot_ref", "installation_ref", "target_ref", "registry_ref",
                "registry_generation_ref", "index_ref", "owner_ref",
                "policy_ref", "policy_version")


@dataclass(frozen=True, slots=True)
class AnchorSnapshotLimits:
    payload: PayloadLimits
    max_epoch: int
    max_sequence: int

    def __post_init__(self):
        if type(self.payload) is not PayloadLimits or any(
                type(value) is not int or value < 0 for value in
                (self.max_epoch, self.max_sequence)):
            raise ContractError("PA01_ANCHOR_LIMITS_INVALID")


@dataclass(frozen=True, slots=True, repr=False)
class AnchorSnapshot:
    object_type: str
    schema_version: str
    snapshot_ref: str
    installation_ref: str
    target_ref: str
    registry_ref: str
    registry_generation_ref: str
    epoch: int
    sequence: int
    head_sha256: str
    index_ref: str
    index_name: str
    nv_value_sha256: str
    owner_ref: str
    policy_ref: str
    policy_version: str
    observed_at: str

    def __post_init__(self):
        _check_anchor_snapshot(self, None)


def _check_anchor_snapshot(value, limits):
    if type(value) is not AnchorSnapshot:
        raise ContractError("PA01_ANCHOR_SNAPSHOT_INVALID")
    if limits is not None and type(limits) is not AnchorSnapshotLimits:
        raise ContractError("PA01_ANCHOR_LIMITS_INVALID")
    if (type(value.object_type) is not str or value.object_type != _ANCHOR_TYPE
            or type(value.schema_version) is not str or value.schema_version != "1.0.0"):
        raise ContractError("PA01_ANCHOR_SCHEMA_INVALID")
    maximum = None if limits is None else limits.payload.max_ref_bytes
    for name in _ANCHOR_REFS:
        _ref(getattr(value, name), maximum)
    for name in ("epoch", "sequence"):
        number = getattr(value, name)
        if type(number) is not int or number < 0:
            raise ContractError("PA01_ANCHOR_NUMBER_INVALID")
        if limits is not None and number > getattr(limits, "max_" + name):
            raise ContractError("PA01_ANCHOR_NUMBER_LIMIT_EXCEEDED")
    _check_digest(value.head_sha256)
    _check_digest(value.nv_value_sha256)
    if type(value.index_name) is not str or _ANCHOR_NAME.fullmatch(value.index_name) is None:
        raise ContractError("PA01_ANCHOR_INDEX_NAME_INVALID")
    _mandate_timestamp(value.observed_at)


def encode_anchor_snapshot(value: AnchorSnapshot, limits: AnchorSnapshotLimits) -> str:
    """Sérialise des données publiques, sans constater leur provenance."""
    if type(limits) is not AnchorSnapshotLimits:
        raise ContractError("PA01_ANCHOR_LIMITS_INVALID")
    _check_anchor_snapshot(value, limits)
    return _encode(asdict(value), limits.payload)


def decode_anchor_snapshot(text: str, limits: AnchorSnapshotLimits) -> AnchorSnapshot:
    if type(text) is not str or type(limits) is not AnchorSnapshotLimits:
        raise ContractError("PA01_ANCHOR_PAYLOAD_INVALID")

    def integer(token):
        if token.startswith("-"):
            raise ContractError("PA01_ANCHOR_NUMBER_INVALID")
        try:
            value = int(token)
        except ValueError as error:
            raise ContractError("PA01_ANCHOR_NUMBER_INVALID") from error
        if value > max(limits.max_epoch, limits.max_sequence):
            raise ContractError("PA01_ANCHOR_NUMBER_LIMIT_EXCEEDED")
        return value

    def noninteger(_token):
        raise ContractError("PA01_ANCHOR_NUMBER_INVALID")

    try:
        if len(text.encode("utf-8")) > limits.payload.max_json_bytes:
            raise ContractError("PA01_PAYLOAD_LIMIT_EXCEEDED")
        value = json.loads(text, object_pairs_hook=_pairs, parse_int=integer,
                           parse_float=noninteger, parse_constant=_constant)
    except (UnicodeEncodeError, json.JSONDecodeError, RecursionError) as error:
        raise ContractError("PA01_ANCHOR_JSON_INVALID") from error
    if type(value) is not dict:
        raise ContractError("PA01_ANCHOR_SNAPSHOT_INVALID")
    _fields(value, AnchorSnapshot)
    snapshot = AnchorSnapshot(**value)
    _check_anchor_snapshot(snapshot, limits)
    return snapshot


def anchor_snapshot_sha256(value: AnchorSnapshot, limits: AnchorSnapshotLimits) -> str:
    return hashlib.sha256(encode_anchor_snapshot(value, limits).encode("utf-8")).hexdigest()


def check_mandate_anchor_binding(mandate: InitialMandate, snapshot: AnchorSnapshot,
                                mandate_limits: MandateLimits,
                                snapshot_limits: AnchorSnapshotLimits) -> None:
    """Compare des DTO ; ne lit ni TPM, journal, politique ou horloge.

    L'admission doit résoudre un instantané courant authentifié et vérifier
    toutes ses preuves. Après consommation, la progression propre au mandat
    doit être réconciliée dans le registre ; cette aide ne gère pas ce cycle.
    """
    if type(mandate_limits) is not MandateLimits or type(snapshot_limits) is not AnchorSnapshotLimits:
        raise ContractError("PA01_ANCHOR_BINDING_INPUT_INVALID")
    _check_mandate(mandate, mandate_limits)
    _check_anchor_snapshot(snapshot, snapshot_limits)
    for name in ("installation_ref", "target_ref", "policy_ref", "policy_version"):
        if getattr(mandate, name) != getattr(snapshot, name):
            raise ContractError("PA01_ANCHOR_CONTEXT_MISMATCH")
    binding = mandate.anchor_binding
    if (binding.ref, binding.version, binding.sha256) != (
            snapshot.snapshot_ref, "1.0.0", anchor_snapshot_sha256(snapshot, snapshot_limits)):
        raise ContractError("PA01_ANCHOR_BINDING_MISMATCH")


__all__ += ["AnchorSnapshotLimits", "AnchorSnapshot", "encode_anchor_snapshot",
            "decode_anchor_snapshot", "anchor_snapshot_sha256", "check_mandate_anchor_binding"]


# Journal structurel D10 : forme seulement, jamais intention durable, preuve, ancrage, IO ou autorite.
_JOURNAL_TYPE = "pixs.agent.postgresql.journal_transition/v1"
_JOURNAL_PREFIX = b"PIXS:PA:POSTGRESQL:JOURNAL:1.0.0\n"
_JOURNAL_STATES = frozenset(("INTENT", "OBSERVED", "RESULT", "RETIRED"))
_JOURNAL_REFS = ("transition_ref", "installation_ref", "target_ref", "registry_ref",
                "registry_generation_ref", "operation_ref")
_JOURNAL_UINT64_MAX = 2 ** 64 - 1


@dataclass(frozen=True, slots=True)
class JournalLimits:
    payload: PayloadLimits
    max_epoch: int
    max_sequence: int
    max_correlation_refs: int
    max_causation_refs: int

    def __post_init__(self):
        _check_journal_limits(self)


@dataclass(frozen=True, slots=True, repr=False)
class JournalTransition:
    object_type: str
    schema_version: str
    transition_ref: str
    installation_ref: str
    target_ref: str
    registry_ref: str
    registry_generation_ref: str
    epoch: int
    sequence: int
    previous_head_sha256: str
    previous_nv_value_sha256: str
    state: str
    operation_ref: str
    mandate_binding: ContentBinding
    content_binding: ContentBinding
    correlation_refs: tuple[str, ...]
    causation_refs: tuple[str, ...]

    def __post_init__(self):
        _check_journal_transition(self, None)


def _check_journal_limits(value):
    if type(value) is not JournalLimits:
        raise ContractError("PA01_JOURNAL_LIMITS_INVALID")
    if type(value.payload) is not PayloadLimits:
        raise ContractError("PA01_JOURNAL_LIMITS_INVALID")
    for name in ("max_epoch", "max_sequence"):
        bound = getattr(value, name)
        if type(bound) is not int or bound < 0 or bound > _JOURNAL_UINT64_MAX:
            raise ContractError("PA01_JOURNAL_LIMITS_INVALID")
    for name in ("max_correlation_refs", "max_causation_refs"):
        bound = getattr(value, name)
        if type(bound) is not int or bound <= 0:
            raise ContractError("PA01_JOURNAL_LIMITS_INVALID")


def _check_journal_transition(value, limits):
    if type(value) is not JournalTransition:
        raise ContractError("PA01_JOURNAL_TRANSITION_INVALID")
    if limits is not None and type(limits) is not JournalLimits:
        raise ContractError("PA01_JOURNAL_LIMITS_INVALID")
    if type(value.object_type) is not str or value.object_type != _JOURNAL_TYPE:
        raise ContractError("PA01_JOURNAL_SCHEMA_INVALID")
    if type(value.schema_version) is not str or value.schema_version != "1.0.0":
        raise ContractError("PA01_JOURNAL_SCHEMA_INVALID")
    maximum = None if limits is None else limits.payload.max_ref_bytes
    for name in _JOURNAL_REFS:
        _ref(getattr(value, name), maximum)
    for name, cap in (("epoch", None if limits is None else limits.max_epoch),
                      ("sequence", None if limits is None else limits.max_sequence)):
        number = getattr(value, name)
        if type(number) is not int or number < 0 or number > _JOURNAL_UINT64_MAX:
            raise ContractError("PA01_JOURNAL_NUMBER_INVALID")
        if cap is not None and number > cap:
            raise ContractError("PA01_JOURNAL_NUMBER_LIMIT_EXCEEDED")
    _check_digest(value.previous_head_sha256)
    _check_digest(value.previous_nv_value_sha256)
    if type(value.state) is not str or value.state not in _JOURNAL_STATES:
        raise ContractError("PA01_JOURNAL_STATE_INVALID")
    _check_binding(value.mandate_binding, maximum)
    _check_binding(value.content_binding, maximum)
    for name, cap in (("correlation_refs", None if limits is None else limits.max_correlation_refs),
                      ("causation_refs", None if limits is None else limits.max_causation_refs)):
        refs = getattr(value, name)
        if type(refs) is not tuple:
            raise ContractError("PA01_JOURNAL_TRACE_INVALID")
        if cap is not None and len(refs) > cap:
            raise ContractError("PA01_JOURNAL_TRACE_LIMIT_EXCEEDED")
        for item in refs:
            _ref(item, maximum)


def encode_journal_transition(value: JournalTransition, limits: JournalLimits) -> str:
    if type(limits) is not JournalLimits:
        raise ContractError("PA01_JOURNAL_LIMITS_INVALID")
    _check_journal_transition(value, limits)
    result = asdict(value)
    result["correlation_refs"] = list(value.correlation_refs)
    result["causation_refs"] = list(value.causation_refs)
    return _encode(result, limits.payload)


def decode_journal_transition(text: str, limits: JournalLimits) -> JournalTransition:
    if type(text) is not str or type(limits) is not JournalLimits:
        raise ContractError("PA01_JOURNAL_PAYLOAD_INVALID")

    def integer(token):
        if token.startswith("-"):
            raise ContractError("PA01_JOURNAL_NUMBER_INVALID")
        try:
            number = int(token)
        except ValueError as error:
            raise ContractError("PA01_JOURNAL_NUMBER_INVALID") from error
        if number > max(limits.max_epoch, limits.max_sequence):
            raise ContractError("PA01_JOURNAL_NUMBER_LIMIT_EXCEEDED")
        return number

    def noninteger(_token):
        raise ContractError("PA01_JOURNAL_NUMBER_INVALID")
    try:
        if len(text.encode("utf-8")) > limits.payload.max_json_bytes:
            raise ContractError("PA01_PAYLOAD_LIMIT_EXCEEDED")
        value = json.loads(text, object_pairs_hook=_pairs, parse_int=integer,
                           parse_float=noninteger, parse_constant=_constant)
    except (UnicodeEncodeError, json.JSONDecodeError, RecursionError) as error:
        raise ContractError("PA01_JOURNAL_JSON_INVALID") from error
    if type(value) is not dict:
        raise ContractError("PA01_JOURNAL_TRANSITION_INVALID")
    _fields(value, JournalTransition)
    for name in ("correlation_refs", "causation_refs"):
        if type(value[name]) is not list:
            raise ContractError("PA01_JOURNAL_TRACE_INVALID")
        value[name] = tuple(value[name])
    for name in ("mandate_binding", "content_binding"):
        binding = value[name]
        if type(binding) is not dict:
            raise ContractError("PA01_JOURNAL_BINDING_INVALID")
        _fields(binding, ContentBinding)
        value[name] = ContentBinding(**binding)
    result = JournalTransition(**value)
    _check_journal_transition(result, limits)
    return result


def journal_transition_head_sha256(value: JournalTransition, limits: JournalLimits) -> str:
    _check_journal_transition(value, limits)
    return hashlib.sha256(_JOURNAL_PREFIX + encode_journal_transition(value, limits).encode("utf-8")).hexdigest()


def journal_expected_nv_sha256(value: JournalTransition, limits: JournalLimits) -> str:
    _check_journal_transition(value, limits)
    try:
        old = binascii.unhexlify(value.previous_nv_value_sha256.encode("ascii"))
        head = binascii.unhexlify(journal_transition_head_sha256(value, limits).encode("ascii"))
    except (ValueError, binascii.Error) as error:
        raise ContractError("PA01_JOURNAL_DIGEST_INVALID") from error
    if len(old) != 32 or len(head) != 32:
        raise ContractError("PA01_JOURNAL_DIGEST_INVALID")
    return hashlib.sha256(old + head).hexdigest()


__all__ += ["JournalLimits", "JournalTransition", "encode_journal_transition",
            "decode_journal_transition", "journal_transition_head_sha256",
            "journal_expected_nv_sha256"]
