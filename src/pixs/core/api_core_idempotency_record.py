"""Modele Core idempotence C06 : persistance interne, CHECK/UNIQUE immediats seuls.

Gouvernance : champs restrictifs CoreBase conserves, classification injectee
explicitement depuis la composition/proprietaire C10 au participant ; aucun
defaut permissif, aucun runtime C10 revendique.
Futur migration 0003 : BEFORE UPDATE/DELETE fige cles/empreinte/contexte/
resultat terminal et interdit la suppression ; transition initiale seulement
dans le xid de staging avec CAS ; CONSTRAINT TRIGGER differe distinct relit
l'etat FINAL par cle et refuse IN_PROGRESS au commit. Non installes ici.
Alias/jeton/operation/xid de staging ne valent pas commit.
"""

from __future__ import annotations

import datetime

from django.core.exceptions import ValidationError
from django.db import models

from pixs.core.api_core_serializer_v1 import API_CORE_COMMAND_TYPES, API_CORE_SERIALIZER_VERSION
from pixs.core.dto import CoreInputInvalid, CoreMutationResult
from pixs.core.persistence.base import UUID7_RE, CoreBase
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7
from pixs.core.scope.context import ScopeContext, ScopeStructureError, ScopeType, validate_structure
from pixs.kernel.data_persistence_states import DataPersistenceState
from pixs.kernel.manifest.semver import parse_version

__all__ = ["CoreApiIdempotencyRecord"]

_FIXED = "Enregistrement idempotence Core invalide."


def _invalid() -> ValidationError:
    return ValidationError(_FIXED, code="core_api_idempotency_invalid")


def _is_opaque(v: object) -> bool:
    if type(v) is not str or not v or "\x00" in v:
        return False
    try:
        v.encode("utf-8")
    except UnicodeError:
        return False
    return True


_STATES = ("IN_PROGRESS", "SUCCEEDED")
_PERSIST = tuple(s.value for s in DataPersistenceState)
_WINDOW_EXPR = models.F("completed_at") + models.ExpressionWrapper(models.F("replay_window_seconds") * datetime.timedelta(seconds=1), output_field=models.DurationField())


class CoreApiIdempotencyRecord(CoreBase):
    record_id = models.UUIDField(primary_key=True, editable=False)
    namespace = models.TextField()
    tenant_id = models.TextField(null=True, blank=True, default=None)
    subject_id = models.TextField()
    command_type = models.TextField()
    idempotency_key = models.TextField()
    scope_type = models.TextField()
    context_tenant_id = models.TextField(null=True, blank=True, default=None)
    context_scope_id = models.TextField(null=True, blank=True, default=None)
    content_sha256 = models.TextField()
    serializer_version = models.TextField()
    state = models.TextField(choices=[("IN_PROGRESS", "IN_PROGRESS"), ("SUCCEEDED", "SUCCEEDED")])
    result_operation_id = models.TextField(null=True, blank=True, default=None)
    result_ref = models.TextField(null=True, blank=True, default=None)
    result_version = models.IntegerField(null=True, blank=True, default=None)
    result_persistence_state = models.TextField(null=True, blank=True, default=None)
    result_correlation_id = models.TextField(null=True, blank=True, default=None)
    completed_at = models.DateTimeField(null=True, blank=True, default=None)
    expires_at = models.DateTimeField()
    replay_window_seconds = models.BigIntegerField()
    revision = models.BigIntegerField()
    operation_id = models.TextField()
    db_alias = models.TextField()
    transaction_token = models.TextField()
    staged_xid = models.TextField()

    class Meta(CoreBase.Meta):
        app_label = "pixs_core"
        db_table = "pixs_core_apiidem"
        constraints = [
            *CoreBase.Meta.constraints,
            models.CheckConstraint(condition=models.Q(record_id__regex=UUID7_RE), name="apiidem_record_uuid7_rgx"),
            models.CheckConstraint(condition=models.Q(namespace__in=["PLATFORM", "TENANT"]), name="apiidem_ns_vocab"),
            models.CheckConstraint(condition=models.Q(scope_type__in=["PLATFORM", "TENANT"]), name="apiidem_scope_vocab"),
            models.CheckConstraint(condition=models.Q(namespace=models.F("scope_type")), name="apiidem_ns_eq_scope"),
            models.CheckConstraint(condition=(models.Q(namespace="PLATFORM", tenant_id__isnull=True, context_tenant_id__isnull=True, context_scope_id__isnull=True) | models.Q(namespace="TENANT", tenant_id__isnull=False, context_tenant_id__isnull=False)), name="apiidem_platform_tenant_nulls"),
            models.CheckConstraint(condition=(models.Q(namespace="PLATFORM") | (models.Q(tenant_id=models.F("context_tenant_id")) & ~models.Q(tenant_id="") & ~models.Q(context_tenant_id=""))), name="apiidem_tenant_eq_ctx"),
            models.CheckConstraint(condition=(models.Q(context_scope_id__isnull=True) | ~models.Q(context_scope_id="")), name="apiidem_scope_nonempty"),
            models.CheckConstraint(condition=~models.Q(subject_id=""), name="apiidem_subject_nonempty"),
            models.CheckConstraint(condition=~models.Q(command_type=""), name="apiidem_type_nonempty"),
            models.CheckConstraint(condition=~models.Q(idempotency_key=""), name="apiidem_key_nonempty"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="apiidem_digest_regex"),
            models.CheckConstraint(condition=models.Q(serializer_version=API_CORE_SERIALIZER_VERSION), name="apiidem_serializer_supported"),
            models.CheckConstraint(condition=models.Q(command_type__in=list(API_CORE_COMMAND_TYPES)), name="apiidem_command_supported"),
            models.CheckConstraint(condition=models.Q(state__in=["IN_PROGRESS", "SUCCEEDED"]), name="apiidem_state_member"),
            models.CheckConstraint(condition=(models.Q(state="IN_PROGRESS", completed_at__isnull=True, result_operation_id__isnull=True, result_ref__isnull=True, result_version__isnull=True, result_persistence_state__isnull=True, result_correlation_id__isnull=True) | models.Q(state="SUCCEEDED", completed_at__isnull=False, result_operation_id__isnull=False, result_ref__isnull=False, result_version__isnull=False, result_persistence_state__isnull=False, result_correlation_id__isnull=False)), name="apiidem_state_result_coherence"),
            models.CheckConstraint(condition=(models.Q(result_version__isnull=True) | models.Q(result_version__gte=1)), name="apiidem_result_version_pos"),
            models.CheckConstraint(condition=models.Q(result_operation_id__isnull=True) | ~models.Q(result_operation_id=""), name="apiidem_result_op_nonempty"),
            models.CheckConstraint(condition=models.Q(result_ref__isnull=True) | ~models.Q(result_ref=""), name="apiidem_result_ref_nonempty"),
            models.CheckConstraint(condition=models.Q(result_correlation_id__isnull=True) | ~models.Q(result_correlation_id=""), name="apiidem_result_corr_nonempty"),
            models.CheckConstraint(condition=models.Q(result_operation_id__isnull=True) | models.Q(result_operation_id=models.F("operation_id")), name="apiidem_result_op_binding"),
            models.CheckConstraint(condition=(models.Q(result_persistence_state__isnull=True) | models.Q(result_persistence_state__in=list(_PERSIST))), name="apiidem_result_pers_vocab"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="apiidem_op_nonempty"),
            models.CheckConstraint(condition=~models.Q(db_alias=""), name="apiidem_alias_nonempty"),
            models.CheckConstraint(condition=~models.Q(transaction_token=""), name="apiidem_token_nonempty"),
            models.CheckConstraint(condition=~models.Q(staged_xid=""), name="apiidem_xid_nonempty"),
            models.CheckConstraint(condition=models.Q(replay_window_seconds__gte=1), name="apiidem_window_positive"),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="apiidem_revision_positive"),
            models.CheckConstraint(condition=models.Q(completed_at__isnull=True) | models.Q(completed_at__gte=models.F("created_at")), name="apiidem_completed_gte_created"),
            models.CheckConstraint(condition=models.Q(expires_at__gt=models.F("created_at")), name="apiidem_expires_gt_created"),
            models.CheckConstraint(condition=(models.Q(state="IN_PROGRESS") | models.Q(expires_at__gte=_WINDOW_EXPR)), name="apiidem_retention_minimum"),
            models.UniqueConstraint(fields=["namespace", "tenant_id", "subject_id", "command_type", "idempotency_key"], name="apiidem_key_uq", nulls_distinct=False),
        ]

    def clean(self) -> None:
        try:
            check_uuid7(self.record_id)
        except (Uuid7Error, AttributeError, TypeError, ValueError):
            raise _invalid() from None
        if type(self.namespace) is not str or self.namespace not in ("PLATFORM", "TENANT"):
            raise _invalid()
        if type(self.scope_type) is not str or self.scope_type not in ("PLATFORM", "TENANT"):
            raise _invalid()
        if self.namespace != self.scope_type:
            raise _invalid()
        if self.namespace == "PLATFORM":
            if self.tenant_id is not None or self.context_tenant_id is not None or self.context_scope_id is not None:
                raise _invalid()
        else:
            if not _is_opaque(self.tenant_id) or not _is_opaque(self.context_tenant_id) or self.tenant_id != self.context_tenant_id:
                raise _invalid()
            if self.context_scope_id is not None and not _is_opaque(self.context_scope_id):
                raise _invalid()
        for name in ("subject_id", "command_type", "idempotency_key"):
            if not _is_opaque(getattr(self, name)):
                raise _invalid()
        try:
            ctx = ScopeContext(ScopeType(self.scope_type), self.context_tenant_id, self.context_scope_id)
            validate_structure(ctx)
        except (ScopeStructureError, AttributeError, TypeError, ValueError):
            raise _invalid() from None
        if not _is_opaque(self.content_sha256) or len(self.content_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.content_sha256):
            raise _invalid()
        try:
            parse_version(self.serializer_version)
        except (ValueError, AttributeError, TypeError):
            raise _invalid() from None
        if type(self.command_type) is not str or self.command_type not in API_CORE_COMMAND_TYPES:
            raise _invalid()
        if self.serializer_version != API_CORE_SERIALIZER_VERSION:
            raise _invalid()
        if type(self.state) is not str or self.state not in _STATES:
            raise _invalid()
        for name in ("operation_id", "db_alias", "transaction_token", "staged_xid"):
            if not _is_opaque(getattr(self, name)):
                raise _invalid()
        if type(self.replay_window_seconds) is not int or self.replay_window_seconds < 1:
            raise _invalid()
        try:
            datetime.timedelta(seconds=self.replay_window_seconds)
        except OverflowError:
            raise _invalid() from None
        if type(self.revision) is not int or self.revision < 1:
            raise _invalid()
        if type(self.version) is not int or self.version < 1:
            raise _invalid()
        for name in ("created_at", "updated_at", "expires_at"):
            v = getattr(self, name)
            if type(v) is not datetime.datetime or v.tzinfo is not datetime.timezone.utc:
                raise _invalid()
        if not self.expires_at > self.created_at:
            raise _invalid()
        if self.state == "IN_PROGRESS":
            if self.completed_at is not None or self.result_operation_id is not None or self.result_ref is not None or self.result_version is not None or self.result_persistence_state is not None or self.result_correlation_id is not None:
                raise _invalid()
            return
        if self.completed_at is None or type(self.completed_at) is not datetime.datetime or self.completed_at.tzinfo is not datetime.timezone.utc:
            raise _invalid()
        if not self.completed_at >= self.created_at:
            raise _invalid()
        if type(self.result_ref) is not str or not self.result_ref or type(self.result_operation_id) is not str or not self.result_operation_id or type(self.result_correlation_id) is not str or not self.result_correlation_id:
            raise _invalid()
        if any(not _is_opaque(value) for value in (self.result_operation_id, self.result_ref, self.result_correlation_id)):
            raise _invalid()
        if self.result_operation_id != self.operation_id:
            raise _invalid()
        if type(self.result_version) is not int or self.result_version < 1 or type(self.result_persistence_state) is not str or self.result_persistence_state not in _PERSIST:
            raise _invalid()
        try:
            res = CoreMutationResult(operation_id=self.result_operation_id, result_ref=self.result_ref, version=self.result_version, persistence_state=DataPersistenceState(self.result_persistence_state), correlation_id=self.result_correlation_id)
            res.__post_init__()
        except (CoreInputInvalid, AttributeError, TypeError, ValueError):
            raise _invalid() from None
        try:
            if not self.expires_at >= self.completed_at + datetime.timedelta(seconds=self.replay_window_seconds):
                raise _invalid()
        except OverflowError:
            raise _invalid() from None
