"""Records C09 2.3 : persistance seule, sans boucle ni exécution.

Bail scheduler distinct du bail Job. Schedule ponctuel `due_at/expires_at`
avec clé matérialisée et IDs cibles alloués serveur avant trigger.
Curseur d'ordre par périmètre sous verrou, sans ordre global.
Enveloppe immuable `wire_document` JSON fermé issu de
`c09_envelope_wire_bytes` puis parsé, colonnes matérialisées concordantes
recoupées par le repository à chaque lecture.
Stage outbox preuve physique Core/C05/C06, sans champ `xid` inventé dans
`TransactionProof`. Publication `OneToOne` event sous bail enveloppe.
Livraison une par (event, consumer) figée au stage. Réception inbox
`INSERT` dans la transaction d'effet. Preuve unité générique
`JOB/INBOX` rejouable sans régression. Slots runtime logiques sans preuve OS.

Contraintes SQL nommées portent les invariants représentables. Les garde-fous
`QuerySet.update`/SQL seront posés par déclencheurs en `0013` ; `save()`
insert-only ne couvre que la voie ORM. Retour vide seul en migration.
Aucun import privé Bulk/Core, aucun `JobRecord`/`0012` modifié.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.connection import ConnectionDoesNotExist

from pixs.backend.c09_job_records import C09UtcDateTimeField

__all__ = [
    "C09SchedulerLeaseRecord",
    "C09ScheduleRecord",
    "C09OrderCursorRecord",
    "C09EventEnvelopeRecord",
    "C09OutboxStageRecord",
    "C09OutboxPublicationRecord",
    "C09DeliveryRecord",
    "C09InboxReceiptRecord",
    "C09OwnerUnitProofRecord",
    "C09RuntimeInstanceRecord",
]

_INVALID = "valeurs evenement C09 invalides"


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="c09_event_record_invalid")


def _is_runtime_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeError:
        return False
    return True


def _require_insert_only(instance, using: object) -> None:
    if not _is_runtime_text(using) or instance._state.adding is not True:
        raise _invalid()
    try:
        connection = transaction.get_connection(using)
    except ConnectionDoesNotExist:
        raise _invalid() from None
    if connection.vendor != "postgresql" or connection.in_atomic_block is not True:
        raise _invalid()


def _scope_condition(scope_name="scope_type", tenant_name="tenant_id", id_name="scope_id"):
    return (
        models.Q(**{scope_name: "PLATFORM", tenant_name + "__isnull": True, id_name + "__isnull": True})
        | (
            models.Q(**{scope_name: "TENANT", tenant_name + "__isnull": False})
            & ~models.Q(**{tenant_name: ""})
            & (models.Q(**{id_name + "__isnull": True}) | ~models.Q(**{id_name: ""}))
        )
    )


class C09SchedulerLeaseRecord(models.Model):
    """Bail scheduler persistant, distinct du bail Job."""

    coordinator_ref = models.TextField(primary_key=True, serialize=False)
    perimeter_reference = models.TextField(blank=False)
    scope_type = models.TextField(blank=False)
    tenant_id = models.TextField(blank=True, null=True)
    scope_id = models.TextField(blank=True, null=True)
    policy_reference = models.TextField(blank=False)
    policy_version = models.TextField(blank=False)
    policy_sha256 = models.TextField(blank=False)
    owner_reference = models.TextField(blank=True, null=True)
    lease_expires_at = C09UtcDateTimeField(blank=True, null=True)
    generation = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    revision = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    admission_closed = models.BooleanField()

    class Meta:
        constraints = [
            models.CheckConstraint(condition=_scope_condition(), name="c09sched_context_shape"),
            models.CheckConstraint(condition=~models.Q(coordinator_ref=""), name="c09sched_coord_non_empty"),
            models.CheckConstraint(condition=~models.Q(perimeter_reference=""), name="c09sched_perimeter_non_empty"),
            models.CheckConstraint(condition=models.Q(scope_type__in=["PLATFORM", "TENANT"]), name="c09sched_scope_member"),
            models.CheckConstraint(condition=models.Q(tenant_id__isnull=True) | ~models.Q(tenant_id=""), name="c09sched_tenant_empty"),
            models.CheckConstraint(condition=models.Q(scope_id__isnull=True) | ~models.Q(scope_id=""), name="c09sched_scope_empty"),
            models.CheckConstraint(condition=~models.Q(policy_reference=""), name="c09sched_policy_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(policy_version=""), name="c09sched_policy_version_non_empty"),
            models.CheckConstraint(condition=models.Q(policy_sha256__regex="^[0-9a-f]{64}$"), name="c09sched_policy_sha_hex"),
            models.CheckConstraint(condition=models.Q(owner_reference__isnull=True) | ~models.Q(owner_reference=""), name="c09sched_owner_empty"),
            models.CheckConstraint(
                condition=(
                    models.Q(owner_reference__isnull=True, lease_expires_at__isnull=True)
                    | models.Q(owner_reference__isnull=False, lease_expires_at__isnull=False)
                ),
                name="c09sched_lease_pair",
            ),
            models.CheckConstraint(condition=models.Q(generation__gte=1), name="c09sched_generation_gte_1"),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="c09sched_revision_gte_1"),
        ]


class C09ScheduleRecord(models.Model):
    """Déclencheur ponctuel, identités et dates gelées avant trigger."""

    schedule_ref = models.TextField(primary_key=True, serialize=False)
    coordinator = models.ForeignKey(
        "backend.C09SchedulerLeaseRecord",
        db_column="coordinator_ref",
        on_delete=models.PROTECT,
        related_name="+",
    )
    identity_document = models.JSONField(blank=False, null=False)
    policy_sha256 = models.TextField(blank=False)
    actor_reference = models.TextField(blank=False)
    perimeter_reference = models.TextField(blank=False)
    handler_reference = models.TextField(blank=False)
    handler_version = models.TextField(blank=False)
    dedup_key = models.TextField(blank=False)
    policy_reference = models.TextField(blank=False)
    policy_version = models.TextField(blank=False)
    content_sha256 = models.TextField(blank=False)
    job_id = models.TextField(blank=False)
    command_id = models.TextField(blank=False)
    operation_id = models.TextField(blank=False)
    due_at = C09UtcDateTimeField()
    expires_at = C09UtcDateTimeField()
    state = models.TextField(blank=False)
    revision = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    failure_code = models.TextField(blank=True, null=True)
    confirmed_job = models.ForeignKey(
        "backend.JobRecord",
        db_column="confirmed_job_id",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(schedule_ref=""), name="c09schedule_ref_non_empty"),
            models.CheckConstraint(condition=models.Q(policy_sha256__regex="^[0-9a-f]{64}$"), name="c09schedule_policy_sha_hex"),
            models.CheckConstraint(condition=~models.Q(actor_reference=""), name="c09schedule_actor_non_empty"),
            models.CheckConstraint(condition=~models.Q(perimeter_reference=""), name="c09schedule_perimeter_non_empty"),
            models.CheckConstraint(condition=~models.Q(handler_reference=""), name="c09schedule_handler_non_empty"),
            models.CheckConstraint(condition=~models.Q(handler_version=""), name="c09schedule_handler_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(dedup_key=""), name="c09schedule_dedup_non_empty"),
            models.CheckConstraint(condition=~models.Q(policy_reference=""), name="c09schedule_policy_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(policy_version=""), name="c09schedule_policy_version_non_empty"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex="^[0-9a-f]{64}$"), name="c09schedule_sha_hex"),
            models.CheckConstraint(condition=~models.Q(job_id=""), name="c09schedule_jobid_non_empty"),
            models.CheckConstraint(condition=~models.Q(command_id=""), name="c09schedule_command_non_empty"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="c09schedule_operation_non_empty"),
            models.CheckConstraint(
                condition=~models.Q(job_id=models.F("command_id"))
                & ~models.Q(job_id=models.F("operation_id"))
                & ~models.Q(command_id=models.F("operation_id")),
                name="c09schedule_ids_distinct",
            ),
            models.CheckConstraint(condition=models.Q(due_at__lte=models.F("expires_at")), name="c09schedule_due_bounded"),
            models.CheckConstraint(
                condition=models.Q(state__in=["PENDING", "TRIGGERED", "FAILED", "PAUSED", "CANCELLED"]),
                name="c09schedule_state_member",
            ),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="c09schedule_revision_gte_1"),
            models.CheckConstraint(
                condition=models.Q(failure_code__isnull=True) | models.Q(failure_code__in=[
                    "CONTEXT_REFUSED", "DEADLINE_EXPIRED", "POLICY_DIVERGENT",
                    "INPUT_INVALID", "TARGET_REFUSED", "RESTORE_UNPROVED",
                ]),
                name="c09schedule_failure_empty",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(state="TRIGGERED", confirmed_job__isnull=False)
                    & models.Q(confirmed_job_id=models.F("job_id"))
                ) | (~models.Q(state="TRIGGERED") & models.Q(confirmed_job__isnull=True)),
                name="c09schedule_triggered_job",
            ),
            models.UniqueConstraint(
                fields=["perimeter_reference", "actor_reference", "handler_reference", "handler_version", "dedup_key"],
                name="c09schedule_key_unique",
            ),
        ]


class C09OrderCursorRecord(models.Model):
    """Curseur canonique par périmètre, progression sous verrou."""

    id = models.BigAutoField(primary_key=True, serialize=False)
    perimeter_reference = models.TextField(blank=False)
    scope_type = models.TextField(blank=False)
    tenant_id = models.TextField(blank=True, null=True)
    scope_id = models.TextField(blank=True, null=True)
    order_scope_reference = models.TextField(blank=False)
    last_sequence = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    revision = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.CheckConstraint(condition=_scope_condition(), name="c09cursor_context_shape"),
            models.CheckConstraint(condition=~models.Q(perimeter_reference=""), name="c09cursor_perimeter_non_empty"),
            models.CheckConstraint(condition=models.Q(scope_type__in=["PLATFORM", "TENANT"]), name="c09cursor_scope_member"),
            models.CheckConstraint(condition=models.Q(tenant_id__isnull=True) | ~models.Q(tenant_id=""), name="c09cursor_tenant_empty"),
            models.CheckConstraint(condition=models.Q(scope_id__isnull=True) | ~models.Q(scope_id=""), name="c09cursor_scope_empty"),
            models.CheckConstraint(condition=~models.Q(order_scope_reference=""), name="c09cursor_order_non_empty"),
            models.CheckConstraint(condition=models.Q(last_sequence__gte=0), name="c09cursor_seq_gte_0"),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="c09cursor_revision_gte_1"),
            models.UniqueConstraint(
                fields=["perimeter_reference", "scope_type", "tenant_id", "scope_id", "order_scope_reference"],
                nulls_distinct=False,
                name="c09cursor_canon_unique",
            ),
        ]


class C09EventEnvelopeRecord(models.Model):
    """Enveloppe immuable, document fermé + colonnes concordantes."""

    event_id = models.TextField(primary_key=True, serialize=False)
    cursor = models.ForeignKey(
        "backend.C09OrderCursorRecord",
        on_delete=models.PROTECT,
        related_name="+",
    )
    sequence_index = models.BigIntegerField(validators=[MinValueValidator(1)])
    kind = models.TextField(blank=False)
    entry_reference = models.TextField(blank=False)
    event_type = models.TextField(blank=False)
    event_version = models.TextField(blank=False)
    producer_reference = models.TextField(blank=False)
    schema_reference = models.TextField(blank=False)
    order_scope_reference = models.TextField(blank=False)
    perimeter_reference = models.TextField(blank=False)
    occurred_at = C09UtcDateTimeField()
    request_content_sha256 = models.TextField(blank=False)
    content_sha256 = models.TextField(blank=False)
    wire_document = models.JSONField(blank=False, null=False)

    def save(self, *args, force_insert=None, force_update=False, using=None, update_fields=None) -> None:
        if args:
            raise _invalid()
        if force_insert is not True:
            raise _invalid()
        if force_update is not False:
            raise _invalid()
        if update_fields is not None:
            raise _invalid()
        _require_insert_only(self, using)
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(event_id=""), name="c09envelope_event_non_empty"),
            models.CheckConstraint(condition=models.Q(sequence_index__gte=1), name="c09envelope_seq_gte_1"),
            models.CheckConstraint(condition=models.Q(kind__in=["DOMAIN", "INTEGRATION"]), name="c09envelope_kind_member"),
            models.CheckConstraint(condition=~models.Q(entry_reference=""), name="c09envelope_entry_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_type=""), name="c09envelope_type_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_version=""), name="c09envelope_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(producer_reference=""), name="c09envelope_producer_non_empty"),
            models.CheckConstraint(condition=~models.Q(schema_reference=""), name="c09envelope_schema_non_empty"),
            models.CheckConstraint(condition=~models.Q(order_scope_reference=""), name="c09envelope_order_non_empty"),
            models.CheckConstraint(condition=~models.Q(perimeter_reference=""), name="c09envelope_perimeter_non_empty"),
            models.CheckConstraint(condition=models.Q(request_content_sha256__regex="^[0-9a-f]{64}$"), name="c09envelope_request_sha_hex"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex="^[0-9a-f]{64}$"), name="c09envelope_sha_hex"),
            models.UniqueConstraint(fields=["cursor", "sequence_index"], name="c09envelope_cursor_seq_unique"),
        ]


class C09OutboxStageRecord(models.Model):
    """Preuve immuable de stage outbox liée à la transaction propriétaire."""

    event = models.OneToOneField(
        "backend.C09EventEnvelopeRecord",
        db_column="event_id",
        primary_key=True,
        serialize=False,
        on_delete=models.PROTECT,
        related_name="+",
    )
    operation_id = models.TextField(blank=False)
    transaction_token = models.TextField(blank=False)
    staged_xid = models.TextField(blank=False)
    context_scope_type = models.TextField(blank=False)
    context_tenant_id = models.TextField(blank=True, null=True)
    context_scope_id = models.TextField(blank=True, null=True)
    owner_unit_ref = models.TextField(blank=True, null=True)
    prepared_at = C09UtcDateTimeField()

    def save(self, *args, force_insert=None, force_update=False, using=None, update_fields=None) -> None:
        if args:
            raise _invalid()
        if force_insert is not True:
            raise _invalid()
        if force_update is not False:
            raise _invalid()
        if update_fields is not None:
            raise _invalid()
        _require_insert_only(self, using)
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=_scope_condition("context_scope_type", "context_tenant_id", "context_scope_id"), name="c09stage_context_shape"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="c09stage_operation_non_empty"),
            models.CheckConstraint(condition=~models.Q(transaction_token=""), name="c09stage_token_non_empty"),
            models.CheckConstraint(condition=~models.Q(staged_xid=""), name="c09stage_xid_non_empty"),
            models.CheckConstraint(condition=models.Q(context_scope_type__in=["PLATFORM", "TENANT"]), name="c09stage_scope_member"),
            models.CheckConstraint(condition=models.Q(context_tenant_id__isnull=True) | ~models.Q(context_tenant_id=""), name="c09stage_tenant_empty"),
            models.CheckConstraint(condition=models.Q(context_scope_id__isnull=True) | ~models.Q(context_scope_id=""), name="c09stage_scopeid_empty"),
            models.CheckConstraint(condition=models.Q(owner_unit_ref__isnull=True) | ~models.Q(owner_unit_ref=""), name="c09stage_ownerunit_empty"),
        ]


class C09OutboxPublicationRecord(models.Model):
    """État de publication d'une enveloppe sous bail enveloppe."""

    event = models.OneToOneField(
        "backend.C09EventEnvelopeRecord",
        db_column="event_id",
        primary_key=True,
        serialize=False,
        on_delete=models.PROTECT,
        related_name="+",
    )
    delivery_policy_reference = models.TextField(blank=False)
    delivery_policy_version = models.TextField(blank=False)
    delivery_policy_sha256 = models.TextField(blank=False)
    state = models.TextField(blank=False)
    revision = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    generation = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    owner_reference = models.TextField(blank=True, null=True)
    lease_expires_at = C09UtcDateTimeField(blank=True, null=True)
    attempt_count = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    next_attempt_at = C09UtcDateTimeField(blank=True, null=True)
    attempt_deadline = C09UtcDateTimeField(blank=True, null=True)
    publication_deadline = C09UtcDateTimeField()
    published_at = C09UtcDateTimeField(blank=True, null=True)
    failure_code = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(state="RUNNING", owner_reference__isnull=False, attempt_deadline__isnull=False)
                    | (~models.Q(state="RUNNING") & models.Q(owner_reference__isnull=True, attempt_deadline__isnull=True))
                ), name="c09pub_running_lease",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(state="RETRYING", next_attempt_at__isnull=False)
                    | (~models.Q(state="RETRYING") & models.Q(next_attempt_at__isnull=True))
                ), name="c09pub_retry_due",
            ),
            models.CheckConstraint(
                condition=models.Q(attempt_deadline__isnull=True) | models.Q(attempt_deadline__lte=models.F("publication_deadline")),
                name="c09pub_attempt_bounded",
            ),
            models.CheckConstraint(
                condition=models.Q(lease_expires_at__isnull=True) | models.Q(lease_expires_at__lte=models.F("attempt_deadline")),
                name="c09pub_lease_bounded",
            ),
            models.CheckConstraint(
                condition=models.Q(next_attempt_at__isnull=True) | models.Q(next_attempt_at__lte=models.F("publication_deadline")),
                name="c09pub_due_bounded",
            ),
            models.CheckConstraint(condition=~models.Q(delivery_policy_reference=""), name="c09pub_policy_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(delivery_policy_version=""), name="c09pub_policy_version_non_empty"),
            models.CheckConstraint(condition=models.Q(delivery_policy_sha256__regex="^[0-9a-f]{64}$"), name="c09pub_policy_sha_hex"),
            models.CheckConstraint(
                condition=models.Q(state__in=["PENDING", "RUNNING", "RETRYING", "PUBLISHED", "FAILED", "DEAD_LETTER", "PAUSED"]),
                name="c09pub_state_member",
            ),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="c09pub_revision_gte_1"),
            models.CheckConstraint(condition=models.Q(generation__gte=1), name="c09pub_generation_gte_1"),
            models.CheckConstraint(condition=models.Q(owner_reference__isnull=True) | ~models.Q(owner_reference=""), name="c09pub_owner_empty"),
            models.CheckConstraint(
                condition=(
                    models.Q(owner_reference__isnull=True, lease_expires_at__isnull=True)
                    | models.Q(owner_reference__isnull=False, lease_expires_at__isnull=False)
                ),
                name="c09pub_lease_pair",
            ),
            models.CheckConstraint(condition=models.Q(attempt_count__gte=0), name="c09pub_attempt_gte_0"),
            models.CheckConstraint(condition=models.Q(failure_code__isnull=True) | models.Q(failure_code__in=[
                "CONTEXT_REFUSED", "DEADLINE_EXPIRED", "BUSINESS_REFUSED", "RETRYABLE_ERROR",
                "RETRY_EXHAUSTED", "LEASE_EXPIRED", "STOP_REQUESTED", "POLICY_DIVERGENT", "RESTORE_UNPROVED",
            ]), name="c09pub_failure_empty"),
            models.CheckConstraint(condition=(
                models.Q(state="PUBLISHED", published_at__isnull=False)
                | (~models.Q(state="PUBLISHED") & models.Q(published_at__isnull=True))
            ), name="c09pub_published_at"),
        ]


class C09DeliveryRecord(models.Model):
    """Livraison par destinataire, snapshot figé au stage."""

    id = models.BigAutoField(primary_key=True, serialize=False)
    event = models.ForeignKey(
        "backend.C09EventEnvelopeRecord",
        db_column="event_id",
        on_delete=models.PROTECT,
        related_name="+",
    )
    consumer_reference = models.TextField(blank=False)
    consumer_version = models.TextField(blank=False)
    event_version = models.TextField(blank=False)
    component_reference = models.TextField(blank=False)
    entry_reference = models.TextField(blank=False)
    declaration_snapshot = models.JSONField(blank=False, null=False)
    governance_reference = models.TextField(blank=True, null=True)
    state = models.TextField(blank=False)
    revision = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    receipt_reference = models.TextField(blank=True, null=True)
    outcome_reference = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(consumer_reference=""), name="c09delivery_consumer_non_empty"),
            models.CheckConstraint(condition=~models.Q(consumer_version=""), name="c09delivery_consumer_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_version=""), name="c09delivery_event_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(component_reference=""), name="c09delivery_component_non_empty"),
            models.CheckConstraint(condition=~models.Q(entry_reference=""), name="c09delivery_entry_non_empty"),
            models.CheckConstraint(condition=models.Q(governance_reference__isnull=True) | ~models.Q(governance_reference=""), name="c09delivery_gov_empty"),
            models.CheckConstraint(condition=models.Q(state__in=["PENDING", "CONFIRMED", "REFUSED"]), name="c09delivery_state_member"),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="c09delivery_revision_gte_1"),
            models.CheckConstraint(condition=models.Q(receipt_reference__isnull=True) | ~models.Q(receipt_reference=""), name="c09delivery_receipt_empty"),
            models.CheckConstraint(condition=models.Q(outcome_reference__isnull=True) | ~models.Q(outcome_reference=""), name="c09delivery_outcome_empty"),
            models.UniqueConstraint(fields=["event", "consumer_reference"], name="c09delivery_event_consumer_unique"),
        ]


class C09InboxReceiptRecord(models.Model):
    """Réception consommateur, insérée dans la transaction d'effet."""

    id = models.BigAutoField(primary_key=True, serialize=False)
    consumer_reference = models.TextField(blank=False)
    event = models.ForeignKey(
        "backend.C09EventEnvelopeRecord", db_column="event_id",
        on_delete=models.PROTECT, related_name="+",
    )
    delivery = models.OneToOneField(
        "backend.C09DeliveryRecord", on_delete=models.PROTECT, related_name="+",
    )
    identity_document = models.JSONField(blank=False, null=False)
    request_version = models.TextField(blank=False)
    request_content_sha256 = models.TextField(blank=False)
    correlation_id = models.TextField(blank=False)
    scope_type = models.TextField(blank=False)
    tenant_id = models.TextField(blank=True, null=True)
    scope_id = models.TextField(blank=True, null=True)
    consumer_version = models.TextField(blank=False)
    event_version = models.TextField(blank=False)
    content_sha256 = models.TextField(blank=False)
    result_reference = models.TextField(blank=False)
    checkpoint_reference = models.TextField(blank=False)
    actor_reference = models.TextField(blank=False)
    perimeter_reference = models.TextField(blank=False)
    request_reference = models.TextField(blank=False)
    operation_id = models.TextField(blank=False)
    transaction_token = models.TextField(blank=False)
    consumed_xid = models.TextField(blank=False)
    consumed_at = C09UtcDateTimeField()

    def save(self, *args, force_insert=None, force_update=False, using=None, update_fields=None) -> None:
        if args:
            raise _invalid()
        if force_insert is not True:
            raise _invalid()
        if force_update is not False:
            raise _invalid()
        if update_fields is not None:
            raise _invalid()
        _require_insert_only(self, using)
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=_scope_condition(), name="c09inbox_context_shape"),
            models.CheckConstraint(condition=~models.Q(request_version=""), name="c09inbox_request_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(correlation_id=""), name="c09inbox_correlation_non_empty"),
            models.CheckConstraint(condition=models.Q(request_content_sha256__regex="^[0-9a-f]{64}$"), name="c09inbox_request_sha_hex"),
            models.CheckConstraint(condition=~models.Q(consumer_reference=""), name="c09inbox_consumer_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_id=""), name="c09inbox_event_non_empty"),
            models.CheckConstraint(condition=~models.Q(consumer_version=""), name="c09inbox_consumer_version_non_empty"),
            models.CheckConstraint(condition=~models.Q(event_version=""), name="c09inbox_version_non_empty"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex="^[0-9a-f]{64}$"), name="c09inbox_digest_hex"),
            models.CheckConstraint(condition=~models.Q(result_reference=""), name="c09inbox_result_non_empty"),
            models.CheckConstraint(condition=~models.Q(checkpoint_reference=""), name="c09inbox_checkpoint_non_empty"),
            models.CheckConstraint(condition=~models.Q(actor_reference=""), name="c09inbox_actor_non_empty"),
            models.CheckConstraint(condition=~models.Q(perimeter_reference=""), name="c09inbox_perimeter_non_empty"),
            models.CheckConstraint(condition=~models.Q(request_reference=""), name="c09inbox_request_non_empty"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="c09inbox_operation_non_empty"),
            models.CheckConstraint(condition=~models.Q(transaction_token=""), name="c09inbox_token_non_empty"),
            models.CheckConstraint(condition=~models.Q(consumed_xid=""), name="c09inbox_xid_non_empty"),
            models.UniqueConstraint(fields=["consumer_reference", "event"], name="c09inbox_consumer_event_unique"),
        ]


class C09OwnerUnitProofRecord(models.Model):
    """Preuve unité générique JOB/INBOX, rejouable sans régression."""

    id = models.BigAutoField(primary_key=True, serialize=False)
    owner_kind = models.TextField(blank=False)
    owner_ref = models.TextField(blank=False)
    unit_ref = models.TextField(blank=False)
    command_type = models.TextField(blank=False)
    idempotency_key = models.TextField(blank=False)
    content_sha256 = models.TextField(blank=False)
    serializer_version = models.TextField(blank=False)
    correlation_id = models.TextField(blank=False)
    operation_id = models.TextField(blank=False)
    transaction_token = models.TextField(blank=False)
    staged_xid = models.TextField(blank=False)
    actor_reference = models.TextField(blank=False)
    perimeter_reference = models.TextField(blank=False)
    request_reference = models.TextField(blank=False)
    request_version = models.TextField(blank=False)
    scope_type = models.TextField(blank=False)
    owner_identity_document = models.JSONField(blank=False, null=False)
    command_request_document = models.JSONField(blank=False, null=False)
    request_content_sha256 = models.TextField(blank=False)
    tenant_id = models.TextField(blank=True, null=True)
    scope_id = models.TextField(blank=True, null=True)
    checkpoint_reference = models.TextField(blank=False)
    complete = models.BooleanField()
    result_document = models.JSONField(blank=False, null=False)
    result_sha256 = models.TextField(blank=False)
    prepared_at = C09UtcDateTimeField()

    def save(self, *args, force_insert=None, force_update=False, using=None, update_fields=None) -> None:
        if args:
            raise _invalid()
        if force_insert is not True:
            raise _invalid()
        if force_update is not False:
            raise _invalid()
        if update_fields is not None:
            raise _invalid()
        _require_insert_only(self, using)
        return super().save(force_insert=True, force_update=False, using=using, update_fields=None)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=_scope_condition(), name="c09unit_context_shape"),
            models.CheckConstraint(condition=models.Q(request_content_sha256__regex="^[0-9a-f]{64}$"), name="c09unit_request_sha_hex"),
            models.CheckConstraint(condition=models.Q(owner_kind__in=["JOB", "INBOX"]), name="c09unit_kind_member"),
            models.CheckConstraint(condition=~models.Q(owner_ref=""), name="c09unit_owner_non_empty"),
            models.CheckConstraint(condition=~models.Q(unit_ref=""), name="c09unit_unit_non_empty"),
            models.CheckConstraint(condition=~models.Q(command_type=""), name="c09unit_command_non_empty"),
            models.CheckConstraint(condition=~models.Q(idempotency_key=""), name="c09unit_key_non_empty"),
            models.CheckConstraint(condition=models.Q(content_sha256__regex="^[0-9a-f]{64}$"), name="c09unit_sha_hex"),
            models.CheckConstraint(condition=~models.Q(serializer_version=""), name="c09unit_serializer_non_empty"),
            models.CheckConstraint(condition=~models.Q(correlation_id=""), name="c09unit_correlation_non_empty"),
            models.CheckConstraint(condition=~models.Q(operation_id=""), name="c09unit_operation_non_empty"),
            models.CheckConstraint(condition=~models.Q(transaction_token=""), name="c09unit_token_non_empty"),
            models.CheckConstraint(condition=~models.Q(staged_xid=""), name="c09unit_xid_non_empty"),
            models.CheckConstraint(condition=~models.Q(actor_reference=""), name="c09unit_actor_non_empty"),
            models.CheckConstraint(condition=~models.Q(perimeter_reference=""), name="c09unit_perimeter_non_empty"),
            models.CheckConstraint(condition=~models.Q(request_reference=""), name="c09unit_request_non_empty"),
            models.CheckConstraint(condition=~models.Q(request_version=""), name="c09unit_request_version_non_empty"),
            models.CheckConstraint(condition=models.Q(tenant_id__isnull=True) | ~models.Q(tenant_id=""), name="c09unit_tenant_empty"),
            models.CheckConstraint(condition=models.Q(scope_id__isnull=True) | ~models.Q(scope_id=""), name="c09unit_scope_empty"),
            models.CheckConstraint(condition=~models.Q(checkpoint_reference=""), name="c09unit_checkpoint_non_empty"),
            models.CheckConstraint(condition=models.Q(result_sha256__regex="^[0-9a-f]{64}$"), name="c09unit_result_sha_hex"),
            models.UniqueConstraint(fields=["owner_kind", "owner_ref", "unit_ref"], name="c09unit_owner_unit_unique"),
        ]


class C09RuntimeInstanceRecord(models.Model):
    """Slot logique de rôle, sans preuve d'application OS."""

    instance_ref = models.TextField(primary_key=True, serialize=False)
    owner_reference = models.TextField(blank=False)
    role = models.TextField(blank=False)
    plan_reference = models.TextField(blank=False)
    plan_version = models.TextField(blank=False)
    plan_sha256 = models.TextField(blank=False)
    budget_reference = models.TextField(blank=False)
    budget_version = models.TextField(blank=False)
    lease_owner = models.TextField(blank=True, null=True)
    lease_expires_at = C09UtcDateTimeField(blank=True, null=True)
    generation = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    revision = models.BigIntegerField(default=1, validators=[MinValueValidator(1)])
    admission_closed = models.BooleanField()
    inflight_count = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    stop_state = models.TextField(blank=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(instance_ref=""), name="c09runtime_instance_non_empty"),
            models.CheckConstraint(condition=~models.Q(owner_reference=""), name="c09runtime_owner_non_empty"),
            models.CheckConstraint(condition=models.Q(role__in=["WEB", "WORKER", "SCHEDULER"]), name="c09runtime_role_member"),
            models.CheckConstraint(condition=~models.Q(plan_reference=""), name="c09runtime_plan_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(plan_version=""), name="c09runtime_plan_version_non_empty"),
            models.CheckConstraint(condition=models.Q(plan_sha256__regex="^[0-9a-f]{64}$"), name="c09runtime_plan_sha_hex"),
            models.CheckConstraint(condition=~models.Q(budget_reference=""), name="c09runtime_budget_ref_non_empty"),
            models.CheckConstraint(condition=~models.Q(budget_version=""), name="c09runtime_budget_version_non_empty"),
            models.CheckConstraint(condition=models.Q(lease_owner__isnull=True) | ~models.Q(lease_owner=""), name="c09runtime_lease_owner_empty"),
            models.CheckConstraint(
                condition=(
                    models.Q(lease_owner__isnull=True, lease_expires_at__isnull=True)
                    | models.Q(lease_owner__isnull=False, lease_expires_at__isnull=False)
                ),
                name="c09runtime_lease_pair",
            ),
            models.CheckConstraint(condition=models.Q(generation__gte=1), name="c09runtime_generation_gte_1"),
            models.CheckConstraint(condition=models.Q(revision__gte=1), name="c09runtime_revision_gte_1"),
            models.CheckConstraint(condition=models.Q(inflight_count__gte=0), name="c09runtime_inflight_gte_0"),
            models.CheckConstraint(
                condition=models.Q(stop_state__in=["STARTING", "RUNNING", "DRAINING", "STOPPED", "UNKNOWN"]),
                name="c09runtime_stop_member",
            ),
        ]
