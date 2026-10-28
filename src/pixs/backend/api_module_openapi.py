"""Profil documentaire module : sous-ensemble OpenAPI 3.1.0 compatible C14.

Sous-ensemble explicite du vocabulaire Core, sans revendication universelle.
Valide les documents des proprietaires modules : operationId optionnel unique,
champs documentaires x-pixs-contract-id / x-pixs-document-ref optionnels ensemble,
schemes declares sous-ensemble exact des schemes connus, sans imposer BearerRefresh.
Les octets publies sont servis tels quels, sans normalisation ni metier.
"""
from __future__ import annotations

import re

from pixs.backend.api import ApiContractPlan, api_major_prefix
from pixs.backend.api_core_openapi import _content, _schema, _schemes
from pixs.backend.openapi_document_view import OpenapiDocumentError, _bounded_json_document, _preloaded_json_view

__all__ = ["validate_module_openapi_document", "build_module_document_view"]

_FORMAT = "3.1.0"
_METHODS = frozenset(("get", "post", "head"))
_ROOTS = frozenset(("openapi", "info", "paths", "components", "x-documents", "x-pixs-contract-id", "x-pixs-document-ref"))
_OPERATION_KEYS = frozenset(("parameters", "security", "responses", "requestBody", "operationId"))
_MAX_SIZE = 65536
_NAME_RE = "[A-Za-z][A-Za-z0-9_]*"
_SEGMENT_RE = r"[A-Za-z0-9_-]+(?:[.][A-Za-z0-9_-]+)*"
_STATUS_RE = r"[1-5][0-9]{2}"
_SHA_RE = r"[0-9a-f]{64}"


def _invalid():
    raise OpenapiDocumentError("Document OpenAPI module invalide.")


def _plan_version(plan):
    prefix = api_major_prefix(plan)
    if type(plan) is not ApiContractPlan:
        _invalid()
    try:
        contract = object.__getattribute__(plan, "contract")
        version = object.__getattribute__(contract, "version")
        contract_id = object.__getattribute__(contract, "contract_id")
        document_ref = object.__getattribute__(plan, "openapi_document_ref")
    except AttributeError:
        _invalid()
    if type(version) is not str or not version:
        _invalid()
    if type(contract_id) is not str or not contract_id:
        _invalid()
    if type(document_ref) is not str or not document_ref:
        _invalid()
    return prefix, version, contract_id, document_ref


def _check_root(root, version, contract_id, document_ref):
    if type(root) is not dict or not set(root) <= _ROOTS:
        _invalid()
    if root.get("openapi") != _FORMAT:
        _invalid()
    info = root.get("info")
    if type(info) is not dict or set(info) != {"title", "version"}:
        _invalid()
    title = info.get("title")
    if type(title) is not str or not title or title.strip() != title:
        _invalid()
    if info.get("version") != version:
        _invalid()
    present_id = "x-pixs-contract-id" in root
    present_ref = "x-pixs-document-ref" in root
    if present_id != present_ref:
        _invalid()
    if present_id:
        if root.get("x-pixs-contract-id") != contract_id:
            _invalid()
        if root.get("x-pixs-document-ref") != document_ref:
            _invalid()


def _check_components(root, known_schemes):
    components = root.get("components")
    if type(components) is not dict or set(components) != {"schemas", "securitySchemes"}:
        _invalid()
    schemas = components.get("schemas")
    declared_schemes = components.get("securitySchemes")
    if type(schemas) is not dict or type(declared_schemes) is not dict:
        _invalid()
    for name, scheme in declared_schemes.items():
        if type(name) is not str or name not in known_schemes or scheme != known_schemes[name]:
            _invalid()
    for name, node in schemas.items():
        if type(name) is not str or not re.fullmatch(_NAME_RE, name):
            _invalid()
        _schema(node, set(schemas))
    return schemas, declared_schemes


def _check_paths(root, prefix, schemas, declared_schemes):
    paths = root.get("paths")
    if type(paths) is not dict or not paths:
        _invalid()
    seen_operation_ids = set()
    for path, methods in paths.items():
        if type(path) is not str or not path.startswith(prefix + "/"):
            _invalid()
        expected = set()
        for segment in path[len(prefix) + 1:].split("/"):
            if re.fullmatch(r"\{(?:tenant_id|scope_id)\}", segment):
                expected.add(segment[1:-1])
            elif not re.fullmatch(_SEGMENT_RE, segment):
                _invalid()
        if type(methods) is not dict or not methods or not set(methods) <= _METHODS:
            _invalid()
        for method, operation in methods.items():
            _check_operation(operation, expected, schemas, declared_schemes, seen_operation_ids)
    return paths


def _check_operation(operation, expected, schemas, declared_schemes, seen_operation_ids):
    if type(operation) is not dict or not set(operation) <= _OPERATION_KEYS:
        _invalid()
    if "operationId" in operation:
        operation_id = operation.get("operationId")
        if type(operation_id) is not str or not operation_id or operation_id in seen_operation_ids:
            _invalid()
        seen_operation_ids.add(operation_id)
    security = operation.get("security")
    if type(security) is not list:
        _invalid()
    for requirement in security:
        if type(requirement) is not dict or len(requirement) != 1:
            _invalid()
        for name, scopes in requirement.items():
            if name not in declared_schemes or scopes != []:
                _invalid()
    parameters = operation.get("parameters")
    if type(parameters) is not list:
        _invalid()
    seen = set()
    declared_parameters = set()
    for parameter in parameters:
        if (type(parameter) is not dict
                or not {"name", "in", "required", "schema"} <= set(parameter)
                or not set(parameter) <= {"name", "in", "required", "schema", "style", "explode"}):
            _invalid()
        if parameter["in"] not in ("path", "query", "header"):
            _invalid()
        if type(parameter["name"]) is not str or not parameter["name"]:
            _invalid()
        if type(parameter["required"]) is not bool:
            _invalid()
        key = (parameter["in"], parameter["name"].lower() if parameter["in"] == "header" else parameter["name"])
        if key in seen:
            _invalid()
        seen.add(key)
        if parameter["in"] == "path":
            if parameter["required"] is not True:
                _invalid()
            declared_parameters.add(parameter["name"])
        if "explode" in parameter and type(parameter["explode"]) is not bool:
            _invalid()
        if "style" in parameter and (parameter["style"] != "form" or parameter.get("explode") is not True):
            _invalid()
        _schema(parameter["schema"], set(schemas))
    if declared_parameters != expected:
        _invalid()
    body = operation.get("requestBody")
    if body is not None:
        if type(body) is not dict or set(body) != {"required", "content"} or body["required"] is not True:
            _invalid()
        _content(body["content"], schemas)
    responses = operation.get("responses")
    if type(responses) is not dict or "200" not in responses:
        _invalid()
    for status, response in responses.items():
        if type(status) is not str or not re.fullmatch(_STATUS_RE, status):
            _invalid()
        if type(response) is not dict or not set(response) <= {"description", "content"}:
            _invalid()
        if type(response.get("description")) is not str:
            _invalid()
        if "content" in response:
            _content(response["content"], schemas)


def _check_index(root, paths):
    if "x-documents" not in root:
        return
    index = root.get("x-documents")
    if type(index) is not list or not index:
        _invalid()
    seen = set()
    for entry in index:
        if type(entry) is not dict or set(entry) != {"href", "sha256", "bytes"}:
            _invalid()
        if entry["href"] not in paths or entry["href"] in seen:
            _invalid()
        if type(entry["sha256"]) is not str or not re.fullmatch(_SHA_RE, entry["sha256"]):
            _invalid()
        if type(entry["bytes"]) is not int or not 1 <= entry["bytes"] <= _MAX_SIZE:
            _invalid()
        seen.add(entry["href"])


def validate_module_openapi_document(plan: ApiContractPlan, document: str) -> dict[str, object]:
    """Valide le vocabulaire documentaire module et retourne le JSON verifie."""
    try:
        prefix, version, contract_id, document_ref = _plan_version(plan)
        _body, root = _bounded_json_document(document, local_references=True)
        _check_root(root, version, contract_id, document_ref)
        known_schemes = _schemes()
        schemas, declared_schemes = _check_components(root, known_schemes)
        paths = _check_paths(root, prefix, schemas, declared_schemes)
        _check_index(root, paths)
    except OpenapiDocumentError:
        raise
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError):
        raise OpenapiDocumentError("Document OpenAPI module invalide.") from None
    return root


def build_module_document_view(plan, document):
    """Valide puis sert les octets originaux, sans normaliser ni enrichir."""
    validate_module_openapi_document(plan, document)
    body, _root = _bounded_json_document(document, local_references=True)
    return _preloaded_json_view(body)
