# Proposal — add-initial-bulk-command-execution-outcome-v1

## Why

Le canon bulk-operations B07 et le schéma CommandExecutionV1 imposent les trois outcomes APPLIED, REPLAYED et REJECTED, sans faux effet nouveau sur REPLAYED. Les consommateurs actuels utilisent des str exactes via validate_command_execution_values ; aucun vocabulaire central BulkCommandExecutionOutcome n’existe.

## What Changes

- Ajouter un Enum pur BulkCommandExecutionOutcome avec APPLIED = "APPLIED", REPLAYED = "REPLAYED" et REJECTED = "REJECTED".
- Sans mixin str, alias, défaut, normalisation ni modification des validateurs et consommateurs str existants.
- Vérifier le contrat fermé et l’import isolé sous gardes d’effets, avec les régressions structurelles proches.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative : bulk-operations B07 porte déjà outcome et schéma. skip_specs: true évite un delta artificiel.

## Impact

Trois fichiers Python nouveaux ; aucune façade ou source existante modifiée. Représentation partielle seule, sans validation, exécution, idempotence, persistance, outbox, autorisation ou transition. PostgreSQL et frontend sans objet pour ce vocabulaire pur.
