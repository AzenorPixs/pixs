# Tâches — PA03

Une tâche sur dix validée : tâche 1 auditée et cochée sur validation CGPT, tâches 2 à 10 ouvertes. Voir [BLOCKERS.md](./BLOCKERS.md).

- [x] 1. Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.
- [ ] 2. Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.
- [ ] 3. Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.
- [ ] 4. Définir les contrats, schémas, propriétaires et adapters du périmètre : Délais et annulations, modes start/stop/daemon, fermeture bornée et isolation des sessions/privilèges ; respecter le rôle spécifique de pzt-daemon.
- [ ] 5. Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.
- [ ] 6. Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.
- [ ] 7. Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.
- [ ] 8. Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.
- [ ] 9. Vérifier la sortie attendue : Arrêt pendant délai/traitement ; sessions concurrentes indépendantes ; verrouillage distinct de fermeture ; pas de succès après coupure forcée.
- [ ] 10. Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Délais et annulations, modes start/stop/daemon, fermeture bornée et isolation des sessions/privilèges ; respecter le rôle spécifique de pzt-daemon.
- Résultat de référence : Arrêt pendant délai/traitement ; sessions concurrentes indépendantes ; verrouillage distinct de fermeture ; pas de succès après coupure forcée.
- Cas de contrôle du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues. | Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts. |
| 2 | Tâche 1 techniquement validée avec ses propres preuves | Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite. | Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet. |
| 3 | Tâche 2 techniquement validée avec ses propres preuves | Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse. | Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code. |
| 4 | Tâche 3 techniquement validée avec ses propres preuves | Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites. | Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve. |
| 5 | Tâche 4 techniquement validée avec ses propres preuves | Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu. | Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici. |
| 6 | Tâche 5 techniquement validée avec ses propres preuves | Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré. | Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante. |
| 7 | Tâche 6 techniquement validée avec ses propres preuves | Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible. | Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux. |
| 8 | Tâche 7 techniquement validée avec ses propres preuves | Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation. | Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément. |
| 9 | Tâche 8 techniquement validée avec ses propres preuves | Arrêt pendant délai/traitement ; sessions concurrentes indépendantes ; verrouillage distinct de fermeture ; pas de succès après coupure forcée. | Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif. |
| 10 | Tâche 9 techniquement validée avec ses propres preuves | Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte. | Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Addendum PA03 — portée documentaire des tâches après orientations et intégration écosystème

Les dix cases ci-dessus restent non cochées. Aucune tâche n’est lancée par cette préparation. La simple rédaction ne vaut pas tâche 1 implémentée ; aucun test produit prétendu. Aucune intégration et qualification PA03 prouvée. Le code du module n'attend ni sa propre qualification future ni un environnement Windows non sélectionné en réalisation.

Critères et renvois réellement nécessaires : objets pa_session_config 1.0.0, pa_operation_envelope 1.0.0 et pa_operation_result 1.0.0 en [session-integration.md](./session-integration.md) ; catalogue pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0 avec sélecteur operation et operation_version 1.0.0 ; delta en [specs/pixs-agent/spec.md](./specs/pixs-agent/spec.md) ; déploiement et configuration par opérations typées avec expected_revision et expected_preimage_ref ; profils Linux Debian13 x86_64 et contrat cible Windows avec environnements réels propres.

## Bilan corrigé 2026-10-26 — audit1 sourcé, en attente de finalisation si clôture différée après contrôles

Change ouvert, en attente de finalisation si clôture différée après contrôles ; pas clôturé avant gate. Dix cases ci-dessus restent ouvertes. Tâche 1 réellement auditée en lecture seule, reste consignation physique et validation CGPT avant cochage. Contrôles OpenSpec finaux du lot 7 fichiers à effectuer après bilan et cochage autorisé ; résultats référencés au checkpoint, non affirmés réussis ici. Aucun SDK, installation, code, exécution ou Git.

Audit1 : rapport auditmsg_17890245c001aSz928o0XhAM61 ; CGPT a vérifié en lecture complète sans import produit les neuf fichiers Python publics, AST et SHA au checkpoint, soit Agent contracts, lifecycle, ports et service, pa_native build_profile, cli et provisioning_contracts, pzt contracts et ports ; ils confirment frontières et classes annoncées, pas fonctionnement et transport. systemd_observation.pyx lu en en-tête seul, pas de qualification par présence. Frontend en repérage ciblé seul, routes dynamiques hors périmètre non exclues, aucune UI universelle conclue. Décisions : réutiliser Agent PBO, CLI et profil au lieu de les recréer. Module PAM C et raccord logind et session PA03 sont notre travail ; C7 fournit build, ABI, distribution, consommateur PA et gardes, sans port logind prêt donc rien à réutiliser, pas d'autre agent censé produire notre module ; C2 fournit contrats et codec de forme, coordination C7 et C2, pas identité et persistance et fencing et transport.

Matrice exclusive lue dans fichiers actuels, mapping statique et non exécuté, méthode titres et comptes lus effectivement, pas PASS :
- Delta Rôle local OS et adaptateurs : Instance isolée par session réelle, Événement non transformé en démon, Initialisation locale sans mandat distant ; source partielle Agent et CLI et profil, manquant module PAM et port logind, propriétaire PA03 avec PA01.
- Delta PFO sans effet OS et PBO validation et mandats : Configuration invalide bloquée, Configuration et résultat séparés ; source frontière Agent, inconnu UI, propriétaire PBO et PA03.
- Delta Échanges PBO et PA via PZT et opérations fermées typées : Rejeu idempotent d'opération PA, Lecture et plan sans effet, Déploiement et configuration autorisés de bout en bout, Révision périmée refusée, Rollback non implicite, Mutation hôte refusée au rôle utilisateur ; source structure PZT, manquant transport réel et catalogue, propriétaire PZT et PA03.
- Delta Module PAM natif et sécurité du contexte : Indication PAM non probante refusée, Mêmes droits réels après handoff ; manquant module et enfant, propriétaire PA03.
- Delta Artefacts, ABI, provenance et chemins gérés : Paquet incohérent bloqué ; source composition build_profile et bundler et linker et builder, manquant ABI qualifiée, propriétaire PA01.
- Delta États, corrélation, durabilité et effet inconnu : Crash entre effet et résultat ; source durabilité PBO, manquant OS, propriétaire PA03.
- Delta Indisponibilité PBO et PZT et initialisation locale : Réseau indisponible et initialisation locale ; partiel lifecycle, manquant preuve PA, propriétaire PA03.
- Delta Contrat cible Windows : Session déjà ouverte avant service, Fermeture distincte de verrouillage et déconnexion ; disponibilité non vérifiable, pas absence prouvée, propriétaire PA03.
- Source Trois binaires PA et six modes distincts de PZT : Répartition PA et PZT ; source catalogue build_profile et CLI, propriétaire PA01 et PA03.
- Source Démarrage système et session borné : Arrêt pendant délai PA ; source contrats, manquant délais OS, propriétaire PA03.
- Source Arrêt contrôlé et résultats réellement observés : Arrêt contrôlé et résultats réellement observés ; source lifecycle et service, manquant preuve OS, propriétaire PA03.
- Source Isolation des sessions et des privilèges : Isolation des sessions et des privilèges ; source ports et profil, manquant isolation OS, propriétaire PA03.

| Tâche | État réel | Reste | Travail propre vs dépendance ou validation | Constat et preuve | Phase | Reprise |
|---|---|---|---|---|---|---|
| 1 | ouverte, audit1 réalisé non coché, ref rapport auditmsg_17890245c001aSz928o0XhAM61 et 9 fichiers AST et SHA | consigner et valider | travail propre audit, sans dépendance externe | inventaire et écarts fournis, revue CGPT en attente | réalisation | validation CGPT de cette consignation |
| 2 | ouverte, ref delta et canon | sélection profil et dépendances | travail propre sélection, schémas à adoption fonctionnelle | orientations module C et PAM et libpam et budgets acquises, source C7 et C2 | réalisation | tâche 1 puis adoption fonctionnelle |
| 3 | ouverte, ref design et session-integration | barrières et choix | profils et contrats avant unité, travail propre, disponibilités au point d'usage | delta défini, packaging PA01 au besoin de l'unité, ref C7 | réalisation | tâche 2 puis preuves au point d'usage |
| 4 | ouverte, ref contracts et session-integration | contrats et schémas | travail propre, pas de qualification future exigée avant code | objets et catalogue définis, ref delta | réalisation | tâche 3 |
| 5 | ouverte, ref C7 et C2 | complément et branchement | travail propre module et raccord, dépendances PA01 et PA02 et Z12 et C08 et A07 au besoin | C7 sans port à réutiliser, C2 forme seule | réalisation | tâche 4 et dépendances au besoin |
| 6 | ouverte, sans preuve | échecs et reprise | travail propre après tâche 5 | non exécuté, ref critères | tests | tâche 5 |
| 7 | ouverte, ref doc 7 | syntaxe et contrôles | travail propre, résultats au checkpoint après contrôles | contrôles finaux à exécuter, ref lot 7 | tests | preuves locales |
| 8 | ouverte, ref C2 et environnements | intégrations R01 à R68 | vrai port et provision et vérification et durabilité et fencing et transport et artefact et environnement ; DTO et mocks ne qualifient pas, non vérifié pas absence | C2 sans producteur, .pyx non exécuté, ref C2 | intégration | artefacts et environnements réels |
| 9 | ouverte, sans preuve | sortie de référence | travail propre après tâche 8 | non exécuté, ref critères | intégration | tâche 8 |
| 10 | ouverte, sans preuve | matrice preuves | travail propre après tâche 9 | non exécuté, ref critères | finale | tâche 9 |

Précondition pour coder : contrat et profil et propriétaire utiles et nouvelle spécification intégrée validée fonctionnellement ; qualification propre du futur module après son code, pas avant. Disponibilités environnement et modes PAM non vérifiables, pas absences prouvées. Pas de nouvelle méthode, PAM configuration réelle ni choix Windows.
## Validation audit1 2026-10-26 — tâche 1 résolue

Audit1 réalisé en lecture seule le 2026-10-26T14:14:16Z, rapport auditmsg_17890245c001aSz928o0XhAM61, revue 9 sources AST et SHA, matrice 8 exigences et 18 scénarios delta et 4 sources. Tâche 1 cochée sur validation explicite CGPT du 2026-10-26. Toutes les mentions anciennes dix cases ouvertes et audit1 non validé sont l’état HISTORIQUE AVANT la validation d’audit du 26 octobre ; elles sont remplacées pour l’état actuel par 1 tâche sur 10 validée. Matrice et tableau historique conservés sans suppression. Détail en [BLOCKERS.md](./BLOCKERS.md).