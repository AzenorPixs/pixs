"""Adhesion du vocabulaire DataRetentionState aux sources canoniques."""

import unittest

import pixs.kernel.data_retention_states as retention_module
from pixs.kernel.data_retention_states import DataRetentionState

CANONICAL_RETENTION_STATES = (
    ("RETAINED", "RETAINED"),
    ("LEGAL_HOLD", "LEGAL_HOLD"),
    ("ELIGIBLE_FOR_PURGE", "ELIGIBLE_FOR_PURGE"),
)


class TestDataRetentionStatesVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self) -> None:
        # Source : data-lifecycle « Dimensions et états distincts » ;
        # scénario canonique « Vocabulaire commun de rétention fermé ».
        observed = tuple(
            (name, member.value)
            for name, member in DataRetentionState.__members__.items()
        )
        self.assertEqual(observed, CANONICAL_RETENTION_STATES)

    def test_module_exports_only_the_vocabulary(self) -> None:
        self.assertEqual(retention_module.__all__, ["DataRetentionState"])
        self.assertIs(retention_module.DataRetentionState, DataRetentionState)


if __name__ == "__main__":
    unittest.main()
