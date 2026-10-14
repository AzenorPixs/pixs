"""Codec pur du snapshot source de fanions, sans E/S ni dépendance externe.

Le module adapte un contrat source déjà validé vers un document JSON-compatible
et inversement. Il ne prouve aucune persistance, aucune provenance PostgreSQL et
n’ajoute aucune norme de ciblage ou d’affectation.
"""

from __future__ import annotations

from typing import NoReturn

from pixs.kernel.feature_flag_cohorts import FeatureFlagCohortRule
from pixs.kernel.feature_flag_sources import (
    FeatureFlagSourceSnapshot,
    validate_feature_flag_source_snapshot,
)
from pixs.kernel.feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
)

__all__ = [
    "FeatureFlagSnapshotCodecError",
    "decode_feature_flag_source_snapshot",
    "encode_feature_flag_source_snapshot",
]

_ERROR_MESSAGE = "Snapshot source de fanions invalide"

_ROOT_KEYS = (
    "configuration_version",
    "definitions",
    "assignments",
    "cohort_rules",
)

_DEFINITION_KEYS = (
    "flag_id",
    "flag_version",
    "owner_component",
    "purpose",
    "value_schema",
    "default_value",
    "targeting_dimensions",
    "cohort_key",
    "prerequisites",
    "fallback_policy",
    "expires_at",
    "audit_policy",
)

_ASSIGNMENT_KEYS = (
    "flag_id",
    "selector",
    "selector_value",
    "value",
    "valid_from",
    "valid_until",
    "configuration_version",
    "updated_by",
)

_RULE_KEYS = (
    "cohort_key",
    "subject_dimension",
    "threshold_basis_points",
    "configuration_version",
)


class FeatureFlagSnapshotCodecError(ValueError):
    """Refus fermé, sans écho de l’entrée ni du diagnostic causal."""

    def __init__(self) -> None:
        super().__init__(_ERROR_MESSAGE)


def _fail() -> NoReturn:
    raise FeatureFlagSnapshotCodecError() from None


def _check_document(value: object, expected: tuple[str, ...]) -> dict[str, object]:
    if type(value) is not dict or len(value) != len(expected):
        _fail()

    matched = [False] * len(expected)
    for key in value:
        if type(key) is not str:
            _fail()
        found = False
        for index, candidate in enumerate(expected):
            if key == candidate:
                matched[index] = True
                found = True
                break
        if not found:
            _fail()

    if not all(matched):
        _fail()
    return value


def _check_text(value: object) -> str:
    if type(value) is not str:
        _fail()
    return value


def _check_boolean_or_text(value: object) -> bool | str:
    if type(value) is bool:
        return value
    if type(value) is str:
        return value
    _fail()


def _check_integer(value: object) -> int:
    if type(value) is not int:
        _fail()
    return value


def _check_optional_text(value: object) -> str | None:
    if value is None:
        return None
    return _check_text(value)


def _encode_text_tuple(value: object) -> list[str]:
    if type(value) is not tuple:
        _fail()
    return [_check_text(item) for item in value]


def _decode_text_tuple(value: object) -> tuple[str, ...]:
    if type(value) is not list:
        _fail()
    return tuple(_check_text(item) for item in value)


def _check_models(value: object, model_type: type) -> tuple[object, ...]:
    if type(value) is not tuple:
        _fail()
    for item in value:
        if type(item) is not model_type:
            _fail()
    return value


def _decode_record_list(value: object, decode_record) -> tuple[object, ...]:
    if type(value) is not list:
        _fail()
    return tuple(decode_record(item) for item in value)


def _encode_definition(definition: object) -> dict[str, object]:
    if type(definition) is not FeatureFlagDefinition:
        _fail()

    return {
        "flag_id": _check_text(definition.flag_id),
        "flag_version": _check_text(definition.flag_version),
        "owner_component": _check_text(definition.owner_component),
        "purpose": _check_text(definition.purpose),
        "value_schema": _check_text(definition.value_schema),
        "default_value": _check_boolean_or_text(definition.default_value),
        "targeting_dimensions": _encode_text_tuple(definition.targeting_dimensions),
        "cohort_key": _check_optional_text(definition.cohort_key),
        "prerequisites": _encode_text_tuple(definition.prerequisites),
        "fallback_policy": _check_text(definition.fallback_policy),
        "expires_at": _check_text(definition.expires_at),
        "audit_policy": _check_text(definition.audit_policy),
    }


def _encode_assignment(assignment: object) -> dict[str, object]:
    if type(assignment) is not FeatureFlagAssignment:
        _fail()

    return {
        "flag_id": _check_text(assignment.flag_id),
        "selector": _check_text(assignment.selector),
        "selector_value": _check_text(assignment.selector_value),
        "value": _check_boolean_or_text(assignment.value),
        "valid_from": _check_text(assignment.valid_from),
        "valid_until": _check_text(assignment.valid_until),
        "configuration_version": _check_text(assignment.configuration_version),
        "updated_by": _check_text(assignment.updated_by),
    }


def _encode_rule(rule: object) -> dict[str, object]:
    if type(rule) is not FeatureFlagCohortRule:
        _fail()

    return {
        "cohort_key": _check_text(rule.cohort_key),
        "subject_dimension": _check_text(rule.subject_dimension),
        "threshold_basis_points": _check_integer(rule.threshold_basis_points),
        "configuration_version": _check_text(rule.configuration_version),
    }


def _decode_definition(value: object) -> FeatureFlagDefinition:
    record = _check_document(value, _DEFINITION_KEYS)

    return FeatureFlagDefinition(
        flag_id=_check_text(record["flag_id"]),
        flag_version=_check_text(record["flag_version"]),
        owner_component=_check_text(record["owner_component"]),
        purpose=_check_text(record["purpose"]),
        value_schema=_check_text(record["value_schema"]),
        default_value=_check_boolean_or_text(record["default_value"]),
        targeting_dimensions=_decode_text_tuple(record["targeting_dimensions"]),
        cohort_key=_check_optional_text(record["cohort_key"]),
        prerequisites=_decode_text_tuple(record["prerequisites"]),
        fallback_policy=_check_text(record["fallback_policy"]),
        expires_at=_check_text(record["expires_at"]),
        audit_policy=_check_text(record["audit_policy"]),
    )


def _decode_assignment(value: object) -> FeatureFlagAssignment:
    record = _check_document(value, _ASSIGNMENT_KEYS)

    return FeatureFlagAssignment(
        flag_id=_check_text(record["flag_id"]),
        selector=_check_text(record["selector"]),
        selector_value=_check_text(record["selector_value"]),
        value=_check_boolean_or_text(record["value"]),
        valid_from=_check_text(record["valid_from"]),
        valid_until=_check_text(record["valid_until"]),
        configuration_version=_check_text(record["configuration_version"]),
        updated_by=_check_text(record["updated_by"]),
    )


def _decode_rule(value: object) -> FeatureFlagCohortRule:
    record = _check_document(value, _RULE_KEYS)

    return FeatureFlagCohortRule(
        cohort_key=_check_text(record["cohort_key"]),
        subject_dimension=_check_text(record["subject_dimension"]),
        threshold_basis_points=_check_integer(record["threshold_basis_points"]),
        configuration_version=_check_text(record["configuration_version"]),
    )


def encode_feature_flag_source_snapshot(
    snapshot: FeatureFlagSourceSnapshot,
) -> dict[str, object]:
    if type(snapshot) is not FeatureFlagSourceSnapshot:
        _fail()
    if validate_feature_flag_source_snapshot(snapshot):
        _fail()

    return {
        "configuration_version": _check_text(snapshot.configuration_version),
        "definitions": [
            _encode_definition(item)
            for item in _check_models(snapshot.definitions, FeatureFlagDefinition)
        ],
        "assignments": [
            _encode_assignment(item)
            for item in _check_models(snapshot.assignments, FeatureFlagAssignment)
        ],
        "cohort_rules": [
            _encode_rule(item)
            for item in _check_models(snapshot.cohort_rules, FeatureFlagCohortRule)
        ],
    }


def decode_feature_flag_source_snapshot(document: object) -> FeatureFlagSourceSnapshot:
    root = _check_document(document, _ROOT_KEYS)

    definitions = _decode_record_list(root["definitions"], _decode_definition)
    assignments = _decode_record_list(root["assignments"], _decode_assignment)
    cohort_rules = _decode_record_list(root["cohort_rules"], _decode_rule)

    snapshot = FeatureFlagSourceSnapshot(
        configuration_version=_check_text(root["configuration_version"]),
        definitions=definitions,
        assignments=assignments,
        cohort_rules=cohort_rules,
    )

    if validate_feature_flag_source_snapshot(snapshot):
        _fail()
    return snapshot
