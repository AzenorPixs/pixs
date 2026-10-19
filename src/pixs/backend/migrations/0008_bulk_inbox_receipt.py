"""Création de la seule table InboxReceipt, état figé depuis le modèle validé."""

from django.db import migrations, models

from pixs.backend import bulk_runtime_records


class Migration(migrations.Migration):
    dependencies = [("backend", "0007_bulk_event_envelope")]

    operations = [
        migrations.CreateModel(
            name="BulkInboxReceiptRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("consumer_reference", models.TextField()),
                ("event_id", models.TextField()),
                ("event_version", models.TextField()),
                ("content_sha256", models.TextField()),
                ("state", models.TextField(choices=[("CONSUMED", "CONSUMED")])),
                ("consumed_at", bulk_runtime_records._TrustedUtcDateTimeField()),
                ("correlation_id", models.TextField()),
                ("causation_id", models.TextField(blank=True, null=True)),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(condition=~models.Q(consumer_reference=""), name="bulkinboxreceipt_consumer_non_empty"),
                    models.CheckConstraint(condition=~models.Q(event_id=""), name="bulkinboxreceipt_event_non_empty"),
                    models.CheckConstraint(condition=~models.Q(event_version=""), name="bulkinboxreceipt_version_non_empty"),
                    models.CheckConstraint(condition=~models.Q(content_sha256=""), name="bulkinboxreceipt_digest_non_empty"),
                    models.CheckConstraint(condition=models.Q(content_sha256__regex=r"^[0-9a-f]{64}$"), name="bulkinboxreceipt_digest_regex"),
                    models.CheckConstraint(condition=models.Q(state__in=["CONSUMED"]), name="bulkinboxreceipt_state_member"),
                    models.CheckConstraint(condition=~models.Q(correlation_id=""), name="bulkinboxreceipt_correlation_non_empty"),
                    models.CheckConstraint(condition=(models.Q(causation_id__isnull=True) | ~models.Q(causation_id="")), name="bulkinboxreceipt_causation_non_empty"),
                    models.UniqueConstraint(fields=["consumer_reference", "event_id"], name="bulkinboxreceipt_consumer_event_unique"),
                ],
            },
        ),
    ]
