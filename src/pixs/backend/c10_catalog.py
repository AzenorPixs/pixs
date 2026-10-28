"""Catalogue initial C10 protégé, lecteur seul et garde filesystem réelle.

Le contrat de composition exige un ancrage et une liaison issus de la procédure
de publication préautorisée, indépendamment de PostgreSQL. Ni un digest, ni une
dataclass, ni la présence du fichier ne prouvent à eux seuls cette origine.
Ce module ne fournit pas l'éditeur, le port transactionnel ou C10 complet.
"""
from __future__ import annotations

import datetime as dt
import fcntl
import hashlib
import os
import stat
import threading
import time
import tomllib
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, fields
from typing import Callable

from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.kernel.data_governance_profile import DataGovernanceProfile, validate_data_governance_profile
from pixs.kernel.manifest.semver import parse_version

__all__ = ["CatalogInvalid", "CatalogUnknown", "CatalogBusy", "CatalogRevoked",
           "ProfileBinding", "CatalogConfig", "CatalogProfileEntry", "C10Catalog"]


class CatalogInvalid(ValueError):
    code = "C10_CATALOG_INVALID"

    def __init__(self) -> None:
        super().__init__("Catalogue initial de gouvernance refusé.")


class CatalogUnknown(CatalogInvalid):
    code = "C10_CATALOG_UNKNOWN"


class CatalogBusy(CatalogInvalid):
    code = "C10_CATALOG_BUSY"


class CatalogRevoked(CatalogInvalid):
    code = "C10_CATALOG_REVOKED"


def _ref(value: object, limit: int) -> None:
    if type(value) is not str or not 0 < len(value) <= limit or not value.isprintable():
        raise CatalogInvalid()


@dataclass(frozen=True, slots=True, repr=False)
class ProfileBinding:
    profile_ref: str
    data_asset_id: str
    owner_component: str
    source_of_truth: str
    profile_version: str


@dataclass(frozen=True, slots=True, repr=False)
class CatalogConfig:
    catalog_path: str
    guard_path: str
    owner_uid: int
    owner_gid: int
    parent_identities: tuple[tuple[int, int], ...]
    max_bytes: int
    max_ref_len: int
    max_profiles: int
    max_refs: int
    max_ttl_seconds: int
    max_freshness_seconds: int
    lock_timeout_ms: int
    retry_interval_ms: int
    expected_catalog_version: str
    expected_publication_ref: str
    expected_sha256: str
    binding: ProfileBinding

    def __post_init__(self) -> None:
        for path in (self.catalog_path, self.guard_path):
            if (type(path) is not str or not path.startswith("/") or "\x00" in path
                    or any(p in ("", ".", "..") for p in path.split("/")[1:])):
                raise CatalogInvalid()
        if (self.catalog_path == self.guard_path
                or os.path.dirname(self.catalog_path) != os.path.dirname(self.guard_path)):
            raise CatalogInvalid()
        for value in (self.owner_uid, self.owner_gid, self.lock_timeout_ms):
            if type(value) is not int or not 0 <= value <= 2**63 - 1:
                raise CatalogInvalid()
        for value in (self.max_bytes, self.max_ref_len, self.max_profiles,
                      self.max_refs, self.max_ttl_seconds,
                      self.max_freshness_seconds, self.retry_interval_ms):
            if type(value) is not int or not 1 <= value <= 2**63 - 1:
                raise CatalogInvalid()
        if self.lock_timeout_ms > 2**31 - 1 or self.retry_interval_ms > 2**31 - 1:
            raise CatalogInvalid()
        if type(self.parent_identities) is not tuple or not self.parent_identities:
            raise CatalogInvalid()
        for pair in self.parent_identities:
            if (type(pair) is not tuple or len(pair) != 2
                    or any(type(v) is not int or v < 0 for v in pair)):
                raise CatalogInvalid()
        for value in (self.expected_catalog_version, self.expected_publication_ref):
            _ref(value, self.max_ref_len)
        if (type(self.expected_sha256) is not str or len(self.expected_sha256) != 64
                or any(c not in "0123456789abcdef" for c in self.expected_sha256)):
            raise CatalogInvalid()
        if type(self.binding) is not ProfileBinding:
            raise CatalogInvalid()
        for field in fields(ProfileBinding):
            _ref(getattr(self.binding, field.name), self.max_ref_len)
        try:
            parse_version(self.binding.profile_version)
        except ValueError:
            raise CatalogInvalid() from None


@dataclass(frozen=True, slots=True, repr=False)
class CatalogProfileEntry:
    publication_ref: str
    catalog_version: str
    raw_sha256: str
    published_version: str
    resource_refs: tuple[str, ...]
    profile: DataGovernanceProfile


def _utc(value: object) -> dt.datetime:
    if type(value) is not dt.datetime or value.tzinfo is not dt.timezone.utc:
        raise CatalogInvalid()
    return value


def _fingerprint(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_uid, st.st_gid, st.st_nlink,
            st.st_size, st.st_mtime_ns, st.st_ctime_ns)


@contextmanager
def _fd(descriptor: int):
    try:
        yield descriptor
    finally:
        os.close(descriptor)


def _directory(st: os.stat_result, config: CatalogConfig, *, final: bool) -> None:
    if not stat.S_ISDIR(st.st_mode):
        raise CatalogInvalid()
    if final:
        if ((st.st_uid, st.st_gid) != (config.owner_uid, config.owner_gid)
                or stat.S_IMODE(st.st_mode) != 0o700):
            raise CatalogInvalid()
    else:
        if (st.st_uid, st.st_gid) not in config.parent_identities:
            raise CatalogInvalid()
        if st.st_mode & 0o002 and not (st.st_uid == 0 and st.st_mode & stat.S_ISVTX):
            raise CatalogInvalid()


def _parent(config: CatalogConfig) -> int:
    parts = [p for p in os.path.dirname(config.catalog_path).split("/") if p]
    with ExitStack() as stack:
        current = stack.enter_context(_fd(os.open(
            "/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)))
        _directory(os.fstat(current), config, final=not parts)
        for index, name in enumerate(parts):
            current = stack.enter_context(_fd(os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=current)))
            _directory(os.fstat(current), config, final=index == len(parts) - 1)
        return os.dup(current)


def _regular(st: os.stat_result, config: CatalogConfig, *, guard: bool) -> None:
    if (not stat.S_ISREG(st.st_mode) or stat.S_IMODE(st.st_mode) != 0o600
            or (st.st_uid, st.st_gid) != (config.owner_uid, config.owner_gid)
            or st.st_nlink != 1):
        raise CatalogInvalid()
    if guard and st.st_size != 0:
        raise CatalogInvalid()
    if not guard and not 0 < st.st_size <= config.max_bytes:
        raise CatalogInvalid()


def _references(raw: object, config: CatalogConfig, *, nonempty: bool) -> tuple[str, ...]:
    if type(raw) is not list or len(raw) > config.max_refs or (nonempty and not raw):
        raise CatalogInvalid()
    for ref in raw:
        _ref(ref, config.max_ref_len)
    if len(set(raw)) != len(raw):
        raise CatalogInvalid()
    return tuple(raw)


def _profile(raw: object, config: CatalogConfig) -> tuple[DataGovernanceProfile, tuple[str, ...], bool]:
    if type(raw) is not dict or set(raw) != {"published_version", "resource_refs", "revoked", "profile"}:
        raise CatalogInvalid()
    if type(raw["revoked"]) is not bool:
        raise CatalogInvalid()
    refs = _references(raw["resource_refs"], config, nonempty=True)
    profile = raw["profile"]
    if type(profile) is not dict or set(profile) != {f.name for f in fields(DataGovernanceProfile)}:
        raise CatalogInvalid()
    profile = dict(profile)
    collection_names = ("data_classes", "purpose_refs", "residency_constraints",
                        "authorized_consumers", "processor_refs")
    for name in collection_names:
        profile[name] = frozenset(_references(profile[name], config, nonempty=False))
    for name in ("profile_version", "data_asset_id", "owner_component", "source_of_truth",
                 "retention_policy", "deletion_policy", "export_policy", "lineage",
                 "confidentiality", "personal_data"):
        _ref(profile[name], config.max_ref_len)
    try:
        profile["confidentiality"] = ConfidentialityLevel(profile["confidentiality"])
        profile["personal_data"] = PersonalDataLevel(profile["personal_data"])
        result = DataGovernanceProfile(**profile)
    except ValueError:
        raise CatalogInvalid() from None
    if validate_data_governance_profile(result):
        raise CatalogInvalid()
    if type(raw["published_version"]) is not str or raw["published_version"] != result.profile_version:
        raise CatalogInvalid()
    return result, refs, raw["revoked"]


class _Lease:
    """Capacité locale admise par le contexte, sans constructeur RPC."""
    def __init__(self, owner: C10Catalog, parent: int, guard: int):
        self.owner, self.parent, self.guard = owner, parent, guard
        self.pid, self.thread = os.getpid(), threading.get_ident()
        self.guard_fingerprint = _fingerprint(os.fstat(guard))

    def profile(self) -> CatalogProfileEntry:
        return self.owner._profile(self)


class C10Catalog:
    def __init__(self, config: CatalogConfig, *, now: Callable[[], dt.datetime]):
        if type(config) is not CatalogConfig or not callable(now):
            raise CatalogInvalid()
        config.__post_init__()
        self.config, self.now = config, now
        self._lease: _Lease | None = None
        self._admission = threading.Lock()

    @contextmanager
    def guard(self):
        if not self._admission.acquire(blocking=False):
            raise CatalogBusy()
        try:
            yield from self._guarded()
        finally:
            self._admission.release()

    def _guarded(self):
        if self._lease is not None:
            raise CatalogBusy()
        config = self.config
        config.__post_init__()
        try:
            with ExitStack() as stack:
                parent = stack.enter_context(_fd(_parent(config)))
                descriptor = stack.enter_context(_fd(os.open(
                    os.path.basename(config.guard_path),
                    os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                    dir_fd=parent)))
                _regular(os.fstat(descriptor), config, guard=True)
                deadline = time.monotonic() + config.lock_timeout_ms / 1000
                while True:
                    try:
                        fcntl.flock(descriptor, fcntl.LOCK_SH | fcntl.LOCK_NB)
                        break
                    except BlockingIOError:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise CatalogBusy() from None
                        time.sleep(min(config.retry_interval_ms / 1000, remaining))
                lease = _Lease(self, parent, descriptor)
                self._lease = lease
                try:
                    self._check(lease)
                    yield lease
                finally:
                    self._lease = None
                    # La fermeture du descripteur libère la garde, y compris
                    # en cas de rollback ou d'exception de la composition.
        except FileNotFoundError:
            raise CatalogUnknown() from None
        except OSError:
            raise CatalogInvalid() from None

    def _check(self, lease: _Lease) -> None:
        if (self._lease is not lease or type(lease) is not _Lease or lease.owner is not self
                or lease.pid != os.getpid() or lease.thread != threading.get_ident()):
            raise CatalogInvalid()
        config = self.config
        config.__post_init__()
        parent = os.fstat(lease.parent)
        _directory(parent, config, final=True)
        guard = os.fstat(lease.guard)
        named = os.stat(os.path.basename(config.guard_path), dir_fd=lease.parent,
                        follow_symlinks=False)
        _regular(guard, config, guard=True)
        if (_fingerprint(guard) != lease.guard_fingerprint
                or _fingerprint(named) != lease.guard_fingerprint):
            raise CatalogInvalid()
        with _fd(_parent(config)) as fresh:
            observed = os.fstat(fresh)
            if (parent.st_dev, parent.st_ino) != (observed.st_dev, observed.st_ino):
                raise CatalogInvalid()

    def _read(self, lease: _Lease) -> bytes:
        self._check(lease)
        config = self.config
        with _fd(os.open(os.path.basename(config.catalog_path),
                         os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                         dir_fd=lease.parent)) as descriptor:
            before = os.fstat(descriptor)
            _regular(before, config, guard=False)
            raw = bytearray()
            while len(raw) <= config.max_bytes:
                part = os.read(descriptor, min(8192, config.max_bytes + 1 - len(raw)))
                if not part:
                    break
                raw.extend(part)
            after = os.fstat(descriptor)
            named = os.stat(os.path.basename(config.catalog_path), dir_fd=lease.parent,
                            follow_symlinks=False)
            if (len(raw) > config.max_bytes or _fingerprint(before) != _fingerprint(after)
                    or _fingerprint(after) != _fingerprint(named)):
                raise CatalogInvalid()
        self._check(lease)
        return bytes(raw)

    def _profile(self, lease: _Lease) -> CatalogProfileEntry:
        try:
            raw = self._read(lease)
            config = self.config
            digest = hashlib.sha256(raw).hexdigest()
            if digest != config.expected_sha256:
                raise CatalogInvalid()
            document = tomllib.loads(raw.decode("utf-8"))
            if type(document) is not dict or set(document) != {"catalog", "profiles"}:
                raise CatalogInvalid()
            header = document["catalog"]
            keys = {"schema_version", "catalog_version", "publication_ref",
                    "valid_from", "valid_until", "published_at", "revoked"}
            if type(header) is not dict or set(header) != keys:
                raise CatalogInvalid()
            if (type(header["schema_version"]) is not str or header["schema_version"] != "1.0.0"
                    or type(header["revoked"]) is not bool):
                raise CatalogInvalid()
            if header["revoked"]:
                raise CatalogRevoked()
            if (header["catalog_version"] != config.expected_catalog_version
                    or header["publication_ref"] != config.expected_publication_ref):
                raise CatalogInvalid()
            start, until, published = (_utc(header[k]) for k in
                                        ("valid_from", "valid_until", "published_at"))
            now = _utc(self.now())
            if not start <= published <= now < until:
                raise CatalogInvalid()
            if ((until - start).total_seconds() > config.max_ttl_seconds
                    or (now - published).total_seconds() > config.max_freshness_seconds):
                raise CatalogInvalid()
            profiles = document["profiles"]
            if type(profiles) is not dict or not 0 < len(profiles) <= config.max_profiles:
                raise CatalogInvalid()
            selected = None
            for ref, value in profiles.items():
                _ref(ref, config.max_ref_len)
                profile, refs, revoked = _profile(value, config)
                if ref == config.binding.profile_ref:
                    selected = (profile, refs, revoked)
            if selected is None:
                raise CatalogUnknown()
            profile, refs, revoked = selected
            if revoked:
                raise CatalogRevoked()
            for name in ("data_asset_id", "owner_component", "source_of_truth", "profile_version"):
                if getattr(profile, name) != getattr(config.binding, name):
                    raise CatalogInvalid()
            self._check(lease)
            return CatalogProfileEntry(header["publication_ref"], header["catalog_version"],
                                       digest, profile.profile_version, refs, profile)
        except FileNotFoundError:
            raise CatalogUnknown() from None
        except (OSError, UnicodeError, ValueError, RecursionError) as error:
            if isinstance(error, CatalogInvalid):
                raise
            raise CatalogInvalid() from None
