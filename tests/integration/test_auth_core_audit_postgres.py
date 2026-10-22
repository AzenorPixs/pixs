"""Recette commune Auth/Core/C04/C05 réels ; plan et classification C08/C10 fixtures."""
from __future__ import annotations

EXPECTED_CASES = ("core_fact_auth_real", "core_suspension_seen", "r01_preadmission_without_target", "r01_real_allow", "r01_real_target_stamp", "r01_final_snapshot_stable", "r01_uncommitted_invisible_peer", "r01_common_commit_audit", "r01_audit_failure_rollback", "r01_bad_signature_deny", "r01_denial_audited", "r01_no_session_or_waiver", "r01_consumed_inspection_only", "r01_plan_substitution_deny", "composite_real_provider", "composite_preadmission_then_owner", "composite_final_revalidation", "composite_auth_metadata", "composite_freshness_real", "composite_audit_common", "composite_revocation_seen")


def scenarios():
    import datetime
    import hashlib
    import json
    import secrets
    from dataclasses import replace
    from django.db import transaction
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    from pixs.auth import models as m
    from pixs.auth.identifiers import new_uuid7, identity_reference, parse_identity_reference
    from pixs.auth.passwords import hash_password
    from pixs.auth.policy import SessionCategory
    from pixs.auth.runtime_verifier import LocalTrustProfile, prepare_password_verifier, AuthVerificationError
    from pixs.auth.invocation import AuthInvocationSource
    from pixs.auth.bootstrap_backend import (AuthBootstrapBackend, AuthBootstrapBackendError, PreparedBootstrapCredential, prepared_credential_digest, BootstrapAuthClassification)
    from pixs.auth.r01 import (BootstrapTrustKey, BootstrapTrustPolicy, SignedBootstrapProof, canonical_bootstrap_bytes, bootstrap_challenge_sha256)
    from pixs.core.bootstrap_operator import BootstrapOperatorFacts, BOOTSTRAP_ACTION
    from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec, CommandEnvelope
    from pixs.core.identity.models import IdentityType, IdentityState
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.query_source import CoreFactSource
    from pixs.core.ports import CorePortError, TransactionProof
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.authz.ports import Request, AuditEvent
    from pixs.core.authz.policy import Effect, IdentityAssurance, FederationTrust
    from pixs.core.services_runtime_bootstrap import RuntimeBootstrapDecider
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

    cases = {}
    ctx = ScopeContext(ScopeType.PLATFORM)
    start = datetime.datetime.now(datetime.timezone.utc)
    class Clock:
        def now(self):
            return start
    clock = Clock()
    real_facts = CoreFactSource()
    password_hash = hash_password("Vecteur public commun C03, aucun secret réel")
    actor_id = new_uuid7()
    actor = identity_reference(actor_id)
    CoreIdentity.objects.create(identity_id=actor_id, identity_type="HUMAN", state="ACTIVE")
    gate = m.AuthAccountGate.objects.create(identity_id=actor_id)
    binding = m.AuthBinding.objects.create(identity=gate, provider_id="local-test", issuer="fixture-common", external_subject="actor-common", enabled=True)
    m.AuthPasswordCredential.objects.create(binding=binding, password_hash=password_hash, enabled=True)
    m.AuthPolicyRow.objects.create(policy_id="common-test", policy_version="1.0.0", origin="fixture-explicite", scope_type="PLATFORM", category="ORDINARY", idle_seconds=600, absolute_seconds=3600, access_seconds=300, freshness_seconds=120, max_sessions=3, is_current=True)
    profile = LocalTrustProfile("common-test", "1.0.0", binding.provider_id, binding.issuer, FederationTrust.TRUSTED)
    class LocalTrust:
        def resolve(self, profile_id, request, *, alias, operation_id):
            return profile
    class Assurance:
        def resolve(self, identity_ref, request, *, alias, operation_id):
            return IdentityAssurance.CLAIMED
    req = Request("common-decision", actor, actor, "pixs.auth.session.create", ctx, "common-correlation")
    source = AuthInvocationSource(prepare_password_verifier(request=req, alias="default", operation_id="common-op", profile=profile, trust_source=LocalTrust(), assurance_source=Assurance(), facts_reader=real_facts, clock=clock, external_subject=binding.external_subject, password="Vecteur public commun C03, aucun secret réel", category=SessionCategory.ORDINARY))
    authentication, status = source.revalidate(req, alias="default", operation_id="common-op")
    cases["core_fact_auth_real"] = authentication.digital_identity_id == actor and authentication.identity_assurance is IdentityAssurance.CLAIMED
    try:
        CoreIdentity.objects.filter(pk=actor_id).update(state="SUSPENDED", version=2)
        try:
            source.revalidate(req, alias="default", operation_id="common-op")
        except AuthVerificationError:
            cases["core_suspension_seen"] = True
        else:
            cases["core_suspension_seen"] = False
    finally:
        CoreIdentity.objects.filter(pk=actor_id).update(state="ACTIVE", version=1)
        source.close()

    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.authz.policy import Policy, Selector, ScopeSelector, Obligation
    from pixs.core.authz.ports import PortError
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_common import CoreServiceError
    composite_req = Request("composite-decision", actor, actor, "pixs.auth.session.create", ctx, "composite-correlation")
    composite_op = "composite-operation"
    source = AuthInvocationSource(prepare_password_verifier(request=composite_req, alias="default", operation_id=composite_op, profile=profile, trust_source=LocalTrust(), assurance_source=Assurance(), facts_reader=real_facts, clock=clock, external_subject=binding.external_subject, password="Vecteur public commun C03, aucun secret réel", category=SessionCategory.ORDINARY))
    account_ref = "pixs.auth.account:"+str(actor_id)
    catalog = Catalog((actor,), (actor, account_ref), (composite_req.action_id,), (ctx,), ())
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    declared = Policy("common-composite-policy", "1.0.0", "pixs.auth", Effect.ALLOW, Selector("subject", (actor,)), Selector("resource", (actor, account_ref)), Selector("action", (composite_req.action_id,)), ScopeSelector((ctx,)), obligations=(Obligation("AUDIT"),))
    CorePolicy.objects.create(policy_id=declared.policy_id, policy_version=declared.policy_version, owner=declared.owner, effect=declared.effect.value, definition=encode_policy(declared))
    store = CoreAuthorizationStore(alias="default", installation_ref="common-ordinary-install", base_epoch="common-composite-v1", catalog=catalog, limits=limits)
    provider = RuntimeTrustedFactsProvider(store=store, authentication_source=source, request=composite_req, operation_id=composite_op, additional_owners=(RuntimeResourceOwner("pixs.auth.", source.ownership),))
    decider = RuntimeAuthorizationDecider(store=store, facts_provider=provider, clock=clock, request=composite_req, operation_id=composite_op)
    try:
        pre = provider.resolve(composite_req)
        cases["composite_real_provider"] = pre.auth.digital_identity_id == actor and pre.ownership.resource_id == actor
        outside = decider.decide(composite_req)
        with transaction.atomic(durable=True):
            decider.prepare_core_under_locks(composite_req, "default", composite_op)
            decision = decider.revalidate_under_locks(composite_req, alias="default", operation_id=composite_op)
            cases["composite_preadmission_then_owner"] = outside.effect is decision.effect is Effect.ALLOW
            actual = provider.resolve(replace(composite_req, decision_id="candidate-account", resource_id=account_ref))
            cases["composite_auth_metadata"] = actual.ownership.resource_id == account_ref and actual.ownership.context == ctx and actual.auth.digital_identity_id == actor
            auth_current = provider.resolve(composite_req).auth
            cases["composite_freshness_real"] = decider.verify_auth_freshness(composite_req, decision, alias="default", operation_id=composite_op, authenticated_at=auth_current.authentication_time, max_age_seconds=120) is None
            # Le C05 réel est déclaré plus bas ; sa construction ne dépend d'aucun double Auth.
            ap = AuditPolicy("composite-audit", "1.0.0", "fixture-explicite", 1, 65536, 50, (), "composite-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
            participant = PostgresAuditParticipant(ExplicitAuditPolicySource(ctx, ap), clock, "peer")
            event = AuditEvent(composite_req.decision_id, actor, actor, composite_req.action_id, ctx, composite_req.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, start)
            stage = participant.stage(event, alias="default", operation_id=composite_op, transaction_token="composite-tx", context=ctx, decision=decision)
            participant.verify_staged(TransactionProof(composite_op, "default", "composite-tx", ctx, (stage,), start))
            final = decider.revalidate_under_locks(composite_req, alias="default", operation_id=composite_op)
            cases["composite_final_revalidation"] = final.effect is Effect.ALLOW and final.policy_version == decision.policy_version
        cases["composite_audit_common"] = CoreAuditEvent.objects.using("peer").filter(operation_id=composite_op).count() == 1
        try:
            CoreIdentity.objects.filter(pk=actor_id).update(state="SUSPENDED", version=2)
            try:
                provider.resolve(composite_req)
            except (PortError, CorePortError, CoreServiceError):
                cases["composite_revocation_seen"] = True
            else:
                cases["composite_revocation_seen"] = False
        finally:
            CoreIdentity.objects.filter(pk=actor_id).update(state="ACTIVE", version=1)
    finally:
        source.close()

    signer = Ed25519PrivateKey.generate()
    public = signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    classification = BootstrapAuthClassification("auth-common-asset", ConfidentialityLevel.CONFIDENTIAL, PersonalDataLevel.PERSONAL)
    class Classification:
        def resolve(self, *, context, alias, operation_id):
            return classification
    def audit(max_bytes=65536):
        policy = AuditPolicy("common-audit", "1.0.0", "fixture-explicite", 1, max_bytes, 50, (), "audit-common-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
        return PostgresAuditParticipant(ExplicitAuditPolicySource(ctx, policy), clock, "peer")

    def fixture(label):
        target_id = new_uuid7()
        target = identity_reference(target_id)
        prepared = PreparedBootstrapCredential("local-test", "fixture-common", "target-"+label, password_hash)
        manifest = {"target": target, "effects": ["CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"], "installation": "common-install", "version": "1.0.0", "credential_digest": prepared_credential_digest(prepared)}
        def digest():
            return hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest()
        facts = BootstrapOperatorFacts("operator-common", "pixs.core.bootstrap:common-install", BOOTSTRAP_ACTION, ctx, "common-install", "1.0.0", (BOOTSTRAP_ACTION,), tuple(manifest["effects"]), "proof-"+label, "authorization-"+label, "operation-"+label, target, None, digest(), start, start+datetime.timedelta(seconds=600), "common-key", "1.0.0", None)
        nonce = secrets.token_bytes(32)
        signed = SignedBootstrapProof(facts, nonce, signer.sign(canonical_bootstrap_bytes(facts, nonce)))
        policy = BootstrapTrustPolicy("1.0.0", (BootstrapTrustKey("common-key", facts.operator_subject_ref, facts.installation_ref, facts.authorized_actions, public, start-datetime.timedelta(days=1), start+datetime.timedelta(days=1), False),))
        class Proofs:
            value = signed
            def resolve(self, ref):
                if ref != facts.operator_proof_ref:
                    raise CorePortError()
                return self.value
        class Trust:
            def resolve(self, version):
                return policy
        row = m.AuthBootstrapAuthorization.objects.create(authorization_ref=facts.authorization_ref, operator_proof_ref=facts.operator_proof_ref, operator_subject_ref=facts.operator_subject_ref, installation_ref=facts.installation_ref, plan_version=facts.plan_version, plan_sha256=facts.plan_sha256, operation_ref=facts.operation_id, target_identity_ref=target, closed_effects=list(facts.closed_effects), authorized_actions=list(facts.authorized_actions), key_id=facts.key_id, trust_policy_version=facts.trust_policy_version, challenge_sha256=bootstrap_challenge_sha256(facts, nonce), credential_prepared_digest=prepared_credential_digest(prepared), valid_from=start, expires_at=facts.expires_at)
        request = Request(facts.authorization_ref, facts.operator_subject_ref, facts.resource_id, facts.action_id, ctx, "correlation-"+label)
        act = BootstrapActInput(facts.operation_id, facts.plan_version, facts.installation_ref, "INSTALLER", facts.operator_proof_ref, facts.operator_subject_ref, facts.authorization_ref, target, None, facts.closed_effects, ("CONFIRMED",), ctx, request.correlation_id, None, "idem-"+label, facts.plan_sha256, "1.0.0")
        envelope = CommandEnvelope(request, act.operation_id, act.idempotency_key, act.content_sha256, act.serializer_version, act.correlation_id, None)
        class Plans:
            confirmed = None
            def verify_plan(self, supplied, *, alias):
                if supplied != act or digest() != facts.plan_sha256:
                    raise CorePortError()
            def verify_operator_binding(self, supplied, candidate, *, alias):
                self.verify_plan(supplied, alias=alias)
                if replace(candidate, consumed_operation_id=None) != facts or candidate.plan_sha256 != digest():
                    raise CorePortError()
            def get_closed_effects(self, *, plan_version, installation_ref):
                if (plan_version, installation_ref) != (facts.plan_version, facts.installation_ref):
                    raise CorePortError()
                return tuple(manifest["effects"])
            def resolve_targets(self, supplied, *, alias):
                self.verify_plan(supplied, alias=alias)
                return BootstrapTargetSpec(target_id, IdentityType.HUMAN, IdentityState.ACTIVE, None, None, None, None)
            def inspect_confirmed(self, supplied):
                return self.confirmed
        proofs, plans = Proofs(), Plans()
        def backend(prepared_value=prepared):
            return AuthBootstrapBackend(alias="default", proofs=proofs, trust=Trust(), facts_reader=real_facts, classification_source=Classification(), clock=clock, prepared=prepared_value)
        b = backend()
        d = RuntimeBootstrapDecider(act=act, envelope=envelope, alias="default", operator=b, plans=plans, clock=clock)
        return dict(facts=facts, row=row, request=request, act=act, backend=b, backend_factory=backend, decider=d, plans=plans, proofs=proofs, manifest=manifest, envelope=envelope, target_id=target_id)

    def under(item):
        return item["decider"].revalidate_under_locks(item["request"], alias="default", operation_id=item["facts"].operation_id)
    def stages(item, participant, *, commit_cases=False):
        facts, request, b = item["facts"], item["request"], item["backend"]
        decision = under(item)
        if decision.effect is not Effect.ALLOW:
            raise AssertionError("R01_ALLOW_REQUIRED")
        CoreIdentity.objects.create(identity_id=item["target_id"], identity_type="HUMAN", state="ACTIVE", **classification.values())
        token = "tx-"+facts.operation_id
        cred = b.stamp(alias="default", operation_id=facts.operation_id, transaction_token=token, target_identity_ref=facts.target_identity_ref, context=ctx)
        if commit_cases:
            cases["r01_real_target_stamp"] = m.AuthPasswordCredential.objects.filter(binding__identity_id=item["target_id"]).exists() and real_facts.read_facts("IDENTITY", (facts.target_identity_ref,), ctx, "default", 1)[0].ref == facts.target_identity_ref
        event = AuditEvent(request.decision_id, request.subject_id, request.resource_id, request.action_id, ctx, request.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, start)
        audited = participant.stage(event, alias="default", operation_id=facts.operation_id, transaction_token=token, context=ctx, decision=decision)
        proof = TransactionProof(facts.operation_id, "default", token, ctx, (cred, audited), start)
        b.verify_staged(proof)
        participant.verify_staged(proof)
        final = under(item)
        if final.effect is not Effect.ALLOW or final.policy_version != decision.policy_version:
            raise AssertionError("FINAL_VERSION_CHANGED")
        if commit_cases:
            cases["r01_final_snapshot_stable"] = True
            cases["r01_uncommitted_invisible_peer"] = not CoreIdentity.objects.using("peer").filter(pk=item["target_id"]).exists() and not CoreAuditEvent.objects.using("peer").filter(operation_id=facts.operation_id).exists()
        return decision

    item = fixture("common-success")
    decision = item["decider"].decide(item["request"])
    cases["r01_preadmission_without_target"] = decision.effect is Effect.ALLOW and not CoreIdentity.objects.filter(pk=item["target_id"]).exists() and not m.AuthAccountGate.objects.filter(pk=item["target_id"]).exists()
    with transaction.atomic(durable=True):
        decision = stages(item, audit(), commit_cases=True)
        cases["r01_real_allow"] = decision.effect is Effect.ALLOW
    item["row"].refresh_from_db()
    confirmed = CoreIdentity.objects.using("peer").filter(pk=item["target_id"]).exists() and m.AuthAccountGate.objects.using("peer").filter(pk=item["target_id"]).exists() and CoreAuditEvent.objects.using("peer").filter(operation_id=item["facts"].operation_id, kind="PDP_AUDIT").count() == 1
    cases["r01_common_commit_audit"] = confirmed and item["row"].consumed_operation_ref == item["facts"].operation_id
    cases["r01_no_session_or_waiver"] = m.AuthSession.objects.count() == 0 and item["decider"].audit_waived(item["request"], decision, alias="default", operation_id=item["facts"].operation_id) is False and item["decider"].governance_waived(item["request"], decision, alias="default", operation_id=item["facts"].operation_id) is False
    item["backend"].close()
    inspector = item["backend_factory"](prepared_value=None)
    item["decider"] = RuntimeBootstrapDecider(act=item["act"], envelope=item["envelope"], alias="default", operator=inspector, plans=item["plans"], clock=clock)
    denied = item["decider"].decide(item["request"]).effect is Effect.DENY
    if confirmed:
        item["plans"].confirmed = "fixture-inspection-"+item["facts"].operation_id
    restored = item["decider"].decide(item["request"]).effect is Effect.ALLOW
    try:
        with transaction.atomic(durable=True):
            inspector.stamp(alias="default", operation_id=item["facts"].operation_id, transaction_token="second-tx", target_identity_ref=item["facts"].target_identity_ref, context=ctx)
    except AuthBootstrapBackendError:
        cases["r01_consumed_inspection_only"] = denied and restored
    else:
        cases["r01_consumed_inspection_only"] = False
    inspector.close()

    item = fixture("common-audit-failure")
    try:
        with transaction.atomic(durable=True):
            stages(item, audit(max_bytes=1))
    except CorePortError:
        item["row"].refresh_from_db()
        cases["r01_audit_failure_rollback"] = item["row"].consumed_operation_ref is None and not CoreIdentity.objects.filter(pk=item["target_id"]).exists() and not m.AuthAccountGate.objects.filter(pk=item["target_id"]).exists() and not CoreAuditEvent.objects.filter(operation_id=item["facts"].operation_id).exists()
    else:
        cases["r01_audit_failure_rollback"] = False
    item["backend"].close()

    item = fixture("common-bad-signature")
    item["proofs"].value = replace(item["proofs"].value, signature=bytes(64))
    denied = item["decider"].decide(item["request"])
    cases["r01_bad_signature_deny"] = denied.effect is Effect.DENY and not m.AuthAccountGate.objects.filter(pk=item["target_id"]).exists()
    participant = audit()
    request, facts = item["request"], item["facts"]
    with transaction.atomic(durable=True):
        event = AuditEvent(request.decision_id, None, request.resource_id, request.action_id, ctx, request.correlation_id, Effect.DENY, "DENIED", denied.policy_version, start)
        ref = participant.stage(event, alias="default", operation_id=facts.operation_id, transaction_token="deny-tx", context=ctx, decision=denied)
        participant.verify_staged(TransactionProof(facts.operation_id, "default", "deny-tx", ctx, (ref,), start))
    cases["r01_denial_audited"] = CoreAuditEvent.objects.using("peer").filter(operation_id=facts.operation_id, kind="PDP_AUDIT").count() == 1
    item["backend"].close()
    item = fixture("common-plan-substitution")
    item["manifest"]["target"] = identity_reference(new_uuid7())
    cases["r01_plan_substitution_deny"] = item["decider"].decide(item["request"]).effect is Effect.DENY
    item["backend"].close()
    return cases


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True)
    result["real_components"] = ["AUTH", "CoreFactSource", "RuntimeBootstrapDecider", "PostgresAuditParticipant"]
    result["plan_classification_assurance"] = "FIXTURES_EXPLICITES"
    result["full_c08_c10_delivery"] = False
    return result
