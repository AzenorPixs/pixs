# Références normatives — B01

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 8 | [Contrat BulkOperation suivi par operation_id](../../specs/bulk-operations/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 17 | [Import via staging privé et commandes propriétaires](../../specs/bulk-operations/spec.md#L17) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 507 | [Runtime Bulk v1 B01 — Périmètre exécutable](../../specs/bulk-operations/spec.md#L507) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 535 | [Runtime Bulk v1 B03 — Ports serveur et autorité](../../specs/bulk-operations/spec.md#L535) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 549 | [Résolution de gouvernance GovernanceResolutionV1 fermée](../../specs/bulk-operations/spec.md#L549) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 583 | [Runtime Bulk v1 B05 — Parsing et mapping](../../specs/bulk-operations/spec.md#L583) | P | COMPLETER_OU_INTEGRER |
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

### Référence bulk-operations--f487525180

Source : `openspec/specs/bulk-operations/spec.md`, ligne 17. SHA-256 du bloc : `3b525720d607aa23dfd92c9cb0660cdd64fbc55f3de3d1177547782844745894`.

~~~~text
### Requirement: Import via staging privé et commandes propriétaires

Tout import MUST passer par un espace privé, vérifier taille, type, somme de contrôle et mapping versionné, puis appeler exclusivement les commandes du module propriétaire avec modes VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT explicites ; les conflits sont rejetés par défaut.

#### Scenario: Ligne en conflit rejetée

- **WHEN** une ligne contredit la stratégie de conflit déclarée
- **THEN** elle est rejetée dans un rapport versionné sans mutation partielle silencieuse
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

### Référence bulk-operations--69c76a1b49

Source : `openspec/specs/bulk-operations/spec.md`, ligne 535. SHA-256 du bloc : `eb37e6bf37f23277ac0ee4765ed3f1dc99702bbadd1062d0cc4b3cd1ab7d91fa`.

~~~~text
### Requirement: Runtime Bulk v1 B03 — Ports serveur et autorité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B03 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Autorité effective

- **WHEN** Django résout une décision effective ALLOW dans le tenant et périmètre autorisés
- **THEN** le runtime utilise le contexte serveur sans transférer de credentials ni exception

#### Scenario: Autorité indisponible

- **WHEN** le port retourne DENY ou UNAVAILABLE après application des règles canoniques
- **THEN** aucune action demandée n’est exécutée et aucun contexte exploitable n’est fourni
~~~~

### Référence bulk-operations--dc5f106bcb

Source : `openspec/specs/bulk-operations/spec.md`, ligne 549. SHA-256 du bloc : `4760f8bca12020f05d0cff30dd8266319b4b796d533c49bbb9f6444133058d66`.

~~~~text
### Requirement: Résolution de gouvernance GovernanceResolutionV1 fermée

La réponse GovernanceResolutionV1 MUST respecter les six clés, types, décisions et garanties de l'annexe correspondante, avec résolution effective et capture immuable. Une validation structurelle seule MUST NOT établir cette résolution.

#### Scenario: Résolution positive

- **WHEN** le port composé résout effectivement politique, classification et obligations pour l'autorité courante
- **THEN** la résolution est RESOLVED avec contexte serveur lié, politique, profil et obligations explicites capturés immuables

#### Scenario: Refus fermé

- **WHEN** la gouvernance refuse pour l'autorité courante
- **THEN** la résolution est DENY avec resolved_context, policy, profile et obligations à None, sans contexte exploitable ni repli

#### Scenario: Indisponible ou exception

- **WHEN** le port composé est indisponible ou lève une exception
- **THEN** la résolution est UNAVAILABLE avec les quatre données résolues à None, sans détail brut ni transfert d'exception

#### Scenario: Structure ou type étranger refusé

- **WHEN** une clé manque ou est inconnue, ou le candidat, une clé ou une valeur n'a pas le type exact attendu
- **THEN** la résolution est refusée avant comportement, parsing ou I/O, sans écho de valeur ni invocation étrangère

#### Scenario: Obligations non résolues

- **WHEN** les obligations ne sont pas effectivement résolues en tuple exact
- **THEN** aucune lecture, transfert ou mutation n'est autorisée ; un tuple vide exige une absence explicitement résolue, jamais un défaut

#### Scenario: Contexte divergent refusé

- **WHEN** le contexte résolu ne correspond pas au sujet, tenant, périmètre et contexte de l'autorité courante
- **THEN** la résolution est refusée sans repli ni contexte exploitable
~~~~

### Référence bulk-operations--2f3a43ac59

Source : `openspec/specs/bulk-operations/spec.md`, ligne 583. SHA-256 du bloc : `c27168072d2c3abc27fff23766ccae292a6422d9eda950e4de2c3aa3b8d106f1`.

~~~~text
### Requirement: Runtime Bulk v1 B05 — Parsing et mapping

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B05 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Mapping déclaré

- **WHEN** un fichier conforme utilise un mapping propriétaire immuable et versionné
- **THEN** seuls les champs déclarés sont transmis au contrat public sans conversion heuristique

#### Scenario: Entrée ambiguë

- **WHEN** un CSV contient un header dupliqué ou un NDJSON une clé dupliquée
- **THEN** le parsing refuse l’entrée et produit un diagnostic statique sans contenu brut
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

