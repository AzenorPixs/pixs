## Why
Les clauses B02 et B09 du runtime Bulk v1 sont validées. Leur application nécessite de refuser les valeurs étrangères avant parsing ou I/O, sans changer les profils Kernel livrés.

## What Changes
- Ajouter les validateurs purs des 36 valeurs d'exécution, de ProgressV1 et de PolicyV1.
- Prouver les types hostiles, les contraintes croisées, l'absence de coercition et d'effets.
- Garder la persistance, les baux, l'autorité et l'exécution pour les changes suivants du même cycle.

## Capabilities
### New Capabilities
Aucune.

### Modified Capabilities
- bulk-operations : première couverture de validation mémoire des données B02.
- jobs : validation mémoire de la politique B09.

## Impact
Trois nouveaux fichiers Python ; aucune dépendance, configuration, table, donnée ni source existante modifiée. Ce lot ne livre pas l'ensemble de B02 ou B09.
