# Entrée Django réelle minimale

## Why

Les manifests et la composition déclarative existent sans entrée exécutable, ce qui empêche tout projet Django vérifiable. Ce jalon partiel fournit la véritable entrée sans activer de runtime.

## What Changes

- Fournir `manage.py` à la racine déléguant réellement à `execute_from_command_line` de Django 5.2.17 existant, sans module settings par défaut, avec message fixe sur `ImproperlyConfigured` et sortie 2 sans configuration.
- Fournir `tests/unit/test_initial_manage_entrypoint.py` en sous-processus à environnement synthétique, bornés, pour `--help`, `--version` et `check` sans configuration, sans serveur ni migration.
- Documenter les limites dans le README backend.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : jalon partiel d'entrée du requirement Composition Django initiale déclarée existant repris inchangé.

## Impact

Trois fichiers, aucune dépendance ni norme ni configuration existante modifiée, pas de P0, PostgreSQL, readiness ni projet complet. `--help` n'est pas une preuve d'activation.
