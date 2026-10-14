"""Migration de la persistance bornée des travaux."""

from __future__ import annotations

import pixs.backend.models
from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("backend", "0001_feature_flag_source_snapshot"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobRecord",
            fields=[
                (
                    "job_id",
                    models.TextField(primary_key=True, serialize=False),
                ),
                ("job_type", models.TextField(blank=False)),
                (
                    "job_version",
                    models.TextField(
                        blank=False,
                        validators=[pixs.backend.models._validate_job_version],
                    ),
                ),
                ("payload", models.JSONField(blank=True, null=False)),
                ("subject", models.JSONField(blank=True, null=False)),
                ("tenant_context", models.JSONField(blank=True, null=False)),
                ("correlation_id", models.TextField(blank=False)),
                ("causation_id", models.TextField(blank=False)),
                ("perimeter_reference", models.TextField(blank=False)),
                (
                    "state",
                    models.TextField(
                        blank=False,
                        choices=[
                            ("PENDING", "PENDING"),
                            ("SCHEDULED", "SCHEDULED"),
                            ("RUNNING", "RUNNING"),
                            ("SUCCEEDED", "SUCCEEDED"),
                            ("RETRYING", "RETRYING"),
                            ("FAILED", "FAILED"),
                            ("PAUSED", "PAUSED"),
                            ("CANCELLED", "CANCELLED"),
                            ("DEAD_LETTER", "DEAD_LETTER"),
                        ],
                    ),
                ),
                (
                    "attempt_count",
                    models.IntegerField(
                        default=0, validators=[MinValueValidator(0)]
                    ),
                ),
                ("lease_owner", models.TextField(blank=True, null=True)),
                ("lease_expires_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "constraints": [
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
                        condition=models.Q(
                            state__in=[
                                "PENDING",
                                "SCHEDULED",
                                "RUNNING",
                                "SUCCEEDED",
                                "RETRYING",
                                "FAILED",
                                "PAUSED",
                                "CANCELLED",
                                "DEAD_LETTER",
                            ]
                        ),
                        name="jobrecord_state_in_jobstate",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(attempt_count__gte=0),
                        name="jobrecord_attempt_count_non_negative",
                    ),
                ],
            },
        ),
    ]
