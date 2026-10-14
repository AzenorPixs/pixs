## Why

Le runtime Bulk v1 doit garder en mémoire les valeurs logiques `ExportManifestV1` avant toute finalisation B12, sans port, ORM, stockage, export, URL, transaction, horloge, gouvernance, autorisation, consistance résolue, hash calculé ni preuve. Il manque la garde exacte des dix-sept clés avec capture owned immuable.

## What Changes

- Ajouter `validate_bulk_export_manifest_values(candidate: object) -> list[Diagnostic]` et `capture_bulk_export_manifest_values(candidate: object) -> tuple[_ExportManifestBound | None, list[Diagnostic]]` purs, sans exception ni `list[str]`.
- Contrôler mapping exact dix-sept clés, tous types et UTC avant helpers et valeurs, douze `str` exactes obligatoires, `scope_context_reference` en `str | None` explicite, `row_count`/`size_bytes` en `int` exact `>=0` sans max, `expires_at` en `datetime` exact `timezone.utc` identité, `complete` en `bool` exact.
- Contrôler valeurs strictes : `str` runtime non vides UTF-8 sans NUL, `manifest_version` EXACT `1.0.0`, `mapping_version` SemVer complète via `_is_complete_semver` existant, `format` `CSV|NDJSON` seul, `consistency_kind` `SNAPSHOT|WATERMARK` seul, `sha256` hex minuscule 64 caractères, `complete` True ou False mémoire.
- N imposer aucun manifeste servi, finalisation prouvée, horloge, gouvernance, autorité, consistance résolue, hash calculé, stockage/export/URL/transaction, défaut, cohérence entre champs ni preuve.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : outillage partiel de B12 déjà validé ; exigence `MODIFIED` recopiée verbatim, aucune annexe ou règle ajoutée.

## Impact

Trois fichiers Python nouveaux seulement : `src/pixs/backend/bulk_export_manifest_values.py`, `tests/unit/test_bulk_export_manifest_values.py`, `tests/integration/test_bulk_export_manifest_integration.py`, plus quatre artefacts de change. Aucun ancien code modifié, aucun ORM, migration, provider, worker, route HTTP, dépendance, Git ou déploiement. Inventaire actif : `openspec/changes/` contient `archive/` seul. Archive future `--skip-specs`, canon inchangé, puis rapport distinct obligatoire.
