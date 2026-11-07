# Références normatives — Z01

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pzt | Processus PZT configurables sous propriétaire réseau unique | 2 | pzt-95b37c9ac7c5 |
| pzt | Base WireGuard et développement propre à Pixs | 1 | pzt-b9f254b10d8c |
| pzt | Module essentiel pixs.pzt et exécutable PZT indépendant | 1 | pzt-1063497b290f |
| pzt | Passage obligatoire PBO–PA par PZT | 1 | pzt-d043fc6da2c1 |
| pzt | Propriétaire des ressources réseau et filtrage | 1 | pzt-061212038e1c |
| zt-controller | CZT obligatoire et périmètre | 1 | zt-controller-0075d78b8361 |
| zt-controller | Base propre chiffrée et initialisation | 1 | zt-controller-99c13d6319c5 |
| zt-controller | Durabilité synchrone et promotion | 1 | zt-controller-a3a1fca8cc08 |
| zt-controller | Continuité bornée sans primaire | 1 | zt-controller-5f13908e4a13 |
| zt-controller | Gestionnaire réseau et propriétaire unique | 1 | zt-controller-a844ba947c3b |
| zt-controller | Backends et protection des échéances | 1 | zt-controller-0b71d7d52f1b |
| zt-controller | Amorçage et opérations multi-rôles | 1 | zt-controller-b3bc36187257 |

### Référence courante pzt-95b37c9ac7c5

Source : [pzt](../../specs/pzt/spec.md), ligne 40. SHA-256 : `95b37c9ac7c5419ffcc719061c7fa805843decda74c5cabb28efcb7c17caf8e5`.

Scénarios : Auxiliaires réseau supplémentaires; Propriétaires réseau concurrents.

~~~~text
### Requirement: Processus PZT configurables sous propriétaire réseau unique

Le binaire PZT MUST permettre un plan de processus et de concurrence selon runtime et les ressources de son environnement. Les rôles, auxiliaires, identités, canaux et limites MUST être déclarés et qualifiés. Le mode pzt-daemon MUST conserver un propriétaire admissible unique des ressources réseau par périmètre ; augmenter les processus MUST NOT créer des écrivains concurrents sur ce périmètre.

#### Scenario: Auxiliaires réseau supplémentaires

- **WHEN** un plan augmente des processus auxiliaires PZT
- **THEN** leurs fonctions restent déclarées sous contrôle du propriétaire réseau sans écriture concurrente des mêmes routes, interfaces ou règles

#### Scenario: Propriétaires réseau concurrents

- **WHEN** un plan demande deux propriétaires simultanément actifs du même périmètre réseau
- **THEN** son activation est refusée sauf séparation explicite de périmètres indépendants qualifiés
~~~~

### Référence courante pzt-b9f254b10d8c

Source : [pzt](../../specs/pzt/spec.md), ligne 68. SHA-256 : `b9f254b10d8cf4f1ddbc4e3ebf343e5033568a89ba3144925386c3a59ed072e7`.

Scénarios : Base WireGuard et développement propre à Pixs.

~~~~text
### Requirement: Base WireGuard et développement propre à Pixs

PZT MUST utiliser WireGuard comme base logicielle du transport IP authentifié/chiffré ; sa cryptographie MUST NOT être réimplémentée. Les capacités de référence NetBird MUST être redéveloppées dans Pixs sans intégration implicite de ses agents, serveurs, code, API ou formats. Backends natifs Linux/Windows MUST être privilégiés ; espace utilisateur seulement sous profil qualifié, sans contourner les permissions de conteneur.

#### Scenario: Base WireGuard et développement propre à Pixs

- **WHEN** un profil exige des permissions tunnel absentes
- **THEN** un backend utilisateur ne les contourne pas et le profil n'est pas activé
~~~~

### Référence courante pzt-1063497b290f

Source : [pzt](../../specs/pzt/spec.md), ligne 77. SHA-256 : `1063497b290fd7bb8e8abad2dad81ac19bb67f139b4c911c98be000279df7b7c`.

Scénarios : Réseau désactivé et gestion conservée.

~~~~text
### Requirement: Module essentiel pixs.pzt et exécutable PZT indépendant

Toute composition cible PBO MUST inclure le module officiel essentiel pixs.pzt,
au-dessus du Kernel et de pixs.core, par les mécanismes génériques. pixs.pzt
MUST configurer, administrer, visualiser, superviser et monitorer PZT. Le réseau
activé/configuré MUST être exécuté par le binaire indépendant PZT, compilé avec
Cython. Désactiver le réseau MUST NOT retirer pixs.pzt de PBO.

#### Scenario: Réseau désactivé et gestion conservée

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais pixs.pzt demeure composé avec ses fonctions de gestion
~~~~

### Référence courante pzt-d043fc6da2c1

Source : [pzt](../../specs/pzt/spec.md), ligne 90. SHA-256 : `d043fc6da2c1af6b20ea6e3d132cef7ef964e1df6b38e09fba4b82a2d52b1955`.

Scénarios : Passage obligatoire PBO–PA par PZT.

~~~~text
### Requirement: Passage obligatoire PBO–PA par PZT

Tous les échanges PBO–PA, instructions, configuration, administration, états, diagnostics, événements et résultats MUST passer par PZT dans les deux sens, même sur le même hôte ou conteneur. Le transport local mTLS MUST conserver identification, autorisation, chiffrement, validité, anti-rejeu et traçabilité ; WireGuard local n'est pas obligatoire. Un profil local indisponible MUST NOT déclencher un canal Unix, loopback ou fichier de substitution hors PZT.

#### Scenario: Passage obligatoire PBO–PA par PZT

- **WHEN** le transport local PZT n'est pas vérifiable
- **THEN** le contrôle PBO–PA concerné est bloqué sans repli de proximité
~~~~

### Référence courante pzt-061212038e1c

Source : [pzt](../../specs/pzt/spec.md), ligne 122. SHA-256 : `061212038e1c7769a435f768ee2ca67fd68ddce82cab591d771c490aecfcd46a`.

Scénarios : Propriétaire des ressources réseau et filtrage.

~~~~text
### Requirement: Propriétaire des ressources réseau et filtrage

Le binaire pzt-daemon MUST gérer les ressources PZT de son périmètre ; les autres modes MUST soumettre leurs demandes autorisées sans écritures réseau directes concurrentes. Les adapters nftables Linux et Windows Filtering Platform MUST appliquer les règles PZT sans écraser les ressources de l'opérateur hors mandat. AllowedIPs, route ou handshake MUST NOT remplacer un droit de protocole, port ou service.

#### Scenario: Propriétaire des ressources réseau et filtrage

- **WHEN** une route existe mais le service n'est pas autorisé
- **THEN** le filtrage bloque l'accès au service
~~~~

### Référence courante zt-controller-0075d78b8361

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 11. SHA-256 : `0075d78b83619c5def0567a914d7afbf54e7fb7afa52b4345dbe2a80e6bc8b80`.

Scénarios : Nouvelle configuration.

~~~~text
### Requirement: CZT obligatoire et périmètre

Chaque ZT MUST avoir au moins un CZT exécuté par PZT. CZT MUST gérer enrôlement technique, acteurs et organisation ZT, carte réseau, adressage des pairs, distribution des configurations et réconciliation ; PBO MUST conserver administration et supervision par contrats publics.

#### Scenario: Nouvelle configuration

- **WHEN** une politique réseau est administrée depuis PBO
- **THEN** sa référence est conservée par CZT sans écriture directe PBO dans les tables privées.
~~~~

### Référence courante zt-controller-99c13d6319c5

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 20. SHA-256 : `99c13d6319c59dbbc43992c47acd6cca1d2c2df7f27ece1b9ac68a44f840dc2a`.

Scénarios : Ajout de CZT.

~~~~text
### Requirement: Base propre chiffrée et initialisation

CZT MUST posséder une PG logique indépendante de PBO, des bases Instance/Domaine, DZT et PKIZT, chiffrée localement. Le premier CZT MUST l'initialiser ; chaque CZT supplémentaire MUST synchroniser sa réplique avec le primaire sans créer de source concurrente.

#### Scenario: Ajout de CZT

- **WHEN** un CZT est ajouté
- **THEN** sa base est synchronisée et vérifiée avant l’autorité correspondante.
~~~~

### Référence courante zt-controller-a3a1fca8cc08

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 29. SHA-256 : `a3a1fca8cc08c66028525454eb093f5df69735c8571174ce4b9eac4bbd594e0b`.

Scénarios : Réplique requise absente.

~~~~text
### Requirement: Durabilité synchrone et promotion

CZT MUST confirmer l'écriture après persistance sur le primaire et les répliques synchrones requises. Le minimum MUST être configurable sans diminution automatique en cas de panne. La bascule automatique MUST être encadrée, exclure l'ancien primaire, vérifier le candidat et conserver les écritures confirmées.

#### Scenario: Réplique requise absente

- **WHEN** le nombre de confirmations est inférieur au minimum configuré
- **THEN** l’écriture n’est pas confirmée par une réduction automatique du minimum.
~~~~

### Référence courante zt-controller-5f13908e4a13

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 38. SHA-256 : `5f13908e4a13140cc9c13d07a3e2ba28739ea6998ceb41162998bbdce41205a6`.

Scénarios : Échéance pendant panne.

~~~~text
### Requirement: Continuité bornée sans primaire

Sans CZT primaire opérationnel, les échanges MUST rester limités aux autorisations encore valides et aux révocations connues. Les opérations requérant CZT MUST être suspendues ; un cache MUST NOT émettre ou prolonger de nouveaux droits.

#### Scenario: Échéance pendant panne

- **WHEN** une autorisation expire sans primaire disponible
- **THEN** l’accès cesse sans grâce ni renouvellement local.
~~~~

### Référence courante zt-controller-a844ba947c3b

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 47. SHA-256 : `a844ba947c3b675f86146904664b15a71a511bff9a7bba354ee3e5e7446cde46`.

Scénarios : Deux rôles demandent des règles.

~~~~text
### Requirement: Gestionnaire réseau et propriétaire unique

Le socle PZT MUST coordonner interfaces, adressage, routage et pare-feu selon les références CZT, en agrégeant les besoins des rôles sous un propriétaire d'écriture par périmètre. Le profil MUST gérer le périmètre PZT par défaut et MAY gérer globalement l'hôte sur choix explicite.

#### Scenario: Deux rôles demandent des règles

- **WHEN** GZT et DZT demandent des règles sur un même périmètre
- **THEN** le gestionnaire commun les réconcilie sans écrivains concurrents ni écrasement hors mandat.
~~~~

### Référence courante zt-controller-0b71d7d52f1b

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 56. SHA-256 : `0b71d7d52f1b610117e914b3e44b53e11b9824b9ef3da9565f6c8e188849e39d`.

Scénarios : Dérive sans correction autorisée.

~~~~text
### Requirement: Backends et protection des échéances

Les profils MUST qualifier Linux nftables et les capacités demandées iptables/ip6tables/ipset, ainsi que le pare-feu Windows/WFP, sans interchangeabilité présumée. La protection indépendante des autorisations MUST être obligatoire. Configuration déclarative/versionnée/reconstruisible et dérives détectées MUST être distinguées de la correction automatique configurable et désactivée par défaut.

#### Scenario: Dérive sans correction autorisée

- **WHEN** un écart au pare-feu est observé sans politique de réparation
- **THEN** le constat et la mise en sécurité prévue sont rapportés sans correction non autorisée.
~~~~

### Référence courante zt-controller-b3bc36187257

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 65. SHA-256 : `b3bc3618725797ff4d27c7f5f2d60dd14f808c15d04e1aa0b17a068cc4b6cfd8`.

Scénarios : Réponse perdue.

~~~~text
### Requirement: Amorçage et opérations multi-rôles

L'amorçage technique MUST être limité et borné, distinct du contrôle normal. Une opération multi-rôles MUST posséder un propriétaire unique, un suivi durable et une reprise sans double effet, avec revalidation des mandats et préconditions.

#### Scenario: Réponse perdue

- **WHEN** une étape multi-rôles a pu produire son effet sans réponse
- **THEN** la reprise réconcilie les propriétaires avant répétition.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 12 | [Base WireGuard et développement propre à Pixs](../../specs/pzt/spec.md#L12) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 21 | [Module essentiel PBO et binaire PZT dédié](../../specs/pzt/spec.md#L21) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 30 | [Passage obligatoire PBO–PA par PZT](../../specs/pzt/spec.md#L30) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 57 | [Propriétaire des ressources réseau et filtrage](../../specs/pzt/spec.md#L57) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--4e34d93767

Source : `openspec/specs/pzt/spec.md`, ligne 12. SHA-256 du bloc : `2f384a124f376373fc5eaa0b7bd4a09f3bb967429bb65bb9f21bad657c30731c`.

~~~~text
### Requirement: Base WireGuard et développement propre à Pixs

PZT MUST utiliser WireGuard comme base logicielle du transport IP authentifié/chiffré ; sa cryptographie MUST NOT être réimplémentée. Les capacités de référence NetBird MUST être redéveloppées dans Pixs sans intégration implicite de ses agents, serveurs, code, API ou formats. Backends natifs Linux/Windows MUST être privilégiés ; espace utilisateur seulement sous profil qualifié, sans contourner les permissions de conteneur.

#### Scenario: Base WireGuard et développement propre à Pixs

- **WHEN** un profil exige des permissions tunnel absentes
- **THEN** un backend utilisateur ne les contourne pas et le profil n'est pas activé
~~~~

### Référence pzt--73016f3d2e

Source : `openspec/specs/pzt/spec.md`, ligne 21. SHA-256 du bloc : `050ae5dc06f898c93bf7624d680e4352ef1525bffe2dbb46b7c66870d5c021d5`.

~~~~text
### Requirement: Module essentiel PBO et binaire PZT dédié

Toute composition cible PBO MUST inclure le module officiel essentiel PZT, au-dessus du Kernel et de pixs.core, par les mécanismes génériques de modules. Le réseau activé/configuré MUST toujours être exécuté par le binaire PZT de PA compilé avec Cython ; PBO MUST assurer configuration, visualisation, supervision et monitoring. Désactiver le réseau MUST NOT retirer le module essentiel de PBO.

#### Scenario: Module essentiel PBO et binaire PZT dédié

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais le module PBO de gestion reste composé
~~~~

### Référence pzt--b09abd6f60

Source : `openspec/specs/pzt/spec.md`, ligne 30. SHA-256 du bloc : `efd3979f85e17ba446c232d0fd897c0c83be33aca423a3668342e3a8a822481d`.

~~~~text
### Requirement: Passage obligatoire PBO–PA par PZT

Tous les échanges PBO–PA, instructions, configuration, administration, états, diagnostics, événements et résultats MUST passer par PZT dans les deux sens, même sur le même hôte ou conteneur. Le transport local mTLS MUST conserver identification, autorisation, chiffrement, validité, anti-rejeu et traçabilité ; WireGuard local n'est pas obligatoire. Un profil local indisponible MUST NOT déclencher un canal Unix, loopback ou fichier de substitution hors PZT.

#### Scenario: Passage obligatoire PBO–PA par PZT

- **WHEN** le transport local PZT n'est pas vérifiable
- **THEN** le contrôle PBO–PA concerné est bloqué sans repli de proximité
~~~~

### Référence pzt--4e6e13b55e

Source : `openspec/specs/pzt/spec.md`, ligne 57. SHA-256 du bloc : `3292d6466d8349594c139ebc1aabded35fc05c48e2561af056448fa42e3e6c70`.

~~~~text
### Requirement: Propriétaire des ressources réseau et filtrage

Le binaire pzt-daemon MUST gérer les ressources PZT de son périmètre ; les autres modes MUST soumettre leurs demandes autorisées sans écritures réseau directes concurrentes. Les adapters nftables Linux et Windows Filtering Platform MUST appliquer les règles PZT sans écraser les ressources de l'opérateur hors mandat. AllowedIPs, route ou handshake MUST NOT remplacer un droit de protocole, port ou service.

#### Scenario: Propriétaire des ressources réseau et filtrage

- **WHEN** une route existe mais le service n'est pas autorisé
- **THEN** le filtrage bloque l'accès au service
~~~~

