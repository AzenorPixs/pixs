# Tâches — Vocabulaire Enum des états de persistance des données

## 1. Vocabulaire structurel pur

- [x] 1.1 Valider strictement le change et la spec `data-lifecycle` (exit 0 obligatoire) avant tout code, consigner les sorties et codes réels des validations globales `--specs --strict --json --report findings` et `--all --strict --json --report findings` selon la règle de qualification de design.md, avec résultat natif contrôlé et code CLI 1 non converti en succès.
- [x] 1.2 Publier `src/pixs/kernel/data_persistence_states.py` : `DataPersistenceState(Enum)` aux quatre noms/valeurs canoniques dans l'ordre de la source (`ACTIVE`, `ARCHIVED`, `SOFT_DELETED`, `PURGE_PENDING`), sans `PURGED`, docstring de frontière, `__all__` limité à la classe, sans façade ni `__init__` modifiés.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_persistence_states.py` : adhésion exacte des quatre noms/valeurs et de leur ordre via `__members__.items()`, absence de membre ou d'alias supplémentaire, `__all__` exact ; pas de test des garanties de la stdlib.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_persistence_states_integration.py` : import en processus frais `-I -B` sous environnement réduit et gardes finies d'effets réutilisées, contrôles positifs avant remise à zéro, couples et `__all__` vérifiés sous gardes, marqueur `DATA_PERSISTENCE_STATES_SAFE_INTEGRATION_OK` seul sur stdout, quatre assertions finales hors du `with`, sans nouvelle dépendance.
- [x] 1.5 Exécuter les compilations ciblées des trois fichiers et la régression minimale définie dans design.md ; contrôler les résultats natifs, UTF-8/LF et les empreintes des fichiers non concernés.
- [x] 1.6 Exécuter après code les stricts du change et de la spec `data-lifecycle` (exit 0), reconsigner les validations globales et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
