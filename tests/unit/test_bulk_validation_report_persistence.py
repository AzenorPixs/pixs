'''Persistance ValidationReportV1 offline en processus frais sous gardes.'''

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / 'src')
_MARKER = 'BULK_VALIDATION_REPORT_OFFLINE_SAFE_OK'
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONDONTWRITEBYTECODE': '1'}

_CHILD = r"""
import socket
import subprocess
import sys
from contextlib import ExitStack
from unittest import mock

sys.path.insert(0, sys.argv[1])

import sys as _sys
from dataclasses import FrozenInstanceError

import django
from django.apps import apps
from django.conf import settings

assert not settings.configured
assert not apps.ready

import psycopg
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper

import pixs.kernel.diagnostics as _diag_pre
import pixs.backend.bulk_execution_values as _exec_pre
import pixs.backend.bulk_validation_report_values as _values_pre

class GuardBlocked(Exception):
    def __init__(self, bucket):
        super().__init__('garde effet interdit')
        self.bucket = bucket

counters = {'db': 0, 'network': 0, 'process': 0}

def _make_guard(bucket):
    def _blocked(*args, **kwargs):
        counters[bucket] += 1
        raise GuardBlocked(bucket)
    return _blocked

guard_targets = [
    (PGWrapper, 'get_new_connection', 'db'),
    (psycopg, 'connect', 'db'),
    (psycopg.Connection, 'connect', 'db'),
    (socket.socket, 'connect', 'network'),
    (socket, 'create_connection', 'network'),
    (subprocess, 'Popen', 'process'),
    (subprocess, 'run', 'process'),
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
        raise AssertionError('garde non declenchee')
    _probe(lambda: PGWrapper.get_new_connection(object(), {}), 'db')
    _probe(lambda: psycopg.connect(), 'db')
    _probe(lambda: psycopg.Connection.connect(), 'db')
    _probe(lambda: socket.socket.connect(object(), ('127.0.0.1', 0)), 'network')
    _probe(lambda: socket.create_connection(('127.0.0.1', 0)), 'network')
    _probe(lambda: subprocess.Popen(['true']), 'process')
    _probe(lambda: subprocess.run(['true']), 'process')
    assert counters == {'db': 3, 'network': 2, 'process': 2}, counters
    for key in counters:
        counters[key] = 0
    from django.core.exceptions import ValidationError
    from django.db import models
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.loader import MigrationLoader
    from django.db.migrations.operations import CreateModel
    from django.db.migrations.state import ProjectState
    settings.configure(DEFAULT_CHARSET='utf-8', INSTALLED_APPS=['pixs.backend'], SECRET_KEY='unit-offline-synthetic-only', DATABASES={'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'bulk_report_offline_synthetic'}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    assert 'pixs.backend.bulk_validation_report_record' not in sys.modules
    assert 'pixs.backend.bulk_validation_report_repository' not in sys.modules
    assert 'pixs.backend.models' not in sys.modules
    django.setup()
    from pixs.backend.bulk_validation_report_record import BulkValidationReportRecord as Model
    from pixs.backend.bulk_validation_report_record import _FIELDS
    from pixs.backend.bulk_validation_report_record import _ReportSnapshot
    from pixs.backend.bulk_validation_report_record import _capture_context
    import pixs.backend.bulk_validation_report_record as record_mod
    import pixs.backend.bulk_validation_report_repository as repo_mod
    from pixs.backend.bulk_validation_report_repository import BulkValidationReportRefused
    from pixs.backend.bulk_validation_report_repository import BulkValidationReportRepository
    import pixs.backend.bulk_validation_report_values as values_mod
    import pixs.backend.models as registered
    assert _sys.get_int_max_str_digits() == 640
    def _policy(**over):
        base = {'max_input_bytes': 1048576, 'max_rows': 1000000, 'max_row_bytes': 8192, 'max_columns': 64, 'max_json_depth': 8, 'max_json_members': 32, 'max_diagnostics': 10, 'read_chunk_bytes': 4096, 'chunk_rows': 500, 'max_attempts': 3, 'lease_seconds': 60, 'renewal_seconds': 20, 'publish_max_attempts': 1, 'publish_lease_seconds': 50, 'publish_renewal_seconds': 20, 'max_parallel_operations': 2, 'max_runtime_seconds': 3600, 'replay_window_seconds': 300, 'idempotency_retention_seconds': 600, 'staging_retention_seconds': 900, 'result_retention_seconds': 1200, 'max_download_url_seconds': 60, 'retry_delays_seconds': [1, 2], 'publish_retry_delays_seconds': []}
        base.update(over)
        return base
    def _progress(**over):
        base = {'total_rows': None, 'validated_rows': 2, 'invalid_rows': 1, 'applied_rows': 0, 'execution_rejected_rows': 0, 'exported_rows': 0}
        base.update(over)
        return base
    def _row(**over):
        base = {'code': 'INVALID_FIELD', 'field_reference': 'name', 'line_index': 1}
        base.update(over)
        return base
    def _report(**over):
        base = {'report_version': '1.0.0', 'operation_id': 'op-test', 'mode': 'VALIDATE_ONLY', 'progress': _progress(), 'diagnostics': (_row(),), 'complete': True, 'source_version': None, 'mapping_version': '1.2.3'}
        base.update(over)
        return base
    def _ctx(**over):
        base = {'policy': _policy(), 'declared_codes': ('INVALID_FIELD',), 'declared_fields': ('name',)}
        base.update(over)
        return base
    def _refused(call, code):
        try:
            call()
        except ValidationError as err:
            assert err.error_list, 'sans liste'
            assert all(item.code == code for item in err.error_list), [i.code for i in err.error_list]
            joined = chr(10).join(err.messages)
            for secret in ('op-test', 'LEAK-MARKER', 'mute'):
                assert secret not in joined
            return
        raise AssertionError('refus ValidationError absent')
    def _repo_refused(call):
        try:
            call()
        except BulkValidationReportRefused as err:
            assert str(err) == 'rapport de validation bulk refuse'
            return
        raise AssertionError('refus repository absent')
    class Hostile:
        def __bool__(self):
            raise AssertionError('bool etranger')
        def __eq__(self, other):
            raise AssertionError('eq etranger')
        def __hash__(self):
            raise AssertionError('hash etranger')
        def __str__(self):
            raise AssertionError('str etranger')
        def __repr__(self):
            raise AssertionError('repr etranger')
    class BadDict(dict):
        def items(self):
            raise AssertionError('items etranger')
    class S(str):
        pass
    class HostileMeta(type):
        def __eq__(cls, other):
            raise AssertionError('eq metaclasse')
        def __hash__(cls):
            raise AssertionError('hash metaclasse')
    class HostileValue(metaclass=HostileMeta):
        pass
    class ForeignTuple(tuple):
        def __len__(self):
            raise AssertionError('len etranger')
        def __iter__(self):
            raise AssertionError('iter etranger')
    class ArmedKey:
        armed = False
        calls = 0
        def __hash__(self):
            if self.armed:
                self.calls += 1
                raise AssertionError('hash etranger')
            return object.__hash__(self)
        def __eq__(self, other):
            raise AssertionError('eq etranger')
        def __repr__(self):
            raise AssertionError('repr etranger')
    assert record_mod.__all__ == ['BulkValidationReportRecord']
    assert repo_mod.__all__ == ['BulkValidationReportRefused', 'BulkValidationReportRepository']
    assert registered.__all__ == ['FeatureFlagSourceSnapshotRecord', 'JobRecord']
    assert tuple(_FIELDS) == ('report_version', 'operation_id', 'mode', 'progress', 'diagnostics', 'complete', 'source_version', 'mapping_version')
    assert apps.get_model('backend', 'BulkValidationReportRecord') is Model
    assert not Model.check(databases=[])
    assert Model._meta.pk.name == 'id'
    assert len(Model._meta.local_fields) == 9
    assert Model.save is not models.Model.save
    names = {c.name for c in Model._meta.constraints}
    assert names == {'bulkvalidationreport_version_exact', 'bulkvalidationreport_operation_non_empty', 'bulkvalidationreport_mode_member', 'bulkvalidationreport_progress_non_empty', 'bulkvalidationreport_diagnostics_non_empty', 'bulkvalidationreport_mapping_non_empty', 'bulkvalidationreport_source_non_empty'}
    fmap = {f.name: f for f in Model._meta.local_fields}
    assert type(fmap['id']).__name__ == 'BigAutoField'
    assert type(fmap['progress']).__name__ == 'TextField'
    assert type(fmap['diagnostics']).__name__ == 'TextField'
    assert type(fmap['complete']).__name__ == 'BooleanField'
    assert 'DateTimeField' not in {type(f).__name__ for f in Model._meta.local_fields}
    assert 'ForeignKey' not in {type(f).__name__ for f in Model._meta.local_fields}
    assert not [c for c in Model._meta.constraints if 'unique' in c.name]
    row = Model.from_values(_report(), **_ctx())
    assert row._state.adding is True
    assert type(row.progress) is str and type(row.diagnostics) is str
    got = row.as_values(**_ctx())
    assert got['progress'] == _progress() and got['diagnostics'] == (_row(),)
    assert got is not row.as_values(**_ctx())
    assert got['diagnostics'][0] == _row() and got['diagnostics'][0] is not row.as_values(**_ctx())['diagnostics'][0]
    assert type(got['diagnostics']) is tuple
    row.full_clean(exclude=[], validate_unique=False, validate_constraints=False, **_ctx())
    row.full_clean(exclude=['mode', 'progress', 'diagnostics'], validate_unique=True, validate_constraints=True, **_ctx())
    snap = row._locked_snapshot(**_ctx())
    assert type(snap) is _ReportSnapshot
    assert hasattr(snap, 'as_values')
    assert snap.as_values() == got
    assert snap.as_values() is not snap.as_values()
    try:
        snap.complete = False
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError('snapshot modifiable')
    try:
        snap.progress.validated_rows = 9
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError('progress modifiable')
    try:
        snap.diagnostics[0].code = 'mute'
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError('row modifiable')
    assert not hasattr(snap.progress, '__dict__')
    caller = _report()
    ctx = _ctx()
    row2 = Model.from_values(caller, **ctx)
    caller['progress']['validated_rows'] = 99
    caller['diagnostics'][0]['code'] = 'mute'
    caller['operation_id'] = 'mute'
    ctx['policy']['retry_delays_seconds'].append(9)
    ctx['declared_codes'] = ('mute',)
    assert row2.operation_id == 'op-test'
    assert row2.as_values()['progress']['validated_rows'] == 2
    assert row2.as_values()['diagnostics'][0]['code'] == 'INVALID_FIELD'
    assert row2._report_context.rebuild_policy()['retry_delays_seconds'] == [1, 2]
    exported = row.as_values(**_ctx())
    exported['progress']['validated_rows'] = 99
    exported['diagnostics'][0]['code'] = 'mute'
    assert row.as_values(**_ctx())['progress']['validated_rows'] == 2
    assert Model.from_values(_report(mode=None, progress=_progress(exported_rows=1, applied_rows=0)), **_ctx())._state.adding is True
    assert Model.from_values(_report(source_version='src-e', mapping_version='2.3.4-rc.1+build.7'), **_ctx())._state.adding is True
    assert Model.from_values(_report(mode='ATOMIC', progress=_progress(applied_rows=1)), **_ctx())._state.adding is True
    assert Model.from_values(_report(diagnostics=()), **_ctx())._state.adding is True
    assert Model.from_values(_report(diagnostics=({'code': 'INVALID_FIELD', 'field_reference': None, 'line_index': None},)), **_ctx())._state.adding is True
    assert Model.from_values(_report(complete=False), **_ctx()).as_values(**_ctx())['complete'] is False
    assert type(Model.from_values(_report(complete=True), **_ctx()).as_values(**_ctx())['complete']) is bool
    for key in ('report_version', 'operation_id', 'mode', 'progress', 'diagnostics', 'complete', 'source_version', 'mapping_version'):
        missing = _report()
        del missing[key]
        _refused(lambda missing=missing: Model.from_values(missing, **_ctx()), 'bulk_validation_report_invalid')
        foreign = _report()
        foreign[key] = Hostile()
        _refused(lambda foreign=foreign: Model.from_values(foreign, **_ctx()), 'bulk_validation_report_invalid')
        meta = _report()
        meta[key] = HostileValue()
        _refused(lambda meta=meta: Model.from_values(meta, **_ctx()), 'bulk_validation_report_invalid')
        raw = Model(**{'report_version': '1.0.0', 'operation_id': 'op-test', 'mode': 'VALIDATE_ONLY', 'progress': '{}', 'diagnostics': '[]', 'complete': True, 'source_version': None, 'mapping_version': '1.2.3'})
        raw.__dict__[key] = Hostile()
        _refused(lambda raw=raw: raw.full_clean(exclude=[key], **_ctx()), 'bulk_validation_report_invalid')
    extra = _report()
    extra['intrus'] = 'x'
    _refused(lambda: Model.from_values(extra, **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(BadDict(_report()), **_ctx()), 'bulk_validation_report_invalid')
    for bad in (None, 0, 'x', [], Hostile()):
        _refused(lambda bad=bad: Model.from_values(bad, **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(diagnostics=ForeignTuple((_row(),))), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(diagnostics=[_row()]), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(diagnostics=(('INVALID_FIELD', 'name', 1),)), **_ctx()), 'bulk_validation_report_invalid')
    for field, bad in (('operation_id', S('op-test')), ('report_version', S('1.0.0')), ('complete', 1)):
        badv = _report()
        badv[field] = bad
        _refused(lambda badv=badv: Model.from_values(badv, **_ctx()), 'bulk_validation_report_invalid')
    for location in ('top', 'progress', 'diagnostics'):
        armed = ArmedKey()
        if location == 'top':
            foreign = _report()
            foreign[armed] = 1
        elif location == 'progress':
            progress = _progress()
            progress[armed] = 1
            foreign = _report(progress=progress)
        else:
            item = _row()
            item[armed] = 1
            foreign = _report(diagnostics=(item,))
        armed.armed = True
        _refused(lambda foreign=foreign: Model.from_values(foreign, **_ctx()), 'bulk_validation_report_invalid')
        assert armed.calls == 0
    _refused(lambda: Model.from_values(_report(), **_ctx(declared_codes=(Hostile(),))), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(), **_ctx(declared_fields=(HostileValue(),))), 'bulk_validation_report_invalid')
    assert Model.from_values(_report(diagnostics=(_row(line_index=2 ** 80),)), **_ctx()).as_values()['diagnostics'][0]['line_index'] == 2 ** 80
    class ForeignList(list):
        def __iter__(self):
            raise AssertionError('iteration liste etrangere')
    _refused(lambda: Model.from_values(_report(), **_ctx(policy=_policy(retry_delays_seconds=ForeignList([1, 2])))), 'bulk_validation_report_invalid')
    for mode in ('IMPORT', 'EXPORT', '', True):
        _refused(lambda mode=mode: Model.from_values(_report(mode=mode), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(mode='VALIDATE_ONLY', progress=_progress(applied_rows=1)), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(mode=None, progress=_progress(applied_rows=1)), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(mode='ATOMIC', progress=_progress(exported_rows=1)), **_ctx()), 'bulk_validation_report_invalid')
    for field in ('operation_id', 'report_version', 'mapping_version', 'mode', 'source_version'):
        for value in ('', 'a' + chr(0) + 'b'):
            _refused(lambda field=field, value=value: Model.from_values(_report(**{field: value}), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(operation_id='x' + chr(0xD800)), **_ctx()), 'bulk_validation_report_invalid')
    assert Model.from_values(_report(operation_id='caf' + chr(0xE9)), **_ctx()).as_values(**_ctx())['operation_id'] == 'caf' + chr(0xE9)
    _refused(lambda: Model.from_values(_report(report_version='2.0.0'), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(mapping_version='1.2'), **_ctx()), 'bulk_validation_report_invalid')
    for bad_row in ({}, {'code': 'LEAK-MARKER', 'field_reference': 'name', 'line_index': 1}, {'code': 'INVALID_FIELD', 'field_reference': 'LEAK-MARKER', 'line_index': 1}, {'code': 'INVALID_FIELD', 'field_reference': 'name', 'line_index': 0}, {'code': 'INVALID_FIELD', 'field_reference': 'name', 'line_index': True}):
        _refused(lambda bad_row=bad_row: Model.from_values(_report(diagnostics=(bad_row,)), **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(), policy=None, declared_codes=('INVALID_FIELD',), declared_fields=('name',)), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(), policy=_policy(max_diagnostics=True), declared_codes=('INVALID_FIELD',), declared_fields=('name',)), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(), **{'policy': _policy(), 'declared_codes': ['INVALID_FIELD'], 'declared_fields': ('name',)}), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(), **{'policy': _policy(), 'declared_codes': (), 'declared_fields': ('name',)}), 'bulk_validation_report_invalid')
    poison_policy = _policy(max_diagnostics=1)
    poisoned = _report(diagnostics=(Hostile(), Hostile()))
    rejected, diagnostics = values_mod.capture_bulk_validation_report_values(poisoned, policy=poison_policy, declared_codes=('INVALID_FIELD',), declared_fields=('name',))
    assert rejected is None and len(diagnostics) == 1
    assert diagnostics[0].element.endswith('.diagnostics') and 'borne PolicyV1' in diagnostics[0].message
    _refused(lambda: Model.from_values(poisoned, policy=poison_policy, declared_codes=('INVALID_FIELD',), declared_fields=('name',)), 'bulk_validation_report_invalid')
    tampered = Model.from_values(_report(), **_ctx())
    tampered.__dict__['progress'] = '{oops'
    _refused(lambda: tampered.as_values(**_ctx()), 'bulk_validation_report_invalid')
    duped = Model.from_values(_report(), **_ctx())
    duped.__dict__['progress'] = '{"total_rows": null, "total_rows": 1}'
    _refused(lambda: duped.as_values(**_ctx()), 'bulk_validation_report_invalid')
    naned = Model.from_values(_report(), **_ctx())
    naned.__dict__['progress'] = 'NaN'
    _refused(lambda: naned.as_values(**_ctx()), 'bulk_validation_report_invalid')
    shaped = Model.from_values(_report(), **_ctx())
    shaped.__dict__['progress'] = '{"total_rows": "1"}'
    _refused(lambda: shaped.as_values(**_ctx()), 'bulk_validation_report_invalid')
    listed = Model.from_values(_report(), **_ctx())
    listed.__dict__['diagnostics'] = '[{"code": "INVALID_FIELD", "field_reference": "name", "line_index": 1}]'
    assert listed.as_values(**_ctx())['diagnostics'] == ({'code': 'INVALID_FIELD', 'field_reference': 'name', 'line_index': 1},)
    unknown = Model.from_values(_report(), **_ctx())
    unknown.__dict__['diagnostics'] = '[{"code": "UNKNOWN", "field_reference": "name", "line_index": 1}]'
    _refused(lambda: unknown.as_values(**_ctx()), 'bulk_validation_report_invalid')
    big = 2 ** 63 + 123
    coherent = _progress(validated_rows=big, invalid_rows=0, applied_rows=big, execution_rejected_rows=0, exported_rows=0)
    assert Model.from_values(_report(mode='ATOMIC', progress=coherent), **_ctx()).as_values(**_ctx())['progress']['validated_rows'] == big
    huge700 = 10 ** 700
    _refused(lambda: Model.from_values(_report(mode='ATOMIC', progress=_progress(validated_rows=huge700, invalid_rows=0, applied_rows=huge700)), **_ctx()), 'bulk_validation_report_capacity_unsupported')
    assert _sys.get_int_max_str_digits() == 640
    sup600 = 10 ** 600
    coherent600 = _progress(validated_rows=sup600, invalid_rows=0, applied_rows=sup600, execution_rejected_rows=0, exported_rows=0)
    assert Model.from_values(_report(mode='ATOMIC', progress=coherent600), **_ctx()).as_values(**_ctx())['progress']['validated_rows'] == sup600
    assert _sys.get_int_max_str_digits() == 640
    try:
        BulkValidationReportRepository(using=Hostile())
    except ValidationError as err:
        assert err.error_list[0].code == 'bulk_validation_report_alias_invalid'
    else:
        raise AssertionError('alias hostile accepte')
    for bad_alias in (None, '', 0, True, b'default', S('default')):
        try:
            BulkValidationReportRepository(using=bad_alias)
        except ValidationError as err:
            assert err.error_list[0].code == 'bulk_validation_report_alias_invalid'
        else:
            raise AssertionError('alias invalide accepte')
    repository = BulkValidationReportRepository(using='default')
    for bad_id in (None, 0, -1, True, '', S('1'), Hostile(), 2 ** 63):
        _repo_refused(lambda bad_id=bad_id: repository.get_report(report_id=bad_id, **_ctx()))
    _repo_refused(lambda: repository.get_report(report_id=999999, policy=None, declared_codes=('INVALID_FIELD',), declared_fields=('name',)))
    _repo_refused(lambda: repository.get_report(report_id=999999, policy=_policy(), declared_codes=['INVALID_FIELD'], declared_fields=('name',)))
    for bad_values in (None, BadDict(_report()), Hostile()):
        _repo_refused(lambda bad_values=bad_values: repository.insert_report(values=bad_values, **_ctx()))
    _repo_refused(lambda: repository.insert_report(values=_report(), **_ctx()))
    good = Model.from_values(_report(operation_id='save-one'), **_ctx())
    for call in (lambda: good.save(), lambda: good.save('pos'), lambda: good.save(force_insert=True, using='default', update_fields=['mode']), lambda: good.save(force_insert=True, force_update=True, using='default'), lambda: good.save(force_insert=False, using='default'), lambda: good.save(force_insert=True, using=''), lambda: good.save(force_insert=True, using=None)):
        _refused(call, 'bulk_validation_report_invalid')
    hydrated = Model.from_values(_report(operation_id='save-two'), **_ctx())
    hydrated._state.adding = False
    _refused(lambda: hydrated.save(force_insert=True, using='default'), 'bulk_validation_report_invalid')
    _refused(lambda: Model.from_values(_report(), **_ctx()).save(force_insert=True, using='default'), 'bulk_validation_report_invalid')
    try:
        Model.from_values(_report())
    except TypeError:
        pass
    else:
        raise AssertionError('contexte obligatoire absent')
    deferred = Model.from_values(_report(), **_ctx())
    del deferred.__dict__['diagnostics']
    _refused(lambda: deferred.as_values(), 'bulk_validation_report_invalid')
    _refused(lambda: deferred.full_clean(exclude=['diagnostics']), 'bulk_validation_report_invalid')
    _refused(lambda: deferred.save(force_insert=True, using='default'), 'bulk_validation_report_invalid')
    bare = Model(report_version='x')
    _refused(lambda: bare.as_values(**_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: bare.full_clean(exclude=[], **_ctx()), 'bulk_validation_report_invalid')
    _refused(lambda: bare.save(force_insert=True, using='default'), 'bulk_validation_report_invalid')
    loader = MigrationLoader(None)
    migration = loader.disk_migrations[('backend', '0009_bulk_validation_report')]
    assert migration.dependencies == [('backend', '0008_bulk_inbox_receipt')]
    assert len(migration.operations) == 1
    op = migration.operations[0]
    assert isinstance(op, CreateModel)
    assert op.name == 'BulkValidationReportRecord'
    assert tuple(name for name, field in op.fields) == ('id', 'report_version', 'operation_id', 'mode', 'progress', 'diagnostics', 'complete', 'source_version', 'mapping_version')
    assert len(op.options['constraints']) == 7
    expected_state = loader.project_state()
    actual_state = ProjectState.from_apps(apps)
    assert MigrationAutodetector(expected_state, actual_state).changes(graph=loader.graph) == {}
    assert MigrationAutodetector(actual_state, expected_state).changes(graph=loader.graph) == {}
    assert counters == {'db': 0, 'network': 0, 'process': 0}, counters
print('BULK_VALIDATION_REPORT_OFFLINE_SAFE_OK')
"""


class BulkValidationReportOfflineTests(unittest.TestCase):
    def test_offline_guards_and_persistence(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-X', 'int_max_str_digits=640', '-c', _CHILD, _SRC], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER + chr(10))
        self.assertEqual(result.stderr, '')


if __name__ == '__main__':
    unittest.main()
