"""Harnais PostgreSQL isolé VALIDATE IMPORT VALIDATE_ONLY ; import inerte, PG réel mandaté.

Aucun effet au import ni à la découverte : stdlib uniquement au niveau
module. Le callable ``run_real_bulk_import_validate_postgres(root)``
vérifie la racine exacte avant tout effet puis compose le parcours
complet sur les vrais dépôts PostgreSQL (BulkRuntimeRepository,
BulkValidationReportRepository, même alias), sans aucun faux
remplaçant protected_unit/transactions/CAS/commit_checkpoint.
Secrets CISMP lus uniquement dans le processus de test via le parseur
partagé ; jamais dans le modèle, la sortie ou les exceptions brutes.
Sortie fermée statique : cases, flags, type d'exception et ligne locale
en cas d'échec, sans message ni secret. Schéma synthétique owned
unique, search_path strict schéma+pg_catalog, migration leaf existante,
tables public avant/après stables, dummy default intouché. Nettoyage
tenté en finally ; seules les sorties natives feront preuve.
Aucun verdict PG sans exécution native ultérieure.
"""

import asyncio
import hashlib
import json
import re
import subprocess
import sys
import textwrap
import threading
import unittest
import uuid
from contextlib import ExitStack, contextmanager
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_INTEGRATION = str(_ROOT / "tests" / "integration")
_TESTS = str(_ROOT / "tests")
_TARGET = str(Path(__file__))
_MARKER = "BULK_VALIDATE_PG_HARNESS_SAFE_OK\n"
_EXPECTED_ROOT = "/home/devops/datas/pixs"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

_PG_HOST = "127.0.0.1"
_PG_PORT = 5432
_CONNECT_TIMEOUT_SECONDS = 2
_ENV_READ_LIMIT = 65537
_SCHEMA_RE = re.compile(r"bulk_validate_[0-9a-f]{16}")
_FIXED_CODE_RE = re.compile(r"[A-Z][A-Z_]*")
_REAL_ALIAS = "bulk_validate_test"
_REPORT_TABLE = "backend_bulkvalidationreportrecord"

_REQUIRED_FLAGS = (
    "migrated",
    "model_state_coherent",
    "search_path_isolated",
    "csv_nominal",
    "ndjson_nominal",
    "owner_single_reject",
    "empty_ndjson_zero",
    "malformed_csv_incomplete",
    "malformed_ndjson_incomplete",
    "storage_hash_diverged",
    "storage_metadata_changed",
    "storage_close_failed",
    "invalid_metadata_type",
    "repository_type_guard",
    "alias_mismatch_guard",
    "vendor_guard",
    "authority_execute_refused",
    "obligations_refused",
    "owner_verdict_malformed",
    "authority_revoked_between_units",
    "read_result_refused_after_commit",
    "atomicity_report_insert_fails",
    "atomicity_checkpoint_insert_fails",
    "fault_after_checkpoint_before_transition",
    "cas_revision_changed_during_owner",
    "lease_lost_during_owner",
    "concurrent_single_result",
    "cancel_during_owner",
    "expiry_effective_refused",
    "cancel_after_report_before_transition",
    "expiry_after_report_before_transition",
    "replay_terminal_stable",
    "default_untouched",
    "public_stable",
)

_PUBLIC_TABLES = (
    "backend_featureflagsourcesnapshotrecord",
    "backend_jobrecord",
    "backend_bulkoperationrecord",
    "backend_bulkoperationexecutionrecord",
    "backend_bulkcheckpointrecord",
    "backend_bulkjobbindingrecord",
    "backend_bulkjobschedulerecord",
    "backend_bulkadmissionidentityrecord",
    "django_migrations",
    _REPORT_TABLE,
)

_CHUNK_TIMEOUT_SECONDS = 60

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

    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from psycopg import Connection

    src_path = sys.argv[1]
    target_path = sys.argv[2]
    sys.path.insert(0, src_path)

    import django
    from django.apps import apps
    from django.conf import settings

    assert settings.configured is False
    assert apps.ready is False

    guard_targets = (
        (psycopg, "connect", ()),
        (Connection, "connect", ()),
        (PGWrapper, "get_new_connection", (object(), {})),
        (socket.socket, "connect", (object(), ("127.0.0.1", 0))),
        (socket, "create_connection", (("127.0.0.1", 0),)),
        (subprocess, "Popen", (["true"],)),
        (subprocess, "run", (["true"],)),
        (builtins, "open", ("project.env", "rb")),
        (Path, "open", (Path("project.env"), "rb")),
        (os, "open", ("project.env", os.O_RDONLY)),
    )
    guards = [mock.Mock(side_effect=AssertionError("forbidden")) for _ in guard_targets]

    with ExitStack() as stack:
        for (target, name, _args), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))
        spec = importlib.util.spec_from_file_location(
            "bulk_validate_pg_harness_under_test", target_path
        )
        harness = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(harness)
        for (target, name, args), guard in zip(guard_targets, guards):
            try:
                getattr(target, name)(*args)
            except AssertionError:
                pass
            else:
                raise AssertionError("garde inactive")
            assert guard.call_count == 1
            guard.reset_mock()
        assert callable(harness.run_real_bulk_import_validate_postgres)
        assert callable(harness._read_project_env)
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = harness.run_real_bulk_import_validate_postgres(bad_root)
            assert outcome["real_pg"] is False
            assert outcome["phase"] == "COMPLETE"
            assert outcome["reason"] == "ROOT_INVALID"
        outcome = harness.run_real_bulk_import_validate_postgres("/synthetic/root")
        assert outcome["reason"] == "ROOT_MISMATCH"
        assert outcome["real_pg"] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [guard.call_count for guard in guards] == [0] * len(guards)

    print("BULK_VALIDATE_PG_HARNESS_SAFE_OK")
    """
).strip()


def _closed_result():
    result = {"real_pg": False, "phase": "INIT", "reason": "NONE"}
    for key in _REQUIRED_FLAGS:
        result[key] = False
    result["case_expected"] = {}
    result["case_observed"] = {}
    result["case_failures"] = {}
    result["case_sql"] = {}
    result["case_sql_writes"] = {}
    result["server_version"] = ""
    result["server_version_num"] = None
    result["cleanup_ok"] = False
    result["conns_closed"] = False
    return result


def _combine(result, code):
    if result["reason"] != "NONE":
        return
    if type(code) is str and _FIXED_CODE_RE.fullmatch(code) and code != "NONE":
        result["reason"] = code


def _read_project_env(root_str):
    if _INTEGRATION not in sys.path:
        sys.path.insert(0, _INTEGRATION)
    import test_pg_connectivity_integration as connectivity

    parse = connectivity._parse_env_text
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
    name = "bulk_validate_" + uuid.uuid4().hex[:16]
    if _SCHEMA_RE.fullmatch(name) is None:
        raise RuntimeError("nom de schema synthetique invalide")
    return name


def _failure_mark(result, case, failure):
    frame = failure.__traceback__
    line = None
    while frame is not None:
        if frame.tb_frame.f_code.co_filename == __file__:
            line = frame.tb_lineno
        frame = frame.tb_next
    result["case_failures"][case] = {"type": type(failure).__name__, "line": line}


def _real_body(result, refs, close_failures, state):
    from datetime import datetime, timedelta, timezone

    import django
    from django.apps import apps
    from django.conf import settings
    from django.db import connections
    from django.db.backends.signals import connection_created
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.state import ProjectState

    if _INTEGRATION not in sys.path:
        sys.path.insert(0, _INTEGRATION)
    if _TESTS not in sys.path:
        sys.path.insert(0, _TESTS)
    import test_job_record_postgres_integration as base_harness
    from unit.test_bulk_execution_values import _valid_execution_import, _valid_policy
    from unit.test_bulk_private_object_reader import (
        _Fournisseur,
        _FournisseurChangeant,
        _Resolveur,
        _metadonnees,
    )
    from unit.test_bulk_runtime_contracts import _CODES, _FIELDS, _mapping
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

    from pixs.backend import bulk_import_validate as orch
    from pixs.backend import bulk_streaming_import as flux

    codes_etendus = tuple(sorted(set(_CODES) | set(flux._CONTENT_CODES)))
    champs = tuple(sorted(_FIELDS))
    media_par_format = {"CSV": "text/csv", "NDJSON": "application/x-ndjson"}

    result["phase"] = "SCHEMA"
    state["schema"] = _safe_schema_name()
    with managed_connection(
        state["database"], state["user"], state["password"], refs, close_failures
    ) as admin_connection:
        state["public_before"] = tuple(
            table_identity(admin_connection, "public", table) for table in _PUBLIC_TABLES
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

    from pixs.backend.bulk_validation_report_record import BulkValidationReportRecord

    real_wrapper = connections[_REAL_ALIAS]
    real_wrapper.ensure_connection()
    manche_principal = real_wrapper.connection
    if manche_principal is not None:
        refs.append(manche_principal)
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
    if not leaf_nodes:
        _combine(result, "MIGRATION_TARGET_MISSING")
        return
    executor.migrate(list(leaf_nodes))
    for app_label, migration_name in leaf_nodes:
        if applied_count(real_wrapper, state["schema"], migration_name) < 1:
            _combine(result, "FORWARD_NOT_PROVED")
            return
    current_state = executor.loader.project_state(list(leaf_nodes))
    actual_state = ProjectState.from_apps(apps)
    detector = MigrationAutodetector(current_state, actual_state)
    reverse_detector = MigrationAutodetector(actual_state, current_state)
    if detector.changes(graph=executor.loader.graph) != {} or reverse_detector.changes(graph=executor.loader.graph) != {}:
        _combine(result, "AUTODETECT_DIVERGED")
        return
    result["model_state_coherent"] = True

    from pixs.backend.bulk_runtime_records import (
        BulkCheckpointRecord as CheckpointModel,
        BulkJobBindingRecord as BindingModel,
        BulkJobScheduleRecord as ScheduleModel,
        BulkOperationExecutionRecord as ExtensionModel,
    )
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
    from pixs.backend.bulk_validation_report_repository import (
        BulkValidationReportRepository,
    )
    from pixs.backend.models import JobRecord

    for model in (
        ExtensionModel,
        CheckpointModel,
        BindingModel,
        ScheduleModel,
        BulkValidationReportRecord,
        JobRecord,
    ):
        if not table_exists(real_wrapper, state["schema"], model._meta.db_table):
            _combine(result, "TABLE_MISSING")
            return
    result["migrated"] = True

    _SIGNAL_UID = "bulk-validate-harness"

    def _receiver(sender, connection, **kwargs):
        try:
            alias = getattr(connection, "alias", None)
        except Exception:
            return
        if alias != _REAL_ALIAS:
            return
        try:
            manche = connection.connection
        except Exception:
            raise AssertionError("signal sans manche réel")
        if manche is None:
            raise AssertionError("signal sans manche réel")
        refs.append(manche)

    connection_created.connect(_receiver, dispatch_uid=_SIGNAL_UID, weak=False)
    state["signal_connected"] = True
    state["signal_uid"] = _SIGNAL_UID
    if real_wrapper.connection is not None:
        refs.append(real_wrapper.connection)

    default_wrapper = connections["default"]
    DefaultDummy = type(default_wrapper)
    default_probes = {"ensure": 0, "cursor": 0}

    def _default_ensure(*args, **kwargs):
        default_probes["ensure"] += 1
        raise AssertionError("acces default refuse")

    def _default_cursor(*args, **kwargs):
        default_probes["cursor"] += 1
        raise AssertionError("acces default refuse")

    from unittest import mock as _mock_harnais
    _gardes = ExitStack()
    _gardes.enter_context(_mock_harnais.patch.object(DefaultDummy, "ensure_connection", new=_default_ensure))
    _gardes.enter_context(_mock_harnais.patch.object(DefaultDummy, "cursor", new=_default_cursor))
    state["gardes_default"] = _gardes

    try:
        import pixs.backend.bulk_trusted_ports as ports_module
        from asgiref.sync import sync_to_async

        runtime_repo = BulkRuntimeRepository(
            using=_REAL_ALIAS, failure_codes=frozenset({"ECHEC_TEST"})
        )
        report_repo = BulkValidationReportRepository(using=_REAL_ALIAS)

        class _Owner:
            """Port de commande reel : validate async, autres methodes piegees."""

            def __init__(self, verdicts=None, hook=None):
                self.calls = []
                self.execute_calls = []
                self.canonical_calls = []
                self.atomic_flags = []
                self.verdicts = dict(verdicts or {})
                self.hook = hook
                self.provider = None

            async def validate(self, contexte, entree, references):
                self.calls.append((contexte, dict(entree), references))
                provider = self.provider
                assert provider is not None
                assert provider.stat_appels == 2
                assert provider.iter_appels == 1
                assert provider.dernier_iterateur.ferme is True
                await self._probe_no_open_transaction()
                if self.hook is not None:
                    await self.hook(self, entree["line_index"])
                ligne = entree["line_index"]
                if ligne in self.verdicts:
                    issued = self.verdicts[ligne]
                    if isinstance(issued, Exception):
                        raise issued
                    return issued
                return {"accepted": True, "diagnostics": ()}

            async def _probe_no_open_transaction(self):
                def _query():
                    wrapper = connections[_REAL_ALIAS]
                    wrapper.ensure_connection()
                    refs.append(wrapper.connection)
                    with wrapper.cursor() as cursor:
                        cursor.execute("SELECT 1")
                        cursor.fetchone()
                    return bool(wrapper.in_atomic_block)

                in_atomic = await sync_to_async(_query, thread_sensitive=True)()
                self.atomic_flags.append(in_atomic)

            def execute(self, *args, **kwargs):
                self.execute_calls.append((args, kwargs))
                raise AssertionError("owner execute must never be invoked")

            def canonical_bytes(self, *args, **kwargs):
                self.canonical_calls.append((args, kwargs))
                raise AssertionError("owner canonical_bytes must never be invoked")

        class _RevokingAuthority(_Authority):
            """ALLOW budgete puis refus : aucune unite supplementaire."""

            def __init__(self, budget):
                super().__init__()
                self.budget = budget

            def check(self, context, action, operation, resource):
                self.calls.append((context, action, operation, resource))
                if len(self.calls) > self.budget:
                    return None
                return self.response

        class _ReadRefusingAuthority(_Authority):
            """EXECUTE ALLOW mais READ_RESULT refuse apres commit."""

            def check(self, context, action, operation, resource):
                self.calls.append((context, action, operation, resource))
                if action == "READ_RESULT":
                    return None
                return self.response

        def _drain_thread_conns():
            async def _close_all():
                await sync_to_async(connections.close_all, thread_sensitive=True)()

            asyncio.run(_close_all())
            connections[_REAL_ALIAS].close()

        def _table_counts():
            return (
                BulkValidationReportRecord.objects.using(_REAL_ALIAS).count(),
                CheckpointModel.objects.using(_REAL_ALIAS).count(),
            )

        def _compose_case(policy, owner, mapping, authority=None, obligations=()):
            response = _resolved_response(obligations=obligations)
            response["policy"]["limits"] = dict(policy)
            governance = _GovernanceResolve3(response=response)
            real_authority = _Authority() if authority is None else authority
            resolver = _Resolver()
            resolver.response = dict(mapping)
            bundle = ports_module.compose_bulk_trusted_ports(
                authority_adapter=real_authority,
                mapping_resolver=resolver,
                mapping_descriptors=(dict(mapping),),
                owner_declarations=(
                    ("owner-test", "1.0.0", codes_etendus, champs),
                ),
                governance_adapter=governance,
                owner_command_adapter=owner,
                owner_projection_adapter=None,
                audit_adapter=None,
            )
            return bundle

        def _prepare_case(tag, payload, fmt="CSV", verdicts=None, hook=None,
                          authority=None, obligations=(), provider_factory=None,
                          metadata_override=None):
            suffix = uuid.uuid4().hex[:12]
            operation_id = "op-validate-%s-%s" % (tag, suffix)
            job_id = "job-validate-%s-%s" % (tag, suffix)
            lease_owner = "lease-%s-%s" % (tag, suffix)
            metadata, _ = _metadonnees(payload)
            metadata["media_type"] = media_par_format[fmt]
            if metadata_override:
                metadata.update(metadata_override)
            mapping = dict(_mapping())
            mapping["format"] = fmt
            policy = _valid_policy()
            start = datetime.now(timezone.utc)
            execution = {
                **_valid_execution_import(),
                "operation_id": operation_id,
                "status": "REQUESTED",
                "commit_mode": "VALIDATE_ONLY",
                "format": fmt,
                "mapping_reference": mapping["mapping_reference"],
                "mapping_version": mapping["mapping_version"],
                "input_reference": metadata["object_reference"],
                "input_version": metadata["version_reference"],
                "input_sha256": metadata["sha256"],
                "input_size_bytes": metadata["size_bytes"],
                "policy_reference": "policy-test",
                "policy_version": "1.0.0",
                "expires_at": start + timedelta(seconds=1800),
                "revision": 1,
                "cancellation_requested": False,
                "progress": {
                    "total_rows": None,
                    "validated_rows": 0,
                    "invalid_rows": 0,
                    "applied_rows": 0,
                    "execution_rejected_rows": 0,
                    "exported_rows": 0,
                },
            }
            runtime_repo.create_execution(values=execution)
            JobRecord(
                job_id=job_id,
                job_type="pixs.bulk.stage",
                job_version="1.0.0",
                payload={"execution_reference": operation_id, "execution_version": "1.0.0"},
                subject={"requested_by_reference": "actor-test"},
                tenant_context={
                    "tenant_context_reference": "tenant-test",
                    "scope_context_reference": None,
                },
                correlation_id="corr-%s" % suffix,
                causation_id="cause-%s" % suffix,
                perimeter_reference="perimeter-test",
                state="PENDING",
                attempt_count=0,
                lease_owner=None,
                lease_expires_at=None,
            ).save(force_insert=True, using=_REAL_ALIAS)
            runtime_repo.bind_job(operation_id=operation_id, job_id=job_id, phase="VALIDATE")
            runtime_repo.create_schedule(values={
                "job_id": job_id,
                "policy_reference": "policy-test",
                "policy_version": "1.0.0",
                "next_run_at": None,
                "attempt_deadline": None,
                "failure_code": None,
                "revision": 1,
            })
            staged_revision = runtime_repo.apply_transition(
                operation_id=operation_id, expected_revision=1,
                to_status="STAGED", now=start,
            )
            real_owner = _Owner(verdicts=verdicts, hook=hook)
            bundle = _compose_case(
                policy, real_owner, mapping,
                authority=authority, obligations=obligations,
            )
            chunks = [payload] if payload else []
            if provider_factory is None:
                real_provider = _Fournisseur(dict(metadata), chunks)
            else:
                real_provider = provider_factory(dict(metadata), chunks)
            real_owner.provider = real_provider
            storage = _Resolveur(real_provider)
            return {
                "operation_id": operation_id,
                "job_id": job_id,
                "lease_owner": lease_owner,
                "metadata": metadata,
                "mapping": mapping,
                "policy": policy,
                "bundle": bundle,
                "owner": real_owner,
                "provider": real_provider,
                "storage": storage,
                "staged_revision": staged_revision,
                "start": start,
                "cancel_event": asyncio.Event(),
                "payload": payload,
            }

        def _base_kwargs(ctx, bundle=None, lease_owner=None,
                         runtime=None, report=None, event=None):
            now = datetime.now(timezone.utc)
            return {
                "trusted_ports": ctx["bundle"] if bundle is None else bundle,
                "runtime_repository": runtime_repo if runtime is None else runtime,
                "report_repository": report_repo if report is None else report,
                "server_context": object(),
                "operation_id": ctx["operation_id"],
                "job_id": ctx["job_id"],
                "owner_reference": "owner-test",
                "lease_owner": ctx["lease_owner"] if lease_owner is None else lease_owner,
                "expected_metadata": dict(ctx["metadata"]),
                "storage_resolver": ctx["storage"],
                "deadline": now + timedelta(seconds=600),
                "now": now,
                "cancel_event": ctx["cancel_event"] if event is None else event,
                "expected_schedule_revision": 1,
            }

        async def _arun(kwargs, counter_box):
            if counter_box is not None:
                def _install():
                    wrapper = connections[_REAL_ALIAS]
                    stack = ExitStack()

                    def _count(execute, query, params, many, context):
                        counter_box[0] += 1
                        try:
                            if type(query) is str:
                                text = query.lstrip()
                                if text.startswith("("):
                                    text = text.lstrip(" \t\r\n\f\v(")
                                verb = text.split(None, 1)[0].upper() if text else ""
                                if verb not in ("SELECT", "SHOW", "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT", "RELEASE"):
                                    counter_box[1] += 1
                            else:
                                counter_box[1] += 1
                        except Exception:
                            try:
                                counter_box[1] += 1
                            except Exception:
                                pass
                        return execute(query, params, many, context)

                    stack.enter_context(wrapper.execute_wrapper(_count))
                    return stack

                installed = await sync_to_async(_install, thread_sensitive=True)()
            else:
                installed = None
            try:
                return await orch.validate_import_only(**kwargs)
            finally:
                if installed is not None:
                    await sync_to_async(installed.close, thread_sensitive=True)()
                await sync_to_async(connections.close_all, thread_sensitive=True)()

        def _run_case(ctx, **overrides):
            counter = [0, 0]
            kwargs = _base_kwargs(ctx)
            kwargs.update(overrides)
            before = _table_counts()
            try:
                outcome, diagnostics = asyncio.run(_arun(kwargs, counter))
            finally:
                _drain_thread_conns()
            after = _table_counts()
            delta = (after[0] - before[0], after[1] - before[1])
            result["case_sql"][ctx["operation_id"]] = counter[0]
            result["case_sql_writes"][ctx["operation_id"]] = counter[1]
            return outcome, diagnostics, delta, counter[0]

        def _loaded(operation_id):
            return runtime_repo.load_execution(operation_id=operation_id)

        def _fetch_report(report_id, policy):
            return report_repo.get_report(
                report_id=report_id,
                policy=dict(policy),
                declared_codes=frozenset(codes_etendus),
                declared_fields=frozenset(champs),
            )

        def _prove_persisted(ctx, outcome, delta, expected_status,
                             expected_validated, expected_invalid,
                             expected_total, expected_complete,
                             expect_owner=True):
            assert delta == (1, 1)
            assert outcome is not None
            assert outcome.to_status == expected_status
            assert outcome.validated_rows == expected_validated
            assert outcome.invalid_rows == expected_invalid
            assert outcome.total_rows == expected_total
            assert outcome.complete is expected_complete
            assert outcome.checkpoint_revision == ctx["staged_revision"] + 2
            assert outcome.transition_revision == ctx["staged_revision"] + 3
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == expected_status
            assert loaded["revision"] == ctx["staged_revision"] + 3
            assert loaded["progress"]["validated_rows"] == expected_validated
            assert loaded["progress"]["invalid_rows"] == expected_invalid
            assert loaded["progress"]["applied_rows"] == 0
            assert loaded["progress"]["execution_rejected_rows"] == 0
            assert loaded["progress"]["exported_rows"] == 0
            assert loaded["progress"]["total_rows"] == expected_total
            assert loaded["checkpoint_reference"] is not None
            stored_checkpoint = CheckpointModel.objects.using(_REAL_ALIAS).get(
                operation_id=ctx["operation_id"],
            )
            assert stored_checkpoint.source_fingerprint == hashlib.sha256(
                ctx["payload"]
            ).hexdigest()
            assert stored_checkpoint.mapping_version == ctx["mapping"]["mapping_version"]
            assert stored_checkpoint.committed_unit_index == expected_validated
            assert stored_checkpoint.progress["validated_rows"] == expected_validated
            assert stored_checkpoint.progress["invalid_rows"] == expected_invalid
            snapshot = _fetch_report(outcome.report_id, ctx["policy"])
            assert snapshot is not None
            values = snapshot.as_values()
            assert values["operation_id"] == ctx["operation_id"]
            assert values["mode"] == "VALIDATE_ONLY"
            assert values["complete"] is expected_complete
            assert values["mapping_version"] == ctx["mapping"]["mapping_version"]
            assert values["progress"]["validated_rows"] == expected_validated
            assert values["progress"]["invalid_rows"] == expected_invalid
            assert len(values["diagnostics"]) <= ctx["policy"]["max_diagnostics"]
            assert ctx["provider"].stat_appels == 2
            assert ctx["provider"].iter_appels == 1
            assert ctx["provider"].dernier_iterateur.ferme is True
            if expect_owner:
                assert all(flag is False for flag in ctx["owner"].atomic_flags)
                assert ctx["owner"].atomic_flags != []
            else:
                assert ctx["owner"].calls == []
                assert ctx["owner"].atomic_flags == []
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []

        def _prove_refused_before_storage(ctx, outcome, diagnostics, delta, sql_count):
            assert outcome is None
            assert type(diagnostics) is list and diagnostics != []
            assert delta == (0, 0)
            assert sql_count == 0
            assert ctx["owner"].calls == []
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []

        _CSV = b"source_name,source_count\nalice,1\nbob,2\n"
        _NDJSON = (
            b'{"source_name":"alice","source_count":1}\n'
            b'{"source_name":"bob","source_count":2}\n'
        )

        result["phase"] = "POSITIVE_CASES"
        for flag, fmt, payload in (
            ("csv_nominal", "CSV", _CSV),
            ("ndjson_nominal", "NDJSON", _NDJSON),
        ):
            try:
                ctx = _prepare_case(flag, payload, fmt=fmt)
                outcome, diagnostics, delta, sql_count = _run_case(ctx)
                assert diagnostics == []
                assert sql_count > 0
                _prove_persisted(
                    ctx, outcome, delta, "COMPLETED", 2, 0, 2, True,
                )
                result["case_expected"][flag] = (1, 1)
                result["case_observed"][flag] = delta
                result[flag] = True
            except Exception as failure:
                _failure_mark(result, flag, failure)

        try:
            ctx = _prepare_case(
                "owner_single_reject", _CSV,
                verdicts={2: {"accepted": False, "diagnostics": (
                    {"code": "REJECTED", "field_reference": "name", "line_index": 2},
                )}},
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert diagnostics == []
            assert sql_count > 0
            _prove_persisted(
                ctx, outcome, delta, "COMPLETED_WITH_ERRORS", 2, 1, 2, True,
            )
            snapshot = _fetch_report(outcome.report_id, ctx["policy"])
            assert len(snapshot.as_values()["diagnostics"]) == 1
            result["case_expected"]["owner_single_reject"] = (1, 1)
            result["case_observed"]["owner_single_reject"] = delta
            result["owner_single_reject"] = True
        except Exception as failure:
            _failure_mark(result, "owner_single_reject", failure)

        try:
            ctx = _prepare_case("empty_ndjson_zero", b"", fmt="NDJSON")
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert diagnostics == []
            assert ctx["owner"].calls == []
            _prove_persisted(
                ctx, outcome, delta, "COMPLETED", 0, 0, 0, True,
                expect_owner=False,
            )
            result["case_expected"]["empty_ndjson_zero"] = (1, 1)
            result["case_observed"]["empty_ndjson_zero"] = delta
            result["empty_ndjson_zero"] = True
        except Exception as failure:
            _failure_mark(result, "empty_ndjson_zero", failure)

        result["phase"] = "INCOMPLETE_CASES"
        try:
            ctx = _prepare_case(
                "malformed_csv_incomplete",
                b"source_name,source_count\nalice,1\nbob\n",
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert diagnostics == []
            _prove_persisted(
                ctx, outcome, delta, "FAILED", 2, 1, None, False,
            )
            result["case_expected"]["malformed_csv_incomplete"] = (1, 1)
            result["case_observed"]["malformed_csv_incomplete"] = delta
            result["malformed_csv_incomplete"] = True
        except Exception as failure:
            _failure_mark(result, "malformed_csv_incomplete", failure)

        try:
            ctx = _prepare_case(
                "malformed_ndjson_incomplete",
                b'{"source_name":"alice","source_count":1}\nNOTJSON\n',
                fmt="NDJSON",
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert diagnostics == []
            _prove_persisted(
                ctx, outcome, delta, "FAILED", 2, 1, None, False,
            )
            result["case_expected"]["malformed_ndjson_incomplete"] = (1, 1)
            result["case_observed"]["malformed_ndjson_incomplete"] = delta
            result["malformed_ndjson_incomplete"] = True
        except Exception as failure:
            _failure_mark(result, "malformed_ndjson_incomplete", failure)

        result["phase"] = "STORAGE_REFUSALS"
        try:
            ctx = _prepare_case(
                "storage_hash_diverged", _CSV,
                metadata_override={"sha256": "b" * 64},
            )
            assert ctx["metadata"]["sha256"] == "b" * 64
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert ctx["owner"].calls == []
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            result["storage_hash_diverged"] = True
        except Exception as failure:
            _failure_mark(result, "storage_hash_diverged", failure)

        try:
            ctx = _prepare_case(
                "storage_metadata_changed", _CSV,
                provider_factory=lambda md, chunks: _FournisseurChangeant(md, chunks),
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert ctx["owner"].calls == []
            assert ctx["provider"].stat_appels == 2
            assert ctx["provider"].iter_appels == 1
            assert ctx["provider"].dernier_iterateur.ferme is True
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            result["storage_metadata_changed"] = True
        except Exception as failure:
            _failure_mark(result, "storage_metadata_changed", failure)

        try:
            ctx = _prepare_case(
                "storage_close_failed", _CSV,
                provider_factory=lambda md, chunks: _Fournisseur(md, chunks, fail_close=True),
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert ctx["owner"].calls == []
            assert ctx["provider"].dernier_iterateur is not None
            assert ctx["provider"].dernier_iterateur.ferme is True
            result["storage_close_failed"] = True
        except Exception as failure:
            _failure_mark(result, "storage_close_failed", failure)

        result["phase"] = "PRIMITIVE_GUARDS"
        try:
            ctx = _prepare_case("invalid_metadata_type", _CSV)
            broken = dict(ctx["metadata"])
            broken["size_bytes"] = "1024"
            outcome, diagnostics, delta, sql_count = _run_case(
                ctx, expected_metadata=broken,
            )
            _prove_refused_before_storage(ctx, outcome, diagnostics, delta, sql_count)
            result["invalid_metadata_type"] = True
        except Exception as failure:
            _failure_mark(result, "invalid_metadata_type", failure)

        try:
            ctx = _prepare_case("repository_type_guard", _CSV)
            outcome, diagnostics, delta, sql_count = _run_case(
                ctx, runtime_repository=object(),
            )
            _prove_refused_before_storage(ctx, outcome, diagnostics, delta, sql_count)
            result["repository_type_guard"] = True
        except Exception as failure:
            _failure_mark(result, "repository_type_guard", failure)

        try:
            from pixs.backend.bulk_validation_report_repository import (
                BulkValidationReportRepository as RealReportRepo,
            )

            ctx = _prepare_case("alias_mismatch_guard", _CSV)
            outcome, diagnostics, delta, sql_count = _run_case(
                ctx, report_repository=RealReportRepo(using="default"),
            )
            _prove_refused_before_storage(ctx, outcome, diagnostics, delta, sql_count)
            result["alias_mismatch_guard"] = True
        except Exception as failure:
            _failure_mark(result, "alias_mismatch_guard", failure)

        try:
            from pixs.backend.bulk_runtime_repository import (
                BulkRuntimeRepository as RealRuntimeRepo,
            )
            from pixs.backend.bulk_validation_report_repository import (
                BulkValidationReportRepository as RealReportRepo,
            )

            ctx = _prepare_case("vendor_guard", _CSV)
            outcome, diagnostics, delta, sql_count = _run_case(
                ctx,
                runtime_repository=RealRuntimeRepo(
                    using="default", failure_codes=frozenset({"ECHEC_TEST"})
                ),
                report_repository=RealReportRepo(using="default"),
            )
            _prove_refused_before_storage(ctx, outcome, diagnostics, delta, sql_count)
            result["vendor_guard"] = True
        except Exception as failure:
            _failure_mark(result, "vendor_guard", failure)

        try:
            failing = _Authority()
            failing.fail = True
            ctx = _prepare_case("authority_execute_refused", _CSV, authority=failing)
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            _prove_refused_before_storage(ctx, outcome, diagnostics, delta, sql_count)
            assert ctx["provider"].stat_appels == 0
            assert ctx["provider"].iter_appels == 0
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "STAGED"
            assert loaded["revision"] == ctx["staged_revision"]
            result["authority_execute_refused"] = True
        except Exception as failure:
            _failure_mark(result, "authority_execute_refused", failure)

        try:
            ctx = _prepare_case(
                "obligations_refused", _CSV, obligations=("obligation-test",),
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None
            assert type(diagnostics) is list and diagnostics != []
            assert any("bulk_import_validate.obligations" in str(item) for item in diagnostics)
            assert delta == (0, 0)
            assert result["case_sql_writes"][ctx["operation_id"]] == 0
            assert ctx["owner"].calls == []
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            assert ctx["provider"].stat_appels == 0
            assert ctx["provider"].iter_appels == 0
            storage_calls = getattr(ctx["storage"], "calls", None)
            if storage_calls is not None:
                assert storage_calls == []
            else:
                for attr in ("stat_appels", "iter_appels", "appels", "calls_stat", "resolve_calls"):
                    val = getattr(ctx["storage"], attr, None)
                    if isinstance(val, int):
                        assert val == 0
                    elif isinstance(val, (list, tuple)):
                        assert len(val) == 0
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "STAGED"
            assert loaded["revision"] == ctx["staged_revision"]
            assert loaded["progress"]["validated_rows"] == 0
            assert loaded["progress"]["invalid_rows"] == 0
            assert loaded["progress"]["applied_rows"] == 0
            assert loaded["progress"]["execution_rejected_rows"] == 0
            assert loaded["progress"]["exported_rows"] == 0
            stored_job = JobRecord.objects.using(_REAL_ALIAS).get(job_id=ctx["job_id"])
            assert stored_job.state == "PENDING"
            assert stored_job.attempt_count == 0
            assert stored_job.lease_owner is None
            assert stored_job.lease_expires_at is None
            stored_schedule = ScheduleModel.objects.using(_REAL_ALIAS).get(job_id=ctx["job_id"])
            assert stored_schedule.revision == 1
            result["obligations_refused"] = True
        except Exception as failure:
            _failure_mark(result, "obligations_refused", failure)

        result["phase"] = "OWNER_REFUSALS"
        try:
            ctx = _prepare_case(
                "owner_verdict_malformed", _CSV, verdicts={2: {"accepted": True}},
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert len(ctx["owner"].calls) == 1
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            result["owner_verdict_malformed"] = True
        except Exception as failure:
            _failure_mark(result, "owner_verdict_malformed", failure)

        try:
            ctx = _prepare_case(
                "authority_revoked_between_units", _CSV,
                authority=_RevokingAuthority(budget=3),
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert len(ctx["owner"].calls) == 1
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            result["authority_revoked_between_units"] = True
        except Exception as failure:
            _failure_mark(result, "authority_revoked_between_units", failure)

        result["phase"] = "READ_GUARD"
        try:
            ctx = _prepare_case(
                "read_result_refused_after_commit", _CSV,
                authority=_ReadRefusingAuthority(),
            )
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (1, 1)
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "COMPLETED"
            assert loaded["revision"] == ctx["staged_revision"] + 3
            result["case_expected"]["read_result_refused_after_commit"] = (1, 1)
            result["case_observed"]["read_result_refused_after_commit"] = delta
            result["read_result_refused_after_commit"] = True
        except Exception as failure:
            _failure_mark(result, "read_result_refused_after_commit", failure)

        result["phase"] = "ATOMICITY"
        from psycopg import sql as _pg_sql

        def _install_trigger(table, trigger_name, function_name, timing, target):
            with managed_connection(
                state["database"], state["user"], state["password"], refs, close_failures,
                options="-c search_path=%s,pg_catalog" % state["search_path"],
            ) as trigger_connection:
                cursor = trigger_connection.cursor()
                try:
                    cursor.execute(_pg_sql.SQL(
                        "CREATE FUNCTION {}() RETURNS trigger AS $late$ "
                        "BEGIN RAISE EXCEPTION 'panne synthetique'; END; $late$ LANGUAGE plpgsql"
                    ).format(_pg_sql.Identifier(function_name)))
                    cursor.execute(_pg_sql.SQL(
                        "CREATE TRIGGER {} {} ON {} FOR EACH ROW EXECUTE FUNCTION {}()"
                    ).format(
                        _pg_sql.Identifier(trigger_name),
                        _pg_sql.SQL(timing),
                        _pg_sql.Identifier(table),
                        _pg_sql.Identifier(function_name),
                    ))
                    _ = target
                finally:
                    cursor.close()

        def _drop_trigger(table, trigger_name, function_name):
            with managed_connection(
                state["database"], state["user"], state["password"], refs, close_failures,
                options=pg_options(state["search_path"]),
            ) as cleanup_connection:
                with cleanup_connection.cursor() as cursor:
                    cursor.execute(_pg_sql.SQL("DROP TRIGGER IF EXISTS {} ON {}").format(
                        _pg_sql.Identifier(trigger_name), _pg_sql.Identifier(table)))
                    cursor.execute(_pg_sql.SQL("DROP FUNCTION IF EXISTS {}()").format(
                        _pg_sql.Identifier(function_name)))

        for flag, model, timing in (
            ("atomicity_report_insert_fails", BulkValidationReportRecord,
             "BEFORE INSERT"),
            ("atomicity_checkpoint_insert_fails", CheckpointModel,
             "BEFORE INSERT"),
        ):
            trigger_name = "bulk_validate_refuse_%s" % flag
            function_name = "bulk_validate_refuse_%s_fn" % flag
            try:
                ctx = _prepare_case(flag, _CSV)
                _install_trigger(
                    model._meta.db_table, trigger_name, function_name,
                    timing, ctx["operation_id"],
                )
                try:
                    outcome, diagnostics, delta, sql_count = _run_case(ctx)
                finally:
                    _drop_trigger(model._meta.db_table, trigger_name, function_name)
                assert outcome is None and diagnostics != []
                assert delta == (0, 0)
                loaded = _loaded(ctx["operation_id"])
                assert loaded["status"] == "VALIDATING"
                assert loaded["revision"] == ctx["staged_revision"] + 1
                assert loaded["progress"]["validated_rows"] == 0
                assert loaded["progress"]["invalid_rows"] == 0
                assert ctx["owner"].execute_calls == []
                assert ctx["owner"].canonical_calls == []
                result[flag] = True
            except Exception as failure:
                try:
                    _drop_trigger(model._meta.db_table, trigger_name, function_name)
                except Exception:
                    close_failures.append("TRIGGER_CLEANUP_FAILED")
                    raise AssertionError("échec nettoyage trigger : %s" % flag)
                _failure_mark(result, flag, failure)

        try:
            flag = "fault_after_checkpoint_before_transition"
            ctx = _prepare_case(flag, _CSV)
            try:
                from pixs.backend.bulk_runtime_repository import ConstraintRefused as _RefusContrainte
            except Exception:
                try:
                    from pixs.backend.bulk_trusted_ports import ConstraintRefused as _RefusContrainte
                except Exception:
                    raise AssertionError("type ConstraintRefused introuvable")
            _origine_apply = BulkRuntimeRepository.apply_transition
            _crochet = {"atteint": False}

            def _transition_fautive(self, operation_id=None, expected_revision=None, to_status=None, now=None, *args, **kwargs):
                if operation_id == ctx["operation_id"] and expected_revision == ctx["staged_revision"] + 2:
                    existe_rapport = BulkValidationReportRecord.objects.using(_REAL_ALIAS).filter(operation_id=operation_id).exists()
                    existe_checkpoint = CheckpointModel.objects.using(_REAL_ALIAS).filter(operation_id=operation_id).exists()
                    charge = self.load_execution(operation_id=operation_id)
                    assert existe_rapport is True
                    assert existe_checkpoint is True
                    assert charge["revision"] == ctx["staged_revision"] + 2
                    assert charge["progress"]["validated_rows"] == 2
                    _crochet["atteint"] = True
                    raise _RefusContrainte("panne synthetique apres checkpoint")
                return _origine_apply(self, operation_id=operation_id, expected_revision=expected_revision, to_status=to_status, now=now, *args, **kwargs)

            from unittest import mock as _mock_transition
            with _mock_transition.patch.object(BulkRuntimeRepository, "apply_transition", new=_transition_fautive):
                outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert _crochet["atteint"] is True
            assert delta == (0, 0)
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            assert loaded["progress"]["validated_rows"] == 0
            assert loaded["progress"]["invalid_rows"] == 0
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            result[flag] = True
        except Exception as failure:
            _failure_mark(result, "fault_after_checkpoint_before_transition", failure)

        result["phase"] = "CONCURRENCY"
        try:
            ctx = _prepare_case("cas_revision_changed_during_owner", _CSV)

            async def _bump_hook(owner, ligne):
                if ligne != 2:
                    return

                def _write():
                    wrapper = connections[_REAL_ALIAS]
                    wrapper.ensure_connection()
                    refs.append(wrapper.connection)
                    with wrapper.cursor() as cursor:
                        cursor.execute(
                            _pg_sql.SQL(
                                "UPDATE {} SET revision = revision + 1 WHERE operation_id = %s"
                            ).format(_pg_sql.Identifier(ExtensionModel._meta.db_table)),
                            (ctx["operation_id"],),
                        )

                await sync_to_async(_write, thread_sensitive=True)()

            ctx["owner"].hook = _bump_hook
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            loaded = _loaded(ctx["operation_id"])
            assert loaded["revision"] == ctx["staged_revision"] + 2
            result["cas_revision_changed_during_owner"] = True
        except Exception as failure:
            _failure_mark(result, "cas_revision_changed_during_owner", failure)

        try:
            ctx = _prepare_case("lease_lost_during_owner", _CSV)

            async def _steal_hook(owner, ligne):
                if ligne != 2:
                    return

                def _steal():
                    JobRecord.objects.using(_REAL_ALIAS).filter(
                        job_id=ctx["job_id"]
                    ).update(lease_owner="lease-voleur")

                await sync_to_async(_steal, thread_sensitive=True)()

            ctx["owner"].hook = _steal_hook
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            assert JobRecord.objects.using(_REAL_ALIAS).get(
                job_id=ctx["job_id"]
            ).lease_owner == "lease-voleur"
            result["lease_lost_during_owner"] = True
        except Exception as failure:
            _failure_mark(result, "lease_lost_during_owner", failure)

        try:
            ctx = _prepare_case("concurrent_single_result", _CSV)
            barrier = threading.Barrier(2)
            outputs = [None, None]
            thread_failures = []
            thread_refs = []

            def _worker(index, lease_owner):
                from django.db import connections as worker_connections

                try:
                    barrier.wait(timeout=10)
                    owner = _Owner()
                    owner.provider = ctx["provider"]
                    bundle = _compose_case(ctx["policy"], owner, ctx["mapping"])
                    now = datetime.now(timezone.utc)
                    outcome, _ = asyncio.run(_arun(
                        {
                            "trusted_ports": bundle,
                            "runtime_repository": BulkRuntimeRepository(
                                using=_REAL_ALIAS, failure_codes=frozenset({"ECHEC_TEST"})
                            ),
                            "report_repository": BulkValidationReportRepository(
                                using=_REAL_ALIAS
                            ),
                            "server_context": object(),
                            "operation_id": ctx["operation_id"],
                            "job_id": ctx["job_id"],
                            "owner_reference": "owner-test",
                            "lease_owner": lease_owner,
                            "expected_metadata": dict(ctx["metadata"]),
                            "storage_resolver": ctx["storage"],
                            "deadline": now + timedelta(seconds=600),
                            "now": now,
                            "cancel_event": asyncio.Event(),
                            "expected_schedule_revision": 1,
                        },
                        None,
                    ))
                    outputs[index] = (outcome, owner)
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
                        thread_failures.append("THREAD_CLOSE_FAILED")

            before = _table_counts()
            workers = [
                threading.Thread(target=_worker, args=(0, "lease-concurrent-a")),
                threading.Thread(target=_worker, args=(1, "lease-concurrent-b")),
            ]
            state.setdefault("workers", []).extend(workers)
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(timeout=_CHUNK_TIMEOUT_SECONDS)
            if any(worker.is_alive() for worker in workers):
                raise AssertionError("threads concurrents bloques")
            refs.extend(thread_refs)
            after = _table_counts()
            delta = (after[0] - before[0], after[1] - before[1])
            assert thread_failures == []
            winners = [item for item in outputs if item is not None and item[0] is not None]
            assert len(winners) == 1
            assert delta == (1, 1)
            winner_owner = winners[0][1]
            assert winner_owner.execute_calls == []
            assert winner_owner.canonical_calls == []
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] in ("COMPLETED", "COMPLETED_WITH_ERRORS")
            result["case_expected"]["concurrent_single_result"] = (1, 1)
            result["case_observed"]["concurrent_single_result"] = delta
            result["concurrent_single_result"] = True
        except Exception as failure:
            _failure_mark(result, "concurrent_single_result", failure)

        result["phase"] = "INTERRUPTIONS"
        try:
            ctx = _prepare_case("cancel_during_owner", _CSV)
            event = ctx["cancel_event"]

            async def _hook_cancel(owner, ligne):
                if ligne == 2:
                    event.set()

            ctx["owner"].hook = _hook_cancel
            outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert event.is_set()
            assert len(ctx["owner"].calls) == 1
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            assert loaded["progress"]["validated_rows"] == 0
            assert loaded["progress"]["invalid_rows"] == 0
            result["cancel_during_owner"] = True
        except Exception as failure:
            _failure_mark(result, "cancel_during_owner", failure)

        try:
            ctx = _prepare_case("expiry_effective_refused", _CSV)
            now = datetime.now(timezone.utc)
            echeance = now + timedelta(seconds=0.3)

            async def _hook_expiry(owner, ligne):
                if ligne == 2:
                    import asyncio as _asyncio_lent
                    await _asyncio_lent.sleep(0.8)

            ctx["owner"].hook = _hook_expiry
            outcome, diagnostics, delta, sql_count = _run_case(
                ctx, deadline=echeance,
            )
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert len(ctx["owner"].calls) == 1
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            assert datetime.now(timezone.utc) >= echeance
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            assert loaded["progress"]["validated_rows"] == 0
            assert loaded["progress"]["invalid_rows"] == 0
            result["expiry_effective_refused"] = True
        except Exception as failure:
            _failure_mark(result, "expiry_effective_refused", failure)

        try:
            ctx = _prepare_case("cancel_after_report_before_transition", _CSV)
            event = ctx["cancel_event"]
            boucle = {}
            insert_atteint = {"oui": False}
            atomic_ok = {"oui": False}
            from pixs.backend.bulk_validation_report_repository import BulkValidationReportRepository as _RR_after
            _origine_insert = _RR_after.insert_report

            async def _hook_after(owner, ligne):
                import asyncio as _asyncio_after
                boucle["loop"] = _asyncio_after.get_running_loop()

            def _insert_apres_rapport(self, *args, **kwargs):
                issue = _origine_insert(self, *args, **kwargs)
                try:
                    from django.db import connections as _conns_insert
                    in_atomic = bool(_conns_insert[_REAL_ALIAS].in_atomic_block)
                except Exception:
                    raise AssertionError("atomicité illisible")
                if in_atomic is not True:
                    raise AssertionError("hors transaction")
                atomic_ok["oui"] = True
                existe = BulkValidationReportRecord.objects.using(_REAL_ALIAS).filter(
                    operation_id=ctx["operation_id"]
                ).exists()
                if existe is not True:
                    raise AssertionError("insertion non persistée")
                insert_atteint["oui"] = True
                manche_loop = boucle.get("loop")
                if manche_loop is None:
                    raise AssertionError("boucle non capturée")
                try:
                    manche_loop.call_soon_threadsafe(event.set)
                except Exception:
                    raise AssertionError("échec signal annulation")
                import time as _temps_after
                _temps_after.sleep(0.02)
                return issue

            ctx["owner"].hook = _hook_after
            from unittest import mock as _mock_after
            with _mock_after.patch.object(_RR_after, "insert_report", new=_insert_apres_rapport):
                outcome, diagnostics, delta, sql_count = _run_case(ctx)
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert event.is_set()
            assert insert_atteint["oui"] is True
            assert atomic_ok["oui"] is True
            assert len(ctx["owner"].calls) == 2
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            assert loaded["progress"]["validated_rows"] == 0
            assert loaded["progress"]["invalid_rows"] == 0
            result["cancel_after_report_before_transition"] = True
        except Exception as failure:
            _failure_mark(result, "cancel_after_report_before_transition", failure)

        try:
            ctx = _prepare_case("expiry_after_report_before_transition", _CSV)
            debut = datetime.now(timezone.utc)
            echeance = debut + timedelta(seconds=2)
            boucle_exp = {}
            insert_atteint = {"oui": False}
            atomic_ok = {"oui": False}
            from pixs.backend.bulk_validation_report_repository import BulkValidationReportRepository as _RR_exp_after
            _origine_exp = _RR_exp_after.insert_report

            async def _hook_exp_after(owner, ligne):
                import asyncio as _asyncio_exp_after
                boucle_exp["loop"] = _asyncio_exp_after.get_running_loop()

            def _insert_apres_echeance(self, *args, **kwargs):
                issue = _origine_exp(self, *args, **kwargs)
                try:
                    from django.db import connections as _conns_exp
                    in_atomic = bool(_conns_exp[_REAL_ALIAS].in_atomic_block)
                except Exception:
                    raise AssertionError("atomicité illisible")
                if in_atomic is not True:
                    raise AssertionError("hors transaction")
                atomic_ok["oui"] = True
                existe = BulkValidationReportRecord.objects.using(_REAL_ALIAS).filter(
                    operation_id=ctx["operation_id"]
                ).exists()
                if existe is not True:
                    raise AssertionError("insertion non persistée")
                insert_atteint["oui"] = True
                limite = echeance + timedelta(seconds=0.02)
                import time as _temps_exp
                while datetime.now(timezone.utc) < limite:
                    _temps_exp.sleep(0.005)
                    if (datetime.now(timezone.utc) - debut).total_seconds() > 2.1:
                        break
                return issue

            ctx["owner"].hook = _hook_exp_after
            from unittest import mock as _mock_exp_after
            with _mock_exp_after.patch.object(_RR_exp_after, "insert_report", new=_insert_apres_echeance):
                outcome, diagnostics, delta, sql_count = _run_case(
                    ctx, deadline=echeance,
                )
            assert outcome is None and diagnostics != []
            assert delta == (0, 0)
            assert insert_atteint["oui"] is True
            assert atomic_ok["oui"] is True
            assert len(ctx["owner"].calls) == 2
            assert ctx["owner"].execute_calls == []
            assert ctx["owner"].canonical_calls == []
            assert datetime.now(timezone.utc) >= echeance
            assert (datetime.now(timezone.utc) - debut).total_seconds() <= 2.5
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "VALIDATING"
            assert loaded["revision"] == ctx["staged_revision"] + 1
            assert loaded["progress"]["validated_rows"] == 0
            assert loaded["progress"]["invalid_rows"] == 0
            result["expiry_after_report_before_transition"] = True
        except Exception as failure:
            _failure_mark(result, "expiry_after_report_before_transition", failure)

        result["phase"] = "REPLAY"
        try:
            ctx = _prepare_case("replay_terminal_stable", _CSV)
            first, diagnostics, first_delta, _ = _run_case(ctx)
            assert first is not None and diagnostics == []
            assert first_delta == (1, 1)
            before = _table_counts()
            owner_calls = len(ctx["owner"].calls)
            second, second_diagnostics, second_delta, _ = _run_case(ctx)
            after = _table_counts()
            assert second is None and second_diagnostics != []
            assert second_delta == (0, 0)
            assert (after[0] - before[0], after[1] - before[1]) == (0, 0)
            assert len(ctx["owner"].calls) == owner_calls
            loaded = _loaded(ctx["operation_id"])
            assert loaded["status"] == "COMPLETED"
            result["case_expected"]["replay_terminal_stable"] = (1, 1)
            result["case_observed"]["replay_terminal_stable"] = first_delta
            result["replay_terminal_stable"] = True
        except Exception as failure:
            _failure_mark(result, "replay_terminal_stable", failure)
    finally:
        try:
            _gardes.close()
        except Exception:
            _combine(result, "DEFAULT_RESTORE_FAILED")
            close_failures.append("DEFAULT_RESTORE_FAILED")
    if default_probes != {"ensure": 0, "cursor": 0}:
        _combine(result, "DEFAULT_TOUCHED")
        return
    if default_wrapper.connection is not None:
        _combine(result, "DEFAULT_CONNECTED")
        return
    if type(connections["default"]).__module__ != "django.db.backends.dummy.base":
        _combine(result, "DEFAULT_BACKEND_DIVERGED")
        return
    result["default_untouched"] = True

    with managed_connection(
        state["database"], state["user"], state["password"], refs, close_failures
    ) as identity_connection:
        state["public_after"] = tuple(
            table_identity(identity_connection, "public", table) for table in _PUBLIC_TABLES
        )
    result["public_stable"] = bool(state["public_after"] == state["public_before"])
    if not result["public_stable"]:
        _combine(result, "PUBLIC_DIVERGED")


def _finalize_bulk(result, refs, close_failures, state):
    for worker in state.get("workers", ()):
        worker.join(timeout=_CHUNK_TIMEOUT_SECONDS)
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
            from django.db.backends.signals import connection_created

            uid = state.get("signal_uid", "bulk-validate-harness")
            if state.get("signal_connected"):
                try:
                    coupe = connection_created.disconnect(dispatch_uid=uid)
                except Exception as failure:
                    close_failures.append("SIGNAL_DISCONNECT_FAILED")
                    raise AssertionError("échec déconnexion signal")
                if coupe is False:
                    close_failures.append("SIGNAL_DISCONNECT_FAILED")
                    raise AssertionError("échec déconnexion signal : uid introuvable")
                state["signal_connected"] = False
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


def run_real_bulk_import_validate_postgres(root_str):
    """Callable PG reel invoque uniquement par une commande CAB dediee."""
    result = _closed_result()
    refs = []
    close_failures = []
    state = {
        "schema": None,
        "owned": False,
        "dropped": False,
        "configured": False,
        "signal_connected": False,
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
            frame = failure.__traceback__
            line = None
            while frame is not None:
                if frame.tb_frame.f_code.co_filename == __file__:
                    line = frame.tb_lineno
                frame = frame.tb_next
            result["failed_phase"] = result["phase"]
            result["failure_type"] = type(failure).__name__
            result["failure_line"] = line
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


class BulkImportValidatePgHarnessSafeTests(unittest.TestCase):
    """Gardes inertes du harnais PG sans executer le callable reel."""

    def test_child_isolated_inert_and_guarded(self):
        """Le sous-processus frais reste inerte et garde."""
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
        """Les racines invalides sont refusees sans base."""
        for bad_root in (None, "", 0, b"/home/devops/datas/pixs"):
            outcome = run_real_bulk_import_validate_postgres(bad_root)
            self.assertIs(outcome["real_pg"], False)
            self.assertEqual(outcome["phase"], "COMPLETE")
            self.assertEqual(outcome["reason"], "ROOT_INVALID")
            self.assertIs(outcome["cleanup_ok"], False)
            self.assertIs(outcome["conns_closed"], False)

    def test_result_schema_without_real_call(self):
        """Le schema des resultats reste ferme sans appel reel."""
        outcome = run_real_bulk_import_validate_postgres("/synthetic/root")
        self.assertIs(outcome["real_pg"], False)
        self.assertEqual(outcome["reason"], "ROOT_MISMATCH")
        for key in _REQUIRED_FLAGS:
            self.assertIs(outcome[key], False)

    def test_entrypoint_help_is_inert(self):
        """Le point d'entree -h reste inerte et affiche l'usage."""
        completed = subprocess.run(
            [sys.executable, "-I", "-B", _TARGET, "-h"],
            cwd=str(_ROOT),
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("usage:", completed.stdout)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--real-pg":
        outcome = run_real_bulk_import_validate_postgres(str(_ROOT))
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome["real_pg"] else 1)
    unittest.main()
