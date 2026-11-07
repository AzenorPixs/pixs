## 1. Validateur et delta

- [x] 1.1 Implémenter `validate_bulk_event_envelope_values` avec mapping 13 clés exact, types exacts puis valeurs, opaques sans NUL, `kind`, SemVer, UTC aware, garde `None` par `non_tenant_authorized`, payload via `validate_json_value` sans défaut, sans capture/snapshot/port/ORM/horloge.
- [x] 1.2 Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopié verbatim, sans annexe ni règle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et réussir les unitaires JSON bornés, hostiles, UTC, garde `None`, fraîcheur des listes, sans écho.
- [x] 2.2 Prouver l'isolation dans un processus frais sous gardes positives sans fichiers/réseau/processus/base/Core concret.
- [x] 2.3 Compiler les 3 Python, réussir les régressions existantes et préserver exports, sources et preuves précédentes par empreinte.
- [x] 2.4 Vérifier strict du change, UTF-8/LF, cohérence et absence d'écriture hors périmètre.

## Procédure après preuves

Cocher seulement après leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, vérifier ses six sections et totaux puis revenir à SÉLECTION sans fin globale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 1. Validateur et delta » ; « 2. Preuves » ; « Procédure après preuves ».

### B33-SL01 — Implémenter `validate_bulk_event_envelope_values` avec mapping 13 clés exact, types exacts puis valeurs, opaques sans NUL, `kind`, SemVer, UTC aware, garde `None` par `non_tenant_authorized`, payload via `validate_json_value` sans défaut, sans capture/snapshot/port/ORM/horloge.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Validateur et delta », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B33-SL02 — Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopié verbatim, sans annexe ni règle nouvelle.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Validateur et delta », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B33-SL03 — Ajouter et réussir les unitaires JSON bornés, hostiles, UTC, garde `None`, fraîcheur des listes, sans écho.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Preuves », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B33-SL04 — Prouver l'isolation dans un processus frais sous gardes positives sans fichiers/réseau/processus/base/Core concret.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Preuves », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B33-SL05 — Compiler les 3 Python, réussir les régressions existantes et préserver exports, sources et preuves précédentes par empreinte.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Preuves », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B33-SL06 — Vérifier strict du change, UTF-8/LF, cohérence et absence d'écriture hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Preuves », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
