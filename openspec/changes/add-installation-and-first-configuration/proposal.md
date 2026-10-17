# C08 — Installateur et première configuration

## Pourquoi

manage.py est une entrée Django sans réglage par défaut ; aucun parcours INSTALLER/première configuration complet n’est démontré.

## Modifications proposées

Livrer le parcours CLI INSTALLER, marqueur externe, état FIRST_CONFIGURATION en base et transitions NORMAL/MAINTENANCE ; provisionner tenant et compte fonctionnel unique ; plans confirmés et reprise. Les mutations d’amorçage pré-session ont leur acteur opérateur explicitement vérifié, sans dépendance circulaire à une session non créée.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-pbo-runtime-secret-provider`.
- `add-core-postgres-services`.
- `add-initial-authentication-and-sessions`.
- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `activate-reference-runtime-composition`.

## Impact

Périmètre de réalisation futur : Séparer marqueur externe d’installation et état FIRST_CONFIGURATION en base. La CLI présente les plans, confirme toute création/migration/destruction concernée et reprend l’état persistant. Authentifier explicitement l’opérateur d’amorçage sans dépendre circulairement d’une session pas encore créée ; valeurs saisies remplacées par références privées.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Base absente/conforme/migrable/incompatible ; confirmations requises ; mots de passe différents refusés ; conservation du Super Admin existant ; reprise sans doublons ; marqueur invalide interdit NORMAL sans relancer implicitement INSTALLER.

## Barrière de conception

Format/propriétaire du marqueur externe, identité opérateur d’amorçage et journal de reprise ; politique de confirmations conforme au canon. Aucun effacement, stockage de secret ou manipulation de base pendant cette préparation.
