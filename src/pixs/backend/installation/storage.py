"""Stockage privé immuable du plan C08, sans autorité ni effet PostgreSQL.

La garde native et le répertoire appartiennent à la configuration protégée.
Publier un plan ne confirme pas son exécution et ne sélectionne aucun mode.
"""
from __future__ import annotations

import fcntl
import os
import stat
from contextlib import contextmanager
from dataclasses import dataclass

from pixs.backend.installation import marker as _io
from pixs.backend.installation.plan import (
    InstallationPlan, PlanInvalid, PlanLimits, canonical_plan_bytes, parse_plan_bytes,
    plan_sha256)

__all__ = ["PlanStoreConfig", "PlanStoreRefused", "PlanStoreUnknown", "PlanStoreBusy",
           "PlanStoreConflict", "PlanStoreIssueUnknown", "initialize_plan_guard", "publish_plan", "read_plan"]


class PlanStoreRefused(PlanInvalid):
    code = "C08_PLAN_STORE_REFUSED"


class PlanStoreUnknown(PlanStoreRefused):
    code = "C08_PLAN_STORE_UNKNOWN"


class PlanStoreBusy(PlanStoreRefused):
    code = "C08_PLAN_STORE_BUSY"


class PlanStoreConflict(PlanStoreRefused):
    code = "C08_PLAN_STORE_CONFLICT"


class PlanStoreIssueUnknown(PlanStoreRefused):
    code = "C08_PLAN_STORE_ISSUE_UNKNOWN"


@dataclass(frozen=True, slots=True, repr=False)
class PlanStoreConfig:
    """io protège ce fichier plan, sans réutiliser la configuration du marqueur."""

    io: _io.MarkerConfig
    lock_basename: str
    limits: PlanLimits

    def __post_init__(self) -> None:
        if type(self.io) is not _io.MarkerConfig or type(self.limits) is not PlanLimits:
            raise PlanStoreRefused()
        self.io.__post_init__()
        self.limits.__post_init__()
        name = self.lock_basename
        if (type(name) is not str or not name or name in (".", "..")
                or "/" in name or not name.isprintable()
                or len(name) > self.io.max_ref_len
                or name == os.path.basename(self.io.path)):
            raise PlanStoreRefused()
        if (self.io.max_bytes != self.limits.max_bytes
                or self.io.max_ref_len != self.limits.max_ref_len
                or self.io.allowed_format_versions != self.limits.allowed_schema_versions):
            raise PlanStoreRefused()


def _config(config: object) -> None:
    if type(config) is not PlanStoreConfig:
        raise PlanStoreRefused()
    try:
        config.__post_init__()
    except _io.MarkerInvalid:
        raise PlanStoreRefused() from None


def _lock_file(descriptor: int, config: PlanStoreConfig) -> None:
    current = os.fstat(descriptor)
    if (not stat.S_ISREG(current.st_mode) or stat.S_IMODE(current.st_mode) != 0o600
            or current.st_nlink != 1 or current.st_size != 0
            or (current.st_uid, current.st_gid) != (config.io.owner_uid, config.io.owner_gid)):
        raise PlanStoreRefused()


def initialize_plan_guard(config: PlanStoreConfig) -> None:
    """Crée seulement la garde privée de métadonnées ; aucun pouvoir d'installation."""
    _config(config)
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
            with _io._fd(descriptor):
                _lock_file(descriptor, config)
                current = os.fstat(descriptor)
                named = os.stat(config.lock_basename, dir_fd=parent, follow_symlinks=False)
                if _io._fingerprint(current) != _io._fingerprint(named):
                    raise PlanStoreRefused()
                os.fsync(descriptor)
                os.fsync(parent)
                _io._same_parent(config.io, parent)
    except FileNotFoundError:
        raise PlanStoreUnknown() from None
    except (_io.MarkerIssueUnknown, OSError):
        raise PlanStoreIssueUnknown() from None
    except (_io.MarkerInvalid, UnicodeError):
        raise PlanStoreRefused() from None


@contextmanager
def _guard(config: PlanStoreConfig, *, write: bool):
    _config(config)
    try:
        parent, name = _io._parent(config.io)
        with _io._fd(parent):
            descriptor = os.open(
                config.lock_basename, os.O_RDONLY | os.O_NOFOLLOW
                | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
            with _io._fd(descriptor):
                _lock_file(descriptor, config)
                try:
                    fcntl.flock(descriptor, (fcntl.LOCK_EX if write else fcntl.LOCK_SH)
                                | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise PlanStoreBusy() from None
                before = os.fstat(descriptor)
                named = os.stat(config.lock_basename, dir_fd=parent, follow_symlinks=False)
                if _io._fingerprint(before) != _io._fingerprint(named):
                    raise PlanStoreRefused()
                yield parent, name
                _io._same_parent(config.io, parent)
                named = os.stat(config.lock_basename, dir_fd=parent, follow_symlinks=False)
                if _io._fingerprint(before) != _io._fingerprint(named):
                    raise PlanStoreRefused()
    except FileNotFoundError:
        raise PlanStoreUnknown() from None
    except _io.MarkerIssueUnknown:
        raise PlanStoreIssueUnknown() from None
    except OSError:
        if write:
            raise PlanStoreIssueUnknown() from None
        raise PlanStoreRefused() from None
    except (_io.MarkerInvalid, UnicodeError):
        raise PlanStoreRefused() from None


def _read_raw(parent: int, name: str, config: PlanStoreConfig, *, durable: bool) -> bytes | None:
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
            raise PlanStoreRefused()
        if durable:
            os.fsync(descriptor)
            os.fsync(parent)
        return bytes(raw)


def read_plan(config: PlanStoreConfig) -> InstallationPlan:
    with _guard(config, write=False) as (parent, name):
        raw = _read_raw(parent, name, config, durable=False)
        if raw is None:
            raise PlanStoreUnknown()
        return parse_plan_bytes(raw, config.limits)


def publish_plan(config: PlanStoreConfig, plan: InstallationPlan) -> str:
    _config(config)
    expected = canonical_plan_bytes(plan, config.limits)
    with _guard(config, write=True) as (parent, name):
        raw = _read_raw(parent, name, config, durable=False)
        if raw is not None:
            current = parse_plan_bytes(raw, config.limits)
            if canonical_plan_bytes(current, config.limits) != expected:
                raise PlanStoreConflict()
        else:
            _io._publish(parent, name, expected, config.io)
        verified = _read_raw(parent, name, config, durable=True)
        if verified is None:
            raise PlanStoreRefused()
        confirmed = parse_plan_bytes(verified, config.limits)
        if canonical_plan_bytes(confirmed, config.limits) != expected:
            raise PlanStoreRefused()
        return plan_sha256(confirmed, config.limits)
