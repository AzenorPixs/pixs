# Conception des déclarations initiales

## Context

Les normes déclarent `pixs.kernel` et `pixs.core` sans manifests, avec le seul exemple inchangé. Aucune activation ne peut être prétendue.

## Goals / Non-Goals

Déclarer les deux manifests schéma 1 versions 0.1.0 et les données de composition 0.1.0. Aucune P0 valide, globalement compatible ou readiness n'est visée. Aucune modification du noyau, de l'exemple ou de la configuration réelle.

## Decisions

- `src/pixs/kernel/component.toml` : schéma 1, `pixs.kernel`, KERNEL 0.1.0, sans capacité ni contrat.
- `src/pixs/core/component.toml` : schéma 1, `pixs.core`, MODULE 0.1.0, dépendance `pixs.kernel ==0.1.0`, sans capacité ni contrat injustifié.
- `src/pixs/backend/composition_initial.py` : données pures, 3 chemins relatifs, `official_ids` kernel/core, `required_ids` kernel/core/example.
- Exemple 1.0.0 inchangé, fonctions publiques `discover`/`validate`/`resolve`/`compose` seules, zéro attestation produite.

## Files

src/pixs/kernel/component.toml, src/pixs/core/component.toml, src/pixs/backend/composition_initial.py, tests/unit/test_initial_component_declarations.py, src/pixs/backend/README.md.

## Validation

Tests unittest en mémoire sans base ni secret ni réseau, syntaxe Python en mémoire, strict OpenSpec avant et après, régressions séparées `tests/unit` et `tests/integration` via `.venv-backend-foundation` existante. Précédence kernel avant core et égalité ordre/graphe sur deux compositions seulement, aucun ordre global arbitraire. `compose` sans attestations refuse l'activation. Limite projet, sans base ni secret ni réseau.
