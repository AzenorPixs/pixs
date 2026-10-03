"""Canonicalite et refus de la jonction structurelle tenant."""

from dataclasses import FrozenInstanceError
import unittest

from pixs.backend.api.tenant_claim import resolve_tenant_boundary
from pixs.core.scope import (
    PropagationDenied, ScopeContext, ScopeType, TopologySnapshot,
)


class Hostile:
    def __repr__(self):
        raise AssertionError("repr interdit")

    def __str__(self):
        raise AssertionError("str interdit")

    def __eq__(self, other):
        raise AssertionError("egalite interdite")

    def __hash__(self):
        raise AssertionError("hash interdit")


class HostileMeta(type):
    def __eq__(cls, other):
        raise AssertionError("egalite de classe interdite")


class HostileString(str, metaclass=HostileMeta):
    def __eq__(self, other):
        raise AssertionError("egalite str sous-classee interdite")


class TenantClaimTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = TopologySnapshot(tenants=("tenant-A", "tenant-B"))
        self.refused = []

    def resolve(self, path, claim=None, **extra):
        return resolve_tenant_boundary(
            path, claim, snapshot=extra.get("snapshot", self.snapshot),
            on_denied=extra.get("on_denied", self.refused.append),
        )

    def assert_denial(self, path, claim=None, **extra):
        before = len(self.refused)
        with self.assertRaises(PropagationDenied) as caught:
            self.resolve(path, claim, **extra)
        self.assertEqual(len(self.refused), before + 1)
        diagnostic = self.refused[-1]
        self.assertEqual(
            (diagnostic.code, diagnostic.element, diagnostic.step),
            ("SCOPE_PROPAGATION_DENIED", "scope_propagation", "check_claim"),
        )
        self.assertEqual(str(caught.exception), "Contexte de périmètre refusé.")

    def test_canonical_without_claim(self):
        context = self.resolve("tenant-A")
        self.assertIs(type(context), ScopeContext)
        self.assertIs(context.scope_type, ScopeType.TENANT)
        self.assertEqual(context.tenant_id, "tenant-A")
        self.assertIsNone(context.scope_id)
        self.assertEqual(self.refused, [])

    def test_matching_claim_has_no_refusal(self):
        context = self.resolve("tenant-A", "tenant-A")
        self.assertEqual(context.tenant_id, "tenant-A")
        self.assertEqual(self.refused, [])

    def test_conflict_refuses_once_with_constant_diagnostic(self):
        self.assert_denial("tenant-A", "tenant-B")

    def test_absent_canonical_tenant_refuses(self):
        self.assert_denial("absent")

    def test_invalid_path_types_do_not_invoke_input_hooks(self):
        values = (None, "", 0, False, b"tenant-A", Hostile(), HostileString("tenant-A"), ScopeContext(ScopeType.TENANT, "tenant-A"))
        for index, value in enumerate(values):
            with self.subTest(index=index):
                self.assert_denial(value)

    def test_invalid_present_claim_does_not_become_absent(self):
        values = ("", 0, False, b"tenant-A", Hostile(), HostileString("tenant-A"), ScopeContext(ScopeType.TENANT, "tenant-A"))
        for index, value in enumerate(values):
            with self.subTest(index=index):
                self.assert_denial("tenant-A", value)

    def test_opaque_values_preserved_without_normalization(self):
        for tenant in (" ", "tenant/A", "é", "e" + chr(0x0301)):
            with self.subTest(tenant=tenant):
                snapshot = TopologySnapshot(tenants=(tenant,))
                context = self.resolve(tenant, tenant, snapshot=snapshot)
                self.assertEqual(context.tenant_id, tenant)
        self.assertEqual(self.refused, [])

    def test_wrong_snapshot_refuses_without_hooks(self):
        self.assert_denial("tenant-A", snapshot=Hostile())

    def test_callback_required_and_exception_sanitized(self):
        with self.assertRaises(PropagationDenied):
            self.resolve("tenant-A", on_denied=None)
        def broken(diagnostic):
            raise RuntimeError("private-marker")
        with self.assertRaises(PropagationDenied) as caught:
            self.resolve("tenant-A", "tenant-B", on_denied=broken)
        self.assertNotIn("private-marker", str(caught.exception))
        self.assertTrue(caught.exception.__suppress_context__)

    def test_result_is_immutable_without_mutating_snapshot(self):
        context = self.resolve("tenant-A")
        with self.assertRaises(FrozenInstanceError):
            context.tenant_id = "tenant-B"
        self.assertEqual(self.snapshot.tenants, ("tenant-A", "tenant-B"))
        self.assertEqual(self.refused, [])


if __name__ == "__main__":
    unittest.main()
