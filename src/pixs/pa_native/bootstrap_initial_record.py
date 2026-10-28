"""Premier enregistrement bootstrap (forme et liaisons attendues seules).

Codec de donnees publiques : derivation deterministe du R0 depuis
plan.recipe et plan reels, canon trie compact, liaisons recalculees en
interne, tete semantique et recu physique attendus calcules sur les memes
octets valides, NV attendu derive de la base attendue et de la tete.
Ne constate aucune observation, lecture HMAC, autorite, admission ou effet.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from dataclasses import dataclass
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
    from .bootstrap_base import BootstrapBase
    from .bootstrap_base import BootstrapBaseContractError as BaseContractError
    from .bootstrap_base import bootstrap_base_binding as base_binding_real
    from .bootstrap_context import BootstrapTpmContext
    from .bootstrap_context import BootstrapContextContractError as CtxContractError
    from .bootstrap_context import bootstrap_context_binding as ctx_binding_real
    from .bootstrap_nv_profile import BootstrapNvProfile
    from .bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
    from .bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_real
    from .bootstrap_plan import BootstrapPlan
    from .bootstrap_plan import BootstrapPlanContractError as PlanContractError
    from .bootstrap_plan import bootstrap_plan_binding as plan_binding_real
    from .bootstrap_plan import encode_bootstrap_plan as plan_encode_real
    from .bootstrap_policy_profile import BootstrapPolicyProfile
    from .bootstrap_policy_profile import BootstrapPolicyProfileContractError as PolContractError
    from .bootstrap_prepublication import BootstrapPrepublicationEnvelope
    from .bootstrap_prepublication import BootstrapPrepublicationContractError as PubContractError
    from .bootstrap_recipe import bootstrap_recipe_binding as recipe_binding_real
    from .bootstrap_recipe import BootstrapRecipeContractError as RecContractError
    from .bootstrap_resource_profile import BootstrapResourceProfile
    from .bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_base" in sys.builtin_module_names
            and "bootstrap_context" in sys.builtin_module_names
            and "bootstrap_nv_profile" in sys.builtin_module_names
            and "bootstrap_plan" in sys.builtin_module_names
            and "bootstrap_policy_profile" in sys.builtin_module_names
            and "bootstrap_prepublication" in sys.builtin_module_names
            and "bootstrap_recipe" in sys.builtin_module_names
            and "bootstrap_resource_profile" in sys.builtin_module_names):
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from bootstrap_base import BootstrapBase
        from bootstrap_base import BootstrapBaseContractError as BaseContractError
        from bootstrap_base import bootstrap_base_binding as base_binding_real
        from bootstrap_context import BootstrapTpmContext
        from bootstrap_context import BootstrapContextContractError as CtxContractError
        from bootstrap_context import bootstrap_context_binding as ctx_binding_real
        from bootstrap_nv_profile import BootstrapNvProfile
        from bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
        from bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_real
        from bootstrap_plan import BootstrapPlan
        from bootstrap_plan import BootstrapPlanContractError as PlanContractError
        from bootstrap_plan import bootstrap_plan_binding as plan_binding_real
        from bootstrap_plan import encode_bootstrap_plan as plan_encode_real
        from bootstrap_policy_profile import BootstrapPolicyProfile
        from bootstrap_policy_profile import BootstrapPolicyProfileContractError as PolContractError
        from bootstrap_prepublication import BootstrapPrepublicationEnvelope
        from bootstrap_prepublication import BootstrapPrepublicationContractError as PubContractError
        from bootstrap_recipe import bootstrap_recipe_binding as recipe_binding_real
        from bootstrap_recipe import BootstrapRecipeContractError as RecContractError
        from bootstrap_resource_profile import BootstrapResourceProfile
        from bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
    else:
        raise ImportError("bootstrap_initial_record: unsupported package context")
else:
    raise ImportError("bootstrap_initial_record: unsupported package context")

__all__ = [
    "BootstrapInitialRecordContractError",
    "BootstrapInitialRecord",
    "derive_bootstrap_initial_record",
    "encode_bootstrap_initial_record",
    "decode_bootstrap_initial_record",
    "bootstrap_initial_record_binding",
    "bootstrap_initial_semantic_head_hex",
    "bootstrap_initial_physical_receipt_expected",
    "bootstrap_initial_expected_nv_hex",
]

_MSG = "bootstrap_initial_record: invalid value"
OBJECT_TYPE = "pixs.agent.bootstrap_initial_record/v1"
SCHEMA_VERSION = "1.0.0"
FIELD_NAMES = (
    "object_type", "schema_version", "transition_ref", "registry_ref",
    "registry_generation_ref", "epoch", "sequence", "correlation_refs",
    "causation_refs", "installation_ref", "target_ref",
    "prepublication_binding", "policy_binding", "resource_profile_binding",
    "nv_profile", "tpm_context_binding", "initial_base_binding",
    "plan_binding", "recipe_binding",
)
_STR_FIELDS = (
    "object_type", "schema_version", "transition_ref", "registry_ref",
    "registry_generation_ref", "installation_ref", "target_ref",
)
_BINDING_FIELDS = (
    "prepublication_binding", "policy_binding", "resource_profile_binding",
    "tpm_context_binding", "initial_base_binding", "plan_binding", "recipe_binding",
)
_NV_KEYS = frozenset(("nv_index", "nv_attributes", "nv_name_alg", "nv_data_size", "nv_authpolicy_hex", "nv_name_hex", "maintenance_p256_ref"))
_BINDING_KEYS = frozenset(("ref", "version", "sha256"))
_R0_PREFIX = b"PIXS:PA:BOOTSTRAP:INITIAL_RECORD:1.0.0"
_REC_PREFIX = b"PIXS:PA:JOURNAL:RECORD:1.0.0"
_UINT64_MAX = 18446744073709551615
_PRODUCER_ERRORS = (PlanContractError, RecContractError, BaseContractError, CtxContractError, PolContractError, PubContractError, ResContractError, NvContractError, PgContractError)


class BootstrapInitialRecordContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapInitialRecordContractError(_MSG) from None


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapInitialRecord:
    object_type: str
    schema_version: str
    transition_ref: str
    registry_ref: str
    registry_generation_ref: str
    epoch: int
    sequence: int
    correlation_refs: tuple[str, ...]
    causation_refs: tuple[str, ...]
    installation_ref: str
    target_ref: str
    prepublication_binding: ContentBinding
    policy_binding: ContentBinding
    resource_profile_binding: ContentBinding
    nv_profile: BootstrapNvProfile
    tpm_context_binding: ContentBinding
    initial_base_binding: ContentBinding
    plan_binding: ContentBinding
    recipe_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            raise BootstrapInitialRecordContractError(_MSG) from None
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            raise BootstrapInitialRecordContractError(_MSG) from None
        for name in ("transition_ref", "registry_ref", "registry_generation_ref", "installation_ref", "target_ref"):
            val = getattr(self, name)
            if type(val) is not str or val == "":
                raise BootstrapInitialRecordContractError(_MSG) from None
            for ch in val:
                o = ord(ch)
                if o < 32 or o == 127:
                    raise BootstrapInitialRecordContractError(_MSG) from None
            try:
                val.encode("utf-8")
            except UnicodeEncodeError:
                raise BootstrapInitialRecordContractError(_MSG) from None
        for name in ("epoch", "sequence"):
            val = getattr(self, name)
            if type(val) is not int or isinstance(val, bool) or val < 0 or val > _UINT64_MAX:
                raise BootstrapInitialRecordContractError(_MSG) from None
        for name in ("correlation_refs", "causation_refs"):
            val = getattr(self, name)
            if type(val) is not tuple:
                raise BootstrapInitialRecordContractError(_MSG) from None
            for item in val:
                if type(item) is not str or item == "":
                    raise BootstrapInitialRecordContractError(_MSG) from None
                for ch in item:
                    o = ord(ch)
                    if o < 32 or o == 127:
                        raise BootstrapInitialRecordContractError(_MSG) from None
                try:
                    item.encode("utf-8")
                except UnicodeEncodeError:
                    raise BootstrapInitialRecordContractError(_MSG) from None
        for name in _BINDING_FIELDS:
            item = getattr(self, name)
            if type(item) is not ContentBinding:
                raise BootstrapInitialRecordContractError(_MSG) from None
            try:
                ContentBinding(ref=item.ref, version=item.version, sha256=item.sha256)
            except PgContractError:
                raise BootstrapInitialRecordContractError(_MSG) from None
            except (TypeError, KeyError):
                raise BootstrapInitialRecordContractError(_MSG) from None
        nv = self.nv_profile
        if type(nv) is not BootstrapNvProfile:
            raise BootstrapInitialRecordContractError(_MSG) from None
        try:
            BootstrapNvProfile(nv_index=nv.nv_index, nv_attributes=nv.nv_attributes, nv_name_alg=nv.nv_name_alg, nv_data_size=nv.nv_data_size, nv_authpolicy_hex=nv.nv_authpolicy_hex, nv_name_hex=nv.nv_name_hex, maintenance_p256_ref=nv.maintenance_p256_ref)
        except NvContractError:
            raise BootstrapInitialRecordContractError(_MSG) from None
        except (TypeError, KeyError):
            raise BootstrapInitialRecordContractError(_MSG) from None


def _check_limits(limits: Any) -> None:
    if type(limits) is not PayloadLimits:
        _fail()
    for name in ("max_json_bytes", "max_ref_bytes", "max_observation_refs"):
        val = getattr(limits, name)
        if type(val) is not int or isinstance(val, bool) or val <= 0:
            _fail()


def _check_producers(r0_limits: Any, producer_limits: Any, resource: Any, plan: Any, env: Any, policy: Any, context: Any, base: Any) -> None:
    _check_limits(r0_limits)
    _check_limits(producer_limits)
    if type(resource) is not BootstrapResourceProfile:
        _fail()
    if type(plan) is not BootstrapPlan:
        _fail()
    if type(env) is not BootstrapPrepublicationEnvelope:
        _fail()
    if type(policy) is not BootstrapPolicyProfile:
        _fail()
    if type(context) is not BootstrapTpmContext:
        _fail()
    if type(base) is not BootstrapBase:
        _fail()


def _ref(text: Any, bound: int) -> None:
    if type(text) is not str or text == "":
        _fail()
    for ch in text:
        o = ord(ch)
        if o < 32 or o == 127:
            _fail()
    try:
        n = len(text.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapInitialRecordContractError(_MSG) from None
    if n > bound:
        _fail()


def _hex64(text: Any) -> None:
    if type(text) is not str or len(text) != 64:
        _fail()
    for ch in text:
        if ch not in "0123456789abcdef":
            _fail()


def _r0_json_bound(r0_limits: PayloadLimits, resource: BootstrapResourceProfile) -> int:
    return min(r0_limits.max_json_bytes, resource.payload_max_json_bytes, resource.max_record)


def _r0_ref_bound(r0_limits: PayloadLimits, resource: BootstrapResourceProfile) -> int:
    return min(r0_limits.max_ref_bytes, resource.payload_max_ref_bytes)


def _revalidated(plan: BootstrapPlan, producer_limits: PayloadLimits, env: Any, policy: Any, resource: Any, context: Any, base: Any) -> None:
    try:
        plan_encode_real(plan, producer_limits, env, policy, resource, context, base)
    except _PRODUCER_ERRORS:
        _fail()


def _recalculated(plan: BootstrapPlan, producer_limits: PayloadLimits, env: Any, policy: Any, resource: Any, context: Any, base: Any) -> tuple:
    try:
        pb = plan_binding_real(plan, producer_limits, env, policy, resource, context, base)
        rb = recipe_binding_real(plan.recipe, producer_limits, base, resource)
        bb = base_binding_real(base, producer_limits)
        cb = ctx_binding_real(context, producer_limits)
        nv_encode_real(plan.nv_profile, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    if plan.tpm_context_binding != cb:
        _fail()
    if plan.recipe.initial_base_binding != bb:
        _fail()
    if base.tpm_context_binding != cb:
        _fail()
    if base.nv_coordinates.nv_index != plan.nv_profile.nv_index:
        _fail()
    if base.nv_coordinates.nv_name_hex != plan.nv_profile.nv_name_hex:
        _fail()
    return (pb, rb)


def _check_intrinsic(value: Any) -> None:
    if type(value) is not BootstrapInitialRecord:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    for name in ("transition_ref", "registry_ref", "registry_generation_ref", "installation_ref", "target_ref"):
        item = getattr(value, name)
        if type(item) is not str or item == "":
            _fail()
        for ch in item:
            o = ord(ch)
            if o < 32 or o == 127:
                _fail()
        try:
            item.encode("utf-8")
        except UnicodeEncodeError:
            raise BootstrapInitialRecordContractError(_MSG) from None
    for name in ("epoch", "sequence"):
        item = getattr(value, name)
        if type(item) is not int or isinstance(item, bool) or item < 0 or item > _UINT64_MAX:
            _fail()
    for name in ("correlation_refs", "causation_refs"):
        item = getattr(value, name)
        if type(item) is not tuple:
            _fail()
        for entry in item:
            if type(entry) is not str or entry == "":
                _fail()
            for ch in entry:
                o = ord(ch)
                if o < 32 or o == 127:
                    _fail()
            try:
                entry.encode("utf-8")
            except UnicodeEncodeError:
                raise BootstrapInitialRecordContractError(_MSG) from None
    for name in _BINDING_FIELDS:
        item = getattr(value, name)
        if type(item) is not ContentBinding:
            _fail()
        try:
            ContentBinding(ref=item.ref, version=item.version, sha256=item.sha256)
        except PgContractError:
            _fail()
        except (TypeError, KeyError):
            _fail()
    nv = value.nv_profile
    if type(nv) is not BootstrapNvProfile:
        _fail()
    try:
        BootstrapNvProfile(nv_index=nv.nv_index, nv_attributes=nv.nv_attributes, nv_name_alg=nv.nv_name_alg, nv_data_size=nv.nv_data_size, nv_authpolicy_hex=nv.nv_authpolicy_hex, nv_name_hex=nv.nv_name_hex, maintenance_p256_ref=nv.maintenance_p256_ref)
    except NvContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()


def _check_bounds(value: BootstrapInitialRecord, r0_limits: PayloadLimits, resource: BootstrapResourceProfile, producer_limits: PayloadLimits) -> None:
    bound = _r0_ref_bound(r0_limits, resource)
    for name in ("transition_ref", "registry_ref", "registry_generation_ref", "installation_ref", "target_ref"):
        _ref(getattr(value, name), bound)
    if value.epoch > resource.max_epoch or value.sequence > resource.max_sequence:
        _fail()
    if len(value.correlation_refs) > resource.max_correlation_refs or len(value.causation_refs) > resource.max_causation_refs:
        _fail()
    for item in value.correlation_refs + value.causation_refs:
        _ref(item, bound)
    for name in _BINDING_FIELDS:
        item = getattr(value, name)
        _ref(item.ref, bound)
        _ref(item.version, bound)
        _hex64(item.sha256)
    try:
        nv_encode_real(value.nv_profile, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    for ch in value.nv_profile.maintenance_p256_ref:
        o = ord(ch)
        if o < 32 or o == 127:
            _fail()
    try:
        mlen = len(value.nv_profile.maintenance_p256_ref.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapInitialRecordContractError(_MSG) from None
    if mlen > bound:
        _fail()


def _expected_record(r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, env: Any, policy: Any, context: Any, base: Any) -> BootstrapInitialRecord:
    _revalidated(plan, producer_limits, env, policy, resource, context, base)
    pb, rb = _recalculated(plan, producer_limits, env, policy, resource, context, base)
    recipe = plan.recipe
    value = BootstrapInitialRecord(
        object_type=OBJECT_TYPE, schema_version=SCHEMA_VERSION,
        transition_ref=recipe.transition_ref, registry_ref=recipe.registry_ref,
        registry_generation_ref=recipe.registry_generation_ref, epoch=recipe.epoch, sequence=recipe.sequence,
        correlation_refs=tuple(recipe.correlation_refs), causation_refs=tuple(recipe.causation_refs),
        installation_ref=plan.installation_ref, target_ref=plan.target_ref,
        prepublication_binding=plan.prepublication_binding, policy_binding=plan.policy_binding,
        resource_profile_binding=plan.resource_profile_binding, nv_profile=plan.nv_profile,
        tpm_context_binding=plan.tpm_context_binding, initial_base_binding=recipe.initial_base_binding,
        plan_binding=pb, recipe_binding=rb,
    )
    _check_bounds(value, r0_limits, resource, producer_limits)
    return value


def _binding_payload(binding: ContentBinding) -> dict:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def _payload(value: BootstrapInitialRecord) -> dict:
    nv = value.nv_profile
    return {
        "object_type": value.object_type, "schema_version": value.schema_version,
        "transition_ref": value.transition_ref, "registry_ref": value.registry_ref,
        "registry_generation_ref": value.registry_generation_ref, "epoch": value.epoch, "sequence": value.sequence,
        "correlation_refs": list(value.correlation_refs), "causation_refs": list(value.causation_refs),
        "installation_ref": value.installation_ref, "target_ref": value.target_ref,
        "prepublication_binding": _binding_payload(value.prepublication_binding),
        "policy_binding": _binding_payload(value.policy_binding),
        "resource_profile_binding": _binding_payload(value.resource_profile_binding),
        "nv_profile": {"nv_index": nv.nv_index, "nv_attributes": nv.nv_attributes, "nv_name_alg": nv.nv_name_alg, "nv_data_size": nv.nv_data_size, "nv_authpolicy_hex": nv.nv_authpolicy_hex, "nv_name_hex": nv.nv_name_hex, "maintenance_p256_ref": nv.maintenance_p256_ref},
        "tpm_context_binding": _binding_payload(value.tpm_context_binding),
        "initial_base_binding": _binding_payload(value.initial_base_binding),
        "plan_binding": _binding_payload(value.plan_binding), "recipe_binding": _binding_payload(value.recipe_binding),
    }


def _canon(payload: dict, bound: int) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapInitialRecordContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > bound:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def _validated_canon(value: BootstrapInitialRecord, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, env: Any, policy: Any, context: Any, base: Any) -> bytes:
    _check_producers(r0_limits, producer_limits, resource, plan, env, policy, context, base)
    _check_intrinsic(value)
    expected = _expected_record(r0_limits, producer_limits, resource, plan, env, policy, context, base)
    if value != expected:
        _fail()
    _check_bounds(value, r0_limits, resource, producer_limits)
    return _canon(_payload(value), _r0_json_bound(r0_limits, resource)).encode("utf-8")


def derive_bootstrap_initial_record(*, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> BootstrapInitialRecord:
    _check_producers(r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    value = _expected_record(r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    _canon(_payload(value), _r0_json_bound(r0_limits, resource))
    return value


def encode_bootstrap_initial_record(value: BootstrapInitialRecord, *, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> str:
    return _validated_canon(value, r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base).decode("utf-8")


def _parse_int(token: str) -> int:
    if token[:1] == "-":
        _fail()
    if len(token) > 20:
        _fail()
    try:
        return int(token, 10)
    except ValueError:
        _fail()


def _reject_float(token: str) -> NoReturn:
    raise BootstrapInitialRecordContractError(_MSG) from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapInitialRecordContractError(_MSG) from None


def _pairs(pairs: list) -> dict:
    keys = [k for k, _ in pairs]
    if any(type(k) is not str for k in keys) or len(set(keys)) != len(keys):
        _fail()
    keyset = set(keys)
    if keyset == _BINDING_KEYS:
        for _, v in pairs:
            if type(v) is not str:
                _fail()
        return {k: v for k, v in pairs}
    if keyset == _NV_KEYS:
        return {k: v for k, v in pairs}
    if keyset == set(FIELD_NAMES):
        return {k: v for k, v in pairs}
    _fail()


def _nested_binding(data: Any) -> ContentBinding:
    if type(data) is not dict or set(data) != _BINDING_KEYS:
        _fail()
    try:
        return ContentBinding(ref=data["ref"], version=data["version"], sha256=data["sha256"])
    except PgContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()


def decode_bootstrap_initial_record(text: Any, *, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> BootstrapInitialRecord:
    _check_producers(r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    _revalidated(plan, producer_limits, prepublication_envelope, policy, resource, context, base)
    _recalculated(plan, producer_limits, prepublication_envelope, policy, resource, context, base)
    if type(text) is not str or text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapInitialRecordContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > _r0_json_bound(r0_limits, resource):
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    try:
        data = json.loads(text, object_pairs_hook=_pairs, parse_int=_parse_int, parse_float=_reject_float, parse_constant=_reject_constant)
    except BootstrapInitialRecordContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict or set(data) != set(FIELD_NAMES):
        _fail()
    for key in _STR_FIELDS:
        if type(data[key]) is not str:
            _fail()
    for key in ("epoch", "sequence"):
        if type(data[key]) is not int or isinstance(data[key], bool):
            _fail()
    for key in ("correlation_refs", "causation_refs"):
        if type(data[key]) is not list or any(type(i) is not str for i in data[key]):
            _fail()
    if type(data["nv_profile"]) is not dict or set(data["nv_profile"]) != _NV_KEYS:
        _fail()
    for key in _BINDING_FIELDS:
        if type(data[key]) is not dict:
            _fail()
    nvd = data["nv_profile"]
    try:
        nv = BootstrapNvProfile(nv_index=nvd["nv_index"], nv_attributes=nvd["nv_attributes"], nv_name_alg=nvd["nv_name_alg"], nv_data_size=nvd["nv_data_size"], nv_authpolicy_hex=nvd["nv_authpolicy_hex"], nv_name_hex=nvd["nv_name_hex"], maintenance_p256_ref=nvd["maintenance_p256_ref"])
    except NvContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        value = BootstrapInitialRecord(
            object_type=data["object_type"], schema_version=data["schema_version"],
            transition_ref=data["transition_ref"], registry_ref=data["registry_ref"],
            registry_generation_ref=data["registry_generation_ref"], epoch=data["epoch"], sequence=data["sequence"],
            correlation_refs=tuple(data["correlation_refs"]), causation_refs=tuple(data["causation_refs"]),
            installation_ref=data["installation_ref"], target_ref=data["target_ref"],
            prepublication_binding=_nested_binding(data["prepublication_binding"]),
            policy_binding=_nested_binding(data["policy_binding"]),
            resource_profile_binding=_nested_binding(data["resource_profile_binding"]),
            nv_profile=nv, tpm_context_binding=_nested_binding(data["tpm_context_binding"]),
            initial_base_binding=_nested_binding(data["initial_base_binding"]),
            plan_binding=_nested_binding(data["plan_binding"]), recipe_binding=_nested_binding(data["recipe_binding"]),
        )
    except BootstrapInitialRecordContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    expected = _expected_record(r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    if value != expected:
        _fail()
    _check_bounds(value, r0_limits, resource, producer_limits)
    _canon(_payload(value), _r0_json_bound(r0_limits, resource))
    return value


def bootstrap_initial_record_binding(value: BootstrapInitialRecord, *, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> ContentBinding:
    raw = _validated_canon(value, r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    digest = hashlib.sha256(raw).hexdigest()
    bound = _r0_ref_bound(r0_limits, resource)
    _ref(value.transition_ref, bound)
    _ref(value.schema_version, bound)
    try:
        return ContentBinding(ref=value.transition_ref, version=value.schema_version, sha256=digest)
    except PgContractError:
        _fail()


def bootstrap_initial_semantic_head_hex(value: BootstrapInitialRecord, *, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> str:
    raw = _validated_canon(value, r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    return hashlib.sha256(_R0_PREFIX + b"\n" + raw).hexdigest()


def bootstrap_initial_physical_receipt_expected(value: BootstrapInitialRecord, *, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> str:
    raw = _validated_canon(value, r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    return hashlib.sha256(_REC_PREFIX + b"\n" + b"\x00" * 32 + struct.pack(">I", len(raw)) + raw).hexdigest()


def bootstrap_initial_expected_nv_hex(value: BootstrapInitialRecord, *, r0_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase) -> str:
    raw = _validated_canon(value, r0_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base)
    head = bytes.fromhex(hashlib.sha256(_R0_PREFIX + b"\n" + raw).hexdigest())
    try:
        base_bytes = bytes.fromhex(base.expected_base_hex64)
    except ValueError:
        _fail()
    if len(base_bytes) != 32:
        _fail()
    return hashlib.sha256(base_bytes + head).hexdigest()
