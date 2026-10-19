# C08 — Installateur et première configuration

## Pourquoi

manage.py est une entrée Django sans réglage par défaut ; aucun parcours INSTALLER/première configuration complet n’est démontré.

## Modifications proposées

Livrer le parcours CLI INSTALLER, marqueur externe, état FIRST_CONFIGURATION en base et transitions NORMAL/MAINTENANCE ; provisionner tenant et compte fonctionnel unique ; plans confirmés et reprise. Les mutations d’amorçage pré-session ont leur acteur opérateur explicitement vérifié, sans dépendance circulaire à une session non créée.

Le complément documentaire R01 du 19 octobre 2026 définit le [contrat d’autorité C08/C02](design.md) : acteur et preuves de confiance, plan/installation/actions liés, confirmations, écritures Core bornées, audit et reprise. La future identité du compte cible ne sert pas d’acteur déjà authentifié. C01 reste limité à ses actions techniques ; aucune permission métier n’en est déduite.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

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

Le complément autorise uniquement les documents C02/C08 concernés et leurs synthèses de cadrage. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Le canon et `skip_specs: true` restent inchangés ; les tâches de réalisation restent non cochées.

## Critères de sortie de réalisation future

Base absente/conforme/migrable/incompatible ; confirmations requises ; mots de passe différents refusés ; conservation du Super Admin existant ; reprise sans doublons ; marqueur invalide interdit NORMAL sans relancer implicitement INSTALLER.

La recette R01 B01–B10 relie ces critères aux preuves d’opérateur et aux gardes C02 : première création sans session préexistante, refus d’autorité ou de plan invalides, conservation, concurrence, rejeu divergent, crash avant/après commit ou marqueur, audit et fin de l’autorité d’initialisation. Aucun cas n’est déclaré exécuté.

## Barrière de conception

R01 fixe la frontière et les informations du contrat d’autorité ; les mécanismes concrets de preuve et leur mapping C03/C04, formats du marqueur/checkpoint, paramètres et ports d’audit restent à détailler sous ces règles avant réalisation. Une preuve impossible à vérifier garde la branche refusée ; aucune extension implicite de C01 ni dérogation normative n’est inventée.
