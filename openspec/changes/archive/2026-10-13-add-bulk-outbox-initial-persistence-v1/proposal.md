# Proposal add-bulk-outbox-initial-persistence-v1

## Why

Le runtime Bulk v1 exige une persistance initiale OutboxPublicationV1 verrouillee : un enregistrement PENDING/attempt 0 explicite, lie 1-1 a une enveloppe persistante immuable, y compris nouvellement inseree dans la transaction proprietaire courante, avec sequence allouee atomiquement par scope prive derive, sans publication ni transition. Ce socle prepare la file initiale ordonnee ; la persistance Inbox deja livree reste distincte. Aucune garantie globale de publication n est deduite de ces primitives. Ce change MUST rester strictement initial et MUST NOT introduire emit, CAS, horloge, bail, API publique ou gouvernance concrete.

## What Changes

Le change MUST ajouter uniquement la persistance initiale : record 13 colonnes physiques (12 logiques canoniques + scope_prive derive) avec FK event_id unique vers BulkEventEnvelopeRecord immuable, compteur prive 2 colonnes par scope, migration 0011 apres 0010 (13 tables preexistantes intactes, 15 finales), wiring models sans toucher Envelope, repository owner-atomique avec allocation runtime meme transaction, getter capture pure figee sans publication, tests unitaires gardes et integration PG isole. Tous champs source, y compris nullable/state/attempt/revision/policy, MUST rester explicites obligatoires sans defaut Python ; toute revision positive fournie MUST etre conservee, aucun 1 impose ; PENDING/attempt0 canoniques MUST etre valides explicitement.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- events : persistance initiale OutboxPublicationV1 PENDING/attempt0, FK unique, sequence runtime par scope, get pur ; sans publisher/transition/CAS.

Impacts limites aux 6 sources : src/pixs/backend/bulk_outbox_publication_record.py, src/pixs/backend/bulk_outbox_publication_repository.py, src/pixs/backend/migrations/0011_bulk_outbox_publication.py, src/pixs/backend/models.py, tests/unit/test_bulk_outbox_initial_persistence.py, tests/integration/test_bulk_outbox_initial_persistence_integration.py.
