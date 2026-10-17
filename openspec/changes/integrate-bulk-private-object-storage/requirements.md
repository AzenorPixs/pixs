# Références normatives — B05

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 17 | [Import via staging privé et commandes propriétaires](../../specs/bulk-operations/spec.md#L17) | P | COMPLETER_OU_INTEGRER |
| object-storage / 37 | [Runtime Bulk v1 B04 — Staging privé et intégrité](../../specs/object-storage/spec.md#L37) | P | CANDIDAT_SI_SELECTION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence bulk-operations--f487525180

Source : `openspec/specs/bulk-operations/spec.md`, ligne 17. SHA-256 du bloc : `3b525720d607aa23dfd92c9cb0660cdd64fbc55f3de3d1177547782844745894`.

~~~~text
### Requirement: Import via staging privé et commandes propriétaires

Tout import MUST passer par un espace privé, vérifier taille, type, somme de contrôle et mapping versionné, puis appeler exclusivement les commandes du module propriétaire avec modes VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT explicites ; les conflits sont rejetés par défaut.

#### Scenario: Ligne en conflit rejetée

- **WHEN** une ligne contredit la stratégie de conflit déclarée
- **THEN** elle est rejetée dans un rapport versionné sans mutation partielle silencieuse
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

