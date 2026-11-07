# Tasks — add-p0-source-filter-plan

## 1. Moteur commun sans changement public

- [x] 1.1 Extraire `_authorize_detailed` dans `decision.py`, `authorize` enveloppe à appel unique, mêmes `Decision`/comportements/audit — preuve : suites PDP existantes 0 échec + revue diff borné
- [x] 1.2 Créer `src/pixs/core/authz/filter_plan.py` : FilterConfig/Lot/Plan frozen, `FilterPlanError`, `plan_filter` à helper unique, enveloppe/limite/horloge/snapshot figés — preuve : tests unitaires
- [x] 1.3 Étendre `__init__.py` : exports bornés seuls — preuve : import public

## 2. Tests

- [x] 2.1 `tests/unit/test_filter_plan.py` : 9 scénarios + bornes + immuabilité — preuve : suite verte
- [x] 2.2 `tests/integration/test_filter_plan_audit.py` : doubles mémoire, sans persistance — preuve : suite verte
- [x] 2.3 Matrice : régression PDP + partial-unknown-after-ALLOW + port-latefail + audit-failed + cost-overflow, tous fermés sans ID — preuve : cas dédiés verts
- [x] 2.4 Suites complètes unit + intégration via chemins DEVOPS — preuve : exits 0

## 3. Validations

- [x] 3.1 AST mémoire, UTF-8/LF ciblés — preuve : contrôles
- [x] 3.2 OpenSpec strict via exécutable DEVOPS — preuve : 0 échec
- [x] 3.3 Revue specs/cadrages/hors périmètre — preuve : rapport

Limites : PEP, PostgreSQL, filtrage exécuté, caches, audit durable, providers, frontend, dépendances nouvelles et P0 global hors périmètre.

## Preuves

- Seul le profil préparatoire `source-filter-plan-v1` est prouvé ; les exigences générales authorization/PEP/filtrage source/audit durable RESTENT non implémentées et ne sont jamais présentées comme couvertes globalement.
- Ciblés : 33 unit OK, 9 intégration OK ; globaux : 349 unit OK, 112 intégration OK ; AST 5, UTF-8/LF 12, OpenSpec 77/0 strict code 0.
- Rapports : msg_0ef28cf43001jU0v2W6GbIhhrJ, msg_0ef27f63d001PQWPWs4vdNplp8.
- Exclusions maintenues.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Validations » ; « Preuves ».

### C27-SL01 — Extraire `_authorize_detailed` dans `decision.py`, `authorize` enveloppe à appel unique, mêmes `Decision`/comportements/audit — preuve : suites PDP existantes 0 échec + revue diff borné

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Moteur commun sans changement public », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL02 — Créer `src/pixs/core/authz/filter_plan.py` : FilterConfig/Lot/Plan frozen, `FilterPlanError`, `plan_filter` à helper unique, enveloppe/limite/horloge/snapshot figés — preuve : tests unitaires

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Moteur commun sans changement public », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL03 — Étendre `__init__.py` : exports bornés seuls — preuve : import public

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Moteur commun sans changement public », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL04 — `tests/unit/test_filter_plan.py` : 9 scénarios + bornes + immuabilité — preuve : suite verte

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Tests », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL05 — `tests/integration/test_filter_plan_audit.py` : doubles mémoire, sans persistance — preuve : suite verte

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Tests », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL06 — Matrice : régression PDP + partial-unknown-after-ALLOW + port-latefail + audit-failed + cost-overflow, tous fermés sans ID — preuve : cas dédiés verts

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Tests », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL07 — Suites complètes unit + intégration via chemins DEVOPS — preuve : exits 0

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL08 — AST mémoire, UTF-8/LF ciblés — preuve : contrôles

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Validations », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL09 — OpenSpec strict via exécutable DEVOPS — preuve : 0 échec

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Validations », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C27-SL10 — Revue specs/cadrages/hors périmètre — preuve : rapport

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Validations », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
