"""Bounded browser harness for the shell adapter, outside discovery."""

import json
import subprocess
import sys
import threading
import time
import urllib.request
from contextlib import ExitStack
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_SRC = str(_ROOT / "src")
_DIST = _ROOT / "frontend" / "dist"
_NODE = "/home/devops/node/current/bin/node"
_SCRIPT = _ROOT / "frontend" / "tests" / "browser-check.mjs"
_HOST = "127.0.0.1"
_PORT = 5173
_TIMEOUT = 120


def _build_app():
    from unittest import mock
    import psycopg
    from django.db.backends.postgresql.base import DatabaseWrapper as PostgresWrapper
    stack = ExitStack()
    psycopg_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    connection_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    wrapper_guard = mock.Mock(side_effect=AssertionError("network forbidden"))
    stack.enter_context(mock.patch.object(psycopg, "connect", psycopg_guard))
    stack.enter_context(mock.patch.object(psycopg.Connection, "connect", connection_guard))
    stack.enter_context(mock.patch.object(PostgresWrapper, "get_new_connection", wrapper_guard))
    try:
        from django.conf import settings
        from django.apps import apps
        assert settings.configured is False
        assert apps.ready is False
        from pixs.backend.shell_adapter import build_shell_views
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.http_route_guard import build_declared_urlpatterns
        views = build_shell_views(_DIST)
        declarations = [RouteDeclaration("", "shell-root", views["index.html"], True)]
        for key in sorted(views):
            if key != "index.html":
                declarations.append(RouteDeclaration(key, "shell-" + key.replace("/", "-"), views[key], True))
        declarations.append(RouteDeclaration("route-inconnue-xyz", "shell-unknown-ui", views["index.html"], True))
        patterns = build_declared_urlpatterns(declarations)
        import types
        urlconf = types.ModuleType("shell_browser_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["shell_browser_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="shell_browser_urlconf",
            ALLOWED_HOSTS=[_HOST],
            INSTALLED_APPS=(),
            MIDDLEWARE=(),
            LOGGING_CONFIG=None,
            DATABASES={"default": {"ENGINE": "django.db.backends.postgresql"}},
        )
        import django
        django.setup()
        from django.core.checks import run_checks
        errors = [entry for entry in run_checks(databases=[]) if entry.level >= 40]
        assert errors == []
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application(), (psycopg_guard, connection_guard, wrapper_guard), stack
    except BaseException:
        stack.close()
        raise


def main() -> int:
    from wsgiref.simple_server import make_server
    application, guards, stack = _build_app()
    with stack:
        server = make_server(_HOST, _PORT, application)
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        thread.start()
        browser_exc = None
        browser_completed = None
        browser_payload = None
        try:
            deadline = time.time() + 20
            while True:
                try:
                    with urllib.request.urlopen(f"http://{_HOST}:{_PORT}/", timeout=2) as response:
                        if response.status == 200:
                            break
                except Exception:
                    pass
                if time.time() > deadline:
                    raise AssertionError("django server unavailable")
                time.sleep(0.2)
            env = {"PATH": "/usr/bin:/bin:/home/devops/node/current/bin", "LANG": "C.UTF-8",
                   "TMPDIR": str(_ROOT / "frontend" / ".cache")}
            try:
                browser_completed = subprocess.run(
                    [_NODE, str(_SCRIPT)],
                    timeout=_TIMEOUT,
                    capture_output=True,
                    text=True,
                    env=env,
                    cwd=str(_ROOT),
                )
            except Exception:
                raise AssertionError("browser harness failed") from None
            browser_payload = json.loads(browser_completed.stdout.strip().splitlines()[-1])
            assert browser_completed.returncode == 0
            assert browser_payload["ok"] is True
            assert browser_payload["cleanup"]["profileRemoved"] is True
            assert browser_payload["cleanup"]["processClosed"] is True
        except BaseException as error:
            browser_exc = error
        finally:
            try:
                server.shutdown()
            finally:
                thread.join(timeout=10)
                server.server_close()
        thread_joined = thread.is_alive() is False
        server_closed = thread_joined and server.fileno() == -1
        print(json.dumps({"browser": browser_payload, "cleanup": {
            "processClosed": browser_payload is not None and browser_payload["cleanup"]["processClosed"] is True,
            "profileRemoved": browser_payload is not None and browser_payload["cleanup"]["profileRemoved"] is True},
            "serverClosed": server_closed, "threadJoined": thread_joined,
            "guards": [guard.call_count for guard in guards]}, indent=2))
        for guard in guards:
            assert guard.call_count == 0
        if browser_exc is not None:
            raise browser_exc
        assert browser_completed is not None and browser_completed.returncode == 0
        assert browser_payload is not None and browser_payload["ok"] is True
        assert server_closed is True
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
