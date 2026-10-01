# Proposal

## Why

La spécification `testing` exige un composant d'exemple P0 démontrant composition par contrats, contexte tenant/scope et autorisation, sans devenir dépendance de production. Aucun exemple n'existe (`src/pixs/**/example*` vide) alors que toutes les fondations mémoire sont présentes (composition, manifests, scope, PDP, filter-plan). Sans cet exemple, le sous-ensemble démonstratif reste non prouvé.

## What Changes

- Exemple P0 synthétique `example.hello` (namespace démonstratif, jamais `pixs.*`, jamais contrat de production) : `component.toml` schéma 1 (MODULE 1.0.0, capacité `example.hello` 1.0.0, contrat `example.hello.contract` 1.0.0), `demo.py` fonctions pures via APIs publiques existantes (parse/compose/scope/authz, ports injectés), `README.md` parcours reproductible via validateurs existants.
- Six fichiers exacts : `src/pixs/example/__init__.py`, `src/pixs/example/component.toml`, `src/pixs/example/demo.py`, `src/pixs/example/README.md`, `tests/unit/test_example_component.py`, `tests/integration/test_example_composition.py`.
- Tests mémoire/doubles uniquement, attestations synthétiques tests-only (`synthetic_attestations`), jamais de PASS préfabriqué en source ; preuves bornées au sous-ensemble, sans conformité P0 globale ni Developer Kit complet ni intégration réelle de référence.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `testing` : traçabilité d'implémentation du composant d'exemple, sans nouvelle exigence canonique.

## Impact

- Code : 4 fichiers exemple (façade, TOML, démo, README). Tests : 2 fichiers (unitaires, intégration mémoire). Exclus : backend Django, PostgreSQL, CLI/Developer Kit complet, providers concrets, frontend, persistance, audit durable, dépendances nouvelles, runtime complet, P0 global.
