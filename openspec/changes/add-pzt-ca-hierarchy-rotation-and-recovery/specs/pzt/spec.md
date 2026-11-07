## ADDED Requirements

### Requirement: Amorçage PKI PZT autonome de première installation avant PostgreSQL

La première installation MAY créer localement sa confiance PKI/PZT avant PostgreSQL par la cérémonie propriétaire Z12 consommée par C08. Cette seule exception aux décisions/engagements Django/PostgreSQL A10i6/A12a MUST satisfaire les garanties des scénarios ci-dessous ; hors de ce parcours, le contrôle ordinaire reste obligatoire.

#### Scenario: Création initiale locale sous autorité technique vérifiée

- **WHEN** une première installation admissible prépare localement les seules identités PKI nécessaires à PA système, PZT et PBO pour établir PostgreSQL
- **THEN** Z12 MUST vérifier positivement origine native, opérateur, mandat explicite, installation, cible, exécutants, rôles fermés, opération/idempotence, plan/digest et politique/version courants, validité, révocation et fraîcheur ; aucune PKI privée opérationnelle ni identité PZT préémise ailleurs ne MUST être un prérequis
- **AND** racine, intermédiaires principal/secours indépendants et terminaux MUST conserver leurs hiérarchie, séparation des clés, algorithmes, usages, durées/bornes et protection matérielle sélectionnés, sans repli logiciel ; la racine MUST rester sous cérémonie hors ligne et hors processus courants
- **AND** le propriétaire Z12 MUST conserver un état technique durable protégé, versionné et fencé, un ancrage contre la restauration qualifié hors de ce domaine logiciel et un audit pré-base indépendant ; il MUST exposer des références publiques liées aux effets réels et un état courant inspectable, sans clé privée, credential PostgreSQL, faux engagement applicatif ni autorité déduite d’un DTO ou de la signature CA

#### Scenario: Adoption et fin de l’autorité initiale avant admission ordinaire

- **WHEN** PostgreSQL et les propriétaires courants sont disponibles pour adopter le premier lot local de confiance
- **THEN** PKI, Core, Auth et C05 MUST vérifier et rapprocher indépendamment les références publiques, leurs octets, les effets et les résultats sous autorité courante ; aucune nouvelle PKI ou recertification systématique ne MUST être déduite du seul passage, et âges, validités, échéances et rotations requises MUST rester opposables
- **AND** adoption PostgreSQL, retrait de l’autorité/canal/mandats initiaux et admission ordinaire MUST être des étapes distinctes prouvées ; aucune atomicité local/PostgreSQL ne MUST être présumée, et toute issue partielle ou incertaine MUST rester non prête et inspectable
- **AND** le retrait initial MUST être irréversible, durable et attesté par une preuve actuelle vérifiée indépendamment avant admission ordinaire Django/A07/A12 ; C08 MUST consommer le contrat Z12 sans devenir un second émetteur ou registre, et aucune panne ultérieure de PostgreSQL ne MUST rouvrir l’amorçage

### Requirement: Profil X.509 des terminaux de première installation Z12
Pour la première installation PA/PZT/PBO avant PostgreSQL, Z12 MUST appliquer le profil terminal fermé ci-dessous avec des clés matérielles non exportables P-256 et des paires distinctes par usage TLS. Les liaisons de politique/plan/identité, durées A10i4 et chaîne D2 MUST rester vérifiées indépendamment de l'admission et du mandat PostgreSQL.

#### Scenario: Émission initiale conforme sous autorité vérifiée
- **WHEN** la cérémonie initiale D4 dispose du mandat courant, du plan protégé et des preuves réelles de clé matérielle et de possession pour les usages client et serveur sélectionnés
- **THEN** les certificats émis respectent le profil terminal, les identités et endpoints explicitement liés au plan, avec des paires distinctes et une chaîne D2 vérifiée
- **AND** conformité du profil, autorisation, engagement et effet observé restent distingués ; aucun mandat technique PostgreSQL n'est déduit des certificats
- **AND** Pour la première installation PA/PZT/PBO avant PostgreSQL, Z12 MUST utiliser des clés ECDSA P-256 matérielles non exportables, sans repli logiciel, et des certificats terminaux X.509 v3 signés suivant le profil CA D2. Une paire et un certificat MUST être distincts pour chaque usage TLS client ou serveur ; aucune clé CA ou de signature opérateur MUST être réutilisée comme clé terminale.
- **AND** Le certificat terminal MUST contenir uniquement les six extensions BasicConstraints, KeyUsage, SubjectAlternativeName, ExtendedKeyUsage, SubjectKeyIdentifier et AuthorityKeyIdentifier. BasicConstraints MUST être critique, CA=false, sans pathLenConstraint ; KeyUsage MUST être critique avec digitalSignature seul ; ExtendedKeyUsage MUST être critique avec exactement clientAuth ou exactement serverAuth, sans anyExtendedKeyUsage. SKI et AKI MUST être non critiques et correspondre aux clés et à l'émetteur réellement vérifiés. La chaîne CA D2 reste distincte : elle n'admet que BasicConstraints, KeyUsage, SKI et AKI et MUST refuser NameConstraints et toute autre extension hors de ce profil fermé.
- **AND** Le Subject MUST être vide. Le SAN MUST être critique et contenir exactement une URI urn:uuid:<UUIDv7 d'instance terminale sous forme canonique minuscule>. Pour un certificat serveur, il MUST aussi contenir exactement l'iPAddress IPv4 loopback explicitement liée à l'endpoint dans le plan protégé ; pour un certificat client, cet iPAddress serveur MUST être absent. Aucun autre nom, CN/DNS de repli, adresse ou port par défaut MUST être ajouté. Les contrôles de chaîne, d'usage, d'URI d'instance et d'IP attendue MUST être indépendants ; loopback ou UUIDv7 seuls MUST NOT prouver identité native, fraîcheur ou autorité.
- **AND** Le propriétaire courant MUST lier installation, cible, identité native d'instance, rôle, usage, clé, génération et certificat à la politique protégée/versionnée et au mandat applicable. Les preuves matérielles, la possession et la correspondance clé/certificat MUST être réellement vérifiées. Le profil structural ou cryptographique seul MUST NOT valoir autorisation d'émettre, admission applicative ou mandat PostgreSQL. Les durées A10i4 sont conservées : 24 heures nominales, renouvellement aux deux tiers de la validité effective (16 heures seulement pour 24 heures effectives), chevauchement au plus cinq minutes selon A10i3, avec validités bornées par la politique et la chaîne et sans remise à zéro des âges.

#### Scenario: Refus d'identité, d'usage ou de chaîne inadmissibles
- **WHEN** un certificat ou une demande présente CA=true, un usage ou une extension étrangers, un EKU double, une paire mutualisée entre usages, un Subject non vide, un SAN non critique ou étranger, une URI non canonique, une IP absente ou étrangère au plan serveur, ou une contrainte de noms hors du profil CA D2
- **THEN** l'émission ou le chargement concerné est refusé avant utilisation TLS, sans repli CN/DNS, logiciel ou autre profil
- **AND** ni la proximité réseau ni une chaîne signée seule ne rétablissent une identité, une permission ou une confiance absentes

### Requirement: Résolution locale du matériel TLS sous propriétaire courant Z12
La composition native locale privée MUST résoudre le matériel TLS depuis le propriétaire réellement compétent pour l'étape, après vérification actuelle de politique, identité, état et ancrage. D4/D6, le même OSSL_LIB_CTX privé et les refus ci-dessous MUST être respectés ; aucune référence ou donnée cliente ne constitue une preuve d'autorité.

#### Scenario: Résolution locale depuis le propriétaire compétent
- **WHEN** la composition locale demande le matériel d'un terminal et que le propriétaire compétent pour l'étape réelle vérifie toutes les liaisons, protections, preuves et bornes courantes
- **THEN** le matériel public et la référence locale terminale sont liés au contexte OpenSSL privé avec une durée de vie contrôlée
- **AND** aucune clé privée, autorité déduite du certificat ou permission applicative n'est transmise par cette résolution
- **AND** Le matériel TLS MUST être résolu par une composition native locale privée depuis le propriétaire courant compétent. Avant toute fourniture ou utilisation, ce propriétaire MUST vérifier la politique protégée/versionnée, l'installation et la cible, les liaisons d'identité/rôle/usage/génération, l'état et l'époque courants, la validité/fraîcheur, la révocation et l'ancrage anti-restauration requis. Un instantané restaurable, un DTO bien formé, une référence opaque ou un booléen client MUST NOT remplacer ces vérifications. Toute source absente, périmée, contradictoire ou invérifiable MUST fermer l'opération concernée.
- **AND** Avant PostgreSQL, le propriétaire initial Z12 D4 MUST vérifier l'origine native et le mandat opérateur lié au plan ; UID 0 seul ou une preuve C01/R01 réutilisée pour un autre usage MUST NOT suffire. Après l'adoption et le retrait attesté D6, seul le propriétaire ordinaire Django/A07/A12 courant MUST pouvoir autoriser la fourniture du matériel. Les références publiques adoptées, âges, validités et retraits connus MUST être conservés ; une panne PostgreSQL après ce passage MUST NOT rouvrir l'autorité initiale.
- **AND** La résolution MUST fournir les seuls matériaux publics nécessaires et une référence opaque de clé terminale locale liée au même OSSL_LIB_CTX privé, avec possession et durée de vie réellement contrôlées. Les références de clés CA, les chemins ou ancres librement fournis par un appelant réseau, les clés privées ou blobs privés publics, les EVP_PKEY ou capsules Python publics et le repli logiciel MUST être refusés. Le contrôle de chaîne et la vérification du pair MUST rester nécessaires ; la résolution du matériel MUST NOT constituer l'autorisation applicative ni le mandat technique PostgreSQL, qui restent distincts.

#### Scenario: Refus après restauration, retrait ou perte d'autorité
- **WHEN** l'état ou la politique est restauré ancien, l'ancrage ou la fraîcheur est invérifiable, le propriétaire compétent est indisponible, une référence CA est proposée, ou une ancienne autorité initiale est sollicitée après clôture D6
- **THEN** la fourniture ou l'utilisation concernée est refusée avant transport ou admission, et le matériel devenu inadmissible cesse d'être utilisable
- **AND** une panne PostgreSQL après D6 ne rouvre pas la cérémonie initiale, ne remet pas les âges à zéro et ne rétablit aucun mandat retiré
### Requirement: Procédure exceptionnelle D18 avec UTC perdu

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — D18 exceptionnelle

La procédure exceptionnelle MUST intervenir seulement lorsque le repère universel ne peut pas être démontré par la voie normale. Elle MUST NOT devenir une routine à chaque lancement. Aucun poste extérieur, aucun opérateur particulier et aucun système mondial de navigation par satellite ne sont imposés. Une heure qualifiée existante MAY être utilisée lorsqu’elle est disponible. Toute réparation ultérieure du temps MUST NOT rouvrir l’autorité initiale. Les règles actuelles relatives à la signature personnelle, au défi à usage unique et à l’enveloppe demeurent conservées lorsque la cérémonie est effectivement nécessaire. Aucun contournement des dates des certificats n’est admis.

#### Scenario: UTC perdu sans routine

- **WHEN** le repère universel ne peut pas être démontré alors qu’une opération datée est demandée
- **THEN** la procédure exceptionnelle s’applique sous autorité explicite ou l’opération est refusée sans contournement des dates

## MODIFIED Requirements

### Requirement: Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i50 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i50

Bornes qualifiées A10i49 A, cycle A10i48 A et contrôles A05/A12 maintenus.
Adaptateurs système retenus pour autorités de validation, avec service système géré par PA selon profil et besoin, sans nouveau démon ni protocole Pixs ; sans autre serveur, logiciel, protocole de synchronisation ou nouvelle source de temps concrète adoptés.

| Choix validé | Provider | Qualification requise |
| --- | --- | --- |
| A | Adaptateurs par plateforme lisant l'horloge système et la qualité de synchronisation de l'infrastructure approuvée | Temps, borne et fraîcheur démontrés pour le profil exact OS/hôte/VM/conteneur |

Utiliser les services de synchronisation approuvés de l'infrastructure,
avec interface PZT commune en lecture : estimation UTC, borne d'erreur,
origine/état de qualification, âge de preuve et correspondance à mesure
monotone. Lecture à chaque contrôle validée A10i51 A, champs/format/unités/API à préciser.
Adaptateurs Linux et Windows
conditionnés aux capacités du profil exact, sans OS déclaré compatible par
son seul nom ou statut « synchronisé ». Statistiques du service exploitables
comme données d'entrée, jamais assimilées automatiquement à borne de sécurité.
Absence de métrique/preuve admissible, origine inconnue ou incohérence bloque
création/admission A10i49 ; aucune valeur zéro ou marge fixe substituées.
PZT ne règle pas automatiquement l'horloge hôte et ne crée pas un second
disciplineur système. Logiciels/configuration/sources d'infrastructure, confiance
et accès de collecte à qualifier, aucune dépendance installée par ce choix.

VM/conteneur : dépendances de temps, horloges exposées, source hôte/invité,
suspension/reprise/restauration et éventuelles métriques indirectes documentées.
Une copie de l'état du collecteur sans fraîcheur retrouvée ne suffit pas.
Docker/LXC Proxmox et Windows/Linux physiques/VM qualifiés séparément ; accès
au temps ou métadonnées sans privilège système, montage ou changement de
synchronisation implicitement accordés. Profil incapable de démontrer U<=1 seconde
dans le premier jet refusé pour ce rôle ; la présente politique MUST NOT accorder un service par PA, seul un service par horloge géré par PA lorsque le profil l’exige MAY être qualifié, sans préjuger sa qualification.

Contrat explicite de confiance et qualité, fraîcheur/dérive/perte de
source, cohérence des membres, correction/saut d'horloge et restauration testés.
PZT conserve calcul prudent des bornes A10i49, échéance immuable et contrôle au
point d'admission. Changement de provider/profil uniquement autorisé/versionné
et compatible, sans renégociation depuis un message reçu. Aucun « temps signé »,
TPM, majorité de sources ou précision nominale suffisant seul sans qualification.
PBO/Django gouverne configuration et diagnostics sans secret, A10i22 B maintenu,
PA sans accès SQL direct. Usage de temps pour autres contrats A05/CA/purge
reste à qualifier séparément ; aucune amélioration système implicite.

A validée pour réutiliser l'infrastructure sous preuve de qualité commune ;
service temporel Pixs dédié alternatif non retenu. Coûts CPU/RAM/I/O/réseau
à mesurer, aucune précision,
disponibilité ou ressource universellement meilleure. Aucune implémentation,
synchronisation d'hôte, configuration, certificat ou OpenSpec modifiés ici.
[Microsoft, Windows Time Service](https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-top)
décrit un service système et ses conditions, [RFC 5905, section 11](https://www.rfc-editor.org/rfc/rfc5905.html#section-11)
des statistiques de qualité ; références sans choix de W32Time/NTP obligatoire
ou conformité/borne PZT automatiquement démontrées. Recette : métrique absente,
statut synchronisé mais preuve insuffisante, preuve ancienne, source non autorisée,
temps hôte/invité divergents, suspension/restauration et collecte non bornée.
A10i50 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i50

- **WHEN** un profil revendique le traitement A10i50 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée

### Requirement: Contrat A10i52 — Budgets bornés d’acquisition et fraîcheur de preuve de temps — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i52 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i52

Lecture cohérente à chaque création/admission A10i51 A, adaptateurs A10i50 A,
borne d'erreur au plus 1 seconde A10i49 A et échéance immuable conservés.
Premier jet configurable validé, à qualifier sans performance mesurée ou API installée.
Interface API/IPC structurée validée A10i53 A.

| Choix validé | Durée par acquisition | Acquisitions au maximum par décision | Budget global d'acquisition | Âge maximal de preuve de synchronisation en SYNCHRONISE |
| --- | --- | --- | --- | --- |
| A | 250 millisecondes | 2 | 1 seconde | 600 secondes |

Acquisition = lecture cohérente de temps/qualité et contrôle du résultat du même
provider/profil. Nombre inclut première acquisition ; acquisition supplémentaire
seulement pour lecture techniquement transitoire qualifiée ou mesure devenue
inadmissible avant usage, pas de répétition d'une admission/décision déjà engagée.
Budget global depuis début de la première acquisition jusqu'à mesure admissible
au point de décision, attentes locales/I/O incluses ; pauses et redémarrage
sans crédit remis à zéro. Plafonds simultanés et budgets de sécurité plus courts
prioritaires, aucune acquisition commencée sans budget restant suffisant.
Reprise sans preuve de temps restant : refus, D jamais repoussée.

Âge maximal concerne la dernière preuve de référence/synchronisation admissible, toujours réelle et vérifiable, pas la date à laquelle l’adaptateur a simplement lu une métrique ou un fichier. Calcul/identité de preuve, source et progression d’âge qualifiés, référence modifiée ou horloge reculante sans âge artificiellement réinitialisé. Âge non vérifiable MUST conduire au refus en tous modes. Âge invérifiable ou supérieur au plafond en mode SYNCHRONISE MUST conduire au refus de création/admission. Âge inférieur au plafond n’autorise pas seul la décision : borne actuelle totale U(t), dérive, cohérence et confiance A10i49/A10i50 toujours démontrées. En mode SYNCHRONISE, âge maximal 600 secondes sans permission de réemploi d’un ancien échantillon entre décisions, A10i51 A inchangé. En mode distinct HORS_LIGNE, un âge supérieur à 600 secondes MAY être admis seulement si le modèle, la provenance et la continuité sont qualifiés, si le profil demeure valide et si la borne totale U(t) au point d’usage demeure inférieure ou égale à une seconde, avec acquisition actuelle et sans réarmement de droits, de budget ou d’échéance ; une lecture récente MUST NOT rajeunir la preuve amont et une nouvelle acquisition MUST NOT remettre à zéro un droit ; aucune durée magique n’est admise.
Borne d'erreur 1 seconde distincte du budget global de lecture 1 seconde et de l'âge
de preuve ; aucune mesure temporelle plus ancienne réputée exacte par budget large.

Même contexte/époque/version et domaine de mesure pour chaque acquisition,
origine/qualité inconnue, événement de temps non couvert ou refus de confiance
arrêtent le traitement ; aucune acquisition répétée destinée à attendre que
le contrôle de sécurité soit contournable. Nouvelle lecture récente sans source
qualifiée ne corrige pas une preuve trop ancienne. Signature ou statut
« synchronisé » seuls ne suffisent pas à admettre une borne de sécurité ;
diagnostic sans secret sur dépassement/échec.
Contrat de blocage/annulation/libération des ressources à qualifier pour toutes
APIs, même bloquantes ; pas de durée système réellement garantie par simple timeout.
Résultat trop tard ou après D refusé, aucun U=0, cache/repli de provider ou grâce.

Valeurs/profil approuvés/versionnés via PBO/Django/A07/A12 avant activation,
compatibilités et modèles de dérive/fraîcheur à qualifier sur Linux/Windows
physiques/VM et Docker/LXC Proxmox. Dossiers/temps de validation A10i39/A10i40,
relances A10i42 et réconciliation A10i43 sans nouveau crédit accordé.
A10i22 B/A05 prioritaires et PA sans SQL direct, aucune acquisition de preuve
de clôture courante imposée aux PA ordinaires. Aucun nom de variable, service,
source/protocole NTP, règle d'horloge, fichier ou OpenSpec modifié ici.

A validée comme premier jet borné/sobre ; profil élargi alternatif non retenu,
garanties de borne/cohérence et budgets appliqués simultanément.
Valeurs Pixs validées et à qualifier par mesures, sans cadence d'infrastructure supposée
compatible ou besoin de la modifier automatiquement. Coûts/CPU/RAM/I/O et
disponibilité à qualifier, aucune supériorité universelle ou réussite garantie.
Recette : durée/âge exacts et plus une unité de précision qualifiée, acquisition
bloquée, deuxième lecture cohérente, troisième interdite, preuve ancienne
lue récemment, U(t)>1 seconde malgré âge acceptable, suspension/reprise,
attente franchissant D et refus sans droit/admission réactivés.
A10i52 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i52

- **WHEN** un profil revendique le traitement A10i52 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée

#### Scenario: Perte d’Internet avec incertitude démontrée

- **WHEN** Internet est perdu mais que le modèle, la provenance et la continuité demeurent qualifiés avec U au point d’usage démontrée
- **THEN** les opérations dépendantes bornées peuvent continuer sans remise à zéro de droit

#### Scenario: Valeur à la borne puis au-delà

- **WHEN** la borne totale se situe juste à une seconde avec comparaison conservatrice établie
- **THEN** l’admission bornée peut intervenir sans prolongation d’échéance
- **WHEN** elle dépasse la borne d’une unité de précision qualifiée
- **THEN** la création ou l’admission est refusée sans nouvelle admission

#### Scenario: Mesure locale ancienne et modèle périmé

- **WHEN** une mesure locale ancienne est lue récemment ou que le modèle est périmé
- **THEN** elle ne doit pas être proposée comme preuve courante et une nouvelle acquisition bornée ou un refus doit intervenir

#### Scenario: Suspension, restauration et retour incohérent

- **WHEN** une suspension, une reprise ou une restauration est observée
- **THEN** la continuité doit être requalifiée avant toute admission
- **WHEN** le retour d’Internet apporte une correction incohérente avec l’intervalle maintenu
- **THEN** le chemin doit être refusé sans réécriture de l’échéance

#### Scenario: Plateformes conteneur et machines virtuelles

- **WHEN** la cible est LXC avec horloge hôte, VM avec horloge propre ou Windows avec fournisseur à qualifier
- **THEN** le profil exact doit être démontré et toute divergence hôte et invité doit bloquer l’admission concernée
