"""Integration tests shell adapter on true dist via guard."""

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]


def _src() -> str:
    return str(_ROOT / "src")


def _cache() -> str:
    return str(_ROOT / "frontend" / ".cache")


def _run(code: str, src: str, cache: str) -> subprocess.CompletedProcess[str]:
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": cache}
    return subprocess.run(
        [sys.executable, "-B", "-c", code, src, cache],
        timeout=30,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_ROOT),
    )


_CODE = textwrap.dedent(r'''
    import sys
    import types
    import json
    import socket
    import hashlib
    from pathlib import Path
    src = sys.argv[1]
    sys.path.insert(0, src)
    from unittest import mock
    from django.conf import settings as settings
    from django.apps import apps
    assert settings.configured is False
    assert apps.ready is False
    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PostgresWrapper
    psycopg_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    connection_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    wrapper_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    socket_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    create_connection_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    with (
        mock.patch.object(psycopg, "connect", psycopg_guard),
        mock.patch.object(psycopg.Connection, "connect", connection_guard),
        mock.patch.object(PostgresWrapper, "get_new_connection", wrapper_guard),
        mock.patch.object(socket.socket, "connect", socket_guard),
        mock.patch.object(socket, "create_connection", create_connection_guard),
    ):
        from pixs.backend.shell_adapter import build_shell_views
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.http_route_guard import build_declared_urlpatterns
        from pixs.backend.http_route_guard import HttpRouteGuardError
        from pixs.backend.liveness_view import liveness_view
        assert str(HttpRouteGuardError()) == "Déclaration de route invalide."
        assert liveness_view.__name__ == "liveness_view"
        root = Path("frontend/dist")
        views = build_shell_views(root)
        expected = {key: (root / key).read_bytes() for key in sorted(views)}
        assert "index.html" in expected
        assert any(key.endswith(".js") for key in expected)
        assert any(key.endswith(".css") for key in expected)
        declarations = [RouteDeclaration("", "shell-root", views["index.html"], True)]
        for key in sorted(views):
            if key != "index.html":
                declarations.append(RouteDeclaration(key, "shell-" + key.replace("/", "-"), views[key], True))
        calls = []
        def private_probe(request):
            calls.append(1)
            from django.http import HttpResponse
            return HttpResponse(b"x", status=200, content_type="text/plain; charset=utf-8")
        declarations.append(RouteDeclaration("private-shell/", "shell-private", private_probe, False))
        patterns = build_declared_urlpatterns(declarations)
        urlconf = types.ModuleType("synthetic_shell_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["synthetic_shell_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="synthetic_shell_urlconf",
            ALLOWED_HOSTS=["testserver"],
            INSTALLED_APPS=(),
            MIDDLEWARE=(),
            LOGGING_CONFIG=None,
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql"}},
        )
        import django
        django.setup()
        from django.test import Client
        from django.urls import resolve
        from django.core.checks import run_checks
        errors = [m for m in run_checks(databases=[]) if m.level >= 40]
        assert errors == []
        client = Client()
        for key in sorted(expected):
            target = "/" if key == "index.html" else "/" + key
            response = client.get(target)
            assert response.status_code == 200
            assert bytes(response.content) == expected[key]
            assert hashlib.sha256(bytes(response.content)).hexdigest() == hashlib.sha256(expected[key]).hexdigest()
            if key == "index.html":
                assert response["Content-Type"] == "text/html; charset=utf-8"
            elif key.endswith(".js"):
                assert response["Content-Type"] == "application/javascript"
            else:
                assert response["Content-Type"] == "text/css"
            assert response["Cache-Control"] == "no-store"
            head_response = client.head(target)
            assert bytes(head_response.content) == b""
            assert head_response["Content-Length"] == str(len(expected[key]))
            denied = client.post(target)
            assert denied.status_code == 405
            assert denied["Allow"] == "GET, HEAD"
            assert resolve(target).func is views[key]
        for method in ("get", "post", "head"):
            assert getattr(client, method)("/private-shell/").status_code == 403
        assert calls == []
        unknown = client.get("/absent-shell-xyz/")
        assert unknown.status_code == 404
        assert unknown.content.decode("utf-8") == "Route inconnue."
        assert psycopg_guard.call_count == 0
        assert connection_guard.call_count == 0
        assert wrapper_guard.call_count == 0
        assert socket_guard.call_count == 0
        assert create_connection_guard.call_count == 0
        from django.db import connections
        assert connections["default"].connection is None
    print(json.dumps({"integration": True}))
''')


class ShellAdapterIntegrationTests(unittest.TestCase):
    def test_real_dist_cycle_without_connections(self):
        result = _run(_CODE, _src(), _cache())
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["integration"])


if __name__ == "__main__":
    unittest.main()
