"""Contrat canonique des phases de job Bulk B08."""

import unittest
from enum import Enum

from pixs.kernel import bulk_job_phase as vocabulary

# DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend.


class TestBulkJobPhase(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("STAGE", "STAGE"),
            ("VALIDATE", "VALIDATE"),
            ("APPLY", "APPLY"),
            ("EXPORT", "EXPORT"),
        )
        phase = vocabulary.BulkJobPhase
        self.assertEqual(
            tuple((name, member.value) for name, member in phase.__members__.items()),
            expected,
        )
        self.assertEqual(len(phase), 4)
        self.assertTrue(issubclass(phase, Enum))
        self.assertFalse(issubclass(phase, str))
        self.assertEqual(vocabulary.__all__, ["BulkJobPhase"])
        self.assertIs(phase("STAGE"), phase.STAGE)
        self.assertEqual(phase.EXPORT.value, "EXPORT")

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in ("stage", "Stage", "STAGE ", " STAGE", "", None, "STAGED"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.BulkJobPhase(value)

if __name__ == "__main__":
    unittest.main()
