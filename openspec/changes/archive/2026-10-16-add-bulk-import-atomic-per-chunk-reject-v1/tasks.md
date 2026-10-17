# Tasks — add-bulk-import-atomic-per-chunk-reject-v1

Aucune tâche cochée sans preuve. Les déclarations serveur et les tests doivent démontrer un chemin positif, sans inventer de garantie à partir de méthodes présentes.

- [x] 1.1 Implémenter la participation PostgreSQL propriétaire explicite et la façade IMPORT ATOMIC_PER_CHUNK/REJECT, avec validation complète avant APPLY, gardes actuelles et engagement atomique par chunk.
- [x] 1.2 Ajouter les tests unitaires d’import inerte, types hostiles, capacités exactes, refus avant I/O, limites, diagnostics statiques et erreurs inattendues non masquées.
- [x] 1.3 Ajouter le test ordinaire inerte et la qualification PostgreSQL réelle isolée : mutation/idempotence/progression/checkpoint/outbox requis same-tx, rollback, CAS, baux, reprise/rejou, annulation/échéances, nettoyage et connexions fermées.
- [x] 2.1 Compiler tous les fichiers Python autorisés et exécuter les tests ordinaires ciblés avec sorties natives.
- [x] 2.2 Qualifier PostgreSQL réel sans mock de la primitive transactionnelle ni modification des tables publiques, avec chemin positif et finalisation prouvés.
- [x] 2.3 Exécuter les régressions affectées, notamment VALIDATE_ONLY et les gardes runtime/annulation/idempotence/outbox ; vérifier les empreintes, UTF-8/LF, conformité documentaire et absence d’écriture hors périmètre.
- [x] 2.4 Obtenir l’exclusion, valider la base combinée et le strict ciblé/global avec résultats exacts, puis relire toutes les preuves avant les coches et l’archive.

Après les preuves préarchive : archive unique et synchronisation B07 seules sous mandat distinct, contrôle postarchive et publication réelle, libération d’exclusion, rapport STATISTIQUES.md distinct vérifié en phase REPORT, gate individuel, désarmement et libération. Le parent CISMP revient à SÉLECTION ; ces opérations ne sont pas cochées par anticipation.
