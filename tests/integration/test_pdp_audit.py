"""Integration PDP audit en memoire, sans persistance."""

import datetime
import unittest

from pixs.core import authz as Z
from pixs.core.scope import ScopeContext, ScopeType
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.scope.topology import TopologySnapshot


def _t0():
    return datetime.datetime(2026, 1, 2, 12, 0, 0, tzinfo=datetime.timezone.utc)


def _limits():
    return Z.Limits(
        max_policies=32, max_selector_values=32,
        max_conditions_per_policy=16, max_set_values=32,
        max_attributes=16, max_memberships=32,
        max_id_length=64, max_value_length=128,
        max_cost=1000000, ttl_seconds=60, max_freshness_seconds=600)


def _ctx(kind, tenant=None):
    if kind == "t1":
        return ScopeContext(ScopeType.TENANT, "t1")
    if kind == "t2":
        return ScopeContext(ScopeType.TENANT, "t2")
    return ScopeContext(ScopeType.PLATFORM)


def _catalog():
    return Z.Catalog(
        ("s1",), ("r1",), ("a1",),
        (_ctx("t1"), _ctx("t2"), _ctx("plat")),
        (("role", "STR"),))


def _policy(effect=None, ctx=None, obligations=(), pid="p1"):
    effect = effect if effect is not None else Z.Effect.ALLOW
    ctx = ctx if ctx is not None else _ctx("t1")
    return Z.Policy(
        pid, "v1", "owner1", effect,
        Z.Selector("subject", ("s1",)),
        Z.Selector("resource", ("r1",)),
        Z.Selector("action", ("a1",)),
        Z.ScopeSelector((ctx,)), obligations=obligations)


def _auth(ctx=None, t0=None):
    t0 = t0 if t0 is not None else _t0()
    ctx = ctx if ctx is not None else _ctx("t1")
    return Z.AuthenticationContext(
        "s1", "prov1", "iss1", "ext1",
        t0 - datetime.timedelta(seconds=10),
        t0 + datetime.timedelta(seconds=300),
        ("password",),
        Z.IdentityAssurance.VERIFIED,
        Z.AuthenticationAssurance.MULTI_FACTOR,
        Z.FederationTrust.TRUSTED, ctx)


def _facts(ctx=None, auth=None, **kw):
    ctx = ctx if ctx is not None else _ctx("t1")
    auth = auth if auth is not None else _auth(ctx)
    base = dict(
        subject_id="s1", resource_id="r1", action_id="a1",
        auth=auth, ownership=ResourceOwnership("r1", ctx),
        context=ctx, revocation_status=Z.RevocationStatus.ACTIVE,
        memberships=(), attributes=())
    base.update(kw)
    return Z.TrustedFacts(**base)


def _request(ctx=None):
    ctx = ctx if ctx is not None else _ctx("t1")
    return Z.Request("d1", "s1", "r1", "a1", ctx, "c1")


def _topo():
    return TopologySnapshot(("t1", "t2"), ())


class _Clock:
    def __init__(self, now):
        self._now = now

    def now(self):
        return self._now


class _Provider:
    def __init__(self, facts=None, exc=None):
        self.calls = 0
        self._facts = facts
        self._exc = exc

    def resolve(self, request):
        self.calls += 1
        if self._exc is not None:
            raise self._exc
        if callable(self._facts):
            return self._facts()
        return self._facts


class _Audit:
    def __init__(self, behavior=True):
        self.events = []
        self.calls = 0
        self._behavior = behavior

    def record(self, event):
        self.calls += 1
        self.events.append(event)
        if callable(self._behavior):
            return self._behavior(event)
        if isinstance(self._behavior, Exception):
            raise self._behavior
        return self._behavior


def _snap(policies):
    return Z.build_snapshot("e1", tuple(policies), _catalog(), _limits())


class AuditTest(unittest.TestCase):
    def test_default_deny_audited_fields(self):
        snap = _snap([])
        audit = _Audit(True)
        dec = Z.authorize(
            _request(), snap, _Provider(_facts()), _Clock(_t0()),
            audit, _topo())
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)
        ev = audit.events[0]
        self.assertEqual(ev.decision_id, "d1")
        self.assertEqual(ev.subject_id, "s1")
        self.assertEqual(ev.resource_id, "r1")
        self.assertEqual(ev.action_id, "a1")
        self.assertEqual(ev.correlation_id, "c1")
        self.assertIsNotNone(ev.context)
        self.assertIs(ev.effect, Z.Effect.DENY)
        self.assertEqual(ev.reason_code, "DENIED")
        self.assertEqual(ev.policy_version, snap.version)
        self.assertEqual(ev.evaluated_at, _t0())

    def test_provider_clock_snapshot_failures(self):
        snap = _snap([_policy()])
        audit = _Audit(True)
        dec = Z.authorize(
            _request(), snap, _Provider(exc=RuntimeError("x")),
            _Clock(_t0()), audit, _topo())
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)

        class Boom:
            def now(self):
                raise RuntimeError("clock")

        audit2 = _Audit(True)
        dec2 = Z.authorize(
            _request(), snap, _Provider(_facts()), Boom(),
            audit2, _topo())
        self.assertIs(dec2.effect, Z.Effect.DENY)
        self.assertIsNone(dec2.evaluated_at)
        self.assertEqual(len(audit2.events), 1)
        forged = object.__new__(Z.Snapshot)
        audit3 = _Audit(True)
        dec3 = Z.authorize(
            _request(), forged, _Provider(_facts()), _Clock(_t0()),
            audit3, _topo())
        self.assertIs(dec3.effect, Z.Effect.DENY)
        self.assertEqual(len(audit3.events), 1)

    def test_audit_sink_not_acknowledged(self):
        snap = _snap([])
        for behavior in (False, None, 1, RuntimeError("sink")):
            with self.subTest(behavior=repr(behavior)):
                audit = _Audit(behavior)
                dec = Z.authorize(
                    _request(), snap, _Provider(_facts()),
                    _Clock(_t0()), audit, _topo())
                self.assertIs(dec.effect, Z.Effect.DENY)
                self.assertEqual(audit.calls, 1)

    def test_platform_without_policy_deny(self):
        snap = _snap([])
        audit = _Audit(True)
        dec = Z.authorize(
            _request(_ctx("plat")), snap, _Provider(_facts(_ctx("plat"))),
            _Clock(_t0()), audit, _topo())
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)

    def test_platform_allow_without_audit_deny(self):
        pol = _policy(ctx=_ctx("plat"))
        snap = _snap([pol])
        audit = _Audit(True)
        dec = Z.authorize(
            _request(_ctx("plat")), snap,
            _Provider(_facts(_ctx("plat"), _auth(_ctx("plat")))),
            _Clock(_t0()), audit, _topo())
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)

    def test_platform_allow_audit_ack(self):
        pol = _policy(
            ctx=_ctx("plat"), obligations=(Z.Obligation("AUDIT"),))
        snap = _snap([pol])
        audit = _Audit(True)
        dec = Z.authorize(
            _request(_ctx("plat")), snap,
            _Provider(_facts(_ctx("plat"), _auth(_ctx("plat")))),
            _Clock(_t0()), audit, _topo())
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.obligations, ("AUDIT",))
        self.assertEqual(len(audit.events), 1)
        self.assertIs(audit.events[0].effect, Z.Effect.ALLOW)

    def test_platform_audit_not_ack_deny(self):
        pol = _policy(
            ctx=_ctx("plat"), obligations=(Z.Obligation("AUDIT"),))
        snap = _snap([pol])
        for behavior in (False, RuntimeError("x")):
            audit = _Audit(behavior)
            dec = Z.authorize(
                _request(_ctx("plat")), snap,
                _Provider(_facts(_ctx("plat"), _auth(_ctx("plat")))),
                _Clock(_t0()), audit, _topo())
            self.assertIs(dec.effect, Z.Effect.DENY)
            self.assertEqual(audit.calls, 1)

    def test_cross_tenant_ownership_deny(self):
        snap = _snap([_policy()])
        facts = _facts(
            ctx=_ctx("t1"),
            ownership=ResourceOwnership("r1", _ctx("t2")))
        audit = _Audit(True)
        dec = Z.authorize(
            _request(), snap, _Provider(facts), _Clock(_t0()),
            audit, _topo())
        self.assertIs(dec.effect, Z.Effect.DENY)
        self.assertEqual(len(audit.events), 1)
        facts2 = _facts(
            ctx=_ctx("t2"), auth=_auth(_ctx("t2")))
        audit2 = _Audit(True)
        dec2 = Z.authorize(
            _request(), snap, _Provider(facts2), _Clock(_t0()),
            audit2, _topo())
        self.assertIs(dec2.effect, Z.Effect.DENY)
        self.assertEqual(len(audit2.events), 1)

    def test_tenant_allow_returns_obligation_no_pep(self):
        pol = _policy(obligations=(Z.Obligation("AUDIT"),))
        snap = _snap([pol])
        audit = _Audit(True)
        touched = []
        provider = _Provider(_facts())

        original = provider.resolve

        def counting(request):
            touched.append(request)
            return original(request)

        provider.resolve = counting
        dec = Z.authorize(
            _request(), snap, provider, _Clock(_t0()), audit, _topo())
        self.assertIs(dec.effect, Z.Effect.ALLOW)
        self.assertEqual(dec.obligations, ("AUDIT",))
        self.assertEqual(len(touched), 1)
        self.assertEqual(audit.calls, 0)

    def test_allow_then_revoked_no_cache(self):
        snap = _snap([_policy()])
        state = {"revoked": False}

        def current():
            if state["revoked"]:
                return _facts(
                    revocation_status=Z.RevocationStatus.REVOKED)
            return _facts()

        provider = _Provider(current)
        audit = _Audit(True)
        dec1 = Z.authorize(
            _request(), snap, provider, _Clock(_t0()), audit, _topo())
        self.assertIs(dec1.effect, Z.Effect.ALLOW)
        state["revoked"] = True
        audit2 = _Audit(True)
        dec2 = Z.authorize(
            _request(), snap, provider, _Clock(_t0()), audit2, _topo())
        self.assertIs(dec2.effect, Z.Effect.DENY)
        self.assertEqual(len(audit2.events), 1)
        self.assertEqual(provider.calls, 2)


if __name__ == "__main__":
    unittest.main()
