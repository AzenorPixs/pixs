"""Première recette réelle du service PZT : C03/C04/C05 et mutations locales."""
from __future__ import annotations
EXPECTED_CASES = ('declare_commit_audit_idem', 'identical_replay_no_double_effect', 'cas_update_created_at_preserved', 'stale_revision_no_business_effect', 'retire_business_preserves_data_dimensions', 'audit_failure_rolls_back_all', 'divergent_replay_closed', 'expired_key_not_reexecuted', 'retirement_replay_confirmed_once', 'retirement_reason_divergence_closed', 'client_governance_not_authority', 'idempotence_policy_requires_positive_lifetime', 'lost_commit_ack_reconciled_without_double_effect', 'commit_not_sent_no_effect_or_success', 'desired_query_current_revision', 'applied_query_unknown_not_zero', 'query_current_permission_deny', 'ordinary_flags_do_not_waive_obligations', 'root_without_flags_remains_audited', 'root_explicit_flags_waive_audit_governance', 'root_waived_replay_no_double_effect', 'revoked_root_cannot_replay_waived_result', 'tenant_service_actual_scope_persisted', 'wrong_scope_cannot_modify_tenant_state', 'platform_and_tenant_same_resource_isolated', 'tenant_query_reads_own_revision', 'concurrent_commands_one_effect_closed_conflict', 'lifecycle_outside_host_closed', 'lifecycle_real_pg_management_ready_without_executor', 'missing_executor_operation_closed', 'unverified_observation_closed', 'lifecycle_exit_revokes_readiness', 'lifecycle_enabled_separate_from_health', 'host_runtime_owned_pg_lifecycle_hooks', 'host_runtime_unready_essential_zero_hooks', 'lifecycle_audit_unavailable_closes_management', 'root_tenant_without_grant_closed', 'root_tenant_grant_current_and_audited', 'root_tenant_granted_explicit_waiver', 'lifecycle_unbound_capability_not_advertised')

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


    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.pzt.models import PztIdempotenceRecord
    from pixs.pzt.services import PostgresPztService, PztManagementPolicy, PztServiceError
    from dataclasses import replace

    governance_profile = configuration().governance

    class ManagementPolicy:
        def resolve(self, *, context, alias, operation_id):
            if context != platform or alias != "default":
                raise PztServiceError("PZT_POLICY_INVALID")
            # Durée explicite de fixture, aucune valeur de production déduite.
            return PztManagementPolicy(datetime.timedelta(minutes=10), governance_profile)

    def source(*, request, alias, operation_id):
        if alias != "default":
            raise PztServiceError("PZT_AUTH_UNAVAILABLE")
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
        return PostgresPztService(
            alias="default", peer_alias="peer", store=store, clock=clock,
            audit=audit, auth_factory=source, policy_source=ManagementPolicy(),
        )

    svc = service(65536)
    first = declare(target, platform, "service-first")
    result = svc.declare_desired(first)
    desired = DesiredPztRecord.objects.get(resource_id=target, tenant_id__isnull=True)
    idem = PztIdempotenceRecord.objects.get(
        tenant_id__isnull=True, subject_id=actor, command_type="declare_desired_pzt",
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
        and DesiredPztRecord.objects.count() == 1
        and PztIdempotenceRecord.objects.count() == 1
        and CoreAuditEvent.objects.count() == initial_audits
    )
    update = declare(target, platform, "service-update")
    update = replace(
        update, expected_revision=1,
        configuration=replace(configuration(), config_revision=2, v6_enabled=True),
    )
    updated = svc.declare_desired(update)
    desired.refresh_from_db()
    cases["cas_update_created_at_preserved"] = (
        updated.outcome == "SUCCEEDED" and desired.config_revision == 2
        and desired.version == 2 and desired.v6_enabled
        and desired.created_at == created_at
    )
    stale = declare(target, platform, "service-stale")
    try:
        svc.declare_desired(stale)
    except PztServiceError as error:
        cases["stale_revision_no_business_effect"] = (
            error.code == "PZT_REVISION_CONFLICT"
            and DesiredPztRecord.objects.get(pk=desired.pk).config_revision == 2
            and not PztIdempotenceRecord.objects.filter(
                idempotency_key=stale.metadata.idempotency_key).exists()
        )
    else:
        cases["stale_revision_no_business_effect"] = False

    retirement_request = request("retire_desired_pzt", target, platform, "service-retire")
    retirement_metadata = CommandMetadata(
        "operation-service-retire", (retirement_request.correlation_id,), (), platform,
        "retire_desired_pzt", actor, "idempotence-service-retire",
    )
    retirement = RetireDesiredPzt(
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
    counts = (DesiredPztRecord.objects.count(), PztIdempotenceRecord.objects.count(),
              CoreAuditEvent.objects.count())
    # C05 réel refuse la taille de l'événement ; aucun mock de son participant.
    broken_audit_service = service(1)
    try:
        broken_audit_service.declare_desired(failing)
    except PztServiceError as error:
        cases["audit_failure_rolls_back_all"] = (
            error.code == "PZT_AUDIT_UNAVAILABLE"
            and not DesiredPztRecord.objects.filter(resource_id=absent).exists()
            and not PztIdempotenceRecord.objects.filter(
                idempotency_key=failing.metadata.idempotency_key).exists()
            and counts == (DesiredPztRecord.objects.count(), PztIdempotenceRecord.objects.count(),
                           CoreAuditEvent.objects.count())
        )
    else:
        cases["audit_failure_rolls_back_all"] = False

    # Les refus de contenu ne doivent jamais être remplacés par une erreur CAS.
    divergent = replace(first, configuration=replace(first.configuration, v6_enabled=True))
    try:
        svc.declare_desired(divergent)
    except PztServiceError as error:
        cases["divergent_replay_closed"] = (
            error.code == "PZT_IDEMPOTENCE_CONFLICT"
            and DesiredPztRecord.objects.get(pk=desired.pk).config_revision == 3
        )
    else:
        cases["divergent_replay_closed"] = False

    old_expires = PztIdempotenceRecord.objects.get(pk=idem.pk).expires_at
    PztIdempotenceRecord.objects.filter(pk=idem.pk).update(
        expires_at=now-datetime.timedelta(seconds=1))
    try:
        try:
            svc.declare_desired(replay)
        except PztServiceError as error:
            cases["expired_key_not_reexecuted"] = (
                error.code == "PZT_IDEMPOTENCE_EXPIRED"
                and DesiredPztRecord.objects.get(pk=desired.pk).config_revision == 3
                and PztIdempotenceRecord.objects.filter(pk=idem.pk).count() == 1
            )
        else:
            cases["expired_key_not_reexecuted"] = False
    finally:
        PztIdempotenceRecord.objects.filter(pk=idem.pk).update(expires_at=old_expires)

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
    except PztServiceError as error:
        cases["retirement_reason_divergence_closed"] = (
            error.code == "PZT_IDEMPOTENCE_CONFLICT"
            and DesiredPztRecord.objects.get(pk=desired.pk).config_revision == 3
        )
    else:
        cases["retirement_reason_divergence_closed"] = False

    spoof = declare(absent, platform, "governance-spoof")
    spoof = replace(spoof, configuration=replace(
        spoof.configuration, governance=replace(governance_profile, data_asset_id="other-asset")))
    try:
        svc.declare_desired(spoof)
    except PztServiceError as error:
        cases["client_governance_not_authority"] = (
            error.code == "PZT_GOVERNANCE_INVALID"
            and not DesiredPztRecord.objects.filter(resource_id=absent).exists()
        )
    else:
        cases["client_governance_not_authority"] = False
    try:
        PztManagementPolicy(datetime.timedelta(), governance_profile)
    except PztServiceError as error:
        cases["idempotence_policy_requires_positive_lifetime"] = error.code == "PZT_POLICY_INVALID"
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
    committed_idem = PztIdempotenceRecord.objects.using("peer").get(
        subject_id=actor, command_type="declare_desired_pzt",
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
        and DesiredPztRecord.objects.filter(resource_id=absent).count() == 1
        and PztIdempotenceRecord.objects.filter(pk=committed_idem.pk).count() == 1
        and CoreAuditEvent.objects.filter(operation_id=lost_command.metadata.command_id).count() == 1
    )
    uncommitted = declare(tenant_target, platform, "uncommitted-error")
    def commit_not_sent():
        raise DatabaseError("fixture_commit_not_sent")
    with patch.object(owner_connection, "commit", side_effect=commit_not_sent):
        unknown = svc.declare_desired(uncommitted)
    cases["commit_not_sent_no_effect_or_success"] = (
        unknown.outcome == "UNKNOWN" and unknown.audit_disposition == "UNKNOWN"
        and not DesiredPztRecord.objects.filter(resource_id=tenant_target).exists()
        and not PztIdempotenceRecord.objects.filter(
            idempotency_key=uncommitted.metadata.idempotency_key).exists()
        and not CoreAuditEvent.objects.filter(operation_id=uncommitted.metadata.command_id).exists()
    )


    from pixs.pzt.contracts import GetDesiredPzt, GetAppliedPzt
    query_request = request("get_desired_pzt", target, platform, "query-desired")
    before_idempotence = PztIdempotenceRecord.objects.count()
    wanted = svc.get_desired(
        GetDesiredPzt("1.0.0", query_request, target), operation_id="query-desired-operation",
    )
    cases["desired_query_current_revision"] = (
        wanted["config_revision"] == DesiredPztRecord.objects.get(pk=desired.pk).config_revision
        and wanted["business_state"] == "RETIRED"
        and wanted["configuration"]["owner_id"] == "pixs.pzt"
    )
    applied_request = request("get_applied_pzt", target, platform, "query-applied")
    observed = svc.get_applied(
        GetAppliedPzt("1.0.0", applied_request, target), operation_id="query-applied-operation",
    )
    cases["applied_query_unknown_not_zero"] = (
        observed["application_status"] == "UNKNOWN"
        and observed["measurement_status"] == "UNMEASURED"
        and all(observed[name] is None for name in (
            "applied_revision", "applied_present", "generation",
            "observed_at", "valid_until", "measurements"))
        and PztIdempotenceRecord.objects.count() == before_idempotence
    )
    fixture_values = {
        field.attname: getattr(desired, field.attname)
        for field in desired._meta.concrete_fields if not field.primary_key
    }
    fixture_values["resource_id"] = denied
    denied_row = DesiredPztRecord(**fixture_values)
    denied_row.full_clean()
    denied_row.save()
    denied_request = request("get_desired_pzt", denied, platform, "query-denied")
    try:
        svc.get_desired(
            GetDesiredPzt("1.0.0", denied_request, denied),
            operation_id="query-denied-operation",
        )
    except PztServiceError as error:
        cases["query_current_permission_deny"] = error.code == "PZT_DENIED"
    else:
        cases["query_current_permission_deny"] = False


    from pixs.core.services_runtime_decider import RuntimeWaiverRequest
    from pixs.core.persistence.models_identity import CoreSuperAdminBinding
    root_before = DesiredPztRecord.objects.get(pk=desired.pk).config_revision
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
        and DesiredPztRecord.objects.get(pk=desired.pk).governance_ref == governance_profile.data_asset_id
    )
    root_binding = CoreSuperAdminBinding.objects.create(
        installation_ref="c14-authz-install", identity_id=actor_id)
    current = DesiredPztRecord.objects.get(pk=desired.pk).config_revision
    root_no_flags = replace(
        declare(target, platform, "root-without-flags"), expected_revision=current,
        configuration=replace(configuration(), config_revision=current + 1),
    )
    root_result = svc.declare_desired(root_no_flags)
    cases["root_without_flags_remains_audited"] = (
        root_result.audit_disposition == "AUDITED"
        and CoreAuditEvent.objects.filter(operation_id=root_no_flags.metadata.command_id).count() == 1
        and DesiredPztRecord.objects.get(pk=desired.pk).governance_ref == governance_profile.data_asset_id
    )

    class WaivedManagementPolicy:
        def resolve(self, *, context, alias, operation_id):
            return PztManagementPolicy(datetime.timedelta(minutes=10), None)
    broken = service(1)
    waived_service = PostgresPztService(
        alias="default", peer_alias="peer", store=store, clock=clock,
        audit=broken._audit, auth_factory=source, policy_source=WaivedManagementPolicy(),
    )
    current = DesiredPztRecord.objects.get(pk=desired.pk).config_revision
    root_waived = replace(
        declare(target, platform, "root-explicit-flags"), expected_revision=current,
        configuration=replace(configuration(), config_revision=current + 1),
    )
    waivers = RuntimeWaiverRequest(
        root_waived.request, "default", root_waived.metadata.command_id, True, True)
    waived_result = waived_service.declare_desired(root_waived, waiver_request=waivers)
    waived_row = DesiredPztRecord.objects.get(pk=desired.pk)
    cases["root_explicit_flags_waive_audit_governance"] = (
        waived_result.outcome == "SUCCEEDED" and waived_result.audit_disposition == "WAIVED"
        and waived_row.governance_ref is None and waived_row.confidentiality is None
        and waived_row.personal is None
        and CoreAuditEvent.objects.filter(operation_id=root_waived.metadata.command_id).count() == 0
    )
    waived_replay = waived_service.declare_desired(root_waived, waiver_request=waivers)
    cases["root_waived_replay_no_double_effect"] = (
        waived_replay.replayed and waived_replay.audit_disposition == "WAIVED"
        and DesiredPztRecord.objects.get(pk=desired.pk).config_revision == waived_result.config_revision
    )
    root_binding.persistence_state = "SOFT_DELETED"
    root_binding.save(update_fields=("persistence_state",))
    try:
        waived_service.declare_desired(root_waived, waiver_request=waivers)
    except PztServiceError as error:
        cases["revoked_root_cannot_replay_waived_result"] = (
            error.code in ("PZT_GOVERNANCE_UNAVAILABLE", "PZT_AUDIT_UNAVAILABLE")
            and DesiredPztRecord.objects.get(pk=desired.pk).config_revision == waived_result.config_revision
        )
    else:
        cases["revoked_root_cannot_replay_waived_result"] = False


    from pixs.core.audit_contracts import AuditError
    class ContextManagementPolicy:
        def resolve(self, *, context, alias, operation_id):
            if context not in (platform, scope_a, scope_b) or alias != "default":
                raise PztServiceError("PZT_POLICY_INVALID")
            return PztManagementPolicy(datetime.timedelta(minutes=10), governance_profile)
    class ContextAuditPolicy:
        def resolve(self, *, context, alias):
            if context not in (platform, scope_a, scope_b) or alias != "default":
                raise AuditError()
            return AuditPolicy(
                "c14-context-audit", "1.0.0", "fixture-explicite", 1, 65536, 50, (),
                "c14-context-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL,
            )
    contextual = PostgresPztService(
        alias="default", peer_alias="peer", store=store, clock=clock,
        audit=PostgresAuditParticipant(ContextAuditPolicy(), clock, "peer"),
        auth_factory=source, policy_source=ContextManagementPolicy(),
    )
    tenant_command = declare(tenant_target, scope_a, "tenant-management")
    tenant_result = contextual.declare_desired(tenant_command)
    tenant_row = DesiredPztRecord.objects.get(resource_id=tenant_target, tenant_id=tenant.pk)
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
    except PztServiceError as error:
        # C04 refuse le contexte propriétaire divergent avant toute décision.
        cases["wrong_scope_cannot_modify_tenant_state"] = (
            error.code == "PZT_STATE_UNAVAILABLE"
            and DesiredPztRecord.objects.get(pk=tenant_row.pk).config_revision == tenant_result.config_revision
            and not PztIdempotenceRecord.objects.filter(
                idempotency_key=wrong_scope.metadata.idempotency_key).exists()
        )
    else:
        cases["wrong_scope_cannot_modify_tenant_state"] = False
    platform_command = declare(tenant_target, platform, "same-id-platform")
    platform_result = contextual.declare_desired(platform_command)
    cases["platform_and_tenant_same_resource_isolated"] = (
        platform_result.outcome == "SUCCEEDED"
        and DesiredPztRecord.objects.filter(resource_id=tenant_target).count() == 2
        and DesiredPztRecord.objects.get(resource_id=tenant_target, tenant_id__isnull=True).pk != tenant_row.pk
        and DesiredPztRecord.objects.get(pk=tenant_row.pk).config_revision == tenant_result.config_revision
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
    held_service = PostgresPztService(
        alias="default", peer_alias="peer", store=store, clock=clock,
        audit=PostgresAuditParticipant(ContextAuditPolicy(), clock, "peer"),
        auth_factory=source, policy_source=HoldingPolicy(),
    )
    def execute_concurrent(label, command):
        try:
            if label == "second":
                second_started.set()
            results[label] = held_service.declare_desired(command).outcome
        except PztServiceError as error:
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
        and results.get("second") in ("PZT_STATE_UNAVAILABLE", "PZT_REVISION_CONFLICT")
        and DesiredPztRecord.objects.get(resource_id=tenant_target, tenant_id__isnull=True).config_revision == 2
        and PztIdempotenceRecord.objects.filter(idempotency_key__in=(
            first_concurrent.metadata.idempotency_key, second_concurrent.metadata.idempotency_key)).count() == 1
        and CoreAuditEvent.objects.filter(operation_id=first_concurrent.metadata.command_id).count() == 1
        and not CoreAuditEvent.objects.filter(operation_id=second_concurrent.metadata.command_id,
                                             generic_payload__result="SUCCEEDED").exists()
    )

    import asyncio
    from pixs.pzt.lifecycle import PztManagementAdapter
    lifecycle = PztManagementAdapter(service=svc, enabled=True, context=platform, capability_bound=True)
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
        lifecycle.require_execution(owner_id="pixs.pzt", target_id=target,
                                    operation="execute", config_revision=1, context=platform)
    except PztServiceError as error:
        cases["missing_executor_operation_closed"] = error.code == "PZT_EXECUTION_UNAVAILABLE"
    else:
        cases["missing_executor_operation_closed"] = False
    try:
        lifecycle.verify_observation(proof_ref="untrusted-client-reference")
    except PztServiceError as error:
        cases["unverified_observation_closed"] = error.code == "PZT_OBSERVATION_UNVERIFIED"
    else:
        cases["unverified_observation_closed"] = False
    asyncio.run(lifecycle.__aexit__(None, None, None))
    cases["lifecycle_exit_revokes_readiness"] = lifecycle.observe_lifecycle().ready is False
    disabled = PztManagementAdapter(service=svc, enabled=False, context=platform, capability_bound=True)
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
    source_texts += (component("test.c14.consumer", extra='\n[dependencies]\ncapabilities = ["pzt.management ==1.0.0"]\n'),)
    plan = prepare_host_plan(
        manifest_texts=source_texts, official_ids=required + ("test.c14.consumer",), required_ids=required,
        attestation_port=SyntheticProofPort(source_texts),
    )
    class ClosingOwnedAdapter(PztManagementAdapter):
        async def __aexit__(self, exc_type, exc, tb):
            # Connexions du thread de recette, avant sa fermeture par le runtime.
            await sync_to_async(connections.close_all, thread_sensitive=True)()
            return await super().__aexit__(exc_type, exc, tb)
    async def exercise_host(enabled):
        events = []
        bound = any(item.provider_ref == "pixs.pzt"
                    and item.capability_id == "pzt.management"
                    and item.capability_version == "1.0.0"
                    for item in plan.composition.capability_descriptors)
        real = ClosingOwnedAdapter(service=svc, enabled=enabled, context=platform,
                                   capability_bound=bound)
        others = ready_adapters(plan, events=events)
        selected = tuple(real if item.component_id == "pixs.pzt" else item for item in others)
        try:
            async with host_runtime(plan, adapters=selected) as context:
                return (
                    context.states["pixs.pzt"].ready is True
                    and sum(call.component_id == "pixs.pzt" for call in context.calls) == 2
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


    bad_audit_adapter = PztManagementAdapter(service=service(1), enabled=True, context=platform, capability_bound=True)
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
    except PztServiceError as error:
        cases["root_tenant_without_grant_closed"] = error.code == "PZT_DENIED"
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

    unbound = PztManagementAdapter(service=svc, enabled=True, context=platform, capability_bound=False)
    asyncio.run(unbound.__aenter__())
    cases["lifecycle_unbound_capability_not_advertised"] = (
        unbound.observe_lifecycle().ready is True and unbound.observe_capabilities() == ())
    asyncio.run(unbound.__aexit__(None, None, None))

    return cases


def run(root_str):
    from c14_pg_test_support import run_in_c14_schema
    return run_in_c14_schema(root_str, scenarios, EXPECTED_CASES)
