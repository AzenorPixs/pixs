"""Contrats administratifs retrait/inspection PA : structure seulement.

Famille PA_POSTGRESQL_WITHDRAWAL, ops withdraw_initial_authority (Critique)
et inspect_initial_authority (Protégé). Structural only : aucune identité,
autorisation, confirmation, durabilité, fraîcheur, révocation ou effet
n'est prouvé par ces DTO. Vérificateur et propriétaires serveur requis.
"""

from __future__ import annotations

from dataclasses import dataclass
import base64
import binascii
import datetime as _datetime
import hashlib
import json
import re

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, MandateLimits, PayloadLimits
elif __package__ in (None, ""):
    import sys as _pa01_sys
    if "postgresql_contracts" not in _pa01_sys.builtin_module_names:
        raise ImportError("PA01_ADMIN_CODEC_PG_BUILTIN_MISSING")
    import postgresql_contracts as _pa01_flat_pg
    ContentBinding = _pa01_flat_pg.ContentBinding
    MandateLimits = _pa01_flat_pg.MandateLimits
    PayloadLimits = _pa01_flat_pg.PayloadLimits
else:
    raise ImportError("PA01_ADMIN_CODEC_CONTEXT_REFUSED")

__all__ = [
    "AdminContractError",
    "WithdrawalClaims",
    "AdminRequest",
    "AdminMandate",
    "SignedAdminMandate",
    "AdminResult",
    "encode_admin_request",
    "decode_admin_request",
    "encode_admin_mandate",
    "decode_admin_mandate",
    "admin_signed_bytes",
    "encode_signed_admin_mandate",
    "decode_signed_admin_mandate",
    "match_admin_request_mandate",
    "encode_admin_result",
    "decode_admin_result",
    "match_admin_result_request",
]

_ADMIN_DOMAIN = "PA_POSTGRESQL_WITHDRAWAL"
_ADMIN_CLASS = {
    "withdraw_initial_authority": "Critique",
    "inspect_initial_authority": "Protégé",
}
_ADMIN_WITHDRAWAL_PREFIX = b"PIXS:PA:WITHDRAWAL:MANDATE:1.0.0\n"
_ADMIN_INSPECTION_PREFIX = b"PIXS:PA:INSPECTION:MANDATE:1.0.0\n"
_ADMIN_DIGEST = re.compile(r"[0-9a-f]{64}")
_ADMIN_TIME = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z"
)
_ADMIN_REQUEST_REFS = (
    "operation_id",
    "idempotency_key",
    "correlation_id",
    "installation_ref",
    "target_ref",
    "mandate_ref",
)
_ADMIN_MANDATE_REFS = (
    "mandate_ref",
    "invocation_ref",
    "operator_ref",
    "operator_key_ref",
    "policy_ref",
    "policy_version",
    "installation_ref",
    "target_ref",
    "caller_terminal_ref",
    "executor_terminal_ref",
    "pzt_relation_ref",
    "operation_id",
    "idempotency_key",
    "correlation_id",
)


class AdminContractError(ValueError):
    """Diagnostic stable sans contenu reçu."""


def _admin_ref(value: object, maximum: int | None) -> None:
    if type(value) is not str or not value:
        raise AdminContractError("PAWD_REFERENCE_INVALID")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise AdminContractError("PAWD_REFERENCE_INVALID")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise AdminContractError("PAWD_REFERENCE_UTF8_INVALID") from error
    if maximum is not None and size > maximum:
        raise AdminContractError("PAWD_REFERENCE_LIMIT_EXCEEDED")


def _admin_digest(value: object) -> None:
    if type(value) is not str or _ADMIN_DIGEST.fullmatch(value) is None:
        raise AdminContractError("PAWD_DIGEST_INVALID")


def _admin_timestamp(value: object) -> _datetime.datetime:
    if type(value) is not str or _ADMIN_TIME.fullmatch(value) is None:
        raise AdminContractError("PAWD_TIMESTAMP_INVALID")
    try:
        return _datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise AdminContractError("PAWD_TIMESTAMP_INVALID") from error


def _admin_number(_: object) -> object:
    raise AdminContractError("PAWD_NUMBER_NOT_ALLOWED")


def _admin_constant(_: object) -> object:
    raise AdminContractError("PAWD_CONSTANT_INVALID")


def _admin_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    data: dict[str, object] = {}
    for name, item in pairs:
        if name in data:
            raise AdminContractError("PAWD_FIELD_DUPLICATED")
        data[name] = item
    return data


def _admin_decode_json(text: object, max_bytes: int) -> dict[str, object]:
    if type(text) is not str or type(max_bytes) is not int:
        raise AdminContractError("PAWD_PAYLOAD_INPUT_INVALID")
    try:
        if len(text.encode("utf-8")) > max_bytes:
            raise AdminContractError("PAWD_PAYLOAD_LIMIT_EXCEEDED")
        value = json.loads(
            text,
            object_pairs_hook=_admin_pairs,
            parse_int=_admin_number,
            parse_float=_admin_number,
            parse_constant=_admin_constant,
        )
    except (UnicodeEncodeError, json.JSONDecodeError, RecursionError) as error:
        raise AdminContractError("PAWD_JSON_INVALID") from error
    if type(value) is not dict:
        raise AdminContractError("PAWD_OBJECT_REQUIRED")
    return value


def _admin_encode(obj: dict[str, object], max_bytes: int) -> str:
    text = json.dumps(
        obj, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )
    if len(text.encode("utf-8")) > max_bytes:
        raise AdminContractError("PAWD_PAYLOAD_LIMIT_EXCEEDED")
    return text


def _admin_fields(value: dict[str, object], names: set[str]) -> None:
    if set(value) != names:
        raise AdminContractError("PAWD_FIELDS_INVALID")


def _admin_check_binding(value: object, maximum: int | None) -> None:
    if type(value) is not ContentBinding:
        raise AdminContractError("PAWD_BINDING_INVALID")
    _admin_ref(value.ref, maximum)
    _admin_ref(value.version, maximum)
    _admin_digest(value.sha256)


def _binding_from_dict(value: object) -> ContentBinding:
    """Construit le ContentBinding public importé, forme seulement.

    Chaque champ est validé localement (type, UTF-8, digest) avant toute
    construction. Si le constructeur importé refuse malgré tout, seule
    l'erreur de valeur précise est transformée en AdminContractError en
    préservant la cause, sans masquer les erreurs inattendues et sans
    appeler de validateur PG.
    """
    if type(value) is not dict:
        raise AdminContractError("PAWD_BINDING_INVALID")
    _admin_fields(value, {"ref", "version", "sha256"})
    ref = value["ref"]
    version = value["version"]
    digest = value["sha256"]
    if type(ref) is not str or type(version) is not str:
        raise AdminContractError("PAWD_BINDING_INVALID")
    _admin_ref(ref, None)
    _admin_ref(version, None)
    _admin_digest(digest)
    try:
        return ContentBinding(ref=ref, version=version, sha256=digest)
    except ValueError as error:
        raise AdminContractError("PAWD_BINDING_INVALID") from error

def _binding_to_dict(value: ContentBinding) -> dict[str, object]:
    return {"ref": value.ref, "version": value.version, "sha256": value.sha256}


@dataclass(frozen=True, slots=True, repr=False)
class WithdrawalClaims:
    plan_binding: ContentBinding
    confirmation_binding: ContentBinding
    proofs_binding: ContentBinding

    def __post_init__(self) -> None:
        _admin_check_binding(self.plan_binding, None)
        _admin_check_binding(self.confirmation_binding, None)
        _admin_check_binding(self.proofs_binding, None)


@dataclass(frozen=True, slots=True, repr=False)
class AdminRequest:
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

    def __post_init__(self) -> None:
        _check_admin_request(self, None)


@dataclass(frozen=True, slots=True, repr=False)
class AdminMandate:
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
    anchor_binding: ContentBinding | None
    claims: WithdrawalClaims | None

    def __post_init__(self) -> None:
        _check_admin_mandate(self, None)


@dataclass(frozen=True, slots=True, repr=False)
class SignedAdminMandate:
    document: AdminMandate
    signature: bytes

    def __post_init__(self) -> None:
        if type(self.document) is not AdminMandate:
            raise AdminContractError("PAWD_DOCUMENT_INVALID")
        _check_admin_mandate(self.document, None)
        if type(self.signature) is not bytes or len(self.signature) != 64:
            raise AdminContractError("PAWD_SIGNATURE_SHAPE_INVALID")


def _check_admin_request(value: AdminRequest, limits: PayloadLimits | None) -> None:
    if type(value) is not AdminRequest:
        raise AdminContractError("PAWD_REQUEST_INVALID")
    if limits is not None and type(limits) is not PayloadLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    if (
        type(value.schema_version) is not str
        or value.schema_version != "1.0.0"
        or type(value.catalog_version) is not str
        or value.catalog_version != "1.0.0"
    ):
        raise AdminContractError("PAWD_VERSION_INVALID")
    if type(value.catalog_operation) is not str or value.catalog_operation not in _ADMIN_CLASS:
        raise AdminContractError("PAWD_OPERATION_INVALID")
    maximum = None if limits is None else limits.max_ref_bytes
    for name in _ADMIN_REQUEST_REFS:
        _admin_ref(getattr(value, name), maximum)
    if type(value.params) is not tuple:
        raise AdminContractError("PAWD_PARAMS_INVALID")
    for pair in value.params:
        if type(pair) is not tuple or len(pair) != 2:
            raise AdminContractError("PAWD_PARAMS_INVALID")
        if type(pair[0]) is not str:
            raise AdminContractError("PAWD_PARAMS_INVALID")
        _admin_ref(pair[1], maximum)
    names = tuple(name for name, _ in value.params)
    if len(set(names)) != len(names) or names != tuple(sorted(names)):
        raise AdminContractError("PAWD_PARAMS_INVALID")
    if value.catalog_operation == "withdraw_initial_authority":
        if names != ():
            raise AdminContractError("PAWD_PARAMS_FIELDS_INVALID")
    else:
        if names != () and names != ("subject_operation_ref",):
            raise AdminContractError("PAWD_PARAMS_FIELDS_INVALID")


def _check_admin_mandate(value: AdminMandate, limits: MandateLimits | None) -> None:
    if type(value) is not AdminMandate:
        raise AdminContractError("PAWD_DOCUMENT_INVALID")
    if limits is not None and type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    payload = None if limits is None else limits.payload
    if payload is not None and type(payload) is not PayloadLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    maximum = None if payload is None else payload.max_ref_bytes
    if (
        type(value.schema_version) is not str
        or value.schema_version != "1.0.0"
        or type(value.catalog_version) is not str
        or value.catalog_version != "1.0.0"
    ):
        raise AdminContractError("PAWD_VERSION_INVALID")
    if type(value.catalog_operation) is not str or value.catalog_operation not in _ADMIN_CLASS:
        raise AdminContractError("PAWD_OPERATION_INVALID")
    if type(value.domain) is not str or value.domain != _ADMIN_DOMAIN:
        raise AdminContractError("PAWD_DOMAIN_INVALID")
    if (
        type(value.criticality) is not str
        or value.criticality != _ADMIN_CLASS[value.catalog_operation]
    ):
        raise AdminContractError("PAWD_CLASS_INVALID")
    for name in _ADMIN_MANDATE_REFS:
        _admin_ref(getattr(value, name), maximum)
    for name, bound in (
        ("correlation_ids", None if limits is None else limits.max_correlation_refs),
        ("causation_ids", None if limits is None else limits.max_causation_refs),
    ):
        refs = getattr(value, name)
        if type(refs) is not tuple:
            raise AdminContractError("PAWD_TRACE_INVALID")
        if bound is not None and len(refs) > bound:
            raise AdminContractError("PAWD_TRACE_LIMIT_EXCEEDED")
        for item in refs:
            _admin_ref(item, maximum)
    if value.correlation_id not in value.correlation_ids:
        raise AdminContractError("PAWD_CORRELATION_MISMATCH")
    issued = _admin_timestamp(value.issued_at)
    start = _admin_timestamp(value.not_before)
    expiry = _admin_timestamp(value.expires_at)
    if not issued <= start < expiry:
        raise AdminContractError("PAWD_TIME_ORDER_INVALID")
    _admin_digest(value.request_digest)
    if value.catalog_operation == "withdraw_initial_authority":
        if type(value.anchor_binding) is not ContentBinding:
            raise AdminContractError("PAWD_ANCHOR_REQUIRED")
        _admin_check_binding(value.anchor_binding, maximum)
        if type(value.claims) is not WithdrawalClaims:
            raise AdminContractError("PAWD_CLAIMS_INVALID")
        _admin_check_binding(value.claims.plan_binding, maximum)
        _admin_check_binding(value.claims.confirmation_binding, maximum)
        _admin_check_binding(value.claims.proofs_binding, maximum)
    else:
        if value.anchor_binding is not None:
            raise AdminContractError("PAWD_ANCHOR_MUST_BE_NULL")
        if value.claims is not None:
            raise AdminContractError("PAWD_CLAIMS_MUST_BE_NULL")


def _admin_request_to_dict(value: AdminRequest) -> dict[str, object]:
    return {
        "schema_version": value.schema_version,
        "catalog_operation": value.catalog_operation,
        "catalog_version": value.catalog_version,
        "operation_id": value.operation_id,
        "idempotency_key": value.idempotency_key,
        "correlation_id": value.correlation_id,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "mandate_ref": value.mandate_ref,
        "params": {name: item for name, item in value.params},
    }


def _admin_claims_to_dict(value: WithdrawalClaims) -> dict[str, object]:
    return {
        "plan_binding": _binding_to_dict(value.plan_binding),
        "confirmation_binding": _binding_to_dict(value.confirmation_binding),
        "proofs_binding": _binding_to_dict(value.proofs_binding),
    }


def _admin_claims_from_dict(value: object) -> WithdrawalClaims:
    if type(value) is not dict:
        raise AdminContractError("PAWD_CLAIMS_INVALID")
    _admin_fields(value, {"plan_binding", "confirmation_binding", "proofs_binding"})
    return WithdrawalClaims(
        plan_binding=_binding_from_dict(value["plan_binding"]),
        confirmation_binding=_binding_from_dict(value["confirmation_binding"]),
        proofs_binding=_binding_from_dict(value["proofs_binding"]),
    )


def _admin_mandate_to_dict(value: AdminMandate) -> dict[str, object]:
    if value.anchor_binding is None:
        anchor: dict[str, object] | None = None
    else:
        anchor = _binding_to_dict(value.anchor_binding)
    if value.claims is None:
        claims: dict[str, object] | None = None
    else:
        claims = _admin_claims_to_dict(value.claims)
    return {
        "schema_version": value.schema_version,
        "domain": value.domain,
        "mandate_ref": value.mandate_ref,
        "invocation_ref": value.invocation_ref,
        "operator_ref": value.operator_ref,
        "operator_key_ref": value.operator_key_ref,
        "policy_ref": value.policy_ref,
        "policy_version": value.policy_version,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "caller_terminal_ref": value.caller_terminal_ref,
        "executor_terminal_ref": value.executor_terminal_ref,
        "pzt_relation_ref": value.pzt_relation_ref,
        "catalog_operation": value.catalog_operation,
        "catalog_version": value.catalog_version,
        "criticality": value.criticality,
        "operation_id": value.operation_id,
        "idempotency_key": value.idempotency_key,
        "correlation_id": value.correlation_id,
        "correlation_ids": list(value.correlation_ids),
        "causation_ids": list(value.causation_ids),
        "issued_at": value.issued_at,
        "not_before": value.not_before,
        "expires_at": value.expires_at,
        "request_digest": value.request_digest,
        "anchor_binding": anchor,
        "claims": claims,
    }


def encode_admin_request(value: AdminRequest, limits: PayloadLimits) -> str:
    if type(value) is not AdminRequest or type(limits) is not PayloadLimits:
        raise AdminContractError("PAWD_INPUT_INVALID")
    _check_admin_request(value, limits)
    return _admin_encode(_admin_request_to_dict(value), limits.max_json_bytes)


def decode_admin_request(text: str, limits: PayloadLimits) -> AdminRequest:
    if type(limits) is not PayloadLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    value = _admin_decode_json(text, limits.max_json_bytes)
    _admin_fields(value, set(AdminRequest.__dataclass_fields__))
    params = value["params"]
    if type(params) is not dict:
        raise AdminContractError("PAWD_PARAMS_INVALID")
    value["params"] = tuple(sorted(params.items()))
    result = AdminRequest(**value)  # type: ignore[arg-type]
    _check_admin_request(result, limits)
    return result


def encode_admin_mandate(value: AdminMandate, limits: MandateLimits) -> str:
    if type(value) is not AdminMandate or type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_INPUT_INVALID")
    _check_admin_mandate(value, limits)
    return _admin_encode(_admin_mandate_to_dict(value), limits.payload.max_json_bytes)


def decode_admin_mandate(text: str, limits: MandateLimits) -> AdminMandate:
    if type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    value = _admin_decode_json(text, limits.payload.max_json_bytes)
    _admin_fields(value, set(AdminMandate.__dataclass_fields__))
    for name in ("correlation_ids", "causation_ids"):
        if type(value[name]) is not list:
            raise AdminContractError("PAWD_TRACE_INVALID")
        value[name] = tuple(value[name])
    anchor = value["anchor_binding"]
    if anchor is None:
        value["anchor_binding"] = None
    else:
        value["anchor_binding"] = _binding_from_dict(anchor)
    claims = value["claims"]
    if claims is None:
        value["claims"] = None
    else:
        value["claims"] = _admin_claims_from_dict(claims)
    result = AdminMandate(**value)  # type: ignore[arg-type]
    _check_admin_mandate(result, limits)
    return result


def admin_signed_bytes(value: AdminMandate, limits: MandateLimits) -> bytes:
    if type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    _check_admin_mandate(value, limits)
    if value.catalog_operation == "withdraw_initial_authority":
        prefix = _ADMIN_WITHDRAWAL_PREFIX
    else:
        prefix = _ADMIN_INSPECTION_PREFIX
    encoded = prefix + encode_admin_mandate(value, limits).encode("utf-8")
    if len(encoded) > limits.payload.max_json_bytes:
        raise AdminContractError("PAWD_PAYLOAD_LIMIT_EXCEEDED")
    return encoded


def encode_signed_admin_mandate(
    value: SignedAdminMandate, limits: MandateLimits
) -> str:
    if type(value) is not SignedAdminMandate or type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_ENVELOPE_INVALID")
    _check_admin_mandate(value.document, limits)
    if type(value.signature) is not bytes or len(value.signature) != 64:
        raise AdminContractError("PAWD_SIGNATURE_SHAPE_INVALID")
    return _admin_encode(
        {
            "document": _admin_mandate_to_dict(value.document),
            "signature_b64": base64.b64encode(value.signature).decode("ascii"),
        },
        limits.payload.max_json_bytes,
    )


def decode_signed_admin_mandate(
    text: str, limits: MandateLimits
) -> SignedAdminMandate:
    if type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    value = _admin_decode_json(text, limits.payload.max_json_bytes)
    if set(value) != {"document", "signature_b64"}:
        raise AdminContractError("PAWD_ENVELOPE_FIELDS_INVALID")
    document = value["document"]
    if type(document) is not dict:
        raise AdminContractError("PAWD_DOCUMENT_INVALID")
    _admin_fields(document, set(AdminMandate.__dataclass_fields__))
    for name in ("correlation_ids", "causation_ids"):
        if type(document[name]) is not list:
            raise AdminContractError("PAWD_TRACE_INVALID")
        document[name] = tuple(document[name])
    anchor = document["anchor_binding"]
    if anchor is None:
        document["anchor_binding"] = None
    else:
        document["anchor_binding"] = _binding_from_dict(anchor)
    claims = document["claims"]
    if claims is None:
        document["claims"] = None
    else:
        document["claims"] = _admin_claims_from_dict(claims)
    mandate = AdminMandate(**document)
    _check_admin_mandate(mandate, limits)
    encoded = value["signature_b64"]
    if type(encoded) is not str or len(encoded) != 88:
        raise AdminContractError("PAWD_SIGNATURE_ENCODING_INVALID")
    try:
        signature = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (ValueError, binascii.Error) as error:
        raise AdminContractError("PAWD_SIGNATURE_ENCODING_INVALID") from error
    if len(signature) != 64:
        raise AdminContractError("PAWD_SIGNATURE_ENCODING_INVALID")
    if base64.b64encode(signature).decode("ascii") != encoded:
        raise AdminContractError("PAWD_SIGNATURE_ENCODING_INVALID")
    return SignedAdminMandate(mandate, signature)


def match_admin_request_mandate(
    request: AdminRequest, mandate: AdminMandate, limits: MandateLimits
) -> None:
    if (
        type(request) is not AdminRequest
        or type(mandate) is not AdminMandate
        or type(limits) is not MandateLimits
    ):
        raise AdminContractError("PAWD_BINDING_INPUT_INVALID")
    _check_admin_request(request, limits.payload)
    _check_admin_mandate(mandate, limits)
    for name in (
        "mandate_ref",
        "catalog_operation",
        "catalog_version",
        "operation_id",
        "idempotency_key",
        "correlation_id",
        "installation_ref",
        "target_ref",
    ):
        if getattr(mandate, name) != getattr(request, name):
            raise AdminContractError("PAWD_REQUEST_MISMATCH")
    expected = hashlib.sha256(
        encode_admin_request(request, limits.payload).encode("utf-8")
    ).hexdigest()
    if mandate.request_digest != expected:
        raise AdminContractError("PAWD_REQUEST_DIGEST_MISMATCH")


_ADMIN_RESULT_PHASES = frozenset(("RECEIVED", "RUNNING", "SUCCEEDED", "FAILED", "IN_DOUBT", "BLOCKED"))
_ADMIN_OBSERVED = frozenset(("UNKNOWN", "UNAVAILABLE", "NON_OBSERVABLE", "INITIAL_ACTIVE", "PENDING", "WITHDRAWN_DECLARED"))
_ADMIN_SUBJECT = frozenset(("UNKNOWN", "NOT_WITHDRAWN", "WITHDRAWN_DECLARED", "FAILED", "IN_DOUBT", "BLOCKED"))
_ADMIN_DIAG = re.compile(r"[A-Z][A-Z0-9_]*")


@dataclass(frozen=True, slots=True, repr=False)
class AdminResult:
    schema_version: str
    catalog_operation: str
    catalog_version: str
    operation_id: str
    subject_operation_ref: str | None
    invocation_ref: str
    correlation_id: str
    correlation_ids: tuple[str, ...]
    causation_ids: tuple[str, ...]
    installation_ref: str
    target_ref: str
    mandate_ref: str
    phase: str
    observed_state: str
    subject_outcome: str | None
    observed_at: str | None
    proof_bindings: tuple[ContentBinding, ...]
    diagnostic_code: str | None

    def __post_init__(self) -> None:
        _check_admin_result(self, None)


def _check_admin_result(value: AdminResult, limits: MandateLimits | None) -> None:
    if type(value) is not AdminResult:
        raise AdminContractError("PAWD_RESULT_INVALID")
    if limits is not None and type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    payload = None if limits is None else limits.payload
    if payload is not None and type(payload) is not PayloadLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    maximum = None if payload is None else payload.max_ref_bytes
    if type(value.schema_version) is not str or value.schema_version != "1.0.0" or type(value.catalog_version) is not str or value.catalog_version != "1.0.0":
        raise AdminContractError("PAWD_VERSION_INVALID")
    if type(value.catalog_operation) is not str or value.catalog_operation not in _ADMIN_CLASS:
        raise AdminContractError("PAWD_OPERATION_INVALID")
    for name in ("operation_id", "invocation_ref", "correlation_id", "installation_ref", "target_ref", "mandate_ref"):
        _admin_ref(getattr(value, name), maximum)
    if value.subject_operation_ref is not None:
        _admin_ref(value.subject_operation_ref, maximum)
    for name, bound in (("correlation_ids", None if limits is None else limits.max_correlation_refs), ("causation_ids", None if limits is None else limits.max_causation_refs)):
        refs = getattr(value, name)
        if type(refs) is not tuple:
            raise AdminContractError("PAWD_TRACE_INVALID")
        if bound is not None and len(refs) > bound:
            raise AdminContractError("PAWD_TRACE_LIMIT_EXCEEDED")
        for item in refs:
            _admin_ref(item, maximum)
    if value.correlation_id not in value.correlation_ids:
        raise AdminContractError("PAWD_CORRELATION_MISMATCH")
    if type(value.phase) is not str or value.phase not in _ADMIN_RESULT_PHASES:
        raise AdminContractError("PAWD_PHASE_INVALID")
    if type(value.observed_state) is not str or value.observed_state not in _ADMIN_OBSERVED:
        raise AdminContractError("PAWD_OBSERVED_INVALID")
    if value.subject_outcome is not None and (type(value.subject_outcome) is not str or value.subject_outcome not in _ADMIN_SUBJECT):
        raise AdminContractError("PAWD_SUBJECT_INVALID")
    if type(value.proof_bindings) is not tuple:
        raise AdminContractError("PAWD_PROOFS_INVALID")
    if payload is not None and len(value.proof_bindings) > payload.max_observation_refs:
        raise AdminContractError("PAWD_PROOFS_LIMIT_EXCEEDED")
    for item in value.proof_bindings:
        _admin_check_binding(item, maximum)
    if value.observed_at is None:
        observed_ok = False
    else:
        _admin_timestamp(value.observed_at)
        observed_ok = True
    if value.diagnostic_code is not None and (type(value.diagnostic_code) is not str or _ADMIN_DIAG.fullmatch(value.diagnostic_code) is None):
        raise AdminContractError("PAWD_DIAGNOSTIC_INVALID")
    non_observable = value.observed_state in ("UNKNOWN", "UNAVAILABLE", "NON_OBSERVABLE")
    if non_observable:
        if observed_ok or len(value.proof_bindings) != 0 or value.phase == "SUCCEEDED":
            raise AdminContractError("PAWD_OBSERVABILITY_MISMATCH")
    else:
        if not observed_ok or len(value.proof_bindings) == 0:
            raise AdminContractError("PAWD_OBSERVABILITY_MISMATCH")
    if value.phase in ("FAILED", "IN_DOUBT", "BLOCKED") and value.diagnostic_code is None:
        raise AdminContractError("PAWD_DIAGNOSTIC_REQUIRED")
    if value.phase == "SUCCEEDED" and value.diagnostic_code is not None:
        raise AdminContractError("PAWD_DIAGNOSTIC_MISMATCH")
    if value.catalog_operation == "withdraw_initial_authority":
        if value.subject_operation_ref != value.operation_id or value.subject_outcome is not None:
            raise AdminContractError("PAWD_SUBJECT_MISMATCH")
        if value.phase == "SUCCEEDED" and (value.observed_state != "WITHDRAWN_DECLARED" or not observed_ok or len(value.proof_bindings) == 0):
            raise AdminContractError("PAWD_WITHDRAW_COHERENCE_INVALID")
    else:
        if value.subject_operation_ref is None:
            if value.subject_outcome is not None:
                raise AdminContractError("PAWD_SUBJECT_MISMATCH")
        else:
            if value.subject_outcome is None:
                raise AdminContractError("PAWD_SUBJECT_MISMATCH")


def _admin_result_to_dict(value: AdminResult) -> dict[str, object]:
    return {
        "schema_version": value.schema_version, "catalog_operation": value.catalog_operation,
        "catalog_version": value.catalog_version, "operation_id": value.operation_id,
        "subject_operation_ref": value.subject_operation_ref, "invocation_ref": value.invocation_ref,
        "correlation_id": value.correlation_id, "correlation_ids": list(value.correlation_ids),
        "causation_ids": list(value.causation_ids), "installation_ref": value.installation_ref,
        "target_ref": value.target_ref, "mandate_ref": value.mandate_ref, "phase": value.phase,
        "observed_state": value.observed_state, "subject_outcome": value.subject_outcome,
        "observed_at": value.observed_at,
        "proof_bindings": [_binding_to_dict(item) for item in value.proof_bindings],
        "diagnostic_code": value.diagnostic_code,
    }


def encode_admin_result(value: AdminResult, limits: MandateLimits) -> str:
    if type(value) is not AdminResult or type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_INPUT_INVALID")
    _check_admin_result(value, limits)
    return _admin_encode(_admin_result_to_dict(value), limits.payload.max_json_bytes)


def decode_admin_result(text: str, limits: MandateLimits) -> AdminResult:
    if type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_LIMITS_INVALID")
    value = _admin_decode_json(text, limits.payload.max_json_bytes)
    _admin_fields(value, set(AdminResult.__dataclass_fields__))
    for name in ("correlation_ids", "causation_ids"):
        if type(value[name]) is not list:
            raise AdminContractError("PAWD_TRACE_INVALID")
        value[name] = tuple(value[name])
    proofs = value["proof_bindings"]
    if type(proofs) is not list:
        raise AdminContractError("PAWD_PROOFS_INVALID")
    value["proof_bindings"] = tuple(_binding_from_dict(item) for item in proofs)
    result = AdminResult(**value)  # type: ignore[arg-type]
    _check_admin_result(result, limits)
    return result


def match_admin_result_request(result: AdminResult, request: AdminRequest, limits: MandateLimits) -> None:
    if type(result) is not AdminResult or type(request) is not AdminRequest or type(limits) is not MandateLimits:
        raise AdminContractError("PAWD_BINDING_INPUT_INVALID")
    _check_admin_result(result, limits)
    _check_admin_request(request, limits.payload)
    for name in ("schema_version", "catalog_operation", "catalog_version", "operation_id", "installation_ref", "target_ref", "correlation_id", "mandate_ref"):
        if getattr(result, name) != getattr(request, name):
            raise AdminContractError("PAWD_RESULT_MISMATCH")
    params = dict(request.params)
    if request.catalog_operation == "withdraw_initial_authority":
        if result.subject_operation_ref != request.operation_id:
            raise AdminContractError("PAWD_RESULT_SUBJECT_MISMATCH")
    else:
        if set(params) == set():
            if result.subject_operation_ref is not None:
                raise AdminContractError("PAWD_RESULT_SUBJECT_MISMATCH")
        elif set(params) == {"subject_operation_ref"}:
            if result.subject_operation_ref != params["subject_operation_ref"]:
                raise AdminContractError("PAWD_RESULT_SUBJECT_MISMATCH")
        else:
            raise AdminContractError("PAWD_PARAMS_FIELDS_INVALID")
