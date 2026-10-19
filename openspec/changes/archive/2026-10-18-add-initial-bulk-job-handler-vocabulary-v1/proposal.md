# Proposal — add-initial-bulk-job-handler-vocabulary-v1

## Why

Le canon jobs B08 impose les quatre noms de handlers Bulk et leur version 1.0.0. Les consommateurs actuels utilisent des littéraux ; aucun vocabulaire central BulkJobHandler n’existe.

## What Changes

- Ajouter un Enum pur BulkJobHandler avec STAGE = "pixs.bulk.stage", VALIDATE = "pixs.bulk.validate", APPLY = "pixs.bulk.apply" et EXPORT = "pixs.bulk.export".
- Exposer BULK_JOB_HANDLER_VERSION = "1.0.0", sans mixin str, alias ni défaut.
- Vérifier le contrat fermé et l’import isolé sous gardes d’effets, avec les régressions structurelles proches.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative : jobs B08 porte déjà noms et version. skip_specs: true évite un delta artificiel.

## Impact

Trois fichiers Python nouveaux ; aucune façade ou source existante modifiée. Représentation partielle seule, sans worker, enregistrement, transition, persistance, liaison, bail, autorisation ou exécution. La version déclarée ne prouve aucune compatibilité runtime. PostgreSQL et frontend sans objet pour ce vocabulaire pur.
