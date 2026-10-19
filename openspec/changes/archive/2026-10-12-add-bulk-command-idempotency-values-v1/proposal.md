## Why

Le canon B10 exige la déduplication des Commands par clé canonique `tenant_id, subject_id, command_type, idempotency_key` avec octets canoniques propriétaire versionnés (`content_sha256`, `serializer_version`), états `IN_PROGRESS | SUCCEEDED | REJECTED`, références stables et horodatages UTC (schéma logique `CommandIdempotencyV1`, 12 clés). Aucun validateur pur de ces 12 valeurs n'existe dans le backend ; la persistance/transaction future ne peut pas s'y référer sans cette primitive mémoire.

## What Changes

- Ajouter une primitive pure mémoire `bulk_command_idempotency_values` : valider une entrée fermée aux 12 clés normatives `CommandIdempotencyV1`, sans ORM, persistance, horloge, port, catalogue, auth, purge ni retry.
- Exposer `validate_bulk_command_idempotency_values(candidate) -> list[Diagnostic]` et `capture_bulk_command_idempotency_values(candidate) -> tuple[_CommandIdempotencyBound | None, list[Diagnostic]]`, dataclass privée frozen/slots owned des 12 valeurs ; validation deux phases (types exacts d'abord, puis valeurs), diagnostics `VALIDATE` statiques triés dédupliqués sans écho.
- Contrôles fermés : 7 `str` obligatoires `tenant_id, subject_id, command_type, idempotency_key, content_sha256, serializer_version, state` ; `result_reference, failure_code` `str | None` explicites ; `created_at, expires_at` `datetime` exacts `timezone.utc` ; `revision` `int` exact `>= 1`, `bool` refusé ; `content_sha256` hex minuscule 64 ; `serializer_version` toute SemVer complète valide via parseur existant (non fixée à `1.0.0`) ; `state` exact `IN_PROGRESS | SUCCEEDED | REJECTED`. `IN_PROGRESS` accepté en mémoire sans engagement.
- Ne jamais prouver la provenance des octets propriétaire, ne jamais déclarer `command_type`/`failure_code`, ne jamais inventer fenêtre d'expiration/holds, commit/CAS, ni cohérence résultat/état non fermée.
- Conserver B10, FingerprintV1, BulkAdmissionIdentityV1, profils préparatoires, persistance, ports et canon interactions inchangés.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- interactions : implémentation partielle de B10 limitée aux valeurs `CommandIdempotencyV1` mémoire déjà validées ; requirement B10 et ses 2 scénarios recopiés strictement verbatim, sans recopier ni modifier clauses/annexes ; le canon interactions fait autorité.

## Impact

Quatre artefacts au début uniquement, puis trois Python après mandats : `src/pixs/backend/bulk_command_idempotency_values.py`, `tests/unit/test_bulk_command_idempotency_values.py`, `tests/integration/test_bulk_command_idempotency_integration.py`. Aucun ancien code ou export modifié. Aucune persistance, transaction, horloge, port, catalogue, auth, purge, retry, preuve provenance, déclaration métier, expiration window/holds, commit/CAS ou cohérence inventée. Aucune dépendance nouvelle. Python et conventions du module `bulk_admission_identity_values` réutilisés. Archive unique avec `--skip-specs`.
