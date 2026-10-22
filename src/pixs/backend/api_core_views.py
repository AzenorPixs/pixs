"""HTTP Core v1 : seules les routes déclarées appellent les propriétaires."""
from __future__ import annotations

import json
import re
import urllib.parse as url
import uuid

from django.core.exceptions import DisallowedHost, RequestDataTooBig
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.urls import re_path

from pixs.auth.contracts import AuthServiceError, Facade, LoginInput
from pixs.auth.facades import WEB_COOKIE
from pixs.auth.identifiers import parse_identity_reference, require_uuid7
from pixs.auth.policy import SessionCategory
from pixs.auth.tokens import TokenKind, parse_token
from pixs.backend.api_core_catalog import (
    COMMANDS, QUERIES, command_resource_ref, context_mode, dispatch_command,
    dispatch_query, parse_command_input,
)
from pixs.backend.api_core_composition import CoreApiComposition
from pixs.backend.api_core_errors_catalog import CoreApiError, classify_error
from pixs.backend.api_core_pagination import CoreCursorBinding
from pixs.core.api_core_serializer_v1 import API_CORE_SERIALIZER_VERSION, command_content_sha256
from pixs.core.dto import CommandEnvelope, CoreMutationResult, CorePage, CoreQueryInput
from pixs.core.persistence.uuid7 import generate_uuid7
from pixs.core.scope.context import ScopeContext, ScopeType

__all__ = ["build_core_api_view", "build_core_api_urls"]


def _fail(code="INPUT_INVALID"):
    raise CoreApiError(code)


def _text(value, maximum):
    if type(value) is not str or not value or len(value) > maximum or chr(0) in value:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeError:
        _fail()
    return value


def _context_json(context):
    return {"scope_type": context.scope_type.value, "tenant_id": context.tenant_id,
            "scope_id": context.scope_id}


def _response(data, *, meta, links, status=200):
    response = JsonResponse({"data": data, "meta": meta, "links": links}, status=status)
    response["Cache-Control"] = "no-store"
    response["Pragma"] = "no-cache"
    response["X-Content-Type-Options"] = "nosniff"
    return response


def _error(error, correlation, language):
    response = JsonResponse(error.envelope(correlation_id=correlation, language=language), status=error.status)
    response["Cache-Control"] = "no-store"
    response["Pragma"] = "no-cache"
    response["X-Content-Type-Options"] = "nosniff"
    allowed = getattr(error, "allowed_methods", None)
    if allowed in ("GET", "POST"):
        response["Allow"] = allowed
    return response


def _language(request):
    value = request.headers.get("Accept-Language", "")
    if type(value) is not str or len(value) > 512:
        return "en"
    best, quality = "en", -1
    for item in value.split(","):
        parts = item.strip().split(";")
        code = parts[0].strip().lower().split("-")[0]
        q = 1000
        if len(parts) > 2:
            continue
        if len(parts) == 2:
            parameter = parts[1].strip()
            if not parameter.startswith("q=") or not re.fullmatch(r"0(?:[.][0-9]{1,3})?|1(?:[.]0{1,3})?", parameter[2:]):
                continue
            number = parameter[2:]
            whole, _, fraction = number.partition(".")
            q = int(whole) * 1000 + int((fraction + "000")[:3])
        if code in ("fr", "en") and q > 0 and q > quality:
            best, quality = code, q
    return best


def _transport(request, composition, web, mutation):
    try:
        if not request.is_secure() or request.get_host() != composition.approved_host:
            _fail("TRANSPORT_REQUIRED")
    except DisallowedHost:
        _fail("TRANSPORT_REQUIRED")
    origin = request.headers.get("Origin")
    if origin not in (None, composition.approved_origin):
        _fail("ACCESS_DENIED")
    if web and mutation and origin != composition.approved_origin:
        _fail("ACCESS_DENIED")
    if web and request.headers.get("Authorization"):
        _fail("ACCESS_DENIED")
    if web is False and request.COOKIES.get(WEB_COOKIE):
        _fail("ACCESS_DENIED")


class _Csrf(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return _error(CoreApiError("CSRF_REQUIRED"), "csrf-boundary", "en")


def _csrf(request):
    guard = _Csrf(lambda request: None)
    guard.process_request(request)
    if guard.process_view(request, _csrf, (), {}) is not None:
        _fail("CSRF_REQUIRED")


def _unquote(segment):
    for match in re.finditer("%", segment):
        if len(segment) < match.start() + 3 or not re.fullmatch("[0-9a-fA-F]{2}", segment[match.start()+1:match.start()+3]):
            _fail()
    try:
        value = url.unquote_to_bytes(segment).decode("utf-8", "strict")
    except UnicodeError:
        _fail()
    if chr(0) in value:
        _fail()
    return value


def _path(request):
    scope = getattr(request, "scope", None)
    raw = scope.get("raw_path") if type(scope) is dict else None
    if raw is None:
        raw = request.META.get("RAW_URI")
    available = raw is not None
    if type(raw) is bytes:
        try:
            raw = raw.decode("ascii")
        except UnicodeError:
            _fail()
    if raw is None:
        raw = url.quote(request.path, safe="/")
    if type(raw) is not str or not raw.startswith("/") or raw.startswith("//"):
        _fail("NOT_FOUND")
    raw = raw.split("?", 1)[0]
    if len(raw) > 65536:
        _fail("PAYLOAD_TOO_LARGE")
    components = raw[1:].split("/")
    if any(not component for component in components):
        _fail("NOT_FOUND")
    decoded = [_unquote(component) for component in components]
    full = "/" + "/".join(decoded)
    if full not in (request.path, request.path_info):
        _fail("CONTEXT_MISMATCH")
    script = request.META.get("SCRIPT_NAME", "")
    if script and full == request.path:
        prefix = script.strip("/").split("/")
        if decoded[:len(prefix)] != prefix:
            _fail("CONTEXT_MISMATCH")
        decoded = decoded[len(prefix):]
    return decoded, raw, available


def _route(parts, raw_available):
    if len(parts) < 3 or parts[:2] != ["api", "v1"]:
        _fail("NOT_FOUND")
    web = parts[2] == "web"
    tail = parts[3:] if web else parts[2:]
    if web and tail == ["auth", "csrf"]:
        return web, ScopeContext(ScopeType.PLATFORM), ["csrf"]
    if tail and tail[0] == "platform":
        return web, ScopeContext(ScopeType.PLATFORM), tail[1:]
    if len(tail) >= 3 and tail[0] == "tenants":
        if not raw_available:
            _fail("SERVICE_UNAVAILABLE")
        if len(tail) >= 5 and tail[2] == "scopes":
            return web, ScopeContext(ScopeType.TENANT, tail[1], tail[3]), tail[4:]
        return web, ScopeContext(ScopeType.TENANT, tail[1]), tail[2:]
    _fail("NOT_FOUND")


def _no_duplicate(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail()
        result[key] = value
    return result


def _reject_number(value):
    _fail()


def _body(request, composition):
    content_length = request.META.get("CONTENT_LENGTH", "")
    if content_length:
        if type(content_length) is not str or not re.fullmatch(r"[0-9]{1,20}", content_length):
            _fail()
        if int(content_length) > composition.limits.max_payload_bytes:
            _fail("PAYLOAD_TOO_LARGE")
    if request.content_type != "application/json":
        _fail()
    try:
        body = request.body
        if len(body) > composition.limits.max_payload_bytes:
            _fail("PAYLOAD_TOO_LARGE")
        value = json.loads(body.decode("utf-8", "strict"), object_pairs_hook=_no_duplicate,
                           parse_float=_reject_number, parse_constant=_reject_number)
    except CoreApiError:
        raise
    except RequestDataTooBig:
        _fail("PAYLOAD_TOO_LARGE")
    except (UnicodeError, ValueError, RecursionError):
        _fail()
    if type(value) is not dict:
        _fail()
    return value


def _key(request, maximum):
    return _text(request.headers.get("Idempotency-Key"), maximum)


def _credential(request, web, kind=None):
    if web:
        return parse_token(request.COOKIES.get(WEB_COOKIE)), TokenKind.WEB_SESSION
    header = request.headers.get("Authorization", "")
    if type(header) is not str or not header.startswith("Bearer "):
        _fail("AUTH_REQUIRED")
    return parse_token(header[7:]), TokenKind.ACCESS if kind is None else kind


def _query(request, composition):
    raw = request.META.get("QUERY_STRING", "")
    if type(raw) is not str or len(raw) > composition.limits.max_query_chars:
        _fail("PAYLOAD_TOO_LARGE")
    try:
        raw.encode("ascii")
        for match in re.finditer("%", raw):
            if not re.fullmatch("[0-9a-fA-F]{2}", raw[match.start()+1:match.start()+3]):
                _fail()
        pairs = url.parse_qsl(raw, keep_blank_values=True, encoding="utf-8", errors="strict")
    except (UnicodeError, ValueError):
        _fail()
    values = {}
    for name, value in pairs:
        if name not in ("limit", "cursor", "ref"):
            _fail()
        values.setdefault(name, []).append(value)
    for name in ("limit", "cursor"):
        if len(values.get(name, ())) > 1:
            _fail()
    limit = values.get("limit", [str(composition.limits.default_page_size)])[0]
    if not re.fullmatch(r"[0-9]{1,6}", limit):
        _fail()
    limit = int(limit)
    if not 1 <= limit <= composition.limits.max_page_size:
        _fail()
    references = tuple(values.get("ref", ()))
    if len(references) > composition.input_limits.max_collection_items:
        _fail()
    for ref in references:
        _text(ref, composition.input_limits.max_reference_chars)
    if len(set(references)) != len(references):
        _fail()
    return limit, tuple(sorted(references)), values.get("cursor", [None])[0]


def _actor(request, composition, context, web, kind=None):
    token, kind = _credential(request, web, kind)
    actor = composition.request_source.resolve_token(context=context, token=token, kind=kind)
    if actor.facade is not (Facade.WEB if web else Facade.API):
        _fail("AUTH_REQUIRED")
    return actor, token, kind


def _core(request, composition, context, tail, web, correlation, raw_path):
    command = len(tail) == 2 and tail[0] == "commands"
    name = tail[1] if command else tail[0] if len(tail) == 1 else None
    registry = COMMANDS if command else QUERIES
    if name not in registry or context_mode(context) not in registry[name]["roots"]:
        _fail("NOT_FOUND")
    _method(request, "POST" if command else "GET")
    if web and command:
        _csrf(request)
    actor, token, kind = _actor(request, composition, context, web)
    operation = str(generate_uuid7())
    decision = str(generate_uuid7())
    if command:
        if request.META.get("QUERY_STRING", ""):
            _fail()
        dto = parse_command_input(name, _body(request, composition), context=context,
                                  correlation_id=correlation, limits=composition.input_limits)
        resource, action = command_resource_ref(name, dto), COMMANDS[name]["action"]
        key = _key(request, composition.input_limits.max_reference_chars)
    else:
        from pixs.core.query_source import collection_ref
        size, filters, cursor = _query(request, composition)
        spec = QUERIES[name]
        resource, action = collection_ref(spec["kind"], context), spec["action"]
        key = "query:" + operation
    req = composition.request_source.request(actor=actor, resource_id=resource, action_id=action,
                                             correlation_id=correlation, decision_id=decision)
    source = composition.request_source.open_core_source(request=req, operation_id=operation,
                                                         token=token, kind=kind)
    try:
        ports = composition.core_ports(request=req, operation_id=operation, authentication_source=source)
        meta = {"correlation_id": correlation, "context": _context_json(context)}
        if command:
            envelope = CommandEnvelope(req, operation, key,
                command_content_sha256(command_type=action + ":v1", dto=dto, context=context),
                API_CORE_SERIALIZER_VERSION, correlation, None)
            result = dispatch_command(name, dto=dto, envelope=envelope, ports=ports, alias=composition.alias)
            if type(result) is not CoreMutationResult:
                _fail("INTERNAL_ERROR")
            if web and name in composition.interactive_commands:
                if result.operation_id != operation:
                    meta["activity"] = {"status":"REPLAY_IGNORED"}
                else:
                    from pixs.backend.api_core_activity import record_completed_core_activity
                    try:
                        record_completed_core_activity(composition=composition, actor=actor,
                            core_operation_id=operation, correlation_id=correlation, token=token, kind=kind)
                    except Exception as activity_error:
                        # Core est déjà confirmé : l'échec distinct de suivi Auth reste explicite.
                        meta["activity"] = {"status":"NOT_RECORDED","error_code":classify_error(activity_error).code}
                    else:
                        meta["activity"] = {"status":"RECORDED"}
            data = {"operation_id": result.operation_id, "result_ref": result.result_ref,
                    "version": result.version, "persistence_state": result.persistence_state.value,
                    "correlation_id": result.correlation_id}
            return _response(data, meta=meta, links={})
        binding = CoreCursorBinding(actor.identity_ref, context, spec["kind"], filters, size)
        state = composition.cursor_codec.decode(cursor, binding=binding) if cursor is not None else None
        query = CoreQueryInput(context, correlation, filters, None,
                              after=None if state is None else state.after, page_limit=size)
        envelope = CommandEnvelope(req, operation, key, "0" * 64, API_CORE_SERIALIZER_VERSION, correlation, None)
        page = dispatch_query(name, query=query, envelope=envelope, ports=ports, alias=composition.alias)
        if type(page) is not CorePage:
            _fail("INTERNAL_ERROR")
        if state is not None:
            composition.cursor_codec.verify_snapshot(state, snapshot_version=page.snapshot_version)
        data = []
        for item in page.items:
            attributes = dict(item.data)
            if item.kind == "POLICY":
                attributes["definition"] = json.loads(attributes["definition"])
            data.append({"kind": item.kind, "ref": item.ref, "context": _context_json(item.context),
                         "version": item.version, "persistence_state": item.persistence_state,
                         "retention_state": item.retention_state, "governance_ref": item.governance_ref,
                         "confidentiality": item.confidentiality, "personal": item.personal,
                         "attributes": attributes})
        links = {}
        if page.next_after is not None:
            next_cursor = composition.cursor_codec.encode(binding=binding, after=page.next_after,
                snapshot_version=page.snapshot_version, decision_expires_at=page.expires_at)
            pairs = [("limit", str(size)), ("cursor", next_cursor)] + [("ref", ref) for ref in filters]
            query_string = url.urlencode(pairs)
            if len(query_string) > composition.limits.max_query_chars:
                _fail("PAYLOAD_TOO_LARGE")
            links["next"] = raw_path + "?" + query_string
        meta["page_size"] = size
        return _response(data, meta=meta, links=links)
    finally:
        source.close()


def _method(request, expected):
    if request.method != expected:
        error = CoreApiError("METHOD_NOT_ALLOWED")
        error.allowed_methods = expected
        raise error


def _uuid(value):
    if type(value) is not str:
        _fail()
    try:
        identifier = uuid.UUID(value)
        require_uuid7(identifier)
    except (ValueError, TypeError):
        _fail()
    if str(identifier) != value:
        _fail()
    return identifier


def _adapt_auth(response, *, correlation, context, language):
    body = json.loads(response.content.decode("utf-8"))
    if response.status_code >= 400:
        codes = {"AUTH_CSRF_REQUIRED": "CSRF_REQUIRED", "AUTH_ORIGIN_INVALID": "ACCESS_DENIED",
                 "AUTH_TRANSPORT_REQUIRED": "TRANSPORT_REQUIRED", "AUTH_METHOD_INVALID": "METHOD_NOT_ALLOWED"}
        if body.get("outcome") == "UNKNOWN":
            public = CoreApiError("UNKNOWN_OUTCOME")
        elif body.get("outcome") == "REAUTH_REQUIRED":
            public = CoreApiError("AUTH_REQUIRED")
        else:
            public = CoreApiError(codes[body["code"]]) if body.get("code") in codes else classify_error(
                AuthServiceError(body.get("code", "AUTH_STATE_UNAVAILABLE")))
        result = _error(public, correlation, language)
    else:
        result = _response(body, meta={"correlation_id": correlation, "context": _context_json(context)}, links={})
    for key, value in response.items():
        if key.lower() not in ("content-type", "content-length", "cache-control", "pragma"):
            result[key] = value
    result.cookies.update(response.cookies)
    return result


def _auth(request, composition, context, tail, web, correlation, language):
    if request.META.get("QUERY_STRING", ""):
        _fail()
    api, browser = composition.facades()
    facade = browser if web else api
    if tail == ["csrf"]:
        _method(request, "GET")
        return _adapt_auth(browser.csrf(request), correlation=correlation, context=context, language=language)
    if len(tail) != 2 or tail[0] != "auth":
        _fail("NOT_FOUND")
    name = tail[1]
    if name not in ("login", "logout", "revoke-session", "revoke-all", "change-password", "renew") or (web and name == "renew"):
        _fail("NOT_FOUND")
    if context.scope_type is ScopeType.TENANT and name in ("revoke-all", "change-password"):
        _fail("NOT_FOUND")
    _method(request, "POST")
    if web:
        _csrf(request)
    body = _body(request, composition)
    maximum = composition.input_limits.max_reference_chars
    key, decision = _key(request, maximum), str(generate_uuid7())
    if name == "login":
        if set(body) - {"external_subject", "password", "replace_session_id"} or not {"external_subject", "password"} <= set(body):
            _fail()
        external = _text(body["external_subject"], maximum)
        password = _text(body["password"], composition.limits.max_payload_bytes)
        actor = composition.request_source.resolve_login(context=context, external_subject=external,
                                                         facade=Facade.WEB if web else Facade.API)
        command = composition.request_source.auth_command(actor=actor, resource_id=composition.request_source.login_resource(actor),
            action_id="pixs.auth.session.create", correlation_id=correlation, decision_id=decision, idempotency_key=key)
        replace_session = _uuid(body["replace_session_id"]) if body.get("replace_session_id") is not None else None
        supplied = LoginInput(external, password, SessionCategory.ADMIN, Facade.WEB if web else Facade.API, replace_session)
        response = facade.login(request, command, supplied)
        return _adapt_auth(response, correlation=correlation, context=context, language=language)
    actor, _, _ = _actor(request, composition, context, web, TokenKind.REFRESH if name == "renew" else None)
    arguments = {}
    if name == "revoke-session":
        if set(body) != {"session_id"}:
            _fail()
        resource, action, operation = "pixs.auth.session:" + str(_uuid(body["session_id"])), "pixs.auth.session.revoke", "revoke_session"
    elif name == "change-password":
        if set(body) != {"new_password"} or actor.credential_id is None:
            _fail()
        arguments["new_password"] = _text(body["new_password"], composition.limits.max_payload_bytes)
        resource, action, operation = "pixs.auth.credential:" + str(actor.credential_id), "pixs.auth.credential.change", "change_password"
    else:
        if body:
            _fail()
        operation = {"logout": "logout", "revoke-all": "revoke_all", "renew": "renew"}[name]
        action = {"logout": "pixs.auth.session.logout", "revoke-all": "pixs.auth.session.revoke_all", "renew": "pixs.auth.session.renew"}[name]
        resource = ("pixs.auth.account:" + str(parse_identity_reference(actor.identity_ref))) if name == "revoke-all" else "pixs.auth.session:" + str(actor.session_id)
    command = composition.request_source.auth_command(actor=actor, resource_id=resource, action_id=action,
        correlation_id=correlation, decision_id=decision, idempotency_key=key)
    return _adapt_auth(facade.invoke(request, command, operation=operation, **arguments),
                       correlation=correlation, context=context, language=language)


def _build_core_api_view(composition):
    if type(composition) is not CoreApiComposition:
        raise ValueError("Composition HTTP Core requise.")
    composition.__post_init__()
    def view(request, **ignored):
        correlation, language = str(generate_uuid7()), _language(request)
        try:
            supplied = request.headers.get("X-Correlation-ID")
            if supplied is not None:
                supplied = _text(supplied, 128)
                if any(c in supplied for c in (chr(10), chr(13))):
                    _fail()
                correlation = supplied
            parts, raw_path, available = _path(request)
            web, context, tail = _route(parts, available)
            for value in (context.tenant_id, context.scope_id):
                if value is not None:
                    _text(value, composition.input_limits.max_reference_chars)
            for header, expected in (("X-Tenant-ID", context.tenant_id), ("X-Scope-ID", context.scope_id)):
                if request.headers.get(header) is not None and request.headers[header] != expected:
                    _fail("CONTEXT_MISMATCH")
            _transport(request, composition, web, request.method not in ("GET", "HEAD", "OPTIONS"))
            if tail == ["csrf"] or (tail and tail[0] == "auth"):
                return _auth(request, composition, context, tail, web, correlation, language)
            return _core(request, composition, context, tail, web, correlation, raw_path)
        except Exception as cause:
            # Frontière HTTP : aucune exception/entrée brute n'est projetée ou journalisée.
            return _error(classify_error(cause), correlation, language)
    return view


def build_core_api_view(composition, *, previous_plan, previous_documents, coexistence_doc=None):
    """Construction atomique du contrat et de la façade, référence approuvée injectée."""
    from pixs.backend.api_core_openapi import (
        build_core_openapi_documents, core_api_contract_plan, build_core_openapi_view,
    )
    from pixs.backend.api_core_openapi_compare import check_core_openapi_evolution
    plan = core_api_contract_plan()
    documents = build_core_openapi_documents(composition)
    check_core_openapi_evolution(previous_plan, plan, previous_documents,
        tuple(document for _,document in documents), coexistence_doc=coexistence_doc)
    documentation = {path:build_core_openapi_view(plan,document) for path,document in documents}
    core_view = _build_core_api_view(composition)
    def view(request, **kwargs):
        document_view = documentation.get(request.path_info)
        if document_view is None:
            return core_view(request, **kwargs)
        try:
            _transport(request, composition, None, False)
            return document_view(request)
        except Exception as cause:
            response = _error(classify_error(cause),str(generate_uuid7()),_language(request))
            if request.method == "HEAD":
                response["Content-Length"] = str(len(response.content))
                response.content = b""
            return response
    return view


def build_core_api_urls(composition, *, previous_plan, previous_documents, coexistence_doc=None):
    view = build_core_api_view(composition, previous_plan=previous_plan,
        previous_documents=previous_documents, coexistence_doc=coexistence_doc)
    return [re_path(r"(?s)^api/v1(?:/.*)?$", view, name="pixs-core-api-v1")]
