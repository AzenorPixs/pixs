"""Contrat fermé du vocabulaire canonique de persistance."""

import unittest

from pixs.kernel import data_persistence as vocabulary


class TestDataPersistenceVocabulary(unittest.TestCase):
    def test_canonical_persistence_dimension_is_closed(self):
        expected = (
            ("ACTIVE", "ACTIVE"),
            ("ARCHIVED", "ARCHIVED"),
            ("SOFT_DELETED", "SOFT_DELETED"),
            ("PURGE_PENDING", "PURGE_PENDING"),
        )
        self.assertEqual(
            tuple(
                (name, member.value)
                for name, member in vocabulary.PersistenceState.__members__.items()
            ),
            expected,
        )
        self.assertEqual(vocabulary.__all__, ["PersistenceState"])
        self.assertIs(
            vocabulary.PersistenceState("SOFT_DELETED"),
            vocabulary.PersistenceState.SOFT_DELETED,
        )
        for undeclared in ("PURGED", "active", "RETAINED"):
            with self.subTest(value=undeclared):
                with self.assertRaises(ValueError):
                    vocabulary.PersistenceState(undeclared)


if __name__ == "__main__":
    unittest.main()
