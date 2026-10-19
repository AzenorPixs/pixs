"""Contrat canonique des handlers de job Bulk B08."""

import unittest
from enum import Enum

from pixs.kernel import bulk_job_handler as vocabulary

# DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend.


class TestBulkJobHandler(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("STAGE", "pixs.bulk.stage"),
            ("VALIDATE", "pixs.bulk.validate"),
            ("APPLY", "pixs.bulk.apply"),
            ("EXPORT", "pixs.bulk.export"),
        )
        phase = vocabulary.BulkJobHandler
        self.assertEqual(
            tuple((name, member.value) for name, member in phase.__members__.items()),
            expected,
        )
        self.assertEqual(type(vocabulary.BULK_JOB_HANDLER_VERSION), str)
        self.assertEqual(vocabulary.BULK_JOB_HANDLER_VERSION, "1.0.0")
        self.assertEqual(len(phase), 4)
        self.assertTrue(issubclass(phase, Enum))
        self.assertFalse(issubclass(phase, str))
        self.assertEqual(vocabulary.__all__, ["BulkJobHandler", "BULK_JOB_HANDLER_VERSION"])
        self.assertIs(phase("pixs.bulk.stage"), phase.STAGE)
        self.assertEqual(phase.EXPORT.value, "pixs.bulk.export")

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in ("stage", "pixs.bulk.STAGE", "pixs.bulk.stage ", " pixs.bulk.stage", "", None, "pixs.bulk.staged"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.BulkJobHandler(value)

if __name__ == "__main__":
    unittest.main()
