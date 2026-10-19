# Proposition — add-initial-bulk-export-consistency-kind-v1

## Why

Le canon bulk-operations B12 et ExportManifestV1 fixent SNAPSHOT et WATERMARK. Les validateurs existants utilisent ces chaînes ; aucun vocabulaire public BulkExportConsistencyKind n’existe.

## What Changes

- Ajouter un Enum pur BulkExportConsistencyKind avec SNAPSHOT et WATERMARK, valeurs identiques aux noms, sans mixin str ni alias.
- Vérifier le contrat et l’import frais sous gardes d’effets.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative : bulk-operations B12 et ExportManifestV1 portent déjà ces deux valeurs. skip_specs: true évite un delta artificiel.

## Impact

Trois fichiers Python nouveaux ; aucune façade, migration ou utilisation existante modifiée. Représentation seule, sans résolution de consistance, export, gouvernance, persistance, autorisation ou garantie runtime. PostgreSQL et frontend sans objet.
