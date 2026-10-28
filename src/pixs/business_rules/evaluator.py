"""Evaluation bornee du profil v1, sans entree-sortie ni etat global."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from .json_contract import JsonContractError, encode_json_document
from .profile import ProfileError, RuleDefinition, validate_inputs


MATCHED = "MATCHED"
NOT_MATCHED = "NOT_MATCHED"


class EvaluatorError(ValueError):
    """Refus type d evaluation, message fixe sans valeur."""

    def __init__(self, code: str) -> None:
        super().__init__("Evaluation O06 refusee.")
        self.code = code
        self.element = "evaluation"
        self.step = "evaluate"


class CatalogError(EvaluatorError):
    """Refus type de catalogue, message fixe sans valeur."""


def _is_bool(value: object) -> bool:
    return type(value) is bool


def _is_int(value: object) -> bool:
    return type(value) is int


def _equals_exact(left: object, right: object) -> bool:
    if _is_bool(left) or _is_bool(right):
        return type(left) is type(right) and left == right
    if _is_int(left) and _is_int(right):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return False
        for index in range(len(left)):
            if not _equals_exact(left[index], right[index]):
                return False
        return True
    return left == right


def _resolve_operand(operand: object, inputs: dict) -> object:
    if type(operand) is not dict:
        raise EvaluatorError("invalid_operand")
    keys = set(operand.keys())
    if keys == {"field"}:
        name = operand["field"]
        if type(name) is not str or not name:
            raise EvaluatorError("invalid_operand")
        if name not in inputs:
            raise EvaluatorError("missing_input")
        return inputs[name]
    if keys == {"literal"}:
        return operand["literal"]
    raise EvaluatorError("invalid_operand")


def _eval_expr(expr: object, inputs: dict) -> bool:
    if type(expr) is not dict:
        raise EvaluatorError("invalid_expression")
    op = expr.get("op")
    args = expr.get("args")
    if op == "all":
        if type(args) is not list:
            raise EvaluatorError("invalid_args")
        for item in args:
            if not _eval_expr(item, inputs):
                return False
        return True
    if op == "any":
        if type(args) is not list:
            raise EvaluatorError("invalid_args")
        for item in args:
            if _eval_expr(item, inputs):
                return True
        return False
    if op == "not":
        if type(args) is not dict:
            raise EvaluatorError("invalid_args")
        return not _eval_expr(args, inputs)
    if op == "exists":
        if type(args) is not dict or set(args.keys()) != {"field"}:
            raise EvaluatorError("invalid_args")
        name = args["field"]
        if type(name) is not str or not name:
            raise EvaluatorError("invalid_args")
        return name in inputs
    if op == "eq" or op == "ne":
        if type(args) is not list or len(args) != 2:
            raise EvaluatorError("invalid_args")
        left = _resolve_operand(args[0], inputs)
        right = _resolve_operand(args[1], inputs)
        if type(left) is not type(right):
            raise EvaluatorError("incomparable")
        same = _equals_exact(left, right)
        return same if op == "eq" else (not same)
    if op == "lt" or op == "lte" or op == "gt" or op == "gte":
        if type(args) is not list or len(args) != 2:
            raise EvaluatorError("invalid_args")
        left = _resolve_operand(args[0], inputs)
        right = _resolve_operand(args[1], inputs)
        if _is_bool(left) or _is_bool(right):
            raise EvaluatorError("incomparable")
        if _is_int(left) and _is_int(right):
            pass
        elif type(left) is str and type(right) is str:
            pass
        else:
            raise EvaluatorError("incomparable")
        if op == "lt":
            return bool(left < right)
        if op == "lte":
            return bool(left <= right)
        if op == "gt":
            return bool(left > right)
        return bool(left >= right)
    if op == "in":
        if type(args) is not list or len(args) != 2:
            raise EvaluatorError("invalid_args")
        needle = _resolve_operand(args[0], inputs)
        haystack = _resolve_operand(args[1], inputs)
        if type(haystack) is not list:
            raise EvaluatorError("invalid_args")
        for item in haystack:
            if type(item) is type(needle) and _equals_exact(needle, item):
                return True
        return False
    raise EvaluatorError("unknown_operator")


def _expected_of(case: object) -> bool:
    if type(case) is not dict:
        raise CatalogError("invalid_case")
    expected = case.get("expected")
    if type(expected) is not bool:
        raise CatalogError("invalid_case")
    return expected


def _inputs_of(case: object) -> object:
    if type(case) is not dict:
        raise CatalogError("invalid_case")
    if "inputs" not in case:
        raise CatalogError("invalid_case")
    return case["inputs"]


def evaluate(rule: RuleDefinition, data: bytes, correlation_id: str) -> dict:
    """Evalue une regle validee, resultat ferme a sept champs."""
    if type(rule) is not RuleDefinition:
        raise EvaluatorError("invalid_rule")
    if type(correlation_id) is not str or not correlation_id.strip():
        raise EvaluatorError("invalid_correlation_id")
    if type(data) is not bytes:
        raise EvaluatorError("invalid_inputs")
    try:
        inputs = validate_inputs(rule, data)
    except ProfileError as exc:
        raise EvaluatorError("invalid_inputs") from exc
    if type(inputs) is not dict:
        raise EvaluatorError("invalid_inputs")
    matched = _eval_expr(rule.expression(), dict(inputs))
    if type(matched) is not bool:
        raise EvaluatorError("invalid_result")
    result = {
        "profile_version": rule.profile_version,
        "rule_id": rule.rule_id,
        "rule_version": rule.rule_version,
        "owner": rule.owner,
        "correlation_id": correlation_id,
        "matched": matched,
        "reason_codes": [MATCHED] if matched else [NOT_MATCHED],
    }
    encode_json_document(result)
    return dict(result)


@dataclass(frozen=True, slots=True)
class RuleCatalog:
    """Catalogue immuable de definitions, active a la construction."""

    definitions: tuple[RuleDefinition, ...]
    _by_key: Mapping[tuple[str, str, str], RuleDefinition] = field(
        init=False, repr=False
    )

    def __post_init__(self) -> None:
        raw = self.definitions
        if type(raw) is list:
            raw_items = tuple(raw)
        elif type(raw) is tuple:
            raw_items = raw
        else:
            raise CatalogError("invalid_definitions")
        index: dict[tuple[str, str, str], RuleDefinition] = {}
        order: list[tuple[str, str, str]] = []
        for item in raw_items:
            if type(item) is not RuleDefinition:
                raise CatalogError("invalid_definition")
            try:
                item.__post_init__()
            except ProfileError as exc:
                raise CatalogError("invalid_definition") from exc
            key = (item.owner, item.rule_id, item.rule_version)
            known = index.get(key)
            if known is not None:
                if known.digest != item.digest or known.canonical != item.canonical:
                    raise CatalogError("version_collision")
                continue
            index[key] = item
            order.append(key)
        object.__setattr__(self, "definitions", tuple(raw_items))
        object.__setattr__(self, "_by_key", MappingProxyType(dict(index)))
        for key in order:
            rule = index[key]
            cases = rule.cases()
            if type(cases) is not list:
                raise CatalogError("invalid_cases")
            for position in range(len(cases)):
                case = cases[position]
                try:
                    payload = encode_json_document(_inputs_of(case))
                except JsonContractError as exc:
                    raise CatalogError("invalid_case") from exc
                expected = _expected_of(case)
                outcome = evaluate(
                    rule,
                    payload,
                    "o06-corpus",
                )
                if type(outcome.get("matched")) is not bool:
                    raise CatalogError("invalid_case")
                if bool(outcome["matched"]) is not expected:
                    raise CatalogError("corpus_mismatch")

    def get(self, owner: str, rule_id: str, rule_version: str) -> RuleDefinition:
        """Retourne la definition fige du triplet, sinon erreur typee."""
        if type(owner) is not str or type(rule_id) is not str:
            raise CatalogError("unknown_rule")
        if type(rule_version) is not str:
            raise CatalogError("unknown_rule")
        rule = self._by_key.get((owner, rule_id, rule_version))
        if rule is None:
            raise CatalogError("unknown_rule")
        return rule
