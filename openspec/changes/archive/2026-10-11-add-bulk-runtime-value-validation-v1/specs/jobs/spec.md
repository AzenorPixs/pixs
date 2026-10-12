## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B09 — Baux, reprise et configuration

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B09 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Reprise sous bail

- **WHEN** un titulaire autorisé acquiert un nouveau bail après interruption
- **THEN** il reprend le dernier checkpoint engagé sous la politique et l’échéance initiales

#### Scenario: Bail périmé

- **WHEN** un ancien titulaire tente une nouvelle unité après expiration ou perte du bail
- **THEN** l’unité est refusée sans nouvel effet ni prolongation implicite
