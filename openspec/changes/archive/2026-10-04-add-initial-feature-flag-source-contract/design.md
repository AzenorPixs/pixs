# Design — snapshot pur de source de fanions

## Modèle

`FeatureFlagSourceSnapshot` est une dataclass frozen à quatre champs obligatoires : `configuration_version`, `definitions`, `assignments`, `cohort_rules`. Les collections sont des tuples exacts. Aucun défaut, alias ou conteneur mutable. Les types et les structures sont fermés avant tout accès d'attribut, comparaison, itération ou hook.

Le validateur retourne uniquement des diagnostics de refus. Il réutilise `validate_feature_flag_definitions`, `validate_feature_flag_assignments` et `validate_feature_flag_cohort_rule`, puis ajoute les liaisons canoniques sans créer de grammaire ni de statut.

## Liaisons

Chaque affectation référence un `flag_id` exactement déclaré dans `definitions` et un `selector` parmi les dimensions de cette définition. La `configuration_version` de toutes les affectations et règles est exactement celle du snapshot. Le champ `flag_version` des définitions reste opaque et distinct ; aucune comparaison ou relation d'ordre entre versions n'est inventée.

Chaque définition portant `cohort_key` doit correspondre à une et une seule règle. Plusieurs définitions peuvent partager une règle si leur `cohort_key` est identique et si la `subject_dimension` de cette règle est déclarée par chaque définition concernée. Une même `cohort_key` ne peut pas recevoir deux règles ou versions divergentes. Une règle non référencée est refusée : le snapshot est un lot canonique indivisible et fermé, choix technique de design, sans nouvelle norme.

Les définitions sans cohorte conservent une évaluation sans règle. Une affectation absente ou une fenêtre non active n'est pas invalidée dans le contrat : le résolveur et l'évaluateur existants produisent leurs propres causes `NO_MATCH` ou ambiguïté. Aucun filtre simpliste de target n'est ajouté et aucune neutralisation de cohorte par projection de définition n'est permise.

## Évaluation

`evaluate_feature_flag_source_snapshot(snapshot, expected_configuration_version, flag_id, context, use_kind)` retourne `FeatureFlagEvaluation`. Après fermeture des types et validation intégrale du lot, la version attendue est comparée exactement à `snapshot.configuration_version`. Une définition absente donne un refus sans repli inventé. La recherche isole ensuite les affectations correspondant au `flag_id` et sélectionne la règle exacte liée à `cohort_key`. Le module délègue alors sans modification à `evaluate_feature_flag_assignments_with_cohort`.

Le snapshot est une frontière de cohérence, pas une preuve de provenance. L'appelant serveur conserve la responsabilité du chargement persistant et de l'authentification administrative. Aucune horloge, cache, TTL, statut nouveau, protocole, mutation, PostgreSQL ou dépendance n'est introduit.
