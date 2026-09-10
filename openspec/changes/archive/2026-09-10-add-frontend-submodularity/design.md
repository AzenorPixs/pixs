## Context

Le shell TanStack, les contributions frontend déclarées et la composition au
build sont déjà des principes Pixs. Les capacités actuelles ne précisent pas
assez que cette composition est récursive et qu'un sous-module peut être un
propriétaire frontend autonome. Voir `proposal.md` pour la motivation.

## Goals / Non-Goals

**Goals:**

- Réutiliser le modèle de composant, le manifest et le graphe de dépendances
  pour les contributions frontend de modules et sous-modules.
- Garantir une composition build-time déterministe, vérifiable et isolée.
- Préserver les frontières publiques entre shell, parent, enfant et composants
  frères.

**Non-Goals:**

- Ne pas introduire de type `FRONTEND_MODULE` ou `FRONTEND_SUBMODULE`.
- Ne pas figer la syntaxe complète de `[frontend]` dans `component.toml`.
- Ne pas introduire de Module Federation, de marketplace ou de code distant.
- Ne pas implémenter le shell TanStack, les manifests ou les bundles.

## Decisions

1. **La modularité frontend est une facette de `MODULE` et `SUBMODULE`.**
   Le composant conserve un manifest et un lifecycle uniques ; `[frontend]`
   déclare seulement des contributions supplémentaires. Cette option évite deux
   graphes, des états divergents et une seconde politique de confiance.
   L'alternative de types frontend dédiés est rejetée car elle dupliquerait le
   modèle commun sans apporter de frontière fonctionnelle supplémentaire.

2. **Le build résout un graphe unique et récursif.**
   Il prend en compte les composants, leurs sous-modules et leurs contributions,
   puis contrôle les contrats publics, les versions, les collisions et les
   dépendances avant de produire les chunks livrés. Un chemin de sources ou un
   ordre d'import n'est jamais une règle de rattachement ou de priorité.
   L'alternative d'une découverte par scan de répertoires est rejetée car elle
   serait non déterministe et contournerait les manifests.

3. **Les intégrations parent-enfant sont contractuelles.**
   Une route, un slot, une façade, une traduction ou un événement UI est
   namespacé et versionné par son propriétaire. Un sous-module ne lit pas le
   store privé de son parent ; il utilise une façade ou un point d'extension
   déclaré. Cette décision préserve l'évolutivité et l'isolation des modules.

4. **Les défaillances suivent la criticité déclarée.**
   Un sous-module optionnel peut être isolé avec ses contributions en
   `DEGRADED` ou `DISABLED`. Une dépendance obligatoire absente, incompatible,
   cyclique ou en collision rend le périmètre concerné non composable. Cela ne
   modifie pas les contrôles backend ni l'interdiction de code distant runtime.

## Risks / Trade-offs

- [Composition plus coûteuse à analyser] → validation statique au build et
  diagnostics corrélés par composant et contribution.
- [Couplage parent-enfant déguisé par imports] → façades publiques versionnées
  et vérification des imports autorisés.
- [Multiplication de routes ou traductions] → identifiants namespacés,
  collisions bloquantes et catalogues appartenant au composant propriétaire.

## Migration Plan

Le changement est préparatoire : il n'existe aucun frontend Pixs à migrer.
Les futurs composants déclareront progressivement leur facette `[frontend]`
et seront validés par le graphe commun. Un retrait revient à supprimer les
contributions déclarées d'un composant dans une évolution compatible ou
versionnée ; aucun état runtime ou stockage métier n'est introduit ici.
