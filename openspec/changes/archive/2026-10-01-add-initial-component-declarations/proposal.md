# Déclarations initiales des composants

## Why

Les composants `pixs.kernel` et `pixs.core` sont déclarés par les normes mais n'ont aucun manifest, ce qui empêche toute composition déclarée avec le seul exemple inchangé. Ce premier jalon déclaratif fournit ces manifests et les données de composition version 0.1.0, sans activation ni P0/Django/HTTP annoncé prêt.

## What Changes

- Ajouter `src/pixs/kernel/component.toml` (KERNEL 0.1.0) et `src/pixs/core/component.toml` (MODULE 0.1.0 dépendant de `pixs.kernel`), sans capacité ni contrat injustifié.
- Ajouter `src/pixs/backend/composition_initial.py` comme données pures version 0.1.0 avec 3 chemins relatifs, `official_ids` kernel/core et `required_ids` kernel/core/example pour empêcher tout retrait de l'exemple, sans règle ajoutée au Kernel.
- Ajouter `tests/unit/test_initial_component_declarations.py` en unittest sans base ni secret, et documenter les limites dans `src/pixs/backend/README.md`.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : premier jalon déclaratif des composants existants, reprise normative inchangée.

## Impact

Cinq futurs fichiers exactement, dépendances inchangées (Django 5.2.17, psycopg 3.3.5), tests unittest sans base ni secret, aucune activation ni attestation fabriquée.
