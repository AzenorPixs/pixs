# Tasks — add-bulk-export-manifest-persistence-v1

- [x] 1. Artefacts stricts pré-code : vérifier proposal headers Why/What Changes, design 17/18/TEXT/TrustedUtc, delta B12 verbatim, 6 fichiers seuls, sans code.
- [x] 2. Modèle/repo/migration/wiring : record 17+PK, repository insert/get, migration 0010 après 0009, models.py wiring seul, sans toucher pur/runtime existants.
- [x] 3. Tests unitaires offline : pur 17 + record/repository sous gardes réelles, frozen, owned, deferred/exclude, alias/atomic, malformed/capacity.
- [x] 4. Tests PG isolés : helper job_record_16hex inchangé, 18 colonnes/checks, roundtrip/None/False/UTC/grands ints, observer, co-commit/rollback, CHECK 23514, forward/reverse 0010.
- [x] 5. Compilation et régressions strictes : py_compile 6 fichiers, contrôles Django du modèle dans harness offline sous gardes, suites unit/integration ciblées, strict qualifié, sans élargir.
- [x] 6. Acceptation scope : 17 explicites, co-transaction owner, même operation stockage seul, non-preuve finalisation/READY/READ_RESULT/gouvernance, exclusions tenues.

Mention : après 6 prouvées, archivage unique et STATISTIQUES.md par archive (hors ces 6, tâche distincte sur mandat séparé).
