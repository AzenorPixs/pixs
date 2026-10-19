# Proposal — add-initial-component-type-vocabulary-v1

## Why

Le canon component-model impose les six types KERNEL, MODULE, SUBMODULE, PROVIDER, EXTENSION et THEME avec les mêmes mécanismes de manifest et de cycle de vie. Aucun vocabulaire central ComponentType n’existe ; les consommateurs comparent des littéraux au frozenset COMPONENT_TYPES du chargeur de manifest.

## What Changes

- Ajouter un Enum pur ComponentType avec KERNEL = "KERNEL", MODULE = "MODULE", SUBMODULE = "SUBMODULE", PROVIDER = "PROVIDER", EXTENSION = "EXTENSION" et THEME = "THEME".
- Exposer uniquement ComponentType via __all__, sans mixin str, alias, défaut, version, runtime, persistance ni modification des façades et sources existantes.
- Vérifier le contrat fermé, le refus sans normalisation, la cohérence avec COMPONENT_TYPES sans accepter les membres Enum dans parse_manifest, et l’import isolé sous gardes d’effets, avec les régressions structurelles proches.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune modification normative : component-model porte déjà les six types. skip_specs: true évite un delta artificiel.

## Impact

Trois fichiers Python nouveaux ; aucune façade ou source existante modifiée. Représentation partielle seule, sans registre, résolution, transition, validation métier, autorisation, exécution ou persistance. PostgreSQL et frontend sans objet pour ce vocabulaire pur.
