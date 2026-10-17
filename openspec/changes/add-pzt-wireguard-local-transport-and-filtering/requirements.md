# Références normatives — Z01

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

