# Adaptateur Django explicite Kernel/Core/Exemple

## Why

La spécification `initial-application-bootstrap` requiert une composition Django initiale chargeant `pixs.kernel` et `pixs.core` explicitement. Les manifests et le pipeline pur existent sans activation, `composition_initial.py` ne déclare que des constantes, et aucun `AppConfig` n'enregistre ces composants dans le registre Django : le chargement effectif via Django est absent. Un unique `PixsBackendConfig` n'enregistrerait pas Kernel/Core, et `ready()` résolvant le pipeline ne serait pas un chargement Django réel. Il s'agit d'une absence technique implémentable, non d'une incohérence documentaire.

## What Changes

- Fournir `src/pixs/backend/apps.py`, adaptateur Django explicite ne couplant aucune source kernel/core/exemple à Django : trois classes `AppConfig` distinctes et statiques `PixsKernelConfig`/`PixsCoreConfig`/`PixsExampleConfig`, `names` `pixs.kernel`/`pixs.core`/`pixs.example`, labels stables `pixs_kernel`/`pixs_core`/`pixs_example` NON versionnés (labels/migrations ne sont pas des versions de contrat).
- Sélection caller explicite des trois chemins de classes dans `INSTALLED_APPS` TEST fraîche ; aucun hook `ready`, pipeline automatique, activation, service, provider, DB, modèle ou secret ; `ready` hérité noop conservé.
- Mapping documenté : module `pixs.example` ≠ ID composant `example.hello` du manifest ; pas de renommage.
- Aucun `default_auto_field` nouveau (aucun modèle, choix inutile) ; aucune métadonnée état/descripteur proposée comme activation.
- Tests subprocess réels : `django.setup()` puis `apps.get_app_config`/`get_app_configs`, identité module/nom/label des trois, `apps.ready`, `get_models()` vide observé, gardes PG/socket zéro ; import adaptateur autorisé à importer `django.apps` (intégration Django explicite) mais zéro `settings.configure`/`setup`/binding/DB/activation à l'import (pas de `BlockDjango` exigé pour la classe).
- `__init__` existants restent purs ; manifests/pipeline/settings/checks/`manage.py` inchangés ; `compose` sans attestations refuse comme avant (couvert par tests existants préservés), aucun claim P0 ; `manage.py check` inchangé (exit 2 sans configuration).

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `initial-application-bootstrap` : premier jalon strict de l'exigence existante « Composition Django initiale déclarée », sous-ensemble enregistrement explicite seul, reprise normative inchangée.

## Impact

Un adaptateur (`apps.py`), deux tests (unit/intégration), un append `README` seul. Aucune source kernel/core/exemple/façade/`manage.py`/`frontend/` modifiée, aucune version/contrat/capacité nouvelle, aucune modification de norme. Si l'enregistrement Django seul s'avérait normativement incompatible, un NDOC serait présenté au lieu d'inventer une extension.
