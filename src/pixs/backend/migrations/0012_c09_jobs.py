"""Persistance C09 Jobs, additive ; retour vide seulement."""

from django.db import migrations, models
from django.core.validators import MinValueValidator
from pixs.backend import c09_job_records


def refuse_nonempty_reverse(apps, schema_editor):
    model = apps.get_model("backend", "C09JobExtensionRecord")
    if model.objects.using(schema_editor.connection.alias).exists():
        raise RuntimeError("C09_RETOUR_NON_VIDE_REFUSE")


class Migration(migrations.Migration):
    dependencies = [("backend", "0011_bulk_outbox_publication")]
    operations = [
        migrations.CreateModel(
            name="C09JobExtensionRecord",
            fields=[
                ('job', models.OneToOneField(
        "backend.JobRecord",
        primary_key=True,
        serialize=False,
        db_column="job_id",
        on_delete=models.PROTECT,
        related_name="+",
    )),
                ('policy_reference', models.TextField(blank=False)),
                ('policy_version', models.TextField(blank=False)),
                ('revision', models.BigIntegerField(default=1, validators=[MinValueValidator(1)])),
                ('lease_generation', models.BigIntegerField(default=1, validators=[MinValueValidator(1)])),
                ('actor_reference', models.TextField(blank=False)),
                ('command_id', models.TextField(blank=False)),
                ('operation_id', models.TextField(blank=False)),
                ('perimeter_reference', models.TextField(blank=False)),
                ('handler_reference', models.TextField(blank=False)),
                ('handler_version', models.TextField(blank=False)),
                ('dedup_key', models.TextField(blank=False)),
                ('request_reference', models.TextField(blank=False)),
                ('request_version', models.TextField(blank=False)),
                ('content_sha256', models.TextField(blank=False)),
                ('job_deadline', c09_job_records.C09UtcDateTimeField()),
                ('attempt_deadline', c09_job_records.C09UtcDateTimeField(blank=True, null=True)),
                ('next_run_at', c09_job_records.C09UtcDateTimeField(blank=True, null=True)),
                ('checkpoint_reference', models.TextField(blank=True, null=True)),
                ('result_reference', models.TextField(blank=True, null=True)),
                ('failure_code', models.TextField(blank=True, null=True)),
            ],
            options={"constraints": [
            models.CheckConstraint(
                condition=~models.Q(policy_reference=""),
                name="c09jobext_policy_ref_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(policy_version=""),
                name="c09jobext_policy_version_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(revision__gte=1),
                name="c09jobext_revision_gte_1",
            ),
            models.CheckConstraint(
                condition=models.Q(lease_generation__gte=1),
                name="c09jobext_lease_gen_gte_1",
            ),
            models.CheckConstraint(
                condition=~models.Q(actor_reference=""),
                name="c09jobext_actor_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(command_id=""),
                name="c09jobext_command_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(operation_id=""),
                name="c09jobext_operation_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(perimeter_reference=""),
                name="c09jobext_perimeter_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(handler_reference=""),
                name="c09jobext_handler_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(handler_version=""),
                name="c09jobext_handler_version_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(dedup_key=""),
                name="c09jobext_dedup_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(request_reference=""),
                name="c09jobext_request_ref_non_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(request_version=""),
                name="c09jobext_request_version_non_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(content_sha256__regex="^[0-9a-f]{64}$"),
                name="c09jobext_sha_hex",
            ),
            models.CheckConstraint(
                condition=models.Q(checkpoint_reference__isnull=True)
                | ~models.Q(checkpoint_reference=""),
                name="c09jobext_checkpoint_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(result_reference__isnull=True)
                | ~models.Q(result_reference=""),
                name="c09jobext_result_empty",
            ),
            models.CheckConstraint(
                condition=models.Q(failure_code__isnull=True)
                | ~models.Q(failure_code=""),
                name="c09jobext_failure_empty",
            ),
            models.CheckConstraint(
                condition=~models.Q(job_id=models.F("command_id"))
                & ~models.Q(job_id=models.F("operation_id"))
                & ~models.Q(command_id=models.F("operation_id")),
                name="c09jobext_ids_distinct",
            ),
            models.CheckConstraint(
                condition=models.Q(attempt_deadline__isnull=True)
                | models.Q(attempt_deadline__lte=models.F("job_deadline")),
                name="c09jobext_attempt_bounded",
            ),
            models.CheckConstraint(
                condition=models.Q(next_run_at__isnull=True)
                | models.Q(next_run_at__lte=models.F("job_deadline")),
                name="c09jobext_schedule_bounded",
            ),
            models.UniqueConstraint(
                fields=[
                    "perimeter_reference",
                    "actor_reference",
                    "handler_reference",
                    "handler_version",
                    "dedup_key",
                ],
                name="c09jobext_admission_unique",
            ),
        ]},
        ),
        # En sens inverse, cette garde précède la suppression de la table.
        migrations.RunPython(migrations.RunPython.noop, refuse_nonempty_reverse),
    ]
