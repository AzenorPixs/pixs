"""Cardinalités et références du profil identité, sans stockage."""

import unittest
import uuid

from pixs.core import identity as I


def u7(n):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


class LinksTest(unittest.TestCase):
    def setUp(self):
        self.users = (I.User(u7(1)), I.User(u7(2)))
        self.identities = (
            I.DigitalIdentity(u7(3), I.IdentityType.HUMAN, I.IdentityState.ACTIVE),
            I.DigitalIdentity(u7(4), I.IdentityType.SERVICE, I.IdentityState.SUSPENDED),
        )
        self.links = (I.IdentityLink(u7(1), u7(3)), I.IdentityLink(u7(2), u7(4)))

    def test_empty_and_independent_entities(self):
        for users, identities in (((), ()), (self.users, ()), ((), self.identities),
                                  (self.users, self.identities)):
            self.assertIs(I.validate_links(users, identities, ()), True)

    def test_valid_bidirectional_links_and_subset(self):
        self.assertIs(I.validate_links(self.users, self.identities, self.links), True)
        self.assertIs(I.validate_links(self.users, self.identities, self.links[:1]), True)

    def test_missing_user_or_identity(self):
        for link in (I.IdentityLink(u7(9), u7(3)), I.IdentityLink(u7(1), u7(9))):
            with self.assertRaises(I.IdentityError):
                I.validate_links(self.users, self.identities, (link,))

    def test_one_user_cannot_link_two_identities(self):
        links = (I.IdentityLink(u7(1), u7(3)), I.IdentityLink(u7(1), u7(4)))
        with self.assertRaises(I.IdentityError):
            I.validate_links(self.users, self.identities, links)

    def test_one_identity_cannot_link_two_users(self):
        links = (I.IdentityLink(u7(1), u7(3)), I.IdentityLink(u7(2), u7(3)))
        with self.assertRaises(I.IdentityError):
            I.validate_links(self.users, self.identities, links)

    def test_repeated_link_rejected(self):
        with self.assertRaises(I.IdentityError):
            I.validate_links(self.users, self.identities, (self.links[0], self.links[0]))

    def test_duplicate_entity_ids_rejected_even_without_links(self):
        duplicate_user = I.User(u7(1))
        duplicate_identity = I.DigitalIdentity(u7(3), I.IdentityType.DEVICE, I.IdentityState.EXPIRED)
        with self.assertRaises(I.IdentityError):
            I.validate_links(self.users + (duplicate_user,), self.identities, ())
        with self.assertRaises(I.IdentityError):
            I.validate_links(self.users, self.identities + (duplicate_identity,), ())

    def test_uuid_collision_between_users_and_identities_rejected(self):
        user = I.User(u7(1))
        ident = I.DigitalIdentity(u7(1), I.IdentityType.SERVICE, I.IdentityState.REVOKED)
        for links in ((), (I.IdentityLink(u7(1), u7(1)),)):
            with self.assertRaises(I.IdentityError):
                I.validate_links((user,), (ident,), links)

    def test_collections_must_be_exact_tuples(self):
        class TupleSubclass(tuple):
            pass
        for bad in ([], None, {}, TupleSubclass()):
            for position in range(3):
                args = [self.users, self.identities, self.links]
                args[position] = bad
                with self.assertRaises(I.IdentityError):
                    I.validate_links(*args)

    def test_wrong_and_incomplete_members_rejected(self):
        for position, cls in enumerate((I.User, I.DigitalIdentity, I.IdentityLink)):
            for bad in (None, "synthetic-invalid", object.__new__(cls)):
                args = [self.users, self.identities, self.links]
                args[position] = (bad,)
                with self.assertRaises(I.IdentityError):
                    I.validate_links(*args)

    def test_altered_members_are_revalidated(self):
        cases = (
            (0, I.User(u7(1)), "user_id"),
            (1, I.DigitalIdentity(u7(3), I.IdentityType.HUMAN, I.IdentityState.ACTIVE), "state"),
            (2, I.IdentityLink(u7(1), u7(3)), "identity_id"),
        )
        for position, value, field in cases:
            object.__setattr__(value, field, "synthetic-invalid")
            args = [self.users, self.identities, self.links]
            args[position] = (value,)
            with self.assertRaises(I.IdentityError):
                I.validate_links(*args)

    def test_validation_preserves_input_and_retains_no_registry(self):
        before_user_ints = tuple(u.user_id.int for u in self.users)
        before_identity = tuple(
            (i.identity_id.int, i.identity_type, i.state) for i in self.identities)
        before_link_ints = tuple(
            (l.user_id.int, l.identity_id.int) for l in self.links)
        self.assertIs(
            I.validate_links(self.users, self.identities, self.links), True)
        self.assertEqual(
            tuple(u.user_id.int for u in self.users), before_user_ints)
        self.assertEqual(
            tuple((i.identity_id.int, i.identity_type, i.state)
                  for i in self.identities),
            before_identity)
        self.assertEqual(
            tuple((l.user_id.int, l.identity_id.int) for l in self.links),
            before_link_ints)
        with self.assertRaises(I.IdentityError):
            I.validate_links((), (), self.links)
        self.assertIs(
            I.validate_links(self.users, self.identities, self.links), True)

    def test_hostile_members_rejected_without_methods(self):
        calls = []
        class Evil:
            def __repr__(self):
                calls.append("repr")
                raise AssertionError("repr")
            def __str__(self):
                calls.append("str")
                raise AssertionError("str")
            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("eq")
            def __hash__(self):
                calls.append("hash")
                raise AssertionError("hash")
        for position in range(3):
            args = [self.users, self.identities, self.links]
            args[position] = (Evil(),)
            with self.assertRaises(I.IdentityError):
                I.validate_links(*args)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
