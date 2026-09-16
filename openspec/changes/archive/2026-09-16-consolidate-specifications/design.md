## Context

Le référentiel actif contient 74 spécifications, 287 exigences et 290
scénarios. La validation stricte OpenSpec est réussie. Deux changes archivés
tracent le socle initial de 56 capacités et sa migration RFC 2119 ; aucune
source OpenSpec ne retrace l'introduction des 18 capacités supplémentaires.

## Goals / Non-Goals

**Goals:**

- Établir les 74 capacités actives comme baseline fonctionnelle unique.
- Préserver exactement les exigences, scénarios et chemins de capacité.
- Rendre explicite la provenance historique disponible et son absence pour les
  18 capacités concernées.
- Définir les contrôles minimaux applicables avant une évolution ultérieure.

**Non-Goals:**

- Modifier une exigence, un scénario ou la taxonomie active.
- Créer, implémenter ou activer une fonctionnalité produit.
- Réécrire l'historique, déplacer ou supprimer une spécification existante.

## Decisions

### Les 74 capacités restent des frontières stables

La consolidation conserve les chemins actifs. Les recouvrements apparents sont
traités comme des interfaces entre capacités, non comme une preuve de doublon.
Cette décision évite une perte de comportement ou de scénario sans arbitrage
fonctionnel explicite. L'alternative — fusionner les capacités — est différée
à un change dédié, avec mapping exigence par exigence et validation du
développeur.

### La baseline est le référentiel actif validé strictement

Les spécifications sous `openspec/specs/` constituent l'unique référence
fonctionnelle consolidée. Les changes archivés sont des preuves historiques et
ne concurrencent pas le référentiel actif. Cette distinction respecte le cycle
de vie OpenSpec et évite de réactiver des tâches archivées.

### La lacune de provenance est déclarée, non reconstituée fictivement

Les capacités `ai-agents`, `architecture-decisions`, `audit-integrity`,
`business-rules`, `component-registry`, `developer-experience`,
`directory-projections`, `distributed-cache`, `installation-provisioning`,
`native-clients`, `progressive-deployment`, `realtime-collaboration`,
`reference-composition`, `reference-runtime`, `reporting-analytics`,
`scim-provisioning`, `secrets-providers` et `service-objectives` ne sont
attribuées à aucun change historique absent. Le présent change fournit le
point de départ traçable pour leurs évolutions futures, sans fabriquer une
provenance rétrospective.

### Contrôles requis avant évolution future

Toute évolution doit partir de la baseline active, identifier la ou les
capacités concernées, préserver ou modifier explicitement les scénarios, et
passer `openspec validate --all --strict`. Une modification de frontière entre
capacités exige un change dédié et une table de correspondance des exigences.

## Risks / Trade-offs

- [Recouvrement encore possible entre capacités] → Le référentiel reste stable
  ; tout regroupement futur nécessite une analyse ciblée et réversible.
- [Provenance antérieure aux 18 capacités indisponible] → La lacune est
  explicitement documentée plutôt qu'inférée ; ce change devient leur point de
  référence à compter de son archivage.
- [Confusion entre artefact historique et référentiel actif] → Les contrôles
  futurs visent uniquement `openspec/specs/` et l'état du change en cours.

## Migration Plan

1. Valider le change documentaire et le référentiel actif en mode strict.
2. Archiver le change sans synchronisation de deltas fonctionnels.
3. Utiliser ensuite le référentiel actif comme baseline de tout nouveau change.

Le retour arrière consiste à ne pas archiver ce change ; il ne modifie aucune
spécification active.
