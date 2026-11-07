## 1. Preparation OpenSpec

- [x] 1.1 Relire proposal et design, verifier les deltas canoniques reference-runtime/runtime sans nouvelle norme.
- [x] 1.2 Creer les seuls deltas requis et valider le change en mode strict ; verifier UTF-8/LF et coherence des cadrages.

## 2. Fondation backend

- [x] 2.1 Declarer les seules dependances directes Django==5.2.17 et psycopg==3.3.5 dans pyproject.toml, en preservant Python >=3.11.
- [x] 2.2 Preparer le paquet backend commun et la configuration explicite PIXS_PROFILE pour web/worker/scheduler, sans defaut de role, secret ou base alternative.
- [x] 2.3 Preparer les controles hors base et limites inspectables, sans declarer de services ou persistance operationnels.
- [x] 2.4 Documenter le parcours synthetique et les exclusions ; toute installation isolee reste un mandat distinct.

## 3. Preuves et cloture

- [x] 3.1 Executer les tests dedies unitaires/integration avec configurations synthetiques et garde contre toute connexion PostgreSQL.
- [x] 3.2 Executer les regressions applicables, controles de syntaxe, UTF-8/LF et validation OpenSpec stricte, puis verifier le perimetre.
- [x] 3.3 Verifier les preuves, les criteres, la coherence et la validation CGPT du dossier de cloture avant archivage.

L'archivage est exige apres toutes les taches ci-dessus prouvees et cochees, sous mandat CAB distinct apres controle CGPT ; il ne fait pas partie de la case 3.3.
La production de STATISTIQUES.md est un mandat distinct apres archivage effectif, avec sonde finale et quotas reels ou N/A motives. Aucune case ci-dessus n'est une preuve acquise. Si la session s'arrete a 16h30 Paris, conserver l'etat du premier jalon non prouve sans archivage ni declaration de reussite.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et cloture ».

### C33-SL01 — Relire proposal et design, verifier les deltas canoniques reference-runtime/runtime sans nouvelle norme.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation OpenSpec », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL02 — Creer les seuls deltas requis et valider le change en mode strict ; verifier UTF-8/LF et coherence des cadrages.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation OpenSpec », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL03 — Declarer les seules dependances directes Django==5.2.17 et psycopg==3.3.5 dans pyproject.toml, en preservant Python >=3.11.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Fondation backend », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL04 — Preparer le paquet backend commun et la configuration explicite PIXS_PROFILE pour web/worker/scheduler, sans defaut de role, secret ou base alternative.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Fondation backend », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL05 — Preparer les controles hors base et limites inspectables, sans declarer de services ou persistance operationnels.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Fondation backend », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL06 — Documenter le parcours synthetique et les exclusions ; toute installation isolee reste un mandat distinct.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Fondation backend », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL07 — Executer les tests dedies unitaires/integration avec configurations synthetiques et garde contre toute connexion PostgreSQL.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et cloture », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL08 — Executer les regressions applicables, controles de syntaxe, UTF-8/LF et validation OpenSpec stricte, puis verifier le perimetre.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et cloture », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C33-SL09 — Verifier les preuves, les criteres, la coherence et la validation CGPT du dossier de cloture avant archivage.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et cloture », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
