"""Persistance CommandIdempotencyV1 offline en processus frais sous gardes."""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "BULK_COMMAND_IDEMPOTENCY_OFFLINE_SAFE_OK"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

_CHILD = r'''
import socket
import subprocess
import sys
from contextlib import ExitStack
from unittest import mock

sys.path.insert(0, sys.argv[1])

import django
from django.apps import apps
from django.conf import settings

assert not settings.configured
assert not apps.ready

import psycopg
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

class GuardBlocked(Exception):
    def __init__(self, bucket):
        super().__init__("garde d effet interdit")
        self.bucket = bucket

counters = {"db": 0, "network": 0, "process": 0}

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
        stack.enter_context(mock.patch.object(target, name, side_effect=_make_guard(bucket)))

    def _probe(call, bucket):
        try:
            call()
        except GuardBlocked as err:
            assert err.bucket == bucket, err.bucket
            return
        raise AssertionError("garde non declenchee")

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

    from datetime import datetime, timezone, tzinfo
    from django.core.exceptions import ValidationError
    from django.db import models
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.loader import MigrationLoader
    from django.db.migrations.operations import CreateModel
    from django.db.migrations.state import ProjectState

    settings.configure(
        DEFAULT_CHARSET="utf-8",
        INSTALLED_APPS=["pixs.backend"],
        SECRET_KEY="unit-offline-synthetic-only",
        DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "bulk_command_offline_synthetic"}},
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    django.setup()

    from pixs.backend.bulk_command_idempotency_record import BulkCommandIdempotencyRecord as Model
    from pixs.backend.bulk_command_idempotency_record import _FIELDS
    import pixs.backend.bulk_command_idempotency_repository as repo_mod
    from pixs.backend.bulk_command_idempotency_repository import (
        BulkCommandIdempotencyConflict,
        BulkCommandIdempotencyRefused,
        BulkCommandIdempotencyRepository,
        BulkCommandIdempotencyStale,
    )
    import pixs.backend.bulk_command_idempotency_record as record_mod
    import pixs.backend.models as registered
    from pixs.backend.bulk_runtime_records import _INT64_MAX

    VALID_SHA = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    EXPIRES = datetime(2026, 5, 6, 7, 8, 9, 10, tzinfo=timezone.utc)

    def _valid(**over):
        base = {
            "tenant_id": "tenant-resolu",
            "subject_id": "sujet-resolu",
            "command_type": "commande.declaree",
            "idempotency_key": "cle-e",
            "content_sha256": VALID_SHA,
            "serializer_version": "1.2.3",
            "state": "IN_PROGRESS",
            "result_reference": None,
            "failure_code": None,
            "created_at": CREATED,
            "expires_at": EXPIRES,
            "revision": 1,
        }
        base.update(over)
        return base

    def _refused(call, code):
        try:
            call()
        except ValidationError as err:
            assert err.error_list, "sans liste"
            assert all(item.code == code for item in err.error_list), [i.code for i in err.error_list]
            joined = "\\n".join(err.messages)
            for secret in ("tenant-resolu", "sujet-resolu", "cle-e", VALID_SHA):
                assert secret not in joined
            return
        raise AssertionError("refus ValidationError absent")

    def _repo_refused(call):
        try:
            call()
        except BulkCommandIdempotencyRefused:
            return
        raise AssertionError("refus Refused absent")

    class Hostile:
        def __bool__(self):
            raise AssertionError("bool etranger")
        def __eq__(self, other):
            raise AssertionError("eq etranger")
        def __hash__(self):
            raise AssertionError("hash etranger")
        def __str__(self):
            raise AssertionError("str etranger")
        def __repr__(self):
            raise AssertionError("repr etranger")

    class BadDict(dict):
        def items(self):
            raise AssertionError("items etranger")

    class BadZone(tzinfo):
        def utcoffset(self, value):
            raise AssertionError("utcoffset etranger")

    class BadDatetime(datetime):
        pass

    assert record_mod.__all__ == ["BulkCommandIdempotencyRecord"]
    assert repo_mod.__all__ == ["BulkCommandIdempotencyConflict", "BulkCommandIdempotencyRefused", "BulkCommandIdempotencyRepository", "BulkCommandIdempotencyStale"]
    assert registered.__all__ == ["FeatureFlagSourceSnapshotRecord", "JobRecord"]
    assert tuple(_FIELDS) == ("tenant_id", "subject_id", "command_type", "idempotency_key", "content_sha256", "serializer_version", "state", "result_reference", "failure_code", "created_at", "expires_at", "revision")
    assert apps.get_model("backend", "BulkCommandIdempotencyRecord") is Model
    assert not Model.check(databases=[])
    assert Model._meta.pk.name == "id"
    assert len(Model._meta.local_fields) == 13
    assert Model.save is models.Model.save
    names = {c.name for c in Model._meta.constraints}
    assert names == {"bulkcommandidempotency_tenant_non_empty", "bulkcommandidempotency_subject_non_empty", "bulkcommandidempotency_type_non_empty", "bulkcommandidempotency_key_non_empty", "bulkcommandidempotency_digest_non_empty", "bulkcommandidempotency_serializer_non_empty", "bulkcommandidempotency_digest_regex", "bulkcommandidempotency_state_member", "bulkcommandidempotency_result_non_empty", "bulkcommandidempotency_failure_non_empty", "bulkcommandidempotency_revision_positive", "bulkcommandidempotency_key_unique"}

    row = Model.from_values(_valid())
    assert row._state.adding is True
    assert row.as_values() == _valid()
    assert row.as_values() is not row.as_values()
    row.full_clean(exclude=[], validate_unique=False, validate_constraints=False)
    assert _valid() == row.as_values()
    caller = _valid()
    row2 = Model.from_values(caller)
    caller["tenant_id"] = "mute"
    caller["revision"] = 999
    assert row2.tenant_id == "tenant-resolu"
    assert row2.revision == 1
    got = row.as_values()
    got["tenant_id"] = "mute"
    assert row.as_values()["tenant_id"] == "tenant-resolu"

    for key in _FIELDS:
        missing = _valid()
        del missing[key]
        _refused(lambda missing=missing: Model.from_values(missing), "bulk_command_idempotency_invalid")
        foreign = _valid()
        foreign[key] = Hostile()
        _refused(lambda foreign=foreign: Model.from_values(foreign), "bulk_command_idempotency_invalid")
        raw = Model(**_valid())
        raw.__dict__[key] = Hostile()
        _refused(lambda raw=raw, key=key: raw.full_clean(exclude=[key], validate_unique=False, validate_constraints=False), "bulk_command_idempotency_invalid")
    extra = _valid()
    extra["intrus"] = "x"
    _refused(lambda: Model.from_values(extra), "bulk_command_idempotency_invalid")
    _refused(lambda: Model.from_values(BadDict(_valid())), "bulk_command_idempotency_invalid")
    for bad in (None, 0, "x", [], Hostile()):
        _refused(lambda bad=bad: Model.from_values(bad), "bulk_command_idempotency_invalid")

    class S(str):
        pass
    for key, value in (("tenant_id", S("t")), ("state", S("IN_PROGRESS")), ("result_reference", S("r")), ("created_at", BadDatetime(2026, 1, 1, tzinfo=timezone.utc)), ("revision", True), ("revision", 1.0), ("revision", "1")):
        bad = _valid()
        bad[key] = value
        _refused(lambda bad=bad: Model.from_values(bad), "bulk_command_idempotency_invalid")

    for when in (datetime(1, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc), datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc)):
        for field in ("created_at", "expires_at"):
            assert Model.from_values(_valid(**{field: when}))._state.adding is True
    from datetime import timedelta
    other = timezone(timedelta(hours=1))
    for when in (datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=other), datetime(2026, 1, 1, tzinfo=BadZone())):
        for field in ("created_at", "expires_at"):
            _refused(lambda field=field, when=when: Model.from_values(_valid(**{field: when})), "bulk_command_idempotency_invalid")

    for bad_sha in ("", "0" * 63, "0" * 65, "G" * 64, "A" * 64):
        _refused(lambda bad_sha=bad_sha: Model.from_values(_valid(content_sha256=bad_sha)), "bulk_command_idempotency_invalid")
    for bad_state in ("", "in_progress", "SUCCEED", "PENDING"):
        _refused(lambda bad_state=bad_state: Model.from_values(_valid(state=bad_state)), "bulk_command_idempotency_invalid")
    for bad_rev in (0, -1):
        _refused(lambda bad_rev=bad_rev: Model.from_values(_valid(revision=bad_rev)), "bulk_command_idempotency_invalid")
    huge = _valid(revision=2**70)
    _refused(lambda: Model.from_values(huge), "bulk_command_idempotency_integer_capacity")
    big_row = Model(**_valid())
    big_row.__dict__["revision"] = 2**70
    _refused(lambda: big_row.as_values(), "bulk_command_idempotency_integer_capacity")
    _refused(lambda: big_row.full_clean(exclude=[], validate_unique=False, validate_constraints=False), "bulk_command_idempotency_integer_capacity")

    assert Model.from_values(_valid(created_at=EXPIRES, expires_at=CREATED))._state.adding is True
    assert Model.from_values(_valid(state="SUCCEEDED", result_reference="r-1", failure_code="f-1"))._state.adding is True
    assert Model.from_values(_valid(state="REJECTED", result_reference=None, failure_code=None))._state.adding is True

    try:
        BulkCommandIdempotencyRepository(using=Hostile())
    except ValidationError as err:
        assert err.error_list[0].code == "bulk_command_idempotency_alias_invalid"
    else:
        raise AssertionError("alias hostile accepte")
    for bad_alias in (None, "", 0, b"default"):
        try:
            BulkCommandIdempotencyRepository(using=bad_alias)
        except ValidationError as err:
            assert err.error_list[0].code == "bulk_command_idempotency_alias_invalid"
        else:
            raise AssertionError("alias invalide accepte")

    repo = BulkCommandIdempotencyRepository(using="default")
    assert repo._unit_var.get() is None
    _repo_refused(lambda: repo.get_entry(tenant_id=Hostile(), subject_id="s", command_type="c", idempotency_key="k"))
    _repo_refused(lambda: repo.get_entry(tenant_id="", subject_id="s", command_type="c", idempotency_key="k"))
    _repo_refused(lambda: repo.replay(tenant_id="t", subject_id="s", command_type="c", idempotency_key="k", content_sha256="bad", serializer_version="1.2.3"))
    _repo_refused(lambda: repo.replay(tenant_id="t", subject_id="s", command_type="c", idempotency_key="k", content_sha256=VALID_SHA, serializer_version="bad"))
    _repo_refused(lambda: repo.finalize_terminal(object(), expected_revision=1, state="SUCCEEDED", result_reference=None, failure_code=None))
    _repo_refused(lambda: repo.finalize_terminal(None, expected_revision=1, state="SUCCEEDED", result_reference=None, failure_code=None))
    repo2 = BulkCommandIdempotencyRepository(using="default")
    from pixs.backend.bulk_command_idempotency_values import capture_bulk_command_idempotency_values as _cap
    bound, diags = _cap(_valid())
    assert diags == [] and bound is not None
    token = repo_mod._IdempotentUnitToken(repo, bound, False)
    assert token.is_replay is False
    assert token.entry == _valid()
    assert token.entry is not token.entry
    _repo_refused(lambda: repo.finalize_terminal(token, expected_revision=1, state="SUCCEEDED", result_reference=None, failure_code=None))
    _repo_refused(lambda: repo2.finalize_terminal(token, expected_revision=1, state="SUCCEEDED", result_reference=None, failure_code=None))
    replay_token = repo_mod._IdempotentUnitToken(repo, bound, True)
    assert replay_token.is_replay is True
    assert replay_token.entry == _valid()
    entry = replay_token.entry
    entry["tenant_id"] = "mute"
    assert replay_token.entry["tenant_id"] == "tenant-resolu"
    try:
        with repo.idempotent_unit(values={"bad": 1}):
            raise AssertionError("unite invalide acceptee")
    except BulkCommandIdempotencyRefused:
        pass
    assert repo._unit_var.get() is None
    try:
        with repo.idempotent_unit(values=_valid(state="SUCCEEDED")):
            raise AssertionError("unite terminale acceptee")
    except BulkCommandIdempotencyRefused:
        pass
    assert repo._unit_var.get() is None

    loader = MigrationLoader(None)
    migration = loader.disk_migrations[("backend", "0006_bulk_command_idempotency")]
    assert migration.dependencies == [("backend", "0005_bulk_admission_identity")]
    assert len(migration.operations) == 1
    op = migration.operations[0]
    assert isinstance(op, CreateModel)
    assert op.name == "BulkCommandIdempotencyRecord"
    assert tuple(name for name, field in op.fields) == ("id",) + tuple(_FIELDS)
    assert len(op.options["constraints"]) == 12
    expected_state = loader.project_state()
    actual_state = ProjectState.from_apps(apps)
    assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
    assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
    assert counters == {"db": 0, "network": 0, "process": 0}, counters

print("BULK_COMMAND_IDEMPOTENCY_OFFLINE_SAFE_OK")
'''


class BulkCommandIdempotencyOfflineTests(unittest.TestCase):
    def test_offline_guards_and_persistence(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER + "\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
