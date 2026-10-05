# Littéraux de chemins de fichiers statiques dans la garde

## Why

La spécification `initial-application-bootstrap` requiert des routes et vues de base séparant la santé du shell et de l'API versionnée, avec déclaration explicite du public et refus du reste sans information sensible. La garde `build_declared_urlpatterns` refuse tout point dans les segments, donc un littéral réel tel que `assets/index-HASH.js` ne peut pas être déclaré. Il s'agit d'une absence technique implémentable, non d'une incohérence documentaire.

## What Changes

- Autoriser le point seulement à l'intérieur des segments dans `_require_path` : refuser point initial/final de segment, points consécutifs, segments `"."` ou `".."`.
- Conserver strictement toutes les autres validations : chaînes exactes, sans slash initial, sans `//`, sans `?#*<> :()[]{}^$+|\%`, sans contrôle, segments non vides, handler callable, `public` bool exact, unicité `path`/`name`, 403 non-public sans appel handler, catchall 404 fixe sans echo.
- Ajouter deux nouveaux fichiers de tests dédiés aux littéraux, sans corriger les deux tests historiques existants.
- Baseline suites unitaires et d'intégration complètes avant code, puis suites complètes après, avec gardes DB/socket.
- Ajouter un append documentaire seul dans `src/pixs/backend/README.md`.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : jalon complémentaire strict de l'exigence existante « Surface HTTP initiale minimale », sous-ensemble grammaire littéraux seule, reprise normative inchangée.

## Impact

Une évolution ciblée seule dans `src/pixs/backend/http_route_guard.py`, deux nouveaux fichiers `tests/unit/test_static_file_path_literals.py` et `tests/integration/test_static_file_path_literals_integration.py`, plus un append seul dans `src/pixs/backend/README.md`. Deux tests historiques intégralement conservés. Aucune façade/`manage.py`/`frontend/` modifié, aucun contrat/version/capacité nouveau, aucune URL concrète distribuée, aucun serveur/DB/SQLite, aucun secret, aucun Git, aucun déploiement. Surface complète, shell servi, API publiée et profil conjoint restent non satisfaits.
