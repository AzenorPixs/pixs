"""Recette du wrapper Argon2id : profil réel et refus avant calcul."""
import hmac
import secrets
import unittest
from unittest.mock import patch

from pixs.auth.passwords import (
    AuthPasswordError, hash_password, verify_password,
    envelope_to_ldap, envelope_to_django,
)


class AuthPasswordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.password = secrets.token_urlsafe(24)
        cls.encoded = hash_password(cls.password)

    def test_password_is_verified(self):
        self.assertTrue(verify_password(self.password, self.encoded))

    def test_wrong_password_is_refused(self):
        self.assertFalse(verify_password(self.password + "!", self.encoded))

    def test_envelope_conversion_preserves_the_whole_argon2_payload(self):
        ldap = envelope_to_ldap(self.encoded)
        self.assertTrue(hmac.compare_digest(ldap[len("{ARGON2}"):], self.encoded[len("argon2"):]))
        restored = envelope_to_django(ldap)
        self.assertTrue(hmac.compare_digest(restored, self.encoded))
        self.assertTrue(verify_password(self.password, restored))

    def test_ldap_envelope_is_not_accepted_as_a_local_django_hash(self):
        with self.assertRaises(AuthPasswordError):
            verify_password(self.password, envelope_to_ldap(self.encoded))

    def test_incompatible_costs_are_refused_before_hasher_creation(self):
        for replacement in ("m=0,", "m=65536,", "m=2147483647,"):
            invalid = self.encoded.replace("m=102400,", replacement, 1)
            with patch("pixs.auth.passwords.Argon2PasswordHasher") as factory:
                with self.assertRaises(AuthPasswordError):
                    verify_password(self.password, invalid)
                self.assertEqual(factory.call_count, 0)

    def test_other_version_or_variant_is_refused(self):
        for invalid in (self.encoded.replace("$v=19$", "$v=16$", 1),
                        self.encoded.replace("$argon2id$", "$argon2i$", 1)):
            with self.assertRaises(AuthPasswordError):
                verify_password(self.password, invalid)

    def test_formats_are_bounded_and_errors_do_not_echo_the_hash(self):
        for invalid in (None, "", "argon2$" + "A" * 600, "argon2$é"):
            with self.assertRaises(AuthPasswordError) as caught:
                verify_password(self.password, invalid)
            self.assertEqual(str(caught.exception), "Justificatif Argon2id invalide.")

    def test_wrong_direction_is_refused(self):
        with self.assertRaises(AuthPasswordError):
            envelope_to_django(self.encoded)
        with self.assertRaises(AuthPasswordError):
            envelope_to_ldap(envelope_to_ldap(self.encoded))

    def test_foreign_inputs_are_rejected_before_method_calls(self):
        class Hostile:
            def startswith(self, prefix):
                raise AssertionError("Méthode étrangère appelée.")
            def __eq__(self, other):
                raise AssertionError("Comparaison étrangère appelée.")
        with self.assertRaises(AuthPasswordError):
            verify_password(Hostile(), self.encoded)
        with self.assertRaises(AuthPasswordError):
            verify_password(self.password, Hostile())

    def test_changed_django_costs_are_not_used(self):
        with patch("pixs.auth.passwords.Argon2PasswordHasher") as factory:
            factory.return_value.memory_cost = 1
            factory.return_value.time_cost = 2
            factory.return_value.parallelism = 8
            with self.assertRaises(AuthPasswordError):
                hash_password(self.password)
            self.assertEqual(factory.return_value.encode.call_count, 0)

    def test_unexpected_programming_error_is_not_hidden(self):
        with patch("pixs.auth.passwords.Argon2PasswordHasher") as factory:
            factory.return_value.memory_cost = 102400
            factory.return_value.time_cost = 2
            factory.return_value.parallelism = 8
            factory.return_value.encode.side_effect = RuntimeError("défaut synthétique")
            with self.assertRaises(RuntimeError):
                hash_password(self.password)


if __name__ == "__main__":
    unittest.main()
