from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    ContractError,
    PayloadLimits,
    TechnicalPlan,
    decode_plan,
    encode_plan,
    plan_sha256,
)
from pixs.pa_native.postgresql_observation import (
    ObservationManifest,
    ObservationContractError,
    decode_observation,
    encode_observation,
    observation_binding,
)
from pixs.pa_native.postgresql_preconditions import (
    PreconditionsManifest,
    PreconditionsContractError,
    PreconditionsLimits,
    decode_preconditions,
    encode_preconditions,
    preconditions_binding,
)
from pixs.pa_native.postgresql_effects import (
    EffectsManifest,
    EffectsContractError,
    decode_effects,
    encode_effects,
    effects_binding,
    effects_digest,
)
from .technical_projection import (
    ProjectionLimits,
    ProjectionService,
    ProjectionRole,
    ProjectionDatabase,
    ProjectionObservation,
    TechnicalProjection,
    TechnicalProjectionError,
    dump_projection_canonical,
    parse_projection_bytes,
    projection_sha256,
)


__all__ = [
    "PlanningBundleError",
    "PlanningBundleLimits",
    "PlanningBundle",
    "parse_planning_bundle",
    "dump_planning_bundle",
    "planning_bundle_sha256",
    "planning_bundle_binding",
]


_BUNDLE_SCHEMA = "pixs.agent.postgresql.planning_bundle"
_BUNDLE_VERSION = "1.0.0"
_BUNDLE_FIELDS = (
    "schema",
    "schema_version",
    "bundle_ref",
    "installation_ref",
    "target_ref",
    "planning_operation_id",
    "preparation_operation_id",
    "correlation_id",
    "projection_document",
    "projection_binding",
    "observation_document",
    "observation_binding",
    "plan_document",
    "plan_binding",
    "preconditions_document",
    "preconditions_binding",
    "effects_document",
    "effects_binding",
    "effects_digest",
)


class PlanningBundleError(ValueError):
    def __init__(self) -> None:
        super().__init__("Bundle planning C08 non verifiable.")
        self.code = "C08_PLANNING_BUNDLE_INVALID"
        self.element = "planning_bundle"
        self.step = "validate_planning_bundle"


@dataclass(frozen=True, slots=True)
class PlanningBundleLimits:
    payload: PayloadLimits
    projection_limits: ProjectionLimits
    preconditions_limits: PreconditionsLimits
    max_bundle_bytes: int

    def __post_init__(self) -> None:
        if type(self.payload) is not PayloadLimits:
            raise PlanningBundleError()
        if type(self.projection_limits) is not ProjectionLimits:
            raise PlanningBundleError()
        if type(self.preconditions_limits) is not PreconditionsLimits:
            raise PlanningBundleError()
        for name in (
            "max_bytes",
            "max_ref_bytes",
            "max_correlation_refs",
            "max_causation_refs",
        ):
            v = getattr(self.projection_limits, name)
            if type(v) is not int or v < 1:
                raise PlanningBundleError()
        if type(self.preconditions_limits.max_conditions) is not int:
            raise PlanningBundleError()
        if self.preconditions_limits.max_conditions < 1:
            raise PlanningBundleError()
        if type(self.max_bundle_bytes) is not int:
            raise PlanningBundleError()
        if self.max_bundle_bytes < 1:
            raise PlanningBundleError()


@dataclass(frozen=True, slots=True, repr=False)
class PlanningBundle:
    schema: str
    schema_version: str
    bundle_ref: str
    installation_ref: str
    target_ref: str
    planning_operation_id: str
    preparation_operation_id: str
    correlation_id: str
    projection_document: TechnicalProjection
    projection_binding: ContentBinding
    observation_document: ObservationManifest
    observation_binding: ContentBinding
    plan_document: TechnicalPlan
    plan_binding: ContentBinding
    preconditions_document: PreconditionsManifest
    preconditions_binding: ContentBinding
    effects_document: EffectsManifest
    effects_binding: ContentBinding
    effects_digest: str

    def __post_init__(self) -> None:
        _check_structure(self)


def _ref(value: str, maximum: int | None) -> None:
    if type(value) is not str or not value:
        raise PlanningBundleError()
    for ch in value:
        o = ord(ch)
        if o < 32 or o == 127 or 55296 <= o <= 57343:
            raise PlanningBundleError()
    try:
        n = len(value.encode("utf-8"))
    except UnicodeEncodeError as e:
        raise PlanningBundleError() from e
    if maximum is not None and n > maximum:
        raise PlanningBundleError()


def _digest(value: str) -> None:
    if type(value) is not str or len(value) != 64:
        raise PlanningBundleError()
    for c in value:
        if c not in "0123456789abcdef":
            raise PlanningBundleError()


def _pairs(pairs) -> dict:
    d = {}
    for k, v in pairs:
        if k in d:
            raise PlanningBundleError()
        d[k] = v
    return d


def _number(v) -> None:
    raise PlanningBundleError()


def _check_structure(value: PlanningBundle) -> None:
    if type(value) is not PlanningBundle:
        raise PlanningBundleError()
    if type(value.schema) is not str or value.schema != _BUNDLE_SCHEMA:
        raise PlanningBundleError()
    if type(value.schema_version) is not str:
        raise PlanningBundleError()
    if value.schema_version != _BUNDLE_VERSION:
        raise PlanningBundleError()
    for name in (
        "bundle_ref",
        "installation_ref",
        "target_ref",
        "planning_operation_id",
        "preparation_operation_id",
        "correlation_id",
    ):
        if type(getattr(value, name)) is not str:
            raise PlanningBundleError()
        if not getattr(value, name):
            raise PlanningBundleError()
    if type(value.projection_document) is not TechnicalProjection:
        raise PlanningBundleError()
    if type(value.projection_document.service) is not ProjectionService:
        raise PlanningBundleError()
    if type(value.projection_document.role) is not ProjectionRole:
        raise PlanningBundleError()
    if type(value.projection_document.database) is not ProjectionDatabase:
        raise PlanningBundleError()
    if type(value.projection_document.observation) is not ProjectionObservation:
        raise PlanningBundleError()
    if type(value.observation_document) is not ObservationManifest:
        raise PlanningBundleError()
    if type(value.plan_document) is not TechnicalPlan:
        raise PlanningBundleError()
    if type(value.preconditions_document) is not PreconditionsManifest:
        raise PlanningBundleError()
    if type(value.effects_document) is not EffectsManifest:
        raise PlanningBundleError()
    for name in (
        "projection_binding",
        "observation_binding",
        "plan_binding",
        "preconditions_binding",
        "effects_binding",
    ):
        if type(getattr(value, name)) is not ContentBinding:
            raise PlanningBundleError()
    if value.projection_binding.version != "1.0.0":
        raise PlanningBundleError()
    if value.observation_binding.version != "1.0.0":
        raise PlanningBundleError()
    if value.preconditions_binding.version != "1.0.0":
        raise PlanningBundleError()
    if value.effects_binding.version != "1.0.0":
        raise PlanningBundleError()
    if value.projection_binding.ref != value.projection_document.projection_ref:
        raise PlanningBundleError()
    if value.observation_binding.ref != value.observation_document.observation_ref:
        raise PlanningBundleError()
    if value.plan_binding.ref != value.plan_document.plan_ref:
        raise PlanningBundleError()
    if value.plan_binding.version != value.plan_document.plan_version:
        raise PlanningBundleError()
    if value.preconditions_binding.ref != (
        value.preconditions_document.preconditions_ref
    ):
        raise PlanningBundleError()
    if value.effects_binding.ref != value.effects_document.effects_ref:
        raise PlanningBundleError()
    _digest(value.effects_digest)
    if value.planning_operation_id == value.preparation_operation_id:
        raise PlanningBundleError()
    if value.preparation_operation_id != value.projection_document.operation_id:
        raise PlanningBundleError()
    if value.preparation_operation_id != value.plan_document.operation_id:
        raise PlanningBundleError()
    if value.preparation_operation_id != (
        value.preconditions_document.operation_id
    ):
        raise PlanningBundleError()
    if value.preparation_operation_id != value.effects_document.operation_id:
        raise PlanningBundleError()
    for doc in (
        value.projection_document,
        value.plan_document,
        value.preconditions_document,
        value.effects_document,
    ):
        if doc.installation_ref != value.installation_ref:
            raise PlanningBundleError()
        if doc.target_ref != value.target_ref:
            raise PlanningBundleError()
    if value.observation_document.installation_ref != value.installation_ref:
        raise PlanningBundleError()
    if value.observation_document.target_ref != value.target_ref:
        raise PlanningBundleError()
    if value.correlation_id != value.projection_document.correlation_id:
        raise PlanningBundleError()
    if value.correlation_id != value.plan_document.correlation_id:
        raise PlanningBundleError()
    if type(value.projection_document.allowed_effects) is not tuple:
        raise PlanningBundleError()
    if type(value.effects_document.allowed_effects) is not tuple:
        raise PlanningBundleError()
    if value.projection_document.allowed_effects != (
        value.effects_document.allowed_effects
    ):
        raise PlanningBundleError()
    if value.observation_document.inspection_operation_id == (
        value.planning_operation_id
    ):
        raise PlanningBundleError()
    if value.observation_document.inspection_operation_id == (
        value.preparation_operation_id
    ):
        raise PlanningBundleError()
    if value.plan_document.projection_ref != (
        value.projection_document.projection_ref
    ):
        raise PlanningBundleError()
    if value.plan_document.preconditions_ref != (
        value.preconditions_document.preconditions_ref
    ):
        raise PlanningBundleError()
    if value.plan_document.service_ref != value.projection_document.service.ref:
        raise PlanningBundleError()
    if value.plan_document.role_ref != value.projection_document.role.ref:
        raise PlanningBundleError()
    if value.plan_document.database_ref != (
        value.projection_document.database.ref
    ):
        raise PlanningBundleError()
    if value.plan_document.idempotency_key != (
        value.projection_document.idempotency_key
    ):
        raise PlanningBundleError()
    if value.plan_document.policy_ref != value.observation_document.policy_ref:
        raise PlanningBundleError()
    if value.preconditions_document.projection_binding != (
        value.projection_binding
    ):
        raise PlanningBundleError()
    if value.preconditions_document.observation_binding != (
        value.observation_binding
    ):
        raise PlanningBundleError()
    if value.effects_document.projection_binding != value.projection_binding:
        raise PlanningBundleError()
    for attr in ("runtime", "service", "role", "database"):
        obs_bind = getattr(
            value.observation_document.profile_bindings, attr
        )
        if attr == "runtime":
            if obs_bind.ref != value.projection_document.runtime_profile_ref:
                raise PlanningBundleError()
            if obs_bind.version != (
                value.projection_document.runtime_profile_version
            ):
                raise PlanningBundleError()
        else:
            proj_obj = getattr(value.projection_document, attr)
            if obs_bind.ref != proj_obj.profile_ref:
                raise PlanningBundleError()
            if obs_bind.version != proj_obj.profile_version:
                raise PlanningBundleError()
    if value.projection_document.observation.ref != value.observation_binding.ref:
        raise PlanningBundleError()
    if value.projection_document.observation.version != (
        value.observation_binding.version
    ):
        raise PlanningBundleError()
    if value.projection_document.observation.sha256 != (
        value.observation_binding.sha256
    ):
        raise PlanningBundleError()
    obs_by_kind = {}
    for r in value.observation_document.resources:
        if type(r.kind) is not str or r.kind in obs_by_kind:
            raise PlanningBundleError()
        obs_by_kind[r.kind] = r
    if set(obs_by_kind) != {"SOFTWARE", "CLUSTER", "SERVICE", "ROLE", "DATABASE"}:
        raise PlanningBundleError()
    guards = value.preconditions_document.resource_guards
    if type(guards) is not tuple or len(guards) != 5:
        raise PlanningBundleError()
    for g in guards:
        if type(g.kind) is not str or g.kind not in obs_by_kind:
            raise PlanningBundleError()
        obs_res = obs_by_kind[g.kind]
        if g.resource_ref != obs_res.resource_ref:
            raise PlanningBundleError()
        if g.kind in ("SOFTWARE", "CLUSTER", "SERVICE"):
            expect_profile = value.observation_document.profile_bindings.service
        elif g.kind == "ROLE":
            expect_profile = value.observation_document.profile_bindings.role
        else:
            expect_profile = (
                value.observation_document.profile_bindings.database
            )
        if g.profile_binding != expect_profile:
            raise PlanningBundleError()
    if guards[3].kind != "ROLE" or guards[4].kind != "DATABASE":
        raise PlanningBundleError()
    if guards[3].resource_ref != value.projection_document.role.ref:
        raise PlanningBundleError()
    if guards[4].resource_ref != value.projection_document.database.ref:
        raise PlanningBundleError()
    service_guard = None
    for g in guards:
        if g.kind == "SERVICE":
            service_guard = g
    if service_guard is None:
        raise PlanningBundleError()
    if service_guard.resource_ref != value.projection_document.service.ref:
        raise PlanningBundleError()
    if service_guard.resource_ref != value.plan_document.service_ref:
        raise PlanningBundleError()
    if guards[3].resource_ref != value.plan_document.role_ref:
        raise PlanningBundleError()
    if guards[4].resource_ref != value.plan_document.database_ref:
        raise PlanningBundleError()
    conds = value.preconditions_document.conditions
    if type(conds) is not tuple:
        raise PlanningBundleError()
    if len(conds) == 0:
        if len(value.effects_document.allowed_effects) != 0:
            raise PlanningBundleError()
    guard_by_kind = {}
    for g in guards:
        guard_by_kind[g.kind] = g
    for cond in conds:
        if cond.effect not in value.effects_document.allowed_effects:
            raise PlanningBundleError()
        if type(cond.resource_kind) is not str:
            raise PlanningBundleError()
        if cond.resource_kind not in guard_by_kind:
            raise PlanningBundleError()
        guard = guard_by_kind[cond.resource_kind]
        if cond.resource_ref != guard.resource_ref:
            raise PlanningBundleError()
        if cond.profile_binding != guard.profile_binding:
            raise PlanningBundleError()
        if cond.evidence_binding is None:
            ok_null = (
                cond.resource_kind == "ROLE"
                and cond.effect == "ROLE_CREATE"
            ) or (
                cond.resource_kind == "DATABASE"
                and cond.effect == "DATABASE_CREATE"
            )
            if not ok_null:
                raise PlanningBundleError()
            if cond.check_stage != "AFTER_SERVICE_START_BEFORE_EFFECT":
                raise PlanningBundleError()
            obs_target = obs_by_kind[cond.resource_kind]
            if obs_target.state != "UNOBSERVABLE":
                raise PlanningBundleError()
            if "SERVICE_START" not in value.effects_document.allowed_effects:
                raise PlanningBundleError()


def _check_bounded(
    value: PlanningBundle, limits: PlanningBundleLimits
) -> None:
    if type(limits) is not PlanningBundleLimits:
        raise PlanningBundleError()
    _check_structure(value)
    maximum = limits.payload.max_ref_bytes
    for name in (
        "bundle_ref",
        "installation_ref",
        "target_ref",
        "planning_operation_id",
        "preparation_operation_id",
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
    _digest(value.effects_digest)
    try:
        expect_proj = projection_sha256(
            value.projection_document, limits.projection_limits
        )
    except TechnicalProjectionError as e:
        raise PlanningBundleError() from e
    if value.projection_binding.sha256 != expect_proj:
        raise PlanningBundleError()
    try:
        expect_obs = observation_binding(
            value.observation_document, limits.payload
        )
    except ObservationContractError as e:
        raise PlanningBundleError() from e
    if (
        expect_obs.ref != value.observation_binding.ref
        or expect_obs.version != value.observation_binding.version
        or expect_obs.sha256 != value.observation_binding.sha256
    ):
        raise PlanningBundleError()
    try:
        expect_plan_sha = plan_sha256(value.plan_document, limits.payload)
    except ContractError as e:
        raise PlanningBundleError() from e
    if value.plan_binding.sha256 != expect_plan_sha:
        raise PlanningBundleError()
    try:
        expect_pre = preconditions_binding(
            value.preconditions_document, limits.preconditions_limits
        )
    except PreconditionsContractError as e:
        raise PlanningBundleError() from e
    if (
        expect_pre.ref != value.preconditions_binding.ref
        or expect_pre.version != value.preconditions_binding.version
        or expect_pre.sha256 != value.preconditions_binding.sha256
    ):
        raise PlanningBundleError()
    try:
        expect_eff = effects_binding(value.effects_document, limits.payload)
    except EffectsContractError as e:
        raise PlanningBundleError() from e
    if (
        expect_eff.ref != value.effects_binding.ref
        or expect_eff.version != value.effects_binding.version
        or expect_eff.sha256 != value.effects_binding.sha256
    ):
        raise PlanningBundleError()
    try:
        expect_digest = effects_digest(value.effects_document, limits.payload)
    except EffectsContractError as e:
        raise PlanningBundleError() from e
    if value.effects_digest != expect_digest:
        raise PlanningBundleError()


def _decode_outer(raw: bytes, limits: PlanningBundleLimits) -> dict:
    if type(raw) is not bytes or not raw:
        raise PlanningBundleError()
    if len(raw) > limits.max_bundle_bytes:
        raise PlanningBundleError()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise PlanningBundleError() from e
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise PlanningBundleError() from e
    if type(doc) is not dict:
        raise PlanningBundleError()
    return doc


def _encode_outer(doc: dict, limits: PlanningBundleLimits) -> bytes:
    try:
        text = json.dumps(
            doc,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError as e:
        raise PlanningBundleError() from e
    if len(raw) > limits.max_bundle_bytes:
        raise PlanningBundleError()
    return raw


def parse_planning_bundle(
    raw: bytes, limits: PlanningBundleLimits
) -> PlanningBundle:
    if type(limits) is not PlanningBundleLimits:
        raise PlanningBundleError()
    doc = _decode_outer(raw, limits)
    if set(doc) != set(_BUNDLE_FIELDS):
        raise PlanningBundleError()
    if type(doc["schema"]) is not str or doc["schema"] != _BUNDLE_SCHEMA:
        raise PlanningBundleError()
    if type(doc["schema_version"]) is not str:
        raise PlanningBundleError()
    if doc["schema_version"] != _BUNDLE_VERSION:
        raise PlanningBundleError()
    for name in (
        "projection_document",
        "observation_document",
        "plan_document",
        "preconditions_document",
        "effects_document",
    ):
        if type(doc[name]) is not dict:
            raise PlanningBundleError()
    for name in (
        "projection_binding",
        "observation_binding",
        "plan_binding",
        "preconditions_binding",
        "effects_binding",
    ):
        b = doc[name]
        if type(b) is not dict or set(b) != {"ref", "version", "sha256"}:
            raise PlanningBundleError()
    try:
        proj_text = json.dumps(
            doc["projection_document"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        proj = parse_projection_bytes(
            proj_text.encode("utf-8"), limits.projection_limits
        )
    except (TechnicalProjectionError, UnicodeEncodeError) as e:
        raise PlanningBundleError() from e
    try:
        obs_text = json.dumps(
            doc["observation_document"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        obs = decode_observation(obs_text, limits.payload)
    except ObservationContractError as e:
        raise PlanningBundleError() from e
    try:
        plan_text = json.dumps(
            doc["plan_document"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        plan = decode_plan(plan_text, limits.payload)
    except ContractError as e:
        raise PlanningBundleError() from e
    try:
        pre_text = json.dumps(
            doc["preconditions_document"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        pre = decode_preconditions(pre_text, limits.preconditions_limits)
    except PreconditionsContractError as e:
        raise PlanningBundleError() from e
    try:
        eff_text = json.dumps(
            doc["effects_document"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        eff = decode_effects(eff_text, limits.payload)
    except EffectsContractError as e:
        raise PlanningBundleError() from e
    try:
        proj_bind = ContentBinding(**doc["projection_binding"])
        obs_bind = ContentBinding(**doc["observation_binding"])
        plan_bind = ContentBinding(**doc["plan_binding"])
        pre_bind = ContentBinding(**doc["preconditions_binding"])
        eff_bind = ContentBinding(**doc["effects_binding"])
    except ContractError as e:
        raise PlanningBundleError() from e
    value = PlanningBundle(
        schema=doc["schema"],
        schema_version=doc["schema_version"],
        bundle_ref=doc["bundle_ref"],
        installation_ref=doc["installation_ref"],
        target_ref=doc["target_ref"],
        planning_operation_id=doc["planning_operation_id"],
        preparation_operation_id=doc["preparation_operation_id"],
        correlation_id=doc["correlation_id"],
        projection_document=proj,
        projection_binding=proj_bind,
        observation_document=obs,
        observation_binding=obs_bind,
        plan_document=plan,
        plan_binding=plan_bind,
        preconditions_document=pre,
        preconditions_binding=pre_bind,
        effects_document=eff,
        effects_binding=eff_bind,
        effects_digest=doc["effects_digest"],
    )
    _check_bounded(value, limits)
    if dump_planning_bundle(value, limits) != raw:
        raise PlanningBundleError()
    return value


def dump_planning_bundle(
    value: PlanningBundle, limits: PlanningBundleLimits
) -> bytes:
    if type(limits) is not PlanningBundleLimits:
        raise PlanningBundleError()
    _check_bounded(value, limits)
    try:
        proj_raw = dump_projection_canonical(
            value.projection_document, limits.projection_limits
        )
    except TechnicalProjectionError as e:
        raise PlanningBundleError() from e
    try:
        proj_doc = json.loads(
            proj_raw.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        RecursionError,
    ) as e:
        raise PlanningBundleError() from e
    try:
        obs_text = encode_observation(value.observation_document, limits.payload)
    except ObservationContractError as e:
        raise PlanningBundleError() from e
    try:
        obs_doc = json.loads(
            obs_text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        plan_text = encode_plan(value.plan_document, limits.payload)
    except ContractError as e:
        raise PlanningBundleError() from e
    try:
        plan_doc = json.loads(
            plan_text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        pre_text = encode_preconditions(
            value.preconditions_document, limits.preconditions_limits
        )
    except PreconditionsContractError as e:
        raise PlanningBundleError() from e
    try:
        pre_doc = json.loads(
            pre_text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise PlanningBundleError() from e
    try:
        eff_text = encode_effects(value.effects_document, limits.payload)
    except EffectsContractError as e:
        raise PlanningBundleError() from e
    try:
        eff_doc = json.loads(
            eff_text,
            object_pairs_hook=_pairs,
            parse_int=_number,
            parse_float=_number,
            parse_constant=_number,
        )
    except (json.JSONDecodeError, RecursionError) as e:
        raise PlanningBundleError() from e
    doc = {
        "schema": value.schema,
        "schema_version": value.schema_version,
        "bundle_ref": value.bundle_ref,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "planning_operation_id": value.planning_operation_id,
        "preparation_operation_id": value.preparation_operation_id,
        "correlation_id": value.correlation_id,
        "projection_document": proj_doc,
        "projection_binding": {
            "ref": value.projection_binding.ref,
            "version": value.projection_binding.version,
            "sha256": value.projection_binding.sha256,
        },
        "observation_document": obs_doc,
        "observation_binding": {
            "ref": value.observation_binding.ref,
            "version": value.observation_binding.version,
            "sha256": value.observation_binding.sha256,
        },
        "plan_document": plan_doc,
        "plan_binding": {
            "ref": value.plan_binding.ref,
            "version": value.plan_binding.version,
            "sha256": value.plan_binding.sha256,
        },
        "preconditions_document": pre_doc,
        "preconditions_binding": {
            "ref": value.preconditions_binding.ref,
            "version": value.preconditions_binding.version,
            "sha256": value.preconditions_binding.sha256,
        },
        "effects_document": eff_doc,
        "effects_binding": {
            "ref": value.effects_binding.ref,
            "version": value.effects_binding.version,
            "sha256": value.effects_binding.sha256,
        },
        "effects_digest": value.effects_digest,
    }
    return _encode_outer(doc, limits)


def planning_bundle_sha256(
    value: PlanningBundle, limits: PlanningBundleLimits
) -> str:
    return hashlib.sha256(dump_planning_bundle(value, limits)).hexdigest()


def planning_bundle_binding(
    value: PlanningBundle, limits: PlanningBundleLimits
) -> ContentBinding:
    _check_bounded(value, limits)
    digest = planning_bundle_sha256(value, limits)
    try:
        return ContentBinding(
            ref=value.bundle_ref, version="1.0.0", sha256=digest
        )
    except ContractError as e:
        raise PlanningBundleError() from e
