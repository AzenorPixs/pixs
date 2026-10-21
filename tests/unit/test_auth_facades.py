"""Recette de frontière HTTP avec CSRF Django réel ; service métier doublé explicitement."""
import datetime
import json
import unittest
from dataclasses import replace
from django.conf import settings
if not settings.configured:
    settings.configure(SECRET_KEY="vecteur-public-de-recette-sans-secret",DEFAULT_CHARSET="utf-8",ALLOWED_HOSTS=["auth.example.test","evil.example.test"],CSRF_USE_SESSIONS=False)
from django.test import RequestFactory, override_settings
from pixs.auth.contracts import AuthResult,AuthEmission,AuthOutcome,AuditDisposition,Facade,SessionInfo,LoginInput,AuthServiceError
from pixs.auth.facades import WebAuthFacade,ApiAuthFacade,WEB_COOKIE
from pixs.auth.tokens import new_token,TokenKind
from pixs.auth.policy import SessionCategory
from pixs.auth.identifiers import new_uuid7
from pixs.core.scope.context import ScopeContext,ScopeType

class FacadeTests(unittest.TestCase):
    def setUp(self):
        self.options=override_settings(ALLOWED_HOSTS=["auth.example.test","evil.example.test"],CSRF_USE_SESSIONS=False,CSRF_COOKIE_NAME="csrftoken",CSRF_COOKIE_DOMAIN=None,CSRF_COOKIE_PATH="/",CSRF_TRUSTED_ORIGINS=[])
        self.options.enable()
        self.addCleanup(self.options.disable)
        self.factory=RequestFactory()
        self.now=datetime.datetime.now(datetime.timezone.utc)
        now=self.now
        class Clock:
            def now(self):return now
        self.clock=Clock()
        class ServiceFixture:
            calls=0
            last_kind=None
            last_token=None
            def login(inner,command,supplied):
                inner.calls+=1
                info=SessionInfo(new_uuid7(),new_uuid7(),supplied.category,supplied.facade,ScopeContext(ScopeType.PLATFORM),now,now+datetime.timedelta(seconds=3600),now+datetime.timedelta(seconds=43200))
                emission=AuthEmission(None,None,new_token()) if supplied.facade is Facade.WEB else AuthEmission(new_token(),new_token(),None)
                inner.last_emission=emission
                return AuthResult(AuthOutcome.ISSUED,"fixture-http-operation",AuditDisposition.CONFIRMED,info,emission,None)
            def logout(inner,command,token,kind):
                inner.calls+=1
                inner.last_kind,inner.last_token=kind,token
                return AuthResult(AuthOutcome.WITHDRAWN,"fixture-http-withdrawal",AuditDisposition.CONFIRMED,None,None,None)
            def renew(inner,command,token):
                return inner.login(command,LoginInput("fixture","vecteur-public",SessionCategory.ORDINARY,Facade.API,None))
        self.service=ServiceFixture()
        args=dict(service=self.service,approved_origin="https://auth.example.test",approved_host="auth.example.test")
        self.web=WebAuthFacade(**args,clock=self.clock)
        self.api=ApiAuthFacade(**args)
        self.supplied=LoginInput("fixture","vecteur-public",SessionCategory.ORDINARY,Facade.WEB,None)
    def request(self,**kwargs):
        defaults=dict(secure=True,HTTP_HOST="auth.example.test",HTTP_ORIGIN="https://auth.example.test")
        defaults.update(kwargs)
        return self.factory.post("/auth/fixture",**defaults)
    def csrf_request(self,**kwargs):
        bootstrap=self.web.csrf(self.factory.get("/auth/csrf",secure=True,HTTP_HOST="auth.example.test"))
        request=self.request(**kwargs)
        request.COOKIES["csrftoken"]=bootstrap.cookies["csrftoken"].value
        request.META["HTTP_X_CSRFTOKEN"]=json.loads(bootstrap.content)["csrf_token"]
        return request
    def test_csrf_bootstrap_is_host_only_and_protected(self):
        result=self.web.csrf(self.factory.get("/auth/csrf",secure=True,HTTP_HOST="auth.example.test"))
        cookie=result.cookies["csrftoken"]
        self.assertEqual(result.status_code,200)
        self.assertTrue(cookie["secure"] and cookie["httponly"])
        self.assertEqual((cookie["domain"],cookie["path"],cookie["samesite"]),("","/","Lax"))
        self.assertNotIn(WEB_COOKIE,result.cookies)
    def test_cookie_is_inaccessible_to_javascript(self):
        result=self.web.login(self.csrf_request(),object(),self.supplied)
        self.assertEqual(result.status_code,200)
        cookie=result.cookies[WEB_COOKIE]
        self.assertTrue(cookie["secure"] and cookie["httponly"])
        self.assertEqual((cookie["path"],cookie["domain"],cookie["samesite"]),("/","","Lax"))
        self.assertEqual(int(cookie["max-age"]),43200)
        self.assertNotIn(self.service.last_emission.cookie.value,result.content.decode())
        self.assertEqual(result["Cache-Control"],"no-store")
    def test_missing_csrf_refused_before_service(self):
        self.assertEqual(self.web.login(self.request(),object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_wrong_csrf_refused_before_service(self):
        request=self.csrf_request();request.META["HTTP_X_CSRFTOKEN"]="A"*64
        self.assertEqual(self.web.login(request,object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_http_refused(self):
        self.assertEqual(self.web.login(self.csrf_request(secure=False),object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_other_host_refused(self):
        self.assertEqual(self.web.login(self.csrf_request(HTTP_HOST="evil.example.test"),object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_cross_origin_refused(self):
        self.assertEqual(self.web.login(self.csrf_request(HTTP_ORIGIN="https://evil.example.test"),object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_absent_origin_refused(self):
        request=self.csrf_request();request.META.pop("HTTP_ORIGIN")
        self.assertEqual(self.web.login(request,object(),self.supplied).status_code,403)
    def test_web_rejects_bearer(self):
        self.assertEqual(self.web.login(self.csrf_request(HTTP_AUTHORIZATION="Bearer "+new_token().value),object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_web_rejects_api_input(self):
        result=self.web.login(self.csrf_request(),object(),replace(self.supplied,facade=Facade.API))
        self.assertEqual(result.status_code,403);self.assertEqual(self.service.calls,0)
    def test_get_cannot_login(self):
        request=self.csrf_request();request.method="GET"
        self.assertEqual(self.web.login(request,object(),self.supplied).status_code,405)
        self.assertEqual(self.service.calls,0)
    def test_web_logout_uses_cookie_kind_and_clears_cookie(self):
        request=self.csrf_request();token=new_token();request.COOKIES[WEB_COOKIE]=token.value
        result=self.web.invoke(request,object(),operation="logout")
        self.assertEqual(result.status_code,200);self.assertIs(self.service.last_kind,TokenKind.WEB_SESSION)
        self.assertEqual(self.service.last_token.value,token.value)
        cookie=result.cookies[WEB_COOKIE]
        self.assertEqual(int(cookie["max-age"]),0);self.assertTrue(cookie["secure"] and cookie["httponly"])
    def test_web_does_not_read_bearer_as_cookie(self):
        result=self.web.invoke(self.csrf_request(),object(),operation="logout")
        self.assertEqual(result.status_code,403);self.assertEqual(self.service.calls,0)
    def test_api_login_emits_only_api_pair(self):
        result=self.api.login(self.request(),object(),replace(self.supplied,facade=Facade.API))
        body=json.loads(result.content)
        self.assertEqual(body["token_type"],"Bearer");self.assertEqual(len(body["access_token"]),43)
        self.assertEqual(len(body["refresh_token"]),43);self.assertFalse(result.cookies)
        self.assertEqual(result["Cache-Control"],"no-store")
    def test_api_rejects_web_input(self):
        self.assertEqual(self.api.login(self.request(),object(),self.supplied).status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_api_cookie_only_cannot_authenticate(self):
        request=self.request();request.COOKIES[WEB_COOKIE]=new_token().value
        self.assertEqual(self.api.invoke(request,object(),operation="logout").status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_api_bearer_uses_access_kind(self):
        token=new_token();request=self.request(HTTP_AUTHORIZATION="Bearer "+token.value)
        self.assertEqual(self.api.invoke(request,object(),operation="logout").status_code,200)
        self.assertIs(self.service.last_kind,TokenKind.ACCESS);self.assertEqual(self.service.last_token.value,token.value)
    def test_api_malformed_bearers_refused(self):
        for value in ("bearer "+new_token().value,"Bearer ","Bearer "+new_token().value+" ","Basic "+new_token().value):
            with self.subTest(kind=value[:7]):
                self.assertEqual(self.api.invoke(self.request(HTTP_AUTHORIZATION=value),object(),operation="logout").status_code,403)
        self.assertEqual(self.service.calls,0)
    def test_api_cross_origin_refused(self):
        result=self.api.login(self.request(HTTP_ORIGIN="https://evil.example.test"),object(),replace(self.supplied,facade=Facade.API))
        self.assertEqual(result.status_code,403);self.assertEqual(self.service.calls,0)
    def test_cli_can_use_api_without_origin(self):
        request=self.request();request.META.pop("HTTP_ORIGIN")
        self.assertEqual(self.api.login(request,object(),replace(self.supplied,facade=Facade.API)).status_code,200)
    def test_missing_https_configuration_refused(self):
        with self.assertRaises(AuthServiceError):
            ApiAuthFacade(service=self.service,approved_origin="http://auth.example.test",approved_host="auth.example.test")
    def test_unknown_operation_never_reaches_service(self):
        result=self.api.invoke(self.request(HTTP_AUTHORIZATION="Bearer "+new_token().value),object(),operation="__dict__")
        self.assertEqual(result.status_code,403);self.assertEqual(self.service.calls,0)

if __name__=="__main__":unittest.main()
