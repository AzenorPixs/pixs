# Tasks add-bulk-outbox-initial-persistence-v1

- [x] 1. Artefacts stricts pre-code : proposal/design/tasks/delta ci-dessus relus, 12 noms et 13+2 colonnes figes, 6 fichiers cibles seuls, aucune ecriture hors perimetre.
- [x] 2. Production 4 fichiers : record 13 colonnes + counter interne 2 colonnes meme module + repository owner-atomique (from_values 12, allocation runtime, savepoint 23505 PK scope, rowlock exact, rollback propage) + migration 0011 apres 0010 + wiring models sans Envelope change.
- [x] 3. Tests unitaires gardes : 12 mapping exact, 11 source obligatoires sans defaut, revision positive conservee, PENDING/attempt0 explicites, types stricts/capacites, couplages lease/RETRYING/PUBLISHED, hostile bool/eq/hash/str, frozen owned, catalogue failure tuple/frozenset.
- [x] 4. Integration PG isole : 2 threads meme scope unique vs scopes independants, owner rollback join, type caps, get initial capture pure, FK event unique immuable, 15 tables finales, reversal 0011 seule, public readiness sans fake publish, cleanup conns, UTF-8/LF.
- [x] 5. Compilation et regressions 6 sources : py_compile, suites unitaires concernees, non-regression Envelope/runtime/purs, strict cible precode/final sans issue, global compare aux trois WARNING historiques exacts sans nouvelle issue, norme preservee, aucun secret.
- [x] 6. Acceptance scope : 12/13/2 colonnes, FK unique, sequence runtime seule, PENDING/attempt0, exclusions publisher/CAS/clock/reset respectees, UTF-8/LF, seuls fichiers attendus modifies et autres sources/canon preserves.

Apres preuves des six taches : coches sous mandat distinct, archivage unique --skip-specs puis STATISTIQUES.md sous mandat distinct, hors de ces six taches et sans condition circulaire.
