# Matrice de conservation — baseline initiale

## Référence et méthode

La baseline cible compte 76 capacités, 300 exigences et 305 scénarios. La
conservation est évaluée unité par unité : chaque exigence et chacun de ses
scénarios restent dans la capacité et sous le même intitulé, sauf les quatre
groupes de deltas explicitement identifiés ci-dessous. Les groupes inchangés
ont une relation identité entre source et cible ; aucune reformulation n'est
autorisée sans un delta distinct et une nouvelle ligne de matrice.

| ID | Source | Cible | Exigences / scénarios | Statut |
| --- | --- | --- | --- | --- |
| M-001 | Les 72 capacités stables hors `audit` et `operations` de la baseline antérieure | Même chemin sous `openspec/specs/` | 277 / 280, relation identité | Conservé textuellement |
| M-002 | Delta `audit` du change `specify-initial-application-bootstrap` | `openspec/specs/audit/spec.md`, `Audit exhaustif du panneau d'administration` | 1 / 1 | Intégré textuellement |
| M-003 | Delta `operations` du change `specify-initial-application-bootstrap` | `openspec/specs/operations/spec.md`, `Maintenance hiérarchisée` | 1 / 1 | Intégré textuellement |
| M-004 | Delta `initial-application-bootstrap` du change `specify-initial-application-bootstrap` | `openspec/specs/initial-application-bootstrap/spec.md` | 4 / 4 | Intégré textuellement |
| M-005 | Delta `initial-administration` du change `specify-initial-application-bootstrap` | `openspec/specs/initial-administration/spec.md` | 7 / 9 | Intégré textuellement |

Les cinq lignes couvrent 76 capacités, 300 exigences et 305 scénarios. Les
capacités et chemins restent distincts ; aucune exigence n'est absorbée,
renommée ou supprimée.

## Dépendances contrôlées

Les relations de M-002 à M-005 restent portées par les capacités de bootstrap,
audit et opérations. Elles s'appuient sur `reference-composition`,
`installation-provisioning`, `identity-assurance`, `authorization` et
`secrets-providers` sans transférer de comportement entre ces capacités.

## Écarts et décisions ouvertes

- La référence résiduelle à 74 capacités a été corrigée à 76 dans le design du
  change.
- Les deltas du bootstrap sont déjà présents dans la baseline : un archivage
  automatique ne doit donc pas tenter de les appliquer une seconde fois.
- Toute consolidation documentaire ultérieure exige une nouvelle entrée de
  matrice et la validation explicite du développeur avant modification des
  spécifications actives.
