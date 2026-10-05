"""Integration tests joint local composition on true Client."""

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


def _run(code: str, src: str, cache: str, mode: str) -> subprocess.CompletedProcess[str]:
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
           "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": cache}
    return subprocess.run(
        [sys.executable, "-B", "-c", code, src, cache, mode],
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
    import urllib.request
    from pathlib import Path
    from contextlib import ExitStack
    src = sys.argv[1]
    mode = sys.argv[3]
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
    with ExitStack() as guards_stack:
        guards_stack.enter_context(mock.patch.object(psycopg, "connect", psycopg_guard))
        guards_stack.enter_context(mock.patch.object(psycopg.Connection, "connect", connection_guard))
        guards_stack.enter_context(mock.patch.object(PostgresWrapper, "get_new_connection", wrapper_guard))
        socket_patch = mock.patch.object(socket.socket, "connect", socket_guard)
        create_patch = mock.patch.object(socket, "create_connection", create_connection_guard)
        socket_patch.start()
        create_patch.start()
        guards_stack.callback(socket_patch.stop)
        guards_stack.callback(create_patch.stop)
        from pixs.backend.api import ApiContractPlan, build_success_response
        from pixs.kernel.contracts import ContractCategory, ContractDescriptor
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.local_test_composition import build_local_test_urlpatterns
        from pixs.backend.local_test_composition import UNSUPPORTED_TEST_CAPABILITIES
        assert "pg-connection" in UNSUPPORTED_TEST_CAPABILITIES
        root = Path("frontend/dist")
        status_schema = {"type": "object",
            "properties": {"data": {"type": "object",
                "properties": {"status": {"type": "string"}},
                "required": ["status"]},
                "meta": {"type": "object"}, "links": {"type": "object"}},
            "required": ["data", "meta", "links"]}
        status_media = {"application/json": {"schema": status_schema}}
        status_operation = {"operationId": "getStatus",
            "responses": {"200": {"description": "Status.", "content": status_media}}}
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
        calls = []
        def status_capacity(request):
            calls.append(request.method)
            return build_success_response({"status": "ok"}, meta={}, links={})
        private_calls = []
        def private_probe(request):
            private_calls.append(request.method)
            from django.http import HttpResponse
            return HttpResponse(b"x", status=200, content_type="text/plain; charset=utf-8")
        capacity = RouteDeclaration("api/v1/status", "test-api-status", status_capacity, True)
        private = RouteDeclaration("api/v1/private", "test-api-private", private_probe, False)
        patterns = build_local_test_urlpatterns(root, plan, document, capacity,
            private_routes=(private,), unknown_ui_route="route-inconnue-xyz")
        urlconf = types.ModuleType("synthetic_joint_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["synthetic_joint_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="synthetic_joint_urlconf",
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
        assert client.get("/health/live").status_code == 200
        assert bytes(client.get("/health/live").content) == b""
        assert client.post("/health/live").status_code == 405
        index_bytes = (root / "index.html").read_bytes()
        assert bytes(client.get("/").content) == index_bytes
        published = client.get("/api/v1/openapi.json")
        assert published.status_code == 200
        assert published.content.decode("utf-8") == document
        assert published["Content-Type"] == "application/json; charset=utf-8"
        capacity_response = client.get("/api/v1/status")
        assert capacity_response.status_code == 200
        payload = json.loads(capacity_response.content.decode("utf-8"))
        assert payload == {"data": {"status": "ok"}, "meta": {}, "links": {}}
        assert type(payload["data"]["status"]) is str
        assert bytes(client.get("/route-inconnue-xyz").content) == index_bytes
        for method in ("get", "post", "head"):
            assert getattr(client, method)("/api/v1/private").status_code == 403
        assert private_calls == []
        assert calls == ["GET"]
        assert client.get("/api/v9/ghost").status_code == 404
        assert resolve("/health/live").func.__name__ == "liveness_view"
        assert psycopg_guard.call_count == 0
        assert socket_guard.call_count == 0
        for asset in sorted((root / "assets").iterdir()):
            asset_path = "/assets/" + asset.name
            expected = asset.read_bytes()
            got = client.get(asset_path)
            assert got.status_code == 200 and got.content == expected
            expected_type = "application/javascript" if asset.suffix == ".js" else "text/css"
            assert got["Content-Type"] == expected_type
            assert got["Cache-Control"] == "no-store"
            head = client.head(asset_path)
            assert head.status_code == 200 and head.content == b""
            assert head["Content-Length"] == got["Content-Length"]
            denied = client.post(asset_path)
            assert denied.status_code == 405 and denied["Allow"] == "GET, HEAD"
        health_head = client.head("/health/live")
        assert health_head.status_code == 200 and health_head.content == b""
        assert health_head["Cache-Control"] == "no-store"
        document_head = client.head("/api/v1/openapi.json")
        assert document_head.status_code == 200 and document_head.content == b""
        assert document_head["Content-Length"] == published["Content-Length"]
        doc_denied = client.post("/api/v1/openapi.json")
        assert doc_denied.status_code == 405 and doc_denied["Allow"] == "GET, HEAD"
        declared = json.loads(published.content)
        schema = declared["paths"]["/api/v1/status"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        assert schema["type"] == "object"
        assert set(schema["required"]) == set(payload)
        assert schema["properties"]["data"]["properties"]["status"]["type"] == "string"
        assert resolve("/api/v1/status").func is status_capacity
        from django.test import override_settings
        bareconf = types.ModuleType("synthetic_joint_bare_urlconf")
        bareconf.urlpatterns = build_local_test_urlpatterns(root, plan, document, capacity)
        sys.modules["synthetic_joint_bare_urlconf"] = bareconf
        with override_settings(ROOT_URLCONF="synthetic_joint_bare_urlconf"):
            assert Client().get("/route-inconnue-xyz").status_code == 404
        assert all(guard.call_count == 0 for guard in
            (psycopg_guard, connection_guard, wrapper_guard, socket_guard, create_connection_guard))
        socket_patch.stop()
        create_patch.stop()
        from django.db import connections
        assert connections["default"].connection is None
        if mode == "cycle":
            from django.core.wsgi import get_wsgi_application
            from pixs.backend.local_test_composition import local_test_server
            application = get_wsgi_application()
            with local_test_server(application, host="127.0.0.1", port=0) as handle:
                address = "http://127.0.0.1:%d/" % (handle["port"],)
                with urllib.request.urlopen(address, timeout=5) as response:
                    assert response.status == 200
                    assert response.read() == index_bytes
                with urllib.request.urlopen(address + "health/live", timeout=5) as response:
                    assert response.status == 200 and response.read() == b""
                with urllib.request.urlopen(address + "api/v1/openapi.json", timeout=5) as response:
                    assert response.status == 200 and response.read().decode() == document
                with urllib.request.urlopen(address + "api/v1/status", timeout=5) as response:
                    assert response.status == 200
                    assert json.loads(response.read()) == {"data": {"status": "ok"}, "meta": {}, "links": {}}
                for asset in sorted((root / "assets").iterdir()):
                    with urllib.request.urlopen(address + "assets/" + asset.name, timeout=5) as response:
                        assert response.status == 200 and response.read() == asset.read_bytes()
                from urllib.error import HTTPError
                for path, status in (("api/v1/private", 403), ("absent-joint-xyz", 404)):
                    try:
                        with urllib.request.urlopen(address + path, timeout=5):
                            raise AssertionError("expected HTTP refusal")
                    except HTTPError as response:
                        assert response.code == status
                        response.close()
                assert private_calls == []

            assert handle["thread"].is_alive() is False
            assert handle["server"].fileno() == -1
            class SentinelError(Exception):
                pass
            try:
                with local_test_server(application, host="127.0.0.1", port=0) as handle:
                    raise SentinelError("sentinel-marker")
            except SentinelError as error:
                assert str(error) == "sentinel-marker"
            else:
                raise AssertionError("sentinel preserved")
            assert handle["thread"].is_alive() is False
            assert handle["server"].fileno() == -1
        assert all(guard.call_count == 0 for guard in (psycopg_guard, connection_guard, wrapper_guard))
    print(json.dumps({"integration": True}))
''')


class LocalTestCompositionIntegrationTests(unittest.TestCase):
    def test_real_joint_client_without_connections(self):
        result = _run(_CODE, _src(), _cache(), "client")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["integration"])

    def test_real_loopback_cycle_and_exception_cleanup(self):
        result = _run(_CODE, _src(), _cache(), "cycle")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["integration"])


if __name__ == "__main__":
    unittest.main()
