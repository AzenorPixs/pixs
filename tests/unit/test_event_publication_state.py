"""Contrat canonique des états de publication d’événement B11."""

import unittest
from enum import Enum

from pixs.backend import event_publication_state as vocabulary


class TestEventPublicationState(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("PENDING", "PENDING"),
            ("PUBLISHED", "PUBLISHED"),
            ("RETRYING", "RETRYING"),
            ("FAILED", "FAILED"),
            ("DEAD_LETTER", "DEAD_LETTER"),
        )
        state = vocabulary.EventPublicationState
        self.assertEqual(
            tuple((name, member.value) for name, member in state.__members__.items()),
            expected,
        )
        self.assertEqual(len(state), 5)
        self.assertTrue(issubclass(state, Enum))
        self.assertFalse(issubclass(state, str))
        self.assertEqual(vocabulary.__all__, ["EventPublicationState"])
        for name, value in expected:
            self.assertIs(state(value), state[name])

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in ("pending", "PENDING ", " PENDING", "SENT", "", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.EventPublicationState(value)


if __name__ == "__main__":
    unittest.main()
