# docker-image Specification

## Purpose
L'image de conteneur est un mode de livraison corrélé à la release Pixs : reproductible, stateless, configurée à l'exécution et alignée sur les contrôles de santé et de cycle de vie du socle.

## Requirements

### Requirement: Réplication des profils sous quotas du conteneur

L'image MUST livrer le binaire PBO commun Nuitka standalone avec ses ressources frontend et conserver les exécutants PA/PZT indépendants prévus. Chaque conteneur MUST sélectionner un rôle applicatif PBO explicite, avec processus et concurrence bornés selon runtime ; les réplicas et exécutants cohébergés MUST partager un budget contrôlé. La réplication MUST NOT cloner un propriétaire réseau ni une identité d'exécutant implicitement.

#### Scenario: Plusieurs conteneurs web

- **WHEN** plusieurs conteneurs lancent le rôle web depuis la même image
- **THEN** leurs budgets cumulés et connexions sont contrôlés, sans activation implicite des binaires PA/PZT présents dans l'image

#### Scenario: Ressources de l'hôte non accordées

- **WHEN** le serveur possède plus de CPU ou mémoire que le quota du conteneur
- **THEN** le dimensionnement respecte les limites accordées et les modes de session PA restent exclus

### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des deux binaires PA système/événements et de PZT indépendant

### Requirement: Image sans état ni secret

L'image MUST NOT contenir de secret, de token, de clé privée, de configuration effective ni de données persistantes ; toute persistance MUST rester hors de l'image via les stockages déclarés.

#### Scenario: Valeur sensible dans l'image

- **WHEN** une analyse détecte une valeur sensible dans une couche ou une métadonnée de l'image
- **THEN** la publication est refusée avec un diagnostic n'exposant pas la valeur

### Requirement: Configuration validée à l'exécution

Le conteneur MUST recevoir sa configuration à l'exécution et la valider avant de passer à l'état de service ; il MUST NOT déduire fournisseur, tenant ou identité de l'état accidentel de l'image ou d'un système de fichiers éphémère.

#### Scenario: Démarrage avec configuration invalide

- **WHEN** un conteneur démarre avec une configuration incomplète ou invalide
- **THEN** il reste hors service avec une raison diagnostiquable au lieu de fonctionner dégradé silencieusement

### Requirement: Sondes alignées sur les états de santé

Les contrôles de santé du conteneur MUST être mappés sur les états distincts du socle et MUST NOT confondre vivacité et capacité à servir ; une dépendance optionnelle absente peut donner un état dégradé explicite, jamais une fausse disponibilité.

#### Scenario: Dépendance optionnelle indisponible

- **WHEN** une intégration optionnelle tombe dans un conteneur par ailleurs sain
- **THEN** la sonde d'exposition reflète l'état dégradé déclaré sans masquer une défaillance de sécurité

### Requirement: Arrêt propre et orchestration sans autorité

Le conteneur MUST gérer le signal d'arrêt par un drain contrôlé jusqu'à un état final explicite dans une durée bornée ; l'orchestrateur reste un adapter qui ne devient ni autorité métier ni substitut des validations de composition.

#### Scenario: Arrêt demandé pendant un traitement

- **WHEN** l'orchestrateur demande l'arrêt d'une instance en cours de traitement
- **THEN** l'instance draine selon son contrat et l'état persistant permet la reprise sans double effet

### Requirement: Composition image PBO PFO deux binaires PA et PZT

L'image Pixs MUST toujours contenir le binaire PBO commun, les ressources PFO,
pixs.core, pixs.auth, pixs.agent, pixs.pzt, deux binaires PA — démon système et
événements du conteneur — et le
binaire indépendant PZT. Elle MUST NOT contenir le binaire utilisateur PA ni
ses modes session-start, session-stop et session-daemon. La séparation PA/PZT
MUST conserver trois exécutables hors PBO/PFO dans l'image.

#### Scenario: Inspection de l’image PA PZT

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO, pixs.agent, pixs.pzt, deux binaires PA et PZT sont présents et le binaire utilisateur PA est absent

### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte

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

### Requirement: Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite

L'image Docker Pixs MUST fournir BIND 9 issu de Debian et ses dépendances identifiées. Cette présence MUST NOT activer le serveur sans application et supervision autorisées par le PA désigné. Version et image MUST être corrélées à la release et aux preuves de qualification. Les couches MUST NOT contenir de secret, clé privée ou état DNS propre à une instance.

#### Scenario: Image fournie avec service non sélectionné

- **WHEN** une image Pixs contenant BIND 9 est construite ou démarrée sans rôle serveur DNS sélectionné et admis
- **THEN** la présence du logiciel est vérifiable sans lancement ou disponibilité DNS implicites
- **AND** le choix BIND 9 MUST NOT autoriser implicitement un port, montage, utilisateur ou privilège supplémentaire

#### Scenario: État et secrets hors des couches

- **WHEN** la composition de l'image et les effets de l'installation du paquet sont contrôlés
- **THEN** aucune couche ne contient de clé privée, secret ou état DNS d'instance
- **AND** l'effacement dans une couche ultérieure n'est pas assimilé à l'absence de la donnée dans l'image

#### Scenario: Activation ultérieure contrôlée

- **WHEN** le rôle serveur DNS est ultérieurement sélectionné et admis dans le conteneur
- **THEN** le PA désigné applique et supervise le processus BIND 9 distinct avec les configurations et ressources effectivement autorisées
- **AND** configuration d'instance, données persistantes et références de secrets MUST suivre les plans et propriétaires du profil
- **AND** seul un résultat réel vérifié permet de déclarer état appliqué ou disponibilité
