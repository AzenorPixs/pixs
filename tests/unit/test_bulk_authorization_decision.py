"""Contrat fermé des décisions d’autorité Bulk et compatibilité des chaînes.

PostgreSQL et frontend sans objet pour ce vocabulaire passif.
"""

import unittest
from enum import Enum

import pixs.backend.bulk_authorization_decision as vocabulary
from pixs.backend.bulk_runtime_contracts import validate_authority_assessment_values


class TestBulkAuthorizationDecision(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        decision = vocabulary.BulkAuthorizationDecision
        expected = ("ALLOW", "DENY", "UNAVAILABLE")
        self.assertEqual(tuple(decision.__members__), expected)
        self.assertEqual(tuple(member.value for member in decision), expected)
        self.assertEqual(len(decision), 3)
        self.assertTrue(issubclass(decision, Enum))
        self.assertFalse(issubclass(decision, str))
        self.assertEqual(vocabulary.__all__, ["BulkAuthorizationDecision"])
        for member in decision:
            self.assertIs(decision(member.value), member)
            self.assertIs(type(member.value), str)
            self.assertNotEqual(member, member.value)

    def test_undeclared_values_rejected_without_normalization(self):
        for value in ("allow", "DENY ", " UNAVAILABLE", "", None, 0, "UNKNOWN", "RESOLVED"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.BulkAuthorizationDecision(value)

    def test_existing_validator_keeps_exact_strings(self):
        context = {
            "subject_id": "actor-test", "tenant_id": "tenant-test",
            "perimeter_reference": "perimeter-test", "context_reference": "context-test",
        }
        for member in vocabulary.BulkAuthorizationDecision:
            with self.subTest(decision=member.name):
                resolved = context if member.name == "ALLOW" else None
                candidate = {"decision": member.value, "resolved_context": resolved}
                self.assertEqual(validate_authority_assessment_values(candidate), [])
                candidate["decision"] = member
                diagnostics = validate_authority_assessment_values(candidate)
                self.assertTrue(diagnostics)
                self.assertTrue(any(item.element.endswith(".decision") for item in diagnostics))
                self.assertTrue(any(item.constraint == "str exact attendu" for item in diagnostics))


if __name__ == "__main__":
    unittest.main()
