# Conception de la vue liveness

## Context

La fabrique `build_declared_urlpatterns` existe avec refus 403/404 fixes sans echo. Les contrôles `check_template`/`inspect_roles` restent non prêts sans service. Le shell `frontend/src/main.js` ne consomme aucune API. Aucune vue liveness réelle n'existe. Les normes imposent liveness = processus capable de répondre, distincte de readiness/startup, sondes rapides/bornées/sans mutation/sans secret, zéro dépendance métier obligatoire.

## Goals / Non-Goals

But : démontrer uniquement qu'une requête est effectivement traitée par Django, sans toucher aucune dépendance. Non-buts : aucune route publique distribuée, aucune assertion readiness/startup/P0/composition/persistance, aucune réponse API/enveloppe, aucun contrat/version nouveau, aucune disponibilité globale, aucun diagnostic détaillé.

## Decisions

- Identifiants anglais seuls : `liveness_view`, `LivenessError` si nécessaire, constantes `LIVENESS_BODY` vide, messages fixes sans valeur.
- Validation standard minimale : exiger un objet requête avec attribut `method` de type exact `str` ; ne pas exiger `type(request) is HttpRequest`, afin d'accepter `WSGIRequest` et `ASGIRequest` réels utilisés par Django ; aucune autre condition sur la requête.
- `method == "GET"` ou `method == "HEAD"` → `HttpResponse` corps vide `b""`, statut 200, `content_type="text/plain; charset=utf-8"`.
- Autre méthode exacte → `HttpResponse` corps vide, statut 405, même `content_type`, header `Allow: GET, HEAD`.
- Toutes les réponses portent `Cache-Control: no-store` ; aucun signal de vivacité issu d’un cache ne doit être confondu avec cette requête réellement traitée.
- Aucun corps non vide, aucun nouveau format, aucune enveloppe API, aucune information sensible, trace ou secret.
- Aucun import/config Django au simple import du module ; imports `django.http` locaux dans la vue uniquement ; aucun `settings.configure`, `django.setup`, serveur, DB, socket ou I/O dans le code.
- Aucune URL distribuée : le module ne déclare aucun `path`, aucun `urlpatterns`, aucun `name`.
- En tests seuls : déclaration explicite via `RouteDeclaration(path=<synthetique>, name=<synthetique>, handler=liveness_view, public=True)` + `build_declared_urlpatterns`, `resolve` réel, client réel ; chemins synthétiques garde-compatibles, jamais présentés comme chemins publics de production.
- Handlers externes et conformité HTTP/enveloppes API restent hors portée.

## Files

`src/pixs/backend/liveness_view.py`, `tests/unit/test_liveness_view.py`, `tests/integration/test_liveness_view_integration.py`, plus append seul `src/pixs/backend/README.md` (texte exact dans NFDOC).

## Validation

OpenSpec strict avant code et finale ; unit sans Django configuré sauf sous-processus isolés ; intégration avec réglages synthétiques explicites en sous-processus frais (`DEFAULT_CHARSET`, `ROOT_URLCONF`, `ALLOWED_HOSTS`, `INSTALLED_APPS=()`, `MIDDLEWARE=()`), aucun secret ni engine SQLite, `django.setup()`, `resolve` réel, test client réel GET/HEAD/POST/inconnue/non-publique, `run_checks(databases=[])`, gardes `socket`/`psycopg` à zéro appel, UTF-8/LF, périmètre strict.

## Risks / Trade-offs

Aucune route utilisable en production issue de ce jalon. Le corps vide évite tout faux format métier. Toute surface concrète (santé exposée, shell servi, API versionnée) exigera un change distinct avec URL explicite validée.
