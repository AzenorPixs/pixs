'''Preuves PostgreSQL isolees EventEnvelope B11 ; import et tests ordinaires inertes.'''
import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
_SRC = str(_ROOT / 'src')
_TARGET = str(Path(__file__).resolve())
_EXPECTED_ROOT = '/home/devops/datas/pixs'
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONDONTWRITEBYTECODE': '1'}
_FLAGS = ('search_path_isolated', 'forward_applied', 'physical_exact', 'roundtrip_nul', 'roundtrip_scalars', 'utc_trusted', 'owned_copies', 'tx_required', 'alias_required', 'co_commit', 'co_rollback', 'duplicate_no_overwrite', 'caught_duplicate_rollback', 'other_integrity_propagates', 'race_one_creation_one_duplicate', 'thread_conns_closed', 'sql_constraints', 'save_hydrated_refused', 'get_none_guarded', 'decoder_malformed_refused', 'reverse_only_0007', 'existing_tables_stable', 'public_tables_stable')
_BASE_TABLES = ('backend_featureflagsourcesnapshotrecord', 'backend_jobrecord', 'backend_bulkoperationrecord', 'backend_bulkoperationexecutionrecord', 'backend_bulkcheckpointrecord', 'backend_bulkjobbindingrecord', 'backend_bulkjobschedulerecord', 'backend_bulkadmissionidentityrecord', 'backend_bulkcommandidempotencyrecord')
_TARGET_TABLE = 'backend_bulkeventenveloperecord'
_CHILD = textwrap.dedent(r'''
    import builtins
    import importlib.util
    import os
    import socket
    import subprocess
    import sys
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock
    src_path = sys.argv[1]
    target_path = sys.argv[2]
    sys.path.insert(0, src_path)
    import django
    import psycopg
    from django.apps import apps
    from django.conf import settings
    from django.db import connection
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from psycopg import Connection
    assert settings.configured is False
    assert apps.ready is False
    guard_targets = ((psycopg, 'connect', ()), (Connection, 'connect', ()), (PGWrapper, 'get_new_connection', (object(), {})), (socket.socket, 'connect', (object(), ('127.0.0.1', 0))), (socket, 'create_connection', (('127.0.0.1', 0),)), (subprocess, 'Popen', (['true'],)), (subprocess, 'run', (['true'],)), (builtins, 'open', ('project.env', 'rb')), (Path, 'open', (Path('project.env'), 'rb')), (os, 'open', ('project.env', os.O_RDONLY)))
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in guard_targets]
    with ExitStack() as stack:
        for (target, name, _a), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))
        spec = importlib.util.spec_from_file_location('envelope_pg_harness_under_test', target_path)
        harness = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(harness)
        for (target, name, args), guard in zip(guard_targets, guards):
            try:
                getattr(target, name)(*args)
            except AssertionError:
                pass
            else:
                raise AssertionError('garde inactive')
            assert guard.call_count == 1
            guard.reset_mock()
        assert callable(harness.run_real_bulk_event_envelope_postgres)
        for bad_root in (None, '', 0, b'/home/devops/datas/pixs'):
            outcome = harness.run_real_bulk_event_envelope_postgres(bad_root)
            assert outcome['real_pg'] is False
            assert outcome['phase'] == 'COMPLETE'
            assert outcome['reason'] == 'ROOT_INVALID'
        outcome = harness.run_real_bulk_event_envelope_postgres('/synthetic/root')
        assert outcome['reason'] == 'ROOT_MISMATCH'
        assert outcome['real_pg'] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [g.call_count for g in guards] == [0] * len(guards)
    print('BULK_EVENT_ENVELOPE_PG_HARNESS_SAFE_OK')
    ''').strip()
_MARKER = 'BULK_EVENT_ENVELOPE_PG_HARNESS_SAFE_OK' + chr(10)
def _helpers():
    integration = str(_ROOT / 'tests' / 'integration')
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration
def _outcome():
    return {'real_pg': False, 'phase': 'COMPLETE', 'reason': 'NONE', 'cleanup_ok': False, 'conns_closed': False, 'server_version_num': None, 'test_schema': None, 'schema_owned': False, **{k: False for k in _FLAGS}}
def _body(result, h, state, refs, failures):
    import math
    import time
    import django
    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime, timezone, timedelta
    from threading import Barrier, Lock
    from django.apps import apps
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connection, transaction
    from django.db.migrations.executor import MigrationExecutor
    from django.db.transaction import TransactionManagementError
    from psycopg import sql
    result['phase'] = 'SCHEMA'
    with h._managed_pg_connection(*state['credentials'], refs, failures) as admin:
        result['server_version_num'] = int(h._scalar(admin, 'SHOW server_version_num', ()))
        state['public_before'] = [h._table_identity(admin, 'public', t) for t in (*state['tables'], _TARGET_TABLE, 'django_migrations')]
        state['schema'] = h._safe_schema_name()
        state['owned'], reason = h._create_schema(admin, state['schema'])
        if reason != 'NONE' or not state['owned']:
            result['reason'] = reason
            return
        search_path = h._quote_search_path(admin, state['schema'])
    if settings.configured:
        result['reason'] = 'SETTINGS_ALREADY_CONFIGURED'
        return
    database, user, password = state['credentials']
    db_config = {'ENGINE': 'django.db.backends.postgresql', 'NAME': database, 'USER': user, 'PASSWORD': password, 'HOST': '127.0.0.1', 'PORT': '5432', 'OPTIONS': {'options': h._pg_options(search_path), 'connect_timeout': 2}, 'CONN_MAX_AGE': 0}
    settings.configure(INSTALLED_APPS=['pixs.backend'], SECRET_KEY='bulk-envelope-synthetic-test', DATABASES={'default': db_config, 'other': dict(db_config)}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state['configured'] = True
    django.setup()
    if h._scalar(connection, 'SELECT current_schemas(false)', ()) != [state['schema'], 'pg_catalog']:
        result['reason'] = 'SEARCH_PATH_MISMATCH'
        return
    refs.append(connection.connection)
    result['search_path_isolated'] = True
    from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord as Model
    from pixs.backend.bulk_event_envelope_repository import BulkEventEnvelopeDuplicate, BulkEventEnvelopeRefused, BulkEventEnvelopeRepository
    CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    def _valid(**over):
        base = {'event_id': 'event-test', 'kind': 'DOMAIN', 'event_type': 'type-test', 'event_version': '1.2.3', 'producer_reference': 'producer-test', 'schema_reference': 'schema-test', 'order_scope_reference': 'scope-test', 'occurred_at': CREATED, 'subject_reference': 'subject-test', 'tenant_context_reference': 'tenant-test', 'correlation_id': 'correlation-test', 'causation_id': None, 'payload': {'name': 'value'}}
        base.update(over)
        return base
    def _limits(**over):
        base = {'max_depth': 8, 'max_members': 10, 'non_tenant_authorized': False}
        base.update(over)
        return base
    lim = _limits()
    def table_query(template):
        return sql.SQL(template).format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection)

    result['phase'] = 'MIGRATION'
    MigrationExecutor(connection).migrate([('backend', '0006_bulk_command_idempotency')])
    before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert all(before) and len(state['tables']) == 9
    MigrationExecutor(connection).migrate([('backend', '0007_bulk_event_envelope')])
    assert h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0007_bulk_event_envelope') == 1
    result['forward_applied'] = True
    with connection.cursor() as cur:
        cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position', (state['schema'], _TARGET_TABLE))
        cols = cur.fetchall()
    assert [c[0] for c in cols] == ['event_id', 'kind', 'event_type', 'event_version', 'producer_reference', 'schema_reference', 'order_scope_reference', 'occurred_at', 'subject_reference', 'tenant_context_reference', 'correlation_id', 'causation_id', 'payload']
    assert all(c[1] == ('timestamp with time zone' if c[0] == 'occurred_at' else 'text') for c in cols)
    with connection.cursor() as cur:
        cur.execute('SELECT conname, contype FROM pg_constraint JOIN pg_class ON pg_class.oid = conrelid JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace WHERE pg_namespace.nspname = %s AND pg_class.relname = %s', (state['schema'], _TARGET_TABLE))
        cons = cur.fetchall()
    assert {c[0] for c in cons if c[1] == 'c'} == {'bulkeventenvelope_type_non_empty', 'bulkeventenvelope_version_non_empty', 'bulkeventenvelope_producer_non_empty', 'bulkeventenvelope_event_non_empty', 'bulkeventenvelope_kind_member', 'bulkeventenvelope_payload_non_empty', 'bulkeventenvelope_schema_non_empty', 'bulkeventenvelope_scope_non_empty', 'bulkeventenvelope_correlation_non_empty', 'bulkeventenvelope_tenant_non_empty', 'bulkeventenvelope_causation_non_empty', 'bulkeventenvelope_subject_non_empty'}
    assert [c[0] for c in cons if c[1] == 'p'] == [_TARGET_TABLE + '_pkey']
    result['physical_exact'] = True
    result['phase'] = 'ROUNDTRIP'
    nul_key = 'a' + chr(0) + 'b'
    nul_val = 'x' + chr(0) + 'y'
    uni = 'e' + chr(0xE9) + chr(0x1F600)
    repo = BulkEventEnvelopeRepository(using='default')
    with transaction.atomic(using='default'):
        Model.from_values(_valid(event_id='rt-nul', payload={nul_key: nul_val}), **lim).save(force_insert=True, using='default')
        got = repo.get_envelope(event_id='rt-nul', **lim)
        assert got.as_values()['payload'] == {nul_key: nul_val}
        from types import MappingProxyType
        from dataclasses import FrozenInstanceError
        assert type(got.payload) is MappingProxyType
        try:
            got.payload[nul_key] = 'changed'
        except TypeError:
            pass
        else:
            raise AssertionError('payload non gele')
        try:
            got.event_id = 'changed'
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('snapshot non gele')
        exported = got.as_values()
        exported['payload'][nul_key] = 'changed'
        assert got.as_values()['payload'] == {nul_key: nul_val}
    result['roundtrip_nul'] = True
    with transaction.atomic(using='default'):
        for idx, payload in enumerate((None, False, True, '', uni, 0, -1, 1.25, [], [None, True, 2, ''], {}, {'a': [1, {'b': None}]})):
            eid = 'rt-s-' + str(idx)
            Model.from_values(_valid(event_id=eid, payload=payload), **lim).save(force_insert=True, using='default')
            assert repo.get_envelope(event_id=eid, **lim).as_values()['payload'] == payload
        neg = Model.from_values(_valid(event_id='rt-neg0', payload=-0.0), **lim)
        neg.save(force_insert=True, using='default')
        assert math.copysign(1.0, repo.get_envelope(event_id='rt-neg0', **lim).as_values()['payload']) == -1.0
        big = 10 ** 600
        Model.from_values(_valid(event_id='rt-big', payload=big), **lim).save(force_insert=True, using='default')
        assert repo.get_envelope(event_id='rt-big', **lim).as_values()['payload'] == big
    result['roundtrip_scalars'] = True
    with transaction.atomic(using='default'):
        row = Model.from_values(_valid(event_id='rt-utc'), **lim)
        row.save(force_insert=True, using='default')
        fetched = repo.get_envelope(event_id='rt-utc', **lim)
        assert fetched.as_values()['occurred_at'] == CREATED and fetched.as_values()['occurred_at'].tzinfo is timezone.utc
    result['utc_trusted'] = True
    with transaction.atomic(using='default'):
        caller = _valid(event_id='rt-owned')
        r = Model.from_values(caller, **lim)
        caller['event_id'] = 'mute'
        caller['payload']['name'] = 'mute'
        r.save(force_insert=True, using='default')
        out = r.as_values(**lim)
        out['payload']['name'] = 'changed'
        assert r.as_values(**lim)['payload'] == {'name': 'value'}
        assert type(r._locked_snapshot(**lim).payload) is MappingProxyType
    result['owned_copies'] = True
    result['phase'] = 'TX'
    try:
        Model.from_values(_valid(event_id='tx-noatomic'), **lim).save(force_insert=True, using='default')
    except ValidationError:
        pass
    else:
        raise AssertionError('tx active requise')
    try:
        repo.insert_envelope(values=_valid(event_id='tx-norepo'), **lim)
    except BulkEventEnvelopeRefused:
        pass
    else:
        raise AssertionError('repo tx requise')
    result['tx_required'] = True
    try:
        BulkEventEnvelopeRepository(using='')
    except ValidationError:
        pass
    else:
        raise AssertionError('alias requis')
    try:
        Model.from_values(_valid(event_id='tx-badalias'), **lim).save(force_insert=True, using='')
    except ValidationError:
        pass
    else:
        raise AssertionError('alias save requis')
    with transaction.atomic(using='default'):
        try:
            BulkEventEnvelopeRepository(using='other').insert_envelope(values=_valid(event_id='other-no-owner'), **lim)
        except BulkEventEnvelopeRefused:
            pass
        else:
            raise AssertionError('transaction autre alias refusee')
        try:
            Model.from_values(_valid(event_id='other-model'), **lim).save(force_insert=True, using='other')
        except ValidationError:
            pass
        else:
            raise AssertionError('save autre alias refuse')
    assert repo.get_envelope(event_id='other-no-owner', **lim) is None
    assert repo.get_envelope(event_id='other-model', **lim) is None
    result['alias_required'] = True
    with connection.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS synthetic_owner_effect (id TEXT PRIMARY KEY, val TEXT)')
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-ok', 'v'])
        repo.insert_envelope(values=_valid(event_id='co-ok'), **lim)
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-ok'])
        assert cur.fetchone()[0] == 1
    assert repo.get_envelope(event_id='co-ok', **lim) is not None
    result['co_commit'] = True
    try:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-rb', 'v'])
            repo.insert_envelope(values=_valid(event_id='co-rb'), **lim)
            raise RuntimeError('panne proprietaire')
    except RuntimeError:
        pass
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-rb'])
        assert cur.fetchone()[0] == 0
    assert repo.get_envelope(event_id='co-rb', **lim) is None
    result['co_rollback'] = True
    with transaction.atomic(using='default'):
        repo.insert_envelope(values=_valid(event_id='dup-one', payload={'name': 'one'}), **lim)
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-before-dup', 'v'])
        try:
            repo.insert_envelope(values=_valid(event_id='dup-one', payload={'name': 'two'}), **lim)
        except BulkEventEnvelopeDuplicate:
            assert transaction.get_rollback(using='default') is True
            try:
                with connection.cursor() as cur2:
                    cur2.execute('SELECT 1')
            except TransactionManagementError:
                pass
            else:
                raise AssertionError('rollback owner attendu')
        else:
            raise AssertionError('duplicate attendu')
    assert repo.get_envelope(event_id='dup-one', **lim).as_values()['payload'] == {'name': 'one'}
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-before-dup'])
        assert cur.fetchone()[0] == 0
    result['duplicate_no_overwrite'] = True
    result['caught_duplicate_rollback'] = True
    with connection.cursor() as cur:
        cur.execute(table_query("ALTER TABLE {}.{} ADD CONSTRAINT tmp_owned_check CHECK (event_id <> 'never-hit-tmp')"))
    try:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-check-failure', 'v'])
            try:
                repo.insert_envelope(values=_valid(event_id='never-hit-tmp'), **lim)
            except IntegrityError as exc:
                assert getattr(exc.__cause__, 'sqlstate', None) == '23514'
                assert transaction.get_rollback(using='default') is True
            else:
                raise AssertionError('erreur CHECK attendue et propagee')
        assert repo.get_envelope(event_id='never-hit-tmp', **lim) is None
        with connection.cursor() as cur:
            cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-check-failure'])
            assert cur.fetchone()[0] == 0
    finally:
        with connection.cursor() as cur:
            cur.execute(table_query('ALTER TABLE {}.{} DROP CONSTRAINT tmp_owned_check'))
    result['other_integrity_propagates'] = True
    result['phase'] = 'RACE'
    with connection.cursor() as cur:
        cur.execute('SELECT c.oid FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = %s AND c.relname = %s', [state['schema'], _TARGET_TABLE])
        relation_oid = cur.fetchone()[0]
    race_barrier = Barrier(3)
    race_pids, race_refs = [], []
    race_lock = Lock()
    def race_worker(idx):
        from django.db import connections as worker_connections
        wrapper = worker_connections['default']
        try:
            wrapper.ensure_connection()
            with wrapper.cursor() as cur:
                cur.execute('SELECT pg_backend_pid()')
                pid = cur.fetchone()[0]
            with race_lock:
                race_pids.append(pid)
                race_refs.append(wrapper.connection)
                refs.append(wrapper.connection)
            with transaction.atomic(using='default'):
                with wrapper.cursor() as cur:
                    cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['race-owner-' + str(idx), 'v'])
                race_barrier.wait(timeout=5)
                try:
                    snapshot = repo.insert_envelope(values=_valid(event_id='race-one', payload={'w': idx}), **lim)
                except BulkEventEnvelopeDuplicate:
                    assert transaction.get_rollback(using='default') is True
                    outcome = 'duplicate'
                else:
                    assert snapshot.as_values()['payload'] == {'w': idx}
                    outcome = 'created'
            return idx, outcome
        finally:
            try:
                wrapper.close()
            except Exception:
                failures.append('RACE_CLOSE_FAILED')
                raise
    with ThreadPoolExecutor(max_workers=2) as pool:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute(table_query('LOCK TABLE {}.{} IN SHARE MODE'))
            futures = [pool.submit(race_worker, i) for i in (0, 1)]
            race_barrier.wait(timeout=5)
            deadline = time.monotonic() + 1
            seen_blocked = False
            while time.monotonic() < deadline:
                with connection.cursor() as cur:
                    cur.execute('SELECT pid, granted FROM pg_locks WHERE locktype = %s AND relation = %s AND mode = %s', ['relation', relation_oid, 'RowExclusiveLock'])
                    rows = cur.fetchall()
                with race_lock:
                    pids = tuple(race_pids)
                if len([row for row in rows if row[0] in pids and row[1] is False]) == 2:
                    seen_blocked = True
                    break
                time.sleep(0.01)
            assert seen_blocked, 'deux workers reellement bloques attendus'
        outcomes = [f.result(timeout=10) for f in futures]
    assert sorted(value for idx, value in outcomes) == ['created', 'duplicate']
    winner = next(idx for idx, value in outcomes if value == 'created')
    assert Model.objects.using('default').filter(event_id='race-one').count() == 1
    assert repo.get_envelope(event_id='race-one', **lim).as_values()['payload'] == {'w': winner}
    with connection.cursor() as cur:
        cur.execute('SELECT id FROM synthetic_owner_effect WHERE id IN (%s, %s)', ['race-owner-0', 'race-owner-1'])
        assert cur.fetchall() == [('race-owner-' + str(winner),)]
    assert len(race_refs) == 2 and all(conn.closed for conn in race_refs)
    result['race_one_creation_one_duplicate'] = True
    result['thread_conns_closed'] = True
    result['phase'] = 'CONSTRAINTS'
    raw_fields = ['event_id', 'kind', 'event_type', 'event_version', 'producer_reference', 'schema_reference', 'order_scope_reference', 'occurred_at', 'subject_reference', 'tenant_context_reference', 'correlation_id', 'causation_id', 'payload']
    for idx, field in enumerate(raw_fields):
        if field == 'occurred_at':
            continue
        raw = _valid(event_id='sql-check-' + str(idx), payload='{}')
        raw[field] = 'INVALID' if field == 'kind' else ''
        try:
            with transaction.atomic(using='default'):
                with connection.cursor() as cur:
                    query = table_query('INSERT INTO {}.{} (event_id,kind,event_type,event_version,producer_reference,schema_reference,order_scope_reference,occurred_at,subject_reference,tenant_context_reference,correlation_id,causation_id,payload) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                    cur.execute(query, [raw[name] for name in raw_fields])
        except IntegrityError as exc:
            assert getattr(exc.__cause__, 'sqlstate', None) == '23514'
        else:
            raise AssertionError('contrainte SQL attendue')
    result['sql_constraints'] = True
    hyd = Model.from_values(_valid(event_id='hyd-one'), **lim)
    with transaction.atomic(using='default'):
        hyd.save(force_insert=True, using='default')
    hyd = Model.objects.using('default').get(pk='hyd-one')
    original_hyd = repo.get_envelope(event_id='hyd-one', **lim).as_values()
    hyd.event_id = 'hyd-moved'
    try:
        hyd.save(force_insert=True, using='default')
    except ValidationError:
        pass
    else:
        raise AssertionError('hydrate refuse')
    assert repo.get_envelope(event_id='hyd-one', **lim).as_values() == original_hyd
    assert repo.get_envelope(event_id='hyd-moved', **lim) is None
    result['save_hydrated_refused'] = True
    assert repo.get_envelope(event_id='missing-none', **lim) is None
    try:
        repo.get_envelope(event_id='', **lim)
    except BulkEventEnvelopeRefused:
        pass
    else:
        raise AssertionError('get guard')
    result['get_none_guarded'] = True
    bad = Model.from_values(_valid(event_id='dec-one'), **lim)
    with transaction.atomic(using='default'):
        bad.save(force_insert=True, using='default')
    for malformed in ('{oops', 'NaN', '{"a":1,"a":2}'):
        with connection.cursor() as cur:
            cur.execute(table_query('UPDATE {}.{} SET payload = %s WHERE event_id = %s'), [malformed, 'dec-one'])
        try:
            repo.get_envelope(event_id='dec-one', **lim)
        except BulkEventEnvelopeRefused:
            pass
        else:
            raise AssertionError('decode malforme refuse')
    result['decoder_malformed_refused'] = True
    result['phase'] = 'REVERSE'
    MigrationExecutor(connection).migrate([('backend', '0006_bulk_command_idempotency')])
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0007_bulk_event_envelope') == 0
    result['reverse_only_0007'] = True
    result['existing_tables_stable'] = before == [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    result['phase'] = 'COMPLETE'
def run_real_bulk_event_envelope_postgres(root_str):
    result = _outcome()
    if type(root_str) is not str or not root_str:
        result['reason'] = 'ROOT_INVALID'
        return result
    if str(Path(root_str).resolve()) != _EXPECTED_ROOT:
        result['reason'] = 'ROOT_MISMATCH'
        return result
    h = _helpers()
    refs, failures = [], []
    state = {'credentials': None, 'schema': None, 'owned': False, 'configured': False, 'public_before': None, 'tables': _BASE_TABLES}
    with h._mask_output():
        try:
            found = h._read_project_env(root_str)
            if type(found) is not dict:
                result['reason'] = 'ENV_REFUSED'
            else:
                credentials = tuple(found.get(n) for n in ('PG_DATABASE', 'PG_USERNAME', 'PG_PASSWORD'))
                del found
                if any(type(v) is not str or not v for v in credentials):
                    result['reason'] = 'ENV_INCOMPLETE'
                else:
                    state['credentials'] = credentials
                    del credentials
                    _body(result, h, state, refs, failures)
        except BaseException:
            result['reason'] = 'TEST_FAILED'
        finally:
            try:
                if state['configured']:
                    from django.db import connections as local_conns
                    local_conns.close_all()
                if state['credentials'] is not None:
                    with h._managed_pg_connection(*state['credentials'], refs, failures) as admin:
                        if state['public_before'] is not None:
                            result['public_tables_stable'] = state['public_before'] == [h._table_identity(admin, 'public', t) for t in (*state['tables'], _TARGET_TABLE, 'django_migrations')]
                        if state['owned']:
                            result['cleanup_ok'] = h._drop_schema_if_owned(admin, state['schema'], True)
                        else:
                            result['cleanup_ok'] = False
                else:
                    result['cleanup_ok'] = False
                result['conns_closed'] = bool(refs) and not failures and all(bool(c.closed) for c in refs)
                if state['configured']:
                    from django.db import connections as local_conns2
                    result['conns_closed'] = result['conns_closed'] and all(w.connection is None for w in local_conns2.all())
            except BaseException:
                result['reason'] = 'FINALIZATION_FAILED'
                result['cleanup_ok'] = result['conns_closed'] = False
    result['test_schema'] = state['schema']
    result['schema_owned'] = state['owned']
    result['real_pg'] = bool(result['reason'] == 'NONE' and result['cleanup_ok'] and result['conns_closed'] and all(result[k] for k in _FLAGS))
    if not result['real_pg'] and result['reason'] == 'NONE':
        result['reason'] = 'FLAGS_INCOMPLETE'
    allowed = {'real_pg', 'phase', 'reason', 'cleanup_ok', 'conns_closed', 'server_version_num', 'test_schema', 'schema_owned', *_FLAGS}
    return {k: result[k] for k in allowed}
class BulkEventEnvelopePostgresInertTests(unittest.TestCase):
    def test_harness_safe(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-c', _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)
        self.assertEqual(result.stderr, '')
if __name__ == '__main__':
    unittest.main()
