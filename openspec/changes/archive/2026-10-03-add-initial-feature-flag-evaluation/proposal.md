# Proposition — add-initial-feature-flag-evaluation

## Why

L'exigence R2 de la capacité `feature-flags` impose une évaluation déterministe utilisant uniquement les dimensions déclarées, avec priorité du général au spécifique (`openspec/specs/feature-flags/spec.md:17-26`, `TECHNICAL.md:367`). Le référentiel possède déjà les modèles déclaratifs `FeatureFlagDefinition` et `FeatureFlagAssignment` avec leurs validateurs dans `src/pixs/kernel/feature_flags.py`, mais aucune sélection déterministe de l'affectation applicable n'existe. Cette unité livre une résolution de candidat de ciblage, non une évaluation runtime complète.

## What Changes

- Ajouter au module existant deux dataclasses frozen : `FeatureFlagEvaluationContext` à cinq champs obligatoires sans défaut, et `FeatureFlagResolution` portant un statut borné, l'affectation retenue ou `None`, et un tuple de diagnostics.
- Ajouter la fonction pure `resolve_feature_flag_assignment(definition, assignments, context)` : adéquation par égalité exacte de `flag_id` et de `selector_value`, dimensions non déclarées ignorées sans élargissement, filtre technique de fenêtre semi-ouverte, priorité par niveaux général puis tenant puis scope, ambiguïté refusée, aucun candidat `NO_MATCH`, candidat unique `SELECTED`.
- Réutiliser `validate_feature_flag_definitions`, `validate_feature_flag_assignments` et les helpers existants ; aucun clonage de grammaire ni d'analyse horodatage ; diagnostics constants triés et dédupliqués sans reproduction de valeur ni index dépendant de l'ordre.
- Deux nouvelles suites de tests, unitaire et d'intégration sans effet, plus la régression des quarante-cinq tests existants.

## Out of scope

Aucune application de cohorte, de prérequis ou de repli ; aucune permission, mutation ni décision métier ; aucune expiration du fanion ni cycle de vie ; aucune source persistante, administration, corrélation, audit, cache, provider, base de données ou contrôle de non-embarquement au build. La garantie R2 complète n'est pas déclarée livrée ; R3 et R4 restent ouvertes.

## Impact et validations

Code : extension minimale d'un module existant et deux suites nouvelles, zéro refactoring, comportement et exports antérieurs préservés. Validations : compilation sous l'interpréteur DEVOPS, suites nouvelles, régression 45/45, relecture byte-exacte des éléments R1 et C1a, `openspec validate add-initial-feature-flag-evaluation --strict` avant code et après preuves. Archivage et `STATISTIQUES.md` constituent deux mandats distincts ultérieurs.
