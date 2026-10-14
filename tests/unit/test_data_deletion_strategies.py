"""Adhesion du vocabulaire DataDeletionStrategy aux sources canoniques."""

import unittest

import pixs.kernel.data_deletion_strategies as deletion_module
from pixs.kernel.data_deletion_strategies import DataDeletionStrategy

CANONICAL_DELETION_STRATEGIES = (
    ("SOFT_DELETE", "SOFT_DELETE"),
    ("PHYSICAL_DELETE", "PHYSICAL_DELETE"),
    ("ARCHIVE", "ARCHIVE"),
    ("IMMUTABLE", "IMMUTABLE"),
)


class TestDataDeletionStrategiesVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self) -> None:
        # Source : data-lifecycle « Vocabulaire commun des stratégies de suppression » ;
        # scénario canonique « Vocabulaire déclaratif distinct de la persistance ».
        observed = tuple(
            (name, member.value)
            for name, member in DataDeletionStrategy.__members__.items()
        )
        self.assertEqual(observed, CANONICAL_DELETION_STRATEGIES)

    def test_module_exports_only_the_vocabulary(self) -> None:
        self.assertEqual(deletion_module.__all__, ["DataDeletionStrategy"])
        self.assertIs(deletion_module.DataDeletionStrategy, DataDeletionStrategy)


if __name__ == "__main__":
    unittest.main()
