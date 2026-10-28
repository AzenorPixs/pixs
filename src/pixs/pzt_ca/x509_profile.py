"""Profil public X509 des CA PZT.

Portée fermée : faits publics DER stricts et vérifications bornées.
Limites : signature/profil/faits publics ne prouvent ni engagement
matériel, ni source A12, ni révocation, ni mandat, ni domaine, ni
contexte courant, ni admission PZT. Engagement durable PostgreSQL
requis pour preuve future. Aucune validation PKIX complète.
Inégalité des clés : contrôle nécessaire, pas preuve d'indépendance.
Cas AlgorithmIdentifier internes/externes et champs adverses signés
valides à qualifier avec bibliothèque appropriée, sans parseur maison.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from cryptography import x509
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509 import (
    DuplicateExtension,
    ExtensionNotFound,
    InvalidVersion,
    UnsupportedGeneralNameType,
)
from cryptography.x509.oid import SignatureAlgorithmOID

Role = Literal["root", "intermediate"]

_ALLOWED_EXTENSION_OIDS = frozenset(
    {
        x509.BasicConstraints.oid,
        x509.KeyUsage.oid,
        x509.SubjectKeyIdentifier.oid,
        x509.AuthorityKeyIdentifier.oid,
    }
)

_EXPECTED_KEY_USAGE = x509.KeyUsage(
    digital_signature=False,
    content_commitment=False,
    key_encipherment=False,
    data_encipherment=False,
    key_agreement=False,
    key_cert_sign=True,
    crl_sign=False,
    encipher_only=False,
    decipher_only=False,
)


class X509ProfileError(ValueError):
    """Erreur de profil à code fixe, sans donnée sensible."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True, repr=False)
class CaCertificateFacts:
    """Faits publics extraits des octets, sans admission."""

    role: str
    subject_rfc4514: str
    issuer_rfc4514: str
    serial_number: int
    not_valid_before_utc: datetime
    not_valid_after_utc: datetime
    public_key_algorithm: str
    curve_name: str
    signature_hash_algorithm: str
    basic_constraints_ca: bool
    basic_constraints_path_length: int | None
    subject_key_identifier: bytes | None
    authority_key_identifier: bytes | None


def _require_der_bytes(value: object) -> bytes:
    if type(value) is not bytes:
        raise X509ProfileError("TYPE_DER")
    if len(value) == 0:
        raise X509ProfileError("DER_VIDE")
    return value


def _require_spki_bytes(value: object) -> bytes:
    if type(value) is not bytes:
        raise X509ProfileError("CLE_ATTENDUE")
    if len(value) == 0:
        raise X509ProfileError("CLE_ATTENDUE")
    return value


def _require_role(value: object) -> Role:
    if type(value) is not str:
        raise X509ProfileError("ROLE")
    if value == "root":
        return "root"
    if value == "intermediate":
        return "intermediate"
    raise X509ProfileError("ROLE")


def _load_strict(raw: bytes) -> x509.Certificate:
    try:
        certificate = x509.load_der_x509_certificate(raw)
    except (ValueError, TypeError, UnsupportedAlgorithm, InvalidVersion, DuplicateExtension):
        raise X509ProfileError("DER_MALFORME") from None
    try:
        reserialised = certificate.public_bytes(serialization.Encoding.DER)
    except (ValueError, TypeError):
        raise X509ProfileError("DER_STRICT") from None
    if type(reserialised) is not bytes:
        raise X509ProfileError("DER_STRICT")
    if reserialised != raw:
        raise X509ProfileError("DER_STRICT")
    return certificate


def _check_version(certificate: x509.Certificate) -> None:
    if certificate.version != x509.Version.v3:
        raise X509ProfileError("VERSION")


def _check_signature_algorithm(certificate: x509.Certificate) -> None:
    try:
        oid = certificate.signature_algorithm_oid
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise X509ProfileError("ALGORITHME") from None
    if oid != SignatureAlgorithmOID.ECDSA_WITH_SHA256:
        raise X509ProfileError("ALGORITHME")
    try:
        hash_algorithm = certificate.signature_hash_algorithm
    except UnsupportedAlgorithm:
        raise X509ProfileError("ALGORITHME") from None
    if not isinstance(hash_algorithm, hashes.SHA256):
        raise X509ProfileError("ALGORITHME")


def _check_public_key(
    certificate: x509.Certificate,
) -> ec.EllipticCurvePublicKey:
    try:
        public_key = certificate.public_key()
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise X509ProfileError("CLE_PUBLIQUE") from None
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise X509ProfileError("CLE_PUBLIQUE")
    if not isinstance(public_key.curve, ec.SECP256R1):
        raise X509ProfileError("COURBE")
    return public_key


def _check_names(certificate: x509.Certificate) -> None:
    try:
        subject_empty = len(certificate.subject.rdns) == 0
        issuer_empty = len(certificate.issuer.rdns) == 0
    except (ValueError, TypeError, UnsupportedGeneralNameType):
        raise X509ProfileError("NOM") from None
    if subject_empty:
        raise X509ProfileError("NOM")
    if issuer_empty:
        raise X509ProfileError("NOM")


def _check_dates(
    certificate: x509.Certificate,
) -> tuple[datetime, datetime]:
    try:
        not_before = certificate.not_valid_before_utc
        not_after = certificate.not_valid_after_utc
    except (ValueError, TypeError):
        raise X509ProfileError("DATES") from None
    if not_before.tzinfo is None:
        raise X509ProfileError("DATES")
    if not_after.tzinfo is None:
        raise X509ProfileError("DATES")
    if not not_before < not_after:
        raise X509ProfileError("DATES")
    return not_before, not_after


def _check_serial(certificate: x509.Certificate) -> None:
    serial = certificate.serial_number
    if not isinstance(serial, int):
        raise X509ProfileError("SERIE")
    if serial <= 0:
        raise X509ProfileError("SERIE")
    # Positif sur 160 bits tient en 20 octets, mais 160 bits avec
    # bit fort à 1 exige un octet de signe DER, soit 21 octets.
    # La borne sûre RFC5280 retenue est donc 159 bits.
    if serial.bit_length() > 159:
        raise X509ProfileError("SERIE")


def _check_extensions(
    certificate: x509.Certificate,
    *,
    role: Role,
    public_key: ec.EllipticCurvePublicKey,
) -> tuple[bytes | None, bytes | None]:
    try:
        extensions = certificate.extensions
    except (DuplicateExtension, ValueError, UnsupportedGeneralNameType):
        raise X509ProfileError("EXTENSION") from None
    for extension in extensions:
        if extension.oid not in _ALLOWED_EXTENSION_OIDS:
            raise X509ProfileError("EXTENSION")
    try:
        basic_constraints = extensions.get_extension_for_oid(
            x509.BasicConstraints.oid
        )
    except ExtensionNotFound:
        raise X509ProfileError("EXTENSION_MANQUANTE") from None
    except DuplicateExtension:
        raise X509ProfileError("EXTENSION") from None
    try:
        key_usage = extensions.get_extension_for_oid(x509.KeyUsage.oid)
    except ExtensionNotFound:
        raise X509ProfileError("EXTENSION_MANQUANTE") from None
    except DuplicateExtension:
        raise X509ProfileError("EXTENSION") from None
    try:
        subject_key = extensions.get_extension_for_oid(
            x509.SubjectKeyIdentifier.oid
        )
    except ExtensionNotFound:
        raise X509ProfileError("EXTENSION_MANQUANTE") from None
    except DuplicateExtension:
        raise X509ProfileError("EXTENSION") from None
    if basic_constraints.critical is not True:
        raise X509ProfileError("CONTRAINTES")
    constraints_value = basic_constraints.value
    if constraints_value.ca is not True:
        raise X509ProfileError("CONTRAINTES")
    expected_path_length = 1 if role == "root" else 0
    if constraints_value.path_length != expected_path_length:
        raise X509ProfileError("CONTRAINTES")
    if key_usage.critical is not True:
        raise X509ProfileError("USAGE")
    # Comparaison entière sans lecture conditionnelle
    # encipher_only/decipher_only, qui lève ValueError quand
    # key_agreement est False. Évite le rejet d'un profil valide.
    if key_usage.value != _EXPECTED_KEY_USAGE:
        raise X509ProfileError("USAGE")
    if subject_key.critical is True:
        raise X509ProfileError("SKI_AKI")
    try:
        expected_ski = x509.SubjectKeyIdentifier.from_public_key(
            public_key
        ).digest
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise X509ProfileError("SKI_AKI") from None
    subject_identifier = subject_key.value.digest
    if type(subject_identifier) is not bytes:
        raise X509ProfileError("SKI_AKI")
    if subject_identifier != expected_ski:
        raise X509ProfileError("SKI_AKI")
    try:
        authority_key = extensions.get_extension_for_oid(
            x509.AuthorityKeyIdentifier.oid
        )
    except ExtensionNotFound:
        if role == "intermediate":
            raise X509ProfileError("SKI_AKI") from None
        return subject_identifier, None
    except DuplicateExtension:
        raise X509ProfileError("EXTENSION") from None
    if authority_key.critical is True:
        raise X509ProfileError("SKI_AKI")
    authority_identifier = authority_key.value.key_identifier
    if authority_identifier is None:
        raise X509ProfileError("SKI_AKI")
    if type(authority_identifier) is not bytes:
        raise X509ProfileError("SKI_AKI")
    if len(authority_identifier) == 0:
        raise X509ProfileError("SKI_AKI")
    return subject_identifier, authority_identifier


def inspect_ca_der(der: bytes, *, role: str) -> CaCertificateFacts:
    """Inspecte des octets DER stricts pour le rôle fermé demandé."""
    raw = _require_der_bytes(der)
    checked_role = _require_role(role)
    certificate = _load_strict(raw)
    _check_version(certificate)
    _check_signature_algorithm(certificate)
    public_key = _check_public_key(certificate)
    _check_names(certificate)
    _check_serial(certificate)
    not_before, not_after = _check_dates(certificate)
    ski, aki = _check_extensions(
        certificate, role=checked_role, public_key=public_key
    )
    try:
        subject_text = certificate.subject.rfc4514_string()
        issuer_text = certificate.issuer.rfc4514_string()
    except (ValueError, TypeError, UnsupportedGeneralNameType):
        raise X509ProfileError("NOM") from None
    try:
        constraints = certificate.extensions.get_extension_for_oid(
            x509.BasicConstraints.oid
        ).value
    except (ExtensionNotFound, DuplicateExtension, ValueError):
        raise X509ProfileError("EXTENSION") from None
    return CaCertificateFacts(
        role=checked_role,
        subject_rfc4514=subject_text,
        issuer_rfc4514=issuer_text,
        serial_number=certificate.serial_number,
        not_valid_before_utc=not_before,
        not_valid_after_utc=not_after,
        public_key_algorithm="EC",
        curve_name="secp256r1",
        signature_hash_algorithm="sha256",
        basic_constraints_ca=True,
        basic_constraints_path_length=constraints.path_length,
        subject_key_identifier=ski,
        authority_key_identifier=aki,
    )


def _load_expected_public_key(
    spki_der: bytes,
) -> ec.EllipticCurvePublicKey:
    raw = _require_spki_bytes(spki_der)
    try:
        public_key = serialization.load_der_public_key(raw)
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise X509ProfileError("CLE_ATTENDUE") from None
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise X509ProfileError("CLE_ATTENDUE")
    if not isinstance(public_key.curve, ec.SECP256R1):
        raise X509ProfileError("CLE_ATTENDUE")
    # N'accepte qu'un SubjectPublicKeyInfo exact, sans autre
    # format ni suffixe.
    try:
        reserialised = public_key.public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise X509ProfileError("CLE_ATTENDUE") from None
    if type(reserialised) is not bytes:
        raise X509ProfileError("CLE_ATTENDUE")
    if reserialised != raw:
        raise X509ProfileError("CLE_ATTENDUE")
    return public_key


def verify_root_self_signature(
    der: bytes, *, expected_public_key_spki_der: bytes
) -> CaCertificateFacts:
    """Vérifie une racine auto-signée contre le matériau public attendu."""
    raw = _require_der_bytes(der)
    expected_key = _load_expected_public_key(expected_public_key_spki_der)
    facts = inspect_ca_der(raw, role="root")
    certificate = _load_strict(raw)
    if certificate.issuer != certificate.subject:
        raise X509ProfileError("EMETTEUR")
    actual_key = _check_public_key(certificate)
    expected_numbers = expected_key.public_numbers()
    actual_numbers = actual_key.public_numbers()
    if (
        expected_numbers.x != actual_numbers.x
        or expected_numbers.y != actual_numbers.y
    ):
        raise X509ProfileError("CLE_ATTENDUE")
    if facts.authority_key_identifier is not None:
        if facts.subject_key_identifier is None:
            raise X509ProfileError("SKI_AKI")
        if facts.authority_key_identifier != facts.subject_key_identifier:
            raise X509ProfileError("SKI_AKI")
    try:
        expected_key.verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            ec.ECDSA(hashes.SHA256()),
        )
    except InvalidSignature:
        raise X509ProfileError("SIGNATURE") from None
    return facts


def verify_intermediate_issued(
    intermediate_der: bytes,
    *,
    issuer_der: bytes,
    expected_issuer_spki_der: bytes,
    expected_intermediate_spki_der: bytes,
) -> tuple[CaCertificateFacts, CaCertificateFacts]:
    """Vérifie un lien intermédiaire contre deux matériaux attendus.

    Exige le matériau intermédiaire attendu en plus de la racine,
    sinon tout frère valide sous la racine passerait. Ne prouve pas
    la provenance autoritative des matériaux comparés.
    """
    raw_intermediate = _require_der_bytes(intermediate_der)
    raw_issuer = _require_der_bytes(issuer_der)
    expected_issuer_key = _load_expected_public_key(expected_issuer_spki_der)
    expected_intermediate_key = _load_expected_public_key(
        expected_intermediate_spki_der
    )
    issuer_facts = verify_root_self_signature(
        raw_issuer, expected_public_key_spki_der=expected_issuer_spki_der
    )
    intermediate_facts = inspect_ca_der(raw_intermediate, role="intermediate")
    issuer_certificate = _load_strict(raw_issuer)
    intermediate_certificate = _load_strict(raw_intermediate)
    if intermediate_certificate.issuer != issuer_certificate.subject:
        raise X509ProfileError("EMETTEUR")
    issuer_public_key = _check_public_key(issuer_certificate)
    intermediate_public_key = _check_public_key(intermediate_certificate)
    expected_issuer_numbers = expected_issuer_key.public_numbers()
    issuer_numbers = issuer_public_key.public_numbers()
    if (
        expected_issuer_numbers.x != issuer_numbers.x
        or expected_issuer_numbers.y != issuer_numbers.y
    ):
        raise X509ProfileError("CLE_ATTENDUE")
    expected_intermediate_numbers = (
        expected_intermediate_key.public_numbers()
    )
    intermediate_numbers = intermediate_public_key.public_numbers()
    if (
        expected_intermediate_numbers.x != intermediate_numbers.x
        or expected_intermediate_numbers.y != intermediate_numbers.y
    ):
        raise X509ProfileError("CLE_ATTENDUE")
    if issuer_facts.subject_key_identifier is None:
        raise X509ProfileError("SKI_AKI")
    if intermediate_facts.authority_key_identifier is None:
        raise X509ProfileError("SKI_AKI")
    if (
        intermediate_facts.authority_key_identifier
        != issuer_facts.subject_key_identifier
    ):
        raise X509ProfileError("SKI_AKI")
    if (
        intermediate_numbers.x == issuer_numbers.x
        and intermediate_numbers.y == issuer_numbers.y
    ):
        raise X509ProfileError("CLE_DISTINCTE")
    try:
        issuer_public_key.verify(
            intermediate_certificate.signature,
            intermediate_certificate.tbs_certificate_bytes,
            ec.ECDSA(hashes.SHA256()),
        )
    except InvalidSignature:
        raise X509ProfileError("SIGNATURE") from None
    return intermediate_facts, issuer_facts
