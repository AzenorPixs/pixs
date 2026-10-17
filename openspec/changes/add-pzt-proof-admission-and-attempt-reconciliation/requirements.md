# Références normatives — Z16

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 7414 | [Contrat A10i41 — Non-admission explicite lorsque le validateur est occupé — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7414) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7469 | [Contrat A10i42 — Relances automatiques bornées après non-admission pour capacité — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7469) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7541 | [Contrat A10i43 — Réconciliation automatique bornée après réponse perdue ou état incertain — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7541) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7616 | [Contrat A10i44 — Fermeture durable d’une tentative coordonnée avec l’admission — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7616) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7689 | [Contrat A10i45 — Conservation individuelle des marqueurs sans compaction automatique — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7689) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7751 | [Contrat A10i46 — Retrait des marqueurs après minimum 24 heures et preuve d’irrecevabilité — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7751) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7819 | [Contrat A10i47 — Identité structurée opération, cycle et numéro de tentative — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7819) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7891 | [Contrat A10i48 — Échéance d’admission fixée à la création active du cycle — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7891) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--06edb9782b

Source : `openspec/specs/pzt/spec.md`, ligne 7414. SHA-256 du bloc : `4315d280b7c504e201bd334e253a4a2b5d2d2ee6c226c2f01ad2891ec04268f8`.

~~~~text
### Requirement: Contrat A10i41 — Non-admission explicite lorsque le validateur est occupé — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i41 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i41

Un dossier actif par instance et budgets A10i40 A conservés. Non-admission
explicite sans file retenue quand ce créneau est occupé, sans augmenter concurrence,
plafonds A10i39 ou habilitations. Demande authentifiée/typée/autorisation courante
avant admission, réponse sans informations sur les dossiers d'autres périmètres.

| Choix validé | Si le créneau est occupé | Conséquence |
| --- | --- | --- |
| A | Non-admission explicite pour capacité indisponible, sans file interne de dossiers | Nouvelle tentative seulement autorisée, aucun travail différé implicitement accepté |

Réponse de capacité indisponible distincte d'échec de preuve ou de sécurité,
sans dossier réputé validé ni réservé pour exécution ultérieure. Admission/
acquisition du créneau contrôlées face à concurrence ; créneau occupé ou état
d'exécution incertain sans second traitement admis. Aucun tampon interne
accumulant des dossiers en attente. Contrôles de débit et concurrence des requêtes
d'admission eux-mêmes à qualifier, absence de file de dossiers sans coût nul.
File interne bornée non retenue. Relances bornées validées A10i42 A ;
représentation/codes de réponse et éventuel délai indicatif à définir par contrat,
sans ETA garantie, renvoi automatique vers instance non qualifiée ou retry infini.

Doublon d'opération déjà connu retrouve son état admissible via A07/A12
sans réservation supplémentaire, même si le créneau est occupé ; changement
de contexte/dossier/version sous même identifiant sans nouvel effet autorisé.
Résultat incertain réconcilié avant nouvelle tentative, limite de concurrence
maintenue ; réponse perdue sans demande automatiquement supposée non admise.
Aucune répétition d'assainissement, signature CA ou destruction sur simple
nouvelle soumission. Validation autorisée distincte du titre d'administrateur,
A05/A10i22 B et autorité Django/A12 maintenus. Codes, admission/exclusivité,
relances A10i42 A validées et budgets inter-tentatives à qualifier,
aucune configuration/runtime ou évolution OpenSpec écrits ici.
A validée pour simplicité et état à conserver limité, sans disponibilité/
débit/latence garantis. Mesures CPU/RAM/I/O/stockage sur Linux/Windows physiques/VM,
Docker/LXC Proxmox et rôles de contrôle, aucun validateur de dossier imposé aux
PA ordinaires. Recette : admissions concurrentes, instance occupée, doublon déjà
traité/en cours, contexte incompatible, réponse perdue, état incertain,
reprise/restauration, révocation avant admission et absence de
preuve, droit ou action destructrice réactivés.
Politique validée par Pixs, sans norme externe la prescrivant.
A10i41 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i41

- **WHEN** un profil revendique le traitement A10i41 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--074960173f

Source : `openspec/specs/pzt/spec.md`, ligne 7469. SHA-256 du bloc : `b5d145ce54e23c2d91328bca55edff36b9ee9d64ff4b3223d58a0754816e2a17`.

~~~~text
### Requirement: Contrat A10i42 — Relances automatiques bornées après non-admission pour capacité — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i42 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i42

Non-admission explicite sans file A10i41 A et budgets A10i40 A conservés.
Relance de demande de validation, sans répétition de récupération, assainissement
ou signature CA. Autorisation courante et identité stable d'opération A07/A12
maintenues ; premier jet de relances automatiques validé, valeurs à qualifier,
aucune tâche programmée ici.

| Choix validé | Après non-admission explicite pour capacité indisponible | Limites |
| --- | --- | --- |
| A | Relances automatiques sous politique/mandat préalablement autorisés | 3 soumissions au total, attentes de 5 puis 10 secondes, fenêtre d'admission de 30 secondes |

Seulement après réponse typée/authentifiée attestant non-admission pour
capacité, opération non commencée et non déjà engagée. Refus de sécurité,
preuve/dossier invalide, expiration, révocation, réponse absente ou résultat
incertain sans relance de validation automatique. Opération déjà en cours ou
clôturée retrouvée via contrat A07/A12, sans nouvelle réservation.
Trois soumissions au maximum = initiale et deux nouvelles, compteurs partagés
entre reprises de la même tentative d'admission. Délais depuis chaque
non-admission prouvée : 5 secondes avant deuxième, 10 avant troisième ;
aucune attente qui dépasse la fenêtre restante ou les validités courantes.
Fenêtre de 30 secondes dès première soumission, temps réseau et temporisations
inclus ; expiration ou troisième non-admission arrêtent le cycle sans grâce.
Budget d'admission distinct des 180 secondes de traitement A10i40, qui ne
commencent que si le créneau de validation est acquis. Admission prouvée
arrête les relances, sans resoumission concurrente pendant traitement.

Automatisation sur demandeur habilité, références/compteurs/échéance conservés
sans secret, reprise avec preuve d'état/temps restant sinon suspension/refus.
Même identifiant d'opération, contexte/dossier/version attendus ; identifiants
de tentatives et schéma à préciser, changement de payload sans opération
distincte autorisée. Aucun compteur neuf ou fenêtre prolongée par redémarrage,
snapshot, nouveau canal ou identité de membre différente. Valeurs/politique
explicites approuvées via PBO/Django/A07/A12, non modifiées depuis réponse
reçue/charge ; nouveau cycle après échec définitif seulement explicitement
autorisé, pas d'enchaînement automatique de cycles finis sans limite.

Contrôle courant du mandat, des retraits/état/contexte avant chaque
soumission ; incapacité ou résultat inconnu de ces contrôles bloque la suite.
Réponse perdue : consultation bornée/réconciliation avant décision, aucune
non-admission déduite d'un timeout ; réconciliation automatique validée A10i43 A,
protocole à qualifier avant activation. Nouvelle validation sans opérations destructrices
répétées, ancienne permission/racine/droit réactivés ou contraintes A10i39 élargies.
Codes d'erreur, temporisations, stockage d'état, transport et idempotence à
qualifier ; aucun ordonnanceur, paramètre runtime ou OpenSpec modifié ici.

A validée pour reprendre quelques indisponibilités brèves sans intervention
répétée, sous bornes et contrôle courant ; mode exclusivement manuel non retenu.
Valeurs Pixs sans mesures de charge justifiant les seuils ni délai de succès
garanti ; ressources et charge de relance à mesurer, pas de gain universel.
Linux/Windows physiques/VM, Docker/LXC Proxmox et rôles de contrôle qualifiés,
aucune boucle de relance ou validation courante imposée aux PA ordinaires.
Recette : trois capacités indisponibles, admission à deuxième tentative, expiration
durant attente, réponse perdue, reçu déjà engagé, changement de dossier/contexte,
restauration du compteur, tentative concurrente et aucune action/droit réactivés.
Politique validée par Pixs, aucune valeur prescrite par une norme externe.
A10i42 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i42

- **WHEN** un profil revendique le traitement A10i42 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--7fdaa510c8

Source : `openspec/specs/pzt/spec.md`, ligne 7541. SHA-256 du bloc : `e9089c8aa6280aca2434d525161ce4b6abbe7630eb8b1e5114557eaa8840e3a8`.

~~~~text
### Requirement: Contrat A10i43 — Réconciliation automatique bornée après réponse perdue ou état incertain — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i43 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i43

Relances de capacité A10i42 A, absence de file A10i41 A et idempotence A07/A12
conservées. Recherche d'état de la même opération/tentative, sans nouvelle
admission ni répétition de validation, assainissement ou signature CA.
Consultation automatique sous mandat retenue ; valeurs de premier jet validées
à qualifier, aucun outil de consultation exécuté ici.

| Choix validé | Réconciliation | Bornes |
| --- | --- | --- |
| A | Consultation automatique de l'autorité Django/A12 sous mandat admissible | 3 requêtes au total, attentes de 2 puis 5 secondes, budget global de 15 secondes |

Interrogation d'état par contrat public A07, sans accès direct aux tables
PostgreSQL. Trois requêtes = initiale et deux nouvelles si état encore inconnu ;
délais après résultat inconnu/absence de réponse de 2 puis 5 secondes, sans
dépasser budget restant. Budget de 15 secondes depuis détection d'incertitude
ouvrant cette réconciliation, temps réseau inclus ; requêtes elles-mêmes bornées.
Même opération, tentative(s) concernée(s), contexte/dossier/version attendus,
demandeur et autorité/époque admissibles contrôlés ; réponse fraîche liée à la
demande/canal, aucun ancien reçu ou événement de cache pris pour état courant.
Contrôles de sécurité invérifiables/refusés arrêtent la consultation automatique.
Consultation authentifiée d'une opération hors périmètre sans statut révélé.

Opération retrouvée en cours : suivre son état connu selon A07, aucune nouvelle
soumission ; opération clôturée : restituer reçu/constat admissibles A12 sans
nouvelle exécution. Budget de réconciliation vise admission/engagement, pas
attente de fin du traitement de 180 secondes A10i40. Notification/delta/cache
sans preuve autoritative actuelle insuffisants pour lever incertitude.
Réponse « introuvable », réplica retardataire ou absence d'accusé sans preuve
que toutes tentatives ont été exclues de tout engagement futur insuffisantes
pour conclure non-admission. Non-admission terminale seulement sur état
autoritatif lié aux tentatives et clôture/exclusion de toute soumission encore
capable d'être admise/engagée ; fermeture durable validée A10i44 A, protocole à qualifier.
Si confirmée, relance A10i42 possible seulement si tous compteurs/échéances/
mandats sont encore admissibles, aucun nouveau cycle automatiquement créé.

Inconnu après troisième requête ou délai : état incertain conservé, suspension/
diagnostic et intervention autorisée pour poursuivre ; aucune nouvelle identité
d'opération, permission ou exécution créée pour contourner l'incertitude.
Compteurs/échéance persistés sans secret, reprise sans remise à zéro par crash,
snapshot, changement de canal/instance. Nouveau cycle seulement explicitement
autorisé. Requête d'état distincte des soumissions A10i42, sans remise à zéro ni
prolongation de leur fenêtre de 30 secondes ; consultation peut réconcilier un
engagement existant après cette fenêtre, mais jamais rouvrir l'admission expirée.

Django/A12 reste autorité, contexte/mandat/révocations A05 prioritaires,
état/commit incertains sans signature les transformant en preuve universelle.
Reçu restitué selon A12d/A12e B et confiance A12c ; véracité/commit sans garantie
au-delà des limites A12c. Schémas d'état, preuve de non-admission terminale,
codes/époques, fraîcheur et durabilité/temps à qualifier avant activation ;
aucun runtime, accès SQL, OpenSpec ou opération destructrice modifiés ici.
A validée pour lever quelques pertes de réponse sans intervention répétée,
sous bornes ; mode exclusivement humain non retenu. CPU/RAM/réseau à mesurer sur
Linux/Windows physiques/VM, Docker/LXC Proxmox et contrôle, aucune consultation
de clôture courante imposée aux PA ordinaires ni réussite/latence garanties.
Recette : réponse perdue mais opération engagée, statut en cours/clôturé,
introuvable avec soumission encore possible, réplica ancien, reçu rejoué,
horloge/reprise inconnues, retrait courant, plafond atteint et aucune action/
permission réactivées. Politique et valeurs Pixs validées sans norme les prescrivant.
A10i43 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i43

- **WHEN** un profil revendique le traitement A10i43 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--1fa56c9494

Source : `openspec/specs/pzt/spec.md`, ligne 7616. SHA-256 du bloc : `98a44728c754d5d109e1a72e1c2622cb831316019c4899ba88098218a4bff495`.

~~~~text
### Requirement: Contrat A10i44 — Fermeture durable d’une tentative coordonnée avec l’admission — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i44 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i44

Réconciliation A10i43 A, relances A10i42 A et absence de file A10i41 A maintenues.
Marqueur durable de fermeture retenu pour empêcher admission tardive après
non-admission, sans annulation d'une opération déjà admise ou engagée.
Même opération métier et tentatives liées, autorité Django/A12 et A05 conservés.

| Choix validé | Mécanisme | Condition de non-admission définitive |
| --- | --- | --- |
| A | Marqueur durable de fermeture par tentative, coordonné transactionnellement avec l'admission | Fermeture engagée avant admission, chaque chemin tardif contrôlant le même état autoritatif |

Commande de fermeture autorisée A07 distincte de consultation A10i43,
idempotente et bornée sous mandat propre ou clause préalable explicitement
habilitée. Enregistrement sans secret lié au périmètre/opération/tentative,
dossier/version et autorité/époque. Admission et fermeture concurrencent le
même état durable dans PostgreSQL A12a/A12b ; unicité d'opération et contrôle
des tentatives qualifiés, aucun test préalable d'absence suivi d'écriture non
coordonnée. Même si aucune tentative n'était enregistrée, fermeture crée
une barrière durable empêchant sa création/admission tardive ; absence de
ligne seule sans verrouillage/contrainte d'unicité appropriés insuffisante.
Schéma/transactions/contraintes/isolation et durabilité à qualifier avant activation.

Si admission gagne, conserver/restituer son état et reçu admissibles, sans
non-admission déclarée ni opération déjà engagée supprimée. Si fermeture gagne,
contrôle d'admission de cette tentative la refuse, même depuis ancien message,
nouveau canal, membre ou redémarrage. Validation ne commence pas sur seul état
local avant engagement admissible d'admission, tous chemins d'exécution inclus.
État/commit incertain : réconcilier, pas de signature de non-admission présumée.
Marqueur terminal pour la tentative visée ; autre tentative de la même opération
seulement sous A10i42 et garde empêchant plusieurs traitements de l'opération.
Couverture de toutes tentatives encore susceptibles d'être admises requise
avant levée d'incertitude ; identité/numérotation et périmètre de fermeture à
spécifier, aucune tentative inconnue réputée couverte par un seul marqueur.

Réponse de non-admission actuelle liée aux tentatives, contexte,
mandat/époque et engagement admissible ; reçu/contrôles A12 sans preuve universelle
de commit ou véracité au-delà d'A12c. Marqueur ne supprime pas une clôture,
un constat ou preuve d'assainissement et ne déclenche aucune destruction.
Restauration/promotion PG selon A12b, état ancien exclu ; conservation individuelle
validée A10i45 A, sans compaction, retrait sous preuve validé A10i46 A ; disparition d'état
sans ancienne tentative réadmise. PA sans accès SQL direct, références/preuves
sans clés/secrets, contrôle individuel A10i22 B conservé. Aucun SQL, migration,
configuration ou évolution OpenSpec effectués ici.

A validée pour utiliser le contrôle transactionnel A12 déjà retenu sans
ticket préalable par soumission, cette architecture alternative non retenue.
Coûts de stockage/transactions/réseau à mesurer sur rôles
de contrôle, Linux/Windows physiques/VM et Docker/LXC Proxmox qualifiés ; aucune
disponibilité/latence ou ressource universellement meilleure, aucun nouvel accès
ou traitement courant imposé aux PA ordinaires.
[PostgreSQL 16, verrouillage](https://www.postgresql.org/docs/16/explicit-locking.html)
et [isolation](https://www.postgresql.org/docs/16/transaction-iso.html) décrivent
les mécanismes de concurrence ; protocole Pixs validé, aucun schéma ou SQL
spécifique qualifié par cette seule référence. Recette : admission/fermeture
simultanées et tous ordres, tentative absente puis tardive, admission déjà engagée,
commit incertain, ancien marqueur restauré, plusieurs tentatives,
compaction trop précoce et absence de nouvelle opération/droit réactivés.
A10i44 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i44

- **WHEN** un profil revendique le traitement A10i44 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--2f9bdc1c11

Source : `openspec/specs/pzt/spec.md`, ligne 7689. SHA-256 du bloc : `4665204ddb616e781b487e60c1bf8cba4f83fcaa949206e109691429e4d97970`.

~~~~text
### Requirement: Contrat A10i45 — Conservation individuelle des marqueurs sans compaction automatique — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i45 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i45

Fermeture durable transactionnelle A10i44 A, réconciliation A10i43 A et relances
A10i42 A conservées. Politique de conservation de l'interdiction de réadmission,
distincte de rétention du dossier/audit et d'assainissement des anciens secrets.
Aucun délai de suppression numérique ou obligation légale de rétention adopté.

| Choix validé | Conservation | Condition de retrait des marqueurs |
| --- | --- | --- |
| A | Marqueurs individuels durables conservés sans compaction automatique | Preuve que les anciennes tentatives sont définitivement irrecevables et règles d'audit satisfaites |

Identité de fermeture, périmètre/opération/tentative, dossier/version et
autorité/époque nécessaires au contrôle conservés dans l'état autoritatif A12.
Expiration des 15 secondes de réconciliation, des 30 secondes d'admission ou
arrêt du validateur sans marqueur supprimé automatiquement. Même une nouvelle
autorisation ne réutilise pas implicitement une tentative terminalement fermée.
Suppression seulement sous procédure/mandat admissibles après preuve de fin
de possibilité d'admission/rejeu sur tous chemins concernés, compatibilités et
règles de rétention/audit vérifiées. Absence de preuve : conservation ou traitement
suspendu pour manque de capacité, sans purge affaiblissant les contrôles.
Minimum 24 heures/retrait sous preuve validés A10i46 A, à qualifier sans
conservation éternelle ou volumétrie négligeable présumées.

Stockage/promotion/restauration A12b préserve interdictions courantes,
aucun snapshot ancien ou historique absent ne rend une tentative recevable.
Identifiants/époques, fin de validité des mandats, accès de vérification et
non-réutilisation à spécifier ; horloge/état courant inconnu refuse réadmission.
Rétention arrivée à terme sans autorisation/preuve de retrait sans suppression
automatique ; preuve d'irrecevabilité distincte d'un simple âge ou TTL.
Quotas/alertes et réaction au manque de stockage à qualifier avant activation,
aucune suppression silencieuse pour maintenir disponibilité. Métadonnées
minimales sans clés, jetons, dossiers bruts ou données personnelles non nécessaires,
accès contrôlés ; conservation n'accorde aucune permission ou clôture nouvelle.
Django/A07/A12 et contrôle individuel A10i22 B gouvernent les mutations ;
A05 prioritaire, PA sans accès SQL direct. Aucun SQL, archivage réel, fichier
d'audit, tâche planifiée ou évolution OpenSpec créés/modifiés ici.

A validée pour simplicité et conservation directe de l'état de chaque
tentative ; compaction vers barrière équivalente non retenue.
Volumes/durées/CPU/I/O à mesurer selon opérations,
sans coût nul ou gain universel ; toutes cibles Linux/Windows physiques/VM et
Docker/LXC Proxmox qualifiées, pas de marqueurs de clôture imposés aux PA ordinaires.
Recette : ancien message après délai local, autorisation nouvelle avec ancien
identifiant, snapshot antérieur, lecteur incompatible, retrait/commit
interrompus, audit absent, quota atteint et refus conservé.
Politique validée par Pixs, ni obligation de rétention externe ni conformité déclarées.
A10i45 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i45

- **WHEN** un profil revendique le traitement A10i45 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--f08bd58cc9

Source : `openspec/specs/pzt/spec.md`, ligne 7751. SHA-256 du bloc : `9f328ffcf09f5606afeb5dad3b574ab123074b5ad7504b350fb4e23d2a3d9001`.

~~~~text
### Requirement: Contrat A10i46 — Retrait des marqueurs après minimum 24 heures et preuve d’irrecevabilité — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i46 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i46

Conservation individuelle sans compaction automatique A10i45 A et fermeture
A10i44 A maintenues. Politique de retrait physique de métadonnées opérationnelles,
sans assainissement de clés ni suppression du dossier/preuves A10i35.
Minimum 24 heures et retrait sous preuve validés, valeurs à qualifier ;
aucun effacement, archivage réel ou mandat exécuté ici.

| Choix validé | Retrait individuel | Conditions cumulatives |
| --- | --- | --- |
| A | Minimum configurable de 24 heures après fermeture, puis retrait autorisé sous preuve | Ancienne tentative définitivement irrecevable sur tous chemins, contrôles courants et audit/rétention satisfaits |

Minimum de 24 heures = 86 400 secondes depuis engagement durable de la
fermeture, pas depuis première soumission, expiration locale ou reçu tardif.
Délai de premier jet configurable/versionné sous politique approuvée, à qualifier,
sans délai maximal autorisant une purge forcée. Temps courant vérifiable et
dates engagées conservés ; nouveau canal, reprise ou snapshot sans crédit
d'ancienneté artificiel. Délai écoulé seul sans preuve d'irrecevabilité insuffisant.

Avant retrait, mandats/cycles/époques pouvant admettre l'ancienne tentative
définitivement clos/expirés ou exclus ; règles d'admission empêchent réémission/
réutilisation de cette identité dans un mandat/cycle nouveau. Tous membres,
chemins d'admission et versions encore autorisés appliquent ces règles, y
compris après restauration/promotion A12b ; horloge, état ou couverture inconnus
interdisent le retrait. Identité structurée/liaison au cycle validées A10i47 A, preuve de fin
de validité et admission à qualifier ; aucun registre ou barrière
compacte ajouté implicitement pour satisfaire cette preuve. Si l'architecture
ne peut démontrer l'irrecevabilité après suppression, conserver le marqueur.
Ancienne requête tardive refusée par conditions courantes même après retrait,
absence de ligne jamais interprétée comme autorisation.

Opérations encore actives, engagements incertains, dépendances de réconciliation
et obligations de conservation interne/audit traités avant retrait ; preuves/
reçus/dossier nécessaires conservés dans leur périmètre autorisé. Procédure
autorisée ciblant références/générations précises, contrôles revalidés à l'engagement,
mutations idempotentes/durables selon Django/A07/A12. État changé avant mutation
ou résultat incertain : arrêt/réconciliation, retrait sans succès présumé.
Quotas ou manque de stockage sans accélération du délai ou preuve supprimée.

Minimum atteint sans permission de rouvrir une tentative,
clôture ou droit PZT ; A05/A10i22 B prioritaires et PA sans accès SQL direct.
Politique de conservation des métadonnées distincte des règles du dossier/
audit et sans durée légale ou certification adoptées ici. Paramètres, critères,
format des preuves, rétention d'audit et procédure de retrait à qualifier avant
activation, aucune tâche de purge programmée ou évolution OpenSpec créée.
A validée pour permettre retrait encadré avec preuve technique obligatoire ;
conservation systématique jusqu’à fin de vie du périmètre non retenue.
Ressources/durées/volumes à mesurer sur contrôle et toutes cibles Linux/Windows
physiques/VM, Docker/LXC Proxmox, sans collecte ou purge courante imposées aux
PA ordinaires. Recette : délai exact et moins une seconde, mandat encore valable,
nouvelle autorisation pour ancienne tentative, lecteur/restauration anciens,
audit manquant, quota atteint, changement avant commit et refus toujours conservé.
A10i46 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i46

- **WHEN** un profil revendique le traitement A10i46 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--d85bddd3ea

Source : `openspec/specs/pzt/spec.md`, ligne 7819. SHA-256 du bloc : `f948adfb1d7b8dfed1969977ddfb0072ba93405d997ca8920bbd756601d91eaf`.

~~~~text
### Requirement: Contrat A10i47 — Identité structurée opération, cycle et numéro de tentative — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i47 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i47

Relances A10i42 A, réconciliation A10i43 A, fermeture A10i44 A et retrait sous
preuve A10i46 A conservés. Identité structurée de tentative retenue,
sans identité PA, clé cryptographique ou ticket d'admission supplémentaire.
Cycle = ensemble borné de soumissions sous la même autorisation de relance,
distinct d'époque d'autorité et de génération de clé/racine.

| Choix validé | Identité de tentative | Liaison à l'autorisation |
| --- | --- | --- |
| A | Tuple structuré opération + cycle + numéro de tentative de 1 à 3 | Cycle créé/habilité par l'autorité, contexte/dossier/version et bornes immuables contrôlés |

Champs typés/versionnés distincts, périmètre de l'opération et autorité
liés au contexte ; aucune concaténation textuelle ambiguë servant d'identité.
Identifiant de cycle attribué sous politique/mandat admissibles via Django/A07/A12,
jamais créé à la volée par un message pour remettre compteurs/échéances à zéro.
Numéro 1 = soumission initiale, 2 et 3 = nouvelles soumissions A10i42 ; doublon
avec même tuple et contenu attendu retrouve état existant sans nouvel effet.
Rang hors limites, même tuple avec dossier/contexte/version différents ou cycle
non admissible refusés. Réservation des rangs/compteurs et admission coordonnés
dans A12, soumissions concurrentes sans quatrième tentative ou second traitement.

Cycle lie demandeur habilité, opération, périmètre, dossier/version, politique,
mandat et échéance finie d'admission. Compatibilité avec fenêtre A10i42 de
30 secondes depuis première soumission, fixation à création validée A10i48 A, preuve à qualifier ;
échéance contrôlée par autorité avant admission, pas seulement par timer client.
Cycle clos/expiré/retiré, état ou temps invérifiables : aucune nouvelle admission
sur ses tentatives même si marqueur retiré sous A10i46. Reprise/restauration et
nouveau canal/membre sans cycle ni identité remis à zéro. Après échec définitif,
nouveau cycle uniquement sous autorisation explicite, identifiant distinct,
sans réaffectation d'un tuple ancien ni réouverture d'une opération déjà engagée.
Contrôle de cycle/mandat préexistant aux fermetures, pas de barrière compacte
créée pour remplacer les marqueurs A10i45 ou permission par identifiant seul.

Identité figée avant soumission, fermeture et réconciliation référencent
exactement opération/cycle/tentative(s) concernées, couverture des tentatives
incertaines sans simple compteur local présumé exhaustif. État autoritatif absent
sans permission d'admettre ; contrat de statut ne transforme pas « introuvable »
en non-admission prouvée. Audit minimal et références sans secret, reçu A12 selon
type/usage, aucune signature ou clé racine/backup/WireGuard ajoutées.
Modèle/schéma exacts et preuve d'irrecevabilité après retrait des marqueurs à
qualifier ; A10i46 sans suppression possible si preuve insuffisante. Ce choix
ne fixe pas la rétention de l'état d'opération/cycle ni de l'audit, aucune
compaction implicite ou purge du seul fait d'un cycle expiré.
A05, contrôle individuel A10i22 B et PA sans SQL direct maintenus ; aucun champ
runtime, SQL, migration ou évolution OpenSpec implémentés ici.

A validée pour exprimer directement le cycle et le rang borné à trois
soumissions ; identifiant opaque individuel alternatif non retenu. Coûts
stockage/contrôles à mesurer sans gain universel, toutes cibles physiques/VM
Linux/Windows et Docker/LXC Proxmox qualifiées, aucune génération de tentative
de clôture courante imposée aux PA ordinaires. Recette : rang 0/4, doublon valide,
même tuple contenu changé, nouveau cycle non habilité, tentative fermée sous
nouvelle autorisation, cycle expiré après retrait de marqueur, association
de cycle absente/ambiguë, restauration ancienne et aucune action/droit réactivés.
Politique Pixs validée, sans format d'UUID ou norme de génération adopté.
A10i47 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i47

- **WHEN** un profil revendique le traitement A10i47 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--4a4a1a6433

Source : `openspec/specs/pzt/spec.md`, ligne 7891. SHA-256 du bloc : `9c1e08429c90d94b62d802096c5e974bce032654dfaf85793d0876619cc1effd`.

~~~~text
### Requirement: Contrat A10i48 — Échéance d’admission fixée à la création active du cycle — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i48 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i48

Identité structurée A10i47 A, trois soumissions/fenêtre 30 secondes A10i42 A,
réconciliation A10i43 A et fermeture A10i44 A conservées. Fixation autoritative
d'une échéance avant première soumission, sans durée de traitement A10i40 ou
conservation de marqueurs A10i46 modifiées. Fixation à création active retenue,
bornes d’incertitude A10i49 A et adaptateurs système A10i50 A validés, protocole à qualifier.

| Choix validé | Fixation de l'échéance | Usage du cycle |
| --- | --- | --- |
| A | À la création active du cycle par l'autorité : T0 + 30 secondes au maximum | Créer une fois les entrées prêtes, première soumission seulement après état admissible confirmé |

Création autorisée/idempotente Django/A07/A12 après préparation des entrées
nécessaires, même opération/dossier/version/mandat figés. T0 de création issu
de temps qualifié d'autorité, enregistré avant engagement avec échéance fixe,
borne de 30 secondes et validités de sécurité plus courtes prioritaires.
T0 antérieur ou égal à la première émission ; temps d'engagement et de restitution
peut réduire la fenêtre utile, sans nouvelle horloge démarrant à l'accusé client.
Échéance et état engagés durables A12 avant toute admission. Réception/réédition
de réponse, requête tardive ou première demande reçue plus tard sans recalcul
de T0/échéance. Création trop tard confirmée ou déjà expirée : aucune admission,
nouveau cycle seulement explicitement autorisé, pas de renouvellement implicite.

Plafond client A10i42 de 30 secondes depuis première soumission
conservé ; échéance d'autorité démarre avant cette soumission et peut être
plus restrictive, sans donner 30 secondes supplémentaires après réception.
Limite effective = toutes bornes de sécurité et de temps admissibles, aucune
grâce par latence, dérive d'horloge, panne ou nouvelle association. Échéance
atteinte, cycle retiré/clos ou temps invérifiable bloque toute nouvelle admission.
Opération déjà admise peut suivre son état sous contrôles A05/A12 et budget
de traitement A10i40, sans admission annulée par seule fin du cycle.
Temps client ne remplace pas celui de l'autorité ; cohérence des membres,
incertitude/dérive, UTC/mesure monotone, restauration et reprise à qualifier.
Horloge reculant ou ancien état restauré sans cycle valable prolongé artificiellement.

Résultat de création incertain : consultation du contrat d'état et
réconciliation A07/A12, aucune nouvelle identité ou soumission créée pour
contourner l'incertitude. Création sans admission d'une tentative ni
créneau réservé, absence de file A10i41 préservée ; chaque tentative recontrôlée.
Échéance/contexte/politique/mandat/époque liés au cycle et reçus admissibles,
sans clé privée/dossier sensible ou URL non fiable accordant une autorisation.
Admission/fermeture/restauration selon A12, PA sans SQL direct. Cycle expiré
sans permission de retirer automatiquement état/trace ou marqueur A10i45/A10i46.
Schéma, horodatages, commande(s), profil de temps et durabilité à qualifier ;
aucune migration, source de temps installée ou évolution OpenSpec réalisée ici.

A validée pour cycle actif en une commande ; préparation puis activation
distincte non retenues. Ressources/latence/temps utiles à mesurer, sans disponibilité ou fenêtre
utile garantie ; rôles de contrôle et Linux/Windows physiques/VM, Docker/LXC
Proxmox qualifiés sans cycle courant imposé aux PA ordinaires.
Recette : accusé tardif, création incertaine, doublon de création, soumission
avant création admissible ou après échéance, mandat plus court, temps inconnu/
reculant, restauration ancienne et aucune admission/droit réactivés.
Politique Pixs validée, aucun format/source de temps ou marge d'horloge adopté.
A10i48 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i48

- **WHEN** un profil revendique le traitement A10i48 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

