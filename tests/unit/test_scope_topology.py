"""Tests topologie via façade publique."""

import dataclasses
import itertools
import traceback
import unittest

from pixs.core import scope


class BadIterable:
    def __iter__(self):
        raise RuntimeError("boom-" + "topo-9c2e")


def _boom_message():
    return "boom-" + "topo-9c2e"


class TopologyTest(unittest.TestCase):
    def test_node_invalid(self):
        with self.assertRaises(scope.TopologyError):
            scope.ScopeNode("", "t1")
        with self.assertRaises(scope.TopologyError):
            scope.ScopeNode("s1", "")
        with self.assertRaises(scope.TopologyError):
            scope.ScopeNode(True, "t1")
        with self.assertRaises(scope.TopologyError):
            scope.ScopeNode(["s"], "t1")
        with self.assertRaises(scope.TopologyError):
            scope.ScopeNode("s1", "t1", "")
        node = scope.ScopeNode("s1", "t1")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            node.scope_id = "s2"

    def test_snapshot_refusals(self):
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(["t1"], [scope.ScopeNode("s1", "tX")])
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(["t1", "t1"], [])
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(
                ["t1"],
                [scope.ScopeNode("s1", "t1"), scope.ScopeNode("s1", "t1")],
            )
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(
                ["t1"], [scope.ScopeNode("s1", "t1", "missing")]
            )
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(
                ["t1", "t2"],
                [scope.ScopeNode("s1", "t1", "s2"),
                 scope.ScopeNode("s2", "t2")],
            )
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(["t1"], [scope.ScopeNode("s1", "t1", "s1")])
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(
                ["t1"],
                [scope.ScopeNode("a", "t1", "c"),
                 scope.ScopeNode("b", "t1", "a"),
                 scope.ScopeNode("c", "t1", "b")],
            )
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot("t1", [])
        with self.assertRaises(scope.TopologyError):
            scope.TopologySnapshot(["t1"], 123)

    def test_valid_multi(self):
        snap = scope.TopologySnapshot(
            ["t1", "t2"],
            [scope.ScopeNode("s1", "t1"), scope.ScopeNode("s2", "t2")],
        )
        self.assertEqual(set(snap.tenants), {"t1", "t2"})

    def test_order_tiebreak(self):
        nodes = [scope.ScopeNode("b", "t1"), scope.ScopeNode("z", "t1"),
                 scope.ScopeNode("a", "t1", "z")]
        expected = ("b", "z", "a")
        for perm in itertools.permutations(nodes):
            snap = scope.TopologySnapshot(["t1"], list(perm))
            self.assertEqual(scope.resolve_order(snap), expected)

    def test_deep_chain(self):
        n = 1500
        nodes = [scope.ScopeNode("s0", "t1")]
        for i in range(1, n):
            nodes.append(scope.ScopeNode("s%d" % i, "t1", "s%d" % (i - 1)))
        snap = scope.TopologySnapshot(["t1"], nodes)
        order = scope.resolve_order(snap)
        self.assertEqual(order, tuple("s%d" % i for i in range(n)))

    def test_defensive_copy(self):
        tenants = ["t1"]
        nodes = [scope.ScopeNode("s1", "t1")]
        snap = scope.TopologySnapshot(tenants, nodes)
        tenants.append("t2")
        nodes.append(scope.ScopeNode("s2", "t1"))
        self.assertEqual(tuple(snap.tenants), ("t1",))
        self.assertEqual(len(snap.scopes), 1)
        it = (x for x in ["t1"])
        snap2 = scope.TopologySnapshot(it, [])
        self.assertEqual(tuple(snap2.tenants), ("t1",))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            snap.tenants = ()
        self.assertIsInstance(snap.scopes, tuple)

    def test_validate_context(self):
        snap = scope.TopologySnapshot(
            ["t1", "t2"], [scope.ScopeNode("s1", "t1")])
        ok = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "s1")
        self.assertTrue(scope.validate_context(ok, snap))
        cross = scope.ScopeContext(scope.ScopeType.TENANT, "t2", "s1")
        with self.assertRaises(scope.TopologyError):
            scope.validate_context(cross, snap)
        bad_tenant = scope.ScopeContext(scope.ScopeType.TENANT, "tX")
        with self.assertRaises(scope.TopologyError):
            scope.validate_context(bad_tenant, snap)
        bad_scope = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "sX")
        with self.assertRaises(scope.TopologyError):
            scope.validate_context(bad_scope, snap)
        plat = scope.ScopeContext(scope.ScopeType.PLATFORM)
        self.assertTrue(scope.validate_context(plat, snap))

    def test_bad_iterable_no_leak(self):
        try:
            scope.TopologySnapshot(BadIterable(), [])
        except scope.TopologyError as err:
            formatted = "".join(traceback.format_exception(err))
            text = str(err) + repr(err)
            self.assertIn("test_bad_iterable_no_leak", formatted)
            self.assertNotIn(_boom_message(), text)
            self.assertNotIn(_boom_message(), formatted)
        else:
            self.fail("TopologyError not raised")


if __name__ == "__main__":
    unittest.main()
