# Tâches — Vocabulaire des variantes d’opération en masse

- [x] 1. Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et réussir la validation stricte du change avant code.
- [x] 2. Ajouter uniquement BulkOperationVariant IMPORT/EXPORT au module existant, conserver BulkCommitMode et la façade, puis réussir compilation, inspection AST et import en processus neuf.
- [x] 3. Réussir les suites existantes de pureté du noyau, façades et vocabulaires voisins ; consigner résultats et codes natifs.
- [x] 4. Réussir la validation finale OpenSpec et contrôler UTF-8/LF, les seules cibles autorisées et les empreintes initiales.

Aucune tâche n’est cochée avant preuve. Ce vocabulaire ne livre pas le contrat BulkOperation complet. Archivage et STATISTIQUES.md restent deux mandats distincts après ces preuves.

## Preuves de clôture

- Quatre artefacts exacts UTF-8/LF et delta canon identique ; strict précode code 0 conservé sans rejeu.
- Module exact, AST et exports inspectés par CGPT ; BulkCommitMode conservé, façade inchangée, 350 empreintes préservées.
- Compilation et import en processus neuf réussis, codes natifs 0.
- 20 tests réussis : pureté 3, façades 11, JobState 3, NotificationChannel 3 ; aucun échec ni skip.
- Change final strict : code natif 0. Canon global : 63 passed / 13 failed warning-only, exit natif 1 ; 21 avertissements de longueur, zéro ERROR, 76 fichiers canoniques inchangés. Résultat qualifié selon le critère développeur excluant la longueur, pas présenté comme une réussite native globale.
- Demandes divergentes refusées sans effet ; délais MCP résolus par polling corrélé ; aucune permission réutilisée.

Archivage et STATISTIQUES.md restent des mandats distincts.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves de clôture ».

### B14-SL01 — Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et réussir la validation stricte du change avant code.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — Vocabulaire des variantes d’opération en masse », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B14-SL02 — Ajouter uniquement BulkOperationVariant IMPORT/EXPORT au module existant, conserver BulkCommitMode et la façade, puis réussir compilation, inspection AST et import en processus neuf.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — Vocabulaire des variantes d’opération en masse », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B14-SL03 — Réussir les suites existantes de pureté du noyau, façades et vocabulaires voisins ; consigner résultats et codes natifs.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — Vocabulaire des variantes d’opération en masse », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B14-SL04 — Réussir la validation finale OpenSpec et contrôler UTF-8/LF, les seules cibles autorisées et les empreintes initiales.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — Vocabulaire des variantes d’opération en masse », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
