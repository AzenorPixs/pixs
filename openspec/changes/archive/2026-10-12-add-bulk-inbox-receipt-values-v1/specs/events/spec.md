## MODIFIED Requirements

### Requirement: Runtime Bulk v1 B11 — Outbox et publication

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B11 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Rollback sans publication

- **WHEN** la transaction propriétaire qui écrit l’événement est annulée
- **THEN** l’événement n’est pas disponible à la publication

#### Scenario: Livraison répétée

- **WHEN** une interruption survient après émission mais avant accusé persistant
- **THEN** une répétition reste possible et l’inbox empêche un second effet confirmé
