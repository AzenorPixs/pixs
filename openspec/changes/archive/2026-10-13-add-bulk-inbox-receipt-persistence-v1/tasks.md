# Tasks — add-bulk-inbox-receipt-persistence-v1

- [x] 1. Préparer les quatre artefacts cohérents, Why/What Changes requis, delta MODIFIED B11 verbatim sans norme nouvelle ; strict précode sans issue.
- [x] 2. Implémenter record/repository, import minimal models.py et migration0008 dépendant de0007 réversible : huit clés exactes, PK technique hors huit, unique consumer_reference/event_id, insert-only/alias/atomic, savepoint INSERT puis lecture, Duplicate/Divergence et rollback propriétaire capturé.
- [x] 3. Implémenter unittest offline : vrais imports sous gardes, types hostiles avant comportement/I/O, sans écho, capture et exports owned/frozen, save/full_clean exclude/déféré, métadonnées/migration sans DB ; aucune preuve SQL par mock miroir.
- [x] 4. Implémenter harness PostgreSQL isolé : clé composée/version/sha/consumer indépendant, co-transaction avec effet synthétique et JobRecord existant, refus capturé rollback, race deux bloqués/un gagnant/connexions fermées, visibilité inflight non ack, forward/reverse0008 seule/public et dix tables stables/cleanup strict.
- [x] 5. Compiler les six sources, exécuter unittest et PG réels autorisés puis régressions pertinentes avec outils DEVOPS ; strict ciblé sans issue et global comparé aux trois WARNING historiques exacts.
- [x] 6. Accepter sur preuves : huit clés sans ajout/default, UTF-8/LF, fichiers ciblés seuls, canon/cadrages/purs/runtime/CommandIdempotency/EventEnvelope préservés, aucune autorité/receiver/provider ni B11 global déclaré.

Après preuve des six tâches, les cocher ; archivage unique --skip-specs puis STATISTIQUES distinct vérifié. Ne pas faire du gate terminal avant archive/rapport une tâche circulaire.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B45-SL01 — Préparer les quatre artefacts cohérents, Why/What Changes requis, delta MODIFIED B11 verbatim sans norme nouvelle ; strict précode sans issue.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tasks — add-bulk-inbox-receipt-persistence-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B45-SL02 — Implémenter record/repository, import minimal models.py et migration0008 dépendant de0007 réversible : huit clés exactes, PK technique hors huit, unique consumer_reference/event_id, insert-only/alias/atomic, savepoint INSERT puis lecture, Duplicate/Divergence et rollback propriétaire capturé.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tasks — add-bulk-inbox-receipt-persistence-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B45-SL03 — Implémenter unittest offline : vrais imports sous gardes, types hostiles avant comportement/I/O, sans écho, capture et exports owned/frozen, save/full_clean exclude/déféré, métadonnées/migration sans DB ; aucune preuve SQL par mock miroir.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tasks — add-bulk-inbox-receipt-persistence-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B45-SL04 — Implémenter harness PostgreSQL isolé : clé composée/version/sha/consumer indépendant, co-transaction avec effet synthétique et JobRecord existant, refus capturé rollback, race deux bloqués/un gagnant/connexions fermées, visibilité inflight non ack, forward/reverse0008 seule/public et dix tables stables/cleanup strict.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tasks — add-bulk-inbox-receipt-persistence-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B45-SL05 — Compiler les six sources, exécuter unittest et PG réels autorisés puis régressions pertinentes avec outils DEVOPS ; strict ciblé sans issue et global comparé aux trois WARNING historiques exacts.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tasks — add-bulk-inbox-receipt-persistence-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B45-SL06 — Accepter sur preuves : huit clés sans ajout/default, UTF-8/LF, fichiers ciblés seuls, canon/cadrages/purs/runtime/CommandIdempotency/EventEnvelope préservés, aucune autorité/receiver/provider ni B11 global déclaré.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tasks — add-bulk-inbox-receipt-persistence-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
