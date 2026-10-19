# Références normatives — Z25

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 138 | [Admission, pairs éphémères et retrait par génération](../../specs/pzt/spec.md#L138) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11954 | [Contrat A11a — Mode d'admission des PA — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L11954) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12080 | [Contrat A11b — Mode d'usage des jetons d'enrôlement — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L12080) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12208 | [Contrat A11c — Cycle de vie des pairs éphémères — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L12208) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--672038e548

Source : `openspec/specs/pzt/spec.md`, ligne 138. SHA-256 du bloc : `db46327efdf9e8e4fc0f1a03400f7cf3d729643cced44e37bb675653c42ca3a6`.

~~~~text
### Requirement: Admission, pairs éphémères et retrait par génération

Admission MUST utiliser mandat et preuves courants ; jeton individuel MUST être à usage unique, consommé atomiquement sans double identité après reprise. Pair éphémère MUST avoir une échéance finie, un renouvellement autorisé avant retrait et un nettoyage par génération sans résurrection. Le retrait MUST NOT supprimer implicitement VM, conteneur ou volume ; une nouvelle admission MUST utiliser un nouveau jeton et de nouvelles preuves.

#### Scenario: Admission, pairs éphémères et retrait par génération

- **WHEN** un pair retiré revient depuis un snapshot
- **THEN** son ancienne admission n'est pas réactivée
~~~~

### Référence pzt--952f315f50

Source : `openspec/specs/pzt/spec.md`, ligne 11954. SHA-256 du bloc : `d4363c259109a80d0bcb48140b9593bd85fa6c498319089eeb9c78beb7bcddb4`.

~~~~text
### Requirement: Contrat A11a — Mode d'admission des PA — option A validée le 5 octobre 2026

Le rôle chargé du traitement A11a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A11a

Ce choix précise qui autorise un nouveau PA à rejoindre PZT. Il conserve
l'amorçage limité A02, l'identité X.509 et la liaison WireGuard JWS, les
preuves TPM et références A10, les permissions A05 et l'autorité métier
Django. Détenir un jeton, être installé ou présenter un nom d'hôte attendu
ne suffit pas à l'admission.

L'option A validée le 5 octobre 2026 permet l'admission automatisée
sous mandat préalable
explicite, créé par un opérateur habilité ou une procédure déjà autorisée.
Le mandat déclare émetteur, destinataire, contexte Pixs, PA attendus ou
critères de provisionnement autorisés, profils de confiance, rôles et
affectations initiales, durée et quotas. Le service d'admission vérifie
les conditions courantes avant chaque décision. Une demande hors mandat
ou nécessitant un privilège supplémentaire reste en attente d'arbitrage
opérateur ; aucune exception de sécurité n'est accordée automatiquement.
Ce choix permet de provisionner machines physiques, VM et conteneurs
sans validation humaine répétée pour chaque instance conforme.

L'identité technique et son rattachement sont
résolus explicitement vers les DigitalIdentity et contextes autorisés,
sans rapprochement par nom d'hôte ou adresse seule. Les conditions de
provisionnement peuvent désigner une instance connue ou un ensemble
explicitement autorisé ; elles ne créent aucune confiance générale dans
une image clonée. La preuve de possession et l'attestation fraîche lient
les clés publiques et le PA à la demande et au canal d'amorçage. Le serveur
est vérifié depuis les ancrages préprovisionnés ; aucun certificat client
PZT déjà délivré n'est supposé pour le premier enrôlement.

Jeton et mandat restent bornés, révocables et limités à l'admission prévue.
La consommation concurrente des usages, l'unicité des rattachements et
l'engagement de la décision sont contrôlés avec idempotence et preuve
courante ; une reprise ne crée ni seconde identité ni double consommation
pour la même opération reconnue. Sans décision autoritative vérifiable,
aucune nouvelle admission n'est annoncée. Coordination et stockage A12,
mode d'usage des jetons A11b et durées de vie des pairs A11c restent à choisir.

Avant admission confirmée, seul A02 permet les échanges techniques requis ;
aucune gestion PBO–PA ni exposition métier n'est ouverte. L'interface PBO
suit demandes, motif stable, preuves et états de décision via les contrats
publics de l'autorité, sans contourner le canal PA. Après admission, émission
des justificatifs, distribution de la liaison et application des permissions
restent des étapes contrôlées ; état admis ne signifie pas configuration
réseau appliquée. `pzt-daemon` garde la propriété A04a, sans distribution de
sa clé privée ou de privilèges aux sessions et services.

Rôle d'autorité, relais ou passerelle, rattachement intertenant et droits
métier ne sont pas obtenus par simple adhésion. Le mandat les exige
explicitement lorsqu'ils sont applicables ; politique courante et Django
restent déterminants. Expiration/révocation du jeton interdit les nouvelles
admissions ; retrait d'un PA déjà admis suit sa révocation distincte A05.
Un refus ne déclenche ni profil de confiance moins exigeant, ni nouveau
jeton illimité, ni canal hors PZT. Secrets fournis par mécanisme protégé,
jamais dans une image, un diagnostic ou une ligne de commande journalisée.

La qualification couvre toutes les plateformes : conforme/hors mandat,
jeton volé sans identité et preuves requises, quotas concurrents, rejeu,
révocation pendant admission, changements entre examen et engagement,
crash et reprise, clone, séparation des contextes et absence d'accès avant
admission. Schémas, durées, quotas, parcours PBO et codes restent à définir.

[L'enrôlement automatisé NetBird](https://docs.netbird.io/manage/peers/register-machines-using-setup-keys)
illustre l'usage de jetons pour provisionner des machines ; PZT redéveloppe
ces capacités avec ses propres mandats et contrôles, sans reprendre de
brique, d'API, de durée ou de défaut NetBird.
A11a, option A, est validé ; schémas, durées et qualification restent à préciser.

##### Application au PA — A11a

L'admission conserve A02, X.509/JWS, preuves et références A10, permissions
A05 et autorité Django. Jeton seul, installation ou nom d'hôte ne suffit pas.

L'option A validée le 5 octobre 2026 automatise l'admission dans un mandat
préalable explicite
émis par un opérateur habilité ou une procédure déjà autorisée : émetteur,
destinataire, contexte, PA attendus ou critères de provisionnement autorisés,
profils, rôles, affectations, durée et quotas déclarés. Chaque demande exige
une évaluation courante. Hors mandat ou privilège supplémentaire : arbitrage
opérateur, sans exception de sécurité automatique. Le mandat couvre les
déploiements physiques, VM et conteneurs, dont les instances éphémères.

Identité et rattachement DigitalIdentity/contexte sont vérifiés
via les contrats publics, sans rapprochement par nom ou IP. Instance connue
ou ensemble de provisionnement explicitement autorisé ne signifie pas
confiance dans toute image clonée. Possession des clés et attestation fraîche
sont liées à la demande/canal ; ancrages serveur préprovisionnés vérifiés,
sans supposer un certificat client PZT avant premier enrôlement.

Mandat/jeton bornés et révocables, consommation concurrente et engagement
idempotents : reprise reconnue sans double identité ni double consommation.
Aucune nouvelle admission sans décision autoritative vérifiable ; coordination
A12, usages des jetons A11b et durée des pairs A11c restent à choisir.

Avant admission, échanges techniques A02 seuls, sans gestion PBO–PA ni
accès métier. PBO suit la demande via l'autorité et ses contrats publics.
Admission, délivrance des justificatifs et réseau effectivement appliqué
sont distingués ; `pzt-daemon` conserve ressources, clés et privilèges A04a.
Rôles d'autorité/relais/passerelle et droits métier ou intertenant exigent
leurs mandats et politiques, sans droit implicite par adhésion.

Jeton expiré/révoqué bloque les nouvelles admissions ; retrait des PA déjà
admis suit une révocation distincte A05. Aucun repli de confiance, jeton
illimité ou canal hors PZT après refus. Secrets protégés, sans image,
diagnostic ou commande journalisée.

Qualification de toutes les cibles : conforme/hors mandat, jeton volé sans
preuves requises, concurrence, rejeu, révocation, changement avant engagement,
crash/reprise, clone, contextes isolés et accès bloqué avant admission.
Schémas, quotas, durées, interface PBO et codes restent à définir ; sources
dans le cadrage PZT. A11a, option A, est validé ; schémas, durées et qualification restent à préciser.

#### Scenario: Conformité du traitement A11a

- **WHEN** un profil revendique le traitement A11a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--ff8aebc86d

Source : `openspec/specs/pzt/spec.md`, ligne 12080. SHA-256 du bloc : `93fc6c4fd5f53a334bd006406320402fd45e8847b2566709e45f54857bec735b`.

~~~~text
### Requirement: Contrat A11b — Mode d'usage des jetons d'enrôlement — option A validée le 5 octobre 2026

Le rôle chargé du traitement A11b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A11b

Le choix fixe la granularité du secret d'admission, sans modifier A11a :
mandat préalable, identité, contexte et preuves A10 restent obligatoires.
Chaque jeton a émetteur et destinataire autorisés,
mandat, périmètre, profils, validité finie et nombre d'usages explicites.
Aucun jeton sans expiration ni nombre d'usages illimité n'est admis.

L'option A validée utilise un jeton propre à chaque nouvelle instance PA,
à usage unique. Une procédure de provisionnement autorisée peut émettre
les jetons individuels d'un lot dans son mandat, sans validation humaine
pour chaque émission conforme ; elle n'obtient aucun pouvoir d'admission
supplémentaire. Le rattachement au PA attendu et aux clés publiques est
vérifié lors de l'enrôlement. Ce choix limite le partage d'un secret entre
instances et trace chaque admission, au prix d'un plus grand nombre de
jetons à émettre et gérer.

Le jeton autorise une seule admission confirmée ; aucun secret réutilisable
partagé entre les PA d'un lot n'est retenu. Les quotas du mandat de
provisionnement et le nombre de pairs simultanément actifs restent
distincts de cet usage unique : retirer un pair ne rend pas un jeton
consommé disponible. Chaque instance conserve identité, clés et preuves
propres ; aucun agrandissement automatique du mandat ou de ses quotas.

Un usage est consommé lors de l'engagement autoritatif de l'admission,
après vérification des conditions courantes et des preuves requises.
Consommation et création du rattachement restent cohérentes, atomiques
et idempotentes. Une réservation technique éventuelle est bornée et
n'accorde pas d'accès ; sa libération exige de connaître l'absence
d'engagement. Deux admissions distinctes ne consomment pas le même usage.
Un échec avant engagement ne constitue pas une admission et ne brûle pas
un usage, sans permettre des tentatives ou réservations non bornées.

La reprise d'une opération engagée peut retrouver son résultat après
vérification du demandeur, de l'identité, des clés et du contexte ; elle
ne crée pas un nouveau PA, ne consomme pas un autre usage et ne réactive
aucun accès expiré ou retiré. Même identifiant d'opération avec demande
contradictoire est refusé. En cas d'état d'engagement indéterminé, aucun
compteur n'est réinitialisé et aucune admission nouvelle n'est annoncée
sans réconciliation. Ces garanties sont qualifiées avec la coordination
A12 ; le stockage et l'algorithme de concurrence restent à choisir.

Le jeton est imprévisible, transmis par un mécanisme protégé et conservé
avec un accès limité ; aucun secret dans l'image, le code source, les
journaux, URL ou arguments de commande exposés. Sa représentation et
vérification au stockage restent à spécifier, sans supposer un jeton JWT
ou réutiliser les clés WireGuard/TPM comme jeton d'enrôlement. Après consommation,
le secret devenu inutile est retiré des emplacements de provisionnement
selon la politique ; les états d'engagement et traces sans secret requis
pour l'anti-rejeu demeurent. Restauration ne remet pas le quota à zéro.

Expiration, révocation connue ou quota épuisé bloque les nouvelles
admissions, y compris entre réservation et engagement. Retrait des PA
existants suit une révocation distincte A05 ; leurs reconnexions utilisent
identité, justificatifs et attestation, sans réutiliser le jeton consommé.
Clone ou remplacement d'instance suit le mandat et la procédure A10/A11,
sans récupération automatique d'un secret de l'ancienne instance.

Durées, quotas de provisionnement, budgets de tentative/réservation, schémas,
interfaces et conservation des traces restent à fixer. Qualification sur
toutes les plateformes : usages concurrents, secret volé sans preuves,
rejeu, expiration/révocation pendant admission, crash avant/après engagement,
reprise contradictoire et restauration, sans exposition ni double identité.

[Les jetons NetBird](https://docs.netbird.io/manage/peers/register-machines-using-setup-keys)
distinguent usage unique et réutilisation ; PZT développe ses propres
mécanismes avec les limites définies ici, sans reprendre les valeurs par
défaut ni les composants NetBird. A11b, option A, est validé ; durées,
schémas, stockage et qualification restent à préciser.

##### Application au PA — A11b

A11a et les preuves A10 sont conservés. Chaque jeton impose émetteur,
destinataire, mandat/périmètre/profils, validité finie et nombre d'usages
explicites ; aucun jeton sans échéance ou quota illimité.

L'option A validée donne un jeton à usage unique par nouvelle instance PA.
Le provisionnement autorisé émet automatiquement les jetons individuels
d'un lot dans son mandat, sans pouvoirs supplémentaires ; identité attendue
et clés publiques liées lors de l'enrôlement. Ce choix évite le partage du
secret et trace les admissions, avec davantage de jetons à gérer.

Une seule admission confirmée par jeton, sans secret réutilisable partagé
par un lot. Chaque PA garde identité, clés, preuves et permissions propres.
Quotas du mandat et nombre de pairs actifs restent distincts de l'usage
unique ; aucun agrandissement automatique du mandat. Retirer un pair ne
restitue pas un jeton consommé.

Consommation à l'engagement autoritatif après les contrôles, cohérente et
atomique avec le rattachement, reprise idempotente. Réservation éventuelle
bornée sans accès ; libération seulement si absence d'engagement connue.
Deux admissions distinctes ne prennent pas le même usage. Échec avant
engagement sans admission ni usage brûlé, avec tentatives limitées.

Reprise authentifiée liée à l'opération, identité, clés et contexte : résultat
retrouvé sans double consommation/identité ni réactivation de droits.
Demande contradictoire refusée ; état incertain réconcilié sans remise à
zéro du compteur. Coordination A12 et stockage restent à qualifier.

Secret imprévisible, accès limité, distribution protégée, sans image, source,
journal, URL ou argument exposé ; format et stockage à spécifier, sans
JWT implicite ni clés WireGuard/TPM partagées. Après usage, secret inutile
retiré selon la politique, états et traces sans secret conservés pour
anti-rejeu. Restauration ne réinitialise aucun quota.

Expiration/révocation/quota épuisé bloque les admissions nouvelles, même
avant engagement après réservation. PA admis : retrait distinct A05 et
reconnexion avec identité/justificatifs/attestation, sans ancien jeton.
Clone/remplacement soumis au mandat et à la procédure, sans secret hérité.
Durées, budgets, interfaces et rétention à définir ; toutes les cibles
qualifient concurrence, rejeu, expiration, vol sans preuves, crash/reprise
et restauration. Sources dans le cadrage PZT. A11b, option A, est validé ;
durées, schémas, stockage et qualification restent à préciser.

#### Scenario: Conformité du traitement A11b

- **WHEN** un profil revendique le traitement A11b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--54c9fbf487

Source : `openspec/specs/pzt/spec.md`, ligne 12208. SHA-256 du bloc : `fc3d02c49154df11f2f1b4849b6233e55eef3498e6dc7b301f7fca49badec4ea`.

~~~~text
### Requirement: Contrat A11c — Cycle de vie des pairs éphémères — option A validée le 5 octobre 2026

Le rôle chargé du traitement A11c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A11c

Le choix concerne la fin de vie du rattachement réseau d'un PA éphémère,
distincte de l'expiration du jeton consommé A11b, de la fraîcheur A10 et des
permissions bornées A05. L'option A validée conserve ces contrôles :
un pair encore inscrit ne dispose pas automatiquement d'un accès valide.
Le profil et le mandat déclarent le caractère éphémère ; Docker, LXC ou VM
ne le déterminent pas à eux seuls. Les PA physiques Linux/Windows, VM
Linux/Windows et conteneurs Docker/LXC sous Proxmox restent couverts selon
leur profil. Aucun accès à l'hyperviseur ou nouveau privilège n'est implicite.

L'option A validée donne à chaque génération de pair une échéance de vie
finie, fixée à l'admission. L'échéance ne glisse pas sur un heartbeat,
un handshake WireGuard ou une reconnexion. Un renouvellement avant échéance
exige une décision autoritative explicite sous mandat, avec identité,
contexte, preuves et permissions courants ; cette décision peut être
automatisée selon la politique, sans arbitrage humain systématique.
Elle définit une nouvelle échéance finie et reste versionnée/idempotente.
Sans renouvellement confirmé, le pair est retiré à l'échéance, même s'il
reste joignable. Une décision de renouvellement connue après expiration
ne ressuscite pas l'ancienne génération. Ce choix borne la présence des
instances abandonnées, y compris encore connectées ; il exige de
dimensionner les renouvellements et de gérer les partitions.

Une fin de charge authentifiée et autorisée ou une révocation explicite
peut retirer le pair avant l'échéance. La présence seule ne renouvelle ni
les preuves A10 ni les permissions A05. Le retrait sur le seul seuil
d'inactivité n'est pas retenu comme modèle de fin de vie. Une absence de
heartbeat signale une indisponibilité, sans prouver la destruction de la
machine ou du conteneur. Les signaux déclarent
identité, génération et contexte ; un vieux signal ne retire pas une
instance de remplacement. Renouvellement et retrait concurrents
sont ordonnés par l'autorité A12, sans décision locale contradictoire ;
le retrait engagé interdit toute réactivation de la même génération.

Le retrait bloque l'accès selon A05 puis retire les annonces,
cartes, routes, affectations et noms détenus par ce pair via les autorités
compétentes, dont le module DNS A06c. Ressources partagées ou administrées
par l'opérateur préservées ; aucune suppression de VM, conteneur, volume
ou donnée métier. Le suivi distingue accès retiré, propagation et nettoyage
confirmés ; reprises idempotentes et budgets finis, échec visible sans
annoncer un nettoyage complet. Un pair distant injoignable reste soumis
aux expirations et protections A05, sans garantie de suppression instantanée
de ses routes locales ni de tous les caches DNS.

Audit sans secret et tombstones de génération persistent selon la rétention
et l'anti-rejeu déclarés ; restaurations et messages tardifs sont réconciliés
sans résurrection ni réutilisation du jeton consommé. Après retrait, une
nouvelle admission/génération exige un mandat, un nouveau jeton individuel
A11b et les preuves A10 ; reconnexion d'un pair encore valide distincte.

Durées par profil, limites de renouvellement, signaux de fin de charge,
horloges, budgets de propagation/nettoyage, rétention et coordination A12
restent à qualifier. Scénarios sur toutes les cibles : charge terminée,
arrêt brutal, partition, instance oubliée encore présente, échéance,
renouvellement concurrent, retour tardif, clone et restauration, sans
retrait d'une autre génération ni réactivation de droits.

[NetBird décrit des pairs éphémères retirés après inactivité](https://docs.netbird.io/manage/peers/register-machines-using-setup-keys).
PZT retient sa propre échéance de vie finie, sans reprendre ce modèle,
son délai ni ses composants. A11c, option A, est validé ; durées, limites
et qualification restent à préciser.

##### Application au PA — A11c

Le rattachement éphémère est distinct du jeton A11b, des preuves A10 et des
permissions A05. Profil et mandat déclarent le caractère éphémère ; une
VM ou un conteneur ne l'impose pas. Toutes les cibles physiques/VM
Linux/Windows et Docker/LXC sous Proxmox restent concernées selon le profil,
sans accès implicite à l'hyperviseur, droits ou montages supplémentaires.

L'option A validée fixe une échéance de vie finie par génération à
l'admission, sans report sur heartbeat, handshake ou reconnexion.
Renouvellement avant échéance par décision autoritative explicite sous
mandat et contrôles courants, automatisable selon la politique ; nouvelle
échéance finie, version et reprise idempotente. Sans décision confirmée,
retrait à l'échéance même si le PA est présent. Une décision tardive ne
ressuscite pas une génération expirée. Ce choix borne la présence des
instances abandonnées, avec renouvellements et partitions à dimensionner.

Fin de charge authentifiée/mandatée ou révocation explicite : retrait
possible avant l'échéance. Présence seule sans renouvellement des preuves
A10 ou des permissions A05 ; retrait sur le seul seuil d'inactivité non
retenu comme modèle de fin de vie. Absence de heartbeat sans preuve de
destruction.
Signaux liés à l'identité, génération et contexte ; ancienne génération
sans effet sur la remplaçante. Concurrence renouvellement/retrait
ordonnée par A12, aucun retour après retrait engagé.

Retrait : blocage A05, puis retrait contrôlé des annonces, cartes,
routes, affectations et noms possédés par le pair, avec le module DNS A06c.
Préservation des ressources partagées/opérateur, VM, conteneurs, volumes
et données métier. Suivi distinct du blocage, propagation et nettoyage
confirmés, reprises idempotentes bornées et échecs visibles. PA injoignable :
expirations/protection A05, sans suppression distante instantanée garantie
ni disparition immédiate de tous les caches DNS.

Audit/tombstones conservés selon politique ; restauration et messages
anciens sans résurrection. Après retrait, nouvelle admission/génération
sous mandat avec nouveau jeton A11b et preuves A10, distincte de la
reconnexion d'un pair valide. Durées, renouvellements, signaux de fin de charge,
horloges, budgets, rétention et A12 restent à qualifier sur chaque cible :
fin de charge, crash, partition, présence prolongée, échéance,
concurrence, retour tardif et restauration. Sources dans le cadrage PZT.
A11c, option A, est validé ; durées, limites et qualification restent à préciser.

#### Scenario: Conformité du traitement A11c

- **WHEN** un profil revendique le traitement A11c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

