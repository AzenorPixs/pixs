"""Changement/récupération et repli D14 réels, sans reconnexion automatique."""
from __future__ import annotations

EXPECTED_CASES = ("change_committed", "old_password_refused", "all_sessions_invalid", "no_auto_session", "credential_result_persisted", "freshness_boundary_refused", "audit_down_withdraw_only", "password_unchanged_after_fallback", "fallback_global_once", "fallback_no_fake_audit", "fallback_reconciliation", "recovery_changed", "recovery_no_mfa_restored", "recovery_audit_down_unchanged", "unknown_commit_no_claim", "unknown_commit_actual_password", "other_account_preserved", "no_new_password_in_observations")


def scenarios():
    import datetime
    import json
    from dataclasses import replace
    from unittest.mock import patch
    from django.db import connections, OperationalError
    from pixs.auth import models as m
    from pixs.auth.contracts import AuthOutcome, CredentialDisposition, AuthServiceError
    from pixs.auth.identifiers import new_uuid7
    from pixs.auth.passwords import verify_password
    from pixs.auth.tokens import TokenKind
    from pixs.auth.runtime_verifier import prepare_token_verifier, AuthVerificationError
    from pixs.auth.invocation import AuthInvocationSource
    from pixs.core.query_source import CoreFactSource
    from pixs.core.authz.policy import AuthenticationAssurance, IdentityAssurance
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from auth_service_fixture import make_auth_service_fixture
    f = make_auth_service_fixture()
    out = {}
    credential = m.AuthPasswordCredential.objects.get(binding__identity_id=f["identity"])
    original_password = f["supplied"].password
    p1, p2, p3, p4, p5 = ("Vecteur public mot de passe "+str(index) for index in range(1, 6))
    other = m.AuthAccountGate.objects.create(identity_id=new_uuid7(), session_generation=9)
    def login(label, password):
        command = f["grant"](f["command"]("pixs.auth.session.create", f["actor"], "credential-login-"+label))
        return f["service"]().login(command, replace(f["supplied"], password=password))
    def command(label, recovery=False):
        return f["grant"](f["command"]("pixs.auth.credential.recover" if recovery else "pixs.auth.credential.change", "pixs.auth.credential:"+str(credential.pk), label))
    def auth(result):
        req = f["command"]("pixs.auth.session.create", f["actor"], "check-"+new_uuid7().hex).request
        operation = "check-"+new_uuid7().hex
        verifier = prepare_token_verifier(request=req, alias="default", operation_id=operation, profile=f["profile"], trust_source=f["trust"], assurance_source=f["assurance"], facts_reader=CoreFactSource(), clock=f["clock"], token=result.emission.access, kind=TokenKind.ACCESS)
        source = AuthInvocationSource(verifier)
        try:
            return source.revalidate(req, alias="default", operation_id=operation)[0]
        finally:
            source.close()
    first, second = login("first", original_password), login("second", original_password)
    before_count = m.AuthSession.objects.count()
    change_cmd = command("credential-change-one")
    changed = f["service"]().change_password(change_cmd, first.emission.access, p1)
    credential.refresh_from_db()
    out["change_committed"] = changed.outcome is AuthOutcome.WITHDRAWN and changed.credential is CredentialDisposition.CHANGED and verify_password(p1, credential.password_hash)
    out["old_password_refused"] = not verify_password(original_password, credential.password_hash)
    denied = 0
    for prior in (first, second):
        try: auth(prior)
        except AuthVerificationError: denied += 1
    out["all_sessions_invalid"] = denied == 2
    out["no_auto_session"] = changed.emission is None and m.AuthSession.objects.count() == before_count
    out["credential_result_persisted"] = m.AuthOperation.objects.get(operation_ref=change_cmd.operation_id).credential_outcome == "CHANGED"
    fresh = login("fresh", p1)
    saved_time = f["clock"].value
    old_hash = credential.password_hash
    try:
        f["clock"].value += datetime.timedelta(seconds=300)
        try:
            f["service"]().change_password(command("too-old"), fresh.emission.access, p2)
        except AuthServiceError:
            out["freshness_boundary_refused"] = m.AuthPasswordCredential.objects.get(pk=credential.pk).password_hash == old_hash
        else:
            out["freshness_boundary_refused"] = False
    finally:
        f["clock"].value = saved_time
    before_gate = m.AuthAccountGate.objects.get(pk=f["identity"])
    old_generation, old_credential_generation = before_gate.session_generation, before_gate.credential_generation
    fallback_cmd = command("credential-audit-down")
    partial = f["service"](1).change_password(fallback_cmd, fresh.emission.access, p2)
    credential.refresh_from_db()
    gate = m.AuthAccountGate.objects.get(pk=f["identity"])
    pending = m.AuthAuditPending.objects.get(operation__operation_ref=fallback_cmd.operation_id)
    out["audit_down_withdraw_only"] = partial.outcome is AuthOutcome.WITHDRAWN_AUDIT_PENDING and partial.credential is CredentialDisposition.UNCHANGED and partial.emission is None
    out["password_unchanged_after_fallback"] = credential.password_hash == old_hash and verify_password(p1, credential.password_hash) and not verify_password(p2, credential.password_hash)
    out["fallback_global_once"] = gate.session_generation == old_generation+1 and gate.credential_generation == old_credential_generation
    out["fallback_no_fake_audit"] = CoreAuditEvent.objects.filter(operation_id=fallback_cmd.operation_id).count() == 0 and pending.operation.credential_outcome == "UNCHANGED"
    current = login("after-fallback", p1)
    reconcile_cmd = f["grant"](f["command"]("pixs.auth.audit.reconcile", "pixs.auth.audit-pending:"+str(pending.pk), "credential-reconcile"))
    reconciled = f["service"]().reconcile_audit(reconcile_cmd, current.emission.access)
    out["fallback_reconciliation"] = reconciled.outcome is AuthOutcome.WITHDRAWN and m.AuthAuditPending.objects.get(pk=pending.pk).state == "RECONCILED" and m.AuthOperation.objects.get(operation_ref=fallback_cmd.operation_id).credential_outcome == "UNCHANGED"
    recovered = f["service"]().recover_password(command("credential-recovery", True), current.emission.access, p3)
    credential.refresh_from_db()
    out["recovery_changed"] = recovered.credential is CredentialDisposition.CHANGED and recovered.emission is None and verify_password(p3, credential.password_hash)
    recovery_actor = login("after-recovery", p3)
    proof = auth(recovery_actor)
    out["recovery_no_mfa_restored"] = proof.authentication_assurance is AuthenticationAssurance.SINGLE_FACTOR and proof.identity_assurance is IdentityAssurance.CLAIMED
    recovery_down_cmd = command("recovery-audit-down", True)
    recovery_partial = f["service"](1).recover_password(recovery_down_cmd, recovery_actor.emission.access, p4)
    credential.refresh_from_db()
    out["recovery_audit_down_unchanged"] = recovery_partial.credential is CredentialDisposition.UNCHANGED and verify_password(p3, credential.password_hash) and not verify_password(p4, credential.password_hash) and m.AuthAuditPending.objects.get(operation__operation_ref=recovery_down_cmd.operation_id).cause == "RECOVERY"
    actor = login("unknown-actor", p3)
    unknown_cmd = command("credential-unknown")
    connection = connections["default"]
    real_commit = connection.commit
    fired = {"value": False}
    def uncertain():
        trigger = not fired["value"] and m.AuthOperation.objects.filter(operation_ref=unknown_cmd.operation_id).exists()
        real_commit()
        if trigger:
            fired["value"] = True
            raise OperationalError("synthetic-after-real-commit")
    with patch.object(connection, "commit", uncertain):
        unknown = f["service"]().change_password(unknown_cmd, actor.emission.access, p5)
    credential.refresh_from_db()
    out["unknown_commit_no_claim"] = fired["value"] and unknown.outcome is AuthOutcome.UNKNOWN and unknown.credential is CredentialDisposition.UNKNOWN and unknown.emission is None
    out["unknown_commit_actual_password"] = verify_password(p5, credential.password_hash) and m.AuthOperation.objects.using("peer").get(operation_ref=unknown_cmd.operation_id).credential_outcome == "CHANGED"
    out["other_account_preserved"] = m.AuthAccountGate.objects.get(pk=other.pk).session_generation == 9
    observations = json.dumps(list(m.AuthAuditPending.objects.values_list("event_payload", flat=True)), sort_keys=True)+json.dumps(list(m.AuthOperation.objects.values_list("request_digest", flat=True)))
    out["no_new_password_in_observations"] = all(value not in observations for value in (original_password, p1, p2, p3, p4, p5))
    return out


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True)
    result["real_components"] = ["CredentialMutationService", "AuthTransitionVerifier", "RuntimeAuthorizationDecider", "PostgresAuditParticipant", "CommittedWithdrawalSource"]
    result["plan_operator_key_governance"] = "FIXTURES_EXPLICITES"
    result["full_p0_activation"] = False
    return result
