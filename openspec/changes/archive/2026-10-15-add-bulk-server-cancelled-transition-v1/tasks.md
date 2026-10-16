# Tasks — add-bulk-server-cancelled-transition-v1

Aucune tâche cochée sans preuve observée. Archivage et rapport utilisent des mandats CAB distincts.

- [x] 1.1 Ajouter `src/pixs/backend/bulk_server_cancelled_transition.py` avec la façade interne minimale, import inerte, types exacts, vraie capacité PG, autorité CANCEL courante avant SQL et unique primitive vers CANCELLED.
- [x] 1.2 Ajouter `tests/unit/test_bulk_server_cancelled_transition.py` : import/gardes hostiles sans I/O, composants exacts, alias/vendor, refus d'autorité avant SQL, diagnostics statiques et erreurs inattendues non masquées.
- [x] 1.3 Ajouter `tests/integration/test_bulk_server_cancelled_transition_postgres_integration.py` : inertie ordinaire, PG réel explicite isolé, flag préalable réel, transition état/révision seuls, coopérativité, conservation des champs/engagements, CAS/race, rollback, terminaux, nettoyage et connexions fermées.
- [x] 2.1 Compiler les trois fichiers et exécuter les nouveaux tests ordinaires avec résultats natifs.
- [x] 2.2 Qualifier le PostgreSQL réel sans mocks de la primitive ni tables publiques modifiées, avec finalisation prouvée.
- [x] 2.3 Exécuter les régressions applicables et vérifier B03/B06, UTF-8/LF, empreintes et absence d'écriture hors périmètre.
- [x] 2.4 Vérifier sous exclusion les validations combinées affectées, le strict ciblé et le résultat global exact avant archive, puis relire toutes les preuves.

Après les preuves préarchive : archive unique et synchronisation B06 seules sous décision distincte, publication et libération d'exclusion, rapport STATISTIQUES.md vérifié en phase REPORT, gate individuel, désarmement et libération. Le parent CISMP reprend sa sélection ; aucune coche anticipée de clôture.

Preuves préarchive observées : trois compilations natives exit 0 ; nouveaux tests ordinaires 3/3 ; régressions 45/45 ; PostgreSQL 16.14 réel, 22 propriétés vérifiées et nettoyage/connexions fermées ; combiné 1 951 tests dans 245 modules, zéro échec/skip et 409 empreintes Python identiques ; strict ciblé 1/1 sans issue ; global standard 80/80 exit 0 ; global strict 78/80 exit 1, uniquement quatre WARNING historiques (bulk-operations requirements[6], [10], [13], identity-assurance requirements[4]), zéro ERROR. Le strict global n’est pas déclaré réussi. Chaque opération conserve sa décision CAB et sa permission native once dans le checkpoint du RUN.
