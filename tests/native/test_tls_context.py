"""Recette dédiée du contexte compilé E3, pas un handshake ou une PKI.

Exiger la construction native puis son répertoire d'artefacts dans sys.path.
Cette suite dédiée doit échouer si le module compilé sélectionné manque.
Aucun test positif ici ne qualifie le transport PZT ou les identités.
"""
from __future__ import annotations

import copy
import pickle
import threading
import unittest

from tls_context import TLS13Context, TLSConfigurationError


class TlsContextTest(unittest.TestCase):
    def test_explicit_suites_and_sides_match_effective_openssl_configuration(self):
        for suite in ("TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"):
            for side in ("client", "server"):
                with self.subTest(suite=suite, side=side), TLS13Context(suite, side) as context:
                    actual = context.configuration()
                    self.assertEqual(actual["tls13_suites"], (suite,))
                    self.assertEqual(actual["minimum_protocol"], 0x0304)
                    self.assertEqual(actual["maximum_protocol"], 0x0304)
                    self.assertTrue(actual["peer_verification"])
                    self.assertEqual(actual["client_certificate_required"], side == "server")
                    self.assertEqual(actual["max_early_data"], 0)

    def test_no_certificate_key_or_transport_readiness_is_invented(self):
        with TLS13Context("TLS_AES_256_GCM_SHA384", "server") as context:
            actual = context.configuration()
            self.assertFalse(actual["certificate_loaded"])
            self.assertFalse(actual["private_key_loaded"])
            self.assertFalse(actual["ready_for_transport"])
            for attribute in ("_ctx", "_library"):
                with self.assertRaises(AttributeError):
                    getattr(context, attribute)

    def test_missing_unsupported_or_multiple_suites_are_rejected(self):
        for suite in (None, "", True, "TLS_AES_128_GCM_SHA256", "DEFAULT",
                      "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256"):
            with self.subTest(suite=suite), self.assertRaises(TLSConfigurationError):
                TLS13Context(suite, "server")
        for side in (None, True, "both", ""):
            with self.assertRaises(TLSConfigurationError):
                TLS13Context("TLS_AES_256_GCM_SHA384", side)
        with self.assertRaises(TypeError):
            TLS13Context()

    def test_close_is_idempotent_and_context_is_no_longer_usable(self):
        context = TLS13Context("TLS_AES_256_GCM_SHA384", "client")
        context.close()
        context.close()
        with self.assertRaises(TLSConfigurationError):
            context.configuration()
        with self.assertRaises(TLSConfigurationError):
            context.__enter__()

    def test_context_manager_releases_on_exception_without_swallowing_it(self):
        context = TLS13Context("TLS_AES_256_GCM_SHA384", "server")
        with self.assertRaisesRegex(ValueError, "test-failure"):
            with context:
                raise ValueError("test-failure")
        with self.assertRaises(TLSConfigurationError):
            context.configuration()

    def test_context_does_not_serialize_or_duplicate_native_state(self):
        with TLS13Context("TLS_AES_256_GCM_SHA384", "client") as context:
            with self.assertRaises(TypeError):
                pickle.dumps(context)
            with self.assertRaises(TypeError):
                copy.copy(context)
            self.assertEqual(repr(context), "TLS13Context(<redacted>)")

    def test_read_and_close_on_another_thread_do_not_share_a_key(self):
        context = TLS13Context("TLS_AES_256_GCM_SHA384", "client")
        errors = []
        def worker():
            try:
                self.assertFalse(context.configuration()["private_key_loaded"])
                context.close()
            except Exception as error:
                errors.append(error)
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        with self.assertRaises(TLSConfigurationError):
            context.configuration()

    def test_rejection_diagnostic_does_not_echo_untrusted_value(self):
        marker = "untrusted-sensitive-marker"
        with self.assertRaises(TLSConfigurationError) as caught:
            TLS13Context(marker, "server")
        self.assertNotIn(marker, str(caught.exception))


class Ed25519PrimitiveTest(unittest.TestCase):
    # RFC 8032 section 7.1, vecteurs 1 et 2 : valeurs PUBLIQUES seulement.
    # Aucune graine ni clé privée, aucun opérateur ou certificat réel.
    # https://www.rfc-editor.org/rfc/rfc8032.html#section-7.1
    KEY1 = bytes.fromhex(
        "d75a980182b10ab7d54bfed3c964073a"
        "0ee172f3daa62325af021a68f707511a")
    SIG1 = bytes.fromhex(
        "e5564300c360ac729086e2cc806e828a"
        "84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46b"
        "d25bf5f0595bbe24655141438e7a100b")
    KEY2 = bytes.fromhex(
        "3d4017c3e843895a92b70aa74d1b7ebc"
        "9c982ccf2ec4968cc0cd55f12af4660c")
    SIG2 = bytes.fromhex(
        "92a009a9f0d4cab8720e820b5f642540"
        "a2b27b5416503f8fb3762223ebdb69da"
        "085ac1e43e15996e458f3613d0f11d8c"
        "387b2eaeb4302aeeb00d291612bb0c00")

    def test_public_reference_signatures_verify_without_loading_private_material(self):
        with TLS13Context("TLS_AES_256_GCM_SHA384", "server") as context:
            for key, signature, message in ((self.KEY1, self.SIG1, b""),
                                             (self.KEY2, self.SIG2, b"\x72")):
                with self.subTest(message=message):
                    self.assertIsNone(context.verify_ed25519(key, signature, message, 1))
            actual = context.configuration()
            self.assertFalse(actual["private_key_loaded"])
            self.assertFalse(actual["certificate_loaded"])
            self.assertFalse(actual["ready_for_transport"])

    def test_modified_message_key_and_signature_fail_then_valid_signature_still_verifies(self):
        changed = bytes([self.SIG1[0] ^ 1]) + self.SIG1[1:]
        with TLS13Context("TLS_AES_256_GCM_SHA384", "client") as context:
            for key, signature, message in ((self.KEY1, self.SIG1, b"x"),
                                             (self.KEY2, self.SIG1, b""),
                                             (self.KEY1, changed, b"")):
                with self.subTest(message=message), self.assertRaisesRegex(
                        TLSConfigurationError, "PA01_ED25519_SIGNATURE_INVALID"):
                    context.verify_ed25519(key, signature, message, 1)
            self.assertIsNone(context.verify_ed25519(self.KEY1, self.SIG1, b"", 1))

    def test_ed25519_primitive_requires_exact_shapes_and_explicit_budget(self):
        with TLS13Context("TLS_AES_256_GCM_SHA384", "client") as context:
            cases = (
                (None, self.SIG1, b"", 1),
                (self.KEY1[:-1], self.SIG1, b"", 1),
                (bytearray(self.KEY1), self.SIG1, b"", 1),
                (self.KEY1, self.SIG1[:-1], b"", 1),
                (self.KEY1, bytearray(self.SIG1), b"", 1),
                (self.KEY1, self.SIG1, "", 1),
                (self.KEY1, self.SIG1, b"trop-long", 1),
                (self.KEY1, self.SIG1, b"", True),
                (self.KEY1, self.SIG1, b"", 0),
            )
            for arguments in cases:
                with self.subTest(types=tuple(type(v).__name__ for v in arguments)):
                    with self.assertRaises(TLSConfigurationError):
                        context.verify_ed25519(*arguments)

    def test_closed_context_cannot_verify_or_grant_authority(self):
        context = TLS13Context("TLS_AES_256_GCM_SHA384", "server")
        context.close()
        with self.assertRaisesRegex(TLSConfigurationError, "PA01_TLS_CONTEXT_CLOSED"):
            context.verify_ed25519(self.KEY1, self.SIG1, b"", 1)

    def test_signature_error_does_not_echo_input_and_does_not_change_transport_state(self):
        marker = b"marqueur-non-fiable"
        with TLS13Context("TLS_AES_256_GCM_SHA384", "server") as context:
            with self.assertRaises(TLSConfigurationError) as caught:
                context.verify_ed25519(self.KEY1, self.SIG1, marker, 64)
            self.assertNotIn(marker.decode(), str(caught.exception))
            self.assertFalse(context.configuration()["ready_for_transport"])


if __name__ == "__main__":
    unittest.main()
