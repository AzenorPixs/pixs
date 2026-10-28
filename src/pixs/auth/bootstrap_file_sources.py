"""Sources publiques R01 lues depuis des publications protégées, sans autorité.

La composition fournit les configurations depuis la procédure de préautorisation.
Ce module ne la réalise pas, ne crée aucun fichier et ne garantit aucun ancrage
anti-restauration. Une empreinte ou un fichier ne publie jamais sa propre confiance.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import os
import posixpath
import re
import stat
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, fields

from pixs.auth.r01 import (
    AuthBootstrapError, BootstrapTrustKey, BootstrapTrustPolicy, SignedBootstrapProof,
    canonical_bootstrap_bytes)
from pixs.core.bootstrap_operator import BootstrapOperatorFacts, BootstrapOperatorError
from pixs.core.ports import CorePortError
from pixs.core.scope.context import (
    ScopeContext, ScopeType, ScopeStructureError, validate_structure)

__all__ = ["BootstrapFileSourceError", "ProtectedSourceFile", "FileProofSourceConfig",
           "FileTrustSourceConfig", "FileProofSource", "FileTrustSource"]
_DOMAIN = b"pixs.bootstrap.r01.v1\0"
_SCHEMA = "pixs.bootstrap.canonical.v1"
_POLICY_SCHEMA = "pixs.auth.bootstrap-trust.v1"
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z")


class BootstrapFileSourceError(CorePortError):
    def __init__(self):
        ValueError.__init__(self, "Source fichier R01 non vérifiable.")
        self.code = "AUTH_FILE_SOURCE_INVALID"
        self.element = "auth_file_source"
        self.step = "read_auth_file_source"


def _fail():
    raise BootstrapFileSourceError()


def _text(value):
    if type(value) is not str or not 0 < len(value) <= 1024 or not value.isprintable():
        _fail()


def _hash(value):
    if (type(value) is not str or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value)):
        _fail()


def _identity_pair(value):
    if (type(value) is not tuple or len(value) != 2
            or any(type(n) is not int or n < 0 for n in value)):
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class ProtectedSourceFile:
    path: str
    expected_sha256: str
    owner_uid: int
    owner_gid: int
    directory_uid: int
    directory_gid: int
    parent_identities: tuple[tuple[int, int], ...]
    max_bytes: int

    def __post_init__(self):
        if (type(self.path) is not str or not self.path.startswith("/")
                or not self.path.isprintable() or posixpath.normpath(self.path) != self.path
                or any(part in ("", ".", "..") for part in self.path.split("/")[1:])):
            _fail()
        _hash(self.expected_sha256)
        for value in (self.owner_uid, self.owner_gid, self.directory_uid, self.directory_gid):
            if type(value) is not int or value < 0:
                _fail()
        if type(self.max_bytes) is not int or self.max_bytes < 1:
            _fail()
        if type(self.parent_identities) is not tuple or not self.parent_identities:
            _fail()
        for pair in self.parent_identities:
            _identity_pair(pair)


@dataclass(frozen=True, slots=True, repr=False)
class FileProofSourceConfig:
    message: ProtectedSourceFile
    signature: ProtectedSourceFile
    proof_ref: str
    challenge_sha256: str

    def __post_init__(self):
        if type(self.message) is not ProtectedSourceFile or type(self.signature) is not ProtectedSourceFile:
            _fail()
        self.message.__post_init__()
        self.signature.__post_init__()
        _text(self.proof_ref)
        _hash(self.challenge_sha256)
        if (self.message.path == self.signature.path
                or self.message.max_bytes > 128 * 1024
                or self.signature.max_bytes != 64
                or self.message.expected_sha256 != self.challenge_sha256):
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class FileTrustSourceConfig:
    policy: ProtectedSourceFile
    policy_ref: str
    policy_version: str
    publication_ref: str
    max_keys: int

    def __post_init__(self):
        if type(self.policy) is not ProtectedSourceFile:
            _fail()
        self.policy.__post_init__()
        for value in (self.policy_ref, self.policy_version, self.publication_ref):
            _text(value)
        if type(self.max_keys) is not int or self.max_keys < 1:
            _fail()


@contextmanager
def _descriptor(fd):
    try:
        yield fd
    finally:
        try:
            os.close(fd)
        except OSError:
            raise BootstrapFileSourceError() from None


def _fingerprint(value):
    return (value.st_dev, value.st_ino, value.st_mode, value.st_uid, value.st_gid,
            value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def _directory(value, config, *, final):
    if not stat.S_ISDIR(value.st_mode):
        _fail()
    if final:
        if ((value.st_uid, value.st_gid) != (config.directory_uid, config.directory_gid)
                or stat.S_IMODE(value.st_mode) != 0o700):
            _fail()
    else:
        if (value.st_uid, value.st_gid) not in config.parent_identities:
            _fail()
        if value.st_mode & 0o002 and not (value.st_uid == 0 and value.st_mode & stat.S_ISVTX):
            _fail()


def _parent(config, stack):
    names = config.path.split("/")[1:]
    current = stack.enter_context(_descriptor(os.open(
        "/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)))
    _directory(os.fstat(current), config, final=len(names) == 1)
    for index, name in enumerate(names[:-1]):
        current = stack.enter_context(_descriptor(os.open(
            name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=current)))
        _directory(os.fstat(current), config, final=index == len(names) - 2)
    return current, names[-1]


def _regular(value, config):
    if (not stat.S_ISREG(value.st_mode) or stat.S_IMODE(value.st_mode) != 0o600
            or (value.st_uid, value.st_gid) != (config.owner_uid, config.owner_gid)
            or value.st_nlink != 1 or not 0 < value.st_size <= config.max_bytes):
        _fail()


def _read(config):
    if type(config) is not ProtectedSourceFile:
        _fail()
    config.__post_init__()
    try:
        with ExitStack() as stack:
            parent, name = _parent(config, stack)
            parent_before = _fingerprint(os.fstat(parent))
            before_path = os.stat(name, dir_fd=parent, follow_symlinks=False)
            _regular(before_path, config)
            fd = stack.enter_context(_descriptor(os.open(
                name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
                dir_fd=parent)))
            before = os.fstat(fd)
            _regular(before, config)
            if _fingerprint(before_path) != _fingerprint(before):
                _fail()
            chunks, remaining = [], config.max_bytes + 1
            while remaining:
                chunk = os.read(fd, min(65536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b"".join(chunks)
            if len(data) != before.st_size or len(data) > config.max_bytes:
                _fail()
            after = os.fstat(fd)
            _regular(after, config)
            # Refaire le parcours absolu : un ancien parent ouvert ne prouve pas
            # que le chemin courant désigne encore cette publication.
            current_parent, current_name = _parent(config, stack)
            current = os.stat(current_name, dir_fd=current_parent, follow_symlinks=False)
            _regular(current, config)
            if (parent_before != _fingerprint(os.fstat(current_parent))
                    or _fingerprint(before) != _fingerprint(after)
                    or _fingerprint(before) != _fingerprint(current)
                    or not hmac.compare_digest(hashlib.sha256(data).hexdigest(),
                                               config.expected_sha256)):
                _fail()
            return data
    except OSError:
        raise BootstrapFileSourceError() from None


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail()
        result[key] = value
    return result


def _number(_):
    _fail()


def _json(data):
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_int=_number, parse_float=_number, parse_constant=_number)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError):
        raise BootstrapFileSourceError() from None
    if type(value) is not dict:
        _fail()
    return value


def _object(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        _fail()
    return value


def _date(value):
    if type(value) is not str or _DATE.fullmatch(value) is None:
        _fail()
    try:
        return dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        raise BootstrapFileSourceError() from None


def _hex32(value):
    _hash(value)
    return bytes.fromhex(value)


def _facts(document):
    names = {f.name for f in fields(BootstrapOperatorFacts)} - {"consumed_operation_id"}
    data = dict(_object(document, names))
    context = _object(data["context"], ("scope_type", "tenant_id", "scope_id"))
    if (type(context["scope_type"]) is not str or context["scope_type"] != "PLATFORM"
            or context["tenant_id"] is not None or context["scope_id"] is not None):
        _fail()
    data["context"] = ScopeContext(ScopeType.PLATFORM)
    try:
        validate_structure(data["context"])
        for key in ("authorized_actions", "closed_effects"):
            if type(data[key]) is not list:
                _fail()
            data[key] = tuple(data[key])
        for key in ("valid_from", "expires_at"):
            data[key] = _date(data[key])
        data["consumed_operation_id"] = None
        facts = BootstrapOperatorFacts(**data)
        facts.__post_init__()
        return facts
    except (BootstrapOperatorError, ScopeStructureError):
        raise BootstrapFileSourceError() from None


class FileProofSource:
    def __init__(self, config: FileProofSourceConfig):
        if type(config) is not FileProofSourceConfig:
            _fail()
        config.__post_init__()
        self._config = config

    def resolve(self, proof_ref: str) -> SignedBootstrapProof:
        config = self._config
        config.__post_init__()
        if type(proof_ref) is not str or proof_ref != config.proof_ref:
            _fail()
        message = _read(config.message)
        signature = _read(config.signature)
        if not message.startswith(_DOMAIN) or len(signature) != 64:
            _fail()
        document = _object(_json(message[len(_DOMAIN):]), ("schema", "facts", "nonce"))
        if type(document["schema"]) is not str or document["schema"] != _SCHEMA:
            _fail()
        facts, nonce = _facts(document["facts"]), _hex32(document["nonce"])
        try:
            if (facts.operator_proof_ref != proof_ref
                    or canonical_bootstrap_bytes(facts, nonce) != message):
                _fail()
            result = SignedBootstrapProof(facts, nonce, signature)
            result.__post_init__()
        except (AuthBootstrapError, BootstrapOperatorError):
            raise BootstrapFileSourceError() from None
        return result


class FileTrustSource:
    def __init__(self, config: FileTrustSourceConfig):
        if type(config) is not FileTrustSourceConfig:
            _fail()
        config.__post_init__()
        self._config = config

    def resolve(self, version: str) -> BootstrapTrustPolicy:
        config = self._config
        config.__post_init__()
        if type(version) is not str or version != config.policy_version:
            _fail()
        document = _object(_json(_read(config.policy)),
                           ("schema", "policy_ref", "publication_ref", "policy"))
        if (type(document["schema"]) is not str or document["schema"] != _POLICY_SCHEMA
                or document["policy_ref"] != config.policy_ref
                or document["publication_ref"] != config.publication_ref):
            _fail()
        policy = _object(document["policy"], ("version", "keys"))
        if type(policy["version"]) is not str or policy["version"] != version:
            _fail()
        raw_keys = policy["keys"]
        if type(raw_keys) is not list or not 0 < len(raw_keys) <= config.max_keys:
            _fail()
        keys = []
        names = ("key_id", "operator_subject_ref", "installation_ref", "authorized_actions",
                 "public_key_hex", "valid_from", "valid_until", "revoked")
        try:
            for raw in raw_keys:
                data = _object(raw, names)
                actions = data["authorized_actions"]
                if type(actions) is not list or type(data["revoked"]) is not bool:
                    _fail()
                key = BootstrapTrustKey(
                    data["key_id"], data["operator_subject_ref"], data["installation_ref"],
                    tuple(actions), _hex32(data["public_key_hex"]),
                    _date(data["valid_from"]), _date(data["valid_until"]), data["revoked"])
                key.__post_init__()
                keys.append(key)
            result = BootstrapTrustPolicy(version, tuple(keys))
            result.__post_init__()
        except AuthBootstrapError:
            raise BootstrapFileSourceError() from None
        return result
