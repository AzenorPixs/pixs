"""Bounded OpenAPI document view, preloaded bytes, no per-request read.

Contract: `build_openapi_view(plan, document)` revalidates `plan` through
the public `api_major_prefix` (exact type, API category, bare ref) and
serves the explicit public `document` (`str` JSON, bounded `64KiB`) as
preloaded frozen bytes. Only the documented 3.1.0 subset is supported:
`openapi == "3.1.0"`, `info.title`/`info.version`, `info.version` equal
to the contract version (local milestone rule, not a global OAS
obligation; `openapi` is the format version, distinct from the document
`info.version`), non-empty `paths` with ASCII literals under the exact
major prefix plus `/` boundary (route-literal grammar: ASCII letters,
digits, `-_.`, internal dots only, applied locally without importing a
private helper and without building Django patterns to validate),
structured operations with `responses` plus `description`, declared
content types (`application/json` only in this minimal subset) with
minimal inline schemas, explicit anonymous `security: []`. External
references are refused. `GET` returns 200 with the exact body, `HEAD`
returns 200 without body and the `Content-Length` of `GET`, other
methods return 405 empty with `Allow: GET, HEAD`. MIME
`application/json; charset=utf-8` and `Cache-Control: no-store`. Bad
construction raises fixed `OpenapiDocumentError` without value echo or
chain. No public URL is distributed by this module.

Limits: pure module import (no Django import or filesystem read at
import, no config or I/O); no `settings.configure`, `django.setup`,
server, DB, socket or secret in this module. The public document is
provided explicitly by the responsible caller; no magic secret
detection is claimed.
"""

from __future__ import annotations

import json
import math

from pixs.backend.api import api_major_prefix

__all__ = [
    "OpenapiDocumentError",
    "build_openapi_view",
]

_ERROR = "Invalid OpenAPI document."
_MAX_DOCUMENT_CHARS = 65536
_MAX_DOCUMENT_SIZE = 65536
_MAX_DEPTH = 32
_ALLOW_VALUE = "GET, HEAD"
_NO_STORE = "no-store"
_CONTENT_TYPE = "application/json; charset=utf-8"
_FORMAT_VERSION = "3.1.0"
_ALLOWED_TOP_KEYS = frozenset({"openapi", "info", "paths", "security"})
_ALLOWED_METHODS = frozenset({"get", "put", "post", "delete", "options", "head", "patch", "trace"})
_ALLOWED_METHOD_KEYS = frozenset({"responses", "summary", "description", "operationId"})
_ALLOWED_RESPONSE_KEYS = frozenset({"description", "content"})
_ALLOWED_MEDIA_KEYS = frozenset({"schema"})
_ALLOWED_SCHEMA_KEYS = frozenset({"type", "properties", "items", "enum", "format", "description", "required"})
_ALLOWED_SCHEMA_TYPES = frozenset({"object", "array", "string", "number", "integer", "boolean", "null"})
_ALLOWED_MEDIA_TYPES = frozenset({"application/json"})


class OpenapiDocumentError(ValueError):
    """Stable document error, without raw value echo."""

    def __init__(self, message: str = _ERROR) -> None:
        super().__init__(message)


def _invalid_document() -> OpenapiDocumentError:
    return OpenapiDocumentError(_ERROR)


def _require_method(request: object) -> str:
    try:
        method = getattr(request, "method", None)
    except Exception:
        raise _invalid_document() from None
    if type(method) is not str:
        raise _invalid_document()
    return method


def _reject_constant(value: str) -> object:
    raise _invalid_document()


def _reject_duplicate_keys(pairs: list) -> dict:
    seen: set[str] = set()
    result: dict[str, object] = {}
    for key, item in pairs:
        if type(key) is not str or key in seen:
            raise _invalid_document()
        seen.add(key)
        result[key] = item
    return result


def _walk_json(value: object, depth: int) -> None:
    if depth > _MAX_DEPTH:
        raise _invalid_document()
    if value is None or type(value) is bool:
        return
    if type(value) is int:
        return
    if type(value) is float:
        try:
            finite = math.isfinite(value)
        except Exception:
            raise _invalid_document() from None
        if finite is not True:
            raise _invalid_document()
        return
    if type(value) is str:
        try:
            value.encode("utf-8")
        except Exception:
            raise _invalid_document() from None
        return
    if type(value) is list:
        for item in value:
            _walk_json(item, depth + 1)
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise _invalid_document()
            if key == "$ref":
                raise _invalid_document()
            try:
                key.encode("utf-8")
            except Exception:
                raise _invalid_document() from None
            _walk_json(item, depth + 1)
        return
    raise _invalid_document()


def _check_route_literal(path: str, prefix: str) -> None:
    if not path.startswith(prefix + "/") or len(path) <= len(prefix) + 1:
        raise _invalid_document()
    rest = path[len(prefix) + 1:]
    if rest.endswith("/"):
        rest = rest[:-1]
    if rest == "":
        raise _invalid_document()
    for segment in rest.split("/"):
        if segment == "" or segment in (".", ".."):
            raise _invalid_document()
        if segment.startswith(".") or segment.endswith("."):
            raise _invalid_document()
        if ".." in segment:
            raise _invalid_document()
        for character in segment:
            valid = ("A" <= character <= "Z" or "a" <= character <= "z"
                     or "0" <= character <= "9" or character in ("-", "_", "."))
            if not valid:
                raise _invalid_document()


def _check_status_code(code: str) -> None:
    if code == "default":
        return
    if type(code) is not str or len(code) != 3:
        raise _invalid_document()
    for character in code:
        if not ("0" <= character <= "9"):
            raise _invalid_document()
    if int(code) < 100 or int(code) > 599:
        raise _invalid_document()


def _enum_key(item: object) -> tuple:
    if type(item) is bool:
        return ("bool", item)
    if type(item) is int:
        return ("number", item)
    if type(item) is float:
        return ("number", item)
    if type(item) is str:
        return ("str", item)
    return ("none", 0)


def _check_schema(node: object, depth: int) -> None:
    if depth > _MAX_DEPTH or type(node) is not dict:
        raise _invalid_document()
    for key in node:
        if type(key) is not str or key == "$ref":
            raise _invalid_document()
        if key not in _ALLOWED_SCHEMA_KEYS:
            raise _invalid_document()
    if "type" in node:
        if type(node["type"]) is not str or node["type"] not in _ALLOWED_SCHEMA_TYPES:
            raise _invalid_document()
    for text_key in ("format", "description"):
        if text_key in node and type(node[text_key]) is not str:
            raise _invalid_document()
    if "properties" in node:
        props = node["properties"]
        if type(props) is not dict:
            raise _invalid_document()
        for name, sub in props.items():
            if type(name) is not str or name == "":
                raise _invalid_document()
            _check_schema(sub, depth + 1)
    if "items" in node:
        _check_schema(node["items"], depth + 1)
    if "enum" in node:
        enum = node["enum"]
        if type(enum) is not list or len(enum) == 0:
            raise _invalid_document()
        seen: set[tuple] = set()
        for item in enum:
            if type(item) not in (str, int, float, bool) and item is not None:
                raise _invalid_document()
            if type(item) is float:
                try:
                    finite = math.isfinite(item)
                except Exception:
                    raise _invalid_document() from None
                if finite is not True:
                    raise _invalid_document()
            key = _enum_key(item)
            if key in seen:
                raise _invalid_document()
            seen.add(key)
    if "required" in node:
        required = node["required"]
        if type(required) is not list:
            raise _invalid_document()
        seen_names: set[str] = set()
        for name in required:
            if type(name) is not str or name == "" or name in seen_names:
                raise _invalid_document()
            seen_names.add(name)


def _check_form(root: object, prefix: str, contract_version: str) -> None:
    if type(root) is not dict:
        raise _invalid_document()
    for key in root:
        if type(key) is not str or key not in _ALLOWED_TOP_KEYS:
            raise _invalid_document()
    if type(root.get("openapi")) is not str or root.get("openapi") != _FORMAT_VERSION:
        raise _invalid_document()
    info = root.get("info")
    if type(info) is not dict:
        raise _invalid_document()
    for key in info:
        if type(key) is not str or key not in ("title", "version"):
            raise _invalid_document()
    title = info.get("title")
    version = info.get("version")
    if type(title) is not str or title == "" or title.strip() != title:
        raise _invalid_document()
    if type(version) is not str or version == "" or version != contract_version:
        raise _invalid_document()
    if "security" not in root or type(root["security"]) is not list or len(root["security"]) != 0:
        raise _invalid_document()
    paths = root.get("paths")
    if type(paths) is not dict or len(paths) == 0:
        raise _invalid_document()
    seen_operation_ids: set[str] = set()
    for path, item in paths.items():
        if type(path) is not str:
            raise _invalid_document()
        _check_route_literal(path, prefix)
        if type(item) is not dict or len(item) == 0:
            raise _invalid_document()
        for method, operation in item.items():
            if type(method) is not str or method not in _ALLOWED_METHODS:
                raise _invalid_document()
            if type(operation) is not dict:
                raise _invalid_document()
            for key in operation:
                if type(key) is not str or key not in _ALLOWED_METHOD_KEYS:
                    raise _invalid_document()
            for text_key in ("summary", "description"):
                if text_key in operation and type(operation[text_key]) is not str:
                    raise _invalid_document()
            if "operationId" in operation:
                operation_id = operation["operationId"]
                if type(operation_id) is not str or operation_id == "" or operation_id in seen_operation_ids:
                    raise _invalid_document()
                seen_operation_ids.add(operation_id)
            responses = operation.get("responses")
            if type(responses) is not dict or len(responses) == 0:
                raise _invalid_document()
            for code, response in responses.items():
                _check_status_code(code)
                if type(response) is not dict:
                    raise _invalid_document()
                for key in response:
                    if type(key) is not str or key not in _ALLOWED_RESPONSE_KEYS:
                        raise _invalid_document()
                if type(response.get("description")) is not str:
                    raise _invalid_document()
                if "content" in response:
                    content = response["content"]
                    if type(content) is not dict or len(content) == 0:
                        raise _invalid_document()
                    for media, media_obj in content.items():
                        if type(media) is not str or media not in _ALLOWED_MEDIA_TYPES:
                            raise _invalid_document()
                        if type(media_obj) is not dict:
                            raise _invalid_document()
                        for key in media_obj:
                            if type(key) is not str or key not in _ALLOWED_MEDIA_KEYS:
                                raise _invalid_document()
                        if "schema" not in media_obj:
                            raise _invalid_document()
                        _check_schema(media_obj["schema"], 0)


def build_openapi_view(plan: object, document: object) -> object:
    """Build the handler serving one validated public document."""
    try:
        prefix = api_major_prefix(plan)
    except Exception:
        raise _invalid_document() from None
    try:
        contract = object.__getattribute__(plan, "contract")
        contract_version = object.__getattribute__(contract, "version")
    except Exception:
        raise _invalid_document() from None
    if type(contract_version) is not str or contract_version == "":
        raise _invalid_document()
    if type(document) is not str or document == "" or len(document) > _MAX_DOCUMENT_CHARS:
        raise _invalid_document()
    try:
        body = document.encode("utf-8")
    except Exception:
        raise _invalid_document() from None
    if len(body) > _MAX_DOCUMENT_SIZE:
        raise _invalid_document()
    try:
        parsed = json.loads(body.decode("utf-8"), parse_constant=_reject_constant, object_pairs_hook=_reject_duplicate_keys)
    except OpenapiDocumentError:
        raise
    except Exception:
        raise _invalid_document() from None
    _walk_json(parsed, 0)
    _check_form(parsed, prefix, contract_version)

    def openapi_handler(request: object) -> object:
        method = _require_method(request)
        from django.http import HttpResponse

        if method == "GET":
            response = HttpResponse(body, status=200, content_type=_CONTENT_TYPE)
            response["Cache-Control"] = _NO_STORE
            response["Content-Length"] = str(len(body))
            return response
        if method == "HEAD":
            response = HttpResponse(b"", status=200, content_type=_CONTENT_TYPE)
            response["Cache-Control"] = _NO_STORE
            response["Content-Length"] = str(len(body))
            return response
        denied = HttpResponse(b"", status=405, content_type=_CONTENT_TYPE)
        denied["Cache-Control"] = _NO_STORE
        denied["Allow"] = _ALLOW_VALUE
        return denied

    return openapi_handler
