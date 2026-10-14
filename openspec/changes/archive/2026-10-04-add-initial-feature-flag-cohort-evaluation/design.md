# Design — composition de cohorte sans projection de définition

## API et compatibilité

Nouvelle fonction à six paramètres obligatoires, retournant le `FeatureFlagEvaluation` public existant. Le module de cohorte importe les modèles et helpers de l'ancien module ; l'ancien module n'importe pas la cohorte : aucun cycle. Les quatre anciens exports, modèles et fonctions de cohorte conservent leurs contrats ; le seul export ajouté est la nouvelle fonction. Aucun autre fichier existant n'est modifié.

Les types exacts de définition, contexte et usage sont fermés avant attributs ou hooks. Si la définition exacte ne déclare aucune cohorte, déléguer l'évaluation à `evaluate_feature_flag_assignments_bounded` inchangé ; ne lire ni règle ni version de cohorte inutilisées, même sous objets à trappes. L'ancienne validation de définition, affectations, contexte et profil reste alors la référence.

## Cohorte déclarée : ordre des portes

1. Résoudre la cohorte réellement avec `resolve_feature_flag_cohort` : types, définition/règle/contexte, clé, dimension déclarée, identité et version attendue. Un refus empêche toute sélection et n'est pas transformé en repli de configuration.
2. Valider les affectations structurellement par le validateur existant. Refuser les prérequis non supportés et toute politique hors DENY/DEFAULT. Aucun callback, comparaison humaine de diagnostic ou grammaire nouvelle.
3. `resolve_feature_flag_assignment` reste le résolveur C2 de candidats : il valide et sélectionne sans contrôler lui-même la cohorte. Refus d'ambiguïté/configuration terminal ; seul refus d'incompatibilité de valeur unique par l'élément machine `feature_flags.evaluation.value` autorise un repli. Vérifier l'invariant du candidat exact avant restitution.
4. Consulter `validate_feature_flag_assignment_expiry` : une définition expirée impose STALE avec diagnostic d'expiration fusionné au repli, pour membre ou non membre. R3 s'applique avant toute restitution ; aucune lecture d'horloge. Cette priorité conserve l'expiration déjà livrée, les entrées et candidats invalides restant terminaux.
5. Sur définition non expirée et sujet NON_MEMBER, exclure la valeur affectée et appliquer `resolve_feature_flag_fallback(..., "ABSENT")`, conformément à R2.
6. Sur MEMBER non expiré, conserver la valeur SELECTED y compris False/VARIANT et usage sensible, sans autorisation positive. NO_MATCH utilise `_classify_no_match` inchangé avec l'instant UTC fourni ; incompatibilité unique de valeur passe par INVALID ; autres refus restent terminaux.

Aucune neutralisation de `cohort_key`, aucun `dataclasses.replace` ou copie de définition pour contourner l'ancien profil. Réutiliser directement les validateurs, résolveurs et repli ; diagnostics constants triés/dédupliqués, sans écho ni mutation. La version de règle est vérifiée contre le snapshot canonique attendu ; aucune relation d'ordre entre versions opaques d'affectation n'est inventée. La provenance et la cohérence globale des affectations restent une précondition de confiance de l'appelant, pas une garantie R4 livrée.

## Validation ciblée

Conserver les 106 tests et les anciens corps/classes du module de cohorte. Matrice booléen/variant, membre/non membre, DENY/DEFAULT et cinq usages, cause ABSENT hors cohorte, STALE sous expiration avant/égal/après, INVALID pour valeur incompatible membre, NO_MATCH fenêtre périmée/future, ambigüité et politiques/prérequis refusés, règle/identité/version invalides avant toute valeur, fanion sans cohorte ignorant les entrées inutilisées hostiles, callbacks zéro et non-mutation. Des espions avec wraps sur les vrais résolveurs vérifient les causes sans remplacer la logique métier.

Intégration dans un enfant frais, finder Django/SQL/réseau et douze mocks causaux réellement sondés avant import puis remis à zéro, valeurs et refus réels suivis de compteurs zéro. Aucun I/O réel des sondes, aucune horloge immuable patchée, aucune donnée secrète ou base. Les imports peuvent lire normalement leurs sources via io.
