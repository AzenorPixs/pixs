"""Fixture COMPOSED browser C14 : construction C03/C04/C05/C14 en mémoire.

Réutilise strictement les constructions 43 HTTP et C06 sans les modifier.
Aucune sortie secret, aucun setting configuré ici, aucun serveur démarré ici.
Appel uniquement dans run_in_c14_schema après migrations en schéma jetable.
"""
from __future__ import annotations

from urllib.parse import urlsplit


def _assert_loopback(origin, host):
    if type(origin) is not str or type(host) is not str:
        raise ValueError("ORIGIN_HOST_TYPE")
    parts = urlsplit(origin)
    if parts.scheme != "https":
        raise ValueError("SCHEME_NOT_HTTPS")
    if parts.hostname != "127.0.0.1":
        raise ValueError("HOSTNAME_NOT_LOOPBACK")
    if parts.username is not None or parts.password is not None:
        raise ValueError("ORIGIN_CREDENTIALS_FORBIDDEN")
    if parts.path or parts.query or parts.fragment:
        raise ValueError("ORIGIN_PATH_FORBIDDEN")
    if parts.port is None or not 1 <= parts.port <= 65535:
        raise ValueError("PORT_INVALID")
    if parts.netloc != host:
        raise ValueError("HOST_NETLOC_MISMATCH")
    if origin != "https://" + host:
        raise ValueError("ORIGIN_HOST_MISMATCH")
    return parts.port


def build_fixture(origin, host):
    """Construit URLs + cookie WEB + CSRF en mémoire seule."""
    import datetime
    import hashlib
    import json
    from dataclasses import replace
    from django.conf import settings
    from pixs.auth.contracts import Facade, AuthOutcome
    from pixs.auth.facades import WEB_COOKIE
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.auth.shell_context import PostgresShellContextService
    from pixs.auth.api_request_source import ApiRequestSource
    from pixs.auth.contracts import AuthDataClassification
    from pixs.backend.api_core_catalog import ApiInputLimits
    from pixs.backend.api_core_composition import CoreApiComposition, CoreHttpLimits
    from pixs.backend.api_core_errors_catalog import CoreApiError
    from pixs.backend.api_core_pagination import CoreCursorCodec, CoreCursorConfig
    from pixs.backend.api_core_views import ModuleHttpComposition
    from pixs.backend.api_core_views import build_core_api_urls as build_core_urls
    from pixs.backend.api_pzt_dns_boundary import build_c14_api_urls, build_c14_module_bindings
    from pixs.backend.api_pzt_dns_catalog import C14_HTTP_BINDINGS
    from pixs.backend.api_pzt_dns_dispatch import C14ApiComposition
    from pixs.backend.api_shell_context import build_shell_context_urls
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.policy import Effect, Policy, Selector, ScopeSelector, Obligation
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy, decode_policy
    from pixs.core.query_source import CoreFactSource
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.pzt.services import PztManagementPolicy
    from pixs.dns.services import DnsManagementPolicy
    from test_pzt_dns_contracts import _pztcfg, _dnscfg
    import auth_service_fixture as base

    port = _assert_loopback(origin, host)
    if not settings.configured:
        raise RuntimeError("SETTINGS_UNCONFIGURED")
    allowed = list(getattr(settings, "ALLOWED_HOSTS", []))
    if "127.0.0.1" not in allowed:
        raise RuntimeError("HOST_UNAPPROVED")
    trusted = list(getattr(settings, "CSRF_TRUSTED_ORIGINS", []))
    if origin not in trusted:
        raise RuntimeError("ORIGIN_UNAPPROVED")

    f = base.make_auth_service_fixture()
    f["clock"].now = lambda: datetime.datetime.now(datetime.timezone.utc)
    login = f["login"]("c14-composed-browser")
    web_login = f["service"]().login(
        f["grant"](f["command"]("pixs.auth.session.create", f["actor"], "c14-composed-web")),
        replace(f["supplied"], facade=Facade.WEB))
    if login.outcome is not AuthOutcome.ISSUED:
        raise RuntimeError("LOGIN_UNPROVED")
    if web_login.outcome is not AuthOutcome.ISSUED:
        raise RuntimeError("WEB_LOGIN_UNPROVED")
    if web_login.emission.cookie is None:
        raise RuntimeError("WEB_COOKIE_MISSING")
    context = f["context"]
    pzt_ref = "pixs.pzt.browser:profile"
    dns_ref = "pixs.dns.browser:profile"
    resources = {pzt_ref, dns_ref}
    actions = {b.name for b in C14_HTTP_BINDINGS}

    def grant(owner, names, targets):
        pid = "c14-browser-" + hashlib.sha256(json.dumps([owner, sorted(names), sorted(targets)]).encode()).hexdigest()[:24]
        policy = Policy(pid, "1.0.0", owner, Effect.ALLOW,
            Selector("subject", (f["actor"],)), Selector("resource", tuple(sorted(targets))),
            Selector("action", tuple(sorted(names))), ScopeSelector((context,)),
            obligations=(Obligation("AUDIT"),))
        CorePolicy.objects.create(policy_id=pid, policy_version=policy.policy_version,
            owner=owner, effect=policy.effect.value, definition=encode_policy(policy))
        return pid

    for owner, targets in (("pixs.pzt", (pzt_ref,)), ("pixs.dns", (dns_ref,))):
        names = tuple(b.name for b in C14_HTTP_BINDINGS if b.owner == owner)
        grant(owner, names, targets)
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
        return CoreAuthorizationStore(alias="default", installation_ref="c14-browser-install",
            base_epoch="c14-browser-v1",
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
            return AuthDataClassification("c14-browser-auth", ConfidentialityLevel.CONFIDENTIAL,
                PersonalDataLevel.PERSONAL)

    audit_policy = AuditPolicy("c14-browser-audit", "1.0.0", "fixture-explicite", 1,
        65536, 100, (), "c14-browser-audit", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
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
    transport = ModuleHttpComposition(source, host, origin,
        CoreHttpLimits(65536, 8192, 2, 10), ApiInputLimits(4096, 128, 32768, 128))
    shell_service = PostgresShellContextService(auth_service=auth_service, request_source=source)
    module_bindings = build_c14_module_bindings()
    c14_urls = build_c14_api_urls(composition, transport)
    shell_urls = build_shell_context_urls(shell_service, transport, module_bindings=module_bindings)

    def closed_core_factory(*, request, operation_id, authentication_source):
        raise CoreApiError("SERVICE_UNAVAILABLE")

    core_composition = CoreApiComposition(alias="default", peer_alias="peer", request_source=source,
        auth_service=auth_service, core_ports_factory=closed_core_factory, clock=f["clock"],
        approved_host=host, approved_origin=origin,
        limits=CoreHttpLimits(65536, 8192, 2, 10), input_limits=ApiInputLimits(128, 128, 32768, 16),
        cursor_codec=CoreCursorCodec(config=CoreCursorConfig(60, 8192, 128, 128, 10),
            key=b"Vecteur public de signature C06 recette seulement", clock=f["clock"]),
        interactive_commands=frozenset())
    from pixs.backend.api_core_openapi import build_core_openapi_documents, core_api_contract_plan
    core_documents = build_core_openapi_documents(core_composition)
    core_plan = core_api_contract_plan()
    core_urls = build_core_urls(core_composition, previous_plan=core_plan,
        previous_documents=tuple(text for _, text in core_documents))
    urls = c14_urls + shell_urls + core_urls
    csrf = "b" * 32
    return {"port": port, "origin": origin, "host": host, "urls": urls,
        "composition": composition, "transport": transport, "module_bindings": module_bindings,
        "core_composition": core_composition,
        "web_cookie_name": WEB_COOKIE, "web_cookie": web_login.emission.cookie.value,
        "csrf": csrf, "actor": f["actor"], "context": context, "clock": f["clock"],
        "pzt_ref": pzt_ref, "dns_ref": dns_ref, "web_session_id": str(web_login.session.session_id)}
