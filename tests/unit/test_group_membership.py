"""Groupes et appartenances n:m, structure seule sans autorisation."""

import dataclasses
import unittest
import uuid

from pixs.core import identity as I
from pixs.core.scope import ScopeContext, ScopeType


def u7(n):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


def ctx_tenant(tenant="t1", scope=None):
    if scope is None:
        return ScopeContext(ScopeType.TENANT, tenant)
    return ScopeContext(ScopeType.TENANT, tenant, scope)


def ctx_platform():
    return ScopeContext(ScopeType.PLATFORM)


class GroupMembershipTest(unittest.TestCase):
    def test_contexts_tenant_and_platform(self):
        g1 = I.Group(u7(1), ctx_tenant("t1"))
        g2 = I.Group(u7(2), ctx_tenant("t1", "s1"))
        g3 = I.Group(u7(3), ctx_platform())
        self.assertTrue(I.validate_group(g1))
        self.assertTrue(I.validate_group(g2))
        self.assertTrue(I.validate_group(g3))

    def test_context_mandatory_bad_altered_incomplete(self):
        with self.assertRaises(I.GroupError):
            I.Group(u7(10), "t1")
        with self.assertRaises(I.GroupError):
            I.Group(u7(10), None)
        forged = object.__new__(I.Group)
        object.__setattr__(forged, "group_id", u7(10))
        object.__setattr__(forged, "context", "t1")
        with self.assertRaises(I.GroupError):
            I.validate_group(forged)
        altered = I.Group(u7(11), ctx_tenant("t1"))
        object.__setattr__(altered, "context", "synthetic-sensitive-marker-ctx")
        with self.assertRaises(I.GroupError):
            I.validate_group(altered)
        incomplete = object.__new__(I.Group)
        object.__setattr__(incomplete, "group_id", u7(12))
        with self.assertRaises(I.GroupError):
            I.validate_group(incomplete)

    def test_uuid_shared_helper_versions_subclasses(self):
        for bad in (
            uuid.UUID(int=(4 << 76) | (2 << 62) | 1),
            123, "x" * 36, True, None,
        ):
            with self.subTest(bad=type(bad).__name__):
                with self.assertRaises(I.GroupError):
                    I.Group(bad, ctx_tenant("t1"))
                with self.assertRaises(I.GroupError):
                    I.Membership(bad, u7(20))
                with self.assertRaises(I.GroupError):
                    I.Membership(u7(20), bad)

        class SubUUID(uuid.UUID):
            pass

        sub = SubUUID(int=u7(21).int)
        with self.assertRaises(I.GroupError):
            I.Group(sub, ctx_tenant("t1"))

    def test_membership_two_ids_frozen_slots(self):
        m = I.Membership(u7(30), u7(31))
        self.assertTrue(I.validate_membership(m))
        self.assertFalse(hasattr(m, "__dict__"))
        for value in (I.Group(u7(32), ctx_tenant("t1")), I.Group(u7(33), ctx_tenant("t1"))):
            self.assertFalse(hasattr(value, "__dict__"))
            with self.assertRaises(dataclasses.FrozenInstanceError):
                value.group_id = u7(34)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            m.user_id = u7(35)

    def test_exact_classes_incomplete_subclass_invalid_user(self):
        for validate, cls in (
            (I.validate_group, I.Group),
            (I.validate_membership, I.Membership),
        ):
            with self.subTest(cls=cls.__name__):
                for bad in (None, (), "synthetic-invalid", object.__new__(cls)):
                    with self.assertRaises(I.GroupError):
                        validate(bad)
                subclass = type("Sub", (cls,), {})
                with self.assertRaises(I.GroupError):
                    validate(object.__new__(subclass))
        forged_user = object.__new__(I.User)
        object.__setattr__(forged_user, "user_id", "bad")
        with self.assertRaises(I.GroupError):
            I.validate_memberships((forged_user,), (I.Group(u7(40), ctx_tenant("t1")),), ())

    def test_exact_tuples_empty_independent(self):
        users = (I.User(u7(50)),)
        groups = (I.Group(u7(51), ctx_tenant("t1")),)
        class TupleSubclass(tuple):
            pass
        for bad in ([], None, {}, TupleSubclass()):
            for pos in range(3):
                args = [users, groups, ()]
                args[pos] = bad
                with self.assertRaises(I.GroupError):
                    I.validate_memberships(*args)
        self.assertTrue(I.validate_memberships((), (), ()))
        self.assertTrue(I.validate_memberships(users, (), ()))
        self.assertTrue(I.validate_memberships((), groups, ()))
        self.assertTrue(I.validate_memberships(users, groups, ()))

    def test_nm_complete_accepted(self):
        users = (I.User(u7(60)), I.User(u7(61)))
        groups = (
            I.Group(u7(62), ctx_tenant("t1")),
            I.Group(u7(63), ctx_platform()),
        )
        memberships = (
            I.Membership(u7(60), u7(62)),
            I.Membership(u7(60), u7(63)),
            I.Membership(u7(61), u7(62)),
            I.Membership(u7(61), u7(63)),
        )
        self.assertTrue(I.validate_memberships(users, groups, memberships))

    def test_absent_duplicates_collision_duplicate_pair(self):
        users = (I.User(u7(70)), I.User(u7(71)))
        groups = (I.Group(u7(72), ctx_tenant("t1")), I.Group(u7(73), ctx_tenant("t1")))
        with self.assertRaises(I.GroupError):
            I.validate_memberships(users, groups, (I.Membership(u7(79), u7(72)),))
        with self.assertRaises(I.GroupError):
            I.validate_memberships(users, groups, (I.Membership(u7(70), u7(79)),))
        with self.assertRaises(I.GroupError):
            I.validate_memberships(
                users + (I.User(u7(70)),), groups, ())
        with self.assertRaises(I.GroupError):
            I.validate_memberships(
                users, groups + (I.Group(u7(72), ctx_tenant("t1")),), ())
        with self.assertRaises(I.GroupError):
            I.validate_memberships(
                (I.User(u7(80)),), (I.Group(u7(80), ctx_tenant("t1")),), ())
        pair = I.Membership(u7(70), u7(72))
        dup = I.Membership(u7(70), u7(72))
        with self.assertRaises(I.GroupError):
            I.validate_memberships(users, groups, (pair, dup))

    def test_non_mutation_primitive_values_no_registry(self):
        users = (I.User(u7(90)), I.User(u7(91)))
        groups = (I.Group(u7(92), ctx_tenant("t1")), I.Group(u7(93), ctx_tenant("t1", "s9")))
        memberships = (I.Membership(u7(90), u7(92)), I.Membership(u7(91), u7(93)))
        before_users = tuple(u.user_id.int for u in users)
        before_groups = tuple(
            (g.group_id.int, g.context.scope_type, g.context.tenant_id, g.context.scope_id)
            for g in groups)
        before_links = tuple((m.user_id.int, m.group_id.int) for m in memberships)
        self.assertTrue(I.validate_memberships(users, groups, memberships))
        self.assertEqual(tuple(u.user_id.int for u in users), before_users)
        self.assertEqual(
            tuple((g.group_id.int, g.context.scope_type, g.context.tenant_id, g.context.scope_id)
                  for g in groups),
            before_groups)
        self.assertEqual(
            tuple((m.user_id.int, m.group_id.int) for m in memberships), before_links)
        with self.assertRaises(I.GroupError):
            I.validate_memberships((), (), memberships)
        self.assertTrue(I.validate_memberships(users, groups, memberships))

    def test_hostile_never_called_marker_absent(self):
        calls = []
        marker = "synthetic-sensitive-marker-groups"

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
            lambda: I.Group(evil, ctx_tenant("t1")),
            lambda: I.Group(u7(99), evil),
            lambda: I.Membership(evil, u7(99)),
            lambda: I.Membership(u7(99), evil),
        ):
            with self.assertRaises(I.GroupError):
                factory()
        for validate in (I.validate_group, I.validate_membership):
            with self.assertRaises(I.GroupError):
                validate(evil)
        forged = object.__new__(I.Group)
        object.__setattr__(forged, "group_id", marker)
        object.__setattr__(forged, "context", ctx_tenant("t1"))
        try:
            I.validate_group(forged)
        except I.GroupError as exc:
            self.assertEqual(exc.code, "GROUP_INVALID")
            self.assertNotIn(marker, str(exc))
            self.assertNotIn(marker, repr(exc))
        else:
            self.fail("GroupError attendue")
        self.assertEqual(calls, [])


    def test_incomplete_altered_and_subclass_scope_contexts(self):
        incomplete = object.__new__(ScopeContext)
        platform_with_tenant = ctx_platform()
        object.__setattr__(platform_with_tenant, "tenant_id", "t1")
        tenant_bad_scope = ctx_tenant()
        object.__setattr__(tenant_bad_scope, "scope_id", 123)
        class ContextSubclass(ScopeContext):
            pass
        subclass = object.__new__(ContextSubclass)
        for context in (incomplete, platform_with_tenant, tenant_bad_scope, subclass):
            with self.assertRaises(I.GroupError):
                I.Group(u7(101), context)

    def test_ensemble_revalidates_altered_members(self):
        for position in range(3):
            user = I.User(u7(110))
            group = I.Group(u7(111), ctx_tenant())
            membership = I.Membership(u7(110), u7(111))
            values = (user, group, membership)
            fields = ("user_id", "context", "group_id")
            object.__setattr__(values[position], fields[position], "synthetic-invalid")
            with self.assertRaises(I.GroupError):
                I.validate_memberships((user,), (group,), (membership,))


if __name__ == "__main__":
    unittest.main()
