"""Tests d’integration garde de routes, Django synthetique isole seul."""

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
    psycopg_guard = mock.Mock(side_effect=AssertionError("reseau interdit"))
    connection_guard = mock.Mock(side_effect=AssertionError("reseau interdit"))
    wrapper_guard = mock.Mock(side_effect=AssertionError("reseau interdit"))
    socket_guard = mock.Mock(side_effect=AssertionError("reseau interdit"))
    create_connection_guard = mock.Mock(side_effect=AssertionError("reseau interdit"))
    with (
        mock.patch.object(psycopg, "connect", psycopg_guard),
        mock.patch.object(psycopg.Connection, "connect", connection_guard),
        mock.patch.object(PostgresWrapper, "get_new_connection", wrapper_guard),
        mock.patch.object(socket.socket, "connect", socket_guard),
        mock.patch.object(socket, "create_connection", create_connection_guard),
    ):
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.http_route_guard import build_declared_urlpatterns
        from pixs.backend.api import build_success_response
        calls = []
        def public_view(request):
            return build_success_response({"ok": True}, meta={}, links={})
        def private_view(request):
            calls.append(1)
            return build_success_response({}, meta={}, links={})
        patterns = build_declared_urlpatterns([
            RouteDeclaration("", "racine", public_view, True),
            RouteDeclaration("ok/", "ok", public_view, True),
            RouteDeclaration("ko/", "ko", private_view, False),
        ])
        assert len(patterns) == 4
        assert [m.name for m in patterns[:3]] == ["racine", "ok", "ko"]
        urlconf = types.ModuleType("synthetique_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["synthetique_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="synthetique_urlconf",
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
        client = Client()
        public_response = client.get("/ok/")
        assert public_response.status_code == 200
        assert public_response["Content-Type"] == "application/json; charset=utf-8"
        assert json.loads(public_response.content.decode("utf-8"))["data"] == {"ok": True}
        assert resolve("/ok/").func is public_view
        root_response = client.get("/")
        assert root_response.status_code == 200
        for method in ("get", "post", "head"):
            private_response = getattr(client, method)("/ko/")
            assert private_response.status_code == 403
            assert private_response["Content-Type"] == "text/plain; charset=utf-8"
            if method == "head":
                assert private_response.content == b""
            else:
                assert private_response.content.decode("utf-8") == "Route non publique."
        assert calls == []
        encoded_response = client.get("/ok/%0A")
        assert encoded_response.status_code == 404
        assert encoded_response.content.decode("utf-8") == "Route inconnue."
        match = resolve("/ok/\n")
        assert match.url_name is None
        catchall_response = match.func(None)
        assert catchall_response.status_code == 404
        assert catchall_response.content.decode("utf-8") == "Route inconnue."
        for path in ("/absente/", "/a/b/c"):
            response = client.get(path)
            assert response.status_code == 404
            assert response["Content-Type"] == "text/plain; charset=utf-8"
            body = response.content.decode("utf-8")
            assert body == "Route inconnue."
            assert path not in body
        assert psycopg_guard.call_count == 0
        assert connection_guard.call_count == 0
        assert wrapper_guard.call_count == 0
        assert socket_guard.call_count == 0
        assert create_connection_guard.call_count == 0
        assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
        from django.db import connections
        assert connections["default"].connection is None
        empty_patterns = build_declared_urlpatterns([])
        assert len(empty_patterns) == 1
        unknown_empty = empty_patterns[0].callback(None)
        assert unknown_empty.status_code == 404
        assert unknown_empty.content.decode("utf-8") == "Route inconnue."
    print(json.dumps({"integration": True}))
''')


class HttpRouteGuardIntegrationTests(unittest.TestCase):
    def test_snippet_compile(self):
        compile(_CODE, "<integration>", "exec")

    def test_real_http_cycle_without_connections(self):
        before = "django" in sys.modules
        result = _run(_CODE, _src())
        self.assertEqual(
            result.returncode, 0,
            f"stdout={result.stdout} stderr={result.stderr}",
        )
        data = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(data, {"integration": True})
        self.assertEqual("django" in sys.modules, before)


if __name__ == "__main__":
    unittest.main()
