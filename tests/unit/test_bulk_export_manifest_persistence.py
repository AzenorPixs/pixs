'''Persistance ExportManifestV1 offline en processus frais sous gardes.'''

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / 'src')
_MARKER = 'BULK_EXPORT_MANIFEST_OFFLINE_SAFE_OK'
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONDONTWRITEBYTECODE': '1'}

_CHILD = r'''
import socket
import subprocess
import sys
import os
import builtins
from pathlib import Path
from contextlib import ExitStack
from unittest import mock
sys.path.insert(0, sys.argv[1])
import sys as _sys
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone, timedelta
import django
from django.apps import apps
from django.conf import settings
assert not settings.configured
assert not apps.ready
import psycopg
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
import pixs.kernel.diagnostics as _diag_pre
import pixs.backend.bulk_execution_values as _exec_pre
import pixs.backend.bulk_export_manifest_values as _values_pre
class GuardBlocked(Exception):
  def __init__(self, bucket):
    super().__init__('garde effet interdit')
    self.bucket = bucket
counters = {'db': 0, 'network': 0, 'process': 0, 'file': 0}
def _make_guard(bucket):
  def _blocked(*args, **kwargs):
    counters[bucket] += 1
    raise GuardBlocked(bucket)
  return _blocked
_orig_open = builtins.open
_orig_path_open = Path.open
_orig_os_open = os.open
def _file_open(file, *args, **kwargs):
  s = str(file)
  if '.env' in s or 'project.env' in s:
    counters['file'] += 1
    raise GuardBlocked('file')
  return _orig_open(file, *args, **kwargs)
def _path_open(self, *args, **kwargs):
  s = str(self)
  if '.env' in s or 'project.env' in s:
    counters['file'] += 1
    raise GuardBlocked('file')
  return _orig_path_open(self, *args, **kwargs)
def _os_open(path, *args, **kwargs):
  s = str(path)
  if '.env' in s or 'project.env' in s:
    counters['file'] += 1
    raise GuardBlocked('file')
  return _orig_os_open(path, *args, **kwargs)
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
  stack.enter_context(mock.patch.object(builtins, 'open', new=_file_open))
  stack.enter_context(mock.patch.object(Path, 'open', new=_path_open))
  stack.enter_context(mock.patch.object(os, 'open', new=_os_open))
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
  _probe(lambda: builtins.open('.env', 'r'), 'file')
  _probe(lambda: Path('.env').open('r'), 'file')
  _probe(lambda: os.open('.env', os.O_RDONLY), 'file')
  assert counters == {'db': 3, 'network': 2, 'process': 2, 'file': 3}, counters
  for key in counters:
    counters[key] = 0
  from django.core.exceptions import ValidationError
  from django.db import models, transaction
  settings.configure(DEFAULT_CHARSET='utf-8', INSTALLED_APPS=['pixs.backend'], SECRET_KEY='unit-offline-synthetic-only', DATABASES={'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'bulk_manifest_offline_synthetic'}, 'other': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'bulk_manifest_offline_other'}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
  django.setup()
  from pixs.backend.bulk_export_manifest_record import BulkExportManifestRecord as Model
  from pixs.backend.bulk_export_manifest_record import _FIELDS
  import pixs.backend.bulk_export_manifest_values as values_mod
  assert _sys.get_int_max_str_digits() == 640
  _CANON = ('manifest_version', 'operation_id', 'format', 'mapping_reference', 'mapping_version', 'tenant_context_reference', 'scope_context_reference', 'consistency_kind', 'consistency_reference', 'row_count', 'size_bytes', 'sha256', 'classification_reference', 'expires_at', 'object_reference', 'object_version', 'complete')
  assert tuple(_FIELDS) == _CANON
  def _base(**over):
    base = {'manifest_version': '1.0.0', 'operation_id': 'op-test', 'format': 'CSV', 'mapping_reference': 'map-ref', 'mapping_version': '1.2.3', 'tenant_context_reference': 'tenant-ref', 'scope_context_reference': 'scope-test', 'consistency_kind': 'SNAPSHOT', 'consistency_reference': 'cons-ref', 'row_count': 2, 'size_bytes': 128, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'classification_reference': 'class-ref', 'expires_at': datetime(2030, 1, 1, tzinfo=timezone.utc), 'object_reference': 'obj-ref', 'object_version': 'v1', 'complete': True}
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
    except BulkExportManifestRefused as err:
      assert str(err) == 'manifeste export bulk refuse'
      return
    raise AssertionError('refus repository absent')
  import pixs.backend.bulk_export_manifest_record as record_mod
  import pixs.backend.bulk_export_manifest_repository as repo_mod
  from pixs.backend.bulk_export_manifest_repository import BulkExportManifestRefused
  from pixs.backend.bulk_export_manifest_repository import BulkExportManifestRepository
  from pixs.backend.bulk_export_manifest_values import _ExportManifestBound
  import pixs.backend.models as registered
  assert record_mod.__all__ == ['BulkExportManifestRecord']
  assert repo_mod.__all__ == ['BulkExportManifestRefused', 'BulkExportManifestRepository']
  assert registered.__all__ == ['FeatureFlagSourceSnapshotRecord', 'JobRecord']
  assert apps.get_model('backend', 'BulkExportManifestRecord') is Model
  assert not Model.check(databases=[])
  assert Model._meta.pk.name == 'id'
  assert len(Model._meta.local_fields) == 18
  assert Model.save is not models.Model.save
  _names = {c.name for c in Model._meta.constraints}
  assert _names == {'bulkexportmanifest_version_exact', 'bulkexportmanifest_operation_non_empty', 'bulkexportmanifest_format_member', 'bulkexportmanifest_mapping_ref_non_empty', 'bulkexportmanifest_mapping_version_non_empty', 'bulkexportmanifest_tenant_non_empty', 'bulkexportmanifest_consistency_member', 'bulkexportmanifest_consistency_ref_non_empty', 'bulkexportmanifest_sha_regex', 'bulkexportmanifest_classification_non_empty', 'bulkexportmanifest_object_ref_non_empty', 'bulkexportmanifest_object_version_non_empty', 'bulkexportmanifest_scope_non_empty', 'bulkexportmanifest_row_count_regex', 'bulkexportmanifest_size_bytes_regex'}
  _fmap = {f.name: f for f in Model._meta.local_fields}
  assert type(_fmap['id']).__name__ == 'BigAutoField'
  assert type(_fmap['row_count']).__name__ == 'TextField'
  assert type(_fmap['size_bytes']).__name__ == 'TextField'
  assert type(_fmap['complete']).__name__ == 'BooleanField'
  assert 'ForeignKey' not in {type(f).__name__ for f in Model._meta.local_fields}
  assert not [c for c in Model._meta.constraints if 'unique' in c.name]
  assert 'TrustedUtc' in type(_fmap['expires_at']).__name__
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
    def keys(self):
      raise AssertionError('keys etranger')
  class S(str):
    def __str__(self):
      raise AssertionError('str sousclasse')
    def __eq__(self, other):
      raise AssertionError('eq sousclasse')
  class I(int):
    def __int__(self):
      raise AssertionError('int sousclasse')
    def __index__(self):
      raise AssertionError('index sousclasse')
  class D(datetime):
    def __getattribute__(self, name):
      if name == 'tzinfo':
        raise AssertionError('tzinfo sousclasse')
      return super().__getattribute__(name)
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
  row = Model.from_values(_base())
  assert row._state.adding is True
  assert row.id is None
  assert type(row.row_count) is str and type(row.size_bytes) is str
  got = row.as_values()
  assert list(got.keys()) == list(_CANON)
  assert got['operation_id'] == 'op-test' and got['row_count'] == 2
  assert got is not row.as_values()
  assert type(got['expires_at']) is datetime and got['expires_at'].tzinfo is timezone.utc
  row.full_clean(exclude=[], validate_unique=False, validate_constraints=False)
  row.full_clean(exclude=['format', 'row_count'], validate_unique=True, validate_constraints=True)
  bound0, diags0 = values_mod.capture_bulk_export_manifest_values(_base())
  assert bound0 is not None and diags0 == []
  assert type(bound0) is _ExportManifestBound
  try:
    bound0.complete = False
  except FrozenInstanceError:
    pass
  else:
    raise AssertionError('bound modifiable')
  caller = _base()
  rec2 = Model.from_values(caller)
  caller['operation_id'] = 'mute'
  caller['row_count'] = 99
  assert rec2.operation_id == 'op-test' and rec2.as_values()['row_count'] == 2
  exported = row.as_values()
  exported['operation_id'] = 'mute'
  assert row.as_values()['operation_id'] == 'op-test'
  assert Model.from_values(_base(scope_context_reference=None)).as_values()['scope_context_reference'] is None
  assert Model.from_values(_base(complete=False)).as_values()['complete'] is False
  assert Model.from_values(_base(format='NDJSON')).as_values()['format'] == 'NDJSON'
  assert Model.from_values(_base(consistency_kind='WATERMARK')).as_values()['consistency_kind'] == 'WATERMARK'
  _min = datetime(1, 1, 1, tzinfo=timezone.utc)
  _max = datetime(9999, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
  assert Model.from_values(_base(expires_at=_min)).as_values()['expires_at'] == _min
  assert Model.from_values(_base(expires_at=_max)).as_values()['expires_at'] == _max
  _foreign_tz = timezone(timedelta(hours=1))
  _refused(lambda: Model.from_values(_base(expires_at=datetime(2030, 1, 1, tzinfo=_foreign_tz))), 'bulk_export_manifest_invalid')
  _refused(lambda: Model.from_values(_base(expires_at=datetime(2030, 1, 1))), 'bulk_export_manifest_invalid')
  _refused(lambda: Model.from_values(_base(expires_at=D(2030, 1, 1, tzinfo=timezone.utc))), 'bulk_export_manifest_invalid')
  try:
    Model.from_values(_base(), unexpected=1)
  except TypeError:
    pass
  else:
    raise AssertionError('callback etranger accepte')
  for key in _CANON:
    missing = _base()
    del missing[key]
    _refused(lambda missing=missing: Model.from_values(missing), 'bulk_export_manifest_invalid')
    foreign = _base()
    foreign[key] = Hostile()
    _refused(lambda foreign=foreign: Model.from_values(foreign), 'bulk_export_manifest_invalid')
    raw = Model.from_values(_base())
    raw.__dict__[key] = Hostile()
    _refused(lambda raw=raw: raw.as_values(), 'bulk_export_manifest_invalid')
    _refused(lambda raw=raw: raw.full_clean(exclude=[key]), 'bulk_export_manifest_invalid')
  extra = _base()
  extra['intrus'] = 'x'
  _refused(lambda: Model.from_values(extra), 'bulk_export_manifest_invalid')
  _refused(lambda: Model.from_values(BadDict(_base())), 'bulk_export_manifest_invalid')
  _refused(lambda: Model.from_values(ForeignTuple()), 'bulk_export_manifest_invalid')
  for field, bad in (('operation_id', S('op-test')), ('complete', 1), ('row_count', True), ('row_count', 1.5), ('row_count', I(1))):
    badv = _base()
    badv[field] = bad
    _refused(lambda badv=badv: Model.from_values(badv), 'bulk_export_manifest_invalid')
  armed = ArmedKey()
  foreign2 = _base()
  foreign2[armed] = 1
  armed.armed = True
  _refused(lambda: Model.from_values(foreign2), 'bulk_export_manifest_invalid')
  assert armed.calls == 0
  big = 2 ** 63 + 123
  assert Model.from_values(_base(row_count=big, size_bytes=big)).as_values()['row_count'] == big
  sup600 = 10 ** 600
  assert Model.from_values(_base(row_count=sup600, size_bytes=sup600)).as_values()['row_count'] == sup600
  assert _sys.get_int_max_str_digits() == 640
  huge1000 = 10 ** 1000
  pb, pd = values_mod.capture_bulk_export_manifest_values(_base(row_count=huge1000, size_bytes=huge1000))
  assert pb is not None and pd == [] and pb.row_count == huge1000
  _refused(lambda: Model.from_values(_base(row_count=huge1000, size_bytes=huge1000)), 'bulk_export_manifest_capacity_unsupported')
  for badcount in (-1, True, 1.5, I(2)):
    _refused(lambda badcount=badcount: Model.from_values(_base(row_count=badcount)), 'bulk_export_manifest_invalid')
  for field in ('row_count', 'size_bytes'):
    for badtext in ('', '+1', '-1', ' 1', '1 ', '01', '00', 'NaN', 'abc', chr(1632) + chr(1633)):
      tamp = Model.from_values(_base())
      tamp.__dict__[field] = badtext
      _refused(lambda tamp=tamp: tamp.as_values(), 'bulk_export_manifest_invalid')
    cap = Model.from_values(_base())
    cap.__dict__[field] = '9' * 1000
    _refused(lambda cap=cap: cap.as_values(), 'bulk_export_manifest_capacity_unsupported')
  uni1 = chr(1632) + chr(1633)
  tampu = Model.from_values(_base())
  tampu.__dict__['row_count'] = uni1
  _refused(lambda: tampu.as_values(), 'bulk_export_manifest_invalid')
  captext = '9' * 1000
  tampc = Model.from_values(_base())
  tampc.__dict__['row_count'] = captext
  _refused(lambda: tampc.as_values(), 'bulk_export_manifest_capacity_unsupported')
  assert _sys.get_int_max_str_digits() == 640
  from datetime import tzinfo
  class ForeignTz(tzinfo):
    def utcoffset(self, dt):
      raise AssertionError('offset tz etranger')
    def dst(self, dt):
      raise AssertionError('dst tz etranger')
    def tzname(self, dt):
      raise AssertionError('name tz etranger')
  foreign_date = datetime(2030, 1, 1, tzinfo=ForeignTz())
  _refused(lambda: Model.from_values(_base(expires_at=foreign_date)), 'bulk_export_manifest_invalid')
  _calls = []
  def _spy(text):
    _calls.append(text)
    raise AssertionError('decode non autorise pour cas foreign')
  with mock.patch.object(record_mod, '_decode_count', side_effect=_spy):
    for field in _CANON:
      spyt = Model.from_values(_base())
      spyt.__dict__[field] = Hostile()
      _refused(lambda spyt=spyt: spyt.as_values(), 'bulk_export_manifest_invalid')
      _refused(lambda spyt=spyt: spyt.full_clean(exclude=list(_CANON)), 'bulk_export_manifest_invalid')
      _refused(lambda spyt=spyt: spyt.save(force_insert=True, using='default'), 'bulk_export_manifest_invalid')
    spyt = Model.from_values(_base())
    spyt.__dict__['expires_at'] = foreign_date
    _refused(lambda: spyt.as_values(), 'bulk_export_manifest_invalid')
    assert _calls == []
  assert Model.from_values(_base(row_count=7)).as_values()['row_count'] == 7
  deferred = Model.from_values(_base())
  del deferred.__dict__['operation_id']
  _refused(lambda: deferred.as_values(), 'bulk_export_manifest_invalid')
  _refused(lambda: deferred.full_clean(exclude=['operation_id']), 'bulk_export_manifest_invalid')
  _refused(lambda: deferred.save(force_insert=True, using='default'), 'bulk_export_manifest_invalid')
  good = Model.from_values(_base(operation_id='save-one'))
  for call in (lambda: good.save(), lambda: good.save('pos'), lambda: good.save(force_insert=False, using='default'), lambda: good.save(force_insert=1, using='default'), lambda: good.save(force_insert=True, force_update=True, using='default'), lambda: good.save(force_insert=True, using='default', update_fields=['format']), lambda: good.save(force_insert=True, using=''), lambda: good.save(force_insert=True, using=None)):
    _refused(call, 'bulk_export_manifest_invalid')
  hydrated = Model.from_values(_base(operation_id='save-two'))
  hydrated._state.adding = False
  _refused(lambda: hydrated.save(force_insert=True, using='default'), 'bulk_export_manifest_invalid')
  _refused(lambda: Model.from_values(_base()).save(force_insert=True, using='default'), 'bulk_export_manifest_invalid')
  try:
    BulkExportManifestRepository(using=Hostile())
  except ValidationError as err:
    assert err.error_list[0].code == 'bulk_export_manifest_alias_invalid'
  else:
    raise AssertionError('alias hostile accepte')
  for bad_alias in (None, '', 0, True, S('default')):
    _refused(lambda bad_alias=bad_alias: BulkExportManifestRepository(using=bad_alias), 'bulk_export_manifest_alias_invalid')
  repository = BulkExportManifestRepository(using='default')
  with mock.patch.object(transaction, 'get_connection', side_effect=AssertionError('connexion non autorisee')):
    _repo_refused(lambda: repository.insert_manifest(values=None))
  with mock.patch.object(Model.objects, 'using', side_effect=AssertionError('orm non autorise')):
    for bad_id in (None, True, 0, -1, 2 ** 63 * 2):
      _repo_refused(lambda bad_id=bad_id: repository.get_manifest(manifest_id=bad_id))
  _repo_refused(lambda: repository.insert_manifest(values=_base()))
  import importlib
  from django.db.migrations.operations.models import CreateModel
  migration_module = importlib.import_module('pixs.backend.migrations.0010_bulk_export_manifest')
  migration = migration_module.Migration('0010_bulk_export_manifest', 'backend')
  assert migration.dependencies == [('backend', '0009_bulk_validation_report')]
  assert len(migration.operations) == 1
  op = migration.operations[0]
  assert type(op) is CreateModel and op.name == 'BulkExportManifestRecord'
  assert tuple(name for name, field in op.fields) == ('id',) + _CANON
  assert len(op.options['constraints']) == 15
  assert [(name, field.deconstruct()[1:]) for name, field in op.fields] == [(field.name, field.deconstruct()[1:]) for field in Model._meta.local_fields]
  assert [c.deconstruct() for c in op.options['constraints']] == [c.deconstruct() for c in Model._meta.constraints]
  assert all(not f.has_default() and not f.unique for f in Model._meta.local_fields if not f.primary_key)
  assert counters == {'db': 0, 'network': 0, 'process': 0, 'file': 0}, counters
  assert _sys.get_int_max_str_digits() == 640
  print('BULK_EXPORT_MANIFEST_OFFLINE_SAFE_OK')
'''

class BulkExportManifestOfflineTests(unittest.TestCase):
  def test_offline_guards_and_persistence(self):
    result = subprocess.run([sys.executable, '-I', '-B', '-X', 'int_max_str_digits=640', '-c', _CHILD, _SRC], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout, _MARKER + chr(10))
    self.assertEqual(result.stderr, '')

if __name__ == '__main__':
  unittest.main()
