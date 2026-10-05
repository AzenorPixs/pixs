'''Unit tests for bounded async PG probe with cooperative doubles.'''

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / 'src')
_CACHE = str(_ROOT / 'frontend' / '.cache')
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONPATH': _SRC, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': _CACHE}


def _run(code, arg):
    return subprocess.run([sys.executable, '-B', '-c', code, arg], timeout=30, capture_output=True, text=True, env=_ENV, cwd=str(_ROOT))


_PURE = textwrap.dedent('''
    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    import builtins
    import importlib.abc
    import os
    import socket
    from pathlib import Path
    from unittest import mock
    blocked = []
    class BlockDeps(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == 'psycopg' or name.startswith('psycopg.') or name == 'django' or name.startswith('django.'):
                blocked.append(name)
                raise ImportError('blocked')
            return None
    sys.meta_path.insert(0, BlockDeps())
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in range(8)]
    names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir'), (socket.socket, 'connect'), (socket, 'create_connection')]
    from contextlib import ExitStack
    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))
        import pixs.backend.pg_connectivity as target
        assert 'psycopg' not in sys.modules
        assert 'django' not in sys.modules
        assert blocked == []
        assert all(g.call_count == 0 for g in guards)
    print('PURE_OK')
''')

_VALID = textwrap.dedent('''
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
            def __init__(self):
                self.closed = 0
            async def execute(self, query):
                calls.append('execute')
                assert query == 'SELECT 1'
            async def fetchone(self):
                calls.append('fetchone')
                return (1,)
            async def close(self):
                calls.append('cursor.close')
                self.closed += 1
        class FakeConn:
            def __init__(self):
                self.closed = 0
            def cursor(self):
                calls.append('cursor')
                return FakeCursor()
            async def close(self):
                calls.append('conn.close')
                self.closed += 1
        async def fake_connect(**kwargs):
            calls.append('connect')
            assert kwargs['host'] == '127.0.0.1' and kwargs['hostaddr'] == '127.0.0.1'
            assert kwargs['autocommit'] is True
            assert kwargs['options'] == '-c default_transaction_read_only=on -c statement_timeout=1500'
            return FakeConn()
        async def main():
            first = await target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500, _connect=fake_connect)
            assert first is True
            second = await target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500, _connect=fake_connect)
            assert second is True
        asyncio.run(main())
        assert calls.count('connect') == 2
        assert calls.count('execute') == 2
        assert calls.count('conn.close') == 2
        assert calls.count('cursor.close') == 2
        assert all(g.call_count == 0 for g in guards)
        assert settings.configured is False and apps.ready is False
    print('VALID_OK')
''')

_NEGATIVE = textwrap.dedent('''
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
        marker = 'OPAQUE_MARKER_PG_002'
        trap_calls = []
        class EvilStr(str):
            def __hash__(self):
                trap_calls.append('hash')
                raise AssertionError('trap')
            def __eq__(self, other):
                trap_calls.append('eq')
                raise AssertionError('trap')
            def __len__(self):
                trap_calls.append('len')
                raise AssertionError('trap')
            def encode(self, *args, **kwargs):
                trap_calls.append('encode')
                raise AssertionError('trap')
        class EvilInt(int):
            def _trap(self, other):
                trap_calls.append('int-compare')
                raise AssertionError('trap')
            __lt__ = __le__ = __gt__ = __ge__ = __eq__ = _trap
        touched = []
        async def never_connect(**kwargs):
            touched.append('connect')
            raise AssertionError('must not connect')
        good = dict(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500)
        async def refuse(**kwargs):
            try:
                await target.probe_pg_connectivity(_connect=never_connect, **kwargs)
            except target.PgProbeError as error:
                assert str(error) == 'pg connectivity invalid'
                assert error.__cause__ is None
                assert error.__suppress_context__ is True
                assert marker not in str(error)
            else:
                raise AssertionError('refusal expected')
        async def main():
            await refuse(**dict(good, hostaddr=EvilStr('127.0.0.1')))
            await refuse(**dict(good, dbname='bad' + chr(0) + marker))
            await refuse(**dict(good, dbname='a=b'))
            await refuse(**dict(good, dbname='a://b'))
            await refuse(**dict(good, port=EvilInt(5432)))
            await refuse(**dict(good, port=True))
            await refuse(**dict(good, connect_timeout_s=1))
            await refuse(**dict(good, connect_timeout_s=2147483648))
            await refuse(**dict(good, query_timeout_s=10**400))
            await refuse(**dict(good, query_timeout_s=float('nan')))
            await refuse(**dict(good, query_timeout_s=chr(0xD800)))
            await refuse(**dict(good, hostaddr='db.example.com'))
            await refuse(**dict(good, hostaddr='127,0,0,1'))
            await refuse(**dict(good, hostaddr='fe80::1%eth0'))
            assert touched == []
            assert trap_calls == []
            order = []
            started = asyncio.Event()
            class HangingCursor:
                async def execute(self, query):
                    order.append('execute')
                    started.set()
                    try:
                        await asyncio.Event().wait()
                    except asyncio.CancelledError:
                        order.append('query.cancel')
                        raise
                async def fetchone(self):
                    order.append('fetchone')
                    return (1,)
                async def close(self):
                    order.append('cursor.close')
            class HangingConn:
                async def close(self):
                    order.append('conn.close')
            async def hanging_connect(**kwargs):
                conn = HangingConn()
                conn.cursor = lambda: HangingCursor()
                return conn
            try:
                await target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=1, statement_timeout_ms=1500, _connect=hanging_connect)
            except target.PgProbeError as error:
                assert error.__cause__ is None
            else:
                raise AssertionError('timeout expected')
            assert order[0] == 'execute'
            assert order.count('execute') == 1
            assert order.count('conn.close') == 1
            assert order.index('conn.close') < order.index('query.cancel')
            assert 'cursor.close' in order
            assert len([t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]) == 0
            for mode in ('connect', 'cursor', 'execute', 'fetch', 'row', 'curclose', 'connclose'):
                events = []
                class FailCursor:
                    async def execute(self, query):
                        events.append('execute')
                        if mode == 'execute':
                            raise RuntimeError(marker)
                    async def fetchone(self):
                        events.append('fetchone')
                        if mode == 'fetch':
                            raise RuntimeError(marker)
                        if mode == 'row':
                            return (True,)
                        return (1,)
                    async def close(self):
                        events.append('cursor.close')
                        if mode == 'curclose':
                            raise RuntimeError(marker)
                class FailConn:
                    def cursor(self):
                        events.append('cursor')
                        if mode == 'cursor':
                            raise RuntimeError(marker)
                        return FailCursor()
                    async def close(self):
                        events.append('conn.close')
                        if mode == 'connclose':
                            raise RuntimeError(marker)
                async def fail_connect(**kwargs):
                    events.append('connect')
                    if mode == 'connect':
                        raise RuntimeError(marker)
                    return FailConn()
                try:
                    await target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500, _connect=fail_connect)
                except target.PgProbeError as error:
                    assert error.__cause__ is None
                    assert marker not in str(error)
                else:
                    raise AssertionError(mode)
                assert events.count('execute') <= 1
                if mode == 'connect':
                    assert events.count('conn.close') == 0
                else:
                    assert events.count('conn.close') == 1
                if mode in ('connect', 'cursor'):
                    assert events.count('cursor.close') == 0
                else:
                    assert events.count('cursor.close') == 1
            probe_events = []
            started2 = asyncio.Event()
            class CancelCursor:
                async def execute(self, query):
                    probe_events.append('execute')
                    started2.set()
                    try:
                        await asyncio.Event().wait()
                    except asyncio.CancelledError:
                        probe_events.append('query.cancel')
                        raise
                async def fetchone(self):
                    return (1,)
                async def close(self):
                    probe_events.append('cursor.close')
            class CancelConn:
                async def close(self):
                    probe_events.append('conn.close')
            async def cancel_connect(**kwargs):
                conn = CancelConn()
                conn.cursor = lambda: CancelCursor()
                return conn
            probe_task = asyncio.ensure_future(target.probe_pg_connectivity(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500, _connect=cancel_connect))
            await started2.wait()
            assert not probe_task.done()
            probe_task.cancel()
            try:
                await probe_task
            except asyncio.CancelledError:
                cancelled = True
            else:
                raise AssertionError('cancel expected')
            assert cancelled is True
            assert 'conn.close' in probe_events
            assert probe_events.index('conn.close') < probe_events.index('query.cancel')
            assert len([t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]) == 0
            assert all(g.call_count == 0 for g in guards)
            assert settings.configured is False and apps.ready is False
            assert trap_calls == []
        asyncio.run(main())
        print('NEGATIVE_OK')
''')


class TestPure(unittest.TestCase):
    def test_pure(self):
        result = _run(_PURE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PURE_OK', result.stdout)


class TestValid(unittest.TestCase):
    def test_valid(self):
        result = _run(_VALID, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('VALID_OK', result.stdout)


class TestNegative(unittest.TestCase):
    def test_negative(self):
        result = _run(_NEGATIVE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('NEGATIVE_OK', result.stdout)


_CLOSEFAIL = textwrap.dedent('''
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
        marker = 'OPAQUE_MARKER_PG_003'
        base = dict(hostaddr='127.0.0.1', dbname='probe_db', user='probe_user', password='probe_secret', port=5432, connect_timeout_s=2, query_timeout_s=5, statement_timeout_ms=1500)
        async def main():
            order = []
            started = asyncio.Event()
            class HangCursor:
                def __init__(self, fail):
                    self.fail = fail
                async def execute(self, query):
                    order.append('execute')
                    started.set()
                    try:
                        await asyncio.Event().wait()
                    except asyncio.CancelledError:
                        order.append('query.cancel')
                        raise
                async def fetchone(self):
                    return (1,)
                async def close(self):
                    order.append('cursor.close')
            class HangConn:
                def __init__(self, fail):
                    self.fail = fail
                async def close(self):
                    order.append('conn.close')
                    if self.fail:
                        raise RuntimeError(marker)
            async def hanging(fail, **kwargs):
                conn = HangConn(fail)
                conn.cursor = lambda: HangCursor(fail)
                return conn
            async def hanging_ok(**kwargs):
                return await hanging(False)
            async def hanging_fail(**kwargs):
                return await hanging(True)
            try:
                await target.probe_pg_connectivity(_connect=hanging_fail, **dict(base, query_timeout_s=1))
            except target.PgProbeError as error:
                assert str(error) == 'pg connectivity invalid'
                assert error.__cause__ is None
                assert marker not in str(error)
            else:
                raise AssertionError('timeout closefail expected')
            assert order.count('execute') == 1
            assert order.count('conn.close') == 1
            assert order.index('conn.close') < order.index('query.cancel')
            assert 'cursor.close' in order
            assert len([t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]) == 0
            order2 = []
            started2 = asyncio.Event()
            class HangCursor2:
                async def execute(self, query):
                    order2.append('execute')
                    started2.set()
                    try:
                        await asyncio.Event().wait()
                    except asyncio.CancelledError:
                        order2.append('query.cancel')
                        raise
                async def fetchone(self):
                    return (1,)
                async def close(self):
                    order2.append('cursor.close')
            class HangConn2:
                async def close(self):
                    order2.append('conn.close')
                    raise RuntimeError(marker)
            async def hanging2(**kwargs):
                conn = HangConn2()
                conn.cursor = lambda: HangCursor2()
                return conn
            probe_task = asyncio.ensure_future(target.probe_pg_connectivity(_connect=hanging2, **base))
            await started2.wait()
            assert not probe_task.done()
            probe_task.cancel()
            try:
                await probe_task
            except target.PgProbeError as error:
                assert error.__cause__ is None
                assert marker not in str(error)
            except asyncio.CancelledError:
                raise AssertionError('expected generic on close failure')
            else:
                raise AssertionError('cancel closefail expected')
            assert order2.index('conn.close') < order2.index('query.cancel')
            assert order2.count('conn.close') == 1
            assert len([t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]) == 0
            order3 = []
            close_started = asyncio.Event()
            class RaceCursor:
                async def execute(self, query):
                    order3.append('execute')
                async def fetchone(self):
                    order3.append('fetchone')
                    return (1,)
                async def close(self):
                    order3.append('cursor.close')
            class RaceConn:
                async def close(self):
                    order3.append('conn.close')
                    close_started.set()
                    await asyncio.sleep(0)
            async def race_connect(**kwargs):
                conn = RaceConn()
                conn.cursor = lambda: RaceCursor()
                return conn
            probe_task = asyncio.ensure_future(target.probe_pg_connectivity(_connect=race_connect, **base))
            await close_started.wait()
            probe_task.cancel()
            try:
                await probe_task
            except target.PgProbeError as error:
                assert error.__cause__ is None
            except asyncio.CancelledError:
                raise AssertionError('expected generic on interrupted close')
            else:
                raise AssertionError('race generic expected')
            assert len([t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]) == 0
            touched = []
            async def never_connect(**kwargs):
                touched.append('connect')
                raise AssertionError('must not connect')
            async def refuse(**kwargs):
                try:
                    await target.probe_pg_connectivity(_connect=never_connect, **kwargs)
                except target.PgProbeError as error:
                    assert error.__cause__ is None
                else:
                    raise AssertionError('refusal expected')
            await refuse(**dict(base, password=chr(0xD800)))
            await refuse(**dict(base, password=''))
            await refuse(**dict(base, statement_timeout_ms=True))
            await refuse(**dict(base, statement_timeout_ms=0))
            await refuse(**dict(base, statement_timeout_ms=2147483648))
            await refuse(**dict(base, query_timeout_s=float('inf')))
            assert touched == []
            for bad_row in (True, [1], (1, 2), 'x', None):
                events = []
                class RowCursor:
                    async def execute(self, query):
                        events.append('execute')
                    async def fetchone(self):
                        events.append('fetchone')
                        return bad_row
                    async def close(self):
                        events.append('cursor.close')
                class RowConn:
                    def cursor(self):
                        return RowCursor()
                    async def close(self):
                        events.append('conn.close')
                async def row_connect(**kwargs):
                    return RowConn()
                try:
                    await target.probe_pg_connectivity(_connect=row_connect, **base)
                except target.PgProbeError as error:
                    assert error.__cause__ is None
                else:
                    raise AssertionError('row refusal expected')
                assert events.count('execute') == 1
                assert events.count('conn.close') == 1
            assert all(g.call_count == 0 for g in guards)
            assert settings.configured is False and apps.ready is False
        asyncio.run(main())
        print('CLOSEFAIL_OK')
''')


class TestCloseFailure(unittest.TestCase):
    def test_close_failure(self):
        result = _run(_CLOSEFAIL, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('CLOSEFAIL_OK', result.stdout)


if __name__ == '__main__':
    unittest.main()
