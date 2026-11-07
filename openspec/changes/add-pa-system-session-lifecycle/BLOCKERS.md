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

## Reprise 2026-10-30 — audit dépendances documentaire sans coche

Identités : RUN cismp3-pixs-01a17557c728, job pa03-reprise-e053f05273b24149a5f4302c50ab9d32, session ses_e88532cdcffeUt80NL4PSM1isd, root /home/devops/datas/pixs, génération 1371, change add-pa-system-session-lifecycle.

Source audit : rapport réel msg_18b23db03001gc6SiNQcvyEF9q, analyse documentaire seulement, aucune case cochée. Sources SHA au checkpoint. Accès READ HELD read-audit-pa03-df8b674ee58645ccac5af6aaa77bda4b libéré. Aucune surveillance ni réponse human requise avant docs autorisés.

Sources publiques relues, chemins et lignes observées : openspec/changes/add-pa-system-session-lifecycle/BLOCKERS.md, tasks.md, proposal.md, design.md, session-integration.md, requirements.md, contracts.md, specs/pixs-agent/spec.md, .openspec.yaml ; openspec/changes/add-pa-bootstrap-and-authority-binding/BLOCKERS.md et tasks.md ; openspec/changes/add-pa-native-build-and-component-composition/VALIDATION.md partielle ; openspec/specs/pixs-agent/spec.md ; openspec/specs/pzt/spec.md ; openspec/BATCH_CODES.md ; src/pixs/agent/ports.py lignes 1-171 profils serveur explicites sans transport ; src/pixs/agent/service.py lignes 233-244 _refuse_pzt PZT_TRANSPORT_UNAVAILABLE et dispatch refusé ; src/pixs/pa_native/build_profile.py lignes 19-29 _ROLES 4 exécutables et _CATALOGUE 3 opérations, lignes 124-136 target debian13 x86_64 physical/vm et toolchain ; src/pixs/pa_native/cli.py lignes 8-13 4 exécutables et modes ; src/pixs/pa_native/provisioning_contracts.py 17 champs forme fermée ; src/pixs/pa_native/provisioning_bindings.py comparaison seule ; src/pixs/pa_native/provisioning_store.py magasin POSIX liaison unique ; src/pixs/pzt/contracts.py structure seule ; src/pixs/pzt/ports.py verifier et gate sans cryptographie.

Retour PA01 selon rapport : Journal21 natif 21 PASS fichiers flock fsync CPython3.14.9, sans TPM ni autorité ni SQL ni PZT ni session PAM ni logind ; graphes 142 et codecs formes et bindings FOURNIS, pas garanties réelles, pas admission ni retrait ni signature ni transport qualifiés.

Retour PA02 selon rapport : 102 méthodes historiques 44 codec plus 28 comparateur plus 30 backend IO du 26/10, six sources inchangées au 30/10, backend POSIX 30 PASS local seul ; aucune admission ni origine ni fencing ni transport ni autorité qualifiés livrés ; classification TOUJOURS BLOQUÉ conservée.

Différences réelles depuis 26/10 : Journal21 natif confirmé fichiers seuls, pas garanties étendues ; 102 méthodes restent historiques, pas nouveaux PASS ; BLOCKERS PA03 SHA 85127c1cce9af09e7b6d1050184353e5efe8ea7808cf1b2d1a80fa51e11606b8 et tasks 1/10 conservés ; aucune fausse absence universelle.

Corrections : Z12, C08 et A07 à vérifier au point d'usage selon contrats et propriétaires, pas causes absences prouvées ; PAM et logind sont travail propre PA03, pas à attendre des autres ; code PA03 attesté BATCH, pas non attribué.

État adoption : objets pa_session_config 1.0.0, pa_operation_envelope 1.0.0, pa_operation_result 1.0.0 et catalogue pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0, pa_reconcile 1.0.0 toujours définis et proposés, non adoptés fonctionnellement. Pas de code ni source ni PAM hôte ni test produit ni archivage.

Matrice 9 tâches non validées, libellés exacts recopiés depuis tasks :

- 2 | Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test. | Dépendances : adoption objets et catalogue INSATISFAITE, manifests et graphe au point d'usage NON VÉRIFIABLES, précondition propre sélection profil. | Constat : INSATISFAIT. | Phase réalisation. | Contrôles et reprise : vérifier manifests et profil contre contrats, reprise après tâche 1 et adoption fonctionnelle.

- 3 | Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire. | Dépendances : tâche 2 directe, PA01 au point d'usage NON VÉRIFIABLE, précondition propre revue conception. | Constat : INSATISFAIT. | Phase réalisation. | Contrôles et reprise : revue conception et refus du profil, reprise après tâche 2.

- 4 | Définir les contrats, schémas, propriétaires et adapters du périmètre : Délais et annulations, modes start/stop/daemon, fermeture bornée et isolation des sessions/privilèges ; respecter le rôle spécifique de pzt-daemon. | Dépendances : tâche 3 directe, précondition propre invariants et catalogue proposé. | Constat : INSATISFAIT. | Phase réalisation. | Contrôles et reprise : revue invariants et structure, reprise après tâche 3.

- 5 | Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées. | Dépendances : tâche 4 directe, PA01 et PA02 et Z12 et C08 et A07 au besoin NON VÉRIFIABLES, C7 sans port logind, C2 forme seule, précondition propre module PAM C et raccord logind. | Constat : INSATISFAIT. | Phase réalisation. | Contrôles et reprise : syntaxe et unités et intégrations au branchement, reprise après tâche 4 et dépendances au besoin.

- 6 | Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants. | Dépendances : tâche 5 directe, fencing et concurrence INDIRECTES. | Constat : NON VÉRIFIABLE non exécuté. | Phase tests. | Contrôles et reprise : injecter pannes et concurrence, reprise après tâche 5.

- 7 | Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles. | Dépendances : tâches 5 et 6, code inexistant. | Constat : NON VÉRIFIABLE non exécuté. | Phase tests. | Contrôles et reprise : consolider résultats sur preuves locales.

- 8 | Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée. | Dépendances : tâches 5 et 6 et 7, vrai port et provision et durabilité et fencing et transport et artefact et environnement NON VÉRIFIABLES. | Constat : NON VÉRIFIABLE non exécuté. | Phase intégration. | Contrôles et reprise : cas profil sur artefacts et environnements réels.

- 9 | Vérifier la sortie attendue : Arrêt pendant délai/traitement ; sessions concurrentes indépendantes ; verrouillage distinct de fermeture ; pas de succès après coupure forcée. | Dépendances : tâches 8 et 7 et 6 et 5. | Constat : NON VÉRIFIABLE non exécuté. | Phase intégration. | Contrôles et reprise : revue croisée, reprise après tâche 8.

- 10 | Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre. | Dépendances : tâche 9 et tâches 8 et 7 et 6 et 5. | Constat : NON VÉRIFIABLE non exécuté. | Phase finale. | Contrôles et reprise : examen fichiers et preuves, reprise après tâche 9.

Classement : TOUJOURS BLOQUÉ pour finalisation. Seules unités documentaires et audit autorisées réalisées. Aucun résultat CLI 2026-10-30 encore exécuté, historiques 26 conservés : ciblée stricte 0/1 exit 1 sept WARNING longueur, globale standard 185/185 exit 0, globale stricte 184/185 exit 1.

Anciennes mentions pas de statistiques obligatoires supersédées par CISMP courant qui impose STATISTICS dans change ouvert. STATISTICS.md cumulatif depuis début du change et toutes reprises dédupliquées avec lacunes N/A attendu à création avant libération, pas déjà écrit. Lien checkpoint préexistant conservé. Ressources propres READ libérées, pas de test créé. Gate OPEN jusqu'à clôture CGPT.

Ligne carte PA03 À VÉRIFIER historique du 26 à actualiser si ce constat daté affecte état actuel et conditions, sans assimiler maintenance à qualification.


## Complément 30 oct 2026 — rapprochement normatif du delta sans modification

Ancien SHA 39f80be8 et nouveau SHA 7d3bab1b constatés avec différence d octets. Le delta courant était déjà restructuré au premier READ d audit du 30 : 8 exigences et 18 scénarios originaux TOUS préservés verbatim, plus 7 scénarios Garanties détaillées ajoutés, soit 25 ACTUELS. Les 8 paragraphes normatifs anciens se reconstruisent EXACTEMENT depuis intro et THEN des détails, avec préservation lexicale prouvée. Auteur et date et autorisation du remaniement NON DÉDUITS. Aucune modification du delta par ce RUN, pas d adoption fonctionnelle implicite. Le strict courant 1 sur 1 exit 0 sans issue est observé, contrairement à l historique du 26 avec warnings, sans prétendre norme delta octets inchangée. Correction de l audit msg_18b23db03001gc6SiNQcvyEF9q sur le décompte et sur le claim de SHA inchangée. Preuve checkpoint resume_20261030.normativeReconciliation. Les 8 clauses et 18 scénarios anciens sont préservés lexicalement, sans autorité déduite, avec conditions d adoption et garanties runtime inchangées. Preuves CLI actuelles : standard call_01a18b6dc61d7749aa954b8377422f26 1 sur 1 exit 0, strict call_01a18b6fbb52747fbdae9f8005618a29 1 sur 1 exit 0, contrôle documentaire pas produit.

