# Références normatives — B07

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| events / 72 | [Runtime Bulk v1 B11 — Outbox et publication](../../specs/events/spec.md#L72) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence events--989ce2593c

Source : `openspec/specs/events/spec.md`, ligne 72. SHA-256 du bloc : `dab4d54506434596b7a9f04290161146387c4ce8d0e00c58993f8e8313d0fa20`.

~~~~text
### Requirement: Runtime Bulk v1 B11 — Outbox et publication

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B11 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Rollback sans publication

- **WHEN** la transaction propriétaire qui écrit l’événement est annulée
- **THEN** l’événement n’est pas disponible à la publication

#### Scenario: Livraison répétée

- **WHEN** une interruption survient après émission mais avant accusé persistant
- **THEN** une répétition reste possible et l’inbox empêche un second effet confirmé

## Annexes normatives — RSMP-BULK-EXECUTION-V1

Les clauses et schémas ci-dessous sont normatifs par les exigences Runtime Bulk v1 qui les référencent. Le schéma logique ne constitue ni une implémentation ni un nouveau wire format public.

### B11 — Outbox et publication

- L’outbox MUST appartenir au runtime et MUST NOT être une responsabilité du Kernel ; événement et mutation MUST être écrits dans la même transaction propriétaire.
- L’enveloppe MUST respecter EventEnvelopeV1 ; contrats DOMAIN et INTEGRATION MUST rester distincts et leurs payloads minimisés, déclarés et validés.
- Le publisher MUST lire uniquement des événements engagés et respecter PENDING, PUBLISHED, RETRYING, FAILED ou DEAD_LETTER sous bail et politique bornés.
- La garantie MUST être au-moins-une-fois ; une interruption après émission et avant accusé persistant MUST pouvoir produire un doublon, jamais une promesse exactly-once.
- L’inbox MUST dédupliquer par consumer_reference et event_id, vérifier version/fingerprint et engager consommation et effets dans une même frontière transactionnelle déclarée.
- Un effet externe MUST utiliser l’idempotence déclarée du provider ; son absence MUST refuser une garantie de déduplication.
- L’outbox MUST allouer atomiquement un sequence_index par périmètre d’ordre ; un événement antérieur non PUBLISHED MUST bloquer les suivants de ce périmètre, sans bloquer un périmètre indépendant.
- Une remise en attente d’un événement FAILED ou DEAD_LETTER MUST être une opération explicite autorisée et bornée, sans modifier son enveloppe ni réexécuter la mutation métier.

### Schéma logique EventEnvelopeV1

```json
[
  [
    "event_id",
    "str opaque",
    "clé locale unique et immuable"
  ],
  [
    "kind",
    "DOMAIN | INTEGRATION",
    "obligatoire"
  ],
  [
    "event_type",
    "str opaque",
    "contrat déclaré"
  ],
  [
    "event_version",
    "str SemVer",
    "version déclarée"
  ],
  [
    "producer_reference",
    "str opaque",
    "composant déclaré"
  ],
  [
    "schema_reference",
    "str opaque",
    "schéma déclaré"
  ],
  [
    "order_scope_reference",
    "str opaque",
    "partition/agrégat déclaré ; aucune promesse d'ordre global"
  ],
  [
    "occurred_at",
    "datetime exact aware UTC",
    "obligatoire"
  ],
  [
    "subject_reference",
    "str opaque",
    "obligatoire"
  ],
  [
    "tenant_context_reference",
    "str opaque | None",
    "None uniquement si contexte non tenant explicite autorisé"
  ],
  [
    "correlation_id",
    "str opaque",
    "obligatoire"
  ],
  [
    "causation_id",
    "str opaque | None",
    "absence explicite"
  ],
  [
    "payload",
    "objet JSON borné conforme au schéma propriétaire",
    "minimisé ; aucun secret"
  ]
]
```

### Schéma logique OutboxPublicationV1

```json
[
  [
    "event_id",
    "FK enveloppe immuable, unique",
    "obligatoire"
  ],
  [
    "state",
    "PENDING | PUBLISHED | RETRYING | FAILED | DEAD_LETTER",
    "initial PENDING explicite"
  ],
  [
    "attempt_count",
    "int exact >=0",
    "initial 0 explicite"
  ],
  [
    "lease_owner",
    "str opaque | None",
    "couplé à lease_expires_at"
  ],
  [
    "lease_expires_at",
    "datetime exact timezone.utc | None",
    "bail persistant"
  ],
  [
    "next_attempt_at",
    "datetime exact timezone.utc | None",
    "RETRYING obligatoire"
  ],
  [
    "published_at",
    "datetime exact timezone.utc | None",
    "PUBLISHED obligatoire"
  ],
  [
    "failure_code",
    "str statique déclarée | None",
    "échec minimisé"
  ],
  [
    "sequence_index",
    "int exact >=1",
    "unique(order_scope_reference,sequence_index), alloué dans la transaction"
  ],
  [
    "policy_reference",
    "str opaque",
    "serveur"
  ],
  [
    "policy_version",
    "str SemVer",
    "immuable"
  ],
  [
    "revision",
    "int exact >=1",
    "CAS"
  ]
]
```

### Schéma logique InboxReceiptV1

```json
[
  [
    "consumer_reference",
    "str déclarée",
    "clé composée"
  ],
  [
    "event_id",
    "str opaque",
    "clé composée"
  ],
  [
    "event_version",
    "str SemVer",
    "version traitée"
  ],
  [
    "content_sha256",
    "hex minuscule 64 caractères",
    "divergence même clé refusée"
  ],
  [
    "state",
    "CONSUMED",
    "construit explicitement, jamais preuve avant commit"
  ],
  [
    "consumed_at",
    "datetime exact timezone.utc",
    "même transaction que les effets"
  ],
  [
    "correlation_id",
    "str opaque",
    "obligatoire"
  ],
  [
    "causation_id",
    "str opaque | None",
    "absence explicite"
  ]
]
```

### Schéma logique JSONValueV1

```json
{
  "types": "None, bool exact, int exact, float exact fini, str Unicode valide, list exacte ou dict exact à clés str exactes ; récursion bornée, doublons refusés au parsing",
  "authority": "Conformité au schéma public propriétaire et aux limites de capacité requise ; aucun objet Python, coercition, sérialisation arbitraire, code ou valeur spéciale non JSON.",
  "storage": "Schéma logique indépendant du choix physique validé du provider ; aucune capacité de représentation n’est présumée si le provider ne la garantit pas."
}
```
~~~~

