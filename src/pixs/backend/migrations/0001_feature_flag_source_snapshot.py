"""Migration initiale de la source persistante des fanions."""

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FeatureFlagSourceSnapshotRecord",
            fields=[
                (
                    "configuration_version",
                    models.TextField(primary_key=True, serialize=False),
                ),
                ("snapshot", models.JSONField()),
            ],
            options={},
        ),
    ]
