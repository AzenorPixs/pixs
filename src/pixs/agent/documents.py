"""Documents payload Agent D-S1 3.4 : traces et observes opaques, verification pure.

Frontiere seule en donnees fournies, sans effet. Ne prouve ni persistance,
ni provenance, ni migration, ni autorite, ni transport, ni confiance, ni signature.
Stdlib et pixs.agent.identifiers pour bornes UTF8 et digests seulement.
Aucun import Django, DB, provider, reseau, horloge ou I/O.
Bornes de longueur fournies par l appelant quand requises, sans defaut invente.
"""
from __future__ import annotations
import hashlib
import json
from pixs.agent import identifiers as ids

AGENT_CONTENT = "AGENT_CONTENT"
AGENT_TRACE = "AGENT_TRACE"
AGENT_OBSERVATION = "AGENT_OBSERVATION"
TRACE_CODEC = "agent-traces.v1"
OBSERVED_CODEC = "agent-observed-opaque.v1"
CONTENT_KEYS = ("codec", "schema_version", "operation_name", "operation_version", "subject_id", "scope_type", "tenant_id", "scope_id", "target_id", "expected_generation", "params_canonical", "mandate_ref", "expires_at")
FIXED_MESSAGE = "Document Agent invalide."

class AgentDocumentError(ValueError):
    def __init__(self) -> None:
        super().__init__(FIXED_MESSAGE)
        self.code = "AGENT_DOCUMENT_INVALID"
        self.element = "agent_document"
        self.step = "validate_document"
    def __repr__(self) -> str:
        return "AgentDocumentError(<redacted>)"
    def __str__(self) -> str:
        return "AgentDocumentError(<redacted>)"

def _fail() -> None:
    raise AgentDocumentError() from None

def _require_opaque_str(value: object, max_len: int | None = None) -> str:
    if type(value) is not str or value == "" or "\x00" in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    assert isinstance(value, str)
    if max_len is not None:
        if type(max_len) is bool or type(max_len) is not int or max_len < 1:
            _fail()
        if len(value) > max_len:
            _fail()
    return value

def _reject_constant(value: str) -> None:
    _fail()

def _reject_float(value: str) -> None:
    _fail()

def _check_int(value: str) -> int:
    try:
        number = int(value, 10)
    except ValueError:
        _fail()
    assert isinstance(number, int)
    return number

def _reject_dup_pairs(pairs: list) -> dict:
    seen: set = set()
    for key, _ in pairs:
        if type(key) is not str or key in seen:
            _fail()
        seen.add(key)
    return {k: v for k, v in pairs}

def _require_id_list(value: object, max_len: int | None = None) -> tuple:
    if type(value) is not tuple:
        _fail()
    assert isinstance(value, tuple)
    for item in value:
        _require_opaque_str(item, max_len)
    return value

def canonical_trace(*, request_operation_id: str, correlation_ids: tuple, causation_ids: tuple, max_len: int | None = None) -> str:
    op = _require_opaque_str(request_operation_id, max_len)
    corr = _require_id_list(correlation_ids, max_len)
    caus = _require_id_list(causation_ids, max_len)
    payload = {"correlation_ids": list(corr), "causation_ids": list(caus), "request_operation_id": op}
    try:
        text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    assert isinstance(text, str)
    if "\x00" in text or text.endswith("\n"):
        _fail()
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    return text

def require_trace_canonical(text: object, max_len: int | None = None) -> str:
    if type(text) is not str or text == "":
        _fail()
    assert isinstance(text, str)
    if "\x00" in text or text.endswith("\n"):
        _fail()
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    try:
        parsed = json.loads(text, object_pairs_hook=_reject_dup_pairs, parse_constant=_reject_constant, parse_float=_reject_float, parse_int=_check_int)
    except (ValueError, RecursionError):
        _fail()
    if type(parsed) is not dict or set(parsed.keys()) != {"request_operation_id", "correlation_ids", "causation_ids"}:
        _fail()
    _require_opaque_str(parsed["request_operation_id"], max_len)
    for key in ("correlation_ids", "causation_ids"):
        seq = parsed[key]
        if type(seq) is not list:
            _fail()
        for item in seq:
            _require_opaque_str(item, max_len)
    try:
        canonical = json.dumps({"correlation_ids": parsed["correlation_ids"], "causation_ids": parsed["causation_ids"], "request_operation_id": parsed["request_operation_id"]}, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    if canonical != text:
        _fail()
    return text

def require_observed_opaque(document: object, max_len: int | None = None) -> bytes:
    text = _require_opaque_str(document, max_len)
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    assert isinstance(raw, bytes)
    if len(raw) == 0:
        _fail()
    return raw

def _require_hex64(value: object) -> str:
    if type(value) is not str or len(value) != 64:
        _fail()
    assert isinstance(value, str)
    for ch in value:
        if not (("0" <= ch <= "9") or ("a" <= ch <= "f")):
            _fail()
    return value

def _require_content_bytes(raw: bytes, codec: str, version: str) -> None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail()
    if "\x00" in text or text == "":
        _fail()
    try:
        parsed = json.loads(text, object_pairs_hook=_reject_dup_pairs, parse_constant=_reject_constant, parse_float=_reject_float, parse_int=_check_int)
    except (ValueError, RecursionError):
        _fail()
    if type(parsed) is not dict or set(parsed.keys()) != set(CONTENT_KEYS):
        _fail()
    if parsed.get("codec") != codec or parsed.get("schema_version") != version:
        _fail()
    try:
        if version == "1.0.0":
            rebuilt = ids.canonical_operation_content(schema_version=parsed["schema_version"], operation_name=parsed["operation_name"], operation_version=parsed["operation_version"], subject_id=parsed["subject_id"], tenant_id=parsed["tenant_id"], scope_id=parsed["scope_id"], target_id=parsed["target_id"], expected_generation=parsed["expected_generation"], params_canonical=parsed["params_canonical"], mandate_ref=parsed["mandate_ref"], expires_at=parsed["expires_at"], scope_type=parsed["scope_type"])
        else:
            rebuilt = ids.canonical_operation_content_v2(schema_version=parsed["schema_version"], operation_name=parsed["operation_name"], operation_version=parsed["operation_version"], subject_id=parsed["subject_id"], tenant_id=parsed["tenant_id"], scope_id=parsed["scope_id"], target_id=parsed["target_id"], expected_generation=parsed["expected_generation"], params_canonical=parsed["params_canonical"], mandate_ref=parsed["mandate_ref"], expires_at=parsed["expires_at"], scope_type=parsed["scope_type"])
    except ids.AgentIdentifierError:
        _fail()
    assert isinstance(rebuilt, str)
    if rebuilt.encode("utf-8") != raw:
        _fail()

def verify_payload_document(*, document_kind: object, payload_contract_version: object, codec: object, payload_bytes: object, byte_length: object, bytes_sha256: object) -> None:
    if type(document_kind) is not str or document_kind not in (AGENT_CONTENT, AGENT_TRACE, AGENT_OBSERVATION):
        _fail()
    if type(payload_contract_version) is not str or payload_contract_version not in ("1.0.0", "2.0.0"):
        _fail()
    if type(codec) is not str:
        _fail()
    assert isinstance(payload_contract_version, str) and isinstance(codec, str)
    if document_kind == AGENT_CONTENT:
        if payload_contract_version == "1.0.0":
            if codec != ids.CONTENT_CODEC:
                _fail()
        else:
            if codec != ids.CONTENT_CODEC_V2:
                _fail()
    elif document_kind == AGENT_TRACE:
        if codec != TRACE_CODEC:
            _fail()
    else:
        if codec != OBSERVED_CODEC:
            _fail()
    if type(payload_bytes) is not bytes or len(payload_bytes) == 0:
        _fail()
    assert isinstance(payload_bytes, bytes)
    if type(byte_length) is bool:
        _fail()
    if type(byte_length) is not int or byte_length <= 0:
        _fail()
    if byte_length != len(payload_bytes):
        _fail()
    digest = _require_hex64(bytes_sha256)
    if hashlib.sha256(payload_bytes).hexdigest() != digest:
        _fail()
    if document_kind == AGENT_CONTENT:
        _require_content_bytes(payload_bytes, codec, payload_contract_version)
    elif document_kind == AGENT_TRACE:
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError:
            _fail()
        require_trace_canonical(text)
    else:
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError:
            _fail()
        require_observed_opaque(text)
