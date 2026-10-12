"""Adhésion aux dimensions canoniques de data-governance, sans taxonomie ajoutée."""

import unittest

from pixs.kernel import data_governance
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel


class TestDataGovernanceVocabulary(unittest.TestCase):
    def test_confidentiality_matches_canonical_dimension(self):
        # Source : data-governance, « Classification restrictive par défaut ».
        expected = (
            ("PUBLIC", "PUBLIC"),
            ("INTERNAL", "INTERNAL"),
            ("CONFIDENTIAL", "CONFIDENTIAL"),
            ("RESTRICTED", "RESTRICTED"),
        )
        actual = tuple(
            (name, member.value) for name, member in ConfidentialityLevel.__members__.items()
        )
        self.assertEqual(actual, expected)

    def test_personal_data_matches_canonical_dimension(self):
        # NONE est une classification déclarée, distincte d'une absence.
        expected = (
            ("NONE", "NONE"),
            ("PERSONAL", "PERSONAL"),
            ("SENSITIVE_PERSONAL", "SENSITIVE_PERSONAL"),
        )
        actual = tuple(
            (name, member.value) for name, member in PersonalDataLevel.__members__.items()
        )
        self.assertEqual(actual, expected)

    def test_public_vocabulary_exports_are_bounded(self):
        self.assertEqual(
            data_governance.__all__, ["ConfidentialityLevel", "PersonalDataLevel"]
        )


if __name__ == "__main__":
    unittest.main()
