# Vocabulaire initial BulkAuthorityAction v1

## Why

Le canon bulk-operations B03 et le contrat AuthorityPort déclarent les actions ADMIT, EXECUTE, CANCEL et READ_RESULT. Le port serveur vérifie déjà ces chaînes exactes ; aucun Enum équivalent n’existe dans les sources examinées.

## What Changes

Ajouter BulkAuthorityAction(Enum) avec les quatre noms et valeurs canoniques, sans mixin str, défaut, normalisation, classement ordinal, façade ni branchement runtime. Vérifier le contrat public et la frontière existante du port.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune évolution normative. Ce sous-lot représente uniquement le vocabulaire déjà défini dans openspec/specs/bulk-operations/spec.md, B03 et contrat AuthorityPort. skip_specs: true évite un delta canonique identique.

## Impact

Un nouveau module backend et deux modules de tests. Aucun contrat, validateur, port, migration, cadrage, dépendance ou export existant ne change. Représenter une action ne réalise aucune autorisation, admission, exécution, annulation, lecture de résultat, persistance ou preuve P0. Les autres RUN restent hors périmètre.
