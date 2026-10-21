"""Audit durable C05 : sink propriétaire Core, deux formats distincts, append-only.

Propriétaire `pixs.core`, table `pixs_core_audit`. Aucune donnée Auth persistée.
Seul `CoreAuditEvent` est réexporté par `models.py`. `alias` corrélation technique
seule ; la preuve utilise la connexion réellement associée.
"""
from __future__ import annotations

import hashlib
import json
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from pixs.core.audit_contracts import AuditError, canonical_pdp_bytes, validate_pdp_payload
from pixs.core.persistence.base import UUID7_RE, CoreBase
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.scope.context import (
    ScopeContext,
    ScopeStructureError,
    ScopeType,
    validate_structure,
)
from pixs.kernel.audit_event import AuditEvent as GenericAuditEvent
from pixs.kernel.audit_event import validate_audit_event

__all__ = ["CoreAuditEvent", "CoreAuditImmutable", "KIND_GENERIC", "KIND_PDP"]

FIXED_MESSAGE = "Audit Core invalide."

KIND_GENERIC = "GENERIC_AUDIT"
KIND_PDP = "PDP_AUDIT"
KINDS = (KIND_GENERIC, KIND_PDP)

_GENERIC_KEYS = frozenset(
    {
        "event_id", "occurred_at", "actor_reference", "tenant_reference",
        "action", "resource_type", "resource_id", "result", "reason_or_error",
        "correlation_ids", "causation_ids", "component_id", "component_version",
    }
)
_PDP_KEYS = frozenset(
    {
        "decision_id", "subject_id", "resource_id", "action_id", "context",
        "correlation_id", "effect", "reason_code", "policy_version", "evaluated_at",
    }
)

class CoreAuditImmutable(ValueError):
    def __init__(self) -> None:
        super().__init__("Audit append-only : mutation ordinaire refusée.")
        self.code = "AUDIT_IMMUTABLE"
        self.element = "core_audit"
        self.step = "guard_orm"


def _is_exact_str(value: object) -> bool:
    return type(value) is str and value != ""


def _is_opt_exact_str(value: object) -> bool:
    # None admis ; sinon str exacte, y compris vide lorsque le constructeur l'admet.
    return value is None or type(value) is str


def _is_exact_str_list(value: object, allow_empty: bool) -> bool:
    if type(value) is not list:
        return False
    if len(value) == 0:
        return allow_empty
    return all(type(item) is str for item in value)


def _is_hex64(value: object) -> bool:
    if type(value) is not str or len(value) != 64:
        return False
    if value != value.lower():
        return False
    return all(c in "0123456789abcdef" for c in value)


def _canonical_generic_bytes(payload: dict) -> bytes:
    # Même schéma de canonicalisation que C01 pour ses seuls événements :
    # JSON UTF-8 trié compact, sans imposer les restrictions C01 aux generics.
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return raw.encode("utf-8")


class CoreAuditQuerySet(models.QuerySet):
    def update(self, *args, **kwargs):
        raise CoreAuditImmutable()

    def bulk_update(self, *args, **kwargs):
        raise CoreAuditImmutable()

    def delete(self):
        raise CoreAuditImmutable()

    def bulk_create(
        self,
        objs,
        batch_size=None,
        ignore_conflicts=False,
        update_conflicts=False,
        update_fields=None,
        unique_fields=None,
    ):
        if ignore_conflicts or update_conflicts or update_fields is not None or unique_fields is not None:
            raise CoreAuditImmutable()
        return super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=False)


class CoreAuditManager(models.Manager):
    def get_queryset(self):
        return CoreAuditQuerySet(self.model, using=self._db)


class CoreAuditEvent(CoreBase):
    record_id = models.UUIDField(primary_key=True, editable=False)
    kind = models.TextField()
    operation_id = models.TextField()
    alias = models.TextField()
    transaction_token = models.TextField()
    staged_xid = models.TextField()
    scope_type = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    scope_id = models.TextField(null=True, blank=True, default=None)

    generic_payload = models.JSONField(null=True, blank=True, default=None)
    pdp_payload = models.JSONField(null=True, blank=True, default=None)

    generic_event_id = models.TextField(null=True, blank=True, default=None)
    generic_event_sha256 = models.TextField(null=True, blank=True, default=None)
    current_payload_sha256 = models.TextField(null=True, blank=True, default=None)
    maintenance_op_id = models.TextField(null=True, blank=True, default=None)
    maintenance_version = models.IntegerField(null=True, blank=True, default=None)
    pdp_decision_id = models.TextField(null=True, blank=True, default=None)

    c01_journal_id = models.UUIDField(null=True, blank=True, default=None)
    c01_sequence = models.IntegerField(null=True, blank=True, default=None)
    c01_event_sha256 = models.TextField(null=True, blank=True, default=None)

    retention_days = models.PositiveIntegerField()
    retention_policy_origin = models.TextField()
    retention_policy_id = models.TextField()
    retention_policy_version = models.TextField()

    objects = CoreAuditManager()

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_audit"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=models.Q(kind__in=list(KINDS)), name="audit_kind_vocab"),
            models.CheckConstraint(condition=models.Q(record_id__regex=UUID7_RE), name="audit_record_uuid7_rgx"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="audit_op_nonempty"),
            models.CheckConstraint(condition=~models.Q(alias=""), name="audit_alias_nonempty"),
            models.CheckConstraint(condition=~models.Q(transaction_token=""), name="audit_token_nonempty"),
            models.CheckConstraint(
                condition=models.Q(scope_type__in=["TENANT", "PLATFORM"]), name="audit_scope_vocab"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(scope_type="TENANT", tenant_id__isnull=False)
                    | models.Q(scope_type="PLATFORM", tenant_id__isnull=True, scope_id__isnull=True)
                ),
                name="audit_tenant_coherence",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(kind=KIND_GENERIC, generic_payload__isnull=False, pdp_payload__isnull=True)
                    | models.Q(kind=KIND_PDP, pdp_payload__isnull=False, generic_payload__isnull=True)
                ),
                name="audit_kind_payload_coherence",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        kind=KIND_GENERIC, generic_event_id__isnull=False,
                        generic_event_sha256__isnull=False, pdp_decision_id__isnull=True,
                    )
                    | models.Q(
                        kind=KIND_PDP, generic_event_id__isnull=True,
                        generic_event_sha256__isnull=True,
                    )
                ),
                name="audit_kind_meta_coherence",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(c01_journal_id__isnull=True, c01_sequence__isnull=True, c01_event_sha256__isnull=True)
                    | models.Q(
                        kind=KIND_GENERIC, c01_journal_id__isnull=False,
                        c01_sequence__isnull=False, c01_event_sha256__isnull=False,
                    )
                ),
                name="audit_c01_all_or_nothing",
            ),
            models.CheckConstraint(
                condition=models.Q(c01_sequence__isnull=True) | models.Q(c01_sequence__gte=1),
                name="audit_c01_seq_pos",
            ),
            models.CheckConstraint(
                condition=models.Q(c01_journal_id__isnull=True) | models.Q(c01_journal_id__regex=UUID7_RE),
                name="audit_c01_uuid7_rgx",
            ),
            models.CheckConstraint(
                condition=models.Q(c01_event_sha256__isnull=True) | models.Q(c01_event_sha256__regex=r"^[0-9a-f]{64}$"),
                name="audit_c01_hash_rgx",
            ),
            models.CheckConstraint(
                condition=models.Q(c01_event_sha256__isnull=True) | models.Q(c01_event_sha256=models.F("generic_event_sha256")),
                name="audit_c01_hash_matches",
            ),
            models.CheckConstraint(
                condition=~models.Q(kind=KIND_GENERIC) | ~models.Q(generic_event_id=""),
                name="audit_gevt_nonempty",
            ),
            models.CheckConstraint(condition=~models.Q(staged_xid=""), name="audit_xid_nonempty"),
            models.CheckConstraint(condition=models.Q(retention_days__gte=1), name="audit_retention_positive"),
            models.CheckConstraint(condition=~models.Q(retention_policy_origin=""), name="audit_policy_origin"),
            models.CheckConstraint(
                condition=models.Q(current_payload_sha256__isnull=True, maintenance_op_id__isnull=True, maintenance_version__isnull=True)
                | (models.Q(current_payload_sha256__isnull=False, current_payload_sha256__regex=r"^[0-9a-f]{64}$", maintenance_op_id__isnull=False, maintenance_version__isnull=False, maintenance_version__gte=1)
                   & ~models.Q(maintenance_op_id="")),
                name="audit_maintenance_coherence",
            ),
            models.CheckConstraint(condition=~models.Q(retention_policy_id=""), name="audit_retpol_nonempty"),
            models.CheckConstraint(
                condition=~models.Q(retention_policy_version=""), name="audit_retpolver_nonempty"
            ),
            models.UniqueConstraint(
                fields=["generic_event_id"], name="audit_gevt_uq",
                condition=models.Q(generic_event_id__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["c01_journal_id", "c01_sequence"], name="audit_c01_journ_seq_uq",
                condition=models.Q(c01_journal_id__isnull=False),
            ),
            # Identité de stage PDP : répéter le même stage ne doit pas insérer
            # silencieusement deux lignes. Clé stable (operation_id, token, decision).
            # nulls_distinct=False : deux NULL décision sont la même identité et se
            # heurtent au lieu de dupliquer. Le sink compare aussi le contenu et
            # refuse toute collision divergente.
            models.UniqueConstraint(
                fields=["operation_id", "transaction_token", "pdp_decision_id"],
                name="audit_pdp_stage_uq",
                condition=models.Q(kind=KIND_PDP),
                nulls_distinct=False,
            ),
        ]
        indexes = [
            models.Index(fields=["tenant_id", "scope_id"], name="audit_tenant_scope_ix"),
            models.Index(fields=["operation_id"], name="audit_op_ix"),
            models.Index(fields=["generic_event_id"], name="audit_gevt_ix"),
            models.Index(fields=["pdp_decision_id"], name="audit_pdec_ix"),
        ]

    def save(self, *args, **kwargs):
        if kwargs.get("update_fields") is not None or not kwargs.get("force_insert", False):
            raise CoreAuditImmutable()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise CoreAuditImmutable()

    def clean(self) -> None:
        try:
            check_uuid7(self.record_id)
        except (Uuid7Error, AttributeError, TypeError, ValueError):
            raise ValidationError(FIXED_MESSAGE) from None
        if type(self.kind) is not str or self.kind not in KINDS:
            raise ValidationError(FIXED_MESSAGE)
        for field in ("operation_id", "alias", "transaction_token"):
            if type(getattr(self, field)) is not str or getattr(self, field) == "":
                raise ValidationError(FIXED_MESSAGE)
        if type(self.scope_type) is not str or self.scope_type not in ("TENANT", "PLATFORM"):
            raise ValidationError(FIXED_MESSAGE)
        if self.scope_type == "PLATFORM":
            if self.tenant_id is not None or self.scope_id is not None:
                raise ValidationError(FIXED_MESSAGE)
        else:
            if type(self.tenant_id) is not str or self.tenant_id == "":
                raise ValidationError(FIXED_MESSAGE)
            if self.scope_id is not None and (type(self.scope_id) is not str or self.scope_id == ""):
                raise ValidationError(FIXED_MESSAGE)
        if type(self.retention_policy_id) is not str or self.retention_policy_id == "":
            raise ValidationError(FIXED_MESSAGE)
        if type(self.retention_policy_version) is not str or self.retention_policy_version == "":
            raise ValidationError(FIXED_MESSAGE)
        if not _is_exact_str(self.staged_xid):
            raise ValidationError(FIXED_MESSAGE)
        if type(self.retention_days) is not int or self.retention_days < 1:
            raise ValidationError(FIXED_MESSAGE)
        if not _is_exact_str(self.retention_policy_origin):
            raise ValidationError(FIXED_MESSAGE)
        maintenance = (self.current_payload_sha256, self.maintenance_op_id, self.maintenance_version)
        if any(value is not None for value in maintenance):
            if not _is_hex64(self.current_payload_sha256) or not _is_exact_str(self.maintenance_op_id):
                raise ValidationError(FIXED_MESSAGE)
            if type(self.maintenance_version) is not int or self.maintenance_version < 1:
                raise ValidationError(FIXED_MESSAGE)
        c01 = [self.c01_journal_id, self.c01_sequence, self.c01_event_sha256]
        if any(v is not None for v in c01):
            if self.kind != KIND_GENERIC:
                raise ValidationError(FIXED_MESSAGE)
            if self.c01_journal_id is None or type(self.c01_journal_id) is not uuid.UUID:
                raise ValidationError(FIXED_MESSAGE)
            try:
                check_uuid7(self.c01_journal_id)
            except (Uuid7Error, AttributeError, TypeError, ValueError):
                raise ValidationError(FIXED_MESSAGE) from None
            if type(self.c01_sequence) is not int or isinstance(self.c01_sequence, bool):
                raise ValidationError(FIXED_MESSAGE)
            if self.c01_sequence < 1:
                raise ValidationError(FIXED_MESSAGE)
            if not _is_hex64(self.c01_event_sha256):
                raise ValidationError(FIXED_MESSAGE)
        if self.kind == KIND_GENERIC:
            self._clean_generic()
        else:
            self._clean_pdp()

    def _clean_generic(self) -> None:
        if self.pdp_payload is not None or self.pdp_decision_id is not None:
            raise ValidationError(FIXED_MESSAGE)
        payload = self.generic_payload
        if type(payload) is not dict or set(payload.keys()) != set(_GENERIC_KEYS):
            raise ValidationError(FIXED_MESSAGE)
        if type(payload["event_id"]) is not str or payload["event_id"] == "":
            raise ValidationError(FIXED_MESSAGE)
        if type(payload["occurred_at"]) is not str or payload["occurred_at"] == "":
            raise ValidationError(FIXED_MESSAGE)
        if type(payload["actor_reference"]) is not str or payload["actor_reference"] == "":
            raise ValidationError(FIXED_MESSAGE)
        if payload["tenant_reference"] is not None and type(payload["tenant_reference"]) is not str:
            raise ValidationError(FIXED_MESSAGE)
        for key in ("action", "resource_type", "resource_id", "result", "component_id", "component_version"):
            if type(payload[key]) is not str or payload[key] == "":
                raise ValidationError(FIXED_MESSAGE)
        if payload["reason_or_error"] is not None and type(payload["reason_or_error"]) is not str:
            raise ValidationError(FIXED_MESSAGE)
        if not _is_exact_str_list(payload["correlation_ids"], allow_empty=True):
            raise ValidationError(FIXED_MESSAGE)
        if not _is_exact_str_list(payload["causation_ids"], allow_empty=True):
            raise ValidationError(FIXED_MESSAGE)
        try:
            event = GenericAuditEvent(
                event_id=payload["event_id"],
                occurred_at=payload["occurred_at"],
                actor_reference=payload["actor_reference"],
                tenant_reference=payload["tenant_reference"],
                action=payload["action"],
                resource_type=payload["resource_type"],
                resource_id=payload["resource_id"],
                result=payload["result"],
                reason_or_error=payload["reason_or_error"],
                correlation_ids=tuple(payload["correlation_ids"]),
                causation_ids=tuple(payload["causation_ids"]),
                component_id=payload["component_id"],
                component_version=payload["component_version"],
            )
        except (TypeError, ValueError):
            raise ValidationError(FIXED_MESSAGE) from None
        if validate_audit_event(event):
            raise ValidationError(FIXED_MESSAGE)
        if self.generic_event_id != payload["event_id"]:
            raise ValidationError(FIXED_MESSAGE)
        # Le hash correspond réellement au JSON UTF-8 trié compact du payload.
        # SHA simple sans garantie cryptographique contre un DBA.
        expect = hashlib.sha256(_canonical_generic_bytes(payload)).hexdigest()
        if not _is_hex64(self.generic_event_sha256):
            raise ValidationError(FIXED_MESSAGE)
        if self.maintenance_op_id is None:
            if self.generic_event_sha256 != expect:
                raise ValidationError(FIXED_MESSAGE)
        elif self.current_payload_sha256 != expect:
            raise ValidationError(FIXED_MESSAGE)

    def _clean_pdp(self) -> None:
        if self.generic_payload is not None or self.generic_event_id is not None or self.generic_event_sha256 is not None:
            raise ValidationError(FIXED_MESSAGE)
        try:
            validate_pdp_payload(self.pdp_payload)
            raw = canonical_pdp_bytes(self.pdp_payload)
        except AuditError as error:
            raise ValidationError(FIXED_MESSAGE) from error
        if self.pdp_decision_id != self.pdp_payload["decision_id"]:
            raise ValidationError(FIXED_MESSAGE)
        if self.maintenance_op_id is not None and self.current_payload_sha256 != hashlib.sha256(raw).hexdigest():
            raise ValidationError(FIXED_MESSAGE)
