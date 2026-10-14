# Proposal — align-jobs-state-vocabulary

## Why

TECHNICAL.md §23 définit neuf états Jobs. La spécification Jobs et la phrase correspondante de BUILD.md omettent SUCCEEDED et PAUSED. Le développeur a validé leur alignement.

## What Changes

- Ajouter SUCCEEDED et PAUSED à la seule exigence « Persistance et états explicites » de Jobs, par synchronisation du delta lors de l'archivage.
- Ajouter les mêmes états à la seule phrase Jobs de BUILD.md.
- Conserver TECHNICAL.md, les scénarios et toutes les autres exigences.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `jobs` : aligner le vocabulaire des états existants.

## Impact

Correction normative et documentaire uniquement. Aucun code, transition, bail, réessai, migration ni comportement d'exécution n'est ajouté ou prouvé.
