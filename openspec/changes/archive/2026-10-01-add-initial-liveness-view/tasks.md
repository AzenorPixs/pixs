## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif hors archive et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Vue strictement bornée

- [x] 2.1 Créer `src/pixs/backend/liveness_view.py` seul, sans modifier facade/`manage.py`/`frontend/`.
- [x] 2.2 Créer `tests/unit/test_liveness_view.py` avec sous-processus isolés.
- [x] 2.3 Créer `tests/integration/test_liveness_view_integration.py` avec Django synthétique et garde explicite seuls en tests.

## 3. Preuves

- [x] 3.1 Réussir tests unitaires et d'intégration réels sous mandats CAB distincts, zéro socket/psycopg/connexion.
- [x] 3.2 Vérifier UTF-8/LF, périmètre trois fichiers code/tests + append README seul, diagnostics fixes sans repr/echo, conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver que tous les critères précédents sont satisfaits et que le delta normatif est identique à la norme validée ; autorisation CGPT d'archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
