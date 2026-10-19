"""Contrat public du vocabulaire BulkExportConsistencyKind."""

import unittest

import pixs.backend.bulk_export_consistency_kind as vocabulary


class BulkExportConsistencyKindTests(unittest.TestCase):
    def test_public_contract(self):
        kind = vocabulary.BulkExportConsistencyKind
        self.assertEqual(vocabulary.__all__, ["BulkExportConsistencyKind"])
        self.assertEqual(list(kind.__members__), ["SNAPSHOT", "WATERMARK"])
        self.assertEqual([member.value for member in kind], ["SNAPSHOT", "WATERMARK"])
        self.assertFalse(issubclass(kind, str))
        for member in kind:
            self.assertNotEqual(member, member.value)
            self.assertIs(kind(member.value), member)

    def test_lookup_does_not_normalize(self):
        for value in ("snapshot", "watermark", "SNAPSHOT ", " SNAPSHOT", "", None, 0):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.BulkExportConsistencyKind(value)


if __name__ == "__main__":
    unittest.main()
