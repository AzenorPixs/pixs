"""Contrat canonique des modes de démarrage de Pixs."""

import unittest
from enum import Enum

from pixs.backend import startup_mode as vocabulary


class TestStartupMode(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("INSTALLER", "INSTALLER"),
            ("FIRST_CONFIGURATION", "FIRST_CONFIGURATION"),
            ("NORMAL", "NORMAL"),
            ("MAINTENANCE", "MAINTENANCE"),
        )
        state = vocabulary.StartupMode
        self.assertEqual(
            tuple((name, member.value) for name, member in state.__members__.items()),
            expected,
        )
        self.assertEqual(len(state), 4)
        self.assertTrue(issubclass(state, Enum))
        self.assertFalse(issubclass(state, str))
        self.assertEqual(vocabulary.__all__, ["StartupMode"])
        self.assertIs(state("NORMAL"), state.NORMAL)

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in ("installer", "NORMAL ", " NORMAL", "PURGED", "", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.StartupMode(value)


if __name__ == "__main__":
    unittest.main()
