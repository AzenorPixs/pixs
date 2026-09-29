"""Tests structure ScopeContext via façade publique."""

import dataclasses
import unittest

import pixs.core as core
from pixs.core import scope


class EvilStr(str):
    def __str__(self):
        raise AssertionError("no str")

    def __repr__(self):
        raise AssertionError("no repr")


class StructureTest(unittest.TestCase):
    def test_tenant_only(self):
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        self.assertEqual(ctx.tenant_id, "t1")
        self.assertIsNone(ctx.scope_id)

    def test_tenant_scope(self):
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, "t1", "s1")
        self.assertTrue(scope.validate_structure(ctx))

    def test_platform_no_ids(self):
        ctx = scope.ScopeContext(scope.ScopeType.PLATFORM)
        self.assertTrue(scope.validate_structure(ctx))

    def test_missing_tenant(self):
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.TENANT)

    def test_orphan_scope(self):
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.TENANT, None, "s1")

    def test_platform_with_ids(self):
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.PLATFORM, "t1")
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.PLATFORM, None, "s1")

    def test_bad_types(self):
        for bad in (True, 1, ["t"], b"t", EvilStr("t")):
            with self.assertRaises(scope.ScopeStructureError):
                scope.ScopeContext(scope.ScopeType.TENANT, bad)
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext("TENANT", "t1")
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.TENANT, "t1", 5)

    def test_str_subclass_rejected(self):
        class Sub(str):
            pass

        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.TENANT, Sub("t1"))

    def test_opaque_preserved(self):
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, "  t1  ")
        self.assertEqual(ctx.tenant_id, "  t1  ")

    def test_frozen(self):
        ctx = scope.ScopeContext(scope.ScopeType.TENANT, "t1")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            ctx.tenant_id = "t2"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            del ctx.tenant_id

    def test_empty_ids(self):
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.TENANT, "")
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(scope.ScopeType.TENANT, "t1", "")

    def test_bad_enum(self):
        with self.assertRaises(scope.ScopeStructureError):
            scope.ScopeContext(None, "t1")

    def test_evil_no_repr(self):
        with self.assertRaises(scope.ScopeStructureError) as cm:
            scope.validate_structure(EvilStr("synthetic-sensitive-marker"))
        err = cm.exception
        self.assertEqual(err.code, "SCOPE_STRUCTURE_INVALID")
        self.assertEqual(err.element, "scope_context")
        self.assertEqual(err.step, "validate_structure")
        self.assertNotIn("synthetic-sensitive-marker", repr(err))
        self.assertNotIn("synthetic-sensitive-marker", str(err))

    def test_error_constants(self):
        err = scope.ScopeStructureError()
        self.assertEqual(err.code, "SCOPE_STRUCTURE_INVALID")
        self.assertEqual(err.element, "scope_context")
        self.assertEqual(err.step, "validate_structure")

    def test_facade(self):
        self.assertIn("scope", core.__all__)
        self.assertIn("ScopeContext", scope.__all__)


if __name__ == "__main__":
    unittest.main()
