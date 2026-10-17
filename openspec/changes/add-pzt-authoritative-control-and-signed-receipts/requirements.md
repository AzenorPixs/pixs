# Références normatives — Z03

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 48 | [Autorité métier et état de contrôle cohérents](../../specs/pzt/spec.md#L48) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12328 | [Contrat A12a — Source autoritative et coordination — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L12328) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12458 | [Contrat A12b — Durabilité, réplication et bascule — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L12458) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12605 | [Contrat A12c — Signataires et preuves d'engagement — option A validée le 5 octobre 2026](../../specs/pzt/spec.md#L12605) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12755 | [Contrat A12d — Format des reçus et permissions PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L12755) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12867 | [Contrat A12e — Algorithme des reçus et permissions PZT — option B validée le 6 octobre 2026](../../specs/pzt/spec.md#L12867) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 12984 | [Contrat A12f — Protection des clés des signataires opérationnels — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L12984) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 13081 | [Contrat A12g — Reprise après perte des clés opérationnelles — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L13081) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--8cb0863347

Source : `openspec/specs/pzt/spec.md`, ligne 48. SHA-256 du bloc : `f95af68cf125ee598e0adf720178e1bce4e0fd2075c848b1f8b093d5e2c2b323`.

~~~~text
### Requirement: Autorité métier et état de contrôle cohérents

Django MUST porter autorisations et mutations applicatives ; PostgreSQL MUST faire autorité par périmètre pour les états de contrôle. PBO et autorités MUST NOT décider indépendamment de la validité d'un même mandat. Un seul primaire admissible MUST écrire ; redondance critique MUST utiliser durabilité synchrone et promotion après exclusion vérifiée. PA MUST NOT accéder directement aux tables ni déduire un commit PostgreSQL d'une signature reçue.

#### Scenario: Autorité métier et état de contrôle cohérents

- **WHEN** une réponse de commit est perdue
- **THEN** la source autoritative est réconciliée sans nouvelle mutation aveugle
~~~~

### Référence pzt--2166301eaf

Source : `openspec/specs/pzt/spec.md`, ligne 12328. SHA-256 du bloc : `60f9a3f12e2565bb9f8c86162b45f51b1699181b8dd56bdd37f3f1dc0e522858`.

~~~~text
### Requirement: Contrat A12a — Source autoritative et coordination — option A validée le 5 octobre 2026

Le rôle chargé du traitement A12a MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12a

Le choix porte sur la persistance et l'engagement des états de contrôle
PZT : délégations, politiques, admissions/consommations A11b, échéances
A11c, révocations, versions de références A10f et mandats de routage A08c.
Django conserve l'autorisation métier ; PostgreSQL reste la source de
vérité applicative Pixs. Chaque autorité logique possède un périmètre,
une source et une frontière d'engagement déclarés. Racine et sous-autorités
ne deviennent pas une autorité globale unique par choix de stockage.

L'option A validée coordonne ces états dans la source PostgreSQL
autoritative déclarée pour le périmètre d'autorité, avec un seul primaire
admissible à l'écriture de ce périmètre à un instant donné. Plusieurs
membres de service actifs peuvent recevoir des demandes et les soumettre
aux Commands/contrats autorisés de l'autorité ; contrôles et engagement
cohérent passent par cette même frontière transactionnelle. Contraintes,
préconditions/version, déduplication et contrôle de concurrence garantissent
notamment qu'un usage A11b, une génération A11c ou un mandat A08c ne peut
recevoir deux engagements incompatibles. Répliques et caches restent des
projections ; ni une base locale de membre ni une réplication ultérieure
ne permet une décision concurrente autonome sur le même périmètre.

Dans A, les mutations et événements requis sont inscrits dans la même
transaction avec l'outbox. Un résultat critique n'est confirmé qu'après
engagement durable selon le profil à qualifier ; publication, signature
et exécution sont suivies distinctement, avec reprise idempotente. Le PA
consomme les contrats PZT/PBO selon son rôle et n'accède pas directement
aux tables Pixs ; PA ordinaire sans serveur PostgreSQL ou moteur de
consensus embarqué. Mutualisation ou séparation des bases selon autorité
et résidence reste un choix de déploiement explicite.

Ce choix réutilise la persistance et les transactions Pixs et limite
les frontières d'engagement à coordonner. Il dépend de la
disponibilité et de la qualification de cette source pour les changements
critiques ; aucun gain CPU/RAM chiffré ni disponibilité automatique promis.

Aucun journal de consensus spécialisé n'est retenu comme source
autoritative supplémentaire du contrôle PZT. La protection des écritures
et de la bascule de PostgreSQL reste à préciser en A12b, sans imposer
un produit ou un contrôleur de haute disponibilité.

Engagement autoritatif indisponible ou incertain :
aucune admission, attribution, extension, renouvellement ou bascule critique
nouvelle confirmée. Les opérations déjà autorisées suivent leurs preuves,
fraîcheur et échéances A05/A10/A11c, sans prolongation ni retour autonome.
Une révocation connue ferme l'accès ; une demande non engagée est signalée
comme telle et peut déclencher un blocage local conservatoire autorisé,
sans prétendre à une révocation globale confirmée. Reprises et restaurations
réconcilient états, versions, tombstones et idempotences avant exposition.

Le profil doit empêcher deux primaires/détenteurs périmés de confirmer des
changements concurrents et empêcher une restauration de rendre disponible
un jeton consommé ou un mandat retiré. Les mécanismes précis d'exclusion
(fencing), seuils de réplication, topologie et promotion suivent A12b A
validé, avec paramètres et qualification encore requis.
Une bascule non qualifiée reste bloquée, même si une autre machine est
joignable. A12c A fixe les signataires et la liaison des preuves ; consensus
et stockage ne prouvent pas qu'un signataire compromis est légitime.

Qualification : demandes concurrentes entre membres, double consommation,
révocation contre renouvellement, perte de réponse après engagement,
partition, promotion avec ancien primaire encore actif, retard de réplica,
restauration et replay. Topologie, isolation/verrous, budgets, RPO/RTO,
chemins de reprise et garanties des changements critiques restent à définir.
Les rôles d'autorité sont qualifiés séparément du PA ordinaire sur les
plateformes autorisées ; aucun droit système ou accès Proxmox implicite.

[PostgreSQL documente les verrous de concurrence](https://www.postgresql.org/docs/current/explicit-locking.html)
et [la prévention des deux primaires lors d'une bascule](https://www.postgresql.org/docs/current/warm-standby-failover.html).
Ces sources ne changent pas les versions supportées du projet. A12a,
option A, est validé ; A12b A est également validé, paramètres à qualifier ;
A12c/A12d A validés ; Ed25519 A12e B validé le 6 octobre 2026 pour reçus/permissions.

##### Application au PA — A12a

Périmètre : états de contrôle PZT, admissions A11b, échéances A11c,
révocations, références A10f et mandats A08c. Django conserve l'autorisation
métier et PostgreSQL la source de vérité applicative. Chaque autorité
logique déclare sa portée et sa frontière d'engagement ; hiérarchie et
responsabilités des instances préservées.

L'option A validée coordonne ces états dans PostgreSQL autoritatif pour
le périmètre, avec un seul primaire admissible à l'écriture à un instant
donné. Plusieurs membres de service actifs reçoivent les demandes via
les contrats autorisés, avec contrôles/engagement dans la même frontière
transactionnelle. Concurrence, préconditions, versions et idempotences
empêchent les engagements incompatibles ; répliques/caches/base locale de
membre sans pouvoir de décision indépendant. Mutation et outbox atomiques,
confirmation après engagement durable qualifié, publication/signature et
exécution suivies séparément. Ce choix réutilise Pixs et limite les
frontières à coordonner ; dépendance à la disponibilité de cette source,
sans gain CPU/RAM chiffré ni HA automatique.

Aucun journal de consensus spécialisé retenu comme autre source du
contrôle PZT ; protection de l'écriture/bascule PostgreSQL à choisir en
A12b, sans produit ou contrôleur HA imposé.

Le PA consomme les contrats selon son rôle,
sans accès direct aux tables Pixs, sans PostgreSQL ou consensus imposé au
PA ordinaire. Source indisponible/engagement incertain : aucune nouvelle
admission, attribution, extension, renouvellement ou bascule critique
confirmée ; droits antérieurs seulement encore vérifiables et non expirés,
révocation connue bloquante, aucun retour autonome. Blocage conservatoire
local autorisé possible sans prétendre à une révocation globale engagée.
Restaurations réconciliées sans résurrection ou réutilisation de jeton.

A12b A validé : durabilité synchrone et bascule contrôlée ; seuils, copies,
exclusion des anciens primaires/détenteurs et reprise restent à qualifier,
bascule non qualifiée bloquée. A12c : signataires et preuve d'engagement, distincts du
consensus. Topologie et budgets RPO/RTO à définir. Qualification des rôles
d'autorité séparée du PA ordinaire sur les cibles autorisées : concurrence,
crash après engagement, partition, deux primaires, répliques en retard,
restauration et replay, sans nouveau privilège implicite. Sources dans le
cadrage PZT. A12a/A12b options A validées ; paramètres à qualifier ;
A12c/A12d A validés ; Ed25519 A12e B validé le 6 octobre 2026 pour reçus/permissions.

#### Scenario: Conformité du traitement A12a

- **WHEN** un profil revendique le traitement A12a et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--50dbb10664

Source : `openspec/specs/pzt/spec.md`, ligne 12458. SHA-256 du bloc : `7c36553cb9634a6cdcf5d82428d84f761c390dcd76c6ef217dea939b1a1182df`.

~~~~text
### Requirement: Contrat A12b — Durabilité, réplication et bascule — option A validée le 5 octobre 2026

Le rôle chargé du traitement A12b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12b

Le choix fixe le profil de référence des autorités redondantes autour de
PostgreSQL retenu en A12a. Il ne transforme pas chaque PA en membre de
base de données. Un profil explicitement mono-instance garde sa durabilité
locale et une reprise déclarée, sans garantie HA ; aucun passage automatique
vers ce profil après perte des copies ou du mécanisme de coordination.

L'option A validée impose une réplication synchrone des décisions critiques.
Le succès n'est confirmé qu'après conservation durable du journal de
transaction sur le primaire et les répliques admissibles requises par le
profil. Ce profil vise la conservation des décisions confirmées lors des
pannes qu'il couvre, notamment jetons consommés, révocations, échéances,
versions et idempotences. Une réception réseau ou écriture dans le cache
OS distant ne suffit pas. Le choix des copies, de leur nombre et des
domaines de panne reste à qualifier, sans majorité ou nombre de machines
supposés ici. La disponibilité d'une copie à jour ne garantit pas à elle
seule qu'elle est autorisée à devenir primaire.

Perte des copies requises : pas de confirmation locale substituée
à la garantie synchrone. Délais d'attente bornés, diagnostic et état
d'engagement indéterminé lorsqu'il n'est pas possible de prouver l'échec.
Un commit peut exister malgré une réponse perdue ou une attente annulée ;
aucune remise à disposition du jeton ni nouvelle opération pour contourner
l'incertitude. Après crash/reprise, une mutation présente dans l'outbox
n'est pas, à elle seule, la preuve de la durabilité requise : vérification
de l'engagement et de la couverture de réplication avant confirmation,
publication autoritative ou signature, puis reprise idempotente.

La bascule est contrôlée, automatisable uniquement après
qualification. Avant promotion, il faut prouver l'exclusion de l'ancien
primaire et des détenteurs périmés, l'autorisation du candidat et sa
couverture des décisions confirmées. Ancien primaire injoignable ne signifie
pas exclu ; un routage vers un nouveau serveur ou un verrou local ne suffit
pas. Faute de preuve, promotion bloquée. Le nouveau primaire doit satisfaire
le profil de durabilité avant toute nouvelle confirmation critique ; sa
promotion seule ne dispense pas des copies requises. Changement de membres,
retour d'un ancien primaire et renouvellement des mandats de signataire
sont contrôlés, sans réintégration d'une source divergente à l'écriture.

Ce choix protège les décisions de sécurité confirmées dans les pannes
couvertes et permet une reprise automatisée qualifiée. Il exige des copies
et une coordination exploitées, ajoute une attente réseau et peut bloquer
les nouveaux engagements en partition ; budgets et performances à mesurer.

Une confirmation durable sur le seul primaire ne remplace pas la garantie
du profil redondant. Sauvegardes et copies asynchrones éventuelles ne
justifient ni cette confirmation critique ni une promotion sans couverture
des décisions confirmées. Récupération/reconstruction reste autorisée et
auditée, avec réconciliation avant reprise ; aucun jeton consommé, retrait
ou version de sécurité n'est annulé pour rétablir le service.

Permissions déjà délivrées uniquement selon
A05/A10/A11c, révocation connue bloquante, pas de prolongation en partition.
Une demande de retrait non engagée reste diagnostiquée ; blocage local
conservatoire sous mandat distinct, sans prétendre à une révocation globale.
Le suivi distingue engagement durable, publication, application et reprise ;
les objectifs A05b ne changent pas. Cohérence des lectures sensibles avec
l'autorité courante, versions/tombstones et anti-rejeu conservés ; copie
en retard sans pouvoir de renouvellement. Signature et preuve reçue restent
le choix A12c, distinct du quorum de réplication ou de promotion.

Topologie, contrôleur de promotion/exclusion, mécanismes de mandat et
époque, seuils de réplication, temps d'attente, horloges, budgets WAL/disque,
RPO/RTO par périmètre et procédures de reconstruction restent à définir.
Machines physiques, VM et conteneurs sur un même hôte Proxmox ou un même
stockage ne constituent pas par défaut des domaines de panne indépendants.
Aucune modification de l'hyperviseur, des montages, droits ou services hôtes
n'est autorisée par ce choix documentaire ; rôles d'autorité qualifiés
séparément des PA Linux/Windows physiques/VM et Docker/LXC ordinaires.

Qualification : perte de primaire avant/après confirmation, réponse perdue,
attente synchrone interrompue, reprise d'outbox, perte des copies requises,
partition avec ancien primaire vivant, candidat en retard, promotion sans
copies suffisantes, retour d'un ancien membre, saturation WAL et restauration.
Aucune double admission, résurrection ou confirmation sans garantie du profil.

[PostgreSQL décrit la durabilité et l'attente de réplication synchrone](https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION)
et [l'exclusion de l'ancien primaire lors d'une bascule](https://www.postgresql.org/docs/current/warm-standby-failover.html).
Ces mécanismes ne constituent pas à eux seuls une élection sûre ; aucun
produit, version ou configuration n'est adopté. A12b, option A, est validé ;
paramètres et qualification restent à préciser, A12c/A12d A validés ; Ed25519 A12e B validé le 6 octobre 2026 pour reçus/permissions.

##### Application au PA — A12b

Profil de référence des autorités redondantes utilisant PostgreSQL A12a,
sans base/consensus imposé au PA ordinaire. Mono-instance : profil explicite
à durabilité/reprise locales, sans HA ni repli automatique vers ce profil.

L'option A validée exige conservation durable du journal sur le primaire
et les copies admissibles requises avant confirmation d'une décision
critique. Réception réseau/cache OS distant insuffisants ; copies et
domaines de panne à qualifier. Perte de copies : aucun remplacement par
une confirmation seulement locale. Attente bornée, état incertain visible ;
réponse perdue ou annulation d'attente sans preuve de rollback. Reprise
avec même opération et réconciliation, aucun jeton restitué. Présence dans
l'outbox après crash sans preuve suffisante : durabilité du profil vérifiée
avant confirmation, publication autoritative ou signature.

Bascule contrôlée automatisable après qualification : exclusion
prouvée de l'ancien primaire/détenteurs périmés, candidat autorisé couvrant
les décisions confirmées. Injoignabilité, routage ou verrou local seuls
insuffisants ; doute bloquant. Promotion sans dispense des copies requises
pour les nouveaux engagements. Retour d'ancien membre et changements de
composition contrôlés, sans écriture divergente. Ce choix protège les
décisions confirmées dans les pannes couvertes et qualifie une reprise
automatisée ; copies, coordination, attente réseau et blocage en partition
à dimensionner.

Confirmation sur le seul primaire sans substitution au profil redondant ;
sauvegardes et copies asynchrones éventuelles sans garantie suffisante
pour confirmer ou promouvoir. Reconstruction autorisée/auditée et
réconciliation avant reprise, sans rendre disponible un jeton consommé
ni annuler retraits ou versions de sécurité.

A05/A10/A11c et les objectifs A05b sont conservés, sans
prolongation des droits en partition, révocation connue bloquante. Blocage
local conservatoire mandaté distinct d'une révocation globale engagée.
Lectures sensibles sous autorité courante, copies en retard non décisionnelles,
audit/versions/tombstones conservés ; engagement, publication et application
suivis séparément. A12c/A12d A validés ; Ed25519 A12e B validé le 6 octobre 2026 pour reçus/permissions.

Contrôleur d'exclusion/promotion, mandats/époques, copies/seuils, délais,
WAL/disque, RPO/RTO, topologie et reconstruction à définir. VM/conteneurs
sur un même hôte Proxmox ou stockage sans indépendance de panne présumée.
Pas de droits, montages ou accès hyperviseur implicites. Qualification des
rôles d'autorité distincte du PA ordinaire sur les cibles autorisées : crash,
réponse perdue, attente interrompue/outbox, partition, deux primaires,
candidat en retard, retour de membre, saturation et restauration, sans
réactivation des accès ou consommation double. Sources dans le cadrage PZT ;
A12b, option A, est validé ; paramètres et qualification restent à préciser,
A12c/A12d A validés ; Ed25519 A12e B validé le 6 octobre 2026 pour reçus/permissions.

#### Scenario: Conformité du traitement A12b

- **WHEN** un profil revendique le traitement A12b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e3c2e56efb

Source : `openspec/specs/pzt/spec.md`, ligne 12605. SHA-256 du bloc : `7d646ff4c15fe24de342edd5e55ae6f5a0417df7f9d22630e57448ad4441ab43`.

~~~~text
### Requirement: Contrat A12c — Signataires et preuves d'engagement — option A validée le 5 octobre 2026

Le rôle chargé du traitement A12c MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12c

Le choix fixe qui signe une décision d'autorité et comment le destinataire
vérifie son origine, sa portée et son rattachement à l'engagement A12a/A12b.
Il ne remplace pas les contrôles Django, A05/A10 ni les exigences de
réplication. Quorum de conservation des données, permission de promotion
et seuil de signataires sont trois conditions distinctes.

Chaque membre signataire possède une
identité, une clé de signature opérationnelle propre et un certificat
X.509 dédié sous la chaîne PZT configurée, avec usages et délégation
bornés. Signature opérationnelle, émission de certificats, identité TLS,
WireGuard et attestation TPM conservent clés/rôles distincts ; certificat
de signataire sans pouvoir implicite d'émettre des certificats ou de
déléguer. La clé racine reste protégée hors de la signature courante,
sans réplication privée ordinaire dans PostgreSQL ni copie par membre.
Protection, sauvegarde et éventuel HSM/TPM suivent un profil à qualifier ;
aucun équipement, mode hors ligne ou privilège hôte imposé ici.

L'option A validée accepte une signature opérationnelle d'un membre
actuellement habilité pour la décision et son périmètre. Le signataire
vérifie l'engagement durable A12b, la version/époque autorisée et son
mandat courant avant émission ; perte de mandat ou engagement invérifiable
bloque la signature nouvelle. Plusieurs membres peuvent signer selon leur
rôle, sans partager leur clé ni décider indépendamment de PostgreSQL.
Ce choix retient une chaîne de vérification simple et une gestion de
clés par membre, sans collecte de cosignatures. Il repose sur la confiance
dans le signataire habilité et sa chaîne : une
clé compromise peut produire une fausse affirmation signée dans la portée
de confiance acceptée avant détection/retrait. Aucune tolérance à un
signataire malveillant ni preuve cryptographique publique du commit
PostgreSQL n'est revendiquée par A.

Aucune collecte obligatoire de cosignatures ni signature agrégée à seuil
n'est retenue pour ce socle. Le quorum de réplication A12b ne devient pas
un seuil de signatures ; clé racine partagée et consensus byzantin ne
sont pas introduits. Plusieurs clés du même membre ne constituent pas
des signataires indépendants, notamment après clone ou restauration.

Le reçu est typé/versionné et lie intégralement la décision :
autorité logique, membre signataire, opération/génération, empreinte des octets,
tenant/scope, usage/destinataire, mandat et version de politique, époque
courante, référence d'engagement, émission, expiration et retrait.
Les champs déterminants sont protégés par signature, sans identifiant WAL
ou drapeau « quorum atteint » accepté comme preuve autonome. Le reçu est
une affirmation signée du signataire sur l'engagement ; le PA ne
lit pas PostgreSQL et ne peut pas déduire le commit de la seule signature.
Une vérification en ligne requise consulte le contrat autorisé d'autorité ;
réutilisation seulement dans la validité/fraîcheur du profil A05, avec
contrôles A10 et révocations connues. Un reçu ancien n'accorde aucun accès
si une condition courante n'est plus vérifiable.

Vérification : ancrage configuré, chaîne/usages/validité/révocation,
mandat de signataire, contexte, destinataire, octets exacts, algorithme
admis, versions/époque et anti-rejeu. Certificat reçu, découverte ou URL de
clé sans création d'ancrage. La signature authentifie une assertion, pas
l'état appliqué au PA : admission/permission/signature et exécution restent
suivies séparément. Reprise idempotente d'une émission sur le même objet,
sans reconstruire une autre décision ni prolonger droits ou échéances.

Retrait/compromission d'un membre invalide ses mandats et les assertions
concernées selon leur portée, avec réévaluation des accès dérivés et audit
sans secret ; une décision engagée peut être réémise par un signataire
admissible seulement après revalidation actuelle. Rotation, changement
d'époque et restauration ne restaurent aucune ancienne confiance. La
procédure de récupération de racine ou de délégation compromise et ses
impacts sont explicitement déclarés, sans nouvelle racine apprise en réseau.

Formats des reçus et permissions, signature des références A10f, profils
X.509, algorithmes, octets protégés, durées, statut de révocation, protection
des clés restent à spécifier. A12d A validé le 6 octobre 2026 retient
JSON/JWS compact pour reçus et permissions ; Ed25519 A12e B validé le 6 octobre 2026.
A10b conserve sa liaison WireGuard JWS distincte. Les autres objets
conservent leurs propres arbitrages de format. Qualification sur chaque rôle/plateforme : faux signataire, mandat
périmé, décision non engagée, mauvais scope/époque, altération, signature
manquante, doublons, compromission, rotation, partition et replay.

[X.509 décrit les usages et la validation de chaîne](https://www.rfc-editor.org/rfc/rfc5280.html#section-6)
et [JWS les signatures et leurs sérialisations](https://www.rfc-editor.org/rfc/rfc7515.html#section-7),
comme références de format, sans prouver l'engagement PostgreSQL ou imposer
un format de reçu. A12c, option A, est validé ; paramètres et qualification
restent à préciser. A12d A validé le 6 octobre 2026 ; Ed25519 A12e B validé le 6 octobre 2026.

##### Application au PA — A12c

Origine/portée et rattachement d'une décision à A12a/A12b, sans remplacer
Django, A05/A10 ou la réplication. Copies durables, autorisation de promotion
et nombre de signataires restent distincts.

Chaque signataire possède une identité/clé opérationnelle propre
et un certificat X.509 dédié, sous chaîne PZT configurée,
usages et délégation bornés ; aucun pouvoir implicite d'émettre un certificat.
Clés/rôles de signature, certification, TLS, WireGuard et attestation distincts.
Racine protégée hors signature courante, sans clé partagée ou réplication
privée ordinaire dans PostgreSQL. Protection/sauvegarde/HSM/TPM à qualifier,
sans équipement, privilège ou mode hors ligne implicite.

L'option A validée accepte une signature de membre actuellement habilité
pour la portée, après contrôle de l'engagement durable, version/époque et
mandat. Doute/perte de mandat : aucune signature nouvelle. Plusieurs membres
possibles sans clé commune ni décision indépendante de la source.
Vérification simple sans collecte de cosignatures ;
confiance dans le signataire requise, clé compromise susceptible de produire
une fausse assertion avant retrait. Aucune tolérance à un signataire
malveillant ni preuve publique du commit PostgreSQL par la seule signature.

Cosignatures obligatoires ou signature agrégée à seuil non retenues pour
le socle. Quorum A12b distinct du nombre de signatures ; aucune clé racine
partagée ou consensus byzantin introduit. Plusieurs clés/clones d'un même
membre ne prouvent aucune indépendance des signataires.

Reçu typé/versionné lié à décision/empreinte, opération/génération,
autorité/membre signataire, scope, destinataire/usage, mandat/politique, époque,
engagement, validité et retrait ; champs déterminants signés. Identifiant
WAL ou drapeau quorum sans valeur de preuve autonome. Affirmation signée,
sans lecture SQL du PA ni preuve de commit déduite de la seule signature.
Vérification en ligne si requise via contrat autorisé ; réutilisation dans
validité/fraîcheur A05, preuves A10 et révocations, sans droit automatique.

Chaîne/usages/ancrage, mandats, octets, algorithmes, scope/époque et anti-rejeu
vérifiés ; clé/URL reçue sans ancrage nouveau. Signature distincte de preuve
d'application locale ; émission idempotente sans prolongation. Compromission
ou retrait invalide les mandats/assertions concernés et réévalue les accès
avec audit ; réémission seulement sur décision encore valide recontrôlée.
Rotation/restauration sans ancienne confiance rétablie ; récupération de
racine/délégation à spécifier, sans racine apprise implicitement en réseau.

Formats/algorithmes, profils, durées, révocation et clés à définir ;
A12d A validé le 6 octobre 2026 : reçus/permissions JSON signés JWS compact,
Ed25519 A12e B validé le 6 octobre 2026 ; liaison WireGuard A10b distincte.
Qualification : signataire/mandat/époque invalides, faux engagement, octets
altérés, signatures manquantes ou doublons, partition, rotation,
compromission et restauration sur les rôles/cibles autorisés. Sources dans
le cadrage PZT. A12c, option A, est validé ; paramètres et qualification restent
à préciser. A12d A validé le 6 octobre 2026 ; Ed25519 A12e B validé le 6 octobre 2026.

#### Scenario: Conformité du traitement A12c

- **WHEN** un profil revendique le traitement A12c et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--8fb2c433db

Source : `openspec/specs/pzt/spec.md`, ligne 12755. SHA-256 du bloc : `f912e77cf71abcef3705743d364ecf8d6c06b0fac541b5c757786c8e67de637a`.

~~~~text
### Requirement: Contrat A12d — Format des reçus et permissions PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A12d MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12d

Le choix porte sur les reçus d'autorité A12c et les permissions de
communication PZT A05. Une signature opérationnelle habilitée par objet,
engagement durable A12b et vérifications de confiance A12c restent requis.
Un reçu d'engagement ne vaut pas permission de communiquer ; les types,
usages, destinataires et règles de vérification sont distincts et explicites.
Aucun reçu, certificat ou format valide ne dispense d'une autorisation.

L'option A validée utilise un contenu JSON UTF-8 typé/versionné signé
asymétriquement en JWS, sérialisation compacte à contenu embarqué et une
signature. En-têtes déterminants protégés et charge liée au type, usage,
scope/destinataire, mandat, époque, version, validité et retrait requis.
Le vérificateur utilise les octets signés reçus, sans réencoder le JSON
pour valider la signature ni inventer une canonicalisation cryptographique.
JWS ne choisit pas JWT : les schémas PZT et leur sémantique sont propres
aux contrats. Transmission par corps/enveloppe autorisée A07, sans secret
ou permission sensible dans URL, arguments ou journaux.

Ce choix réutilise JSON/JWS déjà retenus en A07/A10b et limite les codecs
nécessaires sur PA et PBO. Cette cohérence ne présume
ni bibliothèque déjà implémentée ni gain CPU/RAM ; taille des objets et
coût de vérification restent à mesurer sur les profils qualifiés.

CBOR/COSE n'est pas retenu pour ces reçus et permissions. Les schémas
JSON, usages et contrôles restent distincts des cartes/deltas A07 et de
la liaison WireGuard A10b, sans parser binaire supplémentaire imposé.

Le profil de signature asymétrique est fermé :
algorithmes et clés configurés par usage, type/version et références de
clé protégés, aucune signature absente ou MAC partagé aux vérificateurs.
Algorithme « none », confusion de type, clé non habilitée, champ obligatoire
inconnu, doublons de clés JSON, encodage ambigu ou dépassement des
limites sont refusés. Les champs extérieurs non signés ne modifient pas
la décision ; clé/certificat/URL reçus sans nouvelle confiance implicite.
Analyse des entrées bornée, avant et après vérification, sans usage du
contenu métier avant validation cryptographique et des contrôles courants.

Émission/reprise lie l'objet aux états durables A12a/A12b, à son identifiant
et aux octets protégés ; doublon sans double effet ou extension de validité.
Un reçu ou une permission restaurés ne réintroduisent pas un mandat retiré.
Cache/réutilisation restent bornés par A05/A10, révocations et époque
courantes. Compromission du signataire conserve les limites de confiance
A12c : le format ne transforme pas une assertion en preuve publique du commit.

Ni chiffrement applicatif supplémentaire, jeton d'enrôlement A11b, format
de preuve TPM, schéma des manifestes A10f ni format des cartes/deltas A07
n'est choisi par A12d. Les canaux PZT gardent leurs protections existantes ;
signature ne rend pas publique une permission sensible. Identifiants de
type, schémas, algorithmes, profil de certificat, durées et tailles restent
à définir. Bibliothèques/versions non adoptées ; qualification sur les
PA physiques/VM Linux/Windows, Docker/LXC Proxmox et rôles PBO concernés :
altération, confusion reçu/permission/liaison WireGuard, mauvais contexte,
clé/type/algorithme invalide, doublons, tailles extrêmes et replay.

[JWS définit la sérialisation compacte](https://www.rfc-editor.org/rfc/rfc7515.html#section-3.1).
Ce format encadre la signature, sans déterminer les droits ou la preuve
d'engagement PZT. A12d, option A, est validé le 6 octobre 2026 ; schémas,
durées et tailles restent à préciser, Ed25519 A12e B validé le 6 octobre 2026.

##### Application au PA — A12d

Reçus A12c et permissions de communication A05, avec une signature
habilitée et engagement durable A12b. Reçu et permission ont types/usages
et contrôles distincts ; format ou signature valide sans autorisation
supplémentaire.

L'option A validée utilise JSON UTF-8 typé/versionné signé asymétriquement
en JWS compact, contenu embarqué et une signature, en-têtes déterminants
protégés. Vérification sur octets signés reçus, sans réencodage JSON ni
canonicalisation inventée. Schémas PZT sans JWT implicite ; transport par
corps/enveloppe A07, sans URL/arguments/journaux exposés. Ce choix réutilise
JSON/JWS A07/A10b et limite les codecs, sans gain CPU/RAM présumé.

CBOR/COSE non retenu pour ces objets, sans parser binaire supplémentaire
imposé ; cartes/deltas A07 et liaison WireGuard A10b restent distincts.

Profils fermés par usage, clés/algorithmes/type et
version protégés, aucun MAC partagé/« none »/signature absente ; refus des
confusions de type, clés non habilitées, doublons JSON, champs
obligatoires inconnus, ambiguïtés ou dépassements de limites. Champs
extérieurs non signés sans effet sur la décision, URL/certificat reçus
sans confiance nouvelle. Parse borné avant/après signature, usage métier
seulement après contrôles cryptographiques et conditions courantes.

Identifiant, engagement durable et octets liés à l'émission/reprise ;
doublon sans effet ou validité prolongée, restauration sans mandat retiré
réintroduit. A05/A10/révocation/époque gouvernent cache et réutilisation ;
format sans preuve publique du commit, confiance A12c inchangée.

TPM, jetons A11b, manifestes A10f, cartes/deltas A07 et chiffrement
applicatif supplémentaire non choisis ici. Schémas, identifiants de type,
algorithmes, profils, durées, tailles, bibliothèques/versions à qualifier
sur toutes les cibles PA et rôles PBO concernés : altération, confusion
de types, contexte/clé/algorithme invalides, doublons, dépassements et replay.
Sources dans le cadrage PZT. A12d, option A, est validé le 6 octobre 2026 ;
schémas, durées et tailles à préciser, Ed25519 A12e B validé le 6 octobre 2026.

#### Scenario: Conformité du traitement A12d

- **WHEN** un profil revendique le traitement A12d et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--fdd6745e11

Source : `openspec/specs/pzt/spec.md`, ligne 12867. SHA-256 du bloc : `de9bc3ca2bd7b559fa21e530ce1053c4da42622adc644e841c4e26513e16c199`.

~~~~text
### Requirement: Contrat A12e — Algorithme des reçus et permissions PZT — option B validée le 6 octobre 2026

Le rôle chargé du traitement A12e MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12e

L'option B validée retient Ed25519 pour les signatures opérationnelles JWS
A12d des reçus d'autorité et permissions PZT. Clés distinctes A12c, ancrages,
mandats, engagement durable et contrôles d'autorisation restent requis.
Ce choix ne fixe pas les algorithmes des CA, de TLS, des preuves TPM,
des manifestes A10f ou de la liaison WireGuard A10b.

L'identifiant JOSE entièrement spécifié de l'en-tête protégé `alg` est
`Ed25519`, selon RFC 9864. Le profil utilise Ed25519 pur de RFC 8032,
sans substitution par `EdDSA`, Ed448, Ed25519ph, Ed25519ctx ou X25519.
Les bibliothèques JOSE, providers, clés publiques des certificats
opérationnels et vérificateurs doivent être qualifiés pour ce profil exact.
Le profil X.509 Ed25519 suit RFC 8410 ; sa validation reste celle d'A12c,
sans imposer Ed25519 comme algorithme de signature des CA.

Signature normalisée Ed25519 de 64 octets, encodée dans JWS compact ;
pas de conversion ECDSA R/S ou de signature ASN.1 DER substituée.
Génération des clés avec aléa cryptographique sûr et signature via une
bibliothèque/provider éprouvé ; aucune cryptographie maison. Le nonce
déterministe de signature ne dispense pas de protéger la clé ni de
qualifier la résistance de l'implémentation aux canaux auxiliaires.
Les clés X25519 de WireGuard et les clés d'attestation TPM restent séparées.

Profil autorisé par usage depuis une configuration approuvée, sans
négociation depuis un message non fiable. Clé, certificat, type d'objet et
algorithme permis sont liés et vérifiés ; un `alg` signé ou une clé reçue
ne crée pas une habilitation. Algorithme inconnu/non autorisé, MAC,
« none », clé incompatible, signature invalide ou provider incapable :
refus, sans repli automatique vers ES256 ou l'identifiant générique EdDSA.
Une migration future requiert politique/version approuvées, activation et
retrait bornés, sans conversion d'une assertion reçue en autre signature.

L'identifiant d'opération et la version/empreinte de l'objet protégé,
non les seuls octets de signature, déterminent l'idempotence et l'anti-rejeu.
Une nouvelle signature du même contenu ne renouvelle ni le mandat ni sa
validité. Rotation/révocation des clés et récupération suivent A12c/A05/A10 ;
la signature ne prouve pas à elle seule le commit PostgreSQL.

B vise un profil logiciel performant et robuste ; aucun gain CPU/RAM,
débit, énergie ou niveau de protection supérieur à ES256 n'est garanti.
Signature côté autorité et vérification côté PA sont mesurées séparément,
avec messages et charges comparables : CPU, mémoire, latence, débit,
initialisation des clés et taille totale JWS/certificats. Les signatures
seules font 64 octets dans les deux profils comparés. Ce choix ne modifie
pas le coût du chiffrement WireGuard du trafic.

Bibliothèques, versions, génération/protection des clés, profils X.509,
paramètres de migration et budgets restent à préciser. Qualification des
signataires et vérificateurs sur les rôles réellement exécutés :
Linux/Windows physiques/VM, Docker/LXC Proxmox et PBO concernés ; vecteurs
valides/invalides, interopérabilité de `alg`, encodages/longueurs,
clés/types/algorithmes contradictoires, provider absent, clone, rotation,
révocation et replay. Aucun TPM, HSM, vTPM ou provider Windows/Linux n'est
présumé compatible ; aucun nouvel OS, privilège hôte ou conformité implicite.
A12f A validé le 6 octobre 2026 : profils logiciels protégés ou matériels
selon politique approuvée ; A12g A validé le 6 octobre 2026 : nouvelle clé et reprovisionnement autorisé
après perte, sans restauration de sauvegarde de la clé privée opérationnelle.

[RFC 9864 définit l'identifiant JOSE Ed25519](https://www.rfc-editor.org/rfc/rfc9864.html#section-2.2),
[RFC 8032 définit Ed25519](https://www.rfc-editor.org/rfc/rfc8032.html#section-5.1)
et [RFC 8410 son profil X.509](https://www.rfc-editor.org/rfc/rfc8410.html).
Ces références ne qualifient aucun provider PZT. A12e, option B, est validé
le 6 octobre 2026 ; paramètres et qualification restent à préciser.

##### Application au PA — A12e

L'option B validée retient Ed25519 pour les signatures opérationnelles JWS
A12d des reçus/permissions seulement. CA, TLS, TPM, manifestes A10f et
liaison WireGuard A10b conservent leurs arbitrages. Clés distinctes,
engagement durable et contrôles A12c/A05/A10 maintenus.

`alg` protégé égal à `Ed25519` selon RFC 9864, Ed25519 pur RFC 8032 ;
sans substitution EdDSA générique, Ed448, Ed25519ph/ctx ou X25519.
Bibliothèques JOSE/providers/vérificateurs et clé publique du certificat
compatibles, profil X.509 RFC 8410 sans algorithme de CA imposé.
Signature Ed25519 de 64 octets encodée JWS, sans conversion ECDSA/DER.
Génération des clés avec aléa sûr, bibliothèque/provider éprouvé, pas de
cryptographie maison ; nonce déterministe sans dispense de protection
contre extraction/canaux auxiliaires. Aucune réutilisation de clé WG/TPM.

Profil autorisé par usage depuis configuration approuvée, sans négociation
non fiable. Clé/certificat/type/algorithme liés ; `alg` ou clé reçus sans
habilitation nouvelle. Inconnu/non autorisé, MAC, « none », mauvaise clé,
signature invalide ou provider absent : refus sans repli ES256/EdDSA.
Migration approuvée/versionnée et bornée, sans resigner pour convertir.
Idempotence liée à opération, version et empreinte de l'objet protégé,
sans identité fondée sur les seuls octets de signature. Signature nouvelle
sans validité prolongée ni preuve publique du commit PostgreSQL.

B vise performance/robustesse logicielles sans gain garanti. Mesures
séparées signature autorité/vérification PA, à messages/charges comparables :
CPU, RAM, latence, débit, initialisation, taille JWS/certificats ; signature
seule de 64 octets comme ES256, coût du chiffrement WireGuard inchangé.
Bibliothèques/versions, clés, profils, migration et budgets à préciser.
Qualification par rôle/cible Linux/Windows physique/VM, Docker/LXC Proxmox,
PBO : vecteurs, identifiant JOSE, encodages/longueurs, clés/types/algorithmes
contradictoires, provider absent, clone, rotation, révocation et replay ;
sans support matériel, OS, droit ou conformité implicite. A12f A validé
le 6 octobre 2026 : profils logiciels protégés ou matériels selon politique ;
A12g A validé le 6 octobre 2026 : nouvelle clé et reprovisionnement autorisé après perte. Sources dans le cadrage PZT. A12e B validé
le 6 octobre 2026 ; paramètres et qualification restent à préciser.

#### Scenario: Conformité du traitement A12e

- **WHEN** un profil revendique le traitement A12e et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--4239a47c84

Source : `openspec/specs/pzt/spec.md`, ligne 12984. SHA-256 du bloc : `06b1a0a9b40f70185fb9aa14452edd9031ff3c23abd566e3d433c41912d9432d`.

~~~~text
### Requirement: Contrat A12f — Protection des clés des signataires opérationnels — option A validée le 6 octobre 2026

Le rôle chargé du traitement A12f MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12f

L'option A validée retient des profils explicites de protection des clés
privées Ed25519 A12e des signataires de reçus et permissions A12c/A12d,
selon les rôles effectivement déployés : logiciel protégé autorisé par la
politique du périmètre, ou matériel non exportable exigé par cette politique.
Aucun rôle de signature d'autorité n'est imposé au PA uniquement vérificateur.
Attestation TPM A10d et arbitrages des clés CA, TLS, WireGuard, TPM et
manifestes restent distincts.

Le profil logiciel exige isolation du signataire, accès limité à son
identité de workload, secrets hors sources/images/configuration métier et
journaux, références de secrets autorisées et protection au repos avec
mécanisme de déverrouillage à qualifier. Clés individuelles par signataire,
pas de clé commune copiée entre membres ou héritée d'une image/clonage.
La clé utilisée en logiciel reste exposée à un processus ou hôte compromis ;
ce profil ne promet pas la non-exportabilité matérielle.

Le profil matériel exige un provider réellement qualifié pour Ed25519,
JWS et la protection non exportable de la clé concernée. Le profil est
déclaré, approuvé et lié au mandat du signataire, jamais déduit de son OS,
d'un conteneur ou d'une preuve TPM. Besoin matériel non satisfait :
blocage de la signature, sans repli logiciel ni changement d'algorithme.
Le matériel n'est pas obligatoire pour tous les signataires de production ;
son affectation dépend de la politique approuvée, sans auto-abaissement.

Une VM/vTPM n'est pas réputée équivalente à un TPM physique ; une attestation
hôte ne transforme pas une clé logicielle de conteneur en clé matérielle.
Docker/LXC n'obtiennent ni périphérique, montage, privilège ou accès Proxmox
implicite. Un service de signature hors de leur frontière utilise un
contrat PZT autorisé ; aucune communication PBO–PA ne contourne PZT.

La non-exportabilité ne suffit pas à empêcher un processus compromis
habilité de demander une fausse signature : A12c, engagement/mandat/époque,
contrôles d'accès, révocation et audit restent nécessaires. Échec du
provider : pas de confirmation signée nouvelle ; droits antérieurs bornés
par A05/A10. Rotation et reprise utilisent clés/mandats admissibles,
sans restaurer une ancienne habilitation ou partager une clé retirée.

Providers, politiques d'affectation, stockage/déverrouillage, sauvegarde,
récupération, topologie et budgets restent à préciser ; qualification
Ed25519/JWS/X.509, droits, clones, panne, rotation/révocation/reprise,
CPU/RAM et latence requise. PA uniquement vérificateur sans clé privée
d'autorité ; aucun gain de ressources chiffré ni protection matérielle
universelle présumés. A12f, option A, est validé le 6 octobre 2026 ;
A12g A validé le 6 octobre 2026 : nouvelle clé et reprovisionnement autorisé
après perte, sans restauration de sauvegarde de la clé privée opérationnelle.

##### Application au PA — A12f

L'option A validée retient des profils approuvés par périmètre pour les
clés privées Ed25519 des signataires de reçus/permissions A12c–A12e :
logiciel protégé autorisé, ou matériel non exportable exigé selon politique.
Aucun rôle ni clé privée d'autorité imposés au PA uniquement vérificateur ;
attestation TPM A10d et arbitrages des autres clés maintenus.

Logiciel : signataire isolé, accès réservé à son workload, références de
secrets autorisées, secrets hors sources/images/configuration métier et
journaux, protection au repos et déverrouillage à qualifier ; clé
individuelle sans copie entre membres ni héritage d'image/clone. Risque
d'extraction par processus/hôte compromis, sans non-exportabilité promise.
Matériel : provider qualifié Ed25519/JWS et protection non exportable réelle.
Profil déclaré/approuvé et lié au mandat, sans déduction depuis OS,
conteneur ou preuve TPM. Matériel exigé mais absent/incompatible : blocage
sans repli logiciel ou autre algorithme ; affectation par politique approuvée,
sans obligation matérielle universelle ni auto-abaissement.

Aucune équivalence présumée TPM physique/vTPM ou transformation de clé
logicielle par attestation hôte. Aucun montage, device, privilège ou accès
Proxmox implicite ; service de signature externe par contrat PZT autorisé,
sans contournement PBO–PA. Non-exportabilité sans protection complète contre
usage frauduleux par un processus compromis ; engagement, habilitation,
époque, révocation et audit A12c maintenus. Provider absent sans confirmation
signée nouvelle ; anciens droits bornés A05/A10. Rotation/reprise sans
ancienne habilitation restaurée ni clé retirée partagée.

Providers, affectation, stockage/déverrouillage, sauvegarde/récupération,
topologie et budgets à préciser ; qualification Ed25519/JWS/X.509, droits,
clones, panne, rotation/révocation/reprise, CPU/RAM/latence à prévoir,
sans gain chiffré garanti. A12f, option A, est validé le 6 octobre 2026 ;
A12g A validé le 6 octobre 2026 : nouvelle clé et reprovisionnement autorisé
après perte, sans restauration de sauvegarde de la clé privée opérationnelle.

#### Scenario: Conformité du traitement A12f

- **WHEN** un profil revendique le traitement A12f et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--8ee789ff3b

Source : `openspec/specs/pzt/spec.md`, ligne 13081. SHA-256 du bloc : `28ac5da9b4e072f6ac880ac2c487507a553e0c20985358a4622f6a926a2a746d`.

~~~~text
### Requirement: Contrat A12g — Reprise après perte des clés opérationnelles — option A validée le 6 octobre 2026

Le rôle chargé du traitement A12g MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A12g

L'option A validée retient une nouvelle clé individuelle et son
reprovisionnement autorisé après perte définitive/corruption de la clé
privée ou remplacement déclaré du signataire de reçus/permissions A12c–A12f.
Un redémarrage normal avec clé protégée intacte et contexte courant
vérifiable ne déclenche pas une rotation à chaque démarrage. CA/racines,
TLS, WireGuard, TPM et manifestes conservent leurs plans propres ; la
sauvegarde des données PostgreSQL reste requise et distincte.

La reprise n'utilise pas une sauvegarde de l'ancienne clé privée
opérationnelle pour rétablir la signature ; ce mécanisme n'est pas retenu.
La persistance protégée nécessaire au fonctionnement normal suit A12f.
Un autre signataire admissible peut assurer le service avec sa propre clé
et son mandat A12c, sans copie de la clé perdue entre membres.

Nouvelle clé, certificat et mandat ne sont utilisables qu'après contrôles
actuels et engagement par l'autorité compétente ; aucune auto-certification,
racine apprise en réseau ou permission déduite d'un ancien reçu.
Admission/preuves A02/A10 et mandat A11 applicables au rôle restent requis ;
le reprovisionnement peut être automatisé dans un mandat explicite valide,
sans nouvelle identité, délégation ou capacité métier implicitement accordée.
Retrait de l'ancienne habilitation et traitement des décisions/permissions
dérivées suivent A12c/A05, sans résurrection ni double détenteur autorisé
par la seule possession d'une clé. Clé révoquée, expirée, compromise ou
suspecte jamais réactivée ; nouvelle génération selon le rôle déclaré.
La reprise attend l'autorité disponible ou un membre déjà admissible ;
aucun secours permissif et aucun délai de reprise garanti.

Engagement A12b, idempotence, anti-rejeu, preuves/fraîcheur A10 et durées A05
restent opposables. Restauration de configuration ou de base sans mandat
retiré, ancien profil ou génération réintroduits ; image, clone ou nouvelle
instance sans héritage d'une clé opérationnelle ni admission implicite.
Les clés/certificats publics et preuves nécessaires à l'audit peuvent être
conservés sous gouvernance, sans permettre de nouvelles signatures ni
un accès métier après expiration/révocation. Un PA uniquement vérificateur
ne reçoit pas de clé privée d'autorité pour participer à cette reprise.

Contrats, durées de rotation, qualification du provider, procédures de
provisionnement/retrait, continuité, dépendances et budgets restent à préciser.
Recette : perte/corruption, redémarrage normal, clone, restauration obsolète,
compromission, provider/autorité absents et réémission idempotente ; aucun
gain CPU/RAM courant ou RTO chiffré présumé.

[Le NIST traite séparément sauvegarde et récupération des clés de signature](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
(sections 8.2.2.1 et B.3.1.1) ; référence de gestion, sans adoption de
conformité ou de durées NIST. A12g, option A, est validé le 6 octobre 2026 ;
paramètres et qualification restent à préciser.

##### Application au PA — A12g

L'option A validée retient une nouvelle clé individuelle et son
reprovisionnement autorisé après perte définitive/corruption de la clé
privée ou remplacement déclaré du signataire de reçus/permissions A12c–A12f.
Redémarrage normal avec clé protégée intacte/contexte courant vérifiable
sans rotation à chaque démarrage. Plans CA/racines, TLS, WG, TPM, manifestes
et sauvegarde PostgreSQL distincts ; persistance protégée A12f maintenue.

Pas de restauration d'une sauvegarde de l'ancienne clé privée opérationnelle
pour rétablir la signature. Autre membre admissible avec sa propre clé et
son mandat possible, sans partage de la clé perdue. Certificat, mandat,
preuves actuelles et engagement par autorité compétente avant usage,
sans auto-certification ou ancien reçu donnant accès ; A02/A10/A11 selon
rôle. Automatisation sous mandat explicite courant possible, sans nouvelle
identité, délégation ou capacité implicitement accordée. Ancienne habilitation
et droits dérivés traités selon A12c/A05 ; clé révoquée/expirée/compromise/
suspecte jamais réactivée, sans double détenteur autorisé ni résurrection.
Autorité indisponible sans membre admissible : attente bloquante, sans
secours permissif ou délai de reprise garanti.

Engagement/idempotence A12b, anti-rejeu, fraîcheur A10 et durées A05 conservés ;
restauration de base/configuration sans ancienne habilitation, profil ou
génération réintroduits. Image/clone/nouvelle instance sans héritage de clé
ni admission implicite. Conservation gouvernée des clés/certificats publics
et preuves d'audit sans nouvelle signature ni autorisation après retrait.
PA uniquement vérificateur sans clé privée d'autorité imposée pour la reprise.
Contrats, durées, provider, provisionnement/retrait, continuité/dépendances
et budgets à préciser ; recette perte/corruption, redémarrage normal, clone,
restauration obsolète, compromission, indisponibilité et réémission idempotente ;
sans gain CPU/RAM courant ou RTO garanti. Référence NIST dans le cadrage PZT,
sans conformité implicite. A12g, option A, est validé le 6 octobre 2026 ;
paramètres et qualification restent à préciser.

#### Scenario: Conformité du traitement A12g

- **WHEN** un profil revendique le traitement A12g et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

