## Why

Le runtime Bulk v1 doit garder en mémoire les valeurs logiques `InboxReceiptV1` avant toute persistance ou consommation B11, sans port, ORM, catalogue, autorisation, horloge, déduplication, transaction, calcul, comparaison ni preuve. Il manque la garde exacte des huit clés avec capture owned immuable.

## What Changes

- Ajouter `validate_bulk_inbox_receipt_values(candidate) -> list[Diagnostic]` et `capture_bulk_inbox_receipt_values(candidate) -> tuple[bound | None, list[Diagnostic]]` purs.
- Contrôler mapping exact huit clés, tous types et UTC avant helpers et valeurs, six `str` exactes obligatoires, `causation_id` en `str | None` explicite, `consumed_at` en `datetime` exact `timezone.utc` identité.
- Contrôler valeurs strictes : `str` runtime non vides UTF-8 sans NUL, `event_version` SemVer complète via `_is_complete_semver` existant, `content_sha256` hex minuscule 64 caractères, état `CONSUMED` exact seulement.
- N imposer aucune cohérence entre champs, aucun défaut, aucun engagement ni preuve de consommation avant commit, aucune déduplication, stockage, transaction, horloge, calcul de hash, comparaison de version, catalogue, provenance, auth, FK ou unicité.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- events : outillage partiel de B11 déjà validé ; exigence `MODIFIED` recopiée verbatim, aucune annexe ou règle ajoutée.

## Impact

Trois fichiers Python nouveaux seulement : `src/pixs/backend/bulk_inbox_receipt_values.py`, `tests/unit/test_bulk_inbox_receipt_values.py`, `tests/integration/test_bulk_inbox_receipt_integration.py`, plus quatre artefacts de change. Aucun ancien code modifié, aucun ORM, migration, provider, worker, route HTTP, dépendance, Git ou déploiement. Inventaire actif : `openspec/changes/` contient `archive/` seul. Archive future `--skip-specs`, canon inchangé, puis rapport distinct obligatoire.
