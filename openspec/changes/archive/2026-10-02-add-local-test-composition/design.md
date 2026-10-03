# Conception de la composition TEST conjointe

## Context

Handlers prouvés : `liveness_view` (200 vide), `build_shell_views` (mapping fini préchargé), `build_openapi_view` (document figé), capacité enveloppe `build_success_response`. Harnais navigateur existant (`check_shell_adapter_browser.py`, WSGI thread `127.0.0.1:5173`, `ExitStack` PG, script UNMODIFIÉ, cleanup `finally`). `RuntimeProfile` : déclarations seules.

## Goals / Non-Goals

But : construire et faire tourner réellement la composition TEST conjointe (Client + WSGI loopback + navigateur UNMODIFIÉ). Non-buts : aucune URL de production distribuée, aucune activation P0/compose global, aucun readiness/startup, aucune PG/secrets/dépendance nouvelle, aucun build/install/UI edit.

## Decisions

- `build_local_test_urlpatterns(dist_root, plan, document, capacity, *, private_routes=(), unknown_ui_route=None)` : valide `capacity` (`RouteDeclaration` exact, `public is True`, chemin canonique `"/" + path` dans `paths` document et sous préfixe majeur) ; `private_routes` exact `tuple` d'éléments `RouteDeclaration` `public is False` ; `unknown_ui_route` `None` ou littéral exact validé ; construit vues via `build_shell_views`, `build_openapi_view`, `liveness_view` ; déclare `health/live` (liveness), `""` (index), assets exacts, `prefix + "/openapi.json"` (document), capacité, privées, éventuelle UI inconnue ; noms `test-health-live`, `test-shell-root`, `test-shell-<asset avec / remplacé par ->`, `test-api-document`, `test-api-<nom>`, `test-unknown-ui` ; retourne `list` urlpatterns via `build_declared_urlpatterns` (collisions/inconnues/403 gérées par garde).
- `local_test_server(application, *, host, port)` : `application` callable, `host == "127.0.0.1"` exact, `port` exact `int` (non `bool`) `0..65535` ; `make_server(host, port, application)` (`0` accepté éphémère par wsgiref) ; thread non-démon + `join` borné en `finally`, `shutdown`/`server_close`, `fileno() == -1` et thread joint vérifiables ; erreurs fixes `from None`.
- TESTS : fixtures `TemporaryDirectory(dir=frontend/.cache)` + vrai `dist` ; `resolve`+Client réels, `run_checks(databases=[])`, gardes PG/socket zéro en Client (navigateur : loopback ATTENDU, PG zéro seul, sans claim socket0) ; GET santé/shell/assets/document/capacité cohérente, 403 témoin, 404 inconnues ; serveur FD/thread et profil/processus navigateur nettoyés en `finally` même en échec.
- Diagnostics fixes, identifiants anglais ; caller TEST responsable de ses handlers.

## Files

`src/pixs/backend/local_test_composition.py`, `tests/unit/test_local_test_composition.py`, `tests/integration/test_local_test_composition_integration.py`, `tests/integration/check_local_composition_browser.py`, append seul `src/pixs/backend/README.md`.

## Validation

Unit sous-processus isolés (import pur, validation, hostiles, collisions, chemins document, port, hôte externe refusé) ; intégration Client joint ; harnais navigateur UNMODIFIÉ `5173` ; strict avant/après, AST 3.11, UTF-8/LF, périmètre strict.

## Risks / Trade-offs

Exposition `5173` limitée au harnais TEST. Aucune garantie au-delà du TEST : P0/readiness/production exigeraient des changes distincts.
