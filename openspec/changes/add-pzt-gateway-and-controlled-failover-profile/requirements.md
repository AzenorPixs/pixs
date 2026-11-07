# Références normatives — Z08

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pzt | Passerelles après socle et source conservée | 1 | pzt-663457cbcbaa |
| pzt | Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée | 1 | pzt-965a4413b953 |
| pzt | Contrat A08b — Conservation des sources et routes retour, option A validée | 1 | pzt-2d01384fb49d |
| pzt | Contrat A08c — Principale avec secours et basculement, option A validée | 1 | pzt-4a3dccfe7716 |
| zt-network-services | SZT obligatoire et actifs coopérants | 1 | zt-network-services-7c321c1cf4f2 |
| zt-network-services | RZT obligatoire et relais commun | 1 | zt-network-services-be7be26f8f18 |
| zt-network-services | STZT obligatoire sans primaire | 1 | zt-network-services-e8fd6d093187 |
| zt-network-services | Identités durables et audit des rôles RAM | 1 | zt-network-services-81dcf2614938 |
| zt-network-services | GZT facultatif et périmètre de routage | 1 | zt-network-services-f31b1ffff554 |
| zt-network-services | Traduction source explicite | 1 | zt-network-services-6b4f4e6c8ef5 |
| zt-network-services | EZT distinct facultatif et groupes | 1 | zt-network-services-b00860d61906 |
| zt-network-services | Répartition et continuité EZT | 1 | zt-network-services-c0d7619c05f7 |
| zt-network-services | Santé par chemin et famille IP | 1 | zt-network-services-c1574cf12e7f |
| zt-network-services | RPZT facultatif et actifs multiples | 1 | zt-network-services-c666104b77f7 |
| zt-network-services | Authentification au service cible | 1 | zt-network-services-9f7d4b5d9913 |
| zt-network-services | TLS par publication et distribution PKIZT | 1 | zt-network-services-4da2c1ae43f4 |

### Référence courante pzt-663457cbcbaa

Source : [pzt](../../specs/pzt/spec.md), ligne 176. SHA-256 : `663457cbcbaaa8d390083380584ff1e94bca9683bdfc04e5bb3503b1e1498aa1`.

Scénarios : Passerelles après socle et source conservée.

~~~~text
### Requirement: Passerelles après socle et source conservée

Le profil passerelle MUST être livré après qualification du socle initial. Il MUST conserver les sources et routes retour, sans NAT automatique, avec principale et secours déclarés et un seul actif par périmètre de routage cohérent. Bascule MUST utiliser autorité/mandat courant, vérifier allers/retours et convergence, sans garantir implicitement la continuité des sessions.

#### Scenario: Passerelles après socle et source conservée

- **WHEN** le trafic retour continue d'emprunter l'ancienne passerelle
- **THEN** la bascule n'est pas déclarée réussie
~~~~

### Référence courante pzt-965a4413b953

Source : [pzt](../../specs/pzt/spec.md), ligne 1619. SHA-256 : `965a4413b953316b378bb2bfabbe531cbdcad0be65767d0c8e98d0537dde19ac`.

Scénarios : Conformité du traitement A08a.

~~~~text
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
~~~~

### Référence courante pzt-2d01384fb49d

Source : [pzt](../../specs/pzt/spec.md), ligne 1708. SHA-256 : `2d01384fb49d82ca9ab6373adcb8ae782a6fecdeb71de29b6ee5b1a2225ad9aa`.

Scénarios : Conformité du traitement A08b.

~~~~text
### Requirement: Contrat A08b — Conservation des sources et routes retour, option A validée

Le rôle chargé du traitement A08b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A08b

Cet arbitrage concerne le trafic transféré vers les ressources sans PA du
profil passerelle ultérieur A08a. Il ne rend pas ce profil disponible dans
le socle initial. Le plan A06, les permissions, la protection du dernier
segment et les délais A05 demeurent requis.

L'option A est validée par le développeur le 5 octobre 2026 : l'adresse
source overlay du PA initiateur est conservée, sans NAT sur le trajet
passerelle–ressource. Le réseau de destination doit posséder une route de
retour vers les préfixes PZT autorisés via la passerelle compétente. Les
sources effectivement permises, les chemins aller et les chemins retour
sont vérifiés avant exposition. Une route de retour manquante ou non
vérifiable bloque la ressource, avec diagnostic ; aucune traduction
automatique ne masque cet échec.

L'adresse visible facilite la corrélation des journaux de destination avec
l'origine PZT ; elle ne vaut ni preuve d'identité ni permission. Le contexte,
l'identité et les flux restent corrélés selon les accès, la minimisation
et la rétention déclarés. L'option B de traduction source vers l'adresse
de la passerelle n'est pas retenue comme mode de référence.

La configuration est déclarée par ressource et versionnée ; sa modification
nécessite un plan autorisé et un contrôle de convergence. Le PA applique
ce plan uniquement sur les ressources gérées de son périmètre et rapporte
l'état effectivement appliqué. Les routes nécessaires sur des équipements
externes sont provisionnées par l'opérateur ou par un mécanisme explicitement
autorisé ; leur nécessité n'accorde aucun droit de modification implicite.
Les droits de transit restent distincts des services locaux de la passerelle.
Collisions, boucles, asymétries, anti-usurpation et filtrage des retours sont
vérifiés. Les changements de route ne renouvellent aucune permission.

Le choix s'applique aux familles autorisées du profil ; IPv6 demeure
simplement désactivable selon A06a. Il n'introduit ni NAT IPv6, ni traduction
entre familles, ni route Internet par défaut. Les interfaces de routage,
de transfert et de filtrage, leurs privilèges et leurs effets sur les sessions
sont qualifiés séparément pour chaque plateforme passerelle exposée :
Linux/Windows physiques et VM, Docker/LXC sous Proxmox. Le choix A04b de
nftables ou WFP ne démontre pas à lui seul cette capacité complète.

Les contraintes de retour et de visibilité sont documentées par
[NetBird sur le masquerade](https://docs.netbird.io/manage/networks/masquerade).
PZT développe ses propres contrats et adapters ; les limites de plateforme
et les valeurs de plan NetBird ne sont pas adoptées implicitement. A08c
traite ensuite le basculement : les routes retour doivent rester cohérentes
avec la passerelle active. La continuité des sessions et une économie de
CPU, mémoire ou trafic ne sont pas présumées ; elles restent à qualifier.

##### Application au PA — A08b

Ce choix concerne les flux du profil passerelle ultérieur A08a. Le premier
socle conserve les communications entre PA admis et le contrôle PBO ; il
ne devient pas une passerelle du fait de cet arbitrage.

L'option A est validée par le développeur le 5 octobre 2026 : PA conserve
l'adresse source overlay de l'initiateur sans NAT vers la ressource. Les
sources permises, les chemins aller et les routes de retour vers les préfixes
PZT autorisés via la passerelle compétente sont vérifiés avant exposition.
Une route absente ou non vérifiable bloque la ressource et produit un
diagnostic, sans traduction automatique. L'adresse visible facilite la
corrélation côté destination ; elle ne vaut ni preuve d'identité ni permission.
L'identité, le contexte et les flux restent corrélés selon les accès, la
rétention et la minimisation déclarés. La traduction source, option B,
n'est pas retenue comme mode de référence.

PA applique un plan autorisé, versionné par ressource, sur les seules
ressources de son périmètre et rapporte la convergence et les erreurs.
Les routes requises sur des équipements externes sont provisionnées par
l'opérateur ou selon un mandat explicite ; leur nécessité n'accorde aucun
droit implicite. Changer de route ne renouvelle aucune permission. Transit
et services locaux restent distincts. Collisions, boucles, asymétries,
anti-usurpation et filtrage des retours sont contrôlés. Les familles autorisées
du profil sont respectées ; IPv6 reste désactivable selon A06a, sans NAT IPv6,
traduction entre familles ou routage Internet implicite.

Les interfaces de routage, de transfert et de filtrage et leurs privilèges
sont qualifiés séparément pour chaque plateforme passerelle exposée :
Linux/Windows physiques et VM, Docker/LXC Proxmox. Le choix des adapters
A04b ne démontre pas toute cette capacité. A08c précise le basculement avec
des retours cohérents avec la passerelle active ; la continuité des sessions
n'est pas présumée. CPU, mémoire, tables de suivi, trafic et délais restent
à mesurer. Les sources officielles figurent dans le cadrage PZT.

#### Scenario: Conformité du traitement A08b

- **WHEN** un profil revendique le traitement A08b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence courante pzt-4a3dccfe7716

Source : [pzt](../../specs/pzt/spec.md), ligne 1805. SHA-256 : `4a3dccfe77161808d0c2339bef5e28d115255824b749d6e7dafce12175bedb65`.

Scénarios : Conformité du traitement A08c.

~~~~text
### Requirement: Contrat A08c — Principale avec secours et basculement, option A validée

Le rôle chargé du traitement A08c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A08c

Cet arbitrage complète le profil passerelle ultérieur A08a avec les sources
conservées sans NAT A08b. Il ne modifie pas la livraison du socle initial.
Permissions, preuves d'admission, contraintes de résidence et échéances A05
restent applicables ; un changement de passerelle ne crée ni ne renouvelle
un droit.

L'option A est validée par le développeur le 5 octobre 2026 : une passerelle
principale et un ou plusieurs secours autorisés et qualifiés sont désignés.
Une seule passerelle est active par périmètre de routage cohérent ; les
ressources qui partagent le même chemin de retour sont regroupées, sauf
séparation explicitement qualifiée. La sélection suit des priorités déclarées
et un départage stable. Un secours peut prendre la relève après une
défaillance vérifiée, sur décision courante d'une autorité compétente ou
selon un mandat de basculement explicite encore valide. L'option B de
répartition des flux entre plusieurs passerelles actives n'est pas retenue
comme mode de référence.

Les contrôles de santé vérifient le chemin utile jusqu'à une ressource ou
une sonde autorisée ; la présence d'un processus, d'une interface ou d'un
handshake WireGuard ne suffit pas. Le plan vérifie les permissions et la
configuration de la nouvelle passerelle, les routes aller et retour ainsi
que le filtrage effectivement appliqués, puis rapporte la convergence.
Les modifications de route sur des équipements externes restent soumises
à un mandat ou à une intervention opérateur. Un retour qui emprunte
l'ancienne passerelle ne constitue pas un basculement réussi.

Le profil empêche des décisions actives contradictoires et l'usage d'un
ancien mandat après panne ou restauration. L'algorithme de coordination,
les preuves d'autorité et le traitement des partitions suivent A12a–A12g
validés ; les modalités de réalisation restent à qualifier. A08c ne choisit
pas à elle seule un quorum ou un protocole de consensus.
En cas de preuve ou de chemin indispensable non vérifiable, l'accès concerné
est bloqué selon A05, sans NAT de secours ni contournement hors PZT.

Le retour vers la principale suit une règle explicite de stabilité et une
autorisation valide. Seuils, fenêtres, durée de détection et objectif de
convergence restent à préciser et mesurer ; les temporisations d'optimisation
ne retardent pas une révocation ou une expiration A05. Une interruption de
session demeure possible : conserver la source sans NAT ne conserve pas
automatiquement tous les états des pare-feu ou de l'application.

La [documentation NetBird sur la haute disponibilité sans masquerade](https://docs.netbird.io/manage/networks/masquerade#high-availability-with-masquerade-off)
illustre la nécessité d'adapter le retour à la passerelle active. PZT
redéveloppe ses contrats ; aucune VIP, VRRP, BGP, bibliothèque, privilège
hôte ou configuration Proxmox n'est sélectionné par cette décision.
CPU, mémoire, sondes, trafic de contrôle, interruptions et reprise restent
à qualifier séparément pour chaque plateforme passerelle exposée :
Linux/Windows physiques et VM, Docker/LXC sous Proxmox.

##### Application au PA — A08c

Le choix concerne le profil passerelle ultérieur A08a sans NAT A08b.
Il ne modifie pas la livraison initiale. Admission, permissions, résidence,
expiration et révocation A05 restent applicables ; basculer ne renouvelle
aucun droit.

L'option A est validée par le développeur le 5 octobre 2026 : une principale
avec un ou plusieurs secours autorisés et qualifiés, une seule passerelle
active par périmètre de routage cohérent. Les ressources partageant le retour
sont regroupées, sauf séparation explicitement qualifiée. Priorités et
départage sont déterministes. PA exécute un basculement après une défaillance
vérifiée, selon une décision courante de l'autorité compétente ou un mandat
explicite encore valide. L'option B de répartition entre plusieurs passerelles
actives n'est pas retenue comme mode de référence.

PA vérifie le chemin utile jusqu'à une ressource ou une sonde autorisée ;
processus, interface et handshake WireGuard seuls ne suffisent pas. Il
vérifie ses preuves et sa configuration, applique le plan autorisé et
rapporte les routes et le filtrage réellement appliqués. La convergence
comprend les retours côté destination, provisionnés par l'opérateur ou par
un mécanisme explicitement autorisé ; un retour via l'ancienne passerelle
ne vaut pas basculement réussi.

Le profil empêche des décisions actives contradictoires et la réutilisation
d'un mandat obsolète après panne ou restauration. Coordination, preuves
d'autorité et partitions suivent A12a–A12g validés ; modalités à qualifier.
Sans preuve ou chemin
indispensable vérifiable, l'accès concerné est bloqué selon A05, sans NAT
de secours ni communication hors PZT. Le retour vers la principale suit
une règle de stabilité déclarée et une autorisation valide ; les temporisations
ne prolongent ni permission ni délai de révocation.

Seuils, fenêtres, détection, convergence, consommation et effets sur les
sessions restent à qualifier ; l'absence de NAT ne garantit pas leur
continuité. Le rôle est qualifié par plateforme, avec les contraintes des
machines physiques et VM Linux/Windows et de Docker/LXC Proxmox. Aucun
protocole de redondance, bibliothèque, privilège hôte ou changement Proxmox
n'est choisi. Les sources figurent dans le cadrage PZT.

#### Scenario: Conformité du traitement A08c

- **WHEN** un profil revendique le traitement A08c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence courante zt-network-services-7c321c1cf4f2

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 11. SHA-256 : `7c321c1cf4f26905daee4e480d113bcdb3788457f5db8a88b1f25e245eea7638`.

Scénarios : Pairs sur deux SZT.

~~~~text
### Requirement: SZT obligatoire et actifs coopérants

Chaque ZT MUST disposer d'au moins un SZT pour mettre les pairs en relation. Plusieurs SZT actifs MUST pouvoir coopérer pour des pairs raccordés à des SZT différents. L'état de présence/négociation MUST être temporaire en RAM, reconstruit au démarrage, sans PG propre.

#### Scenario: Pairs sur deux SZT

- **WHEN** deux pairs autorisés sont raccordés à des SZT différents
- **THEN** la signalisation permet leur mise en relation sans créer une nouvelle permission.
~~~~

### Référence courante zt-network-services-be7be26f8f18

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 20. SHA-256 : `be7be26f8f182efa4d0939bbc9800f4dbce7fd69f747e70ffb9330d288197c27`.

Scénarios : Panne du relais.

~~~~text
### Requirement: RZT obligatoire et relais commun

Chaque ZT MUST disposer d'au moins un RZT relayant le trafic chiffré. Plusieurs RZT MAY être actifs et les pairs MUST pouvoir choisir un relais commun admissible. Connexions, associations et tampons MUST rester temporaires en RAM sans PG propre ; la panne MUST permettre une reconnexion autorisée sans promettre la conservation transparente des sessions.

#### Scenario: Panne du relais

- **WHEN** le RZT d’une communication tombe
- **THEN** les pairs rétablissent un chemin admissible et les interruptions sont rapportées sans succès fictif.
~~~~

### Référence courante zt-network-services-e8fd6d093187

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 29. SHA-256 : `e8fd6d093187cfdb8fd956073c19a45151f900fe9f5145dd80bf77796f951669`.

Scénarios : STZT redémarré.

~~~~text
### Requirement: STZT obligatoire sans primaire

Chaque ZT MUST disposer d'au moins un STZT pour la découverte des adresses et ports observés. Plusieurs STZT actifs indépendants MUST être possibles, avec état temporaire RAM sans PG propre ni réplication de cet état.

#### Scenario: STZT redémarré

- **WHEN** un STZT perd ses observations RAM
- **THEN** les pairs peuvent refaire une découverte sans réadmission d’identité ni remise à zéro des autorisations.
~~~~

### Référence courante zt-network-services-81dcf2614938

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 38. SHA-256 : `81dcf2614938db196c5b2c93fcd31900c9084f835df1cda37b4000b5ea3c5a47`.

Scénarios : Rôle RAM redémarré.

~~~~text
### Requirement: Identités durables et audit des rôles RAM

L'absence de PG propre MUST NOT supprimer les identités, références de démarrage et clés protégées des PZT ni l'audit durable applicable. Les politiques MUST rester sous CZT et l'état temporaire MUST NOT devenir source d'autorisation indépendante.

#### Scenario: Rôle RAM redémarré

- **WHEN** SZT ou RZT reconstruit son état
- **THEN** il vérifie les autorisations courantes sans inventer de droits à partir des anciennes connexions.
~~~~

### Référence courante zt-network-services-f31b1ffff554

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 47. SHA-256 : `f31b1ffff55446591fbd93cff12c041836971927a85c3eec9a05e06ffa71ff2c`.

Scénarios : Passerelle de secours.

~~~~text
### Requirement: GZT facultatif et périmètre de routage

GZT MUST être optionnel et désactivé par défaut, exécuté par PZT pour les destinations sans PZT explicitement autorisées. Sa référence MUST être dans CZT et son état opérationnel en RAM sans PG propre. Un GZT actif unique par périmètre MUST être assuré avec répartition des périmètres et secours à bascule automatique encadrée.

#### Scenario: Passerelle de secours

- **WHEN** un GZT est remplacé pour son périmètre
- **THEN** le secours n’achemine qu’après vérification de son autorité et des conditions de reprise.
~~~~

### Référence courante zt-network-services-6b4f4e6c8ef5

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 56. SHA-256 : `6b4f4e6c8ef5c478afc29d4d824fb5a589d4015272d6998adde2bfb0d491d5a6`.

Scénarios : Route retour absente.

~~~~text
### Requirement: Traduction source explicite

La traduction d'adresse source GZT MUST être désactivée par défaut et activable explicitement par périmètre. Sans traduction, les routes de retour MUST être vérifiées ; le dernier segment hors PZT MUST disposer des protections exigées par le périmètre.

#### Scenario: Route retour absente

- **WHEN** une ressource sans PZT n’a pas de retour autorisé vers la source conservée
- **THEN** l’accès n’est pas déclaré fonctionnel et NAT n’est pas activé implicitement.
~~~~

### Référence courante zt-network-services-b00860d61906

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 65. SHA-256 : `b00860d61906096ec9ea962760d5179c2fe18efe94fb63f59d6ff06c71ba7017`.

Scénarios : EZT externe.

~~~~text
### Requirement: EZT distinct facultatif et groupes

EZT MUST être un rôle distinct optionnel et désactivé par défaut, avec référence CZT et état RAM sans PG propre. Les politiques de sortie MUST pouvoir désigner des groupes avec niveaux de priorité et membres explicitement autorisés, y compris externes par approbation sans changement d'appartenance.

#### Scenario: EZT externe

- **WHEN** un groupe référence un EZT d’un autre ZT
- **THEN** son inclusion et son usage exigent les autorisations applicables sans le rendre membre local.
~~~~

### Référence courante zt-network-services-c0d7619c05f7

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 74. SHA-256 : `c0d7619c05f7a300a5d837375353b23fb94b2feb3e02ace22969c3f13e1984d9`.

Scénarios : Groupe indisponible.

~~~~text
### Requirement: Répartition et continuité EZT

Les nouvelles connexions MUST être réparties entre les EZT admissibles du meilleur niveau disponible, avec poids configurables égaux par défaut. Chaque connexion MUST conserver son EZT tant que possible ; retour au préféré MUST être configurable avec maintien des connexions par défaut. L’absence de membre utilisable MUST conduire au blocage, sans sortie directe implicite.

#### Scenario: Groupe indisponible

- **WHEN** aucun EZT du groupe autorisé n’est utilisable
- **THEN** le trafic concerné reste bloqué sans utiliser une sortie non autorisée.
~~~~

### Référence courante zt-network-services-c1574cf12e7f

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 83. SHA-256 : `c1574cf12e7feae841d07b444e6750c07e271dde0efb6f59d151857480319c54`.

Scénarios : Sortie IPv6 rompue.

~~~~text
### Requirement: Santé par chemin et famille IP

Les groupes EZT MUST avoir critères de santé configurables par chemin et famille IP, avec temporisations d'exclusion et réadmission. La santé IPv4 MUST NOT suffire à qualifier le chemin IPv6 ni un simple processus vivant à qualifier la sortie.

#### Scenario: Sortie IPv6 rompue

- **WHEN** un EZT fonctionne en IPv4 mais échoue aux critères IPv6
- **THEN** son admissibilité IPv6 est traitée séparément.
~~~~

### Référence courante zt-network-services-c666104b77f7

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 92. SHA-256 : `c666104b77f7521618077500dde9c139d7352afdcbec9a9190616d99b921a34e`.

Scénarios : Deux RPZT.

~~~~text
### Requirement: RPZT facultatif et actifs multiples

RPZT MUST publier les services HTTP/HTTPS/WebSocket explicitement autorisés, être optionnel et désactivé par défaut, avec référence CZT et RAM sans PG propre. Plusieurs RPZT MAY être actifs pour une publication ; l'orientation des clients et ses effets MUST être qualifiés.

#### Scenario: Deux RPZT

- **WHEN** deux exécutants portent une publication
- **THEN** la présence des deux ne prouve pas à elle seule une orientation ou bascule fonctionnelle.
~~~~

### Référence courante zt-network-services-9f7d4b5d9913

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 101. SHA-256 : `9f7d4b5d99131170e79e5cfaa72940a0b9120e84066bb8b149276257501ab287`.

Scénarios : Service public non déclaré.

~~~~text
### Requirement: Authentification au service cible

RPZT MUST assurer publication, acheminement et restrictions techniques sans authentifier les utilisateurs. Le service cible MUST assurer l'authentification et les droits applicatifs par défaut ; une publication publique MUST être déclarée et autorisée explicitement.

#### Scenario: Service public non déclaré

- **WHEN** une publication vise un service sans authentification sans autorisation publique
- **THEN** elle n’est pas admise comme publication protégée par le seul RPZT.
~~~~

### Référence courante zt-network-services-4da2c1ae43f4

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 110. SHA-256 : `4da2c1ae43f4daf05a06f9d630468a2fd057857830ff776838fc7952e91a13e6`.

Scénarios : TLS passthrough.

~~~~text
### Requirement: TLS par publication et distribution PKIZT

Chaque publication MUST choisir terminaison TLS au RPZT ou passage chiffré jusqu'au service. En terminaison, PKIZT MUST assurer le cycle des certificats et la remise ciblée/protégée selon zt-pki. Un mode TLS MUST NOT créer une responsabilité d'authentification utilisateur au RPZT.

#### Scenario: TLS passthrough

- **WHEN** une publication transmet TLS jusqu’au service
- **THEN** le service termine TLS et RPZT ne prétend pas authentifier l’utilisateur.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 111 | [Passerelles après socle et source conservée](../../specs/pzt/spec.md#L111) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1666 | [Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée](../../specs/pzt/spec.md#L1666) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1755 | [Contrat A08b — Conservation des sources et routes retour, option A validée](../../specs/pzt/spec.md#L1755) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1852 | [Contrat A08c — Principale avec secours et basculement, option A validée](../../specs/pzt/spec.md#L1852) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--030cf179ed

Source : `openspec/specs/pzt/spec.md`, ligne 111. SHA-256 du bloc : `3dcf2db9fddb4d3ab1aece4a7d58c1992d5e484c15b57fd3d2e240f255d04c90`.

~~~~text
### Requirement: Passerelles après socle et source conservée

Le profil passerelle MUST être livré après qualification du socle initial. Il MUST conserver les sources et routes retour, sans NAT automatique, avec principale et secours déclarés et un seul actif par périmètre de routage cohérent. Bascule MUST utiliser autorité/mandat courant, vérifier allers/retours et convergence, sans garantir implicitement la continuité des sessions.

#### Scenario: Passerelles après socle et source conservée

- **WHEN** le trafic retour continue d'emprunter l'ancienne passerelle
- **THEN** la bascule n'est pas déclarée réussie
~~~~

### Référence pzt--0162beddae

Source : `openspec/specs/pzt/spec.md`, ligne 1666. SHA-256 du bloc : `ea0b59ec7919d0d5723c4b63cc96896f99d1bcf52e6983d7b5c7b51a5c4c85f4`.

~~~~text
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

Les sept modes PA conservent leurs responsabilités A04a ; le rôle passerelle
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
~~~~

### Référence pzt--4408379fd3

Source : `openspec/specs/pzt/spec.md`, ligne 1755. SHA-256 du bloc : `bb1617164c47bebca3383256c70ffc353a070649a6a2ae304da1a832e02f7472`.

~~~~text
### Requirement: Contrat A08b — Conservation des sources et routes retour, option A validée

Le rôle chargé du traitement A08b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A08b

Cet arbitrage concerne le trafic transféré vers les ressources sans PA du
profil passerelle ultérieur A08a. Il ne rend pas ce profil disponible dans
le socle initial. Le plan A06, les permissions, la protection du dernier
segment et les délais A05 demeurent requis.

L'option A est validée par le développeur le 5 octobre 2026 : l'adresse
source overlay du PA initiateur est conservée, sans NAT sur le trajet
passerelle–ressource. Le réseau de destination doit posséder une route de
retour vers les préfixes PZT autorisés via la passerelle compétente. Les
sources effectivement permises, les chemins aller et les chemins retour
sont vérifiés avant exposition. Une route de retour manquante ou non
vérifiable bloque la ressource, avec diagnostic ; aucune traduction
automatique ne masque cet échec.

L'adresse visible facilite la corrélation des journaux de destination avec
l'origine PZT ; elle ne vaut ni preuve d'identité ni permission. Le contexte,
l'identité et les flux restent corrélés selon les accès, la minimisation
et la rétention déclarés. L'option B de traduction source vers l'adresse
de la passerelle n'est pas retenue comme mode de référence.

La configuration est déclarée par ressource et versionnée ; sa modification
nécessite un plan autorisé et un contrôle de convergence. Le PA applique
ce plan uniquement sur les ressources gérées de son périmètre et rapporte
l'état effectivement appliqué. Les routes nécessaires sur des équipements
externes sont provisionnées par l'opérateur ou par un mécanisme explicitement
autorisé ; leur nécessité n'accorde aucun droit de modification implicite.
Les droits de transit restent distincts des services locaux de la passerelle.
Collisions, boucles, asymétries, anti-usurpation et filtrage des retours sont
vérifiés. Les changements de route ne renouvellent aucune permission.

Le choix s'applique aux familles autorisées du profil ; IPv6 demeure
simplement désactivable selon A06a. Il n'introduit ni NAT IPv6, ni traduction
entre familles, ni route Internet par défaut. Les interfaces de routage,
de transfert et de filtrage, leurs privilèges et leurs effets sur les sessions
sont qualifiés séparément pour chaque plateforme passerelle exposée :
Linux/Windows physiques et VM, Docker/LXC sous Proxmox. Le choix A04b de
nftables ou WFP ne démontre pas à lui seul cette capacité complète.

Les contraintes de retour et de visibilité sont documentées par
[NetBird sur le masquerade](https://docs.netbird.io/manage/networks/masquerade).
PZT développe ses propres contrats et adapters ; les limites de plateforme
et les valeurs de plan NetBird ne sont pas adoptées implicitement. A08c
traite ensuite le basculement : les routes retour doivent rester cohérentes
avec la passerelle active. La continuité des sessions et une économie de
CPU, mémoire ou trafic ne sont pas présumées ; elles restent à qualifier.

##### Application au PA — A08b

Ce choix concerne les flux du profil passerelle ultérieur A08a. Le premier
socle conserve les communications entre PA admis et le contrôle PBO ; il
ne devient pas une passerelle du fait de cet arbitrage.

L'option A est validée par le développeur le 5 octobre 2026 : PA conserve
l'adresse source overlay de l'initiateur sans NAT vers la ressource. Les
sources permises, les chemins aller et les routes de retour vers les préfixes
PZT autorisés via la passerelle compétente sont vérifiés avant exposition.
Une route absente ou non vérifiable bloque la ressource et produit un
diagnostic, sans traduction automatique. L'adresse visible facilite la
corrélation côté destination ; elle ne vaut ni preuve d'identité ni permission.
L'identité, le contexte et les flux restent corrélés selon les accès, la
rétention et la minimisation déclarés. La traduction source, option B,
n'est pas retenue comme mode de référence.

PA applique un plan autorisé, versionné par ressource, sur les seules
ressources de son périmètre et rapporte la convergence et les erreurs.
Les routes requises sur des équipements externes sont provisionnées par
l'opérateur ou selon un mandat explicite ; leur nécessité n'accorde aucun
droit implicite. Changer de route ne renouvelle aucune permission. Transit
et services locaux restent distincts. Collisions, boucles, asymétries,
anti-usurpation et filtrage des retours sont contrôlés. Les familles autorisées
du profil sont respectées ; IPv6 reste désactivable selon A06a, sans NAT IPv6,
traduction entre familles ou routage Internet implicite.

Les interfaces de routage, de transfert et de filtrage et leurs privilèges
sont qualifiés séparément pour chaque plateforme passerelle exposée :
Linux/Windows physiques et VM, Docker/LXC Proxmox. Le choix des adapters
A04b ne démontre pas toute cette capacité. A08c précise le basculement avec
des retours cohérents avec la passerelle active ; la continuité des sessions
n'est pas présumée. CPU, mémoire, tables de suivi, trafic et délais restent
à mesurer. Les sources officielles figurent dans le cadrage PZT.

#### Scenario: Conformité du traitement A08b

- **WHEN** un profil revendique le traitement A08b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--4d93d98ef2

Source : `openspec/specs/pzt/spec.md`, ligne 1852. SHA-256 du bloc : `278cfbaa3a8deec10e158f35000908db71c64fa8ef1f758c26b4bd5ac2660dc6`.

~~~~text
### Requirement: Contrat A08c — Principale avec secours et basculement, option A validée

Le rôle chargé du traitement A08c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A08c

Cet arbitrage complète le profil passerelle ultérieur A08a avec les sources
conservées sans NAT A08b. Il ne modifie pas la livraison du socle initial.
Permissions, preuves d'admission, contraintes de résidence et échéances A05
restent applicables ; un changement de passerelle ne crée ni ne renouvelle
un droit.

L'option A est validée par le développeur le 5 octobre 2026 : une passerelle
principale et un ou plusieurs secours autorisés et qualifiés sont désignés.
Une seule passerelle est active par périmètre de routage cohérent ; les
ressources qui partagent le même chemin de retour sont regroupées, sauf
séparation explicitement qualifiée. La sélection suit des priorités déclarées
et un départage stable. Un secours peut prendre la relève après une
défaillance vérifiée, sur décision courante d'une autorité compétente ou
selon un mandat de basculement explicite encore valide. L'option B de
répartition des flux entre plusieurs passerelles actives n'est pas retenue
comme mode de référence.

Les contrôles de santé vérifient le chemin utile jusqu'à une ressource ou
une sonde autorisée ; la présence d'un processus, d'une interface ou d'un
handshake WireGuard ne suffit pas. Le plan vérifie les permissions et la
configuration de la nouvelle passerelle, les routes aller et retour ainsi
que le filtrage effectivement appliqués, puis rapporte la convergence.
Les modifications de route sur des équipements externes restent soumises
à un mandat ou à une intervention opérateur. Un retour qui emprunte
l'ancienne passerelle ne constitue pas un basculement réussi.

Le profil empêche des décisions actives contradictoires et l'usage d'un
ancien mandat après panne ou restauration. L'algorithme de coordination,
les preuves d'autorité et le traitement des partitions suivent A12a–A12g
validés ; les modalités de réalisation restent à qualifier. A08c ne choisit
pas à elle seule un quorum ou un protocole de consensus.
En cas de preuve ou de chemin indispensable non vérifiable, l'accès concerné
est bloqué selon A05, sans NAT de secours ni contournement hors PZT.

Le retour vers la principale suit une règle explicite de stabilité et une
autorisation valide. Seuils, fenêtres, durée de détection et objectif de
convergence restent à préciser et mesurer ; les temporisations d'optimisation
ne retardent pas une révocation ou une expiration A05. Une interruption de
session demeure possible : conserver la source sans NAT ne conserve pas
automatiquement tous les états des pare-feu ou de l'application.

La [documentation NetBird sur la haute disponibilité sans masquerade](https://docs.netbird.io/manage/networks/masquerade#high-availability-with-masquerade-off)
illustre la nécessité d'adapter le retour à la passerelle active. PZT
redéveloppe ses contrats ; aucune VIP, VRRP, BGP, bibliothèque, privilège
hôte ou configuration Proxmox n'est sélectionné par cette décision.
CPU, mémoire, sondes, trafic de contrôle, interruptions et reprise restent
à qualifier séparément pour chaque plateforme passerelle exposée :
Linux/Windows physiques et VM, Docker/LXC sous Proxmox.

##### Application au PA — A08c

Le choix concerne le profil passerelle ultérieur A08a sans NAT A08b.
Il ne modifie pas la livraison initiale. Admission, permissions, résidence,
expiration et révocation A05 restent applicables ; basculer ne renouvelle
aucun droit.

L'option A est validée par le développeur le 5 octobre 2026 : une principale
avec un ou plusieurs secours autorisés et qualifiés, une seule passerelle
active par périmètre de routage cohérent. Les ressources partageant le retour
sont regroupées, sauf séparation explicitement qualifiée. Priorités et
départage sont déterministes. PA exécute un basculement après une défaillance
vérifiée, selon une décision courante de l'autorité compétente ou un mandat
explicite encore valide. L'option B de répartition entre plusieurs passerelles
actives n'est pas retenue comme mode de référence.

PA vérifie le chemin utile jusqu'à une ressource ou une sonde autorisée ;
processus, interface et handshake WireGuard seuls ne suffisent pas. Il
vérifie ses preuves et sa configuration, applique le plan autorisé et
rapporte les routes et le filtrage réellement appliqués. La convergence
comprend les retours côté destination, provisionnés par l'opérateur ou par
un mécanisme explicitement autorisé ; un retour via l'ancienne passerelle
ne vaut pas basculement réussi.

Le profil empêche des décisions actives contradictoires et la réutilisation
d'un mandat obsolète après panne ou restauration. Coordination, preuves
d'autorité et partitions suivent A12a–A12g validés ; modalités à qualifier.
Sans preuve ou chemin
indispensable vérifiable, l'accès concerné est bloqué selon A05, sans NAT
de secours ni communication hors PZT. Le retour vers la principale suit
une règle de stabilité déclarée et une autorisation valide ; les temporisations
ne prolongent ni permission ni délai de révocation.

Seuils, fenêtres, détection, convergence, consommation et effets sur les
sessions restent à qualifier ; l'absence de NAT ne garantit pas leur
continuité. Le rôle est qualifié par plateforme, avec les contraintes des
machines physiques et VM Linux/Windows et de Docker/LXC Proxmox. Aucun
protocole de redondance, bibliothèque, privilège hôte ou changement Proxmox
n'est choisi. Les sources figurent dans le cadrage PZT.

#### Scenario: Conformité du traitement A08c

- **WHEN** un profil revendique le traitement A08c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

