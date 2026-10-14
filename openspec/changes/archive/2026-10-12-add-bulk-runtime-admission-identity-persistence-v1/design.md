## API interne

```python
@dataclass(frozen=True, slots=True)
class _AdmissionIdentityBound:
    resolved_tenant_id: str
    resolved_subject_id: str
    bulk_type: str
    idempotency_key: str
    operation_id: str
    admission_content_sha256: str
    admission_contract_version: str
    admission_content_snapshot: bytes
    expires_at: datetime

def validate_bulk_admission_identity_values(candidate: object) -> list[Diagnostic]: ...
def capture_bulk_admission_identity(candidate: object) -> tuple[_AdmissionIdentityBound | None, list[Diagnostic]]: ...

class BulkAdmissionIdentityRecord(models.Model): ...
    @classmethod
    def from_values(cls, values: object) -> "BulkAdmissionIdentityRecord": ...
    def as_values(self) -> dict: ...
    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True): ...

class BulkAdmissionIdentityRepository:
    def __init__(self, using: str = "default"): ...
    def insert_identity(self, *, values: dict) -> None: ...
    def get_identity(self, *, resolved_tenant_id: object, resolved_subject_id: object, bulk_type: object, idempotency_key: object) -> dict | None: ...
```

- Module pur `bulk_admission_identity_values.py` : aucune import ORM/DB ;
  entrée fermée aux 9 clés exactes, capture owned puis contrôles. Types
  exacts d'abord (`type(x) is str/bytes/datetime`, `bool` refusé, `float`
  refusé), textes non vides UTF-8 strict sans NUL, `bulk_type` dans
  `{IMPORT, EXPORT}`, SHA hex minuscule 64, `admission_contract_version`
  `1.0.0` exacte SemVer, `expires_at` datetime exact `tzinfo is timezone.utc`,
  `admission_content_snapshot` bytes non vides.
- Snapshot strict : décodage UTF-8 strict refusé si invalide ; `json.loads`
  avec refus de doublons, refus de float/NaN/Infinity, refus de clés hors 22
  FingerprintV1, refus des champs de suivi ; reconstruction du candidat 22
  champs avec types canoniques stricts puis appel à
  `capture_bulk_admission_fingerprint` existant ; `recapture.canonical_bytes`
  MUST égaler exactement les bytes fournis, sinon refus. Digest fourni MUST
  égaler `recapture.content_sha256`. `bulk_type`, `idempotency_key` et
  `admission_contract_version` fournis MUST égaler les valeurs correspondantes
  du snapshot recapturé (`bulk_type`, `idempotency_key`, `execution_version`).
  `resolved_tenant_id`/`resolved_subject_id` résolus MUST NOT être déduits ni
  comparés aux références opaques `tenant_context_reference` /
  `requested_by_reference` du snapshot : dimensions distinctes, aucune
  confusion.
- `expires_at` d'entrée conservé tel quel UTC exact ; aucune exigence
  d'égalité avec l'`expires_at` du snapshot, aucune règle de rétention
  active.
- Diagnostics VALIDATE statiques triés dédupliqués sans écho de valeur.
- Module `bulk_admission_identity_record.py` : `from_values` valide le dict
  explicite via le module pur avant construction, sans sauvegarde ;
  `full_clean` contrôle les 9 attributs avant conversion ORM même avec
  `exclude`, `ValidationError` statiques sans valeurs ; `save` standard sans
  `full_clean` implicite.
- Module `bulk_admission_identity_repository.py` : `insert_identity` valide
  puis `save(force_insert=True)` dans un `transaction.atomic(using=...)` imbriquable dans la transaction appelante, sans
  `update_or_create`, sans `get_or_create`, sans raw SQL promis hors contrat ;
  `get_identity` contrôle les 4 types de clé avant toute I/O, retourne une
  copie owned ou `None`, sans exception de non-trouvé. Immutabilité garantie
  par l'absence de tout chemin update/purge/touch_expiry. Aucun contournement
  par création d'une clé différente pour corriger une ligne.

## Représentation SQL — choix internes explicites

Choix internes non normatifs, sans extension PG crypto :

- `id` : `BigAutoField` primaire locale technique, non métier.
- `resolved_tenant_id`, `resolved_subject_id`, `idempotency_key`,
  `operation_id` : `TextField` non NULL, non vide (CheckConstraint).
- `bulk_type` : `TextField` non NULL, `choices=[IMPORT, EXPORT]`.
- `admission_content_sha256` : `TextField` non NULL, regex 64 hex minuscule
  côté applicatif ; CheckConstraint regex `^[0-9a-f]{64}$`, sans preuve canonique
  par SQL seul.
- `admission_contract_version` : `TextField` non NULL, `1.0.0` exact
  (CheckConstraint) ; SemVer vérifiée côté applicatif.
- `admission_content_snapshot` : `BinaryField` non NULL (BYTEA), octets
  canoniques exacts ; aucun `JSONField` normalisé.
- `expires_at` : `_TrustedUtcDateTimeField` existant.
- `UniqueConstraint` atomique sur
  `(resolved_tenant_id, resolved_subject_id, bulk_type, idempotency_key)` ;
  aucune contrainte d'unicité sur `operation_id`, aucune FK métier. La
  validation applicative complète précède l'ORM ; les contraintes SQL ne
  constituent pas la preuve complète du canon.

## Relation snapshot / digest / version

- `snapshot` = bytes canoniques FingerprintV1 ; `digest` = SHA-256 hex de ces
  bytes ; `version` = `1.0.0` figée. Les trois sont liés et vérifiés ensemble
  avant écriture ; après écriture ils sont immuables.

## Rétention sans purge — limite explicite

- `expires_at` mémorise l'échéance B10 sans l'exécuter. Aucun purgeur, aucun
  `touch_expiry`, aucun hold, aucune expiration active. Une entrée encore
  requise MUST NOT être purgée ; ce change ne purge rien.

## Migration et câblage

- Migration `0005_bulk_admission_identity` dépendant de `0004`,
  `CreateModel` unique, réversible ; forward/reverse 0005 isolé prouvé en PG
  sans toucher les tables existantes.
- `models.py` : import minimal du module record pour enregistrement, sans
  changement de comportement.

## Limites

Persistance seule : ni admission publique, ni autorisation, ni rejeu rendu,
ni conflit persisté, ni CAS avec révision, ni transaction
admission+extension+Job exécutée ici, ni Command/outbox, ni holds, ni purge,
ni URL, ni rétention active.
