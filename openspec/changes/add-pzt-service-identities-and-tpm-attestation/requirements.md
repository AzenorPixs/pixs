# Références normatives — Z09

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 120 | [Identités de service, PKI et attestation](../../specs/pzt/spec.md#L120) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2362 | [Contrat A10a — Transport partagé et identités de service — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L2362) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2494 | [Contrat A10b — Certificats et liaison WireGuard — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L2494) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2624 | [Contrat A10c — Déclencheurs d'attestation TPM — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L2624) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2766 | [Contrat A10d — Admission par profil TPM — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L2766) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 2896 | [Contrat A10e — Périmètre des mesures d'intégrité — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L2896) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3034 | [Contrat A10f — Gestion des références d'intégrité — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L3034) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--60b0ba04d0

Source : `openspec/specs/pzt/spec.md`, ligne 120. SHA-256 du bloc : `4a8ba1d3aebf494827b65c31c43fae0969ba6b13912768b412a8a8bda4e05f4e`.

~~~~text
### Requirement: Identités de service, PKI et attestation

Le transport partagé MUST conserver des identités et permissions de services distinctes. X.509 et liaison WireGuard JWS MUST être liés à l'identité et au contexte courant. Les profils TPM/vTPM, mesures, fraîcheur et références signées/versionnées MUST suivre A10a–A10f ; posture déclarée MUST NOT être présentée comme une attestation. Clone, snapshot ou cohébergement MUST NOT créer une confiance implicite.

#### Scenario: Identités de service, PKI et attestation

- **WHEN** un clone réutilise une ancienne configuration et une preuve TPM
- **THEN** identité et preuves sont réévaluées avant admission
~~~~

### Référence pzt--6eb3b452fb

Source : `openspec/specs/pzt/spec.md`, ligne 2362. SHA-256 du bloc : `08d6ad5a43000ba7b2d2ca2458d31587d3d4ab3ca27e15c0d8621f47a871e421`.

~~~~text
### Requirement: Contrat A10a — Transport partagé et identités de service — option A validée le 5 octobre 2026

Le rôle chargé du traitement A10a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10a

Cet arbitrage précise la granularité des pairs WireGuard et le point de
contrôle des services. Il conserve la séparation entre identité stable
Pixs, certificat PZT, clé publique WireGuard et clé d'attestation TPM.
Les formats de certificat et de liaison sont à choisir en A10b ; les
conditions et déclencheurs d'attestation restent à préciser en A10c.

L'option A validée le 5 octobre 2026 mutualise le transport WireGuard pour plusieurs services
dans un même environnement d'exécution et un même périmètre PZT compatible.
Chaque service conserve une référence stable, une identité authentifiée,
des permissions propres et un point de contrôle adapté au-dessus du
transport : intégration applicative, proxy ou adapter PA avec identification
vérifiée du processus. Une IP, un port, une étiquette déclarée par l'appelant
ou un tunnel établi ne prouvent pas l'identité du service. Ce choix évite
la multiplication systématique des interfaces et des clés WireGuard par
service ; son coût global reste à qualifier.

Identités et liaisons sont résolues explicitement
vers les DigitalIdentity et contextes Pixs autorisés, selon les contrats
publics. L'identité technique du PA, le service, l'utilisateur éventuel et
l'acteur initial d'une opération restent distincts. Les décisions métier
restent sous l'autorité Django ; droit de transport et permission d'action
ne se confondent pas. Une liaison à un tenant ou scope est vérifiée et ne
crée aucun accès intertenant contournant le profil actuellement validé.

La mutualisation ne fusionne pas les VM, conteneurs,
installations ou périmètres de confiance. Un environnement peut conserver
plusieurs pairs ou interfaces lorsqu'une séparation explicitement déclarée
l'exige ; aucune clé globale n'est partagée entre tous les PA d'un hôte.
Le propriétaire réseau reste `pzt-daemon` selon A04a, avec demandes autorisées
des autres modes. Les services et sessions ne reçoivent pas la clé privée
WireGuard du propriétaire ni ses privilèges système du fait du partage.

Le point de contrôle lie de manière vérifiable l'identité du service à la
connexion ou opération concernée et au contexte autorisé. Il refuse
l'usurpation d'un service voisin et l'accès contournant ce contrôle, y
compris localement selon A03. Les flux dont le profil ne peut vérifier
l'identité ou les preuves requises restent bloqués ; le choix A n'assimile
pas tous les processus de l'hôte à un service authentifié. Expiration et
révocation A05 restent applicables aux connexions persistantes. Le retrait
d'un service invalide ses accès ; les autres ne continuent que si leurs
propres conditions restent vérifiables. Le retrait du PA ou du pair invalide
les accès qui en dépendent.

Le partage du transport ne réduit pas l'exigence d'attestation TPM à chaque
connexion ou reconnexion PZT du PA. Les connexions logiques, les services
et leurs preuves requises sont distingués des handshakes ou renouvellements
WireGuard ; le mapping et les déclencheurs exacts restent à préciser en A10c,
sans dispense implicite. Une preuve d'intégrité ne couvre que les éléments
mesurés par la chaîne de confiance ; elle ne prouve pas à elle seule le
service appelant. Le TPM physique, le passthrough et le vTPM gardent leurs
niveaux de confiance distincts ; conteneur et hôte ne deviennent pas une
même identité par partage du TPM.

L'intégration, la protection des credentials, l'anti-contournement et les
limites de cette isolation sont qualifiés sur Linux/Windows physiques et
VM, Docker/LXC Proxmox, selon A01/A04. Le réseau ne protège pas implicitement
contre un administrateur contrôlant l'environnement. Nombre d'interfaces,
clés, états, coût des contrôles de service, CPU et mémoire sont comparés,
sans économie présumée. Aucune bibliothèque, format de preuve, privilège
hôte ou nouveau mécanisme de délégation n'est adopté par ce choix.

[Le modèle WireGuard](https://www.wireguard.com/#cryptokey-routing) associe
clés et adresses IP des pairs ; le contrôle d'identité de service relève
des contrats PZT/Pixs. [L'architecture RATS, RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html),
distingue production de preuves, vérification et décision d'utilisation ;
elle sert de référence sans sélectionner un format TPM ou un composant.
A10a, option A, est validé ; modalités et qualification restent à préciser.

##### Application au PA — A10a

Ce choix précise les pairs WireGuard et les contrôles des services.
Identité Pixs, certificat PZT, clé WireGuard et clé d'attestation TPM restent
distincts ; formats et liaisons sont à choisir en A10b, conditions et
déclencheurs d'attestation à préciser en A10c.

L'option A validée le 5 octobre 2026 mutualise WireGuard entre services dans un même
environnement d'exécution et un même périmètre PZT compatible. Chaque
service garde identité authentifiée, référence stable, permissions et
point de contrôle propre : intégration applicative, proxy ou adapter avec
identification vérifiée du processus. IP, port et étiquette déclarée ne
suffisent pas. Ce choix évite des interfaces et clés WireGuard
systématiquement dédiées à chaque service ; le coût global reste à qualifier.

PA distingue son identité, le service, l'utilisateur
éventuel et l'acteur initial. Mappings DigitalIdentity et contextes sont
vérifiés par les contrats publics ; Django reste l'autorité métier, sans
accès SQL ni permission intertenant implicite. Chaque opération exige ses
propres permissions, même sur un transport admis.

Le partage reste interne à un périmètre compatible : VM,
conteneurs et installations distinctes gardent leurs frontières. Plusieurs
pairs ou interfaces restent possibles lorsque le profil l'exige, sans clé
globale commune aux PA de l'hôte. `pzt-daemon` garde la propriété A04a ;
autres modes et services ne reçoivent ni sa clé WireGuard privée ni ses
privilèges par le partage. Le contrôle du service lie identité, contexte
et connexion ou opération, refuse l'usurpation et le contournement, y
compris localement. Sans identité ou preuve requise vérifiable, le flux
reste bloqué. Révocation du service retire ses accès ; les autres restent
soumis à leurs conditions, et révocation du PA ou du pair retire les accès
dépendants. Expiration et révocation A05 s'appliquent aux connexions persistantes.

Attestation TPM à chaque connexion ou reconnexion PZT du PA reste exigée ;
mutualisation, handshake ou renouvellement WireGuard ne créent pas de
dispense. Les connexions logiques de service et leurs preuves requises
sont distinguées ; mapping et déclencheurs A10c restent à préciser. Une
attestation ne couvre que les éléments réellement mesurés et ne prouve
pas à elle seule l'appelant. TPM physique, passthrough et vTPM restent
distincts, avec liaison PA–conteneur–hôte vérifiée selon le profil.

Protection des credentials, contrôle des services, anti-contournement,
limites face à l'administrateur hôte et consommation sont qualifiés sur
Linux/Windows physiques et VM, Docker/LXC Proxmox, selon les backends A01.
Aucune économie CPU/mémoire, bibliothèque, format de preuve ou permission
hôte n'est présumé. Les sources figurent dans le cadrage PZT.
A10a, option A, est validé ; modalités et qualification restent à préciser.

#### Scenario: Conformité du traitement A10a

- **WHEN** un profil revendique le traitement A10a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--ec480629cf

Source : `openspec/specs/pzt/spec.md`, ligne 2494. SHA-256 du bloc : `edbab4d4df03867220877bd18bbec65462d7a29978488ef4852f770c0551d921`.

~~~~text
### Requirement: Contrat A10b — Certificats et liaison WireGuard — option A validée le 5 octobre 2026

Le rôle chargé du traitement A10b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10b

Le choix porte sur le certificat d'identité PZT et l'association de cette
identité à une clé publique WireGuard. Identité stable, clé du certificat,
clé WireGuard et clé d'attestation TPM restent distinctes. WireGuard ne
consomme pas le certificat dans son handshake ; les contrôles PZT vérifient
la liaison avant admission. Les formats de permissions et de preuves TPM
ne sont pas choisis ici, ni les déclencheurs A10c.

L'option A validée le 5 octobre 2026 utilise un certificat X.509 pour l'identité PZT/TLS et
un objet de liaison séparé : JSON typé, versionné et signé asymétriquement
au format JWS par l'autorité PZT compétente. Cette séparation permet une
rotation WireGuard par remplacement de la liaison vérifiée, sans imposer
la réémission du certificat d'identité encore valide. Elle exige de vérifier
la cohérence et la validité courante des deux éléments. Ce choix sépare
leurs cycles de vie et réutilise les mécanismes TLS usuels ;
aucun gain CPU ou mémoire n'est présumé.

La liaison identifie explicitement l'émetteur,
l'identité stable et sa référence de credential, le PA ou pair concerné,
le contexte autorisé et la clé publique WireGuard. Elle porte identifiant
ou version autoritative, usage, destinataire, dates d'émission et de
validité et références nécessaires à son retrait. Les noms de champs et
schémas restent à définir dans les contrats publics. Une liaison de pair
n'authentifie pas tous les services partageant son transport selon A10a.
La possession de la clé WireGuard est vérifiée séparément selon une
procédure d'enrôlement ou de rotation à qualifier : cette clé d'accord
X25519 ne signe ni la liaison JWS ni un certificat d'identité.

Les chaînes de certificats sont vérifiées depuis des ancrages explicitement
configurés, avec émetteur, identité, usages, contexte, validité temporelle
et état de révocation requis. Une autorité publique reconnue par l'OS
n'obtient aucun pouvoir PZT implicite. Signature correcte et certificat
valide ne suffisent pas à l'admission, à l'attestation ou à une permission
métier. L'autorité Django, les mappings DigitalIdentity et les garanties
A05 demeurent applicables.

Signature JWS, en-têtes protégés et octets signés suivent le
standard ; le profil fixe explicitement les algorithmes permis, le type
et les références de clés. Algorithme non autorisé, signature absente,
champ obligatoire inconnu, doublon JSON ou dépassement de taille sont
refusés. Une référence de clé reçue ne crée pas d'ancrage de confiance et
ne déclenche pas de récupération depuis une URL non autorisée. Le contrôle
ne remplace pas JWS par une signature JSON inventée ou un secret MAC
commun aux vérificateurs.

Expiration ou révocation connue de l'identité, du certificat, de la liaison
ou du pair invalide les accès dépendants. La rotation ne prolonge pas les
permissions et ne réintroduit pas une ancienne liaison après restauration.
La validité effective reste bornée par les éléments requis et par A05 ;
cohérence des versions, propagation et fonctionnement en partition sont
qualifiés dans le cadre A12a–A12g validé ; modalités de réalisation à préciser.

Protection des clés, vérifications, rotation et retrait sont qualifiés sur
Linux/Windows physiques et VM, Docker/LXC Proxmox, avec les frontières
TPM/passthrough/vTPM existantes. Algorithmes, durées, nommage des identités,
profil X.509, sérialisation JWS, distribution des clés et révocations,
bibliothèques et seuils restent à débattre ; aucune dépendance ou permission
hôte n'est adoptée.

[X.509, RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.html), décrit les
certificats, chaînes et extensions critiques ;
[JWS, RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html), définit la
protection de charges utiles signées ;
[RFC 8410](https://www.rfc-editor.org/rfc/rfc8410.html) distingue les usages
d'accord de clé X25519 des usages de signature.
A10b, option A, est validé ; profil et paramètres restent à spécifier et qualifier.

##### Application au PA — A10b

Ce choix lie l'identité PZT du PA à sa clé publique WireGuard. Identité
stable, clé du certificat, clé WireGuard et clé d'attestation TPM restent
distinctes. Le certificat ne participe pas au handshake WireGuard ; PZT
vérifie la liaison avant admission. Permissions et formats de preuves TPM,
ainsi que les déclencheurs A10c, restent hors de ce choix.

L'option A validée le 5 octobre 2026 associe un certificat d'identité
X.509 PZT/TLS et un
objet séparé de liaison JSON typé, versionné, signé asymétriquement en JWS
par l'autorité PZT compétente. La rotation WireGuard remplace la liaison
vérifiée sans imposer la réémission d'un certificat d'identité encore valide.
PA vérifie la cohérence et la validité courante des deux éléments. Cette
option sépare les cycles de vie ; son coût reste
à qualifier.

La liaison identifie émetteur, identité stable et credential, PA
ou pair, contexte, clé publique WireGuard, version ou identifiant
autoritatif, usage, destinataire, validité et références de retrait.
PA vérifie les mappings DigitalIdentity via les contrats publics, sans
accès SQL ni permission métier implicite ; une liaison de pair n'identifie
pas tous les services selon A10a. La possession de la clé WireGuard est
vérifiée séparément par la procédure d'enrôlement ou de rotation à qualifier.
La clé d'accord X25519 ne signe pas la liaison JWS ou le certificat.

Ancrages de confiance, émetteurs, identités, usages, contexte, dates et
révocations sont contrôlés explicitement. PA vérifie les octets et
en-têtes protégés conformément à JWS, avec algorithmes permis et références
de clés configurés. Signature absente, algorithme non autorisé, doublon
JSON, champ obligatoire inconnu et dépassement de taille sont refusés ;
une référence reçue ne crée pas de confiance ni de récupération depuis
une URL non autorisée. Aucun MAC partagé entre vérificateurs n'est retenu.

Admission, attestation et permissions restent distinctes. Expiration ou
révocation connue de l'identité, du certificat, de la liaison ou du pair
retire les accès dépendants selon A05. Rotation et restauration ne
prolongent pas un droit ni ne réintroduisent une liaison invalidée.
Cohérence des versions et partitions sont qualifiées sans choisir A12.

Protection des clés, rotation, retrait et coût sont qualifiés sur
Linux/Windows physiques et VM, Docker/LXC Proxmox, avec distinction
TPM/passthrough/vTPM. Algorithmes, durées, nommage, profil X.509,
sérialisation JWS, diffusion des clés et révocations, bibliothèques et
seuils restent à spécifier. Aucune dépendance ou permission hôte n'est
adoptée. Les sources officielles figurent dans le cadrage PZT.
A10b, option A, est validé ; profil et paramètres restent à spécifier et qualifier.

#### Scenario: Conformité du traitement A10b

- **WHEN** un profil revendique le traitement A10b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--7ca51f88af

Source : `openspec/specs/pzt/spec.md`, ligne 2624. SHA-256 du bloc : `89c506273b5691f5c7262d0ce8e48b702bc393e83b0c0f7b3214df09e8ea7c84`.

~~~~text
### Requirement: Contrat A10c — Déclencheurs d'attestation TPM — option A validée le 5 octobre 2026

Le rôle chargé du traitement A10c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10c

Le choix précise quand produire une nouvelle preuve TPM. L'exigence déjà
établie demeure : chaque connexion ou reconnexion du PA à PZT exige un
défi frais et une attestation vérifiée avant ouverture des accès concernés.
Ce choix ne décide ni des conditions d'admission sans TPM accessible, ni
du niveau de confiance d'un vTPM, ni des profils de mesures ou formats.

Une connexion du PA désigne ici une association PZT authentifiée et admise,
identifiée par le PA, son interlocuteur, le contexte et une génération de
session. Son établissement, son rétablissement après interruption du canal
de contrôle et une réauthentification exigent une nouvelle attestation,
y compris après reprise TLS ; un ticket ne dispense pas du contrôle TPM.
L'amorçage A02 reste limité aux échanges techniques nécessaires avant
admission. La même règle s'applique au profil TLS local A03.

L'option A validée le 5 octobre 2026 atteste cette association à chaque
connexion ou
reconnexion du PA, puis renouvelle la preuve à l'expiration de sa fraîcheur
ou sur événement de sécurité. Dans cette même association encore valide,
les connexions de service utilisent le résultat d'attestation du PA dans
sa portée déclarée, tout en vérifiant séparément leur identité, leur
liaison au PA, leur contexte et leurs permissions selon A10a. Si le profil
d'un service ou d'une opération exige une preuve supplémentaire, elle reste
obligatoire. Ce choix évite une opération TPM systématique par connexion
de service ; l'économie réelle reste à mesurer.

Une nouvelle attestation est exigée après redémarrage du PA,
changement de rattachement à l'hôte ou d'identité/clé liée, migration,
restauration ou clonage, modification détectée des mesures requises,
changement du référentiel ou de la politique d'attestation applicable,
et demande autorisée du vérificateur. L'extension à un autre contexte ne
réutilise pas implicitement une preuve hors de sa portée. Un rejet ou une
révocation ne se corrige pas par réattestation automatique : les conditions
de réadmission restent distinctes et explicitement autorisées.

Le renouvellement automatique des clés de session WireGuard, un keepalive,
un changement d'endpoint ou une bascule direct/relais ne constituent pas,
à eux seuls, une nouvelle association PZT. Ils ne renouvellent aucune preuve
ni permission. Si l'association ou sa liaison vérifiable est perdue, le
rétablissement impose une nouvelle attestation ; le mapping est qualifié
sur les transports A07/A09, sans assimilation entre leurs connexions.

Le vérificateur produit un résultat authentifié, limité au PA/hôte,
à la génération et au contexte vérifiés, au profil de mesures, aux versions
de références et de politique, avec date et échéance explicites. Défi
imprévisible, délai de réponse borné, liaison au canal et refus du rejeu
sont contrôlés ; leur mécanisme cryptographique reste à spécifier.
Une réponse fraîche ne rend pas fraîches des mesures anciennes : seules
les mesures obtenues par une chaîne de confiance effectivement qualifiée
peuvent justifier l'état couvert. La preuve ne garantit pas l'absence de
compromission entre deux observations.

Les durées maximales de fraîcheur, délais, marges de renouvellement et
opérations exigeant une preuve supplémentaire sont définis par profil et
qualifiés ; sans configuration valide, les accès exigeant cette preuve
restent bloqués. L'expiration et toute invalidation connue retirent les
accès dépendants, même avec tunnel ou connexions persistantes. A05 reste
applicable ; renouveler l'attestation ne renouvelle pas les permissions,
et une partition ne prolonge pas les échéances.

La qualification couvre Linux/Windows physiques et VM, Docker/LXC Proxmox,
TPM physique, passthrough et vTPM déclarés, services concurrents, reprise
du contrôle, changement de transport, saturation et panne du TPM. Elle
vérifie anti-rejeu, liaison PA–conteneur–hôte, retrait effectif et consommation
PA/vérificateur. Aucun accès hôte, bibliothèque ou privilège supplémentaire
n'est adopté ; l'admission suit les profils A10d validés, dont les matrices
et paramètres restent à qualifier.

[L'architecture RATS, RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html#section-10),
distingue fraîcheur des preuves et des résultats de vérification.
[Le protocole WireGuard](https://www.wireguard.com/protocol/) gère ses
renouvellements de clés de session ; ceux-ci restent distincts des décisions
PZT retenues ici. A10c, option A, est validé ; paramètres et qualification
restent à préciser.

##### Application au PA — A10c

Chaque connexion ou reconnexion du PA à PZT conserve l'exigence d'un défi
frais et d'une attestation vérifiée avant accès. La connexion désigne une
association PZT authentifiée et admise, liée au PA, à son interlocuteur,
au contexte et à une génération de session. Établissement, rétablissement
après interruption du canal de contrôle et réauthentification exigent une
nouvelle attestation, même après reprise TLS. Amorçage A02 limité et
profil TLS local A03 gardent leurs garanties.

L'option A validée le 5 octobre 2026 renouvelle ensuite l'attestation sur
expiration de
fraîcheur ou événement de sécurité. Dans la même association encore valide,
les services utilisent le résultat PA dans sa portée déclarée et gardent
leurs propres identités, liaisons au PA, contextes et permissions A10a.
Toute preuve supplémentaire exigée par leur profil reste obligatoire.
Ce choix évite une sollicitation TPM systématique par connexion de
service ; les ressources réellement consommées restent à mesurer.

Redémarrage, changement d'hôte ou d'identité/clé
liée, migration, clone, restauration, modification détectée des mesures
requises, changement du référentiel ou de politique applicable, et demande
autorisée du vérificateur imposent une nouvelle attestation. Aucun résultat
ne s'étend implicitement à un autre contexte. Rejet et révocation gardent
leurs conditions distinctes de réadmission autorisée.

Renouvellement automatique WireGuard, keepalive, endpoint ou bascule
direct/relais ne créent pas seuls une nouvelle association PZT et ne
renouvellent ni preuve ni droit. La perte de l'association ou de sa liaison
vérifiable impose une nouvelle attestation au rétablissement. Ce mapping
reste à qualifier pour A07/A09.

Le résultat authentifié lie PA/hôte, génération, contexte, profil de
mesures, versions des références/politique et échéance. Défi imprévisible,
délai borné, liaison au canal et anti-rejeu sont contrôlés. Une réponse
fraîche ne rend pas actuelles des mesures anciennes ; chaîne de mesure,
états couverts et limites entre deux observations sont qualifiés.

Fraîcheur maximale, délais, marges et opérations nécessitant une preuve
supplémentaire restent à fixer par profil. Configuration absente ou
invalide, expiration ou invalidation connue bloque les accès dépendants,
même sur un tunnel persistant. A05 reste applicable ; attestation et
permissions ont des échéances distinctes, sans prolongation en partition.

Qualification : Linux/Windows physiques et VM, Docker/LXC Proxmox, TPM
physique/passthrough/vTPM déclarés, liaisons PA–conteneur–hôte, concurrence,
reprises, anti-rejeu, retrait, saturation, panne et ressources. Admission
selon les profils A10d validés ; matrices, paramètres, formats et mesures
restent à qualifier ; aucun privilège hôte ou bibliothèque n'est adopté. Les sources
figurent dans le cadrage PZT. A10c, option A, est validé ; paramètres et
qualification restent à préciser.

#### Scenario: Conformité du traitement A10c

- **WHEN** un profil revendique le traitement A10c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--9064a45f10

Source : `openspec/specs/pzt/spec.md`, ligne 2766. SHA-256 du bloc : `3ca92224afdf83207a023cf98d5834e5b6de18ee693a0a3558eff056e4a56022`.

~~~~text
### Requirement: Contrat A10d — Admission par profil TPM — option A validée le 5 octobre 2026

Le rôle chargé du traitement A10d MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10d

Ce choix détermine les sources d'attestation admissibles selon la plateforme.
Il conserve A10c : chaque connexion ou reconnexion du PA exige une preuve
fraîche vérifiable. Aucun profil ne dispense de la mesure de confiance du
binaire PA et de l'environnement requis, de l'identité X.509, de la liaison
WireGuard JWS, des permissions et de la révocation.

L'option A validée le 5 octobre 2026 accepte des profils qualifiés
distincts : TPM physique
sur machine physique, TPM en passthrough qualifié ou vTPM à provenance
vérifiée pour les VM, et attestation de l'hôte avec liaison mesurée au PA
pour les conteneurs. La politique autorise explicitement les sources et
la couverture exigées pour chaque ressource ou opération. Un vTPM ne vaut
pas automatiquement une preuve ancrée dans un TPM physique. Ce choix
couvre Linux/Windows physiques et VM, Docker/LXC Proxmox, sous réserve
de qualification des profils avant admission.

La présence d'une interface TPM, une signature ou
un certificat auto-déclaré ne prouvent ni provenance ni état du PA. Le
vérificateur contrôle l'origine des clés, les ancrages approuvés, les liens
PA–VM/conteneur–hôte et les mesures effectivement couvertes. Pour un vTPM,
l'hyperviseur et le fournisseur deviennent des éléments de confiance
explicitement évalués ; protection de l'état, des sauvegardes et clés,
risques de copie et de retour à un état ancien sont qualifiés. Un simple
émulateur autonome ne devient pas un vTPM de production approuvé.

Pour Docker/LXC, partager le TPM n'accorde aucune identité commune aux PA.
La chaîne de mesure doit distinguer le PA réellement exécuté et son
rattachement ; une mesure de l'hôte ou de l'image seule ne suffit pas si
le profil exige d'autres éléments. Un accès médiatisé à l'attestation de
l'hôte est une possibilité à spécifier et qualifier, sans exposer sa clé
privée ni attribuer automatiquement au conteneur le périphérique TPM,
des montages ou privilèges supplémentaires. Le passthrough en VM n'est
pas choisi par défaut : concurrence d'accès et limitations de migration
sont évaluées pour le backend exact.

Le profil attendu est provisionné et versionné par une autorité compétente.
Un PA ne choisit pas un profil moins exigeant après un refus ou une panne.
Le résultat déclare source de confiance, provenance, couverture et limites ;
la politique d'accès exige les preuves correspondantes, sans surclassement
implicite d'assurance Pixs. La classe Courant/Protégé/Critique A05 ne fixe
pas automatiquement un type de TPM : son mapping reste à valider.

Sans TPM accessible ou source admise, avec preuve manquante ou invérifiable,
l'admission et les accès dépendants sont bloqués. Avant admission, seul
l'amorçage technique limité A02 reste possible dans ses permissions et
limites ; aucun canal de gestion PBO–PA ou accès métier n'est ouvert par
cette exception. Le diagnostic local suit la procédure opérateur prévue.
Des fixtures TPM logiciel peuvent servir aux tests isolés, sans admission
implicite dans les périmètres de production ni accès aux données réelles.

Clonage, restauration, migration, changement d'hôte ou de clés imposent
réévaluation et nouvelles preuves selon A10c ; une identité copiée n'est
pas acceptée automatiquement. La politique traite les identités dupliquées,
les rattachements concurrents et les preuves issues d'un état restauré,
sans réactiver de droits révoqués. Les garanties de la chaîne restent
bornées par son modèle de confiance face à l'administrateur hôte.

Les matrices d'admission, mesures, ancrages, formats, adapters, durées et
budgets restent à spécifier puis qualifier pour chaque cible. Ce choix
n'adopte aucune bibliothèque, dépendance, modification Proxmox, droit hôte
ou nouvelle interface de délégation.

[L'architecture RATS, RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html#section-3.2),
explique les chaînes de mesure et leurs environnements de confiance.
[La documentation TPM QEMU](https://www.qemu.org/docs/master/specs/tpm.html)
distingue passthrough et émulation, avec leurs contraintes d'état et de
migration ; elle sert de référence sans sélectionner un backend Pixs.
A10d, option A, est validé ; matrices et paramètres restent à spécifier et qualifier.

##### Application au PA — A10d

Le choix précise les sources d'attestation admissibles, en maintenant A10c,
la mesure de confiance du PA et de l'environnement requis, l'identité
X.509, la liaison WireGuard JWS, les permissions et la révocation.

L'option A validée le 5 octobre 2026 qualifie des profils distincts :
TPM physique sur
machine physique ; passthrough qualifié ou vTPM à provenance vérifiée en
VM ; attestation de l'hôte avec liaison mesurée au PA pour Docker/LXC.
Chaque ressource ou opération exige une source et une couverture déclarées
par sa politique. Un vTPM ne vaut pas automatiquement un ancrage physique.
Ce choix couvre les plateformes prévues sous réserve de qualification
avant admission.

Le vérificateur contrôle provenance des clés, ancrages, mesures et
rattachements PA–VM/conteneur–hôte. Confiance dans l'hyperviseur/fournisseur,
protection de l'état vTPM, sauvegardes, copie et restauration sont qualifiées.
Un émulateur autonome ne devient pas un vTPM de production approuvé.
Pour les conteneurs, TPM partagé ne signifie pas identité partagée ;
attestation de l'hôte ou de l'image seule ne suffit pas si les mesures
requises couvrent davantage. Un accès médiatisé à l'attestation de l'hôte
reste à spécifier ; aucun périphérique, montage, clé privée ou privilège
hôte n'est accordé implicitement. Passthrough et mobilité sont qualifiés
par backend, sans choix par défaut.

Le profil attendu est provisionné et versionné. PA ne réduit pas ses
exigences après refus ou panne. Les résultats distinguent provenance,
source, couverture et limites, sans surclassement d'assurance Pixs. Le
mapping aux classes A05 reste à valider.

Sans source admise et accessible ou preuve vérifiable, admission et accès
dépendants restent bloqués. Seul l'amorçage technique limité A02 demeure
possible avant admission, sans gestion PBO–PA ni accès métier. Diagnostic
local selon procédure opérateur ; fixtures TPM logiciel réservées aux tests
isolés, sans admission implicite en production.

Clone, restauration, migration ou changement d'hôte/clé imposent nouvelles
preuves et réévaluation A10c. Identités copiées, rattachements concurrents
et droits révoqués ne sont pas réactivés automatiquement. Limites face à
l'administrateur hôte, matrices d'admission, mesures, formats, adapters,
ancrages, durées et budgets restent à qualifier. Aucun changement Proxmox,
dépendance ou privilège n'est adopté. Les sources figurent dans le cadrage PZT.
A10d, option A, est validé ; matrices et paramètres restent à spécifier et qualifier.

#### Scenario: Conformité du traitement A10d

- **WHEN** un profil revendique le traitement A10d et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--110cd85b06

Source : `openspec/specs/pzt/spec.md`, ligne 2896. SHA-256 du bloc : `909d2dae81dfcd2bc69d7124e35c88c5e4fdab8e0f1f201d53fbad88e3d70983`.

~~~~text
### Requirement: Contrat A10e — Périmètre des mesures d'intégrité — option A validée le 5 octobre 2026

Le rôle chargé du traitement A10e MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10e

Ce choix définit les éléments dont l'intégrité doit être attestée. Il
conserve A10c/A10d : preuve fraîche, provenance et rattachements vérifiés,
profils distincts, admission bloquée si une preuve requise manque. Il ne
sélectionne ni bibliothèque, algorithme, banque PCR ou durée de fraîcheur.

L'option A validée le 5 octobre 2026 retient des profils de mesures
ciblés et versionnés,
avec un socle obligatoire : chaîne de démarrage et composants de confiance
nécessaires à la production des preuves, PA réellement chargé, runtime,
dépendances exécutables et paramètres de sécurité requis par son profil.
Le périmètre inclut le collecteur, ses politiques et les mécanismes qui
protègent les mesures et l'identification du PA. Les éléments embarqués
ou chargés dynamiquement par la distribution Python/C sont inventoriés ;
un binaire principal seul ne couvre pas automatiquement ces dépendances.
Ce choix fixe le périmètre des mesures ; sa couverture, ses mises à jour
et son coût restent à qualifier.

Une chaîne de mesure qualifiée collecte les éléments
avant leur utilisation ou selon un mécanisme dont la couverture est établie.
Le vérificateur confronte les journaux de mesures aux preuves TPM et aux
références approuvées ; tronquage, ordre incohérent, élément requis absent,
substitution ou contradiction provoquent le refus. Un hash déclaré par PA,
une signature de paquet ou une mesure d'image ne prouvent pas seuls ce qui
est chargé et exécuté. Les contrôles distinguent mesure, enforcement local,
attestation et identité du service appelant ; une preuve de fichiers ne
prouve pas l'intégrité continue de la mémoire du processus.

Pour Linux, démarrage mesuré et IMA sont des mécanismes candidats à
qualifier, selon noyau, politique, journaux, dépendances et format de
packaging. Pour Windows, Measured Boot et les protections d'intégrité du
code sont des éléments candidats : l'attestation du démarrage ne couvre
pas automatiquement le binaire PA ni ses chargements. Le mécanisme liant
ces éléments au PA exécuté doit être démontré ; un profil incapable de
produire les preuves requises reste non admissible. Aucun service cloud
Microsoft, TPM logiciel ou nouveau composant tiers n'est adopté ici.

En VM, mesures de l'invité et provenance du TPM restent distinctes de
celles de l'hyperviseur. En Docker/LXC, la chaîne de l'hôte doit rattacher
les mesures à l'instance PA, à ses couches et dépendances effectivement
utilisées ; contenu de l'image, couches modifiables, volumes exécutables
et chargements externes sont traités selon le profil. Une mesure globale
partagée ne prouve pas seule l'identité de chaque conteneur. Le partage de
la racine de confiance ne fusionne ni les identités ni leurs permissions.

Chaque profil décrit actifs, dépendances de confiance, moments de mesure,
références admises, exclusions justifiées et limites. Seules les données
non sensibles nécessaires sont transmises : contenu des secrets, données
métier et fichiers privés ne sont ni mesurés pour publication ni inclus
dans les journaux remis au vérificateur. Les paramètres sensibles utilisent
des références et une méthode de preuve à spécifier, sans hash public de
secret. Les journaux techniques restent bornés et protégés.

Les références sont issues d'artefacts approuvés et mises à jour dans un
mandat autorisé, avec provenance, version et période de transition explicites.
Observer une nouvelle valeur ne l'approuve pas. Installation, patch, retour
à une version ancienne et restauration doivent rester compatibles avec la
politique courante, sans réintroduire des références révoquées. Un changement
pertinent invalide le résultat dépendant et déclenche A10c ; les composants
non couverts et les limites face à l'administrateur hôte sont déclarés.

La qualification vérifie altération du PA et d'une dépendance, collecteur
ou politique remplacé, journaux incomplets, chargements externes, conteneur
substitué, mise à jour autorisée ou non, clone, restauration, saturation et
latence sur toutes les plateformes. Elle ne modifie pas implicitement
les noyaux, politiques Windows, configurations Proxmox, montages ou droits.
Les adapters exacts, profils de référence et budgets restent à spécifier.

[La documentation IMA Linux](https://docs.kernel.org/security/IMA-templates.html)
décrit les événements de mesure ;
[Microsoft Measured Boot](https://learn.microsoft.com/en-us/windows/security/operating-system-security/system-security/secure-the-windows-10-boot-process)
traite l'attestation du démarrage ;
[RFC 9684](https://www.rfc-editor.org/rfc/rfc9684.html#appendix-A) décrit le
rôle des journaux IMA en attestation. Ces références n'adoptent ni YANG,
NETCONF, ni un service externe pour PZT.
A10e, option A, est validé ; mécanismes, profils et budgets restent à qualifier.

##### Application au PA — A10e

Le choix définit la couverture des mesures, en conservant A10c/A10d,
les profils de confiance distincts et le blocage sans preuve requise.
Algorithmes, bibliothèques, banques PCR et fraîcheur restent à spécifier.

L'option A validée le 5 octobre 2026 utilise des profils ciblés et
versionnés : chaîne de
démarrage et composants nécessaires aux preuves, PA réellement chargé,
runtime, dépendances exécutables et paramètres de sécurité requis.
Collecteur, politiques et protection des mesures sont inclus. Packaging
Python/C, éléments embarqués et chargements dynamiques sont inventoriés ;
le binaire principal ne couvre pas automatiquement ses dépendances.
Couverture, mises à jour et ressources restent à qualifier.

Chaîne de mesure qualifiée et confrontation des
journaux aux preuves TPM et références approuvées sont requises. Élément
manquant, journal tronqué ou incohérent et substitution imposent le refus.
Déclaration de hash, signature de paquet ou mesure d'image seule ne prouve
pas le PA exécuté ; intégrité continue de sa mémoire et identité de service
ne découlent pas d'une mesure de fichiers.

Linux : démarrage mesuré et IMA candidats à qualifier par noyau/politique.
Windows : Measured Boot et protections du code candidats, avec démonstration
supplémentaire de la liaison au PA et aux dépendances réellement chargés.
Un profil sans preuve suffisante reste non admissible ; aucun service cloud
Microsoft ou composant tiers n'est adopté. En VM, mesures invité et provenance
TPM/hyperviseur sont distinguées. En Docker/LXC, l'hôte lie la mesure à
l'instance PA, ses couches, volumes exécutables et chargements externes ;
une mesure partagée ne fusionne pas les identités.

Le profil déclare actifs, dépendances de confiance, moments de mesure,
exclusions et limites. Journaux transmis bornés et protégés, sans contenu
ni hash public de secret, donnée métier ou fichier privé ; preuves des
paramètres sensibles à spécifier. Références approuvées avec provenance,
version et transition autorisée ; une valeur observée ne s'approuve pas
seule. Mises à jour, rollback et restauration ne réactivent aucune référence
révoquée. Changement pertinent : résultat invalidé et réattestation A10c.

Qualification : altérations PA/dépendances/collecteur/politiques, journaux
incomplets, substitution de conteneur, chargements externes, mises à jour,
clones, restauration, saturation et ressources sur toutes les cibles.
Adapters, profils et budgets restent à définir ; aucun noyau, droit,
montage, politique Windows ou configuration Proxmox n'est modifié.
Les sources figurent dans le cadrage PZT. A10e, option A, est validé ; mécanismes, profils et budgets restent à qualifier.

#### Scenario: Conformité du traitement A10e

- **WHEN** un profil revendique le traitement A10e et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--83645fffdb

Source : `openspec/specs/pzt/spec.md`, ligne 3034. SHA-256 du bloc : `5e5f301a0d7db3503b10d7647f3db80a78e0b9cafff277e0b35bad2fba5a77b2`.

~~~~text
### Requirement: Contrat A10f — Gestion des références d'intégrité — option A validée le 5 octobre 2026

Le rôle chargé du traitement A10f MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10f

Ce choix précise l'activation et le retrait des références approuvées A10e,
pour les mises à jour du PA et des composants de confiance de chaque profil.
Les références sont distribuées dans des manifestes
signés et versionnés, émis par une autorité explicitement habilitée. Mesure
observée, signature du fournisseur ou succès d'installation ne valent pas
approbation automatique dans un périmètre Pixs.

L'option A validée le 5 octobre 2026 autorise une transition progressive
bornée. Avant mise
à jour, le manifeste déclare les ensembles cohérents de mesures de la
version actuelle et de la cible approuvée, leurs destinataires et périodes
d'acceptation. Pendant le chevauchement autorisé, chaque PA doit correspondre
à un ensemble admis complet ; il ne compose pas des valeurs isolées de
versions différentes. À l'échéance, l'ancienne référence est retirée, même
si certains PA ne sont pas à jour. Ce choix permet une mise à jour
progressive des machines physiques, VM et conteneurs ; la durée et
le nombre d'ensembles admis restent à fixer par profil.

Chaque manifeste identifie émetteur, usage, périmètre, profil, plateformes,
artefacts et provenance, ensembles de références compatibles, version de
politique, validité, activation et retrait. Le vérificateur contrôle la
signature selon des ancrages et rôles configurés, la compatibilité et la
cohérence de l'ensemble. Une signature de liaison WireGuard ou une identité
PA n'accorde aucun droit de publier des références. Format de signature,
algorithmes, rotation des signataires et schémas restent à spécifier ; A10b
ne choisit pas implicitement le format de ces manifestes.

Préparation, approbation et activation sont distinctes de l'installation.
La distribution du manifeste ne commande aucun changement de machine.
PBO suit référence souhaitée, état appliqué du vérificateur, version du PA,
preuve courante et écarts via les contrats publics A07. Une installation
relevant d'un mandat PA garde ses permissions et obligations ; nouvelle
preuve A10c requise avant réadmission si les mesures changent. Un manifeste
préparé ou simplement reçu ne vaut pas activation confirmée.

L'ordre des versions de politique protège contre le rejeu d'un ancien
manifeste ; même version avec contenu contradictoire est refusée. Retour
à un ancien binaire reste possible seulement s'il est encore explicitement
admis par la politique courante et dans un mandat autorisé, sans retour à
une ancienne politique. Révocation connue d'un artefact, d'une référence,
d'un signataire ou d'une confiance interdit les accès dépendants, même
pendant une transition. Renouvellement de manifeste ou preuve TPM ne
prolonge aucune permission A05.

Cache et fonctionnement hors ligne restent bornés par validité, fraîcheur
et obligations du profil. Une échéance dépassée ou une politique requise
invérifiable bloque les accès concernés ; une panne ne prolonge pas la
transition. Restauration impose réconciliation des versions et retraits
avec l'autorité compétente avant admission, sans se fier au seul compteur
local restauré. L'autorité de publication et la coordination multimaître
suivent A12a–A12g validés ; modalités de réalisation à qualifier, sans nouveau
stockage autoritatif ou consensus implicite.

La qualification couvre mise à jour progressive, expiration de transition,
révocation urgente, installation échouée, ensemble de mesures mélangé,
rejeu, signature/émetteur invalide, propagation partielle, partition et
restauration sur Linux/Windows physiques et VM, Docker/LXC Proxmox.
Journaux sans secret, charge, tailles et nombre de références sont vérifiés.
Aucune bibliothèque, service de distribution externe ou opération hôte
n'est adopté ; valeurs et procédures restent à qualifier.

[Les valeurs de référence RATS, RFC 9334](https://www.rfc-editor.org/rfc/rfc9334.html#section-8.3),
servent à évaluer les preuves. [La spécification TUF](https://theupdateframework.github.io/specification/latest/)
documente les contrôles de signature, version et expiration contre rejeu
et gel des métadonnées ; elle sert de référence sans adopter TUF ou son
protocole pour PZT. A10f, option A, est validé ; schémas, signatures, durées et qualification restent à préciser.

##### Application au PA — A10f

Les références A10e sont distribuées par manifestes signés et versionnés
d'une autorité explicitement habilitée. Mesure observée, signature fournisseur
ou installation réussie ne vaut pas approbation Pixs.

L'option A validée le 5 octobre 2026 permet une transition progressive
bornée : ensembles
cohérents de mesures actuelle/cible approuvés, destinataires et périodes
d'acceptation déclarés avant mise à jour. Chaque PA correspond à un ensemble
complet, sans mélange de versions. Ancienne référence retirée à l'échéance,
même pour un PA non mis à jour. La transition couvre les déploiements
physiques, VM et conteneurs ; durée et nombre de références restent à fixer.

Manifeste : émetteur, usage, périmètre/profil, plateformes, artefacts et
provenance, ensembles compatibles, politique/version et dates d'activation,
validité et retrait. Signatures, ancrages, rôle du signataire et cohérence
sont contrôlés ; identité PA et liaison WireGuard ne donnent aucun droit
de publication. Schémas, format de signature, algorithmes et rotation restent
à spécifier, sans réutilisation implicite du format A10b.

Préparation, approbation, activation et installation sont distinguées.
Distribuer un manifeste ne commande pas une installation. PBO suit les
états souhaité/appliqué du vérificateur, version PA, preuve et écarts via
A07 ; mandat d'installation et permissions restent requis. Changement de
mesures exige une preuve A10c avant réadmission ; réception ne vaut pas
activation confirmée.

Ancienne politique rejouée ou même version contradictoire refusée. Retour
à un ancien binaire seulement s'il reste admis par la politique courante
et un mandat autorisé ; aucun retour à une ancienne politique. Révocation
connue d'artefact, référence, signataire ou confiance interdit les accès
dépendants, même pendant la transition. Aucun renouvellement de manifeste
ou de preuve ne prolonge les permissions A05.

Cache/hors ligne bornés par validité, fraîcheur et obligations du profil ;
échéance ou preuve de politique requise invérifiable bloque les accès.
Panne ne prolonge pas la transition. Restauration : réconciliation des
versions/retraits auprès de l'autorité avant admission, sans confiance au
seul compteur restauré. Publication et coordination suivent A12a–A12g
validés ; leurs modalités de réalisation restent à qualifier.

Qualification de toutes les cibles : transition, échéance, révocation,
installation échouée, mesures mélangées, rejeu, signature invalide, propagation
partielle, partition, restauration et ressources. Aucun service externe,
bibliothèque ou changement hôte n'est adopté. Les sources figurent dans le
cadrage PZT. A10f, option A, est validé ; schémas, signatures, durées et qualification restent à préciser.

#### Scenario: Conformité du traitement A10f

- **WHEN** un profil revendique le traitement A10f et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

