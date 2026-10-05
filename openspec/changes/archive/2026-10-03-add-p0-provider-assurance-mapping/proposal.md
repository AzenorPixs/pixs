# Proposition : add-p0-provider-assurance-mapping

## Why

La spec canonique `identity-assurance` exige que les trois dimensions d'assurance soient « évaluées séparément selon le mapping déclaré du fournisseur » (R1, scénario « Claim absent sans surclassement »). Les types et contrôles PDP existent (trois enums dans `core/authz/policy.py`, `AuthenticationContext` dans `core/authz/ports.py`, seuils par rang dans `core/authz/decision.py`), mais aucune structure ne déclare le mapping fournisseur lui-même : preuves acceptées, plafonds et conditions de validité (TECHNICAL 43). Cette fondation déclarative pure est la portion R1 réellement manquante.

## What Changes

- Trois sources nouvelles exactes : `src/pixs/core/authz/assurance_mapping.py`, `tests/unit/test_provider_assurance_mapping.py`, `tests/integration/test_provider_assurance_mapping_integration.py` ; aucun fichier existant modifié (`__init__.py` et legacy intacts).
- Un mapping fournisseur déclaratif : `provider_id` opaque, trois plafonds globaux par dimension (un par enum existante, indépendants), règles explicites `(dimension, method, niveau de cette dimension)`, bornes de validité UTC.
- Une évaluation déterministe `evaluate_assurance(mapping, observations, reference_time)` : seule une observation `VERIFIED` validement rattachée au même fournisseur contribue, et seulement au niveau déclaré de chaque règle qui la référence ; jamais de maximum implicite ; aucune hausse d'une autre dimension sans règle explicite ; absence ou divergence ⇒ minimum de la dimension.
- Les observations sont des constats normalisés, non secrets, fournis par un hôte ou backend déjà authentifié : l'expiration est une borne UTC finie stricte (`attested_at < expires_at`), le tuple vide exprime l'absence, `reference_time` vient de l'appelant sans aucune horloge interne.
- Refus fermé constant avant tout crochet étranger : identités de type exactes, ordinaux issus de l'ordre de déclaration des enums existantes ; réutilisation du seul helper UTC `policy._is_utc_aware` validé CGPT, sans invocation de `decision._rank` ; unicité `(dimension, method)` et des `observation_id` ; niveau jamais supérieur au plafond de sa dimension ; erreur structurelle `AssuranceMappingError` constante sans écho (mêmes code, element, step et message sous permutation), aucun retour de liste de diagnostics.

## Hors périmètre

- Pas le R1 complet : aucune authentification réelle produisant un contexte, aucune vérification cryptographique, aucune permission déduite d'un statut autodéclaré ; pas de nouvel `AuthenticationContext` ni de modification du PDP.
- R2 et R3 disposent déjà de contrôles PDP en mémoire (seuils, temps, révocation) ; leurs intégrations authentification/session/audit réelles restent non réalisées et non revendiquées ; pas de P0 global.

## Impact

- Spécification : MODIFIED du seul R1 « Contexte vérifié et dimensions distinctes » MOTAMOT, scénario original conservé, aucune exigence ni scénario ajouté.
- Code : trois sources nouvelles, aucune source actuelle modifiée ; baseline réelle 168 (héritage complet, cœur masqué inclus) prise avant préparation.
- Risque : faible — module isolé sans consommateur existant.
