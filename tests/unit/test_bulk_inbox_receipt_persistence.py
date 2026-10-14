"""Persistance InboxReceiptV1 offline en processus frais sous gardes."""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "BULK_INBOX_RECEIPT_OFFLINE_SAFE_OK"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

_CHILD = r'''
import socket
import subprocess
import sys
from contextlib import ExitStack
from unittest import mock

sys.path.insert(0, sys.argv[1])

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone, tzinfo

import django
from django.apps import apps
from django.conf import settings

assert not settings.configured
assert not apps.ready

import psycopg
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

import pixs.backend.bulk_inbox_receipt_values as _values_pre
import pixs.backend.bulk_execution_values as _exec_pre
import pixs.kernel.diagnostics as _diag_pre

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
        DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "bulk_inbox_offline_synthetic"}},
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    assert "pixs.backend.bulk_inbox_receipt_record" not in sys.modules
    assert "pixs.backend.bulk_inbox_receipt_repository" not in sys.modules
    assert "pixs.backend.models" not in sys.modules
    django.setup()

    from pixs.backend.bulk_inbox_receipt_record import BulkInboxReceiptRecord as Model
    from pixs.backend.bulk_inbox_receipt_record import _FIELDS
    import pixs.backend.bulk_inbox_receipt_record as record_mod
    import pixs.backend.bulk_inbox_receipt_repository as repo_mod
    from pixs.backend.bulk_inbox_receipt_repository import BulkInboxReceiptDivergence
    from pixs.backend.bulk_inbox_receipt_repository import BulkInboxReceiptDuplicate
    from pixs.backend.bulk_inbox_receipt_repository import BulkInboxReceiptRefused
    from pixs.backend.bulk_inbox_receipt_repository import BulkInboxReceiptRepository
    from pixs.backend.bulk_inbox_receipt_values import capture_bulk_inbox_receipt_values
    import pixs.backend.models as registered

    CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    SHA_OK = "0f" * 32
    EXPECTED = ("consumer_reference", "event_id", "event_version", "content_sha256", "state", "consumed_at", "correlation_id", "causation_id")

    def _valid(**over):
        base = {
            "consumer_reference": "consumer-test",
            "event_id": "event-test",
            "event_version": "1.2.3",
            "content_sha256": SHA_OK,
            "state": "CONSUMED",
            "consumed_at": CREATED,
            "correlation_id": "correlation-test",
            "causation_id": None,
        }
        base.update(over)
        return base

    def _refused(call, code):
        try:
            call()
        except ValidationError as err:
            assert err.error_list, "sans liste"
            assert all(item.code == code for item in err.error_list), [i.code for i in err.error_list]
            joined = chr(10).join(err.messages)
            for secret in ("consumer-test", "event-test", "correlation-test"):
                assert secret not in joined
            return
        raise AssertionError("refus ValidationError absent")

    def _repo_refused(call):
        try:
            call()
        except BulkInboxReceiptRefused as err:
            assert str(err) == "accuse reception bulk refuse"
            return
        raise AssertionError("refus repository absent")

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

    class S(str):
        pass

    class HostileMeta(type):
        def __eq__(cls, other):
            raise AssertionError("eq metaclasse")
        def __hash__(cls):
            raise AssertionError("hash metaclasse")

    class HostileValue(metaclass=HostileMeta):
        pass

    class ArmedKey:
        armed = False
        calls = 0
        def __hash__(self):
            if self.armed:
                self.calls += 1
                raise AssertionError("hash etranger")
            return object.__hash__(self)
        def __eq__(self, other):
            raise AssertionError("eq etranger")
        def __repr__(self):
            raise AssertionError("repr etranger")

    assert record_mod.__all__ == ["BulkInboxReceiptRecord"]
    assert repo_mod.__all__ == ["BulkInboxReceiptDivergence", "BulkInboxReceiptDuplicate", "BulkInboxReceiptRefused", "BulkInboxReceiptRepository"]
    assert registered.__all__ == ["FeatureFlagSourceSnapshotRecord", "JobRecord"]
    assert tuple(_FIELDS) == EXPECTED
    assert apps.get_model("backend", "BulkInboxReceiptRecord") is Model
    assert not Model.check(databases=[])
    assert Model._meta.pk.name == "id"
    assert len(Model._meta.local_fields) == 9
    assert Model.save is not models.Model.save
    names = {c.name for c in Model._meta.constraints}
    assert names == {"bulkinboxreceipt_consumer_non_empty", "bulkinboxreceipt_event_non_empty", "bulkinboxreceipt_version_non_empty", "bulkinboxreceipt_digest_non_empty", "bulkinboxreceipt_digest_regex", "bulkinboxreceipt_state_member", "bulkinboxreceipt_correlation_non_empty", "bulkinboxreceipt_causation_non_empty", "bulkinboxreceipt_consumer_event_unique"}
    fmap = {f.name: f for f in Model._meta.local_fields}
    assert type(fmap["id"]).__name__ == "BigAutoField"
    assert type(fmap["consumed_at"]).__name__ == "_TrustedUtcDateTimeField"
    assert type(fmap["consumer_reference"]).__name__ == "TextField"

    row = Model.from_values(_valid())
    assert row._state.adding is True
    got = row.as_values()
    assert got == _valid()
    assert got is not row.as_values()
    caller = _valid(causation_id="cause-test")
    row2 = Model.from_values(caller)
    caller["event_id"] = "mute"
    assert row2.event_id == "event-test"
    exported = row.as_values()
    exported["event_id"] = "mute"
    assert row.as_values()["event_id"] == "event-test"
    row.full_clean(exclude=[], validate_unique=False, validate_constraints=False)
    row.full_clean(exclude=["consumer_reference", "event_id", "event_version", "content_sha256", "state", "consumed_at", "correlation_id", "causation_id"], validate_unique=True, validate_constraints=True)
    bound, diags = capture_bulk_inbox_receipt_values(_valid())
    assert diags == [] and bound is not None
    assert bound.consumer_reference == "consumer-test"
    assert type(bound.consumed_at) is datetime
    assert bound.causation_id is None
    assert not hasattr(bound, "as_values")
    try:
        bound.state = "X"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("bound modifiable")
    assert bound.__slots__ is not None

    for key in EXPECTED:
        missing = _valid()
        del missing[key]
        _refused(lambda missing=missing: Model.from_values(missing), "bulk_inbox_receipt_invalid")
        foreign = _valid()
        foreign[key] = Hostile()
        _refused(lambda foreign=foreign: Model.from_values(foreign), "bulk_inbox_receipt_invalid")
        meta = _valid()
        meta[key] = HostileValue()
        _refused(lambda meta=meta: Model.from_values(meta), "bulk_inbox_receipt_invalid")
        raw = Model(**_valid())
        raw.__dict__[key] = Hostile()
        _refused(lambda raw=raw: raw.full_clean(exclude=[key]), "bulk_inbox_receipt_invalid")
    extra = _valid()
    extra["intrus"] = "x"
    _refused(lambda: Model.from_values(extra), "bulk_inbox_receipt_invalid")
    _refused(lambda: Model.from_values(BadDict(_valid())), "bulk_inbox_receipt_invalid")
    for bad in (None, 0, "x", [], Hostile()):
        _refused(lambda bad=bad: Model.from_values(bad), "bulk_inbox_receipt_invalid")
    key = ArmedKey()
    armed_candidate = {key: 1}
    key.armed = True
    _refused(lambda: Model.from_values(armed_candidate), "bulk_inbox_receipt_invalid")
    assert key.calls == 0
    for field, bad in (("consumer_reference", S("t")), ("event_id", S("e")), ("state", S("CONSUMED")), ("consumed_at", BadDatetime(2026, 1, 1, tzinfo=timezone.utc))):
        badv = _valid()
        badv[field] = bad
        _refused(lambda badv=badv: Model.from_values(badv), "bulk_inbox_receipt_invalid")
    for when in (datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=timezone(timedelta(hours=1))), datetime(2026, 1, 1, tzinfo=BadZone())):
        _refused(lambda when=when: Model.from_values(_valid(consumed_at=when)), "bulk_inbox_receipt_invalid")
    zoned = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(0), "UTC-etranger"))
    assert zoned.tzinfo is not timezone.utc
    _refused(lambda: Model.from_values(_valid(consumed_at=zoned)), "bulk_inbox_receipt_invalid")
    for bad in ("", "ABCDEF" * 11, "0f" * 31, "0f" * 32 + "0", "zz" * 32, "0F" * 32):
        _refused(lambda bad=bad: Model.from_values(_valid(content_sha256=bad)), "bulk_inbox_receipt_invalid")
    for bad in ("", "1.2", "v1.2.3", "1.2.3.4", "a.b.c"):
        _refused(lambda bad=bad: Model.from_values(_valid(event_version=bad)), "bulk_inbox_receipt_invalid")
    for bad in ("PENDING", "consumed", "", "CONSUMED "):
        _refused(lambda bad=bad: Model.from_values(_valid(state=bad)), "bulk_inbox_receipt_invalid")
    nul = chr(0)
    for field in ("consumer_reference", "event_id", "correlation_id", "causation_id"):
        _refused(lambda field=field: Model.from_values(_valid(**{field: "a" + nul + "b"})), "bulk_inbox_receipt_invalid")
        _refused(lambda field=field: Model.from_values(_valid(**{field: ""})), "bulk_inbox_receipt_invalid")
    _refused(lambda: Model.from_values(_valid(consumer_reference="surrogate" + chr(0xD800))), "bulk_inbox_receipt_invalid")
    assert Model.from_values(_valid(causation_id=None))._state.adding is True
    assert Model.from_values(_valid(causation_id="cause-test"))._state.adding is True
    assert Model.from_values(_valid(consumer_reference="reference-" + chr(0xE9))).as_values()["consumer_reference"] == "reference-" + chr(0xE9)

    try:
        BulkInboxReceiptRepository(using=Hostile())
    except ValidationError as err:
        assert err.error_list[0].code == "bulk_inbox_receipt_alias_invalid"
    else:
        raise AssertionError("alias hostile accepte")
    for bad_alias in (None, "", 0, True, b"default", S("default")):
        try:
            BulkInboxReceiptRepository(using=bad_alias)
        except ValidationError as err:
            assert err.error_list[0].code == "bulk_inbox_receipt_alias_invalid"
        else:
            raise AssertionError("alias invalide accepte")
    repository = BulkInboxReceiptRepository(using="default")
    for bad_key in (None, 0, True, "", S("event-test"), Hostile()):
        _repo_refused(lambda bad_key=bad_key: repository.get_receipt(consumer_reference=bad_key, event_id="event-test"))
        _repo_refused(lambda bad_key=bad_key: repository.get_receipt(consumer_reference="consumer-test", event_id=bad_key))
    for bad_values in (None, BadDict(_valid()), Hostile()):
        _repo_refused(lambda bad_values=bad_values: repository.insert_receipt(values=bad_values))
    _repo_refused(lambda: repository.insert_receipt(values=_valid()))

    good = Model.from_values(_valid(event_id="save-one"))
    for call in (lambda: good.save(), lambda: good.save("pos"), lambda: good.save(force_insert=True, using="default", update_fields=["state"]), lambda: good.save(force_insert=True, force_update=True, using="default"), lambda: good.save(force_insert=False, using="default"), lambda: good.save(force_insert=True, using=""), lambda: good.save(force_insert=True, using=None)):
        _refused(call, "bulk_inbox_receipt_invalid")
    hydrated = Model.from_values(_valid(event_id="save-two"))
    hydrated._state.adding = False
    _refused(lambda: hydrated.save(force_insert=True, using="default"), "bulk_inbox_receipt_invalid")
    _refused(lambda: Model.from_values(_valid()).save(force_insert=True, using="default"), "bulk_inbox_receipt_invalid")
    deferred = Model.from_values(_valid())
    del deferred.__dict__["event_id"]
    _refused(lambda: deferred.as_values(), "bulk_inbox_receipt_invalid")
    _refused(lambda: deferred.full_clean(exclude=["event_id"]), "bulk_inbox_receipt_invalid")
    _refused(lambda: deferred.save(force_insert=True, using="default"), "bulk_inbox_receipt_invalid")
    bare = Model(consumer_reference="x")
    _refused(lambda: bare.as_values(), "bulk_inbox_receipt_invalid")
    _refused(lambda: bare.full_clean(exclude=[]), "bulk_inbox_receipt_invalid")
    _refused(lambda: bare.save(force_insert=True, using="default"), "bulk_inbox_receipt_invalid")

    loader = MigrationLoader(None)
    migration = loader.disk_migrations[("backend", "0008_bulk_inbox_receipt")]
    assert migration.dependencies == [("backend", "0007_bulk_event_envelope")]
    assert len(migration.operations) == 1
    op = migration.operations[0]
    assert isinstance(op, CreateModel)
    assert op.name == "BulkInboxReceiptRecord"
    assert tuple(name for name, field in op.fields) == ("id", "consumer_reference", "event_id", "event_version", "content_sha256", "state", "consumed_at", "correlation_id", "causation_id")
    assert len(op.options["constraints"]) == 9
    expected_state = loader.project_state()
    actual_state = ProjectState.from_apps(apps)
    assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
    assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
    assert counters == {"db": 0, "network": 0, "process": 0}, counters

print("BULK_INBOX_RECEIPT_OFFLINE_SAFE_OK")
'''


class BulkInboxReceiptOfflineTests(unittest.TestCase):
    def test_offline_guards_and_persistence(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", _CHILD, _SRC],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER + chr(10))
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
