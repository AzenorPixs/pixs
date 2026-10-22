"""Admission locale réelle C03/C04/C05 ; configuration initiale via recette propriétaire."""
from __future__ import annotations

EXPECTED_CASES = ("configuration_ready", "api_commit_confirmed", "hash_only_storage", "ordinary_durations", "minted_access_usable", "web_cookie_separate", "idempotence_no_reissue", "body_conflict_refused", "wrong_password_audited", "missing_mapping_audited", "core_revocation_closed", "trust_revocation_closed", "audit_failure_rollback", "unknown_commit_no_secret", "unknown_retry_no_reissue", "ordinary_limit", "explicit_replacement", "replacement_audit_failure_rollback", "admin_separate_limit", "target_replacement_refused", "last_slot_concurrent", "thread_connections_closed")


def scenarios():
    import datetime
    import threading
    from dataclasses import replace
    from unittest.mock import patch
    from django.db import connections, OperationalError
    from django.db.models import F
    from pixs.auth import models as m
    from pixs.auth.contracts import AuthCommand, LoginInput, Facade, AuthOutcome, AuthServiceError, AuthDataClassification
    from pixs.auth.policy import SessionCategory
    from pixs.auth.configuration import create_local_auth_sources
    from pixs.auth.identifiers import identity_reference, new_uuid7
    from pixs.auth.tokens import token_fingerprint, TokenKind
    from pixs.auth.runtime_verifier import prepare_token_verifier
    from pixs.auth.invocation import AuthInvocationSource
    from pixs.auth.services import PostgresLocalAuthService
    from pixs.core.authz.ports import Request
    from pixs.core.authz.policy import Effect, Policy, Selector, ScopeSelector, Obligation
    from pixs.core.authz.snapshot import Catalog, Limits
    from pixs.core.persistence.models_authz import CorePolicy, encode_policy
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.query_source import CoreFactSource
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_runtime_store import CoreAuthorizationStore
    from pixs.core.services_runtime_facts import RuntimeTrustedFactsProvider, RuntimeResourceOwner
    from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
    from pixs.core.audit_contracts import AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    from test_auth_configuration_postgres import scenarios as prepare_configuration

    out = {}
    configured = prepare_configuration()
    out["configuration_ready"] = len(configured) == 24 and all(configured.values())
    selection = m.AuthLocalTrustSelection.objects.get(profile_ref="pixs.auth.local")
    identity_id = selection.approval_operation.identity_id
    actor = identity_reference(identity_id)
    context = ScopeContext(ScopeType.PLATFORM)
    class Clock:
        def __init__(self):
            self.value = datetime.datetime.now(datetime.timezone.utc)
        def now(self):
            return self.value
    clock = Clock()
    trust, assurance = create_local_auth_sources(alias="default", profile_id=selection.profile_ref, clock=clock)
    profile = trust.current_profile(context)
    public_password = "Vecteur public configuration C03, aucun secret réel"
    action = "pixs.auth.session.create"
    declared = Policy("login-service-allow", "1.0.0", "pixs.auth", Effect.ALLOW, Selector("subject", (actor,)), Selector("resource", (actor,)), Selector("action", (action,)), ScopeSelector((context,)), obligations=(Obligation("AUDIT"),))
    CorePolicy.objects.create(policy_id=declared.policy_id, policy_version=declared.policy_version, owner=declared.owner, effect=declared.effect.value, definition=encode_policy(declared))
    catalog = Catalog((actor,), (actor,), (action,), (context,), ())
    limits = Limits(64, 64, 10, 20, 20, 64, 256, 256, 10000000, 60, 3600)
    def factory(*, request, operation_id, authentication_source):
        store = CoreAuthorizationStore(alias="default", installation_ref="login-install", base_epoch="login-service-v1", catalog=catalog, limits=limits)
        facts = RuntimeTrustedFactsProvider(store=store, authentication_source=authentication_source, request=request, operation_id=operation_id, additional_owners=(RuntimeResourceOwner("pixs.auth.", authentication_source.ownership),))
        return RuntimeAuthorizationDecider(store=store, facts_provider=facts, clock=clock, request=request, operation_id=operation_id)
    classification = AuthDataClassification("auth-session-asset", ConfidentialityLevel.CONFIDENTIAL, PersonalDataLevel.PERSONAL)
    class Classification:
        def resolve(self, **kwargs):
            return classification
    def service(max_bytes=65536):
        ap = AuditPolicy("login-audit", "1.0.0", "fixture-explicite", 1, max_bytes, 50, (), "login-audit-asset", ConfidentialityLevel.INTERNAL, PersonalDataLevel.PERSONAL)
        audit = PostgresAuditParticipant(ExplicitAuditPolicySource(context, ap), clock, "peer")
        return PostgresLocalAuthService(alias="default", peer_alias="peer", profile_id=selection.profile_ref, trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, audit=audit, classification_source=Classification(), decider_factory=factory)
    svc = service()
    def command(label):
        return AuthCommand(Request("decision-"+label, actor, actor, action, context, "correlation-"+label), "login-"+label, "idem-"+label)
    supplied = LoginInput("initial-subject", public_password, SessionCategory.ORDINARY, Facade.API, None)
    def refused(name, call, code):
        try:
            call()
        except AuthServiceError as error:
            out[name] = error.code == code
        else:
            out[name] = False
    first_command = command("first")
    first = svc.login(first_command, supplied)
    session = m.AuthSession.objects.get(pk=first.session.session_id)
    out["api_commit_confirmed"] = first.outcome is AuthOutcome.ISSUED and first.emission.access is not None and first.emission.refresh is not None and m.AuthSession.objects.using("peer").filter(pk=session.pk).exists() and CoreAuditEvent.objects.using("peer").filter(operation_id=first_command.operation_id).count() == 1
    digests = set(m.AuthToken.objects.filter(session=session).values_list("digest", flat=True))
    out["hash_only_storage"] = digests == {token_fingerprint(first.emission.access, TokenKind.ACCESS), token_fingerprint(first.emission.refresh, TokenKind.REFRESH)} and first.emission.access.value not in digests and first.emission.refresh.value not in digests
    out["ordinary_durations"] = (session.idle_expires_at-session.last_activity_at).total_seconds() == 3600 and (session.absolute_expires_at-session.authenticated_at).total_seconds() == 43200 and m.AuthToken.objects.get(session=session, kind="ACCESS").expires_at == clock.now()+datetime.timedelta(seconds=900)
    proof_request = Request("access-check", actor, actor, action, context, "access-check-correlation")
    source = AuthInvocationSource(prepare_token_verifier(request=proof_request, alias="default", operation_id="access-check-op", profile=profile, trust_source=trust, assurance_source=assurance, facts_reader=CoreFactSource(), clock=clock, token=first.emission.access, kind=TokenKind.ACCESS))
    try:
        auth, _ = source.revalidate(proof_request, alias="default", operation_id="access-check-op")
        out["minted_access_usable"] = auth.session_id == str(session.pk) and auth.digital_identity_id == actor
    finally:
        source.close()
    web = svc.login(command("web"), replace(supplied, facade=Facade.WEB))
    out["web_cookie_separate"] = web.emission.cookie is not None and web.emission.access is None and web.emission.refresh is None and m.AuthToken.objects.filter(session_id=web.session.session_id, kind="WEB_SESSION").count() == 1
    count_before = (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    again = svc.login(first_command, supplied)
    out["idempotence_no_reissue"] = again.outcome is AuthOutcome.REAUTH_REQUIRED and again.emission is None and count_before == (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    refused("body_conflict_refused", lambda: svc.login(first_command, replace(supplied, facade=Facade.WEB)), "AUTH_OPERATION_CONFLICT")
    before_audit = CoreAuditEvent.objects.count()
    refused("wrong_password_audited", lambda: svc.login(command("bad-password"), replace(supplied, password="autre vecteur public")), "AUTH_DENIED")
    out["wrong_password_audited"] &= CoreAuditEvent.objects.count() == before_audit+1
    before_audit = CoreAuditEvent.objects.count()
    refused("missing_mapping_audited", lambda: svc.login(command("absent"), replace(supplied, external_subject="absent")), "AUTH_DENIED")
    out["missing_mapping_audited"] &= CoreAuditEvent.objects.count() == before_audit+1
    try:
        CoreIdentity.objects.filter(pk=identity_id).update(state="SUSPENDED", version=2)
        refused("core_revocation_closed", lambda: svc.login(command("core-revoked"), supplied), "AUTH_DENIED")
    finally:
        CoreIdentity.objects.filter(pk=identity_id).update(state="ACTIVE", version=1)
    try:
        m.AuthLocalTrustSelection.objects.filter(pk=selection.pk).update(is_current=False)
        refused("trust_revocation_closed", lambda: svc.login(command("trust-revoked"), supplied), "AUTH_DENIED")
    finally:
        m.AuthLocalTrustSelection.objects.filter(pk=selection.pk).update(is_current=True)
    audit_failure_command = command("audit-failure")
    before = (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    refused("audit_failure_rollback", lambda: service(1).login(audit_failure_command, supplied), "AUTH_AUDIT_UNAVAILABLE")
    out["audit_failure_rollback"] &= before == (m.AuthSession.objects.count(), m.AuthToken.objects.count()) and not m.AuthOperation.objects.filter(operation_ref=audit_failure_command.operation_id).exists()
    unknown_command = command("unknown-commit")
    connection = connections["default"]
    real_commit = connection.commit
    fired = {"value": False}
    def uncertain_commit():
        should_fire = not fired["value"] and m.AuthOperation.objects.filter(operation_ref=unknown_command.operation_id).exists()
        real_commit()
        if should_fire:
            fired["value"] = True
            raise OperationalError("synthetic-after-real-commit")
    with patch.object(connection, "commit", uncertain_commit):
        unknown = svc.login(unknown_command, supplied)
    out["unknown_commit_no_secret"] = fired["value"] and unknown.outcome is AuthOutcome.UNKNOWN and unknown.emission is None and m.AuthOperation.objects.using("peer").filter(operation_ref=unknown_command.operation_id).exists()
    before = (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    repeated = svc.login(unknown_command, supplied)
    out["unknown_retry_no_reissue"] = repeated.outcome is AuthOutcome.REAUTH_REQUIRED and repeated.emission is None and before == (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    for index in range(10):
        active = m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").count()
        if active >= 5:
            break
        svc.login(command("fill-"+str(index)), supplied)
    before_ids = tuple(m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").order_by("id").values_list("id", flat=True))
    refused("ordinary_limit", lambda: svc.login(command("sixth"), supplied), "AUTH_SESSION_LIMIT")
    out["ordinary_limit"] &= len(before_ids) == 5 and before_ids == tuple(m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").order_by("id").values_list("id", flat=True))
    replaced = svc.login(command("replace"), replace(supplied, replace_session_id=session.pk))
    session.refresh_from_db()
    out["explicit_replacement"] = replaced.outcome is AuthOutcome.ISSUED and session.state == "REVOKED" and not m.AuthToken.objects.filter(session=session).exclude(state="REVOKED").exists() and m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").count() == 5
    candidate = m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").first()
    previous_version = candidate.version
    before = (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    refused("replacement_audit_failure_rollback", lambda: service(1).login(command("replace-audit-failure"), replace(supplied, replace_session_id=candidate.pk)), "AUTH_AUDIT_UNAVAILABLE")
    candidate.refresh_from_db()
    out["replacement_audit_failure_rollback"] &= candidate.state == "ACTIVE" and candidate.version == previous_version and before == (m.AuthSession.objects.count(), m.AuthToken.objects.count())
    admin = replace(supplied, category=SessionCategory.ADMIN)
    svc.login(command("admin-one"), admin)
    svc.login(command("admin-two"), admin)
    refused("admin_separate_limit", lambda: svc.login(command("admin-three"), admin), "AUTH_SESSION_LIMIT")
    out["admin_separate_limit"] &= m.AuthSession.objects.filter(category="ADMIN", state="ACTIVE").count() == 2 and m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").count() == 5
    refused("target_replacement_refused", lambda: svc.login(command("wrong-replace"), replace(supplied, replace_session_id=new_uuid7())), "AUTH_TARGET_INVALID")
    free = m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").first()
    m.AuthSession.objects.filter(pk=free.pk).update(state="REVOKED", revoked_at=clock.now(), version=F("version")+1)
    m.AuthToken.objects.filter(session=free).update(state="REVOKED", version=F("version")+1)
    barrier = threading.Barrier(2)
    results, closed = [], []
    def contender(index):
        raw = []
        try:
            barrier.wait(timeout=5)
            result = service().login(command("concurrent-"+str(index)), supplied)
            results.append(result.outcome.value)
        except AuthServiceError as error:
            results.append(error.code)
        except Exception as error:
            results.append(type(error).__name__)
        finally:
            for alias in ("default", "peer"):
                conn = connections[alias]
                if conn.connection is not None:
                    raw.append(conn.connection)
                conn.close()
            closed.append(all(bool(connection.closed) for connection in raw))
    workers = [threading.Thread(target=contender, args=(index,)) for index in range(2)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(12)
    out["last_slot_concurrent"] = not any(worker.is_alive() for worker in workers) and sorted(results) == ["AUTH_SESSION_LIMIT", "ISSUED"] and m.AuthSession.objects.filter(category="ORDINARY", state="ACTIVE").count() == 5
    out["thread_connections_closed"] = len(closed) == 2 and all(closed)
    return out


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True)
    result["real_components"] = ["PostgresLocalAuthService", "PostgresLocalTrustSource", "PostgresIdentityAssuranceSource", "RuntimeTrustedFactsProvider", "RuntimeAuthorizationDecider", "PostgresAuditParticipant"]
    result["plan_operator_key_governance"] = "FIXTURES_EXPLICITES"
    result["full_p0_activation"] = False
    return result
