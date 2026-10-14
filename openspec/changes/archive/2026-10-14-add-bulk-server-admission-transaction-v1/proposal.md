## Why

Les primitives persistantes Bulk existent, mais leur assemblage d’admission serveur B01 n’est pas livré. Le retour de `operation_id` doit suivre l’engagement atomique de l’opération, de la demande, du premier Job et de leur liaison.

## What Changes

- Réutiliser GovernanceResolutionV1 pour résoudre effectivement la gouvernance d'admission avant SQL, avec contexte lié à l'autorité courante, PolicyV1 et DataGovernanceProfile existants ; un profil structurel seul ne vaut jamais résolution.
- Ajouter un service interne d’admission IMPORT/EXPORT asynchrone, limité à CSV et NDJSON et à un tenant résolu par l’autorité serveur.
- Réutiliser les ports composés et les validateurs existants, vérifier autorité et gouvernance avant tout accès en base.
- Assembler les primitives persistantes existantes dans une transaction Django unique, avec identité et snapshot d’admission B10, premier Job et liaison B08.
- Prouver le rejeu identique, le conflit de contenu, le rollback et l’isolation par tests unitaires et PostgreSQL réels.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `bulk-operations` : implémentation interne de l’admission du contrat B01 déjà validé, sans nouvelle norme.

## Impact

Fichiers prévus : `src/pixs/backend/bulk_server_admission.py`, `tests/unit/test_bulk_server_admission.py` et `tests/integration/test_bulk_server_admission_postgres_integration.py`.

Aucune dépendance, migration de production, route HTTP, implémentation de worker ou modification des profils Kernel/Record. Les tests PostgreSQL utilisent un schéma isolé avec nettoyage et fermeture des connexions prouvés. Le défaut de l’ancien harness JobRecord et les trois avertissements de longueur canoniques restent qualifiés séparément.
