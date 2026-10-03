# Vue liveness initiale bornée

## Why

La spécification `initial-application-bootstrap` requiert des routes et vues de base séparant la santé du shell et de l'API versionnée, avec déclaration explicite du public et refus du reste sans information sensible. La spécification `observability` requiert des sondes distinguant vivacité, disponibilité, démarrage et diagnostic, rapides, bornées, sans mutation ni secret. Seule la garde de déclaration/refus existe sans vue réelle ; aucun service opérationnel, aucune persistance démontrée.

## What Changes

- Fournir un module Django `src/pixs/backend/liveness_view.py` exposant `liveness_view`, sans route concrète distribuée.
- GET et HEAD retournent 200 avec corps vide, `Content-Type: text/plain; charset=utf-8`; autres méthodes retournent 405 avec corps vide et `Allow: GET, HEAD`. Toutes ces réponses portent `Cache-Control: no-store` pour ne pas transformer une réponse mise en cache en signal de vivacité.
- La vue prouve exclusivement une requête effectivement traitée ; aucune assertion readiness, startup, P0, composition, persistance ou API.
- Accepter les requêtes Django réelles (`WSGIRequest`/`ASGIRequest`) par validation standard minimale de l'attribut `method`, sans exiger un type exact `HttpRequest` seul et sans condition readiness.
- Tous nouveaux identifiants en anglais ; diagnostics fixes sans `repr` ni echo de valeur.
- Ajouter une section liveness minimale dans `src/pixs/backend/README.md` (module direct, 3 limites, aucune route publique).
- Tester la vue et son branchement sous déclaration publique explicite via `build_declared_urlpatterns` avec le client Django réel, uniquement en sous-processus synthétiques isolés, avec gardes DB/socket.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : premier jalon strict de l'exigence existante « Surface HTTP initiale minimale », sous-ensemble vue liveness seule, reprise normative inchangée.

## Impact

Trois nouveaux fichiers code/tests hors artefacts : `src/pixs/backend/liveness_view.py`, `tests/unit/test_liveness_view.py`, `tests/integration/test_liveness_view_integration.py`, plus un append documentaire seul dans `src/pixs/backend/README.md`. Aucune façade existante modifiée, aucun `manage.py`/`frontend/` modifié, aucun nouveau contrat/version/capacité, aucun `ApiContractPlan` inventé, aucun serveur/DB/SQLite, aucun secret, aucun Git, aucun déploiement. Surface complète, shell, API publiée et profil conjoint restent non satisfaits.
