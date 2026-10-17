# C19 — Identité signée et release vérifiable

## Pourquoi

Le dépôt ne déclare pas de release ou paquet utilisable publié ; une recette de sources ne prouve pas une identité de distribution installable.

## Modifications proposées

Ajouter signature/provenance/inventaire et vérification avant installation, immuabilité, canaux, rotation/révocation et support ; recette finale du paquet construit, puis publication explicitement autorisée.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `qualify-first-pbo-composition`.
- `build-first-pbo-pfo-debian-package`.

## Impact

Périmètre de réalisation futur : Associer canal expérimental local, version, provenance, inventaire, composition et artefact immuable. Vérifier signature/empreinte/révocation avant installation et mise à niveau ; autorités et matériaux de confiance distincts. Déclarer support/limites et corréler la recette C17 au paquet C18. Publication seulement sur instruction explicite ultérieure.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Installation du paquet final depuis environnement vierge ; empreinte/signature invalide ou révoquée rejetée ; canal non autorisé refusé ; provenance et inventaire vérifiables ; aucun secret embarqué ; version/support et preuve finale corrélés.

## Barrière de conception

Identités/autorités de signature, mécanisme de provenance/inventaire et support ; aucun secret, signature ou publication pendant la préparation.
