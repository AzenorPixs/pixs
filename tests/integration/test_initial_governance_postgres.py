"""Recette PostgreSQL isolée C10, à exécuter en processus frais.

Les fichiers de catalogue sont des fixtures de qualification explicites.
Aucune qualification PZT, publisher autorisé, acte C08 complet ou P0.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib
import json
import os
import secrets
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from core_pg_test_support import (
    read_project_env, mask_output, safe_schema_name, create_schema,
    drop_schema_if_owned, managed_pg_connection, quote_search_path, pg_options, close_django_connections)

NOW = dt.datetime(2026, 10, 23, 8, tzinfo=dt.timezone.utc)
OUTPUT = ROOT / "output" / "tests" / "c10-pg"
INSTALLATION = "qualification-c10"


class Clock:
    def __init__(self):
        self.value = NOW

    def now(self):
        return self.value


def fixture_bytes():
    header = """[catalog]
schema_version = "1.0.0"
catalog_version = "qualification:1"
publication_ref = "publication:qualification"
valid_from = 2026-10-23T07:00:00Z
valid_until = 2026-10-24T07:00:00Z
published_at = 2026-10-23T07:30:00Z
revoked = false
"""
    for name, asset, owner in (("core", "asset:core", "pixs.core"),
                                ("metadata", "asset:c10-receipt", "qualification.c10")):
        header += (
            "\n[profiles." + name + "]\npublished_version = \"1.0.0\"\n"
            'resource_refs = ["pixs.core.bootstrap:qualification-c10"]\nrevoked = false\n'
            "[profiles." + name + ".profile]\n")
        values = dict(profile_version="1.0.0", data_asset_id=asset,
                      owner_component=owner, source_of_truth="declaration:qualification",
                      confidentiality="INTERNAL", personal_data="NONE",
                      retention_policy="retention:qualification-only",
                      deletion_policy="deletion:qualification-only",
                      export_policy="export:qualification-only", lineage="lineage:qualification-only")
        header += "".join(k + " = " + json.dumps(v) + "\n" for k, v in values.items())
        header += "".join(k + " = []\n" for k in (
            "data_classes", "purpose_refs", "residency_constraints",
            "authorized_consumers", "processor_refs"))
    return header.encode("utf-8")


@contextmanager
def expect(error_type):
    try:
        yield
    except error_type:
        return
    raise AssertionError("EXPECTED_REFUSAL_MISSING")


def run():
    env = read_project_env(str(ROOT))
    result = dict(code="TEST_FAILED", cases={}, cleanup=False)
    if env is None:
        result["code"] = "NON_DISPONIBLE"
        result["cleanup"] = True
        return result
    schema, owned = safe_schema_name(), False
    references, close_failures = [], []
    orm_configured = False
    file_directory = None
    def admin():
        return managed_pg_connection(
            env["PG_HOST"], env["PG_PORT"], env["PG_DATABASE"],
            env["PG_USERNAME"], env["PG_PASSWORD"], references, close_failures)
    try:
        with admin() as connection:
            owned, code = create_schema(connection, schema)
            if not owned or code != "NONE":
                raise AssertionError("SCHEMA_UNAVAILABLE")
            quoted = quote_search_path(connection, schema)
        from django.conf import settings
        if settings.configured:
            raise AssertionError("PROCESS_NOT_FRESH")
        database = {
            "ENGINE": "django.db.backends.postgresql", "NAME": env["PG_DATABASE"],
            "USER": env["PG_USERNAME"], "PASSWORD": env["PG_PASSWORD"],
            "HOST": env["PG_HOST"], "PORT": env["PG_PORT"],
            "OPTIONS": {"options": pg_options(quoted), "connect_timeout": 2},
            "TIME_ZONE": "UTC", "CONN_MAX_AGE": 0,
            "ATOMIC_REQUESTS": False, "AUTOCOMMIT": True}
        settings.configure(INSTALLED_APPS=["pixs.backend.apps.PixsCoreConfig", "pixs.backend"],
                           SECRET_KEY=secrets.token_urlsafe(32), DATABASES={
                               "default": database, "foreign": dict(database)},
                           USE_TZ=True, TIME_ZONE="UTC", LOGGING_CONFIG=None, MIDDLEWARE=())
        orm_configured = True
        import django
        django.setup()
        from django.db import connections, transaction, DatabaseError
        from django.db.migrations.state import ProjectState
        from django.db.migrations.exceptions import IrreversibleError
        from pixs.backend.c10_catalog import C10Catalog, CatalogConfig, ProfileBinding
        from pixs.backend.c10_governance_adapter import C10GovernanceAdapter
        from pixs.backend.c10_receipt_record import C10ReceiptRecord
        from pixs.core.authz.ports import Request
        from pixs.core.bootstrap_operator import BOOTSTRAP_ACTION
        from pixs.core.ports import CorePortError, StagedRef, TransactionProof
        from pixs.core.scope.context import ScopeContext, ScopeType
        conn = connections["default"]
        def scope_guard():
            with conn.cursor() as cursor:
                cursor.execute("SELECT current_schemas(false)")
                if cursor.fetchone()[0] != [schema] or schema == "public":
                    raise AssertionError("SCHEMA_SCOPE_DIVERGENT")
        scope_guard()
        migration_module = importlib.import_module(
            "pixs.backend.migrations.0014_c10_initial_governance_receipts")
        migration = migration_module.Migration("0014_c10_initial_governance_receipts", "backend")
        initial = ProjectState()
        with conn.schema_editor() as editor:
            state = migration.apply(initial, editor)
        with conn.schema_editor() as editor:
            migration.unapply(ProjectState(), editor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT to_regclass(%s)", ["backend_c10receiptrecord"])
            if cursor.fetchone()[0] is not None:
                raise AssertionError("REVERSE_EMPTY_UNPROVED")
        with conn.schema_editor() as editor:
            state = migration.apply(ProjectState(), editor)
        result["cases"]["MIGRATION_APPLY_REVERSE_EMPTY"] = "PASS"

        OUTPUT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=OUTPUT, prefix="case-") as directory:
            file_directory = directory
            parent = Path(directory)
            os.chown(parent, -1, os.getegid())
            os.chmod(parent, 0o700)
            path, guard = parent / "catalog.toml", parent / "catalog.guard"
            raw = fixture_bytes()
            path.write_bytes(raw)
            guard.write_bytes(b"")
            os.chmod(path, 0o600)
            os.chmod(guard, 0o600)
            parents = tuple(dict.fromkeys(
                (p.stat().st_uid, p.stat().st_gid) for p in [*reversed(parent.parents), parent]))
            clock = Clock()
            cfg = CatalogConfig(
                str(path), str(guard), os.geteuid(), os.getegid(), parents,
                16384, 128, 8, 32, 90000, 3600, 0, 1,
                "qualification:1", "publication:qualification", hashlib.sha256(raw).hexdigest(),
                ProfileBinding("core", "asset:core", "pixs.core", "declaration:qualification", "1.0.0"))
            meta = replace(cfg, binding=ProfileBinding(
                "metadata", "asset:c10-receipt", "qualification.c10",
                "declaration:qualification", "1.0.0"))
            context = ScopeContext(ScopeType.PLATFORM, None, None)
            request = Request("decision:qualification", "operator:qualification",
                              "pixs.core.bootstrap:" + INSTALLATION, BOOTSTRAP_ACTION,
                              context, "correlation:qualification")
            @contextmanager
            def adapter():
                a, b = C10Catalog(cfg, now=clock.now), C10Catalog(meta, now=clock.now)
                with a.guard() as core_lease, b.guard() as metadata_lease:
                    yield C10GovernanceAdapter(using="default", installation_ref=INSTALLATION,
                        core_lease=core_lease, metadata_lease=metadata_lease, clock=clock)
            counter = 0
            def operation():
                nonlocal counter
                counter += 1
                return "operation:qualification:" + str(counter), "token:qualification:" + str(counter)
            def staged(provider, op, token, read=True):
                attestation = provider.attest(request, alias="default", operation_id=op,
                                               transaction_token=token)
                if attestation.profile.data_asset_id != "asset:core":
                    raise AssertionError("PROFILE_DIVERGENT")
                stage = (provider.stage_read(request, resource_refs=(request.resource_id,),
                          alias="default", operation_id=op, transaction_token=token)
                         if read else StagedRef(op, "default", token, context, "qualification:other-owner"))
                return TransactionProof(op, "default", token, context, (stage,), clock.now())
            with adapter() as provider:
                op, token = operation()
                with transaction.atomic(using="default"):
                    proof = staged(provider, op, token)
                    provider.verify_staged(proof)
                if C10ReceiptRecord.objects.using("default").filter(operation_id=op).count() != 2:
                    raise AssertionError("COMMIT_UNPROVED")
                result["cases"]["ATTEST_READ_COMMIT_NATIVE"] = "PASS"
                with expect(CorePortError):
                    with transaction.atomic(using="default"):
                        provider.verify_staged(proof)
                result["cases"]["OLD_XID_REFUSED"] = "PASS"
                conn.close()
                with expect(CorePortError):
                    with transaction.atomic(using="default"):
                        provider.verify_staged(proof)
                result["cases"]["REPLACED_CONNECTION_REFUSED"] = "PASS"
            with expect(CorePortError):
                provider.attest(request, alias="default", operation_id=op, transaction_token=token)
            result["cases"]["CLOSED_LEASE_REFUSED"] = "PASS"

            op, token = operation()
            with adapter() as provider:
                with expect(CorePortError):
                    with transaction.atomic(using="default"):
                        proof = staged(provider, op, token, read=False)
                        sid = transaction.savepoint(using="default")
                        stage = provider.stage_read(request, resource_refs=(request.resource_id,),
                            alias="default", operation_id=op, transaction_token=token)
                        transaction.savepoint_rollback(sid, using="default")
                        provider.verify_staged(TransactionProof(
                            op, "default", token, context, (stage,), clock.now()))
            if C10ReceiptRecord.objects.using("default").filter(operation_id=op).exists():
                raise AssertionError("ROLLBACK_UNPROVED")
            result["cases"]["SAVEPOINT_RECEIPT_ROLLBACK_REFUSED"] = "PASS"

            with adapter() as provider:
                op, token = operation()
                with expect(CorePortError):
                    with transaction.atomic(using="default"):
                        staged(provider, op, token)
                        provider.stage_read(request, resource_refs=("foreign:resource",),
                            alias="default", operation_id=op, transaction_token=token)
                result["cases"]["FOREIGN_RESOURCE_REFUSED"] = "PASS"
            with adapter() as provider:
                op, token = operation()
                with expect(CorePortError):
                    with transaction.atomic(using="default"):
                        proof = staged(provider, op, token)
                        clock.value = NOW + dt.timedelta(days=2)
                        provider.verify_staged(proof)
            clock.value = NOW
            result["cases"]["EXPIRED_SOURCE_ROLLBACK"] = "PASS"
            with adapter() as provider:
                with expect(CorePortError):
                    provider.authorize_state_change(request, current_state="ACTIVE",
                        target_state="SOFT_DELETED", alias="default",
                        operation_id="outside", transaction_token="outside")
            result["cases"]["GLOBAL_C10_TRANSITION_REFUSED"] = "PASS"

            template = C10ReceiptRecord.objects.using("default").values().first()
            if template is None:
                raise AssertionError("BASE_RECEIPT_MISSING")
            for name, changes in (
                ("BAD_PID", {"pid": 0}), ("BAD_XID", {"xid": "0"}),
                ("JSON_OBJECT", {"resource_refs": {}}), ("JSON_EMPTY", {"resource_refs": []}),
                ("JSON_NONSTRING", {"resource_refs": [False]})):
                candidate = dict(template)
                candidate.update(changes)
                candidate["receipt_id"] = "qualification:" + name
                with expect(DatabaseError):
                    with transaction.atomic(using="default"):
                        with conn.cursor() as cursor:
                            cursor.execute("SELECT pg_backend_pid(),pg_current_xact_id()::text")
                            pid, xid = cursor.fetchone()
                        if "pid" not in changes:
                            candidate["pid"] = pid
                        if "xid" not in changes:
                            candidate["xid"] = xid
                        C10ReceiptRecord.objects.using("default").create(**candidate)
                result["cases"]["TRIGGER_" + name] = "PASS"
            for name, sql in (
                ("UPDATE", "UPDATE backend_c10receiptrecord SET correlation_id=%s"),
                ("DELETE", "DELETE FROM backend_c10receiptrecord WHERE receipt_id<>%s")):
                with expect(DatabaseError):
                    with transaction.atomic(using="default"):
                        with conn.cursor() as cursor:
                            cursor.execute(sql, ["qualification:immutable"])
                result["cases"]["IMMUTABLE_" + name] = "PASS"
            with expect(IrreversibleError):
                with conn.schema_editor() as editor:
                    migration.unapply(state, editor)
            if not C10ReceiptRecord.objects.using("default").exists():
                raise AssertionError("REVERSE_NONEMPTY_DAMAGED")
            result["cases"]["REVERSE_NONEMPTY_REFUSED"] = "PASS"
        result["code"] = "PASS"
    except Exception:
        # Une erreur inattendue reste un échec explicite et sera comptée comme telle.
        result["code"] = "TEST_FAILED"
    finally:
        orm_closed = True
        if orm_configured:
            close_django_connections(references, close_failures)
            orm_closed = not close_failures
        removed = not owned
        if owned:
            with admin() as connection:
                removed = drop_schema_if_owned(connection, schema, owned)
        result["cleanup"] = (removed and orm_closed and not close_failures
                             and (file_directory is None or not Path(file_directory).exists())
                             and all(connection.closed for connection in references))
        if not result["cleanup"]:
            result["code"] = "TEST_FAILED"
    return result


def main():
    result = dict(code="TEST_FAILED", cases={}, cleanup=False)
    with mask_output():
        try:
            result = run()
        except Exception:
            # Rapport fermé et échec explicite, jamais une validation verte.
            result["code"] = "TEST_FAILED"
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["code"] == "PASS" else (2 if result["code"] == "NON_DISPONIBLE" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
