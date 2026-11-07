## 1. Préparation et implémentation

- [x] 1.1 Préparer quatre artefacts révisés, delta MODIFIED B10 verbatim ; réussir strict change avant code.
- [x] 1.2 Implémenter `bulk_command_idempotency_record.py` + `bulk_command_idempotency_repository.py` + import minimal `models.py` + migration réversible `0006` : 12 champs explicites, PK locale hors 12 clés, uniques 4 colonnes, insertion privée dans unit seul, finalize exige jeton actif même thread/alias, atomic savepoint=False + latched + set_rollback.
- [x] 1.3 Implémenter test unitaire pur unittest : types hostiles/noecho avant I/O, import inerte, capture/copies owned et métadonnées/migration sans DB ; rejeu/divergence/CAS comportementaux prouvés en PG réel, sans mocks miroirs.
- [x] 1.4 Implémenter test d'intégration PG isolé unittest : autodetection + forward/reverse 0006 seule, unique clé/race, replay stable/divergent même clé digest ET serializer, rollback technique et sortie non finalisée non committable même après capture, co-transaction synthétique/progression/checkpoint, nettoyage/conns/public stables.
- [x] 1.5 Exécuter `.venv/bin/python3` pour compilation et tests cibles, gardes, puis régressions pertinentes nommées après inspection du code touché avec le mécanisme unittest du projet ; validations OpenSpec avec exécutable DEVOPS.
- [x] 1.6 Vérifier strict change sans issue, UTF-8/LF, périmètre 6 sources, delta verbatim, canon/exports préservés et acceptation complète.

## Procédure après preuves

Sur preuves des six tâches, les cocher. Puis archive unique `--skip-specs`, rapport distinct six sections vérifié, retour SÉLECTION. Ne pas cocher archive/STATISTIQUES avant leur preuve.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Procédure après preuves ».

### B31-SL01 — Préparer quatre artefacts révisés, delta MODIFIED B10 verbatim ; réussir strict change avant code.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation et implémentation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B31-SL02 — Implémenter `bulk_command_idempotency_record.py` + `bulk_command_idempotency_repository.py` + import minimal `models.py` + migration réversible `0006` : 12 champs explicites, PK locale hors 12 clés, uniques 4 colonnes, insertion privée dans unit seul, finalize exige jeton actif même thread/alias, atomic savepoint=False + latched + set_rollback.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation et implémentation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B31-SL03 — Implémenter test unitaire pur unittest : types hostiles/noecho avant I/O, import inerte, capture/copies owned et métadonnées/migration sans DB ; rejeu/divergence/CAS comportementaux prouvés en PG réel, sans mocks miroirs.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Préparation et implémentation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B31-SL04 — Implémenter test d'intégration PG isolé unittest : autodetection + forward/reverse 0006 seule, unique clé/race, replay stable/divergent même clé digest ET serializer, rollback technique et sortie non finalisée non committable même après capture, co-transaction synthétique/progression/checkpoint, nettoyage/conns/public stables.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Préparation et implémentation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B31-SL05 — Exécuter `.venv/bin/python3` pour compilation et tests cibles, gardes, puis régressions pertinentes nommées après inspection du code touché avec le mécanisme unittest du projet ; validations OpenSpec avec exécutable DEVOPS.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Préparation et implémentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B31-SL06 — Vérifier strict change sans issue, UTF-8/LF, périmètre 6 sources, delta verbatim, canon/exports préservés et acceptation complète.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Préparation et implémentation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
