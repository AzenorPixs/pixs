"""Fondation B04 Bulk : métadonnées ObjectMetadataV1 et primitives d'intégrité.

Module purement mémoire : sans entrée/sortie directe, ORM, Django, psycopg,
pixs.core concret, environnement, réseau, processus, import dynamique,
sérialisation, callback du payload ni état global mutable. Les types exacts
sont contrôlés avant toute copie, hashing, comparaison ou lecture d'horloge.
Les diagnostics sont des ``Diagnostic`` VALIDATE statiques du noyau, triés et
dédupliqués, sans écho d'une valeur fournie, d'un octet fautif ni d'une
exception étrangère.

Un flux n'est jamais conservé : seul un digest ``hashlib.sha256`` incrémental
et des compteurs mécaniques sont détenus. Une égalité d'intégrité ne prouve ni
une autorisation, ni la gouvernance, ni l'immuabilité d'un provider, ni une
validation métier ou une mutation. La structure ``ObjectStoragePort`` est
capturée statiquement sans invocation ; la capacité du provider reste
explicitement indisponible tant qu'aucune qualification serveur réelle de la
garantie de version n'est composée et prouvée.

Les validateurs, snapshots et SemVer des modules livrés restent inchangés ;
rien ici n'ajoute de schéma logique, de champ de configuration ni de wire
format.
"""

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from pixs.backend.bulk_execution_values import validate_bulk_policy_values
from pixs.backend.bulk_runtime_contracts import (
    _ContractRefused,
    _capture_policy_values,
    _exact_mapping,
    _is_opaque_text,
    _OPAQUE_RULE,
    _pack,
    _refusal,
)
from pixs.backend.bulk_trusted_ports import _structural_refusals
from pixs.kernel.diagnostics import Diagnostic

__all__ = [
    "validate_object_metadata_values",
    "new_object_integrity_verifier",
    "validate_object_storage_contract",
]

_METADATA_SCOPE = "bulk_object_metadata"
_VERIFIER_SCOPE = "bulk_object_integrity_verifier"
_PORT_SCOPE = "bulk_object_storage_port"

#: Capacité objet non qualifiée : aucune fabrique de provider, aucun booléen
#: du payload ni déclaration positive ne la « prouve ».
_OBJECT_STORAGE_CAPABILITY = "UNAVAILABLE"

_METADATA_KEYS = (
    "object_reference",
    "version_reference",
    "tenant_reference",
    "scope_reference",
    "classification_reference",
    "size_bytes",
    "sha256",
    "media_type",
    "is_private",
    "expires_at",
    "retention_policy_reference",
)
_METADATA_OPAQUE_FIELDS = (
    "object_reference",
    "version_reference",
    "tenant_reference",
    "classification_reference",
    "retention_policy_reference",
)
_MEDIA_TYPES = frozenset({"text/csv", "application/x-ndjson"})
_SHA256_PATTERN = re.compile("[0-9a-f]{64}")

_SHAPE_RULE = "onze clés exactes attendues"
_KEYS_RULE = "clés str exactes attendues"
_STR_RULE = "str exact attendu"
_STR_NONE_RULE = "str exact ou None explicite attendu"
_INT_RULE = "int exact attendu"
_BOOL_RULE = "bool exact attendu"
_DATETIME_RULE = "datetime exact attendu"
_UTC_RULE = "datetime exact aware UTC attendu"
_NONNEGATIVE_RULE = "entier exact supérieur ou égal à zéro attendu"
_SHA_RULE = "empreinte SHA-256 hex minuscule de 64 caractères attendue"
_MEDIA_RULE = "type de média text/csv ou application/x-ndjson exact attendu"
_PRIVATE_RULE = "valeur bool exacte True obligatoire attendue"
_SNAPSHOT_RULE = "snapshot refusé après validation des métadonnées"

_CLOSE_REASONS = frozenset({"CANCELLED", "CLOSED"})
_TERMINAL_RULE = "vérificateur terminal : opération refusée sans altération du bilan"
_STOPPED_RULE = "flux interrompu : aucun octet additionnel accepté"
_CLOSED_RULE = "raison de fermeture exacte CANCELLED ou CLOSED attendue"
_GUARD_TIME_RULE = "horloge serveur datetime exact aware UTC obligatoire"
_GUARD_CANCEL_RULE = "annulation bool exact serveur obligatoire"
_CANCELLED_RULE = "annulation serveur refuse le flux avant composition"
_EXPIRED_RULE = "échéance effective atteinte ou dépassée avant composition"
_LIMIT_DEADLINE_RULE = "échéance effective atteinte pendant le flux"
_CHUNK_TYPE_RULE = "segment bytes exact attendu"
_LIMIT_READ_CHUNK_RULE = "segment supérieur à read_chunk_bytes refusé avant hashing"
_LIMIT_INPUT_BYTES_RULE = "octets dépassant max_input_bytes refusés avant hashing"
_OVER_ANNOUNCED_RULE = "octets dépassant la taille annoncée refusés avant hashing"
_EXPECTED_MISMATCH_RULE = "métadonnées observées divergentes du contrat serveur attendu"
_BOUNDED_SIZE_RULE = "taille annoncée inférieure ou égale à max_input_bytes attendue"
_MISMATCH_RULE = "métadonnées fraîches divergentes de la version et du contexte attendus"
_SIZE_RULE = "octets acceptés différents de la taille annoncée attendus"
_HASH_RULE = "empreinte SHA-256 recalculée différente de l'empreinte attendue"
_INCOMPLETE_RULE = "intégrité incomplète"


class _VerifierRefused(ValueError):
    """Refus interne statique ; aucun message ne porte de valeur fournie."""


@dataclass(frozen=True, slots=True)
class _ObjectMetadataSnapshot:
    object_reference: str
    version_reference: str
    tenant_reference: str
    scope_reference: str | None
    classification_reference: str
    size_bytes: int
    sha256: str
    media_type: str
    is_private: bool
    expires_at: datetime
    retention_policy_reference: str

    def as_values(self) -> dict:
        return {
            "object_reference": self.object_reference,
            "version_reference": self.version_reference,
            "tenant_reference": self.tenant_reference,
            "scope_reference": self.scope_reference,
            "classification_reference": self.classification_reference,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "media_type": self.media_type,
            "is_private": self.is_private,
            "expires_at": self.expires_at,
            "retention_policy_reference": self.retention_policy_reference,
        }


@dataclass(frozen=True, slots=True)
class _ObjectIntegrityResult:
    complete: bool
    accepted_size: int
    sha256: str
    limit_reason: str | None
    diagnostics: tuple[Diagnostic, ...]

    def as_values(self) -> dict:
        return {
            "complete": self.complete,
            "accepted_size": self.accepted_size,
            "sha256": self.sha256,
            "limit_reason": self.limit_reason,
            "diagnostics": tuple(str(item) for item in self.diagnostics),
        }


def _metadata_type_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_METADATA_SCOPE, field, _STR_RULE)
        for field in _METADATA_OPAQUE_FIELDS
        if type(values[field]) is not str
    ]
    if type(values["scope_reference"]) is not str and values["scope_reference"] is not None:
        refusals.append(_refusal(_METADATA_SCOPE, "scope_reference", _STR_NONE_RULE))
    if type(values["size_bytes"]) is not int:
        refusals.append(_refusal(_METADATA_SCOPE, "size_bytes", _INT_RULE))
    if type(values["sha256"]) is not str:
        refusals.append(_refusal(_METADATA_SCOPE, "sha256", _STR_RULE))
    if type(values["media_type"]) is not str:
        refusals.append(_refusal(_METADATA_SCOPE, "media_type", _STR_RULE))
    if type(values["is_private"]) is not bool:
        refusals.append(_refusal(_METADATA_SCOPE, "is_private", _BOOL_RULE))
    expires = values["expires_at"]
    if type(expires) is not datetime:
        refusals.append(_refusal(_METADATA_SCOPE, "expires_at", _DATETIME_RULE))
    elif expires.tzinfo is not timezone.utc:
        refusals.append(_refusal(_METADATA_SCOPE, "expires_at", _UTC_RULE))
    return refusals


def _metadata_value_refusals(values: dict) -> list[Diagnostic]:
    refusals: list[Diagnostic] = [
        _refusal(_METADATA_SCOPE, field, _OPAQUE_RULE)
        for field in _METADATA_OPAQUE_FIELDS
        if not _is_opaque_text(values[field])
    ]
    scope = values["scope_reference"]
    if scope is not None and not _is_opaque_text(scope):
        refusals.append(_refusal(_METADATA_SCOPE, "scope_reference", _OPAQUE_RULE))
    if values["size_bytes"] < 0:
        refusals.append(_refusal(_METADATA_SCOPE, "size_bytes", _NONNEGATIVE_RULE))
    if _SHA256_PATTERN.fullmatch(values["sha256"]) is None:
        refusals.append(_refusal(_METADATA_SCOPE, "sha256", _SHA_RULE))
    if values["media_type"] not in _MEDIA_TYPES:
        refusals.append(_refusal(_METADATA_SCOPE, "media_type", _MEDIA_RULE))
    if values["is_private"] is not True:
        refusals.append(_refusal(_METADATA_SCOPE, "is_private", _PRIVATE_RULE))
    return refusals


def validate_object_metadata_values(candidate: object) -> list[Diagnostic]:
    """Contrôle ObjectMetadataV1 : onze clés, types d'abord, aucune déduction."""
    values, refusals = _exact_mapping(candidate, _METADATA_SCOPE, _METADATA_KEYS, _SHAPE_RULE)
    if values is None:
        return _pack(refusals)
    type_refusals = _metadata_type_refusals(values)
    if type_refusals:
        return _pack(type_refusals)
    return _pack(_metadata_value_refusals(values))


def _capture_metadata_snapshot(candidate: object) -> tuple[_ObjectMetadataSnapshot | None, list[Diagnostic]]:
    if type(candidate) is not dict:
        return None, [_refusal(_METADATA_SCOPE, "mapping", _SHAPE_RULE)]
    items = tuple(candidate.items())
    if any(type(key) is not str for key, _value in items):
        return None, [_refusal(_METADATA_SCOPE, "keys", _KEYS_RULE)]
    captured = {key: value for key, value in items}
    refusals = validate_object_metadata_values(captured)
    if refusals:
        return None, refusals
    try:
        return _ObjectMetadataSnapshot(**captured), []
    except (_ContractRefused, KeyError, TypeError):
        return None, [_refusal(_METADATA_SCOPE, "snapshot", _SNAPSHOT_RULE)]


def _capture_policy(policy: object) -> tuple[dict | None, list[Diagnostic]]:
    captured = _capture_policy_values(policy)
    refusals = validate_bulk_policy_values(captured)
    if refusals:
        return None, refusals
    return captured, []


class _ObjectIntegrityVerifier:
    """Vérificateur d'intégrité borné : digest et compteurs, jamais le fichier."""

    __slots__ = (
        "_expected",
        "_effective",
        "_max_input",
        "_read_chunk",
        "_max_diag",
        "_hasher",
        "_accepted",
        "_stopped",
        "_limit",
        "_diags",
        "_result",
    )

    def __init__(
        self,
        *,
        expected: _ObjectMetadataSnapshot,
        effective: datetime,
        max_input: int,
        read_chunk: int,
        max_diag: int,
    ) -> None:
        self._expected = expected
        self._effective = effective
        self._max_input = max_input
        self._read_chunk = read_chunk
        self._max_diag = max_diag
        self._hasher = hashlib.sha256()
        self._accepted = 0
        self._stopped = False
        self._limit: str | None = None
        self._diags: list[Diagnostic] = []
        self._result: _ObjectIntegrityResult | None = None

    def _record(self, code: str) -> None:
        self._stopped = True
        if self._limit is None:
            self._limit = code
        if len(self._diags) < self._max_diag:
            self._diags.append(_refusal(_VERIFIER_SCOPE, "stream", code))

    def _halt(self, code: str) -> list[Diagnostic]:
        refusal = _refusal(_VERIFIER_SCOPE, "stream", code)
        self._record(code)
        return [refusal]

    def feed(self, chunk: object, *, now: object, cancelled: object) -> list[Diagnostic]:
        if self._result is not None:
            raise _VerifierRefused(_TERMINAL_RULE)
        if self._stopped:
            return _pack([_refusal(_VERIFIER_SCOPE, "stream", _STOPPED_RULE)])
        if type(now) is not datetime or now.tzinfo is not timezone.utc:
            return self._halt(_GUARD_TIME_RULE)
        if type(cancelled) is not bool:
            return self._halt(_GUARD_CANCEL_RULE)
        if cancelled:
            return self._halt(_CANCELLED_RULE)
        if now >= self._effective:
            return self._halt(_LIMIT_DEADLINE_RULE)
        if type(chunk) is not bytes:
            return self._halt(_CHUNK_TYPE_RULE)
        length = len(chunk)
        if length == 0:
            return []
        if length > self._read_chunk:
            return self._halt(_LIMIT_READ_CHUNK_RULE)
        if self._accepted + length > self._max_input:
            return self._halt(_LIMIT_INPUT_BYTES_RULE)
        if self._accepted + length > self._expected.size_bytes:
            return self._halt(_OVER_ANNOUNCED_RULE)
        self._hasher.update(chunk)
        self._accepted += length
        return []

    def finish(
        self, *, observed_metadata: object, now: object, cancelled: object
    ) -> _ObjectIntegrityResult:
        if self._result is not None:
            return self._result
        refusals: list[Diagnostic] = []
        observed, observed_refusals = _capture_metadata_snapshot(observed_metadata)
        refusals.extend(observed_refusals)
        if type(now) is not datetime or now.tzinfo is not timezone.utc:
            refusals.append(_refusal(_VERIFIER_SCOPE, "now", _GUARD_TIME_RULE))
            valid_now = False
        else:
            valid_now = now < self._effective
            if not valid_now:
                refusals.append(_refusal(_VERIFIER_SCOPE, "now", _LIMIT_DEADLINE_RULE))
        if type(cancelled) is not bool:
            refusals.append(_refusal(_VERIFIER_SCOPE, "cancelled", _GUARD_CANCEL_RULE))
            valid_cancel = False
        else:
            valid_cancel = not cancelled
            if not valid_cancel:
                refusals.append(_refusal(_VERIFIER_SCOPE, "cancelled", _CANCELLED_RULE))
        matches = (
            observed is not None
            and observed.as_values() == self._expected.as_values()
        )
        if observed is not None and not matches:
            refusals.append(_refusal(_VERIFIER_SCOPE, "observed_metadata", _MISMATCH_RULE))
        if self._stopped:
            refusals.append(_refusal(_VERIFIER_SCOPE, "stream", _STOPPED_RULE))
        size_ok = self._accepted == self._expected.size_bytes
        if not size_ok:
            refusals.append(_refusal(_VERIFIER_SCOPE, "accepted_size", _SIZE_RULE))
        digest = self._hasher.hexdigest()
        hash_ok = digest == self._expected.sha256
        if not hash_ok:
            refusals.append(_refusal(_VERIFIER_SCOPE, "sha256", _HASH_RULE))
        complete = (
            not self._stopped
            and valid_now
            and valid_cancel
            and matches
            and size_ok
            and hash_ok
        )
        return self._freeze(complete, refusals)

    def close(self, reason: object) -> None:
        if type(reason) is not str or reason not in _CLOSE_REASONS:
            raise _VerifierRefused(_CLOSED_RULE)
        if self._result is not None:
            return
        self._record(reason)
        self._freeze(False)

    def _freeze(
        self, complete: bool, extra: tuple[Diagnostic, ...] | list[Diagnostic] = ()
    ) -> _ObjectIntegrityResult:
        combined = tuple(_pack([*self._diags, *extra])[:self._max_diag])
        reason = self._limit
        if reason is None and not complete:
            reason = _INCOMPLETE_RULE
        self._result = _ObjectIntegrityResult(
            complete=complete,
            accepted_size=self._accepted,
            sha256=self._hasher.hexdigest(),
            limit_reason=reason,
            diagnostics=combined,
        )
        return self._result


def new_object_integrity_verifier(
    *,
    metadata: object,
    expected_metadata: object,
    policy: object,
    deadline: object,
    now: object,
    cancelled: object,
) -> tuple[_ObjectIntegrityVerifier | None, list[Diagnostic]]:
    """Compose un vérificateur borné ; horloge et annulation sont des données serveur."""
    metadata_snapshot, metadata_refusals = _capture_metadata_snapshot(metadata)
    expected_snapshot, expected_refusals = _capture_metadata_snapshot(expected_metadata)
    policy_values, policy_refusals = _capture_policy(policy)
    refusals: list[Diagnostic] = [*metadata_refusals, *expected_refusals, *policy_refusals]
    if type(deadline) is not datetime or deadline.tzinfo is not timezone.utc:
        refusals.append(_refusal(_VERIFIER_SCOPE, "deadline", _UTC_RULE))
    if type(now) is not datetime or now.tzinfo is not timezone.utc:
        refusals.append(_refusal(_VERIFIER_SCOPE, "now", _UTC_RULE))
    if type(cancelled) is not bool:
        refusals.append(_refusal(_VERIFIER_SCOPE, "cancelled", _BOOL_RULE))
    if metadata_snapshot is not None and expected_snapshot is not None:
        if metadata_snapshot.as_values() != expected_snapshot.as_values():
            refusals.append(_refusal(_VERIFIER_SCOPE, "metadata", _EXPECTED_MISMATCH_RULE))
    if (
        metadata_snapshot is not None
        and policy_values is not None
        and metadata_snapshot.size_bytes > policy_values["max_input_bytes"]
    ):
        refusals.append(_refusal(_VERIFIER_SCOPE, "size_bytes", _BOUNDED_SIZE_RULE))
    if (
        refusals
        or metadata_snapshot is None
        or expected_snapshot is None
        or policy_values is None
    ):
        return None, _pack(refusals)
    if cancelled:
        return None, _pack([_refusal(_VERIFIER_SCOPE, "cancelled", _CANCELLED_RULE)])
    effective = min(deadline, metadata_snapshot.expires_at, expected_snapshot.expires_at)
    if not now < effective:
        return None, _pack([_refusal(_VERIFIER_SCOPE, "now", _EXPIRED_RULE)])
    verifier = _ObjectIntegrityVerifier(
        expected=expected_snapshot,
        effective=effective,
        max_input=policy_values["max_input_bytes"],
        read_chunk=policy_values["read_chunk_bytes"],
        max_diag=policy_values["max_diagnostics"],
    )
    return verifier, []


def validate_object_storage_contract(component: object) -> list[Diagnostic]:
    """Structure statique des six méthodes ObjectStoragePort ; aucune invocation.

    Une forme correcte ne constitue jamais un provider prêt : la capacité
    d'objet reste ``UNAVAILABLE`` tant qu'aucune qualification serveur réelle de
    la garantie de version n'est composée et prouvée.
    """
    return _structural_refusals(
        component,
        (
            "stat_private",
            "iter_bytes",
            "begin_private_write",
            "finalize_private_write",
            "revoke",
            "purge_authorized",
        ),
        _PORT_SCOPE,
    )
