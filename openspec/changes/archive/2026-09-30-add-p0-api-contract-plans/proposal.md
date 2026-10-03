## Why

Les contrats API portent leur majeure dans le chemin public, toute rupture impose une nouvelle majeure avec son propre document OpenAPI et une coexistence déclarée. Le socle dispose de descripteurs de contrats et de gardes SemVer pures, sans plan API réutilisant ces garanties. Ce change prépare uniquement des métadonnées testables, sans publication ni transport HTTP.

## What Changes

- Préparer `ApiContractPlan`, dataclass figée à deux champs obligatoires : un `ContractDescriptor` de catégorie API et une référence logique publique de document OpenAPI.
- Préparer `api_major_prefix` dérivant `/api/v{major}` de la version contractuelle SemVer complète, sans utiliser la version du composant, de Django ou du schéma OpenAPI.
- Préparer `check_api_evolution` réutilisant la garde publique de contrat : rupture sans majeure et baisse refusées ; une majeure croissante exige une référence de document distincte et une coexistence documentée.
- Revalider les objets exacts, y compris forgés, avec diagnostics constants sans écho et sans copie d'un parseur.
- Vérifier les cas synthétiques valides et invalides, puis les régressions unitaires et d'intégration séparées.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- api : fondation déclarative partielle de la seule exigence « Contrats OpenAPI versionnés par majeure », reprise à l'identique dans le delta, sans nouvelle norme.

## Impact

Cinq nouveaux fichiers d'implémentation : src/pixs/backend/api/contracts.py, src/pixs/backend/api/__init__.py, src/pixs/backend/api/README.md, tests/unit/test_api_contract_plans.py, tests/integration/test_api_contract_plans_integration.py. Dépendances : stdlib et APIs publiques pixs.kernel.contracts et pixs.kernel.manifest.semver ; aucune dépendance nouvelle ni modification de source existante.

Exclusions : publication effective, génération ou validation complète d'OpenAPI, transport HTTP, coexistence effective, détection sémantique automatique, enveloppes, pagination, idempotence, tenant, authentification, base, persistance, secrets, réseau, Git, runtime et installation. Un plan ne prouve ni fichier présent, ni schéma valide, ni compatibilité comportementale, ni P0 achevé. Les autres exigences API restent hors périmètre.
