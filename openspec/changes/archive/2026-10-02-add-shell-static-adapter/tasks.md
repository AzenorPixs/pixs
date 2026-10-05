## 1. Préparation

- [x] 1.1 Prouver périmètre, absence de change actif hors archive et périmètre CGPT.
- [x] 1.2 Préparer les cinq artefacts et réussir la validation OpenSpec stricte avant code.

## 2. Adaptateur strictement borné

- [x] 2.1 Régénérer `frontend/dist` sous mandat build distinct, sans modifier les sources frontend.
- [x] 2.2 Créer `src/pixs/backend/shell_adapter.py` seul, sans modifier garde/liveness/façade/`manage.py`/`frontend/`.
- [x] 2.3 Créer `tests/unit/test_shell_adapter.py`, `tests/integration/test_shell_adapter_integration.py` et `tests/integration/check_shell_adapter_browser.py` (hors discovery), plus append README seul.

## 3. Preuves

- [x] 3.1 Réussir suites unitaires et d'intégration plus harnais navigateur seul sous mandats CAB distincts, gardes PG zéro, loopback seul, cleanup prouvé.
- [x] 3.2 Vérifier UTF-8/LF, périmètre 4 fichiers + append seul, diagnostics fixes, conformité OpenSpec finale avant tout cochage sur preuves.
- [x] 3.3 Prouver que tous les critères précédents sont satisfaits et que le delta normatif est identique à la norme validée ; autorisation CGPT d'archivage distincte après contrôle.

Archivage et statistiques sont des mandats distincts après toutes les tâches prouvées et cochées ; leurs preuves sont conservées dans le RUN parent.
