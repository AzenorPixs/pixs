"""Persistance EventEnvelopeV1 offline en processus frais sous gardes."""

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / "src")
_MARKER = "BULK_EVENT_ENVELOPE_OFFLINE_SAFE_OK"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

_CHILD = r'''
import socket
import subprocess
import sys
from contextlib import ExitStack
from unittest import mock

sys.path.insert(0, sys.argv[1])

import json
import math
from datetime import datetime, timezone, tzinfo, timedelta
from types import MappingProxyType
from dataclasses import FrozenInstanceError

import django
from django.apps import apps
from django.conf import settings

assert not settings.configured
assert not apps.ready

import psycopg
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

import pixs.kernel.diagnostics as _diag_pre
import pixs.backend.bulk_event_envelope_values as _values_pre
import pixs.backend.bulk_execution_values as _exec_pre

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
        DATABASES={"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "bulk_envelope_offline_synthetic"}},
        LOGGING_CONFIG=None,
        MIDDLEWARE=(),
        USE_TZ=True,
    )
    assert "pixs.backend.bulk_event_envelope_record" not in sys.modules
    assert "pixs.backend.bulk_event_envelope_repository" not in sys.modules
    django.setup()

    from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord as Model
    from pixs.backend.bulk_event_envelope_record import _FIELDS
    import pixs.backend.bulk_event_envelope_record as record_mod
    import pixs.backend.bulk_event_envelope_repository as repo_mod
    from pixs.backend.bulk_event_envelope_repository import BulkEventEnvelopeRepository
    import pixs.backend.models as registered

    CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)

    def _valid(**over):
        base = {
            "event_id": "event-test", "kind": "DOMAIN", "event_type": "type-test",
            "event_version": "1.2.3", "producer_reference": "producer-test",
            "schema_reference": "schema-test", "order_scope_reference": "scope-test",
            "occurred_at": CREATED, "subject_reference": "subject-test",
            "tenant_context_reference": "tenant-test", "correlation_id": "correlation-test",
            "causation_id": None, "payload": {"name": "value"},
        }
        base.update(over)
        return base

    def _limits(**over):
        base = {"max_depth": 8, "max_members": 10, "non_tenant_authorized": False}
        base.update(over)
        return base

    def _refused(call, code):
        try:
            call()
        except ValidationError as err:
            assert err.error_list, "sans liste"
            assert all(item.code == code for item in err.error_list), [i.code for i in err.error_list]
            joined = chr(10).join(err.messages)
            for secret in ("event-test", "tenant-test", "correlation-test"):
                assert secret not in joined
            return
        raise AssertionError("refus ValidationError absent")

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

    assert record_mod.__all__ == ["BulkEventEnvelopeRecord"]
    assert repo_mod.__all__ == ["BulkEventEnvelopeDuplicate", "BulkEventEnvelopeRefused", "BulkEventEnvelopeRepository"]
    assert registered.__all__ == ["FeatureFlagSourceSnapshotRecord", "JobRecord"]
    EXPECTED_FIELDS = ("event_id", "kind", "event_type", "event_version", "producer_reference", "schema_reference", "order_scope_reference", "occurred_at", "subject_reference", "tenant_context_reference", "correlation_id", "causation_id", "payload")
    assert tuple(_FIELDS) == EXPECTED_FIELDS
    assert apps.get_model("backend", "BulkEventEnvelopeRecord") is Model
    assert not Model.check(databases=[])
    assert Model._meta.pk.name == "event_id"
    assert len(Model._meta.local_fields) == 13
    assert Model.save is not models.Model.save
    names = {c.name for c in Model._meta.constraints}
    assert names == {"bulkeventenvelope_event_non_empty", "bulkeventenvelope_kind_member", "bulkeventenvelope_type_non_empty", "bulkeventenvelope_version_non_empty", "bulkeventenvelope_producer_non_empty", "bulkeventenvelope_schema_non_empty", "bulkeventenvelope_scope_non_empty", "bulkeventenvelope_subject_non_empty", "bulkeventenvelope_tenant_non_empty", "bulkeventenvelope_correlation_non_empty", "bulkeventenvelope_causation_non_empty", "bulkeventenvelope_payload_non_empty"}
    fmap = {f.name: f for f in Model._meta.local_fields}
    assert type(fmap["event_id"]).__name__ == "TextField"
    assert type(fmap["payload"]).__name__ == "TextField"

    lim = _limits()
    row = Model.from_values(_valid(), **lim)
    assert row._state.adding is True
    assert type(row.payload) is str
    got = row.as_values(**lim)
    assert got == _valid()
    assert got is not row.as_values(**lim)
    assert got["payload"] == {"name": "value"} and got["payload"] is not row.as_values(**lim)["payload"]
    row.full_clean(exclude=[], validate_unique=False, validate_constraints=False, **lim)
    row.full_clean(exclude=["kind", "payload", "event_id"], validate_unique=True, validate_constraints=True, **lim)

    snap = row._locked_snapshot(**lim)
    assert type(snap.payload) is MappingProxyType
    assert snap.as_values() == _valid()
    assert snap.as_values()["payload"] is not snap.as_values()["payload"]
    frozen_list_row = Model.from_values(_valid(payload=[1, {"b": None}]), **lim)
    list_snapshot = frozen_list_row._locked_snapshot(**lim)
    assert type(list_snapshot.payload) is tuple
    assert type(list_snapshot.payload[1]) is MappingProxyType
    exported = list_snapshot.as_values()
    exported["payload"][1]["b"] = "changed"
    assert list_snapshot.as_values()["payload"] == [1, {"b": None}]
    try:
        snap.event_id = "changed"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("snapshot modifiable")
    try:
        snap.payload["name"] = "changed"
    except TypeError:
        pass
    else:
        raise AssertionError("payload snapshot modifiable")
    assert frozen_list_row.as_values(**lim)["payload"] == [1, {"b": None}]

    caller = _valid()
    row2 = Model.from_values(caller, **lim)
    caller["event_id"] = "mute"
    caller["payload"]["name"] = "mute"
    assert row2.event_id == "event-test"
    assert row2.as_values(**lim)["payload"] == {"name": "value"}

    for payload in (None, False, True, 0, -1, 0.0, -0.0, 1.25, "", "e", [], [None, True, 2, ""], {}, {"a": [1, {"b": None}]}):
        assert Model.from_values(_valid(payload=payload), **lim)._state.adding is True
    assert math.copysign(1.0, Model.from_values(_valid(payload=-0.0), **lim).as_values(**lim)["payload"]) == -1.0
    nulled = _valid(payload={"a" + chr(0) + "b": "x" + chr(0) + "y"})
    assert Model.from_values(nulled, **lim).as_values(**lim)["payload"] == {"a" + chr(0) + "b": "x" + chr(0) + "y"}
    uni = _valid(payload="e" + chr(0xE9) + chr(0x1F600))
    assert Model.from_values(uni, **lim).as_values(**lim)["payload"] == "e" + chr(0xE9) + chr(0x1F600)
    assert Model.from_values(_valid(payload=[[]]), max_depth=2, max_members=1, non_tenant_authorized=False)._state.adding is True
    _refused(lambda: Model.from_values(_valid(payload=[[]]), max_depth=1, max_members=1, non_tenant_authorized=False), "bulk_event_envelope_invalid")
    _refused(lambda: Model.from_values(_valid(payload={"a": 1, "b": 2}), max_depth=8, max_members=1, non_tenant_authorized=False), "bulk_event_envelope_invalid")
    cyc = []
    cyc.append(cyc)
    _refused(lambda: Model.from_values(_valid(payload=cyc), **lim), "bulk_event_envelope_invalid")

    big_ok = 10 ** 600
    assert Model.from_values(_valid(payload=big_ok), **lim)._state.adding is True
    assert Model.from_values(_valid(payload=big_ok), **lim).as_values(**lim)["payload"] == big_ok
    huge = 10 ** 700
    _refused(lambda: Model.from_values(_valid(payload=huge), **lim), "bulk_event_envelope_capacity_unsupported")
    _refused(lambda: Model.from_values(_valid(payload=float("nan")), **lim), "bulk_event_envelope_invalid")
    _refused(lambda: Model.from_values(_valid(payload=float("inf")), **lim), "bulk_event_envelope_invalid")

    for key in EXPECTED_FIELDS:
        missing = _valid()
        del missing[key]
        _refused(lambda missing=missing: Model.from_values(missing, **lim), "bulk_event_envelope_invalid")
        foreign = _valid()
        foreign[key] = Hostile()
        _refused(lambda foreign=foreign: Model.from_values(foreign, **lim), "bulk_event_envelope_invalid")
        raw = Model.from_values(_valid(), **lim)
        raw.__dict__[key] = Hostile()
        _refused(lambda raw=raw: raw.full_clean(exclude=[key], **lim), "bulk_event_envelope_invalid")
    extra = _valid()
    extra["intrus"] = "x"
    _refused(lambda: Model.from_values(extra, **lim), "bulk_event_envelope_invalid")
    _refused(lambda: Model.from_values(BadDict(_valid()), **lim), "bulk_event_envelope_invalid")
    for bad in (None, 0, "x", [], Hostile()):
        _refused(lambda bad=bad: Model.from_values(bad, **lim), "bulk_event_envelope_invalid")
    for field, bad in (("event_id", S("t")), ("kind", S("DOMAIN")), ("occurred_at", BadDatetime(2026, 1, 1, tzinfo=timezone.utc)), ("max_depth", True)):
        if field == "max_depth":
            _refused(lambda: Model.from_values(_valid(), max_depth=bad, max_members=10, non_tenant_authorized=False), "bulk_event_envelope_invalid")
        else:
            badv = _valid()
            badv[field] = bad
            _refused(lambda badv=badv: Model.from_values(badv, **lim), "bulk_event_envelope_invalid")
    for when in (datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=timezone(timedelta(hours=1))), datetime(2026, 1, 1, tzinfo=BadZone())):
        _refused(lambda when=when: Model.from_values(_valid(occurred_at=when), **lim), "bulk_event_envelope_invalid")
    for kwargs in ({"max_depth": 0}, {"max_depth": True}, {"max_members": 0}, {"non_tenant_authorized": 1}, {"non_tenant_authorized": None}):
        args = _limits()
        args.update(kwargs)
        _refused(lambda args=args: Model.from_values(_valid(), **args), "bulk_event_envelope_invalid")
    none_tenant = _valid(tenant_context_reference=None)
    _refused(lambda: Model.from_values(none_tenant, **lim), "bulk_event_envelope_invalid")
    assert Model.from_values(none_tenant, max_depth=8, max_members=10, non_tenant_authorized=True)._state.adding is True
    try:
        Model.from_values(_valid(), max_depth=8, max_members=10)
    except TypeError:
        pass
    else:
        raise AssertionError("limites requises sans defaut")
    try:
        BulkEventEnvelopeRepository(using=Hostile())
    except ValidationError as err:
        assert err.error_list[0].code == "bulk_event_envelope_alias_invalid"
    else:
        raise AssertionError("alias hostile accepte")
    for bad_alias in (None, "", 0, True, b"default", S("default")):
        try:
            BulkEventEnvelopeRepository(using=bad_alias)
        except ValidationError as err:
            assert err.error_list[0].code == "bulk_event_envelope_alias_invalid"
        else:
            raise AssertionError("alias invalide accepte")

    def _repository_refused(call):
        try:
            call()
        except repo_mod.BulkEventEnvelopeRefused as err:
            assert str(err) == "enveloppe evenement bulk refusee"
            return
        raise AssertionError("refus repository absent")

    repository = BulkEventEnvelopeRepository(using="default")
    for bad_id in (None, 0, True, "", S("event-test"), Hostile()):
        _repository_refused(lambda bad_id=bad_id: repository.get_envelope(event_id=bad_id, **lim))
    for bad_values in (None, BadDict(_valid()), Hostile()):
        _repository_refused(lambda bad_values=bad_values: repository.insert_envelope(values=bad_values, **lim))
    _repository_refused(lambda: repository.insert_envelope(values=_valid(), **lim))
    for wrong_limits in ({"max_depth": True}, {"max_members": Hostile()}, {"non_tenant_authorized": 1}):
        invalid_limits = _limits(**wrong_limits)
        _repository_refused(lambda invalid_limits=invalid_limits: repository.get_envelope(event_id="event-test", **invalid_limits))

    class BadList(list):
        def __iter__(self):
            raise AssertionError("iteration etrangere")

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

    _refused(lambda: Model.from_values(_valid(payload=BadList([1])), **lim), "bulk_event_envelope_invalid")
    _refused(lambda: Model.from_values(_valid(payload=[Hostile()]), **lim), "bulk_event_envelope_invalid")
    key = ArmedKey()
    foreign_payload = {key: 1}
    key.armed = True
    _refused(lambda: Model.from_values(_valid(payload=foreign_payload), **lim), "bulk_event_envelope_invalid")
    assert key.calls == 0
    key2 = ArmedKey()
    foreign_candidate = _valid()
    foreign_candidate[key2] = 1
    key2.armed = True
    _refused(lambda: Model.from_values(foreign_candidate, **lim), "bulk_event_envelope_invalid")
    assert key2.calls == 0

    good = Model.from_values(_valid(event_id="save-one"), **lim)
    for call in (lambda: good.save(), lambda: good.save("pos"), lambda: good.save(force_insert=True, using="default", update_fields=["kind"]), lambda: good.save(force_insert=True, force_update=True, using="default"), lambda: good.save(force_insert=False, using="default"), lambda: good.save(force_insert=True, using=""), lambda: good.save(force_insert=True, using=None)):
        _refused(call, "bulk_event_envelope_invalid")
    hydrated = Model.from_values(_valid(event_id="save-two"), **lim)
    hydrated._state.adding = False
    _refused(lambda: hydrated.save(force_insert=True, using="default"), "bulk_event_envelope_invalid")
    _refused(lambda: Model.from_values(_valid(), **lim).save(force_insert=True, using="default"), "bulk_event_envelope_invalid")

    tampered = Model.from_values(_valid(event_id="codec-one"), **lim)
    tampered.__dict__["payload"] = "{oops"
    _refused(lambda: tampered.as_values(**lim), "bulk_event_envelope_invalid")
    duped = Model.from_values(_valid(event_id="codec-two"), **lim)
    duped.__dict__["payload"] = '{"a": 1, "a": 2}'
    _refused(lambda: duped.as_values(**lim), "bulk_event_envelope_invalid")
    naned = Model.from_values(_valid(event_id="codec-three"), **lim)
    naned.__dict__["payload"] = "NaN"
    _refused(lambda: naned.as_values(**lim), "bulk_event_envelope_invalid")

    bare = Model(event_id="x")
    _refused(lambda: bare.as_values(**lim), "bulk_event_envelope_invalid")
    _refused(lambda: bare.full_clean(exclude=[], **lim), "bulk_event_envelope_invalid")
    _refused(lambda: bare.save(force_insert=True, using="default"), "bulk_event_envelope_invalid")

    loader = MigrationLoader(None)
    migration = loader.disk_migrations[("backend", "0007_bulk_event_envelope")]
    assert migration.dependencies == [("backend", "0006_bulk_command_idempotency")]
    assert len(migration.operations) == 1
    op = migration.operations[0]
    assert isinstance(op, CreateModel)
    assert op.name == "BulkEventEnvelopeRecord"
    assert tuple(name for name, field in op.fields) == ("event_id", "kind", "event_type", "event_version", "producer_reference", "schema_reference", "order_scope_reference", "occurred_at", "subject_reference", "tenant_context_reference", "correlation_id", "causation_id", "payload")
    assert len(op.options["constraints"]) == 12
    expected_state = loader.project_state()
    actual_state = ProjectState.from_apps(apps)
    assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
    assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
    assert counters == {"db": 0, "network": 0, "process": 0}, counters

print("BULK_EVENT_ENVELOPE_OFFLINE_SAFE_OK")
'''


class BulkEventEnvelopeOfflineTests(unittest.TestCase):
    def test_offline_guards_and_persistence(self):
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-X", "int_max_str_digits=640", "-c", _CHILD, _SRC],
            cwd=str(_ROOT), env=_ENV, capture_output=True, text=True,
            timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER + chr(10))
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
