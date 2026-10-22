"""UUIDv7 et acteur canonique : format explicite, absence d'alias ou de repli."""
import unittest
import uuid
from unittest.mock import patch

from pixs.auth.identifiers import (
    AuthIdentifierError, require_uuid7, new_uuid7,
    identity_reference, parse_identity_reference,
)
from pixs.auth.apps import PixsAuthConfig
import pixs.auth as auth_module

PUBLIC_UUID = uuid.UUID("018bcfe5-6800-7001-8000-000000000002")


class AuthIdentifierTests(unittest.TestCase):
    def test_public_uuid7_layout_vector(self):
        with patch("pixs.auth.identifiers.time.time_ns", return_value=1700000000000000000), \
             patch("pixs.auth.identifiers.secrets.randbits", side_effect=(1, 2)):
            self.assertEqual(new_uuid7(), PUBLIC_UUID)

    def test_generated_identifier_is_not_a_credential(self):
        current = new_uuid7()
        self.assertIs(require_uuid7(current), current)
        self.assertEqual(current.version, 7)
        self.assertEqual(current.variant, uuid.RFC_4122)

    def test_canonical_reference_roundtrip(self):
        ref = identity_reference(PUBLIC_UUID)
        self.assertEqual(ref, "pixs.core.identity:018bcfe5-6800-7001-8000-000000000002")
        self.assertEqual(parse_identity_reference(ref), PUBLIC_UUID)

    def test_raw_or_other_namespace_is_not_an_actor_alias(self):
        for invalid in (str(PUBLIC_UUID), "pixs.auth.identity:" + str(PUBLIC_UUID),
                        "pixs.core.identity:{" + str(PUBLIC_UUID) + "}",
                        "pixs.core.identity:urn:uuid:" + str(PUBLIC_UUID)):
            with self.assertRaises(AuthIdentifierError):
                parse_identity_reference(invalid)

    def test_uppercase_uuid_spelling_is_not_normalized_implicitly(self):
        with self.assertRaises(AuthIdentifierError):
            parse_identity_reference("pixs.core.identity:" + str(PUBLIC_UUID).upper())

    def test_other_uuid_version_or_variant_is_rejected(self):
        for invalid in (uuid.uuid4(), uuid.UUID(int=(7 << 76)), str(PUBLIC_UUID), True):
            with self.assertRaises(AuthIdentifierError):
                require_uuid7(invalid)

    def test_incomplete_uuid_is_rejected(self):
        with self.assertRaises(AuthIdentifierError):
            require_uuid7(object.__new__(uuid.UUID))

    def test_foreign_conversions_are_not_invoked(self):
        class Hostile:
            def startswith(self, prefix):
                raise AssertionError("Méthode étrangère.")
            def __str__(self):
                raise AssertionError("Conversion étrangère.")
        with self.assertRaises(AuthIdentifierError):
            parse_identity_reference(Hostile())
        with self.assertRaises(AuthIdentifierError):
            identity_reference(Hostile())

    def test_before_epoch_and_overflow_have_no_uuid4_fallback(self):
        for timestamp in (-1000000, (2**48) * 1000000):
            with patch("pixs.auth.identifiers.time.time_ns", return_value=timestamp), \
                 patch("pixs.auth.identifiers.secrets.randbits") as entropy:
                with self.assertRaises(AuthIdentifierError):
                    new_uuid7()
                self.assertEqual(entropy.call_count, 0)

    def test_entropy_error_is_propagated(self):
        with patch("pixs.auth.identifiers.secrets.randbits", side_effect=OSError("entropy indisponible")):
            with self.assertRaises(OSError):
                new_uuid7()

    def test_malformed_entropy_is_not_accepted(self):
        with patch("pixs.auth.identifiers.secrets.randbits", side_effect=(False, 1)):
            with self.assertRaises(AuthIdentifierError):
                new_uuid7()

    def test_package_and_appconfig_declare_without_activating(self):
        self.assertEqual(auth_module.MODULE_VERSION, "0.1.0")
        self.assertEqual(auth_module.CONTRACT_VERSION, "1.0.0")
        self.assertFalse(PixsAuthConfig.default)
        self.assertEqual(PixsAuthConfig.name, "pixs.auth")
        self.assertEqual(PixsAuthConfig.label, "pixs_auth")


if __name__ == "__main__":
    unittest.main()
