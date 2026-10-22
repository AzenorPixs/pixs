"""Generateur et controle UUIDv7 Core, stdlib seule, sans effet a l'import."""

from __future__ import annotations

import secrets
import time
import uuid

__all__ = ["Uuid7Error", "check_uuid7", "generate_uuid7"]


class Uuid7Error(ValueError):
    """Refus ferme sans echo de valeur."""

    def __init__(self) -> None:
        super().__init__("UUIDv7 invalide.")
        self.code = "UUID7_INVALID"
        self.element = "uuid7"
        self.step = "validate_uuid7"


def generate_uuid7() -> uuid.UUID:
    """Construit un UUIDv7 version 7, variant RFC4122."""
    ms = time.time_ns() // 1_000_000
    if not 0 <= ms < 2**48:
        raise Uuid7Error()
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    int_val = (ms << 80) | (7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    return uuid.UUID(int=int_val)


def check_uuid7(value: object) -> bool:
    """Controle exact local, sans appel hostile ni coercition."""
    if type(value) is not uuid.UUID:
        raise Uuid7Error()
    try:
        int_val = object.__getattribute__(value, "int")
        version = object.__getattribute__(value, "version")
        variant = object.__getattribute__(value, "variant")
    except AttributeError:
        raise Uuid7Error() from None
    if type(int_val) is not int or not 0 <= int_val < 2**128:
        raise Uuid7Error()
    if version != 7 or variant != uuid.RFC_4122:
        raise Uuid7Error()
    return True
