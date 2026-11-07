# zt-controller Specification

## Purpose

Controller ZT — CZT — conserve la référence de coordination réseau, des acteurs et des politiques ZT dans une PG indépendante.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45 et TECHNICAL.md §46), sans implémentation ni qualification déduite.

## Requirements

### Requirement: CZT obligatoire et périmètre

Chaque ZT MUST avoir au moins un CZT exécuté par PZT. CZT MUST gérer enrôlement technique, acteurs et organisation ZT, carte réseau, adressage des pairs, distribution des configurations et réconciliation ; PBO MUST conserver administration et supervision par contrats publics.

#### Scenario: Nouvelle configuration

- **WHEN** une politique réseau est administrée depuis PBO
- **THEN** sa référence est conservée par CZT sans écriture directe PBO dans les tables privées.

### Requirement: Base propre chiffrée et initialisation

CZT MUST posséder une PG logique indépendante de PBO, des bases Instance/Domaine, DZT et PKIZT, chiffrée localement. Le premier CZT MUST l'initialiser ; chaque CZT supplémentaire MUST synchroniser sa réplique avec le primaire sans créer de source concurrente.

#### Scenario: Ajout de CZT

- **WHEN** un CZT est ajouté
- **THEN** sa base est synchronisée et vérifiée avant l’autorité correspondante.

### Requirement: Durabilité synchrone et promotion

CZT MUST confirmer l'écriture après persistance sur le primaire et les répliques synchrones requises. Le minimum MUST être configurable sans diminution automatique en cas de panne. La bascule automatique MUST être encadrée, exclure l'ancien primaire, vérifier le candidat et conserver les écritures confirmées.

#### Scenario: Réplique requise absente

- **WHEN** le nombre de confirmations est inférieur au minimum configuré
- **THEN** l’écriture n’est pas confirmée par une réduction automatique du minimum.

### Requirement: Continuité bornée sans primaire

Sans CZT primaire opérationnel, les échanges MUST rester limités aux autorisations encore valides et aux révocations connues. Les opérations requérant CZT MUST être suspendues ; un cache MUST NOT émettre ou prolonger de nouveaux droits.

#### Scenario: Échéance pendant panne

- **WHEN** une autorisation expire sans primaire disponible
- **THEN** l’accès cesse sans grâce ni renouvellement local.

### Requirement: Gestionnaire réseau et propriétaire unique

Le socle PZT MUST coordonner interfaces, adressage, routage et pare-feu selon les références CZT, en agrégeant les besoins des rôles sous un propriétaire d'écriture par périmètre. Le profil MUST gérer le périmètre PZT par défaut et MAY gérer globalement l'hôte sur choix explicite.

#### Scenario: Deux rôles demandent des règles

- **WHEN** GZT et DZT demandent des règles sur un même périmètre
- **THEN** le gestionnaire commun les réconcilie sans écrivains concurrents ni écrasement hors mandat.

### Requirement: Backends et protection des échéances

Les profils MUST qualifier Linux nftables et les capacités demandées iptables/ip6tables/ipset, ainsi que le pare-feu Windows/WFP, sans interchangeabilité présumée. La protection indépendante des autorisations MUST être obligatoire. Configuration déclarative/versionnée/reconstruisible et dérives détectées MUST être distinguées de la correction automatique configurable et désactivée par défaut.

#### Scenario: Dérive sans correction autorisée

- **WHEN** un écart au pare-feu est observé sans politique de réparation
- **THEN** le constat et la mise en sécurité prévue sont rapportés sans correction non autorisée.

### Requirement: Amorçage et opérations multi-rôles

L'amorçage technique MUST être limité et borné, distinct du contrôle normal. Une opération multi-rôles MUST posséder un propriétaire unique, un suivi durable et une reprise sans double effet, avec revalidation des mandats et préconditions.

#### Scenario: Réponse perdue

- **WHEN** une étape multi-rôles a pu produire son effet sans réponse
- **THEN** la reprise réconcilie les propriétaires avant répétition.
