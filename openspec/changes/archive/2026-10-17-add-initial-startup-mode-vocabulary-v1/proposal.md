# Vocabulaire initial des modes de démarrage v1

## Why

Le canon initial-administration impose les modes INSTALLER, FIRST_CONFIGURATION, NORMAL et MAINTENANCE. Aucune représentation de ce vocabulaire n’est présente dans les sources examinées.

## What Changes

Ajouter StartupMode, Enum standard sans mixin str, avec ces quatre noms et valeurs dans leur ordre canonique. Vérifier le contrat public, le refus des valeurs non déclarées et l’import sans effets observables en processus frais.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune évolution normative. Ce sous-lot réalise uniquement le vocabulaire de openspec/specs/initial-administration/spec.md, exigence « Modes de démarrage explicites ». La métadonnée skip_specs: true évite un delta canonique identique.

## Impact

Un nouveau module backend et deux modules de tests. Aucune dépendance, configuration, migration, façade, sélection automatique ou activation runtime. Les changes préparatoires C00 et C08 restent inchangés. Le marqueur externe, la première configuration persistante, les transitions autorisées/auditées et les parcours d’installation restent à réaliser ; ce vocabulaire ne prouve pas leur fonctionnement ni une livraison P0.
