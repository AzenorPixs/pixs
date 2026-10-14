## Context

La source normative reste `openspec/specs/bulk-operations/spec.md` (B12, annexe `ExportManifestV1`) et `src/pixs/backend/bulk_execution_values.py` (`_exact_mapping`, `_is_runtime_text`, `_is_complete_semver`, `_pack`, `_refusal`, `Diagnostic`/`VALIDATE`). Inventaire actif : `openspec/changes/` contient `archive/` seul. Les lots Bulk précédents sont livrés et préservés par empreinte.

## Goals / Non-Goals

Garder et capturer en mémoire la forme exacte d un manifeste candidat, sans effet externe. Ce lot ne réalise ni manifeste servi, ni finalisation prouvée, ni horloge, ni gouvernance, ni autorité, ni consistance résolue, ni hash calculé, ni stockage/export/URL/transaction.

## Decisions

- API interne :
```python
@dataclass(frozen=True, slots=True)
class _ExportManifestBound:
    manifest_version: str
    operation_id: str
    format: str
    mapping_reference: str
    mapping_version: str
    tenant_context_reference: str
    scope_context_reference: str | None
    consistency_kind: str
    consistency_reference: str
    row_count: int
    size_bytes: int
    sha256: str
    classification_reference: str
    expires_at: datetime
    object_reference: str
    object_version: str
    complete: bool
def validate_bulk_export_manifest_values(candidate: object) -> list[Diagnostic]: ...
def capture_bulk_export_manifest_values(candidate: object) -> tuple[_ExportManifestBound | None, list[Diagnostic]]: ...
```
- Profil dix-sept clés exactes dans l ordre canonique : `manifest_version`, `operation_id`, `format`, `mapping_reference`, `mapping_version`, `tenant_context_reference`, `scope_context_reference`, `consistency_kind`, `consistency_reference`, `row_count`, `size_bytes`, `sha256`, `classification_reference`, `expires_at`, `object_reference`, `object_version`, `complete`. `type(candidate) is dict`, clés `str` exactes, refus si manquante ou inconnue ; sans omission, défaut, coercition ni nouveau wire format.
- Deux phases types avant comportement : `_exact_mapping` existant puis refus de types exacts puis refus de valeurs, puis `_pack`. Tous types et UTC avant helpers et valeurs. Diagnostics `VALIDATE` statiques, triés, dédupliqués, sans écho de valeur. Liste fraîche à chaque appel.
- Types : douze `str` en `type is str` ; `scope_context_reference` en `str | None` explicite ; `row_count`/`size_bytes` en `type is int` ; `expires_at` en `type is datetime` puis `tzinfo is timezone.utc` identité, sans `utcoffset`, conversion ni horloge ; `complete` en `type is bool`.
- Valeurs : `str` runtime strictes `_is_runtime_text` non vides UTF-8 sans NUL ; `manifest_version == "1.0.0"` exact ; `mapping_version` SemVer complète via `_is_complete_semver` existant ; `format` `CSV` ou `NDJSON` seul ; `consistency_kind` `SNAPSHOT` ou `WATERMARK` seul ; `sha256` hex minuscule 64 caractères ; `row_count`/`size_bytes` `>=0` sans max ; `complete` True ou False mémoire sans preuve de finalisation. UTC est entièrement garanti dans la phase des types.
- Aucune cohérence entre champs, aucun défaut, aucun manifeste servi, finalisation prouvée, horloge, gouvernance, autorité, consistance résolue, hash calculé, stockage/export/URL/transaction.
- `validate_*` rend la liste ; `capture_*` rend `(None, diags)` si refus sinon `(bound owned frozen, [])`. Dataclass privée `frozen/slots` dix-sept scalaires owned ; mutation ultérieure de l appelant sans effet.
- Réutilise uniquement `_exact_mapping`, `_is_runtime_text`, `_is_complete_semver`, `_pack`, `_refusal` + `Diagnostic` + stdlib (`datetime`, `dataclasses`, `re`) ; aucun import DB, ORM, port ou horloge. `__all__` contient uniquement les deux fonctions. Aucun ancien code modifié.

## Validation

`py_compile` des 3 Python ; unitaires frontières dix-sept clés, types exacts, hostiles sans hooks, SemVer, sha, UTC identité, formats/consistances seuls, fraîcheur des listes sans écho ; intégration en processus frais sous gardes existantes réutilisées sans fichiers, réseau, processus, base ou Core concret ; régressions pures existantes y compris les profils purs Bulk existants ; strict du change sans issue ; UTF-8 et LF et périmètre vérifiés. Archive future unique `--skip-specs` puis `STATISTIQUES.md` sous mandat distinct.

## Risks and Limits

Un candidat valide ne prouve ni manifeste servi, ni finalisation, ni horloge, ni gouvernance, ni autorité, ni consistance résolue, ni hash calculé, ni stockage/export/URL/transaction. Les types hostiles ne doivent ni être comparés ni encodés hors garde exacte.
