"""Modèles Django : source persistante versionnée des fanions, persistance des travaux."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from pixs.backend.bulk_operation_record import BulkOperationRecord
from pixs.backend import bulk_runtime_records as _bulk_runtime_records
from pixs.kernel.jobs import JobState
from pixs.kernel.manifest.semver import parse_version

__all__ = ["FeatureFlagSourceSnapshotRecord", "JobRecord"]


class FeatureFlagSourceSnapshotRecord(models.Model):
    """Versionne le document canonique d’un snapshot de fanions."""

    configuration_version = models.TextField(primary_key=True)
    snapshot = models.JSONField()


def _validate_job_version(value: object) -> None:
    """Contrôle la version du travail en SemVer complet, sans écho de valeur."""
    if type(value) is not str:
        raise ValidationError("version de travail SemVer complète attendue")
    try:
        parse_version(value)
    except ValueError:
        raise ValidationError("version de travail SemVer complète attendue") from None


class JobRecord(models.Model):
    """Persistance bornée des travaux avant exécution : treize champs, sans worker.

    Unité de persistance seule : ne couvre ni transitions, ni acquisition de
    bail, ni politique de réessai, ni autorisation, ni déduplication active ;
    ce n'est pas le contrat Job complet. Les références sont opaques, sans FK
    ni preuve d'existence ; ``save()`` n'appelle pas ``full_clean()`` et les
    contraintes DB ne valident pas SemVer (chemin ``full_clean``/validators
    uniquement).
    """

    job_id = models.TextField(primary_key=True, serialize=False)
    job_type = models.TextField(blank=False)
    job_version = models.TextField(blank=False, validators=[_validate_job_version])
    payload = models.JSONField(blank=True, null=False)
    subject = models.JSONField(blank=True, null=False)
    tenant_context = models.JSONField(blank=True, null=False)
    correlation_id = models.TextField(blank=False)
    causation_id = models.TextField(blank=False)
    perimeter_reference = models.TextField(blank=False)
    state = models.TextField(
        blank=False,
        choices=[(item.value, item.value) for item in JobState],
    )
    attempt_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    lease_owner = models.TextField(blank=True, null=True)
    lease_expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(job_id=""),
                name="jobrecord_job_id_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(job_type=""),
                name="jobrecord_job_type_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(job_version=""),
                name="jobrecord_job_version_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(correlation_id=""),
                name="jobrecord_correlation_id_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(causation_id=""),
                name="jobrecord_causation_id_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(perimeter_reference=""),
                name="jobrecord_perimeter_reference_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(state__in=[item.value for item in JobState]),
                name="jobrecord_state_in_jobstate",
            ),
            models.CheckConstraint(
                condition=models.Q(attempt_count__gte=0),
                name="jobrecord_attempt_count_non_negative",
            ),
        ]
