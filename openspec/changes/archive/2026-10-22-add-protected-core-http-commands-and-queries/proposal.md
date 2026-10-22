# C06 — API et opérations publiques

## Pourquoi

Plans OpenAPI et fabriques de réponses sont isolés ; les documents backend indiquent l’absence de routes Core complètes, pagination et idempotence générale.

## Modifications proposées

Exposer les primitives nécessaires par routes explicites versionnées et OpenAPI, requêtes filtrées, commandes propriétaires, pagination, erreurs localisables et idempotence durable. Ne pas exposer Bulk incomplet.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-core-postgres-services`.
- `add-initial-authentication-and-sessions`.
- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.

## Impact

Périmètre de réalisation futur : Exposer les services Core propriétaires par API versionnée et contrats publiés. Résoudre tenant du chemin, identité et autorisation avant exposition ; requêtes sans mutation, listes filtrées à la source. Lier clé d’idempotence, empreinte de requête, périmètre et résultat durable ; localiser les messages par catalogue.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Parcours API sans frontend ; contrat et réponse concordants ; rejeu même clé/même contenu sans double effet, conflit explicite ; tenant du chemin canonique ; accès privé et inter-tenant refusés.

## Barrière de conception

Catalogue exact de routes et commandes, schémas/versions, contrat de curseur et conservation idempotence ; ne pas annoncer Bulk ou SDK optionnels.
