# Références normatives — Z23

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 11099 | [Contrat A10i109 — Réarmement d'incident de manifeste par commande PBO d'opérateur habilité — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11099) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11147 | [Contrat A10i110 — Original de manifeste protégé, incident marqué hors document sans copie automatique — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11147) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11193 | [Contrat A10i111 — Alerte d'intégrité persistante avec transitions, sans rappel périodique — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11193) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11239 | [Contrat A10i112 — Preuves du réarmement liées à un dossier de contrôle structuré et versionné — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11239) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11285 | [Contrat A10i113 — Commande de réarmement bornée à 60 secondes globales après admission serveur — option B validée le 9 octobre 2026](../../specs/pzt/spec.md#L11285) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11333 | [Contrat A10i114 — Réarmement refusé sur version d'incident obsolète, nouvelle soumission explicite — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11333) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11379 | [Contrat A10i115 — Réarmement limité à une commande active par autorité, sans file — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11379) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11424 | [Contrat A10i116 — Dossier de contrôle de réarmement en JSON UTF-8 fermé et JCS qualifié — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11424) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11475 | [Contrat A10i117 — Dossier de contrôle de réarmement plafonné à 64 Kio par version — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11475) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11521 | [Contrat A10i118 — Dossier de contrôle lié par SHA-384 entière et Base64url externe auditée — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11521) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11581 | [Contrat A10i119 — Complexité du dossier JSON plafonnée à 8 niveaux, 32 membres et 64 éléments — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11581) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11626 | [Contrat A10i120 — Conservation du dossier de réarmement liée aux durées et holds de l'audit — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11626) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11673 | [Contrat A10i121 — Engagement atomique de l'état de réarmement et de ses références — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11673) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11722 | [Contrat A10i122 — Vérification du dossier de réarmement à chaque usage — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11722) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--5a0b413ff8

Source : `openspec/specs/pzt/spec.md`, ligne 11099. SHA-256 du bloc : `e688f696a1bc85b58b24ad563023b48d57010641d672d4ffc351b8c883721fa0`.

~~~~text
### Requirement: Contrat A10i109 — Réarmement d'incident de manifeste par commande PBO d'opérateur habilité — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i109 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i109

Blocage A10i108 A, revalidation A10i105 A, autorité Django et audit requis
conservés. Mode de réarmement indépendant du traitement des artefacts A10i110
et du rappel d'alerte A10i111 ; aucun réessai technique A10i89 sur erreur d'intégrité.

| Choix validé | Réarmement après anomalie | Conséquence |
| --- | --- | --- |
| A | Commande explicite PBO par opérateur habilité, diagnostic et preuves courantes requis | Contrôle humain du périmètre, aucun réarmement automatique |

Identité/contexte/action/périmètre autorisés côté Django, aucune permission
déduite du titre d'administrateur. Diagnostic, cause/confinement, manifeste
original et référence admissibles, audit/source de vérité/provider et exclusion
d'ancien acteur vérifiés ; commande/résultat persistants/corrélés/idempotents.
Procédure automatisée préautorisée B non retenue comme mode alternatif ;
preuve ou commande manquante sans levée implicite de blocage.
Commun : aucun réarmement pour seul redémarrage, temps écoulé, ACK tardif ou
hash désormais égal après contenu réécrit ; toute restauration/provenance/
version/référence contrôlée. Effets inconnus réconciliés, budgets/tentatives/
bail/holds/mandat jamais réinitialisés ou élargis par levée de blocage.
Portée exacte et conditions courantes, blocage global sans levée partielle
présumée suffisante pour dépendances communes non fiables. Nouveau travail
ultérieur seulement sous autorisation valide, aucune purge déclenchée implicitement
par la commande ni ancien Job expiré remis à RUNNING avec 60 s supplémentaires.
Audit individuel des lectures/actions PBO et réarmement persistant obligatoire,
échec fermé si audit requis indisponible ; incident/manifestes historiques conservés.
A validée pour incident d'intégrité. A10i22 B racine et autres réarmements techniques sans nouvelle
portée déduite. Dossier A10i112 A, délai global 60 s A10i113 B et refus de version obsolète
A10i114 A validés le 9 octobre 2026. Aucun clic/commande/réarmement,
purge ou OpenSpec exécutés/modifiés.
Recette : opérateur non habilité, commande dupliquée, cause inconnue, source
réparée sans preuve, acteur encore actif, audit indisponible et mandat expiré.
A10i109 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i109

- **WHEN** un profil revendique le traitement A10i109 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--4875534343

Source : `openspec/specs/pzt/spec.md`, ligne 11147. SHA-256 du bloc : `3a5680325ae87fcf457995f0ee1363109136c257a1f6582f9a01b0a67b2efce0`.

~~~~text
### Requirement: Contrat A10i110 — Original de manifeste protégé, incident marqué hors document sans copie automatique — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i110 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i110

Blocage A10i108 A, octets immuables et conservation d'audit A10i107 A conservés.
Gestion d'artefacts indépendants du réarmement et des rappels, aucun déplacement/
effacement réparateur ou nouvelle purge d'artefact suspect implicitement admis.

| Choix validé | Traitement des artefacts en incident | Conséquence |
| --- | --- | --- |
| A | Registre d'incident distinct, original conservé sous accès restreint | Pas de copie de diagnostic automatique, octets/références préservés |

État d'incident hors octets de manifeste, référence à identité/version/
phase/provenance et observations minimales ; original non réécrit, document
manquant reste manquant, copie supposée saine sans substitution silencieuse.
Accès diagnostic explicitement autorisé/audité, confinement applicatif/stockage
à qualifier sans chmod/droits d'hôte automatiques présumés.
Copie de diagnostic supplémentaire B non retenue comme traitement
automatique ; original manquant/altéré sans reconstruction inventée.
Commun : aucun payload source, secret ou donnée personnelle exposés en logs/
alerte, données non classifiées sous accès restrictif. Contrats de diagnostic/
minimisation sans analyse de secrets ou propagation d'un artefact arbitraire.
Manifeste et audit ne sont pas supprimés à 14 jours pour seul âge de Job ;
holds/références et procédure de retrait autorisée restent applicables.
Diagnostic sans exécution de contenu ou modification d'empreinte auditée,
clé, acteur, permission ou compteur ; source réutilisable seulement sous preuve
admissible/réconciliation, pas parce qu'une copie ou marqueur existe.
A validée pour limiter artefacts et préserver origine ; coûts/procédures/
providers à qualifier. Aucun registre, copie,
déplacement, modification d'accès, analyse, purge ou OpenSpec exécutés/créés.
Recette : original manquant/altéré, accès non habilité, contenu partiel, quota,
hold, contenu inattendu et aucune preuve ou source saine reconstituées tacitement.
A10i110 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i110

- **WHEN** un profil revendique le traitement A10i110 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--966a6be06d

Source : `openspec/specs/pzt/spec.md`, ligne 11193. SHA-256 du bloc : `f46d52dd9e9fac3b9362b385cbc1466af33844d5cd853a8948ea4578ad478f97`.

~~~~text
### Requirement: Contrat A10i111 — Alerte d'intégrité persistante avec transitions, sans rappel périodique — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i111 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i111

Diagnostic/alerte dès anomalie A10i108 A conservés, distincts des seuils d'export/
reliquat A10i81/A10i93. Répétition diagnostique indépendante de réarmement/artefacts,
aucune notification externe ou nouvelle destination créée par cet arbitrage.

| Choix validé | Alerte pendant incident inchangé | Conséquence |
| --- | --- | --- |
| A | Persistante, événements de transition seulement, sans rappel périodique | Incident visible jusqu'à clôture admissible, répétitions limitées |

Ouverture visible dès constat, mises à jour lors de changement qualifié
de cause/portée/état et clôture sous preuves/réarmement applicables. Incident
inchangé sans disparition ou statut sain déduits d'absence de nouveau message.
Rappel diagnostique périodique 24 h B non retenu ; absence de nouveau
message sans clôture automatique ou état sain présumés.
Commun : chaque anomalie/cause nouvelle et audit individuel requis conservés,
pas de regroupement de refus/administration/audit au prétexte d'alerte unique.
Identité/déduplication d'incident, quotas/volumes et provenance à qualifier,
redémarrage sans nouvelle identité permettant d'effacer incident ouvert.
Visibilité locale/PBO sous contrats autorisés disponibles, PZT/mTLS et contrôles
d'accès/audit des consultations conservés ; pas de mail, destinataire ou canal
supplémentaire supposés. Alerte sans contenu secret, payload ou PII.
Acquittement d'affichage distinct de réarmement/clôture, aucune permission
ou purge rendue admissible par acquittement ou rappel. État/couverture inconnus
exposés, audit manquant sans silence interprété comme fin de l'incident.
A validée pour sobriété et transitions explicites,
besoins/charge à qualifier. Aucune alerte, abonnement, timer, notification,
action PBO, purge ou OpenSpec créés/exécutés.
Recette : incident inchangé, nouvelle cause/portée, acquittement, clôture,
redémarrage, absence de rappel et audit individuel jamais remplacé.
A10i111 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i111

- **WHEN** un profil revendique le traitement A10i111 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c686ec1622

Source : `openspec/specs/pzt/spec.md`, ligne 11239. SHA-256 du bloc : `1921900687e566deb3dd9792d0f9622c2444503b815a2767eb5e85b01bc98ab2`.

~~~~text
### Requirement: Contrat A10i112 — Preuves du réarmement liées à un dossier de contrôle structuré et versionné — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i112 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i112

Réarmement opérateur PBO A10i109 A, audit persistant et preuves courantes
conservés. Représentation indépendante du délai A10i113 et de concurrence
de version A10i114 ; aucun dossier de récupération racine A10i35 transposé.

| Choix validé | Représentation des preuves | Conséquence |
| --- | --- | --- |
| A | Dossier structuré/versionné, références et résultats liés à commande/audit | Contrat explicite, stockage/validation à qualifier |

Identité/version/portée d'incident, commande/opération, acteur/contexte,
causes/diagnostic et contrôles d'admissibilité liés. Métadonnées typées sous
schéma fermé, origine des preuves/temps/validité et résultats confirmés/inconnus
explicites, sans payload source/secret ou capture de logs bruts. Dossier durable/
immuable par version, contenu évolué sans réécriture d'une décision passée.
Références directement dans audit sans dossier distinct B non retenues
comme représentation alternative ; référence ou déclaration sans permission.
Commun : preuve documentaire ne remplace jamais revalidation courante du
manifeste/source d'audit/exclusion/autorisation au moment de réarmement.
Preuve périmée/manquante/incohérente => refus, audit et diagnostic ; état actuel
et incident exact reconnus, aucune reconstruction depuis métriques/logs.
Rétention/holds/accès des preuves couvrent audits et reprises liés, aucune
durée 14 jours appliquée automatiquement. Formats/limites/algorithmes éventuels/
source de vérité des références à qualifier ; pas de nouvelle signature adoptée.
A validée pour lisibilité du contrat de réarmement ; coûts/provider/volume
à qualifier. Format JSON/JCS A10i116 et plafond 64 Kio A10i117 A validés le 9 octobre 2026. Autorité Django, PA sans preuve
autoproclamée ou accès SQL. Aucun dossier/événement/preuve réelle, permission,
commande de réarmement, purge ou OpenSpec créés/modifiés.
Recette : dossier incomplet/version remplacée, preuve expirée, lien mutable,
contexte différent, exclusion absente et refus sans réarmement fictif.
A10i112 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i112

- **WHEN** un profil revendique le traitement A10i112 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--0f87b5192f

Source : `openspec/specs/pzt/spec.md`, ligne 11285. SHA-256 du bloc : `afdaab58915119686737fc36f467ef9685261c42ac2bf5414198097b63b882e4`.

~~~~text
### Requirement: Contrat A10i113 — Commande de réarmement bornée à 60 secondes globales après admission serveur — option B validée le 9 octobre 2026

Le rôle chargé du traitement A10i113 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i113

Commande opérateur A10i109 A, contrôle courant et résultat/audit persistants
conservés. Délai de traitement indépendant du dossier/version d'incident ;
temps de préparation/lecture humaine avant soumission hors ce budget.

| Choix validé | Délai global maximal après admission serveur | Conséquence |
| --- | --- | --- |
| B | 60 secondes | Davantage de marge aux contrôles, attentes/ressources à qualifier |

Délai B 60 s validé comme premier jet configurable ; A 30 s non retenu.
Profil habilité/versionné. Origine monotone et
échéance conservées dès admission reconnue, incluent attente/verrous/lecture
de preuves/revalidation/persistance/audit/engagement et relances internes
admissibles ; aucun nouveau budget par appel/reconnexion/actualisation de version.
Absence d'audit/autorisation/preuve ou sécurité non vérifiables sans attente
permissive jusqu'à fin de budget. Sous-opérations bornées au temps restant,
pas de commande d'arrêt du PBO/PA ou état déclaré remis en service sur timeout.
Délai atteint sans nouvelle décision engagée ; effet déjà durable non annulé
fictivement, issue/commit inconnus réconciliés par consultation autoritative
idempotente avant nouvelle action. ACK tardif/absence de réponse sans preuve
qu'aucun réarmement n'a été engagé. Arrêt/ressources qualifiés, pas de commandes
concurrentes accumulées pour contourner timeout ou acteur ancien encore actif.
Fin effective ne relance pas purge, ne prolonge ni travail 60 s A10i87, bail
A10i91 B ni droits de mandat ; nouveau travail éventuel sous contrôles courants.
B validée pour marge supérieure ; coûts/latence/API/annulation à qualifier.
Valeur choisie par Pixs sans promesse de réponse en 60 s ou de récupération
automatique en environnement non admissible. Capacité d’admission active unique sans file A10i115 A
validée le 9 octobre 2026.
Aucune deadline/commande, autorisation, réarmement, purge ou OpenSpec modifiés.
Recette : preuve lente, audit indisponible, verrou occupé, timeout/commit inconnu,
ACK tardif, commande dupliquée et budget jamais remis à zéro.
A10i113 B validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i113

- **WHEN** un profil revendique le traitement A10i113 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--6f2104ada0

Source : `openspec/specs/pzt/spec.md`, ligne 11333. SHA-256 du bloc : `30491793c36138ae8c326ec35aee8fa9d2d82553a165ec469e7168a3446de38f`.

~~~~text
### Requirement: Contrat A10i114 — Réarmement refusé sur version d'incident obsolète, nouvelle soumission explicite — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i114 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i114

Réarmement opérateur A10i109 A, preuves courantes et engagement autoritatif
conservés. Contrôle de l'incident montré/validé par l'opérateur, indépendant
du format de dossier et du délai global 60 s A10i113 B.

| Choix validé | Version d'incident changée | Conséquence |
| --- | --- | --- |
| A | Refus comme obsolète, nouvelle lecture/soumission explicite requise | Aucune adaptation silencieuse de l'état visé par opérateur |

Version d'état pertinente et portée exactes attendues liées à commande/
opération/acteur ; comparaison et engagement coordonnés dans état courant.
Changement de cause/portée/preuve/profil ou version pertinente => refus et
diagnostic minimal, pas d'extension automatique de permission ou nouvelle version
réputée autorisée. Identité de version/formats et atomicité à qualifier.
Actualisation automatique B non retenue comme traitement alternatif.
Version obsolète : nouvelle lecture et soumission explicite requises, aucune
actualisation silencieuse ne vaut accord de l'opérateur.
Commun : déjà réarmé par même opération reconnue => état idempotent retourné,
pas de seconde levée ; autre acteur/commande distingués, audit des refus/
actions administratives individuels conservé. Lecture/audit de consultation
sans mutation artificielle de la version d'état pertinente à chaque affichage.
Comparaison seulement frontend/mémoire locale insuffisante, autorité Django
et persistance courante/contrôles d'accès requis ; issue d'engagement inconnue
réconciliée sans réarmement aveugle. Version seule sans autorisation ou preuve.
A validée pour intention opérateur explicite ; aucun champ/schéma/verrou/
provider concret adopté. Réarmement sans
nouvelle purge, budgets/holds/audit conservés, aucune commande/SQL/OpenSpec modifiés.
Recette : version changée, preuve retirée, commandes concurrentes/dupliquées,
consultation auditable, version obsolète et aucun élargissement tacite.
A10i114 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i114

- **WHEN** un profil revendique le traitement A10i114 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--671f0d0301

Source : `openspec/specs/pzt/spec.md`, ligne 11379. SHA-256 du bloc : `aa12ebe4b0a9f2e4351c63a80a6274bc8f9fba1ca5016dee1e3babce51f4784f`.

~~~~text
### Requirement: Contrat A10i115 — Réarmement limité à une commande active par autorité, sans file — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i115 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i115

Réarmement manuel A10i109 A, délai global 60 s A10i113 B et version obsolète
refusée A10i114 A conservés. Admission des commandes distincte du créneau de
purge A10i90 et des travaux en attente A10i95.

| Choix validé | Capacité par autorité logique | Conséquence |
| --- | --- | --- |
| A | Une commande active, aucune file | Non-admission explicite si occupé, état idempotent consultable |

Admission/possession/exclusion durables sous autorité Django, frontends/acteurs
coordonnés ; mutex local ou nombre de workers sans unicité globale présumée.
Même commande/opération reconnue renvoie son état, pas de second effet ou
créneau. Consultation autorisée du résultat sans nouvelle commande ni slot
mutant requis, audit individuel des consultations toujours applicable.
Occupé => non-admission explicite, sans commande fantôme ni file parallèle.
Commande en attente B non retenue ; aucune file parallèle, demande
persistée ou identité nouvelle pour contourner capacité sous ce profil.
Commun : état/commit inconnus et ressources/acteur précédents réconciliés avant
réutilisation, pas de remplacement concurrent sur seul timeout. Capacité sans
droit de lever incident, aucune purge déclenchée ou compteur de Job réinitialisé.
État affiché et non-admission distingués de refus de sécurité/résultat incertain.
PBO–PA via PZT/mTLS conservé, aucun rôle local PA ou canal de contournement.
A validée pour commandes manuelles et simplicité de charge ; ressources/
concurrence/latence à qualifier. Paramètres
de premier jet sous profil habilité/versionné, pas de débit garanti.
Aucune commande, file, ordonnanceur, autorisation, réarmement ou OpenSpec modifiés.
Recette : occupé, commande dupliquée, absence de file, preuve/version changée,
acteur ancien actif et consultation d'état sans second réarmement.
A10i115 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i115

- **WHEN** un profil revendique le traitement A10i115 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--58d9e8b09a

Source : `openspec/specs/pzt/spec.md`, ligne 11424. SHA-256 du bloc : `b6fd166141b49b52ba4f8a788597f230310ff46801f9544f113e55d6ce4d5602`.

~~~~text
### Requirement: Contrat A10i116 — Dossier de contrôle de réarmement en JSON UTF-8 fermé et JCS qualifié — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i116 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i116

Dossier structuré/versionné A10i112 A et contrôles courants conservés. Choix
de format propre à ce dossier, distinct du manifeste de purge A10i97 et du
dossier racine A10i38 ; plafond 64 Kio A10i117 A conservé.

| Choix validé | Format du dossier de contrôle | Conséquence |
| --- | --- | --- |
| A | JSON UTF-8 fermé/typé/versionné, produit selon JCS qualifié | Conventions JSON homogènes, codec/champs à qualifier |

Objet racine fermé, doublons/inconnus/BOM/Unicode invalide/commentaires/
données après objet refusés. Conventions de chaînes décimales int64/uint64
A10i64 et JCS A10i103 explicitement retenues pour ce rôle, nombres compatibles
exacts seulement, chaînes sans normalisation implicite et octets conservés.
CBOR B non retenu comme format alternatif, aucune conversion silencieuse
ou extension de schéma permissive.
Commun : incident/version/portée, commande/opération/acteur/contexte, contrôles
et références de preuves/résultats liés sous schéma qualifié ; avant/après
engagement distincts, toute évolution versionnée/immuable et liée à audit.
Aucun payload source, log brut, clé/token ou document arbitraire intégré.
Métadonnées lisibles sans devenir permission : contrôle courant à chaque
action, refus si preuve manquante/périmée ou source non admissible.
Taille/profondeur/cardinalités/précision et coûts de construction/validation
à qualifier sous délai 60 s, aucune limite du manifeste/IPC transposée sans
choix explicite. Stockage/accès/holds/références et rétention couvrant audit/
reprises requis, aucune durée d'audit ou signature/hachage supplémentaire adoptés.
A validée pour conventions homogènes,
sans compacité/CPU/RAM universels garantis ; bibliothèque/version non choisies.
Formats JSON/JCS/CBOR décrits par RFC 8259/8785/8949 déjà référencées dans ces
cahiers, préférence choisie par Pixs et qualifications nécessaires.
Intégrité SHA-384/Base64url A10i118, complexité 8/32/64 A10i119 et conservation
liée à audit/holds A10i120 A validées le 9 octobre 2026.
Aucun dossier/codec/provider, clé, réarmement ou OpenSpec créés/modifiés.
Recette : champ inconnu, doublon, numéro 64 bits, preuve brute/secrète refusée,
version remplacée, dossier partiel et aucun réarmement déduit du document.
A10i116 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i116

- **WHEN** un profil revendique le traitement A10i116 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--94a6d89385

Source : `openspec/specs/pzt/spec.md`, ligne 11475. SHA-256 du bloc : `e9a1a474ea9cc25b817d6136f877d01cb72640dea9c8d18051ae07dd47a5207b`.

~~~~text
### Requirement: Contrat A10i117 — Dossier de contrôle de réarmement plafonné à 64 Kio par version — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i117 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i117

Dossier de références/preuves structurées A10i112 A, délai de commande 60 s
A10i113 B et format JSON/JCS A10i116 A conservés. Plafond par document/version
encodé, indépendant de capacité d'admission A10i115.

| Choix validé | Plafond par dossier/version encodé |
| --- | --- |
| A | 64 Kio |

Plafond A 65 536 octets inclusifs validé ; B 128 Kio non retenu.
Contenu encodé exact,
métadonnées/références/contrôles/résultats requis inclus. Références vers pièces
qualifiées sous leurs propres tailles/accès/rétentions ; aucune externalisation
arbitraire de champs pour contourner plafond ou copie de payload source.
Écriture/réception/analyse effectivement bornées, taille annoncée non fiable.
Dossier trop grand/incomplet/ambigu => refus de décision, jamais preuve tronquée,
contrôle omis, autorisation partielle ou réarmement anticipé. Volume maximal
et schéma de toutes phases qualifiés avant activation, pas de dossier produit
sur 128 Kio admis par baisse silencieuse à 64 Kio.
Ressources globales/copies/versions/objets parsés et coût d'accès aux preuves
à qualifier séparément, pas de RAM strictement 64 Kio ou plafond global de
stockage démontrés. Délai 60 s, conditions courantes et incident exact restent
requis, pas de budget remis à zéro pour découper dossier et contourner limite.
A validée comme premier jet de métadonnées/références restreintes ; besoins/
couverture/volumétrie à mesurer. Paramètre configurable
sous profil autorisé/versionné, sans hausse automatique ou nouveau backend.
Aucun fichier/preuve, variable/runtime, événement d'audit, réarmement, purge
ou OpenSpec créés/modifiés. Recette : limite exacte/plus un, référence manquante,
gros IDs, dossier incomplet, copies et aucune décision sans preuves complètes.
A10i117 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i117

- **WHEN** un profil revendique le traitement A10i117 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--9dcafd80ac

Source : `openspec/specs/pzt/spec.md`, ligne 11521. SHA-256 du bloc : `755f4949a2b97bdb49be50c02bb47f82f46cc1cde1ac82a5eab4994f8a860d63`.

~~~~text
### Requirement: Contrat A10i118 — Dossier de contrôle lié par SHA-384 entière et Base64url externe auditée — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i118 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i118

Portée du lot A10i118–A10i120 : contrats de contenu et régime ordinaire des
contrôles applicatifs. Les dérogations réservées au seul Super Admin suivent
authorization (référence de cadrage : openspec/specs/authorization/spec.md),
initial-administration (référence de cadrage : openspec/specs/initial-administration/spec.md) et
audit (référence de cadrage : openspec/specs/audit/spec.md), ainsi que TECHNICAL §12.7.
Compte authentifié et périmètre reconnus, aucun transfert de credentials ou
d'exception à un worker/autre compte, aucun tenant non accordé ouvert.
Contrats structurels/d'exécution et faits établis restent distincts : audit,
document ou contrôle absent/non réalisé jamais présentés comme disponibles
ou effectués. L'absence d'audit liée à dérogation ne fixe pas par elle-même
une durée de conservation nulle ; gouvernance applicable et disponibilité
effective des références déclarées sans inventer preuve ou historique.

Dossier JSON/JCS 64 Kio A10i116/A10i117 A et audit requis A10i112 A conservés.
Liaison à audit/commande indépendante de complexité A10i119 et rétention A10i120 ;
algorithme du manifeste A10i98 sans portée automatique sur ce dossier.

| Choix validé | Liaison d'intégrité du dossier immuable | Conséquence |
| --- | --- | --- |
| A | SHA-384 entière sur octets originaux, Base64url dans référence externe auditée | Liaison de contenu explicite, vérification à qualifier |

Digest 48 octets, encodage 64 ASCII strict selon conventions A10i98/A10i100
explicitement retenues pour ce rôle. Référence externe liée à incident/version/
portée, commande/opération, phase/version de dossier et longueur exacte ;
pas d'autoréférence, troncature, normalisation ou re-sérialisation de l'original.
Liaison par identité/version seule sous contrat provider B non retenue
comme alternative à cette empreinte externe.
Commun : vérifier dossier/profil/corrélation et autorisation/source/preuves
courantes ; hash ou référence ne prouvent ni permission, authenticité autonome,
dernier état, commit PostgreSQL ou exclusion réelle d'ancien acteur.
Pas de clé/signature supplémentaire ni reçu racine A10i35 transposés.
Sélection de format/algorithme explicite, rôles/dossiers distincts ; octets
produits immuables et audit protégés sous autorité Django/source de vérité.
Document manquant/altéré/inconnu => refus/réconciliation, résultat confirmé non
inventé, aucune levée par substitution de digest ou réécriture d'audit.
A validée pour liaison de contenu explicite et conventions homogènes ;
coûts CPU/RAM/I/O à mesurer. Revalidation à chaque usage A10i122 A validée le 9 octobre 2026.
Conventions décrites par FIPS 180-4/RFC 4648 déjà référencées, choix validé
par Pixs sans conformité d'implémentation revendiquée. Aucun digest/dossier
réel, bibliothèque, champ/API, réarmement ou OpenSpec créés/modifiés.
Recette : contenu modifié, référence/phase/version erronées, digest tronqué,
réencodage, ID réutilisé et aucun droit ou effet déduit d'une intégrité seule.
A10i118 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i118

- **WHEN** un profil revendique le traitement A10i118 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e152de0832

Source : `openspec/specs/pzt/spec.md`, ligne 11581. SHA-256 du bloc : `9a4006b13c2f90ed5e3109d8f3d9053d5bed66761a488dea795fdd809e96d58c`.

~~~~text
### Requirement: Contrat A10i119 — Complexité du dossier JSON plafonnée à 8 niveaux, 32 membres et 64 éléments — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i119 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i119

JSON/JCS fermé A10i116 A, contenu 64 Kio A10i117 A et délai 60 s A10i113 B
conservés. Plafonds propres au dossier de contrôle, distincts du manifeste
de purge A10i101 et du JSON IPC A10i65.

| Choix validé | Profondeur maximale | Membres par objet | Éléments par tableau |
| --- | --- | --- | --- |
| A | 8 | 32 | 64 |

Plafonds A 8/32/64 validés, B 16/64/128 non retenus.
Objet racine niveau 1, chaque objet/tableau ajoute niveau, primitives sans
niveau supplémentaire. Plafonds inclusifs/cumulatifs avec 65 536 octets,
schéma/champs/nombres/unités et totalité des contrôles/preuves requis.
Nombre total de références/éléments et limites de chaque champ à qualifier
séparément, tableau de 64 sans nombre de preuves illimité ou type inconnu admis.
Doublons comptés/refusés avant écrasement, limites détectées au plus tôt
par mécanisme qualifié ; aucun arbre non borné construit puis tronqué ou
preuve omise pour contourner. Dépassement/ambiguïté => refus avant réarmement,
dossier initial non réécrit pour faire passer contrôle.
Taille annoncée non fiable, amplification mémoire/tokens/CPU et accès aux
preuves liés à qualifier, pas de plafond RSS démontré par profondeur/64 Kio.
Sérialisation/corrélation/exactitude entière et preuves courantes conservées,
pas de baisse silencieuse d'une politique différente ou d'extension permissive.
A validée pour métadonnées et références restreintes à qualifier. Paramètres de premier jet configurables sous
profil habilité/versionné, aucune couverture ou consommation observée présumées.
Aucun parseur/schéma réel, dossier, variable/runtime, réarmement ou OpenSpec modifiés.
Recette : racine/limites/plus un, nombreux contrôles/références, doublon, types
inconnus, taille saturée et aucun effet sur dossier incomplet/tronqué.
A10i119 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i119

- **WHEN** un profil revendique le traitement A10i119 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--927c72147f

Source : `openspec/specs/pzt/spec.md`, ligne 11626. SHA-256 du bloc : `c7b883484c61a72783299b51552f6cbc7e87ecde81777aeede4e202f9cd9d9b7`.

~~~~text
### Requirement: Contrat A10i120 — Conservation du dossier de réarmement liée aux durées et holds de l'audit — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i120 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i120

Dossier durable/immuable A10i112 A, audit individuel et gouvernance conservés.
Politique propre au dossier de contrôle, indépendante de liaison d'intégrité/
complexité ; manifeste de purge A10i107 garde sa portée distincte.

| Choix validé | Conservation du dossier et versions | Conséquence |
| --- | --- | --- |
| A | Durée/holds hérités de l'audit lié, prolongation tant que références/reprises l'exigent | Décision/preuves/dossier conservés sous contraintes applicables |

Événements/commande/opération/incident et versions référencés identifiés ;
contraintes combinées si plusieurs audits/holds, conservation plus protectrice
si conflit non résolu. Durée numérique d'audit non fixée ici, ancienneté de
l'incident ou métadonnées Job 14 jours sans expiration automatique du dossier.
Politique propre indépendante B non retenue comme règle alternative ;
contraintes des références/audits liés et évolutions courantes conservées.
Commun : aucune suppression sur âge seul ; permission/horloge/provenance/
holds/références/projections, audit et anti-résurrection vérifiés avant retrait.
Preuves référencées ont leur propre gouvernance et restent disponibles tant
que la décision doit être vérifiable ; copie ou lien sans rétention suffisante
ne valent pas conservation. Données non classifiées restrictives, accès
séparément déclarés, héritage de rétention sans droit de consultation automatique.
Dossier requis manquant => incident/état incomplet exposés, aucune reconstruction
de contrôle réussi depuis log/métrique ou ancienne commande affichée. Chaque
usage garde contrôle courant, conservation passée sans permission de réarmer.
A validée pour cohérence documentaire ; besoins/volumes/providers à qualifier,
pas de conservation éternelle,
nouvel archivage/clé/signature ou obligation externe déduits.
Aucun dossier/audit/Job, copie/sauvegarde ou OpenSpec purgés/modifiés ici.
Recette : audits de durées différentes, hold ajouté, référence vivante, Job âgé
de 14 jours, restauration et aucune preuve nécessaire supprimée prématurément.
A10i120 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i120

- **WHEN** un profil revendique le traitement A10i120 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--bcd7cf9dcb

Source : `openspec/specs/pzt/spec.md`, ligne 11673. SHA-256 du bloc : `9f9464bc9bb69f4f2e8288d075cdccab7121c9c326e2bf23bff2fda8aa94d02b`.

~~~~text
### Requirement: Contrat A10i121 — Engagement atomique de l'état de réarmement et de ses références — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i121 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i121

Réarmement opérateur A10i109 A, dossier A10i112 A et budget 60 s A10i113 B
conservés. Contrat d'engagement indépendant de vérification A10i122 et du suivi
A10i123 ; exception applicative Super Admin OpenSpec réservée au compte/périmètre
reconnus, aucun audit absent présenté comme réalisé.

| Choix validé | Engagement retenu | Conséquence |
| --- | --- | --- |
| A validée | Un engagement autoritatif atomique de l'incident, commande/opération et références de dossier/audit applicables | État logique cohérent, frontière transactionnelle à qualifier |

A : comparaison de version pertinente, contrôles applicables et changement
d'état liés à même décision Django/état PostgreSQL courant. Artefacts externes
éventuels préparés durablement/immuables avant engagement, références disponibles
et admissibles ; aucune atomicité physique inter-providers déduite du commit.
L'engagement en phases coordonnées, option B, n'est pas retenu.
Commun : source indisponible/commit inconnu => réconciliation autoritative,
pas de nouvelle commande ou effet réputé absent pour seul ACK perdu.
Publication d'événement seulement après validation de la transaction requise
selon OpenSpec Events ; déduplication et ordre déclarés, notification sans
preuve publique de commit PostgreSQL ou nouvelle permission.
Régime ordinaire : audit requis lié et persistant, indisponibilité bloquante.
Dérogation Super Admin lorsqu'applicable : acteur initial/périmètre reconnus
selon authorization/initial-administration, absence d'audit explicitement non
réalisée, jamais audit/dossier/contrôle inventés. Worker sans credentials ou
identité de service Super Admin, aucun tenant non accordé implicitement ouvert.
Contrats de contenu et faits effectivement établis distincts des dérogations ;
budget/exclusion/reprise reconnus, pas de purge déclenchée par publication.
Cohérence d'état logique retenue. Schéma/provider/SQL/migration/concurrence
à qualifier ; aucun engagement, événement, autorisation, réarmement ou
OpenSpec modifiés ici.
Recette : échec avant/après commit, artefact absent, version changée, audit
ordinaire indisponible, dérogation reconnue sans audit et aucun fait inventé.
A10i121 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i121

- **WHEN** un profil revendique le traitement A10i121 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c93afebf8e

Source : `openspec/specs/pzt/spec.md`, ligne 11722. SHA-256 du bloc : `9273001ca0dc00d38f5db845a18e46e56b85f13f76e5640c15c74ca36f1d0ba6`.

~~~~text
### Requirement: Contrat A10i122 — Vérification du dossier de réarmement à chaque usage — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i122 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i122

Dossier JSON/JCS, SHA-384/Base64url et plafonds A10i116–A10i119 A conservés.
Contrôle de contenu distinct de manifeste A10i105 et des autorisations/source/
références actuelles ; exception Super Admin selon OpenSpec sans fait de preuve créé.

| Choix validé | Vérification de contenu retenue à lecture/export/usage probatoire | Conséquence |
| --- | --- | --- |
| A validée | Revalider schéma/profil/corrélation et recalculer SHA-384 à chaque usage sur octets originaux | Contrat simple sans cache de résultat, calculs répétés à mesurer |

A : dossier original complet et référence admissible disponibles, digest entier
comparé, mauvais rôle/phase/version ou document altéré refusés comme preuve.
Le cache de résultat sur copie immuable, option B, n'est pas retenu.
Contrôles d'autorisation, de révocation et de version d'incident, ainsi que
preuves actuelles, restent séparés ; aucun mandat hérité
d'une ancienne vérification ; pas de cache de preuve temporelle A10i51.
Commun : document manquant/incohérent sans affichage/export comme dossier
valide. Si un contrôle applicatif est dérogé par le Super Admin dans son
périmètre reconnu, contrôle non effectué/dossier absent signalés sans fausse
validation ou preuve d'audit ; aucun bypass structurel conférant privilège.
Validation à chaque usage retenue ; CPU/RAM/latence à mesurer.
Rétention A10i120, contenu 64 Kio et budget du traitement participant
conservés sous contrats applicables.
Aucune lecture/validation réelle, cache, dossier, clé, réarmement ou OpenSpec modifiés.
Recette : altération, référence changée, copie relue sans cache de résultat, autre
périmètre, dossier absent et dérogation sans preuve de validation inventée.
A10i122 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i122

- **WHEN** un profil revendique le traitement A10i122 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

