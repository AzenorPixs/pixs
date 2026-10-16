# Proposal — add-bulk-server-cancellation-request-v1

## Why

La primitive interne `request_cancellation` (CAS, `BulkRuntimeRepository`) existe et est testée, mais aucune composition serveur n'appelle l'autorité `CANCEL` courante avant cette persistance. Une demande d'annulation ne peut donc pas être posée par la façade serveur autorisée sans terminaliser ni reprendre le worker.

## What Changes

Composer une façade serveur minimale `request_bulk_cancellation` avec types exacts avant tout comportement et I/O, vrais composants serveur (`BulkRuntimeRepository`, ports de confiance), refus fermé sans écho, contrôle d'autorité `CANCEL` sur l'opération cible avant tout SQL Bulk, puis persistance des seuls `cancellation_requested` et `revision N+1`. Aucune annulation achevée prétendue, aucun état terminal posé. B03/B06 inchangés ; le delta `bulk-operations` ajoute seulement des scénarios de preuve de demande autorisée et de refus inchangé.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `bulk-operations` : preuve de demande d'annulation autorisée via la façade serveur et refus inchangé (CAS, terminaux, concurrence préservés par la primitive).

## Impact

Fichiers nouveaux uniquement, sans modification d'existants :

- `src/pixs/backend/bulk_server_cancellation.py`
- `tests/unit/test_bulk_server_cancellation.py`
- `tests/integration/test_bulk_server_cancellation_postgres_integration.py`

Tests : types hostiles et refus d'autorité sans I/O ni écho ; PG réel isolé prouvant CAS, terminaux inchangés, rollback externe, concurrence à un seul gagnant et flag bloquant l'unité suivante. Pas de production qualifiée, ni worker, dispatch, route, APPLY, EXPORT, Git, dépendance ou déploiement. Aucune tâche cochée.
