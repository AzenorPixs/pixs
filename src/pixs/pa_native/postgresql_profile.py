"""Profil SQL local explicite ; aucune connexion ni preuve d'autorité."""
from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import PurePosixPath
import tomllib


class PeerProfileError(ValueError):
    """Diagnostic stable sans contenu du profil."""


def _text(value: object) -> None:
    if type(value) is not str or not value or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise PeerProfileError("PA01_PEER_TEXT_INVALID")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise PeerProfileError("PA01_PEER_UTF8_INVALID") from error


def _integer(value: object, minimum: int, maximum: int) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise PeerProfileError("PA01_PEER_NUMBER_INVALID")


@dataclass(frozen=True, slots=True, repr=False)
class PeerProfile:
    schema_version: str
    profile_ref: str
    profile_revision: str
    target_ref: str
    peer_rule_ref: str
    socket_directory: str
    port: int
    database: str
    database_user: str
    server_os_user: str
    connect_timeout_seconds: int
    statement_timeout_ms: int
    lock_timeout_ms: int
    io_timeout_ms: int
    expected_server_version_num: int

    def __post_init__(self):
        if type(self.schema_version) is not str or self.schema_version != "1.0.0":
            raise PeerProfileError("PA01_PEER_SCHEMA_INVALID")
        for name in ("profile_ref", "profile_revision", "target_ref", "peer_rule_ref",
                     "socket_directory", "database", "database_user", "server_os_user"):
            _text(getattr(self, name))
        path = PurePosixPath(self.socket_directory)
        if (not path.is_absolute() or str(path) != self.socket_directory
                or (self.socket_directory != "/" and any(
                    part in (".", "..", "") for part in self.socket_directory.split("/")[1:]))
                or "," in self.socket_directory or "\\" in self.socket_directory):
            raise PeerProfileError("PA01_PEER_SOCKET_DIRECTORY_INVALID")
        _integer(self.port, 1, 65535)
        _integer(self.connect_timeout_seconds, 1, 2147483647)
        _integer(self.statement_timeout_ms, 1, 2147483647)
        _integer(self.lock_timeout_ms, 1, 2147483647)
        _integer(self.io_timeout_ms, 1, 2147483647)
        _integer(self.expected_server_version_num, 1, 2147483647)

    def native_arguments(self) -> tuple[bytes, ...]:
        """Données pour le seul appelant natif de confiance, sans mandat implicite."""
        return tuple(str(value).encode("utf-8") for value in (
            self.socket_directory, self.port, self.database, self.database_user,
            self.server_os_user, self.connect_timeout_seconds,
            self.statement_timeout_ms, self.lock_timeout_ms, self.io_timeout_ms,
            self.expected_server_version_num))


def parse_peer_profile(text: str, *, max_bytes: int, max_field_bytes: int) -> PeerProfile:
    """Lit uniquement le texte déjà fourni par le propriétaire du profil protégé.

    Les références, la règle HBA peer, l'identité locale et leur fraîcheur
    doivent être vérifiées par leur propriétaire avant tout appel natif.
    """
    _integer(max_bytes, 1, 2147483647)
    _integer(max_field_bytes, 1, 2147483647)
    if type(text) is not str:
        raise PeerProfileError("PA01_PEER_DOCUMENT_INVALID")
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError as error:
        raise PeerProfileError("PA01_PEER_UTF8_INVALID") from error
    if len(encoded) > max_bytes:
        raise PeerProfileError("PA01_PEER_DOCUMENT_LIMIT")
    try:
        value = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise PeerProfileError("PA01_PEER_DOCUMENT_INVALID") from error
    if set(value) != {field.name for field in fields(PeerProfile)}:
        raise PeerProfileError("PA01_PEER_FIELDS_INVALID")
    profile = PeerProfile(**value)
    if any(len(item.encode("utf-8")) > max_field_bytes
           for item in value.values() if type(item) is str):
        raise PeerProfileError("PA01_PEER_FIELD_LIMIT")
    return profile
