"""Balayeur d'histoire mixte B puis PG1.0 (forme et maths seules)."""
from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from typing import Any, NoReturn

if __package__ == "pixs.pa_native":
    from .postgresql_contracts import PayloadLimits
    from .postgresql_contracts import ContractError as PgContractError
    from .postgresql_contracts import (
        JournalLimits,
        JournalTransition,
        decode_journal_transition,
        encode_journal_transition,
        journal_expected_nv_sha256,
        journal_transition_head_sha256,
    )
    from .bootstrap_base import BootstrapBase
    from .bootstrap_context import BootstrapTpmContext
    from .bootstrap_initial_record import BootstrapInitialRecordContractError as R0ContractError
    from .bootstrap_initial_record import (
        bootstrap_initial_expected_nv_hex,
        bootstrap_initial_physical_receipt_expected,
        bootstrap_initial_semantic_head_hex,
        decode_bootstrap_initial_record,
        derive_bootstrap_initial_record,
        encode_bootstrap_initial_record,
    )
    from .bootstrap_plan import BootstrapPlan
    from .bootstrap_policy_profile import BootstrapPolicyProfile
    from .bootstrap_prepublication import BootstrapPrepublicationEnvelope
    from .bootstrap_resource_profile import BootstrapResourceProfile
elif __package__ in (None, ""):
    if ("postgresql_contracts" in sys.builtin_module_names
            and "bootstrap_base" in sys.builtin_module_names
            and "bootstrap_context" in sys.builtin_module_names
            and "bootstrap_initial_record" in sys.builtin_module_names
            and "bootstrap_plan" in sys.builtin_module_names
            and "bootstrap_policy_profile" in sys.builtin_module_names
            and "bootstrap_prepublication" in sys.builtin_module_names
            and "bootstrap_resource_profile" in sys.builtin_module_names):
        from postgresql_contracts import PayloadLimits
        from postgresql_contracts import ContractError as PgContractError
        from postgresql_contracts import (
            JournalLimits,
            JournalTransition,
            decode_journal_transition,
            encode_journal_transition,
            journal_expected_nv_sha256,
            journal_transition_head_sha256,
        )
        from bootstrap_base import BootstrapBase
        from bootstrap_context import BootstrapTpmContext
        from bootstrap_initial_record import BootstrapInitialRecordContractError as R0ContractError
        from bootstrap_initial_record import (
            bootstrap_initial_expected_nv_hex,
            bootstrap_initial_physical_receipt_expected,
            bootstrap_initial_semantic_head_hex,
            decode_bootstrap_initial_record,
            derive_bootstrap_initial_record,
            encode_bootstrap_initial_record,
        )
        from bootstrap_plan import BootstrapPlan
        from bootstrap_policy_profile import BootstrapPolicyProfile
        from bootstrap_prepublication import BootstrapPrepublicationEnvelope
        from bootstrap_resource_profile import BootstrapResourceProfile
    else:
        raise ImportError("bootstrap_history: unsupported package context")
else:
    raise ImportError("bootstrap_history: unsupported package context")

__all__ = ["BootstrapHistoryScanError", "BootstrapHistoryFacts", "scan_bootstrap_history"]

_MSG = "bootstrap_history: invalid value"
_JOURNAL_HEADER = b"PIXS:PA:JOURNAL:1.0.0\n"
_REC_PREFIX = b"PIXS:PA:JOURNAL:RECORD:1.0.0\n"
_UINT64_MAX = 18446744073709551615


class BootstrapHistoryScanError(ValueError):
    pass


def _fail() -> NoReturn:
    raise BootstrapHistoryScanError(_MSG) from None


def _hex64(value: Any) -> None:
    if type(value) is not str or len(value) != 64:
        _fail()
    for ch in value:
        if ch not in "0123456789abcdef":
            _fail()


@dataclass(frozen=True, slots=True, repr=False)
class BootstrapHistoryFacts:
    file_size: int
    record_count: int
    first_head_hex: str
    first_receipt_hex: str
    expected_nv_b_hex: str
    tail_head_hex: str
    tail_receipt_hex: str
    expected_tail_nv_hex: str
    pg_payloads: tuple[bytes, ...]
    pg_heads_hex: tuple[str, ...]
    pg_expected_nvs_hex: tuple[str, ...]


def _journal_limits(r0_limits: PayloadLimits, resource: BootstrapResourceProfile) -> JournalLimits:
    journal_json = min(r0_limits.max_json_bytes, resource.payload_max_json_bytes, resource.max_record)
    journal_ref = min(r0_limits.max_ref_bytes, resource.payload_max_ref_bytes)
    journal_obs = min(r0_limits.max_observation_refs, resource.payload_max_observation_refs)
    try:
        payload = PayloadLimits(max_json_bytes=journal_json, max_ref_bytes=journal_ref,
                                max_observation_refs=journal_obs)
    except PgContractError:
        _fail()
    try:
        return JournalLimits(payload=payload, max_epoch=resource.max_epoch,
                             max_sequence=resource.max_sequence,
                             max_correlation_refs=resource.max_correlation_refs,
                             max_causation_refs=resource.max_causation_refs)
    except PgContractError:
        _fail()


def scan_bootstrap_history(journal_raw: bytes, provided_current_nv_hex64: str, *,
                           r0_limits: PayloadLimits, producer_limits: PayloadLimits,
                           resource: BootstrapResourceProfile, plan: BootstrapPlan,
                           prepublication_envelope: BootstrapPrepublicationEnvelope,
                           policy: BootstrapPolicyProfile, context: BootstrapTpmContext,
                           base: BootstrapBase) -> BootstrapHistoryFacts:
    # 1. Types classes seuls, puis R0 reel au DEBUT (valide Resource/limits/Plan).
    if type(journal_raw) is not bytes:
        _fail()
    _hex64(provided_current_nv_hex64)
    if (type(r0_limits) is not PayloadLimits or type(producer_limits) is not PayloadLimits
            or type(resource) is not BootstrapResourceProfile or type(plan) is not BootstrapPlan
            or type(prepublication_envelope) is not BootstrapPrepublicationEnvelope
            or type(policy) is not BootstrapPolicyProfile or type(context) is not BootstrapTpmContext
            or type(base) is not BootstrapBase):
        _fail()
    try:
        derived = derive_bootstrap_initial_record(r0_limits=r0_limits, producer_limits=producer_limits,
                                                  resource=resource, plan=plan,
                                                  prepublication_envelope=prepublication_envelope,
                                                  policy=policy, context=context, base=base)
        canon_expected = encode_bootstrap_initial_record(derived, r0_limits=r0_limits,
                                                         producer_limits=producer_limits, resource=resource,
                                                         plan=plan, prepublication_envelope=prepublication_envelope,
                                                         policy=policy, context=context, base=base).encode("utf-8")
    except (R0ContractError, PgContractError):
        _fail()
    # Capacites utilisees telles quelles (zero autorise pour epoch/seq), sans revalidation >0.
    limits = _journal_limits(r0_limits, resource)
    per_frame_cap = min(limits.payload.max_json_bytes, resource.max_record)
    size = len(journal_raw)
    if size < 59 or size > resource.max_bytes:
        _fail()
    if journal_raw[:22] != _JOURNAL_HEADER:
        _fail()
    payloads: list[bytes] = []
    receipts: list[bytes] = []
    previous = b"\x00" * 32
    offset = 22
    count = 0
    while offset < size:
        if count >= resource.max_records or size - offset < 37:
            _fail()
        length = int.from_bytes(journal_raw[offset:offset + 4], "big")
        # 2. Borne AVANT slicing/copy/parse pour B ET PG.
        if length == 0 or length > per_frame_cap or length + 36 > size - offset:
            _fail()
        payload = journal_raw[offset + 4:offset + 4 + length]
        actual = journal_raw[offset + 4 + length:offset + 4 + length + 32]
        expected = hashlib.sha256(_REC_PREFIX + previous + journal_raw[offset:offset + 4] + payload).digest()
        if actual != expected:
            _fail()
        payloads.append(payload)
        receipts.append(expected)
        previous = expected
        offset += length + 36
        count += 1
    if count == 0 or offset != size:
        _fail()
    if payloads[0] != canon_expected:
        _fail()
    try:
        first_text = payloads[0].decode("utf-8")
    except UnicodeDecodeError:
        _fail()
    try:
        decoded = decode_bootstrap_initial_record(first_text, r0_limits=r0_limits,
                                                  producer_limits=producer_limits, resource=resource, plan=plan,
                                                  prepublication_envelope=prepublication_envelope, policy=policy,
                                                  context=context, base=base)
    except (R0ContractError, PgContractError):
        _fail()
    if decoded != derived:
        _fail()
    try:
        first_head = bootstrap_initial_semantic_head_hex(decoded, r0_limits=r0_limits,
                                                         producer_limits=producer_limits, resource=resource,
                                                         plan=plan, prepublication_envelope=prepublication_envelope,
                                                         policy=policy, context=context, base=base)
        first_receipt = bootstrap_initial_physical_receipt_expected(decoded, r0_limits=r0_limits,
                                                                   producer_limits=producer_limits, resource=resource,
                                                                   plan=plan, prepublication_envelope=prepublication_envelope,
                                                                   policy=policy, context=context, base=base)
        expected_nv_b = bootstrap_initial_expected_nv_hex(decoded, r0_limits=r0_limits,
                                                          producer_limits=producer_limits, resource=resource,
                                                          plan=plan, prepublication_envelope=prepublication_envelope,
                                                          policy=policy, context=context, base=base)
    except (R0ContractError, PgContractError):
        _fail()
    _hex64(first_head)
    _hex64(first_receipt)
    _hex64(expected_nv_b)
    if receipts[0].hex() != first_receipt:
        _fail()
    pg_items: list[JournalTransition] = []
    pg_heads: list[str] = []
    pg_nvs: list[str] = []
    for raw in payloads[1:]:
        if len(raw) < 1 or len(raw) > limits.payload.max_json_bytes:
            _fail()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            _fail()
        try:
            item = decode_journal_transition(text, limits)
            back = encode_journal_transition(item, limits).encode("utf-8")
        except PgContractError:
            _fail()
        if back != raw:
            _fail()
        try:
            head = journal_transition_head_sha256(item, limits)
            nv = journal_expected_nv_sha256(item, limits)
        except PgContractError:
            _fail()
        pg_items.append(item)
        pg_heads.append(head)
        pg_nvs.append(nv)
    refs = [decoded.transition_ref]
    if not pg_items:
        if provided_current_nv_hex64 != expected_nv_b:
            _fail()
        return BootstrapHistoryFacts(file_size=size, record_count=count, first_head_hex=first_head,
                                     first_receipt_hex=first_receipt, expected_nv_b_hex=expected_nv_b,
                                     tail_head_hex=first_head, tail_receipt_hex=receipts[0].hex(),
                                     expected_tail_nv_hex=expected_nv_b, pg_payloads=(),
                                     pg_heads_hex=(), pg_expected_nvs_hex=())
    for item in pg_items:
        refs.append(item.transition_ref)
    if len(set(refs)) != len(refs):
        _fail()
    if decoded.sequence == _UINT64_MAX:
        _fail()
    expect_seq = decoded.sequence + 1
    prev_head = first_head
    prev_nv = expected_nv_b
    for index, item in enumerate(pg_items):
        if item.sequence != expect_seq + index or item.sequence > resource.max_sequence:
            _fail()
        if (item.installation_ref != decoded.installation_ref or item.target_ref != decoded.target_ref
                or item.registry_ref != decoded.registry_ref
                or item.registry_generation_ref != decoded.registry_generation_ref
                or item.epoch != decoded.epoch):
            _fail()
        if item.previous_head_sha256 != prev_head or item.previous_nv_value_sha256 != prev_nv:
            _fail()
        prev_head = pg_heads[index]
        prev_nv = pg_nvs[index]
    # Snapshot CurrentNV : comparaison donnee seule, jamais autorite.
    if provided_current_nv_hex64 != pg_nvs[-1]:
        _fail()
    return BootstrapHistoryFacts(file_size=size, record_count=count, first_head_hex=first_head,
                                 first_receipt_hex=first_receipt, expected_nv_b_hex=expected_nv_b,
                                 tail_head_hex=pg_heads[-1], tail_receipt_hex=receipts[-1].hex(),
                                 expected_tail_nv_hex=pg_nvs[-1], pg_payloads=tuple(payloads[1:]),
                                 pg_heads_hex=tuple(pg_heads), pg_expected_nvs_hex=tuple(pg_nvs))
