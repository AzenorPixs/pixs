"""Préparation PDP interne distincte de l’acquittement d’audit public.

Fixtures mémoire uniquement ; aucune preuve d’authentification, d’audit
persistant, de session ou de commit n’est produite par ces tests.
"""
import unittest

from pixs.core import authz as Z
from pixs.core.authz.decision import _prepare_detailed
from pixs.core.scope.context import ScopeContext, ScopeType
from test_pdp_decision import (
    T0, _Audit, _Clock, _Provider, _catalog, _facts, _limits, _policy,
    _request, _topology,
)


def platform_inputs():
    context = ScopeContext(ScopeType.PLATFORM)
    policy = _policy(scope_ctx=context, obligations=(Z.Obligation("AUDIT"),))
    snapshot = Z.Snapshot("e1", _catalog(), _limits(), (policy,))
    return _request(context), snapshot, _Provider(_facts(ctx=context))


class RuntimeAdmissionPreparationTests(unittest.TestCase):
    def test_preparation_without_session_does_not_create_one(self):
        facts = _facts()
        self.assertIsNone(facts.auth.session_id)
        request = _request()
        snapshot = Z.Snapshot("e1", _catalog(), _limits(), (_policy(),))
        decision, status, view = _prepare_detailed(
            request, snapshot, _Provider(facts), _Clock(T0), _topology())
        self.assertIs(decision.effect, Z.Effect.ALLOW)
        self.assertEqual(status, "ALLOW")
        self.assertEqual(decision.decision_id, request.decision_id)
        self.assertEqual(view[1], request.subject_id)
        self.assertIsNone(facts.auth.session_id)

    def test_public_platform_allow_still_requires_real_acknowledgement(self):
        request, snapshot, provider = platform_inputs()
        prepared, _, _ = _prepare_detailed(request, snapshot, provider, _Clock(T0), _topology())
        self.assertIs(prepared.effect, Z.Effect.ALLOW)
        self.assertEqual(prepared.obligations, ("AUDIT",))
        sink = _Audit(False)
        public = Z.authorize(request, snapshot, provider, _Clock(T0), sink, _topology())
        self.assertIs(public.effect, Z.Effect.DENY)
        self.assertEqual(len(sink.events), 1)

    def test_public_audited_result_matches_preparation_when_acknowledged(self):
        request, snapshot, provider = platform_inputs()
        prepared, _, _ = _prepare_detailed(request, snapshot, provider, _Clock(T0), _topology())
        sink = _Audit(True)
        public = Z.authorize(request, snapshot, provider, _Clock(T0), sink, _topology())
        self.assertEqual(public, prepared)
        self.assertEqual(len(sink.events), 1)

    def test_default_deny_keeps_public_audit(self):
        request = _request()
        snapshot = Z.Snapshot("e1", _catalog(), _limits(), ())
        provider = _Provider(_facts())
        prepared, _, _ = _prepare_detailed(request, snapshot, provider, _Clock(T0), _topology())
        self.assertIs(prepared.effect, Z.Effect.DENY)
        sink = _Audit(True)
        public = Z.authorize(request, snapshot, provider, _Clock(T0), sink, _topology())
        self.assertEqual(public, prepared)
        self.assertEqual(len(sink.events), 1)

    def test_source_failure_is_closed_before_public_audit(self):
        request = _request()
        snapshot = Z.Snapshot("e1", _catalog(), _limits(), (_policy(),))
        provider = _Provider(exc=RuntimeError("synthetic-source-unavailable"))
        prepared, status, _ = _prepare_detailed(request, snapshot, provider, _Clock(T0), _topology())
        self.assertIs(prepared.effect, Z.Effect.DENY)
        self.assertEqual(status, "ERROR")
        sink = _Audit(True)
        public = Z.authorize(request, snapshot, provider, _Clock(T0), sink, _topology())
        self.assertIs(public.effect, Z.Effect.DENY)
        self.assertEqual(len(sink.events), 1)

    def test_public_acknowledgement_remains_exact_true(self):
        for response in (1, "true", object(), None):
            with self.subTest(response_type=type(response).__name__):
                request, snapshot, provider = platform_inputs()
                sink = _Audit(response)
                public = Z.authorize(request, snapshot, provider, _Clock(T0), sink, _topology())
                self.assertIs(public.effect, Z.Effect.DENY)
                self.assertEqual(len(sink.events), 1)


if __name__ == "__main__":
    unittest.main()
