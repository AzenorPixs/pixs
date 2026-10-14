# Tasks — qualify-pdp-authentication-federation-vocabularies-v1

## Préparation
- [ ] 1.1 Vérifier périmètre, NFDOC validé, réservation version 101 et métadonnée `.openspec.yaml`.
- [ ] 1.2 Créer `proposal.md`, `design.md`, `tasks.md` et delta `MODIFIED` reprenant l'exigence `Assurances et faits du profil PDP minimal fermé v1` et ses deux scénarios existants mot pour mot, sans exigence ni scénario nouveau.
- [ ] 1.3 Vérifier UTF-8/LF, delta identique au canon et validation stricte ciblée réussie.
- [ ] 1.4 Déclarer le jalon de préparation stable après preuves (`/ready`).

## Implémentation
- [ ] 2.1 Obtenir l'extension atomique des ressources tests après libération concurrente et `/reconcile` sur référence fraîche.
- [ ] 2.2 Créer le seul test unitaire `tests/unit/test_authentication_federation_vocab.py` : vocabulaires fermés, membres exacts, aller-retour, refus étrangers, absence sans défaut, cross-dimensions.
- [ ] 2.3 Créer le seul test d'intégration `tests/integration/test_authentication_federation_vocab_integration.py` : processus frais sous gardes IO, classes communes aux quatre consommateurs.

## Vérifications
- [ ] 3.1 Compilation réelle séparée des deux tests vers les `cfile` déclarés (`tests/unit/__pycache__/cismp3-authentication-federation.pyc` et équivalent intégration).
- [ ] 3.2 Suite nouvelle dédiée via `unittest -B` avec `PYTHONPATH=src` (`/home/devops/datas/pixs/.venv/bin/python3`).
- [ ] 3.3 Régressions PDP (`policy`, `decision`, `time`, `audit`), `mapping` et `IdentityAssurance` pertinentes.
- [ ] 3.4 Empreintes `authz` inchangées, UTF-8/LF des sources et artefacts, delta exact et revue de cohérence des cadrages.
- [ ] 3.5 Validation stricte du change puis globale standard via `/home/devops/.local/npm/bin/openspec validate` ; strict global : tracer code natif et avertissements historiques sans prétendre succès si `exit 1`.

## Archives et statistiques
Paragraphe hors tâches : après toutes preuves, mandats distincts sous exclusion intégration, archive avec `--skip-specs` puisque canon inchangé, rapport `STATISTIQUES.md` à six sections en UTF-8/LF avec totaux vérifiés, puis `gate/disarm/release` et retour à la sélection. Aucun test ni code à écrire ici, aucune tâche cochée maintenant.
