"""Unités certificat, comparaison complète, sans cert existant."""

from __future__ import annotations

import datetime
import hashlib
import unittest
from unittest import mock

from pixs.pzt_ca.ca_certificate import (
    CaCertificate,
    CaCertificateError,
    CaCertificateResolutionError,
    CertificatePublicBinding,
    certificate_from_json,
    certificate_from_mapping,
    check_bytes_consistency,
    extract_verified_facts,
)
from pixs.pzt_ca.x509_profile import X509ProfileError

_VALID_BEFORE = "2026-10-23T09:00:00Z"
_VALID_AFTER = "2027-10-23T09:00:00Z"
_SENTINEL = "SENTINELLE-SANS-FUITE-zzz-123"

_CERT_DER = b"DER-CERT-PUBLIC-FIXTURE-001"
_ROOT_DER = b"DER-CERT-PUBLIC-FIXTURE-001"
_ROOT_DER_OTHER = b"DER-ROOT-AUTRE-002"
_SUBJECT_SPKI = b"SPKI-SUJET-FIXTURE-001"
_ROOT_SPKI = b"SPKI-RACINE-FIXTURE-001"


class EvilEq:
    def __eq__(self, other: object) -> bool:
        raise AssertionError("EvilEq appele")


def _base_root() -> dict:
    return {
        "object_type": "z12.ca_certificate/v1",
        "schema_version": "1.0.0",
        "cert_ref": "cert-1",
        "cert_bytes_ref": "bytes-1",
        "ca_kind": "root",
        "root_authority_ref": "root-1",
        "subject_key_ref": "sk-1",
        "generation_ref": "gen-root-1",
        "basic_constraints_critical": True,
        "key_usage_critical": True,
        "is_ca": True,
        "path_len": 1,
        "key_usage": ["keyCertSign"],
        "signature_algorithm": "ecdsa-with-SHA256",
        "curve": "secp256r1",
        "serial_public": "serial-opaque-1",
        "not_before_utc": _VALID_BEFORE,
        "not_after_utc": _VALID_AFTER,
        "fingerprint_public": "fp-opaque-1",
        "subject_key_id": "ski-opaque-1",
        "anchor_ref": "anchor-1",
    }


def _base_intermediate() -> dict:
    base = _base_root()
    base.update({
        "ca_kind": "intermediate",
        "issuer_ref": "iss-1",
        "generation_ref": "gen-1",
        "path_len": 0,
        "authority_key_id": "aki-opaque-1",
    })
    return base


def _binding_root() -> CertificatePublicBinding:
    return CertificatePublicBinding(
        cert_ref="cert-1",
        cert_bytes_ref="bytes-1",
        ca_kind="root",
        root_authority_ref="root-1",
        subject_key_ref="sk-1",
        generation_ref="gen-root-1",
        issuer_ref=None,
        anchor_ref="anchor-1",
        serial_public="serial-opaque-1",
        fingerprint_public="fp-opaque-1",
        subject_key_id="ski-opaque-1",
        authority_key_id=None,
        certificate_der=_CERT_DER,
        root_der=_CERT_DER,
        subject_spki_der=_SUBJECT_SPKI,
        root_spki_der=_SUBJECT_SPKI,
        serial_number=42,
        fingerprint_sha256=hashlib.sha256(_CERT_DER).digest(),
        ski=b"ski-bytes",
        aki=None,
    )


def _binding_intermediate() -> CertificatePublicBinding:
    return CertificatePublicBinding(
        cert_ref="cert-1",
        cert_bytes_ref="bytes-1",
        ca_kind="intermediate",
        root_authority_ref="root-1",
        subject_key_ref="sk-1",
        generation_ref="gen-1",
        issuer_ref="iss-1",
        anchor_ref="anchor-1",
        serial_public="serial-opaque-1",
        fingerprint_public="fp-opaque-1",
        subject_key_id="ski-opaque-1",
        authority_key_id="aki-opaque-1",
        certificate_der=b"DER-INTERMEDIAIRE-001",
        root_der=_ROOT_DER_OTHER,
        subject_spki_der=_SUBJECT_SPKI,
        root_spki_der=_ROOT_SPKI,
        serial_number=77,
        fingerprint_sha256=hashlib.sha256(b"DER-INTERMEDIAIRE-001").digest(),
        ski=b"ski-bytes",
        aki=b"aki-bytes",
    )


class FakeFacts:
    def __init__(self, kind: str = "root") -> None:
        if kind == "root":
            self.role = "root"
            self.serial_number = 42
            self.subject_key_identifier = b"ski-bytes"
            self.authority_key_identifier = None
            self.basic_constraints_path_length = 1
        else:
            self.role = "intermediate"
            self.serial_number = 77
            self.subject_key_identifier = b"ski-bytes"
            self.authority_key_identifier = b"aki-bytes"
            self.basic_constraints_path_length = 0
        self.not_valid_before_utc = datetime.datetime(
            2026, 10, 23, 9, 0, 0, tzinfo=datetime.timezone.utc
        )
        self.not_valid_after_utc = datetime.datetime(
            2027, 10, 23, 9, 0, 0, tzinfo=datetime.timezone.utc
        )
        self.signature_hash_algorithm = "sha256"
        self.public_key_algorithm = "EC"
        self.curve_name = "secp256r1"
        self.basic_constraints_ca = True


class MemoryBindings:
    """Comparaison en mémoire seulement, non qualification propriétaire réelle."""

    def __init__(self, binding: CertificatePublicBinding) -> None:
        self._binding = binding

    def resolve_certificate(self, cert_ref: str) -> CertificatePublicBinding:
        if type(cert_ref) is not str:
            raise CaCertificateResolutionError("bindings")
        if cert_ref != self._binding.cert_ref:
            raise CaCertificateResolutionError("bindings")
        return self._binding


class MissingBindings:
    def resolve_certificate(self, cert_ref: str) -> CertificatePublicBinding:
        raise CaCertificateResolutionError("bindings")


class WrongTypeBindings:
    def resolve_certificate(self, cert_ref: str) -> object:
        return {"faux": "binding"}


class CertificateStructureTest(unittest.TestCase):
    def test_alias_liste_non_conservee(self) -> None:
        base = _base_root()
        lst = ["keyCertSign"]
        base["key_usage"] = lst
        dec = certificate_from_mapping(base)
        self.assertEqual(dec.key_usage, ("keyCertSign",))
        self.assertIs(type(dec.key_usage), tuple)
        lst.append("autre")
        self.assertEqual(dec.key_usage, ("keyCertSign",))

    def test_dates_ordre_apres_gardes(self) -> None:
        bad = _base_root()
        bad["not_before_utc"] = _VALID_AFTER
        bad["not_after_utc"] = _VALID_BEFORE
        with self.assertRaises(CaCertificateError):
            certificate_from_mapping(bad)

    def test_construction_directe_naive_subclass_nonutc(self) -> None:
        good = _base_root()
        dec = certificate_from_mapping(good)
        naive = datetime.datetime(2026, 10, 23, 9, 0, 0)
        with self.assertRaises(CaCertificateError):
            CaCertificate(
                object_type=good["object_type"],
                schema_version=good["schema_version"],
                cert_ref=good["cert_ref"],
                cert_bytes_ref=good["cert_bytes_ref"],
                ca_kind=good["ca_kind"],
                root_authority_ref=good["root_authority_ref"],
                subject_key_ref=good["subject_key_ref"],
                generation_ref=good["generation_ref"],
                basic_constraints_critical=True,
                key_usage_critical=True,
                is_ca=True,
                path_len=1,
                key_usage=("keyCertSign",),
                signature_algorithm="ecdsa-with-SHA256",
                curve="secp256r1",
                serial_public=good["serial_public"],
                not_before_utc=naive,
                not_after_utc=dec.not_after_utc,
                fingerprint_public=good["fingerprint_public"],
                subject_key_id=good["subject_key_id"],
                anchor_ref=good["anchor_ref"],
            )

    def test_evil_eq_et_types(self) -> None:
        bad = _base_root()
        bad["object_type"] = EvilEq()
        with self.assertRaises(CaCertificateError):
            certificate_from_mapping(bad)
        bad2 = _base_root()
        bad2["path_len"] = True
        with self.assertRaises(CaCertificateError):
            certificate_from_mapping(bad2)
        bad3 = _base_root()
        bad3["is_ca"] = 1
        with self.assertRaises(CaCertificateError):
            certificate_from_mapping(bad3)

    def test_doublon_et_sentinelle(self) -> None:
        with self.assertRaises(CaCertificateError):
            certificate_from_json('{"a": 1, "a": 2}')
        bad = _base_root()
        bad["cert_ref"] = _SENTINEL
        bad["path_len"] = 7
        try:
            certificate_from_mapping(bad)
        except CaCertificateError as exc:
            self.assertNotIn(_SENTINEL, str(exc))
        else:
            self.fail("refus attendu")


class BindingValidationTest(unittest.TestCase):
    def test_binding_root_valide(self) -> None:
        binding = _binding_root()
        self.assertEqual(binding.serial_number, 42)
        self.assertEqual(len(binding.fingerprint_sha256), 32)

    def test_binding_ref_non_str_refusee(self) -> None:
        with self.assertRaises(CaCertificateResolutionError) as releve:
            CertificatePublicBinding(
                cert_ref=123,
                cert_bytes_ref="bytes-1",
                ca_kind="root",
                root_authority_ref="root-1",
                subject_key_ref="sk-1",
                generation_ref="gen-root-1",
                issuer_ref=None,
                anchor_ref="anchor-1",
                serial_public="serial-opaque-1",
                fingerprint_public="fp-opaque-1",
                subject_key_id="ski-opaque-1",
                authority_key_id=None,
                certificate_der=_CERT_DER,
                root_der=_CERT_DER,
                subject_spki_der=_SUBJECT_SPKI,
                root_spki_der=_ROOT_SPKI,
                serial_number=42,
                fingerprint_sha256=hashlib.sha256(_CERT_DER).digest(),
                ski=b"ski-bytes",
                aki=None,
            )
        self.assertEqual(releve.exception.code, "RESOLUTION_IMPOSSIBLE")

    def test_binding_bytes_vides_refuses(self) -> None:
        with self.assertRaises(CaCertificateResolutionError):
            CertificatePublicBinding(
                cert_ref="cert-1",
                cert_bytes_ref="bytes-1",
                ca_kind="root",
                root_authority_ref="root-1",
                subject_key_ref="sk-1",
                generation_ref="gen-root-1",
                issuer_ref=None,
                anchor_ref="anchor-1",
                serial_public="serial-opaque-1",
                fingerprint_public="fp-opaque-1",
                subject_key_id="ski-opaque-1",
                authority_key_id=None,
                certificate_der=b"",
                root_der=_CERT_DER,
                subject_spki_der=_SUBJECT_SPKI,
                root_spki_der=_ROOT_SPKI,
                serial_number=42,
                fingerprint_sha256=hashlib.sha256(_CERT_DER).digest(),
                ski=b"ski-bytes",
                aki=None,
            )

    def test_binding_serial_non_positif_refuse(self) -> None:
        with self.assertRaises(CaCertificateResolutionError):
            CertificatePublicBinding(
                cert_ref="cert-1",
                cert_bytes_ref="bytes-1",
                ca_kind="root",
                root_authority_ref="root-1",
                subject_key_ref="sk-1",
                generation_ref="gen-root-1",
                issuer_ref=None,
                anchor_ref="anchor-1",
                serial_public="serial-opaque-1",
                fingerprint_public="fp-opaque-1",
                subject_key_id="ski-opaque-1",
                authority_key_id=None,
                certificate_der=_CERT_DER,
                root_der=_CERT_DER,
                subject_spki_der=_SUBJECT_SPKI,
                root_spki_der=_ROOT_SPKI,
                serial_number=0,
                fingerprint_sha256=hashlib.sha256(_CERT_DER).digest(),
                ski=b"ski-bytes",
                aki=None,
            )

    def test_binding_empreinte_courte_refusee(self) -> None:
        with self.assertRaises(CaCertificateResolutionError):
            CertificatePublicBinding(
                cert_ref="cert-1",
                cert_bytes_ref="bytes-1",
                ca_kind="root",
                root_authority_ref="root-1",
                subject_key_ref="sk-1",
                generation_ref="gen-root-1",
                issuer_ref=None,
                anchor_ref="anchor-1",
                serial_public="serial-opaque-1",
                fingerprint_public="fp-opaque-1",
                subject_key_id="ski-opaque-1",
                authority_key_id=None,
                certificate_der=_CERT_DER,
                root_der=_CERT_DER,
                subject_spki_der=_SUBJECT_SPKI,
                root_spki_der=_ROOT_SPKI,
                serial_number=42,
                fingerprint_sha256=b"court",
                ski=b"ski-bytes",
                aki=None,
            )

    def test_binding_branche_root_interdit_emetteur(self) -> None:
        with self.assertRaises(CaCertificateResolutionError):
            CertificatePublicBinding(
                cert_ref="cert-1",
                cert_bytes_ref="bytes-1",
                ca_kind="root",
                root_authority_ref="root-1",
                subject_key_ref="sk-1",
                generation_ref="gen-root-1",
                issuer_ref="iss-1",
                anchor_ref="anchor-1",
                serial_public="serial-opaque-1",
                fingerprint_public="fp-opaque-1",
                subject_key_id="ski-opaque-1",
                authority_key_id=None,
                certificate_der=_CERT_DER,
                root_der=_CERT_DER,
                subject_spki_der=_SUBJECT_SPKI,
                root_spki_der=_ROOT_SPKI,
                serial_number=42,
                fingerprint_sha256=hashlib.sha256(_CERT_DER).digest(),
                ski=b"ski-bytes",
                aki=None,
            )

    def test_binding_branche_intermediaire_exige_emetteur(self) -> None:
        with self.assertRaises(CaCertificateResolutionError):
            CertificatePublicBinding(
                cert_ref="cert-1",
                cert_bytes_ref="bytes-1",
                ca_kind="intermediate",
                root_authority_ref="root-1",
                subject_key_ref="sk-1",
                generation_ref="gen-1",
                issuer_ref=None,
                anchor_ref="anchor-1",
                serial_public="serial-opaque-1",
                fingerprint_public="fp-opaque-1",
                subject_key_id="ski-opaque-1",
                authority_key_id="aki-opaque-1",
                certificate_der=b"DER-INTERMEDIAIRE-001",
                root_der=_ROOT_DER_OTHER,
                subject_spki_der=_SUBJECT_SPKI,
                root_spki_der=_ROOT_SPKI,
                serial_number=77,
                fingerprint_sha256=hashlib.sha256(b"DER-INTERMEDIAIRE-001").digest(),
                ski=b"ski-bytes",
                aki=b"aki-bytes",
            )


class ExtractFactsTest(unittest.TestCase):
    def test_ca_kind_exact_avant_branche(self) -> None:
        with self.assertRaises(CaCertificateError):
            extract_verified_facts(_CERT_DER, None, None, _SUBJECT_SPKI, "ROOT")
        with self.assertRaises(CaCertificateError):
            extract_verified_facts(_CERT_DER, None, None, _SUBJECT_SPKI, 123)

    def test_convertit_seulement_x509(self) -> None:
        with mock.patch(
            "pixs.pzt_ca.ca_certificate._x509.verify_root_self_signature",
            side_effect=X509ProfileError("DER_MALFORME"),
        ):
            with self.assertRaises(CaCertificateError):
                extract_verified_facts(_CERT_DER, None, None, _SUBJECT_SPKI, "root")

    def test_propage_inattendu(self) -> None:
        with mock.patch(
            "pixs.pzt_ca.ca_certificate._x509.verify_root_self_signature",
            side_effect=RuntimeError("panne"),
        ):
            with self.assertRaises(RuntimeError):
                extract_verified_facts(_CERT_DER, None, None, _SUBJECT_SPKI, "root")


class ConsistencyComparisonTest(unittest.TestCase):
    def test_type_exact_requis(self) -> None:
        with self.assertRaises(CaCertificateError):
            check_bytes_consistency({"faux": "objet"}, MemoryBindings(_binding_root()))

    def test_binding_manquante_refus_sans_contenu(self) -> None:
        dec = certificate_from_mapping(_base_root())
        try:
            check_bytes_consistency(dec, MissingBindings())
        except CaCertificateResolutionError as exc:
            self.assertEqual(exc.code, "RESOLUTION_IMPOSSIBLE")
            self.assertNotIn("non resolu", str(exc))
        else:
            self.fail("refus attendu")

    def test_binding_type_inexact_refuse(self) -> None:
        dec = certificate_from_mapping(_base_root())
        with self.assertRaises(CaCertificateResolutionError):
            check_bytes_consistency(dec, WrongTypeBindings())

    def test_toutes_references_comparees(self) -> None:
        dec = certificate_from_mapping(_base_root())
        binding = _binding_root()
        altered = CertificatePublicBinding(
            cert_ref=binding.cert_ref,
            cert_bytes_ref=binding.cert_bytes_ref,
            ca_kind=binding.ca_kind,
            root_authority_ref="root-autre",
            subject_key_ref=binding.subject_key_ref,
            generation_ref=binding.generation_ref,
            issuer_ref=binding.issuer_ref,
            anchor_ref=binding.anchor_ref,
            serial_public=binding.serial_public,
            fingerprint_public=binding.fingerprint_public,
            subject_key_id=binding.subject_key_id,
            authority_key_id=binding.authority_key_id,
            certificate_der=binding.certificate_der,
            root_der=binding.root_der,
            subject_spki_der=binding.subject_spki_der,
            root_spki_der=binding.root_spki_der,
            serial_number=binding.serial_number,
            fingerprint_sha256=binding.fingerprint_sha256,
            ski=binding.ski,
            aki=binding.aki,
        )
        with self.assertRaises(CaCertificateError) as releve:
            check_bytes_consistency(dec, MemoryBindings(altered))
        self.assertEqual(releve.exception.code, "REFERENCE_INCOHERENTE")

    def test_racine_exige_der_egal(self) -> None:
        dec = certificate_from_mapping(_base_root())
        binding = _binding_root()
        altered = CertificatePublicBinding(
            cert_ref=binding.cert_ref,
            cert_bytes_ref=binding.cert_bytes_ref,
            ca_kind=binding.ca_kind,
            root_authority_ref=binding.root_authority_ref,
            subject_key_ref=binding.subject_key_ref,
            generation_ref=binding.generation_ref,
            issuer_ref=binding.issuer_ref,
            anchor_ref=binding.anchor_ref,
            serial_public=binding.serial_public,
            fingerprint_public=binding.fingerprint_public,
            subject_key_id=binding.subject_key_id,
            authority_key_id=binding.authority_key_id,
            certificate_der=binding.certificate_der,
            root_der=_ROOT_DER_OTHER,
            subject_spki_der=binding.subject_spki_der,
            root_spki_der=binding.root_spki_der,
            serial_number=binding.serial_number,
            fingerprint_sha256=binding.fingerprint_sha256,
            ski=binding.ski,
            aki=binding.aki,
        )
        with self.assertRaises(CaCertificateError) as releve:
            check_bytes_consistency(dec, MemoryBindings(altered))
        self.assertEqual(releve.exception.code, "RACINE_INCOHERENTE")

    def test_succes_root_retourne_faits_seuls(self) -> None:
        dec = certificate_from_mapping(_base_root())
        fake = FakeFacts("root")
        with mock.patch(
            "pixs.pzt_ca.ca_certificate.extract_verified_facts",
            return_value=fake,
        ):
            result = check_bytes_consistency(dec, MemoryBindings(_binding_root()))
            self.assertIs(result, fake)

    def test_succes_intermediaire_aki_exacte(self) -> None:
        base = _base_intermediate()
        dec = certificate_from_mapping(base)
        fake = FakeFacts("intermediate")
        with mock.patch(
            "pixs.pzt_ca.ca_certificate.extract_verified_facts",
            return_value=fake,
        ):
            result = check_bytes_consistency(dec, MemoryBindings(_binding_intermediate()))
            self.assertIs(result, fake)

    def test_aki_presence_exacte(self) -> None:
        dec = certificate_from_mapping(_base_root())
        fake = FakeFacts("root")
        fake.authority_key_identifier = b"aki-bytes"
        with mock.patch(
            "pixs.pzt_ca.ca_certificate.extract_verified_facts",
            return_value=fake,
        ):
            with self.assertRaises(CaCertificateError) as releve:
                check_bytes_consistency(dec, MemoryBindings(_binding_root()))
            self.assertEqual(releve.exception.code, "AKI_INCOHERENT")

    def test_serie_empreinte_ski_verifiees(self) -> None:
        dec = certificate_from_mapping(_base_root())
        fake = FakeFacts("root")
        fake.serial_number = 999
        with mock.patch(
            "pixs.pzt_ca.ca_certificate.extract_verified_facts",
            return_value=fake,
        ):
            with self.assertRaises(CaCertificateError) as releve:
                check_bytes_consistency(dec, MemoryBindings(_binding_root()))
            self.assertEqual(releve.exception.code, "SERIE_INCOHERENTE")

    def test_sans_membership_ni_unicite(self) -> None:
        import pixs.pzt_ca.ca_certificate as module

        self.assertFalse(hasattr(module.CertificateOwnerBindings, "is_anchor_provisioned"))
        self.assertFalse(hasattr(module.CertificateOwnerBindings, "is_registry_member"))
        self.assertFalse(hasattr(module.CertificateOwnerBindings, "is_serial_unique"))


class CertificateConsistencyExtraTest(unittest.TestCase):
    def test_runtime_error_resolveur_propagee(self) -> None:
        dec = certificate_from_mapping(_base_root())
        class Exploding:
            def resolve_certificate(self, cert_ref: str) -> CertificatePublicBinding:
                raise RuntimeError("panne-resolveur")
        with self.assertRaises(RuntimeError):
            check_bytes_consistency(dec, Exploding())

    def test_empreinte_alteree_refusee(self) -> None:
        import dataclasses
        dec = certificate_from_mapping(_base_root())
        base = _binding_root()
        altered = dataclasses.replace(base, fingerprint_sha256=b"\x01" * 32)
        fake = FakeFacts("root")
        with mock.patch("pixs.pzt_ca.ca_certificate.extract_verified_facts", return_value=fake):
            with self.assertRaises(CaCertificateError) as releve:
                check_bytes_consistency(dec, MemoryBindings(altered))
            self.assertEqual(releve.exception.code, "EMPREINTE_INCOHERENTE")

    def test_ski_altere_refuse(self) -> None:
        import dataclasses
        dec = certificate_from_mapping(_base_root())
        base = _binding_root()
        altered = dataclasses.replace(base, ski=b"autre-ski")
        fake = FakeFacts("root")
        with mock.patch("pixs.pzt_ca.ca_certificate.extract_verified_facts", return_value=fake):
            with self.assertRaises(CaCertificateError) as releve:
                check_bytes_consistency(dec, MemoryBindings(altered))
            self.assertEqual(releve.exception.code, "SKI_INCOHERENT")

    def test_root_spki_incoherent_refuse(self) -> None:
        import dataclasses
        dec = certificate_from_mapping(_base_root())
        base = _binding_root()
        altered = dataclasses.replace(base, root_spki_der=b"SPKI-AUTRE")
        with self.assertRaises(CaCertificateError) as releve:
            check_bytes_consistency(dec, MemoryBindings(altered))
        self.assertEqual(releve.exception.code, "RACINE_INCOHERENTE")

    def test_chaque_ref_simple_root_comparee_avant_extraction(self) -> None:
        import dataclasses
        dec = certificate_from_mapping(_base_root())
        base = _binding_root()
        for field_name in ("cert_bytes_ref", "root_authority_ref", "subject_key_ref", "generation_ref", "anchor_ref", "serial_public", "fingerprint_public", "subject_key_id"):
            with self.subTest(ref=field_name):
                altered = dataclasses.replace(base, **{field_name: "autre-ref"})
                with self.assertRaises(CaCertificateError) as releve:
                    check_bytes_consistency(dec, MemoryBindings(altered))
                self.assertEqual(releve.exception.code, "REFERENCE_INCOHERENTE")


if __name__ == "__main__":
    unittest.main()
