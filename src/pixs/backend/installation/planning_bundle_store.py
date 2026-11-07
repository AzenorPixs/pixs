"""Stockage prive immuable du seul PlanningBundle, sans autorite ni effet PG."""
from __future__ import annotations

import fcntl
import os
import stat
from contextlib import contextmanager
from dataclasses import dataclass

from pixs.backend.installation import marker as _io
from pixs.backend.installation.planning_bundle import (
    PlanningBundle,
    PlanningBundleError,
    PlanningBundleLimits,
    dump_planning_bundle,
    parse_planning_bundle,
    planning_bundle_sha256,
)

__all__ = [
    "PlanningBundleStoreRefused",
    "PlanningBundleStoreUnknown",
    "PlanningBundleStoreBusy",
    "PlanningBundleStoreConflict",
    "PlanningBundleStoreIssueUnknown",
    "PlanningBundleStoreConfig",
    "initialize_bundle_guard",
    "publish_bundle",
    "read_bundle",
]


class PlanningBundleStoreRefused(PlanningBundleError):
    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_BUNDLE_STORE_REFUSED"
        self.element = "planning_bundle_store"
        self.step = "store_planning_bundle"


class PlanningBundleStoreUnknown(PlanningBundleStoreRefused):
    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_BUNDLE_STORE_UNKNOWN"


class PlanningBundleStoreBusy(PlanningBundleStoreRefused):
    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_BUNDLE_STORE_BUSY"


class PlanningBundleStoreConflict(PlanningBundleStoreRefused):
    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_BUNDLE_STORE_CONFLICT"


class PlanningBundleStoreIssueUnknown(PlanningBundleStoreRefused):
    def __init__(self) -> None:
        super().__init__()
        self.code = "C08_BUNDLE_STORE_ISSUE_UNKNOWN"


@dataclass(frozen=True, slots=True, repr=False)
class PlanningBundleStoreConfig:
    io: _io.MarkerConfig
    lock_basename: str
    bundle_limits: PlanningBundleLimits

    def __post_init__(self) -> None:
        if type(self.io) is not _io.MarkerConfig:
            raise PlanningBundleStoreRefused()
        if type(self.bundle_limits) is not PlanningBundleLimits:
            raise PlanningBundleStoreRefused()
        try:
            self.io.__post_init__()
        except _io.MarkerIssueUnknown as e:
            raise PlanningBundleStoreIssueUnknown() from e
        except _io.MarkerInvalid as e:
            raise PlanningBundleStoreRefused() from e
        try:
            self.bundle_limits.__post_init__()
        except PlanningBundleError as e:
            if isinstance(e, PlanningBundleStoreRefused):
                raise
            raise PlanningBundleStoreRefused() from e
        name = self.lock_basename
        if type(name) is not str or not name:
            raise PlanningBundleStoreRefused()
        if name in (".", ".."):
            raise PlanningBundleStoreRefused()
        if "/" in name or not name.isprintable():
            raise PlanningBundleStoreRefused()
        if len(name) > self.io.max_ref_len:
            raise PlanningBundleStoreRefused()
        if name == os.path.basename(self.io.path):
            raise PlanningBundleStoreRefused()
        if self.io.max_bytes < self.bundle_limits.max_bundle_bytes:
            raise PlanningBundleStoreRefused()
        if "1.0.0" not in self.io.allowed_format_versions:
            raise PlanningBundleStoreRefused()


def _config(config: object) -> None:
    if type(config) is not PlanningBundleStoreConfig:
        raise PlanningBundleStoreRefused()
    try:
        config.__post_init__()
    except _io.MarkerIssueUnknown as e:
        raise PlanningBundleStoreIssueUnknown() from e
    except _io.MarkerInvalid as e:
        raise PlanningBundleStoreRefused() from e
    except PlanningBundleError as e:
        if isinstance(e, PlanningBundleStoreRefused):
            raise
        raise PlanningBundleStoreRefused() from e


def _lock_file(descriptor: int, config: PlanningBundleStoreConfig) -> None:
    current = os.fstat(descriptor)
    if not stat.S_ISREG(current.st_mode):
        raise PlanningBundleStoreRefused()
    if stat.S_IMODE(current.st_mode) != 0o600:
        raise PlanningBundleStoreRefused()
    if current.st_nlink != 1:
        raise PlanningBundleStoreRefused()
    if current.st_size != 0:
        raise PlanningBundleStoreRefused()
    if (current.st_uid, current.st_gid) != (
        config.io.owner_uid,
        config.io.owner_gid,
    ):
        raise PlanningBundleStoreRefused()


def initialize_bundle_guard(config: PlanningBundleStoreConfig) -> None:
    _config(config)
    try:
        parent, _ = _io._parent(config.io)
        with _io._fd(parent):
            try:
                descriptor = os.open(
                    config.lock_basename,
                    os.O_CREAT | os.O_EXCL | os.O_RDWR
                    | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                    0o600,
                    dir_fd=parent,
                )
            except FileExistsError:
                descriptor = os.open(
                    config.lock_basename,
                    os.O_RDONLY | os.O_NOFOLLOW
                    | os.O_NONBLOCK | os.O_CLOEXEC,
                    dir_fd=parent,
                )
            with _io._fd(descriptor):
                _lock_file(descriptor, config)
                current = os.fstat(descriptor)
                named = os.stat(
                    config.lock_basename,
                    dir_fd=parent,
                    follow_symlinks=False,
                )
                if _io._fingerprint(current) != _io._fingerprint(named):
                    raise PlanningBundleStoreRefused()
                os.fsync(descriptor)
                os.fsync(parent)
                current2 = os.fstat(descriptor)
                named2 = os.stat(
                    config.lock_basename,
                    dir_fd=parent,
                    follow_symlinks=False,
                )
                if _io._fingerprint(current2) != _io._fingerprint(named2):
                    raise PlanningBundleStoreIssueUnknown()
                if _io._fingerprint(current) != _io._fingerprint(current2):
                    raise PlanningBundleStoreIssueUnknown()
                _io._same_parent(config.io, parent)
    except FileNotFoundError as e:
        raise PlanningBundleStoreUnknown() from e
    except _io.MarkerIssueUnknown as e:
        raise PlanningBundleStoreIssueUnknown() from e
    except OSError as e:
        raise PlanningBundleStoreIssueUnknown() from e
    except (_io.MarkerInvalid, UnicodeError) as e:
        raise PlanningBundleStoreRefused() from e


@contextmanager
def _guard(config: PlanningBundleStoreConfig, *, write: bool):
    _config(config)
    try:
        parent, name = _io._parent(config.io)
        with _io._fd(parent):
            descriptor = os.open(
                config.lock_basename,
                os.O_RDONLY | os.O_NOFOLLOW
                | os.O_NONBLOCK | os.O_CLOEXEC,
                dir_fd=parent,
            )
            with _io._fd(descriptor):
                _lock_file(descriptor, config)
                try:
                    fcntl.flock(
                        descriptor,
                        (fcntl.LOCK_EX if write else fcntl.LOCK_SH)
                        | fcntl.LOCK_NB,
                    )
                except BlockingIOError as e:
                    raise PlanningBundleStoreBusy() from e
                before = os.fstat(descriptor)
                named = os.stat(
                    config.lock_basename,
                    dir_fd=parent,
                    follow_symlinks=False,
                )
                if _io._fingerprint(before) != _io._fingerprint(named):
                    raise PlanningBundleStoreRefused()
                yield parent, name
                try:
                    _io._same_parent(config.io, parent)
                except _io.MarkerIssueUnknown as e:
                    raise PlanningBundleStoreIssueUnknown() from e
                except (_io.MarkerInvalid, UnicodeError) as e:
                    if write:
                        raise PlanningBundleStoreIssueUnknown() from e
                    raise PlanningBundleStoreRefused() from e
                except FileNotFoundError as e:
                    if write:
                        raise PlanningBundleStoreIssueUnknown() from e
                    raise PlanningBundleStoreUnknown() from e
                except OSError as e:
                    if write:
                        raise PlanningBundleStoreIssueUnknown() from e
                    raise PlanningBundleStoreRefused() from e
                try:
                    after_named = os.stat(
                        config.lock_basename,
                        dir_fd=parent,
                        follow_symlinks=False,
                    )
                except FileNotFoundError as e:
                    if write:
                        raise PlanningBundleStoreIssueUnknown() from e
                    raise PlanningBundleStoreUnknown() from e
                except OSError as e:
                    if write:
                        raise PlanningBundleStoreIssueUnknown() from e
                    raise PlanningBundleStoreRefused() from e
                if _io._fingerprint(before) != _io._fingerprint(
                    after_named
                ):
                    if write:
                        raise PlanningBundleStoreIssueUnknown()
                    raise PlanningBundleStoreRefused()
    except FileNotFoundError as e:
        raise PlanningBundleStoreUnknown() from e
    except _io.MarkerIssueUnknown as e:
        raise PlanningBundleStoreIssueUnknown() from e
    except OSError as e:
        if write:
            raise PlanningBundleStoreIssueUnknown() from e
        raise PlanningBundleStoreRefused() from e
    except (_io.MarkerInvalid, UnicodeError) as e:
        raise PlanningBundleStoreRefused() from e


def _read_raw(
    parent: int,
    name: str,
    config: PlanningBundleStoreConfig,
    *,
    durable: bool,
) -> bytes | None:
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW
            | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=parent,
        )
    except FileNotFoundError:
        return None
    with _io._fd(descriptor):
        before = os.fstat(descriptor)
        try:
            _io._regular(before, config.io)
        except _io.MarkerIssueUnknown as e:
            raise PlanningBundleStoreIssueUnknown() from e
        except _io.MarkerInvalid as e:
            raise PlanningBundleStoreRefused() from e
        limit = config.bundle_limits.max_bundle_bytes
        raw = bytearray()
        while len(raw) <= limit:
            part = os.read(descriptor, min(8192, limit + 1 - len(raw)))
            if not part:
                break
            raw.extend(part)
        after = os.fstat(descriptor)
        named = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if len(raw) > limit:
            raise PlanningBundleStoreRefused()
        if _io._fingerprint(before) != _io._fingerprint(after):
            raise PlanningBundleStoreRefused()
        if _io._fingerprint(after) != _io._fingerprint(named):
            raise PlanningBundleStoreRefused()
        if durable:
            os.fsync(descriptor)
            os.fsync(parent)
            after2 = os.fstat(descriptor)
            named2 = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if _io._fingerprint(after2) != _io._fingerprint(named2):
                raise PlanningBundleStoreIssueUnknown()
            if _io._fingerprint(after) != _io._fingerprint(after2):
                raise PlanningBundleStoreIssueUnknown()
        return bytes(raw)


def read_bundle(config: PlanningBundleStoreConfig) -> PlanningBundle:
    with _guard(config, write=False) as (parent, name):
        raw = _read_raw(parent, name, config, durable=True)
        if raw is None:
            raise PlanningBundleStoreUnknown()
        try:
            return parse_planning_bundle(raw, config.bundle_limits)
        except PlanningBundleError as e:
            if isinstance(e, PlanningBundleStoreRefused):
                raise
            raise PlanningBundleStoreRefused() from e


def publish_bundle(
    config: PlanningBundleStoreConfig,
    bundle: PlanningBundle,
) -> str:
    _config(config)
    try:
        expected = dump_planning_bundle(bundle, config.bundle_limits)
    except PlanningBundleError as e:
        if isinstance(e, PlanningBundleStoreRefused):
            raise
        raise PlanningBundleStoreRefused() from e
    with _guard(config, write=True) as (parent, name):
        raw = _read_raw(parent, name, config, durable=False)
        if raw is not None:
            try:
                current = parse_planning_bundle(
                    raw, config.bundle_limits
                )
            except PlanningBundleError as e:
                if isinstance(e, PlanningBundleStoreRefused):
                    raise
                raise PlanningBundleStoreRefused() from e
            try:
                current_raw = dump_planning_bundle(
                    current, config.bundle_limits
                )
            except PlanningBundleError as e:
                if isinstance(e, PlanningBundleStoreRefused):
                    raise
                raise PlanningBundleStoreRefused() from e
            if current_raw != expected:
                raise PlanningBundleStoreConflict()
            try:
                verified = _read_raw(parent, name, config, durable=True)
            except _io.MarkerIssueUnknown as e:
                raise PlanningBundleStoreIssueUnknown() from e
            except (_io.MarkerInvalid, UnicodeError) as e:
                raise PlanningBundleStoreIssueUnknown() from e
            except OSError as e:
                raise PlanningBundleStoreIssueUnknown() from e
            except PlanningBundleError as e:
                if isinstance(e, PlanningBundleStoreIssueUnknown):
                    raise
                raise PlanningBundleStoreIssueUnknown() from e
            if verified is None:
                raise PlanningBundleStoreIssueUnknown()
            try:
                confirmed = parse_planning_bundle(
                    verified, config.bundle_limits
                )
            except PlanningBundleError as e:
                if isinstance(e, PlanningBundleStoreRefused):
                    raise PlanningBundleStoreIssueUnknown() from e
                raise PlanningBundleStoreIssueUnknown() from e
            try:
                confirmed_raw = dump_planning_bundle(
                    confirmed, config.bundle_limits
                )
            except PlanningBundleError as e:
                if isinstance(e, PlanningBundleStoreRefused):
                    raise PlanningBundleStoreIssueUnknown() from e
                raise PlanningBundleStoreIssueUnknown() from e
            if confirmed_raw != expected:
                raise PlanningBundleStoreIssueUnknown()
            try:
                return planning_bundle_sha256(
                    confirmed, config.bundle_limits
                )
            except PlanningBundleError as e:
                if isinstance(e, PlanningBundleStoreRefused):
                    raise PlanningBundleStoreIssueUnknown() from e
                raise PlanningBundleStoreIssueUnknown() from e
        try:
            _io._publish(parent, name, expected, config.io)
        except _io.MarkerIssueUnknown as e:
            raise PlanningBundleStoreIssueUnknown() from e
        except _io.MarkerInvalid as e:
            raise PlanningBundleStoreRefused() from e
        except OSError as e:
            raise PlanningBundleStoreIssueUnknown() from e
        try:
            verified = _read_raw(parent, name, config, durable=True)
        except _io.MarkerIssueUnknown as e:
            raise PlanningBundleStoreIssueUnknown() from e
        except (_io.MarkerInvalid, UnicodeError) as e:
            raise PlanningBundleStoreIssueUnknown() from e
        except OSError as e:
            raise PlanningBundleStoreIssueUnknown() from e
        except PlanningBundleError as e:
            if isinstance(e, PlanningBundleStoreIssueUnknown):
                raise
            raise PlanningBundleStoreIssueUnknown() from e
        if verified is None:
            raise PlanningBundleStoreIssueUnknown()
        try:
            confirmed = parse_planning_bundle(
                verified, config.bundle_limits
            )
        except PlanningBundleError as e:
            if isinstance(e, PlanningBundleStoreRefused):
                raise PlanningBundleStoreIssueUnknown() from e
            raise PlanningBundleStoreIssueUnknown() from e
        try:
            confirmed_raw = dump_planning_bundle(
                confirmed, config.bundle_limits
            )
        except PlanningBundleError as e:
            if isinstance(e, PlanningBundleStoreRefused):
                raise PlanningBundleStoreIssueUnknown() from e
            raise PlanningBundleStoreIssueUnknown() from e
        if confirmed_raw != expected:
            raise PlanningBundleStoreIssueUnknown()
        try:
            return planning_bundle_sha256(confirmed, config.bundle_limits)
        except PlanningBundleError as e:
            if isinstance(e, PlanningBundleStoreRefused):
                raise PlanningBundleStoreIssueUnknown() from e
            raise PlanningBundleStoreIssueUnknown() from e
