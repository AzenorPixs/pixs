"""Recette tenant C06 : vrais Auth/C04/C05 et ASGI ; C09/C10 explicitement synthétiques."""
from __future__ import annotations

_DIAGNOSTICS=[]
EXPECTED_CASES=(
 "tenant_platform_setup_real_owners","tenant_login_with_real_owner",
 "intent_token_is_not_password_proof","intent_context_and_operation_bound",
 "intent_requires_explicit_policy","tenant_group_membership_commands",
 "tenant_acl_declaration_role_grant_revoke","tenant_no_implicit_permission",
 "tenant_body_header_context_closed","root_assurances_preserved",
 "root_granted_overrides_acl_deny","root_ungranted_refused_even_acl_allow",
 "root_token_no_context_promotion","root_sql_keyset_tenant_isolation",
 "root_web_facade_same_exception","scope_create_and_login_real",
 "scope_token_no_parent_promotion","scope_group_and_query_real",
 "existing_auth_metadata_rejects_intent","global_auth_routes_platform_only",
 "permission_existing_mismatch_inactive_closed",
)


def scenarios():
    import json
    from dataclasses import replace
    from io import BytesIO
    from urllib.parse import quote,unquote,urlsplit
    from django.core.handlers.asgi import ASGIRequest
    from test_api_core_platform_postgres import make_http_fixture
    from pixs.auth.contracts import AuthDataClassification,AuthServiceError
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.backend.api_core_openapi import build_core_openapi_documents,core_api_contract_plan
    from pixs.backend.api_core_views import build_core_api_view
    from pixs.core.audit_contracts import AuditError,AuditPolicy
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.scope.context import ScopeContext,ScopeType
    from pixs.kernel.data_governance import ConfidentialityLevel,PersonalDataLevel

    h=make_http_fixture()
    f=h["f"];actor=f["actor"];call=h["call"]
    h["grant_auth"]("pixs.auth.session.create",actor)
    response,login=call("POST","/api/v1/platform/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},
        headers={"HTTP_IDEMPOTENCY_KEY":"tenant-setup-login"})
    assert response.status_code==200
    bearer=login["data"]["access_token"]
    tenant="tenant/a é "
    h["grant"]("pixs.core.scope.tenant.create","pixs.core.tenant:"+tenant)
    response,_=call("POST","/api/v1/platform/commands/create-tenant",{"tenant_id":tenant},
        bearer=bearer,headers={"HTTP_IDEMPOTENCY_KEY":"tenant-setup-create"})
    assert response.status_code==200
    cases={"tenant_platform_setup_real_owners":True}
    context=ScopeContext(ScopeType.TENANT,tenant)
    h["contexts"].add(context)
    from pixs.auth.identifiers import session_creation_reference
    h["grant_auth"]("pixs.auth.session.create",session_creation_reference(actor,context),context=context)
    audit_policy=AuditPolicy("tenant-http-audit","1.0.0","fixture-explicite",1,65536,100,(),
        "tenant:http-audit",ConfidentialityLevel.INTERNAL,PersonalDataLevel.PERSONAL)
    class Policies:
        def resolve(self,*,context,alias):
            if alias!="default" or context not in h["contexts"]:
                raise AuditError()
            return audit_policy
    class Classification:
        def resolve(self,*,context,alias,operation_id):
            if alias!="default" or context not in h["contexts"]:
                raise AuthServiceError("AUTH_DENIED")
            return AuthDataClassification("tenant-auth-fixture",ConfidentialityLevel.CONFIDENTIAL,PersonalDataLevel.PERSONAL)
    original=h["composition"]
    def decider(**kwargs):
        return original.core_ports(**kwargs).decider
    service=PostgresLocalAuthService(alias="default",peer_alias="peer",profile_id=f["profile"].profile_id,
        trust_source=f["trust"],assurance_source=f["assurance"],facts_reader=__import__(
            "pixs.core.query_source",fromlist=["CoreFactSource"]).CoreFactSource(),
        clock=f["clock"],audit=PostgresAuditParticipant(Policies(),f["clock"],"peer"),
        classification_source=Classification(),decider_factory=decider)
    composition=replace(original,auth_service=service)
    documents=build_core_openapi_documents(composition)
    view=build_core_api_view(composition,previous_plan=core_api_contract_plan(),
                            previous_documents=tuple(text for _,text in documents))
    def asgi_call(method,path,body=None,token=None,key=None,headers_extra=None,cookies=None):
        parsed=urlsplit(path);data=json.dumps({} if body is None else body).encode()
        headers=[(b"host",b"api.example.test"),(b"content-type",b"application/json"),
                 (b"content-length",str(len(data)).encode())]
        if token is not None:headers.append((b"authorization",("Bearer "+token).encode()))
        if key is not None:headers.append((b"idempotency-key",key.encode()))
        if headers_extra:
            headers.extend((name.lower().encode("ascii"),value.encode("ascii")) for name,value in headers_extra.items())
        if cookies:
            headers.append((b"cookie","; ".join(name+"="+value for name,value in cookies.items()).encode("ascii")))
        scope={"type":"http","asgi":{"version":"3.0"},"http_version":"1.1","method":method,
            "scheme":"https","path":unquote(parsed.path),"raw_path":parsed.path.encode("ascii"),
            "query_string":parsed.query.encode("ascii"),"root_path":"","headers":headers,
            "server":("api.example.test",443),"client":("127.0.0.1",12345)}
        request=ASGIRequest(scope,BytesIO(data))
        response=view(request);out=json.loads(response.content)
        _DIAGNOSTICS.append({"status":response.status_code,"error_code":out.get("error_code")})
        return response,out
    base="/api/v1/tenants/"+quote(tenant,safe="")
    response,session=asgi_call("POST",base+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},
        key="tenant-login")
    assert response.status_code==200
    cases["tenant_login_with_real_owner"]=True
    from pixs.auth.tokens import parse_token,TokenKind
    from pixs.auth.runtime_verifier import AuthVerificationError
    from pixs.auth.resource_metadata import AuthResourceMetadataResolver
    from pixs.core.authz.policy import Effect
    from pixs.core.authz.ports import Request
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.persistence.models_group import CoreGroup,CoreIdentityTenantMembership
    from pixs.core.persistence.models_identity import CoreSuperAdminBinding,CoreSuperAdminTenantGrant
    from pixs.core.query_source import collection_ref,CoreFactSource
    from django.db import connections,transaction
    from pixs.auth.facades import WEB_COOKIE
    token_a=session["data"]["access_token"]
    session_a=session["data"]["session"]["id"]
    intent=session_creation_reference(actor,context)
    hint=h["source"].resolve_token(context=context,token=parse_token(token_a),kind=TokenKind.ACCESS)
    request=h["source"].request(actor=hint,resource_id=intent,action_id="pixs.auth.session.create",
                               correlation_id="intent-probe",decision_id="intent-probe")
    with h["source"].open_core_source(request=request,operation_id="intent-probe",token=parse_token(token_a),kind=TokenKind.ACCESS) as source:
        assert source.ownership(intent,context=context,alias="default",operation_id="intent-probe") is None
        cases["intent_token_is_not_password_proof"]=True
        for values in (dict(context=ScopeContext(ScopeType.TENANT,"foreign"),alias="default",operation_id="intent-probe"),
                       dict(context=context,alias="default",operation_id="wrong-operation")):
            try:source.ownership(intent,**values)
            except AuthVerificationError:pass
            else:raise AssertionError("INTENT_HORS_LIAISON_ACCEPTE")
        cases["intent_context_and_operation_bound"]=True
    with transaction.atomic():
        resolver=AuthResourceMetadataResolver(request=request,alias="default",operation_id="intent-existing")
        assert resolver.ownership(intent,context=context,alias="default",operation_id="intent-existing") is None
    cases["existing_auth_metadata_rejects_intent"]=True

    member_ref="pixs.core.identity-tenant:"+str(f["identity"])+"/"+tenant
    h["grant"]("pixs.core.groups.tenant-membership.activate",member_ref,context=context)
    response,_=asgi_call("POST",base+"/commands/activate-tenant-membership",
        {"identity_id":str(f["identity"])},token=token_a,key="tenant-membership")
    assert response.status_code==200
    assert CoreIdentityTenantMembership.objects.get(identity_id=f["identity"],tenant_id=tenant).activation=="ACTIVE"
    group=generate_uuid7();group_ref="pixs.core.group:"+str(group)
    h["grant"]("pixs.core.groups.group.create",group_ref,context=context)
    response,_=asgi_call("POST",base+"/commands/create-group",{"group_id":str(group)},token=token_a,key="tenant-group")
    assert response.status_code==200 and CoreGroup.objects.get(pk=group).tenant_id==tenant
    cases["tenant_group_membership_commands"]=True

    permission="c06-read-group";permission_ref="pixs.core.permission:"+permission
    h["grant"]("pixs.core.authz.permission.declare",permission_ref)
    response,_=call("POST","/api/v1/platform/commands/declare-permission",
        {"permission_id":permission,"owner_component":"pixs.core","resource_ref":group_ref,"action_ref":"pixs.core.groups.read"},
        bearer=bearer,headers={"HTTP_IDEMPOTENCY_KEY":"tenant-permission"})
    assert response.status_code==200
    from pixs.core.persistence.models_authz import CorePermission
    from pixs.core.ports import CorePortError
    inactive="c06-inactive-permission"
    CorePermission.objects.create(permission_id=inactive,owner="pixs.core",resource_ref=group_ref,
        action_ref="pixs.core.groups.read",persistence_state="SOFT_DELETED",
        governance_ref="fixture:inactive",confidentiality="INTERNAL",personal="NONE")
    opaque=parse_token(bearer)
    hint_p=h["source"].resolve_token(context=f["context"],token=opaque,kind=TokenKind.ACCESS)
    req=h["source"].request(actor=hint_p,resource_id=permission_ref,action_id="pixs.core.authz.permission.declare",
        correlation_id="permission-variants",decision_id="permission-variants")
    with h["source"].open_core_source(request=req,operation_id="permission-variants",token=opaque,kind=TokenKind.ACCESS) as source:
        ports=original.core_ports(request=req,operation_id="permission-variants",authentication_source=source)
        with transaction.atomic():
            for pid,owner in ((permission,"pixs.auth"),(inactive,"pixs.core")):
                try:
                    ports.declarations.validate_permission(permission_id=pid,owner=owner,resource_ref=group_ref,
                        action_ref="pixs.core.groups.read",alias="default",operation_id="permission-variants",
                        transaction_token="permission-variants",context=f["context"])
                except CorePortError:pass
                else:raise AssertionError("PERMISSION_DIFFERENTE_OU_INACTIVE_ACCEPTEE")
    assert CorePermission.objects.get(pk=permission).version==1
    cases["permission_existing_mismatch_inactive_closed"]=True
    role="c06-tenant-role";role_ref="pixs.core.role:"+role
    h["grant"]("pixs.core.authz.role.create",role_ref,context=context)
    response,_=asgi_call("POST",base+"/commands/create-role",{"role_id":role,"permission_ids":[permission]},
                         token=token_a,key="tenant-role")
    assert response.status_code==200
    assignment="pixs.core.role-assignment:"+quote(role,safe="")+"/IDENTITY/"+str(f["identity"])
    h["grant"]("pixs.core.authz.role.assign",assignment,context=context)
    response,_=asgi_call("POST",base+"/commands/assign-role",
        {"role_id":role,"subject_type":"IDENTITY","subject_ref":str(f["identity"])},token=token_a,key="tenant-assignment")
    assert response.status_code==200
    collection=collection_ref("GROUP",context)
    h["grant"]("pixs.core.groups.read",collection,context=context)
    response,allowed=asgi_call("GET",base+"/groups",token=token_a)
    assert response.status_code==200 and [item["ref"] for item in allowed["data"]]==[group_ref]
    h["grant"]("pixs.core.authz.role.unassign",assignment,context=context)
    response,_=asgi_call("POST",base+"/commands/unassign-role",
        {"role_id":role,"subject_type":"IDENTITY","subject_ref":str(f["identity"]),"expected_version":1},
        token=token_a,key="tenant-unassign")
    assert response.status_code==200
    response,denied=asgi_call("GET",base+"/groups",token=token_a)
    assert response.status_code==200 and denied["data"]==[]
    cases["tenant_acl_declaration_role_grant_revoke"]=True
    unallowed=generate_uuid7()
    response,_=asgi_call("POST",base+"/commands/create-group",{"group_id":str(unallowed)},token=token_a,key="tenant-no-allow")
    assert response.status_code==403 and not CoreGroup.objects.filter(pk=unallowed).exists()
    cases["tenant_no_implicit_permission"]=True
    response,_=asgi_call("POST",base+"/commands/create-group",
        {"group_id":str(unallowed),"tenant_id":"foreign"},token=token_a,key="tenant-body-conflict")
    assert response.status_code==400
    response,_=asgi_call("GET",base+"/groups",token=token_a,headers_extra={"x-tenant-id":"foreign"})
    assert response.status_code==400
    cases["tenant_body_header_context_closed"]=True

    tenant_b="tenant-b";context_b=ScopeContext(ScopeType.TENANT,tenant_b)
    h["grant"]("pixs.core.scope.tenant.create","pixs.core.tenant:"+tenant_b)
    response,_=call("POST","/api/v1/platform/commands/create-tenant",{"tenant_id":tenant_b},
        bearer=bearer,headers={"HTTP_IDEMPOTENCY_KEY":"tenant-b-create"})
    assert response.status_code==200
    h["contexts"].add(context_b)
    base_b="/api/v1/tenants/"+quote(tenant_b,safe="")
    response,_=asgi_call("POST",base_b+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},key="tenant-b-no-policy")
    assert response.status_code in (401,403)
    cases["intent_requires_explicit_policy"]=True
    h["grant_auth"]("pixs.auth.session.logout","pixs.auth.session:"+login["data"]["session"]["id"])
    response,_=call("POST","/api/v1/platform/auth/logout",{},bearer=bearer,
                    headers={"HTTP_IDEMPOTENCY_KEY":"tenant-close-platform"})
    assert response.status_code==200
    h["grant_auth"]("pixs.auth.session.create",session_creation_reference(actor,context_b),context=context_b)
    response,login_b=asgi_call("POST",base_b+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},key="tenant-b-login")
    assert response.status_code==200
    token_b=login_b["data"]["access_token"]
    group_b=generate_uuid7();group_b_ref="pixs.core.group:"+str(group_b)
    h["grant"]("pixs.core.groups.group.create",group_b_ref,context=context_b)
    h["grant"]("pixs.core.groups.read",collection_ref("GROUP",context_b),context=context_b)
    h["grant"]("pixs.core.groups.read",group_b_ref,context=context_b)
    response,_=asgi_call("POST",base_b+"/commands/create-group",{"group_id":str(group_b)},token=token_b,key="tenant-b-group")
    assert response.status_code==200

    def assurances(token,ctx,label):
        opaque=parse_token(token)
        current=h["source"].resolve_token(context=ctx,token=opaque,kind=TokenKind.ACCESS)
        req=h["source"].request(actor=current,resource_id=collection_ref("GROUP",ctx),
            action_id="pixs.core.groups.read",correlation_id=label,decision_id=label)
        with h["source"].open_core_source(request=req,operation_id=label,token=opaque,kind=TokenKind.ACCESS) as source:
            auth,_=source.revalidate(req,alias="default",operation_id=label)
            return auth.identity_assurance,auth.authentication_assurance,auth.federation_trust
    before=assurances(token_a,context,"before-root")
    # État C08 de recette : vraies lignes de binding/grant, pas qualification du provisionnement R01.
    binding=CoreSuperAdminBinding.objects.create(installation_ref="http-c06-fixture",identity_id=f["identity"],
        governance_ref="fixture:binding",confidentiality="INTERNAL",personal="PERSONAL")
    CoreSuperAdminTenantGrant.objects.create(binding=binding,tenant_id=tenant,
        governance_ref="fixture:grant",confidentiality="INTERNAL",personal="PERSONAL")
    assert assurances(token_a,context,"after-root")==before
    cases["root_assurances_preserved"]=True
    root_groups=[]
    for number in range(3):
        identifier=generate_uuid7();reference="pixs.core.group:"+str(identifier)
        h["grant"]("pixs.core.groups.group.create",reference,context=context,effect=Effect.DENY)
        response,_=asgi_call("POST",base+"/commands/create-group",{"group_id":str(identifier)},
                             token=token_a,key="root-group-"+str(number))
        assert response.status_code==200 and CoreGroup.objects.get(pk=identifier).tenant_id==tenant
        root_groups.append(reference)
    cases["root_granted_overrides_acl_deny"]=True
    response,_=asgi_call("GET",base_b+"/groups",token=token_b)
    assert response.status_code==403
    cases["root_ungranted_refused_even_acl_allow"]=True
    response,_=asgi_call("GET",base+"/groups",token=token_b)
    assert response.status_code==401
    response,_=asgi_call("GET","/api/v1/platform/users",token=token_a)
    assert response.status_code==401
    response,_=asgi_call("GET",base+"/groups",token=token_a,headers_extra={"x-tenant-id":tenant_b})
    assert response.status_code==400
    cases["root_token_no_context_promotion"]=True

    statements=[]
    def capture(execute,sql,params,many,ctx):
        statements.append(sql);return execute(sql,params,many,ctx)
    with connections["default"].execute_wrapper(capture):
        response,page=asgi_call("GET",base+"/groups?limit=2",token=token_a)
    assert response.status_code==200 and len(page["data"])==2 and "next" in page["links"]
    assert any("pixs_core_group" in sql and "ORDER BY" in sql and "LIMIT 3" in sql for sql in statements)
    references=[item["ref"] for item in page["data"]]
    response,last=asgi_call("GET",page["links"]["next"],token=token_a)
    assert response.status_code==200
    references.extend(item["ref"] for item in last["data"])
    assert set(references)=={group_ref,*root_groups} and group_b_ref not in references
    cases["root_sql_keyset_tenant_isolation"]=True

    scope_id="scope/a-é "
    h["grant"]("pixs.core.scope.node.create","pixs.core.scope:"+scope_id,context=context,effect=Effect.DENY)
    response,_=asgi_call("POST",base+"/commands/create-scope",
        {"scope_id":scope_id,"parent_scope_id":None},token=token_a,key="root-create-scope")
    assert response.status_code==200
    h["grant_auth"]("pixs.auth.session.logout","pixs.auth.session:"+session_a,context=context)
    response,_=asgi_call("POST",base+"/auth/logout",{},token=token_a,key="root-close-api-a")
    assert response.status_code==200
    response,csrf=asgi_call("GET","/api/v1/web/auth/csrf")
    assert response.status_code==200
    csrf_cookie=response.cookies["csrftoken"].value
    web_base="/api/v1/web/tenants/"+quote(tenant,safe="")
    response,web=asgi_call("POST",web_base+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},key="root-web-login",
        headers_extra={"origin":"https://api.example.test","x-csrftoken":csrf_cookie},cookies={"csrftoken":csrf_cookie})
    assert response.status_code==200 and WEB_COOKIE in response.cookies
    cookies={WEB_COOKIE:response.cookies[WEB_COOKIE].value,"csrftoken":response.cookies["csrftoken"].value}
    headers={"origin":"https://api.example.test","x-csrftoken":cookies["csrftoken"]}
    web_group=generate_uuid7();h["grant"]("pixs.core.groups.group.create","pixs.core.group:"+str(web_group),
                                      context=context,effect=Effect.DENY)
    response,_=asgi_call("POST",web_base+"/commands/create-group",{"group_id":str(web_group)},
                         key="root-web-group",headers_extra=headers,cookies=cookies)
    assert response.status_code==200 and CoreGroup.objects.get(pk=web_group).tenant_id==tenant
    response,_=asgi_call("GET",web_base+"/groups",cookies=cookies)
    assert response.status_code==200
    response,_=asgi_call("GET",base+"/groups",cookies=cookies)
    assert response.status_code==403
    cases["root_web_facade_same_exception"]=True
    for root in (base,web_base):
        for action in ("revoke-all","change-password"):
            response,_=asgi_call("POST",root+"/auth/"+action,{},
                token=token_b if root==base else None,headers_extra=headers,cookies=None if root==base else cookies)
            assert response.status_code==404
    cases["global_auth_routes_platform_only"]=True

    response,_=asgi_call("POST",web_base+"/auth/logout",{},key="root-web-close",headers_extra=headers,cookies=cookies)
    assert response.status_code==200
    scope_context=ScopeContext(ScopeType.TENANT,tenant,scope_id)
    h["contexts"].add(scope_context)
    scope_base=base+"/scopes/"+quote(scope_id,safe="")
    response,scope_login=asgi_call("POST",scope_base+"/auth/login",
        {"external_subject":f["supplied"].external_subject,"password":f["supplied"].password},key="root-scope-login")
    assert response.status_code==200
    token_s=scope_login["data"]["access_token"]
    cases["scope_create_and_login_real"]=True
    response,_=asgi_call("GET",base+"/groups",token=token_s)
    assert response.status_code==401
    response,_=asgi_call("GET",scope_base+"/groups",token=token_b)
    assert response.status_code==401
    cases["scope_token_no_parent_promotion"]=True
    scope_group=generate_uuid7()
    h["grant"]("pixs.core.groups.group.create","pixs.core.group:"+str(scope_group),
                context=scope_context,effect=Effect.DENY)
    response,_=asgi_call("POST",scope_base+"/commands/create-group",{"group_id":str(scope_group)},
                         token=token_s,key="root-scope-group")
    assert response.status_code==200
    response,scope_page=asgi_call("GET",scope_base+"/groups",token=token_s)
    assert response.status_code==200 and [item["ref"] for item in scope_page["data"]]==["pixs.core.group:"+str(scope_group)]
    assert scope_page["data"][0]["context"]["scope_id"]==scope_id
    cases["scope_group_and_query_real"]=True
    assert set(cases)==set(EXPECTED_CASES)
    return cases


def run_real_api_core_tenant(root_str):
    from auth_pg_test_support import run_in_auth_schema
    _DIAGNOSTICS.clear()
    outcome=run_in_auth_schema(root_str,scenarios,EXPECTED_CASES,with_core=True,core_target="0003_core_idempotence")
    outcome["http_diagnostics"]=_DIAGNOSTICS
    return outcome


if __name__=="__main__":
    import json
    from pathlib import Path
    outcome=run_real_api_core_tenant(str(Path(__file__).resolve().parents[2]))
    print(json.dumps(outcome,ensure_ascii=False,sort_keys=True))
    raise SystemExit(0 if outcome.get("real_pg") and outcome.get("cleanup") and outcome.get("conns_closed") else 1)
