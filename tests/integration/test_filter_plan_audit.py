"""Integration filter_plan audit memoire, sans persistance."""

import datetime
import unittest

from pixs.core import authz as Z
from pixs.core.scope import ScopeContext, ScopeType
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.scope.topology import TopologySnapshot


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


def _plat():
    return ScopeContext(ScopeType.PLATFORM)


def _catalog():
    return Z.Catalog(
        ("s1",), ("r1", "r2"),
        ("a1",),
        (_ctx_t1(), _plat()),
        (("role", "STR"),))


def _topology():
    return TopologySnapshot(("t1",), ())


def _policy(pid="p1", effect=None, resource=("r1",), ctx=None, **kw):
    effect = effect if effect is not None else Z.Effect.ALLOW
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.Policy(
        pid, "v1", "owner1", effect,
        Z.Selector("subject", ("s1",)),
        Z.Selector("resource", resource),
        Z.Selector("action", ("a1",)),
        Z.ScopeSelector((ctx,)), **kw)


def _snapshot(policies):
    return Z.build_snapshot("epoch1", tuple(policies), _catalog(),
                            _limits())


def _auth(ctx=None):
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.AuthenticationContext(
        "s1", "prov1", "iss1", "ext1",
        T0 - datetime.timedelta(seconds=10),
        T0 + datetime.timedelta(seconds=300),
        ("password",),
        Z.IdentityAssurance.VERIFIED,
        Z.AuthenticationAssurance.MULTI_FACTOR,
        Z.FederationTrust.TRUSTED,
        ctx)


def _facts(rid, ctx=None, rev=None):
    ctx = ctx if ctx is not None else _ctx_t1()
    rev = rev if rev is not None else Z.RevocationStatus.ACTIVE
    return Z.TrustedFacts(
        subject_id="s1", resource_id=rid, action_id="a1",
        auth=_auth(ctx), ownership=ResourceOwnership(rid, ctx),
        context=ctx, revocation_status=rev,
        memberships=(), attributes=())


class _MapProvider:
    def __init__(self, mapping, fail_on=(), fail_exc=None):
        self._mapping = dict(mapping)
        self._fail_on = set(fail_on)
        self._fail_exc = fail_exc if fail_exc is not None else RuntimeError(
            "audit port echoue")
        self.calls = []

    def resolve(self, request):
        self.calls.append(request.resource_id)
        if request.resource_id in self._fail_on:
            raise self._fail_exc
        return self._mapping[request.resource_id]


class _FixedClock:
    def __init__(self):
        self.calls = 0

    def now(self):
        self.calls += 1
        return T0


class _OkAudit:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)
        return True


class _FailAudit:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)
        return False


class _ExcAudit:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)
        raise RuntimeError("audit durable indisponible")


def _request(rid, did, ctx=None):
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.Request(did, "s1", rid, "a1", ctx, "c1")


def _lot(rids, ctx=None):
    ctx = ctx if ctx is not None else _ctx_t1()
    reqs = tuple(_request(rid, "d-%s" % rid, ctx) for rid in rids)
    return Z.FilterLot("s1", "a1", ctx, "c1", reqs)


class FilterPlanAuditTest(unittest.TestCase):
    def test_audit_false_apres_allow(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",)),
            _policy("p2", Z.Effect.DENY, ("r2",)),
        ])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        audit = _FailAudit()
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), audit, _topology(),
                          Z.FilterConfig(8))
        self.assertEqual(prov.calls, ["r1", "r2"])
        self.assertTrue(len(audit.events) >= 1)

    def test_audit_exception_apres_allow(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",)),
            _policy("p2", Z.Effect.DENY, ("r2",)),
        ])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        audit = _ExcAudit()
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), audit, _topology(),
                          Z.FilterConfig(8))
        self.assertEqual(prov.calls, ["r1", "r2"])
        self.assertTrue(len(audit.events) >= 1)

    def test_plateforme_audit_declare(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",), ctx=_plat(),
                    obligations=(Z.Obligation("AUDIT"),)),
        ])
        req = Z.Request("d-r1", "s1", "r1", "a1", _plat(), "c1")
        lot = Z.FilterLot("s1", "a1", _plat(), "c1", (req,))
        audit = _OkAudit()
        prov = _MapProvider({"r1": _facts("r1", ctx=_plat())})
        plan = Z.plan_filter(lot, snap, prov, _FixedClock(), audit,
                             _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ("r1",))
        self.assertEqual(plan.obligations, ("AUDIT",))
        self.assertTrue(len(audit.events) >= 1)

    def test_plateforme_sans_audit_vide(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",), ctx=_plat()),
        ])
        req = Z.Request("d-r1", "s1", "r1", "a1", _plat(), "c1")
        lot = Z.FilterLot("s1", "a1", _plat(), "c1", (req,))
        audit = _OkAudit()
        prov = _MapProvider({"r1": _facts("r1", ctx=_plat())})
        plan = Z.plan_filter(lot, snap, prov, _FixedClock(), audit,
                             _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ())
        self.assertEqual(plan.obligations, ())

    def test_plateforme_audit_fail(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",), ctx=_plat(),
                    obligations=(Z.Obligation("AUDIT"),)),
        ])
        req = Z.Request("d-r1", "s1", "r1", "a1", _plat(), "c1")
        lot = Z.FilterLot("s1", "a1", _plat(), "c1", (req,))
        for audit in (_FailAudit(), _ExcAudit()):
            prov = _MapProvider({"r1": _facts("r1", ctx=_plat())})
            with self.assertRaises(Z.FilterPlanError):
                Z.plan_filter(lot, snap, prov, _FixedClock(), audit,
                              _topology(), Z.FilterConfig(8))
            self.assertTrue(len(audit.events) >= 1)

    def test_cross_tenant_facts_incoherents(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        bad = _facts("r1", ctx=ScopeContext(ScopeType.TENANT, "t2"))
        prov = _MapProvider({"r1": bad})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1",)), snap, prov, _FixedClock(),
                          _OkAudit(), _topology(), Z.FilterConfig(8))

    def test_clock_once(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        clock = _FixedClock()
        Z.plan_filter(_lot(("r1", "r2")), snap, prov, clock,
                      _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(clock.calls, 1)

    def test_non_mutation(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        topo = _topology()
        lot = _lot(("r1", "r2"))
        before = (
            lot.subject_id, lot.action_id, lot.correlation_id,
            tuple((r.decision_id, r.subject_id, r.resource_id,
                   r.action_id, r.correlation_id) for r in lot.requests),
            lot.context, snap.epoch if hasattr(snap, "epoch") else None,
            snap.version, topo.tenants, topo.scopes,
        )
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        Z.plan_filter(lot, snap, prov, _FixedClock(), _OkAudit(), topo,
                      Z.FilterConfig(8))
        after = (
            lot.subject_id, lot.action_id, lot.correlation_id,
            tuple((r.decision_id, r.subject_id, r.resource_id,
                   r.action_id, r.correlation_id) for r in lot.requests),
            lot.context, snap.epoch if hasattr(snap, "epoch") else None,
            snap.version, topo.tenants, topo.scopes,
        )
        self.assertEqual(before, after)

    def test_canon_freeze(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1", "r2")),
        ])
        initial_version = snap.version
        base = {"r1": _facts("r1"), "r2": _facts("r2")}

        class _MutatingProvider:
            def __init__(self):
                self.calls = []

            def resolve(self, request):
                self.calls.append(request.resource_id)
                if request.resource_id == "r1":
                    object.__setattr__(snap, "epoch", "changed")
                    object.__setattr__(
                        snap, "policies",
                        (_policy("px", Z.Effect.DENY, ("r2",)),))
                return base[request.resource_id]

        prov = _MutatingProvider()
        plan = Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                             _FixedClock(), _OkAudit(), _topology(),
                             Z.FilterConfig(8))
        self.assertEqual(object.__getattribute__(snap, "epoch"), "changed")
        self.assertEqual(prov.calls, ["r1", "r2"])
        self.assertEqual(plan.resource_ids, ("r1", "r2"))
        self.assertEqual(plan.snapshot_version, initial_version)


if __name__ == "__main__":
    unittest.main()
