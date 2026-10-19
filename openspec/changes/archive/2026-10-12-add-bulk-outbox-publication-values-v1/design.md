## Context

La source normative reste `openspec/specs/events/spec.md` (B11, annexe `OutboxPublicationV1`) et `src/pixs/backend/bulk_execution_values.py` (`_exact_mapping`, `_is_runtime_text`, `_is_complete_semver`, `_pack`, `_refusal`, `Diagnostic`/`VALIDATE`). Inventaire actif : `openspec/changes/` contient `archive/` seul. Les lots Bulk precedents sont livres et preserves par empreinte.

## Goals / Non-Goals

Garder et capturer en memoire la forme exacte d une publication candidate, sans effet externe. Ce lot ne realise ni persistance, ni publication, ni catalogue, ni autorisation, ni horloge, ni allocation de sequence, ni CAS, ni retry, ni SQL, ni preuve serveur.

## Decisions

- API interne :
```python
@dataclass(frozen=True, slots=True)
class _OutboxPublicationBound:
    event_id: str
    state: str
    attempt_count: int
    lease_owner: str | None
    lease_expires_at: datetime | None
    next_attempt_at: datetime | None
    published_at: datetime | None
    failure_code: str | None
    sequence_index: int
    policy_reference: str
    policy_version: str
    revision: int
def validate_bulk_outbox_publication_values(candidate: object) -> list[Diagnostic]: ...
def capture_bulk_outbox_publication_values(candidate: object) -> tuple[_OutboxPublicationBound | None, list[Diagnostic]]: ...
```
- Profil douze cles exactes dans l ordre canonique : `event_id`, `state`, `attempt_count`, `lease_owner`, `lease_expires_at`, `next_attempt_at`, `published_at`, `failure_code`, `sequence_index`, `policy_reference`, `policy_version`, `revision`. `type(candidate) is dict`, cles `str` exactes, refus si manquante ou inconnue ; sans omission, defaut, coercition ni nouveau wire format.
- Deux phases types avant comportement : `_exact_mapping` existant puis refus de types exacts puis refus de valeurs, puis `_pack`. Diagnostics `VALIDATE` statiques, tries, dedupliques, sans echo de valeur. Liste fraiche a chaque appel.
- Types : `event_id/state/policy_reference/policy_version` en `type is str` ; `lease_owner/failure_code` en `str | None` explicite ; `attempt_count/sequence_index/revision` en `type is int` strict ; `lease_expires_at/next_attempt_at/published_at` en `type is datetime | None` puis `tzinfo is timezone.utc` identite si present, sans `utcoffset`, conversion ni horloge.
- Valeurs : `str` runtime strictes `_is_runtime_text` non vides UTF-8 sans NUL ; `attempt_count >= 0`, `sequence_index >= 1`, `revision >= 1` sans borne superieure inventee ; `state` dans `{"PENDING","PUBLISHED","RETRYING","FAILED","DEAD_LETTER"}` ; `policy_version` SemVer complete via `_is_complete_semver` existant ; datetimes recontrolees `timezone.utc`.
- Seuls couplages fermes : `lease_owner is None` ssi `lease_expires_at is None` ; si `state == "RETRYING"` alors `next_attempt_at is not None` ; si `state == "PUBLISHED"` alors `published_at is not None`. Aucune reciproque, aucune autre coherence etat/champ, aucun bail actif, aucune comparaison de dates.
- `PENDING` explicite et compteur `0` sont des valeurs initiales de l appelant ; aucun defaut, initialisation ni restriction historique `PENDING/count`.
- `validate_*` rend la liste ; `capture_*` rend `(None, diags)` si refus sinon `(bound owned frozen, [])`. Dataclass privee `frozen/slots` owned ; mutation ulterieure de l appelant sans effet.
- Reutilise uniquement `_exact_mapping`, `_is_runtime_text`, `_is_complete_semver`, `_pack`, `_refusal` + `Diagnostic` + stdlib (`datetime`, `dataclasses`) ; aucun import DB/ORM/port/horloge. `__all__` contient uniquement les deux fonctions. Aucun ancien code modifie.

## Validation

`py_compile` des 3 Python ; unitaires frontieres 12 cles, types exacts, hostiles sans hooks, ints, SemVer, UTC identite, couplages fermes seuls, fraicheur des listes sans echo ; integration en processus frais sous gardes existantes reutilisees sans fichiers/reseau/processus/base/Core concret ; regressions existantes ; strict du change sans issue ; UTF-8/LF et perimetre verifies. Archive future unique `--skip-specs` puis `STATISTIQUES.md` sous mandat distinct.

## Risks and Limits

Un candidat valide ne prouve ni FK, ni unicite, ni allocation, ni publication, ni retry, ni CAS, ni catalogue, ni politique serveur. Les types hostiles ne doivent ni etre compares ni encoder hors garde exacte.
