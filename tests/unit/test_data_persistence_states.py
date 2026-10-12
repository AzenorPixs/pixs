"""Adhesion du vocabulaire DataPersistenceState aux sources canoniques."""

import unittest

import pixs.kernel.data_persistence_states as persistence_module
from pixs.kernel.data_persistence_states import DataPersistenceState

CANONICAL_PERSISTENCE_STATES = (
    ("ACTIVE", "ACTIVE"),
    ("ARCHIVED", "ARCHIVED"),
    ("SOFT_DELETED", "SOFT_DELETED"),
    ("PURGE_PENDING", "PURGE_PENDING"),
)


class TestDataPersistenceStatesVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self) -> None:
        # Source : data-lifecycle « Dimensions et états distincts » ;
        # corroboré par PROJECT.md §2.15 (PURGED exclu de ce vocabulaire).
        observed = tuple(
            (name, member.value)
            for name, member in DataPersistenceState.__members__.items()
        )
        self.assertEqual(observed, CANONICAL_PERSISTENCE_STATES)

    def test_module_exports_only_the_vocabulary(self) -> None:
        self.assertEqual(persistence_module.__all__, ["DataPersistenceState"])
        self.assertIs(persistence_module.DataPersistenceState, DataPersistenceState)


if __name__ == "__main__":
    unittest.main()
