"""Première recette réelle du service DNS : C03/C04/C05 et mutations locales."""
from __future__ import annotations
EXPECTED_CASES = ('declare_commit_audit_idem', 'identical_replay_no_double_effect', 'cas_update_created_at_preserved', 'stale_revision_no_business_effect', 'retire_business_preserves_data_dimensions', 'audit_failure_rolls_back_all', 'divergent_replay_closed', 'expired_key_not_reexecuted', 'retirement_replay_confirmed_once', 'retirement_reason_divergence_closed', 'client_governance_not_authority', 'idempotence_policy_requires_positive_lifetime', 'lost_commit_ack_reconciled_without_double_effect', 'commit_not_sent_no_effect_or_success', 'desired_query_current_revision', 'applied_query_unknown_not_zero', 'query_current_permission_deny', 'views_order_retained_in_payload', 'name_declaration_atomic_audited', 'name_case_insensitive_replay_original_retained', 'name_reassignment_requires_retirement', 'name_view_isolated', 'name_unknown_view_closed', 'name_outside_zone_closed', 'name_apex_closed', 'name_stale_zone_revision_closed', 'name_audit_failure_rolls_back_all', 'name_policy_is_desired_unverified', 'name_missing_desired_not_nxdomain', 'name_retirement_preserves_history', 'name_retirement_replay_once', 'name_reassignment_new_history_row', 'namespace_change_requires_migration', 'view_removal_with_current_names_closed', 'dns_name_label_wire_boundaries', 'ordinary_flags_do_not_waive_obligations', 'root_without_flags_remains_audited', 'root_explicit_flags_waive_audit_governance', 'root_waived_replay_no_double_effect', 'revoked_root_cannot_replay_waived_result', 'tenant_service_actual_scope_persisted', 'wrong_scope_cannot_modify_tenant_state', 'platform_and_tenant_same_resource_isolated', 'tenant_query_reads_own_revision', 'concurrent_commands_one_effect_closed_conflict', 'lifecycle_outside_host_closed', 'lifecycle_real_pg_management_ready_without_executor', 'missing_executor_operation_closed', 'unverified_observation_closed', 'lifecycle_exit_revokes_readiness', 'lifecycle_enabled_separate_from_health', 'host_runtime_owned_pg_lifecycle_hooks', 'host_runtime_unready_essential_zero_hooks', 'lifecycle_audit_unavailable_closes_management', 'root_tenant_without_grant_closed', 'root_tenant_grant_current_and_audited', 'root_tenant_granted_explicit_waiver', 'lifecycle_unbound_capability_not_advertised', 'views_query_preserves_order', 'policy_query_view_isolation', 'policy_query_ttl_ceilings', 'policy_query_unknown_view_closed', 'policy_query_outside_zone_closed', 'policy_query_permission_deny')

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
    from pixs.dns.adapters import build_dns_authorization
    from pixs.dns.configuration import DesiredDnsConfig
    from pixs.dns.contracts import (
        DeclareDesiredDns, GetDesiredDns, RetireDesiredDns,
        DNS_COMMANDS, DNS_QUERIES,
    )
    from pixs.dns.models import DesiredDnsRecord

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

    target = "pixs.dns.fixture:platform"
    tenant_target = "pixs.dns.fixture:tenant"
    absent = "pixs.dns.fixture:absent"
    denied = "pixs.dns.fixture:denied"
    actions = DNS_COMMANDS + DNS_QUERIES
    catalog = Catalog(
        (actor,), (target, tenant_target, absent, denied), actions,
        (platform, scope_a, scope_b), (),
    )
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    policy = Policy(
        "c14-allow", "1.0.0", "pixs.dns", Effect.ALLOW,
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
            "1.0.0", "pixs.dns.fixture", "pixs.dns", "pixs.dns.postgresql",
            frozenset({"CONFIGURATION"}), ConfidentialityLevel.INTERNAL, PersonalDataLevel.NONE,
            frozenset(), "fixture-retention", "fixture-deletion", frozenset(),
            frozenset(), frozenset(), "fixture-export", "fixture-lineage",
        )
        return DesiredDnsConfig(
            "1.0.0", "pixs.dns", 1, "fixture.invalid", 0, 0,
            ("private", "public"), governance, (),
        )

    def request(action, resource, context, tag):
        return Request("decision-" + tag, actor, resource, action, context, "correlation-" + tag)

    def declare(resource, context, tag):
        req = request("declare_desired_dns", resource, context, tag)
        meta = CommandMetadata(
            "operation-" + tag, (req.correlation_id,), (), context,
            "declare_desired_dns", actor, "idempotence-" + tag,
        )
        return DeclareDesiredDns("1.0.0", meta, req, resource, 0, configuration())

    def query(resource, context, tag):
        return GetDesiredDns("1.0.0", request("get_desired_dns", resource, context, tag), resource)


    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.dns.models import DnsIdempotenceRecord
    from pixs.dns.services import PostgresDnsService, DnsManagementPolicy, DnsServiceError
    from dataclasses import replace

    governance_profile = configuration().governance

    class ManagementPolicy:
        def resolve(self, *, context, alias, operation_id):
            if context != platform or alias != "default":
                raise DnsServiceError("DNS_POLICY_INVALID")
            # Durée explicite de fixture, aucune valeur de production déduite.
            return DnsManagementPolicy(datetime.timedelta(minutes=10), governance_profile)

    def source(*, request, alias, operation_id):
        if alias != "default":
            raise DnsServiceError("DNS_AUTH_UNAVAILABLE")
        return authentication(request, operation_id)

    def service(max_event_bytes):
        audit_policy = AuditPolicy(
            "c14-command-audit", "1.0.0", "fixture-explicite", 1,
            max_event_bytes, 50, (), "c14-command-audit-asset",
            ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL,
        )
        audit = PostgresAuditParticipant(
            ExplicitAuditPolicySource(platform, audit_policy), clock, "peer",
        )
        return PostgresDnsService(
            alias="default", peer_alias="peer", store=store, clock=clock,
            audit=audit, auth_factory=source, policy_source=ManagementPolicy(),
        )

    svc = service(65536)
    first = declare(target, platform, "service-first")
    result = svc.declare_desired(first)
    desired = DesiredDnsRecord.objects.get(resource_id=target, tenant_id__isnull=True)
    idem = DnsIdempotenceRecord.objects.get(
        tenant_id__isnull=True, subject_id=actor, command_type="declare_desired_dns",
        idempotency_key=first.metadata.idempotency_key,
    )
    cases["declare_commit_audit_idem"] = (
        result.outcome == "SUCCEEDED" and result.audit_disposition == "AUDITED"
        and desired.config_revision == 1 and desired.business_state == "DECLARED"
        and idem.state == "SUCCEEDED" and idem.result == result.record()
        and idem.result_version == 1
        and CoreAuditEvent.objects.using("peer").filter(
            operation_id=first.metadata.command_id).count() == 1
        and desired.governance_ref == governance_profile.data_asset_id
        and desired.confidentiality == governance_profile.confidentiality.value
    )
    created_at = desired.created_at
    initial_audits = CoreAuditEvent.objects.count()
    replay_correlation = "correlation-service-replay"
    replay = replace(
        first,
        metadata=replace(first.metadata, command_id="operation-service-replay",
                         correlation_ids=(replay_correlation,)),
        request=replace(first.request, decision_id="decision-service-replay",
                        correlation_id=replay_correlation),
    )
    replayed = svc.declare_desired(replay)
    cases["identical_replay_no_double_effect"] = (
        replayed.replayed and replayed.operation_id == first.metadata.command_id
        and replayed.config_revision == 1
        and DesiredDnsRecord.objects.count() == 1
        and DnsIdempotenceRecord.objects.count() == 1
        and CoreAuditEvent.objects.count() == initial_audits
    )
    update = declare(target, platform, "service-update")
    update = replace(
        update, expected_revision=1,
        configuration=replace(configuration(), config_revision=2, ttl_positive=15),
    )
    updated = svc.declare_desired(update)
    desired.refresh_from_db()
    cases["cas_update_created_at_preserved"] = (
        updated.outcome == "SUCCEEDED" and desired.config_revision == 2
        and desired.version == 2 and desired.ttl_positive == 15
        and desired.created_at == created_at
    )
    stale = declare(target, platform, "service-stale")
    try:
        svc.declare_desired(stale)
    except DnsServiceError as error:
        cases["stale_revision_no_business_effect"] = (
            error.code == "DNS_REVISION_CONFLICT"
            and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == 2
            and not DnsIdempotenceRecord.objects.filter(
                idempotency_key=stale.metadata.idempotency_key).exists()
        )
    else:
        cases["stale_revision_no_business_effect"] = False

    retirement_request = request("retire_desired_dns", target, platform, "service-retire")
    retirement_metadata = CommandMetadata(
        "operation-service-retire", (retirement_request.correlation_id,), (), platform,
        "retire_desired_dns", actor, "idempotence-service-retire",
    )
    retirement = RetireDesiredDns(
        "1.0.0", retirement_metadata, retirement_request, target, 2, "fixture-retire",
    )
    retired = svc.retire_desired(retirement)
    desired.refresh_from_db()
    cases["retire_business_preserves_data_dimensions"] = (
        retired.outcome == "SUCCEEDED" and retired.config_revision == 3
        and desired.business_state == "RETIRED" and desired.persistence_state == "ACTIVE"
        and desired.retention_state == "RETAINED" and desired.created_at == created_at
    )

    failing = declare(absent, platform, "service-audit-failure")
    counts = (DesiredDnsRecord.objects.count(), DnsIdempotenceRecord.objects.count(),
              CoreAuditEvent.objects.count())
    # C05 réel refuse la taille de l'événement ; aucun mock de son participant.
    broken_audit_service = service(1)
    try:
        broken_audit_service.declare_desired(failing)
    except DnsServiceError as error:
        cases["audit_failure_rolls_back_all"] = (
            error.code == "DNS_AUDIT_UNAVAILABLE"
            and not DesiredDnsRecord.objects.filter(resource_id=absent).exists()
            and not DnsIdempotenceRecord.objects.filter(
                idempotency_key=failing.metadata.idempotency_key).exists()
            and counts == (DesiredDnsRecord.objects.count(), DnsIdempotenceRecord.objects.count(),
                           CoreAuditEvent.objects.count())
        )
    else:
        cases["audit_failure_rolls_back_all"] = False

    reordered = replace(first, configuration=replace(
        first.configuration, views=tuple(reversed(first.configuration.views))))
    try:
        svc.declare_desired(reordered)
    except DnsServiceError as error:
        cases["views_order_retained_in_payload"] = error.code == "DNS_IDEMPOTENCE_CONFLICT"
    else:
        cases["views_order_retained_in_payload"] = False

    # Les refus de contenu ne doivent jamais être remplacés par une erreur CAS.
    divergent = replace(first, configuration=replace(first.configuration, ttl_positive=15))
    try:
        svc.declare_desired(divergent)
    except DnsServiceError as error:
        cases["divergent_replay_closed"] = (
            error.code == "DNS_IDEMPOTENCE_CONFLICT"
            and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == 3
        )
    else:
        cases["divergent_replay_closed"] = False

    old_expires = DnsIdempotenceRecord.objects.get(pk=idem.pk).expires_at
    DnsIdempotenceRecord.objects.filter(pk=idem.pk).update(
        expires_at=now-datetime.timedelta(seconds=1))
    try:
        try:
            svc.declare_desired(replay)
        except DnsServiceError as error:
            cases["expired_key_not_reexecuted"] = (
                error.code == "DNS_IDEMPOTENCE_EXPIRED"
                and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == 3
                and DnsIdempotenceRecord.objects.filter(pk=idem.pk).count() == 1
            )
        else:
            cases["expired_key_not_reexecuted"] = False
    finally:
        DnsIdempotenceRecord.objects.filter(pk=idem.pk).update(expires_at=old_expires)

    retirement_replay_correlation = "correlation-retirement-replay"
    retirement_replay = replace(
        retirement,
        metadata=replace(retirement.metadata, command_id="operation-retirement-replay",
                         correlation_ids=(retirement_replay_correlation,)),
        request=replace(retirement.request, decision_id="decision-retirement-replay",
                        correlation_id=retirement_replay_correlation),
    )
    retired_again = svc.retire_desired(retirement_replay)
    cases["retirement_replay_confirmed_once"] = (
        retired_again.replayed and retired_again.operation_id == retirement.metadata.command_id
        and retired_again.config_revision == 3
        and CoreAuditEvent.objects.filter(operation_id=retirement.metadata.command_id).count() == 1
    )
    try:
        svc.retire_desired(replace(retirement_replay, reason="different-fixture-reason"))
    except DnsServiceError as error:
        cases["retirement_reason_divergence_closed"] = (
            error.code == "DNS_IDEMPOTENCE_CONFLICT"
            and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == 3
        )
    else:
        cases["retirement_reason_divergence_closed"] = False

    spoof = declare(absent, platform, "governance-spoof")
    spoof = replace(spoof, configuration=replace(
        spoof.configuration, governance=replace(governance_profile, data_asset_id="other-asset")))
    try:
        svc.declare_desired(spoof)
    except DnsServiceError as error:
        cases["client_governance_not_authority"] = (
            error.code == "DNS_GOVERNANCE_INVALID"
            and not DesiredDnsRecord.objects.filter(resource_id=absent).exists()
        )
    else:
        cases["client_governance_not_authority"] = False
    try:
        DnsManagementPolicy(datetime.timedelta(), governance_profile)
    except DnsServiceError as error:
        cases["idempotence_policy_requires_positive_lifetime"] = error.code == "DNS_POLICY_INVALID"
    else:
        cases["idempotence_policy_requires_positive_lifetime"] = False

    # Injection de défaut de transport : C03/C04/C05 et le commit restent réels.
    from django.db import connections, DatabaseError
    from unittest.mock import patch
    owner_connection = connections["default"]
    commit = owner_connection.commit
    lost_command = declare(absent, platform, "committed-lost-ack")
    def committed_then_lost():
        commit()
        raise DatabaseError("fixture_commit_ack_lost")
    with patch.object(owner_connection, "commit", side_effect=committed_then_lost):
        uncertain = svc.declare_desired(lost_command)
    committed_idem = DnsIdempotenceRecord.objects.using("peer").get(
        subject_id=actor, command_type="declare_desired_dns",
        idempotency_key=lost_command.metadata.idempotency_key, tenant_id__isnull=True,
    )
    lost_replay_correlation = "correlation-lost-ack-replay"
    lost_replay = replace(
        lost_command,
        metadata=replace(lost_command.metadata, command_id="operation-lost-ack-replay",
                         correlation_ids=(lost_replay_correlation,)),
        request=replace(lost_command.request, decision_id="decision-lost-ack-replay",
                        correlation_id=lost_replay_correlation),
    )
    confirmed = svc.declare_desired(lost_replay)
    cases["lost_commit_ack_reconciled_without_double_effect"] = (
        uncertain.outcome == "UNKNOWN" and uncertain.config_revision is None
        and uncertain.audit_disposition == "AUDITED"
        and committed_idem.state == "SUCCEEDED" and confirmed.replayed
        and confirmed.operation_id == lost_command.metadata.command_id
        and DesiredDnsRecord.objects.filter(resource_id=absent).count() == 1
        and DnsIdempotenceRecord.objects.filter(pk=committed_idem.pk).count() == 1
        and CoreAuditEvent.objects.filter(operation_id=lost_command.metadata.command_id).count() == 1
    )
    uncommitted = declare(tenant_target, platform, "uncommitted-error")
    def commit_not_sent():
        raise DatabaseError("fixture_commit_not_sent")
    with patch.object(owner_connection, "commit", side_effect=commit_not_sent):
        unknown = svc.declare_desired(uncommitted)
    cases["commit_not_sent_no_effect_or_success"] = (
        unknown.outcome == "UNKNOWN" and unknown.audit_disposition == "UNKNOWN"
        and not DesiredDnsRecord.objects.filter(resource_id=tenant_target).exists()
        and not DnsIdempotenceRecord.objects.filter(
            idempotency_key=uncommitted.metadata.idempotency_key).exists()
        and not CoreAuditEvent.objects.filter(operation_id=uncommitted.metadata.command_id).exists()
    )


    from pixs.dns.contracts import GetDesiredDns, GetAppliedDns
    query_request = request("get_desired_dns", target, platform, "query-desired")
    before_idempotence = DnsIdempotenceRecord.objects.count()
    wanted = svc.get_desired(
        GetDesiredDns("1.0.0", query_request, target), operation_id="query-desired-operation",
    )
    cases["desired_query_current_revision"] = (
        wanted["config_revision"] == DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
        and wanted["business_state"] == "RETIRED"
        and wanted["configuration"]["owner_id"] == "pixs.dns"
    )
    cases["views_query_preserves_order"] = (
        wanted["configuration"]["views"] == list(first.configuration.views)
        and wanted["configuration"]["views"] == ["private", "public"]
    )
    applied_request = request("get_applied_dns", target, platform, "query-applied")
    observed = svc.get_applied(
        GetAppliedDns("1.0.0", applied_request, target), operation_id="query-applied-operation",
    )
    cases["applied_query_unknown_not_zero"] = (
        observed["application_status"] == "UNKNOWN"
        and observed["measurement_status"] == "UNMEASURED"
        and all(observed[name] is None for name in (
            "applied_revision", "applied_present", "generation",
            "observed_at", "valid_until", "measurements"))
        and DnsIdempotenceRecord.objects.count() == before_idempotence
    )
    fixture_values = {
        field.attname: getattr(desired, field.attname)
        for field in desired._meta.concrete_fields if not field.primary_key
    }
    fixture_values["resource_id"] = denied
    denied_row = DesiredDnsRecord(**fixture_values)
    denied_row.full_clean()
    denied_row.save()
    denied_request = request("get_desired_dns", denied, platform, "query-denied")
    try:
        svc.get_desired(
            GetDesiredDns("1.0.0", denied_request, denied),
            operation_id="query-denied-operation",
        )
    except DnsServiceError as error:
        cases["query_current_permission_deny"] = error.code == "DNS_DENIED"
    else:
        cases["query_current_permission_deny"] = False


    from pixs.dns.contracts import DeclareName, RetireName, ResolveViewPolicy
    from pixs.dns.models import DnsNameRecord
    from pixs.dns.naming import dns_name_key
    current = DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
    reactivate = replace(
        declare(target, platform, "names-reactivate"), expected_revision=current,
        configuration=replace(configuration(), config_revision=current + 1),
    )
    svc.declare_desired(reactivate)

    def name_command(tag, *, name="Alias.fixture.invalid", view="private",
                     reference="pixs.agent.instance:unverified-a", retired=False):
        action = "retire_name" if retired else "declare_name"
        req = request(action, target, platform, tag)
        meta = CommandMetadata("operation-" + tag, (req.correlation_id,), (), platform,
                               action, actor, "idempotence-" + tag)
        rev = DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
        args = ("1.0.0", meta, req, target, rev, name, view)
        return RetireName(*args) if retired else DeclareName(*args, reference)

    def name_failure(command, code, service=svc):
        rev = DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
        count = DnsNameRecord.objects.count()
        try:
            (service.retire_name if type(command) is RetireName else service.declare_name)(command)
        except DnsServiceError as error:
            return (error.code == code
                    and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == rev
                    and DnsNameRecord.objects.count() == count
                    and not DnsIdempotenceRecord.objects.filter(
                        idempotency_key=command.metadata.idempotency_key).exists())
        return False

    name_first = name_command("name-first")
    nr = svc.declare_name(name_first)
    name_row = DnsNameRecord.objects.get(zone=desired, is_current=True)
    cases["name_declaration_atomic_audited"] = (
        nr.outcome == "SUCCEEDED" and nr.audit_disposition == "AUDITED"
        and name_row.config_revision == nr.config_revision
        and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == nr.config_revision
        and name_row.name == "Alias.fixture.invalid"
        and name_row.name_key == "alias.fixture.invalid"
        and name_row.governance_ref == governance_profile.data_asset_id
        and CoreAuditEvent.objects.filter(operation_id=name_first.metadata.command_id).count() == 1
    )
    aliases = DnsNameRecord.objects.count()
    replay_name = svc.declare_name(replace(name_first, name="ALIAS.FIXTURE.INVALID."))
    cases["name_case_insensitive_replay_original_retained"] = (
        replay_name.replayed and replay_name.operation_id == nr.operation_id
        and DnsNameRecord.objects.count() == aliases
        and DnsNameRecord.objects.get(pk=name_row.pk).name == "Alias.fixture.invalid"
    )
    cases["name_reassignment_requires_retirement"] = name_failure(
        name_command("name-collision", name="alias.fixture.invalid",
                     reference="pixs.agent.instance:unverified-b"),
        "DNS_NAME_RETIREMENT_REQUIRED",
    )
    cases["name_view_isolated"] = (
        svc.declare_name(name_command("name-public", view="public",
                                     reference="pixs.agent.instance:unverified-b")).outcome == "SUCCEEDED"
        and DnsNameRecord.objects.filter(zone=desired, name_key="alias.fixture.invalid",
                                         is_current=True).count() == 2
    )
    cases["name_unknown_view_closed"] = name_failure(
        name_command("name-unknown-view", view="other"), "DNS_VIEW_UNAVAILABLE")
    cases["name_outside_zone_closed"] = name_failure(
        name_command("name-outside", name="alias.external.invalid"), "DNS_NAME_OUTSIDE_ZONE")
    cases["name_apex_closed"] = name_failure(
        name_command("name-apex", name="fixture.invalid"), "DNS_NAME_OUTSIDE_ZONE")
    cases["name_stale_zone_revision_closed"] = name_failure(
        replace(name_command("name-stale"), expected_revision=0), "DNS_REVISION_CONFLICT")
    cases["name_audit_failure_rolls_back_all"] = name_failure(
        name_command("name-audit-fail", name="new.fixture.invalid"),
        "DNS_AUDIT_UNAVAILABLE", service(1))

    def policy_query(tag, name, view):
        return ResolveViewPolicy(
            "1.0.0", request("resolve_view_policy", target, platform, tag),
            target, view, name,
        )
    wanted = svc.resolve_view_policy(
        policy_query("name-query", "ALIAS.fixture.invalid.", "public"),
        operation_id="operation-name-query",
    )
    cases["name_policy_is_desired_unverified"] = (
        wanted["desired_name_present"] is True
        and wanted["desired_target_ref"] == "pixs.agent.instance:unverified-b"
        and wanted["target_verification"] == "UNVERIFIED"
        and wanted["application_status"] == "UNKNOWN"
        and wanted["measurement_status"] == "UNMEASURED"
        and wanted["applied_present"] is None and wanted["applied_revision"] is None
    )
    private_policy = svc.resolve_view_policy(
        policy_query("contract-private-view", "alias.fixture.invalid", "private"),
        operation_id="operation-contract-private-view",
    )
    cases["policy_query_view_isolation"] = (
        private_policy["view"] == "private" and wanted["view"] == "public"
        and private_policy["desired_target_ref"] == "pixs.agent.instance:unverified-a"
        and wanted["desired_target_ref"] == "pixs.agent.instance:unverified-b"
    )
    current_zone = DesiredDnsRecord.objects.get(pk=desired.pk)
    cases["policy_query_ttl_ceilings"] = (
        wanted["ttl_positive_ceiling"] == current_zone.ttl_positive == 0
        and wanted["ttl_negative_ceiling"] == current_zone.ttl_negative == 0
        and wanted["applied_present"] is None and wanted["applied_revision"] is None
    )

    def refused_policy(query_value, expected_code, operation):
        before_audit = set(CoreAuditEvent.objects.values_list("pk", flat=True))
        before = (DnsIdempotenceRecord.objects.count(), DnsNameRecord.objects.count(),
                  DesiredDnsRecord.objects.count())
        try:
            svc.resolve_view_policy(query_value, operation_id=operation)
        except DnsServiceError as error:
            # Le refus conserve son audit obligatoire après rollback, sans effet métier.
            added = list(CoreAuditEvent.objects.exclude(pk__in=before_audit)
                         .values_list("kind", "generic_payload"))
            return (error.code == expected_code and before == (
                DnsIdempotenceRecord.objects.count(), DnsNameRecord.objects.count(),
                DesiredDnsRecord.objects.count())
                and len(added) == 1 and added[0][0] == "GENERIC_AUDIT"
                and added[0][1]["result"] == "DENIED"
                and added[0][1]["reason_or_error"] == expected_code
                and added[0][1]["action"] == query_value.request.action_id
                and added[0][1]["resource_id"] == query_value.resource_id)
        return False

    cases["policy_query_unknown_view_closed"] = refused_policy(
        policy_query("contract-unknown-view", "alias.fixture.invalid", "absent-view"),
        "DNS_VIEW_UNAVAILABLE", "operation-contract-unknown-view",
    )
    cases["policy_query_outside_zone_closed"] = refused_policy(
        policy_query("contract-outside-zone", "host.other.invalid", "private"),
        "DNS_NAME_OUTSIDE_ZONE", "operation-contract-outside-zone",
    )
    denied_policy = ResolveViewPolicy(
        "1.0.0", request("resolve_view_policy", denied, platform, "contract-denied"),
        denied, "private", "alias.fixture.invalid",
    )
    cases["policy_query_permission_deny"] = refused_policy(
        denied_policy, "DNS_DENIED", "operation-contract-denied",
    )
    missing = svc.resolve_view_policy(
        policy_query("name-missing-query", "missing.fixture.invalid", "private"),
        operation_id="operation-name-missing-query",
    )
    cases["name_missing_desired_not_nxdomain"] = (
        missing["desired_name_present"] is False and missing["desired_target_ref"] is None
        and missing["application_status"] == "UNKNOWN"
        and missing["applied_present"] is None
    )
    retirement_name = name_command("name-retire", name="aLIAS.fixture.invalid.", retired=True)
    rn = svc.retire_name(retirement_name)
    name_row.refresh_from_db()
    cases["name_retirement_preserves_history"] = (
        rn.outcome == "SUCCEEDED" and name_row.business_state == "RETIRED"
        and name_row.is_current is False and name_row.persistence_state == "ACTIVE"
        and name_row.retention_state == "RETAINED" and name_row.version == 2
    )
    cases["name_retirement_replay_once"] = (
        svc.retire_name(retirement_name).replayed
        and CoreAuditEvent.objects.filter(operation_id=retirement_name.metadata.command_id).count() == 1
    )
    reassigned = svc.declare_name(name_command(
        "name-reassigned", reference="pixs.agent.instance:unverified-c"))
    cases["name_reassignment_new_history_row"] = (
        reassigned.outcome == "SUCCEEDED"
        and DnsNameRecord.objects.filter(zone=desired, name_key="alias.fixture.invalid",
                                        view="private").count() == 2
        and DnsNameRecord.objects.get(zone=desired, name_key="alias.fixture.invalid",
                                     view="private", is_current=True).pk != name_row.pk
    )
    active_zone = DesiredDnsRecord.objects.get(pk=desired.pk)
    changed_suffix = replace(
        declare(target, platform, "namespace-change"),
        expected_revision=active_zone.config_revision,
        configuration=replace(configuration(), config_revision=active_zone.config_revision + 1,
                              suffix="different.invalid"),
    )
    try:
        svc.declare_desired(changed_suffix)
    except DnsServiceError as error:
        cases["namespace_change_requires_migration"] = (
            error.code == "DNS_NAMESPACE_MIGRATION_REQUIRED"
            and DesiredDnsRecord.objects.get(pk=desired.pk).suffix == "fixture.invalid")
    else:
        cases["namespace_change_requires_migration"] = False
    changed_views = replace(
        declare(target, platform, "view-removal"),
        expected_revision=active_zone.config_revision,
        configuration=replace(configuration(), config_revision=active_zone.config_revision + 1,
                              views=("private",)),
    )
    try:
        svc.declare_desired(changed_views)
    except DnsServiceError as error:
        cases["view_removal_with_current_names_closed"] = error.code == "DNS_VIEW_IN_USE"
    else:
        cases["view_removal_with_current_names_closed"] = False
    invalid_names = ("-bad.fixture.invalid", "bad..fixture.invalid", "a" * 64 + ".invalid",
                     "é.fixture.invalid", ("a" * 63 + ".") * 4 + "invalid")
    rejected = []
    for value in invalid_names:
        try:
            dns_name_key(value)
        except ValueError:
            rejected.append(value)
    cases["dns_name_label_wire_boundaries"] = (
        len(rejected) == len(invalid_names)
        and dns_name_key("a" * 63 + ".fixture.invalid.") == "a" * 63 + ".fixture.invalid"
        and dns_name_key("Ab-C.fixture.invalid") == "ab-c.fixture.invalid"
    )


    from pixs.core.services_runtime_decider import RuntimeWaiverRequest
    from pixs.core.persistence.models_identity import CoreSuperAdminBinding
    root_before = DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
    ordinary_flags = replace(
        declare(target, platform, "ordinary-waiver-flags"), expected_revision=root_before,
        configuration=replace(configuration(), config_revision=root_before + 1),
    )
    ordinary_result = svc.declare_desired(
        ordinary_flags, waiver_request=RuntimeWaiverRequest(
            ordinary_flags.request, "default", ordinary_flags.metadata.command_id, True, True),
    )
    cases["ordinary_flags_do_not_waive_obligations"] = (
        ordinary_result.audit_disposition == "AUDITED"
        and CoreAuditEvent.objects.filter(operation_id=ordinary_flags.metadata.command_id).count() == 1
        and DesiredDnsRecord.objects.get(pk=desired.pk).governance_ref == governance_profile.data_asset_id
    )
    root_binding = CoreSuperAdminBinding.objects.create(
        installation_ref="c14-authz-install", identity_id=actor_id)
    current = DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
    root_no_flags = replace(
        declare(target, platform, "root-without-flags"), expected_revision=current,
        configuration=replace(configuration(), config_revision=current + 1),
    )
    root_result = svc.declare_desired(root_no_flags)
    cases["root_without_flags_remains_audited"] = (
        root_result.audit_disposition == "AUDITED"
        and CoreAuditEvent.objects.filter(operation_id=root_no_flags.metadata.command_id).count() == 1
        and DesiredDnsRecord.objects.get(pk=desired.pk).governance_ref == governance_profile.data_asset_id
    )

    class WaivedManagementPolicy:
        def resolve(self, *, context, alias, operation_id):
            return DnsManagementPolicy(datetime.timedelta(minutes=10), None)
    broken = service(1)
    waived_service = PostgresDnsService(
        alias="default", peer_alias="peer", store=store, clock=clock,
        audit=broken._audit, auth_factory=source, policy_source=WaivedManagementPolicy(),
    )
    current = DesiredDnsRecord.objects.get(pk=desired.pk).config_revision
    root_waived = replace(
        declare(target, platform, "root-explicit-flags"), expected_revision=current,
        configuration=replace(configuration(), config_revision=current + 1),
    )
    waivers = RuntimeWaiverRequest(
        root_waived.request, "default", root_waived.metadata.command_id, True, True)
    waived_result = waived_service.declare_desired(root_waived, waiver_request=waivers)
    waived_row = DesiredDnsRecord.objects.get(pk=desired.pk)
    cases["root_explicit_flags_waive_audit_governance"] = (
        waived_result.outcome == "SUCCEEDED" and waived_result.audit_disposition == "WAIVED"
        and waived_row.governance_ref is None and waived_row.confidentiality is None
        and waived_row.personal is None
        and CoreAuditEvent.objects.filter(operation_id=root_waived.metadata.command_id).count() == 0
    )
    waived_replay = waived_service.declare_desired(root_waived, waiver_request=waivers)
    cases["root_waived_replay_no_double_effect"] = (
        waived_replay.replayed and waived_replay.audit_disposition == "WAIVED"
        and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == waived_result.config_revision
    )
    root_binding.persistence_state = "SOFT_DELETED"
    root_binding.save(update_fields=("persistence_state",))
    try:
        waived_service.declare_desired(root_waived, waiver_request=waivers)
    except DnsServiceError as error:
        cases["revoked_root_cannot_replay_waived_result"] = (
            error.code in ("DNS_GOVERNANCE_UNAVAILABLE", "DNS_AUDIT_UNAVAILABLE")
            and DesiredDnsRecord.objects.get(pk=desired.pk).config_revision == waived_result.config_revision
        )
    else:
        cases["revoked_root_cannot_replay_waived_result"] = False


    from pixs.core.audit_contracts import AuditError
    class ContextManagementPolicy:
        def resolve(self, *, context, alias, operation_id):
            if context not in (platform, scope_a, scope_b) or alias != "default":
                raise DnsServiceError("DNS_POLICY_INVALID")
            return DnsManagementPolicy(datetime.timedelta(minutes=10), governance_profile)
    class ContextAuditPolicy:
        def resolve(self, *, context, alias):
            if context not in (platform, scope_a, scope_b) or alias != "default":
                raise AuditError()
            return AuditPolicy(
                "c14-context-audit", "1.0.0", "fixture-explicite", 1, 65536, 50, (),
                "c14-context-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL,
            )
    contextual = PostgresDnsService(
        alias="default", peer_alias="peer", store=store, clock=clock,
        audit=PostgresAuditParticipant(ContextAuditPolicy(), clock, "peer"),
        auth_factory=source, policy_source=ContextManagementPolicy(),
    )
    tenant_command = declare(tenant_target, scope_a, "tenant-management")
    tenant_result = contextual.declare_desired(tenant_command)
    tenant_row = DesiredDnsRecord.objects.get(resource_id=tenant_target, tenant_id=tenant.pk)
    cases["tenant_service_actual_scope_persisted"] = (
        tenant_result.outcome == "SUCCEEDED" and tenant_row.scope_id == first_scope.pk
        and tenant_row.scope_type == "TENANT" and tenant_row.tenant_id == tenant.pk
        and CoreAuditEvent.objects.filter(operation_id=tenant_command.metadata.command_id,
                                          tenant_id=tenant.pk, scope_id=first_scope.pk).count() == 1
    )
    wrong_scope = replace(
        declare(tenant_target, scope_b, "wrong-scope-service"),
        expected_revision=tenant_row.config_revision,
        configuration=replace(configuration(), config_revision=tenant_row.config_revision + 1),
    )
    try:
        contextual.declare_desired(wrong_scope)
    except DnsServiceError as error:
        # C04 refuse le contexte propriétaire divergent avant toute décision.
        cases["wrong_scope_cannot_modify_tenant_state"] = (
            error.code == "DNS_STATE_UNAVAILABLE"
            and DesiredDnsRecord.objects.get(pk=tenant_row.pk).config_revision == tenant_result.config_revision
            and not DnsIdempotenceRecord.objects.filter(
                idempotency_key=wrong_scope.metadata.idempotency_key).exists()
        )
    else:
        cases["wrong_scope_cannot_modify_tenant_state"] = False
    platform_command = declare(tenant_target, platform, "same-id-platform")
    platform_result = contextual.declare_desired(platform_command)
    cases["platform_and_tenant_same_resource_isolated"] = (
        platform_result.outcome == "SUCCEEDED"
        and DesiredDnsRecord.objects.filter(resource_id=tenant_target).count() == 2
        and DesiredDnsRecord.objects.get(resource_id=tenant_target, tenant_id__isnull=True).pk != tenant_row.pk
        and DesiredDnsRecord.objects.get(pk=tenant_row.pk).config_revision == tenant_result.config_revision
    )
    tenant_read = contextual.get_desired(
        query(tenant_target, scope_a, "tenant-read-service"),
        operation_id="operation-tenant-read-service",
    )
    cases["tenant_query_reads_own_revision"] = tenant_read["config_revision"] == tenant_result.config_revision

    import threading
    from django.db import connections
    locked, release, second_started, second_done = (threading.Event() for _ in range(4))
    results, errors = {}, []
    first_concurrent = replace(
        declare(tenant_target, platform, "concurrent-first"), expected_revision=1,
        configuration=replace(configuration(), config_revision=2),
    )
    second_concurrent = replace(
        declare(tenant_target, platform, "concurrent-second"), expected_revision=1,
        configuration=replace(configuration(), config_revision=2),
    )
    class HoldingPolicy(ContextManagementPolicy):
        def resolve(self, *, context, alias, operation_id):
            if operation_id == first_concurrent.metadata.command_id:
                locked.set()
                if not release.wait(10):
                    raise RuntimeError("CONCURRENCY_RELEASE_TIMEOUT")
            return super().resolve(context=context, alias=alias, operation_id=operation_id)
    held_service = PostgresDnsService(
        alias="default", peer_alias="peer", store=store, clock=clock,
        audit=PostgresAuditParticipant(ContextAuditPolicy(), clock, "peer"),
        auth_factory=source, policy_source=HoldingPolicy(),
    )
    def execute_concurrent(label, command):
        try:
            if label == "second":
                second_started.set()
            results[label] = held_service.declare_desired(command).outcome
        except DnsServiceError as error:
            results[label] = error.code
        except Exception as error:
            errors.append(error)
        finally:
            connections.close_all()
            if label == "second":
                second_done.set()
    one = threading.Thread(target=execute_concurrent, args=("first", first_concurrent))
    two = threading.Thread(target=execute_concurrent, args=("second", second_concurrent))
    one.start()
    try:
        if not locked.wait(5):
            raise RuntimeError("CONCURRENCY_LOCK_NOT_OBSERVED")
        two.start()
        if not second_started.wait(5):
            raise RuntimeError("CONCURRENCY_SECOND_NOT_STARTED")
        # B peut terminer son refus avant ou après la fermeture de la transaction A.
        second_done.wait(2)
    finally:
        release.set()
        one.join(10)
        if two.ident is not None:
            two.join(10)
    if errors:
        raise errors[0]
    cases["concurrent_commands_one_effect_closed_conflict"] = (
        not one.is_alive() and not two.is_alive()
        and results.get("first") == "SUCCEEDED"
        and results.get("second") in ("DNS_STATE_UNAVAILABLE", "DNS_REVISION_CONFLICT")
        and DesiredDnsRecord.objects.get(resource_id=tenant_target, tenant_id__isnull=True).config_revision == 2
        and DnsIdempotenceRecord.objects.filter(idempotency_key__in=(
            first_concurrent.metadata.idempotency_key, second_concurrent.metadata.idempotency_key)).count() == 1
        and CoreAuditEvent.objects.filter(operation_id=first_concurrent.metadata.command_id).count() == 1
        and not CoreAuditEvent.objects.filter(operation_id=second_concurrent.metadata.command_id,
                                             generic_payload__result="SUCCEEDED").exists()
    )

    import asyncio
    from pixs.dns.lifecycle import DnsManagementAdapter
    lifecycle = DnsManagementAdapter(service=svc, enabled=True, context=platform, capability_bound=True)
    cases["lifecycle_outside_host_closed"] = lifecycle.observe_lifecycle().ready is False
    asyncio.run(lifecycle.__aenter__())
    lifecycle_state = lifecycle.observe_lifecycle()
    cases["lifecycle_real_pg_management_ready_without_executor"] = (
        lifecycle_state.installed and lifecycle_state.enabled and lifecycle_state.configured
        and lifecycle_state.healthy and lifecycle_state.ready
        and lifecycle.observe_capabilities()[0].operable is True
        and lifecycle.execution_status()["application_status"] == "UNKNOWN"
    )
    hooks = lifecycle.build_hooks()
    hooks["configure"]()
    hooks["start"]()
    try:
        lifecycle.require_execution(owner_id="pixs.dns", target_id=target,
                                    operation="execute", config_revision=1, context=platform)
    except DnsServiceError as error:
        cases["missing_executor_operation_closed"] = error.code == "DNS_EXECUTION_UNAVAILABLE"
    else:
        cases["missing_executor_operation_closed"] = False
    try:
        lifecycle.verify_observation(proof_ref="untrusted-client-reference")
    except DnsServiceError as error:
        cases["unverified_observation_closed"] = error.code == "DNS_OBSERVATION_UNVERIFIED"
    else:
        cases["unverified_observation_closed"] = False
    asyncio.run(lifecycle.__aexit__(None, None, None))
    cases["lifecycle_exit_revokes_readiness"] = lifecycle.observe_lifecycle().ready is False
    disabled = DnsManagementAdapter(service=svc, enabled=False, context=platform, capability_bound=True)
    asyncio.run(disabled.__aenter__())
    disabled_state = disabled.observe_lifecycle()
    cases["lifecycle_enabled_separate_from_health"] = (
        disabled_state.installed and disabled_state.configured and disabled_state.healthy
        and disabled_state.enabled is False and disabled_state.ready is False)
    asyncio.run(disabled.__aexit__(None, None, None))


    # Seul l'adapter propriétaire ci-dessous est réel. Les autres composants
    # et attestations sont des doubles déclarés ; aucun P0 global n'est prouvé.
    from pathlib import Path
    from asgiref.sync import sync_to_async
    from pixs.backend.host_plan import prepare_host_plan
    from pixs.backend.host_runtime import host_runtime, HostRuntimeError
    from tests.unit.test_backend_host_plan import texts as host_fixture_texts, SyntheticProofPort, component
    from tests.unit.test_backend_host_runtime import ready_adapters
    actual_pzt = (Path(__file__).resolve().parents[2] / "src/pixs/pzt/component.toml").read_text()
    source_texts = tuple(
        actual_pzt if '\nid = "pixs.pzt"\n' in text else text
        for text in host_fixture_texts()
    )
    required = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt", "pixs.dns")
    source_texts += (component("test.c14.consumer", extra='\n[dependencies]\ncapabilities = ["dns.management ==1.0.0"]\n'),)
    plan = prepare_host_plan(
        manifest_texts=source_texts, official_ids=required + ("test.c14.consumer",), required_ids=required,
        attestation_port=SyntheticProofPort(source_texts),
    )
    class ClosingOwnedAdapter(DnsManagementAdapter):
        async def __aexit__(self, exc_type, exc, tb):
            # Connexions du thread de recette, avant sa fermeture par le runtime.
            await sync_to_async(connections.close_all, thread_sensitive=True)()
            return await super().__aexit__(exc_type, exc, tb)
    async def exercise_host(enabled):
        events = []
        bound = any(item.provider_ref == "pixs.dns"
                    and item.capability_id == "dns.management"
                    and item.capability_version == "1.0.0"
                    for item in plan.composition.capability_descriptors)
        real = ClosingOwnedAdapter(service=svc, enabled=enabled, context=platform,
                                   capability_bound=bound)
        others = ready_adapters(plan, events=events)
        selected = tuple(real if item.component_id == "pixs.dns" else item for item in others)
        try:
            async with host_runtime(plan, adapters=selected) as context:
                return (
                    context.states["pixs.dns"].ready is True
                    and sum(call.component_id == "pixs.dns" for call in context.calls) == 2
                    and not plan.composition.globally_compatible
                    and bool(plan.unevaluated_dimensions)
                )
        except HostRuntimeError as error:
            if enabled:
                raise
            return (
                error.stage == "disponibilité essentielle"
                and not any(event.startswith("hook:") for event in events)
                and real.observe_lifecycle().ready is False
            )
    cases["host_runtime_owned_pg_lifecycle_hooks"] = asyncio.run(exercise_host(True))
    cases["host_runtime_unready_essential_zero_hooks"] = asyncio.run(exercise_host(False))


    bad_audit_adapter = DnsManagementAdapter(service=service(1), enabled=True, context=platform, capability_bound=True)
    asyncio.run(bad_audit_adapter.__aenter__())
    bad_state = bad_audit_adapter.observe_lifecycle()
    cases["lifecycle_audit_unavailable_closes_management"] = (
        bad_state.installed and bad_state.enabled and bad_state.configured
        and bad_state.healthy is False and bad_state.ready is False
        and bad_audit_adapter.observe_capabilities()[0].operable is False
    )
    asyncio.run(bad_audit_adapter.__aexit__(None, None, None))

    from pixs.core.persistence.models_identity import CoreSuperAdminTenantGrant
    root_binding.persistence_state = "ACTIVE"
    root_binding.save(update_fields=("persistence_state",))
    tenant_query = query(tenant_target, scope_a, "root-tenant-without-grant")
    try:
        contextual.get_desired(tenant_query, operation_id="operation-root-tenant-without-grant")
    except DnsServiceError as error:
        cases["root_tenant_without_grant_closed"] = error.code == "DNS_DENIED"
    else:
        cases["root_tenant_without_grant_closed"] = False
    CoreSuperAdminTenantGrant.objects.create(binding=root_binding, tenant=tenant)
    tenant_query = query(tenant_target, scope_a, "root-tenant-with-grant")
    granted = contextual.get_desired(tenant_query, operation_id="operation-root-tenant-with-grant")
    cases["root_tenant_grant_current_and_audited"] = (
        granted["config_revision"] == tenant_result.config_revision
        and CoreAuditEvent.objects.filter(
            operation_id="operation-root-tenant-with-grant", tenant_id=tenant.pk).count() == 1
    )
    tenant_query = query(tenant_target, scope_a, "root-tenant-waived")
    tenant_waiver = RuntimeWaiverRequest(
        tenant_query.request, "default", "operation-root-tenant-waived", True, True)
    waived_tenant = waived_service.get_desired(
        tenant_query, operation_id="operation-root-tenant-waived", waiver_request=tenant_waiver)
    cases["root_tenant_granted_explicit_waiver"] = (
        waived_tenant["config_revision"] == tenant_result.config_revision
        and not CoreAuditEvent.objects.filter(operation_id="operation-root-tenant-waived").exists()
    )
    root_binding.persistence_state = "SOFT_DELETED"
    root_binding.save(update_fields=("persistence_state",))

    unbound = DnsManagementAdapter(service=svc, enabled=True, context=platform, capability_bound=False)
    asyncio.run(unbound.__aenter__())
    cases["lifecycle_unbound_capability_not_advertised"] = (
        unbound.observe_lifecycle().ready is True and unbound.observe_capabilities() == ())
    asyncio.run(unbound.__aexit__(None, None, None))

    return cases


def run(root_str):
    from c14_pg_test_support import run_in_c14_schema
    return run_in_c14_schema(root_str, scenarios, EXPECTED_CASES)
