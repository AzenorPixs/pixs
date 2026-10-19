# Design — add-initial-bulk-export-consistency-kind-v1

## Module
- `src/pixs/backend/bulk_export_consistency_kind.py` : `Enum` standard seul, `SNAPSHOT="SNAPSHOT"`, `WATERMARK="WATERMARK"`, `__all__` en fin de module. Aucun mixin `str`, aucune normalisation, aucune conversion implicite.

## Tests
- Unitaire : contrat public, membres, valeurs, rejet sans normalisation.
- Intégration : harnais processus frais repris de `test_event_publication_state_integration.py`, façade inchangée, gardes réelles et contrôles positifs.

## Invariants
- Usages chaînes existants inchangés (`bulk_export_manifest_values/record`, `bulk_execution_values`, `bulk_admission_fingerprint`, `bulk_runtime_records`, migrations).
- Aucun effet import ; aucun accès DB/core/réseau/processus/environnement/écriture.
