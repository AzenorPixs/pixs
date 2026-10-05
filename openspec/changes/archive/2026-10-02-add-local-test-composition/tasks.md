## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif hors archive et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Composition strictement bornée

- [x] 2.1 Créer `src/pixs/backend/local_test_composition.py` seul, sans modifier handlers/façade/`manage.py`/`frontend/`.
- [x] 2.2 Créer `tests/unit/test_local_test_composition.py` avec sous-processus isolés.
- [x] 2.3 Créer `tests/integration/test_local_test_composition_integration.py` et `tests/integration/check_local_composition_browser.py` (hors discovery) avec Django synthétique et garde explicite seuls en tests, plus append README seul.

## 3. Preuves

- [x] 3.1 Réussir suites unitaires et d'intégration plus harnais navigateur seul sous mandats CAB distincts, gardes PG zéro, loopback seul, cleanup prouvé.
- [x] 3.2 Vérifier UTF-8/LF, périmètre quatre fichiers + append seul, diagnostics fixes sans valeurs, conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver que tous les critères précédents sont satisfaits et que le delta normatif est identique à la norme validée ; autorisation CGPT d'archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
