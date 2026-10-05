"""Contrat de snapshot source de fanions : validation fermée, sans E/S.

Le snapshot regroupe une configuration canonique et les primitives déclaratives
existantes. La validation vérifie la cohérence du lot complet avant lookup ;
l'évaluation délègue réellement à la composition cohorte/C2/R3/expiration.
La provenance persistante et le contexte applicatif canonique restent une
précondition de confiance de l'appelant serveur ; aucune E/S, horloge, cache,
PostgreSQL ou administration n'est introduite.
"""

from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import VALIDATE, Diagnostic
from .feature_flag_cohorts import (
    FeatureFlagCohortRule,
    evaluate_feature_flag_assignments_with_cohort,
    validate_feature_flag_cohort_rule,
)
from .feature_flags import (
    FeatureFlagAssignment,
    FeatureFlagDefinition,
    FeatureFlagEvaluation,
    FeatureFlagEvaluationContext,
    validate_feature_flag_assignments,
    validate_feature_flag_definitions,
    _FALLBACK_USE_KINDS,
    _evaluation_diagnostics,
    _is_nonempty_text,
)

__all__ = [
    "FeatureFlagSourceSnapshot",
    "validate_feature_flag_source_snapshot",
    "evaluate_feature_flag_source_snapshot",
]


@dataclass(frozen=True)
class FeatureFlagSourceSnapshot:
    """Snapshot canonique immuable à quatre champs obligatoires."""

    configuration_version: str
    definitions: tuple[FeatureFlagDefinition, ...]
    assignments: tuple[FeatureFlagAssignment, ...]
    cohort_rules: tuple[FeatureFlagCohortRule, ...]


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"feature_flags.sources.{field}",
        constraint=constraint,
        message=constraint,
    )


def _pack(diagnostics: list[Diagnostic]) -> tuple[Diagnostic, ...]:
    return _evaluation_diagnostics(diagnostics)


def validate_feature_flag_source_snapshot(
    snapshot: FeatureFlagSourceSnapshot,
) -> tuple[Diagnostic, ...]:
    """Valide la structure, les validateurs anciens et les liaisons d'un lot."""
    if type(snapshot) is not FeatureFlagSourceSnapshot:
        return _pack([_refusal("snapshot", "snapshot exact attendu")])

    diagnostics: list[Diagnostic] = []

    if not _is_nonempty_text(snapshot.configuration_version):
        diagnostics.append(
            _refusal("configuration_version", "version de configuration opaque non vide attendue")
        )
    if type(snapshot.definitions) is not tuple:
        diagnostics.append(_refusal("definitions", "tuple de définitions attendu"))
    if type(snapshot.assignments) is not tuple:
        diagnostics.append(_refusal("assignments", "tuple d'affectations attendu"))
    if type(snapshot.cohort_rules) is not tuple:
        diagnostics.append(_refusal("cohort_rules", "tuple de règles de cohorte attendu"))

    if diagnostics:
        return _pack(diagnostics)

    diagnostics.extend(validate_feature_flag_definitions(snapshot.definitions))
    diagnostics.extend(validate_feature_flag_assignments(snapshot.assignments))
    for rule in snapshot.cohort_rules:
        diagnostics.extend(validate_feature_flag_cohort_rule(rule))

    if diagnostics:
        return _pack(diagnostics)

    definitions_by_id: dict[str, FeatureFlagDefinition] = {}
    for definition in snapshot.definitions:
        definitions_by_id[definition.flag_id] = definition

    for assignment in snapshot.assignments:
        if assignment.flag_id not in definitions_by_id:
            diagnostics.append(_refusal("assignment.flag_id", "définition déclarée attendue"))
        else:
            definition = definitions_by_id[assignment.flag_id]
            if assignment.selector not in definition.targeting_dimensions:
                diagnostics.append(
                    _refusal(
                        "assignment.selector",
                        "selector déclaré par la définition attendu",
                    )
                )
        if assignment.configuration_version != snapshot.configuration_version:
            diagnostics.append(
                _refusal(
                    "assignment.configuration_version",
                    "version de configuration exacte attendue",
                )
            )

    rules_by_key: dict[str, FeatureFlagCohortRule] = {}
    for rule in snapshot.cohort_rules:
        key = rule.cohort_key
        if key in rules_by_key:
            diagnostics.append(_refusal("cohort_rules.cohort_key", "règle unique par cohorte attendue"))
            continue
        rules_by_key[key] = rule
        if rule.configuration_version != snapshot.configuration_version:
            diagnostics.append(
                _refusal(
                    "cohort_rule.configuration_version",
                    "version de configuration exacte attendue",
                )
            )

    if diagnostics:
        return _pack(diagnostics)

    referenced_keys: set[str] = set()
    for definition in snapshot.definitions:
        key = definition.cohort_key
        if key is None:
            continue
        referenced_keys.add(key)
        rule = rules_by_key.get(key)
        if rule is None:
            diagnostics.append(_refusal("definitions.cohort_key", "règle de cohorte exacte attendue"))
        elif rule.subject_dimension not in definition.targeting_dimensions:
            diagnostics.append(
                _refusal(
                    "cohort_rule.subject_dimension",
                    "dimension de sujet déclarée par le fanion attendue",
                )
            )

    unreferenced_keys = sorted(set(rules_by_key) - referenced_keys)
    for _key in unreferenced_keys:
        diagnostics.append(_refusal("cohort_rules.referenced", "règles référencées attendues"))

    return _pack(diagnostics)


def evaluate_feature_flag_source_snapshot(
    snapshot: FeatureFlagSourceSnapshot,
    expected_configuration_version: str,
    flag_id: str,
    context: FeatureFlagEvaluationContext,
    use_kind: str,
) -> FeatureFlagEvaluation:
    """Compose une source validée, sans substituer la provenance serveur."""
    diagnostics: list[Diagnostic] = []

    if type(snapshot) is not FeatureFlagSourceSnapshot:
        diagnostics.append(_refusal("evaluation.snapshot", "snapshot exact attendu"))
    if not _is_nonempty_text(expected_configuration_version):
        diagnostics.append(
            _refusal("expected_configuration_version", "version attendue opaque non vide requise")
        )
    if not _is_nonempty_text(flag_id):
        diagnostics.append(_refusal("evaluation.flag_id", "identifiant non vide attendu"))
    if type(context) is not FeatureFlagEvaluationContext:
        diagnostics.append(_refusal("evaluation.context", "contexte exact attendu"))
    if type(use_kind) is not str or use_kind not in _FALLBACK_USE_KINDS:
        diagnostics.append(_refusal("evaluation.use_kind", "usage reconnu attendu"))

    if diagnostics:
        return FeatureFlagEvaluation("REFUSED", None, _pack(diagnostics))

    snapshot_diagnostics = validate_feature_flag_source_snapshot(snapshot)
    if snapshot_diagnostics:
        return FeatureFlagEvaluation("REFUSED", None, snapshot_diagnostics)

    if snapshot.configuration_version != expected_configuration_version:
        return FeatureFlagEvaluation(
            "REFUSED",
            None,
            _pack([_refusal("expected_configuration_version", "version canonique attendue incompatible")]),
        )

    definition = None
    for item in snapshot.definitions:
        if item.flag_id == flag_id:
            definition = item
            break

    if definition is None:
        return FeatureFlagEvaluation(
            "REFUSED",
            None,
            _pack([_refusal("definitions.flag_id", "définition déclarée attendue")]),
        )

    assignments = tuple(
        item for item in snapshot.assignments if item.flag_id == flag_id
    )

    cohort_rule = None
    if definition.cohort_key is not None:
        for item in snapshot.cohort_rules:
            if item.cohort_key == definition.cohort_key:
                cohort_rule = item
                break

        if cohort_rule is None:
            return FeatureFlagEvaluation(
                "REFUSED",
                None,
                _pack([_refusal("definitions.cohort_key", "règle de cohorte exacte attendue")]),
            )

    return evaluate_feature_flag_assignments_with_cohort(
        definition,
        assignments,
        context,
        use_kind,
        cohort_rule,
        expected_configuration_version,
    )
