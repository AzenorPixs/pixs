# Références normatives — Z20

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 9109 | [Contrat A10i69 — Métriques techniques à dimensions stables et finies — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L9109) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9267 | [Contrat A10i72 — Métriques de collecte plafonnées à 64 séries ordinaires et 1 débordement — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9267) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9377 | [Contrat A10i74 — Tampon d'export métrique plafonné à 256 Kio de charges utiles — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9377) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9429 | [Contrat A10i75 — Export métrique périodique à intervalle nominal de 30 secondes — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9429) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9480 | [Contrat A10i76 — Cycle d'export métrique borné à 5 secondes globales — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9480) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9532 | [Contrat A10i77 — Un seul pipeline d'export métrique actif par instance — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9532) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9581 | [Contrat A10i78 — Cycles métriques sans file, non lancés lorsque l'export est occupé — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9581) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9631 | [Contrat A10i79 — Temporalité cumulative des sommes et histogrammes métriques compatibles — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9631) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9681 | [Contrat A10i80 — Erreurs techniques répétées regroupées sur fenêtre nominale de 30 secondes — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9681) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9731 | [Contrat A10i81 — Alerte d'export après 3 occasions défavorables consécutives — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9731) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9782 | [Contrat A10i82 — Rétention nominale des journaux techniques de collecte à 7 jours — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9782) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9834 | [Contrat A10i83 — Rétention nominale des points métriques agrégés à 30 jours — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9834) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9885 | [Contrat A10i84 — Rétention nominale des traces techniques à 24 heures — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9885) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--cc057c30a8

Source : `openspec/specs/pzt/spec.md`, ligne 9109. SHA-256 du bloc : `0cf07cde061f26c390783dfbc2a72b126498d2c2ca11e83660326a893f185aec`.

~~~~text
### Requirement: Contrat A10i69 — Métriques techniques à dimensions stables et finies — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i69 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i69

Métriques agrégées/journaux transitions-erreurs A10i60 A et observabilité/audit
OpenSpec conservés. Dimensions stables/finies A validées, indépendantes du
format/quota de l'état ; aucune nouvelle télémétrie métier imposée.

| Choix validé | Dimensions des séries métriques | Conséquence |
| --- | --- | --- |
| A | Dimensions stables issues d'ensembles finis approuvés, aucune dimension par requête/incarnation | Détail individuel dans traces/journaux corrélés, combinaisons à qualifier |

Rôles/providers/catégories de profil et codes de résultat/qualité minimaux
choisis dans listes finies qualifiées. Pas d'ID requête/opération/cycle/PA,
PID, incarnation, timestamp, nom d'hôte ou texte libre servant de dimension
de série. Identité de ressource et isolation des périmètres toujours contrôlées ;
profil n'autorise pas des ressources dynamiques infinies sous autre champ.
Dimension métrique par incarnation B non retenue ; détail individuel
conservé dans journaux/traces corrélés sous droits/rétentions propres.
Commun : noms/types/unités, ensembles de valeurs et produit de combinaisons,
limites par instrument/instance/export et agrégation de débordement à
qualifier ; aucune cardinalité illimitée déduite d'un ensemble individuel fini.
Signaux/corrélation/trace requis conservés par mécanismes appropriés, avec
journaux/traces corrélés et exemplaires liés aux traces lorsque qualifiés,
sans imposer ID de trace/requête en dimension de toutes séries métriques.
Agrégation sans double comptage, mesure perdue non présentée comme succès
ou absence de panne, overflow/collecte indisponible diagnostiqués sous politique.
Données personnelles/secret/contenu JSON/dossier jamais exposés, droits et
rétentions propres conservés. Audit métier persistant distinct, aucune suppression
de son détail obligatoire pour réduire la cardinalité technique.
A validée pour réduire combinaisons et coût d'observation, coûts réels à
mesurer. Plafond de séries A10i72 A validé le 9 octobre 2026 ; profil
précis et limites à qualifier, aucun exporter adopté ici.
[OpenTelemetry, Metrics SDK](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)
décrit contrôle de cardinalité/agrégation ; politique choisie par Pixs,
aucun SDK/version installés ni suppression de signal OpenSpec autorisée.
Recette : changements d'incarnation, valeurs libres/non admises, overflow,
corrélation métrique-trace-log, absence de télémétrie technique et audit requis
indisponible, sans secret ou quota illimité implicitement acceptés.
A10i69 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i69

- **WHEN** un profil revendique le traitement A10i69 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--5de1dac066

Source : `openspec/specs/pzt/spec.md`, ligne 9267. SHA-256 du bloc : `b1fc1776389d59e83122618d0a09c568f569d03f673050228ad35430672296f8`.

~~~~text
### Requirement: Contrat A10i72 — Métriques de collecte plafonnées à 64 séries ordinaires et 1 débordement — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i72 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i72

Dimensions stables A10i69 A et agrégation A10i60 A conservées. Plafond A validé
comme premier jet
par instrument, instance logique et cycle de collecte, indépendant du stockage
technique et sans limite imposée au nombre d'événements d'audit métier requis.

| Choix validé | Séries ordinaires au maximum | Série de débordement réservée | Total maximal par instrument/cycle |
| --- | --- | --- | --- |
| A | 64 | 1 | 65 |

64 séries ordinaires plus 1 débordement retenues ; plafond B 256 plus 1
non adopté. Limites inclusives sur combinaisons de dimensions après filtrage qualifié ;
ressources et autres attributs ne permettent pas contourner portée du quota.
Série de débordement préparée pour observations ne pouvant être agrégées
individuellement, pas de nouvelle série par valeur/raison de dépassement.
Pour instruments synchrones, chaque observation reflétée une fois dans série
ordinaire ou débordement ; pas de double comptage/perte silencieuse. Pour
instruments asynchrones, politique d'observation/agrégation cohérente et
sémantique de disponibilité explicitement qualifiées, aucune garantie de
somme générale déduite d'une sélection de gauges instantanées.
Ordre de sélection et temporalité déclarés par profil ; un changement de
dimension/incarnation/exporter ne transforme pas un quota en capacité infinie.
Nombres d'instruments, cycles, fréquence d'export, ressources agrégées d'hôte/
backend, coûts de rétention et limites globales à qualifier séparément ;
65 points au plus par instrument/cycle ne prouvent pas seuls mémoire maximale.
Plafonds de premier jet configurables sous profil autorisé/versionné, avec
contrôle d'overflow et conservation de corrélation/logs/traces requis. Profil
incapable d'agrégation compatible refusé avant activation, aucun SDK/version/
exporter installé ou quota automatique déduit d'une valeur par défaut tierce.
Collecte technique indisponible diagnostiquée selon OpenSpec, sans audit
reconstitué ou preuve de temps inventée depuis métriques manquantes.
A validée comme enveloppe sobre pour dimensions restreintes ; coûts à mesurer.
Tampon 256 Kio/intervalle 30 s A10i74/A10i75 A validés le 9 octobre 2026. Choix Pixs, pas de valeur
prescrite par [OpenTelemetry, cardinalité](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits),
qui décrit mécanismes de limite et d'agrégation. Toutes plateformes à qualifier,
aucune variable/runtime/politique OpenSpec modifiés ici.
Recette : 64 combinaisons puis dépassement, overflow réservé, somme/corrélation,
temporalité asynchrone, dimension libre, exporter changé et audit requis absent.
A10i72 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i72

- **WHEN** un profil revendique le traitement A10i72 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--88f5b461ba

Source : `openspec/specs/pzt/spec.md`, ligne 9377. SHA-256 du bloc : `bd8a3df83c28682902bf85cbd6d70213eb6c684dbf074c971b209d5ec00ed94d`.

~~~~text
### Requirement: Contrat A10i74 — Tampon d'export métrique plafonné à 256 Kio de charges utiles — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i74 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i74

Métriques A10i69/A10i72 A conservées. Enveloppe technique d'export, indépendante
du stockage d'état A10i68 et du plafond mémoire de l'auxiliaire A10i59.

| Choix validé | Plafond total des charges utiles métriques retenues par instance | Conséquence |
| --- | --- | --- |
| A | 256 Kio | Tampon restreint, saturation explicitement diagnostiquée |

Plafond A retenu : 262 144 octets inclusifs ; plafond B 1 Mio non adopté.
Comptage sur somme des octets
encodés exacts des charges utiles retenues, en attente/en cours/relance.
Chaque copie conservée compte ; plafond appliqué avant rétention/allocation
de payload, format SDK/protocole/compression sans possibilité de contourner
par annonce de taille. Comptabilisation et émission progressive qualifiées.
Il s'agit du contenu encodé retenu, pas d'un plafond démontré de RSS : états
d'agrégation, objets SDK, threads, buffers réseau et overhead à borner/qualifier
séparément ; nombre de payloads/exports concurrents et budgets de durée explicites.
Saturation/transport indisponible : traitement borné selon politique qualifiée
d'agrégation/perte technique diagnostiquée, aucune accumulation infinie, écriture
de spool disque implicite ou blocage indéfini du chemin métier/collecte de preuve.
Pas de succès d'export inventé, absence de donnée présentée comme absence de
panne, double comptage ou quota remis à zéro par reconnexion. Temporalité delta/
cumulative et reprise compatibles avec les limites A10i72, pertes éventuelles
signalées ; garantie de livraison technique sans perte non déduite du tampon.
Audit métier requis reste distinct/durable, jamais placé dans ce tampon ou
supprimé pour tenir dans quota ; preuve de temps manquante suit ses propres
refus. Logs/traces/santé obligatoires conservent leurs contrats et budgets.
Paramètre de premier jet configurable sous profil autorisé/versionné et
qualification ; aucune hausse automatique ni choix de format/backend/canal/
endpoint d'export, aucun réseau ou permission supplémentaire ouverts.
A validée pour contenu technique borné ; effets sur consommation/livraison
à mesurer. Délai 5 s/pipeline unique/absence de file A10i76–A10i78 A validés le 9 octobre 2026. Plateformes à qualifier,
aucun buffer réel, spool, exporter, dépendance ou OpenSpec créés/modifiés.
Recette : taille exacte/plus un, copies en cours et en attente, payload trop
grand, serveur absent, reprise delta/cumulative, circuit et audit inchangés.
A10i74 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i74

- **WHEN** un profil revendique le traitement A10i74 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--75a34a4fa6

Source : `openspec/specs/pzt/spec.md`, ligne 9429. SHA-256 du bloc : `e93b42c7b2cc95599e113c5fd97d965ffac8a2a3e94e973a7e900a8e0db3956b`.

~~~~text
### Requirement: Contrat A10i75 — Export métrique périodique à intervalle nominal de 30 secondes — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i75 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i75

Agrégation/corrélation A10i60/A10i69/A10i72 A conservées. Intervalle 30 s A
validé comme premier jet pour
profil d'export périodique, indépendant du tampon A10i74 ; aucun exporter,
transport ou destination choisis, contrat pull non remplacé implicitement.

| Choix validé | Intervalle nominal d'export | Conséquence |
| --- | --- | --- |
| A | 30 secondes | Moins de cycles que 10 secondes, visibilité agrégée moins fréquente |

Intervalle B 10 s non retenu comme alternative. Intervalle configurable sous profil autorisé/versionné, mesure monotone et
périmètre des instruments qualifiés. Cadence nominale sans promesse de livraison,
latence maximale, disponibilité serveur ou consommation réelle démontrées.
Retard/échec sans rafale de rattrapage ni exports simultanés non bornés ;
durées/annulation/reprises d'export à qualifier, tampon/capacité respectés.
Cycle métrique observe les états techniques admissibles, sans déclencher
acquisition temporelle de preuve au repos ou relance métier ; fréquence de
synchronisation infrastructure, budgets A10i52 et fraîcheur A10i49 inchangés.
Erreurs/transitions et contrôles de sécurité non différés jusqu'au prochain
cycle pour seul motif d'intervalle ; journaux/traces/santé restent leurs signaux
propres, audit métier requis sans report/sampling lié à export métrique.
Exporter indisponible selon observabilité/audit OpenSpec, aucune opération
autrement conforme bloquée par seule absence de télémétrie ; preuve temporelle
ou audit obligatoire indisponibles traités selon exigences respectives.
PBO–PA garde PZT/mTLS pour ses échanges, destination/canal d'observabilité et
droits d'accès à qualifier dans frontières autorisées, jamais déduits du SDK.
A validée comme premier jet sobre en cycles ; coûts, alertes et profils à
mesurer sur toutes plateformes, délai global 5 s A10i76 A validé le 9 octobre 2026.
[OpenTelemetry, lecteur métrique périodique](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)
décrit configuration d'intervalle/timeout ; 30 secondes choisies par Pixs,
aucune valeur par défaut tierce ou version SDK adoptées.
Aucun timer, exporter, sonde de temps ou OpenSpec créés/modifiés ici.
Recette : cycle retardé/serveur absent, absence de rattrapage infini, repos
auxiliaire, erreur entre cycles, tampon saturé et audit requis non différé.
A10i75 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i75

- **WHEN** un profil revendique le traitement A10i75 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--cabb815afc

Source : `openspec/specs/pzt/spec.md`, ligne 9480. SHA-256 du bloc : `8227f48119a56efd7a77b3fd6bb1e7cc19d97e66dc2693ff272a831303cc29a9`.

~~~~text
### Requirement: Contrat A10i76 — Cycle d'export métrique borné à 5 secondes globales — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i76 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i76

Intervalle 30 s A10i75 A et tampon 256 Kio A10i74 A conservés. Budget logique
d'un cycle périodique, indépendant des pipelines A10i77 et de l'attente A10i78 ;
distinct du budget de preuve temporelle A10i52.

| Choix validé | Délai global maximal par cycle | Conséquence |
| --- | --- | --- |
| A | 5 secondes | Budget court pour collection/encodage/export, dépassement diagnostiqué |

5 secondes A validées comme premier jet configurable, B 10 secondes non
retenues. Début monotone à
l'acceptation du cycle, attente éventuelle, collection technique, callbacks,
encodage, connexion/émission/accusé et relances internes inclus jusqu'à décision
d'issue. Échéance unique non remise à zéro par batch, socket, reconnexion ou
tentative ; sous-appels bornés au temps restant, pas de timeout 5 s répété
par fragment créant un cycle sans borne globale.
Découpage éventuel en batches respecte ordre, plafond total et échéance globale ;
timeout SDK par batch ne prouve pas ce budget de bout en bout. Contrat/API et
annulation qualifiés avant activation, pas de deadline supposée annulant
instantanément syscall, callback ou ressources en cours.
Dépassement : aucun nouveau sous-appel, issue tardive sans succès annoncé dans
ce cycle, échec/incertitude technique diagnostiqués. Arrêt/libération effectifs
suivis avant slot réutilisé A10i77 ; aucune accumulation de tâches dont fin
n'est pas prouvée, aucun arrêt du PBO/PA ou du collecteur de preuve pour
récupérer une ressource d'export. Chemin métier sans attente de cet export.
Livraison inconnue sans ACK non assimilée à absence de réception ; temporalité/
déduplication/protocole et traitement de résultats partiels à qualifier, aucune
relance métier ou compensation audit déduites d'un timeout métrique.
A validée pour borne courte, coûts et couverture plateforme à mesurer ;
aucune livraison complète ou instantanéité d'arrêt
garanties. [OpenTelemetry, lecteur périodique](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)
décrit des timeouts/batches ; ce budget global est choisi par Pixs, pas de
valeur tierce adoptée. Aucun timer, SDK/runtime ou OpenSpec modifiés ici.
Recette : attente/encodage lent, batches multiples, ACK tardif/absent, relance
interne, callback bloqué et délai jamais remis à zéro ni slot repris prématurément.
A10i76 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i76

- **WHEN** un profil revendique le traitement A10i76 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--bb8eeea9a8

Source : `openspec/specs/pzt/spec.md`, ligne 9532. SHA-256 du bloc : `eed3d6a4f3a1e2ce5dfc6031980450fd6fddb6b6c984ed9c701f11c131d93f93`.

~~~~text
### Requirement: Contrat A10i77 — Un seul pipeline d'export métrique actif par instance — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i77 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i77

Tampon partagé 256 Kio A10i74 A, cardinalité A10i72 A et observabilité OpenSpec
conservés. Nombre de pipelines techniques actifs par instance logique, distinct
du maximum d'un auxiliaire de preuve A10i54 ; aucun nouveau processus imposé.

| Choix validé | Pipelines actifs au maximum | Conséquence |
| --- | --- | --- |
| A | 1 | Sérialisation globale de la publication métrique de collecte |

Un seul pipeline possédé, collection/publication/flush concernés sérialisés ;
export encore actif ou arrêt non prouvé sans nouveau pipeline. Appels d'export
d'une même instance d'exporter jamais concurrents, cycles/batches ordonnés.
Deux pipelines/partitions B non retenus comme exécution alternative ;
aucun dédoublement pour contourner occupation, timeout ou quotas.
Commun : limite totale 256 Kio sur pipeline unique, profils et
quotas jamais multipliés par création d'exporters ; cardinalité par instrument/
instance/cycle A10i72 conservée. Comptes/threads/contexte/réseau et ressources
agrégées à qualifier, aucune nouvelle permission ou source métier déduite.
Collection/reporting partiels diagnostiqués, pas de succès global si une
étape requise échoue. APIs de collecte/flush/arrêt coordonnés et attentes
bornées ; perte de slot sans workers de remplacement accumulés, libération
effective requise avant réutilisation. Reprise du parent A10i73 et autorisations
courantes sans compteurs réinitialisés par incarnation d'export.
A validée pour flux restreint et coordination simple ; coûts à mesurer
avant activation, temporalité cumulative compatible A10i79 A validée le 9 octobre 2026.
[OpenTelemetry, Metrics SDK](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)
prescrit sérialisation d'exports d'un même reader/exporter ; restriction
maintenue par le profil Pixs, aucun exporter/SDK concret choisi.
Délai A10i76 et attente A10i78 indépendants, aucun SDK/version/processus,
partition réelle ou OpenSpec créés/modifiés.
Recette : cycle pendant export, flush concurrent, tentative de pipeline concurrent,
ACK partiel, quota partagé, ancien export toujours actif et aucun nouveau worker.
A10i77 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i77

- **WHEN** un profil revendique le traitement A10i77 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--ecd2a0ceea

Source : `openspec/specs/pzt/spec.md`, ligne 9581. SHA-256 du bloc : `974f1b5ccbfa38bf03268977e416c71b6e8dc954541d22725b75c3801dd7fb5c`.

~~~~text
### Requirement: Contrat A10i78 — Cycles métriques sans file, non lancés lorsque l'export est occupé — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i78 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i78

Cadence 30 s A10i75 A, tampon A10i74 A et budget/pipeline A10i76/A10i77 A
conservés. Choix d'admission technique, indépendant d'une relance d'opération
métier ou de la non-admission de capacité A10i41/A10i42.

| Choix validé | Gestion de l'occupation | Conséquence |
| --- | --- | --- |
| A | Aucune file ; cycle périodique non lancé si aucun slot disponible | Pas de backlog, publication suivante à cadence normale sous capacité admissible |

Occupation vérifiée avant démarrage ; cycle non lancé diagnostiqué comme
tel, aucun succès, snapshot envoyé ou collecte périodique fictifs. Instruments
peuvent continuer leur agrégation bornée selon temporalité/profil, sans payload
mis en attente pour contourner absence de file. Prochain cycle nominal seulement
sous slot effectivement libre et contrôles courants, pas de rafale de rattrapage.
Demande de cycle en attente B non retenue ; occupation sans cycle mis en
file, échéance ou payload fictifs.
Commun : cycle non lancé distinct de succès/échec/livraison inconnue, corrélation
conservée sans dimension métrique par requête. Temporalité/intervalle réel et
pertes/gauges non observées qualifiés, aucune garantie sans perte déduite du
saut de cycle ou de l'agrégation. Cycles distincts sans mélange de batches
incompatible avec reader/exporter, aucun compteur de reprise technique ou
délai métier remis à zéro par ce choix. Audit requis persistant et signaux
logs/traces/santé distincts, seule absence d'export sans métier conforme bloqué.
Cycle sauté sans lecture de preuve temporelle
au repos ; A10i51/A10i52, quotas et permission d'acquisition restent inchangés.
A validée pour éviter backlog et ressources retenues, effets sur visibilité
et pertes à mesurer. La stratégie reste
à qualifier sur toutes plateformes ; aucun calendrier/exporter/queue réelle
ou OpenSpec créés/modifiés. [OpenTelemetry, lecteur périodique](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)
permet de différer ou sauter une collection quand l'export précédent continue ;
le plafond d'attente et budgets ici sont proposés par Pixs.
Recette : slot occupé/arrêt non prouvé, absence de file, retard sans rafale,
flush demandé sous occupation, agrégation delta/cumulative et audit non différé.
A10i78 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i78

- **WHEN** un profil revendique le traitement A10i78 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--cc82d9528b

Source : `openspec/specs/pzt/spec.md`, ligne 9631. SHA-256 du bloc : `8c02b8f0646f57bd8421f272618e96dd0bb6e4427bb80d88092c573c095e2b89`.

~~~~text
### Requirement: Contrat A10i79 — Temporalité cumulative des sommes et histogrammes métriques compatibles — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i79 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i79

Pipeline unique A10i77 A, cadence 30 s A10i75 A et cycles sans file A10i78 A
conservés. Temporalité des sommes/histogrammes qui la supportent, indépendante
du regroupement de logs A10i80 et du seuil d'alerte A10i81.

| Choix validé | Temporalité métrique | Conséquence |
| --- | --- | --- |
| A | Cumulative pour sommes/histogrammes compatibles, origine explicite | Totaux depuis origine dans agrégation bornée, gaps/resets distingués |

Origine et époque de production déclarées, chaque point couvre période
depuis origine courante ; snapshots successifs jamais additionnés comme deltas.
Échec/saut d'export sans remise à zéro de la somme pour seul motif de transport.
Redémarrage/perte d'état d'agrégation => nouvelle origine/gap explicitement
signalés, pas de faux cumul continu ou récupération depuis état de reprise A10i66.
Delta B non retenue comme temporalité alternative automatique ;
protocole/réception inconnue sans double comptage, gaps sans zéro fictif.
Commun : gauges restent mesures instantanées selon leur type, pas cumulative/
delta forcées ; types/unités/histogrammes et min/max/quantiles compatibles
qualifiés, aucun calcul d'intervalle sans données suffisantes. Origine/époque
dans métadonnées appropriées, sans dimension par incarnation contraire à A10i69.
Cardinalité 64 plus 1 A10i72, agrégateur/RAM, tampon 256 Kio et délai 5 s
respectés ; état cumulatif sans croissance illimitée ni toutes mesures brutes
conservées. Cumul ne garantit pas livraison sans perte, conservation des gauges,
min/max par intervalle ou reconstruction de chaque événement.
A validée pour totaux compatibles après export intermittent ; coût côté
producteur/backend à mesurer, aucun gain mémoire
universel. [OpenTelemetry, modèle métrique](https://opentelemetry.io/docs/specs/otel/metrics/data-model/#temporality)
décrit ces sémantiques ; préférence choisie par Pixs, aucun SDK/backend/
convertisseur sélectionné. Profil incompatible refusé sans repli automatique,
audit métier/preuve temporelle distincts, aucun OpenSpec modifié.
Rétention des points 30 jours A10i83 A validée le 9 octobre 2026.
Recette : cycle sauté, ACK inconnu, reset producteur, origine perdue, gauge,
histogramme incompatible et aucune somme doublée ou donnée manquante inventée.
A10i79 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i79

- **WHEN** un profil revendique le traitement A10i79 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--2dfebc72a6

Source : `openspec/specs/pzt/spec.md`, ligne 9681. SHA-256 du bloc : `223b7d9c82b396e16548d75bfafcd64dea0a84b28e830d29c9e108ae2177a980`.

~~~~text
### Requirement: Contrat A10i80 — Erreurs techniques répétées regroupées sur fenêtre nominale de 30 secondes — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i80 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i80

Logs transitions/erreurs A10i60 A, signaux corrélés et audit OpenSpec conservés.
Regroupement A validé pour répétitions équivalentes, indépendant de temporalité et
alerte ; aucun audit métier requis regroupé ou supprimé.

| Choix validé | Journalisation des répétitions techniques | Conséquence |
| --- | --- | --- |
| A | Premier événement individuel puis résumé compté sur fenêtre nominale de 30 secondes | Répétitions regroupées, première erreur et transitions visibles |

Première occurrence émise sans attendre fin de fenêtre, regroupement selon
cause/code/composant/profil/stade équivalents et contexte admissible, clés finies
sans texte libre/secret comme regroupement. Résumé donne compte exact connu,
période et corrélations minimales appropriées ; transitions/changement de cause
et événement exigeant diagnostic individuel hors regroupement.
Fenêtre monotone sans remise à zéro opportuniste par reconnexion ; répétition
non effacée pour sembler guérie. Groupes/mémoire/volumes bornés à qualifier,
perte de résumé/état ou collecte indisponible diagnostiquées, aucun compte exact
inventé après crash ou reprise. Réconciliation/audit persistants séparés.
Événement technique systématique pour chaque répétition B non retenu ;
aucune réponse brute ou donnée sensible ajoutées au résumé.
Commun : obligations individuelles de sécurité, audit persistant et traces
requises préservées ; A ne change ni échec fermé ni contrôles avant opération.
Erreur de sécurité/autorisation ou administration nécessitant audit individuel
reste individuellement auditée, jamais remplacée par résumé technique.
30 s constituent premier jet configurable, pas de délai imposé à action de
sécurité ou visibilité initiale ; cadence métrique A10i75 ne pilote pas fenêtre
de logs et journalisation indisponible ne bloque pas métier autrement conforme.
A validée pour réduire volume des répétitions ;
coûts et corrélation à qualifier par plateforme. Aucun système de logs, nouvelle
collecte de données, backend, timer ou OpenSpec créés/modifiés.
Rétention des logs 7 jours A10i82 A validée le 9 octobre 2026.
Recette : première erreur, répétitions équivalentes/non équivalentes, transition,
fin de fenêtre, résumé perdu, événement de sécurité et audit individuel conservé.
A10i80 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i80

- **WHEN** un profil revendique le traitement A10i80 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c3c634b4ef

Source : `openspec/specs/pzt/spec.md`, ligne 9731. SHA-256 du bloc : `3992c6651d8fd7af9ed6d02b5c7531a897c03ff6c166865741cf75c48da3b04e`.

~~~~text
### Requirement: Contrat A10i81 — Alerte d'export après 3 occasions défavorables consécutives — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i81 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i81

Cadence 30 s, deadline 5 s, pipeline unique et absence de file conservés.
Seuil A 3 occasions validé pour alerte diagnostique d'export ; état de santé, logs d'erreur,
refus de sécurité et audit obligatoires restent leurs contrats propres.

| Choix validé | Déclenchement d'alerte diagnostique | Conséquence |
| --- | --- | --- |
| A | Après 3 occasions périodiques consécutives sans export complet confirmé | Moins d'alertes sur échec isolé, diagnostic initial et santé non différés |

Seuil B dès première occasion non retenu comme règle d’alerte alternative.
Une occasion nominale compte au plus une fois, résultat connu : échec/timeout,
export incomplet/inconnu ou cycle non lancé faute de slot. Sous-appels/retries/
batches sans trois événements artificiels ; cycle en cours non déclaré réussi.
Détection de l'état technique dégradé et premier diagnostic dès première issue
défavorable, sans attendre ce seuil. Sécurité/temps/audit manquants immédiatement
traités selon leurs exigences, jamais différés par compteur d'alerte.
Succès complet admissible d'une occasion courante rompt série d'échecs et clôt
cette alerte avec transition corrélée ; batch partiel, ACK tardif d'ancien cycle
ou silence du backend insuffisants. Aucun autre motif de santé effacé.
Alerte locale/diagnostique visible au PBO par canal autorisé disponible, sans
nouvelle destination, mail, notification ou livraison instantanée imposés.
L'alerte ne dépend pas exclusivement du flux métrique en panne : état local
et consultation qualifiés. L'absence de données reçues ne prouve ni réussite
ni cause certaine de l'échec au backend.
Redémarrage/perte de compteur sans état automatiquement déclaré sain ;
origine/couverture inconnues exposées et contrôles repris selon profil courant,
aucune reprise d'export ou remise à zéro de circuit A10i63 autorisée par alerte.
3 occasions ne constituent pas garantie de délai 90 s : cadence nominale,
retards/indisponibilités et provenance qualifiés, aucune accumulation/rafale.
A validée pour limiter alertes isolées ; seuil de
premier jet configurable sous politique autorisée/versionnée. Plateformes et
interface à qualifier, aucun abonnement/notification/commande ou OpenSpec créés.
Recette : un/trois échecs, cycles sautés, batch partiel, ACK ancien, succès complet,
parent repris avec couverture inconnue et contrôle de sécurité non différé.
A10i81 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i81

- **WHEN** un profil revendique le traitement A10i81 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--41c2872ee1

Source : `openspec/specs/pzt/spec.md`, ligne 9782. SHA-256 du bloc : `8b18e96a622aa24113b8a1886de549aed027a5204d197ea219c073eee79b693a`.

~~~~text
### Requirement: Contrat A10i82 — Rétention nominale des journaux techniques de collecte à 7 jours — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i82 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i82

Journaux A10i60/A10i80 A et gouvernance/observabilité OpenSpec conservés.
Durée A 7 jours validée comme défaut nominal configurable des nouveaux
profils concernés, politique
existante préservée ; indépendante de métriques A10i83 et traces A10i84.

| Choix validé | Rétention nominale des journaux techniques | Conséquence |
| --- | --- | --- |
| A | 7 jours | Historique technique court, volume durable à qualifier |

Jour nominal = 86 400 secondes ; A = 604 800 s. Durée B 30 jours non retenue.
Âge depuis
première persistance durable au backend autorisé, référence conservée à
réexport/rotation/restauration ; heure de l'événement distincte, pas de remise
à zéro par copie ou réingestion. Champ exact/horloge/bornes/provenance à qualifier,
aucun budget de preuve A10i49 automatiquement transposé à la purge.
Logs individuels et résumés conservés sous leur contrat corrélé, aucun secret,
payload brut, droit nouveau ou log technique devenu audit. Horizon nominal
ne garantit pas présence de logs jamais reçus ou compte exact après perte A10i80.
Échéance rend candidat à expiration selon politique, jamais seule permission
de purge : autorisation explicite, règles/holds/références/projections et audit
du travail idempotent requis selon OpenSpec. Temps/provenance incertains sans
suppression fondée sur âge présumé, quota sans purge prématurée.
Dérivés, index/caches/exports et reprises/sauvegardes sous politique de gouvernance
pour éviter republication de contenu purgé ; pas de durée de sauvegarde ou
procédure technique automatiquement déduites. Changement de durée versionné/
autorisé et impacts sur historique vérifiés, aucun écrasement des profils existants.
A validée comme premier jet court pour diagnostics techniques ; besoins/
volumes/couverture à qualifier. Rétention d'audit métier,
dossiers/pièces/reçus A10i35, marqueurs A10i44–A10i46 et état A10i66 inchangés.
Profil/backend doivent déclarer stockage, accès, quotas et expiration ; pas de
spool ou conservation durable locale imposés à tous PA ordinaires. Aucun log,
index, fichier ou OpenSpec purgés/modifiés ici, aucune conformité externe déclarée.
Recette : seuil exact/avant, réingestion, horloge incertaine, hold, quota,
projection/sauvegarde restaurée et audit requis conservé.
A10i82 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i82

- **WHEN** un profil revendique le traitement A10i82 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--f4612442df

Source : `openspec/specs/pzt/spec.md`, ligne 9834. SHA-256 du bloc : `b81f98ce09aeda5addf7d7d618206339567bf7434d76e54adc723d5aaa681d25`.

~~~~text
### Requirement: Contrat A10i83 — Rétention nominale des points métriques agrégés à 30 jours — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i83 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i83

Cumulatif compatible A10i79 A, dimensions/cardinalité A10i69/A10i72 A conservés.
Durée A 30 jours validée comme défaut nominal configurable des points
stockés au backend autorisé, pour nouveaux
profils concernés sans politique existante remplacée ; indépendante des logs/traces.

| Choix validé | Rétention nominale des points métriques | Conséquence |
| --- | --- | --- |
| A | 30 jours | Suivi de tendances, stockage/résolution à qualifier |

Jour nominal = 86 400 s ; A = 2 592 000 s. Durée B 90 jours non retenue.
Âge depuis première
persistance durable du point au backend, origine/temps de mesure distincts ;
export répété d'un même point sans prolongation de rétention ni double comptage.
Nouveau point cumulé et ancien point ont leurs propres références de rétention,
origine/reset/gap préservés ; expiration d'un point ne réinitialise pas agrégateur,
compteur de reprise ou politique d'alerte. Format/provenance/déduplication à qualifier.
30 jours sans présomption de toutes données livrées, capacité mémoire/CPU ou
quota global : fréquence réelle, instruments, séries, résolutions et coût backend
à mesurer. Aucun downsampling automatique ou agrégat historique après horizon
adoptés ; tout dérivé supplémentaire exige contrat/rétention propres déclarés.
Horloge qualifiée et expiration selon politique/gouvernance ; âge seul sans
purge autorisée, holds/références/audit/dérivés contrôlés, restauration sans
résurrection de points purgés. Quota plein sans ancien point courant transformé
en nouveau pour masquer perte, ni audit métier supprimé pour tenir dans quota.
A validée comme premier jet pour suivi de tendances ; besoins/couverture à
qualifier, pas de durée imposée par
OpenTelemetry ou obligation externe revendiquées. Tampon 256 Kio A10i74,
état durable A10i66, logs A10i82 et traces A10i84 gardent leurs périmètres.
Pas de stockage métrique de 30 jours dans RAM de chaque PA ou accès direct
SQL du PA déduits ; backend/droits/profil à qualifier sous autorité Django.
Aucun point/agrégat/base de données ou OpenSpec créés/purgés/modifiés.
Recette : point réexporté, origine cumulative/reset, point expiré, nouveau point,
hold, quota, temps incertain et restauration sans total ni audit falsifiés.
A10i83 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i83

- **WHEN** un profil revendique le traitement A10i83 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--4edbf82cf8

Source : `openspec/specs/pzt/spec.md`, ligne 9885. SHA-256 du bloc : `1aeb282d38c6e841beca859b0db247f60f5106778024730debd6d709565d01e7`.

~~~~text
### Requirement: Contrat A10i84 — Rétention nominale des traces techniques à 24 heures — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i84 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i84

Traces/corrélation OpenSpec et politique A10i60 conservées. Durée A 24 h
validée comme défaut nominal configurable des nouveaux profils pour spans effectivement
stockés, distincte du taux d'échantillonnage et sans politique existante remplacée.

| Choix validé | Rétention nominale des traces techniques | Conséquence |
| --- | --- | --- |
| A | 24 heures | Historique détaillé court, couverture/volumes à qualifier |

A = 86 400 s ; B 7 jours non retenue. Âge depuis première persistance durable du span
au backend autorisé, timestamps de début/fin distincts ; réexport, regroupement
ou restauration sans nouveau départ de rétention pour même span. Références de
trace/span et contexte/provenance qualifiés, pas de payload/secret ajoutés pour
enquête différée. Corrélation logs/métriques conservée sous rétentions distinctes :
lien pointant vers trace expirée indiqué indisponible, jamais trace reconstruite.
24 h ne garantissent pas trace complète ou reçue, span jamais échantillonné/
livré sans contenu inventé. Pas de durée liée à certificat TLS 24 h A10i4 ou
marqueur fermé A10i46 ; valeurs égales sans sémantique commune.
Expiration selon politique autorisée, horloge/provenance/holds/références et
audit vérifiés avant purge ; dérivés, exports, sauvegardes/reprises contrôlés
selon gouvernance. Durée nominale sans purge immédiate ou copie inaltérable
partout supposées. Quota sans troncature d'une preuve métier requise.
A validée comme premier jet court pour traces détaillées. Paramètre/configuration/volumes/besoins à qualifier,
aucun échantillonnage, exporter/backend ou obligation externe adoptés ici.
Audit métier/dossiers/reçus persistent sous leurs exigences propres, traces
sans substitut de preuve de temps ou d'audit. Pas de stockage durable de traces
imposé aux PA ordinaires par cette durée, aucune purge/runtime/OpenSpec exécutés.
Recette : span réexporté, corrélation vers trace expirée, span absent, hold,
horloge incertaine, sauvegarde restaurée et preuve métier jamais remplacée.
A10i84 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i84

- **WHEN** un profil revendique le traitement A10i84 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

