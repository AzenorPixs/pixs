"""Justificatifs opaques Auth v1 : 256 bits, empreinte par usage, aucune session.

La représentation d'un objet ne révèle pas sa valeur. Celle-ci reste en mémoire
pour la remise au client ; elle ne doit être ni journalisée ni persistée.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import re
import secrets
from dataclasses import dataclass
from enum import Enum

_FORMAT = re.compile(r"[A-Za-z0-9_-]{43}")


class AuthTokenError(ValueError):
    def __init__(self) -> None:
        super().__init__("Justificatif opaque Auth invalide.")
        self.code = "AUTH_TOKEN_INVALID"
        self.element = "auth_token"
        self.step = "validate_token"


class TokenKind(Enum):
    WEB_SESSION = "WEB_SESSION"
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


def _bytes(value: object) -> bytes:
    if type(value) is not str or _FORMAT.fullmatch(value) is None:
        raise AuthTokenError()
    try:
        decoded = base64.urlsafe_b64decode(value + "=")
    except (binascii.Error, ValueError):
        raise AuthTokenError() from None
    canonical = base64.urlsafe_b64encode(decoded).rstrip(b"=").decode("ascii")
    if len(decoded) != 32 or not hmac.compare_digest(value, canonical):
        raise AuthTokenError()
    return decoded


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class OpaqueToken:
    value: str

    def __post_init__(self) -> None:
        try:
            value = object.__getattribute__(self, "value")
        except AttributeError:
            raise AuthTokenError() from None
        _bytes(value)


def parse_token(value: str) -> OpaqueToken:
    """Valide seulement le format ; ne prouve ni existence ni validité courante."""
    return OpaqueToken(value)


def new_token() -> OpaqueToken:
    value = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    return OpaqueToken(value)


def token_fingerprint(token: OpaqueToken, kind: TokenKind) -> str:
    if type(token) is not OpaqueToken:
        raise AuthTokenError()
    if type(kind) is not TokenKind or not any(kind is member for member in TokenKind):
        raise AuthTokenError()
    try:
        value = object.__getattribute__(token, "value")
    except AttributeError:
        raise AuthTokenError() from None
    raw = _bytes(value)
    domain = b"pixs.auth.token.v1\0" + kind.value.encode("ascii") + b"\0"
    return hashlib.sha256(domain + raw).hexdigest()


__all__ = ["AuthTokenError", "TokenKind", "OpaqueToken", "parse_token",
           "new_token", "token_fingerprint"]
