## MODIFIED Requirements

### Requirement: Shell TanStack initial intégré

Le frontend initial MUST fournir un shell TanStack construit séparément et
servi par la composition de développement déclarée. Le shell MUST consommer
uniquement la surface HTTP publique déclarée et MUST NOT accéder directement à
PostgreSQL, aux secrets, aux réglages Django privés ou aux implémentations
internes de `pixs.kernel` et `pixs.core`.

#### Scenario: Démarrage du shell initial

- **WHEN** la composition de développement démarre avec le frontend initial
- **THEN** le shell est accessible et ses appels utilisent exclusivement les
  routes HTTP déclarées
