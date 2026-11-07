# Tâches — add-initial-bulk-operation-header-v1

- [x] 1. Vérifier le delta MODIFIED exact des quatre exigences canoniques, l'unicité du change actif, UTF-8/LF et la validation OpenSpec avant code.
- [x] 2. Créer le module interne immuable à trois champs obligatoires et son validateur pur, avec types exacts, parseur SemVer existant et diagnostics statiques.
- [x] 3. Créer les tests unitaires comportementaux : conservation, variantes/versions, refus des types et hooks étrangers, immuabilité, diagnostics déterministes sans écho.
- [x] 4. Créer l'intégration en processus frais sous gardes d'effets avec contrôles positifs.
- [x] 5. Compiler séparément les trois fichiers ; exécuter les tests ciblés et les régressions applicables.
- [x] 6. Valider OpenSpec après code ; vérifier les trois sources, le delta canon exact, UTF-8/LF, les façades et les fichiers existants préservés.
- [x] 7. Contrôler l'acceptation complète et les preuves CAB avant de cocher les tâches.

L'archivage --skip-specs et la publication de STATISTIQUES.md restent des mandats
distincts, autorisés après preuves ; aucune case ne les anticipe.

Preuves vérifiées par CGPT : trois compilations exit0 ; 11 tests ciblés dont processus frais gardé et 43 régressions, soit 54 réussites ; validations OpenSpec avant/après code 1/1 exit0 issues[] ; sept fichiers relus exacts UTF-8/LF, delta canon identique, 21 empreintes de référence préservées après réconciliation des évolutions externes AGENTS.md v0.4 / ORCHESTRATED_CODING.md v0.1. Aucune nouvelle dépendance ni façade modifiée. Archivage et rapport restent à exécuter sous mandats distincts.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B19-SL01 — Vérifier le delta MODIFIED exact des quatre exigences canoniques, l'unicité du change actif, UTF-8/LF et la validation OpenSpec avant code.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B19-SL02 — Créer le module interne immuable à trois champs obligatoires et son validateur pur, avec types exacts, parseur SemVer existant et diagnostics statiques.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B19-SL03 — Créer les tests unitaires comportementaux : conservation, variantes/versions, refus des types et hooks étrangers, immuabilité, diagnostics déterministes sans écho.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B19-SL04 — Créer l'intégration en processus frais sous gardes d'effets avec contrôles positifs.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B19-SL05 — Compiler séparément les trois fichiers ; exécuter les tests ciblés et les régressions applicables.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B19-SL06 — Valider OpenSpec après code ; vérifier les trois sources, le delta canon exact, UTF-8/LF, les façades et les fichiers existants préservés.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B19-SL07 — Contrôler l'acceptation complète et les preuves CAB avant de cocher les tâches.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — add-initial-bulk-operation-header-v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
