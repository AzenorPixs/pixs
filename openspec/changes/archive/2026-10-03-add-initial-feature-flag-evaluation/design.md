# Design — résolution déclarative d'affectations

## Contrat

`FeatureFlagEvaluationContext` est une dataclass frozen à cinq champs obligatoires sans défaut : `installation`, `environment`, `tenant`, `scope`, `as_of`. Les quatre premiers sont soit une chaîne exacte non vide opaque, soit `None`. `as_of` est un horodatage UTC sérialisé au format déjà validé par le helper existant. La présence de `scope` sans `tenant` est refusée comme incohérence de forme uniquement : aucune relation de périmètre, aucune traversée et aucun descendant ne sont prouvés. Les identifiants contextuels sont fournis par l'appelant canonique ; le résolveur n'élargit jamais un périmètre.

`FeatureFlagResolution` est une dataclass frozen portant `status`, `assignment` et `diagnostics`. Le domaine de `status` est borné à `SELECTED`, `NO_MATCH` et `REFUSED`. Une entrée invalide produit `REFUSED` avec diagnostics et aucune valeur ; `False` reste une valeur légitime conservée.

## Choix techniques CGPT

Ces points sont des décisions techniques prises dans un cadre normatif existant, pas des clauses nouvelles.

- **Niveaux de priorité.** Trois niveaux : général (`INSTALLATION` et `ENVIRONMENT` réunis au même niveau), `TENANT`, puis `SCOPE`. Les sources ne prescrivent aucun ordre relatif entre `INSTALLATION` et `ENVIRONMENT`, donc aucun ordre n'est inventé. Plusieurs candidats au meilleur niveau produisent `REFUSED`, même si leurs valeurs coïncident : la sélection ne dépend jamais de l'ordre du lot. Aucun candidat au niveau retenu produit `NO_MATCH` ; un candidat unique produit `SELECTED`.
- **Comparaison.** Adéquation par égalité exacte de `flag_id` et de `selector_value` avec le champ de contexte correspondant au sélecteur. Une dimension non déclarée par la définition est ignorée, sans élargissement.
- **Fenêtre.** Filtre technique semi-ouvert `valid_from <= as_of < valid_until`, en comparant des bornes déjà validées par le helper existant. Aucune horloge système, aucun `datetime.now`, aucun environnement : `as_of` est injecté par l'appelant. Le résolveur ne décide ni l'expiration du fanion portée par `expires_at`, ni son cycle de vie.
- **Fermeture des types.** Types vérifiés par identité exacte avant toute itération, tout accès d'attribut, toute comparaison et tout hachage : conteneur `list` ou `tuple` exact, éléments `FeatureFlagAssignment` exacts, `definition` de type `FeatureFlagDefinition` exact. Les diagnostics des validateurs existants sont réutilisés et restitués triés et dédupliqués, en motifs constants, sans écho de valeur invalide ni index dépendant de l'ordre.
- **Cohérence de valeur.** La valeur de l'affectation retenue doit correspondre au schéma de la définition : `bool` exact pour `BOOLEAN`, jeton littéral borné pour `VARIANT`. Aucun enum métier, aucune liste de variantes autorisées ou proscrites n'est introduit.
- **Préservation.** Renommage, déplacement et refactoring exclus. Les modifications du module se limitent aux blocs nouveaux, à la documentation nécessaire et à l'ajout des nouveaux noms d'export ; les classes, constantes, helpers, validateurs et exports de R1 et C1a restent byte à byte dans leur comportement.

## Limites assumées

Le résultat n'est qu'un candidat de ciblage. La documentation de l'interface interdit d'assimiler ce résultat à une évaluation runtime complète, à une permission, à une mutation autorisée ou à l'application d'un repli. Cohorte effective, prérequis, repli, persistance et administration ne sont pas livrés ; la garantie R2 complète, ainsi que R3 et R4, restent ouvertes.
