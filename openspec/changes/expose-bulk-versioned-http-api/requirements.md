# Références normatives — B09

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 8 | [Contrat BulkOperation suivi par operation_id](../../specs/bulk-operations/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 507 | [Runtime Bulk v1 B01 — Périmètre exécutable](../../specs/bulk-operations/spec.md#L507) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 521 | [Runtime Bulk v1 B02 — Enveloppe et progression](../../specs/bulk-operations/spec.md#L521) | P | COMPLETER_OU_INTEGRER |
| interactions / 45 | [Runtime Bulk v1 B10 — Idempotence durable](../../specs/interactions/spec.md#L45) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence bulk-operations--cd148551a7

Source : `openspec/specs/bulk-operations/spec.md`, ligne 8. SHA-256 du bloc : `267706d53cd36c5b0be4e86398fa92a7a4bdc9ada929dae2ff7d11be3d1236d7`.

~~~~text
### Requirement: Contrat BulkOperation suivi par operation_id

Chaque opération MUST suivre un contrat versionné avec variantes IMPORT et EXPORT, états, rattachement à operation_id, travaux persistants, tenant et scope ; les formats de référence sont CSV et NDJSON, tout autre format via adaptateur déclaré.

#### Scenario: Suivi distinct des travaux

- **WHEN** une opération longue dépasse le seuil synchrone
- **THEN** elle retourne un operation_id suivi, distinct des identifiants des travaux qui l'exécutent
~~~~

### Référence bulk-operations--8cf58a6b8a

Source : `openspec/specs/bulk-operations/spec.md`, ligne 507. SHA-256 du bloc : `0ef12558bbd593c6201682ef8973600a07ed3ba56c21754b11d94367a9dc5063`.

~~~~text
### Requirement: Runtime Bulk v1 B01 — Périmètre exécutable

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B01 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Admission avant suivi

- **WHEN** une demande IMPORT CSV conforme est admise
- **THEN** l’opération, la demande, le premier Job et la liaison sont engagés avant le retour de operation_id

#### Scenario: Format non pris en charge

- **WHEN** le runtime v1 reçoit un format autre que CSV ou NDJSON
- **THEN** il refuse cette capacité sans fallback ni retrait de l’extensibilité générale
~~~~

### Référence bulk-operations--6ac2657694

Source : `openspec/specs/bulk-operations/spec.md`, ligne 521. SHA-256 du bloc : `900129b9cd2578cb565d06d67c1b8f50182d5bac32e95fff5a3d8d0680704206`.

~~~~text
### Requirement: Runtime Bulk v1 B02 — Enveloppe et progression

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B02 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Données explicites

- **WHEN** le producteur serveur fournit toutes les valeurs conformes et leurs None explicites
- **THEN** les valeurs et la révision sont conservées sans coercition ni défaut de modèle

#### Scenario: Valeur étrangère

- **WHEN** un champ est omis, inconnu ou possède un type étranger
- **THEN** la validation refuse avant comportement, parsing ou I/O et sans écho de valeur
~~~~

### Référence interactions--fd05450f99

Source : `openspec/specs/interactions/spec.md`, ligne 45. SHA-256 du bloc : `cb85f020ba302efd40138837a82ee096f55c9851befcb5bab477a3227f8bc36a`.

~~~~text
### Requirement: Runtime Bulk v1 B10 — Idempotence durable

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B10 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Rejeu identique

- **WHEN** la même clé d’admission est présentée avec le même contenu initial
- **THEN** l’opération initiale est rendue après contrôle actuel sans second effet

#### Scenario: Rejeu divergent

- **WHEN** la même clé est présentée avec un fingerprint différent
- **THEN** un conflit explicite est persisté ou retourné sans mutation propriétaire

## Annexes normatives — RSMP-BULK-EXECUTION-V1

Les clauses et schémas ci-dessous sont normatifs par les exigences Runtime Bulk v1 qui les référencent. Le schéma logique ne constitue ni une implémentation ni un nouveau wire format public.

### B10 — Idempotence durable

- L’admission MUST dédupliquer durablement par tenant résolu, acteur résolu, bulk_type et idempotency_key ; contenu identique MUST rendre l’opération initiale et divergence MUST produire un conflit.
- Le fingerprint MUST être SHA-256 du JSON UTF-8 strict trié, compact et sans nombres flottants de l’annexe FingerprintV1 ; operation_id, état, progression et sorties MUST en être exclus.
- Le contenu initial et son fingerprint MUST être immuables après admission ; une reprise MUST NOT recalculer l’identité depuis des champs de suivi modifiés.
- La déduplication des Commands MUST préserver la clé canonique tenant_id, subject_id, command_type, idempotency_key ; les octets canoniques MUST provenir du sérialiseur public versionné du propriétaire.
- Mutation propriétaire, résultat d’idempotence, progression et checkpoint de l’unité MUST être engagés dans la même transaction PostgreSQL.
- La rétention d’idempotence MUST couvrir la fenêtre de rejeu après état terminal et les holds ; une entrée encore requise MUST NOT être purgée.
- Une entrée CommandIdempotencyV1 IN_PROGRESS MUST rester dans la transaction d’exécution ; seul SUCCEEDED ou REJECTED MUST être engagé. Une exception technique MUST annuler cette transaction et ses effets.

### Schéma logique FingerprintV1

```json
{
  "fields": [
    "execution_version",
    "bulk_type",
    "bulk_version",
    "tenant_context_reference",
    "scope_context_reference",
    "format",
    "conflict_strategy",
    "commit_mode",
    "requested_by_reference",
    "mapping_reference",
    "mapping_version",
    "input_reference",
    "input_version",
    "input_sha256",
    "input_size_bytes",
    "projection_reference",
    "consistency_kind",
    "consistency_reference",
    "idempotency_key",
    "policy_reference",
    "policy_version",
    "expires_at"
  ],
  "encoding": "dict fermé trié lexicographiquement par clés ; JSON compact séparateurs virgule/deux-points, ensure_ascii=False, UTF-8 strict ; datetime UTC ISO8601 à six décimales et suffixe Z ; None JSON null ; pas de float ; SHA-256 hex minuscule",
  "snapshot": "valeurs initiales immuables d’admission ; la référence de consistance ultérieure ne modifie pas le fingerprint initial",
  "excluded": [
    "operation_id",
    "status",
    "progress",
    "revision",
    "cancellation_requested",
    "output_reference",
    "output_version",
    "output_sha256",
    "output_size_bytes",
    "checkpoint_reference",
    "result_reference",
    "correlation_id",
    "causation_id"
  ]
}
```

### Schéma logique CommandIdempotencyV1

```json
[
  [
    "tenant_id",
    "str exacte résolue",
    "partie de clé"
  ],
  [
    "subject_id",
    "str exacte résolue",
    "partie de clé"
  ],
  [
    "command_type",
    "str déclarée",
    "partie de clé"
  ],
  [
    "idempotency_key",
    "str opaque",
    "partie de clé"
  ],
  [
    "content_sha256",
    "hex minuscule 64 caractères",
    "octets canoniques propriétaire versionnés"
  ],
  [
    "serializer_version",
    "str SemVer",
    "figée pour l’entrée"
  ],
  [
    "state",
    "IN_PROGRESS | SUCCEEDED | REJECTED",
    "IN_PROGRESS non engagé"
  ],
  [
    "result_reference",
    "str opaque | None",
    "résultat stable"
  ],
  [
    "failure_code",
    "str statique déclarée | None",
    "REJECTED"
  ],
  [
    "created_at",
    "datetime exact timezone.utc",
    "obligatoire"
  ],
  [
    "expires_at",
    "datetime exact timezone.utc",
    "après fin + fenêtre de rejeu, holds respectés"
  ],
  [
    "revision",
    "int exact >=1",
    "CAS et unicité de clé complète"
  ]
]
```

### Schéma logique BulkAdmissionIdentityV1

```json
{
  "key": [
    "resolved_tenant_id",
    "resolved_subject_id",
    "bulk_type",
    "idempotency_key"
  ],
  "persisted_values": [
    "operation_id",
    "admission_content_sha256",
    "admission_contract_version",
    "admission_content_snapshot",
    "expires_at"
  ],
  "guarantees": [
    "unicité atomique de la clé complète",
    "état initial + extension + Job + binding dans la même transaction",
    "rejeu retourne operation_id original après contrôle actuel",
    "divergence n’exécute aucun effet"
  ]
}
```
~~~~

