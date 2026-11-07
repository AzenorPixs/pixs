"""Publication finale B-FIN signee (forme seule, 18 champs).

FORME pure proposee, code NON QUALIFIE : sans admission, acte,
preuve materielle, TPM, PG, PZT, cle privee, verification crypto ni
qualification. Document ferme 18 champs, enveloppe {document,
signature_b64} fermee. PayloadLimits externes explicites par famille
(fin/provenance/producer) sans defaut ni reemploi arbitraire.
Comparaisons = coherence de forme contre objets fournis, jamais preuve
d'autorite, de provenance authentique ou de signature verifiee.
Sans clock/now(), deadline JSON, port, NV, SQL.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import ContentBinding, PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
    from .bootstrap_prepublication import BootstrapPrepublicationEnvelope
    from .bootstrap_prepublication import prepublication_envelope_binding
    from .bootstrap_policy_profile import BootstrapPolicyProfile
    from .bootstrap_policy_profile import bootstrap_policy_profile_binding
    from .bootstrap_plan import BootstrapPlan
    from .bootstrap_plan import bootstrap_plan_binding
    from .bootstrap_initial_record import BootstrapInitialRecord
    from .bootstrap_initial_record import bootstrap_initial_semantic_head_hex
    from .bootstrap_provenance import BootstrapProvenance, BootstrapProvenanceNvPublic
    from .bootstrap_provenance import bootstrap_provenance_binding
    from .bootstrap_context import BootstrapTpmContext
    from .bootstrap_base import BootstrapBase
    from .bootstrap_init_profile import BootstrapInitProfile
    from .bootstrap_resource_profile import BootstrapResourceProfile
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_prepublication" in sys.builtin_module_names
            and "bootstrap_policy_profile" in sys.builtin_module_names
            and "bootstrap_plan" in sys.builtin_module_names
            and "bootstrap_initial_record" in sys.builtin_module_names
            and "bootstrap_provenance" in sys.builtin_module_names
            and "bootstrap_context" in sys.builtin_module_names
            and "bootstrap_base" in sys.builtin_module_names
            and "bootstrap_init_profile" in sys.builtin_module_names
            and "bootstrap_resource_profile" in sys.builtin_module_names):
        from postgresql_contracts import ContentBinding, PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from bootstrap_prepublication import BootstrapPrepublicationEnvelope
        from bootstrap_prepublication import prepublication_envelope_binding
        from bootstrap_policy_profile import BootstrapPolicyProfile
        from bootstrap_policy_profile import bootstrap_policy_profile_binding
        from bootstrap_plan import BootstrapPlan
        from bootstrap_plan import bootstrap_plan_binding
        from bootstrap_initial_record import BootstrapInitialRecord
        from bootstrap_initial_record import bootstrap_initial_semantic_head_hex
        from bootstrap_provenance import BootstrapProvenance, BootstrapProvenanceNvPublic
        from bootstrap_provenance import bootstrap_provenance_binding
        from bootstrap_context import BootstrapTpmContext
        from bootstrap_base import BootstrapBase
        from bootstrap_init_profile import BootstrapInitProfile
        from bootstrap_resource_profile import BootstrapResourceProfile
    else:
        raise ImportError("bootstrap_publication: unsupported package context")
else:
    raise ImportError("bootstrap_publication: unsupported package context")

__all__ = [
    "BootstrapPublicationContractError",
    "BootstrapPublicationFirstContext",
    "BootstrapPublication",
    "BootstrapPublicationEnvelope",
    "encode_bootstrap_publication",
    "decode_bootstrap_publication",
    "publication_signed_bytes",
    "encode_bootstrap_publication_envelope",
    "decode_bootstrap_publication_envelope",
    "publication_envelope_binding",
]

OBJECT_TYPE = "pixs.agent.bootstrap_publication/v1"
SCHEMA_VERSION = "1.0.0"
PLAN_TYPE = "pixs.agent.bootstrap_plan/v1"
ADMISSION_SCOPE = "CONFIGURATION_ONLY"
PREFIX = "PIXS:PA:BOOTSTRAP:PUBLICATION:1.0.0"

FIELD_NAMES = (
    "object_type",
    "schema_version",
    "publication_ref",
    "installation_ref",
    "target_ref",
    "prepublication_binding",
    "policy_binding",
    "plan_type",
    "plan_binding",
    "first_head_sha256",
    "first_sequence",
    "first_context",
    "valid_not_before_utc6",
    "valid_not_after_utc6",
    "observed_from_utc6",
    "observed_to_utc6",
    "provenance_observed_binding",
    "admission_scope",
)

FIRST_CONTEXT_FIELDS = (
    "installation_ref",
    "target_ref",
    "registry_ref",
    "registry_generation_ref",
    "epoch",
)

_HEX = frozenset("0123456789abcdef")

_MSG = "bootstrap_publication: invalid value"


class BootstrapPublicationContractError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapPublicationContractError(_MSG) from None


def _check_limits(limits: Any) -> None:
    if type(limits) is not PayloadLimits:
        _fail()
    if type(limits.max_json_bytes) is not int or isinstance(limits.max_json_bytes, bool):
        _fail()
    if type(limits.max_ref_bytes) is not int or isinstance(limits.max_ref_bytes, bool):
        _fail()
    if type(limits.max_observation_refs) is not int or isinstance(limits.max_observation_refs, bool):
        _fail()
    if limits.max_json_bytes <= 0 or limits.max_ref_bytes <= 0 or limits.max_observation_refs <= 0:
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
    if type(value) is not str or value == "":
        _fail()
    for ch in value:
        if _is_forbidden(ord(ch)):
            _fail()


def _check_bounded_ref(value: Any, bound: int) -> None:
    if type(value) is not str:
        _fail()
    if len(value) > bound:
        _fail()
    for ch in value:
        code = ord(ch)
        if code < 0x20 or code == 0x7F or 0xD800 <= code <= 0xDFFF:
            _fail()
    try:
        size = len(value.encode("utf-8"))
    except UnicodeEncodeError:
        raise BootstrapPublicationContractError(_MSG) from None
    if size < 1 or size > bound:
        _fail()


def _check_hex64(value: Any) -> None:
    if type(value) is not str or len(value) != 64:
        _fail()
    for ch in value:
        if ch not in _HEX:
            _fail()


def _check_utc6_shape(value: Any) -> None:
    if type(value) is not str or len(value) != 27:
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


def _check_sig_b64(sig: Any) -> bytes:
    if type(sig) is not str or len(sig) != 88:
        _fail()
    for ch in sig:
        if ch in "-_":
            _fail()
    try:
        raw = base64.b64decode(sig.encode("ascii"), validate=True)
    except (ValueError, binascii.Error, UnicodeEncodeError) as error:
        raise BootstrapPublicationContractError(_MSG) from error
    if len(raw) != 64:
        _fail()
    if base64.b64encode(raw).decode("ascii") != sig:
        _fail()
    return raw


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPublicationFirstContext:
    installation_ref: str
    target_ref: str
    registry_ref: str
    registry_generation_ref: str
    epoch: int

    def __post_init__(self) -> None:
        _check_strict_text(self.installation_ref)
        _check_strict_text(self.target_ref)
        _check_strict_text(self.registry_ref)
        _check_strict_text(self.registry_generation_ref)
        if type(self.epoch) is not int or isinstance(self.epoch, bool):
            _fail()
        if self.epoch < 0 or self.epoch > 18446744073709551615:
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPublication:
    object_type: str
    schema_version: str
    publication_ref: str
    installation_ref: str
    target_ref: str
    prepublication_binding: ContentBinding
    policy_binding: ContentBinding
    plan_type: str
    plan_binding: ContentBinding
    first_head_sha256: str
    first_sequence: int
    first_context: BootstrapPublicationFirstContext
    valid_not_before_utc6: str
    valid_not_after_utc6: str
    observed_from_utc6: str
    observed_to_utc6: str
    provenance_observed_binding: ContentBinding
    admission_scope: str

    def __post_init__(self) -> None:
        if type(self.object_type) is not str or self.object_type != OBJECT_TYPE:
            _fail()
        if type(self.schema_version) is not str or self.schema_version != SCHEMA_VERSION:
            _fail()
        _check_strict_text(self.publication_ref)
        _check_strict_text(self.installation_ref)
        _check_strict_text(self.target_ref)
        if type(self.prepublication_binding) is not ContentBinding:
            _fail()
        if type(self.policy_binding) is not ContentBinding:
            _fail()
        if type(self.plan_type) is not str or self.plan_type != PLAN_TYPE:
            _fail()
        if type(self.plan_binding) is not ContentBinding:
            _fail()
        _check_hex64(self.first_head_sha256)
        if type(self.first_sequence) is not int or isinstance(self.first_sequence, bool):
            _fail()
        if self.first_sequence < 0 or self.first_sequence > 18446744073709551615:
            _fail()
        if type(self.first_context) is not BootstrapPublicationFirstContext:
            _fail()
        self.first_context.__post_init__()
        _check_utc6_shape(self.valid_not_before_utc6)
        _check_utc6_shape(self.valid_not_after_utc6)
        _check_utc6_shape(self.observed_from_utc6)
        _check_utc6_shape(self.observed_to_utc6)
        if type(self.provenance_observed_binding) is not ContentBinding:
            _fail()
        if type(self.admission_scope) is not str or self.admission_scope != ADMISSION_SCOPE:
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapPublicationEnvelope:
    document: BootstrapPublication
    signature_b64: str

    def __post_init__(self) -> None:
        if type(self.document) is not BootstrapPublication:
            _fail()
        _check_sig_b64(self.signature_b64)


def _check_all_limits(fin_limits: Any, provenance_limits: Any, producer_limits: Any) -> None:
    _check_limits(fin_limits)
    _check_limits(provenance_limits)
    _check_limits(producer_limits)


def _check_types(fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> None:
    if type(resource) is not BootstrapResourceProfile:
        _fail()
    if type(prepublication_envelope) is not BootstrapPrepublicationEnvelope:
        _fail()
    if type(policy) is not BootstrapPolicyProfile:
        _fail()
    if type(plan) is not BootstrapPlan:
        _fail()
    if type(initial_record) is not BootstrapInitialRecord:
        _fail()
    if type(provenance) is not BootstrapProvenance:
        _fail()
    if type(context) is not BootstrapTpmContext:
        _fail()
    if type(base) is not BootstrapBase:
        _fail()
    if type(init_profile) is not BootstrapInitProfile:
        _fail()
    if type(expected_nv_public_before) is not BootstrapProvenanceNvPublic:
        _fail()
    if type(expected_nv_public_after) is not BootstrapProvenanceNvPublic:
        _fail()
    _check_all_limits(fin_limits, provenance_limits, producer_limits)


def _check_context_complete(value: BootstrapPublication, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: Any, prepublication_envelope: Any, policy: Any, plan: Any, initial_record: Any, provenance: Any, context: Any, base: Any, init_profile: Any, expected_nv_public_before: Any, expected_nv_public_after: Any) -> None:
    _check_types(fin_limits, provenance_limits, producer_limits, resource, prepublication_envelope, policy, plan, initial_record, provenance, context, base, init_profile, expected_nv_public_before, expected_nv_public_after)
    if type(value) is not BootstrapPublication:
        _fail()
    value.__post_init__()
    try:
        exp_pub = prepublication_envelope_binding(prepublication_envelope, producer_limits, resource)
        exp_pol = bootstrap_policy_profile_binding(policy, producer_limits, resource)
        exp_plan = bootstrap_plan_binding(plan, producer_limits, prepublication_envelope, policy, resource, context, base)
        exp_prov = bootstrap_provenance_binding(provenance, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base, initial_record=initial_record, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
        exp_head = bootstrap_initial_semantic_head_hex(initial_record, r0_limits=producer_limits, producer_limits=producer_limits, resource=resource, plan=plan, prepublication_envelope=prepublication_envelope, policy=policy, context=context, base=base)
    except (ValueError, TypeError, RecursionError):
        _fail()
    if value.prepublication_binding != exp_pub:
        _fail()
    if value.policy_binding != exp_pol:
        _fail()
    if value.plan_binding != exp_plan:
        _fail()
    if value.provenance_observed_binding != exp_prov:
        _fail()
    if value.first_head_sha256 != exp_head:
        _fail()
    if value.first_sequence != initial_record.sequence:
        _fail()
    fc = value.first_context
    if fc.installation_ref != initial_record.installation_ref:
        _fail()
    if fc.target_ref != initial_record.target_ref:
        _fail()
    if fc.registry_ref != initial_record.registry_ref:
        _fail()
    if fc.registry_generation_ref != initial_record.registry_generation_ref:
        _fail()
    if fc.epoch != initial_record.epoch:
        _fail()
    if value.installation_ref != fc.installation_ref:
        _fail()
    if value.target_ref != fc.target_ref:
        _fail()
    if value.observed_from_utc6 != provenance.observed_from_utc6:
        _fail()
    if value.observed_to_utc6 != provenance.observed_to_utc6:
        _fail()
    if _parse_utc6(value.valid_not_after_utc6) <= _parse_utc6(value.valid_not_before_utc6):
        _fail()
    if _parse_utc6(value.observed_to_utc6) < _parse_utc6(value.observed_from_utc6):
        _fail()
    pub_before = _parse_utc6(prepublication_envelope.document.valid_not_before_utc6)
    pub_after = _parse_utc6(prepublication_envelope.document.valid_not_after_utc6)
    pol_before = _parse_utc6(policy.valid_not_before_utc6)
    pol_after = _parse_utc6(policy.valid_not_after_utc6)
    fin_before = _parse_utc6(value.valid_not_before_utc6)
    fin_after = _parse_utc6(value.valid_not_after_utc6)
    inter_before = pub_before if pub_before >= pol_before else pol_before
    inter_after = pub_after if pub_after <= pol_after else pol_after
    if inter_after <= inter_before:
        _fail()
    if fin_before < inter_before or fin_after > inter_after:
        _fail()
    _delta_fin = fin_after - fin_before
    fin_span = (_delta_fin.days * 86400 + _delta_fin.seconds) * 1000000000 + _delta_fin.microseconds * 1000
    if fin_span <= 0 or fin_span > resource.max_validity_span_ns:
        _fail()
    bound = min(fin_limits.max_ref_bytes, resource.payload_max_ref_bytes)
    for name in ("publication_ref", "installation_ref", "target_ref"):
        _check_bounded_ref(getattr(value, name), bound)
    for name in ("installation_ref", "target_ref", "registry_ref", "registry_generation_ref"):
        _check_bounded_ref(getattr(value.first_context, name), bound)
    for b in (value.prepublication_binding, value.policy_binding, value.plan_binding, value.provenance_observed_binding):
        _check_bounded_ref(b.ref, bound)
        _check_bounded_ref(b.version, bound)
        _check_hex64(b.sha256)


def _first_context_payload(fc: BootstrapPublicationFirstContext) -> dict:
    return {"installation_ref": fc.installation_ref, "target_ref": fc.target_ref, "registry_ref": fc.registry_ref, "registry_generation_ref": fc.registry_generation_ref, "epoch": fc.epoch}


def _binding_payload(binding: ContentBinding) -> dict:
    return {"ref": binding.ref, "version": binding.version, "sha256": binding.sha256}


def _payload(value: BootstrapPublication) -> dict:
    return {
        "object_type": value.object_type, "schema_version": value.schema_version,
        "publication_ref": value.publication_ref, "installation_ref": value.installation_ref, "target_ref": value.target_ref,
        "prepublication_binding": _binding_payload(value.prepublication_binding),
        "policy_binding": _binding_payload(value.policy_binding),
        "plan_type": value.plan_type, "plan_binding": _binding_payload(value.plan_binding),
        "first_head_sha256": value.first_head_sha256, "first_sequence": value.first_sequence,
        "first_context": _first_context_payload(value.first_context),
        "valid_not_before_utc6": value.valid_not_before_utc6, "valid_not_after_utc6": value.valid_not_after_utc6,
        "observed_from_utc6": value.observed_from_utc6, "observed_to_utc6": value.observed_to_utc6,
        "provenance_observed_binding": _binding_payload(value.provenance_observed_binding),
        "admission_scope": value.admission_scope,
    }


def _canon(payload: dict, fin_limits: PayloadLimits, resource: Any) -> str:
    try:
        text = json.dumps(payload, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError):
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPublicationContractError(_MSG) from None
    bound = min(fin_limits.max_json_bytes, resource.payload_max_json_bytes)
    if len(raw) < 1 or len(raw) > bound:
        _fail()
    if b"\r" in raw or b"\n" in raw:
        _fail()
    return text


def _validated_canon(value: BootstrapPublication, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: Any, prepublication_envelope: Any, policy: Any, plan: Any, initial_record: Any, provenance: Any, context: Any, base: Any, init_profile: Any, expected_nv_public_before: Any, expected_nv_public_after: Any) -> bytes:
    _check_context_complete(value, fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
    return _canon(_payload(value), fin_limits, resource).encode("utf-8")


def encode_bootstrap_publication(value: BootstrapPublication, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> str:
    return _validated_canon(value, fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after).decode("utf-8")


def _parse_int(token: str) -> int:
    if token[:1] == "-":
        _fail()
    if len(token) > 20:
        _fail()
    if len(token) == 20 and token > "18446744073709551615":
        _fail()
    try:
        return int(token, 10)
    except ValueError:
        _fail()


def _reject_float(token: str) -> NoReturn:
    raise BootstrapPublicationContractError(_MSG) from None


def _reject_constant(token: str) -> NoReturn:
    raise BootstrapPublicationContractError(_MSG) from None


def _pairs(pairs: list) -> dict:
    keys = [k for k, _ in pairs]
    if any(type(k) is not str for k in keys) or len(set(keys)) != len(keys):
        _fail()
    keyset = set(keys)
    if keyset == frozenset(("ref", "version", "sha256")):
        for _, v in pairs:
            if type(v) is not str:
                _fail()
        return {k: v for k, v in pairs}
    if keyset == frozenset(("document", "signature_b64")):
        return {k: v for k, v in pairs}
    if keyset == frozenset(("installation_ref", "target_ref", "registry_ref", "registry_generation_ref", "epoch")):
        return {k: v for k, v in pairs}
    if keyset == set(FIELD_NAMES):
        return {k: v for k, v in pairs}
    _fail()


def _nested_binding(data: Any) -> ContentBinding:
    if type(data) is not dict or set(data) != frozenset(("ref", "version", "sha256")):
        _fail()
    try:
        return ContentBinding(ref=data["ref"], version=data["version"], sha256=data["sha256"])
    except PgContractError:
        _fail()
    except (TypeError, KeyError):
        _fail()


def _nested_first_context(data: Any) -> BootstrapPublicationFirstContext:
    if type(data) is not dict or set(data) != set(FIRST_CONTEXT_FIELDS):
        _fail()
    try:
        return BootstrapPublicationFirstContext(installation_ref=data["installation_ref"], target_ref=data["target_ref"], registry_ref=data["registry_ref"], registry_generation_ref=data["registry_generation_ref"], epoch=data["epoch"])
    except BootstrapPublicationContractError:
        raise
    except (TypeError, KeyError):
        _fail()


def decode_bootstrap_publication(text: str, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> BootstrapPublication:
    _check_types(fin_limits, provenance_limits, producer_limits, resource, prepublication_envelope, policy, plan, initial_record, provenance, context, base, init_profile, expected_nv_public_before, expected_nv_public_after)
    if type(text) is not str or text == "":
        _fail()
    bound = min(fin_limits.max_json_bytes, resource.payload_max_json_bytes)
    if len(text) > bound:
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPublicationContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > bound:
        _fail()
    try:
        data = json.loads(text, object_pairs_hook=_pairs, parse_int=_parse_int, parse_float=_reject_float, parse_constant=_reject_constant)
    except BootstrapPublicationContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict or set(data) != set(FIELD_NAMES):
        _fail()
    try:
        value = BootstrapPublication(object_type=data["object_type"], schema_version=data["schema_version"], publication_ref=data["publication_ref"], installation_ref=data["installation_ref"], target_ref=data["target_ref"], prepublication_binding=_nested_binding(data["prepublication_binding"]), policy_binding=_nested_binding(data["policy_binding"]), plan_type=data["plan_type"], plan_binding=_nested_binding(data["plan_binding"]), first_head_sha256=data["first_head_sha256"], first_sequence=data["first_sequence"], first_context=_nested_first_context(data["first_context"]), valid_not_before_utc6=data["valid_not_before_utc6"], valid_not_after_utc6=data["valid_not_after_utc6"], observed_from_utc6=data["observed_from_utc6"], observed_to_utc6=data["observed_to_utc6"], provenance_observed_binding=_nested_binding(data["provenance_observed_binding"]), admission_scope=data["admission_scope"])
    except BootstrapPublicationContractError:
        raise
    except (TypeError, KeyError):
        _fail()
    _check_context_complete(value, fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
    _canon(_payload(value), fin_limits, resource)
    return value


def publication_signed_bytes(value: BootstrapPublication, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> bytes:
    raw = _validated_canon(value, fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
    return PREFIX.encode("ascii") + b"\n" + raw


def encode_bootstrap_publication_envelope(env: BootstrapPublicationEnvelope, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> str:
    _check_all_limits(fin_limits, provenance_limits, producer_limits)
    if type(env) is not BootstrapPublicationEnvelope:
        _fail()
    env.__post_init__()
    _check_context_complete(env.document, fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
    payload = {"document": _payload(env.document), "signature_b64": env.signature_b64}
    return _canon(payload, fin_limits, resource)


def decode_bootstrap_publication_envelope(text: str, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> BootstrapPublicationEnvelope:
    _check_types(fin_limits, provenance_limits, producer_limits, resource, prepublication_envelope, policy, plan, initial_record, provenance, context, base, init_profile, expected_nv_public_before, expected_nv_public_after)
    if type(text) is not str or text == "":
        _fail()
    bound = min(fin_limits.max_json_bytes, resource.payload_max_json_bytes)
    if len(text) > bound:
        _fail()
    try:
        raw = text.encode("utf-8")
    except UnicodeEncodeError:
        raise BootstrapPublicationContractError(_MSG) from None
    if len(raw) < 1 or len(raw) > bound:
        _fail()
    try:
        data = json.loads(text, object_pairs_hook=_pairs, parse_int=_parse_int, parse_float=_reject_float, parse_constant=_reject_constant)
    except BootstrapPublicationContractError:
        raise
    except (json.JSONDecodeError, RecursionError):
        _fail()
    if type(data) is not dict or set(data) != frozenset(("document", "signature_b64")):
        _fail()
    doc_data = data["document"]
    sig = data["signature_b64"]
    if type(doc_data) is not dict or type(sig) is not str:
        _fail()
    doc = decode_bootstrap_publication(json.dumps(doc_data, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")), fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
    _check_sig_b64(sig)
    try:
        return BootstrapPublicationEnvelope(document=doc, signature_b64=sig)
    except BootstrapPublicationContractError:
        raise
    except TypeError:
        _fail()


def publication_envelope_binding(env: BootstrapPublicationEnvelope, *, fin_limits: PayloadLimits, provenance_limits: PayloadLimits, producer_limits: PayloadLimits, resource: BootstrapResourceProfile, prepublication_envelope: BootstrapPrepublicationEnvelope, policy: BootstrapPolicyProfile, plan: BootstrapPlan, initial_record: BootstrapInitialRecord, provenance: BootstrapProvenance, context: BootstrapTpmContext, base: BootstrapBase, init_profile: BootstrapInitProfile, expected_nv_public_before: BootstrapProvenanceNvPublic, expected_nv_public_after: BootstrapProvenanceNvPublic) -> ContentBinding:
    _check_all_limits(fin_limits, provenance_limits, producer_limits)
    text = encode_bootstrap_publication_envelope(env, fin_limits=fin_limits, provenance_limits=provenance_limits, producer_limits=producer_limits, resource=resource, prepublication_envelope=prepublication_envelope, policy=policy, plan=plan, initial_record=initial_record, provenance=provenance, context=context, base=base, init_profile=init_profile, expected_nv_public_before=expected_nv_public_before, expected_nv_public_after=expected_nv_public_after)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    _check_bounded_ref(env.document.publication_ref, min(fin_limits.max_ref_bytes, resource.payload_max_ref_bytes))
    _check_bounded_ref(env.document.schema_version, min(fin_limits.max_ref_bytes, resource.payload_max_ref_bytes))
    try:
        return ContentBinding(ref=env.document.publication_ref, version=env.document.schema_version, sha256=digest)
    except PgContractError:
        _fail()
