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
