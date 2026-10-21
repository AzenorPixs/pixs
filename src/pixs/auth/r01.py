"""Profil R01 v1 : signature seule, sans PG, consommation ni preuve de commit.

expected_facts, challenge et politique doivent venir de ports serveur protégés,
jamais du corps appelant. La forme d'un DTO ne prouve aucune confiance.
Les chaînes du profil sont bornées à 1024 caractères et le message à 128 Kio.
"""
from __future__ import annotations

import datetime
import hashlib
import hmac
import json
from dataclasses import dataclass, fields, replace

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from pixs.core.bootstrap_operator import (
    BOOTSTRAP_ACTION, BOOTSTRAP_EFFECTS, BootstrapOperatorError,
    BootstrapOperatorFacts, validate_bootstrap_window_current,
)
from pixs.core.scope.context import ScopeContext
from pixs.kernel.manifest.semver import parse_version

_DOMAIN = b"pixs.bootstrap.r01.v1\0"
_SCHEMA = "pixs.bootstrap.canonical.v1"
_CORE_FIELDS = frozenset((
    "operator_subject_ref", "resource_id", "action_id", "context",
    "installation_ref", "plan_version", "authorized_actions", "closed_effects",
    "operator_proof_ref", "authorization_ref", "operation_id", "target_identity_ref",
    "target_tenant_ref", "plan_sha256", "valid_from", "expires_at", "key_id",
    "trust_policy_version", "consumed_operation_id",
))


class AuthBootstrapError(ValueError):
    def __init__(self) -> None:
        super().__init__("Preuve R01 invalide.")
        self.code = "AUTH_BOOTSTRAP_INVALID"
        self.element = "auth_bootstrap"
        self.step = "validate_bootstrap"


def _field(value: object, name: str):
    try:
        return object.__getattribute__(value, name)
    except AttributeError:
        raise AuthBootstrapError() from None


def _text(value: object) -> str:
    if type(value) is not str or not value or len(value) > 1024:
        raise AuthBootstrapError()
    return value


def _utc(value: object) -> None:
    if type(value) is not datetime.datetime or value.tzinfo is not datetime.timezone.utc:
        raise AuthBootstrapError()


def _bytes(value: object, length: int) -> None:
    if type(value) is not bytes or len(value) != length:
        raise AuthBootstrapError()


def _facts(value: object, *, allow_consumed: bool = False) -> BootstrapOperatorFacts:
    if type(value) is not BootstrapOperatorFacts:
        raise AuthBootstrapError()
    if {f.name for f in fields(BootstrapOperatorFacts)} != _CORE_FIELDS:
        raise AuthBootstrapError()
    for name in _CORE_FIELDS:
        item = _field(value, name)
        if name == "context":
            if type(item) is not ScopeContext:
                raise AuthBootstrapError()
        elif name in ("valid_from", "expires_at"):
            _utc(item)
        elif name in ("authorized_actions", "closed_effects"):
            if type(item) is not tuple or len(item) > len(BOOTSTRAP_EFFECTS):
                raise AuthBootstrapError()
            for part in item:
                _text(part)
        elif name in ("target_tenant_ref", "consumed_operation_id"):
            if item is not None:
                _text(item)
            if name == "consumed_operation_id" and item is not None and not allow_consumed:
                raise AuthBootstrapError()
        else:
            _text(item)
    try:
        value.__post_init__()
    except (BootstrapOperatorError, AttributeError):
        raise AuthBootstrapError() from None
    return value


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapTrustKey:
    key_id: str
    operator_subject_ref: str
    installation_ref: str
    authorized_actions: tuple[str, ...]
    public_key: bytes
    valid_from: datetime.datetime
    valid_until: datetime.datetime
    revoked: bool

    def __post_init__(self) -> None:
        for name in ("key_id", "operator_subject_ref", "installation_ref"):
            _text(_field(self, name))
        actions = _field(self, "authorized_actions")
        if (type(actions) is not tuple or len(actions) != 1
                or type(actions[0]) is not str or actions[0] != BOOTSTRAP_ACTION):
            raise AuthBootstrapError()
        _bytes(_field(self, "public_key"), 32)
        start, end = _field(self, "valid_from"), _field(self, "valid_until")
        _utc(start)
        _utc(end)
        if not start < end or type(_field(self, "revoked")) is not bool:
            raise AuthBootstrapError()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapTrustPolicy:
    version: str
    keys: tuple[BootstrapTrustKey, ...]

    def __post_init__(self) -> None:
        version = _text(_field(self, "version"))
        try:
            parse_version(version)
        except ValueError:
            raise AuthBootstrapError() from None
        keys = _field(self, "keys")
        if type(keys) is not tuple or not keys:
            raise AuthBootstrapError()
        seen: set[str] = set()
        for key in keys:
            if type(key) is not BootstrapTrustKey:
                raise AuthBootstrapError()
            key.__post_init__()
            if key.key_id in seen:
                raise AuthBootstrapError()
            seen.add(key.key_id)


@dataclass(frozen=True, slots=True, repr=False)
class SignedBootstrapProof:
    facts: BootstrapOperatorFacts
    nonce: bytes
    signature: bytes

    def __post_init__(self) -> None:
        _facts(_field(self, "facts"))
        _bytes(_field(self, "nonce"), 32)
        _bytes(_field(self, "signature"), 64)


def canonical_bootstrap_bytes(facts: BootstrapOperatorFacts, nonce: bytes) -> bytes:
    """Codec fermé ; la consommation courante est exclusivement serveur."""
    _facts(facts)
    _bytes(nonce, 32)
    payload = {}
    for name in sorted(_CORE_FIELDS - {"consumed_operation_id"}):
        value = _field(facts, name)
        if name == "context":
            value = {"scope_type": value.scope_type.value,
                     "tenant_id": value.tenant_id, "scope_id": value.scope_id}
        elif name in ("valid_from", "expires_at"):
            value = value.isoformat(timespec="microseconds").replace("+00:00", "Z")
        elif name in ("authorized_actions", "closed_effects"):
            value = list(value)
        payload[name] = value
    document = {"schema": _SCHEMA, "facts": payload, "nonce": nonce.hex()}
    encoded = _DOMAIN + json.dumps(document, sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=True, allow_nan=False).encode("ascii")
    if len(encoded) > 128 * 1024:
        raise AuthBootstrapError()
    return encoded


def bootstrap_challenge_sha256(facts: BootstrapOperatorFacts, nonce: bytes) -> str:
    return hashlib.sha256(canonical_bootstrap_bytes(facts, nonce)).hexdigest()


def verify_signed_bootstrap(
    proof: SignedBootstrapProof, expected_facts: BootstrapOperatorFacts,
    expected_challenge_sha256: str, policy: BootstrapTrustPolicy,
    now: datetime.datetime,
) -> BootstrapOperatorFacts:
    """Retourne les faits serveur vérifiés, jamais une autorisation de second effet.

    Consommation par la même opération : inspection confirmée C08 seulement.
    La primitive ne prouve ni origine des entrées protégées ni commit durable.
    """
    if type(proof) is not SignedBootstrapProof or type(policy) is not BootstrapTrustPolicy:
        raise AuthBootstrapError()
    proof.__post_init__()
    policy.__post_init__()
    _facts(expected_facts, allow_consumed=True)
    _utc(now)
    digest = _text(expected_challenge_sha256)
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise AuthBootstrapError()
    consumed = expected_facts.consumed_operation_id
    if consumed is not None and consumed != expected_facts.operation_id:
        raise AuthBootstrapError()
    try:
        validate_bootstrap_window_current(expected_facts, now)
    except (BootstrapOperatorError, AttributeError):
        raise AuthBootstrapError() from None
    if policy.version != expected_facts.trust_policy_version:
        raise AuthBootstrapError()
    unsigned = replace(expected_facts, consumed_operation_id=None)
    expected = canonical_bootstrap_bytes(unsigned, proof.nonce)
    provided = canonical_bootstrap_bytes(proof.facts, proof.nonce)
    if not hmac.compare_digest(expected, provided):
        raise AuthBootstrapError()
    if not hmac.compare_digest(hashlib.sha256(expected).hexdigest(), digest):
        raise AuthBootstrapError()
    candidates = [key for key in policy.keys if key.key_id == expected_facts.key_id]
    if len(candidates) != 1:
        raise AuthBootstrapError()
    key = candidates[0]
    if (key.revoked or not key.valid_from <= now < key.valid_until
            or key.operator_subject_ref != expected_facts.operator_subject_ref
            or key.installation_ref != expected_facts.installation_ref
            or key.authorized_actions != expected_facts.authorized_actions):
        raise AuthBootstrapError()
    try:
        Ed25519PublicKey.from_public_bytes(key.public_key).verify(proof.signature, expected)
    except (InvalidSignature, ValueError):
        raise AuthBootstrapError() from None
    return expected_facts


__all__ = ["AuthBootstrapError", "BootstrapTrustKey", "BootstrapTrustPolicy",
           "SignedBootstrapProof", "canonical_bootstrap_bytes",
           "bootstrap_challenge_sha256", "verify_signed_bootstrap"]
