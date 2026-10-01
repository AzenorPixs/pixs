"""Tests PDP decision via facade publique, deterministes."""

import dataclasses
import datetime
import unittest

from pixs.core import authz as Z
from pixs.core.scope import ScopeContext, ScopeType
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.scope.topology import ScopeNode, TopologySnapshot


def _utc(y, mo, d, h=0, mi=0, s=0):
    return datetime.datetime(y, mo, d, h, mi, s, tzinfo=datetime.timezone.utc)


T0 = _utc(2026, 1, 2, 12, 0, 0)


def _limits(**over):
    base = dict(
        max_policies=32, max_selector_values=32,
        max_conditions_per_policy=16, max_set_values=32,
        max_attributes=16, max_memberships=32,
        max_id_length=64, max_value_length=128,
        max_cost=1000000, ttl_seconds=60, max_freshness_seconds=600)
    base.update(over)
    return Z.Limits(**base)


def _ctx_t1():
    return ScopeContext(ScopeType.TENANT, "t1")


def _catalog(ctx=None):
    ctx = ctx if ctx is not None else _ctx_t1()
    plat = ScopeContext(ScopeType.PLATFORM)
    return Z.Catalog(
        ("s1", "s2"), ("r1", "r2"), ("a1", "a2"),
        (ctx, ScopeContext(ScopeType.TENANT, "t2"), plat),
        (("role", "STR"), ("level", "INT")))


def _policy(pid="p1", effect=None, scope_ctx=None, **kw):
    effect = effect if effect is not None else Z.Effect.ALLOW
    scope_ctx = scope_ctx if scope_ctx is not None else _ctx_t1()
    return Z.Policy(
        pid, "v1", "owner1", effect,
        Z.Selector("subject", ("s1",)),
        Z.Selector("resource", ("r1",)),
        Z.Selector("action", ("a1",)),
        Z.ScopeSelector((scope_ctx,)), **kw)


def _auth(ctx=None, t0=None):
    t0 = t0 if t0 is not None else T0
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.AuthenticationContext(
        "s1", "prov1", "iss1", "ext1",
        t0 - datetime.timedelta(seconds=10),
        t0 + datetime.timedelta(seconds=300),
        ("password",),
        Z.IdentityAssurance.VERIFIED,
        Z.AuthenticationAssurance.MULTI_FACTOR,
        Z.FederationTrust.TRUSTED, ctx)


def _facts(auth=None, ctx=None, **kw):
    ctx = ctx if ctx is not None else _ctx_t1()
    auth = auth if auth is not None else _auth(ctx)
    base = dict(
        subject_id="s1", resource_id="r1", action_id="a1",
        auth=auth, ownership=ResourceOwnership("r1", ctx),
        context=ctx, revocation_status=Z.RevocationStatus.ACTIVE,
        memberships=(), attributes=())
    base.update(kw)
    return Z.TrustedFacts(**base)


def _request(ctx=None, did="d1"):
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.Request(did, "s1", "r1", "a1", ctx, "c1")


class _Clock:
    def __init__(self, now):
        self._now = now

    def now(self):
        return self._now


class _Provider:
    def __init__(self, facts=None, exc=None):
        self._facts = facts
        self._exc = exc

    def resolve(self, request):
        if self._exc is not None:
            raise self._exc
        return self._facts


class _Audit:
    def __init__(self, ret=True):
        self.events = []
        self._ret = ret

    def record(self, event):
        self.events.append(event)
        return self._ret


def _topology():
    return TopologySnapshot(
        ("t1", "t2"),
        (ScopeNode("s1", "t1"), ScopeNode("s2", "t2")))


def _run(policies, facts=None, topo=None, now=None, audit_ret=True,
         request=None, catalog=None, limits=None, clock=None):
    limits = limits if limits is not None else _limits()
    catalog = catalog if catalog is not None else _catalog()
    snap = Z.Snapshot("e1", catalog, limits, tuple(policies))
    req = request if request is not None else _request()
    facts = facts if facts is not None else _facts()
    topo = topo if topo is not None else _topology()
    now = now if now is not None else T0
    audit = _Audit(audit_ret)
    dec = Z.authorize(req, snap, _Provider(facts), _Clock(now), audit, topo)
    return dec, snap, audit


class DecisionTest(unittest.TestCase):
    def test_baseline_allow_ids(self):
        dec, snap, audit = _run([_policy()])
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.reason_code, "ALLOWED")
        self.assertEqual(dec.decision_id, "d1")
        self.assertEqual(dec.policy_version, snap.version)
        self.assertEqual(audit.events, [])

    def test_default_deny_empty(self):
        dec, snap, audit = _run([])
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(dec.reason_code, "DENIED")
        self.assertEqual(len(audit.events), 1)

    def test_deny_overrides_allow_both_orders(self):
        deny = _policy("pd", Z.Effect.DENY)
        allow = _policy("pa", Z.Effect.ALLOW)
        for policies in ([allow, deny], [deny, allow]):
            dec, _, audit = _run(policies)
            self.assertIs(dec.effect, Z.Effect.DENY)
            self.assertEqual(len(audit.events), 1)

    def test_audit_obligation_dedup(self):
        p1 = _policy("p1", obligations=(Z.Obligation("AUDIT"),))
        p2 = _policy("p2", obligations=(Z.Obligation("AUDIT"),))
        dec, _, _ = _run([p1, p2])
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.obligations, ("AUDIT",))

    def test_facts_mismatch_each_deny(self):
        base_auth = _auth()
        ctx = _ctx_t1()
        cases = [
            dict(subject_id="s2"),
            dict(resource_id="r2"),
            dict(action_id="a2"),
            dict(auth=dataclasses.replace(base_auth, digital_identity_id="s2")),
            dict(ownership=ResourceOwnership("r2", ctx)),
            dict(context=ScopeContext(ScopeType.TENANT, "t2")),
            dict(auth=_auth(ScopeContext(ScopeType.TENANT, "t2"))),
        ]
        for kw in cases:
            with self.subTest(kw=tuple(sorted(kw.keys()))):
                dec, _, audit = _run([_policy()], facts=_facts(**kw))
                self.assertIs(dec.effect, Z.Effect.DENY)
                self.assertEqual(dec.reason_code, "DENIED")
                self.assertEqual(len(audit.events), 1)

    def test_revocation_statuses(self):
        for status, allow in (
                (Z.RevocationStatus.ACTIVE, True),
                (Z.RevocationStatus.REVOKED, False),
                (Z.RevocationStatus.UNKNOWN, False)):
            with self.subTest(status=status):
                dec, _, _ = _run(
                    [_policy()],
                    facts=_facts(revocation_status=status))
                self.assertIs(
                    dec.effect,
                    Z.Effect.ALLOW if allow else Z.Effect.DENY)

    def test_provider_exception_deny(self):
        snap = Z.build_snapshot("e1", (_policy(),), _catalog(), _limits())
        audit = _Audit(True)
        dec = Z.authorize(
            _request(), snap, _Provider(exc=RuntimeError("x")),
            _Clock(T0), audit, _topology())
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)

    def test_invalid_request_and_forged_snapshot_deny(self):
        forged_req = object.__new__(Z.Request)
        dec, snap, audit = _run([_policy()], request=forged_req)
        self.assertIs(dec.effect, Z.Effect.DENY)
        forged_snap = object.__new__(Z.Snapshot)
        audit2 = _Audit(True)
        dec2 = Z.authorize(
            _request(), forged_snap, _Provider(_facts()),
            _Clock(T0), audit2, _topology())
        self.assertIs(dec2.effect, Z.Effect.DENY)
        self.assertEqual(len(audit2.events), 1)

    def test_conditions_eq_in(self):
        pall = _policy(
            conditions=(Z.Condition("role", "eq", "admin"),))
        dec, _, _ = _run(
            [pall], facts=_facts(attributes=(("role", "admin"),)))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        dec2, _, _ = _run(
            [pall], facts=_facts(attributes=(("role", "user"),)))
        self.assertIs(dec2.effect, Z.Effect.DENY)
        pin = _policy(conditions=(Z.Condition("role", "in", ("a", "b")),))
        dec3, _, _ = _run(
            [pin], facts=_facts(attributes=(("role", "b"),)))
        self.assertIs(dec3.effect, Z.Effect.ALLOW)
        dec4, _, _ = _run(
            [pin], facts=_facts(attributes=(("role", "z"),)))
        self.assertIs(dec4.effect, Z.Effect.DENY)
        plvl = _policy(conditions=(Z.Condition("level", "eq", 3),))
        dec5, _, _ = _run(
            [plvl], facts=_facts(attributes=(("level", 3),)))
        self.assertIs(dec5.effect, Z.Effect.ALLOW)

    def test_bool_int_refused(self):
        forged = object.__new__(Z.TrustedFacts)
        object.__setattr__(forged, "subject_id", "s1")
        object.__setattr__(forged, "resource_id", "r1")
        object.__setattr__(forged, "action_id", "a1")
        object.__setattr__(forged, "auth", _auth())
        object.__setattr__(
            forged, "ownership", ResourceOwnership("r1", _ctx_t1()))
        object.__setattr__(forged, "context", _ctx_t1())
        object.__setattr__(
            forged, "revocation_status", Z.RevocationStatus.ACTIVE)
        object.__setattr__(forged, "memberships", ())
        object.__setattr__(forged, "attributes", (("level", True),))
        dec, _, _ = _run([_policy(
            conditions=(Z.Condition("level", "eq", 1),))], facts=forged)
        self.assertIs(dec.effect, Z.Effect.DENY)

    def test_deny_missing_condition_beats_allow(self):
        allow = _policy("pa")
        deny = _policy(
            "pz", Z.Effect.DENY,
            conditions=(Z.Condition("level", "eq", 99),
                        Z.Condition("role", "eq", "admin")))
        for attributes in ((), (("level", 3),)):
            with self.subTest(attributes=attributes):
                dec, _, audit = _run(
                    [allow, deny], facts=_facts(attributes=attributes))
                self.assertIs(dec.effect, Z.Effect.DENY)
                self.assertEqual(len(audit.events), 1)

    def test_assurances_thresholds(self):
        pol = _policy(
            min_identity_assurance=Z.IdentityAssurance.VERIFIED,
            min_authentication_assurance=(
                Z.AuthenticationAssurance.MULTI_FACTOR),
            min_federation_trust=Z.FederationTrust.TRUSTED)
        dec, _, _ = _run([pol])
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        low = _auth()
        low = dataclasses.replace(
            low, identity_assurance=Z.IdentityAssurance.CLAIMED)
        dec2, _, _ = _run([pol], facts=_facts(auth=low))
        self.assertIs(dec2.effect, Z.Effect.DENY)
        low2 = dataclasses.replace(
            _auth(),
            authentication_assurance=(
                Z.AuthenticationAssurance.SINGLE_FACTOR))
        dec3, _, _ = _run([pol], facts=_facts(auth=low2))
        self.assertIs(dec3.effect, Z.Effect.DENY)
        low3 = dataclasses.replace(
            _auth(), federation_trust=Z.FederationTrust.UNTRUSTED)
        dec4, _, _ = _run([pol], facts=_facts(auth=low3))
        self.assertIs(dec4.effect, Z.Effect.DENY)

    def test_forged_assurance_refused(self):
        forged_auth = object.__new__(Z.AuthenticationContext)
        good = _auth()
        for f in ("digital_identity_id", "provider_id", "issuer",
                  "external_subject", "authentication_time", "expires_at",
                  "methods", "identity_assurance",
                  "authentication_assurance", "federation_trust",
                  "context", "session_id", "credential_id"):
            object.__setattr__(
                forged_auth, f, object.__getattribute__(good, f))
        object.__setattr__(forged_auth, "identity_assurance", "VERIFIED")
        dec, _, _ = _run([_policy()], facts=_facts(auth=forged_auth))
        self.assertIs(dec.effect, Z.Effect.DENY)

    def test_bounds_refused(self):
        long_id = "x" * 65
        dec, _, _ = _run(
            [_policy()], request=_request(_ctx_t1(), long_id))
        self.assertIs(dec.effect, Z.Effect.DENY)
        big_attr = _facts(attributes=(("role", "y" * 129),))
        dec2, _, _ = _run([_policy()], facts=big_attr)
        self.assertIs(dec2.effect, Z.Effect.DENY)
        many = tuple("m%d" % i for i in range(33))
        dec3, _, _ = _run([_policy()], facts=_facts(memberships=many))
        self.assertIs(dec3.effect, Z.Effect.DENY)
        many_methods = tuple("m%d" % i for i in range(33))
        auth = dataclasses.replace(_auth(), methods=many_methods)
        dec4, _, _ = _run([_policy()], facts=_facts(auth=auth))
        self.assertIs(dec4.effect, Z.Effect.DENY)

    def test_unknown_scope_and_forged_topology(self):
        other = ScopeContext(ScopeType.TENANT, "t9")
        req = _request(other)
        dec, _, _ = _run([_policy()], request=req)
        self.assertIs(dec.effect, Z.Effect.DENY)
        forged_topo = object.__new__(TopologySnapshot)
        dec2, _, _ = _run([_policy()], topo=forged_topo)
        self.assertIs(dec2.effect, Z.Effect.DENY)

    def test_small_budget_deny(self):
        tiny = _limits(max_cost=1)
        dec, _, _ = _run([_policy()], limits=tiny)
        self.assertIs(dec.effect, Z.Effect.DENY)

    def test_evil_never_called(self):
        calls = []

        class Evil(str):
            def __repr__(self):
                calls.append("repr")
                raise AssertionError("repr called")

            def __str__(self):
                calls.append("str")
                raise AssertionError("str called")

            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("eq called")

            def __hash__(self):
                return 1

        evil = Evil("s1")
        dec, _, audit = _run([_policy()], request=_request(_ctx_t1(), "d1"))
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        forged_req = object.__new__(Z.Request)
        object.__setattr__(forged_req, "decision_id", evil)
        object.__setattr__(forged_req, "subject_id", "s1")
        object.__setattr__(forged_req, "resource_id", "r1")
        object.__setattr__(forged_req, "action_id", "a1")
        object.__setattr__(forged_req, "context", _ctx_t1())
        object.__setattr__(forged_req, "correlation_id", "c1")
        dec2, _, audit2 = _run([_policy()], request=forged_req)
        self.assertIs(dec2.effect, Z.Effect.DENY)
        self.assertEqual(len(audit2.events), 1)
        self.assertEqual(calls, [])

    def test_every_deny_single_audit_public_code(self):
        samples = [
            lambda: _run([]),
            lambda: _run([_policy()],
                         facts=_facts(revocation_status=(
                             Z.RevocationStatus.REVOKED))),
            lambda: _run([_policy()], limits=_limits(max_cost=1)),
        ]
        for fn in samples:
            dec, _, audit = fn()
            self.assertIs(dec.effect, Z.Effect.DENY)
            self.assertEqual(dec.reason_code, "DENIED")
            self.assertEqual(len(audit.events), 1)
            self.assertEqual(audit.events[0].reason_code, "DENIED")

    def test_unknown_operator_rejected_before_evaluation(self):
        with self.assertRaises(Z.PolicyError):
            Z.Condition("role", "contains", "admin")
        condition = object.__new__(Z.Condition)
        object.__setattr__(condition, "attr", "role")
        object.__setattr__(condition, "op", "contains")
        object.__setattr__(condition, "value", "admin")
        invalid = _policy("pz", Z.Effect.DENY, conditions=(condition,))
        decision, _, audit = _run(
            [_policy("pa"), invalid],
            facts=_facts(attributes=(("role", "admin"),)))
        self.assertIs(decision.effect, Z.Effect.DENY)
        self.assertIsNone(decision.policy_version)
        self.assertEqual(len(audit.events), 1)

    def test_request_without_auth_and_new_interface(self):
        self.assertTrue(hasattr(Z.Request, "__dataclass_fields__"))
        self.assertTrue(callable(Z.authorize))
        import inspect
        params = list(inspect.signature(Z.authorize).parameters)
        self.assertEqual(
            params,
            ["request", "snapshot", "provider", "clock", "audit",
             "topology"])
        self.assertTrue(hasattr(Z, "Decision"))
        self.assertNotIn("req_view_partial", dir(Z))


if __name__ == "__main__":
    unittest.main()
