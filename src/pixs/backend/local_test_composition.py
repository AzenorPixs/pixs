"""Joint TEST HTTP composition, real patterns plus loopback lifecycle.

Contract: `build_local_test_urlpatterns(dist_root, plan, document,
capacity, *, private_routes=(), unknown_ui_route=None)` builds real
Django urlpatterns through the guard from proven handlers, declaring
explicit TEST literal routes (health, shell root and assets, versioned
document, caller capacity, explicit privates, optional unknown-UI).
The factory intentionally performs the bounded `dist` reads of
`build_shell_views`; only the module import is pure (no Django import
or filesystem read at import, no bind, DB, socket or config in the
factory). `local_test_server(application, *, host, port)` serves one
explicit caller WSGI application on loopback with observable cleanup.
TEST composition only: no P0 activation, no global compose, no
readiness, no production claim. No production URL is distributed by
this module; TEST routes are documented explicit TEST declarations.

Limits: no `settings.configure`, `django.setup`, server bind, DB,
socket or secret at import or in the factory; the server binds only
inside `local_test_server`, on `127.0.0.1` alone. Capabilities out of
scope are declared NOT SUPPORTED by this TEST composition, never as
machine absences; caller TEST handlers are the caller responsibility.
"""

from __future__ import annotations

import json
from contextlib import contextmanager

from pixs.backend.api import api_major_prefix
from pixs.backend.http_route_guard import RouteDeclaration, build_declared_urlpatterns
from pixs.backend.liveness_view import liveness_view
from pixs.backend.openapi_document_view import build_openapi_view
from pixs.backend.shell_adapter import build_shell_views

__all__ = [
    "UNSUPPORTED_TEST_CAPABILITIES",
    "LocalTestCompositionError",
    "build_local_test_urlpatterns",
    "local_test_server",
]

_ERROR = "Invalid local test composition."
UNSUPPORTED_TEST_CAPABILITIES = (
    "kernel-activation",
    "core-activation",
    "p0",
    "readiness",
    "worker",
    "scheduler",
    "pg-connection",
)
_HEALTH_PATH = "health/live"


class LocalTestCompositionError(ValueError):
    """Stable composition error, without raw value echo."""

    def __init__(self, message: str = _ERROR) -> None:
        super().__init__(message)


def _invalid_composition() -> LocalTestCompositionError:
    return LocalTestCompositionError(_ERROR)


def _require_capacity(capacity: object, document_paths: object, prefix: str) -> str:
    if type(capacity) is not RouteDeclaration:
        raise _invalid_composition() from None
    if capacity.public is not True:
        raise _invalid_composition() from None
    if type(capacity.path) is not str or capacity.path == "":
        raise _invalid_composition() from None
    canonical = "/" + capacity.path
    try:
        known = canonical in document_paths
        under_prefix = canonical.startswith(prefix + "/")
    except Exception:
        raise _invalid_composition() from None
    if known is not True or under_prefix is not True:
        raise _invalid_composition() from None
    return canonical


def _require_private_routes(private_routes: object) -> tuple:
    if type(private_routes) is not tuple:
        raise _invalid_composition() from None
    for route in private_routes:
        if type(route) is not RouteDeclaration:
            raise _invalid_composition() from None
        if route.public is not False:
            raise _invalid_composition() from None
    return private_routes


def _document_paths(document: object) -> object:
    try:
        parsed = json.loads(document)
    except Exception:
        raise _invalid_composition() from None
    try:
        paths = parsed["paths"]
    except Exception:
        raise _invalid_composition() from None
    if type(paths) is not dict:
        raise _invalid_composition() from None
    return paths


def build_local_test_urlpatterns(dist_root: object, plan: object, document: object, capacity: object, *, private_routes: object = (), unknown_ui_route: object = None) -> list:
    """Build the joint TEST urlpatterns through the guard."""
    if type(document) is not str or document == "":
        raise _invalid_composition() from None
    try:
        prefix = api_major_prefix(plan)
    except Exception:
        raise _invalid_composition() from None
    try:
        shell_views = build_shell_views(dist_root)
        document_view = build_openapi_view(plan, document)
    except LocalTestCompositionError:
        raise
    except Exception:
        raise _invalid_composition() from None
    document_paths = _document_paths(document)
    _require_capacity(capacity, document_paths, prefix)
    routes = _require_private_routes(private_routes)
    if unknown_ui_route is not None and type(unknown_ui_route) is not str:
        raise _invalid_composition() from None
    if type(shell_views) is not dict or "index.html" not in shell_views:
        raise _invalid_composition() from None
    declarations = [
        RouteDeclaration(_HEALTH_PATH, "test-health-live", liveness_view, True),
        RouteDeclaration("", "test-shell-root", shell_views["index.html"], True),
    ]
    for key in sorted(shell_views):
        if key != "index.html":
            declarations.append(RouteDeclaration(key, "test-shell-" + key.replace("/", "-"), shell_views[key], True))
    declarations.append(RouteDeclaration(prefix[1:] + "/openapi.json", "test-api-document", document_view, True))
    declarations.append(capacity)
    declarations.extend(routes)
    if unknown_ui_route is not None:
        declarations.append(RouteDeclaration(unknown_ui_route, "test-unknown-ui", shell_views["index.html"], True))
    try:
        return build_declared_urlpatterns(declarations)
    except LocalTestCompositionError:
        raise
    except Exception:
        raise _invalid_composition() from None


@contextmanager
def local_test_server(application: object, *, host: object, port: object) -> object:
    """Serve a finite TEST WSGI application and close its owned resources.

    shutdown waits for the current synchronous request to finish; a caller
    handler that never returns cannot be cancelled by this helper. Tests
    run their finite handlers in a subprocess with an explicit timeout.
    """
    if not callable(application):
        raise _invalid_composition() from None
    if type(host) is not str or host != "127.0.0.1":
        raise _invalid_composition() from None
    if type(port) is bool or type(port) is not int or port < 0 or port > 65535:
        raise _invalid_composition() from None
    from wsgiref.simple_server import make_server
    import threading
    try:
        server = make_server(host, port, application)
    except Exception:
        raise _invalid_composition() from None
    try:
        thread = threading.Thread(
            target=server.serve_forever,
            kwargs={"poll_interval": 0.05},
            daemon=False,
        )
        thread.start()
    except Exception:
        try:
            server.server_close()
        finally:
            raise _invalid_composition() from None
    try:
        yield {"server": server, "thread": thread,
               "host": host, "port": server.server_address[1]}
    finally:
        cleanup_ok = True
        try:
            server.shutdown()
        except Exception:
            cleanup_ok = False
        finally:
            try:
                thread.join(timeout=10)
            except Exception:
                cleanup_ok = False
            finally:
                try:
                    server.server_close()
                except Exception:
                    cleanup_ok = False
        if not cleanup_ok or thread.is_alive() or server.fileno() != -1:
            raise _invalid_composition() from None
