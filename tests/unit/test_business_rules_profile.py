"""Tests tâche2 : parseur et validateurs structuraux v1, sans moteur."""

from __future__ import annotations

import hashlib
import sys
import unittest
from dataclasses import FrozenInstanceError

from pixs.business_rules import (
    JsonContractError,
    ProfileError,
    RuleDefinition,
    decode_json_document,
    encode_json_document,
    normalize_python_value,
    parse_rule_document,
    validate_inputs,
)


def _base_schema():
    return {
        "age": {"type": "integer", "required": True},
        "name": {"type": "string", "required": False},
        "tags": {"type": "array", "required": False},
        "flag": {"type": "boolean", "required": False},
        "nick": {"type": "null", "required": False},
    }


def _base_rule_dict(expression=None, cases=None, schema=None):
    sch = schema if schema is not None else _base_schema()
    expr = expression if expression is not None else {"op": "eq", "args": [{"field": "age"}, {"literal": 3}]}
    cas = cases if cases is not None else [{"case_id": "c1", "inputs": {"age": 3}, "expected": True}]
    return {
        "profile_version": 1,
        "rule_id": "r1",
        "rule_version": "v1",
        "owner": "o1",
        "input_schema": sch,
        "expression": expr,
        "cases": cas,
    }


def _rule_bytes(expression=None, cases=None, schema=None):
    return encode_json_document(_base_rule_dict(expression, cases, schema))


def _assert_refusal(callable_obj):
    try:
        callable_obj()
    except (JsonContractError, ProfileError) as error:
        return error
    raise AssertionError("REFUS_ATTENDU")


class CodecTypesTest(unittest.TestCase):
    def test_all_scalar_types_roundtrip(self):
        for value in (None, True, False, 0, 42, "", "cafe", [], [None, True, 1, "x", [2]]):
            data = encode_json_document(value)
            self.assertEqual(decode_json_document(data), value)

    def test_bool_distinct_from_int(self):
        self.assertIs(decode_json_document(b"true"), True)
        self.assertEqual(decode_json_document(b"1"), 1)
        self.assertIs(type(decode_json_document(b"true")), bool)
        self.assertIs(type(decode_json_document(b"1")), int)

    def test_valid_unicode_accepted(self):
        self.assertEqual(decode_json_document('"caf\\u00e9"'.encode("utf-8")), "café")

    def test_surrogate_escaped_refused(self):
        error = _assert_refusal(lambda: decode_json_document(b'{"a": "\\ud800"}'))
        self.assertNotIn("ud800", str(error))

    def test_float_refused(self):
        for raw in (b"1.5", b'{"a": 1.5}', b"[1.5]"):
            _assert_refusal(lambda raw=raw: decode_json_document(raw))

    def test_non_finite_refused(self):
        for raw in (b"NaN", b"Infinity", b"-Infinity"):
            _assert_refusal(lambda raw=raw: decode_json_document(raw))

    def test_duplicate_keys_refused(self):
        error = _assert_refusal(lambda: decode_json_document(b'{"a": 1, "a": 2}'))
        self.assertEqual(error.code, "JSON_DUPLICATE_KEY")

    def test_unknown_python_types_refused(self):
        for bad in ((1, 2), {1, 2}, 1.5, b"x"):
            _assert_refusal(lambda bad=bad: normalize_python_value(bad))

    def test_dict_with_float_value_refused(self):
        _assert_refusal(lambda: normalize_python_value({"a": 1.5}))

    def test_cycle_refused(self):
        loop = []
        loop.append(loop)
        error = _assert_refusal(lambda: normalize_python_value(loop))
        self.assertEqual(error.code, "JSON_CYCLIC")

    def test_shared_alias_accepted_and_counted(self):
        shared = [1]
        root = [shared, shared]
        snapshot = normalize_python_value(root)
        self.assertEqual(snapshot, [[1], [1]])
        snapshot[0].append(99)
        self.assertEqual(snapshot[1], [1])
        self.assertEqual(root, [[1], [1]])

    def test_direct_mutation_protected(self):
        original = {"a": [1]}
        snapshot = normalize_python_value(original)
        original["a"].append(2)
        original["b"] = 3
        self.assertEqual(snapshot, {"a": [1]})

    def test_refusal_without_echo(self):
        marker = "INERT-ALPHA-DO-NOT-ECHO"
        raw = ('{"a":"' + marker + '","a":2}').encode("utf-8")
        error = _assert_refusal(lambda: decode_json_document(raw))
        self.assertNotIn(marker, str(error))
        self.assertNotIn(marker, repr(error))
        self.assertNotIn(marker, error.code)
        error2 = _assert_refusal(lambda: normalize_python_value({marker: object()}))
        self.assertNotIn(marker, str(error2))


class CodecBoundsTest(unittest.TestCase):
    def test_size_exactly_65536_accepted(self):
        pad = "x" * (65536 - 9)
        data = ('{"k": "' + pad + '"}').encode("utf-8")
        self.assertEqual(len(data), 65536)
        self.assertEqual(decode_json_document(data)["k"], pad)

    def test_size_65537_refused(self):
        pad = "x" * (65537 - 9)
        data = ('{"k": "' + pad + '"}').encode("utf-8")
        self.assertEqual(len(data), 65537)
        _assert_refusal(lambda: decode_json_document(data))

    def test_total_size_direct_normalization_refused(self):
        big = {"a": "x" * 40000, "b": "y" * 30000}
        _assert_refusal(lambda: normalize_python_value(big))

    def test_large_key_names_counted_in_size(self):
        big_key = "k" * 70000
        _assert_refusal(lambda: normalize_python_value({big_key: 1}))

    def test_depth_8_accepted_9_refused(self):
        deep = 1
        for _ in range(8):
            deep = [deep]
        encode_json_document(deep)
        deeper = 1
        for _ in range(9):
            deeper = [deeper]
        _assert_refusal(lambda: normalize_python_value(deeper))
        text = b"[" * 9 + b"1" + b"]" * 9
        _assert_refusal(lambda: decode_json_document(text))

    def test_nodes_256_accepted_257_refused(self):
        ok = list(range(255))
        self.assertEqual(len(encode_json_document(ok)) > 0, True)
        too_many = list(range(256))
        _assert_refusal(lambda: normalize_python_value(too_many))

    def test_6000_digit_int_accepted_and_reencoded(self):
        before = sys.get_int_max_str_digits()
        data = b'{"n":' + b'9' * 6000 + b'}'
        value = decode_json_document(data)
        self.assertTrue(value["n"] == 10 ** 6000 - 1)
        self.assertEqual(encode_json_document(value), data)
        self.assertEqual(sys.get_int_max_str_digits(), before)

    def test_canonical_sorting(self):
        data = encode_json_document({"b": 1, "a": 2})
        self.assertEqual(data, b'{"a":2,"b":1}')


class ProfileStructureTest(unittest.TestCase):
    def test_valid_rule_parses_and_digest(self):
        rule = parse_rule_document(_rule_bytes())
        self.assertEqual(rule.profile_version, 1)
        self.assertEqual(rule.rule_id, "r1")
        self.assertEqual(hashlib.sha256(rule.canonical).hexdigest(), rule.digest)

    def test_all_operators_structurally_valid(self):
        expressions = [
            {"op": "all", "args": [{"op": "eq", "args": [{"field": "age"}, {"literal": 1}]}, {"op": "eq", "args": [{"field": "age"}, {"literal": 1}]}]},
            {"op": "any", "args": [{"op": "eq", "args": [{"field": "age"}, {"literal": 1}]}]},
            {"op": "not", "args": {"op": "eq", "args": [{"field": "age"}, {"literal": 1}]}},
            {"op": "eq", "args": [{"field": "age"}, {"literal": 2}]},
            {"op": "ne", "args": [{"field": "name"}, {"literal": "x"}]},
            {"op": "lt", "args": [{"field": "age"}, {"literal": 5}]},
            {"op": "lte", "args": [{"field": "age"}, {"literal": 5}]},
            {"op": "gt", "args": [{"field": "age"}, {"literal": 5}]},
            {"op": "gte", "args": [{"field": "age"}, {"literal": 5}]},
            {"op": "in", "args": [{"field": "age"}, {"literal": [1, 2]}]},
            {"op": "exists", "args": {"field": "name"}},
        ]
        for expression in expressions:
            with self.subTest(op=expression["op"]):
                parse_rule_document(_rule_bytes(expression=expression))

    def test_unknown_operator_refused(self):
        bad = {"op": "xor", "args": []}
        _assert_refusal(lambda: parse_rule_document(_rule_bytes(expression=bad)))

    def test_unknown_top_field_refused(self):
        base = _base_rule_dict()
        base["extra"] = 1
        _assert_refusal(lambda: parse_rule_document(encode_json_document(base)))

    def test_duplicate_top_keys_refused(self):
        raw = b'{"profile_version": 1, "profile_version": 1, "rule_id": "r1", "rule_version": "v1", "owner": "o1", "input_schema": {}, "expression": {"op": "all", "args": []}, "cases": [{"case_id": "c1", "inputs": {}, "expected": true}]}'
        _assert_refusal(lambda: parse_rule_document(raw))

    def test_arity_errors_refused(self):
        cases = [
            {"op": "all", "args": []},
            {"op": "not", "args": [{"op": "eq", "args": [{"field": "age"}, {"literal": 1}]}]},
            {"op": "exists", "args": [{"field": "name"}]},
            {"op": "exists", "args": {"literal": 1}},
            {"op": "eq", "args": [{"field": "age"}]},
            {"op": "in", "args": [{"field": "age"}, {"literal": 1}]},
        ]
        for expression in cases:
            with self.subTest(expression=expression):
                _assert_refusal(lambda expression=expression: parse_rule_document(_rule_bytes(expression=expression)))

    def test_undeclared_field_refused(self):
        bad = {"op": "eq", "args": [{"field": "nope"}, {"literal": 1}]}
        _assert_refusal(lambda: parse_rule_document(_rule_bytes(expression=bad)))

    def test_comparison_bool_not_int(self):
        bad = {"op": "eq", "args": [{"literal": True}, {"literal": 1}]}
        _assert_refusal(lambda: parse_rule_document(_rule_bytes(expression=bad)))

    def test_ordering_mixed_types_refused(self):
        bad = {"op": "lt", "args": [{"literal": 1}, {"literal": "x"}]}
        _assert_refusal(lambda: parse_rule_document(_rule_bytes(expression=bad)))

    def test_version_and_corpus_rules(self):
        base = _base_rule_dict()
        base["profile_version"] = 2
        _assert_refusal(lambda: parse_rule_document(encode_json_document(base)))
        base2 = _base_rule_dict(cases=[])
        _assert_refusal(lambda: parse_rule_document(encode_json_document(base2)))
        dup = [
            {"case_id": "c1", "inputs": {"age": 1}, "expected": True},
            {"case_id": "c1", "inputs": {"age": 2}, "expected": False},
        ]
        _assert_refusal(lambda: parse_rule_document(encode_json_document(_base_rule_dict(cases=dup))))
        bad_expected = [{"case_id": "c1", "inputs": {"age": 1}, "expected": 1}]
        _assert_refusal(lambda: parse_rule_document(encode_json_document(_base_rule_dict(cases=bad_expected))))

    def test_cases_not_executed(self):
        expression = {"op": "eq", "args": [{"field": "age"}, {"literal": 1}]}
        cases = [{"case_id": "c1", "inputs": {"age": 1}, "expected": False}]
        rule = parse_rule_document(_rule_bytes(expression=expression, cases=cases))
        self.assertEqual(rule.cases()[0]["expected"], False)

    def test_direct_construction_mismatch_refused(self):
        rule = parse_rule_document(_rule_bytes())
        _assert_refusal(lambda: RuleDefinition(1, "WRONG", rule.rule_version, rule.owner, rule.digest, rule.canonical))
        _assert_refusal(lambda: RuleDefinition(1, rule.rule_id, rule.rule_version, rule.owner, "0" * 64, rule.canonical))
        pretty = b" " + rule.canonical + b" "
        _assert_refusal(lambda: RuleDefinition(1, rule.rule_id, rule.rule_version, rule.owner, hashlib.sha256(pretty).hexdigest(), pretty))

    def test_projections_are_defensive_and_frozen(self):
        rule = parse_rule_document(_rule_bytes())
        first = rule.document()
        first["rule_id"] = "MUT"
        first["input_schema"]["age"] = {"type": "string", "required": True}
        self.assertEqual(rule.rule_id, "r1")
        self.assertEqual(rule.document()["rule_id"], "r1")
        with self.assertRaises(FrozenInstanceError):
            rule.rule_id = "MUT"


class ProfileInputsTest(unittest.TestCase):
    def setUp(self):
        self.rule = parse_rule_document(_rule_bytes())

    def test_required_present_and_optional_absent_ok(self):
        result = validate_inputs(self.rule, encode_json_document({"age": 4}))
        self.assertEqual(result, {"age": 4})

    def test_optional_present_must_match(self):
        result = validate_inputs(self.rule, encode_json_document({"age": 4, "name": "ab"}))
        self.assertEqual(result["name"], "ab")

    def test_missing_required_refused(self):
        _assert_refusal(lambda: validate_inputs(self.rule, encode_json_document({})))

    def test_unknown_field_refused(self):
        _assert_refusal(lambda: validate_inputs(self.rule, encode_json_document({"age": 1, "nope": 2})))

    def test_type_mismatch_bool_int_refused(self):
        _assert_refusal(lambda: validate_inputs(self.rule, encode_json_document({"age": True})))
        _assert_refusal(lambda: validate_inputs(self.rule, encode_json_document({"age": "1"})))

    def test_array_elements_must_be_literals(self):
        _assert_refusal(lambda: validate_inputs(self.rule, encode_json_document({"age": 1, "tags": [{"a": 1}]})))

    def test_case_inputs_conform_checked_at_parse(self):
        bad_cases = [{"case_id": "c1", "inputs": {}, "expected": True}]
        _assert_refusal(lambda: parse_rule_document(encode_json_document(_base_rule_dict(cases=bad_cases))))


class AdditionalContractEdgesTest(unittest.TestCase):
    def test_invalid_utf8_and_surrogates_on_all_paths(self):
        with self.assertRaises(JsonContractError):
            decode_json_document(bytes([255]))
        with self.assertRaises(ProfileError):
            parse_rule_document(bytes([255]))
        bad = chr(0xD800)
        for value in (bad, {bad: 1}, {"x": bad}):
            with self.subTest(kind=type(value).__name__):
                with self.assertRaises(JsonContractError):
                    normalize_python_value(value)
                with self.assertRaises(JsonContractError):
                    encode_json_document(value)
        with self.assertRaises(JsonContractError):
            decode_json_document(b'{"' + bytes([92]) + b'ud800":1}')

    def test_keys_do_not_count_as_nodes_and_decoder_checks_nodes(self):
        valid = {"k" + str(i): None for i in range(255)}
        raw = encode_json_document(valid)
        self.assertEqual(decode_json_document(raw), valid)
        invalid = b'[' + b','.join([b'0'] * 256) + b']'
        with self.assertRaises(JsonContractError):
            decode_json_document(invalid)

    def test_codec_depth_boundary_through_decoder(self):
        valid = b'[' * 8 + b'0' + b']' * 8
        self.assertEqual(encode_json_document(decode_json_document(valid)), valid)
        with self.assertRaises(JsonContractError):
            decode_json_document(b'[' * 9 + b'0' + b']' * 9)

    def test_profile_byte_boundary_and_wrapped_rejections(self):
        raw = _rule_bytes()
        padded = raw + b' ' * (65536 - len(raw))
        self.assertEqual(parse_rule_document(padded), parse_rule_document(raw))
        with self.assertRaises(ProfileError):
            parse_rule_document(padded + b' ')

    def test_unhashable_operator_and_schema_types_are_typed_refusals(self):
        for bad in ([], {}, True, 1, ""):
            rule = _base_rule_dict()
            rule["expression"]["op"] = bad
            with self.subTest(part="operator", kind=type(bad).__name__):
                with self.assertRaises(ProfileError):
                    parse_rule_document(encode_json_document(rule))
            rule = _base_rule_dict()
            rule["input_schema"]["age"]["type"] = bad
            with self.subTest(part="schema", kind=type(bad).__name__):
                with self.assertRaises(ProfileError):
                    parse_rule_document(encode_json_document(rule))

    def test_closed_descriptors_and_case_shapes(self):
        descriptor_variants = (
            {"type": "integer"},
            {"type": "integer", "required": 1},
            {"type": "integer", "required": True, "extra": True},
        )
        for descriptor in descriptor_variants:
            rule = _base_rule_dict()
            rule["input_schema"]["age"] = descriptor
            with self.assertRaises(ProfileError):
                parse_rule_document(encode_json_document(rule))
        for key in ("case_id", "inputs", "expected"):
            rule = _base_rule_dict()
            del rule["cases"][0][key]
            with self.subTest(missing=key):
                with self.assertRaises(ProfileError):
                    parse_rule_document(encode_json_document(rule))
        rule = _base_rule_dict()
        rule["cases"][0]["extra"] = "INERT"
        with self.assertRaises(ProfileError):
            parse_rule_document(encode_json_document(rule))

    def test_boolean_profile_version_is_not_integer_one(self):
        rule = _base_rule_dict()
        rule["profile_version"] = True
        with self.assertRaises(ProfileError):
            parse_rule_document(encode_json_document(rule))

    def test_profile_with_long_integer_literals(self):
        expression = {"op": "eq", "args": [{"literal": 0}, {"literal": 0}]}
        cases = [{"case_id": "big", "inputs": {}, "expected": True}]
        raw = _rule_bytes(expression=expression, cases=cases, schema={})
        raw = raw.replace(b'{"literal":0}', b'{"literal":' + b'9' * 6000 + b'}')
        before = sys.get_int_max_str_digits()
        rule = parse_rule_document(raw)
        self.assertIn(b'9' * 6000, rule.canonical)
        self.assertEqual(sys.get_int_max_str_digits(), before)

    def test_profile_refusal_contains_no_supplied_marker(self):
        marker = "INERT-BETA-DO-NOT-ECHO"
        rule = _base_rule_dict()
        rule["extra"] = marker
        with self.assertRaises(ProfileError) as captured:
            parse_rule_document(encode_json_document(rule))
        self.assertNotIn(marker, str(captured.exception))
        self.assertNotIn(marker, repr(captured.exception))
        self.assertNotIn(marker, captured.exception.code)

    def test_definition_projections_and_repr_keep_internal_data_private(self):
        marker = "INERT-GAMMA-DO-NOT-ECHO"
        rule_data = _base_rule_dict(
            expression={"op": "eq", "args": [{"literal": marker}, {"literal": marker}]}
        )
        rule = parse_rule_document(encode_json_document(rule_data))
        schema = rule.input_schema()
        schema.clear()
        expression = rule.expression()
        expression["args"][0]["literal"] = "changed"
        cases = rule.cases()
        cases.clear()
        self.assertEqual(len(rule.input_schema()), 5)
        self.assertEqual(rule.expression()["args"][0]["literal"], marker)
        self.assertEqual(len(rule.cases()), 1)
        self.assertNotIn(marker, repr(rule))


if __name__ == "__main__":
    unittest.main()
