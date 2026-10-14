## Why

Le canon B10 exige un fingerprint SHA-256 du contenu initial d'admission (annexe FingerprintV1, 22 champs, JSON trié compact UTF-8 strict, date UTC six décimales Z, sans float). Aucun sérialiseur canonique ni fingerprint d'admission n'existe dans le backend (contrôle ciblé CGPT) ; la déduplication durable et l'immutabilité du snapshot ne peuvent pas s'y référer sans cette primitive pure.

## What Changes

- Ajouter une primitive pure `initial-snapshot` : valider une entrée fermée 22 champs FingerprintV1, la canonicaliser une seule fois, en rendre le SHA-256 dans un snapshot immuable.
- Exposer `validate_bulk_admission_fingerprint_values(candidate)` et `capture_bulk_admission_fingerprint(candidate) -> tuple[_AdmissionFingerprint | None, list[Diagnostic]]`, dataclass privée frozen/slots contenant bytes canoniques et content_sha256 ; capture owned des 22 valeurs, validation deux phases, canonicalisation unique et hash.
- Refuser tout champ hors 22, notamment les 36 clés BulkExecution ; ne jamais extraire ni recalculer depuis un état muté ; ne jamais recalculer une identité de suivi ici.
- Conserver B02, profils Kernel/Record, persistance, ports, parsing et canon interactions inchangés.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- interactions : implémentation partielle de B10 limitée au fingerprint d'admission déjà validé ; requirement B10 et ses 2 scénarios recopiés strictement verbatim, sans recopier ni modifier clauses/annexes ; le canon interactions fait autorité.

## Impact

Quatre artefacts au début uniquement, puis trois Python après précode validé : module backend, tests unitaires, tests d'intégration `tests/integration/test_bulk_admission_fingerprint_integration.py` (aucun tests/fresh nouveau). Aucune persistance, autorité, idempotence SQL, Command propriétaire, outbox, admission réelle, worker, staging, parsing, HTTP, PA/PZT, dépendance, secret, Git ou déploiement. Python >= 3.12, stdlib + diagnostics + parse_version existants.
