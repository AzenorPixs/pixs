"""Raccord C14 aux frontières HTTP publiques du propriétaire C11/C06.

Les exports ModuleHttp* sont une dépendance explicite. Leur absence ferme la
construction de l'hôte ; aucun transport ou contrôle de sécurité n'est remplacé.
"""
from __future__ import annotations

from pixs.backend.api_pzt_dns_catalog import C14_HTTP_BINDINGS, C14_HTTP_VERSION, c14_api_contract_plan
from pixs.backend.api_pzt_dns_dispatch import C14ApiComposition, C14WaiverIntent, dispatch_c14_operation
from pixs.backend.api_pzt_dns_errors import project_c14_http_error
from pixs.backend.api_pzt_dns_inputs import C14HttpInputError
from pixs.backend.api_pzt_dns_openapi import build_c14_openapi_documents

__all__ = ["build_c14_module_bindings", "build_c14_api_view", "build_c14_api_urls"]


def _body_and_intent(binding, boundary):
    intent = None
    if binding.kind == "COMMAND":
        if type(boundary.body) is not dict:
            raise C14HttpInputError()
        data = dict(boundary.body)
        if "authorization_intent" in data:
            item = data.pop("authorization_intent")
            if (type(item) is not dict
                    or any(type(k) is not str for k in item)
                    or set(item) != {"waive_audit", "waive_governance"}):
                raise C14HttpInputError()
            intent = C14WaiverIntent(item["waive_audit"], item["waive_governance"])
        return data, intent
    if type(boundary.query_pairs) is not tuple:
        raise C14HttpInputError()
    data = {}
    for pair in boundary.query_pairs:
        if (type(pair) is not tuple or len(pair) != 2 or type(pair[0]) is not str
                or type(pair[1]) is not str or pair[0] in data):
            raise C14HttpInputError()
        data[pair[0]] = pair[1]
    if "waive_audit" in data or "waive_governance" in data:
        values = {}
        for name in ("waive_audit", "waive_governance"):
            if name in data:
                literal = data.pop(name)
                if literal not in ("true", "false"):
                    raise C14HttpInputError()
                values[name] = literal == "true"
            else:
                # Une dispense non demandée n'est jamais accordée implicitement.
                values[name] = False
        intent = C14WaiverIntent(values["waive_audit"], values["waive_governance"])
    return data, intent


def build_c14_module_bindings():
    from pixs.backend.api_core_views import ModuleHttpBinding
    return tuple(
        ModuleHttpBinding(
            owner=b.owner, kind=b.kind, name=b.name, contract_id=b.contract_id,
            contract_version=C14_HTTP_VERSION, scopes=("P", "T", "S"), segments=b.segments,
            query_fields=b.query_fields + (("waive_audit", "waive_governance") if b.kind == "QUERY" else ()))
        for b in C14_HTTP_BINDINGS
    )


def build_c14_api_view(composition, http_composition):
    """Monte le dispatch sur les gardes HTTPS/Host/Origin/CSRF/acteur de C11."""
    from pixs.backend.api_core_views import (
        ModuleHttpComposition, ModuleHttpRequest, ModuleHttpResult, build_module_api_view,
    )
    if type(composition) is not C14ApiComposition or type(http_composition) is not ModuleHttpComposition:
        raise C14HttpInputError()
    composition.__post_init__()
    if composition.request_source is not http_composition.request_source:
        raise C14HttpInputError()

    def dispatch(binding, boundary):
        if type(boundary) is not ModuleHttpRequest:
            raise C14HttpInputError()
        try:
            if boundary.actor.context != boundary.context:
                raise C14HttpInputError()
            payload, intent = _body_and_intent(binding, boundary)
            result = dispatch_c14_operation(
                composition, owner=binding.owner, kind=binding.kind, name=binding.name,
                payload=payload, actor=boundary.actor, token=boundary.token,
                token_kind=boundary.token_kind, correlation_id=boundary.correlation_id,
                idempotency_key=boundary.idempotency_key, waiver_intent=intent)
            return ModuleHttpResult(
                status=result.status, data=result.body["data"], links=result.body["links"], error=None,
                activity=result.body["meta"].get("activity"))
        except Exception as cause:
            # Frontière de projection : aucun texte ni attribut inconnu d'exception n'est exposé.
            projected = project_c14_http_error(binding.owner, cause, language=boundary.language)
            return ModuleHttpResult(status=projected.status, data=None, links={}, error=projected.error,
                                    activity=None)

    return build_module_api_view(http_composition, bindings=build_c14_module_bindings(), dispatch=dispatch)


def build_c14_api_urls(composition, http_composition):
    """URLs de gestion et documents bornés, avant le catchall Core de l'hôte."""
    from django.urls import path, re_path
    from pixs.backend.api_core_views import build_module_openapi_view
    management = build_c14_api_view(composition, http_composition)
    result = []
    for owner in ("pixs.pzt", "pixs.dns"):
        for number, (document_path, document) in enumerate(build_c14_openapi_documents(owner)):
            view = build_module_openapi_view(
                http_composition, plan=c14_api_contract_plan(owner), document=document)
            name = "pixs-" + owner.removeprefix("pixs.") + "-management-api-v1"
            if number:
                name += "-part-" + str(number)
            result.append(path(document_path.removeprefix("/"), view, name=name))
    result.append(re_path(
        r"(?s)^api/v1/(?:web/)?(?:platform|tenants/.+)/(?:pzt|dns)/(?:commands|queries)/[^/]+$",
        management, name="pixs-c14-management-api-v1"))
    return result
