"""Contrôle des deux vocabulaires de TECHNICAL §14.1."""

import unittest

from pixs.kernel import data_lifecycle_policy_vocabulary as vocabulary


class TestDataRetentionAndDeletionVocabulary(unittest.TestCase):
    def test_retention_matches_canonical_dimension(self):
        self.assertEqual(
            [(name, member.value) for name, member in vocabulary.RetentionState.__members__.items()],
            [("RETAINED", "RETAINED"), ("LEGAL_HOLD", "LEGAL_HOLD"),
             ("ELIGIBLE_FOR_PURGE", "ELIGIBLE_FOR_PURGE")],
        )
        self.assertIs(vocabulary.RetentionState("LEGAL_HOLD"), vocabulary.RetentionState.LEGAL_HOLD)
        for invalid in ("ACTIVE", "PURGED", "legal_hold"):
            with self.subTest(value=invalid):
                with self.assertRaises(ValueError):
                    vocabulary.RetentionState(invalid)

    def test_deletion_matches_canonical_strategy(self):
        self.assertEqual(
            [(name, member.value) for name, member in vocabulary.DeletionStrategy.__members__.items()],
            [("SOFT_DELETE", "SOFT_DELETE"), ("PHYSICAL_DELETE", "PHYSICAL_DELETE"),
             ("ARCHIVE", "ARCHIVE"), ("IMMUTABLE", "IMMUTABLE")],
        )
        self.assertIs(vocabulary.DeletionStrategy("SOFT_DELETE"), vocabulary.DeletionStrategy.SOFT_DELETE)
        for invalid in ("SOFT_DELETED", "RESTRICT", "soft_delete"):
            with self.subTest(value=invalid):
                with self.assertRaises(ValueError):
                    vocabulary.DeletionStrategy(invalid)

    def test_dimensions_and_exports_remain_distinct(self):
        self.assertEqual(vocabulary.__all__, ["RetentionState", "DeletionStrategy"])
        self.assertIsNot(vocabulary.RetentionState, vocabulary.DeletionStrategy)
        self.assertNotEqual(vocabulary.RetentionState.RETAINED, vocabulary.DeletionStrategy.IMMUTABLE)


if __name__ == "__main__":
    unittest.main()
