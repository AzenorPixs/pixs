"""Contrôles X.509 terminaux initiaux D7, sans autorité ni admission.

Portée : profil feuille §D7, 6 extensions fermées, Subject vide.
Réutilise `x509_profile` réel sans le modifier :
`_load_strict`, `_check_version`, `_check_signature_algorithm`,
`_check_public_key`, `_check_serial`, `_check_dates`,
`_load_expected_public_key`, `verify_intermediate_issued`.
Aucun signataire, admission, loader TLS, parseur ASN.1 maison,
plafond 24h, borne de début, horloge, hardware, possession,
fraîcheur, révocation, politique ou PKIX complet.
"""

from __future__ import annotations

import datetime
import ipaddress
import uuid
from dataclasses import dataclass

from cryptography import x509
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.x509 import (
    DuplicateExtension, ExtensionNotFound, UnsupportedGeneralNameType,
)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID

from pixs.pzt_ca.x509_profile import (
    CaCertificateFacts,
    X509ProfileError as _CaX509Error,
)
from pixs.pzt_ca.x509_profile import _check_dates as _ca_dates
from pixs.pzt_ca.x509_profile import _check_public_key as _ca_key
from pixs.pzt_ca.x509_profile import _check_serial as _ca_serial
from pixs.pzt_ca.x509_profile import _check_signature_algorithm as _ca_algo
from pixs.pzt_ca.x509_profile import _check_version as _ca_version
from pixs.pzt_ca.x509_profile import _load_expected_public_key as _ca_spki
from pixs.pzt_ca.x509_profile import _load_strict as _ca_load
from pixs.pzt_ca.x509_profile import (
    verify_intermediate_issued as _ca_verify_chain,
)

__all__ = [
    "InitialTerminalX509Error",
    "InitialTerminalFacts",
    "inspect_initial_terminal_der",
    "verify_initial_terminal_issued",
    "assert_terminal_pair_distinct",
]

TLS_USAGE = ("clientAuth", "serverAuth")

_ALLOWED_TERMINAL_OIDS = frozenset({
    x509.BasicConstraints.oid,
    x509.KeyUsage.oid,
    x509.SubjectAlternativeName.oid,
    x509.ExtendedKeyUsage.oid,
    x509.SubjectKeyIdentifier.oid,
    x509.AuthorityKeyIdentifier.oid,
})

_EXPECTED_KU = x509.KeyUsage(
    digital_signature=True,
    content_commitment=False,
    key_encipherment=False,
    data_encipherment=False,
    key_agreement=False,
    encipher_only=False,
    decipher_only=False,
    key_cert_sign=False,
    crl_sign=False,
)

_CLIENT_EKU = ExtendedKeyUsageOID.CLIENT_AUTH
_SERVER_EKU = ExtendedKeyUsageOID.SERVER_AUTH


class InitialTerminalX509Error(ValueError):
    """Refus profil/signature à code fixe, sans donnée sensible."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _deny(code: str) -> InitialTerminalX509Error:
    return InitialTerminalX509Error(code)


def _req_exact_str(value: object, code: str) -> str:
    if type(value) is not str:
        raise _deny(code)
    return value


def _req_uuid(value: object) -> str:
    text = _req_exact_str(value, "UUID_INVALIDE")
    try:
        parsed = uuid.UUID(text)
    except ValueError:
        raise _deny("UUID_INVALIDE") from None
    if parsed.variant != uuid.RFC_4122:
        raise _deny("UUID_VARIANTE_INVALIDE")
    if parsed.version != 7:
        raise _deny("UUID_VERSION_INVALIDE")
    if str(parsed) != text:
        raise _deny("UUID_NON_CANONIQUE")
    return text


def _req_ip(value: object) -> str:
    text = _req_exact_str(value, "IP_INVALIDE")
    try:
        addr = ipaddress.IPv4Address(text)
    except ipaddress.AddressValueError:
        raise _deny("IP_INVALIDE") from None
    if str(addr) != text:
        raise _deny("IP_NON_CANONIQUE")
    if not addr.is_loopback:
        raise _deny("IP_NON_LOOPBACK")
    return text


def _require_der(value: object) -> bytes:
    if type(value) is not bytes:
        raise _deny("TYPE_DER")
    if len(value) == 0:
        raise _deny("DER_VIDE")
    return value


def _load(raw: bytes) -> x509.Certificate:
    try:
        return _ca_load(raw)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None


@dataclass(frozen=True, slots=True, repr=False)
class InitialTerminalFacts:
    """Faits publics feuille, sans admission."""

    serial_number: int
    not_valid_before_utc: datetime.datetime
    not_valid_after_utc: datetime.datetime
    instance_uuid: str
    tls_usage: str
    server_ipv4: str | None
    subject_rfc4514: str
    issuer_rfc4514: str
    subject_key_identifier: bytes
    authority_key_identifier: bytes


def _check_subject_issuer(
    certificate: x509.Certificate,
) -> tuple[str, str]:
    try:
        subject_empty = len(certificate.subject.rdns) == 0
        issuer_empty = len(certificate.issuer.rdns) == 0
        subject_text = certificate.subject.rfc4514_string()
        issuer_text = certificate.issuer.rfc4514_string()
    except (ValueError, TypeError, UnsupportedGeneralNameType):
        raise _deny("NOM") from None
    if not subject_empty:
        raise _deny("SUJET_NON_VIDE")
    if issuer_empty:
        raise _deny("EMETTEUR_VIDE")
    return subject_text, issuer_text


def _check_terminal_extensions(
    certificate: x509.Certificate,
    public_key: ec.EllipticCurvePublicKey,
    *,
    expected_uuid: str,
    expected_usage: str,
    expected_ip: str | None,
) -> tuple[bytes, bytes]:
    try:
        extensions = certificate.extensions
    except (DuplicateExtension, ValueError, UnsupportedGeneralNameType):
        raise _deny("EXTENSION") from None
    if len(extensions) != 6:
        raise _deny("EXTENSION_NOMBRE")
    for extension in extensions:
        if extension.oid not in _ALLOWED_TERMINAL_OIDS:
            raise _deny("EXTENSION_ETRANGERE")
    try:
        bc = extensions.get_extension_for_oid(x509.BasicConstraints.oid)
        ku = extensions.get_extension_for_oid(x509.KeyUsage.oid)
        eku = extensions.get_extension_for_oid(
            x509.ExtendedKeyUsage.oid
        )
        san = extensions.get_extension_for_oid(
            x509.SubjectAlternativeName.oid
        )
        ski = extensions.get_extension_for_oid(
            x509.SubjectKeyIdentifier.oid
        )
        aki = extensions.get_extension_for_oid(
            x509.AuthorityKeyIdentifier.oid
        )
    except (ExtensionNotFound, DuplicateExtension):
        raise _deny("EXTENSION_MANQUANTE") from None
    if bc.critical is not True:
        raise _deny("CONTRAINTES_CRITICITE")
    if bc.value.ca is not False:
        raise _deny("CONTRAINTES_CA")
    if bc.value.path_length is not None:
        raise _deny("CONTRAINTES_PATHLEN")
    if ku.critical is not True:
        raise _deny("USAGE_CRITICITE")
    try:
        ku_equal = ku.value == _EXPECTED_KU
    except ValueError:
        raise _deny("USAGE") from None
    if not ku_equal:
        raise _deny("USAGE")
    if eku.critical is not True:
        raise _deny("EKU_CRITICITE")
    wanted = _CLIENT_EKU if expected_usage == "clientAuth" else _SERVER_EKU
    if list(eku.value) != [wanted]:
        raise _deny("EKU")
    if san.critical is not True:
        raise _deny("SAN_CRITICITE")
    names = list(san.value)
    wanted_uri = f"urn:uuid:{expected_uuid}"
    if expected_usage == "clientAuth":
        if len(names) != 1:
            raise _deny("SAN")
        first = names[0]
        if not isinstance(first, x509.UniformResourceIdentifier):
            raise _deny("SAN")
        if first.value != wanted_uri:
            raise _deny("SAN_URI")
    else:
        if len(names) != 2:
            raise _deny("SAN")
        uris = [
            n.value
            for n in names
            if isinstance(n, x509.UniformResourceIdentifier)
        ]
        ips = [n.value for n in names if isinstance(n, x509.IPAddress)]
        if uris != [wanted_uri]:
            raise _deny("SAN_URI")
        if len(ips) != 1 or type(ips[0]) is not ipaddress.IPv4Address:
            raise _deny("SAN_IP")
        if str(ips[0]) != expected_ip:
            raise _deny("SAN_IP")
        if any(not isinstance(n, (x509.UniformResourceIdentifier, x509.IPAddress)) for n in names):
            raise _deny("SAN")
    if ski.critical is not False:
        raise _deny("SKI_CRITICITE")
    try:
        expected_ski = x509.SubjectKeyIdentifier.from_public_key(
            public_key
        ).digest
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise _deny("SKI") from None
    if ski.value.digest != expected_ski:
        raise _deny("SKI")
    if aki.critical is not False:
        raise _deny("AKI_CRITICITE")
    aki_keyid = aki.value.key_identifier
    if aki_keyid is None or type(aki_keyid) is not bytes:
        raise _deny("AKI")
    if len(aki_keyid) == 0:
        raise _deny("AKI")
    return ski.value.digest, aki_keyid


def inspect_initial_terminal_der(
    der: bytes,
    *,
    expected_instance_uuid: str,
    expected_tls_usage: str,
    expected_server_ipv4: str | None,
) -> InitialTerminalFacts:
    """Inspecte une feuille D7 sur octets stricts, sans chaîne."""
    raw = _require_der(der)
    if type(expected_tls_usage) is not str:
        raise _deny("USAGE_ATTENTE")
    if expected_tls_usage not in TLS_USAGE:
        raise _deny("USAGE_ATTENTE")
    uuid_text = _req_uuid(expected_instance_uuid)
    if expected_tls_usage == "serverAuth":
        if expected_server_ipv4 is None:
            raise _deny("IP_ATTENTE_ABSENTE")
        ip_text: str | None = _req_ip(expected_server_ipv4)
    else:
        if expected_server_ipv4 is not None:
            raise _deny("IP_ATTENTE_INTERDITE")
        ip_text = None
    certificate = _load(raw)
    try:
        _ca_version(certificate)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    try:
        _ca_algo(certificate)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    try:
        public_key = _ca_key(certificate)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    try:
        _ca_serial(certificate)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    try:
        not_before, not_after = _ca_dates(certificate)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    subject_text, issuer_text = _check_subject_issuer(certificate)
    ski, aki = _check_terminal_extensions(
        certificate, public_key,
        expected_uuid=uuid_text,
        expected_usage=expected_tls_usage,
        expected_ip=ip_text,
    )
    return InitialTerminalFacts(
        serial_number=certificate.serial_number,
        not_valid_before_utc=not_before,
        not_valid_after_utc=not_after,
        instance_uuid=uuid_text,
        tls_usage=expected_tls_usage,
        server_ipv4=ip_text,
        subject_rfc4514=subject_text,
        issuer_rfc4514=issuer_text,
        subject_key_identifier=ski,
        authority_key_identifier=aki,
    )


def _numbers(
    key: ec.EllipticCurvePublicKey,
) -> tuple[int, int]:
    nums = key.public_numbers()
    return (nums.x, nums.y)


def verify_initial_terminal_issued(
    leaf_der: bytes,
    *,
    intermediate_der: bytes,
    root_der: bytes,
    expected_leaf_spki_der: bytes,
    expected_intermediate_spki_der: bytes,
    expected_root_spki_der: bytes,
    expected_instance_uuid: str,
    expected_tls_usage: str,
    expected_server_ipv4: str | None,
) -> tuple[InitialTerminalFacts, CaCertificateFacts, CaCertificateFacts]:
    """Vérifie feuille D7 contre chaîne D2 réelle et 3 SPKI attendus."""
    leaf_raw = _require_der(leaf_der)
    interm_raw = _require_der(intermediate_der)
    root_raw = _require_der(root_der)
    try:
        chain = _ca_verify_chain(
            interm_raw,
            issuer_der=root_raw,
            expected_issuer_spki_der=expected_root_spki_der,
            expected_intermediate_spki_der=(
                expected_intermediate_spki_der
            ),
        )
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    intermediate_facts, root_facts = chain
    leaf_facts = inspect_initial_terminal_der(
        leaf_raw,
        expected_instance_uuid=expected_instance_uuid,
        expected_tls_usage=expected_tls_usage,
        expected_server_ipv4=expected_server_ipv4,
    )
    try:
        expected_leaf_key = _ca_spki(expected_leaf_spki_der)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    leaf_cert = _load(leaf_raw)
    interm_cert = _load(interm_raw)
    try:
        leaf_key = _ca_key(leaf_cert)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    try:
        interm_key = _ca_key(interm_cert)
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    if _numbers(leaf_key) != _numbers(expected_leaf_key):
        raise _deny("CLE_ATTENDUE")
    try:
        root_key = _ca_key(_load(root_raw))
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    if _numbers(leaf_key) == _numbers(interm_key):
        raise _deny("CLE_REUTILISEE")
    if _numbers(leaf_key) == _numbers(root_key):
        raise _deny("CLE_REUTILISEE")
    if leaf_cert.issuer != interm_cert.subject:
        raise _deny("EMETTEUR")
    if intermediate_facts.subject_key_identifier is None:
        raise _deny("AKI")
    if leaf_facts.authority_key_identifier != (
        intermediate_facts.subject_key_identifier
    ):
        raise _deny("AKI")
    try:
        leaf_aki = leaf_cert.extensions.get_extension_for_oid(
            x509.AuthorityKeyIdentifier.oid
        ).value
    except (ExtensionNotFound, DuplicateExtension, ValueError, UnsupportedGeneralNameType):
        raise _deny("AKI") from None
    auth_issuer = leaf_aki.authority_cert_issuer
    auth_serial = leaf_aki.authority_cert_serial_number
    if auth_issuer is not None or auth_serial is not None:
        if auth_issuer is None or auth_serial is None:
            raise _deny("AKI_INCOHERENT")
        if auth_serial != interm_cert.serial_number:
            raise _deny("AKI_INCOHERENT")
        try:
            expected_issuer_name = interm_cert.issuer
        except (ValueError, TypeError, UnsupportedGeneralNameType):
            raise _deny("EMETTEUR") from None
        issuer_names = list(auth_issuer)
        if not issuer_names:
            raise _deny("AKI_INCOHERENT")
        # Le profil CA D2 n'admet aucun issuerAlternativeName :
        # chaque nom présent doit donc désigner le DN réellement
        # émetteur du certificat intermédiaire (la racine).
        for general in issuer_names:
            if not isinstance(general, x509.DirectoryName):
                raise _deny("AKI_INCOHERENT")
            if general.value != expected_issuer_name:
                raise _deny("AKI_INCOHERENT")
    try:
        interm_key.verify(
            leaf_cert.signature,
            leaf_cert.tbs_certificate_bytes,
            ec.ECDSA(hashes.SHA256()),
        )
    except InvalidSignature:
        raise _deny("SIGNATURE") from None
    return leaf_facts, intermediate_facts, root_facts


def assert_terminal_pair_distinct(
    client_spki_der: bytes,
    server_spki_der: bytes,
) -> None:
    """Vérifie 2 SPKI terminaux distincts, sans prouver source."""
    try:
        client_key = _ca_spki(_require_der(client_spki_der))
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    try:
        server_key = _ca_spki(_require_der(server_spki_der))
    except _CaX509Error as exc:
        raise _deny(exc.code) from None
    if _numbers(client_key) == _numbers(server_key):
        raise _deny("CLE_REUTILISEE")
