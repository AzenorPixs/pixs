"""Transport hôte ASGI, sans configuration Django ni politique applicative.

Reçoit un handler Django déjà configuré et une fabrique de contexte de
durée de vie asynchrone. Pilote le lifespan réel via AsyncExitStack.
Ne fournit aucun lifecycle Auth ni verdict de disponibilité applicative.

AsyncExitStack ne nettoie pas la partie __aenter__ échouée du même contexte.
La fabrique concrète doit gérer ses acquisitions partielles avec son propre
contexte de ressources. Le transport nettoie les contextes effectivement
entrés, y compris si receive/send échoue ou si la tâche est annulée.
Les exceptions des extensions sont traduites en événements failed bornés ;
les interruptions BaseException sont nettoyées puis propagées.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, AsyncExitStack

__all__ = [
    "HostAsgi",
    "HostAsgiError",
]

_ERROR = "Transport ASGI invalide."

_PHASE_NEW = "NEW"
_PHASE_STARTING = "STARTING"
_PHASE_STARTED = "STARTED"
_PHASE_STOPPING = "STOPPING"
_PHASE_STOPPED = "STOPPED"
_PHASE_FAILED = "FAILED"

Scope = dict[str, object]
Receive = Callable[[], Awaitable[dict[str, object]]]
Send = Callable[[dict[str, object]], Awaitable[None]]
LifespanFactory = Callable[[], AbstractAsyncContextManager[object]]


class HostAsgiError(ValueError):
    """Refus generique du transport, sans echo de valeur."""

    def __init__(self, message: str = _ERROR) -> None:
        super().__init__(message)


def _invalid() -> HostAsgiError:
    return HostAsgiError(_ERROR)


class HostAsgi:
    """Enveloppe lifespan et garde de phase autour du handler reel."""

    __slots__ = ("_factory", "_handler", "_lifespan_active", "_loop", "_phase", "_stack")

    def __init__(self, handler: object, lifespan_context_factory: LifespanFactory) -> None:
        from django.core.handlers.asgi import ASGIHandler as _ASGIHandler
        if not isinstance(handler, _ASGIHandler):
            raise _invalid() from None
        if not callable(lifespan_context_factory):
            raise _invalid() from None
        self._handler = handler
        self._factory = lifespan_context_factory
        self._stack: AsyncExitStack | None = None
        self._phase = _PHASE_NEW
        self._lifespan_active = False
        self._loop: asyncio.AbstractEventLoop | None = None

    @property
    def phase(self) -> str:
        return self._phase

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        loop = asyncio.get_running_loop()
        if self._loop is None:
            self._loop = loop
        elif self._loop is not loop:
            raise _invalid() from None
        if type(scope) is not dict:
            raise _invalid() from None
        scope_type = scope.get("type")
        if scope_type == "lifespan":
            await self._handle_lifespan(receive, send)
            return
        if scope_type == "http":
            await self._handle_http(scope, receive, send)
            return
        raise _invalid() from None

    async def _handle_http(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self._phase != _PHASE_STARTED:
            await send(
                {
                    "type": "http.response.start",
                    "status": 503,
                    "headers": [
                        (b"content-type", b"text/plain; charset=utf-8"),
                        (b"content-length", b"0"),
                        (b"cache-control", b"no-store"),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": b"", "more_body": False})
            return
        await self._handler(scope, receive, send)

    async def _handle_lifespan(self, receive: Receive, send: Send) -> None:
        if self._lifespan_active is True:
            raise _invalid() from None
        self._lifespan_active = True
        try:
            while True:
                message = await receive()
                if type(message) is not dict:
                    raise _invalid() from None
                msg_type = message.get("type")
                if msg_type == "lifespan.startup":
                    ok = await self._on_startup(send)
                    if ok is True:
                        continue
                    return
                if msg_type == "lifespan.shutdown":
                    await self._on_shutdown(send)
                    return
                raise _invalid() from None
        finally:
            try:
                stack = self._stack
                if stack is not None:
                    self._phase = _PHASE_STOPPING
                    try:
                        await stack.aclose()
                    finally:
                        self._phase = _PHASE_FAILED
                        self._stack = None
            finally:
                if self._phase in (_PHASE_STARTING, _PHASE_STARTED, _PHASE_STOPPING):
                    self._phase = _PHASE_FAILED
                self._lifespan_active = False

    async def _on_startup(self, send: Send) -> bool:
        if self._phase == _PHASE_STARTED:
            await send({"type": "lifespan.startup.complete"})
            return True
        if self._phase != _PHASE_NEW:
            await send({"type": "lifespan.startup.failed", "message": _ERROR})
            return False
        self._phase = _PHASE_STARTING
        stack = AsyncExitStack()
        try:
            context = self._factory()
            if not (hasattr(context, "__aenter__") and hasattr(context, "__aexit__")):
                raise _invalid() from None
            await stack.enter_async_context(context)
        except Exception:
            try:
                await stack.aclose()
            except Exception:
                self._phase = _PHASE_FAILED
                self._stack = None
                await send({"type": "lifespan.startup.failed", "message": _ERROR})
                return False
            self._phase = _PHASE_FAILED
            self._stack = None
            await send({"type": "lifespan.startup.failed", "message": _ERROR})
            return False
        except BaseException:
            try:
                await stack.aclose()
            except BaseException:
                self._phase = _PHASE_FAILED
                self._stack = None
                raise
            self._phase = _PHASE_FAILED
            self._stack = None
            raise
        self._stack = stack
        self._phase = _PHASE_STARTED
        await send({"type": "lifespan.startup.complete"})
        return True

    async def _on_shutdown(self, send: Send) -> None:
        if self._phase == _PHASE_STOPPED:
            await send({"type": "lifespan.shutdown.complete"})
            return
        if self._phase == _PHASE_FAILED:
            await send({"type": "lifespan.shutdown.failed", "message": _ERROR})
            return
        stack = self._stack
        if stack is None:
            self._phase = _PHASE_STOPPED
            await send({"type": "lifespan.shutdown.complete"})
            return
        self._phase = _PHASE_STOPPING
        try:
            await stack.aclose()
        except Exception:
            self._stack = None
            self._phase = _PHASE_FAILED
            await send({"type": "lifespan.shutdown.failed", "message": _ERROR})
            return
        except BaseException:
            self._stack = None
            self._phase = _PHASE_FAILED
            raise
        self._stack = None
        self._phase = _PHASE_STOPPED
        await send({"type": "lifespan.shutdown.complete"})
