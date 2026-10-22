"""Façades C03 avec vrais services PostgreSQL/C04/C05 ; aucun hôte HTTP activé."""
from __future__ import annotations
EXPECTED_CASES=("csrf_missing_no_session","web_login_committed","cookie_hash_only","web_no_js_token","csrf_rotated","api_pair_committed","api_cookie_only_denied","web_token_not_api_bearer","cli_login_committed","cli_status_no_token","cli_refresh_rotated","cli_other_revoke_preserves_access","cli_pending_withdraw_clears_local","web_logout_committed","api_unknown_no_tokens","api_unknown_actual_commit","https_boundary_no_mutation","public_contracts_implemented")

def scenarios():
    import json
    from dataclasses import replace,asdict
    from unittest.mock import patch
    from django.test import RequestFactory,override_settings
    from django.db import connections,OperationalError
    from pixs.auth import models as m
    from pixs.auth.contracts import Facade,AuthOutcome,AuthenticationService,SessionService,CredentialService
    from pixs.auth.facades import WebAuthFacade,ApiAuthFacade,WEB_COOKIE
    from pixs.auth.cli import CliAuthFacade
    from pixs.auth.cli_vault import MemoryRefreshVault
    from pixs.auth.tokens import parse_token,token_fingerprint,TokenKind
    from pixs.auth.services import PostgresLocalAuthService
    from auth_service_fixture import make_auth_service_fixture
    f=make_auth_service_fixture();out={};rf=RequestFactory()
    with override_settings(ALLOWED_HOSTS=["auth.example.test"],CSRF_USE_SESSIONS=False,CSRF_COOKIE_NAME="csrftoken",CSRF_COOKIE_DOMAIN=None,CSRF_COOKIE_PATH="/",CSRF_TRUSTED_ORIGINS=[]):
        web=WebAuthFacade(service=f["service"](),approved_origin="https://auth.example.test",approved_host="auth.example.test",clock=f["clock"])
        api=ApiAuthFacade(service=f["service"](),approved_origin="https://auth.example.test",approved_host="auth.example.test")
        def request(**headers):
            return rf.post("/auth/fixture",secure=True,HTTP_HOST="auth.example.test",HTTP_ORIGIN="https://auth.example.test",**headers)
        def csrf_request():
            response=web.csrf(rf.get("/auth/csrf",secure=True,HTTP_HOST="auth.example.test"))
            req=request();req.COOKIES["csrftoken"]=response.cookies["csrftoken"].value
            req.META["HTTP_X_CSRFTOKEN"]=json.loads(response.content)["csrf_token"]
            return req
        def login_command(label):return f["grant"](f["command"]("pixs.auth.session.create",f["actor"],label))
        count=m.AuthSession.objects.count()
        missing=web.login(request(),login_command("http-missing-csrf"),replace(f["supplied"],facade=Facade.WEB))
        out["csrf_missing_no_session"]=missing.status_code==403 and m.AuthSession.objects.count()==count
        login_req=csrf_request();old_csrf=login_req.COOKIES["csrftoken"]
        response=web.login(login_req,login_command("http-web-login"),replace(f["supplied"],facade=Facade.WEB))
        body=json.loads(response.content);cookie=response.cookies[WEB_COOKIE].value
        web_session=m.AuthSession.objects.get(pk=body["session"]["id"])
        out["web_login_committed"]=response.status_code==200 and web_session.state=="ACTIVE" and web_session.facade=="WEB"
        out["cookie_hash_only"]=m.AuthToken.objects.filter(session=web_session,digest=token_fingerprint(parse_token(cookie),TokenKind.WEB_SESSION)).exists() and not m.AuthToken.objects.filter(digest=cookie).exists()
        out["web_no_js_token"]=cookie not in response.content.decode() and response.cookies[WEB_COOKIE]["httponly"] is True
        out["csrf_rotated"]=response.cookies["csrftoken"].value!=old_csrf
        api_response=api.login(request(),login_command("http-api-login"),f["supplied"])
        api_body=json.loads(api_response.content)
        api_session=m.AuthSession.objects.get(pk=api_body["session"]["id"])
        out["api_pair_committed"]=api_response.status_code==200 and api_session.facade=="API" and len(api_body["access_token"])==43 and not api_response.cookies
        logout_cmd=f["grant"](f["command"]("pixs.auth.session.logout","pixs.auth.session:"+str(api_session.pk),"http-api-cookie-refused"))
        no_bearer=request();no_bearer.COOKIES[WEB_COOKIE]=cookie
        out["api_cookie_only_denied"]=api.invoke(no_bearer,logout_cmd,operation="logout").status_code==403 and m.AuthSession.objects.get(pk=api_session.pk).state=="ACTIVE"
        wrong_kind=api.invoke(request(HTTP_AUTHORIZATION="Bearer "+cookie),logout_cmd,operation="logout")
        out["web_token_not_api_bearer"]=wrong_kind.status_code==403 and m.AuthSession.objects.get(pk=web_session.pk).state=="ACTIVE"
        vault=MemoryRefreshVault();cli=CliAuthFacade(service=f["service"](),origin="https://auth.example.test",vault=vault)
        cli_status=cli.login(login_command("cli-real-login"),f["supplied"])
        out["cli_login_committed"]=cli_status.outcome is AuthOutcome.ISSUED and m.AuthSession.objects.get(pk=cli_status.session.session_id).state=="ACTIVE"
        access_before=cli._access.value;refresh_before=vault.get("https://auth.example.test",f["actor"]).value
        text=repr(cli_status)+repr(asdict(cli_status))+repr(cli)
        out["cli_status_no_token"]=access_before not in text and refresh_before not in text and not hasattr(cli_status,"emission")
        renew_cmd=f["grant"](f["command"]("pixs.auth.session.renew","pixs.auth.session:"+str(cli_status.session.session_id),"cli-real-renew"))
        rotated=cli.renew(renew_cmd)
        out["cli_refresh_rotated"]=rotated.outcome is AuthOutcome.ISSUED and rotated.session.session_id==cli_status.session.session_id and cli._access.value!=access_before and vault.get("https://auth.example.test",f["actor"]).value!=refresh_before
        target=f["grant"](f["command"]("pixs.auth.session.revoke","pixs.auth.session:"+str(api_session.pk),"cli-other-session-revoke"))
        revoked=cli.invoke(target,operation="revoke_session")
        out["cli_other_revoke_preserves_access"]=revoked.outcome is AuthOutcome.WITHDRAWN and cli._access is not None and m.AuthSession.objects.get(pk=api_session.pk).state=="REVOKED" and m.AuthSession.objects.get(pk=cli_status.session.session_id).state=="ACTIVE"
        cli._service=f["service"](1)
        cli_logout=f["grant"](f["command"]("pixs.auth.session.logout","pixs.auth.session:"+str(cli_status.session.session_id),"cli-real-pending-logout"))
        pending=cli.invoke(cli_logout,operation="logout")
        out["cli_pending_withdraw_clears_local"]=pending.outcome is AuthOutcome.WITHDRAWN_AUDIT_PENDING and pending.local_clear_confirmed and cli._access is None and vault.get("https://auth.example.test",f["actor"]) is None
        web_logout=f["grant"](f["command"]("pixs.auth.session.logout","pixs.auth.session:"+str(web_session.pk),"http-web-logout"))
        logout_request=csrf_request();logout_request.COOKIES[WEB_COOKIE]=cookie
        logged_out=web.invoke(logout_request,web_logout,operation="logout")
        out["web_logout_committed"]=logged_out.status_code==200 and m.AuthSession.objects.get(pk=web_session.pk).state=="REVOKED" and int(logged_out.cookies[WEB_COOKIE]["max-age"])==0
        unknown_cmd=login_command("http-unknown-commit")
        connection=connections["default"];real_commit=connection.commit;fired={"value":False}
        def uncertain():
            trigger=not fired["value"] and m.AuthOperation.objects.filter(operation_ref=unknown_cmd.operation_id).exists()
            real_commit()
            if trigger:
                fired["value"]=True
                raise OperationalError("synthetic-after-real-commit")
        with patch.object(connection,"commit",uncertain):unknown=api.login(request(),unknown_cmd,f["supplied"])
        unknown_body=json.loads(unknown.content)
        out["api_unknown_no_tokens"]=unknown.status_code==503 and unknown_body["outcome"]=="UNKNOWN" and "access_token" not in unknown_body and "refresh_token" not in unknown_body and not unknown.cookies
        out["api_unknown_actual_commit"]=fired["value"] and m.AuthOperation.objects.using("peer").filter(operation_ref=unknown_cmd.operation_id).exists()
        insecure=rf.post("/auth/fixture",secure=False,HTTP_HOST="auth.example.test")
        before=m.AuthSession.objects.count()
        out["https_boundary_no_mutation"]=api.login(insecure,login_command("http-insecure"),f["supplied"]).status_code==403 and m.AuthSession.objects.count()==before
        out["public_contracts_implemented"]=all(isinstance(f["service"](),contract) for contract in (AuthenticationService,SessionService,CredentialService))
        cli.close()
    return out

def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result=run_in_auth_schema(root_str,scenarios,EXPECTED_CASES,with_core=True)
    result["real_components"]=["WebAuthFacade","ApiAuthFacade","CliAuthFacade","PostgresLocalAuthService","RuntimeAuthorizationDecider","PostgresAuditParticipant"]
    result["full_p0_activation"]=False
    return result
