"""Recette BootstrapRecipe/v1 (13 champs).

FORME pure proposee, code NON QUALIFIE : sans admission, acte,
preuve materielle, TPM, PG, PZT, renderer execute, crypto, horloge
ni qualification. 13 valeurs strictes, canon trie compact, liaison
de forme vers BootstrapBase/v1 existante et pinning des 4 champs
de contexte epingles par Resource24 reelle explicite. PayloadLimits
externe borne le chargement ; Resource24 reelle borne epoch,
sequence, correlation, causation et epingle registry/epoch/sequence.
Ces egalites sont de la coherence de forme contre le profil fourni,
jamais une preuve d'origine protegee du profil. Sans clock,
deadline JSON, port, NV, SQL.
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
    from .bootstrap_resource_profile import BootstrapResourceProfile
    from .bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
    from .bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_base" in sys.builtin_module_names
            and "bootstrap_resource_profile" in sys.builtin_module_names):
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from bootstrap_base import BootstrapBase
        from bootstrap_base import BootstrapBaseContractError as BaseContractError
        from bootstrap_base import bootstrap_base_binding as base_binding_public
        from bootstrap_base import encode_bootstrap_base as base_encode_public
        from bootstrap_resource_profile import BootstrapResourceProfile
        from bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
        from bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_public
    else:
        raise ImportError("bootstrap_recipe: unsupported package context")
else:
    raise ImportError("bootstrap_recipe: unsupported package context")

__all__ = [
    "BootstrapRecipeContractError",
    "BootstrapRecipe",
    "encode_bootstrap_recipe",
    "decode_bootstrap_recipe",
    "bootstrap_recipe_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_recipe/v1"
SCHEMA_VERSION = "1.0.0"
RENDERER_ID = "pixs.bootstrap.fixed_renderer/v1"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "recipe_ref",
    "recipe_version",
    "renderer_id",
    "transition_ref",
    "registry_ref",
    "registry_generation_ref",
    "epoch",
    "sequence",
    "correlation_refs",
    "causation_refs",
    "initial_base_binding",
)

_STR_FIELDS = frozenset((
    "object_type",
    "schema_version",
    "recipe_ref",
    "recipe_version",
    "renderer_id",
    "transition_ref",
    "registry_ref",
    "registry_generation_ref",
))

_INT_FIELDS = frozenset((
    "epoch",
    "sequence",
))

_TRACE_FIELDS = frozenset((
    "correlation_refs",
    "causation_refs",
))

_UINT64_MAX = 18446744073709551615

_MSG = "bootstrap_recipe: invalid value"


class BootstrapRecipeContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapRecipeContractError(_MSG) from None


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
        raise BootstrapRecipeContractError(_MSG) from None
    for ch in value:
        if _is_forbidden_codepoint(ord(ch)):
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
        raise BootstrapRecipeContractError(_MSG) from None
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


def _check_uint64(value: Any) -> None:
    if type(value) is not int:
        _fail()
    if isinstance(value, bool):
        _fail()
    if value < 0 or value > _UINT64_MAX:
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


def _check_traces_intrinsic(value: Any) -> None:
    if type(value) is not tuple:
        _fail()
    for item in value:
        _check_strict_nonempty_text(item)


def _check_traces_bounded(items: tuple[str, ...], ceiling: int, count_max: int) -> None:
    if type(items) is not tuple:
        _fail()
    if type(count_max) is not int or isinstance(count_max, bool):
        _fail()
    if len(items) > count_max:
        _fail()
    for item in items:
        _check_bounded_ref(item, ceiling)


def _check_base_valid(base: Any, limits: PayloadLimits) -> None:
    if type(base) is not BootstrapBase:
        _fail()
    try:
        base_encode_public(base, limits)
    except BaseContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


def _check_resource_valid(resource: Any, limits: PayloadLimits) -> None:
    if type(resource) is not BootstrapResourceProfile:
        _fail()
    try:
        res_encode_public(resource, limits)
    except ResContractError:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapRecipe:
    object_type: str
    schema_version: str
    recipe_ref: str
    recipe_version: str
    renderer_id: str
    transition_ref: str
    registry_ref: str
    registry_generation_ref: str
    epoch: int
    sequence: int
    correlation_refs: tuple[str, ...]
    causation_refs: tuple[str, ...]
    initial_base_binding: ContentBinding

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_nonempty_text(self.recipe_ref)
        _check_strict_nonempty_text(self.recipe_version)
        if type(self.renderer_id) is not str or self.renderer_id != RENDERER_ID:
            _fail()
        _check_strict_nonempty_text(self.transition_ref)
        _check_strict_nonempty_text(self.registry_ref)
        _check_strict_nonempty_text(self.registry_generation_ref)
        _check_uint64(self.epoch)
        _check_uint64(self.sequence)
        _check_traces_intrinsic(self.correlation_refs)
        _check_traces_intrinsic(self.causation_refs)
        _check_binding_intrinsic(self.initial_base_binding)


def _check_bounded_form(
    value: BootstrapRecipe,
    limits: PayloadLimits,
    base: BootstrapBase,
    resource: BootstrapResourceProfile,
) -> None:
    _check_limits(limits)
    _check_base_valid(base, limits)
    _check_resource_valid(resource, limits)
    if type(value) is not BootstrapRecipe:
        _fail()
    value.__post_init__()
    _check_bounded_ref(value.recipe_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.recipe_version, limits.max_ref_bytes)
    _check_bounded_ref(value.transition_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.registry_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.registry_generation_ref, limits.max_ref_bytes)
    _check_uint64(value.epoch)
    _check_uint64(value.sequence)
    if value.epoch > resource.max_epoch:
        _fail()
    if value.sequence > resource.max_sequence:
        _fail()
    if type(resource.max_correlation_refs) is not int or isinstance(resource.max_correlation_refs, bool):
        _fail()
    if type(resource.max_causation_refs) is not int or isinstance(resource.max_causation_refs, bool):
        _fail()
    _check_traces_bounded(value.correlation_refs, limits.max_ref_bytes, resource.max_correlation_refs)
    _check_traces_bounded(value.causation_refs, limits.max_ref_bytes, resource.max_causation_refs)
    if value.registry_ref != resource.registry_ref:
        _fail()
    if value.registry_generation_ref != resource.registry_generation_ref:
        _fail()
    if type(resource.epoch) is not int or isinstance(resource.epoch, bool):
        _fail()
    if type(resource.first_sequence) is not int or isinstance(resource.first_sequence, bool):
        _fail()
    if value.epoch != resource.epoch:
        _fail()
    if value.sequence != resource.first_sequence:
        _fail()
    _check_binding_shape(value.initial_base_binding, limits)
    try:
        expected = base_binding_public(base, limits)
    except BaseContractError:
        _fail()
    except (TypeError, ValueError):
        _fail()
    if type(expected) is not ContentBinding:
        _fail()
    if value.initial_base_binding != expected:
        _fail()


def _payload(value: BootstrapRecipe) -> dict[str, Any]:
    return {
        "object_type": value.object_type,
        "schema_version": value.schema_version,
        "recipe_ref": value.recipe_ref,
        "recipe_version": value.recipe_version,
        "renderer_id": value.renderer_id,
        "transition_ref": value.transition_ref,
        "registry_ref": value.registry_ref,
        "registry_generation_ref": value.registry_generation_ref,
        "epoch": value.epoch,
        "sequence": value.sequence,
        "correlation_refs": list(value.correlation_refs),
        "causation_refs": list(value.causation_refs),
        "initial_base_binding": {
            "ref": value.initial_base_binding.ref,
            "version": value.initial_base_binding.version,
            "sha256": value.initial_base_binding.sha256,
        },
    }


def _canon(payload: dict[str, Any], limits: PayloadLimits) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapRecipeContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > limits.max_json_bytes:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def encode_bootstrap_recipe(
    value: BootstrapRecipe,
    limits: PayloadLimits,
    base: BootstrapBase,
    resource: BootstrapResourceProfile,
) -> str:
    _check_bounded_form(value, limits, base, resource)
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
    raise BootstrapRecipeContractError(_MSG) from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapRecipeContractError(_MSG) from None


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
        raise BootstrapRecipeContractError(_MSG) from None
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
    except BootstrapRecipeContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict:
        _fail()
    return data


def _build_recipe(
    data: dict[str, Any],
    limits: PayloadLimits,
    base: BootstrapBase,
    resource: BootstrapResourceProfile,
) -> BootstrapRecipe:
    if type(data) is not dict or set(data) != set(FIELD_NAMES):
        _fail()
    for key in _STR_FIELDS:
        if type(data[key]) is not str:
            _fail()
    for key in _INT_FIELDS:
        if type(data[key]) is not int or isinstance(data[key], bool):
            _fail()
    for key in _TRACE_FIELDS:
        items = data[key]
        if type(items) is not list:
            _fail()
        for item in items:
            if type(item) is not str:
                _fail()
    binding_data = data["initial_base_binding"]
    if type(binding_data) is not dict or set(binding_data) != {"ref", "version", "sha256"}:
        _fail()
    if type(binding_data["ref"]) is not str:
        _fail()
    if type(binding_data["version"]) is not str:
        _fail()
    if type(binding_data["sha256"]) is not str:
        _fail()
    try:
        binding = ContentBinding(ref=binding_data["ref"], version=binding_data["version"], sha256=binding_data["sha256"])
    except PgContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()
    try:
        value = BootstrapRecipe(
            object_type=data["object_type"],
            schema_version=data["schema_version"],
            recipe_ref=data["recipe_ref"],
            recipe_version=data["recipe_version"],
            renderer_id=data["renderer_id"],
            transition_ref=data["transition_ref"],
            registry_ref=data["registry_ref"],
            registry_generation_ref=data["registry_generation_ref"],
            epoch=data["epoch"],
            sequence=data["sequence"],
            correlation_refs=tuple(data["correlation_refs"]),
            causation_refs=tuple(data["causation_refs"]),
            initial_base_binding=binding,
        )
    except BootstrapRecipeContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_bounded_form(value, limits, base, resource)
    return value


def decode_bootstrap_recipe(
    text: Any,
    limits: PayloadLimits,
    base: BootstrapBase,
    resource: BootstrapResourceProfile,
) -> BootstrapRecipe:
    _check_limits(limits)
    _check_base_valid(base, limits)
    _check_resource_valid(resource, limits)
    return _build_recipe(_decode_json(text, limits), limits, base, resource)


def bootstrap_recipe_binding(
    value: BootstrapRecipe,
    limits: PayloadLimits,
    base: BootstrapBase,
    resource: BootstrapResourceProfile,
) -> ContentBinding:
    _check_limits(limits)
    canon = encode_bootstrap_recipe(value, limits, base, resource)
    digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    _check_bounded_ref(value.recipe_ref, limits.max_ref_bytes)
    _check_bounded_ref(value.recipe_version, limits.max_ref_bytes)
    try:
        return ContentBinding(ref=value.recipe_ref, version=value.recipe_version, sha256=digest)
    except PgContractError:
        _fail()
