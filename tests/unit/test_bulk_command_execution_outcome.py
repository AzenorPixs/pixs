"""Contrat canonique des outcomes de commande Bulk B07."""

import unittest
from enum import Enum

import pixs.backend.bulk_command_execution_outcome as vocabulary
import pixs.backend.bulk_runtime_contracts as runtime
from unit.test_bulk_execution_values import _valid_policy

# DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend.


_CODES = frozenset({"INVALID_FIELD", "REJECTED"})
_FIELDS = frozenset({"name", "count"})


def _execution(outcome="APPLIED"):
    return {
        "outcome": outcome, "result_reference": None,
        "diagnostics": (), "event_references": (),
    }


class TestBulkCommandExecutionOutcome(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (
            ("APPLIED", "APPLIED"),
            ("REPLAYED", "REPLAYED"),
            ("REJECTED", "REJECTED"),
        )
        outcome = vocabulary.BulkCommandExecutionOutcome
        self.assertEqual(
            tuple((name, member.value) for name, member in outcome.__members__.items()),
            expected,
        )
        self.assertEqual(len(outcome), 3)
        self.assertTrue(issubclass(outcome, Enum))
        self.assertFalse(issubclass(outcome, str))
        self.assertEqual(vocabulary.__all__, ["BulkCommandExecutionOutcome"])
        self.assertIs(outcome("APPLIED"), outcome.APPLIED)
        self.assertEqual(outcome.REJECTED.value, "REJECTED")

    def test_undeclared_values_rejected_without_normalization(self):
        for value in ("applied", "APPLIED ", " APPLIED", "", None, "UNKNOWN", "REPLAYED ", 0):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.BulkCommandExecutionOutcome(value)

    def test_str_values_not_replaced_by_enum_in_validator(self):
        policy = _valid_policy()
        for name in ("APPLIED", "REPLAYED", "REJECTED"):
            result = runtime.validate_command_execution_values(
                _execution(outcome=name), policy=policy,
                declared_codes=_CODES, declared_fields=_FIELDS,
            )
            self.assertEqual(result, [])
        for member in vocabulary.BulkCommandExecutionOutcome:
            result = runtime.validate_command_execution_values(
                _execution(outcome=member), policy=policy,
                declared_codes=_CODES, declared_fields=_FIELDS,
            )
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
