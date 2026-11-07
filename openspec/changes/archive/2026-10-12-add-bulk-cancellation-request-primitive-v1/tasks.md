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

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Preuves » ; « Procédure après preuves des tâches ».

### B30-SL01 — Implémenter `request_cancellation` dans `bulk_runtime_repository.py` avec gardes, verrous, CAS, terminal refusé et seule écriture flag+revision.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Primitive interne », ligne 2 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B30-SL02 — Ajouter tests unitaires `test_bulk_cancellation_request.py` : types hostiles avant I/O, terminaux, CAS valide/stale, flag persisté et invariants conservés.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Primitive interne », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B30-SL03 — Compiler les trois Python avec Python projet `/home/devops/datas/pixs/.venv/bin/python3`.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Primitive interne », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B30-SL04 — Ajouter tests PG isolés `test_bulk_cancellation_request_integration.py` : rollback, CAS, concurrence, persistance flag, checkpoints/progrès/baux inchangés, nettoyage et connexions fermées.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Preuves », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B30-SL05 — Exécuter régressions repository existantes, strict qualifié, UTF-8/LF et absence d'écriture hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Preuves », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B30-SL06 — Vérifier conformité delta B02/B06 verbatim, sans requirement nouveau ni norme reformulée.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Preuves », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
