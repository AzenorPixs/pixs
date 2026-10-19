# Références normatives — Z05

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 84 | [DNS essentiel partagé administré par PBO](../../specs/pzt/spec.md#L84) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 310 | [Contrat A06c — DNS Pixs géré par un module essentiel PBO, option B validée](../../specs/pzt/spec.md#L310) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 512 | [Contrat A06e — Exécution du service DNS Pixs — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L512) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 602 | [Contrat A06f — Transport des requêtes DNS PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L602) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 698 | [Contrat A06g — Politique de cache et TTL DNS — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L698) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 807 | [Contrat A06h — Sélection des serveurs DNS PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L807) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 906 | [Contrat A06i — Nommage DNS des instances PA — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L906) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1022 | [Contrat A06j — Choix du suffixe DNS privé PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L1022) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 1123 | [Contrat A06k — Représentation des alias DNS lisibles des PA — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L1123) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--fd36d11ae5

Source : `openspec/specs/pzt/spec.md`, ligne 84. SHA-256 du bloc : `2dda88c1bf8014fe3d9fe2daa85d11610559cd7f4bdfc5c0de4440900ce97603`.

~~~~text
### Requirement: DNS essentiel partagé administré par PBO

Le DNS Pixs MUST être administré par un module essentiel PBO et utilisable par PZT et les PA selon leurs droits. Le service DNS MUST être distinct, exécuté sous pilotage de PA désignés ; les PA ordinaires MUST rester clients. Les vues, retraits, caches, règles DoT et identités de destination MUST suivre A06b–A06k ; résolution ou repli public MUST NOT accorder un accès ni masquer une panne.

#### Scenario: DNS essentiel partagé administré par PBO

- **WHEN** le DNS privé requis est indisponible
- **THEN** aucun repli public non autorisé n'expose les noms ou ne contourne la politique
~~~~

### Référence pzt--7a832c1a03

Source : `openspec/specs/pzt/spec.md`, ligne 310. SHA-256 du bloc : `41310aa4a88be761bde4632899a2886e1a8974259515c9e4fe2f2c591d7c23d4`.

~~~~text
### Requirement: Contrat A06c — DNS Pixs géré par un module essentiel PBO, option B validée

Le rôle chargé du traitement A06c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06c

L'option B est validée par le développeur le 5 octobre 2026 avec la précision
suivante : un DNS géré sera développé pour Pixs sous forme de module essentiel
du PBO, utilisable par PZT et par tous les PA. Le module administre les zones,
les enregistrements, les vues, les règles de résolution et leur cycle de vie.
Il possède ses données et expose des contrats publics versionnés au module
PZT ; aucun accès aux tables privées d'un autre module n'est admis. Sa capacité
DNS et ses dépendances obligatoires sont déclarées dans la composition des
profils qui l'utilisent ; une dépendance essentielle manquante bloque leur
activation ou leur readiness selon le contrat. Le Kernel conserve ses
responsabilités génériques. L'identifiant du module, les rôles d'exécution et leur qualification
restent à qualifier ; A06e A validé le 6 octobre 2026 retient un service DNS
distinct du processus PBO, piloté par PA désignés, même hôte possible.
Topologie/redondance et interfaces à préciser ; DoT A06f et cache/TTL A06g
validés, sélection ordonnée/secours A06h et nommage A06i A validés ;
suffixe explicite A06j et alias CNAME A06k A validés.

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
au DNS privé encore indisponible. Suffixes, paramètres de cache A06g,
protocoles DNS amont, persistance,
réplication et comportement des applications avec résolveur propre restent
à définir ; l'absence de fuite doit être démontrée.

##### Application au PA — A06c

L'option B est validée par le développeur le 5 octobre 2026 : un DNS géré
sera développé pour Pixs dans un module essentiel du PBO et utilisé par
PZT et tous les PA. PBO administre ses zones, vues, enregistrements et règles
par les contrats publics du module DNS. Le module PZT utilise ces contrats
pour publier ou retirer ses noms ; il n'accède pas aux données privées du
module DNS. Les dépendances essentielles et leur effet sur l'activation et
la readiness sont déclarés pour les profils consommateurs. L'identifiant
du module, les rôles d'exécution et leur qualification restent ouverts ;
A06e A validé le 6 octobre 2026 retient un service DNS distinct du processus
PBO, piloté par PA désignés, même hôte possible ; topologie/redondance et
interfaces à préciser, DoT A06f, cache/TTL A06g et sélection ordonnée/secours
A06h, nommage A06i, suffixe explicite A06j et alias CNAME A06k A validés.
Le Kernel reste générique.

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
encore inaccessible. Suffixes, paramètres de cache A06g, protocoles DNS amont,
bibliothèques, persistance,
réplication et comportement des applications avec résolveur propre restent
à préciser ; l'absence de fuite doit être démontrée.

#### Scenario: Conformité du traitement A06c

- **WHEN** un profil revendique le traitement A06c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--a74381eadc

Source : `openspec/specs/pzt/spec.md`, ligne 512. SHA-256 du bloc : `c8912798415af724ab37690be88871746a95945434c24697572c02e55a7919ec`.

~~~~text
### Requirement: Contrat A06e — Exécution du service DNS Pixs — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06e MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06e

L'option A validée retient un service DNS distinct du processus PBO, avec
lifecycle propre, exécuté et surveillé sous pilotage de PA désignés par
un rôle/mandat explicite. Le module essentiel PBO A06c B reste propriétaire
des données DNS, des zones/vues, de l'administration et des contrats publics
utilisés par PZT et tous les PA. L'implémentation du service appartient au
module DNS Pixs ; PA pilote déploiement/lifecycle autorisés, sans logique DNS
dans le Kernel ou le PA générique. Aucun serveur ou résolveur autonome
imposé à chaque PA client.

Placement sur le même hôte que PBO ou sur un autre périmètre qualifié
possible, sans machine supplémentaire obligatoire. Budgets et redémarrage
DNS propres ; unité de service distincte à exploiter. Administration et
publication restent dans le module PBO ; le service consomme uniquement
ses contrats publics autorisés, sans SQL direct PA vers tables métier Pixs.
Consommer le DNS ne confère ni rôle serveur, ni publication, ni vue globale.
Les états servis suivent les contrats du module DNS et leur validité.

Contrôle/publication et accès DNS via PZT dans le contexte autorisé,
y compris même hôte A03 ; aucun port/socket de gestion PBO–PA non protégé.
Transport DoT validé A06f, ports/adapters à qualifier ; placement
sans permission d'écoute, privilège ou montage implicite. PBO indisponible :
aucune nouvelle publication/prolongation ; le service peut servir le dernier
état autorisé uniquement dans les bornes A06c et sous permissions/preuves
courantes, sans autorité autonome ni continuité illimitée. Noms privés
non résolubles sans repli public, caches bornés et retraits/AAAA A06d respectés.

Redondance et répartition des vues ouvertes ; sélection ordonnée/secours
A06h A validée,
même hôte/stockage sans domaine de panne indépendant présumé. Amorçage A02
sans dépendance circulaire à un DNS privé encore inaccessible. Identifiants,
contrats, topologie/copies, persistance technique, budgets de cache A06g et budgets
CPU/RAM/latence à préciser, sans gain ou disponibilité chiffrés garantis.
Recette par rôle Linux/Windows physiques/VM, Docker/LXC Proxmox : serveur/
client distincts, droits/vues, démarrage/arrêt PBO et DNS, état expiré,
retrait/restauration, absence de fuite/SQL/privilège implicites.

[NetBird documente la gestion DNS et les nameservers distribués aux pairs](https://docs.netbird.io/manage/dns).
Référence fonctionnelle sans choix d'architecture Pixs ni intégration de
brique NetBird. A06e, option A, est validé le 6 octobre 2026 ; paramètres
et qualification restent à préciser.

##### Application au PA — A06e

L'option A validée retient un service DNS distinct du processus PBO,
lifecycle propre, exécuté/surveillé sous pilotage de PA désignés par rôle/
mandat. Module essentiel PBO propriétaire des données, zones/vues,
administration et contrats publics A06c B conservé ; code du service dans
le module DNS Pixs, PA pilote déploiement/lifecycle autorisés, sans logique
DNS dans Kernel/PA générique ni serveur/résolveur imposé à chaque PA client.

Même hôte PBO ou autre périmètre qualifié possible, sans machine
supplémentaire obligatoire ; budgets/redémarrage propres et unité de
service distincte à exploiter. Administration/publication PBO et contrats
publics autorisés, sans SQL direct PA vers tables Pixs. PA ordinaires
clients/adapters sans rôle serveur, publication ou vue globale implicites.
États servis selon contrats DNS et validité courante.

Contrôle/publication et accès DNS par PZT, y compris même hôte A03, sans
contournement local de gestion PBO–PA. Transport DoT validé A06f,
ports/adapters à qualifier ; aucune écoute, droit ou montage implicite.
PBO absent sans nouvelle publication/prolongation ; dernier état autorisé
servable dans les bornes A06c sous contrôles courants, sans autorité locale
autonome ni continuité illimitée. Noms privés sans repli public, caches
bornés, retraits/AAAA A06d, amorçage A02 sans dépendance circulaire.

Sélection ordonnée/secours A06h A validée ; redondance/vues, contrats, copies,
état technique et budgets de cache A06g à préciser ; même hôte/stockage sans indépendance
de panne présumée. Qualification par rôle/cible Linux/Windows physique/VM,
Docker/LXC Proxmox : client/serveur, droits/vues, pannes PBO/DNS, état expiré,
retrait/restauration et absence de fuite/SQL/privilège implicites, sans gain
CPU/RAM ou disponibilité garantis. Référence NetBird dans le cadrage PZT,
sans intégration de ses briques. A06e, option A, est validé le 6 octobre 2026 ;
paramètres et qualification restent à préciser.

#### Scenario: Conformité du traitement A06e

- **WHEN** un profil revendique le traitement A06e et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--3cb131fa46

Source : `openspec/specs/pzt/spec.md`, ligne 602. SHA-256 du bloc : `e8124d79f58db84a2447651425b17bbfcf70e5b742c22adb2750f692b42140ab`.

~~~~text
### Requirement: Contrat A06f — Transport des requêtes DNS PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06f MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06f

L'option A validée retient DNS sur TLS/TCP (DoT, RFC 7858) pour les
requêtes/réponses entre clients PA/PBO PZT et service DNS A06e. Administration
et publication HTTP/JSON A07 distinctes ; module essentiel PBO propriétaire
A06c, PA ordinaires clients/adapters sans résolveur autonome complet imposé.
Messages DNS standard avec cadrage DoT, sans conversion en commande JSON.

Profil strict d'authentification et de confidentialité RFC 8310, renforcé
par identité mutuelle et autorisation du contexte PZT. TLS obligatoire dès
l'établissement, sans mode opportuniste ; endpoints provisionnés/autorisés,
sans redirection ni serveur appris hors configuration. Réutilisation bornée
des connexions sous permissions/preuves/fraîcheur courantes. Pas de couche
HTTP pour ces requêtes, sans gain CPU/RAM/latence garanti ; clients natifs
ou adapters Linux/Windows à qualifier selon les supports réellement retenus.

Bibliothèques TLS/DNS éprouvées, chaîne/ancrage, identité/usages et contexte
vérifiés ; vue liée au contexte authentifié, jamais au nom ou à la seule IP.
PKI/TLS A10b distincts d'Ed25519 opérationnel A12e ; aucun algorithme/version
TLS sélectionné implicitement. WireGuard interhôtes A01, TLS mutuel même
hôte A03 et contrôles A05 conservés. Échec d'authentification, permission
expirée ou provider incapable : refus sans bascule automatique vers DoH,
DNS UDP/TCP en clair ou résolveur public. IPv6 A06d désactivé exclut aussi
les endpoints DNS IPv6 PZT.

Tailles/parsing, concurrence, connexions et retries bornés ; corrélation
requête/réponse vérifiée, diagnostics sans requêtes, credentials ou noms
privés. Cache DNS sans permission/validité A06c prolongée ni habilitation
par résolution. Adapters minimaux vers OS/applications à qualifier : interface
locale, contrôle du contexte et routage des zones privées restent ouverts,
sans gestion PBO–PA hors PZT ni ouverture d'écoute implicite. Amorçage A02
avec endpoints/ancrages provisionnés, sans dépendance circulaire au DNS privé.

Mesurer initialisation et requêtes sur connexions réutilisées, CPU/RAM,
latence/débit, TLS dans WireGuard et coût des adapters. Ports, limites,
schémas de vue, bibliothèques/versions, profils TLS, comportement OS et
protocoles amont restent à préciser ; cache/TTL A06g A validé.
Recette Linux/Windows physiques/VM, Docker/LXC Proxmox : formats, vue/contexte,
certificat invalide, expiration/révocation, endpoint inconnu/provider absent,
cache/retrait, absence de fuite, IPv6 désactivé, panne et reprise bornée.

[DoT est défini par RFC 7858](https://datatracker.ietf.org/doc/html/rfc7858)
et [ses profils de confidentialité par RFC 8310](https://www.rfc-editor.org/rfc/rfc8310.html#section-5).
Ces références ne qualifient aucun adapter PZT. A06f, option A, est validé
le 6 octobre 2026 ; paramètres et qualification restent à préciser.

##### Application au PA — A06f

L'option A validée retient DNS sur TLS/TCP (DoT RFC 7858) pour les
requêtes/réponses PA/PBO PZT vers service DNS A06e. Administration/publication
HTTP/JSON A07 et propriétaire essentiel PBO A06c conservés ; messages DNS
standard cadrés DoT, sans commande JSON ni résolveur autonome imposé à chaque PA.

Profil strict RFC 8310 renforcé par identité mutuelle et autorisation PZT,
TLS obligatoire dès l'établissement, sans mode opportuniste. Endpoints
provisionnés/autorisés, sans redirection ou serveur appris hors configuration.
Connexions réutilisées bornées sous permissions/preuves/fraîcheur valides ;
pas de couche HTTP, sans gain CPU/RAM/latence garanti. Clients/adapters OS
et plateformes à qualifier.

Bibliothèques TLS/DNS éprouvées, chaîne/ancrage, identité/usages et contexte
courants ; vue liée au contexte vérifié, pas au nom ou à la seule IP.
PKI/TLS A10b distincts d'Ed25519 A12e, sans algorithme/version TLS implicite.
WireGuard interhôtes A01, TLS mutuel même hôte A03 et contrôles A05 maintenus.
Échec sécurité, permission expirée ou provider absent : refus sans bascule
vers DoH, DNS en clair ou repli public ; endpoints IPv6 exclus si A06d désactivé.

Parsing/tailles, concurrence, connexions et retries bornés, corrélation
requête/réponse ; diagnostics sans requêtes, credentials ou noms privés.
Cache DNS sans permission/validité prolongée ni droit par résolution.
Adapters minimaux OS/applications à qualifier, interface locale/contexte/
routage des zones ouverts sans gestion PBO–PA hors PZT ni écoute implicite.
Amorçage A02 sans dépendance circulaire au DNS privé.

Mesurer initialisation/requêtes réutilisées, CPU/RAM/latence/débit, TLS dans
WireGuard et adapters ; ports, limites, vues, bibliothèques/versions/TLS,
OS et amonts à préciser. Cache/TTL A06g A validé. Recette
par rôle/cible : formats, contexte/vue, certificat invalide, expiration/
révocation, endpoint inconnu/provider absent, cache/retrait, absence de fuite,
IPv6 désactivé, panne/reprise bornée. Sources dans le cadrage PZT. A06f, option A,
est validé le 6 octobre 2026 ; paramètres et qualification restent à préciser.

#### Scenario: Conformité du traitement A06f

- **WHEN** un profil revendique le traitement A06f et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--6be4b9c289

Source : `openspec/specs/pzt/spec.md`, ligne 698. SHA-256 du bloc : `7e7d2043a1f9d906f687842fff04f8854385f7760cf5061b93eabcb1f8e40717`.

~~~~text
### Requirement: Contrat A06g — Politique de cache et TTL DNS — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06g MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06g

Le choix concerne les réponses des zones privées gérées par le module DNS
PBO A06c et leurs caches dans les couches PZT/PA maîtrisées. Il ne fixe ni
les TTL de zones publiques amont, ni la durée d'autorisation A05, ni celle
de l'état servi A06e. Pas de résolveur autonome complet imposé à chaque PA ;
réutilisation des capacités OS/adapters seulement après qualification.

L'option A validée retient un cache court, borné et isolé par vue/contexte
autorisé. Plafonds initiaux de TTL : 30 secondes pour une réponse positive et 5 secondes pour
une réponse négative NXDOMAIN/NODATA légitime. TTL effectif au plus égal au
minimum du plafond, du TTL restant des données et des durées restantes de
validité de l'état/vue et des permissions/preuves applicables à la réponse.
Arrondi inférieur en secondes ; TTL zéro possible pour une réponse encore
valide, aucun service après expiration. Réutilisation sans réinitialisation
du délai, et contrôles de sécurité courants avant chaque réponse maîtrisée.
Plafonds initiaux validés pour Pixs, pas imposés par les RFC ni performances
mesurées ; paramètres soumis à politique approuvée, augmentation nécessitant
validation.

Cache négatif seulement pour une absence établie dans la vue autorisée et
courante, avec SOA et borne au minimum des TTL SOA/SOA.MINIMUM conformément
à RFC 2308, puis plafond de 5 secondes et validités PZT. Échec mTLS,
permission refusée, panne ou état expiré ne deviennent pas une réponse
NXDOMAIN/NODATA cacheable. Clés conformes aux réponses DNS, incluant au
minimum vue/contexte, nom normalisé et classe, type quand applicable ;
aucun partage entre périmètres ou permissions incompatibles. Entrées et
mémoire bornées ; budgets et mécanisme d'éviction restent à qualifier.

Le cache ne requiert ni requête Django/SQL par résolution ni prolongation
de l'état A06e. OS/applications peuvent garder une adresse ou une connexion :
comportement et respect des TTL à qualifier, sans purge universelle garantie.

Retrait/révocation connu, changement de vue ou désactivation IPv6
invalident immédiatement les données concernées dans les couches maîtrisées,
sans attente du TTL ; publication connue d'un nom invalide son cache négatif.
Purge distante/application non maîtrisée non garantie ; contrôle d'accès A05
indépendant du DNS et toujours applicable même avec adresse conservée.
Panne DNS/PBO sans réponse périmée au-delà du TTL/validité, sans repli public
pour noms privés ni renouvellement implicite. Restauration/snapshot ou recul
d'horloge ne réinitialisent pas les durées ni un retrait/révocation connu ;
absence de validité temporelle démontrable entraîne refus du cache concerné.

Ce choix vise à réduire les requêtes répétées, avec mémoire de cache
supplémentaire et propagation bornée par TTL hors invalidation connue.
Comparer CPU/RAM/latence et charge réelles sans gain global promis.
Recette par rôle Linux/Windows physiques/VM, Docker/LXC Proxmox : TTL zéro,
expiration sans délai glissant, négatif/SOA, isolement des vues, droits retirés,
publication/retrait, AAAA/IPv6, panne, restauration et mémoire bornée.

[La RFC 1035 définit le TTL et le non-cache pour TTL zéro](https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.1) ;
[la RFC 2308 encadre les réponses négatives et leur expiration](https://datatracker.ietf.org/doc/html/rfc2308#section-5).
A06g, option A et plafonds initiaux 30/5 secondes, est validé le 6 octobre
2026 ; budgets et qualification restent à préciser.

##### Application au PA — A06g

Réponses des zones privées PBO A06c et caches PZT/PA maîtrisés seulement ;
ni TTL publics amont, ni autorisations A05 ou validité de l'état A06e modifiés.
Pas de résolveur complet imposé à chaque PA, capacités OS/adapters à qualifier.

L'option A validée retient un cache court borné, isolé par vue/contexte
autorisé. Plafonds initiaux : positif 30 secondes, négatif NXDOMAIN/NODATA légitime 5 secondes.
TTL effectif limité au minimum du plafond, du TTL restant des données et
des validités restantes de l'état/vue et des permissions/preuves applicables.
Arrondi inférieur, TTL zéro pour donnée encore valide possible, refus après
expiration ; hits sans délai réinitialisé, contrôles courants avant réponse
maîtrisée. Plafonds Pixs initiaux validés, pas imposés par RFC ni mesurés ;
politique approuvée et validation requise pour augmenter les plafonds.

Négatif seulement pour absence établie dans vue autorisée/courante, avec SOA,
minimum TTL SOA/SOA.MINIMUM RFC 2308 puis plafond 5 secondes/validités PZT.
Refus mTLS/droits, panne ou état expiré sans faux NXDOMAIN/NODATA cacheable.
Clés DNS incluant vue/contexte, nom normalisé, classe et type applicable ;
aucun partage incompatible. Nombre d'entrées/mémoire bornés, budgets/éviction
à qualifier. Aucun SQL PA ou requête Django par résolution imposés, ni état
A06e prolongé. OS/applications pouvant conserver adresse/connexion, respect
des TTL à qualifier sans purge universelle garantie.

Retrait/révocation connu, vue modifiée ou IPv6 désactivé : invalidation
immédiate dans couches maîtrisées ; nom publié connu invalide son cache
négatif. Purge distante/application non garantie ; A05 protège l'accès même
avec IP conservée. Panne sans réponse périmée ni repli public pour noms privés,
sans renouvellement implicite ; restauration/snapshot/recul d'horloge sans
réinitialisation des durées ni des retraits/révocations connus. Validité
temporelle non démontrable : cache concerné refusé.

Choix visant à limiter requêtes répétées, avec mémoire supplémentaire
et propagation bornée par TTL hors invalidation connue. CPU/RAM/latence/
charge à mesurer. Recette par rôle/cible : TTL zéro, expiration sans délai
glissant, négatif/SOA, vues, droits retirés, publication/retrait, AAAA/IPv6,
panne, restauration et mémoire bornée. Sources dans cadrage PZT. A06g, option A
et plafonds initiaux 30/5 secondes, est validé le 6 octobre 2026 ; budgets
et qualification restent à préciser.

#### Scenario: Conformité du traitement A06g

- **WHEN** un profil revendique le traitement A06g et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--63fa6ba7a7

Source : `openspec/specs/pzt/spec.md`, ligne 807. SHA-256 du bloc : `cf1bac59fbaa7a171d99857c056685bae5de07d61f382fba56869ab899b90185`.

~~~~text
### Requirement: Contrat A06h — Sélection des serveurs DNS PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06h MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06h

Le choix porte sur la sélection côté client des endpoints DNS DoT A06f
servant une même vue autorisée. Il ne désigne pas le primaire PostgreSQL A12,
ne délègue aucune autorité de publication au DNS et n'impose ni nombre de
machines ni service DNS à chaque PA. PBO/module DNS publie par contrats
publics une configuration versionnée : endpoints, identités attendues,
vues/périmètres et priorités ; aucun serveur appris depuis une réponse DNS,
un DHCP externe ou une redirection pour remplacer cette liste PZT.

L'option A validée retient une liste ordonnée avec serveur préféré et secours,
une seule destination sollicitée à la fois par requête non satisfaite par
cache valide. Le client conserve le serveur préféré tant qu'il est admissible
et utilisable ; passage au suivant seulement après erreur technique admissible
et contrôles courants. Retour au préféré après stabilité vérifiée, avec seuils
et temporisation explicites à qualifier, sans oscillation ni sondes illimitées.
Ces priorités sont celles du client pour sa vue ; elles n'interdisent pas aux
services DNS autorisés de répondre à d'autres clients. Un endpoint unique
reste un profil possible, sans disponibilité redondante présumée.

La sélection et l'utilisation exigent identité mTLS, rôle DNS autorisé,
preuves/permissions et état de vue valides. Compatibilité de version/époque et
retraits déjà connus vérifiée par les contrats publics de contrôle ; pas de
retour à un état plus ancien que la borne connue du client ni réactivation
d'un droit retiré. Aucune signature propriétaire ajoutée aux messages DNS
standard par ce choix. Fraîcheur globale instantanée non promise : les limites
de l'état A06e et du cache A06g demeurent applicables.

Un refus de sécurité, une permission expirée ou un état non vérifiable bloque
la requête concernée ; il n'est pas reclassé en panne pour obtenir une réponse
autorisée ailleurs. Une réponse NXDOMAIN/NODATA valide n'entraîne pas de recherche
d'un résultat différent chez les secours. Délais, essais, connexions et sondes
bornés ; serveurs épuisés sans repli public, clair, DoH ou IPv6 désactivé A06d.
Bascule sans prolongation de TTL, permission, preuve ou validité de l'état ;
cache isolé par contexte et invalidé si la vue devient incompatible.

Ce choix retient priorité/secours côté client, sans répartition active
systématique des requêtes entre serveurs. Ni gain CPU/RAM ni continuité DNS
garantis : copies, mise à jour des vues, domaines
de panne, contrôle de disponibilité et budgets restent à qualifier. Plusieurs
services sur le même hôte/stockage ne constituent pas des pannes indépendantes.
Recette Linux/Windows physiques/VM, Docker/LXC Proxmox : panne technique,
retour stable, refus mTLS/droits, état obsolète, retrait connu, négatif valide,
cache/TTL, ensemble vide et absence de fuite ou bascule non autorisée.

[NetBird documente la distribution de nameservers et le routage par domaine](https://docs.netbird.io/manage/dns#key-concepts).
Référence fonctionnelle seulement ; priorité/secours est un choix Pixs,
sans reprise de briques NetBird. A06h, option A, est validé le 6 octobre 2026 ;
seuils, délais, topologie et qualification restent à préciser.

##### Application au PA — A06h

Sélection client des endpoints DoT A06f pour une même vue autorisée ; ni
primaire PostgreSQL A12, ni nouvelle autorité DNS/publication, ni serveur
imposé à chaque PA. Liste versionnée publiée par contrats publics PBO/DNS :
endpoints, identités attendues, vues/périmètres/priorités. Aucun remplacement
par serveur appris via réponse DNS, DHCP externe ou redirection.

L'option A validée retient préféré et secours ordonnés, une destination à la
fois par requête hors cache valide. Préféré conservé tant qu'admissible/utilisable,
suivant après erreur technique admissible et contrôles courants ; retour
après stabilité vérifiée, seuils/temporisation à qualifier, sans oscillation
ou sondes illimitées. Priorité côté client, sans empêcher un service autorisé
de répondre à d'autres clients ; endpoint unique possible, sans redondance.

Sélection/utilisation : mTLS, rôle, contexte, preuves/permissions et vue valides,
version/époque compatibles et retraits connus contrôlés via contrats publics.
Pas de retour sous la borne d'état connue ni droit retiré réactivé, pas de
signature DNS propriétaire implicite ; validités A06e/A06g maintenues,
sans fraîcheur globale instantanée promise. Refus sécurité, permission expirée
ou état non vérifiable bloque la requête, sans recherche d'une autorisation
ailleurs ; NXDOMAIN/NODATA valide sans tentative d'obtenir un autre résultat.
Essais/délais/connexions/sondes bornés, aucun repli public/clair/DoH ou IPv6
interdit. Bascule sans TTL/permission/preuve/état prolongés ; cache isolé,
invalidé si vue incompatible.

Priorité/secours retenus, sans répartition active systématique des requêtes.
CPU/RAM/continuité à qualifier, copies/vues/domaines de panne/budgets ouverts ;
même hôte/stockage sans indépendance de panne présumée. Recette par rôle/cible :
panne technique, retour stable, refus mTLS/droits, état obsolète/retrait connu,
négatif valide, cache/TTL, ensemble vide et absence de fuite/bascule non autorisée.
Source NetBird fonctionnelle dans cadrage PZT, sans intégration de ses briques.
A06h, option A, est validé le 6 octobre 2026 ; seuils, délais, topologie et
qualification restent à préciser.

#### Scenario: Conformité du traitement A06h

- **WHEN** un profil revendique le traitement A06h et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e19905d610

Source : `openspec/specs/pzt/spec.md`, ligne 906. SHA-256 du bloc : `1c6e5e0b45b931b960aff5f046f391cf418df04bf00c3d2f2df683a6b2d88960`.

~~~~text
### Requirement: Contrat A06i — Nommage DNS des instances PA — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06i MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06i

Le choix porte sur les noms des instances PA admises publiés dans les vues
privées A06c ; aucune modification du hostname OS, suffixe public, domaine
de recherche ou nom de service implicite. Suffixes et organisation des zones
restent à choisir explicitement. La résolution n'accorde ni identité,
ni preuve d'état, ni droit réseau/métier.

L'option A validée retient un nom technique stable généré à partir de
l'identifiant de l'instance admise et de son périmètre, avec alias lisibles
facultatifs administrés par PBO. Correspondance enregistrée par le module
DNS, format de label opaque à préciser, sans secret, nom d'utilisateur,
adresse MAC, hostname découvert ou clé privée dans la dérivation. Unicité
vérifiée à l'engagement, pas supposée depuis un hash ou un identifiant tronqué.
Le nom reste stable tant que l'identifiant de l'instance et le périmètre
restent identiques ; IP, clé ou certificat peuvent changer sans renommer
l'instance, seulement après changements autorisés et vérifiés. Nouvelle
identité d'instance, notamment clone/remplacement, sans reprise automatique
du nom technique précédent. Aucun alias obligatoire pour l'admission automatisée.

Nom absent/invalide/en conflit : publication refusée et état DNS non prêt
visible selon contrat du profil, sans annulation supposée de l'admission
déjà engagée. Les conventions et réservations des alias restent administrées.

Attribution/réservation et publication via contrats publics du module
DNS, permissions distinctes de la seule admission, unicité dans la zone/vue
pertinente, contexte/version/audit et idempotence sous coordination A12.
Admission engagée ne vaut pas publication DNS appliquée ; workflow ordonné
et preuve de publication/retrait, sans transaction SQL PA intermodules.
Alias, changement de cible ou renommage soumis aux mêmes contrôles ; aucun
écrasement, extension de vue, cible hors périmètre ou droit réseau implicite.
Alias CNAME directs A06k A validés ; autres types et format de label ouverts.
Boucles refusées, validité et TTL A06g respectés.

Comparaison des noms sans distinction de casse, syntaxe de labels compatible
avec clients qualifiés, limites DNS : 63 octets par label et 255 octets pour
le nom au format fil complet. Retrait/expiration/révocation A11c : noms et
alias concernés retirés/invalidation des caches maîtrisés, sans attente du
TTL pour un retrait connu. Réaffectation d'un alias à une autre instance
uniquement par nouvelle opération autorisée après retrait de l'ancienne
association ; cache applicatif non purgable universellement, A05 reste le
garde d'accès. Reprise/snapshot sans ancienne association réactivée.
Noms existants préservés, migration/renommage seulement explicitement autorisés.

Le choix vise automatisation et stabilité sans rendre un alias humain
obligatoire ni remplacer le nom technique par un nom lisible imposé.
CPU/RAM, volumétrie des noms/alias, mécanismes de réservation, persistance
des retraits et budgets à qualifier, sans gain chiffré promis. Recette par
rôle Linux/Windows physiques/VM, Docker/LXC Proxmox : concurrence/casse,
collision, changement d'IP/clé, clone, alias interdit, boucle, publication
partielle, retrait, restauration, IPv6/AAAA et absence de fuite entre vues.

[NetBird documente l'attribution automatique de noms de pairs](https://docs.netbird.io/manage/dns#automatic-peer-domain-names) ;
[la RFC 1035 fixe les limites de taille des noms DNS](https://datatracker.ietf.org/doc/html/rfc1035#section-2.3.4).
Références fonctionnelles/protocole, sans convention de nommage NetBird ni
brique reprise. A06i, option A, est validé le 6 octobre 2026 ; format,
valeurs de suffixes et qualification à préciser. Mode explicite A06j A validé ;
Alias CNAME directs A06k A validés.

##### Application au PA — A06i

Noms des instances admises dans vues privées A06c ; hostname OS, suffixe,
domaine de recherche ou nom de service non modifiés implicitement. Suffixes/
zones à choisir ; résolution sans identité/preuve/droit supplémentaires.

L'option A validée retient un nom technique stable généré depuis identifiant
d'instance admise et périmètre, alias lisibles facultatifs administrés par PBO.
Correspondance module DNS persistée, format opaque à préciser ; ni secret,
nom d'utilisateur, MAC, hostname découvert ou clé privée dans la dérivation.
Unicité vérifiée à l'engagement, jamais supposée par hash/troncature. Nom
stable pour même identifiant/périmètre ; changements IP/clé/certificat seulement
autorisés/vérifiés sans renommage imposé. Nouvelle identité, clone/remplacement :
aucun ancien nom technique repris automatiquement, aucun alias obligatoire.

Nom absent/invalide/en conflit : publication refusée et DNS non prêt visible
selon contrat du profil, sans annulation implicite d'admission déjà engagée.
Conventions et réservations des alias administrées.

Contrats publics DNS, droits de nommage/publication distincts de
l'admission, unicité zone/vue pertinente, contexte/version/audit/idempotence
A12. Admission engagée distincte de publication appliquée ; workflow et preuves
sans SQL PA intermodules. Alias/changement de cible/renommage autorisés,
sans écrasement, vue élargie, cible hors périmètre ou accès implicites.
Alias CNAME directs A06k A validés, autres types/format de label ouverts ;
boucles refusées et TTL/validité A06g maintenus. Casse indifférente, syntaxe compatible, label ≤ 63 octets et
nom complet au format fil ≤ 255 octets.

A11c retrait/expiration/révocation : retrait des noms/alias et invalidation
connue immédiate dans caches maîtrisés. Alias réaffecté seulement par nouvelle
opération autorisée après retrait de l'ancienne association ; caches applications
non purgés universellement, contrôle A05 indépendant. Restauration sans ancienne
association réactivée ; noms existants sans migration/renommage implicites.

Automatisation/stabilité et alias humains facultatifs retenus, sans nom
lisible imposé comme référence. Ressources, volumétrie, réservation, persistance
des retraits et budgets à qualifier. Recette par rôle/cible : concurrence/casse,
collision, IP/clé modifiée, clone, alias interdit/boucle, publication partielle,
retrait/restauration, IPv6/AAAA et isolement des vues. Sources dans cadrage PZT,
sans reprise de briques/conventions NetBird. A06i, option A, est validé
le 6 octobre 2026 ; format, suffixes et qualification restent à préciser.
Mode explicite A06j et alias CNAME directs A06k A validés.

#### Scenario: Conformité du traitement A06i

- **WHEN** un profil revendique le traitement A06i et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--6b3cdaf269

Source : `openspec/specs/pzt/spec.md`, ligne 1022. SHA-256 du bloc : `afb3934fa2ea0d6b106e79c5553941ccba5d9c3b72d1c8232c84dbcce0444104`.

~~~~text
### Requirement: Contrat A06j — Choix du suffixe DNS privé PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06j MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06j

Le choix concerne l'initialisation du suffixe des noms/alias A06i par
périmètre de nommage autorisé, pas un suffixe par PA, ni une modification
implicite des DNS ou domaines de recherche de l'OS. Configuration typée,
versionnée, engagée par PBO/module DNS et distribuée par contrats publics.
Les noms complets restent dans les vues et routes de zones autorisées A06c.

L'option A validée retient un suffixe explicite au provisionnement, y compris
par automatisation sous mandat approuvé, sans valeur générée par défaut.
Sous-zone d'un domaine contrôlé par l'opérateur, ou sous-zone privée choisie
sous `.internal`, après vérification de son droit d'administration et des
conflits connus. Exemple illustratif : `pzt.site-a.internal`, sans valeur
réelle adoptée. Aucun domaine public possédé obligatoire, aucune consultation
Internet imposée pour un périmètre privé autonome. Suffixe absent/invalide :
activation/readiness du DNS du périmètre bloquée selon contrat, sans empêcher
l'amorçage technique A02 ni rendre ce DNS utilisable avant validation.

Aucune génération automatique par défaut, réparation de configuration
absente/corrompue ou régénération au redémarrage. Clone devenant nouveau
périmètre : attribution autorisée et conflits vérifiés, pas de copie silencieuse
de namespace. Un identifiant ne prouve pas une unicité globale.

Comparaison DNS sans distinction de casse et limites A06i, contrôle
des collisions/chevauchements avec zones existantes, de l'autorité de zone,
des vues et du routage ; conflits bloquants sans écrasement/fusion implicites.
Une réservation `.internal` n'isole pas deux réseaux privés utilisant le
même suffixe ; absence de collision mondiale ou support OS universel non garantis.
Aucun nom privé publié/recherché dans un DNS public, aucune délégation publique,
certificat externe ou domaine de recherche installé implicitement. Nom/suffixe
ne remplace pas identité mTLS, permissions et preuve PZT A05/A10.

Suffixes/configurations existants préservés ; changement ultérieur uniquement
par migration autorisée/versionnée, avec conflits, publication/retrait, état
appliqué et invalidation des caches connus A06g vérifiés. Transition éventuelle
bornée sans prolonger droits/validités, alias et noms retirés sans résurrection.
Aucune modification de hostname, droits, montages ou hôte Proxmox implicite.
Amorçage/endpoints A02 sans dépendance circulaire au suffixe nouvellement choisi.

Namespace explicitement configuré au provisionnement et intégration aux
zones existantes retenus. Choix sans gain CPU/RAM chiffré établi ; budgets,
interfaces OS et migration restent à qualifier.
Recette Linux/Windows physiques/VM, Docker/LXC Proxmox : suffixe explicite,
absent/invalide, collision/chevauchement/casse, clone, redémarrage/restauration,
configuration existante, migration/retrait, AAAA/IPv6 et absence de fuite.

[L'ICANN réserve .internal hors délégation dans la racine DNS pour les usages privés](https://www.icann.org/en/board-activities-and-meetings/materials/approved-resolutions-special-meeting-of-the-icann-board-29-07-2024-en#section2.a).
Cette réservation ne définit ni format de sous-zone Pixs ni isolation entre
réseaux privés. A06j, option A, est validé le 6 octobre 2026 ; aucun suffixe
concret adopté. Valeurs et qualification restent à préciser.

##### Application au PA — A06j

Initialisation du suffixe des noms/alias A06i par périmètre de nommage,
commun à ses PA ; aucune modification DNS/domaines de recherche OS implicite.
Configuration typée/versionnée engagée par PBO/DNS et contrats publics,
noms complets limités aux vues/routes de zones autorisées A06c.

L'option A validée retient un suffixe explicite au provisionnement, automatisable
sous mandat approuvé, sans défaut généré. Sous-zone de domaine contrôlé ou
sous-zone privée choisie sous `.internal`, après droits/conflits vérifiés ;
`pzt.site-a.internal` illustratif, non adopté. Aucun domaine public possédé
ou accès Internet requis pour profil privé autonome. Absence/invalidité :
DNS non activable/non prêt selon contrat, amorçage technique A02 préservé.

Aucune génération par défaut, réparation de configuration absente/corrompue
ou régénération au redémarrage. Clone nouveau périmètre : attribution
autorisée/conflits vérifiés, sans namespace copié silencieusement ; identifiant
sans unicité mondiale présumée.

Casse/tailles DNS A06i, collisions/chevauchements avec zones existantes,
autorité/vue/routage vérifiés ; conflit bloquant sans écrasement/fusion.
`.internal` réservé ne garantit ni isolation de réseaux privés ni support OS
universel. Aucun DNS public pour nom privé, délégation publique, certificat
externe ou domaine de recherche implicites ; suffixe sans droit/identité PZT.

Suffixes existants préservés, migration ultérieure autorisée/versionnée avec
conflits, publication/retrait, preuves appliquées et invalidation connue A06g.
Transition bornée sans droits/validités prolongés ni nom retiré ressuscité ;
aucun hostname, montage, droit ou hôte Proxmox modifié implicitement. A02 sans
dépendance circulaire. Maîtrise des zones au provisionnement retenue ;
CPU/RAM, interfaces et migration à qualifier. Recette : suffixe fourni/absent/invalide,
conflit/casse/chevauchement, clone, redémarrage/restauration, profil existant,
migration/retrait, IPv6/AAAA et absence de fuite. Source ICANN dans cadrage PZT ;
A06j, option A, est validé le 6 octobre 2026 ; aucun suffixe concret adopté.
Valeurs et qualification restent à préciser.

#### Scenario: Conformité du traitement A06j

- **WHEN** un profil revendique le traitement A06j et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--33f3f9b057

Source : `openspec/specs/pzt/spec.md`, ligne 1123. SHA-256 du bloc : `56795858d404700294860712c2b05cdb959cb895c0d1d8572f7ba849f4d36180`.

~~~~text
### Requirement: Contrat A06k — Représentation des alias DNS lisibles des PA — option A validée le 6 octobre 2026

Le rôle chargé du traitement A06k MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A06k

Alias facultatifs des instances PA A06i sous suffixe explicite A06j seulement ;
noms de services/SRV, PTR et zones externes hors choix. Module PBO/DNS,
contrats publics, permissions et vues A06c conservés.

L'option A validée retient chaque alias lisible en CNAME directement vers
le nom technique courant de l'instance admise, sans alias vers alias dans
ce profil initial. Cible gérée compatible avec vue/périmètre, jamais externe
ou apprise hors configuration. Une cible par alias ; ni boucle, ni CNAME
à la racine de zone, ni A/AAAA ou autre donnée ordinaire incompatible au même
nom. Métadonnées DNSSEC éventuelles régies par les normes, sans activation
implicite. Le service peut joindre les A/AAAA terminales autorisées à la
réponse quand disponibles : requête supplémentaire non systématique.

Opérations autorisées/idempotentes A06i/A07/A12, unicité/collisions,
pas de nouvelle permission par alias. Résolution/suivi limités aux données
visibles du contexte, sans découverte hors vue ni repli public. Chaque élément
nécessaire respecte son TTL restant et ses validités A06g ; chaîne/réponse
complète réutilisable dans leurs bornes communes seulement. Cache, suivi
ou adresse modifiée sans droit/durée prolongés. IPv6 A06d désactivé : aucune
adresse AAAA PZT utilisable via alias, CNAME sans activation IPv6 indirecte.
Retrait connu invalide caches maîtrisés concernés ; A05 reste applicable
aux adresses conservées par les applications.

Résolution sans dispense d'identité de destination, liaison de clé ou contrôles
TLS A10. Aucun nom ajouté automatiquement au certificat, aucune vérification
de nom/contexte désactivée pour rendre un alias utilisable ; intégration
applicative à qualifier. Alias existants préservés ; conversion de représentation
seulement par migration autorisée.

Liaison au nom stable retenue, sans copies A/AAAA indépendantes sur les alias.
Requêtes, taille des réponses,
mises à jour, CPU/RAM/latence à mesurer, sans gain global promis. Recette
Linux/Windows physiques/VM, Docker/LXC Proxmox : CNAME+terminal, cible absente/
interdite, boucle/chaîne, collision/racine, IP modifiée, application partielle/
reprise, retrait/TTL, AAAA désactivé, certificat incompatible et isolement.

[La RFC 1034 décrit CNAME et le suivi des alias](https://www.rfc-editor.org/rfc/rfc1034.html#section-3.6.2) ;
[la RFC 2181 précise l'unicité de cible et les données compatibles](https://www.rfc-editor.org/rfc/rfc2181.html#section-10.1).
Le profil Pixs ajoute contexte et cycle de vie. A06k, option A, est validé
le 6 octobre 2026 ; contrats et qualification restent à préciser.

##### Application au PA — A06k

Alias facultatifs des instances A06i sous suffixe explicite A06j ; noms de
services/SRV, PTR et zones externes hors choix. Module PBO/DNS, contrats
publics, permissions et vues A06c conservés.

L'option A validée retient CNAME vers le nom technique courant de l'instance,
une cible gérée compatible avec vue/périmètre, sans alias vers alias, cible
externe, boucle ou racine de zone. Aucun A/AAAA ou autre donnée ordinaire
incompatible au même nom ; normes DNSSEC pour métadonnées éventuelles,
sans activation implicite. Réponse avec A/AAAA terminales autorisées possible,
sans requête supplémentaire systématique.

Opérations autorisées/idempotentes A06i/A07/A12, unicité/collisions,
contexte/vues sans découverte hors permission ni repli public. TTL/validité
A06g pour chaque élément, réutilisation complète dans bornes communes,
sans durée/droit prolongés par cache/suivi/modification. IPv6 A06d désactivé :
aucune adresse AAAA PZT via alias, CNAME sans activation indirecte. Retrait
connu invalide caches maîtrisés, A05 protège même adresse applicative conservée.
Identité/clé/TLS A10 toujours contrôlés ; aucun nom ajouté au certificat ou
vérification désactivée pour alias, intégration applicative à qualifier.
Alias existants préservés, conversion seulement par migration autorisée.

Liaison au nom stable retenue sans copies A/AAAA indépendantes sur les alias.
Requêtes, taille, mises à jour,
CPU/RAM/latence à mesurer. Recette par rôle/cible : CNAME+terminal, cible
absente/interdite, boucle/chaîne, collision/racine, IP modifiée, état partiel/
reprise, retrait/TTL, AAAA désactivé, certificat incompatible et isolement.
Sources RFC dans cadrage PZT. A06k, option A, est validé le 6 octobre 2026 ;
contrats et qualification restent à préciser.

#### Scenario: Conformité du traitement A06k

- **WHEN** un profil revendique le traitement A06k et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

