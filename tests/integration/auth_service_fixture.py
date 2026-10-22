"""Assemblage de recette : vrais Auth/C04/C05, plan/C10/clé opérateur fixtures."""
from __future__ import annotations


def make_auth_service_fixture():
    import datetime
    import hashlib
    from pixs.auth import models as m
    from pixs.auth.contracts import AuthCommand, LoginInput, Facade, AuthDataClassification
    from pixs.auth.policy import SessionCategory
    from pixs.auth.configuration import create_local_auth_sources
    from pixs.auth.identifiers import identity_reference
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.core.authz.ports import Request
    from pixs.core.authz.policy import Policy, Selector, ScopeSelector, Effect, Obligation
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.query_source import CoreFactSource
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from test_auth_configuration_postgres import scenarios as configure
    configured = configure()
    if len(configured) != 24 or not all(configured.values()):
        raise AssertionError("CONFIGURATION_UNPROVED")
    selected = m.AuthLocalTrustSelection.objects.get(profile_ref="pixs.auth.local")
    identity = selected.approval_operation.identity_id
    actor = identity_reference(identity)
    context = ScopeContext(ScopeType.PLATFORM)
    class Clock:
        def __init__(self):
            self.value = datetime.datetime.now(datetime.timezone.utc)
        def now(self):
            return self.value
    clock = Clock()
    trust, assurance = create_local_auth_sources(alias="default", profile_id=selected.profile_ref, clock=clock)
    actions = ("pixs.auth.session.create", "pixs.auth.session.renew", "pixs.auth.session.logout", "pixs.auth.session.revoke", "pixs.auth.session.revoke_all", "pixs.auth.audit.reconcile", "pixs.auth.credential.change", "pixs.auth.credential.recover", "pixs.auth.session.activity")
    def command(action, resource, label):
        return AuthCommand(Request("decision-"+label, actor, resource, action, context, "correlation-"+label), "operation-"+label, "idem-"+label)
    def grant(cmd):
        pid = "fixture-"+hashlib.sha256((cmd.request.action_id+cmd.request.resource_id).encode()).hexdigest()[:32]
        if not CorePolicy.objects.filter(policy_id=pid).exists():
            p = Policy(pid, "1.0.0", "pixs.auth", Effect.ALLOW, Selector("subject", (actor,)), Selector("resource", (cmd.request.resource_id,)), Selector("action", (cmd.request.action_id,)), ScopeSelector((context,)), obligations=(Obligation("AUDIT"),))
            CorePolicy.objects.create(policy_id=p.policy_id, policy_version=p.policy_version, owner=p.owner, effect=p.effect.value, definition=encode_policy(p))
        return cmd
    def factory(*, request, operation_id, authentication_source):
        resources = {actor, "pixs.auth.account:"+str(identity), request.resource_id}
        resources.update("pixs.auth.session:"+str(pk) for pk in m.AuthSession.objects.values_list("pk", flat=True))
        resources.update("pixs.auth.audit-pending:"+str(pk) for pk in m.AuthAuditPending.objects.values_list("pk", flat=True))
        resources.update("pixs.auth.credential:"+str(pk) for pk in m.AuthPasswordCredential.objects.values_list("pk", flat=True))
        limits = Limits(128, 128, 10, 100, 100, 128, 256, 256, 10000000, 60, 3600)
        store = CoreAuthorizationStore(alias="default", installation_ref="service-fixture", base_epoch="auth-service-v1", catalog=Catalog((actor,), tuple(sorted(resources)), actions, (context,), ()), limits=limits)
        provider = RuntimeTrustedFactsProvider(store=store, authentication_source=authentication_source, request=request, operation_id=operation_id, additional_owners=(RuntimeResourceOwner("pixs.auth.", authentication_source.ownership),))
        return RuntimeAuthorizationDecider(store=store, facts_provider=provider, clock=clock, request=request, operation_id=operation_id)
    class Classification:
        def resolve(self, **kwargs):
            return AuthDataClassification("auth-service-asset", ConfidentialityLevel.CONFIDENTIAL, PersonalDataLevel.PERSONAL)
    def service(max_bytes=65536):
        policy = AuditPolicy("service-audit", "1.0.0", "fixture-explicite", 1, max_bytes, 100, (), "service-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
        return PostgresLocalAuthService(alias="default", peer_alias="peer", profile_id=selected.profile_ref, trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, audit=PostgresAuditParticipant(ExplicitAuditPolicySource(context, policy), clock, "peer"), classification_source=Classification(), decider_factory=factory)
    supplied = LoginInput("initial-subject", "Vecteur public configuration C03, aucun secret réel", SessionCategory.ORDINARY, Facade.API, None)
    def login(label):
        cmd = grant(command("pixs.auth.session.create", actor, "login-"+label))
        return service().login(cmd, supplied)
    return dict(service=service, login=login, command=command, grant=grant, identity=identity, actor=actor, context=context, clock=clock, trust=trust, assurance=assurance, profile=trust.current_profile(context), supplied=supplied)
