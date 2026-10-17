# C09 — Worker, scheduler et événements

## Pourquoi

JobRecord et des primitives transactionnelles Bulk existent ; ils ne fournissent pas le worker et scheduler généraux ni une livraison d’événements qualifiée.

## Modifications proposées

Livrer worker et scheduler du même artefact, travaux persistants, lease/fencing scheduler, publication après commit, consommateurs idempotents, réessais et échecs inspectables. Réévaluer droits et contexte à l’exécution.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `add-protected-core-http-commands-and-queries`.
- `activate-reference-runtime-composition`.

## Impact

Périmètre de réalisation futur : Réutiliser les structures applicables sans généraliser un bail Bulk au scheduler. Exécuter jobs et publication après commit via mêmes contrats, persistance PostgreSQL et contexte réautorisé. Lease persistant et clôture de péremption empêchent l’ancien scheduler d’agir ; reprises, retries et états terminaux sont inspectables.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Deux schedulers → un détenteur admissible ; ancien détenteur rejeté ; crash/reprise sans double effet ; événement jamais avant commit ; révocation avant exécution respectée ; drain borné.

## Barrière de conception

Contrats d’exécution, baux/échéances/fencing, réveil et publication à qualifier. Aucun broker externe ou dépendance ajoutée implicitement ; tout consommateur choisi doit satisfaire sa conformité.
