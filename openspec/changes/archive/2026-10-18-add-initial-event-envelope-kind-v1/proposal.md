# Vocabulaire initial EventEnvelopeKind v1

## Why

Le canon events B11 et son schéma EventEnvelopeV1 imposent le champ kind avec les deux valeurs DOMAIN et INTEGRATION. Le backend les contrôle déjà sous forme de chaînes exactes ; aucun Enum équivalent n’existe dans les sources examinées.

## What Changes

Ajouter EventEnvelopeKind(Enum) dans le backend avec les deux noms et valeurs canoniques, sans mixin str, valeur par défaut, normalisation, façade ou branchement runtime. Vérifier son contrat public et la préservation des validateurs existants.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune évolution normative. Ce sous-lot représente uniquement le vocabulaire déjà défini par openspec/specs/events/spec.md, B11 et EventEnvelopeV1. skip_specs: true évite un delta canonique identique.

## Impact

Un nouveau module backend et deux modules de tests. Aucun validateur, record, migration, contrat, cadrage, dépendance ou export existant ne change. Ce vocabulaire ne réalise ni enregistrement, bus, outbox, publication, persistance, transaction, livraison ou qualification P0. EventPublicationState de CISMP2 et le profil PBO de CISMP3 restent hors périmètre.
