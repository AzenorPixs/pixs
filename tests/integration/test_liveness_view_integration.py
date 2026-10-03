"""Integration tests liveness view, synthetic Django alone via guard."""

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]


def _src() -> str:
    return str(_ROOT / "src")


def _run(code: str, arg: str) -> subprocess.CompletedProcess[str]:
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, "-B", "-c", code, arg],
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
        from pixs.backend.liveness_view import liveness_view
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.http_route_guard import build_declared_urlpatterns
        calls = []
        def private_view(request):
            calls.append(1)
            from django.http import HttpResponse
            return HttpResponse(b"x", status=200, content_type="text/plain; charset=utf-8")
        patterns = build_declared_urlpatterns([
            RouteDeclaration("live-synth/", "live-synth", liveness_view, True),
            RouteDeclaration("private-synth/", "private-synth", private_view, False),
        ])
        assert len(patterns) == 3
        assert [m.name for m in patterns[:2]] == ["live-synth", "private-synth"]
        urlconf = types.ModuleType("synthetic_liveness_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["synthetic_liveness_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="synthetic_liveness_urlconf",
            ALLOWED_HOSTS=["testserver"],
            INSTALLED_APPS=(),
            MIDDLEWARE=(),
            LOGGING_CONFIG=None,
            DATABASES={"default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "db-synthetique",
            }},
        )
        import django
        django.setup()
        from django.test import Client
        from django.urls import resolve
        from django.core.checks import run_checks
        errors = [m for m in run_checks(databases=[]) if m.level >= 40]
        assert errors == []
        assert resolve("/live-synth/").func is liveness_view
        client = Client()
        live_get = client.get("/live-synth/")
        assert live_get.status_code == 200
        assert bytes(live_get.content) == b""
        assert live_get["Content-Type"] == "text/plain; charset=utf-8"
        assert live_get["Cache-Control"] == "no-store"
        live_head = client.head("/live-synth/")
        assert live_head.status_code == 200
        assert bytes(live_head.content) == b""
        assert live_head["Cache-Control"] == "no-store"
        live_post = client.post("/live-synth/")
        assert live_post.status_code == 405
        assert bytes(live_post.content) == b""
        assert live_post["Allow"] == "GET, HEAD"
        assert live_post["Cache-Control"] == "no-store"
        for method in ("get", "post", "head"):
            private_response = getattr(client, method)("/private-synth/")
            assert private_response.status_code == 403
            assert private_response["Content-Type"] == "text/plain; charset=utf-8"
        assert calls == []
        for path in ("/absent-synth/", "/live-synth/extra/"):
            unknown = client.get(path)
            assert unknown.status_code == 404
            assert unknown.content.decode("utf-8") == "Route inconnue."
            assert path not in unknown.content.decode("utf-8")
        from django.core.handlers.wsgi import WSGIRequest
        wsgi_environ = {"REQUEST_METHOD": "GET", "PATH_INFO": "/live-synth/",
            "SERVER_NAME": "testserver", "SERVER_PORT": "80", "wsgi.input": __import__("io").BytesIO(b"")}
        wsgi_response = liveness_view(WSGIRequest(wsgi_environ))
        assert wsgi_response.status_code == 200
        assert bytes(wsgi_response.content) == b""
        from django.core.handlers.asgi import ASGIRequest
        from io import BytesIO
        asgi_scope = {"type": "http", "http_version": "1.1", "method": "HEAD",
            "path": "/live-synth/", "headers": []}
        asgi_response = liveness_view(ASGIRequest(asgi_scope, BytesIO(b"")))
        assert asgi_response.status_code == 200
        assert bytes(asgi_response.content) == b""
        assert asgi_response["Content-Type"] == "text/plain; charset=utf-8"
        assert asgi_response["Cache-Control"] == "no-store"
        asgi_mark = "asgi-ok"
        assert psycopg_guard.call_count == 0
        assert connection_guard.call_count == 0
        assert wrapper_guard.call_count == 0
        assert socket_guard.call_count == 0
        assert create_connection_guard.call_count == 0
        assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
        from django.db import connections
        assert connections["default"].connection is None
    print(json.dumps({"integration": True, "asgi": asgi_mark}))
''')


class LivenessViewIntegrationTests(unittest.TestCase):
    def test_snippet_compile(self):
        compile(_CODE, "<integration>", "exec")

    def test_real_http_cycle_without_connections(self):
        result = _run(_CODE, _src())
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["integration"])
        self.assertEqual(payload["asgi"], "asgi-ok")


if __name__ == "__main__":
    unittest.main()
