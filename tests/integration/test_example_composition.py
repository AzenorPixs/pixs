"""Integration exemple P0 bout-en-bout, memoire sans persistance."""

import dataclasses
import datetime
import unittest
from pathlib import Path

from pixs.core import authz as Z
from pixs.core.scope import ScopeContext, ScopeType
from pixs.core.scope.ownership import ResourceOwnership
from pixs.core.scope.topology import TopologySnapshot
from pixs.example import demo as Demo
from tests.conformity_fixtures import synthetic_attestations


def _utc(y, mo, d, h=0, mi=0, s=0):
    return datetime.datetime(y, mo, d, h, mi, s, tzinfo=datetime.timezone.utc)


T0 = _utc(2026, 1, 2, 12, 0, 0)


def _provider_text():
    return Path("src/pixs/example/component.toml").read_text(
        encoding="utf-8")


def _limits():
    return Z.Limits(
        max_policies=32, max_selector_values=32,
        max_conditions_per_policy=16, max_set_values=32,
        max_attributes=16, max_memberships=32,
        max_id_length=64, max_value_length=128,
        max_cost=1000000, ttl_seconds=60, max_freshness_seconds=600)


def _catalog():
    t1 = ScopeContext(ScopeType.TENANT, "t1")
    t2 = ScopeContext(ScopeType.TENANT, "t2")
    return Z.Catalog(
        ("s1",), ("r1", "r2"), ("a1",),
        (t1, t2), (("role", "STR"),))


def _ctx(tenant):
    return ScopeContext(ScopeType.TENANT, tenant)


def _topology():
    return TopologySnapshot(("t1", "t2"), ())


def _policy(pid, effect, resources, ctx):
    return Z.Policy(
        pid, "v1", "owner1", effect,
        Z.Selector("subject", ("s1",)),
        Z.Selector("resource", resources),
        Z.Selector("action", ("a1",)),
        Z.ScopeSelector((ctx,)))


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
        self.calls.append(request.resource_id)
        return self._mapping[request.resource_id]


class _Clock:
    def now(self):
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


class ExampleCompositionTest(unittest.TestCase):
    def test_resolution_contrat_ordre(self):
        provider, consumer = Demo.example_texts(_provider_text())
        texts = (provider, consumer)
        atts = synthetic_attestations(texts)
        first = Demo.example_compose(texts, atts)
        second = Demo.example_compose((consumer, provider), atts)
        self.assertTrue(first.activated)
        self.assertTrue(second.activated)
        self.assertEqual(first.order, second.order)
        self.assertNotEqual(first.order, ())

    def test_attestations_manquantes(self):
        provider, consumer = Demo.example_texts(_provider_text())
        result = Demo.example_compose([provider, consumer])
        self.assertFalse(result.activated)

        class _CapturingProvider:
            def __init__(self):
                self.calls = []

            def resolve(self, request):
                self.calls.append(request.resource_id)
                raise AssertionError("ne doit pas etre appele")

        capturing = _CapturingProvider()

        def _workflow_caller():
            if not result.activated:
                return None
            return Demo.example_plan(
                _snapshot_for_refusal(), capturing, _Clock(),
                _OkAudit(), _topology(), Z.FilterConfig(8), _ctx("t2"))

        self.assertIsNone(_workflow_caller())
        self.assertEqual(capturing.calls, [])

    def test_pipeline_t2_allow_deny(self):
        provider, consumer = Demo.example_texts(_provider_text())
        texts = (provider, consumer)
        atts = synthetic_attestations(texts)
        composed = Demo.example_compose(texts, atts)
        self.assertTrue(composed.activated)
        self.assertEqual(composed.order, ("example.hello",
                                         "example.client"))
        self.assertIn(("example.client", "example.hello"),
                      composed.edges)
        self.assertFalse(composed.globally_compatible)
        from pixs.kernel.manifest import parse_manifest_text
        manifest = parse_manifest_text(provider)
        self.assertEqual(manifest.implemented_contracts[0].id,
                         "example.hello.contract")
        self.assertEqual(manifest.implemented_contracts[0].version,
                         "1.0.0")
        ctx = _ctx("t2")
        snap = Z.build_snapshot(
            "epoch1",
            (_policy("a", Z.Effect.ALLOW, ("r1", "r2"), ctx),
             _policy("d", Z.Effect.DENY, ("r2",), ctx)),
            _catalog(), _limits())
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", ctx)})
        audit = _OkAudit()
        plan = Demo.example_plan(snap, prov, _Clock(), audit,
                                 _topology(), Z.FilterConfig(8), ctx)
        self.assertEqual(plan.resource_ids, ("r1",))
        self.assertEqual(plan.context, ctx)
        self.assertTrue(any(e.resource_id == "r2" for e in audit.events))

    def test_pipeline_audit_false(self):
        ctx = _ctx("t2")
        snap = Z.build_snapshot(
            "epoch1",
            (_policy("a", Z.Effect.ALLOW, ("r1", "r2"), ctx),
             _policy("d", Z.Effect.DENY, ("r2",), ctx)),
            _catalog(), _limits())
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", ctx)})
        audit = _FailAudit()
        with self.assertRaises(Z.FilterPlanError):
            Demo.example_plan(snap, prov, _Clock(), audit,
                              _topology(), Z.FilterConfig(8), ctx)
        self.assertEqual(prov.calls, ["r1", "r2"])

    def test_cross_tenant(self):
        ctx = _ctx("t2")
        snap = Z.build_snapshot(
            "epoch1",
            (_policy("a", Z.Effect.ALLOW, ("r1", "r2"), ctx),),
            _catalog(), _limits())
        prov = _MapProvider({"r1": _facts("r1", ctx),
                             "r2": _facts("r2", _ctx("t1"))})
        with self.assertRaises(Z.FilterPlanError):
            Demo.example_plan(snap, prov, _Clock(), _OkAudit(),
                              _topology(), Z.FilterConfig(8), ctx)

    def test_versions_frozen(self):
        from pixs.kernel.manifest import parse_manifest_text
        provider, _ = Demo.example_texts(_provider_text())
        manifest = parse_manifest_text(provider)
        self.assertEqual(manifest.version, "1.0.0")
        self.assertEqual(manifest.implemented_contracts[0].version,
                         "1.0.0")
        frozen = Demo.example_scope()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            frozen[0].tenant_id = "tx"


def _snapshot_for_refusal():
    ctx = _ctx("t2")
    return Z.build_snapshot(
        "epoch1",
        (_policy("a", Z.Effect.ALLOW, ("r1", "r2"), ctx),),
        _catalog(), _limits())


if __name__ == "__main__":
    unittest.main()
