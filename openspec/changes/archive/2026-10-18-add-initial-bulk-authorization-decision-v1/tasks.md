# Tâches — add-initial-bulk-authorization-decision-v1

## 1. Préparation et implémentation

- [x] 1.1 Vérifier le canon AuthorityAssessmentV1, l’absence d’équivalent exporté et le NFDOC.
- [x] 1.2 Créer les quatre artefacts OpenSpec sans delta normatif artificiel.
- [x] 1.3 Ajouter BulkAuthorizationDecision passif sans modifier les consommateurs existants.
- [x] 1.4 Ajouter les tests du contrat, la non-substitution des chaînes et l’import isolé sans effet.

## 2. Validation et clôture

- [x] 2.1 Compiler les trois fichiers Python et exécuter les tests ciblés et régressions applicables.
- [x] 2.2 Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; distinguer les avertissements préexistants.
- [x] 2.3 Vérifier contenus, UTF-8/LF, cohérence avec les cadrages et absence d’écriture hors périmètre.
- [x] 2.4 Présenter les preuves et obtenir l’autorisation distincte de Codex pour l’archivage unique.

STATISTIQUES.md est obligatoire après archivage, sous mandat distinct, avant gate et livraison. Arrêt ciblé de CISMP6 après ce seul change ; aucun Git autorisé.

## Preuves examinées par Codex

- Prévol CAB exact, once, code 0 puis READY.
- Sept fichiers relus à l’identique, UTF-8/LF, sans modification des cadrages, du canon ni des consommateurs (empreintes inchangées).
- Trois fichiers Python compilés, code 0.
- 75 tests ciblés et régressions Bulk réussis, code 0.
- OpenSpec ciblé strict : code 0. Global standard : 187/187, code 0.
- Global strict : 184/186, code 1 ; quatre warnings historiques de longueur (bulk-operations exigences 6/10/13, identity-assurance exigence 4), zéro ERROR. Aucune correction hors périmètre. Les nombres globaux évoluent avec les archives concurrentes.
- Archivage unique autorisé par Codex après revue de ces preuves ; rapport STATISTIQUES.md obligatoire ensuite.
- Git non inspecté et aucune opération Git exécutée. PostgreSQL et frontend sans objet. Cycle global incomplet ; arrêt de CISMP6 après ce seul change.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Validation et clôture » ; « Preuves examinées par Codex ».

### B57-SL01 — Vérifier le canon AuthorityAssessmentV1, l’absence d’équivalent exporté et le NFDOC.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation et implémentation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL02 — Créer les quatre artefacts OpenSpec sans delta normatif artificiel.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation et implémentation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL03 — Ajouter BulkAuthorizationDecision passif sans modifier les consommateurs existants.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Préparation et implémentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL04 — Ajouter les tests du contrat, la non-substitution des chaînes et l’import isolé sans effet.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Préparation et implémentation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL05 — Compiler les trois fichiers Python et exécuter les tests ciblés et régressions applicables.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Validation et clôture », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL06 — Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; distinguer les avertissements préexistants.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Validation et clôture », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL07 — Vérifier contenus, UTF-8/LF, cohérence avec les cadrages et absence d’écriture hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Validation et clôture », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B57-SL08 — Présenter les preuves et obtenir l’autorisation distincte de Codex pour l’archivage unique.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Validation et clôture », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
