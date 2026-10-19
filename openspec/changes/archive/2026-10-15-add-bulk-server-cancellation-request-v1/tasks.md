# Tasks — add-bulk-server-cancellation-request-v1

Aucune tâche cochée avant preuve observée. L'archivage nécessite une décision CAB distincte.

- [x] 1.1 Implémenter le module nouveau `src/pixs/backend/bulk_server_cancellation.py` avec `request_bulk_cancellation`, types exacts, vrais composants et capacité PG, autorité `CANCEL` actuelle sur la cible avant SQL Bulk, primitive seule et diagnostics statiques. Preuve attendue : fichier nouveau relu, import inerte, refus hostiles sans I/O.
- [x] 1.2 Ajouter les unitaires nouveaux `tests/unit/test_bulk_server_cancellation.py` pour import inerte, hostiles, refus et absence d'I/O avant autorisation, contrat de retour. Preuve attendue : test nouveau exécuté avec résultat natif.
- [x] 1.3 Ajouter le harnais PG nouveau `tests/integration/test_bulk_server_cancellation_postgres_integration.py` réel isolé pour effet flag et révision seuls, CAS, terminaux, rollback, race, absence de modification de progression, échéance, checkpoint, Job et schedule, blocage de l'unité suivante. Preuve attendue : sortie PG réelle avec nettoyage prouvé.
- [x] 2.1 Compiler les trois fichiers et exécuter les unitaires avec résultats natifs. Preuve attendue : `py_compile` et sortie de test observées.
- [x] 2.2 Exécuter le PG réel explicite avec nettoyage, connexions fermées et tables publiques inchangées. Preuve attendue : outcome réel et finalisation prouvée.
- [x] 2.3 Vérifier régressions ciblées, conformité B03/B06, UTF-8/LF, empreintes et aucune écriture hors périmètre. Preuve attendue : contrôles relus sans écart.
- [x] 2.4 Vérifier sous exclusion d’intégration les validations combinées affectées, le strict ciblé et le résultat global exact avant archivage. Preuve attendue : résultats natifs et contrôles préarchive disponibles.

Clôture après les preuves préarchive : archivage unique sous décision CAB distincte, rapport `STATISTIQUES.md` distinct vérifié, publication, gate individuel, désarmement et libération. Ces opérations suivent la checklist et ne nécessitent aucune coche avant leur propre exécution.

Périmètre : trois fichiers nouveaux seuls et artefacts de ce change uniquement, aucun code existant à modifier.
