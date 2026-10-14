'''Preuves PostgreSQL isolees OutboxPublicationV1 initiales ; import et tests ordinaires inertes.'''
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
_FLAGS = ('search_path_isolated', 'forward_applied', 'physical_exact', 'models_migration_coherent', 'roundtrip_12', 'owned_frozen', 'revision_preserved', 'nullable_preserved', 'catalogue_required', 'prevalidation_no_query', 'scope_derivation', 'unique_event', 'scope_seq_unique', 'scope_counter_atomic', 'owner_envelope_cocommit', 'owner_rollback', 'duplicate_rolls_owner', 'db_error_rolls_owner', 'inflight_not_available', 'utc_identity', 'bigint_text', 'capacity_stdlib', 'full_clean_no_fk_query', 'hydrated_refused', 'deferred_refused', 'scope_mismatch_failclosed', 'same_scope_race', 'independent_scope_progress', 'thread_conns_closed', 'sql_constraints', 'reverse_only_0011', 'existing_tables_stable', 'public_tables_stable')
_BASE_TABLES = ('backend_featureflagsourcesnapshotrecord', 'backend_jobrecord', 'backend_bulkoperationrecord', 'backend_bulkoperationexecutionrecord', 'backend_bulkcheckpointrecord', 'backend_bulkjobbindingrecord', 'backend_bulkjobschedulerecord', 'backend_bulkadmissionidentityrecord', 'backend_bulkcommandidempotencyrecord', 'backend_bulkeventenveloperecord', 'backend_bulkinboxreceiptrecord', 'backend_bulkvalidationreportrecord', 'backend_bulkexportmanifestrecord')
_TARGET_TABLE = 'backend_bulkoutboxpublicationrecord'
_COUNTER_TABLE = 'backend_bulkoutboxscopecounterrecord'
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
    from psycopg import sql
    result['phase'] = 'SCHEMA'
    with h._managed_pg_connection(*state['credentials'], refs, failures) as admin:
        result['server_version_num'] = int(h._scalar(admin, 'SHOW server_version_num', ()))
        state['public_before'] = [h._table_identity(admin, 'public', t) for t in (*state['tables'], _TARGET_TABLE, _COUNTER_TABLE, 'django_migrations')]
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
    settings.configure(INSTALLED_APPS=['pixs.backend'], SECRET_KEY='bulk-outbox-synthetic-test', DATABASES={'default': db_config, 'other': dict(db_config)}, LOGGING_CONFIG=None, MIDDLEWARE=(), USE_TZ=True)
    state['configured'] = True
    django.setup()
    if h._scalar(connection, 'SELECT current_schemas(false)', ()) != [state['schema'], 'pg_catalog']:
        result['reason'] = 'SEARCH_PATH_MISMATCH'
        return
    refs.append(connection.connection)
    result['search_path_isolated'] = True
    from pixs.backend.bulk_event_envelope_record import BulkEventEnvelopeRecord as EnvModel
    from pixs.backend.bulk_event_envelope_repository import BulkEventEnvelopeRepository
    from pixs.backend.bulk_outbox_publication_record import BulkOutboxPublicationRecord as Model
    from pixs.backend.bulk_outbox_publication_record import BulkOutboxScopeCounterRecord as Counter
    from pixs.backend.bulk_outbox_publication_repository import BulkOutboxPublicationRepository
    from datetime import datetime, timezone
    _UTC = timezone.utc
    _OCCURRED = datetime(2030, 1, 1, tzinfo=timezone.utc)
    _LEASE_AT = datetime(2030, 2, 1, tzinfo=timezone.utc)
    _NEXT_AT = datetime(2030, 3, 1, tzinfo=timezone.utc)
    _PUBLISHED_AT = datetime(2030, 4, 1, tzinfo=timezone.utc)
    _CANON12 = ('event_id', 'state', 'attempt_count', 'lease_owner', 'lease_expires_at', 'next_attempt_at', 'published_at', 'failure_code', 'sequence_index', 'policy_reference', 'policy_version', 'revision')
    _LIMITS = {'max_depth': 8, 'max_members': 10, 'non_tenant_authorized': False}
    result['phase'] = 'MIGRATE'
    MigrationExecutor(connection).migrate([('backend', '0010_bulk_export_manifest')])
    before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert len(before) == 13 and all(before)
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert not h._table_exists(connection, state['schema'], _COUNTER_TABLE)
    MigrationExecutor(connection).migrate([('backend', '0011_bulk_outbox_publication')])
    assert h._applied_count(connection, state['schema'], '0011_bulk_outbox_publication') == 1
    with connection.cursor() as cur:
        cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name LIKE %s ORDER BY table_name', [state['schema'], 'backend_%'])
        _backend_tables = [r[0] for r in cur.fetchall()]
    assert len(_backend_tables) == 15
    with connection.cursor() as cur:
        cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position', [state['schema'], _TARGET_TABLE])
        cols = cur.fetchall()
    assert [c[0] for c in cols] == ['event_id', 'state', 'attempt_count', 'lease_owner', 'lease_expires_at', 'next_attempt_at', 'published_at', 'failure_code', 'sequence_index', 'policy_reference', 'policy_version', 'revision', 'order_scope_reference_private']
    assert len(cols) == 13
    _types = dict(cols)
    assert _types['lease_expires_at'] == 'timestamp with time zone' and _types['next_attempt_at'] == 'timestamp with time zone' and _types['published_at'] == 'timestamp with time zone'
    assert all(v == 'text' for k, v in cols if k not in ('lease_expires_at', 'next_attempt_at', 'published_at'))
    with connection.cursor() as cur:
        cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s ORDER BY ordinal_position', [state['schema'], _COUNTER_TABLE])
        _ccols = cur.fetchall()
    assert [c[0] for c in _ccols] == ['scope_private', 'next_index']
    assert all(v == 'text' for k, v in _ccols)
    with connection.cursor() as cur:
        cur.execute('SELECT conname, contype FROM pg_constraint JOIN pg_class ON pg_class.oid = conrelid JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace WHERE pg_namespace.nspname = %s AND pg_class.relname = %s', [state['schema'], _TARGET_TABLE])
        cons = cur.fetchall()
    _checks = {name for name, kind in cons if kind == 'c'}
    assert _checks == {'bulkoutbox_event_non_empty', 'bulkoutbox_state_member', 'bulkoutbox_scope_non_empty', 'bulkoutbox_attempt_codec', 'bulkoutbox_seq_codec', 'bulkoutbox_revision_codec', 'bulkoutbox_lease_pair', 'bulkoutbox_retrying_next', 'bulkoutbox_published_at', 'bulkoutbox_policy_ref_non_empty', 'bulkoutbox_policy_version_non_empty', 'bulkoutbox_lease_owner_empty', 'bulkoutbox_failure_code_empty'}
    assert [name for name, kind in cons if kind == 'p'] == [_TARGET_TABLE + '_pkey']
    assert [name for name, kind in cons if kind == 'u'] == ['bulkoutbox_scope_seq_unique']
    assert len([name for name, kind in cons if kind == 'f']) == 1
    with connection.cursor() as cur:
        cur.execute('SELECT conname, contype FROM pg_constraint JOIN pg_class ON pg_class.oid = conrelid JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace WHERE pg_namespace.nspname = %s AND pg_class.relname = %s', [state['schema'], _COUNTER_TABLE])
        _ccons = cur.fetchall()
    assert {name for name, kind in _ccons if kind == 'c'} == {'bulkoutboxcounter_scope_non_empty', 'bulkoutboxcounter_next_codec'}
    assert [name for name, kind in _ccons if kind == 'p'] == [_COUNTER_TABLE + '_pkey']
    with connection.cursor() as cur:
        details = connection.introspection.get_constraints(cur, _TARGET_TABLE)
        counters_details = connection.introspection.get_constraints(cur, _COUNTER_TABLE)
        cur.execute('SELECT table_name, column_name, collation_name FROM information_schema.columns WHERE table_schema = %s AND ((table_name = %s AND column_name = %s) OR (table_name = %s AND column_name = %s))', [state['schema'], _TARGET_TABLE, 'order_scope_reference_private', _COUNTER_TABLE, 'scope_private'])
        assert len(cur.fetchall()) == 2
        cur.execute('SELECT collation_name FROM information_schema.columns WHERE table_schema = %s AND ((table_name = %s AND column_name = %s) OR (table_name = %s AND column_name = %s))', [state['schema'], _TARGET_TABLE, 'order_scope_reference_private', _COUNTER_TABLE, 'scope_private'])
        assert [r[0] for r in cur.fetchall()] == ['C', 'C']
    assert details[_TARGET_TABLE + '_pkey']['columns'] == ['event_id']
    assert details['bulkoutbox_scope_seq_unique']['unique'] is True
    assert details['bulkoutbox_scope_seq_unique']['columns'] == ['order_scope_reference_private', 'sequence_index']
    assert [(d['columns'], d['foreign_key']) for d in details.values() if d['foreign_key']] == [(['event_id'], ('backend_bulkeventenveloperecord', 'event_id'))]
    assert counters_details[_COUNTER_TABLE + '_pkey']['columns'] == ['scope_private']
    result['forward_applied'] = True
    result['physical_exact'] = True
    from django.apps import apps as runtime_apps
    from django.db.migrations.loader import MigrationLoader
    from django.db.migrations.state import ProjectState
    migration_state = MigrationLoader(None).project_state([('backend', '0011_bulk_outbox_publication')])
    runtime_state = ProjectState.from_apps(runtime_apps)
    for model_name in ('bulkoutboxpublicationrecord', 'bulkoutboxscopecounterrecord'):
        expected = migration_state.models[('backend', model_name)]
        current = runtime_state.models[('backend', model_name)]
        assert set(expected.fields) == set(current.fields)
        for field_name in expected.fields:
            assert expected.fields[field_name].deconstruct()[1:] == current.fields[field_name].deconstruct()[1:]
        assert expected.options.get('db_table') == current.options.get('db_table')
        assert [c.deconstruct() for c in expected.options['constraints']] == [c.deconstruct() for c in current.options['constraints']]
    result['models_migration_coherent'] = True
    result['phase'] = 'DATA'
    def _env_values(event_id, scope):
        return {'event_id': event_id, 'kind': 'DOMAIN', 'event_type': 'type-test', 'event_version': '1.2.3', 'producer_reference': 'producer-test', 'schema_reference': 'schema-test', 'order_scope_reference': scope, 'occurred_at': _OCCURRED, 'subject_reference': 'subject-test', 'tenant_context_reference': 'tenant-test', 'correlation_id': 'correlation-test', 'causation_id': None, 'payload': {'name': 'value'}}
    def _source(event_id, **over):
        base = {'event_id': event_id, 'state': 'PENDING', 'attempt_count': 0, 'lease_owner': None, 'lease_expires_at': None, 'next_attempt_at': None, 'published_at': None, 'failure_code': None, 'policy_reference': 'policy-ref', 'policy_version': '1.2.3', 'revision': 7}
        base.update(over)
        return base
    def _put_envelope(alias, event_id, scope):
        _env_repo = BulkEventEnvelopeRepository(using=alias)
        return _env_repo.insert_envelope(values=_env_values(event_id, scope), max_depth=8, max_members=10, non_tenant_authorized=False)
    def _insert(repo, event_id, catalogue):
        return repo.insert_initial(**_source(event_id), failure_catalogue=catalogue)

    _repo = BulkOutboxPublicationRepository(using='default')
    _other_repo = BulkOutboxPublicationRepository(using='other')
    def _pub_sql(template):
        return sql.SQL(template).format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE)).as_string(connection.connection)
    def _cnt_sql(template):
        return sql.SQL(template).format(sql.Identifier(state['schema']), sql.Identifier(_COUNTER_TABLE)).as_string(connection.connection)
    result['phase'] = 'ROUNDTRIP_COCOMMIT_INFLIGHT'
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-001', 'scope-a')
        _b1 = _insert(_repo, 'evt-001', ())
        assert _b1.event_id == 'evt-001' and _b1.sequence_index == 1 and _b1.revision == 7
        assert list(type(_b1).__dataclass_fields__) == list(_CANON12)
        try:
            _b1.state = 'X'
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('bound modifiable')
        other = connections['other']
        assert h._scalar(other, 'SELECT current_schemas(false)', ()) == [state['schema'], 'pg_catalog']
        refs.append(other.connection)
        assert EnvModel.objects.using('other').filter(event_id='evt-001').first() is None
        assert Model.objects.using('other').filter(event_id='evt-001').first() is None
        assert Counter.objects.using('other').filter(scope_private='scope-a').first() is None
    result['inflight_not_available'] = True
    _g1 = _other_repo.get_publication(event_id='evt-001', failure_catalogue=())
    assert _g1 is not None and list(type(_g1).__dataclass_fields__) == list(_CANON12)
    assert (_g1.event_id, _g1.state, _g1.attempt_count, _g1.sequence_index, _g1.revision) == ('evt-001', 'PENDING', 0, 1, 7)
    assert (_g1.lease_owner, _g1.lease_expires_at, _g1.next_attempt_at, _g1.published_at, _g1.failure_code) == (None, None, None, None, None)
    with connection.cursor() as cur:
        cur.execute(_pub_sql('SELECT sequence_index, revision, order_scope_reference_private FROM {}.{} WHERE event_id = %s'), ['evt-001'])
        _raw1 = cur.fetchone()
        cur.execute(_cnt_sql('SELECT next_index FROM {}.{} WHERE scope_private = %s'), ['scope-a'])
        _rawc1 = cur.fetchone()
    assert _raw1 == ('1', '7', 'scope-a')
    assert _rawc1 == ('2',)
    result['roundtrip_12'] = True
    result['owned_frozen'] = True
    result['revision_preserved'] = True
    result['scope_derivation'] = True
    result['owner_envelope_cocommit'] = True
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-002', 'scope-a')
        _b2 = _insert(_repo, 'evt-002', ())
        assert _b2.sequence_index == 2
    with connection.cursor() as cur:
        cur.execute(_cnt_sql('SELECT next_index FROM {}.{} WHERE scope_private = %s'), ['scope-a'])
        assert cur.fetchone() == ('3',)
    result['scope_counter_atomic'] = True
    result['phase'] = 'NULLABLES_UTC'
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-010', 'scope-b')
        _bfull = _repo.insert_initial(**_source('evt-010', lease_owner='owner-1', lease_expires_at=_LEASE_AT, next_attempt_at=_NEXT_AT, published_at=_PUBLISHED_AT, failure_code='E_CONN-RESET.v2:retry'), failure_catalogue=('E_CONN-RESET.v2:retry',))
        assert _bfull.failure_code == 'E_CONN-RESET.v2:retry' and _bfull.lease_owner == 'owner-1'
        assert _bfull.lease_expires_at.tzinfo is _UTC and _bfull.next_attempt_at.tzinfo is _UTC and _bfull.published_at.tzinfo is _UTC
    _gfull = _repo.get_publication(event_id='evt-010', failure_catalogue=('E_CONN-RESET.v2:retry',))
    assert (_gfull.lease_owner, _gfull.lease_expires_at, _gfull.next_attempt_at, _gfull.published_at, _gfull.failure_code) == ('owner-1', _LEASE_AT, _NEXT_AT, _PUBLISHED_AT, 'E_CONN-RESET.v2:retry')
    result['nullable_preserved'] = True
    result['utc_identity'] = True
    from django.test.utils import CaptureQueriesContext
    from django.db.transaction import TransactionManagementError
    result['phase'] = 'PREVALIDATION_NO_QUERY'
    with CaptureQueriesContext(connection) as _cap:
        try:
            _repo.get_publication(event_id='evt-absent-xyz', failure_catalogue=['E'])
        except ValidationError:
            pass
        else:
            raise AssertionError('catalogue invalide avant ORM absent')
        for _over in ({'revision': True}, {'state': 'PUBLISHED', 'published_at': _PUBLISHED_AT}, {'attempt_count': 1}, {'policy_version': '1.2'}):
            try:
                _repo.insert_initial(**_source('evt-absent-xyz', **_over), failure_catalogue=())
            except ValidationError:
                pass
            else:
                raise AssertionError('source invalide avant requete absente')
        for _kwargs in (_source('evt-absent-xyz'), dict(_source('evt-absent-xyz'), sequence_index=9, failure_catalogue=()), {k: v for k, v in dict(_source('evt-absent-xyz'), failure_catalogue=()).items() if k != 'lease_owner'}):
            try:
                _repo.insert_initial(**_kwargs)
            except TypeError:
                pass
            else:
                raise AssertionError('OUTBOX_TEST_REQUIRED_ARGUMENT_ACCEPTED')
        assert len(_cap) == 0
    result['catalogue_required'] = True
    result['prevalidation_no_query'] = True
    try:
        _repo.get_publication(event_id='evt-010', failure_catalogue=())
    except ValidationError:
        pass
    else:
        raise AssertionError('code non vide catalogue vide accepte')
    class _ExpectedOwnerRollback(Exception):
        pass
    result['phase'] = 'OWNER_ROLLBACK'
    try:
        with transaction.atomic(using='default'):
            _put_envelope('default', 'evt-rb', 'scope-rb')
            _insert(_repo, 'evt-rb', ())
            raise _ExpectedOwnerRollback()
    except _ExpectedOwnerRollback:
        pass
    assert EnvModel.objects.using('default').filter(event_id='evt-rb').first() is None
    assert Model.objects.using('default').filter(event_id='evt-rb').first() is None
    assert Counter.objects.using('default').filter(scope_private='scope-rb').first() is None
    result['owner_rollback'] = True
    result['phase'] = 'DUPLICATE_ROLLS_OWNER'
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-annex-1', 'scope-a')
        try:
            _insert(_repo, 'evt-001', ())
        except IntegrityError as _derr:
            assert _derr.__cause__.sqlstate == '23505'
            assert _derr.__cause__.diag.table_name == _TARGET_TABLE
            assert _derr.__cause__.diag.constraint_name == _TARGET_TABLE + '_pkey'
            assert transaction.get_rollback(using='default') is True
            try:
                with connection.cursor() as cur:
                    cur.execute('SELECT 1')
            except TransactionManagementError:
                pass
            else:
                raise AssertionError('owner doit rester invalide')
        else:
            raise AssertionError('duplicata accepte')
    assert EnvModel.objects.using('default').filter(event_id='evt-annex-1').first() is None
    with connection.cursor() as cur:
        cur.execute(_cnt_sql('SELECT next_index FROM {}.{} WHERE scope_private = %s'), ['scope-a'])
        assert cur.fetchone() == ('3',)
    _gold = _repo.get_publication(event_id='evt-001', failure_catalogue=())
    assert _gold.sequence_index == 1
    result['unique_event'] = True
    result['duplicate_rolls_owner'] = True

    from django.test.utils import CaptureQueriesContext as _CQC
    from django.db.transaction import TransactionManagementError as _TME
    result['phase'] = 'MODEL_GATES_NO_FK'
    _loaded = Model.objects.using('default').get(event_id='evt-001')
    _loaded._outbox_catalogue = ()
    _all_fields = [f.name for f in Model._meta.local_fields]
    with _CQC(connection) as _cap0:
        _loaded.full_clean(exclude=_all_fields)
        assert len(_cap0) == 0
    result['full_clean_no_fk_query'] = True
    try:
        _loaded.save(force_insert=True, using='default')
    except ValidationError:
        pass
    else:
        raise AssertionError('hydrate accepte')
    assert Model.objects.using('default').get(event_id='evt-001').order_scope_reference_private == 'scope-a'
    result['hydrated_refused'] = True
    _deferred = Model.objects.using('default').only('event').get(event_id='evt-001')
    _deferred._outbox_catalogue = ()
    with _CQC(connection) as _cap1:
        for _call in (lambda: _deferred.as_values(), lambda: _deferred.full_clean(exclude=_all_fields)):
            try:
                _call()
            except ValidationError:
                pass
            else:
                raise AssertionError('deferred accepte')
        assert len(_cap1) == 0
    result['deferred_refused'] = True
    result['phase'] = 'SCOPE_MISMATCH'
    with connection.cursor() as cur:
        cur.execute(_pub_sql('UPDATE {}.{} SET order_scope_reference_private = %s WHERE event_id = %s'), ['scope-corrupt', 'evt-001'])
    try:
        _repo.get_publication(event_id='evt-001', failure_catalogue=())
    except ValidationError:
        pass
    else:
        raise AssertionError('scope incoherent accepte')
    with connection.cursor() as cur:
        cur.execute(_pub_sql('UPDATE {}.{} SET order_scope_reference_private = %s WHERE event_id = %s'), ['scope-a', 'evt-001'])
    assert _repo.get_publication(event_id='evt-001', failure_catalogue=()).sequence_index == 1
    result['scope_mismatch_failclosed'] = True
    result['phase'] = 'BIGINT_TEXT'
    _bigseq = 2 ** 100
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-big', 'scope-big')
        _seed = Counter(scope_private='scope-big', next_index=str(_bigseq))
        _seed.save(force_insert=True, using='default')
        _bbig = _repo.insert_initial(**_source('evt-big', revision=_bigseq), failure_catalogue=())
        assert _bbig.sequence_index == _bigseq and _bbig.revision == _bigseq
        try:
            _bbig.sequence_index = -1
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError('bound modifiable')
    with connection.cursor() as cur:
        cur.execute(_pub_sql('SELECT sequence_index, revision FROM {}.{} WHERE event_id = %s'), ['evt-big'])
        assert cur.fetchone() == (str(_bigseq), str(_bigseq))
        cur.execute(_cnt_sql('SELECT next_index FROM {}.{} WHERE scope_private = %s'), ['scope-big'])
        assert cur.fetchone() == (str(_bigseq + 1),)
    result['bigint_text'] = True
    result['phase'] = 'CAPACITY_STDLIB'
    assert _sys.get_int_max_str_digits() == 640
    _cap_rev = 10 ** 640
    with connection.cursor() as cur:
        cur.execute(_pub_sql('SELECT COUNT(*) FROM {}.{}'), [])
        _cnt_pub0 = cur.fetchone()[0]
        cur.execute(_cnt_sql('SELECT COUNT(*) FROM {}.{}'), [])
        _cnt_cnt0 = cur.fetchone()[0]
    with _CQC(connection) as _cap2:
        try:
            _repo.insert_initial(**_source('evt-cap-1', revision=_cap_rev), failure_catalogue=())
        except ValidationError as _cerr:
            assert all(i.code == 'bulk_outbox_publication_capacity_unsupported' for i in _cerr.error_list)
        else:
            raise AssertionError('capacite encode acceptee')
        assert len(_cap2) == 0
    with connection.cursor() as cur:
        cur.execute(_pub_sql('SELECT COUNT(*) FROM {}.{}'), [])
        assert cur.fetchone()[0] == _cnt_pub0
        cur.execute(_cnt_sql('SELECT COUNT(*) FROM {}.{}'), [])
        assert cur.fetchone()[0] == _cnt_cnt0
    _long701 = '7' + '0' * 700
    with connection.cursor() as cur:
        cur.execute(_pub_sql('UPDATE {}.{} SET revision = %s WHERE event_id = %s'), [_long701, 'evt-001'])
    try:
        _repo.get_publication(event_id='evt-001', failure_catalogue=())
    except ValidationError as _cerr2:
        assert all(i.code == 'bulk_outbox_publication_capacity_unsupported' for i in _cerr2.error_list)
    else:
        raise AssertionError('capacite decode acceptee')
    with connection.cursor() as cur:
        cur.execute(_pub_sql('UPDATE {}.{} SET revision = %s WHERE event_id = %s'), ['7', 'evt-001'])
    assert _repo.get_publication(event_id='evt-001', failure_catalogue=()).revision == 7
    result['capacity_stdlib'] = True
    result['phase'] = 'DB_ERROR_ROLLS_OWNER'
    _tmp = 'tmp_outbox_reject_policy'
    with connection.cursor() as cur:
        cur.execute(sql.SQL('ALTER TABLE {}.{} ADD CONSTRAINT {} CHECK (policy_reference <> {})').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE), sql.Identifier(_tmp), sql.Literal('reject-policy')).as_string(connection.connection))
    try:
        with transaction.atomic(using='default'):
            _put_envelope('default', 'evt-dberr', 'scope-db-error')
            try:
                _repo.insert_initial(**_source('evt-dberr', policy_reference='reject-policy'), failure_catalogue=())
            except IntegrityError as _e23514:
                assert _e23514.__cause__.sqlstate == '23514'
                assert _e23514.__cause__.diag.constraint_name == _tmp
                assert transaction.get_rollback(using='default') is True
                try:
                    with connection.cursor() as cur2:
                        cur2.execute('SELECT 1')
                except _TME:
                    pass
                else:
                    raise AssertionError('owner doit rester invalide')
            else:
                raise AssertionError('CHECK temporaire non propage')
    finally:
        with connection.cursor() as cur3:
            cur3.execute(sql.SQL('ALTER TABLE {}.{} DROP CONSTRAINT {}').format(sql.Identifier(state['schema']), sql.Identifier(_TARGET_TABLE), sql.Identifier(_tmp)).as_string(connection.connection))
    assert EnvModel.objects.using('default').filter(event_id='evt-dberr').first() is None
    assert Model.objects.using('default').filter(event_id='evt-dberr').first() is None
    assert Counter.objects.using('default').filter(scope_private='scope-db-error').first() is None
    result['db_error_rolls_owner'] = True

    result['phase'] = 'CONCURRENCY'
    import threading as _threading
    import time as _time
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-race-a1', 'scope-race-a')
        _put_envelope('default', 'evt-race-a2', 'scope-race-a')
        _put_envelope('default', 'evt-race-b1', 'scope-race-b')
    _first_ready = _threading.Event()
    _release_first = _threading.Event()
    _a2_started = _threading.Event()
    _errors = {}
    _pids = {}
    _closed = {}
    def _worker_close(name):
        wrapper = connections['default']
        native = wrapper.connection
        if native is not None:
            refs.append(native)
        try:
            wrapper.close()
        finally:
            _closed[name] = wrapper.connection is None
    def _w_a1():
        try:
            from django.db import connections as _c, transaction as _t
            from pixs.backend.bulk_outbox_publication_repository import BulkOutboxPublicationRepository as _R
            _r = _R(using='default')
            with _t.atomic(using='default'):
                with _c['default'].cursor() as _cur:
                    _cur.execute('SELECT pg_backend_pid()')
                    _pids['a1'] = _cur.fetchone()[0]
                _r.insert_initial(**_source('evt-race-a1'), failure_catalogue=())
                _first_ready.set()
                if not _release_first.wait(timeout=8):
                    raise TimeoutError('OUTBOX_TEST_RELEASE_TIMEOUT')
        except BaseException as _e:
            _errors['a1'] = type(_e).__name__
        finally:
            _worker_close('a1')
    def _w_a2():
        try:
            from django.db import connections as _c, transaction as _t
            from pixs.backend.bulk_outbox_publication_repository import BulkOutboxPublicationRepository as _R
            _r = _R(using='default')
            with _t.atomic(using='default'):
                with _c['default'].cursor() as _cur:
                    _cur.execute('SELECT pg_backend_pid()')
                    _pids['a2'] = _cur.fetchone()[0]
                _a2_started.set()
                _r.insert_initial(**_source('evt-race-a2'), failure_catalogue=())
        except BaseException as _e:
            _errors['a2'] = type(_e).__name__
        finally:
            _worker_close('a2')
    def _w_b():
        try:
            from django.db import transaction as _t
            from pixs.backend.bulk_outbox_publication_repository import BulkOutboxPublicationRepository as _R
            _r = _R(using='default')
            with _t.atomic(using='default'):
                _r.insert_initial(**_source('evt-race-b1'), failure_catalogue=())
        except BaseException as _e:
            _errors['b'] = type(_e).__name__
        finally:
            _worker_close('b')
    _t1 = _threading.Thread(target=_w_a1, name='race-a1')
    _t2 = _threading.Thread(target=_w_a2, name='race-a2')
    _t3 = _threading.Thread(target=_w_b, name='race-b')
    try:
        _t1.start()
        assert _first_ready.wait(timeout=8)
        _t2.start()
        assert _a2_started.wait(timeout=8)
        _deadline = _time.monotonic() + 2.0
        _seen_block = False
        while _time.monotonic() < _deadline:
            with connection.cursor() as _cur:
                _cur.execute('SELECT pg_blocking_pids(%s)', [_pids['a2']])
                _blockers = _cur.fetchone()[0]
            if _pids.get('a1') in list(_blockers or []):
                _seen_block = True
                break
            _time.sleep(0.01)
        assert _seen_block
        assert _t2.is_alive()
        _t3.start()
        _t3.join(timeout=10)
        assert not _t3.is_alive()
        _gb = _repo.get_publication(event_id='evt-race-b1', failure_catalogue=())
        assert _gb is not None and _gb.sequence_index == 1
        with connection.cursor() as _cur:
            _cur.execute(_cnt_sql('SELECT next_index FROM {}.{} WHERE scope_private = %s'), ['scope-race-b'])
            assert _cur.fetchone() == ('2',)
    finally:
        _release_first.set()
        for _t in (_t1, _t2, _t3):
            if _t.ident is not None:
                _t.join(timeout=10)
    assert not _t1.is_alive() and not _t2.is_alive() and not _t3.is_alive()
    assert _errors == {}
    assert _closed.get('a1') is True and _closed.get('a2') is True and _closed.get('b') is True
    result['thread_conns_closed'] = True
    _ga1 = _repo.get_publication(event_id='evt-race-a1', failure_catalogue=())
    _ga2 = _repo.get_publication(event_id='evt-race-a2', failure_catalogue=())
    assert (_ga1.sequence_index, _ga2.sequence_index) == (1, 2)
    with connection.cursor() as _cur:
        _cur.execute(_cnt_sql('SELECT next_index FROM {}.{} WHERE scope_private = %s'), ['scope-race-a'])
        assert _cur.fetchone() == ('3',)
    result['same_scope_race'] = True
    result['independent_scope_progress'] = True
    result['phase'] = 'SQL_CONSTRAINTS'
    def _valid_pub(_eid, _scope):
        return {'event_id': _eid, 'state': 'PENDING', 'attempt_count': '0', 'lease_owner': None, 'lease_expires_at': None, 'next_attempt_at': None, 'published_at': None, 'failure_code': None, 'sequence_index': '1', 'policy_reference': 'policy-ref', 'policy_version': '1.2.3', 'revision': '7', 'order_scope_reference_private': _scope}
    _cases = [('bulkoutbox_event_non_empty', {'event_id': ''}, False), ('bulkoutbox_state_member', {'state': 'NOPE'}, True), ('bulkoutbox_scope_non_empty', {'order_scope_reference_private': ''}, True), ('bulkoutbox_attempt_codec', {'attempt_count': '01'}, True), ('bulkoutbox_seq_codec', {'sequence_index': '0'}, True), ('bulkoutbox_revision_codec', {'revision': '0'}, True), ('bulkoutbox_lease_pair', {'lease_owner': 'o1'}, True), ('bulkoutbox_retrying_next', {'state': 'RETRYING'}, True), ('bulkoutbox_published_at', {'state': 'PUBLISHED'}, True), ('bulkoutbox_policy_ref_non_empty', {'policy_reference': ''}, True), ('bulkoutbox_policy_version_non_empty', {'policy_version': ''}, True), ('bulkoutbox_lease_owner_empty', {'lease_owner': '', 'lease_expires_at': _LEASE_AT}, True), ('bulkoutbox_failure_code_empty', {'failure_code': ''}, True)]
    for _i, (_cname, _mut, _need_env) in enumerate(_cases):
        _eid = 'evt-chk-%02d' % _i
        _scope = 'scope-chk-%02d' % _i
        try:
            with transaction.atomic(using='default'):
                if _need_env:
                    _put_envelope('default', _eid, _scope)
                _row = Model(**dict(dict(_valid_pub(_eid if _cname != 'bulkoutbox_event_non_empty' else '', _scope), **_mut)))
                Model.objects.using('default').bulk_create([_row])
        except IntegrityError as _ex:
            assert _ex.__cause__.sqlstate == '23514'
            assert _ex.__cause__.diag.constraint_name == _cname
            assert _ex.__cause__.diag.table_name == _TARGET_TABLE
        else:
            raise AssertionError('check accepte ' + _cname)
    for _cname2, _kwargs in (('bulkoutboxcounter_scope_non_empty', {'scope_private': '', 'next_index': '1'}), ('bulkoutboxcounter_next_codec', {'scope_private': 'scope-counter-chk', 'next_index': '0'})):
        try:
            with transaction.atomic(using='default'):
                Counter.objects.using('default').bulk_create([Counter(**_kwargs)])
        except IntegrityError as _ex2:
            assert _ex2.__cause__.sqlstate == '23514'
            assert _ex2.__cause__.diag.constraint_name == _cname2
            assert _ex2.__cause__.diag.table_name == _COUNTER_TABLE
        else:
            raise AssertionError('counter check accepte ' + _cname2)
    with transaction.atomic(using='default'):
        _put_envelope('default', 'evt-unique-dup', 'scope-a')
    try:
        with transaction.atomic(using='default'):
            Model.objects.using('default').bulk_create([Model(**_valid_pub('evt-unique-dup', 'scope-a'))])
    except IntegrityError as _ex3:
        assert _ex3.__cause__.sqlstate == '23505'
        assert _ex3.__cause__.diag.constraint_name == 'bulkoutbox_scope_seq_unique'
    else:
        raise AssertionError('unique accepte')
    try:
        with transaction.atomic(using='default'):
            Model.objects.using('default').bulk_create([Model(**_valid_pub('evt-orphan-xyz', 'scope-orphan'))])
    except IntegrityError as _ex4:
        assert _ex4.__cause__.sqlstate == '23503'
    else:
        raise AssertionError('fk accepte')
    result['scope_seq_unique'] = True
    result['sql_constraints'] = True
    result['phase'] = 'REVERSE'
    _stable_before = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    MigrationExecutor(connection).migrate([('backend', '0010_bulk_export_manifest')])
    assert not h._table_exists(connection, state['schema'], _TARGET_TABLE)
    assert not h._table_exists(connection, state['schema'], _COUNTER_TABLE)
    assert h._applied_count(connection, state['schema'], '0011_bulk_outbox_publication') == 0
    assert h._applied_count(connection, state['schema'], '0010_bulk_export_manifest') == 1
    _stable_after = [h._table_identity(connection, state['schema'], t) for t in state['tables']]
    assert _stable_after == _stable_before == before and all(_stable_after)
    with connection.cursor() as _cur:
        _cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name LIKE %s ORDER BY table_name', [state['schema'], 'backend_%'])
        assert [r[0] for r in _cur.fetchall()] == sorted(state['tables'])
    result['reverse_only_0011'] = True
    result['existing_tables_stable'] = True
    result['phase'] = 'COMPLETE'

def run_real_bulk_outbox_initial_postgres(root_str):
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
                            result['public_tables_stable'] = state['public_before'] == [h._table_identity(admin, 'public', t) for t in (*state['tables'], _TARGET_TABLE, _COUNTER_TABLE, 'django_migrations')]
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
        spec = importlib.util.spec_from_file_location('outbox_pg_harness_under_test', target_path)
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
        assert callable(harness.run_real_bulk_outbox_initial_postgres)
        for bad_root in (None, '', 0, b'/home/devops/datas/pixs'):
            outcome = harness.run_real_bulk_outbox_initial_postgres(bad_root)
            assert outcome['real_pg'] is False
            assert outcome['phase'] == 'COMPLETE'
            assert outcome['reason'] == 'ROOT_INVALID'
        outcome = harness.run_real_bulk_outbox_initial_postgres('/synthetic/root')
        assert outcome['reason'] == 'ROOT_MISMATCH'
        assert outcome['real_pg'] is False
        assert settings.configured is False
        assert apps.ready is False
        assert [g.call_count for g in guards] == [0] * len(guards)
    print('BULK_OUTBOX_INITIAL_PG_HARNESS_SAFE_OK')
    ''').strip()
_MARKER = 'BULK_OUTBOX_INITIAL_PG_HARNESS_SAFE_OK' + chr(10)
class BulkOutboxInitialPostgresInertTests(unittest.TestCase):
    def test_harness_safe(self):
        result = subprocess.run([sys.executable, '-I', '-B', '-c', _CHILD, _SRC, _TARGET], cwd=str(_ROOT), env=_ENV, capture_output=True, text=True, timeout=60, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, _MARKER)
        self.assertEqual(result.stderr, '')
if __name__ == '__main__':
    unittest.main()
