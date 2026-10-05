'''Integration PG tests, safe doubles plus explicit real callable.'''

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / 'src')
_CACHE = str(_ROOT / 'frontend' / '.cache')
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONPATH': _SRC, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': _CACHE}

_SAFE = textwrap.dedent('''
    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    import asyncio
    import builtins
    import os
    import socket
    from pathlib import Path
    from unittest import mock
    import django
    import psycopg
    from psycopg import AsyncConnection
    from django.apps import apps
    from django.conf import LazySettings
    from django.conf import settings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper
    from contextlib import ExitStack
    names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir'), (psycopg, 'connect'), (psycopg.Connection, 'connect'), (AsyncConnection, 'connect'), (EngineWrapper, 'get_new_connection'), (socket.socket, 'connect'), (socket, 'create_connection'), (django, 'setup'), (LazySettings, 'configure')]
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in names]
    assert settings.configured is False and apps.ready is False
    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))
        import pixs.backend.pg_connectivity as target
        calls = []
        class FakeCursor:
            async def execute(self, query):
                calls.append('execute')
            async def fetchone(self):
                return (1,)
            async def close(self):
                calls.append('cursor.close')
        class FakeConn:
            def cursor(self):
                return FakeCursor()
            async def close(self):
                calls.append('conn.close')
        async def fake_connect(**kwargs):
            return FakeConn()
        async def main():
            result = await target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname='it_db', user='it_user', password='it_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500, _connect=fake_connect)
            assert result is True
        asyncio.run(main())
        assert calls.count('execute') == 1 and calls.count('conn.close') == 1
        assert all(g.call_count == 0 for g in guards)
    print('SAFE_OK')
''')


def _parse_env_text(text):
    wanted = ('PG_DATABASE', 'PG_USERNAME', 'PG_PASSWORD')
    if type(text) is not str:
        raise ValueError('env invalid') from None
    if len(text) > 65536:
        raise ValueError('env invalid') from None
    if chr(0) in text:
        raise ValueError('env invalid') from None
    lines = text.splitlines()
    if len(lines) > 2000:
        raise ValueError('env invalid') from None
    found = {}
    for raw in lines:
        line = raw.strip()
        if line == '' or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[7:].strip()
        if '=' not in line:
            continue
        name, value = line.split('=', 1)
        name = name.strip()
        if name not in wanted:
            continue
        if name in found:
            raise ValueError('env invalid') from None
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in (chr(39), chr(34)):
            inner = value[1:-1]
            if value[0] in inner:
                raise ValueError('env invalid') from None
            value = inner
        elif len(value) >= 1 and value[0] in (chr(39), chr(34)):
            raise ValueError('env invalid') from None
        elif len(value) >= 1 and value[-1] in (chr(39), chr(34)):
            raise ValueError('env invalid') from None
        if value == '':
            raise ValueError('env invalid') from None
        if chr(0) in value:
            raise ValueError('env invalid') from None
        found[name] = value
    for name in wanted:
        if name not in found:
            raise ValueError('env invalid') from None
    return found


_SQLSTATE_REASONS = {
    '28000': 'AUTH_REFUSED',
    '28P01': 'AUTH_REFUSED',
    '08000': 'CLIENT_OR_NETWORK',
    '08001': 'CLIENT_OR_NETWORK',
    '08003': 'CLIENT_OR_NETWORK',
    '08004': 'CLIENT_OR_NETWORK',
    '08006': 'CLIENT_OR_NETWORK',
    '3D000': 'DB_UNAVAILABLE',
    '53300': 'DB_UNAVAILABLE',
    '57P03': 'DB_UNAVAILABLE',
}


def _classify_driver_error(error):
    '''Fixed closed classification of known driver error classes.'''
    state = getattr(error, 'sqlstate', None)
    if type(state) is str and state in _SQLSTATE_REASONS:
        return _SQLSTATE_REASONS[state]
    try:
        import psycopg
    except Exception:
        psycopg = None
    if psycopg is not None and isinstance(error, (psycopg.OperationalError, psycopg.InterfaceError)):
        return 'CLIENT_OR_NETWORK'
    if isinstance(error, (OSError, TimeoutError)):
        return 'CLIENT_OR_NETWORK'
    return 'DRIVER_FAILED'


def run_real_probe(root_str):
    '''Real PG callable invoked only by a dedicated CAB command.'''
    import asyncio
    import io
    import logging
    import sys
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock

    outcome = {'ok': False, 'select_one': False, 'connection_closed': False, 'cursor_closed': False, 'phase': 'init', 'reason': 'NONE'}
    previous_disable = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    original_out = sys.stdout
    original_err = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    def _fail_state(phase, reason):
        outcome['phase'] = phase
        outcome['reason'] = reason
        return outcome

    try:
        outcome['phase'] = 'read_env'
        try:
            with Path(root_str).joinpath('project.env').open('rb') as handle:
                raw = handle.read(65537)
        except BaseException:
            return _fail_state('read_env', 'INPUT_REFUSED')
        if len(raw) > 65536:
            return _fail_state('read_env', 'INPUT_REFUSED')
        try:
            text = raw.decode('utf-8')
        except BaseException:
            return _fail_state('read_env', 'INPUT_REFUSED')
        outcome['phase'] = 'parse_env'
        try:
            found = _parse_env_text(text)
        except BaseException:
            return _fail_state('parse_env', 'INPUT_REFUSED')
        for name in ('PG_DATABASE', 'PG_USERNAME', 'PG_PASSWORD'):
            item = found.get(name)
            if type(item) is not str or item == '':
                return _fail_state('parse_env', 'INPUT_REFUSED')

        observed = {'phase': 'DRIVER_IMPORT', 'reason': 'DRIVER_FAILED', 'conn_closed': False, 'cur_closed': False}

        async def _attempt(book):
            import pixs.backend.pg_connectivity as target
            from psycopg import AsyncConnection
            from psycopg import AsyncCursor

            real_connect = AsyncConnection.connect
            real_cursor = AsyncConnection.cursor
            real_execute = AsyncCursor.execute
            real_cursor_close = AsyncCursor.close
            real_conn_close = AsyncConnection.close

            conns = []
            cursors = []
            counts = {'connect': 0, 'cursor': 0, 'execute': 0, 'cursor.close': 0, 'conn.close': 0}
            checks = {'host': False, 'limits': False, 'autocommit': False, 'options': False, 'form': False}
            snapshots = {'result': None, 'conn_closed': False, 'cur_closed': False, 'conn_autocommit': False}

            book['phase'] = 'INPUT_VALIDATION'
            for name in ('PG_DATABASE', 'PG_USERNAME', 'PG_PASSWORD'):
                item = found.get(name)
                if type(item) is not str or item == '':
                    book['reason'] = 'INPUT_REFUSED'
                    raise RuntimeError('probe input invalid') from None

            async def spy_connect(**kwargs):
                counts['connect'] += 1
                if kwargs.get('host') == '127.0.0.1' and kwargs.get('hostaddr') == kwargs.get('host'):
                    checks['host'] = True
                if kwargs.get('port') == 5432 and kwargs.get('connect_timeout') == 2:
                    checks['limits'] = True
                if kwargs.get('autocommit') is True:
                    checks['autocommit'] = True
                if kwargs.get('options') == '-c default_transaction_read_only=on -c statement_timeout=1500':
                    checks['options'] = True
                if all(type(kwargs.get(key)) is str and kwargs.get(key) != '' for key in ('dbname', 'user', 'password')):
                    checks['form'] = True
                if counts['connect'] != 1 or not all(checks.values()):
                    raise RuntimeError('probe protocol violation') from None
                book['phase'] = 'DRIVER_CONNECT'
                book['reason'] = 'DRIVER_FAILED'
                try:
                    connection = await real_connect(**kwargs)
                except BaseException as error:
                    book['reason'] = _classify_driver_error(error)
                    raise
                book['phase'] = 'DRIVER_CONNECTED'
                book['reason'] = 'PROBE_FAILED'
                conns.append(connection)
                snapshots['conn_autocommit'] = connection.autocommit is True
                return connection

            def spy_cursor(connection):
                counts['cursor'] += 1
                book['phase'] = 'CURSOR'
                produced = real_cursor(connection)
                cursors.append(produced)
                return produced

            async def spy_execute(cursor, query):
                counts['execute'] += 1
                if counts['execute'] > 1 or query != 'SELECT 1':
                    raise RuntimeError('probe protocol violation')
                book['phase'] = 'QUERY'
                return await real_execute(cursor, query)

            async def spy_cursor_close(cursor):
                counts['cursor.close'] += 1
                book['phase'] = 'CURSOR_CLOSE'
                return await real_cursor_close(cursor)

            async def spy_conn_close(connection):
                counts['conn.close'] += 1
                book['phase'] = 'CONNECTION_CLOSE'
                return await real_conn_close(connection)

            cleanup_failed = False
            with ExitStack() as stack:
                stack.enter_context(mock.patch.object(AsyncConnection, 'connect', spy_connect))
                stack.enter_context(mock.patch.object(AsyncConnection, 'cursor', spy_cursor))
                stack.enter_context(mock.patch.object(AsyncCursor, 'execute', spy_execute))
                stack.enter_context(mock.patch.object(AsyncCursor, 'close', spy_cursor_close))
                stack.enter_context(mock.patch.object(AsyncConnection, 'close', spy_conn_close))
                book['reason'] = 'INPUT_REFUSED'
                try:
                    result = await target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname=found['PG_DATABASE'], user=found['PG_USERNAME'], password=found['PG_PASSWORD'], port=5432, connect_timeout_s=2, query_timeout_s=2, statement_timeout_ms=1500)
                    snapshots['result'] = result
                finally:
                    if conns and conns[-1].closed is True:
                        snapshots['conn_closed'] = True
                        book['conn_closed'] = True
                    if cursors and cursors[-1].closed is True:
                        snapshots['cur_closed'] = True
                        book['cur_closed'] = True
                    for connection in conns:
                        if connection.closed is not True:
                            try:
                                await real_conn_close(connection)
                            except BaseException:
                                cleanup_failed = True
                    for cursor in cursors:
                        if cursor.closed is not True:
                            try:
                                await real_cursor_close(cursor)
                            except BaseException:
                                cleanup_failed = True

            if cleanup_failed:
                book['reason'] = 'CLEANUP_FAILED'
                raise RuntimeError('probe cleanup invalid') from None
            helper_ok = snapshots['result'] is True
            protocol_ok = counts['connect'] == 1 and counts['cursor'] == 1 and counts['execute'] == 1 and counts['cursor.close'] == 1 and counts['conn.close'] == 1
            checks_ok = all(checks.values()) and snapshots['conn_autocommit']
            book['phase'] = 'COMPLETE'
            book['reason'] = 'NONE'
            return {
                'ok': bool(helper_ok and snapshots['conn_closed'] and snapshots['cur_closed'] and protocol_ok and checks_ok),
                'select_one': bool(helper_ok and counts['execute'] == 1),
                'connection_closed': snapshots['conn_closed'],
                'cursor_closed': snapshots['cur_closed'],
                'phase': 'COMPLETE',
                'reason': 'NONE',
            }

        try:
            partial = asyncio.run(_attempt(observed))
        except BaseException:
            outcome['ok'] = False
            outcome['select_one'] = False
            outcome['phase'] = observed['phase']
            outcome['reason'] = observed['reason']
            if observed['conn_closed'] is True:
                outcome['connection_closed'] = True
            if observed['cur_closed'] is True:
                outcome['cursor_closed'] = True
            return outcome
        outcome.update(partial)
        return outcome
    except BaseException:
        outcome['ok'] = False
        outcome['select_one'] = False
        if outcome['reason'] == 'NONE':
            outcome['reason'] = 'INPUT_REFUSED' if outcome['phase'] in ('read_env', 'parse_env') else 'DRIVER_FAILED'
        return outcome
    finally:
        logging.disable(previous_disable)
        sys.stdout = original_out
        sys.stderr = original_err


class TestSafe(unittest.TestCase):
    def test_safe(self):
        result = subprocess.run([sys.executable, '-B', '-c', _SAFE, _SRC], timeout=30, capture_output=True, text=True, env=_ENV, cwd=str(_ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SAFE_OK', result.stdout)


class TestParser(unittest.TestCase):
    def test_parser_accepts(self):
        found = _parse_env_text('\n# commentaire\nexport PG_DATABASE=probe_db\nexport PG_USERNAME=probe_user\nPG_PASSWORD=probe_secret\n')
        self.assertEqual(found, {'PG_DATABASE': 'probe_db', 'PG_USERNAME': 'probe_user', 'PG_PASSWORD': 'probe_secret'})
        found = _parse_env_text("PG_PASSWORD='my=secret'\nPG_DATABASE=probe_db\nPG_USERNAME=probe_user\n")
        self.assertEqual(found['PG_PASSWORD'], 'my=secret')
        found = _parse_env_text('PG_PASSWORD="$Literal$"\nPG_DATABASE=probe_db\nPG_USERNAME=probe_user\n')
        self.assertEqual(found['PG_PASSWORD'], '$Literal$')

    def test_parser_refuses(self):
        cases = [
            '',
            'PG_DATABASE=d\nPG_USERNAME=u\nPG_PASSWORD=bad' + chr(39) + '\n',
            None,
            b'PG_DATABASE=a\n',
            'x' * 65537,
            'PG_DATABASE=a\n' * 2001,
            'PG_DATABASE=d' + chr(0) + 'b\nPG_USERNAME=u\nPG_PASSWORD=p\n',
            'PG_DATABASE=a\nPG_DATABASE=b\nPG_USERNAME=u\nPG_PASSWORD=p\n',
            'PG_USERNAME=u\nPG_PASSWORD=p\n',
            'PG_DATABASE=\nPG_USERNAME=u\nPG_PASSWORD=p\n',
            'PG_PASSWORD=my' + chr(0) + 'pass\nPG_DATABASE=d\nPG_USERNAME=u\n',
            "PG_PASSWORD='unbalanced\nPG_DATABASE=d\nPG_USERNAME=u\n",
            "PG_PASSWORD='a''\nPG_DATABASE=d\nPG_USERNAME=u\n",
            "PG_PASSWORD=\"\nPG_DATABASE=d\nPG_USERNAME=u\n",
            "PG_PASSWORD='a'x\nPG_DATABASE=d\nPG_USERNAME=u\n",
        ]
        for text in cases:
            with self.assertRaises(ValueError) as caught:
                _parse_env_text(text)
            self.assertIsNone(caught.exception.__cause__)
            self.assertEqual(str(caught.exception), 'env invalid')


class TestRealRefusal(unittest.TestCase):
    def test_real_probe_driver_refusal(self):
        import io
        import logging
        import sys
        from unittest import mock
        from psycopg import AsyncConnection

        env_text = 'PG_DATABASE=synthetic_db\nPG_USERNAME=synthetic_user\nPG_PASSWORD=synthetic_secret\n'
        source = io.BytesIO(env_text.encode('utf-8'))
        driver_calls = []

        def fake_open(path, mode='r', *args, **kwargs):
            driver_calls.append(('open', mode))
            return source

        async def fake_connect(**kwargs):
            driver_calls.append(('connect',))
            print('canary-driver-refusal')
            sys.stderr.write('canary-driver-refusal')
            raise RuntimeError('canary-driver-refusal')

        previous_disable = logging.root.manager.disable
        original_out = sys.stdout
        original_err = sys.stderr
        from contextlib import redirect_stdout, redirect_stderr
        capture_out, capture_err = io.StringIO(), io.StringIO()
        with redirect_stdout(capture_out), redirect_stderr(capture_err):
            with mock.patch.object(Path, 'open', fake_open), mock.patch.object(AsyncConnection, 'connect', fake_connect):
                outcome = run_real_probe('/synthetic/root')
        self.assertEqual(capture_out.getvalue(), '')
        self.assertEqual(capture_err.getvalue(), '')
        self.assertIs(sys.stdout, original_out)
        self.assertIs(sys.stderr, original_err)
        self.assertEqual(logging.root.manager.disable, previous_disable)
        self.assertEqual(driver_calls, [('open', 'rb'), ('connect',)])
        self.assertEqual(outcome, {'ok': False, 'select_one': False, 'connection_closed': False, 'cursor_closed': False, 'phase': 'DRIVER_CONNECT', 'reason': 'DRIVER_FAILED'})

    def test_helper_input_refusal(self):
        import io
        import logging
        from unittest import mock
        from psycopg import AsyncConnection
        env_text = 'PG_DATABASE=postgresql://invalid\nPG_USERNAME=synthetic_user\nPG_PASSWORD=synthetic_secret\n'
        source = io.BytesIO(env_text.encode('utf-8'))
        guard = mock.Mock(side_effect=AssertionError('forbidden'))
        previous_disable = logging.root.manager.disable
        original_out, original_err = sys.stdout, sys.stderr
        with mock.patch.object(Path, 'open', return_value=source), mock.patch.object(AsyncConnection, 'connect', guard):
            outcome = run_real_probe('/synthetic/root')
        self.assertIs(sys.stdout, original_out)
        self.assertIs(sys.stderr, original_err)
        self.assertEqual(logging.root.manager.disable, previous_disable)
        self.assertEqual(guard.call_count, 0)
        self.assertEqual(outcome, {'ok': False, 'select_one': False, 'connection_closed': False, 'cursor_closed': False, 'phase': 'INPUT_VALIDATION', 'reason': 'INPUT_REFUSED'})


if __name__ == '__main__':
    unittest.main()
