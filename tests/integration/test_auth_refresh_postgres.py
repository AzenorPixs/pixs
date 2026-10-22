"""Rotation et réutilisation sur vrais Auth/C04/C05, sans secret serveur restituable."""
from __future__ import annotations

EXPECTED_CASES = ("refresh_not_access", "rotation_same_session", "rotation_consumed_once", "no_freshness_or_activity", "hash_only_new_tokens", "repeat_no_reissue", "legitimate_concurrent", "suspect_session_withdrawn", "other_session_preserved", "suspect_audit_down_pending", "suspect_no_fake_audit", "suspect_reconciliation", "rotation_audit_failure_rollback", "unknown_commit_no_secret", "unknown_retry_no_reissue", "idle_expiry_without_activity", "wrong_target_refused", "consumed_never_active")


def scenarios():
    import datetime
    import threading
    from dataclasses import replace
    from unittest.mock import patch
    from django.db import connections, OperationalError
    from pixs.auth import models as m
    from pixs.auth.contracts import AuthOutcome, AuthServiceError
    from pixs.auth.tokens import TokenKind, token_fingerprint
    from pixs.auth.runtime_verifier import prepare_token_verifier, prepare_renewal_verifier, AuthVerificationError
    from pixs.auth.invocation import AuthInvocationSource
    from pixs.auth.identifiers import new_uuid7
    from pixs.core.query_source import CoreFactSource
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from auth_service_fixture import make_auth_service_fixture
    f = make_auth_service_fixture()
    out = {}
    def command(result, label):
        return f["grant"](f["command"]("pixs.auth.session.renew", "pixs.auth.session:"+str(result.session.session_id), label))
    def denied(name, action):
        try:
            action()
        except (AuthServiceError, AuthVerificationError):
            out[name] = True
        else:
            out[name] = False
    first, other = f["login"]("refresh-first"), f["login"]("refresh-other")
    initial = m.AuthSession.objects.get(pk=first.session.session_id)
    before_times = (initial.authenticated_at, initial.last_activity_at, initial.idle_expires_at, initial.absolute_expires_at)
    first_cmd = command(first, "refresh-one")
    kwargs = dict(request=first_cmd.request, alias="default", operation_id=first_cmd.operation_id, profile=f["profile"], trust_source=f["trust"], assurance_source=f["assurance"], facts_reader=CoreFactSource(), clock=f["clock"], token=first.emission.refresh)
    denied("refresh_not_access", lambda: prepare_token_verifier(**kwargs, kind=TokenKind.REFRESH))
    rotated = f["service"]().renew(first_cmd, first.emission.refresh)
    initial.refresh_from_db()
    old = m.AuthToken.objects.get(digest=token_fingerprint(first.emission.refresh, TokenKind.REFRESH))
    out["rotation_same_session"] = rotated.outcome is AuthOutcome.ISSUED and rotated.session.session_id == first.session.session_id and m.AuthSession.objects.count() == 2
    out["rotation_consumed_once"] = old.state == "CONSUMED" and old.consumed_operation_ref == first_cmd.operation_id and m.AuthToken.objects.filter(parent=old).count() == 2
    out["no_freshness_or_activity"] = before_times == (initial.authenticated_at, initial.last_activity_at, initial.idle_expires_at, initial.absolute_expires_at)
    out["hash_only_new_tokens"] = m.AuthToken.objects.filter(digest=token_fingerprint(rotated.emission.refresh, TokenKind.REFRESH)).exists() and not m.AuthToken.objects.filter(digest=rotated.emission.refresh.value).exists()
    count = m.AuthToken.objects.count()
    repeated = f["service"]().renew(first_cmd, first.emission.refresh)
    out["repeat_no_reissue"] = repeated.outcome is AuthOutcome.REAUTH_REQUIRED and repeated.emission is None and count == m.AuthToken.objects.count() and m.AuthSession.objects.get(pk=initial.pk).state == "ACTIVE"
    verifier = prepare_renewal_verifier(**kwargs)
    source = AuthInvocationSource(verifier)
    try:
        denied("consumed_never_active", lambda: source.revalidate(first_cmd.request, alias="default", operation_id=first_cmd.operation_id))
    finally:
        source.close()
    concurrent = f["login"]("refresh-concurrent")
    commands = [command(concurrent, "concurrent-refresh-"+str(index)) for index in range(2)]
    barrier = threading.Barrier(2)
    results, closed = [], []
    def worker(index):
        raw = []
        try:
            barrier.wait(timeout=5)
            result = f["service"]().renew(commands[index], concurrent.emission.refresh)
            results.append(result.outcome.value)
        except Exception as error:
            results.append(type(error).__name__)
        finally:
            for alias in ("default", "peer"):
                conn = connections[alias]
                if conn.connection is not None:
                    raw.append(conn.connection)
                conn.close()
            closed.append(all(bool(conn.closed) for conn in raw))
    workers = [threading.Thread(target=worker, args=(index,)) for index in range(2)]
    for item in workers: item.start()
    for item in workers: item.join(12)
    out["legitimate_concurrent"] = not any(item.is_alive() for item in workers) and sorted(results) == ["ISSUED", "REAUTH_REQUIRED"] and len(closed) == 2 and all(closed) and m.AuthToken.objects.filter(parent__digest=token_fingerprint(concurrent.emission.refresh, TokenKind.REFRESH)).count() == 2
    f["clock"].value += datetime.timedelta(seconds=1)
    suspicious = f["service"]().renew(command(first, "suspect-refresh"), first.emission.refresh)
    out["suspect_session_withdrawn"] = suspicious.outcome is AuthOutcome.WITHDRAWN and m.AuthSession.objects.get(pk=initial.pk).state == "REVOKED"
    out["other_session_preserved"] = m.AuthSession.objects.get(pk=other.session.session_id).state == "ACTIVE" and m.AuthSession.objects.get(pk=concurrent.session.session_id).state == "ACTIVE"
    audit_target = f["login"]("refresh-audit-target")
    audit_first = command(audit_target, "refresh-audit-first")
    f["service"]().renew(audit_first, audit_target.emission.refresh)
    f["clock"].value += datetime.timedelta(seconds=1)
    suspect_cmd = command(audit_target, "refresh-audit-suspect")
    pending_result = f["service"](1).renew(suspect_cmd, audit_target.emission.refresh)
    pending = m.AuthAuditPending.objects.get(operation__operation_ref=suspect_cmd.operation_id)
    out["suspect_audit_down_pending"] = pending_result.outcome is AuthOutcome.WITHDRAWN_AUDIT_PENDING and pending.state == "PENDING" and pending.cause == "REFRESH_REUSE" and m.AuthSession.objects.get(pk=audit_target.session.session_id).state == "REVOKED"
    out["suspect_no_fake_audit"] = CoreAuditEvent.objects.filter(operation_id=suspect_cmd.operation_id).count() == 0
    reconcile_cmd = f["grant"](f["command"]("pixs.auth.audit.reconcile", "pixs.auth.audit-pending:"+str(pending.pk), "reconcile-refresh-reuse"))
    reconciled = f["service"]().reconcile_audit(reconcile_cmd, other.emission.access)
    out["suspect_reconciliation"] = reconciled.outcome is AuthOutcome.WITHDRAWN and m.AuthAuditPending.objects.get(pk=pending.pk).state == "RECONCILED" and CoreAuditEvent.objects.filter(generic_event_id=str(pending.event_id)).count() == 1
    failed_target = f["login"]("refresh-failure-target")
    failed_old = m.AuthToken.objects.get(digest=token_fingerprint(failed_target.emission.refresh, TokenKind.REFRESH))
    count = m.AuthToken.objects.filter(session_id=failed_target.session.session_id).count()
    denied("rotation_audit_failure_rollback", lambda: f["service"](1).renew(command(failed_target, "refresh-fail-audit"), failed_target.emission.refresh))
    failed_old.refresh_from_db()
    out["rotation_audit_failure_rollback"] &= failed_old.state == "ACTIVE" and failed_old.consumed_operation_ref is None and count == m.AuthToken.objects.filter(session_id=failed_target.session.session_id).count()
    unknown_cmd = command(failed_target, "refresh-unknown-commit")
    connection = connections["default"]
    actual_commit = connection.commit
    fired = {"value": False}
    def uncertain():
        trigger = not fired["value"] and m.AuthOperation.objects.filter(operation_ref=unknown_cmd.operation_id).exists()
        actual_commit()
        if trigger:
            fired["value"] = True
            raise OperationalError("synthetic-after-real-commit")
    with patch.object(connection, "commit", uncertain):
        unknown = f["service"]().renew(unknown_cmd, failed_target.emission.refresh)
    out["unknown_commit_no_secret"] = fired["value"] and unknown.outcome is AuthOutcome.UNKNOWN and unknown.emission is None and m.AuthOperation.objects.using("peer").filter(operation_ref=unknown_cmd.operation_id).exists()
    count = m.AuthToken.objects.filter(session_id=failed_target.session.session_id).count()
    retried = f["service"]().renew(unknown_cmd, failed_target.emission.refresh)
    out["unknown_retry_no_reissue"] = retried.outcome is AuthOutcome.REAUTH_REQUIRED and retried.emission is None and count == m.AuthToken.objects.filter(session_id=failed_target.session.session_id).count()
    invalid_target = command(other, "wrong-session-refresh")
    invalid_target = replace(invalid_target, request=replace(invalid_target.request, resource_id="pixs.auth.session:"+str(new_uuid7())))
    denied("wrong_target_refused", lambda: f["service"]().renew(invalid_target, other.emission.refresh))
    expiry = m.AuthSession.objects.get(pk=other.session.session_id).idle_expires_at
    f["clock"].value = expiry
    denied("idle_expiry_without_activity", lambda: f["service"]().renew(command(other, "refresh-idle-boundary"), other.emission.refresh))
    out["idle_expiry_without_activity"] &= m.AuthSession.objects.get(pk=other.session.session_id).idle_expires_at == expiry
    return out


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True)
    result["real_components"] = ["PostgresLocalAuthService", "RenewalPurposeVerifier", "AuthTransitionVerifier", "RuntimeAuthorizationDecider", "PostgresAuditParticipant"]
    result["replay_policy"] = "LOCAL_V1_OP_KEY_OR_SERVER_RECEIVED_BEFORE_CONSUMPTION"
    result["plan_operator_key_governance"] = "FIXTURES_EXPLICITES"
    result["full_p0_activation"] = False
    return result
