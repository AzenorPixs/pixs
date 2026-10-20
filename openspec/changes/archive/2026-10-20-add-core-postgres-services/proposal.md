# C02 — Primitives Core persistantes

## Pourquoi

User, DigitalIdentity, liaisons, groupes et appartenances sont des représentations mémoire. Les modèles backend persistants existants ne constituent pas les services Core complets.

## Modifications proposées

Ajouter modèles, contraintes et migrations propriétaires pour utilisateurs, identités, groupes, appartenances, tenants/scopes, rôles, ACL et permissions ; exposer les services publics requis. Préserver les profils structurels existants.

Le complément documentaire du 19 octobre 2026 précise ces travaux dans le [modèle logique et les contrats](design.md), la [traçabilité exigence → scénario → tâche → vérification](requirements.md) et les [tâches de réalisation](tasks.md). Il traite les six constats C02-A01 à C02-A06 de l’audit ciblé. Les recettes décrites restent à exécuter.

R01 complète le raccordement à [l’autorité de provisionnement C08](../../add-installation-and-first-configuration/design.md) : opérateur vérifié distinct du compte cible, preuves et plan liés à l’installation, première création ou réutilisation, refus et reprise bornée. C02 n’exige pas une session déjà créée du compte futur et n’accepte aucune autorité métier déduite de C01. Les cas B01–B10 enrichissent V05/V07 sans exécution ni nouveau scénario canonique.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `define-first-installable-pbo-profile`.

C00 est adopté et archivé. Les interfaces de conception avec C04, C05, C06, C09 et C10 sont détaillées dans `design.md` : elles ne constituent pas des dépendances inverses de réalisation. C02 peut fournir des primitives non exposées avant leur intégration ; l’activation des opérations attend les garanties applicables de sécurité, d’audit et de gouvernance. C01 n’autorise aucune mutation métier par son exception technique INSTALLER.

## Impact

Périmètre de réalisation futur : Conserver la distinction User/DigitalIdentity et les UUIDv7 ; porter les données Core dans PostgreSQL avec propriétaire explicite, contraintes et services publics. Séparer scopes/platform/tenant, rôles, ACL et permissions ; créer les migrations après revue du schéma, sans écrire les tables d’un autre composant.

Le périmètre documentaire comprend `proposal.md`, `design.md`, `requirements.md` et `tasks.md` de C02 et C08 et leurs synthèses dans PROJECT.md, TECHNICAL.md et README.md. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Le canon et `skip_specs: true` restent inchangés. Les validations de conception et de R01 ne lancent aucune implémentation ni production de code ; les tâches de réalisation restent non cochées.

## Critères de sortie de réalisation future

Les vérifications V01 à V12 de `design.md` relient la régression des profils purs, les contraintes UUIDv7 et cardinalités, l’isolation tenant/scope, les contrats déclarés, les mutations intégrées, la gouvernance et les migrations à leurs tâches. Les preuves distinguent unités, PostgreSQL réel et intégration avec les lots propriétaires. Aucun succès mémoire ne remplace une preuve persistante ni une qualification C17.

## Décisions de conception et suite documentaire

Les options A de D01 à D04 sont adoptées le 19 octobre 2026 : stockage Core avec `PixsCoreConfig`/`pixs_core`, contrats séparés par domaine, transactions/verrous déterministes et politique restrictive avec suppression logique par défaut. `design.md` distingue ces choix acquis des schémas physiques, signatures, paramètres et preuves restant à détailler. Aucun de ces détails ne rouvre automatiquement une orientation adoptée. Aucune réutilisation implicite du modèle User de Django comme fusion de l’identité Pixs. Cette adoption est documentaire et n’autorise aucune réalisation.

## Réalisation locale et clôture du 20 octobre 2026

L’invocation 1CISMP1 a ensuite autorisé l’implémentation de ce seul change, distinctement de sa préparation documentaire. Modèles, migration initiale, services, QUERY et raccordement fermé R01 sont réalisés ; les [preuves natives et limites](VALIDATION.md) relient les 72 exigences/89 références à leur contribution C02. Aucun canon n’est modifié et skip_specs reste vrai. Les intégrations C03–C10 et C16–C19 conservent leurs conditions d’activation ; ni P0 ni cycle global complet ne sont annoncés. Archivage, statistiques vérifiées et gate restent la clôture de ce seul RUN, sans change suivant ni arrêt d’OpenCode partagé.
