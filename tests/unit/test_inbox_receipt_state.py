"""Contrat canonique de l'état de réception inbox InboxReceiptV1."""

import unittest
from datetime import datetime, timezone
from enum import Enum

from pixs.backend import inbox_receipt_state as vocabulary
from pixs.backend.bulk_inbox_receipt_values import (
    validate_bulk_inbox_receipt_values,
)

CONSUMED_AT = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
SHA_OK = "0f" * 32

# DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend.


def _valid(**overrides):
    base = {
        "consumer_reference": "consumer-test",
        "event_id": "event-test",
        "event_version": "1.2.3",
        "content_sha256": SHA_OK,
        "state": "CONSUMED",
        "consumed_at": CONSUMED_AT,
        "correlation_id": "corr-test",
        "causation_id": None,
    }
    base.update(overrides)
    return base


class TestInboxReceiptState(unittest.TestCase):
    def test_canonical_vocabulary_and_public_contract(self):
        expected = (("CONSUMED", "CONSUMED"),)
        state = vocabulary.InboxReceiptState
        self.assertEqual(
            tuple((name, member.value) for name, member in state.__members__.items()),
            expected,
        )
        self.assertEqual(len(state), 1)
        self.assertTrue(issubclass(state, Enum))
        self.assertFalse(issubclass(state, str))
        self.assertEqual(vocabulary.__all__, ["InboxReceiptState"])
        self.assertIs(state("CONSUMED"), state.CONSUMED)
        self.assertEqual(state.CONSUMED.value, "CONSUMED")

    def test_undeclared_values_are_rejected_without_normalization(self):
        for value in ("pending", "consumed", "PENDING", "CONSUMED ", " CONSUMED", "", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.InboxReceiptState(value)

    def test_textual_consumed_admitted_by_existing_validator(self):
        self.assertEqual(validate_bulk_inbox_receipt_values(_valid(state="CONSUMED")), [])

    def test_direct_enum_member_refused_without_validator_change(self):
        before = validate_bulk_inbox_receipt_values(_valid(state="CONSUMED"))
        self.assertEqual(before, [])
        refused = validate_bulk_inbox_receipt_values(
            _valid(state=vocabulary.InboxReceiptState.CONSUMED)
        )
        self.assertTrue(refused)
        after = validate_bulk_inbox_receipt_values(_valid(state="CONSUMED"))
        self.assertEqual(after, [])


if __name__ == "__main__":
    unittest.main()
