"""Registre et cycle de vie CA, représentations liées seules.

Portée exacte : `z12.ca_inventory/v1` (§7.2), `z12.ca_state/v1` (§7.3),
`z12.ca_rotation/v1` (§7.4), `z12.ca_loss/v1` (§7.5),
`z12.ca_succession/v1` (§7.6), `z12.ca_migration/v1` (§7.7),
`z12.ca_application_observation/v1` (§7.8).
Réutilise helpers `ca_identity` et calculs `durations` sans horloge
implicite, sans flottant. Structures et invariants déterminés seuls.
Autorité, appartenance, preuve, retrait effectif et transitions
restent aux vrais services. Aucun bool vérifié. Signature ne prouve
pas PostgreSQL. Égalité exacte même génération/racine refusée car
elle ne prouve pas l'indépendance.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any

from pixs.pzt_ca import durations as _durations
from pixs.pzt_ca.ca_identity import CaIdentityError as _CaIdentityError
from pixs.pzt_ca.ca_identity import _check_bounded_keys as _base_check_bounded
from pixs.pzt_ca.ca_identity import _check_exact_keys as _base_check_exact
from pixs.pzt_ca.ca_identity import _is_utc_instant as _base_is_utc
from pixs.pzt_ca.ca_identity import _parse_rfc3339_utc as _base_parse_time
from pixs.pzt_ca.ca_identity import _require_closed_enum as _base_require_enum
from pixs.pzt_ca.ca_identity import _require_epoch as _base_require_epoch
from pixs.pzt_ca.ca_identity import _require_public_ref as _base_require_ref
from pixs.pzt_ca.ca_identity import _require_version as _base_require_ver
from pixs.pzt_ca.ca_identity import loads_strict_mapping as _base_loads
from pixs.pzt_ca.durations import DurationsError as _DurationsError

__all__ = [
    "CaLifecycleError",
    "CaInventory",
    "CaState",
    "CaRotation",
    "CaLoss",
    "CaSuccession",
    "CaMigration",
    "CaObservation",
    "SCHEMA_VERSION",
    "inventory_from_mapping",
    "inventory_from_json",
    "state_from_mapping",
    "state_from_json",
    "rotation_from_mapping",
    "rotation_from_json",
    "loss_from_mapping",
    "loss_from_json",
    "succession_from_mapping",
    "succession_from_json",
    "migration_from_mapping",
    "migration_from_json",
    "observation_from_mapping",
    "observation_from_json",
    "succession_upper_bound",
    "check_migration_common_plan_fields",
]

SCHEMA_VERSION = "1.0.0"

INVENTORY_OBJECT = "z12.ca_inventory/v1"
STATE_OBJECT = "z12.ca_state/v1"
ROTATION_OBJECT = "z12.ca_rotation/v1"
LOSS_OBJECT = "z12.ca_loss/v1"
SUCCESSION_OBJECT = "z12.ca_succession/v1"
MIGRATION_OBJECT = "z12.ca_migration/v1"
OBSERVATION_OBJECT = "z12.ca_application_observation/v1"

ANCHOR_STATUS = ("not_admitted", "current_only", "coexistence_admitted", "successor_only")
PLAN_STATUS = ("prepared", "engaged", "withdrawn")
LOSS_CLASSES = ("lost", "corrupted", "replaced", "suspected_compromise", "known_compromise")
RECOVERY_STATES = ("detected", "recertification_pending", "reconciled", "blocked")

_INVENTORY_FIELDS = frozenset({
    "object_type", "schema_version", "inventory_id", "domain", "epoch",
    "inventory_version", "issuer_refs", "generation_refs", "cert_refs",
    "anchor_refs", "engagement_ref",
})
_STATE_REQUIRED = frozenset({
    "object_type", "schema_version", "state_id", "domain", "epoch",
    "state_version", "admitted_issuer_refs", "active_generation_refs",
    "withdrawn_generation_refs", "anchor_refs", "anchor_status",
    "current_decision_ref", "engagement_ref",
})
_STATE_ALLOWED = frozenset({
    "object_type", "schema_version", "state_id", "domain", "epoch",
    "state_version", "admitted_issuer_refs", "active_generation_refs",
    "withdrawn_generation_refs", "anchor_refs", "anchor_status",
    "succession_plan_ref", "current_decision_ref", "engagement_ref",
})
_ROTATION_REQUIRED = frozenset({
    "object_type", "schema_version", "plan_ref", "plan_version",
    "context_ref", "domain", "logical_authority", "emission_scope",
    "issuer_ref", "from_generation_ref", "to_generation_ref",
    "offline_procedure_ref", "deadline_utc", "status",
})
_ROTATION_ALLOWED = frozenset({
    "object_type", "schema_version", "plan_ref", "plan_version",
    "context_ref", "domain", "logical_authority", "emission_scope",
    "issuer_ref", "from_generation_ref", "to_generation_ref",
    "offline_procedure_ref", "deadline_utc", "status",
    "engaged_at_utc", "engagement_ref", "exclusion_proof_ref", "withdrawn_at_utc",
})
_LOSS_REQUIRED = frozenset({
    "object_type", "schema_version", "loss_id", "incident_version",
    "context_ref", "issuer_ref", "lost_generation_ref", "loss_class",
    "detected_at_utc", "recovery_state",
})
_LOSS_ALLOWED = frozenset({
    "object_type", "schema_version", "loss_id", "incident_version",
    "context_ref", "issuer_ref", "lost_generation_ref", "loss_class",
    "detected_at_utc", "recovery_state", "replacement_generation_ref",
    "offline_procedure_ref", "reconciliation_ref",
})
_SUCCESSION_REQUIRED = frozenset({
    "object_type", "schema_version", "plan_ref", "plan_version",
    "context_ref", "domain", "scope_ref", "from_root_ref", "to_root_ref",
    "offline_procedure_ref", "deadline_utc", "anchor_bound_at_utc", "status",
})
_SUCCESSION_ALLOWED = frozenset({
    "object_type", "schema_version", "plan_ref", "plan_version",
    "context_ref", "domain", "scope_ref", "from_root_ref", "to_root_ref",
    "offline_procedure_ref", "deadline_utc", "anchor_bound_at_utc", "status",
    "engaged_at_utc", "withdraw_at_utc", "engagement_ref", "withdrawn_at_utc",
})
_MIGRATION_FIELDS = frozenset({
    "object_type", "schema_version", "migration_id", "succession_plan_ref",
    "plan_version", "domain", "scope_ref", "from_anchor_ref", "to_anchor_ref",
    "engagement_ref", "engaged_at_utc", "withdraw_at_utc",
    "anchor_bound_at_utc", "applied_observation_refs", "status",
})
_OBSERVATION_FIELDS = frozenset({
    "object_type", "schema_version", "observation_id", "association_ref",
    "plan_ref", "plan_version", "domain", "scope_ref", "target_anchor_ref",
    "target_generation_ref", "observed_at_utc", "applied_proof_ref", "epoch",
})


class CaLifecycleError(ValueError):
    """Refus structurel sans exposer l'entrée."""

    def __init__(self, code: str, element: str) -> None:
        super().__init__(f"{element} : {code}")
        self.code = code
        self.element = element
        self.step = "validate_structure"


def _deny(code: str, element: str) -> CaLifecycleError:
    return CaLifecycleError(code, element)


def _req_ref(value: object, element: str) -> None:
    try:
        _base_require_ref(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_ver(value: object, element: str) -> None:
    try:
        _base_require_ver(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_enum(value: object, expected: tuple[str, ...], element: str) -> None:
    try:
        _base_require_enum(value, expected, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _req_epoch(value: object, element: str) -> None:
    try:
        _base_require_epoch(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _parse_time(value: object, element: str) -> datetime.datetime:
    try:
        return _base_parse_time(value, element)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _loads_mapping(text: object) -> dict[str, Any]:
    try:
        mapping = _base_loads(text)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "mapping")
    return mapping


def _check_exact(mapping: dict[str, Any], expected: frozenset[str]) -> None:
    try:
        _base_check_exact(mapping, expected)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _check_bounded(mapping: dict[str, Any], required: frozenset[str], allowed: frozenset[str]) -> None:
    try:
        _base_check_bounded(mapping, required, allowed)
    except _CaIdentityError as exc:
        raise _deny(exc.code, exc.element) from None


def _set_from_list(value: object, element: str) -> tuple[str, ...]:
    if type(value) is not list:
        raise _deny("ENSEMBLE_INVALIDE", element)
    seen: set[str] = set()
    for item in value:
        try:
            _base_require_ref(item, element)
        except _CaIdentityError as exc:
            raise _deny(exc.code, exc.element) from None
        if item in seen:
            raise _deny("DOUBLON_INTERDIT", element)
        seen.add(item)  # type: ignore[arg-type]
    return tuple(value)  # type: ignore[arg-type]


def _check_set_tuple(value: object, element: str) -> None:
    if type(value) is not tuple:
        raise _deny("ENSEMBLE_INVALIDE", element)
    seen: set[str] = set()
    for item in value:
        if type(item) is not str:
            raise _deny("REFERENCE_OPAQUE_INVALIDE", element)
        try:
            _base_require_ref(item, element)
        except _CaIdentityError as exc:
            raise _deny(exc.code, exc.element) from None
        if item in seen:
            raise _deny("DOUBLON_INTERDIT", element)
        seen.add(item)


def _opt_ref(mapping: dict[str, Any], name: str, element: str) -> str | None:
    if name not in mapping:
        return None
    value = mapping[name]
    if value is None:
        raise _deny("NUL_INTERDIT", element)
    _req_ref(value, element)
    return value  # type: ignore[return-value]


def _opt_time(mapping: dict[str, Any], name: str, element: str) -> datetime.datetime | None:
    if name not in mapping:
        return None
    value = mapping[name]
    if value is None:
        raise _deny("NUL_INTERDIT", element)
    return _parse_time(value, element)


@dataclass(frozen=True, slots=True, repr=False)
class CaInventory:
    object_type: str
    schema_version: str
    inventory_id: str
    domain: str
    epoch: int
    inventory_version: str
    issuer_refs: tuple[str, ...]
    generation_refs: tuple[str, ...]
    cert_refs: tuple[str, ...]
    anchor_refs: tuple[str, ...]
    engagement_ref: str

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != INVENTORY_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_inventory.object_type")
        _req_ver(current(self, "schema_version"), "ca_inventory.schema_version")
        for name in ("inventory_id", "domain", "inventory_version", "engagement_ref"):
            _req_ref(current(self, name), f"ca_inventory.{name}")
        _req_epoch(current(self, "epoch"), "ca_inventory.epoch")
        for name in ("issuer_refs", "generation_refs", "cert_refs", "anchor_refs"):
            _check_set_tuple(current(self, name), f"ca_inventory.{name}")


@dataclass(frozen=True, slots=True, repr=False)
class CaState:
    object_type: str
    schema_version: str
    state_id: str
    domain: str
    epoch: int
    state_version: str
    admitted_issuer_refs: tuple[str, ...]
    active_generation_refs: tuple[str, ...]
    withdrawn_generation_refs: tuple[str, ...]
    anchor_refs: tuple[str, ...]
    anchor_status: str
    current_decision_ref: str
    engagement_ref: str
    succession_plan_ref: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != STATE_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_state.object_type")
        _req_ver(current(self, "schema_version"), "ca_state.schema_version")
        for name in ("state_id", "domain", "state_version", "current_decision_ref", "engagement_ref"):
            _req_ref(current(self, name), f"ca_state.{name}")
        _req_epoch(current(self, "epoch"), "ca_state.epoch")
        for name in ("admitted_issuer_refs", "active_generation_refs", "withdrawn_generation_refs", "anchor_refs"):
            _check_set_tuple(current(self, name), f"ca_state.{name}")
        _req_enum(current(self, "anchor_status"), ANCHOR_STATUS, "ca_state.anchor_status")
        plan = current(self, "succession_plan_ref")
        if plan is not None:
            _req_ref(plan, "ca_state.succession_plan_ref")
        if current(self, "anchor_status") == "coexistence_admitted" and plan is None:
            raise _deny("PLAN_REQUIS", "ca_state.succession_plan_ref")
        if set(current(self, "active_generation_refs")) & set(current(self, "withdrawn_generation_refs")):
            raise _deny("ENSEMBLES_NON_DISJOINTS", "ca_state.withdrawn_generation_refs")


@dataclass(frozen=True, slots=True, repr=False)
class CaRotation:
    object_type: str
    schema_version: str
    plan_ref: str
    plan_version: str
    context_ref: str
    domain: str
    logical_authority: str
    emission_scope: str
    issuer_ref: str
    from_generation_ref: str
    to_generation_ref: str
    offline_procedure_ref: str
    deadline_utc: datetime.datetime
    status: str
    engaged_at_utc: datetime.datetime | None = None
    engagement_ref: str | None = None
    exclusion_proof_ref: str | None = None
    withdrawn_at_utc: datetime.datetime | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != ROTATION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_rotation.object_type")
        _req_ver(current(self, "schema_version"), "ca_rotation.schema_version")
        for name in ("plan_ref", "plan_version", "context_ref", "domain", "logical_authority", "emission_scope", "issuer_ref", "from_generation_ref", "to_generation_ref", "offline_procedure_ref"):
            _req_ref(current(self, name), f"ca_rotation.{name}")
        if not _base_is_utc(current(self, "deadline_utc")):
            raise _deny("HORODATAGE_NON_UTC", "ca_rotation.deadline_utc")
        _req_enum(current(self, "status"), PLAN_STATUS, "ca_rotation.status")
        for name in ("engaged_at_utc",):
            value = current(self, name)
            if value is not None and not _base_is_utc(value):
                raise _deny("HORODATAGE_NON_UTC", f"ca_rotation.{name}")
        for name in ("engagement_ref", "exclusion_proof_ref"):
            value = current(self, name)
            if value is not None:
                _req_ref(value, f"ca_rotation.{name}")
        withdrawn = current(self, "withdrawn_at_utc")
        if withdrawn is not None and not _base_is_utc(withdrawn):
            raise _deny("HORODATAGE_NON_UTC", "ca_rotation.withdrawn_at_utc")
        status = current(self, "status")
        if status == "prepared":
            if current(self, "engaged_at_utc") is not None or current(self, "engagement_ref") is not None or current(self, "exclusion_proof_ref") is not None or withdrawn is not None:
                raise _deny("DONNEES_ENGAGEES_INTERDITES", "ca_rotation.status")
        elif status == "engaged":
            if current(self, "engaged_at_utc") is None or current(self, "engagement_ref") is None or current(self, "exclusion_proof_ref") is None:
                raise _deny("DONNEES_ENGAGEES_REQUISES", "ca_rotation.status")
            if withdrawn is not None:
                raise _deny("RETRAIT_PREMATURE", "ca_rotation.withdrawn_at_utc")
        else:
            if current(self, "engaged_at_utc") is None or current(self, "engagement_ref") is None or current(self, "exclusion_proof_ref") is None or withdrawn is None:
                raise _deny("DONNEES_RETRAIT_REQUISES", "ca_rotation.status")
        if current(self, "engaged_at_utc") is not None:
            if not current(self, "engaged_at_utc") < current(self, "deadline_utc"):  # type: ignore[operator]
                raise _deny("CHRONOLOGIE_INVALIDE", "ca_rotation.engaged_at_utc")
        if withdrawn is not None and current(self, "engaged_at_utc") is not None:
            if withdrawn < current(self, "engaged_at_utc"):  # type: ignore[operator]
                raise _deny("CHRONOLOGIE_INVALIDE", "ca_rotation.withdrawn_at_utc")
        if current(self, "from_generation_ref") == current(self, "to_generation_ref"):
            raise _deny("GENERATION_NON_INDEPENDANTE", "ca_rotation.to_generation_ref")


@dataclass(frozen=True, slots=True, repr=False)
class CaLoss:
    object_type: str
    schema_version: str
    loss_id: str
    incident_version: str
    context_ref: str
    issuer_ref: str
    lost_generation_ref: str
    loss_class: str
    detected_at_utc: datetime.datetime
    recovery_state: str
    replacement_generation_ref: str | None = None
    offline_procedure_ref: str | None = None
    reconciliation_ref: str | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != LOSS_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_loss.object_type")
        _req_ver(current(self, "schema_version"), "ca_loss.schema_version")
        for name in ("loss_id", "incident_version", "context_ref", "issuer_ref", "lost_generation_ref"):
            _req_ref(current(self, name), f"ca_loss.{name}")
        _req_enum(current(self, "loss_class"), LOSS_CLASSES, "ca_loss.loss_class")
        if not _base_is_utc(current(self, "detected_at_utc")):
            raise _deny("HORODATAGE_NON_UTC", "ca_loss.detected_at_utc")
        _req_enum(current(self, "recovery_state"), RECOVERY_STATES, "ca_loss.recovery_state")
        for name in ("replacement_generation_ref", "offline_procedure_ref", "reconciliation_ref"):
            value = current(self, name)
            if value is not None:
                _req_ref(value, f"ca_loss.{name}")
        state = current(self, "recovery_state")
        offline = current(self, "offline_procedure_ref")
        recon = current(self, "reconciliation_ref")
        if state in ("recertification_pending", "reconciled"):
            if offline is None:
                raise _deny("PROCEDURE_REQUISE", "ca_loss.offline_procedure_ref")
        if state == "reconciled":
            if recon is None:
                raise _deny("RECONCILIATION_REQUISE", "ca_loss.reconciliation_ref")
        if current(self, "replacement_generation_ref") is not None and current(self, "replacement_generation_ref") == current(self, "lost_generation_ref"):
            raise _deny("GENERATION_NON_INDEPENDANTE", "ca_loss.replacement_generation_ref")


@dataclass(frozen=True, slots=True, repr=False)
class CaSuccession:
    object_type: str
    schema_version: str
    plan_ref: str
    plan_version: str
    context_ref: str
    domain: str
    scope_ref: str
    from_root_ref: str
    to_root_ref: str
    offline_procedure_ref: str
    deadline_utc: datetime.datetime
    anchor_bound_at_utc: datetime.datetime
    status: str
    engaged_at_utc: datetime.datetime | None = None
    withdraw_at_utc: datetime.datetime | None = None
    engagement_ref: str | None = None
    withdrawn_at_utc: datetime.datetime | None = None

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != SUCCESSION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_succession.object_type")
        _req_ver(current(self, "schema_version"), "ca_succession.schema_version")
        for name in ("plan_ref", "plan_version", "context_ref", "domain", "scope_ref", "from_root_ref", "to_root_ref", "offline_procedure_ref"):
            _req_ref(current(self, name), f"ca_succession.{name}")
        for name in ("deadline_utc", "anchor_bound_at_utc"):
            if not _base_is_utc(current(self, name)):
                raise _deny("HORODATAGE_NON_UTC", f"ca_succession.{name}")
        _req_enum(current(self, "status"), PLAN_STATUS, "ca_succession.status")
        for name in ("engaged_at_utc", "withdraw_at_utc", "withdrawn_at_utc"):
            value = current(self, name)
            if value is not None and not _base_is_utc(value):
                raise _deny("HORODATAGE_NON_UTC", f"ca_succession.{name}")
        for name in ("engagement_ref",):
            value = current(self, name)
            if value is not None:
                _req_ref(value, f"ca_succession.{name}")
        status = current(self, "status")
        if status == "prepared":
            if current(self, "engaged_at_utc") is not None or current(self, "withdraw_at_utc") is not None or current(self, "engagement_ref") is not None or current(self, "withdrawn_at_utc") is not None:
                raise _deny("DONNEES_ENGAGEES_INTERDITES", "ca_succession.status")
        elif status == "engaged":
            if current(self, "engaged_at_utc") is None or current(self, "withdraw_at_utc") is None or current(self, "engagement_ref") is None:
                raise _deny("DONNEES_ENGAGEES_REQUISES", "ca_succession.status")
            if current(self, "withdrawn_at_utc") is not None:
                raise _deny("RETRAIT_PREMATURE", "ca_succession.withdrawn_at_utc")
        else:
            if current(self, "engaged_at_utc") is None or current(self, "withdraw_at_utc") is None or current(self, "engagement_ref") is None or current(self, "withdrawn_at_utc") is None:
                raise _deny("DONNEES_RETRAIT_REQUISES", "ca_succession.status")
        if current(self, "from_root_ref") == current(self, "to_root_ref"):
            raise _deny("RACINE_NON_INDEPENDANTE", "ca_succession.to_root_ref")
        if status in ("engaged", "withdrawn"):
            if not current(self, "engaged_at_utc") < current(self, "withdraw_at_utc"):  # type: ignore[operator]
                raise _deny("CHRONOLOGIE_INVALIDE", "ca_succession.withdraw_at_utc")
            try:
                bound = _durations.coexistence_upper_bound(
                    current(self, "engaged_at_utc"),
                    current(self, "deadline_utc"),
                    current(self, "anchor_bound_at_utc"),
                )
            except _DurationsError as exc:
                raise _deny(exc.code, "ca_succession.withdraw_at_utc") from None
            if current(self, "withdraw_at_utc") > bound:  # type: ignore[operator]
                raise _deny("BORNE_DEPASSEE", "ca_succession.withdraw_at_utc")
            if current(self, "withdrawn_at_utc") is not None and current(self, "withdrawn_at_utc") < current(self, "engaged_at_utc"):  # type: ignore[operator]
                raise _deny("CHRONOLOGIE_INVALIDE", "ca_succession.withdrawn_at_utc")


@dataclass(frozen=True, slots=True, repr=False)
class CaMigration:
    object_type: str
    schema_version: str
    migration_id: str
    succession_plan_ref: str
    plan_version: str
    domain: str
    scope_ref: str
    from_anchor_ref: str
    to_anchor_ref: str
    engagement_ref: str
    engaged_at_utc: datetime.datetime
    withdraw_at_utc: datetime.datetime
    anchor_bound_at_utc: datetime.datetime
    applied_observation_refs: tuple[str, ...]
    status: str

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != MIGRATION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_migration.object_type")
        _req_ver(current(self, "schema_version"), "ca_migration.schema_version")
        for name in ("migration_id", "succession_plan_ref", "plan_version", "domain", "scope_ref", "from_anchor_ref", "to_anchor_ref", "engagement_ref"):
            _req_ref(current(self, name), f"ca_migration.{name}")
        for name in ("engaged_at_utc", "withdraw_at_utc", "anchor_bound_at_utc"):
            if not _base_is_utc(current(self, name)):
                raise _deny("HORODATAGE_NON_UTC", f"ca_migration.{name}")
        _check_set_tuple(current(self, "applied_observation_refs"), "ca_migration.applied_observation_refs")
        _req_enum(current(self, "status"), PLAN_STATUS, "ca_migration.status")
        if not current(self, "engaged_at_utc") < current(self, "withdraw_at_utc"):  # type: ignore[operator]
            raise _deny("CHRONOLOGIE_INVALIDE", "ca_migration.withdraw_at_utc")
        try:
            upper_bound = _durations.coexistence_upper_bound(
                current(self, "engaged_at_utc"),
                current(self, "withdraw_at_utc"),
                current(self, "anchor_bound_at_utc"),
            )
        except _DurationsError as exc:
            raise _deny(exc.code, "ca_migration.withdraw_at_utc") from None
        if current(self, "withdraw_at_utc") > upper_bound:  # type: ignore[operator]
            raise _deny("BORNE_DEPASSEE", "ca_migration.withdraw_at_utc")
        if current(self, "from_anchor_ref") == current(self, "to_anchor_ref"):
            raise _deny("ANCRE_NON_INDEPENDANTE", "ca_migration.to_anchor_ref")


@dataclass(frozen=True, slots=True, repr=False)
class CaObservation:
    object_type: str
    schema_version: str
    observation_id: str
    association_ref: str
    plan_ref: str
    plan_version: str
    domain: str
    scope_ref: str
    target_anchor_ref: str
    target_generation_ref: str
    observed_at_utc: datetime.datetime
    applied_proof_ref: str
    epoch: int

    def __post_init__(self) -> None:
        current = object.__getattribute__
        if type(current(self, "object_type")) is not str or current(self, "object_type") != OBSERVATION_OBJECT:
            raise _deny("DISCRIMINATEUR_INVALIDE", "ca_observation.object_type")
        _req_ver(current(self, "schema_version"), "ca_observation.schema_version")
        for name in ("observation_id", "association_ref", "plan_ref", "plan_version", "domain", "scope_ref", "target_anchor_ref", "target_generation_ref", "applied_proof_ref"):
            _req_ref(current(self, name), f"ca_observation.{name}")
        if not _base_is_utc(current(self, "observed_at_utc")):
            raise _deny("HORODATAGE_NON_UTC", "ca_observation.observed_at_utc")
        _req_epoch(current(self, "epoch"), "ca_observation.epoch")


def inventory_from_mapping(mapping: dict[str, Any]) -> CaInventory:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_inventory")
    _check_exact(mapping, _INVENTORY_FIELDS)
    return CaInventory(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        inventory_id=mapping["inventory_id"],
        domain=mapping["domain"],
        epoch=mapping["epoch"],
        inventory_version=mapping["inventory_version"],
        issuer_refs=_set_from_list(mapping["issuer_refs"], "ca_inventory.issuer_refs"),
        generation_refs=_set_from_list(mapping["generation_refs"], "ca_inventory.generation_refs"),
        cert_refs=_set_from_list(mapping["cert_refs"], "ca_inventory.cert_refs"),
        anchor_refs=_set_from_list(mapping["anchor_refs"], "ca_inventory.anchor_refs"),
        engagement_ref=mapping["engagement_ref"],
    )


def inventory_from_json(text: object) -> CaInventory:
    return inventory_from_mapping(_loads_mapping(text))


def state_from_mapping(mapping: dict[str, Any]) -> CaState:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_state")
    _check_bounded(mapping, _STATE_REQUIRED, _STATE_ALLOWED)
    plan = mapping.get("succession_plan_ref")
    if "succession_plan_ref" in mapping and plan is None:
        raise _deny("NUL_INTERDIT", "ca_state.succession_plan_ref")
    return CaState(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        state_id=mapping["state_id"],
        domain=mapping["domain"],
        epoch=mapping["epoch"],
        state_version=mapping["state_version"],
        admitted_issuer_refs=_set_from_list(mapping["admitted_issuer_refs"], "ca_state.admitted_issuer_refs"),
        active_generation_refs=_set_from_list(mapping["active_generation_refs"], "ca_state.active_generation_refs"),
        withdrawn_generation_refs=_set_from_list(mapping["withdrawn_generation_refs"], "ca_state.withdrawn_generation_refs"),
        anchor_refs=_set_from_list(mapping["anchor_refs"], "ca_state.anchor_refs"),
        anchor_status=mapping["anchor_status"],
        current_decision_ref=mapping["current_decision_ref"],
        engagement_ref=mapping["engagement_ref"],
        succession_plan_ref=plan,
    )


def state_from_json(text: object) -> CaState:
    return state_from_mapping(_loads_mapping(text))


def rotation_from_mapping(mapping: dict[str, Any]) -> CaRotation:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_rotation")
    _check_bounded(mapping, _ROTATION_REQUIRED, _ROTATION_ALLOWED)
    return CaRotation(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        plan_ref=mapping["plan_ref"],
        plan_version=mapping["plan_version"],
        context_ref=mapping["context_ref"],
        domain=mapping["domain"],
        logical_authority=mapping["logical_authority"],
        emission_scope=mapping["emission_scope"],
        issuer_ref=mapping["issuer_ref"],
        from_generation_ref=mapping["from_generation_ref"],
        to_generation_ref=mapping["to_generation_ref"],
        offline_procedure_ref=mapping["offline_procedure_ref"],
        deadline_utc=_parse_time(mapping["deadline_utc"], "ca_rotation.deadline_utc"),
        status=mapping["status"],
        engaged_at_utc=_opt_time(mapping, "engaged_at_utc", "ca_rotation.engaged_at_utc"),
        engagement_ref=_opt_ref(mapping, "engagement_ref", "ca_rotation.engagement_ref"),
        exclusion_proof_ref=_opt_ref(mapping, "exclusion_proof_ref", "ca_rotation.exclusion_proof_ref"),
        withdrawn_at_utc=_opt_time(mapping, "withdrawn_at_utc", "ca_rotation.withdrawn_at_utc"),
    )


def rotation_from_json(text: object) -> CaRotation:
    return rotation_from_mapping(_loads_mapping(text))


def loss_from_mapping(mapping: dict[str, Any]) -> CaLoss:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_loss")
    _check_bounded(mapping, _LOSS_REQUIRED, _LOSS_ALLOWED)
    return CaLoss(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        loss_id=mapping["loss_id"],
        incident_version=mapping["incident_version"],
        context_ref=mapping["context_ref"],
        issuer_ref=mapping["issuer_ref"],
        lost_generation_ref=mapping["lost_generation_ref"],
        loss_class=mapping["loss_class"],
        detected_at_utc=_parse_time(mapping["detected_at_utc"], "ca_loss.detected_at_utc"),
        recovery_state=mapping["recovery_state"],
        replacement_generation_ref=_opt_ref(mapping, "replacement_generation_ref", "ca_loss.replacement_generation_ref"),
        offline_procedure_ref=_opt_ref(mapping, "offline_procedure_ref", "ca_loss.offline_procedure_ref"),
        reconciliation_ref=_opt_ref(mapping, "reconciliation_ref", "ca_loss.reconciliation_ref"),
    )


def loss_from_json(text: object) -> CaLoss:
    return loss_from_mapping(_loads_mapping(text))


def succession_from_mapping(mapping: dict[str, Any]) -> CaSuccession:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_succession")
    _check_bounded(mapping, _SUCCESSION_REQUIRED, _SUCCESSION_ALLOWED)
    return CaSuccession(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        plan_ref=mapping["plan_ref"],
        plan_version=mapping["plan_version"],
        context_ref=mapping["context_ref"],
        domain=mapping["domain"],
        scope_ref=mapping["scope_ref"],
        from_root_ref=mapping["from_root_ref"],
        to_root_ref=mapping["to_root_ref"],
        offline_procedure_ref=mapping["offline_procedure_ref"],
        deadline_utc=_parse_time(mapping["deadline_utc"], "ca_succession.deadline_utc"),
        anchor_bound_at_utc=_parse_time(mapping["anchor_bound_at_utc"], "ca_succession.anchor_bound_at_utc"),
        status=mapping["status"],
        engaged_at_utc=_opt_time(mapping, "engaged_at_utc", "ca_succession.engaged_at_utc"),
        withdraw_at_utc=_opt_time(mapping, "withdraw_at_utc", "ca_succession.withdraw_at_utc"),
        engagement_ref=_opt_ref(mapping, "engagement_ref", "ca_succession.engagement_ref"),
        withdrawn_at_utc=_opt_time(mapping, "withdrawn_at_utc", "ca_succession.withdrawn_at_utc"),
    )


def succession_from_json(text: object) -> CaSuccession:
    return succession_from_mapping(_loads_mapping(text))


def migration_from_mapping(mapping: dict[str, Any]) -> CaMigration:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_migration")
    _check_exact(mapping, _MIGRATION_FIELDS)
    return CaMigration(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        migration_id=mapping["migration_id"],
        succession_plan_ref=mapping["succession_plan_ref"],
        plan_version=mapping["plan_version"],
        domain=mapping["domain"],
        scope_ref=mapping["scope_ref"],
        from_anchor_ref=mapping["from_anchor_ref"],
        to_anchor_ref=mapping["to_anchor_ref"],
        engagement_ref=mapping["engagement_ref"],
        engaged_at_utc=_parse_time(mapping["engaged_at_utc"], "ca_migration.engaged_at_utc"),
        withdraw_at_utc=_parse_time(mapping["withdraw_at_utc"], "ca_migration.withdraw_at_utc"),
        anchor_bound_at_utc=_parse_time(mapping["anchor_bound_at_utc"], "ca_migration.anchor_bound_at_utc"),
        applied_observation_refs=_set_from_list(mapping["applied_observation_refs"], "ca_migration.applied_observation_refs"),
        status=mapping["status"],
    )


def migration_from_json(text: object) -> CaMigration:
    return migration_from_mapping(_loads_mapping(text))


def observation_from_mapping(mapping: dict[str, Any]) -> CaObservation:
    if type(mapping) is not dict:
        raise _deny("ENVELOPPE_JSON_INVALIDE", "ca_observation")
    _check_exact(mapping, _OBSERVATION_FIELDS)
    return CaObservation(
        object_type=mapping["object_type"],
        schema_version=mapping["schema_version"],
        observation_id=mapping["observation_id"],
        association_ref=mapping["association_ref"],
        plan_ref=mapping["plan_ref"],
        plan_version=mapping["plan_version"],
        domain=mapping["domain"],
        scope_ref=mapping["scope_ref"],
        target_anchor_ref=mapping["target_anchor_ref"],
        target_generation_ref=mapping["target_generation_ref"],
        observed_at_utc=_parse_time(mapping["observed_at_utc"], "ca_observation.observed_at_utc"),
        applied_proof_ref=mapping["applied_proof_ref"],
        epoch=mapping["epoch"],
    )


def observation_from_json(text: object) -> CaObservation:
    return observation_from_mapping(_loads_mapping(text))


def succession_upper_bound(succession: object) -> datetime.datetime:
    """Borne commune engagement+30j, deadline et ancre, sans flottant."""
    if type(succession) is not CaSuccession:
        raise _deny("TYPE_INVALIDE", "ca_succession")
    if succession.status not in ("engaged", "withdrawn"):
        raise _deny("STATUT_INVALIDE", "ca_succession.status")
    try:
        return _durations.coexistence_upper_bound(
            succession.engaged_at_utc,
            succession.deadline_utc,
            succession.anchor_bound_at_utc,
        )
    except _DurationsError as exc:
        raise _deny(exc.code, "ca_succession.withdraw_at_utc") from None


def check_migration_common_plan_fields(migration: object, succession: object) -> None:
    """Compare seulement champs communs ici, sans admission.

    Résolution réelle des ancres vers racines et appartenances restant
    au propriétaire ; ne compare ni from_anchor à from_root, ni lien
    cert/ancre prouvé.
    """
    if type(migration) is not CaMigration:
        raise _deny("TYPE_INVALIDE", "ca_migration")
    if type(succession) is not CaSuccession:
        raise _deny("TYPE_INVALIDE", "ca_succession")
    if migration.succession_plan_ref != succession.plan_ref:
        raise _deny("PLAN_INCOHERENT", "ca_migration.succession_plan_ref")
    if migration.plan_version != succession.plan_version:
        raise _deny("VERSION_INCOHERENTE", "ca_migration.plan_version")
    if migration.domain != succession.domain:
        raise _deny("DOMAINE_INCOHERENT", "ca_migration.domain")
    if migration.scope_ref != succession.scope_ref:
        raise _deny("PERIMETRE_INCOHERENT", "ca_migration.scope_ref")
    if succession.engagement_ref is not None and migration.engagement_ref != succession.engagement_ref:
        raise _deny("ENGAGEMENT_INCOHERENT", "ca_migration.engagement_ref")
    if migration.engaged_at_utc != succession.engaged_at_utc:
        raise _deny("DEBUT_INCOHERENT", "ca_migration.engaged_at_utc")
    if migration.withdraw_at_utc != succession.withdraw_at_utc:
        raise _deny("ECHEANCE_INCOHERENTE", "ca_migration.withdraw_at_utc")
    if migration.anchor_bound_at_utc != succession.anchor_bound_at_utc:
        raise _deny("BORNE_INCOHERENTE", "ca_migration.anchor_bound_at_utc")
    bound = succession_upper_bound(succession)
    if migration.withdraw_at_utc > bound:  # type: ignore[operator]
        raise _deny("BORNE_DEPASSEE", "ca_migration.withdraw_at_utc")
