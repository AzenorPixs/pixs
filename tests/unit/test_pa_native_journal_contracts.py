"""Sources de tests du codec journal : aucune IO, autorité ou ancre réelle.

Les constantes de digest ont été préparées indépendamment par hashlib/json,
sans importer le produit. Elles ne sont pas des résultats de tests exécutés.
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib
import json
import unittest

from pixs.pa_native.postgresql_contracts import (
    ContentBinding, ContractError, JournalLimits, JournalTransition, PayloadLimits,
    decode_journal_transition, encode_journal_transition,
    journal_expected_nv_sha256, journal_transition_head_sha256,
)

HEAD = "546bba19ab4cbec3511bc890b4ada75b728e73f336f1c7e6ea3601e4929570df"
NEXT_NV = "7c8800ca72d77e86c67b20c294edd8fcd834f75a9040db5d8cb4e919a65a5c12"
PREFIX = b"PIXS:PA:POSTGRESQL:JOURNAL:1.0.0\n"


def limits(**changes):
    value = JournalLimits(PayloadLimits(4096, 128, 10), 9, 20, 4, 4)
    return replace(value, **changes) if changes else value


def transition(**changes):
    value = JournalTransition(
        "pixs.agent.postgresql.journal_transition/v1", "1.0.0", "transition-1",
        "installation-1", "target-1", "registry-1", "generation-1", 3, 7,
        "11" * 32, "22" * 32, "INTENT", "operation-1",
        ContentBinding("mandate-1", "1.0.0", "33" * 32),
        ContentBinding("content-1", "1.0.0", "44" * 32),
        ("c-2", "c-1", "c-2"), ("cause-2", "cause-1", "cause-2"))
    return replace(value, **changes) if changes else value


class JournalContractTest(unittest.TestCase):
    def test_roundtrip_preserves_immutable_binding_and_trace_types(self):
        value = transition()
        restored = decode_journal_transition(encode_journal_transition(value, limits()), limits())
        self.assertEqual(restored, value)
        self.assertIs(type(restored.mandate_binding), ContentBinding)
        self.assertIs(type(restored.correlation_refs), tuple)

    def test_independent_head_and_raw_nv_value_vector(self):
        value = transition()
        self.assertEqual(journal_transition_head_sha256(value, limits()), HEAD)
        self.assertEqual(journal_expected_nv_sha256(value, limits()), NEXT_NV)
        self.assertNotEqual(NEXT_NV, hashlib.sha256(
            value.previous_nv_value_sha256.encode() + HEAD.encode()).hexdigest())

    def test_canonical_encoding_has_exact_closed_fields_and_no_future_commitment(self):
        text = encode_journal_transition(transition(), limits())
        value = json.loads(text)
        self.assertEqual(set(value), {
            "object_type", "schema_version", "transition_ref", "installation_ref",
            "target_ref", "registry_ref", "registry_generation_ref", "epoch",
            "sequence", "previous_head_sha256", "previous_nv_value_sha256", "state",
            "operation_ref", "mandate_binding", "content_binding",
            "correlation_refs", "causation_refs"})
        self.assertEqual(text, json.dumps(value, sort_keys=True,
                                         separators=(",", ":"), ensure_ascii=False))
        self.assertEqual(hashlib.sha256(PREFIX + text.encode("utf-8")).hexdigest(), HEAD)

    def test_arrays_keep_their_order_and_duplicates(self):
        value = transition()
        encoded = json.loads(encode_journal_transition(value, limits()))
        self.assertEqual(encoded["correlation_refs"], ["c-2", "c-1", "c-2"])
        self.assertEqual(encoded["causation_refs"], ["cause-2", "cause-1", "cause-2"])
        reordered = replace(value, correlation_refs=("c-1", "c-2", "c-2"))
        self.assertNotEqual(journal_transition_head_sha256(reordered, limits()), HEAD)

    def test_all_declared_states_roundtrip_as_data_only(self):
        for state in ("INTENT", "OBSERVED", "RESULT", "RETIRED"):
            with self.subTest(state=state):
                value = transition(state=state)
                self.assertEqual(decode_journal_transition(
                    encode_journal_transition(value, limits()), limits()), value)
                self.assertFalse(hasattr(value, "verified"))
                self.assertFalse(hasattr(value, "intent_durable"))

    def test_unknown_schema_object_and_state_are_refused_at_construction(self):
        for changes in ({"object_type": "other"}, {"schema_version": "2.0.0"},
                        {"state": "SUCCEEDED"}, {"state": True}):
            with self.subTest(changes=changes):
                with self.assertRaises(ContractError):
                    transition(**changes)

    def test_zero_and_uint64_boundary_are_explicit_not_defaults(self):
        zero = transition(epoch=0, sequence=0)
        zero_limits = limits(max_epoch=0, max_sequence=0)
        self.assertEqual(decode_journal_transition(
            encode_journal_transition(zero, zero_limits), zero_limits), zero)
        maximum = 2 ** 64 - 1
        value = transition(epoch=maximum, sequence=maximum)
        large = limits(max_epoch=maximum, max_sequence=maximum)
        self.assertEqual(decode_journal_transition(
            encode_journal_transition(value, large), large), value)

    def test_numbers_reject_bool_float_negative_and_overflow(self):
        for field in ("epoch", "sequence"):
            for invalid in (True, False, 1.0, -1, 2 ** 64, "3", None):
                with self.subTest(field=field, invalid=invalid):
                    with self.assertRaises(ContractError):
                        transition(**{field: invalid})

    def test_each_number_has_its_own_profile_cap(self):
        value = transition(epoch=9, sequence=7)
        with self.assertRaises(ContractError):
            encode_journal_transition(value, limits(max_epoch=8, max_sequence=20))
        with self.assertRaises(ContractError):
            decode_journal_transition(
                encode_journal_transition(value, limits()),
                limits(max_epoch=20, max_sequence=6))

    def test_limits_require_exact_types_bounds_and_positive_trace_caps(self):
        value = limits()
        for field, invalid in (("payload", None), ("max_epoch", True),
                               ("max_epoch", -1), ("max_sequence", 2 ** 64),
                               ("max_sequence", 1.0), ("max_correlation_refs", 0),
                               ("max_causation_refs", False)):
            with self.subTest(field=field):
                with self.assertRaises(ContractError):
                    replace(value, **{field: invalid})

    def test_references_reject_controls_empty_wrong_type_and_invalid_utf8(self):
        for field in ("transition_ref", "installation_ref", "target_ref", "registry_ref",
                      "registry_generation_ref", "operation_ref"):
            for invalid in ("", "a\x00b", "a\x7fb", "\ud800", 1, None):
                with self.subTest(field=field, kind=type(invalid).__name__):
                    with self.assertRaises(ContractError):
                        transition(**{field: invalid})

    def test_valid_utf8_is_encoded_without_ascii_escape_substitution(self):
        value = transition(target_ref="cible-é")
        text = encode_journal_transition(value, limits())
        self.assertIn("cible-é", text)
        self.assertEqual(decode_journal_transition(text, limits()), value)
        self.assertEqual(journal_transition_head_sha256(value, limits()),
                         hashlib.sha256(PREFIX + text.encode("utf-8")).hexdigest())

    def test_reference_byte_budget_counts_utf8_bytes_and_covers_bindings(self):
        value = transition(target_ref="é" * 65)
        with self.assertRaises(ContractError):
            encode_journal_transition(value, limits())
        value = transition(content_binding=ContentBinding("r", "v" * 129, "44" * 32))
        with self.assertRaises(ContractError):
            encode_journal_transition(value, limits())

    def test_digest_format_is_strict_in_previous_values_and_bindings(self):
        for field in ("previous_head_sha256", "previous_nv_value_sha256"):
            for invalid in ("A" * 64, "00" * 31, "g" * 64, 0):
                with self.subTest(field=field):
                    with self.assertRaises(ContractError):
                        transition(**{field: invalid})
        with self.assertRaises(ContractError):
            transition(mandate_binding={"ref": "r", "version": "1", "sha256": "33" * 32})

    def test_trace_types_elements_and_individual_caps_are_strict(self):
        for changes in ({"correlation_refs": ["c"]}, {"causation_refs": ("",)},
                        {"correlation_refs": (True,)}, {"causation_refs": (1,)}):
            with self.assertRaises(ContractError):
                transition(**changes)
        value = transition()
        with self.assertRaises(ContractError):
            encode_journal_transition(value, limits(max_correlation_refs=2))
        with self.assertRaises(ContractError):
            encode_journal_transition(value, limits(max_causation_refs=2))

    def test_json_missing_extra_and_nested_extra_fields_are_refused(self):
        base = json.loads(encode_journal_transition(transition(), limits()))
        missing = dict(base)
        missing.pop("operation_ref")
        extra = dict(base, unexpected="public-fixture")
        nested = json.loads(json.dumps(base))
        nested["content_binding"]["unexpected"] = "public-fixture"
        for value in (missing, extra, nested):
            with self.assertRaises(ContractError):
                decode_journal_transition(json.dumps(value), limits())

    def test_duplicate_keys_at_root_and_binding_are_refused(self):
        text = encode_journal_transition(transition(), limits())
        duplicate_root = '{"state":"RESULT",' + text[1:]
        duplicate_binding = text.replace('"ref":"content-1"',
                                        '"ref":"content-1","ref":"other"', 1)
        for value in (duplicate_root, duplicate_binding):
            with self.assertRaises(ContractError):
                decode_journal_transition(value, limits())

    def test_json_noninteger_constants_coercions_and_negative_tokens_are_refused(self):
        text = encode_journal_transition(transition(), limits())
        for replacement in ("3.0", "3e0", "NaN", "Infinity", "-Infinity", "-1", "-0",
                            '"3"', "true", "null"):
            with self.subTest(replacement=replacement):
                with self.assertRaises(ContractError):
                    decode_journal_transition(text.replace('"epoch":3',
                                                          '"epoch":' + replacement, 1), limits())

    def test_json_object_arrays_and_binding_shapes_are_checked(self):
        base = json.loads(encode_journal_transition(transition(), limits()))
        for value in ([], True, "text", 1):
            with self.assertRaises(ContractError):
                decode_journal_transition(json.dumps(value), limits())
        for field, value in (("causation_refs", {}), ("content_binding", [])):
            invalid = dict(base)
            invalid[field] = value
            with self.assertRaises(ContractError):
                decode_journal_transition(json.dumps(invalid), limits())

    def test_payload_utf8_and_size_limits_are_checked_before_parsing(self):
        text = encode_journal_transition(transition(), limits())
        tiny = limits(payload=PayloadLimits(10, 128, 10))
        for action in (lambda: encode_journal_transition(transition(), tiny),
                       lambda: decode_journal_transition(text, tiny),
                       lambda: decode_journal_transition("\ud800", limits())):
            with self.assertRaises(ContractError):
                action()

    def test_excessive_json_recursion_is_reported_as_contract_error(self):
        text = "[" * 1500 + "]" * 1500
        with self.assertRaises(ContractError):
            decode_journal_transition(text, limits())

    def test_new_objects_are_frozen_and_repr_does_not_reveal_content(self):
        value = transition()
        with self.assertRaises(FrozenInstanceError):
            value.state = "RESULT"
        self.assertNotIn(value.transition_ref, repr(value))
        with self.assertRaises(FrozenInstanceError):
            limits().max_epoch = 10

    def test_changes_to_all_contextual_commitments_change_the_head(self):
        for changes in ({"installation_ref": "installation-2"},
                        {"target_ref": "target-2"}, {"registry_ref": "registry-2"},
                        {"registry_generation_ref": "generation-2"},
                        {"epoch": 4}, {"sequence": 8},
                        {"previous_head_sha256": "55" * 32},
                        {"previous_nv_value_sha256": "66" * 32},
                        {"state": "RESULT"}, {"operation_ref": "operation-2"},
                        {"mandate_binding": ContentBinding("m2", "1.0.0", "33" * 32)},
                        {"content_binding": ContentBinding("c2", "1.0.0", "44" * 32)}):
            with self.subTest(fields=tuple(changes)):
                self.assertNotEqual(journal_transition_head_sha256(
                    transition(**changes), limits()), HEAD)

    def test_wrong_top_level_inputs_and_limits_never_coerce(self):
        for action in (lambda: encode_journal_transition({}, limits()),
                       lambda: encode_journal_transition(transition(), None),
                       lambda: decode_journal_transition(b"{}", limits()),
                       lambda: decode_journal_transition("{}", None),
                       lambda: journal_transition_head_sha256(transition(), None),
                       lambda: journal_expected_nv_sha256(transition(), None)):
            with self.assertRaises(ContractError):
                action()


if __name__ == "__main__":
    unittest.main()
