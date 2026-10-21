"""UUIDv7 Auth et références Core : identifiants, jamais justificatifs d'accès."""
from __future__ import annotations

import secrets
import time
import uuid

CORE_IDENTITY_PREFIX = "pixs.core.identity:"


class AuthIdentifierError(ValueError):
    def __init__(self) -> None:
        super().__init__("Identifiant Auth invalide.")
        self.code = "AUTH_IDENTIFIER_INVALID"
        self.element = "auth_identifier"
        self.step = "validate_identifier"


def require_uuid7(value: object) -> uuid.UUID:
    if type(value) is not uuid.UUID:
        raise AuthIdentifierError()
    try:
        number = object.__getattribute__(value, "int")
    except AttributeError:
        raise AuthIdentifierError() from None
    if type(number) is not int or not 0 <= number < 2**128:
        raise AuthIdentifierError()
    if (number >> 76) & 15 != 7 or (number >> 62) & 3 != 2:
        raise AuthIdentifierError()
    return value


def new_uuid7() -> uuid.UUID:
    """Format UUIDv7 stdlib compatible Python 3.12, sans compteur DB."""
    milliseconds = time.time_ns() // 1_000_000
    if type(milliseconds) is not int or not 0 <= milliseconds < 2**48:
        raise AuthIdentifierError()
    rand_a, rand_b = secrets.randbits(12), secrets.randbits(62)
    if (type(rand_a) is not int or not 0 <= rand_a < 2**12
            or type(rand_b) is not int or not 0 <= rand_b < 2**62):
        raise AuthIdentifierError()
    number = ((milliseconds << 80) | (7 << 76) | (rand_a << 64)
              | (2 << 62) | rand_b)
    return require_uuid7(uuid.UUID(int=number))


def identity_reference(identity_id: uuid.UUID) -> str:
    return CORE_IDENTITY_PREFIX + str(require_uuid7(identity_id))


def parse_identity_reference(reference: str) -> uuid.UUID:
    if type(reference) is not str or not reference.startswith(CORE_IDENTITY_PREFIX):
        raise AuthIdentifierError()
    raw = reference[len(CORE_IDENTITY_PREFIX):]
    if len(raw) != 36:
        raise AuthIdentifierError()
    try:
        parsed = uuid.UUID(raw)
    except ValueError:
        raise AuthIdentifierError() from None
    require_uuid7(parsed)
    if str(parsed) != raw:
        raise AuthIdentifierError()
    return parsed


__all__ = ["AuthIdentifierError", "CORE_IDENTITY_PREFIX", "require_uuid7",
           "new_uuid7", "identity_reference", "parse_identity_reference"]
