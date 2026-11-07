## ADDED Requirements


### Requirement: PostgreSQL fourni et initialisation PA du profil Docker Pixs

L’image Docker Pixs MUST fournir le logiciel PostgreSQL sans cluster, secret ou données effectives embarqués. Le profil MUST sélectionner explicitement PA système, PZT local et PostgreSQL avec stockage persistant hors image et hors couche éphémère. PA MUST initialiser seulement les ressources manquantes, conserver l’existant et respecter les garanties de supervision, reprise et réplication ci-dessous.

#### Scenario: Garanties du profil Docker PostgreSQL

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** L'image Docker Pixs MUST fournir le logiciel PostgreSQL, sans cluster préinitialisé, configuration effective ni données métier intégrés aux couches. Le profil d'exécution MUST sélectionner explicitement PA système, PZT local et le service PostgreSQL cohébergé, avec supervision, ordre de démarrage, arrêt contrôlé et budgets de ressources communs déclarés ; la simple présence des binaires MUST NOT les activer. Les données PostgreSQL MUST résider dans un stockage persistant déclaré hors de l'image et de la couche éphémère du conteneur. PA MUST vérifier l'état réel de ce stockage, initialiser uniquement ce qui manque, puis préparer et contrôler le service avant les opérations propriétaires PBO. Un stockage existant MUST être conservé et une incompatibilité MUST rester non prête sans effacement automatique. L'image, un redémarrage ou une réplication MUST NOT créer de nouveau propriétaire de base, cloner une identité PA/PZT ou réinitialiser le cluster. Les réplicas MUST déclarer leur cible de persistance et un propriétaire admissible unique pour la préparation. Tous échanges PBO–PA MUST rester via PZT ; les permissions du conteneur MUST NOT être étendues implicitement à l'hôte.

#### Scenario: Premier démarrage Docker

- **WHEN** un conteneur reçoit un stockage persistant vide et un profil PA/PZT/PostgreSQL explicitement admis
- **THEN** PA prépare le cluster avec le logiciel déjà fourni et PBO conserve seul ses migrations et initialisations applicatives ; aucun secret n’est ajouté à l’image

#### Scenario: Redémarrage et réplication Docker

- **WHEN** un conteneur redémarre ou un réplica cible une base déjà initialisée
- **THEN** le stockage et ses données sont conservés, les identités et le propriétaire de préparation restent distincts et aucun second cluster n’est créé implicitement

### Requirement: Profil Docker initial déclaré et supervisé

Le profil Docker initial C08 MUST respecter l’intégralité du contrat normatif du scénario « Démarrage du profil Docker déclaré » pour toute construction, préparation, exécution et tout arrêt du profil. Les garanties de processus, supervision, stockage, ressources et droits y sont indissociables ; leur déclaration MUST NOT constituer une qualification.

#### Scenario: Démarrage du profil Docker déclaré

- **WHEN** le profil initial est demandé avec son artefact, sa configuration et son stockage déclarés
- **THEN** PZT et PA sont admis sous leurs contrôles, PA prépare seulement les ressources PostgreSQL manquantes et PBO conserve ses migrations et initialisations
- **AND** aucun entrypoint hérité ni volume anonyme accidentel n’autorise une initialisation ou une disponibilité
- **AND** Le profil Docker initial C08 MUST déclarer Debian 13 Linux amd64, la base Docker Official Image postgres:16.15-trixie verrouillée par digest avant construction, le paquet Supervisor 4.2.5-3 et ses dépendances système verrouillées, l’init Docker et la supervision au premier plan. Il MUST traiter explicitement ENTRYPOINT, CMD, STOPSIGNAL et VOLUME hérités, sans initialisation automatique PostgreSQL. Il MUST sélectionner un rôle applicatif PBO, les exécutants PA système/événements et PZT indépendant et un service PostgreSQL distinct, sous un plan de ressources et un stockage persistant déclarés. Le lifecycle MUST contrôler ordre, readiness, comptes, signaux et drain ; PostgreSQL MUST attendre sa préparation autorisée par PA. Le profil MUST NOT ajouter implicitement privilège, socket Docker, namespace hôte ou montage de cgroups. Les droits de l’hôte et les données persistantes MUST rester préservés ; une métadonnée d’image ou une dépendance installée MUST NOT valoir qualification.

#### Scenario: Arrêt des processus cohébergés

- **WHEN** le conteneur reçoit son signal d’arrêt déclaré
- **THEN** le lifecycle draine PBO avant fermeture PostgreSQL et conserve PA/PZT jusqu’aux étapes qui les requièrent, dans les bornes accordées
- **AND** une étape inconnue ou interrompue reste non prête et inspectable sans perte silencieuse ni réinitialisation du stockage
