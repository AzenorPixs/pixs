# Conception des littéraux de chemins statiques

## Context

`_require_path` limite chaque segment à `A-Z a-z 0-9 - _`, sans point. Les tests historiques refusent `"."`, `".."`, `"a/./b"`, `"a/../b"`, `"a."`, `"a..b/"`. Les littéraux construits `index.html`, `assets/index-HASH.js`, `assets/index-HASH.css` exigent des points internes. La norme n'impose aucune grammaire de chemin.

## Goals / Non-Goals

But : admettre uniquement des littéraux explicites avec points internes. Non-buts : aucun wildcard, converter, segment dot, chemin caché, traversal, URL distribuée, assertion readiness/startup/P0, enveloppe API.

## Decisions

- Règle point : chaque segment non vide conserve `A-Z a-z 0-9 - _` plus `.` seulement si le segment ne commence ni ne finit par `.`, ne contient pas `..`, et n'est ni `"."` ni `".."`.
- Exemples admis : `index.html`, `assets/index-Ab12.js`, `assets/index-Ab12.css`.
- Autres règles conservées : `".htaccess"`, `".a"`, `"a."`, `"a..b"`, `"a/./b"`, `"a/../b"`, `""` racine admise inchangée, `"*"`, `"<int:x>"`, `"%"`, `"\\"`, contrôles, espaces, `//`, slash initial.
- `public` bool exact, 403/404 fixes, `build_declared_urlpatterns` et catchall inchangés par ailleurs.
- En tests nouveaux seuls : déclarations explicites via `RouteDeclaration` + garde, `resolve` réel, client réel ; chemins synthétiques garde-compatibles, jamais présentés comme chemins publics de production.

## Files

`src/pixs/backend/http_route_guard.py`, `tests/unit/test_static_file_path_literals.py`, `tests/integration/test_static_file_path_literals_integration.py`, plus append seul `src/pixs/backend/README.md`.

## Validation

Baseline `tests/unit` et `tests/integration` complètes avant code ; après code, suites complètes ; unit sans Django configuré sauf sous-processus isolés ; intégration Django synthétique frais (`DEFAULT_CHARSET`, `ROOT_URLCONF`, `ALLOWED_HOSTS`, `INSTALLED_APPS=()`, `MIDDLEWARE=()`), aucun secret ni engine SQLite, `django.setup()`, `resolve` réel, client réel, `run_checks(databases=[])`, gardes `socket`/`psycopg` à zéro, UTF-8/LF, périmètre strict.

## Risks / Trade-offs

Aucune route utilisable en production issue de ce jalon. Tout assouplissement au-delà des points internes exigerait un change distinct.
