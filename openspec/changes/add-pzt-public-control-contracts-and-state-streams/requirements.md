# Références normatives — Z06

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 93 | [Contrats, snapshots, deltas et adaptation de transport](../../specs/pzt/spec.md#L93) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1211 | [Contrat A07a — Contrats HTTP/JSON, option A validée](../../specs/pzt/spec.md#L1211) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1268 | [Contrat A07b — Snapshot et deltas ordonnés, option A validée](../../specs/pzt/spec.md#L1268) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1375 | [Contrat A07c — Notifications WebSocket, option B validée](../../specs/pzt/spec.md#L1375) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1475 | [Contrat A07c2 — Table de règles déterministes, option A validée](../../specs/pzt/spec.md#L1475) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1587 | [Contrat A07d — Deltas par opérations métier JSON typées, option A validée](../../specs/pzt/spec.md#L1587) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--120fef4ef9

Source : `openspec/specs/pzt/spec.md`, ligne 93. SHA-256 du bloc : `b8f046887caca456150894a96e45fdf8e85c3b228c0d02b6c98385c5c6bff4e1`.

~~~~text
### Requirement: Contrats, snapshots, deltas et adaptation de transport

Les commandes et lectures MUST rester HTTP/JSON sur contrats publics versionnés. Notifications MUST utiliser WebSocket de référence ou SSE complémentaire selon la table administrée déterministe A07c2, avec mêmes identités, droits, révisions et validités. Snapshots et deltas métier MUST être ordonnés, idempotents et réconciliables ; un trou MUST conduire à un état complet vérifié. La bascule MUST NOT restaurer un droit retiré ni présumer un gain de ressources.

#### Scenario: Contrats, snapshots, deltas et adaptation de transport

- **WHEN** des deltas arrivent hors séquence après bascule de transport
- **THEN** l'état est réconcilié sans réintroduire de pair révoqué
~~~~

### Référence pzt--4dd19c92ee

Source : `openspec/specs/pzt/spec.md`, ligne 1211. SHA-256 du bloc : `2a2d787643ae931fe97af57ead5e9d79e83d2a00053f6e5ff43e0f92b66744bc`.

~~~~text
### Requirement: Contrat A07a — Contrats HTTP/JSON, option A validée

Le rôle chargé du traitement A07a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A07a

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

##### Application au PA — A07a

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

#### Scenario: Conformité du traitement A07a

- **WHEN** un profil revendique le traitement A07a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--4df27df948

Source : `openspec/specs/pzt/spec.md`, ligne 1268. SHA-256 du bloc : `4231fcfc0b57dde7262595f901e7c2381b9ddce7742bfd6ea2d426c00b39449d`.

~~~~text
### Requirement: Contrat A07b — Snapshot et deltas ordonnés, option A validée

Le rôle chargé du traitement A07b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A07b

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

##### Application au PA — A07b

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

#### Scenario: Conformité du traitement A07b

- **WHEN** un profil revendique le traitement A07b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--eb40174af0

Source : `openspec/specs/pzt/spec.md`, ligne 1375. SHA-256 du bloc : `e8d46b6fd6a61cb371ee13f9f4b8a36ec66b0bee757d38eac986f0a04b3384aa`.

~~~~text
### Requirement: Contrat A07c — Notifications WebSocket, option B validée

Le rôle chargé du traitement A07c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A07c

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

##### Application au PA — A07c

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

#### Scenario: Conformité du traitement A07c

- **WHEN** un profil revendique le traitement A07c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--14dc7ac926

Source : `openspec/specs/pzt/spec.md`, ligne 1475. SHA-256 du bloc : `df3a95504351cdf4b751297b56b7ca21a675e894d3f8cc4e6985d52a8de41b4c`.

~~~~text
### Requirement: Contrat A07c2 — Table de règles déterministes, option A validée

Le rôle chargé du traitement A07c2 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A07c2

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

##### Application au PA — A07c2

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

#### Scenario: Conformité du traitement A07c2

- **WHEN** un profil revendique le traitement A07c2 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--027b4f9267

Source : `openspec/specs/pzt/spec.md`, ligne 1587. SHA-256 du bloc : `809021ce51212a9b898084aef16933b56f3ae9dc331c7006f3998baac3f47a6e`.

~~~~text
### Requirement: Contrat A07d — Deltas par opérations métier JSON typées, option A validée

Le rôle chargé du traitement A07d MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A07d

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

##### Application au PA — A07d

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

#### Scenario: Conformité du traitement A07d

- **WHEN** un profil revendique le traitement A07d et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

