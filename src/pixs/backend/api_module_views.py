"""Frontières HTTP propriétaires : transport commun, aucune autorité implicite.

L’acteur résolu oriente le dispatch ; le propriétaire revalide Auth dans sa
transaction et sous ses verrous avant tout accès ou effet métier.
"""
from __future__ import annotations

import re as _re
import urllib.parse as _url
from dataclasses import dataclass as _dataclass
from urllib.parse import urlsplit as _urlsplit

from django.http import JsonResponse as _JsonResponse

from pixs.auth.api_request_source import ApiRequestSource as _ApiRequestSource
from pixs.auth.api_request_source import ResolvedActor as _ResolvedActor
from pixs.auth.contracts import Facade as _Facade
from pixs.auth.tokens import OpaqueToken as _OpaqueToken
from pixs.auth.tokens import TokenKind as _TokenKind
from pixs.backend.api_core_catalog import ApiInputLimits as _ApiInputLimits
from pixs.backend.api_core_composition import CoreHttpLimits as _CoreHttpLimits
from pixs.backend.api_core_errors_catalog import CoreApiError as _CoreApiError
from pixs.backend.api_core_errors_catalog import classify_error as _classify_error
from pixs.core.persistence.uuid7 import generate_uuid7 as _generate_uuid7
from pixs.core.scope.context import ScopeContext as _ScopeContext
from pixs.core.scope.context import ScopeStructureError as _ScopeStructureError
from pixs.core.scope.context import ScopeType as _ScopeType
from pixs.core.scope.context import validate_structure as _validate_structure

__all__ = ['ModuleHttpComposition', 'ModuleHttpBinding', 'ModuleHttpRequest', 'ModuleHttpResult', 'build_module_api_view', 'build_module_openapi_view']

_OWNER_RE = r'^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+$'
_NAME_RE = r'^[A-Za-z][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_-]+)*$'
_FIELD_RE = r'^[a-z][a-z0-9_]*$'
_SEGMENT_RE = r'^[A-Za-z0-9_-]+$'
_SEMVER_RE = (
    r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'
    r'(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)'
    r'(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?'
    r'(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
)
_SCOPES = frozenset(['P', 'T', 'S'])
_PROTECTED_OWNERS = frozenset(['pixs.core', 'pixs.auth', 'pixs.shell', 'pixs.kernel'])
_PROTECTED_SEGMENTS = frozenset(['auth', 'csrf', 'shell', 'shell-context'])
_ACTIVITY_OK = frozenset(['RECORDED', 'REPLAY_IGNORED'])

def _fail_value(message):
    raise ValueError(message)

def _check_text(value, maximum):
    if type(value) is not str or not value or len(value) > maximum or chr(0) in value:
        _fail_value('Texte module invalide.')
    try:
        value.encode('utf-8')
    except UnicodeError:
        _fail_value('Texte module invalide.')
    return value

def _check_owner(value):
    if type(value) is not str or not _re.fullmatch(_OWNER_RE, value):
        _fail_value('Proprietaire module invalide.')
    for protected in _PROTECTED_OWNERS:
        if value == protected or value.startswith(protected + '.'):
            _fail_value('Proprietaire reserve.')
    return value

def _check_contract_id(owner, value):
    if type(value) is not str:
        _fail_value('Contrat module invalide.')
    if not _re.fullmatch(_OWNER_RE, value):
        _fail_value('Contrat module invalide.')
    if not (value == owner or value.startswith(owner + '.')):
        _fail_value('Contrat hors proprietaire.')
    return value

def _assert_json_finite(value):
    active = set()
    pending = [(value, False)]
    while pending:
        item, exit_frame = pending.pop()
        if exit_frame:
            active.remove(id(item))
            continue
        if item is None or type(item) in (bool, int):
            continue
        if type(item) is float:
            if item != item or item in (float('inf'), float('-inf')):
                _fail_value('JSON non fini.')
            continue
        if type(item) is str:
            try:
                item.encode('utf-8')
            except UnicodeError:
                _fail_value('JSON invalide.')
            if chr(0) in item:
                _fail_value('JSON invalide.')
            continue
        if type(item) not in (list, dict) or id(item) in active:
            _fail_value('JSON cyclique ou non conforme.')
        active.add(id(item))
        pending.append((item, True))
        if type(item) is dict:
            for key, child in item.items():
                if type(key) is not str:
                    _fail_value('Clé JSON invalide.')
                pending.append((key, False))
                pending.append((child, False))
        else:
            pending.extend((child, False) for child in item)

@_dataclass(frozen=True, slots=True, repr=False)
class ModuleHttpComposition:
    request_source: _ApiRequestSource
    approved_host: str
    approved_origin: str
    limits: _CoreHttpLimits
    input_limits: _ApiInputLimits
    def __post_init__(self):
        if type(self.request_source) is not _ApiRequestSource:
            _fail_value('Source Auth explicite requise.')
        for value in (self.approved_host, self.approved_origin):
            if type(value) is not str or not value or chr(0) in value:
                _fail_value('Composition HTTP module invalide.')
        origin = _urlsplit(self.approved_origin)
        if origin.scheme != 'https' or origin.netloc != self.approved_host or origin.username is not None or origin.password is not None or origin.path or origin.query or origin.fragment:
            _fail_value('Origine HTTPS module invalide.')
        if type(self.limits) is not _CoreHttpLimits or type(self.input_limits) is not _ApiInputLimits:
            _fail_value('Limites HTTP module invalides.')
        self.limits.__post_init__()
        self.input_limits.__post_init__()

@_dataclass(frozen=True, slots=True, repr=False)
class ModuleHttpBinding:
    owner: str
    kind: str
    name: str
    contract_id: str
    contract_version: str
    scopes: tuple
    segments: tuple
    query_fields: tuple
    def __post_init__(self):
        _check_owner(self.owner)
        if self.kind not in ('QUERY', 'COMMAND'):
            _fail_value('Genre module invalide.')
        if type(self.name) is not str or not _re.fullmatch(_NAME_RE, self.name):
            _fail_value('Nom module invalide.')
        if self.name in _PROTECTED_SEGMENTS:
            _fail_value('Nom reserve.')
        try:
            from pixs.backend.api_core_catalog import COMMANDS as _COMMANDS
            from pixs.backend.api_core_catalog import QUERIES as _QUERIES
            if self.name in _COMMANDS or self.name in _QUERIES:
                _fail_value('Nom Core reserve.')
        except ImportError:
            _fail_value('Catalogue Core indisponible.')
        _check_contract_id(self.owner, self.contract_id)
        if type(self.contract_version) is not str or not _re.fullmatch(_SEMVER_RE, self.contract_version):
            _fail_value('Version SemVer complete requise.')
        if type(self.scopes) is not tuple or not self.scopes:
            _fail_value('Contextes declares requis.')
        seen_scopes = set()
        for scope in self.scopes:
            if type(scope) is not str or scope not in _SCOPES or scope in seen_scopes:
                _fail_value('Contexte P/T/S unique requis.')
            seen_scopes.add(scope)
        if type(self.segments) is not tuple or not self.segments:
            _fail_value('Suffixe litteral requis.')
        for segment in self.segments:
            if type(segment) is not str or not _re.fullmatch(_SEGMENT_RE, segment):
                _fail_value('Segment litteral invalide.')
        if self.segments[0] in _PROTECTED_SEGMENTS:
            _fail_value('Surface reservee.')
        if ((len(self.segments) == 1 and self.segments[0] in _QUERIES)
                or (len(self.segments) == 2 and self.segments[0] == 'commands' and self.segments[1] in _COMMANDS)):
            _fail_value('Route Core reservee.')
        if type(self.query_fields) is not tuple:
            _fail_value('Champs declares invalides.')
        seen_fields = set()
        for field in self.query_fields:
            if type(field) is not str or not _re.fullmatch(_FIELD_RE, field) or field in seen_fields:
                _fail_value('Champ declare unique requis.')
            seen_fields.add(field)
        if self.kind == 'COMMAND' and self.query_fields != ():
            _fail_value('COMMAND sans query_fields.')

@_dataclass(frozen=True, slots=True, repr=False)
class ModuleHttpRequest:
    facade: _Facade
    context: _ScopeContext
    actor: _ResolvedActor
    token: _OpaqueToken
    token_kind: _TokenKind
    correlation_id: str
    language: str
    body: dict[str, object] | None
    query_pairs: tuple
    idempotency_key: str | None
    raw_path: str
    def __post_init__(self):
        if type(self.facade) is not _Facade:
            _fail_value('Facade invalide.')
        if type(self.context) is not _ScopeContext:
            _fail_value('Contexte invalide.')
        try:
            _validate_structure(self.context)
        except (_ScopeStructureError, AttributeError):
            _fail_value('Contexte invalide.')
        if type(self.actor) is not _ResolvedActor:
            _fail_value('Acteur non resolu.')
        try:
            self.actor.__post_init__()
        except AttributeError:
            _fail_value('Acteur non resolu.')
        if type(self.token) is not _OpaqueToken or type(self.token_kind) is not _TokenKind:
            _fail_value('Justificatif invalide.')
        if self.token_kind not in (_TokenKind.ACCESS, _TokenKind.WEB_SESSION):
            _fail_value('Justificatif invalide.')
        if self.actor.context != self.context or self.actor.facade is not self.facade:
            _fail_value('Acteur ou contexte contradictoire.')
        expected_facade = _Facade.WEB if self.token_kind is _TokenKind.WEB_SESSION else _Facade.API
        if self.facade is not expected_facade:
            _fail_value('Facade et justificatif contradictoires.')
        _check_text(self.correlation_id, 128)
        if any(c in self.correlation_id for c in (chr(10), chr(13))):
            _fail_value('Correlation invalide.')
        if self.language not in ('fr', 'en'):
            _fail_value('Langue invalide.')
        if self.body is not None and type(self.body) is not dict:
            _fail_value('Body dict ou None.')
        if type(self.query_pairs) is not tuple:
            _fail_value('Paires ordonnees requises.')
        for pair in self.query_pairs:
            if type(pair) is not tuple or len(pair) != 2 or type(pair[0]) is not str or type(pair[1]) is not str:
                _fail_value('Paire query invalide.')
        if self.idempotency_key is not None and (type(self.idempotency_key) is not str or not self.idempotency_key or chr(0) in self.idempotency_key):
            _fail_value('Cle idempotence invalide.')
        if type(self.raw_path) is not str or not self.raw_path.startswith('/'):
            _fail_value('Chemin brut invalide.')

@_dataclass(frozen=True, slots=True, repr=False)
class ModuleHttpResult:
    status: int
    data: object
    links: object
    error: object
    activity: object = None
    def __post_init__(self):
        if type(self.status) is not int or not (self.status in (200, 202) or 400 <= self.status <= 599):
            _fail_value('Statut module invalide.')
        if self.status in (200, 202):
            if self.error is not None:
                _fail_value('Succes sans erreur.')
            if type(self.links) is not dict:
                _fail_value('Liens invalides.')
            _assert_json_finite(self.data)
            _assert_json_finite(self.links)
        else:
            if self.data is not None or type(self.links) is not dict or self.links != {}:
                _fail_value('Erreur sans data ni links.')
            if type(self.error) is not dict:
                _fail_value('Erreur proprietaire requise.')
            keys = set(self.error)
            if keys not in (set(['error_code', 'message', 'details']), set(['error_code', 'message', 'details', 'field_errors'])):
                _fail_value('Erreur exactement code/message/details/field_errors.')
            code = self.error['error_code']
            message = self.error['message']
            details = self.error['details']
            if type(code) is not str or not code or type(message) is not str or not message or type(details) is not dict:
                _fail_value('Erreur proprietaire invalide.')
            if not _re.fullmatch(r'^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+\.api\.v1\.[A-Z][A-Z0-9_]*$', code):
                _fail_value('Prefixe proprietaire invalide.')
            if 'field_errors' in self.error:
                fields = self.error['field_errors']
                if type(fields) is not list or any(type(field) is not dict for field in fields):
                    _fail_value('Erreurs de champ invalides.')
            _assert_json_finite(self.error)
        if self.activity is not None:
            if self.status not in (200, 202):
                _fail_value('Activité réservée au résultat métier confirmé ou provisoire.')
            if type(self.activity) is not dict:
                _fail_value('Activite fermee requise.')
            status = self.activity.get('status')
            if status in _ACTIVITY_OK:
                if set(self.activity) != set(['status']):
                    _fail_value('Activite fermee invalide.')
            elif status == 'NOT_RECORDED':
                if set(self.activity) != set(['status', 'error_code']):
                    _fail_value('Activite NOT_RECORDED invalide.')
                error_code = self.activity['error_code']
                if type(error_code) is not str or not error_code.startswith('pixs.core.api.v1.'):
                    _fail_value('Classification C06 requise.')
                if _CoreApiError(error_code.removeprefix('pixs.core.api.v1.')).code != error_code:
                    _fail_value('Classification C06 requise.')
            else:
                _fail_value('Statut activite invalide.')

def _context_mode(context):
    if context.scope_type is _ScopeType.PLATFORM:
        return 'P'
    if context.scope_id is None:
        return 'T'
    return 'S'

def _module_query_pairs(request, composition, binding):
    raw = request.META.get('QUERY_STRING', '')
    if type(raw) is not str or len(raw) > composition.limits.max_query_chars:
        raise _CoreApiError('PAYLOAD_TOO_LARGE')
    if raw and raw.count('&') + 1 > composition.input_limits.max_collection_items:
        raise _CoreApiError('PAYLOAD_TOO_LARGE')
    try:
        raw.encode('ascii')
        for match in _re.finditer('%', raw):
            if not _re.fullmatch('[0-9a-fA-F]{2}', raw[match.start() + 1:match.start() + 3]):
                raise _CoreApiError('INPUT_INVALID')
        pairs = _url.parse_qsl(raw, keep_blank_values=True, encoding='utf-8', errors='strict')
    except _CoreApiError:
        raise
    except (UnicodeError, ValueError):
        raise _CoreApiError('INPUT_INVALID')
    if len(pairs) > composition.input_limits.max_collection_items:
        raise _CoreApiError('PAYLOAD_TOO_LARGE')
    allowed = set(binding.query_fields)
    checked = []
    for key, value in pairs:
        if key not in allowed:
            raise _CoreApiError('INPUT_INVALID')
        if chr(0) in key or chr(0) in value:
            raise _CoreApiError('INPUT_INVALID')
        if len(value) > composition.input_limits.max_reference_chars:
            raise _CoreApiError('INPUT_INVALID')
        try:
            value.encode('utf-8')
        except UnicodeError:
            raise _CoreApiError('INPUT_INVALID')
        checked.append((key, value))
    return tuple(checked)

def build_module_api_view(composition, *, bindings, dispatch):
    if type(composition) is not ModuleHttpComposition:
        _fail_value('Composition module requise.')
    composition.__post_init__()
    if type(bindings) is not tuple or not bindings:
        _fail_value('Bindings exacts requis.')
    seen_names = set()
    seen_triples = set()
    for binding in bindings:
        if type(binding) is not ModuleHttpBinding:
            _fail_value('Binding module exact requis.')
        binding.__post_init__()
        triple = (binding.owner, binding.kind, binding.name)
        if triple in seen_triples:
            _fail_value('Collision proprietaire/genre/nom.')
        seen_triples.add(triple)
        pair = (binding.kind, binding.name)
        if pair in seen_names:
            _fail_value('Collision genre/nom.')
        seen_names.add(pair)
    for index in range(len(bindings)):
        for other in range(index + 1, len(bindings)):
            left = bindings[index]
            right = bindings[other]
            if tuple(left.segments) == tuple(right.segments) and set(left.scopes) & set(right.scopes):
                _fail_value('Route/contextes en collision.')
    if not callable(dispatch):
        _fail_value('Dispatch callable requis.')
    def view(request, **ignored):
        from pixs.backend.api_core_views import _actor as _core_actor
        from pixs.backend.api_core_views import _body as _core_body
        from pixs.backend.api_core_views import _context_json as _core_context_json
        from pixs.backend.api_core_views import _csrf as _core_csrf
        from pixs.backend.api_core_views import _error as _core_error
        from pixs.backend.api_core_views import _key as _core_key
        from pixs.backend.api_core_views import _language as _core_language
        from pixs.backend.api_core_views import _method as _core_method
        from pixs.backend.api_core_views import _path as _core_path
        from pixs.backend.api_core_views import _response as _core_response
        from pixs.backend.api_core_views import _route as _core_route
        from pixs.backend.api_core_views import _text as _core_text
        from pixs.backend.api_core_views import _transport as _core_transport
        correlation = str(_generate_uuid7())
        language = _core_language(request)
        try:
            supplied = request.headers.get('X-Correlation-ID')
            if supplied is not None:
                supplied = _core_text(supplied, 128)
                if any(c in supplied for c in (chr(10), chr(13))):
                    raise _CoreApiError('INPUT_INVALID')
                correlation = supplied
            parts, raw_path, available = _core_path(request)
            web, context, tail = _core_route(parts, available)
            for value in (context.tenant_id, context.scope_id):
                if value is not None:
                    _core_text(value, composition.input_limits.max_reference_chars)
            for header, expected in (('X-Tenant-ID', context.tenant_id), ('X-Scope-ID', context.scope_id)):
                if request.headers.get(header) is not None and request.headers[header] != expected:
                    raise _CoreApiError('CONTEXT_MISMATCH')
            _core_transport(request, composition, web, request.method not in ('GET', 'HEAD', 'OPTIONS'))
            mode = _context_mode(context)
            matched = None
            for binding in bindings:
                if list(binding.segments) == tail and mode in binding.scopes:
                    if matched is not None:
                        raise _CoreApiError('INTERNAL_ERROR')
                    matched = binding
            if matched is None:
                raise _CoreApiError('NOT_FOUND')
            _core_method(request, 'POST' if matched.kind == 'COMMAND' else 'GET')
            if web and matched.kind == 'COMMAND':
                _core_csrf(request)
            actor, token, kind = _core_actor(request, composition, context, web)
            if matched.kind == 'COMMAND':
                if request.META.get('QUERY_STRING', ''):
                    raise _CoreApiError('INPUT_INVALID')
                body = _core_body(request, composition)
                key = _core_key(request, composition.input_limits.max_reference_chars)
                query_pairs = ()
                idempotency_key = key
                raw_body = body
            else:
                if request.headers.get('Idempotency-Key') is not None:
                    raise _CoreApiError('INPUT_INVALID')
                raw_body = None
                query_pairs = _module_query_pairs(request, composition, matched)
                idempotency_key = None
            facade = _Facade.WEB if web else _Facade.API
            boundary = ModuleHttpRequest(facade, context, actor, token, kind, correlation, language, raw_body, query_pairs, idempotency_key, raw_path)
            result = dispatch(matched, boundary)
            if type(result) is not ModuleHttpResult:
                raise _CoreApiError('INTERNAL_ERROR')
            result.__post_init__()
            if result.error is not None and not result.error['error_code'].startswith(matched.owner + '.api.v1.'):
                raise _CoreApiError('INTERNAL_ERROR')
            if result.status in (200, 202):
                meta = {'correlation_id': correlation, 'context': _core_context_json(context)}
                if result.activity is not None:
                    meta['activity'] = dict(result.activity)
                return _core_response(result.data, meta=meta, links=dict(result.links), status=result.status)
            envelope = dict(result.error)
            envelope['correlation_id'] = correlation
            response = _JsonResponse(envelope, status=result.status)
            response['Cache-Control'] = 'no-store'
            response['Pragma'] = 'no-cache'
            response['X-Content-Type-Options'] = 'nosniff'
            return response
        except Exception as cause:
            return _core_error(_classify_error(cause), correlation, language)
    return view

def build_module_openapi_view(composition, *, plan, document):
    if type(composition) is not ModuleHttpComposition:
        _fail_value('Composition module requise.')
    composition.__post_init__()
    from pixs.backend.api_module_openapi import build_module_document_view as _build_doc
    document_view = _build_doc(plan, document)
    def view(request, **ignored):
        from pixs.backend.api_core_views import _error as _core_error
        from pixs.backend.api_core_views import _language as _core_language
        from pixs.backend.api_core_views import _transport as _core_transport
        try:
            if request.method not in ('GET', 'HEAD'):
                error = _CoreApiError('METHOD_NOT_ALLOWED')
                error.allowed_methods = 'GET'
                raise error
            _core_transport(request, composition, None, False)
            response = document_view(request)
            response['Cache-Control'] = 'no-store'
            response['Pragma'] = 'no-cache'
            response['X-Content-Type-Options'] = 'nosniff'
            return response
        except Exception as cause:
            response = _core_error(_classify_error(cause), str(_generate_uuid7()), _core_language(request))
            if request.method == 'HEAD':
                response['Content-Length'] = str(len(response.content))
                response.content = b''
            return response
    return view
