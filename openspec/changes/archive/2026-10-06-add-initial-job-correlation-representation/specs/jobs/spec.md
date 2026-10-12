# jobs

## MODIFIED Requirements

### Requirement: Idempotence et corrélation des travaux

Chaque travail MUST porter identifiants distincts du commandement et de l'opération, corrélation, causalité et périmètre, avec déduplication persistante lorsque nécessaire.

#### Scenario: Double déclenchement dédupliqué

- **WHEN** le même travail est déclenché deux fois
- **THEN** un seul effet métier confirmé est produit et le doublon est tracé
