# jobs Specification

## Purpose
Les travaux exécutent les unités de travail persistantes, planifiées et reprises, sans constituer une autorité métier parallèle.

## Requirements

### Requirement: Exécution asynchrone demandée par le Super Admin

Un Job demandé par le Super Admin MUST conserver son acteur initial et son périmètre explicite et appliquer l'exception de `authorization`. Le worker MUST NOT s'authentifier avec ce compte, recevoir ses credentials ni transférer son exception. Une désactivation non dérogée MUST refuser une nouvelle exécution ou reprise selon `initial-administration`.

#### Scenario: Worker sans compte de service Super Admin

- **WHEN** le Super Admin demande un Job dans un tenant qui lui est explicitement accordé
- **THEN** le worker exécute la demande sous son contexte d'acteur initial sans devenir Super Admin ni utiliser ses credentials

#### Scenario: Nouvelle exécution après désactivation

- **WHEN** un Job du Super Admin attend son exécution ou sa reprise quand une désactivation non dérogée s'applique
- **THEN** l'exécution ou la reprise est refusée

### Requirement: Contrôles applicatifs des Jobs et exception

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Dérogation portée par la demande initiale

- **WHEN** un Job demandé par le Super Admin utilise une dérogation à un contrôle applicatif dans son périmètre accordé
- **THEN** ce contrôle ne bloque pas le Job et l'exception n'est pas transférée à un autre acteur

### Requirement: Persistance et états explicites

Chaque travail MUST être persisté avant exécution avec états PENDING, SCHEDULED, RUNNING, SUCCEEDED, RETRYING, FAILED, PAUSED, CANCELLED ou DEAD_LETTER, bail persistant et politique de réessai bornée distinguant erreurs rejouables et métier.

#### Scenario: Reprise après interruption

- **WHEN** un processus s'interrompt pendant un travail
- **THEN** le travail est repris de façon contrôlée sans dépendre de la mémoire locale

### Requirement: Autorisation réévaluée à l'exécution

L'autorisation est vérifiée à la création et à l'exécution ; un travail MUST NOT utiliser un contexte expiré ni élargir le périmètre de l'acteur initial ; l'indisponibilité du contrôle produit un échec fermé.

#### Scenario: Contexte expiré refusé

- **WHEN** le contexte d'authentification a expiré avant l'exécution
- **THEN** le travail échoue de façon diagnostiquée au lieu de s'exécuter en mode permissif

### Requirement: Idempotence et corrélation des travaux

Chaque travail MUST porter identifiants distincts du commandement et de l'opération, corrélation, causalité et périmètre, avec déduplication persistante lorsque nécessaire.

#### Scenario: Double déclenchement dédupliqué

- **WHEN** le même travail est déclenché deux fois
- **THEN** un seul effet métier confirmé est produit et le doublon est tracé

### Requirement: Runtime Bulk v1 B08 — Jobs et liaison persistante

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B08 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Phase persistante

- **WHEN** une opération IMPORT passe de STAGE à VALIDATE
- **THEN** la phase suivante possède un Job et une liaison persistants sans chevauchement actif

#### Scenario: Liaison multiple

- **WHEN** une demande veut rattacher le même Job Bulk à deux opérations
- **THEN** la contrainte refuse la seconde liaison sans modifier la première

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
