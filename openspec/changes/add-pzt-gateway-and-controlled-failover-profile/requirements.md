# Références normatives — Z08

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

