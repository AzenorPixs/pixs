## Why

BulkOperationConflict v1 est défini dans la spécification validée bulk-operations, mais sa représentation et sa validation pure ne sont pas implémentées. Ce change réalise seulement ce profil préparatoire.

## What Changes

- Ajouter un profil Python immuable à deux champs explicitement fournis : operation_id et conflict_strategy.
- Conserver la référence opaque exacte et les quatre membres canoniques REJECT/CREATE_ONLY/UPDATE_ONLY/UPSERT de BulkConflictStrategy.
- Valider les types exacts avant les attributs ou opérations sur les valeurs, sans conversion, effet ni écho.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : réalisation des quatre exigences BulkOperationConflict v1 existantes, reproduites verbatim dans le delta.

## Impact

Trois nouveaux fichiers : src/pixs/kernel/bulk_operation_conflict.py, tests/unit/test_bulk_operation_conflict.py et tests/integration/test_bulk_operation_conflict_integration.py. Aucun choix ou application de stratégie, résolution de conflit, mutation, idempotence, autorisation, persistance, commande ou import/export. Aucune dépendance, configuration ou opération Git ; PA/PZT conservés hors périmètre. Le rejet des conflits par défaut du contrat général d’import reste applicable.
