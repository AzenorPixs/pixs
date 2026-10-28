"""Contexte public BootstrapTpmContext/v1.

Forme publique de configuration : huit chaînes strictes, canon trié
compact et liaison de forme. Cette forme ne prouve ni identité TPM, ni
autorité, ni garde, ni observation matérielle ; les résolutions natives
restent privées et hors document.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from typing import Any

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, PayloadLimits
elif __package__ in (None, ""):
    if "postgresql_contracts" in sys.builtin_module_names:
        from postgresql_contracts import ContentBinding, PayloadLimits
    else:
        raise ImportError("bootstrap_context: unsupported package context")
else:
    raise ImportError("bootstrap_context: unsupported package context")

__all__ = [
    "BootstrapContextContractError",
    "BootstrapTpmContext",
    "encode_bootstrap_context",
    "decode_bootstrap_context",
    "bootstrap_context_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_tpm_context/v1"
SCHEMA_VERSION = "1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "context_ref",
    "context_version",
    "installation_ref",
    "target_ref",
    "tcti_backend_ref",
    "usage_custody_ref",
)

_REF_FIELDS = (
    "context_ref",
    "context_version",
    "installation_ref",
    "target_ref",
    "tcti_backend_ref",
    "usage_custody_ref",
)


class BootstrapContextContractError(ValueError):
    pass


def _fail() -> None:
    raise BootstrapContextContractError("bootstrap_context: invalid value") from None


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
    size = len(value.encode("utf-8"))
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapTpmContext:
    object_type: str
    schema_version: str
    context_ref: str
    context_version: str
    installation_ref: str
    target_ref: str
    tcti_backend_ref: str
    usage_custody_ref: str

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_nonempty_text(self.context_ref)
        _check_strict_nonempty_text(self.context_version)
        _check_strict_nonempty_text(self.installation_ref)
        _check_strict_nonempty_text(self.target_ref)
        _check_strict_nonempty_text(self.tcti_backend_ref)
        _check_strict_nonempty_text(self.usage_custody_ref)
        _check_no_wildcard(self.installation_ref)
        _check_no_wildcard(self.target_ref)


def _check_bounded_form(value: BootstrapTpmContext, limits: PayloadLimits) -> None:
    if type(value) is not BootstrapTpmContext:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    for name in _REF_FIELDS:
        field_value = getattr(value, name)
        _check_strict_nonempty_text(field_value)
        _check_bounded_ref(field_value, limits.max_ref_bytes)
    _check_no_wildcard(value.installation_ref)
    _check_no_wildcard(value.target_ref)


def encode_bootstrap_context(value: BootstrapTpmContext, limits: PayloadLimits) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits)
    payload = {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "context_ref": value.context_ref,
        "context_version": value.context_version,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "tcti_backend_ref": value.tcti_backend_ref,
        "usage_custody_ref": value.usage_custody_ref,
    }
    try:
        text = json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except BootstrapContextContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapContextContractError("bootstrap_context: invalid value") from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def _reject_number(token: str) -> None:
    raise BootstrapContextContractError("bootstrap_context: invalid value")


def _reject_constant(token: str) -> None:
    raise BootstrapContextContractError("bootstrap_context: invalid value")


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
        if type(item) is not str:
            _fail()
        result[key] = item
    return result


def decode_bootstrap_context(text: Any, limits: PayloadLimits) -> BootstrapTpmContext:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapContextContractError("bootstrap_context: invalid value") from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    try:
        data = json.loads(
            text,
            object_pairs_hook=_pairs_hook,
            parse_int=_reject_number,
            parse_float=_reject_number,
            parse_constant=_reject_constant,
        )
    except BootstrapContextContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    try:
        value = BootstrapTpmContext(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            context_ref=data["context_ref"],
            context_version=data["context_version"],
            installation_ref=data["installation_ref"],
            target_ref=data["target_ref"],
            tcti_backend_ref=data["tcti_backend_ref"],
            usage_custody_ref=data["usage_custody_ref"],
        )
    except BootstrapContextContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits)
    return value


def bootstrap_context_binding(value: BootstrapTpmContext, limits: PayloadLimits) -> ContentBinding:
    _check_limits(limits)
    canon = encode_bootstrap_context(value, limits)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    return ContentBinding(
        ref=value.context_ref,
        version=value.context_version,
        sha256=digest,
    )
