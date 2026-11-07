# Tasks — add-bulk-export-manifest-persistence-v1

- [x] 1. Artefacts stricts pré-code : vérifier proposal headers Why/What Changes, design 17/18/TEXT/TrustedUtc, delta B12 verbatim, 6 fichiers seuls, sans code.
- [x] 2. Modèle/repo/migration/wiring : record 17+PK, repository insert/get, migration 0010 après 0009, models.py wiring seul, sans toucher pur/runtime existants.
- [x] 3. Tests unitaires offline : pur 17 + record/repository sous gardes réelles, frozen, owned, deferred/exclude, alias/atomic, malformed/capacity.
- [x] 4. Tests PG isolés : helper job_record_16hex inchangé, 18 colonnes/checks, roundtrip/None/False/UTC/grands ints, observer, co-commit/rollback, CHECK 23514, forward/reverse 0010.
- [x] 5. Compilation et régressions strictes : py_compile 6 fichiers, contrôles Django du modèle dans harness offline sous gardes, suites unit/integration ciblées, strict qualifié, sans élargir.
- [x] 6. Acceptation scope : 17 explicites, co-transaction owner, même operation stockage seul, non-preuve finalisation/READY/READ_RESULT/gouvernance, exclusions tenues.

Mention : après 6 prouvées, archivage unique et STATISTIQUES.md par archive (hors ces 6, tâche distincte sur mandat séparé).

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B44-SL01 — Artefacts stricts pré-code : vérifier proposal headers Why/What Changes, design 17/18/TEXT/TrustedUtc, delta B12 verbatim, 6 fichiers seuls, sans code.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tasks — add-bulk-export-manifest-persistence-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B44-SL02 — Modèle/repo/migration/wiring : record 17+PK, repository insert/get, migration 0010 après 0009, models.py wiring seul, sans toucher pur/runtime existants.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tasks — add-bulk-export-manifest-persistence-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B44-SL03 — Tests unitaires offline : pur 17 + record/repository sous gardes réelles, frozen, owned, deferred/exclude, alias/atomic, malformed/capacity.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tasks — add-bulk-export-manifest-persistence-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B44-SL04 — Tests PG isolés : helper job_record_16hex inchangé, 18 colonnes/checks, roundtrip/None/False/UTC/grands ints, observer, co-commit/rollback, CHECK 23514, forward/reverse 0010.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tasks — add-bulk-export-manifest-persistence-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B44-SL05 — Compilation et régressions strictes : py_compile 6 fichiers, contrôles Django du modèle dans harness offline sous gardes, suites unit/integration ciblées, strict qualifié, sans élargir.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tasks — add-bulk-export-manifest-persistence-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B44-SL06 — Acceptation scope : 17 explicites, co-transaction owner, même operation stockage seul, non-preuve finalisation/READY/READ_RESULT/gouvernance, exclusions tenues.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tasks — add-bulk-export-manifest-persistence-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
