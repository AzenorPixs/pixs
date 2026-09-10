## ADDED Requirements

### Requirement: Frontières publiques des composants frontend imbriqués

Un parent, un sous-module et leurs composants frères MUST s'intégrer par des routes, slots, façades, événements UI ou autres points d'extension publics, namespacés et versionnés. Une contribution enfant MUST NOT être activée, fusionnée ou rendue prioritaire par effet de bord du parent ; toute politique de composition reste déclarée et déterministe.

#### Scenario: Slot enfant non déclaré

- **WHEN** un sous-module tente de contribuer à une zone d'interface privée de son parent
- **THEN** le build refuse la contribution au lieu de l'intégrer par convention d'arborescence
