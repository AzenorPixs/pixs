# Tasks

## 1. Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif et baseline des éléments R1 et C1a, créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-evaluation --strict` avant tout code.

## 2. Modèles et API

- [x] 2.1 Étendre seulement `src/pixs/kernel/feature_flags.py` : `FeatureFlagEvaluationContext` frozen à cinq champs obligatoires sans défaut, `FeatureFlagResolution` frozen à statut borné, affectation ou `None` et tuple de diagnostics, fonction pure `resolve_feature_flag_assignment` réutilisant les validateurs et helpers existants, sans horloge, E/S, persistance, cohorte, prérequis ni repli.

## 3. Tests

- [x] 3.1 Créer `tests/unit/test_feature_flag_evaluation.py` : formes de contexte acceptées et refusées dont `scope` sans `tenant`, adéquation exacte `flag_id` et `selector_value`, dimensions non déclarées ignorées sans élargissement, fenêtre semi-ouverte sur `as_of` injecté, trois niveaux de priorité sans ordre relatif entre `INSTALLATION` et `ENVIRONMENT`, ambiguïté refusée même à valeurs égales, permutation du lot et double évaluation du même contexte identiques, `NO_MATCH`, `SELECTED` avec `False` conservé, conformité du schéma de valeur à la définition, entrée hostile fermée sans écho ni index dépendant de l'ordre.
- [x] 3.2 Créer `tests/integration/test_feature_flag_evaluation_integration.py` : import d'un enfant frais sous gardes causales d'E/S, résolution témoin déterministe sans effet, refus hostile avant tout usage, marqueur final dédié, périmètre sans Django, PostgreSQL, réseau ni secret.

## 4. Preuves

- [x] 4.1 Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS.
- [x] 4.2 Réussir les deux suites nouvelles et la régression des quarante-cinq tests existants dans un environnement explicite.
- [x] 4.3 Vérifier relecture byte-exacte des éléments R1 et C1a, conservation des exports et de la configuration de style, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R2 MOTAMOT, en explicitant les garanties R2, R3 et R4 non livrées.
- [x] 4.4 Réussir `openspec validate add-initial-feature-flag-evaluation --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d’archivage sous contrôle CGPT.

Après achèvement prouvé des tâches : archivage puis `STATISTIQUES.md` sous deux mandats distincts. Le parent CISMP reste OPEN.
