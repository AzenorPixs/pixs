## RENAMED Requirements

- FROM: `### Requirement: Module essentiel PBO et binaire PZT dédié`
- TO: `### Requirement: Module essentiel pixs.pzt et exécutable PZT indépendant`

## MODIFIED Requirements

### Requirement: Module essentiel pixs.pzt et exécutable PZT indépendant

Toute composition cible PBO MUST inclure le module officiel essentiel pixs.pzt,
au-dessus du Kernel et de pixs.core, par les mécanismes génériques. pixs.pzt
MUST configurer, administrer, visualiser, superviser et monitorer PZT. Le réseau
activé/configuré MUST être exécuté par le binaire indépendant PZT, compilé avec
Cython. Désactiver le réseau MUST NOT retirer pixs.pzt de PBO.

#### Scenario: Réseau désactivé et gestion conservée

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais pixs.pzt demeure composé avec ses fonctions de gestion

### Requirement: Expiration, révocation et protection indépendante

Les autorisations MUST être bornées, réutilisables seulement selon leur classe et retirées dès révocation connue. Les objectifs initiaux A05b MUST être qualifiés par profil : révocation en 5 s maximum lorsque PA est joignable et fermeture après panne PA en 10 s maximum, détection comprise, avec toute échéance antérieure prioritaire. Une interface noyau persistante après crash MUST NOT prolonger un accès.

#### Scenario: Expiration, révocation et protection indépendante

- **WHEN** l’exécutant PZT plante alors que WireGuard reste actif dans le noyau
- **THEN** la protection indépendante ferme les accès dans le budget qualifié

### Requirement: Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée

Le rôle chargé du traitement A08a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A08a

Une passerelle est un PA dont le rôle autorisé permet de transférer des flux
PZT vers une ressource déclarée sans PA, par exemple une imprimante réseau
ou un service dans un sous-réseau distant. La permission de cette ressource
est distincte de l'accès aux services de la passerelle. La capacité de
référence fonctionnelle est décrite dans les [réseaux NetBird](https://docs.netbird.io/manage/networks) ;
sa réalisation est développée dans PZT/PA, selon les contrats Pixs.

L'option A est validée par le développeur le 5 octobre 2026 : le socle de
communication entre PA admis est qualifié d'abord, avec le contrôle PBO
déjà prévu ; l'exécution des passerelles est réservée à un profil ultérieur
explicitement qualifié. Le cadrage conserve leurs garanties et contrats ; leur
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

Les six modes PA et le mode PZT conservent leurs responsabilités A04a ; le rôle passerelle
ne crée pas de mode supplémentaire ni de droits implicites sur l'hôte.
Linux/Windows physiques et VM, Docker/LXC Proxmox conservent leur périmètre
PA ; la capacité passerelle est déclarée et qualifiée séparément sur chaque
profil qui l'expose. Aucun montage, privilège, forwarding hôte ou configuration
Proxmox n'est modifié implicitement. A08b, option A validée, fixe la
conservation des sources sans NAT et la vérification des routes retour.
A08c, option A validée, retient une principale avec secours et un basculement
autorisé. Coordination A12, plateformes passerelles, interfaces et délais
restent à définir et qualifier.

##### Application au PA — A08a

Un PA peut porter un rôle passerelle déclaré pour transférer des flux
PZT autorisés vers une destination sans PA. L'accès à cette destination
reste distinct de l'accès aux services locaux de la passerelle. Ce rôle
n'ajoute aucun mode aux sept modes existants ; la propriété des ressources
A04a reste applicable.

L'option A est validée par le développeur le 5 octobre 2026 : le socle
qualifie d'abord les communications entre PA admis avec le contrôle PBO
déjà prévu ; le rôle passerelle devient exécutable dans un profil ultérieur
explicitement qualifié. Ses contrats et garanties restent au cadrage, avec une
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
ou droit Proxmox n'est accordé implicitement. A08b, option A validée,
fixe la conservation des sources sans NAT et la vérification des routes
retour. A08c, option A validée, retient une principale avec secours et un
basculement autorisé. Coordination A12, plateformes passerelles, interfaces
et délais restent à définir et qualifier.

#### Scenario: Conformité du traitement A08a

- **WHEN** un profil revendique le traitement A08a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée

## ADDED Requirements

### Requirement: Cycle de vie propre du composant PZT

PZT MUST être un composant exécutable indépendant de PA, avec le mode
pzt-daemon, ses comptes, clés, permissions et cycle de vie déclarés. Il MUST
démarrer sans les délais des démons PA au démarrage du système ou du conteneur
et exécuter le réseau seulement s'il est activé/configuré, sinon se fermer.
La colivraison PA/PZT MUST NOT donner à PA la propriété des ressources réseau.

#### Scenario: Démarrage PZT distinct des délais PA

- **WHEN** le démon PA est différé mais PZT activé et configuré est admissible
- **THEN** PZT démarre sans ce délai et conserve son rôle réseau indépendant

#### Scenario: PZT non activé

- **WHEN** le binaire PZT est présent dans le paquet ou l'image mais le réseau n'est pas activé/configuré
- **THEN** il se ferme sans supprimer pixs.pzt ni annoncer un réseau disponible

### Requirement: Contrôle de PZT et séparation de pixs.agent

Les échanges de configuration, administration, supervision et monitoring du
binaire PZT MUST relever des contrats publics sécurisés de pixs.pzt. pixs.agent
MUST gérer PA hors PZT et consommer le transport PZT sans l'administrer. Un
contrat de gestion MUST conserver cible, droits, validité et résultat observé ;
il MUST NOT ouvrir de canal PBO–PZT ou PBO–PA hors des contrôles PZT.

#### Scenario: Administration du réseau depuis PBO

- **WHEN** un opérateur demande une modification PZT autorisée
- **THEN** pixs.pzt porte la gestion et PZT exécute puis rapporte l'état réellement appliqué

### Requirement: Frontières et identités PA PZT explicites

Les profils MUST déclarer les interfaces PA–PZT, appelants, cibles, droits,
isolation et liaisons d'identités et de preuves requises. PA et PZT MUST garder
leurs identités, clés et états distincts. Une colivraison ou une attestation PA
MUST NOT admettre automatiquement PZT, transférer un secret, un privilège ou
supprimer une preuve d'identité, d'hôte ou d'intégrité exigée.

#### Scenario: Colivraison sans admission du composant réseau

- **WHEN** PA et PZT sont installés ensemble mais une preuve requise pour PZT n'est pas vérifiable
- **THEN** le périmètre dépendant est bloqué sans identité partagée ni transfert implicite de droit

### Requirement: Correspondance des rôles réseau dans les contrats intégrés

Les contrats intégrés MUST conserver leurs références, valeurs et garanties.
Leurs mentions héritées de PA comme exécutant ou propriétaire réseau PZT MUST
désigner désormais PZT pour ces rôles. Les objets PA, sessions, hôte et preuves
TPM MUST conserver leur portée propre, avec liaisons explicites. La séparation
MUST NOT affaiblir admission, autorisation, révocation, attestation ou audit.

#### Scenario: Lecture d'un contrat réseau antérieur à la séparation

- **WHEN** une fiche héritée attribue à PA une écriture WireGuard ou un rôle de relais PZT
- **THEN** l'exécutant est PZT et les identités PA, d'hôte et les preuves exigées restent vérifiées dans leur portée
