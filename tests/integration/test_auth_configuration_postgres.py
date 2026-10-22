"""Sources locales PG réelles ; plan C08 et classification C10 fixtures explicites."""
from __future__ import annotations

EXPECTED_CASES = ("absent_profile_closed", "no_assurance_default", "stronger_assurance_refused", "rollback_config_atomic", "staged_profile_refused", "profile_committed", "assurance_committed", "production_auth_context", "explicit_session_policies", "selection_no_secrets", "issuer_mutation_refused", "rehashed_snapshot_refused", "assurance_escalation_refused", "assertion_removed_refused", "expired_profile_refused", "revoked_selection_refused", "after_bootstrap_window", "credential_change_keeps_selection", "approval_fk_protected", "config_digest_bound", "audit_common_commit", "evidence_mutation_refused", "wrong_alias_refused", "wrong_profile_refused")


def scenarios():
    import datetime
    import hashlib
    import json
    import secrets
    from dataclasses import replace
    from django.db import transaction
    from django.db.models.deletion import ProtectedError
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    from pixs.auth import models as m
    from pixs.auth.identifiers import new_uuid7, identity_reference
    from pixs.auth.passwords import hash_password
    from pixs.auth.policy import SessionCategory, default_rule
    from pixs.auth.runtime_verifier import LocalTrustProfile, AuthVerificationError, prepare_password_verifier
    from pixs.auth.invocation import AuthInvocationSource
    from pixs.auth.configuration import InitialLocalAuthSelection, selection_digest, bind_prepared_digest, create_local_auth_sources
    from pixs.auth.bootstrap_backend import AuthBootstrapBackend, PreparedBootstrapCredential, prepared_credential_digest, BootstrapAuthClassification
    from pixs.auth.r01 import BootstrapTrustKey, BootstrapTrustPolicy, SignedBootstrapProof, canonical_bootstrap_bytes, bootstrap_challenge_sha256
    from pixs.core.bootstrap_operator import BootstrapOperatorFacts, BOOTSTRAP_ACTION
    from pixs.core.authz.ports import Request, AuditEvent
    from pixs.core.authz.policy import IdentityAssurance, FederationTrust, AuthenticationAssurance, Effect
    from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec, CommandEnvelope
    from pixs.core.identity.models import IdentityType, IdentityState
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.query_source import CoreFactSource
    from pixs.core.ports import CorePortError, TransactionProof
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_runtime_bootstrap import RuntimeBootstrapDecider
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

    out = {}
    now = datetime.datetime.now(datetime.timezone.utc)
    context = ScopeContext(ScopeType.PLATFORM)
    class Clock:
        def __init__(self):
            self.value = now
        def now(self):
            return self.value
    clock = Clock()
    profile = LocalTrustProfile("pixs.auth.local", "1.0.0", "local", "qualified.local", FederationTrust.TRUSTED)
    selection = InitialLocalAuthSelection(profile, "fixture-plan-r01-explicite", now, now+datetime.timedelta(days=1), IdentityAssurance.CLAIMED, "r01-explicit-initial-claim", (default_rule(SessionCategory.ORDINARY), default_rule(SessionCategory.ADMIN)))
    trust, assurance = create_local_auth_sources(alias="default", profile_id=profile.profile_id, clock=clock)
    def refused(name, action):
        try:
            action()
        except (AuthVerificationError, CorePortError):
            out[name] = True
        else:
            out[name] = False
    refused("absent_profile_closed", lambda: trust.current_profile(context))
    refused("no_assurance_default", lambda: replace(selection, identity_level=None))
    refused("stronger_assurance_refused", lambda: replace(selection, identity_level=IdentityAssurance.PROOFED))
    password = "Vecteur public configuration C03, aucun secret réel"
    prepared = PreparedBootstrapCredential(profile.provider_id, profile.issuer, "initial-subject", hash_password(password), selection)
    target_id = new_uuid7()
    target = identity_reference(target_id)
    manifest = {"target": target, "effects": ["CREATE_IDENTITY", "BIND_SUPER_ADMIN", "STAMP_CREDENTIAL"], "prepared_digest": prepared_credential_digest(prepared)}
    def plan_hash():
        return hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    facts = BootstrapOperatorFacts("operator-config", "pixs.core.bootstrap:config-install", BOOTSTRAP_ACTION, context, "config-install", "1.0.0", (BOOTSTRAP_ACTION,), tuple(manifest["effects"]), "config-proof", "config-authorization", "config-operation", target, None, plan_hash(), now, now+datetime.timedelta(seconds=600), "config-key", "1.0.0", None)
    signer = Ed25519PrivateKey.generate()
    public = signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    nonce = secrets.token_bytes(32)
    signed = SignedBootstrapProof(facts, nonce, signer.sign(canonical_bootstrap_bytes(facts, nonce)))
    policy = BootstrapTrustPolicy("1.0.0", (BootstrapTrustKey("config-key", facts.operator_subject_ref, facts.installation_ref, facts.authorized_actions, public, now-datetime.timedelta(days=1), now+datetime.timedelta(days=1), False),))
    class Proofs:
        def resolve(self, ref):
            if ref != facts.operator_proof_ref:
                raise CorePortError()
            return signed
    class OperatorTrust:
        def resolve(self, version):
            return policy
    classification = BootstrapAuthClassification("auth-config-asset", ConfidentialityLevel.CONFIDENTIAL, PersonalDataLevel.PERSONAL)
    class Classification:
        def resolve(self, **kwargs):
            return classification
    authorization = m.AuthBootstrapAuthorization.objects.create(authorization_ref=facts.authorization_ref, operator_proof_ref=facts.operator_proof_ref, operator_subject_ref=facts.operator_subject_ref, installation_ref=facts.installation_ref, plan_version=facts.plan_version, plan_sha256=facts.plan_sha256, operation_ref=facts.operation_id, target_identity_ref=target, closed_effects=list(facts.closed_effects), authorized_actions=list(facts.authorized_actions), key_id=facts.key_id, trust_policy_version=facts.trust_policy_version, challenge_sha256=bootstrap_challenge_sha256(facts, nonce), credential_prepared_digest=prepared_credential_digest(prepared), valid_from=now, expires_at=facts.expires_at)
    request = Request(facts.authorization_ref, facts.operator_subject_ref, facts.resource_id, facts.action_id, context, "config-correlation")
    act = BootstrapActInput(facts.operation_id, facts.plan_version, facts.installation_ref, "INSTALLER", facts.operator_proof_ref, facts.operator_subject_ref, facts.authorization_ref, target, None, facts.closed_effects, ("CONFIRMED",), context, request.correlation_id, None, "config-idem", facts.plan_sha256, "1.0.0")
    envelope = CommandEnvelope(request, act.operation_id, act.idempotency_key, act.content_sha256, act.serializer_version, act.correlation_id, None)
    class Plans:
        def verify_plan(self, supplied, *, alias):
            if supplied != act or plan_hash() != facts.plan_sha256:
                raise CorePortError()
        def verify_operator_binding(self, supplied, candidate, *, alias):
            self.verify_plan(supplied, alias=alias)
            if replace(candidate, consumed_operation_id=None) != facts:
                raise CorePortError()
        def get_closed_effects(self, *, plan_version, installation_ref):
            if (plan_version, installation_ref) != (facts.plan_version, facts.installation_ref):
                raise CorePortError()
            return facts.closed_effects
        def resolve_targets(self, supplied, *, alias):
            self.verify_plan(supplied, alias=alias)
            return BootstrapTargetSpec(target_id, IdentityType.HUMAN, IdentityState.ACTIVE, None, None, None, None)
        def inspect_confirmed(self, supplied):
            return None
    audit_policy = AuditPolicy("config-audit", "1.0.0", "fixture-explicite", 1, 65536, 50, (), "config-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
    audit = PostgresAuditParticipant(ExplicitAuditPolicySource(context, audit_policy), clock, "peer")
    def backend():
        return AuthBootstrapBackend(alias="default", proofs=Proofs(), trust=OperatorTrust(), facts_reader=CoreFactSource(), classification_source=Classification(), clock=clock, prepared=prepared)
    b = backend()
    d = RuntimeBootstrapDecider(act=act, envelope=envelope, alias="default", operator=b, plans=Plans(), clock=clock)
    with transaction.atomic(durable=True):
        decision = d.revalidate_under_locks(request, alias="default", operation_id=facts.operation_id)
        if decision.effect is not Effect.ALLOW:
            raise AssertionError("BOOTSTRAP_REQUIRED")
        CoreIdentity.objects.create(identity_id=target_id, identity_type="HUMAN", state="ACTIVE", **classification.values())
        b.stamp(alias="default", operation_id=facts.operation_id, transaction_token="config-rollback", target_identity_ref=target, context=context)
        transaction.set_rollback(True)
    b.close()
    authorization.refresh_from_db()
    out["rollback_config_atomic"] = authorization.consumed_operation_ref is None and m.AuthLocalTrustSelection.objects.count() == 0 and m.AuthIdentityAssurance.objects.count() == 0 and m.AuthPolicyRow.objects.count() == 0 and m.AuthOperation.objects.count() == 0 and not CoreIdentity.objects.filter(pk=target_id).exists()
    b = backend()
    d = RuntimeBootstrapDecider(act=act, envelope=envelope, alias="default", operator=b, plans=Plans(), clock=clock)
    with transaction.atomic(durable=True):
        decision = d.revalidate_under_locks(request, alias="default", operation_id=facts.operation_id)
        if decision.effect is not Effect.ALLOW:
            raise AssertionError("BOOTSTRAP_REQUIRED")
        CoreIdentity.objects.create(identity_id=target_id, identity_type="HUMAN", state="ACTIVE", **classification.values())
        cred = b.stamp(alias="default", operation_id=facts.operation_id, transaction_token="config-commit", target_identity_ref=target, context=context)
        refused("staged_profile_refused", lambda: trust.current_profile(context))
        event = AuditEvent(request.decision_id, request.subject_id, request.resource_id, request.action_id, context, request.correlation_id, Effect.ALLOW, "ALLOWED", decision.policy_version, now)
        audited = audit.stage(event, alias="default", operation_id=facts.operation_id, transaction_token="config-commit", context=context, decision=decision)
        proof = TransactionProof(facts.operation_id, "default", "config-commit", context, (cred, audited), now)
        b.verify_staged(proof)
        audit.verify_staged(proof)
        final = d.revalidate_under_locks(request, alias="default", operation_id=facts.operation_id)
        if final.effect is not Effect.ALLOW or final.policy_version != decision.policy_version:
            raise AssertionError("FINAL_DECISION_CHANGED")
    b.close()
    row = m.AuthLocalTrustSelection.objects.get(profile_ref=profile.profile_id)
    claim = m.AuthIdentityAssurance.objects.get(identity_id=target_id)
    credential = m.AuthPasswordCredential.objects.get(binding__identity_id=target_id)
    subject_request = Request("config-login", target, target, "pixs.auth.session.create", context, "config-login-correlation")
    def read_assurance(**updates):
        args = dict(alias="default", operation_id="config-read")
        args.update(updates)
        with transaction.atomic():
            return assurance.resolve(target, subject_request, **args)
    out["profile_committed"] = trust.current_profile(context) == profile
    out["assurance_committed"] = read_assurance() is IdentityAssurance.CLAIMED
    source = AuthInvocationSource(prepare_password_verifier(request=subject_request, alias="default", operation_id="config-login-op", profile=trust.current_profile(context), trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, external_subject=prepared.external_subject, password=password, category=SessionCategory.ORDINARY))
    try:
        auth, status = source.revalidate(subject_request, alias="default", operation_id="config-login-op")
        out["production_auth_context"] = auth.identity_assurance is IdentityAssurance.CLAIMED and auth.authentication_assurance is AuthenticationAssurance.SINGLE_FACTOR and auth.provider_id == profile.provider_id
    finally:
        source.close()
    ordinary = m.AuthPolicyRow.objects.get(category="ORDINARY", is_current=True)
    admin = m.AuthPolicyRow.objects.get(category="ADMIN", is_current=True)
    out["explicit_session_policies"] = (ordinary.idle_seconds, ordinary.absolute_seconds, ordinary.max_sessions, admin.idle_seconds, admin.absolute_seconds, admin.max_sessions) == (3600, 43200, 5, 900, 7200, 2) and ordinary.origin == selection.origin
    encoded = json.dumps(row.selection_payload, sort_keys=True)
    out["selection_no_secrets"] = password not in encoded and prepared.password_hash not in encoded and "password_hash" not in encoded
    out["config_digest_bound"] = bind_prepared_digest(row.credential_components_sha256, row.selection_sha256) == authorization.credential_prepared_digest and row.selection_sha256 == selection_digest(selection)
    out["audit_common_commit"] = CoreAuditEvent.objects.using("peer").filter(operation_id=facts.operation_id).count() == 1 and m.AuthLocalTrustSelection.objects.using("peer").filter(pk=row.pk).exists() and m.AuthIdentityAssurance.objects.using("peer").filter(pk=claim.pk).exists()
    def changed(name, mutate, read=lambda: trust.current_profile(context)):
        with transaction.atomic():
            mutate()
            refused(name, read)
            transaction.set_rollback(True)
    changed("issuer_mutation_refused", lambda: m.AuthLocalTrustSelection.objects.filter(pk=row.pk).update(issuer="unapproved-issuer"))
    forged = replace(selection, profile=replace(profile, issuer="rehashed-unapproved"))
    changed("rehashed_snapshot_refused", lambda: m.AuthLocalTrustSelection.objects.filter(pk=row.pk).update(issuer=forged.profile.issuer, selection_payload=forged.document(), selection_sha256=selection_digest(forged)))
    changed("assurance_escalation_refused", lambda: m.AuthIdentityAssurance.objects.filter(pk=claim.pk).update(level="VERIFIED"), read_assurance)
    changed("assertion_removed_refused", lambda: m.AuthIdentityAssurance.objects.filter(pk=claim.pk).update(is_current=False), read_assurance)
    changed("evidence_mutation_refused", lambda: m.AuthIdentityAssurance.objects.filter(pk=claim.pk).update(evidence_ref="unapproved-evidence"), read_assurance)
    changed("revoked_selection_refused", lambda: m.AuthLocalTrustSelection.objects.filter(pk=row.pk).update(is_current=False))
    try:
        clock.value = selection.valid_until
        refused("expired_profile_refused", lambda: trust.current_profile(context))
        clock.value = now+datetime.timedelta(seconds=700)
        out["after_bootstrap_window"] = trust.current_profile(context) == profile and read_assurance() is IdentityAssurance.CLAIMED
    finally:
        clock.value = now
    with transaction.atomic():
        m.AuthPasswordCredential.objects.filter(pk=credential.pk).update(password_hash=hash_password("Autre vecteur public après changement"), version=2)
        out["credential_change_keeps_selection"] = trust.current_profile(context) == profile
        transaction.set_rollback(True)
    try:
        with transaction.atomic():
            authorization.delete()
    except ProtectedError:
        out["approval_fk_protected"] = True
    else:
        out["approval_fk_protected"] = False
    refused("wrong_alias_refused", lambda: read_assurance(alias="peer"))
    other_trust, _ = create_local_auth_sources(alias="default", profile_id="absent-profile", clock=clock)
    refused("wrong_profile_refused", lambda: other_trust.current_profile(context))
    return out


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True)
    result["real_components"] = ["AuthBootstrapBackend", "PostgresLocalTrustSource", "PostgresIdentityAssuranceSource", "AuthInvocationSource", "CoreFactSource", "RuntimeBootstrapDecider", "PostgresAuditParticipant"]
    result["plan_operator_key_classification"] = "FIXTURES_EXPLICITES"
    result["full_c08_c10_delivery"] = False
    return result
