# Tasks

## 1. Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif et baseline des éléments R1 et C1a, créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-evaluation --strict` avant tout code.

## 2. Modèles et API

- [x] 2.1 Étendre seulement `src/pixs/kernel/feature_flags.py` : `FeatureFlagEvaluationContext` frozen à cinq champs obligatoires sans défaut, `FeatureFlagResolution` frozen à statut borné, affectation ou `None` et tuple de diagnostics, fonction pure `resolve_feature_flag_assignment` réutilisant les validateurs et helpers existants, sans horloge, E/S, persistance, cohorte, prérequis ni repli.

## 3. Tests

- [x] 3.1 Créer `tests/unit/test_feature_flag_evaluation.py` : formes de contexte acceptées et refusées dont `scope` sans `tenant`, adéquation exacte `flag_id` et `selector_value`, dimensions non déclarées ignorées sans élargissement, fenêtre semi-ouverte sur `as_of` injecté, trois niveaux de priorité sans ordre relatif entre `INSTALLATION` et `ENVIRONMENT`, ambiguïté refusée même à valeurs égales, permutation du lot et double évaluation du même contexte identiques, `NO_MATCH`, `SELECTED` avec `False` conservé, conformité du schéma de valeur à la définition, entrée hostile fermée sans écho ni index dépendant de l'ordre.
- [x] 3.2 Créer `tests/integration/test_feature_flag_evaluation_integration.py` : import d'un enfant frais sous gardes causales d'E/S, résolution témoin déterministe sans effet, refus hostile avant tout usage, marqueur final dédié, périmètre sans Django, PostgreSQL, réseau ni secret.

## 4. Preuves

- [x] 4.1 Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS.
- [x] 4.2 Réussir les deux suites nouvelles et la régression des quarante-cinq tests existants dans un environnement explicite.
- [x] 4.3 Vérifier relecture byte-exacte des éléments R1 et C1a, conservation des exports et de la configuration de style, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R2 MOTAMOT, en explicitant les garanties R2, R3 et R4 non livrées.
- [x] 4.4 Réussir `openspec validate add-initial-feature-flag-evaluation --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d’archivage sous contrôle CGPT.

Après achèvement prouvé des tâches : archivage puis `STATISTIQUES.md` sous deux mandats distincts. Le parent CISMP reste OPEN.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 4. Preuves ».

### O45-SL01 — Prouver périmètre CGPT, absence de change actif et baseline des éléments R1 et C1a, créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-evaluation --strict` avant tout code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL02 — Étendre seulement `src/pixs/kernel/feature_flags.py` : `FeatureFlagEvaluationContext` frozen à cinq champs obligatoires sans défaut, `FeatureFlagResolution` frozen à statut borné, affectation ou `None` et tuple de diagnostics, fonction pure `resolve_feature_flag_assignment` réutilisant les validateurs et helpers existants, sans horloge, E/S, persistance, cohorte, prérequis ni repli.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Modèles et API », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL03 — Créer `tests/unit/test_feature_flag_evaluation.py` : formes de contexte acceptées et refusées dont `scope` sans `tenant`, adéquation exacte `flag_id` et `selector_value`, dimensions non déclarées ignorées sans élargissement, fenêtre semi-ouverte sur `as_of` injecté, trois niveaux de priorité sans ordre relatif entre `INSTALLATION` et `ENVIRONMENT`, ambiguïté refusée même à valeurs égales, permutation du lot et double évaluation du même contexte identiques, `NO_MATCH`, `SELECTED` avec `False` conservé, conformité du schéma de valeur à la définition, entrée hostile fermée sans écho ni index dépendant de l'ordre.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL04 — Créer `tests/integration/test_feature_flag_evaluation_integration.py` : import d'un enfant frais sous gardes causales d'E/S, résolution témoin déterministe sans effet, refus hostile avant tout usage, marqueur final dédié, périmètre sans Django, PostgreSQL, réseau ni secret.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL05 — Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Preuves », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL06 — Réussir les deux suites nouvelles et la régression des quarante-cinq tests existants dans un environnement explicite.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Preuves », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL07 — Vérifier relecture byte-exacte des éléments R1 et C1a, conservation des exports et de la configuration de style, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R2 MOTAMOT, en explicitant les garanties R2, R3 et R4 non livrées.

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Preuves », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O45-SL08 — Réussir `openspec validate add-initial-feature-flag-evaluation --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d’archivage sous contrôle CGPT.

- Ancien repère et tâche rattachée : tâche 4.4 ; section « 4. Preuves », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
