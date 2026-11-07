"""Documents OpenAPI C14 déclaratifs, sans montage HTTP ni preuve d'exécution."""
from __future__ import annotations

from dataclasses import fields

from pixs.backend.api_core_catalog import API_UUID7_PATTERN
from pixs.backend.api_core_errors_catalog import error_schema
from pixs.backend.api_pzt_dns_catalog import (
    C14_HTTP_BINDINGS, C14_HTTP_VERSION, C14HttpCatalogError,
    c14_api_contract_plan, c14_http_binding,
)
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_governance_profile import DataGovernanceProfile
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState

__all__ = [
    "build_c14_openapi_document", "build_c14_openapi_documents", "c14_http_request_schema", "c14_http_response_schema",
]


def _text():
    return {"type": "string", "minLength": 1}


def _integer(minimum=0, maximum=None):
    value = {"type": "integer", "minimum": minimum}
    if maximum is not None:
        value["maximum"] = maximum
    return value


def _object(properties):
    return {"type": "object", "additionalProperties": False,
            "properties": properties, "required": list(properties)}


def _nullable(schema):
    return {"anyOf": [schema, {"type": "null"}]}


def _array(schema, *, unique=False, nonempty=False):
    result = {"type": "array", "items": schema}
    if unique:
        result["uniqueItems"] = True
    if nonempty:
        result["minItems"] = 1
    return result


def _governance():
    sets = frozenset(("data_classes", "purpose_refs", "residency_constraints",
                      "authorized_consumers", "processor_refs"))
    properties = {}
    for f in fields(DataGovernanceProfile):
        if f.name in sets:
            properties[f.name] = _array(_text(), unique=True)
        elif f.name == "confidentiality":
            properties[f.name] = {"type": "string", "enum": [v.value for v in ConfidentialityLevel]}
        elif f.name == "personal_data":
            properties[f.name] = {"type": "string", "enum": [v.value for v in PersonalDataLevel]}
        else:
            properties[f.name] = _text()
    return _object(properties)


def _configuration(owner):
    properties = {
        "schema_version": {"type": "string", "const": C14_HTTP_VERSION},
        "owner_id": {"type": "string", "const": owner},
        "config_revision": _integer(1),
        "governance": _governance(),
        "secret_refs": _array(_object({k: _text() for k in ("owner_id", "entry_id", "source")})),
    }
    if owner == "pixs.pzt":
        properties.update(v6_enabled={"type": "boolean"}, plan_ref=_text(), budget_ref=_text())
    else:
        properties.update(suffix=_text(), ttl_positive=_integer(0, 30),
                          ttl_negative=_integer(0, 5), views=_array(_text(), nonempty=True))
    return _object(properties)


def c14_http_request_schema(owner, kind, name):
    """Schéma fermé des champs JSON, distinct de Request/CommandMetadata serveur."""
    binding = c14_http_binding(owner, kind, name)
    properties = {"resource_id": _text()}
    if binding.kind == "COMMAND":
        properties.update(schema_version={"type": "string", "const": C14_HTTP_VERSION},
                          expected_revision=_integer())
        if binding.name in ("declare_desired_pzt", "declare_desired_dns"):
            properties["configuration"] = _configuration(binding.owner)
        elif binding.name in ("retire_desired_pzt", "retire_desired_dns"):
            properties["reason"] = _text()
        else:
            properties.update(name=_text(), view=_text())
            if binding.name == "declare_name":
                properties["target_ref"] = _text()
    elif binding.name == "resolve_view_policy":
        properties.update(view=_text(), name=_text())
    result = _object(properties)
    if binding.kind == "COMMAND":
        result["properties"]["authorization_intent"] = _object({
            "waive_audit": {"type": "boolean"}, "waive_governance": {"type": "boolean"}})
    else:
        result["properties"].update(waive_audit={"type": "boolean"},
                                    waive_governance={"type": "boolean"})
    return result


def _context():
    return {"oneOf": [
        _object({"scope_type": {"type": "string", "const": "PLATFORM"},
                 "tenant_id": {"type": "null"}, "scope_id": {"type": "null"}}),
        _object({"scope_type": {"type": "string", "const": "TENANT"},
                 "tenant_id": _text(), "scope_id": _nullable(_text())}),
    ]}


def _envelope(data, *, with_activity=False):
    meta = _object({"correlation_id": _text(), "context": _context()})
    if with_activity:
        meta["properties"]["activity"] = {"oneOf": [
            _object({"status": {"type": "string", "enum": ["RECORDED", "REPLAY_IGNORED"]}}),
            _object({"status": {"type": "string", "const": "NOT_RECORDED"},
                     "error_code": error_schema()["properties"]["error_code"]}),
        ]}
    return _object({"data": data, "meta": meta, "links": _object({})})


def c14_http_response_schema(owner, kind, name, *, unknown=False):
    """Une issue inconnue ne peut décrire un résultat confirmé ou une mesure."""
    binding = c14_http_binding(owner, kind, name)
    if type(unknown) is not bool or (unknown and binding.kind != "COMMAND"):
        raise C14HttpCatalogError()
    if binding.kind == "COMMAND":
        data = _object({
            "operation_id": _text(), "resource_id": _text(),
            "config_revision": {"type": "null"} if unknown else _integer(1),
            "outcome": {"type": "string", "const": "UNKNOWN" if unknown else "SUCCEEDED"},
            "audit_disposition": {"type": "string", "enum":
                                  ["AUDITED", "WAIVED", "UNKNOWN"] if unknown else ["AUDITED", "WAIVED"]},
        })
    elif binding.name in ("get_desired_pzt", "get_desired_dns"):
        data = _object({
            "schema_version": {"type": "string", "const": C14_HTTP_VERSION},
            "resource_id": _text(), "config_revision": _integer(1),
            "business_state": {"type": "string", "enum": ["DECLARED", "RETIRED"]},
            "persistence_state": {"type": "string", "enum": [v.value for v in DataPersistenceState]},
            "retention_state": {"type": "string", "enum": [v.value for v in DataRetentionState]},
            "configuration": _configuration(binding.owner),
        })
    elif binding.name in ("get_applied_pzt", "get_applied_dns"):
        properties = {"resource_id": _text(), "desired_revision": _integer(1)}
        properties.update({k: {"type": "null"} for k in (
            "applied_revision", "applied_present", "generation", "observed_at", "valid_until", "measurements")})
        properties.update(application_status={"type": "string", "const": "UNKNOWN"},
                          measurement_status={"type": "string", "const": "UNMEASURED"})
        data = _object(properties)
    else:
        data = _object({
            "resource_id": _text(), "desired_revision": _integer(1), "view": _text(), "name_key": _text(),
            "desired_name_present": {"type": "boolean"}, "desired_target_ref": _nullable(_text()),
            "target_verification": {"type": "string", "const": "UNVERIFIED"},
            "ttl_positive_ceiling": _integer(0, 30), "ttl_negative_ceiling": _integer(0, 5),
            "applied_revision": {"type": "null"}, "applied_present": {"type": "null"},
            "application_status": {"type": "string", "const": "UNKNOWN"},
            "measurement_status": {"type": "string", "const": "UNMEASURED"},
        })
    return _envelope(data, with_activity=binding.kind == "COMMAND" and not unknown)


def _error():
    result = _object({"error_code": _text(), "message": _text(),
                    "details": {"type": "object"}, "field_errors": _array({"type": "object"}),
                    "correlation_id": _text()})
    result["required"].remove("field_errors")
    return result


def _ref(name):
    return {"$ref": "#/components/schemas/" + name}


def _response(description, schema):
    return {"description": description, "content": {"application/json": {"schema": schema}}}


def build_c14_openapi_document(owner):
    """Document frais par propriétaire ; sa présence ne prouve pas sa publication."""
    plan = c14_api_contract_plan(owner)
    bindings = tuple(b for b in C14_HTTP_BINDINGS if b.owner == owner)
    schemas = {"Error": _error()}
    paths = {}
    for binding in bindings:
        input_name, output_name = "Input_" + binding.name, "Output_" + binding.name
        schemas[input_name] = c14_http_request_schema(owner, binding.kind, binding.name)
        schemas[output_name] = c14_http_response_schema(owner, binding.kind, binding.name)
        if binding.kind == "COMMAND":
            schemas["Unknown_" + binding.name] = c14_http_response_schema(
                owner, binding.kind, binding.name, unknown=True)
        for web in (False, True):
            prefix = "/api/v1/web" if web else "/api/v1"
            for mode, context, path_keys in (
                ("P", "/platform", ()),
                ("T", "/tenants/{tenant_id}", ("tenant_id",)),
                ("S", "/tenants/{tenant_id}/scopes/{scope_id}", ("tenant_id", "scope_id")),
            ):
                path = prefix + context + "/" + "/".join(binding.segments)
                parameters = [
                    {"name": k, "in": "path", "required": True, "schema": _text()}
                    for k in path_keys
                ]
                parameters.append({"name": "X-Correlation-ID", "in": "header",
                                   "required": False, "schema": _text()})
                if web:
                    parameters.append({
                        "name": "X-Shell-Session-ID", "in": "header", "required": False,
                        "schema": {"type": "string", "pattern": API_UUID7_PATTERN},
                    })
                if binding.kind == "QUERY":
                    parameters.extend({"name": k, "in": "query", "required": True, "schema": _text()}
                                      for k in binding.query_fields)
                    parameters.extend({"name": k, "in": "query", "required": False,
                                       "schema": {"type": "boolean"}}
                                      for k in ("waive_audit", "waive_governance"))
                else:
                    parameters.append({"name": "Idempotency-Key", "in": "header",
                                       "required": True, "schema": _text()})
                    if web:
                        parameters.extend({"name": k, "in": "header", "required": True, "schema": _text()}
                                          for k in ("Origin", "X-CSRFToken"))
                responses = {"200": _response("Résultat propriétaire confirmé.", _ref(output_name))}
                if binding.kind == "COMMAND":
                    responses["202"] = _response("Issue inconnue à rapprocher ; aucune réussite annoncée.",
                                                 _ref("Unknown_" + binding.name))
                for status in ("400", "401", "403", "404", "405", "409", "413", "500", "503"):
                    responses[status] = _response("Refus public stable.", _ref("Error"))
                operation = {
                    "operationId": owner + "." + ("web" if web else "api") + "." + mode + "." + binding.name,
                    "parameters": parameters,
                    "security": [{"WebSession" if web else "BearerAccess": []}],
                    "responses": responses,
                }
                if binding.kind == "COMMAND":
                    operation["requestBody"] = {
                        "required": True, "content": {"application/json": {"schema": _ref(input_name)}}}
                methods = paths.setdefault(path, {})
                method = binding.method.lower()
                if method in methods:
                    raise C14HttpCatalogError()
                methods[method] = operation
    return {
        "openapi": "3.1.0", "info": {"title": "Pixs " + owner + " — gestion souhaitée",
                                   "version": plan.contract.version},
        "x-pixs-contract-id": plan.contract.contract_id,
        "x-pixs-document-ref": plan.openapi_document_ref,
        "paths": paths,
        "components": {
            "schemas": schemas,
            "securitySchemes": {
                "BearerAccess": {"type": "http", "scheme": "bearer", "bearerFormat": "C03 ACCESS"},
                "WebSession": {"type": "apiKey", "in": "cookie", "name": "__Host-pixs-session"},
            },
        },
    }


def build_c14_openapi_documents(owner):
    """Index et fragments publics déterministes, chacun borné à 64 Kio.

    Le document logique complet reste utile aux contrôles de couverture. Seuls
    les octets des fragments et de cet index sont exposés par le transport.
    """
    import hashlib
    import json

    full = build_c14_openapi_document(owner)
    short = owner.removeprefix("pixs.")
    maximum = 65536

    def dump(document):
        return json.dumps(document, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False)

    def render(paths):
        return dump({**full, "paths": paths})

    documents = []
    chunk = {}
    number = 1
    for path, methods in sorted(full["paths"].items()):
        candidate = {**chunk, path: methods}
        if len(render(candidate).encode("utf-8")) > maximum:
            if not chunk:
                raise C14HttpCatalogError()
            documents.append((
                "/api/v1/openapi/" + short + "-management-" + str(number) + ".json",
                render(chunk)))
            number += 1
            chunk = {path: methods}
            if len(render(chunk).encode("utf-8")) > maximum:
                raise C14HttpCatalogError()
        else:
            chunk = candidate
    if chunk:
        documents.append((
            "/api/v1/openapi/" + short + "-management-" + str(number) + ".json",
            render(chunk)))

    operation = {
        "parameters": [], "security": [],
        "responses": {
            "200": _response("Document public borné.", _ref("PublicDocument")),
            "403": _response("Transport ou origine refusé.", _ref("Error")),
            "405": _response("Méthode refusée.", _ref("Error")),
        },
    }
    index_path = "/api/v1/openapi/" + short + "-management.json"
    paths = {path: {"get": operation, "head": operation} for path, _ in documents}
    paths[index_path] = {"get": operation, "head": operation}
    entries = [
        {"href": path, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
         "bytes": len(text.encode("utf-8"))}
        for path, text in documents
    ]
    index = {
        **full, "paths": paths,
        "components": {
            "schemas": {"PublicDocument": {"type": "object"},
                        "Error": full["components"]["schemas"]["Error"]},
            "securitySchemes": {},
        },
        "x-documents": entries,
    }
    documents.insert(0, (index_path, dump(index)))
    if any(len(text.encode("utf-8")) > maximum for _, text in documents):
        raise C14HttpCatalogError()
    return tuple(documents)
