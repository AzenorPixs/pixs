# C14 — Modules essentiels PZT et DNS

## Pourquoi

Le canon impose les modules PZT et DNS essentiels ; aucun module produit PZT/DNS n’est identifié aux emplacements consultés. La spécification seule ne les fournit pas.

## Modifications proposées

Livrer le module essentiel pixs.pzt et le module DNS essentiel, propriété de leurs données, contrats publics, administration et état réseau désactivé. Le périmètre exact dépend de l’examen clause par clause C00 ; une simple page “désactivé” ne suffit pas. Toute clause impérative exigeant PA/DNS actif ajoute D01 au chemin critique.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `define-first-installable-pbo-profile`.
- `add-core-postgres-services`.
- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `add-protected-core-http-commands-and-queries`.
- `compose-modular-frontend-with-core-api`.

## Impact

Périmètre de réalisation futur : Composer deux responsabilités de gestion PBO propriétaires via les mécanismes communs ; identifiant pixs.pzt validé, identifiant DNS et manifests/contrats exacts restant à préciser. Conserver configuration souhaitée, versions et états d’absence d’exécutant ; appliquer les choix validés pertinents à la configuration. N’engager aucun PA, service DNS ou réseau non sélectionné, ni canal de substitution.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Modules composés même réseau désactivé ; absence essentielle bloquante ; configuration/visualisation/supervision honnêtes ; aucune mesure ni application réseau inventée ; aucun canal PBO–PA de substitution ; chaque clause conservée, motivée ou renvoyée vers évolution normative approuvée.

## Barrière de conception

Identifiants canoniques et contrats de gestion, sous-modules et schémas ; recouper chaque clause applicable de la table C00. Toute obligation active non conditionnelle rejoint le chemin critique ; aucune exemption supposée.
