# Références normatives — O04

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| distributed-cache / 10 | [Cache uniquement dérivé et reconstruisible](../../specs/distributed-cache/spec.md#L10) | NE | AUDIT_AVANT_CREATION |
| distributed-cache / 22 | [Partitionnement et autorisation conservés](../../specs/distributed-cache/spec.md#L22) | NE | AUDIT_AVANT_CREATION |
| distributed-cache / 33 | [Invalidation déterministe et traçable](../../specs/distributed-cache/spec.md#L33) | NE | AUDIT_AVANT_CREATION |
| distributed-cache / 45 | [Dégradation et protection contre l'avalanche](../../specs/distributed-cache/spec.md#L45) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence distributed-cache--55c9d28225

Source : `openspec/specs/distributed-cache/spec.md`, ligne 10. SHA-256 du bloc : `c7bb3a45b41316a9afb8943a47dacd5073006ba33a7a065ac678b53200bfc26a`.

~~~~text
### Requirement: Cache uniquement dérivé et reconstruisible

Une entrée de cache MUST être dérivée d'une source autoritative ou d'une
projection reconstruisible. Un CacheProvider MUST NOT devenir la source de
vérité d'une mutation, d'une autorisation, d'une idempotence ou d'un état de
Job persistant.

#### Scenario: Perte complète du cache

- **WHEN** toutes les entrées d'un cache sont indisponibles ou supprimées
- **THEN** le système reconstruit les lectures depuis leurs sources autoritatives selon le mode déclaré
~~~~

### Référence distributed-cache--824e3dbdfd

Source : `openspec/specs/distributed-cache/spec.md`, ligne 22. SHA-256 du bloc : `af9c20e3eda2c0bedb43c4d99dcd7f9fa4306ec18424209d1682453174d5eabd`.

~~~~text
### Requirement: Partitionnement et autorisation conservés

Les clés, tags et partitions MUST intégrer tenant, scope, identité, version et
classification lorsque ces dimensions sont applicables. Une lecture depuis le
cache MUST réappliquer les contrôles d'autorisation nécessaires.

#### Scenario: Changement de tenant

- **WHEN** une identité change de tenant ou de scope
- **THEN** elle ne peut pas réutiliser une entrée du périmètre précédent
~~~~

### Référence distributed-cache--8afbf32f03

Source : `openspec/specs/distributed-cache/spec.md`, ligne 33. SHA-256 du bloc : `b02b0faf20248b2186b60f7f0a7a42f4fc00874c8e6025d9db9710fec1326fcc`.

~~~~text
### Requirement: Invalidation déterministe et traçable

Les mutations, révocations, tombstones et changements de politique MUST
invalider ou rendre non lisibles les entrées dérivées concernées. Une
invalidation échouée MUST être diagnostiquée et ne doit pas prolonger une
décision positive au-delà de sa politique de fraîcheur.

#### Scenario: Permission révoquée

- **WHEN** une permission donnant accès à une ressource est retirée
- **THEN** les entrées associées ne servent plus cette ressource à l'identité concernée
~~~~

### Référence distributed-cache--52bb617f31

Source : `openspec/specs/distributed-cache/spec.md`, ligne 45. SHA-256 du bloc : `f7f90923032d3692974c02e3a798ab1b0c007ba94bea0d7cf997c3505bb6f222`.

~~~~text
### Requirement: Dégradation et protection contre l'avalanche

Le CacheProvider MUST déclarer ses TTL, limites, stratégie anti-stampede et
mode de dégradation. Une indisponibilité de cache MUST NOT produire une donnée
hors périmètre ni masquer l'échec d'une source autoritative obligatoire.

#### Scenario: Expiration concurrente

- **WHEN** de nombreuses lectures atteignent une entrée expirée simultanément
- **THEN** la stratégie déclarée borne la reconstruction et conserve un état diagnostiquable
~~~~

