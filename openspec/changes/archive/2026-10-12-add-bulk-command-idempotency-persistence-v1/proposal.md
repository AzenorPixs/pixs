## Why

Le canon `interactions` B10 exige la déduplication durable des Commands par clé canonique `(tenant_id, subject_id, command_type, idempotency_key)` avec octets canoniques du sérialiseur public versionné du propriétaire, immutabilité du contenu initial, même transaction PostgreSQL pour mutation propriétaire / résultat d'idempotence / progression / checkpoint, rétention couvrant fenêtre de rejeu et holds, et non-engagement de `IN_PROGRESS`. Le schéma logique `CommandIdempotencyV1` à 12 clés existe et le pur `bulk_command_idempotency_values.py` valide/capture sans persister. Aucune persistance interne ne conserve ces 12 valeurs, ni l'unicité atomique de la clé complète, ni le rejeu stable, ni le CAS par révision.

## What Changes

- Ajouter une persistance interne `BulkCommandIdempotency` en 6 sources seules : `bulk_command_idempotency_record.py`, `bulk_command_idempotency_repository.py`, import minimal dans `models.py`, migration réversible `0006_bulk_command_idempotency`, `tests/unit/test_bulk_command_idempotency_persistence.py`, `tests/integration/test_bulk_command_idempotency_persistence_integration.py`. Aucune autre source.
- Réutiliser strictement `validate_bulk_command_idempotency_values` / `capture_bulk_command_idempotency_values` existants sans les modifier ni redéfinir `_CommandIdempotencyBound`. Digest, serializer, contextes et horodatages proviennent du producteur serveur de confiance ; aucun sérialiseur global inventé. Jeton privé et signatures internes sont choix de mise en oeuvre, aucune clé logique/wire ajoutée.
- Aucune voie API publique de stockage n'engage `IN_PROGRESS`. Insertion transitoire privée uniquement à l'intérieur de `idempotent_unit` contrôlé. `get_entry` et `replay` readonly possibles. `finalize_terminal` exige le jeton de réservation exact, actif, dans le même contexte thread/alias ; seuls `SUCCEEDED/REJECTED` via ce jeton sont committables.
- Portée participante `transaction.atomic(using, savepoint=False)` + garde d'échec latched sur le jeton + `set_rollback` lorsque approprié. Savepoint séparé seulement pour l'INSERT unique de race connue si nécessaire, afin de convertir la race en conflit/rejeu sans casser la transaction appelante. Toute sortie non finalisée ou erreur observée de la primitive rend la transaction appelante non committable, même si l'appelant capture le refus et essaie de continuer ; test PG réel exigé.
- Rejeu seulement pour même clé complète avec digest ET serializer identiques, terminal stable sans nouvelle entrée ni révision ; divergence = même clé avec digest/version différents, PAS rejet d'une nouvelle clé distincte. `replay` n'est ni finalisable ni modifiable. Valeurs initiales immuables, CAS stale rejeté sans retry implicite.
- Limite documentée : une exception propriétaire arbitraire avalée puis finalize par code externe est inobservable sans exécuter ce code. Ce lot n'exécute aucun owner ; précondition que le caller propage ses erreurs techniques et participe correctement ; garantie seulement sur erreurs observées de la primitive et sortie non finalisée. Ne pas annoncer B10/owner runtime complet.
- Tous 12 champs explicites ; PK locale technique comme admission ; `save` standard sans preuve workflow ; rétention/autorité/horodatages/gouvernance préconditions du producteur trusted, aucune durée/hold/purge/cohérence inventée. Aucun trigger/dépendance/infrastructure nouvelle, aucune modification du pur, profils, runtime repository ou `__all__` existants.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- interactions : outillage partiel de B10 limité à la persistance interne des 12 valeurs déjà validées et primitives transactionnelles ; requirement B10 et ses 2 scénarios recopiés strictement verbatim, sans recopier ni modifier clauses/annexes ; le canon interactions fait autorité.

## Impact

Quatre artefacts au début uniquement, puis après précode validé : deux modules backend dédiés, import minimal `models.py`, migration réversible `0006`, test unitaire pur unittest, test d'intégration PG synthétique en schéma privé avec forward/reverse 0006 isolé, unicité/race, CAS, replay stable/divergent, rollback technique, fermeture sans finalize, co-transaction synthétique. Aucune route HTTP, worker, publisher, transport, PA/PZT, dépendance, secret, Git ou infra. Python >=3.12, stdlib + Django + diagnostics existants. Archive unique `--skip-specs` prévue, canon inchangé.
