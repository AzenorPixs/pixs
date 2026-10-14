"""Persistance runtime Bulk v1 : extension, checkpoint, liaison, ordonnancement.

Quatre modèles conformes aux annexes approuvées, sans défaut de modèle, sans
auto timestamp et sans champ logique supplémentaire. from_values valide avant
tout accès ORM ; save() reste standard, sans full_clean implicite. Les
contraintes SQL ne prouvent ni SemVer, ni type Python exact, ni existence métier des références opaques, ni
autorisation. La validation combinée des trente-six clés avec le Record réel
appartient au repository, pas à ces modèles.
"""

import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from django.core.exceptions import ValidationError
from django.db import models

from pixs.backend.bulk_execution_values import validate_bulk_progress_values
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "BulkOperationExecutionRecord",
    "BulkCheckpointRecord",
    "BulkJobBindingRecord",
    "BulkJobScheduleRecord",
]

_INVALID = "données runtime bulk invalides"
_EXECUTION_VERSION = "1.0.0"
_PHASES = ("STAGE", "VALIDATE", "APPLY", "EXPORT")
_CONSISTENCY_KINDS = ("SNAPSHOT", "WATERMARK")
_PHASE_CHOICES = [(phase, phase) for phase in _PHASES]
_KIND_CHOICES = [(kind, kind) for kind in _CONSISTENCY_KINDS]
_SHA256_PATTERN = re.compile("[0-9a-f]{64}")
_INT64_MAX = 2**63 - 1

_EXTENSION_KEYS = (
    "execution_version",
    "requested_by_reference",
    "resolved_context_reference",
    "mapping_reference",
    "mapping_version",
    "input_reference",
    "input_version",
    "input_sha256",
    "input_size_bytes",
    "output_reference",
    "output_version",
    "output_sha256",
    "output_size_bytes",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
    "idempotency_key",
    "correlation_id",
    "causation_id",
    "progress",
    "checkpoint_reference",
    "result_reference",
    "expires_at",
    "policy_reference",
    "policy_version",
    "revision",
    "cancellation_requested",
)
_EXTENSION_TEXT_REQUIRED = (
    "requested_by_reference",
    "resolved_context_reference",
    "mapping_reference",
    "idempotency_key",
    "correlation_id",
    "policy_reference",
)
_EXTENSION_SEMVER_FIELDS = ("mapping_version", "policy_version")
_EXTENSION_TEXT_NULLABLE = (
    "input_reference",
    "input_version",
    "output_reference",
    "output_version",
    "projection_reference",
    "consistency_reference",
    "causation_id",
    "checkpoint_reference",
    "result_reference",
)
_EXTENSION_SHA_NULLABLE = ("input_sha256", "output_sha256")
_EXTENSION_SIZE_NULLABLE = ("input_size_bytes", "output_size_bytes")
_EXTENSION_SQL_TEXT_REQUIRED = (
    "execution_version",
    *_EXTENSION_TEXT_REQUIRED,
    *_EXTENSION_SEMVER_FIELDS,
)
_EXTENSION_SQL_TEXT_NULLABLE = (
    *_EXTENSION_TEXT_NULLABLE,
    *_EXTENSION_SHA_NULLABLE,
)

_CHECKPOINT_KEYS = (
    "checkpoint_id",
    "operation_id",
    "phase",
    "source_fingerprint",
    "mapping_version",
    "committed_unit_index",
    "progress",
    "revision",
    "owner_result_reference",
)
_BINDING_KEYS = ("operation_id", "job_id", "phase")
_SCHEDULE_KEYS = (
    "job_id",
    "policy_reference",
    "policy_version",
    "next_run_at",
    "attempt_deadline",
    "failure_code",
    "revision",
)


def _invalid() -> ValidationError:
    return ValidationError(_INVALID, code="bulk_runtime_record_invalid")


def _is_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_optional_text(value: object) -> bool:
    return value is None or _is_text(value)


def _is_sha64(value: object) -> bool:
    return type(value) is str and _SHA256_PATTERN.fullmatch(value) is not None


def _is_optional_sha64(value: object) -> bool:
    return value is None or _is_sha64(value)


def _is_semver(value: object) -> bool:
    if not _is_text(value):
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _is_revision(value: object) -> bool:
    return type(value) is int and value >= 1


def _is_index(value: object) -> bool:
    return type(value) is int and value >= 0


def _is_optional_index(value: object) -> bool:
    return value is None or _is_index(value)


def _is_utc_instant(value: object) -> bool:
    return type(value) is datetime and value.tzinfo is timezone.utc


def _is_optional_utc_instant(value: object) -> bool:
    return value is None or _is_utc_instant(value)


def _is_phase(value: object) -> bool:
    return type(value) is str and value in _PHASES


def _is_optional_kind(value: object) -> bool:
    return value is None or (
        type(value) is str and value in _CONSISTENCY_KINDS
    )


def _is_progress(value: object) -> bool:
    return not validate_bulk_progress_values(value)


def _exact_keys(values: object, fields: tuple) -> dict | None:
    if type(values) is not dict:
        return None
    items = tuple(values.items())
    if any(type(key) is not str for key, _ in items):
        return None
    snapshot = dict(items)
    if len(snapshot) != len(fields):
        return None
    if any(field not in snapshot for field in fields):
        return None
    return snapshot


def _types_valid(values: dict, fields: dict, nullable: frozenset) -> bool:
    for name, kind in fields.items():
        value = values[name]
        if value is None and name in nullable:
            continue
        if type(value) is not kind:
            return False
    for name, kind in fields.items():
        value = values[name]
        if kind is datetime and value is not None and value.tzinfo is not timezone.utc:
            return False
    if "progress" in fields and validate_bulk_progress_values(values["progress"]):
        return False
    return True


def _check_capacity(values: dict, fields: tuple) -> None:
    if any(values[name] is not None and values[name] > _INT64_MAX for name in fields):
        raise ValidationError(
            "capacité entière PostgreSQL non supportée",
            code="bulk_runtime_capacity_unsupported",
        )


_EXTENSION_TYPES = {
    name: str for name in (
        "execution_version", *_EXTENSION_TEXT_REQUIRED,
        *_EXTENSION_SEMVER_FIELDS, *_EXTENSION_TEXT_NULLABLE,
        *_EXTENSION_SHA_NULLABLE, "consistency_kind",
    )
}
_EXTENSION_TYPES.update({
    "input_size_bytes": int, "output_size_bytes": int,
    "progress": dict, "expires_at": datetime, "revision": int,
    "cancellation_requested": bool,
})
_EXTENSION_NULLABLE = frozenset((
    *_EXTENSION_TEXT_NULLABLE, *_EXTENSION_SHA_NULLABLE,
    *_EXTENSION_SIZE_NULLABLE, "consistency_kind",
))
_CHECKPOINT_TYPES = {
    "checkpoint_id": str, "operation_id": str, "phase": str,
    "source_fingerprint": str, "mapping_version": str,
    "committed_unit_index": int, "progress": dict, "revision": int,
    "owner_result_reference": str,
}
_BINDING_TYPES = {"operation_id": str, "job_id": str, "phase": str}
_SCHEDULE_TYPES = {
    "job_id": str, "policy_reference": str, "policy_version": str,
    "next_run_at": datetime, "attempt_deadline": datetime,
    "failure_code": str, "revision": int,
}


def _extension_refusals(values: dict) -> bool:
    if not _types_valid(values, _EXTENSION_TYPES, _EXTENSION_NULLABLE):
        return True
    if not _is_text(values["execution_version"]):
        return True
    if values["execution_version"] != _EXECUTION_VERSION:
        return True
    if any(not _is_text(values[name]) for name in _EXTENSION_TEXT_REQUIRED):
        return True
    if any(not _is_semver(values[name]) for name in _EXTENSION_SEMVER_FIELDS):
        return True
    if any(
        not _is_optional_text(values[name])
        for name in _EXTENSION_TEXT_NULLABLE
    ):
        return True
    if any(
        not _is_optional_sha64(values[name]) for name in _EXTENSION_SHA_NULLABLE
    ):
        return True
    if any(
        not _is_optional_index(values[name])
        for name in _EXTENSION_SIZE_NULLABLE
    ):
        return True
    if not _is_optional_kind(values["consistency_kind"]):
        return True
    if not _is_progress(values["progress"]):
        return True
    if not _is_utc_instant(values["expires_at"]):
        return True
    if not _is_revision(values["revision"]):
        return True
    if type(values["cancellation_requested"]) is not bool:
        return True
    _check_capacity(values, (*_EXTENSION_SIZE_NULLABLE, "revision"))
    return False


def _checkpoint_refusals(values: dict) -> bool:
    if not _types_valid(values, _CHECKPOINT_TYPES, frozenset({"owner_result_reference"})):
        return True
    if not _is_text(values["checkpoint_id"]):
        return True
    if not _is_text(values["operation_id"]):
        return True
    if not _is_phase(values["phase"]):
        return True
    if not _is_sha64(values["source_fingerprint"]):
        return True
    if not _is_semver(values["mapping_version"]):
        return True
    if not _is_index(values["committed_unit_index"]):
        return True
    if not _is_progress(values["progress"]):
        return True
    if not _is_revision(values["revision"]):
        return True
    if not _is_optional_text(values["owner_result_reference"]):
        return True
    _check_capacity(values, ("committed_unit_index", "revision"))
    return False


def _binding_refusals(values: dict) -> bool:
    if not _types_valid(values, _BINDING_TYPES, frozenset()):
        return True
    if values["operation_id"] == values["job_id"]:
        return True
    if not _is_text(values["operation_id"]):
        return True
    if not _is_text(values["job_id"]):
        return True
    if not _is_phase(values["phase"]):
        return True
    return False


def _schedule_refusals(values: dict) -> bool:
    if not _types_valid(values, _SCHEDULE_TYPES, frozenset({"next_run_at", "attempt_deadline", "failure_code"})):
        return True
    if not _is_text(values["job_id"]):
        return True
    if not _is_text(values["policy_reference"]):
        return True
    if not _is_semver(values["policy_version"]):
        return True
    if not _is_optional_utc_instant(values["next_run_at"]):
        return True
    if not _is_optional_utc_instant(values["attempt_deadline"]):
        return True
    if not _is_optional_text(values["failure_code"]):
        return True
    if not _is_revision(values["revision"]):
        return True
    _check_capacity(values, ("revision",))
    return False


class _TrustedUtcDateTimeField(models.DateTimeField):
    """Décodage ORM de confiance uniquement, distinct du contrôle d'entrée.

    Un datetime aware natif timezone ou ZoneInfo est converti en
    timezone.utc ; un datetime naïf ou à tzinfo étranger est refusé sans
    appel de ses callbacks. Les entrées utilisateur exigent timezone.utc
    exact avant tout parsing ou comparaison, sans astimezone.
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        if type(value) is not datetime:
            raise _invalid()
        if type(value.tzinfo) is timezone or type(value.tzinfo) is ZoneInfo:
            return value.astimezone(timezone.utc)
        raise _invalid()


class BulkOperationExecutionRecord(models.Model):
    """Extension d'exécution : relation séparée et vingt-sept clés exactes.

    operation_id est l'argument de relation, jamais une vingt-huitième clé.
    Aucune duplication des neufs champs du Record et aucun placeholder de
    Record ne sont fabriqués ; le garde propre contrôle les vingt-sept clés
    avant tout accès ORM. Le constructeur ne sauvegarde pas.
    """

    operation = models.OneToOneField(
        "backend.BulkOperationRecord",
        primary_key=True,
        serialize=False,
        db_column="operation_id",
        on_delete=models.PROTECT,
        related_name="+",
    )
    execution_version = models.TextField()
    requested_by_reference = models.TextField()
    resolved_context_reference = models.TextField()
    mapping_reference = models.TextField()
    mapping_version = models.TextField()
    input_reference = models.TextField(blank=True, null=True)
    input_version = models.TextField(blank=True, null=True)
    input_sha256 = models.TextField(blank=True, null=True)
    input_size_bytes = models.BigIntegerField(blank=True, null=True)
    output_reference = models.TextField(blank=True, null=True)
    output_version = models.TextField(blank=True, null=True)
    output_sha256 = models.TextField(blank=True, null=True)
    output_size_bytes = models.BigIntegerField(blank=True, null=True)
    projection_reference = models.TextField(blank=True, null=True)
    consistency_kind = models.TextField(
        blank=True,
        null=True,
        choices=_KIND_CHOICES,
    )
    consistency_reference = models.TextField(blank=True, null=True)
    idempotency_key = models.TextField()
    correlation_id = models.TextField()
    causation_id = models.TextField(blank=True, null=True)
    progress = models.JSONField()
    checkpoint_reference = models.TextField(blank=True, null=True)
    result_reference = models.TextField(blank=True, null=True)
    expires_at = _TrustedUtcDateTimeField()
    policy_reference = models.TextField()
    policy_version = models.TextField()
    revision = models.BigIntegerField()
    cancellation_requested = models.BooleanField()

    @classmethod
    def from_values(
        cls, *, operation_id: object, values: object
    ) -> "BulkOperationExecutionRecord":
        """Valide operation_id et vingt-sept clés exactes, puis construit."""
        if not _is_text(operation_id):
            raise _invalid()
        snapshot = _exact_keys(values, _EXTENSION_KEYS)
        if snapshot is None or _extension_refusals(snapshot):
            raise _invalid()
        snapshot["progress"] = snapshot["progress"].copy()
        return cls(operation_id=operation_id, **snapshot)

    def as_values(self) -> dict:
        """Rend les vingt-sept clés d'extension sans la relation séparée."""
        values = {name: getattr(self, name) for name in _EXTENSION_KEYS}
        if _extension_refusals(values):
            raise _invalid()
        values["progress"] = values["progress"].copy()
        return values

    def full_clean(
        self, exclude=None, validate_unique=True, validate_constraints=True,
    ):
        if not _is_text(self.operation_id) or _extension_refusals(
            self.as_values()
        ):
            raise _invalid()
        try:
            return super().full_clean(
                exclude=exclude,
                validate_unique=validate_unique,
                validate_constraints=validate_constraints,
            )
        except ValidationError:
            raise _invalid() from None

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="bulkruntime_execution_operation_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(execution_version="1.0.0"),
                name="bulkruntime_execution_version_exact",
            ),
        ] + [
            models.CheckConstraint(
                condition=~models.Q(**{name: ""}),
                name=f"bulkruntime_execution_{name}_non_empty",
            )
            for name in _EXTENSION_SQL_TEXT_REQUIRED
        ] + [
            models.CheckConstraint(
                condition=(
                    models.Q(**{f"{name}__isnull": True})
                    | ~models.Q(**{name: ""})
                ),
                name=f"bulkruntime_execution_{name}_non_empty",
            )
            for name in _EXTENSION_SQL_TEXT_NULLABLE
        ] + [
            models.CheckConstraint(
                condition=(
                    models.Q(input_size_bytes__isnull=True)
                    | models.Q(input_size_bytes__gte=0)
                ),
                name="bulkruntime_execution_input_size_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(output_size_bytes__isnull=True)
                    | models.Q(output_size_bytes__gte=0)
                ),
                name="bulkruntime_execution_output_size_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(consistency_kind__isnull=True)
                    | models.Q(consistency_kind__in=list(_CONSISTENCY_KINDS))
                ),
                name="bulkruntime_execution_consistency_kind_member",
            ),
            models.CheckConstraint(
                condition=models.Q(revision__gte=1),
                name="bulkruntime_execution_revision_positive",
            ),
        ]


class BulkCheckpointRecord(models.Model):
    """Neuf clés BulkCheckpointV1 ; unique(operation_id, revision) pour CAS."""

    checkpoint_id = models.TextField(primary_key=True, serialize=False)
    operation = models.ForeignKey(
        "backend.BulkOperationRecord",
        db_column="operation_id",
        on_delete=models.PROTECT,
        related_name="+",
    )
    phase = models.TextField(choices=_PHASE_CHOICES)
    source_fingerprint = models.TextField()
    mapping_version = models.TextField()
    committed_unit_index = models.BigIntegerField()
    progress = models.JSONField()
    revision = models.BigIntegerField()
    owner_result_reference = models.TextField(blank=True, null=True)

    @classmethod
    def from_values(cls, values: object) -> "BulkCheckpointRecord":
        """Valide les neuf clés exactes, puis construit sans accès aux données."""
        snapshot = _exact_keys(values, _CHECKPOINT_KEYS)
        if snapshot is None or _checkpoint_refusals(snapshot):
            raise _invalid()
        snapshot["progress"] = snapshot["progress"].copy()
        return cls(**snapshot)

    def as_values(self) -> dict:
        values = {name: getattr(self, name) for name in _CHECKPOINT_KEYS}
        if _checkpoint_refusals(values):
            raise _invalid()
        values["progress"] = values["progress"].copy()
        return values

    def full_clean(
        self, exclude=None, validate_unique=True, validate_constraints=True,
    ):
        if _checkpoint_refusals(self.as_values()):
            raise _invalid()
        try:
            return super().full_clean(
                exclude=exclude,
                validate_unique=validate_unique,
                validate_constraints=validate_constraints,
            )
        except ValidationError:
            raise _invalid() from None

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(checkpoint_id=""),
                name="bulkruntime_checkpoint_id_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="bulkruntime_checkpoint_operation_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(source_fingerprint=""),
                name="bulkruntime_checkpoint_fingerprint_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(mapping_version=""),
                name="bulkruntime_checkpoint_mapping_non_empty",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(owner_result_reference__isnull=True)
                    | ~models.Q(owner_result_reference="")
                ),
                name="bulkruntime_checkpoint_owner_ref_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    phase__in=[phase for phase in _PHASES],
                ),
                name="bulkruntime_checkpoint_phase_member",
            ),
            models.CheckConstraint(
                condition=models.Q(committed_unit_index__gte=0),
                name="bulkruntime_checkpoint_index_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(revision__gte=1),
                name="bulkruntime_checkpoint_revision_positive",
            ),
            models.UniqueConstraint(
                fields=["operation", "revision"],
                name="bulkruntime_checkpoint_operation_revision_unique",
            ),
        ]


class BulkJobBindingRecord(models.Model):
    """Trois clés BulkJobBindingV1 ; job unique, couple opération phase unique.

    job_id et operation_id sont deux identifiants distincts du runtime ;
    le BulkJobLink préparatoire et ses contrats restent inchangés.
    """

    job = models.OneToOneField(
        "backend.JobRecord",
        primary_key=True,
        serialize=False,
        db_column="job_id",
        on_delete=models.PROTECT,
        related_name="+",
    )
    operation = models.ForeignKey(
        "backend.BulkOperationRecord",
        db_column="operation_id",
        on_delete=models.PROTECT,
        related_name="+",
    )
    phase = models.TextField(choices=_PHASE_CHOICES)

    @classmethod
    def from_values(cls, values: object) -> "BulkJobBindingRecord":
        """Valide les trois clés exactes, puis construit sans accès aux données."""
        snapshot = _exact_keys(values, _BINDING_KEYS)
        if snapshot is None or _binding_refusals(snapshot):
            raise _invalid()
        return cls(**snapshot)

    def as_values(self) -> dict:
        values = {name: getattr(self, name) for name in _BINDING_KEYS}
        if _binding_refusals(values):
            raise _invalid()
        return values

    def full_clean(
        self, exclude=None, validate_unique=True, validate_constraints=True,
    ):
        if _binding_refusals(self.as_values()):
            raise _invalid()
        try:
            return super().full_clean(
                exclude=exclude,
                validate_unique=validate_unique,
                validate_constraints=validate_constraints,
            )
        except ValidationError:
            raise _invalid() from None

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="bulkruntime_binding_operation_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(job_id=""),
                name="bulkruntime_binding_job_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(operation_id=models.F("job_id")),
                name="bulkruntime_binding_ids_distinct",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    phase__in=[phase for phase in _PHASES],
                ),
                name="bulkruntime_binding_phase_member",
            ),
            models.UniqueConstraint(
                fields=["operation", "phase"],
                name="bulkruntime_binding_operation_phase_unique",
            ),
        ]


class BulkJobScheduleRecord(models.Model):
    """Sept clés JobScheduleV1 ; révision CAS du calendrier du job."""

    job = models.OneToOneField(
        "backend.JobRecord",
        primary_key=True,
        serialize=False,
        db_column="job_id",
        on_delete=models.PROTECT,
        related_name="+",
    )
    policy_reference = models.TextField()
    policy_version = models.TextField()
    next_run_at = _TrustedUtcDateTimeField(blank=True, null=True)
    attempt_deadline = _TrustedUtcDateTimeField(blank=True, null=True)
    failure_code = models.TextField(blank=True, null=True)
    revision = models.BigIntegerField()

    @classmethod
    def from_values(cls, values: object) -> "BulkJobScheduleRecord":
        """Valide les sept clés exactes, puis construit sans accès aux données."""
        snapshot = _exact_keys(values, _SCHEDULE_KEYS)
        if snapshot is None or _schedule_refusals(snapshot):
            raise _invalid()
        return cls(**snapshot)

    def as_values(self) -> dict:
        values = {name: getattr(self, name) for name in _SCHEDULE_KEYS}
        if _schedule_refusals(values):
            raise _invalid()
        return values

    def full_clean(
        self, exclude=None, validate_unique=True, validate_constraints=True,
    ):
        if _schedule_refusals(self.as_values()):
            raise _invalid()
        try:
            return super().full_clean(
                exclude=exclude,
                validate_unique=validate_unique,
                validate_constraints=validate_constraints,
            )
        except ValidationError:
            raise _invalid() from None

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(job_id=""),
                name="bulkruntime_schedule_job_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(policy_reference=""),
                name="bulkruntime_schedule_policy_reference_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(policy_version=""),
                name="bulkruntime_schedule_policy_version_non_empty",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(failure_code__isnull=True)
                    | ~models.Q(failure_code="")
                ),
                name="bulkruntime_schedule_failure_code_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(revision__gte=1),
                name="bulkruntime_schedule_revision_positive",
            ),
        ]
