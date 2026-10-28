from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError,
    NativeRequest,
    PayloadLimits,
    decode_request,
    encode_request,
)
from .technical_projection import (
    ProjectionLimits,
    TechnicalProjection,
    TechnicalProjectionError,
    dump_projection_canonical,
    parse_projection_bytes,
    projection_sha256,
)


__all__ = [
    "ExchangeEnvelopeError",
    "ExchangeRequestLimits",
    "ExchangeRequest",
    "parse_exchange_request",
    "dump_exchange_request",
    "exchange_request_sha256",
]


_REQ_SCHEMA = "pixs.agent.postgresql.exchange.request"
_REQ_VERSION = "1.1.0"
_PURPOSES = ("OBSERVE", "PREPARE_PLAN", "PREPARE", "READ_RESULT")
_PURPOSE_OPERATION = {
    "OBSERVE": "inspect_postgresql",
    "PREPARE_PLAN": "inspect_postgresql",
    "PREPARE": "prepare_postgresql",
    "READ_RESULT": "get_postgresql_result",
}


class ExchangeEnvelopeError(ValueError):
    def __init__(self) -> None:
        super().__init__("Requete echange 1.1 C08 non verifiable.")
        self.code = "C08_EXCHANGE_REQUEST_INVALID"
        self.element = "exchange_request"
        self.step = "validate_exchange_request"


@dataclass(frozen=True, slots=True)
class ExchangeRequestLimits:
    payload: PayloadLimits
    projection_limits: ProjectionLimits
    max_envelope_bytes: int

    def __post_init__(self) -> None:
        if type(self.payload) is not PayloadLimits:
            raise ExchangeEnvelopeError()
        if type(self.projection_limits) is not ProjectionLimits:
            raise ExchangeEnvelopeError()
        for name in (
            "max_bytes",
            "max_ref_bytes",
            "max_correlation_refs",
            "max_causation_refs",
        ):
            v = getattr(self.projection_limits, name)
            if type(v) is not int or v < 1:
                raise ExchangeEnvelopeError()
        if type(self.max_envelope_bytes) is not int:
            raise ExchangeEnvelopeError()
        if self.max_envelope_bytes < 1:
            raise ExchangeEnvelopeError()


@dataclass(frozen=True, slots=True, repr=False)
class ExchangeRequest:
    schema: str
    schema_version: str
    purpose: str
    request: NativeRequest
    projection_document: TechnicalProjection | None
    projection_binding: ContentBinding | None
    confirmation_ref: str | None

    def __post_init__(self) -> None:
        _check_structure(self)


def _ref(value: str, maximum: int | None) -> None:
    if type(value) is not str or not value:
        raise ExchangeEnvelopeError()
    for ch in value:
        o = ord(ch)
        if o < 32 or o == 127 or 55296 <= o <= 57343:
            raise ExchangeEnvelopeError()
    try:
        n = len(value.encode("utf-8"))
    except UnicodeEncodeError as e:
        raise ExchangeEnvelopeError() from e
    if maximum is not None and n > maximum:
        raise ExchangeEnvelopeError()


def _digest(value: str) -> None:
    if type(value) is not str or len(value) != 64:
        raise ExchangeEnvelopeError()
    for c in value:
        if c not in "0123456789abcdef":
            raise ExchangeEnvelopeError()


def _pairs(pairs) -> dict:
    d = {}
    for k, v in pairs:
        if k in d:
            raise ExchangeEnvelopeError()
        d[k] = v
    return d


def _number(v) -> None:
    raise ExchangeEnvelopeError()


def _check_structure(value: ExchangeRequest) -> None:
    if type(value) is not ExchangeRequest:
        raise ExchangeEnvelopeError()
    if type(value.schema) is not str:
        raise ExchangeEnvelopeError()
    if type(value.schema_version) is not str:
        raise ExchangeEnvelopeError()
    if type(value.purpose) is not str:
        raise ExchangeEnvelopeError()
    if value.schema != _REQ_SCHEMA:
        raise ExchangeEnvelopeError()
    if value.schema_version != _REQ_VERSION:
        raise ExchangeEnvelopeError()
    if value.purpose not in _PURPOSES:
        raise ExchangeEnvelopeError()
    if type(value.request) is not NativeRequest:
        raise ExchangeEnvelopeError()
    if value.request.catalog_operation != _PURPOSE_OPERATION[value.purpose]:
        raise ExchangeEnvelopeError()
    if value.purpose == "PREPARE_PLAN":
        if type(value.projection_document) is not TechnicalProjection:
            raise ExchangeEnvelopeError()
        if type(value.projection_binding) is not ContentBinding:
            raise ExchangeEnvelopeError()
        if type(value.confirmation_ref) is not str:
            raise ExchangeEnvelopeError()
        if not value.confirmation_ref:
            raise ExchangeEnvelopeError()
        if value.projection_binding.version != "1.0.0":
            raise ExchangeEnvelopeError()
        if value.projection_binding.ref != value.projection_document.projection_ref:
            raise ExchangeEnvelopeError()
        if value.request.operation_id == value.projection_document.operation_id:
            raise ExchangeEnvelopeError()
        if value.projection_document.correlation_id != value.request.correlation_id:
            raise ExchangeEnvelopeError()
        if value.projection_document.installation_ref != value.request.installation_ref:
            raise ExchangeEnvelopeError()
        if value.projection_document.target_ref != value.request.target_ref:
            raise ExchangeEnvelopeError()
    else:
        if value.projection_document is not None:
            raise ExchangeEnvelopeError()
        if value.projection_binding is not None:
            raise ExchangeEnvelopeError()
        if value.confirmation_ref is not None:
            raise ExchangeEnvelopeError()


def _check_bounded(
    value: ExchangeRequest, limits: ExchangeRequestLimits
) -> None:
    if type(limits) is not ExchangeRequestLimits:
        raise ExchangeEnvelopeError()
    _check_structure(value)
    maximum = limits.payload.max_ref_bytes
    _ref(value.request.operation_id, maximum)
    _ref(value.request.installation_ref, maximum)
    _ref(value.request.target_ref, maximum)
    if value.purpose == "PREPARE_PLAN":
        if value.projection_document is None:
            raise ExchangeEnvelopeError()
        if value.projection_binding is None:
            raise ExchangeEnvelopeError()
        if type(value.confirmation_ref) is not str:
            raise ExchangeEnvelopeError()
        _ref(value.projection_binding.ref, maximum)
        _ref(value.projection_binding.version, maximum)
        _digest(value.projection_binding.sha256)
        _ref(value.confirmation_ref, maximum)
        try:
            expect = projection_sha256(
                value.projection_document, limits.projection_limits
            )
        except TechnicalProjectionError as e:
            raise ExchangeEnvelopeError() from e
        if value.projection_binding.sha256 != expect:
            raise ExchangeEnvelopeError()


def _decode_outer(raw: bytes, limits: ExchangeRequestLimits) -> dict:
    if type(raw) is not bytes or not raw:
        raise ExchangeEnvelopeError()
    if len(raw) > limits.max_envelope_bytes:
        raise ExchangeEnvelopeError()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ExchangeEnvelopeError() from e
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise ExchangeEnvelopeError() from e
    if type(doc) is not dict:
        raise ExchangeEnvelopeError()
    return doc


def _encode_outer(doc: dict, limits: ExchangeRequestLimits) -> bytes:
    try:
        text = json.dumps(
            doc,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise ExchangeEnvelopeError() from e
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError as e:
        raise ExchangeEnvelopeError() from e
    if len(raw) > limits.max_envelope_bytes:
        raise ExchangeEnvelopeError()
    return raw


def parse_exchange_request(
    raw: bytes, limits: ExchangeRequestLimits
) -> ExchangeRequest:
    if type(limits) is not ExchangeRequestLimits:
        raise ExchangeEnvelopeError()
    doc = _decode_outer(raw, limits)
    purpose = doc.get("purpose")
    if type(purpose) is not str or purpose not in _PURPOSES:
        raise ExchangeEnvelopeError()
    if purpose == "PREPARE_PLAN":
        if set(doc) != {
            "schema",
            "schema_version",
            "purpose",
            "request",
            "projection_document",
            "projection_binding",
            "confirmation_ref",
        }:
            raise ExchangeEnvelopeError()
    else:
        if set(doc) != {"schema", "schema_version", "purpose", "request"}:
            raise ExchangeEnvelopeError()
    if type(doc["schema"]) is not str or doc["schema"] != _REQ_SCHEMA:
        raise ExchangeEnvelopeError()
    if type(doc["schema_version"]) is not str:
        raise ExchangeEnvelopeError()
    if doc["schema_version"] != _REQ_VERSION:
        raise ExchangeEnvelopeError()
    req_doc = doc["request"]
    if type(req_doc) is not dict:
        raise ExchangeEnvelopeError()
    try:
        req_text = json.dumps(
            req_doc,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise ExchangeEnvelopeError() from e
    try:
        native = decode_request(req_text, limits.payload)
    except ContractError as e:
        raise ExchangeEnvelopeError() from e
    if native.catalog_operation != _PURPOSE_OPERATION[purpose]:
        raise ExchangeEnvelopeError()
    proj: TechnicalProjection | None = None
    bind: ContentBinding | None = None
    cref: str | None = None
    if purpose == "PREPARE_PLAN":
        proj_doc = doc["projection_document"]
        bind_doc = doc["projection_binding"]
        cref = doc["confirmation_ref"]
        if type(proj_doc) is not dict:
            raise ExchangeEnvelopeError()
        if type(bind_doc) is not dict:
            raise ExchangeEnvelopeError()
        if type(cref) is not str:
            raise ExchangeEnvelopeError()
        if set(bind_doc) != {"ref", "version", "sha256"}:
            raise ExchangeEnvelopeError()
        try:
            proj_text = json.dumps(
                proj_doc,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        except (TypeError, ValueError, RecursionError) as e:
            raise ExchangeEnvelopeError() from e
        try:
            proj = parse_projection_bytes(
                proj_text.encode("utf-8"), limits.projection_limits
            )
        except (TechnicalProjectionError, UnicodeEncodeError) as e:
            raise ExchangeEnvelopeError() from e
        try:
            bind = ContentBinding(
                ref=bind_doc["ref"],
                version=bind_doc["version"],
                sha256=bind_doc["sha256"],
            )
        except ContractError as e:
            raise ExchangeEnvelopeError() from e
        if bind.version != "1.0.0" or bind.ref != proj.projection_ref:
            raise ExchangeEnvelopeError()
        _digest(bind.sha256)
        try:
            expect = projection_sha256(proj, limits.projection_limits)
        except TechnicalProjectionError as e:
            raise ExchangeEnvelopeError() from e
        if bind.sha256 != expect:
            raise ExchangeEnvelopeError()
        _ref(cref, limits.payload.max_ref_bytes)
        if proj.installation_ref != native.installation_ref:
            raise ExchangeEnvelopeError()
        if proj.target_ref != native.target_ref:
            raise ExchangeEnvelopeError()
        if native.operation_id == proj.operation_id:
            raise ExchangeEnvelopeError()
        if proj.correlation_id != native.correlation_id:
            raise ExchangeEnvelopeError()
    value = ExchangeRequest(
        schema=doc["schema"],
        schema_version=doc["schema_version"],
        purpose=purpose,
        request=native,
        projection_document=proj,
        projection_binding=bind,
        confirmation_ref=cref,
    )
    _check_bounded(value, limits)
    if dump_exchange_request(value, limits) != raw:
        raise ExchangeEnvelopeError()
    return value


def dump_exchange_request(
    value: ExchangeRequest, limits: ExchangeRequestLimits
) -> bytes:
    if type(limits) is not ExchangeRequestLimits:
        raise ExchangeEnvelopeError()
    _check_bounded(value, limits)
    try:
        req_text = encode_request(value.request, limits.payload)
    except ContractError as e:
        raise ExchangeEnvelopeError() from e
    try:
        req_doc = json.loads(
            req_text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise ExchangeEnvelopeError() from e
    doc = {
        "schema": value.schema,
        "schema_version": value.schema_version,
        "purpose": value.purpose,
        "request": req_doc,
    }
    if value.purpose == "PREPARE_PLAN":
        if value.projection_document is None:
            raise ExchangeEnvelopeError()
        if value.projection_binding is None:
            raise ExchangeEnvelopeError()
        if type(value.confirmation_ref) is not str:
            raise ExchangeEnvelopeError()
        try:
            proj_raw = dump_projection_canonical(
                value.projection_document, limits.projection_limits
            )
        except TechnicalProjectionError as e:
            raise ExchangeEnvelopeError() from e
        try:
            proj_doc = json.loads(
                proj_raw.decode("utf-8"),
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
            raise ExchangeEnvelopeError() from e
        doc["projection_document"] = proj_doc
        doc["projection_binding"] = {
            "ref": value.projection_binding.ref,
            "version": value.projection_binding.version,
            "sha256": value.projection_binding.sha256,
        }
        doc["confirmation_ref"] = value.confirmation_ref
    return _encode_outer(doc, limits)


def exchange_request_sha256(
    value: ExchangeRequest, limits: ExchangeRequestLimits
) -> str:
    return hashlib.sha256(dump_exchange_request(value, limits)).hexdigest()
