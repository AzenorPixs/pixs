# Tâches — Représentation Enum de l'état InboxReceiptV1

## 1. Vocabulaire structurel pur

- [x] 1.1 Publier `src/pixs/backend/inbox_receipt_state.py` : `InboxReceiptState(Enum)` au seul membre canonique `CONSUMED`, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.
- [x] 1.2 Publier et exécuter le test unitaire `tests/unit/test_inbox_receipt_state.py` : adhésion exacte au nom/valeur et à l'ordre canonique, absence de membre supplémentaire, refus sans normalisation, chaîne `CONSUMED` admise par `validate_bulk_inbox_receipt_values` existant et membre Enum direct refusé sans modifier le validateur.
- [x] 1.3 Publier et exécuter le test d'intégration `tests/integration/test_inbox_receipt_state_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées positivement, même preuve validateur en lecture seule avec fixture minimale sans base, aucun effet observable.
- [x] 1.4 Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_bulk_inbox_receipt_values`, `test_event_publication_state`), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.

- [x] 1.5 Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.
- [x] 1.6 Vérifier le périmètre et les preuves avant décision distincte d’archivage.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et le rapport STATISTIQUES.md relèvent de décisions et mandats CGPT distincts après preuve des tâches.

<!-- DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend. -->

## Preuves exécutées

- Canon events B11/InboxReceiptV1 et absence de représentation relus, périmètre NFDOC approuvé par CGPT.
- Sept fichiers nouveaux aux contenus exacts, UTF-8/LF ; empreintes des fichiers existants contrôlés inchangées.
- Trois compilations py_compile : code 0.
- Tests ciblés/régressions : 26/26 OK, dont cinq nouveaux tests ; code 0. Import frais sous gardes positives et refus du membre Enum par le validateur existant prouvés.
- OpenSpec ciblé strict : code 0. Global standard : 186/186, code 0.
- Global strict : 184/186, code 1 ; quatre WARNING historiques de longueur (bulk-operations exigences 6/10/13, identity-assurance exigence 4), zéro ERROR ; aucune correction hors périmètre.
- Aucun branchement runtime, migration, façade, dépendance, accès PostgreSQL, navigateur ou Git.
- Archivage, publication et rapport statistique non revendiqués par ces coches ; mandats distincts à suivre.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves exécutées ».

### C92-SL01 — Publier `src/pixs/backend/inbox_receipt_state.py` : `InboxReceiptState(Enum)` au seul membre canonique `CONSUMED`, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Vocabulaire structurel pur », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C92-SL02 — Publier et exécuter le test unitaire `tests/unit/test_inbox_receipt_state.py` : adhésion exacte au nom/valeur et à l'ordre canonique, absence de membre supplémentaire, refus sans normalisation, chaîne `CONSUMED` admise par `validate_bulk_inbox_receipt_values` existant et membre Enum direct refusé sans modifier le validateur.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Vocabulaire structurel pur », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C92-SL03 — Publier et exécuter le test d'intégration `tests/integration/test_inbox_receipt_state_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées positivement, même preuve validateur en lecture seule avec fixture minimale sans base, aucun effet observable.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Vocabulaire structurel pur », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C92-SL04 — Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_bulk_inbox_receipt_values`, `test_event_publication_state`), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Vocabulaire structurel pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C92-SL05 — Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Vocabulaire structurel pur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C92-SL06 — Vérifier le périmètre et les preuves avant décision distincte d’archivage.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Vocabulaire structurel pur », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
