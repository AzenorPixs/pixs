"""Vocabulaire IdentityAssurance : fermeture et profil sans effet."""

import operator
import unittest
from enum import Enum

from pixs.core.authz.policy import AuthenticationAssurance, FederationTrust, IdentityAssurance


class ForeignAssurance(Enum):
    """Enum étranger pour vérification du refus sans défaut."""

    CLAIMED = "CLAIMED"


class TestIdentityAssuranceVocabulary(unittest.TestCase):
    """Conformité du vocabulaire existant, sans ordre ni défaut."""

    def test_closed_member_set(self):
        self.assertEqual(set(IdentityAssurance.__members__), {"CLAIMED", "VERIFIED", "PROOFED"})
        self.assertEqual(len(IdentityAssurance.__members__), 3)
        self.assertEqual({member.value for member in IdentityAssurance}, {"CLAIMED", "VERIFIED", "PROOFED"})
        for member in IdentityAssurance:
            self.assertIs(type(member.value), str)
            self.assertEqual(member.name, member.value)

    def test_name_value_roundtrip(self):
        for name in ("CLAIMED", "VERIFIED", "PROOFED"):
            from_value = IdentityAssurance(name)
            from_name = IdentityAssurance[name]
            self.assertIs(from_value, from_name)
            self.assertEqual(from_value.value, name)
            self.assertEqual(from_value.name, name)

    def test_foreign_values_rejected_without_default(self):
        bad_values = ("FOREIGN", "", "claimed", "verified", "proofed", "Claimed", " CLAIMED", None, 0, 123, b"CLAIMED")
        for bad_value in bad_values:
            with self.subTest(value=bad_value):
                with self.assertRaises(ValueError):
                    IdentityAssurance(bad_value)
        for foreign_member in (AuthenticationAssurance.SINGLE_FACTOR, FederationTrust.UNTRUSTED, ForeignAssurance.CLAIMED):
            with self.subTest(value=foreign_member):
                with self.assertRaises(ValueError):
                    IdentityAssurance(foreign_member)

    def test_constructor_without_argument_fails(self):
        with self.assertRaises(TypeError):
            IdentityAssurance()

    def test_members_not_orderable(self):
        low = IdentityAssurance.CLAIMED
        high = IdentityAssurance.VERIFIED
        for operation in (operator.lt, operator.le, operator.gt, operator.ge):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(TypeError):
                    operation(low, high)

    def test_separate_dimensions(self):
        identity_set = set(IdentityAssurance)
        self.assertEqual(len(identity_set), 3)
        others = list(AuthenticationAssurance) + list(FederationTrust)
        for member in identity_set:
            for outsider in others:
                self.assertIsNot(member, outsider)
                self.assertNotEqual(member, outsider)


if __name__ == "__main__":
    unittest.main()
