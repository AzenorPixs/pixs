# Références normatives — Z12

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 120 | [Identités de service, PKI et attestation](../../specs/pzt/spec.md#L120) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4325 | [Contrat A10i6 — PKI privée dédiée à PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4325) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4415 | [Contrat A10i7 — Émetteur CA dédié par autorité logique habilitée — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4415) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4495 | [Contrat A10i8 — Profils explicites de protection des clés CA intermédiaires — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4495) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4585 | [Contrat A10i9 — Nouvelle clé CA et recertification après perte — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4585) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4680 | [Contrat A10i10 — Secours CA indépendant pré-certifié — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4680) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4772 | [Contrat A10i11 — Bascule CA automatisable sous mandat préalable — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4772) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4858 | [Contrat A10i12 — Exclusion active et vérifiée du signataire CA — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L4858) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 4943 | [Contrat A10i13 — Mécanismes d'exclusion adaptés au profil CA — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L4943) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5039 | [Contrat A10i14 — Clés CA ECDSA P-256 et signatures SHA-256 — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5039) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5117 | [Contrat A10i15 — Nouvelle paire à chaque renouvellement normal des CA intermédiaires — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5117) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5213 | [Contrat A10i16 — Durées et anticipation des CA intermédiaires — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5213) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5334 | [Contrat A10i17 — Durée et anticipation de la racine hors ligne — choix du développeur validé le 7 octobre 2026](../../specs/pzt/spec.md#L5334) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5455 | [Contrat A10i18 — Nouvelle paire indépendante à chaque succession racine — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5455) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5561 | [Contrat A10i19 — Coexistence bornée des ancrages racine sur les PA — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5561) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5657 | [Contrat A10i20 — Plafond de coexistence des ancrages racine — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5657) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

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

### Référence pzt--fefc801de8

Source : `openspec/specs/pzt/spec.md`, ligne 4325. SHA-256 du bloc : `d45cea874242f027f69f3c377904c548d859ed181d512195f8838daebcbe187d`.

~~~~text
### Requirement: Contrat A10i6 — PKI privée dédiée à PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i6 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i6

Option A validée : PKI privée dédiée à PZT, racine protégée hors ligne et
émission courante des certificats terminaux A10b/A10i–A10i5 par autorités
intermédiaires en ligne dédiées au périmètre autorisé. Ancrages explicitement
provisionnés A02 ; aucune confiance implicite depuis la découverte ou les
magasins publics de l'OS. Le PA ordinaire ne devient pas autorité d'émission.
Les autorités de certification et leurs clés restent distinctes des autorités
métier PZT et des signataires opérationnels A12c–A12g.

La clé privée racine reste hors des processus courants PBO/PZT/PA ; les clés
privées des intermédiaires restent dans leur service d'émission protégé, sans
exposition à l'administration PBO ou aux PA ordinaires. PBO pilote politiques
et demandes autorisées par contrats publics. Opérations racine exceptionnelles
sous procédure explicite ; racine non sollicitée à chaque renouvellement terminal.
Cycle de vie des CA, publication de leur état de révocation et remplacement
de racine restent à spécifier. Le rattachement des émetteurs aux périmètres
est validé en A10i7, sans nombre, placement ou topologie automatiquement adoptés.

Django conserve la décision courante A10i, engagement/audit A07/A12 et contrôles
de demande/possession/périmètre. Certificat signé sans décision admissible ne
vaut ni admission ni droit ; chaîne, ancrage, usages, identité, clé et dates
vérifiés avant activation. Signature CA sans preuve cryptographique d'engagement
PostgreSQL. Renouvellement, chevauchement, révocation connue et refus fermé
A05 conservés ; panne d'émetteur sans validité ou permission prolongée.
Aucun raccordement à une PKI d'organisation ou secours par une autre racine
retenu par cette validation. Aucun logiciel CA ou protocole d'émission
choisi ; algorithme de clé/signature CA validé séparément en A10i14. ECDSA
P-256 des terminaux A10i5 ne fixe pas les clés CA ; aucune brique NetBird
ou AD CS n'est adoptée.

A10i6 A est validé le 6 octobre 2026 pour une installation PZT autonome,
avec exploitation et protection des CA dédiées à prévoir. Charge d'émission,
validation et compatibilité à qualifier côté services et PA sur les cibles
Linux/Windows physiques/VM et Docker/LXC Proxmox, sans coût ou disponibilité
promis. La [RFC 5280, section 4.2.1.9](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.2.1.9)
définit les contraintes CA et [sa section 6.1](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.1)
la validation de chaîne. La séparation racine hors ligne/émetteur en ligne
est un choix Pixs, illustré par le [modèle PKI Microsoft](https://learn.microsoft.com/en-us/training/modules/certificate-services-root-issuing-authority/),
sans adoption de ce logiciel. Recette : chaîne/ancrage autorisés, CA ou demande
hors périmètre, émission refusée/incertaine, clés CA inaccessibles au PA ordinaire,
indisponibilité, révocation et reprise sans droits réactivés.

##### Application au PA — A10i6

Option A validée : PKI privée dédiée PZT, racine protégée hors ligne et
intermédiaires d'émission en ligne dédiés au périmètre autorisé pour les
certificats terminaux A10b/A10i–A10i5. Ancrages A02 explicitement provisionnés,
sans confiance implicite par découverte ou magasins publics OS. Le PA ordinaire
ne devient pas CA ; CA/clés distinctes des autorités métier PZT et signataires
opérationnels A12c–A12g.

Clé racine hors processus courants PBO/PZT/PA, clés intermédiaires dans service
protégé sans exposition à l'administration PBO ou aux PA ordinaires. Pilotage
PBO par contrats publics, opérations racine exceptionnelles sous procédure
explicite, aucune signature racine à chaque renouvellement terminal. Cycle de
vie/révocation CA et remplacement racine à spécifier ; rattachement des émetteurs
validé en A10i7 sans nombre, placement ou topologie implicitement retenus.
Django conserve décision A10i, engagement/audit A07/A12 et contrôles de demande/
possession/périmètre. Certificat signé sans décision admissible sans admission/
droit ; chaîne/ancrage/usages/identité/clé/dates vérifiés avant activation.
Signature CA sans preuve cryptographique d'engagement PostgreSQL. A05 et
renouvellement/chevauchement/retrait conservés ; panne d'émetteur sans validité
ou permission prolongée. Clé privée terminale toujours locale A10i2.
Aucun raccordement PKI d'organisation ou autre racine de secours retenu ;
logiciel/protocole CA non choisis, algorithme CA validé séparément en A10i14 ;
clés CA non imposées par ECDSA P-256 terminal, aucun composant NetBird ou AD CS adopté.

A10i6 A validé le 6 octobre 2026 pour autonomie PZT, avec exploitation/protection
des CA dédiées. Charge service/PA et compatibilité Linux/Windows physiques/VM,
Docker/LXC Proxmox à qualifier sans coût ou disponibilité promis ; RFC 5280
et modèle racine hors ligne/émetteur en ligne référencés dans cadrage PZT. Recette :
ancrages/chaînes autorisés, CA/demande hors périmètre, refus/incertitude d'émission,
clés CA inaccessibles au PA ordinaire, indisponibilité/révocation/reprise sans
droits réactivés.

#### Scenario: Conformité du traitement A10i6

- **WHEN** un profil revendique le traitement A10i6 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--002cacafae

Source : `openspec/specs/pzt/spec.md`, ligne 4415. SHA-256 du bloc : `2f6ba44fade9403340c9cff5ff5d6397bfbe83f991f15277ff84fe8456a19609`.

~~~~text
### Requirement: Contrat A10i7 — Émetteur CA dédié par autorité logique habilitée — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i7 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i7

Option A validée : émetteur intermédiaire dédié par autorité logique PZT
habilitée à émettre dans un même domaine de confiance explicitement défini,
avec clé CA propre, référence/version et périmètre explicites. Création sous
mandat ; toutes les sous-autorités ne reçoivent pas un droit d'émettre. Plusieurs
membres de la même autorité logique ne créent pas une CA par membre. Protection
des clés validée en A10i8 ; placement, redondance et nombre de services restent
à arbitrer, sans copie privée ou partage multi-instance implicites.

CA et autorité logique métier PZT sont des objets distincts. Aucun domaine
indépendant rattaché implicitement à une racine commune ; frontières des domaines,
racines et topologie de certification à spécifier. La hiérarchie CA ne reproduit
pas automatiquement la hiérarchie métier PZT, ni chaque machine, VM, conteneur
ou membre multimaître. Émetteur mutualisé entre autorités logiques non retenu.

Chaque vérification associe identité attendue, rattachement courant, domaine
et émetteurs autorisés à une politique versionnée obtenue d'une source de
confiance ; ni certificat reçu ni nom d'issuer ne choisissent cette politique.
Une chaîne valide vers la même racine ne suffit pas : émetteur/clé/référence
et périmètre vérifiés, chemins alternatifs, certifications croisées ou délégations
CA non autorisées refusés. Contraintes X.509 et règles PZT qualifiées avec les
bibliothèques retenues ; aucun champ/extension d'identité précis adopté ici.
Django conserve les décisions d'émission A10i ; A02, A05, A10i–A10i6 et A12
restent applicables. Compromission/révocation connue retire les accès dépendants ;
restauration ou changement d'émetteur sans habilitation réactivée.

A10i7 A est validé le 6 octobre 2026 pour faciliter retrait ciblé et séparation
des clés par autorité logique. Ce cloisonnement dépend du contrôle effectif des
émetteurs admis ; une racine compromise affecte son domaine, sans indépendance
cryptographique des branches sous cette racine. Coût CPU/RAM, stockage, émission,
inventaire et exploitation à qualifier, sans multiplicateur de PA ou serveurs
imposé. La [RFC 5280, section 6.2](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.2)
permet des restrictions applicatives de chemin ; ce découpage est un choix Pixs.
Recette : émetteur correct ou frère interdit, nom falsifié, chemin alternatif,
autorité hors mandat, membres multiples, changement de rattachement, révocation
d'émetteur et restauration.

##### Application au PA — A10i7

Option A validée : intermédiaire dédié par autorité logique PZT habilitée à
émettre dans un même domaine explicitement défini ; clé CA propre, référence/
version/périmètre et création sous mandat. Sous-autorités sans droit d'émission
automatique ; membres multiples sans CA par membre. Protection des clés validée
en A10i8, placement/redondance/nombre de services à arbitrer sans copie privée
ou partage multi-instance implicites. Émetteur mutualisé non retenu.
CA et autorité logique métier distinctes, domaines indépendants sans racine
commune implicite. Frontières/racines/topologie à spécifier ; aucune hiérarchie
CA copiée des parents métier ni CA automatique par machine, VM ou conteneur.

Identité attendue/rattachement courant/domaine/émetteurs admis depuis politique
versionnée de confiance, jamais choisis par certificat reçu ou nom issuer.
Même racine sans acceptation implicite : émetteur/clé/référence/périmètre vérifiés ;
chemins alternatifs, certifications croisées ou délégations CA non autorisées
refusés. Contraintes X.509/règles PZT qualifiées par bibliothèque, aucun champ/
extension d'identité adopté. Django conserve émission A10i ; A02/A05/A10i–A10i6/
A12 conservés. Révocation/compromission connues retirant accès dépendants ;
restauration ou changement d'émetteur sans anciennes habilitations réactivées.
A10i7 A validé le 6 octobre 2026 pour retrait ciblé et clés séparées par autorité
logique, sous contrôle effectif des émetteurs admis ; racine compromise affectant
son domaine, branches sans indépendance cryptographique sous la même racine.
CPU/RAM/stockage/émission/inventaire/exploitation à qualifier sans nombre de PA/
serveurs imposé ; RFC 5280 section 6.2 référencée dans cadrage PZT. Recette : émetteur
correct/frère interdit, nom falsifié, chemin alternatif, hors mandat, membres
multiples, rattachement/révocation/restauration.

#### Scenario: Conformité du traitement A10i7

- **WHEN** un profil revendique le traitement A10i7 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--19d4898890

Source : `openspec/specs/pzt/spec.md`, ligne 4495. SHA-256 du bloc : `0f9923a70dee811ec618a29562ef94eefcf6bf6ca45ffac4b9472148ff567f90`.

~~~~text
### Requirement: Contrat A10i8 — Profils explicites de protection des clés CA intermédiaires — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i8 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i8

Option A validée pour les clés privées des émetteurs en ligne A10i6/A10i7 :
profil explicite approuvé par émetteur/périmètre, logiciel protégé lorsqu'autorisé
ou matériel non exportable lorsque la politique l'exige. Aucun profil déduit
de l'OS, de l'attestation TPM ou du seul placement en VM/conteneur. Protection
de la racine hors ligne, clés TLS terminales, WireGuard, TPM et signatures
opérationnelles A12f/A12g distinctes ; leurs politiques ne sont pas transposées
automatiquement aux CA. Aucun algorithme CA, provider, placement ou réplication
de clé fixé ; reprise après perte validée en A10i9, sans restauration de l’ancienne clé privée.

Profil logiciel : clé chiffrée au repos avec intégrité contrôlée, déverrouillage
protégé à qualifier, identité de service isolée et accès minimal. Secrets hors
sources, images, configuration métier et journaux ; références contrôlées
uniquement. Clé accessible au processus d'émission et exposée à sa compromission
ou à celle de son hôte ; aucune non-exportabilité matérielle revendiquée.

Profil matériel : provider qualifié et clé non exportable, dispositif local
ou service matériel par contrat autorisé à qualifier. Algorithme CA, génération,
accès, signature et protection effective vérifiés, sans équivalence présumée
entre HSM, TPM physique et vTPM. Politique matérielle non satisfaite : émission
bloquée sans repli logiciel, même si ce profil existe pour un autre périmètre.
Aucun matériel imposé aux PA ordinaires, qui ne détiennent pas de clé CA.

Clés CA propres aux émetteurs A10i7, clé privée non exposée à l'administration
PBO/PA ordinaire, opérations limitées à l'émission autorisée par Django et
A07/A12. Matériel non exportable sans garantie qu'un processus compromis habilité
ne puisse demander une émission abusive ; contrôles et révocation nécessaires.
Provider indisponible ou protection invérifiable : pas de nouvelle émission,
sans autre clé/provider implicite ou certificat prolongé. Compromission connue :
retrait A05 ; redémarrage, clone ou restauration sans droit réactivé. Docker/LXC
sans périphérique, montage, privilège ou permission Proxmox implicites ; service
externe par contrat PZT autorisé.

A10i8 A est validé le 6 octobre 2026 pour des profils qualifiés Linux/Windows
physiques/VM et Docker/LXC Proxmox. Le profil logiciel ne prétend pas offrir
une protection matérielle équivalente contre l'extraction. CPU/RAM, latence,
coûts et disponibilité à qualifier par provider, sans supériorité globale.
Le [NIST SP 800-57 partie 1, section 6.2.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite la protection des clés stockées ; profils retenus par Pixs, sans
certification FIPS ou conformité NIST déclarée. Recette : profil approuvé,
logiciel protégé, matériel exigé absent, accès non autorisé, signature réelle,
diagnostics sans secret, panne/clone/restauration et refus de repli.

##### Application au PA — A10i8

Option A validée : clés privées CA en ligne A10i6/A10i7 avec profil explicite
approuvé par émetteur/périmètre, logiciel protégé si autorisé ou matériel non
exportable exigé par politique ; jamais déduit OS/attestation TPM/VM/conteneur.
Racine hors ligne, TLS terminal, WireGuard/TPM et signatures A12f/A12g distincts,
sans transposition automatique. Algorithme CA/provider/placement/réplication
non fixés ; reprise après perte validée en A10i9, sans restauration de clé privée perdue.
Logiciel : chiffrement au repos, intégrité, déverrouillage protégé à qualifier,
service isolé et accès minimal, secrets hors sources/images/configuration métier/
journaux, références contrôlées. Clé accessible au processus d'émission, exposée
à sa compromission ou celle de l'hôte, sans non-exportabilité matérielle.
Matériel : provider qualifié, clé non exportable, dispositif local ou service
par contrat autorisé ; algorithme CA/génération/accès/signature/protection vérifiés,
sans équivalence HSM/TPM physique/vTPM. Matériel exigé absent : émission bloquée
sans repli logiciel, même si autorisé ailleurs. Aucun matériel CA imposé aux PA
ordinaires qui n'ont pas de clé CA.

Clé propre à l'émetteur A10i7 sans exposition à administration PBO/PA ordinaire ;
émission limitée aux décisions Django et A07/A12. Non-exportabilité sans garantie
contre toute émission abusive d'un processus compromis habilité ; contrôles/
révocation maintenus. Provider indisponible/protection invérifiable : pas d'émission,
autre clé/provider implicite ou validité prolongée. Compromission connue : retrait
A05 ; redémarrage/clone/restauration sans droit réactivé. Docker/LXC sans périphérique/
montage/privilège/droit Proxmox implicites, service externe par contrat PZT autorisé.
A10i8 A validé le 6 octobre 2026 ; profils Linux/Windows physiques/VM et Docker/LXC
Proxmox à qualifier. Logiciel sans protection matérielle équivalente contre extraction,
CPU/RAM/latence/coûts/disponibilité à qualifier. NIST SP 800-57 section 6.2.2 référencé
cadrage PZT, sans certification FIPS/conformité déclarée. Recette : profil approuvé,
protection logicielle, matériel exigé absent, accès refusé, signature réelle,
diagnostics sans secret, panne/clone/restauration et refus de repli.

#### Scenario: Conformité du traitement A10i8

- **WHEN** un profil revendique le traitement A10i8 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e870aee0a4

Source : `openspec/specs/pzt/spec.md`, ligne 4585. SHA-256 du bloc : `10b293e5a8039e89a27985e8ebd32d71b1a0c745410e8c13787385589c7b14d3`.

~~~~text
### Requirement: Contrat A10i9 — Nouvelle clé CA et recertification après perte — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i9 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i9

Option A validée : après perte définitive/corruption ou remplacement déclaré
de l'émetteur A10i7/A10i8, nouvelle paire CA indépendante, recertification par
l'autorité CA compétente selon la procédure de racine hors ligne A10i6, puis
reprovisionnement autorisé des émetteurs admis. Aucune sauvegarde de l'ancienne
clé privée CA utilisée pour reprendre la signature ; persistance protégée
normale conservée. Anticipation par secours indépendant pré-certifié validée en A10i10.

Racine hors ligne, clés terminales, WireGuard/TPM et signataires opérationnels
A12g exclus ; sauvegarde de PostgreSQL et des données publiques distincte.
Redémarrage normal avec clé intacte, protection et contexte courants vérifiables
sans rotation systématique. Panne temporaire sans remplacement aveugle ;
identité logique conservée sans habilitation héritée. Retrait de l'ancien
émetteur et traitement des certificats dépendants planifiés sous mandat,
réémission terminale sous contrôles courants A10i–A10i5. Transition CA distincte
du chevauchement terminal A10i3 ; aucune fenêtre CA ou révocation collective
implicite, aucune continuité garantie.

Compromission connue ou suspectée : réutilisation exclue, retrait des accès
concernés A05 et remplacement autorisé ; nouvelle clé sans réhabilitation
présumée de l'hôte compromis. Perte de clé privée sans compromission ne rend
pas à elle seule invalide la vérification des signatures publiques déjà émises ;
acceptation bornée par chaîne, politique des émetteurs, révocation et contrôles
courants. Conservation publique pour audit sans droit réactivé.

Nouvelle émission après preuve de possession, protection A10i8, identité/
périmètre, décision Django et engagement admissible A07/A12 seulement. Ancien
détenteur exclu des nouvelles émissions selon politique engagée et contrôle
vérifiable ; état d'émission/révocation, versions et identifiants réconciliés,
sans numéro de certificat réutilisé ou base/configuration ancienne réactivant
une autorité. État incertain : pas de signature avant réconciliation autorisée.
Autorité/provider indisponible : attente sans grâce, autre racine apprise en
réseau ou profil abaissé ; reprise des PA expirés par A02/A10i. Aucun montage/
droit hôte implicitement modifié, copie privée perdue restaurée ou ancienne
habilitation réintroduite par clone/restauration.

A10i9 A est validé le 6 octobre 2026. La procédure implique accès à la CA
compétente et migration des certificats dépendants, avec délais, coûts, volumes,
retrait et disponibilité à qualifier sur les cibles prévues, sans RTO promis.
Le [NIST SP 800-57 partie 1, section B.3.1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite sauvegarde et alternatives des clés de signature, y compris les CA ;
le choix Pixs de ne pas reprendre l'ancienne clé privée n'est pas une interdiction
universelle attribuée au NIST, ni une conformité déclarée. Recette : perte/
corruption, redémarrage normal, ancien détenteur actif, état incertain,
compromission/suspicion, provider/CA absents, recertification/reprovisionnement,
migration et absence de reprise de clé perdue ou d'ancien droit.

##### Application au PA — A10i9

Option A validée : perte définitive/corruption ou remplacement émetteur A10i7/
A10i8 avec nouvelle paire CA indépendante, recertification selon procédure CA
compétente/racine hors ligne A10i6 et reprovisionnement autorisé des émetteurs
admis. Aucune reprise par sauvegarde de l'ancienne clé privée ; persistance
protégée normale conservée. Anticipation par secours indépendant pré-certifié
validée en A10i10. Racine hors ligne, TLS terminal/WireGuard/TPM/signataires
A12g exclus, sauvegarde PostgreSQL/données publiques distincte.
Redémarrage normal avec clé/protection/contexte vérifiables sans rotation ;
panne temporaire sans remplacement aveugle. Retrait ancien émetteur et migration/
réémission dépendante sous mandat/contrôles A10i–A10i5 ; transition CA distincte
A10i3, aucune fenêtre/révocation collective implicite ni continuité garantie.

Compromission connue/suspectée exclut réutilisation, retrait A05 et remplacement
autorisé sans hôte réhabilité par seule rotation. Perte privée seule sans
compromission sans invalidation automatique des signatures publiques existantes,
acceptation bornée par chaîne/politique/révocation/contrôles courants. Audit public
conservé sans droit réactivé ; émission seulement après possession/protection
A10i8/identité/périmètre, décision Django et engagement admissible A07/A12.
Ancien détenteur exclu de l'émission par politique engagée/contrôle vérifiable,
état/versions/identifiants réconciliés sans numéro de certificat réutilisé ;
ancienne base/configuration sans autorité réactivée, état incertain bloquant.
Autorité/provider indisponible : attente sans grâce/racine apprise en réseau/
profil abaissé, PA expiré par reprise A02/A10i ; aucun montage/droit hôte implicite,
clé perdue restaurée ou habilitation reprise par clone/restauration.
A10i9 A validé le 6 octobre 2026 ; procédure CA et migration dépendante requises,
délais/coûts/volumes/retrait/disponibilité à qualifier sans RTO promis. NIST
SP 800-57 B.3.1.1 référencé cadrage PZT sans lui attribuer une interdiction universelle
de sauvegarde CA ou conformité Pixs. Recette : perte, redémarrage normal,
ancien détenteur actif, état incertain, compromission/suspicion/provider/CA absents,
recertification/migration sans clé perdue ou ancien droit repris.

#### Scenario: Conformité du traitement A10i9

- **WHEN** un profil revendique le traitement A10i9 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--f14c94acdf

Source : `openspec/specs/pzt/spec.md`, ligne 4680. SHA-256 du bloc : `d7b54a6a32822494d6a07b2d43547495df1bab67294be43e58c9b6d502943747`.

~~~~text
### Requirement: Contrat A10i10 — Secours CA indépendant pré-certifié — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i10 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i10

Option A validée : secours de chaque émetteur dédié A10i7 préparé avant incident,
avec paire CA indépendante, certificat CA propre préalablement délivré par la
procédure A10i6, référence/génération et protection A10i8 distinctes. Pas de
copie, dérivation ou sauvegarde de la clé principale ; remplacement indépendant
A10i9 conservé. Aucun partage de clé entre autorités logiques, aucune clé privée
ajoutée aux PA ordinaires ; racine hors ligne et signataires opérationnels exclus.

Le secours est réservé, sans mandat actif d'émission. Ses certificats publics
et état de préparation peuvent être distribués sous mandat sans l'autoriser à
émettre ou à être accepté comme émetteur actif. Certification CA, mandat,
politique d'émetteurs admis et droits métier sont des actes distincts. Préparation
sous décision explicite ; validité de chaîne/certificat, possession, protection,
fraîcheur requise et capacité de reprise qualifiées, secours périmé sans état prêt.

Une seule génération admissible pour de nouvelles émissions par émetteur logique
à un instant donné ; ancien signataire exclu (fencing), choix/génération engagés
A07/A12, état d'émission/révocation et identifiants réconciliés. Activation depuis
PBO par décision Django et mandat courant, jamais par simple détection de panne
ou possession de clé/certificat. Mode d'autorisation de bascule validé en A10i11.
État/exclusion incertains : blocage sans double émission, retour à ancienne clé
ou émission racine courante. A05, identité et contrôles applicables prioritaires.
Retrait de génération principale pour émission distinct du traitement des
certificats terminaux antérieurs : migration autorisée, compromission/révocation
traitées A05, remplacement et permissions sans grâce.

Activation du secours sans dispense de migration des certificats/liaisons et
émetteurs admis A10i9. Secours potentiellement affecté par l'incident, non qualifié
ou invalide : activation refusée, remplacement frais A10i9 sous décision autorisée.
Après usage, génération suivante préparée sous mandat, jamais clé retirée réactivée.
Clés indépendantes sans indépendance de panne supposée : stockage commun, même
hôte/provider ou domaine de compromission exposés dans le plan ; placement et
couverture de pannes à qualifier sans nombre de machines ou accès Proxmox imposés.

A10i10 A est validé le 6 octobre 2026 pour anticiper la certification hors ligne
sans restaurer la clé perdue, avec protection, suivi de validité et inventaire
d'un secours supplémentaires. Le [NIST SP 800-57 partie 1, section B.3.1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
évoque une seconde paire préparée comme alternative à la sauvegarde ; activation/
coordination retenues ici par Pixs. Charge, stockage, latence et délais à qualifier
sur Linux/Windows physiques/VM et Docker/LXC Proxmox, sans continuité ou RTO garantis.
Recette : réserve inactive, activation autorisée/refusée, principal encore actif,
état incertain, secours périmé/compromis, panne commune, migration et
réapprovisionnement sans ancienne génération réactivée.

##### Application au PA — A10i10

Option A validée : secours préparé par émetteur dédié A10i7, paire CA indépendante
sans copie/dérivation/sauvegarde de la principale, certificat CA préalablement
délivré A10i6, référence/génération/protection A10i8 propres ; A10i9 conservé.
Sans clé partagée entre autorités logiques ni clé CA privée aux PA ordinaires,
racine/signataires opérationnels exclus. Réserve sans mandat d'émission actif ;
préparation/distribution publique autorisées sans acceptation d'émetteur actif.
Certificat CA, mandat, politique d'émetteurs admis et droits métier distincts.
Chaîne/dates/possession/protection/fraîcheur requise/capacité de reprise qualifiées,
secours périmé sans état prêt.

Une génération admissible pour nouvelles émissions par émetteur logique, ancien
signataire exclu (fencing), choix/génération engagés A07/A12 et état/révocation/
identifiants réconciliés. Activation PBO sous décision Django/mandat courant,
jamais par panne ou possession seule ; mode d'autorisation validé en A10i11.
État/exclusion incertains bloquants sans double émission, ancienne clé de retour
ou racine émettant au quotidien. A05/identité/contrôles courants prioritaires ;
retrait de génération pour émission distinct du traitement des certificats
terminaux antérieurs, migration autorisée et compromission/révocation A05 sans grâce.
Secours sans dispense de migration A10i9 ; secours affecté par incident, non
qualifié/invalide bloqué, remplacement frais sous décision autorisée. Après usage,
réserve suivante préparée sous mandat sans clé retirée réactivée. Clés indépendantes
sans pannes indépendantes présumées : stockage/hôte/provider/domaine de compromission
communs visibles, placement/couverture à qualifier sans machines/droits Proxmox imposés.
A10i10 A validé le 6 octobre 2026 : anticipation de certification hors ligne sans
restaurer clé perdue, avec protection/suivi/inventaire supplémentaires. NIST SP
800-57 B.3.1.1 (source cadrage PZT) évoque seconde paire préparée, coordination Pixs.
Charge/stockage/latence/délais à qualifier sur Linux/Windows physiques/VM et Docker/
LXC Proxmox sans continuité/RTO garantis. Recette : réserve inactive, activation
refusée/autorisée, principal actif/état incertain, secours périmé/compromis,
panne commune/migration/réapprovisionnement sans ancienne génération réactivée.

#### Scenario: Conformité du traitement A10i10

- **WHEN** un profil revendique le traitement A10i10 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c560650e6f

Source : `openspec/specs/pzt/spec.md`, ligne 4772. SHA-256 du bloc : `72db96ca99779e0392cc7b11f044ca843dec50233ff9a799e8d463c5222382a9`.

~~~~text
### Requirement: Contrat A10i11 — Bascule CA automatisable sous mandat préalable — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i11 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i11

Option A validée : activation du secours A10i10 automatisable depuis PBO sous
politique et mandat de bascule préalables explicites, limités à l'émetteur,
au secours identifié, aux causes techniques admissibles, à une durée finie et
aux opérations autorisées. Mandat conditionnel distinct du mandat actif
d'émission : il ne rend pas la réserve signataire avant engagement admissible.
Critères déterministes vérifiés à l'incident, décision Django actuelle et
engagement A07/A12 requis ; aucune autorité locale de bascule au PA ou à la CA.

Conditions cumulatives : défaillance technique qualifiée couverte, absence de
suspicion de compromission selon l'évaluation autorisée requise, identité/
périmètre et mandat courants, secours valide/protégé A10i8, exclusion vérifiable
du principal, état/versions/identifiants réconciliés et PostgreSQL admissible
A12. Qualification du signal, seuils, fenêtres et délais à préciser avant profil
actif ; preuve d'exclusion validée en A10i12. Timeout ou silence ne prouvent
pas seuls l'exclusion ou une panne sans compromission. Hors mandat, suspicion
ou preuve insuffisante : automatique refusé, arbitrage opérateur ; retraits
immédiats A05 sans attente d'opérateur. L'opérateur ne dispense pas des contrôles
ou de l'exclusion pour maintenir le service.

Opération typée/versionnée/idempotente A07 ; identité/générations, préconditions,
permissions et résultat traçables. Un seul droit d'émission actif ; réponse
perdue/engagement incertain réconciliés avant nouvelle tentative, aucun retour
automatique au principal ou droit prolongé. Engagement, application par les
émetteurs et preuve d'émission admissible distingués PBO ; ACK ou commande
acceptée sans réussite présumée. Migration A10i9 et réserve suivante sous
mandats propres, aucune autorisation globale donnée par la bascule. Contrôle
PBO–PA toujours PZT, sans commande locale de secours. Hiérarchie, admission,
clés et coordination A12 conservées ; contrôleur, topologie et migration
terminale non choisis par cet arbitrage.

A10i11 A est validé le 6 octobre 2026 pour incidents techniques couverts sans
nouvelle intervention humaine, conditions d'activation maintenues. Le
[NIST SP 800-57 partie 1, sections 7.1–7.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
distingue pré-activation et usage actif d'une clé ; automatisation et mandats
retenus par Pixs sans automatisme prescrit par cette référence. Ressources,
délais, critères et disponibilité à qualifier sur les cibles prévues, sans
immédiateté, RTO garanti ou gain CPU/RAM promis. Recette : mandat valide/absent/
expiré, hors cause, secours invalide, suspicion, principal non exclu,
état/engagement incertains, doublon, preuve d'application et opérateur sans relâchement.

##### Application au PA — A10i11

Option A validée : activation A10i10 automatisable PBO sous politique/mandat
préalable explicite, émetteur/secours/causes techniques/durée finie/opérations
bornés. Mandat conditionnel distinct du mandat d'émission actif ; réserve
inactive avant engagement admissible. Critères déterministes à l'incident,
décision Django actuelle et engagement A07/A12, sans autorité locale PA/CA.
Conditions cumulatives : cause technique qualifiée couverte, évaluation de
sécurité requise sans suspicion, identité/périmètre/mandat courants, secours
valide/protégé A10i8, principal exclu de façon vérifiable, état/versions/
identifiants réconciliés et PostgreSQL admissible A12. Signal/seuils/fenêtres/
délais à qualifier avant profil actif ; preuve d'exclusion validée en A10i12.
Timeout/silence seuls sans preuve d'exclusion ou panne sûre. Hors mandat/
suspicion/preuve insuffisante : automatique refusé, arbitrage opérateur ;
retraits A05 immédiats sans attente, opérateur sans dispense de sécurité/exclusion.

Opération typée/versionnée/idempotente A07, générations/préconditions/permissions/
résultat traçables ; un seul droit d'émission actif. Réponse perdue/commit incertain
réconciliés avant reprise, aucun principal restauré ou droit prolongé. Engagement/
application/preuve d'émission admissible distingués PBO, ACK seul sans réussite.
Migration A10i9 et réserve suivante sous mandats propres, sans autorisation globale.
PBO–PA par PZT sans commande locale de secours ; admission/clés/hiérarchie/A12
conservés, contrôleur/topologie/migration terminale non choisis ici.
A10i11 A validé le 6 octobre 2026 ; incidents techniques couverts sans nouvelle
intervention humaine, contrôles maintenus. NIST SP 800-57 sections 7.1–7.2
(source cadrage PZT), mandat/automatisation Pixs sans automatisme NIST prescrit.
Ressources/délais/critères/disponibilité à qualifier sans immédiateté/RTO/gain CPU/RAM.
Recette : mandat valide/absent/expiré, hors cause, secours invalide/suspicion,
principal non exclu, état/engagement incertains, doublon/application, opérateur sans relâchement.

#### Scenario: Conformité du traitement A10i11

- **WHEN** un profil revendique le traitement A10i11 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e0a8407845

Source : `openspec/specs/pzt/spec.md`, ligne 4858. SHA-256 du bloc : `634da90e6b752f79caa057ac7c83467e9b990ae156836b9f0f81df1289de8fd3`.

~~~~text
### Requirement: Contrat A10i12 — Exclusion active et vérifiée du signataire CA — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10i12 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i12

Preuve requise A10i10/A10i11 avant d'autoriser le secours à émettre. Exclusion
du signataire CA distincte de la promotion PostgreSQL A12b, du retrait des
certificats terminaux et de la destruction de clé ; aucun outil ou privilège
hôte, montage, périphérique ou contrôleur Proxmox choisi implicitement.

L'option A validée impose une exclusion active par mécanisme qualifié extérieur
au processus CA, au point de signature/provider ou à sa frontière d'exécution.
Inhibition effective et persistante de l'usage de l'ancienne génération, ou
arrêt de son périmètre avec redémarrage interdit tant qu'il reste retiré, selon
un profil approuvé. Preuve actuelle liée à l'identité du signataire,
clé/génération, cible exacte, opération/version et état appliqué, produite par
le contrôleur de confiance compétent et vérifiée par Django. Un ACK d'arrêt,
la seule révocation d'un credential réseau ou d'un accès fichier ne prouvent
pas qu'une clé logicielle déjà chargée ne peut plus signer. Profil sans
mécanisme d'exclusion démontrable : activation automatique bloquée ; aucune
coupure hôte ou arrêt d'autres services sans mandat couvrant précisément cette
cible et ses impacts. L'expiration d'un bail ne remplace pas cette preuve active.

Source A12 admissible, génération/époque d'émission engagée et vérifiée à chaque
demande ; effet d'exclusion conservé à l'activation du secours. Principale
retirée sans réactivation par reconnexion, clone ou restauration ; pas de voie
alternative de signature autorisée. Preuve perdue/contradictoire, clé
potentiellement compromise ou état inconnu : pas de bascule automatique,
retrait A05 et arbitrage autorisé. Preuve de contrôle dans le modèle de
confiance qualifié, sans garantie contre tout hôte/provider compromis.
Nouvelle émission liée à décision/registre courants A07/A12 ; antidater un
certificat ne lui confère pas l'admissibilité. Certificats antérieurs non
compromis traités par migration A10i9, sans rejet collectif implicite ou grâce.

A10i12 A est validé le 6 octobre 2026. Contrôle qualifié et autorisé par profil
Linux/Windows physique/VM ou Docker/LXC Proxmox ; mécanismes détaillés validés
en A10i13. Ni support universel ni supériorité CPU/RAM ou délai garanti ; coûts
et délais à qualifier. La [documentation PostgreSQL sur la bascule](https://www.postgresql.org/docs/current/warm-standby-failover.html)
illustre le besoin d'éviter le retour d'un ancien primaire ; référence de
coordination, sans assimiler sa procédure à une preuve de fencing CA ou choisir
une version PostgreSQL. Recette : clé déjà chargée, arrêt non appliqué,
redémarrage/clone, mauvais signataire, exclusion levée après activation,
restauration, partition, preuve périmée et certificat tardif antidaté.

##### Application au PA — A10i12

Preuve A10i10/A10i11 avant émission secours, distincte de promotion PostgreSQL
A12b/retrait de certificats/destruction de clé ; aucun outil/droit hôte/montage/
périphérique/contrôleur Proxmox implicitement choisi.
L'option A validée impose un mécanisme qualifié extérieur au processus CA,
point de signature/provider ou frontière d'exécution ; inhibition effective
persistante de l'ancienne génération ou arrêt de périmètre avec redémarrage
interdit tant que retiré. Preuve actuelle signataire/clé/génération/cible/
opération/version/état appliqué, contrôleur de confiance compétent et
vérification Django. ACK d'arrêt ou retrait d'accès réseau/fichier seul sans
preuve pour clé logicielle déjà chargée. Mécanisme non démontrable bloquant
pour automatique ; arrêt/coupure hôte ou autres services sans mandat précis
de cible/impacts interdits. Expiration d'un bail sans remplacement de preuve active.

Source A12 admissible et génération/époque engagées/vérifiées à chaque demande,
effet d'exclusion conservé à activation. Retrait sans réactivation par
reconnexion/clone/restauration ou autre voie de signature autorisée. Preuve
perdue/contradictoire, compromis possible ou état inconnu : automatique refusé,
retrait A05/arbitrage autorisé. Modèle de confiance qualifié sans garantie
contre tout hôte/provider compromis. Émission liée à décision/registre A07/A12
courants, antidatage sans admissibilité ; anciens certificats non compromis
traités par migration A10i9 sans retrait collectif implicite/grâce.
A10i12 A validé le 6 octobre 2026 ; qualification Linux/Windows physiques/VM,
Docker/LXC Proxmox, mécanismes détaillés validés en A10i13. Aucun support/coût/
CPU/RAM/délai universel promis. Référence PostgreSQL bascule cadrage PZT, sans
preuve CA déduite ou version choisie. Recette : clé chargée, arrêt non appliqué,
redémarrage/clone, mauvais signataire, exclusion levée après activation,
restauration/partition/preuve périmée et certificat tardif antidaté.

#### Scenario: Conformité du traitement A10i12

- **WHEN** un profil revendique le traitement A10i12 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--a721c1d30e

Source : `openspec/specs/pzt/spec.md`, ligne 4943. SHA-256 du bloc : `dbe2ebfc4acf1054f3ea7efdb974e3a0f23ed8937c0ef1153618a8218c3e44cf`.

~~~~text
### Requirement: Contrat A10i13 — Mécanismes d'exclusion adaptés au profil CA — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i13 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i13

Ce choix précise l'application d'A10i12 aux profils de protection A10i8.
Les cibles Linux/Windows physiques/VM et Docker/LXC sous Proxmox ont des
qualifications propres. Le mécanisme et son périmètre sont approuvés avant
activation du profil, avec contrôleur compétent, identité de cible, impacts
et contrat de preuve ; aucun provider, outil système ou droit hôte
supplémentaire choisi implicitement.

L'option A validée retient une méthode adaptée au profil, sélectionnée de
manière déterministe au préalable. Pour une clé matérielle, inhibition ciblée
de clé/génération seulement si le provider permet de démontrer l'exclusion
persistante, y compris des sessions et capacités déjà accordées ; la
non-exportabilité seule ne suffit pas. Sinon, et pour une clé logicielle déjà
chargée, exclusion du périmètre d'exécution du signataire par un contrôleur
extérieur qualifié : arrêt effectif et interdiction de redémarrage/réutilisation
de l'ancienne génération. Le périmètre doit couvrir les processus et sessions
conservant une voie de signature ; un service déclaré arrêté ne suffit pas.

Le profil déclare une seule méthode autorisée ; échec sans escalade automatique
vers arrêt de VM, conteneur ou hôte. Changer de méthode exige une nouvelle
qualification et un mandat couvrant les impacts. Contrat de preuve commun,
adapters distincts lorsque les capacités des cibles diffèrent. Principal et
secours contrôlables séparément, même sur le même hôte ; aucune machine
physique distincte imposée par ce choix. L'exclusion du principal ne neutralise
pas le secours ni d'autres signataires admis.

Aucun arrêt global du PBO, de l'hôte ou d'autres services implicite. Cible
réellement arrêtée/inhibée et génération retirée vérifiées, sans confusion par
nom ou IP ; chemins de reprise, démarrage automatique, clone et restauration
couverts par le profil. Contrôleur injoignable, preuve périmée ou périmètre
incomplet : bascule automatique refusée. Les commandes vers un contrôleur
externe suivent un contrat de contrôle explicitement autorisé ; aucun droit
de contournement PBO–PA hors PZT accordé. Une cible retirée ne reçoit pas une
commande métier locale pour se réautoriser. Mandats A10i11, autorité Django/A12
et contrôles courants conservés ; topologie et implémentation restent à qualifier.

A10i13 A est validé le 7 octobre 2026 pour limiter l'action au périmètre
nécessaire qualifié, avec les deux profils A10i8 conservés. Aucun gain de
ressources ou délai universel promis ; adapters et coûts à qualifier.
La [documentation Docker sur les politiques de redémarrage](https://docs.docker.com/engine/containers/start-containers-automatically/)
distingue les reprises après arrêt et redémarrage du daemon ; ces politiques
font partie de la qualification, sans constituer seules une preuve A10i12.
Recette : session matérielle préexistante, clé logicielle chargée, provider sans
inhibition qualifiée, contrôleur indisponible, arrêt partiel, redémarrage
automatique/restauration, mauvaise cible, escalade refusée et secours affecté.

##### Application au PA — A10i13

Application d'A10i12 aux profils A10i8, sans provider/outil/droit hôte adopté.
Qualification propre aux cibles Linux/Windows physiques/VM, Docker/LXC Proxmox ;
méthode/périmètre approuvés avant activation, contrôleur compétent, cible,
impacts et contrat de preuve déclarés.
L'option A validée retient une méthode adaptée au profil, sélection déterministe
préalable. Clé matérielle : inhibition ciblée clé/génération si exclusion
persistante qualifiable, sessions/capacités préexistantes incluses ;
non-exportabilité seule insuffisante. Sinon, et pour clé logicielle chargée :
exclusion du périmètre d'exécution du signataire par contrôleur extérieur
qualifié, arrêt effectif et interdiction de redémarrage/réutilisation de
l'ancienne génération. Processus/sessions pouvant encore signer couverts ;
service déclaré arrêté insuffisant.
Une méthode autorisée par profil, échec sans escalade vers arrêt VM/conteneur/
hôte ; changement sous nouvelle qualification et mandat d'impacts. Contrat de
preuve commun, adapters adaptés aux capacités des cibles. Principal/secours
contrôlables séparément même sur même hôte, sans machine physique distincte
imposée ; secours et autres signataires admis préservés par l'exclusion.

Pas d'arrêt global PBO/hôte/autres services implicite. Cible réelle et génération
vérifiées sans confusion nom/IP, reprises/démarrages automatiques/clones/
restaurations couverts. Contrôleur inaccessible, preuve périmée ou périmètre
incomplet bloquants pour automatique. Contrôle externe seulement par contrat
explicitement autorisé, aucun contournement PBO–PA hors PZT ou commande métier
locale de réautorisation. Mandats A10i11, Django/A12 et contrôles courants
maintenus ; topologie/implémentation ouvertes.
A10i13 A validé le 7 octobre 2026 : action limitée au périmètre nécessaire
qualifié, deux profils A10i8 conservés, adapters/coûts à qualifier sans gain
CPU/RAM/délai universel promis. Référence Docker politiques de redémarrage
cadrage PZT, sans preuve A10i12 déduite. Recette : sessions matérielles préexistantes/
clé chargée, provider sans inhibition qualifiée, contrôleur indisponible,
arrêt partiel, redémarrage/restauration, mauvaise cible, escalade refusée,
secours affecté.

#### Scenario: Conformité du traitement A10i13

- **WHEN** un profil revendique le traitement A10i13 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--7f00749de1

Source : `openspec/specs/pzt/spec.md`, ligne 5039. SHA-256 du bloc : `5720a7fd11583cab54d8bde0efc84889213ac40ba6319ea6fa6d840734dd65fe`.

~~~~text
### Requirement: Contrat A10i14 — Clés CA ECDSA P-256 et signatures SHA-256 — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i14 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i14

L'option A validée fixe les clés CA ECDSA P-256 (`secp256r1`) et signatures de
certificats ECDSA avec SHA-256 (`ecdsa-with-SHA256`) pour la racine hors ligne
A10i6 et les intermédiaires d'émission, principal et secours A10i7–A10i13.
Chaque CA conserve sa paire indépendante ; aucun partage avec un PA, un service
TLS ou un signataire opérationnel, même avec le même algorithme. La clé terminale
ECDSA P-256 A10i5, les signatures opérationnelles Ed25519 A12e, WireGuard et le
chiffrement AES/ChaCha A10h conservent leurs profils et usages distincts.

Clé publique et signature X.509 conformes aux [RFC 5480](https://www.rfc-editor.org/rfc/rfc5480.html)
et [RFC 5758](https://www.rfc-editor.org/rfc/rfc5758.html), sans transposer
l'encodage JWS aux signatures de certificats. Génération de clés, aléa/nonce
de signature et contrôle de validité confiés à un provider qualifié ; aucun
algorithme cryptographique redéveloppé par Pixs. Profil explicite pour la PKI
dédiée, sans sélection automatique ni repli vers Ed25519, RSA ou autre
algorithme CA. Capacités requises du provider sous-jacent conservées.

Génération/signature CA et validation complète des chaînes qualifiées sur les
services d'émission et extrémités PA Linux/Windows physiques/VM, Docker/LXC
Proxmox. Provider matériel requis mais incompatible : activation bloquée,
sans export de clé ni repli logiciel. La [RFC 8446, section 4.2.3](https://www.rfc-editor.org/rfc/rfc8446.html#section-4.2.3)
distingue les signatures de certificats des signatures d'authentification TLS ;
compatibilité réelle vérifiée des deux côtés. Protection A10i8, indépendance
du secours, exclusion et autorité Django/A12 conservées. Durées CA, procédure
racine, révocation et remplacement d'ancrages restent ouverts ; renouvellement
normal des clés intermédiaires validé en A10i15. Changer le profil exige une
migration autorisée, sans changement de clé ou d'ancrage implicite. Aucun
provider, matériel ou logiciel CA adopté.

A10i14 A est validé le 7 octobre 2026 pour conserver la famille ECDSA retenue
pour les terminaux et limiter la diversité des profils X.509/TLS à qualifier.
Choix de cohérence Pixs, sans garantie de support universel ni classement absolu
de sécurité, performances ou consommation. Recette : signatures racine/
intermédiaire/terminal, chaîne et usages, deux extrémités TLS, provider logiciel/
matériel, aléa/nonce, encodages invalides, clé/algorithme incohérents et refus de repli.

##### Application au PA — A10i14

L'option A validée fixe les clés CA ECDSA P-256 (`secp256r1`), signatures
X.509 ECDSA SHA-256 (`ecdsa-with-SHA256`), pour racine hors ligne A10i6 et
intermédiaires principal/secours A10i7–A10i13. Paires indépendantes par CA,
sans partage avec PA/service TLS/signataire opérationnel. Clé terminale
ECDSA P-256 A10i5, signatures opérationnelles Ed25519 A12e, WireGuard et
AES/ChaCha A10h conservés, usages distincts même avec algorithme commun.
RFC 5480/5758 référencées dans cadrage PZT, sans encodage JWS transposé.
Génération/aléa/nonce et signatures par provider qualifié ; aucune cryptographie
redéveloppée par Pixs. Profil explicite sans sélection automatique ni repli
Ed25519/RSA/autre algorithme CA, capacités requises du provider conservées.
Signature CA/validation complète des chaînes qualifiées sur services d'émission
et PA Linux/Windows physiques/VM, Docker/LXC Proxmox. Matériel requis incompatible
bloquant, sans export/repli logiciel. RFC 8446 section 4.2.3 : signatures de
certificats et authentification TLS distinctes, capacités réelles à vérifier
des deux côtés. Protection A10i8, secours indépendant, exclusion et Django/A12
maintenus. Durées CA/procédure racine/révocation/remplacement d'ancrages ouverts ;
renouvellement normal des clés intermédiaires validé en A10i15. Évolution de
profil sous migration autorisée, sans changement implicite de clé/ancrage.
Aucun provider/matériel/logiciel CA choisi.
A10i14 A validé le 7 octobre 2026 pour cohérence avec famille ECDSA terminale
et diversité limitée des profils à qualifier, sans garantie universelle de
support ni classement sécurité/performances/consommation. Recette : signatures
racine/intermédiaire/terminal, chaîne/usages, extrémités TLS, providers logiciel/
matériel, aléa/nonce, encodages invalides, incohérence clé/algorithme, refus de repli.

#### Scenario: Conformité du traitement A10i14

- **WHEN** un profil revendique le traitement A10i14 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--bf2838d7ed

Source : `openspec/specs/pzt/spec.md`, ligne 5117. SHA-256 du bloc : `4b2c34874bd252be323272521704e5450e6a9fb4e4c60bf65c2dc3d58797bd25`.

~~~~text
### Requirement: Contrat A10i15 — Nouvelle paire à chaque renouvellement normal des CA intermédiaires — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i15 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i15

L'option A validée concerne le renouvellement planifié d'un intermédiaire
intact et non compromis, principal ou réserve. Elle complète A10i9
(perte/remplacement) sans modifier la racine hors ligne, les clés TLS terminales
A10i2 ou les clés opérationnelles A12e. Un certificat renouvelé n'accorde pas
de droit nouveau et ne réactive pas un signataire retiré.

Nouvelle paire CA indépendante ECDSA P-256 à chaque renouvellement normal,
nouveau certificat intermédiaire signé sous procédure racine autorisée,
nouvelle référence de clé/génération et provisionnement contrôlé des émetteurs
admis. Pas de dérivation de l'ancienne clé ni recertification de cette même clé
comme renouvellement normal. Une génération de réserve indépendante
pré-certifiée A10i10 peut préparer la transition si son profil, sa validité
et son mandat conviennent ; cette préparation n'autorise pas son activation.
Le secours conserve sa clé indépendante, sans devenir une copie de la principale.

Procédure racine explicite et autorisée, sans mise en ligne permanente de sa
clé ni signature locale autonome du PA. Django/A07/A12 vérifient identité,
périmètre, politique, état, chaîne, usages, validités et possession avant
engagement/application. Renouvellement actif et préparation de réserve
distingués ; une seule génération admissible pour les nouvelles émissions
par émetteur. Changement de signataire actif : exclusion A10i12/A10i13 vérifiée
avant activation du suivant, sous mandat de rotation planifiée propre.
A10i11 ne couvre pas implicitement cette rotation par son mandat d'incident technique.

Certificats terminaux antérieurs non compromis : maintien seulement dans une
migration explicite bornée A10i9, avec chaîne, émetteur admis et contrôles
courants, sans grâce à expiration/révocation. Retrait de l'ancien signataire
pour nouvelle émission distinct de l'acceptation transitoire des certificats
antérieurs. Renouvellement manqué ou état incertain sans prolongation de
validité, restauration d'anciens droits ou retour automatique. Clés anciennes
retirées et cycle de réserve réconciliés ; conservation éventuelle pour un
usage de révocation distinct seulement sous mandat explicite, sans droit
implicite de nouvelle émission. Durées et préparation validées en A10i16 ;
cryptopériodes, transition et procédure racine détaillée à qualifier.

A10i15 A est validé le 7 octobre 2026 pour renouveler effectivement la clé de
signature et identifier distinctement ses générations, avec préparation et
distribution contrôlée des références publiques. Aucun gain CPU/RAM universel
ni délai garanti. La [RFC 5280, section 6.1](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.1)
définit la validation de chaîne ; renouvellement et migration bornée sont des
règles Pixs, sans rotation à chaque renouvellement imposée par cette référence.
Recette : nouvelle clé, recertification de même clé refusée, réserve préparée,
procédure racine indisponible, état incertain, exclusion manquée, certificat
antérieur admissible/retiré et reprise après restauration.

##### Application au PA — A10i15

L'option A validée concerne un intermédiaire intact/non compromis, principal
ou réserve ; A10i9 perte/remplacement conservé, racine hors ligne distincte.
Clés terminales A10i2/opérationnelles A12e inchangées ; nouveau certificat sans
droits nouveaux ou réactivation d'un signataire retiré.
Nouvelle paire CA indépendante ECDSA P-256 à chaque renouvellement normal,
certificat sous procédure racine autorisée, référence clé/génération nouvelle
et provisionnement contrôlé des émetteurs admis. Aucune dérivation ou
recertification de l'ancienne clé comme renouvellement normal. Réserve
pré-certifiée indépendante A10i10 utilisable pour préparation si profil/
validité/mandat adaptés, sans activation implicite ou copie de clé principale.

Procédure racine explicite autorisée, sans clé racine en ligne permanente ou
signature PA autonome. Django/A07/A12 : identité/périmètre/politique/état/
chaîne/usages/validités/possession avant engagement/application. Renouvellement
actif/préparation réserve distingués, une génération de nouvelles émissions
admissible par émetteur. Changement de signataire actif après exclusion
A10i12/A10i13 sous mandat propre de rotation planifiée ; mandat d'incident
A10i11 sans couverture implicite.
Anciens certificats terminaux non compromis admissibles seulement en migration
explicite bornée A10i9 avec chaîne/émetteur/contrôles courants, sans grâce à
expiration/révocation ; retrait du signataire pour émission distinct de leur
acceptation transitoire. Échec/incertitude sans prolongation, restauration
d'anciens droits ni retour automatique. Clés retirées/cycle réserve réconciliés ;
éventuel usage de révocation distinct sous mandat explicite, sans nouvelle
émission implicite. Durées/préparation validées en A10i16 ; cryptopériodes,
transition/procédure racine détaillée à qualifier.
A10i15 A validé le 7 octobre 2026 : clé effectivement renouvelée/générations
distinctes, préparation/distribution de références publiques, sans gain CPU/RAM
universel ou délai garanti. RFC 5280 section 6.1 référencée dans cadrage PZT :
validation de chaîne, rotation/migration règles Pixs. Recette : nouvelle clé,
recertification même clé refusée, réserve, racine indisponible, état incertain,
exclusion manquée, anciens certificats admissibles/retirés, restauration.

#### Scenario: Conformité du traitement A10i15

- **WHEN** un profil revendique le traitement A10i15 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--eacd53b171

Source : `openspec/specs/pzt/spec.md`, ligne 5213. SHA-256 du bloc : `15460b2ecd147fc855a10757085dcb2bcb68d4e480d9bdfdca054de4c8d26753`.

~~~~text
### Requirement: Contrat A10i16 — Durées et anticipation des CA intermédiaires — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i16 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i16

L'option A validée retient un premier jet configurable depuis PBO pour
certificats des intermédiaires principal et réserve, avec renouvellement à
nouvelle paire A10i15. Les certificats terminaux conservent A10i4. Durée et
anticipation de la racine validées séparément en A10i17, cryptopériodes de ses
clés non fixées ici. Valeurs Pixs à qualifier, non prescriptions universelles
de la RFC 5280 ou du NIST.

| Paramètre | Valeur nominale validée |
| --- | --- |
| Validité du certificat intermédiaire | 365 jours |
| Début de préparation du renouvellement | 240 jours après notBefore |
| Marge restante au début de préparation | 125 jours |

Un jour vaut 24 heures ; dates UTC et horloge qualifiée. Durée effective issue
de notBefore/notAfter contrôlés, sans période nominale ajoutée à l'activation.
Le seuil est la fraction 240/365 de la validité effective ; si cette validité
est raccourcie, préparation avancée selon cette fraction. À réception après
le seuil : préparation immédiatement nécessaire, sans remise à zéro du temps.
Préparation et signature racine, provisionnement des références, mandat de
rotation, exclusion et application prouvée sont des étapes distinctes ;
atteindre le seuil n'autorise ni émission racine autonome ni bascule.
Échéance de rotation définie par le plan autorisé avant expiration, avec marge
opérationnelle qualifiée ; préparation commencée sans achèvement prouvé ne
vaut pas renouvellement réussi.

Réserve : dates de son propre certificat, âge réel de sa clé et validité
résiduelle suivis dès préparation, sans nouveau compteur à l'activation ou
après restauration. Réserve trop proche de son expiration pour satisfaire
le profil de transition refusée ; renouvellement/préparation d'une autre
génération sous mandat, sans activation pour contourner une échéance.
Chaque paire a un âge suivi depuis sa génération ; durée de certificat et
cryptopériode ne sont pas assimilées, aucune remise à zéro de l'âge de clé.
Les limites de clé et marges admissibles doivent être déclarées et qualifiées
avant activation du profil ; cet arbitrage ne fixe pas leur valeur numérique.

PBO expose dates, seuil, temps restant et état des étapes sans secrets ;
configuration typée/versionnée, politique autorisée et contrôles Django/A12.
Mandats, révocations et validités plus courts restent prioritaires.
Expiration ou retrait d’admissibilité de l’intermédiaire : aucune nouvelle émission admissible ni
chaîne utilisant cet intermédiaire acceptée hors validités courantes ;
retrait A05 sans grâce, ancien terminal traité par migration A10i9/A10i15.
Le profil Pixs borne la validité des nouveaux certificats terminaux par la
validité résiduelle de leur intermédiaire ; validité insuffisante diagnostiquée,
sans délivrer implicitement 24 heures au-delà de la CA. Incohérence de dates,
horloge non qualifiable, renouvellement manqué ou résultat incertain :
refus fermé et arbitrage autorisé, sans restauration d'anciens droits.

A10i16 A est validé le 7 octobre 2026 comme premier jet, avec marge nominale
de 125 jours pour la procédure racine hors ligne et la rotation contrôlée.
Fréquence moindre sans gain CPU/RAM global présumé ; retrait immédiat connu
en cas de compromission maintenu. Qualification exploitation/charge sur
Linux/Windows physiques/VM et Docker/LXC Proxmox, sans disponibilité garantie.
La [RFC 5280, section 4.1.2.5](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1.2.5)
définit les dates de validité ; ni cadence Pixs ni durée d'usage d'une clé
prescrites par ces dates seules. Recette : seuil nominal/raccourci,
certificat reçu tard, réserve ancienne, procédure racine indisponible,
rotation inachevée, terminal proche d'expiration CA, horloge/restauration,
révocation prioritaire et configuration invalide.

##### Application au PA — A10i16

L'option A validée retient un premier jet PBO configurable pour certificats
intermédiaires principal/réserve, avec nouvelle paire A10i15. Terminaux A10i4
maintenus ; durée/anticipation racine validées en A10i17, cryptopériodes de
ses clés non fixées ici. Valeurs Pixs à qualifier, aucune prescription
universelle RFC 5280/NIST.

| Paramètre | Valeur nominale validée |
| --- | --- |
| Validité du certificat intermédiaire | 365 jours |
| Début de préparation du renouvellement | 240 jours après notBefore |
| Marge restante au début de préparation | 125 jours |

Jour de 24 heures, UTC/horloge qualifiée ; durée effective notBefore/notAfter,
sans durée nominale ajoutée à activation. Seuil fraction 240/365 de validité
effective ; raccourcissement avançant la préparation. Réception après seuil :
préparation immédiatement nécessaire, temps non réinitialisé. Préparation/
signature racine/provisionnement/mandat/exclusion/application distincts ;
seuil sans émission racine autonome ou bascule autorisée. Échéance planifiée
avant expiration et marge opérationnelle qualifiée ; préparation sans
achèvement prouvé ne vaut pas renouvellement réussi.
Réserve : propres dates, âge réel de clé et validité résiduelle depuis
préparation, sans compteur renouvelé par activation/restauration. Résiduel
insuffisant pour transition bloquant ; nouvelle préparation sous mandat,
sans activation contournant échéance. Âge de clé depuis génération sans remise
à zéro, distinct de validité du certificat ; limites de clé/marges déclarées
et qualifiées avant activation, valeurs numériques non fixées ici.

PBO : dates/seuil/temps restant/étapes sans secrets, configuration typée/
versionnée, politique autorisée, Django/A12. Validités/mandats plus courts et
révocation prioritaires. CA expirée ou retirée des émetteurs admis sans nouvelle émission admissible
ou chaîne acceptée hors validités courantes ; A05 sans grâce, anciens terminaux
sous migration A10i9/A10i15. Profil Pixs : validité d'un nouveau terminal bornée
par résiduel de son intermédiaire, insuffisance diagnostiquée, sans 24 heures
implicites au-delà de CA. Dates incohérentes/horloge non qualifiable/échec/
incertitude : refus fermé/arbitrage, aucun ancien droit restauré.
A10i16 A validé le 7 octobre 2026, premier jet/marge nominale 125 jours pour
procédure racine et rotation contrôlée, sans gain global CPU/RAM déduit,
retrait connu immédiat maintenu. Qualification exploitation/charge Linux/
Windows physiques/VM, Docker/LXC Proxmox sans disponibilité garantie.
RFC 5280 section 4.1.2.5 référencée dans cadrage PZT : dates de validité, sans
cadence/cryptopériode Pixs déduites. Recette : seuil nominal/raccourci,
réception tardive, réserve ancienne/racine indisponible, rotation inachevée,
terminal proche expiration CA, horloge/restauration, révocation/configuration invalide.

#### Scenario: Conformité du traitement A10i16

- **WHEN** un profil revendique le traitement A10i16 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--48e3ce692f

Source : `openspec/specs/pzt/spec.md`, ligne 5334. SHA-256 du bloc : `1db6cdedd0fa318329c49d820ad0b8fbc584f474f244f288546fa2d566663838`.

~~~~text
### Requirement: Contrat A10i17 — Durée et anticipation de la racine hors ligne — choix du développeur validé le 7 octobre 2026

Le rôle chargé du traitement A10i17 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i17

Choix explicite du développeur pour la durée nominale du certificat racine
A10i6/A10i14 et la préparation de sa succession. Ni clé racine en ligne ni renouvellement
terminal par racine ; intermédiaires A10i16 inchangés. Nouvelle paire racine
indépendante validée en A10i18 ; procédure de succession, coexistence
des ancrages, sauvegarde et cryptopériodes détaillées restent distinctes.

| Paramètre | Valeur nominale validée |
| --- | --- |
| Durée du certificat racine | 7300 jours, soit 20 années nominales de 365 jours |
| Début de préparation de la succession | 5840 jours après notBefore, soit 16 années nominales de 365 jours |
| Marge restante au début de préparation | 1460 jours |

Jour de 24 heures, UTC/horloge qualifiée ; années indicatives, calculs en jours.
Seuil de préparation à quatre cinquièmes de la validité effective contrôlée
notBefore/notAfter, avancé si durée raccourcie. Réception après seuil :
préparation nécessaire immédiatement, sans compteur recommencé à installation,
restauration ou reprise. Préparation sous procédure racine autorisée, suivi
PBO des étapes et échéances ; seuil sans signature ou adoption automatique
sur les PA. Succession achevée et prouvée avant l'échéance admise par politique,
avec marge opérationnelle qualifiée. Échec sans auto-prolongation.

Admissibilité de chaque ancrage explicitement bornée/versionnée dans PZT,
au plus tard à notAfter du certificat racine de ce profil, avec contrôle
indépendant des seules règles du magasin OS ou du validateur TLS.
Racine retirée, échéance dépassée ou contexte non vérifiable : refus des
chaînes dépendantes et retrait A05, sans maintien implicite d'anciens droits.
La [RFC 5280, sections 6.1 et 6.2](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.1)
traite l'ancrage comme entrée de validation et n'impose pas l'application
de toutes les informations de son certificat auto-signé ; borne d'admission
validée ici comme règle Pixs, pas expiration uniforme garantie par la RFC.
Le profil validé borne aussi les certificats intermédiaires nouvellement
émis par l'échéance d'admissibilité de leur ancrage ; réduction de durée et
besoin de succession diagnostiqués, sans 365 jours implicites au-delà.

Durée du certificat distincte de l'âge et des périodes d'usage de la clé
racine, suivis selon politique qualifiée ; même certificat ou réinstallation
sans remise à zéro de l'âge. Valeur nominale sans garantie de sécurité de
l'algorithme sur toute cette période. Compromission/suspicion connue traitée
immédiatement selon A05 et procédure autorisée, sans attente du seuil.
Changement d'ancrage nécessite provisionnement authentifié explicite A02 et
contrôles courants Django/A12 ; ni téléchargement découvert ni recertification
ne prolonge automatiquement la confiance. Aucun root matériel/provider ou
protocole de succession choisi ; Linux/Windows physiques/VM et Docker/LXC
Proxmox à qualifier, clé racine hors processus courants PBO/PZT/PA conservée.

A10i17 est validé selon le choix du développeur le 7 octobre 2026 : 20 années
nominales, préparation à 16 années nominales et marge de 1460 jours. Année
nominale de 365 jours, sans assimilation aux anniversaires calendaires.
Paramètres PBO configurables et qualifiés ; ces dates ne prescrivent ni usage
ininterrompu de la clé pendant 20 ans ni garantie algorithmique jusqu'à cette
échéance. Politique de sécurité courante et limites de clé peuvent imposer
une succession anticipée, sans attendre le seuil de préparation normal.
Aucun classement universel sécurité/CPU/RAM/disponibilité ni durée prescrite
par la RFC 5280. Recette prévue : seuil nominal/raccourci, validateur ignorant dates
racine, borne PZT expirée, intermédiaire dépassant ancrage, succession manquée,
PA hors ligne, horloge/restauration, retrait connu et configuration invalide.

##### Application au PA — A10i17

Choix explicite du développeur : durée du certificat racine A10i6/A10i14 et
préparation de succession ; pas de
clé racine en ligne ou renouvellement terminal par racine. A10i16 conservé.
Nouvelle paire racine indépendante validée en A10i18 ; procédure/coexistence d'ancrages,
sauvegarde/cryptopériodes détaillées distinctes, non choisies ici.

| Paramètre | Valeur nominale validée |
| --- | --- |
| Durée du certificat racine | 7300 jours, soit 20 années nominales de 365 jours |
| Début de préparation de la succession | 5840 jours après notBefore, soit 16 années nominales de 365 jours |
| Marge restante au début de préparation | 1460 jours |

Jour de 24 heures, UTC/horloge qualifiée, années indicatives/calcul en jours.
Seuil quatre cinquièmes de validité effective notBefore/notAfter, avancé si
raccourcie ; réception après seuil sans compteur remis à zéro par installation/
restauration/reprise. Procédure racine autorisée, suivi PBO, seuil sans signature/
adoption PA automatique ; succession prouvée avant échéance admise et marge
qualifiée, échec sans prolongation.
Ancrage explicitement borné/versionné PZT au plus tard à notAfter de ce profil
racine, contrôle distinct du seul magasin OS/validateur TLS. Retrait/échéance/
contexte invérifiable : chaînes dépendantes refusées, A05 sans anciens droits
maintenus. RFC 5280 sections 6.1/6.2 référencées dans cadrage PZT : ancrage entrée
de validation, informations du certificat auto-signé pas toutes imposées ;
borne d'admission validée comme règle Pixs, sans expiration uniforme déduite de la RFC.
Intermédiaire nouvellement émis borné par échéance de son ancrage, durée
raccourcie/besoin de succession diagnostiqués, sans 365 jours au-delà.

Certificat distinct de l'âge/périodes d'usage de clé racine, suivi qualifié ;
réinstallation/même certificat sans âge réinitialisé. Aucune sécurité
algorithmique garantie sur durée nominale. Compromission/suspicion connue :
A05/procédure autorisée immédiats sans attendre seuil. Nouvel ancrage sous
provisionnement authentifié explicite A02 et Django/A12, découverte/
recertification sans confiance prolongée automatiquement. Matériel/provider/
protocole de succession non choisis ; cibles Linux/Windows physiques/VM,
Docker/LXC Proxmox à qualifier, clé racine hors processus courants PBO/PZT/PA.
A10i17 choix du développeur validé le 7 octobre 2026 : 20 années nominales,
préparation à 16 années nominales, marge 1460 jours. Année nominale de 365 jours,
sans anniversaires calendaires déduits ; paramètres PBO configurables/qualifiés.
Durée sans usage continu de clé imposé ni assurance algorithmique sur 20 ans ;
politique courante/limites de clé pouvant imposer succession anticipée avant
seuil normal. Aucun classement sécurité/CPU/RAM/disponibilité ni durée RFC
5280 prescrite. Recette
prévue : seuil nominal/raccourci, validateur ignorant dates racine, borne PZT
expirée, intermédiaire dépassant ancrage, succession manquée, PA hors ligne,
horloge/restauration/retrait connu/configuration invalide.

#### Scenario: Conformité du traitement A10i17

- **WHEN** un profil revendique le traitement A10i17 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--f0853e6e7c

Source : `openspec/specs/pzt/spec.md`, ligne 5455. SHA-256 du bloc : `40fa29bc4a6803fd86fb32c40add1bf27572180c5305b5f22ff59e04b20c7a61`.

~~~~text
### Requirement: Contrat A10i18 — Nouvelle paire indépendante à chaque succession racine — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i18 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i18

L'option A validée concerne la succession planifiée d'une racine intacte et
non compromise, dont durée et anticipation sont validées en A10i17. Protection
hors ligne A10i6, profil ECDSA P-256/SHA-256 A10i14 et renouvellement indépendant
des intermédiaires A10i15/A10i16 conservés ; aucun renouvellement implicite
des ancrages ou pouvoir autonome d'émission des PA.

Nouvelle paire racine indépendante ECDSA P-256 pour chaque succession normale,
certificat racine auto-signé et nouvelle référence de clé/génération. Nouvelle
clé générée/protégée sous procédure racine qualifiée, sans dérivation, copie
ou réutilisation de la précédente ; clé privée hors processus courants
PBO/PZT/PA. Recertification de la même clé non retenue pour la succession
normale. Nouvel ancrage public provisionné explicitement aux extrémités
autorisées, avec preuve d'application avant son usage. Les intermédiaires
de la génération suivante sont certifiés sous cette racine selon A10i15,
sans adoption automatique de l'ancien arbre. Changement de clé sans nouveau
domaine métier ou nouvelle autorité d'admission implicite.

PBO prépare le plan et suit les références publiques sans recevoir la clé
privée ; mandats racine explicites, décision Django/A07/A12, contrôle de
périmètre, dates, algorithme, usages et engagement/application distingués.
Certificat auto-signé ou signature valide seul sans droit de nouvelle
confiance ; installation dans un magasin OS sans preuve de politique PZT
appliquée insuffisante. La [RFC 5280, section 8](https://www.rfc-editor.org/rfc/rfc5280.html#section-8)
souligne le caractère critique de la distribution authentifiée des clés CA ;
protocole et procédure Pixs restent à spécifier, sans adoption d'un outil CA.
Même nom ou empreinte d'un ancien certificat sans décision courante insuffisant.

Migration des intermédiaires/terminaux et retrait final seulement sous plan
autorisé borné ; coexistence bornée des ancrages validée en A10i19. Ancienne
racine exclue de toute nouvelle certification à l'engagement de la succession ;
vérification des certificats antérieurs possible seulement dans la politique
transitoire explicite et avant sa borne A10i17, sans grâce pour retrait/
compromission ou expiration. Nouvelle certification, admission et droit métier
restent distincts. PA hors ligne ou migration incomplète : pas d'extension
automatique, réadmission/récupération A02 sous procédure authentifiée.
Signature croisée, restauration de clé perdue, clonage ou retour arrière
ne constituent pas une procédure autorisée par ce choix.

Perte, suspicion, protection invérifiable ou état incertain : renouvellement
normal bloqué, A05 et procédure racine exceptionnelle autorisée, à définir ;
aucune recertification pour déclarer la clé sûre ou effacer son historique.
Cryptopériodes, retrait de clé, sauvegarde, contrôles et moyens matériels
restent à qualifier. Cibles Linux/Windows physiques/VM, Docker/LXC Proxmox
conservées, sans changement implicite de privilège ou dépendance.
A10i18 A est validé le 7 octobre 2026 pour renouveler effectivement le secret
racine et distinguer les générations, avec provisionnement/migration des
ancrages à préparer ; aucun gain CPU/RAM ou disponibilité universels promis.
Recette : nouvelle clé, recertification même clé refusée, faux ancrage ou
mauvais périmètre, preuve d'installation absente, cryptopériode dépassée,
racine retirée, certificats antérieurs autorisés/retirés, PA hors ligne et restauration.

##### Application au PA — A10i18

L'option A validée concerne une racine intacte/non compromise en succession
planifiée, durée/anticipation A10i17 conservées. Protection hors ligne A10i6,
ECDSA P-256/SHA-256 A10i14 et intermédiaires A10i15/A10i16 maintenus, sans
confiance prolongée implicitement ou émission PA autonome.
Nouvelle paire racine indépendante ECDSA P-256, certificat auto-signé et
référence clé/génération nouvelle. Génération/protection qualifiées, sans
dérivation/copie/réutilisation de l'ancienne clé, privée hors processus
courants PBO/PZT/PA ; recertification même clé non retenue en succession
normale. Nouvel ancrage public provisionné explicitement, preuve appliquée
avant usage. Intermédiaires suivants certifiés sous nouvelle racine selon
A10i15, ancien arbre non adopté implicitement ; aucun nouveau domaine métier
ou autorité d'admission induit.
Plan PBO/références publiques sans clé privée, mandats racine explicites,
Django/A07/A12, périmètre/dates/algorithme/usages vérifiés, engagement/application
distincts. Auto-signature/signature valide sans droit de confiance, magasin
OS seul sans politique PZT appliquée insuffisant. RFC 5280 section 8 référencée
dans cadrage PZT : distribution authentifiée critique, procédure/protocole Pixs
ouverts, aucun outil CA choisi. Nom/ancienne empreinte seuls sans décision
courante insuffisants.
Migration/retrait final sous plan autorisé borné, coexistence des ancrages
validée en A10i19. Ancienne racine sans nouvelle certification à engagement ;
certificats antérieurs seulement sous politique transitoire explicite avant
borne A10i17, sans grâce pour retrait/compromission/expiration. Certification/
admission/droits distincts. PA hors ligne/migration incomplète sans extension,
récupération A02 authentifiée. Signature croisée/restauration de clé perdue/
clonage/retour arrière sans autorisation déduite de ce choix.
Perte/suspicion/protection invérifiable/état incertain : normal bloqué,
A05/procédure racine exceptionnelle autorisée à définir, aucune recertification
rendant la clé sûre ou effaçant son historique. Cryptopériodes/retrait/sauvegarde/
contrôles/matériel à qualifier ; cibles Linux/Windows physiques/VM, Docker/LXC
Proxmox conservées sans privilège/dépendance implicites.
A10i18 A validé le 7 octobre 2026 : secret renouvelé/générations distinctes,
provisionnement/migration d'ancrages à préparer, aucun gain CPU/RAM/disponibilité
universel promis. Recette : nouvelle clé, même clé recertifiée refusée, faux
ancrage/périmètre incorrect, preuve absente, cryptopériode dépassée, racine
retirée, anciens certificats admissibles/retirés, PA hors ligne/restauration.

#### Scenario: Conformité du traitement A10i18

- **WHEN** un profil revendique le traitement A10i18 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--9f26981801

Source : `openspec/specs/pzt/spec.md`, ligne 5561. SHA-256 du bloc : `900337c4250cda683f1f3b520b2c067a697f220f311c160964d6f31ebb558ced`.

~~~~text
### Requirement: Contrat A10i19 — Coexistence bornée des ancrages racine sur les PA — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i19 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i19

L'option A validée concerne une succession normale non compromise A10i18,
dans le même domaine PZT. Durées A10i17 et certificats A10i4/A10i16 bornés ;
la marge racine de 1460 jours n'est pas une durée de coexistence d'ancrages.
Contrôles PZT et mandats courants maintenus, sans confiance générale dans
toute chaîne portant l'un des noms de racine.

Coexistence autorisée, versionnée et bornée des ancrages courant et suivant
dans le périmètre de migration. Provisionnement authentifié du nouvel ancrage
via contrôle PZT admissible et mandat explicite, preuve de politique appliquée
puis vérification de la nouvelle chaîne avant migration des associations.
Plan distinguant préparation, engagement de la génération d'émission,
migration des credentials et retrait final ; génération unique admissible
pour nouvelles émissions par émetteur conservée, sans deux signataires actifs
déduits des deux ancrages. Après engagement de la nouvelle génération,
ancienne branche sans nouvelle émission admissible ; seuls ses certificats
antérieurs autorisés restent acceptables pendant la fenêtre bornée.
Retrait anticipé si convergence prouvée, sinon retrait au plus tard à l'échéance
engagée même avec PA non migrés. Plafond de 30 jours validé en A10i20, jamais déduit d'une
validité racine/intermédiaire ou prolongée par dernier contact.

Références explicites de clés/générations/ancrages et émetteurs admis,
identité/usages/périmètre/validités vérifiés ; chaîne valide seule sans droits.
Django/A07/A12 distingue ancrage distribué, politique engagée/appliquée et
association effectivement prouvée sous nouvelle chaîne. TLS 1.3, suite A10h,
attestation fraîche A10c et droits A05 contrôlés lors des reconnexions.
Coexistence de références sans duplication de commande métier ou élargissement
de périmètre ; contrôle PBO–PA toujours PZT. Aucune signature croisée ou
confiance par découverte adoptée. Plan incomplet, résultat incertain ou preuve
absente : nouvelles étapes suspendues/réconciliées, sans retour implicite à
l'ancienne génération. Retrait connu/compromission/expiration : A05 prioritaire,
aucune fenêtre de grâce et récupération racine exceptionnelle distincte.
Reprise/restauration/clone ou PA hors ligne sans prolongation ou anciens droits
réactivés. Profils et coûts qualifiés Linux/Windows physiques/VM, Docker/LXC
Proxmox ; aucun logiciel CA/provider ou nouveau privilège choisi.

A10i19 A est validé le 7 octobre 2026 pour faciliter une migration progressive
des PA avec préparation et preuves avant retrait, deux références d'ancrage
contrôlées pendant une fenêtre finie. La [RFC 5280, section 6.2](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.2)
laisse le choix des ancrages à la politique locale ; fenêtre et procédure
Pixs non prescrites par cette référence. Aucun gain universel CPU/RAM ou
continuité garantie. Recette : ancrage non autorisé, mauvais émetteur,
preuve distribuée/appliquée distincte, nouvelle association, PA hors ligne,
fenêtre expirée, retrait connu, double émission refusée, engagement incertain,
clone/restauration et ancienne chaîne après retrait.

##### Application au PA — A10i19

L'option A validée concerne une succession normale non compromise A10i18 dans
même domaine PZT, durées A10i17/certificats A10i4/A10i16 bornés. Marge racine
1460 jours sans durée de coexistence déduite ; contrôles/mandats courants,
noms de racine seuls sans confiance.
Coexistence ancrages courant/suivant autorisée/versionnée/bornée au périmètre.
Provisionnement authentifié sous contrôle PZT admissible et mandat explicite,
preuve appliquée/nouvelle chaîne avant migration des associations. Préparation/
engagement génération d'émission/migration credentials/retrait final distincts ;
une génération de nouvelles émissions admissible par émetteur, deux ancrages
sans deux signataires actifs. Après engagement de nouvelle génération, ancienne
branche sans nouvelle émission admissible, seuls certificats antérieurs
autorisés acceptables dans fenêtre. Retrait anticipé si convergence prouvée,
sinon à échéance engagée même si PA non migrés. Plafond de 30 jours validé en A10i20,
aucune validité ou dernier contact la prolongeant implicitement.
Références clés/générations/ancrages/émetteurs explicites, identité/usages/
périmètre/validités contrôlés, chaîne valide seule sans droits. Django/A07/A12 :
distribution, engagement/application et nouvelle association prouvée distingués.
Reconnexion TLS 1.3/suite A10h/attestation fraîche A10c/droits A05 ; coexistence
sans commande métier doublée ou périmètre élargi. PBO–PA toujours PZT,
signature croisée/découverte sans confiance implicite. Plan incomplet/
incertitude/preuve absente : suspension/réconciliation sans retour implicite ;
retrait connu/compromission/expiration A05 prioritaire, aucune grâce,
récupération exceptionnelle racine distincte. Reprise/restauration/clone/
hors ligne sans prolongation ou anciens droits réactivés. Qualification Linux/
Windows physiques/VM, Docker/LXC Proxmox, sans logiciel CA/provider/privilège adopté.
A10i19 A validé le 7 octobre 2026 : migration progressive avec préparation/
preuves, deux références contrôlées en fenêtre finie. RFC 5280 section 6.2
référencée cadrage PZT : politique locale d'ancrages, sans fenêtre/procédure Pixs
prescrites. Aucun gain CPU/RAM/continuité universel promis. Recette : faux
ancrage/émetteur, distribution/application distinctes, association nouvelle,
hors ligne, fenêtre expirée/retrait connu, double émission refusée,
engagement incertain, clone/restauration, ancienne chaîne après retrait.

#### Scenario: Conformité du traitement A10i19

- **WHEN** un profil revendique le traitement A10i19 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--67b216110f

Source : `openspec/specs/pzt/spec.md`, ligne 5657. SHA-256 du bloc : `e87e3ed14a0a051000a986f23c0d98526dede540fc67916c502016eec398ed73`.

~~~~text
### Requirement: Contrat A10i20 — Plafond de coexistence des ancrages racine — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i20 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i20

Premier jet validé, configurable depuis PBO pour la fenêtre A10i19 d'une succession
normale non compromise. Préparation de la racine A10i17 (marge 1460 jours),
validité terminale et chevauchement de credentials A10i4, ainsi que validité
intermédiaire A10i16 restent distincts. Une fenêtre d'ancrages ne prolonge
aucun certificat, mandat, droit, preuve d'attestation ou période d'usage de clé.

| Choix validé | Plafond nominal de coexistence | Retrait anticipé |
| --- | --- | --- |
| A | 30 jours | Dès convergence prouvée sous plan autorisé |

Jour de 24 heures. Début commun à l'engagement versionné Django/A07/A12 qui
autorise pour la première fois les deux ancrages dans le périmètre ; début UTC
et échéance finie déclarés avant activation. Installation préalable du nouvel
ancrage possible comme référence inactive, sans acceptation des deux racines
avant cet engagement. Le plafond couvre préparation admise, migration et
retrait ; pas de second compteur au changement de génération d'émission.
Application tardive à un PA, reconnexion, redémarrage, clone ou restauration
sans remise à zéro : seul le reliquat de l'échéance commune demeure utilisable.
Horloge/temps restant invérifiables : coexistence non activée ou accès dépendant
retiré selon A05, sans présumer un nouveau délai entier.

Plan autorisé avec budgets et marge qualifiés pour provisionnement, preuves,
engagement d'émission, renouvellement des terminaux et retrait final avant
l'échéance. Seuls les PA maintenus dans le périmètre et leurs associations
courantes prouvées comptent pour la convergence ; PA hors ligne/absence d'ACK
sans preuve de migration ou exclusion implicite du plan. Sortie de périmètre
requiert sa décision autorisée. Retrait anticipé versionné après preuve ;
échéance maximale jamais prolongée par non-convergence, relance ou dernier contact.

Fin effective au plus tard à échéance commune ou borne d'admissibilité de
l'ancien ancrage A10i17, avec retrait connu/compromission prioritaires A05.
Chaque chaîne, credential et permission conserve sa validité propre plus
courte. Après engagement d'émission, anciens certificats terminaux durent
au plus leur validité résiduelle A10i4, pas 30 jours ; chevauchement individuel
toujours au plus 5 minutes. La fenêtre ne donne donc pas à un PA hors ligne
un droit de retour de 30 jours : expiration sans grâce, récupération A02
authentifiée si nécessaire. Ancien ancrage et accès/sessions/tickets dépendants
retirés à la fin ; nouvelles associations sous chaîne nouvelle, attestation
A10c et droits courants. Échec/incertitude sans retour automatique, réconciliation
et diagnostic sans secret, retrait à échéance sans dépendre d'un ancien canal.

A validée pour permettre un calendrier de migration plus souple sur cibles
Linux/Windows physiques/VM et Docker/LXC Proxmox, avec plafond fini et retrait
plus tôt lorsque prouvé. Qualification calendrier,
charge, ressources et contrôles, sans gain CPU/RAM ou continuité garantis.
Valeur Pixs validée, pas une durée prescrite par la [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.html#section-6.2).
Recette prévue : début commun, application tardive, engagement d'émission
sans compteur neuf, convergence partielle, hors ligne, certificat expiré,
fenêtre de credentials 5 minutes, retrait anticipé/à terme, temps invérifiable,
restauration et configuration invalide. A10i20 A validé le 7 octobre 2026.

##### Application au PA — A10i20

Premier jet validé PBO configurable pour fenêtre A10i19, succession normale non
compromise. Marge racine 1460 jours A10i17, validité terminale/chevauchement
A10i4 et intermédiaire A10i16 distincts ; fenêtre sans certificat/mandat/
droit/attestation/période d'usage de clé prolongés.

| Choix validé | Plafond nominal de coexistence | Retrait anticipé |
| --- | --- | --- |
| A | 30 jours | Dès convergence prouvée sous plan autorisé |

Jour de 24 heures, début commun à engagement versionné Django/A07/A12
autorisant pour première fois deux ancrages, début UTC/échéance finie avant
activation. Référence nouvelle préinstallable inactive, sans deux racines
acceptées avant engagement. Plafond couvrant préparation admise/migration/
retrait, aucun compteur neuf à engagement d'émission. Application tardive/
reconnexion/redémarrage/clone/restauration sans remise à zéro, reliquat commun
seul utilisable. Horloge/reliquat invérifiables : activation refusée ou accès
dépendant retiré A05, sans nouveau délai entier présumé.
Plan/budgets/marge qualifiés pour provisionnement/preuves/engagement émission/
renouvellement terminal/retrait avant terme. Convergence : PA maintenus au
périmètre/associations courantes prouvées ; hors ligne/absence ACK sans preuve
ou sortie implicite. Sortie sous décision autorisée ; retrait anticipé
versionné/prouvé, plafond jamais prolongé par non-convergence/relance/contact.

Fin au plus tard à échéance commune ou borne d'ancien ancrage A10i17, retrait
connu/compromission A05 prioritaires. Validités propres plus courtes maintenues.
Après engagement émission, anciens terminaux bornés par validité résiduelle
A10i4, pas 30 jours ; chevauchement individuel au plus 5 minutes. Aucun droit
de retour hors ligne de 30 jours, expiration sans grâce/récupération A02
authentifiée. Ancien ancrage/accès/sessions/tickets dépendants retirés à terme ;
association nouvelle sous nouvelle chaîne/A10c/droits courants. Échec/
incertitude sans retour automatique, réconciliation/diagnostic sans secret,
retrait à échéance sans dépendance à ancien canal.
A validée pour calendrier plus souple Linux/Windows physiques/VM,
Docker/LXC Proxmox, plafond fini/retrait anticipé prouvé. Calendrier/charge/ressources/contrôles
à qualifier sans gain CPU/RAM/continuité promis ; valeur Pixs non prescrite
par RFC 5280 référencée cadrage PZT. Recette prévue : début commun/application
tardive, engagement émission sans compteur neuf, convergence partielle/hors
ligne, expiration terminal/5 minutes credentials, retrait anticipé/à terme,
temps invérifiable/restauration/configuration invalide. A10i20 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i20

- **WHEN** un profil revendique le traitement A10i20 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

