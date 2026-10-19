## 1. Primitive interne
- [x] 1.1 Implémenter `request_cancellation` dans `bulk_runtime_repository.py` avec gardes, verrous, CAS, terminal refusé et seule écriture flag+revision.
- [x] 1.2 Ajouter tests unitaires `test_bulk_cancellation_request.py` : types hostiles avant I/O, terminaux, CAS valide/stale, flag persisté et invariants conservés.
- [x] 1.3 Compiler les trois Python avec Python projet `/home/devops/datas/pixs/.venv/bin/python3`.

## 2. Preuves
- [x] 2.1 Ajouter tests PG isolés `test_bulk_cancellation_request_integration.py` : rollback, CAS, concurrence, persistance flag, checkpoints/progrès/baux inchangés, nettoyage et connexions fermées.
- [x] 2.2 Exécuter régressions repository existantes, strict qualifié, UTF-8/LF et absence d'écriture hors périmètre.
- [x] 2.3 Vérifier conformité delta B02/B06 verbatim, sans requirement nouveau ni norme reformulée.

## Procédure après preuves des tâches
Cocher les tâches uniquement après leurs preuves. Archiver une seule fois avec --skip-specs, publier STATISTIQUES.md sous mandat distinct, vérifier ses six sections et totaux, puis revenir à SÉLECTION sans fin globale.
