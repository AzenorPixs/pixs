"""Modèles runtime Bulk : contrats exacts en processus frais sous gardes."""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
_MARKER = "BULK_RUNTIME_RECORDS_OFFLINE_SAFE_OK"
_CHILD = r'''
import socket
import subprocess
import sys
from contextlib import ExitStack
from unittest import mock

sys.path.insert(0, sys.argv[1])

_MARKER = "BULK_RECORD_OFFLINE_SAFE_OK"

import django
from django.apps import apps
from django.conf import settings

assert not settings.configured
assert not apps.ready

import psycopg
from django.db import connection
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

class GuardBlocked(Exception):
    def __init__(self, bucket):
        super().__init__("garde d'effet interdit")
        self.bucket = bucket

counters = {"db": 0, "network": 0, "process": 0}
blocked = {"db": 0, "network": 0, "process": 0}

def _make_guard(bucket):
    def _blocked(*args, **kwargs):
        counters[bucket] += 1
        raise GuardBlocked(bucket)
    return _blocked

guard_targets = [
    (PGWrapper, "get_new_connection", "db"),
    (psycopg, "connect", "db"),
    (psycopg.Connection, "connect", "db"),
    (socket.socket, "connect", "network"),
    (socket, "create_connection", "network"),
    (subprocess, "Popen", "process"),
    (subprocess, "run", "process"),
]

with ExitStack() as stack:
    for target, name, bucket in guard_targets:
        stack.enter_context(
            mock.patch.object(target, name, side_effect=_make_guard(bucket))
        )

    def _probe(target_call, bucket):
        try:
            target_call()
        except GuardBlocked as error:
            assert error.bucket == bucket, error.bucket
            return
        raise AssertionError("garde non déclenchée")

    _probe(lambda: PGWrapper.get_new_connection(object(), {}), "db")
    _probe(lambda: psycopg.connect(), "db")
    _probe(lambda: psycopg.Connection.connect(), "db")
    _probe(lambda: socket.socket.connect(object(), ("127.0.0.1", 0)), "network")
    _probe(lambda: socket.create_connection(("127.0.0.1", 0)), "network")
    _probe(lambda: subprocess.Popen(["true"]), "process")
    _probe(lambda: subprocess.run(["true"]), "process")
    assert counters == {"db": 3, "network": 2, "process": 2}, counters
    for key in counters:
        counters[key] = 0

    from django.core.exceptions import ValidationError
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.loader import MigrationLoader
    from django.db.migrations.operations import CreateModel
    from django.db.migrations.state import ProjectState

    settings.configure(
        DEFAULT_CHARSET="utf-8",
        INSTALLED_APPS=["pixs.backend"],
        SECRET_KEY="unit-offline-synthetic-only",
        DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "bulk_record_offline_synthetic"}},
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    django.setup()


    sys.path.insert(0, sys.argv[2])
    from datetime import datetime, timedelta, timezone, tzinfo
    from django.db import models
    import pixs.backend.bulk_runtime_records as records
    import pixs.backend.models as registered
    from unit.test_bulk_execution_values import _valid_execution_import

    E = records.BulkOperationExecutionRecord
    C = records.BulkCheckpointRecord
    B = records.BulkJobBindingRecord
    S = records.BulkJobScheduleRecord
    expected_names = [
        "BulkOperationExecutionRecord", "BulkCheckpointRecord",
        "BulkJobBindingRecord", "BulkJobScheduleRecord",
    ]
    assert records.__all__ == expected_names
    assert registered.__all__ == ["FeatureFlagSourceSnapshotRecord", "JobRecord"]
    assert registered.JobRecord._meta.local_fields and len(registered.JobRecord._meta.local_fields) == 13
    assert len(registered.BulkOperationRecord._meta.local_fields) == 9

    base_keys = (
        "operation_id", "bulk_type", "bulk_version", "status",
        "tenant_context_reference", "scope_context_reference", "format",
        "conflict_strategy", "commit_mode",
    )

    def extension():
        full = _valid_execution_import()
        return {key: value for key, value in full.items() if key not in base_keys}

    def progress():
        return {
            "total_rows": 1, "validated_rows": 1, "invalid_rows": 0,
            "applied_rows": 1, "execution_rejected_rows": 0, "exported_rows": 0,
        }

    def checkpoint():
        return {
            "checkpoint_id": "cp-marker", "operation_id": "op-marker",
            "phase": "APPLY", "source_fingerprint": "a" * 64,
            "mapping_version": "1.2.3-rc.1+build", "committed_unit_index": 1,
            "progress": progress(), "revision": 2, "owner_result_reference": None,
        }

    def binding():
        return {"operation_id": "op-marker", "job_id": "job-marker", "phase": "APPLY"}

    def schedule():
        return {
            "job_id": "job-marker", "policy_reference": "policy-marker",
            "policy_version": "1.0.0", "next_run_at": None,
            "attempt_deadline": None, "failure_code": None, "revision": 1,
        }

    def construct(model, values):
        if model is E:
            return model.from_values(operation_id="op-marker", values=values)
        return model.from_values(values)

    def refused(call, capacity=False):
        try:
            call()
        except ValidationError as error:
            expected = "bulk_runtime_capacity_unsupported" if capacity else "bulk_runtime_record_invalid"
            assert all(item.code == expected for item in error.error_list)
            assert all("HOSTILE-MARKER" not in message for message in error.messages)
        else:
            raise AssertionError("donnée invalide acceptée")

    class HostileMeta(type):
        def __eq__(self, other):
            raise AssertionError("égalité de type étranger")
        def __hash__(self):
            raise AssertionError("hash de type étranger")

    class Hostile(metaclass=HostileMeta):
        def __bool__(self):
            raise AssertionError("bool étranger")
        def __eq__(self, other):
            raise AssertionError("égalité étrangère")
        def __hash__(self):
            raise AssertionError("hash étranger")
        def __repr__(self):
            raise AssertionError("repr étranger")
        def __str__(self):
            raise AssertionError("str étranger")

    class ForeignDict(dict, metaclass=HostileMeta):
        def items(self):
            raise AssertionError("items étrangers")
        def copy(self):
            raise AssertionError("copy étrangère")

    class ForeignTimezone(tzinfo):
        def utcoffset(self, value):
            raise AssertionError("utcoffset étranger")
        def dst(self, value):
            raise AssertionError("dst étranger")
        def tzname(self, value):
            raise AssertionError("tzname étranger")

    class ForeignDatetime(datetime):
        @property
        def tzinfo(self):
            raise AssertionError("tzinfo de sous-classe")

    class KeyOnce:
        def __init__(self):
            self.calls = 0
        def __hash__(self):
            self.calls += 1
            if self.calls > 1:
                raise AssertionError("rehash étranger")
            return 17
        def __eq__(self, other):
            raise AssertionError("égalité de clé étrangère")

    for model, factory, count, field_count, excluded in (
        (E, extension, 27, 28, ["operation"]),
        (C, checkpoint, 9, 9, ["operation"]),
        (B, binding, 3, 3, ["operation", "job"]),
        (S, schedule, 7, 7, ["job"]),
    ):
        values = factory()
        assert len(values) == count
        assert len(model._meta.local_fields) == field_count
        assert apps.get_model("backend", model.__name__) is model
        assert not model.check(databases=[])
        for field in model._meta.local_fields:
            assert not field.has_default()
            assert not getattr(field, "auto_now", False)
            assert not getattr(field, "auto_now_add", False)
            if field.is_relation:
                assert field.remote_field.related_name == "+"
                assert field.remote_field.on_delete is models.PROTECT
            if isinstance(field, models.TextField):
                assert field.max_length is None

        row = construct(model, values)
        assert row._state.adding
        assert row.as_values() == values
        assert row.as_values() is not row.as_values()
        row.full_clean(exclude=excluded, validate_unique=False, validate_constraints=False)
        assert values == factory()
        if "progress" in values:
            assert row.progress is not values["progress"]
            rendered = row.as_values()
            assert rendered["progress"] is not row.progress

        for key in values:
            absent = factory()
            del absent[key]
            refused(lambda absent=absent: construct(model, absent))
            foreign = factory()
            foreign[key] = Hostile()
            with mock.patch.object(records, "parse_version", side_effect=AssertionError("parse avant garde")):
                refused(lambda foreign=foreign: construct(model, foreign))
            raw = construct(model, factory())
            raw.__dict__[key] = Hostile()
            refused(lambda raw=raw, key=key: raw.full_clean(
                exclude=excluded + [key], validate_unique=False, validate_constraints=False,
            ))
        extra = factory()
        extra["HOSTILE-MARKER"] = Hostile()
        refused(lambda extra=extra: construct(model, extra))
        refused(lambda factory=factory: construct(model, ForeignDict(factory())))
        key = KeyOnce()
        foreign_keys = factory()
        foreign_keys[key] = Hostile()
        refused(lambda foreign_keys=foreign_keys: construct(model, foreign_keys))
        assert key.calls == 1

    for bad in (None, Hostile(), "", "HOSTILE-MARKER\x00"):
        refused(lambda bad=bad: E.from_values(operation_id=bad, values=extension()))
    refused(lambda: B.from_values({**binding(), "job_id": "op-marker"}))

    for factory, model, fields in (
        (extension, E, ("revision", "input_size_bytes", "output_size_bytes")),
        (checkpoint, C, ("revision", "committed_unit_index")),
        (schedule, S, ("revision",)),
    ):
        for field in fields:
            for bad in (True, -1):
                values = factory()
                values[field] = bad
                refused(lambda values=values, model=model: construct(model, values))
            values = factory()
            values[field] = 2**70
            refused(lambda values=values, model=model: construct(model, values), capacity=True)

    for field in ("expires_at",):
        for bad in (
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, tzinfo=ForeignTimezone()),
            ForeignDatetime(2026, 1, 1, tzinfo=timezone.utc),
        ):
            values = extension()
            values[field] = bad
            with mock.patch.object(records, "parse_version", side_effect=AssertionError("parse avant UTC")):
                refused(lambda values=values: construct(E, values))

    dbfield = E._meta.get_field("expires_at")
    trusted = datetime(2026, 1, 1, 2, tzinfo=timezone(timedelta(hours=2)))
    decoded = dbfield.from_db_value(trusted, None, None)
    assert type(decoded) is datetime and decoded.tzinfo is timezone.utc
    assert decoded == datetime(2026, 1, 1, tzinfo=timezone.utc)
    refused(lambda: dbfield.from_db_value(
        datetime(2026, 1, 1, tzinfo=ForeignTimezone()), None, None,
    ))
    refused(lambda: dbfield.from_db_value(datetime(2026, 1, 1), None, None))

    loader = MigrationLoader(None)
    migration = loader.disk_migrations[("backend", "0004_bulk_runtime_persistence")]
    assert migration.dependencies == [("backend", "0003_bulk_operation_record")]
    assert len(migration.operations) == 4
    assert all(isinstance(op, CreateModel) for op in migration.operations)
    assert [op.name for op in migration.operations] == expected_names
    expected_state = loader.project_state()
    actual_state = ProjectState.from_apps(apps)
    assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
    assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
    assert counters == {"db": 0, "network": 0, "process": 0}

print("BULK_RUNTIME_RECORDS_OFFLINE_SAFE_OK")
'''


class BulkRuntimeRecordsOfflineTests(unittest.TestCase):
    def test_models_exact_values_guards_and_migration(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD,
             str(_ROOT / "src"), str(_ROOT / "tests")],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER + "\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
