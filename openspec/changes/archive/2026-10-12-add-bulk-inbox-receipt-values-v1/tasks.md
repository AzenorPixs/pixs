## 1. Validateur et delta

- [x] 1.1 Implémenter `validate_bulk_inbox_receipt_values` et `capture_bulk_inbox_receipt_values` avec mapping huit clés exact, tous types et UTC avant helpers et valeurs, six `str` exactes, `causation_id` en `str | None`, `consumed_at` en `timezone.utc` identité, `str` runtime, SemVer complète, sha hex 64 minuscule, état `CONSUMED` seul, dataclass privée `frozen/slots` owned, `__all__` deux fonctions, listes fraîches `VALIDATE` triées sans écho, sans défaut, commit, preuve, déduplication, stockage, transaction, horloge, calcul, comparaison, catalogue, provenance, auth, FK, unicité ni cohérence entre champs.
- [x] 1.2 Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopié verbatim, sans annexe ni règle nouvelle.

## 2. Preuves

- [x] 2.1 Ajouter et réussir les unitaires huit clés, vrais hostiles sans hooks, SemVer, sha, UTC identité, état seul, fraîcheur des listes, sans écho.
- [x] 2.2 Prouver l isolation en processus frais sous gardes existantes réutilisées sans fichiers, réseau, processus, base ou Core concret.
- [x] 2.3 Compiler les 3 Python, réussir les régressions pures existantes y compris Outbox et préserver exports, sources et preuves précédentes par empreinte.
- [x] 2.4 Vérifier strict du change, UTF-8 et LF, cohérence et absence d écriture hors périmètre.

## Procedure apres preuves

Cocher seulement après leurs preuves. Archiver une seule fois avec `--skip-specs`, publier `STATISTIQUES.md` sous mandat distinct, vérifier ses six sections et totaux puis revenir à SELECTION sans fin globale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 1. Validateur et delta » ; « 2. Preuves » ; « Procedure apres preuves ».

### B35-SL01 — Implémenter `validate_bulk_inbox_receipt_values` et `capture_bulk_inbox_receipt_values` avec mapping huit clés exact, tous types et UTC avant helpers et valeurs, six `str` exactes, `causation_id` en `str | None`, `consumed_at` en `timezone.utc` identité, `str` runtime, SemVer complète, sha hex 64 minuscule, état `CONSUMED` seul, dataclass privée `frozen/slots` owned, `__all__` deux fonctions, listes fraîches `VALIDATE` triées sans écho, sans défaut, commit, preuve, déduplication, stockage, transaction, horloge, calcul, comparaison, catalogue, provenance, auth, FK, unicité ni cohérence entre champs.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Validateur et delta », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B35-SL02 — Fournir le delta `specs/events/spec.md` `MODIFIED` B11 recopié verbatim, sans annexe ni règle nouvelle.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Validateur et delta », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B35-SL03 — Ajouter et réussir les unitaires huit clés, vrais hostiles sans hooks, SemVer, sha, UTC identité, état seul, fraîcheur des listes, sans écho.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Preuves », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B35-SL04 — Prouver l isolation en processus frais sous gardes existantes réutilisées sans fichiers, réseau, processus, base ou Core concret.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Preuves », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B35-SL05 — Compiler les 3 Python, réussir les régressions pures existantes y compris Outbox et préserver exports, sources et preuves précédentes par empreinte.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Preuves », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B35-SL06 — Vérifier strict du change, UTF-8 et LF, cohérence et absence d écriture hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Preuves », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
