"""Identifiants internes UUIDv7 DNS ; stdlib Python3.12, aucun secret ni IO à l’import."""
from __future__ import annotations

import secrets
import time
import uuid

__all__ = ["DnsIdentifierError", "require_uuid7", "new_uuid7"]

class DnsIdentifierError(ValueError):
    def __init__(self) -> None:
        super().__init__("Identifiant DNS invalide.")
        self.code = "DNS_IDENTIFIER_INVALID"
        self.element = "dns_identifier"
        self.step = "validate_identifier"


def require_uuid7(value: object) -> uuid.UUID:
    if type(value) is not uuid.UUID:
        raise DnsIdentifierError()
    try:
        number = object.__getattribute__(value, "int")
    except AttributeError:
        raise DnsIdentifierError() from None
    if type(number) is not int or not 0 <= number < 2**128:
        raise DnsIdentifierError()
    if (number >> 76) & 15 != 7 or (number >> 62) & 3 != 2:
        raise DnsIdentifierError()
    return value


def new_uuid7() -> uuid.UUID:
    """Format UUIDv7 stdlib compatible Python 3.12, sans compteur DB."""
    milliseconds = time.time_ns() // 1_000_000
    if type(milliseconds) is not int or not 0 <= milliseconds < 2**48:
        raise DnsIdentifierError()
    rand_a, rand_b = secrets.randbits(12), secrets.randbits(62)
    if (type(rand_a) is not int or not 0 <= rand_a < 2**12
            or type(rand_b) is not int or not 0 <= rand_b < 2**62):
        raise DnsIdentifierError()
    number = ((milliseconds << 80) | (7 << 76) | (rand_a << 64)
              | (2 << 62) | rand_b)
    return require_uuid7(uuid.UUID(int=number))

