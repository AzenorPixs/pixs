'''Integration tests for correlated log with real manifests.'''

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / 'src')
_CACHE = str(_ROOT / 'frontend' / '.cache')
_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONPATH': _SRC, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': _CACHE}

_REAL = textwrap.dedent('''
    import sys
    root = sys.argv[1]
    src = sys.argv[2]
    sys.path.insert(0, src)
    import builtins
    import io
    import json
    import os
    import socket
    import uuid
    from pathlib import Path
    from unittest import mock
    import psycopg
    import django
    from django.apps import apps
    from django.conf import LazySettings
    from django.conf import settings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper
    from contextlib import ExitStack
    pg_names = [(psycopg, 'connect'), (psycopg.Connection, 'connect'), (EngineWrapper, 'get_new_connection'), (socket.socket, 'connect'), (socket, 'create_connection'), (django, 'setup'), (LazySettings, 'configure')]
    pg_guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in pg_names]
    assert settings.configured is False and apps.ready is False
    with ExitStack() as outer:
        for pair, guard in zip(pg_names, pg_guards):
            outer.enter_context(mock.patch.object(pair[0], pair[1], guard))
        from pixs.backend.composition_initial import MANIFEST_PATHS
        from pixs.backend.composition_initial import REQUIRED_IDS
        from pixs.backend.composition_initial import OFFICIAL_IDS
        from pixs.kernel.composition import discover as real_discover
        from pixs.kernel.composition import validate as real_validate
        from pixs.kernel.composition import resolve as real_resolve
        base = Path(root)
        texts = tuple((base / rel).read_text(encoding='utf-8') for rel in MANIFEST_PATHS)
        assert len(texts) == 3
        fs_names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir')]
        fs_guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in fs_names]
        with ExitStack() as inner:
            for pair, guard in zip(fs_names, fs_guards):
                inner.enter_context(mock.patch.object(pair[0], pair[1], guard))
            import pixs.backend.correlated_log as target
            from pixs.backend.api.errors import build_infrastructure_error
            found = real_discover(texts)
            manifests, diags = real_validate(found, official_ids=OFFICIAL_IDS, required_ids=REQUIRED_IDS)
            assert diags == ()
            edges, order, rdiags = real_resolve(manifests)
            assert rdiags == ()
            assert set(order) == set(REQUIRED_IDS)
            corr = uuid.UUID(int=99)
            parent = '00-' + 'c' * 32 + '-' + 'd' * 16 + '-01'
            joint = io.StringIO()
            for comp in order:
                assert target.emit_correlated_log(traceparent=parent, correlation_id=corr, component_id=comp, sink=joint) is None
            value = joint.getvalue()
            lines = value.splitlines()
            assert len(lines) == 3
            for comp, line in zip(order, lines):
                item = json.loads(line)
                assert set(item) == {'component', 'correlation_id', 'event', 'parent_id', 'sampled', 'trace_id'}
                assert type(item['sampled']) is bool
                assert item['component'] == comp
                assert item['trace_id'] == 'c' * 32 and item['parent_id'] == 'd' * 16 and item['sampled'] is True
                assert item['correlation_id'] == build_infrastructure_error(corr, internal_error=None)['correlation_id']
                assert parent not in line
                assert line == json.dumps(item, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
                assert line.count(chr(10)) == 0
            assert value == chr(10).join(lines) + chr(10)
            joint2 = io.StringIO()
            for comp in order:
                target.emit_correlated_log(traceparent=parent, correlation_id=corr, component_id=comp, sink=joint2)
            assert joint2.getvalue() == value
            assert all(g.call_count == 0 for g in pg_guards)
            assert all(g.call_count == 0 for g in fs_guards)
            assert settings.configured is False and apps.ready is False
    print('REAL_OK')
''')


class TestReal(unittest.TestCase):
    def test_real(self):
        result = subprocess.run([sys.executable, '-B', '-c', _REAL, str(_ROOT), _SRC], timeout=30, capture_output=True, text=True, env=_ENV, cwd=str(_ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('REAL_OK', result.stdout)


if __name__ == '__main__':
    unittest.main()
