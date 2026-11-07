# Tâches — Vocabulaire commun des stratégies de suppression

## 1. Vocabulaire structurel pur

- [x] 1.1 Valider strictement le change et la spec `data-lifecycle` (exit 0) avant code ; consigner sorties et codes natifs des globaux `--specs` et `--all`, avec la qualification limitée de design.md sans conversion du code CLI 1.
- [x] 1.2 Publier `src/pixs/kernel/data_deletion_strategies.py` : Enum standard à quatre noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` unique, aucun alias, défaut, effet ou réexport.
- [x] 1.3 Publier et exécuter `tests/unit/test_data_deletion_strategies.py` : adhésion exacte des quatre noms/valeurs/ordre et export unique, sans test des garanties de la stdlib.
- [x] 1.4 Publier et exécuter `tests/integration/test_data_deletion_strategies_integration.py` : processus frais `-I -B` sous environnement réduit et gardes réutilisées, contrôles positifs avant remise à zéro, tuple/export sous gardes, marqueur unique et assertions finales hors du `with`, sans nouvelle dépendance.
- [x] 1.5 Exécuter les trois compilations ciblées et la régression minimale de design.md ; contrôler résultats natifs, UTF-8/LF et empreintes hors périmètre.
- [x] 1.6 Valider après code les stricts ciblés (exit 0) et reconsigner les globaux et leur qualification limitée, résultats natifs contrôlés.

Aucune tâche d'archivage ou de statistiques : archivage et `STATISTIQUES.md` exigent décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### C69-SL01 — Valider strictement le change et la spec `data-lifecycle` (exit 0) avant code ; consigner sorties et codes natifs des globaux `--specs` et `--all`, avec la qualification limitée de design.md sans conversion du code CLI 1.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Vocabulaire structurel pur », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C69-SL02 — Publier `src/pixs/kernel/data_deletion_strategies.py` : Enum standard à quatre noms/valeurs canoniques dans l'ordre de la source, docstring de frontière, `__all__` unique, aucun alias, défaut, effet ou réexport.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Vocabulaire structurel pur », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C69-SL03 — Publier et exécuter `tests/unit/test_data_deletion_strategies.py` : adhésion exacte des quatre noms/valeurs/ordre et export unique, sans test des garanties de la stdlib.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Vocabulaire structurel pur », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C69-SL04 — Publier et exécuter `tests/integration/test_data_deletion_strategies_integration.py` : processus frais `-I -B` sous environnement réduit et gardes réutilisées, contrôles positifs avant remise à zéro, tuple/export sous gardes, marqueur unique et assertions finales hors du `with`, sans nouvelle dépendance.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Vocabulaire structurel pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C69-SL05 — Exécuter les trois compilations ciblées et la régression minimale de design.md ; contrôler résultats natifs, UTF-8/LF et empreintes hors périmètre.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Vocabulaire structurel pur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C69-SL06 — Valider après code les stricts ciblés (exit 0) et reconsigner les globaux et leur qualification limitée, résultats natifs contrôlés.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Vocabulaire structurel pur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
