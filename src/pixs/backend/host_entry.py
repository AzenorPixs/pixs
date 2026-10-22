"""Entrée hôte C07 INSTALLER : Django configuré une fois, runtime gardé.

Fabrique ``build_installer_host`` : valide entrées/route/rôle avant toute
résolution, exige ``StartupMode.INSTALLER`` réel et profil ``web``.
``worker`` / ``scheduler`` et ``NORMAL`` refusés avant effet. Source C01
INSTALLER actuelle non modifiée.

Appelle réellement ``resolve_runtime_settings`` puis exige
``RuntimeDjangoSettings`` exact et ``as_dict`` une fois. Django configuré
une fois seulement : ``settings.configured`` ou ``apps.ready`` refuse avant
consommation. Payload conservé, ``DEBUG False``, ``ALLOWED_HOSTS`` conservés.
``INSTALLED_APPS`` explicite = ``DJANGO_REQUIRED_APPS`` C03 +
``PixsCoreConfig`` public. Deux alias ``default`` / ``peer`` issus de la même
configuration, copies fraîches, sans option/secret depuis une requête.
``ROOT_URLCONF`` local, ``urlpatterns`` via ``build_declared_urlpatterns`` :
seul public autorisé = ``liveness_route`` dont handler est exactement
``liveness_view`` ; toute autre route fournie doit être ``public=False``.
Aucune écoute réseau, serveur, installation, migration ou unité systemd
lancée ici. Middleware sécurité explicite, proxy headers non fiables ignorés,
aucune session/cookie métier.

``InstallerHost`` opaque et ``repr`` sans réglages, callable déléguant au
vrai ``HostAsgi``. Contexte async sous ``ThreadSensitiveContext`` :
``adapters_factory`` synchrone trusted appelée en thread sensible après
``django.setup``, puis vrai ``host_runtime`` ; contexte conservé actif
uniquement pendant la vie, propriété ``context`` refuse hors ``STARTED``.
Aucun port/callback depuis manifest ou HTTP. Aucun ready global, P0, paquet,
ressources ou drain qualifié.

Note : la recette positive native C01 peut nécessiter un banc hôte distinct.
Ce module ne lance rien et ne forge aucun objet pour simuler cette preuve.
"""
from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass
from types import ModuleType
import inspect
from urllib.parse import urlsplit

from pixs.backend.host_plan import PreparedHostPlan
from pixs.backend.host_runtime import host_runtime
from pixs.backend.http_route_guard import RouteDeclaration, build_declared_urlpatterns
from pixs.backend.liveness_view import liveness_view
from pixs.backend.runtime_resolve import RuntimeDjangoSettings, resolve_runtime_settings
from pixs.backend.settings import SettingsTemplate
from pixs.backend.bootstrap_policy import PolicySource
from pixs.backend.startup_mode import StartupMode

__all__ = ["HostBoundaryMiddleware", "InstallerHost", "InstallerHostError", "build_installer_host"]

_ENTRY_KEY = object()
_REQUIRED_APPS_SUFFIX = "pixs.backend.apps.PixsCoreConfig"
_SECURITY_MIDDLEWARE = (
    "pixs.backend.host_entry.HostBoundaryMiddleware",
    "django.middleware.security.SecurityMiddleware",
)


class HostBoundaryMiddleware:
    """Valide l'hôte Django et une origine éventuelle sans faire confiance au proxy."""
    sync_capable = True
    async_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def _reject(status):
        from django.http import HttpResponse
        response = HttpResponse(b"", status=status, content_type="text/plain; charset=utf-8")
        response["Cache-Control"] = "no-store"
        return response

    def __call__(self, request):
        from django.core.exceptions import DisallowedHost
        try:
            host = request.get_host()
        except DisallowedHost:
            return self._reject(400)
        origin = request.headers.get("Origin")
        if origin is not None:
            if (not origin or origin != origin.strip()
                    or "?" in origin or "#" in origin
                    or any(ord(char) <= 32 or ord(char) == 127 for char in origin)):
                return self._reject(403)
            try:
                candidate = urlsplit(origin)
                own = urlsplit(request.scheme + "://" + host)
                if (candidate.scheme not in ("http", "https") or candidate.scheme != own.scheme
                        or candidate.username is not None or candidate.password is not None
                        or candidate.path or candidate.query or candidate.fragment
                        or not candidate.hostname or candidate.hostname != own.hostname
                        or (candidate.port if candidate.port is not None else (443 if candidate.scheme == "https" else 80))
                           != (own.port if own.port is not None else (443 if own.scheme == "https" else 80))):
                    return self._reject(403)
            except ValueError:
                return self._reject(403)
        return self.get_response(request)


class InstallerHostError(ValueError):
    def __init__(self, stage):
        super().__init__("Hôte installateur refusé à la phase " + stage + ".")
        self.stage = stage


def _exact(value, kind, stage):
    if type(value) is not kind:
        raise InstallerHostError(stage)
    return value


def _non_empty_str(value, stage):
    if type(value) is not str or not value:
        raise InstallerHostError(stage)
    return value


@dataclass(frozen=True, slots=True, repr=False, init=False)
class InstallerHost:
    _asgi: object
    _holder: object

    def __init__(self, key, *, asgi, holder):
        if key is not _ENTRY_KEY:
            raise InstallerHostError("construction")
        object.__setattr__(self, "_asgi", asgi)
        object.__setattr__(self, "_holder", holder)

    def __repr__(self):
        return "InstallerHost(<confidentiel>)"

    @property
    def phase(self):
        return self._asgi.phase

    @property
    def context(self):
        if self._asgi.phase != "STARTED":
            raise InstallerHostError("contexte hors phase STARTED")
        try:
            return self._holder["current"]
        except KeyError:
            raise InstallerHostError("contexte indisponible") from None

    async def __call__(self, scope, receive, send):
        await self._asgi(scope, receive, send)


def build_installer_host(template, source, mode, purpose, plan, adapters_factory,
                         liveness_route, private_routes=()):
    """Construit l'hôte INSTALLER web ; refuse fermé avant tout effet externe."""
    _exact(template, SettingsTemplate, "gabarit")
    _exact(source, PolicySource, "source")
    if mode is not StartupMode.INSTALLER:
        raise InstallerHostError("mode INSTALLER exigé")
    _non_empty_str(purpose, "finalité")
    _exact(plan, PreparedHostPlan, "plan")
    if (not callable(adapters_factory) or inspect.iscoroutinefunction(adapters_factory)
            or inspect.isasyncgenfunction(adapters_factory)):
        raise InstallerHostError("fabrique adapters synchrone exigée")
    target = getattr(adapters_factory, "__call__", None)
    if inspect.iscoroutinefunction(target) or inspect.isasyncgenfunction(target):
        raise InstallerHostError("fabrique adapters synchrone exigée")
    _exact(liveness_route, RouteDeclaration, "route vivacité")
    if liveness_route.public is not True or liveness_route.handler is not liveness_view:
        raise InstallerHostError("route vivacité publique liveness_view exigée")
    if type(private_routes) not in (tuple, list):
        raise InstallerHostError("routes privées")
    declared = (liveness_route,) + tuple(private_routes)
    for route in declared[1:]:
        _exact(route, RouteDeclaration, "routes privées")
        if route.public is not False:
            raise InstallerHostError("routes fournies non publiques exigées")
    if template.profile != "web":
        raise InstallerHostError("profil web exigé")

    from django.apps import apps
    from django.conf import settings
    if settings.configured or apps.ready:
        raise InstallerHostError("Django déjà configuré")

    # Toute déclaration de route est contrôlée avant consommation C01.
    urlpatterns = build_declared_urlpatterns(declared)
    resolved = resolve_runtime_settings(template=template, source=source, mode=mode, purpose=purpose)
    _exact(resolved, RuntimeDjangoSettings, "réglages runtime")
    payload = resolved.as_dict()
    if type(payload) is not dict:
        raise InstallerHostError("payload runtime")
    if payload.get("DEBUG") is not False:
        raise InstallerHostError("DEBUG False exigé")
    if tuple(payload.get("ALLOWED_HOSTS", ())) != tuple(template.allowed_hosts):
        raise InstallerHostError("ALLOWED_HOSTS conservés exigés")
    try:
        default_cfg = dict(payload["DATABASES"]["default"])
    except (KeyError, TypeError, ValueError):
        raise InstallerHostError("bases runtime") from None
    if "PASSWORD" not in default_cfg:
        raise InstallerHostError("mot de passe runtime exigé")

    from pixs.auth.apps import DJANGO_REQUIRED_APPS
    installed = tuple(DJANGO_REQUIRED_APPS) + (_REQUIRED_APPS_SUFFIX,)
    databases = {"default": dict(default_cfg), "peer": dict(default_cfg)}

    urlconf = ModuleType("pixs_installer_urlconf")
    urlconf.urlpatterns = urlpatterns
    django_kwargs = dict(payload)
    django_kwargs.update({
        "DEBUG": False,
        "ALLOWED_HOSTS": tuple(template.allowed_hosts),
        "DATABASES": databases,
        "SECRET_KEY": payload["SECRET_KEY"],
        "INSTALLED_APPS": installed,
        "MIDDLEWARE": list(_SECURITY_MIDDLEWARE),
        "ROOT_URLCONF": urlconf,
        "USE_TZ": True,
        "TIME_ZONE": "UTC",
        "USE_X_FORWARDED_HOST": False,
        "SECURE_PROXY_SSL_HEADER": None,
        "LOGGING_CONFIG": None,
    })
    settings.configure(**django_kwargs)

    import django
    django.setup()
    if not apps.ready or not apps.is_installed("pixs.auth"):
        raise InstallerHostError("applications Django")

    from django.core.handlers.asgi import ASGIHandler
    from pixs.backend.host_asgi import HostAsgi
    handler = ASGIHandler()
    if type(handler) is not ASGIHandler:
        raise InstallerHostError("handler ASGI réel")
    holder: dict = {}

    def _lifespan_factory():
        @asynccontextmanager
        async def _context():
            from asgiref.sync import ThreadSensitiveContext, sync_to_async
            async with AsyncExitStack() as stack:
                await stack.enter_async_context(ThreadSensitiveContext())
                adapters = await sync_to_async(adapters_factory, thread_sensitive=True)(plan)
                if inspect.iscoroutine(adapters):
                    adapters.close()
                    raise InstallerHostError("fabrique adapters asynchrone interdite")
                if type(adapters) not in (tuple, list):
                    raise InstallerHostError("adapters fournis")
                runtime = host_runtime(plan, adapters=tuple(adapters))
                current = await stack.enter_async_context(runtime)
                holder["current"] = current
                try:
                    yield current
                finally:
                    holder.pop("current", None)
        return _context()

    asgi = HostAsgi(handler, _lifespan_factory)
    return InstallerHost(_ENTRY_KEY, asgi=asgi, holder=holder)
