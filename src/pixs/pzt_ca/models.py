"""Registre CA PZT ; modeles transactionnels, forme seule, sans secret ni activation."""

from __future__ import annotations

import datetime
import hashlib
import re
from decimal import Decimal
from typing import NoReturn
from django.db.models.functions import Length
from django.db.models.lookups import Exact, GreaterThan
from pixs.pzt_ca.x509_profile import (
    X509ProfileError,
    _load_expected_public_key,
    verify_root_self_signature,
    verify_intermediate_issued,
)

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from pixs.core.persistence.base import UUID7_RE, CoreBase
from pixs.pzt.identifiers import PztIdentifierError, new_uuid7, require_uuid7

from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.data_retention_states import DataRetentionState

HEX64_RE = r"^[0-9a-f]{64}$"
_EPOCH_RE = r"^(0|[1-9][0-9]*)$"

SERIAL_MAX = (1 << 159) - 1

CA_KIND_CHOICES = ("root", "intermediate")
ROOT_STATUS_CHOICES = ("prepared", "active", "retired")

FIXED = "État de stockage CA invalide."


def _fail() -> NoReturn:
    raise ValidationError(FIXED)


def _opaque(value: object) -> bool:
    if type(value) is not str or value == "" or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_uuid7(value: object) -> bool:
    try:
        require_uuid7(value)
    except PztIdentifierError:
        return False
    return True


def _common(row: CoreBase) -> None:
    if not _is_uuid7(row.pk):
        _fail()
    if type(row.version) is not int or row.version < 1:
        _fail()
    for value in (row.created_at, row.updated_at):
        if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
            _fail()
    if row.created_at > row.updated_at:
        _fail()
    if row.governance_ref is not None and not _opaque(row.governance_ref):
        _fail()
    for value, allowed in (
        (row.persistence_state, tuple(s.value for s in DataPersistenceState)),
        (row.retention_state, tuple(s.value for s in DataRetentionState)),
    ):
        if type(value) is not str or value not in allowed:
            _fail()
    for value, allowed in (
        (row.confidentiality, tuple(c.value for c in ConfidentialityLevel)),
        (row.personal, tuple(p.value for p in PersonalDataLevel)),
    ):
        if value is not None and (type(value) is not str or value not in allowed):
            _fail()


def _require_serial_exact(value: object) -> int:
    """Série X.509 : int exact ou Decimal exact fini intégral, 1..SERIAL_MAX."""
    if type(value) is int:
        if value < 1 or value > SERIAL_MAX:
            _fail()
        return value
    if type(value) is Decimal:
        if not value.is_finite():
            _fail()
        if value != value.to_integral_value():
            _fail()
        if value < 1 or value > SERIAL_MAX:
            _fail()
        return int(value)
    _fail()


def _epoch_int_to_text(value: object) -> str:
    if type(value) is not int or value < 0:
        _fail()
    try:
        text = str(value)
    except ValueError:
        raise ValidationError(FIXED) from None
    if re.fullmatch(_EPOCH_RE, text) is None:
        _fail()
    return text


def _epoch_text_to_int(text: object) -> int:
    if type(text) is not str or text == "" or "\x00" in text:
        _fail()
    if not text.isascii():
        _fail()
    if re.fullmatch(_EPOCH_RE, text) is None:
        _fail()
    try:
        number = int(text, 10)
    except ValueError:
        raise ValidationError(FIXED) from None
    if type(number) is not int or number < 0:
        _fail()
    return number


def _required_related(row: models.Model, field_name: str, expected_type: type):
    try:
        related = getattr(row, field_name)
    except ObjectDoesNotExist:
        _fail()
    if type(related) is not expected_type:
        _fail()
    return related


class CaKeyMaterial(CoreBase):
    """Référence publique de clé CA, sans privé ni blob TPM ni booléen de protection."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    key_ref = models.TextField(unique=True)
    key_material_ref = models.TextField()
    spki_sha256 = models.CharField(max_length=64, unique=True)
    spki_der = models.BinaryField()
    key_created_at = models.DateTimeField()
    ca_kind = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_key_material"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_km_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(key_ref=""),
                name="pzt_ca_km_keyref_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(key_material_ref=""),
                name="pzt_ca_km_matref_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(spki_sha256__regex=HEX64_RE),
                name="pzt_ca_km_spki_hex",
            ),
            models.CheckConstraint(
                condition=GreaterThan(Length("spki_der"), 0),
                name="pzt_ca_km_der_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(ca_kind__in=["root", "intermediate"]),
                name="pzt_ca_km_kind_vocab",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.key_ref):
            _fail()
        if not _opaque(self.key_material_ref):
            _fail()
        if type(self.spki_sha256) is not str or re.fullmatch(HEX64_RE, self.spki_sha256) is None:
            _fail()
        if type(self.spki_der) is not bytes or len(self.spki_der) == 0:
            _fail()
        if (
            type(self.key_created_at) is not datetime.datetime
            or self.key_created_at.tzinfo is not datetime.timezone.utc
        ):
            _fail()
        if type(self.ca_kind) is not str or self.ca_kind not in CA_KIND_CHOICES:
            _fail()
        digest = hashlib.sha256(self.spki_der).hexdigest()
        if digest != self.spki_sha256:
            _fail()
        # Format public P-256 seul via helper existant, sans re-crypto.
        # Ne prouve ni détention matérielle ni autorité.
        try:
            _load_expected_public_key(self.spki_der)
        except X509ProfileError:
            _fail()


class CaRoot(CoreBase):
    """Racine déclarée. Le statut ne donne aucun droit.

    Liaison immuable et retrait terminal : protégés seulement par SQL
    ultérieur distinct et services, non acquis par ce fragment.
    """

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    domain = models.TextField()
    root_ref = models.TextField()
    root_generation_id = models.TextField(unique=True)
    root_cert_ref = models.TextField()
    key_material = models.OneToOneField(
        CaKeyMaterial,
        on_delete=models.PROTECT,
        related_name="root_binding",
    )
    status = models.TextField(default="prepared")

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_root"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_root_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(domain=""),
                name="pzt_ca_root_domain_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(root_ref=""),
                name="pzt_ca_root_ref_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(root_generation_id=""),
                name="pzt_ca_root_gen_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(root_cert_ref=""),
                name="pzt_ca_root_certref_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=["prepared", "active", "retired"]),
                name="pzt_ca_root_status_vocab",
            ),
            models.UniqueConstraint(
                fields=["domain", "root_ref"],
                name="pzt_ca_root_domain_ref_uq",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.domain):
            _fail()
        if not _opaque(self.root_ref):
            _fail()
        if not _opaque(self.root_generation_id):
            _fail()
        if not _opaque(self.root_cert_ref):
            _fail()
        if type(self.status) is not str or self.status not in ROOT_STATUS_CHOICES:
            _fail()
        linked = _required_related(self, "key_material", CaKeyMaterial)
        if type(linked.ca_kind) is not str or linked.ca_kind != "root":
            _fail()


class CaIssuer(CoreBase):
    """Émetteur déclaré sous une racine. Le rôle ne donne aucun droit."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    domain = models.TextField()
    logical_authority = models.TextField()
    emission_scope = models.TextField()
    issuer_id = models.TextField()
    issuer_role = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_issuer"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_issuer_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(domain=""),
                name="pzt_ca_issuer_domain_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(logical_authority=""),
                name="pzt_ca_issuer_authority_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(emission_scope=""),
                name="pzt_ca_issuer_scope_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(issuer_id=""),
                name="pzt_ca_issuer_issuerid_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(issuer_role__in=["principal", "standby"]),
                name="pzt_ca_issuer_role_vocab",
            ),
            models.UniqueConstraint(
                fields=["domain", "logical_authority", "emission_scope", "issuer_id"],
                name="pzt_ca_issuer_identity_uq",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.domain):
            _fail()
        if not _opaque(self.logical_authority):
            _fail()
        if not _opaque(self.emission_scope):
            _fail()
        if not _opaque(self.issuer_id):
            _fail()
        if type(self.issuer_role) is not str or self.issuer_role not in ("principal", "standby"):
            _fail()


class CaGeneration(CoreBase):
    """Génération d’un émetteur. Aucune réactivation implicitement admise."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    issuer = models.ForeignKey(
        "CaIssuer",
        on_delete=models.PROTECT,
        related_name="generations",
    )
    root = models.ForeignKey(
        "CaRoot",
        on_delete=models.PROTECT,
        related_name="generations",
    )
    key_material = models.OneToOneField(
        "CaKeyMaterial",
        on_delete=models.PROTECT,
        related_name="generation_binding",
    )
    generation_id = models.TextField(unique=True)
    created_epoch = models.TextField()
    status = models.TextField()
    predecessor = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        related_name="successors",
    )

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_generation"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_gen_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(generation_id=""),
                name="pzt_ca_gen_genid_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(created_epoch__regex=_EPOCH_RE),
                name="pzt_ca_gen_epoch_format",
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=["prepared", "reserved", "active", "retired"]),
                name="pzt_ca_gen_status_vocab",
            ),
            models.UniqueConstraint(
                fields=["issuer"],
                condition=models.Q(status="active"),
                name="pzt_ca_gen_one_active_per_issuer",
            ),
            models.CheckConstraint(
                condition=models.Q(predecessor__isnull=True) | ~models.Q(predecessor=models.F("id")),
                name="pzt_ca_gen_pred_not_self",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.generation_id):
            _fail()
        _epoch_text_to_int(self.created_epoch)
        if type(self.status) is not str or self.status not in (
            "prepared",
            "reserved",
            "active",
            "retired",
        ):
            _fail()
        linked_issuer = _required_related(self, "issuer", CaIssuer)
        linked_root = _required_related(self, "root", CaRoot)
        if linked_issuer.domain != linked_root.domain:
            _fail()
        linked_key = _required_related(self, "key_material", CaKeyMaterial)
        if type(linked_key.ca_kind) is not str or linked_key.ca_kind != "intermediate":
            _fail()
        if self.predecessor_id is None:
            return
        linked_pred = _required_related(self, "predecessor", CaGeneration)
        if linked_pred.pk == self.pk:
            _fail()
        if linked_pred.issuer_id != self.issuer_id:
            _fail()
        # Projection publique ultérieure : predecessor.generation_id.
        # Ne jamais confondre UUID interne predecessor_id et public_ref.


class CaCertificate(CoreBase):
    """Certificat public conservé. Vérification publique sans autorité."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    cert_ref = models.TextField(unique=True)
    cert_bytes_ref = models.TextField()
    ca_kind = models.TextField()
    root = models.ForeignKey(
        "CaRoot",
        on_delete=models.PROTECT,
        related_name="certificates",
    )
    intermediate_generation = models.ForeignKey(
        "CaGeneration",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        related_name="certificates",
    )
    serial_number = models.DecimalField(max_digits=48, decimal_places=0)
    serial_public = models.TextField()
    not_before_utc = models.DateTimeField()
    not_after_utc = models.DateTimeField()
    fingerprint_public = models.TextField()
    fingerprint_sha256 = models.BinaryField()
    subject_key_id = models.TextField()
    ski = models.BinaryField()
    authority_key_id = models.TextField(null=True, blank=True, default=None)
    aki = models.BinaryField(null=True, blank=True, default=None)
    certificate_der = models.BinaryField()
    root_der = models.BinaryField()
    subject_spki_der = models.BinaryField()
    root_spki_der = models.BinaryField()
    anchor_ref = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_certificate"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_cert_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(cert_ref=""),
                name="pzt_ca_cert_ref_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(cert_bytes_ref=""),
                name="pzt_ca_cert_bytesref_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(ca_kind__in=["root", "intermediate"]),
                name="pzt_ca_cert_kind_vocab",
            ),
            models.CheckConstraint(
                condition=GreaterThan(models.F("serial_number"), 0),
                name="pzt_ca_cert_serial_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(serial_number__lte=SERIAL_MAX),
                name="pzt_ca_cert_serial_max",
            ),
            models.CheckConstraint(
                condition=~models.Q(serial_public=""),
                name="pzt_ca_cert_serialpub_nonempty",
            ),
            models.CheckConstraint(
                condition=GreaterThan(
                    models.F("not_after_utc"), models.F("not_before_utc")
                ),
                name="pzt_ca_cert_dates_ordered",
            ),
            models.CheckConstraint(
                condition=~models.Q(fingerprint_public=""),
                name="pzt_ca_cert_fppub_nonempty",
            ),
            models.CheckConstraint(
                condition=Exact(Length("fingerprint_sha256"), 32),
                name="pzt_ca_cert_fp32",
            ),
            models.CheckConstraint(
                condition=~models.Q(subject_key_id=""),
                name="pzt_ca_cert_skiid_nonempty",
            ),
            models.CheckConstraint(
                condition=GreaterThan(Length("ski"), 0),
                name="pzt_ca_cert_ski_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(authority_key_id__isnull=True)
                | ~models.Q(authority_key_id=""),
                name="pzt_ca_cert_akiid_opt",
            ),
            models.CheckConstraint(
                condition=models.Q(aki__isnull=True) | GreaterThan(Length("aki"), 0),
                name="pzt_ca_cert_aki_len",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(authority_key_id__isnull=True, aki__isnull=True)
                    | (
                        models.Q(authority_key_id__isnull=False, aki__isnull=False)
                        & ~models.Q(authority_key_id="")
                    )
                ),
                name="pzt_ca_cert_aki_coupling",
            ),
            models.CheckConstraint(
                condition=GreaterThan(Length("certificate_der"), 0),
                name="pzt_ca_cert_der_nonempty",
            ),
            models.CheckConstraint(
                condition=GreaterThan(Length("root_der"), 0),
                name="pzt_ca_cert_rootder_nonempty",
            ),
            models.CheckConstraint(
                condition=GreaterThan(Length("subject_spki_der"), 0),
                name="pzt_ca_cert_subspki_nonempty",
            ),
            models.CheckConstraint(
                condition=GreaterThan(Length("root_spki_der"), 0),
                name="pzt_ca_cert_rootspki_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(anchor_ref=""),
                name="pzt_ca_cert_anchor_nonempty",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        ca_kind="root", intermediate_generation__isnull=True
                    )
                    | models.Q(
                        ca_kind="intermediate",
                        intermediate_generation__isnull=False,
                    )
                ),
                name="pzt_ca_cert_role_branch",
            ),
            models.CheckConstraint(
                condition=~models.Q(ca_kind="intermediate")
                | (
                    models.Q(aki__isnull=False)
                    & GreaterThan(Length("aki"), 0)
                    & models.Q(authority_key_id__isnull=False)
                    & ~models.Q(authority_key_id="")
                ),
                name="pzt_ca_cert_inter_aki_required",
            ),
            models.UniqueConstraint(
                fields=["root", "serial_number"],
                name="pzt_ca_cert_root_serial_uq",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.cert_ref):
            _fail()
        if not _opaque(self.cert_bytes_ref):
            _fail()
        if type(self.ca_kind) is not str or self.ca_kind not in (
            "root",
            "intermediate",
        ):
            _fail()
        _require_serial_exact(self.serial_number)
        if not _opaque(self.serial_public):
            _fail()
        for value in (self.not_before_utc, self.not_after_utc):
            import datetime as _dt

            if (
                type(value) is not _dt.datetime
                or value.tzinfo is not _dt.timezone.utc
            ):
                _fail()
        if self.not_after_utc <= self.not_before_utc:
            _fail()
        if not _opaque(self.fingerprint_public):
            _fail()
        if type(self.fingerprint_sha256) is not bytes or len(
            self.fingerprint_sha256
        ) != 32:
            _fail()
        if not _opaque(self.subject_key_id):
            _fail()
        if type(self.ski) is not bytes or len(self.ski) == 0:
            _fail()
        if self.authority_key_id is not None and not _opaque(
            self.authority_key_id
        ):
            _fail()
        if self.aki is not None and (
            type(self.aki) is not bytes or len(self.aki) == 0
        ):
            _fail()
        if (self.authority_key_id is None) != (self.aki is None):
            _fail()
        for raw in (
            self.certificate_der,
            self.root_der,
            self.subject_spki_der,
            self.root_spki_der,
        ):
            if type(raw) is not bytes or len(raw) == 0:
                _fail()
        if not _opaque(self.anchor_ref):
            _fail()
        linked_root = _required_related(self, "root", CaRoot)
        linked_root_key = _required_related(
            linked_root, "key_material", CaKeyMaterial
        )
        if type(linked_root_key.ca_kind) is not str or (
            linked_root_key.ca_kind != "root"
        ):
            _fail()
        if self.root_spki_der != linked_root_key.spki_der:
            _fail()

        digest = hashlib.sha256(self.certificate_der).digest()
        if digest != self.fingerprint_sha256:
            _fail()

        if self.ca_kind == "root":
            if self.intermediate_generation_id is not None:
                _fail()
            if self.cert_ref != linked_root.root_cert_ref:
                _fail()
            if self.root_der != self.certificate_der:
                _fail()
            if self.subject_spki_der != linked_root_key.spki_der:
                _fail()
            try:
                facts = verify_root_self_signature(
                    self.certificate_der,
                    expected_public_key_spki_der=linked_root_key.spki_der,
                )
            except X509ProfileError:
                raise ValidationError(FIXED) from None
            if int(self.serial_number) != facts.serial_number:
                _fail()
            if (
                self.not_before_utc != facts.not_valid_before_utc
                or self.not_after_utc != facts.not_valid_after_utc
            ):
                _fail()
            if facts.subject_key_identifier != self.ski:
                _fail()
            if facts.authority_key_identifier is None:
                if self.aki is not None:
                    _fail()
            else:
                if self.aki is None or facts.authority_key_identifier != self.aki:
                    _fail()
            return
        linked_gen = _required_related(
            self, "intermediate_generation", CaGeneration
        )
        linked_gen_key = _required_related(
            linked_gen, "key_material", CaKeyMaterial
        )
        if type(linked_gen_key.ca_kind) is not str or (
            linked_gen_key.ca_kind != "intermediate"
        ):
            _fail()
        if self.subject_spki_der != linked_gen_key.spki_der:
            _fail()
        linked_issuer = _required_related(linked_gen, "issuer", CaIssuer)
        linked_gen_root = _required_related(linked_gen, "root", CaRoot)
        if linked_gen_root.pk != linked_root.pk:
            _fail()
        if linked_issuer.domain != linked_root.domain:
            _fail()
        alias = self._state.db
        if type(alias) is not str or alias == "":
            _fail()
        try:
            root_row = CaCertificate.objects.using(alias).get(
                root=linked_root, cert_ref=linked_root.root_cert_ref, ca_kind="root"
            )
        except ObjectDoesNotExist:
            raise ValidationError(FIXED) from None
        if type(root_row.certificate_der) is not bytes:
            _fail()
        if self.root_der != root_row.certificate_der:
            _fail()
        try:
            pair = verify_intermediate_issued(
                self.certificate_der,
                issuer_der=root_row.certificate_der,
                expected_issuer_spki_der=linked_root_key.spki_der,
                expected_intermediate_spki_der=linked_gen_key.spki_der,
            )
        except X509ProfileError:
            raise ValidationError(FIXED) from None
        intermediate_facts = pair[0]
        if int(self.serial_number) != intermediate_facts.serial_number:
            _fail()
        if (
            self.not_before_utc != intermediate_facts.not_valid_before_utc
            or self.not_after_utc != intermediate_facts.not_valid_after_utc
        ):
            _fail()
        if intermediate_facts.subject_key_identifier != self.ski:
            _fail()
        if intermediate_facts.authority_key_identifier is None:
            _fail()
        if self.aki is None or (
            intermediate_facts.authority_key_identifier != self.aki
        ):
            _fail()


class CaActiveSelection(CoreBase):
    """Sélection courante. Aucun droit accordé par la ligne."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    domain = models.TextField()
    logical_authority = models.TextField()
    emission_scope = models.TextField()
    generation = models.OneToOneField(
        "CaGeneration",
        on_delete=models.PROTECT,
        related_name="active_selection",
    )
    epoch = models.TextField()
    engagement_ref = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_active_selection"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_sel_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(domain=""),
                name="pzt_ca_sel_domain_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(logical_authority=""),
                name="pzt_ca_sel_authority_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(emission_scope=""),
                name="pzt_ca_sel_scope_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(epoch__regex=_EPOCH_RE),
                name="pzt_ca_sel_epoch_format",
            ),
            models.CheckConstraint(
                condition=~models.Q(engagement_ref=""),
                name="pzt_ca_sel_engagement_nonempty",
            ),
            models.UniqueConstraint(
                fields=["domain", "logical_authority", "emission_scope"],
                name="pzt_ca_sel_identity_uq",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.domain):
            _fail()
        if not _opaque(self.logical_authority):
            _fail()
        if not _opaque(self.emission_scope):
            _fail()
        _epoch_text_to_int(self.epoch)
        if not _opaque(self.engagement_ref):
            _fail()
        linked_gen = _required_related(self, "generation", CaGeneration)
        if (
            type(linked_gen.status) is not str
            or linked_gen.status != "active"
        ):
            _fail()
        linked_issuer = _required_related(linked_gen, "issuer", CaIssuer)
        if linked_issuer.domain != self.domain:
            _fail()
        if linked_issuer.logical_authority != self.logical_authority:
            _fail()
        if linked_issuer.emission_scope != self.emission_scope:
            _fail()
        linked_gen_root = _required_related(linked_gen, "root", CaRoot)
        if linked_gen_root.domain != self.domain:
            _fail()


class CaOperationLink(CoreBase):
    """Lien d’opération déclaré. Liaison immuable future par trigger/service, non acquise ici."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    domain = models.TextField()
    logical_authority = models.TextField()
    emission_scope = models.TextField()
    operation_id = models.TextField(unique=True)
    operation_version = models.TextField()
    request_id = models.TextField()
    context_ref = models.TextField()
    input_fingerprint = models.TextField()
    epoch = models.TextField()
    policy_ref = models.TextField()
    content_sha256 = models.CharField(max_length=64)
    serializer_version = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_operation_link"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_oplink_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(domain=""),
                name="pzt_ca_oplink_domain_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(logical_authority=""),
                name="pzt_ca_oplink_authority_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(emission_scope=""),
                name="pzt_ca_oplink_scope_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="pzt_ca_oplink_opid_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(operation_version=""),
                name="pzt_ca_oplink_opver_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(request_id=""),
                name="pzt_ca_oplink_reqid_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(context_ref=""),
                name="pzt_ca_oplink_ctx_nonempty",
            ),
            models.CheckConstraint(
                condition=~models.Q(input_fingerprint=""),
                name="pzt_ca_oplink_inputfp_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(epoch__regex=_EPOCH_RE),
                name="pzt_ca_oplink_epoch_format",
            ),
            models.CheckConstraint(
                condition=~models.Q(policy_ref=""),
                name="pzt_ca_oplink_policy_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(content_sha256__regex=HEX64_RE),
                name="pzt_ca_oplink_content_hex",
            ),
            models.CheckConstraint(
                condition=~models.Q(serializer_version=""),
                name="pzt_ca_oplink_server_nonempty",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.domain):
            _fail()
        if not _opaque(self.logical_authority):
            _fail()
        if not _opaque(self.emission_scope):
            _fail()
        if not _opaque(self.operation_id):
            _fail()
        if not _opaque(self.operation_version):
            _fail()
        if not _opaque(self.request_id):
            _fail()
        if not _opaque(self.context_ref):
            _fail()
        if not _opaque(self.input_fingerprint):
            _fail()
        _epoch_text_to_int(self.epoch)
        if not _opaque(self.policy_ref):
            _fail()
        if type(self.content_sha256) is not str or re.fullmatch(
            HEX64_RE, self.content_sha256
        ) is None:
            _fail()
        if not _opaque(self.serializer_version):
            _fail()

        # CommandEnvelope et idempotence Core ne se réduisent pas à cette table.


class CaResultRecord(CoreBase):
    """Résultat §7.1. Enregistrement seul, sans nouvel effet. Aucun droit accordé."""

    RESULT_KIND = ("current_operation", "historical_operation")
    VALIDATION = ("valid", "invalid", "uncertain")
    ENGAGEMENT = ("engaged", "not_engaged", "unknown")
    EFFECT = ("not_started", "applied", "failed", "uncertain")
    ERROR_CODE = (
        "ok",
        "refused",
        "precondition_failed",
        "exclusion_missing",
        "proof_invalid",
        "epoch_stale",
        "mandate_invalid",
        "dependency_unavailable",
        "conflict",
        "unknown",
    )

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    result_id = models.TextField(unique=True)
    operation_link = models.ForeignKey(
        "CaOperationLink",
        on_delete=models.PROTECT,
        related_name="results",
    )
    recorded_at = models.DateTimeField()
    result_kind = models.TextField()
    validation = models.TextField()
    engagement = models.TextField()
    effect = models.TextField()
    error_code = models.TextField(null=True, blank=True, default=None)
    engagement_ref = models.TextField(null=True, blank=True, default=None)
    effect_evidence_ref = models.TextField(null=True, blank=True, default=None)

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_result_record"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_result_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(result_id=""),
                name="pzt_ca_result_rid_nonempty",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    result_kind__in=["current_operation", "historical_operation"]
                ),
                name="pzt_ca_result_kind_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(validation__in=["valid", "invalid", "uncertain"]),
                name="pzt_ca_result_validation_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    engagement__in=["engaged", "not_engaged", "unknown"]
                ),
                name="pzt_ca_result_engagement_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    effect__in=["not_started", "applied", "failed", "uncertain"]
                ),
                name="pzt_ca_result_effect_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(error_code__isnull=True)
                | models.Q(
                    error_code__in=[
                        "ok",
                        "refused",
                        "precondition_failed",
                        "exclusion_missing",
                        "proof_invalid",
                        "epoch_stale",
                        "mandate_invalid",
                        "dependency_unavailable",
                        "conflict",
                        "unknown",
                    ]
                ),
                name="pzt_ca_result_error_vocab",
            ),
            models.CheckConstraint(
                condition=models.Q(engagement_ref__isnull=True)
                | ~models.Q(engagement_ref=""),
                name="pzt_ca_result_engref_opt",
            ),
            models.CheckConstraint(
                condition=models.Q(effect_evidence_ref__isnull=True)
                | ~models.Q(effect_evidence_ref=""),
                name="pzt_ca_result_evidef_opt",
            ),
            models.CheckConstraint(
                condition=~models.Q(engagement="engaged")
                | (
                    models.Q(engagement_ref__isnull=False)
                    & ~models.Q(engagement_ref="")
                ),
                name="pzt_ca_result_engaged_ref",
            ),
            models.CheckConstraint(
                condition=~models.Q(effect="applied")
                | (
                    models.Q(effect_evidence_ref__isnull=False)
                    & ~models.Q(effect_evidence_ref="")
                ),
                name="pzt_ca_result_applied_evid",
            ),
            models.CheckConstraint(
                condition=~models.Q(
                    result_kind="current_operation", validation="invalid"
                )
                | models.Q(engagement="not_engaged", effect="not_started"),
                name="pzt_ca_result_curinv_clean",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.result_id):
            _fail()
        _required_related(self, "operation_link", CaOperationLink)
        import datetime as _dt

        if (
            type(self.recorded_at) is not _dt.datetime
            or self.recorded_at.tzinfo is not _dt.timezone.utc
        ):
            _fail()
        if type(self.result_kind) is not str or self.result_kind not in (
            "current_operation",
            "historical_operation",
        ):
            _fail()
        if type(self.validation) is not str or self.validation not in (
            "valid",
            "invalid",
            "uncertain",
        ):
            _fail()
        if type(self.engagement) is not str or self.engagement not in (
            "engaged",
            "not_engaged",
            "unknown",
        ):
            _fail()
        if type(self.effect) is not str or self.effect not in (
            "not_started",
            "applied",
            "failed",
            "uncertain",
        ):
            _fail()
        if self.error_code is not None and (
            type(self.error_code) is not str
            or self.error_code not in CaResultRecord.ERROR_CODE
        ):
            _fail()
        if self.engagement == "engaged":
            if not _opaque(self.engagement_ref):
                _fail()
        elif self.engagement_ref is not None and not _opaque(
            self.engagement_ref
        ):
            _fail()
        if self.effect == "applied":
            if not _opaque(self.effect_evidence_ref):
                _fail()
        elif self.effect_evidence_ref is not None and not _opaque(
            self.effect_evidence_ref
        ):
            _fail()
        if (
            self.result_kind == "current_operation"
            and self.validation == "invalid"
        ):
            if self.engagement != "not_engaged" or self.effect != "not_started":
                _fail()
        # unknown ne supprime pas les faits applied/failed observés.
        # Interdiction de nouvel effet dans le service, pas dans ce DTO.

    @property
    def operation_id(self):
        return self.operation_link.operation_id

    @property
    def operation_version(self):
        return self.operation_link.operation_version

    @property
    def request_id(self):
        return self.operation_link.request_id

    @property
    def context_ref(self):
        return self.operation_link.context_ref

    @property
    def input_fingerprint(self):
        return self.operation_link.input_fingerprint

    @property
    def domain(self):
        return self.operation_link.domain

    @property
    def logical_authority(self):
        return self.operation_link.logical_authority

    @property
    def emission_scope(self):
        return self.operation_link.emission_scope

    @property
    def epoch(self):
        return self.operation_link.epoch

    @property
    def policy_ref(self):
        return self.operation_link.policy_ref

    @property
    def content_sha256(self):
        return self.operation_link.content_sha256

    @property
    def serializer_version(self):
        return self.operation_link.serializer_version


# Champs projetés depuis le parent CaOperationLink, sans export à ce stade :
# operation_id, operation_version, request_id, context_ref, input_fingerprint,
# domain, logical_authority, emission_scope, epoch, policy_ref,
# content_sha256, serializer_version.
# Noms internes validation/engagement/effect non contractuels :
# sortie future via DTO validation_outcome/engagement_outcome/effect_outcome.


class CaRetirementRecord(CoreBase):
    """Tombstone de retrait. Aucune preuve d’exclusion système déduite."""

    id = models.UUIDField(primary_key=True, default=new_uuid7, editable=False)
    retirement_ref = models.TextField(unique=True)
    target_root = models.OneToOneField(
        "CaRoot",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        related_name="retirement",
    )
    target_generation = models.OneToOneField(
        "CaGeneration",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        related_name="retirement",
    )
    operation_link = models.ForeignKey(
        "CaOperationLink",
        on_delete=models.PROTECT,
        related_name="retirements",
    )
    retired_at = models.DateTimeField()
    epoch = models.TextField()
    retirement_evidence_ref = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_pzt_ca"
        db_table = "pixs_pzt_ca_retirement_record"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(
                condition=models.Q(id__regex=UUID7_RE),
                name="pzt_ca_ret_id_uuid7",
            ),
            models.CheckConstraint(
                condition=~models.Q(retirement_ref=""),
                name="pzt_ca_ret_ref_nonempty",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        target_root__isnull=False,
                        target_generation__isnull=True,
                    )
                    | models.Q(
                        target_root__isnull=True,
                        target_generation__isnull=False,
                    )
                ),
                name="pzt_ca_ret_exactly_one_target",
            ),
            models.CheckConstraint(
                condition=models.Q(epoch__regex=_EPOCH_RE),
                name="pzt_ca_ret_epoch_format",
            ),
            models.CheckConstraint(
                condition=~models.Q(retirement_evidence_ref=""),
                name="pzt_ca_ret_evidence_nonempty",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        _common(self)
        if not _opaque(self.retirement_ref):
            _fail()
        if (self.target_root_id is None) == (
            self.target_generation_id is None
        ):
            _fail()
        linked_operation = _required_related(
            self, "operation_link", CaOperationLink
        )
        if not _opaque(linked_operation.domain):
            _fail()
        import datetime as _dt

        if (
            type(self.retired_at) is not _dt.datetime
            or self.retired_at.tzinfo is not _dt.timezone.utc
        ):
            _fail()
        _epoch_text_to_int(self.epoch)
        _epoch_text_to_int(linked_operation.epoch)
        if self.epoch != linked_operation.epoch:
            _fail()
        if not _opaque(self.retirement_evidence_ref):
            _fail()
        if self.target_root_id is not None:
            linked_root = _required_related(self, "target_root", CaRoot)
            if (
                type(linked_root.status) is not str
                or linked_root.status != "retired"
            ):
                _fail()
            if linked_root.domain != linked_operation.domain:
                _fail()
            return
        linked_generation = _required_related(
            self, "target_generation", CaGeneration
        )
        if (
            type(linked_generation.status) is not str
            or linked_generation.status != "retired"
        ):
            _fail()
        linked_issuer = _required_related(
            linked_generation, "issuer", CaIssuer
        )
        linked_root = _required_related(linked_generation, "root", CaRoot)
        if linked_root.domain != linked_operation.domain:
            _fail()
        if linked_issuer.domain != linked_operation.domain:
            _fail()
        if (
            linked_issuer.logical_authority
            != linked_operation.logical_authority
        ):
            _fail()
        if (
            linked_issuer.emission_scope
            != linked_operation.emission_scope
        ):
            _fail()
        # État retired terminal et immutabilité exigent futurs triggers/services.
