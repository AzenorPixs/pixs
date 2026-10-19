"""Contrat public du vocabulaire EventEnvelopeKind."""

import unittest

import pixs.backend.event_envelope_kind as vocabulary


class EventEnvelopeKindTests(unittest.TestCase):
    def test_public_contract(self):
        kind = vocabulary.EventEnvelopeKind
        self.assertEqual(vocabulary.__all__, ["EventEnvelopeKind"])
        self.assertEqual(
            list(kind.__members__),
            ["DOMAIN", "INTEGRATION"],
        )
        self.assertEqual(
            [member.value for member in kind],
            ["DOMAIN", "INTEGRATION"],
        )
        self.assertFalse(issubclass(kind, str))
        for member in kind:
            self.assertNotEqual(member, member.value)
            self.assertIs(kind(member.value), member)

    def test_lookup_does_not_normalize(self):
        for value in ("domain", "integration", " DOMAIN", "DOMAIN ", "", None, 0):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    vocabulary.EventEnvelopeKind(value)


if __name__ == "__main__":
    unittest.main()
