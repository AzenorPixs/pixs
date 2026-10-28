"""Façade WEB du contexte Auth : chemin canonique et contrat public versionné.

Les URLs retournées sont montées explicitement avant le catchall Core.
"""
from __future__ import annotations

import json as _json

from django.urls import path as _path_url, re_path as _re_path

from pixs.auth.shell_context import PostgresShellContextService, SHELL_CONTEXT_VERSION
from pixs.backend.api import ApiContractPlan
from pixs.backend.api_module_views import ModuleHttpComposition
from pixs.backend.api_module_views import build_module_openapi_view as _build_module_doc_view
from pixs.backend.api_shell_transports import build_shell_transport_resolver as _build_resolver
from pixs.backend.api_shell_transports import shell_transport_resolver_schema as _resolver_schema
from pixs.auth.policy import SessionCategory
from pixs.core.authz.policy import IdentityAssurance, AuthenticationAssurance
from pixs.backend.api_core_catalog import API_UUID7_PATTERN
from pixs.backend.api_core_errors_catalog import CoreApiError as _CoreError, error_schema
from pixs.backend.api_core_openapi import (
    _object, _reference, _nullable, _schemes, validate_core_openapi_document,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor

__all__ = ['shell_context_api_plan', 'build_shell_context_openapi_document', 'build_shell_context_view', 'build_shell_context_urls']

_SHELL_VERSION = SHELL_CONTEXT_VERSION
_SHELL_CONTRACT_ID = 'pixs.auth.shell.context.api'
_SHELL_DOCUMENT_REF = 'pixs-auth-shell-context-api-v1'
_SHELL_DOCUMENT_PATH = 'api/v1/openapi/shell-context.json'


def shell_context_api_plan():
    return ApiContractPlan(ContractDescriptor(_SHELL_CONTRACT_ID, ContractCategory.API, _SHELL_VERSION, 'pixs.auth', 'Contexte WEB possede par Auth, projection blanche sans secret ni jeton.'), _SHELL_DOCUMENT_REF)


def _shell_schemas(http_composition):
    text = {'type': 'string', 'minLength': 1,
            'maxLength': http_composition.input_limits.max_reference_chars}
    correlation = {'type': 'string', 'minLength': 1, 'maxLength': 128}
    scope = _object({
        'scope_type': {'type': 'string', 'enum': ['PLATFORM', 'TENANT']},
        'tenant_id': _nullable(text),
        'scope_id': _nullable(text),
    })
    utc_time = {'type': 'string', 'format': 'date-time', 'pattern': '(?:Z|[+]00:00)$'}
    context = _object({
        'identity_ref': text,
        'scope': _reference('ScopeContext'),
        'session_id': {'type': 'string', 'pattern': API_UUID7_PATTERN},
        'category': {'type': 'string', 'enum': [value.value for value in SessionCategory]},
        'facade': {'type': 'string', 'const': 'WEB'},
        'authentication_time': utc_time,
        'expires_at': utc_time,
        'identity_assurance': {'type': 'string', 'enum': [value.value for value in IdentityAssurance]},
        'authentication_assurance': {'type': 'string', 'enum': [value.value for value in AuthenticationAssurance]},
        'ui_permissions': _object({
            'status': {'type': 'string', 'const': 'UNAVAILABLE'},
            'items': {'type': 'array', 'maxItems': 0},
        }),
    })
    meta = _object({
        'correlation_id': correlation,
        'context': _reference('ScopeContext'),
        'transport_resolver': _reference('TransportResolver'),
    })
    envelope = _object({
        'data': _reference('ShellContext'),
        'meta': _reference('ShellMeta'),
        'links': _object({}),
    })
    return {'ScopeContext': scope, 'ShellContext': context,
            'ShellMeta': meta, 'ShellEnvelope': envelope, 'ShellError': error_schema(),
            'TransportResolver': _resolver_schema()}


def build_shell_context_openapi_document(http_composition, *, module_bindings=()):
    _build_resolver(module_bindings=module_bindings)
    if type(http_composition) is not ModuleHttpComposition:
        raise ValueError('Composition module requise.')
    http_composition.__post_init__()
    plan = shell_context_api_plan()
    maximum = http_composition.input_limits.max_reference_chars
    text = {'type': 'string', 'minLength': 1, 'maxLength': maximum}
    correlation_param = {'name': 'X-Correlation-ID', 'in': 'header', 'required': False, 'schema': {'type': 'string', 'minLength': 1, 'maxLength': 128}}
    origin_param = {'name': 'Origin', 'in': 'header', 'required': False, 'schema': {'type': 'string', 'const': http_composition.approved_origin}}
    failures = (
        ('400', 'Requête invalide.'),
        ('401', 'Authentification requise.'),
        ('403', 'Accès refusé.'),
        ('404', 'Ressource introuvable.'),
        ('405', 'Méthode non admise.'),
        ('409', 'Conflit de ressource.'),
        ('413', 'Requête trop volumineuse.'),
        ('500', 'Erreur interne.'),
        ('503', 'Service indisponible.'),
    )
    error_responses = {
        status: {'description': message, 'content': {
            'application/json': {'schema': _reference('ShellError')}}}
        for status, message in failures
    }
    def operation(mode):
        parameters = [correlation_param, origin_param]
        if mode in ('T', 'S'):
            parameters.append({'name': 'tenant_id', 'in': 'path', 'required': True, 'schema': text})
        if mode == 'S':
            parameters.append({'name': 'scope_id', 'in': 'path', 'required': True, 'schema': text})
        responses = {'200': {'description': 'Contexte WEB projete.', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ShellEnvelope'}}}}}
        responses.update(error_responses)
        return {'parameters': parameters, 'security': [{'WebSession': []}], 'responses': responses}
    paths = {'/api/v1/web/platform/shell/context': {'get': operation('P')}, '/api/v1/web/tenants/{tenant_id}/shell/context': {'get': operation('T')}, '/api/v1/web/tenants/{tenant_id}/scopes/{scope_id}/shell/context': {'get': operation('S')}}
    root = {'openapi': '3.1.0', 'info': {'title': 'Pixs Shell Context HTTP', 'version': plan.contract.version}, 'paths': paths, 'components': {'schemas': _shell_schemas(http_composition), 'securitySchemes': _schemes()}}
    document = _json.dumps(root, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    validate_core_openapi_document(plan, document)
    return document


def build_shell_context_view(service, http_composition, *, module_bindings=()):
    _resolver = _build_resolver(module_bindings=module_bindings)
    if type(service) is not PostgresShellContextService:
        raise ValueError('Producteur Auth exact requis.')
    if type(http_composition) is not ModuleHttpComposition:
        raise ValueError('Composition module requise.')
    http_composition.__post_init__()
    if service.request_source is not http_composition.request_source:
        raise ValueError('Source Auth commune requise.')
    def view(request, **ignored):
        from pixs.backend.api_core_views import _actor as _core_actor
        from pixs.backend.api_core_views import _context_json as _core_context_json
        from pixs.backend.api_core_views import _error as _core_error
        from pixs.backend.api_core_views import _language as _core_language
        from pixs.backend.api_core_views import _method as _core_method
        from pixs.backend.api_core_views import _path as _core_path
        from pixs.backend.api_core_views import _response as _core_response
        from pixs.backend.api_core_views import _route as _core_route
        from pixs.backend.api_core_views import _text as _core_text
        from pixs.backend.api_core_views import _transport as _core_transport
        from pixs.backend.api_core_errors_catalog import classify_error as _classify
        from pixs.core.persistence.uuid7 import generate_uuid7 as _uuid
        correlation = str(_uuid())
        language = _core_language(request)
        try:
            supplied = request.headers.get('X-Correlation-ID')
            if supplied is not None:
                supplied = _core_text(supplied, 128)
                if any(c in supplied for c in (chr(10), chr(13))):
                    raise _CoreError('INPUT_INVALID')
                correlation = supplied
            parts, raw_path, available = _core_path(request)
            web, context, tail = _core_route(parts, available)
            if web is not True or list(tail) != ['shell', 'context']:
                raise _CoreError('NOT_FOUND')
            for value in (context.tenant_id, context.scope_id):
                if value is not None:
                    _core_text(value, http_composition.input_limits.max_reference_chars)
            for header, expected in (('X-Tenant-ID', context.tenant_id), ('X-Scope-ID', context.scope_id)):
                if request.headers.get(header) is not None and request.headers[header] != expected:
                    raise _CoreError('CONTEXT_MISMATCH')
            _core_transport(request, http_composition, web, False)
            _core_method(request, 'GET')
            if request.META.get('QUERY_STRING', ''):
                raise _CoreError('INPUT_INVALID')
            if request.headers.get('Idempotency-Key') is not None:
                raise _CoreError('INPUT_INVALID')
            actor, token, kind = _core_actor(request, http_composition, context, web)
            projection = service.read_context(actor=actor, token=token, kind=kind, correlation_id=correlation)
            if type(projection) is not dict or set(projection) != set(['identity_ref', 'scope', 'session_id', 'category', 'facade', 'authentication_time', 'expires_at', 'identity_assurance', 'authentication_assurance', 'ui_permissions']):
                raise _CoreError('INTERNAL_ERROR')
            if (projection['scope'] != _core_context_json(context)
                    or projection['identity_ref'] != actor.identity_ref
                    or projection['session_id'] != str(actor.session_id)
                    or projection['facade'] != 'WEB'):
                raise _CoreError('INTERNAL_ERROR')
            transport = {'version': _resolver['version'], 'operations': [{**operation, 'scopes': list(operation['scopes']), 'segments': list(operation['segments'])} for operation in _resolver['operations']]}
            meta = {'correlation_id': correlation, 'context': _core_context_json(context), 'transport_resolver': transport}
            return _core_response(projection, meta=meta, links={}, status=200)
        except Exception as cause:
            return _core_error(_classify(cause), correlation, language)
    return view


def build_shell_context_urls(service, http_composition, *, module_bindings=()):
    view = build_shell_context_view(service, http_composition, module_bindings=module_bindings)
    plan = shell_context_api_plan()
    document = build_shell_context_openapi_document(http_composition, module_bindings=module_bindings)
    validate_core_openapi_document(plan, document)
    document_view = _build_module_doc_view(http_composition, plan=plan, document=document)
    result = [_path_url(_SHELL_DOCUMENT_PATH, document_view, name='pixs-shell-context-openapi')]
    result.append(_re_path(r'(?s)^api/v1/web/(?:platform|tenants/.+)/shell/context$', view, name='pixs-shell-context-api-v1'))
    return result
