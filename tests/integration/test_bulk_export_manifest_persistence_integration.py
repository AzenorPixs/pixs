'''Preuves PostgreSQL isolees ExportManifest B12 ; import et tests ordinaires inertes.'''
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
_FLAGS = ('search_path_isolated', 'forward_applied', 'physical_exact', 'roundtrip_17', 'owned_frozen', 'none_complete_modes', 'utc_identity_bounds', 'bigint_text', 'same_operation_ids', 'co_commit', 'co_rollback', 'inflight_not_ready', 'hydrated_refused', 'deferred_refused', 'alias_other_refused', 'bad_id_before_query', 'malformed_refused', 'capacity_stdlib', 'prevalidation_no_row', 'temp_check_propagates', 'sql_constraints', 'reverse_only_0010', 'existing_tables_stable', 'public_tables_stable')
_BASE_TABLES = ('backend_featureflagsourcesnapshotrecord', 'backend_jobrecord', 'backend_bulkoperationrecord', 'backend_bulkoperationexecutionrecord', 'backend_bulkcheckpointrecord', 'backend_bulkjobbindingrecord', 'backend_bulkjobschedulerecord', 'backend_bulkadmissionidentityrecord', 'backend_bulkcommandidempotencyrecord', 'backend_bulkeventenveloperecord', 'backend_bulkinboxreceiptrecord', 'backend_bulkvalidationreportrecord')
_TARGET_TABLE = 'backend_bulkexportmanifestrecord'
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
    from pixs.backend.bulk_export_manifest_record import BulkExportManifestRecord as Model
    from pixs.backend.bulk_export_manifest_repository import BulkExportManifestRefused, BulkExportManifestRepository
    from datetime import datetime, timezone
    _UTC = timezone.utc
    _EXPIRES = datetime(2030, 1, 1, tzinfo=timezone.utc)
    def _fixture_manifest17(suffix, scope_value, complete_value):
        return {'manifest_version': '1.0.0', 'operation_id': 'op-synthetic-' + str(suffix), 'format': 'CSV', 'mapping_reference': 'map-ref', 'mapping_version': '1.2.3', 'tenant_context_reference': 'tenant-ref', 'scope_context_reference': scope_value, 'consistency_kind': 'SNAPSHOT', 'consistency_reference': 'cons-ref', 'row_count': 2, 'size_bytes': 128, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'classification_reference': 'class-ref', 'expires_at': _EXPIRES, 'object_reference': 'obj-ref', 'object_version': 'v1', 'complete': complete_value}
    def _helper_to_values(bound):
        return {'manifest_version': bound.manifest_version, 'operation_id': bound.operation_id, 'format': bound.format, 'mapping_reference': bound.mapping_reference, 'mapping_version': bound.mapping_version, 'tenant_context_reference': bound.tenant_context_reference, 'scope_context_reference': bound.scope_context_reference, 'consistency_kind': bound.consistency_kind, 'consistency_reference': bound.consistency_reference, 'row_count': bound.row_count, 'size_bytes': bound.size_bytes, 'sha256': bound.sha256, 'classification_reference': bound.classification_reference, 'expires_at': bound.expires_at, 'object_reference': bound.object_reference, 'object_version': bound.object_version, 'complete': bound.complete}
    def table_sql(template):
        return sql.SQL(template).format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection)
    _base17 = _fixture_manifest17(1, 'scope-test', True)
    _none17 = _fixture_manifest17(2, None, False)
    assert _base17['scope_context_reference'] == 'scope-test'
    assert _none17['scope_context_reference'] is None
    assert _base17['complete'] is True
    assert _none17['complete'] is False
    assert _base17['expires_at'].tzinfo is _UTC
    assert _none17['expires_at'].tzinfo is _UTC
    result['phase'] = 'MIGRATE'
    MigrationExecutor(connection).migrate([('backend', '0009_bulk_validation_report')])
    before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert len(before) == 12 and all(before)
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    MigrationExecutor(connection).migrate([('backend', '0010_bulk_export_manifest')])
    assert h._applied_count(connection, state['schema'], '0010_bulk_export_manifest') == 1
    with connection.cursor() as cur:
        cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position', [state['schema'], _TARGET_TABLE])
        cols = cur.fetchall()
    assert [c[0] for c in cols] == ['id', 'manifest_version', 'operation_id', 'format', 'mapping_reference', 'mapping_version', 'tenant_context_reference', 'scope_context_reference', 'consistency_kind', 'consistency_reference', 'row_count', 'size_bytes', 'sha256', 'classification_reference', 'expires_at', 'object_reference', 'object_version', 'complete']
    assert len(cols) == 18
    types = dict(cols)
    assert types['id'] == 'bigint' and types['expires_at'] == 'timestamp with time zone' and types['complete'] == 'boolean'
    assert all(value == 'text' for key, value in cols if key not in ['id', 'expires_at', 'complete'])
    with connection.cursor() as cur:
        cur.execute('SELECT conname, contype FROM pg_constraint JOIN pg_class ON pg_class.oid = conrelid JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace WHERE pg_namespace.nspname = %s AND pg_class.relname = %s', [state['schema'], _TARGET_TABLE])
        cons = cur.fetchall()
    checks = {name for name, kind in cons if kind == 'c'}
    assert checks == {'bulkexportmanifest_version_exact', 'bulkexportmanifest_operation_non_empty', 'bulkexportmanifest_format_member', 'bulkexportmanifest_mapping_ref_non_empty', 'bulkexportmanifest_mapping_version_non_empty', 'bulkexportmanifest_tenant_non_empty', 'bulkexportmanifest_consistency_member', 'bulkexportmanifest_consistency_ref_non_empty', 'bulkexportmanifest_sha_regex', 'bulkexportmanifest_classification_non_empty', 'bulkexportmanifest_object_ref_non_empty', 'bulkexportmanifest_object_version_non_empty', 'bulkexportmanifest_scope_non_empty', 'bulkexportmanifest_row_count_regex', 'bulkexportmanifest_size_bytes_regex'}
    assert len(checks) == 15
    assert [name for name, kind in cons if kind == 'p'] == [_TARGET_TABLE + '_pkey']
    assert not [name for name, kind in cons if kind in ['u', 'f']]
    result['forward_applied'] = True
    result['physical_exact'] = True
    repo = BulkExportManifestRepository()
    result['phase'] = 'DATA'
    _mid_base = None
    with transaction.atomic(using='default'):
        _caller = dict(_base17)
        _mid_base = repo.insert_manifest(values=_caller)
        _caller['operation_id'] = 'caller-mute'
        _caller['row_count'] = 999
        _got_base = repo.get_manifest(manifest_id=_mid_base)
        assert type(_got_base) is not Model
        assert not hasattr(_got_base, 'as_values')
        _vals_base = _helper_to_values(_got_base)
        assert list(_vals_base.keys()) == ['manifest_version', 'operation_id', 'format', 'mapping_reference', 'mapping_version', 'tenant_context_reference', 'scope_context_reference', 'consistency_kind', 'consistency_reference', 'row_count', 'size_bytes', 'sha256', 'classification_reference', 'expires_at', 'object_reference', 'object_version', 'complete']
        assert _vals_base == _base17
        try:
            _got_base.complete = False
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('bound modifiable')
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_base)) == _base17
    result['roundtrip_17'] = True
    result['owned_frozen'] = True
    with transaction.atomic(using='default'):
        _mid_none = repo.insert_manifest(values=_none17)
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_none)) == _none17
        _nd = dict(_base17)
        _nd['format'] = 'NDJSON'
        _nd['consistency_kind'] = 'WATERMARK'
        _nd['operation_id'] = 'op-synthetic-10'
        _mid_nd = repo.insert_manifest(values=_nd)
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_nd)) == _nd
    result['none_complete_modes'] = True
    _min = datetime(1, 1, 1, tzinfo=timezone.utc)
    _max = datetime(9999, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    with transaction.atomic(using='default'):
        _mid_min = repo.insert_manifest(values=dict(_base17, expires_at=_min, operation_id='op-synthetic-11'))
        _mid_max = repo.insert_manifest(values=dict(_base17, expires_at=_max, operation_id='op-synthetic-12'))
        assert repo.get_manifest(manifest_id=_mid_min).expires_at.tzinfo is timezone.utc
        assert repo.get_manifest(manifest_id=_mid_max).expires_at.tzinfo is timezone.utc
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_min))['expires_at'] == _min
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_max))['expires_at'] == _max
    result['utc_identity_bounds'] = True
    _big = 9223372036854775807 + 123
    _sup600 = 10 ** 600
    with transaction.atomic(using='default'):
        _mid_big = repo.insert_manifest(values=dict(_base17, row_count=_big, size_bytes=_big, operation_id='op-synthetic-13'))
        _mid_600 = repo.insert_manifest(values=dict(_base17, row_count=_sup600, size_bytes=_sup600, operation_id='op-synthetic-14'))
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_big))['row_count'] == _big
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_600))['row_count'] == _sup600
        with connection.cursor() as cur:
            cur.execute(table_sql('SELECT row_count, size_bytes FROM {}.{} WHERE id = %s'), [_mid_big])
            _raw_big = cur.fetchone()
        assert type(_raw_big[0]) is str and _raw_big[0] == str(_big)
    result['bigint_text'] = True
    with transaction.atomic(using='default'):
        _same_op = 'op-synthetic-same'
        _m1 = repo.insert_manifest(values=dict(_base17, operation_id=_same_op))
        _m2 = repo.insert_manifest(values=dict(_base17, operation_id=_same_op))
        assert _m1 != _m2
        assert _helper_to_values(repo.get_manifest(manifest_id=_m1))['operation_id'] == _same_op
        assert _helper_to_values(repo.get_manifest(manifest_id=_m2))['operation_id'] == _same_op
    result['same_operation_ids'] = True
    with connection.cursor() as cur:
        cur.execute(sql.SQL('CREATE TABLE {}.{} (id bigint PRIMARY KEY)').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection))
    with transaction.atomic(using='default'):
        _mid_co = repo.insert_manifest(values=dict(_base17, operation_id='op-synthetic-20'))
        with connection.cursor() as cur:
            cur.execute(sql.SQL('INSERT INTO {}.{} (id) VALUES (%s)').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [_mid_co])
    with connection.cursor() as cur:
        cur.execute(sql.SQL('SELECT COUNT(*) FROM {}.{} WHERE id = %s').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [_mid_co])
        assert cur.fetchone()[0] == 1
        assert _helper_to_values(repo.get_manifest(manifest_id=_mid_co))['operation_id'] == 'op-synthetic-20'
    result['co_commit'] = True
    try:
        with transaction.atomic(using='default'):
            _mid_rb = repo.insert_manifest(values=dict(_base17, operation_id='op-synthetic-21'))
            with connection.cursor() as cur:
                cur.execute(sql.SQL('INSERT INTO {}.{} (id) VALUES (%s)').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [_mid_rb])
            raise RuntimeError('rollback attendu')
    except RuntimeError:
        pass
    with connection.cursor() as cur:
        cur.execute(sql.SQL('SELECT COUNT(*) FROM {}.{} WHERE id = %s').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [_mid_rb])
        assert cur.fetchone()[0] == 0
        assert repo.get_manifest(manifest_id=_mid_rb) is None
    result['co_rollback'] = True
    with transaction.atomic(using='default'):
        _mid_obs = repo.insert_manifest(values=dict(_base17, operation_id='op-synthetic-30'))
        with connection.cursor() as cur:
            cur.execute(sql.SQL('INSERT INTO {}.{} (id) VALUES (%s)').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [_mid_obs + 1000000])
        other = connections['other']
        assert h._scalar(other, 'SELECT current_schemas(false)', ()) == [state['schema'], 'pg_catalog']
        refs.append(other.connection)
        observer = BulkExportManifestRepository(using='other')
        assert observer.get_manifest(manifest_id=_mid_obs) is None
        with other.cursor() as cur:
            cur.execute(sql.SQL('SELECT COUNT(*) FROM {}.{} WHERE id = %s').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(other.connection), [_mid_obs + 1000000])
            assert cur.fetchone()[0] == 0
    assert _helper_to_values(observer.get_manifest(manifest_id=_mid_obs))['operation_id'] == 'op-synthetic-30'
    with other.cursor() as cur:
        cur.execute(sql.SQL('SELECT COUNT(*) FROM {}.{} WHERE id = %s').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(other.connection), [_mid_obs + 1000000])
        assert cur.fetchone()[0] == 1
    with connection.cursor() as cur:
        cur.execute(sql.SQL('SELECT COUNT(*) FROM {}.{} WHERE id = %s').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [_mid_obs + 1000000])
        assert cur.fetchone()[0] == 1
    result['inflight_not_ready'] = True
    try:
        BulkExportManifestRepository(using='other').insert_manifest(values=dict(_base17, operation_id='op-synthetic-32'))
    except BulkExportManifestRefused:
        pass
    else:
        raise AssertionError('other sans owner accepte')
    result['alias_other_refused'] = True
    _hyd = Model.objects.using('default').get(id=_mid_base)
    _orig_op = _hyd.operation_id
    _hyd.operation_id = 'changed-hydrated-op'
    try:
        _hyd.save(force_insert=True, using='default')
    except ValidationError:
        pass
    else:
        raise AssertionError('hydrate accepte')
    assert Model.objects.using('default').get(id=_mid_base).operation_id == _orig_op
    result['hydrated_refused'] = True
    _defer = Model.objects.using('default').only('id').get(id=_mid_base)
    from django.test.utils import CaptureQueriesContext
    with CaptureQueriesContext(connection) as capture:
        for call in [lambda: _defer.as_values(), lambda: _defer.full_clean(exclude=['operation_id']), lambda: _defer.save(force_insert=True, using='default')]:
            try:
                call()
            except ValidationError:
                pass
            else:
                raise AssertionError('deferred accepte')
        assert len(capture) == 0
    result['deferred_refused'] = True
    from unittest import mock
    with mock.patch.object(Model.objects, 'using', side_effect=AssertionError('query id invalide')):
        for bad in (None, True, 0, -1, 2 ** 63):
            try:
                repo.get_manifest(manifest_id=bad)
            except BulkExportManifestRefused:
                pass
            else:
                raise AssertionError('mauvais id accepte')
    result['bad_id_before_query'] = True
    result['phase'] = 'CHECKS'
    _stor_rec = Model.from_values(_base17)
    _stor_map = {'manifest_version': _stor_rec.manifest_version, 'operation_id': _stor_rec.operation_id, 'format': _stor_rec.format, 'mapping_reference': _stor_rec.mapping_reference, 'mapping_version': _stor_rec.mapping_version, 'tenant_context_reference': _stor_rec.tenant_context_reference, 'scope_context_reference': _stor_rec.scope_context_reference, 'consistency_kind': _stor_rec.consistency_kind, 'consistency_reference': _stor_rec.consistency_reference, 'row_count': _stor_rec.row_count, 'size_bytes': _stor_rec.size_bytes, 'sha256': _stor_rec.sha256, 'classification_reference': _stor_rec.classification_reference, 'expires_at': _stor_rec.expires_at, 'object_reference': _stor_rec.object_reference, 'object_version': _stor_rec.object_version, 'complete': _stor_rec.complete}
    _cols17 = ['manifest_version', 'operation_id', 'format', 'mapping_reference', 'mapping_version', 'tenant_context_reference', 'scope_context_reference', 'consistency_kind', 'consistency_reference', 'row_count', 'size_bytes', 'sha256', 'classification_reference', 'expires_at', 'object_reference', 'object_version', 'complete']
    _vals17 = [_stor_map[k] for k in _cols17]
    def _raw_insert(over):
        _d = dict(zip(_cols17, _vals17))
        _d.update(over)
        _names_sql = sql.SQL(', ').join([sql.Identifier(k) for k in _cols17])
        _ph_sql = sql.SQL(', ').join([sql.SQL('%s') for k in _cols17])
        _q = sql.SQL('INSERT INTO {}.{} ({}) VALUES ({})').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE), _names_sql, _ph_sql).as_string(connection.connection)
        with connection.cursor() as cur:
            cur.execute(_q, [_d[k] for k in _cols17])
    _check_cases = [({'manifest_version': '2.0.0'}, 'bulkexportmanifest_version_exact'), ({'operation_id': ''}, 'bulkexportmanifest_operation_non_empty'), ({'format': 'XML'}, 'bulkexportmanifest_format_member'), ({'mapping_reference': ''}, 'bulkexportmanifest_mapping_ref_non_empty'), ({'mapping_version': ''}, 'bulkexportmanifest_mapping_version_non_empty'), ({'tenant_context_reference': ''}, 'bulkexportmanifest_tenant_non_empty'), ({'consistency_kind': 'BAD'}, 'bulkexportmanifest_consistency_member'), ({'consistency_reference': ''}, 'bulkexportmanifest_consistency_ref_non_empty'), ({'sha256': 'Z' * 64}, 'bulkexportmanifest_sha_regex'), ({'classification_reference': ''}, 'bulkexportmanifest_classification_non_empty'), ({'object_reference': ''}, 'bulkexportmanifest_object_ref_non_empty'), ({'object_version': ''}, 'bulkexportmanifest_object_version_non_empty'), ({'scope_context_reference': ''}, 'bulkexportmanifest_scope_non_empty'), ({'row_count': '01'}, 'bulkexportmanifest_row_count_regex'), ({'size_bytes': '-1'}, 'bulkexportmanifest_size_bytes_regex')]
    for _over, _exp in _check_cases:
        try:
            with transaction.atomic(using='default'):
                _raw_insert(_over)
        except IntegrityError as _err:
            assert _err.__cause__.sqlstate == '23514'
            assert _err.__cause__.diag.constraint_name == _exp
        else:
            raise AssertionError('check accepte')
    result['sql_constraints'] = True
    for _bad in ['', '01', '-1', '+1', ' 1', '1 ', chr(1632) + chr(1633)]:
        try:
            with transaction.atomic(using='default'):
                _raw_insert({'row_count': _bad})
        except IntegrityError as _err:
            assert _err.__cause__.sqlstate == '23514'
            assert _err.__cause__.diag.constraint_name == 'bulkexportmanifest_row_count_regex'
        else:
            raise AssertionError('malforme accepte')
        try:
            with transaction.atomic(using='default'):
                _raw_insert({'size_bytes': _bad})
        except IntegrityError as _err:
            assert _err.__cause__.sqlstate == '23514'
            assert _err.__cause__.diag.constraint_name == 'bulkexportmanifest_size_bytes_regex'
        else:
            raise AssertionError('malforme accepte')
    result['malformed_refused'] = True
    with transaction.atomic(using='default'):
        _mid_mal = repo.insert_manifest(values=dict(_base17, operation_id='op-synthetic-40'))
    with connection.cursor() as cur:
        cur.execute(table_sql('UPDATE {}.{} SET mapping_version = %s WHERE id = %s'), ['1.2', _mid_mal])
    try:
        repo.get_manifest(manifest_id=_mid_mal)
    except BulkExportManifestRefused:
        pass
    else:
        raise AssertionError('semver invalide accepte')
    _lim = _sys.get_int_max_str_digits()
    assert _lim > 0
    _big740 = '9' * (_lim + 100)
    with connection.cursor() as cur:
        cur.execute(table_sql('UPDATE {}.{} SET mapping_version = %s, row_count = %s, size_bytes = %s WHERE id = %s'), ['1.2.3', _big740, _big740, _mid_mal])
    try:
        repo.get_manifest(manifest_id=_mid_mal)
    except BulkExportManifestRefused:
        pass
    else:
        raise AssertionError('capacite decode acceptee')
    with connection.cursor() as cur:
        cur.execute(table_sql('SELECT COUNT(*) FROM {}.{}'), [])
        _cnt_before = cur.fetchone()[0]
    try:
        with transaction.atomic(using='default'):
            repo.insert_manifest(values=dict(_base17, row_count=10 ** (_lim + 100), size_bytes=10 ** (_lim + 100), operation_id='op-synthetic-41'))
    except BulkExportManifestRefused as _err:
        assert isinstance(_err.__cause__, ValidationError)
        assert _err.__cause__.error_list[0].code == 'bulk_export_manifest_capacity_unsupported'
    else:
        raise AssertionError('capacite encode acceptee')
    with connection.cursor() as cur:
        cur.execute(table_sql('SELECT COUNT(*) FROM {}.{}'), [])
        assert cur.fetchone()[0] == _cnt_before
    assert _sys.get_int_max_str_digits() == _lim
    result['capacity_stdlib'] = True
    with connection.cursor() as cur:
        cur.execute(table_sql('SELECT COUNT(*) FROM {}.{}'), [])
        _cnt_pre = cur.fetchone()[0]
    try:
        repo.insert_manifest(values={})
    except BulkExportManifestRefused:
        pass
    else:
        raise AssertionError('prevalidation acceptee')
    with connection.cursor() as cur:
        cur.execute(table_sql('SELECT COUNT(*) FROM {}.{}'), [])
        assert cur.fetchone()[0] == _cnt_pre
    result['prevalidation_no_row'] = True
    for unowned in [repo, BulkExportManifestRepository(using='other')]:
        try:
            unowned.insert_manifest(values=dict(_base17, operation_id='op-unowned-default-or-other'))
        except BulkExportManifestRefused:
            pass
        else:
            raise AssertionError('insertion hors transaction proprietaire acceptee')
    assert Model.objects.using('default').count() == _cnt_pre
    _tmp_name = 'tmp_check_manifest_never_hit'
    _never = 'never-hit-tmp'
    with connection.cursor() as cur:
        cur.execute(sql.SQL('ALTER TABLE {}.{} ADD CONSTRAINT {} CHECK (operation_id <> {})').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE), sql.Identifier(_tmp_name), sql.Literal(_never)).as_string(connection.connection))
    with connection.cursor() as cur:
        cur.execute(table_sql('SELECT COUNT(*) FROM {}.{}'), [])
        _cnt_tmp_before = cur.fetchone()[0]
    try:
        with transaction.atomic(using='default'):
            with connection.cursor() as cur:
                cur.execute(sql.SQL('INSERT INTO {}.{} (id) VALUES (%s)').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [9999999])
            try:
                repo.insert_manifest(values=dict(_base17, operation_id=_never))
            except IntegrityError as err:
                assert err.__cause__.sqlstate == '23514'
                assert err.__cause__.diag.constraint_name == _tmp_name
                assert transaction.get_rollback(using='default') is True
                try:
                    with connection.cursor() as cur:
                        cur.execute('SELECT 1')
                except TransactionManagementError:
                    pass
                else:
                    raise AssertionError('transaction proprietaire doit rester invalide')
            else:
                raise AssertionError('CHECK temporaire non propage')
    finally:
        with connection.cursor() as cur:
            cur.execute(sql.SQL('ALTER TABLE {}.{} DROP CONSTRAINT {}').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE), sql.Identifier(_tmp_name)).as_string(connection.connection))
    with connection.cursor() as cur:
        cur.execute(sql.SQL('SELECT COUNT(*) FROM {}.{} WHERE id = %s').format(sql.Identifier(state['schema']), sql.Identifier('synthetic_owner')).as_string(connection.connection), [9999999])
        assert cur.fetchone()[0] == 0
        cur.execute(table_sql('SELECT COUNT(*) FROM {}.{}'), [])
        assert cur.fetchone()[0] == _cnt_tmp_before
    result['temp_check_propagates'] = True
    MigrationExecutor(connection).migrate([('backend', '0009_bulk_validation_report')])
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert h._applied_count(connection, state['schema'], '0010_bulk_export_manifest') == 0
    _after = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert _after == before
    result['reverse_only_0010'] = True
    result['existing_tables_stable'] = True
    result['phase'] = 'COMPLETE'
def run_real_bulk_export_manifest_postgres(root_str):
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
        assert callable(harness.run_real_bulk_export_manifest_postgres)
        for bad_root in (None, '', 0, b'/home/devops/datas/pixs'):
            outcome = harness.run_real_bulk_export_manifest_postgres(bad_root)
            assert outcome['real_pg'] is False
            assert outcome['phase'] == 'COMPLETE'
            assert outcome['reason'] == 'ROOT_INVALID'
        outcome = harness.run_real_bulk_export_manifest_postgres('/synthetic/root')
        assert outcome['reason'] == 'ROOT_MISMATCH'
        assert outcome['real_pg'] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [g.call_count for g in guards] == [0] * len(guards)
    print('BULK_EXPORT_MANIFEST_PG_HARNESS_SAFE_OK')
    ''').strip()
_MARKER = 'BULK_EXPORT_MANIFEST_PG_HARNESS_SAFE_OK' + chr(10)
class BulkExportManifestPostgresInertTests(unittest.TestCase):
    def test_harness_safe(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-c', _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)
        self.assertEqual(result.stderr, '')
if __name__ == '__main__':
    unittest.main()
