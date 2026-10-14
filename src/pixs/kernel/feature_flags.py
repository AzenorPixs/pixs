"""Définitions déclaratives de fanions (tâche 2.1, add-initial-feature-flag-definitions).

Module pur, stdlib uniquement, sans I/O : modèle figé ``FeatureFlagDefinition``
à douze champs canoniques obligatoires sans aucun défaut (seule la valeur de
``cohort_key`` peut être ``None`` explicitement), ensembles bornés déclaratifs
(``FLAG_VALUE_SCHEMAS``, ``FLAG_TARGETING_DIMENSIONS``) et validation en refus
fermé par agrégation (``validate_feature_flag_definitions``) exigée par la spec
``feature-flags`` (« définition versionnée et bornée »).

Les identifiants nus sont contrôlés par ``parse_requirement`` public partagé
(contraintes vides et cible égale à la valeur), sans regex parallèle. Les
diagnostics nomment l'élément et la contrainte en motifs constants, ne
reproduisent jamais une valeur invalide et portent aucun index dépendant de
l'ordre. L'expiration est une déclaration UTC bornée ``YYYY-MM-DDTHH:MM:SS
[.fraction 1 à 6 chiffres](Z | +00:00)`` analysée par ``datetime.fromisoformat``
sans aucune horloge ni environnement. La gate
``validate_feature_flag_assignment_expiry`` compare deux horodatages déjà
validés et l'évaluateur reçoit l'instant de référence ; aucune horloge interne
n'est consultée. Aucun évaluateur runtime complet, aucune persistance, aucune
activation ici.
Les affectations déclaratives ajoutent un modèle figé à huit champs et une
validation structurelle sans résolution, horloge, persistance ou autorisation.
Les helpers et les contrats des définitions antérieures restent inchangés.

"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from .diagnostics import VALIDATE, Diagnostic
from .manifest.semver import parse_requirement

__all__ = [
    "FLAG_TARGETING_DIMENSIONS",
    "FLAG_VALUE_SCHEMAS",
    "FeatureFlagDefinition",
    "validate_feature_flag_definitions",
    "FeatureFlagAssignment",
    "validate_feature_flag_assignments",
    "FeatureFlagEvaluationContext",
    "FeatureFlagResolution",
    "resolve_feature_flag_assignment",
    "FeatureFlagFallback",
    "resolve_feature_flag_fallback",
    "FeatureFlagEvaluation",
    "evaluate_feature_flag_assignments_bounded",
    "validate_feature_flag_assignment_expiry",
]

#: Schémas de valeur reconnus, bornés à l'usage déclaratif requis.
FLAG_VALUE_SCHEMAS = frozenset({"BOOLEAN", "VARIANT"})

#: Dimensions de ciblage canoniques déclaratives (aucun ciblage effectif).
FLAG_TARGETING_DIMENSIONS = frozenset(
    {"INSTALLATION", "ENVIRONMENT", "TENANT", "SCOPE"}
)



@dataclass(frozen=True)
class FeatureFlagDefinition:
    """Déclaration immuable d'un fanion, douze champs canoniques obligatoires."""

    flag_id: str
    flag_version: str
    owner_component: str
    purpose: str
    value_schema: str
    default_value: bool | str
    targeting_dimensions: tuple[str, ...]
    cohort_key: str | None
    prerequisites: tuple[str, ...]
    fallback_policy: str
    expires_at: str
    audit_policy: str


def _refusal(field: str, constraint: str) -> Diagnostic:
    return Diagnostic(
        step=VALIDATE,
        element=f"feature_flags.{field}",
        constraint=constraint,
        message=constraint,
    )


def _is_bare_reference(value: object) -> bool:
    """Vrai seulement pour une chaîne exacte nu : parse_requirement partagé,
    contraintes vides et cible égale à la valeur (points, tirets, chiffres et
    majuscules de la grammaire des composants existants acceptés)."""
    if type(value) is not str:
        return False
    try:
        requirement = parse_requirement(value)
    except ValueError:
        return False
    return requirement.constraints == () and requirement.target_id == value


def _is_namespaced_reference(value: object) -> bool:
    if not _is_bare_reference(value):
        return False
    segments = value.split(".")
    return len(segments) >= 2 and all(segments)


def _is_nonempty_text(value: object) -> bool:
    return type(value) is str and bool(value)


def _all_ascii_digits(text: str) -> bool:
    return bool(text) and all("0" <= character <= "9" for character in text)


def _is_utc_timestamp(value: object) -> bool:
    """Vraie seulement pour ``YYYY-MM-DDTHH:MM:SS[.fraction 1 à 6](Z | +00:00)``.

    Positions et chiffres ASCII vérifiés sans regex, calendrier réel analysé
    par ``datetime.fromisoformat`` ; aucune horloge, aucun environnement,
    aucune comparaison d'expiration.
    """
    if type(value) is not str:
        return False
    if value.endswith("Z"):
        stamp = value[:-1]
    elif value.endswith("+00:00"):
        stamp = value[:-6]
    else:
        return False
    head, separator, fraction = stamp.partition(".")
    if len(head) != 19:
        return False
    if separator and (len(fraction) > 6 or not _all_ascii_digits(fraction)):
        return False
    if not _all_ascii_digits(
        head[0:4]
        + head[5:7]
        + head[8:10]
        + head[11:13]
        + head[14:16]
        + head[17:19]
    ):
        return False
    if (
        head[4] != "-"
        or head[7] != "-"
        or head[10] != "T"
        or head[13] != ":"
        or head[16] != ":"
    ):
        return False
    if (
        int(head[11:13]) > 23
        or int(head[14:16]) > 59
        or int(head[17:19]) > 59
    ):
        return False
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(None)


def _has_duplicates(values: Sequence[object]) -> bool:
    seen: set[str] = set()
    for value in values:
        if type(value) is not str:
            continue
        if value in seen:
            return True
        seen.add(value)
    return False


def _validate_one(definition: FeatureFlagDefinition) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []

    if not _is_namespaced_reference(definition.flag_id):
        refusals.append(_refusal("flag_id", "identifiant namespacé nu attendu"))
    if not _is_nonempty_text(definition.flag_version):
        refusals.append(_refusal("flag_version", "version opaque non vide attendue"))
    if not _is_bare_reference(definition.owner_component):
        refusals.append(_refusal("owner_component", "référence de composant attendu"))
    if not _is_nonempty_text(definition.purpose):
        refusals.append(_refusal("purpose", "finalité prose non vide attendue"))

    schema_known = (
        type(definition.value_schema) is str
        and definition.value_schema in FLAG_VALUE_SCHEMAS
    )
    if not schema_known:
        refusals.append(_refusal("value_schema", "BOOLEAN ou VARIANT attendu"))
    elif definition.value_schema == "BOOLEAN":
        if type(definition.default_value) is not bool:
            refusals.append(_refusal("default_value", "booléen exact attendu"))
    elif not _is_bare_reference(definition.default_value):
        refusals.append(_refusal("default_value", "jeton littéral nu attendu"))

    if type(definition.targeting_dimensions) is not tuple:
        refusals.append(_refusal("targeting_dimensions", "tuple attendu"))
    else:
        unknown = any(
            type(dimension) is not str
            or dimension not in FLAG_TARGETING_DIMENSIONS
            for dimension in definition.targeting_dimensions
        )
        if unknown:
            refusals.append(
                _refusal(
                    "targeting_dimensions",
                    "dimensions canoniques attendues",
                )
            )
        if _has_duplicates(definition.targeting_dimensions):
            refusals.append(
                _refusal("targeting_dimensions", "dimensions sans doublon attendues")
            )

    if definition.cohort_key is not None and not _is_bare_reference(
        definition.cohort_key
    ):
        refusals.append(_refusal("cohort_key", "référence littérale nue attendue"))

    if type(definition.prerequisites) is not tuple:
        refusals.append(_refusal("prerequisites", "tuple attendu"))
    else:
        invalid_prerequisite = any(
            not _is_bare_reference(prerequisite)
            for prerequisite in definition.prerequisites
        )
        if invalid_prerequisite:
            refusals.append(
                _refusal("prerequisites", "références de prérequis attendues")
            )
        if _has_duplicates(definition.prerequisites):
            refusals.append(
                _refusal("prerequisites", "prérequis sans doublon attendus")
            )

    if not _is_bare_reference(definition.fallback_policy):
        refusals.append(_refusal("fallback_policy", "politique déclarative attendue"))
    if not _is_utc_timestamp(definition.expires_at):
        refusals.append(
            _refusal(
                "expires_at",
                "horodatage UTC RFC3339 borné attendu",
            )
        )
    if not _is_bare_reference(definition.audit_policy):
        refusals.append(_refusal("audit_policy", "politique déclarative attendue"))

    return refusals


def validate_feature_flag_definitions(
    definitions: Sequence[FeatureFlagDefinition],
) -> tuple[Diagnostic, ...]:
    """Valide un lot de définitions en refus fermé agrégé, déterministe et sans écho."""
    if type(definitions) is not list and type(definitions) is not tuple:
        return (_refusal("conteneur", "liste ou tuple attendu"),)

    refusals: list[Diagnostic] = []
    declared_flag_ids: list[str] = []
    for item in definitions:
        if type(item) is not FeatureFlagDefinition:
            refusals.append(_refusal("entree", "définition de fanion exacte attendue"))
            continue
        refusals.extend(_validate_one(item))
        if type(item.flag_id) is str:
            declared_flag_ids.append(item.flag_id)

    if _has_duplicates(declared_flag_ids):
        refusals.append(_refusal("flag_id", "drapeau déclaré une seule fois"))

    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        unique[(diagnostic.element, diagnostic.constraint, diagnostic.message)] = (
            diagnostic
        )
    return tuple(unique[key] for key in sorted(unique))


@dataclass(frozen=True)
class FeatureFlagAssignment:
    """Affectation déclarative bornée d'un fanion, huit champs obligatoires."""

    flag_id: str
    selector: str
    selector_value: str
    value: bool | str
    valid_from: str
    valid_until: str
    configuration_version: str
    updated_by: str


def _validate_one_assignment(assignment: FeatureFlagAssignment) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []

    if not _is_namespaced_reference(assignment.flag_id):
        refusals.append(
            _refusal("assignments.flag_id", "identifiant namespacé nu attendu")
        )
    if type(assignment.selector) is not str or (
        assignment.selector not in FLAG_TARGETING_DIMENSIONS
    ):
        refusals.append(
            _refusal(
                "assignments.selector",
                "dimension canonique unique attendue",
            )
        )
    if not _is_nonempty_text(assignment.selector_value):
        refusals.append(
            _refusal(
                "assignments.selector_value",
                "valeur de sélecteur opaque non vide attendue",
            )
        )

    if type(assignment.value) is not bool and not _is_bare_reference(assignment.value):
        refusals.append(
            _refusal(
                "assignments.value",
                "booléen exact ou jeton littéral nu attendu",
            )
        )

    valid_from_ok = _is_utc_timestamp(assignment.valid_from)
    valid_until_ok = _is_utc_timestamp(assignment.valid_until)
    if not valid_from_ok:
        refusals.append(
            _refusal(
                "assignments.valid_from",
                "horodatage UTC RFC3339 borné attendu",
            )
        )
    if not valid_until_ok:
        refusals.append(
            _refusal(
                "assignments.valid_until",
                "horodatage UTC RFC3339 borné attendu",
            )
        )
    if valid_from_ok and valid_until_ok and not (
        datetime.fromisoformat(assignment.valid_from)
        < datetime.fromisoformat(assignment.valid_until)
    ):
        refusals.append(
            _refusal(
                "assignments.valid_window",
                "fenêtre structurelle strictement positive attendue",
            )
        )

    if not _is_nonempty_text(assignment.configuration_version):
        refusals.append(
            _refusal(
                "assignments.configuration_version",
                "version de configuration opaque non vide attendue",
            )
        )
    if not _is_nonempty_text(assignment.updated_by):
        refusals.append(
            _refusal(
                "assignments.updated_by",
                "référence opaque non vide attendue",
            )
        )

    return refusals


def validate_feature_flag_assignments(
    assignments: Sequence[FeatureFlagAssignment],
) -> tuple[Diagnostic, ...]:
    """Valide un lot d'affectations en refus fermé agrégé, déterministe et sans écho.

    Aucun évaluateur de priorité, de cohorte, de fenêtre effective, aucune
    liaison à une définition, aucune unicité ni chevauchement n'est décidé ici.
    """
    if type(assignments) is not list and type(assignments) is not tuple:
        return (_refusal("assignments.conteneur", "liste ou tuple attendu"),)

    refusals: list[Diagnostic] = []
    for item in assignments:
        if type(item) is not FeatureFlagAssignment:
            refusals.append(
                _refusal("assignments.entree", "affectation de fanion exacte attendue")
            )
            continue
        refusals.extend(_validate_one_assignment(item))

    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        unique[(diagnostic.element, diagnostic.constraint, diagnostic.message)] = (
            diagnostic
        )
    return tuple(unique[key] for key in sorted(unique))


#: Niveaux de priorité du ciblage : ``INSTALLATION`` et ``ENVIRONMENT`` réunis
#: au même niveau général, puis ``TENANT``, puis ``SCOPE``. Aucun ordre relatif
#: n'est inventé entre les deux dimensions générales.
_EVALUATION_LEVELS = {
    "INSTALLATION": 0,
    "ENVIRONMENT": 0,
    "TENANT": 1,
    "SCOPE": 2,
}

#: Champs de contexte correspondant à chaque dimension canonique déclarée.
_EVALUATION_CONTEXT_FIELDS = {
    "INSTALLATION": "installation",
    "ENVIRONMENT": "environment",
    "TENANT": "tenant",
    "SCOPE": "scope",
}

#: Domaine borné du statut d'une résolution.
_STATUS_SELECTED = "SELECTED"
_STATUS_NO_MATCH = "NO_MATCH"
_STATUS_REFUSED = "REFUSED"


@dataclass(frozen=True)
class FeatureFlagEvaluationContext:
    """Contexte déclaratif d'évaluation, cinq champs obligatoires sans défaut.

    Chaque dimension reçoit une chaîne exacte non vide opaque ou ``None`` ;
    ``as_of`` est un horodatage UTC au format déjà borné par ``_is_utc_timestamp``.
    Aucune horloge système, aucun environnement, aucune relation de périmètre :
    ``scope`` sans ``tenant`` est refusé comme incohérence de forme uniquement.
    """

    installation: str | None
    environment: str | None
    tenant: str | None
    scope: str | None
    as_of: str


@dataclass(frozen=True)
class FeatureFlagResolution:
    """Résultat borné d'une résolution de candidat de ciblage.

    ``status`` vaut ``SELECTED``, ``NO_MATCH`` ou ``REFUSED`` ; ``assignment``
    n'est posé que sur ``SELECTED`` ; ``diagnostics`` est trié, dédupliqué et ne
    reproduit aucune valeur. Ce résultat n'est pas une évaluation runtime
    complète : il ne tranche ni repli, ni expiration du fanion, ni cycle de vie,
    ni permission, ni mutation, ni cohorte, ni prérequis, ni persistance.
    """

    status: str
    assignment: FeatureFlagAssignment | None
    diagnostics: tuple[Diagnostic, ...]


def _evaluation_diagnostics(refusals: list[Diagnostic]) -> tuple[Diagnostic, ...]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for diagnostic in refusals:
        unique[(diagnostic.element, diagnostic.constraint, diagnostic.message)] = (
            diagnostic
        )
    return tuple(unique[key] for key in sorted(unique))


def _validate_context(context: FeatureFlagEvaluationContext) -> list[Diagnostic]:
    refusals: list[Diagnostic] = []
    for field in ("installation", "environment", "tenant", "scope"):
        value = getattr(context, field)
        if value is not None and not _is_nonempty_text(value):
            refusals.append(
                _refusal(
                    f"evaluation.{field}",
                    "texte opaque non vide ou None attendu",
                )
            )
    if not _is_utc_timestamp(context.as_of):
        refusals.append(
            _refusal("evaluation.as_of", "horodatage UTC RFC3339 borné attendu")
        )
    if getattr(context, "scope") is not None and getattr(context, "tenant") is None:
        refusals.append(
            _refusal("evaluation.scope", "scope sans tenant refusé en forme")
        )
    return refusals


def _is_candidate(
    definition: FeatureFlagDefinition,
    assignment: FeatureFlagAssignment,
    context: FeatureFlagEvaluationContext,
    reference: datetime,
) -> bool:
    if assignment.flag_id != definition.flag_id:
        return False
    if assignment.selector not in definition.targeting_dimensions:
        return False
    field = _EVALUATION_CONTEXT_FIELDS[assignment.selector]
    context_value = getattr(context, field)
    if context_value is None or assignment.selector_value != context_value:
        return False
    return (
        datetime.fromisoformat(assignment.valid_from)
        <= reference
        < datetime.fromisoformat(assignment.valid_until)
    )


def resolve_feature_flag_assignment(
    definition: FeatureFlagDefinition,
    assignments: Sequence[FeatureFlagAssignment],
    context: FeatureFlagEvaluationContext,
) -> FeatureFlagResolution:
    """Retient le candidat d'affectation applicable, sans aucun effet.

    La résolution ferme d'abord les types exacts avant toute itération, accès
    d'attribut, comparaison ou hachage, délègue aux validateurs et helpers
    existants, n'observe que les dimensions déclarées par la définition, compare
    exactement ``flag_id`` et ``selector_value``, applique la fenêtre technique
    semi-ouverte ``valid_from <= as_of < valid_until`` sur l'instant injecté, puis
    retient le niveau le plus spécifique disponible. Plusieurs candidats au même
    meilleur niveau sont refusés, même à valeurs égales : la décision ne dépend
    jamais de l'ordre du lot. Aucun candidat donne ``NO_MATCH`` ; un candidat
    unique dont la valeur est cohérente avec le schéma de la définition donne
    ``SELECTED``. Une entrée invalide donne ``REFUSED`` sans affectation. Aucune
    cohorte, aucun prérequis, aucun repli, aucune expiration du fanion, aucune
    permission et aucune persistance ne sont évalués ; le résultat n'est pas une
    évaluation runtime complète et ne prétend pas satisfaire R2 entièrement.
    """
    if type(definition) is not FeatureFlagDefinition:
        return FeatureFlagResolution(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [_refusal("evaluation.definition", "définition exacte attendue")]
            ),
        )
    if type(context) is not FeatureFlagEvaluationContext:
        return FeatureFlagResolution(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [_refusal("evaluation.contexte", "contexte exact attendu")]
            ),
        )

    refusals: list[Diagnostic] = list(validate_feature_flag_definitions([definition]))
    refusals.extend(validate_feature_flag_assignments(assignments))
    refusals.extend(_validate_context(context))
    if refusals:
        return FeatureFlagResolution(
            _STATUS_REFUSED, None, _evaluation_diagnostics(refusals)
        )

    reference = datetime.fromisoformat(context.as_of)
    candidates = [
        assignment
        for assignment in assignments
        if _is_candidate(definition, assignment, context, reference)
    ]
    if not candidates:
        return FeatureFlagResolution(_STATUS_NO_MATCH, None, ())

    best_level = max(_EVALUATION_LEVELS[assignment.selector] for assignment in candidates)
    best = [
        assignment
        for assignment in candidates
        if _EVALUATION_LEVELS[assignment.selector] == best_level
    ]
    if len(best) != 1:
        return FeatureFlagResolution(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [
                    _refusal(
                        "evaluation.candidats",
                        "candidat unique au meilleur niveau attendu",
                    )
                ]
            ),
        )

    selected = best[0]
    if definition.value_schema == "BOOLEAN":
        compatible = type(selected.value) is bool
    else:
        compatible = _is_bare_reference(selected.value)
    if not compatible:
        return FeatureFlagResolution(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [
                    _refusal(
                        "evaluation.value",
                        "schéma de valeur cohérent avec la définition attendu",
                    )
                ]
            ),
        )

    return FeatureFlagResolution(_STATUS_SELECTED, selected, ())


@dataclass(frozen=True)
class FeatureFlagFallback:
    """Issue bornée de l'application déclarative du repli R3.

    ``status`` vaut ``DEFAULT`` ou ``REFUSED`` ; ``value`` n'est posée que sur
    ``DEFAULT`` ; ``diagnostics`` est trié, dédupliqué et ne reproduit aucune
    valeur. Réservée à un appelant serveur canonique de confiance : la primitive
    ne prouve aucune provenance, ne constate aucun échec, ne détecte aucune
    absence, invalidité ni péremption, ne retient aucun candidat, n'évalue ni
    cohorte, prérequis, persistance, cache, administration, audit, cycle de vie
    ni horloge, et n'expose ni permission positive ni HTTP, frontend ou CLI.
    La réévaluation globale par le frontend ou le backend reste hors de portée.
    """

    status: str
    value: bool | str | None
    diagnostics: tuple[Diagnostic, ...]


#: Statut d'application du repli, distinct des statuts de résolution de candidat.
_STATUS_DEFAULT = "DEFAULT"

#: Usages déclarés reconnus à l'exécution, sans normalisation ni alias.
_FALLBACK_USE_KINDS = frozenset(
    {"NON_SENSITIVE", "PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT"}
)

#: Usages pour lesquels l'échec est fermé quelle que soit la politique déclarée.
_FALLBACK_SENSITIVE_USE_KINDS = frozenset(
    {"PERMISSION", "MUTATION", "PROTECTED_DATA", "CONTRACT"}
)

#: Causes d'échec nommées par R3, constatées par l'appelant et jamais détectées.
_FALLBACK_FAILURE_KINDS = frozenset({"ABSENT", "INVALID", "STALE"})

#: Vocabulaire d'exécution du repli, borné aux deux politiques déclaratives.
_FALLBACK_POLICIES = frozenset({"DENY", "DEFAULT"})


def resolve_feature_flag_fallback(
    definition: FeatureFlagDefinition,
    use_kind: str,
    failure_kind: str,
) -> FeatureFlagFallback:
    """Applique le repli R3 déclaré à un échec déjà constaté, sans aucun effet.

    Les types sont fermés par identité exacte avant tout accès d'attribut, toute
    itération, toute comparaison et tout hachage, et aucune valeur invalide n'est
    échoée. La définition est validée par ``validate_feature_flag_definitions``
    et les diagnostics sont triés et dédupliqués par ``_evaluation_diagnostics`` ;
    aucune grammaire, aucun horodatage et aucun contrôle de référence ne sont
    dupliqués. ``DENY`` refuse sans valeur, des diagnostics pouvant rester vides ;
    ``DEFAULT`` applique la ``default_value`` validée de la définition uniquement
    pour un usage ``NON_SENSITIVE``, en conservant ``False`` pour ``BOOLEAN`` et
    un jeton littéral pour ``VARIANT`` ; tout usage sensible est refusé quelle que
    soit la politique déclarée ; toute référence de repli opaque héritée, inconnue
    ou incompatible est refusée sans conversion en alias, sans ``casefold``,
    ``strip`` ni normalisation. La classification et le constat d'échec restent la
    responsabilité de l'appelant serveur canonique, qui contrôle aussi ses propres
    dépendances et autorisations indépendamment du repli.
    """
    refusals: list[Diagnostic] = []

    if type(definition) is not FeatureFlagDefinition:
        refusals.append(_refusal("fallback.definition", "définition exacte attendue"))
    if type(use_kind) is not str or use_kind not in _FALLBACK_USE_KINDS:
        refusals.append(
            _refusal("fallback.use_kind", "usage déclaré reconnu attendu")
        )
    if type(failure_kind) is not str or (
        failure_kind not in _FALLBACK_FAILURE_KINDS
    ):
        refusals.append(
            _refusal("fallback.failure_kind", "cause d'échec nommée attendue")
        )
    if refusals:
        return FeatureFlagFallback(
            _STATUS_REFUSED, None, _evaluation_diagnostics(refusals)
        )

    declared = list(validate_feature_flag_definitions([definition]))
    if declared:
        return FeatureFlagFallback(
            _STATUS_REFUSED, None, _evaluation_diagnostics(declared)
        )

    policy = definition.fallback_policy
    if policy not in _FALLBACK_POLICIES:
        return FeatureFlagFallback(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [_refusal("fallback.policy", "politique d'exécution bornée attendue")]
            ),
        )
    if policy == "DENY":
        return FeatureFlagFallback(_STATUS_REFUSED, None, ())
    if use_kind in _FALLBACK_SENSITIVE_USE_KINDS:
        return FeatureFlagFallback(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [
                    _refusal(
                        "fallback.sensible",
                        "repli refusé pour un usage sensible",
                    )
                ]
            ),
        )
    return FeatureFlagFallback(_STATUS_DEFAULT, definition.default_value, ())


@dataclass(frozen=True)
class FeatureFlagEvaluation:
    """Issue bornée de l'évaluation composée des affectations d'un fanion.

    ``status`` vaut ``SELECTED``, ``DEFAULT`` ou ``REFUSED`` ; ``value`` porte la
    valeur retenue sur ``SELECTED`` ou le défaut validé appliqué sur ``DEFAULT``
    et n'est jamais posée sur ``REFUSED`` ; ``diagnostics`` est trié, dédupliqué
    et ne reproduit aucune valeur. Réservée à un appelant serveur canonique de
    confiance : cette composition n'en prouve pas la provenance, une valeur
    retenue n'est jamais une permission positive, et l'appelant conserve
    l'évaluation de ses autorisations, dépendances et contrats. Elle ne tranche
    ni cycle de vie de la définition, ni cohorte, ni prérequis, ni persistance ;
    l'expiration de définition est tranchée par la gate et transmise au repli
    comme cause ``STALE``, les causes ``ABSENT`` et ``INVALID`` restant
    constatées par l'appelant ou par le résolveur.
    """

    status: str
    value: bool | str | None
    diagnostics: tuple[Diagnostic, ...]


def _identity_matches(
    definition: FeatureFlagDefinition,
    assignment: FeatureFlagAssignment,
    context: FeatureFlagEvaluationContext,
) -> bool:
    if assignment.flag_id != definition.flag_id:
        return False
    if assignment.selector not in definition.targeting_dimensions:
        return False
    field = _EVALUATION_CONTEXT_FIELDS[assignment.selector]
    context_value = getattr(context, field)
    return context_value is not None and assignment.selector_value == context_value


def _classify_no_match(
    definition: FeatureFlagDefinition,
    assignments: Sequence[FeatureFlagAssignment],
    context: FeatureFlagEvaluationContext,
    reference: datetime,
) -> str:
    """Classe un ``NO_MATCH`` en ``STALE`` ou ``ABSENT`` pour le repli R3.

    ``STALE`` seulement si une identité correspondante sur une dimension déclarée
    est réellement périmée (``valid_until <= as_of``) ; une fenêtre postérieure
    (``as_of < valid_from``) n'est pas une valeur périmée et reste ``ABSENT``.
    Un lot mêlant identité périmée et identité future sans candidat actif est
    ``STALE`` : choix technique CGPT, la cause périmée est observée et le repli
    produit est identique pour ``ABSENT`` et ``STALE`` à définition, usage et
    politique donnés, donc aucune décision observable n'en dépend. Les bornes
    sont déjà validées UTC et comparées par ``datetime.fromisoformat``, sans
    horloge, sans environnement et sans grammaire horodatage nouvelle.
    """
    for assignment in assignments:
        if not _identity_matches(definition, assignment, context):
            continue
        if datetime.fromisoformat(assignment.valid_until) <= reference:
            return "STALE"
    return "ABSENT"


def validate_feature_flag_assignment_expiry(
    definition: FeatureFlagDefinition,
    context: FeatureFlagEvaluationContext,
) -> tuple[Diagnostic, ...]:
    """Refuse toute nouvelle affectation sur une définition expirée, sans effet.

    Réservée à un appelant serveur canonique de confiance : l'instant de
    référence vient de ``context.as_of`` et aucune horloge interne n'est
    consultée. Les types sont fermés par identité exacte avant tout accès
    d'attribut, puis la validation est déléguée à
    ``validate_feature_flag_definitions`` et ``_validate_context`` : une entrée
    invalide ne reçoit aucune décision d'expiration. La comparaison
    ``expires_at <= as_of`` par ``datetime.fromisoformat`` des deux horodatages
    déjà validés ne produit, en cas d'expiration, qu'un diagnostic constant
    trié, dédupliqué et sans reproduction de valeur. La gate ne retourne ni
    valeur, ni statut, ni repli : l'absence de diagnostic est le seul signal et
    ne vaut aucune admission, autorisation ni persistance.
    """
    if type(definition) is not FeatureFlagDefinition:
        return _evaluation_diagnostics(
            [_refusal("expiry.definition", "définition exacte attendue")]
        )
    if type(context) is not FeatureFlagEvaluationContext:
        return _evaluation_diagnostics(
            [_refusal("expiry.contexte", "contexte exact attendu")]
        )

    refusals = list(validate_feature_flag_definitions([definition]))
    refusals.extend(_validate_context(context))
    if refusals:
        return _evaluation_diagnostics(refusals)

    if datetime.fromisoformat(definition.expires_at) <= datetime.fromisoformat(
        context.as_of
    ):
        return _evaluation_diagnostics(
            [
                _refusal(
                    "expiry.expires_at",
                    "expiration de définition opposée à l'instant de référence serveur",
                )
            ]
        )
    return ()


def evaluate_feature_flag_assignments_bounded(
    definition: FeatureFlagDefinition,
    assignments: Sequence[FeatureFlagAssignment],
    context: FeatureFlagEvaluationContext,
    use_kind: str,
) -> FeatureFlagEvaluation:
    """Compose la résolution C2 et le repli R3 d'un lot d'affectations, sans effet.

    L'ordre est celui du design approuvé : fermeture des types par identité exacte
    avant tout accès d'attribut, itération, ``__eq__`` ou ``__hash__`` ; validations
    déléguées à ``validate_feature_flag_definitions``,
    ``validate_feature_flag_assignments`` et ``_validate_context`` ; refus terminal
    sans repli pour toute entrée, configuration ou ambiguïté invalide ; profil
    borné refusant ``cohort_key`` déclarée ou prérequis non vide sans ``DEFAULT`` ;
    gate de politique bornée à ``DENY`` et ``DEFAULT`` appliquée avant tout appel
    au résolveur, donc avant la moindre restitution d'une valeur, sans ``casefold``,
    ``strip`` ni alias implicite ; puis ``resolve_feature_flag_assignment`` appelé
    inchangé. ``SELECTED`` restitue la valeur de l'affectation retenue, ``False``
    pour ``BOOLEAN`` et un jeton littéral pour ``VARIANT``, pour tout usage y compris sensible, sans jamais
    valoir permission. ``NO_MATCH`` est classé par ``_classify_no_match`` et,
    comme un refus machine d'incompatibilité de valeur unique
    ``feature_flags.evaluation.value``, transmis à ``resolve_feature_flag_fallback``.
    Tout autre refus du résolveur reste terminal. La gate
    ``validate_feature_flag_assignment_expiry`` est alors consultée : une
    définition expirée fait traiter ``SELECTED``, ``NO_MATCH`` et refus
    d'incompatibilité de valeur comme la cause ``STALE`` du repli, avec son
    diagnostic fusionné, sans jamais restituer la valeur de l'affectation. Aucun
    texte de diagnostic humain n'est analysé, aucune horloge, E/S, persistance,
    cache, administration, audit ni exposition HTTP, frontend ou CLI ; les
    garanties globales R2 et R3 ne sont pas livrées.
    """
    refusals: list[Diagnostic] = []
    if type(definition) is not FeatureFlagDefinition:
        refusals.append(
            _refusal("evaluation_bounded.definition", "définition exacte attendue")
        )
    if type(context) is not FeatureFlagEvaluationContext:
        refusals.append(
            _refusal("evaluation_bounded.contexte", "contexte exact attendu")
        )
    if type(use_kind) is not str or use_kind not in _FALLBACK_USE_KINDS:
        refusals.append(
            _refusal("evaluation_bounded.use_kind", "usage déclaré reconnu attendu")
        )
    if refusals:
        return FeatureFlagEvaluation(
            _STATUS_REFUSED, None, _evaluation_diagnostics(refusals)
        )

    refusals = list(validate_feature_flag_definitions([definition]))
    refusals.extend(validate_feature_flag_assignments(assignments))
    refusals.extend(_validate_context(context))
    if refusals:
        return FeatureFlagEvaluation(
            _STATUS_REFUSED, None, _evaluation_diagnostics(refusals)
        )

    if definition.cohort_key is not None or definition.prerequisites != ():
        return FeatureFlagEvaluation(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [
                    _refusal(
                        "evaluation_bounded.configuration",
                        "cohorte ou prérequis non supportés",
                    )
                ]
            ),
        )

    if definition.fallback_policy not in _FALLBACK_POLICIES:
        return FeatureFlagEvaluation(
            _STATUS_REFUSED,
            None,
            _evaluation_diagnostics(
                [
                    _refusal(
                        "evaluation_bounded.policy",
                        "politique d'exécution bornée attendue",
                    )
                ]
            ),
        )

    resolution = resolve_feature_flag_assignment(definition, assignments, context)

    if resolution.status == _STATUS_SELECTED:
        selected = resolution.assignment
        if type(selected) is not FeatureFlagAssignment:
            return FeatureFlagEvaluation(
                _STATUS_REFUSED,
                None,
                _evaluation_diagnostics(
                    [
                        _refusal(
                            "evaluation_bounded.invariant",
                            "affectation sélectionnée exacte attendue",
                        )
                    ]
                ),
            )
        expiry = validate_feature_flag_assignment_expiry(definition, context)
        if expiry:
            fallback = resolve_feature_flag_fallback(definition, use_kind, "STALE")
            return FeatureFlagEvaluation(
                fallback.status,
                fallback.value,
                _evaluation_diagnostics([*expiry, *fallback.diagnostics]),
            )
        return FeatureFlagEvaluation(_STATUS_SELECTED, selected.value, ())

    if resolution.status == _STATUS_NO_MATCH:
        expiry = validate_feature_flag_assignment_expiry(definition, context)
        if expiry:
            cause = "STALE"
        else:
            cause = _classify_no_match(
                definition,
                assignments,
                context,
                datetime.fromisoformat(context.as_of),
            )
        fallback = resolve_feature_flag_fallback(definition, use_kind, cause)
        return FeatureFlagEvaluation(
            fallback.status,
            fallback.value,
            _evaluation_diagnostics([*expiry, *fallback.diagnostics]),
        )

    diagnostics = resolution.diagnostics
    incompatible_value = (
        len(diagnostics) == 1
        and type(diagnostics[0]) is Diagnostic
        and diagnostics[0].element == "feature_flags.evaluation.value"
    )
    if incompatible_value:
        expiry = validate_feature_flag_assignment_expiry(definition, context)
        cause = "STALE" if expiry else "INVALID"
        fallback = resolve_feature_flag_fallback(definition, use_kind, cause)
        return FeatureFlagEvaluation(
            fallback.status,
            fallback.value,
            _evaluation_diagnostics([*expiry, *fallback.diagnostics]),
        )
    return FeatureFlagEvaluation(_STATUS_REFUSED, None, diagnostics)
