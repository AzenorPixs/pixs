# Tasks

## Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif, baseline et collecte initiale.
- [x] 1.2 Créer les cinq artefacts autorisés, UTF-8/LF et validation OpenSpec stricte avant code.

## Implémentation minimale

- [x] 2.1 Étendre seulement src/pixs/kernel/feature_flags.py : modèle frozen à huit champs requis sans défaut, validateur structurel exact, helpers réutilisés, refus déterministe sans écho ; conserver R1 et ne pas introduire de runtime.
- [x] 2.2 Créer tests/unit/test_feature_flag_assignments.py : huit champs, valeurs, UTC/fenêtres, métadonnées opaques, conteneurs/éléments hostiles, aucune exécution de callback, ordre et diagnostics.
- [x] 2.3 Créer tests/integration/test_feature_flag_assignments_integration.py : import enfant frais sous gardes I/O causales, construction/validation témoin et refus hostile sans effet.

## Preuves

- [x] 3.1 Vérifier syntaxe minimum 3.11 et compilation des trois fichiers sous l'interpréteur DEVOPS.
- [x] 3.2 Réussir les deux suites nouvelles et les deux suites R1 existantes.
- [x] 3.3 Vérifier relecture exacte, conservation des éléments R1, sources hors périmètre, UTF-8/LF et delta R4 MOTAMOT ; expliciter les garanties non livrées.
- [x] 3.4 Réussir OpenSpec strict après les preuves avant tout cochage ; cocher uniquement les tâches réellement prouvées sous mandat distinct.

Archive et STATISTIQUES constituent deux opérations distinctes ultérieures après contrôle CGPT ; le parent CISMP reste OPEN jusqu'à sa clôture conforme.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves ».

### O43-SL01 — Prouver périmètre CGPT, absence de change actif, baseline et collecte initiale.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL02 — Créer les cinq artefacts autorisés, UTF-8/LF et validation OpenSpec stricte avant code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « Préparation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL03 — Étendre seulement src/pixs/kernel/feature_flags.py : modèle frozen à huit champs requis sans défaut, validateur structurel exact, helpers réutilisés, refus déterministe sans écho ; conserver R1 et ne pas introduire de runtime.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « Implémentation minimale », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL04 — Créer tests/unit/test_feature_flag_assignments.py : huit champs, valeurs, UTC/fenêtres, métadonnées opaques, conteneurs/éléments hostiles, aucune exécution de callback, ordre et diagnostics.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « Implémentation minimale », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL05 — Créer tests/integration/test_feature_flag_assignments_integration.py : import enfant frais sous gardes I/O causales, construction/validation témoin et refus hostile sans effet.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « Implémentation minimale », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL06 — Vérifier syntaxe minimum 3.11 et compilation des trois fichiers sous l'interpréteur DEVOPS.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « Preuves », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL07 — Réussir les deux suites nouvelles et les deux suites R1 existantes.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « Preuves », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL08 — Vérifier relecture exacte, conservation des éléments R1, sources hors périmètre, UTF-8/LF et delta R4 MOTAMOT ; expliciter les garanties non livrées.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « Preuves », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O43-SL09 — Réussir OpenSpec strict après les preuves avant tout cochage ; cocher uniquement les tâches réellement prouvées sous mandat distinct.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « Preuves », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
