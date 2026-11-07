# Tasks — add-p0-pdp-minimal

## 1. Modèles, catalogue et limites

- [x] 1.1 Créer `src/pixs/core/authz/policy.py` : Effect, Selector, ScopeSelector, Condition eq/in typés, Obligation AUDIT, Policy avec seuils assurance séparés et fenêtres, rejets avant activation — preuve : tests policy
- [x] 1.2 Créer `src/pixs/core/authz/snapshot.py` : Catalog complet, Limits stricts, factory build_snapshot bornes avant normalisation, triés, duplicata policy_id refusé — preuve : tests policy et temps
- [x] 1.3 Créer `src/pixs/core/authz/ports.py` : Request sans auth, AuthenticationContext §4.1, TrustedFacts, provider backend seul, Clock UTC unique, AuditSink strict — preuve : tests décision et audit

## 2. Évaluation et façade

- [x] 2.1 Créer `src/pixs/core/authz/decision.py` : authorize recalculé chaque appel, appariement strict, DENY>ALLOW>défaut, fait requis inconnu refusé sur candidate pertinente DENY ou ALLOW, assurances §4.1, expires min bornes et DENY futur, audit refus, échec jamais ALLOW — preuve : tests décision, temps et audit
- [x] 2.2 Créer `src/pixs/core/authz/__init__.py` : façade bornée des cinq sources — preuve : import public

## 3. Tests

- [x] 3.1 `tests/unit/test_pdp_policy.py` : construction, normalisation, wildcard/obligation inconnue/doublons/bornes refusés
- [x] 3.2 `tests/unit/test_pdp_decision.py` : appariement, priorité, bool/int, opérateur inconnu, absence conservant DENY, périmètres, assurances non substituables, snapshots invalides refusés
- [x] 3.3 `tests/unit/test_pdp_time.py` : UTC, TTL, fraîcheur, transitions futures, fuseaux, échéance exacte, renouvellement facts et snapshot entre deux appels, déterminisme et non-mutation
- [x] 3.4 `tests/integration/test_pdp_audit.py` : refus audités une fois, callback False et exception jamais ALLOW, plateforme explicite, cross-tenant refusé, doubles sans persistance

## 4. Validations

- [x] 4.1 Suites unit et intégration complètes via chemins DEVOPS — preuve : exits 0
- [x] 4.2 AST mémoire, UTF-8 et LF des sources et tests — preuve : contrôle ciblé
- [x] 4.3 OpenSpec strict via exécutable DEVOPS — preuve : 0 échec
- [x] 4.4 Revue code, specs, cadrages et hors périmètre — preuve : rapport

Limites : persistance, PEP, PostgreSQL et audit durable hors périmètre. Archivage et statistiques par mandats distincts ultérieurs.

## Preuves de validation

- 1.1–3.4 : cinq sources et quatre fichiers de tests relus ; 53 tests PDP unitaires et 10 tests PDP d'intégration mémoire inclus dans les suites complètes.
- 4.1 : 281 tests unitaires, exit 0 (`msg_0ee3beaea001czNs46J3NmnpgH`) ; 96 tests d'intégration, exit 0 (`msg_0ee39d289001fgqoFmAmAH7nKQ`).
- 4.2 : AST des neuf fichiers Python et UTF-8/LF des treize fichiers du change, exit 0 (`msg_0ee3d83ca001at9xHC5T7g96Vx`).
- 4.3 : OpenSpec strict, 77 éléments valides, zéro échec, exit 0 (`msg_0ee3ec6bd001vLtuQPf5kC37BE`).
- 4.4 : revue CGPT des sources et tests, du design, de `authorization-engine`, `TECHNICAL §4.1/12`, `PROJECT §2.31/2.32`, README, BUILD et DEVOPS. Les écritures observées de cette session sont limitées aux treize fichiers autorisés. Aucun Git, nouveau fournisseur, dépendance, build Debian/Docker ou accès de production exécuté.

Les refus d'accès sont testés sur un port d'audit mémoire. Un échec du port conserve DENY sans garantir une persistance ; un ALLOW demeure soumis aux obligations du PEP futur. Les réécritures intermédiaires incomplètes et les deux exécutions policy en échec ont été corrigées avant ces validations ; aucun achèvement intermédiaire n'a été coché.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 4. Validations » ; « Preuves de validation ».

### C25-SL01 — Créer `src/pixs/core/authz/policy.py` : Effect, Selector, ScopeSelector, Condition eq/in typés, Obligation AUDIT, Policy avec seuils assurance séparés et fenêtres, rejets avant activation — preuve : tests policy

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Modèles, catalogue et limites », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL02 — Créer `src/pixs/core/authz/snapshot.py` : Catalog complet, Limits stricts, factory build_snapshot bornes avant normalisation, triés, duplicata policy_id refusé — preuve : tests policy et temps

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Modèles, catalogue et limites », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL03 — Créer `src/pixs/core/authz/ports.py` : Request sans auth, AuthenticationContext §4.1, TrustedFacts, provider backend seul, Clock UTC unique, AuditSink strict — preuve : tests décision et audit

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Modèles, catalogue et limites », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL04 — Créer `src/pixs/core/authz/decision.py` : authorize recalculé chaque appel, appariement strict, DENY>ALLOW>défaut, fait requis inconnu refusé sur candidate pertinente DENY ou ALLOW, assurances §4.1, expires min bornes et DENY futur, audit refus, échec jamais ALLOW — preuve : tests décision, temps et audit

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Évaluation et façade », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL05 — Créer `src/pixs/core/authz/__init__.py` : façade bornée des cinq sources — preuve : import public

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Évaluation et façade », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL06 — `tests/unit/test_pdp_policy.py` : construction, normalisation, wildcard/obligation inconnue/doublons/bornes refusés

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL07 — `tests/unit/test_pdp_decision.py` : appariement, priorité, bool/int, opérateur inconnu, absence conservant DENY, périmètres, assurances non substituables, snapshots invalides refusés

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Tests », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL08 — `tests/unit/test_pdp_time.py` : UTC, TTL, fraîcheur, transitions futures, fuseaux, échéance exacte, renouvellement facts et snapshot entre deux appels, déterminisme et non-mutation

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Tests », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL09 — `tests/integration/test_pdp_audit.py` : refus audités une fois, callback False et exception jamais ALLOW, plateforme explicite, cross-tenant refusé, doubles sans persistance

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Tests », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL10 — Suites unit et intégration complètes via chemins DEVOPS — preuve : exits 0

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Validations », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL11 — AST mémoire, UTF-8 et LF des sources et tests — preuve : contrôle ciblé

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Validations », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL12 — OpenSpec strict via exécutable DEVOPS — preuve : 0 échec

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Validations », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C25-SL13 — Revue code, specs, cadrages et hors périmètre — preuve : rapport

- Ancien repère et tâche rattachée : tâche 4.4 ; section « 4. Validations », ligne 26 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
