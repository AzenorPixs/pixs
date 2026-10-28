"""Identifiants Agent : UUIDv7, JSON canoniques versionnés et digests, stdlib et SemVer Kernel public."""
from __future__ import annotations
import datetime
import hashlib
import json
import secrets
import time
import uuid
from pixs.kernel.manifest.semver import parse_version
__all__ = ["AgentIdentifierError", "require_agent_uuid7", "new_agent_uuid7", "require_canonical_instant", "canonical_head_identity", "head_digest", "canonical_idempotence_identity", "idempotence_digest", "require_canonical_params_text", "canonical_params_text", "require_canonical_trace_list", "canonical_operation_content", "content_digest", "HEAD_CODEC", "IDENTITY_CODEC", "CONTENT_CODEC"]
HEAD_CODEC = "agent-head.v1"
IDENTITY_CODEC = "agent-idem.v1"
CONTENT_CODEC = "agent-content.v1"
SCHEMA_VERSION = "1.0.0"
FIXED_MESSAGE = "Identifiant Agent invalide."
class AgentIdentifierError(ValueError):
    def __init__(self) -> None:
        super().__init__(FIXED_MESSAGE)
        self.code = "AGENT_IDENTIFIER_INVALID"
        self.element = "agent_identifier"
        self.step = "validate_identifier"
def _fail() -> None:
    raise AgentIdentifierError() from None
def require_agent_uuid7(value: object) -> uuid.UUID:
    if type(value) is not uuid.UUID:
        _fail()
    try:
        number = object.__getattribute__(value, "int")
    except AttributeError:
        _fail()
    assert isinstance(number, int)
    if not 0 <= number < 2**128:
        _fail()
    if (number >> 76) & 15 != 7 or (number >> 62) & 3 != 2:
        _fail()
    return value
def new_agent_uuid7() -> uuid.UUID:
    ms = time.time_ns() // 1_000_000
    if type(ms) is not int or not 0 <= ms < 2**48:
        _fail()
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    if type(rand_a) is not int or not 0 <= rand_a < 2**12:
        _fail()
    if type(rand_b) is not int or not 0 <= rand_b < 2**62:
        _fail()
    return require_agent_uuid7(uuid.UUID(int=(ms << 80) | (7 << 76) | (rand_a << 64) | (2 << 62) | rand_b))
def _strict_text(value: object, allow_none: bool) -> str | None:
    if value is None and allow_none:
        return None
    if type(value) is not str or value == "" or "\x00" in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    assert isinstance(value, str)
    return value
def _scope_parts(scope_type: object, tenant_id: object, scope_id: object) -> tuple:
    if type(scope_type) is not str or scope_type not in ("PLATFORM", "TENANT"):
        _fail()
    assert isinstance(scope_type, str)
    if scope_type == "PLATFORM":
        if tenant_id is not None or scope_id is not None:
            _fail()
        return (scope_type, None, None)
    _strict_text(tenant_id, allow_none=False)
    if scope_id is not None:
        _strict_text(scope_id, allow_none=False)
    return (scope_type, tenant_id, scope_id)
def require_canonical_instant(value: object) -> str:
    if type(value) is not str or len(value) != 20:
        _fail()
    assert isinstance(value, str)
    if value[4] != "-" or value[7] != "-" or value[10] != "T" or value[13] != ":" or value[16] != ":" or value[19] != "Z":
        _fail()
    if any(not "0" <= value[position] <= "9" for position in (0,1,2,3,5,6,8,9,11,12,14,15,17,18)):
        _fail()
    try:
        parts = (int(value[0:4]), int(value[5:7]), int(value[8:10]), int(value[11:13]), int(value[14:16]), int(value[17:19]))
    except ValueError:
        _fail()
    try:
        datetime.datetime(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
        value.encode("utf-8")
    except (ValueError, UnicodeEncodeError):
        _fail()
    return value
def _require_semver(value: object) -> str:
    text = _strict_text(value, allow_none=False)
    try:
        parse_version(text)
    except ValueError:
        _fail()
    return text
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
def _check_json_value(node: object) -> None:
    """Paramètres2.1a : noms exacts et valeurs scalaires str/int/bool."""
    if type(node) is not dict:
        _fail()
    for key, value in node.items():
        _strict_text(key, allow_none=False)
        if type(value) is str:
            if "\x00" in value:
                _fail()
            try:
                value.encode("utf-8")
            except UnicodeEncodeError:
                _fail()
        elif type(value) not in (int, bool):
            _fail()
def _strict_loads_object(text: str) -> dict:
    try:
        parsed = json.loads(text, object_pairs_hook=_reject_dup_pairs, parse_constant=_reject_constant, parse_float=_reject_float, parse_int=_check_int)
    except (ValueError, RecursionError):
        _fail()
    if type(parsed) is not dict:
        _fail()
    _check_json_value(parsed)
    return parsed
def require_canonical_params_text(text: object) -> str:
    if type(text) is not str or text == "":
        _fail()
    assert isinstance(text, str)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    parsed = _strict_loads_object(text)
    try:
        canonical = json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    if canonical != text:
        _fail()
    return text
def canonical_params_text(params: object) -> str:
    if type(params) is not dict:
        _fail()
    _check_json_value(params)
    try:
        return json.dumps(params, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
def require_canonical_trace_list(text: object) -> str:
    if type(text) is not str or text == "":
        _fail()
    assert isinstance(text, str)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    try:
        parsed = json.loads(text, parse_constant=_reject_constant, parse_float=_reject_float, parse_int=_check_int)
    except (ValueError, RecursionError):
        _fail()
    if type(parsed) is not list:
        _fail()
    for item in parsed:
        if type(item) is not str or item == "" or "\x00" in item:
            _fail()
        try:
            item.encode("utf-8")
        except UnicodeEncodeError:
            _fail()
    try:
        canonical = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    if canonical != text:
        _fail()
    return text
def _dump_closed(payload: dict) -> str:
    try:
        text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        _fail()
    assert isinstance(text, str)
    if "\x00" in text:
        _fail()
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    return text
def _sha(text: str) -> str:
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        _fail()
    assert isinstance(raw, bytes)
    return hashlib.sha256(raw).hexdigest()
def canonical_head_identity(*, scope_type: str, tenant_id: str | None, scope_id: str | None, target_id: str) -> str:
    st, te, sc = _scope_parts(scope_type, tenant_id, scope_id)
    ta = _strict_text(target_id, allow_none=False)
    return _dump_closed({"codec": HEAD_CODEC, "scope_type": st, "tenant_id": te, "scope_id": sc, "target_id": ta})
def head_digest(identity_canonical: object) -> str:
    if type(identity_canonical) is not str or identity_canonical == "":
        _fail()
    assert isinstance(identity_canonical, str)
    return _sha(identity_canonical)
def canonical_idempotence_identity(*, scope_type: str, tenant_id: str | None, scope_id: str | None, target_id: str, subject_id: str, operation_name: str, operation_version: str, idempotency_key: str) -> str:
    st, te, sc = _scope_parts(scope_type, tenant_id, scope_id)
    ta = _strict_text(target_id, allow_none=False)
    su = _strict_text(subject_id, allow_none=False)
    op = _strict_text(operation_name, allow_none=False)
    opv = _strict_text(operation_version, allow_none=False)
    key = _strict_text(idempotency_key, allow_none=False)
    _require_semver(opv)
    return _dump_closed({"codec": IDENTITY_CODEC, "scope_type": st, "tenant_id": te, "scope_id": sc, "target_id": ta, "subject_id": su, "operation_name": op, "operation_version": opv, "idempotency_key": key})
def idempotence_digest(identity_canonical: object) -> str:
    if type(identity_canonical) is not str or identity_canonical == "":
        _fail()
    assert isinstance(identity_canonical, str)
    return _sha(identity_canonical)
def canonical_operation_content(*, schema_version: str, operation_name: str, operation_version: str, subject_id: str, tenant_id: str | None, scope_id: str | None, target_id: str, expected_generation: int, params_canonical: str, mandate_ref: str, expires_at: str, scope_type: str) -> str:
    st, te, sc = _scope_parts(scope_type, tenant_id, scope_id)
    if type(schema_version) is not str or schema_version != SCHEMA_VERSION:
        _fail()
    op = _strict_text(operation_name, allow_none=False)
    opv = _strict_text(operation_version, allow_none=False)
    su = _strict_text(subject_id, allow_none=False)
    ta = _strict_text(target_id, allow_none=False)
    if type(expected_generation) is not int or not 0 <= expected_generation <= 9223372036854775806:
        _fail()
    require_canonical_params_text(params_canonical)
    mr = _strict_text(mandate_ref, allow_none=False)
    ex = require_canonical_instant(expires_at)
    _require_semver(opv)
    return _dump_closed({"codec": CONTENT_CODEC, "schema_version": schema_version, "operation_name": op, "operation_version": opv, "subject_id": su, "scope_type": st, "tenant_id": te, "scope_id": sc, "target_id": ta, "expected_generation": expected_generation, "params_canonical": params_canonical, "mandate_ref": mr, "expires_at": ex})
def content_digest(content_canonical: object) -> str:
    if type(content_canonical) is not str or content_canonical == "":
        _fail()
    assert isinstance(content_canonical, str)
    return _sha(content_canonical)
