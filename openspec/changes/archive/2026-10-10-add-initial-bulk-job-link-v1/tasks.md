# Tâches — add-initial-bulk-job-link-v1

- [x] 1. Vérifier le delta MODIFIED exact des deux exigences canoniques, l'unicité du change actif et UTF-8/LF.
- [x] 2. Créer le module interne BulkJobLink immuable à deux références explicites et son validateur pur selon D2–D5 ; imports dataclasses/diagnostics seuls, façade inchangée.
- [x] 3. Créer les tests unitaires comportementaux : conservation opaque, égalité refusée, types/objets hostiles sans hooks, diagnostics statiques triés/dédupliqués sans écho, immuabilité et champs obligatoires.
- [x] 4. Créer le test en processus frais isolé, sous gardes d'effets avec contrôles positifs et compteurs nuls pendant import/validation.
- [x] 5. Compiler séparément les trois nouveaux fichiers ; exécuter les tests ciblés et les régressions applicables de pureté/façades et vocabulaires Job/Notification.
- [x] 6. Valider le change OpenSpec avant et après code : aucune ERROR, seul avertissement de longueur déjà accepté.
- [x] 7. Relire les trois fichiers et les artefacts ; vérifier les empreintes des sources/cadrages/canon existants, l'absence d'écriture hors périmètre et l'acceptation complète sans inspection Git.

L'archivage --skip-specs et la publication de STATISTIQUES.md restent des phases ultérieures distinctes, autorisées après preuves ; aucune case ne les anticipe.

Preuves vérifiées par CGPT : trois compilations exit 0 ; 9 tests ciblés dont processus frais et 20 régressions (29 réussites), exits 0 ; change validé avant/après 1/1 sans issue ; 96 empreintes de référence préservées, trois sources relues, UTF-8/LF et delta canon exact. Aucun archivage ni rapport anticipé.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B17-SL01 — Vérifier le delta MODIFIED exact des deux exigences canoniques, l'unicité du change actif et UTF-8/LF.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B17-SL02 — Créer le module interne BulkJobLink immuable à deux références explicites et son validateur pur selon D2–D5 ; imports dataclasses/diagnostics seuls, façade inchangée.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B17-SL03 — Créer les tests unitaires comportementaux : conservation opaque, égalité refusée, types/objets hostiles sans hooks, diagnostics statiques triés/dédupliqués sans écho, immuabilité et champs obligatoires.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B17-SL04 — Créer le test en processus frais isolé, sous gardes d'effets avec contrôles positifs et compteurs nuls pendant import/validation.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B17-SL05 — Compiler séparément les trois nouveaux fichiers ; exécuter les tests ciblés et les régressions applicables de pureté/façades et vocabulaires Job/Notification.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B17-SL06 — Valider le change OpenSpec avant et après code : aucune ERROR, seul avertissement de longueur déjà accepté.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B17-SL07 — Relire les trois fichiers et les artefacts ; vérifier les empreintes des sources/cadrages/canon existants, l'absence d'écriture hors périmètre et l'acceptation complète sans inspection Git.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — add-initial-bulk-job-link-v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
