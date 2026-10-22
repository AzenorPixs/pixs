"""Raccordement C06/Auth : propriétaire C03/C04/C05 réels, secrets limités au processus PG."""
from __future__ import annotations

EXPECTED_CASES = (
    "bridge_login_actor_from_binding_admin",
    "bridge_auth_operation_stable_server",
    "bridge_real_admin_login",
    "bridge_access_revalidated_by_c03",
    "bridge_real_clock_preserves_authentication_time",
    "bridge_future_activity_refused",
    "bridge_structural_hint_cannot_forge_actor",
    "bridge_refresh_only_renewal",
    "bridge_web_cookie_bound_to_real_session",
    "bridge_revoked_hint_does_not_authenticate",
)


def scenarios():
    from dataclasses import replace
    from auth_service_fixture import make_auth_service_fixture
    from pixs.auth.api_request_source import ApiRequestSource, ApiRequestSourceError
    from pixs.auth.contracts import AuthOutcome, Facade
    from pixs.auth.identifiers import identity_reference, new_uuid7
    from pixs.auth.policy import SessionCategory
    from pixs.auth.tokens import TokenKind
    from pixs.core.authz.ports import RevocationStatus
    from pixs.core.ports import CorePortError
    from pixs.core.query_source import CoreFactSource

    f = make_auth_service_fixture()
    import datetime
    f["clock"].now = lambda: datetime.datetime.now(datetime.timezone.utc)
    source = ApiRequestSource(
        alias="default", profile_id=f["profile"].profile_id,
        trust_source=f["trust"], assurance_source=f["assurance"],
        facts_reader=CoreFactSource(), clock=f["clock"], max_identifier_chars=4096)
    ctx = f["context"]
    login_hint = source.resolve_login(context=ctx, external_subject=f["supplied"].external_subject, facade=Facade.API)
    assert login_hint.identity_ref == f["actor"]
    assert login_hint.session_id is None and login_hint.category is SessionCategory.ADMIN
    cases = {"bridge_login_actor_from_binding_admin": True}

    def auth_command(hint, action, resource, key, suffix):
        return source.auth_command(
            actor=hint, resource_id=resource, action_id=action,
            correlation_id="correlation-" + suffix, decision_id="decision-" + suffix,
            idempotency_key=key)
    first = auth_command(login_hint, "pixs.auth.session.create", login_hint.identity_ref, "bridge-login-key", "first")
    retry = auth_command(login_hint, "pixs.auth.session.create", login_hint.identity_ref, "bridge-login-key", "retry")
    different = auth_command(login_hint, "pixs.auth.session.create", login_hint.identity_ref, "bridge-other-key", "other")
    assert first.operation_id == retry.operation_id and first.operation_id != different.operation_id
    assert first.request.correlation_id != retry.request.correlation_id
    cases["bridge_auth_operation_stable_server"] = True

    supplied = replace(f["supplied"], category=SessionCategory.ADMIN, facade=Facade.API)
    f["grant"](first)
    api = f["service"]().login(first, supplied)
    assert api.outcome is AuthOutcome.ISSUED and api.session.category is SessionCategory.ADMIN
    assert api.emission.access is not None and api.emission.refresh is not None
    cases["bridge_real_admin_login"] = True

    hint = source.resolve_token(context=ctx, token=api.emission.access, kind=TokenKind.ACCESS)
    assert hint.identity_ref == f["actor"] and hint.session_id == api.session.session_id
    req = source.request(actor=hint, resource_id=hint.identity_ref, action_id="pixs.core.identity.read",
                         correlation_id="core-read-correlation", decision_id="core-read-decision")
    with source.open_core_source(request=req, operation_id="bridge-core-read",
                                 token=api.emission.access, kind=TokenKind.ACCESS) as invocation:
        auth, revocation = invocation.revalidate(req, alias="default", operation_id="bridge-core-read")
        assert auth.digital_identity_id == hint.identity_ref and revocation is RevocationStatus.ACTIVE
        assert hint.credential_id is not None and str(hint.credential_id) == auth.credential_id
    cases["bridge_access_revalidated_by_c03"] = True
    from pixs.auth.models import AuthSession
    stored = AuthSession.objects.get(pk=hint.session_id)
    assert stored.authenticated_at < stored.created_at <= stored.last_activity_at
    assert auth.authentication_time == stored.authenticated_at
    cases["bridge_real_clock_preserves_authentication_time"] = True
    original_activity = stored.last_activity_at
    AuthSession.objects.filter(pk=stored.pk).update(last_activity_at=f["clock"].now()+datetime.timedelta(seconds=10))
    try:
        try:
            with source.open_core_source(request=req, operation_id="bridge-future-activity",
                                         token=api.emission.access, kind=TokenKind.ACCESS) as invocation:
                invocation.revalidate(req, alias="default", operation_id="bridge-future-activity")
        except CorePortError:
            pass
        else:
            raise AssertionError("ACTIVITE_FUTURE_ACCEPTEE")
    finally:
        AuthSession.objects.filter(pk=stored.pk).update(last_activity_at=original_activity)
    cases["bridge_future_activity_refused"] = True

    forged = replace(hint, identity_ref=identity_reference(new_uuid7()))
    fake_request = source.request(actor=forged, resource_id=forged.identity_ref,
                                  action_id="pixs.core.identity.read",
                                  correlation_id="forged-correlation", decision_id="forged-decision")
    try:
        source.open_core_source(request=fake_request, operation_id="bridge-forged",
                                token=api.emission.access, kind=TokenKind.ACCESS)
    except ApiRequestSourceError:
        pass
    else:
        raise AssertionError("ACTEUR_FORGE_ACCEPTE")
    cases["bridge_structural_hint_cannot_forge_actor"] = True

    refresh_hint = source.resolve_token(context=ctx, token=api.emission.refresh, kind=TokenKind.REFRESH)
    try:
        source.open_core_source(request=req, operation_id="bridge-forbidden-refresh",
                                token=api.emission.refresh, kind=TokenKind.REFRESH)
    except ApiRequestSourceError:
        pass
    else:
        raise AssertionError("REFRESH_ORDINAIRE_ACCEPTE")
    renew = auth_command(refresh_hint, "pixs.auth.session.renew",
                         "pixs.auth.session:" + str(refresh_hint.session_id), "bridge-renew-key", "renew")
    f["grant"](renew)
    renewed = f["service"]().renew(renew, api.emission.refresh)
    assert renewed.outcome is AuthOutcome.ISSUED and renewed.session.session_id == api.session.session_id
    assert renewed.emission.access is not None and renewed.emission.refresh is not None
    cases["bridge_refresh_only_renewal"] = True

    web_hint = source.resolve_login(context=ctx, external_subject=f["supplied"].external_subject, facade=Facade.WEB)
    web_command = auth_command(web_hint, "pixs.auth.session.create",
                               web_hint.identity_ref, "bridge-web-key", "web")
    f["grant"](web_command)
    web = f["service"]().login(web_command, replace(supplied, facade=Facade.WEB))
    assert web.outcome is AuthOutcome.ISSUED and web.emission.cookie is not None
    cookie_hint = source.resolve_token(context=ctx, token=web.emission.cookie, kind=TokenKind.WEB_SESSION)
    assert cookie_hint.facade is Facade.WEB and cookie_hint.session_id == web.session.session_id
    web_req = source.request(actor=cookie_hint, resource_id=cookie_hint.identity_ref,
                             action_id="pixs.core.identity.read", correlation_id="web-read", decision_id="web-read")
    with source.open_core_source(request=web_req, operation_id="bridge-web-read",
                                 token=web.emission.cookie, kind=TokenKind.WEB_SESSION) as invocation:
        actual, status = invocation.revalidate(web_req, alias="default", operation_id="bridge-web-read")
        assert actual.digital_identity_id == f["actor"] and status is RevocationStatus.ACTIVE
    cases["bridge_web_cookie_bound_to_real_session"] = True

    current = source.resolve_token(context=ctx, token=renewed.emission.access, kind=TokenKind.ACCESS)
    withdraw = auth_command(current, "pixs.auth.session.logout",
                            "pixs.auth.session:" + str(current.session_id), "bridge-logout-key", "logout")
    f["grant"](withdraw)
    result = f["service"]().logout(withdraw, renewed.emission.access)
    assert result.outcome in (AuthOutcome.WITHDRAWN, AuthOutcome.WITHDRAWN_AUDIT_PENDING)
    # Une orientation structurale peut encore décrire la ligne ; elle ne donne
    # aucun droit sur le justificatif retiré, qui doit échouer à la revalidation.
    stale = source.resolve_token(context=ctx, token=renewed.emission.access, kind=TokenKind.ACCESS)
    stale_req = source.request(actor=stale, resource_id=stale.identity_ref,
                               action_id="pixs.core.identity.read", correlation_id="stale", decision_id="stale")
    try:
        with source.open_core_source(request=stale_req, operation_id="bridge-stale",
                                     token=renewed.emission.access, kind=TokenKind.ACCESS) as invocation:
            invocation.revalidate(stale_req, alias="default", operation_id="bridge-stale")
    except CorePortError:
        pass
    else:
        raise AssertionError("JUSTIFICATIF_RETIRE_ACCEPTE")
    cases["bridge_revoked_hint_does_not_authenticate"] = True
    assert set(cases) == set(EXPECTED_CASES) and all(cases.values())
    return cases


def run_real_api_core_auth(root_str):
    from auth_pg_test_support import run_in_auth_schema
    return run_in_auth_schema(root_str, scenarios, EXPECTED_CASES,
                              with_core=True, core_target="0003_core_idempotence")




def run_dependency_regressions(root_str):
    """Régressions finales isolées : neuf processus, aucun secret transmis au parent."""
    import json
    import subprocess
    import sys
    from pathlib import Path
    if str(Path(root_str).resolve()) != "/home/devops/datas/pixs":
        raise ValueError("RACINE_RECETTE_INVALIDE")
    modules=(
        ("test_auth_verifier_postgres","run"),
        ("test_auth_login_postgres","run"),
        ("test_auth_facades_postgres","run"),
        ("test_auth_activity_postgres","run"),
        ("test_runtime_authorization_declarations","run_real_runtime_declarations"),
        ("test_api_core_idempotence_postgres","run_real_api_core_idempotence"),
        ("test_api_core_auth_postgres","run_real_api_core_auth"),
        ("test_api_core_platform_postgres","run_real_api_core_platform"),
        ("test_api_core_tenant_postgres","run_real_api_core_tenant"),
    )
    results={}
    for module,function in modules:
        arguments=repr(root_str)
        if module=="test_api_core_idempotence_postgres":
            arguments+=", 'c02_'+__import__('uuid').uuid4().hex[:16], with_participant=True"
        script=("import json,sys\nfrom "+module+" import "+function+"\n"
                "result="+function+"("+arguments+")\n"
                "print(json.dumps(result,ensure_ascii=False,sort_keys=True))\n"
                "sys.exit(0 if result.get('real_pg') and result.get('cleanup') and result.get('conns_closed') else 1)\n")
        try:
            process=subprocess.run([sys.executable,"-B","-c",script],cwd=root_str,
                capture_output=True,text=True,timeout=90,check=False)
            try:
                result=json.loads(process.stdout)
                if type(result) is not dict:
                    raise ValueError("BILAN_RECETTE_INVALIDE")
            except (ValueError,TypeError):
                result={"real_pg":False,"cleanup":False,"conns_closed":False,"code":"BILAN_ENFANT_NON_PROUVE"}
            import hashlib
            result["captured_output_sha256"]=hashlib.sha256(process.stdout.encode("utf-8")).hexdigest()
            if result.get("real_pg") is True:
                result.pop("http_diagnostics",None)
            result["process_exit"]=process.returncode
        except subprocess.TimeoutExpired:
            result={"real_pg":False,"cleanup":False,"conns_closed":False,"code":"DELAI_ENFANT_DEPASSE","process_exit":None}
        results[module]=result
    good=all(r.get("real_pg") is True and r.get("cleanup") is True and r.get("conns_closed") is True
             and r.get("process_exit")==0 for r in results.values())
    return {"real_pg":good,"cleanup":all(r.get("cleanup") is True for r in results.values()),
            "conns_closed":all(r.get("conns_closed") is True for r in results.values()),
            "code":"NONE" if good else "REGRESSION_DEPENDANCE_NON_PROUVEE","dependencies":results,
            "case_count":sum(len(r.get("cases",{})) for r in results.values())}


if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    if sys.argv[1:] not in ([], ["--dependencies"]):
        raise SystemExit(2)
    root=str(Path(__file__).resolve().parents[2])
    outcome = run_dependency_regressions(root) if sys.argv[1:] else run_real_api_core_auth(root)
    print(json.dumps(outcome,ensure_ascii=False,sort_keys=True))
    raise SystemExit(0 if outcome.get("real_pg") and outcome.get("cleanup") and outcome.get("conns_closed") else 1)
