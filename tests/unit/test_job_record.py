"""Unités offline de JobRecord : modèle, validateurs et migration, en processus enfant isolé."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "JOB_RECORD_OFFLINE_SAFE_OK"
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

    _MARKER = "JOB_RECORD_OFFLINE_SAFE_OK"

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
        from django.db.migrations.state import ModelState, ProjectState

        settings.configure(
            DEFAULT_CHARSET="utf-8",
            INSTALLED_APPS=["pixs.backend"],
            SECRET_KEY="unit-offline-synthetic-only",
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "job_record_offline_synthetic"}},
            LOGGING_CONFIG=None,
            MIDDLEWARE=(),
            USE_TZ=True,
        )
        django.setup()

        import inspect

        import pixs.backend.models as msrc
        from pixs.backend.models import (
            FeatureFlagSourceSnapshotRecord,
            JobRecord,
            _validate_job_version,
        )
        from pixs.kernel.jobs import JobState

        cases = []

        def case(name, fn, delta=None):
            before = dict(counters)
            fn()
            expected = {
                k: before[k] + ((delta or {}).get(k, 0)) for k in counters
            }
            assert counters == expected, (name, counters, before, delta)
            if delta:
                for k, v in delta.items():
                    blocked[k] += v
                for k in counters:
                    counters[k] = before[k]
            cases.append(name)

        FIXED = "version de travail SemVer complète attendue"

        def valid_kwargs(**over):
            data = dict(
                job_id="j-1",
                job_type="notify.send",
                job_version="1.2.3",
                payload={},
                subject={},
                tenant_context={},
                correlation_id="corr-1",
                causation_id="cause-1",
                perimeter_reference="perim-1",
                state="PENDING",
                attempt_count=0,
            )
            data.update(over)
            return data

        def c_fields():
            names = [f.name for f in JobRecord._meta.get_fields()]
            assert names == [
                "job_id", "job_type", "job_version", "payload", "subject",
                "tenant_context", "correlation_id", "causation_id",
                "perimeter_reference", "state", "attempt_count",
                "lease_owner", "lease_expires_at",
            ], names

        def c_exports():
            assert msrc.__all__ == ["FeatureFlagSourceSnapshotRecord", "JobRecord"]

        def c_ff_intact():
            source = inspect.getsource(FeatureFlagSourceSnapshotRecord)
            assert source.splitlines() == [
                "class FeatureFlagSourceSnapshotRecord(models.Model):",
                '    """Versionne le document canonique d’un snapshot de fanions."""',
                "",
                "    configuration_version = models.TextField(primary_key=True)",
                "    snapshot = models.JSONField()",
            ], source

        def c_meta():
            state = JobRecord._meta.get_field("state")
            assert [v for v, _ in state.choices] == [s.value for s in JobState]
            assert state.has_default() is False
            attempt = JobRecord._meta.get_field("attempt_count")
            assert attempt.has_default() is True and attempt.get_default() == 0
            for fname in ("payload", "subject", "tenant_context"):
                f = JobRecord._meta.get_field(fname)
                assert f.blank is True and f.null is False, fname
            for fname in ("lease_owner", "lease_expires_at"):
                f = JobRecord._meta.get_field(fname)
                assert f.null is True and f.blank is True, fname
            assert JobRecord._meta.db_table == "backend_jobrecord"
            assert JobRecord._meta.pk.name == "job_id"
            assert sorted(c.name for c in JobRecord._meta.constraints) == sorted([
                "jobrecord_job_id_non_empty", "jobrecord_job_type_non_empty",
                "jobrecord_job_version_non_empty",
                "jobrecord_correlation_id_non_empty",
                "jobrecord_causation_id_non_empty",
                "jobrecord_perimeter_reference_non_empty",
                "jobrecord_state_in_jobstate",
                "jobrecord_attempt_count_non_negative",
            ])

        def c_json_containers():
            JobRecord(
                **valid_kwargs(payload={}, subject=[], tenant_context={})
            ).clean_fields()
            JobRecord(
                **valid_kwargs(lease_owner=None, lease_expires_at=None)
            ).clean_fields()

        def c_json_none_documented():
            # Limite documentée : blank=True accepte None au Python ; le
            # NOT NULL SQL est prouvé seulement par la suite PG réelle.
            JobRecord(**valid_kwargs(payload=None)).clean_fields()

        def c_version_ok():
            for value in ("1.2.3", "2.0.0-rc.1"):
                _validate_job_version(value)
                JobRecord(**valid_kwargs(job_version=value)).clean_fields()

        def c_version_bad():
            for bad in (None, 1, ["1.2.3"], "", "01.2.3", "1.2", object()):
                try:
                    _validate_job_version(bad)
                except ValidationError as error:
                    assert error.messages == [FIXED], error.messages
                else:
                    raise AssertionError("version invalide acceptée")

        def c_version_hostile_no_probe():
            calls = {"bool": 0, "repr": 0, "str": 0}

            class Hostile(str):
                def __bool__(self):
                    calls["bool"] += 1
                    return True

                def __repr__(self):
                    calls["repr"] += 1
                    return "hostile"

                def __str__(self):
                    calls["str"] += 1
                    return "hostile"

            try:
                _validate_job_version(Hostile("1.2.3"))
            except ValidationError as error:
                assert error.messages == [FIXED]
            else:
                raise AssertionError("sous-classe acceptée")
            assert calls == {"bool": 0, "repr": 0, "str": 0}, calls

        def c_refs_empty():
            for fname in ("job_id", "job_type", "job_version", "correlation_id",
                          "causation_id", "perimeter_reference"):
                try:
                    JobRecord(**valid_kwargs(**{fname: ""})).clean_fields()
                except ValidationError:
                    continue
                raise AssertionError(fname)

        def c_attempt_negative():
            try:
                JobRecord(**valid_kwargs(attempt_count=-1)).clean_fields()
            except ValidationError:
                return
            raise AssertionError("attempt_count négatif accepté")

        def c_states():
            for value in [s.value for s in JobState]:
                JobRecord(**valid_kwargs(state=value)).clean_fields()
            for bad_state in ("BOGUS", ""):
                try:
                    JobRecord(**valid_kwargs(state=bad_state)).clean_fields()
                except ValidationError:
                    continue
                raise AssertionError(bad_state)

        def c_full_clean_offline():
            JobRecord(**valid_kwargs()).full_clean(
                validate_unique=False, validate_constraints=False
            )

        def c_save_probe():
            bad = JobRecord(**valid_kwargs(state="BOGUS", job_type="", job_id=""))
            clean_probe = mock.Mock()
            full_clean_probe = mock.Mock()
            with mock.patch.object(bad, "clean", clean_probe), \
                 mock.patch.object(bad, "full_clean", full_clean_probe):
                try:
                    bad.save()
                except GuardBlocked as error:
                    assert error.bucket == "db", error.bucket
                else:
                    raise AssertionError("save a réussi malgré la garde")
            assert clean_probe.call_count == 0
            assert full_clean_probe.call_count == 0

        def c_migration_offline():
            loader = MigrationLoader(connection=None, ignore_no_migrations=True)
            key = ("backend", "0002_job_record")
            assert key in loader.disk_migrations, list(loader.disk_migrations)
            mig = loader.disk_migrations[key]
            assert mig.dependencies == [
                ("backend", "0001_feature_flag_source_snapshot")
            ]
            assert len(mig.operations) == 1
            op = mig.operations[0]
            assert isinstance(op, CreateModel) and op.name == "JobRecord"
            assert op.reversible is True
            assert [name for name, _field in op.fields] == [
                f.name for f in JobRecord._meta.get_fields()
            ]
            assert sorted(c.name for c in op.options["constraints"]) == sorted(
                c.name for c in JobRecord._meta.constraints
            )
            assert ("backend", "0001_feature_flag_source_snapshot") in \
                loader.graph.forwards_plan(key)
            from_state = loader.project_state()
            live_state = ProjectState()
            for model in apps.get_models():
                live_state.add_model(ModelState.from_model(model))
            assert MigrationAutodetector(
                from_state, live_state
            ).changes(graph=loader.graph) == {}
            assert MigrationAutodetector(
                live_state, from_state
            ).changes(graph=loader.graph) == {}

        for name, fn in [
            ("fields13", c_fields),
            ("exports", c_exports),
            ("ff_intact", c_ff_intact),
            ("meta", c_meta),
            ("json_containers", c_json_containers),
            ("json_none_documented", c_json_none_documented),
            ("version_ok", c_version_ok),
            ("version_bad", c_version_bad),
            ("version_hostile", c_version_hostile_no_probe),
            ("refs_empty", c_refs_empty),
            ("attempt_negative", c_attempt_negative),
            ("states9", c_states),
            ("full_clean_offline", c_full_clean_offline),
            ("migration_offline", c_migration_offline),
        ]:
            case(name, fn)
        case("save_probe", c_save_probe, delta={"db": 1})
        assert connection.connection is None
        assert counters == {"db": 0, "network": 0, "process": 0}, counters
        assert blocked == {"db": 1, "network": 0, "process": 0}, blocked

        print(
            f"{_MARKER} cases={len(cases)} guards_validation={counters} "
            f"blocked_save={blocked}",
            flush=True,
        )
    '''
)


class JobRecordOfflineTests(unittest.TestCase):
    def test_enfant_offline_sous_gardes(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC],
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=180,
        )
        self.assertEqual(result.returncode, 0, result.stderr[-400:])
        self.assertRegex(
            result.stdout,
            "^JOB_RECORD_OFFLINE_SAFE_OK cases=[1-9][0-9]* "
            "guards_validation=\\{'db': 0, 'network': 0, 'process': 0\\} "
            "blocked_save=\\{'db': 1, 'network': 0, 'process': 0\\}\n$",
        )


if __name__ == "__main__":
    unittest.main()
