## Why

BulkOperationFormat v1 est désormais défini dans la spécification validée bulk-operations, mais sa représentation et sa validation pure ne sont pas implémentées. Ce change réalise seulement ce profil préparatoire.

## What Changes

- Ajouter un profil Python immuable à deux champs explicitement fournis : operation_id et format.
- Conserver la référence opaque exacte et les seuls membres canoniques CSV/NDJSON de BulkReferenceFormat.
- Valider les types exacts avant les attributs ou opérations sur les valeurs, sans conversion, effet ni écho.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : réalisation des quatre exigences BulkOperationFormat v1 existantes, reproduites verbatim dans le delta.

## Impact

Trois nouveaux fichiers : src/pixs/kernel/bulk_operation_format.py, tests/unit/test_bulk_operation_format.py et tests/integration/test_bulk_operation_format_integration.py. Aucun parsing, I/O métier, choix de format, résolution d'adaptateur, compatibilité, autorisation, persistance, runtime import/export, dépendance, configuration ou Git. Intégration et spécifications PA/PZT conservées hors périmètre.
