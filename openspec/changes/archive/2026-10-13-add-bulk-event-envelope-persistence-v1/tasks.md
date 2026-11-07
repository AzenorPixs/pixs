# Tasks — add-bulk-event-envelope-persistence-v1

- [x] 1. Artefacts OpenSpec : proposal, design, tasks et delta specs/events avec B11 verbatim, cohérence des six fichiers et des exclusions.
- [x] 2. Record et codec privé : bulk_event_envelope_record.py avec treize clés, event_id PK, TEXT JSON privé, NUL préservé, UTC strict, copies owned, insert-only.
- [x] 3. Repository, models et migration : bulk_event_envelope_repository.py insert/get avec alias unique et duplicata PK 23505, import minimal dans models.py, migrations/0007_bulk_event_envelope.py dépendant de 0006 et réversible.
- [x] 4. Tests unitaires offline : tests/unit/test_bulk_event_envelope_persistence.py en processus frais, gardes, types hostiles avant callbacks/I/O, NUL payload/-0.0/grand int supporté/refus capacité réelle, UTC, copies et gel, save insert-only/full_clean exclude, migration vue sans base.
- [x] 5. Tests PostgreSQL isolés : tests/integration/test_bulk_event_envelope_persistence_integration.py avec schéma possédé, co-commit/co-rollback, transaction active obligatoire même alias, race une seule création, refus capturé toujours rollback owner, contraintes, forward/reverse 0007 seule, nettoyage et connexions.
- [x] 6. Validations et acceptation : py_compile des fichiers, unittest applicables, contrôle OpenSpec selon DEVOPS.md, régressions pertinentes, conformité au périmètre sans écart.

Note : l'archivage et le rapport par archive suivent une procédure distincte après preuves et ne forment pas une tâche circulaire ici.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B43-SL01 — Artefacts OpenSpec : proposal, design, tasks et delta specs/events avec B11 verbatim, cohérence des six fichiers et des exclusions.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tasks — add-bulk-event-envelope-persistence-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B43-SL02 — Record et codec privé : bulk_event_envelope_record.py avec treize clés, event_id PK, TEXT JSON privé, NUL préservé, UTC strict, copies owned, insert-only.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tasks — add-bulk-event-envelope-persistence-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B43-SL03 — Repository, models et migration : bulk_event_envelope_repository.py insert/get avec alias unique et duplicata PK 23505, import minimal dans models.py, migrations/0007_bulk_event_envelope.py dépendant de 0006 et réversible.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tasks — add-bulk-event-envelope-persistence-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B43-SL04 — Tests unitaires offline : tests/unit/test_bulk_event_envelope_persistence.py en processus frais, gardes, types hostiles avant callbacks/I/O, NUL payload/-0.0/grand int supporté/refus capacité réelle, UTC, copies et gel, save insert-only/full_clean exclude, migration vue sans base.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tasks — add-bulk-event-envelope-persistence-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B43-SL05 — Tests PostgreSQL isolés : tests/integration/test_bulk_event_envelope_persistence_integration.py avec schéma possédé, co-commit/co-rollback, transaction active obligatoire même alias, race une seule création, refus capturé toujours rollback owner, contraintes, forward/reverse 0007 seule, nettoyage et connexions.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tasks — add-bulk-event-envelope-persistence-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B43-SL06 — Validations et acceptation : py_compile des fichiers, unittest applicables, contrôle OpenSpec selon DEVOPS.md, régressions pertinentes, conformité au périmètre sans écart.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tasks — add-bulk-event-envelope-persistence-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
