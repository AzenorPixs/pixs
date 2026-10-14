# Proposition — add-initial-feature-flag-fallback

## Why

La norme R3 de `feature-flags`, approuvée par le développeur, borne à l'exécution le vocabulaire du repli aux seules politiques déclaratives `DENY` et `DEFAULT` (`openspec/specs/feature-flags/spec.md:28-47`, `TECHNICAL.md:373`) : `DENY` refuse l'opération sans exposer de valeur de fanion, `DEFAULT` applique la valeur par défaut validée uniquement pour une fonctionnalité non sensible, et une permission, une mutation, une donnée protégée ou un contrat est refusé quelle que soit la politique déclarée. Rien n'applique cette garantie dans `src/pixs/kernel/feature_flags.py` : `resolve_feature_flag_assignment` ne retient qu'un candidat de ciblage et sa documentation écarte explicitement le repli. Cette unité livre la primitive pure qui applique R3 à un échec déjà constaté, sans évaluateur global.

## What Changes

- Ajouter au module existant, dans un appendice isolé, le résultat frozen `FeatureFlagFallback` à trois champs obligatoires sans défaut (`status`, `value`, `diagnostics`) et la fonction pure `resolve_feature_flag_fallback(definition, use_kind, failure_kind)`.
- Deux domaines privés bornés à des chaînes exactes : usage `NON_SENSITIVE`, `PERMISSION`, `MUTATION`, `PROTECTED_DATA`, `CONTRACT` ; échec `ABSENT`, `INVALID`, `STALE`. Toute autre valeur, toute valeur inconnue et tout type invalide produisent `REFUSED` sans valeur.
- Réutilisation stricte de `validate_feature_flag_definitions`, des helpers existants et de `_evaluation_diagnostics` pour le tri et la déduplication ; aucune duplication de grammaire ni d'analyse d'horodatage ; aucune restriction nouvelle ajoutée au validateur structurel R1.
- Après définition valide : `DENY` produit `REFUSED` avec diagnostics pouvant rester vides ; `DEFAULT` combiné à un usage non sensible et à un échec connu applique la `default_value` validée en conservant `False` pour `BOOLEAN` et un jeton littéral pour `VARIANT` ; un usage sensible est refusé quelle que soit la politique déclarée ; une référence de repli opaque héritée, inconnue ou incompatible est refusée sans aucune conversion en alias implicite, avec un diagnostic constant.
- Deux nouvelles suites de tests, unitaire et d'intégration sous gardes causales, plus la régression des soixante et un tests existants.

## Out of scope

La primitive ne détecte aucune absence, invalidité ni péremption, ne choisit aucune classification et ne retient aucun candidat : `definition`, `use_kind` et `failure_kind` proviennent de l'appelant serveur canonique. Elle n'est exposée ni au HTTP, ni au frontend, ni à une interface CLI, et ne prouve pas la provenance de l'appelant. Aucune réévaluation globale par le frontal, aucune cohorte, aucun prérequis, aucune persistance, cache, administration, audit, cycle de vie ni contrôle de non-embarquement au build n'est livré. La validation structurelle R1 continue d'accepter les références opaques existantes ; les contraintes du vocabulaire sont vérifiées à l'exécution, sans renommage ni alias automatique.

## Impact et validations

Code : appendice isolé d'un module existant et deux suites nouvelles, zéro refactoring ; classes, constantes, helpers, validateurs et exports de R1, C1a et C2 préservés byte à byte, les deux nouveaux noms publics relevant d'un mandat distinct. Validations : compilation des trois sources sous l'interpréteur DEVOPS (référence 3.12, runtime 3.14.8), suites nouvelles, régression 61/61, `openspec validate add-initial-feature-flag-fallback --strict` et `openspec validate feature-flags --type spec --strict` avant code puis après preuves, relecture byte-exacte et UTF-8/LF. Archivage et `STATISTIQUES.md` constituent deux mandats distincts ultérieurs.
