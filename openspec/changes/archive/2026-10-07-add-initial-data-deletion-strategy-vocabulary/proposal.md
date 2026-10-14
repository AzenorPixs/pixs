# Proposition — Vocabulaire commun des stratégies de suppression

## Why

La capacité canonique `data-lifecycle`, après RSMP validée par le développeur, fixe les quatre stratégies communes `SOFT_DELETE`, `PHYSICAL_DELETE`, `ARCHIVE`, `IMMUTABLE`. Aucune représentation commune de ces noms n'est présente dans le Kernel ou les tests examinés.

## What Changes

- Ajouter `DataDeletionStrategy(Enum)` dans `src/pixs/kernel/data_deletion_strategies.py`, avec les quatre noms/valeurs exacts dans l'ordre canonique et `__all__` limité à cette classe.
- Ajouter un test unitaire d'adhésion normative et un test d'import frais sous gardes d'effets réutilisées.
- Reproduire en delta MODIFIED l'exigence « Vocabulaire commun des stratégies de suppression » et son scénario, sans modification normative.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-lifecycle` : delta identique au bloc canonique ; effet d'archive attendu nul.

## Impact

Trois nouveaux fichiers source/tests, aucun fichier existant modifié et aucun réexport du Kernel. Le change livre uniquement ce vocabulaire déclaratif ; il ne fournit pas de stratégie exécutable. Aucun défaut, transition, calcul, politique, autorisation d'effacement, purge, métadonnée, tombstone, DB ou runtime ajouté. `IMMUTABLE` ne confère pas d'immutabilité d'une ressource. Les scénarios de suppression, de purge et de restauration restent hors de cette unité.
