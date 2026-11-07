"""Provenance initiale observee (forme et liaisons, 28 champs).

Forme pure proposee, sans collecteur, observation, HMAC, admission,
acte, preuve materielle, signature, TPM, PG, PZT, cle privee,
verification crypto ni qualification. Les bindings sont des donnees
simples recalculees via API publiques, jamais des resolutions ni des
permissions. La projection deterministe Name des SIX donnees publiques
(calque contracts.md lecture NV, realise prive nv_anchor.pyx, sans
importer l'ABI privee) est autorisee dans le codec, sans pretendre a
une preuve TPM ni qualifier 1.38. Les attendus avant/apres sont des
donnees explicites distinctes fournies, pas une inference d'autorite.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .bootstrap_base import BootstrapBase
    from .bootstrap_base import BootstrapBaseContractError as BaseContractError
    from .bootstrap_base import bootstrap_base_binding as base_binding_real
    from .bootstrap_base import encode_bootstrap_base as base_encode_real
    from .bootstrap_context import BootstrapTpmContext
    from .bootstrap_context import BootstrapContextContractError as CtxContractError
    from .bootstrap_context import bootstrap_context_binding as ctx_binding_real
    from .bootstrap_context import encode_bootstrap_context as ctx_encode_real
    from .bootstrap_init_profile import BootstrapInitProfile
    from .bootstrap_init_profile import BootstrapInitProfileContractError as InitContractError
    from .bootstrap_init_profile import bootstrap_expected_base_hex64 as init_expected_base_real
    from .bootstrap_init_profile import bootstrap_init_profile_binding as init_binding_real
    from .bootstrap_init_profile import encode_bootstrap_init_profile as init_encode_real
    from .bootstrap_initial_record import BootstrapInitialRecord
    from .bootstrap_initial_record import BootstrapInitialRecordContractError as R0ContractError
    from .bootstrap_initial_record import bootstrap_initial_expected_nv_hex as r0_expected_nv_real
    from .bootstrap_initial_record import bootstrap_initial_physical_receipt_expected as r0_receipt_real
    from .bootstrap_initial_record import bootstrap_initial_record_binding as r0_binding_real
    from .bootstrap_initial_record import bootstrap_initial_semantic_head_hex as r0_head_real
    from .bootstrap_initial_record import encode_bootstrap_initial_record as r0_encode_real
    from .bootstrap_nv_profile import BootstrapNvProfile
    from .bootstrap_plan import BootstrapPlan
    from .bootstrap_plan import BootstrapPlanContractError as PlanContractError
    from .bootstrap_plan import bootstrap_plan_binding as plan_binding_real
    from .bootstrap_plan import encode_bootstrap_plan as plan_encode_real
    from .bootstrap_policy_profile import BootstrapPolicyProfile
    from .bootstrap_policy_profile import BootstrapPolicyProfileContractError as PolContractError
    from .bootstrap_policy_profile import bootstrap_policy_profile_binding as pol_binding_real
    from .bootstrap_policy_profile import encode_bootstrap_policy_profile as pol_encode_real
    from .bootstrap_prepublication import BootstrapPrepublicationEnvelope
    from .bootstrap_prepublication import BootstrapPrepublicationContractError as PubContractError
    from .bootstrap_prepublication import encode_bootstrap_prepublication_envelope as pub_encode_real
    from .bootstrap_prepublication import prepublication_envelope_binding as pub_binding_real
    from .bootstrap_recipe import bootstrap_recipe_binding as recipe_binding_real
    from .bootstrap_resource_profile import BootstrapResourceProfile
    from .bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
    from .bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_real
    from .postgresql_contracts import ContentBinding, PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_base" in sys.builtin_module_names
            and "bootstrap_context" in sys.builtin_module_names
            and "bootstrap_init_profile" in sys.builtin_module_names
            and "bootstrap_initial_record" in sys.builtin_module_names
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
        from bootstrap_base import encode_bootstrap_base as base_encode_real
        from bootstrap_context import BootstrapTpmContext
        from bootstrap_context import BootstrapContextContractError as CtxContractError
        from bootstrap_context import bootstrap_context_binding as ctx_binding_real
        from bootstrap_context import encode_bootstrap_context as ctx_encode_real
        from bootstrap_init_profile import BootstrapInitProfile
        from bootstrap_init_profile import BootstrapInitProfileContractError as InitContractError
        from bootstrap_init_profile import bootstrap_expected_base_hex64 as init_expected_base_real
        from bootstrap_init_profile import bootstrap_init_profile_binding as init_binding_real
        from bootstrap_init_profile import encode_bootstrap_init_profile as init_encode_real
        from bootstrap_initial_record import BootstrapInitialRecord
        from bootstrap_initial_record import BootstrapInitialRecordContractError as R0ContractError
        from bootstrap_initial_record import bootstrap_initial_expected_nv_hex as r0_expected_nv_real
        from bootstrap_initial_record import bootstrap_initial_physical_receipt_expected as r0_receipt_real
        from bootstrap_initial_record import bootstrap_initial_record_binding as r0_binding_real
        from bootstrap_initial_record import bootstrap_initial_semantic_head_hex as r0_head_real
        from bootstrap_initial_record import encode_bootstrap_initial_record as r0_encode_real
        from bootstrap_nv_profile import BootstrapNvProfile
        from bootstrap_plan import BootstrapPlan
        from bootstrap_plan import BootstrapPlanContractError as PlanContractError
        from bootstrap_plan import bootstrap_plan_binding as plan_binding_real
        from bootstrap_plan import encode_bootstrap_plan as plan_encode_real
        from bootstrap_policy_profile import BootstrapPolicyProfile
        from bootstrap_policy_profile import BootstrapPolicyProfileContractError as PolContractError
        from bootstrap_policy_profile import bootstrap_policy_profile_binding as pol_binding_real
        from bootstrap_policy_profile import encode_bootstrap_policy_profile as pol_encode_real
        from bootstrap_prepublication import BootstrapPrepublicationEnvelope
        from bootstrap_prepublication import BootstrapPrepublicationContractError as PubContractError
        from bootstrap_prepublication import encode_bootstrap_prepublication_envelope as pub_encode_real
        from bootstrap_prepublication import prepublication_envelope_binding as pub_binding_real
        from bootstrap_recipe import bootstrap_recipe_binding as recipe_binding_real
        from bootstrap_resource_profile import BootstrapResourceProfile
        from bootstrap_resource_profile import BootstrapResourceProfileContractError as ResContractError
        from bootstrap_resource_profile import encode_bootstrap_resource_profile as res_encode_real
    else:
        raise ImportError("bootstrap_provenance: unsupported package context")
else:
    raise ImportError("bootstrap_provenance: unsupported package context")

__all__ = [
    "BootstrapProvenanceContractError",
    "BootstrapProvenanceNvPublic",
    "BootstrapProvenance",
    "encode_bootstrap_provenance",
    "decode_bootstrap_provenance",
    "bootstrap_provenance_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_provenance_observed/v1"
SCHEMA_VERSION = "1.0.0"

FIELD_NAMES = (
    "object_type", "schema_version",
    "provenance_ref", "provenance_version",
    "installation_ref", "target_ref",
    "prepublication_binding", "policy_binding",
    "plan_binding", "recipe_binding",
    "initial_base_binding", "init_profile_binding",
    "tpm_context_binding", "r0_payload_binding",
    "r0_semantic_head_hex64", "r0_physical_receipt_hex64",
    "nv_base_observed_hex64", "nv_after_B_observed_hex64",
    "observed_from_utc6", "observed_to_utc6",
    "authority_binding", "procedure_binding", "executor_binding",
    "definition_attempt_ref", "initialization_attempt_ref", "bootstrap_extend_attempt_ref",
    "nv_public_before_initialization", "nv_public_after_initialization",
)

_STR_FIELDS = frozenset((
    "object_type", "schema_version",
    "provenance_ref", "provenance_version",
    "installation_ref", "target_ref",
    "r0_semantic_head_hex64", "r0_physical_receipt_hex64",
    "nv_base_observed_hex64", "nv_after_B_observed_hex64",
    "observed_from_utc6", "observed_to_utc6",
    "definition_attempt_ref", "initialization_attempt_ref", "bootstrap_extend_attempt_ref",
))

_BINDING_FIELDS = frozenset((
    "prepublication_binding", "policy_binding",
    "plan_binding", "recipe_binding",
    "initial_base_binding", "init_profile_binding",
    "tpm_context_binding", "r0_payload_binding",
    "authority_binding", "procedure_binding", "executor_binding",
))

_NV_PUBLIC_FIELDS = frozenset((
    "nv_public_before_initialization", "nv_public_after_initialization",
))

_BINDING_KEYS = frozenset(("ref", "version", "sha256"))

_NV_PUBLIC_KEYS = frozenset((
    "nv_index", "nv_attributes", "nv_name_alg",
    "nv_data_size", "nv_authpolicy_hex", "nv_name_hex",
))

_NV_INT_FIELDS = frozenset(("nv_index", "nv_attributes", "nv_data_size"))

NV_INDEX_MIN = 0x01000000
NV_INDEX_MAX = 0x01FFFFFF
NV_ATTRIBUTES_MAX = 0xFFFFFFFF
NV_ATTRS_REQUIRED = 0x60040404
NV_ATTRS_FORBIDDEN = 0x1C000800
NV_NT_MASK = 0xF0
NV_NT_EXTEND = 0x40
NV_WRITTEN = 0x20000000
NV_READLOCKED = 0x10000000
NV_WRITELOCKED = 0x00000800
NV_ATTRS_REQUIRED_BEFORE = 0x40040404
NV_NAME_ALG = "SHA256"
NV_DATA_SIZE = 32

_HEX_LOWER = frozenset("0123456789abcdef")

_MSG = "bootstrap_provenance: invalid value"

_PRODUCER_ERRORS = (BaseContractError, CtxContractError, InitContractError, R0ContractError, PlanContractError, PolContractError, PubContractError, ResContractError, PgContractError)


class BootstrapProvenanceContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapProvenanceContractError(_MSG) from None


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


def _is_forbidden(code: int) -> bool:
    if code < 0x20:
        return True
    if code == 0x7F:
        return True
    if 0xD800 <= code <= 0xDFFF:
        return True
    return False


def _check_strict_text(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if value == "":
        _fail()
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapProvenanceContractError(_MSG) from None
    for ch in value:
        if _is_forbidden(ord(ch)):
            _fail()


def _check_bounded_ref(value: str, ceiling: int) -> None:
    _check_strict_text(value)
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapProvenanceContractError(_MSG) from None
    if size < 1:
        _fail()
    if size > ceiling:
        _fail()


def _check_no_wildcard(value: str) -> None:
    if "*" in value:
        _fail()
    if "?" in value:
        _fail()


def _check_hex64(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 64:
        _fail()
    for ch in value:
        if ch not in _HEX_LOWER:
            _fail()


def _check_utc6_shape(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 27:
        _fail()
    if (value[4] != "-" or value[7] != "-" or value[10] != "T"
            or value[13] != ":" or value[16] != ":" or value[19] != "."
            or value[26] != "Z"):
        _fail()
    digits = value[0:4] + value[5:7] + value[8:10] + value[11:13] + value[14:16] + value[17:19] + value[20:26]
    for ch in digits:
        if ch < "0" or ch > "9":
            _fail()


def _parse_utc6(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except (TypeError, ValueError):
        _fail()


def _check_nv_index(value: Any) -> None:
    if type(value) is not int:
        _fail()
    if isinstance(value, bool):
        _fail()
    if value < NV_INDEX_MIN or value > NV_INDEX_MAX:
        _fail()


def _check_nv_attributes_strict(value: Any) -> None:
    if type(value) is not int:
        _fail()
    if isinstance(value, bool):
        _fail()
    if value < 0 or value > NV_ATTRIBUTES_MAX:
        _fail()

def _check_nv_attributes_before(value: Any) -> None:
    _check_nv_attributes_strict(value)
    if (value & NV_ATTRS_REQUIRED_BEFORE) != NV_ATTRS_REQUIRED_BEFORE:
        _fail()
    if (value & NV_ATTRS_FORBIDDEN) != 0:
        _fail()
    if (value & NV_NT_MASK) != NV_NT_EXTEND:
        _fail()
    if (value & (NV_WRITTEN | NV_READLOCKED | NV_WRITELOCKED)) != 0:
        _fail()

def _check_nv_attributes_after(value: Any) -> None:
    _check_nv_attributes_strict(value)
    if (value & NV_ATTRS_REQUIRED) != NV_ATTRS_REQUIRED:
        _fail()
    if (value & NV_ATTRS_FORBIDDEN) != 0:
        _fail()
    if (value & NV_NT_MASK) != NV_NT_EXTEND:
        _fail()


def _check_authpolicy_hex(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 64:
        _fail()
    for ch in value:
        if ch not in _HEX_LOWER:
            _fail()


def _check_name_hex(value: Any) -> None:
    if type(value) is not str:
        _fail()
    if len(value) != 68:
        _fail()
    if value[:4] != "000b":
        _fail()
    for ch in value[4:]:
        if ch not in _HEX_LOWER:
            _fail()


def _expected_name_hex(nv_index: int, nv_attributes: int, authpolicy_hex: str) -> str:
    try:
        policy_bytes = bytes.fromhex(authpolicy_hex)
    except ValueError:
        _fail()
    if len(policy_bytes) != 32:
        _fail()
    wire = struct.pack(">I", nv_index) + struct.pack(">H", 0x000B) + struct.pack(">I", nv_attributes) + struct.pack(">H", 32) + policy_bytes + struct.pack(">H", 32)
    if len(wire) != 46:
        _fail()
    return "000b" + hashlib.sha256(wire).hexdigest()


def _check_binding_intrinsic(binding: Any) -> None:
    if type(binding) is not ContentBinding:
        _fail()
    try:
        ContentBinding(ref=binding.ref, version=binding.version, sha256=binding.sha256)
    except PgContractError:
        _fail()
    except (TypeError, ValueError):
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapProvenanceNvPublic:
    nv_index: int
    nv_attributes: int
    nv_name_alg: str
    nv_data_size: int
    nv_authpolicy_hex: str
    nv_name_hex: str

    def __post_init__(self) -> None:
        _check_nv_index(self.nv_index)
        _check_nv_attributes_strict(self.nv_attributes)
        if type(self.nv_name_alg) is not str or self.nv_name_alg != NV_NAME_ALG:
            _fail()
        if type(self.nv_data_size) is not int or self.nv_data_size != NV_DATA_SIZE:
            _fail()
        if isinstance(self.nv_data_size, bool):
            _fail()
        _check_authpolicy_hex(self.nv_authpolicy_hex)
        _check_name_hex(self.nv_name_hex)
        if _expected_name_hex(self.nv_index, self.nv_attributes, self.nv_authpolicy_hex) != self.nv_name_hex:
            _fail()

def _check_nv_public_before(nv: Any) -> None:
    if type(nv) is not BootstrapProvenanceNvPublic:
        _fail()
    _check_nv_index(nv.nv_index)
    _check_nv_attributes_before(nv.nv_attributes)
    if type(nv.nv_name_alg) is not str or nv.nv_name_alg != NV_NAME_ALG:
        _fail()
    if type(nv.nv_data_size) is not int or nv.nv_data_size != NV_DATA_SIZE:
        _fail()
    if isinstance(nv.nv_data_size, bool):
        _fail()
    _check_authpolicy_hex(nv.nv_authpolicy_hex)
    _check_name_hex(nv.nv_name_hex)
    if _expected_name_hex(nv.nv_index, nv.nv_attributes, nv.nv_authpolicy_hex) != nv.nv_name_hex:
        _fail()

def _check_nv_public_after(nv: Any) -> None:
    if type(nv) is not BootstrapProvenanceNvPublic:
        _fail()
    _check_nv_index(nv.nv_index)
    _check_nv_attributes_after(nv.nv_attributes)
    if type(nv.nv_name_alg) is not str or nv.nv_name_alg != NV_NAME_ALG:
        _fail()
    if type(nv.nv_data_size) is not int or nv.nv_data_size != NV_DATA_SIZE:
        _fail()
    if isinstance(nv.nv_data_size, bool):
        _fail()
    _check_authpolicy_hex(nv.nv_authpolicy_hex)
    _check_name_hex(nv.nv_name_hex)
    if _expected_name_hex(nv.nv_index, nv.nv_attributes, nv.nv_authpolicy_hex) != nv.nv_name_hex:
        _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapProvenance:
    object_type: str
    schema_version: str
    provenance_ref: str
    provenance_version: str
    installation_ref: str
    target_ref: str
    prepublication_binding: ContentBinding
    policy_binding: ContentBinding
    plan_binding: ContentBinding
    recipe_binding: ContentBinding
    initial_base_binding: ContentBinding
    init_profile_binding: ContentBinding
    tpm_context_binding: ContentBinding
    r0_payload_binding: ContentBinding
    r0_semantic_head_hex64: str
    r0_physical_receipt_hex64: str
    nv_base_observed_hex64: str
    nv_after_B_observed_hex64: str
    observed_from_utc6: str
    observed_to_utc6: str
    authority_binding: ContentBinding
    procedure_binding: ContentBinding
    executor_binding: ContentBinding
    definition_attempt_ref: str
    initialization_attempt_ref: str
    bootstrap_extend_attempt_ref: str
    nv_public_before_initialization: BootstrapProvenanceNvPublic
    nv_public_after_initialization: BootstrapProvenanceNvPublic

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            raise BootstrapProvenanceContractError(_MSG) from None
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            raise BootstrapProvenanceContractError(_MSG) from None
        for name in ("provenance_ref", "provenance_version", "installation_ref", "target_ref", "definition_attempt_ref", "initialization_attempt_ref", "bootstrap_extend_attempt_ref"):
            _check_strict_text(getattr(self, name))
        _check_no_wildcard(self.installation_ref)
        _check_no_wildcard(self.target_ref)
        for name in _BINDING_FIELDS:
            _check_binding_intrinsic(getattr(self, name))
        for name in ("r0_semantic_head_hex64", "r0_physical_receipt_hex64", "nv_base_observed_hex64", "nv_after_B_observed_hex64"):
            _check_hex64(getattr(self, name))
        _check_utc6_shape(self.observed_from_utc6)
        _check_utc6_shape(self.observed_to_utc6)
        if _parse_utc6(self.observed_to_utc6) < _parse_utc6(self.observed_from_utc6):
            raise BootstrapProvenanceContractError(_MSG) from None
        attempts = (self.definition_attempt_ref, self.initialization_attempt_ref, self.bootstrap_extend_attempt_ref)
        if len(set(attempts)) != 3:
            raise BootstrapProvenanceContractError(_MSG) from None
        for name in _NV_PUBLIC_FIELDS:
            item = getattr(self, name)
            if type(item) is not BootstrapProvenanceNvPublic:
                raise BootstrapProvenanceContractError(_MSG) from None


def _provenance_json_bound(provenance_limits: PayloadLimits, resource: BootstrapResourceProfile) -> int:
    return min(provenance_limits.max_json_bytes, resource.payload_max_json_bytes)


def _provenance_ref_bound(provenance_limits: PayloadLimits, resource: BootstrapResourceProfile) -> int:
    return min(provenance_limits.max_ref_bytes, resource.payload_max_ref_bytes)


def _check_producers(provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase, initial_record: BootstrapInitialRecord, init_profile: BootstrapInitProfile) -> None:
    _check_limits(provenance_limits)
    _check_limits(producer_limits)
    if type(resource) is not BootstrapResourceProfile:
        _fail()
    if type(plan) is not BootstrapPlan:
        _fail()
    if type(prepublication_envelope) is not BootstrapPrepublicationEnvelope:
        _fail()
    if type(policy) is not BootstrapPolicyProfile:
        _fail()
    if type(context) is not BootstrapTpmContext:
        _fail()
    if type(base) is not BootstrapBase:
        _fail()
    if type(initial_record) is not BootstrapInitialRecord:
        _fail()
    if type(init_profile) is not BootstrapInitProfile:
        _fail()
    try:
        res_encode_real(resource, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        ctx_encode_real(context, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        init_encode_real(init_profile, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        base_encode_real(base, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        pub_encode_real(prepublication_envelope, producer_limits, resource)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        pol_encode_real(policy, producer_limits, resource)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        plan_encode_real(plan, producer_limits, prepublication_envelope, policy, resource, context, base)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        r0_encode_real(initial_record, r0_limits=producer_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()


def _check_intrinsic(value: Any) -> None:
    if type(value) is not BootstrapProvenance:
        _fail()
    value.__post_init__()


def _check_bounds(value: BootstrapProvenance, provenance_limits: PayloadLimits, resource: BootstrapResourceProfile) -> None:
    bound = _provenance_ref_bound(provenance_limits, resource)
    for name in ("provenance_ref", "provenance_version", "installation_ref", "target_ref", "definition_attempt_ref", "initialization_attempt_ref", "bootstrap_extend_attempt_ref"):
        item = getattr(value, name)
        try:
            size = len(item.encode("utf-8"))
        except UnicodeEncodeError:
            raise BootstrapProvenanceContractError(_MSG) from None
        if size < 1:
            _fail()
        if size > bound:
            _fail()
    for name in _BINDING_FIELDS:
        item = getattr(value, name)
        try:
            rsize = len(item.ref.encode("utf-8"))
            vsize = len(item.version.encode("utf-8"))
        except UnicodeEncodeError:
            raise BootstrapProvenanceContractError(_MSG) from None
        if rsize < 1 or rsize > bound:
            _fail()
        if vsize < 1 or vsize > bound:
            _fail()
        _check_hex64(item.sha256)


def _check_coherence(value: BootstrapProvenance, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase, initial_record: BootstrapInitialRecord, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> None:
    if type(expected_nv_public_before) is not BootstrapProvenanceNvPublic:
        _fail()
    if type(expected_nv_public_after) is not BootstrapProvenanceNvPublic:
        _fail()
    _check_nv_public_before(value.nv_public_before_initialization)
    _check_nv_public_after(value.nv_public_after_initialization)
    _check_nv_public_before(expected_nv_public_before)
    _check_nv_public_after(expected_nv_public_after)
    try:
        exp_pub = pub_binding_real(prepublication_envelope, producer_limits, resource)
        exp_pol = pol_binding_real(policy, producer_limits, resource)
        exp_ctx = ctx_binding_real(context, producer_limits)
        exp_base_bind = base_binding_real(base, producer_limits)
        exp_init_bind = init_binding_real(init_profile, producer_limits)
        exp_plan = plan_binding_real(plan, producer_limits, prepublication_envelope, policy, resource, context, base)
        exp_recipe = recipe_binding_real(plan.recipe, producer_limits, base, resource)
        exp_r0 = r0_binding_real(initial_record, r0_limits=producer_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base)
        exp_head = r0_head_real(initial_record, r0_limits=producer_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base)
        exp_receipt = r0_receipt_real(initial_record, r0_limits=producer_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base)
        exp_nv_after = r0_expected_nv_real(initial_record, r0_limits=producer_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base)
        exp_base = init_expected_base_real(init_profile, producer_limits)
    except _PRODUCER_ERRORS:
        _fail()
    except (TypeError, ValueError, RecursionError):
        _fail()
    if value.prepublication_binding != exp_pub:
        _fail()
    if value.policy_binding != exp_pol:
        _fail()
    if value.plan_binding != exp_plan:
        _fail()
    if value.recipe_binding != exp_recipe:
        _fail()
    if value.initial_base_binding != exp_base_bind:
        _fail()
    if value.init_profile_binding != exp_init_bind:
        _fail()
    if value.tpm_context_binding != exp_ctx:
        _fail()
    if value.r0_payload_binding != exp_r0:
        _fail()
    if value.r0_semantic_head_hex64 != exp_head:
        _fail()
    if value.r0_physical_receipt_hex64 != exp_receipt:
        _fail()
    if value.nv_after_B_observed_hex64 != exp_nv_after:
        _fail()
    if value.nv_base_observed_hex64 != exp_base:
        _fail()
    if base.expected_base_hex64 != exp_base:
        _fail()
    if base.init_profile_binding != exp_init_bind:
        _fail()
    if init_profile.tpm_context_binding != exp_ctx:
        _fail()
    if base.tpm_context_binding != exp_ctx:
        _fail()
    if base.nv_coordinates.nv_index != init_profile.nv_profile.nv_index:
        _fail()
    if base.nv_coordinates.nv_name_hex != init_profile.nv_profile.nv_name_hex:
        _fail()
    if value.authority_binding != plan.authority_binding:
        _fail()
    if value.authority_binding != init_profile.authority_binding:
        _fail()
    if value.procedure_binding != plan.procedure_binding:
        _fail()
    if value.procedure_binding != init_profile.procedure_binding:
        _fail()
    if value.executor_binding != plan.executor_binding:
        _fail()
    if value.executor_binding != init_profile.executor_binding:
        _fail()
    if value.installation_ref != resource.installation_ref:
        _fail()
    if value.target_ref != resource.target_ref:
        _fail()
    if value.installation_ref != plan.installation_ref:
        _fail()
    if value.target_ref != plan.target_ref:
        _fail()
    if value.installation_ref != prepublication_envelope.document.installation_ref:
        _fail()
    if value.target_ref != prepublication_envelope.document.target_ref:
        _fail()
    if value.installation_ref != policy.installation_ref:
        _fail()
    if value.target_ref != policy.target_ref:
        _fail()
    if value.installation_ref != context.installation_ref:
        _fail()
    if value.target_ref != context.target_ref:
        _fail()
    if value.installation_ref != initial_record.installation_ref:
        _fail()
    if value.target_ref != initial_record.target_ref:
        _fail()
    if value.installation_ref != init_profile.installation_ref:
        _fail()
    if value.target_ref != init_profile.target_ref:
        _fail()
    if value.nv_public_before_initialization != expected_nv_public_before:
        _fail()
    if value.nv_public_after_initialization != expected_nv_public_after:
        _fail()
    after = value.nv_public_after_initialization
    if after.nv_index != plan.nv_profile.nv_index:
        _fail()
    if after.nv_attributes != plan.nv_profile.nv_attributes:
        _fail()
    if after.nv_name_alg != plan.nv_profile.nv_name_alg:
        _fail()
    if after.nv_data_size != plan.nv_profile.nv_data_size:
        _fail()
    if after.nv_authpolicy_hex != plan.nv_profile.nv_authpolicy_hex:
        _fail()
    if after.nv_name_hex != plan.nv_profile.nv_name_hex:
        _fail()
    if after.nv_index != init_profile.nv_profile.nv_index:
        _fail()
    if after.nv_attributes != init_profile.nv_profile.nv_attributes:
        _fail()
    if after.nv_name_alg != init_profile.nv_profile.nv_name_alg:
        _fail()
    if after.nv_data_size != init_profile.nv_profile.nv_data_size:
        _fail()
    if after.nv_authpolicy_hex != init_profile.nv_profile.nv_authpolicy_hex:
        _fail()
    if after.nv_name_hex != init_profile.nv_profile.nv_name_hex:
        _fail()
    before = value.nv_public_before_initialization
    if before.nv_index != after.nv_index:
        _fail()
    if before.nv_index != plan.nv_profile.nv_index:
        _fail()
    if before.nv_index != init_profile.nv_profile.nv_index:
        _fail()
    if before.nv_name_alg != after.nv_name_alg:
        _fail()
    if before.nv_name_alg != plan.nv_profile.nv_name_alg:
        _fail()
    if before.nv_data_size != after.nv_data_size:
        _fail()
    if before.nv_data_size != plan.nv_profile.nv_data_size:
        _fail()
    if before.nv_authpolicy_hex != after.nv_authpolicy_hex:
        _fail()
    if before.nv_authpolicy_hex != plan.nv_profile.nv_authpolicy_hex:
        _fail()
    if (before.nv_attributes | NV_WRITTEN) != after.nv_attributes:
        _fail()
    if (before.nv_attributes & (NV_WRITTEN | NV_READLOCKED | NV_WRITELOCKED)) != 0:
        _fail()
    if (after.nv_attributes & (NV_READLOCKED | NV_WRITELOCKED)) != 0:
        _fail()
    if (before.nv_attributes ^ after.nv_attributes) != NV_WRITTEN:
        _fail()


def _binding_payload(binding: ContentBinding) -> dict:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def _nv_public_payload(nv: BootstrapProvenanceNvPublic) -> dict:
    return {"nv_index": nv.nv_index, "nv_attributes": nv.nv_attributes, "nv_name_alg": nv.nv_name_alg, "nv_data_size": nv.nv_data_size, "nv_authpolicy_hex": nv.nv_authpolicy_hex, "nv_name_hex": nv.nv_name_hex}


def _payload(value: BootstrapProvenance) -> dict:
    return {
        "object_type": value.object_type, "schema_version": value.schema_version,
        "provenance_ref": value.provenance_ref, "provenance_version": value.provenance_version,
        "installation_ref": value.installation_ref, "target_ref": value.target_ref,
        "prepublication_binding": _binding_payload(value.prepublication_binding),
        "policy_binding": _binding_payload(value.policy_binding),
        "plan_binding": _binding_payload(value.plan_binding),
        "recipe_binding": _binding_payload(value.recipe_binding),
        "initial_base_binding": _binding_payload(value.initial_base_binding),
        "init_profile_binding": _binding_payload(value.init_profile_binding),
        "tpm_context_binding": _binding_payload(value.tpm_context_binding),
        "r0_payload_binding": _binding_payload(value.r0_payload_binding),
        "r0_semantic_head_hex64": value.r0_semantic_head_hex64,
        "r0_physical_receipt_hex64": value.r0_physical_receipt_hex64,
        "nv_base_observed_hex64": value.nv_base_observed_hex64,
        "nv_after_B_observed_hex64": value.nv_after_B_observed_hex64,
        "observed_from_utc6": value.observed_from_utc6, "observed_to_utc6": value.observed_to_utc6,
        "authority_binding": _binding_payload(value.authority_binding),
        "procedure_binding": _binding_payload(value.procedure_binding),
        "executor_binding": _binding_payload(value.executor_binding),
        "definition_attempt_ref": value.definition_attempt_ref,
        "initialization_attempt_ref": value.initialization_attempt_ref,
        "bootstrap_extend_attempt_ref": value.bootstrap_extend_attempt_ref,
        "nv_public_before_initialization": _nv_public_payload(value.nv_public_before_initialization),
        "nv_public_after_initialization": _nv_public_payload(value.nv_public_after_initialization),
    }


def _canon(payload: dict, bound: int) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapProvenanceContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > bound:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def _validated_canon(value: BootstrapProvenance, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase, initial_record: BootstrapInitialRecord, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> bytes:
    _check_producers(provenance_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base, initial_record, init_profile)
    _check_intrinsic(value)
    _check_coherence(value, provenance_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base, initial_record, init_profile, expected_nv_public_before, expected_nv_public_after)
    _check_bounds(value, provenance_limits, resource)
    return _canon(_payload(value), _provenance_json_bound(provenance_limits, resource)).encode("utf-8")


def encode_bootstrap_provenance(value: BootstrapProvenance, *, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase, initial_record: BootstrapInitialRecord, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> str:
    return _validated_canon(value, provenance_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base, initial_record, init_profile, expected_nv_public_before, expected_nv_public_after).decode("utf-8")


def _parse_int(token: str) -> int:
    if token[:1] == "-":
        _fail()
    if len(token) > 10:
        _fail()
    try:
        return int(token, 10)
    except ValueError:
        _fail()


def _reject_float(token: str) -> NoReturn:
    raise BootstrapProvenanceContractError(_MSG) from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapProvenanceContractError(_MSG) from None


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
    if keyset == _NV_PUBLIC_KEYS:
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


def _nested_nv_public(data: Any) -> BootstrapProvenanceNvPublic:
    if type(data) is not dict or set(data) != _NV_PUBLIC_KEYS:
        _fail()
    try:
        return BootstrapProvenanceNvPublic(nv_index=data["nv_index"], nv_attributes=data["nv_attributes"], nv_name_alg=data["nv_name_alg"], nv_data_size=data["nv_data_size"], nv_authpolicy_hex=data["nv_authpolicy_hex"], nv_name_hex=data["nv_name_hex"])
    except BootstrapProvenanceContractError:
        raise
    except (TypeError, KeyError):
        _fail()


def decode_bootstrap_provenance(text: Any, *, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase, initial_record: BootstrapInitialRecord, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> BootstrapProvenance:
    _check_producers(provenance_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base, initial_record, init_profile)
    if type(text) is not str or text == "":
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapProvenanceContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > _provenance_json_bound(provenance_limits, resource):
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    try:
        data = json.loads(text, object_pairs_hook=_pairs, parse_int=_parse_int, parse_float=_reject_float, parse_constant=_reject_constant)
    except BootstrapProvenanceContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict or set(data) != set(FIELD_NAMES):
        _fail()
    for key in _STR_FIELDS:
        if type(data[key]) is not str:
            _fail()
    for key in _BINDING_FIELDS:
        if type(data[key]) is not dict:
            _fail()
    for key in _NV_PUBLIC_FIELDS:
        if type(data[key]) is not dict:
            _fail()
    try:
        value = BootstrapProvenance(
            object_type=data["object_type"], schema_version=data["schema_version"],
            provenance_ref=data["provenance_ref"], provenance_version=data["provenance_version"],
            installation_ref=data["installation_ref"], target_ref=data["target_ref"],
            prepublication_binding=_nested_binding(data["prepublication_binding"]),
            policy_binding=_nested_binding(data["policy_binding"]),
            plan_binding=_nested_binding(data["plan_binding"]),
            recipe_binding=_nested_binding(data["recipe_binding"]),
            initial_base_binding=_nested_binding(data["initial_base_binding"]),
            init_profile_binding=_nested_binding(data["init_profile_binding"]),
            tpm_context_binding=_nested_binding(data["tpm_context_binding"]),
            r0_payload_binding=_nested_binding(data["r0_payload_binding"]),
            r0_semantic_head_hex64=data["r0_semantic_head_hex64"],
            r0_physical_receipt_hex64=data["r0_physical_receipt_hex64"],
            nv_base_observed_hex64=data["nv_base_observed_hex64"],
            nv_after_B_observed_hex64=data["nv_after_B_observed_hex64"],
            observed_from_utc6=data["observed_from_utc6"], observed_to_utc6=data["observed_to_utc6"],
            authority_binding=_nested_binding(data["authority_binding"]),
            procedure_binding=_nested_binding(data["procedure_binding"]),
            executor_binding=_nested_binding(data["executor_binding"]),
            definition_attempt_ref=data["definition_attempt_ref"],
            initialization_attempt_ref=data["initialization_attempt_ref"],
            bootstrap_extend_attempt_ref=data["bootstrap_extend_attempt_ref"],
            nv_public_before_initialization=_nested_nv_public(data["nv_public_before_initialization"]),
            nv_public_after_initialization=_nested_nv_public(data["nv_public_after_initialization"]),
        )
    except BootstrapProvenanceContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_coherence(value, provenance_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base, initial_record, init_profile, expected_nv_public_before, expected_nv_public_after)
    _check_bounds(value, provenance_limits, resource)
    _canon(_payload(value), _provenance_json_bound(provenance_limits, resource))
    return value


def bootstrap_provenance_binding(value: BootstrapProvenance, *, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, plan: BootstrapPlan, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, context: BootstrapTpmContext, base: BootstrapBase, initial_record: BootstrapInitialRecord, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> ContentBinding:
    raw = _validated_canon(value, provenance_limits, producer_limits, resource, plan, prepublication_envelope, policy, context, base, initial_record, init_profile, expected_nv_public_before, expected_nv_public_after)
    digest = hashlib.sha256(raw).hexdigest()
    bound = _provenance_ref_bound(provenance_limits, resource)
    _check_bounded_ref(value.provenance_ref, bound)
    _check_bounded_ref(value.provenance_version, bound)
    try:
        return ContentBinding(ref=value.provenance_ref, version=value.provenance_version, sha256=digest)
    except PgContractError:
        _fail()
