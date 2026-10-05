# Garde de déclaration explicite des routes HTTP

## Why

La spécification `initial-application-bootstrap` requiert une surface HTTP initiale à routes publiques explicitement déclarées et refus fermé du non déclaré, alors que seul l’outillage de réponses existe sans frontière de déclaration/refus vérifiable.

## What Changes

- Fournir une fabrique Django `build_declared_urlpatterns` recevant explicitement une séquence de déclarations exactes, sans route concrète distribuée ni placeholder santé/shell/API.
- Exécuter seuls les handlers des routes `public=True` ; refuser `public=False` en 403 texte fixe sans appeler le handler ; ajouter un catchall final 404 texte fixe sans echo.
- Refuser déclarations invalides et collisions par exception stable sans echo.
- Tester le véritable `resolve` et client/handler Django uniquement en sous-processus synthétiques isolés, avec gardes DB/socket.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : premier jalon strict de l’exigence existante « Surface HTTP initiale minimale », sous-ensemble déclaration public/refus non-public/inconnu, reprise normative inchangée.

## Impact

Trois fichiers hors artefacts : `src/pixs/backend/http_route_guard.py`, `tests/unit/test_initial_http_route_guard.py`, `tests/integration/test_initial_http_route_guard_integration.py`. Aucune facade existante modifiée, aucun nouveau contrat/version/capacité, aucun `ApiContractPlan` inventé ou contourné, aucun `manage.py`/`frontend/` modifié, aucun serveur/DB/SQLite, aucun secret, aucun Git, aucun déploiement. Surface complète, santé, shell, API publiée et profil conjoint restent non satisfaits.
