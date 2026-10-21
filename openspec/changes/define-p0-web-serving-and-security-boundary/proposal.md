# N04 — Entrée web et frontière de service du P0

## Pourquoi

C03 porte sessions/authentification ; C06 les Commands/API ; C07 la composition ; C11 le shell ; C18 les unités de services. Aucun de ces plans ne détaille l’assemblage HTTP distribué : serveur applicatif non destiné au développement, exposition du bundle PFO et liens profonds, chemin API/admin/santé, frontière privée des rôles/management et confiance des en-têtes d’un éventuel intermédiaire.

## Préparation validée

Le développeur a validé ce dossier dédié le 17 octobre 2026 dans l’audit transversal P0. [Conception, responsabilités et critères](design.md). Aucune implémentation autorisée.

## Capacités et deltas

Deltas ADDED dans `reference-runtime` et `api`, limités au profil d’entrée P0. Les seules clauses api « Façade web à cookie et API Bearer explicitement distinctes » et « Contrats de transport et stockage navigateur », issues des décisions C03, sont adoptées au canon le 20 octobre 2026.

Les autres clauses api et le delta reference-runtime restent proposés. Les sources des deux clauses synchronisées sont conservées dans le change ; aucun archivage ni code n’est engagé. Les paramètres encore ouverts ne sont pas réputés approuvés.

## Dépendances et intégration

Voir les responsabilités et conditions de [design.md](design.md) et le [plan global courant](../archive/2026-10-18-define-first-installable-pbo-profile/plan-global-preparation.md). Les producteurs précoces de contrats, les conditions d’activation et la recette finale restent distincts.

## Impact

Préparation documentaire du chemin P0 ; pas d’activation d’option extérieure au profil, d’outil installé, de serveur sélectionné implicitement, de clé réelle, de migration ou de publication. Les tâches futures nécessitent une autorisation de réalisation distincte.

## Dépendances après audit transversal P0

[C03](../add-initial-authentication-and-sessions/proposal.md), [C06](../add-protected-core-http-commands-and-queries/proposal.md), [C07](../activate-reference-runtime-composition/proposal.md), [C11](../compose-modular-frontend-with-core-api/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
