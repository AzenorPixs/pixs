"""Tests unitaires wiring exemple P0, doubles memoire."""

import datetime
import unittest
from pathlib import Path
from unittest import mock

from pixs.core import authz as Z
from pixs.core.scope import ScopeContext, ScopeType
from pixs.core.scope import validate_context as scope_validate_context
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.scope.topology import TopologySnapshot
from pixs.example import demo as Demo
from tests.conformity_fixtures import synthetic_attestations


def _utc(y, mo, d, h=0, mi=0, s=0):
    return datetime.datetime(y, mo, d, h, mi, s, tzinfo=datetime.timezone.utc)


T0 = _utc(2026, 1, 2, 12, 0, 0)
TOML_PATH = Path("src/pixs/example/component.toml")


def _provider_text():
    return TOML_PATH.read_text(encoding="utf-8")


def _limits():
    return Z.Limits(
        max_policies=32, max_selector_values=32,
        max_conditions_per_policy=16, max_set_values=32,
        max_attributes=16, max_memberships=32,
        max_id_length=64, max_value_length=128,
        max_cost=1000000, ttl_seconds=60, max_freshness_seconds=600)


def _ctx_t1():
    return ScopeContext(ScopeType.TENANT, "t1")


def _catalog():
    t1 = ScopeContext(ScopeType.TENANT, "t1")
    t2 = ScopeContext(ScopeType.TENANT, "t2")
    return Z.Catalog(
        ("s1",), ("r1", "r2"), ("a1",),
        (t1, t2), (("role", "STR"),))


def _topology_t1t2():
    return TopologySnapshot(("t1", "t2"), ())


def _policy(pid, effect, resources, ctx):
    return Z.Policy(
        pid, "v1", "owner1", effect,
        Z.Selector("subject", ("s1",)),
        Z.Selector("resource", resources),
        Z.Selector("action", ("a1",)),
        Z.ScopeSelector((ctx,)))


def _ctx(tenant):
    return ScopeContext(ScopeType.TENANT, tenant)


def _auth(ctx):
    return Z.AuthenticationContext(
        "s1", "prov1", "iss1", "ext1",
        T0 - datetime.timedelta(seconds=10),
        T0 + datetime.timedelta(seconds=300),
        ("password",),
        Z.IdentityAssurance.VERIFIED,
        Z.AuthenticationAssurance.MULTI_FACTOR,
        Z.FederationTrust.TRUSTED,
        ctx)


def _facts(rid, ctx):
    return Z.TrustedFacts(
        subject_id="s1", resource_id=rid, action_id="a1",
        auth=_auth(ctx), ownership=ResourceOwnership(rid, ctx),
        context=ctx, revocation_status=Z.RevocationStatus.ACTIVE,
        memberships=(), attributes=())


class _MapProvider:
    def __init__(self, mapping):
        self._mapping = dict(mapping)
        self.calls = []

    def resolve(self, request):
        self.calls.append(request)
        return self._mapping[request.resource_id]


class _Clock:
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
    def record(self, event):
        return False


def _request(rid, did, ctx, corr="c1", sid="s1", aid="a1"):
    return Z.Request(did, sid, rid, aid, ctx, corr)


def _lot(rids, ctx, corr="c1"):
    reqs = tuple(_request(rid, "d-%s" % rid, ctx, corr) for rid in rids)
    return Z.FilterLot("s1", "a1", ctx, corr, reqs)


def _snapshot_for(ctx):
    return Z.build_snapshot(
        "epoch1",
        (_policy("p1", Z.Effect.ALLOW, ("r1", "r2"), ctx),),
        _catalog(), _limits())


class ExampleWiringTest(unittest.TestCase):
    def test_provider_toml_reel(self):
        text = _provider_text()
        provider, consumer = Demo.example_texts(text)
        self.assertEqual(provider, text)
        self.assertIn('id = "example.client"', consumer)
        self.assertIn("example.hello.contract ==1.0.0", consumer)

    def test_scope_fixture_publique(self):
        from pixs.core import scope as scope_facade
        self.assertIn("ScopeContext", scope_facade.__all__)
        self.assertIn("ScopeType", scope_facade.__all__)
        self.assertIn("TopologySnapshot", scope_facade.__all__)
        self.assertIn("validate_context", scope_facade.__all__)
        context, topology = Demo.example_scope()
        scope_validate_context(context, topology)

    def test_import_sans_lecture(self):
        import importlib
        with mock.patch.object(Path, "read_text",
                               side_effect=AssertionError("lecture FS")):
            importlib.reload(Demo)
        self.assertTrue(hasattr(Demo, "example_texts"))

    def test_compose_sans_attestation_refuse(self):
        provider, consumer = Demo.example_texts(_provider_text())
        result = Demo.example_compose([provider, consumer])
        self.assertFalse(result.activated)

    def test_compose_synthetiques_doubles(self):
        provider, consumer = Demo.example_texts(_provider_text())
        texts = (provider, consumer)
        atts = synthetic_attestations(texts)
        first = Demo.example_compose(texts, atts)
        second = Demo.example_compose((consumer, provider), atts)
        self.assertTrue(first.activated)
        self.assertTrue(second.activated)
        self.assertEqual(first.order, second.order)

    def test_contrat_version_non_proxy(self):
        base = _provider_text()
        provider_v2 = base.replace(
            'id = "example.hello"\ntype = "MODULE"\nversion = "1.0.0"',
            'id = "example.hello"\ntype = "MODULE"\nversion = "2.0.0"',
            1)
        _, consumer = Demo.example_texts(base)
        texts = (provider_v2, consumer)
        ok_result = Demo.example_compose(
            texts, synthetic_attestations(texts))
        self.assertTrue(ok_result.activated)
        provider_bad = base.replace(
            'id = "example.hello.contract"\nversion = "1.0.0"',
            'id = "example.hello.contract"\nversion = "2.0.0"')
        _, consumer_same = Demo.example_texts(base)
        bad_texts = (provider_bad, consumer_same)
        bad_result = Demo.example_compose(
            bad_texts, synthetic_attestations(bad_texts))
        self.assertFalse(bad_result.activated)

    def test_plan_t1(self):
        ctx = _ctx("t1")
        snap = _snapshot_for(ctx)
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", ctx)})
        plan = Demo.example_plan(snap, prov, _Clock(), _OkAudit(),
                                 _topology_t1t2(), Z.FilterConfig(8), ctx)
        self.assertEqual(plan.resource_ids, ("r1", "r2"))

    def test_plan_t2_propagation(self):
        ctx = _ctx("t2")
        snap = _snapshot_for(ctx)
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", ctx)})
        plan = Demo.example_plan(snap, prov, _Clock(), _OkAudit(),
                                 _topology_t1t2(), Z.FilterConfig(8), ctx)
        self.assertEqual(plan.resource_ids, ("r1", "r2"))
        for request in prov.calls:
            self.assertEqual(request.context, ctx)

    def test_deny_prioritaire_ordre_permute(self):
        ctx = _ctx("t1")
        for policies in (
            (_policy("a", Z.Effect.ALLOW, ("r1", "r2"), ctx),
             _policy("d", Z.Effect.DENY, ("r1",), ctx)),
            (_policy("d", Z.Effect.DENY, ("r1",), ctx),
             _policy("a", Z.Effect.ALLOW, ("r1", "r2"), ctx)),
        ):
            snap = Z.build_snapshot("epoch1", policies, _catalog(),
                                    _limits())
            prov = _MapProvider({"r1": _facts("r1", ctx),
                                 "r2": _facts("r2", ctx)})
            plan = Demo.example_plan(snap, prov, _Clock(), _OkAudit(),
                                     _topology_t1t2(),
                                     Z.FilterConfig(8), ctx)
            self.assertEqual(plan.resource_ids, ("r2",))

    def test_audit_refusant(self):
        ctx = _ctx("t1")
        snap = Z.build_snapshot(
            "epoch1",
            (_policy("a", Z.Effect.ALLOW, ("r1",), ctx),
             _policy("d", Z.Effect.DENY, ("r2",), ctx)),
            _catalog(), _limits())

        class _CapturingFailAudit:
            def __init__(self):
                self.events = []
                self.calls = 0

            def record(self, event):
                self.events.append(event)
                self.calls += 1
                return False

        audit = _CapturingFailAudit()
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", ctx)})
        with self.assertRaises(Z.FilterPlanError):
            Demo.example_plan(snap, prov, _Clock(), audit,
                              _topology_t1t2(), Z.FilterConfig(8), ctx)
        self.assertEqual([r.resource_id for r in prov.calls],
                         ["r1", "r2"])
        self.assertEqual(audit.calls, 1)
        self.assertEqual(len(audit.events), 1)
        self.assertEqual(audit.events[0].resource_id, "r2")

    def test_cross_tenant_facts_refuse(self):
        ctx = _ctx("t2")
        snap = _snapshot_for(ctx)
        topo = _topology_t1t2()
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", _ctx("t1"))})
        with self.assertRaises(Z.FilterPlanError):
            Demo.example_plan(snap, prov, _Clock(), _OkAudit(), topo,
                              Z.FilterConfig(8), ctx)
        self.assertEqual([r.resource_id for r in prov.calls],
                         ["r1", "r2"])

    def test_non_mutation_complete(self):
        ctx = _ctx("t1")
        snap = _snapshot_for(ctx)
        topo = _topology_t1t2()
        mapping = {"r1": _facts("r1", ctx), "r2": _facts("r2", ctx)}
        prov = _MapProvider(dict(mapping))
        clock = _Clock()
        before = (
            snap.version,
            topo.tenants, topo.scopes,
            ctx,
            tuple((r.resource_id, r.subject_id, r.action_id,
                   r.correlation_id, r.context) for r in (
                       _request("r1", "d-r1", ctx),
                       _request("r2", "d-r2", ctx))),
            tuple(sorted(mapping.keys())),
        )
        plan = Demo.example_plan(snap, prov, clock, _OkAudit(), topo,
                                 Z.FilterConfig(8), ctx)
        after = (
            snap.version,
            topo.tenants, topo.scopes,
            ctx,
            tuple((r.resource_id, r.subject_id, r.action_id,
                   r.correlation_id, r.context) for r in (
                       _request("r1", "d-r1", ctx),
                       _request("r2", "d-r2", ctx))),
            tuple(sorted(mapping.keys())),
        )
        self.assertEqual(before, after)
        self.assertEqual(plan.resource_ids, ("r1", "r2"))
        self.assertEqual(clock.calls, 1)
        self.assertEqual(
            [(r.resource_id, r.subject_id, r.action_id,
              r.correlation_id, r.context) for r in prov.calls],
            [("r1", "s1", "a1", "c1", ctx),
             ("r2", "s1", "a1", "c1", ctx)])


if __name__ == "__main__":
    unittest.main()
