# Proposition — règles de cohorte

## Why

R2 et TECHNICAL.md §7.2 définissent désormais le profil A validé : règle canonique serveur, sujet explicite, seuil de 0 à 10000 et version. Cette unité rend possible la validation et le calcul stable de l'appartenance, sans sélectionner de valeur de fanion.

## What Changes

- Nouveau module pur `src/pixs/kernel/feature_flag_cohorts.py` : règle figée à quatre champs obligatoires, résultat figé `MEMBER`/`NON_MEMBER`/`REFUSED`, validation singulière et résolution fermée sur définition, règle, contexte et version attendue.
- Calcul stable SHA-256 de la clé, de la dimension et de l'identité canonique, modulo 10000 ; aucune horloge, aucun hasard et aucune valeur ou permission exposée.
- Deux nouvelles suites : unitaires et intégration fraîche avec gardes causales. Les dix-sept fichiers préexistants de baseline et les 91 tests antérieurs restent inchangés.

## Capabilities

### Modified Capabilities

- `feature-flags` : portion règle et calcul de R2 seulement ; delta recopié mot pour mot du canonique approuvé.

## Impact

Trois nouvelles sources seulement, stdlib exclusivement et Python >=3.12. Le module existant `feature_flags.py` et ses exports sont préservés. Aucun branchement à la composition d'affectations ou au repli dans cette unité : ce sera une unité ultérieure. Pas de persistance, administration, audit, cache, API, frontend, provenance prouvée du contexte, prérequis, migration, secret ou Git. R2 et R4 globales ne sont pas déclarées livrées.

Validation : compilations des trois fichiers, tests nouveaux et 91 régressions, syntaxe minimum 3.12, processus frais sous gardes éprouvées, stricts du change et du référentiel, UTF-8/LF et scope. Archivage et STATISTIQUES.md constituent deux mandats distincts après preuves.
