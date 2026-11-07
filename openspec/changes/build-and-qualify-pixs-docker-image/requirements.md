# Références normatives — X01

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| docker-image | Réplication des profils sous quotas du conteneur | 2 | docker-image-2ba58f2f253f |
| docker-image | Composition reproductible corrélée à la release | 2 | docker-image-276989d88d03 |
| docker-image | Image sans état ni secret | 1 | docker-image-cd1d3b742826 |
| docker-image | Configuration validée à l'exécution | 1 | docker-image-fe93183206ec |
| docker-image | Sondes alignées sur les états de santé | 1 | docker-image-83a4c263b381 |
| docker-image | Arrêt propre et orchestration sans autorité | 1 | docker-image-830a6195e1f2 |
| docker-image | Composition image PBO PFO deux binaires PA et PZT | 1 | docker-image-17e292fd2853 |
| docker-image | Événements PA limités au conteneur | 1 | docker-image-67e439783126 |
| docker-image | PostgreSQL fourni et initialisation PA du profil Docker Pixs | 3 | docker-image-a163e560260b |
| docker-image | Profil Docker initial déclaré et supervisé | 2 | docker-image-5ecbef2bfc17 |
| docker-image | Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite | 3 | docker-image-ceda1e465971 |
| docker-image | Profils Domaine et persistance des services | 1 | docker-image-a889a820ae60 |
| reference-composition | Qualification du binaire commun et des profils de ressources P0 | 4 | reference-composition-7131b276f78e |
| reference-composition | Capacités obligatoires du P0 | 1 | reference-composition-0af0b6011293 |
| reference-composition | Capacités hors P0 explicites | 1 | reference-composition-986398c06367 |
| reference-composition | Preuve reproductible | 1 | reference-composition-ab553efe6c54 |
| reference-composition | Profil initial PBO PFO Debian local v1 | 2 | reference-composition-5f1322f3cd28 |
| reference-composition | Garanties du socle conservées dans le profil initial | 1 | reference-composition-70063af8e7b7 |
| reference-composition | Parcours installable et utilisable du profil initial | 1 | reference-composition-2614801b7609 |
| reference-composition | Capacités non sélectionnées du profil initial | 1 | reference-composition-ef9b2d25c156 |
| reference-composition | Preuve de la composition effectivement distribuée | 1 | reference-composition-7961b985d4cc |
| reference-composition | Choix C01 systemd et exception d’amorçage du profil Debian local | 2 | reference-composition-80e3d17e557d |
| reference-composition | Qualification et source de vérité après amorçage | 2 | reference-composition-b86766ab642e |
| reference-composition | Profil Auth standard sans connecteur externe installé | 2 | reference-composition-fa2727180f3d |
| reference-composition | Composition ZT initiale et Domaines | 1 | reference-composition-4f43b97aaed5 |
| pixs-domains | Identité et FQDN explicites | 1 | pixs-domains-02f0f83aed5e |
| pixs-domains | ZT obligatoire dédié ou partagé | 2 | pixs-domains-686f4e13ff70 |
| pixs-domains | Isolation dans un ZT partagé | 1 | pixs-domains-bd2991264b73 |
| pixs-domains | Services minimaux par Domaine | 1 | pixs-domains-c9ce061e2b23 |
| pixs-domains | Tenants et propriété des ressources | 2 | pixs-domains-784b3416b755 |
| pixs-domains | Individus et identités multiples | 1 | pixs-domains-8e5157150f7c |
| pixs-domains | Transferts fonctionnels contrôlés V1 | 1 | pixs-domains-ba4dfa97bf7d |
| pixs-domains | Structures organisationnelles non transférables V1 | 1 | pixs-domains-2d4b91559aa3 |
| pixs-domains | Retrait du premier Domaine | 1 | pixs-domains-f9d0dad1d882 |
| pixs-domains | Approbations internes et externes | 1 | pixs-domains-94814997f512 |
| pixs-domains | Références PG et services de Domaine en mode normal ou critique | 1 | pixs-domains-d8fce09ab784 |

### Référence courante docker-image-2ba58f2f253f

Source : [docker-image](../../specs/docker-image/spec.md), ligne 8. SHA-256 : `2ba58f2f253f0bea4c11827b5d2e1ad028bef5992ab59a67f014528f9c14688b`.

Scénarios : Plusieurs conteneurs web; Ressources de l'hôte non accordées.

~~~~text
### Requirement: Réplication des profils sous quotas du conteneur

L'image MUST livrer le binaire PBO commun Nuitka standalone avec ses ressources frontend et conserver les exécutants PA/PZT indépendants prévus. Chaque conteneur MUST sélectionner un rôle applicatif PBO explicite, avec processus et concurrence bornés selon runtime ; les réplicas et exécutants cohébergés MUST partager un budget contrôlé. La réplication MUST NOT cloner un propriétaire réseau ni une identité d'exécutant implicitement.

#### Scenario: Plusieurs conteneurs web

- **WHEN** plusieurs conteneurs lancent le rôle web depuis la même image
- **THEN** leurs budgets cumulés et connexions sont contrôlés, sans activation implicite des binaires PA/PZT présents dans l'image

#### Scenario: Ressources de l'hôte non accordées

- **WHEN** le serveur possède plus de CPU ou mémoire que le quota du conteneur
- **THEN** le dimensionnement respecte les limites accordées et les modes de session PA restent exclus
~~~~

### Référence courante docker-image-276989d88d03

Source : [docker-image](../../specs/docker-image/spec.md), ligne 22. SHA-256 : `276989d88d03cfe27f2b79a91dfbc453fb8e6f76b9f50d0a9d2ab63b0353d80d`.

Scénarios : Deux constructions d'une même release; Binaire utilisateur dans l’image.

~~~~text
### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des deux binaires PA système/événements et de PZT indépendant
~~~~

### Référence courante docker-image-cd1d3b742826

Source : [docker-image](../../specs/docker-image/spec.md), ligne 36. SHA-256 : `cd1d3b742826f68ef714ca9c17bbe9ce712addf2a91919998e568a264e9ab7e1`.

Scénarios : Valeur sensible dans l'image.

~~~~text
### Requirement: Image sans état ni secret

L'image MUST NOT contenir de secret, de token, de clé privée, de configuration effective ni de données persistantes ; toute persistance MUST rester hors de l'image via les stockages déclarés.

#### Scenario: Valeur sensible dans l'image

- **WHEN** une analyse détecte une valeur sensible dans une couche ou une métadonnée de l'image
- **THEN** la publication est refusée avec un diagnostic n'exposant pas la valeur
~~~~

### Référence courante docker-image-fe93183206ec

Source : [docker-image](../../specs/docker-image/spec.md), ligne 45. SHA-256 : `fe93183206ec0c04a71c04d61ebaa87e6ac3d79960a60d78f9889e915d777ef2`.

Scénarios : Démarrage avec configuration invalide.

~~~~text
### Requirement: Configuration validée à l'exécution

Le conteneur MUST recevoir sa configuration à l'exécution et la valider avant de passer à l'état de service ; il MUST NOT déduire fournisseur, tenant ou identité de l'état accidentel de l'image ou d'un système de fichiers éphémère.

#### Scenario: Démarrage avec configuration invalide

- **WHEN** un conteneur démarre avec une configuration incomplète ou invalide
- **THEN** il reste hors service avec une raison diagnostiquable au lieu de fonctionner dégradé silencieusement
~~~~

### Référence courante docker-image-83a4c263b381

Source : [docker-image](../../specs/docker-image/spec.md), ligne 54. SHA-256 : `83a4c263b381b1c4873df0b7b772d43620179c335155cc4d41b9de383e80c79a`.

Scénarios : Dépendance optionnelle indisponible.

~~~~text
### Requirement: Sondes alignées sur les états de santé

Les contrôles de santé du conteneur MUST être mappés sur les états distincts du socle et MUST NOT confondre vivacité et capacité à servir ; une dépendance optionnelle absente peut donner un état dégradé explicite, jamais une fausse disponibilité.

#### Scenario: Dépendance optionnelle indisponible

- **WHEN** une intégration optionnelle tombe dans un conteneur par ailleurs sain
- **THEN** la sonde d'exposition reflète l'état dégradé déclaré sans masquer une défaillance de sécurité
~~~~

### Référence courante docker-image-830a6195e1f2

Source : [docker-image](../../specs/docker-image/spec.md), ligne 63. SHA-256 : `830a6195e1f28088dcf6d3f11fbedbab68c465fcefdb6734e145eb1aecff3b69`.

Scénarios : Arrêt demandé pendant un traitement.

~~~~text
### Requirement: Arrêt propre et orchestration sans autorité

Le conteneur MUST gérer le signal d'arrêt par un drain contrôlé jusqu'à un état final explicite dans une durée bornée ; l'orchestrateur reste un adapter qui ne devient ni autorité métier ni substitut des validations de composition.

#### Scenario: Arrêt demandé pendant un traitement

- **WHEN** l'orchestrateur demande l'arrêt d'une instance en cours de traitement
- **THEN** l'instance draine selon son contrat et l'état persistant permet la reprise sans double effet
~~~~

### Référence courante docker-image-17e292fd2853

Source : [docker-image](../../specs/docker-image/spec.md), ligne 72. SHA-256 : `17e292fd285356a4b244611861a4a2b1f2022227b81b6679918b6f1fcfaa67f0`.

Scénarios : Inspection de l’image PA PZT.

~~~~text
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
~~~~

### Référence courante docker-image-67e439783126

Source : [docker-image](../../specs/docker-image/spec.md), ligne 86. SHA-256 : `67e439783126ef0a8a06f6fccd1b23f938cf3c990e477a02c907cfa37598baab`.

Scénarios : Événements PA limités au conteneur.

~~~~text
### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte
~~~~

### Référence courante docker-image-a163e560260b

Source : [docker-image](../../specs/docker-image/spec.md), ligne 95. SHA-256 : `a163e560260b3dde869579b04669ca5999b0aae00cdfcd9de3a09ae9700488dc`.

Scénarios : Garanties du profil Docker PostgreSQL; Premier démarrage Docker; Redémarrage et réplication Docker.

~~~~text
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
~~~~

### Référence courante docker-image-5ecbef2bfc17

Source : [docker-image](../../specs/docker-image/spec.md), ligne 114. SHA-256 : `5ecbef2bfc1708b352e1948e6893e37e754db62de5f12bd91097ae37e7bdf567`.

Scénarios : Démarrage du profil Docker déclaré; Arrêt des processus cohébergés.

~~~~text
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
~~~~

### Référence courante docker-image-ceda1e465971

Source : [docker-image](../../specs/docker-image/spec.md), ligne 131. SHA-256 : `ceda1e465971ab5e0784c8cc3811f171070311b193543d0f868da0e5d48a2d1c`.

Scénarios : Image fournie avec service non sélectionné; État et secrets hors des couches; Activation ultérieure contrôlée.

~~~~text
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
~~~~

### Référence courante docker-image-a889a820ae60

Source : [docker-image](../../specs/docker-image/spec.md), ligne 154. SHA-256 : `a889a820ae600423c7b5f29e9f38b3d84c48fc37ad2f9e536cbb04706c3cc7b2`.

Scénarios : Rôles répartis.

~~~~text
### Requirement: Profils Domaine et persistance des services

Un profil Docker Domaine MUST déclarer ses services PG propriétaires, LDAP/Kerberos et ZT, comptes, dépendances et persistances sans montage ni privilège implicite. L'image MUST conserver deux binaires PA système/événements et PZT, sans sessions PA utilisateur. Les minima requis MUST être vérifiés sur la composition effective et MUST NOT imposer tous les rôles dans chaque conteneur.

#### Scenario: Rôles répartis

- **WHEN** un Domaine répartit ses rôles sur plusieurs conteneurs autorisés
- **THEN** chaque profil conserve son périmètre et ses stockages sans duplication d’identité ni attribution de droit hôte implicite.
~~~~

### Référence courante reference-composition-7131b276f78e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 10. SHA-256 : `7131b276f78ec528ebd8d3dc65dca30cc41d7a9b3f3ae193754cb02b3e8ea9e6`.

Scénarios : Garanties de qualification du parcours initial PA PZT; P0 sans exécution réseau; P0 sans réseau distant; Plan de ressources sans preuve sur cible.

~~~~text
### Requirement: Qualification du binaire commun et des profils de ressources P0

Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et ses ressources selon reference-runtime et runtime. Il MUST sélectionner et qualifier PA système/PZT local pour préparer PostgreSQL, sans activation déduite de la présence des modules ni confusion avec le réseau distant. La preuve MUST respecter les garanties détaillées du scénario ci-dessous.

#### Scenario: Garanties de qualification du parcours initial PA PZT

- **WHEN** le profil initial PBO et son parcours de préparation PostgreSQL sont évalués
- **THEN** Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et son plan de processus selon reference-runtime et runtime. La preuve MUST relier budgets accordés, configuration demandée, état appliqué, mesures et scénarios de panne. Les modules essentiels MUST rester composés et leur présence MUST NOT valoir activation. Le parcours initial de préparation PostgreSQL par PA MUST sélectionner explicitement les exécutants PA système et PZT local avec leurs profils propres à qualifier ; une absence de réseau distant MUST NOT être confondue avec l'absence de ce transport local obligatoire.

#### Scenario: P0 sans exécution réseau

- **WHEN** le profil initial conserve le réseau désactivé
- **THEN** les modules essentiels restent présents dans le binaire PBO et aucun exécutant PA/PZT ni résultat réseau n'est inventé
- **AND** l’absence de PZT local empêche de qualifier le parcours de préparation PostgreSQL par PA

#### Scenario: P0 sans réseau distant

- **WHEN** le profil initial sélectionne la préparation PostgreSQL par PA sans réseau distant
- **THEN** les modules essentiels et les exécutants PA système/PZT local nécessaires sont explicitement sélectionnés et qualifiés sans revendiquer de résultat de réseau distant

#### Scenario: Plan de ressources sans preuve sur cible

- **WHEN** une composition P0 possède un plan mais pas de recette sur l'environnement distribué
- **THEN** elle ne revendique pas un binaire ou un dimensionnement qualifié sur cette seule déclaration
~~~~

### Référence courante reference-composition-0af0b6011293

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 35. SHA-256 : `0af0b601129367e64eba64554f480dd9d5a1b93ee2348a0ba66ad4ac964e8671`.

Scénarios : Capacité P0 absente.

~~~~text
### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, `pixs.auth` essentiel avec son authentification locale autonome et PostgreSQL par défaut, le contexte tenant/scope, l'autorisation, les API et contrats publics, migrations, runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance, cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication
~~~~

### Référence courante reference-composition-986398c06367

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 44. SHA-256 : `986398c063671a966f8bc20f7e0d7706fe89595ff960a233fa8fbc266c49ad03`.

Scénarios : Synchronisation non sélectionnée.

~~~~text
### Requirement: Capacités hors P0 explicites

Toute capacité hors P0 MAY être ajoutée par sélection explicite. Son absence
MUST être déclarée ou représentée par un état compatible et MUST NOT affaiblir
les garanties du P0.

#### Scenario: Synchronisation non sélectionnée

- **WHEN** une composition P0 n'inclut aucun provider de synchronisation
- **THEN** elle reste valide sans annoncer de capacité réactive
~~~~

### Référence courante reference-composition-ab553efe6c54

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 55. SHA-256 : `ab553efe6c54a415ee9b8e42bbb9e9d009d3681dce99c2210ada04af4ef236b4`.

Scénarios : Deux validations identiques.

~~~~text
### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents
~~~~

### Référence courante reference-composition-5f1322f3cd28

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 66. SHA-256 : `5f1322f3cd28af91090d23c44e81cab453f1e264e606a48d7fbaa4ea3853d90e`.

Scénarios : Garanties du profil Debian local avec préparation PA; Architecture seulement observée.

~~~~text
### Requirement: Profil initial PBO PFO Debian local v1

Le profil pbo-p0-debian-local-v1 MUST identifier PBO/PFO, Debian 13 local, Django/TanStack et PostgreSQL distinct de PBO, préparé par PA système via PZT local. Il MUST déclarer et qualifier ses versions, architectures et exécutants selon le scénario ci-dessous ; un relevé de développement ou une preuve sans ces exécutants MUST NOT qualifier ce profil révisé.

#### Scenario: Garanties du profil Debian local avec préparation PA

- **WHEN** la première livraison du profil pbo-p0-debian-local-v1 est évaluée
- **THEN** La première livraison de profil `pbo-p0-debian-local-v1` MUST identifier PBO/PFO, Debian 13 local, Django, TanStack et PostgreSQL comme service distinct du processus PBO, préparé par le PA système de cet hôte via le parcours PA/PZT déclaré. Le profil MUST sélectionner les exécutants PA système et PZT local nécessaires à ce parcours ; une qualification historique sans ces exécutants MUST NOT prouver ce profil révisé. Elle MUST déclarer ses architectures et versions qualifiées avant distribution ; le relevé de développement MUST NOT tenir lieu de qualification.

#### Scenario: Architecture seulement observée

- **WHEN** une architecture apparaît dans l’environnement de développement sans recette correspondante
- **THEN** elle n’est pas annoncée comme supportée par le profil livré
~~~~

### Référence courante reference-composition-70063af8e7b7

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 80. SHA-256 : `70063af8e7b7f3ec61cbf3a60e111e20b60fcc09b6574df183ec392d1f1dce56`.

Scénarios : Module essentiel absent.

~~~~text
### Requirement: Garanties du socle conservées dans le profil initial

Le profil initial MUST satisfaire les capacités obligatoires P0 et composer les modules de gestion `pixs.agent` (PA hors PZT) et `pixs.pzt` (PZT), ainsi que le module DNS essentiel côté PBO. La désactivation réseau MUST NOT retirer ces modules ni affaiblir identité, périmètre, autorisation, audit, gouvernance ou reprise applicables.

#### Scenario: Module essentiel absent

- **WHEN** le réseau est désactivé mais `pixs.agent`, `pixs.pzt` ou le module DNS essentiel manque à la composition PBO
- **THEN** la qualification du profil échoue avant publication
~~~~

### Référence courante reference-composition-2614801b7609

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 89. SHA-256 : `2614801b7609ab3d7e337158b1a189846ac07b7308a13f21974f0e532efc17de`.

Scénarios : Démonstration mémoire seule.

~~~~text
### Requirement: Parcours installable et utilisable du profil initial

Le profil MUST permettre installation, première configuration, authentification, administration et opérations Core via contrats publics. Les rôles web, worker et scheduler MUST utiliser le même artefact et la persistance de référence ; une composition de test seule MUST NOT prouver ces parcours.

#### Scenario: Démonstration mémoire seule

- **WHEN** les seuls contrôles réussis utilisent des fixtures mémoire sans installation ni dépendance réelle
- **THEN** le profil ne revendique pas un parcours installable et utilisable qualifié
~~~~

### Référence courante reference-composition-ef9b2d25c156

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 98. SHA-256 : `ef9b2d25c1563c4766241a4a4b0e5df4f4188397774c38481e8c1f9e7bd395ab`.

Scénarios : Option absente sans dépendance obligatoire.

~~~~text
### Requirement: Capacités non sélectionnées du profil initial

Le profil MUST déclarer les capacités non sélectionnées et leurs limites sans annoncer leurs garanties. Une dépendance obligatoire d’une capacité sélectionnée MUST NOT être exclue sous prétexte d’option ; son absence bloque la qualification concernée.

#### Scenario: Option absente sans dépendance obligatoire

- **WHEN** aucun provider de synchronisation n’est sélectionné et aucune capacité retenue ne l’exige
- **THEN** son absence est déclarée sans annoncer de synchronisation ni affaiblir le P0
~~~~

### Référence courante reference-composition-7961b985d4cc

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 107. SHA-256 : `7961b985d4cc6e4533276d182585f4d018bce58499a8d3ce46b8b3ae71f2da57`.

Scénarios : Sources et paquet divergents.

~~~~text
### Requirement: Preuve de la composition effectivement distribuée

La preuve initiale MUST relier exigences applicables, scénarios exécutés, composants, versions et artefact installé. Elle MUST distinguer code présent, déclarations, dimensions non évaluées et verdicts observés, sans secret ni compatibilité globale supposée.

#### Scenario: Sources et paquet divergents

- **WHEN** la recette porte sur des sources différentes de celles du paquet proposé
- **THEN** elle ne suffit pas à qualifier la composition distribuée
~~~~

### Référence courante reference-composition-80e3d17e557d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 116. SHA-256 : `80e3d17e557db39ab0b1f163e3b9be60f18df6f7f0cdd4ef4555404d6256b8c9`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Choix C01 systemd et exception d’amorçage du profil Debian local

Le profil pbo-p0-debian-local-v1 MUST sélectionner le transport C01 LoadCredentialEncrypted systemd avec rotation par arrêt attesté et redémarrage contrôlé. Avant disponibilité de la base Pixs et du sink C05, il MUST déclarer explicitement l’exception limitée du journal fonctionnel local d’amorçage, ses politiques et son autorisation INSTALLER.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-b86766ab642e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 130. SHA-256 : `b86766ab642ec0550cf7661ba1d162a50901d633d9bb6948cc548c4cb0225c3e`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Qualification et source de vérité après amorçage

Cette exception MUST NOT devenir une source de vérité métier parallèle après reprise dans PostgreSQL. Les architectures, versions, capacités de stockage et politiques MUST être qualifiées avant distribution ; DEVOPS.md, un test isolé ou un reçu mémoire MUST NOT valoir qualification du paquet.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-fa2727180f3d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 144. SHA-256 : `fa2727180f3d824fbb7e3619a5b0196d02d52df210f1022887c5b3578875e857`.

Scénarios : Profil livré sans connecteurs externes; Profil Domaine.

~~~~text
### Requirement: Profil Auth standard sans connecteur externe installé

Le profil pré-domaine MUST sélectionner Auth local PG et garder les connecteurs externes absents sauf sélection explicite. Le mode Domaine MUST composer les capacités LZT/OpenLDAP et KZT/MIT Kerberos requises par Domaine ; IdP sortant et connecteurs externes MUST rester distincts et non activés implicitement. Présence de logiciel et service opérationnel MUST rester séparés.

#### Scenario: Profil livré sans connecteurs externes

- **WHEN** un profil Standalone standard est installé
- **THEN** Auth PG fonctionne selon sa politique sans service LDAP/KDC ou émission sortante implicite.

#### Scenario: Profil Domaine

- **WHEN** une composition revendique un Domaine opérationnel
- **THEN** ses LZT/KZT et son ZT admissible doivent être vérifiés, même si aucune source externe n’est installée.
~~~~

### Référence courante reference-composition-4f43b97aaed5

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 158. SHA-256 : `4f43b97aaed55b2b87629f7cc9dfae67e927a01213a4051882f1cc89c67f335e`.

Scénarios : PBO seul disponible.

~~~~text
### Requirement: Composition ZT initiale et Domaines

La qualification MUST distinguer PBO composé, PA/PZT disponibles, ZT entièrement initialisé et Domaine opérationnel. Les minima MUST suivre pixs-instance, pixs-domains et zt-instances ; un contrat pur ou artefact présent MUST NOT prouver ces états. Le premier PZT complet MUST cibler Debian/Linux et les autres profils MUST déclarer leurs rôles qualifiés.

#### Scenario: PBO seul disponible

- **WHEN** PBO est qualifié mais aucun exécutant CZT/DZT/PKIZT n’est admissible
- **THEN** la composition ne revendique pas ZT initialisé ni création de Domaine admissible.
~~~~

### Référence courante pixs-domains-02f0f83aed5e

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 11. SHA-256 : `02f0f83aed5e7e038716c3f91cc0b8f31edb2c5ea812cd6dbe8b37b700589e39`.

Scénarios : Racine déjà utilisée.

~~~~text
### Requirement: Identité et FQDN explicites

Chaque Domaine MUST posséder une identité stable et un FQDN DNS explicitement choisi. Deux Domaines d'une même Instance MUST NOT déclarer le même FQDN exact. La position DNS MUST NOT créer d'approbation ni d'autorisation implicite.

#### Scenario: Racine déjà utilisée

- **WHEN** un Domaine demande le FQDN exact d’un autre Domaine de l’Instance
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante pixs-domains-686f4e13ff70

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 20. SHA-256 : `686f4e13ff70e8af073de2ac6f80d25d553a84feb6cec9fec11dc0f13c5d93cc`.

Scénarios : Deux sous-domaines; Faux suffixe.

~~~~text
### Requirement: ZT obligatoire dédié ou partagé

Chaque Domaine MUST utiliser une instance ZT. Il MAY créer son ZT ou utiliser celui de l'Instance lorsque son FQDN est égal au FQDN ZT ou en est un sous-domaine par labels DNS. Plusieurs Domaines admissibles MAY utiliser ce même ZT ; le partage MUST rester explicitement déclaré.

#### Scenario: Deux sous-domaines

- **WHEN** association.pixs.fr et recherche.pixs.fr choisissent le ZT pixs.fr
- **THEN** ils peuvent être rattachés avec des périmètres distincts.

#### Scenario: Faux suffixe

- **WHEN** association-autrepixs.fr demande le ZT pixs.fr en invoquant un suffixe de caractères
- **THEN** la condition hiérarchique DNS est refusée.
~~~~

### Référence courante pixs-domains-bd2991264b73

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 34. SHA-256 : `bd2991264b73d60314f90b7bb3d936bee405c507992fe50e7ff2e06fb1da6fc6`.

Scénarios : Même ZT sans politique.

~~~~text
### Requirement: Isolation dans un ZT partagé

Les politiques MUST pouvoir être propres à un Domaine ou partagées explicitement. Les communications inter-domaines MUST être refusées par défaut et nécessiter une politique explicite. Le partage du ZT MUST NOT fusionner les identités, ACL applicatives, annuaires ou realms.

#### Scenario: Même ZT sans politique

- **WHEN** deux acteurs de Domaines différents partagent ZT sans autorisation de communication
- **THEN** l’initiation inter-domaines est refusée.
~~~~

### Référence courante pixs-domains-c9ce061e2b23

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 43. SHA-256 : `c9ce061e2b23d3859a4cb92e01635334908d63f103ce5c9db7b2b2c1d5a053c5`.

Scénarios : ZT partagé et KZT manquant.

~~~~text
### Requirement: Services minimaux par Domaine

Chaque Domaine MUST disposer de sa PG indépendante, de ses organigrammes organisationnel/fonctionnel, d'au moins un LZT/OpenLDAP et d'un KZT/MIT Kerberos. Chaque Domaine MUST déclarer son realm, unique dans l'Instance. Les minima CZT/SZT/RZT/STZT/DZT/PKIZT MUST être évalués par ZT réel, pas dupliqués par déduction pour un ZT partagé.

#### Scenario: ZT partagé et KZT manquant

- **WHEN** un nouveau Domaine partage un ZT opérationnel mais ne possède aucun KZT
- **THEN** ses services de Domaine restent non opérationnels tant que ce minimum manque.
~~~~

### Référence courante pixs-domains-784b3416b755

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 52. SHA-256 : `784b3416b7559266c7a1b38d15a475ebd8b05a90e2f00eb976a8bf198703e0f4`.

Scénarios : Domaine sans tenant; Tenant rattaché deux fois.

~~~~text
### Requirement: Tenants et propriété des ressources

Un Domaine MUST accepter zéro, un ou plusieurs tenants ; chaque tenant MUST appartenir à un seul Domaine après transition. Les scopes enfants MUST rester rattachés à leur tenant sans cycles. Les propriétés Instance, Domaine et Tenant MUST être distinctes et n'accorder aucun droit implicite.

#### Scenario: Domaine sans tenant

- **WHEN** un Domaine opérationnel ne contient aucun tenant
- **THEN** ses services et son rattachement ZT restent valides.

#### Scenario: Tenant rattaché deux fois

- **WHEN** une mutation rattache simultanément un tenant à deux Domaines
- **THEN** elle est refusée sans ambiguïté de propriétaire.
~~~~

### Référence courante pixs-domains-8e5157150f7c

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 66. SHA-256 : `8e5157150f7c0a1801085b1c19bdd9c69fe4c345dcba246bb25ed2aba4727793`.

Scénarios : Affiliation sans admission.

~~~~text
### Requirement: Individus et identités multiples

Un individu Core MUST pouvoir être affilié à plusieurs Domaines et tenants et posséder plusieurs identités par Domaine. Chaque participation MUST conserver ses admissions, profils et habilitations. Une affiliation Core MUST NOT valoir admission ZT, sauf politique automatique explicite.

#### Scenario: Affiliation sans admission

- **WHEN** un individu est affilié à Recherche sans politique d’admission automatique
- **THEN** son appartenance ZT n’est pas créée par cette seule affiliation.
~~~~

### Référence courante pixs-domains-ba4dfa97bf7d

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 75. SHA-256 : `ba4dfa97bf7dfe8389d5a8f4597671aa9630b9e24d13f8a2ea071bc82dc36b12`.

Scénarios : Tenant transféré.

~~~~text
### Requirement: Transferts fonctionnels contrôlés V1

La V1 MUST prévoir les transferts autorisés d'identités numériques, données métier et tenants entre Domaines de la même Instance, avec vérification des dépendances, continuité des références et réévaluation des droits cibles. Le transfert MUST NOT copier implicitement des autorisations ni être présenté comme déplacement d'une brique exécutable.

#### Scenario: Tenant transféré

- **WHEN** un transfert de tenant est engagé entre deux Domaines
- **THEN** son identité est conservée, son propriétaire est unique et les habilitations de destination sont réévaluées.
~~~~

### Référence courante pixs-domains-2d4b91559aa3

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 84. SHA-256 : `2d4b91559aa387da2cb8be333d66674748a755850567e45bba8b742811112985`.

Scénarios : Transfert de département.

~~~~text
### Requirement: Structures organisationnelles non transférables V1

La V1 MUST NOT proposer le transfert fonctionnel de structures organisationnelles entre Domaines. Miroitage autorisé et réorganisation interne MUST rester distincts d'un tel transfert.

#### Scenario: Transfert de département

- **WHEN** une demande V1 vise à transférer un département entre Domaines
- **THEN** elle est refusée comme hors périmètre sans modifier les structures source ou cible.
~~~~

### Référence courante pixs-domains-f9d0dad1d882

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 93. SHA-256 : `f9d0dad1d882e815cf4d5b665b2037e6591dcb271ed3dd1e9f7605fcd4759334`.

Scénarios : Dernier Domaine.

~~~~text
### Requirement: Retrait du premier Domaine

Le premier Domaine MAY être retiré par procédure explicite si au moins un autre Domaine est opérationnel et si données, identités, authentification globale et dépendances sont traitées. Le retrait MUST NOT rétablir Standalone, laisser l'administration sans identité admissible ou retirer un ZT partagé encore requis.

#### Scenario: Dernier Domaine

- **WHEN** le retrait vise le seul Domaine opérationnel
- **THEN** il est refusé sans retour implicite en Standalone.
~~~~

### Référence courante pixs-domains-94814997f512

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 102. SHA-256 : `94814997f512912fbd83b186f7db3bf2f0771d0e37c0e5ecfc7fe81a41c5562f`.

Scénarios : Individu externe reconnu.

~~~~text
### Requirement: Approbations internes et externes

Les Domaines MUST pouvoir établir des approbations dans une même Instance ou entre Instances selon zt-instances. Un individu externe MUST conserver son identité d'origine ; la cible MUST conserver une référence et décider séparément de ses admissions et droits. Les composantes DNS et Kerberos MUST être explicites.

#### Scenario: Individu externe reconnu

- **WHEN** une approbation permet de reconnaître l’identité externe
- **THEN** la reconnaissance ne crée pas d’identité locale indépendante ou de droits automatiques.
~~~~

### Référence courante pixs-domains-d8fce09ab784

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 111. SHA-256 : `d8fce09ab78488325720197abff25a3f229a41ca7f6e38dac7da16c02df7b924`.

Scénarios : Reconstruction de Domaine.

~~~~text
### Requirement: Références PG et services de Domaine en mode normal ou critique

LZT et KZT MUST être obligatoires par Domaine. PG MUST rester souveraine pour les données de référence Pixs ; LDAP MUST porter l'état opérationnel Kerberos durable en mode normal. Une reconstruction complète depuis PG MUST suivre le mode critique autorisé, avec restauration protégée ou recréation/reprovisionnement selon profil et sauvegardes disponibles. La réplication LDAP MUST NOT remplacer la référence Core PG.

#### Scenario: Reconstruction de Domaine

- **WHEN** tous les annuaires du Domaine sont perdus
- **THEN** le Domaine applique sa procédure critique, distingue données de référence et clés récupérées/recréées, puis vérifie la remise en service.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| docker-image / 8 | [Composition reproductible corrélée à la release](../../specs/docker-image/spec.md#L8) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 22 | [Image sans état ni secret](../../specs/docker-image/spec.md#L22) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 31 | [Configuration validée à l'exécution](../../specs/docker-image/spec.md#L31) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 40 | [Sondes alignées sur les états de santé](../../specs/docker-image/spec.md#L40) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 49 | [Arrêt propre et orchestration sans autorité](../../specs/docker-image/spec.md#L49) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 58 | [Composition image PBO PFO et trois binaires PA](../../specs/docker-image/spec.md#L58) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 67 | [Événements PA limités au conteneur](../../specs/docker-image/spec.md#L67) | ND | CANDIDAT_DISTRIBUTION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence docker-image--eccd04c01b

Source : `openspec/specs/docker-image/spec.md`, ligne 8. SHA-256 du bloc : `26a434c02f066ab105de501c3639ec2efad7e21530b71b2df4d6beadfda1496c`.

~~~~text
### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des trois binaires système PZT
~~~~

### Référence docker-image--514331ad94

Source : `openspec/specs/docker-image/spec.md`, ligne 22. SHA-256 du bloc : `5974b07e2b5a54c8239a477d8e7e809fc8d874f12ac5840107a6780c2b22adf2`.

~~~~text
### Requirement: Image sans état ni secret

L'image MUST NOT contenir de secret, de token, de clé privée, de configuration effective ni de données persistantes ; toute persistance MUST rester hors de l'image via les stockages déclarés.

#### Scenario: Valeur sensible dans l'image

- **WHEN** une analyse détecte une valeur sensible dans une couche ou une métadonnée de l'image
- **THEN** la publication est refusée avec un diagnostic n'exposant pas la valeur
~~~~

### Référence docker-image--9fc683d3ec

Source : `openspec/specs/docker-image/spec.md`, ligne 31. SHA-256 du bloc : `a671f2f8947c154811f74235f744614b0dc1b4bd67e70150a3899c65aac1e295`.

~~~~text
### Requirement: Configuration validée à l'exécution

Le conteneur MUST recevoir sa configuration à l'exécution et la valider avant de passer à l'état de service ; il MUST NOT déduire fournisseur, tenant ou identité de l'état accidentel de l'image ou d'un système de fichiers éphémère.

#### Scenario: Démarrage avec configuration invalide

- **WHEN** un conteneur démarre avec une configuration incomplète ou invalide
- **THEN** il reste hors service avec une raison diagnostiquable au lieu de fonctionner dégradé silencieusement
~~~~

### Référence docker-image--67581165b1

Source : `openspec/specs/docker-image/spec.md`, ligne 40. SHA-256 du bloc : `a4efa5dab25ddc0f3cbba7953ebe0681f906e2e005fa399e522be1cfd7b606b6`.

~~~~text
### Requirement: Sondes alignées sur les états de santé

Les contrôles de santé du conteneur MUST être mappés sur les états distincts du socle et MUST NOT confondre vivacité et capacité à servir ; une dépendance optionnelle absente peut donner un état dégradé explicite, jamais une fausse disponibilité.

#### Scenario: Dépendance optionnelle indisponible

- **WHEN** une intégration optionnelle tombe dans un conteneur par ailleurs sain
- **THEN** la sonde d'exposition reflète l'état dégradé déclaré sans masquer une défaillance de sécurité
~~~~

### Référence docker-image--9b574db47f

Source : `openspec/specs/docker-image/spec.md`, ligne 49. SHA-256 du bloc : `82ad41afe40b83351156f395b3d52ddbfa880371520579dad7c624da84e4b516`.

~~~~text
### Requirement: Arrêt propre et orchestration sans autorité

Le conteneur MUST gérer le signal d'arrêt par un drain contrôlé jusqu'à un état final explicite dans une durée bornée ; l'orchestrateur reste un adapter qui ne devient ni autorité métier ni substitut des validations de composition.

#### Scenario: Arrêt demandé pendant un traitement

- **WHEN** l'orchestrateur demande l'arrêt d'une instance en cours de traitement
- **THEN** l'instance draine selon son contrat et l'état persistant permet la reprise sans double effet
~~~~

### Référence docker-image--a25571dc18

Source : `openspec/specs/docker-image/spec.md`, ligne 58. SHA-256 du bloc : `543b7c1ef253e674df6299fae94b3348f7fadf5961ed804581b5afaf3c413b23`.

~~~~text
### Requirement: Composition image PBO PFO et trois binaires PA

L’image Pixs MUST toujours contenir PBO, PFO, le module essentiel PZT côté PBO et exactement trois binaires PA : démon système, événements système du conteneur et exécution PZT. Elle MUST NOT contenir le binaire utilisateur PA ni ses modes session-start, session-stop et session-daemon.

#### Scenario: Composition image PBO PFO et trois binaires PA

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO et trois binaires PA sont présents et le binaire utilisateur est absent
~~~~

### Référence docker-image--bd24717e3a

Source : `openspec/specs/docker-image/spec.md`, ligne 67. SHA-256 du bloc : `67e439783126ef0a8a06f6fccd1b23f938cf3c990e477a02c907cfa37598baab`.

~~~~text
### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte
~~~~



## Référence BIND 9 adoptée le 24 octobre 2026

La sélection BIND 9 et sa distribution sont désormais normatives, selon
le [choix BIND 9 adopté](../adopt-bind9-managed-dns-and-packaging/proposal.md) et les exigences courantes suivantes :

- [Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite](../../specs/docker-image/spec.md#L131).
- [Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs](../../specs/pzt/spec.md#requirement-fournisseur-bind-9-du-dns-géré-sur-debian-et-docker-pixs).

Le [raccord propre à ce lot](design.md#choix-bind-9-adopté-le-24-octobre-2026)
précise ses responsabilités et les qualifications futures. Ce complément
est une référence au canon adopté, sans copie normative concurrente. Les
relevés historiques ci-dessus conservent leur date ; leurs autres clauses,
lignes et preuves restent à réconcilier avant réalisation. Aucune coche
d'implémentation, installation, construction ou activation n'est ajoutée.
