"""Recette HTTP C06 : Auth/C04/C05/Core/C06 réels ; C09/C10 explicitement synthétiques."""
from __future__ import annotations

_HTTP_DIAGNOSTICS = []

EXPECTED_CASES = (
    "http_login_real_c03", "http_create_user_real_owners", "http_replay_initial_result",
    "http_divergence_no_second_effect", "http_list_filtered_sql_keyset",
    "http_cursor_tamper_closed", "http_cursor_snapshot_change_closed",
    "http_ordinary_no_implicit_permission", "http_transport_context_private_closed",
    "http_strict_json_method_limits", "http_errors_localized_sanitized",
    "http_refresh_not_access", "http_web_cookie_csrf", "http_revoked_access_closed",
    "http_refresh_renewal_does_not_extend_activity", "http_background_query_no_activity",
    "http_interactive_activity_recorded_by_c03", "http_interactive_replay_no_new_activity",
    "http_activity_failure_preserves_confirmed_core_result",
)


def make_http_fixture(*, interactive_commands=frozenset()):
    import datetime
    import hashlib
    import json
    from dataclasses import replace
    from django.conf import settings
    from django.db import connections
    from django.test import RequestFactory
    from auth_service_fixture import make_auth_service_fixture
    import core_pg_participants as doubles
    from pixs.auth.api_request_source import ApiRequestSource
    from pixs.auth.contracts import AuthCommand, AuthDataClassification
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.backend.api_core_catalog import ApiInputLimits, COMMANDS, QUERIES
    from pixs.backend.api_core_composition import CoreApiComposition, CoreHttpLimits
    from pixs.backend.api_core_pagination import CoreCursorCodec, CoreCursorConfig
    from pixs.backend.api_core_views import build_core_api_view
    from pixs.core.api_core_idempotency_repository import CoreApiIdempotencyRepository
    from pixs.core.api_core_idempotency_values import ApiCoreIdempotencyConfig
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant, PostgresAuditSink
    from pixs.core.authz.filter_plan import FilterConfig
    from pixs.core.authz.policy import Effect, Policy, Selector, ScopeSelector, Obligation
    from pixs.core.authz.ports import Request
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy, decode_policy
    from pixs.core.query_source import CoreFactSource
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.core.services_runtime_filter import RuntimeSourceFilterProvider
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.kernel.data_governance_profile import DataGovernanceProfile

    settings.ALLOWED_HOSTS = ["api.example.test"]
    settings.SECRET_KEY = "Vecteur public de recette Django C06, sans secret de déploiement"
    settings.CSRF_TRUSTED_ORIGINS = ["https://api.example.test"]
    f = make_auth_service_fixture()
    offset = [0]
    f["clock"].now = lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=offset[0])
    source = ApiRequestSource(alias="default", profile_id=f["profile"].profile_id,
        trust_source=f["trust"], assurance_source=f["assurance"],
        facts_reader=CoreFactSource(), clock=f["clock"], max_identifier_chars=128)
    with connections["default"].cursor() as cursor:
        cursor.execute("SELECT current_schema()")
        namespace = cursor.fetchone()[0]
        assert __import__("re").fullmatch(r"c03_[0-9a-f]{16}", namespace)
        cursor.execute("CREATE TABLE c02_syn_stages (kind TEXT NOT NULL, op TEXT NOT NULL, token TEXT NOT NULL, backend_pid INTEGER NOT NULL, txid TEXT NOT NULL, detail JSONB NOT NULL)")
    profile = DataGovernanceProfile("1.0.0", "synthetic:asset", "pixs.core", "synthetic:truth",
        frozenset({"synthetic:class"}), ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE,
        frozenset({"synthetic:purpose"}), "synthetic:retention", "synthetic:deletion",
        frozenset(), frozenset({"synthetic:consumer"}), frozenset(), "synthetic:export", "synthetic:lineage")
    references = set()
    contexts = {f["context"]}
    filter_limit = [128]
    actions = tuple(sorted({s["action"] for s in COMMANDS.values()} | {s["action"] for s in QUERIES.values()}))
    def grant(action, resource, context=None, effect=Effect.ALLOW):
        ctx = f["context"] if context is None else context
        references.add(resource)
        contexts.add(ctx)
        pid = "http-" + hashlib.sha256(json.dumps([action, resource, [ctx.scope_type.value,ctx.tenant_id,ctx.scope_id], effect.value]).encode()).hexdigest()[:32]
        if not CorePolicy.objects.filter(policy_id=pid).exists():
            p = Policy(pid, "1.0.0", "pixs.core", effect, Selector("subject", (f["actor"],)),
                       Selector("resource", (resource,)), Selector("action", (action,)),
                       ScopeSelector((ctx,)), obligations=(Obligation("AUDIT"),))
            CorePolicy.objects.create(policy_id=pid, policy_version=p.policy_version,
                owner=p.owner, effect=p.effect.value, definition=encode_policy(p))
        return pid
    def common(*, request, operation_id, authentication_source):
        resources = references | {request.resource_id, f["actor"]}
        declared_actions, subjects, scopes = set(actions), {f["actor"]}, contexts | {request.context}
        for definition in CorePolicy.objects.values_list("definition", flat=True):
            policy = decode_policy(definition)
            resources.update(policy.resource.values)
            declared_actions.update(policy.action.values)
            subjects.update(policy.subject.values)
            scopes.update(policy.scope.contexts)
        for spec in QUERIES.values():
            from pixs.backend.api_core_catalog import context_mode
            if context_mode(request.context) in spec["roots"]:
                resources.update(CoreFactSource().candidates(spec["kind"],request.context,"default",128))
        limits = Limits(512, 512, 16, 100, 100, 512, 512, 512, 10000000, 60, 3600)
        store = CoreAuthorizationStore(alias="default", installation_ref="http-c06-fixture",
            base_epoch="http-c06-v1", catalog=Catalog(tuple(sorted(subjects)), tuple(sorted(resources)),
            tuple(sorted(declared_actions)), tuple(sorted(scopes, key=lambda c: (c.scope_type.value,c.tenant_id or "",c.scope_id or ""))), ()), limits=limits)
        provider = RuntimeTrustedFactsProvider(store=store, authentication_source=authentication_source,
            request=request, operation_id=operation_id,
            additional_owners=(RuntimeResourceOwner("pixs.auth.",authentication_source.ownership),))
        decider = RuntimeAuthorizationDecider(store=store, facts_provider=provider,
            clock=f["clock"], request=request, operation_id=operation_id)
        return store, provider, decider, resources
    def factory(*, request, operation_id, authentication_source):
        store,provider,decider,resources=common(request=request,operation_id=operation_id,authentication_source=authentication_source)
        from pixs.core.services_runtime_declarations import RuntimeDeclarationValidator
        policy = AuditPolicy("http-audit", "1.0.0", "fixture-explicite", 1, 65536, 100, (),
            "http:audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
        audit = PostgresAuditParticipant(ExplicitAuditPolicySource(request.context, policy), f["clock"], "peer")
        filter_provider = RuntimeSourceFilterProvider(store, provider, f["clock"],
            PostgresAuditSink(audit, "default", request.context, operation_id), FilterConfig(filter_limit[0]), request, operation_id)
        flags = {"read_refs": tuple(sorted(resources))}
        supplied = doubles.make_ports("default", f["actor"], flags)
        idem = CoreApiIdempotencyRepository(alias="default", peer_alias="peer",
            config=ApiCoreIdempotencyConfig(3600,128,128,128,128,128), clock=f["clock"],
            request=request, operation_id=operation_id, profile=profile, decider=decider)
        return replace(supplied, facts_provider=provider, clock=f["clock"], decider=decider,
            filter_provider=filter_provider, audit=audit, idempotence=idem,
            declarations=RuntimeDeclarationValidator(store=store,request=request,operation_id=operation_id,
                                                   owners=("pixs.core","pixs.auth")))
    class Classification:
        def resolve(self, **kwargs):
            return AuthDataClassification("http-auth-asset", ConfidentialityLevel.CONFIDENTIAL, PersonalDataLevel.PERSONAL)
    def auth_factory(**kwargs):
        return common(**kwargs)[2]
    auth_policy=AuditPolicy("http-auth-audit","1.0.0","fixture-explicite",1,65536,100,(),
        "http:auth-audit",ConfidentialityLevel.INTERNAL,PersonalDataLevel.PERSONAL)
    auth_service=PostgresLocalAuthService(alias="default",peer_alias="peer",profile_id=f["profile"].profile_id,
        trust_source=f["trust"],assurance_source=f["assurance"],facts_reader=CoreFactSource(),clock=f["clock"],
        audit=PostgresAuditParticipant(ExplicitAuditPolicySource(f["context"],auth_policy),f["clock"],"peer"),
        classification_source=Classification(),decider_factory=auth_factory)
    composition = CoreApiComposition(alias="default", peer_alias="peer", request_source=source,
        auth_service=auth_service, core_ports_factory=factory, clock=f["clock"],
        approved_host="api.example.test", approved_origin="https://api.example.test",
        limits=CoreHttpLimits(65536,8192,2,10), input_limits=ApiInputLimits(128,128,32768,16),
        cursor_codec=CoreCursorCodec(config=CoreCursorConfig(60,8192,128,128,10),
            key=b"Vecteur public de signature C06 recette seulement", clock=f["clock"]),
        interactive_commands=interactive_commands)
    from pixs.backend.api_core_openapi import build_core_openapi_documents, core_api_contract_plan
    approved_documents=build_core_openapi_documents(composition)
    contract_plan=core_api_contract_plan()
    view = build_core_api_view(composition, previous_plan=contract_plan,
                              previous_documents=tuple(text for _,text in approved_documents))
    rf = RequestFactory()
    def call(method, path, body=None, *, bearer=None, headers=None, cookies=None, secure=True, raw_body=None):
        extra = {"HTTP_HOST":"api.example.test"}
        if bearer is not None:
            extra["HTTP_AUTHORIZATION"] = "Bearer " + bearer
        if headers:
            extra.update(headers)
        encoded = raw_body if raw_body is not None else (json.dumps(body).encode() if body is not None else b"")
        request = rf.generic(method, path, data=encoded, content_type="application/json", secure=secure, **extra)
        request.META["RAW_URI"] = path
        if cookies:
            request.COOKIES.update(cookies)
        response = view(request)
        result = json.loads(response.content.decode())
        _HTTP_DIAGNOSTICS.append({"kind":"response","index":len(_HTTP_DIAGNOSTICS),"status":response.status_code,"error_code":result.get("error_code") if type(result.get("error_code")) is str and result["error_code"].startswith("pixs.core.api.v1.") else None})
        return response, result
    def grant_auth(action, resource, *, context=None, effect=Effect.ALLOW):
        ctx=f["context"] if context is None else context
        references.add(resource);contexts.add(ctx)
        material=[action,resource,[ctx.scope_type.value,ctx.tenant_id,ctx.scope_id],effect.value]
        pid="http-auth-"+hashlib.sha256(json.dumps(material).encode()).hexdigest()[:32]
        if not CorePolicy.objects.filter(policy_id=pid).exists():
            policy=Policy(pid,"1.0.0","pixs.auth",effect,Selector("subject",(f["actor"],)),
                Selector("resource",(resource,)),Selector("action",(action,)),ScopeSelector((ctx,)),
                obligations=(Obligation("AUDIT"),))
            CorePolicy.objects.create(policy_id=pid,policy_version=policy.policy_version,
                owner=policy.owner,effect=effect.value,definition=encode_policy(policy))
        return pid
    return dict(f=f, source=source, composition=composition, call=call, grant=grant,
                grant_auth=grant_auth, offset=offset, references=references, contexts=contexts,
                filter_limit=filter_limit, documents=approved_documents, contract_plan=contract_plan)


def scenarios():
    import json
    from urllib.parse import urlsplit, parse_qs
    from django.db import connections
    from pixs.auth.facades import WEB_COOKIE
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.query_source import collection_ref
    h = make_http_fixture(interactive_commands=frozenset({"create-user"}))
    f, call, grant = h["f"], h["call"], h["grant"]
    base = "/api/v1/platform"
    key = lambda value: {"HTTP_IDEMPOTENCY_KEY":value}
    h["grant_auth"]("pixs.auth.session.create", f["actor"])
    response, login = call("POST", base+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},
        headers=key("http-login"))
    assert response.status_code == 200, "LOGIN_HTTP_REFUSE"
    emission = login["data"]
    # Les émissions restent seulement en mémoire du processus masqué.
    access, refresh = emission["access_token"], emission["refresh_token"]
    cases = {"http_login_real_c03":True}
    uid = generate_uuid7()
    ref = "pixs.core.user:"+str(uid)
    grant("pixs.core.identity.user.create", ref)
    response, first = call("POST",base+"/commands/create-user",{"user_id":str(uid)},bearer=access,headers=key("http-create"))
    assert response.status_code == 200, "CREATION_HTTP_REFUSE"
    assert CoreUser.objects.filter(pk=uid).count() == 1
    cases["http_create_user_real_owners"] = True
    response, replay = call("POST",base+"/commands/create-user",{"user_id":str(uid)},bearer=access,
                            headers={**key("http-create"),"HTTP_X_CORRELATION_ID":"correlation-de-rejeu"})
    assert response.status_code == 200 and replay["data"] == first["data"]
    assert replay["meta"]["correlation_id"] == "correlation-de-rejeu"
    cases["http_replay_initial_result"] = True
    other = generate_uuid7()
    grant("pixs.core.identity.user.create","pixs.core.user:"+str(other))
    response, conflict = call("POST",base+"/commands/create-user",{"user_id":str(other)},bearer=access,headers=key("http-create"))
    assert response.status_code == 409 and not CoreUser.objects.filter(pk=other).exists()
    cases["http_divergence_no_second_effect"] = True
    for label in ("second","third"):
        identifier=generate_uuid7();r="pixs.core.user:"+str(identifier)
        grant("pixs.core.identity.user.create",r)
        response,_=call("POST",base+"/commands/create-user",{"user_id":str(identifier)},bearer=access,headers=key("http-"+label))
        assert response.status_code==200
        grant("pixs.core.identity.read",r)
    grant("pixs.core.identity.read",ref)
    grant("pixs.core.identity.read",collection_ref("USER",f["context"]))
    statements=[]
    def capture(execute, sql, params, many, context):
        statements.append(sql)
        return execute(sql,params,many,context)
    with connections["default"].execute_wrapper(capture):
        response, page = call("GET",base+"/users?limit=2",bearer=access)
    assert response.status_code==200 and len(page["data"])==2 and "next" in page["links"], "PAGE_HTTP_REFUSE"
    assert any('pixs_core_user' in s and "ORDER BY" in s and "LIMIT 3" in s for s in statements)
    next_path=page["links"]["next"]
    response,last=call("GET",next_path,bearer=access)
    assert response.status_code==200 and len(last["data"])==1 and not last["links"]
    cases["http_list_filtered_sql_keyset"]=True
    from urllib.parse import urlencode
    query=parse_qs(urlsplit(next_path).query)
    token=query["cursor"][0]
    replacement=("A" if token[-1]!="A" else "B")
    query["cursor"]=[token[:-1]+replacement]
    tampered_path=urlsplit(next_path).path+"?"+urlencode(query,doseq=True)
    assert tampered_path != next_path
    response,_=call("GET",tampered_path,bearer=access)
    assert response.status_code==400
    cases["http_cursor_tamper_closed"]=True
    grant("pixs.core.identity.read","pixs.core.user:"+str(generate_uuid7()))
    response,_=call("GET",next_path,bearer=access)
    assert response.status_code==400
    cases["http_cursor_snapshot_change_closed"]=True
    denied=generate_uuid7()
    response,_=call("POST",base+"/commands/create-user",{"user_id":str(denied)},bearer=access,headers=key("no-allow"))
    assert response.status_code==403 and not CoreUser.objects.filter(pk=denied).exists()
    cases["http_ordinary_no_implicit_permission"]=True
    for path,extra,secure,status in (
        (base+"/users",{},False,403),
        (base+"/users",{"HTTP_X_TENANT_ID":"another"},True,400),
        ("/api/v1/platform/private/credentials",{},True,404),
        ("/api/v1/tenants/foreign/groups",{},True,401),
    ):
        response,_=call("GET",path,bearer=access,headers=extra,secure=secure)
        assert response.status_code==status, "FRONTIERE_HTTP_INCOHERENTE"
    cases["http_transport_context_private_closed"]=True
    for method,path,body,raw,status in (
        ("GET",base+"/commands/create-user",None,None,405),
        ("POST",base+"/commands/create-user",None,b'{"user_id":"x","user_id":"y"}',400),
        ("POST",base+"/commands/create-user",None,b'{"user_id":1.5}',400),
        ("POST",base+"/commands/create-user",{"user_id":str(uid),"actor":"forged"},None,400),
        ("POST",base+"/commands/create-user",None,b" "*65537,413),
        ("GET",base+"/users?limit=2&limit=3",None,None,400),
    ):
        response,_=call(method,path,body,bearer=access,headers=key("invalid"),raw_body=raw)
        assert response.status_code==status, "ENTREE_HTTP_INCOHERENTE"
    cases["http_strict_json_method_limits"]=True
    response,error=call("GET",base+"/private",bearer=access,headers={"HTTP_ACCEPT_LANGUAGE":"fr"})
    assert response.status_code==404 and error["message"]=="Ressource introuvable."
    assert not any(word in json.dumps(error) for word in ("traceback","password","Bearer","SELECT"))
    cases["http_errors_localized_sanitized"]=True
    response,_=call("GET",base+"/users",bearer=refresh)
    assert response.status_code==401
    cases["http_refresh_not_access"]=True
    from pixs.auth.models import AuthSession, AuthOperation
    api_session=AuthSession.objects.get(pk=emission["session"]["id"])
    api_activity=api_session.last_activity_at
    h["grant_auth"]("pixs.auth.session.renew","pixs.auth.session:"+str(api_session.pk))
    response,renewed=call("POST",base+"/auth/renew",{},bearer=refresh,headers=key("http-renew"))
    assert response.status_code==200 and renewed["data"]["session"]["id"]==str(api_session.pk)
    api_session.refresh_from_db()
    assert api_session.last_activity_at==api_activity
    access,refresh=renewed["data"]["access_token"],renewed["data"]["refresh_token"]
    cases["http_refresh_renewal_does_not_extend_activity"]=True
    response,csrf=call("GET","/api/v1/web/auth/csrf")
    assert response.status_code==200 and "csrftoken" in response.cookies
    cookie=response.cookies["csrftoken"].value
    webbase="/api/v1/web/platform"
    response,_=call("POST",webbase+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},
        headers={**key("web-login"),"HTTP_ORIGIN":"https://api.example.test"})
    assert response.status_code==403
    response,web=call("POST",webbase+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},
        headers={**key("web-login"),"HTTP_ORIGIN":"https://api.example.test","HTTP_X_CSRFTOKEN":cookie},
        cookies={"csrftoken":cookie})
    assert response.status_code==200 and WEB_COOKIE in response.cookies
    value=response.cookies[WEB_COOKIE].value
    browser_csrf=response.cookies["csrftoken"].value
    browser_session=AuthSession.objects.get(pk=web["data"]["session"]["id"])
    initial_activity=browser_session.last_activity_at
    response,_=call("GET",webbase+"/users",cookies={WEB_COOKIE:value})
    assert response.status_code==200
    browser_session.refresh_from_db()
    assert browser_session.last_activity_at==initial_activity
    cases["http_background_query_no_activity"]=True
    resource="pixs.auth.session:"+str(browser_session.pk)
    h["grant_auth"]("pixs.auth.session.activity",resource)
    interactive=generate_uuid7();interactive_ref="pixs.core.user:"+str(interactive)
    grant("pixs.core.identity.user.create",interactive_ref)
    headers={**key("interactive-first"),"HTTP_ORIGIN":"https://api.example.test","HTTP_X_CSRFTOKEN":browser_csrf}
    cookies={WEB_COOKIE:value,"csrftoken":browser_csrf}
    before_count=AuthOperation.objects.filter(action_id="pixs.auth.session.activity").count()
    response,recorded=call("POST",webbase+"/commands/create-user",{"user_id":str(interactive)},headers=headers,cookies=cookies)
    assert response.status_code==200 and recorded["meta"]["activity"]=={"status":"RECORDED"}
    browser_session.refresh_from_db()
    assert browser_session.last_activity_at>initial_activity
    activity=browser_session.last_activity_at
    assert AuthOperation.objects.filter(action_id="pixs.auth.session.activity").count()==before_count+1
    cases["http_interactive_activity_recorded_by_c03"]=True
    response,replayed=call("POST",webbase+"/commands/create-user",{"user_id":str(interactive)},headers=headers,cookies=cookies)
    assert response.status_code==200 and replayed["data"]==recorded["data"]
    assert replayed["meta"]["activity"]=={"status":"REPLAY_IGNORED"}
    browser_session.refresh_from_db()
    assert browser_session.last_activity_at==activity
    assert AuthOperation.objects.filter(action_id="pixs.auth.session.activity").count()==before_count+1
    cases["http_interactive_replay_no_new_activity"]=True
    from pixs.core.authz.policy import Effect
    h["grant_auth"]("pixs.auth.session.activity",resource,effect=Effect.DENY)
    denied_activity=generate_uuid7();grant("pixs.core.identity.user.create","pixs.core.user:"+str(denied_activity))
    response,confirmed=call("POST",webbase+"/commands/create-user",{"user_id":str(denied_activity)},
        headers={**headers,**key("interactive-activity-denied")},cookies=cookies)
    assert response.status_code==200 and CoreUser.objects.filter(pk=denied_activity).exists()
    assert confirmed["meta"]["activity"]["status"]=="NOT_RECORDED"
    assert confirmed["meta"]["activity"]["error_code"].startswith("pixs.core.api.v1.")
    browser_session.refresh_from_db()
    assert browser_session.last_activity_at==activity
    assert AuthOperation.objects.filter(action_id="pixs.auth.session.activity").count()==before_count+1
    cases["http_activity_failure_preserves_confirmed_core_result"]=True
    response,_=call("GET",base+"/users",bearer=access,cookies={WEB_COOKIE:value})
    assert response.status_code==403
    cases["http_web_cookie_csrf"]=True
    # Session API actuelle retirée par le propriétaire C03.
    session=emission["session"]["id"]
    h["grant_auth"]("pixs.auth.session.logout","pixs.auth.session:"+session)
    response,_=call("POST",base+"/auth/logout",{},bearer=access,headers=key("logout"))
    assert response.status_code==200
    response,_=call("GET",base+"/users",bearer=access)
    assert response.status_code==401
    cases["http_revoked_access_closed"]=True
    assert set(cases)==set(EXPECTED_CASES) and all(cases.values())
    return cases


def run_real_api_core_platform(root_str):
    from auth_pg_test_support import run_in_auth_schema
    import pixs.backend.api_core_views as boundary
    import re
    original = boundary.classify_error
    _HTTP_DIAGNOSTICS.clear()
    def classify(error):
        chain, cause = [], error
        for _ in range(4):
            if cause is None:
                break
            code = getattr(cause, "code", None)
            frames, tb = [], cause.__traceback__
            while tb is not None and len(frames) < 12:
                filename = tb.tb_frame.f_code.co_filename.rsplit("/", 1)[-1]
                frames.append([filename,tb.tb_lineno,tb.tb_frame.f_code.co_name])
                tb = tb.tb_next
            chain.append({"type":type(cause).__name__,"code":code if type(code) is str and re.fullmatch("[A-Z_]{1,64}",code) else None,"frames":frames})
            cause = cause.__cause__
        if len(_HTTP_DIAGNOSTICS)<128:
            _HTTP_DIAGNOSTICS.append({"kind":"error","chain":chain})
        return original(error)
    boundary.classify_error = classify
    try:
        result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES,
                                   with_core=True, core_target="0003_core_idempotence")
    finally:
        boundary.classify_error = original
    result["http_diagnostics"] = _HTTP_DIAGNOSTICS[:128]
    return result


if __name__ == "__main__":
    import json
    from pathlib import Path
    outcome = run_real_api_core_platform(str(Path(__file__).resolve().parents[2]))
    print(json.dumps(outcome,ensure_ascii=False,sort_keys=True))
    raise SystemExit(0 if outcome.get("real_pg") and outcome.get("cleanup") and outcome.get("conns_closed") else 1)
