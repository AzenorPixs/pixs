## Why
Les neuf valeurs stockées du socle BulkOperationRecord v1 sont validées dans le canon, sans validateur pur encore implémenté.

## What Changes
- Ajouter uniquement validate_bulk_operation_record_values et ses preuves.
- Contrôler dict, clés, types et valeurs canoniques avant toute utilisation.
- Réserver modèle Django, migration et PostgreSQL au change suivant.

## Capabilities
### New Capabilities
Aucune.

### Modified Capabilities
- bulk-operations : implémenter les valeurs explicites, références, version, enums stockés, validation pure et limites déjà canoniques.

## Impact
Trois nouveaux fichiers Python seulement ; aucun code ORM, dépendance, configuration ou fichier existant modifié.
