# Tasks — add-bulk-event-envelope-persistence-v1

- [x] 1. Artefacts OpenSpec : proposal, design, tasks et delta specs/events avec B11 verbatim, cohérence des six fichiers et des exclusions.
- [x] 2. Record et codec privé : bulk_event_envelope_record.py avec treize clés, event_id PK, TEXT JSON privé, NUL préservé, UTC strict, copies owned, insert-only.
- [x] 3. Repository, models et migration : bulk_event_envelope_repository.py insert/get avec alias unique et duplicata PK 23505, import minimal dans models.py, migrations/0007_bulk_event_envelope.py dépendant de 0006 et réversible.
- [x] 4. Tests unitaires offline : tests/unit/test_bulk_event_envelope_persistence.py en processus frais, gardes, types hostiles avant callbacks/I/O, NUL payload/-0.0/grand int supporté/refus capacité réelle, UTC, copies et gel, save insert-only/full_clean exclude, migration vue sans base.
- [x] 5. Tests PostgreSQL isolés : tests/integration/test_bulk_event_envelope_persistence_integration.py avec schéma possédé, co-commit/co-rollback, transaction active obligatoire même alias, race une seule création, refus capturé toujours rollback owner, contraintes, forward/reverse 0007 seule, nettoyage et connexions.
- [x] 6. Validations et acceptation : py_compile des fichiers, unittest applicables, contrôle OpenSpec selon DEVOPS.md, régressions pertinentes, conformité au périmètre sans écart.

Note : l'archivage et le rapport par archive suivent une procédure distincte après preuves et ne forment pas une tâche circulaire ici.
