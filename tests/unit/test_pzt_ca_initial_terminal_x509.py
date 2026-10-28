"""Tests profil feuille D7 sur DER réels éphémères, sans qualification."""

from __future__ import annotations

import datetime
import ipaddress
import unittest
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from pixs.pzt_ca.initial_terminal_x509 import (
    InitialTerminalX509Error,
    assert_terminal_pair_distinct,
    inspect_initial_terminal_der,
    verify_initial_terminal_issued,
)

V7_A = "0193e8d5-5c9a-7a1b-8c2d-3e4f5a6b7c8d"
V7_B = "0193e8d6-1111-7c22-8d33-444455556666"
V4_UUID = "550e8400-e29b-41d4-a716-446655440000"
NON_RFC_VARIANT_UUID = "0193e8d5-5c9a-7a1b-ec2d-3e4f5a6b7c8d"
LOOPBACK = "127.0.0.2"
LOOPBACK_OTHER = "127.0.0.3"
UTC = datetime.timezone.utc
LEAF_NOT_BEFORE = datetime.datetime(2026, 10, 23, 10, 0, 0, tzinfo=UTC)
LEAF_NOT_AFTER = datetime.datetime(2026, 10, 24, 10, 0, 0, tzinfo=UTC)
CA_NOT_BEFORE = datetime.datetime(2026, 10, 23, 10, 0, 0, tzinfo=UTC)
CA_NOT_AFTER = datetime.datetime(2027, 10, 23, 10, 0, 0, tzinfo=UTC)


def _key_p256() -> Any:
    return ec.generate_private_key(ec.SECP256R1())


def _spki(key: Any) -> bytes:
    return key.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def _ski(key: Any) -> bytes:
    return x509.SubjectKeyIdentifier.from_public_key(
        key.public_key()
    ).digest


def _name(cn: str) -> x509.Name:
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)])


def _build_root(key: Any, serial: int = 0x1001) -> bytes:
    builder = (
        x509.CertificateBuilder()
        .subject_name(_name("PZT-Root-D2"))
        .issuer_name(_name("PZT-Root-D2"))
        .public_key(key.public_key())
        .serial_number(serial)
        .not_valid_before(CA_NOT_BEFORE)
        .not_valid_after(CA_NOT_AFTER)
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=1), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=False, content_commitment=False,
                key_encipherment=False, data_encipherment=False,
                key_agreement=False, key_cert_sign=True, crl_sign=False,
                encipher_only=False, decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier(_ski(key)), critical=False
        )
        .add_extension(
            x509.AuthorityKeyIdentifier(
                key_identifier=_ski(key),
                authority_cert_issuer=None,
                authority_cert_serial_number=None,
            ),
            critical=False,
        )
    )
    return builder.sign(key, hashes.SHA256()).public_bytes(
        serialization.Encoding.DER
    )


def _build_interm(
    key: Any, issuer_key: Any, issuer_der: bytes,
    serial: int = 0x2001, extra_nc: bool = False,
) -> bytes:
    issuer_cert = x509.load_der_x509_certificate(issuer_der)
    builder = (
        x509.CertificateBuilder()
        .subject_name(_name("PZT-Inter-D2"))
        .issuer_name(issuer_cert.subject)
        .public_key(key.public_key())
        .serial_number(serial)
        .not_valid_before(CA_NOT_BEFORE)
        .not_valid_after(CA_NOT_AFTER)
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=0), critical=True
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=False, content_commitment=False,
                key_encipherment=False, data_encipherment=False,
                key_agreement=False, key_cert_sign=True, crl_sign=False,
                encipher_only=False, decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier(_ski(key)), critical=False
        )
        .add_extension(
            x509.AuthorityKeyIdentifier(
                key_identifier=_ski(issuer_key),
                authority_cert_issuer=None,
                authority_cert_serial_number=None,
            ),
            critical=False,
        )
    )
    if extra_nc:
        builder = builder.add_extension(
            x509.NameConstraints(
                permitted_subtrees=[x509.DNSName("example.test")], excluded_subtrees=None
            ),
            critical=True,
        )
    return builder.sign(issuer_key, hashes.SHA256()).public_bytes(
        serialization.Encoding.DER
    )


def _leaf_extensions(
    usage: str, instance_uuid: str, ip: str | None,
    key: Any, issuer_key: Any,
    ku_extra: bool = False,
    ku_critical: bool = True,
    eku_mode: str = "exact",
    eku_critical: bool = True,
    san_mode: str = "exact",
    san_critical: bool = True,
    bc_ca: bool = False,
    bc_critical: bool = True,
    ski_bad: bool = False,
    aki_bad: bool = False,
    ski_critical: bool = False,
    aki_critical: bool = False,
) -> list[tuple[x509.ExtensionType, bool]]:
    if usage == "clientAuth":
        wanted = [ExtendedKeyUsageOID.CLIENT_AUTH]
    else:
        wanted = [ExtendedKeyUsageOID.SERVER_AUTH]
    if eku_mode == "double_mixed":
        eku_list = [
            ExtendedKeyUsageOID.CLIENT_AUTH,
            ExtendedKeyUsageOID.SERVER_AUTH,
        ]
    elif eku_mode == "double_same":
        eku_list = [wanted[0], wanted[0]]
    elif eku_mode == "exact":
        eku_list = wanted
    else:
        raise ValueError("Mode fixture EKU inconnu")
    if san_mode == "exact":
        if usage == "clientAuth":
            san_names: list[x509.GeneralName] = [
                x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}")
            ]
        else:
            san_names = [
                x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}"),
                x509.IPAddress(ipaddress.IPv4Address(str(ip))),
            ]
    elif san_mode == "dns":
        san_names = [x509.DNSName("pzt.local")]
    elif san_mode == "ipv6":
        san_names = [
            x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}"),
            x509.IPAddress(ipaddress.IPv6Address("::1")),
        ]
    elif san_mode == "duplicate-uri":
        san_names = [
            x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}"),
            x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}"),
        ]
    elif san_mode == "foreign-uri":
        san_names = [
            x509.UniformResourceIdentifier("urn:uuid:other")
        ]
    elif san_mode == "client-with-ip":
        san_names = [
            x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}"),
            x509.IPAddress(ipaddress.IPv4Address(LOOPBACK)),
        ]
    elif san_mode == "server-missing-ip":
        san_names = [
            x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}")
        ]
    elif san_mode == "extra-foreign":
        san_names = [
            x509.UniformResourceIdentifier(f"urn:uuid:{instance_uuid}"),
            x509.IPAddress(ipaddress.IPv4Address(str(ip))),
            x509.DNSName("pzt.local"),
        ]
    else:
        raise ValueError("Mode fixture SAN inconnu")
    ku = x509.KeyUsage(
        digital_signature=True, content_commitment=False,
        key_encipherment=ku_extra, data_encipherment=False,
        key_agreement=False, key_cert_sign=False, crl_sign=False,
        encipher_only=False, decipher_only=False,
    )
    ski_value = b"\x00" * 20 if ski_bad else _ski(key)
    aki_value = b"\x00" * 20 if aki_bad else _ski(issuer_key)
    return [
        (x509.BasicConstraints(ca=bc_ca, path_length=None), bc_critical),
        (ku, ku_critical),
        (x509.ExtendedKeyUsage(eku_list), eku_critical),
        (x509.SubjectAlternativeName(san_names), san_critical),
        (x509.SubjectKeyIdentifier(ski_value), ski_critical),
        (
            x509.AuthorityKeyIdentifier(
                key_identifier=aki_value,
                authority_cert_issuer=None,
                authority_cert_serial_number=None,
            ),
            aki_critical,
        ),
    ]


def _build_leaf(
    key: Any, issuer_key: Any, issuer_der: bytes,
    usage: str, instance_uuid: str, ip: str | None,
    serial: int = 0x3001,
    subject_empty: bool = True,
    omit_eku: bool = False,
    extra_extension: tuple[x509.ExtensionType, bool] | None = None,
    sign_key: Any = None,
    sign_hash: Any = None,
    eku_mode: str = "exact",
    eku_critical: bool = True,
    san_mode: str = "exact",
    san_critical: bool = True,
    ku_extra: bool = False,
    ku_critical: bool = True,
    bc_ca: bool = False,
    bc_critical: bool = True,
    ski_bad: bool = False,
    aki_bad: bool = False,
    ski_critical: bool = False,
    aki_critical: bool = False,
) -> bytes:
    issuer_cert = x509.load_der_x509_certificate(issuer_der)
    subject = x509.Name([]) if subject_empty else _name("leaf")
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer_cert.subject)
        .public_key(key.public_key())
        .serial_number(serial)
        .not_valid_before(LEAF_NOT_BEFORE)
        .not_valid_after(LEAF_NOT_AFTER)
    )
    for extension, critical in _leaf_extensions(
        usage, instance_uuid, ip, key, issuer_key,
        ku_extra=ku_extra, ku_critical=ku_critical,
        eku_mode=eku_mode, eku_critical=eku_critical,
        san_mode=san_mode, san_critical=san_critical,
        bc_ca=bc_ca, bc_critical=bc_critical,
        ski_bad=ski_bad, aki_bad=aki_bad,
        ski_critical=ski_critical, aki_critical=aki_critical,
    ):
        if omit_eku and isinstance(extension, x509.ExtendedKeyUsage):
            continue
        builder = builder.add_extension(extension, critical=critical)
    if extra_extension is not None:
        builder = builder.add_extension(
            extra_extension[0], critical=extra_extension[1]
        )
    active_sign_key = issuer_key if sign_key is None else sign_key
    active_hash = hashes.SHA256() if sign_hash is None else sign_hash
    return builder.sign(active_sign_key, active_hash).public_bytes(
        serialization.Encoding.DER
    )


def _build_leaf_with_aki_issuer(
    key: Any, issuer_key: Any, issuer_der: bytes,
    usage: str, instance_uuid: str, ip: str | None,
    aki_mode: str,
) -> bytes:
    issuer_cert = x509.load_der_x509_certificate(issuer_der)
    subject = x509.Name([])
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer_cert.subject)
        .public_key(key.public_key())
        .serial_number(0x3100)
        .not_valid_before(LEAF_NOT_BEFORE)
        .not_valid_after(LEAF_NOT_AFTER)
    )
    for extension, critical in _leaf_extensions(
        usage, instance_uuid, ip, key, issuer_key
    ):
        if isinstance(extension, x509.AuthorityKeyIdentifier):
            continue
        builder = builder.add_extension(extension, critical=critical)
    root_cert = issuer_cert
    if aki_mode == "coherent":
        aki = x509.AuthorityKeyIdentifier(
            key_identifier=_ski(issuer_key),
            authority_cert_issuer=[x509.DirectoryName(root_cert.issuer)],
            authority_cert_serial_number=issuer_cert.serial_number,
        )
    elif aki_mode == "wrong-dn-interm":
        aki = x509.AuthorityKeyIdentifier(
            key_identifier=_ski(issuer_key),
            authority_cert_issuer=[
                x509.DirectoryName(issuer_cert.subject)
            ],
            authority_cert_serial_number=issuer_cert.serial_number,
        )
    elif aki_mode == "wrong-serial":
        aki = x509.AuthorityKeyIdentifier(
            key_identifier=_ski(issuer_key),
            authority_cert_issuer=[x509.DirectoryName(root_cert.issuer)],
            authority_cert_serial_number=0x9999,
        )
    else:
        aki = x509.AuthorityKeyIdentifier(
            key_identifier=_ski(issuer_key),
            authority_cert_issuer=[
                x509.DirectoryName(root_cert.issuer),
                x509.RFC822Name("intrus@example.test"),
            ],
            authority_cert_serial_number=issuer_cert.serial_number,
        )
    builder = builder.add_extension(aki, critical=False)
    return builder.sign(issuer_key, hashes.SHA256()).public_bytes(
        serialization.Encoding.DER
    )


def _chain(
    usage: str, uuid_text: str, ip: str | None,
    **leaf_options: Any,
) -> dict[str, Any]:
    root_key = _key_p256()
    interm_key = _key_p256()
    leaf_key = _key_p256()
    root_der = _build_root(root_key)
    interm_der = _build_interm(interm_key, root_key, root_der)
    leaf_der = _build_leaf(
        leaf_key, interm_key, interm_der, usage, uuid_text, ip,
        **leaf_options,
    )
    return {
        "root_key": root_key, "interm_key": interm_key,
        "leaf_key": leaf_key, "root_der": root_der,
        "interm_der": interm_der, "leaf_der": leaf_der,
    }


class TerminalX509Test(unittest.TestCase):
    def test_client_ok_24h(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        facts, _, _ = verify_initial_terminal_issued(
            chain["leaf_der"], intermediate_der=chain["interm_der"],
            root_der=chain["root_der"],
            expected_leaf_spki_der=_spki(chain["leaf_key"]),
            expected_intermediate_spki_der=_spki(chain["interm_key"]),
            expected_root_spki_der=_spki(chain["root_key"]),
            expected_instance_uuid=V7_A,
            expected_tls_usage="clientAuth",
            expected_server_ipv4=None,
        )
        self.assertEqual(facts.instance_uuid, V7_A)
        self.assertIsNone(facts.server_ipv4)
        self.assertEqual(facts.not_valid_before_utc, LEAF_NOT_BEFORE)
        self.assertEqual(facts.not_valid_after_utc, LEAF_NOT_AFTER)

    def test_serveur_ok_ip_explicite(self) -> None:
        chain = _chain("serverAuth", V7_A, LOOPBACK)
        facts, _, _ = verify_initial_terminal_issued(
            chain["leaf_der"], intermediate_der=chain["interm_der"],
            root_der=chain["root_der"],
            expected_leaf_spki_der=_spki(chain["leaf_key"]),
            expected_intermediate_spki_der=_spki(chain["interm_key"]),
            expected_root_spki_der=_spki(chain["root_key"]),
            expected_instance_uuid=V7_A,
            expected_tls_usage="serverAuth",
            expected_server_ipv4=LOOPBACK,
        )
        self.assertEqual(facts.server_ipv4, LOOPBACK)

    def test_extension_manquante(self) -> None:
        chain = _chain("clientAuth", V7_A, None, omit_eku=True)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_extension_etrangere(self) -> None:
        chain = _chain(
            "clientAuth", V7_A, None,
            extra_extension=(
                x509.UnrecognizedExtension(
                    x509.ObjectIdentifier("1.2.3.4"), b"\x05\x00"
                ),
                False,
            ),
        )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_ca_nameconstraints_refuse(self) -> None:
        root_key = _key_p256()
        interm_key = _key_p256()
        leaf_key = _key_p256()
        root_der = _build_root(root_key)
        interm_der = _build_interm(
            interm_key, root_key, root_der, extra_nc=True
        )
        leaf_der = _build_leaf(
            leaf_key, interm_key, interm_der, "clientAuth", V7_A, None
        )
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                leaf_der, intermediate_der=interm_der,
                root_der=root_der,
                expected_leaf_spki_der=_spki(leaf_key),
                expected_intermediate_spki_der=_spki(interm_key),
                expected_root_spki_der=_spki(root_key),
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_sujet_non_vide(self) -> None:
        chain = _chain(
            "clientAuth", V7_A, None, subject_empty=False
        )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_ku_double_et_criticite(self) -> None:
        chain = _chain("clientAuth", V7_A, None, ku_extra=True)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        chain = _chain("clientAuth", V7_A, None, ku_critical=False)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_eku_double_mixte_et_double_meme(self) -> None:
        chain = _chain("clientAuth", V7_A, None, eku_mode="double_mixed")
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        chain = _chain("serverAuth", V7_A, LOOPBACK, eku_mode="double_same")
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="serverAuth",
                expected_server_ipv4=LOOPBACK,
            )
        chain = _chain(
            "clientAuth", V7_A, None, eku_critical=False
        )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_san_criticite(self) -> None:
        chain = _chain("clientAuth", V7_A, None, san_critical=False)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_uri_etrangere_dupliquee(self) -> None:
        for mode in ("foreign-uri", "duplicate-uri", "dns"):
            with self.subTest(mode=mode):
                chain = _chain("clientAuth", V7_A, None, san_mode=mode)
                with self.assertRaises(InitialTerminalX509Error):
                    inspect_initial_terminal_der(
                        chain["leaf_der"],
                        expected_instance_uuid=V7_A,
                        expected_tls_usage="clientAuth",
                        expected_server_ipv4=None,
                    )

    def test_client_ip_interdite(self) -> None:
        chain = _chain(
            "clientAuth", V7_A, None, san_mode="client-with-ip"
        )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_serveur_san_sans_ip_distinct_du_parametre_nul(self) -> None:
        chain = _chain(
            "serverAuth", V7_A, LOOPBACK, san_mode="server-missing-ip"
        )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="serverAuth",
                expected_server_ipv4=LOOPBACK,
            )
        chain = _chain("serverAuth", V7_A, LOOPBACK)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="serverAuth",
                expected_server_ipv4=None,
            )

    def test_ipv6_et_san_etranger(self) -> None:
        chain = _chain("serverAuth", V7_A, LOOPBACK, san_mode="ipv6")
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="serverAuth",
                expected_server_ipv4=LOOPBACK,
            )
        chain = _chain(
            "serverAuth", V7_A, LOOPBACK, san_mode="extra-foreign"
        )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="serverAuth",
                expected_server_ipv4=LOOPBACK,
            )

    def test_ca_true(self) -> None:
        chain = _chain("clientAuth", V7_A, None, bc_ca=True)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_ski_aki_mauvais(self) -> None:
        chain = _chain("clientAuth", V7_A, None, ski_bad=True)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"], expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        chain = _chain("clientAuth", V7_A, None, aki_bad=True)
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                chain["leaf_der"],
                intermediate_der=chain["interm_der"],
                root_der=chain["root_der"],
                expected_leaf_spki_der=_spki(chain["leaf_key"]),
                expected_intermediate_spki_der=_spki(
                    chain["interm_key"]
                ),
                expected_root_spki_der=_spki(chain["root_key"]),
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_aki_issuer_serial_racine(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        coherent = _build_leaf_with_aki_issuer(
            chain["leaf_key"], chain["interm_key"],
            chain["interm_der"], "clientAuth", V7_A, None,
            aki_mode="coherent",
        )
        facts, _, _ = verify_initial_terminal_issued(
            coherent, intermediate_der=chain["interm_der"],
            root_der=chain["root_der"],
            expected_leaf_spki_der=_spki(chain["leaf_key"]),
            expected_intermediate_spki_der=_spki(chain["interm_key"]),
            expected_root_spki_der=_spki(chain["root_key"]),
            expected_instance_uuid=V7_A,
            expected_tls_usage="clientAuth",
            expected_server_ipv4=None,
        )
        self.assertEqual(facts.instance_uuid, V7_A)
        for mode in (
            "wrong-dn-interm", "wrong-serial", "foreign-name"
        ):
            with self.subTest(mode=mode):
                bad = _build_leaf_with_aki_issuer(
                    chain["leaf_key"], chain["interm_key"],
                    chain["interm_der"], "clientAuth", V7_A, None,
                    aki_mode=mode,
                )
                with self.assertRaises(InitialTerminalX509Error):
                    verify_initial_terminal_issued(
                        bad,
                        intermediate_der=chain["interm_der"],
                        root_der=chain["root_der"],
                        expected_leaf_spki_der=_spki(
                            chain["leaf_key"]
                        ),
                        expected_intermediate_spki_der=_spki(
                            chain["interm_key"]
                        ),
                        expected_root_spki_der=_spki(chain["root_key"]),
                        expected_instance_uuid=V7_A,
                        expected_tls_usage="clientAuth",
                        expected_server_ipv4=None,
                    )

    def test_emetteur_signature_faux(self) -> None:
        other_key = _key_p256()
        other_root = _build_root(other_key, serial=0x9001)
        other_interm_key = _key_p256()
        other_interm = _build_interm(
            other_interm_key, other_key, other_root, serial=0x9002
        )
        chain = _chain("clientAuth", V7_A, None)
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                chain["leaf_der"],
                intermediate_der=other_interm,
                root_der=other_root,
                expected_leaf_spki_der=_spki(chain["leaf_key"]),
                expected_intermediate_spki_der=_spki(other_interm_key),
                expected_root_spki_der=_spki(other_key),
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        bad_key = _key_p256()
        chain = _chain(
            "clientAuth", V7_A, None, sign_key=bad_key
        )
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                chain["leaf_der"],
                intermediate_der=chain["interm_der"],
                root_der=chain["root_der"],
                expected_leaf_spki_der=_spki(chain["leaf_key"]),
                expected_intermediate_spki_der=_spki(
                    chain["interm_key"]
                ),
                expected_root_spki_der=_spki(chain["root_key"]),
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_frere_valide_mais_chaine_attentes_contradictoires(self) -> None:
        main = _chain("clientAuth", V7_A, None)
        sibling_interm_key = _key_p256()
        sibling_interm = _build_interm(
            sibling_interm_key, main["root_key"], main["root_der"],
            serial=0x9102,
        )
        sibling_leaf_key = _key_p256()
        sibling_leaf = _build_leaf(
            sibling_leaf_key, sibling_interm_key, sibling_interm,
            "clientAuth", V7_B, None,
        )
        facts, _, _ = verify_initial_terminal_issued(
            sibling_leaf, intermediate_der=sibling_interm,
            root_der=main["root_der"],
            expected_leaf_spki_der=_spki(sibling_leaf_key),
            expected_intermediate_spki_der=_spki(sibling_interm_key),
            expected_root_spki_der=_spki(main["root_key"]),
            expected_instance_uuid=V7_B,
            expected_tls_usage="clientAuth", expected_server_ipv4=None,
        )
        self.assertEqual(facts.instance_uuid, V7_B)
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                sibling_leaf, intermediate_der=main["interm_der"],
                root_der=main["root_der"],
                expected_leaf_spki_der=_spki(sibling_leaf_key),
                expected_intermediate_spki_der=_spki(main["interm_key"]),
                expected_root_spki_der=_spki(main["root_key"]),
                expected_instance_uuid=V7_B,
                expected_tls_usage="clientAuth", expected_server_ipv4=None,
            )
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                main["leaf_der"], intermediate_der=main["interm_der"],
                root_der=main["root_der"],
                expected_leaf_spki_der=_spki(main["leaf_key"]),
                expected_intermediate_spki_der=_spki(main["interm_key"]),
                expected_root_spki_der=_spki(main["root_key"]),
                expected_instance_uuid=V7_B,
                expected_tls_usage="clientAuth", expected_server_ipv4=None,
            )


    def test_spki_etrangeres(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        foreign_key = _key_p256()
        for field, spki in [
            ("leaf", _spki(foreign_key)),
            ("interm", _spki(chain["leaf_key"])),
            ("root", _spki(chain["leaf_key"])),
        ]:
            with self.subTest(field=field):
                kwargs: dict[str, Any] = {
                    "expected_leaf_spki_der": _spki(
                        chain["leaf_key"]
                    ),
                    "expected_intermediate_spki_der": _spki(
                        chain["interm_key"]
                    ),
                    "expected_root_spki_der": _spki(
                        chain["root_key"]
                    ),
                }
                if field == "leaf":
                    kwargs["expected_leaf_spki_der"] = spki
                elif field == "interm":
                    kwargs["expected_intermediate_spki_der"] = spki
                else:
                    kwargs["expected_root_spki_der"] = spki
                with self.assertRaises(InitialTerminalX509Error):
                    verify_initial_terminal_issued(
                        chain["leaf_der"],
                        intermediate_der=chain["interm_der"],
                        root_der=chain["root_der"],
                        expected_instance_uuid=V7_A,
                        expected_tls_usage="clientAuth",
                        expected_server_ipv4=None,
                        **kwargs,
                    )

    def test_reutilisation_ca(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        for key_name in ("interm_key", "root_key"):
            with self.subTest(key_name=key_name):
                reused_key = chain[key_name]
                bad_leaf = _build_leaf(
                    reused_key, chain["interm_key"], chain["interm_der"],
                    "clientAuth", V7_A, None,
                )
                with self.assertRaises(InitialTerminalX509Error) as caught:
                    verify_initial_terminal_issued(
                        bad_leaf, intermediate_der=chain["interm_der"],
                        root_der=chain["root_der"],
                        expected_leaf_spki_der=_spki(reused_key),
                        expected_intermediate_spki_der=_spki(chain["interm_key"]),
                        expected_root_spki_der=_spki(chain["root_key"]),
                        expected_instance_uuid=V7_A,
                        expected_tls_usage="clientAuth", expected_server_ipv4=None,
                    )
                self.assertEqual(caught.exception.code, "CLE_REUTILISEE")


    def test_paire_distincte(self) -> None:
        client = _chain("clientAuth", V7_A, None)
        server = _chain("serverAuth", V7_A, LOOPBACK_OTHER)
        assert_terminal_pair_distinct(
            _spki(client["leaf_key"]), _spki(server["leaf_key"])
        )
        with self.assertRaises(InitialTerminalX509Error):
            assert_terminal_pair_distinct(
                _spki(client["leaf_key"]),
                _spki(client["leaf_key"]),
            )

    def test_cle_rsa_p384_rejetees(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        rsa_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048
        )
        rsa_spki = rsa_key.public_key().public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                chain["leaf_der"],
                intermediate_der=chain["interm_der"],
                root_der=chain["root_der"],
                expected_leaf_spki_der=rsa_spki,
                expected_intermediate_spki_der=_spki(
                    chain["interm_key"]
                ),
                expected_root_spki_der=_spki(chain["root_key"]),
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        p384_key = ec.generate_private_key(ec.SECP384R1())
        with self.assertRaises(InitialTerminalX509Error):
            verify_initial_terminal_issued(
                chain["leaf_der"],
                intermediate_der=chain["interm_der"],
                root_der=chain["root_der"],
                expected_leaf_spki_der=_spki(p384_key),
                expected_intermediate_spki_der=_spki(
                    chain["interm_key"]
                ),
                expected_root_spki_der=_spki(chain["root_key"]),
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_mauvais_hash_signature(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        issuer_cert = x509.load_der_x509_certificate(
            chain["interm_der"]
        )
        builder = (
            x509.CertificateBuilder()
            .subject_name(x509.Name([]))
            .issuer_name(issuer_cert.subject)
            .public_key(chain["leaf_key"].public_key())
            .serial_number(0x3009)
            .not_valid_before(LEAF_NOT_BEFORE)
            .not_valid_after(LEAF_NOT_AFTER)
        )
        for extension, critical in _leaf_extensions(
            "clientAuth", V7_A, None, chain["leaf_key"],
            chain["interm_key"],
        ):
            builder = builder.add_extension(
                extension, critical=critical
            )
        bad_der = builder.sign(
            chain["interm_key"], hashes.SHA384()
        ).public_bytes(serialization.Encoding.DER)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                bad_der, expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_der_malforme_suffixe(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                b"\x30\x03\x02\x01\x05",
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        with self.assertRaises(InitialTerminalX509Error):
            inspect_initial_terminal_der(
                chain["leaf_der"] + b"\x00",
                expected_instance_uuid=V7_A,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )

    def test_diagnostic_sans_entree(self) -> None:
        marker = "VALEUR_SYNTHETIQUE_REJETEE_X509_1a2b"
        chain = _chain("clientAuth", V7_A, None)
        try:
            inspect_initial_terminal_der(
                chain["leaf_der"],
                expected_instance_uuid=marker,
                expected_tls_usage="clientAuth",
                expected_server_ipv4=None,
            )
        except InitialTerminalX509Error as exc:
            self.assertNotIn(marker, str(exc))
            self.assertNotIn(marker, exc.code)
        else:
            self.fail("refus attendu")

    def test_criticite_bc_ski_aki(self) -> None:
        for field, value, code in (
            ("bc_critical", False, "CONTRAINTES_CRITICITE"),
            ("ski_critical", True, "SKI_CRITICITE"),
            ("aki_critical", True, "AKI_CRITICITE"),
        ):
            with self.subTest(field=field):
                chain = _chain("clientAuth", V7_A, None, **{field: value})
                with self.assertRaises(InitialTerminalX509Error) as caught:
                    inspect_initial_terminal_der(
                        chain["leaf_der"], expected_instance_uuid=V7_A,
                        expected_tls_usage="clientAuth", expected_server_ipv4=None,
                    )
                self.assertEqual(caught.exception.code, code)

    def test_algorithme_reel_de_la_cle_feuille(self) -> None:
        chain = _chain("clientAuth", V7_A, None)
        cases = (
            (rsa.generate_private_key(public_exponent=65537, key_size=2048), "CLE_PUBLIQUE"),
            (ec.generate_private_key(ec.SECP384R1()), "COURBE"),
        )
        for key, code in cases:
            with self.subTest(code=code):
                bad_leaf = _build_leaf(
                    key, chain["interm_key"], chain["interm_der"],
                    "clientAuth", V7_A, None,
                )
                with self.assertRaises(InitialTerminalX509Error) as caught:
                    inspect_initial_terminal_der(
                        bad_leaf, expected_instance_uuid=V7_A,
                        expected_tls_usage="clientAuth", expected_server_ipv4=None,
                    )
                self.assertEqual(caught.exception.code, code)

    def test_attentes_strictes_sur_feuille_valide(self) -> None:
        chain = _chain("serverAuth", V7_A, LOOPBACK)
        class SpoofedStr(str):
            pass
        cases = (
            {"expected_instance_uuid": V7_A.upper()},
            {"expected_instance_uuid": V4_UUID},
            {"expected_instance_uuid": NON_RFC_VARIANT_UUID},
            {"expected_instance_uuid": True},
            {"expected_tls_usage": True},
            {"expected_tls_usage": SpoofedStr("serverAuth")},
            {"expected_server_ipv4": None},
            {"expected_server_ipv4": "192.0.2.1"},
            {"expected_server_ipv4": "::1"},
            {"expected_server_ipv4": SpoofedStr(LOOPBACK)},
            {"expected_server_ipv4": LOOPBACK_OTHER},
        )
        for change in cases:
            with self.subTest(fields=tuple(change)):
                expected: dict[str, Any] = {
                    "expected_instance_uuid": V7_A,
                    "expected_tls_usage": "serverAuth",
                    "expected_server_ipv4": LOOPBACK,
                }
                expected.update(change)
                with self.assertRaises(InitialTerminalX509Error):
                    inspect_initial_terminal_der(chain["leaf_der"], **expected)


if __name__ == "__main__":
    unittest.main()
