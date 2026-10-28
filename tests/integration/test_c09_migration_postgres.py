"""Recette C09 : migration et garde de retour sur PostgreSQL isolé.

Les lignes insérées sont des fixtures de schéma. Elles ne qualifient aucun
exécutant, aucune autorisation ou disponibilité de production.
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_EXPECTED = {
    "migration_applied_replay_empty", "model_checks", "schema_inventory",
    "makemigrations_no_drift", "empty_reverse_reapply",
    "guard_ten_tables", "nonempty_last_table_refused",
    "runtime_unknown_not_stopped", "runtime_delete_refused",
}


def scenarios(ctx):
    from django.core import checks
    from django.core.management import call_command
    from django.db import connections, transaction, IntegrityError
    from django.db.migrations.executor import MigrationExecutor
    from pixs.backend import c09_event_records as records

    connection = connections["default"]
    module = importlib.import_module("pixs.backend.migrations.0013_c09_events_scheduler")
    models = tuple(module.C09_MODEL_NAMES)
    expected_models = {
        "C09SchedulerLeaseRecord", "C09ScheduleRecord", "C09OrderCursorRecord",
        "C09EventEnvelopeRecord", "C09OutboxStageRecord", "C09OutboxPublicationRecord",
        "C09DeliveryRecord", "C09InboxReceiptRecord", "C09OwnerUnitProofRecord",
        "C09RuntimeInstanceRecord",
    }
    assert set(models) == expected_models and len(models) == 10
    cases = {"guard_ten_tables": True}
    targets = [("backend", "0013_c09_events_scheduler")]
    assert not MigrationExecutor(connection).migration_plan(targets)
    cases["migration_applied_replay_empty"] = True
    assert not [e for e in checks.run_checks(tags=[checks.Tags.models], databases=[]) if e.level >= 40]
    cases["model_checks"] = True
    call_command("makemigrations", "backend", "--check", "--dry-run", verbosity=0)
    cases["makemigrations_no_drift"] = True

    table_names = {"backend_" + name.lower() for name in models}

    def inventory(present):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema=%s AND table_name=ANY(%s)",
                [ctx["schema"], sorted(table_names)],
            )
            tables = {r[0] for r in cursor.fetchall()}
            cursor.execute(
                "SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid "
                "JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname=%s AND NOT t.tgisinternal AND c.relname=ANY(%s)",
                [ctx["schema"], sorted(table_names)],
            )
            triggers = cursor.fetchone()[0]
            cursor.execute(
                "SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
                "WHERE n.nspname=%s AND left(p.proname,4)=%s",
                [ctx["schema"], "c09_"],
            )
            functions = cursor.fetchone()[0]
        assert tables == (table_names if present else set())
        assert triggers == (24 if present else 0)
        assert functions == (9 if present else 0)

    inventory(True)
    cases["schema_inventory"] = True
    MigrationExecutor(connection).migrate([("backend", "0012_c09_jobs")])
    inventory(False)
    MigrationExecutor(connection).migrate(targets)
    inventory(True)
    assert not MigrationExecutor(connection).migration_plan(targets)
    cases["empty_reverse_reapply"] = True

    # Seule la derniere table du garde est non vide : aucun FK parent ne
    # masque sa verification dans le retour global reel.
    assert models[-1] == "C09RuntimeInstanceRecord"
    with transaction.atomic():
        slot = records.C09RuntimeInstanceRecord.objects.create(
            instance_ref="synthetic:instance", owner_reference="synthetic:owner",
            role="WORKER", plan_reference="synthetic:plan", plan_version="1.0.0",
            plan_sha256="0" * 64, budget_reference="synthetic:budget",
            budget_version="1.0.0", lease_owner=None, lease_expires_at=None,
            generation=1, revision=1, admission_closed=True,
            inflight_count=0, stop_state="STARTING",
        )
    try:
        MigrationExecutor(connection).migrate([("backend", "0012_c09_jobs")])
    except RuntimeError as error:
        assert error.args == ("C09_RETOUR_NON_VIDE_REFUSE",)
    else:
        raise AssertionError("Retour non vide accepte.")
    inventory(True)
    assert records.C09RuntimeInstanceRecord.objects.filter(pk=slot.pk).exists()
    assert not MigrationExecutor(connection).migration_plan(targets)
    cases["nonempty_last_table_refused"] = True

    with transaction.atomic():
        records.C09RuntimeInstanceRecord.objects.filter(pk=slot.pk).update(
            stop_state="UNKNOWN", revision=2, admission_closed=True,
        )
    try:
        with transaction.atomic():
            records.C09RuntimeInstanceRecord.objects.filter(pk=slot.pk).update(
                stop_state="STOPPED", revision=3, admission_closed=True,
            )
    except IntegrityError as error:
        assert getattr(error.__cause__, "sqlstate", None) == "23514"
    else:
        raise AssertionError("UNKNOWN assimile a STOPPED.")
    assert records.C09RuntimeInstanceRecord.objects.get(pk=slot.pk).stop_state == "UNKNOWN"
    cases["runtime_unknown_not_stopped"] = True
    try:
        with transaction.atomic():
            records.C09RuntimeInstanceRecord.objects.filter(pk=slot.pk).delete()
    except IntegrityError as error:
        assert getattr(error.__cause__, "sqlstate", None) == "23514"
    else:
        raise AssertionError("Suppression du compteur acceptee.")
    cases["runtime_delete_refused"] = True
    return cases


class C09MigrationPostgres(unittest.TestCase):
    def test_real_migration(self):
        code = (
            "import json;import test_c09_migration_postgres as t;"
            "import c09_pg_delivery_support as h;"
            "print(json.dumps(h.run_real(" + repr(str(_ROOT)) + ",t.scenarios)))"
        )
        env = {
            "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
            "PYTHONPATH": str(_ROOT / "src") + ":" + str(_ROOT / "tests" / "integration"),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        try:
            result = subprocess.run(
                [sys.executable, "-B", "-c", code], cwd=str(_ROOT), env=env,
                capture_output=True, text=True, timeout=90,
            )
        except subprocess.TimeoutExpired:
            raise AssertionError("Delai de recette depasse.") from None
        self.assertEqual(result.returncode, 0, "Echec du processus isole.")
        lines = [line for line in result.stdout.splitlines() if line.startswith("{")]
        self.assertEqual(len(lines), 1, "Resultat de recette absent.")
        out = json.loads(lines[0])
        print("C09_MIGRATION_PG " + json.dumps(out, sort_keys=True))
        self.assertIs(out.get("real_pg"), True)
        self.assertIs(out.get("cleanup"), True)
        self.assertIs(out.get("conns_closed"), True)
        self.assertEqual(out.get("code"), "NONE")
        self.assertEqual(set(out.get("cases", {})), _EXPECTED)
        self.assertTrue(all(value is True for value in out["cases"].values()))


if __name__ == "__main__":
    unittest.main()
