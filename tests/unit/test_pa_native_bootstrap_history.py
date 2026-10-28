"""Histoire mixte B+PG : octets reels, sans IO ni autorite."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import struct
import unittest
from unittest.mock import patch

from pixs.pa_native.bootstrap_history import (
    BootstrapHistoryFacts,
    BootstrapHistoryScanError,
    scan_bootstrap_history,
)
from pixs.pa_native.postgresql_contracts import (
    ContentBinding,
    JournalLimits,
    JournalTransition,
    PayloadLimits,
    decode_journal_transition,
    encode_journal_transition,
    journal_expected_nv_sha256,
    journal_transition_head_sha256,
)
from pixs.pa_native.bootstrap_initial_record import (
    bootstrap_initial_expected_nv_hex,
    bootstrap_initial_semantic_head_hex,
)
from tests.unit.test_pa_native_bootstrap_initial_record import (
    _candidate_from_oracle,
    _closure,
    _kw,
    _oracle19,
    _plan_for,
    _recipe_for,
)

_HEADER = b"PIXS:PA:JOURNAL:1.0.0\n"
_PREFIX = b"PIXS:PA:JOURNAL:RECORD:1.0.0\n"


def _bind(ref="m-qxqx", ver="1.0.0", digest=None):
    return ContentBinding(ref=ref, version=ver, sha256=digest or "ab" * 32)


def _frame(payload: bytes, previous: bytes) -> bytes:
    length = struct.pack(">I", len(payload))
    receipt = hashlib.sha256(_PREFIX + previous + length + payload).digest()
    return length + payload + receipt


def _journal(payloads):
    raw = bytearray(_HEADER)
    previous = b"\x00" * 32
    for payload in payloads:
        raw += _frame(payload, previous)
        previous = hashlib.sha256(_PREFIX + previous + struct.pack(">I", len(payload)) + payload).digest()
    return bytes(raw)


def _journal_limits_for(closure):
    limits, resource, _, _, _, _, _ = closure
    journal_json = min(limits.max_json_bytes, resource.payload_max_json_bytes, resource.max_record)
    journal_ref = min(limits.max_ref_bytes, resource.payload_max_ref_bytes)
    journal_obs = min(limits.max_observation_refs, resource.payload_max_observation_refs)
    payload = PayloadLimits(max_json_bytes=journal_json, max_ref_bytes=journal_ref,
                            max_observation_refs=journal_obs)
    return JournalLimits(payload=payload, max_epoch=resource.max_epoch,
                         max_sequence=resource.max_sequence,
                         max_correlation_refs=resource.max_correlation_refs,
                         max_causation_refs=resource.max_causation_refs)


def _pg_payload(closure, seq, prev_head, prev_nv, tref, epoch=None):
    limits_j = _journal_limits_for(closure)
    _, resource, _, _, _, _, _ = closure
    use_epoch = resource.epoch if epoch is None else epoch
    item = JournalTransition(object_type="pixs.agent.postgresql.journal_transition/v1",
                             schema_version="1.0.0", transition_ref=tref, installation_ref="inst",
                             target_ref="tgt", registry_ref="reg", registry_generation_ref="gen",
                             epoch=use_epoch, sequence=seq, previous_head_sha256=prev_head,
                             previous_nv_value_sha256=prev_nv, state="OBSERVED",
                             operation_ref="op-" + tref, mandate_binding=_bind("mand-" + tref),
                             content_binding=_bind("cont-" + tref),
                             correlation_refs=(), causation_refs=())
    text = encode_journal_transition(item, limits_j)
    self_check = decode_journal_transition(text, limits_j)
    assert self_check == item
    assert encode_journal_transition(self_check, limits_j) == text
    return (text.encode("utf-8"), journal_transition_head_sha256(item, limits_j),
            journal_expected_nv_sha256(item, limits_j), item)


def _b_payload_positive(closure, plan):
    oracle, text, _, _ = _oracle19(closure, plan)
    candidate = _candidate_from_oracle(oracle)
    from pixs.pa_native.bootstrap_initial_record import encode_bootstrap_initial_record
    assert encode_bootstrap_initial_record(candidate, **_kw(closure, plan)) == text
    return text.encode("utf-8")


def _b_bytes_via_oracle(closure, plan):
    oracle, text, _, _ = _oracle19(closure, plan)
    assert set(oracle) == {"object_type", "schema_version", "transition_ref", "registry_ref",
                           "registry_generation_ref", "epoch", "sequence", "correlation_refs",
                           "causation_refs", "installation_ref", "target_ref", "prepublication_binding",
                           "policy_binding", "resource_profile_binding", "nv_profile",
                           "tpm_context_binding", "initial_base_binding", "plan_binding", "recipe_binding"}
    return text.encode("utf-8")


def _nv_b_of(closure, plan):
    return bootstrap_initial_expected_nv_hex(
        _candidate_from_oracle(_oracle19(closure, plan)[0]), **_kw(closure, plan))


def _head_b_of(closure, plan):
    return bootstrap_initial_semantic_head_hex(
        _candidate_from_oracle(_oracle19(closure, plan)[0]), **_kw(closure, plan))


class BootstrapHistoryNominalTest(unittest.TestCase):
    def test_b_seul_seq0(self):
        closure = _closure()
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        nv_b = _nv_b_of(closure, plan)
        facts = scan_bootstrap_history(_journal([raw_b]), nv_b, **_kw(closure, plan))
        self.assertEqual(facts.record_count, 1)
        self.assertEqual(facts.expected_tail_nv_hex, nv_b)
        self.assertEqual(facts.pg_payloads, ())

    def test_b_plus_1pg(self):
        closure = _closure(max_sequence=10, max_records=10, max_bytes=60000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        pg_raw, _, pg_nv, _ = _pg_payload(closure, 1, head_b, nv_b, "pg-1-qxqx")
        facts = scan_bootstrap_history(_journal([raw_b, pg_raw]), pg_nv, **_kw(closure, plan))
        self.assertEqual(facts.record_count, 2)
        self.assertEqual(facts.expected_tail_nv_hex, pg_nv)

    def test_b_plus_2pg_tail_hashes(self):
        closure = _closure(max_sequence=10, max_records=10, max_bytes=90000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        pg1, head1, nv1, _ = _pg_payload(closure, 1, head_b, nv_b, "pg-1-qxqx")
        pg2, head2, nv2, _ = _pg_payload(closure, 2, head1, nv1, "pg-2-qxqx")
        journal = _journal([raw_b, pg1, pg2])
        facts = scan_bootstrap_history(journal, nv2, **_kw(closure, plan))
        self.assertEqual((facts.record_count, len(facts.pg_payloads)), (3, 2))
        self.assertEqual(facts.expected_tail_nv_hex, nv2)
        self.assertEqual(facts.file_size, len(journal))
        self.assertEqual(facts.tail_receipt_hex, journal[-32:].hex())
        self.assertEqual(facts.tail_head_hex, head2)
        self.assertEqual(facts.pg_heads_hex, (head1, head2))
        self.assertEqual(facts.pg_expected_nvs_hex, (nv1, nv2))

    def test_seq7_et_max_seuls(self):
        closure = _closure(epoch=5, first_sequence=7, max_epoch=100, max_sequence=100,
                           max_bytes=60000, max_records=10)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource, epoch=5, sequence=7,
                             correlation_refs=("s1",), causation_refs=("t1",))
        plan = _plan_for(closure, recipe)
        nv_b = _nv_b_of(closure, plan)
        facts = scan_bootstrap_history(_journal([_b_payload_positive(closure, plan)]), nv_b,
                                       **_kw(closure, plan))
        self.assertEqual(facts.record_count, 1)
        big = 2 ** 64 - 1
        closure2 = _closure(epoch=big, first_sequence=big, max_epoch=big, max_sequence=big,
                            max_bytes=60000, max_records=10)
        limits2, resource2, _, _, _, _, _ = closure2
        recipe2 = _recipe_for(limits2, closure2[4], resource2, epoch=big, sequence=big,
                              correlation_refs=(), causation_refs=())
        plan2 = _plan_for(closure2, recipe2)
        nv2 = _nv_b_of(closure2, plan2)
        facts2 = scan_bootstrap_history(_journal([_b_payload_positive(closure2, plan2)]), nv2,
                                        **_kw(closure2, plan2))
        self.assertEqual(facts2.record_count, 1)

    def test_overflow_max_pg_valide_seul_mais_mixte_refuse(self):
        big = 2 ** 64 - 1
        closure = _closure(epoch=big, first_sequence=big, max_epoch=big, max_sequence=big,
                           max_bytes=90000, max_records=10)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource, epoch=big, sequence=big,
                             correlation_refs=(), causation_refs=())
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        pg_raw, _, pg_nv, item = _pg_payload(closure, 0, head_b, nv_b, "pg-0-qxqx", epoch=big)
        limits_j = _journal_limits_for(closure)
        self.assertEqual(encode_journal_transition(item, limits_j).encode("utf-8"), pg_raw)
        with self.assertRaises(BootstrapHistoryScanError):
            scan_bootstrap_history(_journal([raw_b, pg_raw]), pg_nv, **_kw(closure, plan))


class BootstrapHistorySemanticTest(unittest.TestCase):
    def test_context_seq_prev_reconstruits(self):
        closure = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=90000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        base_pg, _, _, base_item = _pg_payload(closure, 1, head_b, nv_b, "pg-1-qxqx")
        limits_j = _journal_limits_for(closure)
        good_nv = journal_expected_nv_sha256(base_item, limits_j)
        for field, bad in (("installation_ref", "bad-inst"), ("target_ref", "bad-tgt"),
                           ("registry_ref", "bad-reg"), ("registry_generation_ref", "bad-gen"),
                           ("epoch", 2)):
            with self.subTest(field=field):
                mutated = dataclasses.replace(base_item, **{field: bad})
                text = encode_journal_transition(mutated, limits_j).encode("utf-8")
                head_m = journal_transition_head_sha256(mutated, limits_j)
                nv_m = journal_expected_nv_sha256(mutated, limits_j)
                with self.assertRaises(BootstrapHistoryScanError):
                    scan_bootstrap_history(_journal([raw_b, text]), nv_m, **_kw(closure, plan))
        with self.subTest(field="seq-gap"):
            mutated = dataclasses.replace(base_item, sequence=5)
            text = encode_journal_transition(mutated, limits_j).encode("utf-8")
            nv_m = journal_expected_nv_sha256(mutated, limits_j)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, text]), nv_m, **_kw(closure, plan))
        with self.subTest(field="prev-head"):
            mutated = dataclasses.replace(base_item, previous_head_sha256="ff" * 32)
            text = encode_journal_transition(mutated, limits_j).encode("utf-8")
            nv_m = journal_expected_nv_sha256(mutated, limits_j)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, text]), nv_m, **_kw(closure, plan))
        with self.subTest(field="prev-nv"):
            mutated = dataclasses.replace(base_item, previous_nv_value_sha256="00" * 32)
            text = encode_journal_transition(mutated, limits_j).encode("utf-8")
            nv_m = journal_expected_nv_sha256(mutated, limits_j)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, text]), nv_m, **_kw(closure, plan))

    def test_duplicate_ordre_types_noncanon(self):
        closure = _closure(max_sequence=10, max_records=10, max_bytes=90000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        pg1, head1, nv1, _ = _pg_payload(closure, 1, head_b, nv_b, "pg-1-qxqx")
        _, _, nv2, _ = _pg_payload(closure, 2, head1, nv1, "pg-1-qxqx")
        with self.subTest(case="dup-ref-correct-chain"):
            pg2dup, _, _, _ = _pg_payload(closure, 2, head1, nv1, "pg-1-qxqx")
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, pg1, pg2dup]), nv2, **_kw(closure, plan))
        with self.subTest(case="pg-avant-b"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([pg1, raw_b]), nv1, **_kw(closure, plan))
        with self.subTest(case="double-b"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, raw_b]), nv_b, **_kw(closure, plan))
        with self.subTest(case="b-noncanon-espace"):
            data = json.loads(raw_b.decode("utf-8"))
            noncanon = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(", ", ": ")).encode("utf-8")
            self.assertNotEqual(noncanon, raw_b)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([noncanon]), nv_b, **_kw(closure, plan))

    def test_reconstitution_tampered_avant_decode(self):
        closure = _closure()
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        data = json.loads(raw_b.decode("utf-8"))
        data["installation_ref"] = "autr"
        tampered = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.assertNotEqual(tampered, raw_b)
        from pixs.pa_native.bootstrap_initial_record import bootstrap_initial_expected_nv_hex
        from tests.unit.test_pa_native_bootstrap_initial_record import _candidate_from_oracle
        good = _candidate_from_oracle(_oracle19(closure, plan)[0])
        nv_b = bootstrap_initial_expected_nv_hex(good, **_kw(closure, plan))
        with self.assertRaises(BootstrapHistoryScanError):
            scan_bootstrap_history(_journal([tampered]), nv_b, **_kw(closure, plan))


class BootstrapHistoryFramesTest(unittest.TestCase):
    def test_physiques(self):
        closure = _closure(max_sequence=10, max_records=10, max_bytes=90000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        nv_b = _nv_b_of(closure, plan)
        journal = _journal([raw_b])
        with self.subTest(case="faux-recu"):
            bad = bytearray(journal)
            bad[-1] ^= 1
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(bytes(bad), nv_b, **_kw(closure, plan))
        with self.subTest(case="faux-header"):
            bad = b"X" + journal[1:]
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(bad, nv_b, **_kw(closure, plan))
        with self.subTest(case="len0"):
            bad = _HEADER + struct.pack(">I", 0) + b"X" * 32
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(bad, nv_b, **_kw(closure, plan))
        with self.subTest(case="tronque-payload"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(journal[:-2], nv_b, **_kw(closure, plan))
        with self.subTest(case="trailing"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(journal + b"\x00", nv_b, **_kw(closure, plan))
        with self.subTest(case="vide-header-seul"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(b"", nv_b, **_kw(closure, plan))
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_HEADER, nv_b, **_kw(closure, plan))
        with self.subTest(case="types-entree"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(bytearray(journal), nv_b, **_kw(closure, plan))
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(journal.decode("utf-8", errors="ignore"), nv_b, **_kw(closure, plan))
        with self.subTest(case="faux-nv"):
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(journal, "ff" * 32, **_kw(closure, plan))

    def test_caps_reconstruits(self):
        closure0 = _closure(max_sequence=10, max_records=10, max_bytes=90000)
        limits0, resource0, _, _, _, _, _ = closure0
        recipe0 = _recipe_for(limits0, closure0[4], resource0)
        plan0 = _plan_for(closure0, recipe0)
        raw_b0 = _b_payload_positive(closure0, plan0)
        head0, nv0 = _head_b_of(closure0, plan0), _nv_b_of(closure0, plan0)
        pg0, _, _, _ = _pg_payload(closure0, 1, head0, nv0, "pg-1-qxqx")
        cap_record = max(len(raw_b0), len(pg0))
        wide = _closure(max_sequence=10, max_records=10, max_bytes=90000,
                        max_record=cap_record, payload_max_json_bytes=32768,
                        payload_max_ref_bytes=256, payload_max_observation_refs=16)
        limits_w, resource_w, _, _, _, _, _ = wide
        recipe_w = _recipe_for(limits_w, wide[4], resource_w)
        plan_w = _plan_for(wide, recipe_w)
        raw_bw = _b_payload_positive(wide, plan_w)
        head_w, _ = _head_b_of(wide, plan_w), _nv_b_of(wide, plan_w)
        pg_w, _, _, _ = _pg_payload(wide, 1, head_w, _nv_b_of(wide, plan_w), "pg-1-qxqx")
        journal_w = _journal([raw_bw, pg_w])
        exact_n = len(journal_w)
        self.assertGreater(exact_n, cap_record + 58)
        rebuilt = _closure(max_sequence=10, max_records=2, max_bytes=exact_n,
                           max_record=cap_record, payload_max_json_bytes=32768,
                           payload_max_ref_bytes=256, payload_max_observation_refs=16)
        limits2, resource2, _, _, _, _, _ = rebuilt
        recipe2 = _recipe_for(limits2, rebuilt[4], resource2)
        plan2 = _plan_for(rebuilt, recipe2)
        raw_b2 = _b_payload_positive(rebuilt, plan2)
        head2, nv2 = _head_b_of(rebuilt, plan2), _nv_b_of(rebuilt, plan2)
        pg2, pg_head2, pg_nv2, _ = _pg_payload(rebuilt, 1, head2, nv2, "pg-1-qxqx")
        journal2 = _journal([raw_b2, pg2])
        self.assertEqual(len(journal2), exact_n)
        facts = scan_bootstrap_history(journal2, pg_nv2, **_kw(rebuilt, plan2))
        self.assertEqual(facts.record_count, 2)
        self.assertEqual(facts.expected_tail_nv_hex, pg_nv2)
        rebuilt_count = _closure(max_sequence=10, max_records=1, max_bytes=90000,
                                 max_record=cap_record, payload_max_json_bytes=32768,
                                 payload_max_ref_bytes=256, payload_max_observation_refs=16)
        limits_c, _, _, _, _, _, _ = rebuilt_count
        recipe_c = _recipe_for(limits_c, rebuilt_count[4], rebuilt_count[1])
        plan_c = _plan_for(rebuilt_count, recipe_c)
        raw_bc = _b_payload_positive(rebuilt_count, plan_c)
        head_c, nv_c = _head_b_of(rebuilt_count, plan_c), _nv_b_of(rebuilt_count, plan_c)
        pg_c, _, pg_nv_c, _ = _pg_payload(rebuilt_count, 1, head_c, nv_c, "pg-1-qxqx")
        journal_c = _journal([raw_bc, pg_c])
        self.assertEqual(len([raw_bc, pg_c]), 2)
        with self.assertRaises(BootstrapHistoryScanError):
            scan_bootstrap_history(journal_c, pg_nv_c, **_kw(rebuilt_count, plan_c))
        rebuilt_bytes = _closure(max_sequence=10, max_records=10, max_bytes=exact_n - 1,
                                 max_record=cap_record, payload_max_json_bytes=32768,
                                 payload_max_ref_bytes=256, payload_max_observation_refs=16)
        limits_b, resource_b, _, _, _, _, _ = rebuilt_bytes
        self.assertLessEqual(cap_record + 58, resource_b.max_bytes)
        recipe_b = _recipe_for(limits_b, rebuilt_bytes[4], resource_b)
        plan_b = _plan_for(rebuilt_bytes, recipe_b)
        raw_bb = _b_payload_positive(rebuilt_bytes, plan_b)
        head_bb, nv_bb = _head_b_of(rebuilt_bytes, plan_b), _nv_b_of(rebuilt_bytes, plan_b)
        pg_bb, _, pg_nv_bb, _ = _pg_payload(rebuilt_bytes, 1, head_bb, nv_bb, "pg-1-qxqx")
        journal_bb = _journal([raw_bb, pg_bb])
        self.assertGreater(len(journal_bb), resource_b.max_bytes)
        with self.assertRaises(BootstrapHistoryScanError):
            scan_bootstrap_history(journal_bb, pg_nv_bb, **_kw(rebuilt_bytes, plan_b))


class BootstrapHistoryFactsTest(unittest.TestCase):
    def test_facts_bpg_runtime_malformed(self):
        closure = _closure(max_sequence=10, max_records=10, max_bytes=90000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        pg_raw, _, pg_nv, _ = _pg_payload(closure, 1, head_b, nv_b, "pg-1-qxqx")
        facts = scan_bootstrap_history(_journal([raw_b, pg_raw]), pg_nv, **_kw(closure, plan))
        self.assertIn("pg-1-qxqx", facts.pg_payloads[0].decode("utf-8"))
        self.assertNotIn("pg-1-qxqx", repr(facts))
        self.assertFalse(hasattr(facts, "__dict__"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            facts.record_count = 99
        with patch("pixs.pa_native.bootstrap_history.derive_bootstrap_initial_record",
                   side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                scan_bootstrap_history(_journal([raw_b, pg_raw]), pg_nv, **_kw(closure, plan))
        good_resource = resource
        bad_resource = dataclasses.replace(good_resource, max_bytes=90000)
        object.__setattr__(bad_resource, "payload_max_json_bytes", "x")
        with self.assertRaises(BootstrapHistoryScanError):
            scan_bootstrap_history(_journal([raw_b, pg_raw]), pg_nv,
                                   r0_limits=limits, producer_limits=limits, resource=bad_resource,
                                   plan=plan, prepublication_envelope=env, policy=policy,
                                   context=context, base=base)


class BootstrapHistoryAdditionalTest(unittest.TestCase):
    def test_pg_noncanon_unknown_utf8(self):
        closure = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=90000)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource)
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
        pg_raw, pg_head, pg_nv, _ = _pg_payload(closure, 1, head_b, nv_b, "pg-1-qxqx")
        facts = scan_bootstrap_history(_journal([raw_b, pg_raw]), pg_nv, **_kw(closure, plan))
        self.assertEqual(facts.record_count, 2)
        self.assertEqual(facts.expected_tail_nv_hex, pg_nv)
        with self.subTest(case="pg-noncanon-whitespace"):
            data = json.loads(pg_raw.decode("utf-8"))
            noncanon = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(", ", ": ")).encode("utf-8")
            self.assertNotEqual(noncanon, pg_raw)
            self.assertEqual(json.loads(noncanon.decode("utf-8")), json.loads(pg_raw.decode("utf-8")))
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, noncanon]), pg_nv, **_kw(closure, plan))
        with self.subTest(case="pg-type-inconnu"):
            data = dict(json.loads(pg_raw.decode("utf-8")))
            data["object_type"] = "pixs.agent.postgresql.journal_transition/v9"
            unknown = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, unknown]), pg_nv, **_kw(closure, plan))
        with self.subTest(case="pg-utf8-invalide"):
            bad = b"\xff\xfe\x00bad"
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, bad]), pg_nv, **_kw(closure, plan))

    def test_caps_json_record_ref(self):
        def _fat_bytes(encode_closure, prev_head, prev_nv, tref, refs, seq=1):
            limits_j = _journal_limits_for(encode_closure)
            item = JournalTransition(object_type="pixs.agent.postgresql.journal_transition/v1",
                                     schema_version="1.0.0", transition_ref=tref,
                                     installation_ref="inst", target_ref="tgt",
                                     registry_ref="reg", registry_generation_ref="gen",
                                     epoch=1, sequence=seq,
                                     previous_head_sha256=prev_head,
                                     previous_nv_value_sha256=prev_nv, state="OBSERVED",
                                     operation_ref="op-" + tref,
                                     mandate_binding=ContentBinding(ref="mand-" + tref, version="1.0.0", sha256="ab" * 32),
                                     content_binding=ContentBinding(ref="cont-" + tref, version="1.0.0", sha256="cd" * 32),
                                     correlation_refs=tuple(refs), causation_refs=())
            text = encode_journal_transition(item, limits_j).encode("utf-8")
            return (text, journal_transition_head_sha256(item, limits_j),
                    journal_expected_nv_sha256(item, limits_j))
        with self.subTest(case="ref-256-pass-puis-257-refuse-seul"):
            closure = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=90000)
            limits, resource, context, nv, base, policy, env = closure
            recipe = _recipe_for(limits, base, resource)
            plan = _plan_for(closure, recipe)
            raw_b = _b_payload_positive(closure, plan)
            head_b, nv_b = _head_b_of(closure, plan), _nv_b_of(closure, plan)
            ok_ref = "r" * 256
            item_ok = JournalTransition(object_type="pixs.agent.postgresql.journal_transition/v1",
                                        schema_version="1.0.0", transition_ref="pg-ref-qxqx",
                                        installation_ref="inst", target_ref="tgt", registry_ref="reg",
                                        registry_generation_ref="gen", epoch=1, sequence=1,
                                        previous_head_sha256=head_b, previous_nv_value_sha256=nv_b,
                                        state="OBSERVED", operation_ref="op-pg-ref-qxqx",
                                        mandate_binding=ContentBinding(ref=ok_ref, version="1.0.0", sha256="ab" * 32),
                                        content_binding=ContentBinding(ref="cont-pg-ref-qxqx", version="1.0.0", sha256="cd" * 32),
                                        correlation_refs=(), causation_refs=())
            limits_j = _journal_limits_for(closure)
            text_ok = encode_journal_transition(item_ok, limits_j).encode("utf-8")
            nv_ok = journal_expected_nv_sha256(item_ok, limits_j)
            facts_ok = scan_bootstrap_history(_journal([raw_b, text_ok]), nv_ok, **_kw(closure, plan))
            self.assertEqual(facts_ok.record_count, 2)
            big_ref = "r" * 257
            item_big = JournalTransition(object_type="pixs.agent.postgresql.journal_transition/v1",
                                         schema_version="1.0.0", transition_ref="pg-big-qxqx",
                                         installation_ref="inst", target_ref="tgt", registry_ref="reg",
                                         registry_generation_ref="gen", epoch=1, sequence=1,
                                         previous_head_sha256=head_b, previous_nv_value_sha256=nv_b,
                                         state="OBSERVED", operation_ref="op-pg-big-qxqx",
                                         mandate_binding=ContentBinding(ref=big_ref, version="1.0.0", sha256="ab" * 32),
                                         content_binding=ContentBinding(ref="cont-pg-big-qxqx", version="1.0.0", sha256="cd" * 32),
                                         correlation_refs=(), causation_refs=())
            wide_payload = PayloadLimits(max_json_bytes=32768, max_ref_bytes=512, max_observation_refs=16)
            wide_j = JournalLimits(payload=wide_payload, max_epoch=10, max_sequence=10,
                                   max_correlation_refs=4, max_causation_refs=4)
            text_big = encode_journal_transition(item_big, wide_j).encode("utf-8")
            nv_big = journal_expected_nv_sha256(item_big, wide_j)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b, text_big]), nv_big, **_kw(closure, plan))
        with self.subTest(case="fat-exact-puis-record-moins1"):
            refs = tuple("a" * 200 for _ in range(8))
            probe = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=200000,
                             max_correlation_refs=8, max_causation_refs=8)
            limits_p, _, _, _, _, _, _ = probe
            recipe_p = _recipe_for(limits_p, probe[4], probe[1])
            plan_p = _plan_for(probe, recipe_p)
            raw_bp = _b_payload_positive(probe, plan_p)
            head_p, nv_p = _head_b_of(probe, plan_p), _nv_b_of(probe, plan_p)
            fat_probe, _, _ = _fat_bytes(probe, head_p, nv_p, "pg-fat-qxqx", refs)
            self.assertGreater(len(fat_probe), len(raw_bp))
            cap = len(fat_probe)
            exact = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=200000,
                             max_record=cap, max_correlation_refs=8, max_causation_refs=8)
            limits_e, _, _, _, _, _, _ = exact
            recipe_e = _recipe_for(limits_e, exact[4], exact[1])
            plan_e = _plan_for(exact, recipe_e)
            raw_be = _b_payload_positive(exact, plan_e)
            self.assertLessEqual(len(raw_be), cap)
            head_e, nv_e = _head_b_of(exact, plan_e), _nv_b_of(exact, plan_e)
            fat_e, _, nv_fat_e = _fat_bytes(exact, head_e, nv_e, "pg-fat-qxqx", refs)
            self.assertEqual(len(fat_e), cap)
            facts_e = scan_bootstrap_history(_journal([raw_be, fat_e]), nv_fat_e, **_kw(exact, plan_e))
            self.assertEqual(facts_e.record_count, 2)
            neg = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=200000,
                           max_record=cap - 1, max_correlation_refs=8, max_causation_refs=8)
            limits_n, _, _, _, _, _, _ = neg
            recipe_n = _recipe_for(limits_n, neg[4], neg[1])
            plan_n = _plan_for(neg, recipe_n)
            raw_bn = _b_payload_positive(neg, plan_n)
            self.assertLessEqual(len(raw_bn), cap - 1)
            head_n, nv_n = _head_b_of(neg, plan_n), _nv_b_of(neg, plan_n)
            fat_n, _, nv_fat_n = _fat_bytes(exact, head_n, nv_n, "pg-fat-qxqx", refs)
            self.assertEqual(len(fat_n), cap)
            self.assertGreater(len(fat_n), neg[1].max_record)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_bn, fat_n]), nv_fat_n, **_kw(neg, plan_n))
        with self.subTest(case="json-exact-puis-moins1"):
            refs = tuple("b" * 200 for _ in range(8))
            probe = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=200000,
                             max_correlation_refs=8, max_causation_refs=8)
            limits_p, _, _, _, _, _, _ = probe
            recipe_p = _recipe_for(limits_p, probe[4], probe[1])
            plan_p = _plan_for(probe, recipe_p)
            raw_bp = _b_payload_positive(probe, plan_p)
            head_p, nv_p = _head_b_of(probe, plan_p), _nv_b_of(probe, plan_p)
            fat_probe, _, _ = _fat_bytes(probe, head_p, nv_p, "pg-fat2-qxqx", refs)
            cap = len(fat_probe)
            self.assertGreater(cap, len(raw_bp))
            exact = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=200000,
                             max_record=20000, max_correlation_refs=8, max_causation_refs=8,
                             payload_max_json_bytes=cap)
            limits_e, _, _, _, _, _, _ = exact
            recipe_e = _recipe_for(limits_e, exact[4], exact[1])
            plan_e = _plan_for(exact, recipe_e)
            raw_be = _b_payload_positive(exact, plan_e)
            self.assertLessEqual(len(raw_be), cap)
            head_e, nv_e = _head_b_of(exact, plan_e), _nv_b_of(exact, plan_e)
            fat_e, _, nv_fat_e = _fat_bytes(exact, head_e, nv_e, "pg-fat2-qxqx", refs)
            self.assertEqual(len(fat_e), cap)
            facts_e = scan_bootstrap_history(_journal([raw_be, fat_e]), nv_fat_e, **_kw(exact, plan_e))
            self.assertEqual(facts_e.record_count, 2)
            neg = _closure(max_epoch=10, max_sequence=10, max_records=10, max_bytes=200000,
                           max_record=20000, max_correlation_refs=8, max_causation_refs=8,
                           payload_max_json_bytes=cap - 1)
            limits_n, _, _, _, _, _, _ = neg
            recipe_n = _recipe_for(limits_n, neg[4], neg[1])
            plan_n = _plan_for(neg, recipe_n)
            raw_bn = _b_payload_positive(neg, plan_n)
            self.assertLessEqual(len(raw_bn), cap - 1)
            head_n, nv_n = _head_b_of(neg, plan_n), _nv_b_of(neg, plan_n)
            fat_n, _, nv_fat_n = _fat_bytes(exact, head_n, nv_n, "pg-fat2-qxqx", refs)
            self.assertEqual(len(fat_n), cap)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_bn, fat_n]), nv_fat_n, **_kw(neg, plan_n))

    def test_zero_caps_and_resource_malformed(self):
        closure = _closure(epoch=0, first_sequence=0, max_epoch=0, max_sequence=0,
                           max_bytes=60000, max_records=10)
        limits, resource, context, nv, base, policy, env = closure
        recipe = _recipe_for(limits, base, resource, epoch=0, sequence=0,
                             correlation_refs=(), causation_refs=())
        plan = _plan_for(closure, recipe)
        raw_b = _b_payload_positive(closure, plan)
        nv_b = _nv_b_of(closure, plan)
        facts = scan_bootstrap_history(_journal([raw_b]), nv_b, **_kw(closure, plan))
        self.assertEqual(facts.record_count, 1)
        self.assertEqual(facts.expected_tail_nv_hex, nv_b)
        with self.subTest(case="resource-bool-avant-parse"):
            good = dataclasses.replace(resource, max_bytes=60000)
            object.__setattr__(good, "max_bytes", True)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b]), nv_b, r0_limits=limits,
                                       producer_limits=limits, resource=good, plan=plan,
                                       prepublication_envelope=env, policy=policy,
                                       context=context, base=base)
        with self.subTest(case="resource-str-avant-parse"):
            good2 = dataclasses.replace(resource, max_bytes=60000)
            object.__setattr__(good2, "max_records", "x")
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(_journal([raw_b]), nv_b, r0_limits=limits,
                                       producer_limits=limits, resource=good2, plan=plan,
                                       prepublication_envelope=env, policy=policy,
                                       context=context, base=base)
        with self.subTest(case="provided-ancien-nv-refuse"):
            closure2 = _closure(max_sequence=10, max_records=10, max_bytes=90000)
            limits2, _, _, _, _, _, _ = closure2
            recipe2 = _recipe_for(limits2, closure2[4], closure2[1])
            plan2 = _plan_for(closure2, recipe2)
            raw_b2 = _b_payload_positive(closure2, plan2)
            head2, nv2 = _head_b_of(closure2, plan2), _nv_b_of(closure2, plan2)
            pg2, _, pg_nv2, _ = _pg_payload(closure2, 1, head2, nv2, "pg-1-qxqx")
            journal2 = _journal([raw_b2, pg2])
            self.assertNotEqual(nv2, pg_nv2)
            with self.assertRaises(BootstrapHistoryScanError):
                scan_bootstrap_history(journal2, nv2, **_kw(closure2, plan2))

if __name__ == "__main__":
    unittest.main()
