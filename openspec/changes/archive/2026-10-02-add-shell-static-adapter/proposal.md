# Adaptateur statique borné du shell construit

## Why

La spécification `initial-application-bootstrap` requiert un shell TanStack construit séparément et servi par la composition de développement déclarée, ne consommant que la surface HTTP publique déclarée. Le shell `frontend/dist/index.html` + `assets/` est construit, la garde accepte désormais les littéraux `js`/`css`, mais aucune vue ne sert réellement ces octets. Il s'agit d'une absence technique implémentable, non d'une incohérence documentaire.

## What Changes

- Fournir `src/pixs/backend/shell_adapter.py` avec `build_shell_views(dist_root)` : `dist_root` argument EXPLICITE de racine de build (exact `str` ou `Path` sûr, portable) ; aucun chemin absolu projet ni `frontend/dist` codé dans la bibliothèque.
- Sous cette racine seule : lire uniquement `index.html` et des assets `js`/`css` réguliers, non cachés, sans symlink ; chaque lecture bornée `max 1MiB`, `max 64 fichiers`, budget total `8MiB` documentés comme choix internes ; mapping FINI `filename -> handler` (clé HTML `index.html`), octets préchargés et figés ; aucun lecteur HTTP dynamique, aucun catchall nouveau, aucune lecture à chaque requête.
- `GET` → 200 corps exact préchargé ; `HEAD` → 200 sans corps avec Content-Length identique au GET, autre méthode → 405 vide avec `Allow: GET, HEAD` ; MIME exact (`text/html; charset=utf-8`, `application/javascript`, `text/css`) et `Cache-Control: no-store` ; mauvaise construction → `ShellAdapterError` fixe sans chemin brut ni chaîne.
- Import module pur (aucun import Django/lecture FS à l'import, accès `dist` seulement dans la fabrique) ; le caller runtime déclare lui-même `public=True/False` via la garde ; aucune URL publique distribuée.
- Tests synthétiques sous `frontend/.cache/<dir explicite>` seul (jamais `/tmp`/env/secret) + vrai `dist` construit après `npm run build` existant ; harness navigateur `tests/integration/check_shell_adapter_browser.py` (hors discovery) : serveur WSGI Django thread `127.0.0.1:5173` seul, `frontend/tests/browser-check.mjs` UNMODIFIÉ, `finally` cleanup prouvé ; route cliente introuvable `route-inconnue-xyz` déclarée PUBLIQUE vers index en TEST seul, toutes autres inconnues 404.
- Gardes PG zéro partout ; navigateur : loopback test autorisée, externe bloqué par le script (aucun claim `socket 0` global) ; serveur + navigateur en une seule commande harness CAB ; pas de Vite.
- Quatre fichiers code nécessaires + append `README` seul : `src/pixs/backend/shell_adapter.py`, `tests/unit/test_shell_adapter.py`, `tests/integration/test_shell_adapter_integration.py`, `tests/integration/check_shell_adapter_browser.py`, append `src/pixs/backend/README.md`.
- Commandes complètes : voir design.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : jalon strict de l'exigence existante « Shell TanStack initial intégré », sous-ensemble adaptateur + preuve Client/navigateur seuls, reprise normative inchangée.

## Impact

Aucune source frontend/garde/liveness/façade/`manage.py` modifiée, aucune version/contrat/capacité nouvelle, aucune modification de norme. `frontend/dist` seul régénérable sous mandat build. Shell servi, API publiée, composition P0 qualifiée, readiness/startup/P0/global et cycle CISMP restent non revendiqués au-delà de ce jalon.
