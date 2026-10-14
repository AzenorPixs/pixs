## Why
Le canon Bulk v1 B02 enveloppe/CAS et B06 machine coopérative est validé. Le flag `cancellation_requested` existe en extension 27 champs mais aucune primitive interne ne permet de le poser après autorisation de la couche supérieure sans décider un CANCEL autoritatif.

## What Changes
- Ajouter une primitive interne de stockage `request_cancellation(*, operation_id, expected_revision)` qui pose `cancellation_requested=True` avec `revision+1` sous CAS, sans argument temporel ni transition d'état.
- Ajouter tests unitaires type-avant-I/O et tests PostgreSQL isolés de persistance, CAS, concurrence et conservation checkpoints/progrès/baux.
- Reproduire en delta les Requirements B02 et B06 verbatim, sans norme nouvelle ni reformulation.

## Capabilities
### New Capabilities
Aucune.

### Modified Capabilities
- bulk-operations : couverture persistante de B02/B06 déjà normatifs, sans champ ni effet nouveau.

## Impact
Trois fichiers code/tests : `src/pixs/backend/bulk_runtime_repository.py`, `tests/unit/test_bulk_cancellation_request.py`, `tests/integration/test_bulk_cancellation_request_integration.py`. Aucun modèle, migration, port, dépendance, canon ou cadrage modifié. Aucune route HTTP, provider concret, worker ou déploiement.
