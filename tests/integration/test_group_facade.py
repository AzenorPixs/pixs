"""Groupes via facades publiques, sans autorisation ni topologie."""

import unittest
import uuid

from pixs.core import identity as I
from pixs.core.scope import ScopeContext, ScopeType


def u7(n):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


class GroupFacadeTest(unittest.TestCase):
    def test_existing_identity_contract_then_groups(self):
        u1, u2 = u7(1), u7(2)
        i1 = u7(11)
        user1 = I.User(u1)
        user2 = I.User(u2)
        ident = I.DigitalIdentity(i1, I.IdentityType.HUMAN, I.IdentityState.ACTIVE)
        link = I.IdentityLink(u1, i1)
        self.assertTrue(I.validate_links((user1, user2), (ident,), (link,)))
        g1 = I.Group(u7(21), ScopeContext(ScopeType.TENANT, "t1"))
        g2 = I.Group(u7(22), ScopeContext(ScopeType.PLATFORM))
        memberships = (
            I.Membership(u1, u7(21)),
            I.Membership(u1, u7(22)),
            I.Membership(u2, u7(21)),
        )
        self.assertTrue(
            I.validate_memberships((user1, user2), (g1, g2), memberships))
        self.assertEqual(g1.context.scope_type, ScopeType.TENANT)
        self.assertEqual(g2.context.scope_type, ScopeType.PLATFORM)
        self.assertFalse(hasattr(g1, "permissions"))
        self.assertFalse(hasattr(g1, "authentication_assurance"))
        self.assertFalse(hasattr(g1, "session"))

    def test_group_exports_and_privates_hidden(self):
        for name in (
            "Group", "Membership", "GroupError",
            "validate_group", "validate_membership", "validate_memberships",
        ):
            self.assertIn(name, I.__all__)
            self.assertTrue(hasattr(I, name))
        for name in ("_check_uuid", "_check_context", "groups"):
            self.assertNotIn(name, I.__all__)

    def test_stable_errors_absent_refs_duplicate(self):
        marker = "synthetic-invalid-group-entry"
        with self.assertRaises(I.GroupError) as caught:
            I.Group(marker, ScopeContext(ScopeType.TENANT, "t1"))
        self.assertEqual(caught.exception.code, "GROUP_INVALID")
        self.assertNotIn(marker, str(caught.exception))
        self.assertNotIn(marker, repr(caught.exception))
        users = (I.User(u7(31)),)
        groups = (I.Group(u7(32), ScopeContext(ScopeType.TENANT, "t1")),)
        with self.assertRaises(I.GroupError):
            I.validate_memberships(users, groups, (I.Membership(u7(39), u7(32)),))
        pair = I.Membership(u7(31), u7(32))
        with self.assertRaises(I.GroupError):
            I.validate_memberships(users, groups, (pair, pair))


if __name__ == "__main__":
    unittest.main()
