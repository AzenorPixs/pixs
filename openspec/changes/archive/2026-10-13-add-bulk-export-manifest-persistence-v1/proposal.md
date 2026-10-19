# Proposal — add-bulk-export-manifest-persistence-v1

## Why

Le schéma logique ExportManifestV1 (17 clés, B12) existe sans persistance dédiée. Le pur `bulk_export_manifest_values.py` valide et capture sans I/O ni horloge. Il faut une persistance append-only co-transactionnée au propriétaire, sans modifier le pur, le runtime, Report/Inbox/Envelope/Idempotency, ni prouver finalisation, projection, consistance, classification, gouvernance, READY ou READ_RESULT.

## What Changes

Persistance Django seule : record insert-only 17 colonnes logiques + PK technique, repository insert/get seuls, migration 0010 après 0009 seule, wiring models.py, tests unit offline sous gardes et intégration PG isolée. Compteurs row_count/size_bytes int exact >=0 en pur, TEXT décimal privé canonique en DB avec refus capacité stdlib avant I/O. expires_at entrée timezone.utc exact, DB via _TrustedUtcDateTimeField réutilisé, sans horloge ni expiration appliquée. Same operation_id plusieurs ids = stockage seul, sans latest/unicité publique.

## Capabilities

### New Capabilities

Aucune nouvelle capacité.

### Modified Capabilities

- bulk-operations : delta B12 et deux scénarios repris verbatim, sans ajout normatif.

## Impacts

6 fichiers approuvés seulement :
- src/pixs/backend/bulk_export_manifest_record.py
- src/pixs/backend/bulk_export_manifest_repository.py
- src/pixs/backend/migrations/0010_bulk_export_manifest.py
- src/pixs/backend/models.py
- tests/unit/test_bulk_export_manifest_persistence.py
- tests/integration/test_bulk_export_manifest_persistence_integration.py

Hors périmètre : mutation du pur ou runtime/repo existant/Report/Inbox/Envelope/Idempotency ; production export/finalisation/URL signée/hachage/clock/gouvernance/endpoint/Outbox/PA/PZT ; nouvelle norme/type/default/cardinalité/format public/dépendance/cadrage/Git/frontend.
