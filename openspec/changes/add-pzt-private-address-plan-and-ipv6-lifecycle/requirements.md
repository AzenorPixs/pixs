# Références normatives — Z04

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 75 | [IPv6 désactivable et configuration hôte préservée](../../specs/pzt/spec.md#L75) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 250 | [Contrat A06b — Plan privé et allocation validés, qualification requise](../../specs/pzt/spec.md#L250) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 425 | [Contrat A06d — Valeur initiale du réglage IPv6 PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L425) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--005df2f1f1

Source : `openspec/specs/pzt/spec.md`, ligne 75. SHA-256 du bloc : `35cee37f580ed5aa5e9b42f5ccb11b0e6b821d88594348966e5065701860af07`.

~~~~text
### Requirement: IPv6 désactivable et configuration hôte préservée

PZT MUST prendre en charge IPv4/IPv6 et un réglage unique de désactivation IPv6 propre à PZT. Les nouveaux périmètres MUST commencer IPv6 désactivé sans choix explicite ; l'existant MUST être préservé. La désactivation MUST retirer adresses, routes, autorisations, endpoints IPv6 et AAAA PZT sans désactiver IPv6 sur l'hôte. Collisions MUST être détectées sans écrasement implicite de configuration externe.

#### Scenario: IPv6 désactivable et configuration hôte préservée

- **WHEN** l'opérateur désactive IPv6 PZT
- **THEN** seules les ressources IPv6 gérées par PZT sont retirées et leur état est rapporté
~~~~

### Référence pzt--93943f7161

Source : `openspec/specs/pzt/spec.md`, ligne 250. SHA-256 du bloc : `7afacce60541d832844f50b56cc0d3ff90e170c2659379693a7bcfc086deeaa5`.

~~~~text
### Requirement: Contrat A06b — Plan privé et allocation validés, qualification requise

Le rôle chargé du traitement A06b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06b

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

##### Application au PA — A06b

L'option A, validée par le développeur le 5 octobre 2026 dans le registre intégré commun à PA et PZT,
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

#### Scenario: Conformité du traitement A06b

- **WHEN** un profil revendique le traitement A06b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e5df8c262f

Source : `openspec/specs/pzt/spec.md`, ligne 425. SHA-256 du bloc : `d0a052e54574acbc15ea5c0f076f84b2d582873dc78bdb98c87e5a5cde760f3a`.

~~~~text
### Requirement: Contrat A06d — Valeur initiale du réglage IPv6 PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06d MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06d

L'option A validée initialise le réglage unique « IPv6 activé » A06a à
désactivé lors de la création d'un nouveau périmètre sans valeur choisie
explicitement, dans une configuration initialisée et approuvée. Le défaut
est persisté et versionné. IPv6 reste implémenté et testé dès le socle ;
activation explicite autorisée depuis PBO ou les contrats de configuration
PZT, y compris dès le provisionnement d'un profil nécessitant IPv6.
Aucun écrasement de configuration existante ni migration forcée ; ce défaut
ne remplace pas au runtime un état manquant, corrompu ou non vérifiable.

L'activation ne crée ni allocation, route ni permission depuis le seul
réglage : familles configurées, adapters qualifiés, routes/endpoints,
droits et preuves courants restent requis. Aucun Internet IPv6 imposé,
chemin IPv6 garanti, gain CPU/RAM chiffré ou sécurité cryptographique
supérieure présumés. La désactivation simple A06a reste disponible.

La portée conserve la distinction overlay/transport : adresses, routes,
autorisations IPv6 PZT, publication AAAA propre au PZT, endpoints
WireGuard/TLS, candidats ICE/STUN et transports vers les relais. Réglage
désactivé : aucun de ces chemins IPv6 n'est utilisé, y compris après
résolution DNS ou roaming WireGuard. IPv6 hôte, autres applications et
réseaux de l'opérateur inchangés ; aucun sysctl, registre Windows, droit
Proxmox, montage ou privilège du conteneur implicite. Une continuité IPv4
requiert son propre profil et une voie autorisée ; sinon blocage diagnostiqué,
sans activation implicite IPv4/IPv6 ni sortie de PZT.

Changements ultérieurs autorisés, engagés et réconciliés ; PBO expose
valeur souhaitée/appliquée et écarts, sans succès avant preuve de l'état
appliqué. Une restauration ne réactive ni famille ni droits retirés.
Aucune bascule dynamique du réglage pour améliorer la connectivité ;
A07c2 ne permet pas de modifier les familles IP. Schéma de configuration,
héritage des périmètres, mécanismes de retrait et budgets à préciser.
Qualification Linux/Windows physiques/VM, Docker/LXC Proxmox : création
sans choix, IPv6 explicite, profil existant, changement/retrait, endpoints
IPv6, absence de voie IPv4, configuration invalide, DNS/caches, roaming,
restauration et absence de modification hôte.

[WireGuard distingue AllowedIPs et Endpoint](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8) ;
ce réglage global est un contrat PZT à qualifier dans ses adapters.
A06d, option A, est validé le 6 octobre 2026 ; paramètres et qualification
restent à préciser.

##### Application au PA — A06d

L'option A validée initialise « IPv6 activé » A06a à désactivé à la création
d'un nouveau périmètre sans choix explicite, dans une configuration
initialisée/approuvée, avec valeur persistée/versionnée. IPv6 reste
implémenté/testé ; activation explicite autorisée par PBO/contrats PZT,
y compris dès provisionnement. Aucun écrasement de profil existant ou
migration forcée, ni défaut au runtime sur état manquant/corrompu/non vérifiable.

Réglage sans droit, allocation ou route implicite ; usage selon familles,
adapters, routes/endpoints, droits et preuves courants, sans Internet IPv6
imposé, voie garantie, gain CPU/RAM ou sécurité cryptographique supérieure
présumés. Désactivation simple maintenue.

Portée A06a overlay et transport : ressources IPv6 PZT, AAAA propres,
endpoints WireGuard/TLS, candidats ICE/STUN et relais. Désactivé : chemins
IPv6 exclus, y compris DNS/roaming WireGuard ; IPv6 hôte/autres applications/
opérateur inchangé, sans sysctl, registre, accès Proxmox, montage ou
privilège implicite. Voie IPv4 autorisée/configurée requise pour continuité ;
sinon blocage sans activation implicite ou sortie de PZT.
Changements autorisés engagés/réconciliés avec preuve de l'état appliqué ;
souhaité/appliqué et écarts visibles PBO. Restauration sans ancienne famille
ou droits réactivés ; pas de bascule dynamique du réglage pour connectivité
ni via A07c2. Schémas, héritage, retrait et budgets à préciser ; qualification
Linux/Windows physique/VM, Docker/LXC Proxmox : création sans choix,
IPv6 explicite, profil existant, retrait, endpoints IPv6, absence de voie IPv4,
configuration invalide, DNS/caches, roaming, restauration et hôte inchangé.
Source WireGuard dans le cadrage PZT. A06d, option A, est validé le 6 octobre 2026 ;
paramètres et qualification restent à préciser.

#### Scenario: Conformité du traitement A06d

- **WHEN** un profil revendique le traitement A06d et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

