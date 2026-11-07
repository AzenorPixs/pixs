# Tasks add-bulk-outbox-initial-persistence-v1

- [x] 1. Artefacts stricts pre-code : proposal/design/tasks/delta ci-dessus relus, 12 noms et 13+2 colonnes figes, 6 fichiers cibles seuls, aucune ecriture hors perimetre.
- [x] 2. Production 4 fichiers : record 13 colonnes + counter interne 2 colonnes meme module + repository owner-atomique (from_values 12, allocation runtime, savepoint 23505 PK scope, rowlock exact, rollback propage) + migration 0011 apres 0010 + wiring models sans Envelope change.
- [x] 3. Tests unitaires gardes : 12 mapping exact, 11 source obligatoires sans defaut, revision positive conservee, PENDING/attempt0 explicites, types stricts/capacites, couplages lease/RETRYING/PUBLISHED, hostile bool/eq/hash/str, frozen owned, catalogue failure tuple/frozenset.
- [x] 4. Integration PG isole : 2 threads meme scope unique vs scopes independants, owner rollback join, type caps, get initial capture pure, FK event unique immuable, 15 tables finales, reversal 0011 seule, public readiness sans fake publish, cleanup conns, UTF-8/LF.
- [x] 5. Compilation et regressions 6 sources : py_compile, suites unitaires concernees, non-regression Envelope/runtime/purs, strict cible precode/final sans issue, global compare aux trois WARNING historiques exacts sans nouvelle issue, norme preservee, aucun secret.
- [x] 6. Acceptance scope : 12/13/2 colonnes, FK unique, sequence runtime seule, PENDING/attempt0, exclusions publisher/CAS/clock/reset respectees, UTF-8/LF, seuls fichiers attendus modifies et autres sources/canon preserves.

Apres preuves des six taches : coches sous mandat distinct, archivage unique --skip-specs puis STATISTIQUES.md sous mandat distinct, hors de ces six taches et sans condition circulaire.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B46-SL01 — Artefacts stricts pre-code : proposal/design/tasks/delta ci-dessus relus, 12 noms et 13+2 colonnes figes, 6 fichiers cibles seuls, aucune ecriture hors perimetre.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tasks add-bulk-outbox-initial-persistence-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B46-SL02 — Production 4 fichiers : record 13 colonnes + counter interne 2 colonnes meme module + repository owner-atomique (from_values 12, allocation runtime, savepoint 23505 PK scope, rowlock exact, rollback propage) + migration 0011 apres 0010 + wiring models sans Envelope change.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tasks add-bulk-outbox-initial-persistence-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B46-SL03 — Tests unitaires gardes : 12 mapping exact, 11 source obligatoires sans defaut, revision positive conservee, PENDING/attempt0 explicites, types stricts/capacites, couplages lease/RETRYING/PUBLISHED, hostile bool/eq/hash/str, frozen owned, catalogue failure tuple/frozenset.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tasks add-bulk-outbox-initial-persistence-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B46-SL04 — Integration PG isole : 2 threads meme scope unique vs scopes independants, owner rollback join, type caps, get initial capture pure, FK event unique immuable, 15 tables finales, reversal 0011 seule, public readiness sans fake publish, cleanup conns, UTF-8/LF.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tasks add-bulk-outbox-initial-persistence-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B46-SL05 — Compilation et regressions 6 sources : py_compile, suites unitaires concernees, non-regression Envelope/runtime/purs, strict cible precode/final sans issue, global compare aux trois WARNING historiques exacts sans nouvelle issue, norme preservee, aucun secret.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tasks add-bulk-outbox-initial-persistence-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B46-SL06 — Acceptance scope : 12/13/2 colonnes, FK unique, sequence runtime seule, PENDING/attempt0, exclusions publisher/CAS/clock/reset respectees, UTF-8/LF, seuls fichiers attendus modifies et autres sources/canon preserves.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tasks add-bulk-outbox-initial-persistence-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
