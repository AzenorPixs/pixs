"""Règle déclarative et appartenance de cohorte : module pur, stdlib seulement.

Algorithme v1 : JSON ASCII compact [clé, dimension, identité], SHA-256 complet
big-endian modulo 10000. Le seuil, la version et as_of ne redistribuent pas
le bucket. L'appelant serveur canonique est une précondition de confiance,
non une provenance prouvée. Aucune valeur de fanion ou permission n'est rendue ;
la composition, l'expiration, les prérequis et la persistance restent séparés.
Les helpers privés partagés du même Kernel évitent toute grammaire parallèle.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from collections.abc import Sequence
from datetime import datetime

from .diagnostics import VALIDATE, Diagnostic
from .feature_flags import (
    FLAG_TARGETING_DIMENSIONS,
    FeatureFlagDefinition,
    FeatureFlagEvaluationContext,
    _EVALUATION_CONTEXT_FIELDS,
    _evaluation_diagnostics,
    _is_bare_reference,
    _is_nonempty_text,
    _validate_context,
    validate_feature_flag_definitions,
    FeatureFlagAssignment,
    FeatureFlagEvaluation,
    _FALLBACK_USE_KINDS,
    _FALLBACK_POLICIES,
    _classify_no_match,
    evaluate_feature_flag_assignments_bounded,
    resolve_feature_flag_assignment,
    resolve_feature_flag_fallback,
    validate_feature_flag_assignments,
    validate_feature_flag_assignment_expiry,
)

__all__ = [
    "FeatureFlagCohortRule", "FeatureFlagCohortResolution",
    "validate_feature_flag_cohort_rule", "resolve_feature_flag_cohort",
    "evaluate_feature_flag_assignments_with_cohort",
]

_BUCKET_MODULUS = 10000


@dataclass(frozen=True)
class FeatureFlagCohortRule:
    """Quatre champs canoniques obligatoires, sans défaut ou alias."""

    cohort_key: str
    subject_dimension: str
    threshold_basis_points: int
    configuration_version: str


@dataclass(frozen=True)
class FeatureFlagCohortResolution:
    """MEMBER/NON_MEMBER avec bucket ; REFUSED sans bucket, jamais permission."""

    status: str
    bucket: int | None
    diagnostics: tuple[Diagnostic, ...]


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(step=VALIDATE, element=f"feature_flags.cohorts.{field}",
                      constraint=constraint, message=constraint)


def _refused(diagnostics: list[Diagnostic]) -> FeatureFlagCohortResolution:
    return FeatureFlagCohortResolution("REFUSED", None,
                                       _evaluation_diagnostics(diagnostics))


def validate_feature_flag_cohort_rule(rule: FeatureFlagCohortRule) -> tuple[Diagnostic, ...]:
    """Valide une seule règle, sans lookup de dataset, attribut hostile ou effet."""
    if type(rule) is not FeatureFlagCohortRule:
        return _evaluation_diagnostics([_refusal("rule", "règle exacte attendue")])
    diagnostics: list[Diagnostic] = []
    if not _is_bare_reference(rule.cohort_key):
        diagnostics.append(_refusal("cohort_key", "référence nue attendue"))
    if type(rule.subject_dimension) is not str or rule.subject_dimension not in FLAG_TARGETING_DIMENSIONS:
        diagnostics.append(_refusal("subject_dimension", "dimension bornée attendue"))
    threshold = rule.threshold_basis_points
    if type(threshold) is not int or not 0 <= threshold <= _BUCKET_MODULUS:
        diagnostics.append(_refusal("threshold_basis_points", "entier de 0 à 10000 attendu"))
    if not _is_nonempty_text(rule.configuration_version):
        diagnostics.append(_refusal("configuration_version", "version opaque non vide attendue"))
    return _evaluation_diagnostics(diagnostics)


def resolve_feature_flag_cohort(
    definition: FeatureFlagDefinition,
    rule: FeatureFlagCohortRule,
    context: FeatureFlagEvaluationContext,
    expected_configuration_version: str,
) -> FeatureFlagCohortResolution:
    """Résout seulement l'appartenance sous une configuration serveur validée.

    Types exacts avant tout attribut/comparaison/hachage. Une définition reste
    validée structurellement : expiration, politique de repli et prérequis ne
    sont pas évalués ici. Une identité opaque n'est jamais normalisée, ni une
    relation de scope inférée. La version attendue vient du snapshot serveur.
    """
    diagnostics: list[Diagnostic] = []
    if type(definition) is not FeatureFlagDefinition:
        diagnostics.append(_refusal("definition", "définition exacte attendue"))
    if type(rule) is not FeatureFlagCohortRule:
        diagnostics.append(_refusal("rule", "règle exacte attendue"))
    if type(context) is not FeatureFlagEvaluationContext:
        diagnostics.append(_refusal("context", "contexte exact attendu"))
    if not _is_nonempty_text(expected_configuration_version):
        diagnostics.append(_refusal("expected_configuration_version", "version attendue opaque non vide requise"))
    if diagnostics:
        return _refused(diagnostics)

    diagnostics.extend(validate_feature_flag_definitions([definition]))
    diagnostics.extend(validate_feature_flag_cohort_rule(rule))
    diagnostics.extend(_validate_context(context))
    if diagnostics:
        return _refused(diagnostics)

    if definition.cohort_key is None or definition.cohort_key != rule.cohort_key:
        diagnostics.append(_refusal("cohort_key", "cohorte déclarée correspondante attendue"))
    if rule.subject_dimension not in definition.targeting_dimensions:
        diagnostics.append(_refusal("subject_dimension", "dimension du sujet déclarée par le fanion requise"))
    if rule.configuration_version != expected_configuration_version:
        diagnostics.append(_refusal("configuration_version", "version canonique attendue incompatible"))
    if diagnostics:
        return _refused(diagnostics)

    identity = getattr(context, _EVALUATION_CONTEXT_FIELDS[rule.subject_dimension])
    if identity is None:
        return _refused([_refusal("identity", "identité canonique présente requise")])
    seed = json.dumps([rule.cohort_key, rule.subject_dimension, identity],
                      ensure_ascii=True, separators=(",", ":")).encode("ascii")
    bucket = int.from_bytes(hashlib.sha256(seed).digest(), "big") % _BUCKET_MODULUS
    status = "MEMBER" if bucket < rule.threshold_basis_points else "NON_MEMBER"
    return FeatureFlagCohortResolution(status, bucket, ())


def evaluate_feature_flag_assignments_with_cohort(
    definition: FeatureFlagDefinition,
    assignments: Sequence[FeatureFlagAssignment],
    context: FeatureFlagEvaluationContext,
    use_kind: str,
    rule: FeatureFlagCohortRule | None,
    expected_configuration_version: str | None,
) -> FeatureFlagEvaluation:
    """Compose réellement la cohorte validée et les primitives existantes.

    Les entrées de cohorte inutilisées ne sont jamais consultées sans clé.
    Sous cohorte, configuration et candidats sont fermés avant toute valeur ;
    l'expiration impose STALE, puis un non-membre non expiré impose ABSENT.
    Une valeur sensible sélectionnée n'est jamais une autorisation positive.
    Le snapshot serveur est une précondition de confiance, non une provenance
    prouvée ; aucune projection de définition ou grammaire parallèle.
    """
    diagnostics: list[Diagnostic] = []
    if type(definition) is not FeatureFlagDefinition:
        diagnostics.append(_refusal("evaluation.definition", "définition exacte attendue"))
    if type(context) is not FeatureFlagEvaluationContext:
        diagnostics.append(_refusal("evaluation.context", "contexte exact attendu"))
    if type(use_kind) is not str or use_kind not in _FALLBACK_USE_KINDS:
        diagnostics.append(_refusal("evaluation.use_kind", "usage reconnu attendu"))
    if diagnostics:
        return FeatureFlagEvaluation("REFUSED", None, _evaluation_diagnostics(diagnostics))
    if definition.cohort_key is None:
        return evaluate_feature_flag_assignments_bounded(definition, assignments, context, use_kind)

    cohort = resolve_feature_flag_cohort(definition, rule, context, expected_configuration_version)
    if cohort.status == "REFUSED":
        return FeatureFlagEvaluation("REFUSED", None, cohort.diagnostics)
    diagnostics.extend(validate_feature_flag_assignments(assignments))
    if definition.prerequisites:
        diagnostics.append(_refusal("evaluation.prerequisites", "prérequis non supportés"))
    if definition.fallback_policy not in _FALLBACK_POLICIES:
        diagnostics.append(_refusal("evaluation.policy", "politique DENY ou DEFAULT attendue"))
    if diagnostics:
        return FeatureFlagEvaluation("REFUSED", None, _evaluation_diagnostics(diagnostics))

    candidate = resolve_feature_flag_assignment(definition, assignments, context)
    incompatible_value = (
        candidate.status == "REFUSED"
        and len(candidate.diagnostics) == 1
        and type(candidate.diagnostics[0]) is Diagnostic
        and candidate.diagnostics[0].element == "feature_flags.evaluation.value"
    )
    if candidate.status == "REFUSED" and not incompatible_value:
        return FeatureFlagEvaluation("REFUSED", None, candidate.diagnostics)
    if candidate.status == "SELECTED" and type(candidate.assignment) is not FeatureFlagAssignment:
        return FeatureFlagEvaluation("REFUSED", None, _evaluation_diagnostics([
            _refusal("evaluation.invariant", "candidat exact attendu")]))
    if candidate.status not in ("SELECTED", "NO_MATCH", "REFUSED"):
        return FeatureFlagEvaluation("REFUSED", None, _evaluation_diagnostics([
            _refusal("evaluation.invariant", "statut de candidat reconnu attendu")]))

    expiry = validate_feature_flag_assignment_expiry(definition, context)
    if expiry:
        fallback = resolve_feature_flag_fallback(definition, use_kind, "STALE")
        return FeatureFlagEvaluation(fallback.status, fallback.value,
                                    _evaluation_diagnostics([*expiry, *fallback.diagnostics]))
    if cohort.status == "NON_MEMBER":
        fallback = resolve_feature_flag_fallback(definition, use_kind, "ABSENT")
        return FeatureFlagEvaluation(fallback.status, fallback.value, fallback.diagnostics)
    if cohort.status != "MEMBER":
        return FeatureFlagEvaluation("REFUSED", None, _evaluation_diagnostics([
            _refusal("evaluation.invariant", "appartenance connue attendue")]))
    if candidate.status == "SELECTED":
        return FeatureFlagEvaluation("SELECTED", candidate.assignment.value, ())
    if candidate.status == "NO_MATCH":
        cause = _classify_no_match(definition, assignments, context,
                                   datetime.fromisoformat(context.as_of))
    else:
        cause = "INVALID"
    fallback = resolve_feature_flag_fallback(definition, use_kind, cause)
    return FeatureFlagEvaluation(fallback.status, fallback.value, fallback.diagnostics)
