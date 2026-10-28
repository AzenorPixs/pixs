"""Contrats du profil O06 v1, sans activation runtime implicite."""

from .json_contract import (
    JsonContractError,
    MAX_DEPTH,
    MAX_DOCUMENT_BYTES,
    MAX_NODES,
    decode_json_document,
    encode_json_document,
    normalize_python_value,
)
from .profile import (
    PROFILE_VERSION,
    ProfileError,
    RuleDefinition,
    parse_rule_document,
    validate_inputs,
)

__all__ = [
    "JsonContractError",
    "MAX_DEPTH",
    "MAX_DOCUMENT_BYTES",
    "MAX_NODES",
    "decode_json_document",
    "encode_json_document",
    "normalize_python_value",
    "PROFILE_VERSION",
    "ProfileError",
    "RuleDefinition",
    "parse_rule_document",
    "validate_inputs",
]

from .evaluator import CatalogError, EvaluatorError, RuleCatalog, evaluate

__all__ += ["CatalogError", "EvaluatorError", "RuleCatalog", "evaluate"]
