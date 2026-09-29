"""Tests propriété via façade publique. ACL aval hors périmètre."""

import dataclasses
import unittest

from pixs.core import scope


class OwnershipTest(unittest.TestCase):
    def test_contexts(self):
        root = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        child = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "s1")
        plat = scope.ScopeContext(scope.ScopeType.PLATFORM)
        o1 = scope.ResourceOwnership("r1", root)
        o2 = scope.ResourceOwnership("r2", child)
        o3 = scope.ResourceOwnership("r3", plat)
        self.assertIs(o1.context, root)
        self.assertIs(o2.context, child)
        self.assertIs(o3.context, plat)

    def test_bad_ids(self):
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        for bad in ("", True, 1, ["r"], b"r"):
            with self.assertRaises(scope.OwnershipError):
                scope.ResourceOwnership(bad, ctx)

    def test_bad_context(self):
        with self.assertRaises(scope.OwnershipError):
            scope.ResourceOwnership("r1", "ctx")
        with self.assertRaises(scope.OwnershipError):
            scope.ResourceOwnership("r1", None)

    def test_frozen(self):
        owner = scope.ResourceOwnership(
            "r1", scope.ScopeContext(scope.ScopeType.TENANT, "t1"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            owner.resource_id = "r2"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            del owner.context

    def test_boundary(self):
        snap = scope.TopologySnapshot(["t1"], [])
        owner = scope.ResourceOwnership(
            "r1", scope.ScopeContext(scope.ScopeType.TENANT, "t1", "sX"))
        with self.assertRaises(scope.TopologyError):
            scope.validate_context(owner.context, snap)
        self.assertEqual(owner.resource_id, "r1")

    def test_no_leak(self):
        with self.assertRaises(scope.OwnershipError) as cm:
            scope.ResourceOwnership("", "bad")
        text = str(cm.exception) + repr(cm.exception)
        self.assertNotIn("bad", text)


if __name__ == "__main__":
    unittest.main()
