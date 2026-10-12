"""Adhesion du vocabulaire DataSubjectOperation aux sources canoniques."""

import unittest

import pixs.kernel.data_subject_operations as operations_module
from pixs.kernel.data_subject_operations import DataSubjectOperation

CANONICAL_OPERATIONS = (
    ("ACCESS", "ACCESS"),
    ("EXPORT", "EXPORT"),
    ("RECTIFY", "RECTIFY"),
    ("ERASE", "ERASE"),
    ("RESTRICT", "RESTRICT"),
)


class TestDataSubjectOperationsVocabulary(unittest.TestCase):
    def test_names_values_and_order_follow_the_canonical_source(self) -> None:
        # Source : data-governance « Demandes relatives aux données tracées » ;
        # identifiants anglais de TECHNICAL.md §14.6.
        observed = tuple(
            (name, member.value)
            for name, member in DataSubjectOperation.__members__.items()
        )
        self.assertEqual(observed, CANONICAL_OPERATIONS)

    def test_module_exports_only_the_vocabulary(self) -> None:
        self.assertEqual(operations_module.__all__, ["DataSubjectOperation"])
        self.assertIs(operations_module.DataSubjectOperation, DataSubjectOperation)


if __name__ == "__main__":
    unittest.main()
