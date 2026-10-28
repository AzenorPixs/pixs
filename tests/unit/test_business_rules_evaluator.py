"""Tests du moteur borne et du catalogue, corpus embarque uniquement."""

import random
import socket
import time
import unittest
from unittest.mock import patch

from pixs.business_rules.evaluator import (
    CatalogError,
    EvaluatorError,
    RuleCatalog,
    evaluate,
)
from pixs.business_rules.json_contract import (
    JsonContractError,
    MAX_DEPTH,
    MAX_DOCUMENT_BYTES,
    MAX_NODES,
    encode_json_document,
)
from pixs.business_rules.profile import (
    ProfileError,
    RuleDefinition,
    parse_rule_document,
)


def _fields(**kinds: str) -> dict:
    return {name: {"type": kind, "required": False} for name, kind in kinds.items()}


def _doc(expression: dict, schema: dict, cases: list, owner="o-a",
         rule_id="r-a", rule_version="v1") -> dict:
    return {
        "profile_version": 1,
        "owner": owner,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "input_schema": schema,
        "expression": expression,
        "cases": [dict(case, case_id="case-" + str(i))
                  for i, case in enumerate(cases or [{"inputs": {}, "expected": False}])],
    }


def _rule(expression: dict, schema: dict, cases: list | None = None,
          owner="o-a", rule_id="r-a", rule_version="v1") -> RuleDefinition:
    doc = _doc(expression, schema, [] if cases is None else cases,
               owner, rule_id, rule_version)
    return parse_rule_document(encode_json_document(doc))


def _run(expression: dict, schema: dict, inputs: object,
         correlation_id: str = "corr-1") -> dict:
    rule = _rule(expression, schema)
    return evaluate(rule, encode_json_document(inputs), correlation_id)


def _expr(op: str, args: object) -> dict:
    return {"op": op, "args": args}


def _f(name: str) -> dict:
    return {"field": name}


def _lit(value: object) -> dict:
    return {"literal": value}


class OperatorCoverageTest(unittest.TestCase):
    def test_all_true(self):
        out = _run(_expr("all", [_expr("eq", [_f("a"), _lit(1)]),
                                     _expr("eq", [_f("b"), _lit("x")])]),
                   _fields(a="integer", b="string"), {"a": 1, "b": "x"})
        self.assertTrue(out["matched"])

    def test_all_false(self):
        out = _run(_expr("all", [_expr("eq", [_f("a"), _lit(1)]),
                                     _expr("eq", [_f("b"), _lit("y")])]),
                   _fields(a="integer", b="string"), {"a": 1, "b": "x"})
        self.assertFalse(out["matched"])

    def test_any_true(self):
        out = _run(_expr("any", [_expr("eq", [_f("a"), _lit(9)]),
                                     _expr("eq", [_f("b"), _lit("x")])]),
                   _fields(a="integer", b="string"), {"a": 1, "b": "x"})
        self.assertTrue(out["matched"])

    def test_any_false(self):
        out = _run(_expr("any", [_expr("eq", [_f("a"), _lit(9)]),
                                     _expr("eq", [_f("b"), _lit("y")])]),
                   _fields(a="integer", b="string"), {"a": 1, "b": "x"})
        self.assertFalse(out["matched"])

    def test_not_object_expression(self):
        out = _run(_expr("not", _expr("eq", [_f("a"), _lit(1)])),
                   _fields(a="integer"), {"a": 2})
        self.assertTrue(out["matched"])
        with self.assertRaises(ProfileError):
            _run(_expr("not", [_expr("eq", [_f("a"), _lit(1)])]),
                 _fields(a="integer"), {"a": 2})

    def test_eq_ne(self):
        self.assertTrue(_run(_expr("eq", [_f("a"), _lit(1)]),
                             _fields(a="integer"), {"a": 1})["matched"])
        self.assertTrue(_run(_expr("ne", [_f("a"), _lit(1)]),
                             _fields(a="integer"), {"a": 2})["matched"])

    def test_lt_lte_gt_gte(self):
        self.assertTrue(_run(_expr("lt", [_f("a"), _lit(2)]),
                             _fields(a="integer"), {"a": 1})["matched"])
        self.assertTrue(_run(_expr("lte", [_f("a"), _lit(1)]),
                             _fields(a="integer"), {"a": 1})["matched"])
        self.assertTrue(_run(_expr("gt", [_f("a"), _lit(1)]),
                             _fields(a="integer"), {"a": 2})["matched"])
        self.assertTrue(_run(_expr("gte", [_f("a"), _lit(2)]),
                             _fields(a="integer"), {"a": 2})["matched"])
        self.assertTrue(_run(_expr("lt", [_f("s"), _lit("b")]),
                             _fields(s="string"), {"s": "a"})["matched"])

    def test_in_membership(self):
        out = _run(_expr("in", [_f("a"), _lit([1, 2, 3])]),
                   _fields(a="integer"), {"a": 2})
        self.assertTrue(out["matched"])
        out = _run(_expr("in", [_f("a"), _lit([1, 2, 3])]),
                   _fields(a="integer"), {"a": 9})
        self.assertFalse(out["matched"])

    def test_exists_field_object(self):
        self.assertTrue(_run(_expr("exists", _f("opt")),
                             _fields(opt="integer"), {"opt": 1})["matched"])
        self.assertFalse(_run(_expr("exists", _f("opt")),
                              _fields(opt="integer"), {})["matched"])
        with self.assertRaises(ProfileError):
            _run(_expr("exists", {"literal": 1}),
                 _fields(opt="integer"), {"opt": 1})


class ShortCircuitTest(unittest.TestCase):
    def test_all_short_circuits_before_missing(self):
        expr = _expr("all", [_expr("eq", [_lit(1), _lit(2)]),
                             _expr("eq", [_f("missing"), _lit(1)])])
        out = _run(expr, _fields(missing="integer"), {})
        self.assertFalse(out["matched"])

    def test_all_consumed_missing_refuses(self):
        expr = _expr("all", [_expr("eq", [_f("missing"), _lit(1)]),
                             _expr("eq", [_lit(1), _lit(2)])])
        with self.assertRaises(EvaluatorError):
            _run(expr, _fields(missing="integer"), {})

    def test_any_short_circuits_before_missing(self):
        expr = _expr("any", [_expr("eq", [_lit(1), _lit(1)]),
                             _expr("eq", [_f("missing"), _lit(1)])])
        out = _run(expr, _fields(missing="integer"), {})
        self.assertTrue(out["matched"])

    def test_any_consumed_missing_refuses(self):
        expr = _expr("any", [_expr("eq", [_f("missing"), _lit(1)]),
                             _expr("eq", [_lit(1), _lit(1)])])
        with self.assertRaises(EvaluatorError):
            _run(expr, _fields(missing="integer"), {})


class ExactTypesTest(unittest.TestCase):
    def test_bool_is_not_int(self):
        with self.assertRaises(ProfileError):
            _run(_expr("eq", [_f("a"), _lit(1)]),
                 _fields(a="boolean"), {"a": True})

    def test_arrays_recursive_exact(self):
        expr = _expr("eq", [_f("v"), _lit([1, [True, "x"]])])
        self.assertTrue(_run(expr, _fields(v="array"),
                             {"v": [1, [True, "x"]]})["matched"])
        self.assertFalse(_run(_expr("eq", [_f("v"), _lit([1])]),
                              _fields(v="array"), {"v": [True]})["matched"])
        out = _run(_expr("eq", [_f("v"), _lit([1, 2])]),
                   _fields(v="array"), {"v": [1, 3]})
        self.assertFalse(out["matched"])

    def test_membership_exact_types(self):
        out = _run(_expr("in", [_f("a"), _lit([1, 2])]),
                   _fields(a="boolean"), {"a": True})
        self.assertFalse(out["matched"])

    def test_unicode_and_bigints(self):
        big = 10 ** 60 + 123456789
        out = _run(_expr("eq", [_f("n"), _lit(big)]),
                   _fields(n="integer"), {"n": big})
        self.assertTrue(out["matched"])
        out = _run(_expr("lt", [_f("s"), _lit("éé")]),
                   _fields(s="string"), {"s": "ée"})
        self.assertTrue(out["matched"])
        self.assertFalse(_run(_expr("gt", [_f("n"), _lit(big)]),
                              _fields(n="integer"), {"n": big})["matched"])


class StabilityTest(unittest.TestCase):
    def test_replay_result_stable_and_no_mutation(self):
        expr = _expr("eq", [_f("a"), _lit(1)])
        schema = _fields(a="integer")
        rule = _rule(expr, schema)
        before_doc = dict(rule.document())
        payload = encode_json_document({"a": 1})
        first = evaluate(rule, payload, "corr-stable")
        second = evaluate(rule, payload, "corr-stable")
        self.assertEqual(first, second)
        self.assertEqual(rule.document(), before_doc)
        self.assertEqual(payload, encode_json_document({"a": 1}))

    def test_replay_refusal_stable(self):
        expr = _expr("eq", [_f("missing"), _lit(1)])
        rule = _rule(expr, _fields(missing="integer"))
        payload = encode_json_document({})
        errors = []
        for _ in range(2):
            with self.assertRaises(EvaluatorError) as caught:
                evaluate(rule, payload, "corr-r1")
            errors.append((type(caught.exception), caught.exception.code, str(caught.exception)))
        self.assertEqual(errors[0], errors[1])


class RefusalTest(unittest.TestCase):
    def test_unknown_operator(self):
        with self.assertRaises(ProfileError):
            _run({"op": "nope", "args": []}, {}, {})

    def test_missing_input_consumed(self):
        with self.assertRaises(EvaluatorError):
            _run(_expr("eq", [_f("need"), _lit(1)]),
                 _fields(need="integer"), {})

    def test_invalid_operand_envelope(self):
        with self.assertRaises(ProfileError):
            _run(_expr("eq", [{"unknown": 1}, _lit(1)]),
                 _fields(a="integer"), {"a": 1})

    def test_invalid_bytes_and_utf8_and_float(self):
        rule = _rule(_expr("eq", [_f("a"), _lit(1)]), _fields(a="integer"))
        with self.assertRaises(EvaluatorError):
            evaluate(rule, b"\xff\xfe", "corr-1")
        with self.assertRaises(EvaluatorError):
            evaluate(rule, b'{"a":1.5}', "corr-1")
        with self.assertRaises((EvaluatorError, ProfileError)):
            evaluate(rule, b"not-json", "corr-1")

    def test_bounds_reuse_codec(self):
        self.assertEqual(MAX_DOCUMENT_BYTES, 65536)
        self.assertEqual(MAX_DEPTH, 8)
        self.assertEqual(MAX_NODES, 256)
        with self.assertRaises(JsonContractError):
            encode_json_document(["x"] * (MAX_NODES + 10))
        deep: object = 1
        for _ in range(MAX_DEPTH + 2):
            deep = [deep]
        with self.assertRaises(JsonContractError):
            encode_json_document(deep)


class ResultContractTest(unittest.TestCase):
    def test_seven_fields_reason_and_no_echo(self):
        rule = _rule(_expr("eq", [_f("a"), _lit(1)]), _fields(a="integer"),
                     owner="o-r", rule_id="r-r", rule_version="v9")
        out = evaluate(rule, encode_json_document({"a": 1}), "corr-explicit")
        self.assertEqual(set(out.keys()),
                         {"profile_version", "rule_id", "rule_version",
                          "owner", "correlation_id", "matched", "reason_codes"})
        self.assertEqual(out["reason_codes"], ["MATCHED"])
        out2 = evaluate(rule, encode_json_document({"a": 2}), "corr-explicit")
        self.assertEqual(out2["reason_codes"], ["NOT_MATCHED"])
        self.assertNotIn("a", out)
        self.assertNotIn("inputs", out)
        with self.assertRaises(EvaluatorError):
            evaluate(rule, encode_json_document({"a": 1}), "   ")

    def test_no_io_clock_random(self):
        rule = _rule(_expr("eq", [_f("a"), _lit(1)]), _fields(a="integer"))
        payload = encode_json_document({"a": 1})
        with patch("builtins.open", side_effect=AssertionError("no-open")), \
             patch("socket.socket", side_effect=AssertionError("no-socket")), \
             patch("time.time", side_effect=AssertionError("no-clock")), \
             patch("random.random", side_effect=AssertionError("no-random")):
            out = evaluate(rule, payload, "corr-pure")
        self.assertTrue(out["matched"])


class CatalogTest(unittest.TestCase):
    def _catalog_rule(self, expression, schema, cases, owner="o-c",
                      rule_id="r-c", rule_version="v1"):
        doc = _doc(expression, schema, cases, owner, rule_id, rule_version)
        return parse_rule_document(encode_json_document(doc))

    def test_each_embedded_case_runs_mismatch_last_refuses(self):
        expr = _expr("eq", [_f("a"), _lit(1)])
        schema = _fields(a="integer")
        good = [
            {"inputs": {"a": 1}, "expected": True},
            {"inputs": {"a": 2}, "expected": False},
        ]
        rule = self._catalog_rule(expr, schema, good)
        RuleCatalog((rule,))
        bad = [
            {"inputs": {"a": 1}, "expected": True},
            {"inputs": {"a": 2}, "expected": True},
        ]
        bad_rule = self._catalog_rule(expr, schema, bad,
                                      rule_id="r-last-bad")
        with self.assertRaises(CatalogError) as ctx:
            RuleCatalog((bad_rule,))
        self.assertNotIn("r-last-bad", str(ctx.exception))

    def test_optional_consumed_absent_in_corpus_refuses(self):
        expr = _expr("eq", [_f("need"), _lit(1)])
        schema = _fields(need="integer")
        rule = self._catalog_rule(expr, schema,
                                  [{"inputs": {}, "expected": False}],
                                  rule_id="r-opt")
        with self.assertRaises(EvaluatorError):
            RuleCatalog((rule,))

    def test_collision_same_version_content_diff(self):
        expr_a = _expr("eq", [_f("a"), _lit(1)])
        expr_b = _expr("eq", [_f("a"), _lit(2)])
        schema = _fields(a="integer")
        ra = self._catalog_rule(expr_a, schema, [], rule_id="r-x")
        rb = self._catalog_rule(expr_b, schema, [], rule_id="r-x")
        with self.assertRaises(CatalogError):
            RuleCatalog((ra, rb))

    def test_copies_immutable_and_direct_ctor_validates(self):
        expr = _expr("eq", [_f("a"), _lit(1)])
        schema = _fields(a="integer")
        rule = self._catalog_rule(expr, schema,
                                  [{"inputs": {"a": 1}, "expected": True}])
        catalog = RuleCatalog((rule,))
        self.assertEqual(catalog.get("o-c", "r-c", "v1").rule_id, "r-c")
        with self.assertRaises(AttributeError):
            catalog.definitions = ()
        with self.assertRaises(CatalogError):
            RuleCatalog("not-a-tuple")
        with self.assertRaises(CatalogError) as ctx:
            catalog.get("o-c", "unknown", "v1")
        self.assertEqual(ctx.exception.code, "unknown_rule")
        self.assertNotIn("unknown", str(ctx.exception))


class EvaluationBoundaryTest(unittest.TestCase):
    def test_input_boundaries_and_closed_schema(self):
        rule = _rule(_expr("exists", _f("v")), _fields(v="array"))
        documents = [b'{"unknown":1}', b'{"v":true}', b'{"v":[1.2]}',
                     b'{"v":' + b'[' * 8 + b'0' + b']' * 8 + b'}',
                     b'{"v":[' + b','.join([b'0'] * 255) + b']}',
                     b'{"v":[]}'+ b' ' * 65536]
        for data in documents:
            with self.subTest(size=len(data)):
                with self.assertRaises(EvaluatorError):
                    evaluate(rule, data, "bounds")

    def test_null_boolean_and_nested_membership(self):
        self.assertTrue(_run(_expr("eq", [_f("v"), _lit(None)]),
                             _fields(v="null"), {"v": None})["matched"])
        self.assertFalse(_run(_expr("ne", [_f("v"), _lit(True)]),
                              _fields(v="boolean"), {"v": True})["matched"])
        self.assertTrue(_run(_expr("in", [_f("v"), _f("items")]),
                             _fields(v="array", items="array"),
                             {"v": [True], "items": [[1], [True]]})["matched"])
        self.assertFalse(_run(_expr("in", [_f("v"), _f("items")]),
                              _fields(v="array", items="array"),
                              {"v": [True], "items": [[1]]})["matched"])

    def test_sensitive_values_not_echoed(self):
        marker = "valeur-privee-inerte-o06"
        rule = _rule(_expr("exists", _f("champ-prive-inerte")),
                     _fields(**{"champ-prive-inerte": "string"}))
        result = evaluate(rule, encode_json_document({"champ-prive-inerte": marker}), "corr")
        serialized = encode_json_document(result)
        self.assertNotIn(marker.encode(), serialized)
        self.assertNotIn(b"champ-prive-inerte", serialized)
        with self.assertRaises(EvaluatorError) as caught:
            evaluate(rule, encode_json_document({"champ-prive-inerte": [marker]}), "corr")
        self.assertNotIn(marker, str(caught.exception))
        self.assertNotIn("champ-prive-inerte", str(caught.exception))

    def test_catalog_copies_input_collection_and_duplicates(self):
        rule = _rule(_expr("exists", _f("v")), _fields(v="string"),
                     [{"inputs": {"v": "x"}, "expected": True}])
        original = [rule, rule]
        catalog = RuleCatalog(original)
        original.clear()
        self.assertIs(catalog.get(rule.owner, rule.rule_id, rule.rule_version), rule)
        self.assertEqual(len(catalog.definitions), 2)
        with self.assertRaises(CatalogError):
            catalog.get(rule.owner, rule.rule_id, "absente")
        with self.assertRaises(CatalogError):
            RuleCatalog((object(),))


if __name__ == "__main__":
    unittest.main()
