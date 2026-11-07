## 1. Validateur et delta

- [x] 1.1 Implementer `validate_bulk_outbox_publication_values` et `capture_bulk_outbox_publication_values` avec mapping 12 cles exact, deux phases types avant comportement, `str` runtime, `attempt_count >= 0`, `sequence_index/revision >= 1`, SemVer complete, UTC `timezone.utc` identite, seuls couplages `lease_owner/lease_expires_at`, `RETRYING/next_attempt_at`, `PUBLISHED/published_at`, dataclass privee `frozen/slots` owned, sans defaut, catalogue, horloge, comparaison, politique, FK, unicite, allocation, publication, retry, CAS, SQL ni preuve serveur.
- [x] 1.2 Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopie verbatim, sans annexe ni regle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et reussir les unitaires 12 cles, hostiles sans hooks, ints, SemVer, UTC identite, couplages fermes seuls, fraicheur des listes, sans echo.
- [x] 2.2 Prouver l isolation dans un processus frais sous gardes existantes reutilisees sans fichiers/reseau/processus/base/Core concret.
- [x] 2.3 Compiler les 3 Python, reussir les regressions existantes et preserver exports, sources et preuves precedentes par empreinte.
- [x] 2.4 Verifier strict du change, UTF-8/LF, coherence et absence d ecriture hors perimetre.

## Procedure apres preuves

Cocher seulement apres leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, verifier ses six sections et totaux puis revenir a SELECTION sans fin globale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 1. Validateur et delta » ; « 2. Preuves » ; « Procedure apres preuves ».

### B36-SL01 — Implementer `validate_bulk_outbox_publication_values` et `capture_bulk_outbox_publication_values` avec mapping 12 cles exact, deux phases types avant comportement, `str` runtime, `attempt_count >= 0`, `sequence_index/revision >= 1`, SemVer complete, UTC `timezone.utc` identite, seuls couplages `lease_owner/lease_expires_at`, `RETRYING/next_attempt_at`, `PUBLISHED/published_at`, dataclass privee `frozen/slots` owned, sans defaut, catalogue, horloge, comparaison, politique, FK, unicite, allocation, publication, retry, CAS, SQL ni preuve serveur.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Validateur et delta », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B36-SL02 — Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopie verbatim, sans annexe ni regle nouvelle.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Validateur et delta », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B36-SL03 — Ajouter et reussir les unitaires 12 cles, hostiles sans hooks, ints, SemVer, UTC identite, couplages fermes seuls, fraicheur des listes, sans echo.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Preuves », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B36-SL04 — Prouver l isolation dans un processus frais sous gardes existantes reutilisees sans fichiers/reseau/processus/base/Core concret.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Preuves », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B36-SL05 — Compiler les 3 Python, reussir les regressions existantes et preserver exports, sources et preuves precedentes par empreinte.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Preuves », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B36-SL06 — Verifier strict du change, UTF-8/LF, coherence et absence d ecriture hors perimetre.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Preuves », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
