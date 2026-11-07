# Tasks — qualify-pdp-authentication-federation-vocabularies-v1

## Préparation
- [x] 1.1 Vérifier périmètre, NFDOC validé, réservation initiale version 101 historique, courante v115/ref12, NDFOC ISMP msg_13d7b8635001mK4f3vLNQU486t validé humain+CGPT, et métadonnée `.openspec.yaml` existante.
- [x] 1.2 Créer `proposal.md`, `design.md`, `tasks.md` et delta `MODIFIED` reprenant l'exigence `Assurances et faits du profil PDP minimal fermé v1` et ses deux scénarios existants mot pour mot, sans exigence ni scénario nouveau — cinq artefacts prouvés.
- [x] 1.3 Vérifier UTF-8/LF, delta identique au canon et validation stricte ciblée réussie — strict 1/1 exit 0 prouvé.
- [x] 1.4 Déclarer le jalon de préparation stable après preuves (`/ready`) — READY préparation conservé.

## Implémentation
- [x] 2.1 Obtenir l'extension atomique des ressources tests après libération concurrente et `/reconcile` sur référence fraîche — CISMP1 DELIVERED, ref12 reconcile v114 puis extend v115 sur quatre chemins.
- [x] 2.2 Créer le seul test unitaire `tests/unit/test_authentication_federation_vocab.py` : vocabulaires fermés, membres exacts, aller-retour, refus étrangers, absence sans défaut, cross-dimensions — write cismp3-5229b9b102ef4f prouvé.
- [x] 2.3 Créer le seul test d'intégration `tests/integration/test_authentication_federation_vocab_integration.py` : processus frais sous gardes IO, classes communes aux quatre consommateurs — write cismp3-fd06001ef99943 puis seule correction causale cismp3-c7cd2ec60d9f42.

## Vérifications
- [x] 3.1 Compilation réelle séparée des deux tests vers les `cfile` déclarés (`tests/unit/__pycache__/cismp3-authentication-federation.pyc` et équivalent intégration) — compilations séparées cismp3-e988b0f29db64d et cismp3-ab7629fec63a4c exit 0.
- [x] 3.2 Suite nouvelle dédiée via `unittest -B` avec `PYTHONPATH=src:tests/unit` (`/home/devops/datas/pixs/.venv/bin/python3`) — chemin effectif corrigé, 7 tests exit 0 cismp3-d99dcc50d6414d.
- [x] 3.3 Régressions PDP (`policy`, `decision`, `time`, `audit`), `mapping` et `IdentityAssurance` pertinentes — 96 régressions exit 0 cismp3-385248fa305745 conservées, 24 empreintes inchangées ; premier échec import cismp3-b2e4427a2df440 et prévol cismp3-fef311ebf24e44 préservés.
- [x] 3.4 Empreintes `authz` inchangées, UTF-8/LF des sources et artefacts, delta exact et revue de cohérence des cadrages — 7 sources production inchangées, UTF-8/LF vérifié, delta exact, cadrages concernés relus sans divergence nouvelle.
- [x] 3.5 Validation stricte du change puis globale standard via `/home/devops/.local/npm/bin/openspec validate` — strict ciblé 1/1 exit 0 cismp3-5b65726a9f4c49, global standard 79/79 exit 0 cismp3-56a7aa62d3894e ; strict global 77/79 exit 1 cismp3-01af2eceeba343 (métadonnée native Bash prt_13d8c6eda001DMP7IHa0gVFXKu exit 1), exactement 4 WARNING longueur bulk[6,10,13]/identity[4], zéro ERROR, aucun strict-success, norme longueur non modifiée conformément à CISMP.

## Archives et statistiques
Paragraphe hors tâches : protocole planifié conservé, après toutes preuves, mandats distincts sous exclusion intégration, archive avec `--skip-specs` puisque canon inchangé, rapport `STATISTIQUES.md` à six sections en UTF-8/LF avec totaux vérifiés, puis `gate/disarm/release` et retour à la sélection. Seules les 12 tâches ci-dessus sont prouvées ; archive et statistiques non revendiquées maintenant. Aucun test ni code à écrire ici.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### C82-SL01 — Vérifier périmètre, NFDOC validé, réservation initiale version 101 historique, courante v115/ref12, NDFOC ISMP msg_13d7b8635001mK4f3vLNQU486t validé humain+CGPT, et métadonnée `.openspec.yaml` existante.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « Préparation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL02 — Créer `proposal.md`, `design.md`, `tasks.md` et delta `MODIFIED` reprenant l'exigence `Assurances et faits du profil PDP minimal fermé v1` et ses deux scénarios existants mot pour mot, sans exigence ni scénario nouveau — cinq artefacts prouvés.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL03 — Vérifier UTF-8/LF, delta identique au canon et validation stricte ciblée réussie — strict 1/1 exit 0 prouvé.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « Préparation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL04 — Déclarer le jalon de préparation stable après preuves (`/ready`) — READY préparation conservé.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « Préparation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL05 — Obtenir l'extension atomique des ressources tests après libération concurrente et `/reconcile` sur référence fraîche — CISMP1 DELIVERED, ref12 reconcile v114 puis extend v115 sur quatre chemins.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « Implémentation », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL06 — Créer le seul test unitaire `tests/unit/test_authentication_federation_vocab.py` : vocabulaires fermés, membres exacts, aller-retour, refus étrangers, absence sans défaut, cross-dimensions — write cismp3-5229b9b102ef4f prouvé.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « Implémentation », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL07 — Créer le seul test d'intégration `tests/integration/test_authentication_federation_vocab_integration.py` : processus frais sous gardes IO, classes communes aux quatre consommateurs — write cismp3-fd06001ef99943 puis seule correction causale cismp3-c7cd2ec60d9f42.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « Implémentation », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL08 — Compilation réelle séparée des deux tests vers les `cfile` déclarés (`tests/unit/__pycache__/cismp3-authentication-federation.pyc` et équivalent intégration) — compilations séparées cismp3-e988b0f29db64d et cismp3-ab7629fec63a4c exit 0.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « Vérifications », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL09 — Suite nouvelle dédiée via `unittest -B` avec `PYTHONPATH=src:tests/unit` (`/home/devops/datas/pixs/.venv/bin/python3`) — chemin effectif corrigé, 7 tests exit 0 cismp3-d99dcc50d6414d.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « Vérifications », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL10 — Régressions PDP (`policy`, `decision`, `time`, `audit`), `mapping` et `IdentityAssurance` pertinentes — 96 régressions exit 0 cismp3-385248fa305745 conservées, 24 empreintes inchangées ; premier échec import cismp3-b2e4427a2df440 et prévol cismp3-fef311ebf24e44 préservés.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « Vérifications », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL11 — Empreintes `authz` inchangées, UTF-8/LF des sources et artefacts, delta exact et revue de cohérence des cadrages — 7 sources production inchangées, UTF-8/LF vérifié, delta exact, cadrages concernés relus sans divergence nouvelle.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « Vérifications », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C82-SL12 — Validation stricte du change puis globale standard via `/home/devops/.local/npm/bin/openspec validate` — strict ciblé 1/1 exit 0 cismp3-5b65726a9f4c49, global standard 79/79 exit 0 cismp3-56a7aa62d3894e ; strict global 77/79 exit 1 cismp3-01af2eceeba343 (métadonnée native Bash prt_13d8c6eda001DMP7IHa0gVFXKu exit 1), exactement 4 WARNING longueur bulk[6,10,13]/identity[4], zéro ERROR, aucun strict-success, norme longueur non modifiée conformément à CISMP.

- Ancien repère et tâche rattachée : tâche 3.5 ; section « Vérifications », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
