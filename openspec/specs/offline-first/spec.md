# offline-first Specification

## Purpose
La capacité hors ligne, opt-in et déclarée par ressource, conserve des projections locales versionnées et des intentions non confirmées, sans autorité locale ni contournement serveur.

## Requirements

### Requirement: Éligibilité déclarée et projections non autoritatives

Seules les ressources et commandes explicitement déclarées sont utilisables hors ligne ; toute projection locale reste non autoritative, versionnée avec points de reprise, et MUST NOT autoriser ni confirmer un effet métier.

#### Scenario: Ressource non éligible indisponible

- **WHEN** une ressource non déclarée est demandée hors ligne
- **THEN** elle reste indisponible avec un état explicite au lieu d'une réplication implicite

### Requirement: Intentions provisoires réévaluées au serveur

Le système MUST respecter les garanties suivantes.

Toute commande créée hors ligne reste provisoire avec identifiant d'idempotence ; à la reconnexion, identité, périmètre, autorisation, droits, quotas, concurrence et gouvernance sont réévalués côté serveur avant confirmation.

#### Scenario: Commande hors ligne rejetée au serveur

- **WHEN** une intention locale contredit l'autorisation ou la concurrence courante
- **THEN** elle est rejetée avec un conflit explicite et aucun double effet confirmé

### Requirement: Conflits, révocation et purge locale

Les stratégies de conflit sont explicites par ressource sans résolution silencieuse ; révocations, suppressions, marqueurs, expirations et changements de périmètre invalident ou purgent les données et intentions locales selon le cycle déclaré ; secrets, jetons et données restreintes MUST NOT être stockés localement.

#### Scenario: Révocation purgeant le local

- **WHEN** une révocation ou un changement de périmètre survient
- **THEN** les projections et files locales concernées sont invalidées ou purgées
