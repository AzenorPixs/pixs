"""Propriété PZT et autorisation C03/C04 réelles, sans service C14 ni audit commit.

Les politiques et identités sont des fixtures PostgreSQL. Les vérificateurs
locaux C03 ne créent aucune session ; la recette ne qualifie aucun raccord HTTP.
"""
from __future__ import annotations

EXPECTED_CASES = (
    "public_c03_verifier_actual", "first_platform_creation_allow",
    "first_tenant_creation_allow", "committed_owner_scope",
    "query_guard_context", "query_guard_alias", "query_guard_operation",
    "query_absent_no_intent", "retire_absent_no_intent", "no_permission_deny",
    "suspended_identity_refused", "inactive_auth_binding_refused",
    "prior_tx_callback_refused", "client_auth_dto_refused",
    "bad_namespace_refused", "command_id_substitution_refused",
    "alias_substitution_refused", "existing_scope_mismatch_closed",
    "no_config_mutation_by_adapter",
)


def scenarios():
    import datetime
    from contextlib import contextmanager
    from django.db import transaction
    from pixs.auth import models as auth_models
    from pixs.auth.identifiers import new_uuid7, identity_reference
    from pixs.auth.passwords import hash_password
    from pixs.auth.policy import SessionCategory
    from pixs.auth.runtime_verifier import (
        AuthAuthenticationVerifier, AuthVerificationError, LocalTrustProfile,
        prepare_password_verifier,
    )
    from pixs.core.authz.ports import AuthenticationContext, PortError, Request, RevocationStatus
    from pixs.core.authz.policy import (
        Effect, FederationTrust, IdentityAssurance, Obligation,
        Policy, ScopeSelector, Selector,
    )
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.command_metadata import CommandMetadata
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.persistence.models_scope import CoreScope, CoreTenant
    from pixs.core.persistence.models_group import CoreIdentityTenantMembership
    from pixs.core.query_source import CoreFactSource
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_authorization_guard import transaction_identity
    from pixs.core.services_common import CoreServiceError
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from pixs.kernel.data_governance_profile import DataGovernanceProfile
    from pixs.pzt.adapters import build_pzt_authorization
    from pixs.pzt.configuration import DesiredPztConfig
    from pixs.pzt.contracts import (
        DeclareDesiredPzt, GetDesiredPzt, RetireDesiredPzt,
        PZT_COMMANDS, PZT_QUERIES,
    )
    from pixs.pzt.models import DesiredPztRecord

    cases = {}
    now = datetime.datetime.now(datetime.timezone.utc)
    platform = ScopeContext(ScopeType.PLATFORM)
    tenant = CoreTenant.objects.create(tenant_id="tenant-c14-authz-opaque")
    first_scope = CoreScope.objects.create(scope_id="scope-c14-authz-a", tenant=tenant)
    second_scope = CoreScope.objects.create(scope_id="scope-c14-authz-b", tenant=tenant)
    scope_a = ScopeContext(ScopeType.TENANT, tenant.pk, first_scope.pk)
    scope_b = ScopeContext(ScopeType.TENANT, tenant.pk, second_scope.pk)

    class Clock:
        def now(self):
            return now

    clock = Clock()
    actor_id = new_uuid7()
    actor = identity_reference(actor_id)
    CoreIdentity.objects.create(identity_id=actor_id, identity_type="HUMAN", state="ACTIVE")
    CoreIdentityTenantMembership.objects.create(identity_id=actor_id, tenant=tenant, activation="ACTIVE")
    gate = auth_models.AuthAccountGate.objects.create(identity_id=actor_id)
    binding = auth_models.AuthBinding.objects.create(
        identity=gate, provider_id="c14-local", issuer="fixture-c14",
        external_subject="fixture-c14-actor", enabled=True,
    )
    # Valeur publique de fixture ; aucun credential réel n'est reçu ou imprimé.
    password = "Vecteur public C14 pour verifier local reel"
    auth_models.AuthPasswordCredential.objects.create(
        binding=binding, password_hash=hash_password(password), enabled=True,
    )
    for context in (platform, scope_a, scope_b):
        auth_models.AuthPolicyRow.objects.create(
            policy_id="c14-auth-policy", policy_version="1.0.0", origin="fixture-explicite",
            scope_type=context.scope_type.value, tenant_id=context.tenant_id, scope_id=context.scope_id,
            category="ORDINARY", idle_seconds=600, absolute_seconds=3600, access_seconds=300,
            freshness_seconds=120, max_sessions=3, is_current=True,
        )
    profile = LocalTrustProfile(
        "c14-auth-policy", "1.0.0", binding.provider_id, binding.issuer, FederationTrust.TRUSTED,
    )

    class Trust:
        def resolve(self, profile_id, request, *, alias, operation_id):
            return profile

    class Assurance:
        def resolve(self, identity_ref, request, *, alias, operation_id):
            return IdentityAssurance.CLAIMED

    def authentication(request, operation_id):
        return prepare_password_verifier(
            request=request, alias="default", operation_id=operation_id, profile=profile,
            trust_source=Trust(), assurance_source=Assurance(), facts_reader=CoreFactSource(),
            clock=clock, external_subject=binding.external_subject, password=password,
            category=SessionCategory.ORDINARY,
        )

    target = "pixs.pzt.fixture:platform"
    tenant_target = "pixs.pzt.fixture:tenant"
    absent = "pixs.pzt.fixture:absent"
    denied = "pixs.pzt.fixture:denied"
    actions = PZT_COMMANDS + PZT_QUERIES
    catalog = Catalog(
        (actor,), (target, tenant_target, absent, denied), actions,
        (platform, scope_a, scope_b), (),
    )
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    policy = Policy(
        "c14-allow", "1.0.0", "pixs.pzt", Effect.ALLOW,
        Selector("subject", (actor,)), Selector("resource", (target, tenant_target, absent)),
        Selector("action", actions), ScopeSelector((platform, scope_a, scope_b)),
        obligations=(Obligation("AUDIT"),),
    )
    CorePolicy.objects.create(
        policy_id=policy.policy_id, policy_version=policy.policy_version,
        owner=policy.owner, effect=policy.effect.value, definition=encode_policy(policy),
    )
    store = CoreAuthorizationStore(
        alias="default", installation_ref="c14-authz-install",
        base_epoch="c14-authz-v1", catalog=catalog, limits=limits,
    )

    def configuration():
        governance = DataGovernanceProfile(
            "1.0.0", "pixs.pzt.fixture", "pixs.pzt", "pixs.pzt.postgresql",
            frozenset({"CONFIGURATION"}), ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE,
            frozenset(), "fixture-retention", "fixture-deletion", frozenset(),
            frozenset(), frozenset(), "fixture-export", "fixture-lineage",
        )
        return DesiredPztConfig(
            "1.0.0", "pixs.pzt", 1, False, "fixture-plan", "fixture-budget", governance, (),
        )

    def request(action, resource, context, tag):
        return Request("decision-" + tag, actor, resource, action, context, "correlation-" + tag)

    def declare(resource, context, tag):
        req = request("declare_desired_pzt", resource, context, tag)
        meta = CommandMetadata(
            "operation-" + tag, (req.correlation_id,), (), context,
            "declare_desired_pzt", actor, "idempotence-" + tag,
        )
        return DeclareDesiredPzt("1.0.0", meta, req, resource, 0, configuration())

    def query(resource, context, tag):
        return GetDesiredPzt("1.0.0", request("get_desired_pzt", resource, context, tag), resource)

    @contextmanager
    def authorize(command, operation_id):
        verifier = authentication(command.request, operation_id)
        with transaction.atomic(using="default", durable=True):
            provider, decider, owners = build_pzt_authorization(
                store=store, auth_source=verifier, clock=clock, cmd=command,
                alias="default", operation_id=operation_id,
            )
            decider.prepare_core_under_locks(command.request, "default", operation_id)
            yield verifier, provider, decider, owners

    def denied_port(name, action):
        try:
            action()
        except PortError:
            cases[name] = True
        else:
            cases[name] = False

    def seed(resource, context):
        row = DesiredPztRecord(
            resource_id=resource, scope_type=context.scope_type.value,
            tenant_id=context.tenant_id, scope_id=context.scope_id,
            v6_enabled=False, plan_ref="fixture-plan", budget_ref="fixture-budget",
            config=dict(schema_version="1.0.0", plan_ref="fixture-plan",
                        budget_ref="fixture-budget", v6_enabled=False),
            governance=dict(
                profile_version="1.0.0", data_asset_id="pixs.pzt.fixture",
                owner_component="pixs.pzt", source_of_truth="pixs.pzt.postgresql",
                data_classes=["CONFIGURATION"], confidentiality="INTERNAL", personal_data="NONE",
                purpose_refs=[], retention_policy="fixture-retention",
                deletion_policy="fixture-deletion", residency_constraints=[],
                authorized_consumers=[], processor_refs=[], export_policy="fixture-export",
                lineage="fixture-lineage",
            ),
            payload_sha256="a" * 64, created_at=now, updated_at=now,
        )
        row.full_clean()
        row.save()
        return row

    first = declare(target, platform, "first")
    with authorize(first, first.metadata.command_id) as (verifier, provider, decider, owners):
        decision = decider.revalidate_under_locks(
            first.request, alias="default", operation_id=first.metadata.command_id,
        )
        facts = provider.resolve(first.request)
        cases["public_c03_verifier_actual"] = (
            type(verifier) is AuthAuthenticationVerifier
            and type(facts.auth) is AuthenticationContext
            and facts.auth.digital_identity_id == actor
            and facts.auth.session_id is None
            and facts.revocation_status is RevocationStatus.ACTIVE
        )
        cases["first_platform_creation_allow"] = (
            decision.effect is Effect.ALLOW and facts.ownership.context == platform
            and facts.ownership.resource_id == target
            and DesiredPztRecord.objects.count() == 0
        )
    seed(target, platform)
    tenant_first = declare(tenant_target, scope_b, "tenant-first")
    with authorize(tenant_first, tenant_first.metadata.command_id) as (_, provider, decider, owners):
        decision = decider.revalidate_under_locks(
            tenant_first.request, alias="default", operation_id=tenant_first.metadata.command_id,
        )
        cases["first_tenant_creation_allow"] = (
            decision.effect is Effect.ALLOW
            and provider.resolve(tenant_first.request).ownership.context == scope_b
        )
    seed(tenant_target, scope_a)

    q = query(target, platform, "query")
    with authorize(q, "operation-query") as (_, provider, decider, owners):
        decision = decider.revalidate_under_locks(q.request, alias="default", operation_id="operation-query")
        own = owners[0].ownership(target, context=platform, alias="default", operation_id="operation-query")
        cases["committed_owner_scope"] = decision.effect is Effect.ALLOW and own.context == platform
        denied_port("query_guard_context", lambda: owners[0].ownership(
            target, context=scope_a, alias="default", operation_id="operation-query"))
        denied_port("query_guard_alias", lambda: owners[0].ownership(
            target, context=platform, alias="peer", operation_id="operation-query"))
        denied_port("query_guard_operation", lambda: owners[0].ownership(
            target, context=platform, alias="default", operation_id="other-operation"))
        old_owner = owners[0]
        old_pin = transaction_identity("default")
        denied_port("client_auth_dto_refused", lambda: build_pzt_authorization(
            store=store, auth_source={"authenticated": True}, clock=clock,
            cmd=q, alias="default", operation_id="operation-query"))
        denied_port("alias_substitution_refused", lambda: build_pzt_authorization(
            store=store, auth_source=authentication(q.request, "operation-query"), clock=clock,
            cmd=q, alias="peer", operation_id="operation-query"))
    with transaction.atomic(using="default", durable=True):
        different_tx = transaction_identity("default") != old_pin
        denied_port("prior_tx_callback_refused", lambda: old_owner.ownership(
            target, context=platform, alias="default", operation_id="operation-query"))
        cases["prior_tx_callback_refused"] = cases["prior_tx_callback_refused"] and different_tx

    missing_query = query(absent, platform, "missing-query")
    with authorize(missing_query, "operation-missing-query") as (_, _, _, owners):
        cases["query_absent_no_intent"] = owners[0].ownership(
            absent, context=platform, alias="default", operation_id="operation-missing-query") is None
    retire_request = request("retire_desired_pzt", absent, platform, "missing-retire")
    retire_metadata = CommandMetadata(
        "operation-missing-retire", (retire_request.correlation_id,), (), platform,
        "retire_desired_pzt", actor, "idempotence-missing-retire",
    )
    retire = RetireDesiredPzt("1.0.0", retire_metadata, retire_request, absent, 1, "fixture-retire")
    with authorize(retire, retire_metadata.command_id) as (_, _, _, owners):
        cases["retire_absent_no_intent"] = owners[0].ownership(
            absent, context=platform, alias="default", operation_id=retire_metadata.command_id) is None

    without_right = declare(denied, platform, "without-right")
    with authorize(without_right, without_right.metadata.command_id) as (_, _, decider, _):
        cases["no_permission_deny"] = decider.revalidate_under_locks(
            without_right.request, alias="default", operation_id=without_right.metadata.command_id
        ).effect is Effect.DENY

    mismatch = query(tenant_target, scope_b, "mismatch")
    with authorize(mismatch, "operation-mismatch") as (_, provider, _, owners):
        actual = owners[0].ownership(
            tenant_target, context=scope_b, alias="default", operation_id="operation-mismatch")
        try:
            provider.resolve(mismatch.request)
        except PortError:
            cases["existing_scope_mismatch_closed"] = actual.context == scope_a
        else:
            cases["existing_scope_mismatch_closed"] = False

    bad = declare("pixs.foreign.fixture:other", platform, "bad-namespace")
    with transaction.atomic(using="default", durable=True):
        denied_port("bad_namespace_refused", lambda: build_pzt_authorization(
            store=store, auth_source=authentication(bad.request, bad.metadata.command_id),
            clock=clock, cmd=bad, alias="default", operation_id=bad.metadata.command_id))
        denied_port("command_id_substitution_refused", lambda: build_pzt_authorization(
            store=store, auth_source=authentication(first.request, first.metadata.command_id),
            clock=clock, cmd=first, alias="default", operation_id="substituted-operation"))

    CoreIdentity.objects.filter(pk=actor_id).update(state="SUSPENDED", version=2)
    try:
        try:
            with authorize(first, first.metadata.command_id) as (_, _, decider, _):
                decider.revalidate_under_locks(
                    first.request, alias="default", operation_id=first.metadata.command_id)
        except (PortError, CoreServiceError, AuthVerificationError):
            cases["suspended_identity_refused"] = (
                CoreIdentity.objects.get(pk=actor_id).state == "SUSPENDED")
        else:
            cases["suspended_identity_refused"] = False
    finally:
        CoreIdentity.objects.filter(pk=actor_id).update(state="ACTIVE", version=1)
    auth_models.AuthBinding.objects.filter(pk=binding.pk).update(enabled=False, version=2)
    try:
        try:
            authentication(first.request, first.metadata.command_id)
        except AuthVerificationError:
            cases["inactive_auth_binding_refused"] = not auth_models.AuthBinding.objects.get(pk=binding.pk).enabled
        else:
            cases["inactive_auth_binding_refused"] = False
    finally:
        auth_models.AuthBinding.objects.filter(pk=binding.pk).update(enabled=True, version=1)
    cases["no_config_mutation_by_adapter"] = DesiredPztRecord.objects.count() == 2
    return cases


def run(root_str):
    from c14_pg_test_support import run_in_c14_schema
    return run_in_c14_schema(root_str, scenarios, EXPECTED_CASES)
