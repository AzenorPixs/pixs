## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B04 — Staging privé et intégrité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B04 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Objet vérifié

- **WHEN** un objet privé immuable satisfait les contrôles de taille, type, classification et SHA-256
- **THEN** son contenu peut être traité sous sa version stable et les limites déclarées

#### Scenario: Intégrité rompue

- **WHEN** le checksum ou la version observée diffère du contenu attendu
- **THEN** le traitement est refusé avant tout appel propriétaire, sans copie de secours locale
