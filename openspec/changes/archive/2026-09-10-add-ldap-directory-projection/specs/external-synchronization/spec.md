## MODIFIED Requirements

### Requirement: Contrat de synchronisation et autorité déclarés

Chaque synchronisation MUST déclarer direction (import, export,
bidirectionnel, projection), autorité, mappings versionnés, points de reprise
et stratégie de conflits ; le chargeur externe MUST NOT écrire directement
dans les modèles privés. Une projection LDAP des identités numériques, groupes
et appartenances MUST être déclarée sortante avec l'autorité PIXS ; elle MUST
NOT importer de mutation, de suppression ou de décision d'autorisation depuis
LDAP.

#### Scenario: Import direct refusé

- **WHEN** un connecteur tente d'écrire hors commande du module propriétaire
- **THEN** l'opération est refusée avec une erreur explicite et un audit
