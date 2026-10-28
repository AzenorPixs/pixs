"""C05 réel pour Agent ; politiques/identités/décisions sont des fixtures.

Le harness Auth sert seulement à l'isolation PG et aux migrations Core.
Cette recette ne qualifie ni authentification C03, ni autorisation C04,
ni transport PA/PZT. Les contrats de retour patchés sont identifiés.
"""
from __future__ import annotations
import datetime
import json
import sys
from dataclasses import replace

sys.path.insert(0, "src")
sys.path.insert(0, "tests/integration")
import auth_pg_test_support as harness

ROOT = "/home/devops/datas/pixs"
EXPECTED_CASES = (
    "generic_staging_visibility", "generic_commit_payload",
    "pdp_staging_contract", "combined_staging", "rollback_removes_record",
    "outside_tx_refused", "invalid_owner_refused", "invalid_event_scope_refused",
    "divergent_decision_refused", "expired_decision_refused",
    "forged_proof_refused", "bad_verifier_contract_refused",
    "policy_error_sanitized", "clock_error_sanitized",
    "programming_error_propagates", "invalid_text_refused",
)


def _cases():
    from unittest.mock import patch
    from django.db import transaction
    from pixs.agent.audit_adapter import AgentAuditAdapter, AgentAuditError
    from pixs.agent.identifiers import new_agent_uuid7
    from pixs.core.audit_contracts import AuditError, AuditPolicy, ExplicitAuditPolicySource
    from pixs.core.audit_sink import PostgresAuditParticipant
    from pixs.core.authz.decision import Decision
    from pixs.core.authz.ports import AuditEvent as PdpEvent
    from pixs.core.authz.policy import Effect
    from pixs.core.ports import StagedRef, TransactionProof
    from pixs.core.scope.context import ScopeContext, ScopeType
    from pixs.core.persistence.models_audit import CoreAuditEvent
    from pixs.kernel.audit_event import AuditEvent
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel

    class Clock:
        def now(self):
            return datetime.datetime.now(datetime.timezone.utc)

    class RollbackFixture(Exception):
        pass

    clock = Clock()
    context = ScopeContext(ScopeType.PLATFORM)
    policy = AuditPolicy("fixture:agent-audit", "1", "fixture", 1, 65536, 50,
                         (), "fixture:asset", ConfidentialityLevel.INTERNAL,
                         PersonalDataLevel.NONE)
    source = ExplicitAuditPolicySource(context, policy)
    owner = PostgresAuditParticipant(source, clock, "peer")
    adapter = AgentAuditAdapter(owner)
    cases = {}

    def uid():
        return str(new_agent_uuid7())

    def count():
        return CoreAuditEvent.objects.using("default").count()

    def event():
        return AuditEvent(uid(), clock.now().isoformat(), "fixture:actor", None,
                          "fixture:action", "fixture:resource-type",
                          "fixture:target", "OBSERVED", None, ("fixture:corr",),
                          ("fixture:cause",), "pixs.agent", "0.1.0")

    def pdp():
        now = clock.now()
        version = ("fixture:epoch", ())
        identity = uid()
        ev = PdpEvent(identity, "fixture:actor", "fixture:target", "fixture:action",
                      context, "fixture:corr", Effect.ALLOW, "ALLOWED", version, now)
        dec = Decision(identity, Effect.ALLOW, "ALLOWED", version, (),
                       now, now + datetime.timedelta(seconds=60))
        return ev, dec

    def stage(ev=None, op=None, token=None, port=adapter):
        return port.stage_generic(ev if ev is not None else event(),
                                  alias="default", operation_id=op or uid(),
                                  transaction_token=token or uid(), context=context)

    def refused(fn, expected):
        try:
            fn()
        except AgentAuditError as error:
            assert error.code == expected
            assert error.__cause__ is None
            return
        raise AssertionError("REFUS_ATTENDU")

    def rejected_tx(name, fn, expected):
        before = count()
        with transaction.atomic(using="default", durable=True):
            refused(fn, expected)
            assert count() == before
        assert count() == before
        cases[name] = True

    op, token, ev = uid(), uid(), event()
    with transaction.atomic(using="default", durable=True):
        ref = stage(ev, op, token)
        assert type(ref) is StagedRef
        assert (ref.operation_id, ref.alias, ref.transaction_token, ref.context,
                ref.staged_kind) == (op, "default", token, context, "audit")
        proof = TransactionProof(op, "default", token, context, (ref,), clock.now())
        assert adapter.verify_staged(proof) is None
        assert not CoreAuditEvent.objects.using("peer").filter(operation_id=op).exists()
    cases["generic_staging_visibility"] = True
    row = CoreAuditEvent.objects.using("peer").get(operation_id=op)
    assert row.generic_payload["actor_reference"] == ev.actor_reference
    assert row.generic_payload["resource_id"] == ev.resource_id
    assert row.generic_payload["action"] == ev.action
    assert row.generic_payload["correlation_ids"] == list(ev.correlation_ids)
    assert row.generic_payload["causation_ids"] == list(ev.causation_ids)
    cases["generic_commit_payload"] = True

    ev2, dec2 = pdp()
    op2, token2 = uid(), uid()
    with transaction.atomic(using="default", durable=True):
        ref2 = adapter.stage_decision(ev2, alias="default", operation_id=op2,
            transaction_token=token2, context=context, decision=dec2)
        assert type(ref2) is StagedRef and ref2.staged_kind == "audit"
    row2 = CoreAuditEvent.objects.using("peer").get(operation_id=op2)
    assert row2.pdp_payload["decision_id"] == ev2.decision_id
    assert row2.pdp_payload["effect"] == "ALLOW"
    cases["pdp_staging_contract"] = True

    op3, token3 = uid(), uid()
    ev3, dec3 = pdp()
    with transaction.atomic(using="default", durable=True):
        generic_ref = stage(event(), op3, token3)
        pdp_ref = adapter.stage_decision(ev3, alias="default", operation_id=op3,
            transaction_token=token3, context=context, decision=dec3)
        assert adapter.verify_staged(TransactionProof(op3, "default", token3,
            context, (generic_ref, pdp_ref), clock.now())) is None
    assert CoreAuditEvent.objects.using("peer").filter(operation_id=op3).count() == 2
    cases["combined_staging"] = True

    rop, rtoken = uid(), uid()
    before = count()
    try:
        with transaction.atomic(using="default", durable=True):
            stage(event(), rop, rtoken)
            raise RollbackFixture()
    except RollbackFixture:
        pass
    assert count() == before
    assert not CoreAuditEvent.objects.using("peer").filter(operation_id=rop).exists()
    cases["rollback_removes_record"] = True

    before = count()
    refused(lambda: stage(), "STAGING_IMPOSSIBLE")
    assert count() == before
    cases["outside_tx_refused"] = True
    class SubOwner(PostgresAuditParticipant):
        pass
    for wrong in (None, True, object(), object.__new__(SubOwner)):
        refused(lambda: AgentAuditAdapter(wrong), "PROPRIETAIRE_INVALIDE")
    cases["invalid_owner_refused"] = True
    rejected_tx("invalid_event_scope_refused", lambda: stage(ev2), "EVENEMENT_INVALIDE")
    rejected_tx("invalid_event_scope_refused",
                lambda: stage(replace(event(), tenant_reference="fixture:other")),
                "LIAISON_TENANT_DIVERGENTE")
    bad_decision = replace(dec2, decision_id=uid())
    rejected_tx("divergent_decision_refused", lambda: adapter.stage_decision(ev2,
        alias="default", operation_id=uid(), transaction_token=uid(),
        context=context, decision=bad_decision), "STAGING_IMPOSSIBLE")
    expired = replace(dec2, evaluated_at=dec2.evaluated_at-datetime.timedelta(seconds=120),
                      expires_at=dec2.evaluated_at-datetime.timedelta(seconds=60))
    rejected_tx("expired_decision_refused", lambda: adapter.stage_decision(ev2,
        alias="default", operation_id=uid(), transaction_token=uid(),
        context=context, decision=expired), "STAGING_IMPOSSIBLE")

    op4, token4 = uid(), uid()
    with transaction.atomic(using="default", durable=True):
        ref4 = stage(event(), op4, token4)
        proof4 = TransactionProof(op4, "default", token4, context, (ref4,), clock.now())
        assert adapter.verify_staged(proof4) is None
        forged_token = uid()
        forged_ref = replace(ref4, transaction_token=forged_token)
        forged_proof = replace(proof4, transaction_token=forged_token, staged=(forged_ref,))
        refused(lambda: adapter.verify_staged(forged_proof), "PREUVE_NON_VERIFIEE")
        # Contrat de retour simulé, distinct des preuves SQL réelles ci-dessus.
        with patch.object(PostgresAuditParticipant, "verify_staged", return_value="CONFIRMED"):
            refused(lambda: adapter.verify_staged(proof4), "PREUVE_NON_VERIFIEE")
    cases["forged_proof_refused"] = True
    cases["bad_verifier_contract_refused"] = True

    class BadSource:
        def resolve(self, **kwargs):
            raise AuditError("FIXTURE_POLICY_UNAVAILABLE")
    bad_policy = AgentAuditAdapter(PostgresAuditParticipant(BadSource(), clock, "peer"))
    rejected_tx("policy_error_sanitized", lambda: stage(port=bad_policy),
                "STAGING_IMPOSSIBLE")

    class BadClock:
        def now(self):
            return "date-invalide"
    bad_clock = AgentAuditAdapter(PostgresAuditParticipant(source, BadClock(), "peer"))
    rejected_tx("clock_error_sanitized", lambda: stage(port=bad_clock),
                "STAGING_IMPOSSIBLE")

    def bug(*args, **kwargs):
        raise TypeError("défaut de programmation fixture")
    before = count()
    with patch.object(PostgresAuditParticipant, "stage_generic", new=bug):
        try:
            with transaction.atomic(using="default", durable=True):
                stage()
        except TypeError:
            pass
        else:
            raise AssertionError("DEFAUT_MASQUE")
    assert count() == before
    cases["programming_error_propagates"] = True

    before = count()
    for invalid in ("x" + chr(0), "x" + chr(55296)):
        refused(lambda: stage(op=invalid), "LIAISON_INVALIDE")
    assert count() == before
    cases["invalid_text_refused"] = True
    assert set(cases) == set(EXPECTED_CASES)
    return cases


def main():
    result = harness.run_in_auth_schema(ROOT, _cases, EXPECTED_CASES,
                                       with_core=True, core_target="0002_core_audit")
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0 if (result["real_pg"] is True and set(result["cases"]) == set(EXPECTED_CASES)
                 and all(value is True for value in result["cases"].values())) else 1


if __name__ == "__main__":
    raise SystemExit(main())
