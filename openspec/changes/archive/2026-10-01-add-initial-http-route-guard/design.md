# Conception de la garde de routes

## Context

Les fabriques `build_success_response` et `build_infrastructure_response` existent avec tests isolés. Aucune frontière déclarative des routes n’existe. La norme impose déclaration explicite du public et refus du reste sans information sensible, sans simuler métier/autorisation/identité.

## Goals / Non-Goals

But : démontrer uniquement la frontière déclaration/refus dans Django existant. Non-buts : aucune route concrète distribuée, aucun placeholder, aucune réponse API concrète, aucun contrat/version nouveau, aucune santé/shell/API publiée, aucun profil conjoint, aucune activation/publication par la fabrique seule.

## Decisions

- Déclaration exacte exigée : `path` relatif strict sans regex/converters/glob/fragment/query/catchall, sans slash initial ambigu ; `name` unique non vide ; `handler` callable, sans invocation pendant validation ; `public` bool exact obligatoire. Tout écart lève `HttpRouteGuardError` stable sans echo de valeur.
- Collision de `path` ou `name`, ordre conservé, doublon refusé. Ordre d’entrée préservé avant catchall.
- Seul `public=True` enveloppé vers son handler. `public=False` enveloppé vers refus 403 `HttpResponse` texte fixe `Route non publique.`, sans appel handler ni prétention d’authentification/autorisation.
- Catchall final systématique vers 404 texte fixe `Route inconnue.`, sans echo du chemin, secret ou trace.
- Aucun import/config Django au simple import du module ; imports `django.http`/`django.urls` locaux dans la fabrique uniquement ; aucun `settings.configure`, `django.setup`, serveur ou I/O dans le code.
- Handlers externes et leur conformité HTTP/enveloppes restent hors portée ; en test seul, usage permis de `build_success_response` existant et descripteur synthétique sans attestation de publication.

## Files

`src/pixs/backend/http_route_guard.py`, `tests/unit/test_initial_http_route_guard.py`, `tests/integration/test_initial_http_route_guard_integration.py`.

## Validation

OpenSpec strict avant code et finale ; unit sans Django configuré sauf sous-processus isolés ; intégration avec réglages synthétiques explicites en sous-processus frais (`DEFAULT_CHARSET`, `ROOT_URLCONF`, `ALLOWED_HOSTS`, `INSTALLED_APPS=()`, `MIDDLEWARE=()`), aucun secret ni engine SQLite, `django.setup()`, `resolve` réel, test client réel, `run_checks(databases=[])`, gardes `socket`/`psycopg` à zéro appel, espion `public=False` jamais appelé, entrées hostiles/collisions/ordre testés, UTF-8/LF, périmètre strict.

## Risks / Trade-offs

Aucune route utilisable en production issue de ce jalon. Le choix 403/404 textes fixes évite toute fausse sémantique métier. Toute surface concrète exigera un change distinct.
