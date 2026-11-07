# Tâches — Vocabulaire des modes d’import en masse

- [x] 1. Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon, et réussir la validation stricte du change avant code.
- [x] 2. Ajouter le seul module interne BulkCommitMode aux quatre membres canoniques, sans façade ni dépendance, puis réussir sa compilation.
- [x] 3. Vérifier l’import isolé, les membres et l’export ; réussir les suites existantes de pureté du noyau, façades et vocabulaires voisins.
- [x] 4. Réussir la validation finale OpenSpec ; vérifier UTF-8/LF, les seules cibles autorisées et les empreintes des fichiers préexistants.

Une tâche n’est cochée qu’après ses preuves. Le vocabulaire ne constitue pas une implémentation de l’import effectif ou du contrat BulkOperation complet. Archivage et STATISTIQUES.md restent deux mandats distincts après les quatre tâches prouvées.

## Preuves de clôture

- Quatre artefacts UTF-8/LF ; delta MODIFIED identique à l’exigence canonique et son scénario.
- Canon bulk-operations et change avant code : validations strictes, codes natifs 0.
- Module relu (AST : quatre membres nom=valeur, export unique) ; py_compile avec Python déclaré, code natif 0.
- Chargement du module en processus neuf via -B -m, code natif 0 ; l’inspection -c initiale a été refusée avant exécution pour échappement divergent et n’est pas une preuve.
- Tests existants : 14 intégration de pureté/façades et 6 unitaires des vocabulaires voisins, soit 20 réussis, aucun échec ni skip ; codes natifs 0.
- Change final strict : code natif 0 ; cinq fichiers autorisés UTF-8/LF et empreintes des cadrages, canon, dépendances et façade initiale inchangées.
- Écarts de pilotage refusés sans effet ; trois transferts de session via job/recover avec prévol neuf, réponse MCP corrélée, permission unique et READY pending0. Résultats réussis conservés.

Archivage et STATISTIQUES.md restent des mandats distincts après ces preuves.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves de clôture ».

### B12-SL01 — Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon, et réussir la validation stricte du change avant code.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — Vocabulaire des modes d’import en masse », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B12-SL02 — Ajouter le seul module interne BulkCommitMode aux quatre membres canoniques, sans façade ni dépendance, puis réussir sa compilation.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — Vocabulaire des modes d’import en masse », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B12-SL03 — Vérifier l’import isolé, les membres et l’export ; réussir les suites existantes de pureté du noyau, façades et vocabulaires voisins.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — Vocabulaire des modes d’import en masse », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B12-SL04 — Réussir la validation finale OpenSpec ; vérifier UTF-8/LF, les seules cibles autorisées et les empreintes des fichiers préexistants.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — Vocabulaire des modes d’import en masse », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
