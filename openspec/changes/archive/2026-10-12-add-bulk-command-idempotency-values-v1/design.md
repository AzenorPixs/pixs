## API interne

```python
@dataclass(frozen=True, slots=True)
class _CommandIdempotencyBound:
    tenant_id: str
    subject_id: str
    command_type: str
    idempotency_key: str
    content_sha256: str
    serializer_version: str
    state: str
    result_reference: str | None
    failure_code: str | None
    created_at: datetime
    expires_at: datetime
    revision: int

def validate_bulk_command_idempotency_values(candidate: object) -> list[Diagnostic]: ...
def capture_bulk_command_idempotency_values(candidate: object) -> tuple[_CommandIdempotencyBound | None, list[Diagnostic]]: ...
```

- Entrée fermée aux 12 clés exactes : `tenant_id, subject_id, command_type, idempotency_key, content_sha256, serializer_version, state, result_reference, failure_code, created_at, expires_at, revision`.
- Types exacts d'abord, sans hooks étrangers : `type(x) is dict` pour le mapping via `_exact_mapping` existant (clés `str` exactes, refus des sous-classes sans appeler leurs hooks) ; 7 `str` obligatoires en `type is str` ; `result_reference, failure_code` en `type is str or None` explicite ; `created_at, expires_at` en `type is datetime` puis `tzinfo is timezone.utc` (naïf, décalé ou `tzinfo` étranger refusé avant tout callback) ; `revision` en `type is int` strict (`bool` refusé car sous-classe) ; tout candidat étranger, `Hostile`, sous-classe `str/bytes/datetime/dict` ou clé étrangère refusé avant comportement.
- Valeurs ensuite : textes runtime `_is_runtime_text` (non vides, UTF-8 strict, sans NUL) pour les 7 `str` et pour `result_reference/failure_code` lorsqu'ils sont `str` ; `content_sha256` regex `[0-9a-f]{64}` plein ; `serializer_version` toute SemVer complète via `_is_complete_semver` existant (pas de fixation `1.0.0`) ; `state` appartenance exacte `{"IN_PROGRESS", "SUCCEEDED", "REJECTED"}` ; `revision >= 1` ; `created_at/expires_at` recontrôle `timezone.utc`. Aucune comparaison `created_at/expires_at`, aucune fenêtre, aucun hold, aucune règle `result_reference/failure_code` selon `state`, aucune déclaration `command_type/failure_code`, aucun hash recalculé.
- Deux phases partagées : `_exact_mapping` puis refus de types puis refus de valeurs puis `_pack` (triés, dédupliqués, `step == "validate"`, sans écho de secret). `validate_*` rend la liste ; `capture_*` rend `(None, diags)` si refus, sinon `(bound owned frozen, [])` avec copie défensive (`str/datetime/int` immuables, `None` conservé).
- Immutabilité owned : dataclass privée frozen/slots ; toute mutation ultérieure du dict appelant ne change jamais le bound ; `IN_PROGRESS` rendu comme les autres états, sans engager de transaction.
- Réutilise uniquement `bulk_execution_values._exact_mapping, _is_runtime_text, _is_complete_semver, _pack, _refusal` + `Diagnostic` + stdlib (`re`, `datetime`, `dataclasses`) ; aucun import DB/ORM/port/horloge.

## Limites

Valeurs mémoire seulement : ni ORM, ni persistance, ni horloge, ni port, ni catalogue, ni auth, ni purge, ni retry, ni preuve d'octets propriétaire, ni déclaration métier, ni expiration window/holds, ni commit/CAS, ni cohérence résultat/état inventée. `IN_PROGRESS` n'engage rien.
