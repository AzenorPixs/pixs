# bulk-operations Delta

## MODIFIED Requirements

### Requirement: Contrat BulkOperation suivi par operation_id

Chaque opération MUST suivre un contrat versionné avec variantes IMPORT et EXPORT, états, rattachement à operation_id, travaux persistants, tenant et scope ; les formats de référence sont CSV et NDJSON, tout autre format via adaptateur déclaré.

#### Scenario: Suivi distinct des travaux

- **WHEN** une opération longue dépasse le seuil synchrone
- **THEN** elle retourne un operation_id suivi, distinct des identifiants des travaux qui l'exécutent
