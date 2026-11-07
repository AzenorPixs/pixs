# Tasks — VALIDATE IMPORT VALIDATE_ONLY

- [x] 1. Vérifier artefacts, delta exact et périmètre strict ciblé avant tout code. Preuve : quatre artefacts UTF-8 LF, B07 canonique exact, `openspec validate add-bulk-import-validation-orchestration-v1 --strict` exit 0, requestId cismp1-751d094337644962a27d8eaccc484dce.
- [x] 2. Factorisation privée minimale de `bulk_private_object_reader.py` préservant API et comportement hash-only. Preuve : API hash-only/signature/14 AST inchangés, `py_compile` exit 0 request cismp1-d8acefe5251942b2a9940a618254c5ec, 21 tests compat exit 0 request cismp1-42793a17a1164228a918759b9c5081a4.
- [x] 3. Helper de capture `validate` dans `bulk_trusted_ports.py` seulement si strictement nécessaire, sous mandat distinct. Preuve : N/A justifié, helper existant `_capture_python_method` capture déjà `validate` async, `bulk_trusted_ports.py` inchangé (contrôle empreintes).
- [x] 4. Nouveau `bulk_import_validate.py` : phase VALIDATE_ONLY, parcours qualifié unique, parsing interne, tampon borné nettoyé, owner après intégrité et fermeture. Preuve : parcours qualifié unique, owner après intégrité/fermeture, zéro `execute`/`canonical`, unitaires 29/29 request cismp1-b6640a668bd64f14b17457868d978b11 et PG 34/34 request cismp1-5d5d8c28e83c49ae8a06625522b94572.
- [x] 5. Persistance finale rapport, checkpoint et progression avec transition sous gardes actuelles seulement et frontière async ORM ; refus sans forçage après annulation, expiration ou perte de bail. Preuve : mêmes 34 critères PostgreSQL réel 16.14, exit 0 `real_pg` True, `cleanup`/`conns`/`public` stables True.
- [x] 6. Tests unitaires : séquences, gardes, bornes, non-fuite, nettoyage du tampon, aucun owner avant preuve, zéro `execute`. Preuve : 29/29 inchangés après garde borne corrigée, repris dans régression 578 tests exit 0.
- [x] 7. Tests PostgreSQL isolés : nominal, rejets, rollback, CAS et concurrence, bail, replay terminal, aucun forçage. Preuve : harnais PG 34/34 tous flags True, aucun secret exposé, schéma owned nettoyé, toutes connexions fermées, request cismp1-5d5d8c28e83c49ae8a06625522b94572.
- [x] 8. `py_compile` de tous les fichiers Python modifiés et régressions lecteur, trusted ports, parser, repositories et admission utiles. Preuve : cinq Python compilés exit 0 (B04 request cismp1-d8acefe5251942b2a9940a618254c5ec, module après borne request cismp1-f3fa249d29e1478681d1ecd2ec76fa4e, unitaires request cismp1-597e341b790440688c2f186c69837730, harnais final request cismp1-2a1283826ed7468d8792d36a1d4f8ad3, fixture FeatureFlag request cismp1-d92dd27b9d2a4c4f9eefe103ea52232a), fixture `tests/integration/test_feature_flag_postgres_source_integration.py` remplacement unique `_CHILD` oracle, 39 AST préservés hors `_CHILD`, empreinte inverse vérifiée, test ciblé 1 test exit 0 request cismp1-76fc2f98570447eca9cac73b3a4c8095 ; régressions unit+intégration Bulk 578 tests exit 0 request cismp1-899000bc3a4646bab6151900020a67e9 et PG 34/34 request cismp1-5d5d8c28e83c49ae8a06625522b94572 conservés.
- [x] 9. Conformité OpenSpec, UTF-8 LF, empreintes du périmètre et validation combinée sous intégration. Preuve périmètre VALIDATE_ONLY : sous exclusion ref11, request cismp1-249a2cb5f1f849a7a3d398670517c544 235/235 modules, 1915 tests, 0 skip, 0 fail, exit natif 0, manifeste a68d004fa07bd1ab97b0320bf65a32f3cd715b87b99c5e8e93558ce42cef6e5a ; 10 fichiers UTF-8 LF, empreintes scope 5 Python vérifiées checkpoint integration_final_scope ; change courant valid True issues[] strict global JSON request cismp1-ab1aa0626b0d41cf85ee2e301747ec1f. Limitation exacte : Global --all --strict exit natif 1, 4 WARNING de longueur (>500 caractères), zéro ERROR : bulk-operations requirements[6],[10],[13] et identity-assurance requirements[4], préexistants et inchangés, pas de succès strict global. Aucun de ces anciens requirements modifié, canon Bulk SHA initial identique. Conformité fonctionnelle et validation stricte du change prouvées, pas conformité stricte globale inventée. Historique conservé : échec monolithique 1901 tests exit 1 (3 failures, 1 error), diagnostic protégé environnement/isolement et 22 tests API/PDP exit 0 request cismp1-dbd965bcd6a142cfb20fba104f722403, adaptation processus frais sans skip et correction fixture prouvées.

Procédure après preuves : archive unique seulement sur autorisation CGPT sous intégration,
puis `STATISTIQUES.md` sous mandat distinct (six sections et totaux),
publication, gate et libération, date archive CLI et fin RUN restent PROCÉDURE À EXÉCUTER ensuite,
non inclus comme preuve acquise de tâche 9 ; RUN non TERMINÉ.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Tasks — VALIDATE IMPORT VALIDATE_ONLY ».

### B52-SL01 — Vérifier artefacts, delta exact et périmètre strict ciblé avant tout code. Preuve : quatre artefacts UTF-8 LF, B07 canonique exact, `openspec validate add-bulk-import-validation-orchestration-v1 --strict` exit 0, requestId cismp1-751d094337644962a27d8eaccc484dce.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL02 — Factorisation privée minimale de `bulk_private_object_reader.py` préservant API et comportement hash-only. Preuve : API hash-only/signature/14 AST inchangés, `py_compile` exit 0 request cismp1-d8acefe5251942b2a9940a618254c5ec, 21 tests compat exit 0 request cismp1-42793a17a1164228a918759b9c5081a4.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL03 — Helper de capture `validate` dans `bulk_trusted_ports.py` seulement si strictement nécessaire, sous mandat distinct. Preuve : N/A justifié, helper existant `_capture_python_method` capture déjà `validate` async, `bulk_trusted_ports.py` inchangé (contrôle empreintes).

- Ancien repère et tâche rattachée : tâche 3 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL04 — Nouveau `bulk_import_validate.py` : phase VALIDATE_ONLY, parcours qualifié unique, parsing interne, tampon borné nettoyé, owner après intégrité et fermeture. Preuve : parcours qualifié unique, owner après intégrité/fermeture, zéro `execute`/`canonical`, unitaires 29/29 request cismp1-b6640a668bd64f14b17457868d978b11 et PG 34/34 request cismp1-5d5d8c28e83c49ae8a06625522b94572.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL05 — Persistance finale rapport, checkpoint et progression avec transition sous gardes actuelles seulement et frontière async ORM ; refus sans forçage après annulation, expiration ou perte de bail. Preuve : mêmes 34 critères PostgreSQL réel 16.14, exit 0 `real_pg` True, `cleanup`/`conns`/`public` stables True.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL06 — Tests unitaires : séquences, gardes, bornes, non-fuite, nettoyage du tampon, aucun owner avant preuve, zéro `execute`. Preuve : 29/29 inchangés après garde borne corrigée, repris dans régression 578 tests exit 0.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL07 — Tests PostgreSQL isolés : nominal, rejets, rollback, CAS et concurrence, bail, replay terminal, aucun forçage. Preuve : harnais PG 34/34 tous flags True, aucun secret exposé, schéma owned nettoyé, toutes connexions fermées, request cismp1-5d5d8c28e83c49ae8a06625522b94572.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL08 — `py_compile` de tous les fichiers Python modifiés et régressions lecteur, trusted ports, parser, repositories et admission utiles. Preuve : cinq Python compilés exit 0 (B04 request cismp1-d8acefe5251942b2a9940a618254c5ec, module après borne request cismp1-f3fa249d29e1478681d1ecd2ec76fa4e, unitaires request cismp1-597e341b790440688c2f186c69837730, harnais final request cismp1-2a1283826ed7468d8792d36a1d4f8ad3, fixture FeatureFlag request cismp1-d92dd27b9d2a4c4f9eefe103ea52232a), fixture `tests/integration/test_feature_flag_postgres_source_integration.py` remplacement unique `_CHILD` oracle, 39 AST préservés hors `_CHILD`, empreinte inverse vérifiée, test ciblé 1 test exit 0 request cismp1-76fc2f98570447eca9cac73b3a4c8095 ; régressions unit+intégration Bulk 578 tests exit 0 request cismp1-899000bc3a4646bab6151900020a67e9 et PG 34/34 request cismp1-5d5d8c28e83c49ae8a06625522b94572 conservés.

- Ancien repère et tâche rattachée : tâche 8 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B52-SL09 — Conformité OpenSpec, UTF-8 LF, empreintes du périmètre et validation combinée sous intégration. Preuve périmètre VALIDATE_ONLY : sous exclusion ref11, request cismp1-249a2cb5f1f849a7a3d398670517c544 235/235 modules, 1915 tests, 0 skip, 0 fail, exit natif 0, manifeste a68d004fa07bd1ab97b0320bf65a32f3cd715b87b99c5e8e93558ce42cef6e5a ; 10 fichiers UTF-8 LF, empreintes scope 5 Python vérifiées checkpoint integration_final_scope ; change courant valid True issues[] strict global JSON request cismp1-ab1aa0626b0d41cf85ee2e301747ec1f. Limitation exacte : Global --all --strict exit natif 1, 4 WARNING de longueur (>500 caractères), zéro ERROR : bulk-operations requirements[6],[10],[13] et identity-assurance requirements[4], préexistants et inchangés, pas de succès strict global. Aucun de ces anciens requirements modifié, canon Bulk SHA initial identique. Conformité fonctionnelle et validation stricte du change prouvées, pas conformité stricte globale inventée. Historique conservé : échec monolithique 1901 tests exit 1 (3 failures, 1 error), diagnostic protégé environnement/isolement et 22 tests API/PDP exit 0 request cismp1-dbd965bcd6a142cfb20fba104f722403, adaptation processus frais sans skip et correction fixture prouvées.

- Ancien repère et tâche rattachée : tâche 9 ; section « Tasks — VALIDATE IMPORT VALIDATE_ONLY », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
