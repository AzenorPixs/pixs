# Tâches — Vocabulaire Enum des opérations de demande relative aux données

## 1. Vocabulaire structurel pur

- [x] 1.1 Valider strictement le change et la spec `data-governance` (exit 0 obligatoire) avant tout code, consigner les sorties et codes réels des validations globales `--specs --strict --json --report findings` et `--all --strict --json --report findings` selon la règle de qualification de design.md, avec résultat natif contrôlé.
- [x] 1.2 Publier `src/pixs/kernel/data_subject_operations.py` : `DataSubjectOperation(Enum)` aux cinq noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` limité à la classe, sans façade ni `__init__` modifiés.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_subject_operations_vocabulary.py` : adhésion exacte des cinq noms/valeurs et de leur ordre via `__members__.items()`, absence de membre ou d'alias supplémentaire, `__all__` exact ; pas de test de garanties stdlib.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_subject_operations_vocabulary_integration.py` : import en processus frais `-I -B` sous environnement réduit et gardes finies d'effets réutilisées, contrôles positifs avant remise à zéro, couples et `__all__` vérifiés sous gardes, marqueur fixe, quatre assertions finales hors du `with`, sans nouvelle dépendance.
- [x] 1.5 Exécuter les compilations ciblées des trois fichiers et la régression minimale définie dans design.md ; contrôler les résultats natifs, UTF-8/LF et les empreintes des fichiers non concernés.
- [x] 1.6 Exécuter après code les stricts du change et de la spec `data-governance` (exit 0), reconsigner les validations globales et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
