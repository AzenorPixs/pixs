# Vocabulaire initial des états de décision d’architecture v1

## Why

La capacité canonique architecture-decisions, exigence « États traçables », nomme PROPOSED, ACCEPTED, SUPERSEDED et REJECTED. Aucun vocabulaire Python correspondant n’est présent dans les sources examinées.

## What Changes

Fournir uniquement ArchitectureDecisionState, une Enum standard sans mixin str, avec ces quatre noms et valeurs dans l’ordre canonique. Ajouter des tests de contrat et un import en processus frais sous gardes d’effets. Aucun fichier existant n’est modifié.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative. Le change implémente seulement le vocabulaire de openspec/specs/architecture-decisions/spec.md, exigence « États traçables ». skip_specs: true évite un delta identique artificiel ; la conformité au canon reste requise.

## Impact

Nouveau module pur et deux modules de tests. Sans dépendance, configuration, façade ou activation P0. Les dossiers préparatoires C00 et suivants restent inchangés. Le change ne réalise pas une décision contextualisée, ses transitions, la relation de remplacement, l’historique, la persistance ni la prévalence automatisée d’OpenSpec. Il ne clôture pas la capacité entière.
