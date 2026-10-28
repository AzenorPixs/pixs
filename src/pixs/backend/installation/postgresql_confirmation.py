"""Codec confirmation C08 1.0.0 : forme et octets seulement, sans consentement prouve, autorite, signature, fraicheur ni retrait administratif."""

from __future__ import annotations

from dataclasses import dataclass
import datetime
import hashlib
import json

from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError,
    PayloadLimits,
)
from .planning_bundle import (
    PlanningBundle,
    PlanningBundleLimits,
    PlanningBundleError,
    dump_planning_bundle,
)


__all__ = [
    "ConfirmationError",
    "ConfirmationLimits",
    "Confirmation",
    "parse_confirmation",
    "dump_confirmation",
    "confirmation_sha256",
    "confirmation_binding",
    "match_confirmation_bundle",
]


_CONF_SCHEMA = "pixs.c08.postgresql-confirmation.v1"
_CONF_VERSION = "1.0.0"
_CONF_FIELDS = (
    "schema",
    "schema_version",
    "confirmation_ref",
    "installation_ref",
    "target_ref",
    "operation_id",
    "operator_ref",
    "projection_binding",
    "observation_binding",
    "plan_binding",
    "preconditions_binding",
    "effects_binding",
    "policy_ref",
    "policy_version",
    "confirmed_at",
    "correlation_id",
)


class ConfirmationError(ValueError):
    def __init__(self) -> None:
        super().__init__("Confirmation C08 non verifiable.")
        self.code = "C08_CONFIRMATION_INVALID"
        self.element = "confirmation"
        self.step = "validate_confirmation"


@dataclass(frozen=True, slots=True)
class ConfirmationLimits:
    payload: PayloadLimits
    max_confirmation_bytes: int

    def __post_init__(self) -> None:
        if type(self.payload) is not PayloadLimits:
            raise ConfirmationError()
        if type(self.max_confirmation_bytes) is not int:
            raise ConfirmationError()
        if self.max_confirmation_bytes < 1:
            raise ConfirmationError()


@dataclass(frozen=True, slots=True, repr=False)
class Confirmation:
    schema: str
    schema_version: str
    confirmation_ref: str
    installation_ref: str
    target_ref: str
    operation_id: str
    operator_ref: str
    projection_binding: ContentBinding
    observation_binding: ContentBinding
    plan_binding: ContentBinding
    preconditions_binding: ContentBinding
    effects_binding: ContentBinding
    policy_ref: str
    policy_version: str
    confirmed_at: str
    correlation_id: str

    def __post_init__(self) -> None:
        _check_structure(self)


def _ref(value: str, maximum: int | None) -> None:
    if type(value) is not str or not value:
        raise ConfirmationError()
    for ch in value:
        o = ord(ch)
        if o < 32 or o == 127 or 55296 <= o <= 57343:
            raise ConfirmationError()
    try:
        n = len(value.encode("utf-8"))
    except UnicodeEncodeError as e:
        raise ConfirmationError() from e
    if maximum is not None and n > maximum:
        raise ConfirmationError()


def _digest(value: str) -> None:
    if type(value) is not str or len(value) != 64:
        raise ConfirmationError()
    for c in value:
        if c not in "0123456789abcdef":
            raise ConfirmationError()


def _confirmed_at(value: str) -> None:
    if type(value) is not str or len(value) != 27:
        raise ConfirmationError()
    if (
        value[4] != "-"
        or value[7] != "-"
        or value[10] != "T"
        or value[13] != ":"
        or value[16] != ":"
        or value[19] != "."
        or value[26] != "Z"
    ):
        raise ConfirmationError()
    digits = value[0:4] + value[5:7] + value[8:10]
    digits = digits + value[11:13] + value[14:16] + value[17:19]
    digits = digits + value[20:26]
    for c in digits:
        if c not in "0123456789":
            raise ConfirmationError()
    try:
        datetime.datetime(
            int(value[0:4]),
            int(value[5:7]),
            int(value[8:10]),
            int(value[11:13]),
            int(value[14:16]),
            int(value[17:19]),
            int(value[20:26]),
        )
    except ValueError as e:
        raise ConfirmationError() from e


def _pairs(pairs) -> dict:
    d = {}
    for k, v in pairs:
        if k in d:
            raise ConfirmationError()
        d[k] = v
    return d


def _number(v) -> None:
    raise ConfirmationError()


def _check_structure(value: Confirmation) -> None:
    if type(value) is not Confirmation:
        raise ConfirmationError()
    if type(value.schema) is not str or value.schema != _CONF_SCHEMA:
        raise ConfirmationError()
    if type(value.schema_version) is not str:
        raise ConfirmationError()
    if value.schema_version != _CONF_VERSION:
        raise ConfirmationError()
    for name in (
        "confirmation_ref",
        "installation_ref",
        "target_ref",
        "operation_id",
        "operator_ref",
        "policy_ref",
        "policy_version",
        "correlation_id",
    ):
        if type(getattr(value, name)) is not str:
            raise ConfirmationError()
        if not getattr(value, name):
            raise ConfirmationError()
    for name in (
        "projection_binding",
        "observation_binding",
        "plan_binding",
        "preconditions_binding",
        "effects_binding",
    ):
        if type(getattr(value, name)) is not ContentBinding:
            raise ConfirmationError()
    if value.projection_binding.version != "1.0.0":
        raise ConfirmationError()
    if value.observation_binding.version != "1.0.0":
        raise ConfirmationError()
    if type(value.plan_binding.version) is not str:
        raise ConfirmationError()
    if not value.plan_binding.version:
        raise ConfirmationError()
    if value.preconditions_binding.version != "1.0.0":
        raise ConfirmationError()
    if value.effects_binding.version != "1.0.0":
        raise ConfirmationError()
    _digest(value.projection_binding.sha256)
    _digest(value.observation_binding.sha256)
    _digest(value.plan_binding.sha256)
    _digest(value.preconditions_binding.sha256)
    _digest(value.effects_binding.sha256)
    _confirmed_at(value.confirmed_at)


def _check_bounded(value: Confirmation, limits: ConfirmationLimits) -> None:
    if type(limits) is not ConfirmationLimits:
        raise ConfirmationError()
    _check_structure(value)
    maximum = limits.payload.max_ref_bytes
    for name in (
        "confirmation_ref",
        "installation_ref",
        "target_ref",
        "operation_id",
        "operator_ref",
        "policy_ref",
        "policy_version",
        "correlation_id",
    ):
        _ref(getattr(value, name), maximum)
    for bname in (
        "projection_binding",
        "observation_binding",
        "plan_binding",
        "preconditions_binding",
        "effects_binding",
    ):
        b = getattr(value, bname)
        _ref(b.ref, maximum)
        _ref(b.version, maximum)
        _digest(b.sha256)


def _decode_outer(raw: bytes, limits: ConfirmationLimits) -> dict:
    if type(raw) is not bytes or not raw:
        raise ConfirmationError()
    if len(raw) > limits.max_confirmation_bytes:
        raise ConfirmationError()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ConfirmationError() from e
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise ConfirmationError() from e
    if type(doc) is not dict:
        raise ConfirmationError()
    return doc


def _encode_outer(doc: dict, limits: ConfirmationLimits) -> bytes:
    try:
        text = json.dumps(
            doc,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise ConfirmationError() from e
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError as e:
        raise ConfirmationError() from e
    if len(raw) > limits.max_confirmation_bytes:
        raise ConfirmationError()
    return raw


def parse_confirmation(
    raw: bytes, limits: ConfirmationLimits
) -> Confirmation:
    if type(limits) is not ConfirmationLimits:
        raise ConfirmationError()
    doc = _decode_outer(raw, limits)
    if set(doc) != set(_CONF_FIELDS):
        raise ConfirmationError()
    for name in (
        "confirmation_ref",
        "installation_ref",
        "target_ref",
        "operation_id",
        "operator_ref",
        "policy_ref",
        "policy_version",
        "correlation_id",
        "confirmed_at",
    ):
        if type(doc[name]) is not str:
            raise ConfirmationError()
    for name in (
        "projection_binding",
        "observation_binding",
        "plan_binding",
        "preconditions_binding",
        "effects_binding",
    ):
        b = doc[name]
        if type(b) is not dict or set(b) != {"ref", "version", "sha256"}:
            raise ConfirmationError()
    try:
        proj_bind = ContentBinding(**doc["projection_binding"])
        obs_bind = ContentBinding(**doc["observation_binding"])
        plan_bind = ContentBinding(**doc["plan_binding"])
        pre_bind = ContentBinding(**doc["preconditions_binding"])
        eff_bind = ContentBinding(**doc["effects_binding"])
    except ContractError as e:
        raise ConfirmationError() from e
    value = Confirmation(
        schema=doc["schema"],
        schema_version=doc["schema_version"],
        confirmation_ref=doc["confirmation_ref"],
        installation_ref=doc["installation_ref"],
        target_ref=doc["target_ref"],
        operation_id=doc["operation_id"],
        operator_ref=doc["operator_ref"],
        projection_binding=proj_bind,
        observation_binding=obs_bind,
        plan_binding=plan_bind,
        preconditions_binding=pre_bind,
        effects_binding=eff_bind,
        policy_ref=doc["policy_ref"],
        policy_version=doc["policy_version"],
        confirmed_at=doc["confirmed_at"],
        correlation_id=doc["correlation_id"],
    )
    _check_bounded(value, limits)
    if dump_confirmation(value, limits) != raw:
        raise ConfirmationError()
    return value


def dump_confirmation(
    value: Confirmation, limits: ConfirmationLimits
) -> bytes:
    if type(limits) is not ConfirmationLimits:
        raise ConfirmationError()
    _check_bounded(value, limits)
    doc = {
        "schema": value.schema,
        "schema_version": value.schema_version,
        "confirmation_ref": value.confirmation_ref,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "operation_id": value.operation_id,
        "operator_ref": value.operator_ref,
        "projection_binding": {
            "ref": value.projection_binding.ref,
            "version": value.projection_binding.version,
            "sha256": value.projection_binding.sha256,
        },
        "observation_binding": {
            "ref": value.observation_binding.ref,
            "version": value.observation_binding.version,
            "sha256": value.observation_binding.sha256,
        },
        "plan_binding": {
            "ref": value.plan_binding.ref,
            "version": value.plan_binding.version,
            "sha256": value.plan_binding.sha256,
        },
        "preconditions_binding": {
            "ref": value.preconditions_binding.ref,
            "version": value.preconditions_binding.version,
            "sha256": value.preconditions_binding.sha256,
        },
        "effects_binding": {
            "ref": value.effects_binding.ref,
            "version": value.effects_binding.version,
            "sha256": value.effects_binding.sha256,
        },
        "policy_ref": value.policy_ref,
        "policy_version": value.policy_version,
        "confirmed_at": value.confirmed_at,
        "correlation_id": value.correlation_id,
    }
    return _encode_outer(doc, limits)


def confirmation_sha256(
    value: Confirmation, limits: ConfirmationLimits
) -> str:
    return hashlib.sha256(dump_confirmation(value, limits)).hexdigest()


def confirmation_binding(
    value: Confirmation, limits: ConfirmationLimits
) -> ContentBinding:
    _check_bounded(value, limits)
    digest = confirmation_sha256(value, limits)
    try:
        return ContentBinding(
            ref=value.confirmation_ref, version="1.0.0", sha256=digest
        )
    except ContractError as e:
        raise ConfirmationError() from e


def match_confirmation_bundle(
    value: Confirmation,
    limits: ConfirmationLimits,
    bundle: PlanningBundle,
    bundle_limits: PlanningBundleLimits,
) -> None:
    dump_confirmation(value, limits)
    try:
        dump_planning_bundle(bundle, bundle_limits)
    except PlanningBundleError as e:
        raise ConfirmationError() from e
    if value.confirmation_ref != bundle.plan_document.confirmation_ref:
        raise ConfirmationError()
    if value.installation_ref != bundle.installation_ref:
        raise ConfirmationError()
    if value.target_ref != bundle.target_ref:
        raise ConfirmationError()
    if value.operation_id != bundle.preparation_operation_id:
        raise ConfirmationError()
    if value.correlation_id != bundle.correlation_id:
        raise ConfirmationError()
    if value.projection_binding != bundle.projection_binding:
        raise ConfirmationError()
    if value.observation_binding != bundle.observation_binding:
        raise ConfirmationError()
    if value.plan_binding != bundle.plan_binding:
        raise ConfirmationError()
    if value.preconditions_binding != bundle.preconditions_binding:
        raise ConfirmationError()
    if value.effects_binding != bundle.effects_binding:
        raise ConfirmationError()
    if value.policy_ref != bundle.plan_document.policy_ref:
        raise ConfirmationError()
    if value.policy_ref != bundle.observation_document.policy_ref:
        raise ConfirmationError()
    if value.policy_version != bundle.observation_document.policy_version:
        raise ConfirmationError()
    return None
