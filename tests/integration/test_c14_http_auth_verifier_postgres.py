"""Factory publique C14/Auth : PostgreSQL et admission C03/C04/C05 réels.

Les secrets de session produits par la recette restent dans le processus
confiné au schéma jetable. Aucun transport HTTP n'est qualifié ici.
"""
from __future__ import annotations

EXPECTED_CASES = (
    "real_auth_login_and_context", "actual_public_c03_verifier",
    "current_tx_authentication", "factory_has_no_auth_mutation",
    "bound_before_first_revalidation", "factory_outside_tx_closed",
    "bind_outside_tx_closed", "factory_alias_mismatch_closed",
    "factory_request_type_closed", "refresh_not_access",
    "raw_token_closed", "factory_context_mismatch_closed",
    "factory_subject_mismatch_closed", "operation_mismatch_closed",
    "request_mismatch_closed", "verifier_alias_mismatch_closed",
    "fresh_factory_in_new_tx", "token_revocation_revalidated",
    "core_identity_revocation_revalidated", "wrong_token_kind_closed",
    "historical_core_bridge_preserved", "same_tx_binding_repeatable",
)


def scenarios():
    import datetime
    from dataclasses import replace
    from django.apps import apps
    from django.db import transaction
    from auth_service_fixture import make_auth_service_fixture
    from pixs.auth.api_request_source import ApiRequestSource, ApiRequestSourceError
    from pixs.auth.contracts import AuthOutcome
    from pixs.auth.identifiers import identity_reference, new_uuid7
    from pixs.auth.models import AuthToken
    from pixs.auth.runtime_verifier import AuthAuthenticationVerifier, AuthVerificationError
    from pixs.auth.tokens import TokenKind
    from pixs.core.authz.ports import Request, RevocationStatus
    from pixs.core.persistence.models_identity import CoreIdentity
    from pixs.core.query_source import CoreFactSource
    from pixs.core.scope.context import ScopeContext, ScopeType

    f = make_auth_service_fixture()
    f["clock"].now = lambda: datetime.datetime.now(datetime.timezone.utc)
    login = f["login"]("c14-http-factory")
    assert login.outcome is AuthOutcome.ISSUED and login.emission.access is not None
    token = login.emission.access
    source = ApiRequestSource(
        alias="default", profile_id=f["profile"].profile_id,
        trust_source=f["trust"], assurance_source=f["assurance"],
        facts_reader=CoreFactSource(), clock=f["clock"], max_identifier_chars=4096)
    actor = source.resolve_token(context=f["context"], token=token, kind=TokenKind.ACCESS)
    req = source.request(actor=actor, resource_id="c14-ressource-opaque",
                         action_id="get_desired_pzt", correlation_id="c14-http-correlation",
                         decision_id="c14-http-decision")
    cases = {"real_auth_login_and_context":
             actor.identity_ref == f["actor"] and actor.session_id == login.session.session_id}

    def factory(**updates):
        args = dict(request=req, alias="default", operation_id="c14-http-operation",
                    token=token, kind=TokenKind.ACCESS)
        args.update(updates)
        return source.token_verifier(**args)

    def verify(verifier, **updates):
        args = dict(alias="default", operation_id="c14-http-operation")
        args.update(updates)
        return verifier.revalidate(req, **args)

    def refused(name, action, exception):
        try:
            action()
        except exception:
            cases[name] = True
        else:
            cases[name] = False

    def counts():
        return {m._meta.db_table: m.objects.count()
                for m in apps.get_app_config("pixs_auth").get_models()}

    before = counts()
    with transaction.atomic():
        verifier = factory()
        cases["actual_public_c03_verifier"] = type(verifier) is AuthAuthenticationVerifier
        cases["factory_has_no_auth_mutation"] = counts() == before
        auth, status = verify(verifier)
        cases["current_tx_authentication"] = (
            auth.digital_identity_id == actor.identity_ref
            and auth.session_id == str(actor.session_id) and status is RevocationStatus.ACTIVE)
        verifier.bind_transaction(req, alias="default", operation_id="c14-http-operation")
        again, again_status = verify(verifier)
        cases["same_tx_binding_repeatable"] = again == auth and again_status is status

    with transaction.atomic():
        unused = factory()
    with transaction.atomic():
        refused("bound_before_first_revalidation", lambda: verify(unused), AuthVerificationError)
    refused("factory_outside_tx_closed", factory, ApiRequestSourceError)
    refused("bind_outside_tx_closed",
            lambda: verifier.bind_transaction(req, alias="default", operation_id="c14-http-operation"),
            AuthVerificationError)

    with transaction.atomic():
        refused("factory_alias_mismatch_closed", lambda: factory(alias="peer"), ApiRequestSourceError)
        refused("factory_request_type_closed", lambda: factory(request={}), ApiRequestSourceError)
        refused("refresh_not_access",
                lambda: factory(token=login.emission.refresh, kind=TokenKind.REFRESH),
                ApiRequestSourceError)
        refused("raw_token_closed", lambda: factory(token="vecteur brut interdit"), ApiRequestSourceError)
        refused("factory_context_mismatch_closed",
                lambda: factory(request=replace(req, context=ScopeContext(ScopeType.TENANT, "tenant opaque"))),
                ApiRequestSourceError)
        refused("factory_subject_mismatch_closed",
                lambda: factory(request=replace(req, subject_id=identity_reference(new_uuid7()))),
                ApiRequestSourceError)
        refused("wrong_token_kind_closed",
                lambda: factory(kind=TokenKind.WEB_SESSION), ApiRequestSourceError)
        fresh = factory()
        refused("operation_mismatch_closed",
                lambda: verify(fresh, operation_id="autre-operation"), AuthVerificationError)
        refused("request_mismatch_closed",
                lambda: fresh.revalidate(replace(req, action_id="autre-action"),
                                         alias="default", operation_id="c14-http-operation"),
                AuthVerificationError)
        refused("verifier_alias_mismatch_closed", lambda: verify(fresh, alias="peer"), AuthVerificationError)
        auth, status = verify(fresh)
        cases["fresh_factory_in_new_tx"] = (
            fresh is not verifier and auth.digital_identity_id == actor.identity_ref
            and status is RevocationStatus.ACTIVE)

    with transaction.atomic():
        fresh = factory()
        AuthToken.objects.filter(session_id=actor.session_id, kind="ACCESS").update(state="REVOKED")
        refused("token_revocation_revalidated", lambda: verify(fresh), AuthVerificationError)
        transaction.set_rollback(True)

    with transaction.atomic():
        fresh = factory()
        CoreIdentity.objects.filter(pk=f["identity"]).update(state="SUSPENDED", version=2)
        refused("core_identity_revocation_revalidated", lambda: verify(fresh), AuthVerificationError)
        transaction.set_rollback(True)

    # L'ancien bridge est volontairement utilisé hors TX, comme dans C06.
    with source.open_core_source(request=req, operation_id="c14-historical-core",
                                 token=token, kind=TokenKind.ACCESS) as historical:
        auth, status = historical.revalidate(req, alias="default", operation_id="c14-historical-core")
        cases["historical_core_bridge_preserved"] = (
            auth.digital_identity_id == actor.identity_ref and status is RevocationStatus.ACTIVE)
    return cases


def run(root_str):
    from c14_pg_test_support import run_in_c14_schema
    result = run_in_c14_schema(root_str, scenarios, EXPECTED_CASES)
    result["real_c03_c04_c05_login"] = True if result["real_pg"] else False
    result["http_transport_qualified"] = False
    return result
