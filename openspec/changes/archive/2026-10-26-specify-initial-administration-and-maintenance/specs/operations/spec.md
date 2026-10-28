## ADDED Requirements

### Requirement: Maintenance hiérarchisée

Le mode MAINTENANCE MUST pouvoir être appliqué à une portée générale couvrant
toute l'installation, granulaire couvrant un composant, module, service ou
domaine, ou sous-granulaire couvrant une capacité, route, action ou opération
précise. Chaque maintenance MUST déclarer sa portée, ses utilisateurs autorisés,
les opérations permises et interdites, sa condition de sortie et son audit.

#### Scenario: Maintenance d'une route

- **WHEN** une route est placée en maintenance sous-granulaire
- **THEN** les autres routes indépendantes restent disponibles selon leurs
  propres règles et la route concernée retourne son état contractuel
