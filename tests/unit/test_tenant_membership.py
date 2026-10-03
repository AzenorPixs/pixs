"""TenantMembership N-N DigitalIdentity-Tenant, structure seule."""

import dataclasses
import unittest
import uuid

from pixs.core import identity as I


def u7(n):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


def ident(n, itype=None, state=None):
    itype = itype if itype is not None else I.IdentityType.HUMAN
    state = state if state is not None else I.IdentityState.ACTIVE
    return I.DigitalIdentity(u7(n), itype, state)


class TenantMembershipTest(unittest.TestCase):
    def test_nn_four_combinations_accepted(self):
        ids = (ident(1), ident(2))
        tenants = ("tenant-01", "tenant-02")
        memberships = (
            I.TenantMembership(u7(1), "tenant-01"),
            I.TenantMembership(u7(1), "tenant-02"),
            I.TenantMembership(u7(2), "tenant-01"),
            I.TenantMembership(u7(2), "tenant-02"),
        )
        self.assertTrue(I.validate_tenant_membership(memberships[0]))
        self.assertTrue(I.validate_tenant_memberships(ids, tenants, memberships))

    def test_service_without_user_admitted(self):
        svc = I.DigitalIdentity(u7(11), I.IdentityType.SERVICE, I.IdentityState.ACTIVE)
        m = I.TenantMembership(u7(11), "tenant-01")
        self.assertTrue(I.validate_tenant_memberships((svc,), ("tenant-01",), (m,)))

    def test_all_types_and_states_valid_no_right(self):
        for itype in I.IdentityType:
            for state in I.IdentityState:
                with self.subTest(itype=itype.value, state=state.value):
                    ident_obj = I.DigitalIdentity(u7(21), itype, state)
                    m = I.TenantMembership(u7(21), "tenant-01")
                    self.assertTrue(I.validate_tenant_memberships((ident_obj,), ("tenant-01",), (m,)))
                    self.assertFalse(hasattr(m, "active"))
                    self.assertFalse(hasattr(m, "rights"))

    def test_error_constant_without_value(self):
        marker = "synthetic-sensitive-marker-tenant"
        with self.assertRaises(I.TenantMembershipError) as caught:
            I.TenantMembership(marker, "tenant-01")
        self.assertEqual(caught.exception.code, "TENANT_MEMBERSHIP_INVALID")
        self.assertEqual(caught.exception.element, "tenant_membership")
        self.assertEqual(caught.exception.step, "validate_tenant_membership")
        self.assertNotIn(marker, str(caught.exception))
        self.assertNotIn(marker, repr(caught.exception))

    def test_uuid_exact_and_corrupted(self):
        for bad in (
            uuid.UUID(int=(4 << 76) | (2 << 62) | 1),
            123, "x" * 36, True, None,
        ):
            with self.subTest(bad=type(bad).__name__):
                with self.assertRaises(I.TenantMembershipError):
                    I.TenantMembership(bad, "tenant-01")

        class SubUUID(uuid.UUID):
            pass

        with self.assertRaises(I.TenantMembershipError):
            I.TenantMembership(SubUUID(int=u7(31).int), "tenant-01")

    def test_tenant_str_exact_no_normalization(self):
        for bad in (None, "", 123, True, b"tenant-01", ("tenant-01",)):
            with self.subTest(bad=type(bad).__name__):
                with self.assertRaises(I.TenantMembershipError):
                    I.TenantMembership(u7(41), bad)

        class SubStr(str):
            pass

        with self.assertRaises(I.TenantMembershipError):
            I.TenantMembership(u7(41), SubStr("tenant-01"))
        ok = I.TenantMembership(u7(42), " t1")
        self.assertTrue(I.validate_tenant_membership(ok))
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships((ident(42),), ("t1",), (I.TenantMembership(u7(42), " t1"),))
        self.assertTrue(I.validate_tenant_memberships((ident(42),), (" t1",), (I.TenantMembership(u7(42), " t1"),)))

    def test_exact_tuples_and_empty(self):
        ids = (ident(50),)
        tenants = ("tenant-01",)

        class TupleSubclass(tuple):
            pass

        for bad in ([], None, {}, TupleSubclass()):
            for pos in range(3):
                args = [ids, tenants, ()]
                args[pos] = bad
                with self.assertRaises(I.TenantMembershipError):
                    I.validate_tenant_memberships(*args)
        self.assertTrue(I.validate_tenant_memberships((), (), ()))
        self.assertTrue(I.validate_tenant_memberships(ids, (), ()))
        self.assertTrue(I.validate_tenant_memberships((), tenants, ()))
        self.assertTrue(I.validate_tenant_memberships(ids, tenants, ()))

    def test_exact_classes_subclass_rejected(self):
        for bad in (None, (), "synthetic-invalid", object.__new__(I.TenantMembership)):
            with self.assertRaises(I.TenantMembershipError):
                I.validate_tenant_membership(bad)
        subclass = type("Sub", (I.TenantMembership,), {})
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_membership(object.__new__(subclass))

    def test_corrupted_missing_slots_and_altered(self):
        forged = object.__new__(I.TenantMembership)
        object.__setattr__(forged, "identity_id", u7(60))
        object.__setattr__(forged, "tenant_id", "tenant-01")
        self.assertTrue(I.validate_tenant_membership(forged))
        incomplete = object.__new__(I.TenantMembership)
        object.__setattr__(incomplete, "identity_id", u7(61))
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_membership(incomplete)
        altered = I.TenantMembership(u7(62), "tenant-01")
        object.__setattr__(altered, "tenant_id", 123)
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_membership(altered)

    def test_absent_duplicates_and_pairs(self):
        ids = (ident(70), ident(71))
        tenants = ("tenant-01", "tenant-02")
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships(ids, tenants, (I.TenantMembership(u7(79), "tenant-01"),))
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships(ids, tenants, (I.TenantMembership(u7(70), "tenant-unknown"),))
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships(ids + (ident(70),), tenants, ())
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships(ids, tenants + ("tenant-01",), ())
        pair = I.TenantMembership(u7(70), "tenant-01")
        dup = I.TenantMembership(u7(70), "tenant-01")
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships(ids, tenants, (pair, dup))

    def test_frozen_slots_immutable(self):
        m = I.TenantMembership(u7(80), "tenant-01")
        self.assertFalse(hasattr(m, "__dict__"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            m.tenant_id = "tenant-02"

    def test_hostile_never_called(self):
        calls = []

        class Evil:
            def __str__(self):
                calls.append("str")
                raise AssertionError("str")

            def __repr__(self):
                calls.append("repr")
                raise AssertionError("repr")

            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("eq")

            def __hash__(self):
                calls.append("hash")
                raise AssertionError("hash")

        evil = Evil()
        for factory in (
            lambda: I.TenantMembership(evil, "tenant-01"),
            lambda: I.TenantMembership(u7(90), evil),
        ):
            with self.assertRaises(I.TenantMembershipError):
                factory()
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_membership(evil)
        self.assertEqual(calls, [])


    def test_corrupted_uuid_and_identity(self):
        broken = u7(63)
        object.__setattr__(broken, "int", "synthetic-invalid-uuid")
        with self.assertRaises(I.TenantMembershipError) as caught:
            I.TenantMembership(broken, "tenant-01")
        self.assertIsNone(caught.exception.__cause__)
        self.assertTrue(caught.exception.__suppress_context__)
        identity = ident(64)
        object.__setattr__(identity, "state", "synthetic-invalid-state")
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships((identity,), ("tenant-01",), ())
        incomplete = object.__new__(I.DigitalIdentity)
        with self.assertRaises(I.TenantMembershipError):
            I.validate_tenant_memberships((incomplete,), (), ())

    def test_hostile_collections_and_elements_no_callbacks(self):
        calls = []

        class HostileMeta(type):
            def __eq__(cls, other):
                calls.append("type_eq")
                raise AssertionError("type_eq")

        class Hostile(metaclass=HostileMeta):
            def __getattribute__(self, name):
                calls.append("getattribute")
                raise AssertionError("getattribute")

            def __hash__(self):
                calls.append("hash")
                raise AssertionError("hash")

            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("eq")

            def __iter__(self):
                calls.append("iter")
                raise AssertionError("iter")

            def __repr__(self):
                calls.append("repr")
                raise AssertionError("repr")

        evil = Hostile()
        for pos in range(3):
            for bad in (evil, (evil,)):
                args = [(), (), ()]
                args[pos] = bad
                with self.assertRaises(I.TenantMembershipError):
                    I.validate_tenant_memberships(*args)
        self.assertEqual(calls, [])

if __name__ == "__main__":
    unittest.main()
