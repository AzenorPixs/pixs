# C07 — Composition et lifecycle réels

## Pourquoi

Le gabarit est toujours non prêt, les profils sont déclaratifs et composition_proof reste partielle ; l’activation réelle intégrée n’est pas démontrée.

## Modifications proposées

Fournir l’hôte Django de composition Kernel/Core/providers et les adaptateurs de lifecycle ; relier les contrôles de versions et preuves authentifiées aux capacités réellement présentes. Définir le branchement PZT sans le simuler : les tests intermédiaires restent bornés et le passage P0 à ready demeure refusé tant que C14 et les autres obligations manquent.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-pbo-runtime-secret-provider`.
- `add-core-postgres-services`.
- `add-durable-minimized-audit`.

## Impact

Périmètre de réalisation futur : Fournir l’hôte runtime et les adapters du lifecycle commun, sans remplacer les mécanismes purs. Lier composants/providers/configuration/migrations et preuves authentifiées. L’hôte intermédiaire peut être exercé isolément mais refuse readiness P0 si PZT/DNS ou toute autre obligation manque ; C14 et C17 ferment l’intégration.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Ordre de composition déterministe, entrée runtime réelle en environnement isolé ; composant essentiel absent, fournisseur ambigu ou preuve manquante → P0 hors service. L’hôte intermédiaire ne certifie pas le produit ; intégration complète de PZT en C14 et recette installable en C17.

## Barrière de conception

Entrée de lancement, registre des adapters et limites d’exposition à arrêter sans nouveau runtime ; ne pas transformer globally_compatible=False en certificat global.
