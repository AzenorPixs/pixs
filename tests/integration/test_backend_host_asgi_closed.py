"""Transport ASGI ferme, child-process Django isole ephemere.

Contexte et routes de test synthetiques, seul le handler transport Django
est reel via get_asgi_application et guards existants. Aucune qualification
Auth/P0. SECRET_KEY aleatoire ephemere du seul child, jamais affiche.
DB dummy, aucun Auth, reseau, port ou socket reel.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_THIS = Path(__file__)
_CHILD = "--child-closed"


if _CHILD in sys.argv:
    import asyncio
    import secrets
    import types
    from contextlib import AsyncExitStack

    sys.path.insert(0, str(_ROOT / "src"))
    from pixs.backend.host_asgi import HostAsgi, HostAsgiError
    from pixs.backend.liveness_view import liveness_view
    from pixs.backend.http_route_guard import RouteDeclaration, build_declared_urlpatterns
    from django.conf import settings as dj_settings

    assert dj_settings.configured is False
    _EPHEMERAL = secrets.token_hex(32)
    _calls: list = []

    def _private_view(request):
        _calls.append(1)
        from django.http import HttpResponse
        return HttpResponse(b"x", status=200, content_type="text/plain; charset=utf-8")

    _patterns = build_declared_urlpatterns(
        [
            RouteDeclaration("health/live", "host-health-live", liveness_view, True),
            RouteDeclaration("private-synth/", "private-synth", _private_view, False),
        ]
    )
    _urlconf = types.ModuleType("synthetic_host_closed_urlconf")
    _urlconf.urlpatterns = _patterns
    sys.modules["synthetic_host_closed_urlconf"] = _urlconf
    dj_settings.configure(
        SECRET_KEY=_EPHEMERAL,
        ALLOWED_HOSTS=["testserver"],
        ROOT_URLCONF="synthetic_host_closed_urlconf",
        INSTALLED_APPS=(),
        MIDDLEWARE=(),
        DATABASES={"default": {"ENGINE": "django.db.backends.dummy"}},
        LOGGING_CONFIG=None,
        DEBUG=False,
        USE_TZ=True,
    )
    import django

    django.setup()
    from django.core.asgi import get_asgi_application
    from django.core.handlers.asgi import ASGIHandler

    _HANDLER = get_asgi_application()
    assert isinstance(_HANDLER, ASGIHandler)

    def _scope(path: str, method: str) -> dict:
        return {
            "type": "http",
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [(b"host", b"testserver")],
        }

    async def _http(host: HostAsgi, path: str, method: str):
        from asgiref.testing import ApplicationCommunicator

        comm = ApplicationCommunicator(host, _scope(path, method))
        await comm.send_input({"type": "http.request", "body": b"", "more_body": False})
        start = await comm.receive_output(timeout=5)
        body = await comm.receive_output(timeout=5)
        await comm.wait(timeout=5)
        assert start["type"] == "http.response.start"
        assert body["type"] == "http.response.body"
        assert body.get("more_body", False) is False
        return start["status"], {key.lower(): value for key, value in start.get("headers", [])}, body.get("body", b"")

    class _Life:
        def __init__(self, host: HostAsgi, test: unittest.IsolatedAsyncioTestCase):
            self.host = host
            self.inbox: asyncio.Queue = asyncio.Queue()
            self.outbox: asyncio.Queue = asyncio.Queue()
            self.task: asyncio.Task | None = None
            self.test = test

        async def _receive(self) -> dict:
            return await self.inbox.get()

        async def _send(self, message: dict) -> None:
            await self.outbox.put(message)

        async def start(self):
            async def receive() -> dict:
                return await self._receive()

            async def send(message: dict) -> None:
                await self._send(message)

            self.task = asyncio.create_task(self.host({"type": "lifespan"}, receive, send))
            self.test.addAsyncCleanup(self._cleanup)
            await self.inbox.put({"type": "lifespan.startup"})
            first = await asyncio.wait_for(self.outbox.get(), timeout=5)
            return first

        async def put(self, message: dict) -> None:
            await self.inbox.put(message)

        async def next_output(self) -> dict:
            return await asyncio.wait_for(self.outbox.get(), timeout=5)

        async def _cleanup(self) -> None:
            task = self.task
            if task is not None and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    class _CtxOrder:
        def __init__(self, log: list, name: str):
            self._log = log
            self._name = name

        async def __aenter__(self):
            self._log.append("enter-" + self._name)
            return self

        async def __aexit__(self, *exc):
            self._log.append("exit-" + self._name)
            return False

    class _CtxStacked:
        def __init__(self, log: list):
            self._log = log
            self._stack = AsyncExitStack()

        async def __aenter__(self):
            try:
                await self._stack.enter_async_context(_CtxOrder(self._log, "A"))
                await self._stack.enter_async_context(_CtxOrder(self._log, "B"))
                return self
            except BaseException:
                await self._stack.aclose()
                raise

        async def __aexit__(self, *exc):
            await self._stack.aclose()
            return False

    class _CtxPartialHonest:
        def __init__(self, log: list):
            self._log = log
            self._stack = AsyncExitStack()

        async def __aenter__(self):
            from contextlib import asynccontextmanager

            @asynccontextmanager
            async def _res():
                self._log.append("r1-enter")
                try:
                    yield "r1"
                finally:
                    self._log.append("r1-exit")

            try:
                await self._stack.enter_async_context(_res())
                self._log.append("r2-attempt")
                raise RuntimeError("boom-partial-synthetic")
            except BaseException:
                await self._stack.aclose()
                raise

        async def __aexit__(self, *exc):
            await self._stack.aclose()
            return False

    class _CtxBadExit:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            raise RuntimeError("boom-exit-synthetic")

    class ClosedTransportTests(unittest.IsolatedAsyncioTestCase):
        async def test_closed_then_guarded_routes(self):
            host = HostAsgi(_HANDLER, lambda: _CtxOrder([], "solo"))
            self.assertEqual(host.phase, "NEW")
            status, headers, body = await _http(host, "/health/live", "GET")
            self.assertEqual(status, 503)
            self.assertEqual(body, b"")
            self.assertEqual(headers.get(b"cache-control"), b"no-store")
            life = _Life(host, self)
            first = await life.start()
            self.assertEqual(first["type"], "lifespan.startup.complete")
            self.assertEqual(host.phase, "STARTED")
            status, _, body = await _http(host, "/health/live", "GET")
            self.assertEqual((status, body), (200, b""))
            status, _, _ = await _http(host, "/health/live", "HEAD")
            self.assertEqual(status, 200)
            status, headers405, body405 = await _http(host, "/health/live", "POST")
            self.assertEqual(status, 405)
            self.assertEqual(body405, b"")
            self.assertEqual(headers405.get(b"allow"), b"GET, HEAD")
            _calls.clear()
            status, _, body403 = await _http(host, "/private-synth/", "GET")
            self.assertEqual(status, 403)
            self.assertIn("Route non publique.", body403.decode("utf-8"))
            self.assertEqual(_calls, [])
            status, _, body404 = await _http(host, "/absent-synth/", "GET")
            self.assertEqual(status, 404)
            text404 = body404.decode("utf-8")
            self.assertIn("Route inconnue.", text404)
            self.assertNotIn("/absent-synth/", text404)

        async def test_order_duplicate_stop_restart(self):
            log: list = []
            calls = {"n": 0}

            def factory():
                calls["n"] += 1
                return _CtxStacked(log)

            host = HostAsgi(_HANDLER, factory)
            life = _Life(host, self)
            first = await life.start()
            self.assertEqual(first["type"], "lifespan.startup.complete")
            self.assertEqual(log, ["enter-A", "enter-B"])
            await life.put({"type": "lifespan.startup"})
            dup = await life.next_output()
            self.assertEqual(dup["type"], "lifespan.startup.complete")
            self.assertEqual(calls["n"], 1)
            self.assertEqual(log, ["enter-A", "enter-B"])
            await life.put({"type": "lifespan.shutdown"})
            await asyncio.wait_for(life.task, timeout=5)
            self.assertEqual(log, ["enter-A", "enter-B", "exit-B", "exit-A"])
            self.assertEqual(host.phase, "STOPPED")
            status, _, _ = await _http(host, "/health/live", "GET")
            self.assertEqual(status, 503)
            life2 = _Life(host, self)
            again = await life2.start()
            self.assertEqual(again["type"], "lifespan.startup.failed")
            self.assertEqual(host.phase, "STOPPED")

        async def test_startup_partial_and_shutdown_failed(self):
            log: list = []
            bad = HostAsgi(_HANDLER, lambda: _CtxPartialHonest(log))
            life = _Life(bad, self)
            first = await life.start()
            self.assertEqual(first["type"], "lifespan.startup.failed")
            self.assertEqual(first["message"], "Transport ASGI invalide.")
            self.assertIn("r1-enter", log)
            self.assertIn("r1-exit", log)
            self.assertEqual(bad.phase, "FAILED")
            status, _, _ = await _http(bad, "/health/live", "GET")
            self.assertEqual(status, 503)
            failing = HostAsgi(_HANDLER, lambda: _CtxBadExit())
            life2 = _Life(failing, self)
            started = await life2.start()
            self.assertEqual(started["type"], "lifespan.startup.complete")
            await life2.put({"type": "lifespan.shutdown"})
            closed = await life2.next_output()
            self.assertEqual(closed["type"], "lifespan.shutdown.failed")
            self.assertEqual(failing.phase, "FAILED")

        async def test_cancel_send_receive_and_guards(self):
            log: list = []

            class _Ctx:
                async def __aenter__(self):
                    log.append("enter")
                    return self

                async def __aexit__(self, *exc):
                    log.append("exit")
                    return False

            host = HostAsgi(_HANDLER, lambda: _Ctx())
            inbox: asyncio.Queue = asyncio.Queue()
            outbox: asyncio.Queue = asyncio.Queue()

            async def receive() -> dict:
                return await inbox.get()

            async def send(message: dict) -> None:
                await outbox.put(message)

            task = asyncio.create_task(host({"type": "lifespan"}, receive, send))
            await inbox.put({"type": "lifespan.startup"})
            first = await asyncio.wait_for(outbox.get(), timeout=5)
            self.assertEqual(first["type"], "lifespan.startup.complete")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            else:
                self.fail("cancellation propagee")
            self.assertEqual(host.phase, "FAILED")
            self.assertIn("exit", log)
            failing_host = HostAsgi(_HANDLER, lambda: _Ctx())

            receives = 0

            async def receive_raise() -> dict:
                nonlocal receives
                receives += 1
                if receives == 1:
                    return {"type": "lifespan.startup"}
                raise ValueError("recv-synthetic")

            async def send_ok(message: dict) -> None:
                return None

            with self.assertRaises(ValueError):
                await failing_host({"type": "lifespan"}, receive_raise, send_ok)
            self.assertEqual(failing_host.phase, "FAILED")
            self.assertEqual(log[-2:], ["enter", "exit"])
            try:
                HostAsgi("not-a-handler", lambda: _Ctx())
            except HostAsgiError:
                pass
            else:
                self.fail("handler reel exige")
            try:
                HostAsgi(_HANDLER, "not-callable")
            except HostAsgiError:
                pass
            else:
                self.fail("fabrique exigee")
            no_cm = HostAsgi(_HANDLER, lambda: object())
            life_nc = _Life(no_cm, self)
            failed = await life_nc.start()
            self.assertEqual(failed["type"], "lifespan.startup.failed")
            concurrent = HostAsgi(_HANDLER, lambda: _Ctx())
            life_first = _Life(concurrent, self)
            ok_first = await life_first.start()
            self.assertEqual(ok_first["type"], "lifespan.startup.complete")
            with self.assertRaises(HostAsgiError):
                await concurrent({"type": "lifespan"}, life_first._receive, life_first._send)
            self.assertEqual(concurrent.phase, "STARTED")
            with self.assertRaises(HostAsgiError):
                await concurrent({"type": "unknown-synthetic"}, life_first._receive, life_first._send)
            async def other_loop_probe():
                async def receive_unreachable():
                    self.fail("Réception interdite dans une autre boucle")

                async def send_unreachable(_message):
                    self.fail("Envoi interdit dans une autre boucle")

                await concurrent({"type": "http"}, receive_unreachable, send_unreachable)

            with self.assertRaises(HostAsgiError):
                await asyncio.wait_for(
                    asyncio.to_thread(lambda: asyncio.run(other_loop_probe())), timeout=5
                )


        async def test_stopping_closes_admission_before_cleanup(self):
            from contextlib import asynccontextmanager
            stopping, release = asyncio.Event(), asyncio.Event()
            log = []

            @asynccontextmanager
            async def resources():
                log.append("enter")
                try:
                    yield
                finally:
                    stopping.set()
                    await release.wait()
                    log.append("exit")

            host = HostAsgi(_HANDLER, resources)
            life = _Life(host, self)
            self.assertEqual((await life.start())["type"], "lifespan.startup.complete")
            self.addCleanup(release.set)
            await life.put({"type": "lifespan.shutdown"})
            await asyncio.wait_for(stopping.wait(), timeout=5)
            self.assertEqual(host.phase, "STOPPING")
            status, _, body = await _http(host, "/health/live", "GET")
            self.assertEqual((status, body), (503, b""))
            release.set()
            self.assertEqual((await life.next_output())["type"], "lifespan.shutdown.complete")
            await asyncio.wait_for(life.task, timeout=5)
            self.assertEqual(log, ["enter", "exit"])

        async def test_cancel_during_startup_cleans_partial_context(self):
            from contextlib import asynccontextmanager, suppress
            entered, block = asyncio.Event(), asyncio.Event()
            log = []

            @asynccontextmanager
            async def resources():
                async with AsyncExitStack() as partial:
                    await partial.enter_async_context(_CtxOrder(log, "A"))
                    entered.set()
                    await block.wait()
                    yield

            host = HostAsgi(_HANDLER, resources)
            life = _Life(host, self)
            starter = asyncio.create_task(life.start())
            try:
                await asyncio.wait_for(entered.wait(), timeout=5)
                life.task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await life.task
            finally:
                starter.cancel()
                with suppress(asyncio.CancelledError):
                    await starter
            self.assertEqual(host.phase, "FAILED")
            self.assertEqual(log, ["enter-A", "exit-A"])
            self.assertEqual((await _http(host, "/health/live", "GET"))[0], 503)

        async def test_send_error_closes_entered_context(self):
            log = []
            host = HostAsgi(_HANDLER, lambda: _CtxOrder(log, "A"))

            async def receive():
                return {"type": "lifespan.startup"}

            async def send(_message):
                raise ValueError("send-synthetic")

            with self.assertRaisesRegex(ValueError, "send-synthetic"):
                await host({"type": "lifespan"}, receive, send)
            self.assertEqual(host.phase, "FAILED")
            self.assertEqual(log, ["enter-A", "exit-A"])

        async def test_unknown_lifespan_message_closes_entered_context(self):
            log = []
            host = HostAsgi(_HANDLER, lambda: _CtxOrder(log, "A"))
            life = _Life(host, self)
            self.assertEqual((await life.start())["type"], "lifespan.startup.complete")
            await life.put({"type": "unknown-synthetic"})
            with self.assertRaises(HostAsgiError):
                await asyncio.wait_for(life.task, timeout=5)
            life.task = None
            self.assertEqual(host.phase, "FAILED")
            self.assertEqual(log, ["enter-A", "exit-A"])
            self.assertEqual((await _http(host, "/health/live", "GET"))[0], 503)

    _suite = unittest.defaultTestLoader.loadTestsFromTestCase(ClosedTransportTests)
    _runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=1)
    _result = _runner.run(_suite)
    _ok = _result.wasSuccessful()
    sys.stdout.write(json.dumps({"closed": bool(_ok), "tests": _result.testsRun}) + "\n")
    sys.stdout.flush()
    sys.exit(0 if _ok else 1)


class BackendHostAsgiClosedParentTests(unittest.TestCase):
    def test_closed_transport_in_isolated_child(self):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(
            [sys.executable, "-B", str(_THIS), _CHILD],
            timeout=120,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(_ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(payload["closed"])
        self.assertEqual(payload["tests"], 8)
        print(json.dumps({"child_tests": payload["tests"], "child_ok": payload["closed"]}))


if __name__ == "__main__":
    unittest.main()
