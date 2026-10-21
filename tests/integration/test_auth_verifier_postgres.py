"""Auth PG réel ; ports Core/confiance/assurance doublés, sans qualification commune C04."""
from __future__ import annotations

EXPECTED_CASES = ("password_verified", "single_factor_only", "explicit_assurance", "repeat_without_mutation", "new_transaction_refused", "outside_transaction_refused", "wrong_password_refused", "missing_mapping_refused", "request_binding", "alias_binding", "operation_binding", "gate_generation", "credential_revision", "binding_disabled", "core_revoked", "core_version", "assurance_missing", "trust_withdrawn", "password_freshness_boundary", "access_verified", "access_deadline", "session_revoked", "token_revoked", "refresh_not_access", "wrong_facade", "access_expiry_boundary", "policy_reduction", "metadata_credential_platform", "metadata_session_real", "metadata_unknown_closed", "metadata_missing_closed", "metadata_context_from_row", "metadata_operation_binding", "metadata_new_tx_binding", "source_preadmission_owner", "source_before_commit", "source_metadata_boundaries", "source_revoke_between", "source_credential_between", "source_freshness_not_reset", "source_closed", "source_operation_binding")


def scenarios():
    import datetime
    from dataclasses import replace
    from django.apps import apps
    from django.db import transaction
    from pixs.auth import models as m
    from pixs.auth.identifiers import new_uuid7, identity_reference
    from pixs.auth.passwords import hash_password
    from pixs.auth.tokens import new_token, TokenKind, token_fingerprint
    from pixs.auth.policy import SessionCategory
    from pixs.auth.runtime_verifier import (AuthVerificationError, LocalTrustProfile, prepare_password_verifier, prepare_token_verifier, acquire_auth_policy_guard)
    from pixs.core.authz.ports import Request, RevocationStatus
    from pixs.core.authz.policy import IdentityAssurance, AuthenticationAssurance, FederationTrust
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.dto import CorePageItem

    cases = {}
    now = datetime.datetime.now(datetime.timezone.utc)
    context = ScopeContext(ScopeType.PLATFORM)
    gate = m.AuthAccountGate.objects.create(identity_id=new_uuid7())
    actor = identity_reference(gate.pk)
    request = Request("auth-decision", actor, actor, "pixs.auth.session.create", context, "auth-correlation")
    binding = m.AuthBinding.objects.create(identity=gate, provider_id="local-test", issuer="qualified-fixture", external_subject="explicit-subject", enabled=True)
    password = "Vecteur public de qualification C03, aucun secret réel"
    credential = m.AuthPasswordCredential.objects.create(binding=binding, password_hash=hash_password(password), enabled=True)
    policy = m.AuthPolicyRow.objects.create(policy_id="qualified-fixture", policy_version="1.0.0", origin="fixture-explicite", scope_type="PLATFORM", category="ORDINARY", idle_seconds=600, absolute_seconds=3600, access_seconds=300, freshness_seconds=120, max_sessions=3, is_current=True)
    profile = LocalTrustProfile("local-test", "1.0.0", binding.provider_id, binding.issuer, FederationTrust.TRUSTED)

    class Clock:
        def __init__(self, initial):
            self.value = initial
        def now(self):
            return self.value
    class Trust:
        value = profile
        def resolve(self, profile_id, request, *, alias, operation_id):
            return self.value
    class Assurance:
        value = IdentityAssurance.CLAIMED
        def resolve(self, identity_ref, request, *, alias, operation_id):
            return self.value
    class Facts:
        state = "ACTIVE"
        version = 1
        def read_facts(self, kind, refs, ctx, alias, limit):
            if (kind, refs, ctx, alias, limit) != ("IDENTITY", (actor,), context, "default", 1):
                raise AssertionError("FACT_PORT_BINDING")
            return (CorePageItem("IDENTITY", actor, context, self.version, "ACTIVE", "RETAINED", None, None, None, (("identity_id", str(gate.pk)), ("identity_type", "HUMAN"), ("state", self.state))),)
    clock, trust, assurance, facts = Clock(now), Trust(), Assurance(), Facts()
    common = dict(request=request, alias="default", operation_id="auth-operation", profile=profile, trust_source=trust, assurance_source=assurance, facts_reader=facts, clock=clock)

    def password_verifier(**updates):
        args = dict(common, external_subject=binding.external_subject, password=password, category=SessionCategory.ORDINARY)
        args.update(updates)
        return prepare_password_verifier(**args)

    def revalidate(verifier, **updates):
        args = dict(alias="default", operation_id="auth-operation")
        args.update(updates)
        return verifier.revalidate(request, **args)

    def refused(name, action):
        try:
            action()
        except AuthVerificationError:
            cases[name] = True
        else:
            cases[name] = False

    verifier = password_verifier()
    before = {model._meta.db_table: model.objects.count() for model in apps.get_app_config("pixs_auth").get_models()}
    with transaction.atomic():
        auth, status = revalidate(verifier)
        cases["password_verified"] = auth.digital_identity_id == actor and status is RevocationStatus.ACTIVE and auth.session_id is None
        cases["single_factor_only"] = auth.methods == ("PASSWORD",) and auth.authentication_assurance is AuthenticationAssurance.SINGLE_FACTOR
        cases["explicit_assurance"] = auth.identity_assurance is IdentityAssurance.CLAIMED
        again, status_again = revalidate(verifier)
        after = {model._meta.db_table: model.objects.count() for model in apps.get_app_config("pixs_auth").get_models()}
        cases["repeat_without_mutation"] = auth == again and status_again is status and before == after
    with transaction.atomic():
        refused("new_transaction_refused", lambda: revalidate(verifier))
    refused("outside_transaction_refused", lambda: revalidate(password_verifier()))
    refused("wrong_password_refused", lambda: password_verifier(password="autre vecteur public"))
    refused("missing_mapping_refused", lambda: password_verifier(external_subject="absent"))
    for name, mutate in (("request_binding", lambda v: v.revalidate(replace(request, action_id="another-action"), alias="default", operation_id="auth-operation")), ("alias_binding", lambda v: revalidate(v, alias="peer")), ("operation_binding", lambda v: revalidate(v, operation_id="another-operation"))):
        v = password_verifier()
        with transaction.atomic():
            refused(name, lambda: mutate(v))

    def changed(name, mutate, factory=password_verifier):
        v = factory()
        with transaction.atomic():
            mutate()
            refused(name, lambda: revalidate(v))
            transaction.set_rollback(True)

    changed("gate_generation", lambda: m.AuthAccountGate.objects.filter(pk=gate.pk).update(session_generation=2))
    changed("credential_revision", lambda: m.AuthPasswordCredential.objects.filter(pk=credential.pk).update(version=2))
    changed("binding_disabled", lambda: m.AuthBinding.objects.filter(pk=binding.pk).update(enabled=False))
    for name, obj, attribute, value in (("core_revoked", facts, "state", "REVOKED"), ("core_version", facts, "version", 2), ("assurance_missing", assurance, "value", None), ("trust_withdrawn", trust, "value", None), ("password_freshness_boundary", clock, "value", now+datetime.timedelta(seconds=120))):
        v = password_verifier()
        previous = getattr(obj, attribute)
        try:
            setattr(obj, attribute, value)
            with transaction.atomic():
                refused(name, lambda: revalidate(v))
        finally:
            setattr(obj, attribute, previous)

    started = now-datetime.timedelta(seconds=60)
    session = m.AuthSession.objects.create(identity=gate, binding=binding, credential=credential, category="ORDINARY", facade="API", scope_type="PLATFORM", policy=policy, generation=1, token_generation=1, credential_revision=1, binding_revision=1, core_identity_version=1, created_at=started, authenticated_at=started, last_activity_at=started, idle_expires_at=started+datetime.timedelta(seconds=600), absolute_expires_at=started+datetime.timedelta(seconds=3600), context_expires_at=started+datetime.timedelta(seconds=3600), state="ACTIVE")
    opaque = new_token()
    row = m.AuthToken.objects.create(session=session, digest=token_fingerprint(opaque, TokenKind.ACCESS), kind="ACCESS", state="ACTIVE", issued_at=now, expires_at=now+datetime.timedelta(seconds=900), session_generation=1)

    def token_verifier(**updates):
        args = dict(common, token=opaque, kind=TokenKind.ACCESS)
        args.update(updates)
        return prepare_token_verifier(**args)

    v = token_verifier()
    with transaction.atomic():
        auth, status = revalidate(v)
        cases["access_verified"] = auth.session_id == str(session.pk) and auth.credential_id == str(credential.pk) and status is RevocationStatus.ACTIVE
        cases["access_deadline"] = auth.expires_at == now+datetime.timedelta(seconds=300) and auth.authentication_time == started
    changed("session_revoked", lambda: m.AuthSession.objects.filter(pk=session.pk).update(state="REVOKED", revoked_at=now), token_verifier)
    changed("token_revoked", lambda: m.AuthToken.objects.filter(pk=row.pk).update(state="REVOKED"), token_verifier)
    refused("refresh_not_access", lambda: token_verifier(kind=TokenKind.REFRESH))
    refused("wrong_facade", lambda: token_verifier(kind=TokenKind.WEB_SESSION))
    v = token_verifier()
    try:
        clock.value = now+datetime.timedelta(seconds=300)
        with transaction.atomic():
            refused("access_expiry_boundary", lambda: revalidate(v))
    finally:
        clock.value = now
    def reduce_policy():
        acquire_auth_policy_guard("default", exclusive=True)
        m.AuthPolicyRow.objects.filter(pk=policy.pk).update(access_seconds=1)
        clock.value = now+datetime.timedelta(seconds=1)
    try:
        changed("policy_reduction", reduce_policy, token_verifier)
    finally:
        clock.value = now
    from pixs.auth.resource_metadata import AuthResourceMetadataResolver
    meta = AuthResourceMetadataResolver(request=request, alias="default", operation_id="auth-operation")
    def ownership(resource, **updates):
        kwargs = dict(context=context, alias="default", operation_id="auth-operation")
        kwargs.update(updates)
        return meta.ownership(resource, **kwargs)
    with transaction.atomic():
        credential_ref = "pixs.auth.credential:"+str(credential.pk)
        session_ref = "pixs.auth.session:"+str(session.pk)
        cases["metadata_credential_platform"] = ownership(credential_ref).context == ScopeContext(ScopeType.PLATFORM)
        cases["metadata_session_real"] = ownership(session_ref).resource_id == session_ref and ownership(session_ref).context == context
        cases["metadata_unknown_closed"] = ownership("pixs.auth.token:"+str(row.pk)) is None
        cases["metadata_missing_closed"] = ownership("pixs.auth.session:"+str(new_uuid7())) is None
        values = {field.attname: getattr(session, field.attname) for field in session._meta.concrete_fields if not field.primary_key}
        values.update(scope_type="TENANT", tenant_id="tenant-fixture", scope_id=None)
        tenant_session = m.AuthSession.objects.create(**values)
        actual = ownership("pixs.auth.session:"+str(tenant_session.pk))
        cases["metadata_context_from_row"] = actual.context == ScopeContext(ScopeType.TENANT, "tenant-fixture") and actual.context != context
        refused("metadata_operation_binding", lambda: ownership(session_ref, operation_id="another-operation"))
    with transaction.atomic():
        refused("metadata_new_tx_binding", lambda: ownership(session_ref))
    from pixs.auth.invocation import AuthInvocationSource
    source = AuthInvocationSource(password_verifier())
    pre, pre_status = source.revalidate(request, alias="default", operation_id="auth-operation")
    with transaction.atomic(durable=True):
        owner_auth, owner_status = source.revalidate(request, alias="default", operation_id="auth-operation")
        final_auth, final_status = source.revalidate(request, alias="default", operation_id="auth-operation")
        cases["source_preadmission_owner"] = pre == owner_auth and pre_status is owner_status is RevocationStatus.ACTIVE
        cases["source_before_commit"] = owner_auth == final_auth and final_status is owner_status
    source.close()
    token_source = AuthInvocationSource(token_verifier())
    first_owner = token_source.ownership(session_ref, context=context, alias="default", operation_id="auth-operation")
    with transaction.atomic(durable=True):
        second_owner = token_source.ownership(session_ref, context=context, alias="default", operation_id="auth-operation")
        cases["source_metadata_boundaries"] = first_owner == second_owner and second_owner.context == context
    token_source.close()

    def source_changed(name, model, key, changes, restore):
        source = AuthInvocationSource(password_verifier())
        source.revalidate(request, alias="default", operation_id="auth-operation")
        try:
            model.objects.filter(pk=key).update(**changes)
            with transaction.atomic(durable=True):
                refused(name, lambda: source.revalidate(request, alias="default", operation_id="auth-operation"))
        finally:
            model.objects.filter(pk=key).update(**restore)
            source.close()
    source_changed("source_revoke_between", m.AuthAccountGate, gate.pk, {"session_generation": 2}, {"session_generation": 1})
    source_changed("source_credential_between", m.AuthPasswordCredential, credential.pk, {"enabled": False}, {"enabled": True})
    source = AuthInvocationSource(password_verifier())
    source.revalidate(request, alias="default", operation_id="auth-operation")
    try:
        clock.value = now+datetime.timedelta(seconds=120)
        with transaction.atomic(durable=True):
            refused("source_freshness_not_reset", lambda: source.revalidate(request, alias="default", operation_id="auth-operation"))
    finally:
        clock.value = now
        source.close()
    refused("source_closed", lambda: source.revalidate(request, alias="default", operation_id="auth-operation"))
    source = AuthInvocationSource(password_verifier())
    try:
        refused("source_operation_binding", lambda: source.revalidate(request, alias="default", operation_id="another-operation"))
    finally:
        source.close()
    return cases


def run(root_str):
    from auth_pg_test_support import run_in_auth_schema
    result = run_in_auth_schema(root_str, scenarios, EXPECTED_CASES)
    result["core_trust_assurance_ports"] = "DOUBLES_EXPLICITES"
    result["common_c04_c05_qualification"] = False
    return result
