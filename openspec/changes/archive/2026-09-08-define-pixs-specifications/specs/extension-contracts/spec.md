## Purpose

Les contrats d'extension cadrent les contributions vers les points d'extension publics, côté applicatif comme côté interface, sans modifier le noyau ni les implémentations privées.

## ADDED Requirements

### Requirement: Points d'extension publics versionnés

Chaque point d'extension DOIT déclarer identifiant namespacé, catégorie, version, schéma de contribution, propriétaire et garanties documentées.

#### Scenario: Contribution sans point déclaré rejetée

- **WHEN** une contribution vise un point non déclaré ou incompatible
- **THEN** la composition du périmètre concerné est refusée

### Requirement: Contributions déclarées et isolées

Chaque contribution DOIT déclarer identifiant stable, composant cible, version de contrat, point d'entrée, dépendances, permissions, niveau de confiance et conditions d'activation ; elle NE DOIT ni importer d'implémentation privée ni modifier directement les données d'un autre composant.

#### Scenario: Accès privé bloqué

- **WHEN** une extension importe un modèle interne ou écrit dans les tables privées d'un autre module
- **THEN** le build ou l'activation bloque avec un diagnostic explicite

### Requirement: Collisions et composition déterministe

Les collisions sont refusées par défaut ; toute composition multi-contributions DOIT déclarer politique de fusion, priorité et ordre déterministes ; une contribution obligatoire incompatible bloque, une optionnelle est isolée et diagnostiquée.

#### Scenario: Deux routes en collision

- **WHEN** deux contributions revendiquent le même chemin sans politique déclarée
- **THEN** la composition est refusée au lieu d'un choix arbitraire

### Requirement: Composition interface au build

Les extensions d'interface de référence DOIVENT être composées au build depuis des sources versionnées ; aucun téléchargement, installation ni évaluation de code distant au runtime ; toute isolation (sandbox, iframe) expose une API explicitement limitée.

#### Scenario: Code distant implicite refusé

- **WHEN** une extension tente de charger du code distant non déclaré au runtime
- **THEN** le chargement est refusé et l'état FAILED est diagnostiqué
