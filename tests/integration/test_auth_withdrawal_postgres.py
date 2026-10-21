"""Retraits et réconciliation D14 réels ; aucune réactivation d'un justificatif retiré."""
from __future__ import annotations

EXPECTED_CASES = ("logout_confirmed", "all_derivatives_invalid", "other_session_preserved", "audit_failure_withdrawn", "audit_failure_no_fiction", "pending_durable_peer", "reconcile_denied_without_current_actor", "reconcile_audit_down_keeps_pending", "reconcile_with_new_authority", "original_event_id_time", "pending_resolved_common", "reconcile_idempotent", "global_generation_withdrawal", "global_all_contexts_invalid", "other_account_preserved", "tampered_payload_refused", "pending_not_resolved_on_tamper", "no_secret_in_pending")


def scenarios():
    import datetime
    from django.db import transaction
    from pixs.auth import models as m
    from pixs.auth.contracts import AuthOutcome, AuditDisposition, AuthServiceError
    from pixs.auth.tokens import TokenKind
    from pixs.auth.identifiers import new_uuid7
    from pixs.auth.runtime_verifier import prepare_token_verifier, prepare_renewal_verifier, AuthVerificationError
    from pixs.auth.invocation import AuthInvocationSource
    from pixs.core.query_source import CoreFactSource
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from auth_service_fixture import make_auth_service_fixture
    f = make_auth_service_fixture()
    out = {}
    def cmd(action, resource, label):
        return f["grant"](f["command"](action, resource, label))
    def refused(name, call):
        try:
            call()
        except (AuthServiceError, AuthVerificationError):
            out[name] = True
        else:
            out[name] = False
    def valid(result, kind=TokenKind.ACCESS):
        sid = result.session.session_id
        request = f["command"]("pixs.auth.session.renew" if kind is TokenKind.REFRESH else "pixs.auth.session.create", "pixs.auth.session:"+str(sid) if kind is TokenKind.REFRESH else f["actor"], "probe-"+new_uuid7().hex).request
        token = result.emission.refresh if kind is TokenKind.REFRESH else result.emission.access
        kwargs = dict(request=request, alias="default", operation_id="probe-"+new_uuid7().hex, profile=f["profile"], trust_source=f["trust"], assurance_source=f["assurance"], facts_reader=CoreFactSource(), clock=f["clock"], token=token)
        verifier = prepare_renewal_verifier(**kwargs) if kind is TokenKind.REFRESH else prepare_token_verifier(**kwargs, kind=kind)
        source = AuthInvocationSource(verifier)
        try:
            return source.revalidate(request, alias="default", operation_id=verifier._operation)
        finally:
            source.close()
    first, second = f["login"]("first"), f["login"]("second")
    logout_cmd = cmd("pixs.auth.session.logout", "pixs.auth.session:"+str(first.session.session_id), "logout-first")
    result = f["service"]().logout(logout_cmd, first.emission.access)
    out["logout_confirmed"] = result.outcome is AuthOutcome.WITHDRAWN and result.audit is AuditDisposition.CONFIRMED and m.AuthSession.objects.get(pk=first.session.session_id).state == "REVOKED" and CoreAuditEvent.objects.filter(operation_id=logout_cmd.operation_id).count() == 2
    access_denied = refresh_denied = False
    try: valid(first)
    except AuthVerificationError: access_denied = True
    try: valid(first, TokenKind.REFRESH)
    except AuthVerificationError: refresh_denied = True
    out["all_derivatives_invalid"] = access_denied and refresh_denied
    out["other_session_preserved"] = valid(second)[0].session_id == str(second.session.session_id)
    third = f["login"]("third")
    pending_cmd = cmd("pixs.auth.session.logout", "pixs.auth.session:"+str(third.session.session_id), "logout-audit-down")
    pending_result = f["service"](1).logout(pending_cmd, third.emission.access)
    pending = m.AuthAuditPending.objects.get(operation__operation_ref=pending_cmd.operation_id)
    out["audit_failure_withdrawn"] = pending_result.outcome is AuthOutcome.WITHDRAWN_AUDIT_PENDING and pending_result.audit is AuditDisposition.PENDING and m.AuthSession.objects.get(pk=third.session.session_id).state == "REVOKED"
    out["audit_failure_no_fiction"] = CoreAuditEvent.objects.filter(operation_id=pending_cmd.operation_id).count() == 0 and pending.operation.outcome == "WITHDRAWAL_PENDING_AUDIT"
    out["pending_durable_peer"] = m.AuthAuditPending.objects.using("peer").filter(pk=pending.pk, state="PENDING").exists()
    event_id, event_time = str(pending.event_id), pending.event_payload["occurred_at"]
    reconcile_cmd = cmd("pixs.auth.audit.reconcile", "pixs.auth.audit-pending:"+str(pending.pk), "reconcile-pending")
    refused("reconcile_denied_without_current_actor", lambda: f["service"]().reconcile_audit(reconcile_cmd, third.emission.access))
    f["clock"].value += datetime.timedelta(seconds=700)
    current = f["login"]("reconcile-actor")
    refused("reconcile_audit_down_keeps_pending", lambda: f["service"](1).reconcile_audit(reconcile_cmd, current.emission.access))
    out["reconcile_audit_down_keeps_pending"] &= m.AuthAuditPending.objects.get(pk=pending.pk).state == "PENDING"
    reconciled = f["service"]().reconcile_audit(reconcile_cmd, current.emission.access)
    out["reconcile_with_new_authority"] = reconciled.outcome is AuthOutcome.WITHDRAWN and reconciled.audit is AuditDisposition.CONFIRMED
    event = CoreAuditEvent.objects.get(generic_event_id=event_id)
    out["original_event_id_time"] = event.generic_payload["event_id"] == event_id and event.generic_payload["occurred_at"] == event_time
    out["pending_resolved_common"] = m.AuthAuditPending.objects.using("peer").get(pk=pending.pk).state == "RECONCILED" and m.AuthOperation.objects.using("peer").get(operation_ref=pending_cmd.operation_id).outcome == "RECORDED" and CoreAuditEvent.objects.using("peer").filter(generic_event_id=event_id).count() == 1
    repeated = f["service"]().reconcile_audit(reconcile_cmd, current.emission.access)
    out["reconcile_idempotent"] = repeated.emission is None and CoreAuditEvent.objects.filter(generic_event_id=event_id).count() == 1
    extra = m.AuthAccountGate.objects.create(identity_id=new_uuid7(), session_generation=7)
    before = m.AuthAccountGate.objects.get(pk=f["identity"]).session_generation
    global_cmd = cmd("pixs.auth.session.revoke_all", "pixs.auth.account:"+str(f["identity"]), "revoke-all")
    global_result = f["service"]().revoke_all(global_cmd, current.emission.access)
    out["global_generation_withdrawal"] = global_result.outcome is AuthOutcome.WITHDRAWN and m.AuthAccountGate.objects.get(pk=f["identity"]).session_generation == before+1
    failures = 0
    for prior in (second, current):
        try: valid(prior)
        except AuthVerificationError: failures += 1
    out["global_all_contexts_invalid"] = failures == 2
    out["other_account_preserved"] = m.AuthAccountGate.objects.get(pk=extra.pk).session_generation == 7
    bad = f["login"]("tamper-target")
    bad_cmd = cmd("pixs.auth.session.logout", "pixs.auth.session:"+str(bad.session.session_id), "tamper-withdraw")
    f["service"](1).logout(bad_cmd, bad.emission.access)
    changed = m.AuthAuditPending.objects.get(operation__operation_ref=bad_cmd.operation_id)
    original = dict(changed.event_payload)
    wrong = dict(original, event_id=str(new_uuid7()))
    m.AuthAuditPending.objects.filter(pk=changed.pk).update(event_payload=wrong)
    actor = f["login"]("tamper-reconcile-actor")
    tamper_cmd = cmd("pixs.auth.audit.reconcile", "pixs.auth.audit-pending:"+str(changed.pk), "tamper-reconcile")
    refused("tampered_payload_refused", lambda: f["service"]().reconcile_audit(tamper_cmd, actor.emission.access))
    out["pending_not_resolved_on_tamper"] = m.AuthAuditPending.objects.get(pk=changed.pk).state == "PENDING" and not CoreAuditEvent.objects.filter(generic_event_id=wrong["event_id"]).exists()
    m.AuthAuditPending.objects.filter(pk=changed.pk).update(event_payload=original)
    import json
    persisted = json.dumps(list(m.AuthAuditPending.objects.values_list("event_payload", flat=True)), sort_keys=True)
    out["no_secret_in_pending"] = all(token.value not in persisted for entry in (first, second, third, current, bad, actor) for token in (entry.emission.access, entry.emission.refresh)) and "password" not in persisted
    return out


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True)
    result["real_components"] = ["PostgresLocalAuthService", "AuthTransitionVerifier", "RuntimeAuthorizationDecider", "PostgresAuditParticipant", "CommittedWithdrawalSource"]
    result["plan_operator_key_governance"] = "FIXTURES_EXPLICITES"
    result["full_p0_activation"] = False
    return result
