"""Vocabulaire AuthenticationAssurance et FederationTrust : fermeture et profil sans effet."""

import operator
import unittest
from enum import Enum

from pixs.core.authz.policy import AuthenticationAssurance, FederationTrust, IdentityAssurance


class ForeignAssurance(Enum):
    """Enum étranger portant des valeurs identiques pour vérification du refus sans défaut."""

    SINGLE_FACTOR = "SINGLE_FACTOR"
    UNTRUSTED = "UNTRUSTED"


class TestAuthenticationFederationVocabulary(unittest.TestCase):
    """Conformité des vocabulaires existants, sans ordre ni défaut."""

    def test_closed_member_set(self):
        self.assertEqual(
            set(AuthenticationAssurance.__members__),
            {"SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"},
        )
        self.assertEqual(len(AuthenticationAssurance.__members__), 3)
        self.assertEqual(
            {member.value for member in AuthenticationAssurance},
            {"SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"},
        )
        self.assertEqual(
            set(FederationTrust.__members__),
            {"UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"},
        )
        self.assertEqual(len(FederationTrust.__members__), 3)
        self.assertEqual(
            {member.value for member in FederationTrust},
            {"UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"},
        )
        for member in list(AuthenticationAssurance) + list(FederationTrust):
            self.assertIs(type(member.value), str)
            self.assertEqual(member.name, member.value)

    def test_name_value_roundtrip(self):
        for name in ("SINGLE_FACTOR", "MULTI_FACTOR", "PHISHING_RESISTANT"):
            from_value = AuthenticationAssurance(name)
            from_name = AuthenticationAssurance[name]
            self.assertIs(from_value, from_name)
            self.assertEqual(from_value.value, name)
            self.assertEqual(from_value.name, name)
        for name in ("UNTRUSTED", "TRUSTED", "STRONGLY_BOUND"):
            from_value = FederationTrust(name)
            from_name = FederationTrust[name]
            self.assertIs(from_value, from_name)
            self.assertEqual(from_value.value, name)
            self.assertEqual(from_value.name, name)

    def test_foreign_values_rejected_without_default(self):
        bad_auth_values = (
            "FOREIGN",
            "",
            "single_factor",
            "Single_Factor",
            " SINGLE_FACTOR",
            "SINGLE_FACTOR ",
            None,
            0,
            123,
            b"SINGLE_FACTOR",
        )
        for bad_value in bad_auth_values:
            with self.subTest(enum="AuthenticationAssurance", value=bad_value):
                with self.assertRaises(ValueError):
                    AuthenticationAssurance(bad_value)
        bad_federation_values = (
            "FOREIGN",
            "",
            "untrusted",
            "Untrusted",
            " UNTRUSTED",
            "UNTRUSTED ",
            None,
            0,
            123,
            b"UNTRUSTED",
        )
        for bad_value in bad_federation_values:
            with self.subTest(enum="FederationTrust", value=bad_value):
                with self.assertRaises(ValueError):
                    FederationTrust(bad_value)
        for foreign_member in (
            IdentityAssurance.CLAIMED,
            IdentityAssurance.VERIFIED,
            FederationTrust.UNTRUSTED,
            ForeignAssurance.SINGLE_FACTOR,
            ForeignAssurance.UNTRUSTED,
        ):
            with self.subTest(enum="AuthenticationAssurance", value=foreign_member):
                with self.assertRaises(ValueError):
                    AuthenticationAssurance(foreign_member)
        for foreign_member in (
            IdentityAssurance.CLAIMED,
            AuthenticationAssurance.SINGLE_FACTOR,
            ForeignAssurance.SINGLE_FACTOR,
            ForeignAssurance.UNTRUSTED,
        ):
            with self.subTest(enum="FederationTrust", value=foreign_member):
                with self.assertRaises(ValueError):
                    FederationTrust(foreign_member)

    def test_constructor_without_argument_fails(self):
        with self.assertRaises(TypeError):
            AuthenticationAssurance()
        with self.assertRaises(TypeError):
            FederationTrust()

    def test_members_not_orderable(self):
        low_auth = AuthenticationAssurance.SINGLE_FACTOR
        high_auth = AuthenticationAssurance.MULTI_FACTOR
        for operation in (operator.lt, operator.le, operator.gt, operator.ge):
            with self.subTest(enum="AuthenticationAssurance", operation=operation.__name__):
                with self.assertRaises(TypeError):
                    operation(low_auth, high_auth)
        low_federation = FederationTrust.UNTRUSTED
        high_federation = FederationTrust.TRUSTED
        for operation in (operator.lt, operator.le, operator.gt, operator.ge):
            with self.subTest(enum="FederationTrust", operation=operation.__name__):
                with self.assertRaises(TypeError):
                    operation(low_federation, high_federation)

    def test_separate_dimensions(self):
        authentication_set = set(AuthenticationAssurance)
        federation_set = set(FederationTrust)
        identity_set = set(IdentityAssurance)
        self.assertEqual(len(authentication_set), 3)
        self.assertEqual(len(federation_set), 3)
        for member in authentication_set:
            for outsider in list(federation_set) + list(identity_set):
                self.assertIsNot(member, outsider)
                self.assertNotEqual(member, outsider)
        for member in federation_set:
            for outsider in list(authentication_set) + list(identity_set):
                self.assertIsNot(member, outsider)
                self.assertNotEqual(member, outsider)


if __name__ == "__main__":
    unittest.main()
