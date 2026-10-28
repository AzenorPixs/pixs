# Tâches — C08

## État et méthode

Le parcours PA/PZT → PostgreSQL → PBO et les huit deltas sont adoptés au canon le 22 octobre 2026. Les quatre ajouts précédents restent acquis ; PROJECT, TECHNICAL et BUILD sont alignés. Cette adoption documentaire ne réalise aucune des tâches ci-dessous. Les dix-sept identifiants existants sont conservés ; les cases reflètent uniquement les validations techniques prouvées de chaque tâche.

Sur instruction explicite du développeur du 23 octobre 2026, les réalisations sont préparées d'abord, puis les tests et la validation sont conduits dans un second temps. Cette instruction remplace, pour ce change, l'obligation antérieure de valider techniquement chaque réalisation avant de préparer la suivante. Les tâches déjà validées 1.1–1.5 restent acquises. Chaque réalisation non encore testée reste identifiée « réalisée, à tester » dans le checkpoint ; sa case demeure ouverte.

L'ordre des réalisations respecte les dépendances techniques réelles. Un prérequis de validation indiqué ci-dessous s'applique à la validation de la tâche ; il ne bloque plus sa préparation indépendante. Un contrat propriétaire absent, un choix technique encore non adopté ou une autorisation manquante ne sont toutefois pas remplacés par un double, une API inventée ou l'accord par silence. La partie dépendante reste en attente explicite ; les réalisations indépendantes peuvent avancer. Les mandats CAB unitaires et les contrôles de sécurité des écritures restent obligatoires.

Les cas B01–B10, S01–S04, G01–G03 et P01–P10 décrits dans requirements.md et design.md restent tous requis. Les contrôles listés pour chaque tâche sont conservés et seront exécutés, tracés et validés par tâche pendant la phase de tests 2.4, puis complétés par les vérifications globales 3.1. Les mentions de contrôles « dans cette tâche » désignent leur rattachement aux critères de cette tâche, sans imposer leur exécution pendant la réalisation. Aucun contrôle nécessaire n'est supprimé ni réputé réussi par ce report.

Pour toute tâche de code : examiner les fichiers touchés et préserver la sécurité pendant la réalisation ; préparer les tests avec les critères correspondants. Pendant la phase de tests, vérifier la syntaxe et les contrôles configurés, exécuter les unités et intégrations applicables, conserver commandes/résultats/versions/artefacts et contrôler la non-régression avant validation et coche. Un double peut vérifier un contrat isolé ; il ne qualifie ni un exécutant, ni une persistance, ni une politique native réels. Un échec ou une preuve obligatoire manquante bloque la validation de la tâche et les garanties qui en dépendent, sans empêcher une préparation indépendante sûre. Les droits, dépendances et paramètres nouveaux restent soumis aux validations applicables avant leur utilisation.

## Préparation des contrats et profils

- [x] 1.1 Revoir le canon courant, les huit deltas adoptés, requirements.md et les limites des archives C01/C02/C03/C04/C05/C06/C07, sans recréer leurs réalisations.
  - Prérequis : accès aux sources et preuves actuelles ; adoption C08 documentaire acquise.
  - Critères : chaque exigence applicable et chaque scénario B/S/G/P possède propriétaire, périmètre et lot ; les limites des preuves historiques et prérequis de réalisation sont explicites.
  - Contrôles : recoupement des titres et scénarios avec les canons ; vérification des liens et de l’absence de doublon ; validation OpenSpec stricte. Le résultat est documentaire, sans recette produit.

- [x] 1.2 Détailler les mécanismes conformes à R01, le plan privé, le marqueur/checkpoint et la transaction propriétaire ; présenter les fichiers et contrats avant code, sans rouvrir D01–D04 de C02.
  - Prérequis : 1.1 validée ; interfaces publiques Core/Auth/autorisation/audit connues.
  - Critères : opérateur pré-session Ed25519, mapping et autorisation finale de 600 secondes liés au plan ; empreinte sans auto-référence ; propriétaire de chaque état et traitement commit/rollback/issue inconnue définis ; aucun credential dans le plan public.
  - Contrôles : revue des flux B01/B02/B06/B07/B08/B09/B10, invariants et frontières transactionnelles sur exemples documentaires nominaux et refusés ; paramètres et décisions manquants signalés avant réalisation.

- [x] 1.3 Définir les politiques de résolution par mode/workload, l’audit avant base, son relais C05 et la procédure externe de publication des références.
  - Prérequis : 1.2 validée ; contrat C01 et quatre ajouts C08 antérieurs recoupés.
  - Critères : identité native, mode, rôle, finalité, cible, références/versions, bornes et révocations vérifiables sans Auth dans la base à ouvrir ; publication distincte du provider de lecture ; autres résolutions sous autorité applicative courante.
  - Contrôles : revue S01–S04/P05/P06 avec cas mode interdit, politique absente/périmée, référence divergente et audit indisponible ; absence de réétiquetage INSTALLER, de writer implicite et de secret dans les artefacts.

- [x] 1.4 Déclarer le contrat minimal de gouvernance initiale et sa source de confiance réelle, en coordination avec C10.
  - Prérequis : 1.3 validée ; GovernanceProvider et data-governance disponibles comme contrats.
  - Critères : profil complet/versionné, cibles et transaction liées, revalidation avant commit et refus fermé définis ; aucun défaut de rétention inventé ni producteur de fixture présenté comme source déployée.
  - Contrôles : revue G01–G03, substitution et péremption de profil, rollback commun et limites du périmètre C10 ; chaque donnée requise possède sa source et son propriétaire.

- [x] 1.5 Déclarer les profils concrets physique/VM et Docker conformes aux cadrages désormais alignés, avec processus, versions, stockage, budgets et supervision.
  - Prérequis : 1.4 validée ; profil PBO et contrats de distribution adoptés.
  - Critères : PA système/PZT local explicitement sélectionnés ; PostgreSQL fourni sans état dans l’image Docker ; stockage persistant conservé, propriétaire unique et budgets partagés ; mécanisme de secrets Docker déclaré avant qualification, sans équivalence systemd supposée.
  - Contrôles : matrice P01/P02/P10, versions/architectures et ressources réellement visées ; revue des démarrages/arrêts/réplicas et absence d’élargissement implicite des droits du conteneur. Les preuves historiques sans exécutants ne qualifient pas ce profil.

- [x] 1.6 Détailler le provisionnement opérateur indépendant de PG, la capacité PostgreSQL du catalogue fermé PA et le profil PZT local mTLS.
  - Prérequis : 1.5 validée ; contrats publics PA/PZT disponibles et paramètres à qualifier identifiés.
  - Critères : identités/ancrages/politique protégés, actions/cibles fermées, validité/fraîcheur/révocation/anti-rejeu et audit pré-base définis ; aucun premier PBO auto-approuvé, shell arbitraire, repli local hors PZT ou droit métier implicite.
  - Contrôles : revue P03/P04/P07/P09 et transition vers l’autorité PostgreSQL ; R01/C01 conservés, aucun cycle exigeant Auth PG pour fournir sa propre connexion. Toute décision nécessaire à une réalisation dépendante est résolue avant cette réalisation ; la préparation indépendante et les propositions non adoptées peuvent avancer.

## Réalisations, puis phase de tests et validation

- [ ] 2.5 Réaliser le raccord post-INSTALLER du provider systemd existant, le fournisseur Docker explicitement adopté et la remise technique minimale de connexion PBO.
  - Prérequis : 1.6 validée ; transport et audit indépendants de la base effectivement disponibles pour le profil choisi.
  - Critères : seuls modes/workloads/finalités/références autorisés reçoivent une valeur ; aucun writer implicite, réétiquetage de NORMAL, contournement de révocation ou modification des gabarits purs ; audit durable puis relais C05 idempotent avant disponibilité.
  - Contrôles dans cette tâche : S01–S04 et P05/P06 sur le fournisseur réel de chaque profil systemd et Docker, selon les choix D1–D3 adoptés en 1.5 ; preuve native valide/invalide, base initialement fermée, rotation/révocation, consommateur actif, publication absente/divergente, audit indisponible et crash du relais. Syntaxe et non-régressions C01/C05 applicables. Aucun mécanisme Docker non exécuté ni double n’est qualifié ; le lifecycle doit prouver l’arrêt attesté des consommateurs avant remplacement puis remontage/recréation contrôlée, sans perte PostgreSQL ni reconstruction d’image.

- [ ] 2.6 Raccorder une source de gouvernance initiale réelle au port propriétaire et sa revalidation transactionnelle.
  - Prérequis : 2.5 validée ; contrat 1.4 et source protégée disponibles.
  - Critères : profil et attestation effectivement produits, liés à la cible et à la transaction ; absence/péremption/substitution refusées sans dispense du futur compte ; rollback et reprise respectent les propriétaires Core/Auth/audit.
  - Contrôles dans cette tâche : G01–G03 et contrôles propriétaires pertinents de B01/B02/B06/B07/B08 sur PostgreSQL réel avec le fournisseur courant ; aucun résultat intégré C08 non encore réalisé n’est anticipé. Syntaxe et régressions du port concerné.

- [ ] 2.7 Réaliser les raccords techniques propriétaires PA/PZT/PostgreSQL nécessaires à la préparation, sans réaliser l’acte métier à leur place.
  - Prérequis : 2.6 validée ; profils 1.5/1.6 et capacités propriétaires PA/PZT réellement livrés ou réalisés dans ce périmètre sous mandat approprié.
  - Critères : provisionnement opérateur, préparation PG et première connexion technique PA via PZT local prouvés ; stockage existant conservé ; résultat durable inspectable et idempotent ; aucun accès aux tables métier, credential de management, autorité concurrente ou compensation destructive implicite.
  - Contrôles dans cette tâche : parties techniques P01–P04/P06/P07/P09/P10 sur cibles autorisées, y compris PZT absent, politique révoquée, réponse perdue, reprise et concurrence ; physique/VM et Docker qualifiés seulement pour les profils réellement exécutés. Les cas applicatifs P08 et l’intégration complète attendent leurs tâches propriétaires ci-dessous, sans remplacer ces contrôles techniques.

- [ ] 2.1 Réaliser le marqueur externe, la machine de modes et l’état durable d’opération C08 liés au plan, à l’installation/base et aux confirmations.
  - Prérequis : 2.7 validée ; plan 1.2 et contrats propriétaires persistants disponibles.
  - Critères : états inspectables, deux marqueurs distincts, absence de secret, exclusion et identité/version contrôlées ; publication durable seulement après résultat confirmé ; issue inconnue réconciliée avant reprise, sans création de compte nécessaire pour tester ce propriétaire isolé.
  - Contrôles dans cette tâche : unités/négatifs de fichier, droits/propriétaire/type/liens, contenu/version/digest et confirmations ; persistance réelle de l’état C08 ; portions locales B06/B07/B10/P07/P08 avec résultat propriétaire contrôlé, crash aux frontières et absence de duplication. Ne pas qualifier l’acte Core/Auth encore absent.

- [ ] 2.2 Réaliser la CLI et l’orchestration d’inspection des états de base et des plans/confirmations de préparation et migration.
  - Prérequis : 2.1 validée ; raccords techniques 2.5/2.7 et mécanismes de confirmation 1.2 disponibles.
  - Critères : base absente créée seulement après confirmation ; base conforme conservée ; base migrable sous plan confirmé ; base incompatible sans destruction avant confirmations distinctes, fraîches et liées à la cible ; PBO conserve les migrations propriétaires.
  - Contrôles dans cette tâche : quatre états sur environnements autorisés, B03/B04/P01/P02/P07 et refus de plan/cible/confirmation divergents ; interruption après préparation et avant migration, reprise sans nouvelle base, credential absent des sorties. Syntaxe et unités/recettes CLI applicables à valider avant la validation de 2.3.

- [ ] 2.3 Créer ou réutiliser le Super Admin unique et le premier tenant via les écritures propriétaires C02, le credential privé C03 et l’acte R01.
  - Prérequis : 2.2 validée ; gouvernance 2.6, Auth/autorisation/audit et transaction C08 réellement disponibles.
  - Critères : opérateur et décision liés au plan sans authentification anticipée du compte cible ; unicité, mot de passe confirmé, base conservée sans reset, aucun accord tenant implicite ; effets Core/Auth/C05/C08 engagés ensemble, sans atomicité prétendue avec la préparation PA externe.
  - Contrôles dans cette tâche : B01–B10 applicables, G01–G03 et P08/P09 sur la composition réelle ; mauvais opérateur, saisies différentes, concurrence, rejou identique/divergent, panne avant/après commit/marqueur, audit absent, autorité hors périmètre et transitions. Syntaxe et régressions propriétaires ; tous ces tests nécessaires sont rattachés à 2.3 et exécutés pendant la phase de tests 2.4 avant validation de 2.3.

- [ ] 2.4 Exécuter les tests locaux différés, puis consolider la recette intégrée C08 et vérifier les parcours B/S/G/P complets.
  - Prérequis : réalisations nécessaires préparées et dépendances techniques disponibles. Exécuter d'abord les contrôles rattachés à chaque tâche, dans l'ordre des dépendances ; les valider séparément, puis lancer la recette intégrée. Aucune tâche locale obligatoire non prouvée ne permet de valider 2.4.
  - Critères : chaque scénario applicable est relié à l’artefact, version, cible et résultat observé ; P01–P10, B01–B10, S01–S04 et G01–G03 couvrent l’ensemble du parcours sélectionné ; gardes locales et preuves intégrées sont distinctes, sans disponibilité P0 déduite.
  - Contrôles : exécuter la recette intégrée et les non-régressions pertinentes, confronter état technique PA, audit pré-base, relais C05, commit applicatif et marqueur ; signaler toute cible non exécutée et bloquer les garanties qui en dépendent.

## Consolidation des preuves et clôture future

- [ ] 3.1 Exécuter les vérifications globales configurées sur le périmètre final, en complément des contrôles déjà passés dans chaque tâche.
  - Prérequis : 2.4 validée.
  - Critères : syntaxe, suites applicables, lint/types/build lorsqu’ils sont configurés et pertinents, avec versions et résultats natifs ; aucun test de sécurité ou de persistance remplacé par la syntaxe.
  - Contrôles : commandes du projet sur les fichiers finaux et suites de non-régression nécessaires ; échec ou indisponibilité obligatoire bloque la validation.

- [ ] 3.2 Vérifier la conformité de chaque scénario, l’isolation, les échecs et l’absence de secret sur les preuves finales.
  - Prérequis : 3.1 validée.
  - Critères : matrice requirements.md complète avec preuves actuelles, contrôles d’autorité et de reprise observés ; non exécuté et non applicable motivés sans fabriquer une preuve requise.
  - Contrôles : revue croisée B/S/G/P, des sorties minimisées et des verdicts ; requalifier les seules preuves invalidées par des modifications ultérieures.

- [ ] 3.3 Examiner les fichiers réellement modifiés, le périmètre, les impacts et limites, en préservant les travaux préexistants.
  - Prérequis : 3.2 validée.
  - Critères : seuls les fichiers autorisés sont touchés ; aucune dérive de contrat ou dépendance non validée ; C08 ne prétend pas qualifier P0 avant C14/C17/C18/C19 et les profils concernés.
  - Contrôles : comparaison au point de référence, cohérence OpenSpec, UTF-8/LF et liens, inventaire des effets et des preuves ; revue des divergences concurrentes avant clôture.

- [ ] 3.4 Préparer la clôture et effectuer uniquement les opérations finales autorisées séparément.
  - Prérequis : 3.3 validée ; autorisation distincte pour toute opération Git, archivage, installation, déploiement ou publication.
  - Critères : les deltas C08 déjà adoptés ne sont pas appliqués une seconde fois ; l’état et les preuves de chaque tâche sont disponibles. En cas d’archivage demandé et réussi, STATISTIQUES.md possède ses preuves propres.
  - Contrôles : validations globales requises, métadonnées et contrôles propres à l’opération explicitement autorisée ; en son absence, conserver le dossier actif et rapporter ce statut sans simuler une publication ou une archive.

## Rattachement du retrait de la préparation initiale PA

Le retrait irréversible de la nouvelle préparation initiale PA est rattaché à 1.6 pour sa conception, et à 2.7 pour ses raccords techniques, avec mobilisation de 2.6 pour la gouvernance concernée et de 2.1 pour l'état et la reprise. Les intitulés, l'ordre et les coches existantes restent inchangés.

La conception précise l'action withdraw_initial_authority, de classe Critique, dans le domaine PA_POSTGRESQL_WITHDRAWAL, sous la permission WITHDRAW_PA_INITIAL, le mandat signé nouveau distinct de R01 et E4, la confirmation C08 avec C03 et C04 courants, et les vérifications PA de signature, politique, révocation, fraîcheur UTC, identités, cible, plan, contexte, anti-rejeu, quiescence et ancrage durable. Les contrats de topologie D8/D6, de wire et de résolveurs restent à fermer en revue commune avant leur code, les qualifications réelles en phase 2 après réalisation. Aucune réalisation n'est anticipée par ce rattachement. L'adoption des principes ne vaut pas réalisation.

E5 est adopté documentairement et reste non réalisé ni qualifié. L'ordre des réalisations respecte OBSERVE, projection liée à l'observation, PREPARE_PLAN, confirmation, PREPARE critique, READ_RESULT. Les qualifications réelles suivent en phase 2 après réalisation, sans modifier les coches ni l'ordre des dix-sept tâches. Aucun code, test, producteur ou infrastructure n'est livré par cette transcription.

## Bilan des blocages

- [Bilan des blocages](BLOCKERS.md) — clôture différée pour dépendances manquantes, constat du 2026-10-26T15:03:52.704560+00:00, 6 tâches achevées et 11 tâches ouvertes détaillées.
