## API interne

```python
class BulkCommandIdempotencyRecord(models.Model):
    @classmethod
    def from_values(cls, values: object) -> "BulkCommandIdempotencyRecord": ...
    def as_values(self) -> dict: ...
    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True): ...

class BulkCommandIdempotencyRefused(Exception): ...
class BulkCommandIdempotencyConflict(Exception): ...
class BulkCommandIdempotencyStale(Exception): ...

class BulkCommandIdempotencyRepository:
    def __init__(self, using: str = "default"): ...
    def get_entry(self, *, tenant_id: object, subject_id: object, command_type: object, idempotency_key: object) -> dict | None: ...
    def replay(self, *, tenant_id: object, subject_id: object, command_type: object, idempotency_key: object, content_sha256: object, serializer_version: object) -> dict | None: ...
    def finalize_terminal(self, token: object, *, expected_revision: object, state: object, result_reference: object, failure_code: object) -> int: ...
    @contextmanager
    def idempotent_unit(self, *, values: object): ...
```

- Pur existant inchangé et non redéfini : `capture_bulk_command_idempotency_values` / `validate_bulk_command_idempotency_values` seuls producteurs du Bound. Aucune clé logique/wire ajoutée. Jeton privé `_IdempotentUnitToken` et bookkeeping internes : alias, thread_ident, clé complète, expected_revision, active, finalized, failed_latched ; is_replay est un indicateur privé de contrôle, pas une clé logique supplémentaire.
- `bulk_command_idempotency_record.py` : `from_values` valide le dict explicite via le pur avant construction, sans sauvegarde ; `full_clean` contrôle les 12 attributs avant conversion ORM même avec `exclude`, `ValidationError` statiques sans valeurs ; `save` standard sans `full_clean` implicite et sans preuve workflow ; `as_values` données ORM de confiance seules, copie owned.
- `bulk_command_idempotency_repository.py` nouveau dédié, sans toucher `bulk_runtime_repository.py` : pas de `store_initial` public autonome. Seule fonction privée `_insert_transient` appelée par `idempotent_unit`. `get_entry` contrôle les 4 types de clé avant I/O, copie owned ou `None`. `replay` readonly : même clé complète + digest ET serializer identiques et état terminal => rend copie stable sans nouvelle entrée ni révision ; même clé avec digest/version différents => conflit explicite ; clé distincte => `None` sans rejet ; jamais finalisable ni modifiable.
- `finalize_terminal` exige le jeton exact actif retourné par `idempotent_unit`, même objet, même thread, même alias, non finalisé ni en échec latched. N'accepte que `SUCCEEDED/REJECTED` avec result_reference/failure_code contrôlés par les types et valeurs du validateur pur existant, sans nouvelle relation état/références inventée. expected_revision est explicite, int exact incrémentable, et correspond à la réservation et au CAS SQL. Conserve octets/valeurs initiales, refuse toute divergence de clé/digest/serializer, applique CAS par `update` filtré `revision=expected` vers `revision+1`, stale => `BulkCommandIdempotencyStale` sans retry implicite, `IntegrityError` => refus statique sans écho.

## Représentation SQL — choix internes explicites

Choix internes non normatifs, sans extension PG crypto :

- `id` : `BigAutoField` primaire locale technique, explicitement hors des 12 clés logiques, comme patron admission déjà livré.
- 12 colonnes explicites : `tenant_id`, `subject_id`, `command_type`, `idempotency_key`, `content_sha256`, `serializer_version`, `state` dans `IN_PROGRESS/SUCCEEDED/REJECTED`, `result_reference` NULL admissible, `failure_code` NULL admissible, `created_at` / `expires_at` via `_TrustedUtcDateTimeField` existant, `revision` `BigIntegerField >=1`. `CheckConstraint` non-vide, digest regex `^[0-9a-f]{64}$`, révision positive. `UniqueConstraint` atomique sur `(tenant_id, subject_id, command_type, idempotency_key)`. Aucune FK métier. Contraintes SQL non présentées comme preuve complète du canon.
- B02/B13 et Frontière uniquement pour co-transaction, types/rétention et découpage interne. `expires_at`, autorité, horodatages et gouvernance = préconditions du producteur trusted, aucune durée/hold/purge/cohérence inventée.

## Mécanisme exact IN_PROGRESS non engagé et rollback parent

- `idempotent_unit(values)` ouvre `transaction.atomic(using=self._using, savepoint=False)` donc rejoint la transaction appelante sur même alias sans savepoint indépendant. Un atomic imbriqué normal à savepoint ne forcerait pas le rollback parent après exception capturée ; `savepoint=False` évite cette isolation.
- Le producteur fournit explicitement les 12 valeurs initiales, dont IN_PROGRESS et révision 1 ; toute autre initialisation de cette primitive est refusée sans défaut ni substitution et sans modifier le pur général. Insertion transitoire `IN_PROGRESS revision 1` tentée dans un sous-atomic à savepoint isolé seulement pour la race d'unicité connue : duplication concurrente => conflit/rejeu sans casser l'appelant ; toute autre erreur => échec latched + `transaction.set_rollback(True, using)` sur la portée participante.
- Jeton actif exigé pour `finalize_terminal`. `__exit__` : si non finalisé, ou si erreur observée de la primitive, positionne `failed_latched=True` et appelle `set_rollback`, puis lève refus statique. La transaction appelante devient non committable même si l'appelant capture le refus et tente de continuer ; test PG réel l'exige. Seuls `SUCCEEDED/REJECTED` via jeton valide avec CAS réussissent le commit.
- Un rejeu terminal reçoit un jeton de lecture distinct déjà satisfait, is_replay=True, sans insertion ni révision et sans finalisation possible. Une réservation nouvelle reçoit is_replay=False. Le caller de confiance ne réalise ses effets qu'après une réservation nouvelle et les omet sur rejeu.
- Limite : ce lot n'exécute aucun owner. Une exception propriétaire avalée puis finalize externe est inobservable ici. Précondition que le caller propage ses erreurs et participe sur même alias ; garantie limitée aux erreurs observées de la primitive et à la sortie non finalisée. Aucun B10/owner runtime complet annoncé.

## Co-transaction PostgreSQL appelante

- Démontrée par fixtures synthétiques sur même alias : unité appelante `atomic(using)` écrivant un effet propriétaire synthétique et utilisant aussi les vraies primitives protégées/checkpoint/progression runtime existantes puis entrée/sortie `idempotent_unit` + `finalize/replay` ; succès commun committé ensemble, divergence/rollback ensemble. Ne prétend pas un runtime propriétaire complet.

## Migration et câblage

- Migration `0006_bulk_command_idempotency` dépendant de `0005`, `CreateModel` unique, réversible ; forward/reverse 0006 isolé prouvé sans toucher tables existantes.
- `models.py` : import minimal du record pour enregistrement, sans changement de comportement ni de `__all__` existants.

## Limites

Persistance seule : ni exécution propriétaire, ni autorisation, ni provider, ni purge, ni holds, ni politique temporelle, ni outbox, ni URL, ni rétention active. Aucun changement du pur, profils, runtime repository, exports existants. Aucun trigger/dépendance/infrastructure nouvelle.
