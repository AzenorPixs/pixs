## Why

Pixs prévoit déjà des contributions frontend composées au build, mais ne
formalise pas explicitement leur modularité récursive. Un module métier doit
pouvoir déléguer une capacité d'interface à des sous-modules autonomes sans
créer un second moteur de composants, de dépendances ou de lifecycle.

## What Changes

- Formaliser la facette frontend des composants `MODULE` et `SUBMODULE`.
- Résoudre les contributions frontend de modules et sous-modules dans un graphe
  unique, déterministe et validé au build.
- Encadrer les frontières publiques entre un parent, ses sous-modules, le shell
  et le Design System, sans accès aux implémentations privées.
- Ajouter les contrôles de composition récursive à la conformité frontend.
- Mettre à jour `PROJECT.md`, `TECHNICAL.md` et `BUILD.md` pour refléter ces
  garanties de conception, de mise en oeuvre et de construction.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `component-model`: les facettes frontend des modules et sous-modules utilisent
  le modèle de composant commun, sans type parallèle.
- `dependencies`: le graphe frontend récursif est résolu avec les dépendances
  de composants et les façades publiques déclarées.
- `extension-contracts`: les frontières et points d'intégration entre composants
  frontend imbriqués sont des contrats publics versionnés.
- `frontend`: les contributions de modules et sous-modules sont composées de
  manière récursive, déterministe et isolée.
- `modules`: un module et un sous-module restent propriétaires de leurs
  contributions frontend déclarées.
- `testing`: la conformité couvre la résolution récursive et l'isolation des
  sous-modules frontend.

## Impact

Le changement est exclusivement architectural et documentaire : aucun code,
API HTTP, provider, dépendance technique ou chargement de code distant n'est
introduit. Les futurs manifests `component.toml`, le shell TanStack et la
chaîne de build devront appliquer les contraintes ajoutées.
