"""Recettes C14 sur la frontière C11 réelle et PostgreSQL isolé.

RequestFactory exerce les gardes applicatives HTTPS/Host/Origin/CSRF ; aucun
TLS déployé ni exécutant réseau/DNS n'est qualifié. Les secrets restent locaux.
"""
from __future__ import annotations

_HTTP_DIAGNOSTICS = []

EXPECTED_CASES = (
    "real_login_and_owner_dispatch", "pzt_desired_persisted", "pzt_replay_once",
    "pzt_divergent_key_closed", "pzt_query_current", "pzt_applied_unknown",
    "dns_desired_persisted", "dns_query_current", "dns_applied_unknown", "dns_name_declared", "dns_policy_unverified",
    "dns_name_retired", "dns_profile_retired", "pzt_profile_retired",
    "missing_bearer_closed", "refresh_as_access_closed", "insecure_transport_closed",
    "foreign_host_closed", "foreign_origin_closed", "method_closed",
    "context_header_closed", "duplicate_query_closed", "foreign_query_closed",
    "client_authority_closed", "invalid_types_closed", "stale_revision_closed",
    "web_csrf_closed", "web_command_and_activity", "web_replay_no_activity",
    "background_query_no_activity", "cookie_bearer_mix_closed",
    "ordinary_waiver_not_authority", "fresh_policy_denial",
    "revoked_token_closed", "openapi_real_views_and_guards",
    "shell_context_real_c14_bindings", "shell_metadata_no_authority_or_activity",
    "shell_core_only_no_c14_binding", "shell_incoherent_bindings_closed",
    "web_displayed_session_mismatch_closed", "web_displayed_session_match_admitted",
    "web_displayed_session_absent_legacy", "bearer_displayed_session_header_ignored",
)


def scenarios():
    import datetime
    import re
    import copy
    import hashlib
    import json
    from dataclasses import replace
    from urllib.parse import urlencode
    from django.conf import settings
    from django.test import RequestFactory
    from auth_service_fixture import make_auth_service_fixture
    from test_pzt_dns_contracts import _pztcfg, _dnscfg
    from test_pzt_dns_http_inputs import wire
    from pixs.auth import models as auth_models
    from pixs.auth.api_request_source import ApiRequestSource
    from pixs.auth.contracts import AuthDataClassification, Facade, AuthOutcome
    from pixs.auth.facades import WEB_COOKIE
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.auth.shell_context import PostgresShellContextService
    from pixs.backend.api_core_catalog import ApiInputLimits
    from pixs.backend.api_core_composition import CoreHttpLimits
    from pixs.backend.api_core_views import ModuleHttpComposition
    from pixs.backend.api_pzt_dns_boundary import build_c14_api_urls, build_c14_module_bindings
    from pixs.backend.api_shell_context import build_shell_context_urls
    from pixs.backend.api_pzt_dns_catalog import C14_HTTP_BINDINGS
    from pixs.backend.api_pzt_dns_dispatch import C14ApiComposition
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.policy import Effect, Policy, Selector, ScopeSelector, Obligation
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy, decode_policy
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.query_source import CoreFactSource
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.dns.models import DesiredDnsRecord, DnsNameRecord
    from pixs.dns.services import DnsManagementPolicy
    from pixs.pzt.models import DesiredPztRecord, PztIdempotenceRecord
    from pixs.pzt.services import PztManagementPolicy
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

    settings.ALLOWED_HOSTS = ["c14.example.test"]
    settings.SECRET_KEY = "Vecteur public de recette C14, sans secret de déploiement"
    settings.CSRF_TRUSTED_ORIGINS = ["https://c14.example.test"]
    f = make_auth_service_fixture()
    offset = [0]
    f["clock"].now = lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=offset[0])
    login = f["login"]("c14-real-api")
    web_login = f["service"]().login(
        f["grant"](f["command"]("pixs.auth.session.create", f["actor"], "c14-real-web")),
        replace(f["supplied"], facade=Facade.WEB))
    login_b = f["service"]().login(
        f["grant"](f["command"]("pixs.auth.session.create", f["actor"], "c14-other-web-tab")),
        replace(f["supplied"], facade=Facade.WEB))
    assert login_b.outcome is AuthOutcome.ISSUED and login_b.emission.cookie is not None
    assert login.outcome is AuthOutcome.ISSUED and web_login.outcome is AuthOutcome.ISSUED
    token = login.emission.access
    web_token = web_login.emission.cookie
    assert token is not None and web_token is not None
    context = f["context"]
    pzt_ref, dns_ref = "pixs.pzt.http:profile", "pixs.dns.http:profile"
    web_ref = "pixs.pzt.http:web"
    waiver_ref = "pixs.pzt.http:ordinary-waiver"
    resources = {pzt_ref, dns_ref, web_ref, waiver_ref}
    actions = {b.name for b in C14_HTTP_BINDINGS}
    policy_ids = {}

    def grant(owner, names, targets):
        pid = "c14-http-" + hashlib.sha256(json.dumps([owner, names, targets]).encode()).hexdigest()[:24]
        policy = Policy(pid, "1.0.0", owner, Effect.ALLOW,
            Selector("subject", (f["actor"],)), Selector("resource", tuple(targets)),
            Selector("action", tuple(names)), ScopeSelector((context,)),
            obligations=(Obligation("AUDIT"),))
        CorePolicy.objects.create(policy_id=pid, policy_version=policy.policy_version,
            owner=owner, effect=policy.effect.value, definition=encode_policy(policy))
        return pid

    for owner, targets in (("pixs.pzt", (pzt_ref, web_ref, waiver_ref)), ("pixs.dns", (dns_ref,))):
        names = tuple(b.name for b in C14_HTTP_BINDINGS if b.owner == owner)
        policy_ids[owner] = grant(owner, names, targets)
    session_ref = "pixs.auth.session:" + str(web_login.session.session_id)
    grant("pixs.auth", ("pixs.auth.session.activity", "pixs.auth.session.context.read"), (session_ref,))

    def make_store(request=None):
        subjects = {f["actor"]}
        declared_resources, declared_actions, scopes = set(resources), set(actions), {context}
        if request is not None:
            declared_resources.add(request.resource_id)
            declared_actions.add(request.action_id)
            scopes.add(request.context)
        for definition in CorePolicy.objects.values_list("definition", flat=True):
            p = decode_policy(definition)
            subjects.update(p.subject.values)
            declared_resources.update(p.resource.values)
            declared_actions.update(p.action.values)
            scopes.update(p.scope.contexts)
        declared_resources.update("pixs.auth.session:" + str(pk)
            for pk in auth_models.AuthSession.objects.values_list("pk", flat=True))
        return CoreAuthorizationStore(alias="default", installation_ref="c14-http-install",
            base_epoch="c14-http-v1",
            catalog=Catalog(tuple(sorted(subjects)), tuple(sorted(declared_resources)),
                tuple(sorted(declared_actions)),
                tuple(sorted(scopes, key=lambda c: (c.scope_type.value, c.tenant_id or "", c.scope_id or ""))), ()),
            limits=Limits(512, 512, 16, 100, 100, 512, 512, 512, 10000000, 60, 3600))

    def auth_decider(*, request, operation_id, authentication_source):
        store = make_store(request)
        provider = RuntimeTrustedFactsProvider(store=store, authentication_source=authentication_source,
            request=request, operation_id=operation_id,
            additional_owners=(RuntimeResourceOwner("pixs.auth.", authentication_source.ownership),))
        return RuntimeAuthorizationDecider(store=store, facts_provider=provider,
            clock=f["clock"], request=request, operation_id=operation_id)

    class Classification:
        def resolve(self, **kwargs):
            return AuthDataClassification("c14-http-auth", ConfidentialityLevel.CONFIDENTIAL,
                                          PersonalDataLevel.PERSONAL)

    audit_policy = AuditPolicy("c14-http-audit", "1.0.0", "fixture-explicite", 1,
        65536, 100, (), "c14-http-audit", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
    audit = PostgresAuditParticipant(ExplicitAuditPolicySource(context, audit_policy), f["clock"], "peer")
    auth_service = PostgresLocalAuthService(alias="default", peer_alias="peer",
        profile_id=f["profile"].profile_id, trust_source=f["trust"], assurance_source=f["assurance"],
        facts_reader=CoreFactSource(), clock=f["clock"], audit=audit,
        classification_source=Classification(), decider_factory=auth_decider)
    source = ApiRequestSource(alias="default", profile_id=f["profile"].profile_id,
        trust_source=f["trust"], assurance_source=f["assurance"], facts_reader=CoreFactSource(),
        clock=f["clock"], max_identifier_chars=4096)

    class PztPolicy:
        def resolve(self, *, context, alias, operation_id):
            assert context == f["context"] and alias == "default"
            return PztManagementPolicy(datetime.timedelta(minutes=10), _pztcfg(1).governance)

    class DnsPolicy:
        def resolve(self, *, context, alias, operation_id):
            assert context == f["context"] and alias == "default"
            return DnsManagementPolicy(datetime.timedelta(minutes=10), _dnscfg(1).governance)

    composition = C14ApiComposition("default", "peer", source, auth_service, make_store(),
        audit, f["clock"], PztPolicy(), DnsPolicy(), frozenset({"declare_desired_pzt"}))
    transport = ModuleHttpComposition(source, "c14.example.test", "https://c14.example.test",
        CoreHttpLimits(65536, 8192, 2, 10), ApiInputLimits(4096, 128, 32768, 128))
    shell_service = PostgresShellContextService(auth_service=auth_service, request_source=source)
    module_bindings = build_c14_module_bindings()
    urls = build_c14_api_urls(composition, transport) + build_shell_context_urls(
        shell_service, transport, module_bindings=module_bindings)
    rf = RequestFactory()

    def call(method, path, body=None, *, access=token, headers=None, cookies=None, secure=True, routes=None):
        extra = {"HTTP_HOST": "c14.example.test"}
        if access is not None:
            extra["HTTP_AUTHORIZATION"] = "Bearer " + access.value
        if headers:
            extra.update(headers)
        req = rf.generic(method, path, data=json.dumps(body).encode() if body is not None else b"",
            content_type="application/json", secure=secure, **extra)
        req.META["RAW_URI"] = path
        if cookies:
            req.COOKIES.update(cookies)
        for pattern in (urls if routes is None else routes):
            match = pattern.resolve(path.split("?", 1)[0].lstrip("/"))
            if match is not None:
                response = match.func(req, **match.kwargs)
                data = json.loads(response.content) if response.content else None
                return response, data
        raise AssertionError("C14_ROUTE_UNRESOLVED")

    base = "/api/v1/platform/"
    def query(module, operation, **parameters):
        return base + module + "/queries/" + operation + "?" + urlencode(parameters)
    def command(module, name):
        return base + module + "/commands/" + name
    def key(value):
        return {"HTTP_IDEMPOTENCY_KEY": value}
    def declaration(owner, target):
        return {"schema_version": "1.0.0", "resource_id": target, "expected_revision": 0,
            "configuration": wire(_pztcfg(1) if owner == "pzt" else _dnscfg(1))}
    def expect(response, status, suffix=None):
        r, data = response
        code = data.get("error_code") if type(data) is dict else None
        safe_code = code if type(code) is str and re.fullmatch(r"pixs\.(?:core|pzt|dns)\.api\.v1\.[A-Z][A-Z0-9_]*", code) else None
        _HTTP_DIAGNOSTICS.append({"index":len(_HTTP_DIAGNOSTICS),"status":r.status_code,"expected":status,"code":safe_code})
        assert r.status_code == status
        if suffix is not None:
            assert data["error_code"].endswith("." + suffix)
        assert r["Cache-Control"] == "no-store" and r["X-Content-Type-Options"] == "nosniff"
        return data

    cases = {}
    pzt_body = declaration("pzt", pzt_ref)
    first = expect(call("POST", command("pzt", "declare_desired_pzt"), pzt_body, headers=key("c14-pzt-first")), 200)
    cases["real_login_and_owner_dispatch"] = first["data"]["outcome"] == "SUCCEEDED"
    cases["pzt_desired_persisted"] = DesiredPztRecord.objects.get(resource_id=pzt_ref).config_revision == 1
    audits, idem = CoreAuditEvent.objects.count(), PztIdempotenceRecord.objects.count()
    replay = expect(call("POST", command("pzt", "declare_desired_pzt"), pzt_body, headers=key("c14-pzt-first")), 200)
    cases["pzt_replay_once"] = replay["data"] == first["data"] and CoreAuditEvent.objects.count() == audits and PztIdempotenceRecord.objects.count() == idem
    divergent = copy.deepcopy(pzt_body)
    divergent["configuration"]["plan_ref"] = "autre-plan-de-recette"
    expect(call("POST", command("pzt", "declare_desired_pzt"), divergent, headers=key("c14-pzt-first")), 409, "IDEMPOTENCE_CONFLICT")
    cases["pzt_divergent_key_closed"] = DesiredPztRecord.objects.get(resource_id=pzt_ref).config_revision == 1
    desired = expect(call("GET", query("pzt", "get_desired_pzt", resource_id=pzt_ref)), 200)
    cases["pzt_query_current"] = desired["data"]["configuration"] == pzt_body["configuration"]
    applied = expect(call("GET", query("pzt", "get_applied_pzt", resource_id=pzt_ref)), 200)["data"]
    cases["pzt_applied_unknown"] = applied["application_status"] == "UNKNOWN" and applied["measurement_status"] == "UNMEASURED" and applied["applied_revision"] is None and applied["measurements"] is None

    expect(call("POST", command("dns", "declare_desired_dns"), declaration("dns", dns_ref), headers=key("c14-dns")), 200)
    cases["dns_desired_persisted"] = DesiredDnsRecord.objects.get(resource_id=dns_ref).config_revision == 1
    dns_desired = expect(call("GET", query("dns", "get_desired_dns", resource_id=dns_ref)), 200)["data"]
    cases["dns_query_current"] = dns_desired["configuration"] == declaration("dns", dns_ref)["configuration"]
    dns_applied = expect(call("GET", query("dns", "get_applied_dns", resource_id=dns_ref)), 200)["data"]
    cases["dns_applied_unknown"] = dns_applied["application_status"] == "UNKNOWN" and dns_applied["measurement_status"] == "UNMEASURED" and dns_applied["applied_revision"] is None
    name = {"schema_version": "1.0.0", "resource_id": dns_ref, "expected_revision": 1,
        "name": "service.pzt.test.internal", "view": "vue-test", "target_ref": "cible-opaque"}
    expect(call("POST", command("dns", "declare_name"), name, headers=key("c14-dns-name")), 200)
    cases["dns_name_declared"] = DnsNameRecord.objects.filter(zone__resource_id=dns_ref).count() == 1
    policy = expect(call("GET", query("dns", "resolve_view_policy", resource_id=dns_ref,
        view="vue-test", name=name["name"])), 200)["data"]
    cases["dns_policy_unverified"] = policy["target_verification"] == "UNVERIFIED" and policy["application_status"] == "UNKNOWN" and policy["applied_present"] is None
    retirement = {k: v for k, v in name.items() if k != "target_ref"}
    retirement["expected_revision"] = 2
    expect(call("POST", command("dns", "retire_name"), retirement, headers=key("c14-dns-retire-name")), 200)
    cases["dns_name_retired"] = DnsNameRecord.objects.get(zone__resource_id=dns_ref).business_state == "RETIRED"
    for module, target, revision, label in (("dns", dns_ref, 3, "dns_profile_retired"), ("pzt", pzt_ref, 1, "pzt_profile_retired")):
        expect(call("POST", command(module, "retire_desired_" + module),
            {"schema_version": "1.0.0", "resource_id": target, "expected_revision": revision, "reason": "retrait de recette"},
            headers=key("c14-retire-" + module)), 200)
        model = DesiredPztRecord if module == "pzt" else DesiredDnsRecord
        cases[label] = model.objects.get(resource_id=target).business_state == "RETIRED"

    qp = query("pzt", "get_desired_pzt", resource_id=pzt_ref)
    for label, result, status, suffix in (
        ("missing_bearer_closed", call("GET", qp, access=None), 401, "AUTH_REQUIRED"),
        ("refresh_as_access_closed", call("GET", qp, access=login.emission.refresh), 401, "AUTH_REQUIRED"),
        ("insecure_transport_closed", call("GET", qp, secure=False), 403, "TRANSPORT_REQUIRED"),
        ("foreign_host_closed", call("GET", qp, headers={"HTTP_HOST": "foreign.example.test"}), 403, "TRANSPORT_REQUIRED"),
        ("foreign_origin_closed", call("GET", qp, headers={"HTTP_ORIGIN": "https://foreign.example.test"}), 403, "ACCESS_DENIED"),
        ("method_closed", call("POST", qp, {}, headers=key("wrong-method")), 405, "METHOD_NOT_ALLOWED"),
        ("context_header_closed", call("GET", qp, headers={"HTTP_X_TENANT_ID": "foreign"}), 400, "CONTEXT_MISMATCH"),
        ("duplicate_query_closed", call("GET", qp + "&resource_id=duplicate"), 400, "INPUT_INVALID"),
        ("foreign_query_closed", call("GET", qp + "&subject_id=foreign"), 400, "INPUT_INVALID"),
    ):
        expect(result, status, suffix)
        cases[label] = True
    for label, changes, status, suffix in (
        ("client_authority_closed", {"metadata": {"subject_id": f["actor"]}}, 400, "INPUT_INVALID"),
        ("invalid_types_closed", {"expected_revision": True}, 400, "INPUT_INVALID"),
        ("stale_revision_closed", {}, 409, "REVISION_CONFLICT"),
    ):
        expect(call("POST", command("pzt", "declare_desired_pzt"),
            dict(pzt_body, **changes), headers=key("c14-negative-" + label)), status, suffix)
        cases[label] = DesiredPztRecord.objects.get(resource_id=pzt_ref).config_revision == 2

    ordinary = declaration("pzt", waiver_ref)
    ordinary["authorization_intent"] = {"waive_audit": True, "waive_governance": True}
    before_waiver_audits = CoreAuditEvent.objects.count()
    ordinary_result = expect(call("POST", command("pzt", "declare_desired_pzt"),
        ordinary, headers=key("c14-ordinary-waiver")), 200)
    cases["ordinary_waiver_not_authority"] = (
        ordinary_result["data"]["audit_disposition"] == "AUDITED"
        and CoreAuditEvent.objects.count() == before_waiver_audits + 1
        and DesiredPztRecord.objects.get(resource_id=waiver_ref).config_revision == 1)

    web_path = "/api/v1/web/platform/pzt/commands/declare_desired_pzt"
    web_body = declaration("pzt", web_ref)
    csrf = "a" * 32
    cookies = {WEB_COOKIE: web_token.value, "csrftoken": csrf}
    wh = dict(key("c14-web-first"), HTTP_ORIGIN="https://c14.example.test", HTTP_X_CSRFTOKEN=csrf)
    expect(call("POST", web_path, web_body, access=None, cookies={WEB_COOKIE: web_token.value},
        headers=dict(key("c14-web-no-csrf"), HTTP_ORIGIN="https://c14.example.test")), 403, "CSRF_REQUIRED")
    cases["web_csrf_closed"] = not DesiredPztRecord.objects.filter(resource_id=web_ref).exists()
    offset[0] = 2
    web_result = expect(call("POST", web_path, web_body, access=None, cookies=cookies, headers=wh), 200)
    cases["web_command_and_activity"] = web_result["meta"]["activity"]["status"] == "RECORDED"
    session = auth_models.AuthSession.objects.get(pk=web_login.session.session_id)
    last_activity = session.last_activity_at
    offset[0] = 4
    replay = expect(call("POST", web_path, web_body, access=None, cookies=cookies, headers=wh), 200)
    session.refresh_from_db()
    cases["web_replay_no_activity"] = replay["meta"]["activity"]["status"] == "REPLAY_IGNORED" and session.last_activity_at == last_activity
    expect(call("GET", qp.replace("/api/v1/", "/api/v1/web/"), access=None, cookies=cookies), 200)
    session.refresh_from_db()
    cases["background_query_no_activity"] = session.last_activity_at == last_activity
    expect(call("GET", qp, cookies=cookies), 403, "ACCESS_DENIED")
    cases["cookie_bearer_mix_closed"] = True

    # Vrai producteur C03 et façade C11, injectés par le caller d'assemblage.
    # Aucun résolveur du client n'est traité comme une permission.
    before_shell_audits = CoreAuditEvent.objects.count()
    shell_path = "/api/v1/web/platform/shell/context"
    shell = expect(call("GET", shell_path, access=None, cookies=cookies), 200)
    resolver = shell["meta"]["transport_resolver"]
    owner_operations = [operation for operation in resolver["operations"]
                        if operation["owner"] in ("pixs.pzt", "pixs.dns")]
    expected_operations = [{
        "kind": binding.kind, "name": binding.name, "owner": binding.owner,
        "contractVersion": binding.contract_version, "scopes": list(binding.scopes),
        "segments": list(binding.segments),
    } for binding in module_bindings]
    cases["shell_context_real_c14_bindings"] = (
        resolver["version"] == "1.0.0" and len(resolver["operations"]) == 48
        and owner_operations == expected_operations
        and len(owner_operations) == 11
        and shell["data"]["identity_ref"] == f["actor"]
        and shell["data"]["session_id"] == str(web_login.session.session_id))
    session.refresh_from_db()
    cases["shell_metadata_no_authority_or_activity"] = (
        "transport_resolver" not in shell["data"]
        and shell["data"]["ui_permissions"] == {"status": "UNAVAILABLE", "items": []}
        and CoreAuditEvent.objects.count() == before_shell_audits + 1
        and session.last_activity_at == last_activity)
    core_routes = build_shell_context_urls(shell_service, transport)
    core_shell = expect(call("GET", shell_path, access=None, cookies=cookies, routes=core_routes), 200)
    cases["shell_core_only_no_c14_binding"] = (
        len(core_shell["meta"]["transport_resolver"]["operations"]) == 37
        and all(operation["owner"] == "pixs.core"
                for operation in core_shell["meta"]["transport_resolver"]["operations"])
        and core_shell["data"] == shell["data"])
    rejected = 0
    for invalid_bindings in (list(module_bindings), module_bindings + (module_bindings[0],)):
        try:
            build_shell_context_urls(shell_service, transport, module_bindings=invalid_bindings)
        except ValueError:
            rejected += 1
    cases["shell_incoherent_bindings_closed"] = rejected == 2

    # Changement de cookie dans un autre onglet : l'indication affichée
    # ne devient jamais une autorité ni un remplacement de la session C03.
    cookie_b = {WEB_COOKIE: login_b.emission.cookie.value, "csrftoken": csrf}
    shown_a = str(web_login.session.session_id)
    shown_b = str(login_b.session.session_id)
    assert shown_a != shown_b
    revisions_before = list(DesiredPztRecord.objects.order_by("resource_id").values_list("resource_id", "config_revision"))
    audits_before = CoreAuditEvent.objects.count()
    idempotence_before = PztIdempotenceRecord.objects.count()
    mismatch_headers = dict(key("c14-other-tab-mismatch"),
        HTTP_ORIGIN="https://c14.example.test", HTTP_X_CSRFTOKEN=csrf,
        HTTP_X_SHELL_SESSION_ID=shown_a)
    expect(call("POST", web_path, web_body, access=None,
        cookies=cookie_b, headers=mismatch_headers), 400, "CONTEXT_MISMATCH")
    cases["web_displayed_session_mismatch_closed"] = (
        list(DesiredPztRecord.objects.order_by("resource_id").values_list("resource_id", "config_revision")) == revisions_before
        and CoreAuditEvent.objects.count() == audits_before
        and PztIdempotenceRecord.objects.count() == idempotence_before)
    web_qp = qp.replace("/api/v1/", "/api/v1/web/")
    matched = expect(call("GET", web_qp, access=None, cookies=cookie_b,
        headers={"HTTP_X_SHELL_SESSION_ID": shown_b}), 200)
    cases["web_displayed_session_match_admitted"] = matched["data"]["resource_id"] == pzt_ref
    legacy = expect(call("GET", web_qp, access=None, cookies=cookie_b), 200)
    cases["web_displayed_session_absent_legacy"] = legacy["data"] == matched["data"]
    bearer = expect(call("GET", qp,
        headers={"HTTP_X_SHELL_SESSION_ID": shown_a}), 200)
    cases["bearer_displayed_session_header_ignored"] = bearer["data"] == matched["data"]

    docs_ok = True
    for owner, count in (("pzt", 24), ("dns", 42)):
        path = "/api/v1/openapi/" + owner + "-management.json"
        index = expect(call("GET", path, access=None), 200)
        found = {}
        for entry in index["x-documents"]:
            response, fragment = call("GET", entry["href"], access=None)
            expect((response, fragment), 200)
            docs_ok = docs_ok and len(response.content) == entry["bytes"]
            docs_ok = docs_ok and hashlib.sha256(response.content).hexdigest() == entry["sha256"]
            docs_ok = docs_ok and not (set(found) & set(fragment["paths"]))
            found.update(fragment["paths"])
        docs_ok = docs_ok and len(found) == count
        response, empty = call("HEAD", path, access=None)
        docs_ok = docs_ok and response.status_code == 200 and empty is None
        expect(call("GET", path, access=None, secure=False), 403, "TRANSPORT_REQUIRED")
    cases["openapi_real_views_and_guards"] = docs_ok

    CorePolicy.objects.filter(policy_id=policy_ids["pixs.pzt"]).delete()
    expect(call("GET", qp), 403, "ACCESS_DENIED")
    cases["fresh_policy_denial"] = True
    auth_models.AuthToken.objects.filter(session_id=login.session.session_id, kind="ACCESS").update(state="REVOKED")
    revoked_response = call("GET", qp)
    # Le service propriétaire normalise aussi les faits Auth illisibles en 503.
    # Le critère de révocation est le refus sans donnée, pas un 401 inventé.
    assert revoked_response[0].status_code in (401, 503)
    revoked = expect(revoked_response, revoked_response[0].status_code)
    cases["revoked_token_closed"] = (
        "data" not in revoked and revoked["error_code"] in (
            "pixs.pzt.api.v1.AUTH_REQUIRED", "pixs.pzt.api.v1.SERVICE_UNAVAILABLE",
            "pixs.pzt.api.v1.AUDIT_UNAVAILABLE"))
    return cases


def run(root_str):
    from c14_pg_test_support import run_in_c14_schema
    result = run_in_c14_schema(root_str, scenarios, EXPECTED_CASES)
    result["http_diagnostics"] = list(_HTTP_DIAGNOSTICS[-10:])
    result["application_http_guards"] = result["real_pg"]
    result["deployed_tls_qualified"] = False
    result["network_executor_qualified"] = False
    return result
