# Tasks — add-bulk-server-cancellation-request-v1

Aucune tâche cochée avant preuve observée. L'archivage nécessite une décision CAB distincte.

- [x] 1.1 Implémenter le module nouveau `src/pixs/backend/bulk_server_cancellation.py` avec `request_bulk_cancellation`, types exacts, vrais composants et capacité PG, autorité `CANCEL` actuelle sur la cible avant SQL Bulk, primitive seule et diagnostics statiques. Preuve attendue : fichier nouveau relu, import inerte, refus hostiles sans I/O.
- [x] 1.2 Ajouter les unitaires nouveaux `tests/unit/test_bulk_server_cancellation.py` pour import inerte, hostiles, refus et absence d'I/O avant autorisation, contrat de retour. Preuve attendue : test nouveau exécuté avec résultat natif.
- [x] 1.3 Ajouter le harnais PG nouveau `tests/integration/test_bulk_server_cancellation_postgres_integration.py` réel isolé pour effet flag et révision seuls, CAS, terminaux, rollback, race, absence de modification de progression, échéance, checkpoint, Job et schedule, blocage de l'unité suivante. Preuve attendue : sortie PG réelle avec nettoyage prouvé.
- [x] 2.1 Compiler les trois fichiers et exécuter les unitaires avec résultats natifs. Preuve attendue : `py_compile` et sortie de test observées.
- [x] 2.2 Exécuter le PG réel explicite avec nettoyage, connexions fermées et tables publiques inchangées. Preuve attendue : outcome réel et finalisation prouvée.
- [x] 2.3 Vérifier régressions ciblées, conformité B03/B06, UTF-8/LF, empreintes et aucune écriture hors périmètre. Preuve attendue : contrôles relus sans écart.
- [x] 2.4 Vérifier sous exclusion d’intégration les validations combinées affectées, le strict ciblé et le résultat global exact avant archivage. Preuve attendue : résultats natifs et contrôles préarchive disponibles.

Clôture après les preuves préarchive : archivage unique sous décision CAB distincte, rapport `STATISTIQUES.md` distinct vérifié, publication, gate individuel, désarmement et libération. Ces opérations suivent la checklist et ne nécessitent aucune coche avant leur propre exécution.

Périmètre : trois fichiers nouveaux seuls et artefacts de ce change uniquement, aucun code existant à modifier.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B53-SL01 — Implémenter le module nouveau `src/pixs/backend/bulk_server_cancellation.py` avec `request_bulk_cancellation`, types exacts, vrais composants et capacité PG, autorité `CANCEL` actuelle sur la cible avant SQL Bulk, primitive seule et diagnostics statiques. Preuve attendue : fichier nouveau relu, import inerte, refus hostiles sans I/O.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B53-SL02 — Ajouter les unitaires nouveaux `tests/unit/test_bulk_server_cancellation.py` pour import inerte, hostiles, refus et absence d'I/O avant autorisation, contrat de retour. Preuve attendue : test nouveau exécuté avec résultat natif.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B53-SL03 — Ajouter le harnais PG nouveau `tests/integration/test_bulk_server_cancellation_postgres_integration.py` réel isolé pour effet flag et révision seuls, CAS, terminaux, rollback, race, absence de modification de progression, échéance, checkpoint, Job et schedule, blocage de l'unité suivante. Preuve attendue : sortie PG réelle avec nettoyage prouvé.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B53-SL04 — Compiler les trois fichiers et exécuter les unitaires avec résultats natifs. Preuve attendue : `py_compile` et sortie de test observées.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B53-SL05 — Exécuter le PG réel explicite avec nettoyage, connexions fermées et tables publiques inchangées. Preuve attendue : outcome réel et finalisation prouvée.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B53-SL06 — Vérifier régressions ciblées, conformité B03/B06, UTF-8/LF, empreintes et aucune écriture hors périmètre. Preuve attendue : contrôles relus sans écart.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B53-SL07 — Vérifier sous exclusion d’intégration les validations combinées affectées, le strict ciblé et le résultat global exact avant archivage. Preuve attendue : résultats natifs et contrôles préarchive disponibles.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « Tasks — add-bulk-server-cancellation-request-v1 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
