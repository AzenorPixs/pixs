"""Rejets immédiats du profil public X509, sans matériau secret."""

from __future__ import annotations

import inspect
import traceback
import unittest

from pixs.pzt_ca.x509_profile import (
    X509ProfileError,
    _require_spki_bytes,
    inspect_ca_der,
    verify_intermediate_issued,
    verify_root_self_signature,
)


class EvilEq:
    def __eq__(self, other: object) -> bool:
        raise AssertionError("eq-etranger-appele")


class BytesSubclass(bytes):
    pass


def assert_code(test: unittest.TestCase, error: X509ProfileError, expected: str) -> None:
    test.assertIs(type(error.code), str)
    test.assertEqual(error.code, expected)


class RejectTypesTest(unittest.TestCase):
    def test_reject_der_none(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(None, role="root")  # type: ignore[arg-type]
        assert_code(self, ctx.exception, "TYPE_DER")

    def test_reject_der_bytearray(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(bytearray(b"\x30\x00"), role="root")  # type: ignore[arg-type]
        assert_code(self, ctx.exception, "TYPE_DER")

    def test_reject_der_bytes_subclass(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(BytesSubclass(b"\x30\x00"), role="root")
        assert_code(self, ctx.exception, "TYPE_DER")

    def test_reject_der_empty(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"", role="root")
        assert_code(self, ctx.exception, "DER_VIDE")

    def test_reject_role_evil_eq_never_called(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"\x30\x00", role=EvilEq())  # type: ignore[arg-type]
        assert_code(self, ctx.exception, "ROLE")

    def test_reject_role_bytes(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"\x30\x00", role=b"root")  # type: ignore[arg-type]
        assert_code(self, ctx.exception, "ROLE")

    def test_reject_role_leaf(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"\x30\x00", role="leaf")
        assert_code(self, ctx.exception, "ROLE")


class RejectMalformedDerTest(unittest.TestCase):
    def test_reject_truncated(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"\x30\x03\x02\x01\x05", role="root")
        assert_code(self, ctx.exception, "DER_MALFORME")

    def test_reject_text(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"not-a-certificate", role="root")
        assert_code(self, ctx.exception, "DER_MALFORME")

    def test_reject_invalid_der_with_trailing(self) -> None:
        # DER déjà invalide ici, rejet avant la garde stricte.
        # Le vrai cas certificat valide suffixé reste en attente
        # des fixtures TPM2 éphémères.
        with self.assertRaises(X509ProfileError) as ctx:
            inspect_ca_der(b"\x30\x00\x00", role="root")
        assert_code(self, ctx.exception, "DER_MALFORME")


class RejectExpectedMaterialTest(unittest.TestCase):
    def test_reject_root_key_str(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            verify_root_self_signature(
                b"\x30\x03\x02\x01\x05",
                expected_public_key_spki_der="KEY",  # type: ignore[arg-type]
            )
        assert_code(self, ctx.exception, "CLE_ATTENDUE")

    def test_reject_root_key_subclass(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            verify_root_self_signature(
                b"\x30\x03\x02\x01\x05",
                expected_public_key_spki_der=BytesSubclass(b"\x30\x00"),
            )
        assert_code(self, ctx.exception, "CLE_ATTENDUE")

    def test_reject_root_key_malformed(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            verify_root_self_signature(
                b"\x30\x03\x02\x01\x05",
                expected_public_key_spki_der=b"\x30\x03\x02\x01\x05",
            )
        assert_code(self, ctx.exception, "CLE_ATTENDUE")

    def test_reject_spki_guard_empty_direct(self) -> None:
        # Unité interne de garde explicitement limitée : le cas
        # intermédiaire vide est testé ici sans faux positif
        # d'ordre des gardes.
        with self.assertRaises(X509ProfileError) as ctx:
            _require_spki_bytes(b"")
        assert_code(self, ctx.exception, "CLE_ATTENDUE")

    def test_reject_link_intermediate_key_param_required(self) -> None:
        parameters = inspect.signature(verify_intermediate_issued).parameters
        self.assertIn("expected_intermediate_spki_der", parameters)
        with self.assertRaises(TypeError):
            verify_intermediate_issued(  # type: ignore[call-arg]
                b"\x30\x03\x02\x01\x05",
                issuer_der=b"\x30\x03\x02\x01\x05",
                expected_issuer_spki_der=b"\x30\x00",
            )

    def test_reject_link_issuer_bytearray(self) -> None:
        with self.assertRaises(X509ProfileError) as ctx:
            verify_intermediate_issued(
                b"\x30\x03\x02\x01\x05",
                issuer_der=bytearray(b"\x30\x00"),  # type: ignore[arg-type]
                expected_issuer_spki_der=b"\x30\x00",
                expected_intermediate_spki_der=b"\x30\x00",
            )
        assert_code(self, ctx.exception, "TYPE_DER")


class RejectDiagnosticsTest(unittest.TestCase):
    def test_error_fixed_without_sentinel(self) -> None:
        sentinel = b"SENTINELLE_SECRETE_XYZ"
        try:
            inspect_ca_der(b"\x30\x00" + sentinel, role="root")
        except X509ProfileError as error:
            self.assertEqual(error.code, "DER_MALFORME")
            self.assertIs(error.__cause__, None)
            self.assertTrue(error.__suppress_context__)
            formatted = "".join(
                traceback.format_exception(
                    type(error), error, error.__traceback__
                )
            )
            self.assertNotIn("SENTINELLE", formatted)
            self.assertNotIn("SENTINELLE", str(error))
        else:
            self.fail("X509ProfileError attendue")


if __name__ == "__main__":
    unittest.main()
