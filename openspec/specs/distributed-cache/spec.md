# distributed-cache Specification

## Purpose

Le cache distribué accélère les lectures et traitements dérivés tout en
préservant PostgreSQL, Django et les contrats applicatifs comme autorités.

## Requirements

### Requirement: Cache uniquement dérivé et reconstruisible

Une entrée de cache MUST être dérivée d'une source autoritative ou d'une
projection reconstruisible. Un CacheProvider MUST NOT devenir la source de
vérité d'une mutation, d'une autorisation, d'une idempotence ou d'un état de
Job persistant.

#### Scenario: Perte complète du cache

- **WHEN** toutes les entrées d'un cache sont indisponibles ou supprimées
- **THEN** le système reconstruit les lectures depuis leurs sources autoritatives selon le mode déclaré

### Requirement: Partitionnement et autorisation conservés

Les clés, tags et partitions MUST intégrer tenant, scope, identité, version et
classification lorsque ces dimensions sont applicables. Une lecture depuis le
cache MUST réappliquer les contrôles d'autorisation nécessaires.

#### Scenario: Changement de tenant

- **WHEN** une identité change de tenant ou de scope
- **THEN** elle ne peut pas réutiliser une entrée du périmètre précédent

### Requirement: Invalidation déterministe et traçable

Les mutations, révocations, tombstones et changements de politique MUST
invalider ou rendre non lisibles les entrées dérivées concernées. Une
invalidation échouée MUST être diagnostiquée et ne doit pas prolonger une
décision positive au-delà de sa politique de fraîcheur.

#### Scenario: Permission révoquée

- **WHEN** une permission donnant accès à une ressource est retirée
- **THEN** les entrées associées ne servent plus cette ressource à l'identité concernée

### Requirement: Dégradation et protection contre l'avalanche

Le CacheProvider MUST déclarer ses TTL, limites, stratégie anti-stampede et
mode de dégradation. Une indisponibilité de cache MUST NOT produire une donnée
hors périmètre ni masquer l'échec d'une source autoritative obligatoire.

#### Scenario: Expiration concurrente

- **WHEN** de nombreuses lectures atteignent une entrée expirée simultanément
- **THEN** la stratégie déclarée borne la reconstruction et conserve un état diagnostiquable
