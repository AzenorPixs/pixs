# Conception de l'adaptateur shell

## Context

`frontend/dist/index.html`, `assets/index-Big655uI.js`, `assets/index-CEeMJxYe.css` construits. Garde compatible points internes. `browser-check.mjs` exige `http://127.0.0.1:5173` codé et `/route-inconnue-xyz` pour UI introuvable. Aucune vue statique en `src`.

## Goals / Non-Goals

But : servir réellement les octets construits via handlers préchargés et le prouver par Client + navigateur UNMODIFIÉ. Non-buts : aucune URL distribuée, aucune composition P0 ni composition globale de développement ou production qualifiée ; composition HTTP de TEST seule exécutée, aucun readiness/startup/P0, aucune API, aucun Vite, aucune PG/secrets/dépendance nouvelle.

## Decisions

- `build_shell_views(dist_root)` : `dist_root` exact `str` non vide ou `Path` ; résolu, doit être un répertoire ; lecture limitée à `index.html` + `assets/*.js|css` réguliers (`is_file`, non symlink, non caché, taille `<= 1MiB`, `<= 64` fichiers, total `<= 8MiB`) ; sinon `ShellAdapterError("Invalid shell distribution.")` fixe.
- Retourne mapping fini `{ "index.html": handler, "assets/<nom>": handler }` ; handlers ferment sur octets figés + MIME exact ; `GET` 200 corps exact, `HEAD` 200 sans corps avec Content-Length identique au GET, autres 405 vide + `Allow` ; `Cache-Control: no-store` partout.
- Tests unitaires : fixtures synthétiques dans `TemporaryDirectory(dir=frontend/.cache, prefix=shell-fixtures-)` + cas `dist` réel optionnel après build ; traversal/caché/symlink/sur-budget refusés.
- Tests intégration : `build_shell_views` sur vrai `dist` + `build_declared_urlpatterns` (`""`→index PUBLIC, assets→PUBLIC, témoin private→403, `route-inconnue-xyz`→index PUBLIC en TEST seul, autres→404), `resolve`+Client réels, `run_checks(databases=[])`, gardes `psycopg` zéro, settings `ENGINE` seul.
- Harness `check_shell_adapter_browser.py` : thread WSGI `127.0.0.1:5173`, attente disponibilité bornée, `node frontend/tests/browser-check.mjs` UNMODIFIÉ avec `PATH` incluant node, `finally` shutdown/join/rm éphémère même en échec ; loopback seule autorisée.
- URLs jamais distribuées par la bibliothèque ; caller TEST déclare explicitement.

## Files

`src/pixs/backend/shell_adapter.py`, `tests/unit/test_shell_adapter.py`, `tests/integration/test_shell_adapter_integration.py`, `tests/integration/check_shell_adapter_browser.py`, append seul `src/pixs/backend/README.md`.

## Validation

Commandes complètes, chacune sous mandat CAB unitaire distinct, sans `&&`/`;` :
- `/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend run build`
- `/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/home/devops/datas/pixs/frontend/.cache /home/devops/datas/pixs/.venv/bin/python -B -m unittest discover -s /home/devops/datas/pixs/tests/unit`
- `/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/home/devops/datas/pixs/frontend/.cache /home/devops/datas/pixs/.venv/bin/python -B -m unittest discover -s /home/devops/datas/pixs/tests/integration`
- `/usr/bin/env -i PATH=/usr/bin:/bin:/home/devops/node/current/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/home/devops/datas/pixs/frontend/.cache /home/devops/datas/pixs/.venv/bin/python -B /home/devops/datas/pixs/tests/integration/check_shell_adapter_browser.py`
OpenSpec strict avant/après, AST 3.11, UTF-8/LF, périmètre strict. Matrice : DEVOPS (outils/ports), README racine (générique sans grammaire chemin).

## Risks / Trade-offs

Préchargement mémoire borné 8MiB préféré à la relecture par requête (aucune relecture filesystem par requête ; aucune attestation d’atomicité de la construction du dist). Toute mise en cache navigateur neutralisée par `no-store`. Exposition 5173 limitée au harnais TEST.
