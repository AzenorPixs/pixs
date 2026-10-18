# Vocabulaire initial des états de publication d’événement v1

## Why

Le canon `events`, B11 « Outbox et publication » et `OutboxPublicationV1`, fixe les états `PENDING`, `PUBLISHED`, `RETRYING`, `FAILED` et `DEAD_LETTER`. Le validateur Bulk les contrôle déjà sous forme de chaînes, mais aucun vocabulaire Python Enum correspondant n’existe dans les sources examinées.

## What Changes

Fournir uniquement `EventPublicationState`, Enum standard sans mixin `str`, avec ces cinq noms et valeurs dans l’ordre canonique. Ajouter des tests de contrat et d’import en processus frais sous gardes d’effets. Aucun fichier existant n’est modifié.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative. Ce change réalise seulement le vocabulaire de `openspec/specs/events/spec.md`, B11 et `OutboxPublicationV1`. `skip_specs: true` évite un delta identique artificiel ; la conformité au canon reste obligatoire.

## Impact

Un module pur du backend et deux modules de tests. Aucune dépendance, configuration, migration ou modification de façade. Aucun branchement aux validateurs ou modèles existants. Aucun publisher, outbox, inbox, bail, séquence, politique, autorisation ou activation P0. Les changes O11/O12 et C00 restent hors périmètre. Ce vocabulaire ne clôture pas la capacité `events` entière.
