# Conception de l'adaptateur Django

## Context

Manifests `kernel`/`core`/`example` et pipeline `discover/validate/resolve/compose` purs existants ; `composition_initial.py` constantes seules ; `test_initial_component_declarations.py` couvre validation sans activation ; `manage.py` partiel (`--help`/`--version` 0, `check` sans config 2). Aucun adaptateur `apps.py` distribué (glob vide), aucun chargement distribué via `INSTALLED_APPS` ; les fixtures TEST existantes ne sont pas cette composition distribuée.

## Goals / Non-Goals

But : enregistrer explicitement les trois composants dans le registre Django réel en TEST. Non-buts : aucun `ready` actif, pipeline auto, activation, service, provider, DB, modèle, secret, `default_auto_field`, composition P0/prod, readiness/startup.

## Decisions

- Classes exactes : `PixsKernelConfig(AppConfig)` avec `name = "pixs.kernel"`, `label = "pixs_kernel"` (idem core/example) ; `verbose_name` anglais stable ; aucun attribut versionné ; `ready` non redéfini (noop hérité prouvé par `PixsKernelConfig.ready is AppConfig.ready`).
- Trois classes `default = False` : elles sont sélectionnées par leurs chemins explicites, sans choix automatique dans le module backend. `apps.ready` décrit le registre Django rempli en TEST, sans attester le P0 ni la readiness globale du projet.
- Caller TEST : `INSTALLED_APPS = ("pixs.backend.apps.PixsKernelConfig", "pixs.backend.apps.PixsCoreConfig", "pixs.backend.apps.PixsExampleConfig")`, settings synthétiques `ENGINE` seul, uniquement ces trois apps et middleware vides, `django.setup()` ; assertions `get_app_config(label).name/label/module`, trois configs dans `get_app_configs()`, `apps.ready is True`, `list(apps.get_models()) == []` observé, `run_checks(databases=[])` vert observé (distinct du `manage.py check` inchangé exit 2).
- Unit (sans setup) : import pur sans FS (gardes `os.open`/`scandir`/`Path.open`/`read_bytes` actives, `django.apps` importable), identité/noms/labels/`__all__`, base `AppConfig`, `ready` hérité, labels non versionnés et uniques, settings non configurés.
- Diagnostics : adaptateur sans erreur propre (classes statiques) ; tests hostiles limités aux entrées TEST (chemins `INSTALLED_APPS` invalides refusés par Django lui-même, non wrappés).
- Mapping `pixs.example` (module) vs `example.hello` (ID manifest) documenté dans proposal/design, sans renommage.

## Files

`src/pixs/backend/apps.py`, `tests/unit/test_initial_django_app_configs.py`, `tests/integration/test_initial_django_app_configs_integration.py`, append seul `src/pixs/backend/README.md`.

## Validation

Strict avant/après ; unit sous-processus isolés ; intégration Django réel joint ; AST 3.11, UTF-8/LF, périmètre strict.

## Risks / Trade-offs

Enregistrement seul, sans preuve d'activation : toute activation P0 exigerait un change distinct.
