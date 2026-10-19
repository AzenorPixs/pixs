# Références normatives — Z21

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 9931 | [Contrat A10i85 — Travaux de purge de télémétrie à cadence nominale de 24 heures — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9931) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9982 | [Contrat A10i86 — Lots de purge plafonnés à 1 000 enregistrements sources — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9982) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10032 | [Contrat A10i87 — Travail actif de purge borné à 60 secondes globales — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10032) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10083 | [Contrat A10i88 — Point de reprise durable après chaque lot de purge confirmé — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10083) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10132 | [Contrat A10i89 — Réessai technique de purge borné à 2 tentatives et attente nominale de 1 seconde — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10132) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10183 | [Contrat A10i90 — Un seul travail de purge télémétrie actif par autorité logique — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10183) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10233 | [Contrat A10i91 — Bail persistant de purge nominal 60 secondes, renouvellement 20 secondes — option B validée le 9 octobre 2026](../../specs/pzt/spec.md#L10233) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10281 | [Contrat A10i92 — Travaux de purge ordonnés par rotation déterministe des classes — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10281) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10330 | [Contrat A10i93 — Alerte de reliquat de purge après 2 observations qualifiées consécutives — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10330) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10379 | [Contrat A10i94 — Audit des effets de purge par lot lié à un manifeste durable — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10379) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10429 | [Contrat A10i95 — Attente de purge plafonnée à 3 travaux, un par classe — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10429) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10478 | [Contrat A10i96 — Rétention nominale des métadonnées terminales de purge à 14 jours — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10478) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--b878787fe7

Source : `openspec/specs/pzt/spec.md`, ligne 9931. SHA-256 du bloc : `424d3937144f5ec20780342005c62986014e0b950b3d7306f4320788d88261a2`.

~~~~text
### Requirement: Contrat A10i85 — Travaux de purge de télémétrie à cadence nominale de 24 heures — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i85 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i85

Rétentions logs 7 jours/métriques 30 jours/traces 24 h A10i82–A10i84 A conservées.
Cadence de conception d'un travail backend autorisé, indépendante du lot A10i86
et du budget A10i87 ; âge seul sans permission de purge selon OpenSpec.

| Choix validé | Cadence nominale de conception | Conséquence |
| --- | --- | --- |
| A | Toutes les 24 heures | Moins de réveils, attente potentiellement plus longue après éligibilité |

Cadence A 24 h validée comme premier jet configurable, B 1 h non retenue.
Profil versionné/habilité, activation après
qualification. Un seul travail actif par classe/périmètre déclaré ; déclenchements
concurrents coalescés/refusés selon contrat, pas de rafale de rattrapage ou
travaux sans borne accumulés après panne. Planning/zone temporelle et horloge
de cadence qualifiés, distincts de l'horloge qualifiant la rétention.
Django porte décision/autorisation, backend/provider de données opère sous
contrat déclaré ; aucun accès SQL ou droit destructif direct accordés au PA
ou collecteur temporel. Mandat/politique explicite de purge pour périmètre
exact, contrôle courant des âges/holds/références/projections et audit persistant
avant effet selon contrat transactionnel qualifié ; échec fermé si preuves manquent.
Rétention nominale expirée sans purge instantanée garantie : cadence/retard/
backlog/holds et budgets comptent. Capacité à tenir volumes/stockage et suivi
d'éléments éligibles non traités qualifiés avant activation, pas de données
courantes supprimées pour rattraper retard. Aucun horizon d'audit métier,
dossier racine, marqueur A10i44–A10i46 ou clé/backup concernés.
A validée comme premier jet sobre en réveils. Valeur choisie par Pixs,
aucune conformité ou durée légale
déduites. Cadence ne vaut ni mandat d'exécution réel ni création d'automation
dans cet environnement. Aucun cron, ordonnanceur, purge ou OpenSpec exécutés/
modifiés, plateformes/backend et procédures à qualifier. Travaux Jobs
persistés avant exécution, bail/états/corrélation et contrôles courants requis.
Concurrence globale d’un travail actif A10i90 A validée le 9 octobre 2026.
Recette : âge non atteint, hold, audit indisponible, travail actif, retard,
backlog, reprise et aucune rafale ou suppression hors périmètre.
A10i85 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i85

- **WHEN** un profil revendique le traitement A10i85 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--b657cbbdb8

Source : `openspec/specs/pzt/spec.md`, ligne 9982. SHA-256 du bloc : `38938af9261969eeef7868c489da85c96ba3cbd61bdc9d2dd26ce7ee290b6960`.

~~~~text
### Requirement: Contrat A10i86 — Lots de purge plafonnés à 1 000 enregistrements sources — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i86 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i86

Travail backend autorisé sous contrôles de cycle de vie/gouvernance conservé.
Taille de lot indépendante de cadence A10i85 et durée globale A10i87 ; aucun
quota ou règle d'archivage de dossiers métier transposé.

| Choix validé | Enregistrements sources au maximum par lot | Conséquence |
| --- | --- | --- |
| A | 1 000 | Lots plus petits, verrous/transactions et reprise à qualifier |

Plafond A 1 000 validé, B 10 000 non retenu.
Un enregistrement source = événement technique de log, point métrique ou span
stocké, selon classe déclarée ; comptage inclusif, lot d'une même classe/
périmètre et plan admissibles. Effets dérivés/index/références comptabilisés et
bornés séparément, pas de 1 000 lignes physiques ou consommation mémoire fixe
déduites de 1 000 enregistrements logiques.
Sélection déterministe/reprenable sous contrat provider, curseur et références
qualifiés sans chargement intégral non borné. Taille d'octets, amplification,
I/O/verrous et limites de transaction à qualifier ; temps global prioritaire.
Contrôles courants avant effet, changement de hold/politique/contexte sans
ancien lot déjà sélectionné réputé encore purgeable. Résultat/audit et checkpoint
durables cohérents, résultat d'engagement incertain réconcilié avant reprise,
pas de lot répété pour masquer absence de preuve.
Dérivés/restaurations soumis aux exigences d'anti-résurrection OpenSpec ;
incomplétude déclarée sans purge présentée globale ou données recréées.
Audit métier/reçus/dossiers/état de reprise hors cible, secrets jamais analysés
ou exposés comme payload de sélection. Autorité Django, PA sans SQL direct.
A validée comme premier jet de petite taille ; débit/CPU/RAM/latence
à qualifier, sans garantie universelle. Valeur configurable
sous profil autorisé, sans augmentation automatique pour épuiser backlog.
Point de reprise par lot confirmé A10i88 A validé le 9 octobre 2026.
Aucun lot, requête SQL, suppression ou OpenSpec exécutés/modifiés ici.
Recette : lot exact/plus un, gros enregistrement, hold concurrent, curseur repris,
commit incertain, index/sauvegarde et aucune double purge ou preuve inventée.
A10i86 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i86

- **WHEN** un profil revendique le traitement A10i86 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--7e48e03402

Source : `openspec/specs/pzt/spec.md`, ligne 10032. SHA-256 du bloc : `8699531ec18049dc0646690d4a7e101e5ab77a82a3557c959ad6a0588880c7c4`.

~~~~text
### Requirement: Contrat A10i87 — Travail actif de purge borné à 60 secondes globales — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i87 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i87

Rétentions validées et purge autorisée/auditée/idempotente OpenSpec conservées.
Budget de conception indépendant de cadence/lot A10i85/A10i86 ; pas de budget
du collecteur de preuve A10i52 ou du cycle métrique A10i76 remplacé.

| Choix validé | Budget global maximal par travail actif | Conséquence |
| --- | --- | --- |
| A | 60 secondes | Travail court, progression admissible conservée, achèvement complet non garanti |

Budget A 60 s validé comme premier jet configurable, B 300 s non retenu.
Profil habilité/versionné ; origine monotone à
admission active après attribution de créneau, échéance unique sans remise à
zéro par lot/reconnexion/retry. Sélection/contrôles/I/O/transactions/attentes/
audit/checkpoint et relances internes participants inclus ; sous-opérations
bornées par temps restant, un lot de 1 000 sans nouveau budget 60 s autonome.
Au budget atteint : aucun nouveau lot/effet engagé, checkpoint/résultat courant
réconciliés ; statut partiel/arrêt/incertain exposé, aucun « terminé » pour seul
timer. Effet déjà durable sans annulation fictive, transaction inconnue sans
commit présumé absent ; annulation effective et ressources suivies, pas de
lancement concurrent pour contourner tâche ancienne encore active.
Reprise ultérieure sous politique/mandat encore admissibles, contrôles réévalués
et opération idempotente reconnue, sans prolonger budget de travail expiré ou
enchaîner des relances sans borne pour finir à tout prix. Échec de sécurité/
rétention/hold/audit sans tentative permissive ; pas d'arrêt du PBO/PA/hôte ou
service de synchronisation pour récupérer un créneau de maintenance.
Horizon de conservation et capacité de purge globale à qualifier avec volumes ;
60 s de travail quotidien sans promesse d'épuiser tous éléments éligibles,
alerte/backlog/quotas explicites à qualifier sans réduire rétention validée.
A validée pour travail borné court ; coût,
durabilité/checkpoints et annulation à mesurer sur plateformes/providers.
Réessai borné 2 tentatives/attente 1 s A10i89 A validé le 9 octobre 2026.
Aucune tâche, relance, suppression, modification d'autorisation ou OpenSpec
exécutés/créés ici. Recette : budget exact/au-delà, attente de verrou, lot en
cours, commit incertain, checkpoint, travail ancien actif et audit requis absent.
A10i87 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i87

- **WHEN** un profil revendique le traitement A10i87 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--ba7e93a0f7

Source : `openspec/specs/pzt/spec.md`, ligne 10083. SHA-256 du bloc : `8467fc3b7601d1f11dfdf0fc75d8bf646bb8a1aa984b1516c8bb8fd5384d0900`.

~~~~text
### Requirement: Contrat A10i88 — Point de reprise durable après chaque lot de purge confirmé — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i88 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i88

Lots 1 000 A10i86 A et budget global 60 s A10i87 A conservés. Travail persisté,
bail/états/corrélation/idempotence et contrôles OpenSpec Jobs applicables ;
granularité indépendante des réessais A10i89 et de la concurrence A10i90.

| Choix validé | Point de reprise durable | Conséquence |
| --- | --- | --- |
| A | Après chaque lot entièrement confirmé | Progression par lot, interruption réconciliée avant reprise idempotente |

Point avancé après preuve des effets requis et audit durable du lot,
contexte/identités travail-commande-opération, classe/périmètre, politique/version
et bornes de sélection liés. Dernier lot incomplet/inconnu sans point avancé
ou ligne supposée purgée. Reprise depuis dernier point confirmé, contrôle des
effets déjà réalisés avant rejeu, aucune suppression d'un nouvel enregistrement
occupant une position réutilisée ou non conforme à la sélection d'origine.
Point de reprise à chaque enregistrement B non retenu comme granularité
alternative ; preuves/audit des effets et contrôles courants conservés.
Commun : progression durable dans contrat de travail sous autorité Django/
source de vérité PostgreSQL, pas de fichier PA devenu autorité de purge.
Contrat provider doit relier sélection/effets/audit/progression ou décrire
réconciliation d'étapes non atomiques ; checkpoint seul sans preuve de commit
ou propagation réelle présumés. Progression périmée/retour arrière/incertitude
bloquants jusqu'à réconciliation, audit jamais reconstruit depuis compteur.
États Jobs autorisés conservés, résultat partiel en métadonnées sans nouveau
statut implicite ni SUCCEEDED pour seul timer. Indisponibilité de persistance/
bail/autorisation sans exécution ; réévaluation à création/exécution/reprise.
A validée pour petite taille de lot et simplicité de progression ; coûts
durabilité/rejeu à mesurer, aucun gain universel.
Schéma/curseur/contrat exacts à qualifier, pas de migration, point de reprise,
requête SQL ou OpenSpec modifiés ici. Recette : lot partiel, audit absent,
commit incertain, position réutilisée, doublon déclenchement et reprise sans
double effet confirmé ou progression fictive.
A10i88 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i88

- **WHEN** un profil revendique le traitement A10i88 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--dc8facc32b

Source : `openspec/specs/pzt/spec.md`, ligne 10132. SHA-256 du bloc : `d6036c4266cc29646da1a41c116b125971a3688c92d1d2205ac4a92f7b5a0bc1`.

~~~~text
### Requirement: Contrat A10i89 — Réessai technique de purge borné à 2 tentatives et attente nominale de 1 seconde — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i89 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i89

Travail persistant/autorisé/idempotent OpenSpec Jobs et global 60 s A10i87 A
conservés. Réessai technique sous mandat/politique préalable, indépendant de
granularité du checkpoint et de concurrence ; pas de réessai métier permissif.

| Choix validé | Politique de réessai technique | Conséquence |
| --- | --- | --- |
| A | Au plus 2 tentatives initiale comprise, attente nominale 1 seconde avant l'unique réessai | Reprise technique bornée dans le même budget global |

Erreurs rejouables déclarées par profil/provider, échec transitoire attesté,
mandat/contexte/bail courants et cause sans blocage de sécurité/rétention/hold/
audit. Compteur réservé/persisté avant chaque tentative, attente monotone 1 s
nominale sans nouvelle échéance ; début/compteur/budget conservés à reconnexion
ou reprise, pas de « deux tentatives » à chaque niveau de wrapper.
Issue d'effet/commit inconnue => consultation/réconciliation autoritative,
jamais nouvelle suppression parce que réponse absente. Réessai seulement
quand état admissible et absence de double effet/future exécution de l'ancienne
tentative prouvés ; idempotence sans validation de droits ou dernier état présumés.
Tentative de reprise limitée au travail/unité reconnus, pas de nouveau Job ou
identifiant permettant de réinitialiser compteur et 60 s. Budget insuffisant,
compteur épuisé ou contrôle incertain => arrêt/statut Jobs cohérent et diagnostic.
Reprise uniquement explicite après toute erreur B non retenue comme règle
alternative ; erreurs non rejouables ou incertaines restent bloquantes.
Commun : sécurité, rétention non atteinte, hold, contexte expiré et audit requis
indisponible ne deviennent jamais erreurs techniques rejouables par ce choix.
Bail/états Jobs persistants, corrélation et déduplication conservés ; bail
paramétré 60 s/renouvellement 20 s A10i91 B validé le 9 octobre 2026. Reprise
après incident sans autorité de l'agent local ou relance aveugle destructrice.
A validée pour un incident technique transitoire ; chiffres de premier jet
configurables et qualification requise,
pas de succès/débit garantis. Aucun retry, temporisateur, purge, changement
de mandat, configuration ou OpenSpec exécutés/modifiés ici.
Recette : erreur rejouable, seconde tentative, budget restant insuffisant,
ACK perdu/commit inconnu, ancien acteur actif, hold et refus sans compteur remis à zéro.
A10i89 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i89

- **WHEN** un profil revendique le traitement A10i89 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--811d4618ea

Source : `openspec/specs/pzt/spec.md`, ligne 10183. SHA-256 du bloc : `8c2d34420b9d6c7af8f43edb079c56c468659b16b09159a08666d16da03a754c`.

~~~~text
### Requirement: Contrat A10i90 — Un seul travail de purge télémétrie actif par autorité logique — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i90 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i90

Un actif par classe/périmètre A10i85 A maintenu, Jobs persistants et budget
60 s par travail A10i87 A conservés. Limite globale par autorité logique,
indépendante de taille de lot/checkpoint/réessai, sans quota par PA ordinaire.

| Choix validé | Travaux actifs par autorité logique | Conséquence |
| --- | --- | --- |
| A | 1, toutes classes de télémétrie confondues | Créneau partagé entre logs/métriques/traces, coordination globale qualifiée |

Créneau partagé de maintenance sous contrat d'admission durable,
périmètres/classes ordonnés selon politique qualifiée sans starvation silencieuse.
Trois travaux simultanés B non retenus ; classes/périmètres sans quotas
multipliés par partitionnement ou création d'acteurs.
Commun : admission/exclusion et propriétaire/génération coordonnés sous
autorité Django/état courant admissible, identités de travail/opération distinctes
et bail persistant Jobs, aucune unicité globale déduite d'un mutex local ou PID.
Tous chemins d'effet provider appliquent l'exclusion qualifiée ; expiration
de bail seule sans ancien acteur inhibé/terminé ou effets empêchés ne suffit pas
à engager un remplaçant. État/commit incertains réconciliés avant réutilisation,
pas de workers accumulés ou arrêt de service non concerné.
Perte d'autorisation/bail/profil/exclusion => aucun nouvel effet, progression
confirmée conservée, statut Jobs/diagnostic/audit cohérents. Coordonnateur/source
de vérité indisponibles sans relance locale autonome. PA sans SQL/droit de purge,
aucun nouveau protocole/clé/permissions ou multi-hôte implicites.
Limites mémoire/CPU/I/O/verrous/provider globales à qualifier, 60 s par travail
sans garantie de débit ou traitement complet. Cadence/volume/backlog
doivent être compatibles avec rétentions, aucune réduction automatique de durée.
A validée pour charge de maintenance limitée et coordination simple.
Ordre A10i92 A et alerte de reliquat A10i93 A validés le 9 octobre 2026.
Valeurs configurables sous politique
autorisée/versionnée, pas de runtime/provider/migration/worker ou OpenSpec créés.
Recette : déclenchements concurrents, classe identique, autorité indisponible,
bail expiré avec acteur vivant, commit incertain, refus sans remplacement illimité.
A10i90 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i90

- **WHEN** un profil revendique le traitement A10i90 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--311b97a91a

Source : `openspec/specs/pzt/spec.md`, ligne 10233. SHA-256 du bloc : `409c586cca63e4596c92c708e5e5d9460e08e32b2648c56d5c743d990fb3bb06`.

~~~~text
### Requirement: Contrat A10i91 — Bail persistant de purge nominal 60 secondes, renouvellement 20 secondes — option B validée le 9 octobre 2026

Le rôle chargé du traitement A10i91 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i91

Jobs persistants/bail obligatoire OpenSpec, un travail actif A10i90 A et budget
global 60 s A10i87 A conservés. Paramètres de premier jet indépendants de l'ordre
A10i92 et de l'alerte A10i93 ; aucun bail CA/TLS ou droit métier remplacé.

| Choix validé | Durée nominale de bail | Renouvellement nominal |
| --- | --- | --- |
| B | 60 secondes | Toutes les 20 secondes |

Option B validée : 60 s/renouvellement 20 s. Option A 30/10 s non retenue.
Bail lié au travail/propriétaire/génération et périmètre courants ; autorité
Django/état durable admissible avant exécution/renouvellement. Origine/échéance
et engagement du renouvellement qualifiés ; envoi de demande sans bail prolongé
réputé acquis, ACK incertain réconcilié. Renouvellement à cadence nominale depuis
dernier engagement connu, sans nouvelle autorité sur simple horloge locale.
Expiration effective plafonnée par échéance de travail, mandat/contexte et
validités plus courtes ; renouvellement sans remise à zéro des 60 s, du compteur
de tentatives A10i89 ou du checkpoint. Renouveler n'est pas une nouvelle purge.
Horloges/bornes de bail, perte de continuité et propagation provider à qualifier,
sans U<=1 s A10i49 appliqué implicitement à ce rôle. Incertitude/absence de
renouvellement admissible bloque nouveaux effets à échéance sûre, anciennes
transactions suivies/réconciliées. Bail expiré seul sans exclusion effective
d'ancien acteur ne permet jamais le remplaçant A10i90.
B validée pour davantage de marge entre renouvellements ; coût I/O/réseau
et détection à mesurer. Cadence sans promesse de prise de relais 60 s,
perte réseau sans redémarrage permissif.
Paramètres configurables sous profil autorisé/versionné, couverture des
plateformes/providers et mécanismes à qualifier avant activation.
Aucun bail, timer, mandat, SQL, service, arrêt de processus ou OpenSpec modifiés.
Recette : renouvellement perdu/retardé, ACK inconnu, échéance globale plus courte,
ancien acteur vivant, horloge incertaine et aucun travail concurrent autorisé.
A10i91 B validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i91

- **WHEN** un profil revendique le traitement A10i91 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--de6f49130f

Source : `openspec/specs/pzt/spec.md`, ligne 10281. SHA-256 du bloc : `15cdb0c8520951834f6a88774ea8dfc8e8c7fe3d46ae32816806a045d5fbe2fd`.

~~~~text
### Requirement: Contrat A10i92 — Travaux de purge ordonnés par rotation déterministe des classes — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i92 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i92

Concurrence globale 1 A10i90 A, cadence nominale 24 h A10i85 A et contrôles
d'admissibilité conservés. Ordre de choix d'un travail prêt, indépendant du
bail/alerte ; pas de FIFO de cycles métriques contraire à A10i78.

| Choix validé | Ordre des travaux prêts admissibles | Conséquence |
| --- | --- | --- |
| A | Rotation logs/métriques/traces, plus ancien admissible dans la classe choisie | Partage du créneau entre classes |

Tour durable/courant et règle de départage déclarés par politique versionnée ;
classe sans travail prêt/admissible passée sans purge ni attente artificielle.
Après admission connue, choix suivant progresse selon règle durable ; échec
d'admission incertain sans tour/Job supposés absents, déduplication conservée.
Ancienneté globale toutes classes B non retenue comme règle alternative ;
ancienneté dans classe choisie et départage stable restent qualifiés.
Commun : admissibilité d'autorisation/hold/rétention/bail et capacité vérifiée
avant effet, ordonnancement sans élargissement de périmètre. Limites de travaux
en attente/ancienneté et diagnostics de retard à qualifier, aucune file illimitée
ou création d'un Job par réveil après panne. Lots 1 000 et budgets 60 s propres
aux travaux, classe ne reçoit pas automatiquement toutes les ressources.
Cadence 24 h reste par profil/classe concernés : plusieurs travaux dus peuvent
s'exécuter successivement sous créneau unique et autorisation, rotation sans
règle implicite « une seule classe par jour » ou garantie d'horizon de traitement.
Attente prolongée visible, sans réduction de rétention ou autre classe ignorée
silencieusement pour absorber backlog. Ordre des enregistrements d'un lot et
points de reprise A10i88 gardent leurs contrats qualifiés.
A validée pour partage entre classes ; coûts/débit/équité à mesurer. Stockage/contrat du tour et admission à qualifier,
pas de nouvelle autorité dans PA ou de durée légale déduite d'une priorité.
Capacité d’attente 3 travaux/un par classe A10i95 A validée le 9 octobre 2026.
Aucun ordonnanceur, worker, file, migration ou OpenSpec créés/modifiés ici.
Recette : classe vide/bloquée, tous travaux dus, même ancienneté, reprise du tour,
admission incertaine, classe très chargée et attente jamais masquée.
A10i92 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i92

- **WHEN** un profil revendique le traitement A10i92 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--50cc73e0dc

Source : `openspec/specs/pzt/spec.md`, ligne 10330. SHA-256 du bloc : `a5a57062e411a73c04ea7ae8eee1a9ebfde61442b0f91b792a6592062a93675d`.

~~~~text
### Requirement: Contrat A10i93 — Alerte de reliquat de purge après 2 observations qualifiées consécutives — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i93 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i93

Cadence 24 h, budget 60 s et purge sous contrôles courants conservés.
Alerte diagnostique distincte de l'export métrique A10i81 ; état/sécurité/audit
et obligations de conservation sans effet différé par ce seuil.

| Choix validé | Seuil d'alerte diagnostique | Conséquence |
| --- | --- | --- |
| A | Après 2 observations qualifiées consécutives laissant un reliquat éligible/admissible | Reliquat persistant signalé, diagnostic initial non différé |

Seuil A 2 observations validé ; seuil B dès première observation non retenu.
Observation déclarée par classe/périmètre/plan, compte au plus une fois par
occasion nominale ; lots/retries/renouvellements de bail sans plusieurs
observations artificielles. Reliquat mesuré/référencé admissible, données sous
hold/rétention non atteinte distinguées, jamais considérées purgeables pour
faire baisser compteur. Politique de mesure/contexte/couverture à qualifier.
Premier reliquat/échec et cause exposés dès constat, succès partiel sans travail
SUCCEEDED fictif. État inconnu/autorité indisponible sans zéro reliquat déduit ;
diagnostic propre immédiat, pas de suppression pour obtenir une mesure.
Observation courante confirmant absence de reliquat admissible clôt cette
alerte avec transition corrélée ; absence de métriques ou redémarrage ne vaut
pas guérison. Compteur/couverture après incident qualifiés, pas d'ancien état
sain restauré sans preuve ; aucune autorisation ou rétention modifiées par alerte.
Visibilité locale/PBO par contrats autorisés disponibles, sans nouvelle
notification externe, destinataire ou livraison instantanée imposés. Audit
métier/holds et refus de sécurité restent individuels/immédiats selon exigences.
Deux observations ne garantissent pas 48 h : retards, cadence/couverture,
créneau et provenance comptent, aucune promesse de temps universelle.
A validée pour filtrer reliquat isolé ; seuil de
premier jet configurable sous profil autorisé, besoins/volumes à qualifier.
Aucune alerte réelle, notification, purge, sonde destructive ou OpenSpec créés.
Recette : reliquat isolé/persistant, hold, état inconnu, compteur après reprise,
observation complète sans reliquat et audit/sécurité non différés.
A10i93 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i93

- **WHEN** un profil revendique le traitement A10i93 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e1460fd68b

Source : `openspec/specs/pzt/spec.md`, ligne 10379. SHA-256 du bloc : `2edb0d9351421e47718d12b30b0702501bac28daf6c3cecf9902b08cc5b3fab5`.

~~~~text
### Requirement: Contrat A10i94 — Audit des effets de purge par lot lié à un manifeste durable — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i94 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i94

Audit persistant OpenSpec, lots 1 000 A10i86 A et checkpoint par lot A10i88 A
conservés. Audit des effets de purge télémétrie, indépendant des admissions/
autorisations/activités administratives qui restent individuellement auditées.

| Choix validé | Granularité d'audit des effets | Conséquence |
| --- | --- | --- |
| A | Événement structuré par lot, lié à un manifeste durable des cibles exactes et résultats | Sélection/résultat vérifiables sous contrat qualifié, sans copie des contenus |

Identités travail/commande/opération, acteur/contexte/périmètre, politique/
version, sélection exacte bornée et résultats liés par références qualifiées.
Manifeste durable/intègre sans payload source, clés, secrets ou données
personnelles superflues ; référence à un lot mutable ou simple compteur
insuffisants pour prouver quelles cibles/effets sont couverts.
Effets partiels/confirmés/inconnus distingués, aucune purge globale annoncée
quand tous effets requis ne sont pas confirmés. Disponibilité/rétention du
manifeste et liaison à l'audit qualifiées, audit complet consultable sous droits.
Événement d'effet par enregistrement source B non retenu comme granularité
alternative ; audit individuel de sécurité/administration toujours préservé.
Commun : autorisation sensible, refus, changement de politique et actions
d'administration gardent événements obligatoires propres ; « par lot » sans
exception de sécurité/audit. Atomisation des effets/transactions/provider et
couplage audit/effet à qualifier, audit requis indisponible sans nouvel effet.
Audit jamais dérivé des métriques/logs ni point de reprise ; manifeste manquant
sans preuve complète inventée. Références de gouvernance/holds vérifiées avant
retrait de métadonnées A10i96, pas d'audit supprimé par âge de télémétrie.
A validée pour effet de lot sous preuve détaillée liée ; coûts/contrats de
conservation à qualifier. Format JSON A10i97, SHA-384 A10i98 et plafond 128 Kio A10i99
validés le 9 octobre 2026. Schéma/signature non sélectionnés ici,
aucun reçu racine A10i35 détourné.
Aucun événement, manifeste, nouvelle collecte de données, purge ou OpenSpec créés.
Recette : lot partiel, manifeste mutable/absent, références exactes, audit absent,
événement administratif individuel et reprise sans purge confirmée en double ni audit fictif.
A10i94 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i94

- **WHEN** un profil revendique le traitement A10i94 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--1101fe44b5

Source : `openspec/specs/pzt/spec.md`, ligne 10429. SHA-256 du bloc : `ed848b9e7253294b8a25db498f5684db65a20e4d55427d30b3c78ead716575b5`.

~~~~text
### Requirement: Contrat A10i95 — Attente de purge plafonnée à 3 travaux, un par classe — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i95 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i95

Concurrence active globale 1 A10i90 A, rotation de classes A10i92 A et Jobs
persistants conservés. Travaux PENDING/SCHEDULED prêts ou planifiés en attente
d'exécution dans ce profil, distincts des cycles métriques sans file A10i78.

| Choix validé | Attente maximale par autorité logique | Limite par classe |
| --- | --- | --- |
| A | 3 travaux | 1 pour journaux, 1 pour métriques, 1 pour traces |

Capacité A 3/un par classe validée, B 9/trois par classe non retenue.
Travail actif compté séparément sous limite 1, états retenus/ressources ou
réessais encore actifs jamais reclassés « attente » pour libérer un créneau
fictif. Admission coordonnée/durable, autorisation et déduplication persistantes.
Même commande/opération/contexte reconnus renvoie état existant, pas de nouvelle
place ; coalescence de réveils uniquement même plan/version/classe/périmètre/
mandat admissibles. Aucun mélange de tenants/périmètres ou élargissement de
cibles pour tenir dans un Job. Travail en attente déjà persisté sans éviction
silencieuse au profit d'une demande plus récente.
Capacité pleine => non-admission explicite diagnostiquée, aucune file secondaire
illimitée, Job fantôme, suppression de preuve ou relance de fond sans borne.
Plans/retards et périmètres non encore admis suivis selon contrat borné qualifié,
rotation/ancienneté conservées ; aucune garantie de délai faute de capacité.
Attente ne démarre pas budget actif 60 s ; à l'exécution contexte/bail/autorisation
courants réévalués, expiration sans ancien droit conservé. Durée maximale de
plan/attente et quotas d'autorité/hôte/volumétrie à qualifier séparément.
A validée pour un prochain travail par classe ; coûts/équité multi-périmètres
à mesurer. Paramètres configurables sous
profil autorisé/versionné, preuve de capacité à tenir volume et rétentions avant
activation, sans création d'autorité locale PA ou nouveau droit SQL.
Aucune file/Job/autorisation/ordonnanceur/purge ou OpenSpec créés/modifiés ici.
Recette : capacité exacte/plus un, même commande, contexte différent, attente
expirée, plusieurs périmètres, active/attente distincts et refus sans perte de Job.
A10i95 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i95

- **WHEN** un profil revendique le traitement A10i95 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--5cc1b0674d

Source : `openspec/specs/pzt/spec.md`, ligne 10478. SHA-256 du bloc : `0fac14e198e2ade0b4ca69ee5d78ae7d85af95b044a3a137676613ec4fb1dcc9`.

~~~~text
### Requirement: Contrat A10i96 — Rétention nominale des métadonnées terminales de purge à 14 jours — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i96 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i96

Jobs persistants et audit métier séparé conservés. Défaut nominal configurable
pour nouveaux profils concernés, existant préservé ; métadonnées opérationnelles
de travail hors artefacts/preuves encore nécessaires à une reprise ou un audit.

| Choix validé | Rétention nominale après issue terminale durable confirmée | Conséquence |
| --- | --- | --- |
| A | 14 jours | Historique opérationnel court, références nécessaires conservées séparément |

Durée A 14 jours validée, B 30 jours non retenue.
Jour nominal 86 400 s : A = 1 209 600 s. Point de départ =
issue terminale durable/admissible confirmée et références cohérentes ; état
FAILED/DEAD_LETTER ou timer sans résultat réconcilié ne prouvent pas terminalité
sans reprise requise. États Jobs autorisés sans nouveau statut « purgé » implicite.
Travail actif/en attente/PAUSED/RETRYING, effets inconnus, bail/ancien acteur
non exclus ou reprise encore possible hors éligibilité de retrait par ce délai.
Âge seul jamais permission de supprimer : autorisation/holds/références/audit/
projections vérifiés, irrecevabilité de rejeu ancien et anti-résurrection après
restauration qualifiées. Compteurs/checkpoints/déduplication requis pas retirés
tant que l'absence d'un Job pourrait permettre nouveau droit ou double effet.
Manifeste d'audit A10i94, événements d'audit et pièces/reçus/dossiers métier
sous leurs exigences propres ; référence encore nécessaire bloque retrait,
aucune archive/backend supplémentaire ou durée d'audit déduits automatiquement.
Copie/réexport/reprise sans réinitialisation d'âge ; source/horloge/bornes et
procédure de retrait à qualifier. Quota plein sans effacement prématuré ou
travail ancien présenté comme nouveau ; diagnostic/audit minimal sans secrets.
A validée comme premier jet de suivi opérationnel court ; besoins/volumes/
qualification et politique versionnée/habilitée
requis. Aucun historique, checkpoint, Job, audit ou OpenSpec purgés/modifiés.
Recette : terminalité réelle/ambiguë, référence d'audit vivante, ancien acteur,
hold, restauration/rejeu et absence de remise à zéro d'autorisation ou compteur.
A10i96 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i96

- **WHEN** un profil revendique le traitement A10i96 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

