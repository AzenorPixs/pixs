"""Recette PG C06 PHASE MIGRATION : 0003 structurel seul, sans metier."""

from __future__ import annotations

import re

__all__ = ["run_real_api_core_idempotence"]

_SCHEMA = re.compile(r"c02_[0-9a-f]{16}")
_REQUIRED = [
    "migrate_0003_and_replay_no_plan",
    "table_trigger_final_deferrable",
    "reverse_empty_then_reapply",
    "in_progress_commit_refused_final",
    "insert_update_succeeded_persisted",
    "terminal_update_delete_refused_unchanged",
    "downgrade_nonempty_refused_present",
]


def run_real_api_core_idempotence(root_str: str, schema_name: str) -> dict:
    import core_pg_test_support as support

    out = {"real_pg": False, "cases": {}, "cleanup": True, "conns_closed": False,
           "code": "NONE", "phase": "INIT", "failure_type": "",
           "django_version_num": "", "pg_version_num": ""}
    refs, close_failures, private_values = [], [], []
    owned, configured = False, False
    if type(root_str) is not str or root_str != support.EXPECTED_ROOT:
        out["code"] = "RACINE_INVALIDE"
        return out
    if type(schema_name) is not str or _SCHEMA.fullmatch(schema_name) is None:
        out["code"] = "SCHEMA_INVALIDE"
        return out
    with support.mask_output():
        try:
            env = support.read_project_env(root_str)
            if env is None:
                out["code"] = "ENV_REFUSE"
            else:
                private_values = list(env.values())
                with support.managed_pg_connection(env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"], env["PG_USERNAME"], env["PG_PASSWORD"], refs, close_failures) as admin:
                    try:
                        owned, reason = support.create_schema(admin, schema_name)
                        if not owned or reason != "NONE":
                            raise RuntimeError("SCHEMA_NON_PROUVE")
                        out["cleanup"] = False
                        options = support.pg_options(support.quote_search_path(admin, schema_name))
                        spec = {"dbname": env["PG_DATABASE"], "user": env["PG_USERNAME"], "password": env["PG_PASSWORD"], "host": env["PG_HOST"], "port": env["PG_PORT"], "options": options}
                        support.configure_django_core_pg({"default": dict(spec), "peer": dict(spec)})
                        configured = True
                        import django
                        django.setup()
                        from django.db import connections, transaction, DatabaseError
                        out["phase"] = "MIGRATION"
                        from django.db.migrations.executor import MigrationExecutor
                        from django.db.migrations.recorder import MigrationRecorder
                        from pixs.core.migration_lock import run_core_initial
                        run_core_initial("default", origin=None, target="0.1.0")
                        MigrationExecutor(connections["default"]).migrate([("pixs_core", "0003_core_idempotence")])
                        applied = {f"{a}.{n}" for a, n in MigrationRecorder(connections["default"]).applied_migrations()}
                        assert "pixs_core.0001_core_initial" in applied and "pixs_core.0002_core_audit" in applied and "pixs_core.0003_core_idempotence" in applied
                        ex2 = MigrationExecutor(connections["default"])
                        plan = ex2.migration_plan([("pixs_core", "0003_core_idempotence")])
                        assert plan == []
                        assert applied == {
                            "pixs_core.0001_core_initial",
                            "pixs_core.0002_core_audit",
                            "pixs_core.0003_core_idempotence",
                        }
                        out["cases"]["migrate_0003_and_replay_no_plan"] = True
                        assert support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        q = "SELECT COUNT(*) FROM pg_trigger WHERE tgrelid = to_regclass(%s) AND tgname='pixs_core_apiidem_final' AND tgdeferrable AND tginitdeferred"
                        assert int(support.scalar_one(admin, q, (schema_name + ".pixs_core_apiidem",))) == 1
                        out["cases"]["table_trigger_final_deferrable"] = True
                        out["django_version_num"] = django.get_version()
                        with connections["default"].cursor() as cur:
                            cur.execute("SELECT current_setting('server_version_num')")
                            out["pg_version_num"] = cur.fetchone()[0]
                        if out["pg_version_num"] != "160014":
                            raise RuntimeError("VERSION_NON_PROUVEE")
                        MigrationExecutor(connections["default"]).migrate([("pixs_core", "0002_core_audit")])
                        assert not support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        MigrationExecutor(connections["default"]).migrate([("pixs_core", "0003_core_idempotence")])
                        assert support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        out["cases"]["reverse_empty_then_reapply"] = True
                        out["phase"] = "SCENARIOS"
                        from pixs.core.models import CoreApiIdempotencyRecord
                        from pixs.core.persistence.uuid7 import generate_uuid7
                        import datetime
                        now = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
                        rid = generate_uuid7()
                        base = dict(record_id=rid, namespace="PLATFORM", tenant_id=None, subject_id="s-1", command_type="pixs.core.identity.user.create:v1", idempotency_key="k-1", scope_type="PLATFORM", context_tenant_id=None, context_scope_id=None, content_sha256="0" * 64, serializer_version="1.0.0", state="IN_PROGRESS", result_operation_id=None, result_ref=None, result_version=None, result_persistence_state=None, result_correlation_id=None, created_at=now, completed_at=None, expires_at=now + datetime.timedelta(seconds=3600), replay_window_seconds=3600, revision=1, version=1, operation_id="op-1", db_alias="default", transaction_token="tok-1")
                        try:
                            with transaction.atomic(using="default"):
                                with connections["default"].cursor() as cur:
                                    cur.execute("SELECT pg_current_xact_id()::text")
                                    xid = cur.fetchone()[0]
                                assert type(xid) is str and xid != ""
                                CoreApiIdempotencyRecord.objects.using("default").create(**dict(base, staged_xid=xid))
                        except DatabaseError as error:
                            cause = getattr(error, "__cause__", None)
                            diag = getattr(cause, "diag", None)
                            if getattr(diag, "message_primary", None) != "APIIDEM_FINAL_STATE":
                                raise
                            out["cases"]["in_progress_commit_refused_final"] = True
                        else:
                            raise RuntimeError("COMMIT_INATTENDU")
                        assert CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid).count() == 0
                        rid2 = generate_uuid7()
                        completed = now + datetime.timedelta(seconds=5)
                        expires = completed + datetime.timedelta(seconds=3600)
                        with transaction.atomic(using="default"):
                            with connections["default"].cursor() as cur:
                                cur.execute("SELECT pg_current_xact_id()::text")
                                xid2 = cur.fetchone()[0]
                            CoreApiIdempotencyRecord.objects.using("default").create(**dict(base, record_id=rid2, staged_xid=xid2, operation_id="op-2", transaction_token="tok-2"))
                            row = CoreApiIdempotencyRecord.objects.using("default").select_for_update().get(record_id=rid2)
                            row.state = "SUCCEEDED"
                            row.result_operation_id = "op-2"
                            row.result_ref = "pixs.core.user:x"
                            row.result_version = 1
                            row.result_persistence_state = "ACTIVE"
                            row.result_correlation_id = "c-2"
                            row.completed_at = completed
                            row.updated_at = completed
                            row.expires_at = expires
                            row.version = 2
                            row.revision = 2
                            row.save(using="default")
                        got = CoreApiIdempotencyRecord.objects.using("default").get(record_id=rid2)
                        assert got.state == "SUCCEEDED" and got.version == 2 and got.revision == 2
                        assert got.result_ref == "pixs.core.user:x" and got.completed_at == completed and got.expires_at == expires
                        peer = CoreApiIdempotencyRecord.objects.using("peer").get(record_id=rid2)
                        assert peer.result_operation_id == "op-2" and peer.staged_xid == got.staged_xid
                        out["cases"]["insert_update_succeeded_persisted"] = True
                        try:
                            with transaction.atomic(using="default"):
                                row = CoreApiIdempotencyRecord.objects.using("default").select_for_update().get(record_id=rid2)
                                row.result_ref = "pixs.core.user:autre"
                                row.save(using="default")
                        except DatabaseError as error:
                            if getattr(getattr(error, "__cause__", None), "diag", None) is None or getattr(error.__cause__.diag, "message_primary", None) != "APIIDEM_TRANSITION":
                                raise
                        else:
                            raise RuntimeError("UPDATE_TERMINAL_INATTENDU")
                        try:
                            with transaction.atomic(using="default"):
                                CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid2).delete()
                        except DatabaseError as error:
                            if getattr(getattr(error, "__cause__", None), "diag", None) is None or getattr(error.__cause__.diag, "message_primary", None) != "APIIDEM_DELETE_FORBIDDEN":
                                raise
                        else:
                            raise RuntimeError("DELETE_INATTENDU")
                        assert CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid2, result_ref="pixs.core.user:x").count() == 1
                        out["cases"]["terminal_update_delete_refused_unchanged"] = True
                        try:
                            MigrationExecutor(connections["default"]).migrate([("pixs_core", "0002_core_audit")])
                        except RuntimeError as error:
                            assert str(error) == "Retour migration refuse : idempotence non vide."
                            out["cases"]["downgrade_nonempty_refused_present"] = True
                        else:
                            raise RuntimeError("DOWNGRADE_INATTENDU")
                        assert support.table_exists(admin, schema_name, "pixs_core_apiidem")
                        assert CoreApiIdempotencyRecord.objects.using("default").filter(record_id=rid2).count() == 1
                        remaining = MigrationRecorder(connections["default"]).applied_migrations()
                        assert ("pixs_core", "0003_core_idempotence") in remaining
                        assert int(support.scalar_one(admin, q, (schema_name + ".pixs_core_apiidem",))) == 1
                    finally:
                        if configured:
                            support.close_django_connections(refs, close_failures)
                        if owned:
                            out["cleanup"] = support.drop_schema_if_owned(admin, schema_name, True)
        except Exception as error:
            out["code"] = "EXECUTION_NON_PROUVEE"
            out["failure_type"] = type(error).__name__
            candidate = getattr(error, "code", None)
            if type(candidate) is str and re.fullmatch(r"[A-Z][A-Z0-9_]{2,80}", candidate):
                out["code"] = candidate
        finally:
            out["conns_closed"] = not close_failures and all(bool(c.closed) for c in refs)
            out["real_pg"] = bool(out["code"] == "NONE" and out["cleanup"] and out["conns_closed"] and set(out["cases"]) == set(_REQUIRED) and all(out["cases"].values()))
            if not out["real_pg"] and out["code"] == "NONE":
                out["code"] = "CAS_NON_PROUVE"
            for key, value in tuple(out.items()):
                if type(value) is str:
                    out[key] = support.scrub_text(value, private_values)
    return out
