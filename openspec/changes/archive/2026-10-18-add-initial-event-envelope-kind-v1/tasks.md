# Tâches — vocabulaire initial EventEnvelopeKind

- [x] 1. Vérifier le canon, l’absence de représentation équivalente et les frontières du sous-lot.
- [x] 2. Ajouter EventEnvelopeKind et ses deux valeurs canoniques sans branchement runtime.
- [x] 3. Prouver les recherches exactes, la préservation des gardes existantes et l’import en processus frais sous gardes éprouvées.
- [x] 4. Exécuter syntaxe, tests et régressions pertinents, UTF-8/LF et validations OpenSpec ; conserver leurs résultats réels.
- [x] 5. Vérifier le périmètre et réunir les preuves autorisant l’archivage de ce seul change par CGPT.

L’archivage, la publication et STATISTIQUES.md restent des mandats distincts. Aucune tâche ne peut être cochée avant ses preuves.

## Preuves

- Canon events B11/EventEnvelopeV1 relu ; absence d’Enum équivalent vérifiée.
- Sept fichiers nouveaux relus UTF-8/LF, contenus exacts vérifiés ; 17 références/cadrages/validateurs existants inchangés par empreinte.
- Trois fichiers Python compilés, code 0 ; 47 tests réussis (5 nouveaux et 42 régressions), code 0.
- Import frais -I -B avec gardes éprouvées et préservation de la validation str exacte prouvés par ces tests.
- OpenSpec ciblé strict : valide, code 0. Global standard : 187/187, code 0.
- Global strict : 185/187, code 1 ; exactement quatre WARNING de longueur préexistants dans bulk-operations[6,10,13] et identity-assurance[4], zéro ERROR. Aucun canon hors périmètre corrigé.
- Deux prévols CAB complets exacts et permissions once corrélées prouvés ; une demande de tests mal scopée annulée avant effet et une demande globale sur base périmée refusée avant effet, puis reprises avec identités neuves.
- Archivage, publication et rapport statistique non revendiqués par ces coches ; opérations distinctes à suivre.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves ».

### C90-SL01 — Vérifier le canon, l’absence de représentation équivalente et les frontières du sous-lot.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — vocabulaire initial EventEnvelopeKind », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C90-SL02 — Ajouter EventEnvelopeKind et ses deux valeurs canoniques sans branchement runtime.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — vocabulaire initial EventEnvelopeKind », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C90-SL03 — Prouver les recherches exactes, la préservation des gardes existantes et l’import en processus frais sous gardes éprouvées.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — vocabulaire initial EventEnvelopeKind », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C90-SL04 — Exécuter syntaxe, tests et régressions pertinents, UTF-8/LF et validations OpenSpec ; conserver leurs résultats réels.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — vocabulaire initial EventEnvelopeKind », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C90-SL05 — Vérifier le périmètre et réunir les preuves autorisant l’archivage de ce seul change par CGPT.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — vocabulaire initial EventEnvelopeKind », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
