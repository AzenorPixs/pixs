'''Preuves PostgreSQL isolees ValidationReport B13 ; import et tests ordinaires inertes.'''
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
_FLAGS = ('search_path_isolated', 'forward_applied', 'physical_exact', 'roundtrip_8', 'codec_order', 'none_modes', 'bigint_text', 'bound_before_poison', 'catalog_refused', 'owned_frozen', 'same_operation_ids', 'co_commit', 'co_rollback', 'inflight_not_result', 'hydrated_refused', 'alias_other_refused', 'malformed_refused', 'capacity_stdlib', 'prevalidation_no_row', 'temp_check_propagates', 'reverse_only_0009', 'existing_tables_stable', 'public_tables_stable')
_BASE_TABLES = ('backend_featureflagsourcesnapshotrecord', 'backend_jobrecord', 'backend_bulkoperationrecord', 'backend_bulkoperationexecutionrecord', 'backend_bulkcheckpointrecord', 'backend_bulkjobbindingrecord', 'backend_bulkjobschedulerecord', 'backend_bulkadmissionidentityrecord', 'backend_bulkcommandidempotencyrecord', 'backend_bulkeventenveloperecord', 'backend_bulkinboxreceiptrecord')
_TARGET_TABLE = 'backend_bulkvalidationreportrecord'
def _helpers():
    integration = str(_ROOT / 'tests' / 'integration')
    if integration not in sys.path:
        sys.path.insert(0, integration)
    import test_job_record_postgres_integration
    return test_job_record_postgres_integration
def _outcome():
    return {'real_pg': False, 'phase': 'COMPLETE', 'reason': 'NONE', 'cleanup_ok': False, 'conns_closed': False, 'server_version_num': None, 'test_schema': None, 'schema_owned': False, **{k: False for k in _FLAGS}}
def _body(result, h, state, refs, failures):
    import sys as _sys
    import django
    from dataclasses import FrozenInstanceError
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
    settings.configure(INSTALLED_APPS=['pixs.backend'], SECRET_KEY='bulk-report-synthetic-test', DATABASES={'default': db_config, 'other': dict(db_config)}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state['configured'] = True
    django.setup()
    if h._scalar(connection, 'SELECT current_schemas(false)', ()) != [state['schema'], 'pg_catalog']:
        result['reason'] = 'SEARCH_PATH_MISMATCH'
        return
    refs.append(connection.connection)
    result['search_path_isolated'] = True
    from pixs.backend.bulk_validation_report_record import BulkValidationReportRecord as Model
    from pixs.backend.bulk_validation_report_repository import BulkValidationReportRefused, BulkValidationReportRepository
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
    def table_query(template):
        return sql.SQL(template).format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection)
    result['phase'] = 'MIGRATION'
    MigrationExecutor(connection).migrate([('backend', '0008_bulk_inbox_receipt')])
    before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert all(before) and len(state['tables']) == 11
    MigrationExecutor(connection).migrate([('backend', '0009_bulk_validation_report')])
    assert h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0009_bulk_validation_report') == 1
    result['forward_applied'] = True
    with connection.cursor() as cur:
        cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position', (state['schema'], _TARGET_TABLE))
        cols = cur.fetchall()
    assert [c[0] for c in cols] == ['id', 'report_version', 'operation_id', 'mode', 'progress', 'diagnostics', 'complete', 'source_version', 'mapping_version']
    types = {c[0]: c[1] for c in cols}
    assert types['id'] == 'bigint'
    assert types['complete'] == 'boolean'
    assert all(types[k] == 'text' for k in ('report_version', 'operation_id', 'mode', 'progress', 'diagnostics', 'source_version', 'mapping_version'))
    with connection.cursor() as cur:
        cur.execute('SELECT conname, contype FROM pg_constraint JOIN pg_class ON pg_class.oid = conrelid JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace WHERE pg_namespace.nspname = %s AND pg_class.relname = %s', (state['schema'], _TARGET_TABLE))
        cons = cur.fetchall()
    assert {c[0] for c in cons if c[1] == 'c'} == {'bulkvalidationreport_version_exact', 'bulkvalidationreport_operation_non_empty', 'bulkvalidationreport_mode_member', 'bulkvalidationreport_progress_non_empty', 'bulkvalidationreport_diagnostics_non_empty', 'bulkvalidationreport_mapping_non_empty', 'bulkvalidationreport_source_non_empty'}
    assert [c[0] for c in cons if c[1] == 'p'] == [_TARGET_TABLE + '_pkey']
    assert not [c[0] for c in cons if c[1] == 'u']
    assert not [c[0] for c in cons if c[1] == 'f']
    result['physical_exact'] = True
    result['phase'] = 'ROUNDTRIP'
    repo = BulkValidationReportRepository(using='default')
    with transaction.atomic(using='default'):
        caller = _report()
        ctx = _ctx()
        rid = repo.insert_report(values=caller, **ctx)
        assert type(rid) is int and rid >= 1
        caller['progress']['validated_rows'] = 99
        caller['diagnostics'][0]['code'] = 'mute'
        ctx['policy']['retry_delays_seconds'].append(9)
        snap = repo.get_report(report_id=rid, **_ctx())
        assert snap is not None and hasattr(snap, 'as_values')
        got = snap.as_values()
        assert got == _report()
        assert set(got) == {'report_version','operation_id','mode','progress','diagnostics','complete','source_version','mapping_version'}
        assert type(got['diagnostics']) is tuple
        assert got['diagnostics'][0] == _row()
        assert snap.progress.validated_rows == 2
        try:
            snap.complete = False
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('snapshot non gele')
        try:
            snap.progress.validated_rows = 9
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('progress non gele')
        try:
            snap.diagnostics[0].code = 'mute'
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('row non gelee')
        exported = snap.as_values()
        exported['progress']['validated_rows'] = 99
        assert snap.as_values()['progress']['validated_rows'] == 2
    result['roundtrip_8'] = True
    result['owned_frozen'] = True
    with transaction.atomic(using='default'):
        multi = _report(diagnostics=(_row(line_index=1), _row(line_index=2)))
        rid2 = repo.insert_report(values=multi, **_ctx(policy=_policy(max_diagnostics=10)))
        fetched = repo.get_report(report_id=rid2, **_ctx(policy=_policy(max_diagnostics=10)))
        assert [r['line_index'] for r in fetched.as_values()['diagnostics']] == [1, 2]
    result['codec_order'] = True
    with transaction.atomic(using='default'):
        rnone = repo.insert_report(values=_report(operation_id='op-é', mode=None, complete=False, progress=_progress(exported_rows=1, applied_rows=0)), **_ctx())
        assert repo.get_report(report_id=rnone, **_ctx()).as_values() == _report(operation_id='op-é', mode=None, complete=False, progress=_progress(exported_rows=1, applied_rows=0))
        repo.insert_report(values=_report(mode='VALIDATE_ONLY', progress=_progress()), **_ctx())
    result['none_modes'] = True
    with transaction.atomic(using='default'):
        big = 2 ** 63 + 123
        coherent = _progress(validated_rows=big, invalid_rows=0, applied_rows=big, execution_rejected_rows=0, exported_rows=0)
        rb = repo.insert_report(values=_report(mode='ATOMIC', progress=coherent), **_ctx())
        assert repo.get_report(report_id=rb, **_ctx()).as_values()['progress']['validated_rows'] == big
        lb = repo.insert_report(values=_report(diagnostics=(_row(line_index=2 ** 80),)), **_ctx())
        assert repo.get_report(report_id=lb, **_ctx()).as_values()['diagnostics'][0]['line_index'] == 2 ** 80
        sup600 = 10 ** 600
        c600 = _progress(validated_rows=sup600, invalid_rows=0, applied_rows=sup600, execution_rejected_rows=0, exported_rows=0)
        r600 = repo.insert_report(values=_report(mode='ATOMIC', progress=c600), **_ctx())
        assert repo.get_report(report_id=r600, **_ctx()).as_values()['progress']['validated_rows'] == sup600
    result['bigint_text'] = True
    assert _sys.get_int_max_str_digits() > 0
    with transaction.atomic(using='default'):
        class Hostile:
            pass
        poisoned = _report(diagnostics=(Hostile(), Hostile()))
        try:
            repo.insert_report(values=poisoned, policy=_policy(max_diagnostics=1), declared_codes=('INVALID_FIELD',), declared_fields=('name',))
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('borne avant poison attendue')
        try:
            repo.insert_report(values=_report(), policy=_policy(), declared_codes=('UNKNOWN',), declared_fields=('name',))
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('catalogue refuse attendu')
        try:
            repo.get_report(report_id=999999999, policy=None, declared_codes=('INVALID_FIELD',), declared_fields=('name',))
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('contexte avant requete attendu')
    result['bound_before_poison'] = True
    result['catalog_refused'] = True
    with transaction.atomic(using='default'):
        first = repo.insert_report(values=_report(operation_id='op-same'), **_ctx())
        second = repo.insert_report(values=_report(operation_id='op-same'), **_ctx())
        assert first != second
        assert repo.get_report(report_id=first, **_ctx()).as_values()['operation_id'] == 'op-same'
        assert repo.get_report(report_id=second, **_ctx()).as_values()['operation_id'] == 'op-same'
    result['same_operation_ids'] = True
    result['phase'] = 'TX'
    with connection.cursor() as cur:
        cur.execute('CREATE TABLE synthetic_owner_effect (id TEXT PRIMARY KEY, val TEXT)')
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-ok', 'v'])
        ok_id = repo.insert_report(values=_report(operation_id='op-ok'), **_ctx())
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-ok'])
        assert cur.fetchone()[0] == 1
    assert repo.get_report(report_id=ok_id, **_ctx()).operation_id == 'op-ok'
    result['co_commit'] = True
    try:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-rb', 'v'])
            rb_id = repo.insert_report(values=_report(operation_id='op-rb'), **_ctx())
            raise RuntimeError('panne proprietaire')
    except RuntimeError:
        pass
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-rb'])
        assert cur.fetchone()[0] == 0
    assert repo.get_report(report_id=rb_id, **_ctx()) is None
    result['co_rollback'] = True
    other = connections['other']
    with transaction.atomic(using='default'):
        with connection.cursor() as cur:
            cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-inflight', 'v'])
        inflight = repo.insert_report(values=_report(operation_id='op-inflight'), **_ctx())
        assert type(inflight) is int
        assert h._scalar(other, 'SELECT current_schemas(false)', ()) == [state['schema'], 'pg_catalog']
        refs.append(other.connection)
        observer = BulkValidationReportRepository(using='other')
        assert observer.get_report(report_id=inflight, **_ctx()) is None
        with other.cursor() as cur:
            cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-inflight'])
            assert cur.fetchone()[0] == 0
        try:
            BulkValidationReportRepository(using='other').insert_report(values=_report(operation_id='op-other'), **_ctx())
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('alias other refuse')
    with connection.cursor() as cur:
        cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-inflight'])
        assert cur.fetchone()[0] == 1
    assert observer.get_report(report_id=inflight, **_ctx()).operation_id == 'op-inflight'
    result['inflight_not_result'] = True
    result['alias_other_refused'] = True
    hyd = None
    with transaction.atomic(using='default'):
        tmp = Model.from_values(_report(operation_id='op-hyd'), **_ctx())
        tmp.save(force_insert=True, using='default')
        hyd_id = tmp.id
    from pixs.backend.bulk_validation_report_record import BulkValidationReportRecord as HydModel
    hyd = HydModel.objects.using('default').get(id=hyd_id)
    original = repo.get_report(report_id=hyd_id, **_ctx()).as_values()
    hyd.operation_id = 'moved'
    try:
        hyd.save(force_insert=True, using='default')
    except ValidationError:
        pass
    else:
        raise AssertionError('hydrate refuse')
    assert repo.get_report(report_id=hyd_id, **_ctx()).as_values() == original
    result['hydrated_refused'] = True
    result['phase'] = 'CONSTRAINTS'
    with connection.cursor() as cur:
        cur.execute(sql.SQL('ALTER TABLE {}.{} ADD CONSTRAINT tmp_owned_check CHECK (operation_id <> {})').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE), sql.Literal('never-hit-tmp')))
    try:
        before_count = HydModel.objects.using('default').count()
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute('INSERT INTO synthetic_owner_effect (id, val) VALUES (%s, %s)', ['owner-check-failure', 'v'])
            try:
                repo.insert_report(values=_report(operation_id='never-hit-tmp'), **_ctx())
            except IntegrityError as exc:
                assert getattr(exc.__cause__, 'sqlstate', None) == '23514'
                assert transaction.get_rollback(using='default') is True
                try:
                    with connection.cursor() as cur:
                        cur.execute('SELECT 1')
                except TransactionManagementError:
                    pass
                else:
                    raise AssertionError('transaction proprietaire doit rester invalidee')
            else:
                raise AssertionError('erreur CHECK attendue')
        assert HydModel.objects.using('default').count() == before_count
        with connection.cursor() as cur:
            cur.execute('SELECT count(*) FROM synthetic_owner_effect WHERE id = %s', ['owner-check-failure'])
            assert cur.fetchone()[0] == 0
        try:
            with connection.cursor() as cur:
                cur.execute('SELECT 1')
        except TransactionManagementError:
            raise AssertionError('connexion assainie attendue apres rollback')
    finally:
        with connection.cursor() as cur:
            cur.execute(table_query('ALTER TABLE {}.{} DROP CONSTRAINT tmp_owned_check'))
    result['temp_check_propagates'] = True
    with transaction.atomic(using='default'):
        invalid_count_before = HydModel.objects.using('default').count()
        try:
            repo.insert_report(values={'intrus': 1}, **_ctx())
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('prevalidation attendue')
        assert HydModel.objects.using('default').count() == invalid_count_before
    result['prevalidation_no_row'] = True
    malformed_targets = ['{oops', 'NaN', '{"a": 1, "a": 2}', '{"total_rows": "1"}']
    for idx, malformed in enumerate(malformed_targets):
        with transaction.atomic(using='default'):
            target = repo.insert_report(values=_report(operation_id='op-mal-' + str(idx)), **_ctx())
        with connection.cursor() as cur:
            cur.execute(table_query('UPDATE {}.{} SET progress = %s WHERE id = %s'), [malformed, target])
        try:
            repo.get_report(report_id=target, **_ctx())
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('malforme refuse attendu')
    with connection.cursor() as cur:
        cur.execute(table_query('UPDATE {}.{} SET diagnostics = %s WHERE id = %s'), ['[{oops]', target])
    try:
        repo.get_report(report_id=target, **_ctx())
    except BulkValidationReportRefused:
        pass
    else:
        raise AssertionError('diagnostic malforme refuse')
    for encoded in ('[{"code":"UNKNOWN","field_reference":"name","line_index":1}]',
                    '[{"code":"INVALID_FIELD","field_reference":"name","line_index":1}]'[:-1] + ',' + ','.join(['{"code":"INVALID_FIELD","field_reference":"name","line_index":1}'] * 10) + ']'):
        with connection.cursor() as cur:
            cur.execute(table_query('UPDATE {}.{} SET progress = %s, diagnostics = %s WHERE id = %s'),
                        ['{"total_rows":null,"validated_rows":2,"invalid_rows":1,"applied_rows":0,"execution_rejected_rows":0,"exported_rows":0}', encoded, target])
        try:
            repo.get_report(report_id=target, **_ctx())
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('catalogue ou borne au rechargement attendus')
    result['malformed_refused'] = True
    digit_limit = _sys.get_int_max_str_digits()
    assert digit_limit > 0
    unsupported = 10 ** (digit_limit + 100)
    before_capacity = HydModel.objects.using('default').count()
    with transaction.atomic(using='default'):
        try:
            repo.insert_report(values=_report(mode='ATOMIC', progress=_progress(validated_rows=unsupported, invalid_rows=0, applied_rows=unsupported)), **_ctx())
        except BulkValidationReportRefused:
            pass
        else:
            raise AssertionError('capacite stdlib refusee attendue')
    assert HydModel.objects.using('default').count() == before_capacity
    with connection.cursor() as cur:
        encoded_huge = '{"total_rows":null,"validated_rows":' + '9' * (digit_limit + 100) + ',"invalid_rows":0,"applied_rows":0,"execution_rejected_rows":0,"exported_rows":0}'
        cur.execute(table_query('UPDATE {}.{} SET progress = %s WHERE id = %s'), [encoded_huge, target])
    try:
        repo.get_report(report_id=target, **_ctx())
    except BulkValidationReportRefused:
        pass
    else:
        raise AssertionError('capacite stdlib rechargement refusee attendue')
    assert _sys.get_int_max_str_digits() == digit_limit
    result['capacity_stdlib'] = True
    result['phase'] = 'REVERSE'
    MigrationExecutor(connection).migrate([('backend', '0008_bulk_inbox_receipt')])
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0009_bulk_validation_report') == 0
    result['reverse_only_0009'] = True
    result['existing_tables_stable'] = before == [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    result['phase'] = 'COMPLETE'
def run_real_bulk_validation_report_postgres(root_str):
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
        spec = importlib.util.spec_from_file_location('report_pg_harness_under_test', target_path)
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
        assert callable(harness.run_real_bulk_validation_report_postgres)
        for bad_root in (None, '', 0, b'/home/devops/datas/pixs'):
            outcome = harness.run_real_bulk_validation_report_postgres(bad_root)
            assert outcome['real_pg'] is False
            assert outcome['phase'] == 'COMPLETE'
            assert outcome['reason'] == 'ROOT_INVALID'
        outcome = harness.run_real_bulk_validation_report_postgres('/synthetic/root')
        assert outcome['reason'] == 'ROOT_MISMATCH'
        assert outcome['real_pg'] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [g.call_count for g in guards] == [0] * len(guards)
    print('BULK_VALIDATION_REPORT_PG_HARNESS_SAFE_OK')
    ''').strip()
_MARKER = 'BULK_VALIDATION_REPORT_PG_HARNESS_SAFE_OK' + chr(10)
class BulkValidationReportPostgresInertTests(unittest.TestCase):
    def test_harness_safe(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-c', _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)
        self.assertEqual(result.stderr, '')
if __name__ == '__main__':
    unittest.main()
