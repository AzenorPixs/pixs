# Références normatives — Z11

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 3927 | [Contrat A10i — Renouvellement anticipé des certificats TLS sous mandat — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3927) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4016 | [Contrat A10i2 — Nouvelle paire de clés TLS à chaque renouvellement — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4016) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4097 | [Contrat A10i3 — Transition TLS par chevauchement borné — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4097) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4175 | [Contrat A10i4 — Durées TLS initiales — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4175) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4257 | [Contrat A10i5 — Clé d'authentification TLS ECDSA P-256 — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4257) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--75c102770d

Source : `openspec/specs/pzt/spec.md`, ligne 3927. SHA-256 du bloc : `dba9d8d6866d1537a1564f963d76a9f22ecac0bdb44ebe24e131b73148abf588`.

~~~~text
### Requirement: Contrat A10i — Renouvellement anticipé des certificats TLS sous mandat — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i

Le choix concerne les certificats d'identité PZT/TLS A10b des PA et services,
pas les racines/intermédiaires de confiance, clés WireGuard, clés TPM ou
signatures opérationnelles A12e. Il arbitre l'autorisation du renouvellement,
sans fixer durée de certificat, fenêtre d'anticipation, algorithme de clé,
rotation/réutilisation de clé, protocole d'émission ou bibliothèque.

Option A validée : renouvellement anticipé automatisable sous politique et mandat
préalables explicites depuis PBO, couvrant identités/périmètre/usages/durées
et limites. PZT/PA soumettent la demande par contrats publics ; l'autorité
compétente vérifie les contrôles courants à chaque émission. La possession
d'un certificat encore valide ou une tentative reçue ne vaut pas mandat de
renouvellement. En dehors du mandat, émission bloquée jusqu'à décision autorisée.

Garanties du renouvellement : Django demeure l'autorité de décision, engagement/version/audit A07/A12.
Identité stable, rattachement, usages et contexte autorisés vérifiés ; preuve
de possession de la clé associée, profil/chaîne/ancrages, révocation et
attestation courante selon A10c requis. Une CSR ou un certificat n'accorde
aucune permission. Nouveau certificat, chaîne et correspondance de clé
vérifiés avant installation/activation ; réception/émission sans application
présumée. Liaison JWS au credential A10b mise à jour sous autorisation si
nécessaire, sans rotation WireGuard ou réémission de droits implicites.
Nouvelle association TLS avec preuve fraîche A10c ; aucun ticket ancien ne
contourne le changement, retrait ou contrôle courant.

Échec, PA hors ligne ou autorité indisponible : ancien certificat utilisable
seulement tant que tous ses contrôles et droits restent valides. Expiration
ou révocation connue retire les accès dépendants selon A05, sans délai de
grâce, certificat expiré accepté ou émission locale autonome. Reprise après
expiration par procédure autorisée avec preuves actuelles ; amorçage A02 reste
limité à son rôle technique, sans contrôle métier contourné. Restauration ou
renouvellement ne réactivent aucune ancienne habilitation. PBO expose échéance,
demande, émission, installation vérifiée et échec, sans secret.

La [RFC 5280, section 4.1.2.5](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1.2.5)
définit l'intervalle X.509 `notBefore`/`notAfter` ; la politique d'automatisation
validée ici est un choix Pixs. A10i A est validé le 6 octobre 2026 ; cycle
de vie des clés validé en A10i2. Providers, horloges, charge d'émission/attestation
et continuité à
qualifier sur toutes les cibles, sans gain ou disponibilité promis.
Recette : renouvellement dans/hors mandat, preuve/CSR incorrectes, refus de
permission, révocation/expiration, PA hors ligne, autorité indisponible,
certificat reçu non installé, liaison JWS, ticket/reconnexion et restauration.

##### Application au PA — A10i

Certificats d'identité PZT/TLS PA/services A10b ; racines/intermédiaires,
WireGuard/TPM/signatures A12e exclus. Durée/fenêtre d'anticipation/algorithme,
rotation ou réutilisation de clé/protocole/provider restent à arbitrer.
Option A validée : renouvellement anticipé automatisable sous politique/mandat PBO
préalables explicites (identités/périmètre/usages/durées/limites). Demande par
contrats publics et contrôles courants par autorité compétente à chaque émission ;
certificat valide/réception de demande sans mandat implicite, hors mandat bloqué.
Garanties du renouvellement : Django, engagement/version/audit A07/A12 ; identité/rattachement/usages/
contexte, possession de clé, profil/chaîne/ancrages, révocation et attestation
courante A10c vérifiés. CSR/certificat sans droit implicite. Nouveau certificat/
chaîne/clé vérifiés avant installation/activation, réception/émission sans
application présumée. Liaison JWS au credential A10b actualisée sous autorisation
si requis, sans rotation WireGuard ou droits renouvelés implicites. Association
TLS avec preuve fraîche A10c, tickets sans changement/retrait contournés.

Échec/hors ligne/autorité indisponible : ancien certificat sous contrôles/droits
encore valides seulement ; expiration/révocation connues retirent accès A05,
sans grâce, certificat expiré accepté ou émission autonome PA. Reprise après
expiration autorisée avec preuves actuelles, A02 limité à l'amorçage technique ;
renouvellement/restauration sans habilitation retirée réactivée. PBO expose
échéance/demande/émission/installation vérifiée/échec sans secret.
RFC 5280 et distinction politique Pixs dans cadrage PZT. A10i A validé le
6 octobre 2026 ; cycle de vie des clés A10i2 validé. Qualification providers/
horloges/charge/continuité par cible, aucun gain ou disponibilité promis.
Recette : mandat, preuve/CSR, permissions, révocation/expiration/hors ligne,
autorité indisponible, réception sans installation, liaison, ticket/reconnexion
et restauration.

#### Scenario: Conformité du traitement A10i

- **WHEN** un profil revendique le traitement A10i et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--45b43e3af7

Source : `openspec/specs/pzt/spec.md`, ligne 4016. SHA-256 du bloc : `fc6f6169aba11b20afc1d49414f04409aedba9aecb55bb1e3f2354a5a3f8682a`.

~~~~text
### Requirement: Contrat A10i2 — Nouvelle paire de clés TLS à chaque renouvellement — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i2 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i2

Ce choix porte sur la paire de clés d'authentification associée au certificat
PZT/TLS A10b/A10i, pas les clés de trafic TLS, clés WireGuard, TPM, autorités
CA ou signatures opérationnelles A12e. Identité stable et permissions demeurent
distinctes du credential ; algorithme de clé et durée numérique restent ouverts.

Option A validée : nouvelle paire de clés indépendante à chaque renouvellement
normal du certificat. Génération dans le périmètre du PA/service concerné
par un provider qualifié, avec aléa cryptographique et protection conformes
au profil autorisé. Seuls clé publique, demande et preuves nécessaires passent
par les contrats publics ; aucune clé privée TLS transmise au PBO. Clé nouvelle
sans dérivation depuis l'ancienne ; identité stable conservée après contrôles.

Garanties de gestion des clés : mandat A10i couvrant la gestion de clé, preuve de possession et
correspondance certificat/clé vérifiées avant activation, engagements/audit
A07/A12 et liaison JWS A10b actualisée si nécessaire. Changement de clé sans
nouveau droit, réadmission implicite, rotation WireGuard ou fallback de provider.
Provider incapable de satisfaire la politique : activation refusée, pas de
réutilisation de clé en secours de A ni d'export matériel implicite. Compromission
connue, perte ou clé non vérifiable : accès dépendants retirés A05 et procédure
autorisée avec preuves actuelles ; un simple renouvellement ne réhabilite pas
un hôte compromis. Clone/restauration sans anciennes habilitations réactivées.
Retrait de l'ancien credential, transition, protection et destruction de clé
à qualifier par provider/cible ; conservation des références publiques d'audit
sans autoriser un nouvel usage de la clé privée retirée. Réémission idempotente
après réponse perdue ne vaut pas nouveau renouvellement ni génération répétée
aveugle ; résultat courant réconcilié avant activation.

[NIST SP 800-57 partie 1 révision 5, sections 5.3 et 8.2.3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
distingue période d'usage et remplacement par une clé indépendante ; il ne
prescrit pas ici le choix Pixs d'une clé à chaque certificat. A10i2 A est
validé le 6 octobre 2026 ; transition entre credentials validée en A10i3.
CPU/RAM, stockage, aléa,
opérations matérielles, émission et reconnexion à qualifier sur Linux/Windows
physiques/VM, Docker/LXC Proxmox ; aucune supériorité globale ou coût chiffré
promis. Recette : clé indépendante/correspondance, identité stable, absence
de réutilisation à un nouveau renouvellement, provider indisponible, mandat refusé, perte/compromission, réémission
idempotente, transition/restauration/clone et absence de secret dans diagnostics.

##### Application au PA — A10i2

Paire d'authentification du certificat PZT/TLS A10b/A10i ; clés de trafic TLS,
WireGuard/TPM/CA/signatures A12e exclues. Identité stable/droits distincts,
algorithme et durée numériques non retenus.
Option A validée : paire nouvelle indépendante à chaque renouvellement normal,
générée dans périmètre PA/service via provider qualifié, aléa/protection du
profil autorisé. Contrats publics pour clé publique/demande/preuves seulement,
aucune clé privée TLS au PBO ni dérivation depuis l'ancienne ; identité stable
sous contrôles. Garanties de gestion des clés : mandat de gestion de clé A10i, possession/correspondance avant activation,
engagement/audit A07/A12, liaison A10b actualisée si requise ; aucun droit ou
rotation WireGuard implicites. Provider incapable : refus, sans clé réutilisée
en secours de A, export matériel ou fallback implicites. Compromission connue/
perte/clé non vérifiable : retrait A05 et reprise autorisée avec preuves actuelles,
pas d'hôte compromis réhabilité par renouvellement. Clone/restauration sans
habilitations anciennes ; retrait credential/transition/protection/destruction
à qualifier par provider/cible, références publiques d'audit sans nouvel usage
de clé privée retirée. Réémission idempotente après réponse perdue réconciliée,
sans renouvellement neuf ou génération répétée aveugle.
NIST SP 800-57 et distinction de choix Pixs dans cadrage PZT. A10i2 A validé le
6 octobre 2026 ; transition entre credentials A10i3 validée. Coûts
CPU/RAM/stockage/aléa/matériel/émission/
reconnexion à qualifier par cible, aucune supériorité globale promise.
Recette : indépendance/correspondance, identité stable, absence de réutilisation, provider/
mandat refusés, perte/compromission, idempotence, transition/restauration/clone
et diagnostics sans secret.

#### Scenario: Conformité du traitement A10i2

- **WHEN** un profil revendique le traitement A10i2 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c3e75025c7

Source : `openspec/specs/pzt/spec.md`, ligne 4097. SHA-256 du bloc : `38c4acde468c53671e547fd05ebd45957bf8b96a9e124d125d5391d57547b0e5`.

~~~~text
### Requirement: Contrat A10i3 — Transition TLS par chevauchement borné — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i3 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i3

Option A validée : chevauchement borné des credentials lors d'un renouvellement
normal A10i/A10i2. PBO autorise explicitement ancien et nouveau certificats
pour la même identité, les mêmes usages et le même périmètre, avec début et
fin de transition configurés/versionnés avant activation. Nouveau certificat
et paire de clés vérifiés, puis nouvelle association TLS avec attestation
fraîche A10c et contrôles courants. Preuve d'application requise avant retrait
planifié de l'ancien credential ; à la fin de fenêtre, ancien retiré même
si tous les PA n'ont pas convergé, sans maintien illimité pour disponibilité.
PBO distingue émis, installé, accepté, utilisé et retiré ; aucun ACK ne prouve
à lui seul la nouvelle association authentifiée.

Garanties de transition : mandat A10i, identité stable et liaison A10b cohérentes, engagements
A07/A12 et permissions A05. Références distinctes des deux certificats/clés,
sans nouveau droit, double exécution métier, écoute ou ancrage implicites.
Le chevauchement de credentials ne modifie pas l'unique suite effective A10h.
Validité X.509 et validités requises bornent l'usage de chaque credential ;
fenêtre sans prolongation de certificat, mandat, permission ou attestation.
Expiration, révocation ou compromission connue rendent l'ancien inadmissible
immédiatement selon A05 ; aucun chevauchement de secours pour ce credential.
Sans nouvelle association TLS vérifiable, accès protégé refusé. Retrait de l'ancien
avec accès/sessions/tickets dépendants invalidés, fermeture/reconnexion contrôlées
et nouvelle preuve A10c ; restauration sans credential retiré réactivé.
Résultat d'engagement incertain réconcilié, aucun retour automatique à l'ancien.

Fenêtre finie, charge et stockage de deux clés protégées, qualification des
providers, propagation, pertes de contrôle et horloges à préciser sur toutes
les cibles. Le mandat doit permettre le retrait à échéance même si l'ancien
canal est perdu, sans autorité locale supplémentaire. La
[RFC 5280, section 4.1.2.5](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1.2.5)
définit la validité des certificats ; le chevauchement est un choix Pixs
validé, sans continuité garantie. A10i3 A est validé le 6 octobre 2026 ; valeurs
initiales de validité, anticipation et fenêtre validées en A10i4.
Recette : transition normale, preuves manquantes, non-convergence à échéance,
ancien expiré/révoqué/compromis, ticket, liaison, provider sans capacité pour
deux clés, commit incertain, perte du contrôle et restauration.

##### Application au PA — A10i3

Option A validée : renouvellement normal A10i/A10i2 avec chevauchement borné des
credentials, explicitement autorisé/versionné par PBO (même identité/usages/
périmètre, début/fin configurés). Nouveau certificat/clé vérifiés, association
TLS avec attestation fraîche A10c et contrôles courants, preuve d'application
avant retrait planifié ; ancien retiré à la fin même si PA non convergés.
PBO distingue émis/installé/accepté/utilisé/retiré ; ACK sans association prouvée.
Garanties de transition : mandat A10i, identité/liaison A10b, engagements A07/A12, droits A05.
Références distinctes des certificats/clés sans droit, double opération,
écoute ou ancrage implicites ; une suite effective A10h inchangée. Validité
X.509 et autres validités bornent chaque usage, fenêtre sans prolongation.
Expiration/révocation/compromission connues rendent ancien inadmissible A05,
sans chevauchement de secours ; nouvelle association TLS non vérifiable bloquante.
Retrait avec accès/sessions/tickets dépendants invalidés, fermeture/reconnexion
contrôlées et preuve fraîche A10c. Restauration/commit incertain sans ancien
credential réactivé ni retour automatique, réconciliation obligatoire.
Fenêtre, deux clés protégées/charge, providers/propagation/horloges/perte de
contrôle à qualifier par cible ; retrait à échéance sous mandat même sans
ancien canal, aucune autorité locale supplémentaire. RFC 5280 dans cadrage PZT ;
chevauchement validé Pixs sans continuité garantie. A10i3 A validé le
6 octobre 2026 ; valeurs initiales de validité/anticipation/fenêtre A10i4
validées. Recette : normal,
preuve/non-convergence, ancien expiré/révoqué/compromis, ticket/liaison, provider
sans capacité deux clés, commit incertain, perte contrôle/restauration.

#### Scenario: Conformité du traitement A10i3

- **WHEN** un profil revendique le traitement A10i3 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--863cc1c210

Source : `openspec/specs/pzt/spec.md`, ligne 4175. SHA-256 du bloc : `62718d1e91f063e75487e218aaf0174313e38b679525bbd0ae70c228d48a483d`.

~~~~text
### Requirement: Contrat A10i4 — Durées TLS initiales — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i4 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i4

Premier jet validé pour certificats d'identité PZT/TLS PA/services A10i–A10i3,
pas les racines/intermédiaires CA. Valeurs nominales initiales configurables
et versionnées depuis PBO sous permission et mandat ; qualification requise,
sans mesure de disponibilité ou performance démontrée.

| Paramètre | Valeur initiale validée |
|---|---|
| Validité nominale du certificat | 24 heures |
| Début prévu du renouvellement | Après 16 heures |
| Chevauchement maximal de credentials | 5 minutes |

Renouvellement aux deux tiers de la durée effective depuis `notBefore`, sous
mandat A10i ; les 16 heures supposent la validité nominale entière de 24 heures.
Calcul depuis les dates autorisées/vérifiées, pas un compteur remis à zéro par
connexion ou restauration. Validité effective bornée par la politique,
l'identité et la chaîne de confiance requises ; si elle est raccourcie,
seuil recalculé avant expiration. Paramètres incohérents ou marge insuffisante
selon qualification bloquent l'activation du profil, sans validité allongée.

La fenêtre de 5 minutes est un plafond depuis le début de transition engagé
et versionné A10i3. Aucun certificat hors validité, révoqué ou compromis
utilisable, aucun mandat/permission/attestation prolongé. Retrait planifié
dès preuve de transition suffisante, au plus tard à l'échéance ; PA non
convergé sans ancienne validité prolongée. Nouvelle clé A10i2 à chaque
renouvellement normal ; génération, demande et réponse idempotentes distinguées.
Horloges, anticipation, dispersion et charge à qualifier sur Linux/Windows
physiques/VM et Docker/LXC Proxmox. PA hors ligne après expiration sans grâce :
reprise autorisée A10i et contrôles courants A02/A05.

A10i4 A est validé le 6 octobre 2026 comme premier jet, avec marge nominale
d'anticipation de 8 heures. Aucun gain CPU/RAM/disponibilité déduit de la seule
cadence. Valeurs Pixs, pas des durées prescrites par la RFC 5280 ou le
[NIST SP 800-57](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final).
Algorithme de clé de certificat validé en A10i5. Recette : dates nominales/
raccourcies, seuil, configuration invalide, renouvellement refusé/manqué,
chevauchement plafonné, horloge/restauration, retrait, PA hors ligne et coût réel.

##### Application au PA — A10i4

Premier jet validé configurable/versionné depuis PBO sous permission/mandat
pour certificats PA/services A10i–A10i3, CA exclues ; qualification requise.

| Paramètre | Valeur initiale validée |
|---|---|
| Validité nominale du certificat | 24 heures |
| Début prévu du renouvellement | Après 16 heures |
| Chevauchement maximal de credentials | 5 minutes |

Renouvellement aux deux tiers de durée effective depuis `notBefore`, mandat
A10i ; 16 heures si durée nominale entière de 24 heures. Dates autorisées/
vérifiées sans remise à zéro connexion/restauration ; durée bornée par
politique/identité/chaîne, raccourcissement avec seuil recalculé avant expiration.
Paramètres incohérents/marge insuffisante selon qualification bloquants,
aucune validité allongée. Fenêtre 5 minutes au plus depuis début de transition
engagé/versionné A10i3 ; jamais certificat invalide/révoqué/compromis ou
mandat/permission/attestation prolongés. Retrait dès preuve suffisante,
au plus tard à échéance, PA non convergé sans maintien de l'ancien.
Nouvelle clé A10i2, émission/idempotence distinctes du renouvellement normal.
Horloges/anticipation/dispersion/charge à qualifier par cible ; hors ligne
après expiration sans grâce, reprise autorisée A10i et contrôles A02/A05.
A10i4 A validé le 6 octobre 2026 comme premier jet avec marge nominale 8 heures,
sans gain CPU/RAM/disponibilité inféré. Valeurs Pixs sans durée prescrite RFC/
NIST, sources cadrage PZT. Algorithme de clé A10i5 validé. Recette : dates/seuil/
raccourcissement, profil invalide, renouvellement refusé/manqué, plafond,
horloge/restauration, retrait, hors ligne et coût réel.

#### Scenario: Conformité du traitement A10i4

- **WHEN** un profil revendique le traitement A10i4 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--b363d83a3b

Source : `openspec/specs/pzt/spec.md`, ligne 4257. SHA-256 du bloc : `c3cd26e771ee922e5d28be860b2651aaa529be22bcdf28af8910b1604ee9a5f9`.

~~~~text
### Requirement: Contrat A10i5 — Clé d'authentification TLS ECDSA P-256 — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i5 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i5

Option A validée : paire ECDSA sur P-256 (`secp256r1`) pour la clé publique
du certificat terminal PZT/TLS PA/service et authentification TLS 1.3 avec
`ecdsa_secp256r1_sha256`, dans le périmètre A10b/A10g/A10i. Correspondance
clé/certificat/schéma TLS contrôlée ; format de signature conforme au protocole
TLS, sans substitution du format JWS opérationnel. Profil fixé sans fallback
Ed25519, RSA ou TLS 1.2 pour cette authentification. Capacités normativement
requises du provider sous-jacent conservées.

Ce choix ne fixe pas l'algorithme de signature des CA ou leurs clés, les
groupes d'échange TLS, les clés de trafic AES/ChaCha A10h, WireGuard/TPM ou
les signatures opérationnelles Ed25519 A12e. Clés distinctes par usage ;
un nom d'algorithme commun ne permet aucune réutilisation de clé.

Génération/protection qualifiées dans le périmètre PA/service A10i2, clé
privée non transmise à PBO, possession vérifiée, chaîne/ancrages/usages/identité
contrôlés. Nouvelle clé à chaque renouvellement, durées A10i4 et transition
A10i3 conservées. Provider ou extrémité incompatible : activation bloquée,
pas d'export matériel ou permission hôte implicites. Profil X.509, révocation,
provider logiciel/matériel et qualification Linux/Windows physiques/VM,
Docker/LXC Proxmox restent à préciser ; émission des certificats validée en A10i6.

La [RFC 8446, section 9.1](https://www.rfc-editor.org/rfc/rfc8446.html#section-9.1)
inclut `ecdsa_secp256r1_sha256` dans les signatures à prendre en charge.
Cette base d'interopérabilité ne prouve pas le support réel d'un provider ou
matériel, ni une supériorité universelle de sécurité/CPU/RAM. A10i5 A est
validé le 6 octobre 2026. Recette : clé/schéma/certificat compatibles, deux
extrémités, signature réelle, nonce/aléa/provider qualifiés, renouvellement/
transition, refus de fallback et clés opérationnelles distinctes.

##### Application au PA — A10i5

Option A validée : paire ECDSA P-256 (`secp256r1`) du certificat terminal
PA/service, authentification TLS 1.3 `ecdsa_secp256r1_sha256` A10b/A10g/A10i.
Correspondance clé/certificat/schéma vérifiée, signature au format TLS sans
format JWS substitué. Profil sans fallback Ed25519/RSA/TLS 1.2 pour cette
authentification ; capacités normativement requises du provider conservées.
Signature/clés CA, groupes d'échange, clés de trafic AES/ChaCha A10h,
WireGuard/TPM et signatures opérationnelles Ed25519 A12e distincts. Clés
séparées par usage, même si algorithme commun.

Génération/protection A10i2 qualifiées, clé privée locale non transmise à PBO,
possession/chaîne/ancrages/usages/identité vérifiés ; nouvelle clé à chaque
renouvellement, durées A10i4 et transition A10i3 conservées. Incompatibilité
provider/extrémité bloquante, aucun export matériel/privilège hôte implicites.
Profil X.509/révocation/provider logiciel ou matériel à qualifier sur Linux/
Windows physiques/VM, Docker/LXC Proxmox ; émission validée en A10i6.
A10i5 A validé le 6 octobre 2026 : base d'interopérabilité TLS 1.3 selon RFC
8446 section 9.1 (source cadrage PZT), support réel à vérifier sans classement
universel sécurité/coût/CPU/RAM. Recette : correspondance, extrémités, signature,
nonce/aléa/provider, renouvellement/transition, refus fallback et clés
opérationnelles distinctes.

#### Scenario: Conformité du traitement A10i5

- **WHEN** un profil revendique le traitement A10i5 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

