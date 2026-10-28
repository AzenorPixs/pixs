"""Profil O06 JSON v1, pur stdlib, sans moteur ni integration.

Definition figee avec octets JSON canoniques comme unique source de
verite immuable. Construction directe validee, projections defensives.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .json_contract import (
    JsonContractError,
    decode_json_document,
    encode_json_document,
)

__all__ = [
    "ProfileError",
    "RuleDefinition",
    "PROFILE_VERSION",
    "OPERATORS",
    "FIELD_TYPES",
    "TOP_FIELDS",
    "parse_rule_document",
    "validate_inputs",
]

PROFILE_VERSION = 1
OPERATORS = frozenset({"all", "any", "not", "eq", "ne", "lt", "lte", "gt", "gte", "in", "exists"})
FIELD_TYPES = frozenset({"null", "boolean", "integer", "string", "array"})
TOP_FIELDS = ("profile_version", "rule_id", "rule_version", "owner", "input_schema", "expression", "cases")

_FIXED = "Regle O06 hors contrat."


class ProfileError(ValueError):
    """Erreur typee stable, sans valeur refusee recopiee."""

    def __init__(self, code: str = "PROFILE_INVALID") -> None:
        super().__init__(_FIXED)
        self.code = code
        self.element = "profile"
        self.step = "validate"


def _fail(code: str) -> None:
    raise ProfileError(code)


def _is_nonempty_str(value: object) -> bool:
    return type(value) is str and value != ""


def _principal_of_literal(value: object) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "boolean"
    if type(value) is int:
        return "integer"
    if type(value) is str:
        return "string"
    if type(value) is list:
        return "array"
    _fail("PROFILE_LITERAL_FORBIDDEN")
    return "null"


def _check_literal_value(value: object) -> None:
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            _check_literal_value(item)
        return
    _fail("PROFILE_LITERAL_FORBIDDEN")


def _field_type_of(schema: dict, name: str) -> str:
    descriptor = schema.get(name)
    if type(descriptor) is not dict:
        _fail("PROFILE_FIELD_UNDECLARED")
    return descriptor["type"]


def _check_input_schema(schema: object) -> dict:
    if type(schema) is not dict:
        _fail("PROFILE_SCHEMA_INVALID")
    for name, descriptor in schema.items():
        if not _is_nonempty_str(name):
            _fail("PROFILE_SCHEMA_INVALID")
        if type(descriptor) is not dict or set(descriptor.keys()) != {"type", "required"}:
            _fail("PROFILE_SCHEMA_INVALID")
        if type(descriptor["type"]) is not str or descriptor["type"] not in FIELD_TYPES:
            _fail("PROFILE_TYPE_FORBIDDEN")
        if type(descriptor["required"]) is not bool:
            _fail("PROFILE_SCHEMA_INVALID")
    return schema


def _check_operand(operand: object, schema: dict) -> None:
    if type(operand) is not dict or set(operand.keys()) not in ({"field"}, {"literal"}):
        _fail("PROFILE_OPERAND_INVALID")
    if "field" in operand:
        name = operand["field"]
        if not _is_nonempty_str(name):
            _fail("PROFILE_FIELD_UNDECLARED")
        if name not in schema:
            _fail("PROFILE_FIELD_UNDECLARED")
        return
    _check_literal_value(operand["literal"])


def _operand_principal(operand: dict, schema: dict) -> str | None:
    if "literal" in operand:
        return _principal_of_literal(operand["literal"])
    name = operand["field"]
    descriptor = schema.get(name)
    if type(descriptor) is not dict:
        return None
    declared = descriptor.get("type")
    if declared in FIELD_TYPES:
        return declared
    return None


def _require_two_operands(args: object, schema: dict) -> tuple:
    if type(args) is not list or len(args) != 2:
        _fail("PROFILE_ARITY_INVALID")
    first, second = args
    _check_operand(first, schema)
    _check_operand(second, schema)
    return (first, second)


def _check_expression(expression: object, schema: dict) -> None:
    if type(expression) is not dict or set(expression.keys()) != {"op", "args"}:
        _fail("PROFILE_EXPRESSION_INVALID")
    op = expression["op"]
    args = expression["args"]
    if type(op) is not str or op not in OPERATORS:
        _fail("PROFILE_OPERATOR_FORBIDDEN")
    if op in ("all", "any"):
        if type(args) is not list or len(args) == 0:
            _fail("PROFILE_ARITY_INVALID")
        for sub in args:
            _check_expression(sub, schema)
        return
    if op == "not":
        if type(args) is not dict:
            _fail("PROFILE_ARITY_INVALID")
        _check_expression(args, schema)
        return
    if op == "exists":
        if type(args) is not dict:
            _fail("PROFILE_ARITY_INVALID")
        _check_operand(args, schema)
        if "field" not in args:
            _fail("PROFILE_OPERAND_INVALID")
        return
    first, second = _require_two_operands(args, schema)
    if op in ("eq", "ne"):
        left = _operand_principal(first, schema)
        right = _operand_principal(second, schema)
        if left is not None and right is not None and left != right:
            _fail("PROFILE_COMPARISON_INVALID")
        return
    if op in ("lt", "lte", "gt", "gte"):
        left = _operand_principal(first, schema)
        right = _operand_principal(second, schema)
        if left is not None and right is not None:
            if not ((left == "integer" and right == "integer") or (left == "string" and right == "string")):
                _fail("PROFILE_COMPARISON_INVALID")
        return
    if op == "in":
        right = second
        if "literal" in right:
            if type(right["literal"]) is not list:
                _fail("PROFILE_COMPARISON_INVALID")
        else:
            declared = _field_type_of(schema, right["field"])
            if declared != "array":
                _fail("PROFILE_COMPARISON_INVALID")
        return
    _fail("PROFILE_OPERATOR_FORBIDDEN")


def _check_value_against_type(value: object, declared: str) -> None:
    if declared == "null":
        if value is not None:
            _fail("PROFILE_INPUT_TYPE")
        return
    if declared == "boolean":
        if type(value) is not bool:
            _fail("PROFILE_INPUT_TYPE")
        return
    if declared == "integer":
        if type(value) is not int:
            _fail("PROFILE_INPUT_TYPE")
        return
    if declared == "string":
        if type(value) is not str:
            _fail("PROFILE_INPUT_TYPE")
        return
    if declared == "array":
        if type(value) is not list:
            _fail("PROFILE_INPUT_TYPE")
        for item in value:
            _check_literal_value(item)
        return
    _fail("PROFILE_TYPE_FORBIDDEN")


def _check_inputs_dict(schema: dict, inputs: object) -> dict:
    if type(inputs) is not dict:
        _fail("PROFILE_INPUTS_INVALID")
    for key in inputs.keys():
        if type(key) is not str or key not in schema:
            _fail("PROFILE_INPUT_UNKNOWN")
    for name, descriptor in schema.items():
        if name not in inputs:
            if descriptor["required"] is True:
                _fail("PROFILE_INPUT_MISSING")
            continue
        _check_value_against_type(inputs[name], descriptor["type"])
    return inputs


def _validate_rule_structure(document: object) -> dict:
    if type(document) is not dict or set(document.keys()) != set(TOP_FIELDS):
        _fail("PROFILE_TOP_INVALID")
    if type(document["profile_version"]) is not int or document["profile_version"] != PROFILE_VERSION:
        _fail("PROFILE_VERSION_INVALID")
    for key in ("rule_id", "rule_version", "owner"):
        if not _is_nonempty_str(document[key]):
            _fail("PROFILE_IDENTITY_INVALID")
    schema = _check_input_schema(document["input_schema"])
    _check_expression(document["expression"], schema)
    cases = document["cases"]
    if type(cases) is not list or len(cases) == 0:
        _fail("PROFILE_CASES_INVALID")
    seen: set = set()
    for case in cases:
        if type(case) is not dict or set(case.keys()) != {"case_id", "inputs", "expected"}:
            _fail("PROFILE_CASE_INVALID")
        if not _is_nonempty_str(case["case_id"]):
            _fail("PROFILE_CASE_INVALID")
        if case["case_id"] in seen:
            _fail("PROFILE_CASE_DUPLICATE")
        seen.add(case["case_id"])
        if type(case["expected"]) is not bool:
            _fail("PROFILE_CASE_EXPECTED")
        _check_inputs_dict(schema, case["inputs"])
    return document


def _digest_of(canonical: bytes) -> str:
    return hashlib.sha256(canonical).hexdigest()


@dataclass(frozen=True, slots=True)
class RuleDefinition:
    profile_version: int
    rule_id: str
    rule_version: str
    owner: str
    digest: str
    canonical: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.profile_version) is not int or self.profile_version != PROFILE_VERSION:
            _fail("PROFILE_VERSION_INVALID")
        if not _is_nonempty_str(self.rule_id):
            _fail("PROFILE_IDENTITY_INVALID")
        if not _is_nonempty_str(self.rule_version):
            _fail("PROFILE_IDENTITY_INVALID")
        if not _is_nonempty_str(self.owner):
            _fail("PROFILE_IDENTITY_INVALID")
        if type(self.canonical) is not bytes or len(self.canonical) == 0:
            _fail("PROFILE_CANONICAL_INVALID")
        if type(self.digest) is not str or self.digest == "":
            _fail("PROFILE_DIGEST_INVALID")
        try:
            decoded = decode_json_document(self.canonical)
        except JsonContractError as error:
            raise ProfileError(error.code) from error
        if type(decoded) is not dict:
            _fail("PROFILE_TOP_INVALID")
        _validate_rule_structure(decoded)
        try:
            normalized = encode_json_document(decoded)
        except JsonContractError as error:
            raise ProfileError(error.code) from error
        if normalized != self.canonical:
            _fail("PROFILE_CANONICAL_INVALID")
        if decoded["profile_version"] != self.profile_version:
            _fail("PROFILE_IDENTITY_MISMATCH")
        if decoded["rule_id"] != self.rule_id:
            _fail("PROFILE_IDENTITY_MISMATCH")
        if decoded["rule_version"] != self.rule_version:
            _fail("PROFILE_IDENTITY_MISMATCH")
        if decoded["owner"] != self.owner:
            _fail("PROFILE_IDENTITY_MISMATCH")
        if _digest_of(self.canonical) != self.digest:
            _fail("PROFILE_DIGEST_MISMATCH")

    def document(self) -> dict:
        decoded = decode_json_document(self.canonical)
        assert type(decoded) is dict
        return decoded

    def input_schema(self) -> dict:
        return self.document()["input_schema"]

    def expression(self) -> dict:
        return self.document()["expression"]

    def cases(self) -> list:
        return self.document()["cases"]


def parse_rule_document(data: bytes) -> RuleDefinition:
    try:
        decoded = decode_json_document(data)
    except JsonContractError as error:
        raise ProfileError(error.code) from error
    if type(decoded) is not dict:
        _fail("PROFILE_TOP_INVALID")
    _validate_rule_structure(decoded)
    try:
        canonical = encode_json_document(decoded)
    except JsonContractError as error:
        raise ProfileError(error.code) from error
    return RuleDefinition(
        profile_version=decoded["profile_version"],
        rule_id=decoded["rule_id"],
        rule_version=decoded["rule_version"],
        owner=decoded["owner"],
        digest=_digest_of(canonical),
        canonical=canonical,
    )


def validate_inputs(rule: RuleDefinition, data: bytes) -> dict:
    if type(rule) is not RuleDefinition:
        _fail("PROFILE_RULE_INVALID")
    rule.__post_init__()
    try:
        decoded = decode_json_document(data)
    except JsonContractError as error:
        raise ProfileError(error.code) from error
    schema = rule.input_schema()
    _check_inputs_dict(schema, decoded)
    assert type(decoded) is dict
    return decoded
