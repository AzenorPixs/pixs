# C16 — Migrations, mise à niveau et restauration

## Pourquoi

Des migrations bornées existent, mais aucune recette de restauration produit cohérente avec gouvernance, travaux et composition n’est démontrée.

## Modifications proposées

Déclarer contrats et ordre exclusif des migrations, reprises, expansion/contraction ; stratégie sauvegarde du profil avec RPO/RTO déclarés ; restauration isolée et réapplication des gouvernances avant exposition.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-installation-and-first-configuration`.
- `add-reference-worker-scheduler-and-event-delivery`.
- `enforce-core-data-governance-and-lifecycle`.
- `add-runtime-observability-and-operations`.

## Impact

Périmètre de réalisation futur : Versionner contrats/plans de migration, ordre exclusif, reprise et contraction séparée. Sauvegarder les périmètres réellement livrés puis restaurer isolément, réappliquer effacements/holds avant exposition. Retour arrière applicatif seulement si matrice compatible ; sinon restauration explicite confirmée/auditée.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Installation et mise à niveau interrompues puis reprises ; contraction prématurée refusée ; origine compatible explicitée ; restauration mesurée sans résurrection ; rollback seulement si matrice le prouve, sinon restauration confirmée ; aucune downgrade automatique.

## Barrière de conception

RPO/RTO et rétention du profil, stratégie de sauvegarde et origines/version compatibles ; ne pas sélectionner un outil ni rétrograder une base implicitement.
