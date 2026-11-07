# Références normatives — O18

Réconciliation documentaire du 1er novembre 2026 — GSCM3 : les seules copies divergentes et leurs références sont actualisées depuis le canon courant. Aucun delta normatif, tâche, case ou preuve de réalisation n’est modifié.

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| offline-first / 8 | [Éligibilité déclarée et projections non autoritatives](../../specs/offline-first/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| offline-first / 17 | [Intentions provisoires réévaluées au serveur](../../specs/offline-first/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| offline-first / 28 | [Conflits, révocation et purge locale](../../specs/offline-first/spec.md#L28) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence offline-first--085e23ad80

Source : `openspec/specs/offline-first/spec.md`, ligne 8. SHA-256 du bloc : `d18ddd96b4f83ba4a2f56a4564a83d88373006ca2d2129b1ea99651284806470`.

~~~~text
### Requirement: Éligibilité déclarée et projections non autoritatives

Seules les ressources et commandes explicitement déclarées sont utilisables hors ligne ; toute projection locale reste non autoritative, versionnée avec points de reprise, et MUST NOT autoriser ni confirmer un effet métier.

#### Scenario: Ressource non éligible indisponible

- **WHEN** une ressource non déclarée est demandée hors ligne
- **THEN** elle reste indisponible avec un état explicite au lieu d'une réplication implicite
~~~~

### Référence offline-first--0fe04ca3cc

Source : `openspec/specs/offline-first/spec.md`, ligne 17. SHA-256 du bloc : `2e6af7983f274a3319f9d4956d91035a0a769fdf8f5d7918954321928072827e`.

~~~~text
### Requirement: Intentions provisoires réévaluées au serveur

Le système MUST respecter les garanties suivantes.

Toute commande créée hors ligne reste provisoire avec identifiant d'idempotence ; à la reconnexion, identité, périmètre, autorisation, droits, quotas, concurrence et gouvernance sont réévalués côté serveur avant confirmation.

#### Scenario: Commande hors ligne rejetée au serveur

- **WHEN** une intention locale contredit l'autorisation ou la concurrence courante
- **THEN** elle est rejetée avec un conflit explicite et aucun double effet confirmé
~~~~

### Référence offline-first--c958b582ba

Source : `openspec/specs/offline-first/spec.md`, ligne 28. SHA-256 du bloc : `ef180bc6108d0fdae456f3bd48a28f3aa4b12e1ce6027ee96f0af82fa3f42cbd`.

~~~~text
### Requirement: Conflits, révocation et purge locale

Les conflits MUST suivre une stratégie explicite par ressource, sans résolution silencieuse. Révocations, suppressions, marqueurs, expirations et changements de périmètre MUST invalider ou purger données et intentions locales selon leur cycle déclaré. Les données restreintes MUST NOT être stockées localement. Secrets et jetons MUST NOT être conservés hors du coffre natif sécurisé séparé défini par native-clients, ni copiés dans les projections, caches ou files hors ligne.

#### Scenario: Révocation purgeant le local

- **WHEN** une révocation ou un changement de périmètre survient
- **THEN** les projections et files locales concernées sont invalidées ou purgées

#### Scenario: Coffre natif séparé de la réplique

- **WHEN** un profil natif hors ligne utilise un credential conservé dans le mécanisme sécurisé déclaré par la plateforme
- **THEN** ce credential ne figure dans aucune projection, cache, file d’intentions ou export de données hors ligne
- **AND** sa présence dans le coffre ne confirme aucune mutation et ne prolonge aucun droit révoqué


#### Scenario: Donnée restreinte hors réplique refusée

- **WHEN** un client propose de conserver une donnée restreinte dans un fichier local extérieur aux projections, caches et files
- **THEN** ce stockage est refusé ; l’exception du coffre natif ne s’applique pas aux données restreintes
~~~~

