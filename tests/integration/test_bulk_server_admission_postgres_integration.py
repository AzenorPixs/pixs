"""Harnais PostgreSQL isolé B01 : gardes inertes plus callable réel mandaté."""

import re
import subprocess
import sys
import textwrap
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_INTEGRATION = str(_ROOT / "tests" / "integration")
_TARGET = str(Path(__file__))
_MARKER = "BULK_ADMISSION_PG_HARNESS_SAFE_OK\n"
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

_PG_HOST = "127.0.0.1"
_PG_PORT = 5432
_CONNECT_TIMEOUT_SECONDS = 2
_STATEMENT_TIMEOUT_MS = 1500
_LOCK_TIMEOUT_MS = 1500
_ENV_READ_LIMIT = 65537
_MIGRATION_TARGET = ("backend", "0011_bulk_outbox_publication")
_SCHEMA_RE = re.compile(r"bulk_admission_[0-9a-f]{16}")
_FIXED_CODE_RE = re.compile(r"[A-Z][A-Z_]*")
_REAL_ALIAS = "bulk_admission_test"
_TRUE_CONFLICT_MESSAGE = "conflit d'admission bulk"

_REQUIRED_FLAGS = (
    "migrated",
    "import_csv",
    "import_ndjson",
    "export_csv",
    "export_ndjson",
    "replay_stable",
    "conflict_static",
    "actor_isolated",
    "tenant_isolated",
    "search_path_isolated",
    "model_state_coherent",
    "concurrent_single_graph",
    "late_rollback_clean",
    "commit_failure_clean",
    "visibility_ordered",
    "ambient_refused",
    "autocommit_refused",
    "default_untouched",
    "public_stable",
)

_CHILD = textwrap.dedent(
    r"""
    import builtins
    import importlib.util
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock

    src_path = sys.argv[1]
    target_path = sys.argv[2]

    refused = {"import": 0, "open": 0, "env": 0, "net": 0, "proc": 0}
    origin_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split(".")[0] in ("django", "psycopg"):
            refused["import"] += 1
            raise ImportError("blocage ORM du test inerte")
        return origin_import(name, *args, **kwargs)

    def guarded_open(*args, **kwargs):
        refused["open"] += 1
        raise OSError("lecture refusée par le test inerte")

    def guarded_getenv(*args, **kwargs):
        refused["env"] += 1
        raise AssertionError("environnement refusé par le test inerte")

    def guarded_socket(*args, **kwargs):
        refused["net"] += 1
        raise OSError("réseau refusé par le test inerte")

    def guarded_run(*args, **kwargs):
        refused["proc"] += 1
        raise OSError("processus refusé par le test inerte")

    sys.path.insert(0, src_path)
    builtins.__import__ = guarded_import
    try:
        spec = importlib.util.spec_from_file_location(
            "bulk_admission_pg_harness_under_test", target_path
        )
        harness = importlib.util.module_from_spec(spec)
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(builtins, "open", side_effect=guarded_open))
            stack.enter_context(mock.patch.object(Path, "open", side_effect=guarded_open))
            stack.enter_context(mock.patch.object(Path, "read_text", side_effect=guarded_open))
            stack.enter_context(mock.patch.object(Path, "read_bytes", side_effect=guarded_open))
            stack.enter_context(mock.patch.object(os, "getenv", side_effect=guarded_getenv))
            stack.enter_context(mock.patch.object(os.environ, "get", side_effect=guarded_getenv))
            stack.enter_context(mock.patch.object(type(os.environ), "__getitem__", side_effect=guarded_getenv))
            stack.enter_context(mock.patch.object(socket, "socket", side_effect=guarded_socket))
            stack.enter_context(mock.patch.object(socket, "create_connection", side_effect=guarded_socket))
            stack.enter_context(mock.patch.object(subprocess, "Popen", side_effect=guarded_run))
            stack.enter_context(mock.patch.object(subprocess, "run", side_effect=guarded_run))
            spec.loader.exec_module(harness)
            assert callable(harness.run_real_bulk_server_admission_postgres)
            assert callable(harness._read_project_env)
            for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
                outcome = harness.run_real_bulk_server_admission_postgres(bad_root)
                assert outcome["real_pg"] is False
                assert outcome["phase"] == "COMPLETE"
                assert outcome["reason"] == "ROOT_INVALID"
            outcome = harness.run_real_bulk_server_admission_postgres("/synthetic/root")
            assert outcome["reason"] == "ROOT_MISMATCH"
            assert outcome["real_pg"] is False
            assert refused["import"] == 0
            assert refused["open"] == 0
            assert refused["env"] == 0
            assert refused["net"] == 0
            assert refused["proc"] == 0
    finally:
        builtins.__import__ = origin_import

    print("BULK_ADMISSION_PG_HARNESS_SAFE_OK")
    """
).strip()


def _closed_result():
    result = {"real_pg": False, "phase": "INIT", "reason": "NONE"}
    for key in _REQUIRED_FLAGS:
        result[key] = False
    result["case_expected"] = {}
    result["case_observed"] = {}
    result["server_version"] = ""
    result["cleanup_ok"] = False
    result["conns_closed"] = False
    return result


def _combine(result, code):
    if result["reason"] != "NONE":
        return
    if type(code) is str and _FIXED_CODE_RE.fullmatch(code) and code != "NONE":
        result["reason"] = code


def _env_loader():
    if _INTEGRATION not in sys.path:
        sys.path.insert(0, _INTEGRATION)
    import test_pg_connectivity_integration as harness

    return harness._parse_env_text


def _read_project_env(root_str):
    parse = _env_loader()
    env_path = Path(root_str) / "project.env"
    try:
        with env_path.open("rb") as handle:
            raw = handle.read(_ENV_READ_LIMIT)
    except Exception:
        return None
    if len(raw) >= _ENV_READ_LIMIT:
        return None
    try:
        text = raw.decode("utf-8")
    except Exception:
        return None
    if "\x00" in text:
        return None
    try:
        return parse(text)
    except Exception:
        return None


@contextmanager
def _mask_output():
    import io
    import logging

    previous_disable = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    original_out = sys.stdout
    original_err = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = original_out
        sys.stderr = original_err
        logging.disable(previous_disable)


def _safe_schema_name():
    name = "bulk_admission_" + uuid.uuid4().hex[:16]
    if _SCHEMA_RE.fullmatch(name) is None:
        raise RuntimeError("nom de schéma synthétique invalide")
    return name


def _real_body(result, refs, close_failures, state):
    import threading

    import django
    from django.conf import settings
    from django.db import connections, transaction
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.state import ProjectState

    if _INTEGRATION not in sys.path:
        sys.path.insert(0, _INTEGRATION)
    import test_job_record_postgres_integration as base_harness
    from unit.test_bulk_execution_values import validate_bulk_execution_values, _valid_policy
    from unit.test_bulk_runtime_contracts import _authority, _context, _mapping
    from unit.test_bulk_trusted_ports import (
        _Authority,
        _GovernanceResolve3,
        _Resolver,
        _resolved_response,
    )

    scalar = base_harness._scalar
    table_exists = base_harness._table_exists
    table_identity = base_harness._table_identity
    applied_count = base_harness._applied_count
    managed_connection = base_harness._managed_pg_connection
    pg_options = base_harness._pg_options

    result["phase"] = "SCHEMA"
    state["schema"] = _safe_schema_name()
    with managed_connection(
        state["database"], state["user"], state["password"], refs, close_failures
    ) as admin_connection:
        public_tables = (
            "backend_featureflagsourcesnapshotrecord",
            "backend_jobrecord",
            "backend_bulkoperationrecord",
            "backend_bulkoperationexecutionrecord",
            "backend_bulkjobbindingrecord",
            "backend_bulkjobschedulerecord",
            "backend_bulkadmissionidentityrecord",
            "django_migrations",
        )
        state["public_before"] = tuple(
            table_identity(admin_connection, "public", table) for table in public_tables
        )
        from psycopg import sql

        try:
            cursor = admin_connection.cursor()
            try:
                cursor.execute(
                    sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(state["schema"]))
                )
                state["owned"] = True
            finally:
                cursor.close()
        except Exception:
            _combine(result, "SCHEMA_CREATE_FAILED")
            return
        state["search_path"] = sql.Identifier(state["schema"]).as_string(admin_connection)

    if settings.configured:
        _combine(result, "SETTINGS_ALREADY_CONFIGURED")
        return
    settings.configure(
        DEFAULT_CHARSET="utf-8",
        INSTALLED_APPS=["pixs.backend"],
        SECRET_KEY="real-pg-synthetic-only",
        DATABASES={
            _REAL_ALIAS: {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": state["database"],
                "USER": state["user"],
                "PASSWORD": state["password"],
                "HOST": _PG_HOST,
                "PORT": str(_PG_PORT),
                "OPTIONS": {
                    "options": pg_options(state["search_path"]),
                    "connect_timeout": _CONNECT_TIMEOUT_SECONDS,
                },
                "TIME_ZONE": "UTC",
                "CONN_MAX_AGE": 0,
                "ATOMIC_REQUESTS": False,
                "AUTOCOMMIT": True,
            },
            "default": {"ENGINE": "django.db.backends.dummy"},
        },
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    state["configured"] = True
    django.setup()

    real_wrapper = connections[_REAL_ALIAS]
    if scalar(real_wrapper, "SELECT current_schemas(false)", ()) != [state["schema"], "pg_catalog"]:
        _combine(result, "SEARCH_PATH_MISMATCH")
        return
    result["server_version"] = str(scalar(real_wrapper, "SHOW server_version", ()))
    result["server_version_num"] = int(scalar(real_wrapper, "SHOW server_version_num", ()))
    result["test_schema"] = state["schema"]
    result["search_path_isolated"] = True
    result["phase"] = "MIGRATION"
    executor = MigrationExecutor(real_wrapper)
    leaf_nodes = executor.loader.graph.leaf_nodes("backend")
    if _MIGRATION_TARGET not in executor.loader.graph.nodes:
        _combine(result, "MIGRATION_TARGET_MISSING")
        return
    executor.migrate(list(leaf_nodes))
    if applied_count(real_wrapper, state["schema"], _MIGRATION_TARGET[1]) < 1:
        _combine(result, "FORWARD_NOT_PROVED")
        return
    current_state = executor.loader.project_state(list(leaf_nodes))
    actual_state = ProjectState.from_apps(django.apps.apps)
    detector = MigrationAutodetector(current_state, actual_state)
    reverse_detector = MigrationAutodetector(actual_state, current_state)
    if detector.changes(graph=executor.loader.graph) != {} or reverse_detector.changes(graph=executor.loader.graph) != {}:
        _combine(result, "AUTODETECT_DIVERGED")
        return
    result["model_state_coherent"] = True

    from django.apps import apps

    identity_model = apps.get_model("backend", "BulkAdmissionIdentityRecord")
    operation_model = apps.get_model("backend", "BulkOperationRecord")
    extension_model = apps.get_model("backend", "BulkOperationExecutionRecord")
    job_model = apps.get_model("backend", "JobRecord")
    binding_model = apps.get_model("backend", "BulkJobBindingRecord")
    schedule_model = apps.get_model("backend", "BulkJobScheduleRecord")
    six_models = (identity_model, operation_model, extension_model, job_model, binding_model, schedule_model)
    for model in six_models:
        if not table_exists(real_wrapper, state["schema"], model._meta.db_table):
            _combine(result, "TABLE_MISSING")
            return
    result["migrated"] = True

    from pixs.backend.bulk_server_admission import (
        BulkAdmissionConflict,
        BulkAdmissionRefused,
        admit_bulk_operation,
    )

    default_probes = {"ensure": 0, "cursor": 0}
    default_wrapper = connections["default"]
    origin_ensure = default_wrapper.ensure_connection
    origin_cursor = default_wrapper.cursor

    def _default_ensure(*args, **kwargs):
        default_probes["ensure"] += 1
        raise AssertionError("accès default refusé")

    def _default_cursor(*args, **kwargs):
        default_probes["cursor"] += 1
        raise AssertionError("accès default refusé")

    default_wrapper.ensure_connection = _default_ensure
    default_wrapper.cursor = _default_cursor
    try:
        import pixs.backend.bulk_trusted_ports as ports_module
        from unit.test_bulk_server_admission import _base_time

        def _case_arguments(variant, export_format, identity_key=None, tenant_id="tenant-test", subject_id="actor-test"):
            policy = _valid_policy()
            start, operation_expiry, identity_expiry = _base_time(policy)
            suffix = uuid.uuid4().hex[:12]
            operation_id = "operation-" + suffix
            job_id = "job-" + suffix
            idempotency_key = identity_key if identity_key is not None else "idem-" + suffix
            if variant == "EXPORT":
                from unit.test_bulk_execution_values import _valid_execution_export

                execution = dict(_valid_execution_export())
            else:
                from unit.test_bulk_server_admission import _new_execution

                execution = dict(_new_execution(policy, operation_expiry))
                execution = dict(execution)
            mapping = _mapping()
            mapping_override = dict(mapping)
            mapping_override.update({"variant": variant, "format": export_format})
            execution.update(
                {
                    "bulk_type": variant,
                    "format": export_format,
                    "status": "REQUESTED",
                    "revision": 1,
                    "cancellation_requested": False,
                    "checkpoint_reference": None,
                    "result_reference": None,
                    "output_reference": None,
                    "output_version": None,
                    "output_sha256": None,
                    "output_size_bytes": None,
                    "operation_id": operation_id,
                    "idempotency_key": idempotency_key,
                    "mapping_reference": mapping_override["mapping_reference"],
                    "mapping_version": mapping_override["mapping_version"],
                    "resolved_context_reference": "context-test",
                    "policy_reference": "policy-test",
                    "policy_version": "1.0.0",
                    "expires_at": operation_expiry,
                }
            )
            progress = dict(execution["progress"])
            for key in ("validated_rows", "invalid_rows", "applied_rows", "execution_rejected_rows", "exported_rows"):
                progress[key] = 0
            progress["total_rows"] = 0 if variant == "IMPORT" else None
            if variant == "EXPORT":
                progress["exported_rows"] = 0
            execution["progress"] = progress
            if validate_bulk_execution_values(execution) != []:
                raise RuntimeError("fixture invalide avant admission")
            resolved_context = {
                "subject_id": subject_id,
                "tenant_id": tenant_id,
                "perimeter_reference": "perimeter-test",
                "context_reference": "context-test",
            }
            authority = _Authority(response={"decision": "ALLOW", "resolved_context": dict(resolved_context)})
            resolver = _Resolver()
            resolver.response = dict(mapping_override)
            governance_response = _resolved_response(policy_ref="policy-test", policy_ver="1.0.0")
            governance_response["resolved_context"] = dict(resolved_context)
            governance = _GovernanceResolve3(response=governance_response)
            bundle = ports_module.compose_bulk_trusted_ports(
                authority_adapter=authority,
                mapping_resolver=resolver,
                mapping_descriptors=(mapping_override,),
                owner_declarations=(("owner-test", "1.0.0", frozenset({"INVALID_FIELD"}), frozenset(mapping_override["target_fields"])),),
                governance_adapter=governance,
                owner_command_adapter=None,
                owner_projection_adapter=None,
                audit_adapter=None,
            )
            schedule = {
                "job_id": job_id,
                "policy_reference": "policy-test",
                "policy_version": "1.0.0",
                "next_run_at": None,
                "attempt_deadline": None,
                "failure_code": None,
                "revision": 1,
            }
            arguments = {
                "trusted_ports": bundle,
                "server_context": object(),
                "using": _REAL_ALIAS,
                "execution_values": execution,
                "policy": dict(policy),
                "owner_reference": "owner-test",
                "job_id": job_id,
                "job_causation_id": "cause-" + suffix,
                "schedule_values": schedule,
                "identity_expires_at": identity_expiry,
                "failure_codes": frozenset({"ECHEC_TEST"}),
                "now_utc": start,
            }
            return arguments, execution, schedule, policy

        def _six_counts():
            real_wrapper.ensure_connection()
            handle = real_wrapper.connection
            tables = [model._meta.db_table for model in six_models]
            from psycopg import sql

            counts = []
            for table in tables:
                query = (
                    sql.SQL("SELECT count(*) FROM {}.{}")
                    .format(sql.Identifier(state["schema"]), sql.Identifier(table))
                    .as_string(handle)
                )
                counts.append(int(scalar(real_wrapper, query, ())))
            return tuple(counts)

        result["phase"] = "POSITIVE_CASES"
        for variant, export_format, flag in (
            ("IMPORT", "CSV", "import_csv"),
            ("IMPORT", "NDJSON", "import_ndjson"),
            ("EXPORT", "CSV", "export_csv"),
            ("EXPORT", "NDJSON", "export_ndjson"),
        ):
            before = _six_counts()
            arguments, _, _, _ = _case_arguments(variant, export_format)
            returned = admit_bulk_operation(**arguments)
            after = _six_counts()
            observed = tuple(b - a for a, b in zip(before, after))
            result["case_expected"][flag] = (1, 1, 1, 1, 1, 1)
            result["case_observed"][flag] = observed
            if observed != (1, 1, 1, 1, 1, 1):
                _combine(result, "GRAPH_INCOMPLETE")
                return
            if returned != arguments["execution_values"]["operation_id"]:
                _combine(result, "OPERATION_MISMATCH")
                return
            stored = job_model.objects.using(_REAL_ALIAS).get(pk=arguments["job_id"])
            expected_phase = "STAGE" if variant == "IMPORT" else "EXPORT"
            binding = binding_model.objects.using(_REAL_ALIAS).get(job_id=arguments["job_id"])
            if binding.phase != expected_phase:
                _combine(result, "PHASE_DIVERGED")
                return
            if not (
                stored.job_type == ("pixs.bulk.stage" if variant == "IMPORT" else "pixs.bulk.export")
                and stored.job_version == "1.0.0"
                and stored.payload == {"execution_reference": returned, "execution_version": "1.0.0"}
                and stored.state == "PENDING"
                and stored.attempt_count == 0
                and stored.lease_owner is None
                and stored.lease_expires_at is None
                and stored.subject == {"requested_by_reference": arguments["execution_values"]["requested_by_reference"]}
                and stored.perimeter_reference == "perimeter-test"
                and stored.tenant_context == {
                    "tenant_context_reference": arguments["execution_values"]["tenant_context_reference"],
                    "scope_context_reference": arguments["execution_values"]["scope_context_reference"],
                }
                and stored.correlation_id == arguments["execution_values"]["correlation_id"]
                and stored.causation_id == arguments["job_causation_id"]
            ):
                _combine(result, "JOB_VALUES_DIVERGED")
                return
            from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
            from pixs.backend.bulk_admission_fingerprint import capture_bulk_admission_fingerprint
            from pixs.backend.bulk_server_admission import _FINGERPRINT_FIELDS
            execution = arguments["execution_values"]
            loaded = BulkRuntimeRepository(using=_REAL_ALIAS, failure_codes=arguments["failure_codes"]).load_execution(operation_id=returned)
            if loaded != execution:
                _combine(result, "EXECUTION_VALUES_DIVERGED")
                return
            expected_fingerprint, diagnostics = capture_bulk_admission_fingerprint({key: execution[key] for key in _FINGERPRINT_FIELDS})
            persisted_identity = identity_model.objects.using(_REAL_ALIAS).get(operation_id=returned)
            persisted_schedule = schedule_model.objects.using(_REAL_ALIAS).get(job_id=arguments["job_id"])
            if diagnostics or expected_fingerprint is None or not (
                bytes(persisted_identity.admission_content_snapshot) == expected_fingerprint.canonical_bytes
                and persisted_identity.admission_content_sha256 == expected_fingerprint.content_sha256
                and persisted_identity.admission_contract_version == "1.0.0"
                and persisted_identity.expires_at == arguments["identity_expires_at"]
                and persisted_identity.resolved_tenant_id == "tenant-test"
                and persisted_identity.resolved_subject_id == "actor-test"
                and persisted_schedule.as_values() == arguments["schedule_values"]
            ):
                _combine(result, "IDENTITY_OR_SCHEDULE_DIVERGED")
                return
            result[flag] = True

        result["phase"] = "REPLAY"
        replay_key = "idem-replay-" + uuid.uuid4().hex[:12]
        replay_first, _, _, replay_policy = _case_arguments("IMPORT", "CSV", identity_key=replay_key)
        original_operation = admit_bulk_operation(**replay_first)
        stored_identity = identity_model.objects.using(_REAL_ALIAS).get(operation_id=original_operation)
        before_snapshot = bytes(stored_identity.admission_content_snapshot)
        before_hash = str(stored_identity.admission_content_sha256)
        before_version = str(stored_identity.admission_contract_version)
        before_expiry = stored_identity.expires_at
        replay_second, _, _, _ = _case_arguments("IMPORT", "CSV", identity_key=replay_key)
        replay_execution = dict(replay_second["execution_values"])
        replay_execution["operation_id"] = "operation-" + uuid.uuid4().hex[:12]
        replay_execution["correlation_id"] = "corr-rejeu-" + uuid.uuid4().hex[:8]
        replay_execution["causation_id"] = "cause-rejeu-" + uuid.uuid4().hex[:8]
        replay_second["execution_values"] = replay_execution
        replay_second["job_id"] = "job-" + uuid.uuid4().hex[:12]
        replay_second["schedule_values"] = dict(replay_second["schedule_values"])
        replay_second["schedule_values"]["job_id"] = replay_second["job_id"]
        from datetime import timedelta as _delta

        policy_max = replay_policy["max_runtime_seconds"]
        late_now = replay_second["execution_values"]["expires_at"] + _delta(seconds=1)
        replay_second["now_utc"] = late_now
        replay_second["identity_expires_at"] = replay_second["execution_values"]["expires_at"] + _delta(
            seconds=replay_policy["replay_window_seconds"] + 3600
        )
        before_replay = _six_counts()
        returned_replay = admit_bulk_operation(**replay_second)
        after_replay = _six_counts()
        stored_again = identity_model.objects.using(_REAL_ALIAS).get(operation_id=original_operation)
        if returned_replay != original_operation or before_replay != after_replay:
            _combine(result, "REPLAY_NOT_STABLE")
            return
        if not (
            bytes(stored_again.admission_content_snapshot) == before_snapshot
            and str(stored_again.admission_content_sha256) == before_hash
            and str(stored_again.admission_contract_version) == before_version
            and stored_again.expires_at == before_expiry
        ):
            _combine(result, "REPLAY_IDENTITY_CHANGED")
            return
        del policy_max
        result["replay_stable"] = True

        conflict_arguments = dict(replay_second)
        conflict_execution = dict(conflict_arguments["execution_values"])
        conflict_execution["operation_id"] = "operation-" + uuid.uuid4().hex[:12]
        conflict_execution["input_reference"] = "entree-divergente"
        conflict_arguments["execution_values"] = conflict_execution
        conflict_arguments["job_id"] = "job-" + uuid.uuid4().hex[:12]
        conflict_arguments["schedule_values"] = dict(conflict_arguments["schedule_values"])
        conflict_arguments["schedule_values"]["job_id"] = conflict_arguments["job_id"]
        before_conflict = _six_counts()
        try:
            admit_bulk_operation(**conflict_arguments)
        except BulkAdmissionConflict as refused:
            if not (
                refused.args == (_TRUE_CONFLICT_MESSAGE,)
                and refused.__cause__ is None
                and refused.__context__ is None
            ):
                _combine(result, "CONFLICT_SHAPE_INVALID")
                return
        except Exception:
            _combine(result, "CONFLICT_TYPE_INVALID")
            return
        else:
            _combine(result, "CONFLICT_NOT_RAISED")
            return
        if _six_counts() != before_conflict:
            _combine(result, "CONFLICT_CREATED_GRAPH")
            return
        result["conflict_static"] = True

        result["phase"] = "KEY_ISOLATION"
        shared_key = "idem-acteur-" + uuid.uuid4().hex[:12]
        for tenant_id, subject_id in (("tenant-test", "actor-test"), ("tenant-autre", "actor-test"), ("tenant-test", "sujet-autre")):
            actor_arguments, _, _, _ = _case_arguments(
                "IMPORT", "CSV", identity_key=shared_key, tenant_id=tenant_id, subject_id=subject_id
            )
            before_actor = _six_counts()
            admit_bulk_operation(**actor_arguments)
            if tuple(b - a for a, b in zip(before_actor, _six_counts())) != (1, 1, 1, 1, 1, 1):
                _combine(result, "ACTOR_ISOLATION_FAILED")
                return
        result["actor_isolated"] = True
        result["tenant_isolated"] = True

        result["phase"] = "CONCURRENCY"
        concurrent_key = "idem-concurrent-" + uuid.uuid4().hex[:12]
        first_thread, _, _, _ = _case_arguments("IMPORT", "CSV", identity_key=concurrent_key)
        second_thread, _, _, _ = _case_arguments("IMPORT", "CSV", identity_key=concurrent_key)
        for arguments in (first_thread, second_thread):
            execution = dict(arguments["execution_values"])
            execution["operation_id"] = "operation-concurrent-" + uuid.uuid4().hex[:8]
            arguments["execution_values"] = execution
            arguments["job_id"] = "job-concurrent-" + uuid.uuid4().hex[:8]
            arguments["schedule_values"] = dict(arguments["schedule_values"])
            arguments["schedule_values"]["job_id"] = arguments["job_id"]
        barrier = threading.Barrier(2)
        thread_outputs = [None, None]
        thread_failures = []
        thread_refs = []
        thread_close_issues = []

        def _worker(index, arguments):
            from django.db import connections as worker_connections

            try:
                barrier.wait(timeout=10)
                thread_outputs[index] = admit_bulk_operation(**arguments)
            except Exception:
                thread_failures.append("THREAD_FAILED")
            finally:
                try:
                    for alias in worker_connections:
                        wrapper = worker_connections[alias]
                        if wrapper.connection is not None:
                            thread_refs.append(wrapper.connection)
                        wrapper.close()
                except Exception:
                    thread_close_issues.append("THREAD_CLOSE_FAILED")

        before_threads = _six_counts()
        workers = [
            threading.Thread(target=_worker, args=(0, first_thread)),
            threading.Thread(target=_worker, args=(1, second_thread)),
        ]
        state.setdefault("workers", []).extend(workers)
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=30)
        if any(worker.is_alive() for worker in workers):
            _combine(result, "THREAD_JOIN_TIMEOUT")
            return
        refs.extend(thread_refs)
        if thread_close_issues:
            close_failures.append("THREAD_CLOSE_FAILED")
        if thread_failures or thread_outputs[0] != thread_outputs[1]:
            _combine(result, "CONCURRENT_DIVERGED")
            return
        if tuple(b - a for a, b in zip(before_threads, _six_counts())) != (1, 1, 1, 1, 1, 1):
            _combine(result, "CONCURRENT_GRAPH_INVALID")
            return
        if len(thread_refs) != 2 or not all(handle.closed for handle in thread_refs):
            raise AssertionError("fermeture des deux connexions concurrentes non prouvée")
        result["concurrent_connections_closed"] = len(thread_refs)
        result["concurrent_single_graph"] = True

        result["phase"] = "LATE_ROLLBACK"
        schedule_table = schedule_model._meta.db_table
        trigger_name = "bulk_admission_refuse_schedule"
        function_name = "bulk_admission_refuse_schedule_fn"
        with managed_connection(
            state["database"], state["user"], state["password"], refs, close_failures,
            options=f"-c search_path={state['search_path']},pg_catalog",
        ) as trigger_connection:
            cursor = trigger_connection.cursor()
            try:
                cursor.execute(sql.SQL(
                    "CREATE FUNCTION {}() RETURNS trigger AS $late$ "
                    "BEGIN RAISE EXCEPTION 'refus tardif'; END; $late$ LANGUAGE plpgsql"
                ).format(sql.Identifier(function_name)))
                cursor.execute(sql.SQL(
                    "CREATE TRIGGER {} BEFORE INSERT ON {} FOR EACH ROW EXECUTE FUNCTION {}()"
                ).format(sql.Identifier(trigger_name), sql.Identifier(schedule_table), sql.Identifier(function_name)))
            finally:
                cursor.close()
        late_trace = {"schedule_attempts": 0, "successful_inserts": 0}

        def observe_late(execute, query, params, many, context):
            is_insert = type(query) is str and query.lstrip().upper().startswith("INSERT")
            if is_insert and schedule_table in query:
                late_trace["schedule_attempts"] += 1
            returned = execute(query, params, many, context)
            if is_insert:
                late_trace["successful_inserts"] += 1
            return returned

        try:
            late_arguments, _, _, _ = _case_arguments("IMPORT", "CSV")
            before_late = _six_counts()
            with real_wrapper.execute_wrapper(observe_late):
                try:
                    admit_bulk_operation(**late_arguments)
                except BulkAdmissionRefused as refused:
                    if refused.args != ("admission bulk refusée",) or refused.__cause__ is not None or refused.__context__ is not None:
                        raise AssertionError("forme du refus tardif divergente")
                else:
                    raise AssertionError("refus tardif absent")
            if _six_counts() != before_late or late_trace != {"schedule_attempts": 1, "successful_inserts": 5}:
                _combine(result, "LATE_ROLLBACK_UNPROVED")
                return
            result["late_trace"] = dict(late_trace)
        finally:
            with managed_connection(
                state["database"], state["user"], state["password"], refs, close_failures,
                options=pg_options(state["search_path"]),
            ) as trigger_cleanup:
                with trigger_cleanup.cursor() as cursor:
                    cursor.execute(sql.SQL("DROP TRIGGER IF EXISTS {} ON {}").format(sql.Identifier(trigger_name), sql.Identifier(schedule_table)))
                    cursor.execute(sql.SQL("DROP FUNCTION IF EXISTS {}()").format(sql.Identifier(function_name)))
        result["late_rollback_clean"] = True

        result["phase"] = "COMMIT_FAILURE"
        guard_table = "bulk_admission_commit_guard"
        constraint_name = "bulk_admission_schedule_guard_fk"
        with managed_connection(
            state["database"], state["user"], state["password"], refs, close_failures,
            options=f"-c search_path={state['search_path']},pg_catalog",
        ) as guard_connection:
            cursor = guard_connection.cursor()
            try:
                cursor.execute(sql.SQL("CREATE TABLE {} (identifier TEXT PRIMARY KEY)").format(sql.Identifier(guard_table)))
                cursor.execute(sql.SQL(
                    "ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY (policy_reference) REFERENCES {}(identifier) "
                    "DEFERRABLE INITIALLY DEFERRED NOT VALID"
                ).format(sql.Identifier(schedule_table), sql.Identifier(constraint_name), sql.Identifier(guard_table)))
            finally:
                cursor.close()
        commit_trace = {"successful_inserts": 0, "schedule_successes": 0, "commit_calls": 0, "commit_failures": 0}
        original_commit = real_wrapper.commit

        def observe_commit_sql(execute, query, params, many, context):
            returned = execute(query, params, many, context)
            if type(query) is str and query.lstrip().upper().startswith("INSERT"):
                commit_trace["successful_inserts"] += 1
                if schedule_table in query:
                    commit_trace["schedule_successes"] += 1
            return returned

        def observe_real_commit():
            commit_trace["commit_calls"] += 1
            try:
                return original_commit()
            except Exception:
                commit_trace["commit_failures"] += 1
                raise

        real_wrapper.commit = observe_real_commit
        try:
            commit_arguments, _, _, _ = _case_arguments("IMPORT", "CSV")
            before_commit = _six_counts()
            with real_wrapper.execute_wrapper(observe_commit_sql):
                try:
                    admit_bulk_operation(**commit_arguments)
                except BulkAdmissionRefused as refused:
                    if not (refused.args == ("admission bulk refusée",) and refused.__cause__ is None and refused.__context__ is None):
                        raise AssertionError("forme du refus COMMIT divergente")
                else:
                    raise AssertionError("échec COMMIT non propagé")
            if _six_counts() != before_commit or commit_trace != {"successful_inserts": 6, "schedule_successes": 1, "commit_calls": 1, "commit_failures": 1}:
                _combine(result, "COMMIT_ROLLBACK_UNPROVED")
                return
            result["commit_trace"] = dict(commit_trace)
        finally:
            real_wrapper.commit = original_commit
            with managed_connection(
                state["database"], state["user"], state["password"], refs, close_failures,
                options=pg_options(state["search_path"]),
            ) as guard_cleanup:
                with guard_cleanup.cursor() as cursor:
                    cursor.execute(sql.SQL("ALTER TABLE {} DROP CONSTRAINT IF EXISTS {}").format(sql.Identifier(schedule_table), sql.Identifier(constraint_name)))
                    cursor.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(guard_table)))
        result["commit_failure_clean"] = True

        result["phase"] = "VISIBILITY"
        import time
        visibility_trigger = "bulk_admission_visibility_schedule"
        visibility_function = "bulk_admission_visibility_fn"
        visibility_lock = uuid.uuid4().int & ((1 << 63) - 1)
        visibility_outputs = [None]
        visibility_failures = []
        visibility_refs = []
        visibility_ready = threading.Event()
        visibility_pid = [None]
        visibility_return_at = [None]
        visibility_arguments, _, _, _ = _case_arguments("IMPORT", "CSV")

        def visibility_worker():
            from django.db import connections as worker_connections
            try:
                wrapper = worker_connections[_REAL_ALIAS]
                wrapper.ensure_connection()
                visibility_refs.append(wrapper.connection)
                with wrapper.cursor() as cursor:
                    cursor.execute("SET statement_timeout = '15s'")
                    cursor.execute("SET lock_timeout = '12s'")
                    cursor.execute("SELECT pg_backend_pid()")
                    visibility_pid[0] = int(cursor.fetchone()[0])
                visibility_ready.set()
                visibility_outputs[0] = admit_bulk_operation(**visibility_arguments)
                visibility_return_at[0] = time.monotonic()
            except Exception:
                visibility_failures.append("VISIBILITY_WORKER_FAILED")
                visibility_ready.set()
            finally:
                try:
                    worker_connections.close_all()
                except Exception:
                    visibility_failures.append("VISIBILITY_CLOSE_FAILED")

        with managed_connection(
            state["database"], state["user"], state["password"], refs, close_failures,
            options=pg_options(state["search_path"]),
        ) as control:
            with control.cursor() as cursor:
                cursor.execute(sql.SQL(
                    "CREATE FUNCTION {}() RETURNS trigger AS $$ "
                    "BEGIN PERFORM pg_advisory_xact_lock({}); RETURN NEW; END; $$ LANGUAGE plpgsql"
                ).format(sql.Identifier(visibility_function), sql.Literal(visibility_lock)))
                cursor.execute(sql.SQL(
                    "CREATE TRIGGER {} BEFORE INSERT ON {} FOR EACH ROW EXECUTE FUNCTION {}()"
                ).format(sql.Identifier(visibility_trigger), sql.Identifier(schedule_table), sql.Identifier(visibility_function)))
            locked = False
            worker = None
            unlock_started = None
            before_visibility = _six_counts()
            try:
                scalar(control, "SELECT pg_advisory_lock(%s)", (visibility_lock,))
                locked = True
                worker = threading.Thread(target=visibility_worker)
                state.setdefault("workers", []).append(worker)
                worker.start()
                if not visibility_ready.wait(timeout=5) or visibility_pid[0] is None:
                    raise AssertionError("connexion du test de visibilité absente")
                deadline = time.monotonic() + 8
                blocked = False
                while time.monotonic() < deadline:
                    blocked = bool(scalar(
                        control,
                        "SELECT EXISTS (SELECT 1 FROM pg_stat_activity WHERE pid = %s AND wait_event_type = 'Lock' AND wait_event = 'advisory')",
                        (visibility_pid[0],),
                    ))
                    if blocked:
                        break
                    if not worker.is_alive():
                        break
                    time.sleep(0.02)
                visible_counts = tuple(int(scalar(
                    control,
                    sql.SQL("SELECT count(*) FROM {}.{}").format(sql.Identifier(state["schema"]), sql.Identifier(model._meta.db_table)),
                    (),
                )) for model in six_models)
                if not blocked or visible_counts != before_visibility or visibility_outputs[0] is not None or not worker.is_alive():
                    raise AssertionError("absence de visibilité avant COMMIT non prouvée")
                result["visibility_before_counts"] = visible_counts
                result["visibility_blocked"] = True
            finally:
                if locked:
                    unlock_started = time.monotonic()
                    scalar(control, "SELECT pg_advisory_unlock(%s)", (visibility_lock,))
                if worker is not None:
                    worker.join(timeout=30)
                    if worker.is_alive():
                        visibility_failures.append("VISIBILITY_JOIN_TIMEOUT")
                refs.extend(visibility_refs)
                with control.cursor() as cursor:
                    cursor.execute(sql.SQL("DROP TRIGGER IF EXISTS {} ON {}").format(sql.Identifier(visibility_trigger), sql.Identifier(schedule_table)))
                    cursor.execute(sql.SQL("DROP FUNCTION IF EXISTS {}()").format(sql.Identifier(visibility_function)))
            if visibility_failures or visibility_outputs[0] != visibility_arguments["execution_values"]["operation_id"]:
                raise AssertionError("retour du test de visibilité invalide")
            if visibility_return_at[0] is None or unlock_started is None or visibility_return_at[0] < unlock_started:
                raise AssertionError("retour observé avant libération du verrou")
            after_visibility = _six_counts()
            observed_visibility = tuple(b - a for a, b in zip(before_visibility, after_visibility))
            if observed_visibility != (1, 1, 1, 1, 1, 1):
                raise AssertionError("graphe après COMMIT invalide")
            result["case_expected"]["visibility"] = (1, 1, 1, 1, 1, 1)
            result["case_observed"]["visibility"] = observed_visibility
        result["visibility_ordered"] = True

        result["phase"] = "AMBIENT_TRANSACTION"
        ambient_arguments, _, _, _ = _case_arguments("IMPORT", "CSV")
        before_ambient = _six_counts()
        try:
            with transaction.atomic(using=_REAL_ALIAS):
                admit_bulk_operation(**ambient_arguments)
        except BulkAdmissionRefused:
            pass
        else:
            _combine(result, "AMBIENT_NOT_REFUSED")
            return
        if _six_counts() != before_ambient:
            _combine(result, "AMBIENT_DIRTY")
            return
        result["ambient_refused"] = True

        autocommit_arguments, _, _, _ = _case_arguments("IMPORT", "CSV")
        before_autocommit = _six_counts()
        alias_connection = transaction.get_connection(_REAL_ALIAS)
        previous_autocommit = alias_connection.get_autocommit()
        try:
            alias_connection.set_autocommit(False)
            try:
                admit_bulk_operation(**autocommit_arguments)
            except BulkAdmissionRefused:
                pass
            else:
                _combine(result, "AUTOCOMMIT_NOT_REFUSED")
                return
        finally:
            alias_connection.set_autocommit(previous_autocommit)
            alias_connection.rollback()
        if _six_counts() != before_autocommit:
            _combine(result, "AUTOCOMMIT_DIRTY")
            return
        result["autocommit_refused"] = True
    finally:
        default_wrapper.ensure_connection = origin_ensure
        default_wrapper.cursor = origin_cursor
    if default_probes != {"ensure": 0, "cursor": 0}:
        _combine(result, "DEFAULT_TOUCHED")
        return
    if default_wrapper.connection is not None:
        _combine(result, "DEFAULT_CONNECTED")
        return
    result["default_untouched"] = True

    with managed_connection(
        state["database"], state["user"], state["password"], refs, close_failures
    ) as identity_connection:
        public_tables = (
            "backend_featureflagsourcesnapshotrecord",
            "backend_jobrecord",
            "backend_bulkoperationrecord",
            "backend_bulkoperationexecutionrecord",
            "backend_bulkjobbindingrecord",
            "backend_bulkjobschedulerecord",
            "backend_bulkadmissionidentityrecord",
            "django_migrations",
        )
        state["public_after"] = tuple(
            table_identity(identity_connection, "public", table) for table in public_tables
        )
    result["public_stable"] = bool(state["public_after"] == state["public_before"])
    if not result["public_stable"]:
        _combine(result, "PUBLIC_DIVERGED")


def _finalize_bulk(result, refs, close_failures, state):
    for worker in state.get("workers", ()):
        worker.join(timeout=30)
        if worker.is_alive():
            result["cleanup_ok"] = False
            result["conns_closed"] = False
            result["real_pg"] = False
            result["phase"] = "COMPLETE"
            _combine(result, "WORKER_STILL_ACTIVE")
            return
    if state["configured"]:
        try:
            from django.db import connections

            for alias in connections:
                wrapper = connections[alias]
                if wrapper.connection is not None:
                    refs.append(wrapper.connection)
                wrapper.close()
        except Exception:
            close_failures.append("ORM_CLOSE_FAILED")
    if state["owned"]:
        if not state["dropped"]:
            try:
                if _INTEGRATION not in sys.path:
                    sys.path.insert(0, _INTEGRATION)
                import test_job_record_postgres_integration as base_harness

                with base_harness._managed_pg_connection(
                    state["database"],
                    state["user"],
                    state["password"],
                    refs,
                    close_failures,
                ) as cleanup_connection:
                    state["dropped"] = base_harness._drop_schema_if_owned(
                        cleanup_connection, state["schema"], True
                    )
            except Exception:
                state["dropped"] = False
        result["cleanup_ok"] = bool(state["dropped"])
        if not state["dropped"]:
            _combine(result, "CLEANUP_FAILED")
    else:
        result["cleanup_ok"] = False
    all_closed = not close_failures
    for handle in refs:
        try:
            all_closed = all_closed and bool(handle.closed)
        except Exception:
            all_closed = False
    result["conns_closed"] = bool(refs) and bool(all_closed)
    if not all_closed:
        _combine(result, "CONNECTION_CLOSE_FAILED")
    result["real_pg"] = bool(
        result["reason"] == "NONE"
        and result["cleanup_ok"]
        and result["conns_closed"]
        and all(result[key] for key in _REQUIRED_FLAGS)
    )
    result["phase"] = "COMPLETE"
    if not result["real_pg"] and result["reason"] == "NONE":
        result["reason"] = "CASE_INCOMPLETE"


def run_real_bulk_server_admission_postgres(root_str):
    """Callable PG réel invoqué uniquement par une commande CAB dédiée."""
    result = _closed_result()
    refs = []
    close_failures = []
    state = {
        "schema": None,
        "owned": False,
        "dropped": False,
        "configured": False,
        "search_path": None,
        "database": None,
        "user": None,
        "password": None,
        "public_before": "UNSET",
        "public_after": "UNSET",
    }
    with _mask_output():
        try:
            if type(root_str) is not str or root_str == "":
                _combine(result, "ROOT_INVALID")
            else:
                try:
                    resolved = str(Path(root_str).resolve())
                except Exception:
                    resolved = ""
                if resolved != _EXPECTED_ROOT:
                    _combine(result, "ROOT_MISMATCH")
                else:
                    found = _read_project_env(root_str)
                    if not isinstance(found, dict):
                        _combine(result, "ENV_REFUSED")
                    else:
                        values = tuple(
                            found.get(name)
                            for name in ("PG_DATABASE", "PG_USERNAME", "PG_PASSWORD")
                        )
                        if any(
                            type(value) is not str or value == "" for value in values
                        ):
                            _combine(result, "ENV_INCOMPLETE")
                        else:
                            (
                                state["database"],
                                state["user"],
                                state["password"],
                            ) = values
                            del values, found
                            result["phase"] = "ENV_READY"
                            _real_body(result, refs, close_failures, state)
        except Exception as failure:
            result["failed_phase"] = result["phase"]
            result["failure_type"] = type(failure).__name__
            frame = failure.__traceback__
            result["failure_line"] = None
            while frame is not None:
                if frame.tb_frame.f_code.co_filename == __file__:
                    result["failure_line"] = frame.tb_lineno
                frame = frame.tb_next
            _combine(result, "UNEXPECTED")
        finally:
            try:
                _finalize_bulk(result, refs, close_failures, state)
            except Exception:
                result["real_pg"] = False
                result["cleanup_ok"] = False
                result["conns_closed"] = False
                result["phase"] = "COMPLETE"
                _combine(result, "FINALIZATION_FAILED")
    return result


class BulkServerAdmissionPgHarnessSafeTests(unittest.TestCase):
    """Gardes inertes du harnais PG sans exécuter le callable réel."""

    def test_child_isolated_inert_and_guarded(self):
        """Le sous-processus frais reste inerte et gardé."""
        completed = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC, _TARGET],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, _MARKER)

    def test_bad_roots_without_database(self):
        """Les racines invalides sont refusées sans base."""
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = run_real_bulk_server_admission_postgres(bad_root)
            self.assertIs(outcome["real_pg"], False)
            self.assertEqual(outcome["phase"], "COMPLETE")
            self.assertEqual(outcome["reason"], "ROOT_INVALID")
            self.assertIs(outcome["cleanup_ok"], False)
            self.assertIs(outcome["conns_closed"], False)

    def test_result_schema_without_real_call(self):
        """Le schéma des résultats reste fermé sans appel réel."""
        outcome = run_real_bulk_server_admission_postgres("/synthetic/root")
        self.assertIs(outcome["real_pg"], False)
        self.assertEqual(outcome["reason"], "ROOT_MISMATCH")
        for key in _REQUIRED_FLAGS:
            self.assertIs(outcome[key], False)


if __name__ == "__main__":
    unittest.main()
