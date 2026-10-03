## MODIFIED Requirements

### Requirement: Signaux structurés et corrélés

Chaque composant MUST émettre journaux structurés, métriques, traces et contrôles de santé avec identifiants de corrélation et de trace ; les signaux restent compatibles OpenTelemetry avec propagation W3C lorsque le transport le permet.

#### Scenario: Corrélation bout en bout

- **WHEN** une requête traverse plusieurs composants
- **THEN** journaux, métriques et traces partagent les identifiants de corrélation sans exposer de secret
