# C13 — Panneau d’administration utilisable

## Pourquoi

La route UI actuelle affiche le shell de développement ; elle ne démontre pas un panneau /admin/ de première configuration et d’administration Core.

## Modifications proposées

Livrer /admin/, première configuration, gestion des primitives Core, route administrable et secours ; utiliser les mêmes contrats que la CLI et l’API, avec visibilité tenant et contrôle ordinaire/Super Admin.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-installation-and-first-configuration`.
- `enforce-core-data-governance-and-lifecycle`.
- `compose-modular-frontend-with-core-api`.
- `complete-shared-ui-i18n-and-accessibility`.

## Impact

Périmètre de réalisation futur : Construire le panneau avec les mêmes API/Commands que les autres façades ; conserver droits ordinaires et exception Super Admin dans son seul périmètre. Route initiale /admin/ administrable sans collision ; santé réservée selon niveau ; première configuration réservée au compte fonctionnel ; états/messages et erreurs localisés.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Installation → connexion Super Admin → première configuration → NORMAL → administration ordinaire ; changement route sans collision et ancienne route refusée/auditée ; état santé sans credential ; aucun second compte ni transfert de privilège.

## Barrière de conception

Catalogue exact d’écrans/actions, transitions et changement de route sous contrats publics ; ne pas activer implicitement l’administration Django ni créer un second modèle de permissions.
