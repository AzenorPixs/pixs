# Tasks — add-bulk-server-cancelled-transition-v1

Aucune tâche cochée sans preuve observée. Archivage et rapport utilisent des mandats CAB distincts.

- [x] 1.1 Ajouter `src/pixs/backend/bulk_server_cancelled_transition.py` avec la façade interne minimale, import inerte, types exacts, vraie capacité PG, autorité CANCEL courante avant SQL et unique primitive vers CANCELLED.
- [x] 1.2 Ajouter `tests/unit/test_bulk_server_cancelled_transition.py` : import/gardes hostiles sans I/O, composants exacts, alias/vendor, refus d'autorité avant SQL, diagnostics statiques et erreurs inattendues non masquées.
- [x] 1.3 Ajouter `tests/integration/test_bulk_server_cancelled_transition_postgres_integration.py` : inertie ordinaire, PG réel explicite isolé, flag préalable réel, transition état/révision seuls, coopérativité, conservation des champs/engagements, CAS/race, rollback, terminaux, nettoyage et connexions fermées.
- [x] 2.1 Compiler les trois fichiers et exécuter les nouveaux tests ordinaires avec résultats natifs.
- [x] 2.2 Qualifier le PostgreSQL réel sans mocks de la primitive ni tables publiques modifiées, avec finalisation prouvée.
- [x] 2.3 Exécuter les régressions applicables et vérifier B03/B06, UTF-8/LF, empreintes et absence d'écriture hors périmètre.
- [x] 2.4 Vérifier sous exclusion les validations combinées affectées, le strict ciblé et le résultat global exact avant archive, puis relire toutes les preuves.

Après les preuves préarchive : archive unique et synchronisation B06 seules sous décision distincte, publication et libération d'exclusion, rapport STATISTIQUES.md vérifié en phase REPORT, gate individuel, désarmement et libération. Le parent CISMP reprend sa sélection ; aucune coche anticipée de clôture.

Preuves préarchive observées : trois compilations natives exit 0 ; nouveaux tests ordinaires 3/3 ; régressions 45/45 ; PostgreSQL 16.14 réel, 22 propriétés vérifiées et nettoyage/connexions fermées ; combiné 1 951 tests dans 245 modules, zéro échec/skip et 409 empreintes Python identiques ; strict ciblé 1/1 sans issue ; global standard 80/80 exit 0 ; global strict 78/80 exit 1, uniquement quatre WARNING historiques (bulk-operations requirements[6], [10], [13], identity-assurance requirements[4]), zéro ERROR. Le strict global n’est pas déclaré réussi. Chaque opération conserve sa décision CAB et sa permission native once dans le checkpoint du RUN.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B54-SL01 — Ajouter `src/pixs/backend/bulk_server_cancelled_transition.py` avec la façade interne minimale, import inerte, types exacts, vraie capacité PG, autorité CANCEL courante avant SQL et unique primitive vers CANCELLED.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B54-SL02 — Ajouter `tests/unit/test_bulk_server_cancelled_transition.py` : import/gardes hostiles sans I/O, composants exacts, alias/vendor, refus d'autorité avant SQL, diagnostics statiques et erreurs inattendues non masquées.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B54-SL03 — Ajouter `tests/integration/test_bulk_server_cancelled_transition_postgres_integration.py` : inertie ordinaire, PG réel explicite isolé, flag préalable réel, transition état/révision seuls, coopérativité, conservation des champs/engagements, CAS/race, rollback, terminaux, nettoyage et connexions fermées.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B54-SL04 — Compiler les trois fichiers et exécuter les nouveaux tests ordinaires avec résultats natifs.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B54-SL05 — Qualifier le PostgreSQL réel sans mocks de la primitive ni tables publiques modifiées, avec finalisation prouvée.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B54-SL06 — Exécuter les régressions applicables et vérifier B03/B06, UTF-8/LF, empreintes et absence d'écriture hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B54-SL07 — Vérifier sous exclusion les validations combinées affectées, le strict ciblé et le résultat global exact avant archive, puis relire toutes les preuves.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « Tasks — add-bulk-server-cancelled-transition-v1 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
