## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et perimetre CGPT.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Classificateur pur

- [x] 2.1 Creer src/pixs/backend/health_classifier.py seul, API classify_health exacte, quatre types separes, PG obligatoire, limite interne 256, refus ValueError("Invalid health snapshot") from None, sans IO ni import Django ni execution de sonde.
- [x] 2.2 Creer tests/unit/test_health_classifier.py avec objets doubles, matrices quatre types, PG obligatoire, optionnels, combos startup/alive, types et repr hostile, grand tuple 257 et objet hostile en premier element, sans reseau ni PG reel ni assertion de temps.
- [x] 2.3 Creer tests/integration/test_health_classifier_integration.py sans reseau, subprocess frais avec gardes IO/sockets/SQL et sans import Django, plus append README seul.

## 3. Preuves

- [x] 3.1 Reussir tests unitaires puis integration sans reseau sur l'executable DEVOPS actuel sous mandats distincts, determinisme et gardes prouves sans fake hard deadline.
- [x] 3.2 Verifier AST 3.11 UTF-8 LF, perimetre 3 sources plus append seul, comptages baseline CGPT exacts, diagnostics sans valeur brute, strict apres preuves, matrice et conformite finale avant tout cochage.
- [x] 3.3 Prouver criteres precedents et delta normatif MOTAMOT sans nouveau scenario ; archivage et statistiques distincts apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves ».

### C47-SL01 — Prouver perimetre, absence de change actif et perimetre CGPT.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL02 — Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL03 — Creer src/pixs/backend/health_classifier.py seul, API classify_health exacte, quatre types separes, PG obligatoire, limite interne 256, refus ValueError("Invalid health snapshot") from None, sans IO ni import Django ni execution de sonde.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Classificateur pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL04 — Creer tests/unit/test_health_classifier.py avec objets doubles, matrices quatre types, PG obligatoire, optionnels, combos startup/alive, types et repr hostile, grand tuple 257 et objet hostile en premier element, sans reseau ni PG reel ni assertion de temps.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Classificateur pur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL05 — Creer tests/integration/test_health_classifier_integration.py sans reseau, subprocess frais avec gardes IO/sockets/SQL et sans import Django, plus append README seul.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Classificateur pur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL06 — Reussir tests unitaires puis integration sans reseau sur l'executable DEVOPS actuel sous mandats distincts, determinisme et gardes prouves sans fake hard deadline.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL07 — Verifier AST 3.11 UTF-8 LF, perimetre 3 sources plus append seul, comptages baseline CGPT exacts, diagnostics sans valeur brute, strict apres preuves, matrice et conformite finale avant tout cochage.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C47-SL08 — Prouver criteres precedents et delta normatif MOTAMOT sans nouveau scenario ; archivage et statistiques distincts apres controle.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
