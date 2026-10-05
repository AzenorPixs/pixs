## MODIFIED Requirements

### Requirement: Événements immuables versionnés

Chaque événement MUST porter type, version, producteur, schéma et périmètre d'ordre déclaré ; les événements de domaine internes et d'intégration publics restent des contrats distincts.

#### Scenario: Contrat d'intégration séparé

- **WHEN** un événement de domaine est exposé vers l'extérieur
- **THEN** il passe par un contrat d'intégration versionné distinct, jamais par exposition directe
