# Références normatives — Z17

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 7961 | [Contrat A10i49 — Bornes d’incertitude qualifiées pour admission avant échéance — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7961) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8039 | [Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8039) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8109 | [Contrat A10i51 — Lecture cohérente de temps et qualité à chaque décision — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8109) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8169 | [Contrat A10i52 — Budgets bornés d’acquisition et fraîcheur de preuve de temps — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8169) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8246 | [Contrat A10i53 — API native ou IPC documentée pour lecture structurée du temps — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8246) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--8a438b699e

Source : `openspec/specs/pzt/spec.md`, ligne 7961. SHA-256 du bloc : `afc05b83bf1150c4ec3dd584f55b2804b3c9a10d194da916b30cc932d15c4479`.

~~~~text
### Requirement: Contrat A10i49 — Bornes d’incertitude qualifiées pour admission avant échéance — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i49 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i49

Création active/échéance fixe A10i48 A et maximum 30 secondes A10i42 conservés.
Bornes qualifiées retenues pour comparaison temporelle, sans marge prolongeant admission
ou droit. Plafond d'incertitude de premier jet : 1 seconde, configurable sous
profil approuvé et à qualifier ; aucune source de temps ou synchronisation installée.

| Choix validé | Marge temporelle | Condition d'admission |
| --- | --- | --- |
| A | Bornes d'incertitude qualifiées à création et contrôle, au plus 1 seconde | Échéance fondée sur borne basse de création ; borne haute du temps courant strictement avant échéance |

À création, temps estimé T0 et borne d'erreur U0 admissibles ; référence
basse T0 − U0, échéance D au plus T0 − U0 + 30 secondes, et toutes validités
plus courtes prioritaires. D figée/engagée avant admission, aucune correction
future d'U0 ne recalcule D à la hausse. Au contrôle, estimation t et borne U(t)
qualifiées/fraîches ; admission seulement si t + U(t) < D et autres conditions
courantes satisfaites. U0 et U(t) finis, non négatifs, au plus 1 seconde dans
ce premier jet ; comparaison et arrondis conservateurs à spécifier.
Borne inconnue, périmée, invérifiable ou supérieure au plafond bloque création/
admission, aucun U=0 supposé par défaut ou à partir d'un simple drapeau synchronisé.

Contrôle temporel au point d'admission, sans décision sur une mesure
ancienne ; attente transactionnelle sans report d'échéance, mécanisme de contrôle/
engagement à qualifier, aucune admission tardive par seul précontrôle réussi.
Qualification couvre sources/chaîne de confiance, fraîcheur, dérive,
asymétrie/latence pertinentes, corrections d'horloge, création/contrôle sur membres
différents, suspension VM/conteneur, redémarrage/restauration et unités/précision.
Statistique de synchronisation ou horloge monotone seules sans preuve suffisante
de correspondance au temps de référence et de borne. Vieillissement des preuves
et perte de source sans intervalle d'erreur artificiellement rétréci.
Temps UTC estimé et mesure écoulée monotone conciliés selon profil à qualifier,
pas de calcul de marge depuis requête non fiable ou numéro de certificat.
Incertitude ne prouve pas à elle seule expiration réelle, mais ne permet pas
admission sans certitude d'être avant D. État terminal déjà engagé sans réouverture
par correction de temps ; fermeture de tentative selon commande A10i44,
autorisation et état incertains sans effets présumés.

Plafond client A10i42 et validités A05 restent applicables, borne la plus
restrictive prévaut. Réponse tardive, canal neuf ou reprise sans D remise à zéro.
Opération déjà admise suivie sous A10i40/A05/A12, aucune destruction ou annulation
automatique de décision engagée. Ce choix ne qualifie pas automatiquement le temps
pour durées CA, bail de permission, purge après 24 heures A10i46 ou horodatage
historique : contrats temporels de ces usages distincts.
Métadonnées de temps/qualité minimales liées au cycle/autorité/époque, audit
sans secret ; adaptateurs système validés A10i50 A, schéma/source/attestation, précision et
fraîcheur à spécifier avant activation. PBO/Django/A07/A12 contrôle le profil, modification
explicite/versionnée sans relèvement automatique par charge ou panne. PA sans
SQL direct, A10i22 B maintenu ; aucune règle système de temps/OpenSpec modifiée ici.

A validée pour une marge proportionnée aux bornes réellement qualifiées ;
marge fixe alternative non retenue. CPU/RAM/réseau et qualité des bornes à
mesurer sur contrôle,
Linux/Windows physiques/VM et Docker/LXC Proxmox, sans précision ou disponibilité
garanties, ni nouvelle source de temps imposée aux PA ordinaires.
[RFC 5905, section 11](https://www.rfc-editor.org/rfc/rfc5905.html#section-11)
décrit des statistiques de qualité/erreur NTP ; cette référence ne choisit pas
NTP comme provider ni ne qualifie seule une borne de sécurité Pixs. Valeur
1 seconde et formules de décision validées par Pixs, sans exigence de la RFC.
Recette : t+U juste avant/égal/après D, U inconnue/périmée/supérieure à 1 seconde,
U0 corrigée après création, attente transactionnelle franchissant D, changement
de membre, temps reculant/restauré et
refus sans nouvelle admission, délai ou droit réactivés.
A10i49 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i49

- **WHEN** un profil revendique le traitement A10i49 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--7c35729f30

Source : `openspec/specs/pzt/spec.md`, ligne 8039. SHA-256 du bloc : `2515f0ad709528aea175ae6e350cd3498a1aaab3cbf82e1c941fdd8582639414`.

~~~~text
### Requirement: Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i50 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i50

Bornes qualifiées A10i49 A, cycle A10i48 A et contrôles A05/A12 maintenus.
Adaptateurs système retenus pour autorités de validation, sans serveur, logiciel,
protocole de synchronisation ou nouvelle source de temps concrète adoptés.

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
dans le premier jet refusé pour ce rôle ; PA ordinaire sans rôle de validation
ne reçoit pas un service temporel supplémentaire par cette politique.

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
~~~~

### Référence pzt--e4e09ec26e

Source : `openspec/specs/pzt/spec.md`, ligne 8109. SHA-256 du bloc : `4b084ba7a51cc0ad796a242c2c4b41ed2168bd2bd5fe555f62fd3af9779f427d`.

~~~~text
### Requirement: Contrat A10i51 — Lecture cohérente de temps et qualité à chaque décision — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i51 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i51

Adaptateurs système A10i50 A, bornes A10i49 A et échéance immuable A10i48 A
conservés. Lecture cohérente par création/admission retenue,
sans changement de synchronisation d'infrastructure ou de plafond d'erreur.

| Choix validé | Acquisition | Réutilisation entre contrôles |
| --- | --- | --- |
| A | Lecture cohérente/qualifiée de temps et qualité à chaque création et contrôle d'admission | Aucun échantillon antérieur réutilisé comme preuve courante |

Lecture cohérente du provider au point de décision, estimation UTC, borne,
origine/état/âge de preuve et mesure monotone liés au même contexte d'acquisition.
Durée et cohérence des lectures, notamment entre heure et métriques distinctes,
couvertes par qualification ; ancien résultat d'API associé à une nouvelle heure
sans borne suffisante refusé. Âge de preuve de synchronisation distinct du temps
de lecture : une lecture récente ne rend pas récente une source ancienne.
Validité jusqu'au point d'usage et attente transactionnelle couvertes A10i49 ;
si mesure devenue inadmissible, nouvelle acquisition bornée ou refus, pas
d'admission sur précontrôle ancien. Lecture applicative sans nouvelle requête
de synchronisation réseau systématiquement exigée, service d'infrastructure
et son rythme inchangés. Preuve archivée pour audit sans réemploi automatique
pour autoriser une nouvelle tentative.

Interface en lecture A10i50, données sans clé/secrets et sans timestamp
client ou statut « synchronisé » transformés en preuve. D à création conservée,
aucune nouvelle acquisition ou borne améliorée ne la repousse. À admission,
t+U(t)<D et autres validités A10i49/A05, fermeture A10i44 et état courant recontrôlés.
Type/qualité/temps inconnus ou borne dépassée refuse création/admission ; requêtes,
budgets de lecture/fraîcheur validés A10i52 A, buffers/cadence/contrat à qualifier.
Aucun cycle expiré/terminal rouvert ni contrôle TPM/TLS/CA/purge qualifié par
ce choix ; lecture historique sans permission courante accordée.
PBO/Django/A07/A12 contrôle le profil, A10i22 B et PA sans SQL direct maintenus.
Pas de nouveau service temporel, cache distribué ou échange d'échantillons
entre hôtes admis implicitement ; plateformes Linux/Windows physiques/VM,
Docker/LXC Proxmox qualifiées sans modification d'horloge, privilège ou montage.

A validée pour limiter la complexité d'extrapolation/invalidation entre
décisions ; réemploi d'échantillon entre contrôles non retenu.
Coût de lecture/CPU/RAM/I/O à mesurer selon adaptateur/fréquence,
aucun gain universel ou absence de coût promis. Contrat validé par Pixs,
sans API/bibliothèque/daemon concret adoptés.
Recette : source ancienne lue récemment, heure/qualité incohérentes, lecture
franchissant D, ancien échantillon proposé au réemploi, U dépassant 1 seconde,
horloge corrigée, VM reprise/restaurée et refus sans admission/droit réactivés.
A10i51 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i51

- **WHEN** un profil revendique le traitement A10i51 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--732f4ee09e

Source : `openspec/specs/pzt/spec.md`, ligne 8169. SHA-256 du bloc : `ba5683405a453505f6eb0bf62293e832030468f3317d1aed2095c9221ee40aaf`.

~~~~text
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

| Choix validé | Durée par acquisition | Acquisitions au maximum par décision | Budget global d'acquisition | Âge maximal de preuve de synchronisation |
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

Âge maximal concerne la dernière preuve de référence/synchronisation admissible,
pas la date à laquelle l'adaptateur a simplement lu une métrique ou un fichier.
Calcul/identité de preuve, source et progression d'âge qualifiés, référence
modifiée ou horloge reculante sans âge artificiellement réinitialisé.
Âge nul/inconnu sans fraîcheur vraie présumée ; âge non vérifiable ou supérieur
au plafond refuse création/admission. Âge inférieur au plafond n'autorise pas
seul la décision : borne actuelle totale U(t), dérive, cohérence et confiance
A10i49/A10i50 toujours démontrées. Âge maximal 600 secondes sans permission de réemploi
d'un ancien échantillon entre décisions, A10i51 A inchangé.
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
~~~~

### Référence pzt--6618b62308

Source : `openspec/specs/pzt/spec.md`, ligne 8246. SHA-256 du bloc : `dfc03314795ce52596ad634dcda2f57be6f56690c6022a78c5f45f12640b8c8f`.

~~~~text
### Requirement: Contrat A10i53 — API native ou IPC documentée pour lecture structurée du temps — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i53 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i53

Adaptateurs système A10i50 A, lecture par contrôle A10i51 A, budgets A10i52 A
et borne A10i49 A conservés. API/IPC structurée en lecture retenue, sans API,
bibliothèque, outil, commande ou langage supplémentaire concret adopté.

| Choix validé | Interface | Conditions |
| --- | --- | --- |
| A | API native ou IPC documentée avec données structurées | Lecture seule, profil/version/types/unités/cohérence qualifiés, budgets A10i52 respectés |

Adaptateur lit interface documentée de l'OS ou du service d'infrastructure
approuvé, identité de source et frontière locale qualifiées. Contrat de retour
typé, tailles/versions/champs obligatoires, unités et états de qualité contrôlés ;
ABI/bibliothèque/transport IPC et mappage au contrat PZT à qualifier.
API permettant aussi réglage/configuration limitée aux opérations de lecture,
aucun mode de correction d'horloge ou modification de source activé par le lecteur.
Défaut d'interface/droit/compatibilité/qualité : résultat inadmissible et diagnostic,
aucun recours implicite à CLI ou privilège supplémentaire. Profil incapable de
fournir preuve sous cette politique refusé pour rôle de validation, sans PA
ordinaire déclaré incompatible par ce seul défaut.

Temps/qualité/âge/mesure monotone acquis de façon cohérente A10i51,
données bornées avant analyse, informations inconnues/absentes/ambiguës sans
borne zéro présumée. Unités/modes/profil de temps vérifiés, chiffres ou chaîne
« synchronisé » sans preuve A10i49. Résultats sensibles filtrés avant journaux/
transmission, métadonnées publiques minimales seulement ; aucune clé, jeton,
authentifiant ou contenu brut non maîtrisé remonté. Formats/volume/parsing et
auxiliaire isolé validé A10i54 A, contrat à qualifier avant activation,
budget 250 ms sans propriété d'annulation réelle déduite d'un simple timeout.

Placement local du lecteur et source d'infrastructure documentés ; PBO–PA garde
ses canaux PZT/mTLS A03/A07, collecte OS sans nouveau canal de pilotage PA.
Django/A12 reste autorité de décision, contrôle individuel A10i22 B et A05,
PA sans SQL direct. Linux/Windows physiques/VM, Docker/LXC Proxmox qualifiés
sans nouveau montage, permission conteneur, accès hôte ou synchronisation
implicitement autorisés. Dépendance nouvelle soumise à validation distincte,
aucun système, outil, test à effet de bord ou OpenSpec modifié/exécuté ici.

A validée pour données structurées et absence de lancement CLI par collecte ;
outils système alternatifs non retenus. Coûts des interfaces à mesurer, aucun
gain CPU/RAM/latence ou disponibilité universel,
aucune API garantissant seule borne de 1 seconde.
[Linux, adjtimex(2)](https://man7.org/linux/man-pages/man2/adjtimex.2.html)
documente lecture et réglage, [Microsoft, outils Windows Time](https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/windows-time-service-tools-and-settings)
des outils de consultation/configuration ; exemples de documentation à examiner,
sans adoption de ces interfaces ni borne/compatibilité automatiquement qualifiées.
Recette : mauvaise version/ABI/unité, données incomplètes/trop grandes, CLI
proposé comme repli, interface bloquée, résultat après budget, mode d'écriture,
annulation incomplète et refus sans commande/horloge/droit modifiés.
A10i53 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i53

- **WHEN** un profil revendique le traitement A10i53 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

