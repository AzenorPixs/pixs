"""Repository transactionnel interne du runtime Bulk v1.

Primitives CAS, checkpoints, transitions B06 et baux sous politique serveur
explicite. Ni admission, ni port d'autorité, ni commande propriétaire, ni
provider concret ; CANCELLED et FAILED restent des primitifs internes appelés
après autorisation ou qualification d'une couche supérieure. Les gardes
refusent les types étrangers avant tout parsing, comparaison ou I/O, sans
écho de valeur ni mutation du dictionnaire du caller. Les refus de capacité
utilisent des codes et messages statiques, jamais une erreur SQL brute.
"""

import threading
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from pixs.backend.bulk_execution_values import (
    _EXECUTION_KEYS,
    _RECORD_FIELDS,
    validate_bulk_execution_values,
    validate_bulk_policy_values,
    validate_bulk_progress_values,
)
from pixs.backend.bulk_operation_record import BulkOperationRecord
from pixs.backend.bulk_runtime_records import (
    _CHECKPOINT_KEYS,
    _EXTENSION_KEYS,
    _INT64_MAX,
    _SCHEDULE_KEYS,
    _checkpoint_refusals,
    _exact_keys,
    _invalid,
    _is_phase,
    _is_revision,
    _is_text,
    _is_utc_instant,
    _schedule_refusals,
    BulkCheckpointRecord,
    BulkJobBindingRecord,
    BulkJobScheduleRecord,
    BulkOperationExecutionRecord,
)
from pixs.backend.models import JobRecord

__all__ = [
    "BulkRuntimeRepository",
    "CasConflict",
    "TransitionRefused",
    "LeaseLost",
    "ConstraintRefused",
]

_INT32_MAX = 2**31 - 1


class CasConflict(Exception):
    """Révision CAS obsolète ; aucune donnée concurrente écrasée."""


class TransitionRefused(Exception):
    """Transition B06 refusée par la matrice canonique approuvée."""


class LeaseLost(Exception):
    """Bail expiré, perdu, occupé ou unité indisponible ; effet nul."""


class ConstraintRefused(Exception):
    """Contrainte ou invariant de périmètre refusé ; effet nul."""


_TERMINAL_BULK = frozenset(
    {
        "COMPLETED",
        "COMPLETED_WITH_ERRORS",
        "FAILED",
        "CANCELLED",
        "EXPIRED",
    }
)
_ALL_BULK_STATES = _TERMINAL_BULK | frozenset(
    {"REQUESTED", "STAGED", "VALIDATING", "READY", "RUNNING"}
)
_IMPORT_MATRIX = {
    "REQUESTED": frozenset({"STAGED"}),
    "STAGED": frozenset({"VALIDATING"}),
    "VALIDATING": frozenset({"READY", "COMPLETED", "COMPLETED_WITH_ERRORS"}),
    "READY": frozenset({"RUNNING"}),
    "RUNNING": frozenset({"COMPLETED", "COMPLETED_WITH_ERRORS"}),
}
_EXPORT_MATRIX = {
    "REQUESTED": frozenset({"VALIDATING"}),
    "VALIDATING": frozenset({"READY"}),
    "READY": frozenset({"RUNNING"}),
    "RUNNING": frozenset({"COMPLETED"}),
}
_TERMINAL_JOB_STATES = frozenset(
    {"SUCCEEDED", "FAILED", "CANCELLED", "DEAD_LETTER"}
)
_STRICT_COMMIT_MODES = frozenset({"ATOMIC", "ATOMIC_PER_CHUNK"})
_PROGRESS_COUNTERS = (
    "total_rows",
    "validated_rows",
    "invalid_rows",
    "applied_rows",
    "execution_rejected_rows",
    "exported_rows",
)


def _integer_capacity() -> ValidationError:
    return ValidationError(
        "capacité entière PostgreSQL non supportée",
        code="bulk_runtime_integer_capacity",
    )


def _time_capacity() -> ValidationError:
    return ValidationError(
        "capacité temporelle PostgreSQL non supportée",
        code="bulk_runtime_time_capacity",
    )


def _require_incrementable_revision(value: object) -> None:
    if not _is_revision(value):
        raise _invalid()
    if value >= _INT64_MAX:
        raise _integer_capacity()


def _rejected_rows(progress: dict) -> int:
    return progress["invalid_rows"] + progress["execution_rejected_rows"]


def _import_arc_allowed(
    from_status: str, to_status: str, commit_mode: object, progress: dict
) -> bool:
    if to_status not in _IMPORT_MATRIX[from_status]:
        return False
    if commit_mode == "VALIDATE_ONLY" and to_status in ("READY", "RUNNING"):
        return False
    if from_status == "VALIDATING":
        if to_status == "READY":
            if commit_mode in _STRICT_COMMIT_MODES:
                return progress["invalid_rows"] == 0
            return True
        if commit_mode != "VALIDATE_ONLY":
            return False
        if to_status == "COMPLETED":
            return _rejected_rows(progress) == 0
        return _rejected_rows(progress) > 0
    if from_status == "RUNNING":
        if to_status == "COMPLETED":
            return _rejected_rows(progress) == 0
        return (
            commit_mode == "BEST_EFFORT"
            and _rejected_rows(progress) > 0
        )
    return True


def _counter_decreased(old: object, new: object) -> bool:
    if old is None:
        return False
    if new is None:
        return True
    return new < old


def _add_seconds_limited(now: datetime, seconds: int, cap: datetime) -> datetime:
    if type(seconds) is not int or seconds <= 0:
        raise _invalid()
    try:
        deadline = now + timedelta(seconds=seconds)
    except OverflowError:
        raise _time_capacity() from None
    return min(deadline, cap)


class _ProtectedUnit:
    """Contexte privé d'une unité protégée, actif pendant la transaction."""

    __slots__ = (
        "operation_id",
        "job_id",
        "phase",
        "owner",
        "now",
        "expected_extension_revision",
        "thread_ident",
        "active",
        "committed",
    )

    def __init__(
        self,
        *,
        operation_id: str,
        job_id: str,
        phase: str,
        owner: str,
        now: datetime,
        expected_extension_revision: int,
    ) -> None:
        self.operation_id = operation_id
        self.job_id = job_id
        self.phase = phase
        self.owner = owner
        self.now = now
        self.expected_extension_revision = expected_extension_revision
        self.thread_ident = threading.get_ident()
        self.active = True
        self.committed = False


class BulkRuntimeRepository:
    """Primitives de persistance runtime sur un alias de base déclaré."""

    def __init__(
        self, *, using: object, failure_codes: object
    ) -> None:
        if not _is_text(using):
            raise _invalid()
        if type(failure_codes) is not frozenset:
            raise _invalid()
        if any(not _is_text(code) for code in failure_codes):
            raise _invalid()
        self._using = using
        self._failure_codes = frozenset(failure_codes)
        self._unit_var: ContextVar[_ProtectedUnit | None] = ContextVar(
            "bulk_runtime_unit", default=None
        )

    def _lock_operation(self, operation_id: str) -> BulkOperationRecord:
        record = (
            BulkOperationRecord.objects.using(self._using)
            .filter(operation_id=operation_id)
            .select_for_update()
            .first()
        )
        if record is None:
            raise ConstraintRefused()
        return record

    def _lock_extension(self, operation_id: str) -> BulkOperationExecutionRecord:
        extension = (
            BulkOperationExecutionRecord.objects.using(self._using)
            .filter(operation_id=operation_id)
            .select_for_update()
            .first()
        )
        if extension is None:
            raise ConstraintRefused()
        return extension

    def _lock_schedule(self, job_id: str) -> BulkJobScheduleRecord:
        schedule = (
            BulkJobScheduleRecord.objects.using(self._using)
            .filter(job_id=job_id)
            .select_for_update()
            .first()
        )
        if schedule is None:
            raise ConstraintRefused()
        return schedule

    def _lock_job(self, job_id: str) -> JobRecord:
        job = (
            JobRecord.objects.using(self._using)
            .filter(job_id=job_id)
            .select_for_update()
            .first()
        )
        if job is None:
            raise ConstraintRefused()
        return job

    def _find_binding(self, job_id: str) -> BulkJobBindingRecord:
        binding = (
            BulkJobBindingRecord.objects.using(self._using)
            .filter(job_id=job_id)
            .first()
        )
        if binding is None:
            raise ConstraintRefused()
        return binding

    def _check_policy(self, policy: object) -> dict:
        if type(policy) is not dict:
            raise _invalid()
        items = tuple(policy.items())
        if any(type(key) is not str for key, _ in items):
            raise _invalid()
        snapshot = dict(items)
        if validate_bulk_policy_values(snapshot):
            raise _invalid()
        for name in ("retry_delays_seconds", "publish_retry_delays_seconds"):
            snapshot[name] = list(snapshot[name])
        return snapshot

    def _check_binding(
        self, operation_id: str, job_id: str, phase: str
    ) -> None:
        binding = (
            BulkJobBindingRecord.objects.using(self._using)
            .filter(operation_id=operation_id, phase=phase)
            .select_for_update()
            .first()
        )
        if binding is None or binding.job_id != job_id:
            raise ConstraintRefused()

    def _check_failure_code(self, failure_code: object) -> None:
        if failure_code is None:
            return
        if not _is_text(failure_code):
            raise _invalid()
        if failure_code not in self._failure_codes:
            raise ConstraintRefused()

    def _check_schedule_invariants(
        self,
        job: JobRecord,
        next_run_at: object,
        attempt_deadline: object,
        expires_at: object,
    ) -> None:
        if type(job.state) is not str or type(job.attempt_count) is not int:
            raise ConstraintRefused()
        if job.state in ("SCHEDULED", "RETRYING") and next_run_at is None:
            raise ConstraintRefused()
        if job.state == "RUNNING" and attempt_deadline is None:
            raise ConstraintRefused()
        if (
            attempt_deadline is not None
            and expires_at is not None
            and attempt_deadline > expires_at
        ):
            raise ConstraintRefused()

    def _check_policy_refs(self, schedule: object, extension: object) -> None:
        if (
            schedule.policy_reference != extension.policy_reference
            or schedule.policy_version != extension.policy_version
        ):
            raise ConstraintRefused()

    def create_execution(self, *, values: object) -> str:
        """Valide trente-six clés, puis crée Record et extension en une transaction."""
        if type(values) is not dict:
            raise _invalid()
        items = tuple(values.items())
        if any(type(key) is not str for key, _ in items):
            raise _invalid()
        snapshot = dict(items)
        if validate_bulk_execution_values(snapshot):
            raise _invalid()
        operation_id = snapshot["operation_id"]
        record_values = {name: snapshot[name] for name in _RECORD_FIELDS}
        extension_values = {name: snapshot[name] for name in _EXTENSION_KEYS}
        record = BulkOperationRecord.from_values(record_values)
        extension = BulkOperationExecutionRecord.from_values(
            operation_id=operation_id, values=extension_values
        )
        try:
            with transaction.atomic(using=self._using):
                record.save(using=self._using, force_insert=True)
                extension.save(using=self._using, force_insert=True)
        except IntegrityError:
            raise ConstraintRefused() from None
        return operation_id

    def load_execution(self, *, operation_id: object) -> dict:
        """Combine Record et extension sous verrou opérationnel cohérent."""
        if not _is_text(operation_id):
            raise _invalid()
        with transaction.atomic(using=self._using):
            record = self._lock_operation(operation_id)
            extension = self._lock_extension(operation_id)
            combined = {name: getattr(record, name) for name in _RECORD_FIELDS}
            combined.update(extension.as_values())
            values = {key: combined[key] for key in _EXECUTION_KEYS}
            if validate_bulk_execution_values(values):
                raise _invalid()
            return values

    def bind_job(
        self, *, operation_id: object, job_id: object, phase: object
    ) -> dict:
        """Lie un Job existant fourni ; aucune création ni dérivation de Job."""
        if not _is_text(operation_id) or not _is_text(job_id):
            raise _invalid()
        if operation_id == job_id:
            raise _invalid()
        if not _is_phase(phase):
            raise _invalid()
        values = {
            "operation_id": operation_id,
            "job_id": job_id,
            "phase": phase,
        }
        try:
            with transaction.atomic(using=self._using):
                record = self._lock_operation(operation_id)
                if type(record.bulk_type) is not str:
                    raise ConstraintRefused()
                if record.bulk_type == "IMPORT":
                    allowed = {"STAGE", "VALIDATE"}
                    if record.commit_mode != "VALIDATE_ONLY":
                        allowed.add("APPLY")
                elif record.bulk_type == "EXPORT":
                    allowed = {"EXPORT"}
                else:
                    raise ConstraintRefused()
                if phase not in allowed:
                    raise ConstraintRefused()
                others = list(
                    BulkJobBindingRecord.objects.using(self._using)
                    .filter(operation_id=operation_id)
                    .order_by("job_id")
                    .select_for_update()
                )
                locked_jobs = {
                    key: self._lock_job(key)
                    for key in sorted({job_id, *(other.job_id for other in others)})
                }
                for other in others:
                    if other.phase == phase:
                        raise ConstraintRefused()
                    other_job = locked_jobs[other.job_id]
                    if type(other_job.state) is not str:
                        raise ConstraintRefused()
                    if other_job.state not in _TERMINAL_JOB_STATES:
                        raise ConstraintRefused()
                binding = BulkJobBindingRecord.from_values(values)
                binding.save(using=self._using, force_insert=True)
        except IntegrityError:
            raise ConstraintRefused() from None
        return binding.as_values()

    def get_binding(
        self, *, operation_id: object, phase: object
    ) -> dict | None:
        if not _is_text(operation_id) or not _is_phase(phase):
            raise _invalid()
        binding = (
            BulkJobBindingRecord.objects.using(self._using)
            .filter(operation_id=operation_id, phase=phase)
            .first()
        )
        if binding is None:
            return None
        return binding.as_values()

    def create_schedule(self, *, values: object) -> dict:
        """Crée un ordonnancement pour un Job déjà lié, sous verrous uniformes."""
        snapshot = _exact_keys(values, _SCHEDULE_KEYS)
        if snapshot is None or _schedule_refusals(snapshot):
            raise _invalid()
        self._check_failure_code(snapshot["failure_code"])
        schedule = BulkJobScheduleRecord.from_values(snapshot)
        try:
            with transaction.atomic(using=self._using):
                binding = self._find_binding(snapshot["job_id"])
                self._lock_operation(binding.operation_id)
                extension = self._lock_extension(binding.operation_id)
                self._check_binding(binding.operation_id, binding.job_id, binding.phase)
                job = self._lock_job(snapshot["job_id"])
                self._check_schedule_invariants(
                    job,
                    snapshot["next_run_at"],
                    snapshot["attempt_deadline"],
                    extension.expires_at,
                )
                self._check_policy_refs(schedule, extension)
                schedule.save(using=self._using, force_insert=True)
        except IntegrityError:
            raise ConstraintRefused() from None
        return schedule.as_values()

    def update_schedule(
        self,
        *,
        job_id: object,
        expected_revision: object,
        next_run_at: object,
        attempt_deadline: object,
        failure_code: object,
    ) -> dict:
        if not _is_text(job_id):
            raise _invalid()
        _require_incrementable_revision(expected_revision)
        if next_run_at is not None and not _is_utc_instant(next_run_at):
            raise _invalid()
        if attempt_deadline is not None and not _is_utc_instant(
            attempt_deadline
        ):
            raise _invalid()
        self._check_failure_code(failure_code)
        with transaction.atomic(using=self._using):
            binding = self._find_binding(job_id)
            self._lock_operation(binding.operation_id)
            extension = self._lock_extension(binding.operation_id)
            self._check_binding(binding.operation_id, binding.job_id, binding.phase)
            schedule = self._lock_schedule(job_id)
            job = self._lock_job(job_id)
            self._check_policy_refs(schedule, extension)
            self._check_schedule_invariants(
                job, next_run_at, attempt_deadline, extension.expires_at
            )
            if schedule.revision != expected_revision:
                raise CasConflict()
            updated = BulkJobScheduleRecord.objects.using(self._using).filter(
                job_id=job_id, revision=expected_revision
            ).update(
                revision=expected_revision + 1,
                next_run_at=next_run_at,
                attempt_deadline=attempt_deadline,
                failure_code=failure_code,
            )
            if updated != 1:
                raise CasConflict()
            schedule.refresh_from_db()
            return schedule.as_values()

    def _lease_guard(self, **kwargs: object) -> dict:
        operation_id = kwargs["operation_id"]
        job_id = kwargs["job_id"]
        phase = kwargs["phase"]
        owner = kwargs["owner"]
        now = kwargs["now"]
        expected_schedule_revision = kwargs["expected_schedule_revision"]
        if not _is_text(operation_id) or not _is_text(job_id):
            raise _invalid()
        if not _is_phase(phase) or not _is_text(owner):
            raise _invalid()
        if not _is_utc_instant(now):
            raise _invalid()
        _require_incrementable_revision(expected_schedule_revision)
        policy = self._check_policy(kwargs["policy"])
        return {
            "operation_id": operation_id,
            "job_id": job_id,
            "phase": phase,
            "owner": owner,
            "now": now,
            "expected_schedule_revision": expected_schedule_revision,
            "policy": policy,
        }

    def _lease_preconditions(
        self, record: BulkOperationRecord, extension: object, job: JobRecord, guard: dict
    ) -> None:
        if record.status in _TERMINAL_BULK:
            raise LeaseLost()
        if type(job.state) is not str or type(job.attempt_count) is not int:
            raise ConstraintRefused()
        if job.state in _TERMINAL_JOB_STATES or job.state == "PAUSED":
            raise LeaseLost()
        if extension.cancellation_requested is not False:
            raise LeaseLost()
        if guard["now"] >= extension.expires_at:
            raise LeaseLost()

    def acquire_lease(
        self,
        *,
        operation_id: object,
        job_id: object,
        phase: object,
        owner: object,
        policy: object,
        now: object,
        expected_schedule_revision: object,
    ) -> datetime:
        guard = self._lease_guard(
            operation_id=operation_id,
            job_id=job_id,
            phase=phase,
            owner=owner,
            policy=policy,
            now=now,
            expected_schedule_revision=expected_schedule_revision,
        )
        with transaction.atomic(using=self._using):
            record = self._lock_operation(guard["operation_id"])
            extension = self._lock_extension(guard["operation_id"])
            self._check_binding(
                guard["operation_id"], guard["job_id"], guard["phase"]
            )
            schedule = self._lock_schedule(guard["job_id"])
            job = self._lock_job(guard["job_id"])
            self._check_policy_refs(schedule, extension)
            self._check_schedule_invariants(job, schedule.next_run_at, schedule.attempt_deadline, extension.expires_at)
            self._lease_preconditions(record, extension, job, guard)
            if (
                job.lease_owner is not None
                and job.lease_expires_at is not None
                and job.lease_expires_at > guard["now"]
            ):
                raise LeaseLost()
            if job.state in ("SCHEDULED", "RETRYING") and (
                schedule.next_run_at is not None
                and guard["now"] < schedule.next_run_at
            ):
                raise LeaseLost()
            attempt_count = job.attempt_count
            if attempt_count < 0 or attempt_count + 1 > _INT32_MAX:
                raise _integer_capacity()
            if attempt_count + 1 > guard["policy"]["max_attempts"]:
                raise ConstraintRefused()
            if (
                schedule.attempt_deadline is not None
                and guard["now"] >= schedule.attempt_deadline
            ):
                raise LeaseLost()
            if schedule.attempt_deadline is not None:
                attempt_deadline = schedule.attempt_deadline
            else:
                attempt_deadline = _add_seconds_limited(
                    guard["now"],
                    guard["policy"]["max_runtime_seconds"],
                    extension.expires_at,
                )
            lease_expires_at = _add_seconds_limited(
                guard["now"],
                guard["policy"]["lease_seconds"],
                min(attempt_deadline, extension.expires_at),
            )
            if lease_expires_at <= guard["now"]:
                raise LeaseLost()
            if schedule.revision != guard["expected_schedule_revision"]:
                raise CasConflict()
            updated = BulkJobScheduleRecord.objects.using(
                self._using
            ).filter(
                job_id=guard["job_id"],
                revision=guard["expected_schedule_revision"],
            ).update(
                revision=guard["expected_schedule_revision"] + 1,
                attempt_deadline=attempt_deadline,
            )
            if updated != 1:
                raise CasConflict()
            JobRecord.objects.using(self._using).filter(
                job_id=guard["job_id"]
            ).update(
                lease_owner=guard["owner"],
                lease_expires_at=lease_expires_at,
                attempt_count=attempt_count + 1,
            )
            return lease_expires_at

    def renew_lease(
        self,
        *,
        operation_id: object,
        job_id: object,
        phase: object,
        owner: object,
        policy: object,
        now: object,
        expected_schedule_revision: object,
    ) -> datetime:
        guard = self._lease_guard(
            operation_id=operation_id,
            job_id=job_id,
            phase=phase,
            owner=owner,
            policy=policy,
            now=now,
            expected_schedule_revision=expected_schedule_revision,
        )
        with transaction.atomic(using=self._using):
            record = self._lock_operation(guard["operation_id"])
            extension = self._lock_extension(guard["operation_id"])
            self._check_binding(
                guard["operation_id"], guard["job_id"], guard["phase"]
            )
            schedule = self._lock_schedule(guard["job_id"])
            job = self._lock_job(guard["job_id"])
            self._check_policy_refs(schedule, extension)
            self._check_schedule_invariants(job, schedule.next_run_at, schedule.attempt_deadline, extension.expires_at)
            self._lease_preconditions(record, extension, job, guard)
            if job.lease_owner != guard["owner"]:
                raise LeaseLost()
            if (
                job.lease_expires_at is None
                or job.lease_expires_at <= guard["now"]
            ):
                raise LeaseLost()
            if (
                schedule.attempt_deadline is not None
                and guard["now"] >= schedule.attempt_deadline
            ):
                raise LeaseLost()
            caps = [extension.expires_at]
            if schedule.attempt_deadline is not None:
                caps.append(schedule.attempt_deadline)
            lease_expires_at = _add_seconds_limited(
                guard["now"],
                guard["policy"]["lease_seconds"],
                min(caps),
            )
            if lease_expires_at <= guard["now"]:
                raise LeaseLost()
            if lease_expires_at <= job.lease_expires_at:
                raise LeaseLost()
            if schedule.revision != guard["expected_schedule_revision"]:
                raise CasConflict()
            updated = BulkJobScheduleRecord.objects.using(
                self._using
            ).filter(
                job_id=guard["job_id"],
                revision=guard["expected_schedule_revision"],
            ).update(
                revision=guard["expected_schedule_revision"] + 1,
            )
            if updated != 1:
                raise CasConflict()
            JobRecord.objects.using(self._using).filter(
                job_id=guard["job_id"]
            ).update(lease_expires_at=lease_expires_at)
            return lease_expires_at

    def release_lease(
        self,
        *,
        operation_id: object,
        job_id: object,
        phase: object,
        owner: object,
        policy: object,
        now: object,
        expected_schedule_revision: object,
    ) -> int:
        guard = self._lease_guard(
            operation_id=operation_id,
            job_id=job_id,
            phase=phase,
            owner=owner,
            policy=policy,
            now=now,
            expected_schedule_revision=expected_schedule_revision,
        )
        with transaction.atomic(using=self._using):
            self._lock_operation(guard["operation_id"])
            extension = self._lock_extension(guard["operation_id"])
            self._check_binding(
                guard["operation_id"], guard["job_id"], guard["phase"]
            )
            schedule = self._lock_schedule(guard["job_id"])
            job = self._lock_job(guard["job_id"])
            self._check_policy_refs(schedule, extension)
            self._check_schedule_invariants(job, schedule.next_run_at, schedule.attempt_deadline, extension.expires_at)
            if type(job.state) is not str or type(job.attempt_count) is not int:
                raise ConstraintRefused()
            if job.lease_owner != guard["owner"]:
                raise LeaseLost()
            if (
                job.lease_expires_at is None
                or job.lease_expires_at <= guard["now"]
            ):
                raise LeaseLost()
            if schedule.revision != guard["expected_schedule_revision"]:
                raise CasConflict()
            updated = BulkJobScheduleRecord.objects.using(
                self._using
            ).filter(
                job_id=guard["job_id"],
                revision=guard["expected_schedule_revision"],
            ).update(
                revision=guard["expected_schedule_revision"] + 1,
            )
            if updated != 1:
                raise CasConflict()
            JobRecord.objects.using(self._using).filter(
                job_id=guard["job_id"]
            ).update(lease_owner=None, lease_expires_at=None)
            return guard["expected_schedule_revision"] + 1

    @contextmanager
    def protected_unit(
        self,
        *,
        operation_id: object,
        job_id: object,
        phase: object,
        owner: object,
        policy: object,
        now: object,
        expected_extension_revision: object,
        expected_schedule_revision: object,
    ):
        if self._unit_var.get() is not None:
            raise ConstraintRefused()
        if not _is_text(operation_id) or not _is_text(job_id):
            raise _invalid()
        if not _is_phase(phase) or not _is_text(owner):
            raise _invalid()
        if not _is_utc_instant(now):
            raise _invalid()
        _require_incrementable_revision(expected_extension_revision)
        _require_incrementable_revision(expected_schedule_revision)
        policy_values = self._check_policy(policy)
        unit = _ProtectedUnit(
            operation_id=operation_id,
            job_id=job_id,
            phase=phase,
            owner=owner,
            now=now,
            expected_extension_revision=expected_extension_revision,
        )
        with transaction.atomic(using=self._using):
            record = self._lock_operation(operation_id)
            extension = self._lock_extension(operation_id)
            self._check_binding(operation_id, job_id, phase)
            schedule = self._lock_schedule(job_id)
            job = self._lock_job(job_id)
            self._check_policy_refs(schedule, extension)
            self._check_schedule_invariants(job, schedule.next_run_at, schedule.attempt_deadline, extension.expires_at)
            if record.status in _TERMINAL_BULK:
                raise TransitionRefused()
            if type(job.state) is not str or type(job.attempt_count) is not int:
                raise ConstraintRefused()
            if job.state in _TERMINAL_JOB_STATES or job.state == "PAUSED":
                raise LeaseLost()
            if extension.cancellation_requested is not False:
                raise LeaseLost()
            if extension.revision != expected_extension_revision:
                raise CasConflict()
            if schedule.revision != expected_schedule_revision:
                raise CasConflict()
            if job.lease_owner != owner:
                raise LeaseLost()
            if job.lease_expires_at is None or job.lease_expires_at <= now:
                raise LeaseLost()
            if now >= extension.expires_at:
                raise LeaseLost()
            if (
                schedule.attempt_deadline is not None
                and now >= schedule.attempt_deadline
            ):
                raise LeaseLost()
            if job.attempt_count < 1:
                raise LeaseLost()
            if job.attempt_count > policy_values["max_attempts"]:
                raise ConstraintRefused()
            self._check_policy_refs(schedule, extension)
            token = self._unit_var.set(unit)
            try:
                yield unit
            finally:
                self._unit_var.reset(token)
                unit.active = False

    def _extension_progress(self, extension: object) -> dict:
        progress = extension.progress
        if validate_bulk_progress_values(progress):
            raise ConstraintRefused()
        return progress

    def commit_checkpoint(self, unit: object, checkpoint: object) -> int:
        current = self._unit_var.get()
        if (
            current is None
            or current is not unit
            or not unit.active
            or unit.committed
            or threading.get_ident() != unit.thread_ident
        ):
            raise ConstraintRefused()
        snapshot = _exact_keys(checkpoint, _CHECKPOINT_KEYS)
        if snapshot is None or _checkpoint_refusals(snapshot):
            raise _invalid()
        if snapshot["operation_id"] != unit.operation_id:
            raise _invalid()
        if snapshot["phase"] != unit.phase:
            raise _invalid()
        expected = unit.expected_extension_revision
        if snapshot["revision"] != expected + 1:
            raise _invalid()
        with transaction.atomic(using=self._using):
            record = self._lock_operation(unit.operation_id)
            extension = self._lock_extension(unit.operation_id)
            self._check_binding(unit.operation_id, unit.job_id, unit.phase)
            schedule = self._lock_schedule(unit.job_id)
            job = self._lock_job(unit.job_id)
            if (
                record.status in _TERMINAL_BULK
                or job.state in _TERMINAL_JOB_STATES
                or job.state == "PAUSED"
                or extension.cancellation_requested is not False
                or job.lease_owner != unit.owner
                or job.lease_expires_at is None
                or job.lease_expires_at <= unit.now
                or extension.expires_at <= unit.now
                or schedule.attempt_deadline is None
                or schedule.attempt_deadline <= unit.now
            ):
                raise LeaseLost()
            persisted = self._extension_progress(extension)
            if snapshot["mapping_version"] != extension.mapping_version:
                raise ConstraintRefused()
            for field in _PROGRESS_COUNTERS:
                if _counter_decreased(persisted[field], snapshot["progress"][field]):
                    raise ConstraintRefused()
            any_previous = (
                BulkCheckpointRecord.objects.using(self._using)
                .filter(operation_id=unit.operation_id)
                .order_by("-revision")
                .first()
            )
            if any_previous is not None and (
                snapshot["revision"] <= any_previous.revision
            ):
                raise ConstraintRefused()
            phase_previous = (
                BulkCheckpointRecord.objects.using(self._using)
                .filter(
                    operation_id=unit.operation_id, phase=unit.phase
                )
                .order_by("-revision")
                .first()
            )
            if phase_previous is not None:
                if (
                    snapshot["source_fingerprint"]
                    != phase_previous.source_fingerprint
                    or snapshot["mapping_version"]
                    != phase_previous.mapping_version
                ):
                    raise ConstraintRefused()
                if (
                    snapshot["committed_unit_index"]
                    <= phase_previous.committed_unit_index
                ):
                    raise ConstraintRefused()
                previous_progress = self._extension_progress(phase_previous)
                for field in _PROGRESS_COUNTERS:
                    if _counter_decreased(
                        previous_progress[field], snapshot["progress"][field]
                    ):
                        raise ConstraintRefused()
            combined = {name: getattr(record, name) for name in _RECORD_FIELDS}
            combined.update(extension.as_values())
            combined.update(
                revision=expected + 1,
                progress=dict(snapshot["progress"]),
                checkpoint_reference=snapshot["checkpoint_id"],
            )
            values = {key: combined[key] for key in _EXECUTION_KEYS}
            if validate_bulk_execution_values(values):
                raise _invalid()
            updated = BulkOperationExecutionRecord.objects.using(
                self._using
            ).filter(
                operation_id=unit.operation_id, revision=expected
            ).update(
                revision=expected + 1,
                progress=dict(snapshot["progress"]),
                checkpoint_reference=snapshot["checkpoint_id"],
            )
            if updated != 1:
                raise CasConflict()
            try:
                row = BulkCheckpointRecord.from_values(snapshot)
                row.save(using=self._using, force_insert=True)
            except IntegrityError:
                raise ConstraintRefused() from None
            unit.committed = True
            return expected + 1

    def request_cancellation(
        self,
        *,
        operation_id: object,
        expected_revision: object,
    ) -> int:
        """Pose interne cancellation_requested apres autorisation superieure."""
        if not _is_text(operation_id):
            raise _invalid()
        _require_incrementable_revision(expected_revision)
        with transaction.atomic(using=self._using):
            record = self._lock_operation(operation_id)
            extension = self._lock_extension(operation_id)
            if record.status in _TERMINAL_BULK:
                raise TransitionRefused()
            if extension.revision != expected_revision:
                raise CasConflict()
            rows = BulkOperationExecutionRecord.objects.using(
                self._using
            ).filter(
                operation_id=operation_id, revision=expected_revision
            ).update(cancellation_requested=True, revision=expected_revision + 1)
            if rows != 1:
                raise CasConflict()
            return expected_revision + 1

    def apply_transition(
        self,
        *,
        operation_id: object,
        expected_revision: object,
        to_status: object,
        now: object,
    ) -> int:
        if not _is_text(operation_id):
            raise _invalid()
        _require_incrementable_revision(expected_revision)
        if type(to_status) is not str or to_status not in _ALL_BULK_STATES:
            raise _invalid()
        if not _is_utc_instant(now):
            raise _invalid()
        with transaction.atomic(using=self._using):
            record = self._lock_operation(operation_id)
            extension = self._lock_extension(operation_id)
            from_status = record.status
            if from_status in _TERMINAL_BULK:
                raise TransitionRefused()
            if extension.revision != expected_revision:
                raise CasConflict()
            expired = now >= extension.expires_at
            if to_status in ("EXPIRED", "CANCELLED", "FAILED"):
                if to_status == "EXPIRED":
                    if not expired:
                        raise TransitionRefused()
                elif to_status == "CANCELLED":
                    if extension.cancellation_requested is not True:
                        raise TransitionRefused()
                elif to_status != "FAILED":
                    raise TransitionRefused()
            else:
                if expired:
                    raise TransitionRefused()
                progress = self._extension_progress(extension)
                if record.bulk_type == "IMPORT":
                    if not _import_arc_allowed(
                        from_status, to_status, record.commit_mode, progress
                    ):
                        raise TransitionRefused()
                    if from_status == "VALIDATING" and to_status == "READY":
                        if (
                            extension.input_reference is None
                            or extension.input_sha256 is None
                        ):
                            raise TransitionRefused()
                elif record.bulk_type == "EXPORT":
                    if to_status not in _EXPORT_MATRIX.get(
                        from_status, frozenset()
                    ):
                        raise TransitionRefused()
                    if from_status == "VALIDATING" and to_status == "READY":
                        if (
                            extension.consistency_kind is None
                            or extension.consistency_reference is None
                        ):
                            raise TransitionRefused()
                else:
                    raise TransitionRefused()
            rows = BulkOperationExecutionRecord.objects.using(
                self._using
            ).filter(
                operation_id=operation_id, revision=expected_revision
            ).update(revision=expected_revision + 1)
            if rows != 1:
                raise CasConflict()
            status_rows = BulkOperationRecord.objects.using(
                self._using
            ).filter(
                operation_id=operation_id, status=from_status
            ).update(status=to_status)
            if status_rows != 1:
                raise CasConflict()
            return expected_revision + 1
