"""Contrats internes du runtime Bulk v1 : sept schémas logiques gardés par types exacts.

Module purement mémoire : sans entrée/sortie, ORM, sérialisation, parsing de
format, pixs.core, import dynamique ni état global mutable. Les diagnostics
restent statiques, triés et dédupliqués, et ne reproduisent jamais une valeur
fournie. Les snapshots sont des dataclasses privées figées construites
seulement après validation complète ; ils ne constituent pas un type d'entrée
implicite. Les catalogues de codes et de champs sont exigés depuis des
déclarations serveur explicites, jamais depuis un payload. Pour JSONValueV1,
la profondeur compte les conteneurs list/dict imbriqués depuis 1 pour la
racine, et les membres comptent les éléments de chaque conteneur
individuellement ; ce contrôle n'est ni un sérialiseur global ni une preuve
de contenu propriétaire. Les doublons de clés ne sont pas prouvables après
construction d'un dict et ne sont pas annoncés comme refusés ici.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from pixs.backend.bulk_execution_values import validate_bulk_policy_values
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest.semver import parse_version

__all__ = [
    "validate_authority_assessment_values",
    "validate_server_context_refs_values",
    "validate_mapping_descriptor_values",
    "validate_row_diagnostic_values",
    "validate_command_validation_values",
    "validate_command_execution_values",
    "validate_json_value",
]

_AUTHORITY_SCOPE = "bulk_authority_assessment"
_CONTEXT_SCOPE = "bulk_server_context_refs"
_MAPPING_SCOPE = "bulk_mapping_descriptor"
_ROW_DIAGNOSTIC_SCOPE = "bulk_row_diagnostic"
_COMMAND_VALIDATION_SCOPE = "bulk_command_validation"
_COMMAND_EXECUTION_SCOPE = "bulk_command_execution"
_JSON_SCOPE = "bulk_json_value"

_DECISIONS = frozenset({"ALLOW", "DENY", "UNAVAILABLE"})
_OUTCOMES = frozenset({"APPLIED", "REPLAYED", "REJECTED"})
_VARIANTS = frozenset({"IMPORT", "EXPORT"})
_FORMATS = frozenset({"CSV", "NDJSON"})

_ALLOW = "ALLOW"
_DENY = "DENY"
_UNAVAILABLE = "UNAVAILABLE"
_OPAQUE_RULE = "référence opaque str exacte non vide UTF-8 sans NUL attendue"
_JSON_LEAD = object()

_AUTHORITY_KEYS = ("decision", "resolved_context")
_CONTEXT_KEYS = (
    "subject_id",
    "tenant_id",
    "perimeter_reference",
    "context_reference",
)
_MAPPING_KEYS = (
    "mapping_reference",
    "mapping_version",
    "owner_reference",
    "variant",
    "format",
    "source_fields",
    "target_fields",
    "required_source_fields",
    "field_bindings",
)
_ROW_DIAGNOSTIC_KEYS = ("code", "field_reference", "line_index")
_COMMAND_VALIDATION_KEYS = ("accepted", "diagnostics")
_COMMAND_EXECUTION_KEYS = (
    "outcome",
    "result_reference",
    "diagnostics",
    "event_references",
)


class _ContractRefused(ValueError):
    """Refus interne statique d'un snapshot en validation non vide."""


def _refusal(scope: str, field: str, rule: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"{scope}.{field}" if field else scope,
        constraint=rule,
        message=rule,
    )


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique = {
        (item.element, item.constraint, item.message): item
        for item in refusals
    }
    return [unique[key] for key in sorted(unique)]


def _is_opaque_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_json_text(value: object) -> bool:
    if type(value) is not str:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_complete_semver(value: object) -> bool:
    if type(value) is not str:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


def _exact_mapping(
    candidate: object, scope: str, fields: tuple[str, ...], shape_rule: str
) -> tuple[dict | None, list[Diagnostic]]:
    if type(candidate) is not dict:
        return None, [_refusal(scope, "mapping", shape_rule)]
    items = tuple(candidate.items())
    if any(type(key) is not str for key, _value in items):
        return None, [_refusal(scope, "keys", "clés str exactes attendues")]
    values = dict(items)
    refusals: list[Diagnostic] = []
    if any(key not in fields for key in values):
        refusals.append(_refusal(scope, "mapping", shape_rule))
    for field in fields:
        if field not in values:
            refusals.append(_refusal(scope, field, "champ explicite requis"))
    if refusals:
        return None, refusals
    return values, []


def _catalog_state(
    declared: object, scope: str, field: str
) -> tuple[frozenset[str] | None, list[Diagnostic]]:
    declared_type = type(declared)
    if declared_type is not tuple and declared_type is not frozenset:
        return None, [_refusal(scope, field, "tuple exact ou frozenset attendu")]
    elements = tuple(declared)
    if any(
        not _is_opaque_text(item) for item in elements
    ):
        return None, [_refusal(scope, field, "éléments de catalogue str opaques attendus")]
    return frozenset(elements), []


def _context_type_refusals(values: dict, element: str) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in ("subject_id", "perimeter_reference", "context_reference"):
        if type(values[field]) is not str:
            refusals.append(_refusal(element, field, "str exact attendu"))
    if values["tenant_id"] is not None and type(values["tenant_id"]) is not str:
        refusals.append(_refusal(element, "tenant_id", "str exact ou None attendu"))
    return refusals


def _context_value_refusals(values: dict, element: str) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in (
        "subject_id",
        "tenant_id",
        "perimeter_reference",
        "context_reference",
    ):
        value = values[field]
        if value is None:
            continue
        if not _is_opaque_text(value):
            refusals.append(_refusal(element, field, _OPAQUE_RULE))
    return refusals


def validate_server_context_refs_values(candidate: object) -> list[Diagnostic]:
    """Contrôle ServerContextRefsV1 : quatre clés, tenant None générique admis."""
    values, refusals = _exact_mapping(
        candidate, _CONTEXT_SCOPE, _CONTEXT_KEYS, "quatre clés exactes attendues"
    )
    if values is None:
        return _pack(refusals)
    type_refusals = _context_type_refusals(values, _CONTEXT_SCOPE)
    if type_refusals:
        return _pack(type_refusals)
    return _pack(_context_value_refusals(values, _CONTEXT_SCOPE))


def validate_authority_assessment_values(candidate: object) -> list[Diagnostic]:
    """Contrôle AuthorityAssessmentV1 Bulk : ALLOW complet non None, refus sans contexte."""
    values, refusals = _exact_mapping(
        candidate, _AUTHORITY_SCOPE, _AUTHORITY_KEYS, "deux clés exactes attendues"
    )
    if values is None:
        return _pack(refusals)
    type_refusals: list[Diagnostic] = []
    if type(values["decision"]) is not str:
        type_refusals.append(
            _refusal(_AUTHORITY_SCOPE, "decision", "str exact attendu")
        )
    resolved = values["resolved_context"]
    if resolved is not None and type(resolved) is not dict:
        type_refusals.append(
            _refusal(
                _AUTHORITY_SCOPE,
                "resolved_context",
                "None ou dict exact attendu",
            )
        )
    if type_refusals:
        return _pack(type_refusals)
    decision = values["decision"]
    if decision not in _DECISIONS:
        return _pack(
            [
                _refusal(
                    _AUTHORITY_SCOPE,
                    "decision",
                    "membre ALLOW, DENY ou UNAVAILABLE attendu",
                )
            ]
        )
    if decision == _ALLOW:
        if resolved is None:
            return _pack(
                [
                    _refusal(
                        _AUTHORITY_SCOPE,
                        "resolved_context",
                        "contexte ServerContextRefsV1 obligatoire pour ALLOW",
                    )
                ]
            )
        context_element = f"{_AUTHORITY_SCOPE}.resolved_context"
        context_values, context_refusals = _exact_mapping(
            resolved, context_element, _CONTEXT_KEYS, "quatre clés exactes attendues"
        )
        if context_values is None:
            return _pack(context_refusals)
        context_types = _context_type_refusals(context_values, context_element)
        if context_types:
            return _pack(context_types)
        refusals = _context_value_refusals(context_values, context_element)
        if context_values["tenant_id"] is None:
            refusals.append(
                _refusal(
                    context_element,
                    "tenant_id",
                    "ALLOW Bulk avec tenant_id résolu non None attendu",
                )
            )
        return _pack(refusals)
    if resolved is not None:
        return _pack(
            [
                _refusal(
                    _AUTHORITY_SCOPE,
                    "resolved_context",
                    "None attendu pour DENY ou UNAVAILABLE",
                )
            ]
        )
    return []


def _tuple_of_exact_str(values: dict, field: str) -> list[Diagnostic]:
    if any(type(item) is not str for item in values[field]):
        return [_refusal(_MAPPING_SCOPE, field, "éléments str exacts attendus")]
    return []


def _bindings_type_refusals(values: dict) -> list[Diagnostic]:
    for item in values["field_bindings"]:
        if type(item) is not tuple or len(item) != 2:
            return [
                _refusal(
                    _MAPPING_SCOPE,
                    "field_bindings",
                    "couples tuple exacts de longueur deux attendus",
                )
            ]
        if any(type(part) is not str for part in item):
            return [
                _refusal(
                    _MAPPING_SCOPE,
                    "field_bindings",
                    "couples de str exactes attendus",
                )
            ]
    return []


def validate_mapping_descriptor_values(candidate: object) -> list[Diagnostic]:
    """Contrôle MappingDescriptorV1 : immuabilité déclarée, bijection sans heuristique."""
    values, refusals = _exact_mapping(
        candidate, _MAPPING_SCOPE, _MAPPING_KEYS, "neuf clés exactes attendues"
    )
    if values is None:
        return _pack(refusals)
    type_refusals: list[Diagnostic] = []
    for field in (
        "mapping_reference",
        "mapping_version",
        "owner_reference",
        "variant",
        "format",
    ):
        if type(values[field]) is not str:
            type_refusals.append(_refusal(_MAPPING_SCOPE, field, "str exact attendu"))
    for field in (
        "source_fields",
        "target_fields",
        "required_source_fields",
        "field_bindings",
    ):
        if type(values[field]) is not tuple:
            type_refusals.append(_refusal(_MAPPING_SCOPE, field, "tuple exact attendu"))
    if type_refusals:
        return _pack(type_refusals)
    element_refusals: list[Diagnostic] = []
    for field in ("source_fields", "target_fields", "required_source_fields"):
        element_refusals.extend(_tuple_of_exact_str(values, field))
    element_refusals.extend(_bindings_type_refusals(values))
    if element_refusals:
        return _pack(element_refusals)

    refusals = []
    for field in ("mapping_reference", "owner_reference"):
        if not _is_opaque_text(values[field]):
            refusals.append(_refusal(_MAPPING_SCOPE, field, _OPAQUE_RULE))
    if not _is_complete_semver(values["mapping_version"]):
        refusals.append(
            _refusal(
                _MAPPING_SCOPE,
                "mapping_version",
                "version SemVer complète exacte attendue",
            )
        )
    if values["variant"] not in _VARIANTS:
        refusals.append(
            _refusal(
                _MAPPING_SCOPE,
                "variant",
                "valeur exacte IMPORT ou EXPORT attendue",
            )
        )
    if values["format"] not in _FORMATS:
        refusals.append(
            _refusal(
                _MAPPING_SCOPE,
                "format",
                "valeur exacte CSV ou NDJSON attendue",
            )
        )
    for field in ("source_fields", "target_fields", "required_source_fields"):
        items = values[field]
        if any(not _is_opaque_text(item) for item in items):
            refusals.append(_refusal(_MAPPING_SCOPE, field, _OPAQUE_RULE))
        elif len(set(items)) != len(items):
            refusals.append(
                _refusal(
                    _MAPPING_SCOPE,
                    field,
                    "str uniques dans l'ordre déclaré attendues",
                )
            )
    source_set = frozenset(values["source_fields"])
    target_set = frozenset(values["target_fields"])
    if any(item not in source_set for item in values["required_source_fields"]):
        refusals.append(
            _refusal(
                _MAPPING_SCOPE,
                "required_source_fields",
                "sous-ensemble de source_fields attendu",
            )
        )
    bound_sources = [item[0] for item in values["field_bindings"]]
    bound_targets = [item[1] for item in values["field_bindings"]]
    bindings = values["field_bindings"]
    if any(not _is_opaque_text(item) for pair in bindings for item in pair):
        refusals.append(
            _refusal(
                _MAPPING_SCOPE,
                "field_bindings",
                "éléments de couples str opaques attendus",
            )
        )
    else:
        if len(set(bound_sources)) != len(bound_sources):
            refusals.append(
                _refusal(
                    _MAPPING_SCOPE,
                    "field_bindings",
                    "bijection déclarée sans source dupliquée attendue",
                )
            )
        if len(set(bound_targets)) != len(bound_targets):
            refusals.append(
                _refusal(
                    _MAPPING_SCOPE,
                    "field_bindings",
                    "bijection déclarée sans cible dupliquée attendue",
                )
            )
        if any(item not in source_set for item in bound_sources):
            refusals.append(
                _refusal(
                    _MAPPING_SCOPE,
                    "field_bindings",
                    "source déclarée en source_fields attendue",
                )
            )
        if any(item not in target_set for item in bound_targets):
            refusals.append(
                _refusal(
                    _MAPPING_SCOPE,
                    "field_bindings",
                    "cible déclarée en target_fields attendue",
                )
            )
    if frozenset(bound_sources) != source_set or frozenset(bound_targets) != target_set:
        refusals.append(
            _refusal(_MAPPING_SCOPE, "field_bindings", "bijection complète des champs déclarés attendue")
        )
    return _pack(refusals)


def _row_diagnostic_refusals(
    item: object, element: str, codes: frozenset[str], fields: frozenset[str]
) -> list[Diagnostic]:
    values, refusals = _exact_mapping(
        item, element, _ROW_DIAGNOSTIC_KEYS, "trois clés exactes attendues"
    )
    if values is None:
        return refusals
    type_refusals: list[Diagnostic] = []
    if type(values["code"]) is not str:
        type_refusals.append(_refusal(element, "code", "str exact attendu"))
    field_reference = values["field_reference"]
    if field_reference is not None and type(field_reference) is not str:
        type_refusals.append(
            _refusal(element, "field_reference", "str exact ou None attendu")
        )
    line_index = values["line_index"]
    if line_index is not None and type(line_index) is not int:
        type_refusals.append(
            _refusal(element, "line_index", "int exact ou None attendu")
        )
    if type_refusals:
        return type_refusals
    refusals = []
    if values["code"] not in codes:
        refusals.append(
            _refusal(element, "code", "code statique déclaré côté serveur attendu")
        )
    if field_reference is not None and field_reference not in fields:
        refusals.append(
            _refusal(
                element,
                "field_reference",
                "champ déclaré côté serveur ou None attendu",
            )
        )
    if line_index is not None and line_index < 1:
        refusals.append(
            _refusal(
                element, "line_index", "entier exact supérieur ou égal à un attendu"
            )
        )
    return refusals


def validate_row_diagnostic_values(
    candidate: object, *, declared_codes: object, declared_fields: object
) -> list[Diagnostic]:
    """Contrôle RowDiagnosticV1 avec catalogues serveur explicites, sans écho."""
    codes, code_refusals = _catalog_state(
        declared_codes, _ROW_DIAGNOSTIC_SCOPE, "declared_codes"
    )
    fields, field_refusals = _catalog_state(
        declared_fields, _ROW_DIAGNOSTIC_SCOPE, "declared_fields"
    )
    if codes is None or fields is None:
        return _pack([*code_refusals, *field_refusals])
    return _pack(
        _row_diagnostic_refusals(candidate, _ROW_DIAGNOSTIC_SCOPE, codes, fields)
    )


def _policy_bound(policy: object, scope: str) -> tuple[int | None, list[Diagnostic]]:
    if validate_bulk_policy_values(policy):
        return None, [
            _refusal(
                scope,
                "policy",
                "PolicyV1 exacte valide obligatoire pour les bornes",
            )
        ]
    return policy["max_diagnostics"], []


def _command_items_refusals(
    diagnostics: tuple[object, ...],
    scope: str,
    codes: frozenset[str],
    fields: frozenset[str],
) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for index, item in enumerate(diagnostics):
        refusals.extend(
            _row_diagnostic_refusals(
                item, f"{scope}.diagnostics[{index}]", codes, fields
            )
        )
    return refusals


def validate_command_validation_values(
    candidate: object,
    *,
    policy: object,
    declared_codes: object,
    declared_fields: object,
) -> list[Diagnostic]:
    """Contrôle CommandValidationV1 : accepted si et seulement si diagnostics vide."""
    bound, refusals = _policy_bound(policy, _COMMAND_VALIDATION_SCOPE)
    codes, code_refusals = _catalog_state(
        declared_codes, _COMMAND_VALIDATION_SCOPE, "declared_codes"
    )
    fields, field_refusals = _catalog_state(
        declared_fields, _COMMAND_VALIDATION_SCOPE, "declared_fields"
    )
    refusals = [*refusals, *code_refusals, *field_refusals]
    if refusals or bound is None or codes is None or fields is None:
        return _pack(refusals)
    values, mapping_refusals = _exact_mapping(
        candidate,
        _COMMAND_VALIDATION_SCOPE,
        _COMMAND_VALIDATION_KEYS,
        "deux clés exactes attendues",
    )
    if values is None:
        return _pack(mapping_refusals)
    type_refusals: list[Diagnostic] = []
    if type(values["accepted"]) is not bool:
        type_refusals.append(
            _refusal(_COMMAND_VALIDATION_SCOPE, "accepted", "bool exact attendu")
        )
    if type(values["diagnostics"]) is not tuple:
        type_refusals.append(
            _refusal(_COMMAND_VALIDATION_SCOPE, "diagnostics", "tuple exact attendu")
        )
    if type_refusals:
        return _pack(type_refusals)
    item_refusals = _command_items_refusals(
        values["diagnostics"], _COMMAND_VALIDATION_SCOPE, codes, fields
    )
    if item_refusals:
        return _pack(item_refusals)
    count = len(values["diagnostics"])
    refusals = []
    if count > bound:
        refusals.append(
            _refusal(
                _COMMAND_VALIDATION_SCOPE,
                "diagnostics",
                "longueur bornée par max_diagnostics attendue",
            )
        )
    if values["accepted"] is not (count == 0):
        refusals.append(
            _refusal(
                _COMMAND_VALIDATION_SCOPE,
                "accepted",
                "accepted vrai si et seulement si diagnostics vide attendu",
            )
        )
    return _pack(refusals)


def validate_command_execution_values(
    candidate: object,
    *,
    policy: object,
    declared_codes: object,
    declared_fields: object,
) -> list[Diagnostic]:
    """Contrôle CommandExecutionV1 sans couplage inventé entre outcome et diagnostics."""
    bound, refusals = _policy_bound(policy, _COMMAND_EXECUTION_SCOPE)
    codes, code_refusals = _catalog_state(
        declared_codes, _COMMAND_EXECUTION_SCOPE, "declared_codes"
    )
    fields, field_refusals = _catalog_state(
        declared_fields, _COMMAND_EXECUTION_SCOPE, "declared_fields"
    )
    refusals = [*refusals, *code_refusals, *field_refusals]
    if refusals or bound is None or codes is None or fields is None:
        return _pack(refusals)
    values, mapping_refusals = _exact_mapping(
        candidate,
        _COMMAND_EXECUTION_SCOPE,
        _COMMAND_EXECUTION_KEYS,
        "quatre clés exactes attendues",
    )
    if values is None:
        return _pack(mapping_refusals)
    type_refusals: list[Diagnostic] = []
    if type(values["outcome"]) is not str:
        type_refusals.append(
            _refusal(_COMMAND_EXECUTION_SCOPE, "outcome", "str exact attendu")
        )
    result_reference = values["result_reference"]
    if result_reference is not None and type(result_reference) is not str:
        type_refusals.append(
            _refusal(
                _COMMAND_EXECUTION_SCOPE,
                "result_reference",
                "str exact ou None attendu",
            )
        )
    if type(values["diagnostics"]) is not tuple:
        type_refusals.append(
            _refusal(_COMMAND_EXECUTION_SCOPE, "diagnostics", "tuple exact attendu")
        )
    if type(values["event_references"]) is not tuple:
        type_refusals.append(
            _refusal(
                _COMMAND_EXECUTION_SCOPE, "event_references", "tuple exact attendu"
            )
        )
    if type_refusals:
        return _pack(type_refusals)
    for event_index, event in enumerate(values["event_references"]):
        if type(event) is not str:
            return _pack(
                [
                    _refusal(
                        _COMMAND_EXECUTION_SCOPE,
                        f"event_references[{event_index}]",
                        "str exact attendu",
                    )
                ]
            )
    item_refusals = _command_items_refusals(
        values["diagnostics"], _COMMAND_EXECUTION_SCOPE, codes, fields
    )
    if item_refusals:
        return _pack(item_refusals)
    refusals = []
    if values["outcome"] not in _OUTCOMES:
        refusals.append(
            _refusal(
                _COMMAND_EXECUTION_SCOPE,
                "outcome",
                "membre APPLIED, REPLAYED ou REJECTED attendu",
            )
        )
    if result_reference is not None and not _is_opaque_text(result_reference):
        refusals.append(
            _refusal(_COMMAND_EXECUTION_SCOPE, "result_reference", _OPAQUE_RULE)
        )
    if len(values["diagnostics"]) > bound:
        refusals.append(
            _refusal(
                _COMMAND_EXECUTION_SCOPE,
                "diagnostics",
                "longueur bornée par max_diagnostics attendue",
            )
        )
    for event_index, event in enumerate(values["event_references"]):
        if not _is_opaque_text(event):
            refusals.append(
                _refusal(
                    _COMMAND_EXECUTION_SCOPE,
                    f"event_references[{event_index}]",
                    _OPAQUE_RULE,
                )
            )
    return _pack(refusals)


def validate_json_value(
    candidate: object, *, max_depth: object, max_members: object
) -> list[Diagnostic]:
    """Contrôle itératif borné de JSONValueV1 ; ni sérialiseur ni preuve de doublons."""
    if type(max_depth) is not int or max_depth <= 0:
        return _pack(
            [
                _refusal(
                    _JSON_SCOPE,
                    "max_depth",
                    "entier exact strictement positif obligatoire attendu",
                )
            ]
        )
    if type(max_members) is not int or max_members <= 0:
        return _pack(
            [
                _refusal(
                    _JSON_SCOPE,
                    "max_members",
                    "entier exact strictement positif obligatoire attendu",
                )
            ]
        )
    refusals: list[Diagnostic] = []
    stack: list[object] = [(candidate, 1, "")]
    ancestor_ids: list[int] = []
    while stack:
        entry = stack.pop()
        if entry is _JSON_LEAD:
            ancestor_ids.pop()
            continue
        value, depth, position = entry
        element = f"{_JSON_SCOPE}{position}"
        value_type = type(value)
        if value is None or value_type is bool or value_type is int:
            continue
        if value_type is float:
            if not math.isfinite(value):
                refusals.append(
                    _refusal(element, "value", "float exact fini attendu")
                )
            continue
        if value_type is str:
            if not _is_json_text(value):
                refusals.append(
                    _refusal(element, "value", "str Unicode valide attendue")
                )
            continue
        if value_type is list or value_type is dict:
            if depth > max_depth:
                refusals.append(
                    _refusal(
                        element,
                        "container",
                        "profondeur de conteneur inférieure ou égale à la limite attendue",
                    )
                )
                continue
            if id(value) in ancestor_ids:
                refusals.append(
                    _refusal(element, "container", "structure cyclique refusée")
                )
                continue
            if len(value) > max_members:
                refusals.append(
                    _refusal(element, "members", "nombre de membres du conteneur inférieur ou égal à la limite attendu")
                )
                continue
            if value_type is dict:
                items = tuple(value.items())
                if any(type(key) is not str for key, _ignored in items):
                    refusals.append(
                        _refusal(element, "keys", "clés dict str exactes attendues")
                    )
                    continue
                if any(not _is_json_text(key) for key, _ignored in items):
                    refusals.append(
                        _refusal(
                            element, "keys", "clés dict str Unicode valides attendues"
                        )
                    )
                    continue
                children = [(key, child) for key, child in items]
            else:
                children = [(None, child) for child in value]
            count = len(children)
            if count > max_members:
                refusals.append(
                    _refusal(
                        element,
                        "members",
                        "nombre de membres du conteneur inférieur ou égal à la limite attendu",
                    )
                )
            ancestor_ids.append(id(value))
            stack.append(_JSON_LEAD)
            for index in range(count - 1, -1, -1):
                stack.append((children[index][1], depth + 1, f"{position}[{index}]"))
            continue
        refusals.append(
            _refusal(
                element,
                "value",
                "None, bool, int, float fini, str, list ou dict exacts attendus",
            )
        )
    return _pack(refusals)


@dataclass(frozen=True, slots=True)
class _ServerContextRefsSnapshot:
    subject_id: str
    tenant_id: str | None
    perimeter_reference: str
    context_reference: str

    def as_values(self) -> dict:
        return {
            "subject_id": self.subject_id,
            "tenant_id": self.tenant_id,
            "perimeter_reference": self.perimeter_reference,
            "context_reference": self.context_reference,
        }


@dataclass(frozen=True, slots=True)
class _AuthorityAssessmentSnapshot:
    decision: str
    resolved_context: _ServerContextRefsSnapshot | None

    def as_values(self) -> dict:
        return {
            "decision": self.decision,
            "resolved_context": (
                self.resolved_context.as_values()
                if self.resolved_context is not None
                else None
            ),
        }


@dataclass(frozen=True, slots=True)
class _MappingDescriptorSnapshot:
    mapping_reference: str
    mapping_version: str
    owner_reference: str
    variant: str
    format: str
    source_fields: tuple[str, ...]
    target_fields: tuple[str, ...]
    required_source_fields: tuple[str, ...]
    field_bindings: tuple[tuple[str, str], ...]

    def as_values(self) -> dict:
        return {
            "mapping_reference": self.mapping_reference,
            "mapping_version": self.mapping_version,
            "owner_reference": self.owner_reference,
            "variant": self.variant,
            "format": self.format,
            "source_fields": tuple(self.source_fields),
            "target_fields": tuple(self.target_fields),
            "required_source_fields": tuple(self.required_source_fields),
            "field_bindings": tuple(tuple(pair) for pair in self.field_bindings),
        }


@dataclass(frozen=True, slots=True)
class _RowDiagnosticSnapshot:
    code: str
    field_reference: str | None
    line_index: int | None

    def as_values(self) -> dict:
        return {
            "code": self.code,
            "field_reference": self.field_reference,
            "line_index": self.line_index,
        }


@dataclass(frozen=True, slots=True)
class _CommandValidationSnapshot:
    accepted: bool
    diagnostics: tuple[_RowDiagnosticSnapshot, ...]

    def as_values(self) -> dict:
        return {
            "accepted": self.accepted,
            "diagnostics": tuple(item.as_values() for item in self.diagnostics),
        }


@dataclass(frozen=True, slots=True)
class _CommandExecutionSnapshot:
    outcome: str
    result_reference: str | None
    diagnostics: tuple[_RowDiagnosticSnapshot, ...]
    event_references: tuple[str, ...]

    def as_values(self) -> dict:
        return {
            "outcome": self.outcome,
            "result_reference": self.result_reference,
            "diagnostics": tuple(item.as_values() for item in self.diagnostics),
            "event_references": tuple(self.event_references),
        }


def _require_clean(refusals: list[Diagnostic]) -> None:
    if refusals:
        raise _ContractRefused("snapshot de contrat bulk runtime refusé en validation")


def _capture_contract_values(candidate: object, fields: tuple[str, ...], scope: str) -> dict:
    values, refusals = _exact_mapping(candidate, scope, fields, "clés logiques exactes requises")
    _require_clean(refusals)
    if fields is _AUTHORITY_KEYS and type(values["resolved_context"]) is dict:
        values["resolved_context"] = _capture_contract_values(
            values["resolved_context"], _CONTEXT_KEYS, _CONTEXT_SCOPE
        )
    if fields is _COMMAND_VALIDATION_KEYS or fields is _COMMAND_EXECUTION_KEYS:
        diagnostics = values["diagnostics"]
        if type(diagnostics) is tuple:
            values["diagnostics"] = tuple(
                _capture_contract_values(item, _ROW_DIAGNOSTIC_KEYS, _ROW_DIAGNOSTIC_SCOPE)
                if type(item) is dict else item
                for item in diagnostics
            )
    return values


def _capture_policy_values(policy: object) -> object:
    if type(policy) is not dict:
        return policy
    items = tuple(policy.items())
    if any(type(key) is not str for key, _value in items):
        return policy
    copied = dict(items)
    for name in ("retry_delays_seconds", "publish_retry_delays_seconds"):
        if name in copied and type(copied[name]) is list:
            copied[name] = list(copied[name])
    return copied


def _build_server_context_refs_snapshot(values: dict) -> _ServerContextRefsSnapshot:
    values = _capture_contract_values(values, _CONTEXT_KEYS, _CONTEXT_SCOPE)
    _require_clean(validate_server_context_refs_values(values))
    return _ServerContextRefsSnapshot(
        subject_id=values["subject_id"],
        tenant_id=values["tenant_id"],
        perimeter_reference=values["perimeter_reference"],
        context_reference=values["context_reference"],
    )


def _build_authority_assessment_snapshot(
    values: dict,
) -> _AuthorityAssessmentSnapshot:
    values = _capture_contract_values(values, _AUTHORITY_KEYS, _AUTHORITY_SCOPE)
    _require_clean(validate_authority_assessment_values(values))
    resolved = values["resolved_context"]
    return _AuthorityAssessmentSnapshot(
        decision=values["decision"],
        resolved_context=(
            _build_server_context_refs_snapshot(resolved)
            if resolved is not None
            else None
        ),
    )


def _build_mapping_descriptor_snapshot(
    values: dict,
) -> _MappingDescriptorSnapshot:
    values = _capture_contract_values(values, _MAPPING_KEYS, _MAPPING_SCOPE)
    _require_clean(validate_mapping_descriptor_values(values))
    return _MappingDescriptorSnapshot(
        mapping_reference=values["mapping_reference"],
        mapping_version=values["mapping_version"],
        owner_reference=values["owner_reference"],
        variant=values["variant"],
        format=values["format"],
        source_fields=tuple(values["source_fields"]),
        target_fields=tuple(values["target_fields"]),
        required_source_fields=tuple(values["required_source_fields"]),
        field_bindings=tuple(tuple(pair) for pair in values["field_bindings"]),
    )


def _build_row_diagnostic_snapshot(
    values: dict, *, declared_codes: object, declared_fields: object
) -> _RowDiagnosticSnapshot:
    values = _capture_contract_values(values, _ROW_DIAGNOSTIC_KEYS, _ROW_DIAGNOSTIC_SCOPE)
    _require_clean(
        validate_row_diagnostic_values(
            values,
            declared_codes=declared_codes,
            declared_fields=declared_fields,
        )
    )
    return _RowDiagnosticSnapshot(
        code=values["code"],
        field_reference=values["field_reference"],
        line_index=values["line_index"],
    )


def _build_command_validation_snapshot(
    values: dict,
    *,
    policy: dict,
    declared_codes: object,
    declared_fields: object,
) -> _CommandValidationSnapshot:
    values = _capture_contract_values(values, _COMMAND_VALIDATION_KEYS, _COMMAND_VALIDATION_SCOPE)
    policy = _capture_policy_values(policy)
    _require_clean(
        validate_command_validation_values(
            values,
            policy=policy,
            declared_codes=declared_codes,
            declared_fields=declared_fields,
        )
    )
    return _CommandValidationSnapshot(
        accepted=values["accepted"],
        diagnostics=tuple(
            _build_row_diagnostic_snapshot(
                item,
                declared_codes=declared_codes,
                declared_fields=declared_fields,
            )
            for item in values["diagnostics"]
        ),
    )


def _build_command_execution_snapshot(
    values: dict,
    *,
    policy: dict,
    declared_codes: object,
    declared_fields: object,
) -> _CommandExecutionSnapshot:
    values = _capture_contract_values(values, _COMMAND_EXECUTION_KEYS, _COMMAND_EXECUTION_SCOPE)
    policy = _capture_policy_values(policy)
    _require_clean(
        validate_command_execution_values(
            values,
            policy=policy,
            declared_codes=declared_codes,
            declared_fields=declared_fields,
        )
    )
    return _CommandExecutionSnapshot(
        outcome=values["outcome"],
        result_reference=values["result_reference"],
        diagnostics=tuple(
            _build_row_diagnostic_snapshot(
                item,
                declared_codes=declared_codes,
                declared_fields=declared_fields,
            )
            for item in values["diagnostics"]
        ),
        event_references=tuple(values["event_references"]),
    )
