## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif hors archive et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Adaptateur strictement borné

- [x] 2.1 Créer `src/pixs/backend/apps.py` seul (3 classes statiques, sans ready actif), sans modifier kernel/core/exemple/façade/`manage.py`/`frontend/`.
- [x] 2.2 Créer `tests/unit/test_initial_django_app_configs.py` avec sous-processus isolés.
- [x] 2.3 Créer `tests/integration/test_initial_django_app_configs_integration.py` avec Django réel et registre explicite seuls en tests, plus append README seul.

## 3. Preuves

- [x] 3.1 Réussir tests unitaires et d'intégration réels sous mandats CAB distincts, zéro socket/psycopg/connexion.
- [x] 3.2 Vérifier UTF-8/LF, périmètre adaptateur + 2 tests + append seul, diagnostics fixes, conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver que tous les critères précédents sont satisfaits et que le delta normatif est identique à la norme validée ; autorisation CGPT d'archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
