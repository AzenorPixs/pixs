"""Contrat canonique des états de décision d'architecture."""

import unittest
from enum import Enum

from pixs.kernel import architecture_decision_state as vocabulary


class TestArchitectureDecisionState(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("PROPOSED", "PROPOSED"),
            ("ACCEPTED", "ACCEPTED"),
            ("SUPERSEDED", "SUPERSEDED"),
            ("REJECTED", "REJECTED"),
        )
        state = vocabulary.ArchitectureDecisionState
        self.assertEqual(
            tuple((name, member.value) for name, member in state.__members__.items()),
            expected,
        )
        self.assertEqual(len(state), 4)
        self.assertTrue(issubclass(state, Enum))
        self.assertFalse(issubclass(state, str))
        self.assertEqual(vocabulary.__all__, ["ArchitectureDecisionState"])
        self.assertIs(state("ACCEPTED"), state.ACCEPTED)

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in ("proposed", "ACCEPTED ", "PURGED", "", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.ArchitectureDecisionState(value)


if __name__ == "__main__":
    unittest.main()
