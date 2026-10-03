"""Unit tests liveness view, no Django configured in the parent."""

import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}


def _run(code: str, arg: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "-c", code, arg],
        timeout=30,
        capture_output=True,
        text=True,
        env=_ENV,
        cwd=str(_ROOT),
    )


_PURE_IMPORT_CODE = textwrap.dedent(f'''
    import sys
    sys.path.insert(0, {repr(_SRC)})
    import importlib.abc

    class BlockDjango(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == "django" or name.startswith("django."):
                raise ImportError("Django blocked in pure import")
            return None

    sys.meta_path.insert(0, BlockDjango())
    import pixs.backend.liveness_view as view
    assert "django" not in sys.modules
    assert "django.conf" not in sys.modules
    assert tuple(view.__all__) == ("LivenessError", "liveness_view")
    print("PUR")
''')


_METHODS_CODE = textwrap.dedent(r'''
    import sys
    import types
    src = sys.argv[1]
    sys.path.insert(0, src)
    from django.conf import settings
    if not settings.configured:
        settings.configure(DEFAULT_CHARSET="utf-8", LOGGING_CONFIG=None)
    from pixs.backend.liveness_view import LivenessError, liveness_view

    def fake_request(method):
        return types.SimpleNamespace(method=method)

    for exact in ("GET", "HEAD"):
        response = liveness_view(fake_request(exact))
        assert response.status_code == 200
        assert bytes(response.content) == b""
        assert response["Content-Type"] == "text/plain; charset=utf-8"
        assert response["Cache-Control"] == "no-store"

    for other in ("POST", "PUT", "DELETE", "PATCH", "OPTIONS", "get", "head", "", "GET "):
        response = liveness_view(fake_request(other))
        assert response.status_code == 405
        assert bytes(response.content) == b""
        assert response["Content-Type"] == "text/plain; charset=utf-8"
        assert response["Cache-Control"] == "no-store"
        assert response["Allow"] == "GET, HEAD"

    class FakeWsgiRequest:
        def __init__(self, method):
            self.method = method

    class FakeAsgiRequest:
        def __init__(self, method):
            self.method = method

    assert liveness_view(FakeWsgiRequest("GET")).status_code == 200
    assert liveness_view(FakeAsgiRequest("HEAD")).status_code == 200
    print("METHODS")
''')


_INVALID_REQUEST_CODE = textwrap.dedent(r'''
    import sys
    import types
    src = sys.argv[1]
    sys.path.insert(0, src)
    from django.conf import settings
    if not settings.configured:
        settings.configure(DEFAULT_CHARSET="utf-8", LOGGING_CONFIG=None)
    from pixs.backend.liveness_view import LivenessError, liveness_view

    for bad in (None, 123, b"GET", ["GET"], {"method": "GET"}):
        try:
            liveness_view(bad)
        except LivenessError as error:
            assert str(error) == "Invalid liveness request."
        else:
            raise AssertionError("invalid request refused")

    for bad_method in (None, 123, b"GET", ["GET"]):
        try:
            liveness_view(types.SimpleNamespace(method=bad_method))
        except LivenessError as error:
            assert str(error) == "Invalid liveness request."
            assert "GET" not in str(error) or str(error) == "Invalid liveness request."
        else:
            raise AssertionError("invalid method refused")

    try:
        liveness_view(types.SimpleNamespace())
    except LivenessError:
        pass
    else:
        raise AssertionError("missing method refused")
    class HostileRequest:
        @property
        def method(self):
            raise ValueError("RAW_HOSTILE_METHOD_MARKER")
        def __repr__(self):
            raise AssertionError("repr forbidden")

    class HostileMethod(str):
        def __eq__(self, other):
            raise AssertionError("comparison forbidden")

    for hostile in (HostileRequest(), types.SimpleNamespace(method=HostileMethod("GET"))):
        try:
            liveness_view(hostile)
        except LivenessError as error:
            assert str(error) == "Invalid liveness request."
            assert "RAW_HOSTILE_METHOD_MARKER" not in str(error)
        else:
            raise AssertionError("hostile request refused")

    print("INVALID")
''')


class LivenessViewUnitTests(unittest.TestCase):
    def test_snippets_compile(self):
        compile(_PURE_IMPORT_CODE, "<pure>", "exec")
        compile(_METHODS_CODE, "<methods>", "exec")
        compile(_INVALID_REQUEST_CODE, "<invalid>", "exec")

    def test_pure_import_without_django(self):
        result = _run(_PURE_IMPORT_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PUR", result.stdout)

    def test_methods_without_connection(self):
        result = _run(_METHODS_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("METHODS", result.stdout)

    def test_invalid_request_stable(self):
        result = _run(_INVALID_REQUEST_CODE, _SRC)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INVALID", result.stdout)


if __name__ == "__main__":
    unittest.main()
