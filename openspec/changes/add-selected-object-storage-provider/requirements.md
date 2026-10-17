# Références normatives — O01

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| object-storage / 8 | [Contrat fournisseur objet et métadonnées Pixs](../../specs/object-storage/spec.md#L8) | P | CANDIDAT_SI_SELECTION |
| object-storage / 19 | [Isolation tenant et périmètre](../../specs/object-storage/spec.md#L19) | P | CANDIDAT_SI_SELECTION |
| object-storage / 28 | [Conformité des adaptateurs](../../specs/object-storage/spec.md#L28) | P | CANDIDAT_SI_SELECTION |
| object-storage / 37 | [Runtime Bulk v1 B04 — Staging privé et intégrité](../../specs/object-storage/spec.md#L37) | P | CANDIDAT_SI_SELECTION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence object-storage--5d009db875

Source : `openspec/specs/object-storage/spec.md`, ligne 8. SHA-256 du bloc : `46152e4fbe091d4389a3baf696e3cdcf13c39d42c4c8d36ca66504503fef4bd9`.

~~~~text
### Requirement: Contrat fournisseur objet et métadonnées Pixs

Le système MUST respecter les garanties suivantes.

Le contenu binaire est confié à un ObjectStorageProvider compatible ; identité, tenant, permissions, audit et cycle de vie restent gérés par Pixs via la métadonnée, indépendamment de la durée technique des octets.

#### Scenario: Suppression propagée au fournisseur

- **WHEN** une métadonnée est supprimée ou purgée
- **THEN** un marqueur et une décision d'effacement sont propagés au fournisseur sans exposer l'autorité métier
~~~~

### Référence object-storage--04c1210b71

Source : `openspec/specs/object-storage/spec.md`, ligne 19. SHA-256 du bloc : `15355080ecef95511dc8f16b9821f334bd4bb2edfa44a03e468a15501b532507`.

~~~~text
### Requirement: Isolation tenant et périmètre

Chaque objet MUST porter le tenant racine et le scope applicable ; aucun partage direct avec un espace exclusif tiers ; toute suppression respecte rétention, holds et révocation.

#### Scenario: Accès inter-tenant refusé

- **WHEN** une identité demande un objet hors de son périmètre autorisé
- **THEN** l'accès est refusé avec un audit, sans fuite d'existence
~~~~

### Référence object-storage--c6f2e67334

Source : `openspec/specs/object-storage/spec.md`, ligne 28. SHA-256 du bloc : `569617d086c4c1454acbe88cc39da6b10f1af133a1504f2527c8bbde44d90eda`.

~~~~text
### Requirement: Conformité des adaptateurs

Chaque adaptateur MUST déclarer transport, chiffrement, localisation, rétention, suppression, restitution et révocation ; les clés et identifiants restent fournis par référence externe.

#### Scenario: Adaptateur non conforme bloqué

- **WHEN** un adaptateur ne démontre pas la suppression ou la révocation déclarée
- **THEN** sa composition est refusée
~~~~

### Référence object-storage--5e22f844d0

Source : `openspec/specs/object-storage/spec.md`, ligne 37. SHA-256 du bloc : `a13cceb66d33c513321c668d1aa3f06fbfb8b9a65400943a0e3d649905fa2f8e`.

~~~~text
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
~~~~

