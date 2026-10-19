# C04 — Autorisation Django et Super Admin

## Pourquoi

authorize et source-filter-plan-v1 fournissent un PDP et un plan préparatoires ; l’intégration PEP Django et l’exception Super Admin opérationnelle ne sont pas démontrées.

## Modifications proposées

Brancher PEP, PDP et filtrage à la source ; intégrer l’exception du seul Super Admin authentifié, les accords explicites de tenant et la propagation de l’acteur initial sans credentials délégués.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-core-postgres-services`.
- `add-initial-authentication-and-sessions`.

- `add-durable-minimized-audit` : audit durable des authentifications, refus et décisions runtime.

## Impact

Périmètre de réalisation futur : Reconnaître le seul compte fonctionnel authentifié à la frontière runtime, avec accords tenant explicites. Conserver les profils structurels sans privilège. Pour comptes ordinaires, appliquer DENY/ALLOW/refus par défaut et obligations PEP ; filtrer à la source avant pagination. Propager acteur initial et périmètre sans credentials délégués.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

DENY/ALLOW et refus par défaut ordinaires ; tenant non accordé refusé même au Super Admin ; tenant accordé et dérogations testés ; même sémantique API/CLI/panneau/asynchrone ; obligations PEP réellement honorées.

## Barrière de conception

Reconnaissance du compte unique, persistance des accords tenant, interprétation des obligations et protocole de dérogation/audit avec C05 ; conception transversale à revoir avant modification du runtime.
