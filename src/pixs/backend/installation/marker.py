"""Marqueur privé C08, sans sélection de mode ni autorisation métier.

La composition serveur fournit le lecteur propriétaire et sa garde exclusive
de résultat confirmé. Ce module ne fournit pas encore ce lecteur PostgreSQL.
Une recette avec un double ne qualifie que les entrées et sorties du fichier.
"""
from __future__ import annotations

import json
import os
import stat
import uuid
from contextlib import AbstractContextManager, ExitStack, contextmanager
from dataclasses import dataclass
from typing import Protocol

__all__ = ["MarkerConfig", "InstallationMarkerContent", "ConfirmedResultSource",
           "MarkerInvalid", "MarkerUnknown", "MarkerDivergent",
           "MarkerIssueUnknown", "MarkerResultUnavailable",
           "read_installation_marker", "publish_installation_marker"]


class MarkerInvalid(ValueError):
    """Diagnostic fermé, sans chemin ni contenu du fichier."""
    code = "C08_MARKER_INVALID"

    def __init__(self) -> None:
        super().__init__("Marqueur d'installation refusé.")


class MarkerUnknown(MarkerInvalid):
    code = "C08_MARKER_UNKNOWN"


class MarkerDivergent(MarkerInvalid):
    code = "C08_MARKER_DIVERGENT"


class MarkerIssueUnknown(MarkerInvalid):
    code = "C08_MARKER_ISSUE_UNKNOWN"


class MarkerResultUnavailable(MarkerInvalid):
    code = "C08_MARKER_RESULT_UNAVAILABLE"


def _positive(value: object) -> None:
    if type(value) is not int or value < 1:
        raise MarkerInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class MarkerConfig:
    path: str
    owner_uid: int
    owner_gid: int
    max_bytes: int
    max_ref_len: int
    allowed_format_versions: tuple[str, ...]
    parent_identities: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        if (type(self.path) is not str or not self.path.startswith("/")
                or "\x00" in self.path
                or any(p in ("", ".", "..") for p in self.path.split("/")[1:])):
            raise MarkerInvalid()
        for value in (self.owner_uid, self.owner_gid):
            if type(value) is not int or value < 0:
                raise MarkerInvalid()
        _positive(self.max_bytes)
        _positive(self.max_ref_len)
        if type(self.allowed_format_versions) is not tuple or not self.allowed_format_versions:
            raise MarkerInvalid()
        for version in self.allowed_format_versions:
            _reference(version, self.max_ref_len)
        if len(set(self.allowed_format_versions)) != len(self.allowed_format_versions):
            raise MarkerInvalid()
        if type(self.parent_identities) is not tuple or not self.parent_identities:
            raise MarkerInvalid()
        for pair in self.parent_identities:
            if type(pair) is not tuple or len(pair) != 2:
                raise MarkerInvalid()
            if any(type(v) is not int or v < 0 for v in pair):
                raise MarkerInvalid()


def _reference(value: object, bound: int) -> None:
    if (type(value) is not str or not 0 < len(value) <= bound
            or not value.isprintable()):
        raise MarkerInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class InstallationMarkerContent:
    format_version: str
    installation_ref: str
    result_ref: str
    result_version: int


class ConfirmedResultSource(Protocol):
    """Capacité privée injectée par le serveur, jamais un paramètre client.

    Le producteur inspecte le commit par la voie propriétaire, refuse tout
    état absent/inconnu/divergent et détient l'exclusion interprocessus sur
    l'installation jusqu'à la sortie du contexte, y compris les fsync.
    Le DTO retourné ne constitue pas à lui seul une preuve de commit.
    """

    def guard_confirmed(self, *, installation_ref: str
                        ) -> AbstractContextManager[InstallationMarkerContent]: ...


def _checked(content: object, config: MarkerConfig) -> InstallationMarkerContent:
    if type(content) is not InstallationMarkerContent:
        raise MarkerInvalid()
    for value in (content.format_version, content.installation_ref, content.result_ref):
        _reference(value, config.max_ref_len)
    if content.format_version not in config.allowed_format_versions:
        raise MarkerInvalid()
    _positive(content.result_version)
    return content


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise MarkerInvalid()
        result[key] = value
    return result


def _constant(value: str) -> object:
    raise MarkerInvalid()


def _decode(raw: bytes, config: MarkerConfig) -> InstallationMarkerContent:
    try:
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                         parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError):
        raise MarkerInvalid() from None
    keys = {"format_version", "installation_ref", "result_ref", "result_version"}
    if type(obj) is not dict or set(obj) != keys:
        raise MarkerInvalid()
    return _checked(InstallationMarkerContent(**obj), config)


@contextmanager
def _fd(descriptor: int):
    try:
        yield descriptor
    finally:
        os.close(descriptor)


def _directory(st: os.stat_result, config: MarkerConfig, *, final: bool) -> None:
    if not stat.S_ISDIR(st.st_mode):
        raise MarkerInvalid()
    if final:
        if ((st.st_uid, st.st_gid) != (config.owner_uid, config.owner_gid)
                or stat.S_IMODE(st.st_mode) != 0o700):
            raise MarkerInvalid()
    else:
        if (st.st_uid, st.st_gid) not in config.parent_identities:
            raise MarkerInvalid()
        # Un parent publiquement modifiable n'est admissible que comme
        # répertoire système sticky ; le dernier parent reste privé 0700.
        if st.st_mode & 0o002 and not (st.st_uid == 0 and st.st_mode & stat.S_ISVTX):
            raise MarkerInvalid()


def _parent(config: MarkerConfig) -> tuple[int, str]:
    components = config.path.split("/")[1:]
    with ExitStack() as stack:
        current = stack.enter_context(_fd(os.open(
            "/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)))
        _directory(os.fstat(current), config, final=len(components) == 1)
        for index, name in enumerate(components[:-1]):
            current = stack.enter_context(_fd(os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=current)))
            _directory(os.fstat(current), config, final=index == len(components) - 2)
        return os.dup(current), components[-1]


def _same_parent(config: MarkerConfig, directory: int) -> None:
    fresh, _ = _parent(config)
    with _fd(fresh):
        first, second = os.fstat(directory), os.fstat(fresh)
        if (first.st_dev, first.st_ino) != (second.st_dev, second.st_ino):
            raise MarkerIssueUnknown()


def _regular(st: os.stat_result, config: MarkerConfig) -> None:
    if (not stat.S_ISREG(st.st_mode) or stat.S_IMODE(st.st_mode) != 0o600
            or (st.st_uid, st.st_gid) != (config.owner_uid, config.owner_gid)
            or st.st_nlink != 1 or not 0 < st.st_size <= config.max_bytes):
        raise MarkerInvalid()


def _fingerprint(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns,
            st.st_uid, st.st_gid, st.st_mode, st.st_nlink)


def _read(directory: int, name: str, config: MarkerConfig, *,
          durable: bool = False) -> InstallationMarkerContent | None:
    try:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                             | os.O_CLOEXEC, dir_fd=directory)
    except FileNotFoundError:
        return None
    with _fd(descriptor):
        before = os.fstat(descriptor)
        _regular(before, config)
        raw = bytearray()
        while len(raw) <= config.max_bytes:
            part = os.read(descriptor, min(8192, config.max_bytes + 1 - len(raw)))
            if not part:
                break
            raw.extend(part)
        if len(raw) > config.max_bytes:
            raise MarkerInvalid()
        after = os.fstat(descriptor)
        named = os.stat(name, dir_fd=directory, follow_symlinks=False)
        if (_fingerprint(before) != _fingerprint(after)
                or _fingerprint(after) != _fingerprint(named)):
            raise MarkerInvalid()
        content = _decode(bytes(raw), config)
        if durable:
            os.fsync(descriptor)
            os.fsync(directory)
        return content


def _config(config: object) -> None:
    if type(config) is not MarkerConfig:
        raise MarkerInvalid()
    config.__post_init__()


def read_installation_marker(config: MarkerConfig) -> InstallationMarkerContent:
    _config(config)
    try:
        parent, name = _parent(config)
        with _fd(parent):
            content = _read(parent, name, config)
            _same_parent(config, parent)
        if content is None:
            raise MarkerUnknown()
        return content
    except FileNotFoundError:
        raise MarkerUnknown() from None
    except OSError:
        raise MarkerInvalid() from None


def _remove_own_tmp(directory: int, name: str, created: os.stat_result) -> None:
    try:
        current = os.stat(name, dir_fd=directory, follow_symlinks=False)
    except FileNotFoundError:
        return
    if (current.st_dev, current.st_ino) != (created.st_dev, created.st_ino):
        raise MarkerIssueUnknown()
    os.unlink(name, dir_fd=directory)


def _publish(directory: int, name: str, payload: bytes, config: MarkerConfig) -> None:
    temporary = ".c08-marker-" + uuid.uuid4().hex
    created = None
    moved = False
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                             | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=directory)
        with _fd(descriptor):
            created = os.fstat(descriptor)
            if ((created.st_uid, created.st_gid) != (config.owner_uid, config.owner_gid)
                    or not stat.S_ISREG(created.st_mode)
                    or stat.S_IMODE(created.st_mode) != 0o600 or created.st_nlink != 1):
                raise MarkerInvalid()
            remaining = memoryview(payload)
            while remaining:
                written = os.write(descriptor, remaining)
                if written <= 0:
                    raise MarkerIssueUnknown()
                remaining = remaining[written:]
            os.fsync(descriptor)
            written_stat = os.fstat(descriptor)
            named = os.stat(temporary, dir_fd=directory, follow_symlinks=False)
            _regular(written_stat, config)
            if _fingerprint(written_stat) != _fingerprint(named):
                raise MarkerIssueUnknown()
        _same_parent(config, directory)
        os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
        moved = True
        os.fsync(directory)
    finally:
        if created is not None and not moved:
            _remove_own_tmp(directory, temporary, created)


def publish_installation_marker(*, config: MarkerConfig, installation_ref: str,
                                source: ConfirmedResultSource
                                ) -> InstallationMarkerContent:
    _config(config)
    _reference(installation_ref, config.max_ref_len)
    if source is None or not callable(getattr(source, "guard_confirmed", None)):
        raise MarkerResultUnavailable()
    try:
        # La garde appartient au lecteur C08 de la composition de confiance.
        # Aucun held=True fourni par l'appelant ne remplace cette capacité.
        with source.guard_confirmed(installation_ref=installation_ref) as result:
            expected = _checked(result, config)
            if expected.installation_ref != installation_ref:
                raise MarkerDivergent()
            payload = json.dumps(
                {"format_version": expected.format_version,
                 "installation_ref": expected.installation_ref,
                 "result_ref": expected.result_ref,
                 "result_version": expected.result_version},
                ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                allow_nan=False).encode("utf-8")
            if len(payload) > config.max_bytes:
                raise MarkerInvalid()
            parent, name = _parent(config)
            with _fd(parent):
                existing = _read(parent, name, config)
                if existing is not None and existing != expected:
                    raise MarkerDivergent()
                if existing is None:
                    _publish(parent, name, payload, config)
                confirmed = _read(parent, name, config, durable=True)
                _same_parent(config, parent)
                if confirmed != expected:
                    raise MarkerIssueUnknown()
                return confirmed
    except (OSError, UnicodeError):
        # Après replace, une panne de fsync n'autorise pas une annonce de
        # succès ; la reprise devra inspecter le résultat et le fichier.
        raise MarkerIssueUnknown() from None
