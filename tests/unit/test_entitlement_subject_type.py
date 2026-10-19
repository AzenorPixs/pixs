"""Contrat public du vocabulaire fermé des sujets d'entitlement."""

import unittest
from enum import Enum

from pixs.kernel import entitlement_subject_type as vocabulary


class TestEntitlementSubjectType(unittest.TestCase):
    def test_names_and_order(self):
        self.assertEqual(
            tuple(vocabulary.EntitlementSubjectType.__members__),
            ("INSTALLATION", "PLATFORM", "TENANT", "SCOPE"),
        )

    def test_exact_values(self):
        self.assertEqual(
            tuple(member.value for member in vocabulary.EntitlementSubjectType),
            ("INSTALLATION", "PLATFORM", "TENANT", "SCOPE"),
        )

    def test_public_export(self):
        self.assertEqual(vocabulary.__all__, ["EntitlementSubjectType"])

    def test_standard_enum_without_string_mixin(self):
        self.assertTrue(issubclass(vocabulary.EntitlementSubjectType, Enum))
        self.assertFalse(issubclass(vocabulary.EntitlementSubjectType, str))

    def test_construction_returns_canonical_singletons(self):
        for member in vocabulary.EntitlementSubjectType:
            with self.subTest(member=member.name):
                self.assertIs(vocabulary.EntitlementSubjectType(member.value), member)
                self.assertIs(vocabulary.EntitlementSubjectType[member.name], member)

    def test_only_four_distinct_members_without_alias(self):
        kind = vocabulary.EntitlementSubjectType
        self.assertEqual(len(kind), 4)
        self.assertEqual(len(kind.__members__), len(kind))
        self.assertEqual(len(set(kind)), 4)

    def test_quota_only_scopes_and_user_are_rejected(self):
        for value in ("IDENTITY", "IP", "OPERATION", "USER", "UNKNOWN"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.EntitlementSubjectType(value)

    def test_no_case_or_space_normalization(self):
        for value in ("installation", "Installation", "tenant", " TENANT", "TENANT ", "\tSCOPE", "SCOPE\n", ""):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.EntitlementSubjectType(value)

    def test_non_string_values_are_rejected(self):
        for value in (None, 0, 1, False, True, b"TENANT", 1.0):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.EntitlementSubjectType(value)

    def test_members_do_not_compare_equal_to_strings(self):
        for member in vocabulary.EntitlementSubjectType:
            with self.subTest(member=member.name):
                self.assertNotEqual(member, member.value)
                self.assertIs(type(member.value), str)

    def test_member_values_are_read_only(self):
        with self.assertRaises(AttributeError):
            vocabulary.EntitlementSubjectType.TENANT.value = "INSTALLATION"

    def test_unknown_name_is_rejected(self):
        with self.assertRaises(KeyError):
            vocabulary.EntitlementSubjectType["IDENTITY"]


if __name__ == "__main__":
    unittest.main()
