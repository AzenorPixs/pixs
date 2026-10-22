"""Argon2id D11 via Django, sans sélection de confiance ni création de session.

Les secrets restent en mémoire ; aucun effacement garanti des str Python.
L'adaptation d'enveloppe conserve l'empreinte, sans nouveau hachage.
"""
from __future__ import annotations

from argon2 import extract_parameters
from argon2.low_level import Type
from argon2.exceptions import (
    HashingError, InvalidHashError, UnsupportedParametersError,
    VerificationError, VerifyMismatchError,
)
from django.contrib.auth.hashers import Argon2PasswordHasher

_DJANGO = "argon2$argon2id$v=19$"
_LDAP = "{ARGON2}$argon2id$v=19$"


class AuthPasswordError(ValueError):
    def __init__(self) -> None:
        super().__init__("Justificatif Argon2id invalide.")
        self.code = "AUTH_PASSWORD_INVALID"
        self.element = "auth_password"
        self.step = "validate_password"


def _password(value: object) -> None:
    if type(value) is not str or value == "":
        raise AuthPasswordError()


def _hasher() -> Argon2PasswordHasher:
    hasher = Argon2PasswordHasher()
    if (hasher.memory_cost, hasher.time_cost, hasher.parallelism) != (102400, 2, 8):
        raise AuthPasswordError()
    return hasher


def _check(encoded: object, prefix: str) -> str:
    if (type(encoded) is not str or not encoded.isascii()
            or len(encoded) > 512 or not encoded.startswith(prefix)):
        raise AuthPasswordError()
    offset = len("argon2") if prefix == _DJANGO else len("{ARGON2}")
    try:
        params = extract_parameters(encoded[offset:])
    except (ValueError, InvalidHashError):
        raise AuthPasswordError() from None
    if not (params.type is Type.ID and params.version == 19
            and params.memory_cost == 102400 and params.time_cost == 2
            and params.parallelism == 8 and params.hash_len == 32
            and params.salt_len >= 16):
        raise AuthPasswordError()
    return encoded


def hash_password(password: str) -> str:
    """Produit une empreinte Django au profil qualifié, sans persistance."""
    _password(password)
    hasher = _hasher()
    try:
        encoded = hasher.encode(password, hasher.salt())
    except (HashingError, UnsupportedParametersError, ValueError):
        raise AuthPasswordError() from None
    return _check(encoded, _DJANGO)


def verify_password(password: str, encoded: str) -> bool:
    """Vérifie une enveloppe Django ; un autre profil est refusé avant calcul."""
    _password(password)
    encoded = _check(encoded, _DJANGO)
    try:
        return _hasher().verify(password, encoded)
    except VerifyMismatchError:
        return False
    except (VerificationError, InvalidHashError, UnsupportedParametersError, ValueError):
        raise AuthPasswordError() from None


def envelope_to_ldap(encoded: str) -> str:
    return "{ARGON2}" + _check(encoded, _DJANGO)[len("argon2"):]


def envelope_to_django(encoded: str) -> str:
    return "argon2" + _check(encoded, _LDAP)[len("{ARGON2}"):]


__all__ = ["AuthPasswordError", "hash_password", "verify_password",
           "envelope_to_ldap", "envelope_to_django"]
