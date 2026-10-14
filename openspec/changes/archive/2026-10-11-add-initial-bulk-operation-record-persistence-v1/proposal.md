## Why
Le canon BulkOperationRecord v1 et son validateur pur définissent neuf valeurs explicites ; leur socle Django et PostgreSQL reste à livrer.

## What Changes
- Ajouter le modèle préparatoire interne à neuf colonnes, son constructeur non sauvegardant et full_clean explicite avant conversion.
- Enregistrer le modèle sans élargir les exports existants.
- Ajouter uniquement la migration 0003 réversible et des preuves offline/PG isolées.

## Capabilities
### New Capabilities
Aucune.

### Modified Capabilities
- bulk-operations : réaliser le modèle, la validation ORM explicite, les contraintes persistantes et les limites déjà canoniques.

## Impact
Quatre nouveaux fichiers Python et un import de registration dans models.py ; aucune dépendance ou configuration nouvelle. La migration crée seulement backend_bulkoperationrecord.
