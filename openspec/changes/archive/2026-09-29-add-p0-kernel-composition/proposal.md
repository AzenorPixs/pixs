# Proposal

## Why

Aucun socle P0 exécutable n'existe : les capacités `kernel`, `component-model`,
`dependencies`, `capabilities`, `contracts`, `services`, `providers`, `lifecycle`,
`configuration` et `compatibility` sont spécifiées, mais aucun mécanisme générique
ne permet de découvrir, valider, ordonner et activer des composants de façon
déterministe. Sans ce socle, `pixs.core`, la composition de référence et
l'application initiale ne peuvent être ni composées ni vérifiées.

## What Changes

- Implémentation du noyau générique : registre de modules, résolveur de
  dépendances, gestionnaire de cycle de vie, registre de services, bus
  d'événements, registre de configuration, registre d'extensions.
- Modèle de composants appliqué : validation des manifests `component.toml`
  (schéma versionné, identifiants namespacés `pixs.*` réservés, types unifiés,
  refus de secret ou de logique exécutable), collisions d'identifiants refusées.
- Résolution déterministe : graphe de dépendances et ordre de chargement stables
  à entrée identique ; refus explicites des cycles, des ambiguïtés de fournisseurs
  (configuré, sinon candidat unique, sinon invalidation) et des contraintes de
  compatibilité insatisfaites, avec diagnostics ; vérification des contraintes de
  version des contrats avant activation.
- Règle déclarative rendant `pixs.core` obligatoire : portée comme métadonnée de
  composition validée par les mécanismes du noyau, sans qu'aucune notion métier
  (utilisateur, groupe, ACL, fournisseur) n'entre dans le noyau.
- Tests de socle : niveaux unitaires et d'intégration distincts, fixtures
  synthétiques sans secret, preuves reproductibles ; les hooks de cycle de vie et
  opérations mécaniques (`discover`…`disable`) sont dans le périmètre ;
  `migrate`, `upgrade`, `uninstall`, `purge` effectifs relèvent de changes ultérieurs.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Aucune : le change implémente des exigences normatives existantes, sans nouvelle
exigence ni modification normative.

## Impact

- Composants : code du kernel (registres, résolveur, cycle de vie, configuration),
  validateur de manifests, diagnostics de composition.
- Tests : suites unitaires (schéma, graphe, cycles, ambiguïté, identifiants) et
  d'intégration (composition kernel + coquille de test), sans secret ni donnée de production.
- Exclus : primitives fonctionnelles de `pixs.core` (utilisateurs, groupes,
  appartenances, tenants, rôles, ACL, permissions), surface API HTTP, frontend
  TanStack, providers concrets, résolution effective de secrets (structure de
  référence côté noyau uniquement), contribution frontend récursive au graphe,
  et composition de référence intégrale `reference-composition` : changes ultérieurs.
