## Purpose

Les capacités décrivent les comportements fournis et requis par les composants, résolus avant activation indépendamment de tout ordre de découverte.

## ADDED Requirements

### Requirement: Descripteur de capacité résolu à la composition

Chaque capacité DOIT déclarer identifiant, version, composant propriétaire, références de contrats, fournisseur éventuel, criticité et politique de repli ; la résolution intervient avant activation sans dépendre du système de fichiers ni des imports.

#### Scenario: Résolution indépendante de l'ordre

- **WHEN** la même composition est découverte dans deux ordres différents
- **THEN** le graphe de capacités résolu est identique

### Requirement: États de disponibilité distincts

La disponibilité SUIT DECLARED vers RESOLVED vers AVAILABLE, avec DEGRADED, DISABLED et BLOCKED ; une capacité obligatoire non AVAILABLE bloque l'activation, une optionnelle reste isolée avec repli déclaré.

#### Scenario: Capacité optionnelle indisponible isolée

- **WHEN** une capacité optionnelle est absente ou incompatible
- **THEN** le composant reste valide avec un comportement dégradé déclaré et diagnostiqué

### Requirement: Fanion ne remplace pas la résolution

Un fanion de fonctionnalité NE DOIT jamais remplacer la résolution d'une capacité ni rendre compatible un contrat incompatible.

#### Scenario: Fanion sans fournisseur refusé

- **WHEN** un fanion est actif mais aucun fournisseur compatible n'est résolu
- **THEN** la capacité reste BLOCKED et l'activation est refusée
