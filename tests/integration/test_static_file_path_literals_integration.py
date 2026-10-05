"""Integration tests static literals via guard, synthetic Django alone."""

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
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.http_route_guard import build_declared_urlpatterns
        calls = []
        def public_asset(request):
            from django.http import HttpResponse
            return HttpResponse(b"asset", status=200, content_type="text/plain; charset=utf-8")
        def private_asset(request):
            calls.append(1)
            from django.http import HttpResponse
            return HttpResponse(b"x", status=200, content_type="text/plain; charset=utf-8")
        patterns = build_declared_urlpatterns([
            RouteDeclaration("assets/index-Ab12.js", "asset-js", public_asset, True),
            RouteDeclaration("assets/secret-Ab12.js", "asset-private", private_asset, False),
        ])
        assert len(patterns) == 3
        urlconf = types.ModuleType("synthetic_static_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["synthetic_static_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="synthetic_static_urlconf",
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
        assert resolve("/assets/index-Ab12.js").func is public_asset
        client = Client()
        public_response = client.get("/assets/index-Ab12.js")
        assert public_response.status_code == 200
        assert bytes(public_response.content) == b"asset"
        for method in ("get", "post", "head"):
            private_response = getattr(client, method)("/assets/secret-Ab12.js")
            assert private_response.status_code == 403
        assert calls == []
        unknown = client.get("/assets/absent-Ab12.js")
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


class StaticFilePathLiteralsIntegrationTests(unittest.TestCase):
    def test_real_http_cycle_without_connections(self):
        result = _run(_CODE, _src())
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["integration"])


if __name__ == "__main__":
    unittest.main()
