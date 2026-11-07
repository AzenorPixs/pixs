# Tasks — add-p0-developer-kit-validators

## 1. Façade et sanitisation

- [x] 1.1 `src/pixs/developer_kit/validators.py` : `validate_manifest_text/file`, délégation noyau seul via ports publiés, sanitisation fermée champ/règle + repli, `TypeError` mésusage, erreurs lecture/Unicode/TOML en refus sans valeur. (validators01/02/03 ; relectures intégrales)
- [x] 1.2 Façade publique du rapport : `ValidationReport` défini dans `validators.py` et réexporté par `src/pixs/developer_kit/__init__.py` (anti-cycle, décision CGPT), frozen slots + `__post_init__` ssi, exports bornés, imports sans FS ni activation, docstring limites (pas de Kit complet, pas de conformité production). (init01 ; relecture 28 lignes)
- [x] 1.3 `src/pixs/developer_kit/README.md` : parcours local borné (écrire → valider → lire diagnostics), sans secret/réseau/production. (readme01 ; relecture 50 lignes)

## 2. Tests

- [x] 2.1 `tests/unit/test_developer_kit_validators.py` : enveloppe, immuabilité, sanitisation, adversariaux sans affichage de fixtures. (unit01/02 ; 19 méthodes)
- [x] 2.2 `tests/integration/test_developer_kit_example.py` : exemple P0 validé via le kit, mémoire seule. (integration01/02 ; 7 méthodes)
- [x] 2.3 Tests ciblés 100 % : 19/19 unitaires (unittest02, exit 0) puis 7/7 intégration (integrationtest01, exit 0), `PYTHONPATH=src`, `python3 -B`, chemins absolus DEVOPS. Incident : unittest01 18/19 (brut `TOML invalide` découpé), corrigé validators03, retest 19/19.
- [x] 2.4 Régressions globales 100 % : 380 unit (globalunit01, exit 0) + 125 intégration (globalintegration01, exit 0), sans régression des suites existantes.

## 3. Validations

- [x] 3.1 AST Python du périmètre : 4 fichiers compilent sans erreur. (ast02, exit 0)
- [x] 3.2 UTF-8/LF des 10 fichiers du périmètre, absence de modification hors scope, matrice cadrages/delta exact (delta MODIFIED `developer-experience` : recopie exacte `Parcours local reproductible` + `Diagnostics sans fuite` et leurs scénarios canoniques, aucune exigence nouvelle ; `component-model` en dépendance réutilisée, pas en capacité modifiée). (ast02 : `utf8_lf_files: 10`, `delta_exact: true`, `kernel_imports_public: true` ; AST01 REJECTED avant tout Bash, récupéré recovery02)
- [x] 3.3 `openspec validate --all --strict` : 77 passed, 0 failed, 14 INFO non bloquantes ; change valide. (validatechange01 + validateall01, exit 0)

NOTE de pilotage (pas une tâche d'implémentation) : l'archivage du change et les statistiques restent des mandats CAB distincts à venir, non prouvés pré-archive ; jamais les déclarer faits. Aucune affirmation de Kit complet ni de P0 global.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Tasks — add-p0-developer-kit-validators » ; « 3. Validations ».

### O42-SL01 — `src/pixs/developer_kit/validators.py` : `validate_manifest_text/file`, délégation noyau seul via ports publiés, sanitisation fermée champ/règle + repli, `TypeError` mésusage, erreurs lecture/Unicode/TOML en refus sans valeur. (validators01/02/03 ; relectures intégrales)

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Façade et sanitisation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL02 — Façade publique du rapport : `ValidationReport` défini dans `validators.py` et réexporté par `src/pixs/developer_kit/__init__.py` (anti-cycle, décision CGPT), frozen slots + `__post_init__` ssi, exports bornés, imports sans FS ni activation, docstring limites (pas de Kit complet, pas de conformité production). (init01 ; relecture 28 lignes)

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Façade et sanitisation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL03 — `src/pixs/developer_kit/README.md` : parcours local borné (écrire → valider → lire diagnostics), sans secret/réseau/production. (readme01 ; relecture 50 lignes)

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Façade et sanitisation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL04 — `tests/unit/test_developer_kit_validators.py` : enveloppe, immuabilité, sanitisation, adversariaux sans affichage de fixtures. (unit01/02 ; 19 méthodes)

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Tests », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL05 — `tests/integration/test_developer_kit_example.py` : exemple P0 validé via le kit, mémoire seule. (integration01/02 ; 7 méthodes)

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Tests », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL06 — Tests ciblés 100 % : 19/19 unitaires (unittest02, exit 0) puis 7/7 intégration (integrationtest01, exit 0), `PYTHONPATH=src`, `python3 -B`, chemins absolus DEVOPS. Incident : unittest01 18/19 (brut `TOML invalide` découpé), corrigé validators03, retest 19/19.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Tests », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL07 — Régressions globales 100 % : 380 unit (globalunit01, exit 0) + 125 intégration (globalintegration01, exit 0), sans régression des suites existantes.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL08 — AST Python du périmètre : 4 fichiers compilent sans erreur. (ast02, exit 0)

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Validations », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL09 — UTF-8/LF des 10 fichiers du périmètre, absence de modification hors scope, matrice cadrages/delta exact (delta MODIFIED `developer-experience` : recopie exacte `Parcours local reproductible` + `Diagnostics sans fuite` et leurs scénarios canoniques, aucune exigence nouvelle ; `component-model` en dépendance réutilisée, pas en capacité modifiée). (ast02 : `utf8_lf_files: 10`, `delta_exact: true`, `kernel_imports_public: true` ; AST01 REJECTED avant tout Bash, récupéré recovery02)

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Validations », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O42-SL10 — `openspec validate --all --strict` : 77 passed, 0 failed, 14 INFO non bloquantes ; change valide. (validatechange01 + validateall01, exit 0)

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Validations », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
