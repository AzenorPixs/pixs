"""Unit tests for initial proof helper in fresh subprocesses."""

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

def _run(code: str, arg: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, arg],
        timeout=30,
        capture_output=True,
        text=True,
        env=_ENV,
        cwd=str(_ROOT),
    )



_PURE_IMPORT_CODE = textwrap.dedent("""

    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    import builtins
    import importlib.abc
    import os
    import pathlib
    import socket
    from unittest import mock
    import psycopg
    from pathlib import Path
    blocked = []
    class BlockDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == "django" or name.startswith("django."):
                blocked.append(name)
                raise ImportError("Django blocked in pure import")
            return None
    sys.meta_path.insert(0, BlockDjango())
    open_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
    path_open_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
    path_text_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
    path_bytes_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
    os_open_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
    os_scan_guard = mock.Mock(side_effect=AssertionError("file forbidden"))
    pg_guard = mock.Mock(side_effect=AssertionError("pg forbidden"))
    pg_conn_guard = mock.Mock(side_effect=AssertionError("pg forbidden"))
    sock_guard = mock.Mock(side_effect=AssertionError("socket forbidden"))
    sock_create_guard = mock.Mock(side_effect=AssertionError("socket forbidden"))
    with mock.patch.object(builtins, "open", open_guard):
        with mock.patch.object(Path, "open", path_open_guard):
            with mock.patch.object(Path, "read_text", path_text_guard):
                with mock.patch.object(Path, "read_bytes", path_bytes_guard):
                    with mock.patch.object(os, "open", os_open_guard):
                        with mock.patch.object(os, "scandir", os_scan_guard):
                            with mock.patch.object(psycopg, "connect", pg_guard):
                                with mock.patch.object(psycopg.Connection, "connect", pg_conn_guard):
                                    with mock.patch.object(socket.socket, "connect", sock_guard):
                                        with mock.patch.object(socket, "create_connection", sock_create_guard):
                                            import pixs.backend.composition_proof as target
                                            assert tuple(target.__all__) == ("InitialProofError", "PROOF_VERSION", "build_initial_proof")
                                            assert target.PROOF_VERSION == "0.1.0"
                                            assert "django" not in sys.modules
                                            assert open_guard.call_count == 0
                                            assert pg_guard.call_count == 0
                                            assert sock_guard.call_count == 0
                                            assert all(guard.call_count == 0 for guard in (open_guard, path_open_guard, path_text_guard, path_bytes_guard, os_open_guard, os_scan_guard, pg_guard, pg_conn_guard, sock_guard, sock_create_guard))
                                            assert blocked == []
    print("PURE_OK")
""")

_VALID_PROOF_CODE = textwrap.dedent("""
    import builtins
    import os
    import socket
    from contextlib import contextmanager, ExitStack
    from pathlib import Path
    from unittest import mock
    import django
    import psycopg
    from django.apps import apps
    from django.conf import settings, LazySettings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper

    @contextmanager
    def guarded_calls():
        targets = [
            (builtins, "open"), (Path, "open"), (Path, "read_text"),
            (Path, "read_bytes"), (os, "open"), (os, "scandir"),
            (psycopg, "connect"), (psycopg.Connection, "connect"),
            (EngineWrapper, "get_new_connection"),
            (socket.socket, "connect"), (socket, "create_connection"),
            (django, "setup"), (LazySettings, "configure"),
        ]
        guards = [mock.Mock(side_effect=AssertionError("operation forbidden"))
                  for _ in targets]
        assert settings.configured is False and apps.ready is False
        with ExitStack() as stack:
            for (owner, name), guard in zip(targets, guards):
                stack.enter_context(mock.patch.object(owner, name, guard))
            yield guards
            assert all(guard.call_count == 0 for guard in guards)
            assert settings.configured is False and apps.ready is False


    import sys
    src = sys.argv[1]
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
    from pixs.kernel.composition import discover as real_discover
    from pixs.kernel.composition import validate as real_validate
    from pixs.kernel.composition import resolve as real_resolve
    kernel_text = 'schema_version = "1"\\nid = "pixs.kernel"\\ntype = "KERNEL"\\nversion = "0.1.0"\\n'
    core_text = 'schema_version = "1"\\nid = "pixs.core"\\ntype = "MODULE"\\nversion = "0.1.0"\\n[dependencies]\\ncomponents = ["pixs.kernel ==0.1.0"]\\n'
    example_text = 'schema_version = "1"\\nid = "example.hello"\\ntype = "MODULE"\\nversion = "1.0.0"\\n[provides]\\n[[provides.capabilities]]\\nid = "example.hello"\\nversion = "1.0.0"\\ncontracts = ["example.hello.contract"]\\ncriticality = "REQUIRED"\\nfallback = "none"\\n[implements]\\n[[implements.contracts]]\\nid = "example.hello.contract"\\nversion = "1.0.0"\\n'
    opaque_name = 'name = "OPAQUE_MARKER_XYZ_001"\\n'
    named_example = opaque_name + example_text
    with guarded_calls():
        import pixs.backend.composition_proof as target
        calls = []
        def wrap_discover(items):
            calls.append("discover")
            return real_discover(items)
        def wrap_validate(items, official_ids=(), required_ids=()):
            calls.append("validate")
            return real_validate(items, official_ids=official_ids, required_ids=required_ids)
        def wrap_resolve(items):
            calls.append("resolve")
            return real_resolve(items)
        with mock.patch.object(target, "discover", wrap_discover):
            with mock.patch.object(target, "validate", wrap_validate):
                with mock.patch.object(target, "resolve", wrap_resolve):
                    first = target.build_initial_proof((kernel_text, core_text, example_text))
                    second = target.build_initial_proof((kernel_text, core_text, example_text))
                    assert first == second
                    perms = list(itertools.permutations((kernel_text, core_text, example_text)))
                    assert len(perms) == 6
                    for perm in perms:
                        assert target.build_initial_proof(perm) == first
                    assert calls == ["discover", "validate", "resolve"] * 8
                    proof = json.loads(first)
                    assert proof["partial"] is True
                    assert proof["activated"] is False
                    assert proof["globally_compatible"] is False
                    assert proof["proof_version"] == "0.1.0"
                    assert first == json.dumps(proof, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                    assert proof["capabilities"] == [{"id": "example.hello", "owner": "example.hello", "version": "1.0.0"}]
                    assert proof["contracts"] == [{"id": "example.hello.contract", "owner": "example.hello", "version": "1.0.0"}]
                    assert proof["checks"] == ["discover", "validate", "resolve"]
                    assert proof["evaluated_scope"] == ["capabilities", "components", "contracts"]
                    assert "conformity" in proof["unevaluated_dimensions"]
                    assert "profiles" in proof["unevaluated_dimensions"]
                    assert {entry["id"] for entry in proof["components"]} == {"pixs.kernel", "pixs.core", "example.hello"}
                    assert proof["order"].index("pixs.kernel") < proof["order"].index("pixs.core")
                    assert "OPAQUE" not in first
                    assert "fallback" not in first
                    assert "warnings" not in first
                    named = target.build_initial_proof((kernel_text, core_text, named_example))
                    assert "OPAQUE_MARKER_XYZ_001" not in named
                    assert named == first
                print("VALID_OK")
""")

_NEGATIVE_CODE = textwrap.dedent("""
    import builtins
    import os
    import socket
    from contextlib import contextmanager, ExitStack
    from pathlib import Path
    from unittest import mock
    import django
    import psycopg
    from django.apps import apps
    from django.conf import settings, LazySettings
    from django.db.backends.postgresql.base import DatabaseWrapper as EngineWrapper

    @contextmanager
    def guarded_calls():
        targets = [
            (builtins, "open"), (Path, "open"), (Path, "read_text"),
            (Path, "read_bytes"), (os, "open"), (os, "scandir"),
            (psycopg, "connect"), (psycopg.Connection, "connect"),
            (EngineWrapper, "get_new_connection"),
            (socket.socket, "connect"), (socket, "create_connection"),
            (django, "setup"), (LazySettings, "configure"),
        ]
        guards = [mock.Mock(side_effect=AssertionError("operation forbidden"))
                  for _ in targets]
        assert settings.configured is False and apps.ready is False
        with ExitStack() as stack:
            for (owner, name), guard in zip(targets, guards):
                stack.enter_context(mock.patch.object(owner, name, guard))
            yield guards
            assert all(guard.call_count == 0 for guard in guards)
            assert settings.configured is False and apps.ready is False


    import sys
    src = sys.argv[1]
    sys.path.insert(0, src)
    import builtins
    from pathlib import Path
    from unittest import mock
    import pixs.backend.composition_proof as target
    kernel_text = 'schema_version = "1"\\nid = "pixs.kernel"\\ntype = "KERNEL"\\nversion = "0.1.0"\\n'
    core_text = 'schema_version = "1"\\nid = "pixs.core"\\ntype = "MODULE"\\nversion = "0.1.0"\\n[dependencies]\\ncomponents = ["pixs.kernel ==0.1.0"]\\n'
    example_text = 'schema_version = "1"\\nid = "example.hello"\\ntype = "MODULE"\\nversion = "1.0.0"\\n[provides]\\n[[provides.capabilities]]\\nid = "example.hello"\\nversion = "1.0.0"\\ncontracts = ["example.hello.contract"]\\ncriticality = "REQUIRED"\\nfallback = "none"\\n[implements]\\n[[implements.contracts]]\\nid = "example.hello.contract"\\nversion = "1.0.0"\\n'
    marker = "OPAQUE_MARKER_XYZ_002"
    unknown_schema = 'schema_version = "2"\\nid = "pixs.kernel"\\ntype = "KERNEL"\\nversion = "0.1.0"\\n'
    malformed_id = 'schema_version = "1"\\nid = "bad id with spaces"\\ntype = "MODULE"\\nversion = "1.0.0"\\n'
    extra_text = 'schema_version = "1"\\nid = "acme.extra"\\ntype = "MODULE"\\nversion = "1.0.0"\\n'
    wrong_role = 'schema_version = "1"\\nid = "pixs.kernel"\\ntype = "MODULE"\\nversion = "0.1.0"\\n'
    dep_text = 'schema_version = "1"\\nid = "example.hello"\\ntype = "MODULE"\\nversion = "1.0.0"\\n[dependencies]\\ncomponents = ["acme.absent >=1.0.0"]\\n'
    cycle_core = 'schema_version = "1"\\nid = "pixs.core"\\ntype = "MODULE"\\nversion = "0.1.0"\\n[dependencies]\\ncomponents = ["pixs.kernel ==0.1.0", "example.hello"]\\n'
    cycle_example = 'schema_version = "1"\\nid = "example.hello"\\ntype = "MODULE"\\nversion = "1.0.0"\\n[dependencies]\\ncomponents = ["pixs.core"]\\n[provides]\\n[[provides.capabilities]]\\nid = "example.hello"\\nversion = "1.0.0"\\ncontracts = ["example.hello.contract"]\\ncriticality = "REQUIRED"\\nfallback = "none"\\n[implements]\\n[[implements.contracts]]\\nid = "example.hello.contract"\\nversion = "1.0.0"\\n'
    big_text = "x" * 70000
    trap_calls = []
    class EvilTuple(tuple):
        def __len__(self):
            trap_calls.append("len")
            raise AssertionError("trap len")
    class EvilStr(str):
        def __hash__(self):
            trap_calls.append("hash")
            raise AssertionError("trap hash")
        def __eq__(self, other):
            trap_calls.append("eq")
            raise AssertionError("trap eq")
        def encode(self, *args, **kwargs):
            trap_calls.append("encode")
            raise AssertionError("trap encode")
    evil_tuple = EvilTuple((kernel_text, core_text, example_text))
    evil_str = EvilStr(kernel_text)
    cases = []
    cases.append(evil_tuple)
    cases.append((evil_str, core_text, example_text))
    cases.append([kernel_text, core_text, example_text])
    cases.append((kernel_text, core_text))
    cases.append((kernel_text, core_text, example_text, kernel_text))
    cases.append((kernel_text, None, example_text))
    cases.append(("", core_text, example_text))
    cases.append(("\\ud800", core_text, example_text))
    cases.append((big_text, core_text, example_text))
    cases.append((unknown_schema, core_text, example_text))
    cases.append((malformed_id, core_text, example_text))
    cases.append((kernel_text, core_text, extra_text))
    cases.append((kernel_text, kernel_text, core_text))
    cases.append((wrong_role, core_text, example_text))
    cases.append((kernel_text, core_text, dep_text))
    cases.append((kernel_text, cycle_core, cycle_example))
    cases.append((kernel_text, core_text, 'name = "' + marker + '"\\ninvalid_field = 1\\n' + example_text))
    cases.append(("[", core_text, example_text))
    cases.append((kernel_text + "#" + "é" * 40000, core_text, example_text))
    with guarded_calls():
        import pixs.kernel.composition as pipeline
        from pixs.kernel.composition import resolve as real_resolve
        reached = []
        def wrap_resolve(items):
            reached.append("resolve")
            return real_resolve(items)
        with mock.patch.object(target, "resolve", wrap_resolve):
            for value in cases:
                try:
                    target.build_initial_proof(value)
                except target.InitialProofError as error:
                    assert str(error) == "initial composition invalid"
                    assert error.__cause__ is None
                    assert marker not in str(error)
                    assert "acme.absent" not in str(error)
                else:
                    raise AssertionError("refusal expected")
            assert len(reached) == 2
            assert trap_calls == []
        print("NEGATIVE_OK")
""")

class TestPureImport(unittest.TestCase):
    def test_pure_import(self) -> None:
        result = _run(_PURE_IMPORT_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PURE_OK", result.stdout)


class TestValidProof(unittest.TestCase):
    def test_valid_determinism_pipeline(self) -> None:
        result = _run(_VALID_PROOF_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID_OK", result.stdout)


class TestNegative(unittest.TestCase):
    def test_generic_refusals(self) -> None:
        result = _run(_NEGATIVE_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NEGATIVE_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
