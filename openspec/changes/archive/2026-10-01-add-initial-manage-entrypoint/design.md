# Conception de l'entrée Django réelle

## Context

Les manifests et données existent sans entrée exécutable. Aucune configuration runtime n'est prouvée.

## Goals / Non-Goals

Fournir la délégation réelle à Django sans settings par défaut ni activation. Aucun projet complet, P0, readiness ou PostgreSQL n'est visé.

## Decisions

- `manage.py` délègue réellement à `django.core.management.execute_from_command_line` de Django 5.2.17 existant ; `main(argv=None)` avec argv explicite ou `sys.argv`, sans `os.environ`, module settings, import composition, attestation ou checker.
- Seul `django.core.exceptions.ImproperlyConfigured` est capturé : message fixe sans exception brute, sortie 2 ; aucun catch général masquant les autres erreurs.
- Django reste responsable des commandes ; aucun `runserver`/`migrate` exécuté.
- `DJANGO_SETTINGS_MODULE` est la configuration runtime standard future, sans valeur distribuée et non chargée pour les tests.

## Files

manage.py, tests/unit/test_initial_manage_entrypoint.py, src/pixs/backend/README.md.

## Validation

Sous-processus `sys.executable -B` à environnement synthétique construit explicitement sans `os.environ`, délai 30, `--help`/`--version` sortie 0 et `check` sans settings sortie 2 au diagnostic fixe sans traceback. Syntaxe AST en mémoire, régressions unit/integration via venv existante avec `PYTHONPATH` explicite et `TMPDIR` projet, strict avant et après. Aucun package supplémentaire ni configuration existante modifiée.
