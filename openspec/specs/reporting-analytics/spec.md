# reporting-analytics Specification

## Purpose

Le reporting et l'analytique produisent des modèles de lecture, des rapports et
des exports gouvernés sans dédoubler l'autorité métier ou les droits d'accès.

## Requirements

### Requirement: Projections analytiques dérivées et propriétaires

Chaque projection analytique MUST déclarer son composant propriétaire, ses
sources, son schéma, sa fraîcheur, sa reconstruction et sa lignée. Une
projection MUST NOT devenir la source de vérité d'une ressource métier.

#### Scenario: Projection reconstruite

- **WHEN** une projection est invalidée ou perdue
- **THEN** elle est reconstruite depuis les sources et événements autorisés avec un état de fraîcheur explicite

### Requirement: Couche sémantique versionnée

Les métriques, dimensions, définitions de rapport et filtres autorisés MUST
être versionnés et testables. Une métrique ambiguë ou incompatible MUST être
refusée avant publication d'un rapport ou d'un tableau de bord.

#### Scenario: Définition de métrique modifiée

- **WHEN** une métrique change de sens ou de calcul de manière incompatible
- **THEN** une nouvelle version est publiée sans réécrire silencieusement les résultats précédents

### Requirement: Filtrage, gouvernance et résidence à la source

Toute requête analytique et tout rapport MUST appliquer le ScopeContext,
l'autorisation, la classification, la résidence et la minimisation avant toute
agrégation ou exposition. Un tableau de bord MUST NOT déduire ou révéler une
donnée non accessible par ses résultats agrégés.

#### Scenario: Agrégat inter-tenant non autorisé

- **WHEN** un rapport demande des données de plusieurs tenants sans droit plateforme explicite
- **THEN** la requête est refusée ou limitée au périmètre autorisé

### Requirement: Exports et rapports asynchrones contrôlés

Un rapport coûteux ou un export MUST utiliser une opération persistante avec
durée de conservation, audit et révocation. Son résultat MUST être filtré,
gouverné et stocké via les providers déclarés.

#### Scenario: Autorisation révoquée pendant un export

- **WHEN** le droit du demandeur est retiré avant la remise du résultat
- **THEN** le résultat est refusé ou révoqué selon la politique déclarée
