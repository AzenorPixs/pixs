# Design — add-initial-frontend-contribution-type-vocabulary

## Contrats
- Source canonique unique : `openspec/specs/frontend/spec.md`, Requirement `Vocabulaire structurel préparatoire FrontendContributionType v1` et ses deux scénarios.
- Python `>=3.12` conservé, stdlib seulement (`enum.Enum`).

## Fichiers
- `src/pixs/kernel/frontend_contribution_types.py` :
  - docstring structurelle seule, sans machine, transition, envoi, routage, activation ou persistance ;
  - `class FrontendContributionType(Enum)` avec exactement dans cet ordre :
    `ROUTE="ROUTE"`, `PAGE="PAGE"`, `NAVIGATION="NAVIGATION"`, `COMPONENT="COMPONENT"`, `FORM="FORM"`, `TRANSLATION="TRANSLATION"`, `UI_PERMISSION="UI_PERMISSION"`, `UI_SLOT="UI_SLOT"` ;
  - `__all__ = ["FrontendContributionType"]` ;
  - aucune fonction, classe supplémentaire, constante applicative ni import autre que enum.Enum.
- `src/pixs/kernel/__init__.py` : inchangé.
- `tests/unit/test_frontend_contribution_type.py` : même forme que `test_notification_delivery_state.py` avec canon à huit paires, contrôle `len==8`, `members==8`, `__all__` seul.
- `tests/integration/test_frontend_contribution_type_integration.py` : même forme que `test_notification_delivery_state_integration.py` avec gardes writes/network/process/environ/db, contrôles positifs, import `pixs.kernel.frontend_contribution_types`, canon à huit paires, `MARKER="FRONTEND_CONTRIBUTION_TYPE_SAFE_INTEGRATION_OK"`, `FIXED_ENV={"LANG":"C.UTF-8","PATH":"/usr/bin:/bin"}`, `TIMEOUT_SECONDS=10`.

## Exclusions
- Le module MUST NOT enregistrer, composer, charger ou activer une contribution.
- Il MUST NOT définir un champ de manifest, une route, une permission ou un effet runtime.
