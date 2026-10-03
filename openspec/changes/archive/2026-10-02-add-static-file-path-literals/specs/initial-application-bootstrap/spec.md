## MODIFIED Requirements

### Requirement: Surface HTTP initiale minimale

L'application initiale MUST déclarer des routes et des vues de base séparant
la vérification de santé du shell et de l'API versionnée. Toute route publique
MUST être explicitement déclarée ; toute route non déclarée publique MUST être
protégée ou refusée. Les réponses API initiales MUST respecter les contrats
HTTP publics applicables et MUST NOT simuler une capacité métier, une
autorisation ou une identité inexistante.

#### Scenario: Route initiale non déclarée

- **WHEN** une requête vise une route qui n'est ni une route de santé, ni une
  route du shell, ni une route API explicitement déclarée
- **THEN** l'application la refuse avec une réponse sans information sensible
