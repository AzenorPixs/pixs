## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B12 — Export et résultats

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B12 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Résultat gouverné

- **WHEN** une projection propriétaire autorisée fournit sa consistance déclarée
- **THEN** un objet privé et un manifeste complet sont engagés avant disponibilité du résultat

#### Scenario: Résultat non résolu

- **WHEN** la consistance, la gouvernance ou l’autorisation du résultat ne peut être résolue
- **THEN** l’action concernée est refusée sans présentation d’un export complet
