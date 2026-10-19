'''Persistance OutboxPublicationV1 initiale offline en processus frais sous gardes.'''

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / 'src')
_MARKER = 'BULK_OUTBOX_INITIAL_OFFLINE_SAFE_OK'
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
import pixs.backend.bulk_outbox_publication_values as _values_pre
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
guard_targets = [(PGWrapper, 'get_new_connection', 'db'), (psycopg, 'connect', 'db'), (psycopg.Connection, 'connect', 'db'), (socket.socket, 'connect', 'network'), (socket, 'create_connection', 'network'), (subprocess, 'Popen', 'process'), (subprocess, 'run', 'process')]
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
  settings.configure(DEFAULT_CHARSET='utf-8', INSTALLED_APPS=['pixs.backend'], SECRET_KEY='unit-offline-synthetic-only', DATABASES={'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'bulk_outbox_offline_synthetic'}, 'other': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'bulk_outbox_offline_other'}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
  django.setup()
  from pixs.backend.bulk_outbox_publication_record import BulkOutboxPublicationRecord as Model
  from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord as Counter
  from pixs.backend.bulk_outbox_publication_record import _FIELDS, _encode_count, _decode_count, _capture_catalogue, _check_failure_code, _invalid, _AllocationContext, _allocation_var
  from pixs.backend.bulk_outbox_publication_repository import BulkOutboxPublicationRepository
  from pixs.backend.bulk_outbox_publication_values import capture_bulk_outbox_publication_values as _capture
  from pixs.backend.bulk_outbox_publication_values import _OutboxPublicationBound
  assert _sys.get_int_max_str_digits() == 640
  _CANON12 = ('event_id', 'state', 'attempt_count', 'lease_owner', 'lease_expires_at', 'next_attempt_at', 'published_at', 'failure_code', 'sequence_index', 'policy_reference', 'policy_version', 'revision')
  assert tuple(_FIELDS) == _CANON12
  def _base12(**over):
    base = {'event_id': 'evt-test-001', 'state': 'PENDING', 'attempt_count': 0, 'lease_owner': None, 'lease_expires_at': None, 'next_attempt_at': None, 'published_at': None, 'failure_code': None, 'sequence_index': 1, 'policy_reference': 'policy-ref', 'policy_version': '1.2.3', 'revision': 7}
    base.update(over)
    return base
  def _source11(**over):
    src = {'event_id': 'evt-test-001', 'state': 'PENDING', 'attempt_count': 0, 'lease_owner': None, 'lease_expires_at': None, 'next_attempt_at': None, 'published_at': None, 'failure_code': None, 'policy_reference': 'policy-ref', 'policy_version': '1.2.3', 'revision': 7}
    src.update(over)
    return src
  _EMPTY_CATALOGUE = ()
  _OPAQUE_CODE = 'E_CONN-RESET.v2:retry'
  def _base_full(**over):
    base = _base12(lease_owner='owner-1', lease_expires_at=datetime(2030, 2, 1, tzinfo=timezone.utc), next_attempt_at=datetime(2030, 3, 1, tzinfo=timezone.utc), published_at=datetime(2030, 4, 1, tzinfo=timezone.utc), failure_code=_OPAQUE_CODE)
    base.update(over)
    return base
  def _refused(call):
    try:
      call()
    except ValidationError as err:
      assert err.error_list
      assert all(item.code == 'bulk_outbox_publication_invalid' for item in err.error_list)
      joined = chr(10).join(err.messages)
      for secret in ('evt-test-001', 'owner-1', 'LEAK-MARKER'):
        assert secret not in joined
      return
    raise AssertionError('refus ValidationError absent')
  _b0, _d0 = _capture(_base12())
  assert _b0 is not None and _d0 == []
  assert type(_b0) is _OutboxPublicationBound
  try:
    _b0.state = 'X'
  except FrozenInstanceError:
    pass
  else:
    raise AssertionError('bound modifiable')
  _bf, _df = _capture(_base_full())
  assert _bf is not None and _df == []
  _check_failure_code(_bf.failure_code, (_OPAQUE_CODE,))

  import importlib as _il
  import pixs.backend.bulk_outbox_publication_record as record_mod
  import pixs.backend.bulk_outbox_publication_repository as repo_mod
  from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord as EnvModel
  import pixs.backend.models as registered
  from django.db import IntegrityError
  assert record_mod.__all__ == ['BulkOutboxPublicationRecord']
  assert repo_mod.__all__ == ['BulkOutboxPublicationRepository']
  assert registered.__all__ == ['FeatureFlagSourceSnapshotRecord', 'JobRecord']
  assert apps.get_model('backend', 'BulkOutboxPublicationRecord') is Model
  assert not Model.check(databases=[])
  assert not Counter.check(databases=[])
  assert {f.attname for f in Model._meta.local_fields} == set(_CANON12) | {'order_scope_reference_private'}
  _evf = Model._meta.get_field('event')
  assert type(_evf).__name__ == 'OneToOneField' and _evf.primary_key and _evf.db_column == 'event_id' and _evf.remote_field.related_name == '+' and _evf.serialize is False
  assert _evf.remote_field.on_delete is models.PROTECT
  assert Model.save is not models.Model.save
  _cmap = {f.name: f for f in Counter._meta.local_fields}
  assert set(_cmap) == {'scope_private', 'next_index'} and _cmap['scope_private'].primary_key
  assert Counter._meta.db_table == 'backend_bulkoutboxscopecounterrecord'
  assert all(not f.has_default() and not f.unique for f in Model._meta.local_fields if not f.primary_key)
  assert 'IntegerField' not in {type(f).__name__ for f in Model._meta.local_fields}
  assert 'TrustedUtc' in type(Model._meta.get_field('lease_expires_at')).__name__
  assert {c.name for c in Model._meta.constraints} == {'bulkoutbox_event_non_empty', 'bulkoutbox_state_member', 'bulkoutbox_scope_non_empty', 'bulkoutbox_attempt_codec', 'bulkoutbox_seq_codec', 'bulkoutbox_revision_codec', 'bulkoutbox_lease_pair', 'bulkoutbox_retrying_next', 'bulkoutbox_published_at', 'bulkoutbox_policy_ref_non_empty', 'bulkoutbox_policy_version_non_empty', 'bulkoutbox_lease_owner_empty', 'bulkoutbox_failure_code_empty', 'bulkoutbox_scope_seq_unique'}
  assert {c.name for c in Counter._meta.constraints} == {'bulkoutboxcounter_scope_non_empty', 'bulkoutboxcounter_next_codec'}
  _migmod = _il.import_module('pixs.backend.migrations.0011_bulk_outbox_publication')
  _mig = _migmod.Migration('0011_bulk_outbox_publication', 'backend')
  assert _mig.dependencies == [('backend', '0010_bulk_export_manifest')]
  assert len(_mig.operations) == 2
  from django.db.migrations.operations.models import CreateModel as _CM
  _op0, _op1 = _mig.operations
  assert type(_op0) is _CM and _op0.name == 'BulkOutboxScopeCounterRecord'
  assert type(_op1) is _CM and _op1.name == 'BulkOutboxPublicationRecord'
  assert tuple(n for n, f in _op1.fields) == ('event', 'state', 'attempt_count', 'lease_owner', 'lease_expires_at', 'next_attempt_at', 'published_at', 'failure_code', 'sequence_index', 'policy_reference', 'policy_version', 'revision', 'order_scope_reference_private')
  assert [c.deconstruct() for c in _op1.options['constraints']] == [c.deconstruct() for c in Model._meta.constraints]
  assert [c.deconstruct() for c in _op0.options['constraints']] == [c.deconstruct() for c in Counter._meta.constraints]
  class Hostile:
    def __bool__(self): raise AssertionError('bool etranger')
    def __eq__(self, other): raise AssertionError('eq etranger')
    def __hash__(self): raise AssertionError('hash etranger')
    def __str__(self): raise AssertionError('str etranger')
    def __repr__(self): raise AssertionError('repr etranger')
  class S(str):
    def __str__(self): raise AssertionError('str sousclasse')
    def __eq__(self, other): raise AssertionError('eq sousclasse')
  class I(int):
    def __int__(self): raise AssertionError('int sousclasse')
    def __index__(self): raise AssertionError('index sousclasse')
  class D(datetime):
    def __getattribute__(self, name):
      if name == 'tzinfo': raise AssertionError('tzinfo sousclasse')
      return super().__getattribute__(name)
  class BadDict(dict):
    def items(self): raise AssertionError('items etranger')
  for _st in ('PENDING', 'PUBLISHED', 'RETRYING', 'FAILED', 'DEAD_LETTER'):
    _sv = _base12(state=_st)
    if _st == 'RETRYING': _sv['next_attempt_at'] = datetime(2031, 1, 1, tzinfo=timezone.utc)
    if _st == 'PUBLISHED': _sv['published_at'] = datetime(2031, 1, 1, tzinfo=timezone.utc)
    _pb, _pd = _capture(_sv)
    assert _pb is not None and _pd == [] and _pb.state == _st
  _nd, _ng = _capture(_base12(state='DRAFT'))
  assert _nd is None and _ng != []
  _refused(lambda: Model.from_values(_base12(state='DRAFT'), order_scope_reference_private='scope-test', failure_catalogue=()))
  _refused(lambda: _capture_catalogue(['x']))
  _nb, _ng2 = _capture(BadDict(_base12()))
  assert _nb is None and _ng2 != []
  _miss = _base12(); del _miss['revision']
  _mb, _mg = _capture(_miss)
  assert _mb is None and _mg != []
  _refused(lambda: Model.from_values(_base_full(), order_scope_reference_private='scope-test', failure_catalogue=('zzz',)))
  assert Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=()).as_values()['revision'] == 7
  _full_row = Model.from_values(_base_full(), order_scope_reference_private='scope-a', failure_catalogue=(_OPAQUE_CODE,))
  assert _full_row.as_values()['lease_owner'] == 'owner-1'
  for _bad in (True, 1.5, I(3), -1):
    _refused(lambda _bad=_bad: Model.from_values(_base12(attempt_count=_bad), order_scope_reference_private='scope-test', failure_catalogue=()))
    _refused(lambda _bad=_bad: Model.from_values(_base12(sequence_index=_bad), order_scope_reference_private='scope-test', failure_catalogue=()))
  for _badtext in ('', '01', '+1', '-1', ' 1', '1 '):
    _t = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
    _t.__dict__['sequence_index'] = _badtext
    _refused(lambda _t=_t: _t.as_values())
  _tn = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  _tn.__dict__['sequence_index'] = '1\n1'
  _refused(lambda: _tn.as_values())
  assert Model.from_values(_base12(attempt_count=2 ** 100, sequence_index=2 ** 100, revision=2 ** 100), order_scope_reference_private='scope-test', failure_catalogue=()).as_values()['revision'] == 2 ** 100
  _huge = 10 ** 640
  _hb, _hd = _capture(_base12(attempt_count=_huge, sequence_index=_huge, revision=_huge))
  assert _hb is not None and _hd == []
  try:
    Model.from_values(_base12(attempt_count=_huge, sequence_index=_huge, revision=_huge), order_scope_reference_private='scope-test', failure_catalogue=())
  except ValidationError as _ce:
    assert all(i.code == 'bulk_outbox_publication_capacity_unsupported' for i in _ce.error_list)
  else:
    raise AssertionError('capacite stdlib absente')
  _foreign_tz = timezone(timedelta(hours=1))
  _refused(lambda: Model.from_values(_base12(lease_expires_at=datetime(2030, 1, 1, tzinfo=_foreign_tz)), order_scope_reference_private='scope-test', failure_catalogue=()))
  _refused(lambda: Model.from_values(_base12(next_attempt_at=datetime(2030, 1, 1)), order_scope_reference_private='scope-test', failure_catalogue=()))
  _refused(lambda: Model.from_values(_base12(published_at=D(2030, 1, 1, tzinfo=timezone.utc)), order_scope_reference_private='scope-test', failure_catalogue=()))
  _calls = []
  def _spy(text):
    _calls.append(text)
    raise AssertionError('decode non autorise pour cas foreign')
  with mock.patch.object(record_mod, '_decode_count', side_effect=_spy):
    for _fld in list(_CANON12) + ['order_scope_reference_private']:
      _sp = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
      _sp.__dict__[_fld] = Hostile()
      _refused(lambda _sp=_sp: _sp.as_values())
    assert _calls == []
  _okrow = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  _okrow.full_clean(exclude=[])
  with mock.patch.object(Model._meta.get_field('event'), 'validate', side_effect=AssertionError('fk query')):
    _okrow.full_clean(exclude=['event', 'state', 'attempt_count', 'lease_owner', 'lease_expires_at', 'next_attempt_at', 'published_at', 'failure_code', 'sequence_index', 'policy_reference', 'policy_version', 'revision', 'order_scope_reference_private'])
  _repo = BulkOutboxPublicationRepository(using='default')
  try:
    _repo.insert_initial(event_id='x', state='PENDING', attempt_count=0, lease_owner=None, lease_expires_at=None, next_attempt_at=None, published_at=None, failure_code=None, policy_reference='p', policy_version='1.2.3', revision=1)
  except TypeError:
    pass
  else:
    raise AssertionError('catalogue optionnel accepte')
  try:
    _repo.insert_initial(**dict(_source11(), sequence_index=9), failure_catalogue=())
  except TypeError:
    pass
  else:
    raise AssertionError('sequence caller acceptee')
  try:
    _repo.insert_initial(event_id='e', state='PENDING', attempt_count=0, failure_catalogue=())
  except TypeError:
    pass
  else:
    raise AssertionError('nullable optionnel accepte')
  with mock.patch.object(transaction, 'get_connection', side_effect=AssertionError('connexion non autorisee')):
    with mock.patch.object(Model.objects, 'using', side_effect=AssertionError('orm non autorise')):
      try:
        _repo._validated_source(**_source11(), failure_catalogue=Hostile())
      except ValidationError:
        pass
      else:
        raise AssertionError('source invalide avant connexion absente')
      try:
        _repo.insert_initial(**_source11(state='PUBLISHED', published_at=datetime(2032, 1, 1, tzinfo=timezone.utc)), failure_catalogue=())
      except ValidationError:
        pass
      else:
        raise AssertionError('insert non-PENDING avant connexion absente')
  with mock.patch.object(Model.objects, 'using', side_effect=AssertionError('orm non autorise')):
    try:
      _repo.get_publication(event_id='evt-test-001', failure_catalogue=Hostile())
    except ValidationError:
      pass
    else:
      raise AssertionError('catalogue get invalide avant ORM absent')
  _good = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  for _call in (lambda: _good.save(), lambda: _good.save('pos'), lambda: _good.save(force_insert=False, using='default'), lambda: _good.save(force_insert=True, force_update=True, using='default'), lambda: _good.save(force_insert=True, using='default', update_fields=['state']), lambda: _good.save(force_insert=True, using=None)):
    _refused(_call)
  _hyd = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  _hyd._state.adding = False
  _refused(lambda: _hyd.save(force_insert=True, using='default'))
  _refused(lambda: _good.save(force_insert=True, using='default'))
  _frames = [object()]
  class _FakeConn:
    in_atomic_block = True
    def __init__(self, blocks): self.atomic_blocks = blocks
  _fake = _FakeConn(_frames)
  _row = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  _other_row = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  _ctx_ok = _AllocationContext(record=_row, owner_blocks=tuple(_frames), alias='default', event_id='evt-test-001', scope_private='scope-test', sequence_index=1)
  with mock.patch.object(transaction, 'get_connection', return_value=_fake):
    _tok0 = _allocation_var.set(_ctx_ok)
    try:
      _refused(lambda: _row.save(force_insert=True, using='other'))
    finally:
      _allocation_var.reset(_tok0)
    _tok = _allocation_var.set(_AllocationContext(record=_other_row, owner_blocks=tuple(_frames), alias='default', event_id='evt-test-001', scope_private='scope-test', sequence_index=1))
    try:
      _refused(lambda: _row.save(force_insert=True, using='default'))
    finally:
      _allocation_var.reset(_tok)
    _tok2 = _allocation_var.set(_AllocationContext(record=_row, owner_blocks=(object(),), alias='default', event_id='evt-test-001', scope_private='scope-test', sequence_index=1))
    try:
      _refused(lambda: _row.save(force_insert=True, using='default'))
    finally:
      _allocation_var.reset(_tok2)
    _tok3 = _allocation_var.set(_AllocationContext(record=_row, owner_blocks=(), alias='default', event_id='evt-test-001', scope_private='scope-test', sequence_index=1))
    try:
      _refused(lambda: _row.save(force_insert=True, using='default'))
    finally:
      _allocation_var.reset(_tok3)
    _tok4 = _allocation_var.set(_ctx_ok)
    try:
      with mock.patch.object(models.Model, 'save', return_value=None) as _ms:
        _row.save(force_insert=True, using='default')
        assert _ms.call_count == 1
        _, _kw = _ms.call_args
        assert _kw.get('force_insert') is True and _kw.get('using') == 'default'
    finally:
      _allocation_var.reset(_tok4)
  assert _allocation_var.get() is None
  _cok = Counter(scope_private='scope-test', next_index='4')
  _cok.full_clean(exclude=['scope_private', 'next_index'])
  assert _cok._current_values() == {'scope_private': 'scope-test', 'next_index': 4}
  _refused(lambda: Counter(scope_private='scope-test', next_index='0').full_clean(exclude=[]))
  _refused(lambda: _cok.save(force_insert=True, using='default'))
  class _FakeQS:
    def __init__(self, value): self._v = value
    def filter(self, **kw): return self
    def values(self, *a, **k): return self
    def first(self): return self._v
  _grow = Model.from_values(_base12(), order_scope_reference_private='scope-a', failure_catalogue=(_OPAQUE_CODE,))
  with mock.patch.object(Model.objects, 'using', return_value=_FakeQS(_grow)):
    with mock.patch.object(EnvModel.objects, 'using', return_value=_FakeQS({'event_id': 'evt-test-001', 'order_scope_reference': 'scope-a'})):
      _got = _repo.get_publication(event_id='evt-test-001', failure_catalogue=(_OPAQUE_CODE,))
      assert type(_got) is _OutboxPublicationBound and _got.sequence_index == 1
      try:
        _got.state = 'X'
      except FrozenInstanceError:
        pass
      else:
        raise AssertionError('getter bound modifiable')
  _bad = Model.from_values(_base12(), order_scope_reference_private='scope-a', failure_catalogue=(_OPAQUE_CODE,))
  del _bad.__dict__['revision']
  with mock.patch.object(Model.objects, 'using', return_value=_FakeQS(_bad)):
    with mock.patch.object(EnvModel.objects, 'using', side_effect=AssertionError('envelope non autorise')):
      try:
        _repo.get_publication(event_id='evt-test-001', failure_catalogue=(_OPAQUE_CODE,))
      except ValidationError:
        pass
      else:
        raise AssertionError('ligne malformee avant envelope absente')
  with mock.patch.object(Model.objects, 'using', return_value=_FakeQS(_grow)):
    with mock.patch.object(EnvModel.objects, 'using', return_value=_FakeQS({'event_id': 'evt-test-001', 'order_scope_reference': 'scope-b'})):
      try:
        _repo.get_publication(event_id='evt-test-001', failure_catalogue=(_OPAQUE_CODE,))
      except ValidationError:
        pass
      else:
        raise AssertionError('scope incoherent accepte')
  from types import SimpleNamespace as _NS
  def _mkexc(sqlstate, constraint, table):
    _cause = Exception('synthetic db cause')
    _cause.sqlstate = sqlstate
    _cause.diag = _NS(constraint_name=constraint, table_name=table)
    _e = IntegrityError('conflit')
    _e.__cause__ = _cause
    return _e
  assert repo_mod._is_counter_pk_conflict(_mkexc('23505', 'backend_bulkoutboxscopecounterrecord_pkey', 'backend_bulkoutboxscopecounterrecord')) is True
  assert repo_mod._is_counter_pk_conflict(_mkexc('23503', 'backend_bulkoutboxscopecounterrecord_pkey', 'backend_bulkoutboxscopecounterrecord')) is False
  assert repo_mod._is_counter_pk_conflict(_mkexc('23505', 'autre_contrainte', 'backend_bulkoutboxscopecounterrecord')) is False
  assert repo_mod._is_counter_pk_conflict(_mkexc('23505', 'backend_bulkoutboxscopecounterrecord_pkey', 'autre_table')) is False
  assert repo_mod._is_counter_pk_conflict(IntegrityError('x')) is False
  class _EvilStr(IntegrityError):
    def __str__(self): raise AssertionError('str interdit')
  _evil = _EvilStr('x'); _evil.__cause__ = None
  assert repo_mod._is_counter_pk_conflict(_evil) is False
  import inspect
  assert list(inspect.signature(_capture).parameters) == ['candidate']
  assert list(inspect.signature(_values_pre.validate_bulk_outbox_publication_values).parameters) == ['candidate']
  _sig = inspect.signature(BulkOutboxPublicationRepository.insert_initial)
  _source_names = ['event_id', 'state', 'attempt_count', 'lease_owner', 'lease_expires_at', 'next_attempt_at', 'published_at', 'failure_code', 'policy_reference', 'policy_version', 'revision', 'failure_catalogue']
  assert list(_sig.parameters) == ['self'] + _source_names
  assert all(_sig.parameters[n].default is inspect.Parameter.empty for n in _source_names)
  assert _cmap['scope_private'].db_collation == 'C'
  assert all(type(f) is models.TextField and not f.has_default() for f in Counter._meta.local_fields)
  for _badtext in ('1' + chr(10), chr(10) + '1', '1' + chr(10) + '1', '0'):
    _r = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
    _r.__dict__['sequence_index'] = _badtext
    _refused(lambda _r=_r: _r.as_values())
  for _fld in ('event_id', 'state', 'policy_reference', 'policy_version'):
    _refused(lambda _fld=_fld: Model.from_values(_base12(**{_fld: S('value')}), order_scope_reference_private='scope-test', failure_catalogue=()))
  _refused(lambda: _capture_catalogue((S('failure'),)))
  _refused(lambda: _capture_catalogue((Hostile(),)))
  assert _capture_catalogue(frozenset()) == ()
  assert _repo._validated_source(**_source11(), failure_catalogue=())[0].revision == 7
  _all_exclude = [f.name for f in Model._meta.local_fields]
  _badclean = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  _badclean.__dict__['state'] = 'INVALID'
  _refused(lambda: _badclean.full_clean(exclude=_all_exclude))
  _deferred = Model.from_values(_base12(), order_scope_reference_private='scope-test', failure_catalogue=())
  del _deferred.__dict__['event_id']
  _refused(lambda: _deferred.full_clean(exclude=_all_exclude))
  with mock.patch.object(Model.objects, 'using', return_value=_FakeQS(None)):
    assert _repo.get_publication(event_id='missing-synthetic', failure_catalogue=frozenset()) is None
  with mock.patch.object(transaction, 'get_connection', side_effect=AssertionError('source must be rejected before connection')):
    for _over in ({'event_id': Hostile()}, {'revision': True}, {'attempt_count': 1}, {'policy_version': '1.2'}):
      _refused(lambda _over=_over: _repo.insert_initial(**_source11(**_over), failure_catalogue=()))
  _owned = _base12()
  _owned_row = Model.from_values(_owned, order_scope_reference_private='scope-test', failure_catalogue=())
  _owned['revision'] = 88
  _snapshot = _owned_row.as_values()
  _snapshot['revision'] = 99
  assert _owned_row.as_values()['revision'] == 7
  assert counters == {'db': 0, 'network': 0, 'process': 0, 'file': 0}, counters
  assert _sys.get_int_max_str_digits() == 640
  print('BULK_OUTBOX_INITIAL_OFFLINE_SAFE_OK')
'''

class BulkOutboxInitialOfflineTests(unittest.TestCase):
  def test_offline_guards_and_persistence(self):
    result = subprocess.run([sys.executable, '-X', 'int_max_str_digits=640', '-c', _CHILD, _SRC], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=30, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout, _MARKER + chr(10))
    self.assertEqual(result.stderr, '')

if __name__ == '__main__':
  unittest.main()
