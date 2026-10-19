"""Contrat public du vocabulaire passif des actions d’autorité Bulk."""

import operator
import unittest
from enum import Enum

import pixs.backend.bulk_authority_action as vocabulary
from pixs.backend.bulk_authority_action import BulkAuthorityAction


class ForeignAction(Enum):
    ADMIT = "ADMIT"


class BulkAuthorityActionTests(unittest.TestCase):
    def test_closed_public_vocabulary(self):
        expected = ("ADMIT", "EXECUTE", "CANCEL", "READ_RESULT")
        self.assertEqual(vocabulary.__all__, ["BulkAuthorityAction"])
        self.assertEqual(tuple(BulkAuthorityAction.__members__), expected)
        self.assertEqual(tuple(item.value for item in BulkAuthorityAction), expected)
        self.assertEqual(len(set(BulkAuthorityAction)), 4)
        self.assertFalse(issubclass(BulkAuthorityAction, str))

    def test_explicit_roundtrip_preserves_members(self):
        for item in BulkAuthorityAction:
            with self.subTest(item=item.name):
                self.assertIs(type(item.value), str)
                self.assertEqual(item.name, item.value)
                self.assertIs(BulkAuthorityAction[item.name], item)
                self.assertIs(BulkAuthorityAction(item.value), item)
                self.assertNotEqual(item, item.value)

    def test_unknown_values_are_not_normalized_or_defaulted(self):
        for value in ("admit", "Admit", " ADMIT", "ADMIT ", "", "UNKNOWN", None, 0, b"ADMIT", ForeignAction.ADMIT):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    BulkAuthorityAction(value)
        with self.assertRaises(TypeError):
            BulkAuthorityAction()

    def test_members_have_no_ordinal_comparison(self):
        for comparison in (operator.lt, operator.le, operator.gt, operator.ge):
            with self.subTest(comparison=comparison.__name__):
                with self.assertRaises(TypeError):
                    comparison(BulkAuthorityAction.ADMIT, BulkAuthorityAction.EXECUTE)


if __name__ == "__main__":
    unittest.main()
