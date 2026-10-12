# Tâches — Vocabulaire commun des stratégies de suppression

## 1. Vocabulaire structurel pur

- [x] 1.1 Valider strictement le change et la spec `data-lifecycle` (exit 0) avant code ; consigner sorties et codes natifs des globaux `--specs` et `--all`, avec la qualification limitée de design.md sans conversion du code CLI 1.
- [x] 1.2 Publier `src/pixs/kernel/data_deletion_strategies.py` : Enum standard à quatre noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` unique, aucun alias, défaut, effet ou réexport.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_deletion_strategies.py` : adhésion exacte des quatre noms/valeurs/ordre et export unique, sans test des garanties de la stdlib.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_deletion_strategies_integration.py` : processus frais `-I -B` sous environnement réduit et gardes réutilisées, contrôles positifs avant remise à zéro, tuple/export sous gardes, marqueur unique et assertions finales hors du `with`, sans nouvelle dépendance.
- [x] 1.5 Exécuter les trois compilations ciblées et la régression minimale de design.md ; contrôler résultats natifs, UTF-8/LF et empreintes hors périmètre.
- [x] 1.6 Valider après code les stricts ciblés (exit 0) et reconsigner les globaux et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ou de statistiques : archivage et `STATISTIQUES.md` exigent décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
