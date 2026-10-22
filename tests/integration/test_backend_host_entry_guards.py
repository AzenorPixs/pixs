"""Gardes d'entrée C07 et frontière HTTP, enfants isolés, aucun P0/C01 natif.

(A) gardes build_installer_host, Django NON configuré, plan réel + preuves
doubles. (B) frontière HTTP réelle ASGIHandler, config Django de RECETTE
seulement. Aucun réseau/base/unité systemd. Enfants JSON filtré sans secret.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_THIS = Path(__file__)
_CHILD_GUARDS = "--child-guards"
_CHILD_BOUNDARY = "--child-boundary"


class SafeResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.details = []

    def _record(self, test, error):
        import traceback
        self.details.append({"test": test.id(), "type": error[0].__name__,
            "frames": [{"file": Path(frame.filename).name, "line": frame.lineno, "func": frame.name}
                       for frame in traceback.extract_tb(error[2])]})

    def addError(self, test, error):
        self._record(test, error)
        super().addError(test, error)

    def addFailure(self, test, error):
        self._record(test, error)
        super().addFailure(test, error)


def run_child(case, family, facts):
    result = SafeResult()
    unittest.defaultTestLoader.loadTestsFromTestCase(case).run(result)
    payload = {"family": family, "tests": result.testsRun,
        "passed": result.testsRun - len(result.errors) - len(result.failures),
        "failed": result.details, "facts": facts()}
    print(json.dumps(payload, ensure_ascii=False), flush=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if _CHILD_GUARDS in sys.argv:
    from unittest import mock
    sys.path.insert(0, str(_ROOT))
    sys.path.insert(0, str(_ROOT / "src"))
    from pixs.backend.bootstrap_policy import PolicySource
    from pixs.backend.host_entry import InstallerHostError, build_installer_host
    from pixs.backend.host_plan import prepare_host_plan
    from pixs.backend.http_route_guard import HttpRouteGuardError, RouteDeclaration
    from pixs.backend.liveness_view import liveness_view
    from pixs.backend.settings import build_settings_template
    from pixs.backend.startup_mode import StartupMode
    from pixs.kernel.config.resolution import SecretReference
    from tests.conformity_fixtures import synthetic_attestations
    from tests.unit.test_backend_host_plan import texts as base_texts
    from django.apps import apps as _apps
    from django.conf import settings as _settings

    _REQUIRED = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt")

    class ProofPortDouble:
        def __init__(self, source):
            self.source = tuple(source)
        def authenticate_and_read(self, manifests):
            return synthetic_attestations(self.source)

    def _plan():
        source = base_texts()
        return prepare_host_plan(manifest_texts=source, official_ids=_REQUIRED,
                                 required_ids=_REQUIRED, attestation_port=ProofPortDouble(source))

    def _template(profile="web"):
        return build_settings_template(
            profile=profile,
            database={"name": "pixs", "user": "pixs", "host": "localhost", "port": 5432},
            allowed_hosts=["testserver"],
            secret_key_ref=SecretReference("pixs.auth", "django-secret", "systemd"),
            database_password_ref=SecretReference("pixs.auth", "db-password", "systemd"))

    def _source():
        return PolicySource(path=str(_ROOT / "tests" / "runtime" / "c07-entry-unused.toml"), owner_uid=0,
                            policy_id="synth", max_policy_bytes=4096)

    def _liveness():
        return RouteDeclaration("health/live", "host-health-live", liveness_view, True)

    def _dummy(request):
        return None

    def _private(name="private-synth"):
        return RouteDeclaration("private-synth/", name, _dummy, False)

    class BuildGuardsTests(unittest.TestCase):
        def assertUnconfigured(self):
            self.assertFalse(_settings.configured)
            self.assertFalse(_apps.ready)
        def test_normal_mode_refused_before_c01(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.NORMAL, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_string_mode_refused_before_c01(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), "INSTALLER", "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_worker_profile_refused_before_c01(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template("worker"), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_scheduler_profile_refused_before_c01(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template("scheduler"), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_bad_template_type_refused(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host({}, _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_bad_source_type_refused(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), "src", StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_bad_plan_type_refused(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", "plan", lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_empty_purpose_refused(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_async_factory_refused(self):
            async def _async_factory(plan):
                return ()
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), _async_factory, _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_async_callable_object_refused(self):
            class AsyncFactory:
                async def __call__(self, plan):
                    return ()
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), AsyncFactory(), _liveness())
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_public_non_liveness_refused(self):
            other = RouteDeclaration("other/", "other", _dummy, True)
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), other)
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_private_marked_public_refused(self):
            bad = RouteDeclaration("private-synth/", "private-synth", _dummy, True)
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness(), (bad,))
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_duplicate_path_refused(self):
            dup = RouteDeclaration("health/live", "dup", _dummy, False)
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(HttpRouteGuardError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness(), (dup,))
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_bad_path_refused(self):
            bad = RouteDeclaration("/bad", "bad", _dummy, False)
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaises(HttpRouteGuardError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness(), (bad,))
                self.assertEqual(mocked.call_count, 0)
            self.assertUnconfigured()
        def test_doubled_producer_dict_refused(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings", return_value={}) as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 1)
            self.assertUnconfigured()
        def test_doubled_producer_object_refused(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings", return_value=object()) as mocked:
                with self.assertRaises(InstallerHostError):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
                self.assertEqual(mocked.call_count, 1)
            self.assertUnconfigured()
        def test_producer_unexpected_error_propagates(self):
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings", side_effect=RuntimeError("Echec explicite de recette")):
                with self.assertRaisesRegex(RuntimeError, "Echec explicite"):
                    build_installer_host(_template(), _source(), StartupMode.INSTALLER, "p", _plan(), lambda plan: (), _liveness())
            self.assertUnconfigured()

    run_child(BuildGuardsTests, "construction", lambda: {"django_unconfigured": not _settings.configured and not _apps.ready})


if _CHILD_BOUNDARY in sys.argv:
    import secrets
    import types
    sys.path.insert(0, str(_ROOT))
    sys.path.insert(0, str(_ROOT / "src"))
    from pixs.backend.host_entry import HostBoundaryMiddleware
    from pixs.backend.http_route_guard import RouteDeclaration, build_declared_urlpatterns
    from pixs.backend.liveness_view import liveness_view
    from django.conf import settings as _dj
    assert _dj.configured is False
    _EPHEMERAL = secrets.token_hex(32)
    _calls = []
    def _private_view(request):
        _calls.append(1)
        from django.http import HttpResponse
        return HttpResponse(b"x", status=200, content_type="text/plain; charset=utf-8")
    _patterns = build_declared_urlpatterns([RouteDeclaration("health/live", "host-health-live", liveness_view, True),
                                            RouteDeclaration("private-synth/", "private-synth", _private_view, False)])
    _urlconf = types.ModuleType("synthetic_entry_boundary_urlconf")
    _urlconf.urlpatterns = _patterns
    _dj.configure(SECRET_KEY=_EPHEMERAL, ALLOWED_HOSTS=["testserver"],
                  ROOT_URLCONF=_urlconf, INSTALLED_APPS=(),
                  MIDDLEWARE=["pixs.backend.host_entry.HostBoundaryMiddleware",
                              "django.middleware.security.SecurityMiddleware"],
                  DATABASES={"default": {"ENGINE": "django.db.backends.dummy"}},
                  LOGGING_CONFIG=None, DEBUG=False, USE_TZ=True,
                  USE_X_FORWARDED_HOST=False, SECURE_PROXY_SSL_HEADER=None)
    import django
    django.setup()
    import asyncio
    from django.core.handlers.asgi import ASGIHandler
    _HANDLER = ASGIHandler()
    assert isinstance(_HANDLER, ASGIHandler)

    def _scope(path, method, headers=((b"host", b"testserver"),)):
        return {"type": "http", "asgi": {"version": "3.0"}, "server": ("testserver", 80),
                "client": ("127.0.0.1", 1234), "http_version": "1.1", "method": method, "scheme": "http",
                "path": path, "raw_path": path.encode(), "query_string": b"", "headers": list(headers)}

    async def _http(app, path, method, headers=((b"host", b"testserver"),)):
        from asgiref.testing import ApplicationCommunicator
        comm = ApplicationCommunicator(app, _scope(path, method, headers))
        await comm.send_input({"type": "http.request", "body": b"", "more_body": False})
        start = await comm.receive_output(timeout=5)
        body = await comm.receive_output(timeout=5)
        await comm.wait(timeout=5)
        return start["status"], {k.lower(): v for k, v in start.get("headers", [])}, body.get("body", b"")

    class BoundaryTests(unittest.IsolatedAsyncioTestCase):
        async def test_host_valid_and_invalid(self):
            s, _, _ = await _http(_HANDLER, "/health/live", "GET")
            self.assertEqual(s, 200)
            s, _, _ = await _http(_HANDLER, "/health/live", "GET", ((b"host", b"evil.example"),))
            self.assertEqual(s, 400)
        async def test_forwarded_headers_ignored(self):
            s, _, _ = await _http(_HANDLER, "/health/live", "GET",
                                  ((b"host", b"testserver"), (b"x-forwarded-host", b"evil.example"),
                                   (b"x-forwarded-proto", b"https")))
            self.assertEqual(s, 200)
            s, _, _ = await _http(_HANDLER, "/health/live", "GET",
                                  ((b"host", b"evil.example"), (b"x-forwarded-host", b"testserver")))
            self.assertEqual(s, 400)
        async def test_origin_accepted_and_refused(self):
            good = [(b"host", b"testserver"), (b"origin", b"http://testserver")]
            s, _, _ = await _http(_HANDLER, "/health/live", "GET", good)
            self.assertEqual(s, 200)
            s, _, _ = await _http(_HANDLER, "/health/live", "GET",
                                  ((b"host", b"testserver"), (b"origin", b"http://testserver:80")))
            self.assertEqual(s, 200)
            for origin in [b"https://evil.example", b"null", b"", b"http://user@testserver",
                            b"http://testserver?x=1", b"http://testserver#frag",
                            b"https://testserver", b"http://testserver?", b"http://testserver#",
                            b"http://testserver:0", b"http://testserver:65536",
                            b"http://testserver:8001"]:
                s, _, _ = await _http(_HANDLER, "/health/live", "GET",
                                      ((b"host", b"testserver"), (b"origin", origin)))
                self.assertEqual(s, 403)
        async def test_methods_liveness(self):
            s, _, b = await _http(_HANDLER, "/health/live", "GET")
            self.assertEqual((s, b), (200, b""))
            s, _, _ = await _http(_HANDLER, "/health/live", "HEAD")
            self.assertEqual(s, 200)
            s, h, b = await _http(_HANDLER, "/health/live", "POST")
            self.assertEqual(s, 405)
            self.assertEqual(h.get(b"allow"), b"GET, HEAD")
            self.assertEqual(b, b"")
        async def test_private403_never_calls_handler(self):
            _calls.clear()
            s, _, _ = await _http(_HANDLER, "/private-synth/", "GET")
            self.assertEqual(s, 403)
            self.assertEqual(_calls, [])
        async def test_unknown404_no_html(self):
            s, _, b = await _http(_HANDLER, "/absent-synth/", "GET")
            self.assertEqual(s, 404)
            text = b.decode("utf-8")
            self.assertIn("Route inconnue.", text)
            self.assertNotIn("/absent-synth/", text)
            self.assertNotIn("<html", text.lower())
        async def test_factory_when_configured_refuses_before_c01(self):
            from unittest import mock
            from pixs.backend.host_entry import InstallerHostError, build_installer_host
            from pixs.backend.bootstrap_policy import PolicySource
            from pixs.backend.settings import build_settings_template
            from pixs.backend.startup_mode import StartupMode
            from pixs.backend.host_plan import prepare_host_plan
            from pixs.kernel.config.resolution import SecretReference
            from tests.unit.test_backend_host_plan import texts, SyntheticProofPort
            source_texts = texts()
            required = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt")
            plan = prepare_host_plan(manifest_texts=source_texts, official_ids=required,
                required_ids=required, attestation_port=SyntheticProofPort(source_texts))
            template = build_settings_template(profile="web",
                database={"name": "fixture", "user": "fixture", "host": "localhost", "port": 5432},
                allowed_hosts=["testserver"],
                secret_key_ref=SecretReference("pixs.backend", "key", "systemd:key"),
                database_password_ref=SecretReference("pixs.backend", "password", "systemd:password"))
            source = PolicySource(str(_ROOT / "tests" / "runtime" / "c07-entry-unused.toml"), 0, "fixture", 4096)
            route = RouteDeclaration("health/live", "fixture-live", liveness_view, True)
            with mock.patch("pixs.backend.host_entry.resolve_runtime_settings") as mocked:
                with self.assertRaisesRegex(InstallerHostError, "Django déjà configuré"):
                    build_installer_host(template, source, StartupMode.INSTALLER, "fixture", plan,
                                         lambda selected: (), route)
                mocked.assert_not_called()
        async def test_boundary_middleware_flags(self):
            self.assertTrue(HostBoundaryMiddleware.sync_capable)
            self.assertFalse(HostBoundaryMiddleware.async_capable)

    from django.db import connections
    run_child(BoundaryTests, "HTTP", lambda: {"dummy_db_closed": connections["default"].connection is None})


class BackendHostEntryGuardsParentTests(unittest.TestCase):
    def test_guards_in_isolated_child(self):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, "-B", str(_THIS), _CHILD_GUARDS],
                                timeout=120, capture_output=True, text=True, env=env, cwd=str(_ROOT))
        self.assertTrue(bool(result.stdout.strip()), "Réponse JSON filtrée absente")
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(result.returncode, 0, json.dumps(payload, ensure_ascii=False))
        self.assertEqual(payload["tests"], 17)
        self.assertEqual(payload["passed"], 17)
        print(json.dumps(payload, ensure_ascii=False))


class BackendHostEntryBoundaryParentTests(unittest.TestCase):
    def test_boundary_in_isolated_child(self):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, "-B", str(_THIS), _CHILD_BOUNDARY],
                                timeout=120, capture_output=True, text=True, env=env, cwd=str(_ROOT))
        self.assertTrue(bool(result.stdout.strip()), "Réponse JSON filtrée absente")
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(result.returncode, 0, json.dumps(payload, ensure_ascii=False))
        self.assertEqual(payload["tests"], 8)
        self.assertEqual(payload["passed"], 8)
        print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
