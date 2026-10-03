'''Integration guard tests for the health classifier in fresh subprocesses.'''

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / 'src')
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONPATH': _SRC, 'PYTHONDONTWRITEBYTECODE': '1'}


def _run(code: str):
    return subprocess.run([sys.executable, '-B', '-c', code, _SRC], timeout=30, capture_output=True, text=True, env=_ENV, cwd=str(_ROOT))


_GUARDED = textwrap.dedent('''
    import builtins
    import importlib.abc
    import os
    import socket
    import sys
    import types
    from contextlib import ExitStack
    from pathlib import Path
    from unittest import mock

    src = sys.argv[1]
    sys.path.insert(0, src)

    blocked = []

    class BlockSQLAndDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            base = name.split('.')[0]
            if base in ('django', 'sqlite3', 'mysql', 'MySQLdb', 'psycopg', 'psycopg2', 'psycopg_pool', 'pg8000', 'asyncpg', 'sqlalchemy'):
                blocked.append(name)
                raise ImportError('blocked')
            return None

    sys.meta_path.insert(0, BlockSQLAndDjango())

    fake_psycopg = types.ModuleType('psycopg')
    fake_connect = mock.Mock(side_effect=AssertionError('forbidden'))
    fake_psycopg.connect = fake_connect
    sys.modules['psycopg'] = fake_psycopg

    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in range(8)]
    names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir'), (socket.socket, 'connect'), (socket, 'create_connection')]

    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))

        probes = (
            lambda: builtins.open('dummy-path'),
            lambda: Path('dummy-path').open(),
            lambda: Path('dummy-path').read_text(),
            lambda: Path('dummy-path').read_bytes(),
            lambda: os.open('dummy-path', 0),
            lambda: os.scandir('dummy-path'),
            lambda: socket.socket.connect(object(), ('127.0.0.1', 0)),
            lambda: socket.create_connection(('127.0.0.1', 0)),
            lambda: fake_psycopg.connect('dummy-dsn'),
        )
        for probe in probes:
            try:
                probe()
            except AssertionError as exc:
                assert str(exc) == 'forbidden'
            else:
                raise AssertionError('guard not active')

        try:
            import django
        except ImportError:
            pass
        try:
            import sqlite3
        except ImportError:
            pass

        assert len(blocked) == 2, blocked
        assert blocked[0] == 'django' and blocked[1] == 'sqlite3', blocked
        assert fake_connect.call_count == 1, fake_connect.call_count
        for guard in guards:
            assert guard.call_count == 1, guard.call_count

        for guard in guards:
            guard.reset_mock()
        fake_connect.reset_mock()
        blocked.clear()

        import pixs.backend.health_classifier as target

        result = target.classify_health(alive=True, startup_complete=True, pg_available=True, required=(True,), optional=(True, False))
        assert result == {
            'liveness': True,
            'startup': True,
            'availability': True,
            'degraded': True,
            'pg_available': True,
            'required_count': 2,
            'required_ok_count': 2,
            'optional_count': 2,
            'optional_ok_count': 1,
        }, result
        again = target.classify_health(alive=True, startup_complete=True, pg_available=True, required=(True,), optional=(True, False))
        assert again == result and again is not result

        refused = 0
        for kwargs in (
            {'alive': 1, 'startup_complete': True, 'pg_available': True},
            {'alive': True, 'startup_complete': 1, 'pg_available': True},
            {'alive': True, 'startup_complete': True, 'pg_available': 1},
            {'alive': True, 'startup_complete': True, 'pg_available': True, 'required': [True]},
            {'alive': True, 'startup_complete': True, 'pg_available': True, 'optional': [True]},
        ):
            try:
                target.classify_health(**kwargs)
            except ValueError as exc:
                assert str(exc) == 'Invalid health snapshot'
                assert exc.__cause__ is None
                refused += 1
        assert refused == 5, refused

    assert blocked == [], blocked
    counts = [guard.call_count for guard in guards]
    counts.append(fake_connect.call_count)
    assert all(count == 0 for count in counts), counts
    print('GUARDS_OK')
''')


class TestGuardedImport(unittest.TestCase):
    def test_import_et_classification_sous_gardes(self) -> None:
        proc = _run(_GUARDED)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, 'GUARDS_OK\n')
        self.assertEqual(proc.stderr, '', proc.stderr)
