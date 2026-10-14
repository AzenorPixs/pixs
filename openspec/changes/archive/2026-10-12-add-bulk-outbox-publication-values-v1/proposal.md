## Why

Le runtime Bulk v1 doit garder en memoire les valeurs logiques `OutboxPublicationV1` avant toute persistance ou publication B11, sans port, ORM, catalogue, autorisation, horloge, allocation ni CAS. Il manque la garde exacte des 12 cles avec capture owned immuable.

## What Changes

- Ajouter `validate_bulk_outbox_publication_values(candidate) -> list[Diagnostic]` et `capture_bulk_outbox_publication_values(candidate) -> tuple[bound | None, list[Diagnostic]]` purs.
- Controler mapping exact 12 cles, types exacts avant valeurs, `str` runtime strictes, `attempt_count >= 0`, `sequence_index/revision >= 1` sans borne superieure, `policy_version` SemVer complete via helper existant, datetimes `timezone.utc` identite.
- N imposer que les couplages fermes : `lease_owner/lease_expires_at` tous deux `None` ou presents, `next_attempt_at` present si `RETRYING`, `published_at` present si `PUBLISHED` ; sans reciproques ni autre coherence etat/champ.
- `PENDING` explicite et compteur `0` restent des valeurs initiales de l appelant, sans defaut, initialisation ni restriction historique ; sans catalogue, bail actif, horloge, comparaison de dates, politique, FK, unicite, allocation, publication, retry, CAS, SQL ni preuve serveur.

## Capabilities

### New Capabilities

Aucune nouvelle capacite normative.

### Modified Capabilities

- events : outillage partiel de B11 deja valide ; exigence `MODIFIED` recopiee verbatim, aucune annexe ou regle ajoutee.

## Impact

Trois fichiers Python nouveaux : `src/pixs/backend/bulk_outbox_publication_values.py`, `tests/unit/test_bulk_outbox_publication_values.py`, `tests/integration/test_bulk_outbox_publication_integration.py`, plus quatre artefacts de change. Aucun ancien code modifie, aucun ORM/migration, provider, worker, publication, route HTTP, dependance, Git ou deploiement. Inventaire actif : `openspec/changes/` contient `archive/` seul. Archive future `--skip-specs`, canon inchange.
