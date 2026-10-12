# Tâches — Vocabulaire Enum des classifications de gouvernance des données

## 1. Vocabulaire structurel pur

- [x] 1.1 Exécuter les stricts du change et de la spec `data-governance` (exit 0 obligatoire) avant tout code, consigner les sorties et codes réels des validations globales `--specs --strict` et `--all --strict --json --report findings` selon la règle de qualification de design.md, avec résultat natif contrôlé.
- [x] 1.2 Publier `src/pixs/kernel/data_governance.py` : `ConfidentialityLevel` et `PersonalDataLevel`, Enum standards aux noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` limité aux deux classes, sans façade ni `__init__` modifiés.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_governance_vocabulary.py` : adhésion exacte des sept noms/valeurs et de leur ordre à la source canonique citée, absence de membre ou d'alias supplémentaire, `__all__` exact.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_governance_vocabulary_integration.py` : import en processus frais `-I -B` sous environnement réduit et gardes finies d'effets réutilisées, marqueur fixe, aucun effet observable, sans nouvelle dépendance.
- [x] 1.5 Exécuter les compilations ciblées des trois fichiers et la régression kernel/gouvernance pertinente définie dans design.md ; contrôler les résultats natifs, UTF-8/LF et les empreintes des fichiers non concernés.
- [x] 1.6 Exécuter après code les stricts du change et de la spec `data-governance` (exit 0), reconsigner les validations globales et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
