# Composition HTTP TEST locale conjointe

## Why

La spécification `initial-application-bootstrap` requiert des routes séparant santé/shell/API versionnée avec déclaration explicite, et un profil de test local vérifiant backend Django et shell TanStack ensemble (dépendances, adresse d'écoute, capacités absentes, cycle démarrage/arrêt), sans présentation production. Les handlers `liveness_view`, `build_shell_views`, `build_openapi_view` et la capacité enveloppe existent et prouvés isolément, mais aucune composition TEST conjointe réelle n'existe ; `RuntimeProfile` reste déclaratif sans activation. Il s'agit d'une absence technique implémentable, non d'une incohérence documentaire.

## What Changes

- Fournir `src/pixs/backend/local_test_composition.py` avec `build_local_test_urlpatterns(dist_root, plan, document, capacity, *, private_routes=(), unknown_ui_route=None)` : fabrique réelle retournant des urlpatterns Django via la garde (pas un descripteur pur, pas une sonde sans contrat).
- `capacity` = `RouteDeclaration` EXACT fourni `public=True` par le caller ; son chemin canonique doit figurer dans `paths` du document et sous le préfixe majeur ; `private_routes` = tuple exact de `RouteDeclaration` `False` explicites validées par la garde.
- Distribution TEST littérale documentée : `health/live` → liveness, racine `""` → `index.html`, assets exacts préchargés, `api_major_prefix(plan)` + `/openapi.json` → document, capacité caller ; noms de routes TEST déterministes uniques, collision refusée ; inconnu 404 et privées 403 via garde.
- `unknown_ui_route` : `None` ou littéral exact validé (grammaire garde, sans collision), mappé PUBLIC vers index en TEST seul ; défaut `None` (aucun fallback) ; jamais de fallback SPA universel ; le catchall garde reste 404.
- Helper `local_test_server(application, *, host, port)` contextmanager WSGI : ne configure jamais Django, aucun bind à l'import/fabrique ; application WSGI caller explicite, `host` exact `127.0.0.1` seul, `port` exact `int` `0..65535` (`0` éphémère tests non-navigateur, `5173` script Chromium) ; yield handle serveur/thread/adresse pour cleanup observable ; `serve_forever`, `shutdown`/`join`/`close` en `finally`, exceptions fixes `from None`, aucun kill de groupe de processus non borné.
- Capacités non prises en charge déclarées par cette composition TEST (activation Kernel/Core, P0, readiness, worker, scheduler, connexion PG), non comme absences machine non vérifiées ; aucun callback arbitraire attesté, aucune détection magique de secrets.
- Métadonnées `PROFILES`/déploiement/`PIXS_PROFILE` inchangées ; configuration caller TEST fraîche explicite `ENGINE` seul, apps/middleware vides ; contrat capacité `GET` cohérent avec le document publié ; rien métier distribué.
- Quatre nouveaux fichiers + append `README` seul ; `frontend/dist` réel préservé, aucun build/install/UI edit.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : jalon strict couvrant « Surface HTTP initiale minimale » et « Profil de test intégré isolé » (composition TEST conjointe seule), reprise normative inchangée.

## Impact

Aucune source frontend/garde/liveness/shell/document/façade/`manage.py` modifiée, aucune version/contrat/capacité nouvelle, aucune modification de norme. Activation P0/compose global non prouvés et non fabriqués. Readiness/startup/global/production non revendiqués.
