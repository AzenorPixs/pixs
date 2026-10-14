# Tasks — add-bulk-inbox-receipt-persistence-v1

- [x] 1. Préparer les quatre artefacts cohérents, Why/What Changes requis, delta MODIFIED B11 verbatim sans norme nouvelle ; strict précode sans issue.
- [x] 2. Implémenter record/repository, import minimal models.py et migration0008 dépendant de0007 réversible : huit clés exactes, PK technique hors huit, unique consumer_reference/event_id, insert-only/alias/atomic, savepoint INSERT puis lecture, Duplicate/Divergence et rollback propriétaire capturé.
- [x] 3. Implémenter unittest offline : vrais imports sous gardes, types hostiles avant comportement/I/O, sans écho, capture et exports owned/frozen, save/full_clean exclude/déféré, métadonnées/migration sans DB ; aucune preuve SQL par mock miroir.
- [x] 4. Implémenter harness PostgreSQL isolé : clé composée/version/sha/consumer indépendant, co-transaction avec effet synthétique et JobRecord existant, refus capturé rollback, race deux bloqués/un gagnant/connexions fermées, visibilité inflight non ack, forward/reverse0008 seule/public et dix tables stables/cleanup strict.
- [x] 5. Compiler les six sources, exécuter unittest et PG réels autorisés puis régressions pertinentes avec outils DEVOPS ; strict ciblé sans issue et global comparé aux trois WARNING historiques exacts.
- [x] 6. Accepter sur preuves : huit clés sans ajout/default, UTF-8/LF, fichiers ciblés seuls, canon/cadrages/purs/runtime/CommandIdempotency/EventEnvelope préservés, aucune autorité/receiver/provider ni B11 global déclaré.

Après preuve des six tâches, les cocher ; archivage unique --skip-specs puis STATISTIQUES distinct vérifié. Ne pas faire du gate terminal avant archive/rapport une tâche circulaire.
