# Références normatives — Z07

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pzt | Découverte, chemins et relais chiffrés | 1 | pzt-97fdb0de58ec |
| pzt | Contrat A09a — Découverte des chemins ICE/STUN, option A validée | 1 | pzt-e8cea9286485 |
| pzt | Contrat A09b — Relais UDP avec secours WSS, option A validée | 1 | pzt-66ad8e558680 |
| pzt | Contrat A09c — QUIC avec DATAGRAM pour les relais UDP, option A validée | 1 | pzt-78e2da0ffc80 |
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

### Référence courante pzt-97fdb0de58ec

Source : [pzt](../../specs/pzt/spec.md), ligne 167. SHA-256 : `97fdb0de58ecc3ca8f258ea6441c359376310cd8e43da77f79e256adc49f4e10`.

Scénarios : Découverte, chemins et relais chiffrés.

~~~~text
### Requirement: Découverte, chemins et relais chiffrés

La découverte MUST exposer uniquement les pairs et destinations autorisés. Direct MUST être prioritaire ; ICE/STUN, relais QUIC DATAGRAM puis secours WSS MUST suivre les mandats et limites A09a–A09c. Le relais MUST NOT déchiffrer WireGuard ni remplacer les datagrammes par un stream fiable implicite. MTU, pertes, congestion, sondes, signalisation et résidence MUST être qualifiés.

#### Scenario: Découverte, chemins et relais chiffrés

- **WHEN** aucun chemin autorisé n'est disponible
- **THEN** la communication échoue explicitement sans chemin de contournement
~~~~

### Référence courante pzt-e8cea9286485

Source : [pzt](../../specs/pzt/spec.md), ligne 1910. SHA-256 : `e8cea928648568f535bea68eb752256e3cdae3b8a95e7489005ac7dd68be3cef`.

Scénarios : Conformité du traitement A09a.

~~~~text
### Requirement: Contrat A09a — Découverte des chemins ICE/STUN, option A validée

Le rôle chargé du traitement A09a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A09a

Ce choix concerne l'établissement des tunnels WireGuard entre PA admis,
y compris le contrôle PBO, selon les profils A01–A07. La traversée des NAT
du réseau physique est distincte de l'absence de NAT sur le segment
passerelle–ressource validée en A08b. La découverte d'un chemin n'accorde
ni admission, ni permission d'accès, ni rôle d'autorité.

L'option A est validée par le développeur le 5 octobre 2026 : ICE/STUN
est utilisé pour collecter les endpoints candidats,
tester leur joignabilité entre pairs et sélectionner un chemin direct
compatible avec le profil. Les candidats locaux et les adresses/ports
observés via STUN sont traités selon le périmètre réseau autorisé ; les
candidats appris lors des vérifications suivent les procédures qualifiées.
La signalisation et le rendez-vous sont développés dans PZT, avec des
contrats propres ; les services nécessaires sont exploités par l'opérateur.
Un relais autorisé reste disponible si le direct échoue selon les limites
déclarées. La décision couvre les topologies physiques, virtuelles et
conteneurisées demandées, sous réserve de qualification ; elle ne garantit
pas un chemin direct à travers tout NAT ou filtrage.

L'option B de rendez-vous limité avec davantage de recours aux relais
n'est pas retenue comme mode de référence.

Seuls les pairs et services autorisés reçoivent les
candidats nécessaires à leur contexte. Les messages de signalisation sont
protégés contre lecture, usurpation et rejeu, liés aux identités et à la
validité de la relation. Ils empruntent les contrats de contrôle PZT déclarés,
sans exposer les modèles privés ou les clés WireGuard privées. L'amorçage
A02/A03 doit permettre de joindre le contrôle avant cette découverte ;
ICE ne résout pas à lui seul la joignabilité de sa signalisation.

Le profil validé distingue la signalisation chiffrée PZT, les
sondes techniques ICE/STUN précédant le tunnel et les données chiffrées
WireGuard. Les sondes STUN UDP standard n'assurent pas la confidentialité
des métadonnées échangées ; leur exposition minimale, les contrôles
d'intégrité et d'authentification applicables, les destinataires et les
limites sont à spécifier. Elles ne transportent aucune donnée métier ni
clé privée et ne constituent aucun canal alternatif de contrôle PBO–PA.
Ce profil de sondes est inclus dans la décision validée ; il ne permet
aucun autre échange non chiffré de données ou de contrôle PZT.

Les candidats doivent correspondre au chemin UDP réellement utilisable par
le backend WireGuard. Un test réussi depuis un autre socket ne prouve pas
que le mapping NAT du socket WireGuard fonctionne ; partage, multiplexage
ou adaptation du socket et leurs privilèges sont à qualifier pour chaque
backend natif ou utilisateur. Une bibliothèque ICE ne démontre pas à elle
seule cette intégration. IPv6 désactivé selon A06a exclut aussi les candidats,
les endpoints de services auxiliaires et les sondes IPv6 propres à PZT.

Candidats, essais simultanés, fréquences, délais et reprises sont bornés par
profil, sans scan général du réseau ni modification implicite des routeurs,
pare-feu, droits de conteneur ou paramètres Proxmox. Changement d'interface,
de réseau ou de mapping entraîne une réévaluation du chemin et des conditions
de politique concernées ; sondes et keepalives ne renouvellent aucun droit.
Sans chemin autorisé compatible, l'échec est diagnostiqué et l'accès bloqué.
CPU, mémoire, trafic de sondes, délai de connexion et charge des relais sont
comparés sur Linux/Windows physiques et VM, Docker/LXC Proxmox, avec NAT
multiples, UDP bloqué et changement de réseau.

[ICE, RFC 8445](https://www.rfc-editor.org/rfc/rfc8445.html) décrit la recherche
et les vérifications de chemins UDP ; [STUN, RFC 8489](https://www.rfc-editor.org/rfc/rfc8489.html)
fournit notamment l'observation des mappings et n'est pas une solution de
traversée complète à lui seul. [L'architecture officielle NetBird](https://docs.netbird.io/about-netbird/how-netbird-works)
sert de référence fonctionnelle pour la distinction signalisation, connexion
directe et relais. Aucune brique, API ou bibliothèque NetBird n'est reprise.
Les versions, mises à jour normatives, bibliothèques indépendantes et budgets
restent à choisir et qualifier. A09b, option A validée, fixe UDP prioritaire
avec secours WSS ; A09c, option A validée, retient QUIC avec DATAGRAM. La décision
A09a seule ne sélectionne ni TURN, ni QUIC, ni TCP ou WebSocket de relais.

##### Application au PA — A09a

Le choix concerne les tunnels WireGuard entre PA admis et le contrôle PBO.
La traversée des NAT du réseau physique est distincte du transfert sans NAT
vers les ressources A08b ; découvrir un chemin n'accorde aucun accès.

L'option A est validée par le développeur le 5 octobre 2026 : PA intègre
ICE/STUN pour collecter les endpoints candidats,
vérifier leur joignabilité entre pairs et privilégier un chemin direct
compatible. Signalisation et rendez-vous sont développés dans PZT avec
services exploités par l'opérateur ; un relais autorisé reste disponible
en cas d'échec direct selon les limites du profil. Les topologies demandées
restent à qualifier, sans garantie de direct à travers tout NAT ou filtrage.

L'option B de rendez-vous limité avec davantage de recours aux relais
n'est pas retenue comme mode de référence.

PA limite collecte et distribution au contexte
réseau autorisé. La signalisation protégée contre lecture, usurpation et
rejeu utilise les contrats PZT déclarés ; identité, contexte et validité
sont vérifiés sans transmettre de clé WireGuard privée. L'amorçage A02/A03
permet de joindre le contrôle avant cette découverte ; ICE ne remplace pas
ce prérequis.

Les sondes techniques ICE/STUN précédant le tunnel sont
distinguées de la signalisation chiffrée et des données WireGuard. STUN UDP
standard ne chiffre pas les métadonnées des sondes : leur exposition minimale,
les contrôles d'intégrité et d'authentification applicables et les limites
sont à spécifier. Aucune donnée métier, clé privée ou commande alternative
PBO–PA ne passe par ces sondes ; ce profil technique est inclus dans la
décision validée, sans autoriser d'autre contrôle ou donnée PZT en clair.

Le chemin vérifié doit être utilisable par le socket UDP du backend
WireGuard ; un test depuis un socket indépendant ne prouve pas son mapping
NAT. Partage, multiplexage ou adaptation sont qualifiés séparément pour
chaque backend, sans privilège implicite. IPv6 désactivé exclut aussi les
candidats, services auxiliaires et sondes IPv6 propres à PZT. Essais,
concurrence, délais et reprises restent bornés ; aucune modification
implicite des routeurs, pare-feu, montages ou droits Proxmox n'est engagée.
Changement de réseau ou de mapping impose une réévaluation ; sondes et
keepalives ne renouvellent aucune permission. Sans chemin compatible et
autorisé, PA rapporte l'échec et bloque l'accès.

CPU, mémoire, sondes, connexion et trafic relayé sont comparés par plateforme :
Linux/Windows physiques et VM, Docker/LXC Proxmox, NAT multiples, UDP bloqué
et mobilité. Bibliothèques, versions normatives et budgets restent à choisir.
Les sources officielles figurent dans le cadrage PZT. A09b, option A validée,
fixe UDP prioritaire avec secours WSS ; A09c, option A validée, retient
QUIC avec DATAGRAM pour les relais UDP. A09a seule ne sélectionne ni TURN, ni QUIC, ni TCP ou WebSocket de relais.

#### Scenario: Conformité du traitement A09a

- **WHEN** un profil revendique le traitement A09a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence courante pzt-66ad8e558680

Source : [pzt](../../specs/pzt/spec.md), ligne 2045. SHA-256 : `66ad8e5586808c3eb96e21559a4719beceb3aea736c1842da2cb4bb8a013ea36`.

Scénarios : Conformité du traitement A09b.

~~~~text
### Requirement: Contrat A09b — Relais UDP avec secours WSS, option A validée

Le rôle chargé du traitement A09b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A09b

Cet arbitrage concerne le transport des paquets WireGuard déjà chiffrés
lorsqu'un chemin direct compatible A09a n'est pas disponible. Un relais
transporte ces paquets sans terminer le tunnel entre les pairs, sans clés
privées WireGuard et sans devenir une passerelle A08 ou une autorité A12.
Les services de relais et leurs contrats sont développés dans PZT et
exploités par l'opérateur ; aucune brique NetBird n'est utilisée.

L'option A est validée par le développeur le 5 octobre 2026 : le relais
prend en charge un transport UDP prioritaire et un secours WebSocket sur
TLS (WSS), porté par TCP, lorsque le
chemin UDP autorisé est indisponible. Un adapter PZT encapsule les paquets
WireGuard dans ce transport ; le backend WireGuard conserve son protocole
UDP natif. Ce choix couvre aussi les réseaux où UDP est bloqué mais WSS
est autorisé et joignable, sous réserve de qualification. Il ne garantit pas
la traversée de tous les pare-feu ou proxies ; le support et l'autorisation
de chaque chemin restent nécessaires.

L'option B de relais UDP seuls n'est pas retenue comme mode de référence.

Chaque liaison PA–relais est authentifiée et autorisée
pour des pairs, un contexte et une durée bornée. Le relais refuse le transit
libre, les allocations hors mandat et les destinations non autorisées.
Validité, révocation, quotas et résidence restent opposables, y compris aux
liaisons persistantes ; changer de transport ne renouvelle aucun droit.
Les mécanismes standards d'authentification et de protection du transport
UDP sont fixés par A09c, option A validée : QUIC avec DATAGRAM. Le choix
A09b porte sur la couverture UDP/WSS ; les bibliothèques restent à définir.
Le chiffrement WireGuard de bout en bout est maintenu dans tous les cas.

Les endpoints WSS, ancrages TLS, authentification du PA et
permissions de relais sont vérifiés avant transfert. Un échec de preuve,
de certificat ou de permission bloque l'accès concerné ; il n'est pas
assimilé à une panne de transport permettant de contourner le refus.
Les proxies ne sont utilisés que selon une configuration autorisée et
qualifiée ; les contrôles TLS ne sont pas désactivés. La connexion WSS est
un transport PZT interne déclaré, distinct du canal de notifications et
retours JSON A07c ; SSE ne transporte pas les paquets WireGuard.

La sélection suit une politique déterministe versionnée : direct admissible
prioritaire, puis relais UDP admissible, puis WSS admissible. Les échecs de transport, budgets d'essais, fenêtres de stabilité
et conditions de retour vers UDP ou le direct sont déclarés et restent à
calibrer. Aucun second transport de données permanent n'est entretenu pour
mesurer son coût ; un chevauchement de transition éventuel est borné et
qualifié. Une politique imposée ou une contrainte de sécurité reste prioritaire
sur cette préférence, sans repli automatique vers un mode non autorisé.

L'adapter conserve les limites des datagrammes et la liaison avec le pair
WireGuard destinataire ; il ne capture ni ne transfère de paquets applicatifs
en clair. Le cadrage binaire, tailles maximales, MTU, buffers, files, délais
et traitement des dépassements sont spécifiés et bornés. L'intégration
avec les sockets des backends A01 et les liaisons où un PA utilise UDP et
l'autre WSS, si exposées, sont qualifiées séparément. Une reprise vérifie
l'état courant ; aucune file ne remet en circulation un flux expiré ou
révoqué. Engorgement et pertes sont diagnostiqués sans mémoire illimitée.

IPv6 désactivé A06a exclut aussi les endpoints et transports IPv6 des relais.
CPU, mémoire, trafic, connexions, débit, latence sous pertes, délais de
basculement et charge des services exécutés par les PA sont mesurés sur
Linux/Windows physiques et VM, Docker/LXC Proxmox. Le transport TCP peut
retarder des paquets derrière une retransmission ; l'impact sur les flux
TCP et UDP encapsulés est qualifié. Les délais A05 restent applicables,
sans promesse de continuité des sessions ou d'économie de ressources.
Aucun privilège, montage, port fixe ou changement Proxmox n'est introduit.

[WireGuard documente son transport UDP](https://www.wireguard.com/protocol/) ;
[WebSocket, RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html), définit
un transport sur TCP et sa protection TLS en WSS. La
[documentation officielle NetBird sur les relais](https://docs.netbird.io/about-netbird/understanding-nat-and-connectivity#netbird-relay)
décrit QUIC/UDP avec secours WebSocket ; elle sert de référence fonctionnelle.
PZT ne reprend ni son protocole, ni sa course simultanée des transports,
ni ses performances ou paramètres. La décision A09b reste à qualifier par
profil ; A09c, option A validée, fixe QUIC avec DATAGRAM pour l'UDP.

##### Application au PA — A09b

Le relais transporte les paquets WireGuard déjà chiffrés entre pairs admis,
sans terminer leur tunnel ni posséder leurs clés privées. Son rôle reste
distinct de la passerelle A08 et de l'autorité A12 ; les contrats et adapters
sont développés dans PZT, sans brique NetBird.

L'option A est validée par le développeur le 5 octobre 2026 : PA utilise
un transport de relais UDP prioritaire avec secours WebSocket sur TLS
(WSS), porté par TCP, si le chemin UDP autorisé
est indisponible. PA encapsule les paquets WireGuard via un adapter PZT ;
WireGuard conserve son UDP natif. Ce choix couvre les réseaux où WSS reste
permis malgré un blocage UDP, sous réserve de qualification, sans garantie
de passage à travers tous les proxies ou pare-feu.

L'option B de relais UDP seuls n'est pas retenue comme mode de référence.

PA authentifie la liaison avec le relais et présente une autorisation
liée aux pairs, au contexte et à une durée bornée. Quotas, résidence,
révocation et expiration restent opposables ; basculer ou maintenir une
connexion ne renouvelle aucun droit. Le mécanisme standard de protection
et d'authentification du transport UDP est fixé par A09c, option A validée :
QUIC avec DATAGRAM, bibliothèques à définir ; WireGuard chiffre toujours
les données de bout en bout.

PA vérifie endpoint WSS, ancrage TLS, authentification et
permission avant transfert. Un refus de certificat, de preuve ou de droit
ne déclenche aucun contournement. Les proxies sont configurés et qualifiés
explicitement, sans désactiver les contrôles TLS. Ce transport de paquets
est distinct des notifications et retours JSON A07c ; SSE ne relaie pas
les paquets WireGuard.

La politique déterministe versionnée privilégie le direct admissible,
puis UDP relayé admissible et WSS admissible. Politique
imposée et sécurité restent prioritaires. Essais, fenêtres de stabilité,
retour à UDP ou au direct et chevauchement éventuel de transition sont
bornés et à calibrer, sans second transport de données permanent pour
mesurer son coût. Aucun passage vers un mode non autorisé n'est permis.

L'adapter préserve les limites des datagrammes et le pair destinataire,
sans transfert de données applicatives en clair. Cadrage binaire, tailles,
MTU, buffers, files, dépassements et intégration au socket WireGuard sont
qualifiés par backend ; les liaisons mixtes UDP/WSS, si exposées, sont
qualifiées séparément. Reprise et files respectent l'état courant et les
échéances A05, sans émission d'un flux révoqué ou expiré.

IPv6 désactivé exclut les endpoints et transports IPv6 des relais. CPU,
mémoire, sondes, trafic, connexions, latence sous pertes, débit et basculement
sont mesurés par plateforme Linux/Windows physique et VM, Docker/LXC Proxmox,
y compris sur les PA portant le rôle relais. Retransmissions TCP et files
peuvent retarder les flux ; les sessions ne sont pas présumées continues.
Aucun gain de ressources, privilège, montage ou changement Proxmox n'est
présumé. Les sources officielles figurent dans le cadrage PZT.
La décision A09b reste à qualifier par profil ; A09c, option A validée,
fixe QUIC avec DATAGRAM pour le transport UDP.

#### Scenario: Conformité du traitement A09b

- **WHEN** un profil revendique le traitement A09b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence courante pzt-78e2da0ffc80

Source : [pzt](../../specs/pzt/spec.md), ligne 2190. SHA-256 : `78e2da0ffc80ac88e1f0594b817b53307a7774489be07ed84bbb5e98a09d746d`.

Scénarios : Conformité du traitement A09c.

~~~~text
### Requirement: Contrat A09c — QUIC avec DATAGRAM pour les relais UDP, option A validée

Le rôle chargé du traitement A09c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A09c

Ce choix complète le transport UDP prioritaire avec secours WSS validé
A09b. Il concerne les liaisons PA–relais ; le direct reste WireGuard sur
UDP et le relais transporte des paquets WireGuard déjà chiffrés entre PA.
Le contrôle PBO et les notifications A07 conservent leurs contrats.

L'option A est validée par le développeur le 5 octobre 2026 : PZT utilise
QUIC avec sa protection TLS et l'extension DATAGRAM pour les paquets
WireGuard relayés. Les datagrammes perdus ne sont pas
retransmis automatiquement par cette extension ; ils restent soumis au
contrôle de congestion QUIC. Les streams fiables ne sont pas utilisés comme
substitut pour les paquets WireGuard du profil UDP. Les éventuels échanges
internes de gestion du relais sont bornés, déclarés et distincts des
Commands et Queries PBO. Le transport s'appuie sur les mécanismes standards
de gestion de connexion et de congestion QUIC ; consommation et performances
restent à qualifier.

L'option B de protection par DTLS 1.3 n'est pas retenue comme mécanisme
UDP de référence pour les relais.

PZT développe la gestion des circuits et l'adapter
avec des bibliothèques standards indépendantes à sélectionner. Le pair,
le contexte et le circuit sont liés à une permission vérifiable ; le
handshake de transport ne vaut pas autorisation métier. Identités, formats
de preuve et ancrages restent à préciser en A10. Expiration, révocation,
quotas et résidence A05/A09b restent opposables. Une reprise de session TLS
ou un ticket de transport ne restaure ni ne prolonge un mandat. Le profil
validé n'autorise pas de transfert ou d'allocation en données précoces
0-RTT avant vérification courante de la relation et de ses preuves.

Le support DATAGRAM et ses limites sont vérifiés pour chaque
liaison. Une incompatibilité ne transforme pas silencieusement les paquets
en stream fiable ; le secours WSS n'est engagé que selon la politique
validée A09b. Tailles de datagrammes, surcharge d'encapsulation, MTU du
chemin et MTU WireGuard sont qualifiées ensemble ; l'extension DATAGRAM
ne fragmente pas ses frames. Un paquet trop grand est traité et diagnostiqué
selon un contrat borné, sans présumer une fragmentation transparente.

Les identifiants de circuit et leur traitement préservent l'isolation entre
pairs et contextes. Files, buffers, états de connexion, reconnexions,
anti-rejeu et limites anti-abus sont bornés et diagnostiqués. Un changement
d'adresse ou une migration de transport réévalue les conditions du profil,
sans renouveler un droit ; les données périmées ou révoquées ne sont pas
réémises depuis une file. Le relais termine la protection QUIC de sa liaison,
mais ne déchiffre pas les données WireGuard entre PA.

IPv6 désactivé A06a reste exclu des endpoints et transports PZT. Les tests
couvrent Linux/Windows physiques et VM, Docker/LXC Proxmox, backends A01,
pertes, réordonnancement, MTU réduite, changement de réseau et secours WSS.
CPU, mémoire, états, sondes, débit et latence sont comparés côté PA et relais,
y compris lorsque le relais est exécuté par un PA pour le PBO. Aucune
bibliothèque, dépendance, version d'OS, privilège ou modification Proxmox
n'est choisie par cette décision ; les profils de bibliothèques et leurs
versions normatives restent à valider et qualifier. HTTP/3, WebTransport
et une API QUIC métier ne sont pas introduits par le choix de QUIC.

[QUIC, RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), et sa
[protection TLS, RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html),
définissent le transport sécurisé ; [DATAGRAM, RFC 9221](https://www.rfc-editor.org/rfc/rfc9221.html),
définit les datagrammes sans retransmission. [DTLS 1.3, RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.html),
définit l'alternative de protection sur datagrammes. Ces standards servent
au développement propre PZT ; aucune brique NetBird n'est reprise.
La décision fixe QUIC avec DATAGRAM ; les interfaces, bibliothèques et
paramètres de qualification restent à spécifier.

##### Application au PA — A09c

Ce choix concerne la liaison PA–relais UDP A09b ; le direct conserve
WireGuard sur UDP, et les paquets relayés restent chiffrés entre PA.
Le contrôle PBO et les notifications A07 conservent leurs contrats.

L'option A est validée par le développeur le 5 octobre 2026 : PA utilise
QUIC protégé par TLS avec l'extension DATAGRAM pour les paquets WireGuard, sans retransmission automatique des datagrammes
perdus et avec contrôle de congestion QUIC. Les streams fiables ne servent
pas de substitut aux paquets du profil UDP ; les éventuels échanges internes
de gestion du relais restent déclarés et bornés. La gestion de connexion
et de congestion est celle du transport QUIC, sans gain présumé de ressources
ou de performances.

L'option B de protection par DTLS 1.3 n'est pas retenue comme mécanisme
UDP de référence pour les relais.

PA utilise un adapter PZT et une bibliothèque standard indépendante à
sélectionner, avec circuit lié au pair, au contexte et à une permission
vérifiable. Le handshake de transport ne remplace pas l'autorisation.
Formats et ancrages A10 restent à définir ; les garanties A05/A09b sont
maintenues. Reprise TLS et tickets ne restaurent ni ne prolongent un mandat.
Le profil validé exclut transfert et allocation en données précoces
0-RTT avant vérification courante des preuves et de la relation.

PA vérifie le support DATAGRAM, les tailles négociées et
la compatibilité avec les MTU WireGuard et du chemin. Une incompatibilité
ne provoque pas de passage silencieux en stream fiable ; WSS suit la
politique A09b. DATAGRAM ne fragmente pas ses frames ; les paquets trop
grands suivent un traitement déclaré, borné et diagnostiqué.

Circuits, états, files, buffers, reprise, anti-rejeu et anti-abus sont
qualifiés et bornés par contexte. Changement de réseau ou migration du
transport réévalue le profil sans renouveler de permission. Le relais
termine la protection QUIC de sa liaison sans pouvoir déchiffrer
les données WireGuard entre PA. IPv6 désactivé reste exclu des transports PZT.

Qualification et comparaison CPU, mémoire, trafic, états, pertes, MTU et
latence couvrent les PA Linux/Windows physiques et VM, Docker/LXC Proxmox,
les backends A01 et les PA portant le relais, avec secours WSS. Aucune
bibliothèque, dépendance, version d'OS ou permission hôte n'est sélectionnée.
HTTP/3, WebTransport et une API métier QUIC ne sont pas introduits.
Les sources officielles figurent dans le cadrage PZT. QUIC avec DATAGRAM est
retenu ; interfaces, bibliothèques et paramètres restent à spécifier et qualifier.

#### Scenario: Conformité du traitement A09c

- **WHEN** un profil revendique le traitement A09c et ses garanties dans un rôle déclaré
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
| pzt / 102 | [Découverte, chemins et relais chiffrés](../../specs/pzt/spec.md#L102) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1957 | [Contrat A09a — Découverte des chemins ICE/STUN, option A validée](../../specs/pzt/spec.md#L1957) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2092 | [Contrat A09b — Relais UDP avec secours WSS, option A validée](../../specs/pzt/spec.md#L2092) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2237 | [Contrat A09c — QUIC avec DATAGRAM pour les relais UDP, option A validée](../../specs/pzt/spec.md#L2237) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--7c8aaf6a4f

Source : `openspec/specs/pzt/spec.md`, ligne 102. SHA-256 du bloc : `f43f522d60a0c9946438b45e738166c241c15f2f3cb53a3743f54efe91a2fd58`.

~~~~text
### Requirement: Découverte, chemins et relais chiffrés

La découverte MUST exposer uniquement les pairs et destinations autorisés. Direct MUST être prioritaire ; ICE/STUN, relais QUIC DATAGRAM puis secours WSS MUST suivre les mandats et limites A09a–A09c. Le relais MUST NOT déchiffrer WireGuard ni remplacer les datagrammes par un stream fiable implicite. MTU, pertes, congestion, sondes, signalisation et résidence MUST être qualifiés.

#### Scenario: Découverte, chemins et relais chiffrés

- **WHEN** aucun chemin autorisé n'est disponible
- **THEN** la communication échoue explicitement sans chemin de contournement
~~~~

### Référence pzt--c881bca702

Source : `openspec/specs/pzt/spec.md`, ligne 1957. SHA-256 du bloc : `93c30a8a452a78304a8d6e358dc9ea44eb8ec7ca12abb18cbd5292bccd2f0635`.

~~~~text
### Requirement: Contrat A09a — Découverte des chemins ICE/STUN, option A validée

Le rôle chargé du traitement A09a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A09a

Ce choix concerne l'établissement des tunnels WireGuard entre PA admis,
y compris le contrôle PBO, selon les profils A01–A07. La traversée des NAT
du réseau physique est distincte de l'absence de NAT sur le segment
passerelle–ressource validée en A08b. La découverte d'un chemin n'accorde
ni admission, ni permission d'accès, ni rôle d'autorité.

L'option A est validée par le développeur le 5 octobre 2026 : ICE/STUN
est utilisé pour collecter les endpoints candidats,
tester leur joignabilité entre pairs et sélectionner un chemin direct
compatible avec le profil. Les candidats locaux et les adresses/ports
observés via STUN sont traités selon le périmètre réseau autorisé ; les
candidats appris lors des vérifications suivent les procédures qualifiées.
La signalisation et le rendez-vous sont développés dans PZT, avec des
contrats propres ; les services nécessaires sont exploités par l'opérateur.
Un relais autorisé reste disponible si le direct échoue selon les limites
déclarées. La décision couvre les topologies physiques, virtuelles et
conteneurisées demandées, sous réserve de qualification ; elle ne garantit
pas un chemin direct à travers tout NAT ou filtrage.

L'option B de rendez-vous limité avec davantage de recours aux relais
n'est pas retenue comme mode de référence.

Seuls les pairs et services autorisés reçoivent les
candidats nécessaires à leur contexte. Les messages de signalisation sont
protégés contre lecture, usurpation et rejeu, liés aux identités et à la
validité de la relation. Ils empruntent les contrats de contrôle PZT déclarés,
sans exposer les modèles privés ou les clés WireGuard privées. L'amorçage
A02/A03 doit permettre de joindre le contrôle avant cette découverte ;
ICE ne résout pas à lui seul la joignabilité de sa signalisation.

Le profil validé distingue la signalisation chiffrée PZT, les
sondes techniques ICE/STUN précédant le tunnel et les données chiffrées
WireGuard. Les sondes STUN UDP standard n'assurent pas la confidentialité
des métadonnées échangées ; leur exposition minimale, les contrôles
d'intégrité et d'authentification applicables, les destinataires et les
limites sont à spécifier. Elles ne transportent aucune donnée métier ni
clé privée et ne constituent aucun canal alternatif de contrôle PBO–PA.
Ce profil de sondes est inclus dans la décision validée ; il ne permet
aucun autre échange non chiffré de données ou de contrôle PZT.

Les candidats doivent correspondre au chemin UDP réellement utilisable par
le backend WireGuard. Un test réussi depuis un autre socket ne prouve pas
que le mapping NAT du socket WireGuard fonctionne ; partage, multiplexage
ou adaptation du socket et leurs privilèges sont à qualifier pour chaque
backend natif ou utilisateur. Une bibliothèque ICE ne démontre pas à elle
seule cette intégration. IPv6 désactivé selon A06a exclut aussi les candidats,
les endpoints de services auxiliaires et les sondes IPv6 propres à PZT.

Candidats, essais simultanés, fréquences, délais et reprises sont bornés par
profil, sans scan général du réseau ni modification implicite des routeurs,
pare-feu, droits de conteneur ou paramètres Proxmox. Changement d'interface,
de réseau ou de mapping entraîne une réévaluation du chemin et des conditions
de politique concernées ; sondes et keepalives ne renouvellent aucun droit.
Sans chemin autorisé compatible, l'échec est diagnostiqué et l'accès bloqué.
CPU, mémoire, trafic de sondes, délai de connexion et charge des relais sont
comparés sur Linux/Windows physiques et VM, Docker/LXC Proxmox, avec NAT
multiples, UDP bloqué et changement de réseau.

[ICE, RFC 8445](https://www.rfc-editor.org/rfc/rfc8445.html) décrit la recherche
et les vérifications de chemins UDP ; [STUN, RFC 8489](https://www.rfc-editor.org/rfc/rfc8489.html)
fournit notamment l'observation des mappings et n'est pas une solution de
traversée complète à lui seul. [L'architecture officielle NetBird](https://docs.netbird.io/about-netbird/how-netbird-works)
sert de référence fonctionnelle pour la distinction signalisation, connexion
directe et relais. Aucune brique, API ou bibliothèque NetBird n'est reprise.
Les versions, mises à jour normatives, bibliothèques indépendantes et budgets
restent à choisir et qualifier. A09b, option A validée, fixe UDP prioritaire
avec secours WSS ; A09c, option A validée, retient QUIC avec DATAGRAM. La décision
A09a seule ne sélectionne ni TURN, ni QUIC, ni TCP ou WebSocket de relais.

##### Application au PA — A09a

Le choix concerne les tunnels WireGuard entre PA admis et le contrôle PBO.
La traversée des NAT du réseau physique est distincte du transfert sans NAT
vers les ressources A08b ; découvrir un chemin n'accorde aucun accès.

L'option A est validée par le développeur le 5 octobre 2026 : PA intègre
ICE/STUN pour collecter les endpoints candidats,
vérifier leur joignabilité entre pairs et privilégier un chemin direct
compatible. Signalisation et rendez-vous sont développés dans PZT avec
services exploités par l'opérateur ; un relais autorisé reste disponible
en cas d'échec direct selon les limites du profil. Les topologies demandées
restent à qualifier, sans garantie de direct à travers tout NAT ou filtrage.

L'option B de rendez-vous limité avec davantage de recours aux relais
n'est pas retenue comme mode de référence.

PA limite collecte et distribution au contexte
réseau autorisé. La signalisation protégée contre lecture, usurpation et
rejeu utilise les contrats PZT déclarés ; identité, contexte et validité
sont vérifiés sans transmettre de clé WireGuard privée. L'amorçage A02/A03
permet de joindre le contrôle avant cette découverte ; ICE ne remplace pas
ce prérequis.

Les sondes techniques ICE/STUN précédant le tunnel sont
distinguées de la signalisation chiffrée et des données WireGuard. STUN UDP
standard ne chiffre pas les métadonnées des sondes : leur exposition minimale,
les contrôles d'intégrité et d'authentification applicables et les limites
sont à spécifier. Aucune donnée métier, clé privée ou commande alternative
PBO–PA ne passe par ces sondes ; ce profil technique est inclus dans la
décision validée, sans autoriser d'autre contrôle ou donnée PZT en clair.

Le chemin vérifié doit être utilisable par le socket UDP du backend
WireGuard ; un test depuis un socket indépendant ne prouve pas son mapping
NAT. Partage, multiplexage ou adaptation sont qualifiés séparément pour
chaque backend, sans privilège implicite. IPv6 désactivé exclut aussi les
candidats, services auxiliaires et sondes IPv6 propres à PZT. Essais,
concurrence, délais et reprises restent bornés ; aucune modification
implicite des routeurs, pare-feu, montages ou droits Proxmox n'est engagée.
Changement de réseau ou de mapping impose une réévaluation ; sondes et
keepalives ne renouvellent aucune permission. Sans chemin compatible et
autorisé, PA rapporte l'échec et bloque l'accès.

CPU, mémoire, sondes, connexion et trafic relayé sont comparés par plateforme :
Linux/Windows physiques et VM, Docker/LXC Proxmox, NAT multiples, UDP bloqué
et mobilité. Bibliothèques, versions normatives et budgets restent à choisir.
Les sources officielles figurent dans le cadrage PZT. A09b, option A validée,
fixe UDP prioritaire avec secours WSS ; A09c, option A validée, retient
QUIC avec DATAGRAM pour les relais UDP. A09a seule ne sélectionne ni TURN, ni QUIC, ni TCP ou WebSocket de relais.

#### Scenario: Conformité du traitement A09a

- **WHEN** un profil revendique le traitement A09a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--253cb3dd9e

Source : `openspec/specs/pzt/spec.md`, ligne 2092. SHA-256 du bloc : `55f022ca6d34cd182acad6281631cde39d3b752f353be7f8b73b856c9a346f9c`.

~~~~text
### Requirement: Contrat A09b — Relais UDP avec secours WSS, option A validée

Le rôle chargé du traitement A09b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A09b

Cet arbitrage concerne le transport des paquets WireGuard déjà chiffrés
lorsqu'un chemin direct compatible A09a n'est pas disponible. Un relais
transporte ces paquets sans terminer le tunnel entre les pairs, sans clés
privées WireGuard et sans devenir une passerelle A08 ou une autorité A12.
Les services de relais et leurs contrats sont développés dans PZT et
exploités par l'opérateur ; aucune brique NetBird n'est utilisée.

L'option A est validée par le développeur le 5 octobre 2026 : le relais
prend en charge un transport UDP prioritaire et un secours WebSocket sur
TLS (WSS), porté par TCP, lorsque le
chemin UDP autorisé est indisponible. Un adapter PZT encapsule les paquets
WireGuard dans ce transport ; le backend WireGuard conserve son protocole
UDP natif. Ce choix couvre aussi les réseaux où UDP est bloqué mais WSS
est autorisé et joignable, sous réserve de qualification. Il ne garantit pas
la traversée de tous les pare-feu ou proxies ; le support et l'autorisation
de chaque chemin restent nécessaires.

L'option B de relais UDP seuls n'est pas retenue comme mode de référence.

Chaque liaison PA–relais est authentifiée et autorisée
pour des pairs, un contexte et une durée bornée. Le relais refuse le transit
libre, les allocations hors mandat et les destinations non autorisées.
Validité, révocation, quotas et résidence restent opposables, y compris aux
liaisons persistantes ; changer de transport ne renouvelle aucun droit.
Les mécanismes standards d'authentification et de protection du transport
UDP sont fixés par A09c, option A validée : QUIC avec DATAGRAM. Le choix
A09b porte sur la couverture UDP/WSS ; les bibliothèques restent à définir.
Le chiffrement WireGuard de bout en bout est maintenu dans tous les cas.

Les endpoints WSS, ancrages TLS, authentification du PA et
permissions de relais sont vérifiés avant transfert. Un échec de preuve,
de certificat ou de permission bloque l'accès concerné ; il n'est pas
assimilé à une panne de transport permettant de contourner le refus.
Les proxies ne sont utilisés que selon une configuration autorisée et
qualifiée ; les contrôles TLS ne sont pas désactivés. La connexion WSS est
un transport PZT interne déclaré, distinct du canal de notifications et
retours JSON A07c ; SSE ne transporte pas les paquets WireGuard.

La sélection suit une politique déterministe versionnée : direct admissible
prioritaire, puis relais UDP admissible, puis WSS admissible. Les échecs de transport, budgets d'essais, fenêtres de stabilité
et conditions de retour vers UDP ou le direct sont déclarés et restent à
calibrer. Aucun second transport de données permanent n'est entretenu pour
mesurer son coût ; un chevauchement de transition éventuel est borné et
qualifié. Une politique imposée ou une contrainte de sécurité reste prioritaire
sur cette préférence, sans repli automatique vers un mode non autorisé.

L'adapter conserve les limites des datagrammes et la liaison avec le pair
WireGuard destinataire ; il ne capture ni ne transfère de paquets applicatifs
en clair. Le cadrage binaire, tailles maximales, MTU, buffers, files, délais
et traitement des dépassements sont spécifiés et bornés. L'intégration
avec les sockets des backends A01 et les liaisons où un PA utilise UDP et
l'autre WSS, si exposées, sont qualifiées séparément. Une reprise vérifie
l'état courant ; aucune file ne remet en circulation un flux expiré ou
révoqué. Engorgement et pertes sont diagnostiqués sans mémoire illimitée.

IPv6 désactivé A06a exclut aussi les endpoints et transports IPv6 des relais.
CPU, mémoire, trafic, connexions, débit, latence sous pertes, délais de
basculement et charge des services exécutés par les PA sont mesurés sur
Linux/Windows physiques et VM, Docker/LXC Proxmox. Le transport TCP peut
retarder des paquets derrière une retransmission ; l'impact sur les flux
TCP et UDP encapsulés est qualifié. Les délais A05 restent applicables,
sans promesse de continuité des sessions ou d'économie de ressources.
Aucun privilège, montage, port fixe ou changement Proxmox n'est introduit.

[WireGuard documente son transport UDP](https://www.wireguard.com/protocol/) ;
[WebSocket, RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html), définit
un transport sur TCP et sa protection TLS en WSS. La
[documentation officielle NetBird sur les relais](https://docs.netbird.io/about-netbird/understanding-nat-and-connectivity#netbird-relay)
décrit QUIC/UDP avec secours WebSocket ; elle sert de référence fonctionnelle.
PZT ne reprend ni son protocole, ni sa course simultanée des transports,
ni ses performances ou paramètres. La décision A09b reste à qualifier par
profil ; A09c, option A validée, fixe QUIC avec DATAGRAM pour l'UDP.

##### Application au PA — A09b

Le relais transporte les paquets WireGuard déjà chiffrés entre pairs admis,
sans terminer leur tunnel ni posséder leurs clés privées. Son rôle reste
distinct de la passerelle A08 et de l'autorité A12 ; les contrats et adapters
sont développés dans PZT, sans brique NetBird.

L'option A est validée par le développeur le 5 octobre 2026 : PA utilise
un transport de relais UDP prioritaire avec secours WebSocket sur TLS
(WSS), porté par TCP, si le chemin UDP autorisé
est indisponible. PA encapsule les paquets WireGuard via un adapter PZT ;
WireGuard conserve son UDP natif. Ce choix couvre les réseaux où WSS reste
permis malgré un blocage UDP, sous réserve de qualification, sans garantie
de passage à travers tous les proxies ou pare-feu.

L'option B de relais UDP seuls n'est pas retenue comme mode de référence.

PA authentifie la liaison avec le relais et présente une autorisation
liée aux pairs, au contexte et à une durée bornée. Quotas, résidence,
révocation et expiration restent opposables ; basculer ou maintenir une
connexion ne renouvelle aucun droit. Le mécanisme standard de protection
et d'authentification du transport UDP est fixé par A09c, option A validée :
QUIC avec DATAGRAM, bibliothèques à définir ; WireGuard chiffre toujours
les données de bout en bout.

PA vérifie endpoint WSS, ancrage TLS, authentification et
permission avant transfert. Un refus de certificat, de preuve ou de droit
ne déclenche aucun contournement. Les proxies sont configurés et qualifiés
explicitement, sans désactiver les contrôles TLS. Ce transport de paquets
est distinct des notifications et retours JSON A07c ; SSE ne relaie pas
les paquets WireGuard.

La politique déterministe versionnée privilégie le direct admissible,
puis UDP relayé admissible et WSS admissible. Politique
imposée et sécurité restent prioritaires. Essais, fenêtres de stabilité,
retour à UDP ou au direct et chevauchement éventuel de transition sont
bornés et à calibrer, sans second transport de données permanent pour
mesurer son coût. Aucun passage vers un mode non autorisé n'est permis.

L'adapter préserve les limites des datagrammes et le pair destinataire,
sans transfert de données applicatives en clair. Cadrage binaire, tailles,
MTU, buffers, files, dépassements et intégration au socket WireGuard sont
qualifiés par backend ; les liaisons mixtes UDP/WSS, si exposées, sont
qualifiées séparément. Reprise et files respectent l'état courant et les
échéances A05, sans émission d'un flux révoqué ou expiré.

IPv6 désactivé exclut les endpoints et transports IPv6 des relais. CPU,
mémoire, sondes, trafic, connexions, latence sous pertes, débit et basculement
sont mesurés par plateforme Linux/Windows physique et VM, Docker/LXC Proxmox,
y compris sur les PA portant le rôle relais. Retransmissions TCP et files
peuvent retarder les flux ; les sessions ne sont pas présumées continues.
Aucun gain de ressources, privilège, montage ou changement Proxmox n'est
présumé. Les sources officielles figurent dans le cadrage PZT.
La décision A09b reste à qualifier par profil ; A09c, option A validée,
fixe QUIC avec DATAGRAM pour le transport UDP.

#### Scenario: Conformité du traitement A09b

- **WHEN** un profil revendique le traitement A09b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--6951afc6e2

Source : `openspec/specs/pzt/spec.md`, ligne 2237. SHA-256 du bloc : `cfc501b9e0962f7b6eab36f6ed9f9aac5383631ab968d206daac287463da25d1`.

~~~~text
### Requirement: Contrat A09c — QUIC avec DATAGRAM pour les relais UDP, option A validée

Le rôle chargé du traitement A09c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A09c

Ce choix complète le transport UDP prioritaire avec secours WSS validé
A09b. Il concerne les liaisons PA–relais ; le direct reste WireGuard sur
UDP et le relais transporte des paquets WireGuard déjà chiffrés entre PA.
Le contrôle PBO et les notifications A07 conservent leurs contrats.

L'option A est validée par le développeur le 5 octobre 2026 : PZT utilise
QUIC avec sa protection TLS et l'extension DATAGRAM pour les paquets
WireGuard relayés. Les datagrammes perdus ne sont pas
retransmis automatiquement par cette extension ; ils restent soumis au
contrôle de congestion QUIC. Les streams fiables ne sont pas utilisés comme
substitut pour les paquets WireGuard du profil UDP. Les éventuels échanges
internes de gestion du relais sont bornés, déclarés et distincts des
Commands et Queries PBO. Le transport s'appuie sur les mécanismes standards
de gestion de connexion et de congestion QUIC ; consommation et performances
restent à qualifier.

L'option B de protection par DTLS 1.3 n'est pas retenue comme mécanisme
UDP de référence pour les relais.

PZT développe la gestion des circuits et l'adapter
avec des bibliothèques standards indépendantes à sélectionner. Le pair,
le contexte et le circuit sont liés à une permission vérifiable ; le
handshake de transport ne vaut pas autorisation métier. Identités, formats
de preuve et ancrages restent à préciser en A10. Expiration, révocation,
quotas et résidence A05/A09b restent opposables. Une reprise de session TLS
ou un ticket de transport ne restaure ni ne prolonge un mandat. Le profil
validé n'autorise pas de transfert ou d'allocation en données précoces
0-RTT avant vérification courante de la relation et de ses preuves.

Le support DATAGRAM et ses limites sont vérifiés pour chaque
liaison. Une incompatibilité ne transforme pas silencieusement les paquets
en stream fiable ; le secours WSS n'est engagé que selon la politique
validée A09b. Tailles de datagrammes, surcharge d'encapsulation, MTU du
chemin et MTU WireGuard sont qualifiées ensemble ; l'extension DATAGRAM
ne fragmente pas ses frames. Un paquet trop grand est traité et diagnostiqué
selon un contrat borné, sans présumer une fragmentation transparente.

Les identifiants de circuit et leur traitement préservent l'isolation entre
pairs et contextes. Files, buffers, états de connexion, reconnexions,
anti-rejeu et limites anti-abus sont bornés et diagnostiqués. Un changement
d'adresse ou une migration de transport réévalue les conditions du profil,
sans renouveler un droit ; les données périmées ou révoquées ne sont pas
réémises depuis une file. Le relais termine la protection QUIC de sa liaison,
mais ne déchiffre pas les données WireGuard entre PA.

IPv6 désactivé A06a reste exclu des endpoints et transports PZT. Les tests
couvrent Linux/Windows physiques et VM, Docker/LXC Proxmox, backends A01,
pertes, réordonnancement, MTU réduite, changement de réseau et secours WSS.
CPU, mémoire, états, sondes, débit et latence sont comparés côté PA et relais,
y compris lorsque le relais est exécuté par un PA pour le PBO. Aucune
bibliothèque, dépendance, version d'OS, privilège ou modification Proxmox
n'est choisie par cette décision ; les profils de bibliothèques et leurs
versions normatives restent à valider et qualifier. HTTP/3, WebTransport
et une API QUIC métier ne sont pas introduits par le choix de QUIC.

[QUIC, RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), et sa
[protection TLS, RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html),
définissent le transport sécurisé ; [DATAGRAM, RFC 9221](https://www.rfc-editor.org/rfc/rfc9221.html),
définit les datagrammes sans retransmission. [DTLS 1.3, RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.html),
définit l'alternative de protection sur datagrammes. Ces standards servent
au développement propre PZT ; aucune brique NetBird n'est reprise.
La décision fixe QUIC avec DATAGRAM ; les interfaces, bibliothèques et
paramètres de qualification restent à spécifier.

##### Application au PA — A09c

Ce choix concerne la liaison PA–relais UDP A09b ; le direct conserve
WireGuard sur UDP, et les paquets relayés restent chiffrés entre PA.
Le contrôle PBO et les notifications A07 conservent leurs contrats.

L'option A est validée par le développeur le 5 octobre 2026 : PA utilise
QUIC protégé par TLS avec l'extension DATAGRAM pour les paquets WireGuard, sans retransmission automatique des datagrammes
perdus et avec contrôle de congestion QUIC. Les streams fiables ne servent
pas de substitut aux paquets du profil UDP ; les éventuels échanges internes
de gestion du relais restent déclarés et bornés. La gestion de connexion
et de congestion est celle du transport QUIC, sans gain présumé de ressources
ou de performances.

L'option B de protection par DTLS 1.3 n'est pas retenue comme mécanisme
UDP de référence pour les relais.

PA utilise un adapter PZT et une bibliothèque standard indépendante à
sélectionner, avec circuit lié au pair, au contexte et à une permission
vérifiable. Le handshake de transport ne remplace pas l'autorisation.
Formats et ancrages A10 restent à définir ; les garanties A05/A09b sont
maintenues. Reprise TLS et tickets ne restaurent ni ne prolongent un mandat.
Le profil validé exclut transfert et allocation en données précoces
0-RTT avant vérification courante des preuves et de la relation.

PA vérifie le support DATAGRAM, les tailles négociées et
la compatibilité avec les MTU WireGuard et du chemin. Une incompatibilité
ne provoque pas de passage silencieux en stream fiable ; WSS suit la
politique A09b. DATAGRAM ne fragmente pas ses frames ; les paquets trop
grands suivent un traitement déclaré, borné et diagnostiqué.

Circuits, états, files, buffers, reprise, anti-rejeu et anti-abus sont
qualifiés et bornés par contexte. Changement de réseau ou migration du
transport réévalue le profil sans renouveler de permission. Le relais
termine la protection QUIC de sa liaison sans pouvoir déchiffrer
les données WireGuard entre PA. IPv6 désactivé reste exclu des transports PZT.

Qualification et comparaison CPU, mémoire, trafic, états, pertes, MTU et
latence couvrent les PA Linux/Windows physiques et VM, Docker/LXC Proxmox,
les backends A01 et les PA portant le relais, avec secours WSS. Aucune
bibliothèque, dépendance, version d'OS ou permission hôte n'est sélectionnée.
HTTP/3, WebTransport et une API métier QUIC ne sont pas introduits.
Les sources officielles figurent dans le cadrage PZT. QUIC avec DATAGRAM est
retenu ; interfaces, bibliothèques et paramètres restent à spécifier et qualifier.

#### Scenario: Conformité du traitement A09c

- **WHEN** un profil revendique le traitement A09c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

