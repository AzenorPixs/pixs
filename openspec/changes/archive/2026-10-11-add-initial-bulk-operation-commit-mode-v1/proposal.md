## Why

Le canon bulk-operations définit BulkOperationCommitMode v1, mais son profil préparatoire et sa validation pure ne sont pas implémentés. Ce change réalise uniquement ce contrat déjà validé.

## What Changes

- Ajouter une représentation interne immuable à deux champs obligatoires sans défaut : operation_id et commit_mode.
- Réutiliser les quatre membres canoniques BulkCommitMode, sans choix ni application de mode.
- Ajouter une validation pure de types exacts et des diagnostics statiques VALIDATE triés/dédupliqués, sans écho.
- Ajouter des tests unitaires et une intégration en processus frais sous gardes d’effets à contrôles positifs.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- bulk-operations : implémentation du seul profil préparatoire BulkOperationCommitMode v1.

## Impact

Trois nouveaux fichiers Python uniquement, sans modification des enums, des façades ou d’une autre implémentation. Aucun schéma SQL, dépendance, configuration, endpoint, staging, transaction, mutation, découpage, autorisation, persistance ou import/export. PA/PZT et les exigences générales bulk restent applicables.
