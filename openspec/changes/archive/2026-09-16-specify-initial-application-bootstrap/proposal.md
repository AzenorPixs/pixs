# SP05 — Spécification de l’amorçage applicatif initial

<!-- ACL-R2 : code de lot attribué rétrospectivement le 2026-10-28. -->

## Why

La proposition historique du 16 septembre 2026 définit la première composition
de développement Django, PostgreSQL et TanStack. Son lot bootstrap est séparé
des exigences d'administration, maintenance et audit pour rendre chaque
proposition complète validable strictement. Ce découpage documentaire conserve
les garanties historiques et ne les réapplique pas au canon actuel.

## What Changes

- Conserver les quatre exigences de composition P0, surface HTTP, shell et
  profil local dans le seul lot bootstrap.
- Préserver intégralement le fichier de deltas `initial-application-bootstrap`
  corrigé le 26 octobre 2026 : quatre exigences et six scénarios.
- Transférer les neuf exigences d'administration, maintenance et audit au lot
  compagnon `specify-initial-administration-and-maintenance`, sans duplication.
- Conserver le plan historique des douze tâches comme trace du périmètre
  initial ; les validations courantes distinguent les deux lots.

## Capabilities

### New Capabilities

- `initial-application-bootstrap` : capacité du lot historique de composition
  Django et TanStack, déjà présente dans le canon ; aucune nouvelle adoption
  canonique n'est effectuée par ce découpage.

## Impact

Ce lot reste exclusivement documentaire : aucun code, dépendance, configuration
exécutable, donnée métier ou secret n'est produit. Le réarchivage utilise
`--skip-specs` afin de préserver les évolutions ultérieures du canon.
Le lot compagnon est conservé dans
[son archive](../2026-10-26-specify-initial-administration-and-maintenance/proposal.md).
