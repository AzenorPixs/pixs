'''Preuves PostgreSQL isolees CommandIdempotency B10 ; import et tests ordinaires inertes.'''
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
_FLAGS = ('search_path_isolated', 'forward_applied', 'roundtrip', 'owned_copy', 'sql_checks', 'unique_key', 'new_finalize_succeeded', 'new_finalize_rejected', 'replay_stable', 'replay_owned', 'fourth_key_independent', 'divergence_sha', 'divergence_serializer', 'race_one_creation_one_replay', 'thread_conns_closed', 'cotrans_success', 'cotrans_rollback', 'unfinalized_rollback', 'caught_refusal_rollback', 'guards_foreign', 'guards_cross_instance', 'guards_thread', 'guards_inactive', 'guards_replay_finalize', 'guards_refinalize', 'guards_cas', 'guards_tamper', 'contextvar_reset', 'runtime_protected_checkpoint', 'reverse_only_0006', 'existing_tables_stable', 'public_tables_stable')
_BASE_TABLES = ('backend_featureflagsourcesnapshotrecord', 'backend_jobrecord', 'backend_bulkoperationrecord', 'backend_bulkoperationexecutionrecord', 'backend_bulkcheckpointrecord', 'backend_bulkjobbindingrecord', 'backend_bulkjobschedulerecord', 'backend_bulkadmissionidentityrecord')
_TARGET_TABLE = 'backend_bulkcommandidempotencyrecord'
_VALID_SHA = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
_OTHER_SHA = 'fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210'
def _helpers():
    integration = str(_ROOT / 'tests' / 'integration')
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration
def _outcome():
    return {'real_pg': False, 'phase': 'COMPLETE', 'reason': 'NONE', 'cleanup_ok': False, 'conns_closed': False, 'server_version_num': None, 'test_schema': None, 'schema_owned': False, **{k: False for k in _FLAGS}}
def _body(result, h, state, refs, failures):
    import time
    import django
    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime, timezone
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
    settings.configure(INSTALLED_APPS=['pixs.backend'], SECRET_KEY='bulk-cmd-idem-synthetic-test', DATABASES={'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': database, 'USER': user, 'PASSWORD': password, 'HOST': '127.0.0.1', 'PORT': '5432', 'OPTIONS': {'options': h._pg_options(search_path), 'connect_timeout': 2}, 'CONN_MAX_AGE': 0}}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state['configured'] = True
    django.setup()
    if h._scalar(connection, 'SELECT current_schemas(false)', ()) != [state['schema'], 'pg_catalog']:
        result['reason'] = 'SEARCH_PATH_MISMATCH'
        return
    result['search_path_isolated'] = True
    from pixs.backend.bulk_command_idempotency_record import BulkCommandIdempotencyRecord as Model
    from pixs.backend.bulk_command_idempotency_repository import BulkCommandIdempotencyConflict, BulkCommandIdempotencyRefused, BulkCommandIdempotencyRepository, BulkCommandIdempotencyStale
    from pixs.backend.bulk_runtime_repository import BulkRuntimeRepository
    from pixs.backend.models import JobRecord
    tests_path = str(_ROOT / 'tests')
    if tests_path not in sys.path:
        sys.path.insert(0, tests_path)
    from unit.test_bulk_execution_values import _valid_execution_import, _valid_policy
    CREATED = datetime(2026, 1, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    EXPIRES = datetime(2026, 5, 6, 7, 8, 9, 10, tzinfo=timezone.utc)
    NOW = CREATED
    def valid(**over):
        d = {'tenant_id': 'tenant-resolu', 'subject_id': 'sujet-resolu', 'command_type': 'commande.declaree', 'idempotency_key': 'cle-e', 'content_sha256': _VALID_SHA, 'serializer_version': '1.2.3', 'state': 'IN_PROGRESS', 'result_reference': None, 'failure_code': None, 'created_at': CREATED, 'expires_at': EXPIRES, 'revision': 1}
        d.update(over)
        return d
    def refused(call, expected):
        try:
            call()
        except expected:
            return
        raise AssertionError('refus attendu absent')
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
    result['phase'] = 'MIGRATION'
    MigrationExecutor(connection).migrate([('backend', '0005_bulk_admission_identity')])
    before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert all(before) and len(state['tables']) == 8
    assert h._applied_count(connection, state['schema'], '0005_bulk_admission_identity') == 1
    MigrationExecutor(connection).migrate([('backend', '0006_bulk_command_idempotency')])
    assert h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0006_bulk_command_idempotency') == 1
    result['forward_applied'] = True
    snap = valid(idempotency_key='cle-model', state='SUCCEEDED', result_reference='res-snapshot', revision=2)
    mrow = Model.from_values(dict(snap))
    mrow.save(force_insert=True)
    fetched = Model.objects.get(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-model')
    assert fetched.as_values() == snap
    assert fetched.created_at == CREATED and fetched.created_at.tzinfo is timezone.utc
    result['roundtrip'] = True
    caller = valid(idempotency_key='cle-owned')
    r2 = Model.from_values(caller)
    caller['tenant_id'] = 'mute'
    assert r2.tenant_id == 'tenant-resolu'
    got = r2.as_values()
    got['tenant_id'] = 'mute'
    assert r2.as_values()['tenant_id'] == 'tenant-resolu'
    result['owned_copy'] = True
    def refuses_integrity(op):
        try:
            with transaction.atomic():
                op()
        except IntegrityError:
            return True
        return False
    assert refuses_integrity(lambda: Model.objects.create(**valid(idempotency_key='cle-sql1', tenant_id='')))
    assert refuses_integrity(lambda: Model.objects.create(**valid(idempotency_key='cle-sql2', content_sha256='Z' * 64)))
    assert refuses_integrity(lambda: Model.objects.create(**valid(idempotency_key='cle-sql3', state='BOGUS')))
    assert refuses_integrity(lambda: Model.objects.create(**valid(idempotency_key='cle-sql4', revision=0)))
    result['sql_checks'] = True
    assert refuses_integrity(lambda: Model.objects.create(**valid(idempotency_key='cle-model', state='SUCCEEDED', result_reference='res-snapshot', revision=2)))
    result['unique_key'] = True
    repo = BulkCommandIdempotencyRepository(using='default')
    with repo.idempotent_unit(values=valid(idempotency_key='cle-new-ok')) as tok:
        assert tok.is_replay is False
        assert repo.finalize_terminal(tok, expected_revision=1, state='SUCCEEDED', result_reference='res-synthetic', failure_code=None) == 2
    stored = repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-new-ok')
    assert stored['revision'] == 2 and stored['state'] == 'SUCCEEDED'
    result['new_finalize_succeeded'] = True
    with repo.idempotent_unit(values=valid(idempotency_key='cle-new-rej')) as tok2:
        assert repo.finalize_terminal(tok2, expected_revision=1, state='REJECTED', result_reference=None, failure_code='TECHNICAL') == 2
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-new-rej')['state'] == 'REJECTED'
    result['new_finalize_rejected'] = True
    seen = repo.replay(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-new-ok', content_sha256=_VALID_SHA, serializer_version='1.2.3')
    assert seen is not None and seen['revision'] == 2
    seen['state'] = 'MUTE'
    seen['revision'] = 999
    again = repo.replay(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-new-ok', content_sha256=_VALID_SHA, serializer_version='1.2.3')
    assert again['state'] == 'SUCCEEDED' and again['revision'] == 2
    assert Model.objects.filter(idempotency_key='cle-new-ok').count() == 1
    result['replay_stable'] = True
    result['replay_owned'] = True
    assert repo.replay(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-autre-independante', content_sha256=_VALID_SHA, serializer_version='1.2.3') is None
    with repo.idempotent_unit(values=valid(idempotency_key='cle-autre-independante')) as tok3:
        assert tok3.is_replay is False
        repo.finalize_terminal(tok3, expected_revision=1, state='SUCCEEDED', result_reference='res-autre', failure_code=None)
    result['fourth_key_independent'] = True
    refused(lambda: repo.replay(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-new-ok', content_sha256=_OTHER_SHA, serializer_version='1.2.3'), BulkCommandIdempotencyConflict)
    result['divergence_sha'] = True
    refused(lambda: repo.replay(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-new-ok', content_sha256=_VALID_SHA, serializer_version='2.0.0'), BulkCommandIdempotencyConflict)
    result['divergence_serializer'] = True
    refused(lambda: BulkCommandIdempotencyRepository(using=Hostile()), ValidationError)
    refused(lambda: repo.get_entry(tenant_id=Hostile(), subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='k'), BulkCommandIdempotencyRefused)
    refused(lambda: repo.replay(tenant_id='t', subject_id='s', command_type='c', idempotency_key='k', content_sha256=_VALID_SHA, serializer_version=Hostile()), BulkCommandIdempotencyRefused)
    other_repo = BulkCommandIdempotencyRepository(using='default')
    result['phase'] = 'GUARDS'
    def absent(key):
        assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key=key) is None
        assert repo._unit_var.get() is None
    try:
        with repo.idempotent_unit(values=valid(idempotency_key='cle-guard-foreign')) as tokf:
            refused(lambda: repo.finalize_terminal(object(), expected_revision=1, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
            refused(lambda: repo.finalize_terminal(tokf, expected_revision=1, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
    except BulkCommandIdempotencyRefused:
        pass
    else:
        raise AssertionError('sortie latchee attendue')
    absent('cle-guard-foreign')
    result['guards_foreign'] = True
    with repo.idempotent_unit(values=valid(idempotency_key='cle-cross-instance')) as tokx:
        refused(lambda: other_repo.finalize_terminal(tokx, expected_revision=1, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
        assert repo.finalize_terminal(tokx, expected_revision=1, state='SUCCEEDED', result_reference='res-x', failure_code=None) == 2
    result['guards_cross_instance'] = True
    try:
        with repo.idempotent_unit(values=valid(idempotency_key='cle-guard-cas')) as tokc:
            refused(lambda: repo.finalize_terminal(tokc, expected_revision=999, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyStale)
            refused(lambda: repo.finalize_terminal(tokc, expected_revision=1, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
    except BulkCommandIdempotencyRefused:
        pass
    else:
        raise AssertionError('sortie CAS latchee attendue')
    absent('cle-guard-cas')
    result['guards_cas'] = True
    with repo.idempotent_unit(values=valid(idempotency_key='cle-guard-replay-once')) as torg:
        repo.finalize_terminal(torg, expected_revision=1, state='SUCCEEDED', result_reference='res-g', failure_code=None)
    original_replay = repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-guard-replay-once')
    try:
        with repo.idempotent_unit(values=valid(idempotency_key='cle-guard-replay-once')) as tokr2:
            assert tokr2.is_replay is True
            try:
                tokr2.is_replay = False
            except AttributeError:
                pass
            else:
                raise AssertionError('propriete replay modifiable')
            refused(lambda: repo.finalize_terminal(tokr2, expected_revision=2, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
    except BulkCommandIdempotencyRefused:
        pass
    else:
        raise AssertionError('sortie replay latchee attendue')
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-guard-replay-once') == original_replay
    result['guards_replay_finalize'] = True
    refused(lambda: repo.finalize_terminal(torg, expected_revision=2, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
    result['guards_inactive'] = True
    try:
        with repo.idempotent_unit(values=valid(idempotency_key='cle-guard-refin')) as tok4:
            repo.finalize_terminal(tok4, expected_revision=1, state='SUCCEEDED', result_reference='res-r', failure_code=None)
            refused(lambda: repo.finalize_terminal(tok4, expected_revision=2, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyRefused)
    except BulkCommandIdempotencyRefused:
        pass
    else:
        raise AssertionError('sortie refinalize latchee attendue')
    absent('cle-guard-refin')
    result['guards_refinalize'] = True
    try:
        with repo.idempotent_unit(values=valid(idempotency_key='cle-guard-tamper-once')) as tokt:
            keyf = {'tenant_id': 'tenant-resolu', 'subject_id': 'sujet-resolu', 'command_type': 'commande.declaree', 'idempotency_key': 'cle-guard-tamper-once'}
            Model.objects.filter(**keyf).update(content_sha256=_OTHER_SHA, revision=99)
            refused(lambda: repo.finalize_terminal(tokt, expected_revision=1, state='SUCCEEDED', result_reference='r', failure_code=None), BulkCommandIdempotencyStale)
    except BulkCommandIdempotencyRefused:
        pass
    else:
        raise AssertionError('sortie tamper latchee attendue')
    absent('cle-guard-tamper-once')
    result['guards_tamper'] = True
    with repo.idempotent_unit(values=valid(idempotency_key='cle-cross-main')) as maintok:
        assert maintok._active is True
        def worker_try():
            from django.db import connections as wconns
            w = wconns['default']
            before = w.connection
            try:
                repo.finalize_terminal(maintok, expected_revision=1, state='SUCCEEDED', result_reference='r', failure_code=None)
            except BulkCommandIdempotencyRefused:
                return (before, w.connection)
            raise AssertionError('worker cross-thread doit refuser')
        with ThreadPoolExecutor(max_workers=1) as tpool:
            wbefore, wafter = tpool.submit(worker_try).result(timeout=15)
            assert wbefore is None and wafter is None
        repo.finalize_terminal(maintok, expected_revision=1, state='SUCCEEDED', result_reference='res-cross', failure_code=None)
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-cross-main')['state'] == 'SUCCEEDED'
    result['guards_thread'] = True
    result['phase'] = 'RACE'
    with connection.cursor() as cur_oid:
        cur_oid.execute('SELECT c.oid FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = %s AND c.relname = %s', [state['schema'], _TARGET_TABLE])
        relation_oid = cur_oid.fetchone()[0]
    race_barrier = Barrier(3)
    race_pids, race_refs = [], []
    race_lock = Lock()
    def race_worker():
        from django.db import connections as cconns
        wrapper = cconns['default']
        try:
            wrapper.ensure_connection()
            with wrapper.cursor() as cur_pid:
                cur_pid.execute('SELECT pg_backend_pid()')
                pid = cur_pid.fetchone()[0]
            with race_lock:
                race_pids.append(pid)
                race_refs.append(wrapper.connection)
            race_barrier.wait(timeout=5)
            with repo.idempotent_unit(values=valid(idempotency_key='cle-race')) as rt:
                if rt.is_replay:
                    return 'replay'
                repo.finalize_terminal(rt, expected_revision=1, state='SUCCEEDED', result_reference='res-race', failure_code=None)
                return 'new'
        finally:
            wrapper.close()
    with ThreadPoolExecutor(max_workers=2) as race_pool:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur_lock:
                lock_q = sql.SQL('LOCK TABLE {}.{} IN SHARE MODE').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection)
                cur_lock.execute(lock_q)
            f_a = race_pool.submit(race_worker)
            f_b = race_pool.submit(race_worker)
            race_barrier.wait(timeout=5)
            deadline = time.monotonic() + 3
            seen_blocked = False
            while time.monotonic() < deadline:
                with connection.cursor() as cur_locks:
                    cur_locks.execute('SELECT pid, granted FROM pg_locks WHERE locktype = %s AND relation = %s AND mode = %s', ['relation', relation_oid, 'RowExclusiveLock'])
                    rows = cur_locks.fetchall()
                with race_lock:
                    pids = tuple(race_pids)
                waiting = [row for row in rows if row[0] in pids and row[1] is False]
                if len(waiting) == 2:
                    seen_blocked = True
                    break
                time.sleep(0.01)
            assert seen_blocked
        outs = sorted([f_a.result(timeout=10), f_b.result(timeout=10)])
    assert outs == ['new', 'replay']
    assert Model.objects.filter(idempotency_key='cle-race').count() == 1
    assert len(race_refs) == 2 and all(conn.closed for conn in race_refs)
    result['race_one_creation_one_replay'] = True
    result['thread_conns_closed'] = True
    result['phase'] = 'COTRANSACTION'
    with connection.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS synthetic_owner_effect (id TEXT PRIMARY KEY, val TEXT)')
    policy = _valid_policy()
    policy.update(max_attempts=3, retry_delays_seconds=[1, 2], lease_seconds=30, renewal_seconds=5, max_runtime_seconds=200)
    rt_repo = BulkRuntimeRepository(using='default', failure_codes=frozenset({'TECHNICAL'}))
    def make_exec(op):
        data = _valid_execution_import()
        data.update(operation_id=op, status='RUNNING', bulk_type='IMPORT', bulk_version='1.0.0', tenant_context_reference='tenant-resolu', scope_context_reference=None, format='CSV', conflict_strategy='REJECT', commit_mode='ATOMIC', execution_version='1.0.0', requested_by_reference='sujet-resolu', mapping_reference='mapping-test', mapping_version='1.0.0', input_reference='objet-test', input_version='v1', input_sha256=_VALID_SHA, input_size_bytes=0, policy_reference='policy-test', policy_version='1.0.0', revision=1, cancellation_requested=False, expires_at=datetime(2026, 6, 1, tzinfo=timezone.utc))
        data.update(checkpoint_reference=None, progress={'total_rows': 1, 'validated_rows': 1, 'invalid_rows': 0, 'applied_rows': 0, 'execution_rejected_rows': 0, 'exported_rows': 0})
        return data
    def progress_full():
        return {'total_rows': 1, 'validated_rows': 1, 'invalid_rows': 0, 'applied_rows': 1, 'execution_rejected_rows': 0, 'exported_rows': 0}
    def checkpoint_full(op, cid, rev):
        return {'checkpoint_id': cid, 'operation_id': op, 'phase': 'APPLY', 'source_fingerprint': _VALID_SHA, 'mapping_version': '1.0.0', 'committed_unit_index': 1, 'progress': progress_full(), 'revision': rev, 'owner_result_reference': 'owner-res-ok'}
    def runtime_neighbors(jid):
        from pixs.backend.bulk_runtime_records import BulkJobBindingRecord, BulkJobScheduleRecord
        job = JobRecord.objects.get(pk=jid)
        return {'job': {field.attname: getattr(job, field.attname) for field in JobRecord._meta.concrete_fields}, 'schedule': BulkJobScheduleRecord.objects.get(pk=jid).as_values(), 'binding': BulkJobBindingRecord.objects.get(job_id=jid).as_values()}
    def prepared(op):
        rt_repo.create_execution(values=dict(make_exec(op)))
        JobRecord(job_id='job-' + op, job_type='pixs.bulk.apply', job_version='1.0.0', payload={'execution_reference': op, 'execution_version': '1.0.0'}, subject={'requested_by_reference': 'sujet-resolu'}, tenant_context={'tenant_context_reference': 'tenant-resolu', 'scope_context_reference': None}, correlation_id='corr-test', causation_id='cause-test', perimeter_reference='perim-test', state='PENDING', attempt_count=0, lease_owner=None, lease_expires_at=None).save(force_insert=True)
        rt_repo.bind_job(operation_id=op, job_id='job-' + op, phase='APPLY')
        rt_repo.create_schedule(values={'job_id': 'job-' + op, 'policy_reference': 'policy-test', 'policy_version': '1.0.0', 'next_run_at': None, 'attempt_deadline': None, 'failure_code': None, 'revision': 1})
        rt_repo.acquire_lease(operation_id=op, job_id='job-' + op, phase='APPLY', owner='owner-test', policy=policy, now=NOW, expected_schedule_revision=1)
        return 'job-' + op
    jid_ok = prepared('op-cotrans-ok')
    with transaction.atomic(using='default'):
        with repo.idempotent_unit(values=valid(idempotency_key='cle-cotrans-ok')) as ctok:
            with rt_repo.protected_unit(operation_id='op-cotrans-ok', job_id=jid_ok, phase='APPLY', owner='owner-test', policy=policy, now=NOW, expected_extension_revision=1, expected_schedule_revision=2) as unit:
                with connection.cursor() as cur2:
                    cur2.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-ok', 'v'])
                rt_repo.commit_checkpoint(unit, checkpoint_full('op-cotrans-ok', 'ckpt-ok', 2))
                repo.finalize_terminal(ctok, expected_revision=1, state='SUCCEEDED', result_reference='res-cotrans', failure_code=None)
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-cotrans-ok')['state'] == 'SUCCEEDED'
    with connection.cursor() as cur3:
        cur3.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-ok'])
        assert cur3.fetchone()[0] == 1
    result['cotrans_success'] = True
    result['runtime_protected_checkpoint'] = True
    jid_rb = prepared('op-cotrans-rb')
    full_before = rt_repo.load_execution(operation_id='op-cotrans-rb')
    rb_neighbors = runtime_neighbors(jid_rb)
    with connection.cursor() as curj:
        curj.execute('SELECT lease_owner FROM backend_jobrecord WHERE job_id = %s', [jid_rb])
        bail_before = curj.fetchone()[0]
    try:
        with transaction.atomic(using='default'):
            with repo.idempotent_unit(values=valid(idempotency_key='cle-cotrans-rb')) as ctok2:
                with rt_repo.protected_unit(operation_id='op-cotrans-rb', job_id=jid_rb, phase='APPLY', owner='owner-test', policy=policy, now=NOW, expected_extension_revision=1, expected_schedule_revision=2) as unit2:
                    with connection.cursor() as cur4:
                        cur4.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-rb', 'v'])
                    rt_repo.commit_checkpoint(unit2, checkpoint_full('op-cotrans-rb', 'ckpt-rb', 2))
                    raise RuntimeError('panne proprietaire propagee')
    except RuntimeError:
        pass
    else:
        raise AssertionError('erreur proprietaire doit propager')
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-cotrans-rb') is None
    assert rt_repo.load_execution(operation_id='op-cotrans-rb') == full_before
    assert runtime_neighbors(jid_rb) == rb_neighbors
    with connection.cursor() as cur5:
        cur5.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-rb'])
        assert cur5.fetchone()[0] == 0
        cur5.execute('SELECT count(*) FROM backend_bulkcheckpointrecord WHERE checkpoint_id = %s', ['ckpt-rb'])
        assert cur5.fetchone()[0] == 0
        cur5.execute('SELECT lease_owner FROM backend_jobrecord WHERE job_id = %s', [jid_rb])
        assert cur5.fetchone()[0] == bail_before
    result['cotrans_rollback'] = True
    jid_unfin = prepared('op-cotrans-unfin')
    full_unfin_before = rt_repo.load_execution(operation_id='op-cotrans-unfin')
    unfin_neighbors = runtime_neighbors(jid_unfin)
    try:
        with transaction.atomic(using='default'):
            with repo.idempotent_unit(values=valid(idempotency_key='cle-unfinalized')):
                with rt_repo.protected_unit(operation_id='op-cotrans-unfin', job_id=jid_unfin, phase='APPLY', owner='owner-test', policy=policy, now=NOW, expected_extension_revision=1, expected_schedule_revision=2) as unfin_unit:
                    with connection.cursor() as unfin_cur:
                        unfin_cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-unfin', 'v'])
                    rt_repo.commit_checkpoint(unfin_unit, checkpoint_full('op-cotrans-unfin', 'ckpt-unfin', 2))
    except BulkCommandIdempotencyRefused:
        pass
    else:
        raise AssertionError('sortie non finalisee doit refuser')
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-unfinalized') is None
    assert rt_repo.load_execution(operation_id='op-cotrans-unfin') == full_unfin_before
    assert runtime_neighbors(jid_unfin) == unfin_neighbors
    with connection.cursor() as verify_unfin:
        verify_unfin.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-unfin'])
        assert verify_unfin.fetchone()[0] == 0
        verify_unfin.execute('SELECT count(*) FROM backend_bulkcheckpointrecord WHERE checkpoint_id = %s', ['ckpt-unfin'])
        assert verify_unfin.fetchone()[0] == 0
    result['unfinalized_rollback'] = True
    with transaction.atomic(using='default'):
        with connection.cursor() as cur_pre:
            cur_pre.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-before-caught', 'v'])
        try:
            with repo.idempotent_unit(values=valid(idempotency_key='cle-caught')):
                pass
        except BulkCommandIdempotencyRefused:
            assert transaction.get_rollback(using='default') is True
            try:
                with connection.cursor() as cur7:
                    cur7.execute('SELECT 1')
            except TransactionManagementError:
                pass
            else:
                raise AssertionError('requete sous rollback doit echouer')
    assert repo.get_entry(tenant_id='tenant-resolu', subject_id='sujet-resolu', command_type='commande.declaree', idempotency_key='cle-caught') is None
    with connection.cursor() as cur8:
        cur8.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-before-caught'])
        assert cur8.fetchone()[0] == 0
    result['caught_refusal_rollback'] = True
    assert repo._unit_var.get() is None
    result['contextvar_reset'] = True
    assert Model.objects.filter(state='IN_PROGRESS').count() == 0
    MigrationExecutor(connection).migrate([('backend', '0005_bulk_admission_identity')])
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0006_bulk_command_idempotency') == 0
    assert h._applied_count(connection, state['schema'], '0005_bulk_admission_identity') == 1
    result['reverse_only_0006'] = True
    result['existing_tables_stable'] = before == [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    result['phase'] = 'COMPLETE'
def run_real_bulk_command_idempotency_postgres(root_str):
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
        except BaseException as failure:
            result['reason'] = 'TEST_FAILED'
            result['error_type'] = type(failure).__name__
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
                            result['cleanup_ok'] = True
                else:
                    result['cleanup_ok'] = True
                result['conns_closed'] = not failures and all(bool(c.closed) for c in refs)
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
        result['reason'] = 'CASE_INCOMPLETE'
    return result
_CHILD = textwrap.dedent(r'''
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
guard_targets = ((psycopg, "connect", ()), (Connection, "connect", ()), (PGWrapper, "get_new_connection", (object(), {})), (socket.socket, "connect", (object(), ("127.0.0.1", 0))), (socket, "create_connection", (("127.0.0.1", 0),)), (subprocess, "Popen", (["true"],)), (subprocess, "run", (["true"],)), (__import__("builtins"), "open", ("project.env", "rb")), (Path, "open", (Path("project.env"), "rb")), (os, "open", ("project.env", os.O_RDONLY)))
guards = [mock.Mock(side_effect=AssertionError("forbidden")) for _ in guard_targets]
with ExitStack() as stack:
    for (t, n, _a), g in zip(guard_targets, guards):
        stack.enter_context(mock.patch.object(t, n, g))
    spec = importlib.util.spec_from_file_location("cmd_idem_pg_harness_under_test", target_path)
    harness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness)
    for (t, n, a), g in zip(guard_targets, guards):
        try:
            getattr(t, n)(*a)
        except AssertionError:
            pass
        else:
            raise AssertionError("garde inactive")
        assert g.call_count == 1
        g.reset_mock()
    assert callable(harness.run_real_bulk_command_idempotency_postgres)
    for bad in (None, "", 0, b"/home/devops/datas/pixs"):
        o = harness.run_real_bulk_command_idempotency_postgres(bad)
        assert o["real_pg"] is False and o["phase"] == "COMPLETE" and o["reason"] == "ROOT_INVALID"
    o = harness.run_real_bulk_command_idempotency_postgres("/synthetic/root")
    assert o["reason"] == "ROOT_MISMATCH" and o["real_pg"] is False
    assert settings.configured is False and apps.ready is False
    assert [g.call_count for g in guards] == [0] * len(guards)
print("BULK_COMMAND_IDEMPOTENCY_PG_HARNESS_SAFE_OK")
''').strip()
class BulkCommandIdempotencyPgHarnessSafeTests(unittest.TestCase):
    def test_child_isolated_inert_and_guarded(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-c', _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'BULK_COMMAND_IDEMPOTENCY_PG_HARNESS_SAFE_OK\n')
        self.assertEqual(result.stderr, '')
_REAL_WORKER = 'import importlib.util\nimport json\nimport sys\nsys.path.insert(0, sys.argv[1])\nspec = importlib.util.spec_from_file_location("cmd_idem_pg_real_worker", sys.argv[2])\nharness = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(harness)\nresult = harness.run_real_bulk_command_idempotency_postgres(sys.argv[3])\nprint(json.dumps(result, sort_keys=True))\nraise SystemExit(0 if result["real_pg"] else 1)\n'
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--real-pg':
        try:
            completed = subprocess.run([sys.executable, '-I', '-B', '-c', _REAL_WORKER, _SRC, _TARGET, str(_ROOT)], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=90, check=False)
        except subprocess.TimeoutExpired:
            outcome = _outcome()
            outcome['reason'] = 'WORKER_TIMEOUT'
        else:
            try:
                outcome = json.loads(completed.stdout)
                assert type(outcome) is dict
            except Exception:
                outcome = _outcome()
                outcome['reason'] = 'WORKER_OUTPUT_INVALID'
        print(json.dumps(outcome, sort_keys=True))
        raise SystemExit(0 if outcome.get('real_pg') else 1)
    unittest.main()
