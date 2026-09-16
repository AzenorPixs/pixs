# dependencies Specification

## Purpose
Les dépendances explicites garantissent une composition cohérente, ordonnée et sans cycle avant toute activation.

## Requirements

### Requirement: Dépendances déclarées typées

Chaque composant MUST déclarer dépendances composants et capacités, obligatoires et optionnelles distinguées, avec contraintes SemVer.

#### Scenario: Optionnelle absente tolérée

- **WHEN** une dépendance optionnelle est absente
- **THEN** la composition reste valide avec un comportement dégradé déclaré

### Requirement: Cycles et incompatibilités refusés

Le système MUST respecter les garanties suivantes.

Toute dépendance obligatoire absente, incompatible ou cyclique invalide la composition avant activation.

#### Scenario: Cycle détecté

- **WHEN** A dépend de B qui dépend de A
- **THEN** la composition est refusée avec le cycle diagnostiqué

### Requirement: Ordre de chargement déterministe

L'ordre résolu MUST être identique à composants, versions et configuration identiques, sans dépendre du système de fichiers ni des imports.

#### Scenario: Double composition identique

- **WHEN** la même composition est résolue deux fois
- **THEN** l'ordre de chargement est identique

### Requirement: Graphe frontend récursif et façades publiques

Le résolveur MUST intégrer les contributions frontend des modules et sous-modules dans le graphe de composants commun, vérifier leurs contraintes SemVer, leurs dépendances obligatoires et optionnelles, et n'autoriser que les façades frontend publiques déclarées par le shell, le Design System ou un composant. Les chemins physiques, l'ordre des imports et l'arborescence parent-enfant MUST NOT créer de dépendance ou de priorité implicite.

#### Scenario: Import privé d'un parent refusé

- **WHEN** un sous-module frontend dépend d'un store ou d'une implémentation privée de son parent sans façade publique déclarée
- **THEN** la composition est refusée avant exposition avec un diagnostic du contrat manquant
