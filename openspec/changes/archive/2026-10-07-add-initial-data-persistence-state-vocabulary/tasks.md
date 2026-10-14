# Tâches — Vocabulaire Enum des états de persistance

## 1. Vocabulaire structurel pur

- [x] 1.1 Exécuter les stricts du change et de la spec `data-lifecycle` (exit 0 obligatoire) avant tout code, consigner et contrôler leurs résultats natifs.
- [x] 1.2 Publier `src/pixs/kernel/data_persistence.py` : `PersistenceState(Enum)` standard aux noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` limité à cette classe, sans façade ni `__init__` modifiés ; compiler le fichier, résultat natif contrôlé.
- [x] 1.3 Publier `tests/unit/test_data_persistence_vocabulary.py` : adhésion exacte des quatre noms/valeurs et de leur ordre à la source canonique citée, absence de membre, d'alias ou de `PURGED` ajouté, `__all__` exact, aucune référence au cycle mécanique `lifecycle.state` ; compiler puis exécuter le test.
- [x] 1.4 Publier `tests/integration/test_data_persistence_vocabulary_integration.py` : import en processus frais `-I -B` sous environnement réduit et gardes positives d'effets déjà observées, marqueur fixe, aucun effet observable, aucun chargement mécanique supplémentaire par rapport à la façade `pixs.kernel` existante ; compiler, exécuter, puis exécuter la régression ciblée (kernel purity, façades publiques, vocabulaire voisin).
- [x] 1.5 Exécuter après code les stricts du change et de la spec `data-lifecycle` (exit 0), reconsigner les validations globales et leur qualification limitée, contrôler UTF-8/LF, l'identité octet par octet du bloc requirement du delta et les empreintes des fichiers non concernés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
