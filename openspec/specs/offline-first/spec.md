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
