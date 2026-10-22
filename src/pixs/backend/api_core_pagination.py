"""Curseurs Core v1 signés, sans autorité ni accès aux données métier.

Le sujet, contexte, filtre, kind, ordre et taille sont liés par empreinte.
Le snapshot d'autorisation est contrôlé après la Query propriétaire, avant
exposition. Les données signées ne sont pas chiffrées ; aucune clé ni preuve
d'authentification n'est incluse.
"""
from __future__ import annotations

import datetime
import hashlib
import hmac
import json
from dataclasses import dataclass

from django.core import signing
from pixs.core.authz.filter_plan import PROFILE_VERSION
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure

__all__ = ["API_CORE_CURSOR_VERSION", "CoreCursorError", "CoreCursorConfig",
           "CoreCursorBinding", "CoreCursorState", "CoreCursorCodec"]

API_CORE_CURSOR_VERSION = "1.0.0"
_ORDER = "core-key-v1"
_TOKEN_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-:")
_EPOCH = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


class CoreCursorError(ValueError):
    code = "API_CURSOR_INVALID"
    def __init__(self):
        super().__init__("Curseur invalide ou périmé.")


def _fail():
    raise CoreCursorError()


def _text(value, maximum=None):
    if type(value) is not str or not value or chr(0) in value:
        _fail()
    if maximum is not None and len(value) > maximum:
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeError:
        _fail()


def _utc(value):
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        _fail()
    return value


def _digest(value):
    if type(value) is not str or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        _fail()
    return value


def _hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                     separators=(",", ":"), allow_nan=False).encode("ascii")).hexdigest()


def _stamp(value):
    delta = _utc(value) - _EPOCH
    return (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds


def _date(value):
    if type(value) is not int:
        _fail()
    try:
        return _EPOCH + datetime.timedelta(microseconds=value)
    except OverflowError:
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class CoreCursorConfig:
    ttl_seconds: int
    max_cursor_chars: int
    max_reference_chars: int
    max_filter_refs: int
    max_page_size: int
    def __post_init__(self):
        for name in ("ttl_seconds", "max_cursor_chars", "max_reference_chars",
                     "max_filter_refs", "max_page_size"):
            value = object.__getattribute__(self, name)
            if type(value) is not int or value < 1:
                _fail()
        try:
            datetime.timedelta(seconds=self.ttl_seconds)
        except OverflowError:
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class CoreCursorBinding:
    subject_id: str
    context: ScopeContext
    kind: str
    resource_refs: tuple[str, ...]
    page_size: int
    def __post_init__(self):
        _text(self.subject_id)
        _text(self.kind)
        if type(self.context) is not ScopeContext:
            _fail()
        try:
            validate_structure(self.context)
        except (ScopeStructureError, AttributeError):
            _fail()
        if type(self.resource_refs) is not tuple:
            _fail()
        for ref in self.resource_refs:
            _text(ref)
        if len(set(self.resource_refs)) != len(self.resource_refs):
            _fail()
        if type(self.page_size) is not int or self.page_size < 1:
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class CoreCursorState:
    after: str
    snapshot_sha256: str
    expires_at: datetime.datetime
    def __post_init__(self):
        _text(self.after)
        _digest(self.snapshot_sha256)
        _utc(self.expires_at)


class CoreCursorCodec:
    def __init__(self, *, config: CoreCursorConfig, key: bytes, clock):
        if type(config) is not CoreCursorConfig or type(key) is not bytes or len(key) < 32:
            _fail()
        try:
            config.__post_init__()
        except AttributeError:
            _fail()
        if not callable(getattr(clock, "now", None)):
            _fail()
        self._config, self._clock = config, clock
        self._signer = signing.Signer(key=key, salt="pixs.core.cursor.v1",
                                      algorithm="sha256", fallback_keys=())

    @property
    def config(self) -> CoreCursorConfig:
        """Politique publique immuable ; ne fournit ni clé ni signature."""
        if type(self._config) is not CoreCursorConfig:
            _fail()
        self._config.__post_init__()
        return self._config

    def _now(self):
        return _utc(self._clock.now())

    def _binding(self, binding):
        if type(binding) is not CoreCursorBinding:
            _fail()
        try:
            binding.__post_init__()
        except AttributeError:
            _fail()
        config = self._config
        if (binding.page_size > config.max_page_size
                or len(binding.resource_refs) > config.max_filter_refs):
            _fail()
        context = binding.context
        for value in (binding.subject_id, binding.kind, context.tenant_id, context.scope_id):
            if value is not None:
                _text(value, config.max_reference_chars)
        for ref in binding.resource_refs:
            _text(ref, config.max_reference_chars)
        return _hash({
            "subject": binding.subject_id,
            "context": [context.scope_type.value, context.tenant_id, context.scope_id],
            "kind": binding.kind, "filter": sorted(binding.resource_refs),
            "size": binding.page_size, "order": _ORDER, "profile": PROFILE_VERSION,
        })

    def _snapshot(self, version):
        if (type(version) is not tuple or len(version) != 2
                or type(version[1]) is not tuple):
            _fail()
        _text(version[0], self._config.max_reference_chars)
        for pair in version[1]:
            if type(pair) is not tuple or len(pair) != 2:
                _fail()
            _text(pair[0], self._config.max_reference_chars)
            _text(pair[1], self._config.max_reference_chars)
        return _hash(version)

    def encode(self, *, binding: CoreCursorBinding, after: str,
               snapshot_version: tuple, decision_expires_at: datetime.datetime) -> str:
        bound = self._binding(binding)
        _text(after, self._config.max_reference_chars)
        now = self._now()
        try:
            expires = min(_utc(decision_expires_at),
                          now + datetime.timedelta(seconds=self._config.ttl_seconds))
        except OverflowError:
            _fail()
        if not now < expires:
            _fail()
        payload = {
            "version": API_CORE_CURSOR_VERSION, "binding": bound,
            "snapshot": self._snapshot(snapshot_version), "order": _ORDER,
            "page_size": binding.page_size, "after": after,
            "issued_at": _stamp(now), "expires_at": _stamp(expires),
        }
        token = self._signer.sign_object(payload, compress=False)
        if len(token) > self._config.max_cursor_chars:
            _fail()
        return token

    def decode(self, token: str, *, binding: CoreCursorBinding) -> CoreCursorState:
        bound = self._binding(binding)
        _text(token, self._config.max_cursor_chars)
        if token.count(":") != 1 or any(c not in _TOKEN_CHARS for c in token):
            _fail()
        try:
            payload = self._signer.unsign_object(token)
        except (signing.BadSignature, ValueError, TypeError, UnicodeError, RecursionError):
            raise CoreCursorError() from None
        fields = {"version", "binding", "snapshot", "order", "page_size", "after",
                  "issued_at", "expires_at"}
        if type(payload) is not dict or set(payload) != fields:
            _fail()
        if (type(payload["version"]) is not str or payload["version"] != API_CORE_CURSOR_VERSION
                or type(payload["order"]) is not str or payload["order"] != _ORDER
                or type(payload["page_size"]) is not int
                or payload["page_size"] != binding.page_size):
            _fail()
        _digest(payload["binding"])
        _digest(payload["snapshot"])
        if not hmac.compare_digest(payload["binding"], bound):
            _fail()
        _text(payload["after"], self._config.max_reference_chars)
        issued, expires = _date(payload["issued_at"]), _date(payload["expires_at"])
        if (not issued <= self._now() < expires
                or expires - issued > datetime.timedelta(seconds=self._config.ttl_seconds)):
            _fail()
        return CoreCursorState(payload["after"], payload["snapshot"], expires)

    def verify_snapshot(self, state: CoreCursorState, *, snapshot_version: tuple) -> None:
        if type(state) is not CoreCursorState:
            _fail()
        try:
            state.__post_init__()
        except AttributeError:
            _fail()
        if (not self._now() < state.expires_at
                or not hmac.compare_digest(state.snapshot_sha256, self._snapshot(snapshot_version))):
            _fail()
