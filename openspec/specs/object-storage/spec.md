# object-storage Specification

## Purpose
Le stockage objet conserve les octets via des fournisseurs interchangeables, tandis que Pixs garde l'autorité sur métadonnées, permissions et cycle de vie.

## Requirements

### Requirement: Contrat fournisseur objet et métadonnées Pixs

Le système MUST respecter les garanties suivantes.

Le contenu binaire est confié à un ObjectStorageProvider compatible ; identité, tenant, permissions, audit et cycle de vie restent gérés par Pixs via la métadonnée, indépendamment de la durée technique des octets.

#### Scenario: Suppression propagée au fournisseur

- **WHEN** une métadonnée est supprimée ou purgée
- **THEN** un marqueur et une décision d'effacement sont propagés au fournisseur sans exposer l'autorité métier

### Requirement: Isolation tenant et périmètre

Chaque objet MUST porter le tenant racine et le scope applicable ; aucun partage direct avec un espace exclusif tiers ; toute suppression respecte rétention, holds et révocation.

#### Scenario: Accès inter-tenant refusé

- **WHEN** une identité demande un objet hors de son périmètre autorisé
- **THEN** l'accès est refusé avec un audit, sans fuite d'existence

### Requirement: Conformité des adaptateurs

Chaque adaptateur MUST déclarer transport, chiffrement, localisation, rétention, suppression, restitution et révocation ; les clés et identifiants restent fournis par référence externe.

#### Scenario: Adaptateur non conforme bloqué

- **WHEN** un adaptateur ne démontre pas la suppression ou la révocation déclarée
- **THEN** sa composition est refusée

### Requirement: Runtime Bulk v1 B04 — Staging privé et intégrité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B04 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Objet vérifié

- **WHEN** un objet privé immuable satisfait les contrôles de taille, type, classification et SHA-256
- **THEN** son contenu peut être traité sous sa version stable et les limites déclarées

#### Scenario: Intégrité rompue

- **WHEN** le checksum ou la version observée diffère du contenu attendu
- **THEN** le traitement est refusé avant tout appel propriétaire, sans copie de secours locale

#### Scenario: Lecture actuelle sous autorité et gouvernance

- **WHEN** un check EXECUTE actuel ALLOW puis une gouvernance RESOLVED actuelle sur le contrat ObjectMetadataV1 attendu sont résolus via ports composés avant lecture
- **THEN** la lecture stat_private puis iter_bytes peut alimenter le vérificateur sous PolicyV1, deadline et annulation serveur, sans contenu conservé ni remis avant intégrité positive

#### Scenario: Contrôle actuel refusé

- **WHEN** l'autorité est DENY ou UNAVAILABLE, ou la gouvernance est DENY, UNAVAILABLE ou à contexte divergent
- **THEN** aucune lecture n'est invoquée et aucun contexte exploitable n'est fourni

#### Scenario: Qualification ou version insuffisante

- **WHEN** la liaison qualifiée résolue est absente ou la version observée diverge de la version attendue
- **THEN** l'opération est refusée sans traitement ni copie locale, même à stats apparentes identiques

## Annexes normatives — RSMP-BULK-EXECUTION-V1

Les clauses et schémas ci-dessous sont normatifs par les exigences Runtime Bulk v1 qui les référencent. Le schéma logique ne constitue ni une implémentation ni un nouveau wire format public.

### B04 — Staging privé et intégrité

- Le staging MUST utiliser un objet privé immuable et versionné d’un ObjectStorageProvider déclaré ; lecture et écriture MUST être bornées par politique, délai et cancellation.
- Le worker MUST vérifier appartenance, classification, type, taille et SHA-256 réel du flux complet avant toute validation ou mutation propriétaire ; un écart MUST refuser l’opération.
- L’identité de version du contenu MUST rester stable entre vérification et traitement ; un provider incapable de cette garantie MUST être refusé, sans copie de secours locale.
- Un objet écrit mais non référencé par une transaction validée MUST rester privé et non publiable ; son effacement MUST suivre la politique de gouvernance et de rétention.

### Schéma logique ObjectMetadataV1

```json
[
  [
    "object_reference",
    "str opaque",
    "obligatoire"
  ],
  [
    "version_reference",
    "str opaque",
    "immuable"
  ],
  [
    "tenant_reference",
    "str opaque",
    "obligatoire pour ce runtime Bulk tenant"
  ],
  [
    "scope_reference",
    "str opaque | None",
    "contexte serveur explicite"
  ],
  [
    "classification_reference",
    "str opaque",
    "gouvernance résolue"
  ],
  [
    "size_bytes",
    "int exact >=0",
    "borne PolicyV1"
  ],
  [
    "sha256",
    "hex minuscule 64 caractères",
    "recalculé sur octets"
  ],
  [
    "media_type",
    "text/csv | application/x-ndjson",
    "format déclaré"
  ],
  [
    "is_private",
    "bool exact",
    "True obligatoire"
  ],
  [
    "expires_at",
    "datetime exact timezone.utc",
    "politique résolue"
  ],
  [
    "retention_policy_reference",
    "str opaque",
    "holds et révocation sous autorité Pixs"
  ]
]
```
