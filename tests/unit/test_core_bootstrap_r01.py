"""Raccordement R01 : liaisons, refus ordinaires et restauration sans nouvel effet.

Les participants ci-dessous sont synthétiques ; ces tests ne prouvent ni
signature C03, ni audit C05 persistant, ni commit PostgreSQL.
"""
from __future__ import annotations

import datetime
import unittest
from dataclasses import replace
from unittest.mock import Mock, patch

from pixs.core.authz.decision import Decision
from pixs.core.authz.policy import Effect
from pixs.core.authz.ports import Request
from pixs.core.dto import BootstrapActInput, CommandEnvelope
from pixs.core.ports import (
    BootstrapServicePorts, CoreServicePorts, CorePortError, InstallationPlanSource,
)
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.core.services_bootstrap_facts import (
    BootstrapBindingError, check_act_binding, check_consumed_policy,
    check_request_binding, require_current_window,
)
from pixs.core.services_common import CoreServiceError, allow
from pixs.core.services_transactions import _attempt
from test_bootstrap_operator import make_facts, VALID_FROM, EXPIRES_AT, UUID7, StrSub


def request_for(facts, **changes):
    request = Request(facts.authorization_ref, facts.operator_subject_ref,
                      facts.resource_id, facts.action_id, facts.context, "corr-distincte")
    return replace(request, **changes)


def act_for(facts, **changes):
    act = BootstrapActInput(
        facts.operation_id, facts.plan_version, facts.installation_ref, "INSTALLER",
        facts.operator_proof_ref, facts.operator_subject_ref, facts.authorization_ref,
        facts.target_identity_ref, facts.target_tenant_ref, facts.closed_effects,
        ("CONFIRMED",), facts.context, "corr-distincte", None, "idem-01", "b" * 64, "1.0.0",
    )
    return replace(act, **changes)


class SyntheticClock:
    def now(self):
        return VALID_FROM


class SyntheticFactsProvider:
    def __init__(self, facts):
        self.facts = facts
    def resolve(self, request):
        return self.facts


class SyntheticDecider:
    def decide(self, request):
        return Decision(request.decision_id, Effect.ALLOW, "ALLOWED",
                        ("r01-policy", (("r01", "1.0.0"),)), (),
                        VALID_FROM, EXPIRES_AT)
    def revalidate_under_locks(self, request, *, alias, operation_id):
        return self.decide(request)


def bootstrap_ports(idempotence=None):
    return BootstrapServicePorts(
        object(), SyntheticDecider(), object(), object(), SyntheticClock(), None,
        object() if idempotence is None else idempotence, object(),
    )


class R01BindingTests(unittest.TestCase):
    def test_request_and_act_bound_without_conflating_correlation(self):
        facts = make_facts()
        request = request_for(facts)
        self.assertNotEqual(request.correlation_id, facts.authorization_ref)
        check_request_binding(facts, request, operation_id=facts.operation_id)
        check_act_binding(act_for(facts), facts)
        require_current_window(facts, VALID_FROM)

    def test_request_substitutions_fail(self):
        facts = make_facts()
        changes = [
            {"subject_id": "operator-other"}, {"resource_id": "pixs.core.bootstrap:other"},
            {"action_id": "pixs.core.bootstrap.other"}, {"decision_id": "corr-distincte"},
            {"context": ScopeContext(ScopeType.TENANT, "tenant-other")},
        ]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(BootstrapBindingError):
                check_request_binding(facts, request_for(facts, **change), operation_id=facts.operation_id)
        with self.assertRaises(BootstrapBindingError):
            check_request_binding(facts, request_for(facts), operation_id="other-op")

    def test_act_substitutions_fail(self):
        facts = make_facts()
        changes = [
            {"operator_subject_ref": "operator-other"}, {"operator_proof_ref": "proof-other"},
            {"installation_ref": "install-other"}, {"plan_version": "plan-other"},
            {"authorization_ref": "authorization-other"}, {"operation_id": "op-other"},
            {"target_identity_ref": "pixs.core.identity:" + UUID7.replace("8b4c", "8b4d")},
            {"target_tenant_ref": "pixs.core.tenant:other"},
            {"closed_effects": tuple(reversed(facts.closed_effects))},
        ]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(BootstrapBindingError):
                check_act_binding(act_for(facts, **change), facts)

    def test_expired_and_future_admission_fail(self):
        facts = make_facts()
        for now in (EXPIRES_AT, EXPIRES_AT + datetime.timedelta(seconds=1),
                    VALID_FROM - datetime.timedelta(seconds=1), VALID_FROM.replace(tzinfo=None)):
            with self.subTest(now=now), self.assertRaises(BootstrapBindingError):
                require_current_window(facts, now)

    def test_consumed_operation_requires_confirmed_same_operation(self):
        facts = make_facts()
        self.assertEqual(check_consumed_policy(facts, facts.operation_id, None), "FRESH")
        consumed = replace(facts, consumed_operation_id=facts.operation_id)
        self.assertEqual(check_consumed_policy(consumed, facts.operation_id, "result-confirmed"), "RESTORE_ONLY")
        for inspection in (None, "", False, StrSub("result-confirmed")):
            with self.subTest(inspection=inspection), self.assertRaises(BootstrapBindingError):
                check_consumed_policy(consumed, facts.operation_id, inspection)
        other = replace(facts, consumed_operation_id="other-op")
        with self.assertRaises(BootstrapBindingError):
            check_consumed_policy(other, facts.operation_id, "result-confirmed")
        with self.assertRaises(BootstrapBindingError):
            check_request_binding(other, request_for(other), operation_id="other-op")

    def test_inherited_plan_binding_is_closed(self):
        class MissingBinding(InstallationPlanSource):
            pass
        facts = make_facts()
        with self.assertRaises(CorePortError):
            MissingBinding().verify_operator_binding(act_for(facts), facts, alias="unused")

    def test_operator_facts_refused_by_ordinary_core_ports(self):
        facts = make_facts()
        ports = CoreServicePorts(SyntheticFactsProvider(facts), SyntheticClock(),
                                 SyntheticDecider(), object(), None, object(), object())
        with self.assertRaises(CoreServiceError) as caught:
            allow(ports, request_for(facts), under_locks=False, alias="unused", operation_id=facts.operation_id)
        self.assertEqual(caught.exception.code, "FAITS_INVALIDES")
        with self.assertRaises(CoreServiceError) as caught:
            allow(ports, request_for(facts), under_locks=False, alias="unused",
                  operation_id=facts.operation_id, _facts_source=lambda request: facts)
        self.assertEqual(caught.exception.code, "SOURCE_INTERDITE")

    def test_bootstrap_admission_uses_disjoint_facts_without_creating_identity(self):
        facts = make_facts()
        accepted, decision = allow(bootstrap_ports(), request_for(facts), under_locks=False,
                                   alias="unused", operation_id=facts.operation_id,
                                   _facts_source=lambda request: facts)
        self.assertIs(accepted, facts)
        self.assertIs(decision.effect, Effect.ALLOW)
        self.assertFalse(hasattr(accepted, "auth"))
        self.assertFalse(hasattr(accepted, "digital_identity_id"))

    def test_consumed_without_idempotent_result_never_calls_apply(self):
        facts = make_facts(consumed_operation_id="op-01")
        request = request_for(facts)
        envelope = CommandEnvelope(request, facts.operation_id, "idem-01", "b" * 64,
                                   "1.0.0", request.correlation_id, None)
        idempotence = Mock()
        idempotence.verify_staged.return_value = None
        idempotence.restore_confirmed.return_value = None
        ctx = Mock()
        apply = Mock()
        decision = SyntheticDecider().decide(request)
        with patch("pixs.core.services_transactions.acquire_catalog_guard"), \
             patch("pixs.core.services_transactions.lock_scopes"), \
             patch("pixs.core.services_transactions.allow", return_value=(facts, decision)), \
             patch("pixs.core.services_transactions.published_profile", return_value=(None, False, False)), \
             patch("pixs.core.services_transactions.MutationContext", return_value=ctx):
            with self.assertRaises(CoreServiceError) as caught:
                _attempt(bootstrap_ports(idempotence), envelope=envelope, alias="unused",
                         scopes=("bootstrap:install-01",), apply=apply, payload_refs=(),
                         facts_source=lambda request: facts,
                         state={"token": "synthetic-token", "command_type": "pixs.core.bootstrap.apply:v1"})
        self.assertEqual(caught.exception.code, "ISSUE_INCONNUE")
        apply.assert_not_called()


if __name__ == "__main__":
    unittest.main()
