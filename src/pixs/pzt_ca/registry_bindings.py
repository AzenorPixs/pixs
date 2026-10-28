"""PZT CA liaisons publiques certificat, lecture atomique seule."""
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connections, transaction

from pixs.pzt_ca.ca_certificate import (
    CertificateOwnerBindings,
    CertificatePublicBinding,
    CaCertificateResolutionError,
)
from pixs.pzt_ca.models import CaCertificate, _require_serial_exact


def _opaque(value: object) -> str:
    if type(value) is not str:
        raise CaCertificateResolutionError("certificate")
    if value == "" or "\x00" in value:
        raise CaCertificateResolutionError("certificate")
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        raise CaCertificateResolutionError("certificate") from None
    return value


def _b(value: object) -> bytes:
    if type(value) is bytes:
        return value
    if type(value) is memoryview:
        return value.tobytes()
    raise CaCertificateResolutionError("certificate")


def _b_opt(value: object) -> bytes | None:
    if value is None:
        return None
    return _b(value)


class DjangoCertificateOwnerBindings(CertificateOwnerBindings):
    def __init__(self, alias: str) -> None:
        _opaque(alias)
        if alias not in connections:
            raise CaCertificateResolutionError("certificate")
        if connections[alias].vendor != "postgresql":
            raise CaCertificateResolutionError("certificate")
        self._alias = alias

    def resolve_certificate(self, cert_ref: str) -> CertificatePublicBinding:
        ref = _opaque(cert_ref)
        alias = self._alias
        try:
            with transaction.atomic(using=alias):
                row = (
                    CaCertificate.objects.using(alias)
                    .select_related(
                        "root",
                        "root__key_material",
                        "intermediate_generation",
                        "intermediate_generation__issuer",
                        "intermediate_generation__key_material",
                        "intermediate_generation__root",
                        "intermediate_generation__root__key_material",
                    )
                    .get(cert_ref=ref)
                )
                row.certificate_der = _b(row.certificate_der)
                row.root_der = _b(row.root_der)
                row.subject_spki_der = _b(row.subject_spki_der)
                row.root_spki_der = _b(row.root_spki_der)
                row.fingerprint_sha256 = _b(row.fingerprint_sha256)
                row.ski = _b(row.ski)
                row.aki = _b_opt(row.aki)
                row.root.key_material.spki_der = _b(row.root.key_material.spki_der)
                try:
                    row.root.key_material.clean()
                    row.root.clean()
                except ValidationError:
                    raise CaCertificateResolutionError("certificate") from None
                serial = _require_serial_exact(row.serial_number)
                if type(row.ca_kind) is not str or row.ca_kind not in ("root", "intermediate"):
                    raise CaCertificateResolutionError("certificate") from None
                if row.ca_kind == "root":
                    root = row.root
                    try:
                        row.clean()
                    except ValidationError:
                        raise CaCertificateResolutionError("certificate") from None
                    true = (
                        CaCertificate.objects.using(alias)
                        .select_related("root")
                        .get(root_id=root.pk, cert_ref=root.root_cert_ref, ca_kind="root")
                    )
                    true.certificate_der = _b(true.certificate_der)
                    if row.root_der != true.certificate_der:
                        raise CaCertificateResolutionError("certificate")
                    if row.subject_spki_der != root.key_material.spki_der:
                        raise CaCertificateResolutionError("certificate")
                    if row.root_spki_der != root.key_material.spki_der:
                        raise CaCertificateResolutionError("certificate")
                    return CertificatePublicBinding(
                        cert_ref=row.cert_ref,
                        cert_bytes_ref=row.cert_bytes_ref,
                        ca_kind=row.ca_kind,
                        root_authority_ref=root.root_ref,
                        subject_key_ref=root.key_material.key_ref,
                        generation_ref=root.root_generation_id,
                        issuer_ref=None,
                        anchor_ref=row.anchor_ref,
                        serial_public=row.serial_public,
                        fingerprint_public=row.fingerprint_public,
                        subject_key_id=row.subject_key_id,
                        authority_key_id=row.authority_key_id,
                        certificate_der=row.certificate_der,
                        root_der=row.root_der,
                        subject_spki_der=row.subject_spki_der,
                        root_spki_der=row.root_spki_der,
                        serial_number=serial,
                        fingerprint_sha256=row.fingerprint_sha256,
                        ski=row.ski,
                        aki=row.aki,
                    )
                gen = row.intermediate_generation
                if gen is None:
                    raise CaCertificateResolutionError("certificate") from None
                gen.key_material.spki_der = _b(gen.key_material.spki_der)
                gen_root = gen.root
                gen_root.key_material.spki_der = _b(gen_root.key_material.spki_der)
                try:
                    gen.key_material.clean()
                    gen_root.key_material.clean()
                    gen.issuer.clean()
                    gen_root.clean()
                    gen.clean()
                    row.clean()
                except ValidationError:
                    raise CaCertificateResolutionError("certificate") from None
                true = (
                    CaCertificate.objects.using(alias)
                    .select_related("root")
                    .get(root_id=gen_root.pk, cert_ref=gen_root.root_cert_ref, ca_kind="root")
                )
                true.certificate_der = _b(true.certificate_der)
                if row.root_der != true.certificate_der:
                    raise CaCertificateResolutionError("certificate")
                if row.subject_spki_der != gen.key_material.spki_der:
                    raise CaCertificateResolutionError("certificate")
                if row.root_spki_der != gen_root.key_material.spki_der:
                    raise CaCertificateResolutionError("certificate")
                return CertificatePublicBinding(
                    cert_ref=row.cert_ref,
                    cert_bytes_ref=row.cert_bytes_ref,
                    ca_kind=row.ca_kind,
                    root_authority_ref=gen_root.root_ref,
                    subject_key_ref=gen.key_material.key_ref,
                    generation_ref=gen.generation_id,
                    issuer_ref=gen.issuer.issuer_id,
                    anchor_ref=row.anchor_ref,
                    serial_public=row.serial_public,
                    fingerprint_public=row.fingerprint_public,
                    subject_key_id=row.subject_key_id,
                    authority_key_id=row.authority_key_id,
                    certificate_der=row.certificate_der,
                    root_der=row.root_der,
                    subject_spki_der=row.subject_spki_der,
                    root_spki_der=row.root_spki_der,
                    serial_number=serial,
                    fingerprint_sha256=row.fingerprint_sha256,
                    ski=row.ski,
                    aki=row.aki,
                )
        except CaCertificateResolutionError:
            raise
        except ObjectDoesNotExist:
            raise CaCertificateResolutionError("certificate") from None
        except ValidationError:
            raise CaCertificateResolutionError("certificate") from None
