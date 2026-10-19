# Références normatives — O18

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

Source : `openspec/specs/offline-first/spec.md`, ligne 28. SHA-256 du bloc : `8f62af57faa3572f5919d46b545a30853d17c837bc59dda33241bcb56ad771b8`.

~~~~text
### Requirement: Conflits, révocation et purge locale

Les stratégies de conflit sont explicites par ressource sans résolution silencieuse ; révocations, suppressions, marqueurs, expirations et changements de périmètre invalident ou purgent les données et intentions locales selon le cycle déclaré ; secrets, jetons et données restreintes MUST NOT être stockés localement.

#### Scenario: Révocation purgeant le local

- **WHEN** une révocation ou un changement de périmètre survient
- **THEN** les projections et files locales concernées sont invalidées ou purgées
~~~~

