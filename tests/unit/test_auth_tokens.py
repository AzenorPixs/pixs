"""Justificatifs opaques : format canonique, séparation des usages et refus fermés."""
import base64
import hmac
import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch

from pixs.auth.tokens import (
    AuthTokenError, TokenKind, OpaqueToken, parse_token, new_token, token_fingerprint,
)

PUBLIC_ZERO = "A" * 43
ACCESS_ZERO_DIGEST = "e2dbe2ef0f889810762ff86e088499f43f447976ff4af476a5d3acc67bcd4660"


class AuthTokenTests(unittest.TestCase):
    def test_public_serialization_vector_v1(self):
        actual = token_fingerprint(parse_token(PUBLIC_ZERO), TokenKind.ACCESS)
        self.assertTrue(hmac.compare_digest(actual, ACCESS_ZERO_DIGEST))

    def test_usages_have_distinct_fingerprints(self):
        token = parse_token(PUBLIC_ZERO)
        values = {token_fingerprint(token, kind) for kind in TokenKind}
        self.assertEqual(len(values), 3)

    def test_new_token_has_256_encoded_bits(self):
        token = new_token()
        self.assertEqual(len(token.value), 43)
        self.assertEqual(len(base64.urlsafe_b64decode(token.value + "=")), 32)
        self.assertTrue(hmac.compare_digest(parse_token(token.value).value, token.value))

    def test_noncanonical_or_foreign_values_are_refused(self):
        invalids = (None, True, b"A" * 43, "", "A" * 42, "A" * 44,
                    "A" * 42 + "B", PUBLIC_ZERO + "=", PUBLIC_ZERO + "\n",
                    "é" * 43, "Bearer " + PUBLIC_ZERO)
        for invalid in invalids:
            with self.assertRaises(AuthTokenError) as caught:
                parse_token(invalid)
            self.assertEqual(str(caught.exception), "Justificatif opaque Auth invalide.")

    def test_foreign_equality_or_conversion_is_not_used(self):
        class Hostile:
            def __eq__(self, other):
                raise AssertionError("Comparaison étrangère.")
            def __str__(self):
                raise AssertionError("Conversion étrangère.")
        with self.assertRaises(AuthTokenError):
            parse_token(Hostile())
        with self.assertRaises(AuthTokenError):
            token_fingerprint(parse_token(PUBLIC_ZERO), Hostile())

    def test_incomplete_or_mutated_token_is_refused(self):
        with self.assertRaises(AuthTokenError):
            token_fingerprint(object.__new__(OpaqueToken), TokenKind.ACCESS)
        token = parse_token(PUBLIC_ZERO)
        object.__setattr__(token, "value", "invalid")
        with self.assertRaises(AuthTokenError):
            token_fingerprint(token, TokenKind.ACCESS)

    def test_plain_strings_are_not_accepted_as_opaque_objects(self):
        with self.assertRaises(AuthTokenError):
            token_fingerprint(PUBLIC_ZERO, TokenKind.ACCESS)
        with self.assertRaises(AuthTokenError):
            token_fingerprint(parse_token(PUBLIC_ZERO), "ACCESS")

    def test_representation_does_not_include_the_value(self):
        token = new_token()
        self.assertFalse(token.value in repr(token))
        self.assertFalse(token.value in str(token))

    def test_object_is_immutable(self):
        token = parse_token(PUBLIC_ZERO)
        with self.assertRaises(FrozenInstanceError):
            token.value = PUBLIC_ZERO

    def test_entropy_failure_has_no_fallback(self):
        with patch("pixs.auth.tokens.secrets.token_bytes", side_effect=OSError("entropy indisponible")):
            with self.assertRaises(OSError):
                new_token()

    def test_short_entropy_result_is_not_accepted(self):
        with patch("pixs.auth.tokens.secrets.token_bytes", return_value=b"public-fixture!!"):
            with self.assertRaises(AuthTokenError):
                new_token()


if __name__ == "__main__":
    unittest.main()
