# Proposal — add-initial-capability-criticality-vocabulary-v1

## Why

Le canon component-model impose pour le schéma 1 une criticité REQUIRED ou OPTIONAL avec repli explicite ("none" si REQUIRED, non vide si OPTIONAL), et le canon capabilities exige criticité et repli résolus avant activation. Aucun vocabulaire central CapabilityCriticality n'existe ; les consommateurs comparent des littéraux au frozenset CRITICALITIES du chargeur de manifest.

## What Changes

- Ajouter un Enum pur CapabilityCriticality avec REQUIRED = "REQUIRED" et OPTIONAL = "OPTIONAL".
- Exposer uniquement CapabilityCriticality via __all__, sans mixin str, alias, défaut, version, runtime, persistance ni modification des façades et sources existantes.
- Vérifier le contrat fermé, le refus sans normalisation, la cohérence avec CRITICALITIES sans accepter les membres Enum dans parse_manifest, la préservation des règles fallback REQUIRED/OPTIONAL, et l'import isolé sans Django ni réseau/commandes, avec les régressions structurelles proches.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative : component-model et capabilities portent déjà REQUIRED et OPTIONAL. skip_specs: true évite un delta artificiel.

## Impact

Deux fichiers Python nouveaux ; aucune façade ou source existante modifiée. Représentation partielle seule, sans registre, résolution, transition, validation métier, autorisation, exécution ou persistance. PostgreSQL et frontend sans objet pour ce vocabulaire pur.
