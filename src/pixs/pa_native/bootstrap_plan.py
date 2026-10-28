"""Plan BootstrapPlan/v1 (15 champs).

FORME pure proposee, code NON QUALIFIE : sans admission, acte,
autorite, execution, TPM, PG, PZT, crypto, horloge ni qualification.
15 valeurs strictes, canon trie compact, liaisons de forme vers
objets reels existants : enveloppe entiere de prepublication,
Policy14, Resource24, Context8, Base8 et Recipe13 embarquee.
PayloadLimits externe borne JSON et references ; Resource24 reelle epingle
contexte et borne nombres et traces via Recipe ; ces egalites sont de la
coherence de forme contre les producteurs fournis, jamais une preuve
d'origine protegee.
Sans clock, deadline JSON, first_head, plan parent, cycle, port,
NV, SQL, ni defaut de production.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
    from .bootstrap_base import BootstrapBase
    from .bootstrap_base import BootstrapBaseContractError as BaseContractError
    from .bootstrap_base import bootstrap_base_binding as base_binding_public
    from .bootstrap_base import encode_bootstrap_base as base_encode_public
    from .bootstrap_context import BootstrapTpmContext
    from .bootstrap_context import BootstrapContextContractError as CtxContractError
    from .bootstrap_context import bootstrap_context_binding as ctx_binding_public
    from .bootstrap_context import encode_bootstrap_context as ctx_encode_public
    from .bootstrap_nv_profile import BootstrapNvProfile
    from .bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
    from .bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_public
    from .bootstrap_policy_profile import BootstrapPolicyProfile
    from .bootstrap_policy_profile import BootstrapPolicyProfileContractError as PolContractError
    from .bootstrap_policy_profile import bootstrap_policy_profile_binding as pol_binding_public
    from .bootstrap_policy_profile import encode_bootstrap_policy_profile as pol_encode_public
    from .bootstrap_prepublication import BootstrapPrepublicationEnvelope
    from .bootstrap_prepublication import BootstrapPrepublicationContractError as PubContractError
    from .bootstrap_prepublication import encode_bootstrap_prepublication_envelope as pub_encode_public
    from .bootstrap_prepublication import prepublication_envelope_binding as pub_binding_public
    from .bootstrap_recipe import BootstrapRecipe
    from .bootstrap_recipe import BootstrapRecipeContractError as RecContractError
    from .bootstrap_recipe import encode_bootstrap_recipe as rec_encode_public
    from .bootstrap_resource_profile import BootstrapResourceProfile
    from .bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
    from .bootstrap_resource_profile import bootstrap_resource_profile_binding as res_binding_public
    from .bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_base" in sys.builtin_module_names
            and "bootstrap_context" in sys.builtin_module_names
            and "bootstrap_nv_profile" in sys.builtin_module_names
            and "bootstrap_policy_profile" in sys.builtin_module_names
            and "bootstrap_prepublication" in sys.builtin_module_names
            and "bootstrap_recipe" in sys.builtin_module_names
            and "bootstrap_resource_profile" in sys.builtin_module_names):
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from bootstrap_base import BootstrapBase
        from bootstrap_base import BootstrapBaseContractError as BaseContractError
        from bootstrap_base import bootstrap_base_binding as base_binding_public
        from bootstrap_base import encode_bootstrap_base as base_encode_public
        from bootstrap_context import BootstrapTpmContext
        from bootstrap_context import BootstrapContextContractError as CtxContractError
        from bootstrap_context import bootstrap_context_binding as ctx_binding_public
        from bootstrap_context import encode_bootstrap_context as ctx_encode_public
        from bootstrap_nv_profile import BootstrapNvProfile
        from bootstrap_nv_profile import BootstrapNvProfileContractError as NvContractError
        from bootstrap_nv_profile import encode_bootstrap_nv_profile as nv_encode_public
        from bootstrap_policy_profile import BootstrapPolicyProfile
        from bootstrap_policy_profile import BootstrapPolicyProfileContractError as PolContractError
        from bootstrap_policy_profile import bootstrap_policy_profile_binding as pol_binding_public
        from bootstrap_policy_profile import encode_bootstrap_policy_profile as pol_encode_public
        from bootstrap_prepublication import BootstrapPrepublicationEnvelope
        from bootstrap_prepublication import BootstrapPrepublicationContractError as PubContractError
        from bootstrap_prepublication import encode_bootstrap_prepublication_envelope as pub_encode_public
        from bootstrap_prepublication import prepublication_envelope_binding as pub_binding_public
        from bootstrap_recipe import BootstrapRecipe
        from bootstrap_recipe import BootstrapRecipeContractError as RecContractError
        from bootstrap_recipe import encode_bootstrap_recipe as rec_encode_public
        from bootstrap_resource_profile import BootstrapResourceProfile
        from bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
        from bootstrap_resource_profile import bootstrap_resource_profile_binding as res_binding_public
        from bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
    else:
        raise ImportError("bootstrap_plan: unsupported package context")
else:
    raise ImportError("bootstrap_plan: unsupported package context")

__all__ = [
    "BootstrapPlanContractError",
    "BootstrapPlan",
    "encode_bootstrap_plan",
    "decode_bootstrap_plan",
    "bootstrap_plan_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_plan/v1"
SCHEMA_VERSION = "1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "plan_ref",
    "plan_version",
    "installation_ref",
    "target_ref",
    "prepublication_binding",
    "policy_binding",
    "resource_profile_binding",
    "nv_profile",
    "tpm_context_binding",
    "recipe",
    "authority_binding",
    "procedure_binding",
    "executor_binding",
)

_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "plan_ref",
    "plan_version",
    "installation_ref",
    "target_ref",
))

_BINDING_FIELDS = frozenset((
    "prepublication_binding",
    "policy_binding",
    "resource_profile_binding",
    "tpm_context_binding",
    "authority_binding",
    "procedure_binding",
    "executor_binding",
))

_MSG = "bootstrap_plan: invalid value"


class BootstrapPlanContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapPlanContractError(_MSG) from None


def _is_forbidden_codepoint(code: int) -> bool:
    if code < 0x20:
        return True
    if code == 0x7F:
        return True
    if 0xD800 <= code <= 0xDFFF:
        return True
    return False


def _check_strict_nonempty_text(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if value == "":
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPlanContractError(_MSG) from None
    for ch in value:
        if _is_forbidden_codepoint(ord(ch)):
            _fail()


def _check_no_wildcard(value: str) -> None:
    if "*" in value:
        _fail()


def _check_limits(limits: Any) -> None:
    if type(limits) is not PayloadLimits:
        _fail()
    if type(limits.max_json_bytes) is not int:
        _fail()
    if type(limits.max_ref_bytes) is not int:
        _fail()
    if type(limits.max_observation_refs) is not int:
        _fail()
    if isinstance(limits.max_json_bytes, bool):
        _fail()
    if isinstance(limits.max_ref_bytes, bool):
        _fail()
    if isinstance(limits.max_observation_refs, bool):
        _fail()
    if limits.max_json_bytes <= 0:
        _fail()
    if limits.max_ref_bytes <= 0:
        _fail()
    if limits.max_observation_refs <= 0:
        _fail()


def _check_bounded_ref(value: str, ceiling: int) -> None:
    _check_strict_nonempty_text(value)
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapPlanContractError(_MSG) from None
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


def _check_binding_intrinsic(binding: Any) -> None:
    if type(binding) is not ContentBinding:
        _fail()
    try:
        ContentBinding(ref=binding.ref, version=binding.version, sha256=binding.sha256)
    except PgContractError:
        _fail()
    except (TypeError, ValueError):
        _fail()


def _check_binding_shape(binding: Any, limits: PayloadLimits) -> None:
    _check_binding_intrinsic(binding)
    _check_bounded_ref(binding.ref, limits.max_ref_bytes)
    _check_bounded_ref(binding.version, limits.max_ref_bytes)


def _check_producers_valid(
    limits: PayloadLimits,
    env: Any,
    policy: Any,
    resource: Any,
    context: Any,
    base: Any,
) -> None:
    if type(env) is not BootstrapPrepublicationEnvelope:
        _fail()
    if type(policy) is not BootstrapPolicyProfile:
        _fail()
    if type(resource) is not BootstrapResourceProfile:
        _fail()
    if type(context) is not BootstrapTpmContext:
        _fail()
    if type(base) is not BootstrapBase:
        _fail()
    try:
        pub_encode_public(env, limits, resource)
    except PubContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        pol_encode_public(policy, limits, resource)
    except PolContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        res_encode_public(resource, limits)
    except ResContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        ctx_encode_public(context, limits)
    except CtxContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        base_encode_public(base, limits)
    except BaseContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        nv_encode_public(policy.nv_profile, limits)
    except NvContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


def _check_nv_equal(a: Any, b: Any) -> None:
    if type(a) is not BootstrapNvProfile or type(b) is not BootstrapNvProfile:
        _fail()
    if a != b:
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPlan:
    object_type: str
    schema_version: str
    plan_ref: str
    plan_version: str
    installation_ref: str
    target_ref: str
    prepublication_binding: ContentBinding
    policy_binding: ContentBinding
    resource_profile_binding: ContentBinding
    nv_profile: BootstrapNvProfile
    tpm_context_binding: ContentBinding
    recipe: BootstrapRecipe
    authority_binding: ContentBinding
    procedure_binding: ContentBinding
    executor_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_nonempty_text(self.plan_ref)
        _check_strict_nonempty_text(self.plan_version)
        _check_strict_nonempty_text(self.installation_ref)
        _check_strict_nonempty_text(self.target_ref)
        _check_no_wildcard(self.installation_ref)
        _check_no_wildcard(self.target_ref)
        for b in (
            self.prepublication_binding,
            self.policy_binding,
            self.resource_profile_binding,
            self.tpm_context_binding,
            self.authority_binding,
            self.procedure_binding,
            self.executor_binding,
        ):
            _check_binding_intrinsic(b)
        if type(self.nv_profile) is not BootstrapNvProfile:
            _fail()
        if type(self.recipe) is not BootstrapRecipe:
            _fail()


def _check_bounded_form(
    value: BootstrapPlan,
    limits: PayloadLimits,
    env: BootstrapPrepublicationEnvelope,
    policy: BootstrapPolicyProfile,
    resource: BootstrapResourceProfile,
    context: BootstrapTpmContext,
    base: BootstrapBase,
) -> None:
    if type(value) is not BootstrapPlan:
        _fail()
    if type(value.object_type) is not str or value.object_type != OBJECT_TYPE:
        _fail()
    if type(value.schema_version) is not str or value.schema_version != SCHEMA_VERSION:
        _fail()
    for name in ("plan_ref", "plan_version", "installation_ref", "target_ref"):
        _check_bounded_ref(getattr(value, name), limits.max_ref_bytes)
    _check_no_wildcard(value.installation_ref)
    _check_no_wildcard(value.target_ref)
    for b in (
        value.prepublication_binding,
        value.policy_binding,
        value.resource_profile_binding,
        value.tpm_context_binding,
        value.authority_binding,
        value.procedure_binding,
        value.executor_binding,
    ):
        _check_binding_shape(b, limits)
    _check_producers_valid(limits, env, policy, resource, context, base)
    try:
        nv_encode_public(value.nv_profile, limits)
    except NvContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        rec_encode_public(value.recipe, limits, base, resource)
    except RecContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    if value.installation_ref != env.document.installation_ref:
        _fail()
    if value.target_ref != env.document.target_ref:
        _fail()
    if value.installation_ref != policy.installation_ref:
        _fail()
    if value.target_ref != policy.target_ref:
        _fail()
    if value.installation_ref != resource.installation_ref:
        _fail()
    if value.target_ref != resource.target_ref:
        _fail()
    if value.installation_ref != context.installation_ref:
        _fail()
    if value.target_ref != context.target_ref:
        _fail()
    if env.document.policy_ref != policy.policy_ref:
        _fail()
    if env.document.policy_version != policy.policy_version:
        _fail()
    _check_nv_equal(value.nv_profile, env.document.nv_profile)
    _check_nv_equal(value.nv_profile, policy.nv_profile)
    if base.nv_coordinates.nv_index != value.nv_profile.nv_index:
        _fail()
    if base.nv_coordinates.nv_name_hex != value.nv_profile.nv_name_hex:
        _fail()
    try:
        expected_ctx = ctx_binding_public(context, limits)
        expected_pub = pub_binding_public(env, limits, resource)
        expected_pol = pol_binding_public(policy, limits, resource)
        expected_res = res_binding_public(resource, limits)
    except (CtxContractError, PubContractError, PolContractError, ResContractError):
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    if value.tpm_context_binding != expected_ctx:
        _fail()
    if policy.tpm_context_binding != expected_ctx:
        _fail()
    if base.tpm_context_binding != expected_ctx:
        _fail()
    if value.prepublication_binding != expected_pub:
        _fail()
    if value.policy_binding != expected_pol:
        _fail()
    if value.resource_profile_binding != expected_res:
        _fail()
    if policy.resource_profile_binding != expected_res:
        _fail()


def _binding_payload(binding: ContentBinding) -> dict[str, str]:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def _nv_payload(nv: BootstrapNvProfile) -> dict[str, Any]:
    return {
        "nv_index": nv.nv_index,
        "nv_attributes": nv.nv_attributes,
        "nv_name_alg": nv.nv_name_alg,
        "nv_data_size": nv.nv_data_size,
        "nv_authpolicy_hex": nv.nv_authpolicy_hex,
        "nv_name_hex": nv.nv_name_hex,
        "maintenance_p256_ref": nv.maintenance_p256_ref,
    }


def _recipe_payload(recipe: BootstrapRecipe) -> dict[str, Any]:
    return {
        "object_type": recipe.object_type,
        "schema_version": recipe.schema_version,
        "recipe_ref": recipe.recipe_ref,
        "recipe_version": recipe.recipe_version,
        "renderer_id": recipe.renderer_id,
        "transition_ref": recipe.transition_ref,
        "registry_ref": recipe.registry_ref,
        "registry_generation_ref": recipe.registry_generation_ref,
        "epoch": recipe.epoch,
        "sequence": recipe.sequence,
        "correlation_refs": list(recipe.correlation_refs),
        "causation_refs": list(recipe.causation_refs),
        "initial_base_binding": _binding_payload(recipe.initial_base_binding),
    }


def _payload(value: BootstrapPlan) -> dict[str, Any]:
    return {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "plan_ref": value.plan_ref,
        "plan_version": value.plan_version,
        "installation_ref": value.installation_ref,
        "target_ref": value.target_ref,
        "prepublication_binding": _binding_payload(value.prepublication_binding),
        "policy_binding": _binding_payload(value.policy_binding),
        "resource_profile_binding": _binding_payload(value.resource_profile_binding),
        "nv_profile": _nv_payload(value.nv_profile),
        "tpm_context_binding": _binding_payload(value.tpm_context_binding),
        "recipe": _recipe_payload(value.recipe),
        "authority_binding": _binding_payload(value.authority_binding),
        "procedure_binding": _binding_payload(value.procedure_binding),
        "executor_binding": _binding_payload(value.executor_binding),
    }


def _canon(payload: dict[str, Any], limits: PayloadLimits) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except BootstrapPlanContractError:
        raise
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPlanContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def encode_bootstrap_plan(
    value: BootstrapPlan,
    limits: PayloadLimits,
    prepublication_envelope: BootstrapPrepublicationEnvelope,
    policy: BootstrapPolicyProfile,
    resource: BootstrapResourceProfile,
    context: BootstrapTpmContext,
    base: BootstrapBase,
) -> str:
    _check_limits(limits)
    _check_bounded_form(value, limits, prepublication_envelope, policy, resource, context, base)
    return _canon(_payload(value), limits)


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
    raise BootstrapPlanContractError(_MSG) from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapPlanContractError(_MSG) from None


def _pairs_generic(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    for key, _ in pairs:
        if type(key) is not str:
            _fail()
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        _fail()
    return {key: item for key, item in pairs}


def _decode_json(text: Any, limits: PayloadLimits) -> dict[str, Any]:
    _check_limits(limits)
    if type(text) is not str:
        _fail()
    if text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPlanContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    try:
        data = json.loads(
            text,
            object_pairs_hook=_pairs_generic,
            parse_int=_parse_int,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except BootstrapPlanContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    return data


def _nested_binding(data: Any) -> ContentBinding:
    if type(data) is not dict or set(data) != {"ref", "version", "sha256"}:
        _fail()
    if type(data["ref"]) is not str:
        _fail()
    if type(data["version"]) is not str:
        _fail()
    if type(data["sha256"]) is not str:
        _fail()
    try:
        return ContentBinding(ref=data["ref"], version=data["version"], sha256=data["sha256"])
    except PgContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()


def _build_plan(
    data: dict[str, Any],
    limits: PayloadLimits,
    env: BootstrapPrepublicationEnvelope,
    policy: BootstrapPolicyProfile,
    resource: BootstrapResourceProfile,
    context: BootstrapTpmContext,
    base: BootstrapBase,
) -> BootstrapPlan:
    if type(data) is not dict or set(data) != set(FIELD_NAMES):
        _fail()
    for key in _STR_FIELDS:
        if type(data[key]) is not str:
            _fail()
    for key in _BINDING_FIELDS:
        if type(data[key]) is not dict:
            _fail()
    if type(data["nv_profile"]) is not dict:
        _fail()
    if type(data["recipe"]) is not dict:
        _fail()
    bindings = {k: _nested_binding(data[k]) for k in _BINDING_FIELDS}
    nv_data = data["nv_profile"]
    if set(nv_data) != {"nv_index", "nv_attributes", "nv_name_alg", "nv_data_size", "nv_authpolicy_hex", "nv_name_hex", "maintenance_p256_ref"}:
        _fail()
    if type(nv_data["nv_index"]) is not int or isinstance(nv_data["nv_index"], bool):
        _fail()
    if type(nv_data["nv_attributes"]) is not int or isinstance(nv_data["nv_attributes"], bool):
        _fail()
    for k in ("nv_name_alg", "nv_authpolicy_hex", "nv_name_hex", "maintenance_p256_ref"):
        if type(nv_data[k]) is not str:
            _fail()
    if type(nv_data["nv_data_size"]) is not int or isinstance(nv_data["nv_data_size"], bool):
        _fail()
    try:
        nv = BootstrapNvProfile(
            nv_index=nv_data["nv_index"],
            nv_attributes=nv_data["nv_attributes"],
            nv_name_alg=nv_data["nv_name_alg"],
            nv_data_size=nv_data["nv_data_size"],
            nv_authpolicy_hex=nv_data["nv_authpolicy_hex"],
            nv_name_hex=nv_data["nv_name_hex"],
            maintenance_p256_ref=nv_data["maintenance_p256_ref"],
        )
    except NvContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    rec_data = data["recipe"]
    if set(rec_data) != {"object_type", "schema_version", "recipe_ref", "recipe_version", "renderer_id", "transition_ref", "registry_ref", "registry_generation_ref", "epoch", "sequence", "correlation_refs", "causation_refs", "initial_base_binding"}:
        _fail()
    for k in ("object_type", "schema_version", "recipe_ref", "recipe_version", "renderer_id", "transition_ref", "registry_ref", "registry_generation_ref"):
        if type(rec_data[k]) is not str:
            _fail()
    for k in ("epoch", "sequence"):
        if type(rec_data[k]) is not int or isinstance(rec_data[k], bool):
            _fail()
    for k in ("correlation_refs", "causation_refs"):
        if type(rec_data[k]) is not list:
            _fail()
        for item in rec_data[k]:
            if type(item) is not str:
                _fail()
    rec_binding = _nested_binding(rec_data["initial_base_binding"])
    try:
        recipe = BootstrapRecipe(
            object_type=rec_data["object_type"],
            schema_version=rec_data["schema_version"],
            recipe_ref=rec_data["recipe_ref"],
            recipe_version=rec_data["recipe_version"],
            renderer_id=rec_data["renderer_id"],
            transition_ref=rec_data["transition_ref"],
            registry_ref=rec_data["registry_ref"],
            registry_generation_ref=rec_data["registry_generation_ref"],
            epoch=rec_data["epoch"],
            sequence=rec_data["sequence"],
            correlation_refs=tuple(rec_data["correlation_refs"]),
            causation_refs=tuple(rec_data["causation_refs"]),
            initial_base_binding=rec_binding,
        )
    except RecContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        value = BootstrapPlan(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            plan_ref=data["plan_ref"],
            plan_version=data["plan_version"],
            installation_ref=data["installation_ref"],
            target_ref=data["target_ref"],
            prepublication_binding=bindings["prepublication_binding"],
            policy_binding=bindings["policy_binding"],
            resource_profile_binding=bindings["resource_profile_binding"],
            nv_profile=nv,
            tpm_context_binding=bindings["tpm_context_binding"],
            recipe=recipe,
            authority_binding=bindings["authority_binding"],
            procedure_binding=bindings["procedure_binding"],
            executor_binding=bindings["executor_binding"],
        )
    except BootstrapPlanContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits, env, policy, resource, context, base)
    return value


def decode_bootstrap_plan(
    text: Any,
    limits: PayloadLimits,
    prepublication_envelope: BootstrapPrepublicationEnvelope,
    policy: BootstrapPolicyProfile,
    resource: BootstrapResourceProfile,
    context: BootstrapTpmContext,
    base: BootstrapBase,
) -> BootstrapPlan:
    _check_limits(limits)
    _check_producers_valid(limits, prepublication_envelope, policy, resource, context, base)
    return _build_plan(_decode_json(text, limits), limits, prepublication_envelope, policy, resource, context, base)


def bootstrap_plan_binding(
    value: BootstrapPlan,
    limits: PayloadLimits,
    prepublication_envelope: BootstrapPrepublicationEnvelope,
    policy: BootstrapPolicyProfile,
    resource: BootstrapResourceProfile,
    context: BootstrapTpmContext,
    base: BootstrapBase,
) -> ContentBinding:
    _check_limits(limits)
    canon = encode_bootstrap_plan(value, limits, prepublication_envelope, policy, resource, context, base)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    _check_bounded_ref(value.plan_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.plan_version, limits.max_ref_bytes)
    try:
        return ContentBinding(ref=value.plan_ref, version=value.plan_version, sha256=digest)
    except PgContractError:
        _fail()
    except (TypeError, ValueError):
        _fail()
