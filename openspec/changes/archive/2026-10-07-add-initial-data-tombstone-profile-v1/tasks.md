# Tâches — profil tombstone-v1

## 1. Préparation

- [x] 1.1 Vérifier les artefacts UTF-8/LF, le delta mot pour mot identique au requirement canonique et les validations OpenSpec du change et du canon.

## 2. Implémentation minimale

- [x] 2.1 Ajouter uniquement src/pixs/kernel/data_tombstone_profile.py : TombstoneProfile immuable à huit champs sans défaut et validateur structurel pur à diagnostics VALIDATE statiques triés/dédupliqués.
- [x] 2.2 Ajouter les tests unitaires de surface, valeurs opaques, types exacts/hostiles, calendrier UTC, scope/tenant et diagnostics sans écho.
- [x] 2.3 Ajouter et réussir l'intégration en processus frais -I -B avec gardes positives d'effets, d'environnement, de base et d'horloge.

## 3. Validation

- [x] 3.1 Compiler les trois fichiers Python avec l'interpréteur déclaré et réussir les tests ciblés.
- [x] 3.2 Réussir les régressions des profils/vocabulaires de données, des diagnostics, de pureté Kernel et des façades.
- [x] 3.3 Vérifier la conformité canon/cadrages/code/tests, les validations OpenSpec finales, UTF-8/LF et l'absence de modification hors périmètre par empreintes sans Git.

L'archivage --skip-specs reste un mandat distinct après toutes les preuves. Le rapport STATISTIQUES.md de l'archive exige ensuite son propre mandat et la vérification de ses six sections et totaux. Ce profil n'achève pas les exigences runtime générales de cycle de vie.

## Preuves de fin du périmètre

- Trois compilations natives réussies, code 0 pour chaque fichier Python.
- Tests ciblés : 21 unitaires et 1 intégration en processus frais, tous réussis.
- Régressions : 108 tests dans 23 modules historiques, sans échec, erreur ou skip.
- Change validé strictement : 1/1, issues vides, code 0 ; global : 77/77, code 0.
- Canon validé sur les critères applicables ; les 20 WARNING globaux portent uniquement sur la longueur, explicitement exclue comme critère de qualité par le développeur. Le contrôle strict du canon à code 1 n'est pas déclaré réussi.
- Delta canonique identique ; UTF-8/LF ; 198 empreintes de référence intactes et trois nouveaux fichiers conformes aux contenus revus.
- Cadrages cohérents dans ce périmètre ; aucun Git, dépendance, façade, configuration, accès PostgreSQL ou comportement runtime ajouté.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Validation » ; « Preuves de fin du périmètre ».

### C74-SL01 — Vérifier les artefacts UTF-8/LF, le delta mot pour mot identique au requirement canonique et les validations OpenSpec du change et du canon.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C74-SL02 — Ajouter uniquement src/pixs/kernel/data_tombstone_profile.py : TombstoneProfile immuable à huit champs sans défaut et validateur structurel pur à diagnostics VALIDATE statiques triés/dédupliqués.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Implémentation minimale », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C74-SL03 — Ajouter les tests unitaires de surface, valeurs opaques, types exacts/hostiles, calendrier UTC, scope/tenant et diagnostics sans écho.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Implémentation minimale », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C74-SL04 — Ajouter et réussir l'intégration en processus frais -I -B avec gardes positives d'effets, d'environnement, de base et d'horloge.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Implémentation minimale », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C74-SL05 — Compiler les trois fichiers Python avec l'interpréteur déclaré et réussir les tests ciblés.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Validation », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C74-SL06 — Réussir les régressions des profils/vocabulaires de données, des diagnostics, de pureté Kernel et des façades.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Validation », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C74-SL07 — Vérifier la conformité canon/cadrages/code/tests, les validations OpenSpec finales, UTF-8/LF et l'absence de modification hors périmètre par empreintes sans Git.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Validation », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
