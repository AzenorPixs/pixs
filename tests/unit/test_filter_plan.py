"""Tests unitaires filter_plan via facade publique, doubles memoire."""

import dataclasses
import datetime
import inspect
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


def _ctx_t2():
    return ScopeContext(ScopeType.TENANT, "t2")


def _catalog():
    plat = ScopeContext(ScopeType.PLATFORM)
    return Z.Catalog(
        ("s1", "s2"), ("r1", "r2", "r3"),
        ("a1", "a2"),
        (_ctx_t1(), _ctx_t2(), plat),
        (("role", "STR"), ("level", "INT")))


def _topology():
    return TopologySnapshot(("t1", "t2"), ())


def _policy(pid="p1", effect=None, resource=("r1",), scope_ctx=None, **kw):
    effect = effect if effect is not None else Z.Effect.ALLOW
    scope_ctx = scope_ctx if scope_ctx is not None else _ctx_t1()
    return Z.Policy(
        pid, "v1", "owner1", effect,
        Z.Selector("subject", ("s1",)),
        Z.Selector("resource", resource),
        Z.Selector("action", ("a1",)),
        Z.ScopeSelector((scope_ctx,)), **kw)


def _snapshot(policies, catalog=None, limits=None):
    catalog = catalog if catalog is not None else _catalog()
    limits = limits if limits is not None else _limits()
    return Z.build_snapshot("epoch1", tuple(policies), catalog, limits)


def _auth(t0=None, ctx=None):
    t0 = t0 if t0 is not None else T0
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.AuthenticationContext(
        "s1", "prov1", "iss1", "ext1",
        t0 - datetime.timedelta(seconds=10),
        t0 + datetime.timedelta(seconds=300),
        ("password",),
        Z.IdentityAssurance.VERIFIED,
        Z.AuthenticationAssurance.MULTI_FACTOR,
        Z.FederationTrust.TRUSTED,
        ctx)


def _facts(rid, auth=None, attributes=(), memberships=(),
           rev=None, ctx=None):
    auth = auth if auth is not None else _auth(ctx=ctx)
    ctx = ctx if ctx is not None else _ctx_t1()
    rev = rev if rev is not None else Z.RevocationStatus.ACTIVE
    return Z.TrustedFacts(
        subject_id="s1", resource_id=rid, action_id="a1",
        auth=auth, ownership=ResourceOwnership(rid, ctx),
        context=ctx, revocation_status=rev,
        memberships=memberships, attributes=attributes)


class _MapProvider:
    def __init__(self, mapping, fail_on=(), fail_exc=None):
        self._mapping = dict(mapping)
        self._fail_on = set(fail_on)
        self._fail_exc = fail_exc if fail_exc is not None else RuntimeError(
            "port backend en echec")
        self.calls = []

    def resolve(self, request):
        self.calls.append(request.resource_id)
        if request.resource_id in self._fail_on:
            raise self._fail_exc
        return self._mapping[request.resource_id]


class _FixedClock:
    def __init__(self, now=None):
        self._now = now if now is not None else T0
        self.calls = 0

    def now(self):
        self.calls += 1
        return self._now


class _NaiveClock:
    def now(self):
        return datetime.datetime(2026, 1, 2, 12, 0, 0)


class _ExcClock:
    def now(self):
        raise RuntimeError("horloge en echec")


class _OkAudit:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)
        return True


class _FailAudit:
    def record(self, event):
        return False


def _request(rid, did, ctx=None, corr="c1", sid="s1", aid="a1"):
    ctx = ctx if ctx is not None else _ctx_t1()
    return Z.Request(did, sid, rid, aid, ctx, corr)


def _lot(rids, corr="c1", ctx=None):
    ctx = ctx if ctx is not None else _ctx_t1()
    reqs = tuple(_request(rid, "d-%s" % rid, ctx, corr) for rid in rids)
    return Z.FilterLot("s1", "a1", ctx, corr, reqs)


class FilterPlanMatrixTest(unittest.TestCase):
    def test_authorize_signature_unchanged(self):
        sig = inspect.signature(Z.authorize)
        self.assertEqual(
            list(sig.parameters),
            ["request", "snapshot", "provider", "clock", "audit",
             "topology"])

    def test_decision_fields_unchanged(self):
        fields = list(Z.Decision.__dataclass_fields__)
        self.assertEqual(
            fields,
            ["decision_id", "effect", "reason_code", "policy_version",
             "obligations", "evaluated_at", "expires_at"])

    def test_frozen(self):
        lot = _lot(("r1",))
        with self.assertRaises(Exception):
            lot.subject_id = "sx"
        plan = Z.plan_filter(
            _lot(("r1",)), _snapshot([_policy()]),
            _MapProvider({"r1": _facts("r1")}), _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        with self.assertRaises(Exception):
            plan.resource_ids = ()
        self.assertIs(type(plan.resource_ids), tuple)
        self.assertIs(type(plan.obligations), tuple)

    def test_mix_allow_deny(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",)),
            _policy("p2", Z.Effect.DENY, ("r2",)),
        ])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        plan = Z.plan_filter(
            _lot(("r1", "r2")), snap, prov, _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ("r1",))
        self.assertEqual(plan.profile_version, "source-filter-plan-v1")

    def test_deny_seul_vide(self):
        snap = _snapshot([_policy("p1", Z.Effect.DENY, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        plan = Z.plan_filter(
            _lot(("r1", "r2")), snap, prov, _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ())
        self.assertEqual(plan.obligations, ())
        self.assertIsNone(plan.expires_at)

    def test_absence_politique_plan_vide(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        plan = Z.plan_filter(
            _lot(("r1", "r2")), snap, prov, _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ("r1",))

    def test_ressource_hors_catalogue(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        prov = _MapProvider({"r1": _facts("r1")})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "rx")), snap, prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(8))

    def test_tri(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        plan = Z.plan_filter(
            _lot(("r2", "r1")), snap, prov, _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ("r1", "r2"))

    def test_expires_minimum_distinct(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))],
                         limits=_limits(ttl_seconds=60))
        auth_r1 = _auth()
        auth_r2 = dataclasses.replace(
            _auth(), expires_at=T0 + datetime.timedelta(seconds=20))
        prov = _MapProvider({
            "r1": _facts("r1", auth=auth_r1),
            "r2": _facts("r2", auth=auth_r2),
        })
        for order in (("r1", "r2"), ("r2", "r1")):
            plan = Z.plan_filter(
                _lot(order), snap, _MapProvider({
                    "r1": _facts("r1", auth=auth_r1),
                    "r2": _facts("r2", auth=auth_r2)}),
                _FixedClock(), _OkAudit(), _topology(),
                Z.FilterConfig(8))
            self.assertEqual(
                plan.expires_at, T0 + datetime.timedelta(seconds=20))
        self.assertEqual(prov.calls, [])

    def test_union_audit(self):
        snap = _snapshot([_policy(
            "p1", Z.Effect.ALLOW, ("r1", "r2"),
            obligations=(Z.Obligation("AUDIT"),))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        plan = Z.plan_filter(
            _lot(("r1", "r2")), snap, prov, _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.obligations, ("AUDIT",))

    def test_snapshot_version_multiples(self):
        snap = _snapshot([
            _policy("p2", Z.Effect.ALLOW, ("r2",)),
            _policy("p1", Z.Effect.ALLOW, ("r1",)),
        ])
        prov = _MapProvider({"r1": _facts("r1")})
        plan = Z.plan_filter(
            _lot(("r1",)), snap, prov, _FixedClock(), _OkAudit(),
            _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.snapshot_version, snap.version)
        epoch, pairs = snap.version
        self.assertEqual(epoch, "epoch1")
        self.assertEqual(tuple(pairs), (("p1", "v1"), ("p2", "v1")))

    def test_hetero_internes_catalogue(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        ctx = _ctx_t1()
        cases = [
            Z.FilterLot("s1", "a1", ctx, "c1",
                        (_request("r1", "d-r1", ctx, "c1", sid="s1"),
                         _request("r2", "d-r2", ctx, "c1", sid="s2"))),
            Z.FilterLot("s1", "a1", ctx, "c1",
                        (_request("r1", "d-r1", ctx, "c1", aid="a1"),
                         _request("r2", "d-r2", ctx, "c1", aid="a2"))),
            Z.FilterLot("s1", "a1", ctx, "c1",
                        (_request("r1", "d-r1", ctx, "c1"),
                         _request("r2", "d-r2", _ctx_t2(), "c1"))),
            Z.FilterLot("s1", "a1", ctx, "c1",
                        (_request("r1", "d-r1", ctx, "c1"),
                         _request("r2", "d-r2", ctx, "c2"))),
        ]
        for lot in cases:
            with self.assertRaises(Z.FilterPlanError):
                Z.plan_filter(lot, snap, prov, _FixedClock(),
                              _OkAudit(), _topology(), Z.FilterConfig(8))

    def test_limite(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(1))

    def test_filter_config_constructeur(self):
        for bad in (True, 3.5, "8", 0, -1):
            with self.assertRaises(Z.FilterPlanError):
                Z.FilterConfig(bad)

    def test_condition_absente_apres_allow(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",)),
            Z.Policy(
                "p2", "v1", "owner1", Z.Effect.ALLOW,
                Z.Selector("subject", ("s1",)),
                Z.Selector("resource", ("r2",)),
                Z.Selector("action", ("a1",)),
                Z.ScopeSelector((_ctx_t1(),)),
                conditions=(Z.Condition("level", "eq", 1),)),
        ])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(8))

    def test_bool_prioritaire_revoked(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        bad = _facts("r1", attributes=(("level", True),),
                     rev=Z.RevocationStatus.REVOKED)
        prov = _MapProvider({"r1": bad})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1",)), snap, prov, _FixedClock(),
                          _OkAudit(), _topology(), Z.FilterConfig(8))

    def test_revoked_connu_exclut(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({
            "r1": _facts("r1"),
            "r2": _facts("r2", rev=Z.RevocationStatus.REVOKED),
        })
        plan = Z.plan_filter(
            _lot(("r1", "r2")), snap, prov, _FixedClock(),
            _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ("r1",))

    def test_unknown_revocation_error(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        prov = _MapProvider({
            "r1": _facts("r1", rev=Z.RevocationStatus.UNKNOWN),
        })
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1",)), snap, prov, _FixedClock(),
                          _OkAudit(), _topology(), Z.FilterConfig(8))

    def test_provider_policy_deny_injecte(self):
        from pixs.core.authz import decision as D
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1")},
                            fail_on=("r2",), fail_exc=D._PolicyDeny())
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(8))

    def test_audit_fail_apres_allow(self):
        snap = _snapshot([
            _policy("p1", Z.Effect.ALLOW, ("r1",)),
            _policy("p2", Z.Effect.DENY, ("r2",)),
        ])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), _FailAudit(), _topology(),
                          Z.FilterConfig(8))

    def test_cout_overflow_apres_allow(self):
        limits = _limits(max_cost=9500)
        snap = _snapshot(
            [_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))], limits=limits)
        single = Z.plan_filter(
            _lot(("r1",)), snap, _MapProvider({"r1": _facts("r1")}),
            _FixedClock(), _OkAudit(), _topology(), Z.FilterConfig(8))
        self.assertEqual(single.resource_ids, ("r1",))
        heavy = _facts(
            "r2", memberships=tuple("m%02dxxxxxxxxxxxxxxxxxxxxxxxx" % i
                                    for i in range(32)))
        prov = _MapProvider({"r1": _facts("r1"), "r2": heavy})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(8))
        self.assertEqual(prov.calls, ["r1", "r2"])

    def test_vide_admis(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        lot = Z.FilterLot("s1", "a1", _ctx_t1(), "c1", ())
        plan = Z.plan_filter(lot, snap, _MapProvider({}),
                             _FixedClock(), _OkAudit(), _topology(),
                             Z.FilterConfig(8))
        self.assertEqual(plan.resource_ids, ())
        self.assertIsNone(plan.expires_at)

    def test_vide_catalogue_unknown(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        for lot in (
            Z.FilterLot("sx", "a1", _ctx_t1(), "c1", ()),
            Z.FilterLot("s1", "ax", _ctx_t1(), "c1", ()),
            Z.FilterLot("s1", "a1", ScopeContext(ScopeType.TENANT, "tx"),
                        "c1", ()),
        ):
            with self.assertRaises(Z.FilterPlanError):
                Z.plan_filter(lot, snap, _MapProvider({}),
                              _FixedClock(), _OkAudit(), _topology(),
                              Z.FilterConfig(8))

    def test_vide_topologie_malformee(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        lot = Z.FilterLot("s1", "a1", _ctx_t1(), "c1", ())
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(lot, snap, _MapProvider({}), _FixedClock(),
                          _OkAudit(), "bad-topology", Z.FilterConfig(8))

    def test_snapshot_invalide(self):
        prov = _MapProvider({"r1": _facts("r1")})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1",)), "bad-snapshot", prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(8))

    def test_header_long(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        long_id = "x" * 65
        lot = Z.FilterLot(long_id, "a1", _ctx_t1(), "c1", ())
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(lot, snap, _MapProvider({}), _FixedClock(),
                          _OkAudit(), _topology(), Z.FilterConfig(8))

    def test_request_types_stricts(self):
        with self.assertRaises(Exception):
            Z.Request("d1", 123, "r1", "a1", _ctx_t1(), "c1")
        with self.assertRaises(Exception):
            Z.Request("d1", "s1", "r1", "a1", "bad-ctx", "c1")

    def test_clock_invalide(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        prov = _MapProvider({"r1": _facts("r1")})
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1",)), snap, prov, _NaiveClock(),
                          _OkAudit(), _topology(), Z.FilterConfig(8))
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1",)), snap, prov, _ExcClock(),
                          _OkAudit(), _topology(), Z.FilterConfig(8))

    def test_clock_unique(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        clock = _FixedClock()
        plan = Z.plan_filter(
            _lot(("r1", "r2")), snap, prov, clock, _OkAudit(),
            _topology(), Z.FilterConfig(8))
        self.assertEqual(clock.calls, 1)
        self.assertEqual(plan.evaluated_at, T0)

    def test_config_invalide(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        prov = _MapProvider({"r1": _facts("r1")})
        for bad in ("8", 0, -1, True, None):
            with self.assertRaises(Z.FilterPlanError):
                Z.plan_filter(_lot(("r1",)), snap, prov,
                              _FixedClock(), _OkAudit(), _topology(), bad)

    def test_ids_decisions_dupliques(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1"), "r2": _facts("r2")})
        ctx = _ctx_t1()
        reqs = (_request("r1", "d-same", ctx, "c1"),
                _request("r2", "d-same", ctx, "c1"))
        lot = Z.FilterLot("s1", "a1", ctx, "c1", reqs)
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(lot, snap, prov, _FixedClock(), _OkAudit(),
                          _topology(), Z.FilterConfig(8))

    def test_ids_ressources_dupliquees(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1",))])
        prov = _MapProvider({"r1": _facts("r1")})
        ctx = _ctx_t1()
        reqs = (_request("r1", "d-1", ctx, "c1"),
                _request("r1", "d-2", ctx, "c1"))
        lot = Z.FilterLot("s1", "a1", ctx, "c1", reqs)
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(lot, snap, prov, _FixedClock(), _OkAudit(),
                          _topology(), Z.FilterConfig(8))

    def test_rollback_apres_fail(self):
        snap = _snapshot([_policy("p1", Z.Effect.ALLOW, ("r1", "r2"))])
        prov = _MapProvider({"r1": _facts("r1")}, fail_on=("r2",))
        with self.assertRaises(Z.FilterPlanError):
            Z.plan_filter(_lot(("r1", "r2")), snap, prov,
                          _FixedClock(), _OkAudit(), _topology(),
                          Z.FilterConfig(8))
        self.assertEqual(prov.calls, ["r1", "r2"])


if __name__ == "__main__":
    unittest.main()
