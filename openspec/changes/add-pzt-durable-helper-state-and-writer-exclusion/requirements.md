# Références normatives — Z19

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 8945 | [Contrat A10i66 — État de reprise technique local durable, protégé et possédé par le parent — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8945) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9007 | [Contrat A10i67 — État technique courant en document JSON UTF-8 typé/versionné — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L9007) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9058 | [Contrat A10i68 — Stockage de l'état technique et de sa publication plafonné à 256 Kio — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L9058) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9109 | [Contrat A10i69 — Métriques techniques à dimensions stables et finies — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L9109) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9162 | [Contrat A10i70 — Publication de l'état JSON par candidat synchronisé et remplacement atomique — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9162) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9214 | [Contrat A10i71 — Exclusion des écrivains par verrou OS sur objet stable distinct — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9214) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9267 | [Contrat A10i72 — Métriques de collecte plafonnées à 64 séries ordinaires et 1 débordement — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9267) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 9322 | [Contrat A10i73 — Reprise du parent au même démarrage OS sous continuité complète prouvée — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L9322) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--c65e6a1c6b

Source : `openspec/specs/pzt/spec.md`, ligne 8945. SHA-256 du bloc : `de6e29b17b58592e6236cdf349609396f1cbe1810332ca00f7a268e1608a8c75`.

~~~~text
### Requirement: Contrat A10i66 — État de reprise technique local durable, protégé et possédé par le parent — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i66 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i66

Circuit/recréations A10i63 A et contrôle courant d'autorisation conservés.
Support local durable A validé, indépendant du contrat IPC ;
aucune décision métier, mandat ou audit rendu autoritatif depuis cet état local.

| Choix validé | Conservation technique | Conséquence après redémarrage du parent |
| --- | --- | --- |
| A | État local durable, protégé et possédé par le parent | Reprise seulement si état et continuité qualifiés, sinon blocage/réconciliation |

Compteur/réservations, état du circuit, instance logique/profil/provider,
génération et références temporelles/domaine de continuité nécessaires
conservés sans réponse de temps, clé, token ou données métier. État borné,
écriture réservée au parent autorisé, auxiliaire de collecte sans droit d'y
modifier son quota ou statut. Réservation de tentative durable avant lancement ;
écriture échouée/incertaine sans lancement autorisé par ce résultat.
Opérations concurrentes sérialisées sans second parent réinitialisant le quota.
Durabilité/atomicité/reprise d'écriture à qualifier par OS, filesystem et profil
physique/VM/Docker/LXC ; renommage atomique ou flush isolé sans preuve suffisante
d'ensemble présumés. Aucun montage, volume, droit ou fichier d'état réel créé ici.
État valide conservant circuit bloqué : aucun réarmement au seul redémarrage.
État absent/corrompu/retourné en arrière/cloné, continuité temporelle inconnue,
ancien processus non exclu ou provenance non vérifiable : blocage et
réconciliation autorisée, jamais zéro tentative implicite. Un fichier lisible
ou une somme de contrôle ne prouvent pas qu'il s'agit du dernier état ; contexte
de reprise/anti-retour à qualifier, aucun TPM ou matériel supplémentaire imposé.
Conservation seulement en mémoire B non retenue comme alternative de reprise ;
perte/incertitude restent bloquantes sous le profil durable A.
Commun : provisionnement initial d'une instance neuve explicitement autorisé,
pas de restauration présentée comme neuve. État local purement technique et
restrictif, PostgreSQL reste vérité métier et Django autorité ; aucun accès
SQL de PA/auxiliaire, audit obligatoire persistant séparé. PBO–PA garde PZT/mTLS.
A10i54/A10i63 restent appliqués, réarmement sans nouvelle admission/durée/permission
métier. I/O/qualification/attente chargées aux budgets A10i52 lorsqu'elles
participent à une acquisition, aucune latence de disque tenue pour nulle.
A validée pour éviter intervention au seul redémarrage quand continuité
prouvée. Format JSON A10i67 et plafond 256 Kio A10i68 validés le 8 octobre 2026.
Moyen exact/support/qualification à définir, aucune technologie concrète
choisie ni OpenSpec modifié.
[Linux, fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html) et
[Microsoft, FlushFileBuffers](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)
documentent des mécanismes de synchronisation ; aucune API sélectionnée ici
ni preuve de résistance aux snapshots/reprises déduite de ces mécanismes seuls.
Recette : panne avant/après réservation, erreur d'I/O, circuit bloqué,
parent redémarré, état ancien/snapshot/clonage, deux parents, temps incertain,
reprise autorisée et aucune remise à zéro implicite.
A10i66 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i66

- **WHEN** un profil revendique le traitement A10i66 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--3ef6d61fb7

Source : `openspec/specs/pzt/spec.md`, ligne 9007. SHA-256 du bloc : `78859165c2513d6f83810ec442872150b61fc5fdfc049f95129cc2223b4cca58`.

~~~~text
### Requirement: Contrat A10i67 — État technique courant en document JSON UTF-8 typé/versionné — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i67 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i67

État local durable A10i66 A, limites de reprise A10i63 A et vérité métier
Django/PostgreSQL conservés. Document courant JSON A validé, indépendant du
plafond de stockage A10i68 et des métriques A10i69.

| Choix validé | Représentation locale | Conséquence |
| --- | --- | --- |
| A | Un document JSON UTF-8 typé/versionné représentant l'état courant complet | Lecture directe de l'état, publication complète durable à qualifier |

Document sans secret ou échantillon de temps, contexte/génération du
parent, compteurs/réservations et blocage nécessaires. Schéma fermé, doublons/
inconnus refusés ; conventions de grands entiers A10i64 explicitement réutilisées
pour ses champs int64/uint64, profondeur/cardinalités à qualifier pour cet état,
sans plafond IPC 16 Kio automatiquement transposé au stockage local.
Publication nouvelle image entière avec réservation durable avant lancement ;
ancien/candidat/engagement et reprise sur panne sans état remis à zéro.
Atomicité, synchronisation, emplacement, exclusion d'écrivains et preuve de
dernier état à qualifier ; fichier valide ou remplacement atomique sans
preuve anti-retour présumés. Aucun chemin/API/procédure de remplacement adopté.
Journal de transitions/checkpoint B non retenu comme représentation
alternative ; publication A10i70 A et exclusion A10i71 A validées le 9 octobre 2026.
Commun : format local technique distinct du dossier A10i38 et des marqueurs
métier A10i44–A10i46 ; aucune compaction de ces derniers autorisée. Audit
persistant requis distinct, snapshot technique sans valeur d'audit.
État absent/ambigu/ancien ou continuité inconnue => blocage A10i66 ; zéro
tentative jamais déduit d'une image manquante. Quotas A10i68 et
budgets A10i52 applicables, aucune I/O ignorée dans acquisition.
A validée pour état restreint à lecture directe. Coûts à mesurer, pas
de gain universel ou preuve de durabilité fournie par JSON.
[RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) définit JSON ; stratégie de
persistance choisie par Pixs. Plateformes et méthodes à qualifier, aucun
fichier d'état réel, backend, migration ou OpenSpec créé/modifié.
Recette : panne de publication, image/candidat incohérents, image partielle/ancienne,
format de journal non admis, état bloqué, compteur réservé et aucune remise à zéro.
A10i67 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i67

- **WHEN** un profil revendique le traitement A10i67 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--84b9058dfd

Source : `openspec/specs/pzt/spec.md`, ligne 9058. SHA-256 du bloc : `a7e279c4b757716931b7f78c5e24681cd75e532a998d01e408d94d7f3cdc2908`.

~~~~text
### Requirement: Contrat A10i68 — Stockage de l'état technique et de sa publication plafonné à 256 Kio — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i68 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i68

État durable A10i66 A maintenu. Plafond A 256 Kio validé comme premier jet
par instance logique de validation,
indépendant du format A10i67 ; ne plafonne ni audit ni stockage métier.

| Choix validé | Plafond total des contenus de l'état et artefacts de publication | Conséquence |
| --- | --- | --- |
| A | 256 Kio | Enveloppe sobre pour compteurs/réservations et remplacement borné |

1 Kio = 1024 octets ; plafond A = 262 144 octets inclusifs.
Plafond B 1 Mio non retenu. Somme des octets exacts de contenu : état courant,
candidat, index et copies temporaires nécessaires à la
publication/reprise possédés dans ce profil. Chaque copie compte, y compris
même contenu répété ; aucun nom de temporaire dispensant du plafond.
Taille logique du contenu, sans disque réellement alloué/overhead filesystem
ou plafond du volume/hôte réputés identiques. Nombre de fichiers/metadata,
quota physique et ressources agrégées PBO/hôte à qualifier séparément.
Contrôle de capacité avant publication, écriture et lecture effectivement
bornées, annonce de taille non autoritative. Dépassement/état incomplet :
refus de nouvelle réservation/recréation et diagnostic ; aucun lancement
fondé sur écriture incertaine, troncature, purge de blocage ou compteur oublié.
Publication/retrait d'artefact technique seulement avec preuve d'état actuel
durable/admissible et profil autorisé ; quota ne permet aucune suppression de
preuve/audit ou ancien marqueur métier. Concurrence et phase transitoire du
remplacement incluses, hausse automatique ou fallback A/B interdits.
Paramètre de premier jet configurable sous profil versionné/habilité et
qualification ; persistance A10i66 toujours requise, quota trop faible
sans données omises pour sembler conforme. RAM de l'auxiliaire A10i59,
message IPC 16 Kio A10i56 et dossier A10i39 distincts.
A validée pour métadonnées restreintes. Pas de consommation observée ou capacité d'un runtime démontrée.
Toutes plateformes à qualifier ; aucun volume/permission/fichier/variable
réelle ou OpenSpec modifiés. Recette : total exact/plus un, même contenu en
plusieurs copies, disque plein, candidat ne tenant pas avec état actuel,
publication interrompue et absence de suppression ou relance permissives.
A10i68 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i68

- **WHEN** un profil revendique le traitement A10i68 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

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

### Référence pzt--5b57318d5a

Source : `openspec/specs/pzt/spec.md`, ligne 9162. SHA-256 du bloc : `b5b4ddce125871d169edbd429e0c9cc317f3dbd01c9b0f07ebbef5c08cbad4ef`.

~~~~text
### Requirement: Contrat A10i70 — Publication de l'état JSON par candidat synchronisé et remplacement atomique — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i70 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i70

Image JSON courante A10i67 A, stockage total 256 Kio A10i68 A et blocage sur
état incertain A10i66 A conservés. Publication par candidat A validée, indépendante du
mécanisme d'exclusion A10i71 et du budget métrique A10i72.

| Choix validé | Publication durable | Conséquence |
| --- | --- | --- |
| A | Candidat complet synchronisé, remplacement atomique et synchronisation des métadonnées nécessaires | Image courante directement accessible, durabilité des étapes à qualifier |

Emplacement protégé possédé par le parent ; candidat distinct de l'image
active, dans le même domaine filesystem qualifié. Contenu exact écrit/validé
et rendu durable, publication atomique puis preuve de durabilité du nom et
métadonnées nécessaires avant réservation confirmée/lancement. Pas d'écriture
en place pouvant laisser image active partielle. Erreur de flush/publication
ou accusé incertain : état réconcilié sous A10i66, jamais lancement ou zéro
tentative déduits d'un retour ambigu. Le candidat complet ne vaut pas à lui
seul état engagé. Remplacement/répertoires/permissions/handles qualifiés par OS,
pas de copie inter-volumes présentée comme remplacement atomique.
Deux emplacements avec sélecteur B non retenus comme stratégie alternative ;
aucune sélection automatique d'image plus ancienne après panne.
Commun : ensemble des artefacts compris dans 256 Kio, aucune sauvegarde infinie
ou suppression de blocage/compteur pour tenir dans le quota. Ancien/candidat/
courant et issue incertaine distingués ; retrait technique sous preuve d'état
actuel admissible et profil autorisé, sans audit/marqueur métier effacés.
Durabilité, exclusion et preuve de dernier état trois contrôles distincts :
aucune stratégie ne détecte seule rollback/snapshot/clonage de l'ensemble.
A10i52 englobe I/O participante ; arrêt/reprise A10i54/A10i63 conservés.
A validée pour publication à image courante directe. Coûts et plateformes
à qualifier ; reprise du parent A10i73 A validée le 9 octobre 2026.
[Linux, rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html) décrit
remplacement atomique, sans garantie de durabilité complète ou équivalence
Windows déduite de cet appel. APIs/ordre exact de synchronisation/profil
Windows à préciser, aucun fichier renommé, montage ou OpenSpec modifiés ici.
Recette : panne entre étapes, état complet non engagé, erreur de synchronisation,
image ancienne, changement de volume, quota et aucune tentative remise à zéro.
A10i70 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i70

- **WHEN** un profil revendique le traitement A10i70 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--33ca2093cb

Source : `openspec/specs/pzt/spec.md`, ligne 9214. SHA-256 du bloc : `f081046f21ab71dfbbbde9a28c7ff328eb2b696e959ed6b46b7e34c743b8a2ae`.

~~~~text
### Requirement: Contrat A10i71 — Exclusion des écrivains par verrou OS sur objet stable distinct — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i71 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i71

Un parent écrivain autorisé A10i66 A et une image JSON A10i67 A conservés.
Exclusion OS locale A validée, distincte de l'exclusion CA A10i12 et de
l'autorité métier A12 ; aucun verrou local ne prouve un commit PostgreSQL.

| Choix validé | Exclusion locale | Conséquence |
| --- | --- | --- |
| A | Verrou exclusif OS sur objet stable distinct de l'image JSON, détenu par le parent | Contrôle inter-processus local, libération/reprise à qualifier |

Objet stable au même périmètre approuvé, non remplacé avec image courante ;
identité filesystem/namespace et droits qualifiés contre substitution/lien/
suppression recréant un verrou distinct. Propriété par handle/descripteur du
parent, acquisition exclusive avant lecture d'état pour décision, réservation,
publication ou recréation d'auxiliaire ; refus borné si possession impossible.
Tous parents autorisés passent par cette exclusion, mutex seulement interne ou
PID dans fichier insuffisants. Héritage au collecteur interdit, fermeture/
terminaison/libération qualifiées. Acquérir le verrou après un crash ne
prouve ni la fin de l'ancien auxiliaire ni l'admissibilité de l'état retrouvé.
Répertoire de possession B non retenu comme mécanisme alternatif ;
aucune suppression d'objet ou attente d'expiration pour contourner un verrou.
Commun : portée par instance logique dans même domaine d'exécution/stockage
qualifié ; VM/conteneurs/partages et locks réseau sans coordination globale
déduite. Profil partageant état entre parents sur plusieurs hôtes non activable
sans preuve d'exclusion adaptée, aucun montage/coordonnateur supplémentaire
admis ici. Perte d'exclusion arrête nouvelles écritures/collectes, issue déjà
incertaine réconciliée, pas de création de parents pour contourner verrou.
L'acquisition du verrou ne déclare aucun mandat/droit, temps ou état actuel
admissible. Contrôles courants et budgets A10i52 s'appliquent sans attente infinie.
A validée pour exclusion OS directe, profils/mécanismes à qualifier.
[Linux, flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) et
[Microsoft, LockFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
documentent des mécanismes possibles, sans API choisie ni résistance à
l'hôte compromis/rollback présumée. Profil exact et objets à qualifier,
aucun lock, commande d'arrêt ou OpenSpec exécutés/modifiés.
Recette : deux parents, objet remplacé, handle hérité, ancien auxiliaire vivant,
crash du détenteur, verrou substitué, partage non qualifié et attente bornée.
A10i71 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i71

- **WHEN** un profil revendique le traitement A10i71 et ses garanties dans un rôle déclaré
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

### Référence pzt--661eb042b1

Source : `openspec/specs/pzt/spec.md`, ligne 9322. SHA-256 du bloc : `ba15df8d035fe5905a20717cc2a4be7f8b87e7abb15af888874b181fa8d69a12`.

~~~~text
### Requirement: Contrat A10i73 — Reprise du parent au même démarrage OS sous continuité complète prouvée — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i73 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i73

État durable A10i66 A, publication A10i70 A et exclusion A10i71 A conservés.
Reprise A validée sous continuité prouvée, indépendante de l'export métrique ; aucun
réarmement automatique d'un circuit bloqué A10i63 autorisé.

| Choix validé | Reprise technique du parent | Conséquence |
| --- | --- | --- |
| A | Reprise automatique possible au même démarrage OS, seulement avec continuité complète prouvée | Moins d'interventions après simple redémarrage du processus, qualification stricte |

Même domaine de démarrage/horloge monotone qualifié, dernière image durable
et réservations admissibles, possession exclusive du nouvel écrivain, fin de
l'ancien parent et absence d'ancien auxiliaire prouvées. Identités/profil/provider,
mandat de collecte et autorisations courants revérifiés, circuit/compteurs
conservés ; reprise d'un état bloqué sans réarmement reste refusée.
Même identifiant de démarrage, PID absent, fichier valide ou horloge monotone
croissante seuls ne prouvent pas absence de snapshot/rollback/clonage.
Continuité du stockage, du contexte d'exécution et du domaine temporel qualifiée
par le profil ; VM/conteneurs suspendus/restaurés/clonés ou provenance incertaine
sans reprise automatique par simple identité OS conservée.
Nouveau démarrage OS, domaine monotone changé ou continuité non démontrée :
blocage et réconciliation explicitement autorisée, aucun compteur remis à zéro
ou temps depuis ancien boot comparé directement au nouveau. Reprise automatique
après reboot OS non adoptée par cette option, sans matériel supplémentaire imposé.
Réconciliation systématique après chaque redémarrage B non retenue ;
blocage/réconciliation requis lorsque continuité ou état ne sont pas prouvés.
Commun : politique/profil de reprise déclarés avant activation, pas de
fallback permissif ; réconciliation et réarmement techniques distincts d'un
nouveau cycle métier. A10i52/D/A10i47–A10i49 inchangés, aucune réponse temporelle
stockée réutilisée comme nouvelle preuve ou reprise d'acquisition expirée.
A validée pour reprise limitée à continuité prouvée. Qualification par Linux/Windows physiques/VM, Docker/LXC,
sans garantie universelle de couverture ou API choisie.
[Linux, horloges](https://man7.org/linux/man-pages/man2/clock_gettime.2.html) et
[Microsoft, GetTickCount64](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64)
documentent des mesures temporelles système ; elles ne constituent pas seules
preuve anti-restauration. Choix validé par Pixs, aucun redémarrage, état,
mandat ou OpenSpec modifiés ici.
Recette : parent redémarré même OS, reboot OS, snapshot avec identité conservée,
ancien auxiliaire vivant, circuit bloqué et refus sans compteur/durée réinitialisés.
A10i73 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i73

- **WHEN** un profil revendique le traitement A10i73 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

