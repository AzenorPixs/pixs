## Context

La source normative reste `openspec/specs/events/spec.md` (B11, annexe `InboxReceiptV1`) et `src/pixs/backend/bulk_execution_values.py` (`_exact_mapping`, `_is_runtime_text`, `_is_complete_semver`, `_pack`, `_refusal`, `Diagnostic`/`VALIDATE`). Inventaire actif : `openspec/changes/` contient `archive/` seul. Les lots Bulk précédents sont livrés et préservés par empreinte.

## Goals / Non-Goals

Garder et capturer en mémoire la forme exacte d un accusé candidat, sans effet externe. Ce lot ne réalise ni persistance, ni déduplication, ni stockage, ni transaction, ni horloge, ni calcul de hash, ni comparaison de version, ni catalogue, ni provenance, ni auth, ni FK, ni unicité, ni preuve de consommation.

## Decisions

- API interne :
```python
@dataclass(frozen=True, slots=True)
class _InboxReceiptBound:
    consumer_reference: str
    event_id: str
    event_version: str
    content_sha256: str
    state: str
    consumed_at: datetime
    correlation_id: str
    causation_id: str | None
def validate_bulk_inbox_receipt_values(candidate: object) -> list[Diagnostic]: ...
def capture_bulk_inbox_receipt_values(candidate: object) -> tuple[_InboxReceiptBound | None, list[Diagnostic]]: ...
```
- Profil huit clés exactes dans l ordre canonique : `consumer_reference`, `event_id`, `event_version`, `content_sha256`, `state`, `consumed_at`, `correlation_id`, `causation_id`. `type(candidate) is dict`, clés `str` exactes, refus si manquante ou inconnue ; sans omission, défaut, coercition ni nouveau wire format.
- Deux phases types avant comportement : `_exact_mapping` existant puis refus de types exacts puis refus de valeurs, puis `_pack`. Tous types et UTC avant helpers et valeurs. Diagnostics `VALIDATE` statiques, triés, dédupliqués, sans écho de valeur. Liste fraîche à chaque appel.
- Types : `consumer_reference`, `event_id`, `event_version`, `content_sha256`, `state`, `correlation_id` en `type is str` ; `causation_id` en `str | None` explicite ; `consumed_at` en `type is datetime` puis `tzinfo is timezone.utc` identité, sans `utcoffset`, conversion ni horloge.
- Valeurs : `str` runtime strictes `_is_runtime_text` non vides UTF-8 sans NUL ; `event_version` SemVer complète via `_is_complete_semver` existant ; `content_sha256` hex minuscule 64 caractères ; `state == "CONSUMED"` exact seulement. UTC est entièrement garanti dans la phase des types.
- Aucune cohérence entre champs, aucun défaut, aucun engagement ni preuve avant commit, aucune déduplication, stockage, transaction, horloge, calcul, comparaison, catalogue, provenance, auth, FK ou unicité.
- `validate_*` rend la liste ; `capture_*` rend `(None, diags)` si refus sinon `(bound owned frozen, [])`. Dataclass privée `frozen/slots` owned ; mutation ultérieure de l appelant sans effet.
- Réutilise uniquement `_exact_mapping`, `_is_runtime_text`, `_is_complete_semver`, `_pack`, `_refusal` + `Diagnostic` + stdlib (`datetime`, `dataclasses`, `re`) ; aucun import DB, ORM, port ou horloge. `__all__` contient uniquement les deux fonctions. Aucun ancien code modifié.

## Validation

`py_compile` des 3 Python ; unitaires frontières huit clés, types exacts, hostiles sans hooks, SemVer, sha, UTC identité, état seul, fraîcheur des listes sans écho ; intégration en processus frais sous gardes existantes réutilisées sans fichiers, réseau, processus, base ou Core concret ; régressions pures existantes y compris Outbox ; strict du change sans issue ; UTF-8 et LF et périmètre vérifiés. Archive future unique `--skip-specs` puis `STATISTIQUES.md` sous mandat distinct.

## Risks and Limits

Un candidat valide ne prouve ni commit, ni consommation, ni déduplication, ni stockage, ni transaction, ni horloge, ni catalogue, ni auth, ni FK, ni unicité. Les types hostiles ne doivent ni être comparés ni encodés hors garde exacte.
