## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B10 — Idempotence durable

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B10 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Rejeu identique

- **WHEN** la même clé d’admission est présentée avec le même contenu initial
- **THEN** l’opération initiale est rendue après contrôle actuel sans second effet

#### Scenario: Rejeu divergent

- **WHEN** la même clé est présentée avec un fingerprint différent
- **THEN** un conflit explicite est persisté ou retourné sans mutation propriétaire
