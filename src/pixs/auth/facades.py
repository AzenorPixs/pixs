"""Adaptateurs Auth déclarés : cookie web/CSRF, Bearer API/CLI, sans route ni écoute HTTP.

L'hôte C06 fournit le mandat serveur, l'origine approuvée et un objet HttpRequest
après sa frontière N04. Aucune identité, décision ou preuve n'est tirée d'un en-tête client.
"""
from __future__ import annotations
import datetime
from urllib.parse import urlsplit
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware, get_token, rotate_token
from pixs.auth.contracts import AuthResult, AuthOutcome, AuthServiceError, Facade, LoginInput
from pixs.auth.tokens import parse_token, AuthTokenError, TokenKind

WEB_COOKIE = "__Host-pixs-session"


def _response(body, status=200):
    response=JsonResponse(body,status=status)
    response["Cache-Control"]="no-store"
    response["Pragma"]="no-cache"
    response["X-Content-Type-Options"]="nosniff"
    return response


def _denied(code="AUTH_DENIED", status=403):
    return _response({"code":code},status)


class _CsrfGuard(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Le contrôle Django reste complet ; aucun diagnostic ne recopie la requête.
        return _denied("AUTH_CSRF_REQUIRED")


def _csrf_view(request):
    return None


def _body(result):
    if type(result) is not AuthResult:
        raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
    result.__post_init__()
    body={"outcome":result.outcome.value,"audit":result.audit.value,"operation_id":result.operation_id}
    if result.session is not None:
        body["session"]={"id":str(result.session.session_id),"authenticated_at":result.session.authenticated_at.isoformat(),"idle_expires_at":result.session.idle_expires_at.isoformat(),"absolute_expires_at":result.session.absolute_expires_at.isoformat()}
    if result.credential is not None:
        body["credential"]=result.credential.value
    if result.pending_audit_ref is not None:
        body["pending_audit_ref"]=result.pending_audit_ref
    return body


def _status(result):
    return 503 if result.outcome is AuthOutcome.UNKNOWN else 401 if result.outcome is AuthOutcome.REAUTH_REQUIRED else 200


class _Boundary:
    def __init__(self, *, service, approved_origin, approved_host):
        if type(approved_origin) is not str or type(approved_host) is not str:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        parsed=urlsplit(approved_origin)
        if (parsed.scheme!="https" or not parsed.netloc or parsed.netloc!=approved_host or parsed.username is not None or parsed.password is not None or parsed.path or parsed.query or parsed.fragment):
            raise AuthServiceError("AUTH_INPUT_INVALID")
        self._service,self._origin,self._host=service,approved_origin,approved_host
    def _guard(self, request):
        try:
            if not request.is_secure() or request.get_host()!=self._host:
                return _denied("AUTH_TRANSPORT_REQUIRED")
        except DisallowedHost:
            return _denied("AUTH_TRANSPORT_REQUIRED")
        if request.method!="POST":
            return _denied("AUTH_METHOD_INVALID",405)
        return None
    def _error(self, error):
        code=error.code if type(error) is AuthServiceError else "AUTH_DENIED"
        return _denied(code,409 if code=="AUTH_SESSION_LIMIT" else 503 if code in ("AUTH_STATE_UNAVAILABLE","AUTH_COMMIT_UNKNOWN","AUTH_AUDIT_UNAVAILABLE") else 401 if code=="AUTH_REAUTH_REQUIRED" else 403)


class WebAuthFacade(_Boundary):
    """Façade web explicitement montée par l'hôte, cookie seul et CSRF Django réel."""
    def __init__(self, *, service, approved_origin, approved_host, clock):
        super().__init__(service=service,approved_origin=approved_origin,approved_host=approved_host)
        if settings.CSRF_USE_SESSIONS or not callable(getattr(clock,"now",None)):
            raise AuthServiceError("AUTH_INPUT_INVALID")
        self._clock=clock
        self._csrf=_CsrfGuard(lambda request:_response({}))
    def _guard(self, request):
        denied=super()._guard(request)
        if denied is not None: return denied
        if request.headers.get("Origin")!=self._origin or request.headers.get("Authorization"):
            return _denied("AUTH_ORIGIN_INVALID")
        self._csrf.process_request(request)
        return self._csrf.process_view(request,_csrf_view,(),{})
    def csrf(self, request):
        # Seul bootstrap public : ce jeton CSRF n'est jamais un justificatif Auth.
        try:
            if request.method!="GET" or not request.is_secure() or request.get_host()!=self._host:
                return _denied("AUTH_TRANSPORT_REQUIRED")
        except DisallowedHost:
            return _denied("AUTH_TRANSPORT_REQUIRED")
        if request.headers.get("Origin") not in (None,self._origin):
            return _denied("AUTH_ORIGIN_INVALID")
        self._csrf.process_request(request)
        response=_response({"csrf_token":get_token(request)})
        response=self._csrf.process_response(request,response)
        cookie=response.cookies.get(settings.CSRF_COOKIE_NAME)
        if cookie is None: raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
        cookie["secure"],cookie["httponly"],cookie["samesite"],cookie["path"],cookie["domain"]=True,True,"Lax","/",""
        return response
    def login(self, request, command, supplied):
        denied=self._guard(request)
        if denied is not None: return denied
        try:
            if type(supplied) is not LoginInput or supplied.facade is not Facade.WEB:
                raise AuthServiceError("AUTH_INPUT_INVALID")
            result=self._service.login(command,supplied)
            response=_response(_body(result),_status(result))
            if result.emission is not None:
                now=self._clock.now()
                if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc or result.session.facade is not Facade.WEB or result.emission.cookie is None:
                    raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
                lifetime=int((result.session.absolute_expires_at-now).total_seconds())
                if lifetime<=0: raise AuthServiceError("AUTH_REAUTH_REQUIRED")
                response.set_cookie(WEB_COOKIE,result.emission.cookie.value,max_age=lifetime,secure=True,httponly=True,samesite="Lax",path="/")
                rotate_token(request)
                response=self._csrf.process_response(request,response)
                csrf_cookie=response.cookies.get(settings.CSRF_COOKIE_NAME)
                if csrf_cookie is not None:
                    csrf_cookie["secure"],csrf_cookie["httponly"],csrf_cookie["samesite"],csrf_cookie["path"],csrf_cookie["domain"]=True,True,"Lax","/",""
            return response
        except (AuthServiceError,AuthTokenError) as error: return self._error(error)
    def invoke(self, request, command, *, operation, **server_arguments):
        denied=self._guard(request)
        if denied is not None: return denied
        try:
            if operation not in ("logout","revoke_session","revoke_all","change_password","recover_password","reconcile_audit") or "kind" in server_arguments:
                raise AuthServiceError("AUTH_INPUT_INVALID")
            token=parse_token(request.COOKIES.get(WEB_COOKIE))
            result=getattr(self._service,operation)(command,token,kind=TokenKind.WEB_SESSION,**server_arguments)
            response=_response(_body(result),_status(result))
            if result.outcome in (AuthOutcome.WITHDRAWN,AuthOutcome.WITHDRAWN_AUDIT_PENDING) and operation in ("logout","revoke_all","change_password","recover_password"):
                response.delete_cookie(WEB_COOKIE,path="/",samesite="Lax")
                response.cookies[WEB_COOKIE]["secure"]=True
                response.cookies[WEB_COOKIE]["httponly"]=True
            return response
        except (AuthServiceError,AuthTokenError) as error: return self._error(error)


class ApiAuthFacade(_Boundary):
    """Transport Bearer explicite partagé par API et CLI, sans fallback cookie."""
    def _guard(self, request):
        denied=super()._guard(request)
        if denied is not None: return denied
        # Les navigateurs d'une autre origine ne peuvent réutiliser cette façade.
        if request.headers.get("Origin") not in (None,self._origin):
            return _denied("AUTH_ORIGIN_INVALID")
        return None
    def credential(self, request):
        header=request.headers.get("Authorization","")
        if type(header) is not str or not header.startswith("Bearer "):
            raise AuthServiceError("AUTH_DENIED")
        return parse_token(header[7:])
    def _result(self, result):
        body=_body(result)
        if result.emission is not None:
            if result.session.facade is not Facade.API or result.emission.access is None or result.emission.refresh is None:
                raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
            body["access_token"],body["refresh_token"]=result.emission.access.value,result.emission.refresh.value
            body["token_type"]="Bearer"
        return _response(body,_status(result))
    def login(self, request, command, supplied):
        denied=self._guard(request)
        if denied is not None: return denied
        try:
            if type(supplied) is not LoginInput or supplied.facade is not Facade.API:
                raise AuthServiceError("AUTH_INPUT_INVALID")
            return self._result(self._service.login(command,supplied))
        except (AuthServiceError,AuthTokenError) as error: return self._error(error)
    def invoke(self, request, command, *, operation, **server_arguments):
        denied=self._guard(request)
        if denied is not None: return denied
        try:
            if operation not in ("logout","revoke_session","revoke_all","change_password","recover_password","reconcile_audit","renew") or "kind" in server_arguments:
                raise AuthServiceError("AUTH_INPUT_INVALID")
            token=self.credential(request)
            kwargs={} if operation=="renew" else {"kind":TokenKind.ACCESS}
            return self._result(getattr(self._service,operation)(command,token,**kwargs,**server_arguments))
        except (AuthServiceError,AuthTokenError) as error: return self._error(error)


__all__=["WEB_COOKIE","WebAuthFacade","ApiAuthFacade"]
