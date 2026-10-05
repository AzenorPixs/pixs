"""Bounded browser harness for the joint composition, outside discovery."""

import json
import subprocess
import sys
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
        from pixs.backend.api import ApiContractPlan, build_success_response
        from pixs.kernel.contracts import ContractCategory, ContractDescriptor
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.local_test_composition import build_local_test_urlpatterns, local_test_server
        status_schema = {"type": "object",
            "properties": {"data": {"type": "object",
                "properties": {"status": {"type": "string"}},
                "required": ["status"]},
                "meta": {"type": "object"}, "links": {"type": "object"}},
            "required": ["data", "meta", "links"]}
        status_media = {"application/json": {"schema": status_schema}}
        status_operation = {"responses": {"200": {"description": "Status.", "content": status_media}}}
        document = json.dumps({"openapi": "3.1.0",
            "info": {"title": "Synthetic Status", "version": "1.0.0"},
            "security": [],
            "paths": {
                "/api/v1/status": {"get": status_operation},
                "/api/v1/openapi.json": {"get": {"responses": {"200": {"description": "Document."}}}},
            }})
        plan = ApiContractPlan(
            contract=ContractDescriptor(
                contract_id="pixs.contract.synthetic.status",
                category=ContractCategory.API,
                version="1.0.0",
                owner_component="pixs.backend",
                guarantees_doc="Synthetic guarantees.",
            ),
            openapi_document_ref="pixs.api.synthetic.status.v1",
        )
        def status_capacity(request):
            return build_success_response({"status": "ok"}, meta={}, links={})
        capacity = RouteDeclaration("api/v1/status", "test-api-status", status_capacity, True)
        private_calls = []
        def private_probe(request):
            private_calls.append(request.method)
            raise AssertionError("private handler must not run")
        private = RouteDeclaration("api/v1/private", "test-api-private", private_probe, False)
        patterns = build_local_test_urlpatterns(_DIST, plan, document, capacity,
            private_routes=(private,), unknown_ui_route="route-inconnue-xyz")
        import types
        urlconf = types.ModuleType("joint_browser_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["joint_browser_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="joint_browser_urlconf",
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
        return get_wsgi_application(), (psycopg_guard, connection_guard, wrapper_guard), stack, document, private_calls
    except BaseException:
        stack.close()
        raise


def main() -> int:
    from urllib.error import HTTPError
    from pixs.backend.local_test_composition import local_test_server
    application, guards, stack, document, private_calls = _build_app()
    handle = None
    browser_completed = None
    browser_payload = None
    http_results = []
    with stack:
        try:
            with local_test_server(application, host=_HOST, port=_PORT) as handle:
                origin = f"http://{_HOST}:{handle['port']}"
                def request(path, expected_status):
                    try:
                        response = urllib.request.urlopen(origin + path, timeout=5)
                    except HTTPError as error:
                        response = error
                    with response:
                        status = response.status
                        body = response.read()
                        assert status == expected_status
                        http_results.append({"path": path, "method": "GET", "status": status})
                        return body
                assert request("/health/live", 200) == b""
                assert request("/", 200) == (_DIST / "index.html").read_bytes()
                for asset in sorted((_DIST / "assets").iterdir()):
                    assert request("/assets/" + asset.name, 200) == asset.read_bytes()
                published = request("/api/v1/openapi.json", 200)
                assert published.decode("utf-8") == document
                capacity_payload = json.loads(request("/api/v1/status", 200))
                assert capacity_payload == {"data": {"status": "ok"}, "meta": {}, "links": {}}
                schema = json.loads(published)["paths"]["/api/v1/status"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
                assert schema["type"] == "object" and set(schema["required"]) == set(capacity_payload)
                assert schema["properties"]["data"]["properties"]["status"]["type"] == "string"
                request("/api/v1/private", 403)
                request("/absent-joint-xyz/", 404)
                assert private_calls == []
                env = {"PATH": "/usr/bin:/bin:/home/devops/node/current/bin", "LANG": "C.UTF-8",
                       "TMPDIR": str(_ROOT / "frontend" / ".cache")}
                try:
                    browser_completed = subprocess.run(
                        [_NODE, str(_SCRIPT)], timeout=_TIMEOUT,
                        capture_output=True, text=True, env=env, cwd=str(_ROOT))
                except Exception:
                    raise AssertionError("browser harness failed") from None
                browser_payload = json.loads(browser_completed.stdout.strip().splitlines()[-1])
                assert browser_completed.returncode == 0 and browser_payload["ok"] is True
                assert browser_payload["cleanup"]["profileRemoved"] is True
                assert browser_payload["cleanup"]["processClosed"] is True
                assert private_calls == []
        finally:
            thread_joined = handle is not None and handle["thread"].is_alive() is False
            server_closed = thread_joined and handle["server"].fileno() == -1
            cleanup = {
                "processClosed": browser_payload is not None and browser_payload["cleanup"]["processClosed"] is True,
                "profileRemoved": browser_payload is not None and browser_payload["cleanup"]["profileRemoved"] is True}
            print(json.dumps({"browser": browser_payload, "httpResults": http_results,
                "cleanup": cleanup, "serverClosed": server_closed, "threadJoined": thread_joined,
                "guards": [guard.call_count for guard in guards]}))
        assert server_closed is True
        assert all(guard.call_count == 0 for guard in guards)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
