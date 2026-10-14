## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B08 — Jobs et liaison persistante

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B08 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Phase persistante

- **WHEN** une opération IMPORT passe de STAGE à VALIDATE
- **THEN** la phase suivante possède un Job et une liaison persistants sans chevauchement actif

#### Scenario: Liaison multiple

- **WHEN** une demande veut rattacher le même Job Bulk à deux opérations
- **THEN** la contrainte refuse la seconde liaison sans modifier la première

### Requirement: Runtime Bulk v1 B09 — Baux, reprise et configuration

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B09 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Reprise sous bail

- **WHEN** un titulaire autorisé acquiert un nouveau bail après interruption
- **THEN** il reprend le dernier checkpoint engagé sous la politique et l’échéance initiales

#### Scenario: Bail périmé

- **WHEN** un ancien titulaire tente une nouvelle unité après expiration ou perte du bail
- **THEN** l’unité est refusée sans nouvel effet ni prolongation implicite
