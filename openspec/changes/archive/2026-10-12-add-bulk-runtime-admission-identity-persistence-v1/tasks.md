## 1. Préparation et implémentation

- [x] 1.1 Préparer quatre artefacts révisés, delta MODIFIED B10 verbatim ; réussir strict change avant code.
- [x] 1.2 Implémenter `bulk_admission_identity_values.py` pur : 9 clés exactes, snapshot bytes strict recapturé octet pour octet, digest/version/bulk_type/idempotency_key cohérents, résolus distincts des références snapshot, expires_at UTC exact.
- [x] 1.3 Implémenter `bulk_admission_identity_record.py` : from_values/as_values/full_clean explicites, PK id locale + UniqueConstraint 4 colonnes, checks non-vide/version/variant/digest, sans unicité operation_id ni FK ni extension crypto.
- [x] 1.4 Implémenter `bulk_admission_identity_repository.py` : insert force_insert seul + get owned, sans update/purge/touch_expiry ni raw SQL hors contrat ; importer minimalement dans `models.py`.
- [x] 1.5 Implémenter migration réversible `0005` unique ; prouver forward/reverse 0005 isolé.
- [x] 1.6 Implémenter test unitaire pur : types hostiles, JSON non canonique/doublons/suivi/float, digest et cohérences, immutabilité owned.
- [x] 1.7 Implémenter test d'intégration en processus frais pur sous gardes fichiers/réseau/processus/environnement/DB/Core, sans effet.
- [x] 1.8 Implémenter test PG synthétique en schéma privé : roundtrip, contraintes SQL, concurrence d'unicité (un seul gagnant), rollback, reverse only 0005, tables existantes stables, connexions fermées, aucun secret affiché.
- [x] 1.9 Compiler séparément les Python touchés ; réussir tests ciblés et régressions Bulk/Kernel/Jobs applicables.
- [x] 1.10 Vérifier strict change sans issue, UTF-8/LF, canon/exports/sources préservés et acceptation complète.

## Procédure après preuves

Cocher seulement après preuves ; archive unique --skip-specs puis STATISTIQUES.md sous mandat distinct. Vérifier six sections et totaux avant retour. Aucune admission complète ni idempotence SQL annoncée au-delà de la persistance.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Procédure après preuves ».

### B38-SL01 — Préparer quatre artefacts révisés, delta MODIFIED B10 verbatim ; réussir strict change avant code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation et implémentation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL02 — Implémenter `bulk_admission_identity_values.py` pur : 9 clés exactes, snapshot bytes strict recapturé octet pour octet, digest/version/bulk_type/idempotency_key cohérents, résolus distincts des références snapshot, expires_at UTC exact.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation et implémentation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL03 — Implémenter `bulk_admission_identity_record.py` : from_values/as_values/full_clean explicites, PK id locale + UniqueConstraint 4 colonnes, checks non-vide/version/variant/digest, sans unicité operation_id ni FK ni extension crypto.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Préparation et implémentation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL04 — Implémenter `bulk_admission_identity_repository.py` : insert force_insert seul + get owned, sans update/purge/touch_expiry ni raw SQL hors contrat ; importer minimalement dans `models.py`.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Préparation et implémentation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL05 — Implémenter migration réversible `0005` unique ; prouver forward/reverse 0005 isolé.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Préparation et implémentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL06 — Implémenter test unitaire pur : types hostiles, JSON non canonique/doublons/suivi/float, digest et cohérences, immutabilité owned.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Préparation et implémentation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL07 — Implémenter test d'intégration en processus frais pur sous gardes fichiers/réseau/processus/environnement/DB/Core, sans effet.

- Ancien repère et tâche rattachée : tâche 1.7 ; section « 1. Préparation et implémentation », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL08 — Implémenter test PG synthétique en schéma privé : roundtrip, contraintes SQL, concurrence d'unicité (un seul gagnant), rollback, reverse only 0005, tables existantes stables, connexions fermées, aucun secret affiché.

- Ancien repère et tâche rattachée : tâche 1.8 ; section « 1. Préparation et implémentation », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL09 — Compiler séparément les Python touchés ; réussir tests ciblés et régressions Bulk/Kernel/Jobs applicables.

- Ancien repère et tâche rattachée : tâche 1.9 ; section « 1. Préparation et implémentation », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B38-SL10 — Vérifier strict change sans issue, UTF-8/LF, canon/exports/sources préservés et acceptation complète.

- Ancien repère et tâche rattachée : tâche 1.10 ; section « 1. Préparation et implémentation », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
