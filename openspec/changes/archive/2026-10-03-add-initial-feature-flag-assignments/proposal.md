# Proposition — add-initial-feature-flag-assignments

## Pourquoi

La forme `FeatureFlagAssignment` est cadrée par TECHNICAL.md §7.2 mais absente du code. R1 dispose déjà d'un modèle de définition et de helpers de validation. Cette unité prépare la représentation structurelle des affectations, prérequis du traitement runtime de R4.

## Ce qui change

- Ajouter `FeatureFlagAssignment` frozen et `validate_feature_flag_assignments` dans le module existant `src/pixs/kernel/feature_flags.py`.
- Huit champs requis sans défaut : flag_id, selector, selector_value, value, valid_from, valid_until, configuration_version, updated_by.
- Validation pure stdlib, types exacts, diagnostics agrégés déterministes sans écho et réutilisation des helpers existants.
- Deux suites nouvelles ; régression des définitions R1 existantes.

## Choix techniques CGPT

Les champs proviennent du cadrage validé. Les représentations Python suivantes sont des choix techniques CGPT : textes opaques non vides pour selector_value/configuration_version/updated_by, bool exact ou jeton littéral pour value, bornes UTC sérialisées cohérentes et fenêtre structurelle strictement positive. Aucun ordre de version ni preuve d'identité n'en est déduit.

## Hors périmètre

Aucun évaluateur, priorité, cohorte, comparaison à une horloge, expiration runtime ou lifecycle. Aucune unicité/gestion de chevauchement, liaison à une définition, persistance, cache, administration, audit effectif, authentification, provider, DB, endpoint, CLI ou dépendance nouvelle. Les exigences R2 et R4 effectives restent non livrées par cette unité.

## Impact et validations

Code : extension minimale d'un module et deux suites nouvelles, sans refactoring. Préserver douze champs, defaults, helpers, validateur et exports antérieurs de R1. Compilation minimum 3.11/runtime DEVOPS, tests unitaires/intégration et régressions R1, UTF-8/LF, OpenSpec strict avant code et après preuves.

Delta MODIFIED de R4 MOTAMOT uniquement pour ancrage documentaire : aucune clause ou scénario normatif ajouté et aucune suppression des garanties de source persistante ou de rejet au build. Archive et STATISTIQUES nécessitent des mandats distincts après toutes les preuves.
