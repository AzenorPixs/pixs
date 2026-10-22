# Tâches — C06

La réalisation est autorisée par CISMP5 et la conception validée par CGPT.
Les coches ci-dessous sont adossées aux preuves natives, sans remplacer le
gate terminal. Archivage, publication et rapport post-archive sont encore
une séquence distincte obligatoire avant toute déclaration TERMINÉ.

## 1. Revue de conception

- [x] 1.1 Revoir requirements.md et le profil C00, puis recouper le canon courant : empreintes historiques distinguées de la relecture du 22 octobre ; aucune règle canonique modifiée.
- [x] 1.2 Lever les barrières de conception avant code et valider les compléments nécessaires : sérialiseur/curseur/idempotence, Auth contextuelle sans réétiquetage, horloge réelle C03, réutilisation immuable des permissions C04, fichiers et limites documentés.

## 2. Réalisation

- [x] 2.1 Déclarer routes publiques/protégées et schémas réellement exposés : 156 opérations, OpenAPI 3.1.0 / contrat 1.0.0, index et documents bornés, garde structurelle exécutée avant construction des fabriques.
- [x] 2.2 Relier les Commands/Queries propriétaires, C03/C04/C05 réels, contexte canonique et keyset SQL après filtrage/gouvernance ; aucune promotion de contexte par token ou header.
- [x] 2.3 Relier idempotence durable et migration additive 0003, résultat initial complet, conflit/rollback/réconciliation sans second effet, erreurs stables et localisation français/anglais.
- [x] 2.4 Tester sans frontend : rejeu, divergence, refus privés/inter-tenant, ordonnance SQL, cookie/CSRF/Bearer, activité C03 et renouvellement, tenant/scope/Root, ACL et concordance contrat-serveur.

## 3. Preuves et garde de clôture

- [x] 3.1 Exécuter les vérifications applicables : 166 unitaires OK, 192 cas PostgreSQL sur neuf recettes OK, cleanup/conns_closed vrais, 33 fichiers Python compilés ; strict C06 valide avant alignement documentaire. Les contrôles stricts et documentaires finaux restent à consigner avant archive.
- [x] 3.2 Vérifier isolation et refus ; bilans masqués sans valeurs Auth brutes ; identifier les doubles C09/C10, le setup C08 et les non-applicables Jobs/Bulk/Frontend/TLS réseau/P0 complet dans requirements.md et design.md.
- [x] 3.3 Examiner le périmètre et les effets exacts par mandats natifs et SHA, préserver les changements préexistants ; aucune opération Git ni changement de configuration, aucun frontend ni déploiement.
- [x] 3.4 Vérifier les autorisations avant les seules opérations engagées et cadrer la séquence terminale CISMP5 : archive C06, publication CAB et rapport distinct STATISTIQUES.md sont autorisés sous leurs mandats ; Git, déploiement et prochain change restent hors périmètre.

## Séquence terminale post-archive — obligation distincte

Le rapport STATISTIQUES.md n'est pas déclaré produit par ces coches.
Après preuve d'archive, sa création et sa vérification UTF-8/LF, six sections,
totaux et quotas restent obligatoires, puis publication/gate individuel,
désarmement et libération. Le checkpoint et le rapport réel font foi de
cette clôture ; aucune archive seule ne vaut TERMINÉ.

## Preuves de réalisation

- Neuf recettes PG, 192 cas : call_01a1612c0a267426b2a7213b01d628b0.
- Unitaires finaux, 166 tests : call_01a1612dc5ca722cbd04fc7b39425507.
- py_compile, 33 fichiers : call_01a1612f3f457159936f1edc70d3509c.
- Strict C06 avant alignement : call_01a161311fd4740682a8e9bf65c6c538.
- Détails, versions et limites : design.md et requirements.md ; sorties natives dans le checkpoint scopé du RUN.
