# Zéro Trust Pixs (ZTP)

- Version : 0.3.0
- Date : 5 octobre 2026
- Statut : cahier des charges de conception avec points techniques à arbitrer

Ce document décrit Zéro Trust Pixs (ZTP), le réseau propre à Pixs destiné à
relier des instances selon une chaîne d'autorité verticale et des relations
de coopération horizontales. ZTP est exécuté par le Pixs Agent (PA), contrôlé
et configuré par le Pixs Backoffice (PBO). Le document rassemble les orientations
validées pendant la réflexion et identifie les mécanismes qui restent à arbitrer.

La version 0.3.0 intègre le choix explicite de WireGuard comme base logicielle
du transport et des capacités inspirées de la documentation officielle NetBird,
à redévelopper au sein de ZTP et du PA. Elle conserve le module officiel dédié
côté PBO, les autorités et délégations, ainsi que les garanties de contrats,
de configuration, d'exploitation et de qualification. Les arbitrages techniques
non décidés sont identifiés séparément ; une recommandation ne vaut pas validation.
Elle ne constitue pas une
spécification OpenSpec validée, une autorisation d'implémentation ou une preuve
de fonctionnement. Les spécifications OpenSpec existantes conservent leur
autorité sur le comportement actuel de Pixs.

## Objet et périmètre

ZTP assure l'identification des pairs, leur rattachement aux autorités,
l'autorisation de leurs communications, la découverte des destinations et le
transport chiffré. Sa granularité va de la machine complète aux services
applicatifs d'une instance Pixs.

Une position dans la hiérarchie, une appartenance au réseau, une adresse IP ou
un certificat valide ne donnent pas, à eux seuls, accès aux ressources.
Chaque communication est couverte par une autorisation vérifiable émanant
d'une autorité compétente.

Le réseau possède ses propres mécanismes de sécurité. Son fonctionnement ne
dépend pas obligatoirement d'un SSO externe, d'un cloud, d'un VPN supplémentaire
ou d'un service mesh. Des protections complémentaires peuvent s'y superposer
sans remplacer ses contrôles ni élargir ses permissions.

Le nom Zéro Trust Pixs et son sigle ZTP désignent cette architecture Pixs.
Aucun choix du produit ZeroTier n'est effectué.

## Base WireGuard et développement propre à Pixs

WireGuard, en tant que logiciel, est la base retenue pour le transport IP
authentifié et chiffré entre pairs ZTP. Le protocole cryptographique n'est pas
réimplémenté dans Pixs. Le backend, les versions et les interfaces de pilotage
restent à qualifier pour chaque plateforme et profil.

ZTP développe ses propres fonctions d'enrôlement, de gestion des pairs,
d'autorisation, de distribution des configurations, de découverte, de
rendez-vous, de relais, d'adressage, de DNS, de posture et de supervision.
NetBird sert de référence documentaire pour les capacités retenues ; ses
agents, serveurs, briques et code ne sont pas intégrés. Aucune compatibilité
avec ses API, protocoles internes ou formats n'est exigée implicitement.
La réutilisation de bibliothèques standards indépendantes de NetBird reste
soumise aux choix techniques et à la politique de dépendances Pixs.

Le plan de contrôle associe les décisions de gestion du PBO et les décisions
des autorités compétentes selon les frontières déjà décrites. Le PA exécute
les fonctions de contrôle qui correspondent à ses rôles déclarés et applique
le plan de données WireGuard. Le trafic métier ne traverse pas obligatoirement
le PBO ni une autorité. Une carte réseau autorisée ne crée pas un maillage
intégral et ne confère pas de droit métier.

Tous les composants nécessaires sont exploitables sur l'infrastructure de
l'opérateur : autorités, certification, découverte, rendez-vous, relais,
résolution de noms et références temporelles. Aucun service NetBird, cloud
éditeur ou SSO extérieur n'est nécessaire au fonctionnement du réseau.
Les dépendances externes facultatives sont déclarées et leur indisponibilité
n'élargit jamais les accès. L'autonomie est qualifiée au démarrage à froid,
à l'enrôlement, au renouvellement et au basculement, avec les services de
l'éditeur injoignables.

### Plateformes d'exécution du PA

Le périmètre précisé par le développeur le 5 octobre 2026 couvre PA sur
machines physiques Linux et Windows, VM Linux et Windows, Docker et LXC
sous Proxmox. Les garanties ZTP restent communes ; backends, filtrage, DNS,
privilèges et attestation sont qualifiés par plateforme et profil. Cela
n'impose pas Windows comme plateforme de PBO ni tous les rôles d'autorité
sur chaque cible. La matrice détaillée figure dans le CdC PA.

Le choix A01, validé par le développeur le 5 octobre 2026, privilégie les
backends natifs : WireGuard du noyau Linux et backend natif Windows, dont
WireGuardNT reste le candidat à qualifier. L'espace utilisateur est retenu
pour les profils qui le nécessitent, après qualification. Une VM utilise
le noyau de son invité ; un conteneur Linux
partage celui de son hôte effectif. Docker dans une VM et Docker dans LXC
ont des frontières distinctes. Le placement exact, les versions Proxmox et
les profils privilégiés ou non privilégiés restent à préciser. Un backend
en espace utilisateur ne contourne pas les permissions nécessaires au tunnel.

Le TPM de l'hôte, le passthrough TPM et le vTPM sont distingués. Snapshot,
clone, restauration ou migration réévaluent les identités et preuves requises ;
aucune copie de configuration n'accorde automatiquement une identité admise.
Les conditions de confiance des profils virtualisés restent dans A10.

### Capacités de référence et adaptation ZTP

La documentation officielle a été consultée le 5 octobre 2026. Cette matrice
identifie des capacités à spécifier ; elle ne promet ni parité générale avec
NetBird ni prise en charge de tous ses clients et plateformes.

| Référence fonctionnelle | Exigence propre à ZTP | Référence officielle |
| --- | --- | --- |
| Gestion et distribution des pairs | Inventaire et carte réseau limitée aux relations autorisées, versionnée et réconciliée. | [Architecture NetBird](https://docs.netbird.io/about-netbird/how-netbird-works) |
| Groupes et politiques d'accès | Sélection explicite des sources, destinations, directions, protocoles et ports, sous les délégations ZTP et les permissions Pixs. | [Politiques NetBird](https://docs.netbird.io/manage/access-control/manage-network-access) |
| Enrôlement automatisé | Jetons à validité et usages bornés, admission contrôlée et identités permanentes ou éphémères. | [Enrôlement NetBird](https://docs.netbird.io/manage/peers/register-machines-using-setup-keys) |
| Connectivité directe et relayée | Recherche de chemins autorisés et relais ZTP transportant les paquets WireGuard sans les déchiffrer. | [Connectivité NetBird](https://docs.netbird.io/about-netbird/understanding-nat-and-connectivity) |
| DNS privé | Zones et résolveurs administrés, résolution par domaine et visibilité bornée par les politiques. | [DNS NetBird](https://docs.netbird.io/manage/dns) |
| Ressources et passerelles | Accès explicite à une IP, un préfixe ou un domaine sans PA sur la ressource finale. | [Networks NetBird](https://docs.netbird.io/manage/networks) |
| Posture | Évaluation des versions et conditions de sécurité déclarées, distincte de l'attestation TPM. | [Posture NetBird](https://docs.netbird.io/manage/access-control/posture-checks) |
| Redondance de routage | Sélection et basculement entre passerelles, avec effets sur les sessions documentés. | [Passerelles NetBird](https://docs.netbird.io/manage/networks/how-routing-peers-work) |

Le socle de rédaction couvre les pairs, politiques, connectivité, DNS,
posture, réconciliation et révocation. Les passerelles et ressources sans PA
constituent un profil de réseau étendu dont l'inclusion dans la première
réalisation reste à arbitrer. Les sorties Internet globales, accès SSH,
reverse proxies publics et intégrations EDR/MDM restent des extensions
à cadrer séparément ; cette intégration ne les active pas.

## Modes de fonctionnement

| Mode | Fonctionnement |
| --- | --- |
| Autonome | Une seule instance Pixs, indépendante des autres instances, assure sa propre gouvernance, son administration et ses opérations métier. |
| Zéro Trust Pixs (ZTP) | Plusieurs instances participent à un réseau gouverné, avec autorités hiérarchiques, délégations explicites et coopération autorisée entre pairs. |

Le mode autonome conserve les règles de sécurité de Pixs. L'autonomie décrit
l'absence de dépendance à une autorité Pixs extérieure ; les dépendances
techniques nécessaires au service restent déclarées et exploitées dans son
périmètre.

Dans le mode ZTP, chaque instance conserve ses responsabilités locales,
ses contrôles applicatifs et l'autorité sur les ressources qui lui sont
attribuées. Elle respecte les contraintes communes et les mandats reçus.

Le passage d'un mode à l'autre est explicite. Une coupure, une révocation ou
une perte de quorum ne déclenche pas un retour automatique au mode autonome.
La procédure d'adhésion ou de retrait reste à spécifier.

## Vocabulaire

| Terme | Sens dans ce document |
| --- | --- |
| Zéro Trust Pixs (ZTP) | Le réseau sécurisé Pixs et ses mécanismes de communication et d'autorité. |
| PZT | Sigle employé dans le CdC du PA pour le même réseau ; ZTP reste le sigle de ce document. |
| Pixs Agent (PA) | Le composant qui exécute ZTP selon les rôles et permissions qui lui sont attribués. |
| Pixs Backoffice (PBO) | Le composant qui contrôle et configure le PA dans le périmètre autorisé. |
| Instance Pixs | Une installation logique Pixs ; elle peut comporter plusieurs processus ou services. |
| Pair | Une entité communicante identifiée : machine, environnement isolé, instance ou service. |
| Autorité logique | Une responsabilité de gouvernance, éventuellement assurée par plusieurs membres actifs. |
| Membre d'autorité | Un composant participant au fonctionnement d'une même autorité logique. |
| Tranche | Un niveau de l'organisation verticale ; son appartenance ne crée aucun droit automatique. |
| Groupe de coopération | Un ensemble de pairs autorisés à collaborer pour une finalité et un périmètre précis. |
| Délégation | Un mandat limité autorisant un bénéficiaire à exercer certains pouvoirs. |
| Autorisation de communication | Une décision couvrant une relation entre pairs et les services concernés. |
| Relais | Un service acheminant les échanges lorsque le chemin direct est indisponible. |

L'identité d'un pair reste distincte de son adresse de connexion. Un déplacement
réseau ne modifie pas automatiquement son identité, sa tranche ou ses droits.

## Modèle des identités ZTP

L'installation Pixs, l'autorité logique, le membre d'autorité, le PA, le pair
et le service exposé possèdent des références distinctes et stables. Les
entités persistées par Pixs utilisent les UUIDv7 prévus par le projet ; les
composants, capacités et contrats utilisent leurs identifiants namespacés.
Les identifiants de transport et empreintes cryptographiques restent séparés
de ces références.

Les mappings vers les DigitalIdentity Pixs sont explicites, déterministes et
auditables. Une identité de machine ou de service n'implique pas la présence
d'un utilisateur humain. Le renouvellement d'une clé ne change pas
automatiquement l'identité ; un certificat ne fusionne pas deux identités.
Un pair distant ne peut pas imposer un tenant ou un scope local.

L'assurance d'identité, l'assurance d'authentification et la confiance fédérée
restent distinctes. La possession d'une clé n'accorde pas automatiquement une
assurance multifacteur. Les opérations de gestion sensibles du PBO exigent
l'assurance et la fraîcheur déclarées, avec step-up ou refus lorsque nécessaire.
La représentation détaillée des identités et de leurs mappings reste à spécifier.

## Articulation avec le cahier des charges du PA

Le [CdC Pixs Agent](PIXS_AGENT.md), relu en version 0.0.6 pour cette intégration,
décrit le PA comme un binaire pouvant fonctionner sans PBO, PFO ou navigateur
local. ZTP conserve cette indépendance d'installation. Le langage cible du PA
est Python avec génération de C puis compilation native ; les bibliothèques
et adapters ZTP doivent être qualifiés avec cette chaîne, ses dépendances et
les plateformes retenues. L'outil de compilation n'est pas choisi par ce CdC.

Les sept modes proposés du même binaire sont system-start, system-stop,
system-daemon, session-start, session-stop, session-daemon et `pzt-daemon`.
Ils constituent
des contextes d'exécution du PA, distincts de ses rôles ZTP de pair, d'autorité,
de découverte ou de relais. Un mode système ne donne pas automatiquement
un pouvoir d'autorité et un mode utilisateur ne s'élève pas implicitement.

Les identités, états et permissions des contextes système et utilisateur sont
séparés. Une session graphique est distinguée du compte utilisateur ; plusieurs
sessions concurrentes restent isolées. Le contrat rattache les opérations et
communications au mode, à la cible et à la session lorsque celle-ci s'applique.

Les délais de lancement de system-daemon et de session-daemon, les préconditions
et les budgets d'arrêt sont déclarés. Le mode `pzt-daemon` démarre sans délai
au démarrage du système ou du conteneur, avec les droits système. Il assure
la convergence et la réconciliation de ZTP lorsque celui-ci est activé et
configuré sur ce PA ; sinon, il se ferme. Son démarrage sans délai ne dispense
pas des préconditions et contrôles d'autorisation applicables et ne modifie
pas les délais des deux autres démons.
Le séquencement garantit que les fonctions ZTP nécessaires sont
disponibles pour les échanges des invocations ponctuelles et permanentes.
Le provisionnement établit explicitement la configuration minimale, l'identité,
les ancrages et les références de secrets avant le premier échange PBO–PA.
Il ne sert pas de canal continu de commandes par fichiers. L'initialisation
minimale ZTP reste distincte des activités différées des démons ; son
séquencement avec `pzt-daemon` et les autres modes reste à qualifier dans
l'adaptateur de plateforme.

L'arrêt conserve ZTP tant que les échanges requis restent possibles dans
le budget déclaré, puis draine ou interrompt les traitements selon leur contrat.
Un arrêt forcé ne vaut pas preuve d'exécution d'une opération de fermeture.
Une indisponibilité du réseau pendant l'arrêt produit un résultat explicite
et suit la politique de reprise définie.

Les opérations locales sont sélectionnées dans un catalogue déclaré et livré
par une chaîne contrôlée. La détection d'une dérive reste distincte de sa
correction ; celle-ci exige une politique et une autorisation propres. Une
instruction reçue via ZTP ne suffit pas à télécharger du code, évaluer du
Python ou ouvrir un shell privilégié.

Les états techniques locaux éventuellement nécessaires au PA sont déclarés,
bornés, protégés et soumis à rétention. Ils ne deviennent pas une source
d'autorité métier et ne remplacent pas les états autoritatifs ZTP. Une opération
interne au PA, sans échange PBO, reste distincte d'une communication PBO–PA ;
elle n'autorise aucun canal de contournement ni succès métier déduit localement.

La composition des capacités PA est réalisée au build et utilise les
métadonnées et contrats Pixs applicables. Elle n'impose pas à l'exécutable PA
d'embarquer Django ou PostgreSQL. Le stockage technique de reprise possède
son contrat de durabilité et ne dépend pas d'un filesystem éphémère lorsque
la reprise est requise. Un stockage plein, indisponible ou corrompu bloque
les opérations dont la preuve durable ne peut être tenue.

## Exécution et contrôle de ZTP

Le PA assure l'exécution de ZTP. Selon les rôles qui lui sont attribués, il
porte les fonctions de communication entre pairs et les services de contrôle
ou de transport décrits dans ce document. Ses capacités effectives restent
limitées par sa configuration, son identité et ses mandats.

Le PBO contrôle et configure le PA : il permet de gérer les rôles, les
paramètres et les politiques applicables, ainsi que de consulter l'état
d'exécution et les diagnostics autorisés. Les actions effectuées depuis le
PBO respectent les trois politiques complémentaires et la chaîne d'autorité.

| Élément | Responsabilité |
| --- | --- |
| ZTP | Définir le fonctionnement du réseau et ses garanties. |
| PA | Exécuter les fonctions ZTP autorisées et appliquer la configuration reçue. |
| PBO | Contrôler et configurer le PA dans le périmètre attribué à l'opérateur ou à l'autorité. |

Le PBO constitue le point de contrôle et de configuration ; son utilisation
ne vaut pas, à elle seule, autorisation d'une opération. Les décisions restent
rattachées à l'autorité compétente et aux permissions de l'acteur. Le PA
vérifie les instructions et leurs mandats avant de les appliquer.

Le backend Django du PBO autorise les opérations de gestion. Les services
d'autorité ZTP exécutés par les PA valident les communications dans leur
mandat ; les PA destinataires appliquent les décisions vérifiables. Une
instruction de gestion acceptée par le PBO ne remplace pas la validation
réseau requise par l'autorité compétente.

Les opérations métier restent autorisées par Django chez le destinataire.
Le PA ne devient pas une seconde autorité métier et une permission de
communication ne vaut pas permission applicative.

Tous les échanges entre PBO et PA passent par ZTP, dans les deux sens et
pour les sept modes décrits par le CdC PA. Cela couvre les instructions,
configurations, opérations d'administration, états, diagnostics, événements
et résultats, même sur le même hôte ou dans le même conteneur.

Un transport local fait partie de ZTP et applique identification,
authentification mutuelle, autorisation, chiffrement, validité, protection
contre le rejeu et traçabilité. Il n'impose pas un détour par un relais distant.
Le choix A03, option A validée par le développeur le 5 octobre 2026, retient
TLS mutuel intégré à ZTP pour PBO et PA sur le même hôte d'exécution : même
OS hôte, même VM ou même conteneur selon le profil. Ce transport local porte
les échanges courants sans exiger un tunnel WireGuard local. Des VM ou
conteneurs distincts sur un même serveur physique conservent leurs frontières
réseau ; leur cohébergement ne suffit pas à appliquer ce profil local.
L'endpoint, sa portée d'écoute et les mécanismes d'isolation restent à
qualifier selon la plateforme. TLS mutuel ne remplace pas les contrôles
d'autorisation, d'attestation et de révocation de ZTP.
Une socket Unix, la boucle locale ou un fichier ne peuvent pas servir de canal
PBO–PA hors ZTP. Les permissions système sont complémentaires aux contrôles ZTP.

Si ZTP est indisponible, non initialisé ou non vérifiable, la communication
PBO–PA concernée est bloquée sans repli hors ZTP. Le séquencement d'amorçage,
les modalités du TLS mutuel local et la répartition des services restent à
spécifier.

## Module ZTP côté PBO

Le pilotage de ZTP côté PBO est fourni par un module Pixs officiel dédié,
utilisant le système normal de modules. Il possède ses propres responsabilités,
contrats publics, données de gestion, migrations, permissions, contributions
frontend et cycle de vie.

Le module ZTP n'est pas intégré au Kernel ni absorbé par pixs.core. Le Kernel
fournit les mécanismes génériques de composition ; pixs.core fournit les
identités, tenants, scopes et permissions communes que le module consomme
par leurs contrats publics. ZTP ne crée pas de référentiel d'identité Pixs
concurrent.

Le module porte la représentation et le pilotage des autorités, des délégations,
des politiques, des configurations des PA, des opérations de contrôle et de
leur suivi. Le PA conserve l'exécution des fonctions réseau et des services
ZTP correspondant à ses rôles. Cette séparation ne déplace pas l'exécution
des communications dans le PBO.

Les autres opérations système ou utilisateur restent possédées par les
modules qui les définissent et utilisent les interfaces publiques PA et ZTP.
Le module réseau ne devient pas propriétaire de toutes les opérations locales.
PFO adresse ses demandes à PBO, qui les autorise avant transmission via ZTP ;
une liaison directe PFO–PA exige un cadrage distinct.

### Caractère obligatoire et protection

Le module est requis dans les profils PBO qui pilotent ZTP. Une composition
déclarant ce profil sans le socle ZTP est invalide. Son caractère obligatoire
est déclaré et vérifié par les mécanismes génériques de composition, sans
traitement fonctionnel spécifique de ZTP dans le Kernel.

Le terme inaliénable signifie que le socle ne peut pas être retiré ou désactivé
tant que le profil le requiert. Un retrait du réseau et un changement de profil
passent par une procédure explicite et contrôlée avant tout retrait éventuel
du module.

Cette protection reste compatible avec les mises à jour, migrations,
réparations et mesures de quarantaine autorisées. La suspension d'un transport
ou l'isolement d'un pair ne supprime pas le socle de contrôle. Une panne produit
un état diagnostiquable et suspend les fonctions concernées selon leurs
garanties, sans fonctionnement permissif ni abandon des contraintes du réseau.

La présence obligatoire du module dans toutes les installations autonomes
n'est pas décidée. S'il est inclus dans un profil autonome, il peut fournir
le pilotage local du PA sans activer les fonctions de réseau distribué.

### Enrichissement par sous-modularité

Le module comprend un socle stable de pilotage et de contrats avec le PA.
Ses capacités sont enrichies par des sous-modules utilisant les mécanismes
Pixs habituels : manifests, dépendances, lifecycle, services, permissions,
configuration et contributions frontend déclarées.

Le découpage envisagé est le suivant ; ses frontières exactes restent à préciser :

```text
Module ZTP côté PBO
├── Socle de pilotage et contrats PA
├── Autorités et délégations
├── Politiques et autorisations
├── Gestion des agents
├── Découverte et relais
├── Topologie et supervision
└── Extensions spécialisées
```

Les sous-modules enrichissent le module par ses interfaces publiques, sans
modifier directement son implémentation privée ou celle d'un autre composant.
Ils ne peuvent ni supprimer les contrôles obligatoires, ni élargir implicitement
les permissions. Une capacité nécessaire à un rôle déclaré reste requise,
même si son implémentation est portée par un sous-module.

### Administration locale et reprise

Un accès d'administration local authentifié et protégé permet de diagnostiquer
et réparer ZTP lorsque ses communications distantes sont indisponibles. Le
contrôle PBO–PA utilise un transport local intégré à ZTP et conserve ses
permissions, contrôles et audit ; il ne dépend pas exclusivement d'un chemin
distant, mais ne contourne jamais ZTP.

Si les fonctions ZTP locales nécessaires sont elles-mêmes indisponibles,
le contrôle PBO–PA reste bloqué. Les opérations d'amorçage ou de reprise
strictement internes au PA et les adapters de plateforme déclarés sont
spécifiés séparément, avec leur autorisation ; ils ne créent pas un canal
alternatif PBO–PA. Aucun accès local hors ZTP n'est activé implicitement.

Les mécanismes exacts de protection du lifecycle, l'accès local de reprise,
l'identifiant canonique du module et les contrats PBO vers PA restent à
spécifier avant implémentation.

## Contrats et compatibilités

Des contrats publics distincts définissent la configuration, les instructions
de contrôle, les rapports d'état, la découverte, les autorisations et les
révocations. Chaque contrat possède un propriétaire, un identifiant, une
version, des schémas, des erreurs stables et des garanties documentées.

Les versions du CdC, du module PBO, du PA, du protocole ZTP, des schémas de
configuration et des politiques sont distinctes. Une matrice de compatibilité
vérifie les composants, capacités, contrats, événements, providers et données
concernés avant activation ou mise à niveau. Une version plus récente n'est
pas présumée compatible.

Pour le CdC en version x.y.z, un incrément de 0.1.0 augmente la composante
mineure et conserve les autres composantes : x.(y+1).z. La consolidation
présente fait ainsi passer le CdC de 0.2.0 à 0.3.0.

Les API de gestion PBO suivent les contrats OpenAPI Pixs, leurs enveloppes de
succès et d'erreur et leur versionnement. Le protocole entre PA peut employer
un transport adapté avec ses propres schémas documentés. Les événements de
contrôle sont versionnés séparément des contrats HTTP.

Les mises à jour progressives prévoient une coexistence explicite des versions
supportées. Une combinaison incompatible est refusée sans abaisser les
exigences de sécurité. Les migrations restent contrôlées et aucun downgrade
automatique du schéma ne simule un rollback. Les versions admises et les
formats exacts des contrats restent à définir avant implémentation.

Le contrat d'instruction de contrôle précise l'émetteur PBO vérifié, l'acteur
initial, l'exécuteur technique, la cible canonique, le contexte, l'opération
et sa version, les paramètres typés et bornés, le mandat et sa validité,
les versions de politique et de délégation, les obligations et les références
de suivi. PA vérifie ces éléments à l'exécution, y compris après attente ou
reprise. Une permission de surveillance ne vaut pas permission de modification.

La réception, la validation, l'exécution technique, la livraison du résultat
et sa confirmation applicative sont des dimensions distinctes. Un accusé de
réception ne prouve pas la réussite. Après un effet système dont le résultat
est indéterminé, la reprise vérifie la postcondition si le contrat le permet
ou requiert une intervention autorisée, sans rejeu aveugle.

## Configuration demandée et configuration appliquée

Le PBO conserve la configuration souhaitée. Le PA rapporte la configuration
effectivement appliquée, sa version, son résultat et les écarts diagnostiquables.
Une configuration envoyée ou reçue n'est pas présentée comme appliquée avant
confirmation vérifiable de son application.

Les configurations possèdent un schéma typé et versionné. Leur résolution
respecte les sources et priorités communes Pixs : schéma, défauts du composant,
configuration statique, configuration runtime, puis références de secrets.
Les formats Debian, Docker et développement alimentent ce même modèle.

L'application vérifie les préconditions, la compatibilité, l'autorisation et
la version de concurrence attendue. Une configuration périmée ou conflictuelle
est refusée explicitement. Le contrat définit la frontière d'application,
les états intermédiaires et le comportement après application partielle ou
interruption. La reprise ne restaure pas une ancienne configuration interdite.

Un feature flag ne peut ni retirer une capacité requise, ni modifier
implicitement les permissions, les providers ou les contraintes du réseau.

Une reconfiguration affectant ZTP prévoit dans son plan la validation du
nouveau canal de contrôle et le comportement en cas de perte de contact.
Une compensation préautorisée peut être prévue lorsque sa faisabilité,
son déclencheur et sa durée sont déclarés. Elle ne réactive jamais une identité
révoquée, un mandat expiré ou une permission supprimée. Sans compensation sûre,
l'échec reste explicite et suit la procédure de reprise, sans canal hors ZTP.

## Opérations de gestion persistantes

L'enrôlement, le changement de parent, la révocation, la reconfiguration,
la maintenance et les mises à niveau sont des opérations contrôlées. Elles
portent un plan, un identifiant d'opération, un acteur, un périmètre, une
version, une corrélation, une clé d'idempotence et un résultat persistant.
Les mutations sensibles séparent la préparation du plan et son application
confirmée ou explicitement autorisée.

Les mutations de gestion possédées par le module PBO passent par ses Commands
autorisées et leurs frontières transactionnelles Django. Les instructions
vers le PA conservent le mandat et l'identité de l'acteur initial. La CLI,
l'interface PBO et les façades non interactives consomment les mêmes contrats.

Les traitements longs utilisent des opérations suivies et des Jobs persistants
avec checkpoints, retries bornés et états d'échec diagnostiquables. L'autorisation
est réévaluée à l'exécution. Les identifiants d'opération, de Command, d'événement
et de Job restent distincts.

Un rejeu identique restitue l'état ou le résultat enregistré sans double effet ;
un contenu divergent produit un conflit. Les événements confirmant une mutation
sont publiés après son engagement, avec outbox et déduplication lorsqu'elles
sont requises. La livraison générale suit at-least-once sans promesse
exactly-once de bout en bout.

## Trois politiques complémentaires

Les trois politiques sont complémentaires. Leur attribution est explicite ;
aucune ne donne automatiquement les pouvoirs des deux autres.

| Politique | Pouvoirs possibles | Limites |
| --- | --- | --- |
| Gouvernance et délégation | Définir les contraintes communes, enrôler dans un périmètre, attribuer ou révoquer des mandats et encadrer les échanges. | La position hiérarchique ne vaut pas accès général aux données ou aux machines. |
| Administration | Consulter la santé, distribuer une configuration autorisée, organiser les mises à jour, gérer les modules, renouveler les identités et mettre en quarantaine. | Chaque opération possède un périmètre et un contrôle ; un accès système général ne découle pas de cette politique. |
| Opérations métier | Consulter des projections autorisées, traiter des ressources, approuver des opérations et coordonner des workflows. | Les règles métier, tenant, scope, confidentialité et propriété des données continuent à s'appliquer. |

Une autorité régionale peut disposer des trois politiques avec des périmètres
différents. Un service de maintenance peut recevoir uniquement un mandat
d'administration. Un pair métier peut coopérer sans gouverner ni administrer
son destinataire.

Le pouvoir d'administration peut affecter indirectement les données, notamment
lorsqu'il permet de changer le logiciel ou les permissions. Les opérations
modifiant les contrôles de sécurité demandent donc une protection spécifique.
La séparation des identités techniques utilisées pour ces pouvoirs est une
proposition de conception à préciser.

## Organisation verticale et horizontale

La structure retenue superpose un arbre de gouvernance et un graphe de
coopération. Une instance rattachée possède un parent logique unique ; les
rattachements sont sans cycle. Le nombre de niveaux reste adaptable.

```mermaid
flowchart TB
    R["Autorité racine logique"]
    R -->|Délégation| A["Autorité A logique"]
    R -->|Délégation| B["Autorité B logique"]
    A --> A1["Instance A1"]
    A --> A2["Instance A2"]
    B --> B1["Instance B1"]
    B --> B2["Instance B2"]
    A <-->|Coopération autorisée| B
    A1 <-->|Coopération autorisée| A2
    A2 <-->|Coopération interbranche autorisée| B1
```

Les relations horizontales couvrent les pairs d'une même tranche et peuvent
relier des branches différentes sur un périmètre autorisé. Les permissions
peuvent être différentes dans les deux sens. Une instance peut participer à
plusieurs groupes de coopération.

Le niveau organisationnel et le niveau de sécurité sont distincts. Les rôles
d'identité, d'administration et de traitement métier peuvent être isolés sans
imposer un nombre fixe de tranches ou un classement universel des instances.

L'arbre des autorités ne se confond pas avec la hiérarchie des scopes métier
de Pixs. Un rattachement au réseau ne crée ni tenant, ni appartenance, ni accès
intertenant implicite.

## Règles de délégation

Une délégation identifie son émetteur, son bénéficiaire, les actions permises,
les cibles, le périmètre, la période de validité et le droit éventuel de
redélégation. Elle possède une identité stable, une version et un état
vérifiable de validité ou de révocation.

Une autorité ne transmet que les pouvoirs qu'elle détient et qu'elle est
autorisée à déléguer. Les contraintes obligatoires d'un ancêtre restent
applicables ; un descendant peut les renforcer sans les affaiblir.

Le destinataire contrôle le mandat avant d'exécuter une instruction, même si
l'émetteur est son parent. Les refus explicites et les limites de périmètre
restent applicables. Une délégation valide ne remplace pas une vérification
d'identité ou une autorisation métier.

Un changement de parent, de tranche ou de groupe réévalue les droits concernés.
Les versions de politiques et de délégations utilisées sont traçables.

## Autorités multimaîtres et synchronisation

L'autorité racine et les sous-autorités peuvent fonctionner en multimaître.
Plusieurs membres actifs représentent une même autorité logique et
synchronisent leur état. Le parent unique désigne cette autorité logique,
sans imposer une machine unique.

L'état partagé comprend les rattachements, identités publiques, délégations,
politiques, autorisations, révocations et décisions nécessaires à leur
exercice. La gestion des clés privées de signature est traitée séparément de
la réplication ordinaire des données.

Chaque état de contrôle ZTP identifie son propriétaire, sa source autoritative,
son mécanisme d'engagement et ses projections. Cela couvre notamment les
politiques, délégations, rattachements et révocations, qui sont eux-mêmes des
données de référence. La base du PBO et l'état des autorités ne peuvent pas
décider indépendamment de la validité d'un même mandat.

PostgreSQL demeure la référence applicative Pixs. L'utilisation d'un autre
stockage autoritatif exige une capacité spécialisée explicitement spécifiée
et validée. Le choix du stockage spécialisé éventuel, du consensus et de la
coordination entre gestion PBO et décisions d'autorité reste ouvert.

Le multimaître des autorités ne signifie pas que les données métier Pixs
deviennent multimaîtres. Leurs règles de persistance, de propriété et de
placement restent celles des spécifications applicables.

**Proposition à arbitrer :** utiliser un fonctionnement actif-actif avec
cohérence forte pour les changements critiques. Chaque membre peut recevoir
une demande ; son engagement est soumis à une validation commune. Cette
organisation peut utiliser un leader interne de consensus. Elle ne correspond
pas à des écritures indépendantes engagées par tous les membres pendant une
partition réseau.

Une synchronisation ultérieure avec priorité au dernier horodatage n'est pas
une règle suffisante pour résoudre un conflit entre révocation et attribution
de droits. L'ordre des décisions, leur validation et la protection contre une
autorité périmée restent à spécifier.

**Proposition à arbitrer :** sans quorum, bloquer les nouveaux changements
critiques et conserver uniquement les opérations dont le mandat, la fraîcheur
et la validité restent vérifiables. Le délai de propagation des révocations
et la disponibilité recherchée devront être définis ensemble.

Le consensus protège la cohérence ; il ne suffit pas à protéger contre un
signataire compromis. Les règles de signature, de révocation d'un membre et
de preuve d'engagement des décisions font partie du futur design.

## Chaîne de certification et identités

La confiance cryptographique repose sur une chaîne de certification ancrée
dans les autorités racines et déléguée aux autorités intermédiaires.
L'enrôlement établit explicitement les ancrages de confiance avant les échanges.
La découverte d'une autorité ne suffit pas à lui accorder confiance.

Chaque pair dispose d'une identité propre et d'une clé privée protégée. Le
certificat rattache l'identité à une autorité reconnue ; les permissions de
communication sont portées par une décision distincte et vérifiable.

L'authentification mutuelle vérifie l'identité attendue, la chaîne, les usages
admis, les contraintes des autorités, la validité et la révocation selon la
politique applicable. La preuve de possession de la clé est nécessaire.

La rotation, le renouvellement, la révocation et la récupération sont prévus
pour les pairs comme pour les autorités. Aucun secret n'est publié dans la
découverte, les journaux ou les messages d'audit.

La racine logique peut être représentée par plusieurs membres, mais cela ne
valide pas une copie non contrôlée de sa clé sur chacun d'eux. La distribution
des signataires, les certificats intermédiaires et l'éventuelle signature à
seuil restent à choisir. Les formats de certificats, de signatures d'autorité
et de liaisons de clés ne sont pas arrêtés ; la cryptographie du transport
reste celle de l'implémentation WireGuard retenue.

### Enrôlement et protection des clés

L'enrôlement définit l'établissement initial de confiance, la preuve d'identité,
les préconditions, le mandat et la mise en service contrôlée. La présence
d'une configuration, d'une adresse découverte ou d'un artefact ne crée pas
automatiquement un compte administrateur, un rattachement ou une confiance.
Une reprise réutilise l'opération persistante sans dupliquer l'identité.

La protection des clés, leur rotation et la récupération après compromission
font partie des procédures d'exploitation. Les configurations du PBO utilisent
des références de secrets ou des interfaces de signature contrôlées ; les
clés privées ne sont pas exposées dans le frontend, les API de consultation,
les rapports, les manifests, les paquets ou les images.

Les accès aux secrets ou fonctions de signature sont liés à une identité
de workload et à une politique déclarée. Une référence indisponible ou une
permission non vérifiable bloque la fonction protégée concernée. Les procédures
de renouvellement, de changement d'ancrage et de reprise précisent leurs
conditions de sécurité sans transformer la découverte en source de confiance.

### Intégration du PA et attestation TPM de l'hôte

L'identité stable Pixs, le certificat d'identité ZTP, la clé publique
WireGuard et la clé d'attestation TPM sont des éléments distincts. Leur
association est vérifiée, versionnée et auditée. Le certificat ne participe
pas directement au handshake WireGuard ; il établit la confiance dans la
liaison identité–clé que le contrôle ZTP distribue aux pairs autorisés.
Une rotation de clé WireGuard ne recrée pas l'identité Pixs et la révocation
de son ancienne liaison entraîne le retrait des accès correspondants.

La clé WireGuard est générée localement et sa valeur privée reste dans le
périmètre d'exécution autorisé. Le backend retenu précise son accès et sa
protection. La non-exportabilité de la clé d'attestation TPM ne prouve pas
que la clé privée WireGuard reste dans le TPM : le stockage protégé, le
déverrouillage éventuel et la résidence en mémoire sont qualifiés séparément.

Le protocole d'intégration d'un PA au réseau ZTP enregistre la clé publique
TPM de référence de l'hôte ainsi que son nom d'hôte. Ces informations sont
rattachées explicitement à l'identité stable du PA et de son hôte, avec le
rôle de la clé, sa provenance vérifiée et les justificatifs de confiance
nécessaires. Le nom d'hôte est une métadonnée contrôlée ; il ne constitue
ni une identité cryptographique, ni une preuve d'intégrité à lui seul.

La clé publique sert à vérifier les preuves TPM requises lors de chaque
connexion ou reconnexion du PA à ZTP. La clé d'identité du TPM et la clé
d'attestation utilisée pour signer ces preuves sont distinguées lorsque
leurs rôles diffèrent ; leur liaison est vérifiée à l'enrôlement. La clé
privée d'attestation est créée dans le TPM et non exportable. Le PBO reçoit
les éléments publics et les preuves, jamais cette clé privée.

Chaque vérification utilise un défi aléatoire frais et une preuve liée au
PA, à l'hôte et à la connexion concernée, afin de refuser le rejeu d'une
ancienne réponse. Une signature valide prouve l'utilisation de la clé
correspondante ; elle ne démontre pas, à elle seule, l'intégrité du PA.
La vérification d'intégrité exige une attestation des mesures du binaire
PA et de l'environnement requis par son profil, collectées par une chaîne
de mesure de confiance, protégées par le TPM et confrontées aux références
approuvées. Une empreinte simplement déclarée ou signée par le PA ne suffit
pas. La preuve ne couvre que les éléments et états effectivement mesurés.

Ce contrôle complète le protocole d'authentification du PA à ZTP sans le
remplacer, le surclasser ou affaiblir ses exigences. Une attestation valide
ne dispense jamais de l'authentification, des contrôles de certificat,
de révocation, de délégation et d'autorisation applicables. Une preuve
d'intégrité requise absente, périmée, rejouée, invalide ou non vérifiable
bloque la connexion ou reconnexion concernée et produit un diagnostic
et un audit sans secret.

Pour un PA dans Docker ou LXC, le protocole distingue le nom du conteneur
du nom de l'hôte portant le TPM et vérifie la liaison PA–conteneur–hôte.
Le partage du TPM ne fusionne pas les identités des PA. Un changement
d'hôte, de clé ou de nom d'hôte suit une mise à jour contrôlée du rattachement,
sans remplacement automatique sur simple déclaration du PA.

Les formats de preuves, le choix et la liaison des clés TPM, les mesures
couvrant effectivement le PA, leurs références et leur politique de mise
à jour restent à spécifier. L'absence ou l'inaccessibilité d'un TPM, ainsi
que l'emploi d'un TPM logiciel ou virtuel, sont déclarés explicitement ;
les conditions d'admission de ces profils restent à arbitrer et ne valent
pas implicitement une attestation matérielle réussie.

## Services de contrôle et de transport

| Service | Responsabilité |
| --- | --- |
| Autorité | Enrôler, déléguer, valider les relations et gérer leur révocation. |
| Certification | Émettre et renouveler les justificatifs d'identité dans un mandat autorisé. |
| Découverte | Enregistrer et résoudre les pairs et services accessibles selon la politique. |
| Rendez-vous | Aider les pairs autorisés à déterminer leurs chemins de connexion possibles. |
| Relais | Acheminer le trafic chiffré lorsque la communication directe est impossible. |
| Adressage et DNS | Gérer les adresses overlay, les noms et la résolution dans les périmètres autorisés. |
| Passerelle | Acheminer les flux autorisés vers des ressources sans PA selon un profil de réseau étendu déclaré. |
| Pixs Agent (PA) | Exécuter ZTP selon les rôles attribués, présenter les identités des pairs, vérifier les permissions et établir les canaux. |
| Pixs Backoffice (PBO) | Contrôler et configurer les PA et consulter leur état dans le périmètre autorisé. |

La découverte et le relais peuvent comporter plusieurs services répartis.
Leur emplacement ne leur donne aucun pouvoir d'autorité implicite. Les rôles
peuvent être cohébergés sans confondre leurs permissions.

Les services de contrôle possèdent eux aussi des identités certifiées et des
communications authentifiées et chiffrées. La réplication de leur état respecte
la confidentialité et les règles de résidence applicables.

## Lifecycle et profils ZTP

L'installation, l'activation, la configuration, la readiness et la santé sont
des dimensions distinctes. Le rattachement au réseau, la disponibilité des
capacités et la quarantaine sont également représentés explicitement, sans
les réduire à un état global ambigu.

Chaque profil déclare ses rôles, capacités obligatoires et optionnelles,
contrats, dépendances, limites et frontières réseau. Les rôles de pair,
d'autorité, de découverte, de rendez-vous et de relais ne sont pas activés
implicitement par la présence d'un composant ou d'un fichier.

Les contrôles distinguent liveness, startup, readiness et diagnostic opérateur.
Ils sont rapides, bornés, sans mutation métier et sans secret. Une capacité
obligatoire non vérifiable ne devient pas prête ; une capacité optionnelle
indisponible peut être isolée avec un état dégradé explicite.

Une panne de transport ne masque pas l'état du contrôle local. La maintenance
et la quarantaine peuvent cibler un composant, service ou capacité déclaré,
avec drainage borné, opérations permises et conditions de sortie vérifiées.
La reprise ne réactive pas un rôle ou un accès révoqué. Les états précis et
les profils distribuables restent à spécifier.

## Découverte et établissement des communications

### Inventaire et carte réseau autorisée

L'inventaire de contrôle associe l'identité stable, les liaisons de clés
publiques, les adresses overlay, les capacités, les groupes, les services,
les profils, les versions et les états d'admission. Les données privées de
connexion et de posture respectent les règles de minimisation et de rétention.

Chaque PA reçoit une carte réseau limitée à ses relations autorisées. Elle
identifie l'autorité compétente, le destinataire, la version et la validité,
les pairs joignables, leurs clés publiques vérifiées, leurs chemins candidats,
les routes et les décisions applicables. Elle ne révèle pas toute la topologie
ni les informations privées des branches étrangères au mandat.

La distribution prévoit un état initial, les changements de version et la
réconciliation après coupure. Une séquence manquante déclenche une resynchronisation
contrôlée ; un état périmé, contradictoire ou non vérifiable n'est pas appliqué.
A07a, option A validée le 5 octobre 2026, retient HTTP/JSON avec contrats
OpenAPI versionnés pour le contrôle. A07b, option A validée le 5 octobre
2026, retient un snapshot initial et des deltas ordonnés, avec reprise complète
en cas de désynchronisation. A07c, option B validée le 5 octobre 2026,
retient WebSocket/JSON pour les notifications et retours de suivi ; les API
HTTP de commande et de lecture sont conservées. A07d, option A validée
le 5 octobre 2026, retient les opérations métier JSON typées pour les deltas ;
les schémas et preuves restent à préciser. L'accusé de réception ne prouve pas que
les tunnels, routes et filtres sont effectivement configurés.

### Parcours d'établissement

La découverte ne révèle que les informations accessibles au demandeur. Elle
publie l'identité du service, ses caractéristiques nécessaires à la connexion
et des informations de joignabilité bornées dans le temps. Elle ne constitue
pas un annuaire public de toute la topologie.

Une communication suit le parcours de référence suivant :

1. Le pair demande une destination et un service identifiés.
2. L'autorité compétente valide la relation, en ligne ou par une autorisation
   signée encore valide selon le profil de sensibilité.
3. La découverte ou le rendez-vous fournit les chemins candidats autorisés.
4. Les pairs s'authentifient mutuellement et vérifient les permissions.
5. Ils privilégient un chemin direct compatible avec les contraintes déclarées.
6. Si le direct échoue, ils utilisent un relais autorisé.
7. Ils renouvellent les preuves nécessaires ou ferment la communication lorsque
   ses conditions cessent d'être satisfaites.

La recherche de connectivité ne contourne pas les règles du réseau sous-jacent
et n'accorde pas de nouvelles permissions. Un changement d'adresse ou de
chemin conserve les contrôles d'identité et d'autorisation.

Les mécanismes de traversée de NAT, le repli lorsque certains transports sont
bloqués et la sélection des relais restent à définir techniquement.

La recherche de chemins reprend les capacités de rendez-vous et de traversée
de NAT documentées par NetBird, avec un protocole et une implémentation propres
à ZTP. Les candidats de connectivité ne sont distribués qu'après autorisation.
Les services de découverte de chemins sont auto-hébergés et leurs messages
sont protégés contre l'usurpation et le rejeu selon un contrat à qualifier.
Le roaming WireGuard ne remplace pas la réévaluation d'une condition de
politique dépendant du réseau physique ou de la posture.

### Amorçage et identité du contrôle

Le premier tunnel nécessite la connaissance vérifiée des clés des pairs.
L'amorçage établit les ancrages, le mandat d'admission, la liaison de clé
WireGuard et les preuves d'attestation requises avant l'accès courant.
Il ne repose ni sur la confiance dans le premier serveur rencontré ni sur
une admission générale au réseau.

Le choix A02, option A validée par le développeur le 5 octobre 2026, retient
un canal TLS authentifié intégré à ZTP, restreint à l'enrôlement, aux preuves
d'attestation requises et à l'échange des paramètres publics WireGuard.
Le PA dispose d'un ancrage de confiance provisionné avant le premier contact
et vérifie l'autorité avant de lui transmettre ses justificatifs d'admission.
Les preuves d'identité et d'attestation requises sont vérifiées avant admission
et activation des communications courantes : WireGuard interhôtes ou
TLS mutuel dans le profil local validé dans A03.

Le profil précise la preuve d'identité initiale du PA, l'émetteur admis,
les opérations accessibles et les limites. Les formats, versions TLS,
bibliothèques et modalités de provisionnement restent à spécifier ; cette
décision ne suppose pas un certificat client déjà délivré avant l'enrôlement.
Le canal ne crée aucun échange PBO–PA hors ZTP et n'autorise aucun accès métier
avant admission. La reprise et le renouvellement respectent ces mêmes garanties
et ne deviennent pas un canal de contrôle général hors du transport courant.

La connexion logique ZTP, le tunnel WireGuard, le canal de contrôle et le
renouvellement cryptographique sont des événements distincts. Le mapping
vers les vérifications TPM et la reconnexion reste à décider dans A10 ; cette
distinction n'exempte aucune connexion ou reconnexion ZTP du contrôle requis.

## Enrôlement automatisé et pairs éphémères

Un jeton d'enrôlement possède un émetteur autorisé, un périmètre, une durée,
un nombre maximal d'usages et des conditions d'admission. Il sert uniquement
à l'admission prévue et ne remplace ni l'attestation, ni le certificat, ni
l'autorisation de communication. Aucun secret partagé sans limite n'est
fourni par défaut. Sa consommation concurrente respecte l'atomicité et
l'idempotence et son contenu n'est exposé ni dans les diagnostics ni dans
les lignes de commande journalisées.

La révocation ou l'expiration du jeton interdit les nouveaux enrôlements.
Le retrait des pairs déjà admis est une opération de révocation distincte,
explicite et traçable. Les affectations initiales à des groupes ne confèrent
que les permissions autorisées dans le mandat d'admission.

Un pair éphémère possède une politique de fin de vie déclarée. Sa disparition
entraîne une révocation et un retrait contrôlés des cartes, routes et noms,
avec les traces et tombstones requis ; aucun délai de suppression NetBird
n'est repris implicitement. Une reprise ne ressuscite pas son ancien accès.
Les règles de durée, de renouvellement et de nettoyage relèvent de A11.

## Adressage et résolution de noms

Le plan d'adressage overlay est configurable, distinct des réseaux physiques
et rattaché au domaine réseau déclaré. Il garantit l'unicité dans le périmètre
où elle est requise et détecte les collisions, chevauchements et boucles.
Il ne reprend pas automatiquement la plage CGNAT de NetBird. A06a, option A
validée par le développeur le 5 octobre 2026, retient IPv4 et IPv6 dès le
socle : contrats, adresses, routes, filtrage et qualification prennent en
charge les deux familles. Chaque profil active IPv4, IPv6 ou les deux selon
sa configuration explicite ; une famille non activée n'ouvre aucun accès PZT.
La famille des adresses overlay est distincte de celle des endpoints du
transport physique ; aucune connexion Internet IPv6 n'est imposée.
Le développeur précise que la prise en charge IPv6 doit être simplement
désactivable dans PZT. Un réglage unique « IPv6 activé », présenté par le
module PBO dans le périmètre administré, contrôle l'usage IPv6 de ce PZT.
Sa valeur est persistée et versionnée ; PBO distingue l'état souhaité de
l'état appliqué et rapporte les écarts. Le réglage respecte les permissions
et délégations du périmètre ; ses valeurs par défaut restent à préciser.

Lorsqu'il est désactivé, PZT retire ses adresses, routes, annonces et
autorisations IPv6, cesse de publier ses propres enregistrements AAAA et
ferme ses échanges IPv6 concernés. Il ne sélectionne plus d'endpoint IPv6
pour WireGuard, TLS d'amorçage ou TLS mutuel local. Le retrait concerne
uniquement les ressources PZT gérées ; l'IPv6 du système hôte et les ressources
de l'opérateur ne sont pas désactivés ou modifiés implicitement. Une voie
IPv4 autorisée est nécessaire à la continuité ; à défaut, les accès concernés
restent bloqués avec diagnostic explicite, sans repli hors PZT ni activation
implicite d'IPv4. La désactivation suit un plan vérifié et contrôle les sessions
existantes ; l'interface n'affiche pas un succès avant preuve du retrait.
La réactivation demande la réconciliation et la validation des permissions,
routes et preuves courantes, sans restaurer des droits périmés.

Les deux chemins appliquent les mêmes exigences de permission, de posture
et de révocation, sans repli hors PZT. A06b, option A validée par le
développeur le 5 octobre 2026, retient un plan privé configurable et
l'allocation automatique par l'autorité compétente, avec contrôles de
collisions. L'interconnexion de domaines doit respecter le plan et
les permissions déclarés. Un chevauchement non résolu bloque la route concernée.

Le DNS privé fournit les noms de pairs et de services autorisés, les zones,
résolveurs, règles par domaine et délais de fraîcheur déclarés. Un nom DNS
n'est pas une preuve d'identité ; sa résolution est confrontée à la destination
et à la liaison de clé attendues. Les changements retirent les noms et routes
invalidés sans maintenir silencieusement un accès supprimé.

Les réponses et caches respectent la visibilité par contexte et la rétention.
Les modes de résolution administrés ou laissés au système sont explicites
et leur coexistence est qualifiée. La gestion du DNS ne remplace pas sans
mandat les paramètres de l'hôte ni n'impose un résolveur public. A06c,
option B validée le 5 octobre 2026, retient un DNS Pixs développé et géré
par un module essentiel PBO, disponible à PZT et tous les PA selon leurs
permissions. Les contrats de publication et de consommation, le cycle de
vie et les limites de continuité sont précisés dans A06c ; placement,
interfaces et délais restent à définir et à qualifier.

## Politiques réseau et posture

Une politique décrit ses sources et destinations canoniques, les groupes
ou selectors autorisés, le service, la direction, les protocoles, les ports,
le contexte, la validité et les conditions de posture. Les groupes réseau
ne créent pas automatiquement des appartenances ou droits métier Pixs.
Le refus explicite prévaut, puis l'autorisation explicite, puis le refus
par défaut. La création d'une instance ou d'un groupe n'ouvre aucun maillage
général. Les directions d'initiation et le trafic de réponse sont spécifiés.

Les AllowedIPs WireGuard associent les adresses aux clés des pairs ; ils
ne constituent pas une autorisation par port ou par service applicatif.
Le PA applique les contrôles complémentaires sur les flux entrants,
sortants et transférés selon le profil et vérifie leur état réel. Une règle
autorisant une ressource derrière une passerelle n'autorise pas les services
locaux de la passerelle. Les états de connexion existants sont invalidés
conformément aux délais de révocation, sans exception générale pour les
flux déjà établis. A04b, option A validée par le développeur le 5 octobre
2026, retient nftables sous Linux et Windows Filtering Platform sous Windows,
pilotés par des adapters PA avec un contrat commun de politiques PZT.
Chaque adapter traduit les règles et vérifie leur application effective sur
les flux de son profil. Les ressources PZT sont identifiées séparément et
leur coexistence avec les règles de l'opérateur est qualifiée ; aucun
remplacement global du pare-feu existant n'est autorisé implicitement.
Les versions, bibliothèques, interfaces de pilotage, privilèges et frontières
Docker/LXC restent à préciser et qualifier. Cette décision ne prouve pas
l'équivalence des capacités des deux plateformes ni la fermeture après panne,
qui relève de A05.

A04a, option A validée par le développeur le 5 octobre 2026, confie à
`pzt-daemon` la gestion permanente des interfaces WireGuard, routes, règles
de filtrage et ressources DNS PZT de son périmètre. Les six autres modes
du PA lui soumettent leurs demandes autorisées sans modifier directement
ces ressources. Un propriétaire est identifié par périmètre ; cette décision
n'accorde aucun droit implicite sur un hôte ou sur les ressources d'une autre
instance. Les ressources administrées par l'opérateur restent distinctes.
Les demandes internes sont authentifiées, autorisées et traçables selon un
contrat à spécifier. L'indisponibilité du propriétaire n'autorise aucune
prise de contrôle implicite par un autre mode ; A05 précise la protection
des accès actifs et la reprise après panne.

La posture peut porter sur la version du PA, le système, la présence de
protections requises et le contexte réseau. Chaque donnée indique son origine,
son niveau de confiance et sa fraîcheur. Une information rapportée par PA
n'est pas présentée comme une mesure matériellement attestée. Les évaluations
à l'admission, après modification et pendant les sessions respectent les
délais déclarés ; une preuve requise absente ou non vérifiable bloque l'accès
concerné. La posture complète l'attestation TPM sans la remplacer.

A05a, option A validée par le développeur le 5 octobre 2026, retient le
modèle hybride avec autorisations de durée bornée et protection indépendante
du processus PA. Après perte du contact avec l'autorité, seules les permissions
déjà accordées, encore vérifiables et réutilisables selon leur classe restent
applicables jusqu'à leur échéance, sans renouvellement implicite ni période
de grâce. Une révocation connue est appliquée dans le délai déclaré sans
attendre l'expiration. Les classes exigeant une décision en ligne la conservent.

Un profil qualifie l'expiration et la révocation même si PA est arrêté ou
planté alors que les tunnels et filtres du noyau subsistent. Le mécanisme
indépendant applique uniquement les expirations, retraits ou fermetures
préautorisés du périmètre PZT ; il n'accorde aucun accès, ne renouvelle aucune
permission et ne prend pas la gestion générale des ressources de `pzt-daemon`.
Sa réalisation, son propre comportement après panne et les délais A05b sont
à qualifier. Le redémarrage ne réactive aucun accès expiré ou révoqué et
nécessite une réconciliation vérifiée. Aucune expiration automatique des
configurations WireGuard n'est présumée.

## Passerelles et ressources sans PA

Un rôle explicite permet d'accéder à des ressources déclarées par IP, préfixe
ou domaine depuis l'overlay, sans PA sur leur destination finale. L'annonce
d'une route et sa distribution ne valent pas permission d'accès. Les droits
de consommer et de fournir une ressource sont vérifiés séparément. Une
passerelle ne devient ni une autorité ni un relais par sa seule présence.

Le relais transporte le tunnel chiffré entre ses pairs ; la passerelle termine
un tunnel puis transfère des paquets vers une autre ressource. Le chiffrement
WireGuard couvre alors le segment jusqu'à la passerelle. La protection du
dernier segment et l'authentification du service final sont déclarées ; si
le profil exige le chiffrement jusqu'à la ressource, une protection applicative
ou un pair WireGuard à destination est nécessaire. L'attestation de la
passerelle ne constitue pas celle de l'équipement sans PA.

Le profil spécifie les routes de retour, la conservation ou traduction des
adresses sources, les frontières de confiance et la traçabilité. Les routes
larges exigent un mandat explicite. Les règles contre le contournement, les
chevauchements et les boucles couvrent aussi IPv6 lorsque pris en charge.

Plusieurs passerelles peuvent desservir une ressource. La sélection tient
compte des contraintes du profil et n'est pas confondue avec un équilibrage
de charge. Les conséquences du changement de passerelle sur les sessions,
notamment avec traduction d'adresses, sont documentées et testées. Leur
redondance ne remplace pas le consensus des autorités. A08a, option A
validée le 5 octobre 2026, réserve leur livraison à un profil ultérieur
après qualification du socle initial. A08b est soumis pour l'adressage source
et les retours ; le basculement reste à débattre dans A08c.

## Validation hybride selon la sensibilité

Le principe validé combine une décision en ligne et des autorisations signées
de courte durée selon la sensibilité. Chaque communication possède une preuve
d'autorisation d'une autorité compétente ; chaque paquet ne nécessite pas
une consultation centrale.

| Profil proposé | Validation |
| --- | --- |
| Courant | Autorisation signée courte, vérifiée localement par les pairs. |
| Protégé | Autorisation courte avec exigences renforcées de fraîcheur, de révocation et de renouvellement. |
| Critique | Décision en ligne avant la session ou l'opération concernée ; une approbation collective peut être requise par la politique. |

Les profils Courant, Protégé et Critique et leurs premiers objectifs de
délai sont retenus dans A05b, premier jet validé par le développeur le
5 octobre 2026. L'affectation précise des communications, les seuils de
sensibilité et la durée d'exécution des mandats restent à spécifier. Les
objectifs validés doivent encore être démontrés par qualification.

Le contenu proposé d'une autorisation comprend : émetteur, bénéficiaire,
destination, service, direction, périmètre, conditions, validité, identifiant
unique, versions de politique et de délégation, et liaison à l'identité
cryptographique du bénéficiaire. Son format reste à définir.

Une autorisation de canal ne remplace pas le contrôle des opérations qui y
circulent. Une opération critique peut nécessiter une nouvelle décision même
si le canal existe déjà. Les protections contre le rejeu et les changements
de contexte sont prévues dans le futur protocole.

Une autorisation courte borne la durée d'accès ; elle ne garantit pas seule
une révocation immédiate. Les sessions persistantes ne prolongent pas
indéfiniment une permission expirée. Une fraîcheur ou une révocation non
vérifiable conduit au refus de l'opération concernée.

### Révocation et référence temporelle

La politique définit la propagation des révocations, l'invalidation des caches,
la fermeture des sessions et la réévaluation des instructions en attente.
Une preuve conservée localement ne prolonge pas silencieusement un accès
révoqué, une délégation expirée ou une version de politique dépassée.

Les instants contractuels sont exprimés en UTC. La source de temps, les écarts
tolérés, les fenêtres de validité et la fraîcheur maximale sont déclarés.
Un temps non fiable ou des conditions temporelles non vérifiables conduisent
au refus de l'opération concernée, sans période de grâce permissive implicite.

Les mesures monotones des délais de lancement ou durées d'arrêt du PA sont
distinctes des instants UTC de validité des mandats. Elles ne remplacent pas
la référence temporelle nécessaire à l'autorisation.

Les délais maximaux de propagation, d'invalidation, de renouvellement et de
fermeture des accès sont des objectifs explicites par profil. Leur qualification
couvre aussi les partitions, les redémarrages et les connexions persistantes.

## Chiffrement et relais

Tous les échanges réseau entre pairs sont authentifiés et chiffrés, y compris
les communications des autorités, de découverte, de rendez-vous et de
synchronisation. Les données restent chiffrées de bout en bout entre les
pairs destinataires, y compris lorsqu'un relais est utilisé.

Le relais ne dispose pas des clés permettant de lire les données transportées.
Il peut observer les métadonnées nécessaires à l'acheminement ; leur exposition
et leur rétention sont limitées. Le passage du direct au relais ne change ni
les identités, ni le périmètre autorisé.

L'accès aux relais est contrôlé afin qu'ils ne deviennent pas des services
ouverts de transit. Leur sélection tient compte de la disponibilité, du chemin,
de la capacité et des contraintes de résidence.

Le protocole réutilise des primitives cryptographiques et des bibliothèques
éprouvées. L'authentification mutuelle, le renouvellement des clés de session
et la confidentialité persistante après compromission ultérieure d'une clé
font partie du design à préciser ; aucune cryptographie propriétaire n'est
retenue dans cette rédaction.

Le relais ZTP transfère les paquets WireGuard sans disposer des clés privées
des pairs. Son autorisation de transport est liée aux identités, au périmètre
et à une validité bornée. Un repli sur TCP ou WebSocket transporte ces paquets
via un adapter ZTP à qualifier ; WireGuard n'offre pas nativement un mode TCP.
Le choix ICE/STUN et du transport de relais figure dans A09. Aucune brique
NetBird de signalisation ou de relais n'est utilisée pour leur réalisation.

## Granularité des pairs

| Granularité | Périmètre d'exposition |
| --- | --- |
| Machine | Les interfaces ou réseaux explicitement déclarés de l'hôte. |
| VM ou conteneur | Un environnement isolé identifié. |
| Instance Pixs | Les capacités réseau déclarées d'une installation. |
| Service applicatif | Un service précisément identifié, avec ses relations propres. |

Le contrôle réseau d'une machine peut limiter les destinations et protocoles,
mais ne prouve pas l'identité de chaque application qu'elle héberge.
L'identification d'un service exige une identité distincte et un point de
contrôle adapté : intégration au service, proxy ou agent avec identification
vérifiée du processus. Un numéro de port ou une étiquette déclarée par le
client ne suffit pas. Le PA porte ou coordonne ce point de contrôle selon
le mode d'intégration retenu.

L'isolation d'un service dépend aussi de la frontière fournie par l'hôte.
Le réseau ne promet pas de protéger un service contre un administrateur qui
contrôle entièrement son environnement d'exécution.

Les permissions de transport et les permissions métier restent distinctes.
Le droit de joindre une API n'autorise pas toutes ses actions ni toutes les
données qu'elle peut traiter.

## Privilèges et exposition réseau

Chaque profil déclare ses interfaces, ports, protocoles, réseaux exposés et
privilèges système nécessaires. Les frontières d'accès sont vérifiées avant
mise en service. Un profil nouveau ne rend pas publics les workers, schedulers,
stores de coordination ou interfaces de management existants.

L'exécution utilise le moindre privilège. Les fonctions nécessitant des droits
système élevés sont limitées, justifiées et isolées autant que possible.
L'API PBO ne reçoit pas automatiquement les privilèges réseau du PA. Le
contrôle d'une machine n'accorde pas une exécution arbitraire de commandes
système hors des opérations et mandats déclarés.

La distribution précise les droits, ressources persistantes et adaptations
nécessaires pour Debian, Docker et le développement. Les choix du runtime PA
et de son déploiement restent explicites ; ils ne remplacent pas la pile
applicative de référence Django, PostgreSQL et TanStack du PBO.

## Intégration avec Pixs et ses données

Le destinataire conserve l'évaluation applicative des droits par Django.
L'identité distante est résolue explicitement vers le contexte d'identité
Pixs et son périmètre. Un tenant ou scope transmis par un pair ne devient pas
automatiquement une référence canonique locale.

Les échanges métier utilisent des contrats déclarés. La propriété des
ressources, les règles de confidentialité, de résidence, de suppression et
d'audit suivent les données et leurs projections. Le réseau ne crée pas de
réplication générale ou d'accès SQL interinstance implicite.

Le profil PDP minimal v1 actuel refuse l'intertenant. Le réseau ne contourne
pas cette limite ; une capacité métier nécessitant des échanges intertenants
demande un cadrage OpenSpec adapté et une autorisation distincte.

Les profils web, worker et scheduler conservent leurs frontières d'exposition.
Les nouveaux services de contrôle sont explicitement déclarés et protégés ;
leur présence ne rend pas publics les services privés existants.

Le placement côté PBO est fixé par le module officiel ZTP décrit ci-dessus.
Le détail des sous-modules, providers et profils d'exécution du PA reste à
définir en respectant le Kernel agnostique. WireGuard est la base logicielle
du transport IP. Les orchestrateurs, stores de consensus, adapters et autres
outils ne sont pas imposés implicitement au Kernel ou au socle Pixs ; leurs
choix suivent les arbitrages et profils déclarés.

La qualification des déploiements distingue PA seul, le cohébergement PBO–PA
sur un hôte, les conteneurs séparés et le conteneur commun. Un conteneur commun
exige un profil et un adapter explicitement validés ; il ne découle pas d'un
lancement implicite des rôles PBO. Chaque profil précise ses modes, comptes,
signaux, budgets d'arrêt, persistance et capacités désactivées. Un profil non
qualifié n'est pas présenté comme supporté.

## Sauvegarde et restauration

La stratégie couvre séparément l'état des autorités, les configurations,
les opérations et checkpoints, les audits et les mécanismes de protection
des clés. Chaque périmètre déclare sa rétention, son accès, sa résidence,
ses objectifs de perte acceptable et de délai de reprise, ainsi que la preuve
attendue après restauration.

Une restauration commence en état contrôlé. Elle vérifie les versions,
la cohérence des états et les décisions de révocation intervenues depuis la
sauvegarde avant toute exposition ou réintégration. Elle ne réactive aucun
droit révoqué ; si l'état courant ne peut pas être établi, les fonctions
protégées restent bloquées.

Les tombstones, décisions d'effacement, restrictions et rétentions applicables
sont réconciliés. Les opérations non terminées reprennent de manière idempotente
sans réémission automatique d'effets confirmés. Une sauvegarde ne devient
pas une nouvelle autorité et une restauration ne réinitialise pas les identités
ou permissions pour masquer un écart.

Les procédures sont testées dans un environnement isolé et produisent une
preuve auditable. Les sauvegardes de clés et leurs mécanismes de récupération
respectent leurs protections propres ; aucune clé privée n'est incorporée
aux artefacts applicatifs ou aux rapports.

La reprise distingue les opérations non commencées, en cours, interrompues
et terminées. Un résultat inconnu ne constitue ni un succès ni une preuve
d'absence d'effet. Une action non idempotente n'est pas rejouée sans stratégie
de reprise validée. La reconnexion à plusieurs PBO conserve l'isolation des
relations et refuse les instructions incompatibles sans priorité implicite
au dernier message reçu.

## Limites et quotas

Les enrôlements, requêtes de découverte, sessions, débits des relais, tailles
des messages et profondeurs de délégation sont bornés par des politiques
déclarées. Chaque limite précise son unité, son périmètre, sa période ou sa
durée, sa stratégie d'agrégation et le comportement en cas de dépassement.

Une autorisation ne donne pas une capacité de consommation illimitée. Les
limites applicables à plusieurs périmètres sont cumulatives. Les quotas
durables et réservations utilisent les garanties persistantes, atomiques
et idempotentes prévues par Pixs, avec réconciliation après reprise ou annulation.
Le comptage réseau de haute fréquence dispose d'un contrat adapté, sans
transformer chaque paquet en transaction applicative obligatoire.

Les refus et indisponibilités produisent des erreurs stables et diagnostiquables.
Un quota ou un entitlement ne remplace pas l'autorisation et un contrôle non
vérifiable n'accorde pas une consommation protégée implicite. Les valeurs
et méthodes de mesure restent à définir par profil.

## Performance et observabilité

La priorité est un chemin direct entre pairs autorisés, sans transit métier
obligatoire par les autorités. Les autorisations réutilisables restent bornées
par les exigences de sécurité ; la performance ne justifie pas un repli
permissif.

WireGuard est la base logicielle retenue pour le transport IP. QUIC avec
TLS 1.3 peut être étudié comme protocole applicatif au-dessus de ce transport,
sans devenir une base concurrente implicite. ICE, STUN et TURN constituent
des références de connectivité ; les mécanismes ZTP sont développés dans Pixs
et leurs bibliothèques, encapsulations et combinaisons restent à qualifier.
Aucune supériorité de performance n'est démontrée à ce stade.

Les mesures prévues couvrent latence d'autorisation et d'établissement, débit,
CPU, mémoire, pertes, MTU, proportion de chemins directs, capacité des relais,
temps de convergence et délai de révocation. Les objectifs chiffrés restent
à fixer par release ou profil. Chaque objectif précise son périmètre, sa
méthode, son seuil, sa période d'évaluation et sa version. La qualification
produit une preuve reproductible ou un diagnostic d'insatisfaction ; une
mesure locale ne constitue pas une garantie générale du réseau.

Les objectifs couvrent également la disponibilité, la reprise et la
compatibilité. Aucun seuil universel n'est déduit du runtime ou inventé
pour l'ensemble des déploiements.

Les diagnostics distinguent refus de politique, identité invalide, autorisation
expirée, perte de quorum, destination indisponible et recours au relais.
Ils permettent la corrélation des décisions sans exposer de clé, de jeton,
de secret ou de donnée personnelle dans les journaux techniques.

Les métriques, traces et journaux techniques sont distincts du diagnostic
opérateur et de l'audit fonctionnel persistant. La corrélation relie le PBO,
les autorités et les PA, avec trace_id, correlation_id et causalité lorsque
pertinents ; la propagation suit W3C Trace Context lorsque le transport
le permet. Ces références ne constituent jamais une preuve d'identité.

Les métriques emploient des labels à cardinalité bornée. Les signaux respectent
la minimisation, la pseudonymisation et des rétentions séparées ; les accès
tenant-scoped ou plateforme restent explicitement autorisés. L'audit des
opérations de gestion et de sécurité conserve l'acteur, le périmètre, les
versions utiles, la décision et le résultat sans copier les payloads sensibles.
Une panne de collecte technique est diagnostiquée et ne supprime pas une
obligation d'audit requise pour autoriser une opération.

## Interface PBO

Le module et ses sous-modules déclarent leurs contributions frontend dans
leurs manifests communs. Routes, navigation, formulaires et points d'extension
restent namespacés, versionnés, composés au build et soumis aux contrats du
shell TanStack. L'interface ne charge pas implicitement du code distant pour
activer une contribution.

Les textes sont traduits par les catalogues du composant propriétaire, avec
le catalogue canonique anglais prévu par Pixs. L'interface utilise le Design
System, les modes Light et Dark, le responsive et la cible WCAG 2.2 AA.
Une vue de topologie graphique possède une alternative lisible et accessible,
notamment sous forme de liste ou de tableau, permettant les mêmes opérations.

Les permissions d'affichage ne remplacent pas les contrôles Django. Les clés
de cache et états de l'interface respectent l'identité, le tenant et le scope ;
un changement de contexte invalide les données dépendantes. L'état demandé,
l'état appliqué et les opérations en cours sont présentés distinctement,
sans afficher de clé privée ni de token brut.

## Validation future de la conception

Les scénarios suivants sont retenus comme critères de validation future.
Ils ne constituent pas des tests déjà exécutés.

Les exigences WireGuard et capacités inspirées de NetBird ajoutent les
scénarios suivants. Les alternatives A01 à A12 sont qualifiées seulement
après leur décision et leur spécification ; aucune recommandation n'est
considérée comme un résultat de recette.

- Démarrage à froid, admission, renouvellement et basculement réussissent
  avec les services de l'éditeur injoignables et les services locaux requis disponibles.
- Un pair reçoit uniquement sa carte réseau autorisée ; une carte altérée,
  périmée, destinée à un autre pair ou à une ancienne liaison de clé est refusée.
- Une rupture de séquence déclenche une réconciliation sans réintroduire
  les pairs ou permissions révoqués.
- Une clé WireGuard valide ou des AllowedIPs larges ne permettent pas
  d'accéder à un protocole, port ou service non autorisé.
- La révocation d'un jeton bloque les nouvelles admissions ; la révocation
  d'un pair retire ses accès indépendamment du jeton utilisé à l'installation.
- Le chemin direct et le relais conservent les identités et permissions ;
  le relais ne peut déchiffrer les données WireGuard.
- Un changement d'endpoint conserve l'identité et réévalue les conditions
  dépendant de la localisation ou de la posture lorsqu'elles sont requises.
- Le DNS privé respecte la visibilité, refuse les destinations inattendues
  et retire les noms ou routes invalidés ; un conflit bloque le périmètre concerné.
- Une posture déclarée ne constitue pas une attestation TPM ; une preuve
  requise non vérifiable bloque l'accès selon le profil.
- Un flux déjà établi cesse après révocation dans le délai déclaré, y compris
  si PA plante et que le noyau conserve une interface active.
- Une configuration réseau partielle ou concurrente reste diagnostiquable
  et n'ouvre aucune fenêtre permissive.
- Une passerelle ne donne pas accès à ses services locaux ; les ressources
  sans PA ont un dernier segment protégé conformément au profil.
- Le basculement de passerelle respecte les contraintes de résidence et
  documente les pertes ou réinitialisations des sessions, sans promesse implicite de continuité.
- Le retrait d'un pair éphémère enlève ses accès, routes et noms tout en
  préservant les traces requises et sans résurrection après restauration.
- Le profil local et l'amorçage retenus restent dans PZT, avec leurs contrôles,
  même avant la disponibilité du transport WireGuard courant.

- Une instance autonome fonctionne sans autorité Pixs extérieure.
- Le PA exécute ZTP conformément à sa configuration et à ses mandats.
- Le mode `pzt-daemon` démarre sans délai au démarrage du système ou du
  conteneur et assure la convergence et la réconciliation de ZTP si celui-ci
  est activé et configuré sur ce PA ; sinon, il se ferme. Les délais de
  system-daemon et de session-daemon restent respectés.
- Une instruction de contrôle ou de configuration reçue depuis le PBO sans
  permission valide est refusée par le PA.
- Une composition PBO déclarant le pilotage ZTP sans son socle requis est
  refusée ; le retrait ou la désactivation du socle dans ce profil est bloqué.
- Un sous-module peut enrichir le pilotage sans modifier les implémentations
  privées ; une extension affaiblissant un contrôle obligatoire est refusée.
- L'administration locale authentifiée permet une reprise contrôlée lorsque
  les chemins distants sont indisponibles, via un transport local ZTP sans
  contournement des permissions.
- Tous les échanges PBO–PA restent dans ZTP sur le même hôte ou dans le même
  conteneur ; toute tentative de canal hors ZTP est refusée.
- Un ZTP non initialisé ou non vérifiable bloque les échanges PBO–PA, y compris
  pendant l'amorçage, sans repli vers un canal de secours hors ZTP.
- Un certificat valide sans permission de communication est refusé.
- L'intégration d'un PA enregistre la clé publique TPM de référence et le
  nom de l'hôte, avec leur rattachement vérifié à l'identité du PA.
- Chaque connexion ou reconnexion vérifie une attestation fraîche couvrant
  les mesures d'intégrité requises du PA ; une preuve rejouée, une mesure
  non conforme ou une preuve requise non vérifiable bloque la connexion.
- Une signature TPM valide sans mesures de confiance couvrant le PA ne
  constitue pas une preuve de son intégrité ; une attestation valide ne
  remplace pas l'authentification ni les autorisations ZTP.
- Des PA en conteneurs partageant un TPM conservent leurs identités distinctes
  et un rattachement vérifiable à leur hôte ; un profil sans TPM ou à TPM
  logiciel ou virtuel n'est pas présenté automatiquement comme matériellement
  attesté.
- Deux pairs d'une même tranche ne communiquent pas sans autorisation.
- Une délégation dépassant le mandat de l'émetteur est refusée.
- Un chemin direct est privilégié lorsqu'il est disponible et autorisé.
- Le relais permet le même échange sans accéder au contenu en clair.
- Une identité de service ne donne pas accès aux autres services de l'hôte.
- Une opération critique exige sa décision même sur un canal déjà établi.
- Expiration, révocation et perte de fraîcheur interrompent les accès concernés
  selon des délais et règles explicitement définis.
- Les membres d'une autorité reprennent après panne sans réintroduire de droits
  révoqués ni accepter un état périmé comme courant.
- Une partition réseau respecte le comportement arbitré pour les changements
  critiques et ne déclenche pas de passage automatique au mode autonome.
- Une communication autorisée ne contourne ni les droits métier ni les
  contraintes tenant, scope et résidence.
- Une configuration reçue ne devient appliquée qu'après confirmation
  vérifiable ; un conflit ou une application partielle reste diagnostiquable.
- Une reconfiguration réseau préserve ou valide son canal de contrôle ; une
  compensation ne réactive aucun droit invalidé et ne contourne pas ZTP.
- Une opération de gestion rejouée ne produit aucun double effet ; son mandat
  est réévalué avant exécution et son suivi survit au redémarrage.
- Une restauration ne réactive aucun droit révoqué après la sauvegarde et
  n'expose pas le service avant réconciliation des états de sécurité.
- Les privilèges du PA restent limités au rôle déclaré et ne sont pas transmis
  implicitement à l'API PBO.
- Les limites et quotas sont appliqués sans transformer une autorisation
  en consommation illimitée ni compter deux fois une opération rejouée.

### Matrice de qualification ZTP

Chaque profil déclare ses scénarios applicables et les preuves attendues.
La matrice distingue tests de contrat, d'intégration, de sécurité, de reprise,
de packaging et d'interface. Les environnements sont dédiés ; les fixtures
et identités sont synthétiques, sans secret ni donnée de production.

| Domaine | Scénarios de qualification |
| --- | --- |
| Connectivité | Chemins directs et relayés, NAT, transports bloqués et changement de chemin avec mêmes contrôles. |
| WireGuard et politiques | Backends qualifiés, AllowedIPs, routes et filtres distincts, absence d'accès général, rotation et retrait des liaisons de clés. |
| Plateformes PA | Linux/Windows physiques et VM, Docker/LXC Proxmox ; noyau effectif, backends et privilèges par profil, clones, snapshots, migration et preuves TPM/vTPM. |
| Carte réseau et admission | Visibilité limitée, versions, destinataire, ruptures de séquence, enrôlements concurrents, jetons bornés et retrait des pairs éphémères. |
| DNS et adressage | Collisions, chevauchements, réponses et caches par contexte, identité attendue et retrait des noms ou routes invalidés. |
| Posture et expiration locale | Origine et fraîcheur des preuves, évolution en session et blocage après crash de PA avec tunnels persistants. |
| Passerelles, si le profil est retenu | Accès aux ressources distinct des services locaux, NAT et routes de retour, protection du dernier segment et effets du basculement. |
| Autorités | Partitions, perte d'un membre, reconnexion, convergence et refus des décisions périmées selon le modèle arbitré. |
| Autorisations | Révocation en session, expiration, dérive temporelle, invalidation des caches et instructions en attente. |
| Attestation TPM du PA | Enrôlement de la clé publique et du nom d'hôte, liaison des clés d'identité et d'attestation, défis frais à chaque connexion et reconnexion, mesures du PA conformes ou altérées, rejeu, maintien de l'authentification, clés privées non exportées, conteneurs partageant un TPM et profils sans TPM matériel. |
| Reprise | Redémarrage, messages dupliqués ou désordonnés, checkpoints, restauration et absence de droits réintroduits. |
| Configuration | Versions concurrentes, refus d'une configuration invalide, application partielle et distinction entre état souhaité et appliqué. |
| Compatibilité | Coexistence des versions supportées, mise à niveau, migration, refus d'une combinaison incompatible et rollback autorisé. |
| Isolation | Services, tenants, scopes, branches, groupes de coopération, privilèges et visibilité de la découverte. |
| Distribution | Packaging Debian et Docker, configuration runtime, secrets externes, persistance, signaux et arrêt contrôlé. |
| Intégration PA | Sept modes d'exécution, dont `pzt-daemon` sans délai pour la convergence et la réconciliation de ZTP si activé et configuré sur ce PA, sinon fermeture ; provisionnement, initialisation minimale ZTP distincte des démons différés, fermeture bornée, sessions concurrentes, absence de PBO/PFO local, chaîne Python/C et états techniques de reprise. |
| Transport local | PBO et PA cohébergés, chiffrement et contrôles ZTP, refus des canaux hors ZTP, amorçage et reprise sans chemin distant. |
| Interface PBO | Parcours dans Chromium et Firefox headless déclarés dans DEVOPS.md, clavier, technologies d'assistance, traductions, Light/Dark et responsive. |
| Objectifs de service | Latence, débit, ressources, révocation, convergence et reprise selon les seuils et méthodes du profil. |

Les contrôles d'interface incluent des parcours manuels d'accessibilité lorsque
nécessaires. Une construction réussie ou un test Node ne remplace pas une
preuve de comportement dans les navigateurs déclarés. Un scénario non exécuté,
non applicable, indisponible ou échoué est signalé explicitement.

## Points restant à arbitrer

### Registre des choix WireGuard et capacités inspirées de NetBird

Le développeur a validé WireGuard comme base logicielle et le développement
propre à PZT/PA des capacités inspirées de NetBird. A01 est validé le
5 octobre 2026 : priorité aux backends natifs par OS et espace utilisateur
pour les profils qui le nécessitent. Cette décision ne valide pas les
versions, dépendances, privilèges ou résultats de qualification. A02, option A,
est validé le 5 octobre 2026 : canal TLS d'amorçage intégré à PZT, limité à
l'admission et aux preuves requises, avec ancrage de confiance préalable.
A03, option A, est validé le 5 octobre 2026 : TLS mutuel intégré à PZT pour
PBO et PA sur le même hôte d'exécution, avec maintien des contrôles PZT.
Les frontières distinctes des VM et conteneurs restent prises en compte.
A04a, option A, est validé le 5 octobre 2026 : `pzt-daemon` possède la gestion
permanente des ressources réseau PZT de son périmètre ; les autres modes
lui soumettent leurs demandes autorisées. A04b, option A, est validé le
5 octobre 2026 : nftables sous Linux et Windows Filtering Platform sous
Windows, adapters PA et contrat commun. Les interfaces et dépendances
exactes ainsi que les profils de coexistence restent à qualifier. A05a,
option A, est validé le 5 octobre 2026 : modèle hybride, autorisations bornées,
révocation connue sans attente d'expiration et protection indépendante de PA.
A05b est validé comme premier jet le 5 octobre 2026 : durées et objectifs
de renouvellement par classe, révocation en 5 secondes maximum si le PA
est joignable et fermeture de protection en 10 secondes maximum après panne.
Ces objectifs restent à qualifier sur chaque profil. A06a, option A, est
validé le 5 octobre 2026 : IPv4/IPv6 dès le socle et familles activées par
profil, avec réglage unique pour désactiver l'usage IPv6 de PZT sans modifier
l'IPv6 de l'hôte. A06b, option A, est validé le 5 octobre 2026 : pools privés
configurables et allocation par l'autorité compétente, avec contrôle des
collisions. A06c, option B, est validé le 5 octobre 2026 : DNS Pixs géré
par un module essentiel PBO, utilisable par PZT et tous les PA selon leurs
permissions. Placement, suffixes, TTL et bibliothèques restent ouverts.
A07a, option A, est validé le 5 octobre 2026 : contrôle HTTP/JSON avec
contrats OpenAPI versionnés pour PBO–PA et PA–PA. A07b, option A, est validé
le 5 octobre 2026 : snapshot initial, deltas ordonnés et reprise complète
en cas de désynchronisation. A07c, option B, est validé le 5 octobre
2026 : notifications et retours de suivi WebSocket/JSON, API HTTP conservées.
A07d option A est validée le 5 octobre 2026 pour les deltas JSON typés.
Les autres arbitrages sont présentés avec leurs alternatives pour le débat
au fil de la rédaction. Toute décision reçue est reportée dans les deux CdC,
avec sa date, son périmètre et ses conséquences ; une présélection de l'interface
ou l'absence de réponse ne vaut jamais validation.

| Référence et état | Alternatives et conséquences | Décision ou recommandation et statut |
| --- | --- | --- |
| A01 — Backend — validé le 5 octobre 2026 | Périmètre : Linux et Windows physiques et VM, Docker/LXC sous Proxmox. Versions, intégration et droits sont qualifiés séparément ; la décision ne prouve pas la compatibilité d'un profil. | Décision validée : priorité au noyau Linux et au backend natif Windows, dont WireGuardNT reste le candidat à qualifier ; espace utilisateur pour les profils qui le nécessitent, sans contournement des restrictions des conteneurs. |
| A02 — Amorçage — option A validée le 5 octobre 2026 | TLS authentifié intégré à PZT et limité à l'admission, retenu ; alternative du pair WireGuard préprovisionné non retenue comme mode d'amorçage de référence. | Décision validée : TLS d'amorçage intégré à PZT, ancrage de confiance préalable, preuves requises et paramètres publics WireGuard ; aucun accès métier avant admission. Formats, versions, bibliothèques et provisionnement restent à spécifier. |
| A03 — Transport local — option A validée le 5 octobre 2026 | TLS mutuel intégré à PZT retenu pour PBO et PA sur le même hôte d'exécution ; WireGuard local n'est pas exigé pour ce profil. | Décision validée : authentification mutuelle, permissions, attestation, révocation et audit PZT maintenus ; WireGuard interhôtes. VM et conteneurs distincts ne deviennent pas un même hôte d'exécution par cohébergement ; endpoints et isolation à qualifier. |
| A04 — Filtrage et propriété — A04a et A04b option A validées le 5 octobre 2026 | A04a : gestion permanente par pzt-daemon. A04b : adapters nftables Linux et Windows Filtering Platform Windows avec contrat commun ; le pilotage d'une couche pare-feu existante n'est pas retenu comme mécanisme de référence. | Décisions validées : un propriétaire par périmètre PZT et demandes autorisées des six autres modes sans écritures directes ; filtrage natif par OS, ressources PZT distinctes des règles de l'opérateur. Interfaces, dépendances, privilèges, coexistence et isolation restent à qualifier. |
| A05 — Expiration et panne — A05a option A et A05b premier jet validés le 5 octobre 2026 | Modèle hybride, autorisations de durée bornée et protection indépendante du processus PA ; objectifs initiaux par sensibilité détaillés ci-dessous. | Expiration opposable même après crash, révocation connue sans attente d'expiration, contrôle en ligne selon la classe et aucun élargissement par le mécanisme indépendant. Réalisation et objectifs A05b validés restent à qualifier. |
| A06 — Adressage et DNS — A06a/A06b option A et A06c option B validées le 5 octobre 2026 | A06a : IPv4/IPv6 dès le socle et réglage unique de désactivation IPv6 PZT. A06b : plan privé configurable et allocations par l'autorité compétente. A06c : DNS Pixs développé et géré par un module essentiel PBO, utilisable par PZT et tous les PA. | Décisions validées : pools IPv4 RFC 1918, IPv6 ULA /48 et conflits bloquants ; DNS accessible selon le contexte, publication et consultation distinctes par contrats publics. Aucun repli public des noms privés ; retraits et désactivation IPv6 contrôlés. Placement, interfaces, suffixes, TTL et bibliothèques restent à définir et à qualifier. |
| A07 — Contrats du contrôle — A07a/A07b option A et A07c option B validées le 5 octobre 2026, extension adaptative validée en principe ; A07c2 option A validée le 5 octobre 2026 ; A07d option A validée le 5 octobre 2026 | A07a : HTTP/JSON avec OpenAPI PBO–PA et PA–PA. A07b : snapshot initial, deltas ordonnés et reprise complète. A07c : WebSocket/JSON de référence, support SSE complémentaire et adaptation déterministe validés en principe ; commandes et lectures restent HTTP. A07c2 : table de règles prioritaires et seuils explicites pour sélectionner le mode, valeurs à calibrer. A07d : opérations métier JSON typées avec schémas versionnés retenues. | Décisions validées : contrats versionnés, idempotence, déduplication et reprise sans résurrection ni prolongation des droits ; curseurs distincts des preuves d'application, consommation et délais A05b à qualifier. Décision A07c2 option A validée le 5 octobre 2026 : règles prioritaires, seuils de bascule/retour distincts et stabilité, aucun contournement de sécurité ; valeurs et consommation à qualifier. Décision A07d option A validée le 5 octobre 2026 : opérations métier JSON typées, validation sémantique et audit ; catalogue, schémas et bibliothèques à définir et qualifier. |
| A08 — Passerelles — A08a option A validée le 5 octobre 2026 ; A08b soumis ; A08c à débattre | A08a : socle initial entre PA admis avec contrôle PBO, puis profil passerelle ultérieur. A08b : conservation des sources avec routes retour ; ou traduction source déclarée vers la passerelle. A08c : sélection et basculement. | Décision A08a validée : contrats et garanties des passerelles conservés, livraison après qualification du socle. Recommandation A08b : sources conservées si les retours sont maîtrisés, visibilité et corrélation explicites ; traduction alternative à qualifier sans repli automatique. Plateformes, NAT IPv6, privilèges et basculement restent ouverts. A08b non validé. |
| A09 — Connectivité et relais — à débattre | ICE/STUN avec signalisation propre à PZT ; ou un rendez-vous plus limité avec davantage de relais. Relais UDP ; ou ajout d'une encapsulation TCP/WebSocket pour réseaux restrictifs. | Primitives standards et bibliothèques indépendantes qualifiées, direct prioritaire et relais conservant le chiffrement WireGuard ; mesurer coûts et couverture des réseaux. |
| A10 — Identités, clés et attestation — à débattre | Identité de service au-dessus du tunnel hôte ; ou pairs/interfaces isolés par service. Certificats et formats de liaison à choisir. Déclencheurs TPM distincts des handshakes à définir. | Liaisons explicites des quatre identités/clés, clés privées locales, attestation fraîche à chaque connexion logique et contrôles supplémentaires par service selon son profil ; mapping exact à valider. |
| A11 — Admission et éphémères — à débattre | Validation opérateur ou admission automatisée par mandat préalable ; jetons à usage unique ou usages limités. Délais de présence, renouvellement et retrait à fixer. | Jetons bornés et admission mandatée, expiration du jeton distincte du retrait des pairs ; nettoyage traçable avec conservation de l'audit. |
| A12 — État autoritatif et multimaître — à débattre | État de gestion et décisions coordonnés autour de PostgreSQL ; ou capacité de consensus spécialisée validée avec source de vérité explicite. Signataires et preuves d'engagement à définir. | Cohérence forte des changements critiques, refus des décisions périmées et maintien des seules permissions encore vérifiables sans quorum ; ne pas présumer une HA à partir de la redondance de routage. |

### A05b — Objectifs initiaux validés, qualification requise

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026. Ces
valeurs sont les objectifs initiaux du CdC, à mesurer sur chaque profil ;
elles ne sont ni des performances démontrées ni des valeurs imposées par
WireGuard ou NetBird. Elles sont des paramètres documentés par profil dans
les limites retenues ; leur modification nécessite une décision explicite.
L'affectation détaillée des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

Les renouvellements exigent une nouvelle décision valide ; la répétition d'une
ancienne preuve ne remet pas un compteur à zéro. L'expiration n'ajoute aucune
période de grâce. L'UTC contractuel et la confiance temporelle restent requis.
Pause, reprise, snapshot et restauration doivent empêcher la réactivation
d'un accès périmé avant toute reprise des échanges. Un profil qui ne démontre
pas les délais retenus n'est pas déclaré conforme ; leur modification exige
une décision explicite documentée.

### A06b — Plan privé et allocation validés, qualification requise

L'option A, validée par le développeur le 5 octobre 2026, combine un plan
privé configurable et des allocations automatiques par l'autorité compétente.
Les pools IPv4 sont choisis dans
les plages privées [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) et validés
par l'opérateur, sans sous-réseau identique imposé à toutes les installations.
Pour IPv6, un préfixe ULA /48 est généré par domaine selon
[RFC 4193](https://www.rfc-editor.org/rfc/rfc4193), ou fourni par l'opérateur ;
la génération ne constitue pas une preuve d'absence de collision. Lorsque
IPv6 est désactivé pour ce PZT, aucune allocation IPv6 n'est activée sur PA.

Les allocations sont tracées, liées aux identités admises et conservées selon
le cycle de vie déclaré. Les vérifications couvrent les réseaux connus des
hôtes, LAN, VPN, Docker/LXC et les préfixes des domaines interconnectés avant
application des routes ; elles ne prétendent pas connaître tous les réseaux
externes. Un conflit bloque le périmètre concerné et appelle un plan explicite,
sans renumérotation, traduction d'adresses ou modification de l'hôte implicites.
La taille des pools IPv4, le découpage IPv6, la persistance, les délégations
d'allocation et la résolution des conflits restent à préciser ; A12 fixe
la cohérence autoritative requise.

Le provisionnement manuel de chaque adresse n'est pas retenu comme mode
de référence. Les contrôles de collisions et de permissions restent
obligatoires ; les pools concrets et la réalisation restent à qualifier.

### A06c — DNS Pixs géré par un module essentiel PBO, option B validée

L'option B est validée par le développeur le 5 octobre 2026 avec la précision
suivante : un DNS géré sera développé pour Pixs sous forme de module essentiel
du PBO, utilisable par PZT et par tous les PA. Le module administre les zones,
les enregistrements, les vues, les règles de résolution et leur cycle de vie.
Il possède ses données et expose des contrats publics versionnés au module
PZT ; aucun accès aux tables privées d'un autre module n'est admis. Sa capacité
DNS et ses dépendances obligatoires sont déclarées dans la composition des
profils qui l'utilisent ; une dépendance essentielle manquante bloque leur
activation ou leur readiness selon le contrat. Le Kernel conserve ses
responsabilités génériques. L'identifiant du module, les rôles d'exécution
du service DNS, leur placement et leur redondance restent à spécifier.

Tous les PA admis peuvent utiliser ce service dans leur périmètre autorisé
via PZT. La consultation, la publication, la modification et le retrait sont
des permissions distinctes ; être client DNS ne rend pas un PA administrateur
ou serveur DNS. Le module PZT publie et retire ses noms par les contrats
publics du module DNS, avec origine, contexte, version et audit. Les changements
administrés par PBO sont exécutés par les PA aux rôles déclarés et contrôlés
par les preuves d'état appliqué. Un échec ou une application partielle reste
visible et ne vaut pas succès. Les vues limitent la découverte aux noms
permis ; une résolution n'accorde aucun accès réseau ou métier et ne remplace
pas la vérification de l'identité et de la clé de destination.

Les adapters PA dirigent les requêtes des zones PZT vers le service DNS Pixs.
Les autres noms utilisent le DNS habituel du profil, sauf configuration
administrée explicitement. Développer un résolveur autonome dans chaque PA
n'est pas le mécanisme de référence retenu. Les interfaces Linux, Windows,
Docker et LXC, permissions et frontières d'écoute sont qualifiées séparément.
Les domaines de routage de [systemd-resolved](https://systemd.io/RESOLVED-VPNS/)
et les [règles NRPT Windows](https://learn.microsoft.com/en-us/powershell/module/dnsclient/add-dnsclientnrptrule)
restent des candidats. [Docker distingue le DNS hérité et son DNS embarqué](https://docs.docker.com/engine/network/#dns-services)
selon le profil réseau. Aucune interface, bibliothèque ou modification des
paramètres de l'hôte ou du conteneur n'est choisie implicitement.

Une panne DNS ne dirige pas les noms privés vers un résolveur public. Les
caches gérés ne servent aucun état au-delà de sa validité déclarée ; retraits,
révocations et désactivation IPv6 invalident les enregistrements et caches
PZT concernés, dont les AAAA propres à PZT. Les caches des applications sont
qualifiés séparément ; leur présence ne prolonge jamais une autorisation
réseau. L'indisponibilité du PBO n'autorise aucune nouvelle publication ni
prolongation : le service ne peut continuer sur son dernier état vérifié que
dans les limites déclarées, à qualifier. L'amorçage A02 doit disposer de
références d'endpoints et d'ancrages provisionnés sans dépendance circulaire
au DNS privé encore indisponible. Suffixes, TTL, protocoles DNS, persistance,
réplication et comportement des applications avec résolveur propre restent
à définir ; l'absence de fuite doit être démontrée.

### A07a — Contrats HTTP/JSON, option A validée

L'option A est validée par le développeur le 5 octobre 2026 : les échanges
applicatifs de contrôle PBO–PA et PA–PA utilisent HTTP avec messages JSON
et contrats OpenAPI versionnés, au-dessus des transports PZT déjà retenus.
Les contrats restent distincts selon leur propriétaire, rôle et périmètre.
Ce choix prolonge HTTP/REST OpenAPI pour les API de gestion PBO conformément
aux spécifications Pixs existantes. [OpenAPI décrit les API HTTP indépendamment du langage](https://spec.openapis.org/oas/latest.html).
Version majeure, schémas validés à l'exécution, erreurs stables, corrélation
et idempotence des commandes rejouables sont explicites. La qualification
couvre la chaîne PA Python/C et chaque plateforme ; les performances restent
à mesurer. Le RPC binaire n'est pas retenu comme mécanisme de référence
pour ces échanges de contrôle.

Le canal respecte A02/A03 et WireGuard interhôtes. L'identité, le contexte,
le mandat, la fraîcheur et l'autorisation restent vérifiés ; HTTP ne les
remplace pas. Les requêtes sont bornées et les erreurs n'exposent aucun secret.
Cette validation ne sélectionne aucune bibliothèque, version HTTP ou OpenAPI,
ni aucun format de certificat. A07b, option A validée le 5 octobre 2026,
fixe la distribution par snapshot initial et deltas ordonnés. A07c, option B
validée le 5 octobre 2026, retient WebSocket/JSON pour les notifications et
retours de suivi déclarés, sans remplacer les API HTTP de commande et lecture.

### A07b — Snapshot et deltas ordonnés, option A validée

L'option A est validée par le développeur le 5 octobre 2026 pour la
distribution des cartes réseau, configurations et politiques autorisées.
Un snapshot désigne ici un état complet de contrôle
limité au destinataire et à son contexte ; il est distinct d'un snapshot
de VM ou de conteneur. Les permissions A05 restent bornées indépendamment
du mécanisme de distribution.

Le mécanisme retenu combine un snapshot initial, des notifications de
changement et des deltas ordonnés représentant les modifications depuis une
révision de base explicitement identifiée. Chaque mise à jour porte son
identifiant, son producteur autorisé, le destinataire, le périmètre, la version
de contrat, les révisions de base et de résultat, la validité et les preuves
requises. L'ordre est défini par périmètre autoritatif ou partition déclaré,
sans supposer un ordre global entre toutes les autorités ; A12 reste ouvert.
Les événements annoncent uniquement des changements engagés. Les consommateurs
supportent les doublons sans double effet, conformément aux contrats Pixs ;
aucune livraison exactement une fois n'est promise.

PA vérifie la base et les preuves avant application. Un delta manquant,
contradictoire ou incompatible provoque une récupération d'état complet
vérifié ; un historique dépassant sa rétention ne rend pas le replay obligatoire.
La reprise après coupure ou redémarrage réconcilie aussi l'état effectivement
appliqué. La réception d'un message ne prouve pas l'application des interfaces,
routes, filtres ou paramètres DNS ; les erreurs et applications partielles
sont rapportées sans fenêtre permissive. Une réconciliation ne restaure
aucun droit expiré ou révoqué, et un changement de visibilité retire les
données et accès devenus interdits.

Une notification ne vaut pas autorisation et son rejeu ne renouvelle aucune
échéance. Les retraits vérifiés sont traités en priorité, sans attendre un
lot complet de modifications non critiques ; aucune révision antérieure ne
peut ensuite les annuler. Pendant une désynchronisation, aucune nouvelle
permission non vérifiable n'est appliquée ; seules les permissions encore
vérifiables peuvent subsister dans les limites A05, avec contrôle en ligne
pour les cas critiques. Les objectifs A05b, notamment la révocation en cinq
secondes sur un chemin qualifié, restent opposables et à mesurer de bout
en bout, récupération comprise.

Ce choix vise à limiter la retransmission d'états complets
lors de changements fréquents, tout en conservant une reprise explicite ;
il ajoute la gestion des révisions, doublons et trous de séquence. A07d,
option A validée le 5 octobre 2026, retient les opérations métier JSON typées
pour les deltas ; leurs schémas, catalogue et versions restent à spécifier.
Les preuves d'autorité et de validité restent requises.

La distribution de seuls états complets à chaque changement n'est pas
retenue comme mécanisme de référence. HTTP/JSON A07a reste applicable ;
A07c, option B validée le 5 octobre 2026, retient WebSocket pour les
notifications et retours de suivi. A07d option A est validée pour les deltas ;
fréquences, budgets, rétention, tailles et pagination restent à qualifier.

### A07c — Notifications WebSocket, option B validée

L'option B est validée par le développeur le 5 octobre 2026 : un canal
WebSocket avec messages JSON versionnés porte les notifications de contrôle
et leurs retours de suivi déclarés. Le PA ouvre la connexion vers un endpoint
PZT autorisé ; les rôles producteurs et consommateurs PA–PA sont déclarés.
Les commandes, rapports hors suivi et lectures de snapshots ou deltas
conservent les API HTTP/JSON A07a. Le retour de suivi peut accuser réception,
vérification ou application selon un type explicite ; recevoir un message
ne prouve pas l'application effective. Un abonnement n'ajoute aucun rôle,
droit ou visibilité. WebSocket demeure la référence ; le principe du support
SSE complémentaire avec adaptation déterministe est ensuite validé, avec
règles A07c2 option A validées le 5 octobre 2026.

[RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455) définit une communication
bidirectionnelle ; le contrat PZT précise les types de messages, versions,
identifiants, corrélation, périmètres et limites. Un curseur de reprise est
une position dans l'historique autorisé, distincte des révisions effectivement
appliquées. WebSocket ne fournit pas à lui seul la persistance, le replay,
la déduplication ou la preuve d'application. PZT assure les garanties A07b ;
un curseur inconnu, incompatible ou hors rétention appelle un état complet
vérifié. Les messages hors contexte, invalides ou expirés sont refusés.

La connexion et la reconnexion vérifient l'identité, le contexte, la fraîcheur
et les permissions selon A02/A03 et les transports PZT retenus. Les droits
sont réévalués pendant le canal ; leur perte ferme l'accès concerné selon
A05. Aucun secret n'est placé dans l'URL. Les heartbeats prouvent seulement
l'activité du canal et ne renouvellent aucune permission. Une vérification
périodique bornée de la révision autoritative détecte les notifications
perdues sans prolonger les droits. Fréquences, délais de reconnexion,
heartbeats, limites de file, tailles et règles de fermeture restent à définir.
Les retraits vérifiés sont prioritaires ; saturation et client lent produisent
un diagnostic et la réconciliation ou fermeture requise, sans retard
silencieux ni repli hors PZT. Aucun broker n'est sélectionné.

Le choix vise notamment l'économie des échanges de suivi fréquents dans
les deux sens. Aucun gain CPU, mémoire ou réseau n'est déclaré démontré.
La qualification compare WebSocket et une référence SSE/HTTP à charge,
messages, sécurité et garanties identiques, côté PA et PBO : repos, activité,
nombre de PA simultanés, rafales, clients lents, coupure et reprise. Les mesures
couvrent CPU, mémoire, connexions, files, octets transférés et latence jusqu'à
l'état appliqué ; les objectifs A05b restent opposables. Les commandes et
lectures restant HTTP dans les deux profils, leur coût est inclus.
La gestion des connexions longues doit éviter un worker bloquant dédié
par PA ; l'intégration asynchrone PBO et le client natif PA Python/C sont
qualifiés sur Linux/Windows physiques et VM, Docker/LXC Proxmox. Cette décision
ne sélectionne ni bibliothèque, version HTTP, serveur ou compression, ni
nouvelle dépendance. A07d option A est validée le 5 octobre 2026 pour les deltas JSON typés.

### A07c2 — Table de règles déterministes, option A validée

Après la validation de WebSocket, le développeur a demandé puis approuvé
le 5 octobre 2026 le principe de prise en charge SSE et WebSocket avec
adaptation déterministe. WebSocket demeure le mode de référence déjà validé.
La capacité SSE complémentaire suit les mêmes contrats JSON, identités,
permissions, validités et garanties A07b. En SSE, les retours de suivi passent
par HTTP/JSON ; en WebSocket, ils peuvent emprunter le canal bidirectionnel.
Commandes et lectures restent HTTP dans les deux cas. Le gain de ressources
n'est pas présumé et le double support ajoute une qualification et une
maintenance propres aux deux transports.

Une politique administrée, versionnée et auditée déclare les modes permis,
le mode éventuellement imposé, les critères de sélection et leur priorité.
La décision est prise par l'autorité de configuration compétente et appliquée
par PA ; une adaptation locale ne peut suivre que les règles explicitement
déléguées. Politique, mesures, fenêtre d'observation et état précédent doivent
permettre de reproduire la décision. Une négociation de capacité ou un
changement de mode n'accorde aucune nouvelle autorité ou permission.

L'option A est validée par le développeur le 5 octobre 2026 : une table
de règles prioritaires avec seuils explicites, calibrés par les mesures PA/PBO.
L'ordre retenu est le suivant :

| Priorité | Critère déterministe retenu | Résultat |
| --- | --- | --- |
| 1 | Un mode est imposé par une politique valide. | Utiliser ce mode s'il est admis et qualifié ; sinon échec explicite, sans dérogation automatique. |
| 2 | Capacité des deux extrémités, profil réseau et sécurité requis. | Éliminer les modes non déclarés, non autorisés ou non qualifiés pour le contexte et les délais A05b. |
| 3 | Échec vérifié propre au transport courant. | Utiliser l'autre mode seulement s'il reste autorisé et qualifié ; un refus d'identité, de permission ou de preuve ne déclenche aucun contournement. |
| 4 | Fréquence et volume des notifications/retours, CPU et mémoire PA/PBO, concurrence et budgets réseau, dans une fenêtre déclarée. | Appliquer la préférence du profil de coût mesuré. Une faible activité ne suffit pas à déclarer SSE moins cher, ni une forte activité WebSocket moins cher. |
| 5 | Seuil de bascule, seuil de retour et durée de stabilité distincts. | Éviter l'oscillation ; si les données de coût sont absentes ou trop anciennes, conserver le mode courant admis, ou WebSocket à l'initialisation, sans nouvelle permission. |

Les seuils, budgets, durée de fenêtre, fraîcheur des mesures et tables de coût
restent à débattre et à qualifier. La stabilisation des optimisations ne
retarde jamais une fermeture de sécurité ou le traitement d'un retrait.
Les coûts d'un mode inactif proviennent du profil qualifié ; le système
n'entretient pas deux canaux permanents pour les mesurer. La table de règles
permet une décision explicable et reproductible ; aucun gain de ressources
n'est déclaré mesuré.

Le score de coût pondéré, option B, n'est pas retenu comme mécanisme de
référence. La calibration des profils et valeurs reste requise avant de
déclarer une sélection adaptée à une plateforme ou charge donnée.

Un seul canal de notification reste actif en régime établi. Une éventuelle
courte coexistence lors de la transition est bornée, tracée et dédupliquée,
sans double application. La bascule conserve les révisions et identifiants,
distingue reçu/vérifié/appliqué, réauthentifie le nouveau canal et récupère
un état complet si nécessaire. Elle ne renouvelle aucun droit et ne restaure
aucun accès retiré. Coupures, saturation, changement de politique et bascule
sont qualifiés de bout en bout avec A05b ; un échec reste explicite et limité
par A05. Le support adaptatif et la table de règles A07c2 sont validés ;
les valeurs des seuils, budgets, fenêtres, limites de transition et
bibliothèques restent à définir et qualifier.

### A07d — Deltas par opérations métier JSON typées, option A validée

L'option A est validée par le développeur le 5 octobre 2026 : les deltas
utilisent des opérations métier typées en JSON et des contrats versionnés :
retirer un pair, mettre à jour une route ou remplacer une politique, par
exemple. Chaque opération cible un
objet par identité stable dans le contexte autorisé, porte un identifiant
permettant la déduplication et précise ses préconditions, ses données et
son résultat attendu. L'enveloppe A07b conserve autorité, destinataire,
révisions de base et de résultat, validité et preuves requises. Ces opérations
représentent des changements autoritatifs engagés ; elles ne constituent
pas des commandes arbitraires de l'hôte ni de nouvelles décisions d'autorité.

La validation sémantique et l'audit sont explicites sur la chaîne PA Python/C.
Les schémas et le catalogue sont à spécifier ; le traitement peut cibler
les objets concernés sans supposer
un gain de performance démontré. Une opération inconnue ou incompatible
n'est pas ignorée : la mise à jour est refusée avec diagnostic, puis un état
complet compatible est demandé. Si le contrat reste incompatible, le
périmètre demeure bloqué selon A05 et la matrice de compatibilité.

JSON Patch, option B, n'est pas retenu comme format de référence des deltas.
Les schémas, le catalogue d'opérations et leurs versions restent à spécifier
avant réalisation.

PA valide la modification avant activation et
rapporte l'état réellement appliqué, y compris un échec système partiel.
Une opération JSON valide ne prouve pas l'application des routes ou filtres.
Aucun droit expiré ou révoqué n'est restauré ; la cohérence des dépendances,
les retraits prioritaires et la reprise complète A07b restent applicables.
HTTP/JSON A07a et les modes de notification A07c/A07c2 sont conservés : ce choix
ne déplace pas le transfert des deltas vers le canal de notification.
Tailles, budgets, transactions de configuration, catalogue et bibliothèques
restent ouverts.
Ces modalités restent à qualifier ; A08a, option A validée le 5 octobre
2026, réserve le rôle passerelle à un profil ultérieur après le socle initial.

### A08a — Socle initial puis profil passerelle ultérieur, option A validée

Une passerelle est un PA dont le rôle autorisé permet de transférer des flux
PZT vers une ressource déclarée sans PA, par exemple une imprimante réseau
ou un service dans un sous-réseau distant. La permission de cette ressource
est distincte de l'accès aux services de la passerelle. La capacité de
référence fonctionnelle est décrite dans les [réseaux NetBird](https://docs.netbird.io/manage/networks) ;
sa réalisation est développée dans PZT/PA, selon les contrats Pixs.

L'option A est validée par le développeur le 5 octobre 2026 : le socle de
communication entre PA admis est qualifié d'abord, avec le contrôle PBO
déjà prévu ; l'exécution des passerelles est réservée à un profil ultérieur
explicitement qualifié. Le cahier des charges conserve leurs garanties et contrats ; leur
mise à disposition suit une décision de livraison distincte. Le premier
socle ne déclare pas accessibles via PZT des destinations sans PA. Cette
décision permet de qualifier d'abord admission, politiques,
expiration, révocation et reprises sur les plateformes demandées, puis
le transfert et la protection du dernier segment.

La livraison d'un profil passerelle dès la première réalisation, option B,
n'est pas retenue. Ses exigences restent définies pour le profil ultérieur.

Dans ce profil ultérieur, chaque ressource déclare destinations, protocoles,
ports, sens d'initiation et protection du dernier segment. Le chiffrement
WireGuard s'arrête à la passerelle si la destination n'est pas un pair ;
la protection du service final doit satisfaire son profil. Attester la
passerelle ne revient pas à attester la destination sans PA. Les routes,
droits et reprises respectent A05/A06 ; aucun chevauchement ou retrait connu
n'est contourné par le transfert. Une ressource qui exige des preuves que
ce profil ne peut fournir reste inaccessible.

Les sept modes PA conservent leurs responsabilités A04a ; le rôle passerelle
ne crée pas de mode supplémentaire ni de droits implicites sur l'hôte.
Linux/Windows physiques et VM, Docker/LXC Proxmox conservent leur périmètre
PA ; la capacité passerelle est déclarée et qualifiée séparément sur chaque
profil qui l'expose. Aucun montage, privilège, forwarding hôte ou configuration
Proxmox n'est modifié implicitement. A08a ne sélectionne pas le NAT, les
routes de retour, la redondance, une plateforme passerelle initiale ou une
bibliothèque : A08b porte sur l'adressage source et les retours, A08c sur le
basculement. Ces modalités restent à définir et qualifier.

### A08b — Proposition d'adressage source et de routes retour, non validée

Cet arbitrage définit le trafic transféré vers les ressources sans PA du
profil passerelle ultérieur A08a. Il ne rend pas ce profil disponible dans
le socle initial. Le plan A06, les permissions, la protection du dernier
segment et les délais A05 demeurent requis.

L'option A proposée conserve l'adresse source overlay du PA initiateur,
sans NAT sur le trajet passerelle–ressource. Le réseau de destination doit
posséder une route de retour vers les préfixes PZT autorisés via la passerelle
compétente ; les adresses sources effectivement permises et les chemins
aller/retour sont vérifiés avant exposition. L'adresse visible facilite la
corrélation des journaux de destination avec l'origine PZT, sans valoir
preuve d'identité ou permission. Cette option est recommandée lorsque
l'opérateur maîtrise les routes de retour, pour conserver cette visibilité.
Une route de retour manquante ou non vérifiable bloque la ressource, avec
diagnostic ; aucune traduction automatique ne masque cet échec.

L'option B proposée traduit explicitement l'adresse source des flux autorisés
vers une adresse de la passerelle joignable depuis la destination (SNAT,
éventuellement masquerade selon le profil qualifié). La destination répond
à cette adresse ; le profil peut éviter une route spécifique vers les
préfixes overlay lorsqu'un retour valide vers la passerelle existe déjà.
Les journaux de destination voient l'adresse traduite et ne distinguent pas
à eux seuls les PA d'origine ; PZT conserve une corrélation autorisée entre
identité, contexte, flux et traduction selon ses règles de minimisation et
de rétention. L'état de traduction et ses effets sur les sessions, quotas,
expiration et panne sont qualifiés. Cette option convient aux réseaux où
l'opérateur ne peut pas établir les routes de retour PZT.

Ces contraintes de retour et de visibilité figurent dans la [documentation
NetBird sur le masquerade](https://docs.netbird.io/manage/networks/masquerade) ;
la traduction IPv4 traditionnelle est décrite par [RFC 3022](https://datatracker.ietf.org/doc/html/rfc3022).
PZT développe ses propres contrats et adapters ; aucune limitation de
plateforme ou valeur de plan NetBird n'est adoptée implicitement.

Dans les deux options, la configuration est déclarée par ressource et
versionnée ; changer de mode nécessite un plan autorisé, des contrôles de
convergence et une qualification des sessions existantes. Le PA exécute
le plan uniquement sur les ressources gérées de son périmètre. Les droits
de transit restent distincts des services locaux de la passerelle, et la
traduction ne crée aucune permission. Collisions, boucles, asymétries,
anti-usurpation et filtrage des retours sont vérifiés. Le réglage IPv6 A06a
s'applique ; le choix n'introduit implicitement ni NAT IPv6, ni traduction
entre familles, ni route Internet par défaut.

A08c fixe ensuite le basculement : les routes retour ou états traduits
doivent rester cohérents avec la passerelle active, et une continuité de
session n'est pas présumée. CPU, mémoire, tables de suivi, trafic et délais
sont mesurés dans chaque profil ; aucune économie de ressources n'est déclarée
sans preuve. Les interfaces NAT/routage et les plateformes passerelles Linux,
Windows, VM ou conteneurs restent à qualifier séparément ; WFP ou nftables
retenus pour le filtrage ne démontrent pas à eux seuls toute cette capacité.
Aucune option A08b n'est adoptée.

### Autres modalités restant à préciser

| Sujet | Décision attendue |
| --- | --- |
| Multimaître et état autoritatif | Source de vérité précise des états de contrôle, coordination avec le PBO, stockage spécialisé éventuel, écritures concurrentes, partitions, quorum et éventuel leader interne. |
| Certification | Formats, ancrages, signataires, protection des clés racines, rotation et reprise après compromission. |
| Validation hybride | Classes de sensibilité, opérations exigeant une décision en ligne et conditions de réutilisation. |
| Révocation | Qualification des objectifs initiaux A05b, mécanismes de propagation et de clôture des sessions, affectation des classes et comportement lorsque l'état courant est inconnu. |
| Découverte | Distribution du catalogue, visibilité, fraîcheur, quotas et autorité compétente pour les relations interbranches. |
| Transport | WireGuard interhôtes, orientation des backends A01, TLS d'amorçage A02 et TLS mutuel sur le même hôte d'exécution A03 validés ; connectivité et relais A09, endpoints locaux, interfaces des backends et protocoles applicatifs à préciser. |
| Relais | Placement, sélection, capacité, contrôle d'accès et contraintes de résidence. |
| Cycle de vie | Enrôlement, changement de parent, adhésion, retrait, quarantaine et réintégration. |
| Services | Attestation locale, frontières d'isolation et intégration aux identités Pixs. |
| PA et PBO | Interfaces de contrôle et de configuration, déploiement et répartition des services exécutés par les PA. |
| Contrats et configuration | Formats, versions compatibles, états de suivi, frontières d'application et traitement des conflits ou applications partielles. |
| Identités | Références, mappings DigitalIdentity, enrôlement et preuves d'assurance propres aux rôles. |
| Attestation TPM du PA | Clés d'identité et d'attestation, formats et fraîcheur des preuves, chaîne de mesure couvrant le binaire et son environnement, références approuvées et mises à jour, liaison PA–conteneur–hôte, changement d'hôte et conditions d'admission sans TPM ou avec TPM logiciel ou virtuel. |
| Intégration PA | Séquencement des sept modes avec les services ZTP, dont `pzt-daemon` sans délai et son articulation avec l'initialisation minimale, sessions, budgets d'arrêt, qualification Python/C et états techniques locaux. |
| Amorçage et secours local | Transport local ZTP, initialisation, réparations internes au PA et blocage du contrôle PBO–PA lorsque ZTP local est indisponible. |
| Module ZTP côté PBO | Identifiant canonique, contrats, découpage des sous-modules, protection du lifecycle, accès local de reprise et présence éventuelle dans les profils autonomes. |
| Exploitation | Objectifs chiffrés, périmètres de sauvegarde, restauration, privilèges système, limites et quotas par profil. |

## Historique du document

| Version | Date | Évolution |
| --- | --- | --- |
| 0.0.1 | 4 octobre 2026 | Première rédaction du réseau Zero Trust Pixs. |
| 0.0.2 | 4 octobre 2026 | Adoption du nom Zéro Trust Pixs (ZTP), exécuté par le Pixs Agent (PA), contrôlé et configuré par le Pixs Backoffice (PBO). |
| 0.1.0 | 4 octobre 2026 | Formalisation du cahier des charges et intégration du module officiel ZTP côté PBO, obligatoire et protégé dans les profils concernés, enrichissable par sous-modularité, avec administration locale de reprise. |
| 0.2.0 | 4 octobre 2026 | Consolidation validée après relecture des cadrages Pixs : responsabilités, sources autoritatives, identités, contrats, configuration souhaitée/appliquée, lifecycle, opérations persistantes, clés, révocation, restauration, privilèges, quotas, interface PBO et matrice de qualification. Confrontation au CdC PA v0.0.4 : six modes, chaîne Python/C, séparation système/session, provisionnement, preuve d'exécution, protection du contrôle lors d'une reconfiguration et passage obligatoire PBO–PA par ZTP, y compris localement. Incrément mineur de 0.1.0 appliqué à la version précédente 0.1.0. |
| 0.3.0 | 5 octobre 2026 | Intégration demandée de WireGuard comme base logicielle et des capacités documentées par NetBird à redévelopper dans PZT/PA : cartes réseau, admission, connectivité, relais, DNS, posture, filtrage et passerelles ; critères de qualification et registre A01–A12. Périmètre précisé : PA Linux/Windows physiques et VM, Docker/LXC Proxmox ; A01 validé : priorité aux backends natifs par OS, espace utilisateur selon les besoins du profil. A02 option A validée : TLS d'amorçage intégré à PZT, limité à l'admission et aux preuves requises, avec ancrage de confiance préalable. A03 option A validée : TLS mutuel PZT sur le même hôte d'exécution, frontières des VM et conteneurs préservées. A04a option A validée : pzt-daemon gère les ressources réseau PZT de son périmètre, les autres modes soumettent leurs demandes autorisées. A04b option A validée : adapters PA nftables Linux et Windows Filtering Platform Windows, contrat commun et coexistence avec les règles de l'opérateur à qualifier. A05a option A validée : autorisations bornées, révocation connue sans attente d'expiration et protection indépendante de PA ; A05b premier jet validé : Courant 5 minutes/renouvellement 60 secondes, Protégé 60 secondes/renouvellement 20 secondes, Critique en ligne, révocation PA joignable en 5 secondes et protection après panne en 10 secondes ; objectifs à qualifier. A06a option A validée : IPv4/IPv6 dès le socle, familles activées par profil et désactivation IPv6 PZT par réglage unique, couvrant overlay et endpoints WireGuard/TLS sans modification implicite de l'IPv6 hôte ; A06b option A validée : plan privé configurable, allocations par autorité compétente, pools IPv4 RFC 1918 validés, IPv6 ULA /48 par domaine et contrôles de collisions ; A06c option B validée : DNS Pixs géré par un module essentiel PBO et utilisable par PZT et tous les PA, droits de publication/consultation et contrats publics distincts ; placement, interfaces et TTL à préciser. A07a option A validée : contrôle PBO–PA et PA–PA HTTP/JSON avec contrats OpenAPI versionnés ; A07b option A validée : snapshot initial et deltas ordonnés, déduplication et reprise complète en cas de désynchronisation, sans prolongation ni résurrection des droits ; A07c option B validée : notifications et retours de suivi WebSocket/JSON, commandes et lectures HTTP conservées ; consommation comparative PA/PBO et délais à qualifier. Extension A07c approuvée en principe : SSE et WebSocket avec adaptation déterministe ; A07c2 option A validée le 5 octobre 2026 : table de règles prioritaires, critères déterministes et seuils explicites ; valeurs, fenêtres, bascule et consommation à qualifier. A07d option A validée le 5 octobre 2026 : opérations métier JSON typées, identité stable, préconditions, versions, déduplication et preuves maintenues ; catalogue et schémas à préciser. A08a option A validée le 5 octobre 2026 : socle initial entre PA admis avec contrôle PBO, puis profil passerelle ultérieur, contrats et garanties conservés. A08b sources conservées ou traduction source soumis ; basculement A08c restant à débattre. Les autres recommandations restent ouvertes. Alignement sur PA v0.0.6 ; aucune écriture OpenSpec ni implémentation. |

## Références

Le cadrage existant de Pixs est décrit dans [PROJECT.md](PROJECT.md),
[TECHNICAL.md](TECHNICAL.md), [BUILD.md](BUILD.md) et [DEVOPS.md](DEVOPS.md).
L'intégration du PA est cadrée dans [PIXS_AGENT.md](PIXS_AGENT.md), relu en
version 0.0.6. PZT y désigne le réseau nommé ZTP dans le présent document.

Les spécifications applicables comprennent
[security](openspec/specs/security/spec.md),
[authorization](openspec/specs/authorization/spec.md),
[authorization-engine](openspec/specs/authorization-engine/spec.md),
[authentication](openspec/specs/authentication/spec.md),
[kernel](openspec/specs/kernel/spec.md),
[core](openspec/specs/core/spec.md),
[modules](openspec/specs/modules/spec.md),
[lifecycle](openspec/specs/lifecycle/spec.md),
[component-model](openspec/specs/component-model/spec.md),
[compatibility](openspec/specs/compatibility/spec.md),
[configuration](openspec/specs/configuration/spec.md),
[interactions](openspec/specs/interactions/spec.md),
[events](openspec/specs/events/spec.md),
[jobs](openspec/specs/jobs/spec.md),
[operations](openspec/specs/operations/spec.md),
[secrets-providers](openspec/specs/secrets-providers/spec.md),
[backup-disaster-recovery](openspec/specs/backup-disaster-recovery/spec.md),
[observability](openspec/specs/observability/spec.md),
[service-objectives](openspec/specs/service-objectives/spec.md),
[quotas-entitlements](openspec/specs/quotas-entitlements/spec.md),
[frontend](openspec/specs/frontend/spec.md),
[accessibility](openspec/specs/accessibility/spec.md),
[internationalization](openspec/specs/internationalization/spec.md),
[themes](openspec/specs/themes/spec.md),
[runtime](openspec/specs/runtime/spec.md) et
[regional-residency](openspec/specs/regional-residency/spec.md).

Les références techniques éclairent les mécanismes envisagés sans sélectionner
une brique NetBird ni démontrer une intégration fonctionnelle. WireGuard est
retenu explicitement comme base logicielle ; les autres choix restent ouverts :

- [WireGuard](https://www.wireguard.com/) : logiciel de transport IP sur UDP,
  clés publiques et AllowedIPs ; distribution de clés et configuration hors protocole.
- [Limites WireGuard](https://www.wireguard.com/known-limitations/) : absence
  de mode TCP natif et contraintes à traiter par les couches complémentaires.
- [Namespaces WireGuard](https://www.wireguard.com/netns/) : référence pour
  la qualification des frontières réseau locales et des conteneurs.
- Les références officielles NetBird sont identifiées dans la matrice de
  capacités en début de document ; elles servent au cadrage du développement propre à Pixs.

- [NIST SP 800 207](https://csrc.nist.gov/pubs/sp/800/207/final) : architecture
  Zero Trust et absence de confiance implicite fondée sur l'emplacement réseau.
- [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html) : sécurisation de QUIC
  à l'aide de TLS.
- [RFC 8445](https://www.rfc-editor.org/rfc/rfc8445.html) : établissement de
  connectivité ICE et traversée de NAT.
- [FAQ etcd](https://etcd.io/docs/v3.6/faq/) : exemple de consensus majoritaire
  et de compromis entre cohérence, tolérance aux pannes et latence.
