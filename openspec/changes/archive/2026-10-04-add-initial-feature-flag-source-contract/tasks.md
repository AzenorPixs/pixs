# Tasks

## 1. Préparation

- [x] 1.1 Confirmer périmètre, absence de change actif, 22 baselines, 119 tests et normes R2/R4 ; publier les cinq artefacts puis réussir les stricts avant code.

## 2. Contrat

- [x] 2.1 Ajouter `FeatureFlagSourceSnapshot` à quatre champs figés et son validateur avec les validateurs existants, liaisons exactes, règle unique par clé et refus de toute règle non référencée.
- [x] 2.2 Ajouter `evaluate_feature_flag_source_snapshot` : types et version fermés, lookup exact, extraction complète des affectations, appel réel à `evaluate_feature_flag_assignments_with_cohort` sans projection ni repli inventé.

## 3. Tests

- [x] 3.1 Créer la suite unitaire causale : lot vide valide, définition ou règle manquantes, affectation hors flag, selector non déclaré, versions divergentes, règles hôtes partagées, liaisons incohérentes, entrées hostiles sans callback, non-mutation et absence d'écho.
- [x] 3.2 Créer l'intégration fraîche sans I/O réelle : finder et gardes éprouvés avant import, appel de composition réel, comptes zéro après usages, aucune horloge, base, réseau ou secret.

## 4. Preuves

- [x] 4.1 Réussir les compilations des trois sources, syntaxe minimum 3.12, nouvelles suites et les 119 régressions dans un environnement explicite.
- [x] 4.2 Vérifier les 22 baselines inchangées, le delta R2/R4 recopié mot pour mot, UTF-8/LF, limites de provenance et absence de persistance livrée.
- [x] 4.3 Réussir les stricts du change et canonique après preuves, cocher uniquement les huit tâches sous mandat distinct, puis faire contrôler l'archivage par CGPT.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 4. Preuves ».

### O52-SL01 — Confirmer périmètre, absence de change actif, 22 baselines, 119 tests et normes R2/R4 ; publier les cinq artefacts puis réussir les stricts avant code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL02 — Ajouter `FeatureFlagSourceSnapshot` à quatre champs figés et son validateur avec les validateurs existants, liaisons exactes, règle unique par clé et refus de toute règle non référencée.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Contrat », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL03 — Ajouter `evaluate_feature_flag_source_snapshot` : types et version fermés, lookup exact, extraction complète des affectations, appel réel à `evaluate_feature_flag_assignments_with_cohort` sans projection ni repli inventé.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Contrat », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL04 — Créer la suite unitaire causale : lot vide valide, définition ou règle manquantes, affectation hors flag, selector non déclaré, versions divergentes, règles hôtes partagées, liaisons incohérentes, entrées hostiles sans callback, non-mutation et absence d'écho.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL05 — Créer l'intégration fraîche sans I/O réelle : finder et gardes éprouvés avant import, appel de composition réel, comptes zéro après usages, aucune horloge, base, réseau ou secret.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Tests », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL06 — Réussir les compilations des trois sources, syntaxe minimum 3.12, nouvelles suites et les 119 régressions dans un environnement explicite.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Preuves », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL07 — Vérifier les 22 baselines inchangées, le delta R2/R4 recopié mot pour mot, UTF-8/LF, limites de provenance et absence de persistance livrée.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Preuves », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O52-SL08 — Réussir les stricts du change et canonique après preuves, cocher uniquement les huit tâches sous mandat distinct, puis faire contrôler l'archivage par CGPT.

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Preuves », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
