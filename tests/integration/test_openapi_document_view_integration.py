"""Integration tests OpenAPI document view on true Client via guard."""

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
        import json as json_module
        from pixs.backend.api import ApiContractPlan, build_success_response
        from pixs.kernel.contracts import ContractCategory, ContractDescriptor
        from pixs.backend.openapi_document_view import build_openapi_view
        from pixs.backend.http_route_guard import RouteDeclaration
        from pixs.backend.http_route_guard import build_declared_urlpatterns
        status_schema = {"type": "object",
            "properties": {"data": {"type": "object",
                "properties": {"status": {"type": "string"}},
                "required": ["status"]},
                "meta": {"type": "object"}, "links": {"type": "object"}},
            "required": ["data", "meta", "links"]}
        status_media = {"application/json": {"schema": status_schema}}
        status_operation = {"operationId": "getStatus",
            "responses": {"200": {"description": "Status.", "content": status_media}}}
        document_dict = {"openapi": "3.1.0",
            "info": {"title": "Synthetic Status", "version": "1.0.0"},
            "security": [],
            "paths": {
                "/api/v1/status": {"get": status_operation},
                "/api/v1/openapi.json": {"get": {"responses": {"200": {"description": "Document."}}}},
            }}
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
        document = json_module.dumps(document_dict)
        first = build_openapi_view(plan, document)
        calls = []
        def status_capacity(request):
            calls.append(request.method)
            return build_success_response({"status": "ok"}, meta={}, links={})
        patterns = build_declared_urlpatterns([
            RouteDeclaration("api/v1/openapi.json", "api-document", first, True),
            RouteDeclaration("api/v1/status", "api-status", status_capacity, True),
            RouteDeclaration("api/v1/private", "api-private", status_capacity, False),
        ])
        assert len(patterns) == 4
        urlconf = types.ModuleType("synthetic_api_urlconf")
        urlconf.urlpatterns = patterns
        sys.modules["synthetic_api_urlconf"] = urlconf
        settings.configure(
            DEFAULT_CHARSET="utf-8",
            DEBUG=False,
            ROOT_URLCONF="synthetic_api_urlconf",
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
        assert resolve("/api/v1/openapi.json").func is first
        assert resolve("/api/v1/status").func is status_capacity
        client = Client()
        published = client.get("/api/v1/openapi.json")
        assert published.status_code == 200
        assert published.content.decode("utf-8") == document
        assert published["Content-Type"] == "application/json; charset=utf-8"
        assert published["Cache-Control"] == "no-store"
        head = client.head("/api/v1/openapi.json")
        assert head.status_code == 200 and head.content == b""
        assert head["Content-Length"] == published["Content-Length"]
        denied = client.post("/api/v1/openapi.json")
        assert denied.status_code == 405 and denied["Allow"] == "GET, HEAD"
        capacity = client.get("/api/v1/status")
        assert capacity.status_code == 200
        payload = json_module.loads(capacity.content.decode("utf-8"))
        assert payload == {"data": {"status": "ok"}, "meta": {}, "links": {}}
        assert type(payload["data"]["status"]) is str
        declared = json_module.loads(published.content.decode("utf-8"))
        assert declared["info"]["version"] == plan.contract.version
        assert set(declared["paths"]) == {"/api/v1/status", "/api/v1/openapi.json"}
        returned_schema = declared["paths"]["/api/v1/status"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        assert returned_schema["type"] == "object"
        assert set(returned_schema["required"]) == set(payload)
        for field in ("data", "meta", "links"):
            assert returned_schema["properties"][field]["type"] == "object" and type(payload[field]) is dict
        assert returned_schema["properties"]["data"]["properties"]["status"]["type"] == "string"
        assert set(returned_schema["properties"]["data"]["required"]) == set(payload["data"])
        for method in ("get", "post", "head"):
            assert getattr(client, method)("/api/v1/private").status_code == 403
        assert calls == ["GET"]
        other_major = client.get("/api/v2/openapi.json")
        assert other_major.status_code == 404
        assert other_major.content.decode("utf-8") == "Route inconnue."
        assert psycopg_guard.call_count == 0
        assert connection_guard.call_count == 0
        assert wrapper_guard.call_count == 0
        assert socket_guard.call_count == 0
        assert create_connection_guard.call_count == 0
        from django.db import connections
        assert connections["default"].connection is None
    print(json.dumps({"integration": True}))
''')


class OpenapiDocumentViewIntegrationTests(unittest.TestCase):
    def test_real_document_cycle_without_connections(self):
        result = _run(_CODE, _src())
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["integration"])


if __name__ == "__main__":
    unittest.main()
