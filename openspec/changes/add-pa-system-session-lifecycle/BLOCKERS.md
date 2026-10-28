# BLOCKERS — add-pa-system-session-lifecycle

Date du constat : 2026-10-26T14:43:00Z. Informations d’audit datées du 2026-10-26T14:14:16Z.

Identité : prompt 1CISMP3 et CISMP.md, sous-job RSMP. RUN : cismp3-pixs-01a17557c728. Session : ses_e88532cdcffeUt80NL4PSM1isd. Change : add-pa-system-session-lifecycle.

Références relatives : [design](./design.md), [contracts](./contracts.md), [session-integration](./session-integration.md), [requirements](./requirements.md), [delta](./specs/pixs-agent/spec.md), [tasks](./tasks.md). Checkpoint : [state.json](../../../output/cismp/cismp3-pixs-01a17557c728/state.json), clé ecosystem_validation_ops à venir ; les CLI obtenus dans le checkpoint constitueront l’état ultérieur.

Motif : surtout adoption fonctionnelle de la nouvelle spécification et prérequis runtime non qualifiés. Le code autorisé reste possible après adoption, sans attendre sa propre qualification future. Rapport de préparation de clôture ; gate et libération pas encore faits. Future clôture sous réserve de fin de l’unité documentaire.

## Travail achevé et limites

- Audit tâche 1 réalisé en lecture seule, rapport auditmsg_17890245c001aSz928o0XhAM61.
- Revue complète des 9 sources publiques AST et SHA au checkpoint : Agent contracts, lifecycle, ports, service ; pa_native build_profile, cli, provisioning_contracts ; pzt contracts, ports. Frontières et classes confirmées, pas fonctionnement ni transport. Références aux documents : proposal, design, contracts, session-integration, requirements, delta et tasks.
- Nouvelle spécification intégrée objets et catalogue définie et proposée, à adoption fonctionnelle avant implémentation. RSMP courant sans code. Aucune preuve produit.
- C7 : RUN cismp7-pixs-023c11510a274b19, change add-pa-native-build-and-component-composition. D14 source .pyx non qualifiée. PAM et logind PA03 sont notre travail propre ; C7 fournit build, ABI, distribution, consommateur PA et gardes, rien à réutiliser comme port logind.
- C2 : RUN cismp2-pixs-797dcac8c8814e27, reçu 77. Codec de forme seul et 44 unitaires rapportés par le propriétaire, pas nos propres tests. Transport, exécutant durable, fencing et provision d’autorité non qualifiés au point d’usage.
- Z12, C08 et A07 non attribués absents sans preuve du propriétaire ; candidats à vérifier selon design, pas cause établie.
- Environnements Debian13 et Windows non vérifiés, pas déclarés indisponibles. Contrats et documents non transport.

## Statut

PARTIELLEMENT RÉALISABLE documentaire. Contrôles OpenSpec documentaires avant clôture restants. Pas de contrainte Windows bloquant le code Linux.

## Tâches non validées 2 à 10

| Tâche | Libellé exact | Dépendances et travail restant | Constat et preuves | Phase | Contrôles et reprise |
|---|---|---|---|---|---|
| 2 | Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test. | Travail PA03 : sélection profil Debian13 et contrat Windows. Documents sources proposés non adoptés, distinct de sans preuve universelle. Adoption nouvelle spécification requise. | Non validée, sans preuve. | réalisation | Vérifier manifests et profil ; reprise après tâche 1 et adoption fonctionnelle. |
| 3 | Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire. | Travail PA03 : barrières et choix. Documents sources proposés non adoptés. PA01 au point d’usage non vérifié. | Non validée, sans preuve. | réalisation | Revue conception ; reprise après tâche 2. |
| 4 | Définir les contrats, schémas, propriétaires et adapters du périmètre : Délais et annulations, modes start/stop/daemon, fermeture bornée et isolation des sessions/privilèges ; respecter le rôle spécifique de pzt-daemon. | Travail PA03 : contrats et schémas. Documents sources proposés non adoptés. | Non validée, sans preuve. | réalisation | Revue invariants ; reprise après tâche 3. |
| 5 | Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées. | Travail PA03 : module PAM C et raccord logind. Dépendances PA01, PA02, Z12, C08, A07 au besoin. C7 sans port à réutiliser. C2 forme seule. | Non validée, sans preuve. | réalisation | Syntaxe, unités et intégrations ; reprise après tâche 4 et dépendances au besoin. |
| 6 | Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants. | Travail PA03 après tâche 5, directe. | Non validée, non exécutée. | tests | Injecter pannes ; reprise après tâche 5. |
| 7 | Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles. | Prérequis tâche 6 direct et tâche 5 indirect, code PA03 inexistant. Tests produit futurs, pas contrôles documentaires préparatoires assimilés. | Non exécutés. | tests | Consolider résultats ; reprise sur preuves locales. |
| 8 | Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée. | Non exécutée, tous critères NON PROUVÉS. Dépendances tâches 5, 6 et 7, vrai port, provision, vérification, durabilité, fencing, transport, artefact, environnement. DTO et mocks ne qualifient pas. | Non validée, non exécutée. | intégration | Cas profil ; reprise après artefacts et environnements réels. |
| 9 | Vérifier la sortie attendue : Arrêt pendant délai/traitement ; sessions concurrentes indépendantes ; verrouillage distinct de fermeture ; pas de succès après coupure forcée. | Dépend tâches 8, 7, 6 et 5. Travail PA03 après tâche 8. | Non validée, non exécutée. | intégration | Revue croisée ; reprise après tâche 8. |
| 10 | Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre. | Dépend tâche 9 et tâches 8, 7, 6 et 5. Travail PA03 après tâche 9. | Non validée, non exécutée. | finale | Examen fichiers ; reprise après tâche 9. |

## Contrôles et ressources

Réussis : audit1 lecture seule et revue 9 sources. Non exécutés : contrôles OpenSpec finaux du lot 7 fichiers. Disponibilités non vérifiées, refs C7 et C2 globales conservées. Prochaine étape : contrôles documentaires puis revue CGPT. Ressources : réservation détenue, accès 0 au dernier constat, aucun conteneur ni heartbeat propre créé, gate OPEN. Résultat de libération ensuite au checkpoint.

## Complément 2026-10-26 — contrôles documentaires observés, sans validation strict PASS

Tâche 1 seule validée et case 1 cochée, 9 autres tâches ouvertes. Tous documents 8 exigences et 18 scénarios relus, aucun code produit ni qualification.

CLI observés : ciblée stricte 0/1 exit 1 avec sept WARNING longueur supérieur à 500 caractères, partId prt_178ac35dd001Je2NlX8HsHVyTq ; globale standard 185/185 exit 0, partId prt_178ada83a001yUajeICOakBj4e ; globale stricte 184/185 exit 1 avec seul échec PA03, partId prt_178ae5a9f001M1BSmXgzmTGnSr. Les preuves natives font foi ; le rapport antérieur annonçant exit 0 pour le ciblé strict est corrigé en exit 1.

Motifs : ne pas relancer modèle ou CAB ni raccourcir les exigences, car selon CISMP la longueur n’est pas un critère de qualité. Pas de validation strict PASS ; la validation standard documentaire ne vaut pas fonctionnement du module.

Préparation de clôture : unités documentaires audit et revue achevées ; dernière consignation et validation standard ciblée encore à faire. Ensuite aucune unité indépendante autorisée en RSMP sans code ; nouvelle adoption fonctionnelle des objets et catalogue nécessaire avant implémentation ; contraintes runtime à vérifier aux points d’usage, pas absence universelle.

Classement PA03 à la reprise : ÉTAT NON VÉRIFIABLE tant que manquent des contrôles ciblés actuels, pas aucun travail réalisable universel ; nos unités RSMP sont épuisées après la suite prévue. Contrôles produit non exécutés ; archive et statistiques d’archive non applicables au change ouvert. Gate OPEN jusqu’aux preuves ; désarmement et libération non encore faits ; résultats au checkpoint après.

Première étape de reprise explicitement demandée : lire ce BLOCKERS, revalider l’adoption des contrats, les dépendances affectées, le rôle et profil et les preuves. Un nouveau CISMP général après clôture avec resélection argumentée peut choisir un autre candidat ; une demande visant explicitement PA03 conserve la cible.
