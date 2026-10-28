"""Checkpoint durable privé C08, sans autorité ni sélection de mode.

Observations de progression seules. Ne prouve ni commit, ni résultat,
ni autorisation, ni disponibilité. Ne déclenche aucun mode ni effet externe.
Le digest et les champs sont une liaison structurelle ; le futur consommateur
rapproche le checkpoint du plan immuable courant. Ils ne prouvent ni ce plan
ni son autorisation. Publication via helper privé existant marker._publish,
sans refactor, avec son temporaire privé dans le même répertoire.
"""
from __future__ import annotations

import fcntl
import json
import os
import stat
from contextlib import contextmanager
from dataclasses import dataclass

from pixs.backend.installation import marker as _io
from pixs.backend.installation.plan import PlanInvalid

__all__ = ["CheckpointLimits", "CheckpointConfig", "InstallationCheckpointContent",
           "CheckpointRefused", "CheckpointUnknown", "CheckpointBusy",
           "CheckpointConflict", "CheckpointIssueUnknown",
           "initialize_checkpoint_guard", "read_checkpoint", "publish_checkpoint"]


class CheckpointRefused(PlanInvalid):
    code = "C08_CHECKPOINT_REFUSED"


class CheckpointUnknown(CheckpointRefused):
    code = "C08_CHECKPOINT_UNKNOWN"


class CheckpointBusy(CheckpointRefused):
    code = "C08_CHECKPOINT_BUSY"


class CheckpointConflict(CheckpointRefused):
    code = "C08_CHECKPOINT_CONFLICT"


class CheckpointIssueUnknown(CheckpointRefused):
    code = "C08_CHECKPOINT_ISSUE_UNKNOWN"


_PHASES = ("PLAN_RECORDED", "PROOF_LINK_OBSERVED",
           "INSPECTION_OBSERVED", "RECOVERY_NOTE_RECORDED")


def _positive(value: object) -> None:
    if type(value) is not int or value < 1:
        raise CheckpointRefused()


def _reference(value: object, bound: int) -> None:
    if (type(value) is not str or not 0 < len(value) <= bound
            or not value.isprintable()):
        raise CheckpointRefused()


@dataclass(frozen=True, slots=True, repr=False)
class CheckpointLimits:
    max_bytes: int
    max_ref_len: int
    max_confirmations: int
    allowed_format_versions: tuple[str, ...]
    allowed_phases: tuple[str, ...]

    def __post_init__(self) -> None:
        for value in (self.max_bytes, self.max_ref_len, self.max_confirmations):
            if type(value) is not int or value < 1:
                raise CheckpointRefused()
        for versions in (self.allowed_format_versions, self.allowed_phases):
            if type(versions) is not tuple or not versions:
                raise CheckpointRefused()
            for version in versions:
                _reference(version, self.max_ref_len)
            if len(set(versions)) != len(versions):
                raise CheckpointRefused()
        if any(p not in _PHASES for p in self.allowed_phases):
            raise CheckpointRefused()


@dataclass(frozen=True, slots=True, repr=False)
class InstallationCheckpointContent:
    format_version: str
    installation_ref: str
    database_target_ref: str
    operation_id: str
    plan_version: str
    plan_sha256: str
    correlation_id: str
    causation_id: str | None
    idempotency_key: str
    revision: int
    phase: str
    confirmation_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True, repr=False)
class CheckpointConfig:
    io: _io.MarkerConfig
    lock_basename: str
    limits: CheckpointLimits

    def __post_init__(self) -> None:
        if type(self.io) is not _io.MarkerConfig or type(self.limits) is not CheckpointLimits:
            raise CheckpointRefused()
        self.io.__post_init__()
        self.limits.__post_init__()
        name = self.lock_basename
        if (type(name) is not str or not name or name in (".", "..")
                or "/" in name or not name.isprintable()
                or len(name) > self.io.max_ref_len
                or name == os.path.basename(self.io.path)):
            raise CheckpointRefused()
        if (self.io.max_bytes != self.limits.max_bytes
                or self.io.max_ref_len != self.limits.max_ref_len
                or self.io.allowed_format_versions != self.limits.allowed_format_versions):
            raise CheckpointRefused()


def _config(config: object) -> None:
    if type(config) is not CheckpointConfig:
        raise CheckpointRefused()
    try:
        config.__post_init__()
    except _io.MarkerInvalid:
        raise CheckpointRefused() from None


def _checked(content: object, config: CheckpointConfig) -> InstallationCheckpointContent:
    if type(content) is not InstallationCheckpointContent:
        raise CheckpointRefused()
    for value in (content.format_version, content.installation_ref,
                  content.database_target_ref, content.operation_id,
                  content.plan_version, content.correlation_id,
                  content.idempotency_key):
        _reference(value, config.limits.max_ref_len)
    if content.causation_id is not None:
        _reference(content.causation_id, config.limits.max_ref_len)
    if type(content.phase) is not str:
        raise CheckpointRefused()
    _reference(content.phase, config.limits.max_ref_len)
    if content.format_version not in config.limits.allowed_format_versions:
        raise CheckpointRefused()
    if content.phase not in config.limits.allowed_phases:
        raise CheckpointRefused()
    _positive(content.revision)
    digest = content.plan_sha256
    if (type(digest) is not str or len(digest) != 64
            or any(c not in "0123456789abcdef" for c in digest)):
        raise CheckpointRefused()
    refs = content.confirmation_refs
    if type(refs) is not tuple:
        raise CheckpointRefused()
    for ref in refs:
        _reference(ref, config.limits.max_ref_len)
    if len(refs) > config.limits.max_confirmations or len(set(refs)) != len(refs):
        raise CheckpointRefused()
    return content


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise CheckpointRefused()
        result[key] = value
    return result


def _constant(value: str) -> object:
    raise CheckpointRefused()


def _decode(raw: bytes, config: CheckpointConfig) -> InstallationCheckpointContent:
    try:
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                         parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError):
        raise CheckpointRefused() from None
    keys = {"format_version", "installation_ref", "database_target_ref",
            "operation_id", "plan_version", "plan_sha256", "correlation_id",
            "causation_id", "idempotency_key", "revision",
            "phase", "confirmation_refs"}
    if type(obj) is not dict or set(obj) != keys:
        raise CheckpointRefused()
    if type(obj["confirmation_refs"]) is not list:
        raise CheckpointRefused()
    obj["confirmation_refs"] = tuple(obj["confirmation_refs"])
    return _checked(InstallationCheckpointContent(**obj), config)


def _encode(content: InstallationCheckpointContent, config: CheckpointConfig) -> bytes:
    _checked(content, config)
    document = {"format_version": content.format_version,
                "installation_ref": content.installation_ref,
                "database_target_ref": content.database_target_ref,
                "operation_id": content.operation_id,
                "plan_version": content.plan_version,
                "plan_sha256": content.plan_sha256,
                "correlation_id": content.correlation_id,
                "causation_id": content.causation_id,
                "idempotency_key": content.idempotency_key,
                "revision": content.revision,
                "phase": content.phase,
                "confirmation_refs": list(content.confirmation_refs)}
    try:
        raw = json.dumps(document, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError):
        raise CheckpointRefused() from None
    if not 0 < len(raw) <= config.limits.max_bytes:
        raise CheckpointRefused()
    return raw


def _lock_file(descriptor: int, config: CheckpointConfig) -> None:
    current = os.fstat(descriptor)
    if (not stat.S_ISREG(current.st_mode) or stat.S_IMODE(current.st_mode) != 0o600
            or current.st_nlink != 1 or current.st_size != 0
            or (current.st_uid, current.st_gid) != (config.io.owner_uid, config.io.owner_gid)):
        raise CheckpointRefused()


def initialize_checkpoint_guard(config: CheckpointConfig) -> None:
    _config(config)
    observed = False
    try:
        parent, _ = _io._parent(config.io)
        with _io._fd(parent):
            try:
                descriptor = os.open(
                    config.lock_basename, os.O_CREAT | os.O_EXCL | os.O_RDWR
                    | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, 0o600, dir_fd=parent)
            except FileExistsError:
                descriptor = os.open(
                    config.lock_basename, os.O_RDONLY | os.O_NOFOLLOW
                    | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
            observed = True
            with _io._fd(descriptor):
                _lock_file(descriptor, config)
                current = os.fstat(descriptor)
                named = os.stat(config.lock_basename, dir_fd=parent, follow_symlinks=False)
                if _io._fingerprint(current) != _io._fingerprint(named):
                    raise CheckpointRefused()
                os.fsync(descriptor)
                os.fsync(parent)
                _io._same_parent(config.io, parent)
    except FileNotFoundError:
        if observed:
            raise CheckpointIssueUnknown() from None
        raise CheckpointUnknown() from None
    except (_io.MarkerIssueUnknown, OSError):
        raise CheckpointIssueUnknown() from None
    except (_io.MarkerInvalid, UnicodeError):
        raise CheckpointRefused() from None


@contextmanager
def _guard(config: CheckpointConfig, *, write: bool):
    _config(config)
    observed = False
    entered = False
    try:
        parent, name = _io._parent(config.io)
        with _io._fd(parent):
            descriptor = os.open(
                config.lock_basename, os.O_RDONLY | os.O_NOFOLLOW
                | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
            observed = True
            with _io._fd(descriptor):
                _lock_file(descriptor, config)
                try:
                    fcntl.flock(descriptor, (fcntl.LOCK_EX if write else fcntl.LOCK_SH)
                                | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise CheckpointBusy() from None
                before = os.fstat(descriptor)
                named = os.stat(config.lock_basename, dir_fd=parent, follow_symlinks=False)
                if _io._fingerprint(before) != _io._fingerprint(named):
                    raise CheckpointRefused()
                entered = True
                yield parent, name
                _io._same_parent(config.io, parent)
                named = os.stat(config.lock_basename, dir_fd=parent, follow_symlinks=False)
                if _io._fingerprint(before) != _io._fingerprint(named):
                    raise CheckpointIssueUnknown()
    except FileNotFoundError:
        if observed:
            raise CheckpointIssueUnknown() from None
        raise CheckpointUnknown() from None
    except _io.MarkerIssueUnknown:
        raise CheckpointIssueUnknown() from None
    except OSError:
        if write or entered:
            raise CheckpointIssueUnknown() from None
        raise CheckpointRefused() from None
    except (_io.MarkerInvalid, UnicodeError):
        if write and entered:
            raise CheckpointIssueUnknown() from None
        raise CheckpointRefused() from None


def _read_raw(parent: int, name: str, config: CheckpointConfig, *, durable: bool) -> bytes | None:
    try:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW
                             | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
    except FileNotFoundError:
        return None
    with _io._fd(descriptor):
        before = os.fstat(descriptor)
        _io._regular(before, config.io)
        raw = bytearray()
        while len(raw) <= config.io.max_bytes:
            part = os.read(descriptor, min(8192, config.io.max_bytes + 1 - len(raw)))
            if not part:
                break
            raw.extend(part)
        after = os.fstat(descriptor)
        named = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if (len(raw) > config.io.max_bytes
                or _io._fingerprint(before) != _io._fingerprint(after)
                or _io._fingerprint(after) != _io._fingerprint(named)):
            raise CheckpointRefused()
        if durable:
            os.fsync(descriptor)
            os.fsync(parent)
        return bytes(raw)


def _identity(content: InstallationCheckpointContent) -> tuple[object, ...]:
    return (content.format_version, content.installation_ref,
            content.database_target_ref, content.operation_id,
            content.plan_version, content.plan_sha256,
            content.correlation_id, content.causation_id,
            content.idempotency_key)


def read_checkpoint(config: CheckpointConfig) -> InstallationCheckpointContent:
    with _guard(config, write=False) as (parent, name):
        raw = _read_raw(parent, name, config, durable=False)
        if raw is None:
            raise CheckpointUnknown()
        return _decode(raw, config)


def publish_checkpoint(config: CheckpointConfig,
                       content: InstallationCheckpointContent) -> InstallationCheckpointContent:
    _config(config)
    expected = _encode(content, config)
    with _guard(config, write=True) as (parent, name):
        raw = _read_raw(parent, name, config, durable=False)
        if raw is not None:
            if raw == expected:
                verified = _read_raw(parent, name, config, durable=True)
                if verified is None or verified != expected:
                    raise CheckpointIssueUnknown()
                return _decode(verified, config)
            current = _decode(raw, config)
            if (_identity(current) != _identity(content)
                    or content.revision != current.revision + 1):
                raise CheckpointConflict()
            _io._publish(parent, name, expected, config.io)
        else:
            if content.revision != 1:
                raise CheckpointConflict()
            _io._publish(parent, name, expected, config.io)
        verified = _read_raw(parent, name, config, durable=True)
        if verified is None or verified != expected:
            raise CheckpointIssueUnknown()
        return _decode(verified, config)
