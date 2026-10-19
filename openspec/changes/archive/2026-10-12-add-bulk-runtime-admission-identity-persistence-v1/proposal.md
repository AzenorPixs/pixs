## Why

Le canon `interactions` B10 exige une déduplication durable par clé complète
`(resolved_tenant_id, resolved_subject_id, bulk_type, idempotency_key)` avec
contenu initial immuable et fingerprint SHA-256 FingerprintV1. Le schéma
logique `BulkAdmissionIdentityV1` existe mais aucune persistance interne ne
conserve la clé complète, le snapshot initial exact, son digest, sa version
de contrat et son échéance. Sans cette persistance, aucune admission future
ne peut retrouver l'`operation_id` initial ni détecter une divergence sans
second effet.

## What Changes

- Ajouter une persistance interne `BulkAdmissionIdentity` en trois petits
  fichiers dédiés : module pur `bulk_admission_identity_values.py` (dataclass
  privée `_AdmissionIdentityBound` + validation/capture des 9 clés, sans ORM),
  `bulk_admission_identity_record.py` (modèle/from_values/as_values/full_clean),
  `bulk_admission_identity_repository.py` (insert/get seuls), plus import
  minimal dans `models.py` et migration réversible `0005`.
- Réutiliser strictement `capture_bulk_admission_fingerprint` existant :
  snapshot bytes exacts non vides vérifiés UTF-8 strict, JSON fermé 22 champs
  reconstruit de façon stricte, recapture égale octet pour octet aux bytes
  fournis ; rejeter JSON non canonique, doublons, champs de suivi, float/NaN.
  Vérifier cohérence `bulk_type`/`idempotency_key`/`contract_version` avec le
  snapshot ; ne jamais confondre tenant/acteur résolus avec les références
  opaques du snapshot. `expires_at` d'entrée conservé UTC exact sans règle
  d'égalité à l'échéance snapshot ni rétention active inventée.
- Garantir l'immutabilité par repository insert/get sans update/purge ;
  `insert` en `force_insert` seul, lookup owned. Aucune correction par
  création d'une clé différente.
- Ne créer aucune admission publique, aucun rejeu autorisé, aucun
  update/purge/touch_expiry, aucun moteur de holds, aucune autorité, aucune
  FK métier, aucune unicité `operation_id`, aucun CAS sans révision
  normative, aucune `CommandIdempotency`/outbox, aucune extension PG crypto.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- interactions : outillage partiel de B10 limité à la persistance interne de
  l'identité d'admission déjà validée ; requirement B10 et ses 2 scénarios
  recopiés strictement verbatim, sans recopier ni modifier clauses/annexes ;
  le canon interactions fait autorité.

## Impact

Quatre artefacts au début uniquement, puis après précode validé : trois
modules backend dédiés, une migration réversible, un import minimal
`models.py`, un test unitaire pur, un test d'intégration en processus frais
pur, un test PG synthétique en schéma privé avec forward/reverse 0005 isolé,
concurrence d'unicité et rollback. Aucune route HTTP, worker, staging,
parsing, PA/PZT, dépendance, secret, Git ou déploiement. Python >= 3.12,
stdlib + Django + diagnostics existants. Archive unique `--skip-specs`
prévue, canon inchangé.
