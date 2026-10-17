# C12 — Primitives UI, langues, thèmes et accessibilité

## Pourquoi

Catalogues anglais/français et thèmes du shell existent ; les erreurs API comportent encore des textes fixes et les primitives partagées ne sont pas complètement qualifiées.

## Modifications proposées

Livrer les primitives publiques nécessaires aux parcours, catalogues anglais complets/français, localisation des erreurs API, formats et préférences ; vérifier Light/Dark, clavier, lecteur d’écran et responsive.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-protected-core-http-commands-and-queries`.
- `compose-modular-frontend-with-core-api`.

## Impact

Périmètre de réalisation futur : Étendre les catalogues par propriétaire, canon anglais complet, préférences et formats sans altérer les valeurs métier. Stabiliser tokens/primitives publiques nécessaires aux parcours P0, clair/sombre, noms/états natifs et focus. Exécuter unités dans les deux navigateurs et compléter par vérifications manuelles WCAG.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Aucun texte utilisateur hors catalogue propriétaire ; build refuse incohérences ; unités dans Chromium et Firefox headless ; parcours manuels et outillés WCAG 2.2 AA ; pas de substitution par build ou Node.

## Barrière de conception

Surface publique des primitives, résolution préférences/périmètre/installation et protocole manuel d’accessibilité ; pas de bibliothèque UI nouvelle implicite.
