# Design — application déclarative du repli R3

## Contrat

`FeatureFlagFallback` est une dataclass frozen à trois champs obligatoires sans défaut : `status` (domaine borné à `DEFAULT` et `REFUSED`), `value` (`bool`, `str` ou `None`, jamais posé hors `DEFAULT`) et `diagnostics` (tuple trié et dédupliqué, sans reproduction de valeur). `resolve_feature_flag_fallback(definition, use_kind, failure_kind)` prend trois paramètres obligatoires : une `definition` de type exact `FeatureFlagDefinition`, une `use_kind` et une `failure_kind` en chaînes exactes.

Le type est fermé avant tout accès d'attribut, toute comparaison, tout hachage ou toute itération : une `definition` d'un autre type (sous-classe, objet étranger, objet piégé) et une `use_kind` ou `failure_kind` qui n'est pas une chaîne exacte produisent `REFUSED` sans valeur. Le résultat ne comporte aucun défaut de champ et aucun enum public ni contexte supplémentaire n'est ajouté.

## Domaines privés fermés

- Usages reconnus : `NON_SENSITIVE`, `PERMISSION`, `MUTATION`, `PROTECTED_DATA`, `CONTRACT`. Les quatre derniers constituent le périmètre sensible de R3.
- Échecs reconnus : `ABSENT`, `INVALID`, `STALE`, correspondant aux trois causes nommées par R3 (valeur absente, invalide ou périmée).

Les domaines sont portés par des constantes privées du module ; le rôle de la primitive est de les vérifier à l'exécution, pas de les découvrir. Une valeur hors domaine est un `REFUSED` avec diagnostic constant, sans écho de la valeur reçue.

## Décision

Après validité structurelle de la définition obtenue par `validate_feature_flag_definitions` :

| `fallback_policy` déclaré | `use_kind` | Issue |
|---|---|---|
| `DENY` | n'importe quel usage reconnu | `REFUSED`, aucune valeur, diagnostics pouvant rester vides |
| `DEFAULT` | `NON_SENSITIVE` | `DEFAULT` avec la `default_value` validée de la définition, `False` et jeton `VARIANT` conservés à l'identique |
| `DEFAULT` | usage sensible | `REFUSED`, aucune valeur |
| référence opaque héritée, inconnue ou incompatible | n'importe lequel | `REFUSED`, aucune valeur, diagnostic constant, aucun alias implicite |

Un usage sensible est donc refusé quelle que soit la politique déclarée, conformément à R3. La valeur n'est jamais déduite, normalisée ni remplacée : `False` n'est pas un échec et un jeton `VARIANT` n'est pas converti en booléen.

## Choix techniques documentés

- Les domaines fermés, le nom `FeatureFlagFallback`, le choix de diagnostics pouvant rester vides sur `DENY` et la restriction de `value` au seul statut `DEFAULT` sont des choix techniques dans le cadre normatif déjà approuvé, pas des clauses nouvelles.
- La déduplication et le tri des diagnostics réutilisent `_evaluation_diagnostics` ; les contrôles de référence réutilisent `_is_bare_reference` ; aucune grammaire, aucun horodatage ni aucun motif de diagnostic n'est recopié.
- Le validateur structurel R1 reste inchangé et continue d'accepter `fallback_policy` comme référence opaque : la restriction du vocabulaire est une décision d'exécution, pas une migration de modèle, sans renommage ni alias automatique des références héritées.

## Provenance et interdiction d'exposition

La classification sensible ou non sensible et le constat d'échec proviennent du contexte applicatif canonique côté serveur. La documentation de l'interface précise qu'elle est réservée à un appelant interne de confiance : la primitive ne prouve pas cette provenance, ne lit aucun environnement, aucune entrée réseau et aucune horloge, et n'est exportée ni par HTTP, ni par le frontend, ni par une CLI. Elle ne prétend ni couvrir la réévaluation par le frontal, ni livrer la garantie R3 complète.

## Préservation et tests

L'ajout est un appendice isolé en fin de module, suivi d'un mandat distinct pour `__all__` ; les classes, constantes, helpers, validateurs, résolveurs et exports antérieurs de R1, C1a et C2 restent identiques. Les tests couvrent la matrice des usages et des échecs, la conservation de `False` et du jeton `VARIANT`, le refus d'une référence héritée inconnue sans alias, le refus d'un usage sensible sous `DEFAULT`, les types hostiles et objets piégés sans aucun callback déclenché, la stabilité et l'absence d'écho des diagnostics, ainsi que l'immutabilité et l'obligation des champs. L'intégration exécute la primitive dans un enfant frais sous gardes causales d'E/S avec remise à zéro prouvée, sans Django, PostgreSQL, réseau ni secret.
