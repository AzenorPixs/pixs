# Références normatives — Z24

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 11764 | [Contrat A10i123 — Suivi événementiel du statut de réarmement avec réconciliation — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11764) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11814 | [Contrat A10i124 — Mutualisation du canal de suivi de statut — option A validée le 10 octobre 2026](../../specs/pzt/spec.md#L11814) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11864 | [Contrat A10i125 — Fenêtre nominale de rejeu des statuts de 1 heure — option A validée le 10 octobre 2026](../../specs/pzt/spec.md#L11864) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11910 | [Contrat A10i126 — Reprise du suivi par état autoritatif courant puis événements — option A validée le 10 octobre 2026](../../specs/pzt/spec.md#L11910) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--81c9885a1d

Source : `openspec/specs/pzt/spec.md`, ligne 11764. SHA-256 du bloc : `41e84fe72a54daca02e65642aa0eb60f8518260d35fa6f1f6165473b6be7f2f5`.

~~~~text
### Requirement: Contrat A10i123 — Suivi événementiel du statut de réarmement avec réconciliation — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i123 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i123

Commande idempotente/durable, contrôle de version A10i114 A et traitement 60 s
A10i113 B conservés. Suivi de résultat indépendant d'engagement/vérification ;
aucune nouvelle soumission de commande autorisée par événement ou polling.

| Choix validé | Suivi retenu | Conséquence |
| --- | --- | --- |
| A validée | Événements de statut versionnés via contrat autorisé, consultation autoritative de réconciliation si nécessaire | Moins de consultations périodiques possibles, canal/ordre/reprise à qualifier |

A : événements issus de faits durables publiés après validation selon Events,
commande/opération/incident/version et périmètre liés. Périmètre d'ordre et
déduplication déclarés, doublon/ancien événement/trou de séquence sans état
fictif ; réconciliation depuis Django/source courante si livraison ou dernier
état incertains. Choix SSE/WebSocket A07c2 conservés ; mutualisation du canal
A10i124, fenêtre de rejeu A10i125 et reprise A10i126 A validées le 10 octobre 2026.
Le polling périodique, option B, n'est pas retenu ; les consultations de
réconciliation restent distinctes et autorisées, sans prolonger la commande.
Commun : accès/périmètre/acteur courants contrôlés selon authorization, audit
individuel requis pour compte ordinaire ; exception Super Admin non déléguée et
tenant explicitement accordé, audit dérogé sans événement réalisé prétendu.
Statuts commande, effet confirmé/inconnu, dossier/audit disponibles et contrôles
réellement exécutés distingués ; délai/silence/absence de message sans succès
ou non-exécution déduits. Échec du suivi sans seconde levée, consultation et
commande mutante distinctes, capacité unique sans file A10i115 conservée.
UI cachée/déconnexion/contrôle indisponible : état inconnu ou dernier état daté
explicite, reprise autorisée bornée à qualifier ; aucune réémission automatique
de réarmement pour faire apparaître statut final. Aucun secret/payload exposés.
Suivi par faits de statut retenu ; coûts/canal/résilience à mesurer.
Profil, sécurité/corrélation et limites d'événements/requêtes à qualifier
avant activation, aucune livraison garantie.
Aucun abonnement, notification externe, requête/commande, runtime ou OpenSpec modifiés.
Recette : événement perdu/dupliqué/ancien, réconciliation indisponible, ACK perdu,
compte non accordé, dérogation d'audit et aucun résultat ou contrôle inventés.
A10i123 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i123

- **WHEN** un profil revendique le traitement A10i123 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--98368734a1

Source : `openspec/specs/pzt/spec.md`, ligne 11814. SHA-256 du bloc : `386a7d6f5b2261fce3fb72776cefcd30063a37f3f22ed8891be8be1107dbc667`.

~~~~text
### Requirement: Contrat A10i124 — Mutualisation du canal de suivi de statut — option A validée le 10 octobre 2026

Le rôle chargé du traitement A10i124 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i124

Suivi événementiel A10i123 A conservé ; canal, rétention A10i125 et reprise
A10i126 sont trois décisions indépendantes. Double support SSE/WebSocket,
table déterministe et canal unique en régime établi A07c2 restent acquis.
Le choix porte sur l'intégration du suivi, sans changer le transport de référence.

| Choix validé | Intégration retenue | Conséquence |
| --- | --- | --- |
| A validée | Réutiliser le canal de notification autorisé entre les mêmes extrémités, avec abonnement logique distinct | Évite une connexion supplémentaire ; isolation et partage de capacité à qualifier |

A : canal existant admis pour les mêmes extrémités et périmètre, contrat de
statut versionné et autorisation de chaque abonnement/donnée ; présence d'un
canal sans droit implicite. Aucun canal disponible => ouverture selon profil
déjà autorisé A07, sans imposer deux connexions permanentes ni autre permission.
Le canal dédié de suivi, option B, n'est pas retenu.
Commun : événements de faits engagés, jamais commandes de réarmement.
Commandes/lectures restent HTTP. Bascule SSE/WebSocket selon A07c2, droits,
versions et déduplication conservés ; aucun gain CPU/RAM universel promis.
Le flux interface–PBO reste distinct de PBO–PA : aucune réutilisation de
connexion entre extrémités différentes ; tout échange PBO–PA sous PZT/mTLS,
même hôte inclus. Pas d'abonnement permanent supplémentaire sur PA ordinaire.
Références de transport : [WHATWG SSE](https://html.spec.whatwg.org/multipage/server-sent-events.html)
et [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html).
Authentification de flux compatible avec le client à qualifier : EventSource
natif sans option d'en-tête Authorization arbitraire, aucun secret dans URL.
Origine, proxies, révocation en cours, lenteur, équité et bornes de messages/
buffers/abonnements/reconnexions à qualifier ; pas de boucle infinie native.
Audit et contrôles ordinaires applicables ; exception Super Admin selon
OpenSpec, non déléguée et tenants explicitement accordés, aucun fait inventé.
Mutualisation retenue pour limiter les connexions ; partage de capacité à qualifier.
Recette : canal absent, abonnement non autorisé, saturation d'un autre flux,
bascule, session expirée et fermeture sans commande réémise.
Aucun canal, abonnement, permission, dépendance ou OpenSpec modifiés ici.
A10i124 A validé le 10 octobre 2026.

#### Scenario: Conformité du traitement A10i124

- **WHEN** un profil revendique le traitement A10i124 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--43d1ec56b6

Source : `openspec/specs/pzt/spec.md`, ligne 11864. SHA-256 du bloc : `f125975fa14dd29018d2440337b2aa647130f0068937f1e6c61749c2f5637e3d`.

~~~~text
### Requirement: Contrat A10i125 — Fenêtre nominale de rejeu des statuts de 1 heure — option A validée le 10 octobre 2026

Le rôle chargé du traitement A10i125 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i125

Conservation du flux A10i123 A indépendante du canal A10i124 et de la stratégie
A10i126. Projection de livraison distincte de l'état autoritatif, de l'audit,
du dossier A10i120 et de l'historique de commande ; leurs rétentions subsistent.

| Choix validé | Fenêtre nominale retenue en régime ordinaire | Conséquence |
| --- | --- | --- |
| A validée | Événements de suivi disponibles au rejeu pendant 1 heure | Fenêtre courte ; volume dépendant du débit, moins d'historique de livraison |

Fenêtre depuis première persistance durable de l'événement ; réémission,
reconnexion ou restauration sans remise à zéro de son âge. Politique de
gouvernance versionnée, classification, consommateurs et résidence déclarés.
Plafonds distincts en octets/nombre d'événements et coût de stockage à qualifier :
une durée seule ne borne pas la mémoire. Sous saturation, aucune garantie
fictive de disponibilité complète ; plage réellement disponible et lacunes
explicites, consultation autoritative si reprise impossible.
Backend de livraison autorisé, aucune copie persistante supplémentaire imposée
à chaque PA ; contenu minimal de statut, sans dossier brut, secret ni audit dupliqué.
En régime ordinaire, expiration ne vaut ni autorisation de purge physique ni
suppression de référence encore requise : procédure applicable, holds et
anti-résurrection conservés. Projection indisponible sans preuve de commande
absente, d'effet annulé ou de contrôle effectué. Aucun historique reconstitué.
Dérogations Super Admin limitées au compte/périmètre reconnus selon OpenSpec,
sans transfert à worker, tenant implicite ou preuve d'audit inventée.
Fenêtre nominale de 1 heure retenue ; option B de 24 heures non retenue.
Pas de purge, Job,
stockage, rétention d'audit ou configuration réelle modifiés.
Recette : frontière d'âge, restauration d'un ancien événement, saturation,
hold, curseur expiré et consultation courante sans historique inventé.
A10i125 A validé le 10 octobre 2026.

#### Scenario: Conformité du traitement A10i125

- **WHEN** un profil revendique le traitement A10i125 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--344e8e53f6

Source : `openspec/specs/pzt/spec.md`, ligne 11910. SHA-256 du bloc : `c3547b7bcf62fa133b115aa457fd5920e4731465f33597d84720d3d1af62c404`.

~~~~text
### Requirement: Contrat A10i126 — Reprise du suivi par état autoritatif courant puis événements — option A validée le 10 octobre 2026

Le rôle chargé du traitement A10i126 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i126

Reprise de statut A10i123 A, distincte du canal A10i124 et de la fenêtre
A10i125 ; aucune reprise ne soumet à nouveau la commande de réarmement.

| Choix validé | Reprise retenue | Conséquence |
| --- | --- | --- |
| A validée | Relire un état autoritatif courant puis reprendre les événements à une borne cohérente | Lecture supplémentaire, convergence sur l'état courant sans exiger tout l'historique |

A : instantané courant Django lié à version/borne de flux cohérente, raccord
sans perte entre lecture et abonnement ; événements intervenus pendant cette
lecture rattrapés ou nouvelle réconciliation, jamais sautés silencieusement.
Pas d'atomicité inter-providers présumée ; mécanisme de raccord à qualifier.
La reprise prioritaire depuis un curseur, option B, n'est pas retenue.
La fenêtre A10i125 ne garantit ni curseur toujours disponible ni rejeu complet.
Commun : faits après commit, livraison au-moins-une-fois et ordre par agrégat
déclaré selon Events, déduplication/version empêchant régression d'état.
Accès actuels et audit ordinaires réévalués à la reprise et pendant diffusion ;
exception Super Admin OpenSpec non transférable, périmètre explicitement accordé,
contrôles/audits non réalisés jamais présentés comme effectués.
État indisponible affiché inconnu ou dernier connu daté ; aucune conclusion
d'effet à partir du silence ou de la seule fin du flux. Borne de reprise,
nombre/délai de réessais, volume de rattrapage et abonnements à qualifier,
sans boucle infinie, file cachée ou nouveau budget de commande A10i113 B.
État courant du PBO prioritaire à la reprise ; historique de livraison
distinct de l'audit. Coûts CPU/RAM/lectures à mesurer.
Recette : mutation entre instantané et abonnement, doublon, trou de séquence,
curseur expiré, révocation, source indisponible et absence de double réarmement.
A10i126 A validé le 10 octobre 2026.

#### Scenario: Conformité du traitement A10i126

- **WHEN** un profil revendique le traitement A10i126 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

