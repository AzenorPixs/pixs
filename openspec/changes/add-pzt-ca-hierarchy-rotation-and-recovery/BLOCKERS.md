# BLOCKERS — add-pzt-ca-hierarchy-rotation-and-recovery

Prompt : 1CISMP6 / CISMP1320 SHA a87db708bf1812d457f334b8e0b7de6cbeb440cfb555aeeea750ba6c9e8a5e89

Date constat UTC : 2026-10-26T16:50:33.314075+00:00
RUN : cismp6-pixs-9dd1542d4c0542f2
Session : ses_e86fbafd4ffea5n3Iw1SpbyDRx
Job : job-89862b20df4a4974aac32a3b3a1db0d1
Checkpoint : output/cismp/cismp6-pixs-9dd1542d4c0542f2/state.json
Limite : T1 actuel seulement ; T2/T3/T4 pas automatiquement autorisés ; aucune installation/activation/Git/archive
État : TOUJOURS BLOQUÉ pour dépendances de développement/qualification manquantes. Change ouvert, non livré, non archivé. Réalisations locales partielles ont avancé (T1-A/B1/B2/C ci-dessous), sans qualification réelle.

## Preuves locales réussies (contrôles locaux seulement, aucune qualification réelle du producteur UTC)

- T1-A local_count 68 at 2026-10-26T13:17:48.887579+00:00 : cismp6-t1-1e01d7cdbf684e118d2ec4ad63690a9f / prt_178516a68001gzXC7NdSzIX4yP exit 0 ; cismp6-t1-259fd7f50ffd492eac7a89b5ac4dfbe1 / prt_17851e378001Y3UUc4so7YIcjp exit 0 ; cismp6-t1-fc39e603be074c5892891d1860ff631b / prt_17852bf99001ZFX0n5gXy9CBPo exit 0 ; cismp6-t1-761c748027394e08a8ff48b58a5d7be4 / prt_1785aedd600166hex4fY6bx6Qd exit 0.
- T1-B1 local_count 61 at 2026-10-26T14:44:23.401769+00:00 : cismp6-t1-defc4805542c43fc889fe0179d3ea4d7 / prt_1789a2b080018qr1x6MFLIyLHT exit 0 ; cismp6-t1-ca40726d834145bcb49c04af9fbabe09 / prt_1789a9465001pMtqWXdB8HtSkW exit 0 ; cismp6-t1-66b0af6f3c8344cd82ff782e038b9f7f / prt_1789b036e001Nrrh7nk312tss5 exit 0 ; cismp6-t1-12555c48c9a24960aa378746b7d3092b / prt_1789b6c74001vAAhWQYFrnEmlY exit 0 ; cismp6-t1-ea43222840fa4b93a757374151e87826 / prt_1789c0ba0001wUesG2Wlh3QPDw exit 0.
- T1-B2 local_count 52 at 2026-10-26T16:32:54.943354+00:00 : cismp6-t1-43c738c2c03c4ef1938bb848275c66b6 / prt_1790c9c32001Iqnqbr2dE6UFFY exit 0 ; cismp6-t1-8b9f68608a024399ad9237f856237852 / prt_1790d2231001mpz64KUEqImuwy exit 0 ; cismp6-t1-4dc6f65905684309a671bc81657f9291 / prt_1790dc663001dmug67D8yBaFy5 exit 0 ; cismp6-t1-e6cf4d13a3464888bd75108de671851e / prt_1790e5f6d001Z3D3ajgECVCqWJ exit 0.
- T1-C local_count 10 at 2026-10-26T16:50:33.224828+00:00 : cismp6-t1-bf8acf5a27604653a26ca95a78941180 / prt_1791cf34c001TdudfajM1t8Djo exit 0 ; cismp6-t1-2a4cd6c7ff3f49109a76f95e663ad1aa / prt_1791d757400161s2Dryc0G26aN exit 0.

Sources : src/pixs/core/time_guard.py 5b8e235f3ca47ea352db3f60869eb3a4a01e32ce4c7c605ab5c5b33df742a91e ; tests/unit/test_time_guard_delegation.py 58d47632a09594592cb3cdf7cc18373b91f80acd7a2edfe08e7f5ac9d2cbdc8f ; src/pixs/pzt_ca/native/z12_time_budget.inc f17c9f5803f57e7086026d2201022b5ea8184d4720d8ef8633327458258beebc ; tests/integration/z12/native_time_budget_check.c a9b127c1d6bc80182e1c91e32892b120e947a3465747dabef9d7c25d6861504a ; openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/RACCORDS_TEMPS_V2.md cc7fbbe463fba10899561984f007811c52ecb49fe36e1b671f923c4eaa7bfba7 ; src/pixs/pzt_ca/native/z12_time_profile.inc f05651e116a2ba7cc9c6bff6cf26a848f00faa7d2c826ae33e438f33418013f1 ; tests/integration/z12/native_time_math.c b4a4d1c2f0ecc6272b037801bd0231e34b36fcda7dbcdb4a71131b40c8162f30.
Historique conservé au checkpoint, pas réévalué ici. Profils réels rho/ancre/continuité non fournis dans preuves actuelles ; disponibilité réelle non vérifiable ici, non déclarée absente globalement.

## Refus CAB et contrôles restants

- Admission native : HTTP409 corrigés avant décision/effet sur cismp6-t1-bf8afac216ea4e9892e755f5d715bec9 : native-validation-not-correlated (ordre clés expected_revisions seulement ; mêmes valeurs et commande), native-permission-ask-required (tools:true a introduit allow, rétabli ask avant toute décision/effet) ; même demande, entrée native exacte relayée ; décision explicite approved puis HELD puis once/exit0 ; aucun effet hors mandat ni rejeu. Refus de décision : aucun ; toutes décisions métier émises approved. Autres incidents historiques conservés au checkpoint, récupération session native réussie sans replays.
- Contrôles restants non exécutés (qualification réelle) : observation/consommation natives avec composition/liaisons résolues effectives, continuité/provenance/profils réels et validations, NTS/TLS/intervalles réels, intégrations/conformités, sortie attendue, matrice preuves. Helpers purs déjà prouvés ne les remplacent pas.
- Travail propre restant déclaré en tant que tel : gardes Auth/Agent/PZT non branchées, observation/consommation natives, raccord/qualification avec PA01 TimeService v2 manquant comme dépendance prouvée, jamais sous fausse cause normative.

## Tâches 3-10 non validées

| ID | Libellé exact | Dépendances directes/indirectes et faits datés seuls | Phase empêchée | Contrôles ciblés | Conditions vérifiables de reprise |
|---|---|---|---|---|---|
| 3 | Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire. | choix/contrats adoptés ; validation globale du tout périmètre pas réévaluée, cause globale de blocage non établie ici ; préconditions réelles unités natives et qualification insatisfaites/non vérifiables ; limite T1 validé partiel, futur T2/T3/T4 soumis validations propres | décision | revue documentaire stricte | NFDOC/Codex existants, sans réouvrir choix adoptés |
| 4 | Définir les contrats, schémas, propriétaires et adapters du périmètre : A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine. | choix/contrats adoptés ; validation globale pas réévaluée, cause globale non établie ; préconditions natives et qualification insatisfaites/non vérifiables ; limite T1 partiel, T2/T3/T4 validations propres ; futurs time_guard non preuves de lacune | réalisation contrats | syntaxe + types/bornes/refus | mandats T1 unitaires seuls ; T2/T3/T4 non auto-autorisés |
| 5 | Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées. | PA01 TimeService v2 manquant, dépendance prouvée au 2026-10-26, time_service_local_path src/pixs/pa_native/time_service.pyx absent ; A07/A12/canal/registre/contrôleur requis | réalisation | unités + intégration nominale/refus sur sources réelles | sources réelles + autorisations, sans inventer API |
| 6 | Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants. | §15.5 IN_DOUBT/réconciliation, fencing et D6 sans réouverture ; indirectes via réalisation 5 non validée ; fondations A07/A12 etc non évaluées globalement ici | reprise | panne/concurrence/réponse perdue/crash | effets autorisés, composition effective |
| 7 | Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles. | tâches 4-6 non validées ; T1-A 68, B1 61, B2 52, C 10 ci-dessus ne les couvrent pas | tests | consolider sans extrapoler | après 4-6 |
| 8 | Exécuter les intégrations/conformités du profil : Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier. | NTS/TLS/producteur réels, bornes 600s/1s, continuité/provenance/profils réels non fournis ici ; indirectes via réalisation 5 et intégration 8 non validées ; fondations A07/A12 etc non évaluées globalement ici | intégration | cas §15.5/D14-D18 sur réels | environnements/effets autorisés |
| 9 | Vérifier la sortie attendue : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot. | exclusion vérifiée, recertification, adoption/retrait D6 | validation | revue croisée scénarios/preuves | après 5-8 |
| 10 | Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre. | matrice preuves/versions, gate OPEN au constat | clôture | examen fichiers/preuves/périmètre | autorisations propres, gate VALIDÉ requis |

## Ressources au constat (avant clôture)

reservation_version 1310, state RESERVED, gate OPEN, job_armed true, current_mandate null, own_active_effects 0, OpenCode préservé partagé avec autres RUN, time_service_local_path absent comme ci-dessus, qualified_profiles non fournis ici. Résultat gate/disarm/release sera consigné au checkpoint après rapport, sans écriture post-libération.

## Prochaine étape et conditions concrètes (pas d'attente active)

1. Contrôler producteur PA01 effectif consommable.
2. Renseigner profils/provenance/continuité avec valeurs et preuve.
3. Établir composition/liaisons courantes authentiques.
4. Obtenir autorisation phase concernée avant tests à effets.
5. Réévaluer preuves affectées après chaque effet.
