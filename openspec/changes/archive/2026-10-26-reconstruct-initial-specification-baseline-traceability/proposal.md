# SP26 — Reconstruction de la traçabilité du référentiel initial de spécifications

<!-- ACL-R2 : code de lot attribué rétrospectivement le 2026-10-28. -->

## Why

La revalidation de `2026-09-16-consolidate-initial-specification-baseline`
a relevé une matrice trop agrégée et une différence de dix exigences et dix
scénarios entre ses lignes et les totaux annoncés. Sept tâches historiques
manquaient de preuves dans le périmètre alors consulté.

Le développeur a validé le 26 octobre 2026 les corrections documentaires et
les vérifications, y compris la consultation de l'historique Git, avec
préservation de l'archive historique. Le présent lot porte cette réalisation
distincte ; il ne rouvre pas le RUN RCAMP clôturé.

## What Changes

- Reconstituer la matrice élément par élément depuis des commits identifiés.
- Expliquer les dix exigences et dix scénarios omis de l'agrégation initiale.
- Séparer conservation historique, traçabilité vers le canon actuel et
  preuves de décisions humaines.
- Examiner chacun des sept points non vérifiables et qualifier les contrôles
  actuels sans les transformer en preuves d'exécutions passées.
- Fournir un vérificateur documentaire reproductible et les empreintes des
  sources protégées.

## Capabilities

### New Capabilities

Aucune. Le lot produit des preuves documentaires.

### Modified Capabilities

Aucune. Aucun delta normatif ni synchronisation n'est prévu.

## Impact

Seul ce nouveau dossier OpenSpec et les preuves non versionnées de ses
vérifications sont écrits. Le lot n'écrit dans aucune des deux archives,
leurs statistiques, les spécifications actives, le code, les tests existants
ou les cadrages. Le contrôle final exige l'identité de l'archive cible et du
canon capturé ; une dérive observée dans l'archive auxiliaire est signalée
séparément, ses sources normatives étant lues dans le commit H1 immuable.
La consultation Git reste en lecture seule ; aucun commit, push ou
changement de branche n'est réalisé. Après validation du lot, le développeur
a expressément demandé son archivage avec statistiques le 26 octobre 2026,
avec maintien des réserves historiques et des points partiels. Cet archivage
documentaire ne synchronise aucune spécification et n'affecte pas les deux
archives historiques citées.
