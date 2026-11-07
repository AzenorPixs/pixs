"""Recette O06 : Auth, C04, C05, Core et C06 reels sur schema jetable.

C09 et C10 restent les participants synthetiques declares par la fixture C06.
Le harnais existant possede migrations, masquage, schema et fermeture ; seules
ses sorties assainies sont imprimees. Aucun secret ne quitte le processus.
"""
from __future__ import annotations

EXPECTED_CASES = (
    "command_reelle_et_proposition_durable",
    "resultat_false_sans_command",
    "favorable_sans_permission_refuse",
    "droits_revoques_apres_proposition",
    "version_proprietaire_courante",
    "isolation_tenant_et_scope",
    "lecture_audit_autorisee",
    "correlation_sans_droit",
    "lecture_contexte_etranger_refusee",
    "audit_indisponible_sans_mutation",
    "explication_effacee_refusee",
    "pseudonymisation_et_retention",
    "transaction_externe_refusee",
)


def scenarios():
    import json
    from contextlib import contextmanager
    from dataclasses import replace
    from unittest.mock import patch
    from django.db import transaction
    from test_api_core_platform_postgres import make_http_fixture
    from pixs.auth.tokens import TokenKind, parse_token
    from pixs.auth.runtime_verifier import AuthVerificationError
    from pixs.backend.api_core_catalog import COMMANDS, command_resource_ref, parse_command_input
    from pixs.business_rules import RuleCatalog, encode_json_document, evaluate, parse_rule_document
    from pixs.business_rules.core_binding import ACTION_PROPOSED, BusinessRuleCoreBinding
    import pixs.business_rules.core_binding as binding_module
    from pixs.business_rules.evaluator import EvaluatorError
    from pixs.core.api_core_serializer_v1 import API_CORE_SERIALIZER_VERSION, command_content_sha256
    from pixs.core.audit_access import audit_candidate_references, filter_audit
    from pixs.core.audit_contracts import AuditError, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.policy import Effect
    from pixs.core.authz.ports import PortError
    from pixs.core.dto import CommandEnvelope, CoreMutationResult
    from pixs.core.ports import CorePortError
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.core.persistence.models_authz import CoreRole
    from pixs.core.persistence.models_identity import CoreUser
    from pixs.core.persistence.uuid7 import generate_uuid7
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.services_common import CoreServiceError
    from pixs.kernel.audit_field_redaction import AuditFieldRedaction, RedactionMode
    from pixs.kernel.data_governance import PersonalDataLevel

    h = make_http_fixture()
    f, grant = h["f"], h["grant"]
    h["grant_auth"]("pixs.auth.session.create", f["actor"])
    response, login = h["call"](
        "POST", "/api/v1/platform/auth/login",
        {"external_subject": f["supplied"].external_subject, "password": f["supplied"].password},
        headers={"HTTP_IDEMPOTENCY_KEY": "o06-login"},
    )
    assert response.status_code == 200, "LOGIN_REFUSE"
    token = parse_token(login["data"]["access_token"])
    actor = h["source"].resolve_token(context=f["context"], token=token, kind=TokenKind.ACCESS)
    marker = "marqueur-prive-inerte-o06"
    document = {
        "profile_version": 1, "rule_id": "r-o06", "rule_version": "v1", "owner": "pixs.core",
        "input_schema": {"valeur": {"type": "string", "required": True}},
        "expression": {"op": "eq", "args": [{"field": "valeur"}, {"literal": marker}]},
        "cases": [
            {"case_id": "oui", "inputs": {"valeur": marker}, "expected": True},
            {"case_id": "non", "inputs": {"valeur": "non"}, "expected": False},
        ],
    }
    rule = parse_rule_document(encode_json_document(document))
    catalog = RuleCatalog((rule,))
    binding = BusinessRuleCoreBinding("pixs.core", "create-user", catalog)
    cases = {}
    uid = lambda: str(generate_uuid7())

    def expect(call, kinds, code=None):
        try:
            call()
        except kinds as error:
            if code is not None:
                assert getattr(error, "code", None) == code, "CODE_REFUS_DIVERGENT"
            return error
        raise AssertionError("REFUS_ATTENDU")

    def current_ports(request, operation, auth):
        original = h["composition"].core_ports(
            request=request, operation_id=operation, authentication_source=auth)
        policy = replace(original.audit.policy(request.context, "default"),
                         governance_ref="synthetic:asset", personal=PersonalDataLevel.NONE)
        audit = PostgresAuditParticipant(
            ExplicitAuditPolicySource(request.context, policy), f["clock"], "peer")
        supplied = replace(original, audit=audit)
        if request.action_id != "pixs.core.audit.read":
            return supplied
        # La composition C06 n enregistre pas AUDIT implicitement. Cette
        # composition de recette declare les deux ports C05 dans C04 reel.
        from pixs.core.persistence.models_authz import CorePolicy, decode_policy
        from pixs.core.authz.snapshot import Catalog, Limits
        from pixs.core.authz.filter_plan import FilterConfig
        from pixs.core.services_runtime_store import CoreAuthorizationStore
        from pixs.core.services_runtime_facts import RuntimeResourceOwner, RuntimeTrustedFactsProvider
        from pixs.core.services_runtime_decider import RuntimeAuthorizationDecider
        from pixs.core.services_runtime_filter import RuntimeCandidateSource, RuntimeSourceFilterProvider
        from pixs.core.audit_sink import PostgresAuditSink
        from pixs.core.audit_access import audit_resource_ownership
        resources = set(h["references"]) | {request.resource_id, f["actor"]}
        actions, subjects = {request.action_id}, {f["actor"]}
        contexts = set(h["contexts"]) | {request.context}
        for definition in CorePolicy.objects.using("default").values_list("definition", flat=True):
            policy_definition = decode_policy(definition)
            resources.update(policy_definition.resource.values)
            actions.update(policy_definition.action.values)
            subjects.update(policy_definition.subject.values)
            contexts.update(policy_definition.scope.contexts)
        store = CoreAuthorizationStore(
            alias="default", installation_ref="o06-audit-fixture", base_epoch="o06-audit-v1",
            catalog=Catalog(tuple(sorted(subjects)), tuple(sorted(resources)), tuple(sorted(actions)),
                tuple(sorted(contexts, key=lambda c: (c.scope_type.value, c.tenant_id or "", c.scope_id or ""))), ()),
            limits=Limits(512, 512, 16, 100, 100, 512, 512, 512, 10000000, 60, 3600))
        def ownership(reference, *, context, alias, operation_id):
            return audit_resource_ownership(resource_id=reference, context=context, alias=alias)
        facts = RuntimeTrustedFactsProvider(
            store=store, authentication_source=auth, request=request, operation_id=operation,
            additional_owners=(RuntimeResourceOwner("audit:", ownership),))
        decider = RuntimeAuthorizationDecider(
            store=store, facts_provider=facts, clock=f["clock"], request=request, operation_id=operation)
        source_filter = RuntimeSourceFilterProvider(
            store, facts, f["clock"], PostgresAuditSink(audit, "default", request.context, operation),
            FilterConfig(128), request, operation,
            additional_sources=(RuntimeCandidateSource("AUDIT", "audit:",
                                audit_candidate_references, audit_resource_ownership),))
        return replace(supplied, facts_provider=facts, decider=decider, filter_provider=source_filter)

    @contextmanager
    def command(name, body, *, authorized=True):
        correlation = uid()
        dto = parse_command_input(name, body, context=f["context"], correlation_id=correlation,
                                  limits=h["composition"].input_limits)
        resource = command_resource_ref(name, dto)
        action = COMMANDS[name]["action"]
        if authorized:
            grant(action, resource)
        request = h["source"].request(actor=actor, resource_id=resource, action_id=action,
                                      correlation_id=correlation, decision_id=uid())
        operation = uid()
        with h["source"].open_core_source(request=request, operation_id=operation,
                                         token=token, kind=TokenKind.ACCESS) as auth:
            ports = current_ports(request, operation, auth)
            envelope = CommandEnvelope(
                request, operation, "o06-" + operation,
                command_content_sha256(command_type=action + ":v1", dto=dto, context=request.context),
                API_CORE_SERIALIZER_VERSION, correlation, None)
            yield dto, envelope, ports

    def invoke(selected, dto, envelope, ports, value=marker):
        return selected.invoke(
            dto=dto, envelope=envelope, ports=ports, alias="default",
            inputs=encode_json_document({"valeur": value}), rule_id=rule.rule_id,
            rule_version=rule.rule_version, correlation_id=envelope.correlation_id)

    def proposal_count():
        return CoreAuditEvent.objects.using("peer").filter(
            kind="GENERIC_AUDIT", generic_payload__action=ACTION_PROPOSED).count()

    def proposal_for(correlation):
        rows = list(CoreAuditEvent.objects.using("peer").filter(
            kind="GENERIC_AUDIT", generic_payload__action=ACTION_PROPOSED,
            generic_payload__correlation_ids=[correlation]))
        assert len(rows) == 1, "PROPOSITION_NON_UNIQUE"
        return rows[0]

    def read(reference, *, authorized=False, correlation=None, context=None):
        ctx = f["context"] if context is None else context
        with transaction.atomic(using="default", durable=True):
            h["references"].update(audit_candidate_references(
                kind="AUDIT", context=ctx, alias="default", limit=128))
        h["references"].add(reference)
        if authorized:
            grant("pixs.core.audit.read", reference, context=ctx)
        request = h["source"].request(
            actor=actor, resource_id=reference, action_id="pixs.core.audit.read",
            correlation_id=correlation or uid(), decision_id=uid())
        if ctx != request.context:
            request = replace(request, context=ctx)
        operation = uid()
        with h["source"].open_core_source(request=request, operation_id=operation,
                                         token=token, kind=TokenKind.ACCESS) as auth:
            ports = current_ports(request, operation, auth)
            return filter_audit(ports=ports, request=request, alias="default",
                                operation_id=operation, limit=10)

    identifier = generate_uuid7()
    with command("create-user", {"user_id": str(identifier)}) as (dto, envelope, ports):
        result = invoke(binding, dto, envelope, ports)
        policy = ports.audit.policy(envelope.request.context, "default")
        correlation = envelope.correlation_id
    assert result["dispatched"] is True and type(result["command_result"]) is CoreMutationResult
    assert result["evaluation"] == evaluate(rule, encode_json_document({"valeur": marker}), correlation)
    assert CoreUser.objects.using("peer").filter(pk=identifier).count() == 1, "EFFET_ABSENT"
    assert set(result) == {"evaluation", "audit_reference", "dispatched", "command_result"}
    row = proposal_for(correlation)
    assert result["audit_reference"] == "audit:" + str(row.record_id)
    assert row.retention_days == policy.retention_days and row.retention_days > 0
    assert row.generic_payload["result"] == "PROPOSED"
    assert json.loads(row.generic_payload["reason_or_error"]) == result["evaluation"]
    assert marker not in json.dumps(row.generic_payload), "FUITE_ENTREE"
    cases["command_reelle_et_proposition_durable"] = True

    identifier_false = generate_uuid7()
    with command("create-user", {"user_id": str(identifier_false)}) as (dto, envelope, ports):
        no_match = invoke(binding, dto, envelope, ports, "non")
        false_correlation = envelope.correlation_id
    assert no_match["evaluation"]["matched"] is False
    assert no_match["dispatched"] is False and no_match["command_result"] is None
    assert not CoreUser.objects.using("peer").filter(pk=identifier_false).exists()
    assert proposal_for(false_correlation).generic_payload["result"] == "PROPOSED"
    cases["resultat_false_sans_command"] = True

    identifier_denied = generate_uuid7()
    assert evaluate(rule, encode_json_document({"valeur": marker}), uid())["matched"] is True
    before = proposal_count()
    with command("create-user", {"user_id": str(identifier_denied)}, authorized=False) as args:
        expect(lambda: invoke(binding, *args), CoreServiceError, "DECISION_REFUSEE")
    assert not CoreUser.objects.using("peer").filter(pk=identifier_denied).exists()
    assert proposal_count() == before
    cases["favorable_sans_permission_refuse"] = True

    real_dispatch = binding_module.dispatch_command
    observed = {}

    def revoke_then_dispatch(name, *, dto, envelope, ports, alias):
        persisted = proposal_for(envelope.correlation_id)
        assert json.loads(persisted.generic_payload["reason_or_error"])["matched"] is True
        grant(COMMANDS[name]["action"], envelope.request.resource_id, effect=Effect.DENY)
        try:
            return real_dispatch(name, dto=dto, envelope=envelope, ports=ports, alias=alias)
        except CoreServiceError as error:
            observed["error"] = error
            raise

    identifier_revoked = generate_uuid7()
    with command("create-user", {"user_id": str(identifier_revoked)}) as args:
        revoked_correlation = args[1].correlation_id
        with patch.object(binding_module, "dispatch_command", new=revoke_then_dispatch):
            error = expect(lambda: invoke(binding, *args), CoreServiceError, "DECISION_REFUSEE")
    assert observed.get("error") is error, "ERREUR_PROPRIETAIRE_TRANSFORMEE"
    assert not CoreUser.objects.using("peer").filter(pk=identifier_revoked).exists()
    assert proposal_for(revoked_correlation).generic_payload["result"] == "PROPOSED"
    cases["droits_revoques_apres_proposition"] = True

    role_id = "o06-role"
    with command("create-role", {"role_id": role_id, "permission_ids": []}) as (dto, envelope, ports):
        real_dispatch("create-role", dto=dto, envelope=envelope, ports=ports, alias="default")
    role = CoreRole.objects.using("peer").get(role_id=role_id)
    first_version = role.version
    with command("set-role-permissions", {
            "role_id": role_id, "permission_ids": [], "expected_version": first_version}) as args:
        real_dispatch("set-role-permissions", dto=args[0], envelope=args[1], ports=args[2], alias="default")
    current_version = CoreRole.objects.using("peer").get(role_id=role_id).version
    assert current_version > first_version
    role_binding = BusinessRuleCoreBinding("pixs.core", "set-role-permissions", catalog)
    with command("set-role-permissions", {
            "role_id": role_id, "permission_ids": [], "expected_version": first_version}) as args:
        stale_correlation = args[1].correlation_id
        expect(lambda: invoke(role_binding, *args), CoreServiceError, "CONFLIT_CAS")
    assert CoreRole.objects.using("peer").get(role_id=role_id).version == current_version
    assert proposal_for(stale_correlation).generic_payload["result"] == "PROPOSED"
    cases["version_proprietaire_courante"] = True

    before = proposal_count()
    cross_id = generate_uuid7()
    with command("create-user", {"user_id": str(cross_id)}) as (dto, envelope, ports):
        for context in (ScopeContext(ScopeType.TENANT, "o06-autre", None),
                        ScopeContext(ScopeType.TENANT, "o06-autre", "o06-scope")):
            foreign_envelope = replace(envelope, request=replace(envelope.request, context=context))
            expect(lambda: invoke(binding, dto, foreign_envelope, ports),
                   EvaluatorError, "context_mismatch")
    assert proposal_count() == before and not CoreUser.objects.using("peer").filter(pk=cross_id).exists()
    cases["isolation_tenant_et_scope"] = True

    views = read(result["audit_reference"], authorized=True)
    assert len(views) == 1 and views[0].reference == result["audit_reference"], "LECTURE_NON_BORNEE"
    payload = json.loads(views[0].payload_json)
    explanation = json.loads(payload["reason_or_error"])
    assert explanation == result["evaluation"]
    assert set(explanation) == {"profile_version", "rule_id", "rule_version", "owner",
                                "correlation_id", "matched", "reason_codes"}
    assert marker not in views[0].payload_json and "valeur" not in payload["reason_or_error"]
    cases["lecture_audit_autorisee"] = True

    expect(lambda: read(no_match["audit_reference"], correlation=correlation),
           CoreServiceError, "DECISION_REFUSEE")
    cases["correlation_sans_droit"] = True

    forbidden_context_errors = (CorePortError, PortError, CoreServiceError, AuditError, AuthVerificationError)
    for context in (ScopeContext(ScopeType.TENANT, "o06-autre", None),
                    ScopeContext(ScopeType.TENANT, "o06-autre", "o06-scope")):
        expect(lambda: read(result["audit_reference"], correlation=correlation, context=context),
               forbidden_context_errors)
    cases["lecture_contexte_etranger_refusee"] = True

    identifier_tiny = generate_uuid7()
    before = proposal_count()
    with command("create-user", {"user_id": str(identifier_tiny)}) as (dto, envelope, ports):
        policy = replace(ports.audit.policy(envelope.request.context, "default"), max_event_bytes=10)
        tiny = PostgresAuditParticipant(ExplicitAuditPolicySource(envelope.request.context, policy),
                                       f["clock"], "peer")
        expect(lambda: invoke(binding, dto, envelope, replace(ports, audit=tiny)), AuditError, "AUDIT_CAPACITY")
    assert proposal_count() == before and not CoreUser.objects.using("peer").filter(pk=identifier_tiny).exists()
    cases["audit_indisponible_sans_mutation"] = True

    identifier_redacted = generate_uuid7()
    before = proposal_count()
    with command("create-user", {"user_id": str(identifier_redacted)}) as (dto, envelope, ports):
        policy = replace(ports.audit.policy(envelope.request.context, "default"),
                         redactions=(AuditFieldRedaction("generic.reason_or_error", RedactionMode.REDACTED, None),))
        redacted = PostgresAuditParticipant(ExplicitAuditPolicySource(envelope.request.context, policy),
                                           f["clock"], "peer")
        expect(lambda: invoke(binding, dto, envelope, replace(ports, audit=redacted)),
               EvaluatorError, "explanation_redacted")
    assert proposal_count() == before
    assert not CoreUser.objects.using("peer").filter(pk=identifier_redacted).exists()
    cases["explication_effacee_refusee"] = True

    identifier_pseudo = generate_uuid7()
    with command("create-user", {"user_id": str(identifier_pseudo)}) as (dto, envelope, ports):
        policy = replace(ports.audit.policy(envelope.request.context, "default"),
                         redactions=(AuditFieldRedaction("generic.actor_reference",
                                     RedactionMode.PSEUDONYMIZED_REFERENCE, "acteur-inerte-pseudonyme"),))
        audit = PostgresAuditParticipant(ExplicitAuditPolicySource(envelope.request.context, policy),
                                        f["clock"], "peer")
        pseudonymized = invoke(binding, dto, envelope, replace(ports, audit=audit))
        pseudo_correlation = envelope.correlation_id
    row = proposal_for(pseudo_correlation)
    assert row.generic_payload["actor_reference"] == "acteur-inerte-pseudonyme"
    assert json.loads(row.generic_payload["reason_or_error"]) == pseudonymized["evaluation"]
    assert row.retention_days == policy.retention_days and row.retention_days > 0
    assert CoreUser.objects.using("peer").filter(pk=identifier_pseudo).exists()
    cases["pseudonymisation_et_retention"] = True

    external_id = generate_uuid7()
    before = proposal_count()
    with command("create-user", {"user_id": str(external_id)}) as args:
        with transaction.atomic(using="default"):
            expect(lambda: invoke(binding, *args), EvaluatorError, "external_transaction")
    assert proposal_count() == before and not CoreUser.objects.using("peer").filter(pk=external_id).exists()
    cases["transaction_externe_refusee"] = True
    assert set(cases) == set(EXPECTED_CASES) and all(cases.values()), "CAS_INCOMPLETS"
    return cases


def run_real_business_rules_pg(root_str):
    from auth_pg_test_support import run_in_auth_schema
    return run_in_auth_schema(root_str, scenarios, EXPECTED_CASES, with_core=True,
                              core_target="0003_core_idempotence")


if __name__ == "__main__":
    import json
    from pathlib import Path
    outcome = run_real_business_rules_pg(str(Path(__file__).resolve().parents[2]))
    print(json.dumps(outcome, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if outcome.get("real_pg") and outcome.get("cleanup")
                     and outcome.get("conns_closed") else 1)
