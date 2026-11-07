# Tâches — Vocabulaire Enum des états de persistance

## 1. Vocabulaire structurel pur

- [x] 1.1 Exécuter les stricts du change et de la spec `data-lifecycle` (exit 0 obligatoire) avant tout code, consigner et contrôler leurs résultats natifs.
- [x] 1.2 Publier `src/pixs/kernel/data_persistence.py` : `PersistenceState(Enum)` standard aux noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` limité à cette classe, sans façade ni `__init__` modifiés ; compiler le fichier, résultat natif contrôlé.
- [x] 1.3 Publier `tests/unit/test_data_persistence_vocabulary.py` : adhésion exacte des quatre noms/valeurs et de leur ordre à la source canonique citée, absence de membre, d'alias ou de `PURGED` ajouté, `__all__` exact, aucune référence au cycle mécanique `lifecycle.state` ; compiler puis exécuter le test.
- [x] 1.4 Publier `tests/integration/test_data_persistence_vocabulary_integration.py` : import en processus frais `-I -B` sous environnement réduit et gardes positives d'effets déjà observées, marqueur fixe, aucun effet observable, aucun chargement mécanique supplémentaire par rapport à la façade `pixs.kernel` existante ; compiler, exécuter, puis exécuter la régression ciblée (kernel purity, façades publiques, vocabulaire voisin).
- [x] 1.5 Exécuter après code les stricts du change et de la spec `data-lifecycle` (exit 0), reconsigner les validations globales et leur qualification limitée, contrôler UTF-8/LF, l'identité octet par octet du bloc requirement du delta et les empreintes des fichiers non concernés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et `STATISTIQUES.md` relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### C71-SL01 — Exécuter les stricts du change et de la spec `data-lifecycle` (exit 0 obligatoire) avant tout code, consigner et contrôler leurs résultats natifs.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Vocabulaire structurel pur », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C71-SL02 — Publier `src/pixs/kernel/data_persistence.py` : `PersistenceState(Enum)` standard aux noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` limité à cette classe, sans façade ni `__init__` modifiés ; compiler le fichier, résultat natif contrôlé.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Vocabulaire structurel pur », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C71-SL03 — Publier `tests/unit/test_data_persistence_vocabulary.py` : adhésion exacte des quatre noms/valeurs et de leur ordre à la source canonique citée, absence de membre, d'alias ou de `PURGED` ajouté, `__all__` exact, aucune référence au cycle mécanique `lifecycle.state` ; compiler puis exécuter le test.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Vocabulaire structurel pur », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C71-SL04 — Publier `tests/integration/test_data_persistence_vocabulary_integration.py` : import en processus frais `-I -B` sous environnement réduit et gardes positives d'effets déjà observées, marqueur fixe, aucun effet observable, aucun chargement mécanique supplémentaire par rapport à la façade `pixs.kernel` existante ; compiler, exécuter, puis exécuter la régression ciblée (kernel purity, façades publiques, vocabulaire voisin).

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Vocabulaire structurel pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C71-SL05 — Exécuter après code les stricts du change et de la spec `data-lifecycle` (exit 0), reconsigner les validations globales et leur qualification limitée, contrôler UTF-8/LF, l'identité octet par octet du bloc requirement du delta et les empreintes des fichiers non concernés.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Vocabulaire structurel pur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
