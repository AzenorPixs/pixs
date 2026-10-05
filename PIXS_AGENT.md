# Cahier des charges Pixs Agent

- Version : 0.0.6
- Date : 5 octobre 2026
- Statut : cahier des charges de conception avec modalités techniques à spécifier
- Dénomination conventionnelle du binaire : **Pixs Agent (PA)**
- Nom proposé du binaire : `pixs-agent`

Le binaire est conventionnellement appelé **Pixs Agent (PA)**. Il constitue
la troisième brique logicielle de Pixs et sert d'appui à **Pixs Backoffice
(PBO)** et à **Pixs Frontoffice (PFO)**. PA exécute des opérations locales sur
un système ou une session graphique et communique avec les instances Pixs
autorisées via le réseau Zéro Trust Pixs (PZT). Toute communication entre
PBO et PA passe par PZT, y compris sur le même hôte ou dans le même conteneur.

Ce cahier des charges rassemble le besoin exprimé et les exigences proposées
pour sa réalisation. La version 0.0.6 intègre WireGuard comme base logicielle
du transport PZT et les capacités inspirées de NetBird à développer dans Pixs.
Elle conserve les principes de conception validés et distingue les modalités
techniques restant à spécifier. Une recommandation inscrite au registre
d'arbitrages ne vaut pas une décision du développeur. Elle ne
constitue pas une spécification OpenSpec validée, une autorisation
d'implémentation ni une preuve de fonctionnement. La version du document est
distincte de la future version du logiciel.

## Positionnement des trois composants

| Composant | Abréviation conventionnelle | Responsabilité dans le cadrage |
| --- | --- | --- |
| Pixs Frontoffice | PFO | Interface utilisateur et interactions avec les capacités exposées par Pixs Backoffice. |
| Pixs Backoffice | PBO | Règles métier, autorisation applicative, API, orchestration et accès à la source de vérité PostgreSQL. |
| Pixs Agent | PA | Appui à PBO et PFO par l'exécution locale, l'observation et l'application des opérations autorisées sur les systèmes et sessions utilisateur. |

Les dénominations Pixs Agent, Pixs Backoffice et Pixs Frontoffice sont
conservées dans tout le document. Les abréviations PA, PBO et PFO désignent
respectivement ces trois composants. Le rôle d'appui de PA respecte leurs
frontières de responsabilité ; le détail fonctionnel de PBO et PFO reste
défini par les spécifications Pixs existantes.

Dans ce CdC, PZT désigne le réseau Zéro Trust Pixs, nommé ZTP dans
[ZERO_TRUST.md](ZERO_TRUST.md). Ces deux sigles renvoient au même réseau ;
PZT est le sigle utilisé dans le présent CdC.

Pixs Agent peut être installé sur une machine ou dans un conteneur sans
Pixs Frontoffice ni Pixs Backoffice. Leur présence locale ne modifie pas les
contrôles d'identité et d'autorisation. L'agent ne requiert pas un navigateur
pour fonctionner.

L'indépendance d'installation ne signifie pas que toute opération est possible
sans réseau. Les opérations locales et celles nécessitant un échange avec
Pixs Backoffice sont distinguées dans leur contrat.

### Pilotage par les modules de PBO et appui à PFO

Le pilotage réseau de PA passe par le module Pixs officiel ZTP défini dans
[ZERO_TRUST.md](ZERO_TRUST.md). Ce module appartient au système normal de
modules de PBO, avec ses contrats publics, données de gestion, migrations,
permissions, contributions frontend et lifecycle. Il consomme les primitives
de `pixs.core` par leurs contrats ; il n'est intégré ni au Kernel ni à
`pixs.core` et ne crée pas de référentiel d'identité concurrent.

Le socle de ce module est requis et protégé dans les profils PBO qui pilotent
PZT. Son retrait ou sa désactivation exige un retrait du réseau ou un
changement de profil contrôlé. Ses sous-modules enrichissent les capacités
par les interfaces publiques sans affaiblir les contrôles obligatoires.
Sa présence obligatoire dans tous les profils autonomes reste indécise,
conformément au CdC PZT.

Les fonctions réseau sont exécutées par PA selon ses rôles attribués. Les
autres opérations système ou utilisateur sont apportées par les modules
propriétaires de ces fonctionnalités, qui utilisent les interfaces publiques
de PA et PZT. Le module de pilotage réseau ne devient pas propriétaire de
toutes les règles métier ou opérations système.

PFO présente les informations et adresse ses demandes à PBO. PBO applique
les contrôles applicatifs avant de transmettre une instruction à PA via PZT.
Une liaison directe PFO–PA ne fait pas partie de ce contrat ; elle nécessiterait
un cadrage distinct préservant les mêmes frontières d'autorisation.

## Besoin exprimé

Le besoin initial couvre les éléments suivants :

- un logiciel développé en Python, compilé en passant par du C pour produire
  un binaire et rechercher de meilleures performances ;
- un déploiement sur un système d'exploitation ou dans un conteneur ;
- un fonctionnement en arrière-plan pour les activités permanentes ;
- une relation avec différentes instances Pixs via le réseau Zéro Trust Pixs ;
- le passage obligatoire par PZT de toute communication entre PBO et PA,
  même sur le même hôte ou dans le même conteneur ;
- des opérations ponctuelles au démarrage et à l'arrêt du système, avec des
  droits système ;
- un démon système lancé après un délai suivant le démarrage ;
- un démon PZT lancé sans délai au démarrage du système ou du conteneur,
  assurant la convergence et la réconciliation de PZT si celui-ci est activé
  et configuré sur ce PA, et se fermant sinon ;
- des opérations ponctuelles à l'ouverture et à la fermeture d'une session
  graphique, avec les droits de l'utilisateur ;
- un démon de session lancé après un délai suivant l'ouverture de la session ;
- des activités de fonctionnement, paramétrage, contrôle, surveillance et
  suivi des dérives, dans le contexte système ou utilisateur concerné.

Les sections suivantes décrivent les exigences du CdC pour répondre à ce besoin.
Les propositions de mécanismes concrets et les modalités non arrêtées sont
signalées à leur emplacement et dans le tableau des arbitrages.

## Composition et catalogue des capacités

Chaque capacité embarquée dans PA possède un identifiant stable, un
composant propriétaire, une version, des contrats publics, des dépendances,
un schéma de configuration, un profil de sécurité et des permissions
déclarées. Les opérations système et utilisateur font partie d'un catalogue
versionné dont les entrées sont rattachées à ces capacités.

La composition utilise les métadonnées et mécanismes communs de composants
Pixs, notamment les manifests `component.toml` lorsque le composant les
requiert. Son graphe, ses contrats, ses points d'entrée, ses dépendances et
ses contraintes de sécurité sont vérifiés avant activation. Une sélection
ambiguë ou une capacité obligatoire incompatible bloque le périmètre concerné.

La première réalisation utilise une composition au build. L'ajout de code
exécutable nécessite une nouvelle distribution vérifiée ; les messages PBO–PA
sélectionnent uniquement des opérations déjà livrées et autorisées. Aucun
chargement implicite de code distant n'est admis.

Cette composition ne remplace pas le runtime Django de PBO et n'impose pas
à PA d'embarquer Django ou PostgreSQL. Les garanties spécifiques de l'exécutable
PA seront définies dans une évolution OpenSpec dédiée, sans variante cachée
du runtime de référence.

## Capacités réseau PZT fondées sur WireGuard

WireGuard est utilisé comme logiciel de transport IP authentifié et chiffré.
PA pilote une implémentation éprouvée selon un adapter de plateforme qualifié ;
il ne réimplémente pas sa cryptographie. Les fonctions complémentaires sont
développées dans PZT et PA. Les briques, clients, serveurs et code NetBird ne
sont pas intégrés ; sa documentation sert de référence de capacités, sans
compatibilité implicite avec ses API, formats ou protocoles internes.

Le [CdC ZTP v0.3.0](ZERO_TRUST.md) décrit les garanties communes, les références
officielles et le registre A01 à A12. Ce CdC décrit leur application par PA.
L'usage de bibliothèques indépendantes reste soumis à qualification et à la
politique de dépendances Pixs. A01, A02 option A pour l'amorçage et A03
option A pour le transport local sur le même hôte d'exécution sont validés
par le développeur le 5 octobre 2026. Leurs modalités de réalisation restent
à préciser et qualifier.

| Capacité de PA | Responsabilité d'exécution | Contrôle et preuve attendus |
| --- | --- | --- |
| Adapter WireGuard | Configurer interfaces, pairs, endpoints, MTU et paramètres du backend. | État réel conforme au plan autorisé ; clés privées protégées. |
| Carte réseau | Vérifier et appliquer les versions, relations et décisions destinées au PA. | Refus des états non vérifiables ; resynchronisation après rupture de séquence. |
| Politiques réseau | Appliquer le filtrage entrant, sortant et transféré du profil. | Refus par défaut ; AllowedIPs et routes distincts des permissions de service et métier. |
| Connectivité | Négocier les chemins autorisés, sélectionner le direct ou un relais et gérer les changements. | Identités et permissions maintenues ; état direct/relayé rapporté. |
| Adressage et DNS | Appliquer adresses, routes, zones et règles de résolution déclarées. | Collisions détectées ; états invalidés retirés ; coexistence avec l'hôte. |
| Enrôlement | Produire les éléments publics et preuves et suivre admission, renouvellement et retrait. | Idempotence ; aucun secret exposé ; droits bornés avant admission. |
| Posture et TPM | Collecter les informations autorisées et produire les attestations requises. | Origine, fraîcheur et confiance distinctes ; une déclaration n'est pas une attestation matérielle. |
| Réconciliation et révocation | Comparer l'état souhaité et appliqué, retirer les accès invalidés et reprendre après interruption. | Confirmation ou écart explicite ; pas de résurrection d'accès révoqué. |
| Passerelle, si déclarée | Transférer les flux autorisés vers les ressources sans PA. | Accès aux ressources et aux services de la passerelle distincts ; protection du dernier segment déclarée. |
| Contrôle ou relais, si déclaré | Exécuter les services d'autorité, découverte, rendez-vous ou relais du rôle attribué. | Mandat propre au rôle ; aucun pouvoir déduit du mode système. |

### Backend et séparation des privilèges

Le périmètre demandé couvre Linux et Windows sur machines physiques et
virtuelles, ainsi que Docker et LXC sous Proxmox. A01, validé par le
développeur le 5 octobre 2026, privilégie le backend WireGuard du noyau Linux
et un backend natif Windows, dont WireGuardNT reste le candidat à qualifier.
Le traitement en espace utilisateur est retenu pour les profils qui le
nécessitent, après qualification. Ce choix couvre toutes les cibles demandées ;
il ne constitue pas une preuve de compatibilité de chaque environnement.

PA conserve la chaîne Python, génération C et compilation native, avec un
artefact pour chaque cible OS/CPU ; le backend WireGuard traite les paquets.
Les interfaces et dépendances du pilotage Linux et Windows sont qualifiées
séparément. Pour chaque profil en espace utilisateur, la nécessité, les
versions et les dépendances restent à préciser ; il ne dispense pas des
droits d'accès aux interfaces virtuelles et du filtrage requis.

Les adapters déclarent les interfaces de pilotage du noyau, routage, DNS
et filtrage, les privilèges nécessaires et les ressources gérées par PA.
Les mécanismes de filtrage sont retenus dans A04b, option A validée par le
développeur le 5 octobre 2026 : nftables sous Linux et Windows Filtering
Platform sous Windows, avec adapters PA et contrat commun de politiques PZT.
Les adapters traduisent les règles, vérifient l'état appliqué et identifient
les ressources PZT séparément des règles de l'opérateur. La coexistence,
les versions, bibliothèques, Netlink, outils système et interfaces exactes
restent à préciser et qualifier ; aucun remplacement global du pare-feu
existant n'est autorisé implicitement. Le choix ne prouve pas l'équivalence
des capacités par OS ni la protection après panne, qui relève de A05.
Aucun adapter n'accepte de commande shell libre reçue du réseau.
Les profils hôte, Docker et LXC distinguent namespace, TPM et périmètre
administré ; aucun montage, capacité ou accès à l'hôte n'est ajouté implicitement.

### Propriété des ressources et coexistence des modes

Chaque interface, route, règle et ressource DNS administrée possède un
propriétaire explicite. Les écritures concurrentes sont contrôlées et le
retrait ne supprime pas les éléments de l'opérateur ou d'un autre composant.
Une dérive est diagnostiquée ; sa correction exige une autorisation propre.

A04a, option A validée par le développeur le 5 octobre 2026, confie à
`pzt-daemon` la gestion permanente des interfaces WireGuard, routes, règles
de filtrage et ressources DNS PZT de son périmètre. Les six autres modes
lui soumettent leurs demandes autorisées sans modifier directement ces
ressources. Le propriétaire est identifié par périmètre ; un PA en conteneur
n'obtient aucun pouvoir implicite sur l'hôte Proxmox ou une autre instance.
Les sessions gardent leurs
identités distinctes et ne reçoivent pas les clés ou privilèges système.
Le mécanisme strictement interne entre invocations, son authentification,
ses permissions et sa traçabilité restent à spécifier. Il ne crée aucun canal
PBO–PA hors PZT. L'indisponibilité de `pzt-daemon` n'autorise aucune prise
de contrôle implicite des ressources par les autres modes. La protection
des accès actifs et la reprise après panne relèvent de A05. A04b retient
les mécanismes natifs de filtrage décrits ci-dessus ; leur réalisation
reste à qualifier pour chaque profil Linux, Windows, Docker et LXC.

### Amorçage, contrôle local et clés

L'amorçage prépare les liaisons de clés et les preuves nécessaires au premier
tunnel. A02, option A validée par le développeur le 5 octobre 2026, retient
un canal TLS authentifié intégré à PZT, limité à l'enrôlement, aux preuves
d'attestation requises et aux paramètres publics WireGuard. PA vérifie
l'autorité à partir d'un ancrage de confiance provisionné avant le premier
contact, puis présente ses justificatifs. Les preuves requises sont vérifiées
avant admission et activation des communications courantes : WireGuard
interhôtes ou TLS mutuel dans le profil local validé dans A03.
L'attente d'admission n'accorde aucun accès métier. Les formats, versions TLS,
bibliothèques et modalités de provisionnement restent à spécifier ; aucun
certificat client déjà délivré n'est supposé avant l'enrôlement. Reprise et
renouvellement respectent ces garanties sans ouvrir un contrôle général
hors du transport courant.

A03, option A validée par le développeur le 5 octobre 2026, retient TLS
mutuel intégré à PZT pour PBO et PA sur le même hôte d'exécution : même OS
hôte, même VM ou même conteneur selon le profil. Les échanges locaux
courants utilisent ce transport sans exiger un tunnel WireGuard local.
Des VM ou conteneurs distincts sur un même serveur physique conservent
leurs frontières réseau ; leur cohébergement ne suffit pas à appliquer
ce profil. L'endpoint, sa portée d'écoute et les mécanismes d'isolation
restent à qualifier selon la plateforme. PA applique aussi les permissions,
l'attestation, la révocation et l'audit PZT ; TLS mutuel ne les remplace pas.

PA distingue identité stable, certificat PZT, clé WireGuard et clé d'attestation
TPM. Les valeurs privées restent dans les périmètres protégés déclarés. La
non-exportabilité de la clé d'attestation ne prouve pas que la clé WireGuard
réside dans le TPM ; sa protection et sa résidence dans le backend sont
qualifiées séparément. Le mapping entre connexion logique PZT, tunnel,
canal de contrôle et renouvellement WireGuard relève de A10, sans exemption
d'attestation pour une connexion ou reconnexion ZTP.

### Adressage overlay et familles IP

A06a, option A validée par le développeur le 5 octobre 2026, retient IPv4
et IPv6 dès le socle PA/PZT : contrats, adresses, routes, filtrage et
qualification prennent en charge les deux familles. Chaque profil active
IPv4, IPv6 ou les deux selon sa configuration explicite ; une famille
non activée n'ouvre aucun accès PZT. Les adresses overlay sont distinctes
des endpoints du transport physique ; aucune connexion Internet IPv6 n'est
imposée. Un réglage unique « IPv6 activé » du périmètre PZT permet la
désactivation simple demandée par le développeur. PBO présente ce réglage
persisté et versionné avec ses permissions, états souhaité/appliqué et écarts.
Les valeurs par défaut restent à préciser. PA retire alors uniquement les
adresses, routes, annonces et autorisations IPv6 qu'il gère pour PZT,
cesse de publier les AAAA propres à PZT et ferme les échanges IPv6 concernés.
Il ne sélectionne plus d'endpoint IPv6 pour WireGuard ni les canaux TLS
d'amorçage ou locaux. L'IPv6 de l'hôte et les ressources de l'opérateur
ne sont pas désactivés ou modifiés implicitement.

La continuité exige une voie IPv4 autorisée ; sinon les accès concernés
restent bloqués avec diagnostic, sans repli hors PZT ni activation implicite
d'IPv4. Le retrait suit un plan vérifié, couvre les sessions existantes et
n'est pas annoncé réussi avant preuve de l'état appliqué. La réactivation
réconcilie les permissions, routes et preuves courantes sans restaurer des
droits périmés. PA applique les mêmes permissions, posture et révocation sur les
deux chemins, sans repli hors PZT. A06b, option A validée par le développeur
le 5 octobre 2026, retient le plan privé configurable et les allocations
par l'autorité compétente détaillés ci-dessous. PA applique les allocations
autorisées et vérifie les conflits du profil sans choisir seul un préfixe.
A06c, option B validée le 5 octobre 2026, retient le DNS Pixs développé et
géré par un module essentiel PBO, utilisable par PZT et tous les PA selon
leurs permissions ; PA applique les configurations autorisées du profil.

### Révocation, panne et diagnostic réseau

Une configuration WireGuard n'expire pas automatiquement avec un mandat PZT.
PA applique les retraits aux pairs, filtres, routes, noms et états de connexion
concernés. A05a, option A validée par le développeur le 5 octobre 2026,
retient le modèle hybride : après perte du contact avec l'autorité, seules
les permissions déjà accordées, encore vérifiables et réutilisables selon
leur classe subsistent jusqu'à leur échéance, sans renouvellement implicite
ni période de grâce. Une révocation connue s'applique dans le délai déclaré
sans attendre l'expiration ; les classes exigeant une décision en ligne la
conservent.

Une protection indépendante du processus PA garantit les expirations et
fermetures préautorisées lorsque PA est arrêté ou planté et que le noyau
conserve ses ressources. Elle n'accorde aucun accès, ne renouvelle aucune
permission et ne prend pas la gestion générale des ressources de `pzt-daemon`.
Sa réalisation, son propre comportement après panne et les délais A05b sont
à qualifier. Le profil n'est pas qualifié avant preuve de ces garanties.
Le redémarrage exige une réconciliation vérifiée et ne réactive aucun accès
expiré ou révoqué ; reprise et compensation restent bornées.

Les changements réseau suivent un plan et une application sans fenêtre
permissive, vérifiée par postcondition. Le canal de contrôle est vérifié avant
retrait de l'ancien chemin selon le plan autorisé. Une application partielle
n'est pas un succès et sa reprise n'élargit pas les permissions.

Les diagnostics distinguent tunnel configuré, dernier handshake, destination
joignable, service disponible et opération autorisée. Un handshake récent
ne prouve ni la readiness ni la réussite métier. Les mesures de chemin,
route, DNS, posture, fraîcheur et révocation respectent les permissions de
consultation et ne publient jamais de clé privée ou de jeton.

## Modes d'exécution

Les sept modes sont des invocations distinctes du même binaire. Le contexte
et le mode sont explicites ; ils ne sont pas déduits de la présence d'un
Pixs Backoffice local. Les noms techniques ci-dessous sont proposés et les
options de ligne de commande restent à spécifier.

| Mode proposé | Déclencheur | Durée | Droits | Finalité |
| --- | --- | --- | --- | --- |
| `system-start` | Démarrage du système ou du conteneur | Ponctuelle | Système | Opérations liées au démarrage. |
| `system-stop` | Arrêt contrôlé du système ou du conteneur | Ponctuelle et bornée | Système | Opérations liées à l'arrêt. |
| `system-daemon` | Démarrage du système ou du conteneur, après délai | Permanente | Système | Fonctionnement, paramétrage, contrôle, surveillance et dérives. |
| `session-start` | Ouverture d'une session graphique | Ponctuelle | Utilisateur de la session | Opérations liées à l'ouverture. |
| `session-stop` | Fermeture contrôlée d'une session graphique | Ponctuelle et bornée | Utilisateur de la session | Opérations liées à la fermeture. |
| `session-daemon` | Ouverture d'une session graphique, après délai | Permanente, limitée à la session | Utilisateur de la session | Fonctionnement, paramétrage, contrôle, surveillance et dérives. |
| `pzt-daemon` | Démarrage du système ou du conteneur, sans délai | Permanente | Système | Assure la convergence et la réconciliation de PZT si celui-ci est activé et configuré sur ce PA, sinon se ferme. |

Une invocation ponctuelle produit un résultat et se termine. Un démon reste
actif jusqu'à son arrêt, son échec ou la disparition de son contexte. Les
modes sont activables séparément dans le profil de déploiement.

### Amorçage et provisionnement

Avant le premier échange PBO–PA, une procédure explicite de provisionnement
établit la configuration minimale de PA, son identité technique, les ancrages
de confiance et les références de secrets nécessaires à PZT. Ces éléments
sont fournis au déploiement et restent hors du binaire et des artefacts de
distribution. Leur origine, leur intégrité et les permissions de l'opérateur
de provisionnement sont vérifiables et auditables.

Cette procédure est distincte d'un échange de contrôle PBO–PA. Elle ne peut
pas servir de canal continu de commandes par fichiers contournant PZT.
Le premier PBO rencontré n'est jamais approuvé automatiquement ; aucun
compte administrateur, secret commun ou droit de production par défaut n'est
créé implicitement.

Le provisionnement expose un état non provisionné, en cours, prêt ou échoué.
Une interruption reprend depuis un état durable sans dupliquer une identité
ou une autorisation. Une référence de secret ou un ancrage de confiance
invalide bloque les communications et les opérations qui en dépendent.

L'initialisation minimale nécessaire à PZT est distinguée de l'activation
différée des activités permanentes de fonctionnement et de surveillance.
Le septième mode `pzt-daemon` démarre sans délai pour assurer la convergence
et la réconciliation de PZT lorsque celui-ci est activé et configuré sur ce PA ;
sinon, il se ferme. Les délais de `system-daemon` et de `session-daemon` sont
préservés. Le séquencement exact de l'initialisation minimale PZT et les
préconditions de chaque mode restent à qualifier dans l'adaptateur de plateforme.

Sans PBO joignable, PA peut uniquement initialiser les capacités et réaliser
les opérations locales explicitement provisionnées, éligibles et encore
autorisées. Il ne s'attribue pas de mandat ni de nouvelle autonomie de gouvernance.

### Délais et préconditions de démarrage

Les délais de `system-daemon` et de `session-daemon` sont indépendants,
configurables et non négatifs. Aucune valeur numérique n'est fixée en v0.0.6.
Le mode `pzt-daemon` n'est pas soumis à ces délais ; son démarrage sans délai
ne dispense pas des préconditions et contrôles d'autorisation applicables.

**Proposition :** mesurer le délai système depuis le début du cycle de
démarrage concerné et le délai utilisateur depuis l'ouverture de la session
graphique concernée. L'adaptateur de plateforme définit un événement
observable et une mesure monotone, indépendante des corrections de l'heure.

Un délai écoulé ne prouve pas la disponibilité du réseau, des fichiers ou
des services nécessaires. Chaque opération déclare ses préconditions et
une attente maximale. Une précondition absente conduit à un état explicite
d'attente, d'indisponibilité ou d'échec.

L'arrêt du système ou de la session pendant le délai annule le démarrage
différé. La reprise après un redémarrage du seul processus démon doit être
spécifiée sans être confondue avec un nouveau démarrage du système ou une
nouvelle ouverture de session.

### Arrêt et fermeture de session

Les opérations d'arrêt sont conçues pour des événements contrôlés. Une panne
électrique, un arrêt forcé ou la destruction immédiate du processus ne permet
pas de garantir leur exécution. Une opération interrompue reste incomplète ;
elle n'est jamais déclarée réussie par déduction.

L'intégration définit l'ordre entre le démon, l'instance ponctuelle d'arrêt
et les dépendances nécessaires. Elle évite qu'une action d'arrêt soit exécutée
deux fois ou concurrence une action permanente incompatible.

Les opérations de fermeture disposent d'une durée maximale. Elles ne doivent
pas suspendre indéfiniment l'arrêt du système ou la déconnexion. Si le réseau
est déjà indisponible, le résultat local suit la politique de reprise prévue.

L'ordre d'arrêt conserve PZT tant que les échanges nécessaires avec PBO restent
possibles dans le budget d'arrêt. Les nouvelles opérations incompatibles
avec la fermeture sont refusées et les traitements en cours sont drainés
ou interrompus selon leur contrat avant l'arrêt des dépendances concernées.
Les instances de session restent limitées à la durée de leur session réelle.

L'impossibilité de transmettre un résultat ne permet pas un canal hors PZT.
Un résultat technique conservé pour reprise reste distingué d'un résultat
reçu et confirmé par PBO. Une extinction brutale ne crée aucune preuve
d'exécution ou de livraison.

Dans Docker, le processus principal reçoit un signal d'arrêt puis peut être
tué à l'expiration du délai. L'intégration doit donc propager le signal à
Pixs Agent et réserver un budget suffisant à ses opérations de fermeture.
Ce fonctionnement est décrit par la [documentation Docker sur l'arrêt des
conteneurs](https://docs.docker.com/reference/cli/docker/container/stop/).

### Sessions graphiques et concurrence

Une session graphique est identifiée séparément du compte utilisateur.
Plusieurs utilisateurs, ou plusieurs sessions d'un même utilisateur, peuvent
être actifs simultanément. Les états et les actions sont isolés par session.

La fermeture d'une session arrête son démon sans arrêter ceux des autres
sessions. Le verrouillage de l'écran et la suspension de la machine ne sont
pas assimilés à une fermeture de session.

**Proposition :** commencer par une instance permanente système par cible
et une instance permanente par session graphique. Un mécanisme local empêche
les doublons dans ce périmètre sans devenir une autorité métier Pixs.

Un gestionnaire de services utilisateur peut avoir une durée de vie différente
de celle d'une session graphique. Le futur adaptateur doit prouver le lien
avec la session réelle. L'autostart XDG couvre le lancement à l'ouverture du
bureau ; un mécanisme de fermeture doit être spécifié séparément.
Voir la [spécification Desktop Application Autostart](https://specifications.freedesktop.org/autostart/latest/).

## Opérations locales et suivi des dérives

Chaque opération déclare un identifiant, une version, son contexte, ses
paramètres validés, ses cibles, ses privilèges nécessaires, ses préconditions,
son délai maximal et son résultat attendu. Son caractère idempotent, sa
politique de reprise et ses effets de bord sont explicites.

Les familles fonctionnelles proposées sont :

| Famille | Résultat attendu |
| --- | --- |
| Fonctionnement | Vérifier les préconditions et réaliser une activité locale autorisée. |
| Paramétrage | Appliquer une configuration approuvée dans un périmètre déclaré. |
| Contrôle | Comparer un état observé à une règle ou à une configuration attendue. |
| Surveillance | Suivre périodiquement des signaux déclarés et produire des événements. |
| Dérive | Identifier un écart, sa référence, sa date de détection et son impact. |

Le catalogue exact des opérations reste à définir. Les exemples de gestion
de services, de fichiers ou de paramètres système ne valent pas autorisation
de les implémenter ou de les exécuter.

**Proposition :** la détection d'une dérive produit d'abord un constat.
Une correction automatique est une capacité distincte, désactivée tant
qu'une politique explicite ne l'autorise pas. Elle possède ses propres
contrôles, critères de réussite, limites et stratégie de compensation.

Les actions sont sélectionnées dans un catalogue déclaré et livré par une
chaîne de distribution contrôlée. Un message réseau ne permet pas, à lui
seul, de télécharger du code, d'évaluer du Python ou d'ouvrir un shell avec
des droits système.

### Préparation et application des opérations sensibles

L'observation, la génération d'un plan et son application sont des opérations
distinctes. Le plan versionné identifie les changements, les ressources
affectées, les privilèges, les risques, les préconditions, les validations
attendues et la compensation éventuelle. Il porte une durée de validité et
une référence à l'état ou à la version de configuration observée.

Une modification sensible exige une confirmation autorisée ou une étape
d'application distincte de la préparation du plan. Au moment de l'application,
PA contrôle le mandat, les obligations et l'état courant de la cible.
Un plan expiré ou devenu obsolète est refusé jusqu'à nouvelle validation.
Une simulation ou un diagnostic ne réalise aucune mutation système ou métier.

La correction automatique d'une dérive reste une capacité distincte et
explicitement autorisée. Ses limites de fréquence, de tentatives, de concurrence
et de périmètre empêchent une boucle de corrections. Une compensation est
prévue uniquement lorsque ses effets et sa faisabilité sont déclarés ;
elle ne vaut pas promesse de retour arrière universel.

### Protection du contrôle pendant une reconfiguration réseau

Une opération modifiant le réseau ou PZT décrit son impact sur le canal de
contrôle. Son plan prévoit une validation de la nouvelle connectivité et,
lorsque cela est possible, une compensation préautorisée avec un déclencheur
et une durée bornés. Le comportement en cas de perte de contact est fixé
avant l'application.

Une compensation ne réactive jamais une identité révoquée, un mandat expiré
ou une permission supprimée. Une perte de contrôle sans compensation sûre
produit un état explicite à traiter par la procédure de reprise. Aucun canal
PBO–PA hors PZT n'est ouvert pour masquer l'échec.

### Réception et preuve de l'exécution

Le contrat distingue une instruction reçue, validée, en cours, réussie,
échouée, interrompue ou dont le résultat est indéterminé. Ces états décrivent
l'exécution technique de PA ; la confirmation applicative par PBO et la
livraison du résultat sont des dimensions séparées. Un accusé de réception
ne constitue pas une preuve d'application ou de réussite.

Les identifiants d'instruction, de Command, d'opération et de Job, lorsqu'ils
existent, restent distincts, corrélés et stables pendant les reprises.
La clé d'idempotence, l'empreinte du contenu, les tentatives et les preuves
utiles sont conservées selon une fenêtre de rejeu déclarée. Une même clé
avec un contenu différent produit un conflit.

Un crash après un effet système et avant l'enregistrement du résultat laisse
un résultat indéterminé. PA vérifie la postcondition lorsque le contrat le
permet, ou demande une intervention autorisée ; il ne rejoue pas aveuglément
une action dangereuse. La garantie ne promet pas `exactly-once` de bout en bout.

## Droits système et droits utilisateur

Les quatre modes système disposent des droits nécessaires à leurs opérations
système. Le détail du compte d'exécution, des capacités et des modalités de
séparation des privilèges reste à spécifier. Un fonctionnement sous `root`
doit être justifié par les opérations concernées et leur environnement.

Les trois modes utilisateur s'exécutent avec les droits de l'utilisateur
de la session. Ils ne s'élèvent pas implicitement et ne modifient pas les
ressources d'un autre utilisateur ou du système sans un contrat distinct
explicitement autorisé.

La configuration, les états, les identités techniques et les communications
locales des deux contextes sont séparés. Si un canal entre processus est
nécessaire, il vérifie l'identité de l'appelant et l'autorisation de l'action.
Une donnée fournie par une session ne constitue pas une commande privilégiée.
Lorsqu'un tel canal relie PBO et PA, il passe obligatoirement par PZT.

Les privilèges dans un conteneur s'appliquent à son périmètre déclaré.
Ils ne confèrent aucun droit implicite sur l'hôte. Les montages, capacités
et accès à l'hôte nécessaires doivent être inventoriés et validés.

### Séparation des fonctions et des privilèges

Les fonctions de communication PZT, de surveillance et d'exécution privilégiée
possèdent des frontières explicites. Chaque fonction reçoit uniquement les
secrets, ressources, fichiers et capacités système nécessaires. Les instances
de session ne reçoivent ni les clés réservées au contexte système ni ses
permissions d'exécution.

Une séparation en processus utilisant le même binaire peut mettre en œuvre
ces frontières. Son organisation exacte reste à qualifier ; le partage d'un
binaire ne justifie pas un processus cumulant implicitement tous les droits.
Les comptes, canaux locaux internes et ressources partagées sont déclarés
et contrôlés selon le profil.

## Relation avec Pixs Backoffice et le réseau PZT

Pixs Agent communique avec une ou plusieurs instances Pixs explicitement
autorisées. Chaque relation possède un périmètre, des capacités et des
versions de contrat identifiables. Plusieurs connexions ne signifient pas
que plusieurs Pixs Backoffice peuvent administrer librement la même cible.

Le CdC [Zéro Trust Pixs](ZERO_TRUST.md), actuellement en v0.3.0,
décrit les orientations réseau. Il reste lui aussi un document de conception.
PA exécute PZT selon les rôles attribués, sous le contrôle et la configuration
de PBO dans le périmètre autorisé. Ce rôle ne lui attribue pas automatiquement
les pouvoirs d'autorité, de certification, de relais ou de Pixs Backoffice.

### Passage obligatoire par PZT

Toute communication entre un PBO et un PA doit passer par PZT, dans les
deux sens et pour chacun des sept modes d'exécution. Cette obligation couvre
les instructions, la configuration, l'administration, les consultations
d'état, les diagnostics, les événements et les résultats d'opérations.

Elle s'applique entre machines distantes, sur le même hôte et dans le même
conteneur. La proximité, un compte système commun ou des permissions locales
ne constituent aucune exemption. Un canal direct entre PBO et PA contournant
PZT est interdit, y compris via une socket Unix, une adresse de boucle locale
ou des fichiers utilisés comme canal d'échange.

Le transport TLS mutuel local validé dans A03 est intégré à PZT et applique ses garanties
d'identification, d'authentification mutuelle, d'autorisation, de chiffrement,
de validité, de protection contre le rejeu et de traçabilité. Ses endpoints
et leur isolation restent à qualifier ; le passage par PZT n'impose pas
un détour par un relais distant.
Les permissions du système d'exploitation restent des protections
complémentaires et ne remplacent pas les contrôles PZT.

Si le canal PZT requis est indisponible ou si ses preuves ne sont pas
vérifiables, la communication concernée est bloquée avec un diagnostic
explicite. Aucun repli vers un canal local hors PZT n'est autorisé.

Le provisionnement et l'initialisation décrits dans la section Amorçage et
provisionnement établissent les prérequis de ce canal. Leur séquencement
technique reste à spécifier sans canal d'amorçage PBO–PA contournant PZT.

Les exigences de communication de PA sont les suivantes :

- enrôlement explicite et identité technique propre ;
- vérification de l'identité attendue du correspondant ;
- échanges authentifiés et chiffrés, y compris via un relais autorisé ;
- autorisation du canal distincte de l'autorisation des opérations ;
- contrôle de l'émetteur, de la cible, de l'action, du périmètre, de la validité
  et de la fraîcheur avant exécution ;
- révocation, renouvellement et rotation selon la politique réseau applicable ;
- protection contre le rejeu et corrélation des demandes et des résultats ;
- refus lorsque les preuves requises sont absentes, invalides ou périmées.

Une appartenance au réseau, un certificat valide ou la présence locale de
Pixs Backoffice ne suffisent pas à autoriser une action.

L'identité du système, celle du processus agent, l'utilisateur local et
l'identité applicative Pixs sont distingués. Leur association éventuelle
est explicite ; un identifiant local ne crée pas une permission Pixs.

### Contrat des instructions de contrôle

Chaque instruction PBO–PA expose, lorsque applicable à l'opération :

- l'identité vérifiée du PBO émetteur, l'acteur initial et l'exécuteur technique ;
- l'identifiant de l'instruction, l'opération demandée et sa version de contrat ;
- la cible canonique et le contexte de plateforme, de tenant ou de scope ;
- les paramètres typés, bornés et validés ;
- la référence du mandat, son émetteur, ses actions, ses limites et sa validité ;
- les versions de politique et de délégation, les exigences de fraîcheur,
  d'assurance et les obligations applicables ;
- les références de corrélation, de causalité et de suivi, ainsi que la clé
  d'idempotence et la référence du plan lorsqu'elles sont requises.

PA vérifie l'identité attendue, le destinataire, la cible, le contenu et les
preuves au moment de l'exécution, y compris après attente ou reprise.
Une permission de surveillance ne permet pas une reconfiguration. L'acteur
initial reste traçable sans élargissement de son périmètre par l'exécuteur.

Les autorisations de canal PZT, les décisions applicatives de PBO et les
permissions techniques d'exécution restent distinctes. PBO conserve l'autorité
métier Django ; les contrôles de PA appliquent le mandat et les limites de
l'exécution locale sans constituer une autorité métier concurrente.

Une opération modifiant les protections de PA ou PZT exige les obligations
renforcées déclarées par la politique, notamment une confirmation, une assurance
supérieure ou une décision en ligne lorsqu'elles sont requises. Une obligation
non satisfaite bloque l'action. Les détails de format et le protocole concret
seront définis par les contrats publics et l'évolution OpenSpec correspondante.

Les instants de validité des mandats sont exprimés en UTC selon une source
de temps et des tolérances déclarées par PZT. Un temps non fiable ou une
validité temporelle non vérifiable bloque l'opération concernée. Les mesures
monotones des délais de démarrage et d'arrêt ne remplacent pas cette référence
temporelle d'autorisation.

### Plusieurs instances Pixs et conflits

**Proposition :** commencer avec une autorité d'administration explicite
par ressource ou périmètre, et des délégations bornées pour les autres
instances. Les autres modèles restent à arbitrer.

Des instructions contradictoires ou concurrentes ne sont pas résolues
par le dernier message reçu. L'agent bloque les actions incompatibles,
conserve un diagnostic et applique une politique de priorité validée.
L'isolation des relations empêche une instance d'accéder aux configurations,
résultats ou identités d'une autre sans autorisation explicite.

### Contrats et autorité applicative

Pixs Backoffice conserve les règles métier, l'autorisation applicative et
la source de vérité PostgreSQL. Pixs Agent réalise l'exécution locale et
les contrôles techniques prévus par le contrat ; il ne confirme pas de son
propre chef une mutation métier Pixs.

Les échanges applicatifs passent par des contrats publics versionnés.
L'agent n'accède pas directement aux tables PostgreSQL d'une instance Pixs.
Les règles d'API, d'identité, de tenant, de scope et de confidentialité
continuent de s'appliquer. Un canal Zero Trust ne contourne aucune limitation
intertenant existante.

Le protocole de réception des instructions, de livraison des résultats et
de diffusion des configurations reste à définir. Les versions incompatibles
conduisent à un refus explicite des capacités concernées.

## Indisponibilité réseau et reprise

L'absence de Pixs Backoffice local est un déploiement normal. Une instance
distante indisponible est une situation distincte, diagnostiquée par relation.

Seules les opérations locales explicitement éligibles, dont la configuration
et les autorisations demeurent vérifiables, peuvent être exécutées.
Une action requérant une autorisation en ligne reste bloquée. Une perte réseau
ne déclenche ni un mode permissif ni une nouvelle autonomie de gouvernance.
Une opération strictement interne à PA, sans échange avec PBO, reste distincte
d'une communication PBO–PA. Son éventuelle éligibilité locale n'autorise jamais
un contournement de PZT pour recevoir une instruction ou transmettre un résultat.

### Reprise locale de PZT

L'indisponibilité du réseau distant est distincte de celle de PZT dans son
ensemble. Un profil local de PZT permet le diagnostic et la réparation depuis
PBO lorsque ce profil reste disponible et que les identités, permissions,
preuves de validité et exigences de fraîcheur sont vérifiables. Il conserve
l'authentification mutuelle, le chiffrement, la protection contre le rejeu et
l'audit ; il ne dépend pas exclusivement d'un relais ou d'une autorité distante.
Une opération exigeant une décision en ligne indisponible reste bloquée.

Cette distinction précise l'administration locale de reprise décrite par le
CdC PZT sans créer d'exemption au passage obligatoire par PZT. Si PZT lui-même
est entièrement indisponible, aucun échange PBO–PA n'est possible. Une éventuelle
réparation par un opérateur système suit une procédure distincte, explicitement
autorisée et auditée, qui ne constitue pas une communication PBO–PA ni un canal
local de contrôle de substitution.

### Propriété et persistance des états

| Catégorie | Autorité et conservation |
| --- | --- |
| État métier et décisions de référence | PBO et la persistance autoritative Pixs, avec les contrats et contrôles applicables. |
| État de contrôle PZT | Propriétaire et source autoritative définis selon le CdC PZT ; les politiques, délégations et révocations ne sont pas des décisions locales indépendantes de PA. |
| État technique local de PA | Exécution, déduplication, résultats en attente, configuration appliquée et reprise, selon un contrat de persistance dédié. |
| Secrets d'identité | Fournisseur runtime protégé, accessible aux seuls composants autorisés, avec rotation et révocation. |

Le contrat de persistance technique déclare les états conservés, leur
durabilité, les limites de stockage, la rétention, le contrôle d'accès,
les protections d'intégrité et les conditions de restauration. En conteneur,
un état nécessaire à la reprise ne dépend pas d'un filesystem éphémère.
Les garanties et le provider local restent à spécifier explicitement avant
implémentation ; ils ne modifient pas implicitement les exigences stateless
du runtime PBO.

Les projections et intentions métier restent soumises à `offline-first` et
ne deviennent pas des décisions confirmées. Les clés techniques nécessaires
à l'identité de PA sont résolues par références via le fournisseur de secrets ;
elles ne sont jamais intégrées à ces projections, au journal d'exécution ou
aux résultats en attente.

La persistance technique locale ne remplace pas l'état autoritatif des services
PZT. La gestion PBO et les fonctions d'autorité exécutées par PA ne décident
pas indépendamment de la validité d'un même mandat. Leur coordination et un
éventuel stockage spécialisé restent soumis au contrat PZT et à une capacité
explicitement spécifiée et validée.

Un stockage plein, indisponible ou corrompu produit un diagnostic explicite.
Une opération nécessitant une preuve durable d'autorisation, d'exécution,
d'audit ou de déduplication est bloquée si cette garantie ne peut être tenue.
Les capacités indépendantes peuvent rester disponibles uniquement selon
leur contrat et sans perte silencieuse ni repli permissif.

Une restauration ne réintroduit pas un droit révoqué ou un mandat expiré.
La validité, la fraîcheur, la configuration et les postconditions sont
réévaluées avant reprise ; un état trop ancien ou non vérifiable est bloqué.

La reprise distingue les opérations non commencées, en cours, interrompues
et terminées. Un résultat inconnu n'est pas assimilé à un succès ni à une
preuve d'absence d'effet. Les retries sont bornés et n'engagent pas une action
non idempotente sans stratégie de reprise validée.

## Configuration et observabilité

La configuration est externe au binaire, typée, versionnée et validée avant
activation. Les valeurs effectives suivent la hiérarchie de configuration
Pixs. Les domaines à spécifier comprennent :

- les modes activés et les cibles système ou session ;
- les délais de démarrage et les préconditions ;
- les relations avec les instances Pixs et les références d'identité ;
- les opérations autorisées, les fréquences et les limites de concurrence ;
- les durées maximales, les retries et les politiques d'arrêt ;
- les budgets de ressources, la rétention et les possibilités de reprise.

Les noms de clés, les formats et leurs valeurs par défaut ne sont pas figés
par ce document. Les secrets sont fournis par référence via un mécanisme
runtime protégé ; ils ne figurent ni dans le binaire ni dans les journaux.

### Configuration souhaitée et configuration appliquée

PBO conserve la configuration souhaitée ; PA rapporte celle effectivement
appliquée, sa version, son résultat et les écarts. Une configuration envoyée
ou reçue n'est pas présentée comme appliquée avant confirmation vérifiable.

L'application contrôle l'autorisation, le schéma, la compatibilité, les
préconditions et la version de concurrence attendue. Le contrat fixe sa
frontière d'application et les états intermédiaires. Un conflit, une application
partielle ou une interruption restent diagnostiquables et suivent la politique
de reprise, sans restauration d'une configuration devenue interdite.
Un feature flag ne retire pas une capacité requise et ne modifie pas
implicitement les permissions, providers ou contraintes PZT.

### Santé et diagnostic

Les diagnostics distinguent le démarrage, la vivacité, la capacité à exécuter
les opérations et la connexion à chaque instance Pixs. Un démon vivant peut
être dégradé ou incapable d'exécuter une opération protégée.

Les événements techniques portent au minimum les références du composant,
du mode, de la cible, de l'opération et de la corrélation, ainsi que le résultat
et la cause d'un refus ou d'un échec. Les références de session et d'utilisateur
sont minimisées ou pseudonymisées. Aucune donnée personnelle ou sensible n'est
exposée dans les diagnostics génériques.

### Maintenance et quarantaine

Les profils déclarent un fonctionnement normal, un mode de surveillance seule,
une maintenance et une quarantaine avec leurs portées, opérations permises,
interdites et conditions de sortie. Ces états n'accordent aucun nouveau droit.
Une maintenance draine les traitements dans une durée bornée et refuse les
nouvelles modifications incompatibles avec sa portée.

La quarantaine peut limiter les communications et suspendre des opérations
sans supprimer les données ni le socle requis de pilotage PZT. Les fonctions
de diagnostic ou de reprise restent accessibles uniquement selon les permissions
et le profil PZT autorisés. La sortie réévalue identité, mandats, composition,
configuration, dépendances et santé avant réactivation.

### Audit et interfaces d'exploitation

Les actions privilégiées et les événements de sécurité produisent un audit
distinct des logs techniques, avec acteur initial, exécuteur, référence du
mandat, action, cible, périmètre, versions utiles, horodatage UTC, résultat
et corrélation. L'audit est durable, protégé et append-only dans son usage
normal, avec rétention et accès séparés des autres signaux. Une obligation
d'audit doit être satisfaite avant d'autoriser l'action concernée.

Les logs, métriques et traces utilisent des structures compatibles avec
l'observabilité Pixs et propagent le contexte W3C lorsque le transport le
permet. Les sondes de démarrage, vivacité et disponibilité restent distinctes,
bornées et sans mutation ; leurs détails ne sont accessibles qu'aux opérateurs
autorisés.

Les interfaces non interactives fournissent des erreurs structurées et des
codes de sortie stables. Les messages humains sont internationalisables dès
la première réalisation, avec catalogues appartenant au composant et locale
canonique `en`. Les codes, noms de champs et structures contractuelles restent
non localisés. La CLI et les façades d'administration utilisent les mêmes
contrats ; lorsqu'elles relient PBO à PA, leurs échanges passent par PZT.

## Compilation et objectifs de performance

La chaîne cible part des sources Python, génère du C puis produit un
exécutable natif pour chaque plateforme supportée. Les dépendances runtime
et bibliothèques natives nécessaires sont inventoriées. L'autonomie visée
est une installation sans Pixs Frontoffice ni Pixs Backoffice, avec un runtime
embarqué si nécessaire pour éviter un interpréteur Python installé séparément.

**Candidat à évaluer, non retenu :** Nuitka propose des modes de distribution
autonomes et s'appuie sur un compilateur C. Sa compatibilité avec le Python,
les dépendances et les plateformes retenus doit être qualifiée. Voir le
[manuel officiel Nuitka](https://nuitka.net/user-documentation/user-manual.html).

La génération de C ne suffit pas à démontrer un gain de performance.
La qualification compare les mêmes opérations dans la version Python
et dans la version compilée, avec les mêmes entrées et contrôles de sécurité.
Elle distingue les traitements CPU, les attentes réseau et les accès système.

| Mesure | Qualification attendue |
| --- | --- |
| Temps de lancement | Mesurer séparément les invocations ponctuelles et les démons. |
| CPU et mémoire | Mesurer au repos, en surveillance et en exécution d'opérations. |
| Latence et débit | Mesurer sur un catalogue et une charge représentatifs. |
| Coût réseau et disque | Mesurer les échanges, les journaux et la reprise. |
| Taille et dépendances | Inventorier l'artefact, son runtime et ses bibliothèques. |
| Arrêt | Mesurer la durée de drainage et des opérations de fermeture. |

Les seuils, machines de référence, charges et durées de mesure restent à
valider. Aucun gain chiffré ni budget universel n'est annoncé en v0.0.6.
Une optimisation ne peut affaiblir les autorisations, l'isolation ou l'audit.

## Plateformes et distribution

**Périmètre de conception demandé le 5 octobre 2026 :** PA sur machines
physiques Linux et Windows, machines virtuelles Linux et Windows, conteneurs
Docker et conteneurs LXC sous Proxmox. La conception ne se limite pas à Debian.
Les versions, architectures et profils doivent encore être qualifiés ; le
périmètre demandé n'est pas une preuve de support logiciel déjà disponible.
`DEVOPS.md` décrit l'environnement de développement Debian 13 et Python
3.14.8 ; `pyproject.toml` déclare Python >=3.12. Ces références ne fixent pas
implicitement les versions de Windows ou de Proxmox supportées par PA et
ne déplacent pas le runtime de PBO sur Windows.

| Environnement PA demandé | Frontière technique | Qualification attendue |
| --- | --- | --- |
| Machine physique Linux | Noyau de l'hôte, services système et sessions Linux. | Backend, routage, filtrage, DNS, permissions et TPM de l'hôte. |
| Machine physique Windows | Noyau Windows, services et sessions Windows. | Backend natif ou espace utilisateur, API réseau/filtrage/DNS, signatures et protections des clés. |
| VM Linux | Noyau et identités de l'invité, distincts de l'hyperviseur. | Réseau virtuel, redémarrage, snapshot, clonage et migration, avec preuves TPM selon le profil. |
| VM Windows | Noyau et identités de l'invité Windows. | Backend Windows et mêmes scénarios VM, sessions et service Windows qualifiés. |
| Docker sous Proxmox | Noyau du système qui héberge Docker et namespace du conteneur PA. | Placement dans VM ou LXC à préciser, comptes, capacités minimales, persistance et frontière des ressources réseau. |
| LXC sous Proxmox | Noyau Linux partagé avec l'hôte Proxmox et périmètre du conteneur. | Profil privilégié/non privilégié déclaré, disponibilité de WireGuard, restrictions et isolation. |

Docker dans une VM et Docker imbriqué dans LXC sont des topologies distinctes
à qualifier lorsqu'elles sont retenues ; aucune modification de l'hôte Proxmox
ni activation de nesting n'est autorisée par ce seul CdC. LXC sous Proxmox
vise des invités Linux, sans assimiler une VM Windows à un conteneur LXC.
Le besoin éventuel de conteneurs Windows Docker reste à préciser séparément.

Le TPM physique, le TPM transmis à un invité et le vTPM sont identifiés
distinctement. Une VM, un snapshot ou un clone ne crée pas une nouvelle
confiance automatique et ne duplique pas une identité ou clé admise. Migration,
restauration et changement d'hôte réévaluent les liaisons et l'attestation
requises. Un vTPM ne vaut pas implicitement attestation matérielle du PA.

Les versions d'OS, architectures CPU, bibliothèques système et environnements
graphiques supportés seront déclarés dans une matrice de qualification.
Un conteneur sans session graphique peut activer seulement les modes système.

**Adaptateurs proposés :** gestionnaire de services système, intégration au
bureau utilisateur et mécanisme de démarrage et d'arrêt du conteneur.
Systemd est un candidat pour Linux ; les services Windows et les événements
de session Windows disposent d'un adapter distinct à spécifier. Les modes
système/session restent les mêmes contrats, sans déduire leur implémentation
de l'OS. Les intégrations exactes ne sont pas arrêtées. Un démon peut fonctionner au premier plan sous son superviseur
tout en assurant le service en arrière-plan pour l'utilisateur.

### Profils de déploiement

Les profils de déploiement sont déclarés et qualifiés séparément :

| Profil | Cadre d'exploitation |
| --- | --- |
| PA seul sur un hôte ou dans un conteneur | Installation indépendante de PBO et PFO, avec relations distantes autorisées via PZT. |
| PBO et PA sur le même hôte | Comptes et frontières de privilèges explicites ; tous les échanges PBO–PA passent par PZT. |
| PBO et PA dans des conteneurs séparés | Réseaux, identités, persistance et permissions déclarés ; échanges via PZT. |
| PBO et PA dans un conteneur commun | Profil explicitement composé avec supervision, comptes, signaux et limites propres ; échanges via PZT. |

La première qualification couvre PA seul et le cohébergement sur un hôte.
Le conteneur commun ne résulte pas d'un lancement implicite de plusieurs rôles
PBO ; son support exige un profil et un adaptateur validés, cohérents avec
`BUILD.md`. Il ne modifie pas les contrats des rôles `web`, `worker` et
`scheduler` ni leurs frontières d'exposition.

Chaque profil précise ses modes actifs, superviseurs, comptes et privilèges,
signaux, budgets d'arrêt, persistance, réseaux, secrets, préconditions et
capacités désactivées. Un profil non qualifié n'est pas présenté comme supporté.

Le déploiement fournit le binaire, ses dépendances déclarées, les adaptateurs,
les schémas de configuration et les procédures d'exploitation. La construction
est reproductible et traçable à une version de source. Les outils de compilation
ne sont pas requis sur la cible d'exécution.

Les mises à niveau préservent les configurations administrées et les états
techniques nécessaires à une reprise validée. La provenance et l'intégrité
des artefacts sont vérifiées. Aucun téléchargement ou remplacement automatique
de logiciel n'est autorisé par ce seul cahier des charges.

### Compatibilité et qualification des artefacts

La matrice de compatibilité PBO–PA–PZT identifie les versions de composants,
de contrats, de configuration, d'événements, de politiques et d'états locaux
pertinentes. Elle distingue compatibilité, migration requise, dépréciation
et blocage. Un numéro plus récent ne constitue pas une preuve de compatibilité.
La coexistence et les chemins de mise à niveau sont déclarés et testés.

La qualification du binaire couvre l'interpréteur de construction, le runtime
embarqué, les dépendances directes et transitives, les bibliothèques natives,
leurs interfaces binaires et chaque cible OS/CPU déclarée. Elle respecte
la politique de dépendances Pixs sans imposer à PA des dépendances PBO inutiles.
Un changement de Python nécessaire reste soumis à la validation applicable.

Les distributions sont signées et identifiables par version et empreinte.
Elles disposent d'un inventaire des dépendances et d'un SBOM, d'une provenance
traçable et de contrôles de secrets et de vulnérabilités. L'installation et
la mise à niveau vérifient l'intégrité, la confiance, la révocation et les
préconditions avant activation. Un artefact altéré ou révoqué est refusé.

Les tests de contrat, d'exécution, de sécurité, de reprise et de packaging sont
distincts et complètent la comparaison Python/binaire compilé. Ils couvrent
les sept modes sur les cibles où ils sont déclarés disponibles, les profils
supportés et la préservation des états techniques lors d'une mise à niveau.
Les fixtures sont synthétiques et n'exigent aucun secret de production.

## Critères de recette proposés

Ces critères décrivent la future recette ; aucun test logiciel Pixs Agent
n'est déclaré exécuté par la rédaction de ce document. Les plateformes,
contrats et seuils nécessaires seront fixés avant la recette correspondante.

| Référence | Scénario | Résultat attendu |
| --- | --- | --- |
| R01 | Installation sans Pixs Frontoffice ni Pixs Backoffice | Le binaire fonctionne avec ses seules dépendances déclarées et joint une instance distante autorisée via PZT. |
| R02 | Démarrage du système ou du conteneur | `system-start` exécute les opérations déclarées et restitue leur résultat. |
| R03 | Arrêt contrôlé du système ou du conteneur | `system-stop` réalise ou interrompt explicitement les opérations dans le budget prévu. |
| R04 | Démarrage différé système | `system-daemon` respecte le délai, les préconditions et l'annulation en cas d'arrêt anticipé. |
| R05 | Ouverture de session graphique | `session-start` utilise l'identité et les droits de la session concernée. |
| R06 | Fermeture contrôlée de session graphique | `session-stop` produit un résultat borné et le démon concerné s'arrête. |
| R07 | Démarrage différé de session | `session-daemon` respecte le délai et ne survit pas à la fermeture de sa session. |
| R08 | Sessions concurrentes et déclenchements répétés | Les sessions restent isolées et les invocations répétées ne produisent pas de doublon incontrôlé. |
| R09 | Requête utilisateur exigeant des droits système | L'élévation implicite est refusée et diagnostiquée. |
| R10 | Agent dans un conteneur | Aucun accès à l'hôte n'est possible au-delà du périmètre explicitement accordé. |
| R11 | Identité, autorisation ou fraîcheur invalide | L'action concernée est refusée sans repli permissif. |
| R12 | Relations avec plusieurs instances Pixs | Les périmètres sont isolés et les instructions contradictoires sont bloquées selon la politique. |
| R13 | Coupure réseau, expiration ou révocation | Les opérations non autorisées cessent et seules les capacités locales explicitement éligibles restent possibles. |
| R14 | Rejeu, crash et redémarrage | La reprise respecte l'idempotence et distingue les effets dont le résultat est inconnu. |
| R15 | Dérive détectée | Un constat traçable est produit ; aucune correction non autorisée n'est engagée. |
| R16 | Configuration ou contrat incompatible | La capacité concernée reste inactive avec un diagnostic exploitable. |
| R17 | Binaire compilé sur une cible supportée | Les sept modes conservent leur comportement et les performances respectent les budgets validés. |
| R18 | Inspection des artefacts et diagnostics | Aucun secret ni donnée personnelle interdite n'est présent. |
| R19 | Arrêt forcé ou disparition brutale de session | L'agent ne prétend pas avoir exécuté un traitement de fermeture non observé. |
| R20 | Mise à niveau du composant | La configuration administrée et la reprise restent compatibles avec la procédure validée. |
| R21 | PBO et PA sur le même hôte ou dans le même conteneur | Tous leurs échanges, dans les deux sens, passent par PZT avec ses contrôles et son chiffrement. |
| R22 | Tentative de communication PBO–PA hors PZT | Le canal de contournement est refusé, même si les permissions locales permettraient son utilisation. |
| R23 | Canal PZT requis indisponible, non initialisé ou preuves invalides | La communication PBO–PA concernée est bloquée sans repli hors PZT, y compris pendant l'amorçage. |
| R24 | Premier démarrage sans PBO joignable | PA se limite aux capacités et opérations locales explicitement provisionnées, éligibles et encore autorisées. |
| R25 | Réseau distant indisponible et profil local PZT disponible | Le diagnostic et la reprise depuis PBO utilisent PZT avec les mêmes contrôles ; une décision en ligne indisponible bloque l'action qui l'exige. |
| R26 | PZT entièrement arrêté | Aucun échange PBO–PA n'est possible ; une éventuelle réparation système suit la procédure opérateur distincte et auditée. |
| R27 | Profil de pilotage PZT sans module officiel requis | La composition PBO est refusée ; une extension ne peut ni retirer le socle ni affaiblir ses contrôles. |
| R28 | Capacité incompatible ou ajout de code demandé par message | L'activation ou le chargement est refusé ; seules les opérations livrées par une composition vérifiée sont sélectionnables. |
| R29 | Mandat hors cible, périmètre, validité ou obligations | L'instruction est refusée au moment de l'exécution, même sur un canal PZT valide et après attente ou reprise. |
| R30 | Instance de session demandant un secret ou un droit système | L'accès est refusé ; les identités, clés et privilèges des fonctions séparées restent isolés. |
| R31 | Stockage technique plein, indisponible ou corrompu | Les opérations dont les garanties durables ne peuvent être tenues sont bloquées et l'écart est diagnostiqué sans perte silencieuse. |
| R32 | Crash après effet système mais avant enregistrement du résultat | L'état indéterminé conduit à une vérification de postcondition ou une intervention autorisée, sans réexécution aveugle. |
| R33 | Simulation ou plan expiré ou devenu obsolète | La simulation reste sans mutation ; l'application d'un plan invalide est refusée jusqu'à nouvelle validation. |
| R34 | Reconfiguration réseau interrompant le contrôle | L'échec est diagnostiqué et la compensation suit le plan préautorisé, sans réactiver un droit révoqué ni ouvrir un canal hors PZT. |
| R35 | Restauration d'un ancien état technique | Les droits révoqués et mandats expirés restent refusés et les préconditions sont réévaluées avant reprise. |
| R36 | Maintenance, surveillance seule ou quarantaine | Les actions interdites restent bloquées, le drainage est borné et la sortie contrôle les préconditions avant réactivation. |
| R37 | Action privilégiée soumise à une obligation d'audit | L'acteur, l'exécuteur, le mandat, la cible et le résultat sont corrélés ; une obligation non satisfaite empêche l'autorisation. |
| R38 | Changement de langue et appel non interactif | Les messages humains sont traduits tandis que codes de sortie, codes d'erreur et structures contractuelles restent stables. |
| R39 | Profil de déploiement qualifié | Les comptes, signaux, persistance, réseaux et limites correspondent au profil ; le conteneur commun ne lance pas implicitement plusieurs rôles PBO. |
| R40 | Versions PBO–PA–PZT incompatibles | La capacité est bloquée ou suit la migration déclarée, sans compatibilité déduite du seul numéro de version. |
| R41 | Binaire sur une cible OS/CPU déclarée | Le runtime embarqué et les bibliothèques natives sont qualifiés et les modes disponibles passent leurs tests applicables. |
| R42 | Artefact altéré ou révoqué | La vérification de signature, d'intégrité, de confiance et de provenance empêche son activation. |
| R43 | Arrêt contrôlé pendant une opération et livraison du résultat | Le séquencement conserve PZT dans le budget prévu et distingue exécution, résultat en attente et confirmation par PBO. |
| R44 | Configuration reçue, concurrente ou partiellement appliquée | L'état souhaité reste distinct de l'état appliqué ; les conflits et interruptions sont explicites et aucune réussite n'est déduite de la réception. |
| R45 | Référence temporelle d'autorisation non fiable | L'opération concernée est refusée ; les délais monotones ne servent pas de preuve de validité du mandat. |
| R46 | Démarrage du système ou du conteneur avec `pzt-daemon` | Le mode démarre sans délai et assure la convergence et la réconciliation de PZT lorsque celui-ci est activé et configuré sur ce PA ; sinon, il se ferme. |
| R47 | Backend WireGuard du profil retenu | PA pilote le backend qualifié, sans réimplémenter la cryptographie ; dépendances et privilèges correspondent au profil. |
| R48 | Carte ou delta altéré, périmé, hors destinataire, dupliqué ou de base incompatible ; séquence manquante et reprise | La configuration invalide est refusée ; un doublon ne produit aucun double effet et ne prolonge aucune permission. Une base incompatible, un trou ou un historique hors rétention déclenche un état complet vérifié. La réconciliation contrôle l'état effectivement appliqué et ne réintroduit aucun droit expiré ou retiré ; les objectifs A05b restent opposables. |
| R49 | AllowedIPs ou route présents sans permission du service | Les adapters nftables Linux et Windows Filtering Platform Windows appliquent les politiques PZT du profil et vérifient leur état ; les flux non autorisés sont bloqués, le tunnel ne donne pas accès aux services voisins et les ressources gérées restent distinctes des règles de l’opérateur. |
| R50 | PBO, sessions et modes ponctuels utilisant le même PA | Le propriétaire des ressources réseau évite les écritures concurrentes ; aucune session ne reçoit de clé ou privilège système. |
| R51 | Enrôlement automatisé et jeton expiré, révoqué ou au quota épuisé | Les nouvelles admissions sont refusées ; les secrets ne sont pas exposés et le retrait des pairs existants suit une opération distincte. |
| R52 | Fin de vie d'un pair éphémère et reprise après restauration | Accès, routes et noms sont retirés selon la politique ; les traces requises persistent et l'ancien pair n'est pas réactivé. |
| R53 | Connectivité directe, relayée et transports bloqués | Les chemins qualifiés respectent les permissions et le relais ne déchiffre pas les données WireGuard ; sans chemin admis, l'échec est explicite. |
| R54 | Changement d'endpoint ou de contexte réseau | L'identité demeure stable et les conditions de posture concernées sont réévaluées selon le profil. |
| R55 | Activation/désactivation IPv6 PZT, DNS administré et chevauchement d'adresses ou de routes | Le réglage unique retire les ressources IPv6 PZT, les AAAA propres à PZT et les échanges/endpoints IPv6 WireGuard/TLS concernés sans désactiver l'IPv6 hôte. Les sessions et états souhaité/appliqué sont vérifiés ; aucune réussite n'est annoncée sans preuve, aucun repli hors PZT ni droit périmé restauré. Les familles actives appliquent les garanties PZT ; les conflits bloquent le périmètre concerné sans écraser la configuration de l'hôte sans mandat. |
| R56 | DNS Pixs via module essentiel PBO : publication, consultation, panne et destination inattendue | Les contrats publics et droits distincts de publication/consultation sont vérifiés pour chaque contexte PA ; retraits et caches gérés respectent la validité, avec aucune fuite par repli public en panne. Dépendance essentielle, état appliqué et continuité sans PBO sont qualifiés selon le profil. Une résolution DNS seule n'accorde aucun accès ; une destination dont l'identité ou la clé diffère de celle attendue est refusée. |
| R57 | Posture modifiée en session et preuve TPM absente ou rejouée | Origine et fraîcheur sont vérifiées ; les accès concernés sont bloqués selon le profil, sans assimilation d'une déclaration à une attestation. |
| R58 | Crash ou blocage de PA avec tunnel et flux déjà actifs dans le noyau | La protection indépendante ferme les accès en 10 secondes maximum, détection et action comprises, sans prolonger une permission ni en créer ; une échéance antérieure reste prioritaire. Une révocation connue n'attend pas l'expiration et prend effet en 5 secondes maximum si PA est joignable sur le chemin de contrôle qualifié. La reprise vérifie l'état courant avant réactivation ; les objectifs A05b doivent être démontrés sur chaque profil. |
| R59 | Rotation d'une clé WireGuard | L'identité Pixs reste stable, la nouvelle liaison est vérifiée et l'ancienne liaison est retirée conformément à la politique. |
| R60 | Ressource sans PA derrière une passerelle déclarée | La permission ne donne pas accès aux services locaux de la passerelle ; le dernier segment respecte la protection du profil. |
| R61 | Basculement de passerelle avec ou sans NAT | Le profil qualifie les routes de retour, les effets sur les sessions et la traçabilité ; aucune continuité non démontrée n'est annoncée. |
| R62 | Démarrage à froid, admission, renouvellement et basculement sans accès à l'éditeur | Les services PZT exploités par l'opérateur suffisent lorsque les dépendances déclarées du profil sont disponibles. |
| R63 | TLS d'amorçage A02 et TLS mutuel local A03 validés | L'amorçage vérifie l'autorité à partir de l'ancrage préalable et refuse l'admission si les preuves requises sont invalides ; aucun accès métier avant admission. Le profil local sur le même hôte d'exécution vérifie les deux identités et les contrôles PZT ; identité, permission ou preuve requise invalides bloquent l'échange sans repli hors PZT. Endpoints, isolation et frontières des VM/conteneurs sont qualifiés par profil. |
| R64 | Propriété, réconciliation et retrait des ressources réseau | pzt-daemon gère les ressources PZT de son périmètre ; les six autres modes soumettent leurs demandes autorisées sans écritures directes, y compris après indisponibilité du propriétaire. PA ne retire que les ressources dont il possède la gestion ; une application partielle est rapportée sans fenêtre permissive. |
| R65 | Handshake récent et service indisponible | Le diagnostic distingue transport, joignabilité, readiness, autorisation et résultat métier. |
| R66 | PA Linux et Windows sur machines physiques et virtuelles | Chaque cible demandée dispose d'un backend, d'adapters système/session, de réseau, DNS et filtrage qualifiés ; aucune exclusion n'est déduite de l'environnement Debian du projet. |
| R67 | PA Docker et LXC sous Proxmox | Le profil vérifie le noyau effectif, le placement, les droits minimaux et l'isolation ; aucun repli en espace utilisateur ne suppose des privilèges absents. |
| R68 | Snapshot, clone, restauration ou migration d'une VM ou d'un conteneur | Les identités, liaisons de clés et preuves TPM/vTPM sont réévaluées ; aucun accès ni identité clonée n'est accepté implicitement. |

## Arbitrages nécessaires avant réalisation

Le registre canonique A01 à A12 figure dans
[les points à arbitrer du CdC PZT](ZERO_TRUST.md#points-restant-à-arbitrer).
Les décisions sont communes aux deux CdC et reportées dans chacun après
réponse explicite du développeur. WireGuard comme logiciel de base et le
développement propre à Pixs des capacités inspirées de NetBird sont validés.
A01 est validé le 5 octobre 2026 : priorité aux backends natifs par OS et
espace utilisateur pour les profils qui le nécessitent. Les versions,
dépendances et privilèges restent à qualifier. A02, option A, est validé le
5 octobre 2026 : TLS d'amorçage intégré à PZT, admission restreinte et ancrage
de confiance préalable. A03, option A, est validé le 5 octobre 2026 : TLS
mutuel intégré à PZT sur le même hôte d'exécution, avec maintien des contrôles
PZT et des frontières des VM et conteneurs. A04a, option A, est validé le
5 octobre 2026 : `pzt-daemon` gère les ressources réseau PZT de son périmètre,
les autres modes soumettent leurs demandes autorisées. A04b, option A,
est validé le 5 octobre 2026 : nftables sous Linux et Windows Filtering
Platform sous Windows, adapters PA et contrat commun. A05a, option A,
est validé le 5 octobre 2026 : autorisations bornées, révocation connue sans
attente d'expiration et protection indépendante de PA. A05b est validé
comme premier jet le 5 octobre 2026 ; les objectifs ci-dessous restent
à qualifier sur chaque profil. A06a, option A, est validé le 5 octobre
2026 : IPv4/IPv6 dès le socle, familles activées par profil et réglage unique
pour désactiver l'usage IPv6 de PZT sans modifier l'IPv6 de l'hôte. A06b,
option A, est validé le 5 octobre 2026 : plan privé configurable et allocations
par l'autorité compétente, avec contrôles de collisions. A06c, option B,
est validé le 5 octobre 2026 : DNS Pixs géré par un module essentiel PBO,
utilisable par PZT et tous les PA selon leurs permissions. Placement,
suffixes, TTL et bibliothèques restent ouverts. A07a, option A, est validé
le 5 octobre 2026 : contrôle HTTP/JSON avec contrats OpenAPI versionnés
pour PBO–PA et PA–PA. A07b, option A, est validé le 5 octobre 2026 :
snapshot initial, deltas ordonnés et reprise complète en cas de
désynchronisation. A07c, option B, est validé le 5 octobre
2026 : notifications et retours de suivi WebSocket/JSON, API HTTP conservées.
A07d option A est validée le 5 octobre 2026 pour les deltas JSON typés.
Les autres choix sont présentés pour la suite du débat.

| Référence | Choix technique ou décision | Conséquence propre au PA | État |
| --- | --- | --- | --- |
| A01 | Priorité au noyau Linux et au backend natif Windows, dont WireGuardNT reste le candidat à qualifier ; espace utilisateur pour les profils qui le nécessitent. | Matrice physique/VM Linux et Windows, Docker/LXC Proxmox ; qualification distincte des versions, dépendances, droits et isolation, sans contournement des restrictions des conteneurs. | Validé le 5 octobre 2026. |
| A02 | Canal TLS d'amorçage authentifié intégré à PZT, limité à l'admission, aux preuves requises et aux paramètres publics WireGuard. | Ancrage de confiance préalable, vérification des preuves avant admission et accès courant sur WireGuard ; formats, versions, bibliothèques et provisionnement à spécifier. | Option A validée le 5 octobre 2026. |
| A03 | TLS mutuel local intégré à PZT pour PBO et PA sur le même hôte d'exécution. | Contrôles PZT maintenus ; VM/conteneurs distincts conservent leurs frontières réseau. Endpoints et isolation à qualifier selon le profil. | Option A validée le 5 octobre 2026. |
| A04 | A04a : gestion permanente par pzt-daemon. A04b : adapters nftables Linux et Windows Filtering Platform Windows avec contrat commun. | Un propriétaire par périmètre PZT ; les six autres modes soumettent leurs demandes autorisées sans écritures directes. Ressources PZT distinctes des règles de l'opérateur ; interfaces, dépendances, privilèges, coexistence et isolation à qualifier. | A04a et A04b option A validées le 5 octobre 2026. |
| A05 | Modèle hybride, autorisations de durée bornée et protection indépendante de PA ; objectifs initiaux par sensibilité détaillés ci-dessous. | Expiration après crash, révocation connue sans attente d'expiration et contrôle en ligne selon la classe ; protection limitée aux retraits et fermetures préautorisés. Réalisation et objectifs A05b à qualifier. | A05a option A et A05b premier jet validés le 5 octobre 2026. |
| A06 | A06a : IPv4/IPv6 dès le socle et réglage unique de désactivation IPv6 PZT. A06b : plan privé configurable et allocations par l'autorité compétente. A06c : DNS Pixs développé et géré par un module essentiel PBO. | Tous les PA admis peuvent consommer le DNS via PZT selon leur contexte ; droits de consultation et publication distincts. Adapters par profil, aucun repli public des noms privés, retraits et caches contrôlés. Pools IPv4 RFC 1918, IPv6 ULA /48 et conflits bloquants maintenus ; placement, interfaces, suffixes, TTL et bibliothèques à définir et qualifier. | A06a/A06b option A et A06c option B validées le 5 octobre 2026. |
| A07 | A07a : contrôle HTTP/JSON avec OpenAPI. A07b : snapshot initial et deltas ordonnés avec reprise complète. A07c : WebSocket/JSON de référence, support SSE complémentaire et adaptation déterministe validés en principe ; commandes et lectures restent HTTP. A07c2 : table de règles prioritaires et seuils explicites pour sélectionner le mode, valeurs à calibrer. A07d : opérations métier JSON typées avec schémas versionnés retenues. | Contrats versionnés, validation et déduplication ; reprise sans prolongation des permissions, curseurs distincts des preuves d'application, clients, ressources et délais A05b à qualifier. Décision A07c2 option A validée le 5 octobre 2026 : règles prioritaires, seuils de bascule/retour distincts et stabilité, aucun contournement de sécurité ; valeurs et consommation à qualifier. Décision A07d option A validée le 5 octobre 2026 : opérations métier JSON typées, validation sémantique et audit. | A07a/A07b option A et A07c option B validées le 5 octobre 2026, extension adaptative validée en principe ; A07c2 option A validée le 5 octobre 2026 ; A07d option A validée le 5 octobre 2026. |
| A08 | A08a : socle initial entre PA admis avec contrôle PBO, puis profil passerelle ultérieur. A08b : sources conservées et routes retour ; ou traduction source déclarée. A08c : sélection et basculement. | Contrats du rôle passerelle conservés, livraison après qualification du socle. Recommandation A08b : conserver les sources lorsque les routes retour sont maîtrisées ; traductions alternatives, corrélation, ressources et effets sur les sessions à qualifier. Aucun NAT IPv6 ou privilège choisi implicitement. | A08a option A validée le 5 octobre 2026 ; A08b soumis ; A08c à débattre. |
| A09 | ICE/STUN et rendez-vous ; relais UDP et éventuelle encapsulation TCP/WebSocket. | Connectivité, coûts, bibliothèques indépendantes et qualification du backend. | À débattre. |
| A10 | Isolation des services, liaisons de clés, formats de certificat et déclencheurs TPM. | Protection des clés, points de contrôle et attestation des connexions logiques. | À débattre. |
| A11 | Admission opérateur ou mandat préalable, jetons bornés et délais des pairs éphémères. | Provisionnement et retrait traçables, reprise et absence de résurrection. | À débattre. |
| A12 | État autoritatif, consensus, sources de vérité et signataires des autorités. | Services exécutés selon le rôle attribué et refus des décisions périmées. | À débattre. |

### A05b — Objectifs initiaux validés, qualification requise

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026, commun
avec le CdC PZT. Ces objectifs doivent être mesurés sur chaque profil Linux,
Windows, VM, Docker et LXC ; aucune performance n'est présumée démontrée.
Ils sont des paramètres documentés par profil dans les limites retenues ;
leur modification nécessite une décision explicite. L'affectation détaillée
des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

PA ne prolonge aucune échéance en rejouant une preuve et n'ajoute aucune
période de grâce. Pause, reprise, snapshot et restauration doivent empêcher
la réactivation d'un accès périmé avant toute reprise des échanges. La confiance
temporelle reste requise ; un profil sans preuve des délais retenus n'est pas
déclaré conforme. Leur modification exige une décision explicite documentée.

### A06b — Plan privé et allocation validés, qualification requise

L'option A, validée par le développeur le 5 octobre 2026 dans les deux CdC,
prévoit des pools IPv4
[RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) choisis et validés par
l'opérateur, et un préfixe IPv6 ULA /48 par domaine généré selon
[RFC 4193](https://www.rfc-editor.org/rfc/rfc4193) ou fourni. L'autorité
compétente alloue les adresses dans ce plan ; PA applique seulement les
allocations autorisées et vérifie les conflits avec les réseaux connus de
son profil et des domaines interconnectés. Une génération ULA ne dispense
pas de ces vérifications. Lorsque IPv6 est désactivé pour ce PZT, aucune
allocation IPv6 n'est activée sur PA. Un conflit bloque le périmètre concerné sans
renumérotation, NAT ou modification implicite de l'hôte. La persistance,
les délégations, tailles et découpages restent à préciser, avec A12 pour
la cohérence autoritative.

Le provisionnement manuel de chaque adresse n'est pas retenu comme mode
de référence. Les pools concrets, la réalisation et les contrôles de conflits
restent à qualifier ; le réglage IPv6 A06a demeure applicable.

### A06c — DNS Pixs géré par un module essentiel PBO, option B validée

L'option B est validée par le développeur le 5 octobre 2026 : un DNS géré
sera développé pour Pixs dans un module essentiel du PBO et utilisé par
PZT et tous les PA. PBO administre ses zones, vues, enregistrements et règles
par les contrats publics du module DNS. Le module PZT utilise ces contrats
pour publier ou retirer ses noms ; il n'accède pas aux données privées du
module DNS. Les dépendances essentielles et leur effet sur l'activation et
la readiness sont déclarés pour les profils consommateurs. L'identifiant
du module, les PA chargés d'exécuter le service DNS, son placement et sa
redondance restent à spécifier ; le Kernel reste générique.

Chaque PA admis peut consommer le DNS dans son contexte autorisé via PZT.
Les droits de consultation sont distincts des droits de publication et
d'administration. Le rôle client ne confère ni un rôle serveur ni une
visibilité sur tous les autres pairs. PA applique les configurations et
retraits autorisés de son périmètre et rapporte l'état réellement appliqué,
les erreurs et les applications partielles. Une résolution ne vaut jamais
autorisation de communication ; l'identité et la clé de destination restent
vérifiées indépendamment.

Des adapters dirigent les requêtes des zones PZT vers le service DNS Pixs ;
les autres noms conservent le DNS habituel sauf configuration explicite.
Un résolveur autonome développé dans chaque PA n'est pas retenu comme
mécanisme de référence. Les mécanismes Linux, Windows, Docker et LXC,
permissions et frontières d'écoute sont qualifiés séparément : domaines
de routage systemd-resolved et règles NRPT restent des candidats, et les
profils Docker distinguent DNS hérité et DNS embarqué. Aucun service système,
montage ou droit du conteneur n'est modifié implicitement.

Une panne DNS ou une preuve requise non vérifiable n'entraîne aucun repli
des noms privés vers un DNS public. Les caches gérés respectent leur validité ;
retraits, révocations et désactivation IPv6 invalident les enregistrements et
caches PZT concernés, dont les AAAA propres à PZT. Les caches des applications
ne prolongent aucun accès réseau. Une panne du PBO ne permet aucune nouvelle
publication ou prolongation ; une continuité sur le dernier état vérifié du
service reste limitée par le contrat et à qualifier. L'amorçage utilise les
références d'endpoints et ancrages provisionnés sans attendre un DNS privé
encore inaccessible. Suffixes, TTL, protocoles DNS, bibliothèques, persistance,
réplication et comportement des applications avec résolveur propre restent
à préciser ; l'absence de fuite doit être démontrée.

### A07a — Contrats HTTP/JSON, option A validée

L'option A est validée par le développeur le 5 octobre 2026 : HTTP avec
messages JSON et contrats OpenAPI versionnés pour les échanges de contrôle
PBO–PA et PA–PA, avec contrats distincts selon les rôles et propriétaires.
Elle prolonge le choix HTTP/REST OpenAPI des API de gestion PBO. PA valide
les messages à l'exécution, les versions compatibles, l'identité, le contexte,
les mandats, leur fraîcheur et les permissions avant application. Erreurs
stables, corrélation et idempotence des commandes rejouables font partie du
contrat. Le RPC binaire n'est pas retenu comme mécanisme de référence.
La qualification couvre la chaîne Python/C et chaque plateforme ; aucune
performance n'est présumée et aucune bibliothèque n'est sélectionnée.

Les transports PZT A02/A03 et WireGuard interhôtes restent applicables.
HTTP ne remplace aucun contrôle d'autorisation. La validation ne choisit
ni version HTTP/OpenAPI ni format de certificat. A07b, option A validée
le 5 octobre 2026, fixe le snapshot initial, les deltas ordonnés et la reprise
complète. A07c, option B validée le 5 octobre 2026, retient WebSocket/JSON
pour les notifications et retours de suivi, avec les API HTTP conservées.

### A07b — Snapshot et deltas ordonnés, option A validée

Un snapshot de contrôle est un état autorisé complet pour ce PA et son
contexte, distinct d'un snapshot de virtualisation. L'option A est validée
par le développeur le 5 octobre 2026. Le mécanisme retenu combine snapshot
initial, notifications de changement et deltas ordonnés,
avec révision de base et de résultat. PA vérifie l'identifiant du message,
l'autorité productrice, le destinataire, le périmètre, la version de contrat,
la validité et les preuves requises. L'ordre est limité au périmètre autoritatif
ou à la partition déclarée ; le choix multimaître A12 reste ouvert. Les
notifications annoncent des changements engagés ; doublons et replays sont
traités sans double effet ni prolongation de permission.

Une base inconnue, une séquence manquante, une contradiction, une version
incompatible ou un historique trop ancien appelle un état complet vérifié.
La reprise réconcilie l'état réseau effectivement appliqué et refuse les
états périmés. Les retraits vérifiés sont prioritaires et ne peuvent être
annulés par une révision antérieure. Les changements de visibilité retirent
les données et accès devenus interdits. La réception et l'application restent
deux états distincts ; les échecs partiels ne sont pas annoncés comme réussis
et n'ouvrent aucune fenêtre permissive.

Pendant une désynchronisation, PA n'applique aucune nouvelle permission non
vérifiable. Le maintien des permissions existantes suit strictement A05,
sans prolongation hors ligne et avec décision en ligne pour les cas critiques.
La récupération n'ajoute aucune grâce aux délais A05b ; ceux-ci sont qualifiés
de bout en bout sur Linux/Windows physiques et VM, Docker/LXC Proxmox,
y compris après interruption ou restauration.

Ce choix vise à limiter les états complets retransmis lors
de changements fréquents, avec une reprise explicite ; il exige la gestion
des révisions, doublons et trous de séquence. A07d, option A validée le
5 octobre 2026, retient les opérations métier JSON typées ; schémas, catalogue
et versions restent à préciser, sans supprimer les preuves requises.
La distribution de seuls états complets à chaque changement n'est pas
retenue comme mécanisme de référence. HTTP/JSON A07a reste applicable ;
A07c, option B validée le 5 octobre 2026, retient WebSocket pour les
notifications et retours de suivi. A07d option A est validée pour les deltas ;
fréquences, limites, rétention et pagination restent à définir et qualifier.

### A07c — Notifications WebSocket, option B validée

L'option B est validée par le développeur le 5 octobre 2026 : PA ouvre un
canal WebSocket vers un producteur PZT autorisé, avec messages JSON versionnés
pour les notifications et retours de suivi déclarés. Les rôles PA–PA restent
explicites. Commandes, rapports hors suivi et lectures de snapshots ou deltas
conservent HTTP/JSON A07a. Réception, vérification et application sont des
états distincts, avec types de retour et corrélation ; aucun abonnement
n'ajoute un droit ou une visibilité. WebSocket demeure la référence ; le
principe du support SSE complémentaire avec adaptation déterministe est
ensuite validé, avec règles A07c2 option A validées le 5 octobre 2026.

Le contrat précise versions, identifiants, périmètres, curseurs de reprise
et limites. PA conserve la déduplication et les contrôles A07b ; WebSocket
ne prouve ni persistance ni livraison sans perte. Un curseur inconnu,
incompatible ou hors rétention déclenche l'état complet vérifié. Les messages
invalides, hors contexte ou expirés sont refusés ; les états réellement
appliqués sont rapportés séparément des messages reçus.

Connexion, reconnexion et maintien du canal contrôlent identité, contexte,
permissions et fraîcheur selon les transports PZT A02/A03. La perte de droit
ferme l'accès concerné dans les délais A05. Heartbeats et curseurs ne
prolongent aucune permission ; aucun secret n'est placé dans l'URL.
Une vérification périodique bornée de la révision autoritative détecte les
notifications perdues. Retraits vérifiés, files saturées, clients lents et
reprise sont qualifiés avec les délais A05b ; les erreurs sont explicites
et aucun repli hors PZT n'est admis. Fréquences, tailles, files, reconnexion
et fermeture restent à préciser.

L'économie des échanges de suivi fréquents motive le choix ; aucun gain
n'est déclaré mesuré. La qualification compare PA et PBO à charge identique
avec une référence SSE/HTTP, en incluant les API HTTP conservées : CPU, mémoire,
connexions, files, trafic et latence d'application, au repos et en charge,
y compris rafales, coupure et reprise. Le client natif Python/C et le service
PBO asynchrone sont qualifiés sur Linux/Windows physiques et VM, Docker/LXC
Proxmox ; aucune bibliothèque ou dépendance n'est sélectionnée. A07d option A est validée le 5 octobre 2026 pour les deltas JSON typés.

### A07c2 — Table de règles déterministes, option A validée

Le développeur a approuvé le 5 octobre 2026 le principe de prise en charge
SSE et WebSocket avec adaptation déterministe. WebSocket demeure la référence
A07c validée ; SSE est une capacité complémentaire à qualifier avec les mêmes
contrats JSON, identités, permissions, validités et garanties A07b. En SSE,
les retours de suivi utilisent HTTP/JSON ; en WebSocket, ils peuvent utiliser
le canal bidirectionnel. Les commandes et lectures restent HTTP.

PA applique une politique administrée, versionnée et auditée : modes permis,
mode imposé éventuel, critères, priorité et périmètre de délégation. Il ne
choisit localement un mode que si cette adaptation est explicitement déléguée.
La décision est reproductible à partir de la politique, des mesures, de leur
fenêtre et de l'état précédent. Un changement de mode ne confère aucun droit.

L'option A est validée par le développeur le 5 octobre 2026 : une table
de règles prioritaires avec seuils explicites, calibrés pour PA et PBO.
L'ordre retenu est : mode imposé ; capacités, contexte et sécurité ;
échec vérifié du seul transport courant ; profil de coût selon fréquence,
volume, CPU, mémoire, concurrence et trafic ; seuils de bascule/retour et
durée de stabilité distincts. Les modes non autorisés ou non qualifiés sont
exclus. Un refus d'identité ou d'autorisation ne déclenche aucun repli.
Sans mesures de coût suffisamment fraîches, PA conserve le mode courant
admis ou utilise WebSocket à l'initialisation, sans prolonger de permission.
Une activité faible ou forte ne démontre pas à elle seule le mode le moins
coûteux. Seuils, fenêtres, budgets et fraîcheur restent à définir et qualifier.
La décision reste lisible et reproductible ; aucun gain n'est déclaré mesuré.

Le score pondéré, option B, n'est pas retenu comme mécanisme de référence.
Les profils de coût et valeurs restent à calibrer avant qualification.

PA maintient un seul canal en régime établi ; une courte coexistence de
transition est bornée et dédupliquée. La bascule conserve identifiants et
révisions, distingue reçu/vérifié/appliqué, revalide le nouveau canal et
reprend par état complet si nécessaire. La temporisation d'optimisation
ne retarde aucun retrait ou fermeture de sécurité. Les coûts du mode inactif
proviennent du profil qualifié, sans deux canaux permanents de mesure.
Bascule, reprise, charge et défaillance sont qualifiées avec A05b sur chaque
plateforme ; aucun repli hors PZT ou renouvellement implicite n'est admis.
Le support adaptatif et la table de règles A07c2 sont validés ; les valeurs
des seuils, budgets, fenêtres, limites de transition et bibliothèques
restent à définir et qualifier.

### A07d — Deltas par opérations métier JSON typées, option A validée

L'option A est validée par le développeur le 5 octobre 2026 : les changements
sont représentés par opérations métier JSON typées et schémas versionnés :
retirer un pair ou mettre à jour une route, par exemple. PA identifie l'objet
par identité stable et contexte, valide
l'opération, ses préconditions et ses données, et déduplique son identifiant.
L'enveloppe A07b conserve les preuves d'autorité, le destinataire, les révisions
et la validité. Une opération traduit un état engagé ; elle n'autorise
aucune commande hôte arbitraire ou décision autonome de PA. Le catalogue
et les schémas précis restent à définir. La validation sémantique et l'audit
restent explicites, sans gain de ressources présumé.

JSON Patch, option B, n'est pas retenu comme format de référence des deltas.
Le catalogue, les schémas et leurs versions restent à spécifier avant réalisation.

Un changement invalide, inconnu ou incompatible est
refusé avec diagnostic et appelle un état complet compatible. Sans contrat
compatible, le périmètre reste bloqué selon A05. Validation de la configuration
et application réseau restent distinctes ; les effets partiels sont rapportés,
les retraits restent prioritaires et aucune réconciliation ne restaure un
droit expiré ou révoqué. Les deltas restent récupérés par HTTP/JSON A07a ;
le mode A07c/A07c2 conserve les notifications et leurs retours déclarés.
Catalogue, tailles, budgets, transactions et bibliothèques restent à définir
et qualifier.
Ces modalités restent à qualifier ; A08a, option A validée le 5 octobre
2026, réserve le rôle passerelle à un profil ultérieur après le socle initial.

### A08a — Socle initial puis profil passerelle ultérieur, option A validée

Un PA peut porter un rôle passerelle déclaré pour transférer des flux
PZT autorisés vers une destination sans PA. L'accès à cette destination
reste distinct de l'accès aux services locaux de la passerelle. Ce rôle
n'ajoute aucun mode aux sept modes existants ; la propriété des ressources
A04a reste applicable.

L'option A est validée par le développeur le 5 octobre 2026 : le socle
qualifie d'abord les communications entre PA admis avec le contrôle PBO
déjà prévu ; le rôle passerelle devient exécutable dans un profil ultérieur
explicitement qualifié. Ses contrats et garanties restent au cahier des charges, avec une
décision de livraison distincte. Le premier socle ne déclare pas accessibles
via PZT les ressources sans PA. Le socle est qualifié avant les contraintes
de transit et du dernier segment.

Le profil passerelle dès la première réalisation, option B, n'est pas
retenu ; ses exigences sont conservées pour le profil ultérieur.

PA vérifie les ressources, ports, protocoles et sens d'initiation autorisés,
la protection du dernier segment et l'état effectivement appliqué. Le tunnel
WireGuard ne chiffre pas à lui seul le trajet au-delà de la passerelle ;
l'attestation du PA ne vaut pas attestation de la destination sans PA.
Les preuves du profil restent requises, sinon l'accès est bloqué. Expiration,
révocation et reprise A05, collisions et réglage IPv6 A06 restent applicables.
Chaque cible PA demandée conserve son support ; le rôle passerelle est
qualifié séparément par profil. Aucun privilège, montage, forwarding hôte
ou droit Proxmox n'est accordé implicitement. NAT et retours sont débattus
en A08b, basculement en A08c ; A08a ne choisit ni plateforme passerelle
initiale ni dépendance. Ces modalités restent à définir et qualifier.

### A08b — Proposition d'adressage source et de routes retour, non validée

Ce choix concerne les flux du profil passerelle ultérieur A08a. Le premier
socle conserve les communications entre PA admis et le contrôle PBO ; il
ne devient pas une passerelle du fait de cet arbitrage.

L'option A proposée préserve l'adresse source overlay sans NAT vers la
ressource. PA vérifie les chemins et les routes de retour des préfixes PZT
permis via la passerelle compétente, avant exposition. L'adresse reste
visible pour la corrélation côté destination ; elle ne vaut ni preuve d'identité
ni permission. Une route absente ou non vérifiable bloque la ressource et
produit un diagnostic, sans traduction automatique. Cette option est
recommandée si l'opérateur maîtrise les routes retour.

L'option B utilise une traduction source explicitement déclarée vers une
adresse de la passerelle joignable depuis la destination. Le retour doit
être valide vers cette adresse ; une route spécifique vers l'overlay peut
alors être évitée. Les journaux de destination voient l'adresse traduite ;
PZT corrèle l'identité et le contexte d'origine avec le flux et la traduction,
selon les accès, rétention et minimisation déclarés. États, quotas, expiration,
panne et effets sur les sessions nécessitent une qualification. Cette option
convient quand les routes de retour PZT ne peuvent pas être établies.

Dans les deux options, PA applique un plan autorisé, versionné par ressource,
sur les seules ressources de son périmètre, et rapporte la convergence et
les erreurs. Changer de mode ne renouvelle aucune permission ; les sessions
existantes sont qualifiées. Transit et services locaux restent distincts.
Collisions, boucles, asymétries, anti-usurpation et filtrage des retours sont
contrôlés. IPv6 demeure désactivable selon A06a ; aucun NAT IPv6, traduction
entre familles ou routage Internet n'est introduit implicitement.

Le basculement A08c doit préserver la cohérence des chemins retour et états
éventuellement traduits, sans continuité de session présumée. CPU, mémoire,
tables de suivi, trafic et délais restent à mesurer sur les profils concernés.
Les interfaces NAT/routage et leurs privilèges sont qualifiés séparément sur
Linux/Windows physiques et VM, Docker/LXC Proxmox ; le choix des adapters de
filtrage A04b ne sélectionne pas implicitement toute la réalisation NAT.
Les sources officielles figurent dans le CdC PZT. Aucune option A08b n'est adoptée.

### Autres modalités de réalisation

Les autres modalités de réalisation sont maintenues ci-dessous. Les nouvelles
capacités ne choisissent pas implicitement une bibliothèque, un droit de
conteneur, une durée ou une plateforme supplémentaire.

| Sujet | Décision à prendre |
| --- | --- |
| Catalogue initial | Opérations effectivement livrées dans chaque mode et périmètres concernés. |
| Compilation | Outil, version, runtime embarqué, format mono-fichier ou distribution avec dépendances et qualification Python. |
| Support | Versions d'OS, architectures, types de conteneur et bureaux graphiques. |
| Privilèges | Comptes, capacités système et mise en œuvre des frontières entre communication, surveillance et exécution privilégiée. |
| Lifecycle | Adaptateurs, déclencheurs, délais, séquencement et politique de redémarrage. |
| Multi-instance | Autorité par ressource, délégations, concurrence et résolution des conflits. |
| Réseau | Transports PZT distants et locaux, enrôlement, justificatifs, fraîcheur et propagation des révocations. |
| Amorçage PZT | Procédure de provisionnement, preuves, références de secrets et ordre d'initialisation sans communication PBO–PA hors PZT. |
| Pilotage PBO | Identifiants des composants, contrats avec le module officiel PZT, sous-modules et contributions PFO. |
| API agent | Formats des instructions, mandats, plans, résultats, états et garanties de compatibilité. |
| Persistance PA | Provider, schéma et garanties des états techniques locaux, limites, rétention, restauration et comportement après corruption. |
| Reprise PZT | Adaptateur du profil local PZT, protections, opérations de réparation et procédure opérateur si PZT est entièrement indisponible. |
| Hors ligne | Opérations éligibles, durées de validité, stockage technique et politique de reprise. |
| Dérives | Référentiels attendus, fréquences de mesure et conditions de correction. |
| Plans et compensation | Validation, confirmation, obsolescence, limites de correction et compensation préautorisée après perte de contrôle réseau. |
| Exploitation | Portées de maintenance et de quarantaine, conditions de sortie, audit, sondes et codes stables. |
| Internationalisation | Catalogues, locales supportées et résolution de la langue des messages humains. |
| Performance | Budgets CPU, mémoire, lancement, arrêt, débit et références de comparaison. |
| Distribution | Profils qualifiés, artefacts, signatures, provenance, SBOM, installation, mise à niveau et désinstallation. |

## Historique du document

| Version | Date | Évolution |
| --- | --- | --- |
| 0.0.1 | 4 octobre 2026 | Première rédaction de Pixs Agent et des six modes d'exécution. |
| 0.0.2 | 4 octobre 2026 | Dénominations PA, PBO et PFO et rôle d'appui de PA. |
| 0.0.3 | 4 octobre 2026 | Passage obligatoire par PZT de toute communication PBO–PA, y compris locale. |
| 0.0.4 | 4 octobre 2026 | Intégration des principes de provisionnement, reprise PZT, pilotage modulaire, composition, mandats, séparation des privilèges, persistance, plans, preuves d'exécution, profils et qualification ; cohérence avec le CdC PZT v0.2.0. |
| 0.0.5 | 4 octobre 2026 | Ajout du septième mode `pzt-daemon`, lancé sans délai au démarrage du système ou du conteneur pour assurer la convergence et la réconciliation de PZT si celui-ci est activé et configuré sur ce PA, sinon fermeture ; mise en cohérence des modes, privilèges et critères de recette. |
| 0.0.6 | 5 octobre 2026 | Intégration demandée de WireGuard et des capacités inspirées de NetBird à redévelopper dans PZT/PA : adapters, cartes réseau, politiques, DNS, posture, admission, connectivité, révocation et passerelles selon profil ; critères R47–R68 et arbitrages A01–A12. Périmètre précisé : Linux/Windows physiques et VM, Docker/LXC sous Proxmox ; A01 validé : priorité aux backends natifs par OS, espace utilisateur selon les besoins du profil. A02 option A validée : TLS d'amorçage intégré à PZT, limité à l'admission et aux preuves requises, avec ancrage de confiance préalable. A03 option A validée : TLS mutuel PZT sur le même hôte d'exécution, frontières des VM et conteneurs préservées. A04a option A validée : pzt-daemon gère les ressources réseau PZT de son périmètre, les autres modes soumettent leurs demandes autorisées. A04b option A validée : adapters PA nftables Linux et Windows Filtering Platform Windows, contrat commun et coexistence avec les règles de l'opérateur à qualifier. A05a option A validée : autorisations bornées, révocation connue sans attente d'expiration et protection indépendante de PA ; A05b premier jet validé : Courant 5 minutes/renouvellement 60 secondes, Protégé 60 secondes/renouvellement 20 secondes, Critique en ligne, révocation PA joignable en 5 secondes et protection après panne en 10 secondes ; objectifs à qualifier. A06a option A validée : IPv4/IPv6 dès le socle, familles activées par profil et désactivation IPv6 PZT par réglage unique, couvrant overlay et endpoints WireGuard/TLS sans modification implicite de l'IPv6 hôte ; A06b option A validée : plan privé configurable, allocations par autorité compétente, pools IPv4 RFC 1918 validés, IPv6 ULA /48 par domaine et contrôles de collisions ; A06c option B validée : DNS Pixs géré par un module essentiel PBO et utilisable par PZT et tous les PA, droits de publication/consultation et contrats publics distincts ; placement, interfaces et TTL à préciser. A07a option A validée : contrôle PBO–PA et PA–PA HTTP/JSON avec contrats OpenAPI versionnés ; A07b option A validée : snapshot initial et deltas ordonnés, déduplication et reprise complète en cas de désynchronisation, sans prolongation ni résurrection des droits ; A07c option B validée : notifications et retours de suivi WebSocket/JSON, commandes et lectures HTTP conservées ; consommation comparative PA/PBO et délais à qualifier. Extension A07c approuvée en principe : SSE et WebSocket avec adaptation déterministe ; A07c2 option A validée le 5 octobre 2026 : table de règles prioritaires, critères déterministes et seuils explicites ; valeurs, fenêtres, bascule et consommation à qualifier. A07d option A validée le 5 octobre 2026 : opérations métier JSON typées, identité stable, préconditions, versions, déduplication et preuves maintenues ; catalogue et schémas à préciser. A08a option A validée le 5 octobre 2026 : socle initial entre PA admis avec contrôle PBO, puis profil passerelle ultérieur, contrats et garanties conservés. A08b sources conservées ou traduction source soumis ; basculement A08c restant à débattre. Alignement sur ZTP v0.3.0 ; autres recommandations ouvertes, sans implémentation ni écriture OpenSpec. |

## Documents de référence et suite du cadrage

Les documents du projet consultés pour cette rédaction sont [AGENTS.md](AGENTS.md),
[PROJECT.md](PROJECT.md), [TECHNICAL.md](TECHNICAL.md), [BUILD.md](BUILD.md),
[DEVOPS.md](DEVOPS.md), [ZERO_TRUST.md](ZERO_TRUST.md) et [pyproject.toml](pyproject.toml).

L'intégration réseau se réfère au [CdC ZTP v0.3.0](ZERO_TRUST.md), à sa matrice
de documentation NetBird officielle consultée le 5 octobre 2026 et au
[logiciel WireGuard](https://www.wireguard.com/). Les références documentaires
servent à spécifier les capacités développées dans Pixs ; aucune brique
NetBird ni compatibilité avec son agent n'est introduite.

La préparation des profils s'appuie également sur
[WireGuardNT](https://git.zx2c4.com/wireguard-nt/about/), la
[bibliothèque de tunnel Windows](https://git.zx2c4.com/wireguard-windows/about/embeddable-dll-service/README.md),
[Windows Filtering Platform](https://learn.microsoft.com/en-us/windows/win32/fwp/windows-filtering-platform-start-page)
et la [documentation des conteneurs Proxmox](https://github.com/proxmox/pve-docs/blob/master/pct.adoc).
Ces références identifient des mécanismes candidats ; les versions et modes
d'intégration restent soumis aux arbitrages et à qualification.

Les capacités OpenSpec examinées sont [runtime](openspec/specs/runtime/spec.md),
[security](openspec/specs/security/spec.md), [api](openspec/specs/api/spec.md),
[authorization](openspec/specs/authorization/spec.md),
[configuration](openspec/specs/configuration/spec.md),
[observability](openspec/specs/observability/spec.md),
[offline-first](openspec/specs/offline-first/spec.md) et
[performance](openspec/specs/performance/spec.md).

Les garanties de la présente révision s'articulent également avec
[reference-runtime](openspec/specs/reference-runtime/spec.md),
[operations](openspec/specs/operations/spec.md),
[installation-provisioning](openspec/specs/installation-provisioning/spec.md)
et [secrets-providers](openspec/specs/secrets-providers/spec.md).

Les exigences propres à Pixs Agent restent à traduire dans une évolution
OpenSpec explicitement autorisée. Cette étape devra traiter les frontières
avec les profils `web`, `worker` et `scheduler`, ainsi que les états techniques
locaux éventuellement nécessaires à l'agent, sans affaiblir les garanties
existantes. Le présent document n'ajoute pas implicitement un profil au
runtime Pixs Backoffice.

La suite est la définition des modalités techniques encore ouvertes et du
catalogue initial, puis la préparation OpenSpec explicitement autorisée avant
toute implémentation. Les principes validés de ce CdC et les responsabilités
du CdC PZT sont conservés ; aucun choix technique ne peut créer un canal
PBO–PA hors PZT. Cette révision ne modifie ni le code existant ni les
spécifications OpenSpec du projet.
