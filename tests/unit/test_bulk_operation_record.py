"""Preuves offline du modèle BulkOperationRecord v1, en processus frais sous gardes."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "BULK_RECORD_OFFLINE_SAFE_OK"
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONDONTWRITEBYTECODE": "1",
}

_CHILD = textwrap.dedent(
    r'''

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

        from django.db import models
        from pixs.backend.bulk_operation_record import BulkOperationRecord as Model
        import pixs.backend.models as registered
        from pixs.kernel.bulk_operations import (
            BulkCommitMode, BulkConflictStrategy, BulkOperationState,
            BulkOperationVariant, BulkReferenceFormat,
        )

        fields = (
            "operation_id", "bulk_type", "bulk_version", "status",
            "tenant_context_reference", "scope_context_reference", "format",
            "conflict_strategy", "commit_mode",
        )
        nullable = {"scope_context_reference", "conflict_strategy", "commit_mode"}
        enums = {
            "bulk_type": BulkOperationVariant, "status": BulkOperationState,
            "format": BulkReferenceFormat, "conflict_strategy": BulkConflictStrategy,
            "commit_mode": BulkCommitMode,
        }
        fixed = "valeurs de persistance bulk invalides"
        cases = []

        def valid(**over):
            values = dict(
                operation_id="opaque-é", bulk_type=next(iter(BulkOperationVariant)).value,
                bulk_version="1.2.3-rc.1+build.7",
                status=next(iter(BulkOperationState)).value,
                tenant_context_reference="equal opaque",
                scope_context_reference="equal opaque",
                format=next(iter(BulkReferenceFormat)).value,
                conflict_strategy=None, commit_mode=None,
            )
            values.update(over)
            return values

        def clean(row, **over):
            row.full_clean(validate_unique=False, validate_constraints=False, **over)

        def refused(call):
            try:
                call()
            except ValidationError as error:
                assert error.messages == [fixed], error.messages
                assert error.error_list[0].code == "bulk_operation_record_invalid"
            else:
                raise AssertionError("valeur invalide acceptée")

        assert tuple(f.name for f in Model._meta.fields) == fields
        assert all(isinstance(f, models.TextField) for f in Model._meta.fields)
        assert all(not f.has_default() and not f.is_relation for f in Model._meta.fields)
        assert {f.name for f in Model._meta.fields if f.null} == nullable
        assert Model._meta.pk.name == "operation_id"
        assert len(Model._meta.constraints) == 9
        assert apps.get_model("backend", "BulkOperationRecord") is Model
        assert registered.__all__ == ["FeatureFlagSourceSnapshotRecord", "JobRecord"]
        cases.append("nine_text_fields_no_defaults_no_relations_registration")

        data = valid()
        row = Model.from_values(data)
        assert row._state.adding is True
        assert all(getattr(row, key) == value for key, value in data.items())
        assert data == valid()
        clean(row)
        cases.append("factory_unsaved_opaque_equal_roundtrip_offline")

        for name in fields:
            missing = valid()
            del missing[name]
            refused(lambda missing=missing: Model.from_values(missing))
            refused(lambda name=name: clean(Model(**valid(**{name: 42})), exclude=[name]))
            refused(lambda name=name: clean(Model(**valid(**{name: ""}))))
            if name not in nullable:
                refused(lambda name=name: Model.from_values(valid(**{name: None})))
        for name in nullable:
            clean(Model.from_values(valid(**{name: None})))
        unknown = valid()
        unknown["unapproved"] = "secret-marker"
        refused(lambda: Model.from_values(unknown))
        cases.append("keys_exact_required_values_no_coercion_even_excluded")

        calls = []
        class Hostile(str):
            def __str__(self):
                calls.append("str")
                raise AssertionError("conversion interdite")
            def __repr__(self):
                calls.append("repr")
                raise AssertionError("repr interdite")
            def __bool__(self):
                calls.append("bool")
                raise AssertionError("bool interdit")
            def __eq__(self, other):
                calls.append("eq")
                raise AssertionError("comparaison interdite")
            def __hash__(self):
                calls.append("hash")
                raise AssertionError("hash interdit")
        class ForeignDict(dict):
            def copy(self):
                calls.append("copy")
                raise AssertionError("copy interdite")
        for name in fields:
            hostile = Hostile("secret-marker")
            refused(lambda name=name, hostile=hostile: Model.from_values(valid(**{name: hostile})))
            refused(lambda name=name, hostile=hostile: clean(Model(**valid(**{name: hostile})), exclude=[name]))
        refused(lambda: Model.from_values(ForeignDict(valid())))
        assert calls == []
        cases.append("foreign_hooks_never_called_no_echo")

        for name, enum in enums.items():
            assert [v for v, label in Model._meta.get_field(name).choices] == [v.value for v in enum]
            for item in enum:
                clean(Model.from_values(valid(**{name: item.value})))
                refused(lambda name=name, item=item: Model.from_values(valid(**{name: item})))
            refused(lambda name=name: clean(Model(**valid(**{name: "UNKNOWN"}))))
        for version in ("0.0.0", "1.2.3-rc.1+meta", "999.0.1"):
            clean(Model.from_values(valid(bulk_version=version)))
        for version in ("1.2", "01.2.3", "1.2.3-01", " 1.2.3"):
            refused(lambda version=version: clean(Model(**valid(bulk_version=version))))
        cases.append("canonical_strings_without_applicability_and_semver")

        with mock.patch.object(models.Model, "full_clean", side_effect=ValidationError("opaque-sensitive-input")):
            refused(lambda: clean(Model(**valid())))
        cases.append("orm_errors_static_without_echo")

        loader = MigrationLoader(None)
        migration = loader.disk_migrations[("backend", "0003_bulk_operation_record")]
        assert migration.dependencies == [("backend", "0002_job_record")]
        assert len(migration.operations) == 1
        operation = migration.operations[0]
        assert isinstance(operation, CreateModel)
        assert operation.name == "BulkOperationRecord"
        assert tuple(name for name, field in operation.fields) == fields
        assert len(operation.options["constraints"]) == 9
        for name, field in operation.fields:
            assert isinstance(field, models.TextField)
            assert not field.has_default()
            assert field.null == (name in nullable)
        expected_state = loader.project_state()
        actual_state = ProjectState.from_apps(apps)
        assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
        assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
        cases.append("migration_exact_create_model_and_no_drift")

        with mock.patch.object(Model, "full_clean", side_effect=AssertionError("validation implicite")), mock.patch.object(Model, "clean", side_effect=AssertionError("clean implicite")):
            _probe(lambda: Model(**valid()).save(), "db")
        assert counters == {"db": 1, "network": 0, "process": 0}, counters
        counters["db"] = 0
        cases.append("save_inherited_without_implicit_validation")
        assert counters == {"db": 0, "network": 0, "process": 0}, counters

    print("BULK_RECORD_OFFLINE_SAFE_OK")
    '''
).strip()


class BulkOperationRecordOfflineTests(unittest.TestCase):
    def test_model_factory_validation_migration_and_guards(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER + "\n")


if __name__ == "__main__":
    unittest.main()
