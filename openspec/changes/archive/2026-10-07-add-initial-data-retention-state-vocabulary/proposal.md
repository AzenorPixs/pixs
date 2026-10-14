# Proposition — Vocabulaire commun des états de rétention

## Why

La capacité canonique `data-lifecycle`, après RSMP validée par le développeur, nomme exactement `RETAINED`, `LEGAL_HOLD`, `ELIGIBLE_FOR_PURGE`. Aucune représentation commune de ces noms n'est présente dans le Kernel ou les tests examinés.

## What Changes

- Ajouter `DataRetentionState(Enum)` dans `src/pixs/kernel/data_retention_states.py`, avec les trois noms/valeurs exacts dans l'ordre canonique et `__all__` limité à cette classe.
- Ajouter un test unitaire d'adhésion normative et un test d'import frais sous gardes d'effets réutilisées.
- Reproduire en delta MODIFIED l'exigence « Dimensions et états distincts » et ses deux scénarios, sans modification normative.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-lifecycle` : delta identique au bloc canonique ; effet d'archive attendu nul.

## Impact

Trois nouveaux fichiers source/tests, aucun fichier existant modifié et aucun réexport du Kernel. Cette fondation représente uniquement le vocabulaire commun de rétention ; elle ne clôture pas l'exigence de séparation des dimensions ni ses scénarios de cycle de vie. Aucun défaut, transition, calcul d'éligibilité, politique, purge, autorisation, métadonnée, tombstone, persistance, DB ou runtime n'est ajouté ou revendiqué. Les scénarios de suppression, de purge refusée et de restauration restent hors de cette unité.
