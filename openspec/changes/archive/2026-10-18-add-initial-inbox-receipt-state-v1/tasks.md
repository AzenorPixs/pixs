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
