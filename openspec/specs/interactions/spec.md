# interactions Specification

## Purpose
Les interactions distinguent les commandes de mutation et les requêtes de lecture, exécutées dans des frontières transactionnelles explicites et autorisées.

## Requirements

### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Command propriétaire avec dérogation métier

- **WHEN** le Super Admin demande une Command dans son périmètre autorisé en dérogeant à une règle métier
- **THEN** la règle dérogée ne bloque pas la Command
- **AND** l'exécution et son résultat restent sous l'autorité Django et le suivi asynchrone ne devient pas un succès déjà acquis

### Requirement: Commandes validées et autorisées

Toute commande MUST être validée métier, autorisée puis exécutée en transaction ; une commande synchrone retourne le résultat, une asynchrone retourne un identifiant d'opération sans présenter la mutation comme acquise.

#### Scenario: Mutation sans autorisation refusée

- **WHEN** une commande ne dispose pas d'une autorisation valide
- **THEN** aucune mutation n'est appliquée et une erreur métier explicite est retournée

### Requirement: Requêtes sans mutation implicite

Une requête de lecture MUST NOT produire de mutation métier implicite et MUST appliquer le filtrage autorisé à la source avant pagination ou projection.

#### Scenario: Lecture filtrée à la source

- **WHEN** une collection contient des ressources non autorisées
- **THEN** seules les ressources autorisées sont retournées, sans filtrage frontal

### Requirement: Idempotence et traçabilité des commandes

Toute commande rejouable MUST porter identifiant, corrélation, causalité, contexte de périmètre et clé d'idempotence ; un rejou à contenu identique restitue le résultat, à contenu divergent produit un conflit explicite.

#### Scenario: Rejou divergent

- **WHEN** la même clé d'idempotence est réutilisée avec un contenu différent
- **THEN** le système retourne un conflit explicite au lieu d'un double effet

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
