# events Specification

## Purpose
Les événements notifient des faits déjà survenus, versionnés et immuables, sans remplacer les garanties transactionnelles synchrones.

## Requirements

### Requirement: Événements immuables versionnés

Chaque événement MUST porter type, version, producteur, schéma et périmètre d'ordre déclaré ; les événements de domaine internes et d'intégration publics restent des contrats distincts.

#### Scenario: Contrat d'intégration séparé

- **WHEN** un événement de domaine est exposé vers l'extérieur
- **THEN** il passe par un contrat d'intégration versionné distinct, jamais par exposition directe

### Requirement: Publication après validation transactionnelle

Un événement issu d'une mutation MUST être publié uniquement après validation de la transaction ; en cas d'échec, il reste absent du mécanisme de diffusion.

#### Scenario: Transaction échouée sans événement

- **WHEN** la transaction métier échoue
- **THEN** aucun événement d'acquisition n'est publié

### Requirement: Consommateurs idempotents et ordonnés

La garantie générale est au-moins-une-fois ; l'ordre n'est garanti que par agrégat ou partition déclaré ; les consommateurs MUST supporter les rejou sans double effet métier.

#### Scenario: Rejou sans double effet

- **WHEN** un événement est livré deux fois
- **THEN** le consommateur le déduplique et ne produit qu'un seul effet confirmé

### Requirement: Profil préparatoire de déclaration d'enregistrement d'événement v1

Le profil `EventRegistrationDeclarationV1` MUST être figé et contenir uniquement `owner_id`, `entry_id` et `event_contract`. Les deux identifiants MUST être des chaînes exactes non vides, sans coercition ni normalisation ; `event_contract` MUST être un objet exact `DomainEventContract` ou `IntegrationEventContract` existant, sans copie de leurs cinq champs.

#### Scenario: Déclaration passive de contrat de domaine

- **WHEN** une déclaration fournit les trois champs et un contrat de domaine structurellement valide
- **THEN** sa validation structurelle réussit sans enregistrer ni publier un événement

#### Scenario: Contrat d'intégration distinct

- **WHEN** le champ `event_contract` porte un objet exact `IntegrationEventContract`
- **THEN** sa nature distincte est conservée sans substitution par un contrat de domaine

### Requirement: Validation fermée de la déclaration d'enregistrement v1

La validation MUST refuser les types étrangers, sous-classes et valeurs invalides sans coercition ; elle MUST réutiliser les validateurs structurels existants du contrat porté. Les refus MUST produire des diagnostics `VALIDATE` existants, stables et triés, sans écho des valeurs brutes, sans IO ni exécution de callback fourni par l'appelant.

#### Scenario: Référence ou type étranger refusé

- **WHEN** un identifiant est vide, non exactement une chaîne, ou un objet de déclaration ou de contrat est étranger au profil
- **THEN** la validation refuse l'entrée avec des diagnostics sans valeur brute et sans effet

#### Scenario: Contrat porté invalide

- **WHEN** un contrat de domaine ou d'intégration exact ne satisfait pas son validateur structurel existant
- **THEN** la déclaration est refusée sans réinterpréter les champs ni affaiblir la validation du contrat

### Requirement: Frontière préparatoire de la déclaration d'enregistrement v1

Cette validation MUST rester seulement structurelle : elle ne prouve ni propriétaire admis, existence, résolution, légitimité ou sensibilité d'une référence. Elle MUST NOT réaliser d'enregistrement, d'abonnement, de publication ou de livraison, ni ouvrir le registre d'événements P0 ; sa réussite MUST NOT être présentée comme un bus d'exécution livré.

#### Scenario: Validité structurelle sans admission runtime

- **WHEN** une déclaration satisfait le profil préparatoire
- **THEN** les refus d'admission du registre P0 et les garanties existantes après commit, au-moins-une-fois, d'idempotence et d'ordre déclaré restent inchangés

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
