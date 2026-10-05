## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif hors archive et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Grammaire strictement bornée

- [x] 2.1 Prouver baseline suites unitaires et d'intégration complètes avant code, sans modifier les tests historiques.
- [x] 2.2 Corriger `_require_path` seul dans `src/pixs/backend/http_route_guard.py`, sans modifier facade/`manage.py`/`frontend/`.
- [x] 2.3 Créer `tests/unit/test_static_file_path_literals.py` et `tests/integration/test_static_file_path_literals_integration.py` avec sous-processus isolés, plus append README seul.

## 3. Preuves

- [x] 3.1 Réussir suites unitaires et d'intégration complètes après code sous mandats CAB distincts, zéro socket/psycopg/connexion.
- [x] 3.2 Vérifier UTF-8/LF, périmètre correction + 2 tests + append seul, tests historiques inchangés, diagnostics sans valeurs, conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver que tous les critères précédents sont satisfaits et que le delta normatif est identique à la norme validée ; autorisation CGPT d'archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
