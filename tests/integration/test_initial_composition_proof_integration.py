"""Integration tests for initial proof with real manifests."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_CACHE = str(_ROOT / "frontend" / ".cache")
_ENV = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "PYTHONDONTWRITEBYTECODE": "1",
    "TMPDIR": _CACHE,
}


_REAL_PIPELINE_CODE = textwrap.dedent("""
    import sys
    root = sys.argv[1]
    src = sys.argv[2]
    sys.path.insert(0, src)
    import builtins
    import itertools
    import json
    import os
    import pathlib
    import socket
    from pathlib import Path
    from unittest import mock
    import psycopg
    import django
    from django.apps import apps
    from django.conf import LazySettings
    from django.conf import settings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper
    from pixs.backend.composition_initial import MANIFEST_PATHS
    from pixs.kernel.composition import resolve as real_resolve
    pg_one = mock.Mock(side_effect=AssertionError("pg forbidden"))
    pg_two = mock.Mock(side_effect=AssertionError("pg forbidden"))
    pg_three = mock.Mock(side_effect=AssertionError("pg forbidden"))
    sock_one = mock.Mock(side_effect=AssertionError("socket forbidden"))
    sock_two = mock.Mock(side_effect=AssertionError("socket forbidden"))
    setup_guard = mock.Mock(side_effect=AssertionError("setup forbidden"))
    configure_guard = mock.Mock(side_effect=AssertionError("configure forbidden"))
    with mock.patch.object(psycopg, "connect", pg_one):
        with mock.patch.object(psycopg.Connection, "connect", pg_two):
            with mock.patch.object(EngineWrapper, "get_new_connection", pg_three):
                with mock.patch.object(socket.socket, "connect", sock_one):
                    with mock.patch.object(socket, "create_connection", sock_two):
                        with mock.patch.object(django, "setup", setup_guard):
                            with mock.patch.object(LazySettings, "configure", configure_guard):
                                base = Path(root)
                                texts = tuple((base / rel).read_text(encoding="utf-8") for rel in MANIFEST_PATHS)
                                assert len(texts) == 3
                                open_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
                                path_open_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
                                path_text_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
                                path_bytes_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
                                os_open_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
                                os_scan_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
                                with mock.patch.object(builtins, "open", open_guard):
                                    with mock.patch.object(Path, "open", path_open_guard):
                                        with mock.patch.object(Path, "read_text", path_text_guard):
                                            with mock.patch.object(Path, "read_bytes", path_bytes_guard):
                                                with mock.patch.object(os, "open", os_open_guard):
                                                    with mock.patch.object(os, "scandir", os_scan_guard):
                                                        import pixs.backend.composition_proof as target
                                                        calls = []
                                                        def wrap_resolve(items):
                                                            result = real_resolve(items)
                                                            calls.append(result)
                                                            return result
                                                        with mock.patch.object(target, "resolve", wrap_resolve):
                                                            first = target.build_initial_proof(texts)
                                                            second = target.build_initial_proof(texts)
                                                            assert first == second
                                                            for perm in itertools.permutations(texts):
                                                                assert target.build_initial_proof(perm) == first
                                                            proof = json.loads(first)
                                                            assert proof["partial"] is True
                                                            assert proof["activated"] is False
                                                            assert proof["globally_compatible"] is False
                                                            assert proof["checks"] == ["discover", "validate", "resolve"]
                                                            assert proof["evaluated_scope"] == ["capabilities", "components", "contracts"]
                                                            assert "conformity" in proof["unevaluated_dimensions"]
                                                            assert "profiles" in proof["unevaluated_dimensions"]
                                                            assert settings.configured is False
                                                            assert apps.ready is False
                                                            assert "SECRET_KEY" not in first
                                                            assert "fallback" not in first
                                                            assert open_guard.call_count == 0
                                                            assert len(calls) == 8
                                                            actual_edges, actual_order, diagnostics = calls[0]
                                                            assert diagnostics == ()
                                                            assert proof["order"] == list(actual_order)
                                                            assert proof["edges"] == [list(edge) for edge in sorted(set(actual_edges))]
                                assert pg_one.call_count == 0
                                assert pg_two.call_count == 0
                                assert pg_three.call_count == 0
                                assert sock_one.call_count == 0
                                assert sock_two.call_count == 0
                                assert setup_guard.call_count == 0
                                assert configure_guard.call_count == 0
    print("REAL_OK")
""")


class TestRealPipeline(unittest.TestCase):
    def test_real_joint_determinism(self) -> None:
        result = subprocess.run(
            [sys.executable, "-B", "-c", _REAL_PIPELINE_CODE, str(_ROOT), _SRC],
            timeout=30,
            capture_output=True,
            text=True,
            env=_ENV,
            cwd=str(_ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REAL_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
