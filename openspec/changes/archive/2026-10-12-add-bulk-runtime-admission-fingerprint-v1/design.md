## API interne

```python
@dataclass(frozen=True, slots=True)
class _AdmissionFingerprint:
    canonical_bytes: bytes
    content_sha256: str

def validate_bulk_admission_fingerprint_values(candidate: object) -> list[Diagnostic]: ...
def capture_bulk_admission_fingerprint(candidate: object) -> tuple[_AdmissionFingerprint | None, list[Diagnostic]]: ...
```

- Entrée fermée aux 22 clés FingerprintV1 : execution_version, bulk_type, bulk_version, tenant_context_reference, scope_context_reference, format, conflict_strategy, commit_mode, requested_by_reference, mapping_reference, mapping_version, input_reference, input_version, input_sha256, input_size_bytes, projection_reference, consistency_kind, consistency_reference, idempotency_key, policy_reference, policy_version, expires_at.
- Types : primitives exactes ou None selon canon, aucun dict/bool admis ; `type(x) is str/int/datetime` strict, `bool` refusé partout y compris pour `int`, `float` refusé y compris fini, `None` explicite uniquement où le canon l'admet ; textes non vides UTF-8 strict sans NUL ; SemVer complète via parse_version existant ; SHA hex minuscule 64 ; `int >= 0`, `revision` hors périmètre ; `expires_at` datetime exact `tzinfo is timezone.utc` ; règles IMPORT/EXPORT B02 réutilisées sans modification ; `scope None` ne désigne ni PLATFORM ni tenant global.
- Deux phases : capture owned (dict exact, clés str exactes, 22 clés exactes, copie des valeurs) puis contrôle des valeurs ; diagnostics VALIDATE statiques triés dédupliqués sans écho. Canonicalisation unique interne : tri lexicographique, JSON compact virgule/deux-points, ensure_ascii=False, UTF-8 strict, datetime via isoformat(timespec="microseconds") avec suffixe +00:00 remplacé par Z (année sur quatre chiffres), None->null ; `hashlib.sha256(canonical).hexdigest()`.
- Immutabilité : toute modification ultérieure du dict caller, y compris consistency_reference initiale, ne change JAMAIS le snapshot retourné ; un nouveau capture d'un nouveau contenu reflète sa nouvelle empreinte, ce n'est pas une reprise ; aucun runtime ne recalcule une identité de suivi ici.
- Sans valeur par défaut normative, sans conversion, sans fabrication BulkExecutionV1, sans valeur de suivi, sans ajout normatif.

## Limites

Primitive snapshot seulement : ni valideur complet d'admission, ni persistance, ni autorité, ni idempotence SQL, ni Command/outbox, ni reprise, ni-url, ni rétention.
