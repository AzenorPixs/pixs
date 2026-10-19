# Références normatives — B08

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 8 | [Contrat BulkOperation suivi par operation_id](../../specs/bulk-operations/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 507 | [Runtime Bulk v1 B01 — Périmètre exécutable](../../specs/bulk-operations/spec.md#L507) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 521 | [Runtime Bulk v1 B02 — Enveloppe et progression](../../specs/bulk-operations/spec.md#L521) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 597 | [Runtime Bulk v1 B06 — Machine à états](../../specs/bulk-operations/spec.md#L597) | P | COMPLETER_OU_INTEGRER |
| jobs / 58 | [Runtime Bulk v1 B08 — Jobs et liaison persistante](../../specs/jobs/spec.md#L58) | P | COMPLETER_OU_INTEGRER |
| jobs / 72 | [Runtime Bulk v1 B09 — Baux, reprise et configuration](../../specs/jobs/spec.md#L72) | P | COMPLETER_OU_INTEGRER |

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

### Référence bulk-operations--903835d3c7

Source : `openspec/specs/bulk-operations/spec.md`, ligne 597. SHA-256 du bloc : `188a5ed48de220764a9d2c74613035c40467ada7b97998b5805fe5608e4b0665`.

~~~~text
### Requirement: Runtime Bulk v1 B06 — Machine à états

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B06 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Transition permise

- **WHEN** une opération non terminale franchit une étape autorisée par la matrice
- **THEN** la transition et sa révision sont persistées avec la preuve de l’étape

#### Scenario: Terminalité conservée

- **WHEN** une demande tente de passer de COMPLETED à RUNNING
- **THEN** la transition est refusée sans réinitialiser progression, checkpoint ou échéance

#### Scenario: Demande d’annulation autorisée sans terminalisation

- **WHEN** une autorité serveur courante autorise CANCEL sur une opération non terminale avec la révision attendue courante
- **THEN** la demande persiste uniquement cancellation_requested et la révision suivante, sans changer progression, checkpoint, échéance, Job ou schedule et sans prétendre annuler une unité déjà engagée

#### Scenario: Demande refusée sans altération concurrente

- **WHEN** l’autorité CANCEL refuse ou reste indisponible, ou que la primitive refuse une opération terminale ou une révision périmée
- **THEN** la demande est refusée sans altérer l’opération ni ses effets engagés, et aucune requête SQL Bulk ne précède l’autorisation serveur

#### Scenario: Transition d’annulation serveur autorisée et coopérative

- **WHEN** une autorité serveur courante autorise CANCEL pour une opération non terminale dont le flag cancellation_requested est True et la révision attendue courante
- **THEN** la transition persiste uniquement CANCELLED et la révision suivante sous les verrous et la matrice canoniques, conserve les effets déjà engagés et tous les autres champs, et interdit de nouvelles unités protégées

#### Scenario: Transition d’annulation refusée sans altération

- **WHEN** l’autorité CANCEL refuse ou reste indisponible, le flag n’est pas True, la révision est périmée ou l’opération est terminale
- **THEN** la transition est refusée sans altération de l’opération ni de ses effets, aucune requête SQL Bulk ne précède l’autorité serveur et aucun retry ou rebase automatique n’est réalisé
~~~~

### Référence jobs--0dc2276581

Source : `openspec/specs/jobs/spec.md`, ligne 58. SHA-256 du bloc : `da7d99daa2b5640e634dc85decfee5facc300dddb342e327786106f66d31f4b3`.

~~~~text
### Requirement: Runtime Bulk v1 B08 — Jobs et liaison persistante

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B08 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Phase persistante

- **WHEN** une opération IMPORT passe de STAGE à VALIDATE
- **THEN** la phase suivante possède un Job et une liaison persistants sans chevauchement actif

#### Scenario: Liaison multiple

- **WHEN** une demande veut rattacher le même Job Bulk à deux opérations
- **THEN** la contrainte refuse la seconde liaison sans modifier la première
~~~~

### Référence jobs--7589701c51

Source : `openspec/specs/jobs/spec.md`, ligne 72. SHA-256 du bloc : `207b14af05f457bfb27b92bcd13808124784099912f63a3de1ae8356d524dbd6`.

~~~~text
### Requirement: Runtime Bulk v1 B09 — Baux, reprise et configuration

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B09 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Reprise sous bail

- **WHEN** un titulaire autorisé acquiert un nouveau bail après interruption
- **THEN** il reprend le dernier checkpoint engagé sous la politique et l’échéance initiales

#### Scenario: Bail périmé

- **WHEN** un ancien titulaire tente une nouvelle unité après expiration ou perte du bail
- **THEN** l’unité est refusée sans nouvel effet ni prolongation implicite

## Annexes normatives — RSMP-BULK-EXECUTION-V1

Les clauses et schémas ci-dessous sont normatifs par les exigences Runtime Bulk v1 qui les référencent. Le schéma logique ne constitue ni une implémentation ni un nouveau wire format public.

### B08 — Jobs et liaison persistante

- Une liaison BulkJobBindingV1 MUST référencer une opération et un Job existants ; job_id MUST être unique dans ces liaisons, et le couple opération/phase MUST être unique.
- Les phases MUST être STAGE, VALIDATE, APPLY et EXPORT ; IMPORT utilise STAGE puis VALIDATE puis APPLY, sauf VALIDATE_ONLY sans APPLY ; EXPORT utilise EXPORT.
- Un seul Job/une seule phase MUST être active pour une opération ; les retries MUST conserver le Job initial et augmenter son compteur de tentatives de façon atomique.
- Les handlers déclarés MUST être pixs.bulk.stage, pixs.bulk.validate, pixs.bulk.apply et pixs.bulk.export, version 1.0.0 ; le payload MUST porter seulement la référence et version de demande d’exécution.
- Le Job MUST conserver l’acteur initial, les corrélations et le périmètre serveur ; il MUST NOT posséder ou réutiliser ses credentials ni transférer une exception.

### B09 — Baux, reprise et configuration

- La politique MUST fournir explicitement les clés de l’annexe PolicyV1, sans défaut numérique ; absence, type étranger, incohérence ou version non résolue MUST refuser l’admission.
- Les tentatives MUST être bornées ; le nombre de délais MUST valoir max_attempts moins un. Chaque délai MUST être positif et une reprise MUST respecter expires_at.
- Les baux MUST avoir propriétaire et expiration persistants, contrôlés par révision ; deux fois renewal_seconds MUST être inférieur à lease_seconds.
- La perte ou expiration du bail MUST interdire une nouvelle unité ; le nouveau titulaire MUST reprendre le dernier checkpoint validé, sans prolonger l’échéance initiale.
- Seuls les échecs déclarés techniques/rejouables par le port de confiance MUST être retentés ; un rejet métier MUST rester un rejet, sans retry permissif.
- Après épuisement technique, le Job MUST être diagnostiqué en DEAD_LETTER ; l’opération MUST devenir FAILED et préserver ses unités déjà engagées.
- Les échéances de scheduling et de tentative MUST être persistées dans JobScheduleV1 ; le runtime MUST NOT ajouter de défaut ni modifier le contrat préparatoire JobRecord existant.

### Schéma logique BulkJobBindingV1

```json
[
  [
    "operation_id",
    "FK BulkOperationRecord, PROTECT",
    "obligatoire"
  ],
  [
    "job_id",
    "FK JobRecord, PROTECT, unique",
    "obligatoire"
  ],
  [
    "phase",
    "STAGE | VALIDATE | APPLY | EXPORT",
    "unique (operation_id,phase)"
  ]
]
```

### Schéma logique JobScheduleV1

```json
[
  [
    "job_id",
    "FK JobRecord unique",
    "obligatoire"
  ],
  [
    "policy_reference",
    "str opaque",
    "politique serveur"
  ],
  [
    "policy_version",
    "str SemVer",
    "immuable"
  ],
  [
    "next_run_at",
    "datetime exact timezone.utc | None",
    "SCHEDULED/RETRYING obligatoire"
  ],
  [
    "attempt_deadline",
    "datetime exact timezone.utc | None",
    "RUNNING obligatoire et <= expires_at"
  ],
  [
    "failure_code",
    "str statique déclarée | None",
    "aucune exception brute"
  ],
  [
    "revision",
    "int exact >=1",
    "CAS"
  ]
]
```

### Schéma logique JobPayloadV1

```json
[
  [
    "execution_reference",
    "str opaque",
    "référence de demande persistante"
  ],
  [
    "execution_version",
    "str SemVer",
    "1.0.0"
  ]
]
```

### Schéma logique JobMetadataBindingV1

```json
{
  "subject": "dict exact requested_by_reference : référence originale ; aucune assertion d’authentification",
  "tenant_context": "dict exact tenant_context_reference et scope_context_reference venant du contexte serveur",
  "perimeter_reference": "ServerContextRefsV1.perimeter_reference ; jamais un fallback déduit d’un None",
  "state_initial": "PENDING ; attempt_count=0 ; lease_owner=None ; lease_expires_at=None explicitement construits",
  "job_type": "nom de handler déclaré B08 ; job_version=1.0.0",
  "correlation": "command_id, job_id et operation_id distincts ; corrélation/causalité explicites selon le contrat propriétaire"
}
```

### Matrice des Jobs

```json
{
  "PENDING": [
    "RUNNING",
    "SCHEDULED",
    "PAUSED",
    "CANCELLED"
  ],
  "SCHEDULED": [
    "RUNNING",
    "PAUSED",
    "CANCELLED"
  ],
  "RUNNING": [
    "SUCCEEDED",
    "RETRYING",
    "FAILED",
    "PAUSED (checkpoint/bail libéré)",
    "CANCELLED",
    "DEAD_LETTER"
  ],
  "RETRYING": [
    "RUNNING (délai atteint)",
    "PAUSED",
    "CANCELLED",
    "DEAD_LETTER"
  ],
  "PAUSED": [
    "PENDING (reprise explicite autorisée)",
    "CANCELLED"
  ],
  "terminals": [
    "SUCCEEDED",
    "FAILED",
    "CANCELLED",
    "DEAD_LETTER"
  ]
}
```
~~~~

