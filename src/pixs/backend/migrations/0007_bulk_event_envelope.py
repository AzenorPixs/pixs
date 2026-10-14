"""Création de la seule table EventEnvelope, état figé depuis le modèle validé."""

from django.db import migrations, models

from pixs.backend import bulk_runtime_records


class Migration(migrations.Migration):
    dependencies = [("backend", "0006_bulk_command_idempotency")]

    operations = [
        migrations.CreateModel(
            name="BulkEventEnvelopeRecord",
            fields=[
                ("event_id", models.TextField(primary_key=True, serialize=False)),
                ("kind", models.TextField(choices=[("DOMAIN", "DOMAIN"), ("INTEGRATION", "INTEGRATION")])),
                ("event_type", models.TextField()),
                ("event_version", models.TextField()),
                ("producer_reference", models.TextField()),
                ("schema_reference", models.TextField()),
                ("order_scope_reference", models.TextField()),
                ("occurred_at", bulk_runtime_records._TrustedUtcDateTimeField()),
                ("subject_reference", models.TextField()),
                ("tenant_context_reference", models.TextField(blank=True, null=True)),
                ("correlation_id", models.TextField()),
                ("causation_id", models.TextField(blank=True, null=True)),
                ("payload", models.TextField()),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(condition=~models.Q(event_id=""), name="bulkeventenvelope_event_non_empty"),
                    models.CheckConstraint(condition=models.Q(kind__in=["DOMAIN", "INTEGRATION"]), name="bulkeventenvelope_kind_member"),
                    models.CheckConstraint(condition=~models.Q(event_type=""), name="bulkeventenvelope_type_non_empty"),
                    models.CheckConstraint(condition=~models.Q(event_version=""), name="bulkeventenvelope_version_non_empty"),
                    models.CheckConstraint(condition=~models.Q(producer_reference=""), name="bulkeventenvelope_producer_non_empty"),
                    models.CheckConstraint(condition=~models.Q(schema_reference=""), name="bulkeventenvelope_schema_non_empty"),
                    models.CheckConstraint(condition=~models.Q(order_scope_reference=""), name="bulkeventenvelope_scope_non_empty"),
                    models.CheckConstraint(condition=~models.Q(subject_reference=""), name="bulkeventenvelope_subject_non_empty"),
                    models.CheckConstraint(condition=(models.Q(tenant_context_reference__isnull=True) | ~models.Q(tenant_context_reference="")), name="bulkeventenvelope_tenant_non_empty"),
                    models.CheckConstraint(condition=~models.Q(correlation_id=""), name="bulkeventenvelope_correlation_non_empty"),
                    models.CheckConstraint(condition=(models.Q(causation_id__isnull=True) | ~models.Q(causation_id="")), name="bulkeventenvelope_causation_non_empty"),
                    models.CheckConstraint(condition=~models.Q(payload=""), name="bulkeventenvelope_payload_non_empty"),
                ],
            },
        ),
    ]
