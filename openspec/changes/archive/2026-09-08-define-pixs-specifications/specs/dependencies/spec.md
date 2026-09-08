## Purpose

Les dépendances explicites garantissent une composition cohérente, ordonnée et sans cycle avant toute activation.

## ADDED Requirements

### Requirement: Dépendances déclarées typées

Chaque composant DOIT déclarer dépendances composants et capacités, obligatoires et optionnelles distinguées, avec contraintes SemVer.

#### Scenario: Optionnelle absente tolérée

- **WHEN** une dépendance optionnelle est absente
- **THEN** la composition reste valide avec un comportement dégradé déclaré

### Requirement: Cycles et incompatibilités refusés

Toute dépendance obligatoire absente, incompatible ou cyclique invalide la composition avant activation.

#### Scenario: Cycle détecté

- **WHEN** A dépend de B qui dépend de A
- **THEN** la composition est refusée avec le cycle diagnostiqué

### Requirement: Ordre de chargement déterministe

L'ordre résolu DOIT être identique à composants, versions et configuration identiques, sans dépendre du système de fichiers ni des imports.

#### Scenario: Double composition identique

- **WHEN** la même composition est résolue deux fois
- **THEN** l'ordre de chargement est identique
