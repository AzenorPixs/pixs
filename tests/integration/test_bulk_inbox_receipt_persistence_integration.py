"""Preuves PostgreSQL de la fondation Inbox, sans receiver ni ack.

Contrat Job de fixture pixs.inbox.synthetic 1.0.0 seulement : payload
références synthétiques, aucun handler/worker/autorité de production.
"""
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
_FLAGS = ('search_path_isolated', 'forward_applied', 'physical_exact', 'roundtrip_8', 'unicode_chr', 'utc_trusted', 'frozen_owned', 'consumer_independent', 'duplicate_identical', 'divergence_sha', 'divergence_version', 'originals_preserved', 'caught_rollback', 'co_commit', 'co_rollback', 'inflight_not_ack', 'same_tx_rollback', 'race_one_creation_one_duplicate', 'thread_conns_closed', 'sql_constraints', 'hydrated_refused', 'alias_other_refused', 'other_integrity_propagates', 'reverse_only_0008', 'existing_tables_stable', 'public_tables_stable')
_BASE_TABLES = ('backend_featureflagsourcesnapshotrecord', 'backend_jobrecord', 'backend_bulkoperationrecord', 'backend_bulkoperationexecutionrecord', 'backend_bulkcheckpointrecord', 'backend_bulkjobbindingrecord', 'backend_bulkjobschedulerecord', 'backend_bulkadmissionidentityrecord', 'backend_bulkcommandidempotencyrecord', 'backend_bulkeventenveloperecord')
_TARGET_TABLE = 'backend_bulkinboxreceiptrecord'
def _helpers():
    integration = str(_ROOT / 'tests' / 'integration')
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration
def _outcome():
    return {'real_pg': False, 'phase': 'COMPLETE', 'reason': 'NONE', 'cleanup_ok': False, 'conns_closed': False, 'server_version_num': None, 'test_schema': None, 'schema_owned': False, **{k: False for k in _FLAGS}}
def _export_bound(bound):
    return {k: getattr(bound, k) for k in ('consumer_reference', 'event_id', 'event_version', 'content_sha256', 'state', 'consumed_at', 'correlation_id', 'causation_id')}
def _body(result, h, state, refs, failures):
    import time
    import django
    from concurrent.futures import ThreadPoolExecutor
    from dataclasses import FrozenInstanceError
    from datetime import datetime, timezone
    from threading import Barrier, Lock
    from django.conf import settings
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, connection, connections, transaction
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
    settings.configure(INSTALLED_APPS=['pixs.backend'], SECRET_KEY='bulk-inbox-synthetic-test', DATABASES={'default': db_config, 'other': dict(db_config)}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state['configured'] = True
    django.setup()
    if h._scalar(connection, 'SELECT current_schemas(false)', ()) != [state['schema'], 'pg_catalog']:
        result['reason'] = 'SEARCH_PATH_MISMATCH'
        return
    refs.append(connection.connection)
    result['search_path_isolated'] = True
    from pixs.backend.bulk_inbox_receipt_record import BulkInboxReceiptRecord as Model
    from pixs.backend.bulk_inbox_receipt_repository import BulkInboxReceiptDivergence, BulkInboxReceiptDuplicate, BulkInboxReceiptRefused, BulkInboxReceiptRepository
    from pixs.backend.models import JobRecord
    CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    SHA_A = '0f' * 32
    SHA_B = 'f0' * 32
    def _valid(**over):
        base = {'consumer_reference': 'consumer-test', 'event_id': 'event-test', 'event_version': '1.2.3', 'content_sha256': SHA_A, 'state': 'CONSUMED', 'consumed_at': CREATED, 'correlation_id': 'correlation-test', 'causation_id': None}
        base.update(over)
        return base
    def _job_values(jid):
        return {'job_id': jid, 'job_type': 'pixs.inbox.synthetic', 'job_version': '1.0.0', 'payload': {'event_reference': 'synthetic-event', 'consumer_reference': 'synthetic-consumer'}, 'subject': {'requested_by_reference': 'sujet-resolu'}, 'tenant_context': {'tenant_context_reference': 'tenant-resolu'}, 'correlation_id': 'corr-test', 'causation_id': 'cause-test', 'perimeter_reference': 'perim-test', 'state': 'PENDING', 'attempt_count': 0, 'lease_owner': None, 'lease_expires_at': None}
    def _create_job(jid):
        # Contrat de fixture synthétique, aucun handler/worker de production.
        job = JobRecord(**_job_values(jid))
        job.full_clean(validate_unique=False, validate_constraints=False)
        job.save(force_insert=True, using='default')
    def _owner_count(key, wrapper=connection):
        with wrapper.cursor() as cur:
            cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', [key])
            return cur.fetchone()[0]
    result['phase'] = 'MIGRATION'
    MigrationExecutor(connection).migrate([('backend', '0007_bulk_event_envelope')])
    before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert all(before) and len(state['tables']) == 10
    MigrationExecutor(connection).migrate([('backend', '0008_bulk_inbox_receipt')])
    assert h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0008_bulk_inbox_receipt') == 1
    result['forward_applied'] = True
    with connection.cursor() as cur:
        cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position', (state['schema'], _TARGET_TABLE))
        cols = cur.fetchall()
    assert [c[0] for c in cols] == ['id', 'consumer_reference', 'event_id', 'event_version', 'content_sha256', 'state', 'consumed_at', 'correlation_id', 'causation_id']
    types = {c[0]: c[1] for c in cols}
    assert types['id'] == 'bigint'
    assert types['consumed_at'] == 'timestamp with time zone'
    assert all(types[k] == 'text' for k in ('consumer_reference', 'event_id', 'event_version', 'content_sha256', 'state', 'correlation_id', 'causation_id'))
    with connection.cursor() as cur:
        cur.execute('SELECT conname, contype FROM pg_constraint JOIN pg_class ON pg_class.oid = conrelid JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace WHERE pg_namespace.nspname = %s AND pg_class.relname = %s', (state['schema'], _TARGET_TABLE))
        cons = cur.fetchall()
    assert {c[0] for c in cons if c[1] == 'c'} == {'bulkinboxreceipt_consumer_non_empty', 'bulkinboxreceipt_event_non_empty', 'bulkinboxreceipt_version_non_empty', 'bulkinboxreceipt_digest_non_empty', 'bulkinboxreceipt_digest_regex', 'bulkinboxreceipt_state_member', 'bulkinboxreceipt_correlation_non_empty', 'bulkinboxreceipt_causation_non_empty'}
    assert [c[0] for c in cons if c[1] == 'p'] == [_TARGET_TABLE + '_pkey']
    assert [c[0] for c in cons if c[1] == 'u'] == ['bulkinboxreceipt_consumer_event_unique']
    result['physical_exact'] = True
    result['phase'] = 'ROUNDTRIP'
    repo = BulkInboxReceiptRepository(using='default')
    with transaction.atomic(using='default'):
        bound = repo.insert_receipt(values=_valid(event_id='rt-8', causation_id=None))
        assert not hasattr(bound, 'as_values')
        exported = _export_bound(bound)
        assert exported == _valid(event_id='rt-8', causation_id=None)
        assert type(exported['consumed_at']) is datetime
        fetched = repo.get_receipt(consumer_reference='consumer-test', event_id='rt-8')
        assert _export_bound(fetched) == exported
        try:
            fetched.state = 'X'
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('bound non gele')
        mutated = _export_bound(fetched)
        mutated['event_id'] = 'mute'
        assert _export_bound(repo.get_receipt(consumer_reference='consumer-test', event_id='rt-8'))['event_id'] == 'rt-8'
    result['roundtrip_8'] = True
    result['frozen_owned'] = True
    with transaction.atomic(using='default'):
        uni = 'e' + chr(0xE9)
        b = repo.insert_receipt(values=_valid(event_id='rt-uni', consumer_reference=uni, correlation_id=uni))
        assert _export_bound(repo.get_receipt(consumer_reference=uni, event_id='rt-uni'))['consumer_reference'] == uni
    result['unicode_chr'] = True
    with transaction.atomic(using='default'):
        repo.insert_receipt(values=_valid(event_id='rt-utc'))
        got = repo.get_receipt(consumer_reference='consumer-test', event_id='rt-utc')
        assert got.consumed_at == CREATED and got.consumed_at.tzinfo is timezone.utc
    result['utc_trusted'] = True
    with transaction.atomic(using='default'):
        repo.insert_receipt(values=_valid(consumer_reference='consumer-A', event_id='event-1'))
        repo.insert_receipt(values=_valid(consumer_reference='consumer-B', event_id='event-1'))
        assert repo.get_receipt(consumer_reference='consumer-A', event_id='event-1') is not None
        assert repo.get_receipt(consumer_reference='consumer-B', event_id='event-1') is not None
    result['consumer_independent'] = True
    with connection.cursor() as cur:
        cur.execute('CREATE TABLE synthetic_owner_effect (id TEXT PRIMARY KEY, val TEXT)')
    with transaction.atomic(using='default'):
        repo.insert_receipt(values=_valid(consumer_reference='consumer-dup', event_id='event-dup', correlation_id='corr-orig', causation_id='cause-orig', consumed_at=CREATED))
    original_receipt = _export_bound(repo.get_receipt(consumer_reference='consumer-dup', event_id='event-dup'))
    def _refusal_rollback(expected, values, suffix):
        owner_id = 'owner-' + suffix
        job_id = 'job-' + suffix
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', [owner_id, 'v'])
            _create_job(job_id)
            try:
                repo.insert_receipt(values=values)
            except expected:
                assert transaction.get_rollback(using='default') is True
                try:
                    with connection.cursor() as cur:
                        cur.execute('SELECT 1')
                except TransactionManagementError:
                    pass
                else:
                    raise AssertionError('requete sous rollback doit refuser')
            else:
                raise AssertionError('refus exact attendu')
        assert _owner_count(owner_id) == 0
        assert JobRecord.objects.filter(pk=job_id).count() == 0
        assert _export_bound(repo.get_receipt(consumer_reference='consumer-dup', event_id='event-dup')) == original_receipt
    _refusal_rollback(BulkInboxReceiptDuplicate, _valid(consumer_reference='consumer-dup', event_id='event-dup'), 'duplicate')
    result['duplicate_identical'] = True
    result['caught_rollback'] = True
    _refusal_rollback(BulkInboxReceiptDivergence, _valid(consumer_reference='consumer-dup', event_id='event-dup', content_sha256=SHA_B), 'divergence-sha')
    result['divergence_sha'] = True
    _refusal_rollback(BulkInboxReceiptDivergence, _valid(consumer_reference='consumer-dup', event_id='event-dup', event_version='9.9.9'), 'divergence-version')
    result['divergence_version'] = True
    result['originals_preserved'] = True
    with connection.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS synthetic_owner_effect (id TEXT PRIMARY KEY, val TEXT)')
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-ok', 'v'])
        _create_job('job-ok')
        repo.insert_receipt(values=_valid(consumer_reference='consumer-ok', event_id='event-ok'))
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-ok'])
        assert cur.fetchone()[0] == 1
    assert JobRecord.objects.filter(pk='job-ok').count() == 1
    assert repo.get_receipt(consumer_reference='consumer-ok', event_id='event-ok') is not None
    result['co_commit'] = True
    try:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-rb', 'v'])
            _create_job('job-rb')
            repo.insert_receipt(values=_valid(consumer_reference='consumer-rb', event_id='event-rb'))
            raise RuntimeError('panne proprietaire')
    except RuntimeError:
        pass
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-rb'])
        assert cur.fetchone()[0] == 0
    assert JobRecord.objects.filter(pk='job-rb').count() == 0
    assert repo.get_receipt(consumer_reference='consumer-rb', event_id='event-rb') is None
    result['co_rollback'] = True
    other = BulkInboxReceiptRepository(using='other')
    observer = connections['other']
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-inflight', 'v'])
        _create_job('job-inflight')
        inflight = repo.insert_receipt(values=_valid(consumer_reference='consumer-inflight', event_id='event-inflight'))
        assert inflight.state == 'CONSUMED'
        assert other.get_receipt(consumer_reference='consumer-inflight', event_id='event-inflight') is None
        refs.append(observer.connection)
        assert h._scalar(observer, 'SELECT current_schemas(false)', ()) == [state['schema'], 'pg_catalog']
        assert _owner_count('owner-inflight', observer) == 0
        assert JobRecord.objects.using('other').filter(pk='job-inflight').count() == 0
        assert repo.get_receipt(consumer_reference='consumer-inflight', event_id='event-inflight').state == 'CONSUMED'
    assert other.get_receipt(consumer_reference='consumer-inflight', event_id='event-inflight').state == 'CONSUMED'
    assert _owner_count('owner-inflight', observer) == 1
    assert JobRecord.objects.using('other').filter(pk='job-inflight').count() == 1
    result['inflight_not_ack'] = True
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-same', 'v'])
        _create_job('job-same')
        same_snapshot = repo.insert_receipt(values=_valid(consumer_reference='consumer-same', event_id='event-same'))
        assert same_snapshot.state == 'CONSUMED'
        assert other.get_receipt(consumer_reference='consumer-same', event_id='event-same') is None
        try:
            repo.insert_receipt(values=_valid(consumer_reference='consumer-same', event_id='event-same'))
        except BulkInboxReceiptDuplicate:
            assert transaction.get_rollback(using='default') is True
        else:
            raise AssertionError('duplicata propre transaction attendu')
    assert same_snapshot.state == 'CONSUMED'
    assert repo.get_receipt(consumer_reference='consumer-same', event_id='event-same') is None
    assert _owner_count('owner-same') == 0
    assert JobRecord.objects.filter(pk='job-same').count() == 0
    result['same_tx_rollback'] = True
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
                _create_job('job-race-' + str(idx))
                race_barrier.wait(timeout=5)
                try:
                    repo.insert_receipt(values=_valid(consumer_reference='consumer-race', event_id='event-race'))
                except BulkInboxReceiptDuplicate:
                    assert transaction.get_rollback(using='default') is True
                    return idx, 'duplicate'
                else:
                    return idx, 'created'
        finally:
            try:
                wrapper.close()
            except Exception:
                failures.append('RACE_CLOSE_FAILED')
                raise
    with ThreadPoolExecutor(max_workers=2) as pool:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute(sql.SQL('LOCK TABLE {}.{} IN SHARE MODE').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection))
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
    assert Model.objects.using('default').filter(consumer_reference='consumer-race', event_id='event-race').count() == 1
    with connection.cursor() as cur:
        cur.execute('SELECT id FROM synthetic_owner_effect WHERE id IN (%s, %s)', ['race-owner-0', 'race-owner-1'])
        rows = cur.fetchall()
        assert rows == [('race-owner-' + str(winner),)]
    assert list(JobRecord.objects.filter(job_id__in=['job-race-0', 'job-race-1']).values_list('job_id', flat=True)) == ['job-race-' + str(winner)]
    assert len(race_refs) == 2 and all(conn.closed for conn in race_refs)
    result['race_one_creation_one_duplicate'] = True
    result['thread_conns_closed'] = True
    result['phase'] = 'CONSTRAINTS'
    invalid_cases = [('consumer_reference', ''), ('event_id', ''), ('event_version', ''), ('content_sha256', ''), ('content_sha256', '0F' * 32), ('correlation_id', ''), ('causation_id', ''), ('state', 'PENDING')]
    for idx, (field, invalid) in enumerate(invalid_cases):
        raw = _valid(consumer_reference='consumer-sql-' + str(idx), event_id='event-sql-' + str(idx))
        raw[field] = invalid
        try:
            with transaction.atomic(using='default'):
                with connection.cursor() as cur:
                    query = sql.SQL('INSERT INTO {}.{} (consumer_reference, event_id, event_version, content_sha256, state, consumed_at, correlation_id, causation_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection)
                    cur.execute(query, [raw[k] for k in ('consumer_reference', 'event_id', 'event_version', 'content_sha256', 'state', 'consumed_at', 'correlation_id', 'causation_id')])
        except IntegrityError as exc:
            assert getattr(exc.__cause__, 'sqlstate', None) == '23514'
        else:
            raise AssertionError('contrainte SQL attendue')
    result['sql_constraints'] = True
    hyd = Model.from_values(_valid(consumer_reference='consumer-hyd', event_id='event-hyd'))
    with transaction.atomic(using='default'):
        hyd.save(force_insert=True, using='default')
    hyd = Model.objects.using('default').get(consumer_reference='consumer-hyd', event_id='event-hyd')
    original = _export_bound(repo.get_receipt(consumer_reference='consumer-hyd', event_id='event-hyd'))
    hyd.event_id = 'moved'
    try:
        hyd.save(force_insert=True, using='default')
    except ValidationError:
        pass
    else:
        raise AssertionError('hydrate refuse')
    assert _export_bound(repo.get_receipt(consumer_reference='consumer-hyd', event_id='event-hyd')) == original
    assert repo.get_receipt(consumer_reference='consumer-hyd', event_id='moved') is None
    result['hydrated_refused'] = True
    with transaction.atomic(using='default'):
        try:
            BulkInboxReceiptRepository(using='other').insert_receipt(values=_valid(consumer_reference='consumer-other', event_id='event-other'))
        except BulkInboxReceiptRefused:
            pass
        else:
            raise AssertionError('alias other refuse')
    assert repo.get_receipt(consumer_reference='consumer-other', event_id='event-other') is None
    result['alias_other_refused'] = True
    with connection.cursor() as cur:
        cur.execute(sql.SQL("CREATE UNIQUE INDEX tmp_owned_partial ON {}.{} (content_sha256) WHERE consumer_reference = 'consumer-partial'").format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection))
    try:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-partial', 'v'])
            _create_job('job-partial')
            repo.insert_receipt(values=_valid(consumer_reference='consumer-partial', event_id='event-p1', content_sha256=SHA_A))
            try:
                repo.insert_receipt(values=_valid(consumer_reference='consumer-partial', event_id='event-p2', content_sha256=SHA_A))
            except IntegrityError as exc:
                assert getattr(exc.__cause__, 'sqlstate', None) == '23505'
                assert getattr(exc.__cause__.diag, 'constraint_name', None) == 'tmp_owned_partial'
                assert transaction.get_rollback(using='default') is True
            else:
                raise AssertionError('autre 23505 attendue')
        assert repo.get_receipt(consumer_reference='consumer-partial', event_id='event-p1') is None
        assert JobRecord.objects.filter(pk='job-partial').count() == 0
        assert _owner_count('owner-partial') == 0
        assert repo.get_receipt(consumer_reference='consumer-partial', event_id='event-p2') is None
    finally:
        with connection.cursor() as cur:
            cur.execute(sql.SQL('DROP INDEX {}.tmp_owned_partial').format(sql.Identifier(state['schema'])).as_string(connection.connection))
    result['other_integrity_propagates'] = True
    result['phase'] = 'REVERSE'
    MigrationExecutor(connection).migrate([('backend', '0007_bulk_event_envelope')])
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0008_bulk_inbox_receipt') == 0
    result['reverse_only_0008'] = True
    result['existing_tables_stable'] = before == [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    result['phase'] = 'COMPLETE'
def run_real_bulk_inbox_receipt_postgres(root_str):
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
    from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper
    from psycopg import Connection
    assert settings.configured is False
    assert apps.ready is False
    guard_targets = ((psycopg, 'connect', ()), (Connection, 'connect', ()), (PGWrapper, 'get_new_connection', (object(), {})), (socket.socket, 'connect', (object(), ('127.0.0.1', 0))), (socket, 'create_connection', (('127.0.0.1', 0),)), (subprocess, 'Popen', (['true'],)), (subprocess, 'run', (['true'],)), (builtins, 'open', ('project.env', 'rb')), (Path, 'open', (Path('project.env'), 'rb')), (os, 'open', ('project.env', os.O_RDONLY)))
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in guard_targets]
    with ExitStack() as stack:
        for (target, name, _a), guard in zip(guard_targets, guards):
            stack.enter_context(mock.patch.object(target, name, guard))
        spec = importlib.util.spec_from_file_location('inbox_pg_harness_under_test', target_path)
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
        assert callable(harness.run_real_bulk_inbox_receipt_postgres)
        for bad_root in (None, '', 0, b'/home/devops/datas/pixs'):
            outcome = harness.run_real_bulk_inbox_receipt_postgres(bad_root)
            assert outcome['real_pg'] is False
            assert outcome['phase'] == 'COMPLETE'
            assert outcome['reason'] == 'ROOT_INVALID'
        outcome = harness.run_real_bulk_inbox_receipt_postgres('/synthetic/root')
        assert outcome['reason'] == 'ROOT_MISMATCH'
        assert outcome['real_pg'] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [g.call_count for g in guards] == [0] * len(guards)
    print('BULK_INBOX_RECEIPT_PG_HARNESS_SAFE_OK')
    ''').strip()
_MARKER = 'BULK_INBOX_RECEIPT_PG_HARNESS_SAFE_OK' + chr(10)
class BulkInboxReceiptPostgresInertTests(unittest.TestCase):
    def test_harness_safe(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-c', _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)
        self.assertEqual(result.stderr, '')
if __name__ == '__main__':
    unittest.main()
