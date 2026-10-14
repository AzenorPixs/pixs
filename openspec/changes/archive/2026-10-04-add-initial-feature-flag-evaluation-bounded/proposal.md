# Proposition — add-initial-feature-flag-evaluation-bounded

## Why

`src/pixs/kernel/feature_flags.py` possède déjà trois primitives pures, chacune prouvée et archivée : définitions déclaratives R1 (`validate_feature_flag_definitions`), affectations et résolution de candidat R2 partiel (`resolve_feature_flag_assignment`), application déclarative du repli R3 (`resolve_feature_flag_fallback`). Rien ne les compose : un appelant serveur canonique doit aujourd'hui enchaîner lui-même résolution, classification de la cause d'échec et repli, et pourrait le faire de façon incohérente — par exemple retenir une valeur sous une politique de repli non reconnue, ou confondre absence et péremption. Cette unité ajoute uniquement cette composition bornée, sans permission, sans horloge, sans E/S et sans persistance.

## What Changes

- Ajouter au module existant, dans un appendice isolé, le DTO frozen `FeatureFlagEvaluation` (`status` ∈ `SELECTED`/`DEFAULT`/`REFUSED`, `value` `bool`/`str`/`None`, `diagnostics` tuple) à trois champs obligatoires sans défaut, et la fonction pure `evaluate_feature_flag_assignments_bounded(definition, assignments, context, use_kind)` à quatre paramètres requis. Les deux noms publics sont exposés sous un mandat distinct.
- Réutilisation stricte des validateurs et helpers existants (`validate_feature_flag_definitions`, `validate_feature_flag_assignments`, `_validate_context`, `resolve_feature_flag_assignment`, `resolve_feature_flag_fallback`, `_evaluation_diagnostics`, `_is_bare_reference`) ; aucune grammaire, aucun horodatage et aucun algorithme de ciblage dupliqués.
- Profil borné explicite : `cohort_key` déclarée ou prérequis non vide → refus pour configuration non supportée, sans repli ; une politique de repli hors `DENY`/`DEFAULT` est refusée AVANT toute valeur, donc avant toute restitution d'un candidat valide ; `expires_at` de la définition reste une donnée validée structurellement sans jamais être décidé ; un usage sensible n'est pas refusé à l'aveugle sur un candidat valide.
- Deux nouvelles suites (unitaire paramétrée par propriétés, intégration en enfant frais sous gardes causales d'E/S) et régression des soixante et onze tests existants.

## Hors périmètre

Aucune cohorte effective, aucun prérequis évalué, aucune détection d'invalidité de valeur hors constat machine connu, aucune expiration ni cycle de vie de la définition, aucune source persistante, administration, corrélation, audit, cache, exposition HTTP/frontend/CLI, ni permission positive. La provenance serveur canonique de l'appelant et la réévaluation applicative de bout en bout restent hors périmètre.

## Impact et validations

Code : appendice isolé d'un module existant et deux suites nouvelles, zéro refactoring ; classes, constantes, helpers, validateurs, résolveurs et exports antérieurs préservés byte à byte. Validations : compilation sous l'interpréteur DEVOPS (référence 3.12, runtime 3.14.8), suites nouvelles, régression 71/71, `openspec validate add-initial-feature-flag-evaluation-bounded --strict` et `openspec validate feature-flags --type spec --strict` avant code puis après preuves, relecture byte-exacte et UTF-8/LF. Archivage et `STATISTIQUES.md` constituent deux mandats distincts ultérieurs.
