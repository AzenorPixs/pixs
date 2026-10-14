# Design — gate temporelle d'expiration de définition

## Contrat de la gate

`validate_feature_flag_assignment_expiry(definition, context)` retourne un `tuple[Diagnostic, ...]` et rien d'autre : aucune valeur, aucun statut, aucun repli, aucune admission. Le nom reflète l'usage — refuser toute **nouvelle** affectation sur une définition expirée (`TECHNICAL.md:383`) — et la gate n'examine aucune candidate : la fenêtre propre d'une affectation relève déjà de `validate_feature_flag_assignments` et de `resolve_feature_flag_assignment`.

Ordre interne :
1. `type(definition) is not FeatureFlagDefinition` ou `type(context) is not FeatureFlagEvaluationContext` : diagnostics constants `feature_flags.expiry.definition` et `feature_flags.expiry.contexte`, aucune lecture d'attribut.
2. Validation déléguée : `validate_feature_flag_definitions([definition])` puis `_validate_context(context)`. Toute refus est retourné tel quel, trié et dédupliqué par `_evaluation_diagnostics` : une entrée ou définition invalide ne reçoit **aucune** décision d'expiration et ne produit jamais de laisser-passer.
3. Décision : `datetime.fromisoformat(definition.expires_at) <= datetime.fromisoformat(context.as_of)` produit le diagnostic constant `feature_flags.expiry.expires_at` de contrainte « expiration de définition opposée à l'instant de référence serveur », sans reproduction d'aucun horodatage ni identifiant ; sinon tuple vide.

Aucune grammaire horodatage, aucune analyse UTC, aucun domaine de statut, aucune classe ou dataclass nouvelle n'est introduit : les bornes et `as_of` sont déjà validés par le helper `_is_utc_timestamp` et le contexte. Aucune horloge, aucun `datetime.now`, aucun environnement, aucune E/S.

## Intégration dans la composition bornée

La gate est appelée après les refus terminaux existants (types, validateurs, profil cohorte/prérequis, politique hors `DENY`/`DEFAULT`) et après `resolve_feature_flag_assignment`, donc le refus terminal sans valeur est toujours décidé avant qu'une expiration ne puisse autoriser quoi que ce soit :

- `SELECTED` : si la gate émet un diagnostic, la valeur de l'affectation n'est **pas** restituée ; la décision est déléguée à `resolve_feature_flag_fallback(definition, use_kind, "STALE")` et le diagnostic d'expiration est fusionné aux diagnostics du repli. Sous `DENY` ou pour un usage sensible, le résultat est `REFUSED` sans valeur ; sous `DEFAULT` et `NON_SENSITIVE`, `default_value` validée est appliquée (`False` et jeton `VARIANT` conservés) avec le diagnostic d'expiration joint.
- `NO_MATCH` : comportement de classification inchangé, puis, si la gate émet un diagnostic, la cause retenue pour le repli est `STALE` et le diagnostic d'expiration est fusionné. La distinction `ABSENT`/`STALE` de `_classify_no_match` reste inchangée pour les définitions non expirées.
- `REFUSED` d'incompatibilité de valeur reconnu par le seul champ machine `feature_flags.evaluation.value` : le repli `INVALID` existant est conservé hors expiration ; sur définition expirée, la cause est `STALE` et le diagnostic d'expiration est joint.
- Tout autre `REFUSED` (`evaluation_bounded.*`, `evaluation.candidats`, `evaluation.definition`, `evaluation.contexte`, `evaluation.invariant`, diagnostics des validateurs) : terminal, `value` `None`, diagnostics inchangés, la gate ne transforme jamais un refus terminal en valeur.

Les refus terminaux sont donc préservés même sur définition expirée : cohorte déclarée, prérequis non vides, politique héritée inconnue, ambiguïté de candidats et entrées invalides restent refusés avec leurs diagnostics propres.

## Docstrings à corriger localement

- En-tête du module (l. 14-17) : la mention « sans aucune … décision d'expiration » devient « la gate `validate_feature_flag_assignment_expiry` compare deux horodatages déjà validés et l'évaluateur reçoit l'instant de référence ; aucune horloge n'est consultée ».
- `FeatureFlagEvaluation` (l. 723-734) : « Elle ne tranche ni expiration ni cycle de vie » est réduit au cycle de vie, à la cohorte, aux prérequis et à la persistance ; l'expiration de définition est désormais tranchée par la gate et le repli.
- `evaluate_feature_flag_assignments_bounded` (l. 787-807) : la phrase « aucune comparaison de `expires_at` de la définition » est remplacée par la description de la gate et de ses effets, sans changer le reste.
- `FeatureFlagResolution`, `resolve_feature_flag_assignment`, `FeatureFlagFallback` et `resolve_feature_flag_fallback` restent exacts : le résolveur ne tranche toujours ni expiration ni repli, et le repli continue de recevoir une cause constatée par l'appelant, jamais de la détecter.

## Choix documentés, aucune norme nouvelle

- Bord inclusif `expires_at <= as_of` : retenu par la norme déjà approuvée (`spec.md:34` « inférieur ou égal », `TECHNICAL.md:383` même formulation) ; un instant de référence strictement antérieur à l'expiration laisse la définition valide.
- Le diagnostic d'expiration est joint au repli plutôt que de remplacer sa sémantique : R3 impose la politique déclarée, pas un statut supplémentaire ; les statuts restent `SELECTED`, `DEFAULT`, `REFUSED`.
- La gate ne retourne pas de booléen : l'absence de diagnostic est le seul signal, pour ne créer aucune autorisation positive implicite.
- `equivalence Z` et `+00:00` provient du helper déjà validé ; aucune comparaison naïve de chaînes n'est ajoutée.

## Tests et limites

Unitaires : bornes avant/égal/après, équivalence des deux formes UTC et fractions de secondes, gate autonome sans valeur ni repli et refus sur entrée invalide sans décision d'expiration, matrice deux politiques × cinq usages sur définition expirée, conservation de `False` et du jeton `VARIANT`, refus terminal préservé pour cohorte, prérequis, politique inconnue et ambiguïté sur définition expirée, objets hôtes et à hooks sans aucun callback, tri, déduplication, absence d'écho, permutation et double appel identiques, non-mutation des entrées. Intégration : même enfant frais que la suite existante, douze gardes causales d'E/S et finder Django/PostgreSQL éprouvés avant import puis remis à zéro, appel réel de la gate et d'une évaluation expirée, marqueur dédié, aucune horloge, base, réseau ni secret.

Limites assumées : aucune admission complète de nouvelle affectation (la candidate n'est pas inspectée), aucune autorisation, persistance, administration, audit, cache, cycle de vie ni purge ; provenance de l'appelant non prouvée ; R2 et R3 globales non livrées.
