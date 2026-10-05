'''Unit tests for bounded correlated log in fresh subprocesses.'''

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
    import psycopg
    blocked = []
    class BlockDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == 'django' or name.startswith('django.'):
                blocked.append(name)
                raise ImportError('blocked')
            return None
    sys.meta_path.insert(0, BlockDjango())
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in range(10)]
    names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir'), (psycopg, 'connect'), (psycopg.Connection, 'connect'), (socket.socket, 'connect'), (socket, 'create_connection')]
    from contextlib import ExitStack
    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))
        import pixs.backend.correlated_log as target
        assert 'django' not in sys.modules
        assert blocked == []
        assert all(g.call_count == 0 for g in guards)
    print('PURE_OK')
''')

_VALID = textwrap.dedent('''
    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    import builtins
    import io
    import json
    import os
    import socket
    import uuid
    from pathlib import Path
    from unittest import mock
    import django
    import psycopg
    from django.apps import apps
    from django.conf import LazySettings
    from django.conf import settings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper
    from contextlib import ExitStack
    names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir'), (psycopg, 'connect'), (psycopg.Connection, 'connect'), (EngineWrapper, 'get_new_connection'), (socket.socket, 'connect'), (socket, 'create_connection'), (django, 'setup'), (LazySettings, 'configure')]
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in names]
    assert settings.configured is False and apps.ready is False
    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))
        import pixs.backend.correlated_log as target
        from pixs.backend.api.errors import build_infrastructure_error
        corr = uuid.UUID(int=42)
        good = '00-' + '1' * 32 + '-' + '2' * 16 + '-09'
        sink = io.StringIO()
        assert target.emit_correlated_log(traceparent=good, correlation_id=corr, component_id='pixs.kernel', sink=sink) is None
        first = sink.getvalue()
        proof = json.loads(first)
        assert set(proof) == {'component', 'correlation_id', 'event', 'parent_id', 'sampled', 'trace_id'}
        assert type(proof['sampled']) is bool
        assert type(proof['component']) is str and type(proof['correlation_id']) is str
        assert type(proof['event']) is str and type(proof['parent_id']) is str and type(proof['trace_id']) is str
        assert first == json.dumps(proof, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + chr(10)
        assert good not in first
        assert 'timestamp' not in first and 'message' not in first and 'version' not in first
        assert proof['event'] == 'component.context'
        assert proof['sampled'] is True
        assert proof['correlation_id'] == build_infrastructure_error(corr, internal_error=None)['correlation_id']
        sink2 = io.StringIO()
        assert target.emit_correlated_log(traceparent=good, correlation_id=corr, component_id='pixs.kernel', sink=sink2) is None
        assert sink2.getvalue() == first
        for flag in range(256):
            text = '00-' + 'a' * 32 + '-' + 'b' * 16 + '-' + format(flag, '02x')
            fresh = io.StringIO()
            target.emit_correlated_log(traceparent=text, correlation_id=corr, component_id='pixs.core', sink=fresh)
            parsed = target.parse_traceparent(text)
            assert type(parsed) is target.TraceContext
            assert parsed.trace_id == 'a' * 32 and parsed.parent_id == 'b' * 16
            assert parsed.sampled is ((flag & 1) == 1)
            assert json.loads(fresh.getvalue())['sampled'] is parsed.sampled
        for version in range(16):
            for variant in range(4):
                cand = uuid.UUID(int=(version << 76) | (variant << 62) | 7)
                fresh = io.StringIO()
                target.emit_correlated_log(traceparent=good, correlation_id=cand, component_id='example.hello', sink=fresh)
                assert json.loads(fresh.getvalue())['correlation_id'] == build_infrastructure_error(cand, internal_error=None)['correlation_id']
        for cand in (uuid.UUID(int=0), uuid.UUID(int=2**128 - 1)):
            fresh = io.StringIO()
            target.emit_correlated_log(traceparent=good, correlation_id=cand, component_id='example.hello', sink=fresh)
            assert json.loads(fresh.getvalue())['correlation_id'] == build_infrastructure_error(cand, internal_error=None)['correlation_id']
        assert all(g.call_count == 0 for g in guards)
        assert settings.configured is False and apps.ready is False
    print('VALID_OK')
''')

_NEGATIVE = textwrap.dedent('''
    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    import builtins
    import io
    import os
    import socket
    import uuid
    from pathlib import Path
    from unittest import mock
    import django
    import psycopg
    from django.apps import apps
    from django.conf import LazySettings
    from django.conf import settings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper
    from contextlib import ExitStack
    names = [(builtins, 'open'), (Path, 'open'), (Path, 'read_text'), (Path, 'read_bytes'), (os, 'open'), (os, 'scandir'), (psycopg, 'connect'), (psycopg.Connection, 'connect'), (EngineWrapper, 'get_new_connection'), (socket.socket, 'connect'), (socket, 'create_connection'), (django, 'setup'), (LazySettings, 'configure')]
    guards = [mock.Mock(side_effect=AssertionError('forbidden')) for _ in names]
    assert settings.configured is False and apps.ready is False
    with ExitStack() as stack:
        for pair, guard in zip(names, guards):
            stack.enter_context(mock.patch.object(pair[0], pair[1], guard))
        import pixs.backend.correlated_log as target
        good = '00-' + '1' * 32 + '-' + '2' * 16 + '-01'
        corr = uuid.UUID(int=7)
        marker = 'OPAQUE_MARKER_XYZ_011'
        bad_traces = ['00-' + '1' * 32 + '-' + '2' * 16 + '-0G', '01-' + '1' * 32 + '-' + '2' * 16 + '-01', '00-' + '1' * 31 + '-' + '2' * 16 + '-01', '00-' + 'A' * 32 + '-' + '2' * 16 + '-01', '00-' + '0' * 32 + '-' + '2' * 16 + '-01', 'x' * 70, chr(0xD800)]
        bad_traces.extend([good + '-suffix', 'ff' + good[2:], good[:-1], '00-' + '1' * 32 + '-' + '0' * 16 + '-01', marker, 'x' * 100000, None, b'raw', True, ['raw']])
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
        class EvilUUID(uuid.UUID):
            def __getattribute__(self, name):
                trap_calls.append('uget')
                raise AssertionError('trap')
            def __str__(self):
                trap_calls.append('ustr')
                raise AssertionError('trap')
        class EvilInt(int):
            def _trap(self, other):
                trap_calls.append('int-compare')
                raise AssertionError('trap')
            __lt__ = __le__ = __gt__ = __ge__ = __eq__ = _trap
        evil_trace = EvilStr(good)
        evil_comp = EvilStr('pixs.kernel')
        evil_uuid = object.__new__(EvilUUID)
        object.__setattr__(evil_uuid, 'int', 7)
        forged_none = object.__new__(uuid.UUID)
        def forged_int(value):
            item = object.__new__(uuid.UUID)
            object.__setattr__(item, 'int', value)
            return item
        touched = []
        class GetterSink:
            @property
            def write(self):
                touched.append('getter')
                raise AssertionError(marker)
        for trace_value, corr_value, comp_value in [(evil_trace, corr, 'pixs.kernel'), (good, forged_none, 'pixs.kernel'), (good, forged_int(True), 'pixs.kernel'), (good, forged_int(None), 'pixs.kernel'), (good, forged_int('42'), 'pixs.kernel'), (good, forged_int(-1), 'pixs.kernel'), (good, forged_int(2**128), 'pixs.kernel'), (good, forged_int(EvilInt(5)), 'pixs.kernel'), (good, evil_uuid, 'pixs.kernel'), (good, corr, evil_comp), (good, corr, 'acme.unknown'), (123, corr, 'pixs.kernel')]:
            try:
                target.emit_correlated_log(traceparent=trace_value, correlation_id=corr_value, component_id=comp_value, sink=GetterSink())
            except target.CorrelatedLogError as error:
                assert str(error) == 'correlated log invalid'
                assert error.__cause__ is None
                assert error.__suppress_context__ is True
                assert marker not in str(error)
            else:
                raise AssertionError('refusal expected')
        for item in bad_traces:
            try:
                target.emit_correlated_log(traceparent=item, correlation_id=corr, component_id='pixs.kernel', sink=GetterSink())
            except target.CorrelatedLogError as error:
                assert error.__cause__ is None
            else:
                raise AssertionError('trace refusal expected')
        assert touched == []
        assert trap_calls == []
        assert all(g.call_count == 0 for g in guards)
        class WriteSink:
            def __init__(self, mode):
                self.mode = mode
                self.calls = 0
                self.data = ''
                self.flushes = 0
                self.closes = 0
            def write(self, data):
                self.calls += 1
                self.data += data[:-1] if self.mode == 'short' else data[:10] if self.mode == 'raises' else data
                if self.mode == 'raises':
                    raise RuntimeError(marker)
                if self.mode == 'short':
                    return len(data) - 1
                if self.mode == 'none':
                    return None
                if self.mode == 'bool':
                    return True
                if self.mode == 'str':
                    return marker
                if self.mode == 'intsubclass':
                    return EvilInt(len(data))
                return len(data)
            def flush(self):
                self.flushes += 1
                raise AssertionError('flush forbidden')
            def close(self):
                self.closes += 1
                raise AssertionError('close forbidden')
        for mode in ('short', 'raises', 'none', 'bool', 'str', 'intsubclass'):
            sink = WriteSink(mode)
            assert sink.calls == 0 and sink.data == ''
            try:
                target.emit_correlated_log(traceparent=good, correlation_id=corr, component_id='pixs.kernel', sink=sink)
            except target.CorrelatedLogError as error:
                assert str(error) == 'correlated log invalid'
                assert error.__cause__ is None and error.__suppress_context__ is True
                assert marker not in str(error)
            else:
                raise AssertionError('write refusal expected')
            assert sink.calls == 1 and sink.data.startswith('{')
            assert sink.flushes == 0 and sink.closes == 0
            if mode in ('short', 'raises'):
                assert not sink.data.endswith(chr(10))
            else:
                assert sink.data.endswith(chr(10))
        try:
            target.emit_correlated_log(traceparent=good, correlation_id=corr, component_id='pixs.kernel', sink=GetterSink())
        except target.CorrelatedLogError as error:
            assert str(error) == 'correlated log invalid'
            assert error.__cause__ is None and error.__suppress_context__ is True
            assert marker not in str(error)
        else:
            raise AssertionError('getter refusal expected')
        assert touched == ['getter']
        class NonCallableSink:
            write = 42
        try:
            target.emit_correlated_log(traceparent=good, correlation_id=corr, component_id='pixs.kernel', sink=NonCallableSink())
        except target.CorrelatedLogError as error:
            assert str(error) == 'correlated log invalid'
        else:
            raise AssertionError('noncallable refusal expected')
        try:
            target.parse_traceparent(marker)
        except target.CorrelatedLogError as error:
            assert str(error) == 'correlated log invalid' and marker not in str(error)
        else:
            raise AssertionError('parse refusal expected')
        assert all(g.call_count == 0 for g in guards)
        assert settings.configured is False and apps.ready is False
        assert trap_calls == []
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


if __name__ == '__main__':
    unittest.main()
