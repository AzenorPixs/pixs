# C11 — Frontend connecté et composable

## Pourquoi

Le shell est autonome ; les facettes frontend sont des déclarations immuables sans composition récursive de modules opérationnelle.

## Modifications proposées

Construire les contributions de modules/sous-modules depuis manifests, façades publiques, collisions et ordre explicites ; shell connecté aux API, sessions et contexte tenant, invalidation et refus côté serveur.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-protected-core-http-commands-and-queries`.
- `activate-reference-runtime-composition`.

## Impact

Périmètre de réalisation futur : Composer au build depuis manifests et contrats publics, sans registre/lifecycle frontend parallèle. Résoudre récursion et dépendances, collisions et façades ; le shell fournit session/contexte et consomme les API. Une intention UI ne devient un effet confirmé qu’après réponse serveur ; invalidation sous tenant courant.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Module et sous-module ajoutés sans éditer le shell ; collision et import privé refusés ; navigation/session/tenant corrects ; annulation ou refus de mutation visibles ; ordre identique entre développement et artefact.

## Barrière de conception

API publique du shell et points de contribution, frontières de build et catalogue de routes à formaliser ; conserver JavaScript existant sans conversion TypeScript implicite ni téléchargement runtime.
