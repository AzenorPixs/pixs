# Proposition — intégration de la cohorte à l'évaluation

## Why

La règle et le calcul de cohorte sont prouvés et archivés. L'évaluation existante refuse encore toute cohorte déclarée ; R2 et R3 déjà validées demandent son intégration à la valeur, au repli et à l'expiration.

## What Changes

- Ajouter `evaluate_feature_flag_assignments_with_cohort(definition, assignments, context, use_kind, rule, expected_configuration_version)` dans le module existant `feature_flag_cohorts.py`, avec le seul export ajouté.
- Déléguer les fanions sans cohorte à l'évaluation existante, sans consulter les deux entrées de cohorte inutilisées. Pour les fanions avec cohorte, consommer la décision réelle validée avant sélection de valeur.
- Préserver les refus terminaux et appliquer l'expiration de définition, puis le repli ABSENT hors cohorte, ou la sélection et les causes existantes pour les membres.
- Deux nouvelles suites ciblées ; les 106 tests existants et leurs fichiers restent intacts.

## Capabilities

### Modified Capabilities

- `feature-flags` : portion de composition R2/R3 ; delta recopié mot pour mot du canonique approuvé, aucune norme nouvelle.

## Impact

Trois sources seulement : un module étendu et deux suites nouvelles. L'ancien `feature_flags.py`, les anciens modèles, helpers et autres fichiers de baseline restent inchangés. Aucun contournement de cohorte par remplacement ou projection de définition. Aucun nouveau modèle de domaine, statut, grammaire, dépendance ou horloge.

Pas de persistance, cache, administration, audit, UI, API, provenance canonique prouvée du snapshot, résolution de prérequis, migration, secret ou Git. R2/R3/R4 globales ne sont pas livrées. Compilations, tests nouveaux et 106 régressions, stricts, UTF-8/LF, scope et preuves précèdent cochage/archivage ; STATISTIQUES.md est un mandat distinct.
