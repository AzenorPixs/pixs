# Proposal — add-initial-bulk-job-phase-vocabulary-v1

## Why

La spécification canonique `jobs` B08 et son schéma `BulkJobBindingV1` imposent les quatre phases `STAGE`, `VALIDATE`, `APPLY`, `EXPORT`, mais aucun module Python ne représente ce vocabulaire (recherche `BulkJobPhase` sans résultat en `src/pixs/kernel` ciblé). Sans représentation unique, chaque futur consommateur reproduirait les phases par des chaînes libres, source de divergences silencieuses.

## What Changes

- Publier `src/pixs/kernel/bulk_job_phase.py` : contrat générique pur `BulkJobPhase(Enum)` avec les quatre membres exacts `STAGE = "STAGE"`, `VALIDATE = "VALIDATE"`, `APPLY = "APPLY"`, `EXPORT = "EXPORT"`, sans mixin `str`, alias, défaut, validation ni runtime.
- Publier un test unitaire significatif du vocabulaire et un test d'intégration d'import en processus frais sans effet, prouvant l'adhésion exacte au canon B08 et l'absence d'effet runtime, sans modifier les validateurs/records existants.
- Aucun fichier existant modifié, aucune façade ni `__init__` touché.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification de texte canonique. `skip_specs: true` évite un delta identique artificiel.

## Impact

Fondation partielle : représente les phases, ne prouve ni transition, machine d'états, persistance, liaison, bail, autorisation ni exécution. La convention Enum standard n'offre pas d'immutabilité profonde et il n'en est promis aucune. Pas de tests PostgreSQL pour ce vocabulaire pur ; DB/frontend non pertinents (N/A).
