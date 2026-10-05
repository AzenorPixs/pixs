# Proposition — add-initial-feature-flag-definition-expiry

## Why

La norme R3 de `feature-flags`, approuvée par le développeur et déjà intégrale dans `openspec/specs/feature-flags/spec.md:32-54` et `TECHNICAL.md:383`, impose qu'à l'instant de référence UTC canonique serveur une définition dont `expires_at` est atteint rende périmées ses valeurs déjà affectées, applique la politique de repli déclarée et bloque les nouvelles affectations avec un diagnostic. Rien ne l'applique : `src/pixs/kernel/feature_flags.py:804` documente expressément « aucune comparaison de `expires_at` de la définition » et l'en-tête du module (l. 14-17) « aucune décision d'expiration ». Cette unité rend la norme exécutoire dans la composition bornée existante, sans persistance ni backend.

## What Changes

- Ajouter une gate temporelle pure `validate_feature_flag_assignment_expiry(definition, context)` : fermeture des types exacts avant tout accès d'attribut, validations déléguées à `validate_feature_flag_definitions` et `_validate_context`, refus de `expires_at <= as_of` par un diagnostic constant trié, dédupliqué et non échoé, comparaison par `datetime.fromisoformat` des horodatages déjà validés. Elle ne retourne que des diagnostics : ni valeur, ni repli, ni admission.
- Consommer cette gate dans `evaluate_feature_flag_assignments_bounded` avant toute restitution de valeur : un `SELECTED` sur définition expirée n'expose pas sa valeur et transite par `resolve_feature_flag_fallback(definition, use_kind, "STALE")` avec le diagnostic d'expiration ajouté, y compris sous `DEFAULT` ; un `NO_MATCH` expiré est traité avec la cause `STALE` ; le chemin `INVALID` non expiré conserve son repli ; sur définition expirée, la cause devient `STALE` avec le diagnostic d'expiration ; tout refus terminal (entrées invalides, cohorte déclarée, prérequis non vides, politique hors `DENY`/`DEFAULT`, candidats ambigus, invariant) reste terminal sans valeur, même sur définition expirée.
- Corriger localement les docstrings désormais inexactes (en-tête du module, `FeatureFlagEvaluation`, `evaluate_feature_flag_assignments_bounded`) sans refactor ; les autres fonctions, classes, constantes, helpers et exports restent byte à byte, `__all__` reçoit le seul export ajouté dans le même mandat du module.
- Étendre les deux suites bornées existantes ; régression des quatre-vingt-trois tests.

## Out of scope

Aucune admission complète d'une nouvelle affectation, aucune autorisation, aucune source persistante, administration, corrélation, audit, cache, exposition HTTP/frontend/CLI, aucun cycle de vie `DRAFT→ACTIVE→PAUSED→EXPIRED→RETIRED`, aucune purge, aucune suppression de code, données ou contrats, aucune cohorte ni prérequis, aucune horloge système ni environnement. La provenance canonique serveur de l'appelant n'est pas prouvée et les garanties globales R2, R3 et R4 ne sont pas livrées.

## Impact et validations

Code : une fonction ajoutée, une fonction existante étendue, deux suites étendues, zéro refactoring, aucune dépendance nouvelle (`pyproject.toml` : `requires-python = ">=3.12"`). Validations : `py_compile` des trois fichiers sous l'interpréteur DEVOPS, suites étendues, régression 83/83, `openspec validate add-initial-feature-flag-definition-expiry --strict` et `openspec validate feature-flags --type spec --strict` avant code, après preuves puis après cochage, relecture byte-à-byte des symboles antérieurs et UTF-8/LF. Impact de compatibilité : seule une définition expirée portant des affectations actives change d'observable, et aucun consommateur global de fanions n'existe à ce jour. Archivage et `STATISTIQUES.md` sont deux mandats distincts.
