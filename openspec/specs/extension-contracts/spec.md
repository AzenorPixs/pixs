# extension-contracts Specification

## Purpose
Les contrats d'extension cadrent les contributions vers les points d'extension publics, côté applicatif comme côté interface, sans modifier le noyau ni les implémentations privées.

## Requirements

### Requirement: Points d'extension publics versionnés

Chaque point d'extension MUST déclarer identifiant namespacé, catégorie, version, schéma de contribution, propriétaire et garanties documentées.

#### Scenario: Contribution sans point déclaré rejetée

- **WHEN** une contribution vise un point non déclaré ou incompatible
- **THEN** la composition du périmètre concerné est refusée

### Requirement: Contributions déclarées et isolées

Chaque contribution MUST déclarer identifiant stable, composant cible, version de contrat, point d'entrée, dépendances, permissions, niveau de confiance et conditions d'activation ; elle MUST NOT importer d'implémentation privée ni modifier directement les données d'un autre composant.

#### Scenario: Accès privé bloqué

- **WHEN** une extension importe un modèle interne ou écrit dans les tables privées d'un autre module
- **THEN** le build ou l'activation bloque avec un diagnostic explicite

### Requirement: Niveau de confiance des extensions

Toute extension MUST déclarer l'un des niveaux `PLATFORM`, `TRUSTED`,
`SANDBOXED` ou `DEVELOPMENT`. `DEVELOPMENT` MUST NOT être activé en production.
`SANDBOXED` MUST limiter ses accès aux APIs, permissions et données explicitement
accordées ; ce niveau MUST NOT contourner les contrats, l'autorisation ou la gouvernance.

#### Scenario: Extension de développement en production

- **WHEN** une composition de production inclut une extension `DEVELOPMENT`
- **THEN** sa validation échoue avant activation

### Requirement: Collisions et composition déterministe

Les collisions sont refusées par défaut ; toute composition multi-contributions MUST déclarer politique de fusion, priorité et ordre déterministes ; une contribution obligatoire incompatible bloque, une optionnelle est isolée et diagnostiquée.

#### Scenario: Deux routes en collision

- **WHEN** deux contributions revendiquent le même chemin sans politique déclarée
- **THEN** la composition est refusée au lieu d'un choix arbitraire

### Requirement: Composition interface au build

Les extensions d'interface de référence MUST être composées au build depuis des sources versionnées ; aucun téléchargement, installation ni évaluation de code distant au runtime ; toute isolation (sandbox, iframe) expose une API explicitement limitée.

#### Scenario: Code distant implicite refusé

- **WHEN** une extension tente de charger du code distant non déclaré au runtime
- **THEN** le chargement est refusé et l'état FAILED est diagnostiqué

### Requirement: Frontières publiques des composants frontend imbriqués

Un parent, un sous-module et leurs composants frères MUST s'intégrer par des routes, slots, façades, événements UI ou autres points d'extension publics, namespacés et versionnés. Une contribution enfant MUST NOT être activée, fusionnée ou rendue prioritaire par effet de bord du parent ; toute politique de composition reste déclarée et déterministe.

#### Scenario: Slot enfant non déclaré

- **WHEN** un sous-module tente de contribuer à une zone d'interface privée de son parent
- **THEN** le build refuse la contribution au lieu de l'intégrer par convention d'arborescence
