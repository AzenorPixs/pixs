# search Specification

## Purpose
La recherche repose sur des projections reconstruisibles et remplaçables, filtrées par autorisation à la source, sans devenir une source de vérité.

## Requirements

### Requirement: Projections dérivées reconstruisibles

Les index MUST dériver de la source de vérité via des projections versionnées, reconstruisibles et invalidées lors des changements de permissions, suppressions ou expirations.

#### Scenario: Permission révoquée propagée

- **WHEN** une permission est révoquée ou une ressource supprimée
- **THEN** la projection correspondante est mise à jour ou invalidée avant toute exposition

### Requirement: Filtrage autorisé à la source

Toute requête MUST appliquer le tenant, l'identité et les ACL à la source avant pagination, facettes ou autocomplétion ; aucun filtrage frontal ne remplace ce contrôle.

#### Scenario: Résultat hors périmètre exclu

- **WHEN** un index contient des documents hors périmètre
- **THEN** ils sont exclus avant pagination sans être chargés côté client

### Requirement: Cohérence et dégradation déclarées

Le système MUST respecter les garanties suivantes.

Cohérence éventuelle, disponibilité dégradée et limites de pertinence sont déclarées par capacité ; le moteur concret reste remplaçable sous contrat stable.

#### Scenario: Moteur dégradé diagnostiqué

- **WHEN** le moteur est indisponible avec un mode dégradé déclaré
- **THEN** un état contrôlé est retourné au lieu d'un résultat silencieux incomplet
