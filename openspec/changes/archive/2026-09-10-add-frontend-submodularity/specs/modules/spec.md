## ADDED Requirements

### Requirement: Propriété des contributions frontend modulaires

Un MODULE ou SUBMODULE qui déclare une facette frontend MUST être propriétaire de ses contributions, traductions et façades publiques associées. Il MUST les exposer par son manifest et ses contrats versionnés, sans modifier le shell, le parent ou un composant frère ; les mutations restent exclusivement exécutées par les API et Commands publiques autorisées.

#### Scenario: Sous-module autonome intégré

- **WHEN** un sous-module fournit une page, une navigation et des traductions déclarées
- **THEN** le shell les compose sous l'identité du sous-module sans les transformer en implémentation privée du parent
