"""Certificat CA public, structure seule et comparaison bornée.

Portée exacte : `z12.ca_certificate/v1` (§5.2).
Réutilise helpers internes `ca_identity` et fonctions existantes
`x509_profile` sans recopier la crypto. Structure seule, sans
autorisation, sans preuve d'ancrage, de registre ou d'unicité.
Référence opaque seule ne prouve rien. Aucun bool verified fabriqué.
Empreinte technique SHA256 via `cryptography` admise, sans changer
les références publiques ni créer une norme.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any, Protocol

from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_bounded_keys as _base_check_keys
from pixs.pzt_ca.ca_identity import _is_utc_instant as _base_is_utc
from pixs.pzt_ca.ca_identity import _parse_rfc3339_utc as _base_parse_time
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads
from pixs.pzt_ca import x509_profile as _x509
from pixs.pzt_ca.x509_profile import X509ProfileError
from cryptography.hazmat.primitives import hashes

__all__ = [
    "CaCertificateError",
    "CaCertificateResolutionError",
    "CaCertificate",
    "CertificatePublicBinding",
    "CertificateOwnerBindings",
    "CERT_OBJECT",
    "SCHEMA_VERSION",
    "certificate_from_mapping",
    "certificate_from_json",
    "extract_verified_facts",
    "check_bytes_consistency",
]

SCHEMA_VERSION = "1.0.0"
CERT_OBJECT = "z12.ca_certificate/v1"

CA_KINDS = ("root", "intermediate")

_CERT_REQUIRED = frozenset({
    "object_type", "schema_version", "cert_ref", "cert_bytes_ref",
    "ca_kind", "root_authority_ref", "subject_key_ref",
    "generation_ref", "basic_constraints_critical",
    "key_usage_critical", "is_ca", "path_len", "key_usage",
    "signature_algorithm", "curve", "serial_public",
    "not_before_utc", "not_after_utc", "fingerprint_public",
    "subject_key_id", "anchor_ref",
})
_CERT_ALLOWED = frozenset({
    "object_type", "schema_version", "cert_ref", "cert_bytes_ref",
    "ca_kind", "root_authority_ref", "subject_key_ref",
    "generation_ref", "issuer_ref",
    "basic_constraints_critical",
    "key_usage_critical", "is_ca", "path_len", "key_usage",
    "signature_algorithm", "curve", "serial_public",
    "not_before_utc", "not_after_utc", "fingerprint_public",
    "authority_key_id", "subject_key_id", "anchor_ref",
})


class CaCertificateError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


class CaCertificateResolutionError(ValueError):
    """Échec de résolution sans contenu externe."""

    def __init__(self, element: str) -> None:
        super().__init__(f"{element} : RESOLUTION_IMPOSSIBLE")
        self.code = "RESOLUTION_IMPOSSIBLE"
        self.element = element
        self.step = "resolve_binding"


def _deny(code: str, element: str) -> CaCertificateError:
    return CaCertificateError(code, element)


def _deny_resolution(element: str) -> CaCertificateResolutionError:
    return CaCertificateResolutionError(element)


def _req_ref(value: object, element: str) -> None:
    try:
        _base_require_ref(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_ver(value: object, element: str) -> None:
    try:
        _base_require_ver(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_enum(value: object, expected: tuple[str, ...], element: str) -> None:
    try:
        _base_require_enum(value, expected, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _parse_time(value: object, element: str) -> datetime.datetime:
    try:
        return _base_parse_time(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _loads_mapping(text: object) -> dict[str, Any]:
    try:
        mapping = _base_loads(text)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping")
    return mapping


def _check_keys(mapping: dict[str, Any]) -> None:
    try:
        _base_check_keys(mapping, _CERT_REQUIRED, _CERT_ALLOWED)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _require_true_bool(value: object, element: str) -> None:
    if type(value) is not bool or value is not True:
        raise _deny("BOOL_VRAI_REQUIS", element)


def _require_path_len(value: object, element: str) -> None:
    if type(value) is not int or value not in (0, 1):
        raise _deny("PATH_LEN_INVALIDE", element)


def _require_key_usage_list(value: object, element: str) -> None:
    if type(value) is not list:
        raise _deny("USAGE_INVALIDE", element)
    if len(value) != 1:
        raise _deny("USAGE_INVALIDE", element)
    item = value[0]
    if type(item) is not str or item != "keyCertSign":
        raise _deny("USAGE_INVALIDE", element)


def _sha256_technical(data: bytes) -> bytes:
    h = hashes.Hash(hashes.SHA256())
    h.update(data)
    return h.finalize()


@dataclass(frozen=True, slots=True, repr=False)
class CertificatePublicBinding:
    """Faits publics liés, résolution atomique au propriétaire réel."""

    cert_ref: str
    cert_bytes_ref: str
    ca_kind: str
    root_authority_ref: str
    subject_key_ref: str
    generation_ref: str
    issuer_ref: str | None
    anchor_ref: str
    serial_public: str
    fingerprint_public: str
    subject_key_id: str
    authority_key_id: str | None
    certificate_der: bytes
    root_der: bytes
    subject_spki_der: bytes
    root_spki_der: bytes
    serial_number: int
    fingerprint_sha256: bytes
    ski: bytes
    aki: bytes | None

    def __post_init__(self) -> None:
        try:
            _base_require_ref(self.cert_ref, "certificate_binding.cert_ref")
            _base_require_ref(self.cert_bytes_ref, "certificate_binding.cert_bytes_ref")
            _base_require_enum(self.ca_kind, CA_KINDS, "certificate_binding.ca_kind")
            _base_require_ref(self.root_authority_ref, "certificate_binding.root_authority_ref")
            _base_require_ref(self.subject_key_ref, "certificate_binding.subject_key_ref")
            _base_require_ref(self.generation_ref, "certificate_binding.generation_ref")
            _base_require_ref(self.anchor_ref, "certificate_binding.anchor_ref")
            _base_require_ref(self.serial_public, "certificate_binding.serial_public")
            _base_require_ref(self.fingerprint_public, "certificate_binding.fingerprint_public")
            _base_require_ref(self.subject_key_id, "certificate_binding.subject_key_id")
            if self.ca_kind == "root":
                if self.issuer_ref is not None:
                    raise _deny_resolution("certificate_binding.issuer_ref")
                if self.authority_key_id is not None:
                    _base_require_ref(self.authority_key_id, "certificate_binding.authority_key_id")
            else:
                _base_require_ref(self.issuer_ref, "certificate_binding.issuer_ref")
                if self.authority_key_id is None:
                    raise _deny_resolution("certificate_binding.authority_key_id")
                _base_require_ref(self.authority_key_id, "certificate_binding.authority_key_id")
        except CaCertificateResolutionError:
            raise
        except _CaIdentityError as exc:
            raise _deny_resolution(exc.element) from None
        if type(self.certificate_der) is not bytes or len(self.certificate_der) == 0:
            raise _deny_resolution("certificate_binding.certificate_der")
        if type(self.root_der) is not bytes or len(self.root_der) == 0:
            raise _deny_resolution("certificate_binding.root_der")
        if type(self.subject_spki_der) is not bytes or len(self.subject_spki_der) == 0:
            raise _deny_resolution("certificate_binding.subject_spki_der")
        if type(self.root_spki_der) is not bytes or len(self.root_spki_der) == 0:
            raise _deny_resolution("certificate_binding.root_spki_der")
        if type(self.serial_number) is not int or self.serial_number <= 0:
            raise _deny_resolution("certificate_binding.serial_number")
        if type(self.fingerprint_sha256) is not bytes or len(self.fingerprint_sha256) != 32:
            raise _deny_resolution("certificate_binding.fingerprint_sha256")
        if type(self.ski) is not bytes or len(self.ski) == 0:
            raise _deny_resolution("certificate_binding.ski")
        if self.aki is not None:
            if type(self.aki) is not bytes or len(self.aki) == 0:
                raise _deny_resolution("certificate_binding.aki")


class CertificateOwnerBindings(Protocol):
    """Résolution propriétaire des références opaques vers faits typés.

    Le resolveur doit convertir ses absences attendues en
    CaCertificateResolutionError ; seul ce type est normalise,
    les autres erreurs se propagent.
    """

    def resolve_certificate(self, cert_ref: str) -> CertificatePublicBinding: ...


@dataclass(frozen=True, slots=True, repr=False)
class CaCertificate:
    """Métadonnées publiques non preuves, vérifiées sur octets séparément."""

    object_type: str
    schema_version: str
    cert_ref: str
    cert_bytes_ref: str
    ca_kind: str
    root_authority_ref: str
    subject_key_ref: str
    generation_ref: str
    basic_constraints_critical: bool
    key_usage_critical: bool
    is_ca: bool
    path_len: int
    key_usage: tuple[str, ...]
    signature_algorithm: str
    curve: str
    serial_public: str
    not_before_utc: datetime.datetime
    not_after_utc: datetime.datetime
    fingerprint_public: str
    subject_key_id: str
    anchor_ref: str
    issuer_ref: str | None = None
    authority_key_id: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        ot = current(self, "object_type")
        if type(ot) is not str:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_certificate.object_type")
        if ot != CERT_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_certificate.object_type")
        _req_ver(current(self, "schema_version"), "ca_certificate.schema_version")
        for name in (
            "cert_ref", "cert_bytes_ref", "root_authority_ref",
            "subject_key_ref", "generation_ref", "serial_public",
            "fingerprint_public", "subject_key_id", "anchor_ref",
        ):
            _req_ref(current(self, name), f"ca_certificate.{name}")
        _req_enum(current(self, "ca_kind"), CA_KINDS, "ca_certificate.ca_kind")
        _require_true_bool(
            current(self, "basic_constraints_critical"),
            "ca_certificate.basic_constraints_critical",
        )
        _require_true_bool(
            current(self, "key_usage_critical"),
            "ca_certificate.key_usage_critical",
        )
        _require_true_bool(current(self, "is_ca"), "ca_certificate.is_ca")
        _require_path_len(current(self, "path_len"), "ca_certificate.path_len")
        ku = current(self, "key_usage")
        if type(ku) is not tuple or len(ku) != 1:
            raise _deny("USAGE_INVALIDE", "ca_certificate.key_usage")
        if type(ku[0]) is not str or ku[0] != "keyCertSign":
            raise _deny("USAGE_INVALIDE", "ca_certificate.key_usage")
        _req_enum(
            current(self, "signature_algorithm"),
            ("ecdsa-with-SHA256",),
            "ca_certificate.signature_algorithm",
        )
        _req_enum(
            current(self, "curve"), ("secp256r1",),
            "ca_certificate.curve",
        )
        if not _base_is_utc(current(self, "not_before_utc")):
            raise _deny("HORODATAGE_NON_UTC", "ca_certificate.not_before_utc")
        if not _base_is_utc(current(self, "not_after_utc")):
            raise _deny("HORODATAGE_NON_UTC", "ca_certificate.not_after_utc")
        if not current(self, "not_before_utc") < current(self, "not_after_utc"):
            raise _deny("DATES_INCOHERENTES", "ca_certificate.validite")
        kind = current(self, "ca_kind")
        issuer = current(self, "issuer_ref")
        aki = current(self, "authority_key_id")
        if kind == "root":
            if issuer is not None:
                raise _deny("EMETTEUR_INTERDIT", "ca_certificate.issuer_ref")
            if current(self, "path_len") != 1:
                raise _deny("CONTRAINTES_INCOHERENTES", "ca_certificate.path_len")
            if aki is not None:
                _req_ref(aki, "ca_certificate.authority_key_id")
        else:
            if issuer is None:
                raise _deny("EMETTEUR_REQUIS", "ca_certificate.issuer_ref")
            _req_ref(issuer, "ca_certificate.issuer_ref")
            if current(self, "path_len") != 0:
                raise _deny("CONTRAINTES_INCOHERENTES", "ca_certificate.path_len")
            if aki is None:
                raise _deny("SKI_AKI_REQUIS", "ca_certificate.authority_key_id")
            _req_ref(aki, "ca_certificate.authority_key_id")


def certificate_from_mapping(mapping: dict[str, Any]) -> CaCertificate:
    """Construit depuis un dictionnaire strict déjà analysé."""
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_certificate")
    _check_keys(mapping)
    _require_key_usage_list(mapping["key_usage"], "ca_certificate.key_usage")
    ku_tuple = (mapping["key_usage"][0],)
    return CaCertificate(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        cert_ref=mapping["cert_ref"],
        cert_bytes_ref=mapping["cert_bytes_ref"],
        ca_kind=mapping["ca_kind"],
        root_authority_ref=mapping["root_authority_ref"],
        subject_key_ref=mapping["subject_key_ref"],
        generation_ref=mapping["generation_ref"],
        basic_constraints_critical=mapping["basic_constraints_critical"],
        key_usage_critical=mapping["key_usage_critical"],
        is_ca=mapping["is_ca"],
        path_len=mapping["path_len"],
        key_usage=ku_tuple,
        signature_algorithm=mapping["signature_algorithm"],
        curve=mapping["curve"],
        serial_public=mapping["serial_public"],
        not_before_utc=_parse_time(
            mapping["not_before_utc"], "ca_certificate.not_before_utc"
        ),
        not_after_utc=_parse_time(
            mapping["not_after_utc"], "ca_certificate.not_after_utc"
        ),
        fingerprint_public=mapping["fingerprint_public"],
        subject_key_id=mapping["subject_key_id"],
        anchor_ref=mapping["anchor_ref"],
        issuer_ref=mapping.get("issuer_ref"),
        authority_key_id=mapping.get("authority_key_id"),
    )


def certificate_from_json(text: object) -> CaCertificate:
    """Analyse JSON strict puis construit, sans normalisation."""
    return certificate_from_mapping(_loads_mapping(text))


def extract_verified_facts(
    der: bytes,
    issuer_der: bytes | None,
    expected_issuer_spki_der: bytes | None,
    expected_subject_spki_der: bytes | None,
    ca_kind: str,
) -> _x509.CaCertificateFacts:
    """Retourne faits vérifiés seuls, portée cryptographique.

    Vérifie les octets réels via `x509_profile` existant avec SPKI
    publics attendus. Ne compare aucune référence déclarée. Seule
    `X509ProfileError` est convertie ; erreurs inattendues propagées.
    """
    _req_enum(ca_kind, CA_KINDS, "ca_kind")
    try:
        if ca_kind == "root":
            if not isinstance(expected_subject_spki_der, bytes):
                raise CaCertificateError("MANQUANT", "materiau_attendu")
            return _x509.verify_root_self_signature(
                der,
                expected_public_key_spki_der=expected_subject_spki_der,
            )
        if (
            not isinstance(issuer_der, bytes)
            or not isinstance(expected_issuer_spki_der, bytes)
            or not isinstance(expected_subject_spki_der, bytes)
        ):
            raise CaCertificateError("MANQUANT", "materiau_attendu")
        pair = _x509.verify_intermediate_issued(
            der,
            issuer_der=issuer_der,
            expected_issuer_spki_der=expected_issuer_spki_der,
            expected_intermediate_spki_der=expected_subject_spki_der,
        )
        return pair[0]
    except X509ProfileError as exc:
        raise CaCertificateError(exc.code, "cert_bytes") from None


def check_bytes_consistency(
    declared: object,
    bindings: CertificateOwnerBindings,
) -> _x509.CaCertificateFacts:
    """Compare le record lié aux déclarations puis aux octets.

    Exige type exact `CaCertificate`, résout le binding atomique par
    `resolve_certificate`, exige type exact `CertificatePublicBinding`,
    compare toutes les références du record lié à celles déclarées,
    extrait et vérifie octets et SPKI via `x509_profile`, impose
    `certificate_der == root_der` pour racine, compare dates, profil,
    série, empreinte SHA256 technique, SKI et AKI. Présence et absence
    AKI déclarées égales aux faits. Retourne faits crypto seuls, sans
    admission, sans ancrage courant, sans autorité, sans registre.
    Registre, ancrage provisionné et unicité restent atomiques aux
    vrais services ultérieurs.
    """
    if type(declared) is not CaCertificate:
        raise CaCertificateError("TYPE_INVALIDE", "ca_certificate")
    if bindings is None:
        raise CaCertificateResolutionError("bindings")
    resolve = getattr(bindings, "resolve_certificate", None)
    if not callable(resolve):
        raise CaCertificateResolutionError("bindings")
    try:
        linked = resolve(declared.cert_ref)
    except CaCertificateResolutionError as exc:
        raise CaCertificateResolutionError("bindings") from None
    if type(linked) is not CertificatePublicBinding:
        raise CaCertificateResolutionError("bindings")
    for field_name in (
        "cert_ref",
        "cert_bytes_ref",
        "ca_kind",
        "root_authority_ref",
        "subject_key_ref",
        "generation_ref",
        "issuer_ref",
        "anchor_ref",
        "serial_public",
        "fingerprint_public",
        "subject_key_id",
        "authority_key_id",
    ):
        if getattr(linked, field_name) != getattr(declared, field_name):
            raise CaCertificateError("REFERENCE_INCOHERENTE", f"ca_certificate.{field_name}")
    if declared.ca_kind == "root":
        if linked.certificate_der != linked.root_der:
            raise CaCertificateError("RACINE_INCOHERENTE", "ca_certificate.cert_bytes_ref")
        if linked.root_spki_der != linked.subject_spki_der:
            raise CaCertificateError("RACINE_INCOHERENTE", "ca_certificate.subject_key_ref")
        facts = extract_verified_facts(
            linked.certificate_der,
            None,
            None,
            linked.subject_spki_der,
            linked.ca_kind,
        )
    else:
        facts = extract_verified_facts(
            linked.certificate_der,
            linked.root_der,
            linked.root_spki_der,
            linked.subject_spki_der,
            linked.ca_kind,
        )
    if facts.role != declared.ca_kind:
        raise CaCertificateError("ROLE_INCOHERENT", "ca_certificate.ca_kind")
    if facts.not_valid_before_utc != declared.not_before_utc:
        raise CaCertificateError("DATES_INCOHERENTES", "ca_certificate.not_before_utc")
    if facts.not_valid_after_utc != declared.not_after_utc:
        raise CaCertificateError("DATES_INCOHERENTES", "ca_certificate.not_after_utc")
    if facts.signature_hash_algorithm != "sha256":
        raise CaCertificateError("ALGORITHME_INCOHERENT", "ca_certificate.signature_algorithm")
    if facts.public_key_algorithm != "EC" or facts.curve_name != "secp256r1":
        raise CaCertificateError("CLE_INCOHERENTE", "ca_certificate.curve")
    if facts.basic_constraints_ca is not True:
        raise CaCertificateError("CONTRAINTES_INCOHERENTES", "ca_certificate.is_ca")
    expected_path = 1 if declared.ca_kind == "root" else 0
    if facts.basic_constraints_path_length != expected_path:
        raise CaCertificateError("CONTRAINTES_INCOHERENTES", "ca_certificate.path_len")
    if facts.serial_number != linked.serial_number:
        raise CaCertificateError("SERIE_INCOHERENTE", "ca_certificate.serial_public")
    try:
        tech_fp = _sha256_technical(linked.certificate_der)
    except (ValueError, TypeError):
        raise CaCertificateError("EMPREINTE_IMPOSSIBLE", "ca_certificate.cert_bytes_ref") from None
    if linked.fingerprint_sha256 != tech_fp:
        raise CaCertificateError("EMPREINTE_INCOHERENTE", "ca_certificate.fingerprint_public")
    if facts.subject_key_identifier != linked.ski:
        raise CaCertificateError("SKI_INCOHERENT", "ca_certificate.subject_key_id")
    declared_has_aki = declared.authority_key_id is not None
    linked_has_aki = linked.aki is not None
    facts_has_aki = facts.authority_key_identifier is not None
    if declared_has_aki != facts_has_aki or linked_has_aki != facts_has_aki:
        raise CaCertificateError("AKI_INCOHERENT", "ca_certificate.authority_key_id")
    if facts_has_aki and linked.aki != facts.authority_key_identifier:
        raise CaCertificateError("AKI_INCOHERENT", "ca_certificate.authority_key_id")
    return facts
